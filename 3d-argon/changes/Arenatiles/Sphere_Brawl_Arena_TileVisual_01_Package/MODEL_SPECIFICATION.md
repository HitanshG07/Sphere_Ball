# MODEL SPECIFICATION — `SM_Arena_TileVisual_01` & Modular Hazard Overlays

| Specification Field | Value |
| :--- | :--- |
| **Canonical Asset ID** | `SM_Arena_TileVisual_01` |
| **Scale Convention** | `1 Blender unit = 1.0 Roblox stud` (`+Y` Up, `-Z` Forward) |
| **Base Local Origin** | `(0.0000, 0.0000, 0.0000)` at the geometric center of the `11.8000 × 2.0000 × 11.8000` visual tile |
| **Base Local Bounding Box** | `Local X in [-5.9000, +5.9000]`, `Local Y in [-1.0000, +1.0000]`, `Local Z in [-5.9000, +5.9000]` |
| **Overlay Local Origin** | `(0.0000, 0.0000, 0.0000)` (Shared local origin with the base tile so overlay aligns at `Local Y in [+1.0000, +1.0500]`) |
| **Overlay Local Bounding Box** | `Local X in [-5.7000, +5.7000]`, `Local Y in [+1.0000, +1.0500]`, `Local Z in [-5.7000, +5.7000]` (`11.4000 × 0.0500 × 11.4000 studs`) |
| **Overlay Geometric Center** | `Local (0.0000, +1.0250, 0.0000)` -> `World (12x, 51.0250, 12z)` when cell center is at `World Y = 50.0000` |
| **Palette Texture Atlas** | `textures/T_Arena_TilePalette_256.png` (`256 × 256 px`, `933` bytes, `SHA-256: 3ab02901089d986685060313261da32d2f121c31979bb4b996dd41a3685f6e06`) |

## 1. Base Visual Tile Component Hierarchy & Geometry (`152 Triangles` / `456 Vertices`)

Both `SM_Arena_TileVisual_01_VariantA` and `SM_Arena_TileVisual_01_VariantB` contain the exact same `5` named components, `152` triangles, and `456` vertices:

| Component Name | Triangles | Vertices | Variant A Material | Variant B Material | Local Bounding Box (`min` -> `max`) | Geometric Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`COMP_Arena_TileBevelFrame_118`** | `70` | `210` | `MAT_DarkNeutral` (`#202636`) | `MAT_AltNeutral` (`#2A3246`) | `[-5.90, -1.00, -5.90]` -> `[+5.90, +1.00, +5.90]` | Outer `11.8 × 2.0 × 11.8` armor skirt, `0.25-stud` 45° top & bottom chamfers, bottom cap, and `1.05-stud` top perimeter collar at `Y = +1.0000`. |
| **`GEO_Tile_CyanCircuitInlay`** | `24` | `72` | `EMI_Cyan` (`#00C3FF`) | `EMI_Cyan` (`#00C3FF`) | `[-5.25, +0.985, -5.25]` -> `[+5.25, +1.00, +5.25]` | `0.20-stud` wide recessed octagonal cyan energy channel (`Y = +0.9850..+1.0000`) plus 4 cardinal bus ticks (`Y = +0.9990`). |
| **`GEO_Tile_CenterDeckPlate`** | `22` | `66` | `MAT_AltNeutral` (`#2A3246`) | `MAT_DarkNeutral` (`#202636`) | `[-4.40, +0.985, -4.40]` -> `[+4.40, +1.00, +4.40]` | Inner octagonal rolling deck stepping up from `Y = +0.9850` to a flat top cap at `Local Y = +1.0000` (`World Y = 51.0000`). |
| **`GEO_Tile_CornerTrimLock_04`** | `16` | `48` | `MAT_LightTrim` (`#AABED7`) | `MAT_LightTrim` (`#AABED7`) | `[-5.18, +0.999, -5.18]` -> `[+5.18, +0.999, +5.18]` | Four restrained L-shaped metallic corner brackets (`2 quads = 4 tris` per corner) inset inside the top perimeter collar. |
| **`GEO_Tile_UndersideRibs`** | `20` | `60` | `MAT_AltNeutral` (`#2A3246`) | `MAT_DarkNeutral` (`#202636`) | `[-5.80, -0.95, -1.65]` -> `[+5.80, -0.45, +1.65]` | Two parallel underside structural beams (`Y in [-0.9500, -0.4500]`) visible during ring-collapse sink/tilt. |
| **TOTAL BASE VISUAL TILE** | **`152`** | **`456`** | **4 Materials** | **4 Materials** | **`[-5.90, -1.00, -5.90]` -> `[+5.90, +1.00, +5.90]`** | **Strictly `<= 170` base triangle target (`18` tris margin).** |

### Surface Area Distribution by Material (`Variant A` vs. `Variant B`)
- **Variant A (`(x + z) % 2 == 0`):** `MAT_DarkNeutral` = `64.57%`, `MAT_AltNeutral` = `32.51%`, `EMI_Cyan` = `1.88%`, `MAT_LightTrim` = `1.04%`.
- **Variant B (`(x + z) % 2 != 0`):** `MAT_AltNeutral` = `64.57%`, `MAT_DarkNeutral` = `32.51%`, `EMI_Cyan` = `1.88%`, `MAT_LightTrim` = `1.04%`.

## 2. Modular Non-Colliding Hazard Overlay Specifications (`meshes/overlays/`)

Every overlay asset is exported with its local origin at `(0.0000, 0.0000, 0.0000)` (matching the base tile's geometric center) so that its vertices span `Local Y in [+1.0000, +1.0500]` (geometric center `Local Y = +1.0250`, or `World Y = 51.0250` when the cell is at `World Y = 50.0000`). If imported into Roblox Studio as a `Model` or `MeshPart` whose bounding-box center is used as its `Position`, its world position is `tileCenter + Vector3.new(0, 1.025, 0)`.

| Overlay Asset Name | Triangles | Vertices | Components | Local Bounds (`min` -> `max`) | Used Material Slots | Supported Runtime Rotations (Yaw around `+Y`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`OVL_Arena_Warn_Ice`** | `38` | `114` | `4` | `[-5.70, +1.00, -5.70]` -> `[+5.70, +1.05, +5.70]` | `MAT_DarkNeutral`, `EMI_Amber`, `EMI_Ice`, `MAT_PrimaryText` | `0°`, `45°`, `90°`, `135°` (rotates inner motif or overlay) |
| **`OVL_Arena_Active_Ice`** | `38` | `114` | `5` | `[-5.70, +1.00, -5.70]` -> `[+5.70, +1.05, +5.70]` | `MAT_AltNeutral`, `EMI_Ice`, `EMI_Cyan`, `MAT_PrimaryText` | `0°`, `45°`, `90°`, `135°` |
| **`OVL_Arena_Warn_Magnetic`** | `56` | `168` | `4` | `[-5.70, +1.00, -5.70]` -> `[+5.70, +1.05, +5.70]` | `MAT_DarkNeutral`, `EMI_Amber`, `EMI_Magnetic` | `0°` (radially symmetric) |
| **`OVL_Arena_Active_MagneticAnchor`** | `72` | `216` | `7` | `[-5.70, +1.00, -5.70]` -> `[+5.70, +1.05, +5.70]` | `MAT_DarkNeutral`, `EMI_Magnetic`, `MAT_PrimaryText` | `0°` (radially symmetric) |
| **`OVL_Arena_Active_MagneticField`** | `42` | `126` | `4` | `[-5.70, +1.00, -5.70]` -> `[+5.70, +1.05, +5.70]` | `MAT_DarkNeutral`, `EMI_Magnetic`, `MAT_PrimaryText` | `0°`, `90°`, `180°`, `270°` (points toward anchor cell) |
| **`OVL_Arena_Warn_Boost`** | `34` | `102` | `4` | `[-5.70, +1.00, -5.70]` -> `[+5.70, +1.05, +5.70]` | `MAT_DarkNeutral`, `EMI_Amber`, `EMI_Kinetic` | `0°`, `90°`, `180°`, `270°` (unified one-way runway vector) |
| **`OVL_Arena_Active_Boost`** | `36` | `108` | `7` | `[-5.70, +1.00, -5.70]` -> `[+5.70, +1.05, +5.70]` | `MAT_DarkNeutral`, `EMI_Kinetic`, `EMI_Amber`, `MAT_PrimaryText` | `0°`, `90°`, `180°`, `270°` (unified one-way runway vector) |
| **`OVL_Arena_Collapse_Warn`** | `32` | `96` | `4` | `[-5.70, +1.00, -5.70]` -> `[+5.70, +1.05, +5.70]` | `MAT_DarkNeutral`, `EMI_DangerRed`, `MAT_PrimaryText` | `0°` (applied to `D=4` and `D=3` ring cells) |

## 3. Complete Per-Cell Allowed State Triangle Budget Table (Hard Gate `<= 249` Triangles)

| Allowed Visual Cell State | Base Tile Mesh (`Variant A` or `B`) | Simultaneous Hazard Overlay Mesh | Base Triangles | Overlay Triangles | Total Combined Cell Triangles | Hard Cap (`<= 249`) | Gate Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Safe Tile (Even Parity)** | `SM_Arena_TileVisual_01_VariantA` | *None* | `152` | `0` | **`152`** | `249` | **PASS (`-97`)** |
| **2. Safe Tile (Odd Parity)** | `SM_Arena_TileVisual_01_VariantB` | *None* | `152` | `0` | **`152`** | `249` | **PASS (`-97`)** |
| **3. Ice Corridor Warning** | `SM_Arena_TileVisual_01_VariantA/B` | `OVL_Arena_Warn_Ice` | `152` | `38` | **`190`** | `249` | **PASS (`-59`)** |
| **4. Ice Corridor Active** | `SM_Arena_TileVisual_01_VariantA/B` | `OVL_Arena_Active_Ice` | `152` | `38` | **`190`** | `249` | **PASS (`-59`)** |
| **5. Magnetic Storm Warning** | `SM_Arena_TileVisual_01_VariantA/B` | `OVL_Arena_Warn_Magnetic` | `152` | `56` | **`208`** | `249` | **PASS (`-41`)** |
| **6. Magnetic Storm Active (Anchor)** | `SM_Arena_TileVisual_01_VariantA/B` | `OVL_Arena_Active_MagneticAnchor` | `152` | `72` | **`224`** | `249` | **PASS (`-25`)** |
| **7. Magnetic Storm Active (Field)** | `SM_Arena_TileVisual_01_VariantA/B` | `OVL_Arena_Active_MagneticField` | `152` | `42` | **`194`** | `249` | **PASS (`-55`)** |
| **8. Boost Runway Warning** | `SM_Arena_TileVisual_01_VariantA/B` | `OVL_Arena_Warn_Boost` | `152` | `34` | **`186`** | `249` | **PASS (`-63`)** |
| **9. Boost Runway Active** | `SM_Arena_TileVisual_01_VariantA/B` | `OVL_Arena_Active_Boost` | `152` | `36` | **`188`** | `249` | **PASS (`-61`)** |
| **10. Ring-Collapse 3.0s Warning & Sink** | `SM_Arena_TileVisual_01_VariantA/B` | `OVL_Arena_Collapse_Warn` | `152` | `32` | **`184`** | `249` | **PASS (`-65`)** |

### Full-Board 81-Cell Instance Statistics (Counting Base & Overlay Instances Separately)
- **81 Base Tile Instances (`41 × Variant A` + `40 × Variant B`):** `81 × 152 = 12,312 triangles` (`36,936 vertices`).
- **Maximum Active Hazard Overlay Instances (`floor(81 × 0.35) = 28` simultaneous hazard cells):**
  - Minimum overlay load (`28 × 32 tris` Collapse/Boost): `+896` to `+1,008 triangles` -> **`13,208 to 13,320` total board triangles**.
  - Typical mixed pulse (`28 × ~40 tris`): **`~13,432` total board triangles**.
  - Theoretical worst-case pulse (`1` Magnetic Anchor `72 tris` + `27` Magnetic Warning `56 tris`): `12,312 + 72 + 1,512 =` **`13,896` total board triangles** (`6,273 triangles` below the `20,169` full-board ceiling).

## 4. Exact Material Palette & Texture Specification

All 10 material slots map to both `MTL`/`GLB` PBR properties and `textures/T_Arena_TilePalette_256.png` (`256 × 256 px`, `933` bytes, `SHA-256: 3ab02901089d986685060313261da32d2f121c31979bb4b996dd41a3685f6e06`):

| Material Slot | sRGB `(R, G, B)` | Hex | Roblox `Enum.Material` | Roblox `Color3` | Metallic / Roughness | Emissive | Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MAT_DarkNeutral` | `(32, 38, 54)` | `#202636` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `0.55 / 0.42` | `false` | Primary body & Variant A outer bevel frame; overlay carrier |
| `MAT_AltNeutral` | `(42, 50, 70)` | `#2A3246` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `0.60 / 0.35` | `false` | Alternate checker frame (Variant B); Variant A deck; Ice carrier |
| `MAT_LightTrim` | `(170, 190, 215)` | `#AABED7` | `Enum.Material.Metal` | `Color3.fromRGB(170, 190, 215)` | `0.78 / 0.28` | `false` | Restrained corner L-brackets (`GEO_Tile_CornerTrimLock_04`) |
| `MAT_PrimaryText` | `(245, 248, 255)` | `#F5F8FF` | `Enum.Material.Neon` | `Color3.fromRGB(245, 248, 255)` | `0.10 / 0.20` | `true` | High-contrast pale ice chevrons, magnetic pull arrows, turbine bar |
| `EMI_Cyan` | `(0, 195, 255)` | `#00C3FF` | `Enum.Material.Neon` | `Color3.fromRGB(0, 195, 255)` | `0.10 / 0.15` | `true` | Safe-state recessed energy conduit (`GEO_Tile_CyanCircuitInlay`) |
| `EMI_Ice` | `(0, 235, 255)` | `#00EBFF` | `Enum.Material.Neon` | `Color3.fromRGB(0, 235, 255)` | `0.10 / 0.15` | `true` | Ice Corridor active frost frame & 6-bar snowflake icon |
| `EMI_Magnetic` | `(165, 55, 255)` | `#A537FF` | `Enum.Material.Neon` | `Color3.fromRGB(165, 55, 255)` | `0.12 / 0.16` | `true` | Magnetic Storm anchor core, concentric 2D rings & field chevrons |
| `EMI_Kinetic` | `(255, 125, 0)` | `#FF7D00` | `Enum.Material.Neon` | `Color3.fromRGB(255, 125, 0)` | `0.14 / 0.18` | `true` | Boost Runway directional chevrons, side rails & turbine intake |
| `EMI_Amber` | `(255, 170, 0)` | `#FFAA00` | `Enum.Material.Neon` | `Color3.fromRGB(255, 170, 0)` | `0.15 / 0.18` | `true` | Pre-hazard warning border, corner alert triangles & boost accents |
| `EMI_DangerRed` | `(255, 40, 40)` | `#FF2828` | `Enum.Material.Neon` | `Color3.fromRGB(255, 40, 40)` | `0.15 / 0.18` | `true` | Ring-collapse 3.0s warning border flash & fracture crack decals |
