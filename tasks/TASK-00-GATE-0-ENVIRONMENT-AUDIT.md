# TASK-00 / GATE 0 - Environment, Tooling, and Physics Architecture Feasibility

**Must be first. Do not write the game systems before this gate passes.**

## Goal
Select and verify one of the two pre-approved physics architecture paths for the exact target Roblox Studio environment, and document available agent/build tools.

## Read first
- `AI_AGENT_GLOBAL_SYSTEM_PROMPT.md`
- Master Plan Sections 9, 10, 13, 14

## Tasks
1. Inspect repository, branch/worktree state, and existing work. Do not delete or overwrite anything.
2. Record OS, Roblox Studio version/channel, Rojo version, Luau analyzer version, Stylua/Selene availability, Blender availability, Studio test automation access, and any MCP/computer-use tools available to the agent.
3. Read the current official Roblox Creator Hub server-authority setup and inspect the target Studio build. Attempt Path A first: verify `Workspace.AuthorityMode = Server`, the dependent Workspace settings, and `RunService:BindToSimulation()` are available and enabled in Studio. These settings are environment configuration; do not assume Rojo can set them.
4. If Path A is genuinely unavailable (the property/API or required beta surface is absent), follow approved Decision D-018 Path B. Do not choose Path B merely because Path A code/test has a defect; first debug and retest Path A.
5. In a disposable branch/test place, create a minimal two-client scene with one sphere root per player and a flat floor. For Path A, test predicted local input plus server correction using the shared simulation. For Path B, test server-owned roots (`SetNetworkOwner(nil)`) plus validated input intents, no more than 20 input updates/second. Keep tests isolated from product code.
6. In both paths verify: two players can move; the server decides collisions, knockback and eliminations; a client cannot claim arbitrary hit/KO; no client-applied gameplay impulse is authoritative. For Path B, test representative network latency and visual-only extrapolation.
7. Use the correct simulation callbacks and clocks for the selected path. In Path A, use synchronized simulation time (`time()`) inside `BindToSimulation`; use `Workspace:GetServerTimeNow()` for network-aligned presentation timestamps, not rollback-sensitive simulation state.
8. Produce `docs/GATE_0_REPORT.md` with chosen path, versions, settings, screenshots/log excerpts, passed/failed checks and exact reproduction steps.

## Allowed changes
Only temporary Gate 0 test files or `docs/GATE_0_REPORT.md`. Do not start GridService, QueueService or product UI. At close-out, a docs-only commit may also add `docs/evidence/gate0/`, decision D-024, `docs/PROJECT_STATUS.md` and the Gate 0 boxes of `ALPHA_ACCEPTANCE_CHECKLIST.md`.

## Execution details (approved 2026-10-20; D-024 reserved, D-025)
- **Configuration check:** verify `Workspace.AuthorityMode = Server` and the dependent settings in Studio's **Properties panel** (screenshot as evidence). A failed script read or assignment of `AuthorityMode` is not evidence of unavailability: the Roblox API definitions expose that property only at RobloxScriptSecurity.
- **Isolation and branches:** prototype code lives under the existing `src/` paths of `default.project.json` on branch `gate0-spike`, which is never merged. Run `rojo serve default.project.json` from the repository root. At close-out, switch to `alpha` and make one docs-only commit (report, evidence, D-024, status, checklist); confirm its staged paths before committing.
- **Path A specifics (D-025):** the server creates roots; each client calls `SetPredictionMode(ownRoot, Enum.PredictionMode.On)` and verifies `GetPredictionStatus == Predicted`. The `Move` action is a world-space Direction2D fed through a `Scriptable` InputBinding by the client; the simulation clamps magnitude to <= 1. Simulation callbacks contain no print, FX, sound, remote or instance creation; outcomes use sequence-ID attributes and observers deduplicate.
- **AutoDrive test source:** Studio-gated (`RunService:IsStudio()`), spike-only, armed by integer attribute `workspace.Gate0AutoDrive` (set from the MCP Server datamodel or the Server test window's Command Bar; cleared by setting it to nil), with modes `HeadOn`, `Forward` and `EdgeFall`. Direction toward a target: `d = (target - own)` with Y zeroed; fire `Vector2.zero` if `d.Magnitude < 0.01`, else `Vector2.new(d.Unit.X, d.Unit.Z)`. It resets to `Vector2.zero` after the hit, after 4 s, or on clear, and each run ID is used once.
- **Acceptance criteria:** common C1-C5 (solo movement and fall, two-client server-only hit, security and input clamp, camera, restore matrix) plus only the selected path's criteria. Path A: A1 configuration, A2 prediction status, A3 responsiveness, A4 authoritative correction (<= 0.5 stud within 1 s), A5 rollback reproducibility, A6 server-only outcomes. Path B: B1 unavailability evidence, B2 ownership nil, B3 input validation, B4 rate limit, B5 replication latency, B6 knockback and elimination, B7 presentation-only extrapolation. Path B is never held to Path A's prediction or rollback criteria.
- **A5 rollback reproducibility:** 150 ms incoming replication lag; 5 server kicks (+20 studs/s, unpredictable to the client) and 5 HeadOn runs; record rollback, misprediction, resimulation, correction-distance, server-hit, server-kick, raw-FX and unique-FX counters. PASS requires at least one observed rollback and unique FX = hits + kicks. If none is observed, repeat once at 250 ms; if still none, mark INCONCLUSIVE, investigate, and report Gate 0 as BLOCKED rather than PASS.

## Pass criteria
- Exactly one pre-approved path is selected and recorded: Path A (Roblox Server Authority) or Path B (server-owned physics fallback).
- A two-client movement/collision smoke test passes; a four-client smoke test is run before alpha acceptance.
- Server owns gameplay outcomes; clients send input/action intent only.
- Path B, if selected, passes latency and rate-limit checks and uses no client-applied gameplay impulse.
- Toolchain and unresolved environment requirements are documented.

## Stop condition
If Path A is genuinely unavailable, test pre-approved Path B per D-018. If Path A is available but its test fails, debug Path A before considering the fallback. If the chosen path fails validation, or both paths fail, mark `BLOCKED`, record evidence, and stop. Do not implement a third hybrid or client-applied impulse workaround.

## Handoff
Report PASS/FAIL/BLOCKED, exact Studio version/settings, selected path, test evidence, limitations and `docs/GATE_0_REPORT.md` path. If Path B is selected, document that it is server-owned simulation without the native rollback/prediction guarantees of Path A.
