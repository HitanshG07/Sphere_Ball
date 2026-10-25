# MODEL SPECIFICATION — `SM_ArenaEnvironment_Colosseum_01` (Phase 2 Production Kit)

## 1. Final World Bounds, Pivot & Spatial Envelope

All production exports are authored in world space (`1 Blender unit = 1.0 Roblox stud`, `+Y` Up) with model origin and pivot at **`(0.0000, 0.0000, 0.0000)`**, surrounding the untouched `9×9` gameplay arena centered at **`(0.0000, 50.0000, 0.0000)`**:

| Spatial Metric | Concept 02 Baseline | Phase 2 Production Measured Value | Compliance Status |
| :--- | :--- | :--- | :--- |
| **World Origin / Pivot** | `(0.0, 0.0, 0.0)` | **`(0.0000, 0.0000, 0.0000)`** (`CFrame.new(0, 0, 0)`) | **PASS (Exact)** |
| **World X Bounds** | `[-130.0248, +130.0248]` | **`[-130.0917, +130.0917]` studs** (`260.1834` studs span; `+0.0669` studs from 2-step gate column abacus moulding) | **PASS** |
| **World Y Bounds** | `[18.0600, 125.0000]` | **`[18.0600, 125.0000]` studs** (`106.9400` studs height; `-32.94` to `+74.00` studs relative to `Y = 51.0` floor) | **PASS (Exact Match)** |
| **World Z Bounds** | `[-136.0248, +136.0248]` | **`[-136.0917, +136.0917]` studs** (`272.1834` studs span) | **PASS** |
| **Inner Elliptical Void (`R_x × R_z`)** | `98.0000 × 104.0000` studs | **`98.0000 × 104.0000` studs** (`R_min = 98.0000` studs, `0` vertices intruding inside inner ellipse) | **PASS (`0` Intrusions)** |
| **Cardinal Clearances to `108×108` Grid** | `44.00` studs (`±X`), `50.00` studs (`±Z`) | **`44.0000` studs (`±X`) • `50.0000` studs (`±Z`)** | **PASS** |
| **Diagonal (`45°`) & 3D Corner Clearance** | `24.4994` studs (`24.8145` 3D) | **`24.4994` studs radial (`24.8145` studs min 3D Euclidean distance to `(±54, 51, ±54)`)** | **PASS** |
| **Void-Elimination Threshold (`World Y < 15.0`)** | `Y_min = 18.06` (`+3.06` studs above `Y = 15.0`) | **`Y_min = 18.0600` studs** (`+3.0600` studs safely above canonical `World Y < 15.0` elimination threshold) | **PASS** |

---

## 2. Five Reusable Production Archetypes (`meshes/archetypes/`)

The complete 48-bay elliptical Colosseum (`40` standard/vomitorium bays + `4` two-bay cardinal gate pavilions + `1` North Imperial Reactor Crest) is constructed from **5 reusable modular archetypes** with **zero (`0`) additional connector or trim meshes**:

| Unique Archetype ID | Unique Triangles | Unique Vertices | Instance Count | Instantiated Triangles | Local Bounding Box (`min` to `max` studs) | OBJ / GLB SHA-256 (Prefix) | Roblox `< 20k` Gate |
| :--- | ---: | ---: | :---: | ---: | :--- | :--- | :--- |
| `UMOD_01_Standard_Window_Bay` | **`6,018`** | `18,054` | `12×` | **`72,216`** | `(-9.67, -32.94, -26.23)` to `(8.77, 63.60, 3.73)` | `f8d96f0bf4bd6fe2...` / `e30207c3767faa0f...` | **PASS (`< 20,000`)** |
| `UMOD_02_Standard_Clipeus_Bay` | **`5,982`** | `17,946` | `20×` | **`119,640`** | `(-9.69, -32.94, -26.22)` to `(8.78, 63.60, 3.73)` | `9d8e9592cc26a75d...` / `c9dd30e463402e7f...` | **PASS (`< 20,000`)** |
| `UMOD_03_Vomitorium_Cavea_Bay` | **`6,712`** | `20,136` | `8×` | **`53,696`** | `(-9.59, -32.94, -26.24)` to `(8.72, 63.60, 3.73)` | `b1464f1d15a7f0f3...` / `898c69405f9829fd...` | **PASS (`< 20,000`)** |
| `UMOD_04_Cardinal_Triumphal_Gate_Pavilion` | **`8,680`** | `26,040` | `4×` | **`34,720`** | `(-17.49, -32.94, -16.84)` to `(17.49, 63.50, 16.09)` | `bc4d6813d3e0d781...` / `a6780309a5d773a7...` | **PASS (`< 20,000`)** |
| `UMOD_05_North_Imperial_Reactor_Crest` | **`3,496`** | `10,488` | `1×` | **`3,496`** | `(-10.20, 0.00, -8.56)` to `(10.20, 10.50, 8.50)` | `0ca9b789c0addc7b...` / `7076343ade396f40...` | **PASS (`< 20,000`)** |
| **Total Modular Kit (`5` Archetypes)** | **`30,888`** | **`92,664`** | **`45` instances** | **`283,768`** | — | — | **100% `< 20,000` Tris** |

- **Exact Accounting Proof (No Double-Counting)**:
  $$12 \times 6,018 + 20 \times 5,982 + 8 \times 6,712 + 4 \times 8,680 + 1 \times 3,496 = 72,216 + 119,640 + 53,696 + 34,720 + 3,496 = \mathbf{283,768\text{ triangles}}$$
  Every single triangle in the assembled `283,768`-triangle Colosseum is accounted for by the `45` instances of `UMOD_01..UMOD_05`, with **`0` additional connector triangles**.

---

## 3. Aggregate Architectural Group Breakdown & Comparison to Concept 02

| Base Architectural Group | Concept 02 Triangles | Phase 2 Production Triangles | Delta vs. Concept 02 | Architectural Explanation of Phase 2 Delta |
| :--- | ---: | ---: | ---: | :--- |
| `COL_ExteriorArcade` | `34,880` | **`34,880`** | `+0` | Preserves the exact 120 exterior arches, 9 wedge voussoirs/arch, keystones, imposts & barrel-vaulted soffits. |
| `COL_ColumnOrders` | `30,640` | **`70,880`** | `+40,240` | Section 4.1 refinement of all 120 exterior columns: 2-tier entasis/fluted shafts, 3-ring curved Tuscan echinus + cyma abacus, multi-turn coiled 3D Ionic spiral volutes + contoured bolsters, and 16-leaf 3D Corinthian capitals + corner caulicoli volutes. |
| `COL_StoneMasonry` | `36,608` | **`67,328`** | `+30,720` | Section 4.1 bevelled *opus quadratum* ashlar pier & spandrel blocks (`chamfer = 0.04` studs) creating physical 3D mortar relief channels on every pier course. |
| `COL_CaveaSeating` | `30,080` | **`44,240`** | `+14,160` | Section 4.1 refinement of the 40 interior *Porticus in Summa Cavea* Corinthian columns (16-leaf capitals & 16-vertex fluted shafts) above the 22 profiled seating tiers. |
| `COL_Vomitoria` | `9,760` | **`6,672`** | `-3,088` | Standardizes the 8 inter-cardinal vaulted 7-voussoir *vomitoria* portals (`UMOD_03`) and 32 solid *balteus* bays (`UMOD_01`/`UMOD_02`) for 100% pure 5-archetype modularity. |
| `COL_AtticCornice` | `22,320` | **`22,320`** | `+0` | Preserves the exact 4th-level Attic windows, 3D bronze *clipei* shields, 80 corbels, 40 *velarium* masts & 4 dentil entablature rings. |
| `COL_GateTowers` | `20,496` | **`33,952`** | `+13,456` | Section 4.1 refinement of the 16 large Corinthian columns & 13-voussoir bevelled ashlar piers across the 4 Cardinal Triumphal Gate Pavilions + `MAT_AltNeutral`/`MAT_LightTrim` portcullis bezels. |
| `COL_NorthReactorCrest` | `1,804` | **`3,496`** | `+1,692` | Section 4.1 refinement of the 4 Corinthian aedicula columns, bevelled ashlar piers & `MAT_AltNeutral`/`MAT_LightTrim` reactor frame on the North Imperial Tribune. |
| **Total Assembled Scene** | **`186,588`** | **`283,768`** | **`+97,180` (`1.52×`)** | **All added geometry is concentrated in sculpted capitals, volutes, acanthus leaves & ashlar bevel relief.** |

---

## 4. All 33 Import-Safe Section MeshParts (`meshes/sections/` & Assembled Submeshes)

To guarantee that **every individual MeshPart is strictly below Roblox Studio's `20,000`-triangle limit**, both `meshes/sections/` and the assembled `meshes/SM_ArenaEnvironment_Colosseum_01.{obj,glb,gltf,fbx}` are partitioned into **33 named architectural MeshParts** (`1,668` to `16,832` triangles each, all sharing world pivot `(0, 0, 0)`):

| Section MeshPart Name | Triangles | Vertices | World Bounding Box (`min` to `max` studs) | OBJ / GLB SHA-256 (Prefix) | `< 20,000` Gate |
| :--- | ---: | ---: | :--- | :--- | :--- |
| `COL_StoneMasonry_Q1` | `16,832` | `50,496` | `(0.00, 18.06, 0.00)` to `(128.00, 109.20, 134.00)` | `d0a20667bc1e0707...` / `c2ff2df77fc90dd3...` | **PASS (`< 20,000`)** |
| `COL_ExteriorArcade_Q1` | `8,720` | `26,160` | `(15.61, 59.25, 16.49)` to `(125.55, 96.88, 131.52)` | `36221b5225b651b2...` / `07986f891077ce12...` | **PASS (`< 20,000`)** |
| `COL_ColumnOrders_O1` | `8,860` | `26,580` | `(98.66, 51.00, 16.07)` to `(126.46, 109.20, 82.12)` | `6d7ca178b58e994f...` / `960758fc36be7c60...` | **PASS (`< 20,000`)** |
| `COL_AtticCornice_Q1` | `5,580` | `16,740` | `(15.73, 65.60, 16.55)` to `(126.56, 114.60, 132.51)` | `aa8e4dad9f31fb77...` / `aad3536a72d08885...` | **PASS (`< 20,000`)** |
| `COL_CaveaSeating_Q1` | `11,060` | `33,180` | `(12.79, 51.00, 13.57)` to `(125.42, 109.20, 131.37)` | `ac27277908ecf562...` / `66aab381525af3df...` | **PASS (`< 20,000`)** |
| `COL_Vomitoria_Q1` | `1,668` | `5,004` | `(14.44, 73.80, 15.22)` to `(112.33, 82.34, 118.28)` | `47f205152bbf78ce...` / `5b0c3cac7eb7cb5b...` | **PASS (`< 20,000`)** |
| `COL_ColumnOrders_O2` | `8,860` | `26,580` | `(31.22, 51.00, 92.13)` to `(90.75, 109.20, 129.10)` | `6e8939058a00d5c5...` / `9c995dc307202715...` | **PASS (`< 20,000`)** |
| `COL_StoneMasonry_Q2` | `16,832` | `50,496` | `(-128.00, 18.06, 0.00)` to `(0.00, 109.20, 134.00)` | `2f6cff0fa0ccfb81...` / `4dd031419d597e84...` | **PASS (`< 20,000`)** |
| `COL_ExteriorArcade_Q2` | `8,720` | `26,160` | `(-125.56, 59.25, 16.43)` to `(-15.67, 96.88, 131.50)` | `463789b749389f26...` / `bb359497a8a48e5c...` | **PASS (`< 20,000`)** |
| `COL_ColumnOrders_O3` | `8,860` | `26,580` | `(-78.56, 51.00, 103.34)` to `(-15.31, 109.20, 132.41)` | `be701fc25d49a50e...` / `d8c3648eed318aaf...` | **PASS (`< 20,000`)** |
| `COL_AtticCornice_Q2` | `5,580` | `16,740` | `(-126.56, 65.60, 16.55)` to `(-15.73, 114.60, 132.51)` | `c4b4071708c13c02...` / `e7e16623e759f1cc...` | **PASS (`< 20,000`)** |
| `COL_CaveaSeating_Q2` | `11,060` | `33,180` | `(-125.42, 51.00, 13.57)` to `(-12.79, 109.20, 131.37)` | `2848ea0cad9d5865...` / `7dc00e3aff7450a9...` | **PASS (`< 20,000`)** |
| `COL_Vomitoria_Q2` | `1,668` | `5,004` | `(-112.33, 73.80, 15.22)` to `(-14.44, 82.36, 118.28)` | `f99c14180b0dcb25...` / `7735f95cc793012e...` | **PASS (`< 20,000`)** |
| `COL_ColumnOrders_O4` | `8,860` | `26,580` | `(-123.29, 51.00, 32.74)` to `(-87.97, 109.20, 94.91)` | `8bcf9d88f4fc2789...` / `55d0e532cadbb96a...` | **PASS (`< 20,000`)** |
| `COL_StoneMasonry_Q3` | `16,832` | `50,496` | `(-128.00, 18.06, -134.00)` to `(-0.00, 109.20, 0.00)` | `d9fecba5f3c60699...` / `ce221715eda76be7...` | **PASS (`< 20,000`)** |
| `COL_ExteriorArcade_Q3` | `8,720` | `26,160` | `(-125.55, 59.25, -131.52)` to `(-15.61, 96.88, -16.49)` | `a9133aec29c212de...` / `6dbaae90d30e310a...` | **PASS (`< 20,000`)** |
| `COL_ColumnOrders_O5` | `8,860` | `26,580` | `(-126.46, 51.00, -82.12)` to `(-98.66, 109.20, -16.07)` | `98069031744a5cf7...` / `56ac9a8bb7c138e9...` | **PASS (`< 20,000`)** |
| `COL_AtticCornice_Q3` | `5,580` | `16,740` | `(-126.56, 65.60, -132.51)` to `(-15.73, 114.60, -16.55)` | `983d130afea481f9...` / `a7a5d25a795f80f2...` | **PASS (`< 20,000`)** |
| `COL_CaveaSeating_Q3` | `11,060` | `33,180` | `(-125.42, 51.00, -131.37)` to `(-12.79, 109.20, -13.57)` | `3c821cb308831ed9...` / `5a9f0b4d24e53e50...` | **PASS (`< 20,000`)** |
| `COL_Vomitoria_Q3` | `1,668` | `5,004` | `(-112.33, 73.80, -118.28)` to `(-14.44, 82.34, -15.22)` | `8b1ecf3a7dcfe79a...` / `5a1712e151b5f278...` | **PASS (`< 20,000`)** |
| `COL_ColumnOrders_O6` | `8,860` | `26,580` | `(-90.75, 51.00, -129.10)` to `(-31.22, 109.20, -92.13)` | `c3a07cebb9abb616...` / `0089f9245ec57a59...` | **PASS (`< 20,000`)** |
| `COL_StoneMasonry_Q4` | `16,832` | `50,496` | `(-0.00, 18.06, -134.00)` to `(128.00, 109.20, -0.00)` | `96c8cc61921027ea...` / `4dcf24b5a1486b80...` | **PASS (`< 20,000`)** |
| `COL_ExteriorArcade_Q4` | `8,720` | `26,160` | `(15.67, 59.25, -131.50)` to `(125.56, 96.88, -16.43)` | `5279b3cbeec2abdd...` / `a79abc0713cd33ee...` | **PASS (`< 20,000`)** |
| `COL_ColumnOrders_O7` | `8,860` | `26,580` | `(15.31, 51.00, -132.41)` to `(78.56, 109.20, -103.34)` | `b53673965546182b...` / `97e2dacfb84318ae...` | **PASS (`< 20,000`)** |
| `COL_AtticCornice_Q4` | `5,580` | `16,740` | `(15.73, 65.60, -132.51)` to `(126.56, 114.60, -16.55)` | `e6ad5175db9ffb7d...` / `ac986f62dcb91fe5...` | **PASS (`< 20,000`)** |
| `COL_CaveaSeating_Q4` | `11,060` | `33,180` | `(12.79, 51.00, -131.37)` to `(125.42, 109.20, -13.57)` | `ad98bb8c81e4f879...` / `550dd028c87436fd...` | **PASS (`< 20,000`)** |
| `COL_Vomitoria_Q4` | `1,668` | `5,004` | `(14.44, 73.80, -118.28)` to `(112.33, 82.36, -15.22)` | `28932faf40e715a4...` / `202bd630a5d67ec1...` | **PASS (`< 20,000`)** |
| `COL_ColumnOrders_O8` | `8,860` | `26,580` | `(87.97, 51.00, -94.91)` to `(123.29, 109.20, -32.74)` | `23b801b429f7ddc0...` / `58811b5cd2f9744b...` | **PASS (`< 20,000`)** |
| `COL_GateTower_East` | `8,488` | `25,464` | `(97.91, 48.80, -14.26)` to `(130.09, 114.50, 14.26)` | `2834cc4c6ac47775...` / `eedad5e0d422ff02...` | **PASS (`< 20,000`)** |
| `COL_GateTower_South` | `8,488` | `25,464` | `(-14.26, 48.80, 103.91)` to `(14.26, 114.50, 136.09)` | `ad7182558b25b86b...` / `f41c9c8345662b15...` | **PASS (`< 20,000`)** |
| `COL_GateTower_West` | `8,488` | `25,464` | `(-130.09, 48.80, -14.26)` to `(-97.91, 114.50, 14.26)` | `377b9bb8161454f2...` / `b35f8e43aba30ec6...` | **PASS (`< 20,000`)** |
| `COL_GateTower_North` | `8,488` | `25,464` | `(-14.26, 48.80, -136.09)` to `(14.26, 114.50, -103.91)` | `d8a6ded26a50ccef...` / `497053d0e9996dd3...` | **PASS (`< 20,000`)** |
| `COL_NorthReactorCrest` | `3,496` | `10,488` | `(-10.20, 114.50, -128.50)` to `(10.20, 125.00, -111.44)` | `18fa54e652df0655...` / `45a7590a6d3042fe...` | **PASS (`< 20,000`)** |
| **Total (`33` Section MeshParts)** | **`283,768`** | **`851,304`** | `(-130.09, 18.06, -136.09)` to `(+130.09, 125.00, +136.09)` | — | **100% PASS (Max `16,832`)** |

---

## 5. Twelve Canonical Materials, PBR Values & `512×512` UV Atlas Mapping

All 12 canonical materials are defined consistently across `.obj`/`.mtl`, `.glb`, `.gltf`, and `.fbx`, and mapped via box-projected `vt` UV coordinates (`TEXCOORD_0`) to padded cells inside `textures/T_Colosseum_Production_Atlas_512.png` (`512 × 512 px`, `SHA-256: 6bbec54b5e9b72dddf443ef33d2292420656309b7ec820ecc362199b8181ae0e`):

| Material Name | Base RGB | Hex | Roughness | Metallic | Emissive Factor | Atlas Cell `(cx, cy)` | Roblox `Enum.Material` | Surface Area (sq studs) | Area Share (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | ---: | ---: |
| `MAT_TravertineWarm` | `(196, 178, 150)` | `#C4B296` | `0.66` | `0.04` | `(0.0, 0.0, 0.0)` | `(1, 0)` | `Limestone` | `340,017.69` | `43.05%` |
| `MAT_TravertineLight` | `(214, 198, 172)` | `#D6C6AC` | `0.62` | `0.04` | `(0.0, 0.0, 0.0)` | `(0, 0)` | `Limestone` | `194,077.42` | `24.57%` |
| `MAT_TuffFoundation` | `(132, 122, 108)` | `#847A6C` | `0.74` | `0.06` | `(0.0, 0.0, 0.0)` | `(3, 0)` | `Slate` | `122,605.50` | `15.52%` |
| `MAT_ImperialMarble` | `(232, 224, 210)` | `#E8E0D2` | `0.34` | `0.08` | `(0.0, 0.0, 0.0)` | `(1, 1)` | `Marble` | `79,949.50` | `10.12%` |
| `MAT_BasaltShadow` | `(58, 60, 68)` | `#3A3C44` | `0.76` | `0.10` | `(0.0, 0.0, 0.0)` | `(0, 1)` | `Basalt` | `24,448.80` | `3.10%` |
| `MAT_LimestoneCream` | `(204, 192, 172)` | `#CCC0AC` | `0.64` | `0.04` | `(0.0, 0.0, 0.0)` | `(2, 0)` | `Limestone` | `21,312.77` | `2.70%` |
| `MAT_DarkNeutral` | `(32, 38, 54)` | `#202636` | `0.42` | `0.58` | `(0.0, 0.0, 0.0)` | `(3, 1)` | `SmoothPlastic` | `3,713.36` | `0.47%` |
| `EMI_Cyan` | `(0, 195, 255)` | `#00C3FF` | `0.15` | `0.00` | `(0.0, 0.76, 1.0)` | `(2, 2)` | `Neon` | `1,853.53` | `0.23%` |
| `MAT_BronzeClipeus` | `(176, 142, 88)` | `#B08E58` | `0.36` | `0.72` | `(0.0, 0.0, 0.0)` | `(2, 1)` | `Metal` | `1,091.71` | `0.14%` |
| `MAT_AltNeutral` | `(42, 50, 70)` | `#2A3246` | `0.38` | `0.62` | `(0.0, 0.0, 0.0)` | `(0, 2)` | `Metal` | `367.60` | `0.05%` |
| `MAT_LightTrim` | `(170, 190, 215)` | `#AABED7` | `0.28` | `0.78` | `(0.0, 0.0, 0.0)` | `(1, 2)` | `Metal` | `318.24` | `0.04%` |
| `EMI_Amber` | `(255, 170, 0)` | `#FFAA00` | `0.15` | `0.00` | `(1.0, 0.67, 0.0)` | `(3, 2)` | `Neon` | `8.12` | `< 0.01%` |
| **Total Surface Area** | — | — | — | — | — | — | — | **`789,764.24`** | **`100.00%` (`0.23%` Emissive)** |
