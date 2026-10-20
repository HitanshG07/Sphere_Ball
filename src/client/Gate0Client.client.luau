--!strict
-- GATE 0 SPIKE ONLY (branch gate0-spike, never merged). Client harness for the Path A prototype.
-- D-025: SetPredictionMode is called here (client-only); input reaches the simulation through the
-- world-space Scriptable bridge; presentation and logging stay outside BindToSimulation.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Gate0Sim = require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("Gate0Sim"))
Gate0Sim.init()

local player = Players.LocalPlayer
local camera = workspace.CurrentCamera
local spheres = workspace:WaitForChild("Gate0Spheres")
local bogus = ReplicatedStorage:WaitForChild("Gate0Bogus") :: RemoteEvent

local clientLog = ReplicatedStorage:WaitForChild("Gate0ClientLog") :: RemoteEvent
local function log(fmt: string, ...: any)
	local line = string.format(fmt, ...)
	print("[G0C] " .. line)
	clientLog:FireServer(line) -- test-only evidence forwarding (data only on the server)
end

local function num(inst: Instance, name: string, default: number): number
	local v = inst:GetAttribute(name)
	return if typeof(v) == "number" then v else default
end

-- Counters (observed outside the simulation) -----------------------------------------------------
local rollbacks, mispredictions = 0, 0
local rawFx, uniqueFx = 0, 0
local maxCorrection, maxRoll = 0, 0
RunService.Rollback:Connect(function()
	rollbacks += 1
end)
-- FAIL-007: Misprediction needs plugin/Open Cloud capability; a LocalScript may not connect it.
local mispredictionOk, mispredictionErr = pcall(function()
	RunService.Misprediction:Connect(function(t: number, instances: { any }, stats: { [string]: any })
		mispredictions += 1
		if mispredictions <= 3 then
			local keys = {}
			for k, v in stats do
				table.insert(keys, tostring(k) .. "=" .. tostring(v))
			end
			log(
				"misprediction #%d t=%.3f instances=%d stats={%s}",
				mispredictions,
				t,
				#instances,
				table.concat(keys, ", ")
			)
		end
	end)
end)
log("Misprediction connectable=%s err=%s", tostring(mispredictionOk), tostring(mispredictionErr))

-- FAIL-008: on a predicted root the server-written sequence attributes replicate (GetAttribute is current)
-- but GetAttributeChangedSignal does not fire. Presentation therefore polls the simulation results once per
-- rendered frame and presents each sequence number at most once (D-025). The signal counter is kept only as
-- evidence of that engine behaviour.
local signalFx = 0
local regressions = 0 -- observed value moved backwards (for example during a rollback)
local FX_ATTRS = { "HitSeq", "KickSeq" }
-- Keys include the server's SpawnId: a respawned root starts a fresh sequence, while a root that streams out and
-- back in keeps its key, so its sequence numbers are never presented twice (RV-01 M3).
local lastValue: { [string]: number } = {}
local presented: { [string]: number } = {} -- highest sequence number already presented per root spawn/attribute
local function watchFx(root: Instance)
	for _, attr in FX_ATTRS do
		root:GetAttributeChangedSignal(attr):Connect(function()
			signalFx += 1
		end)
	end
end
for _, root in spheres:GetChildren() do
	watchFx(root)
end
spheres.ChildAdded:Connect(watchFx)
RunService.PreRender:Connect(function()
	for _, root in spheres:GetChildren() do
		for _, attr in FX_ATTRS do
			local value = num(root, attr, 0)
			local key = root.Name .. ":" .. tostring(root:GetAttribute("SpawnId")) .. ":" .. attr
			local last = lastValue[key] or 0
			if value ~= last then
				rawFx += 1
				if value < last then
					regressions += 1
				end
				lastValue[key] = value
			end
			-- Present every sequence number at most once, even if the value regresses and returns.
			local done = presented[key] or 0
			if value > done then
				uniqueFx += value - done
				presented[key] = value
			end
		end
	end
end)

-- Hardware input: client-only context (never replicated) --------------------------------------------
local hardware = Instance.new("InputContext")
hardware.Name = "Gate0Hardware"
local hwMove = Instance.new("InputAction")
hwMove.Name = "HwMove"
hwMove.Type = Enum.InputActionType.Direction2D
hwMove.Parent = hardware
local keys = Instance.new("InputBinding")
keys.Up = Enum.KeyCode.W
keys.Down = Enum.KeyCode.S
keys.Left = Enum.KeyCode.A
keys.Right = Enum.KeyCode.D
keys.Parent = hwMove
local stick = Instance.new("InputBinding")
stick.KeyCode = Enum.KeyCode.Thumbstick1
stick.Parent = hwMove
hardware.Parent = player

-- Production mapping (D-025): camera-relative hardware input -> world-space Vector2(x, z).
local function hardwareWorldMove(): Vector2
	local raw = hwMove:GetState()
	if typeof(raw) ~= "Vector2" then
		return Vector2.zero
	end
	local look = camera.CFrame.LookVector
	local forward = Vector3.new(look.X, 0, look.Z)
	forward = if forward.Magnitude < 1e-3 then Vector3.zAxis else forward.Unit
	local right = forward:Cross(Vector3.yAxis)
	local world = right * raw.X + forward * raw.Y
	local m = Vector2.new(world.X, world.Z)
	return if m.Magnitude > 1 then m.Unit else m
end

-- AutoDrive: Studio-gated test source feeding the same bridge -------------------------------------------
local AUTODRIVE_LIMIT = { Forward = 1.5, Oversize = 1.5, EdgeFall = 3, HeadOn = 4, Hold = 12 }
local autoRun, autoMode, autoStart = 0, "", 0
local autoHits: { [Instance]: number } = {}
local consumedRuns: { [number]: boolean } = {}
local firstMoveFrame: number? = nil
local a3Armed = false -- measure A3 once per AutoDrive run
local frame = 0

local function liveOthers(own: BasePart): { BasePart }
	local list = {}
	for _, r in spheres:GetChildren() do
		if r:IsA("BasePart") and r ~= own and r:GetAttribute("Eliminated") ~= true then
			table.insert(list, r)
		end
	end
	return list
end

local function autoDriveVector(own: BasePart): Vector2?
	if not RunService:IsStudio() then
		return nil
	end
	local run = workspace:GetAttribute("Gate0AutoDrive")
	if typeof(run) ~= "number" then
		autoRun = 0
		return nil
	end
	if run ~= autoRun then
		if consumedRuns[run] then
			return nil
		end
		consumedRuns[run] = true
		autoRun = run
		local mode = workspace:GetAttribute("Gate0AutoDriveMode")
		autoMode = if typeof(mode) == "string" then mode else "Hold"
		autoStart = os.clock()
		table.clear(autoHits)
		for _, r in spheres:GetChildren() do
			autoHits[r] = num(r, "HitSeq", 0)
		end
		firstMoveFrame = nil
		a3Armed = true
		log("autodrive start run=%d mode=%s frame=%d", run, autoMode, frame)
	end
	if autoRun == 0 then
		return nil
	end
	local hitChanged = false
	for r, seq in autoHits do
		if r.Parent and num(r, "HitSeq", 0) ~= seq then
			hitChanged = true
		end
	end
	local limit = AUTODRIVE_LIMIT[autoMode] or 4
	if hitChanged or os.clock() - autoStart > limit then
		log("autodrive stop run=%d mode=%s reason=%s", autoRun, autoMode, if hitChanged then "hit" else "time")
		autoRun = 0
		return Vector2.zero
	end
	if autoMode == "Forward" then
		return Vector2.new(0, 1)
	elseif autoMode == "Oversize" then
		return Vector2.new(0, 10) -- deliberately oversized; the simulation must clamp it to a unit input
	elseif autoMode == "EdgeFall" then
		return Vector2.new(0, -1)
	elseif autoMode == "HeadOn" then
		local nearest: BasePart? = nil
		for _, r in liveOthers(own) do
			if not nearest or (r.Position - own.Position).Magnitude < (nearest.Position - own.Position).Magnitude then
				nearest = r
			end
		end
		if not nearest then
			return Vector2.zero
		end
		local d = Vector3.new(nearest.Position.X - own.Position.X, 0, nearest.Position.Z - own.Position.Z)
		if d.Magnitude < 0.01 then
			return Vector2.zero
		end
		local u = d.Unit
		return Vector2.new(u.X, u.Z)
	end
	return Vector2.zero
end

-- Round binding (re-entrant: every own root that appears gets one fresh set of connections) ------------
local roundConns: { RBXScriptConnection } = {}
local bindGeneration = 0 -- bumped on every unbind; a bind that yielded across an unbind abandons itself (RV-01 L3)
local ignoreCorrectionUntil = 0 -- reset teleports are not corrections (RV-01 M2)
local function unbindRound(reason: string)
	bindGeneration += 1
	for _, c in roundConns do
		c:Disconnect()
	end
	table.clear(roundConns)
	autoRun = 0 -- an AutoDrive run never carries over to a new root
	log("unbind reason=%s roundConns=%d", reason, #roundConns)
end

local function bindRound(root: BasePart)
	unbindRound("rebind")
	local generation = bindGeneration
	local function stale(): boolean
		return generation ~= bindGeneration or root.Parent == nil
	end
	RunService:SetPredictionMode(root, Enum.PredictionMode.On)
	local t0 = os.clock()
	local status = RunService:GetPredictionStatus(root)
	while status ~= Enum.PredictionStatus.Predicted and os.clock() - t0 < 5 and not stale() do
		task.wait(0.1)
		status = RunService:GetPredictionStatus(root)
	end
	log("A2 uid=%d own=%s status=%s after=%.2fs", player.UserId, root.Name, status.Name, os.clock() - t0)

	local ctx = player:WaitForChild("Gate0Input")
	local bridge = ctx:WaitForChild("Move"):WaitForChild("Bridge") :: InputBinding
	if stale() then
		log("bind abandoned: root replaced or restored while binding")
		return
	end
	local eliminated = false
	local spectating: BasePart? = nil
	camera.CameraType = Enum.CameraType.Scriptable
	local camPos = root.Position + Vector3.new(0, 9, -18)
	local lastPos, lastVel = root.Position, root.AssemblyLinearVelocity

	table.insert(
		roundConns,
		RunService.PreRender:Connect(function(dt: number)
			frame += 1
			-- Input bridge (outside the simulation).
			if not eliminated then
				local auto = autoDriveVector(root)
				local move = if auto then auto else hardwareWorldMove()
				bridge:Fire(move)
				if a3Armed and auto and auto.Magnitude > 0 then
					a3Armed = false
					firstMoveFrame = frame
				end
				local v = root.AssemblyLinearVelocity
				if firstMoveFrame and Vector3.new(v.X, 0, v.Z).Magnitude > 0.5 then
					log("A3 response frames=%d", frame - firstMoveFrame)
					firstMoveFrame = nil
				end
			end
			-- Correction estimate (approximation: predicted position vs last position + velocity * dt).
			if root.Parent then
				local expected = lastPos + lastVel * dt
				if os.clock() >= ignoreCorrectionUntil then
					maxCorrection = math.max(maxCorrection, (root.Position - expected).Magnitude)
				end
				lastPos, lastVel = root.Position, root.AssemblyLinearVelocity
			end
			-- Camera: position-only follow, no roll.
			local target: BasePart = if spectating and spectating.Parent then spectating else root
			local focus = target.Position + Vector3.new(0, 2, 0)
			camPos = camPos:Lerp(focus + Vector3.new(0, 7, -18), 1 - math.exp(-8 * dt))
			camera.CFrame = CFrame.lookAt(camPos, focus)
			maxRoll = math.max(maxRoll, math.abs(camera.CFrame.RightVector.Y))
		end)
	)
	table.insert(
		roundConns,
		root:GetAttributeChangedSignal("Eliminated"):Connect(function()
			if root:GetAttribute("Eliminated") == true and not eliminated then
				eliminated = true
				bridge:Fire(Vector2.zero)
				hardware.Enabled = false
				local others = liveOthers(root)
				spectating = others[1]
				local focus = workspace:FindFirstChild("Gate0World")
				focus = focus and focus:FindFirstChild("Gate0ArenaFocus")
				if not spectating and focus and focus:IsA("BasePart") then
					spectating = focus
				end
				log(
					"C5 eliminated: input unbound hardwareEnabled=%s spectating=%s",
					tostring(hardware.Enabled),
					tostring(spectating)
				)
			end
		end)
	)
end

local function ownRootAdded(child: Instance)
	if child.Name == tostring(player.UserId) and child:IsA("BasePart") then
		hardware.Enabled = true
		task.spawn(bindRound, child)
	end
end
spheres.ChildAdded:Connect(ownRootAdded)
local existing = spheres:FindFirstChild(tostring(player.UserId))
if existing then
	ownRootAdded(existing)
end

-- Restore (server signals via a Player attribute) ------------------------------------------------------
player:GetAttributeChangedSignal("Gate0Restored"):Connect(function()
	unbindRound("restore")
	camera.CameraType = Enum.CameraType.Custom
	local humanoid = player.Character and player.Character:FindFirstChildOfClass("Humanoid")
	if humanoid then
		camera.CameraSubject = humanoid
	end
	log(
		"C5 client restore cameraType=%s subjectIsHumanoid=%s roundConns=%d",
		camera.CameraType.Name,
		tostring(humanoid ~= nil and camera.CameraSubject == humanoid),
		#roundConns
	)
end)

-- Commands mirrored from the server: report and tamper ----------------------------------------------
workspace:GetAttributeChangedSignal("Gate0Cmd"):Connect(function()
	local value = workspace:GetAttribute("Gate0Cmd")
	if typeof(value) ~= "string" then
		return
	end
	local verb = string.match(value, "^(%a+)") or ""
	if verb == "report" then
		local steps, resim = Gate0Sim.counters()
		local statuses = {}
		for _, r in spheres:GetChildren() do
			table.insert(statuses, r.Name .. ":" .. RunService:GetPredictionStatus(r).Name)
		end
		log(
			"report %s uid=%d rollbacks=%d mispredictions=%d simSteps=%d resimSteps=%d maxCorrectionSinceLastReport=%.3f rawFx=%d uniqueFx=%d signalFx=%d regressions=%d maxCameraRollY=%.5f predictionStatus=[%s]",
			value,
			player.UserId,
			rollbacks,
			mispredictions,
			steps,
			resim,
			maxCorrection,
			rawFx,
			uniqueFx,
			signalFx,
			regressions,
			maxRoll,
			table.concat(statuses, ", ")
		)
		maxCorrection = 0 -- per-interval metric (RV-01 M2)
	elseif verb == "reset" then
		ignoreCorrectionUntil = os.clock() + 0.75
	elseif verb == "tamper" then
		for _, r in spheres:GetChildren() do
			if r:IsA("BasePart") then
				r.AssemblyLinearVelocity = Vector3.new(0, 150, 0) -- local write outside the simulation
				bogus:FireServer("KO", r.Name, { closing = 99, victim = r.Name })
			end
		end
		log("C3 tamper sent uid=%d", player.UserId)
	end
end)

-- A4: measure when the server's reference position for this player arrives. The Player is not predicted, so its
-- attribute signal fires; the sequence number changes on every report even if the position does not.
player:GetAttributeChangedSignal("Gate0RefSeq"):Connect(function()
	local ref = player:GetAttribute("Gate0RefPos")
	local own = spheres:FindFirstChild(tostring(player.UserId))
	if typeof(ref) == "Vector3" and own and own:IsA("BasePart") then
		local v = own.AssemblyLinearVelocity
		log(
			"A4 refSeq=%s refPosDelta=%.3f ownHSpeed=%.2f ping=%.3f status=%s",
			tostring(player:GetAttribute("Gate0RefSeq")),
			(own.Position - ref).Magnitude,
			Vector3.new(v.X, 0, v.Z).Magnitude,
			player:GetNetworkPing(),
			RunService:GetPredictionStatus(own).Name
		)
	end
end)

log("client ready uid=%d studio=%s", player.UserId, tostring(RunService:IsStudio()))
