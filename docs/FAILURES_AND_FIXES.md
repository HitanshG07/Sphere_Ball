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

### FAIL-007 update (S-20261020-04)
- **Fix committed:** `b7beeef` wraps the `Misprediction` connection in `pcall` and logs its availability.
- **Retest:** T-G0-019. The client logged `Misprediction connectable=false err=... PluginOrOpenCloud` and continued normally (A2 `Predicted`, input bridge working). A plugin-context connection through MCP `execute_luau` works (T-G0-030), so A5 can still count mispredictions.
- **Status:** FIXED-VERIFIED

## FAIL-008 — Client never observed server-written sequence attributes through change signals
- **Session / discovered:** S-20261020-04, preliminary kick stimulus at 0 ms in solo Play (T-G0-027, prototype `7640809`).
- **Error / observation (confirmed):** the server applied 5 kicks (`KickSeq` 1..5). The client observer, built on `GetAttributeChangedSignal`, counted 0 effects, while the client still read `KickSeq = 5` with `GetAttribute` on its predicted root. 6 rollbacks and 27 resimulated steps occurred during the run.
- **Cause:** confirmed that the change signal does not fire for these updates on a predicted instance in Studio 0.743. Not documented. The `IsResimulating` reference page even says property-changed signals fire for replayed steps (architect research RA-01). Hypothesis: values restored during rollback do not raise change signals.
- **Fix:** `5493108` makes presentation poll the sequence attributes once per rendered frame and present each sequence number at most once (monotonic "highest presented" counter, reset when a root is removed). This matches the documented Creator Hub pattern (effects in a render-step function that compares with previous state). The signal counter is kept as evidence only.
- **Retest:** T-G0-028, same stimulus. Rollbacks 6, resimulated steps 31, plugin-context mispredictions 6, polled raw 5, unique 5, signals 0, regressions 0.
- **Remaining:** the A5 conditions (150 ms, 2 clients, head-on hits, non-predicted remote roots) are not yet tested.
- **Prevention:** recorded for D-025 implementation in TASK-04/05/06: never drive gameplay presentation from change signals on predicted instances.
- **Status:** FIXED-VERIFIED (for the solo 0 ms failure; A5 is tracked separately in T-G0-036)

## FAIL-009 — Parked avatar streamed out on its owner's client
- **Session / discovered:** S-20261020-04, first solo Play (T-G0-017).
- **Observation (confirmed):** with StreamingEnabled and `ReplicationFocus = SphereRoot`, the avatar parked at the D-023 pod (about 2,800 studs away) had no `HumanoidRootPart` on the client (server had it). The default `Animate` script logged `Infinite yield possible on ... WaitForChild("HumanoidRootPart")`. After restore (`ReplicationFocus = nil`, avatar back at the hub) it streamed in again.
- **Cause (confirmed):** documented streaming behavior. The client only streams content near the replication focus.
- **Fix attempted (spike experiment, `48c619d`):** server `player:AddReplicationFocus(hrp)` after parking, `RemoveReplicationFocus(hrp)` on restore (architect RA-01 recommendation; both APIs are server-only, Security None).
- **Retest:** T-G0-037. Client keeps the HRP at the pod, 0 infinite-yield warnings, own root still `Predicted`, elimination and two restore cycles unchanged.
- **Remaining:** adopting this in the product changes D-023 (owner decision) and is proposed as D-026 (awaiting owner approval). Extra foci add server streaming load (documented); measure in the 4- and 6-client tests.
- **Status:** FIXED-UNVERIFIED (works in the spike; product adoption pending owner approval of D-026)

## FAIL-010 — C2 instrumentation could not validate the §8.5 knockback math
- **Session / discovered:** S-20261020-05, independent review RV-01 (finding B2) of `2291ccf`. Found by code review before any 2-client run.
- **Defect (confirmed from code):** the driver compared `appliedDv` with `expectedDv`, both computed from the same formula and closing speed, so they always matched. The only independent numbers were sampled at Heartbeat, after the engine's own contact solve, so the §8.5 application could not be isolated.
- **Fix:** `0c02823`. The simulation records `HitNormal`, `HitVictimPre/Post` and `HitAttackerPre/Post` at the moment it applies the hit. The driver checks the applied victim and attacker velocity changes along the normal against the formula, and reports the engine's after-contact contribution separately.
- **Retest:** needs the owner's 2-client session (C2 in T-G0-036). Solo regression T-G0-039 shows no breakage.
- **Related design question (for the owner, not a defect):** the review computed, and the lead re-derived, that §8.5 alone separates a colliding pair only for closing speeds from about 32.9 to 40 studs/s. With dv = (c − 10) × 1.15 clamped to 32 plus 0.25 recoil, the pair stops closing only if 1.25 × dv ≥ c. Above that (a symmetric head-on at 42 + 42 = 84 still closes at 44 after the hit), the engine contact with elasticity 0 also changes the outcome. Recorded as owner question Q-1 in `PROJECT_STATUS.md`; no locked value was changed.
- **Status:** FIXED-UNVERIFIED (awaiting the 2-client run)

### FAIL-004 update (S-20261020-06)
- **Retest:** T-G0-040. The native `Roblox_Studio` MCP tools are available in the current Claude session (28 tools) and work against the Studio instance `Gate0.rbxl`. The direct stdio workaround is no longer needed.
- **Remaining uncertainty:** the path-case hypothesis was not tested directly; the user-scope registration made it irrelevant.
- **Status:** FIXED-VERIFIED

### FAIL-006 update (S-20261020-06) — now blocking
- **Observation (confirmed):** after the owner reconnected Studio (place lock file 11:48:15), Studio was running `place/Gate0.rbxl` from disk, still saved with `AuthorityMode = Automatic` (re-decoded: value 1). The live session lost Server Authority: `SetNetworkOwner(player)` succeeded, client roots were `Authoritative`, and server velocity writes had no effect (T-G0-041).
- **Impact:** all Path A Studio tests are blocked until `AuthorityMode = Server` is set in the Properties panel **and saved**. A script cannot set it (`lacking capability RobloxScript`, T-G0-005).
- **Status:** OPEN — blocking (owner action)

### FAIL-006 update (S-20261020-06) — fixed
- **Fix:** owner set `AuthorityMode = Server` in the Properties panel and saved (`place/Gate0.rbxl`, 12:06:15).
- **Retest:** T-G0-042 (decoded file and five Properties-panel screenshots) and T-G0-043 (Server Authority active in Play: SetNetworkOwner rejected, roots Predicted).
- **Prevention:** owner instructions now stress that the setting must be saved; T-G0-041 showed that an unsaved setting is lost when Studio reopens the place.
- **Status:** FIXED-VERIFIED

## FAIL-011 — Clients rendered only sky: default camera overrode the sphere camera
- **Session / discovered:** S-20261020-06, first two-client session. The owner reported "only sky"; MCP probes confirmed it.
- **Observation (confirmed):** both clients' workspaces contained the floor and both spheres. The client `CameraType` was `Custom` with the avatar's Humanoid as subject, and the final rendered camera (probe at RenderPriority Last) was at (2000, 209, 1988), the holding pod beyond the 2048-stud baseplate, so only sky and void were visible.
- **Cause (confirmed):** the default PlayerModule camera script resets `CameraType` to `Custom` when the avatar spawns, and its render-step update ran after the harness's `PreRender` camera write every frame.
- **Collateral finding:** the solo C4 measurement (T-G0-025) read the camera inside the harness's own update, so it measured the intended camera, not the rendered one. That result is invalidated by a correction in the test register.
- **Fix:** `554bcdf`. The sphere camera is driven with `BindToRenderStep` at `RenderPriority.Camera + 1` and re-asserts `Scriptable`. C4 is measured from the final camera at `RenderPriority.Last + 1`, with an override counter and a final-distance-error metric. Both bindings are unbound on unbind and restore.
- **Retest:** T-G0-045 (solo): final camera at the intended 20.12-stud offset, roll 0, sphere visible in a screen capture. Two-client confirmation is due in the 150 ms session.
- **Prevention for TASK-04:** the production CameraController must own the camera after the default camera update (or disable the default camera module) and be tested on the rendered result, not its own writes.
- **Status:** FIXED-UNVERIFIED (solo verified; two-client confirmation pending)

### FAIL-011 update (S-20261020-06) — verified
- **Retest:** T-G0-046h, two clients at 150 ms. Final rendered camera Scriptable at the intended 20.12-stud offset with roll 0; screen capture shows both spheres on the arena.
- **Status:** FIXED-VERIFIED

## FAIL-012 — Shell command substitution erased text from a record line
- **Session / discovered:** introduced in S-20261020-07 (commit `001156d`, pushed to `origin/alpha` in S-20261020-08); found by the read-only audit before S-20261020-09.
- **Observation (confirmed):** `docs/PROJECT_STATUS.md` read "**Waiting on:** owner approval of . Q-1 was decided as D-027 ...". The backtick-quoted file name (`docs/TASK-01_PLAN.md`) is missing.
- **Cause (confirmed by the symptom):** the Markdown was passed to the shell inside a double-quoted string. The shell treated the backticks as command substitution, ran the file name as a command, and replaced it with the (empty) output.
- **Impact:** only that line. The other lines added in `001156d` were checked and are intact. No other damage.
- **Fix:** S-20261020-09 rewrote the line in `PROJECT_STATUS.md`.
- **Prevention:** never put Markdown containing backticks or `$` in double-quoted shell strings. Write records with the editor's file tools, or with a single-quoted heredoc file that is then appended. Related: FAIL-003 (heredoc parse failure on record text).
- **Status:** FIXED-VERIFIED (line rewritten; `git diff` inspected)
