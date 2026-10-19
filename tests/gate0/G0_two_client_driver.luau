--!strict
-- GATE 0 SPIKE ONLY (branch gate0-spike). Two-client test driver for C2, C3, A4 and the A5 stimulus.
-- Run it in the SERVER context of a Studio "Test > Clients and Servers" session with 2 players, either through
-- the Studio MCP (execute_luau, datamodel_type "Server") or by pasting it into the Server window's Command Bar.
-- It only sets the documented Gate 0 test attributes and samples authoritative state; it never moves roots itself.
-- Clients forward their [G0C] lines to the server, so the Server window's Output holds all evidence.
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local spheres = workspace:WaitForChild("Gate0Spheres")
local out: { string } = {}
local function say(fmt: string, ...: any)
	local line = string.format(fmt, ...)
	print("[G0D] " .. line)
	table.insert(out, line)
end
local function num(inst: Instance, name: string, default: number): number
	local v = inst:GetAttribute(name)
	return if typeof(v) == "number" then v else default
end
local function roots(): { BasePart }
	local list = {}
	for _, r in spheres:GetChildren() do
		if r:IsA("BasePart") and r:GetAttribute("Eliminated") ~= true then
			table.insert(list, r)
		end
	end
	return list
end

local runBase = (num(workspace, "Gate0DriverRuns", 0) + 1) * 100
workspace:SetAttribute("Gate0DriverRuns", runBase / 100)
local nextId = runBase
local function id(): number
	nextId += 1
	return nextId
end
local function cmd(verb: string)
	workspace:SetAttribute("Gate0Cmd", verb .. "#" .. id())
end

local lagOk, lag = pcall(function()
	return (settings() :: any).Network.IncomingReplicationLag
end)
say(
	"driver start runBase=%d players=%d roots=%d incomingReplicationLag=%s",
	runBase,
	#Players:GetPlayers(),
	#roots(),
	if lagOk then tostring(lag) else "unreadable here"
)
if #Players:GetPlayers() < 2 or #roots() < 2 then
	say("ABORT: need 2 players with live roots (got %d players, %d roots)", #Players:GetPlayers(), #roots())
	return table.concat(out, "\n")
end
for _, r in roots() do
	say(
		"root uid=%s slot=%s pos=%s status=%s",
		r.Name,
		tostring(r:GetAttribute("Slot")),
		tostring(r.Position),
		RunService:GetPredictionStatus(r).Name
	)
end

-- C2 + A4: one head-on run with measured velocity changes at the hit frame -------------------------------
local function headOn(label: string): boolean
	cmd("reset")
	task.wait(2)
	workspace:SetAttribute("Gate0AutoDriveMode", "HeadOn")
	local before: { [BasePart]: Vector3 } = {}
	local hitBefore: { [BasePart]: number } = {}
	for _, r in roots() do
		before[r] = r.AssemblyLinearVelocity
		hitBefore[r] = num(r, "HitSeq", 0)
	end
	workspace:SetAttribute("Gate0AutoDrive", id())
	local t0 = os.clock()
	while os.clock() - t0 < 5 do
		RunService.Heartbeat:Wait()
		for _, victim in roots() do
			if num(victim, "HitSeq", 0) ~= hitBefore[victim] then
				local attackerId = tostring(num(victim, "LastHitBy", 0))
				local attacker = spheres:FindFirstChild(attackerId)
				local dv = num(victim, "HitDeltaV", -1)
				local closing = num(victim, "HitClosing", -1)
				local expected = math.clamp((closing - 10) * 1.15, 0, 32)
				if attacker and attacker:IsA("BasePart") then
					local d = victim.Position - attacker.Position
					local n = Vector3.new(d.X, 0, d.Z).Unit
					local victimDv = (victim.AssemblyLinearVelocity - before[victim]):Dot(n)
					local attackerDv = (attacker.AssemblyLinearVelocity - before[attacker]):Dot(n)
					say(
						"%s HIT victim=%s attacker=%s closing=%.2f appliedDv=%.2f expectedDv=%.2f measuredVictimDv=%.2f measuredAttackerDv=%.2f expectedRecoil=%.2f",
						label,
						victim.Name,
						attackerId,
						closing,
						dv,
						expected,
						victimDv,
						attackerDv,
						-0.25 * dv
					)
				else
					say("%s HIT victim=%s attacker=%s (attacker root missing)", label, victim.Name, attackerId)
				end
				return true
			end
		end
		for _, r in roots() do
			before[r] = r.AssemblyLinearVelocity
		end
	end
	say("%s NO HIT within 5 s", label)
	return false
end

headOn("C2")
task.wait(3) -- let both spheres settle for A4
cmd("report") -- server publishes Gate0RefPos_<uid>; each client reports refPosDelta (A4 needs <= 0.5)
task.wait(1.5)

-- C3: tamper under two clients ----------------------------------------------------------------------------
cmd("reset")
task.wait(2)
local maxVy = -math.huge
local t0 = os.clock()
cmd("tamper")
while os.clock() - t0 < 1.5 do
	for _, r in roots() do
		maxVy = math.max(maxVy, r.AssemblyLinearVelocity.Y)
	end
	RunService.Heartbeat:Wait()
end
say("C3 tamper serverMaxVy=%.2f (expect about 0)", maxVy)

-- A5 stimulus: 5 server kicks (clients hold still), then 5 head-on runs ------------------------------------
local function totals(): (number, number)
	local k, h = 0, 0
	for _, r in spheres:GetChildren() do
		k += num(r, "KickSeq", 0)
		h += num(r, "HitSeq", 0)
	end
	return k, h
end
cmd("reset")
task.wait(2)
local baseKick, baseHit = totals()
cmd("report") -- baseline client counters
task.wait(1)
workspace:SetAttribute("Gate0AutoDriveMode", "Hold")
workspace:SetAttribute("Gate0AutoDrive", id())
for _ = 1, 5 do
	workspace:SetAttribute("Gate0Kick", id())
	task.wait(2)
end
local hits = 0
for i = 1, 5 do
	if headOn("A5-headon-" .. i) then
		hits += 1
	end
	task.wait(1)
end
task.wait(1)
local endKick, endHit = totals()
say(
	"A5 server deltas: kickEvents=%d hitEvents=%d headOnRunsWithHit=%d/5 expectedUniqueFxDeltaPerClient=%d (compare with each client's uniqueFx change between the A5 baseline and final reports)",
	endKick - baseKick,
	endHit - baseHit,
	hits,
	(endKick - baseKick) + (endHit - baseHit)
)
cmd("report") -- final client counters (rollbacks, resimSteps, rawFx, uniqueFx, signalFx, regressions)
task.wait(1.5)
say("driver done. Next: close ONE client window to exercise disconnect cleanup (C5), then copy the Server Output.")
return table.concat(out, "\n")
