# Sphere Brawl: Rolling Rampage — Arena Shop Bar Production Package (`SM_Hub_ShopKiosk_01`)

**Package Path:** `3d-argon/changes/6/Sphere_Brawl_Hub_ShopKiosk_01_Package/`  
**Archive Path:** `3d-argon/changes/6/Sphere_Brawl_Hub_ShopKiosk_01_Package.zip`  
**Stage:** Step 4 — Phase 2: Approved Arena Shop Bar Production (`20.0 × 8.0 × 7.6 studs`)  
**Canonical Asset ID:** `SM_Hub_ShopKiosk_01`  
**Descriptive Name:** Sphere Brawl Arena Shop Bar (Static 3D Environment Showcase Station; Display-Only in Alpha)  
**Approved Concept Source:** `Sphere_Brawl_Shop_Bar_Concept_Reset_01.zip`  
**Authoritative Sources Inspected:** `tasks/TASK-03-KINETIC-HUB-ENVIRONMENT.md`, `tasks/TASK-09-ASSETS-VFX-ANIMATION-AUDIO.md`, `MASTER_IMPLEMENTATION_PLAN.md` (§2.2, §2.4, §11.1, §11.3, §11.4), `specs/DESIGN_CONSTANTS.md`, `DECISION_LOG.md` (D-001..D-027), `3d-argon/sphere_brawl_master_3d_art_bible_and_technical_handoff.md`, and local unmodified Step 1 (`SM_Hub_PlazaPlatform_01`), Step 2 (`SM_Hub_QueuePadRing_01`), Step 3 (`SM_Hub_CustomizeKiosk_01`), and Stage 4 (`SM_Hub_QueuePortalArch_01`) packages.

## 1. Production Summary

This package delivers the final production-ready 3D asset **`SM_Hub_ShopKiosk_01` (Sphere Brawl Arena Shop Bar)** built directly from the owner-approved Phase 1 concept (`Sphere_Brawl_Shop_Bar_Concept_Reset_01.zip`):

1. **Dominant Continuous Bar Counter (`GEO_ShopKiosk_Base`, `GEO_ShopKiosk_CounterBody`, `GEO_ShopKiosk_Countertop`):** A `15.10-stud` continuous customer-facing counter (`X in [-7.55, +7.55]`, `Y in [0.48, 2.92]`, `Z in [-2.22, +2.72]`) supported by a two-stage stepped plinth (`Y = 0.00..0.48`), featuring a recessed kick-toe, outward-angled faceted front fascia armor panels, `MAT_LightTrim` bullnose rail and vertical ribs, and recessed `EMI_Cyan` energy channels.
2. **Extended Side Wings (`GEO_ShopKiosk_SideWings`, `GEO_ShopKiosk_WingShelves`):** Purposeful left and right wings (`X in [-10.00, -7.15]` and `[+7.15, +10.00]`) with open presentation shelf decks (`Y = 2.38..2.60`) and floating upper wing rails (`Y = 3.85..4.25`), expanding the total station width to **`20.0000 studs`** while keeping the sides and rear completely open.
3. **Four Replaceable Non-Spherical Countertop Merchandise Displays (`GEO_ShopKiosk_DisplayPad_01..04` & `GEO_ShopKiosk_DisplayItem_01..04`):** Spaced evenly along the countertop at `Z = +0.25` (`X = -5.10, -1.70, +1.70, +5.10`):
   - **`GEO_ShopKiosk_DisplayItem_01` (`X = -5.10`):** Faceted Hexagonal Emblem / Shield Plate (`World (42.7500, 154.1800, -305.1000)`)
   - **`GEO_ShopKiosk_DisplayItem_02` (`X = -1.70`):** Vertical Toroidal Halo / Energy-Ring Ornament (`World (42.7500, 154.2200, -301.7000)`)
   - **`GEO_ShopKiosk_DisplayItem_03` (`X = +1.70`):** Segmented Triple-Chevron Trail-Effect Fins (`World (42.7500, 154.1500, -298.3000)`)
   - **`GEO_ShopKiosk_DisplayItem_04` (`X = +5.10`):** Geometric Starburst Burst-Effect Prism (`World (42.7500, 154.2500, -294.9000)`)
4. **Lightweight Suspended Sign Frame & Separate Blank UI-Ready Sign Panel (`GEO_ShopKiosk_SignFrame`, `GEO_ShopKiosk_SignPanel`):** Two slender raked rear struts (`X = ±6.45`) hold a segmented top visor (`Y = 7.28..7.60`) and the separate blank sign panel (`11.20 × 1.44 studs`, `Y in [5.68, 7.12]`), leaving a `2.36-stud` unobstructed viewing window above the counter.
5. **Measured Polygon & Envelope Contract:**
   - **Local Envelope (`+Y Up`, `+Z Forward`, `+X Right`):** `Width (X) = 20.0000 studs` (`[-10.0, +10.0]`), `Height (Y) = 7.6000 studs` (`[0.0, +7.6]`), `Depth (Z) = 8.0000 studs` (`[-4.0, +4.0]`).
   - **World-Aligned Envelope at `(43, 150, -300)` Facing `-X` (`Yaw = -90°`):** `World X in [39.0000, 47.0000]`, `World Y in [150.0000, 157.6000]`, `World Z in [-310.0000, -290.0000]` (Vertex radial span `R = 39.3026..47.9210 studs`, 100% inside `R = 37.0..52.5`).
   - **Measured Polygon Budget:** **`2,424 triangles`** (`7,272 export vertices`) across `18` named components—**`576` triangles (`19.20%`) below the `< 3,000 triangle` Hub station target**.

## 2. Canonical File Inventory (30 Total Package Files)

Using one canonical copy of each file without root/subdirectory duplication, the archive contains **30 files** (`28` payload files described in `MANIFEST.json` + `MANIFEST.json` + `SHA256SUMS.txt`):

| Relative Path in Package | Category | Description |
|---|---|---|
| `README.md` | Handoff Root | Package overview, production summary, canonical 30-file inventory, and quick-start commands |
| `MODEL_SPECIFICATION.md` | Handoff Root | Complete geometric, coordinate, countertop display slot, non-spherical item, and material specification |
| `ROBLOX_STUDIO_IMPORT_GUIDE.md` | Handoff Root | Step-by-step Roblox Studio 3D import, `WorldPivot`, `PivotTo`, material, collision, and replacement guide |
| `VALIDATION_REPORT.md` | Handoff Root | Measured validation results with explicit `PASS`, `NOT RUN`, `REQUIRES OWNER REVIEW`, and `ASSET_PENDING` statuses |
| `MANIFEST.json` | Handoff Root | Machine-readable manifest covering all 28 payload files, byte sizes, SHA-256 hashes, and geometry metrics |
| `SHA256SUMS.txt` | Handoff Root | `sha256sum -c` checksum list covering all 29 verifiable files (`28` payload files + `MANIFEST.json`) |
| `meshes/SM_Hub_ShopKiosk_01.obj` | 3D Mesh | Wavefront OBJ (`2,424 triangles`, `7,272 vertices`, 18 `o GEO_ShopKiosk_*` objects, UVs, vertex colors) |
| `meshes/SM_Hub_ShopKiosk_01.mtl` | 3D Material | Wavefront MTL material library (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`, `EMI_Amber`) |
| `meshes/SM_Hub_ShopKiosk_01.glb` | 3D Mesh | Binary glTF 2.0 (`19` nodes: root `SM_Hub_ShopKiosk_01` + `18` child meshes, `COLOR_0`, `TEXCOORD_0`, embedded PNG atlas) |
| `meshes/SphereBrawl_ShopKiosk_PaletteAtlas.png` | Texture | Companion `64×64` 4×2 sRGB palette atlas alongside `SM_Hub_ShopKiosk_01.mtl` |
| `meshes/collision_proxy/COL_ShopKiosk_Body.obj` | Optional Collider | Optional simple structural collision proxy (`36 triangles`: central counter box + left/right wing boxes) |
| `meshes/collision_proxy/COL_ShopKiosk_Body.mtl` | Optional Collider | Companion MTL for optional collision proxy |
| `meshes/collision_proxy/COL_ShopKiosk_Body.glb` | Optional Collider | Companion GLB for optional collision proxy |
| `meshes/collision_proxy/SphereBrawl_ShopKiosk_PaletteAtlas.png` | Optional Collider | Companion `64×64` palette atlas for optional collision proxy MTL |
| `textures/SphereBrawl_ShopKiosk_PaletteAtlas.png` | Texture | Canonical `64×64` (`<= 1024×1024`) palette swatch texture |
| `scripts/generate_hub_shop_kiosk_blender.py` | Generator | Deterministic Python 3 & Blender 3.6+/4.x (`bpy`/`bmesh`) procedural generator script |
| `scripts/validate_package.py` | Audit Tool | Automated package, manifest, file-size, SHA-256, right-handed orientation matrix, and clean-extraction ZIP audit tool |
| `config/shop_kiosk_parameters.json` | Config | Machine-readable dimensional, display slot, right-handed transform, material, and validation parameters |
| `manifest/SM_Hub_ShopKiosk_01.manifest.json` | Asset Manifest | Proposed canonical entry for `assets/asset-manifest.json` conforming to `specs/ASSET_MANIFEST.schema.json` |
| `docs/HUB_INTEGRATION_AND_CLEARANCE_REPORT.md` | Documentation | Spatial integration and clearance report against Plaza, Queue Ring, Portal Arch, Customize Kiosk, Mode Board, and Leaderboard |
| `previews/01_Preview_ThreeQuarter_Perspective.png` | Preview 1 | Clean material-shaded three-quarter player-approach view of the Arena Shop Bar |
| `previews/02_Preview_Front_Inward_Presentation.png` | Preview 2 | Direct front elevation, perspective presentation, and blank UI-ready `GEO_ShopKiosk_SignPanel` proof |
| `previews/03_Preview_Top_Orthographic_Arrangement.png` | Preview 3 | Top orthographic 3D render and dimensioned engineering footprint blueprint (`20.0 × 8.0 studs`) |
| `previews/04_Preview_Low_PlayerHeight_Approach.png` | Preview 4 | Low player-height (`Y = 4.5 studs`) gameplay views confirming storefront readability |
| `previews/05_Preview_Rear_Side_Underside_Construction.png` | Preview 5 | Rear three-quarter view, direct side/profile orthographic view, and upward underside construction view |
| `previews/06_Preview_NeutralClay_Geometry.png` | Preview 6 | Clean neutral studio clay geometry views verifying form and bevels without wireframe clutter |
| `previews/07_Preview_Wireframe_Topology.png` | Preview 7 | Dedicated depth-tested technical wireframe views (`2,424 triangles`) |
| `previews/08_Preview_Material_CloseUp.png` | Preview 8 | Close-up inspection of counter bullnose trim, recessed cyan channels, display pads, and 4 non-spherical items |
| `previews/09_Preview_Integration_Hub_Overview.png` | Preview 9 | Software-rendered Hub integration overview at `(43, 150, -300)` alongside unmodified Plaza, Queue Ring, Portal, and Customize Kiosk |
| `previews/10_Preview_Visual_Comparison_Customize_vs_Shop.png` | Preview 10 | Side-by-side clean neutral-clay comparison of `SM_Hub_CustomizeKiosk_01` vs. `SM_Hub_ShopKiosk_01` at identical scale and camera angle |

## 3. Reproducible Generation & Package Audit Commands

```bash
python3 scripts/generate_hub_shop_kiosk_blender.py --out_dir ./repro_exports
python3 scripts/validate_package.py
python3 scripts/validate_package.py --zip Sphere_Brawl_Hub_ShopKiosk_01_Package.zip
```
