# Project Status — Sphere Brawl: Rolling Rampage

Current-state snapshot. History: [WORK_LOG.md](WORK_LOG.md). Earlier versions of this file are in Git history.

**Updated:** 2026-10-20, session S-20261020-09 (lead: Claude Code, Opus 5.5)
**Milestone:** TASK-01 (project scaffolding, types, configuration and remotes). Gate 0 PASSED (2026-10-20, Path A, D-024).
**Overall status:** Part A (GitHub publishing setup) done in S-20261020-09; TASK-01 in progress on branch `task01`.
**Waiting on:** nothing from the owner until TASK-01 finishes. TASK-02 needs owner approval before it starts.

**GitHub:** `https://github.com/HitanshG07/Sphere_Ball`, PUBLIC (owner decision), default branch `alpha` (set S-20261020-09).
**Branches:**
- `main` = `f726ddd` (untouched spec baseline; `origin/main`).
- `alpha` = integration branch; last pushed hash in the work log (S-20261020-09).
- `gate-0` = `bc4cfa7` (Gate 0 prototype; `origin/gate-0`; never merged into `alpha`). Local alias `gate0-spike` tracks `origin/gate-0`; a duplicate local `gate-0` branch is kept until the owner authorizes deleting it.
- `task01` = TASK-01 work, branched from `alpha`.

## Completed (verified)
- **Gate 0** passed with Path A; report `GATE_0_REPORT.md` §10; decisions D-024 to D-027.
- **Cross-AI rules and audit trail** (S-20261020-03), plus GitHub rules in `AGENTS.md` and protocol §7 (S-20261020-09).
- **Canonical Studio place** `place/Gate0.rbxl` is version-controlled: no scripts, `AuthorityMode` Server (T-PUB-001).
- **FAIL-012** (shell substitution erased this file's "Waiting on" text) fixed.

## Failed, blocked or open
- **FAIL-009:** parked-avatar streaming. Spike fix works; product implementation (D-026) comes in TASK-04/07.
- **Antigravity's loading** of `AGENTS.md`/`GEMINI.md` is unverified (owner to confirm in Antigravity).

## Known risks
- **Public repository:** existing Gate 0 evidence and commit metadata contain the owner's Roblox username, UserId and email. Only new evidence is redacted; removing the old values needs a history rewrite (owner approval required).
- **Attribute budget** (64 per instance; names and string values up to 50 characters) matters for TASK-04 design.
- **4-client smoke test** deferred to TASK-10.

## Prerequisites
- Studio with `place/Gate0.rbxl` open and the Rojo plugin connected to `rojo serve default.project.json` (repo root).
- Claude Code started in the repo root (`C:\Sphere_ball_rblox\Sphere_Brawl_AI_Agent_Task_Pack`), so `CLAUDE.md` and the `sphere-*` agents load.

## Next three actions
1. Lead: finish TASK-01 on `task01` (plan: `docs/TASK-01_PLAN.md`) and run its gate.
2. Lead: push `task01`, merge into `alpha` after the gate passes, push and record.
3. Owner: approve TASK-02 before it starts.
