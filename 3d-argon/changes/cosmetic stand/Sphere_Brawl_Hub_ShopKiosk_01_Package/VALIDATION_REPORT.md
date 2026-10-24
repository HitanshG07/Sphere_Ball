# Validation Report — `SM_Hub_ShopKiosk_01` (Argon Step 4 Phase 2 — Approved Arena Shop Bar Production)

**Validation Timestamp:** 2026-10-24  
**Canonical Asset ID:** `SM_Hub_ShopKiosk_01`  
**Descriptive Name:** Sphere Brawl Arena Shop Bar (`20.0 × 8.0 × 7.6 studs`)  
**Approved Concept Source:** `Sphere_Brawl_Shop_Bar_Concept_Reset_01.zip`  
**Validator Scripts:** `scripts/generate_hub_shop_kiosk_blender.py`, `scripts/validate_package.py`

## 1. Technical Validation Summary Table

Explicit statuses used: `PASS`, `FAIL`, `NOT RUN`, `REQUIRES OWNER REVIEW`, `ASSET_PENDING`.

### A. Approved Concept Fidelity & Geometry Validation

| Check | Requirement / Target | Measured Evidence | Status |
|---|---|---|---|
| **Approved Arena Shop Bar Silhouette Preserved** | Wide, horizontal, open-front arena-game shop (`20.0 × 8.0 × 7.6 studs`) with dominant continuous counter, 2 side wings, and lightweight suspended sign | Verified across all 10 production previews (`01`..`10`): continuous `15.10-stud` faceted bar counter (`GEO_ShopKiosk_CounterBody` + `GEO_ShopKiosk_Countertop`), swept left/right wings (`GEO_ShopKiosk_SideWings` + `GEO_ShopKiosk_WingShelves`) reaching `20.0000 studs` width, and open raked sign frame (`GEO_ShopKiosk_SignFrame`) holding separate blank `GEO_ShopKiosk_SignPanel`. Zero cupboard walls or 2×2 compartments. | **PASS** |
| **Four Non-Spherical Countertop Merchandise Displays** | 4 distinct non-spherical items in a single horizontal row along the countertop on compact display pads | Verified `GEO_ShopKiosk_DisplayPad_01..04` (`22 tris` each) and `GEO_ShopKiosk_DisplayItem_01..04` along `Z = +0.25` at `X = -5.10, -1.70, +1.70, +5.10`: `DisplayItem_01` (**Hexagonal Emblem Plate**, `80 tris`), `DisplayItem_02` (**Vertical Halo Ring**, `96 tris`), `DisplayItem_03` (**Segmented Chevron Trail Fins**, `74 tris`), and `DisplayItem_04` (**Geometric Starburst Burst Prism**, `44 tris`). Zero spheres used. | **PASS** |
| **Separate Blank UI-Ready Sign Panel** | Separate blank sign panel suitable for future Roblox UI; no baked-in text in production geometry | `GEO_ShopKiosk_SignPanel` (`16 tris`, `11.20 × 1.44 × 0.48 studs`) is exported as an independent mesh node with a flat, blank front face at `Local Z = +0.6800`. Verified in `previews/02_Preview_Front_Inward_Presentation.png` Panel C. | **PASS** |
| **Canonical Asset ID & Component Naming Consistency** | Root `SM_Hub_ShopKiosk_01` + `18` identical `GEO_ShopKiosk_*` components across OBJ, GLB, config, manifest & docs | Verified `SM_Hub_ShopKiosk_01` root + `18` identical `GEO_ShopKiosk_*` component names across `SM_Hub_ShopKiosk_01.obj`, `.mtl`, `.glb` (`19` nodes including root), `config/shop_kiosk_parameters.json`, `MANIFEST.json`, and `SM_Hub_ShopKiosk_01.manifest.json`. | **PASS** |
| **Actual Bounding Dimensions & Pivot Measured** | Approved target `20.0 (W) × 8.0 (D) × 7.6 (H) studs`; pivot `(0,0,0)` at footprint center with base at `Y = 0` | Measured from `7,272` export vertices: `X in [-10.0000, +10.0000]` (`20.0000 studs`), `Y in [0.0000, +7.6000]` (`7.6000 studs`), `Z in [-4.0000, +4.0000]` (`8.0000 studs`). `0.0000 stud` deviation from approved target. | **PASS** |
| **Topology, Normals & Z-Fighting Check** | `0` degenerate faces; `0` normal mismatches; `0` coplanar same-normal cross-component overlaps; complete underside at `Y = 0` | Measured across all `2,424` triangles: `degenerate_faces = 0` (`min_area = 0.000215 sq. studs`), `normal_mismatches = 0`, `coplanar_cross_component_overlaps = 0`, sealed underside at `Y = 0.0000` (`vn = (0, -1, 0)`). | **PASS** |
| **Triangle Budget Measured from Export** | Below `3,000` triangles | Measured **`2,424 triangles`** (`7,272 vertices`) in both `.obj` and `.glb` (**`576` triangles / `19.20%` below the `3,000` cap**). | **PASS** |
| **Palette & Texture Budgets Respected** | 5 locked materials; texture `<= 1024×1024` | Verified all 5 locked materials (`54.12%` `MAT_DarkNeutral` + `32.64%` `MAT_AltNeutral` = `86.76%` dark alloy body, `8.39%` `MAT_LightTrim`, `3.11%` `EMI_Cyan`, `0.84%` `EMI_Amber`) and `64×64` (`176-byte`) PNG swatch atlas. | **PASS** |
| **Clean Material & Clay Previews (No Wireframe Clutter)** | Clean material-shaded and clay-shaded previews without wireframe lines across faces; wireframe only in `07` | Verified visually across all 10 rendered preview sheets (`01`..`10`): views `01..06` and `08..10` use clean surface shading with `wire_overlay = False`; wireframe edges appear exclusively in `07_Preview_Wireframe_Topology.png`. | **PASS** |

### B. Spatial Integration Validation

| Check | Requirement / Target | Measured Evidence | Status |
|---|---|---|---|
| **Position `(43, 150, -300)` & Orientation Verified** | `CFrame.new(43, 150, -300) * CFrame.Angles(0, math.rad(-90), 0)` mapping `Local +Z` -> `World -X`, `Local +Y` -> `World +Y`, right-handed (`det = +1.0`) | Mathematically verified in `scripts/validate_package.py`: `RightVector = (0, 0, 1)`, `UpVector = (0, 1, 0)`, `ZVector = (-1, 0, 0)`, `Right × Up == ZVector`, `det(R) == +1.0000`. | **PASS** |
| **Actual Transformed World Bounds Recorded** | Expected `X in [39, 47]`, `Y in [150, 157.6]`, `Z in [-310, -290]` | Transformed all `7,272` OBJ vertices: **`World X in [39.0000, 47.0000]`**, **`World Y in [150.0000, 157.6000]`**, **`World Z in [-310.0000, -290.0000]`**. | **PASS** |
| **Inside Approved Plaza Station Region (`R = 37.0..52.5`)** | Peripheral station band `R = 37.0..52.5 studs` measured across real transformed vertices | Measured across all `7,272` transformed vertices from `(0, 150, -300)`: **`R_vertex_min = 39.3026 studs`** (`R_bbox_min = 39.0000` at centerline `Z = -300`, `>= 37.00`) and **`R_vertex_max = 47.9210 studs`** (`R_bbox_max = 48.0521`, `<= 52.50`). `100%` inside flat station band. | **PASS** |
| **Clearances to Neighbouring Hub Features Verified** | Clear of Queue Ring, Portal, Customize Kiosk, Mode Board & Leaderboard | Measured edge-to-edge clearances: **`25.0000 studs`** to `SM_Hub_QueuePadRing_01` (`X = +14.00`), **`18.6000 studs`** to `SM_Hub_QueuePortalArch_01` east pylon (`X = +20.40`), **`78.0000 studs`** to `SM_Hub_CustomizeKiosk_01` (`X = -39.00`), and **`16.0000 studs`** along Z from `Z = -310/-290` to Mode Board `(35, 150, -326)` and Leaderboard `(35, 150, -274)` centers. | **PASS** |

### C. Export, Package & Limitations Validation

| Check | Requirement / Target | Measured Evidence | Status |
|---|---|---|---|
| **OBJ & MTL Exported & Parsed** | Valid Wavefront `.obj` and `.mtl` | Parsed `2,424` faces, `7,272` vertices, `2,424` normals, `5` UVs, and `5` `newmtl` definitions across `18` `o GEO_ShopKiosk_*` objects. | **PASS** |
| **GLB Exported & Header/Length Checked** | Valid binary glTF 2.0 `.glb` (**`399,176 bytes` total file size**) | Parsed GLB v2 header (`total_len = 399,176 bytes`: `12-byte` GLB header + `8-byte` JSON chunk header + `20,828-byte` JSON chunk + `8-byte` BIN chunk header + `378,320-byte` BIN buffer chunk): `19` nodes (`1` root + `18` child meshes), `2,424` triangles, `5` PBR materials, embedded `64×64` PNG atlas. | **PASS** |
| **Manifest, Checksums & Final ZIP Integrity** | `validate_package.py --zip` passes on clean extraction | Verified **`30` ZIP entries** = **`28` payload files** in `MANIFEST.json` + `MANIFEST.json` + `SHA256SUMS.txt`; **`29/29` SHA-256 checksums verified (`100%`)** from clean extraction; `0` CRC errors; `0` nested archives. | **PASS** |
| **Editable `.blend` Binary Generation** | Save `.blend` if Blender is available | `blender` executable is not installed in this Linux container (`which blender` returned exit code 1). `generate_hub_shop_kiosk_blender.py` includes complete `bpy`/`bmesh` code to save `SM_Hub_ShopKiosk_01.blend` when run inside Blender. | **NOT RUN** |
| **Live Roblox Studio Import, Material & Walkability Test** | Import in Studio test place, apply `Metal`/`Neon`, verify collision & walkability | Roblox Studio is unavailable in this Linux container. Complete Luau scripts and instructions are provided in `ROBLOX_STUDIO_IMPORT_GUIDE.md`. | **NOT RUN** |
| **Owner Production Mesh Review** | Human owner sign-off on Phase 2 production Arena Shop Bar package | Ready for owner review of the exported `.obj`/`.mtl`/`.glb` meshes, 10 clean preview sheets, and audited 30-file package. | **REQUIRES OWNER REVIEW** |
| **Roblox Cloud Asset ID (`robloxAssetId`)** | Publish `MeshPart`s in target Studio experience | Remains `null` (`ASSET_PENDING`) until imported and published in Roblox Studio by the owner. | **ASSET_PENDING** |
