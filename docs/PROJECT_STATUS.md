# Project Status — Sphere Brawl: Rolling Rampage

Current-state snapshot. History: [WORK_LOG.md](WORK_LOG.md). Earlier versions of this file are in Git history.

**Updated:** 2026-10-20, session S-20261020-06 (lead: Claude Code 2.1.303, Opus 5.5)
**Milestone:** Gate 0 (TASK-00), environment and physics-authority feasibility
**Overall status:** IN PROGRESS. **Gate 0 has not passed.** TASK-01 has not started and is not authorized.
**Waiting on:** two-client **session 2 at 150 ms** (Owner actions C). Session 1 at 0 ms is done (C2, C3, A4 and C5 disconnect PASS; A5 preliminary PASS; FAIL-011 camera found, fixed and verified in solo).
**Branches:**
- `main` = `f726ddd` (untouched spec baseline).
- `alpha` = `cff1063` (rules and records as of S-20261020-03).
- `gate0-spike` = prototype plus the latest records; never merged into `alpha`. At Gate 0 close-out, the record files are copied to `alpha` in one docs-only commit.

**Last verified commit:** see `git log -1 gate0-spike` (the records commit closing S-20261020-05).

## Completed (verified)
- **Step 0:** toolchain, layout, decisions D-019 to D-023 and D-025 (S-20261020-01).
- **Cross-AI rules and audit trail:** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, protocol, five specialist agents, registers (S-20261020-03).
- **Path A prototype** on `gate0-spike` (strict-clean). Solo-tested:
  - Server Authority active;
  - client prediction `Predicted`;
  - input bridge works;
  - speed 42 and input clamp;
  - tamper ignored;
  - fall with one elimination;
  - restore matrix twice with no double-bind;
  - camera without roll;
  - 1-frame response at 0 ms.
- **FAIL-007 and FAIL-008 fixed and retested;** FAIL-009 fix works in the spike (product adoption proposed as D-026).
- **Two-client test driver ready:** `tests/gate0/G0_two_client_driver.luau`.
- **Independent review RV-01** (Opus, read-only) applied in `0c02823`. Solo regression T-G0-039 PASS. A re-review (RV-02) of the fixes was requested; see the work log for its result.

## Failed, blocked or open
- **FAIL-004:** resolved. The native Studio MCP tools work in the current session (T-G0-040, FIXED-VERIFIED).
- **FAIL-006:** fixed. Place saved with `AuthorityMode = Server`; A1 fully evidenced (T-G0-042); solo regression passes (T-G0-043).
- **FAIL-009:** parked-avatar streaming. Spike fix works; adoption approved as **D-026** (2026-10-20). Product implementation comes in TASK-04/07.
- **A1:** complete (T-G0-042).
- **FAIL-010:** C2 instrumentation fixed (`0c02823`); unverified until the 2-client run. Related owner question Q-1.

## Outstanding tests (Gate 0)
C2, C3 (two-client part), A3 at 150 ms, A4, A5, C5 disconnect: all need the owner's 2-client session (T-G0-036). The 4-client smoke test is deferred to TASK-10. Details: [TEST_RESULTS.md](TEST_RESULTS.md), [GATE_0_REPORT.md](GATE_0_REPORT.md) section 8.

## Known risks
- **A5 may not show a rollback at 150 ms;** the defined retry is 250 ms, then INCONCLUSIVE, which blocks Gate 0.
- **Remote players' spheres may not be predicted on other clients** (to be observed in the 2-client report).
- **Attribute budget** (64 per instance; names and string values up to 50 characters) matters for TASK-04 design.
- **Antigravity's loading** of `AGENTS.md`/`GEMINI.md` is unverified.

## Prerequisites
- Studio 0.743 with `place/Gate0.rbxl` open, `AuthorityMode = Server` **saved**, and the Rojo plugin connected to `rojo serve default.project.json` (repo root).
- Claude Code started in the repo root.

## Owner actions (do these in order; about 30 minutes)
**A. Before testing**
1. In Studio (`Gate0.rbxl`), select **Workspace**. In the Properties panel confirm `AuthorityMode = Server`. Clear the search filter and take a screenshot showing NextGenerationReplication, PlayerScriptsUseInputActionSystem, SignalBehavior, UseFixedSimulation and StreamingEnabled (several screenshots are fine). Save them in `docs/evidence/gate0/` named like `YYYYMMDD-HHMMSS_A1_owner-screenshot_dependent-settings.png`.
2. Press **Ctrl+S** to save `Gate0.rbxl`. This clears FAIL-006.
3. Make sure `rojo serve default.project.json` is running in the repo root and the Rojo plugin shows **Connected**. Explorer should show `ServerScriptService.Server.Gate0Server`, `StarterPlayer.StarterPlayerScripts.Client.Gate0Client` and `ReplicatedStorage.Shared.Gate0Sim`.
4. Optional (FAIL-004 is already verified fixed): when you next restart Claude Code, open it in the repo root and run `/context` to confirm `CLAUDE.md` loads; the five `sphere-*` specialists should then be usable by name (they load only when Claude Code starts).

**B. Session 1: 0 ms latency**
5. Studio: **File ▸ Studio Settings ▸ Network ▸ Incoming Replication Lag = 0** (it reads 0 now). Alternatively, tell Claude to set it through the MCP.
6. **Test ▸ Clients and Servers**, Players = **2**, then **Start**. A Server window and 2 client windows open. Do not touch the client windows; AutoDrive moves the spheres.
7. Wait until the Server window's Output shows **both** clients' `[G0C<-...] A2 ... status=Predicted` lines. Then Claude runs the driver through the MCP if it can reach the Server window. Otherwise, in the **Server** window open **View ▸ Command Bar**, paste the whole file `tests/gate0/G0_two_client_driver.luau` and press Enter. Wait about 1.5–2 minutes for `[G0D] driver done`.
8. Close **one** client window (disconnect test) and wait 3 seconds.
9. In the Server window's **Output**, select all, copy, and save it as `docs/evidence/gate0/YYYYMMDD-HHMMSS_T-G0-036_2client_0ms_server-output.txt` (or let Claude read it through the MCP).
10. Stop the test session.

**C. Session 2: 150 ms latency (A3 and A5)**
11. Set **Incoming Replication Lag = 0.15** and repeat steps 6–10 (file name `..._2client_150ms_...`). While it runs, press **Ctrl+Shift+F6** in one client window (server-authority visualizer) and take a screenshot.
12. If the client report lines in the Output show `rollbacks=0`, repeat once with **0.25**.
13. Set Incoming Replication Lag back to **0** afterwards.

**D. Decisions for the owner**
14. ~~D-026~~ **Approved** by the owner on 2026-10-20 (all three parts).
15. **Q-1 (knockback feel; no change made yet).** The locked §8.5 knockback fully separates two colliding spheres only when they close at about 32.9–40 studs/s. In a full-speed head-on (about 84 studs/s) they are still closing at about 44 studs/s after the knockback, so Roblox's own contact physics also shapes the outcome (FAIL-010).

    The 2-client run will log both parts. Options to decide after seeing it:
    - (a) accept it and tune at playtest;
    - (b) stop sphere–sphere physical collision and resolve contacts only with §8.5 (changes the locked collision matrix in §6.2);
    - (c) cancel the remaining closing speed before applying §8.5 (changes the formula's meaning).

    No action is needed until the 2-client results are in.
16. Optional: open the repo in Antigravity and confirm it shows the `AGENTS.md`/`GEMINI.md` rules; tell Claude the result.

## Next three actions (after the owner's session)
1. Lead: analyze the two Server Outputs, record C2/C3/A3/A4/A5/C5 results and decide PASS/FAIL/INCONCLUSIVE per plan rev 4.
2. Lead: Gate 0 close-out: D-024 path selection, report, checklist boxes, docs-only commit to `alpha`.
3. If Gate 0 passes: plan TASK-01 with the multi-agent protocol (owner approval of the plan first).
