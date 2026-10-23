# Validation Report — `SM_Hub_QueuePadRing_01` (Argon Step 2)

**Validation Timestamp:** 2026-10-23  
**Asset ID:** `SM_Hub_QueuePadRing_01`  
**Validator Scripts:** `generate_hub_queue_pad_ring_blender.py`, `build_and_validate_queue_pad_ring.py`

---

## 1. Comprehensive Validation Checklist (Prompt §9)

Explicit status labels used: `PASS`, `FAIL`, `NOT RUN`, `REQUIRES OWNER REVIEW`, `ASSET_PENDING`.

### A. Geometry Validation

| Check | Requirement / Target | Measured Evidence | Status |
|---|---|---|---|
| **Asset Name & Exported Files** | `SM_Hub_QueuePadRing_01` across `.obj`, `.mtl`, `.glb`, generator & docs | Verified root node `SM_Hub_QueuePadRing_01` in `.glb`, header & `mtllib` in `.obj`/`.mtl`, and 4 named `GEO_QueuePadRing_*` components. | **PASS** |
| **Outer Radius & Diameter** | Outer radius `14.0000 studs`, outer diameter `28.0000 studs` | Measured across all `2,880` export vertices: `R_xz_max = 14.0000 studs`, `Outer_Diameter = 28.0000 studs` (`X in [-14.0000, +14.0000]`, `Z in [-14.0000, +14.0000]`). | **PASS** |
| **Inner Radius & Band Width** | Unobstructed central standing area; narrow boundary band | Measured `R_xz_min = 12.8000 studs` (`Inner_Diameter = 25.6000 studs`), `Band_Width = 1.2000 studs` (`0` vertices inside `R_xz < 12.8000`, `0` vertices outside `R_xz > 14.0000`). | **PASS** |
| **Scale in Studs** | `1.0 Blender/Export Unit = 1.0 Roblox Stud` | Verified `28.0000 × 0.0760 × 28.0000 studs` bounding box (`+Y Up`, `+Z Forward`, `+X Right`). | **PASS** |
| **Pivot & Documented Placement** | Floor-level centre pivot `(0, 0, 0)` mapping to World `(0, 150, -300)` | Verified `Center_X = 0.0000`, `Center_Z = 0.0000`; `WorldPivot` calibration and `PivotTo(CFrame.new(0, 150, -300))` script documented in `ROBLOX_STUDIO_IMPORT_GUIDE.md`. | **PASS** |
| **Clean Normals & Winding** | Outward-consistent face winding and unit normals | Verified `dot(n_geom, vn) == 1.0` across all `960` triangles (`0` normal mismatches; `0` inverted upper faces). | **PASS** |
| **No Degenerate Faces** | Zero-area triangle count = `0` | Verified across all `960` triangles: `0` degenerate faces (`min_triangle_area = 0.002015 sq. studs > 1e-6`). | **PASS** |
| **No Duplicate or Floating Geometry** | Watertight, contiguous 32-sector ring + 16 integrated clasps | Verified all `960` triangles belong to the 4 contiguous ring/clasp components within `R in [12.8000, 14.0000]` and `Y in [0.0040, 0.0800]`. | **PASS** |
| **No Protrusions into Walking Surface** | Low-profile floor-integrated inlay; non-colliding | Max bezel height `Y_max = +0.0800 studs` (`+0.0440 studs` at cardinal threshold gates); `CanCollide = false` contract documented. | **PASS** |
| **Central Standing Area Clear** | `R < 12.8000 studs` completely open | `0` triangles and `0` vertices inside `R_xz < 12.8000 studs` (`514.72 sq. studs` unobstructed central circle). | **PASS** |
| **Polygon Count Recorded** | Well below TASK-09 budget (`< 2,500 tris` for Hub stations) | Exact measured count: **`960 triangles`** (`2,880 export vertices`) in both `.obj` and `.glb`. | **PASS** |

### B. Spatial Integration Validation

| Check | Requirement / Target | Measured Evidence | Status |
|---|---|---|---|
| **Compared Against Existing Queue Portal** | Inspect `QueuePortalArch_Prototype.obj` (`SM_Hub_QueuePortalArch_01`) | Programmatically parsed `9,504` portal vertices: floor elements span `R_xz in [15.0187, 20.4658] studs` (`|X| >= 15.0500 studs`). | **PASS** |
| **Compared Against Existing Plaza Platform** | Inspect `SM_Hub_PlazaPlatform_01.obj` (`SM_Hub_PlazaPlatform_01`) | Programmatically parsed `8,064` platform vertices: top deck at `Y = 0.0000` is flat across `R <= 21.2000 studs`; inner framing ring is at `R in [21.2000, 23.0000]`. | **PASS** |
| **No Duplicated Portal or Plaza Details** | Complement existing assets without duplicating arch, curbs, or deck | Reuses Plaza Platform's central deck (`R < 12.80`) and outer framing ring (`R = 21.20..23.00`), and reuses Portal Arch's pylons/curbs (`R >= 15.05`). | **PASS** |
| **Radius-14 Boundary Verified** | Outer edge matches `GameConfig.Lobby.QueuePadRadius = 14` | Verified `R_outer = 14.0000 studs` (`D = 28.0000 studs`). | **PASS** |
| **Relevant Clearances Measured & Documented** | Record radial and vertical margins | `+1.0500 studs` to portal pylon brackets (`|X| = 15.05`), `+1.2000 studs` to portal flank glow rims (`R = 15.20`), `+7.2000 studs` to plaza framing ring (`R = 21.20`), `+0.0040 studs` vertical offset above `Y = 0.0000` deck (zero z-fighting). | **PASS** |
| **Material Palette Consistent with Project** | Locked 4-slot Hub palette (`#202636`, `#2A3246`, `#AABED7`, `#00C3FF`) | 100% exact RGB match across `.mtl`, `.obj` vertex colors, `.glb` `baseColorFactor`/`COLOR_0`, and `64×64` PNG atlas. | **PASS** |

### C. Export, Previews, Package & Live Runtime Validation

| Check | Requirement / Target | Measured Evidence | Status |
|---|---|---|---|
| **OBJ / MTL Exported & Checked** | Valid Wavefront `.obj` and `.mtl` with resolved `mtllib`/`usemtl` | Parsed `SM_Hub_QueuePadRing_01.obj` (`960` faces, `2,880` verts, `4` `o` groups) and `.mtl` (`4` `newmtl` blocks). | **PASS** |
| **GLB Exported & Checked** | Valid binary glTF 2.0 `.glb` with multi-node hierarchy & vertex colors | Parsed 12-byte GLB header + JSON + BIN chunks: `5` nodes (`1` root + `4` child meshes), `960` triangles, `COLOR_0`, `TEXCOORD_0`, and embedded PNG atlas. | **PASS** |
| **Material Assignments Verified** | 70 / 20 / 10 visual hierarchy preserved across exports | `BaseCollar (MAT_DarkNeutral) = 320 tris (69.78% 3D area)`, `ChannelInlay (MAT_AltNeutral) = 320 tris (11.46%)`, `TrimBezels (MAT_LightTrim) = 256 tris (9.20%)`, `CyanConduit (EMI_Cyan) = 64 tris (9.56%)`. | **PASS** |
| **Deterministic Generator Reproducibility** | Re-running generator produces identical SHA-256 outputs | Executed independent reproducibility run in `/tmp/repro_queue_ring_verify`; `.obj`, `.mtl`, and `.glb` SHA-256 digests matched 100%. | **PASS** |
| **Documentation, Manifest & Previews Included** | `README.md`, `MODEL_SPECIFICATION.md`, `ROBLOX_STUDIO_IMPORT_GUIDE.md`, `VALIDATION_REPORT.md`, `PORTAL_AND_PLAZA_CLEARANCE_REPORT.md`, `MANIFEST.json`, `SHA256SUMS.txt`, 8 PNG previews | All required documents and all 8 rendered PNG previews (`1920×1080`) generated and visually inspected. | **PASS** |
| **SHA-256 Checksums & ZIP Integrity** | `SHA256SUMS.txt` & `MANIFEST.json` included at package root in ZIP; `zipfile.testzip()` passes | Verified `0` CRC/ZIP errors across all `33` ZIP file entries (`31` content files + `MANIFEST.json` + `SHA256SUMS.txt`) and `32/32` (`100%`) SHA-256 checksum matches via `sha256sum -c SHA256SUMS.txt`. | **PASS** |
| **Owner Visual Review of Exported Renders** | Visual approval of proportions, trim, and cyan detailing | Approved by owner in Step 2 review (`8` high-resolution preview sheets preserved unchanged). | **PASS** |
| **Blender `.blend` Binary Generation** | Native `.blend` file creation via Blender executable | `blender` binary is not installed in this Linux container (`which blender` not found). `generate_hub_queue_pad_ring_blender.py` includes complete `bpy`/`bmesh` code to save `SM_Hub_QueuePadRing_01.blend` when run in Blender 3.6+/4.x. | **NOT RUN** |
| **Live Roblox Studio Import, Co-Placement & Avatar Walk Test** | Import `.glb`/`.obj` into Studio, apply `Metal`/`Neon`, co-place with Portal & Plaza at `(0, 150, -300)`, walk R15 avatar across ring | Roblox Studio is not available in this Linux container. Complete step-by-step Luau verification scripts and instructions are provided in `ROBLOX_STUDIO_IMPORT_GUIDE.md`. | **NOT RUN** |
| **Roblox Cloud Asset Upload (`robloxAssetId`)** | Assign published `rbxassetid://` after Studio import | Remains `null` (`ASSET_PENDING` in `assets/asset-manifest.json` until imported and published by owner in Roblox Studio). | **ASSET_PENDING** |
