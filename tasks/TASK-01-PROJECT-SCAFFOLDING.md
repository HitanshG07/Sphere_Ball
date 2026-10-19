# TASK-01 - Project Scaffolding, Types, Configuration, and Remotes

## Preconditions
Gate 0 is PASS and the orchestrator has approved the repository/toolchain.

## Goal
Create the stable repository layout and shared contracts before any service implementation.

## Files
- `default.project.json`
- `src/shared/Types.luau`
- `src/shared/Config/GameConfig.luau`
- `src/shared/Config/ChassisConfig.luau`
- `src/shared/Config/CoreConfig.luau`
- `src/shared/Config/AssetManifest.luau`
- `src/shared/Modules/CoordinateUtils.luau`
- Remote declarations in project tree
- `README.md`, formatting/lint configs if tools are available
- `docs/DECISION_LOG.md` if no root decision log exists

## Required details
1. Use the exact file tree and names in Master Plan Section 10. Do not create parallel duplicate modules.
2. Apply `--!strict` to every Luau source file.
3. Define types/unions for phase, hazards, queue source, chassis, core, sphere skin, trail, effects, PlayerLoadout, GridCell, PatternMeta, pulse payload, queue payload, match-state payload and results.
4. Freeze all approved constants into GameConfig; no literal copies of timings/limits in service implementations. Constants referenced by the specification must have one canonical source.
5. Define all remotes in Master Plan Section 10.3 exactly once. No `KnockbackEvent`. `InputIntentRemote` exists for Path B only and must not be emitted under Path A.
6. `CoordinateUtils` supports local-grid-to-world and world-to-grid based on an Arena CFrame/center and pitch. Rounding must be deterministic, and out-of-board coordinates return explicit invalid/nil status rather than being clamped silently.
7. Separate tuning config from content IDs. Any unverified asset is `ASSET_PENDING`, not a fake `rbxassetid://` value.

## Tests
- Type analysis has no unapproved errors.
- Coordinate round-trip passes for all coordinates [-4,4].
- Project builds if Rojo is selected.
- All remote names/types match spec and no duplicate declaration exists.

## Stop conditions
If Rojo project format differs from installed version, use that version's verified format and document it. Do not modify gameplay design to compensate for toolchain issues.

## Handoff
List files, tools/versions, exact commands, tests, and any unavailable validators.
