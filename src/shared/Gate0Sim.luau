--!strict
-- GATE 0 SPIKE ONLY (branch gate0-spike, never merged). Shared simulation bound on client and server.
-- D-025: this callback writes synchronized state only. No print, FX, sound, remote or instance creation.
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local Gate0Sim = {}

Gate0Sim.ACCEL = 85
Gate0Sim.TOP_SPEED = 42
Gate0Sim.HARD_CAP = 55
Gate0Sim.DRAG = 1.8
Gate0Sim.DIAMETER = 6
Gate0Sim.MIN_CLOSING = 10
Gate0Sim.KNOCK_SCALE = 1.15
Gate0Sim.KNOCK_MAX = 32
Gate0Sim.RECOIL = 0.25
Gate0Sim.PAIR_COOLDOWN = 0.35
Gate0Sim.VOID_Y = 15
Gate0Sim.KO_WINDOW = 5
Gate0Sim.KICK_SPEED = 20

local isServer = RunService:IsServer()
local started = false
local resetRequested = false
local totalSteps = 0
local resimSteps = 0 -- test instrumentation: plain Lua counter, no instance or IO
local lastKickRun = 0 -- server only
local lastHitAt: { [string]: number } = {} -- server only

local function horizontal(v: Vector3): Vector3
	return Vector3.new(v.X, 0, v.Z)
end

local function capHorizontal(v: Vector3, cap: number): Vector3
	local h = horizontal(v)
	if h.Magnitude > cap then
		h = h.Unit * cap
	end
	return Vector3.new(h.X, v.Y, h.Z)
end

local function num(inst: Instance, name: string, default: number): number
	local v = inst:GetAttribute(name)
	return if typeof(v) == "number" then v else default
end

function Gate0Sim.knockback(closing: number): number
	return math.clamp((closing - Gate0Sim.MIN_CLOSING) * Gate0Sim.KNOCK_SCALE, 0, Gate0Sim.KNOCK_MAX)
end

-- World-space move intent (D-025): Vector2(x, y) maps to world (x, 0, y). Magnitude is clamped to <= 1 here,
-- so a forged or oversized value can never exceed a full-stick input.
function Gate0Sim.readMove(player: Player): Vector2
	local ctx = player:FindFirstChild("Gate0Input")
	local action = ctx and ctx:FindFirstChild("Move")
	if not (action and action:IsA("InputAction")) then
		return Vector2.zero
	end
	local state = action:GetState()
	if typeof(state) ~= "Vector2" then
		return Vector2.zero
	end
	local mag = state.Magnitude
	if mag ~= mag or mag == math.huge then -- NaN or infinite input (RV-01 L1)
		return Vector2.zero
	end
	if state.Magnitude > 1 then
		return state.Unit
	end
	return state
end

function Gate0Sim.stepMovement(v: Vector3, move: Vector2, dt: number): Vector3
	local h = horizontal(v)
	local mag = move.Magnitude
	if mag > 0.01 then
		local target = Vector3.new(move.X, 0, move.Y).Unit * (Gate0Sim.TOP_SPEED * mag)
		local delta = target - h
		local maxStep = Gate0Sim.ACCEL * dt
		if delta.Magnitude > maxStep then
			delta = delta.Unit * maxStep
		end
		h += delta
	else
		h *= math.max(0, 1 - Gate0Sim.DRAG * dt)
	end
	return capHorizontal(Vector3.new(h.X, v.Y, h.Z), Gate0Sim.HARD_CAP)
end

local function liveRoots(): { BasePart }
	local live: { BasePart } = {}
	local folder = workspace:FindFirstChild("Gate0Spheres")
	if not folder then
		return live
	end
	for _, inst in folder:GetChildren() do
		if inst:IsA("BasePart") and inst:GetAttribute("Eliminated") ~= true then
			table.insert(live, inst)
		end
	end
	table.sort(live, function(a, b)
		return num(a, "OwnerUserId", 0) < num(b, "OwnerUserId", 0)
	end)
	return live
end

local function serverStep(live: { BasePart }, dt: number)
	local now = time()
	if resetRequested then
		resetRequested = false
		for _, root in live do
			local spawn = root:GetAttribute("SpawnPos")
			if typeof(spawn) == "Vector3" then
				root.CFrame = CFrame.new(spawn)
				root.AssemblyLinearVelocity = Vector3.zero
				root.AssemblyAngularVelocity = Vector3.zero
			end
		end
	end

	-- ServerKick stimulus: alternating +X / -X so repeated kicks keep the sphere on the board.
	local kickRun = workspace:GetAttribute("Gate0Kick")
	if typeof(kickRun) == "number" and kickRun ~= lastKickRun then
		lastKickRun = kickRun
		local dir = if kickRun % 2 == 1 then 1 else -1
		for _, root in live do
			local kicked = root.AssemblyLinearVelocity + Vector3.new(dir * Gate0Sim.KICK_SPEED, 0, 0)
			root.AssemblyLinearVelocity = capHorizontal(kicked, Gate0Sim.HARD_CAP)
			root:SetAttribute("KickSeq", num(root, "KickSeq", 0) + 1)
		end
	end

	-- Master Plan §8.5 contact check, predictive so it resolves before the engine's own contact.
	for i = 1, #live do
		for j = i + 1, #live do
			local a, b = live[i], live[j]
			local d = horizontal(b.Position - a.Position)
			local dist = d.Magnitude
			if dist > 0.01 then
				local n = d.Unit
				local va, vb = horizontal(a.AssemblyLinearVelocity), horizontal(b.AssemblyLinearVelocity)
				local closing = (va - vb):Dot(n)
				if closing >= Gate0Sim.MIN_CLOSING and dist - closing * dt <= Gate0Sim.DIAMETER + 0.05 then
					local ua, ub = num(a, "OwnerUserId", 0), num(b, "OwnerUserId", 0)
					local key = string.format("%d:%d", math.min(ua, ub), math.max(ua, ub))
					if now - (lastHitAt[key] or -math.huge) >= Gate0Sim.PAIR_COOLDOWN then
						lastHitAt[key] = now
						local attacker, victim, dir = a, b, n
						if vb:Dot(-n) > va:Dot(n) then
							attacker, victim, dir = b, a, -n
						end
						local dv = Gate0Sim.knockback(closing)
						local victimPre, attackerPre = victim.AssemblyLinearVelocity, attacker.AssemblyLinearVelocity
						victim.AssemblyLinearVelocity = capHorizontal(victimPre + dir * dv, Gate0Sim.HARD_CAP)
						attacker.AssemblyLinearVelocity =
							capHorizontal(attackerPre - dir * (dv * Gate0Sim.RECOIL), Gate0Sim.HARD_CAP)
						-- RV-01 B2: record the exact velocities this step applied, so C2 can check the §8.5 math
						-- independently of the engine's later contact solve.
						victim:SetAttribute("HitNormal", dir)
						victim:SetAttribute("HitVictimPre", victimPre)
						victim:SetAttribute("HitVictimPost", victim.AssemblyLinearVelocity)
						victim:SetAttribute("HitAttackerPre", attackerPre)
						victim:SetAttribute("HitAttackerPost", attacker.AssemblyLinearVelocity)
						victim:SetAttribute("HitSeq", num(victim, "HitSeq", 0) + 1)
						victim:SetAttribute("LastHitBy", num(attacker, "OwnerUserId", 0))
						victim:SetAttribute("LastHitAt", now)
						victim:SetAttribute("HitClosing", closing)
						victim:SetAttribute("HitDeltaV", dv)
					end
				end
			end
		end
	end

	for _, root in live do
		if root.Position.Y < Gate0Sim.VOID_Y then
			local by, at = num(root, "LastHitBy", 0), num(root, "LastHitAt", -math.huge)
			root:SetAttribute("Eliminated", true)
			root:SetAttribute("EliminatedAt", now)
			root:SetAttribute("KOCredit", if by ~= 0 and now - at <= Gate0Sim.KO_WINDOW then by else 0)
		end
	end
end

local function step(dt: number)
	totalSteps += 1
	if RunService:IsResimulating() then
		resimSteps += 1
	end
	local live = liveRoots()
	for _, root in live do
		local player = Players:GetPlayerByUserId(num(root, "OwnerUserId", 0))
		local simulate = isServer or RunService:GetPredictionStatus(root) == Enum.PredictionStatus.Predicted
		if player and simulate then
			root.AssemblyLinearVelocity =
				Gate0Sim.stepMovement(root.AssemblyLinearVelocity, Gate0Sim.readMove(player), dt)
		end
	end
	if isServer then
		serverStep(live, dt)
	end
end

function Gate0Sim.init(): RBXScriptConnection
	assert(not started, "Gate0Sim.init called twice")
	started = true
	return RunService:BindToSimulation(step, Enum.StepFrequency.Hz60)
end

function Gate0Sim.requestReset()
	resetRequested = true
end

function Gate0Sim.counters(): (number, number)
	return totalSteps, resimSteps
end

return Gate0Sim
