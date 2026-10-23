# Validation Report — `SM_Hub_PlazaPlatform_01` (Argon Step 1)

**Validation Timestamp:** 2026-10-23  
**Validator Script:** `artifacts/file_generation/ttl=63d/intermediate/render_and_validate_hub_platform.py`

## 1. Required Validation Scorecard (Prompt §11)

| Check | Expected Result | Measured Evidence | Status |
|---|---|---|---|
| **Asset identity** | `SM_Hub_PlazaPlatform_01` used consistently | Root node in `.glb`, header in `.obj`/`.mtl`, manifest ID, and documentation all use `SM_Hub_PlazaPlatform_01`. | **PASS** |
| **Outer diameter** | Exactly `140 studs` | Measured across all `8,064` vertices in `.obj` and `.glb`: `2 * max(sqrt(X^2 + Z^2)) = 140.0000 studs` (`R_max = 70.0000 studs`). | **PASS** |
| **XZ footprint** | Does not exceed `140 × 140 studs` | Measured bounding box: `X in [-70.0000, +70.0000]` (`140.0000 studs`), `Z in [-70.0000, +70.0000]` (`140.0000 studs`). | **PASS** |
| **Top-surface elevation** | Local top = `0`; intended world top = `Y 150` | Measured `Y_max = 0.0000 studs`, `Y_min = -12.0000 studs` (`0` vertices with `Y > 0.0000`). At world pivot `(0, 150, -300)`, top surface maps to `World Y = 150.0000`. | **PASS** |
| **Pivot** | Documented and aligned to the center of the top walking surface | Local origin `(0.0000, 0.0000, 0.0000)` is at the exact XZ center `(0, 0)` and top walking surface `Y = 0.0000`. | **PASS** |
| **Axis convention** | Verified for Roblox import | Authored and exported with `+Y Up`, `+Z Forward`, `+X Right`, `1.0 unit = 1.0 stud`. Cardinal bridges align with `0°, 90°, 180°, 270°`. | **PASS** |
| **Queue Portal clearance** | No conflicting or duplicated portal-pad geometry | Inspected `QueuePortalArch_Prototype.obj` (`R_floor in [15.02, 20.47]`, queue pad `R = 14.0`). Platform surface in `R <= 21.20` is 100% flat at `Y = 0.0000` (`0` protrusions). Inner framing conduit sits at `R in [21.20, 23.00]` (`+0.7342 studs` radial clearance outside portal pylon buttresses). | **PASS** |
| **Mesh integrity** | No detected degenerate faces, inverted normals or unintended holes | `0` degenerate triangles (`min_area = 0.052000 sq. studs`), `0` face-winding/normal mismatches (`dot(n_geom, vn) == 1.0` across all `2,688` faces), `100%` finite coordinates. | **PASS** |
| **Visual appearance** | Coherent structural layers, consistent bevels and controlled cyan accents | Verified across all 5 software Z-buffer rendered preview sheets; `MAT_DarkNeutral` = `67.13%` top area (`63.31%` 3D area), `MAT_AltNeutral` = `24.04%` top (`27.92%` 3D), `MAT_LightTrim + EMI_Cyan` = `8.82%` top (`8.77%` 3D). | **REQUIRES OWNER REVIEW** |
| **Material separation** | Expected material slots survive export and re-import | Re-parsed `.obj`, `.mtl`, and `.glb`: all 4 locked materials (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`) and all 7 child component nodes (`GEO_PlazaPlatform_*`) survive export and re-import with `< 0.0001` RGB error. | **PASS** |
| **Triangle count** | Measured and recorded | Measured `2,688 triangles` (`8,064 export vertices`) in both `.obj` and `.glb` (below the proposed `6,000` triangle target). Optional collision proxy `COL_PlazaPlatform_Deck` is `128 triangles`. | **PASS** |
| **File consistency** | OBJ, MTL, GLB and source correspond to the same final design | `.obj` and `.glb` match 100% on triangle count (`2,688`), vertex count (`8,064`), bounding box (`[-70, -12, -70]` to `[70, 0, 70]`), and child component list. | **PASS** |
| **Reproducibility** | Generator runs successfully in the available environment | Re-executed `python3 scripts/generate_hub_plaza_platform_blender.py --out_dir /tmp/repro_hub_test`; output `.obj`, `.mtl`, and `.glb` produced 100% identical SHA-256 hashes. | **PASS** |
| **Import verification (Local Re-Import Parser)** | Re-opened and parsed exported `.obj`, `.mtl`, and `.glb` locally | Executed independent Python parsers (`parse_and_validate_obj`, `parse_and_validate_mtl`, `parse_and_validate_glb`) verifying binary glTF chunks, accessors, normals, UVs, and vertex colors. | **PASS** |
| **Import verification (Live Roblox Studio & Walkability)** | Live Roblox Studio 3D Importer, `Enum.Material` setup & R15 walk test | Roblox Studio is not installed in this headless Linux VM container. Exact import, pivot, material, and collision instructions are documented in `ROBLOX_STUDIO_IMPORT_GUIDE.md`. | **NOT RUN** |
| **Blender `.blend` Binary Creation** | Native `.blend` file creation via Blender executable | Blender (`blender` / `bpy`) is not installed in this Linux VM container. The deterministic generator `scripts/generate_hub_plaza_platform_blender.py` includes full `bpy`/`bmesh` support to save `SM_Hub_PlazaPlatform_01.blend` when run on a machine with Blender 3.6+/4.x. | **NOT RUN** |
| **Package integrity** | ZIP opens and contains the expected files | Verified with `zipfile.ZipFile.testzip()` (`0` errors) and full file inventory check. | **PASS** |
| **Checksums** | Generated and checked against the final deliverables | `SHA256SUMS.txt` generated and programmatically verified against every file on disk and inside `Sphere_Brawl_Hub_Platform_01_Package.zip`. | **PASS** |

## 2. Per-Component Measured Breakdown

| Component (`o` / GLB Child Node) | Material Slot | Triangle Count | Export Vertices |
|---|---|---:|---:|
| `GEO_PlazaPlatform_Deck` | `MAT_DarkNeutral` | `408` | `1224` |
| `GEO_PlazaPlatform_DeckInlays` | `MAT_AltNeutral` | `360` | `1080` |
| `GEO_PlazaPlatform_Rim` | `MAT_DarkNeutral` | `224` | `672` |
| `GEO_PlazaPlatform_Structure` | `MAT_AltNeutral` | `448` | `1344` |
| `GEO_PlazaPlatform_Underside` | `MAT_DarkNeutral` | `224` | `672` |
| `GEO_PlazaPlatform_Trim` | `MAT_LightTrim` | `840` | `2520` |
| `GEO_PlazaPlatform_CyanAccents` | `EMI_Cyan` | `184` | `552` |
| **Total (`SM_Hub_PlazaPlatform_01`)** | **4 Materials** | **`2,688`** | **`8,064`** |
| `COL_PlazaPlatform_Deck` (Optional Collision Proxy) | `MAT_DarkNeutral` | `128` | `384` |
