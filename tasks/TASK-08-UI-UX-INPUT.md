# TASK-08 - Lobby UI, Customization Modal, Arena HUD, Results, and Input

## Preconditions
Queue/Loadout/MatchState payloads are frozen; lobby and sphere lifecycle exist.

## Goal
Build every Alpha UI state and responsive input without dead controls or unapproved mechanics.

## Files
- `src/client/Controllers/LobbyUIController.luau`
- `src/client/Controllers/LoadoutUIController.luau`
- `src/client/Controllers/HUDController.luau`
- `src/client/Controllers/InputController.luau` (coordinate with TASK-04 owner)
- `src/client/Controllers/SpectatorController.luau`
- UI tests/screenshots

## UI modules
1. `HubNavigationGui`: Play/Quick Queue, Customize, Inventory (Coming Soon), Shop (Coming Soon), Quests (Coming Soon), Settings; queue status and Leave Queue.
2. `CustomizationModalGui`: category tabs, rotatable 3D ViewportFrame preview, item cards, equipped state, server confirmation and loadout-lock state. Tabs per D-021: Build = chassis, Skins = sphere skin (Gold/Void shown locked per D-020), Core, Trails (`None`, `CoreStreak`, `CyanStreak`), Effects (`StandardSpark`, `CoreBurst`); the Ball tab is disabled and labelled `COMING SOON`.
3. `ArenaCombatHUDGui`: next-hazard name/icon/timer, alive counter, ring collapse countdown, boost/brake/core ability buttons and cooldowns. The boost button is the D-019 Burst boost with its 4-second cooldown overlay.
4. `MatchResultsGui`: winner/tie, placement, KOs, survival time and Return to Hub.

## Behavior
- UI is presentation only; state comes from server payloads/replicated state.
- Play/Quick Queue and physical pad use same QueueService.
- If already queued, action label is `LEAVE QUEUE` and calls LeaveQueue.
- Loadout equips only on server confirmation. UI must never display an item as equipped if the server rejected it.
- At T-5, disable item selection and show why it is locked.
- Only Free-for-All can be entered; future modes are visibly disabled.
- Touch controls for boost, brake and ability; desktop keyboard and supported gamepad input route to the same local input state used by the approved simulation.
- Avoid hard-coded absolute pixel coordinates as the only layout; use scale, UISizeConstraint, safe areas, text limits, and responsive variants.
- Customization ViewportFrame uses its own camera/model clone with no physics and stops its render/tween loops when closed.
- Add reduced camera shake and audio toggles in Settings.

## Tests / visual checks
Capture all states in Master Plan Section 13.5. Test 1920x1080, 1280x720, 4:3 tablet and narrow phone sizes. Test touch buttons, cooldown states, queue count refresh, countdown cancellation, loadout rejection, and result return. No critical button may overlap ability controls or screen safe areas.

## Handoff
List tested viewports and controls, provide screenshots, and identify every button marked Coming Soon.
