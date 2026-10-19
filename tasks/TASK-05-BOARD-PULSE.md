# TASK-05 - Board Pulse Geometry, Scheduler, and Client Visualizer

## Preconditions
TASK-01 and TASK-02 accepted; TASK-04 simulation exposes the needed root/tile state.

## Goal
Implement deterministic timed hazard events using one authoritative payload per cycle and the three approved patterns.

## Files
- `src/shared/Modules/PatternDefinitions.luau`
- `src/server/Core/PulseService.luau`
- `src/client/Visualizers/PulseClientVisualizer.luau`
- unit tests for geometry and schedule

## Requirements
1. Cycle times are exactly: Opening 14+3.5+7+3.5=28s; MidGame 10+2.5+6+2.5=21s; SuddenDeath 6+2+5+2=15s.
2. Use one cycle payload with Pattern, Phase, EventId, WarningAt, ActivationAt, EndAt, ResetEndAt, and deterministic Meta, sent reliably. A snapshot path supports late listeners.
3. Server sets/clears gameplay state from synchronized times. Clients calculate remaining time using `Workspace:GetServerTimeNow()` and only render presentation. No client decides activation.
4. Implement formulas and phase-specific dimensions from Master Plan Section 7, including diagonal Ice segment bounds, cardinal-only Boost Runway and magnetic radius.
5. Every pattern excludes destroyed/pending cells and remains <= `floor(liveCellCount*0.35)`. Do not truncate arbitrarily; use specified smaller geometry.
6. Use a server-seeded Random instance; avoid consecutive identical pattern/orientation where an alternative exists.
7. Warning shows floor projection/chevrons and short text/audio; active and reset transitions restore original appearance exactly.
8. Maintain tween registry per client, cancel an existing tween before starting another. Do not put Tween objects in Attributes.
9. Cancel/reset hazard before ring collapse and on cleanup.

## Tests
- exact phase-cycle arithmetic and timestamp order
- every phase/pattern/angle tile count and connectivity tests
- no destroyed cells returned
- stable ordering for deterministic payloads
- Boost same direction for every tile; one trigger per sphere per event
- clients joining mid-warning/active receive correct visual snapshot
- three consecutive cycles leave no active tweens or stale state

## Handoff
Attach pattern screenshots for each angle/phase and test table with live count, selected count, cap, and pass status.
