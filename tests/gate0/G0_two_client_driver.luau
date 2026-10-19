--!strict
-- GATE 0 SPIKE ONLY (branch gate0-spike). Two-client test driver for C2, C3, A4 and the A5 stimulus.
-- Run it in the SERVER context of a Studio "Test > Clients and Servers" session with 2 players, either through
-- the Studio MCP (execute_luau, datamodel_type "Server") or by pasting it into the Server window's Command Bar.
-- It only sets the documented Gate 0 test attributes and samples authoritative state; it never moves roots itself.
-- Clients forward their [G0C] lines to the server, so the Server window's Output holds all evidence.
-- Revised after independent review RV-01 (B2, M1, M3).
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
local function vec(inst: Instance, name: string): Vector3
	local v = inst:GetAttribute(name)
	return if typeof(v) == "Vector3" then v else Vector3.zero
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

-- Event tally that survives eliminations and root removal (RV-01 M3): accumulates positive sequence deltas.
local tally = { kick = 0, hit = 0 }
local lastSeq: { [Instance]: { kick: number, hit: number } } = {}
local tallyConn = RunService.Heartbeat:Connect(function()
	for _, r in spheres:GetChildren() do
		local prev = lastSeq[r] or { kick = num(r, "KickSeq", 0), hit = num(r, "HitSeq", 0) }
		local k, h = num(r, "KickSeq", 0), num(r, "HitSeq", 0)
		tally.kick += math.max(0, k - prev.kick)
		tally.hit += math.max(0, h - prev.hit)
		lastSeq[r] = { kick = k, hit = h }
	end
end)

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
	tallyConn:Disconnect()
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

-- C2: one head-on run. Validates the §8.5 velocities this step applied (recorded inside the simulation at the hit),
-- and reports separately what the engine's contact solve changed afterwards (RV-01 B2).
local function headOn(label: string): boolean
	cmd("reset")
	task.wait(2)
	workspace:SetAttribute("Gate0AutoDriveMode", "HeadOn")
	local hitBefore: { [BasePart]: number } = {}
	for _, r in roots() do
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
				local n = vec(victim, "HitNormal")
				local closing = num(victim, "HitClosing", -1)
				local expected = math.clamp((closing - 10) * 1.15, 0, 32)
				local victimPre, victimPost = vec(victim, "HitVictimPre"), vec(victim, "HitVictimPost")
				local attackerPre, attackerPost = vec(victim, "HitAttackerPre"), vec(victim, "HitAttackerPost")
				local appliedVictim = (victimPost - victimPre):Dot(n)
				local appliedAttacker = (attackerPost - attackerPre):Dot(n)
				local victimHeartbeat = victim.AssemblyLinearVelocity
				local attackerHeartbeat = if attacker and attacker:IsA("BasePart")
					then attacker.AssemblyLinearVelocity
					else attackerPost
				say(
					"%s HIT victim=%s attacker=%s closing=%.2f expectedDv=%.2f appliedVictimDv=%.2f appliedAttackerDv=%.2f expectedRecoil=%.2f capped=%s",
					label,
					victim.Name,
					attackerId,
					closing,
					expected,
					appliedVictim,
					appliedAttacker,
					-0.25 * expected,
					tostring(victimPost.Magnitude >= 54.99 or attackerPost.Magnitude >= 54.99)
				)
				say(
					"%s ENGINE after-contact (Heartbeat minus applied, along n): victim=%.2f attacker=%.2f relativeClosingAfterApply=%.2f",
					label,
					(victimHeartbeat - victimPost):Dot(n),
					(attackerHeartbeat - attackerPost):Dot(n),
					(attackerPost - victimPost):Dot(n)
				)
				return true
			end
		end
	end
	say("%s NO HIT within 5 s", label)
	return false
end

-- A4: reference positions at +1 s and +3 s (RV-01 M1). Each client logs "A4 refSeq=.. refPosDelta=..".
local function a4Samples(label: string)
	task.wait(1)
	say("%s A4 sample +1s", label)
	cmd("report")
	task.wait(2)
	say("%s A4 sample +3s", label)
	cmd("report")
	task.wait(1)
end

headOn("C2")
a4Samples("after-hit")

cmd("reset")
task.wait(2)
workspace:SetAttribute("Gate0AutoDriveMode", "Hold")
workspace:SetAttribute("Gate0AutoDrive", id())
workspace:SetAttribute("Gate0Kick", id())
a4Samples("after-kick")

-- C3: tamper under two clients -------------------------------------------------------------------------------
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

-- A5 stimulus: 5 server kicks (clients hold still), then 5 head-on runs ----------------------------------------
cmd("reset")
task.wait(2)
local baseKick, baseHit = tally.kick, tally.hit
cmd("report") -- baseline client counters (also resets each client's correction maximum)
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
local kicks, hitEvents = tally.kick - baseKick, tally.hit - baseHit
say(
	"A5 server deltas: kickEvents=%d hitEvents=%d headOnRunsWithHit=%d/5 expectedUniqueFxDeltaPerClient=%d (compare with each client's uniqueFx change between the A5 baseline and final reports)",
	kicks,
	hitEvents,
	hits,
	kicks + hitEvents
)
cmd("report") -- final client counters (rollbacks, resimSteps, rawFx, uniqueFx, signalFx, regressions)
task.wait(1.5)
tallyConn:Disconnect()
say("driver done. Next: close ONE client window to exercise disconnect cleanup (C5), then copy the Server Output.")
return table.concat(out, "\n")
