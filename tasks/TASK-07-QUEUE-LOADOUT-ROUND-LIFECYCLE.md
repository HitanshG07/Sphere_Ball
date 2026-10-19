# TASK-07 - Queue, Loadout, RoundManager, Results, and Cleanup

## Preconditions
TASK-01 through TASK-06 accepted; lobby pad exists and GridService resets reliably.

## Goal
Connect the full player journey from physical lobby queue to the results screen and return.

## Files
- `src/server/Core/QueueService.luau`
- `src/server/Core/LoadoutService.luau`
- `src/server/Core/RoundManager.luau`
- `src/server/Core/ResultsService.luau`
- `src/server/Core/CleanupService.luau`
- `src/server/Core/PlayerLifecycle.luau`
- integration tests

## Queue semantics (LOCKED)
- Physical pad dwell one full continuous second joins `Source=Portal`.
- Portal-sourced entry removed after 0.5s outside pad.
- Quick Queue entry persists until leave/cancel, assignment or disconnect.
- Both sources share one dictionary keyed by UserId. Concurrent requests are idempotent.
- 6 players -> 8-second countdown immediately; 4-5 players -> wait up to 25 seconds then 10-second partial countdown; fewer than 4 never starts.
- At T-5 loadouts lock; queue drop below 4 cancels countdown.
- Alpha permits only FreeForAll mode and one live arena match per server.

## RoundManager
Use exact states from Master Plan Section 4.2. Transition only from the one master manager. Opening=two 28s pulses, collapse D4, MidGame=two 21s pulses, collapse D3, SuddenDeath=15s pulse loops to survivor or 150s hard timeout. Cancel/reset hazard before collapse. Results lasts 8 seconds, followed by cleanup.

## Avatar and sphere lifecycle
Save every property changed on R15 avatar and restore original values exactly. Move avatar into holding pod with movement disabled during play; spawn separate sphere for active player. On cleanup destroy sphere/visuals, return avatar to hub, restore controls and clear state. Do not respawn/replace the whole Character to swap forms.

## Results
Compute placements, KOs and survival time on server. Hard timeout tiebreak: placement score, then valid KOs, then survival time; if still equal, shared tie. Do not display coins/XP until real reward logic is implemented.

## Tests
- every queue rule in Master Plan Section 5
- invalid loadout ID and locked item rejected
- match starts/aborts correctly under disconnect and queue changes
- each phase transitions at exact times
- 3 consecutive end-to-end rounds leave no residual state
- hidden avatars return with original transparency, decals, movement and accessories
