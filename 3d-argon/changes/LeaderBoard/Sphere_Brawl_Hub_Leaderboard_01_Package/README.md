# `SM_Hub_Leaderboard_01` — Grand Three-Board Monument & Nine-Position Podium Array (Step 6, Phase 2 Production Package)

- **Project:** *Sphere Brawl: Rolling Rampage* (`HitanshG07/Sphere_Ball`, branch `3d_mesh`)
- **Canonical Asset ID:** `SM_Hub_Leaderboard_01`
- **Package Name:** `Sphere_Brawl_Hub_Leaderboard_01_Package` (`Sphere_Brawl_Hub_Leaderboard_01_Package.zip`)
- **Workspace Location:** `3d-argon/changes/8/Sphere_Brawl_Hub_Leaderboard_01_Package/`
- **Phase:** Step 6, Phase 2 — Final Production 3D Geometry, Exports & Delivery Package
- **Approved Concept Input:** `Sphere_Brawl_Hub_Leaderboard_Concept_06.zip` (`SHA-256: bb705ed9a35fca5ada4f0065f90db818010aafc85f00986946967323080f15e0`)
- **Preserved Earlier Concept Archives (Untouched):**
  - `Sphere_Brawl_Hub_Leaderboard_Concept_01.zip`: `5047fd853bc008457e3427fb4be7755cab328ec611b96b256eb22886875a96bb`
  - `Sphere_Brawl_Hub_Leaderboard_Concept_02.zip`: `41a1385c038faf7a240c417c82d5f0c717fd1e2908d8b7323d4bc41e4b0e4584`
  - `Sphere_Brawl_Hub_Leaderboard_Concept_03.zip`: `79241055955456209f5d4bcc892bcd66a50cbc0e5b434fb783495a37c2caabb7`
  - `Sphere_Brawl_Hub_Leaderboard_Concept_04.zip`: `6352a34ad31aa1407d80878661c8546f46f4da8da72d9067f1493ee3bdada6a0`
  - `Sphere_Brawl_Hub_Leaderboard_Concept_05.zip`: `d3952ef4e3f64b5034f3807c2f6e78134cc9425133292a9cd59f03c27d5896d1`
  - `Sphere_Brawl_Hub_Leaderboard_Concept_06.zip`: `bb705ed9a35fca5ada4f0065f90db818010aafc85f00986946967323080f15e0`
- **Engine & Scale Convention:** Roblox Studio (`1.0 Blender/Export Unit = 1.0 Roblox Stud`, `+Y` Up, `+Z` Front, `+X` Width Axis)
- **Blender `.blend` Source Status:** `NOT GENERATED — BLENDER UNAVAILABLE` (Blender is not installed in the sandbox VM; deterministic dual-mode Python/Blender source `scripts/generate_hub_leaderboard_blender.py` is provided and verified).
- **Live Roblox Studio Verification Status:** `NOT RUN` (Headless Linux VM without Roblox Studio GUI; full manual Studio import and verification protocol is provided in `ROBLOX_STUDIO_IMPORT_GUIDE.md`).

---

## 1. Executive Summary & Key Production Metrics

This package converts the owner-approved **Concept 06** design for `SM_Hub_Leaderboard_01` into a verified, production-ready 3D station asset for the Kinetic Hub at `(35, 150, -274)`.

| Property | Approved Concept 06 Target | Measured Production Value | Verification Label |
|---|---|---|---|
| **Overall Local Envelope (`W × H × D`)** | `42.0 × 26.0 × 9.0 studs` | **`42.0000 W × 26.0000 H × 9.0000 D studs`** | **MEASURED — PASS** |
| **Local X Span & Geometric Center** | `[-11.0, +31.0]` (`X_c = +10.0`) | **`[-11.0000, +31.0000] studs`** (`X_c = +10.0000`) | **MEASURED — PASS** |
| **Local Y Span** | `[0.0, +26.0]` | **`[0.0000, +26.0000] studs`** | **MEASURED — PASS** |
| **Local Z Span** | `[-4.2, +4.8]` | **`[-4.2000, +4.8000] studs`** | **MEASURED — PASS** |
| **Visual Triangle Count** | `< 2,000 triangles` (Concept: `1,996`) | **`1,852 triangles`** (`148` tris below `2,000` ceiling) | **MEASURED — PASS** |
| **Visual Vertex / Normal / UV Count** | Consistent across OBJ & GLB | **`5,556 vertices` / `1,852 normals` / `6 UVs`** | **MEASURED — PASS** |
| **Named Visual Components** | `53` components (`GEO_Leaderboard_*`) | **`53` named components** (`OBJ` groups & `GLB` child nodes) | **MEASURED — PASS** |
| **Leaderboard Display Modules** | `3` (`KOs`, `WINS`, `STANDINGS`) | **`3` independent `12.80 W` modules (`11.80 W` UI width)** | **MEASURED — PASS** |
| **Separate 3-Place Podium Stages** | `3` stages (`9` podium positions total) | **`3` separate `12.00 W × 4.35 D` stages (`A2,A1,A3`, `B2,B1,B3`, `C2,C1,C3`)** | **MEASURED — PASS** |
| **Replaceable UI-Ready Surfaces** | `15` (`3` headers + `3` tables + `9` nameplates) | **`15` separate flat `+Z` components (`0` baked text)** | **MEASURED — PASS** |
| **Static Player Avatars in Mesh** | `0` (runtime anchors only) | **`0` baked avatars** (`9` runtime `4.0000-stud` anchor specs documented) | **MEASURED — PASS** |
| **Collision Proxy (`COL_Leaderboard_Body`)** | Open above podiums & in walk-up zones | **`168 triangles` across `5` convex hull components** | **MEASURED — PASS** |
| **World Anchor & Inward Yaw** | `(35, 150, -274)`, `Yaw = -126.60707939°` | **`CFrame.new(35, 150, -274) * CFrame.Angles(0, math.rad(-126.60707939), 0)`** | **CALCULATED — PASS** |
| **Transformed World Vertex Bounds** | `X[13.7938, 44.8432], Y[150, 176], Z[-284.2912, -246.7044]` | **`X[13.7938, 44.8432], Y[150.0000, 176.0000], Z[-284.2912, -246.7044]`** | **MEASURED — PASS** |
| **Radial Span from Hub Center `(0,150,-300)`** | `[38.8377, 56.8872] studs` (`6.3128` inside curb) | **`R_hub in [38.8377, 56.8872] studs`** (`6.3128 studs` inside `R = 63.2` curb) | **MEASURED — PASS** |

---

## 2. Package Inventory (`30` Total Files: `28` Payload Files + `MANIFEST.json` + `SHA256SUMS.txt`)

- `README.md` — Package overview, key production metrics, world transform, and file inventory.
- `MODEL_SPECIFICATION.md` — Complete geometric, component, material, UI-surface, runtime avatar anchor, and collision proxy specifications.
- `ROBLOX_STUDIO_IMPORT_GUIDE.md` — Step-by-step Roblox Studio import, `Model:PivotTo` placement, material setup, `SurfaceGui` mounting, and runtime 4.0-stud avatar placement guide.
- `VALIDATION_REPORT.md` — Measured validation results across geometry, UVs, normals, exports, world bounds, neighbour clearances, and archive integrity.
- `INTEGRATION_REPORT.md` — Schema-verified `assets/asset-manifest.json` candidate entry (`hub.station.leaderboard`), expected hierarchy, and integration handoff notes.
- `MANIFEST.json` — Machine-readable package metadata and inventory of all `28` payload files with exact byte sizes and SHA-256 digests.
- `SHA256SUMS.txt` — Standard SHA-256 checksum file covering all `28` payload files plus `MANIFEST.json` (`29` entries).
- `meshes/SM_Hub_Leaderboard_01.obj` — Wavefront OBJ production visual mesh (`1,852` triangles, `5,556` vertices, `53` named objects).
- `meshes/SM_Hub_Leaderboard_01.mtl` — Wavefront MTL material library (`6` locked material slots referencing `SphereBrawl_Leaderboard_PaletteAtlas.png`).
- `meshes/SM_Hub_Leaderboard_01.glb` — Binary glTF 2.0 (`.glb`) production visual mesh (`348,236` bytes, root node `SM_Hub_Leaderboard_01` + `53` child mesh nodes).
- `meshes/SphereBrawl_Leaderboard_PaletteAtlas.png` — Local copy of the `64 × 64` sRGB PNG palette atlas alongside the OBJ/MTL export.
- `meshes/collision_proxy/COL_Leaderboard_Body.obj` — Wavefront OBJ collision proxy (`168` triangles across `5` hull components).
- `meshes/collision_proxy/COL_Leaderboard_Body.mtl` — Wavefront MTL material library for the collision proxy.
- `meshes/collision_proxy/COL_Leaderboard_Body.glb` — Binary glTF 2.0 (`.glb`) collision proxy (`32,484` bytes).
- `meshes/collision_proxy/SphereBrawl_Leaderboard_PaletteAtlas.png` — Local copy of the `64 × 64` palette atlas alongside the collision proxy MTL.
- `textures/SphereBrawl_Leaderboard_PaletteAtlas.png` — Canonical `64 × 64` sRGB PNG palette atlas (`<= 1024 × 1024` project texture limit).
- `scripts/generate_hub_leaderboard_blender.py` — Deterministic Python 3 / Blender 3.6+ / 4.x production mesh & collision proxy generator.
- `scripts/validate_package.py` — Standalone automated package, geometry, transform, UI-surface, clearance, and ZIP archive validator.
- `config/leaderboard_parameters.json` — Complete machine-readable coordinates, bounds, component metrics, 15 UI surface specs, and 9 avatar anchor specs.
- `manifest/SM_Hub_Leaderboard_01.manifest.json` — Standalone schema-compliant `assets/asset-manifest.json` entry (`hub.station.leaderboard`).
- `previews/01_Production_Monument_Approach_ThreeQuarter.png` — Clean shaded 3/4 player-approach beauty render (`2400 × 1350`, zero wireframe overlay).
- `previews/02_Production_Direct_Front_Elevation.png` — True 1:1 orthographic front elevation (`42.0000 W × 26.0000 H studs`).
- `previews/03_Production_Side_Orthographic.png` — Orthographic side profile and `9.0000-stud` depth / avatar clearance proof.
- `previews/04_Production_Rear_Structural_View.png` — Clean shaded rear structural elevation and 3/4 views (`-Z` backplane, piers, clamps, stabilizers, spines).
- `previews/05_Production_TopDown_Footprint_Clearance.png` — Top-down footprint and Kinetic Hub radial/neighbour clearance map.
- `previews/06_Production_Neutral_Clay_AvatarScale.png` — Monochromatic matte clay form readability and `5.5-stud` vs `4.0-stud` avatar scale study.
- `previews/07_Production_Hub_Integration.png` — Full Kinetic Hub plaza integration render at `(35, 150, -274)` facing `(0, 150, -300)`.
- `previews/08_Production_Three_Board_UI.png` — Three-board UI surface proof (`SESSION KOs` Cyan, `SESSION WINS` Amber, `SESSION STANDINGS` Magnetic Purple).
- `previews/09_Production_Nine_Podium_UI_Surface_Proof.png` — Nine-podium and 15 replaceable UI-ready surface proof (bare production geometry vs runtime presentation).
- `previews/10_Production_Technical_Component_And_Collision_Overview.png` — Isolated technical wireframe (`1,852` tris) and collision proxy (`168` tris) verification sheet.
