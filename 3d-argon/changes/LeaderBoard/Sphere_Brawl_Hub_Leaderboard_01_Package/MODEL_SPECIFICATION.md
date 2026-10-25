# Model Specification — `SM_Hub_Leaderboard_01` (Grand Three-Board Monument & Nine-Position Podium Array)

- **Canonical Asset ID:** `SM_Hub_Leaderboard_01`
- **Approved Concept Baseline:** `Sphere_Brawl_Hub_Leaderboard_Concept_06.zip` (`SHA-256: bb705ed9a35fca5ada4f0065f90db818010aafc85f00986946967323080f15e0`)
- **Scale & Axis Convention:** `1.0 unit = 1.0 Roblox stud` | `+Y` Up | `+Z` Front (faces Hub Center `(0, 150, -300)`) | `+X` Width Axis across the boards

---

## 1. Local & World Bounding Envelope and Pivot Convention

- **Pivot / Local Origin `(0.0000, 0.0000, 0.0000)`:** Placed at the bottom-floor walking-surface reference (`Local Y = 0.0000 -> World Y = 150.0000`) aligned with the authoritative world anchor `(35.0000, 150.0000, -274.0000)`.
- **Deliberate Asymmetric Local X Span:** As locked in Concept 06, the local X bounds span **`[-11.0000, +31.0000] studs`** (`42.0000 studs` total width, geometric center at `Local X_c = +10.0000`). The model is **not** recentered around `X = 0` so that the South/Port edge (`Local X = -11.0000`) maintains its verified walkable clearance to `SM_Hub_ShopKiosk_01` while expanding northward into the open NE plaza arc.

| Metric | X Span (Studs) | Y Span (Studs) | Z Span (Studs) | Overall Dimensions (`W × H × D`) | Status |
|---|---|---|---|---|---|
| **Overall Local Bounds (`SM_Hub_Leaderboard_01`)** | `[-11.0000, +31.0000]` | `[0.0000, +26.0000]` | `[-4.2000, +4.8000]` | **`42.0000 × 26.0000 × 9.0000 studs`** | **MEASURED** |
| **Main Monument Wall Local Bounds** | `[-11.0000, +31.0000]` | `[0.0000, +26.0000]` | `[-4.2000, +0.6800]` | `42.0000 × 26.0000 × 4.8800 studs` | **MEASURED** |
| **Combined 3 Podium Stages Local Bounds** | `[-9.7000, +29.7000]` | `[0.0000, +2.5000]` | `[+0.6000, +4.8000]` | `39.4000 × 2.5000 × 4.2000 studs` | **MEASURED** |
| **Transformed World Bounds (`Yaw = -126.60707939°`)** | `[13.7938, 44.8432]` | `[150.0000, 176.0000]` | `[-284.2912, -246.7044]` | **`31.0494 × 26.0000 × 37.5868 studs`** | **MEASURED** |

- **Verified World Placement Transform (`CALCULATED` & `MEASURED`):**
  ```lua
  local targetCFrame =
      CFrame.new(35, 150, -274)
      * CFrame.Angles(0, math.rad(-126.60707939), 0)
  ```
  - **World Forward Vector (`+Z_local`):** `(-0.80274385, 0.00000000, -0.59632400)` (unit vector from `(35, 150, -274)` to `(0, 150, -300)`).
  - **World Right Vector (`+X_local`):** `(-0.59632400, 0.00000000, +0.80274385)`.
  - **World Up Vector (`+Y_local`):** `(0.00000000, 1.00000000, 0.00000000)`.
  - **Orthonormality & Right-Handedness:** `det(R) = +1.00000000`, `||R^T R - I||_inf < 1e-12`.

---

## 2. Final Vertex, Triangle & Export-Format Consistency Metrics

| Export File | Format | Triangles | Vertices | Normals | UVs | Components / Nodes | Byte Size | Status |
|---|---|---|---|---|---|---|---|---|
| `meshes/SM_Hub_Leaderboard_01.obj` | Wavefront OBJ | **`1,852`** | `5,556` | `1,852` | `6` | `53` `o`/`g` groups | `353,730 B` | **MEASURED — PASS** |
| `meshes/SM_Hub_Leaderboard_01.mtl` | Wavefront MTL | — | — | — | — | `6` `newmtl` definitions | `1,548 B` | **MEASURED — PASS** |
| `meshes/SM_Hub_Leaderboard_01.glb` | Binary glTF 2.0 | **`1,852`** | `5,556` | `5,556` | `5,556` | `1` root + `53` mesh nodes (`54` total) | `348,236 B` | **MEASURED — PASS** |
| `meshes/collision_proxy/COL_Leaderboard_Body.obj` | Wavefront OBJ | **`168`** | `504` | `168` | `1` | `5` `o`/`g` hull groups | `31,829 B` | **MEASURED — PASS** |
| `meshes/collision_proxy/COL_Leaderboard_Body.mtl` | Wavefront MTL | — | — | — | — | `1` `newmtl` definition | `390 B` | **MEASURED — PASS** |
| `meshes/collision_proxy/COL_Leaderboard_Body.glb` | Binary glTF 2.0 | **`168`** | `504` | `504` | `504` | `1` root + `5` hull nodes (`6` total) | `32,484 B` | **MEASURED — PASS** |
| `textures/SphereBrawl_Leaderboard_PaletteAtlas.png` | PNG (`64 × 64`) | — | — | — | — | `6` palette swatches (`3 × 2` grid) | `343 B` | **MEASURED — PASS** |

- **Triangle Budget Compliance:** The visual production mesh has **`1,852` triangles** (`144` triangles cleaner than the `1,996`-triangle Concept 06 blockout by consolidating the 9 stepped podium columns into unified 8-sided chamfered prisms), staying **`148` triangles below** the `< 2,000` maximum budget.
- **Geometry Hygiene:** `0` degenerate faces (`min_triangle_area = 0.00400 sq studs`), `0` inverted or mismatched normals, `0` cross-component coplanar overlaps, `0` baked text triangles, and `0` static player avatar triangles.

---

## 3. Locked Material Slots & Surface Area Distribution

| Material Slot | sRGB `(R, G, B)` | Hex | Emissive | Roblox Material | Triangles | 3D Area (sq studs) | 3D Area % | Top Area % | Surface Role |
|---|---|---|---|---|---|---|---|---|---|
| `MAT_DarkNeutral` | `(32, 38, 54)` | `#202636` | No | `Enum.Material.Metal` | `920` | `6,208.6731` | **`61.02%`** | `53.26%` | Grounded wall plinth, 4 support piers, rear A-frame stabilizers, 3 module housings, rear service panels, canopy visors, 3 podium stage bases, 9 podium pedestals, 15 UI backing planes |
| `MAT_AltNeutral` | `(42, 50, 70)` | `#2A3246` | No | `Enum.Material.Metal` | `208` | `3,452.0670` | **`33.93%`** | `41.71%` | Stepped wall pedestal deck, 3 structural cross-girders, 3 module inner bezels, 3 rear cooling spines, 3 podium stage decks |
| `MAT_LightTrim` | `(170, 190, 215)` | `#AABED7` | No | `Enum.Material.Metal` | `484` | `399.5758` | **`3.93%`** | `4.71%` | 16 pier collar clamps, UI perimeter frame rails, canopy brow trims, 3-tier crown crest, 2nd-place podium trims, 9 nameplate bezels |
| `EMI_Cyan` | `(0, 195, 255)` | `#00C3FF` | Yes | `Enum.Material.Neon` | `80` | `37.5740` | **`0.37%`** | `0.10%` | Display A (`SESSION KOs`) and Stage A (`A1`/`A3`) cyan conduits, divider bar, canopy beacon, rear spine status strip, stage threshold bar |
| `EMI_Amber` | `(255, 170, 0)` | `#FFAA00` | Yes | `Enum.Material.Neon` | `80` | `38.7460` | **`0.38%`** | `0.11%` | Display B (`SESSION WINS`) and Stage B (`B1`/`B3`) amber conduits, divider bar, center crown beacon, rear spine status strip, stage threshold bar |
| `EMI_Magnetic` | `(165, 55, 255)` | `#A537FF` | Yes | `Enum.Material.Neon` | `80` | `37.5740` | **`0.37%`** | `0.10%` | Display C (`SESSION STANDINGS`) and Stage C (`C1`/`C3`) magnetic-purple conduits, divider bar, canopy beacon, rear spine status strip, stage threshold bar |

- **Palette Balance:** Dark/slate metallic structure (`MAT_DarkNeutral + MAT_AltNeutral`) accounts for **`94.95%`** of total 3D surface area (`94.97%` top-projected area), `MAT_LightTrim` accounts for **`3.93%`**, and the three emissive accents combined account for **`1.12%`**.
- **Texture Atlas:** `textures/SphereBrawl_Leaderboard_PaletteAtlas.png` is a deterministic `64 × 64` sRGB PNG (`343` bytes, `SHA-256: 299993571790b284162c852e77940f089355650c01552483ee9cf1fa4c4b2390`).

---

## 4. Three Leaderboard Displays & Three Separate 3-Place Podium Stages (`9` Podiums Total)

### 4.1 Three Colour-Themed Leaderboard Modules

| Board ID | Board Title & Intended Alpha Scope | Accent Material | Outer Housing Local Bounds (`X / Y / Z`) | Header UI Surface (`W × H`, `Y` Span) | Main Table UI Surface (`W × H`, `Y` Span) | Front UI `Z` |
|---|---|---|---|---|---|---|
| **Display A (Left)** | `SESSION KOs` (`RANK \| PILOT NAME \| KOs`) | `EMI_Cyan` (`#00C3FF`) | `X[-10.10, +2.70]` (`12.80 W`), `Y[3.80, 22.90]`, `Z[-3.25, +0.04]` | `11.8000 × 2.3500` (`X[-9.60, +2.20]`, `Y[19.55, 21.90]`) | `11.8000 × 13.0000` (`X[-9.60, +2.20]`, `Y[6.20, 19.20]`) | `+0.1800` |
| **Display B (Center)** | `SESSION WINS` (`RANK \| PILOT NAME \| WINS`) | `EMI_Amber` (`#FFAA00`) | `X[+3.60, +16.40]` (`12.80 W`), `Y[3.80, 23.60]`, `Z[-3.32, +0.14]` | `11.8000 × 2.6000` (`X[+4.10, +15.90]`, `Y[19.95, 22.55]`) | `11.8000 × 13.4000` (`X[+4.10, +15.90]`, `Y[6.20, 19.60]`) | `+0.2800` |
| **Display C (Right)** | `SESSION STANDINGS` (`RANK \| PILOT NAME \| KOs \| WINS`) | `EMI_Magnetic` (`#A537FF`) | `X[+17.30, +30.10]` (`12.80 W`), `Y[3.80, 22.90]`, `Z[-3.25, +0.04]` | `11.8000 × 2.3500` (`X[+17.80, +29.60]`, `Y[19.55, 21.90]`) | `11.8000 × 13.0000` (`X[+17.80, +29.60]`, `Y[6.20, 19.20]`) | `+0.1800` |

### 4.2 Three Physically Separate 3-Position Podium Stages (`9` Podium Positions)

Each leaderboard module has its own dedicated `12.0000 W × 4.2000 D` foreground stage (`Local Z in [+0.6000, +4.8000]`, base `Y in [0.0000, 0.3200]`, deck `Y in [0.3200, 0.5200]`), separated by **`1.7000-stud` open walkways** (`Local X in [+2.3000, +4.0000]` and `[+16.0000, +17.7000]`):

| Stage | Stage Local `X` Span | Position Key | Placement & Rank | Podium Column Local `X` Span (`Width`) | Podium Column Local `Z` Span (`Depth`) | Podium Top `Y` | Trim Material |
|---|---|---|---|---|---|---|---|
| **Stage A (`KOs`)** | `[-9.7000, +2.3000]` (`12.00 W`) | **`A2`** | Left — `2ND` Place | `[-9.3100, -5.7900]` (`3.5200 W`, `X_c = -7.5500`) | `[+1.5900, +4.5100]` (`2.9200 D`) | **`1.9500`** | `MAT_LightTrim` |
| **Stage A (`KOs`)** | `[-9.7000, +2.3000]` (`12.00 W`) | **`A1`** | Center — `1ST` Place | `[-5.5600, -1.8400]` (`3.7200 W`, `X_c = -3.7000`) | `[+1.4400, +4.6100]` (`3.1700 D`) | **`2.5000`** | `EMI_Cyan` |
| **Stage A (`KOs`)** | `[-9.7000, +2.3000]` (`12.00 W`) | **`A3`** | Right — `3RD` Place | `[-1.6100, +1.9100]` (`3.5200 W`, `X_c = +0.1500`) | `[+1.5900, +4.5100]` (`2.9200 D`) | **`1.5000`** | `EMI_Cyan` |
| **Stage B (`WINS`)** | `[+4.0000, +16.0000]` (`12.00 W`) | **`B2`** | Left — `2ND` Place | `[+4.3900, +7.9100]` (`3.5200 W`, `X_c = +6.1500`) | `[+1.5900, +4.5100]` (`2.9200 D`) | **`1.9500`** | `MAT_LightTrim` |
| **Stage B (`WINS`)** | `[+4.0000, +16.0000]` (`12.00 W`) | **`B1`** | Center — `1ST` Place | `[+8.1400, +11.8600]` (`3.7200 W`, `X_c = +10.0000`) | `[+1.4400, +4.6100]` (`3.1700 D`) | **`2.5000`** | `EMI_Amber` |
| **Stage B (`WINS`)** | `[+4.0000, +16.0000]` (`12.00 W`) | **`B3`** | Right — `3RD` Place | `[+12.0900, +15.6100]` (`3.5200 W`, `X_c = +13.8500`) | `[+1.5900, +4.5100]` (`2.9200 D`) | **`1.5000`** | `EMI_Amber` |
| **Stage C (`STANDINGS`)** | `[+17.7000, +29.7000]` (`12.00 W`) | **`C2`** | Left — `2ND` Place | `[+18.0900, +21.6100]` (`3.5200 W`, `X_c = +19.8500`) | `[+1.5900, +4.5100]` (`2.9200 D`) | **`1.9500`** | `MAT_LightTrim` |
| **Stage C (`STANDINGS`)** | `[+17.7000, +29.7000]` (`12.00 W`) | **`C1`** | Center — `1ST` Place | `[+21.8400, +25.5600]` (`3.7200 W`, `X_c = +23.7000`) | `[+1.4400, +4.6100]` (`3.1700 D`) | **`2.5000`** | `EMI_Magnetic` |
| **Stage C (`STANDINGS`)** | `[+17.7000, +29.7000]` (`12.00 W`) | **`C3`** | Right — `3RD` Place | `[+25.7900, +29.3100]` (`3.5200 W`, `X_c = +27.5500`) | `[+1.5900, +4.5100]` (`2.9200 D`) | **`1.5000`** | `EMI_Magnetic` |

---

## 5. All 15 Replaceable UI-Ready Surface Specifications (Zero Baked Text)

Every UI-ready component has an exact 2-triangle flat front quad facing **`Local +Z = (0.000000, 0.000000, +1.000000)`** (`World Normal = (-0.802744, 0.000000, -0.596324)`):

| # | Component Name | Role | Width × Height (Studs) | Local `X` Span | Local `Y` Span | Front `Z` | Front Face Local Center | Front Face World Center |
|---|---|---|---|---|---|---|---|---|
| 1 | `GEO_Leaderboard_UIHeader_A_SessionKOs` | Display A Header | `11.8000 × 2.3500` | `[-9.60, +2.20]` | `[19.55, 21.90]` | `+0.1800` | `(-3.7000, 20.7250, 0.1800)` | `(37.0619, 170.7250, -277.0745)` |
| 2 | `GEO_Leaderboard_UIMain_A_SessionKOs` | Display A Main Table | `11.8000 × 13.0000` | `[-9.60, +2.20]` | `[6.20, 19.20]` | `+0.1800` | `(-3.7000, 12.7000, 0.1800)` | `(37.0619, 162.7000, -277.0745)` |
| 3 | `GEO_Leaderboard_UIHeader_B_SessionWins` | Display B Header | `11.8000 × 2.6000` | `[+4.10, +15.90]` | `[19.95, 22.55]` | `+0.2800` | `(10.0000, 21.2500, 0.2800)` | `(28.8120, 171.2500, -266.1395)` |
| 4 | `GEO_Leaderboard_UIMain_B_SessionWins` | Display B Main Table | `11.8000 × 13.4000` | `[+4.10, +15.90]` | `[6.20, 19.60]` | `+0.2800` | `(10.0000, 12.9000, 0.2800)` | `(28.8120, 162.9000, -266.1395)` |
| 5 | `GEO_Leaderboard_UIHeader_C_SessionStandings` | Display C Header | `11.8000 × 2.3500` | `[+17.80, +29.60]` | `[19.55, 21.90]` | `+0.1800` | `(23.7000, 20.7250, 0.1800)` | `(20.7226, 170.7250, -255.0842)` |
| 6 | `GEO_Leaderboard_UIMain_C_SessionStandings` | Display C Main Table | `11.8000 × 13.0000` | `[+17.80, +29.60]` | `[6.20, 19.20]` | `+0.1800` | `(23.7000, 12.7000, 0.1800)` | `(20.7226, 162.7000, -255.0842)` |
| 7 | `GEO_Leaderboard_PodiumNameplate_A2_2ND` | Stage A 2nd Nameplate | `2.9000 × 0.9800` | `[-9.00, -6.10]` | `[0.74, 1.72]` | `+4.5300` | `(-7.5500, 1.2300, 4.5300)` | `(35.8658, 151.2300, -282.7590)` |
| 8 | `GEO_Leaderboard_PodiumNameplate_A1_1ST` | Stage A 1st Nameplate | `3.1000 × 1.3200` | `[-5.25, -2.15]` | `[0.88, 2.20]` | `+4.6300` | `(-3.7000, 1.5400, 4.6300)` | `(33.4897, 151.5400, -279.7282)` |
| 9 | `GEO_Leaderboard_PodiumNameplate_A3_3RD` | Stage A 3rd Nameplate | `2.9000 × 0.6800` | `[-1.30, +1.60]` | `[0.66, 1.34]` | `+4.5300` | `(0.1500, 1.0000, 4.5300)` | `(31.2741, 151.0000, -276.5779)` |
| 10 | `GEO_Leaderboard_PodiumNameplate_B2_2ND` | Stage B 2nd Nameplate | `2.9000 × 0.9800` | `[+4.70, +7.60]` | `[0.74, 1.72]` | `+4.5300` | `(6.1500, 1.2300, 4.5300)` | `(27.6962, 151.2300, -271.7614)` |
| 11 | `GEO_Leaderboard_PodiumNameplate_B1_1ST` | Stage B 1st Nameplate | `3.1000 × 1.3200` | `[+8.45, +11.55]` | `[0.88, 2.20]` | `+4.6300` | `(10.0000, 1.5400, 4.6300)` | `(25.3201, 151.5400, -268.7306)` |
| 12 | `GEO_Leaderboard_PodiumNameplate_B3_3RD` | Stage B 3rd Nameplate | `2.9000 × 0.6800` | `[+12.40, +15.30]` | `[0.66, 1.34]` | `+4.5300` | `(13.8500, 1.0000, 4.5300)` | `(23.1045, 151.0000, -265.5803)` |
| 13 | `GEO_Leaderboard_PodiumNameplate_C2_2ND` | Stage C 2nd Nameplate | `2.9000 × 0.9800` | `[+18.40, +21.30]` | `[0.74, 1.72]` | `+4.5300` | `(19.8500, 1.2300, 4.5300)` | `(19.5265, 151.2300, -260.7638)` |
| 14 | `GEO_Leaderboard_PodiumNameplate_C1_1ST` | Stage C 1st Nameplate | `3.1000 × 1.3200` | `[+22.15, +25.25]` | `[0.88, 2.20]` | `+4.6300` | `(23.7000, 1.5400, 4.6300)` | `(17.1504, 151.5400, -257.7330)` |
| 15 | `GEO_Leaderboard_PodiumNameplate_C3_3RD` | Stage C 3rd Nameplate | `2.9000 × 0.6800` | `[+26.10, +29.00]` | `[0.66, 1.34]` | `+4.5300` | `(27.5500, 1.0000, 4.5300)` | `(14.9348, 151.0000, -254.5827)` |

---

## 6. All Nine Runtime Avatar Placement Reference Anchors (`4.0000-Stud` Display Scale)

No dummy avatars are exported in `SM_Hub_Leaderboard_01.obj` or `.glb`. When the runtime system spawns or renders winners' avatars on the nine podiums, use a uniform **`4.0000-stud` height (`72.7273%` of a `5.5000-stud` R15 reference avatar)** facing `Local +Z` (`World (-0.802744, 0, -0.596324)`) at these exact coordinates:

| Podium Key | Stage / Board | Rank | Feet Local Anchor `(X, Y, Z)` | Head Top Local `(X, Y, Z)` | Feet World Anchor `(X, Y, Z)` | Head Top World `(X, Y, Z)` | Screen Bottom `Y` |
|---|---|---|---|---|---|---|---|
| **`A2`** | Stage A (`SESSION KOs`) | `2ND` (Left) | `(-7.5500, 1.9500, +3.0500)` | `(-7.5500, 5.9500, +3.0500)` | `(37.0539, 151.9500, -281.8765)` | `(37.0539, 155.9500, -281.8765)` | `6.2000` (`+0.25` clear) |
| **`A1`** | Stage A (`SESSION KOs`) | `1ST` (Center) | `(-3.7000, 2.5000, +3.0250)` | `(-3.7000, 6.5000, +3.0250)` | `(34.7781, 152.5000, -278.7711)` | `(34.7781, 156.5000, -278.7711)` | `6.2000` (`0.30` overlap at lower border) |
| **`A3`** | Stage A (`SESSION KOs`) | `3RD` (Right) | `(+0.1500, 1.5000, +3.0500)` | `(+0.1500, 5.5000, +3.0500)` | `(32.4622, 151.5000, -275.6954)` | `(32.4622, 155.5000, -275.6954)` | `6.2000` (`+0.70` clear) |
| **`B2`** | Stage B (`SESSION WINS`) | `2ND` (Left) | `(+6.1500, 1.9500, +3.0500)` | `(+6.1500, 5.9500, +3.0500)` | `(28.8842, 151.9500, -270.8789)` | `(28.8842, 155.9500, -270.8789)` | `6.2000` (`+0.25` clear) |
| **`B1`** | Stage B (`SESSION WINS`) | `1ST` (Center) | `(+10.0000, 2.5000, +3.0250)` | `(+10.0000, 6.5000, +3.0250)` | `(26.6085, 152.5000, -267.7735)` | `(26.6085, 156.5000, -267.7735)` | `6.2000` (`0.30` overlap at lower border) |
| **`B3`** | Stage B (`SESSION WINS`) | `3RD` (Right) | `(+13.8500, 1.5000, +3.0500)` | `(+13.8500, 5.5000, +3.0500)` | `(24.2926, 151.5000, -264.6978)` | `(24.2926, 155.5000, -264.6978)` | `6.2000` (`+0.70` clear) |
| **`C2`** | Stage C (`SESSION STANDINGS`) | `2ND` (Left) | `(+19.8500, 1.9500, +3.0500)` | `(+19.8500, 5.9500, +3.0500)` | `(20.7146, 151.9500, -259.8813)` | `(20.7146, 155.9500, -259.8813)` | `6.2000` (`+0.25` clear) |
| **`C1`** | Stage C (`SESSION STANDINGS`) | `1ST` (Center) | `(+23.7000, 2.5000, +3.0250)` | `(+23.7000, 6.5000, +3.0250)` | `(18.4388, 152.5000, -256.7759)` | `(18.4388, 156.5000, -256.7759)` | `6.2000` (`0.30` overlap at lower border) |
| **`C3`** | Stage C (`SESSION STANDINGS`) | `3RD` (Right) | `(+27.5500, 1.5000, +3.0500)` | `(+27.5500, 5.5000, +3.0500)` | `(16.1229, 151.5000, -253.7002)` | `(16.1229, 155.5000, -253.7002)` | `6.2000` (`+0.70` clear) |

---

## 7. Complete 53-Component Hierarchy Breakdown (`SM_Hub_Leaderboard_01`)

| # | Component Name | Material | Tris | Verts | 3D Area (sq studs) | Local Bounding Box (`[x0,y0,z0]` to `[x1,y1,z1]`) |
|---|---|---|---|---|---|---|
| 1 | `GEO_Leaderboard_WallPlinth` | `MAT_DarkNeutral` | `50` | `150` | `709.1347` | `[-11.00, 0.00, -4.20]` to `[31.00, 3.10, 0.60]` |
| 2 | `GEO_Leaderboard_WallPedestal` | `MAT_AltNeutral` | `22` | `66` | `282.2840` | `[-10.60, 1.05, -3.85]` to `[30.60, 2.30, 0.35]` |
| 3 | `GEO_Leaderboard_SupportPiers` | `MAT_DarkNeutral` | `88` | `264` | `701.7972` | `[-10.94, 3.10, -3.42]` to `[30.94, 24.10, 0.22]` |
| 4 | `GEO_Leaderboard_CollarClamps` | `MAT_LightTrim` | `160` | `480` | `145.4392` | `[-11.00, 5.92, -3.55]` to `[31.00, 22.08, 0.32]` |
| 5 | `GEO_Leaderboard_RearStabilizers` | `MAT_DarkNeutral` | `40` | `120` | `172.3406` | `[-10.86, 1.05, -4.15]` to `[30.86, 18.20, -3.35]` |
| 6 | `GEO_Leaderboard_CrossGirders` | `MAT_AltNeutral` | `30` | `90` | `619.2996` | `[-10.30, 3.00, -3.38]` to `[30.30, 22.85, -0.05]` |
| 7 | `GEO_Leaderboard_Module_A_Housing` | `MAT_DarkNeutral` | `34` | `102` | `690.9095` | `[-10.10, 3.80, -3.25]` to `[2.70, 22.90, 0.22]` |
| 8 | `GEO_Leaderboard_Module_A_Bezel` | `MAT_AltNeutral` | `8` | `24` | `473.0080` | `[-9.92, 3.95, +0.02]` to `[2.52, 22.75, 0.16]` |
| 9 | `GEO_Leaderboard_LightTrim` | `MAT_LightTrim` | `228` | `684` | `189.0462` | `[-9.95, 5.98, +0.14]` to `[29.95, 25.55, 0.68]` |
| 10 | `GEO_Leaderboard_UIHeader_A_SessionKOs` | `MAT_DarkNeutral` | `8` | `24` | `55.7420` | `[-9.60, 19.55, +0.12]` to `[2.20, 21.90, 0.18]` |
| 11 | `GEO_Leaderboard_UIMain_A_SessionKOs` | `MAT_DarkNeutral` | `8` | `24` | `308.3600` | `[-9.60, 6.20, +0.12]` to `[2.20, 19.20, 0.18]` |
| 12 | `GEO_Leaderboard_Accent_A` | `EMI_Cyan` | `64` | `192` | `36.3420` | `[-10.04, 0.36, -3.75]` to `[2.64, 23.95, 4.68]` |
| 13 | `GEO_Leaderboard_RearSpine` | `MAT_AltNeutral` | `66` | `198` | `966.5221` | `[-8.10, 4.10, -3.74]` to `[28.10, 21.80, -3.25]` |
| 14 | `GEO_Leaderboard_RearServicePanels` | `MAT_DarkNeutral` | `150` | `450` | `421.4160` | `[-7.30, 4.70, -3.82]` to `[27.30, 20.00, -3.63]` |
| 15 | `GEO_Leaderboard_Module_B_Housing` | `MAT_DarkNeutral` | `34` | `102` | `722.0482` | `[+3.60, 3.80, -3.32]` to `[16.40, 23.60, 0.32]` |
| 16 | `GEO_Leaderboard_Module_B_Bezel` | `MAT_AltNeutral` | `8` | `24` | `490.6200` | `[+3.78, 3.95, +0.12]` to `[16.22, 23.45, 0.26]` |
| 17 | `GEO_Leaderboard_UIHeader_B_SessionWins` | `MAT_DarkNeutral` | `8` | `24` | `61.6720` | `[+4.10, 19.95, +0.22]` to `[15.90, 22.55, 0.28]` |
| 18 | `GEO_Leaderboard_UIMain_B_SessionWins` | `MAT_DarkNeutral` | `8` | `24` | `317.8480` | `[+4.10, 6.20, +0.22]` to `[15.90, 19.60, 0.28]` |
| 19 | `GEO_Leaderboard_Accent_B` | `EMI_Amber` | `64` | `192` | `37.5140` | `[+3.66, 0.36, -3.82]` to `[16.34, 24.65, 4.68]` |
| 20 | `GEO_Leaderboard_Module_C_Housing` | `MAT_DarkNeutral` | `34` | `102` | `690.9095` | `[+17.30, 3.80, -3.25]` to `[30.10, 22.90, 0.22]` |
| 21 | `GEO_Leaderboard_Module_C_Bezel` | `MAT_AltNeutral` | `8` | `24` | `473.0080` | `[+17.48, 3.95, +0.02]` to `[29.92, 22.75, 0.16]` |
| 22 | `GEO_Leaderboard_UIHeader_C_SessionStandings` | `MAT_DarkNeutral` | `8` | `24` | `55.7420` | `[+17.80, 19.55, +0.12]` to `[29.60, 21.90, 0.18]` |
| 23 | `GEO_Leaderboard_UIMain_C_SessionStandings` | `MAT_DarkNeutral` | `8` | `24` | `308.3600` | `[+17.80, 6.20, +0.12]` to `[29.60, 19.20, 0.18]` |
| 24 | `GEO_Leaderboard_Accent_C` | `EMI_Magnetic` | `64` | `192` | `36.3420` | `[+17.36, 0.36, -3.75]` to `[30.04, 23.95, 4.68]` |
| 25 | `GEO_Leaderboard_CanopyCrown` | `MAT_DarkNeutral` | `88` | `264` | `349.1532` | `[-10.40, 22.90, -3.15]` to `[30.40, 26.00, 0.60]` |
| 26 | `GEO_Leaderboard_PodiumStage_A_Base` | `MAT_DarkNeutral` | `28` | `84` | `109.2781` | `[-9.70, 0.00, +0.60]` to `[2.30, 0.32, 4.80]` |
| 27 | `GEO_Leaderboard_PodiumStage_A_Deck` | `MAT_AltNeutral` | `22` | `66` | `51.2392` | `[-9.45, 0.32, +0.65]` to `[2.05, 0.52, 4.62]` |
| 28 | `GEO_Leaderboard_Podium_A2_2ND` | `MAT_DarkNeutral` | `22` | `66` | `27.9977` | `[-9.31, 0.52, +1.59]` to `[-5.79, 1.95, 4.51]` |
| 29 | `GEO_Leaderboard_PodiumLightTrim` | `MAT_LightTrim` | `96` | `288` | `65.0904` | `[-9.08, 0.61, +4.43]` to `[29.08, 2.25, 4.64]` |
| 30 | `GEO_Leaderboard_PodiumNameplate_A2_2ND` | `MAT_DarkNeutral` | `8` | `24` | `5.7820` | `[-9.00, 0.74, +4.48]` to `[-6.10, 1.72, 4.53]` |
| 31 | `GEO_Leaderboard_Podium_A1_1ST` | `MAT_DarkNeutral` | `22` | `66` | `38.0191` | `[-5.56, 0.52, +1.44]` to `[-1.84, 2.50, 4.61]` |
| 32 | `GEO_Leaderboard_PodiumAccent_A` | `EMI_Cyan` | `16` | `48` | `1.2320` | `[-5.26, 1.36, +4.48]` to `[1.61, 2.46, 4.64]` |
| 33 | `GEO_Leaderboard_PodiumNameplate_A1_1ST` | `MAT_DarkNeutral` | `8` | `24` | `8.3160` | `[-5.25, 0.88, +4.58]` to `[-2.15, 2.20, 4.63]` |
| 34 | `GEO_Leaderboard_Podium_A3_3RD` | `MAT_DarkNeutral` | `22` | `66` | `22.3991` | `[-1.61, 0.52, +1.59]` to `[1.91, 1.50, 4.51]` |
| 35 | `GEO_Leaderboard_PodiumNameplate_A3_3RD` | `MAT_DarkNeutral` | `8` | `24` | `4.0120` | `[-1.30, 0.66, +4.48]` to `[1.60, 1.34, 4.53]` |
| 36 | `GEO_Leaderboard_PodiumStage_B_Base` | `MAT_DarkNeutral` | `28` | `84` | `109.2781` | `[+4.00, 0.00, +0.60]` to `[16.00, 0.32, 4.80]` |
| 37 | `GEO_Leaderboard_PodiumStage_B_Deck` | `MAT_AltNeutral` | `22` | `66` | `51.2392` | `[+4.25, 0.32, +0.65]` to `[15.75, 0.52, 4.62]` |
| 38 | `GEO_Leaderboard_Podium_B2_2ND` | `MAT_DarkNeutral` | `22` | `66` | `27.9977` | `[+4.39, 0.52, +1.59]` to `[7.91, 1.95, 4.51]` |
| 39 | `GEO_Leaderboard_PodiumNameplate_B2_2ND` | `MAT_DarkNeutral` | `8` | `24` | `5.7820` | `[+4.70, 0.74, +4.48]` to `[7.60, 1.72, 4.53]` |
| 40 | `GEO_Leaderboard_Podium_B1_1ST` | `MAT_DarkNeutral` | `22` | `66` | `38.0191` | `[+8.14, 0.52, +1.44]` to `[11.86, 2.50, 4.61]` |
| 41 | `GEO_Leaderboard_PodiumAccent_B` | `EMI_Amber` | `16` | `48` | `1.2320` | `[+8.44, 1.36, +4.48]` to `[15.31, 2.46, 4.64]` |
| 42 | `GEO_Leaderboard_PodiumNameplate_B1_1ST` | `MAT_DarkNeutral` | `8` | `24` | `8.3160` | `[+8.45, 0.88, +4.58]` to `[11.55, 2.20, 4.63]` |
| 43 | `GEO_Leaderboard_Podium_B3_3RD` | `MAT_DarkNeutral` | `22` | `66` | `22.3991` | `[+12.09, 0.52, +1.59]` to `[15.61, 1.50, 4.51]` |
| 44 | `GEO_Leaderboard_PodiumNameplate_B3_3RD` | `MAT_DarkNeutral` | `8` | `24` | `4.0120` | `[+12.40, 0.66, +4.48]` to `[15.30, 1.34, 4.53]` |
| 45 | `GEO_Leaderboard_PodiumStage_C_Base` | `MAT_DarkNeutral` | `28` | `84` | `109.2781` | `[+17.70, 0.00, +0.60]` to `[29.70, 0.32, 4.80]` |
| 46 | `GEO_Leaderboard_PodiumStage_C_Deck` | `MAT_AltNeutral` | `22` | `66` | `51.2392` | `[+17.95, 0.32, +0.65]` to `[29.45, 0.52, 4.62]` |
| 47 | `GEO_Leaderboard_Podium_C2_2ND` | `MAT_DarkNeutral` | `22` | `66` | `27.9977` | `[+18.09, 0.52, +1.59]` to `[21.61, 1.95, 4.51]` |
| 48 | `GEO_Leaderboard_PodiumNameplate_C2_2ND` | `MAT_DarkNeutral` | `8` | `24` | `5.7820` | `[+18.40, 0.74, +4.48]` to `[21.30, 1.72, 4.53]` |
| 49 | `GEO_Leaderboard_Podium_C1_1ST` | `MAT_DarkNeutral` | `22` | `66` | `38.0191` | `[+21.84, 0.52, +1.44]` to `[25.56, 2.50, 4.61]` |
| 50 | `GEO_Leaderboard_PodiumAccent_C` | `EMI_Magnetic` | `16` | `48` | `1.2320` | `[+22.14, 1.36, +4.48]` to `[29.01, 2.46, 4.64]` |
| 51 | `GEO_Leaderboard_PodiumNameplate_C1_1ST` | `MAT_DarkNeutral` | `8` | `24` | `8.3160` | `[+22.15, 0.88, +4.58]` to `[25.25, 2.20, 4.63]` |
| 52 | `GEO_Leaderboard_Podium_C3_3RD` | `MAT_DarkNeutral` | `22` | `66` | `22.3991` | `[+25.79, 0.52, +1.59]` to `[29.31, 1.50, 4.51]` |
| 53 | `GEO_Leaderboard_PodiumNameplate_C3_3RD` | `MAT_DarkNeutral` | `8` | `24` | `4.0120` | `[+26.10, 0.66, +4.48]` to `[29.00, 1.34, 4.53]` |

---

## 8. Collision Proxy Specification (`COL_Leaderboard_Body`)

The optional collision proxy (`meshes/collision_proxy/COL_Leaderboard_Body.obj`, `.mtl`, `.glb`) contains **`168` triangles** across **`5` named hull components** (`14` axis-aligned convex boxes):
1. `COL_Leaderboard_WallPlinthHull` (`12` tris): `X in [-11.0000, +31.0000]`, `Y in [0.0000, +3.1000]`, `Z in [-4.2000, +0.6000]`.
2. `COL_Leaderboard_MainWallHull` (`12` tris): `X in [-10.9400, +30.9400]`, `Y in [3.1000, +26.0000]`, `Z in [-4.1500, +0.6800]`.
3. `COL_Leaderboard_Stage_A_Hull` (`48` tris): Stage A deck box (`X in [-9.70, +2.30]`, `Y in [0.00, +0.52]`, `Z in [+0.60, +4.80]`) + 3 stepped podium boxes (`A2` `Y = 0.52..1.95`, `A1` `Y = 0.52..2.50`, `A3` `Y = 0.52..1.50`).
4. `COL_Leaderboard_Stage_B_Hull` (`48` tris): Stage B deck box (`X in [+4.00, +16.00]`, `Y in [0.00, +0.52]`, `Z in [+0.60, +4.80]`) + 3 stepped podium boxes (`B2` `Y = 0.52..1.95`, `B1` `Y = 0.52..2.50`, `B3` `Y = 0.52..1.50`).
5. `COL_Leaderboard_Stage_C_Hull` (`48` tris): Stage C deck box (`X in [+17.70, +29.70]`, `Y in [0.00, +0.52]`, `Z in [+0.60, +4.80]`) + 3 stepped podium boxes (`C2` `Y = 0.52..1.95`, `C1` `Y = 0.52..2.50`, `C3` `Y = 0.52..1.50`).

- **Avatar & Walk-Up Safety Proof:** `COL_Leaderboard_Body` contains **zero** geometry above `Y = 2.5000 / 1.9500 / 1.5000` in the foreground stage region (`Local Z in [+0.6800, +4.8000]`), leaving all 9 runtime avatar standing volumes, both `1.70-stud` inter-stage walkways, and the entire front plaza walk-up apron (`Local Z > +4.8000`) 100% unobstructed.
