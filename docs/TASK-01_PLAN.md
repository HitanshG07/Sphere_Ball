# TASK-01 Plan — Project Scaffolding, Types, Configuration and Remotes

**Status:** APPROVED by the owner on 2026-10-20 (executed in session S-20261020-09).
**Branch:** `task01` from `alpha`, merged into `alpha` by the lead after the gate passes.
**Source:** `tasks/TASK-01-PROJECT-SCAFFOLDING.md`, Master Plan §10, `specs/DESIGN_CONSTANTS.md`, decisions D-001 to D-027.

## What gets built
| File | Content |
|---|---|
| `src/shared/Types.luau` | Strict unions and payload types: RoundPhase, HazardPattern, PulseState, QueueSource, ChassisId, CoreId, SphereSkinId, TrailId, EffectId (D-021), PlayerLoadout, GridCell, PatternMeta, BoardPulsePayload, QueueStatePayload, MatchStatePayload, ResultPayload |
| `src/shared/Config/GameConfig.luau` | Every locked constant in one place: arena, round, queue, pulse cycles (28/21/15), physics and combat, Burst boost (D-019), colors, lobby layout, holding pods (D-023), the extra-focus rule (D-026) |
| `src/shared/Config/ChassisConfig.luau` | The four chassis: cosmetic only, all multipliers 1.0 (D-008) |
| `src/shared/Config/CoreConfig.luau` | Kinetic, Cryo and Magnetic ability values (§8.3) |
| `src/shared/Config/AssetManifest.luau` | Content IDs separate from tuning; unverified assets marked `ASSET_PENDING`, never fake IDs |
| `src/shared/Modules/CoordinateUtils.luau` | Grid ↔ world through `ArenaCFrame` (center applied once); deterministic rounding; out-of-board returns nil |
| `src/server/Tests/TestRunner.luau` plus `*.spec.luau` | Small test runner (no framework) run through the Studio MCP; specs for coordinates, config sums, and remotes |
| `README.md` | Setup and check commands |

`default.project.json` already declares the 10 remotes exactly once; it is only verified, not changed.

## Agents and models (protocol §3–5)
- **Lead (Opus 5.5):** writes the shared contracts (Types, Config). These have one owner and are not parallelized.
- **sphere-gameplay (Sonnet):** writes `CoordinateUtils` and its spec in a separate worktree, once Types and GameConfig are frozen.
- **sphere-docs (Haiku):** mechanical audit that every GameConfig value matches `DESIGN_CONSTANTS.md`; README.
- **sphere-reviewer (Opus):** independent review before the gate.

The project agents load only in a new Claude Code session. If they are still unavailable, the same roles run as general agents with their role files, as during Gate 0.

## Gate (all must pass, with evidence in the registers)
1. `rojo build`, sourcemap, luau-lsp strict (0 errors), StyLua and Selene are clean on real code.
2. Coordinate round trip for every cell in [-4, 4]; out-of-board inputs return nil; the center offset is applied once.
3. Config asserts: cycle sums 28/21/15, Sudden Death 6/2/5/2, caps 42/55, D-019 boost values.
4. The 10 remotes exist exactly once with the right classes; no `KnockbackEvent`.
5. The constants audit finds no mismatch with `DESIGN_CONSTANTS.md`.
6. Independent review has no open high-severity finding.

## Not in TASK-01
Grid, lobby, spheres, gameplay services, UI (Tasks 02 to 10).
