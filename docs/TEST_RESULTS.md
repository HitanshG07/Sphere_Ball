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

## Gate 0 runs — sessions S-20261020-04 and S-20261020-05 (MCP solo Play unless stated)

Placeholders T-G0-009 to T-G0-015 above stay as written; the rows below are the actual runs. Solo results do **not** satisfy criteria that require two clients or 150 ms latency. Evidence files are in `docs/evidence/gate0/`.

| ID | Requirement | Command / procedure | Expected | Actual | Status | Evidence / notes |
|---|---|---|---|---|---|---|
| T-G0-017 | First solo Play of prototype `8517adb` | `start_stop_play`; console | harness starts | server OK; client LocalScript died at line 34 (`Misprediction` capability) | FAIL | FAIL-007; `20261020-022400_T-G0-017_solo-play-1_console.txt` |
| T-G0-018 | A1 functional: Server Authority active in the live session | server probe `root:SetNetworkOwner(player)` | error under Server Authority | `Can not call Network Ownership API when workspace.AuthorityMode = Enums.AuthorityMode.Server.` (every session) | PASS | live session only; saved file still Automatic (FAIL-006) |
| T-G0-019 | A2 prediction status (retest after FAIL-007 fix, `b7beeef`) | client `SetPredictionMode(own, On)`; `GetPredictionStatus` on client and server | Predicted / Authoritative | client `Predicted after=0.00s`; server `Authoritative`; repeated after respawn | PASS | solo; also observed: own root already Predicted before the client call (automatic mode) |
| T-G0-020 | C1 speed | `drive_c1.luau` Forward run, server samples each Heartbeat | 42 ± 2, <= 55 | max 42.00; >= 40 after 0.583 s (includes attribute replication); 42.00 at 1.0 s | PASS | `20261020-022651_T-G0-018-024_solo-play-2_results.txt` |
| T-G0-021 | C3 oversized input clamp | AutoDrive `Oversize` fires `Vector2(0,10)` | same as unit input | max 42.00 | PASS | same file |
| T-G0-022 | C3 tamper (solo part) | client writes +150 Y locally and fires bogus KO | no server effect | server max Vy 0.00, dY 0.00; server log `bogus claim ... ignored` | PASS | two-client part pending |
| T-G0-023 | C1 fall and single elimination | AutoDrive `EdgeFall` | natural fall, one elimination, no Y snap | eliminated at 1.42 s, once; max upward step 0.025 stud/frame; KOCredit 0 (environment) | PASS | same file |
| T-G0-024 | C5 restore matrix (solo part) | `restore`, `respawn`, `restore` commands | avatar hidden after elimination; exact restore; camera Custom; focus nil; no double-bind | after elimination hidden and anchored, focus `Gate0ArenaFocus`; both restores: mismatches 0, focus nil, savedRecords 0, roundConns 0, camera Custom with Humanoid subject; HRP streamed back | PASS | disconnect part NOT RUN (needs 2 clients) |
| T-G0-025 | C4 camera roll | client max `abs(RightVector.Y)` | 0 | 0.00000 | PASS | solo |
| T-G0-026 | A3 responsiveness at 0 ms | client frames from first fired input to predicted motion | same or next frame | 1 frame | PASS | 0 ms only; 150 ms NOT RUN |
| T-G0-027 | Preliminary kick stimulus (`7640809`), 0 ms | `drive_kick.luau`: 5 server kicks | unique client FX = 5 | rollbacks 6, resimSteps 27, plugin mispredictions 6, client FX 0 | FAIL | FAIL-008; `20261020-023057_T-G0-025_prelim-kick-rollback_solo-0ms.txt` (file name uses an earlier provisional ID) |
| T-G0-028 | Retest of T-G0-027 with polling observer (`5493108`) | same driver | unique FX = kicks, no duplicates, at least 1 rollback | rollbacks 6, resimSteps 31, plugin mispredictions 6, rawFx 5, uniqueFx 5, signalFx 0, regressions 0 | PASS | preliminary only: A5 requires 150 ms and head-on runs |
| T-G0-029 | Correction convergence (preliminary for A4) | client `refPosDelta` after settling | <= 0.5 stud | 0.039 stud | PASS | solo; A4 needs 2 clients |
| T-G0-030 | `Misprediction` from plugin context | MCP `execute_luau` Client datamodel | connects | connected; counted 6 | PASS | tool capability only |
| T-G0-031 | Strict analysis of prototype `8517adb` (first run) | `luau-lsp analyze ... src` | 0 errors | 2 errors (union iteration over `roundConns[player] or {}`) | FAIL | fixed before commit |
| T-G0-032 | Retest of T-G0-031 | same plus StyLua, Selene, `rojo build` | clean | all clean (974 lines) | PASS | |
| T-G0-033 | Static checks for `30d2978` (first run) | luau-lsp | 0 errors | optional-table and sealed/unsealed union errors in the log budget | FAIL | fixed with a named type |
| T-G0-034 | Retest of T-G0-033 | luau-lsp, StyLua, Selene on `src` and `tests`, `rojo build` | clean | all clean | PASS | every prototype commit (`b7beeef`, `7640809`, `5493108`, `30d2978`) passed these checks before committing |
| T-G0-035 | Client log forwarding and driver smoke test (`30d2978`) | solo Play; run `tests/gate0/G0_two_client_driver.luau` in the Server datamodel | forwarded `[G0C<-uid]` lines; driver aborts with 1 player | both as expected; driver read `incomingReplicationLag=0` | PASS | |
| T-G0-036 | C2, C3 (two-client), A3 at 150 ms, A4, A5, C5 disconnect | owner-run two-client sessions with the driver | per plan rev 4 | not executed | NOT RUN | owner session pending |
| T-G0-037 | FAIL-009 experiment: extra replication focus (`48c619d`) | solo Play; client and server character probes; `drive_c5.luau` rerun | client keeps parked HRP; no Animate infinite yield; restore unchanged | client `hrp=true` at the pod; 0 infinite-yield warnings; own root Predicted; elimination and two restore cycles unchanged | PASS | spike only; product adoption needs D-026 approval |
| T-G0-038 | Assumption check: attribute names containing `-` (Studio test UserIds are negative) | Edit `execute_luau`: `workspace:SetAttribute("Gate0RefPos_-1", ...)` | (assumed) error | accepted without error | PASS | assumption disproved; the prepared helper was reverted (never committed); the stray Edit attribute was removed and verified empty |
