# Model Specification — `SM_Hub_QueuePadRing_01`

## 1. Asset Identity & Authoritative Coordinate Contract

| Property | Locked / Verified Value | Specification Source |
|---|---|---|
| **Asset ID** | `SM_Hub_QueuePadRing_01` | Locked (`TASK-03`, `TASK-09`, Prompt §3) |
| **Asset Type** | Static decorative environment mesh (Hub Queue Pad boundary ring) | Locked (`TASK-03`, `MASTER_IMPLEMENTATION_PLAN.md` §11.3) |
| **Intended World Centre** | `(0, 150, -300)` | Locked (`TASK-03`, `MASTER_IMPLEMENTATION_PLAN.md` §2.4, `GameConfig.Lobby.QueuePortal`) |
| **Reference Top Walking Surface** | `Local Y = 0.0000 studs` -> `World Y = 150.0000 studs` | Locked (`TASK-03`, `MASTER_IMPLEMENTATION_PLAN.md` §2.4) |
| **Nominal Outer Queue Boundary Radius** | `14.0000 studs` (`Measured R_outer = 14.0000 studs`) | Locked (`TASK-03`, `GameConfig.Lobby.QueuePadRadius = 14`) |
| **Nominal Outer Diameter** | `28.0000 studs` (`Measured X/Z Span = 28.0000 × 28.0000 studs`) | Locked (`TASK-03`, Prompt §3) |
| **Inner Queue Boundary Radius** | `12.8000 studs` (`Inner Clear Diameter = 25.6000 studs`) | **Documented Design Choice** (`0` vertices inside `R < 12.8000 studs`) |
| **Radial Band Width** | `1.2000 studs` (`R in [12.8000, 14.0000] studs`) | **Documented Design Choice** (Restrained floor-integrated boundary ring) |
| **Vertical Bounds & Thickness** | `Local Y in [+0.0040, +0.0800] studs` (`0.0760-stud` structural thickness; `0.0800-stud` max height above deck) | **Documented Design Choice** (`+0.0040-stud` non-coplanar offset prevents z-fighting on `Y = 0.0000` deck) |
| **Radial Segmentation** | `32 segments` (`11.25°` per sector) + `16` radial clasps/divider ribs | **Documented Design Choice** (Matches `SM_Hub_PlazaPlatform_01` 32-sector topology 1:1) |
| **Local Origin / Pivot Convention** | `(0.0000, 0.0000, 0.0000)` at exact centre of the `Local Y = 0.0000` floor reference plane | Verified (`+Y Up`, `+Z Forward`, `+X Right`, `1.0 Unit = 1.0 Roblox Stud`) |
| **Measured Triangle Count** | `960 triangles` (`2,880 export vertices`) | Measured (`SM_Hub_QueuePadRing_01.obj` & `.glb`) |

---

## 2. Mathematical Verification of Pivot, Bounds & World Placement

The exported `SM_Hub_QueuePadRing_01.obj` and `SM_Hub_QueuePadRing_01.glb` vertices satisfy:
- `X_min = -14.0000`, `X_max = +14.0000` -> `Center_X = 0.0000 studs`, `Outer_Diameter_X = 28.0000 studs`
- `Z_min = -14.0000`, `Z_max = +14.0000` -> `Center_Z = 0.0000 studs`, `Outer_Diameter_Z = 28.0000 studs`
- `R_xz_min = 12.8000`, `R_xz_max = 14.0000` -> `Band_Width = 1.2000 studs`, `Inner_Clear_Diameter = 25.6000 studs`
- `Y_min = +0.0040`, `Y_max = +0.0800` -> `Structural_Thickness = 0.0760 studs`, `Max_Elevation_Above_Deck = 0.0800 studs`

When the model's floor-reference pivot `(0, 0, 0)` is placed at the locked Hub Queue Portal coordinate `(0, 150, -300)`:
- `World_X = Local_X + 0.0` -> `[-14.0000, +14.0000]`
- `World_Y = Local_Y + 150.0` -> `[150.0040, 150.0800]` (Sits `0.0040 studs` above the `World Y = 150.0000` plaza walking surface with zero coplanar flicker)
- `World_Z = Local_Z - 300.0` -> `[-314.0000, -286.0000]`

In Roblox Studio, an imported `Model`'s bounding-box center sits at `Local Y = +0.0420` (`0.5 * (0.0040 + 0.0800)`), which is `0.0040 studs` above `Local Y = 0.0000` plus half the `0.0760-stud` height (`0.0380 studs`). Setting `ring.PrimaryPart = nil`, calibrating `ring.WorldPivot = CFrame.new(bboxCFrame.Position - Vector3.new(0, bboxSize.Y / 2 + 0.004, 0))`, and calling `ring:PivotTo(CFrame.new(0, 150, -300))` places the asset at its exact intended world coordinates.

---

## 3. Radial & Sector Architecture

### A. Concentric Radial Profile (`R = 12.8000` to `14.0000 studs`, `Band Width = 1.2000 studs`)
1. **Inner Chamfer Skirt (`R = 12.8000 -> 12.9000`, `Y = +0.0040 -> +0.0680` [`+0.0440` at thresholds]):**
   - Low-profile `MAT_DarkNeutral` inner transition skirt rising cleanly from `R_inner = 12.8000 studs`.
2. **Inner Structural Collar Deck (`R = 12.9000 -> 13.0600`, `Y = +0.0680` [`+0.0440` at thresholds]):**
   - Flat `MAT_DarkNeutral` load-bearing collar band.
3. **Inner Precision Bezel (`R = 13.0600 -> 13.1800`, `Y = +0.0680 -> +0.0800`):**
   - Brushed `MAT_LightTrim` (`#AABED7`) metallic highlight ring framing the inner edge of the energy channel.
4. **Inner Channel Slope Wall (`R = 13.1800 -> 13.2600`, `Y = +0.0800 -> +0.0360`):**
   - Angled `MAT_AltNeutral` (`#2A3246`) bevel wall stepping down into the recessed conduit trough so the cyan glow sits in physical relief.
5. **Recessed Cyan Boundary Conduit (`R = 13.2600 -> 13.5400`, `Y = +0.0360`, `Width = 0.2800 studs`):**
   - Recessed `EMI_Cyan` (`#00C3FF`, `Enum.Material.Neon`) energy channel segmented by 16 radial clasps and narrowed to a `0.1200-stud` alignment diode (`R = 13.3400..13.4600`) across the 4 cardinal threshold gates.
6. **Outer Channel Slope Wall (`R = 13.5400 -> 13.6200`, `Y = +0.0360 -> +0.0800` [`+0.0740` at intercardinal locks]):**
   - Angled `MAT_AltNeutral` outer trough wall.
7. **Outer Precision Bezel / Intercardinal Lock Casing (`R = 13.6200 -> 13.7400`, `Y = +0.0800 -> +0.0680`):**
   - `MAT_LightTrim` outer metallic bezel on standard boundary sectors, alternating with `MAT_AltNeutral` structural lock casings at the 4 intercardinal octants (`45°, 135°, 225°, 315°`).
8. **Outer Structural Collar Deck (`R = 13.7400 -> 13.9000`, `Y = +0.0680` [`+0.0440` at thresholds]):**
   - Flat `MAT_DarkNeutral` outer collar deck.
9. **Outer Chamfer Skirt (`R = 13.9000 -> 14.0000`, `Y = +0.0680 -> +0.0040`):**
   - Outer `MAT_DarkNeutral` bevel terminating at the exact `R_outer = 14.0000 stud` (`28.0000-stud` diameter) nominal queue boundary.
10. **Bottom Closure Face (`R = 14.0000 -> 12.8000`, `Y = +0.0040`, `-Y` normal):**
    - Watertight lower closure plane keeping all geometry strictly above `Y = 0.0000`.

### B. 32-Sector Circumferential Layout & 16 Radial Clasps
- **8 Cardinal Walk-Through Threshold Sectors (`{31, 0}` at `+X`, `{7, 8}` at `+Z`, `{15, 16}` at `-X`, `{23, 24}` at `-Z`):**
  - Each cardinal approach features a `22.5°` (`~5.26-stud` wide) lower threshold bridge (`Y_top = +0.0440 studs`) with `MAT_LightTrim` threshold plates and a recessed `0.12-stud` `EMI_Cyan` alignment strip.
- **8 Intercardinal Structural Lock Sectors (`{3, 4}`, `{11, 12}`, `{19, 20}`, `{27, 28}` at `45°, 135°, 225°, 315°`):**
  - Feature `MAT_AltNeutral` outer lock casings that align with the 4 diagonal inlay sectors of `SM_Hub_PlazaPlatform_01`.
- **16 Radial Clasps / Divider Ribs (`18 triangles` each):**
  - `8` `MAT_LightTrim` threshold gate clasps (`R = 12.92..13.88`, `Y_top = +0.0780`) framing the 4 cardinal entry gates, plus `8` `MAT_AltNeutral` intermediate segmentation bridges (`R = 13.12..13.68`, `Y_top = +0.0740`) dividing the recessed cyan channel into 12 crisp arc segments.

---

## 4. Per-Component Hierarchy & Locked Material Slot Mapping

The table below is derived directly from `meshes/SM_Hub_QueuePadRing_01.obj` and `meshes/SM_Hub_QueuePadRing_01.glb` (`100%` parity across OBJ, GLB, `MANIFEST.json`, and `VALIDATION_REPORT.md`):

| Child Component Name (`o` / GLB Node) | Assigned Material Slot | Locked RGB & Hex | Roblox Target Material | Triangles | Export Vertices | 3D Surface Area (`sq. studs` / `%`) | Top-Projected Area (`sq. studs` / `%`) |
|---|---|---|---|---:|---:|---:|---:|
| `GEO_QueuePadRing_BaseCollar` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `320` | `960` | `146.58` (`69.78%`) | `43.50` (`41.93%`) |
| `GEO_QueuePadRing_ChannelInlay` | `MAT_AltNeutral` | `(42, 50, 70)` `#2A3246` | `Enum.Material.Metal` | `320` | `960` | `24.08` (`11.46%`) | `22.02` (`21.22%`) |
| `GEO_QueuePadRing_TrimBezels` | `MAT_LightTrim` | `(170, 190, 215)` `#AABED7` | `Enum.Material.Metal` | `256` | `768` | `19.32` (`9.20%`) | `18.15` (`17.49%`) |
| `GEO_QueuePadRing_CyanConduit` | `EMI_Cyan` | `(0, 195, 255)` `#00C3FF` | `Enum.Material.Neon` | `64` | `192` | `20.08` (`9.56%`) | `20.08` (`19.35%`) |
| **Total (`SM_Hub_QueuePadRing_01`)** | **4 Locked Materials** | — | — | **`960`** | **`2,880`** | **`210.07` (`100.00%`)** | **`103.74` (`100.00%`)** |
