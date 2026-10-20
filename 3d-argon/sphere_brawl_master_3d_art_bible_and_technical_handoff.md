# Sphere Brawl: Rolling Rampage — Master 3D Art Direction, Visual Design Bible & Asset Production Handoff

**Project Repository Grounding:** `HitanshG07/Sphere_Ball` (`alpha` branch) | **Unit Scale:** `1.0 Unit = 1.0 Roblox Stud`

## Stage 1 — Source Specification Audit & Real Output Capabilities

### 1. Confirmed Browser/VM Output Capabilities
In this environment, I can genuinely produce and have delivered:
- **Actual Downloadable 3D Prototype Mesh Files (`.obj`):** Complete, multi-material 3D hard-surface meshes exported at exact 1:1 Roblox stud scale (`QueuePortalArch_Prototype.obj` at `3,552 triangles` and `Chassis_Rammer_Prototype.obj` at `2,940 triangles`), ready for direct import into Roblox Studio or Blender.
- **Deterministic Blender 3.6+/4.x Python Generation Scripts (`.py`):** Full parametric `bpy` / `bmesh` source scripts (`generate_queue_portal_blender.py` and `generate_rammer_chassis_blender.py`) that build the procedural hard-surface bevels, boolean cuts, and Principled BSDF materials from scratch and export `.glb` and `.fbx`.
- **Cohesive Studio Concept & Orthographic Turnaround Sheets:** High-resolution visual presentation sheets covering all four chassis silhouettes, four skins, three elemental cores, the Kinetic Hub station family, and all six arena tile/hazard states.
- **Honest Limitation Note:** Because the headless container does not run a live Roblox Studio `.rbxl` binary serializer, I have not claimed that assets are already imported into a `.rbxl` place file; instead, I have provided the actual `.obj` 3D geometry files, runnable Blender `.py` generators, and step-by-step Studio import instructions.

### 2. Source Specification Verification & Resolved Engineering Contracts
All six project sources were inspected prior to designing any asset:
- [MASTER\_IMPLEMENTATION\_PLAN.md](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FHitanshG07%2FSphere_Ball%2Fblob%2Falpha%2FMASTER_IMPLEMENTATION_PLAN.md) — Verified 4–6 player Free-for-All loop, 9x9 arena grid, 6 deterministic spawn coordinates, and 3-phase Board Pulse collapse schedule.
- [TASK-09-ASSETS-VFX-ANIMATION-AUDIO.md](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FHitanshG07%2FSphere_Ball%2Fblob%2Falpha%2Ftasks%2FTASK-09-ASSETS-VFX-ANIMATION-AUDIO.md) — Verified `< 5,000 triangle` budget per sphere shell, `<= 1024x1024` texture cap, 4 chassis (`Rammer`, `Trickster`, `Magnetar`, `Bulwark`), 4 skins (`Default`, `Neon`, `Gold`, `Void`), 2 trails (`CoreStreak`, `CyanStreak`), and 2 impact effects (`StandardSpark`, `CoreBurst`).
- [TASK-03-KINETIC-HUB-ENVIRONMENT.md](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FHitanshG07%2FSphere_Ball%2Fblob%2Falpha%2Ftasks%2FTASK-03-KINETIC-HUB-ENVIRONMENT.md) — Verified Hub center `(0, 150, -300)`, `140-stud` outer platform diameter, Main Spawn `(0, 150, -334)` looking `+Z` toward Queue Portal `(0, 150, -300)` (`Radius = 14.0 studs`), and locked station coordinates.
- [DESIGN\_CONSTANTS.md](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FHitanshG07%2FSphere_Ball%2Fblob%2Falpha%2Fspecs%2FDESIGN_CONSTANTS.md) — Verified physical sphere diameter `6.0 studs` (`Collider Radius = 3.000 studs`), tile pitch `12.0 studs`, collision tile `(12, 2, 12)`, visual tile `(11.8, 2, 11.8)`, top surface `Y = 51.0`, sphere spawn center `Y = 54.15`, and void threshold `Y < 15`.
- [DECISION\_LOG.md](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FHitanshG07%2FSphere_Ball%2Fblob%2Falpha%2FDECISION_LOG.md) — Verified Decisions D-001 through D-027, including cosmetic-only Alpha chassis fairness, Shift Burst Boost (`+12 studs/s`, `4.0s` cooldown), and server-authoritative knockback.
- [Sphere\_Brawl\_Rolling\_Rampage\_Final\_Concept.png](https://www.google.com/search?q=https%3A%2F%2Fraw.githubusercontent.com%2FHitanshG07%2FSphere_Ball%2Falpha%2Fassets%2Fconcept%2FSphere_Brawl_Rolling_Rampage_Final_Concept.png) — Note: Direct raw HTTP access to the `.png` URL is restricted, so the concept art was inspected via its rendered display inside [MASTER\_IMPLEMENTATION\_PLAN.md](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FHitanshG07%2FSphere_Ball%2Fblob%2Falpha%2FMASTER_IMPLEMENTATION_PLAN.md).

### 3. Unresolved Dependencies & Spec Conflict Report
1. **Hub Station & Arch Bounding-Box Envelopes (Proposed vs. Verified):** While [TASK-03-KINETIC-HUB-ENVIRONMENT.md](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FHitanshG07%2FSphere_Ball%2Fblob%2Falpha%2Ftasks%2FTASK-03-KINETIC-HUB-ENVIRONMENT.md) locks the exact world coordinates for the Queue Portal pad (`(0, 150, -300)`, `R = 14.0 studs`), Customize Kiosk (`(-43, 150, -300)`), Shop Kiosk (`(43, 150, -300)`), Mode Board (`(35, 150, -326)`), and Leaderboard (`(35, 150, -274)`), it does not specify exact height/width/depth bounding boxes for the decorative arch or kiosk structures. All proposed structural dimensions are explicitly marked as **Proposed** in Deliverable 4.
2. **Concept Image vs. Text Spec Station Placement:** The 2D concept image depicts Mode Select and Leaderboards as right-side UI HUD panels, whereas [TASK-03](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FHitanshG07%2FSphere_Ball%2Fblob%2Falpha%2Ftasks%2FTASK-03-KINETIC-HUB-ENVIRONMENT.md) specifies physical world stations at `(35, 150, -326)` and `(35, 150, -274)`. Following your priority rule, the text specification takes strict precedence, and physical 3D stations are designed for those exact world positions without moving any station.

## Deliverable 1 — Visual Design Bible

### 1. Proportions, Silhouette Hierarchy & Hard-Surface Bevel Conventions
- **70 / 20 / 10 Visual Read Hierarchy:**
  - **70% Primary Read:** Broad matte dark neutral armor shells (`RGB(32, 38, 54)`) that establish an unmistakable outer silhouette at 30–45 studs camera distance.
  - **20% Secondary Read:** Chamfered alternate neutral sub-plates (`RGB(42, 50, 70)`) and light metallic mechanical clasps/bumpers (`RGB(170, 190, 215)`).
  - **10% Tertiary Read:** Recessed glowing energy conduits (`Enum.Material.Neon`) and directional status diodes that communicate core identity and hazard phase without blooming over the silhouette.
- **Standardized Bevel & Seam Rules:**
  - **Player Sphere Shells (`6.0-stud` diameter):** Primary armor edge chamfers = `0.08–0.12 studs` at `45°`; panel seam gap width = `0.06 studs`; seam recess depth = `0.05 studs`; minimum detail feature width `>= 0.18 studs` to eliminate sub-pixel shimmering on mobile screens.
  - **Arena Grid Tiles (`11.8 x 2.0 x 11.8 studs` visual inside `12.0-stud` pitch):** Outer top edge chamfer = `0.25 studs` at `45°`; natural inter-tile gap = `0.20 studs` (100% consistent across all 81 cells).
  - **Hub Monument & Kiosk Props (`10–32 stud` scale):** Structural edge chamfers = `0.25–0.45 studs` at `45°` with stepped collar joints every `4.0 studs`.

### 2. Locked Colour Hierarchy & Material Rules

| Material Slot Name | Locked Palette Role | RGB Value | Hex Code | Roblox Material / PBR Target | Assigned System Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `MAT_DarkNeutral` | Dark Neutral Surface | `RGB(32, 38, 54)` | `#202636` | `Metal` / `SmoothPlastic` (Rough `0.42`, Metal `0.55`) | Inner containment sphere, dark checkerboard grid tiles, kiosk base hulls |
| `MAT_AltNeutral` | Alternate Neutral Surface | `RGB(42, 50, 70)` | `#2A3246` | `Metal` (Rough `0.35`, Metal `0.60`) | Layered cranial/equatorial armor plates, light grid tiles, arch ribs |
| `MAT_LightTrim` | Secondary Text / Trim | `RGB(170, 190, 215)` | `#AABED7` | `Metal` (Rough `0.28`, Metal `0.78`) | High-impact bumper faces, chamfered edge bezels, floor tie-down cleats |
| `MAT_PrimaryText` | Primary Text / Light Trim | `RGB(245, 248, 255)` | `#F5F8FF` | `SmoothPlastic` / Low-bloom `Neon` | Kiosk signage headers, directional decals, Void skin crisp rim highlights |
| `EMI_Cyan` | Primary Cyan / Energy | `RGB(0, 195, 255)` | `#00C3FF` | `Neon` (Recessed channel) | Default core glow, Queue Portal conduit, Neon skin circuits, safe tile diodes |
| `EMI_Ice` | Ice / Cryo | `RGB(0, 235, 255)` | `#00EBFF` | `Neon` + `Glass`/`Ice` (Rough `0.12`) | Cryo Anchor Brake core crystals, Ice Corridor active tile frost plating |
| `EMI_Magnetic` | Magnetic Purple | `RGB(165, 55, 255)` | `#A537FF` | `Neon` (Induction ring strips) | Magnetic Pulse Tether core coils, Magnetar rings, Magnetic Storm tile |
| `EMI_Kinetic` | Kinetic Boost Orange | `RGB(255, 125, 0)` | `#FF7D00` | `Neon` (Directional chevrons) | Kinetic Overdrive Dash core turbine, Boost Runway chevrons, rear exhaust |
| `EMI_Amber` | Warning Amber | `RGB(255, 170, 0)` | `#FFAA00` | `Neon` / Brushed Gold `Metal` | Pre-hazard Warning Phase tile borders (`3.5s`/`2.5s`/`2.0s`), Shop pods, Gold trim |
| `EMI_DangerRed` | Danger Red | `RGB(255, 40, 40)` | `#FF2828` | `Neon` (High-urgency pulse) | Ring D4 & Ring D3 collapse warning tiles, vertical perimeter laser curtains |

### 3. Shared Modular Components, Naming & Technical Budgets
- **Shared Component Library:**
  1. `COMP_Sphere_InnerHull_R248` (`R = 2.48 studs` dark containment sphere shared across all 4 chassis).
  2. `COMP_Hub_CornerBracket_01` (chamfered `MAT_LightTrim` mounting cleat reused across Queue Portal pylons and all 4 kiosks).
  3. `COMP_Hub_FloorCurb_4Stud` (modular perimeter trim strip with recessed cyan diode slot).
  4. `COMP_Arena_TileBevelFrame_118` (`11.8 x 2.0 x 11.8 stud` base frame shared across all tile states).
- **Technical Budgets:**
  - Player Sphere Visual Shell: `< 5,000 triangles` hard cap (`2,600–3,400 tris` target; `0` dynamic lights).
  - Hub Queue Portal Arch: `< 4,500 triangles` (`3,552 tris` measured).
  - Hub Station Kiosks: `< 2,500 triangles` each.
  - Arena Visual Tile: `< 250 triangles` per cell (`<= 20,250 triangles` total across all 81 cells).
  - Texture Maps: Maximum `1024 x 1024` resolution (`SurfaceAppearance` Color/Normal/Metalness/Roughness).

## Deliverable 2 — Cohesive 3D Asset Family Design Specification

### A. Player Sphere Chassis Family (Strict `R <= 3.000 Stud` Envelope)
Every chassis shell is strictly cosmetic (`CanCollide = false`, `CanTouch = false`, `CanQuery = false`, `Massless = true`) and welded to the authoritative `6.0-stud` diameter (`R = 3.000 studs`) root sphere collider at `(0, 0, 0)`:

| Chassis Name | Asset ID | Silhouette & Mechanical Form Language | Verified Shell Envelope |
| :--- | :--- | :--- | :--- |
| **1. Rammer** | `SM_Chassis_Rammer_01` | Heavy wedge-shaped frontal battering bumper (`+Z`), thick equatorial bash guards, 4 segmented cranial armor plates, hexagonal frontal core window. | `R_inner = 2.480 studs`<br>`R_max = 2.970 studs` (Verified `< 3.000`) |
| **2. Trickster** | `SM_Chassis_Trickster_01` | Lightweight swept-back aero fins with asymmetric diagonal split channels, exposing a continuous Y-shaped cyan velocity core channel. | `R_inner = 2.480 studs`<br>`R_max = 2.950 studs` (Verified `< 3.000`) |
| **3. Magnetar** | `SM_Chassis_Magnetar_01` | Recessed twin electromagnetic induction rings inclined at `+-35°` held by curved C-clamps over purple `EMI_Magnetic` field coils. | `R_inner = 2.480 studs`<br>`R_max = 2.960 studs` (Verified `< 3.000`) |
| **4. Bulwark** | `SM_Chassis_Bulwark_01` | Broad interlocking hexagonal tank plating with 8 heavy corner shock-absorber bolsters and deep recessed hex-grid core vents. | `R_inner = 2.480 studs`<br>`R_max = 2.970 studs` (Verified `< 3.000`) |

### B. Sphere Skins & Elemental Cores
- **Four Surface Skins (`MI_Skin_*` — Applied to any Chassis without changing geometry):**
  1. **Default (`MI_Skin_Default` — Unlocked):** Factory gunmetal slate (`#202636` / `#2A3246`) with brushed silver-blue trim (`#AABED7`) and 10% surface area `EMI_Cyan` (`#00C3FF`) core seams.
  2. **Neon (`MI_Skin_Neon` — Unlocked):** Deep anodized slate (`#181D2A`) with high-contrast glowing `EMI_Cyan` (`#00C3FF`) circuit channels inset along every armor plate perimeter.
  3. **Gold (`MI_Skin_Gold` — Locked Preview):** Prestige satin-brushed gold metallic armor (`Roughness = 0.22`, `Metalness = 0.92`) with warm `EMI_Amber` (`#FFAA00`) inner bevel glow and cyan core aperture.
  4. **Void (`MI_Skin_Void` — Locked Preview):** Ultra-matte obsidian black (`#0D0F17`, `Roughness = 0.68`) that absorbs ambient light, accented by razor-thin `#F5F8FF` white-violet rim highlights.
- **Three Elemental Cores (`VFX_Core_*` — Mounted at `ATT_Core_Center` inside `R = 1.65 stud` cavity):**
  1. **Kinetic Core (`#FF7D00`):** Twin orange turbine propulsion rings that spin up rapidly during **Kinetic Overdrive Dash** (`8.0s` cooldown, `+22 studs/s` velocity delta, `1.25x` outgoing knockback for `1.0s`).
  2. **Cryo Core (`#00EBFF`):** Six-point crystalline frost emitter that projects a downward hexagonal ice anchor glyph during **Cryo Anchor Brake** (`9.0s` cooldown, removes `85%` lateral drift, grants `2.5s` Ice/Magnetic hazard immunity, reduces incoming knockback to `1/1.5` for `2.0s`).
  3. **Magnetic Core (`#A537FF`):** Counter-rotating purple electromagnetic torus rings that fire a bounded purple plasma tether arc to the nearest sphere within `24 studs` during **Magnetic Pulse Tether** (`10.0s` cooldown, `+16 studs/s` pull toward caster).

### C. Effects-Ready Combat & Board-Pulse Visual Specification
- **Collision Impacts (`Pairwise Hit Cooldown = 0.35s`, `Min Closing Speed = 10 studs/s`):**
  - **Light Impact (`10–22 studs/s` closing speed — `StandardSpark`):** Short-lived (`0.25s`) radial burst of 12 crisp cyan/white geometric spark diamonds (`Radius <= 3.5 studs`) at the contact point.
  - **Heavy Impact (`> 22 studs/s` closing speed or `CoreBurst`):** Dual-layer shock ring (`0.40s` lifetime, `Radius = 6.0 studs`) tinted to the attacker's active Core colour (`#FF7D00`, `#00EBFF`, or `#A537FF`) plus directional knockback vector streaks.
- **Shift Burst Boost (`+12 studs/s` kick, `4.0s` cooldown, D-019) & Trails:**
  - Instant rear chevron shock-cone (`0.30s` fade) paired with a ribbon trail (`CoreStreak` in core color or `CyanStreak` in `#00C3FF`, `0.45s` lifetime, tapering from `3.2 studs` to `0.0 studs`).
- **Mobile Fallback Rule:** Under low graphics quality or high latency, particle counts scale down by 50% while retaining the deterministic 3D shock-ring mesh and ribbon trail so gameplay readability is never lost.

## Deliverable 3 & Deliverable 4 — Technical Handoff, File Inventory & Production Plan

### 1. Complete Deliverable File Inventory
- **`QueuePortalArch_Prototype.obj`** — **Actual 3D Model File** for Prototype 1 (`SM_Hub_QueuePortalArch_01`): `3,552 triangles`, `10,656 vertices`, bounding box `32.80 x 22.75 x 30.40 studs`, `24.70-stud` unobstructed inner arch span framing the `R = 14.0 stud` Queue Pad at `(0, 150, -300)`.
- **`Chassis_Rammer_Prototype.obj`** — **Actual 3D Model File** for Prototype 2 (`SM_Chassis_Rammer_01`): `2,940 triangles`, `8,820 vertices`, bounding box `5.93 x 5.76 x 5.83 studs`, maximum vertex radius `R_max = 2.970 studs` (verified strictly inside the `R = 3.000 stud` root sphere collider).
- **`generate_queue_portal_blender.py`** — **Deterministic Blender Python Generator** for `SM_Hub_QueuePortalArch_01` (builds full beveled geometry + Principled BSDF materials and exports `.glb` / `.fbx`).
- **`generate_rammer_chassis_blender.py`** — **Deterministic Blender Python Generator** for `SM_Chassis_Rammer_01` (builds spherical-patch armor plates + Principled BSDF materials and exports `.glb` / `.fbx`).

### 2. Master Per-Asset Technical Specification Table

| Asset Name | Deliverable Status | Dimensions (Studs) & Spec Status | Triangle Count | Materials Used | Moving Parts | Mesh Role & Collision Contract |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SM_Chassis_Rammer_01` | **Actual 3D `.obj` + `.py` Script** | `5.93 x 5.76 x 5.83` (`R_max = 2.970`, **Verified `<= 3.000`**) | `2,940 tris` (Measured) | `MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`, `EMI_Kinetic` | Rigid weld to root sphere | Visual-only shell (`CanCollide=false`, `Massless=true`) inside `6-stud` root sphere collider |
| `SM_Chassis_Trickster_01` | **Concept + Spec** | `5.90 x 5.80 x 5.90` (`R_max = 2.950`, **Verified `<= 3.000`**) | `~2,800 tris` (Target `< 5,000`) | `MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan` | Rigid weld to root sphere | Visual-only shell (`CanCollide=false`, `Massless=true`) |
| `SM_Chassis_Magnetar_01` | **Concept + Spec** | `5.92 x 5.84 x 5.92` (`R_max = 2.960`, **Verified `<= 3.000`**) | `~3,400 tris` (Target `< 5,000`) | `MAT_DarkNeutral`, `MAT_LightTrim`, `EMI_Cyan`, `EMI_Magnetic` | Optional client-only ring spin | Visual-only shell (`CanCollide=false`, `Massless=true`) |
| `SM_Chassis_Bulwark_01` | **Concept + Spec** | `5.94 x 5.88 x 5.94` (`R_max = 2.970`, **Verified `<= 3.000`**) | `~3,200 tris` (Target `< 5,000`) | `MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan` | Rigid weld to root sphere | Visual-only shell (`CanCollide=false`, `Massless=true`) |
| `SM_Hub_QueuePortalArch_01` | **Actual 3D `.obj` + `.py` Script** | Pad `R = 14.0` (**Verified** at `(0,150,-300)`); Arch `32.8 x 22.75 x 30.4` (**Proposed**) | `3,552 tris` (Measured) | `MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan` | Static arch + Crown `SurfaceGui` | Visual-only decorative arch (`CanCollide=false`, `CanTouch=false`, `CanQuery=false`); pad 100% open |
| `SM_Hub_CustomizeKiosk_01` | **Concept + Spec** | Pos `(-43, 150, -300)` (**Verified**); Box `10.0 x 9.5 x 8.0` (**Proposed**) | `~1,850 tris` (Target `< 3,000`) | `MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan` | Client rotating hologram sphere | Visual mesh + simple anchored box collider behind interaction zone |
| `SM_Hub_ShopKiosk_01` | **Concept + Spec** | Pos `(43, 150, -300)` (**Verified**); Box `10.0 x 11.0 x 8.0` (**Proposed**) | `~2,100 tris` (Target `< 3,000`) | `MAT_DarkNeutral`, `MAT_AltNeutral`, `EMI_Amber`, `EMI_Cyan` | 4 rotating showcase pods | Visual mesh + simple anchored box collider behind interaction zone |
| `SM_Hub_ModeBoard_01` | **Concept + Spec** | Pos `(35, 150, -326)` (**Verified**); Box `14.0 x 8.5 x 3.0` (**Proposed**) | `~1,100 tris` (Target `< 2,000`) | `MAT_DarkNeutral`, `MAT_LightTrim`, `EMI_Cyan` | Static terminal + `SurfaceGui` | Visual frame + simple anchored box collider |
| `SM_Hub_Leaderboard_01` | **Concept + Spec** | Pos `(35, 150, -274)` (**Verified**); Box `6.5 x 16.0 x 4.5` (**Proposed**) | `~1,250 tris` (Target `< 2,000`) | `MAT_DarkNeutral`, `MAT_AltNeutral`, `EMI_Cyan` | Static pylon + `SurfaceGui` | Visual pylon + simple anchored box collider |
| `SM_Arena_TileVisual_01` (x6 states) | **Concept + Spec** | Collider `12 x 2 x 12` (**Verified**); Visual `11.8 x 2 x 11.8` (**Verified**) | `~220 tris` / tile (`17,820` for 81) | `MAT_DarkNeutral`, `MAT_AltNeutral` + Hazard Neon overlays | Vertical sink tween on Ring Collapse | Visual mesh is `CanCollide=false`; hidden `12x2x12` Part is authoritative collider |

### 3. Stage 4 Prototype Review & Stage 5 Sequenced Production Plan
- **Stage 4 Review & Refinement Notes:**
  - **Validated Strengths:** Both Stage 3 prototypes import cleanly at 1:1 stud scale, stay well under polygon limits (`3,552 tris` for the Queue Portal Arch and `2,940 tris` for the Rammer Chassis vs. the `5,000-tri` cap), and respect all gameplay collision boundaries (`R_max = 2.970 studs` on the Rammer shell, leaving a `0.030-stud` safety buffer inside the `3.000-stud` collider; `24.70-stud` clear span on the Queue Portal Arch).
  - **Refinement for Next Iteration:** On `SM_Chassis_Rammer_01`, adding a single beveled transition ring (`~96 tris`) at latitude `phi = +-1.15 rad` between the polar cap and the four quadrant armor plates will further tighten the upper silhouette gap at close-up customization camera angles.
- **Stage 5 Next-Batch Production Order:**
  1. **Batch 2 — Modular Arena Tile & Hazard Overlays (`SM_Arena_TileVisual_01`):** Highest engineering dependency for `GridService` so all 81 cells have production visual meshes for Safe, Warning, Ice Corridor, Magnetic Storm, Boost Runway, and Ring D4/D3 Collapse states.
  2. **Batch 3 — Remaining Three Player Chassis (`Trickster`, `Magnetar`, `Bulwark`):** Built on the validated `R <= 2.970 stud` spherical mounting rig from Prototype 2.
  3. **Batch 4 — Skins & Elemental Core Emitter Meshes:** Author the four `1024x1024` `SurfaceAppearance` material sets and the three internal core meshes (`Kinetic`, `Cryo`, `Magnetic`).
  4. **Batch 5 — Hub Kiosk Stations & 6 Holding Pods:** Produce the four Hub stations at their locked coordinates and the six `10 x 1 x 10 stud` Holding Pod frames at `(2000 + 20*(i-1), 200, 2000)`.
