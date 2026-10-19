# Project Status — Sphere Brawl: Rolling Rampage

Current-state snapshot. History lives in [WORK_LOG.md](WORK_LOG.md) (earlier versions of this file are in Git history, for example commit `fc109f8`).

**Updated:** 2026-10-20, session S-20261020-03 (lead: Claude Code 2.1.303, Opus 5.5)
**Milestone:** Gate 0 (TASK-00), environment and physics-authority feasibility
**Overall status:** IN PROGRESS. Gate 0 has **not** passed. TASK-01 has **not** started and is not authorized.
**Branches:**
- `main`: `f726ddd`, untouched spec baseline.
- `alpha`: approved work and records.
- `gate0-spike`: Gate 0 prototype only, never merged. Currently equal to `fc109f8` plus stash `stash@{0}` holding the unanalyzed draft `src/shared/Gate0Sim.luau`.

**Last verified commit:** `fc109f8` on `alpha` (Step 0). This session's governance commit is recorded in the work log.

## Completed (verified)
- Step 0 ([WORK_LOG.md](WORK_LOG.md) S-20261020-01):
  - git baseline;
  - Rokit-pinned toolchain;
  - `src/` layout;
  - `rojo build` and sourcemap PASS;
  - decisions D-019 to D-023 and D-025 recorded (D-024 reserved);
  - insert-only doc sync.
- Owner Studio handoff (S-20261020-02): `place/Gate0.rbxl` open in Studio, `rojo serve` 7.4.4 running and synced (T-G0-003).
- G0-1 API probe: all Path A APIs present (T-G0-004). Script access to `AuthorityMode` is restricted, as expected (T-G0-005).
- Cross-AI development system (S-20261020-03): `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, [AI_DEVELOPMENT_PROTOCOL.md](AI_DEVELOPMENT_PROTOCOL.md), five `.claude/agents/` specialists, and the audit-trail registers.

## Failed, blocked or open
- [FAIL-004](FAILURES_AND_FIXES.md): Studio MCP tools not loaded in the Claude session. Fix FIXED-UNVERIFIED (user-scope registration); workaround is a direct stdio client.
- [FAIL-006](FAILURES_AND_FIXES.md): the saved `place/Gate0.rbxl` has `AuthorityMode = Automatic`; the live session shows Server. OPEN, needs the owner to save.
- A1 dependent settings not yet visible in evidence (T-G0-006 INCONCLUSIVE).

## Outstanding tests (Gate 0)
C1–C5 and A2–A6 are NOT RUN (T-G0-009 to T-G0-015). The 4-client smoke test is deferred to TASK-10. See [TEST_RESULTS.md](TEST_RESULTS.md) and [GATE_0_REPORT.md](GATE_0_REPORT.md).

## Known risks
- Path A input bridge (world-space Scriptable binding fired by the client) is unverified until C1/C2 run.
- Rollback may not trigger reliably at 150 ms (A5 has a defined retry and INCONCLUSIVE rule).
- MCP play is solo only; multi-client tests depend on the owner.
- Antigravity loading of `AGENTS.md`/`GEMINI.md` is unverified (third-party documentation only).

## Prerequisites
- Studio 0.743 with `place/Gate0.rbxl` open, `AuthorityMode = Server` **saved**, Rojo connected (`rojo serve default.project.json` from the repo root).
- Rokit tools resolve only inside the repo.
- Start Claude Code in the repo root.

## Evidence and reports
[GATE_0_REPORT.md](GATE_0_REPORT.md), [TEST_RESULTS.md](TEST_RESULTS.md), [FAILURES_AND_FIXES.md](FAILURES_AND_FIXES.md), `docs/evidence/gate0/` (untracked until the Gate 0 docs-only close-out commit), [DECISION_LOG](../DECISION_LOG.md).

## Next three actions
1. Owner: in Studio, press Ctrl+S on `Gate0.rbxl` (keeping `AuthorityMode = Server`) and screenshot the Workspace Properties showing the five dependent settings (clears FAIL-006 and T-G0-006).
2. Lead: switch to `gate0-spike`, restore the stashed draft, finish and analyze the prototype, and run C1 and A2 in MCP solo play.
3. Owner + lead: two-client session (C2–C5, A3–A6), including 150 ms Network Simulation for A5.
