# TASK-02 - GridService, Coordinate Index, and Ring Collapse

## Preconditions
TASK-01 accepted.

## Goal
Generate and manage the arena as 81 deterministic live cells with smooth gameplay collision surfaces and separate visuals.

## Files
- `src/server/Core/GridService.luau`
- `src/shared/Modules/CoordinateUtils.luau` (only if a tested defect is found)
- `src/server/Tests/Unit/GridService.spec.luau`
- `src/server/Tests/Unit/CoordinateUtils.spec.luau`
- asset/geometry manifest updates

## Requirements
1. Generate coordinates X,Z -4..4 exactly once; key format `x..","..z` (example `-4,2`).
2. For every cell create exactly one invisible anchored collision part `(12,2,12)`, centered using shared coordinate utility. Create separate non-colliding visible tile `(11.8,2,11.8)` plus optional non-colliding overlay.
3. No stacked colliders, no 0.2-stud collision gaps, no per-tile Scripts, no per-tile RunService loops.
4. Ring index uses `max(abs(X), abs(Z))`. D4=32 cells; D3=24 cells.
5. `CollapseRing(4)` makes 49 live cells; `CollapseRing(3)` then makes 25. Remove cells from live index once only and ignore them in any later pattern query.
6. Visual warning can shake/sink only after collision is disabled at the authoritative collapse timestamp. Do not tween a collidable tile through the sphere before disabling it.
7. `ResetArena()` restores exactly 81 cells and clears hazard/owner/timer/pending state.

## Tests
- exact counts and unique IDs
- exact world coordinates and visible tile inset
- no collision part overlaps another in Y; neighbor centers differ by exactly 12 studs
- collapse counts 81 -> 49 -> 25
- regenerate/reset twice with no duplicate cell IDs
- destroyed/pending cells excluded from live queries

## Handoff
Include test assertions and a screenshot/top-down test capture showing the board and ring grooves. Do not add final decorative meshes until grid/collision tests pass.
