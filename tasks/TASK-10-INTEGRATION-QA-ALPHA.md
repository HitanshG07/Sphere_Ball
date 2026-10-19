# TASK-10 - Integration, Performance, Security, Visual QA, and Alpha Gate

## Preconditions
TASK-01 to TASK-09 implemented and merged. No known owner conflict is unresolved.

## Goal
Run the entire acceptance suite; report release readiness based on evidence, not confidence.

## Steps
1. Read every item in `ALPHA_ACCEPTANCE_CHECKLIST.md`.
2. Run formatter, strict analysis, project build and unit tests. Attach command logs.
3. Run local multi-client tests at 4 and 6 clients; run network emulation representative of moderate/high latency and jitter if tooling supports it.
4. Run three full matches back-to-back; test queue cancellation, disconnect, invalid loadout, ability cooldown and round cleanup.
5. Capture all required visual QA states and required display sizes.
6. Profile server/client with Developer Console/MicroProfiler; note worst spikes, script activity, memory trend, physics ownership/simulation warnings and rendering bottlenecks.
7. Test exploit cases: queue duplication, request spam, fake IDs, invalid ability while dead, client-reported KO, tampered velocity, loadout changes after lock, and reused remote payload.
8. Mark every checklist item PASS/FAIL/NOT RUN. Attach evidence path per item.
9. Fix defects only within an explicitly assigned fix pass. Do not weaken acceptance criteria.
10. Produce `docs/ALPHA_QA_REPORT.md` and a release recommendation: ACCEPT / BLOCKED.

## Exit requirements
- All mandatory checklist items PASS with evidence.
- No unresolved physics authority, hit-validation, queue consistency, hidden-avatar, cleanup or match-state defect.
- Any asset still `ASSET_PENDING` must be non-required and not referenced in release experience.
- All remaining TODOs labeled LATER or VISUAL_POLISH.

## Stop conditions
If tests require altering locked design values, changing the authority architecture, or disabling a required check, stop and ask owner for a decision. Do not publish the game or upload assets unless explicitly authorized.
