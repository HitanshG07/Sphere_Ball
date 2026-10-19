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

local function log(fmt: string, ...: any)
	print("[G0C] " .. string.format(fmt, ...))
end

local function num(inst: Instance, name: string, default: number): number
	local v = inst:GetAttribute(name)
	return if typeof(v) == "number" then v else default
end

-- Counters (observed outside the simulation) -----------------------------------------------------
local rollbacks, mispredictions = 0, 0
local rawFx, uniqueFx = 0, 0
local fxSeen: { [string]: boolean } = {}
local maxCorrection, maxRoll = 0, 0
RunService.Rollback:Connect(function()
	rollbacks += 1
end)
RunService.Misprediction:Connect(function(t: number, instances: { any }, stats: { [string]: any })
	mispredictions += 1
	if mispredictions <= 3 then
		local keys = {}
		for k, v in stats do
			table.insert(keys, tostring(k) .. "=" .. tostring(v))
		end
		log("misprediction #%d t=%.3f instances=%d stats={%s}", mispredictions, t, #instances, table.concat(keys, ", "))
	end
end)

local function watchFx(root: Instance)
	for _, attr in { "HitSeq", "KickSeq" } do
		root:GetAttributeChangedSignal(attr):Connect(function()
			rawFx += 1
			local key = root.Name .. ":" .. attr .. ":" .. tostring(root:GetAttribute(attr))
			if not fxSeen[key] then
				fxSeen[key] = true
				uniqueFx += 1
			end
		end)
	end
end
for _, root in spheres:GetChildren() do
	watchFx(root)
end
spheres.ChildAdded:Connect(watchFx)

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
local function unbindRound(reason: string)
	for _, c in roundConns do
		c:Disconnect()
	end
	table.clear(roundConns)
	log("unbind reason=%s roundConns=%d", reason, #roundConns)
end

local function bindRound(root: BasePart)
	unbindRound("rebind")
	RunService:SetPredictionMode(root, Enum.PredictionMode.On)
	local t0 = os.clock()
	local status = RunService:GetPredictionStatus(root)
	while status ~= Enum.PredictionStatus.Predicted and os.clock() - t0 < 5 do
		task.wait(0.1)
		status = RunService:GetPredictionStatus(root)
	end
	log("A2 uid=%d own=%s status=%s after=%.2fs", player.UserId, root.Name, status.Name, os.clock() - t0)

	local ctx = player:WaitForChild("Gate0Input")
	local bridge = ctx:WaitForChild("Move"):WaitForChild("Bridge") :: InputBinding
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
				if auto and auto.Magnitude > 0 and not firstMoveFrame then
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
				maxCorrection = math.max(maxCorrection, (root.Position - expected).Magnitude)
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
		local own = spheres:FindFirstChild(tostring(player.UserId))
		local ref = workspace:GetAttribute("Gate0RefPos_" .. player.UserId)
		local refDelta = if own
				and own:IsA("BasePart")
				and typeof(ref) == "Vector3"
			then string.format("%.3f", (own.Position - ref).Magnitude)
			else "n/a"
		log(
			"report %s uid=%d rollbacks=%d mispredictions=%d simSteps=%d resimSteps=%d maxCorrection=%.3f rawFx=%d uniqueFx=%d maxCameraRollY=%.5f refPosDelta=%s",
			value,
			player.UserId,
			rollbacks,
			mispredictions,
			steps,
			resim,
			maxCorrection,
			rawFx,
			uniqueFx,
			maxRoll,
			refDelta
		)
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

log("client ready uid=%d studio=%s", player.UserId, tostring(RunService:IsStudio()))
