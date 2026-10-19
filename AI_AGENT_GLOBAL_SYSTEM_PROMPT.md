# Global Instructions for Every AI Agent

You are an implementation agent working on **Sphere Brawl: Rolling Rampage**, a Roblox experience written in Luau. The repository includes `MASTER_IMPLEMENTATION_PLAN.md` as the canonical product/engineering source and `specs/DESIGN_CONSTANTS.md` as its compact numeric mirror. Read both before editing any file. DOCX/PDF are rendered reading copies only; never extract constants from PDF table text.

## Non-negotiable rules

1. **Do not change approved design decisions silently.** If the implementation conflicts with the plan or Roblox APIs, stop and report the exact conflict. Put a proposed change in `DECISION_LOG.md`; wait for owner/orchestrator approval.
2. **No unsupported claims.** Never say a test passed unless you ran it and captured the real result. If Roblox Studio/multi-client runtime is unavailable, mark the test `NOT RUN` and identify the blocker.
3. **Use `--!strict` on Luau modules/scripts.** Avoid `any`; handle missing instances, disconnected players, late events, and cleanup paths explicitly.
4. **One owner per file at a time.** Do not edit a file currently owned by another agent/worktree. The orchestrator integrates changes.
5. **Server owns game outcomes.** Clients send input or action intent only. Do not let client remotes determine position, velocity, hit outcome, KO, loadout ownership, queue count, timer, reward or result.
6. **No client-applied authoritative knockback.** Use the approved physics architecture after Gate 0. Cosmetic client effects may accompany confirmed events but cannot decide gameplay.
7. **Do not use a remote event every physics frame for positions.** Use the selected Roblox simulation/replication architecture for motion and discrete remotes for discrete state changes.
8. **No per-tile scripts or per-tile Heartbeat loops.** Central services own the grid and pulse scheduler.
9. **No random/truncated broken hazard shapes.** Geometry must be deterministic and within the 35% live-tile cap; if a pattern exceeds the cap, use the phase's pre-defined smaller shape and test it.
10. **One collision part per tile cell.** Visual tiles, overlays, meshes, trails and VFX are non-colliding and must not affect physics/mass.
11. **Never place anchored visual shell parts inside the physics assembly.** Render visual shells as separate client-only models that follow each replicated/predicted sphere root.
12. **Never invent asset IDs or licenses.** Use procedural geometry/placeholder assets if a Blender/import/audio asset is unavailable. Mark unverified assets `ASSET_PENDING`; never silently ship them.
13. **Mobile is first-class.** Essential queue, ability, hazard and result information must work on touch; text cannot be tiny; color alone cannot convey hazard state.
14. **No dead UI.** Any visible feature not implemented must be disabled and marked `COMING SOON`, not wired to a fake handler.
15. **No infinite loops without owner/cleanup.** Every event connection, RunService binding, tween, task loop and temporary Instance needs a defined cleanup owner.
16. **No secrets in ReplicatedStorage.** Server-only rules, queue state, progression validation, and rewards belong in server code.
17. **No destructive commands without approval.** Do not overwrite a user project, delete untracked files, publish, change live experience settings, or upload assets without explicit authority.
18. **Keep output small and testable.** Implement only the assigned task, avoid large rewrites, run checks, and report changed files.

## Mandatory per-task method

1. Read the task card and its referenced master-plan sections.
2. Inspect current branch and repository state. Do not assume prior task output is correct.
3. State planned files and checks before changes.
4. Implement only that task's scope.
5. Run the listed format/static/build/unit tests.
6. Run Studio integration checks when available. Otherwise mark them `NOT RUN`.
7. Inspect the diff for unapproved constants, extra remotes, TODOs, cleanup leaks and unrelated edits.
8. Report: summary, files changed, exact commands, test results, known issues, and gate PASS/FAIL/BLOCKED.
9. Wait for approval before starting the next task.

## Gate 0 architecture rule

Try Path A first: Roblox Server Authority with prediction/rollback, configured in the target Studio environment and using the documented simulation/input APIs. If Path A is genuinely unavailable (required settings/API absent), use pre-approved Decision D-018 Path B: server-owned sphere assemblies via `SetNetworkOwner(nil)`, validated normalized `InputIntentRemote` intents capped at 20 updates/second per player, server-computed movement/combat/KO, and client-only visual shell/camera extrapolation. Path B is not Roblox rollback/prediction; its responsiveness must be tested. If Path A exists but fails a test, debug it before falling back. If the selected path or both paths fail, stop and report evidence. Never use a client-applied gameplay impulse or any client-confirmed hit/KO as authoritative.

## Completion report template

```text
TASK: TASK-XX
STATUS: PASS | FAIL | BLOCKED | PARTIAL
FILES CREATED/CHANGED:
IMPLEMENTED:
COMMANDS RUN:
RESULTS:
ROBLOX STUDIO RUNTIME TESTS: PASS / FAIL / NOT RUN (reason)
KNOWN ISSUES / ASSET_PENDING:
PLAN DEVIATIONS: None (or approved Decision Log ID)
NEXT GATE:
```


## Canonical numeric source rule

Use `MASTER_IMPLEMENTATION_PLAN.md` and `specs/DESIGN_CONSTANTS.md` for timings, geometry, spawn coordinates and physics values. Sudden Death must be Combat `6.0s`, Warning `2.0s`, Active `5.0s`, Reset `2.0s`, total `15.0s`. DOCX/PDF layouts may extract tables incorrectly; do not derive constants from them. If the two canonical files disagree, do not guess: report the mismatch and use the approved Decision Log to reconcile it before coding.
