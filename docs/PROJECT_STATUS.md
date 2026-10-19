# Project Status — Sphere Brawl: Rolling Rampage

**Updated:** 2026-10-20
**Milestone:** Gate 0 (TASK-00), environment and physics-authority feasibility
**Current step:** Step 0 complete; waiting on the owner's Studio handoff before the Gate 0 runtime tests
**Branch:** `alpha` (baseline `f726ddd` on `main`)
**Next approved task:** TASK-00 runtime tests only. TASK-01 is not authorized until Gate 0 passes with evidence.

## Completed
| Step | Evidence |
|---|---|
| Step 0.1: git baseline | `f726ddd` "Import spec pack (baseline, untouched)" on `main`; branch `alpha` created |
| Step 0.2: layout | `src/shared`, `src/server`, `src/client` (`.gitkeep` only); `build/` and `place/` created and gitignored; `.gitattributes` keeps LF line endings |
| Step 0.3: tooling | Rokit 1.2.0; pinned Rojo 7.4.4, luau-lsp 1.70.1, StyLua 2.6.0, Selene 0.32.0 (`rokit.toml`); `globalTypes.d.luau` pinned to luau-lsp commit `8e8a4e7` |
| Step 0.4: build | `rojo build default.project.json -o build/Gate0.rbxlx` exit 0; sourcemap (with `--include-non-scripts`) shows 10 remotes and 3 mapped folders |
| Step 0.5: checks | StyLua PASS, Selene PASS (both trivial, 0 files); luau-lsp "no files provided" (not counted); analyzer smoke test outside the repo shows the definitions and strict analysis work |
| Step 0.6: decisions/docs | D-019 to D-023 and D-025 recorded; D-024 reserved; synchronized insert-only edits in the master plan (v1.2), design constants, TASK-00/04/06/07/08, STUDIO_GATE_00 and the acceptance checklist. An automated diff check confirmed no existing text or locked value was removed. |
| Step 0.8: Studio MCP | pre-existing local-scope `Roblox_Studio` registration verified (Connected); no duplicate added |

Full details: `docs/GATE_0_REPORT.md`.

## Tests
- Passed: Rojo build, sourcemap, StyLua check, Selene (trivial, no sources).
- Failed: none.
- Not run: every Studio runtime criterion (G0-1, C1–C5, A1–A6 / B1–B7); the 4-client smoke test is deferred to TASK-10.

## Features
- Implemented: none (no gameplay code is authorized before Gate 0).
- Partial: none.
- Missing: everything in TASK-01 to TASK-10.

## Assets
- Concept board: VERIFIED (visual reference only).
- `sphere.shell.rammer`, `audio.hazard_warning`: ASSET_PENDING (unchanged from the spec pack).

## Blockers
1. **Owner action required:** the Studio handoff below. MCP tools load only when Claude Code starts.
2. Multi-client tests (2 clients for C2/A3–A5) need the owner to start Test ▸ Clients and Servers.

## Files created or modified in Step 0
Verified with `git show --stat 86b9a65` (21 files, 17,641 insertions, 13 deletions; the 13 deletions are lines rewritten with inserted text only):
- New: `.gitattributes`, `.gitignore`, `rokit.toml`, `stylua.toml`, `selene.toml`, `globalTypes.d.luau`, `src/{shared,server,client}/.gitkeep`, `docs/GATE_0_REPORT.md`, `docs/PROJECT_STATUS.md`
- Modified: `DECISION_LOG.md`, `MASTER_IMPLEMENTATION_PLAN.md`, `specs/DESIGN_CONSTANTS.md`, `specs/STUDIO_GATE_00.md`, `ALPHA_ACCEPTANCE_CHECKLIST.md`, `tasks/TASK-00`, `TASK-04`, `TASK-06`, `TASK-07`, `TASK-08`
- Untracked by design (gitignored): `build/Gate0.rbxlx`, `sourcemap.json`, `place/`

## Resume steps (next session)
1. Owner completes the Studio handoff (in the final report of this session).
2. Claude Code opened in `C:\Sphere_ball_rblox\Sphere_Brawl_AI_Agent_Task_Pack`: `git switch -c gate0-spike` from `alpha`, then G0-1 via the `Roblox_Studio` MCP tools.
3. Follow plan rev 4 Gate 0 steps 2–6; close out with a docs-only commit on `alpha`.
