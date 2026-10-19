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
