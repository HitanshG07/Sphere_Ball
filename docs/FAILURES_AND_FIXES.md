# Failures and Fixes Register

Append-only. Each significant failure keeps its ID forever; later fixes and retests link back to it. Statuses: `OPEN`, `INVESTIGATING`, `FIXED-VERIFIED`, `FIXED-UNVERIFIED`, `WONT-FIX` (with reason). See `docs/AI_DEVELOPMENT_PROTOCOL.md` section 6.

Backfill note: FAIL-001 to FAIL-006 were recorded on 2026-10-20 in session S-20261020-03 from command output observed in sessions S-20261020-01 and S-20261020-02. Their status lines were re-checked against the repository at the time of writing unless marked otherwise.

---

## FAIL-001 — `rokit add` blocked by an interactive trust prompt
- **Session / discovered:** S-20261020-01, Step 0.3, running `rokit add <tool>` for the four pinned tools in a non-interactive shell.
- **Error:** `ERROR The following tool has not been marked as trusted: rojo-rbx/rojo` (same for luau-lsp, StyLua, selene). Piping `y` into the command did not answer the prompt.
- **Cause (confirmed):** Rokit asks for trust interactively; the agent shell has no TTY.
- **Fix attempted:** `rokit trust rojo-rbx/rojo JohnnyMorganz/luau-lsp JohnnyMorganz/StyLua Kampfkarren/selene`, then `rokit add` again. Worked.
- **Retest evidence:** `rokit.toml` lists `rojo-rbx/rojo@7.4.4`, `JohnnyMorganz/luau-lsp@1.70.1`, `JohnnyMorganz/StyLua@2.6.0`, `Kampfkarren/selene@0.32.0`; `--version` of each printed `Rojo 7.4.4`, `1.70.1`, `stylua 2.6.0`, `selene 0.32.0` (test T-S0-011).
- **Prevention:** document `rokit trust` before `rokit add` for agent shells.
- **Status:** FIXED-VERIFIED

## FAIL-002 — `rojo sourcemap` produced `null`
- **Session / discovered:** S-20261020-01, Step 0.4, test T-S0-002.
- **Error:** `sourcemap.json` contained only `null` (4 bytes); a parser then raised `TypeError: 'NoneType' object is not subscriptable`.
- **Cause (confirmed):** by default `rojo sourcemap` keeps only script nodes; with no scripts in `src/` the whole tree was pruned.
- **Fix:** add `--include-non-scripts`. Retest T-S0-003: 10 remotes, 3 mapped folders, 0 `.gitkeep` instances.
- **Prevention:** the flag is part of the documented verification command (`AGENTS.md`, `docs/GATE_0_REPORT.md`).
- **Status:** FIXED-VERIFIED

## FAIL-003 — Bash heredoc failed while appending decision-log entries
- **Session / discovered:** S-20261020-01, Step 0.6.
- **Error:** `/usr/bin/bash: -c: line 64: unexpected EOF while looking for matching ''`; exit code 2.
- **Effect (confirmed):** the command never ran; `git diff --stat` showed no change and `DECISION_LOG.md` ended at D-018.
- **Cause:** not confirmed. Hypothesis: shell quoting inside a long heredoc wrapped in the tool's command string.
- **Fix:** appended the same entries with the file Edit tool instead. Worked (D-019 to D-025 present in commit `86b9a65`).
- **Prevention:** use the Edit/Write tools for long Markdown insertions.
- **Status:** FIXED-VERIFIED

## FAIL-004 — Roblox Studio MCP tools not loaded in the Claude Code session
- **Session / discovered:** S-20261020-02, first Gate 0 step (verify the MCP connection). `ToolSearch` found no Roblox tools; test T-G0-001.
- **Observations (confirmed):**
  - `claude mcp list` from both the parent folder and the repo reports `Roblox_Studio ... ✔ Connected` (local scope; `cmd.exe /c cd /d %LOCALAPPDATA%\Roblox && .\mcp.bat`).
  - The owner's command `claude mcp add --transport stdio Roblox_Studio -- ...` returned `MCP server Roblox_Studio already exists in local config` (exit 1); the existing entry is identical.
  - Claude Code's MCP logs (`%LOCALAPPDATA%\claude-cli-nodejs\Cache\*\mcp-logs-Roblox-Studio\`) contain only short health-check connections from `claude mcp list/get`; none from the chat session itself.
  - `~/.claude.json` holds the server under uppercase keys `C:/Sphere_ball_rblox` and `C:/Sphere_ball_rblox/Sphere_Brawl_AI_Agent_Task_Pack`; another project shows separate `c:/RGame` (no servers) and `C:/RGame` (with the server) keys.
- **Likely cause (hypothesis, not confirmed):** the VS Code session started in `c:\Sphere_ball_rblox` with a lowercase drive letter and looked up a lowercase project key that has no MCP servers.
- **Fixes attempted:**
  1. Owner's `claude mcp add` (local scope): no change, entry already existed.
  2. Registered the same server at **user scope** so it applies regardless of path casing (first attempt failed, see FAIL-005; second attempt verified in `~/.claude.json`).
  3. Workaround for the current session: a direct stdio JSON-RPC client (session scratchpad `mcpcall.py`) talking to the same `mcp.bat` server. Handshake succeeded (T-G0-002).
- **Remaining:** the user-scope fix only takes effect in a new session; it is unverified until a new Claude Code session shows the Roblox tools.
- **Evidence:** `docs/evidence/gate0/20261020-021342_G0-0_mcp-connection.txt`
- **Status:** FIXED-UNVERIFIED (workaround in use)

## FAIL-005 — `claude mcp add --scope user` from Git Bash mangled the `/c` argument
- **Session / discovered:** S-20261020-02.
- **Error:** the CLI echoed `Added stdio MCP server Roblox_Studio with command: cmd.exe C:/ cd /d %LOCALAPPDATA%\Roblox && .\mcp.bat`; the stored args would have been `["C:/", ...]`.
- **Cause (confirmed):** MSYS path conversion in Git Bash rewrites a bare `/c` argument to `C:/`.
- **Fix:** `claude mcp remove Roblox_Studio -s user`, then the same add from PowerShell. `~/.claude.json` now has `"args": ["/c", "cd /d %LOCALAPPDATA%\\Roblox && .\\mcp.bat"]` (verified with Python JSON read).
- **Prevention:** run Windows-style command arguments from PowerShell, or set `MSYS_NO_PATHCONV=1` in Git Bash.
- **Status:** FIXED-VERIFIED

## FAIL-006 — Saved `place/Gate0.rbxl` is not configured for Server Authority
- **Session / discovered:** S-20261020-02, G0-1 / A1 (test T-G0-007).
- **Observation (confirmed):** decoding the Workspace PROP chunks of `place/Gate0.rbxl` (mtime 2026-10-20 01:57:23) gives `AuthorityMode` = 1 (`Automatic`; Studio enum table `Server=0, Automatic=1`), `NextGenerationReplication` = Default, `PlayerScriptsUseInputActionSystem` = Enabled, `SignalBehavior2` = 2 (Deferred), `StreamingEnabled` = true, `UseFixedSimulation` = Default.
- **Conflicting evidence:** the owner's Properties-panel screenshot (taken 01:59:46, after the save) shows `AuthorityMode = Server` in the live session.
- **Likely cause (hypothesis):** `AuthorityMode` was set after the last save.
- **Fix required:** owner saves the place (Ctrl+S) with `AuthorityMode = Server`; then re-decode the saved file. Not a code failure.
- **Evidence:** `docs/evidence/gate0/20261020-021341_G0-1_saved-place-workspace-settings.txt`, `docs/evidence/gate0/20261020-015946_A1_owner-screenshot_properties-panel_AuthorityMode-Server.png`
- **Status:** OPEN

## FAIL-007 — Client harness stopped: `RunService.Misprediction` not connectable from game scripts
- **Session / discovered:** S-20261020-04, first MCP solo Play of prototype `8517adb` (test T-G0-017).
- **Error:** `The current thread cannot connect 'Misprediction' (lacking capability PluginOrOpenCloud)` at `Players.<user>.PlayerScripts.Client.Gate0Client`, line 34. The uncaught error ended the LocalScript, so client prediction setup, the input bridge and the camera never ran.
- **Cause (confirmed):** `RunService.Misprediction` requires plugin or Open Cloud capability; LocalScripts cannot connect it. `RunService.Rollback` (line 31) connected without error.
- **Fix:** guard the `Misprediction` connection with `pcall` and log its availability; keep the `Rollback` event and the in-simulation resimulation counter as the game-script measures for A5; try `Misprediction` from the plugin-capable MCP `execute_luau` Client context during A5.
- **Status:** INVESTIGATING (fix in progress)
