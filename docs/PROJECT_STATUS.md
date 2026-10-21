# Project Status — Sphere Brawl: Rolling Rampage

Current-state snapshot. History: [WORK_LOG.md](WORK_LOG.md). Earlier versions of this file are in Git history.

**Updated:** 2026-10-21, session S-20261021-03 (lead: Claude Code, Opus 5.5)
**Milestone:** TASK-02 (GridService, arena collision geometry, ring collapse).
**Overall status:** TASK-02 **accepted** by Antigravity's independent review RV-T02 (ACCEPT WITH DOCUMENTED FOLLOW-UPS: 0 HIGH, 2 LOW, 2 INFORMATIONAL; T-T02-013) and **merged into `alpha`** by fast-forward (`cb8c5ce` → `067379f`, T-T02-018). Post-merge validation passed (static checks and manifest T-T02-015; Studio `4 specs, 38 passed, 0 failed` T-T02-016). TASK-03 has not started.
**Waiting on:** the owner's explicit approval before TASK-03 starts, and the owner decision RV-T02-02 (unlisted collision pairs) before TASK-03/04 applies the §6.2 matrix.

**GitHub:** `https://github.com/HitanshG07/Sphere_Ball`, PUBLIC (owner decision), default branch `alpha`.
**Branches:**
- `main` = `f726ddd` (untouched spec baseline).
- `alpha` = TASK-01 and TASK-02 merged. TASK-02 fast-forward pushed at `067379f` (verified with `git ls-remote`); the session's record commit follows it (head in `git log`).
- `task02` = finished TASK-02 branch, `origin/task02` = `067379f` (accepted code at `3c624c7`; later commits are records).
- `task01` = `c843af4` (finished TASK-01 branch).
- `gate-0` = `bc4cfa7` (Gate 0 prototype; never merged into `alpha`). The local alias `gate0-spike` tracks `origin/gate-0`; a duplicate local `gate-0` branch is kept until the owner authorizes deleting it.

## Completed (verified)
- **Gate 0** passed with Path A (D-024 to D-027).
- **TASK-01** (merged into `alpha`): strict shared contracts, CoordinateUtils, TestRunner and specs.
- **TASK-02** (accepted by RV-T02; merged into `alpha`):
  - `src/server/Core/GridService.luau`: 81 cells, one 12×2×12 `ArenaTile` collider and one 11.8×2×11.8 visual each; `CollapseRing` 4 then 3 (81 → 49 → 25), collider removed first; `ResetArena` with cancellation and a generation guard.
  - D-028 recorded and applied (tile physics 0/0/100; greybox sink 4 studs over 0.65 s).
  - Studio: `4 specs, 38 passed, 0 failed` (T-T02-007); static checks clean (T-T02-006); manifest valid (T-T02-003); four top-down captures (T-T02-010).
  - Checklist grid items marked with test IDs.

## Documented follow-ups from review RV-T02 (tracked; dispositions in WORK_LOG.md, S-20261021-03)
| Finding | Sev | Follow-up | When |
|---|---|---|---|
| RV-T02-01 `ResetArena` destroys any `Workspace` child named `Arena` | LOW | narrow the deletion to the service's own folder, or keep `Workspace.Arena` formally reserved | TASK-07 (lead), when RoundManager first calls `ResetArena` |
| RV-T02-02 unlisted collision pairs (`ArenaTile` with `Default`, and others) | LOW | owner decision | before TASK-03/04 applies the §6.2 matrix |
| RV-T02-03 server-side greybox sink tween | INFO | move to a client visualizer with the collapse polish (D-028 allows it now) | TASK-09 |
| RV-T02-04 rolling seam test | INFO | dynamic rolling over seams; checklist item stays PARTIAL until then | TASK-04 |

## Open questions for the owner (answer before the task that needs them)
- **Q-2 (TASK-04/06):** how does the D-019 Burst boost request reach the server? Either `AbilityRequest` with a kind field (`Core` or `Boost`), or a simulation input action like movement.
- **Q-3 (TASK-07):** the default loadout for a new player (chassis, skin, core, trail, effect).
- **Spec gaps found by review RV-T01-01 (TASK-04/06):** the §8.5 "contact tolerance" distance; the "near zero" thresholds for the dash and boost direction fallbacks (§8.3, D-019); how ability feedback such as NO TARGET and cooldowns reaches the client; who selects the spectate target that D-023's ReplicationFocus follows.
- **Collision pairs the §6.2 matrix does not list** (for example LobbyAvatar with LobbyAvatar, `ArenaTile` with `Default`, any group with Default): decide before TASK-03/04 applies the matrix.

## Failed, blocked or open
- **FAIL-009:** parked-avatar streaming. The spike fix works; the product implementation (D-026) comes in TASK-04/07.
- **Antigravity's loading** of `AGENTS.md`/`GEMINI.md` is unverified.
- FAIL-014 (Rojo plugin crash), FAIL-015 (test pattern) and FAIL-016 (push before reading the audit hits; no exposure) are FIXED-VERIFIED.

## Known risks
- **Rojo plugin can stop syncing silently** (FAIL-014): before every Studio run, compare the Edit datamodel with the repo (module presence and source sizes).
- **Re-saving the place:** Rojo syncs the modules into the Studio Edit datamodel. Pressing Ctrl+S would save them into `place/Gate0.rbxl`. Do not commit a re-saved place without the protocol §7 check.
- **Public repository:** existing Gate 0 evidence and commit metadata contain the owner's Roblox username, UserId and email; only new evidence is redacted.
- **Attribute budget** (64 per instance; names and string values up to 50 characters) matters for TASK-04 design.
- **4-client smoke test** deferred to TASK-10.

## Handoff notes for later tasks (from TASK-02; not implemented)
- Apply the full §6.2 collision matrix when LobbyAvatar, LobbyWorld and ArenaSphere first exist (TASK-03/04). Unlisted pairs, including `ArenaTile` with `Default`, still need an owner decision.
- RoundManager (TASK-07) owns the 3 s warning timing and calls `GridService.CollapseRing` at the collapse timestamp; it also calls `ResetArena()` (nothing builds the arena at server start today).
- PulseService (TASK-05) must cancel hazards before a collapse and must query only `GridService.GetLiveCells()`.
- Client visualizers (TASK-05/09) find tiles by key in `Workspace.Arena.Visual` and must tolerate StreamingEnabled. TASK-09 replaces the greybox sink (and may move the tween client-side).

## Prerequisites
- Studio with `place/Gate0.rbxl` open and the Rojo plugin connected to `rojo serve default.project.json` (repo root), with the sync checked before each run.
- Claude Code started in the repo root (`C:\Sphere_ball_rblox\Sphere_Brawl_AI_Agent_Task_Pack`) so `CLAUDE.md` and the `sphere-*` agents load by name.

## Next three actions
1. Owner: decide RV-T02-02 (unlisted collision pairs, including `ArenaTile` with `Default`).
2. Owner: explicitly approve TASK-03 (or another next task); answer Q-2/Q-3 before TASK-04/06/07.
3. Lead, after approval: plan the approved task from `alpha`, carrying the RV-T02 follow-ups to their tasks.
