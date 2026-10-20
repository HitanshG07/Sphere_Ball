# Project Status — Sphere Brawl: Rolling Rampage

Current-state snapshot. History: [WORK_LOG.md](WORK_LOG.md). Earlier versions of this file are in Git history.

**Updated:** 2026-10-20, session S-20261020-09 (lead: Claude Code, Opus 5.5)
**Milestone:** TASK-01 (project scaffolding, types, configuration and remotes): **gate PASSED** (2026-10-20).
**Overall status:** TASK-01 is merged into `alpha`. TASK-02 (GridService and arena collision geometry) has **not** started.
**Waiting on:** owner approval to start TASK-02, and answers to the open questions below.

**GitHub:** `https://github.com/HitanshG07/Sphere_Ball`, PUBLIC (owner decision), default branch `alpha`.
**Branches:**
- `main` = `f726ddd` (untouched spec baseline).
- `alpha` = integration branch. TASK-01 was merged by fast-forward and pushed at `c843af4` (verified with `git ls-remote`); the session's final record commit follows it.
- `task01` = finished TASK-01 branch, `origin/task01` = `c843af4`.
- `gate-0` = `bc4cfa7` (Gate 0 prototype; never merged into `alpha`). The local alias `gate0-spike` tracks `origin/gate-0`; a duplicate local `gate-0` branch is kept until the owner authorizes deleting it.

## Completed (verified)
- **Gate 0** passed with Path A (D-024 to D-027).
- **GitHub hub rules** (`AGENTS.md`, protocol §7) and the canonical Studio place `place/Gate0.rbxl` (T-PUB-001).
- **TASK-01:**
  - Strict shared contracts: `src/shared/Types.luau`, `src/shared/Config/{GameConfig,ChassisConfig,CoreConfig,AssetManifest}.luau`.
  - `src/shared/Modules/CoordinateUtils.luau`.
  - `src/server/Tests/TestRunner.luau` plus three specs: 25 tests pass in Studio.
  - README "Setup and checks" section.
  - Gate table: [TEST_RESULTS.md](TEST_RESULTS.md) (TASK-01 gate verdict).

## Open questions for the owner (answer before the task that needs them)
- **Q-2 (TASK-04/06):** how does the D-019 Burst boost request reach the server? Either `AbilityRequest` with a kind field (`Core` or `Boost`), or a simulation input action like movement. `AbilityRequest` is documented today as "use the equipped core ability", with no payload.
- **Q-3 (TASK-07):** the default loadout for a new player (chassis, skin, core, trail, effect). The spec does not define one.
- **Spec gaps found by review RV-T01-01 (TASK-04/06):**
  - the §8.5 "contact tolerance" distance;
  - the "near zero" thresholds for the dash and boost direction fallbacks (§8.3, D-019);
  - how ability feedback such as NO TARGET and cooldowns reaches the client;
  - who selects the spectate target that D-023's ReplicationFocus follows (the "arena focus part" option avoids a new remote).
- **Collision pairs the §6.2 matrix does not list** (for example LobbyAvatar with LobbyAvatar, any group with Default): decide in TASK-02/03.

## Failed, blocked or open
- **FAIL-009:** parked-avatar streaming. The spike fix works; the product implementation (D-026) comes in TASK-04/07.
- **Antigravity's loading** of `AGENTS.md`/`GEMINI.md` is unverified.

## Known risks
- **Re-saving the place:** Rojo now syncs the TASK-01 modules into the Studio Edit datamodel. Pressing Ctrl+S in Studio would save them into `place/Gate0.rbxl`. Do not commit a re-saved place without the protocol §7 check (decoded file: no scripts, no owner identifiers, `AuthorityMode` 0).
- **Public repository:** existing Gate 0 evidence and commit metadata contain the owner's Roblox username, UserId and email; only new evidence is redacted.
- **Attribute budget** (64 per instance; names and string values up to 50 characters) matters for TASK-04 design.
- **4-client smoke test** deferred to TASK-10.

## Prerequisites
- Studio with `place/Gate0.rbxl` open and the Rojo plugin connected to `rojo serve default.project.json` (repo root).
- Claude Code started in the repo root (`C:\Sphere_ball_rblox\Sphere_Brawl_AI_Agent_Task_Pack`), so `CLAUDE.md` and the `sphere-*` agents load by name. This session started in the parent folder, so the roles ran as general agents.

## Next three actions
1. Owner: review TASK-01 and approve TASK-02 (or request changes).
2. Owner: answer Q-2 and Q-3 (they are needed by TASK-04/06/07, not by TASK-02).
3. Lead, after approval: write the TASK-02 plan (GridService, collision geometry, grid tests) using the frozen TASK-01 contracts.
