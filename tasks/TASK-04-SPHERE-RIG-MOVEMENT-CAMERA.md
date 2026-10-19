# TASK-04 - Sphere Lifecycle, Simulation, Movement, Visual Shell, and Camera

## Preconditions
Gate 0 PASS; TASK-01 accepted; arena collider available.

## Goal
Deliver a controllable sphere with a stable horizon and separated visual roll.

## Files
- `src/server/Core/SphereService.luau`
- `src/shared/Modules/SimulationMath.luau`
- `src/client/Controllers/InputController.luau`
- `src/client/Controllers/SphereMovementController.luau`
- `src/client/Controllers/SphereVisualRig.luau`
- `src/client/Controllers/CameraController.luau`
- relevant unit/integration tests

## Requirements
1. Use the architecture selected and documented at Gate 0. Path A uses Server Authority + `BindToSimulation`; pre-approved Path B uses `SetNetworkOwner(nil)` and validated client input intent only. Do not use `SetNetworkOwner(player)` as a fallback. Never accept client-authoritative collisions, knockback, or eliminations.
2. Inputs: WASD/left stick, Shift boost, Space brake, E core ability. On touch, show equivalent buttons. Keep movement and core simulation deterministic according to the authority model.
3. SphereRoot is a 6-stud invisible collidable sphere. Configure attachment/forces/constraints only as verified by the target simulation API.
4. Visible shell is client-only and non-colliding; never anchor it as a child of the physics assembly. For all visible sphere roots, create shells in a separate client visual folder and update them on PreRender.
5. Compute visual roll from position delta and sphere radius, with stable axis handling for low/zero movement. Large corrections are interpolated visually without rotating camera.
6. Camera follows a position-only target, keeps horizon stable, offers normal follow distance/offset, and has reduced-shake/disable option.
7. Implement acceleration, drag, lateral steering, brake, normal speed cap 42 and absolute speed cap 55 using shared config only.
8. Use these exact initial-match spawn slots. Grid cells `(X,Z)` are `(0,-3)`, `(3,-2)`, `(3,2)`, `(0,3)`, `(-3,2)`, `(-3,-2)`. Convert each once using `ArenaCFrame:PointToWorldSpace(Vector3.new(12*X, 4.15, 12*Z))`; for arena center `(0,50,0)` aligned to world axes, the world sphere centers are `(0,54.15,-36)`, `(36,54.15,-24)`, `(36,54.15,24)`, `(0,54.15,36)`, `(-36,54.15,24)`, `(-36,54.15,-24)`. Assign deterministically by sorted UserId to slot index. These are initial spawn points only; no mid-match respawns. On elimination, disable input before spectator camera. On cleanup, remove visual shell connections and root.

## Tests
- forward input reaches target speed within configured tolerance in controlled test
- brake decelerates predictably
- left/right turn, reverse steering, no-input coast
- no camera roll/jitter with shell rolling
- no seam snag or unexplained vertical bounce
- fall remains possible; no Y position snap
- shell never participates in collisions or affects root mass
- every spawn slot is centered on the correct D=3 cell, live at match start, inside the collider bounds, and pairwise >12 studs apart
- reconnect/character reset cleans and rebinds exactly once

## Handoff
Include a 2-client and 4-client movement report, screen capture, values measured, and authority/prediction notes.
