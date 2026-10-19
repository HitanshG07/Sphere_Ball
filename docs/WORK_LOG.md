# Work Log — Sphere Brawl: Rolling Rampage

Append-only chronological history for every AI and human working on the project. One section per session (`S-YYYYMMDD-NN`). Never edit or delete an earlier entry; append a correction that references it. Times are IST (+05:30). Process rules: [AI_DEVELOPMENT_PROTOCOL.md](AI_DEVELOPMENT_PROTOCOL.md).

**Backfill notice:** the sessions S-20261019-01 to S-20261020-02 were written retrospectively on 2026-10-20 in S-20261020-03 by the same lead agent. Facts marked *(verified)* were re-checked against the repository, Git history, file timestamps or saved evidence while writing. Other facts come from that agent's own conversation transcript and are marked *(transcript)*. Approximate times are marked `~`.

---

## S-20261019-01 — Planning and read-only environment audit
- **When:** 2026-10-19 ~23:30 to 2026-10-20 ~01:05 *(transcript)*
- **Lead:** Claude Code (VS Code extension), model Opus 5.5 (`claude-opus-5-5`), in plan mode. No subagents.
- **Milestone:** pre-Gate 0 (planning only; no repository changes).
- **Actions** *(transcript)*:
  - Read the spec pack: master plan, global prompt, decision log, design constants, assignment matrix, checklist, kickoff prompt, all task cards, STUDIO_GATE_00, VISUAL_QA_SHOTLIST, asset manifest and schema.
  - Read-only tool audit. Results: git 2.51.0; Rojo 7.4.4 (WinGet) plus Studio plugin; Python 3.11.0; Node 22.19.0; Studio 0.743.0.7431133; no luau-lsp, StyLua, Selene, Lune or Blender. The Studio binary contains the Path A strings. The Studio MCP was installed but not connected to Claude Code.
  - Checked Creator Hub pages for Server Authority, RunService, InputBinding, InputAction and the PredictionMode/PredictionStatus enums.
- **Owner decisions captured:**
  - connect the Studio MCP;
  - the repo root is the task-pack folder;
  - Rokit-pinned tools;
  - D-019 Burst boost;
  - D-020 skin unlocks.
- **Plan revisions:** rev 1 to rev 3 were rejected by the owner with corrections:
  - rev 1: working directory consistency, Properties-panel verification of AuthorityMode, the restore matrix, review of D-021 to D-023;
  - rev 2: Rojo start order, one gate0 layout and branch workflow, client-only `SetPredictionMode`, the deprecated `InputAction:Fire`, rollback safety, the duplicate D-021;
  - rev 3: separate Path A/B criteria, a reproducible rollback test, a complete AutoDrive spec, "planned" file-list wording.

  Rev 4 was approved with an added instruction to create `build/` and `place/`.
- **Files changed:** none in the repository (no Git repository existed yet).
- **Next action recorded:** execute Step 0.

## S-20261020-01 — Step 0 bootstrap
- **When:** 2026-10-20 ~01:05 to 01:25. Commits at 01:08:43, 01:21:19 and 01:21:32 *(verified, `git log`)*.
- **Lead:** Claude Code, Opus 5.5. No subagents.
- **Milestone:** Step 0 of the Gate 0 plan rev 4.
- **Actions and outcomes:**
  1. `git init -b main`; baseline commit `f726ddd` "Import spec pack (baseline, untouched)"; `git switch -c alpha` *(verified)*.
  2. Created `.gitignore` (`build/`, `place/`, `sourcemap.json`, lock files) and `.gitattributes` (`* text=auto eol=lf`, binary types). `.gitattributes` was a deviation from the rev 4 file list, added because the global `core.autocrlf` would convert line endings and break `stylua --check` *(verified)*.
  3. Created `src/{shared,server,client}/.gitkeep`, `build/` and `place/` *(verified)*.
  4. Installed Rokit 1.2.0 (GitHub release; `rokit self-install` added `~/.rokit/bin` to the user PATH). `rokit add` failed on the trust prompt (FAIL-001); fixed with `rokit trust`. Pinned Rojo 7.4.4, luau-lsp 1.70.1, StyLua 2.6.0 and Selene 0.32.0 *(verified, `rokit.toml`)*.
  5. Downloaded `globalTypes.d.luau` (luau-lsp `globalTypes.None.d.luau` at commit `8e8a4e745c814ee8d3dd1cea8980901cb27a6970`). Finding: `Workspace.AuthorityMode` appears only at RobloxScriptSecurity *(verified)*.
  6. Wrote `stylua.toml` and `selene.toml` (`std = "roblox"`).
  7. Checks: T-S0-001 build PASS; T-S0-002 sourcemap FAIL (FAIL-002), retested as T-S0-003 PASS with `--include-non-scripts`; T-S0-004 StyLua and T-S0-005 Selene trivially PASS; T-S0-006 luau-lsp INCONCLUSIVE (no files); T-S0-007 analyzer smoke test PASS (outside the repo).
  8. Decision-log append via a Bash heredoc failed without changes (FAIL-003); redone with the Edit tool. Added D-019 to D-023 and D-025; reserved D-024.
  9. Insert-only edits:
     - `MASTER_IMPLEMENTATION_PLAN.md` (v1.2);
     - `specs/DESIGN_CONSTANTS.md`;
     - `specs/STUDIO_GATE_00.md`;
     - `ALPHA_ACCEPTANCE_CHECKLIST.md`;
     - `tasks/TASK-00`, `TASK-04`, `TASK-06`, `TASK-07`, `TASK-08`.

     Checks T-S0-008 (no lost text) and T-S0-009 (mirror values) PASS.
  10. Wrote `docs/GATE_0_REPORT.md` (environment section) and `docs/PROJECT_STATUS.md`.
  11. MCP: found a pre-existing local-scope `Roblox_Studio` registration (`claude mcp list`: Connected). It was not created by this agent, so no duplicate was added.
  12. Commits on `alpha`: `86b9a65` (21 files, 17,641 insertions, 13 deletions, verified with `git show --stat`) and `fc109f8` (status file list). T-S0-010 and T-S0-011 PASS.
- **Handoff:** owner to start `rojo serve`, save a Baseplate as `place/Gate0.rbxl`, set `AuthorityMode = Server` in the Properties panel, connect Rojo, and restart Claude Code in the repo root.

## S-20261020-02 — Gate 0 start (TASK-00)
- **When:** 2026-10-20 ~01:58 to 02:11 *(file timestamps verified: rojo started 01:53:52, Studio 01:56:20, place saved 01:57:23, screenshot 01:59:46, stash 02:11:46)*.
- **Lead:** Claude Code, Opus 5.5. Session working directory `c:\Sphere_ball_rblox` (parent folder, lowercase drive letter).
- **Owner actions observed:** Studio running with `place/Gate0.rbxl`; `rojo serve` 7.4.4 running; screenshot saved to `docs/evidence/gate0/` (original name `Screenshot 2026-10-20 015946.png`, later renamed to `20261020-015946_A1_owner-screenshot_properties-panel_AuthorityMode-Server.png`).
- **Actions and outcomes:**
  1. No Roblox tools in the session (T-G0-001 FAIL, FAIL-004).
     - The owner's `claude mcp add --transport stdio Roblox_Studio -- "cmd.exe" "/c" "cd /d %LOCALAPPDATA%\Roblox && .\mcp.bat"` returned `already exists in local config` (exit 1).
     - Claude MCP logs show only health-check connections.
     - Hypothesis: project-key case mismatch.
  2. User-scope registration: first attempt from Git Bash mangled `/c` (FAIL-005); removed and re-added from PowerShell; args verified.
  3. Wrote a direct stdio JSON-RPC client (session scratchpad `mcpcall.py`, not in the repo). Handshake, 28 tools and studio `082e378a-d699-429a-88ed-557091cff28d` (T-G0-002 PASS); Rojo sync confirmed (T-G0-003 PASS).
  4. `git switch -c gate0-spike` from `alpha` at `fc109f8` *(verified)*.
  5. G0-1:
     - T-G0-004 PASS (APIs present);
     - T-G0-005 PASS (expected script restriction);
     - T-G0-008 INCONCLUSIVE (`inspect_instance` gave no properties; the first call used a wrong argument name);
     - T-G0-006 INCONCLUSIVE (screenshot shows only AuthorityMode);
     - T-G0-007 FAIL (saved place has `AuthorityMode = Automatic`, FAIL-006).

     The saved place was decoded with a scratchpad parser (`rbxlprops.py`) after three parser iterations: the first stopped on a ZSTD chunk, the second skipped every chunk, and the third decoded ZSTD raw blocks.
  6. Drafted `src/shared/Gate0Sim.luau` (shared BindToSimulation module). It was not analyzed or committed and is stashed as `stash@{0}` ("gate0-spike WIP: Gate0Sim.luau (unanalyzed)", commit `70c3ee5`).
- **Interrupted by:** the owner's instruction to set up the permanent cross-AI development system (S-20261020-03).

## S-20261020-03 — Cross-AI development system and audit trail
- **When:** 2026-10-20 from 02:11 *(verified: stash time 02:11:46)*.
- **Lead:** Claude Code 2.1.303, Opus 5.5. Branch `alpha` (switched from `gate0-spike` after stashing the draft).
- **Objective:** owner instructions to make the multi-agent workflow, model selection and audit trail permanent and tool-agnostic. The owner added mid-session: no Copilot or Cursor adapters.
- **Acceptance:**
  - shared rules in `AGENTS.md` and the protocol;
  - verified adapters for Claude Code and Gemini/Antigravity;
  - specialist agents;
  - registers backfilled from verified facts only;
  - links valid, diff inspected, committed on `alpha`, no change to `main`, no spike merge.
- **Inspection:** no `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.claude/`, Copilot or Cursor files in the repo, its parent or user scope. `~/.claude/settings.json` (model `opus`, ponytail plugin) left unchanged.
- **Subagents:** three read-only availability probes (`general-purpose`), no tools used:

  | Alias | Reported model |
  |---|---|
  | `haiku` | Haiku 4.5 (`claude-haiku-4-5-20251001`) |
  | `sonnet` | Sonnet 5.5 (`claude-sonnet-5-5`) |
  | `opus` | Opus 5.5 (`claude-opus-5-5`) |

- **Documentation checks:**
  - Claude Code memory docs: `@AGENTS.md` import, `/context`, `/memory`; subdirectory `CLAUDE.md` loads on demand.
  - Claude Code subagent docs: frontmatter fields, model aliases, `claude plugin validate`.
  - Gemini CLI memport: `@./file.md` imports.
  - GitHub Copilot docs: `.github/copilot-instructions.md` and `AGENTS.md`.
  - Cursor docs: `.cursor/rules/*.mdc` and `AGENTS.md`.
  - Antigravity: `GEMINI.md`, `AGENTS.md` (IDE v1.20.x) and `.agents/rules/`, from third-party guides only, so marked unverified.
- **Evidence saved** (untracked until the Gate 0 close-out), in `docs/evidence/gate0/`:
  - `20261020-020425_G0-1_api-probe_execute-luau_edit.txt`
  - `20261020-020434_G0-1_inspect-instance_workspace.txt`
  - `20261020-021341_G0-1_saved-place-workspace-settings.txt`
  - `20261020-021342_G0-0_mcp-connection.txt`
  - the renamed owner screenshot.
- **Files created:**
  - `AGENTS.md`: shared rules for all tools;
  - `CLAUDE.md`: `@AGENTS.md` import plus Claude-specific multi-agent and Studio notes;
  - `GEMINI.md`: `@./AGENTS.md` import plus Gemini/Antigravity notes;
  - `docs/AI_DEVELOPMENT_PROTOCOL.md`: the detailed process;
  - `.claude/agents/sphere-architect.md` (opus), `sphere-gameplay.md` (sonnet), `sphere-client.md` (sonnet), `sphere-reviewer.md` (opus, read-only) and `sphere-docs.md` (haiku). None may spawn further agents (no `Agent` tool);
  - `docs/WORK_LOG.md`, `docs/TEST_RESULTS.md`, `docs/FAILURES_AND_FIXES.md`.
- **Files modified:**
  - `docs/PROJECT_STATUS.md`: rewritten as a snapshot in the owner's required format; the previous content is preserved in commit `fc109f8` and summarized above;
  - `docs/GATE_0_REPORT.md`: section 7 appended; sections 1–6 unchanged.
- **Not created (owner instruction):** `.github/copilot-instructions.md` and `.cursor/rules/`.
- **Validation:**
  - `claude plugin validate .claude/agents`: "✔ Validation passed" (exit 0).
  - Frontmatter check: all five agents have name, description, tools and model, and the name matches the filename. A first run reported every file as BAD because of a path-separator bug in the checker itself; after the fix all were OK.
  - Relative-link check: the first run found 11 missing references: `docs/WORK_LOG.md` (not yet written at that point) and the future TASK-01 contract file `src/shared/Types.luau` (intentional). The re-run after writing this log is recorded in the next entry.
- **Commit:** pending at the time of writing; recorded in the next entry.

### S-20261020-03 (continued) — commit and branch sync
- Link re-check after writing this log: 105 references in 14 files; 6 unresolved, all intentional: `src/shared/Types.luau` (future TASK-01 contract file, 3 mentions) and `src/shared/Gate0Sim.luau` (exists only on `gate0-spike`/stash, 3 mentions).
- Commit `2d55f5e` on `alpha` at 02:19:42: 14 files, 656 insertions, 46 deletions (the deletions are the `PROJECT_STATUS.md` snapshot rewrite; `GATE_0_REPORT.md` received additions only). `main` still at `f726ddd`. Evidence files remain untracked until the Gate 0 close-out commit.
- Next: fast-forward `gate0-spike` to `alpha` (alpha into the spike only; the spike is never merged into `alpha`) so the rule files exist on both branches, restore `stash@{0}`, and resume Gate 0 under session S-20261020-04.

## S-20261020-04 — Gate 0 continued (TASK-00)
- **When:** 2026-10-20 from ~02:21.
- **Lead:** Claude Code 2.1.303, Opus 5.5. Branch `gate0-spike` fast-forwarded to `cff1063`; `stash@{0}` popped, so `src/shared/Gate0Sim.luau` (draft) is back as an untracked file. Studio MCP still reached through the direct stdio client (FAIL-004 workaround).
- **Objective:** finish the Path A prototype (server and client scripts), run strict analysis, format, lint and build, commit on `gate0-spike`, then run the solo-play criteria C1 and A2 (plus the parts of C3/C4 possible solo) through the MCP.
- **Acceptance for this step:** analyzer, StyLua, Selene and build clean on the prototype; solo results recorded in `docs/TEST_RESULTS.md` with evidence. Multi-client criteria (C2, C5 disconnect, A3–A6) remain NOT RUN until the owner starts a 2-client session.
- **Records workflow on the spike:** record-only commits are allowed on `gate0-spike`; at Gate 0 close-out the record files are copied to `alpha` in the docs-only commit (`git checkout gate0-spike -- <record files>`), never by merging the spike.
- **Supporting agents:** none planned; the prototype files are interdependent and the milestone limits helpers to read-only work.

### S-20261020-04 — results (appended)
- **Prototype written and checked:**
  - Files: `src/server/Gate0Server.server.luau` (server bootstrap) and `src/client/Gate0Client.client.luau` (client harness), alongside the restored `src/shared/Gate0Sim.luau`.
  - First strict analysis found 2 errors (T-G0-031, union iteration); fixed. All checks clean (T-G0-032).
  - Committed `8517adb` on `gate0-spike` (974 lines).
- **Studio access:** scripts synced by Rojo and confirmed in the Edit datamodel. All Studio work went through the direct stdio MCP client (FAIL-004 workaround).
- **Solo Play 1** (`8517adb`):
  - The client harness died on `RunService.Misprediction` (FAIL-007, T-G0-017).
  - Server Authority was confirmed active in the live session by the `SetNetworkOwner` error (T-G0-018).
  - The parked avatar was streamed out on the client (FAIL-009).
  - The own root was `Predicted` even before any client call (automatic prediction).
- **Fixes:**
  - `b7beeef`: `pcall` around `Misprediction`.
  - `7640809`: harness bugs. The A3 log re-armed every frame (spam), and an AutoDrive run could carry over to a new root after unbind. Both fixed; harness only, no gameplay effect.
- **Solo Play 2** (`b7beeef`/`7640809`):

  | Test | Result |
  |---|---|
  | A2 (T-G0-019) | `Predicted` / `Authoritative` |
  | C1 speed (T-G0-020) | 42.00 |
  | Oversize clamp (T-G0-021) | 42.00 |
  | C3 tamper, solo (T-G0-022) | server Vy 0 |
  | Edge fall, single elimination (T-G0-023) | at 1.42 s, KOCredit 0 |
  | C5 restore matrix, twice (T-G0-024) | mismatches 0 |
  | C4 camera roll (T-G0-025) | 0 |
  | A3 at 0 ms (T-G0-026) | 1 frame |

- **Preliminary kick stimulus** (T-G0-027): 0 client FX against 5 kicks (FAIL-008). Investigation showed the client value was current but `AttributeChangedSignal` did not fire.
- **Owner checkpoint:** the owner asked for a short status at ~02:33. It was given in chat; the records had not yet been updated for these results at that point. They are now.

## S-20261020-05 — Gate 0 continued after owner checkpoint
- **When:** 2026-10-20 from ~02:35.
- **Lead:** Claude Code 2.1.303, Opus 5.5, branch `gate0-spike`.
- **Owner instruction:** continue, follow the multi-agent protocol, maintain the reports and the owner's to-do list, and finish everything possible before the owner's 2-client session (the owner runs it after waking).
- **Objective:**
  - fix and verify FAIL-008;
  - research the open API questions;
  - get an independent review;
  - prepare the 2-client session (driver plus instructions);
  - update all records.

  TASK-01 is not authorized.
- **Delegation** (protocol section 5; read-only per Gate 0 restriction):
  - The project agents in `.claude/agents/` could not be invoked by name: `Agent type 'sphere-architect' not found`. Claude Code loads project agents at session start, and these were created mid-session. To verify in a new session: the agent list should include them.
  - Fallback used: `general-purpose` agents given the specialist definition file as their role, with the same model.
    - RA-01 `sphere-architect` role, Opus 5.5: research on Server Authority observation patterns, streaming, telemetry, Scriptable input and conflicts with D-025. Report received and summarized below; it was research, with no files changed.
    - RV-01 `sphere-reviewer` role, Opus 5.5: independent review of the prototype. Result recorded when received.
- **RA-01 key findings** (sources in the agent report; the lead re-verified the API names in `globalTypes.d.luau`):
  - Creator Hub documents per-frame comparison in `RenderStepped` for effects, supporting the FAIL-008 fix.
  - `Player:AddReplicationFocus` and `RemoveReplicationFocus` are server-only, Security None; recommended for FAIL-009.
  - `Player:GetCameraState()` exists under Server Authority, so D-025's "server has no camera" rationale is outdated (lead verified the definition at line 14668).
  - `InputBinding:Fire` does not re-fire identical consecutive values and is ignored when its action or context is disabled.
  - Remote players' spheres may not be auto-predicted. Check in the 2-client session.
  - Studio's server-authority visualizer (Ctrl+Shift+F6) can provide A5 screenshot evidence.
- **Work and results:**
  1. Probed the still-running Play session: client `KickSeq` = 5, server `KickSeq` = 5. The value replicated; the signal did not fire.
  2. FAIL-008 fix `5493108`: polling observer. Retest T-G0-028 PASS (unique FX 5 = kicks 5, signals 0, rollbacks 6).
  3. Read-only probe: `settings().Network.IncomingReplicationLag` is readable from the plugin context, currently 0. Not changed; the owner sets it.
  4. `30d2978`:
     - test-only `Gate0ClientLog` remote, so clients forward `[G0C]` lines to the Server Output (length- and rate-capped, data only);
     - `tests/gate0/G0_two_client_driver.luau`: one script for C2, C3, A4 and the A5 stimulus.

     Smoke test T-G0-035 PASS. The type errors found on the way (T-G0-033) were fixed (T-G0-034).
  5. `48c619d`:
     - FAIL-009 experiment, extra replication focus on the parked avatar: T-G0-037, HRP stays streamed, 0 infinite-yield warnings, restore unchanged;
     - A4 reference measured when the server reference attribute arrives (fixes a race under latency);
     - per-root prediction status in client reports.
  6. Decision log: **D-026 PROPOSED** (D-023 focus amendment, D-025 rationale correction, presentation-polling clarification). Not approved; not applied to locked text.
- **Evidence added** in `docs/evidence/gate0/`:
  - `20261020-022400_T-G0-017_solo-play-1_console.txt`
  - `20261020-022651_T-G0-018-024_solo-play-2_results.txt` plus raw console and driver copies
  - `20261020-023057_T-G0-025_prelim-kick-rollback_solo-0ms.txt` (provisional ID in the name; the register entry is T-G0-027)
  - `*_T-G0-026_kick-retest-polling_solo-0ms.txt` (register entry T-G0-028)
  - `*_T-G0-037_extra-replication-focus-experiment.txt`
- **Disproved assumption (S-20261020-05):** I expected attribute names with a `-` (from negative Studio test UserIds, for example `Gate0RefPos_-1`) to be rejected and wrote a sign-safe helper. A probe showed the name is accepted (T-G0-038), so the helper was reverted before any commit.
  - The probe left `Gate0RefPos_-1` on the **Edit** workspace. It was removed immediately, and the Edit workspace attribute list was verified empty, so nothing stray will be saved into the owner's place.
- **Records updated:** `TEST_RESULTS.md` (T-G0-017 to T-G0-038), `FAILURES_AND_FIXES.md` (FAIL-007 update, FAIL-008, FAIL-009), `DECISION_LOG.md` (D-026 PROPOSED), `GATE_0_REPORT.md` section 8, `PROJECT_STATUS.md` (snapshot plus step-by-step owner actions).
