# TASK-02 Plan — GridService, Arena Collision Geometry and Ring Collapse

**Status:** APPROVED by the owner (planning Q&A 2026-10-20; the corrected plan, with three corrections, approved 2026-10-21). Executed in session S-20261021-01.
**Branch:** `task02` from `alpha` at `cb8c5ce`. It is pushed to `origin/task02` for review. **It is not merged into `alpha`** until Antigravity's independent acceptance review passes and the owner approves integration.
**Source:** `tasks/TASK-02-GRID-AND-COLLAPSE.md`, Master Plan §6.1–6.5, §10.5, §11.4, §13.2 items 2–3, §15, decisions D-005, D-012, D-016, D-028.
**Out of scope:**
- TASK-03 and later work.
- External 3D assets (the owner's own mesh work is not touched or integrated).
- Hazard overlays (optional on the card; TASK-05 may add them client-side).
- The full §6.2 collision matrix (TASK-03/04, when the other groups first exist).
- A server bootstrap: nothing builds the arena at server start until RoundManager (TASK-07). Tests call `ResetArena()` directly.

## Owner decision D-028 (taken in planning)
1. **Tile physics:** friction 0, elasticity 0 and both property weights 100, the Gate 0 floor values (`PhysicalProperties.new(0.7, 0, 0, 100, 100)`). Traction comes from the movement code (§6.2, §6.3). Density is the Plastic default; it has no effect on anchored tiles. TASK-04 may retune through a TUNING decision.
2. **Greybox collapse visual:** at the collapse timestamp the collider is removed first. Cells are `PendingCollapse` while the visual tile sinks 4 studs and fades over 0.65 s (inside §11.4's 0.5–0.8 s), then they become `Destroyed`. Shake and polish are TASK-09.

## What gets built
| File | Content |
|---|---|
| `src/server/Core/GridService.luau` | New. The only owner of tile Live/PendingCollapse/Destroyed state and of ring collapse (§10.5) |
| `src/server/Tests/Unit/GridService.spec.luau` | New. Card tests, a collider query with negative controls, and Studio physics checks |
| `src/shared/Config/GameConfig.luau` | Additive `Arena` fields for D-028: `TileFriction = 0`, `TilePropertyWeight = 100`, `CollapseSinkTime = 0.65`, `CollapseSinkDepth = 4`. No existing field changes |
| `src/server/Tests/Unit/Config.spec.luau` | Asserts the four D-028 values |
| `assets/asset-manifest.json` | `arena.tile.collision` (PROCEDURAL, `AUTHORITATIVE_COLLIDER`) and `arena.tile.visual` (PROCEDURAL, `VISUAL_ONLY`), source `src/server/Core/GridService.luau`, rights `ORIGINAL_GENERATED`, `robloxAssetId` null |
| `DECISION_LOG.md` | D-028 |

`CoordinateUtils` (unless a test exposes a defect), `Types`, `AssetManifest.luau`, the remotes and `default.project.json` are not changed.

## GridService (server module; functions only; no loops, Heartbeat or connections)
**Reuse:** `CoordinateUtils.gridToWorld` gives every tile center (the arena center is applied once); orientation is `CFrame.new(pos) * GameConfig.Arena.CFrame.Rotation`. `CoordinateUtils.ring` and `isOnBoard` validate input. Sizes, colors, rings, spawn slots and the `ArenaTile` group name come from `GameConfig`. Cells use `Types.GridCell` / `Types.CellState`.

**Geometry:**
- Keys follow `x..","..z` (for example `-4,2`); each part is named after its key. Cells come from integer loops x, z = −4..4, so the order is deterministic and there is no `-0`.
- `Workspace.Arena/Collision/<key>`: anchored, `CanCollide` true, Transparency 1, size (12, 2, 12), collision group `ArenaTile`, `CustomPhysicalProperties` from D-028.
- `Workspace.Arena/Visual/<key>`: anchored, `CanCollide` and `CanTouch` false, size (11.8, 2, 11.8), same center (0.2-stud grooves), SmoothPlastic, `TileDark` when `(x + z) % 2 == 0`, otherwise `TileLight`.
- Everything is built off the DataModel, then parented once.
- Only the `ArenaTile` group is registered, idempotently. Pairs the §6.2 matrix does not list stay undecided.

**API:**
- `ResetArena(): ()`
  1. Increments a generation counter.
  2. Cancels the stored collapse-delay threads (`task.cancel` inside `pcall`) and the stored sink tweens (`:Cancel()`), then clears both lists.
  3. The generation guard stays as the safety net: each delayed callback captures its generation and does nothing if it changed. Each callback removes its own thread handle from the list when it runs.
  4. Destroys the old `Workspace.Arena`, rebuilds 81 Live cells and resets the collapse step to the first ring.
- `CollapseRing(ring: number): boolean`
  - Proceeds only after a build and only if `ring` is the next entry of `GameConfig.Arena.CollapseRings` (4, then 3). Otherwise it warns, returns false and changes nothing (ring 3 first, repeats, 0, 5, 2.5, NaN, ±inf, before any build).
  - For each cell in the ring, in deterministic order: state `PendingCollapse`; **destroy the collider first** (card item 6); then tween the visual down `CollapseSinkDepth` with Transparency → 1 over `CollapseSinkTime`.
  - One generation-guarded `task.delay(CollapseSinkTime, …)` per collapse sets `Destroyed` and destroys the visuals. Its thread and the sink tweens are stored so `ResetArena` can cancel them. Returns true.
- `GetLiveCells(): { Types.GridCell }`: copies of the Live cells, ordered by X, then Z.
- `GetCell(x, z): Types.GridCell?`: a copy, or nil when the cell is off the board, non-integer, NaN, or not built yet.
- `IsLive(x, z): boolean`.

**Invariants:** a live cell always has exactly one collider; pending and destroyed cells have none; a cell leaves the live index exactly once. During the 3 s collapse warning (§6.4) cells stay Live; the warning timing belongs to the caller (RoundManager, TASK-07).

## Tests (Studio TestRunner, `GridService.spec.luau`)
Each test starts with `ResetArena()`. Temporary parts and test balls are checked while present, inside a pcall wrapper that always destroys them and then re-raises any failure.

1. **Counts and IDs.** 81 unique cells; keys match `^-?%d,-?%d$` and equal `x..","..z`; 81 colliders and 81 visual tiles with unique names; no `LuaSourceContainer` under `Arena`.
2. **Collider geometry and physics.** Size (12, 2, 12), anchored, collidable, Transparency 1, group `ArenaTile`, friction 0, elasticity 0, weights 100, center = `gridToWorld(x, z)` within 1e-4, top surface Y 51.
3. **Visual geometry.** Size (11.8, 2, 11.8), `CanCollide` and `CanTouch` false, same center as the collider, checkerboard colors.
4. **Edge to edge with no stacking.**
   - Each +X and +Z neighbour center is exactly 12 studs apart on one axis and 0 on the other, at the same Y (with 81 × 144 = 108², the board is tiled with no gap or overlap).
   - `workspace:GetPartBoundsInBox(GameConfig.Arena.CFrame, Vector3.new(107.9, 1.9, 107.9), params)` with `params.RespectCanCollide = true` returns exactly the 81 colliders, all under `Workspace.Arena.Collision`, none under `Visual`, named with the 81 keys. The frame is the explicit config CFrame (0, 50, 0): `Workspace.Arena` is a Folder and has no CFrame. With no include filter, the query also catches foreign colliders in the board volume.
   - **Negative controls**, each asserted while its temporary part is present, with cleanup guaranteed even when an assertion fails (`withTempPart`: create, `pcall(check)`, destroy, re-raise): baseline 81; a colliding 4×1×4 part inside tile (0, 0) gives 82; a non-colliding one gives 81; afterwards 81 again and no temporary part remains.
5. **Rings.** Ring 4 has 32 cells and ring 3 has 24.
6. **Collapse sequence.** `CollapseRing(3)` first → false, 81 live. `CollapseRing(4)` → true; right away 49 Live, 32 `PendingCollapse`, 49 colliders, ring-4 visuals still present, `IsLive(4, 0)` false, `GetLiveCells` excludes ring 4. A repeat → false. After `CollapseSinkTime` + 0.3 s: 32 `Destroyed`, 49 visuals. `CollapseRing(3)` → after the wait, 25 Live, 25 colliders, 25 visuals. Any further call → false.
7. **Invalid inputs.** `CollapseRing` with 0, 2, 5, 2.5, NaN, −4 and `math.huge` → false with no change. `GetCell` / `IsLive` with (5, 0), (0.5, 0) and (NaN, 0) → nil / false.
8. **Reset twice.** After both collapses, `ResetArena()` gives 81/81/81, all Live, one `Arena` folder, unique names; once more; `GetLiveCells` order identical across resets.
9. **Reset during a collapse.** `CollapseRing(4)`, `ResetArena()` at once, wait `CollapseSinkTime` + 0.3 s: still 81 Live, 81 colliders and 81 visuals at their original positions and full opacity, nothing `Destroyed`. Repeated with two quick resets in a row.
10. **Returned copies are isolated.** Mutating the results of `GetCell` and `GetLiveCells` does not change the service.
11. **Six spawn slots.** All six `SpawnSlots` cells are Live after reset; each sphere footprint (radius 3) lies inside its tile (offset 0 + 3 ≤ 6).
12. **Physics** (Studio only, yields). Unanchored diameter-6 balls dropped from Y 54.15 over a cell center, the seam at world x = 6 and the 4-cell corner (6, ·, 6) rest at Y ≈ 54 ± 0.1 after about 1.5 s. After `CollapseRing(4)`, a ball dropped over cell (4, 0) is below `VoidY` after about 1.5 s.
13. **TASK-01 regression.** The Config (with the D-028 asserts), Remotes and CoordinateUtils specs still pass.

**Static checks** (repo root): `rojo build default.project.json -o build/Gate0.rbxlx`; `rojo sourcemap default.project.json --include-non-scripts -o sourcemap.json`; `luau-lsp analyze --definitions=globalTypes.d.luau --sourcemap=sourcemap.json src`; `stylua --check src`; `selene src`. The manifest is checked against the schema's required keys and enums.

**Studio run:** solo Play through MCP, Server context `require(ServerScriptService.Server.Tests.TestRunner).run()`, output saved under `docs/evidence/task02/`. The arena is built only on the Play server, never in Edit mode, and the place is never saved.

**Handoff capture:** on the Play server `ResetArena()`; on the client the CoreGui is hidden (no player list) and a Scriptable top-down camera looks at the arena center. Captures of the full board and of the board after the ring-4 sink. Each image is checked for owner identifiers before it is committed.

## Gate and review flow
**Gate:** tests 1–12 pass in Studio; the TASK-01 regressions pass; the five static checks are clean; the manifest validates; the captures are saved. §15 criteria: exactly 81 live cells, unique IDs, one collidable part per cell, no collider gaps, correct ring counts, and regeneration works twice.

**Review flow:**
1. Mark the checklist grid items with test IDs.
2. Write `docs/TASK-02_REVIEW_PACKAGE.md` for Antigravity.
3. Run the pre-push audit (protocol §7), push `task02` and verify it with `git ls-remote`.
4. Record the results, then stop.
5. Antigravity runs the independent acceptance review and records its result in `WORK_LOG.md` and `TEST_RESULTS.md`.
6. Merge into `alpha` only after that review passes with no open HIGH finding and the owner approves.

**Agents:** the lead writes everything. The files are tightly coupled and the shared config is lead-owned, so there are no parallel writers and no worktrees. There is no internal reviewer agent; the independent review is Antigravity's.
