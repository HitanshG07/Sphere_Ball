# Sphere Brawl: Rolling Rampage — Mode Selection Board Production Package (`SM_Hub_ModeBoard_01`)

- **Canonical Asset ID:** `SM_Hub_ModeBoard_01`
- **Descriptive Name:** Tactical Arena Mode Selection Command Gantry (`14.4000 (W) × 3.8000 (D) × 8.8000 (H) studs`)
- **Stage:** Step 5, Phase 2 — Final Production Mesh & Delivery Package
- **Package Directory:** `3d-argon/changes/7/Sphere_Brawl_Hub_ModeBoard_01_Package/`
- **Archive Name:** `Sphere_Brawl_Hub_ModeBoard_01_Package.zip`
- **Approved Phase 1 Concept Reference:** `Sphere_Brawl_Hub_ModeBoard_Concept_01.zip` (`SHA-256: e76c211dd44fc5c36d71a546ef8e683de05923e8ee142e203173caabeeaddeb6`, confirmed identical prior to Phase 2 production)
- **Editable `.blend` Source Status:** `NOT GENERATED — BLENDER UNAVAILABLE` (deterministic dual-mode Python / `bpy` generator script provided at `scripts/generate_mode_board_blender.py`)
- **Live Roblox Studio Verification Status:** `NOT RUN` (headless Linux container; exact Luau placement, material, collider proxy, and `SurfaceGui` adornee scripts provided in `ROBLOX_STUDIO_IMPORT_GUIDE.md`)

---

## 1. Production Mesh Summary & Exact Placement Transform

- **Measured Primary Visual Mesh (`meshes/SM_Hub_ModeBoard_01.obj`, `.mtl`, `.glb`):**
  - **`1,612 triangles`** (`4,836 vertices`, `1,612` outward face normals, `5` palette UVs) across **`18` named components** (`GEO_ModeBoard_*`) — **`888 triangles` (`35.52%`) below the Master 3D Art Bible's `< 2,500` triangle station budget**.
  - **`0` degenerate faces** (`min_area = 0.001060 sq. studs`), **`0` normal mismatches**, **`0` cross-component coplanar Z-fighting overlaps**, and a sealed base underside at `Local Y = 0.0000`.
- **Optional Simplified Collision Proxy (`meshes/collision_proxy/COL_ModeBoard_Body.obj`, `.mtl`, `.glb`):**
  - **`36 triangles`** (`108 vertices`) across `3` clean box hulls (`COL_ModeBoard_BaseHull`, `COL_ModeBoard_MainGantryHull`, `COL_ModeBoard_CanopyHull`), blocking the station core while leaving the front walk-up approach (`Local Z > +1.5200`) 100% open.
- **Measured Local & Transformed World Bounds:**
  - **Local Bounds (`Pivot = (0, 0, 0)` at bottom footprint center):** `X in [-7.2000, +7.2000]` (`14.4000 studs`), `Y in [0.0000, +8.8000]` (`8.8000 studs`), `Z in [-1.9000, +1.9000]` (`3.8000 studs`).
  - **Authoritative World Placement Transform (`(35, 150, -326)`, `θ_yaw = -53.39292061°`):**
    ```luau
    local targetCFrame =
        CFrame.new(35, 150, -326)
        * CFrame.Angles(0, math.rad(-53.39292061), 0)
    ```
  - **Verified World FrontVector:** **`(-0.802744, 0.000000, +0.596324)`** (pointing radially inward toward Hub center `(0, 150, -300)`).
  - **Measured Transformed World AABB:** `World X in [29.3702, 40.6298]` (`11.2595 studs`), `World Y in [150.0000, 158.8000]` (`8.8000 studs`), `World Z in [-332.6738, -319.3320]` (`13.3418 studs`).
  - **Measured Vertex Radial Span:** **`R_vertex in [41.7610, 46.0024] studs`** (`100%` inside the approved `R = 37.0..52.5 stud` Peripheral Station Plaza Ring on `SM_Hub_PlazaPlatform_01`).
- **Five Separate UI-Ready Replaceable Panel Surfaces (Zero Baked Text):**
  1. `GEO_ModeBoard_UIPanel_01_FFA` (`4.0800 W × 3.7800 H studs`, `14.0°` tilt — `FREE-FOR-ALL — ACTIVE`)
  2. `GEO_ModeBoard_UIPanel_02_Duel` (`5.0400 W × 1.2000 H studs`, `14.0°` tilt — `DUEL — COMING SOON`)
  3. `GEO_ModeBoard_UIPanel_03_TeamClash` (`5.0400 W × 1.2000 H studs`, `14.0°` tilt — `TEAM CLASH — COMING SOON`)
  4. `GEO_ModeBoard_UIPanel_04_KingTile` (`5.0400 W × 1.2000 H studs`, `14.0°` tilt — `KING TILE — COMING SOON`)
  5. `GEO_ModeBoard_HeaderSign` (`11.4800 W × 0.8200 H studs`, `0.0°` upright — `ARENA MODE SELECT`)

---

## 2. Complete 30-File Package Inventory

| # | Relative Path in Package | Category | Description |
|---:|---|---|---|
| 1 | `README.md` | Documentation | Package overview, production summary, transform contract, and 30-file inventory |
| 2 | `MODEL_SPECIFICATION.md` | Documentation | Complete geometry specification, 18-component table, 5 UI-panel transforms, and material/export breakdown |
| 3 | `ROBLOX_STUDIO_IMPORT_GUIDE.md` | Documentation | Step-by-step Studio import settings, `PivotTo` calibration, material script, collision proxy, and `SurfaceGui` adornee setup |
| 4 | `VALIDATION_REPORT.md` | Documentation | Full technical validation matrix (`PASS` / `NOT RUN` / `NOT APPLICABLE` / `REQUIRES OWNER REVIEW` / `ASSET_PENDING`) |
| 5 | `INTEGRATION_REPORT.md` | Documentation | Schema-verified `assets/asset-manifest.json` entry, measured neighbour clearances, and integration handoff |
| 6 | `MANIFEST.json` | Package Manifest | Machine-readable inventory of all 28 payload files with exact byte sizes, SHA-256 hashes, and geometry metadata |
| 7 | `SHA256SUMS.txt` | Checksums | Standard `sha256sum -c` checksum file covering all 28 payload files + `MANIFEST.json` (`29` total lines) |
| 8 | `config/mode_board_parameters.json` | Config | Machine-readable transform, UI-panel coordinates, palette metadata, and measured mesh metrics |
| 9 | `manifest/SM_Hub_ModeBoard_01.manifest.json` | Asset Manifest | Ready-to-merge JSON entry conforming to `specs/ASSET_MANIFEST.schema.json` |
| 10 | `meshes/SM_Hub_ModeBoard_01.obj` | Primary Mesh | Wavefront OBJ (`1,612` triangles, `4,836` vertices, `18` `o GEO_ModeBoard_*` objects) |
| 11 | `meshes/SM_Hub_ModeBoard_01.mtl` | Primary Material | Wavefront MTL defining the 5 locked Kinetic Grid materials (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`, `EMI_Amber`) |
| 12 | `meshes/SM_Hub_ModeBoard_01.glb` | Primary GLB | Binary glTF 2.0 (`272,664 bytes`, `19` nodes = root + `18` child meshes, `5` PBR materials, embedded `64×64` atlas) |
| 13 | `meshes/SphereBrawl_ModeBoard_PaletteAtlas.png` | Mesh Texture | `64×64` PNG swatch atlas (`176 bytes`) co-located with `.mtl` |
| 14 | `meshes/collision_proxy/COL_ModeBoard_Body.obj` | Collision Proxy | Optional simplified 3-hull box collision proxy Wavefront OBJ (`36` triangles, `108` vertices) |
| 15 | `meshes/collision_proxy/COL_ModeBoard_Body.mtl` | Collision Proxy | Wavefront MTL for `COL_ModeBoard_Body.obj` |
| 16 | `meshes/collision_proxy/COL_ModeBoard_Body.glb` | Collision Proxy | Binary glTF 2.0 collision proxy (`9,772 bytes`, `36` triangles) |
| 17 | `meshes/collision_proxy/SphereBrawl_ModeBoard_PaletteAtlas.png` | Collision Texture | `64×64` PNG swatch atlas co-located with collision proxy `.mtl` |
| 18 | `textures/SphereBrawl_ModeBoard_PaletteAtlas.png` | Texture Atlas | Canonical copy of the `64×64` sRGB palette swatch atlas (`176 bytes`) |
| 19 | `scripts/generate_mode_board_blender.py` | Generator Script | Deterministic Python 3 & Blender 3.6+/4.x (`bpy`/`bmesh`) production mesh generator |
| 20 | `scripts/validate_package.py` | Validator Script | Automated package inventory, SHA-256, transform basis, UI-panel, and mesh/GLB audit tool |
| 21 | `previews/01_Production_Player_Approach_ThreeQuarter.png` | Production Preview 1 | Player-height (`Y = 4.8 studs`) three-quarter approach views & close walk-up view (clean shaded) |
| 22 | `previews/02_Production_Direct_Front_Elevation.png` | Production Preview 2 | Direct front orthographic & perspective elevations showing all 4 mode locations & hierarchy |
| 23 | `previews/03_Production_Side_Orthographic.png` | Production Preview 3 | Left/right side orthographic elevations (`3.80-stud` depth, `14.0°` tilt, floor `Y = 150.0000`) |
| 24 | `previews/04_Production_Rear_Structural_View.png` | Production Preview 4 | Rear-quarter, direct rear, and low underside views showing 3 diagonal spine ribs & sealed base |
| 25 | `previews/05_Production_TopDown_Footprint.png` | Production Preview 5 | Top-down 3D render (`14.40 × 3.80 studs`) and measured world vertex clearance blueprint |
| 26 | `previews/06_Production_Neutral_Clay.png` | Production Preview 6 | Pure neutral-clay evaluation & 1:1 station family comparison (Customize, ModeBoard, ShopBar, Leaderboard) |
| 27 | `previews/07_Production_Hub_Integration.png` | Production Preview 7 | Full Kinetic Hub integration at `(35, 150, -326)` `Yaw = -53.3929°` with all approved Hub stations |
| 28 | `previews/08_Production_ModeState_CloseUp.png` | Production Preview 8 | High-resolution close-up of Active Free-for-All hero bay vs. recessed Coming Soon bays |
| 29 | `previews/09_Production_UI_Panel_Surface_Proof.png` | Production Preview 9 | Dedicated proof that all 5 display surfaces are separate flat replaceable components with 0 baked text |
| 30 | `previews/10_Production_Technical_Component_Overview.png` | Production Preview 10 | Color-coded 18-component map, isolated technical wireframe (`1,612` tris), and `36`-tri collision proxy overlay |

*(Note: Rows 1–30 above correspond to the 30 total files in the package: 28 payload files + `MANIFEST.json` + `SHA256SUMS.txt`.)*
