# Decision Log

Do not edit the approved baseline entries below unless a human owner authorizes a change. New decisions must include date, decision ID, who approved it, rationale, impacted files, migration plan, and test impact.

## Approved baseline decisions

| ID | Decision | Status |
|---|---|---|
| D-001 | Game identity/theme is Sphere Brawl: Rolling Rampage in the Kinetic Grid world. | LOCKED |
| D-002 | Alpha is Free-for-All, 4-6 players, one 9x9 arena, one active match per server. | LOCKED |
| D-003 | The arena uses timed Board Pulse hazards; collisions never create hazard tiles. | LOCKED |
| D-004 | Alpha has Ice Corridor, Magnetic Storm, Boost Runway only. | LOCKED |
| D-005 | Ring D=4 collapses first (81 -> 49 cells), then D=3 (49 -> 25 cells). | LOCKED |
| D-006 | Physical queue-pad and Quick Queue use the same unique server-owned queue table. | LOCKED |
| D-007 | Portal-sourced queue entries expire after a short exit grace period; Quick Queue persists until cancel/assignment/disconnect. | LOCKED |
| D-008 | Alpha chassis choices are cosmetic silhouettes with identical combat stats. | LOCKED |
| D-009 | Core abilities and timing/physics values follow MASTER_IMPLEMENTATION_PLAN.md. | LOCKED baseline values |
| D-010 | No unverified asset IDs or third-party assets may ship. | LOCKED |
| D-011 | Path A Roblox Server Authority is preferred and must be tested at Gate 0. If its required settings/API are genuinely unavailable, use the pre-approved Path B server-owned physics fallback in D-018; if the selected path fails validation, stop. | LOCKED / GATE |
| D-012 | Tile visuals are separate, non-colliding objects; exactly one 12x2x12 collision tile per grid cell. | LOCKED |
| D-013 | No client-applied knockback can determine an authoritative combat outcome. | LOCKED |
| D-014 | Match queue is same-server for Alpha; cross-server matchmaking is LATER. | LOCKED |

## New decision template

```text
ID: D-XXX
Date:
Requested by:
Approved by:
Decision:
Reason:
Alternatives considered:
Files/contracts affected:
Migration/backward compatibility:
Tests required:
Status: PROPOSED / APPROVED / REJECTED
```

## Approved Gate 0 and spawn corrections (2026-10-18)

### D-015: Lobby main spawn orientation (LOCKED)
- **Date:** 2026-10-18
- **Requested by:** Project owner via supplied technical patch
- **Approved by:** Project owner
- **Decision:** Construct the Hub main spawn using `CFrame.lookAt(Vector3.new(0, 150, -334), Vector3.new(0, 150, -300))`, so the avatar faces +Z toward the central Queue Portal. Never rely on the default orientation.
- **Rationale:** The queue portal is at greater Z than the spawn. An unrotated `CFrame.new(...)` faces -Z and points away from the plaza.
- **Files/contracts affected:** Master plan Section 2.4; `tasks/TASK-03-KINETIC-HUB-ENVIRONMENT.md`; lobby builder/tests.
- **Migration/backward compatibility:** Replace the ambiguous spawn orientation instruction; no save-data impact.
- **Tests required:** Main-spawn `LookVector` dot the horizontal direction toward the portal must be `> 0.99`; capture a spawn-to-queue screenshot.
- **Status:** APPROVED / LOCKED

### D-016: Deterministic six-slot arena spawn coordinates (LOCKED)
- **Date:** 2026-10-18
- **Requested by:** Project owner via supplied technical patch
- **Approved by:** Project owner
- **Decision:** Use the six exact D=3 grid-cell spawn slots listed in `specs/DESIGN_CONSTANTS.md` and Master Plan Section 6.5. Assign slots deterministically; do not randomize. Their world positions are defined for arena center `(0, 50, 0)` and sphere center Y `54.15`.
- **Rationale:** Tile-centered slots are reproducible and avoid placing a sphere across tile-corner seams. Note: the minimum pairwise distance for the listed coordinates is approximately `37.95` studs; do not describe the slots as an exact regular 60-degree radial arrangement.
- **Files/contracts affected:** Master plan Section 6.5; `specs/DESIGN_CONSTANTS.md`; `tasks/TASK-04-SPHERE-RIG-MOVEMENT-CAMERA.md`; spawn integration tests.
- **Migration/backward compatibility:** Replaces the approximate radius-based instruction. These are initial-match slots only; no mid-match respawns occur.
- **Tests required:** Each slot resolves to its listed cell; live at match start; sphere footprint is safely inside that tile; pairwise spacing >= `12` studs; slot is not reused after elimination.
- **Status:** APPROVED / LOCKED

### D-017: Canonical Board Pulse timing source (LOCKED)
- **Date:** 2026-10-18
- **Requested by:** Project owner via supplied technical patch
- **Approved by:** Project owner
- **Decision:** `MASTER_IMPLEMENTATION_PLAN.md` and `specs/DESIGN_CONSTANTS.md` are the machine-readable timing sources. Sudden Death is `SafeCombat=6.0s`, `Warning=2.0s`, `Active=5.0s`, `Reset=2.0s`, `Total=15.0s`. DOCX/PDF are rendered reading copies; agents must not parse their extracted table text for constants.
- **Rationale:** Prevent PDF text/table extraction from swapping timing columns and creating divergent implementation.
- **Files/contracts affected:** Master plan Section 0.2 / 7.2; `specs/DESIGN_CONSTANTS.md`; PulseService and pulse tests; global agent instructions.
- **Migration/backward compatibility:** Any generated constant mirror must be compared to the canonical sources.
- **Tests required:** Arithmetic asserts total cycle lengths of 28s, 21s, and 15s; tests assert named Warning/Active values rather than only row position.
- **Status:** APPROVED / LOCKED

### D-018: Gate 0 physics architecture fallback (LOCKED)
- **Date:** 2026-10-18
- **Requested by:** Project owner via supplied technical patch
- **Approved by:** Project owner
- **Decision:** Gate 0 tries Path A, Roblox Server Authority with prediction/rollback, first. If the required mode/settings/APIs are genuinely unavailable in the target environment, Path B is pre-approved: server-owned sphere physics via `SetNetworkOwner(nil)`, validated client input intents only, server-computed motion/impacts/knockback/KO, and client-only visual shell/camera interpolation. No client-applied gameplay impulse is allowed.
- **Rationale:** Do not block all implementation solely because a beta/configuration surface is unavailable, while preserving server control over competitive outcomes. Path B is a fallback server-owned simulation, not the Roblox rollback/prediction model; responsiveness must be tested.
- **Files/contracts affected:** Master plan Section 9; `specs/STUDIO_GATE_00.md`; `tasks/TASK-00-GATE-0-ENVIRONMENT-AUDIT.md`; Task 04; global prompt; input remote contract.
- **Migration/backward compatibility:** Select one architecture at Gate 0 and record it in `docs/GATE_0_REPORT.md`; never mix both paths inside product gameplay.
- **Tests required:** Two-client and four-client movement/collision tests, malicious-input/KO test, rate-limit test, and latency test under Studio Network Simulation where available. If both paths fail, stop for owner review.
- **Status:** APPROVED / LOCKED
