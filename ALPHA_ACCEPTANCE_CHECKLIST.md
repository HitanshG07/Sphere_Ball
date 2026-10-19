# Alpha Acceptance Checklist

Every item must be marked `PASS`, `FAIL`, or `NOT RUN` with evidence. Release is blocked by every FAIL or NOT RUN item. Do not convert a failure into a pass by weakening a test.

## Gate 0 - Studio and network architecture
- [ ] Target Studio/version and exact feature/settings availability are recorded.
- [ ] Exactly one architecture path is selected and documented: Path A (Roblox Server Authority) or, only if Path A's required setting/API is genuinely unavailable, Path B (server-owned physics fallback).
- [ ] Path A settings/API and two-client movement/prediction/correction smoke test pass, OR Path B server ownership (`SetNetworkOwner(nil)`), validated input-intent rate limit (<=20 updates/second per player), two-client test, and representative-latency test pass.
- [ ] Four-client movement/collision smoke test passes before Alpha acceptance.
- [ ] Server owns authoritative movement outcome under selected model: hit, knockback, ability effects, elimination, queue, match timer and result state.
- [ ] No client-applied authoritative impulse or client-authoritative hit/KO path exists.
- [ ] `docs/GATE_0_REPORT.md` identifies the selected path, exact settings, test evidence, unrun tests and known limitations.

## Repository and type contracts
- [ ] Rojo project builds, if Rojo is used.
- [ ] All gameplay Luau uses `--!strict` and analyzer has no unapproved errors.
- [ ] Every remote has a documented schema, direction, validation and rate limit.
- [ ] No unapproved duplicate service/module or second source of truth exists.
- [ ] Decision log contains all approved departures from baseline.

## Grid and collision surface
- [ ] Grid generation creates exactly 81 unique cells.
- [ ] Each cell has exactly one collidable `CollisionTile` and non-colliding visuals.
- [ ] Grid coordinate round-trip passes for every coordinate in [-4,4].
- [ ] Ring D=4 contains 32 cells; first collapse leaves 49.
- [ ] Ring D=3 contains 24 cells; second collapse leaves 25.
- [ ] Tiles are edge-to-edge with no collision gaps; no stacked colliders.
- [ ] Regeneration creates 81 cells and resets all tile state after each round.
- [ ] Six initial sphere spawns use the exact D=3 cell centers in `specs/DESIGN_CONSTANTS.md`, are fully above live tiles, and are pairwise at least 12 studs apart.

## Sphere movement and camera
- [ ] Sphere collider diameter is 6 studs; visual shell never collides.
- [ ] Visual shell is not anchored/welded into physics assembly.
- [ ] Camera horizon remains stable; shell roll never rotates camera.
- [ ] Acceleration, braking, top speed and speed cap meet configured tolerance.
- [ ] No seam snag or unexplained vertical bounce in the arena.
- [ ] Sphere can fall naturally and is not Y-snapped back onto the board.
- [ ] Desktop, touch and supported controller inputs route into the same validated input state.

## Board Pulse
- [ ] Opening cycle total is exactly 28 seconds (14 + 3.5 + 7 + 3.5).
- [ ] MidGame cycle total is exactly 21 seconds (10 + 2.5 + 6 + 2.5).
- [ ] SuddenDeath cycle total is exactly 15 seconds (6 + 2 + 5 + 2).
- [ ] Server emits deterministic pattern metadata/timestamps.
- [ ] Clients render warnings from synchronized timestamps, not remote arrival time.
- [ ] Ice Corridor geometry is continuous where specified and within 35% cap.
- [ ] Magnetic Storm anchor/radius do not include destroyed/pending cells.
- [ ] Boost Runway direction is cardinal and uniform one-way.
- [ ] Pattern tile count never exceeds floor(live tiles * 0.35).
- [ ] Boost activates at most once per sphere per event.
- [ ] Every hazard cleanly resets before ring collapse.
- [ ] Late-client state snapshot reconstructs the current hazard state correctly.

## Combat and cores
- [ ] Head-on and glancing-impact fixtures pass.
- [ ] Closing speed below 10 studs/s does not trigger knockback.
- [ ] Knockback delta is bounded and does not exceed configured cap.
- [ ] Pairwise cooldown is symmetric (A/B == B/A).
- [ ] Kinetic ability speed and 1-second impact buff are correct.
- [ ] Cryo drift cancellation, immunity and resistance windows are correct.
- [ ] Magnetic ability selects nearest valid target with deterministic tie-break.
- [ ] Magnetic ability with no valid target shows feedback and does not consume cooldown.
- [ ] Horizontal speed remains capped at 55 studs/s.
- [ ] Client cannot select attacker, victim, hit normal, velocity, KO or reward.

## Queue, loadout and lobby
- [ ] Physical pad dwell <1 second never queues a player.
- [ ] Physical pad dwell >=1 second joins once.
- [ ] Portal entry removed after 0.5 seconds outside pad.
- [ ] Quick Queue persists off pad until cancellation/assignment/disconnect.
- [ ] Pad + Quick Queue concurrent requests still produce one UserId entry.
- [ ] Six players trigger 8-second countdown; 4-5 start after 25-second wait plus 10-second countdown.
- [ ] Less than four players never starts a match.
- [ ] Queue decrease below minimum cancels/repairs countdown correctly.
- [ ] Loadout locks at T-5 and invalid IDs/locked items are rejected.
- [ ] R15 avatar properties restore exactly after match/elimination/disconnect.
- [ ] Hub main spawn faces +Z toward the physical queue portal (`CFrame.lookAt` assertion passes); route to customization, mode board and shop is unobstructed.

## Match lifecycle and cleanup
- [ ] Opening runs two 28-second cycles, then Collapse1.
- [ ] MidGame runs two 21-second cycles, then Collapse2.
- [ ] SuddenDeath repeats 15-second cycles until winner/timeout.
- [ ] Falling below Y=15 eliminates once only.
- [ ] Attribution expires at 5 seconds and resets between rounds.
- [ ] Eliminated player cannot move, attack, use ability or affect hazard physics.
- [ ] Results compute placements, KOs and survival time server-side.
- [ ] Results panel lasts 8 seconds and has working Return to Hub.
- [ ] Three sequential rounds complete with no stale tile/hazard/connection state.

## UI / visuals / audio / accessibility
- [ ] All active lobby buttons work; unimplemented features are disabled/Coming Soon.
- [ ] Customization preview creates no physics and cleans render loops on close.
- [ ] Hazard state is distinguishable by shape/icon/motion as well as color.
- [ ] Camera shake can be disabled and remains within amplitude/time budget.
- [ ] Audio IDs are permission-verified or explicitly pending; no fake IDs ship.
- [ ] Low-quality/mobile VFX budget is tested.
- [ ] 1920x1080, 1280x720, 4:3 tablet and narrow phone layouts have no critical overlap/cutoff.
- [ ] Keyboard controls and touch buttons both work; cooldowns show correctly.

## Security/performance/release
- [ ] Remotes have server validation and rate limits.
- [ ] No client can set authoritative queue counts, timers, hits, scores or persistent data.
- [ ] Six-client test passes under network emulation.
- [ ] Developer Console/MicroProfiler reviewed; no unbounded loops or frame spikes from tile scripts.
- [ ] Asset manifest has source/rights/import status for every shipped asset.
- [ ] No Alpha-critical TODO remains.
- [ ] Every mandatory test is PASS with test evidence attached to the handoff report.
