# TASK-02 Review Package — for Antigravity's independent acceptance review

**Prepared by:** lead agent, Claude Code (Opus 5.5, `claude-opus-5-5`), session S-20261021-01, 2026-10-21.
**Reviewer:** Antigravity (owner instruction). The lead did not run an internal reviewer agent, so this review is the only independent one.
**What is asked:** accept or reject TASK-02 on branch `task02`. Record the result in `docs/WORK_LOG.md` (new session ID) and `docs/TEST_RESULTS.md` (new `T-T02-NNN` rows), and list findings with severity (HIGH / MEDIUM / LOW). `alpha` is fast-forwarded only after this review accepts with no open HIGH finding **and** the owner confirms.

## 1. Branch and commits
- **Branch:** `task02` (pushed to `origin/task02`). **Base:** `alpha` at `cb8c5ce` (equal to `origin/alpha` at session start).
- **Code under review:** `3c624c7`. Every later commit on `task02` changes records only (docs, evidence); check with `git diff --stat 3c624c7..origin/task02 -- src assets default.project.json`.

| Commit | Content |
|---|---|
| `f94d610` | `docs/TASK-02_PLAN.md`: the approved plan (first commit, as instructed) |
| `8f33de7` | D-028 in `DECISION_LOG.md`; work-log session start |
| `f61075a` | GridService, GridService.spec, D-028 config fields and assert, manifest entries |
| `3c624c7` | Spec fix: cell-key Lua pattern (FAIL-015); first-run evidence; plan text note |
| `6b1c8d8` | Studio evidence, test rows, FAIL-014/015, checklist |
| `96dde1c` | this package, status and work log; first push of `task02` (verified with `git ls-remote`) |
| next | push record (T-T02-011/012); the current head is shown by `git log cb8c5ce..origin/task02` |

## 2. Changed files
| File | Purpose |
|---|---|
| `src/server/Core/GridService.luau` | **New.** Only owner of tile Live/PendingCollapse/Destroyed state and ring collapse (§10.5): `ResetArena`, `CollapseRing`, `GetLiveCells`, `GetCell`, `IsLive` |
| `src/server/Tests/Unit/GridService.spec.luau` | **New.** The 12 card/plan tests (Studio only; tests 06, 09, 12 yield) |
| `src/shared/Config/GameConfig.luau` | Additive D-028 fields in `Arena`: `TileFriction = 0`, `TilePropertyWeight = 100`, `CollapseSinkTime = 0.65`, `CollapseSinkDepth = 4` (4 lines; no existing value changed) |
| `src/server/Tests/Unit/Config.spec.luau` | One new test asserting the four D-028 values and the §11.4 window |
| `assets/asset-manifest.json` | `arena.tile.collision` (PROCEDURAL, `AUTHORITATIVE_COLLIDER`) and `arena.tile.visual` (PROCEDURAL, `VISUAL_ONLY`) |
| `DECISION_LOG.md` | D-028 (owner-approved in TASK-02 planning) |
| `docs/TASK-02_PLAN.md` | Approved plan in repo form (test 1 pattern corrected with a note, FAIL-015) |
| `docs/TASK-02_REVIEW_PACKAGE.md` | This file |
| `docs/WORK_LOG.md`, `docs/TEST_RESULTS.md`, `docs/FAILURES_AND_FIXES.md`, `docs/PROJECT_STATUS.md`, `ALPHA_ACCEPTANCE_CHECKLIST.md` | Records |
| `docs/evidence/task02/*` | 2 run logs, 4 captures |

**Not changed:** `CoordinateUtils.luau` and its spec (no defect found), `Types.luau`, `AssetManifest.luau` (no content IDs), remotes, `default.project.json`, `place/Gate0.rbxl`. No server bootstrap: nothing builds the arena at server start until RoundManager (TASK-07).

## 3. Spec references
TASK-02 card (`tasks/TASK-02-GRID-AND-COLLAPSE.md`); Master Plan §6.1 (coordinates, rings), §6.2 (collision construction, groups), §6.3 (physics values, Y 51), §6.4 (ring collapse), §6.5 (spawn slots), §10.5 (service ownership), §11.4 (collapse visual 0.5–0.8 s after collision removal), §13.2 items 2–3, §15; decisions D-005 (ring order), D-012 (one collider per cell, separate visuals), D-016 (spawn slots), D-028 (tile physics; greybox collapse).

## 4. Design summary (what to check against)
- **Instances:** `Workspace.Arena` (Folder) → `Collision/<key>` (81 Parts) and `Visual/<key>` (81 Parts); key = `x..","..z`, for example `-4,2`. Built off the DataModel, parented once. No scripts, loops, Heartbeat or connections per tile or in the service.
- **Collider:** anchored, `CanCollide` true, Transparency 1, (12, 2, 12), group `ArenaTile`, `CustomPhysicalProperties(Plastic density, 0, 0, 100, 100)`, center = `CoordinateUtils.gridToWorld(x, z)`.
- **Visual:** anchored, `CanCollide` and `CanTouch` false, (11.8, 2, 11.8), same center (0.2-stud grooves), SmoothPlastic, `TileDark` when `(x + z) % 2 == 0`, otherwise `TileLight`.
- **`CollapseRing(ring)`:** accepts only the next entry of `CollapseRings` (4, then 3) on a built arena; otherwise warns, returns false, changes nothing. Per ring cell: state `PendingCollapse` → **collider destroyed** → visual tween (sink 4 studs, Transparency → 1, 0.65 s). One `task.delay(0.65)` per collapse sets `Destroyed` and destroys the visuals; it is generation-guarded and its thread and tweens are stored.
- **`ResetArena()`:** bumps the generation; `task.cancel` (in `pcall`) on stored delay threads; `:Cancel()` on stored tweens; destroys every `Workspace` child named `Arena`; rebuilds 81 Live cells; collapse step back to ring 4. Registers `ArenaTile` once (idempotent). GridService stores no hazard, owner or timer state (those belong to PulseService and others, §10.5), so its reset clears all the tile state it has.
- **Queries:** `GetLiveCells` returns copies of Live cells ordered X then Z; `GetCell` returns a copy or nil (off-board, non-integer, NaN, ±inf, not built); `IsLive` boolean. `-0` keys are normalized.

## 5. How to reproduce
**Static checks** (repo root, tools pinned in `rokit.toml`: Rojo 7.4.4, luau-lsp 1.70.1, StyLua 2.6.0, Selene 0.32.0):
```
git fetch origin && git switch task02 && git log --oneline -1
rojo build default.project.json -o build/Gate0.rbxlx
rojo sourcemap default.project.json --include-non-scripts -o sourcemap.json
luau-lsp analyze --definitions=globalTypes.d.luau --sourcemap=sourcemap.json src
stylua --check src
selene src
```
**Expected:** build and sourcemap succeed; luau-lsp prints no errors; StyLua prints nothing; Selene `0 errors, 0 warnings, 0 parse errors`.

**Manifest:** validate each entry of `assets/asset-manifest.json` against `specs/ASSET_MANIFEST.schema.json` (for example Python `jsonschema.Draft202012Validator`). **Expected:** 5 entries valid.

**Studio** (only on a Play server; the tests build `Workspace.Arena`):
1. Open `place/Gate0.rbxl`, run `rojo serve default.project.json` in the repo root and connect the Rojo plugin.
2. **Check the sync first** (FAIL-014): in Edit, `ServerScriptService.Server.Core.GridService` must exist and `#Source` must equal the file size (`wc -c src/server/Core/GridService.luau`, 7297 bytes at `3c624c7`; `GridService.spec` 17549).
3. Start Play (solo). In the **Server** context run:
   `print(require(game:GetService("ServerScriptService").Server.Tests.TestRunner).run())`
4. Stop Play. **Do not save the place** (Ctrl+S would write the Rojo-synced scripts into `place/Gate0.rbxl`).

**Expected:** `[TestRunner] 4 specs, 38 passed, 0 failed` in about 7 s. The Output also shows exactly 14 warnings `[GridService] CollapseRing(...) rejected: ...` (tests 06 and 07 call it with invalid values on purpose) and no errors.

## 6. Evidence and test IDs (`docs/TEST_RESULTS.md`, TASK-02 section)
| ID | What | Status | File |
|---|---|---|---|
| T-T02-001 / 002 | static checks (fail: 3 type errors + formatting, then clean) | FAIL / PASS | — |
| T-T02-003 | manifest schema validation + negative control | PASS | — |
| T-T02-004 | Rojo sync before Play | BLOCKED (FAIL-014, owner reconnected) | — |
| T-T02-005 | first Studio run: 37 passed, 1 failed (test pattern defect, FAIL-015) | FAIL | `docs/evidence/task02/20261021-003337_T-T02-005_studio-testrunner.txt` |
| T-T02-006 | static checks after the fix | PASS | — |
| T-T02-007 | Studio run: **4 specs, 38 passed, 0 failed** | PASS | `docs/evidence/task02/20261021-003505_T-T02-007_studio-testrunner.txt` |
| T-T02-008 | every test by name (38 PASS) | PASS | same file |
| T-T02-009 | measured values (rest Y 53.9968 at center/seam/corner, mid-sink sample, fall-through Y 5.265) | PASS | same file |
| T-T02-010 | top-down captures: 81, 49, 25 cells, groove close-up (owner identifiers checked) | PASS | `docs/evidence/task02/*_T-T02-010_*.jpg` |
| T-T02-011 / 012 | pre-push audit; push verified with `git ls-remote` | see `TEST_RESULTS.md` | — |

## 7. Checklist items claimed (`ALPHA_ACCEPTANCE_CHECKLIST.md`, Grid and collision surface)
- 81 unique cells: **PASS** (spec 01).
- Exactly one collidable `CollisionTile` per cell, non-colliding visuals: **PASS** (specs 01–04).
- Ring 4 = 32, first collapse leaves 49: **PASS** (specs 05–06). Ring 3 = 24, second collapse leaves 25: **PASS**.
- Edge-to-edge, no gaps, no stacked colliders: **PASS** (spec 04 query with 82/81 negative controls; spec 12; T-T02-009).
- Regeneration: **PASS at GridService level** (specs 08–09); per-round use is TASK-07.
- Six spawns: **PASS at grid level** (spec 11 plus the TASK-01 CoordinateUtils spec); real sphere spawning is TASK-04/07.
- "No seam snag or vertical bounce" (movement section): **PARTIAL**, static drops only; rolling is TASK-04.

## 8. Known limitations and deferred items
- **Collision groups:** only `ArenaTile` is registered. The full §6.2 matrix is applied when LobbyAvatar, LobbyWorld and ArenaSphere first exist (TASK-03/04). The physics test balls are in the `Default` group, which collides with `ArenaTile` by Roblox default; `ArenaTile`–`Default` is a pair the matrix does not list and still needs an owner decision.
- **Server-side sink tween** (`ponytail:` note in `GridService.luau`): up to 32 parts tween for 0.65 s and replicate; move it client-side in TASK-09 if network cost matters. Shake and polish are TASK-09 (D-028).
- **`ResetArena` destroys any `Workspace` child named `Arena`**, not only the folder it built, so a second module instance or a stray folder can never leave two arenas. `Workspace.Arena` is reserved for GridService.
- **Collapse warning timing** (3 s, §6.4) is the caller's: cells stay Live until `CollapseRing` is called at the timestamp (RoundManager, TASK-07). PulseService (TASK-05) must cancel hazards before the collapse and query only `GetLiveCells()`.
- **StreamingEnabled:** the solo client received all 162 parts at the tested distance. Client visualizers (TASK-05/09) should look tiles up by key in `Workspace.Arena.Visual` and tolerate parts that are not streamed in.
- **Not covered by a test:** `CollapseRing`/`GetCell` before the first `ResetArena` in a server (code reading only: module state cannot be reset inside one Play session). No multi-client run (not applicable).
- Still open for later tasks: Q-2, Q-3, the §8.5 contact tolerance, near-zero direction thresholds, the ability-feedback channel, spectate-target selection.

## 9. Focused questions for the reviewer
1. **Collider-first ordering:** in `CollapseRing`, is the collider always destroyed before any visual motion starts, so no collidable tile moves through a sphere (card item 6)?
2. **Generation guard on reset mid-sink:** can a delayed callback from an older generation ever change a rebuilt cell? Is `pcall(task.cancel, thread)` plus the guard sufficient, including two collapses pending and two resets in a row (spec 09)?
3. **One collider per live cell after each step:** does `expectBoard` (colliders = exactly the Live cells) hold after every call in specs 06–09, and is any path able to leave a Live cell without a collider or a pending cell with one?
4. **Live queries exclude pending and destroyed cells:** `GetLiveCells` and `IsLive` right after `CollapseRing` (not only after the sink).
5. **No per-tile scripts or loops:** no scripts under `Arena` (spec 01), no RunService use, no connections in GridService.
6. **D-028 values:** friction 0, elasticity 0, weights 100; sink 4 studs over 0.65 s; are they applied exactly as decided?
7. **Scope:** nothing from TASK-03 or later, no external assets, no changes to frozen TASK-01 contracts beyond the additive D-028 fields.
