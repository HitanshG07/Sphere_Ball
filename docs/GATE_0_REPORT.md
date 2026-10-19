# Gate 0 Report — Environment, Tooling and Physics Authority

**Task:** TASK-00 / GATE 0
**Status:** IN PROGRESS. The environment audit and Step 0 bootstrap are complete; Studio runtime tests are **NOT RUN** (awaiting the owner's Studio handoff).
**Selected path:** none yet. D-024 is reserved until the runtime criteria are evaluated.
**Plan:** Step 0 + Gate 0 execution plan rev 4 (owner-approved 2026-10-20).

## 1. Environment audit (collected 2026-10-19/20, read-only)

| Item | Result | Evidence |
|---|---|---|
| OS | Windows 11 Home Single Language 10.0.26300 | session environment |
| Git | 2.51.0.windows.1; identity `HitanshG07` | `git --version`, `git config --global user.name` |
| Repository | `C:\Sphere_ball_rblox\Sphere_Brawl_AI_Agent_Task_Pack`; baseline `f726ddd` on `main` (untouched spec pack); work on `alpha` | `git log --oneline` |
| Python / Node | 3.11.0 / v22.19.0 | `python --version`, `node --version` |
| Roblox Studio | **0.743.0.7431133** at `%LOCALAPPDATA%\Roblox\Versions\version-4f087c32742644ab\RobloxStudioBeta.exe` (2026-10-15). Only one Studio build is installed. | file version via PowerShell |
| Path A strings in the Studio binary | present: `AuthorityMode`, `BindToSimulation` (+`BindToSimulationParallel`), `PlayerScriptsUseInputActionSystem`, `NextGenerationReplication`, `UseFixedSimulation`, `SetNetworkOwnerFailIfServerAuthority`, `GetServerTimeNow`, `InputAction*` | `grep -a -o` over the binary |
| Roblox Studio MCP | installed (`%LOCALAPPDATA%\Roblox\mcp.bat` → `StudioMCP.exe`); tools include `execute_luau` (Edit/Client/Server), `start_stop_play` (solo play only), `get_console_output`, `screen_capture`, `inspect_instance`, keyboard/mouse input | `StudioMCP\tools-cache.json` |
| MCP registration for Claude Code | **pre-existing** server `Roblox_Studio` (scope: Local, this repo; `cmd.exe /c cd /d %LOCALAPPDATA%\Roblox && .\mcp.bat`); health check Connected. Not created by this session; no duplicate added. Its tools are not loaded in the current session, so a restart is required. | `claude mcp list`, `claude mcp get Roblox_Studio` |
| Rojo Studio plugin | `RojoManagedPlugin.rbxm` installed | `%LOCALAPPDATA%\Roblox\Plugins` |
| Blender | not installed (optional; procedural geometry fallback per Master Plan §11.1) | `Get-Command blender` |
| Studio test automation | MCP `start_stop_play` provides solo play only. Multi-client (2/4/6) sessions need the owner to start Test ▸ Clients and Servers. | tool schema |

## 2. Toolchain installed in Step 0 (Rokit-pinned, project-scoped)

| Tool | Version | Pin |
|---|---|---|
| Rokit | 1.2.0 | `~/.rokit/bin`, added to the user PATH by `rokit self-install` |
| Rojo | 7.4.4 | `rojo-rbx/rojo@7.4.4` (matches the installed Studio plugin and the WinGet copy) |
| luau-lsp | 1.70.1 | `JohnnyMorganz/luau-lsp@1.70.1` |
| StyLua | 2.6.0 | `JohnnyMorganz/StyLua@2.6.0` |
| Selene | 0.32.0 | `Kampfkarren/selene@0.32.0` |
| Roblox type definitions | `globalTypes.d.luau` = luau-lsp `scripts/globalTypes.None.d.luau` (normal script security) at commit `8e8a4e745c814ee8d3dd1cea8980901cb27a6970` (2026-10-15) | committed in the repo root |

Rokit tools resolve only inside a directory containing `rokit.toml` (verified: running them from outside the repo fails with "Failed to find tool ... in any project manifest file").

## 3. Step 0 checks (actual results)

| Check | Command | Result |
|---|---|---|
| Mapped directories | `default.project.json`: `ReplicatedStorage.Shared → src/shared`, `ServerScriptService.Server → src/server`, `StarterPlayer.StarterPlayerScripts.Client → src/client` | all three exist (each holds only `.gitkeep`) |
| Build | `rojo build default.project.json -o build/Gate0.rbxlx` | **PASS**: exit 0, "Built project to Gate0.rbxlx" (3,037 bytes); tree has 9 `RemoteEvent` + 1 `UnreliableRemoteEvent` (10 remotes) and 4 Folders (`Remotes`, `Shared`, `Server`, `Client`) |
| Sourcemap | `rojo sourcemap default.project.json --include-non-scripts -o sourcemap.json` | **PASS**: 10 remotes, the 3 mapped folders, 0 `.gitkeep` instances. Without `--include-non-scripts` the output is `null` because no scripts exist yet, so the flag is now part of the verification command. |
| Format | `stylua --check src` | **PASS** (exit 0); trivial: 0 Luau files in `src` |
| Lint | `selene src` | **PASS** (0 errors, 0 warnings, 0 parse errors); trivial: 0 files |
| Strict analysis | `luau-lsp analyze --definitions=globalTypes.d.luau --sourcemap=sourcemap.json src` | **NOT APPLICABLE YET**: exit 1, "no files provided" (no sources). Not counted as a pass. |
| Analyzer smoke test (outside the repo) | strict throwaway file using `BindToSimulation`, Scriptable `InputBinding:Fire`, client `SetPredictionMode`/`GetPredictionStatus`, plus one deliberate type error | analyzer and definitions work: the deliberate error was reported, and all Path A calls type-checked. Selene's `roblox` std also loaded. |

## 4. Static API findings relevant to Gate 0 (from the pinned definitions; to be confirmed in Studio)

- `Workspace.AuthorityMode` appears **only** in the RobloxScriptSecurity definitions, not at None or PluginSecurity level. `PlayerScriptsUseInputActionSystem` likewise. `NextGenerationReplication`, `SignalBehavior` and `UseFixedSimulation` are not exposed to scripts at all. Consequences:
  - A script, command-bar or MCP `execute_luau` read or assignment of these properties is expected to fail and is **not** evidence that Path A is unavailable (D-025; TASK-00 execution details).
  - The Studio Properties panel, plus functional runtime evidence (client `Predicted` status, the `SetNetworkOwner` failure under Server Authority, synchronized `time()`), decides A1.
  - Product code must not depend on reading `workspace.AuthorityMode` at runtime. This matters for TASK-01 planning.
- `Enum.AuthorityMode` (`Automatic`, `Server`), `Enum.PredictionMode` (`Automatic`, `On`, `Off`) and `Enum.PredictionStatus` are exposed to scripts.
- `RunService:BindToSimulation(func, frequency: StepFrequency?, priority: number?)`, `SetPredictionMode(context, mode)`, `GetPredictionStatus`, `IsResimulating` are present.
- `InputAction:Fire` is annotated deprecated. `InputAction:GetState()` is present and **not** deprecated in these definitions; there is no separate state property. G0-1 confirms which read works inside the simulation.
- `InputBinding:Fire(state)`, `InputBinding.Type` (`Automatic`/`Scriptable`) and `InputBinding.ClampMagnitudeToOne` are present.

## 5. Runtime criteria (Studio): NOT RUN

All items below require the Studio session (owner handoff). None has been executed. None is claimed as passed.

| ID | Criterion | Status |
|---|---|---|
| G0-1 | Properties panel + API probe | NOT RUN |
| C1 | Solo movement 42±2, ≤55; natural fall; single elimination | NOT RUN |
| C2 | Two-client server-only head-on hit, §8.5 velocities ±1 stud/s | NOT RUN |
| C3 | Tamper ignored; oversized input clamped | NOT RUN |
| C4 | Stable, no-roll camera | NOT RUN |
| C5 | D-023 restore matrix (miniature) | NOT RUN |
| A1–A6 | Path A criteria (if Path A is selected) | NOT RUN |
| B1–B7 | Path B criteria (only if Path A is genuinely unavailable) | NOT RUN |
| 4-client | Four-client smoke test | DEFERRED to TASK-10 per the task card |

## 6. Known limits

- MCP play is solo only; C2, A3–A5 and the disconnect part of C5 need the owner to start a multi-client session and, for A5, to set Network Simulation lag.
- MCP may not reach Test-mode client windows; if not, the owner pastes each window's Output and the report records that as the evidence source.
- Properties-panel screenshots come from the owner (MCP `screen_capture` captures the viewport).
- The tooling addition `.gitattributes` (`* text=auto eol=lf`) was not in the rev 4 file list. It keeps working-copy line endings LF despite the global `core.autocrlf` conversion, so `stylua --check` stays reproducible across branch switches.

## 7. Progress update (appended 2026-10-20, sessions S-20261020-02 and S-20261020-03)

Sections 1–6 above are unchanged; this section records what happened after the owner's Studio handoff. Test IDs refer to [TEST_RESULTS.md](TEST_RESULTS.md); failure IDs to [FAILURES_AND_FIXES.md](FAILURES_AND_FIXES.md).

**Handoff state verified:**
- Studio window title `...\place\Gate0.rbxl` (process started 01:56:20);
- `rojo serve` 7.4.4 reachable at `localhost:34872`;
- the Gate0 DataModel contains the 10 remotes and the `Shared`/`Server`/`Client` folders (T-G0-003).

**MCP connection:**
- The `Roblox_Studio` tools did not load into the Claude Code session (FAIL-004, T-G0-001). It was also registered at user scope (FAIL-005 fixed along the way); that fix is unverified until a new session.
- This session talks to the same server through a direct stdio JSON-RPC client. The handshake passed (T-G0-002).

**G0-1 results:**

| Check | Result | Status |
|---|---|---|
| Path A APIs and enums | all present (T-G0-004) | PASS |
| Script access to `AuthorityMode` | `lacking capability RobloxScript` for read and write, as the definitions predicted; not unavailability evidence (T-G0-005) | PASS (expected) |
| Properties panel (owner screenshot) | `AuthorityMode = Server` in the live session; dependent settings not visible (T-G0-006) | INCONCLUSIVE |
| Saved `place/Gate0.rbxl` | `AuthorityMode = Automatic`; NextGenerationReplication Default; PlayerScriptsUseInputActionSystem Enabled; SignalBehavior Deferred; StreamingEnabled true; UseFixedSimulation Default (T-G0-007) | FAIL (FAIL-006, owner save needed) |
| `inspect_instance(Workspace)` | returns no properties (T-G0-008) | INCONCLUSIVE (tool limitation) |

**Path decision:** none yet. Path A APIs exist and AuthorityMode can be set to Server in the Properties panel, so the D-018/D-025 rule keeps Path A as the path under test; Path B is not triggered.

**Prototype:** branch `gate0-spike` created from `alpha` at `fc109f8`. A draft `src/shared/Gate0Sim.luau` was written but not analyzed or committed; it was stashed (`stash@{0}`) when governance setup work began.

**Runtime criteria C1–C5 and A2–A6:** still NOT RUN.

## 8. Criteria status after solo testing (appended 2026-10-20, sessions S-20261020-04 and S-20261020-05)

**Path decision:** Path A remains the path under test. Its APIs exist, and Server Authority is demonstrably active in the live session (T-G0-018). Path B conditions are not met.

**Gate 0 status:** **NOT PASSED.** Two-client and 150 ms criteria are outstanding.

| Criterion | Status | Evidence (TEST_RESULTS IDs) |
|---|---|---|
| A1 configuration | PARTIAL: live session runs Server Authority (PASS, T-G0-018); Properties panel shows `AuthorityMode = Server` but the dependent settings are not yet captured (T-G0-006 INCONCLUSIVE); saved `Gate0.rbxl` still `Automatic` (T-G0-007 FAIL, FAIL-006) | owner save and screenshot needed |
| A2 prediction status | PASS in solo (T-G0-019); re-check every root in the 2-client session | |
| A3 responsiveness | PASS at 0 ms (1 frame, T-G0-026); 150 ms NOT RUN | |
| A4 authoritative correction | NOT RUN (2 clients); solo preliminary 0.039 stud (T-G0-029) | |
| A5 rollback reproducibility | NOT RUN at 150 ms; mechanism verified in solo at 0 ms after FAIL-008 fix (T-G0-028) | |
| A6 server-only outcomes | partial: solo tamper and input clamp PASS (T-G0-021, T-G0-022); independent code review RV-01 pending or recorded in the work log | |
| C1 movement, fall, elimination | PASS in solo (T-G0-020, T-G0-023) | |
| C2 two-client server-only hit | NOT RUN | |
| C3 security | PASS in solo (T-G0-021, T-G0-022); two-client part NOT RUN | |
| C4 camera | PASS in solo (T-G0-025) | |
| C5 restore matrix | PASS for elimination, restore and re-entry in solo (T-G0-024, T-G0-037); disconnect NOT RUN | |

**Engine findings during solo testing** (details in `FAILURES_AND_FIXES.md`):
- `RunService.Misprediction` is plugin/Open Cloud only (FAIL-007).
- Change signals do not fire for server-written attributes on predicted roots (FAIL-008); presentation must poll.
- The parked avatar streams out on its owner's client unless an extra replication focus is added (FAIL-009); proposed as D-026.

**Prepared for the owner session:**
- `tests/gate0/G0_two_client_driver.luau` (C2, C3, A4 and the A5 stimulus in one run).
- Client logs forwarded into the Server Output.
- Step-by-step instructions in `PROJECT_STATUS.md`, "Owner actions".

## 9. Independent review (appended 2026-10-20, session S-20261020-05)
- **RV-01:** read-only review by a `sphere-reviewer` role agent (Opus 5.5). No server-authority or rollback-safety defects. Confirmed C2-validity defect B2 (FAIL-010); B1 disputed by Studio evidence (T-G0-038). Medium and low items fixed in `0c02823`; solo regression T-G0-039 PASS.
- **RV-02 re-review:** requested; result recorded in the work log.
- **Owner question Q-1:** §8.5 alone separates colliding spheres only for closing speeds of about 32.9–40 studs/s; above that, engine contact also shapes the result. The 2-client driver now logs the applied §8.5 change and the engine contribution separately (see `PROJECT_STATUS.md`).
- **Gate 0 status:** unchanged, **NOT PASSED** (two-client and 150 ms criteria outstanding).
