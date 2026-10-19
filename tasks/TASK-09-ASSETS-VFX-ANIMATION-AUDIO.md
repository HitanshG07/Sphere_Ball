# TASK-09 - 3D Assets, VFX, Animation, Audio, and Visual Polish

## Preconditions
Mechanics and UI work end-to-end. Functional greybox assets are already in place.

## Goal
Upgrade visuals without changing physics, network authority, queue, timing, or gameplay contracts.

## Files
- `assets/models/`, `assets/textures/`, `assets/audio/`, `assets/animations/`
- `assets/asset-manifest.json`
- `src/client/Visualizers/*`
- no gameplay-authority files unless owner approves a narrowly scoped interface change

## Agent pipeline
1. Check whether Blender/Python export and Roblox asset import are available. If not, use procedural Roblox primitives and document the reason; do not block a functional Alpha on unavailable modelling software.
2. Keep source for generated mesh assets (`.blend` and deterministic export script) plus exported files and import instructions.
3. Do not use unverified/free-model assets or unverified `SoundId`s. Every shipped asset must list source/ownership/permission status.
4. Preserve collider dimensions and non-collision of visual mesh. Assets may not change mass, hitbox, speed, cooldown or ability values.
5. Keep visual shell under 5,000 triangles and main texture <=1024x1024 as targets; mobile fallback should use fewer particles and simpler materials.
6. Implement hazard-specific warning/active/reset VFX from Master Plan Section 11.5 and audio from Section 11.6.
7. Make every tween, Trail, Beam, ParticleEmitter and loop bounded and cleaned at event end/round cleanup.
8. Avoid large full-screen flashes, forced camera roll, long hit-stop, and persistent particles that obscure edge/collapse warnings.

## Required assets
- Four distinct chassis shell silhouettes (Rammer, Trickster, Magnetar, Bulwark)
- Four sphere skin looks (Default, Neon, Gold, Void; locked/unowned items can be previewed with lock state)
- Three core icons/colors (Cryo/Magnetic/Kinetic)
- Hub portal, customize kiosk, shop stand, mode board, leaderboard, queue pad/ring
- Ice, Magnet and Boost overlays/icons
- Light/heavy impact VFX, boost trail, core ability VFX, ring-collapse warning/sink animation
- Short warning, activation, collision and collapse audio if verified; otherwise keep pending placeholder

## Tests
- all asset names match manifest and code references
- shell dimensions never exceed root collider envelope
- VFX clears on Reset/Results/Cleanup and does not leak connections
- low-quality/mobile path reduces effects gracefully
- asset source/permission status complete
- missing optional asset uses a controlled placeholder and logs in development

## Handoff
Include rendered captures, asset manifest, triangle/texture budgets if measurable, import instructions and list of ASSET_PENDING items. No unverified item can be included in release build.
