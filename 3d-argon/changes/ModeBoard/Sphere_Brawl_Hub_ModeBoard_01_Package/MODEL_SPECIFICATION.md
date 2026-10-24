# Model Specification — `SM_Hub_ModeBoard_01` (Step 5, Phase 2 Final Production Mesh)

## 1. Asset Identity, Approved Concept Provenance & World Placement Contract

| Property | Measured / Verified Production Value | Authority / Status |
|---|---|---|
| **Canonical Asset ID** | `SM_Hub_ModeBoard_01` | Locked (`TASK-03`, `TASK-09`, `Master 3D Art Bible`) |
| **Descriptive Name** | Tactical Arena Mode Selection Command Gantry (`14.4000 × 3.8000 × 8.8000 studs`) | Approved Phase 1 Concept (`Sphere_Brawl_Hub_ModeBoard_Concept_01.zip`) |
| **Approved Concept Archive Hash** | `e76c211dd44fc5c36d71a546ef8e683de05923e8ee142e203173caabeeaddeb6` (`1,647,242 bytes`) | **Verified Identical** before Phase 2 build |
| **Authoritative World Position** | **`(35.0000, 150.0000, -326.0000)`** | **LOCKED** (`TASK-03`, `MASTER_IMPLEMENTATION_PLAN.md` §2.4, `GameConfig.Lobby.ModeBoard`) |
| **Authoritative Floor Reference** | **`World Y = 150.0000`** (`Local Y = 0.0000`) | **LOCKED** (`TASK-03`, `MASTER_IMPLEMENTATION_PLAN.md` §2.4, `SM_Hub_PlazaPlatform_01`) |
| **Verified Radial Inward Yaw** | **`θ_yaw = -53.39292061°`** (`-0.93188189 rad`, `atan2(-35, 26)`) | **Verified** (Points `Local +Z` front directly at Hub center `(0, 150, -300)`) |
| **Required Placement Transform** | `CFrame.new(35, 150, -326) * CFrame.Angles(0, math.rad(-53.39292061), 0)` | **Verified Right-Handed Orthonormal Transform** (`det(R) = +1.0000`) |
| **Resulting World FrontVector** | **`(-0.802744, 0.000000, +0.596324)`** (unit vector from `(35, 150, -326)` to `(0, 150, -300)`) | **Verified (`dot = 1.000000`)** |
| **Local Coordinate Convention** | `1.0 Blender/Export Unit = 1.0 Roblox Stud` (`+Y Up`, `+Z Front`, `+X Right`, origin `(0, 0, 0)` at bottom footprint center) | **Locked & Verified** |
| **Measured Local Bounding Box** | `Width (X) = 14.4000 studs` (`[-7.2000, +7.2000]`), `Height (Y) = 8.8000 studs` (`[0.0000, +8.8000]`), `Depth (Z) = 3.8000 studs` (`[-1.9000, +1.9000]`) | **Measured from `4,836` export vertices (`0.0000 stud` deviation from approved concept)** |
| **Main Command Matrix Tilt** | **`14.0°` backward from vertical** (`front normal = (0.000000, +0.241922, +0.970296)`) | **Measured & Verified** |
| **Measured Transformed World AABB** | `World X in [29.3702, 40.6298]` (`11.2595 studs`), `World Y in [150.0000, 158.8000]` (`8.8000 studs`), `World Z in [-332.6738, -319.3320]` (`13.3418 studs`) | **Measured across all `4,836` transformed vertices** |
| **Measured Vertex Radial Span** | **`R_vertex in [41.7610, 46.0024] studs`** from Hub center `(0, 150, -300)` | **Measured (`100%` inside approved `R = 37.0..52.5 stud` station band)** |
| **Primary Visual Triangle Count** | **`1,612 triangles`** (`4,836 export vertices`) across `18` named components | **Measured (`888 triangles` / `35.52%` below the Art Bible `< 2,500` station budget)** |
| **Optional Collision Proxy Count** | **`36 triangles`** (`108 vertices`) across `3` box hulls in `COL_ModeBoard_Body` | **Measured (`meshes/collision_proxy/COL_ModeBoard_Body.obj` & `.glb`)** |
| **Texture Atlas Specification** | `64 × 64 pixels` (`176 bytes`, 8-bit sRGB PNG swatch atlas `SphereBrawl_ModeBoard_PaletteAtlas.png`, `SHA-256: 0a03e72726052db05ee3aac0da6597a362f69e3a19ab319f72c3efd306acc3b5`) | **Measured (`<= 1024 × 1024` per `TASK-09`)** |
| **Editable `.blend` Source Status** | **`NOT GENERATED — BLENDER UNAVAILABLE`** (`which blender` exited non-zero in container; runnable `bpy`/`bmesh` code included in `scripts/generate_mode_board_blender.py`) | **Honest Environment Disclosure** |

---

## 2. Mathematical Verification of the Placement Transform & Orthonormal Basis

At the locked station center `P_board = (35.0, 150.0, -326.0)`, the horizontal vector to the central Hub / Queue Portal `P_hub = (0.0, 150.0, -300.0)` is:
```text
ΔV = P_hub - P_board = (-35.0000, 0.0000, +26.0000),   ||ΔV|| = sqrt(1225 + 676) = sqrt(1901) = 43.60045871 studs
FrontVector = ΔV / ||ΔV|| = (-0.80274385, 0.00000000, +0.59632400)
```
Rotating around the vertical `+Y` axis by `θ_yaw = atan2(-35.0, 26.0) = -0.93188189 rad = -53.39292061°` (`cos(θ_yaw) = +0.59632400`, `sin(θ_yaw) = -0.80274385`):
```luau
local targetCFrame =
    CFrame.new(35, 150, -326)
    * CFrame.Angles(0, math.rad(-53.39292061), 0)
```
produces the right-handed orthonormal rotation matrix `R_y(-53.39292061°)`:
- **`RightVector (Local +X)`:** `(+0.59632400, 0.00000000, +0.80274385)`
- **`UpVector (Local +Y)`:** `(0.00000000, +1.00000000, 0.00000000)`
- **`ZVector / FrontVector (Local +Z)`:** `(-0.80274385, 0.00000000, +0.59632400)`
- **Orthonormality & Right-Handedness:** `R^T R = I_3`, `RightVector × UpVector = ZVector`, and `det(R) = +1.00000000`.
- **World Coordinate Mapping for any Local Vertex `(x_local, y_local, z_local)`:**
  - `World_X = 35.0000 + 0.59632400 * x_local - 0.80274385 * z_local`
  - `World_Y = 150.0000 + y_local`
  - `World_Z = -326.0000 + 0.80274385 * x_local + 0.59632400 * z_local`

---

## 3. Five Separate UI-Ready Replaceable Panel Surfaces (Critical Section 5.2 Contract)

All five display surfaces (`GEO_ModeBoard_UIPanel_01_FFA`, `GEO_ModeBoard_UIPanel_02_Duel`, `GEO_ModeBoard_UIPanel_03_TeamClash`, `GEO_ModeBoard_UIPanel_04_KingTile`, and `GEO_ModeBoard_HeaderSign`) are exported as **independent, flat, non-overlapping mesh components** with **zero baked text geometry**. None of the strings `ARENA MODE SELECT`, `FREE-FOR-ALL`, `DUEL`, `TEAM CLASH`, `KING TILE`, `ACTIVE`, or `COMING SOON` exist in the mesh triangles:

| Component Name | Mode & State | Panel Dimensions (`W × H × T studs`) | Tilt Angle | Front Face Local Center `(X, Y, Z)` | Front Face World Center `(X, Y, Z)` | Local Front Normal | World Front Normal |
|---|---|---|---|---|---|---|---|
| `GEO_ModeBoard_UIPanel_01_FFA` | **FREE-FOR-ALL** (`ACTIVE`) | `4.0800 × 3.7800 × 0.0800` | `14.0°` | `[-3.0, 4.48792, 0.48161]` | **`[32.8244, 154.4879, -328.121]`** | `[0.0, 0.241922, 0.970296]` | `[-0.778899, 0.241922, 0.578611]` |
| `GEO_ModeBoard_UIPanel_02_Duel` | **DUEL** (`COMING SOON`) | `5.0400 × 1.2000 × 0.0800` | `14.0°` | `[2.88, 6.04778, -0.08251]` | **`[36.7836, 156.0478, -323.7373]`** | `[0.0, 0.241922, 0.970296]` | `[-0.778899, 0.241922, 0.578611]` |
| `GEO_ModeBoard_UIPanel_03_TeamClash` | **TEAM CLASH** (`COMING SOON`) | `5.0400 × 1.2000 × 0.0800` | `14.0°` | `[2.88, 4.43709, 0.31908]` | **`[36.4613, 154.4371, -323.4978]`** | `[0.0, 0.241922, 0.970296]` | `[-0.778899, 0.241922, 0.578611]` |
| `GEO_ModeBoard_UIPanel_04_KingTile` | **KING TILE** (`COMING SOON`) | `5.0400 × 1.2000 × 0.0800` | `14.0°` | `[2.88, 2.8264, 0.72067]` | **`[36.1389, 152.8264, -323.2583]`** | `[0.0, 0.241922, 0.970296]` | `[-0.778899, 0.241922, 0.578611]` |
| `GEO_ModeBoard_HeaderSign` | **ARENA MODE SELECT** (`STATIC_HEADER`) | `11.4800 × 0.8200 × 0.4000` | `0.0°` | `[0.0, 7.95, 0.88]` | **`[34.2936, 157.95, -325.4752]`** | `[0.0, 0.0, 1.0]` | `[-0.802744, 0.0, 0.596324]` |

### Non-Collision & Non-Overlap Between UI Surfaces and Physical Relief Elements
- On **`GEO_ModeBoard_UIPanel_01_FFA`**, the flat UI surface sits at `d = +0.3000` (`X in [-5.04, -0.96]`, `s in [0.96, 4.74]`). The modular 3D active status pill (`s in [4.18, 4.58]`), central sphere-clash reticle (`s in [1.76, 4.14]`), and bottom sub-banner (`s in [1.12, 1.52]`) project forward (`d = +0.3000..+0.4500`), leaving an unobstructed `4.08 × 0.76 stud` primary title band (`s in [1.62, 2.38]`) plus clean text regions inside the top status pill and bottom sub-banner.
- On **`GEO_ModeBoard_UIPanel_02_Duel`**, **`_03_TeamClash`**, and **`_04_KingTile`**, each flat UI surface sits at `d = +0.1300` (`X in [+0.36, +5.40]`, `1.20 studs` tall). The left padlock relief (`X in [+0.72, +1.18]`), mode icon relief (`X in [+1.21, +1.71]`), and right lock badge housing (`X in [+3.64, +5.02]`) leave an unobstructed **`1.88 × 1.20 stud` central title zone (`X in [+1.74, +3.62]`)** for `DUEL`, `TEAM CLASH`, and `KING TILE` plus a **`1.18 × 0.52 stud` badge face (`X in [+3.66, +4.84]`)** for `COMING SOON`.

---

## 4. Complete 18-Component Hierarchy & Material Slot Breakdown

Every component listed below is preserved identically in `meshes/SM_Hub_ModeBoard_01.obj` (`18` `o GEO_ModeBoard_*` objects) and `meshes/SM_Hub_ModeBoard_01.glb` (`19` glTF nodes: `1` root `SM_Hub_ModeBoard_01` + `18` child mesh nodes):

| # | Component Name | Material Slot | Locked RGB & Hex | Roblox Target Material | Triangles | Vertices | Local Bounding Box (`min` -> `max`) | 3D Area (`sq. studs` / `%`) |
|---:|---|---|---|---|---:|---:|---|---:|
| 1 | `GEO_ModeBoard_BasePlinth` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `50` | `150` | `[-7.2, 0.0, -1.9]` -> `[7.2, 1.72, 1.9]` | `174.90` (`15.66%`) |
| 2 | `GEO_ModeBoard_BaseUpperTier` | `MAT_AltNeutral` | `(42, 50, 70)` `#2A3246` | `Enum.Material.Metal` | `90` | `270` | `[-6.85, 0.42, -1.76]` -> `[6.85, 7.45, 1.74]` | `155.98` (`13.96%`) |
| 3 | `GEO_ModeBoard_MainChassis` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `28` | `84` | `[-5.8, 1.4758, -1.2097]` -> `[5.8, 7.234, 0.8994]` | `158.86` (`14.22%`) |
| 4 | `GEO_ModeBoard_LeftButtress` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `44` | `132` | `[-7.08, 0.88, -1.74]` -> `[-5.82, 8.35, 1.36]` | `62.20` (`5.57%`) |
| 5 | `GEO_ModeBoard_RightButtress` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `44` | `132` | `[5.82, 0.88, -1.74]` -> `[7.08, 8.35, 1.36]` | `62.20` (`5.57%`) |
| 6 | `GEO_ModeBoard_SideCollars` | `MAT_LightTrim` | `(170, 190, 215)` `#AABED7` | `Enum.Material.Metal` | `212` | `636` | `[-7.14, 0.02, -1.88]` -> `[7.14, 6.8893, 1.895]` | `83.93` (`7.51%`) |
| 7 | `GEO_ModeBoard_CommandMatrixFrame` | `MAT_AltNeutral` | `(42, 50, 70)` `#2A3246` | `Enum.Material.Metal` | `172` | `516` | `[-7.2, 1.1, -1.32]` -> `[7.2, 7.2, 1.1226]` | `133.86` (`11.98%`) |
| 8 | `GEO_ModeBoard_UIPanel_01_FFA` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `10` | `30` | `[-5.04, 2.6347, -0.0532]` -> `[-0.96, 6.3218, 0.9388]` | `16.68` (`1.49%`) |
| 9 | `GEO_ModeBoard_UIPanel_02_Duel` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `10` | `30` | `[0.36, 5.4462, -0.3053]` -> `[5.4, 6.63, 0.0626]` | `7.05` (`0.63%`) |
| 10 | `GEO_ModeBoard_UIPanel_03_TeamClash` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `10` | `30` | `[0.36, 3.8356, 0.0963]` -> `[5.4, 5.0193, 0.4642]` | `7.05` (`0.63%`) |
| 11 | `GEO_ModeBoard_UIPanel_04_KingTile` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `10` | `30` | `[0.36, 2.2249, 0.4979]` -> `[5.4, 3.4086, 0.8658]` | `7.05` (`0.63%`) |
| 12 | `GEO_ModeBoard_HeaderCanopy` | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | `Enum.Material.Metal` | `50` | `150` | `[-6.8, 7.45, -1.55]` -> `[6.8, 8.8, 0.48]` | `112.66` (`10.09%`) |
| 13 | `GEO_ModeBoard_HeaderSign` | `MAT_AltNeutral` | `(42, 50, 70)` `#2A3246` | `Enum.Material.Metal` | `8` | `24` | `[-5.74, 7.54, 0.48]` -> `[5.74, 8.36, 0.88]` | `19.48` (`1.74%`) |
| 14 | `GEO_ModeBoard_ActiveModeReticle` | `MAT_LightTrim` | `(170, 190, 215)` `#AABED7` | `Enum.Material.Metal` | `162` | `486` | `[-5.6, 2.1349, -0.1742]` -> `[-0.4, 6.9087, 1.249]` | `19.50` (`1.75%`) |
| 15 | `GEO_ModeBoard_LockReliefs` | `MAT_LightTrim` | `(170, 190, 215)` `#AABED7` | `Enum.Material.Metal` | `270` | `810` | `[0.16, 2.186, -0.2422]` -> `[5.6, 6.7196, 1.0065]` | `15.63` (`1.40%`) |
| 16 | `GEO_ModeBoard_ModeReliefs` | `MAT_LightTrim` | `(170, 190, 215)` `#AABED7` | `Enum.Material.Metal` | `194` | `582` | `[-6.04, 1.7034, -0.4747]` -> `[6.04, 8.52, 1.1008]` | `55.69` (`4.99%`) |
| 17 | `GEO_ModeBoard_CyanAccents` | `EMI_Cyan` | `(0, 195, 255)` `#00C3FF` | `Enum.Material.Neon` | `198` | `594` | `[-6.58, 0.42, -0.0968]` -> `[6.58, 8.74, 1.84]` | `23.03` (`2.06%`) |
| 18 | `GEO_ModeBoard_AmberAccents` | `EMI_Amber` | `(255, 170, 0)` `#FFAA00` | `Enum.Material.Neon` | `50` | `150` | `[1.8, 0.42, -0.0339]` -> `[6.58, 6.2369, 1.82]` | `1.24` (`0.11%`) |
| — | **Total (`SM_Hub_ModeBoard_01`)** | **5 Locked Materials** | — | — | **`1,612`** | **`4,836`** | **`[-7.20, 0.00, -1.90]` -> `[+7.20, 8.80, +1.90]`** | **`1116.99` (`100.00%`)** |
| — | `COL_ModeBoard_Body` (Optional Proxy) | `MAT_DarkNeutral` | `(32, 38, 54)` `#202636` | Invisible Collider (`Transparency = 1`) | **`36`** | **`108`** | `[-7.20, 0.00, -1.90]` -> `[+7.20, 8.80, +1.52]` | `385.16` |

### Summary by Locked Material Slot (70 / 20 / 10 Visual Hierarchy)

| Material Slot | Locked RGB | Hex Code | Native Roblox Material | Triangles | 3D Surface Area (`sq. studs`) | 3D Area Share (`%`) | Top-Projected Area Share (`%`) |
|---|---|---|---|---:|---:|---:|---:|
| **`MAT_DarkNeutral`** | `(32, 38, 54)` | `#202636` | `Enum.Material.Metal` | `256` | `608.53` | **`54.48%`** | `58.69%` |
| **`MAT_AltNeutral`** | `(42, 50, 70)` | `#2A3246` | `Enum.Material.Metal` | `270` | `309.32` | **`27.69%`** | `22.89%` |
| **`MAT_LightTrim`** | `(170, 190, 215)` | `#AABED7` | `Enum.Material.Metal` | `838` | `174.82` | **`15.65%`** | `16.37%` |
| **`EMI_Cyan`** | `(0, 195, 255)` | `#00C3FF` | `Enum.Material.Neon` | `198` | `23.03` | **`2.06%`** | `1.94%` |
| **`EMI_Amber`** | `(255, 170, 0)` | `#FFAA00` | `Enum.Material.Neon` | `50` | `1.24` | **`0.11%`** | `0.11%` |
| **Total** | — | — | **18 Named Components** | **`1,612`** | **`1,116.95`** | **`100.00%`** | **`100.00%`** |

- **Dark/Slate Structural Dominance:** `MAT_DarkNeutral` (`54.48%`) + `MAT_AltNeutral` (`27.69%`) = **`82.17%`** of total 3D surface area.
- **Secondary Light Metallic Trim:** `MAT_LightTrim` = **`15.65%`** of total 3D surface area.
- **Restrained Recessed Energy Accents:** `EMI_Cyan` (`2.06%`) + `EMI_Amber` (`0.11%`) = **`2.17%`** of total 3D surface area, with **`EMI_Cyan` (`23.03 sq. studs`) exceeding `EMI_Amber` (`1.24 sq. studs`) by an `18.6 : 1` surface-area ratio**.

---

## 5. Binary glTF 2.0 (`.glb`) & Wavefront (`.obj` / `.mtl`) Export Specifications

- **`meshes/SM_Hub_ModeBoard_01.obj` (`334,410 bytes`) & `meshes/SM_Hub_ModeBoard_01.mtl` (`1,080 bytes`):**
  - Valid relative `mtllib SM_Hub_ModeBoard_01.mtl` header; `18` `o GEO_ModeBoard_*` / `g GEO_ModeBoard_*` groups; `4,836` vertex lines (`v x y z r g b`); `5` UV palette coordinates (`vt`); `1,612` outward unit face normals (`vn`); `1,612` triangle faces (`f`).
- **`meshes/SM_Hub_ModeBoard_01.glb` (`272,664 bytes`):**
  - `12-byte` GLB v2 header + `8-byte` JSON chunk header + `20,988-byte` JSON chunk + `8-byte` BIN chunk header + `251,648-byte` BIN buffer chunk = **`272,664 bytes`**.
  - Contains `19` nodes (`SM_Hub_ModeBoard_01` root node + `18` named `GEO_ModeBoard_*` child mesh nodes), `18` meshes (`1,612` triangles total), `5` PBR materials (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`, `EMI_Amber`), and embedded `64×64` PNG palette atlas.
- **Optional Collision Proxy (`meshes/collision_proxy/COL_ModeBoard_Body.obj` `5,259 bytes`, `.mtl` `364 bytes`, `.glb` `9,772 bytes`):**
  - `3` simple non-snagging box hulls (`COL_ModeBoard_BaseHull`, `COL_ModeBoard_MainGantryHull`, `COL_ModeBoard_CanopyHull`) totaling **`36 triangles`** (`108 vertices`), leaving the entire player walk-up space in front of `Local Z = +1.5200` unobstructed.
