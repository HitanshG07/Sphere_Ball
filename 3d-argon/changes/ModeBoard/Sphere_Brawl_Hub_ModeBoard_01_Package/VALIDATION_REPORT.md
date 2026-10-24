# Validation Report — `SM_Hub_ModeBoard_01` (Step 5, Phase 2 Final Production Mesh & Package)

- **Validation Timestamp:** `2026-10-24`
- **Canonical Asset ID:** `SM_Hub_ModeBoard_01`
- **Descriptive Name:** Tactical Arena Mode Selection Command Gantry (`14.4000 × 3.8000 × 8.8000 studs`)
- **Approved Phase 1 Concept Source:** `Sphere_Brawl_Hub_ModeBoard_Concept_01.zip` (`SHA-256: e76c211dd44fc5c36d71a546ef8e683de05923e8ee142e203173caabeeaddeb6`)
- **Generator & Validator Scripts:** `scripts/generate_mode_board_blender.py`, `scripts/validate_package.py`

---

## 1. Technical Validation Matrix

Explicit statuses used: `PASS`, `FAIL`, `NOT RUN`, `NOT APPLICABLE`, `REQUIRES OWNER REVIEW`, `ASSET_PENDING`.

### A. Concept Fidelity, Geometry, Normals & Triangle Budget Validation

| Check | Requirement / Target | Method | Measured Evidence | Status |
|---|---|---|---|---|
| **Approved Concept Archive Hash Confirmed** | Confirm `Sphere_Brawl_Hub_ModeBoard_Concept_01.zip` matches `e76c211d...` before building Phase 2 | `sha256sum` CLI on Phase 1 ZIP | Verified `e76c211dd44fc5c36d71a546ef8e683de05923e8ee142e203173caabeeaddeb6` (`1,647,242 bytes`). | **PASS** |
| **Approved Concept Silhouette & Layout Preserved** | Grounded 2-stage plinth, layered A-frame buttresses + collar clamps, `14.0°` tilted command matrix, overhead visor/header, 1 left active hero bay + 3 right stacked Coming Soon bays | Visual & vertex audit across `01`..`10` previews | Preserved 100% of the approved Phase 1 silhouette and proportions with zero redesign, zero extra modes, and zero random props. | **PASS** |
| **Final Primary Triangle Count (`< 2,500` Budget)** | Master 3D Art Bible station budget `< 2,500` triangles | Parsed exported `SM_Hub_ModeBoard_01.obj` & `.glb` | Measured **`1,612 triangles`** (`4,836 vertices`) across `18` named components — **`888 triangles` (`35.52%`) below the `< 2,500` station budget**. | **PASS** |
| **Optional Collision Proxy Triangle Count** | Simplified non-snagging collider proxy reported separately | Parsed `COL_ModeBoard_Body.obj` & `.glb` | Measured **`36 triangles`** (`108 vertices`) across `3` box hulls (`BaseHull`, `MainGantryHull`, `CanopyHull`). Leaves front walk-up zone (`Local Z > +1.52`) open. | **PASS** |
| **Local Bounding Box & Floor-Reference Pivot** | `X in [-7.20, +7.20]` (`14.40`), `Y in [0.00, +8.80]` (`8.80`), `Z in [-1.90, +1.90]` (`3.80`), pivot `(0,0,0)` at bottom footprint center | Vertex min/max scan across all `4,836` OBJ/GLB vertices | Measured `X in [-7.2000, +7.2000]` (`14.4000 studs`), `Y in [0.0000, +8.8000]` (`8.8000 studs`), `Z in [-1.9000, +1.9000]` (`3.8000 studs`). `0.0000 stud` deviation. | **PASS** |
| **Mesh Degeneracy, Winding & Normal Consistency** | `0` degenerate faces (`area > 0`), `0` inverted/mismatched normals, sealed underside at `Y = 0` | Programmatic cross-product & normal dot-product check | `degenerate_faces = 0` (`min_triangle_area = 0.001060 sq. studs`), `normal_mismatches = 0`, sealed underside at `Local Y = 0.0000` (`vn = (0, -1, 0)`). | **PASS** |
| **Coplanar Cross-Component Z-Fighting Check** | `0` overlapping same-normal coplanar triangles between different components | 2D Separating Axis Theorem (SAT) polygon intersection test across all plane groups | Measured **`0` cross-component same-normal coplanar overlaps** across all `1,612` triangles. | **PASS** |
| **Named Component Hierarchy (`18` Components)** | Clean named components preserved across OBJ, GLB, config & docs | Parsed OBJ `o` tags & GLB `nodes` array | Verified `18` identical `GEO_ModeBoard_*` components in OBJ and `19` nodes (`SM_Hub_ModeBoard_01` root + `18` child nodes) in GLB. | **PASS** |
| **Five Separate UI-Ready Replaceable Panel Surfaces** | `GEO_ModeBoard_UIPanel_01_FFA`, `_02_Duel`, `_03_TeamClash`, `_04_KingTile`, and `GEO_ModeBoard_HeaderSign` flat & free of baked text | Normal & plane coplanarity audit + visual check in `09_Production_UI_Panel_Surface_Proof.png` | All 5 components have exact flat 2-triangle front quads (`vn = (0, 0.24192, 0.97030)` for mode panels, `vn = (0, 0, 1)` for header sign) and `0` baked text triangles. | **PASS** |
| **Locked 5-Slot Palette & Texture Atlas** | `MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`, `EMI_Amber`; texture `<= 1024×1024` | Parsed MTL, GLB materials & PNG header | Verified all 5 locked materials (`82.17%` dark/slate body, `15.65%` light metallic trim, `2.06%` `EMI_Cyan`, `0.11%` `EMI_Amber`) and `64×64` (`176-byte`) PNG swatch atlas. | **PASS** |
| **Ten Clean Production Previews (`previews/01..10`)** | 10 PNGs of final exported mesh; beauty views `01`..`09` wireframe-free; wireframe isolated to `10` | Visual inspection via `view_file` across `previews/01..10` | Verified all 10 high-resolution (`2400×1350`) PNG sheets inside `previews/`. Beauty views `01`..`09` have `wire_overlay = False`. | **PASS** |

### B. Spatial Transform, Radial Band & Neighbour Clearance Validation

| Check | Requirement / Target | Method | Measured Evidence | Status |
|---|---|---|---|---|
| **Placement Transform & Front Direction Verified** | `CFrame.new(35, 150, -326) * CFrame.Angles(0, math.rad(-53.39292061), 0)` maps `Local +Z` to `FrontVector = (-0.802744, 0, +0.596324)` | Orthonormal matrix & dot-product check in `validate_package.py` | Verified `RightVector = (+0.596324, 0, +0.802744)`, `UpVector = (0, 1, 0)`, `ZVector = (-0.802744, 0, +0.596324)`, `det(R) = +1.0000`, `R^T R = I_3`. | **PASS** |
| **Actual Transformed World Bounds Recorded** | Transform all `4,836` exported production vertices into world space | Vertex matrix transform in `validate_package.py` | **`World X in [29.3702, 40.6298]`** (`11.2595 studs`), **`World Y in [150.0000, 158.8000]`** (`8.8000 studs`), **`World Z in [-332.6738, -319.3320]`** (`13.3418 studs`). | **PASS** |
| **Peripheral Station Ring Fit (`R in [37.0, 52.5]`)** | All transformed vertices fit inside the flat station ring on `SM_Hub_PlazaPlatform_01` | Euclidean distance from `(0, 150, -300)` across all `4,836` vertices | **`R_vertex_min = 41.7610 studs`** (`+4.7610` margin above `37.0`) and **`R_vertex_max = 46.0024 studs`** (`+6.4976` margin below `52.5`). `100%` inside flat station ring. | **PASS** |
| **Neighbouring Station & Route Clearances** | Recalculate clearances using actual exported production vertices | Pairwise vertex & bounding-box distance audit | **`10.1829 studs` min XZ vertex distance** (`9.3320 studs` Z gap) to `SM_Hub_ShopKiosk_01`; **`27.7610 studs`** to `SM_Hub_QueuePadRing_01`; **`24.5615 studs`** to `SM_Hub_QueuePortalArch_01` East Pylon; **`29.3702 studs`** lateral clearance to `X = 0` Main Spawn-to-Portal corridor; **`42.3018 studs` (estimated)** to future `SM_Hub_Leaderboard_01`. | **PASS** |

### C. Export Readability, Package Finalization & Environment Gates

| Check | Requirement / Target | Method | Measured Evidence | Status |
|---|---|---|---|---|
| **OBJ, MTL & GLB Readability & Consistency** | Valid Wavefront `.obj`/`.mtl` and binary glTF 2.0 `.glb` | Parsed by `validate_package.py` | Primary `.obj` (`334,410 B`), `.mtl` (`1,080 B`), `.glb` (`272,664 B`: `12B` hdr + `8B` + `20,988B` JSON + `8B` + `251,648B` BIN); Collision `.obj` (`7,733 B`), `.mtl` (`343 B`), `.glb` (`9,772 B`). | **PASS** |
| **Complete Package Inventory & Checksums** | `30` total files (`28` payload files in `MANIFEST.json` + `MANIFEST.json` + `SHA256SUMS.txt` with `29` checksum lines) | `validate_package.py --zip` + `sha256sum -c` + `unzip -t` on clean extraction | **`30` ZIP entries**, **`28` manifest payload entries**, **`29/29` SHA-256 checksums passed (`0` failed)** in clean `/tmp` extraction, `unzip -t` `No errors detected`, `0` missing/duplicate/unexpected files. | **PASS** |
| **Editable `.blend` Binary File** | Include `.blend` if Blender is installed; otherwise mark `NOT GENERATED — BLENDER UNAVAILABLE` | `which blender` check | `blender` executable is not installed in this Linux container. Runnable `bpy`/`bmesh` generator provided in `scripts/generate_mode_board_blender.py`. | **NOT APPLICABLE (`BLENDER UNAVAILABLE`)** |
| **Live Roblox Studio Import, Material, UI & Walkability Tests** | Test in live Studio if available; otherwise mark `NOT RUN` | Environment check | Roblox Studio is unavailable in this Linux container. Complete Luau scripts and manual verification steps provided in `ROBLOX_STUDIO_IMPORT_GUIDE.md`. | **NOT RUN** |
| **Owner Phase 2 Production Package Review** | Final owner sign-off on Phase 2 production package | Handoff review gate | Complete 30-file package verified and ready for owner review. | **REQUIRES OWNER REVIEW** |
| **Roblox Cloud Asset ID (`robloxAssetId`)** | Assign after importing and publishing in target experience | `manifest/SM_Hub_ModeBoard_01.manifest.json` | Remains `null` (`ASSET_PENDING`) until published in Roblox Studio. | **ASSET_PENDING** |
