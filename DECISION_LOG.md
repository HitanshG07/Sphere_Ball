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

## Owner decisions and Gate 0 API corrections (2026-10-20)

D-001 through D-018 are unchanged. The entries below fill specification gaps found during the Gate 0 review; none changes a locked value. D-024 is reserved for the Gate 0 path selection and is written only at Gate 0 close-out, with evidence.

### D-019: Shift Burst Boost (APPROVED / TUNING)
- **Date:** 2026-10-20
- **Requested by:** Orchestrator (spec gap: Master Plan §11.7 and Tasks 04/08 require a "Shift boost" key and touch button but define no mechanic, value or cooldown)
- **Approved by:** Project owner (explicit choice "Burst boost", 2026-10-20)
- **Decision:** Shift (keyboard) or the touch Boost button requests a one-time +12 studs/s horizontal velocity delta along the move input direction; if there is no input, along current horizontal velocity; if both are near zero, along facing. Cooldown 4.0 s. Horizontal speed remains capped at 55 studs/s. Outgoing impact factor 1.0 (no combat bonus). AbilityService validates the request like a core ability (alive, valid phase, cooldown).
- **Rationale:** Fills an undefined control without changing locked values; deliberately weaker than Kinetic Overdrive Dash (+22, 8 s, 1.25x for 1 s) so the cores stay distinct.
- **Alternatives considered:** hold-to-sprint (42 to 50 top speed, no cooldown; rejected because it makes the 42 top speed meaningless); defer boost (rejected: removes a specified control).
- **Files/contracts affected:** Master Plan §8.4 and §11.7; `specs/DESIGN_CONSTANTS.md`; Tasks 04, 06, 08; future `GameConfig`, `AbilityService`, `InputController`, HUD.
- **Migration/backward compatibility:** None (no code exists yet).
- **Tests required:** delta is +12 within tolerance; a second request inside 4 s is rejected; horizontal speed <= 55 after boost; rejected while eliminated or outside a combat phase.
- **Status:** APPROVED

### D-020: Alpha sphere-skin unlock rule (APPROVED)
- **Date:** 2026-10-20
- **Requested by:** Orchestrator (spec gap: §3.1 requires locked skins to appear locked and be rejected, but does not say which skins are unlocked)
- **Approved by:** Project owner (explicit choice, 2026-10-20)
- **Decision:** `Default` and `Neon` are unlocked for every player. `Gold` and `Void` are previewable but locked; LoadoutService rejects equipping them with a lock reason. The unlock inventory is session-only and held in server code (no persistence in Alpha; the unlock pipeline is TASK-11 / LATER).
- **Rationale:** Exercises the locked-item rejection path with real items instead of only forged IDs.
- **Files/contracts affected:** Master Plan §3.1; `specs/DESIGN_CONSTANTS.md`; Tasks 07, 08; future `LoadoutService`, customization UI.
- **Migration/backward compatibility:** None.
- **Tests required:** equipping Gold or Void is rejected with a lock reason and the UI never shows them equipped; Default and Neon equip succeeds before loadout lock.
- **Status:** APPROVED

### D-021: Cosmetic IDs and customization tabs (APPROVED, canonical)
- **Date:** 2026-10-20
- **Requested by:** Orchestrator (spec gap: `TrailId`/`EffectId` values are never enumerated; §11.7 lists both "Ball" and "Skins" tabs but the data model has only one sphere-skin category)
- **Approved by:** Project owner (approval of execution plan rev 4, 2026-10-20). This single definition supersedes an earlier, shorter draft list; no other D-021 variant exists.
- **Decision:** `TrailId = "None" | "CoreStreak" | "CyanStreak"`; `EffectId = "StandardSpark" | "CoreBurst"`; all unlocked and cosmetic-only. Customization tabs: Build = `ChassisId`, Skins = `SphereSkinId` (the shot list's "Ball/Skin" capture), Core = `CoreId`, Trails = `TrailId`, Effects = `EffectId`. The "Ball" tab remains visible but disabled and labelled `COMING SOON` (permitted by §3.2), so all six §11.7 tabs exist and none is a dead button.
- **Rationale:** Smallest content set that makes every category a real choice, with no invented mechanics.
- **Files/contracts affected:** Master Plan §3.1 and §11.7; `specs/DESIGN_CONSTANTS.md`; Task 08; future `Types`, `GameConfig`, customization UI.
- **Migration/backward compatibility:** None.
- **Tests required:** unknown trail or effect IDs are rejected; the Ball tab is non-interactive and labelled `COMING SOON`.
- **Status:** APPROVED

### D-022: Hard-timeout placement score (APPROVED)
- **Date:** 2026-10-20
- **Requested by:** Orchestrator (spec gap: the §4.2 tiebreak starts with "highest current placement score", which is not defined)
- **Approved by:** Project owner (approval of execution plan rev 4, 2026-10-20)
- **Decision:** At the 150 s hard timeout, every player still alive outranks every eliminated player. Eliminated players rank by elimination time, latest first; eliminations in the same server step share a placement. Remaining ties use the existing §4.2 chain: highest valid knockouts, then longest survival time, then a shared tie. Never random.
- **Rationale:** Defines the term without reordering the locked tiebreak chain.
- **Files/contracts affected:** Master Plan §4.2; `specs/DESIGN_CONSTANTS.md`; Task 07; future `ResultsService`.
- **Migration/backward compatibility:** None.
- **Tests required:** timeout fixtures for survivor versus eliminated, KO tiebreak, survival tiebreak, shared tie and same-step eliminations.
- **Status:** APPROVED

### D-023: Holding pods, replication focus and restore matrix (APPROVED)
- **Date:** 2026-10-20
- **Requested by:** Orchestrator and project owner review (§5.4 references a `LobbyConfig` file absent from the §10.2 tree; StreamingEnabled must stream the arena while the avatar is parked; the owner required explicit restoration rules)
- **Approved by:** Project owner (approval of execution plan rev 4, 2026-10-20)
- **Decision:** `LobbyConfig` is implemented as the `GameConfig.Lobby` section (no new file). Six holding pods: anchored 10x1x10 floor, top surface Y=200, centred at `(2000 + 20*(i-1), 200, 2000)` for i = 1..6, collision group `LobbyAvatar`, outside camera view and outside the streaming radius of the play areas. `Player.ReplicationFocus` follows the player's SphereRoot during play and the spectated root or an arena focus part while spectating. Per §5.4 step 5 (LOCKED), the avatar stays hidden after elimination until Results/Cleanup. Restore matrix:

| Event | Sphere | Input / ability | Camera | ReplicationFocus | Avatar |
|---|---|---|---|---|---|
| Elimination | removed from simulation, then destroyed | client bindings unbound; server rejects requests | spectator follow | spectated root or arena focus part | stays hidden in pod |
| Disconnect | destroyed; registry and references cleared | connections disconnected | n/a | n/a | saved-property record deleted |
| Match end, then Cleanup | all roots destroyed; client shells destroyed | all bindings unbound | `Custom`, subject = Humanoid | `nil` (default) | saved properties restored exactly, unanchored, moved to Hub spawn; missing Character triggers `LoadCharacter` |

  Cleanup ends with an invariant check: no SphereRoot remains, no saved-property records remain, every player's ReplicationFocus is nil, and connection counts are back to baseline.
- **Rationale:** Prevents broken cameras, hidden avatars and unstreamed arenas while respecting the locked §5.4 elimination rule.
- **Files/contracts affected:** Master Plan §5.4; `specs/DESIGN_CONSTANTS.md`; Tasks 04, 07; future `GameConfig`, `PlayerLifecycle`, `SphereService`, `CleanupService`, `CameraController`, `SpectatorController`.
- **Migration/backward compatibility:** None.
- **Tests required:** Gate 0 C5 (miniature); TASK-04 and TASK-07 full matrix tests for elimination, disconnect, match end and three consecutive rounds.
- **Status:** APPROVED

### D-024: Gate 0 physics-architecture selection (RESERVED)
- Reserved. Written at Gate 0 close-out with the selected path (A or B) and links to evidence in `docs/GATE_0_REPORT.md`.

### D-025: Path A API usage rules (APPROVED; correction to §9.2 wording, no gameplay change)
- **Date:** 2026-10-20
- **Requested by:** Project owner review and Creator Hub verification (2026-10-20)
- **Approved by:** Project owner (approval of execution plan rev 4, 2026-10-20)
- **Decision:**
  1. The server creates SphereRoot instances. Each client calls `RunService:SetPredictionMode(ownRoot, Enum.PredictionMode.On)` after its root replicates and verifies `RunService:GetPredictionStatus(ownRoot) == Enum.PredictionStatus.Predicted`. Server code never calls `SetPredictionMode`.
  2. Input bridge: the server has no camera, so the simulation `Move` action (Direction2D, in a server-created InputContext under the Player) is world-space: `Vector2(x, y)` maps to the horizontal world vector `(x, 0, y)`. Its only binding has `Type = Enum.InputBindingType.Scriptable`. The client InputController reads hardware (keyboard, gamepad, touch) through a client-only InputContext, computes `camForward = Vector3.new(look.X, 0, look.Z).Unit`, `camRight = camForward:Cross(Vector3.yAxis)` and `world = camRight*raw.X + camForward*raw.Y`, and fires `InputBinding:Fire(Vector2.new(world.X, world.Z))` each frame outside the simulation. The simulation clamps the magnitude to <= 1 again. The deprecated `InputAction:Fire` is never used. Test automation (AutoDrive) is only an alternative source feeding the same bridge with the same mapping; it is gated by `RunService:IsStudio()`, exists only in test code and never ships in production controllers. Under Path B the same world vector is the `InputIntentRemote` payload.
  3. `BindToSimulation` callbacks write only synchronized state (velocities and attributes on predicted instances). No VFX, audio, remotes, logging or instance creation runs inside them. Server-only outcomes (hits, KO attribution, hazard one-shots such as the Boost Runway stamp) are written as attributes with monotonically increasing sequence IDs, so a client resimulation never re-applies them; presentation and logging run in render-step or Heartbeat observers and deduplicate by sequence ID.
- **Rationale:** The Creator Hub marks `InputAction:Fire` deprecated and documents `InputBinding:Fire` with Scriptable bindings; simulation callbacks can re-run during client resimulation; prediction is configured client-side.
- **Files/contracts affected:** Master Plan §9.2; `specs/DESIGN_CONSTANTS.md` (Gate 0 section); `tasks/TASK-00-GATE-0-ENVIRONMENT-AUDIT.md`; `specs/STUDIO_GATE_00.md`; `ALPHA_ACCEPTANCE_CHECKLIST.md`; Task 04.
- **Migration/backward compatibility:** None (no code exists yet).
- **Tests required:** Gate 0 A2 (prediction status), A5 (rollback with FX deduplication) and C3 (input magnitude clamp); verification that the Scriptable bridge reaches the server simulation and of which side must create the binding.
- **Status:** APPROVED
