# Sphere Brawl: Rolling Rampage — Hub Customization Kiosk (`SM_Hub_CustomizeKiosk_01`)

**Package Path:** `3d-argon/changes/5/Sphere_Brawl_Hub_CustomizeKiosk_01_Package/`  
**Asset ID:** `SM_Hub_CustomizeKiosk_01`  
**Asset Type:** Static 3D Environment Showcase Station (Four-Pedestal Sphere Customization Kiosk)  
**Scope:** `TASK-03` Kinetic Hub Environment + `TASK-09` Assets, VFX, Animation and Audio  
**Authoritative Sources Inspected:** `tasks/TASK-03-KINETIC-HUB-ENVIRONMENT.md`, `tasks/TASK-09-ASSETS-VFX-ANIMATION-AUDIO.md`, `MASTER_IMPLEMENTATION_PLAN.md` (§2.2, §2.4, §11.1, §11.3, §11.4), `specs/DESIGN_CONSTANTS.md` (Palette & D-020/D-021), `DECISION_LOG.md` (D-001..D-027), `assets/asset-manifest.json`, `specs/ASSET_MANIFEST.schema.json`, `3d-argon/sphere_brawl_master_3d_art_bible_and_technical_handoff.md`, and local Step 1 (`SM_Hub_PlazaPlatform_01`), Step 2 (`SM_Hub_QueuePadRing_01`), Stage 4 (`SM_Hub_QueuePortalArch_01` & `SM_Chassis_Rammer_01`), and Arena Tiles packages.

## 1. Executive Summary & Scope Confirmation

This package delivers the validated static 3D model **`SM_Hub_CustomizeKiosk_01`**, a four-pedestal sphere-customization showcase positioned at the locked Hub station coordinate **`(-43, 150, -300)`** facing inward (`+X` in world space) toward the central Queue Portal at `(0, 150, -300)`:

- **Exact Measured Dimensions (100% Match to Proposed Envelope):**
  - **Local Envelope (`+Y Up`, `+Z Forward`, `+X Right`):** `Width (X) = 10.0000 studs` (`[-5.0000, +5.0000]`), `Height (Y) = 9.5000 studs` (`[0.0000, +9.5000]`), `Depth (Z) = 8.0000 studs` (`[-4.0000, +4.0000]`).
  - **Valid Right-Handed Placement Transform:**
    - Primary Euler rotation: `CFrame.new(-43, 150, -300) * CFrame.Angles(0, math.rad(90), 0)`
    - Equivalent right-handed orthonormal basis matrix: `CFrame.fromMatrix(Vector3.new(-43, 150, -300), Vector3.new(0, 0, -1), Vector3.new(0, 1, 0), Vector3.new(1, 0, 0))`
    - Maps local `+Z` (model front) to world `+X` (`(1, 0, 0)`), keeps local `+Y` vertical (`(0, 1, 0)`), and maps local `+X` (model right) to world `-Z` (`(0, 0, -1)`), so `p_world = (-43 + x_local*0 + z_local*1, 150 + y_local, -300 - x_local)`.
  - **World-Aligned Envelope at `(-43, 150, -300)` Facing `+X` (`Yaw = +90°`):** `World X in [-47.0000, -39.0000]` (`8.0000 studs` depth along X), `World Y in [150.0000, 159.5000]` (`9.5000 studs` height above the `Y = 150.0000` walking deck), `World Z in [-305.0000, -295.0000]` (`10.0000 studs` width along Z).
- **Measured Polygon Budget:** **`2,038 triangles`** (`6,114 export vertices`) across `14` cleanly separated, named components—well under the `< 2,500 triangle` Hub station budget (`18.48%` margin below cap) while preserving smooth `12×6` UV spheres (`120 tris` each) for the four replaceable preview spheres.
- **Four Separate Display Pedestals & Four Replaceable Generic Preview Spheres:**
  - Arranged in a stadium-stepped shallow arc so all four preview positions are 100% unobstructed from player height (`p_world = (-43 + z_local, 150 + y_local, -300 - x_local)`):
    - **Slot 01 (Outer Left Front):** `GEO_CustomizeKiosk_DisplayPedestal_01` + `GEO_CustomizeKiosk_PreviewSphere_01` at `Local (-3.3500, 3.0500, +0.5500)` -> **`World (-42.4500, 153.0500, -296.6500)`** (`R = 0.9000 studs`).
    - **Slot 02 (Inner Left Elevated):** `GEO_CustomizeKiosk_DisplayPedestal_02` + `GEO_CustomizeKiosk_PreviewSphere_02` at `Local (-1.1500, 3.5000, -0.4500)` -> **`World (-43.4500, 153.5000, -298.8500)`** (`R = 0.9000 studs`).
    - **Slot 03 (Inner Right Elevated):** `GEO_CustomizeKiosk_DisplayPedestal_03` + `GEO_CustomizeKiosk_PreviewSphere_03` at `Local (+1.1500, 3.5000, -0.4500)` -> **`World (-43.4500, 153.5000, -301.1500)`** (`R = 0.9000 studs`).
    - **Slot 04 (Outer Right Front):** `GEO_CustomizeKiosk_DisplayPedestal_04` + `GEO_CustomizeKiosk_PreviewSphere_04` at `Local (+3.3500, 3.0500, +0.5500)` -> **`World (-42.4500, 153.0500, -303.3500)`** (`R = 0.9000 studs`).
  - All four placeholder spheres are neutral `MAT_AltNeutral` (`#2A3246`) generic spheres that do not masquerade as unfinished chassis models or skin packages.

## 2. Canonical File Inventory (29 Total Package Files)

Preferring one canonical copy of each file without unnecessary root/subdirectory duplication, the archive contains **29 files** (`27` payload files described in `MANIFEST.json` + `MANIFEST.json` + `SHA256SUMS.txt`):

| Relative Path in Package | Category | Size (Bytes) | Description |
|---|---|---:|---|
| `README.md` | Handoff Root | Dynamic | Package overview, canonical file inventory, and quick-start commands |
| `MODEL_SPECIFICATION.md` | Handoff Root | Dynamic | Complete geometric, coordinate, pedestal slot, and per-component specification |
| `ROBLOX_STUDIO_IMPORT_GUIDE.md` | Handoff Root | Dynamic | Step-by-step Roblox Studio 3D import, `WorldPivot`, `PivotTo`, material, collision, and replacement guide |
| `VALIDATION_REPORT.md` | Handoff Root | Dynamic | Measured validation results with explicit `PASS`, `NOT RUN`, and `ASSET_PENDING` statuses |
| `MANIFEST.json` | Handoff Root | Dynamic | Machine-readable manifest covering all 27 payload files, byte sizes, SHA-256 hashes, and geometry metrics |
| `SHA256SUMS.txt` | Handoff Root | Dynamic | `sha256sum -c` checksum list covering all 28 verifiable files (`27` payload files + `MANIFEST.json`) |
| `meshes/SM_Hub_CustomizeKiosk_01.obj` | 3D Mesh | `425,200` | Wavefront OBJ (`2,038 triangles`, `6,114 vertices`, 14 `o GEO_CustomizeKiosk_*` objects, UVs, vertex colors) |
| `meshes/SM_Hub_CustomizeKiosk_01.mtl` | 3D Material | `849` | Wavefront MTL material library (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`) |
| `meshes/SM_Hub_CustomizeKiosk_01.glb` | 3D Mesh | `334,648` | Binary glTF 2.0 (`15` nodes: root `SM_Hub_CustomizeKiosk_01` + `14` child meshes, `COLOR_0`, `TEXCOORD_0`, embedded PNG atlas) |
| `meshes/SphereBrawl_CustomizeKiosk_PaletteAtlas.png` | Texture | `166` | Companion `64×64` 2×2 sRGB palette atlas alongside `SM_Hub_CustomizeKiosk_01.mtl` |
| `meshes/collision_proxy/COL_CustomizeKiosk_Body.obj` | Optional Collider | `4,995` | Optional simple structural collision proxy (`24 triangles`: rear frame + lower plinth) |
| `meshes/collision_proxy/COL_CustomizeKiosk_Body.mtl` | Optional Collider | `283` | Companion MTL for optional collision proxy |
| `meshes/collision_proxy/COL_CustomizeKiosk_Body.glb` | Optional Collider | `5,152` | Companion GLB for optional collision proxy |
| `meshes/collision_proxy/SphereBrawl_CustomizeKiosk_PaletteAtlas.png` | Optional Collider | `166` | Companion `64×64` palette atlas for optional collision proxy MTL |
| `textures/SphereBrawl_CustomizeKiosk_PaletteAtlas.png` | Texture | `166` | Canonical `64×64` (`<= 1024×1024`) palette swatch texture |
| `scripts/generate_hub_customize_kiosk_blender.py` | Generator | `52,879` | Deterministic Python 3 & Blender 3.6+/4.x (`bpy`/`bmesh`) procedural generator script |
| `scripts/validate_package.py` | Audit Tool | Dynamic | Automated package, manifest, file-size, SHA-256, right-handed orientation matrix, and clean-extraction ZIP audit tool |
| `config/customize_kiosk_parameters.json` | Config | Dynamic | Machine-readable dimensional, pedestal, right-handed transform, material, and validation parameters |
| `manifest/SM_Hub_CustomizeKiosk_01.manifest.json` | Asset Manifest | `1,046` | Proposed canonical entry for `assets/asset-manifest.json` conforming to `specs/ASSET_MANIFEST.schema.json` |
| `docs/HUB_INTEGRATION_AND_CLEARANCE_REPORT.md` | Documentation | Dynamic | Supplementary spatial integration and clearance report against Plaza, Queue Ring, and Portal Arch |
| `previews/01_Preview_ThreeQuarter_Perspective.png` | Preview 1 | `122,941` | Three-quarter perspective view showing entire kiosk and all four sphere displays |
| `previews/02_Preview_Front_Inward_Presentation.png` | Preview 2 | `90,342` | Front inward-facing presentation showing four distinct pedestals and slot coordinates |
| `previews/03_Preview_Top_Orthographic_Arrangement.png` | Preview 3 | `215,632` | Top orthographic render and engineering spacing blueprint of the four preview positions |
| `previews/04_Preview_Low_PlayerHeight_Approach.png` | Preview 4 | `105,488` | Low player-height (`Y = 4.5 studs`) camera view showing readability and approach clearance |
| `previews/05_Preview_Rear_Side_Underside_Construction.png` | Preview 5 | `77,857` | Rear three-quarter, side profile orthographic, and underside upward construction views |
| `previews/06_Preview_NeutralClay_Geometry.png` | Preview 6 | `102,191` | Neutral studio clay geometry views verifying silhouette, bevels, and normal continuity |
| `previews/07_Preview_Wireframe_Topology.png` | Preview 7 | `173,003` | Depth-tested technical wireframe views (`2,038 triangles`) |
| `previews/08_Preview_Material_CloseUp.png` | Preview 8 | `79,076` | Macro close-up of dark alloy (`#202636`), alt slate (`#2A3246`), light trim (`#AABED7`), and cyan (`#00C3FF`) |
| `previews/09_Preview_Integration_Hub_Overview.png` | Preview 9 | Dynamic | Software-rendered Hub integration overview at `(-43, 150, -300)` with unmodified Plaza, Queue Ring, and Portal |

## 3. Reproducible Generation & Package Audit Commands

To deterministically regenerate all meshes in standard Python 3:

```bash
python3 scripts/generate_hub_customize_kiosk_blender.py --out_dir ./repro_exports
```

To run inside Blender 3.6+ / 4.x and also save an editable `.blend` file (`SM_Hub_CustomizeKiosk_01.blend`):

```bash
blender --background --python scripts/generate_hub_customize_kiosk_blender.py -- --out_dir ./repro_exports
```

To run the automated package, orientation transform, and ZIP integrity audit:

```bash
python3 scripts/validate_package.py
python3 scripts/validate_package.py --zip /path/to/Sphere_Brawl_Hub_CustomizeKiosk_01_Package.zip
```
