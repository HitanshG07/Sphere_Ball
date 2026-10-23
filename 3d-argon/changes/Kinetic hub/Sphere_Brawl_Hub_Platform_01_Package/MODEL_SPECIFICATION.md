# Model Specification — `SM_Hub_PlazaPlatform_01`

## 1. Asset Identity & Coordinate Contract

| Property | Locked / Proposed Value | Specification Source |
|---|---|---|
| **Asset ID** | `SM_Hub_PlazaPlatform_01` | Locked (`TASK-03`, Prompt §3) |
| **Outer Platform Diameter** | `140.0000 studs` (`R_outer = 70.0000 studs`) | Locked (`TASK-03`, `MASTER_IMPLEMENTATION_PLAN.md` §11.3, `GameConfig.Lobby.PlazaDiameter`) |
| **Maximum XZ Footprint** | `140.0000 × 140.0000 studs` (`X in [-70.0000, +70.0000]`, `Z in [-70.0000, +70.0000]`) | Locked (Prompt §3.1) |
| **World Center of Walking Surface** | `(0, 150, -300)` | Locked (`TASK-03`, `MASTER_IMPLEMENTATION_PLAN.md` §2.4, `GameConfig.Lobby.HubCenter`) |
| **Top Walking-Surface Elevation** | `Local Y = 0.0000 studs` -> `World Y = 150.0000 studs` | Locked (`TASK-03`, `MASTER_IMPLEMENTATION_PLAN.md` §2.4) |
| **Local Origin / Pivot Convention** | `(0.0000, 0.0000, 0.0000)` at exact center of top walking surface | Locked / Verified (Prompt §3.1) |
| **Local Coordinate Orientation** | `+Y Up`, `+Z Forward`, `+X Right`, `1.0 Unit = 1.0 Roblox Stud` | Locked (`DESIGN_CONSTANTS.md`, Art Bible) |
| **Total Platform Thickness** | `12.0000 studs` (`Local Y in [-12.0000, 0.0000]` -> `World Y in [138.0000, 150.0000]`) | **Proposed Design Decision** (1:11.67 thickness-to-diameter ratio) |
| **Perimeter Radial Segmentation** | `32 segments` (`11.25°` per sector) with `8` primary buttress bays (`45°` interval) | **Proposed Design Decision** (Vertices at `k * 11.25°` align exactly with `±70.0000` on `+X/-X/+Z/-Z`) |
| **Measured Triangle Count** | `2,688 triangles` (Target: `<= 6,000 triangles`) | Measured (`SM_Hub_PlazaPlatform_01.obj` & `.glb`) |

## 2. Mathematical Verification of Pivot & World Placement

The model vertices satisfy:
- `X_min = -70.0000`, `X_max = +70.0000` -> `Center_X = 0.0000 studs`, `Width_X = 140.0000 studs`
- `Z_min = -70.0000`, `Z_max = +70.0000` -> `Center_Z = 0.0000 studs`, `Depth_Z = 140.0000 studs`
- `Y_min = -12.0000`, `Y_max = 0.0000` -> `Top_Surface_Y = 0.0000 studs`, `Height_Y = 12.0000 studs`

When the model's pivot `(0, 0, 0)` is placed at the locked Hub world coordinate `(0, 150, -300)`:
- `World_X = Local_X + 0.0` -> `[-70.0000, +70.0000]`
- `World_Y = Local_Y + 150.0` -> `[138.0000, 150.0000]` (Top walking surface is at **exact `World Y = 150.0000`**)
- `World_Z = Local_Z - 300.0` -> `[-370.0000, -230.0000]`

Note: If Roblox Studio computes an imported `Model`'s default bounding-box center at `Local Y = -6.0000` (`0.5 * (-12.0 + 0.0)`), setting `Model.WorldPivot = CFrame.new(0, 150, -300)` (or centering the root `Model` bounding box at `(0, 144, -300)`) places the `Local Y = 0.0000` walking deck at exact `World Y = 150.0000`. Both methods are documented in `ROBLOX_STUDIO_IMPORT_GUIDE.md`.

## 3. Structural Cross-Section & Radial Zones (Proposed Design Dimensions)

### A. Top Walking Deck (`Local Y = 0.0000`, `R = 0.00` to `65.80 studs`)
1. **Central Queue Pad Core & Outer Zone (`R = 0.00` to `14.00 studs`, `Y = 0.0000`):**
   - Continuous, flat `MAT_DarkNeutral` deck (`96 triangles`). Zero raised rings, bumps, or duplicated portal geometry.
2. **Portal Pylon & Approach Clearance Apron (`R = 14.00` to `21.20 studs`, `Y = 0.0000`):**
   - Completely flat at `Y = 0.0000` across the entire Queue Portal Arch footprint (`QueuePortalArch_Prototype.obj` floor elements span `R = 15.02..20.47 studs`). Uses `MAT_DarkNeutral` across all cardinal approaches and pylon foundations with 4 flush diagonal `MAT_AltNeutral` accent plates.
3. **Inner Plaza Framing Ring & Recessed Cyan Conduit (`R = 21.20` to `23.00 studs`, `Y in [-0.0600, 0.0000]`):**
   - Positioned `0.7342 studs` outside the outermost Queue Portal pylon buttress (`R = 20.4658 studs`).
   - Features inner and outer flush `MAT_LightTrim` bezels (`R = 21.20..21.55` and `22.65..23.00` at `Y = 0.0000`), `45°` `MAT_AltNeutral` bevel walls, and a shallow `0.06-stud` recessed `EMI_Cyan` energy conduit (`Y = -0.0600`) bridged at the 4 cardinal walkway axes (`+X, -X, +Z, -Z`) by `MAT_LightTrim` lock plates.
4. **Inner Promenade & Main Spawn Ring (`R = 23.00` to `36.20 studs`, `Y = 0.0000`):**
   - Supports the Main Spawn at `(0, 150, -334)` (`Local (0, 0, -34.0)`, `R = 34.0 studs`). Flat `Y = 0.0000` `MAT_DarkNeutral` deck with symmetric `MAT_AltNeutral` radial walkway inlays leading directly along `+Z` to the Queue Portal.
5. **Mid-Deck Precision Guide Ring (`R = 36.20` to `37.00 studs`, `Y = 0.0000`):**
   - Flush concentric transition ring (`MAT_AltNeutral`, `MAT_LightTrim` at buttress axes, and 8 restrained `EMI_Cyan` alignment markers).
6. **Peripheral Station Plaza Ring (`R = 37.00` to `52.50 studs`, `Y = 0.0000`):**
   - Provides a flat, unobstructed `Y = 0.0000` foundation for Customize `(-43, 150, -300)` (`R = 43.0`), Shop `(43, 150, -300)` (`R = 43.0`), Mode Selection Board `(35, 150, -326)` (`R = 43.60`), Leaderboard `(35, 150, -274)` (`R = 43.60`), and Optional Reward Display `(-38, 150, -326)` (`R = 46.04`).
7. **Outer Promenade Deck (`R = 52.50` to `63.20 studs`, `Y = 0.0000`):**
   - Broad `MAT_DarkNeutral` armored deck plates with 4 cardinal `MAT_AltNeutral` radial expansion plates.
8. **Outer Deck Curb Bezel & Recessed Perimeter Energy Trough (`R = 63.20` to `65.80 studs`, `Y in [-0.1800, 0.0000]`):**
   - Flush `MAT_LightTrim` curb collars (`R = 63.20..63.75` and `65.35..65.80` at `Y = 0.0000`) framing a `0.18-stud` recessed `EMI_Cyan` perimeter energy channel (`R = 63.95..65.15`, `Y = -0.1800`), bridged across the 8 buttress sectors by `MAT_LightTrim` structural clamps.

### B. Outer Structural Rim & Sidewall (`R = 65.80` to `70.0000 studs`, `Local Y = 0.0000` to `-6.2000`)
- **Upper Rim Crest (`R = 65.80..68.80`, `Y = 0.0000`):** Load-bearing perimeter deck (`MAT_DarkNeutral` with `MAT_AltNeutral` buttress caps).
- **Outer Upper `45°` Chamfer (`R = 68.80, Y = 0.0000` -> `R = 70.0000, Y = -1.2000`):** `1.20-stud` precision bevel (`MAT_DarkNeutral` main sectors, `MAT_LightTrim` buttress sectors) with 16 inset `MAT_LightTrim` mounting brackets (`R = 68.55..69.92`, `Y = -0.15..-3.55`).
- **Primary Vertical Sidewall (`R = 70.0000`, `Y = -1.2000` to `-3.4000`):** Defines the exact `140.0000-stud` outer diameter (`MAT_DarkNeutral`).
- **Recessed Sidewall Tech Band (`R = 69.2500`, `Y = -3.4000` to `-5.0000`):** Undercut channel housing 16 alternating `EMI_Cyan` status light bars, 8 `MAT_LightTrim` buttress armor plates, and 8 `MAT_AltNeutral` bay casings.
- **Lower Rim Cheek Bevel (`R = 69.85, Y = -5.0000` -> `R = 68.20, Y = -6.2000`):** `MAT_DarkNeutral` lower sidewall transition.

### C. Underside Structural Truss & Keel (`R = 68.20` to `0.0000 studs`, `Local Y = -6.2000` to `-12.0000`)
- **Outer Underside Soffit (`R = 68.20..61.00`, `Y = -6.20..-6.50`) & Stepped Mid-Hull Wall (`R = 61.00..56.00`, `Y = -6.50..-7.60`):** `MAT_DarkNeutral` and `MAT_AltNeutral` stepped upper hull underside.
- **Recessed Truss Bay Ceiling (`R = 56.00..38.00`, `Y = -7.60..-8.90`):** `MAT_DarkNeutral` recessed ceiling allowing the 8 radial box-girders to project downward in full 3D relief.
- **8 Radial Underside Box-Girders & Gussets (`R = 21.50..67.60`, `Y = -6.20..-11.92`):** 8 heavy `MAT_AltNeutral` beveled box-girders (`width = 3.10..4.20 studs`) with `MAT_LightTrim` outer soffit gusset brackets (`R = 60.50..67.60`).
- **Lower Hull Diagnostic Collar (`R = 38.00..34.50`, `Y = -8.90..-9.60`):** Alternating `MAT_LightTrim` collar plates and `EMI_Cyan` diagnostic vents.
- **Lower Keel Bevel (`R = 34.50..22.00`, `Y = -9.60..-12.00`) & Central Keel Plate (`R = 22.00..0.00`, `Y = -12.0000`):** Tapered `MAT_DarkNeutral` lower hull terminating in a flat `MAT_AltNeutral` / `MAT_DarkNeutral` octagonal keel cap at `Local Y = -12.0000`.

## 4. Named Component Hierarchy & Material Slot Mapping

| Child Component Name | Assigned Material Slot | Locked RGB & Hex | Roblox Target Material | Triangle Count |3D Surface Area Share | Top-View Projected Area Share |
|---|---|---|---|---:|---:|---:|
| `GEO_PlazaPlatform_Deck` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `480` | — | — |
| `GEO_PlazaPlatform_Rim` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `224` | — | — |
| `GEO_PlazaPlatform_Underside` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `224` | `63.31%` (Combined DarkNeutral) | `67.13%` |
| `GEO_PlazaPlatform_DeckInlays` | `MAT_AltNeutral` | `(42, 50, 70)` `#2A3246` | `Enum.Material.Metal` | `392` | — | — |
| `GEO_PlazaPlatform_Structure` | `MAT_AltNeutral` | `(42, 50, 70)` `#2A3246` | `Enum.Material.Metal` | `448` | `27.92%` (Combined AltNeutral) | `24.04%` |
| `GEO_PlazaPlatform_Trim` | `MAT_LightTrim` | `(170, 190, 215)` `#AABED7` | `Enum.Material.Metal` | `752` | `5.85%` | `5.78%` |
| `GEO_PlazaPlatform_CyanAccents` | `EMI_Cyan` | `(0, 195, 255)` `#00C3FF` | `Enum.Material.Neon` | `168` | `2.92%` | `3.04%` |
| **Total (`SM_Hub_PlazaPlatform_01`)** | **4 Locked Materials** | — | — | **`2,688`** | **`100.00%` (`38,224.24 sq. studs`)** | **`100.00%`** |
