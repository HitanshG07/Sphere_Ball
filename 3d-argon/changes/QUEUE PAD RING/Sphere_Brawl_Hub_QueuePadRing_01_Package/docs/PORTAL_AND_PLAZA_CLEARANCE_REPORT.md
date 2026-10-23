# Portal & Plaza Spatial Integration and Clearance Report — `SM_Hub_QueuePadRing_01`

**Asset ID:** `SM_Hub_QueuePadRing_01`  
**Target World Placement:** `(0, 150, -300)` (Reference Top Walking Surface `World Y = 150.0000`)  
**Inspected Reference Assets:**
1. **`SM_Hub_QueuePortalArch_01`** (`QueuePortalArch_Prototype.obj` / `generate_queue_portal_blender.py` — `3,168 triangles`, `9,504 vertices`)
2. **`SM_Hub_PlazaPlatform_01`** (`SM_Hub_PlazaPlatform_01.obj` / `generate_hub_plaza_platform_blender.py` — `2,688 triangles`, `8,064 vertices`)

---

## 1. Executive Summary of Spatial Compatibility

Programmatic vertex-level inspection of the approved `SM_Hub_QueuePortalArch_01` and `SM_Hub_PlazaPlatform_01` meshes confirms **zero geometric conflict** at the nominal `14.0-stud` outer queue boundary:

- **`SM_Hub_QueuePortalArch_01` Floor Footprint:** All floor-level elements of the Queue Portal Arch (`Local Y <= 6.0 studs`) lie strictly within **`R_xz in [15.0187, 20.4658] studs`**, leaving 100% of the `R <= 14.0000 stud` circle completely open.
- **`SM_Hub_PlazaPlatform_01` Top Deck:** The Plaza Platform top deck (`Local Y = 0.0000`) is a flat, unadorned `MAT_DarkNeutral` plane across `R in [0.0000, 14.0000] studs` and `R in [14.0000, 21.2000] studs` (with 4 flush `Y = 0.0000` diagonal `MAT_AltNeutral` inlays in `R = 14.00..21.20`), and its recessed inner framing ring sits at **`R in [21.2000, 23.0000] studs`**.
- **Resulting Concentric Hierarchy:** `SM_Hub_QueuePadRing_01` occupies the exact annular band **`R in [12.8000, 14.0000] studs`** (`Outer Diameter = 28.0000 studs`, `Inner Diameter = 25.6000 studs`, `Band Width = 1.2000 studs`), providing a **`+1.0500-stud` minimum horizontal clearance** inside the innermost portal pylon bracket (`|X| = 15.0500 studs`), a **`+1.2000-stud` radial clearance** inside the portal flank glow rims (`R = 15.2000 studs`), and a **`+7.2000-stud` radial clearance** inside the plaza's inner framing ring (`R = 21.2000 studs`).

---

## 2. Measured Footprint Breakdown of Existing Reference Assets

### A. Existing Queue Portal Arch (`SM_Hub_QueuePortalArch_01`)

| Portal Sub-Component (`QueuePortalArch_Prototype.obj`) | Material Slot | Local Elevation `Y` (Studs) | Radial Distance `R_xz` from `(0,0,0)` (Studs) | Horizontal `X / Z` Extents (Studs) | Radial Clearance to New Ring (`R_outer = 14.0000`) |
|---|---|---|---|---|---|
| `Portal_FloorGlowRim_L / R` | `EMI_Cyan` | `0.0000 .. 0.3000` | `15.2000 .. 15.6000` | `|X| in [8.9343, 15.6000]`, `Z in [-12.6207, +12.6207]` | **`+1.2000 studs` clear** |
| `Portal_FloorCurb_L / R` | `MAT_DarkNeutral` | `0.0000 .. 0.2800` | `15.6000 .. 17.2000` | `|X| in [9.1694, 17.2000]`, `Z in [-13.9151, +13.9151]` | **`+1.6000 studs` clear** |
| `Portal_TieCleat_L / R` & `TieTrim` | `MAT_AltNeutral` / `LightTrim` | `0.0000 .. 0.5200` | `15.7124 .. 17.1113` | `|X| in [11.6999, 13.5729]`, `|Z| in [9.75, 11.3902]` | **`+1.7124 studs` clear** |
| `Portal_PylonBracketF/B_L/R` | `MAT_LightTrim` | `0.6000 .. 4.4000` | `15.1281 .. 15.7000` | `|X| in [15.0500, 15.5500]`, `|Z| in [1.4750, 2.2250]` | **`+1.1281 studs` radial / `+1.0500 studs` on X** |
| `Portal_PylonBase_L / R` | `MAT_DarkNeutral` | `0.0000 .. 5.0000` | `15.3791 .. 19.1436` | `|X| in [15.2000, 19.0000]`, `Z in [-2.6000, +2.6000]` | **`+1.3791 studs` radial / `+1.2000 studs` on X** |
| `Portal_PylonButtress_L / R` | `MAT_AltNeutral` | `0.0000 .. 4.2000` | `18.8714 .. 20.4658` | `|X| in [18.8000, 20.4000]`, `Z in [-1.8000, +1.8000]` | **`+4.8714 studs` clear** |
| `Portal_ArchInnerConduit` & `ArchCore` | `EMI_Cyan` / `DarkNeutral` | `6.0000 .. 24.0500` | Overhead arch (`R_in = 15.00`) | Clear span `X in [-15.0000, +15.0000]`, crown `Y = 20.93` | **`+5.9200 studs` vertical overhead clearance** |

### B. Existing Plaza Platform (`SM_Hub_PlazaPlatform_01`)

| Plaza Platform Zone (`SM_Hub_PlazaPlatform_01.obj`) | Material Slot | Local Elevation `Y` (Studs) | Radial Span `R_xz` (Studs) | Relationship to `SM_Hub_QueuePadRing_01` |
|---|---|---|---|---|
| **Central Queue Pad Deck** (`GEO_PlazaPlatform_Deck`) | `MAT_DarkNeutral` | `0.0000` (Flat) | `0.0000 .. 14.0000` (`32` sectors) | Provides the flat walking surface inside `R < 12.8000` and beneath `R in [12.8000, 14.0000]`; **reused, never duplicated**. |
| **Portal Pylon Apron** (`Deck` + `DeckInlays`) | `MAT_DarkNeutral` / `AltNeutral` | `0.0000` (Flat) | `14.0000 .. 21.2000` (`32` sectors) | Flat apron outside `R = 14.0000` supporting the Queue Portal Arch pylons and flank curbs. |
| **Inner Plaza Framing Ring** (`Trim` + `CyanAccents`) | `MAT_LightTrim` / `EMI_Cyan` | `-0.0600 .. 0.0000` | `21.2000 .. 23.0000` (`32` sectors) | Outer architectural framing ring (`+7.2000 studs` outside `SM_Hub_QueuePadRing_01`). |

---

## 3. Coplanar Z-Fighting Prevention & Walkability Verification

1. **Non-Coplanar Elevation Offset (`Local Y_min = +0.0040 studs`):**
   - `SM_Hub_PlazaPlatform_01` has its top walking deck at exact `Local Y = 0.0000` (`World Y = 150.0000`).
   - Every vertex of `SM_Hub_QueuePadRing_01` is authored at `Local Y >= +0.0040 studs` (`World Y >= 150.0040`), with `0` vertices at `Y <= 0.0000`. This `4 mm` (`0.0040-stud`) vertical separation eliminates coplanar polygon overlap and prevents Z-fighting flicker at all camera distances.
2. **Restrained Low-Profile Walkable Cross-Section (`Local Y_max = +0.0800 studs`):**
   - Standard boundary sectors rise via `32.6°` chamfer skirts to `Y = +0.0680 studs` (`MAT_DarkNeutral` collar) and `Y = +0.0800 studs` (`MAT_LightTrim` bezel crest), framing a recessed `EMI_Cyan` conduit at `Y = +0.0360 studs`.
   - Along the 4 cardinal approach axes (`-Z` from Main Spawn `(0, 150, -334)`, `+Z`, `-X` from Customize Kiosk, and `+X` from Shop Stand), the ring transitions into lower **`0.0440-stud` walk-through threshold ramps**.
   - Furthermore, all 4 child `MeshPart`s of `SM_Hub_QueuePadRing_01` are configured with `CanCollide = false`, `CanTouch = false`, and `CanQuery = false`, guaranteeing zero physical snagging for R15 avatars or rolling spheres.
3. **Deliberately Reused Geometry (Zero Duplication):**
   - **Central Standing Deck (`R < 12.8000 studs`):** Reuses `GEO_PlazaPlatform_Deck` from `SM_Hub_PlazaPlatform_01` (`0` central disc faces in `SM_Hub_QueuePadRing_01`).
   - **Portal Arch & Flank Curbs (`R >= 15.0500 studs`):** Reuses `SM_Hub_QueuePortalArch_01` without recreating any arch, pylon, or outer flank curb.
   - **Outer Plaza Framing Ring (`R = 21.20..23.00 studs`):** Reuses `SM_Hub_PlazaPlatform_01` without duplicating outer rings.
