--!strict
-- GATE 0 SPIKE ONLY (branch gate0-spike, never merged). Server bootstrap for the Path A prototype.
-- Creates roots and the input bridge; never calls SetPredictionMode (client-only, D-025).
-- All logging and non-simulation side effects run here, outside BindToSimulation.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Gate0Sim = require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("Gate0Sim"))

local SLOTS = {
	Vector3.new(0, 54.15, -36),
	Vector3.new(36, 54.15, -24),
	Vector3.new(36, 54.15, 24),
	Vector3.new(0, 54.15, 36),
	Vector3.new(-36, 54.15, 24),
	Vector3.new(-36, 54.15, -24),
}

local function podCenter(slot: number): Vector3
	return Vector3.new(2000 + 20 * (slot - 1), 200, 2000)
end

local function log(fmt: string, ...: any)
	print("[G0] " .. string.format(fmt, ...))
end

local function num(inst: Instance, name: string, default: number): number
	local v = inst:GetAttribute(name)
	return if typeof(v) == "number" then v else default
end

local function anchoredPart(name: string, size: Vector3, cframe: CFrame, parent: Instance): Part
	local p = Instance.new("Part")
	p.Name = name
	p.Size = size
	p.CFrame = cframe
	p.Anchored = true
	p.Parent = parent
	return p
end

-- World ----------------------------------------------------------------------------------------
local world = Instance.new("Folder")
world.Name = "Gate0World"
world.Parent = workspace
local floor = anchoredPart("Gate0Floor", Vector3.new(108, 2, 108), CFrame.new(0, 50, 0), world)
floor.CustomPhysicalProperties = PhysicalProperties.new(0.7, 0, 0, 100, 100)
floor.Color = Color3.fromRGB(32, 38, 54)
local focusPart = anchoredPart("Gate0ArenaFocus", Vector3.one, CFrame.new(0, 51, 0), world)
focusPart.Transparency = 1
focusPart.CanCollide = false
focusPart.CanQuery = false
focusPart.CanTouch = false
for slot = 1, #SLOTS do
	anchoredPart(
		"Gate0Pod" .. slot,
		Vector3.new(10, 1, 10),
		CFrame.new(podCenter(slot) - Vector3.new(0, 0.5, 0)),
		world
	)
end
local spheres = Instance.new("Folder")
spheres.Name = "Gate0Spheres"
spheres.Parent = workspace
local bogus = Instance.new("RemoteEvent")
bogus.Name = "Gate0Bogus"
bogus.Parent = ReplicatedStorage
-- Test-only evidence channel: clients forward their [G0C] log lines so one Server Output holds all evidence.
-- Data only: never affects simulation state; length- and rate-capped.
local clientLog = Instance.new("RemoteEvent")
clientLog.Name = "Gate0ClientLog"
clientLog.Parent = ReplicatedStorage
-- Per-player one-second budget; dropped messages are counted and reported (RV-01 L6).
type LogBudget = { count: number, window: number, dropped: number }
local function withinBudget(budgets: { [Player]: LogBudget }, player: Player, limit: number, label: string): boolean
	local now = os.clock()
	local budget: LogBudget = budgets[player] or { count = 0, window = now, dropped = 0 }
	if now - budget.window >= 1 then
		if budget.dropped > 0 then
			print(string.format("[G0] %s uid=%d: %d dropped by rate limit", label, player.UserId, budget.dropped))
		end
		budget.count, budget.window, budget.dropped = 0, now, 0
	end
	budgets[player] = budget
	budget.count += 1
	if budget.count > limit then
		budget.dropped += 1
		return false
	end
	return true
end
local clientLogBudget: { [Player]: LogBudget } = {}
local bogusBudget: { [Player]: LogBudget } = {}
clientLog.OnServerEvent:Connect(function(player: Player, line: any)
	if typeof(line) ~= "string" or not withinBudget(clientLogBudget, player, 30, "client log") then
		return
	end
	print(string.format("[G0C<-%d] %s", player.UserId, string.sub(line, 1, 400)))
end)
Players.PlayerRemoving:Connect(function(player: Player)
	clientLogBudget[player] = nil
	bogusBudget[player] = nil
end)

-- Per-player state ---------------------------------------------------------------------------
type SavedAvatar = {
	character: Model,
	parts: { [BasePart]: number },
	decals: { [Decal]: number },
	hrp: BasePart,
	hrpAnchored: boolean,
	walkSpeed: number,
	jumpPower: number,
	jumpHeight: number,
}
local saved: { [Player]: SavedAvatar } = {}
local roots: { [Player]: BasePart } = {}
local roundConns: { [Player]: { RBXScriptConnection } } = {}
local seen: { [BasePart]: { hit: number, kick: number, elim: boolean } } = {}
local restoreCount: { [Player]: number } = {}
local maxSpeed: { [BasePart]: number } = {}

local function forgetRoot(root: BasePart)
	seen[root] = nil
	maxSpeed[root] = nil -- RV-01 L4
end

local function connCount(): number
	local n = 0
	for _, list in roundConns do
		n += #list
	end
	return n
end

local function disconnectRound(player: Player)
	local list = roundConns[player]
	if list then
		for _, c in list do
			c:Disconnect()
		end
	end
	roundConns[player] = nil
end

local function savedCount(): number
	local n = 0
	for _ in saved do
		n += 1
	end
	return n
end

local function freeSlot(player: Player): number
	local sorted = Players:GetPlayers()
	table.sort(sorted, function(a, b)
		return a.UserId < b.UserId
	end)
	local used: { [number]: boolean } = {}
	for p, root in roots do
		if p ~= player then
			used[num(root, "Slot", 0)] = true
		end
	end
	local preferred = table.find(sorted, player) or 1
	if not used[preferred] and SLOTS[preferred] then
		return preferred
	end
	for slot = 1, #SLOTS do
		if not used[slot] then
			return slot
		end
	end
	return 1
end

local function ensureInputBridge(player: Player)
	if player:FindFirstChild("Gate0Input") then
		return
	end
	local ctx = Instance.new("InputContext")
	ctx.Name = "Gate0Input"
	local action = Instance.new("InputAction")
	action.Name = "Move"
	action.Type = Enum.InputActionType.Direction2D
	action.Parent = ctx
	local bridge = Instance.new("InputBinding")
	bridge.Name = "Bridge"
	bridge.Type = Enum.InputBindingType.Scriptable
	bridge.Parent = action
	ctx.Parent = player
end

local function park(player: Player, character: Model, slot: number)
	local hrp = character:WaitForChild("HumanoidRootPart", 10)
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	if not (hrp and hrp:IsA("BasePart") and humanoid) then
		log("park FAIL uid=%d: character incomplete", player.UserId)
		return
	end
	local previous = saved[player]
	if previous then -- a new character while parked: release the old extra focus (RV-01 L4)
		player:RemoveReplicationFocus(previous.hrp)
	end
	local rec: SavedAvatar = {
		character = character,
		parts = {},
		decals = {},
		hrp = hrp,
		hrpAnchored = hrp.Anchored,
		walkSpeed = humanoid.WalkSpeed,
		jumpPower = humanoid.JumpPower,
		jumpHeight = humanoid.JumpHeight,
	}
	for _, d in character:GetDescendants() do
		if d:IsA("BasePart") then
			rec.parts[d] = d.Transparency
			d.Transparency = 1
		elseif d:IsA("Decal") then
			rec.decals[d] = d.Transparency
			d.Transparency = 1
		end
	end
	humanoid.WalkSpeed = 0
	humanoid.JumpPower = 0
	humanoid.JumpHeight = 0
	hrp.Anchored = true
	character:PivotTo(CFrame.new(podCenter(slot) + Vector3.new(0, 3, 0)))
	-- FAIL-009 experiment (proposed D-023 amendment, not yet approved): keep the parked avatar streamed on its
	-- owner's client with an extra replication focus while ReplicationFocus follows the sphere.
	player:AddReplicationFocus(hrp)
	saved[player] = rec
	log("park uid=%d slot=%d pod=%s extraFocus=HRP", player.UserId, slot, tostring(podCenter(slot)))
end

local spawnCounter = 0
local function spawnRound(player: Player)
	if roots[player] then
		-- Deliberate guard (RV-01 L2): an eliminated player's record stays until restore; respawning first would
		-- save the hidden avatar as its "original" appearance.
		log("respawn skipped uid=%d: round record exists; restore first", player.UserId)
		return
	end
	spawnCounter += 1
	ensureInputBridge(player)
	local slot = freeSlot(player)
	local root = Instance.new("Part")
	root.Name = tostring(player.UserId)
	root.Shape = Enum.PartType.Ball
	root.Size = Vector3.one * Gate0Sim.DIAMETER
	root.CFrame = CFrame.new(SLOTS[slot])
	root.CustomPhysicalProperties = PhysicalProperties.new(1, 0, 0, 100, 100)
	root.Transparency = 0.25
	root.Color = if slot % 2 == 1 then Color3.fromRGB(0, 195, 255) else Color3.fromRGB(255, 125, 0)
	root:SetAttribute("OwnerUserId", player.UserId)
	root:SetAttribute("SpawnId", spawnCounter) -- lets presentation tell a respawned root from a streamed-back one
	root:SetAttribute("Slot", slot)
	root:SetAttribute("SpawnPos", SLOTS[slot])
	root:SetAttribute("HitSeq", 0)
	root:SetAttribute("KickSeq", 0)
	root:SetAttribute("LastHitBy", 0)
	root:SetAttribute("LastHitAt", -1)
	root:SetAttribute("Eliminated", false)
	root.Parent = spheres
	roots[player] = root
	seen[root] = { hit = 0, kick = 0, elim = false }
	roundConns[player] = {}

	local ok, err = pcall(function()
		root:SetNetworkOwner(player)
	end)
	log("SetNetworkOwner(player) probe uid=%d ok=%s err=%s", player.UserId, tostring(ok), tostring(err))
	player.ReplicationFocus = root

	local function onCharacter(character: Model)
		park(player, character, slot)
	end
	if player.Character then
		task.spawn(onCharacter, player.Character)
	end
	table.insert(roundConns[player], player.CharacterAdded:Connect(onCharacter))
	log("spawn uid=%d slot=%d pos=%s conns=%d", player.UserId, slot, tostring(SLOTS[slot]), connCount())
end

local function restore(player: Player)
	local rec = saved[player]
	local mismatches = 0
	if rec then
		local humanoid = rec.character:FindFirstChildOfClass("Humanoid")
		local hrp = rec.character:FindFirstChild("HumanoidRootPart")
		for part, t in rec.parts do
			if part.Parent then
				part.Transparency = t
			end
		end
		for decal, t in rec.decals do
			if decal.Parent then
				decal.Transparency = t
			end
		end
		if humanoid then
			humanoid.WalkSpeed = rec.walkSpeed
			humanoid.JumpPower = rec.jumpPower
			humanoid.JumpHeight = rec.jumpHeight
		end
		if hrp and hrp:IsA("BasePart") then
			hrp.Anchored = rec.hrpAnchored
		end
		player:RemoveReplicationFocus(rec.hrp)
		local spawn = workspace:FindFirstChildOfClass("SpawnLocation")
		rec.character:PivotTo(CFrame.new((if spawn then spawn.Position else Vector3.zero) + Vector3.new(0, 4, 0)))
		for part, t in rec.parts do
			if part.Parent and part.Transparency ~= t then
				mismatches += 1
			end
		end
		if humanoid and (humanoid.WalkSpeed ~= rec.walkSpeed or humanoid.JumpPower ~= rec.jumpPower) then
			mismatches += 1
		end
	end
	saved[player] = nil
	player.ReplicationFocus = nil
	local root = roots[player]
	if root then
		forgetRoot(root)
		root:Destroy()
	end
	roots[player] = nil
	disconnectRound(player)
	restoreCount[player] = (restoreCount[player] or 0) + 1
	player:SetAttribute("Gate0Restored", restoreCount[player])
	log(
		"C5 restore uid=%d hadRecord=%s mismatches=%d focusNil=%s savedRecords=%d roundConns=%d",
		player.UserId,
		tostring(rec ~= nil),
		mismatches,
		tostring(player.ReplicationFocus == nil),
		savedCount(),
		connCount()
	)
end

local function report(tag: string)
	for player, root in roots do
		local v = root.AssemblyLinearVelocity
		local ctx = player:FindFirstChild("Gate0Input")
		local action = ctx and ctx:FindFirstChild("Move")
		local rawState = if action and action:IsA("InputAction") then action:GetState() else nil
		log(
			"report %s uid=%d pos=(%.2f,%.2f,%.2f) hspeed=%.2f rawMove=%s clampedMove=%s hit=%d kick=%d elim=%s focus=%s",
			tag,
			player.UserId,
			root.Position.X,
			root.Position.Y,
			root.Position.Z,
			Vector3.new(v.X, 0, v.Z).Magnitude,
			tostring(rawState),
			tostring(Gate0Sim.readMove(player)),
			num(root, "HitSeq", 0),
			num(root, "KickSeq", 0),
			tostring(root:GetAttribute("Eliminated")),
			tostring(player.ReplicationFocus)
		)
		-- A4 reference on the Player (not predicted, so its change signal fires); the sequence number makes a
		-- repeated identical position still produce a change (RV-01 B1/M1).
		player:SetAttribute("Gate0RefPos", root.Position)
		player:SetAttribute("Gate0RefSeq", num(player, "Gate0RefSeq", 0) + 1)
	end
	local steps, resim = Gate0Sim.counters()
	log(
		"report %s server simSteps=%d resimSteps=%d savedRecords=%d roundConns=%d",
		tag,
		steps,
		resim,
		savedCount(),
		connCount()
	)
end

-- Commands (set from the MCP Server datamodel or the Server Command Bar): workspace.Gate0Cmd = "<verb>#<n>"
workspace:GetAttributeChangedSignal("Gate0Cmd"):Connect(function()
	local value = workspace:GetAttribute("Gate0Cmd")
	if typeof(value) ~= "string" then
		return
	end
	local verb = string.match(value, "^(%a+)") or ""
	log("cmd %s", value)
	if verb == "report" then
		report(value)
	elseif verb == "reset" then
		Gate0Sim.requestReset()
	elseif verb == "restore" then
		for _, player in Players:GetPlayers() do
			restore(player)
		end
	elseif verb == "respawn" then
		for _, player in Players:GetPlayers() do
			spawnRound(player)
		end
	end
end)

bogus.OnServerEvent:Connect(function(player: Player, ...: any)
	if not withinBudget(bogusBudget, player, 10, "bogus claims") then
		return
	end
	local args = table.pack(...)
	local parts = {}
	for i = 1, args.n do
		table.insert(parts, tostring(args[i]))
	end
	log("C3 bogus claim from uid=%d ignored (args: %s)", player.UserId, table.concat(parts, ", "))
end)

-- Observer outside the simulation: logs sequence changes once and handles elimination side effects.
RunService.Heartbeat:Connect(function()
	for player, root in roots do
		local state = seen[root]
		if not state then
			continue
		end
		local v = root.AssemblyLinearVelocity
		local hspeed = Vector3.new(v.X, 0, v.Z).Magnitude
		maxSpeed[root] = math.max(maxSpeed[root] or 0, hspeed)
		local hit, kick = num(root, "HitSeq", 0), num(root, "KickSeq", 0)
		if hit ~= state.hit then
			state.hit = hit
			local closing = num(root, "HitClosing", 0)
			log(
				"hit victim=%d seq=%d by=%d closing=%.2f deltaV=%.2f expected=%.2f",
				player.UserId,
				hit,
				num(root, "LastHitBy", 0),
				closing,
				num(root, "HitDeltaV", -1),
				Gate0Sim.knockback(closing)
			)
		end
		if kick ~= state.kick then
			state.kick = kick
			log("kick uid=%d seq=%d hspeed=%.2f", player.UserId, kick, hspeed)
		end
		if root:GetAttribute("Eliminated") == true and not state.elim then
			state.elim = true
			log(
				"ELIM uid=%d credit=%d y=%.2f maxHSpeed=%.2f",
				player.UserId,
				num(root, "KOCredit", 0),
				root.Position.Y,
				maxSpeed[root] or 0
			)
			local target: Instance = focusPart
			for other, otherRoot in roots do
				if other ~= player and otherRoot:GetAttribute("Eliminated") ~= true then
					target = otherRoot
				end
			end
			player.ReplicationFocus = target
			task.delay(0.5, function()
				if roots[player] == root then
					forgetRoot(root)
					root:Destroy()
					log("ELIM root destroyed uid=%d focus=%s", player.UserId, tostring(player.ReplicationFocus))
				end
			end)
		end
	end
end)

Players.PlayerAdded:Connect(spawnRound)
for _, player in Players:GetPlayers() do
	task.spawn(spawnRound, player)
end
Players.PlayerRemoving:Connect(function(player: Player)
	local root = roots[player]
	if root then
		forgetRoot(root)
		root:Destroy()
	end
	roots[player] = nil
	local rec = saved[player]
	if rec then
		player:RemoveReplicationFocus(rec.hrp) -- D-026 proposal: no extra focus survives a disconnect (RV-01 L4)
	end
	saved[player] = nil
	restoreCount[player] = nil
	disconnectRound(player)
	log(
		"C5 disconnect cleanup uid=%d remainingRoots=%d savedRecords=%d roundConns=%d",
		player.UserId,
		#spheres:GetChildren(),
		savedCount(),
		connCount()
	)
end)

Gate0Sim.init()
log("server ready authority-probe: see SetNetworkOwner lines; studio=%s", tostring(RunService:IsStudio()))
