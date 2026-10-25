# 02 — Scale, Void-Clearance & Arena Alignment Verification (Concept 02)

## 1. Locked `9×9` Gameplay Arena Grid Reference (Untouched)

The playable arena of **Map 01 (*Sphere Brawl: Rolling Rampage*)** is a locked `9×9` modular grid of `81` tiles (`Workspace.Map01_Arena.ArenaTiles`), which **Concept 02 does not modify, overlap, or occlude under any circumstances**:

| Locked Gameplay Arena Parameter | Exact Value | Verification Status |
| :--- | :--- | :--- |
| **Grid Layout** | `9 × 9` tiles (`81` tiles total, `Tile_R1_C1` .. `Tile_R9_C9`) | **LOCKED & UNTOUCHED** |
| **Single Tile Size** | `12 × 2 × 12` studs (`X × Y × Z`) | **LOCKED & UNTOUCHED** |
| **Total Playable Footprint** | `108 × 108` studs (`X ∈ [-54.0, +54.0]`, `Z ∈ [-54.0, +54.0]`) | **LOCKED & UNTOUCHED** |
| **Center Tile (`Tile_R5_C5`) CFrame** | `(0, 50, 0)` | **LOCKED & UNTOUCHED** |
| **Playable Top Surface (`Y_top`)** | `Y = 51.0` studs (`Y_bottom = 49.0` studs) | **LOCKED & UNTOUCHED** |
| **Corner Tile Outer Corners** | `(±54.0, 51.0, ±54.0)` — radial distance from `(0, 50, 0)` = **`76.3675` studs** | **LOCKED & UNTOUCHED** |
| **Elimination Plane (`Y_elim`)** | `Y < 10.0` studs | **CLEAR (Lowest env vertex is `Y = 18.06` studs)** |

---

## 2. Concept 02 Dimensional Envelope & Void-Clearance Proof

All `559,764` vertices (`186,588` triangles) of `SM_ArenaEnvironment_Colosseum_01` were programmatically audited in `concept_source/generate_colosseum_concept_02.py`. The table below documents the exact dimensional compliance against every requirement:

| Spatial / Clearance Metric | Required Specification | Concept 02 Measured Value | Margin / Status |
| :--- | :--- | :--- | :--- |
| **World Origin / Pivot** | `(0, 0, 0)` (`1 unit = 1 Roblox stud`, `+Y` Up) | `(0.0000, 0.0000, 0.0000)` | **PASS (Exact)** |
| **Inner Void Minimum Radius (`R_min`)** | `≥ 96.0` studs (`96..104` studs target) | **`98.0000` studs** (`R_x = 98.0`, `R_z = 104.0` elliptical inner *podium*) | **PASS (`+2.00` studs safety margin)** |
| **Vertices Inside `R < 98.0` or Elliptical Void** | `0` vertices (`100%` open drop zone) | **`0` vertices** (`(X/98)² + (Z/104)² ≥ 1.0000` for all `559,764` vertices) | **PASS (`0` intrusions)** |
| **East / West Cardinal Void Clearance (`±X`)** | `≥ 22.0` studs from `X = ±54.0` | **`44.0000` studs** (`X = ±54.0` tile edge to `X = ±98.0` inner podium wall) | **PASS (`+22.00` studs above min)** |
| **North / South Cardinal Void Clearance (`±Z`)** | `≥ 22.0` studs from `Z = ±54.0` | **`50.0000` studs** (`Z = ±54.0` tile edge to `Z = ±104.0` inner podium wall) | **PASS (`+28.00` studs above min)** |
| **Diagonal (`45°`) Corner Void Clearance** | `≥ 22.0` studs from `(±54, ±54)` (`R = 76.37`) | **`24.4994` studs** radial (`R_ellipse(45°) = 100.8669` studs vs. `76.3675` studs) | **PASS (`+2.50` studs above min)** |
| **Min 3D Euclidean Distance to Grid Corners** | `≥ 22.0` studs | **`24.8145` studs** | **PASS (`+2.81` studs above min)** |
| **Outer Wall Footprint Radius (`R_max`)** | `≤ 142.0` studs (`126..142` studs target) | **`136.6984` studs** (Standard facade `128 × 134`; Gate pavilions `130 × 136`) | **PASS (`5.30` studs inside max)** |
| **Overall Bounding Box (`X × Y × Z`)** | Symmetric centered envelope | **`260.05 × 106.94 × 272.05` studs** (`X ∈ [-130.02, +130.02]`, `Y ∈ [18.06, 125.00]`, `Z ∈ [-136.02, +136.02]`) | **PASS (Centered on `(0,0,0)`)** |
| **Top Elevation Above Tile Top (`Y = 51.0`)** | `+62.0` to `+78.0` studs (`Y = 113..129`) | **`+74.00` studs** (`Y_max = 125.00` at North Imperial Crest; `Y = 118.20` at *velarium* masts; `Y = 114.60` at attic cornice) | **PASS (Inside `+62..+78` range)** |
| **Foundation Depth Below Tile Top (`Y = 51.0`)** | `-26.0` to `-38.0` studs (`Y = 13..25`) | **`-32.94` studs** (`Y_min = 18.06` studs at lower tuff foundation base) | **PASS (Inside `-26..-38` range)** |

---

## 3. Elevated Gameplay Camera Sightline & Collision Proof

1. **Unobstructed Elevated Gameplay Camera (`Y = 85..145` studs, pitch `35°..55°`)**:
   - At the standard arena camera height (`Y = 115..140` studs looking toward `(0, 50, 0)`), the `98.0 × 104.0`-stud inner elliptical void provides a `44.0`-stud (`±X`) to `50.0`-stud (`±Z`) perimeter buffer around the `108 × 108` tile grid.
   - Because the seating bowl (*cavea*) slopes outward as it rises (`R = 101.2` at `Y = 53.8` expanding to `R = 123.5` at `Y = 90.8`), the camera sightline from any azimuth angle has a `100%` unobstructed view of all `81` tiles, corner hazards, and falling spheres in the elimination moat.
2. **Non-Colliding Visual Surroundings (`CanCollide = false`)**:
   - Every MeshPart in `SM_ArenaEnvironment_Colosseum_01` is configured with `Anchored = true`, `CanCollide = false`, `CanTouch = false`, and `CanQuery = false`, guaranteeing zero physics interference with rolling player spheres or falling tiles.
