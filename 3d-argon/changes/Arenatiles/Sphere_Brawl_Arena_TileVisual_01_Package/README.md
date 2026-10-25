# `SM_Arena_TileVisual_01` — Phase 2 Final Production Asset Package

| Property | Value |
| :--- | :--- |
| **Project** | *Sphere Brawl: Rolling Rampage* |
| **Repository & Branch** | `HitanshG07/Sphere_Ball` (`3d_mesh`) |
| **Canonical Asset ID** | `SM_Arena_TileVisual_01` |
| **Asset Type** | Reusable 3D arena visual floor tile system (`Variant A` & `Variant B`) + 8 modular non-colliding hazard overlays |
| **Production Status** | **PHASE 2 FINAL PRODUCTION ASSET PACKAGE — GEOMETRY, BUDGETS & EXPORTS VALIDATED** |
| **Approved Concept Baseline** | `Sphere_Brawl_Arena_TileVisual_Concept_01.zip` (`SHA-256: fe40cd09419b86b915a896c90d37b3ea8978e0607bb4171c0a13bbc3b1b714d7`) |
| **Repository Handoff Location** | `3d-argon/changes/9/Sphere_Brawl_Arena_TileVisual_01_Package/` |
| **Scale Convention** | `1 Blender unit = 1.0 Roblox stud` |
| **Locked Grid Architecture** | `9 × 9 cells` (`81` initial cells), integer coordinates `X, Z in [-4, +4]`, `12.0000-stud` center-to-center pitch |
| **Grid Centre (`ArenaCFrame`)** | `(0.0000, 50.0000, 0.0000)`; Top rolling surface at `World Y = 51.0000` |
| **Authoritative Collision Tile** | `12.0000 × 2.0000 × 12.0000 studs` (`CanCollide = true`, `Transparency = 1`, seamless edge-to-edge; **NOT** in visual exports) |
| **Production Base Visual Tile** | `11.8000 × 2.0000 × 11.8000 studs` (`CanCollide = false`, `CanTouch = false`, `0.2000-stud` visible inter-tile groove) |
| **Local Origin** | `(0.0000, 0.0000, 0.0000)` at geometric center of the `11.8 × 2.0 × 11.8` visual tile (`Top Face Local Y = +1.0000`) |
| **Base Tile Triangle Count** | **`152 triangles` (`456 vertices`)** across `5` named components (strictly `<= 170` Phase 2 base target) |
| **Combined Per-Cell State Budget** | **`152 to 224 triangles`** across all allowed visual states (every single state strictly `<= 249` triangles!) |
| **Shared Palette Texture Atlas** | `textures/T_Arena_TilePalette_256.png` (`256 × 256 px <= 1024 × 1024`, `933` bytes, `SHA-256: 3ab02901089d986685060313261da32d2f121c31979bb4b996dd41a3685f6e06`) |
| **Editable `.blend` Source Status** | **`NOT GENERATED — BLENDER UNAVAILABLE`** (Deterministic generator `scripts/generate_arena_tile_blender.py` included and verified) |

## 1. Executive Summary & Phase 2 Budget Correction

This package delivers the final production 3D mesh assets (`.obj`, `.mtl`, `.glb`), compact palette texture atlas, deterministic Python/Blender generator, automated package validator, 10 high-resolution production preview renders, and technical integration documentation for **`SM_Arena_TileVisual_01`**.

### Phase 1 -> Phase 2 Triangle Budget Correction
In Phase 1, the concept base tile used `196 triangles`, which caused the **Magnetic Storm Anchor (`196 + 72 = 268 tris`)** and **Magnetic Storm Warning (`196 + 56 = 252 tris`)** states to exceed the strict `< 250` (`<= 249`) per-cell combined visual triangle cap.
In **Phase 2**, the base tile topology was streamlined from `196` to **`152 triangles` (`456 vertices`)** by merging the inner perimeter collar step directly into the recessed cyan circuit channel (`COMP_Arena_TileBevelFrame_118`: `70 tris`), removing micro corner tie-lugs (`GEO_Tile_CornerTrimLock_04`: `16 tris`), and simplifying the underside structural ribs into two clean cross-beams (`GEO_Tile_UndersideRibs`: `20 tris`).
As a result:
- **Base Tile (`Variant A` & `Variant B`):** **`152 triangles`** (18 triangles below the `<= 170` base target).
- **Most Complex Combined Cell State (`Base + OVL_Arena_Active_MagneticAnchor`):** **`152 + 72 = 224 triangles`** (`25 triangles` below the `<= 249` hard ceiling).
- **Every single allowed cell state (`Safe`, `Warn_Ice`, `Active_Ice`, `Warn_Magnetic`, `Active_MagneticAnchor`, `Active_MagneticField`, `Warn_Boost`, `Active_Boost`, `Collapse_Warn`) stays strictly within `152..224 triangles` (`<= 249`).**

## 2. Locked Grid Pitch, Coordinate Convention & Checkerboard Variants

- **World Centre Calculation (Applied Once):**
  ```luau
  local tileCenter = (ArenaCFrame * CFrame.new(12 * x, 0, 12 * z)).Position
  ```
  where `ArenaCFrame = CFrame.new(0, 50, 0)` and integer `x, z in (-4, -3, -2, -1, 0, 1, 2, 3, 4)`.
- **Ring Index Formula:** `D = max(abs(x), abs(z))` (`D=4` outer ring has `32` cells -> `49` remain; `D=3` ring has `24` cells -> `25` remain).
- **Checkerboard Material Variants (`Variant A` vs. `Variant B`):**
  - `meshes/SM_Arena_TileVisual_01_VariantA.{obj,mtl,glb}` (**Even Parity `(x + z) % 2 == 0`**, `41` cells on the `9 × 9` board): `MAT_DarkNeutral` (`#202636`) outer bevel frame & body; `MAT_AltNeutral` (`#2A3246`) center deck & underside ribs.
  - `meshes/SM_Arena_TileVisual_01_VariantB.{obj,mtl,glb}` (**Odd Parity `(x + z) % 2 != 0`**, `40` cells on the `9 × 9` board): `MAT_AltNeutral` (`#2A3246`) outer bevel frame & body; `MAT_DarkNeutral` (`#202636`) center deck & underside ribs.
  - Both variants have **100% identical vertex coordinates (`456` vertices), face indices (`152` triangles), origin `(0, 0, 0)`, and bounding box (`[-5.9, -1.0, -5.9]` to `[+5.9, +1.0, +5.9]`)**.

## 3. Production Mesh & Hazard-Overlay Index (`meshes/`)

| Asset Name | Relative Paths (`.obj`, `.mtl`, `.glb`) | Local Bounds (`X × Y × Z`) | Triangles / Vertices | Combined Cell Triangles (`Base + Overlay`) |
| :--- | :--- | :--- | :--- | :--- |
| **`SM_Arena_TileVisual_01_VariantA`** | `meshes/SM_Arena_TileVisual_01_VariantA.{obj,mtl,glb}` | `[-5.9, +5.9] × [-1.0, +1.0] × [-5.9, +5.9]` (`11.8 × 2.0 × 11.8`) | **152 tris / 456 verts** | **152 / 249 (`PASS`)** |
| **`SM_Arena_TileVisual_01_VariantB`** | `meshes/SM_Arena_TileVisual_01_VariantB.{obj,mtl,glb}` | `[-5.9, +5.9] × [-1.0, +1.0] × [-5.9, +5.9]` (`11.8 × 2.0 × 11.8`) | **152 tris / 456 verts** | **152 / 249 (`PASS`)** |
| **`OVL_Arena_Warn_Ice`** | `meshes/overlays/OVL_Arena_Warn_Ice.{obj,mtl,glb}` | `[-5.7, +5.7] × [+1.00, +1.05] × [-5.7, +5.7]` (`11.4 × 0.05 × 11.4`) | **38 tris / 114 verts** | **190 / 249 (`PASS`)** |
| **`OVL_Arena_Active_Ice`** | `meshes/overlays/OVL_Arena_Active_Ice.{obj,mtl,glb}` | `[-5.7, +5.7] × [+1.00, +1.05] × [-5.7, +5.7]` (`11.4 × 0.05 × 11.4`) | **38 tris / 114 verts** | **190 / 249 (`PASS`)** |
| **`OVL_Arena_Warn_Magnetic`** | `meshes/overlays/OVL_Arena_Warn_Magnetic.{obj,mtl,glb}` | `[-5.7, +5.7] × [+1.00, +1.05] × [-5.7, +5.7]` (`11.4 × 0.05 × 11.4`) | **56 tris / 168 verts** | **208 / 249 (`PASS`)** |
| **`OVL_Arena_Active_MagneticAnchor`** | `meshes/overlays/OVL_Arena_Active_MagneticAnchor.{obj,mtl,glb}` | `[-5.7, +5.7] × [+1.00, +1.05] × [-5.7, +5.7]` (`11.4 × 0.05 × 11.4`) | **72 tris / 216 verts** | **224 / 249 (`PASS`)** |
| **`OVL_Arena_Active_MagneticField`** | `meshes/overlays/OVL_Arena_Active_MagneticField.{obj,mtl,glb}` | `[-5.7, +5.7] × [+1.00, +1.05] × [-5.7, +5.7]` (`11.4 × 0.05 × 11.4`) | **42 tris / 126 verts** | **194 / 249 (`PASS`)** |
| **`OVL_Arena_Warn_Boost`** | `meshes/overlays/OVL_Arena_Warn_Boost.{obj,mtl,glb}` | `[-5.7, +5.7] × [+1.00, +1.05] × [-5.7, +5.7]` (`11.4 × 0.05 × 11.4`) | **34 tris / 102 verts** | **186 / 249 (`PASS`)** |
| **`OVL_Arena_Active_Boost`** | `meshes/overlays/OVL_Arena_Active_Boost.{obj,mtl,glb}` | `[-5.7, +5.7] × [+1.00, +1.05] × [-5.7, +5.7]` (`11.4 × 0.05 × 11.4`) | **36 tris / 108 verts** | **188 / 249 (`PASS`)** |
| **`OVL_Arena_Collapse_Warn`** | `meshes/overlays/OVL_Arena_Collapse_Warn.{obj,mtl,glb}` | `[-5.7, +5.7] × [+1.00, +1.05] × [-5.7, +5.7]` (`11.4 × 0.05 × 11.4`) | **32 tris / 96 verts** | **184 / 249 (`PASS`)** |

## 4. Production Preview Index (`previews/`)

All 10 preview images (`2400 × 1350` PNG) are rendered directly from the actual exported production `.obj` meshes:
1. `previews/01_Production_Safe_Tile_ThreeQuarter.png` — Variant A & Variant B 3/4 shaded beauty views, Neutral-Clay view, underside `152-tri` wireframe, and production spec summary.
2. `previews/02_Production_Checkerboard_3x3_Patch.png` — `3 × 3` checkerboard grid patch (`36 × 36 studs`) at gameplay camera distance with `6.0-stud` sphere, top orthographic groove rhythm, and 4-corner seam roll clearance.
3. `previews/03_Production_Tile_Orthographic_Dimensions.png` — Top, Front (`+Z`), and Side (`+X` wireframe) elevations plus two-cell engineering cross-section and separation contract.
4. `previews/04_Production_SixState_Overview.png` — Side-by-side 3/4 and top-down silhouette comparison of all 6 required visual states with verified `<= 249` combined triangle counts.
5. `previews/05_Production_IceCorridor_Warning_Active.png` — `OVL_Arena_Warn_Ice` (`38 tris`) and `OVL_Arena_Active_Ice` (`38 tris`, `190` combined) single-tile and `3 × 3` corridor views.
6. `previews/06_Production_MagneticStorm_Warning_Active.png` — `OVL_Arena_Warn_Magnetic` (`56 tris`, `208` combined), `OVL_Arena_Active_MagneticAnchor` (`72 tris`, `224` combined), and `OVL_Arena_Active_MagneticField` (`42 tris`, `194` combined).
7. `previews/07_Production_BoostRunway_Warning_Active.png` — `OVL_Arena_Warn_Boost` (`34 tris`, `186` combined) and `OVL_Arena_Active_Boost` (`36 tris`, `188` combined) with side orthographic flat-profile proof.
8. `previews/08_Production_RingCollapse_Warning_Sink.png` — `OVL_Arena_Collapse_Warn` (`32 tris`, `184` combined) 4-stage collapse sequence, perimeter cutaway, and `9 × 9` ring index map (`D=4` & `D=3`).
9. `previews/09_Production_Arena_9x9_Overview.png` — Full `9 × 9` (`81`-cell) demonstration board (`12,312` base triangles across `41` Variant A + `40` Variant B instances) and complete per-state triangle budget proof table.
10. `previews/10_Production_Component_And_Collision_Separation.png` — Exploded 3-layer separation diagram (`CollisionTile` vs. `SM_Arena_TileVisual_01` vs. `OVL_Arena_*`), isolated technical wireframe (`224 tris` worst-case), 5-component breakdown, `256 × 256` palette atlas swatches, and all 8 overlay wireframes.

## 5. Package Inventory

```text
Sphere_Brawl_Arena_TileVisual_01_Package/
├── README.md
├── MODEL_SPECIFICATION.md
├── ROBLOX_STUDIO_IMPORT_GUIDE.md
├── VALIDATION_REPORT.md
├── INTEGRATION_REPORT.md
├── MANIFEST.json
├── SHA256SUMS.txt
├── meshes/
│   ├── SM_Arena_TileVisual_01_VariantA.obj
│   ├── SM_Arena_TileVisual_01_VariantA.mtl
│   ├── SM_Arena_TileVisual_01_VariantA.glb
│   ├── SM_Arena_TileVisual_01_VariantB.obj
│   ├── SM_Arena_TileVisual_01_VariantB.mtl
│   ├── SM_Arena_TileVisual_01_VariantB.glb
│   └── overlays/
│       ├── OVL_Arena_Warn_Ice.{obj,mtl,glb}
│       ├── OVL_Arena_Active_Ice.{obj,mtl,glb}
│       ├── OVL_Arena_Warn_Magnetic.{obj,mtl,glb}
│       ├── OVL_Arena_Active_MagneticAnchor.{obj,mtl,glb}
│       ├── OVL_Arena_Active_MagneticField.{obj,mtl,glb}
│       ├── OVL_Arena_Warn_Boost.{obj,mtl,glb}
│       ├── OVL_Arena_Active_Boost.{obj,mtl,glb}
│       └── OVL_Arena_Collapse_Warn.{obj,mtl,glb}
├── scripts/
│   ├── generate_arena_tile_blender.py
│   └── validate_package.py
├── textures/
│   └── T_Arena_TilePalette_256.png
└── previews/
    ├── 01_Production_Safe_Tile_ThreeQuarter.png
    ├── 02_Production_Checkerboard_3x3_Patch.png
    ├── 03_Production_Tile_Orthographic_Dimensions.png
    ├── 04_Production_SixState_Overview.png
    ├── 05_Production_IceCorridor_Warning_Active.png
    ├── 06_Production_MagneticStorm_Warning_Active.png
    ├── 07_Production_BoostRunway_Warning_Active.png
    ├── 08_Production_RingCollapse_Warning_Sink.png
    ├── 09_Production_Arena_9x9_Overview.png
    └── 10_Production_Component_And_Collision_Separation.png
```
