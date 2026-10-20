# Locked Design Constants (Quick Reference)

The master plan is the canonical source; this sheet is its compact numeric mirror. If they disagree, STOP and reconcile the mismatch through an approved decision-log entry before coding. Never guess or resolve a conflict from PDF/DOCX extraction.

## Arena
- center: `(0, 50, 0)`
- pitch: `12` studs
- grid radius: `4`
- coordinates: `-4..4` inclusive
- starting live cells: `81`
- D4 ring: `32` cells; post-collapse `49`
- D3 ring: `24` cells; post-collapse `25`
- collision cell size: `(12,2,12)`, hidden, anchored
- visual tile size: `(11.8,2,11.8)`, non-colliding
- tile top surface Y: `51`
- sphere diameter: `6`
- initial sphere center Y: `54.15`
- void threshold: `Y < 15`
- initial match spawn slots (grid cell -> world sphere center via `ArenaCFrame:PointToWorldSpace(Vector3.new(12*X,4.15,12*Z))`, arena center `(0,50,0)`): `(0,-3)->(0,54.15,-36)`, `(3,-2)->(36,54.15,-24)`, `(3,2)->(36,54.15,24)`, `(0,3)->(0,54.15,36)`, `(-3,2)->(-36,54.15,24)`, `(-3,-2)->(-36,54.15,-24)`; slot order is fixed
- maximum hazard cells: `floor(liveCellCount * 0.35)`

## Round / queue
- min match players `4`; max `6`
- hub capacity target `12` in Alpha; one live match per server
- full queue countdown `8s`
- partial queue wait `25s`, then countdown `10s` if 4-5 players remain
- loadout lock at T-minus `5s`
- physical portal dwell `1.0s`; exit grace `0.5s`
- Results `8s`
- Main lobby spawn position `(0,150,-334)` faces queue target `(0,150,-300)` using `CFrame.lookAt`
- Opening: two cycles of 28s = 56s
- Collapse1: remove D4
- MidGame: two cycles of 21s = 42s
- Collapse2: remove D3
- SuddenDeath: cycles of 15s; hard match timeout 150s

## Pulse cycles
- Source rule: use this file together with `MASTER_IMPLEMENTATION_PLAN.md`; never parse DOCX/PDF table extraction for constants. SuddenDeath = SafeCombat `6.0s`, Warning `2.0s`, Active `5.0s`, Reset `2.0s`, Total `15.0s`.
- Opening = Safe 14 + Warning 3.5 + Active 7 + Reset 3.5 = 28s
- MidGame = Safe 10 + Warning 2.5 + Active 6 + Reset 2.5 = 21s
- SuddenDeath = Safe 6 + Warning 2 + Active 5 + Reset 2 = 15s
- patterns = `IceCorridor`, `MagneticStorm`, `BoostRunway`
- Boost directions = 0, 90, 180, 270 degrees only
- Ice angles = 0, 45, 90, 135; diagonal geometry is phase-shortened to obey cap
- pulse synchronization = `Workspace:GetServerTimeNow()` timestamps plus state snapshot

## Physics and combat tuning
- normal top speed `42` studs/s
- hard horizontal cap `55` studs/s
- base acceleration `85` studs/s^2
- lateral damping `6.5`
- longitudinal drag `1.8`
- brake deceleration `95` studs/s^2
- ice steering multiplier `0.45`
- ice lateral damping `1.625`
- magnetic max acceleration `22` studs/s^2, inward contribution cap `12` studs/s
- boost runway kick `+18` studs/s once per sphere per event
- minimum closing speed `10` studs/s
- knockback formula: `(closingSpeed - 10) * 1.15 * outgoingFactor * victimResistanceFactor`
- knockback delta-V clamp `[0,32]` studs/s
- attacker recoil ratio `0.25`
- pairwise hit cooldown `0.35s`
- KO attribution `5s`
- spawn invulnerability `2.5s`

## Cores
- Kinetic Overdrive Dash: CD `8s`; +22 studs/s; 55 speed cap; outgoing factor 1.25 for 1s
- Cryo Anchor Brake: CD `9s`; remove 85% lateral drift; immunity to Ice/Magnetic for 2.5s; incoming knockback factor 1/1.5 for 2s
- Magnetic Pulse Tether: CD `10s`; nearest target <=24 studs; target +16 studs/s toward caster; no target means no cooldown consumption

## Colors
- tile dark `(32,38,54)`
- tile light `(42,50,70)`
- primary cyan `(0,195,255)`
- ice `(0,235,255)`
- magnet `(165,55,255)`
- boost `(255,125,0)`
- warning amber `(255,170,0)`
- collapse red `(255,40,40)`

## Gate 0 physics architecture
- Path A preferred: Roblox Server Authority (`Workspace.AuthorityMode=Server`, supported settings, `BindToSimulation`, prediction/rollback).
- Path B pre-approved only if Path A is genuinely unavailable: server-owned sphere assemblies using `SetNetworkOwner(nil)`; validated `InputIntentRemote` normalized movement intent (sequence-numbered, maximum 20 updates/second per player, enforced independently by the server); server computes movement, impacts, knockback, eliminations, and results; client extrapolates visual shell/camera presentation only. `InputIntentRemote` is unused under Path A.
- No client-applied authoritative impulses, client-selected positions/velocities, or client-authoritative hit/KO results. If Path B fails latency/integrity validation, block and escalate.
- Path A API usage (D-025): client-only `RunService:SetPredictionMode(ownRoot, Enum.PredictionMode.On)` after the root replicates, verified by `GetPredictionStatus == Predicted`; the server never calls it. Simulation `Move` action = world-space Direction2D (`Vector2(x,y)` maps to world `(x,0,y)`) with one `Scriptable` binding fired by the client each frame outside the simulation; simulation clamps magnitude to `<= 1`; deprecated `InputAction:Fire` is never used; test automation is `RunService:IsStudio()`-gated and never ships. Simulation callbacks write only synchronized state; server-only outcomes use monotonically increasing sequence-ID attributes; presentation/logging deduplicate by sequence ID outside the simulation and poll each frame instead of using change signals on predicted instances (D-026).
- Gate 0 path selection: D-024 (reserved until Gate 0 close-out).

## Owner decisions 2026-10-20 (mirror of Master Plan v1.2; see DECISION_LOG.md)
- Burst boost (D-019): Shift / touch Boost; `+12` studs/s one-time along move input (fallback: horizontal velocity, then facing); cooldown `4s`; horizontal cap `55`; outgoing impact factor `1.0`; validated by AbilityService
- Sphere-skin unlocks (D-020): unlocked `Default`, `Neon`; locked (previewable, rejected) `Gold`, `Void`; session-only server inventory
- Cosmetic IDs (D-021): `TrailId` = `None`, `CoreStreak`, `CyanStreak`; `EffectId` = `StandardSpark`, `CoreBurst`; all unlocked. Tabs: Build = chassis, Skins = sphere skin, Core, Trails, Effects; Ball tab disabled `COMING SOON`
- Hard-timeout placement score (D-022): alive outranks eliminated; eliminated ranked by elimination time, latest first; same-step eliminations share a placement; then valid KOs, then survival time, then shared tie
- Holding pods (D-023): `GameConfig.Lobby`; 6 pods; anchored floor `(10,1,10)`; top surface Y `200`; centre `(2000 + 20*(i-1), 200, 2000)` for i = 1..6; collision group `LobbyAvatar`; ReplicationFocus = own SphereRoot in play, spectated root or arena focus part while spectating, `nil` after cleanup; restore matrix in Master Plan §5.4; extra replication focus on the parked avatar's HumanoidRootPart during play, removed at restore/cleanup/disconnect (D-026)
