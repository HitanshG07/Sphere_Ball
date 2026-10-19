# TASK-03 - Kinetic Hub and World Stations

## Preconditions
TASK-01 accepted; grid coordinate conventions frozen. TASK-02 can run in parallel only if the environment agent does not edit GridService files.

## Goal
Build the approved lobby layout as a usable Roblox scene, not just concept art.

## Files
- `src/server/Core/LobbyService.luau`
- `src/server/Core/PlayerLifecycle.luau` (or approved avatar lifecycle module)
- `src/shared/Config/GameConfig.luau` only through orchestrator-controlled change
- `assets/asset-manifest.json`
- `assets/models/` or procedural environment builder

## Exact layout
Use Master Plan Section 2.4. Top walking surface is centered at Y=150. Hub center `(0,150,-300)`. Main spawn position `(0,150,-334)` must use `CFrame.lookAt(Vector3.new(0,150,-334), Vector3.new(0,150,-300))` so its LookVector faces +Z toward the central queue portal. Physical Queue Portal at `(0,150,-300)` radius 14. Customize kiosk at `(-43,150,-300)`, Shop at `(43,150,-300)`, Mode board `(35,150,-326)`, Leaderboard `(35,150,-274)`.

## Requirements
1. Platform outer diameter 140 studs; platform top Y=150. Keep queue pad physically open and visible from spawn.
2. The queue pad has a ground ring/zone trigger and decorative arch. The arch is not a collision obstacle. The pad zone and UI use the same server queue state.
3. Build stations with Roblox primitives first; optional custom meshes are a later visual pass. Do not require external asset IDs for a functional scene.
4. All station interactions use proximity/range validation or physical region tracking, not client-sent arbitrary object references.
5. Mode board has only Free-for-All active. Duel/Team Clash/King Tile are marked `COMING SOON` and disabled.
6. Leaderboard may show session-only values in Alpha; no fabricated persistent stats.
7. Set correct collision groups so lobby players and arena objects cannot disturb each other.
8. Provide safe spawn points, navigation and a clean route from spawn to queue, customization, and stations.

## Tests
- spawn line-of-sight to queue pad clear
- main spawn LookVector horizontal dot direction-to-portal is > 0.99
- player can walk across lobby without snagging/falling
- station interactions respond only within expected range
- no shop/mode dead buttons
- player character reset/lifecycle test passes

## Handoff
Provide Explorer tree, geometry sizes/coordinates, visual QA screenshots, and list of assets created/imported/pending.
