# Production Validation Report — `SM_Hub_Leaderboard_01` (`Sphere_Brawl_Hub_Leaderboard_01_Package`)

- **Canonical Asset ID:** `SM_Hub_Leaderboard_01`
- **Approved Concept Input:** `Sphere_Brawl_Hub_Leaderboard_Concept_06.zip` (`SHA-256: bb705ed9a35fca5ada4f0065f90db818010aafc85f00986946967323080f15e0` — **VERIFIED**)
- **Preserved Earlier Concept Archives:** Concepts 01–06 verified untouched on disk.
- **Blender `.blend` Source Status:** `NOT GENERATED — BLENDER UNAVAILABLE`
- **Live Roblox Studio Verification Status:** `NOT RUN` (Headless Linux container without Roblox Studio GUI)

---

## 1. Automated Geometry, Export, Material & UI-Surface Validation Matrix

All checks below were executed against the actual exported files on disk and inside a clean temporary extraction of `Sphere_Brawl_Hub_Leaderboard_01_Package.zip`:

| Validation Gate | Target / Specification | Measured Result | Label / Verdict |
|---|---|---|---|
| **Primary Visual Exports Existence** | `meshes/SM_Hub_Leaderboard_01.obj`, `.mtl`, `.glb` | Present (`353,730 B`, `1,548 B`, `348,236 B`) | **MEASURED — PASS** |
| **Collision Proxy Exports Existence** | `meshes/collision_proxy/COL_Leaderboard_Body.obj`, `.mtl`, `.glb` | Present (`31,829 B`, `390 B`, `32,484 B`) | **MEASURED — PASS** |
| **Palette Texture Atlas Existence** | `textures/SphereBrawl_Leaderboard_PaletteAtlas.png` (`<= 1024×1024`) | Present (`64 × 64` sRGB PNG, `343 B`, SHA-256 `29999357...`) | **MEASURED — PASS** |
| **OBJ/MTL Material Consistency** | `mtllib SM_Hub_Leaderboard_01.mtl`; `6` locked palette slots | `6` `newmtl` definitions matching `usemtl` tags 1:1 | **MEASURED — PASS** |
| **GLB Binary & Node Structure** | glTF 2.0 binary (`0x46546C67`, version `2`), root + `53` child nodes | Valid header, `54` total nodes (`SM_Hub_Leaderboard_01` + `53` meshes) | **MEASURED — PASS** |
| **Visual Triangle Budget** | `< 2,000` triangles (Concept 06 blockout: `1,996`) | **`1,852 triangles`** (`148` triangles below `2,000` ceiling) | **MEASURED — PASS** |
| **Visual Vertices / Normals / UVs** | Consistent across OBJ & GLB | **`5,556` vertices / `1,852` normals / `6` UVs** | **MEASURED — PASS** |
| **Geometry Degeneracy Check** | `0` zero-area or sliver triangles | **`0` degenerate faces** (`min_triangle_area = 0.00400 sq studs`) | **MEASURED — PASS** |
| **Normal & Winding Consistency** | Outward right-handed CCW normals; top caps `+Y`, bottom caps `-Y` | **`0` normal mismatches** (`100%` of face normals match cross-product) | **MEASURED — PASS** |
| **Cross-Component Coplanar Check** | `0` coplanar Z-fighting overlaps across components | **`0` cross-component coplanar overlaps** | **MEASURED — PASS** |
| **Named Component Count** | `53` named `GEO_Leaderboard_*` components | **`53` named components** verified in OBJ & GLB | **MEASURED — PASS** |
| **Three Themed Leaderboard Modules** | `Display A` (`EMI_Cyan`), `Display B` (`EMI_Amber`), `Display C` (`EMI_Magnetic`) | All `3` modules (`12.80 W` housing, `11.80 W` UI width) verified | **MEASURED — PASS** |
| **Three Separate Podium Stages (`9` Podiums)** | `Stage A` (`A2,A1,A3`), `Stage B` (`B2,B1,B3`), `Stage C` (`C2,C1,C3`) | `3` separate `12.00 W × 4.20 D` stages with `1.70-stud` gaps & `9` podiums | **MEASURED — PASS** |
| **All 15 Replaceable UI-Ready Surfaces** | `3` headers + `3` main tables + `9` podium nameplates (`0` baked text) | **`15` separate components**, each with `2` flat `+Z` (`0,0,1`) front tris | **MEASURED — PASS** |
| **Static Player Avatars in Mesh** | `0` baked avatars in production mesh | **`0` avatar triangles** in `SM_Hub_Leaderboard_01.obj` / `.glb` | **MEASURED — PASS** |
| **Collision Proxy (`COL_Leaderboard_Body`)** | Open above podium tops (`Y > 2.50`) & in `1.70-stud` walkways | **`168` triangles across `5` hulls**; max foreground `Y = 2.5000` | **MEASURED — PASS** |

---

## 2. Spatial Bounds, World Transform & Neighbour Clearance Audit

| Spatial Check | Measured / Calculated Value | Evidence Label | Verdict |
|---|---|---|---|
| **Local Bounding Box (`SM_Hub_Leaderboard_01`)** | `X in [-11.0000, +31.0000]` (`42.0000 W`, `X_c = +10.0000`), `Y in [0.0000, +26.0000]` (`26.0000 H`), `Z in [-4.2000, +4.8000]` (`9.0000 D`) | **MEASURED** | **PASS** |
| **World Placement Transform** | `CFrame.new(35, 150, -274) * CFrame.Angles(0, math.rad(-126.60707939), 0)` (`Forward +Z_local = (-0.80274385, 0, -0.59632400)`) | **CALCULATED** | **PASS** |
| **Transformed World Vertex Bounds** | `X in [13.7938, 44.8432]` (`31.0494`), `Y in [150.0000, 176.0000]` (`26.0000`), `Z in [-284.2912, -246.7044]` (`37.5868`) | **MEASURED** | **PASS** |
| **Radial Span from Hub Center `(0,150,-300)`** | **`R_hub in [38.8377, 56.8872] studs`** (extends `4.3872 studs` past nominal `R = 52.5` band on outer Starboard rear corner; **`6.3128 studs` inside** `R = 63.2` outer plaza curb) | **MEASURED** | **PASS** |
| **Clearance to `SM_Hub_ShopKiosk_01`** | **`7.2474 studs`** min vertex XZ distance (`5.9254` vertex-to-AABB, `5.7088` AABB-to-AABB) at package placement `(43, 150, -300)`; **`5.8700 studs`** 2D polygon gap (`5.7340` vertex XZ, `5.7088` AABB) at legacy `(35, 150, -300)` | **MEASURED** | **PASS** |
| **Clearance to `SM_Hub_ModeBoard_01`** | **`35.0413 studs`** min vertex XZ distance (`35.0408` AABB-to-AABB) to approved package placement `(35, 150, -326)` (`Yaw = -53.3929°`); **`9.0858 studs`** min vertex XZ (`8.8510` vertex-to-AABB, `8.57` to `15×4` blockout) to North `(0, 150, -245)` | **MEASURED** | **PASS** |
| **Clearance to `SM_Hub_QueuePadRing_01` (`R = 14.0`)** | **`24.8377 studs`** radial edge-to-edge clearance (`38.8377 - 14.0000`) | **MEASURED** | **PASS** |
| **Clearance to Main Spawn Sightline (`X = 0`)** | **`13.7938 studs`** lateral X clearance (`10.7938 studs` from `6-stud` corridor) | **MEASURED** | **PASS** |
| **Walk-Up Area for 9 Podiums & Plaza Deck Grounding** | All static base vertices grounded flush on `World Y = 150.0000`; `24.8377-stud` open front plaza apron plus two `1.7000-stud` inter-stage walkways | **MEASURED** | **PASS** |

---

## 3. Package Inventory, Checksum & Clean-Extraction Verification

- **Total Package Files:** **`30`** (`28` payload files described in `MANIFEST.json` + `MANIFEST.json` + `SHA256SUMS.txt`).
- **All 10 Production Previews Under `previews/`:** `01_Production_Monument_Approach_ThreeQuarter.png` through `10_Production_Technical_Component_And_Collision_Overview.png` (`0` PNGs at package root).
- **Archive Integrity (`unzip -t`):** `No errors detected in compressed data of Sphere_Brawl_Hub_Leaderboard_01_Package.zip` (**PASS**).
- **Clean Temp Extraction & `sha256sum -c SHA256SUMS.txt`:** All `29` checksummed entries (`28` payload files + `MANIFEST.json`) verified `OK` (**PASS**).
- **Standalone Validator (`scripts/validate_package.py --zip ...`):** `status: PASS`, `errors: []` (**PASS**).

---

## 4. Live Roblox Studio Tests (`NOT RUN`)

The following interactive engine checks were **not executed** in this Linux build environment and are documented for manual execution in `ROBLOX_STUDIO_IMPORT_GUIDE.md` §6:
- Live Roblox Studio GLB/OBJ import and `Model:PivotTo` visual check (`NOT RUN`)
- Live `MeshPart` `Metal` / `Neon` lighting appearance (`NOT RUN`)
- Live `SurfaceGui` attachment and text rendering on the 15 surfaces (`NOT RUN`)
- Live runtime 4.0-stud avatar spawning on the 9 podiums (`NOT RUN`)
- Live R15 character walkability around the 3 podium stages and `SM_Hub_ShopKiosk_01` corridor (`NOT RUN`)
