# Validation Report — `SM_Hub_CustomizeKiosk_01` (Argon Step 3 — Final QA Correction)

**Validation Timestamp:** 2026-10-23  
**Asset ID:** `SM_Hub_CustomizeKiosk_01`  
**Validator Scripts:** `scripts/generate_hub_customize_kiosk_blender.py`, `scripts/validate_package.py`

## 1. Technical Validation Checklist (Prompt §11 & Step 3 Final QA Correction)

Explicit statuses used: `PASS`, `FAIL`, `NOT RUN`, `REQUIRES OWNER REVIEW`, `ASSET_PENDING`.

### A. Geometry Validation

| Check | Requirement / Target | Measured Evidence | Status |
|---|---|---|---|
| **Model Identity & Component Naming** | Root `SM_Hub_CustomizeKiosk_01` + consistent `GEO_CustomizeKiosk_*` subcomponents across OBJ, GLB & manifest | Verified `14` identical component names across `SM_Hub_CustomizeKiosk_01.obj`, `.glb` (`15` nodes including root), and `MANIFEST.json`. | **PASS** |
| **Actual Bounding Dimensions Recorded** | Proposed envelope `10.0 (W) × 9.5 (H) × 8.0 (D) studs` | Measured from `6,114` export vertices: `X in [-5.0000, +5.0000]` (`10.0000 studs`), `Y in [0.0000, +9.5000]` (`9.5000 studs`), `Z in [-4.0000, +4.0000]` (`8.0000 studs`). | **PASS** |
| **World Placement & Floor Pivot** | Floor-reference pivot `(0, 0, 0)` aligned to `World (-43, 150, -300)` at `Y = 150.0` | Base underside is at exact `Local Y = 0.0000`. Placed at `(-43, 150, -300)` via `CFrame.new(-43, 150, -300) * CFrame.Angles(0, math.rad(90), 0)`, world bounds are `X in [-47.00, -39.00]`, `Y in [150.00, 159.50]`, `Z in [-305.00, -295.00]`. | **PASS** |
| **Right-Handed Orientation Transform** | Valid orthonormal matrix mapping local `+Z` -> world `+X`, `+Y` -> `+Y`, `+X` -> `-Z` | Mathematically verified in `scripts/validate_package.py`: `RightVector = (0, 0, -1)`, `UpVector = (0, 1, 0)`, `ZVector = (1, 0, 0)`, `Right × Up == ZVector`, `det(R) == +1.0000`. | **PASS** |
| **Four Distinct Pedestals Present** | `GEO_CustomizeKiosk_DisplayPedestal_01` through `_04` | Verified 4 separate components (`100 tris` each) in stadium-stepped arc (`Slot 01/04` at `Local Z = +0.55` -> `World X = -42.45`; `Slot 02/03` elevated on `Y = 0.68` riser at `Local Z = -0.45` -> `World X = -43.45`). | **PASS** |
| **Four Replaceable Neutral Preview Spheres** | `GEO_CustomizeKiosk_PreviewSphere_01` through `_04` | Verified 4 separate `12×6` UV spheres (`120 tris` each, `R = 0.9000 studs`) at `World (-42.45, 153.05, -296.65)`, `(-43.45, 153.50, -298.85)`, `(-43.45, 153.50, -301.15)`, and `(-42.45, 153.05, -303.35)`. | **PASS** |
| **No Unfinished Chassis Models Used** | Do not include Trickster, Magnetar, Bulwark, or skin variants | Verified 100% generic neutral spheres; zero chassis silhouettes or Default/Neon/Gold/Void skin materials used. | **PASS** |
| **No Degenerate Faces or Normal Defects** | `0` degenerate faces; `dot(n_geom, vn) == 1.0` | Measured across all `2,038` triangles: `degenerate_faces = 0` (`min_area = 0.003150 sq. studs`), `normal_mismatches = 0`, closed underside at `Y = 0.0000` (`vn = (0, -1, 0)`). | **PASS** |
| **Triangle Count Measured** | Target `~1,850 tris`; Hub kiosk budget `< 2,500 tris` | Measured **`2,038 triangles`** in both `.obj` and `.glb` (`462 triangles` / `18.48%` below the `2,500` cap). | **PASS** |
| **Unit Scale Compatibility** | `1.0 Unit = 1.0 Roblox Stud` | Verified against `SM_Hub_PlazaPlatform_01` (`D = 140`), `SM_Hub_QueuePadRing_01` (`R = 14`), and `SM_Hub_QueuePortalArch_01`. | **PASS** |

### B. Layout & Spatial Integration Validation

| Check | Requirement / Target | Measured Evidence | Status |
|---|---|---|---|
| **Station at Locked Reference Position** | `(-43, 150, -300)` | Verified world footprint centered at `(-43.0000, 150.0000, -300.0000)` on `SM_Hub_PlazaPlatform_01`'s flat peripheral station ring (`R = 37.0..52.5 studs`, `Y = 150.0000`). | **PASS** |
| **Station Faces Inward Toward Hub** | Local `+Z` faces world `+X` toward `(0, 150, -300)` | Verified `CFrame.new(-43, 150, -300) * CFrame.Angles(0, math.rad(90), 0)` (`CFrame.fromMatrix(Vector3.new(-43, 150, -300), Vector3.new(0, 0, -1), Vector3.new(0, 1, 0), Vector3.new(1, 0, 0))`) maps local `+Z` to world `+X`. | **PASS** |
| **Four Displays Visible from Approach** | Unobstructed sightlines from player height | Verified in `02_Preview_Front_Inward_Presentation.png`, `04_Preview_Low_PlayerHeight_Approach.png`, and `09_Preview_Integration_Hub_Overview.png` (Slots `01..04` ordered left-to-right from `Z = -296.65` to `Z = -303.35`). | **PASS** |
| **No Overlap with Queue Ring or Portal** | Clear of `R = 14` Queue Ring and Portal Arch | Kiosk front toe is at `World X = -39.0000`: **`25.0000 studs` clearance** to `SM_Hub_QueuePadRing_01` (`X = -14.0000`) and **`23.9500 studs` clearance** to `SM_Hub_QueuePortalArch_01` (`X = -15.0500`). | **PASS** |
| **No Obstruction to Main Walking Paths** | Clear of outer curb (`R = 63.2`) and spawn route | Kiosk rear-most corners (`(-47, -305)` and `(-47, -295)`) sit at `R_max = 47.2652 studs` from Hub center, leaving **`15.9348 studs` clearance** inside the outer plaza curb (`R = 63.2000 studs`). | **PASS** |
| **Reference Assets Preserved Unchanged** | Do not modify Plaza, Queue Ring, Portal, or Rammer | Verified reference files were read-only inputs for clearance verification and Preview 09 rendering. | **PASS** |

### C. Export, Materials & Packaging Validation

| Check | Requirement / Target | Measured Evidence | Status |
|---|---|---|---|
| **OBJ / MTL Exported & Parsed** | Valid Wavefront `.obj` (`425,200 bytes`) and `.mtl` (`849 bytes`) | Parsed `2,038` faces, `6,114` vertices, `2,038` normals, `4` UVs, and `4` `newmtl` definitions. SHA-256 preserved unchanged. | **PASS** |
| **GLB Exported & Hierarchy Checked** | Valid binary glTF 2.0 `.glb` (**`334,648 bytes` total file size**) | Parsed GLB v2 header (`total_len = 334,648 bytes`: `12-byte` GLB header + `8-byte` JSON chunk header + `16,524-byte` JSON chunk + `8-byte` BIN chunk header + `318,096-byte` BIN buffer chunk): `15` nodes (`1` root + `14` child meshes), `2,038` triangles, `4` PBR materials, embedded `64×64` PNG atlas. SHA-256 preserved unchanged. | **PASS** |
| **Expected Material Slots Survive Export** | `MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan` | Verified all 4 locked materials and exact RGB values across `.obj`, `.mtl`, `.glb`, and `64×64` PNG texture (`<= 1024×1024`). | **PASS** |
| **Deterministic Generator Reproducibility** | Re-running generator produces identical SHA-256 hashes | Verified 100% identical `.obj`, `.mtl`, and `.glb` SHA-256 digests across independent runs (`scripts/generate_hub_customize_kiosk_blender.py` hash preserved unchanged). | **PASS** |
| **Package Inventory, Manifest, Transform & Checksums** | `validate_package.py` passes on clean ZIP extraction | Verified **`29` ZIP entries** = **`27` payload files** in `MANIFEST.json` + `MANIFEST.json` + `SHA256SUMS.txt`; **`28/28` SHA-256 checksums verified (`100%`)**; right-handed transform test `PASS`; `0` CRC errors. | **PASS** |
| **Editable `.blend` Binary Generation** | Generate `.blend` if Blender is installed | `blender` executable is not installed in this container (`which blender` returned exit code 1). `generate_hub_customize_kiosk_blender.py` includes complete `bpy`/`bmesh` code to save `SM_Hub_CustomizeKiosk_01.blend` when run in Blender. | **NOT RUN** |
| **Live Roblox Studio Import & Avatar Walk Test** | Import in Studio test place, apply `Metal`/`Neon`, verify walk-up | Roblox Studio is unavailable in this Linux container. Complete Luau scripts and instructions are provided in `ROBLOX_STUDIO_IMPORT_GUIDE.md`. | **NOT RUN** |
| **Owner Visual & Integration Review** | Human owner sign-off on Step 3 kiosk package | Ready for owner review of the 9 software-rendered previews and exported 3D package. | **REQUIRES OWNER REVIEW** |
| **Roblox Cloud Asset ID (`robloxAssetId`)** | Publish `MeshPart`s in target Studio experience | Remains `null` (`ASSET_PENDING`) until imported and published in Roblox Studio by the owner. | **ASSET_PENDING** |
