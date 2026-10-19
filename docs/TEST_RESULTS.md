# Test and Validation Register

Append-only. Every validation attempt gets its own ID (`T-<milestone>-NNN`). A retest is a new row that references the original. Statuses: `PASS` (ran in the required environment and passed), `FAIL`, `BLOCKED`, `NOT RUN`, `INCONCLUSIVE`, `SKIPPED`. See `docs/AI_DEVELOPMENT_PROTOCOL.md` section 6.

**Environment (unless stated):** Windows 11 Home 10.0.26300; Rokit 1.2.0 with Rojo 7.4.4, luau-lsp 1.70.1, StyLua 2.6.0, Selene 0.32.0; Roblox Studio 0.743.0.7431133; lead agent Claude Code 2.1.303 running Opus 5.5 (`claude-opus-5-5`).

Backfill note: rows T-S0-001 to T-G0-016 were written on 2026-10-20 in session S-20261020-03 from command output observed in sessions S-20261020-01 and S-20261020-02. Step 0 times are bounded by the commits (`f726ddd` at 01:08:43 and `86b9a65` at 01:21:19 IST); exact per-command times were not recorded.

## Step 0 (session S-20261020-01)

| ID | Requirement | Command / procedure | Expected | Actual | Status | Evidence / notes |
|---|---|---|---|---|---|---|
| T-S0-001 | Rojo project builds | `rojo build default.project.json -o build/Gate0.rbxlx` | exit 0 | exit 0, "Built project to Gate0.rbxlx" (3,037 bytes); 9 RemoteEvent + 1 UnreliableRemoteEvent, 4 Folders | PASS | build output inspected with grep |
| T-S0-002 | Sourcemap lists tree | `rojo sourcemap default.project.json -o sourcemap.json` | full tree | file contained `null` | FAIL | FAIL-002 |
| T-S0-003 | Retest of T-S0-002 | `rojo sourcemap default.project.json --include-non-scripts -o sourcemap.json` | 10 remotes, 3 folders, no `.gitkeep` | 10 remotes, `Shared`/`Server`/`Client` folders, 0 `.gitkeep` | PASS | fixes FAIL-002 |
| T-S0-004 | Formatting | `stylua --check src` | exit 0 | exit 0 | PASS | limitation: 0 Luau files existed, nothing meaningful was checked |
| T-S0-005 | Lint | `selene src` | no errors | 0 errors, 0 warnings, 0 parse errors | PASS | limitation: 0 files checked |
| T-S0-006 | Strict analysis | `luau-lsp analyze --definitions=globalTypes.d.luau --sourcemap=sourcemap.json src` | no errors | exit 1, `error: no files provided` | INCONCLUSIVE | no source files; not counted as a pass |
| T-S0-007 | Analyzer and definitions work | strict throwaway file in the session scratchpad (outside the repo) using Path A APIs plus one deliberate type error | deliberate error reported, Path A calls accepted | deliberate `number`/`string` error reported; Path A calls type-checked; also reported `Workspace.AuthorityMode` missing at None security | PASS | limited: not project code |
| T-S0-008 | Doc edits are insert-only | Python check over `git diff -U0`: each removed line must survive inside an added line | no lost text | 13 removed lines; 3 flagged, all confirmed false positives by word-diff (version bump 1.1 to 1.2 and two inserted parentheticals) | PASS | |
| T-S0-009 | Master plan and constants mirror agree | grep counts of new values across master plan, constants and decision log | values present in all | `+12`, cosmetic IDs, pod formula, `PredictionMode.On` present in all three | PASS | D-024 intentionally only in log and mirror |
| T-S0-010 | Rebuild before commit `fc109f8` | `rojo build ...` and `stylua --check src` | exit 0 | both exit 0 | PASS | trivial for StyLua |
| T-S0-011 | Pinned tools resolve | `rojo --version`, `luau-lsp --version`, `stylua --version`, `selene --version` inside the repo | pinned versions | Rojo 7.4.4, 1.70.1, stylua 2.6.0, selene 0.32.0 | PASS | outside the repo the tools fail to resolve by design |

## Gate 0 (sessions S-20261020-02 onward)

| ID | Requirement | Command / procedure | Expected | Actual | Status | Evidence / notes |
|---|---|---|---|---|---|---|
| T-G0-001 | Studio MCP tools available in the Claude session | `ToolSearch` for Roblox tools | Roblox tools listed | none found | FAIL | FAIL-004 |
| T-G0-002 | Studio MCP reachable | direct stdio JSON-RPC client: `initialize`, `tools/list`, `list_roblox_studios` | server responds | `RobloxStudio 1.0.0`; 28 tools; studio `082e378a-d699-429a-88ed-557091cff28d` ("Place1") | PASS | `docs/evidence/gate0/20261020-021342_G0-0_mcp-connection.txt` |
| T-G0-003 | Gate0 place open and Rojo-synced | `get_studio_state`; `search_game_tree` on ReplicatedStorage, ServerScriptService, StarterPlayer; Studio window title; `GET localhost:34872/api/rojo` | Edit mode; 10 remotes; mapped folders | Edit mode; DataModel `SphereBrawlRollingRampage`; 10 remotes; `Shared`, `Server`, `Client`; window title `...\place\Gate0.rbxl`; rojo serve 7.4.4 | PASS | |
| T-G0-004 | G0-1 API presence | `execute_luau` (Edit) pcall probe | APIs present | `BindToSimulation`, `SetPredictionMode`, `GetPredictionStatus`, `IsResimulating`, `Rollback`, `Misprediction`, InputContext/InputAction/InputBinding with Scriptable `Fire` and `GetState` all present; enums: PredictionMode Automatic/On/Off, PredictionStatus Authoritative/Predicted/None, InputBindingType Automatic/Scriptable, StepFrequency Hz60..Hz1 | PASS | `docs/evidence/gate0/20261020-020425_G0-1_api-probe_execute-luau_edit.txt` |
| T-G0-005 | Script access to AuthorityMode is restricted (expected per definitions) | same probe: read and write `workspace.AuthorityMode` | error | read and write both fail: `lacking capability RobloxScript`; NextGenerationReplication, SignalBehavior, UseFixedSimulation are "not a valid member" to scripts; StreamingEnabled readable (`true`) | PASS | expected restriction confirmed; **not** evidence that Path A is unavailable (D-025) |
| T-G0-006 | A1: AuthorityMode = Server in Properties panel | owner screenshot of Workspace Properties | `Server` plus 5 dependent settings visible | `AuthorityMode = Server` visible; dependent settings hidden by the search filter | INCONCLUSIVE | `docs/evidence/gate0/20261020-015946_A1_owner-screenshot_properties-panel_AuthorityMode-Server.png`; needs a screenshot of the dependent settings |
| T-G0-007 | A1: saved place configured | decode Workspace PROP chunks of `place/Gate0.rbxl` | `AuthorityMode` = Server (0) | `AuthorityMode` = 1 (Automatic); NextGenerationReplication Default; PlayerScriptsUseInputActionSystem Enabled; SignalBehavior2 Deferred; StreamingEnabled true; UseFixedSimulation Default | FAIL | FAIL-006; `docs/evidence/gate0/20261020-021341_G0-1_saved-place-workspace-settings.txt` |
| T-G0-008 | MCP can show Workspace properties | `inspect_instance` path `Workspace` | property list | first call used the wrong argument name (`instance_path`), error `Missing required argument: path`; second call returned `"properties":[]` | INCONCLUSIVE | `docs/evidence/gate0/20261020-020434_G0-1_inspect-instance_workspace.txt`; MCP cannot be used for A1 |
| T-G0-009 | C1 solo movement, fall, single elimination | MCP solo play with AutoDrive | per plan rev 4 | not executed | NOT RUN | prototype not finished |
| T-G0-010 | C2 two-client server-only hit | owner-run 2-client session | per plan | not executed | NOT RUN | needs owner |
| T-G0-011 | C3 tamper and input clamp | prototype tamper step | per plan | not executed | NOT RUN | |
| T-G0-012 | C4 camera horizon | prototype camera | per plan | not executed | NOT RUN | |
| T-G0-013 | C5 restore matrix (miniature) | prototype restore commands | per plan | not executed | NOT RUN | |
| T-G0-014 | A2 client prediction status | client `SetPredictionMode` + `GetPredictionStatus` | Predicted / Authoritative | not executed | NOT RUN | |
| T-G0-015 | A3–A6 responsiveness, correction, rollback, server-only outcomes | per plan rev 4 | per plan | not executed | NOT RUN | A5 needs 150 ms Network Simulation set by the owner |
| T-G0-016 | 4-client smoke test | owner-run | per task card | deferred | NOT RUN | deferred to TASK-10 per TASK-00 card |
