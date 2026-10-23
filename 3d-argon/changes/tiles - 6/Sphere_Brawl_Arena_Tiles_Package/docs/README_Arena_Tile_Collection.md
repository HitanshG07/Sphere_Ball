# Sphere Brawl: Rolling Rampage — Arena Tile Collection (Material Correction & Finalization Guide)

## 1. Root Cause Analysis: Why Previous Tiles Appeared Pale Grey in Roblox Studio
Inspection of the previous package's `.obj`, `.mtl`, and `.glb` files revealed that while the **source files contained the exact RGB values** in `.mtl` (`Kd`/`Ke`) and `.glb` (`baseColorFactor`/`emissiveFactor`), they triggered four well-known **Roblox Studio 3D Importer** behaviors that caused all six tiles to appear pale grey (`Medium stone grey`, RGB `163, 162, 165`) upon import:

1. **Wavefront `.obj` Importer Ignores `.mtl` `Kd` / `Ke` Colors**: Roblox Studio's `.obj` importer reads geometry (`v`, `vt`, `vn`, `f`) and texture maps (`map_Kd`), but ignores solid `.mtl` diffuse (`Kd`) and emissive (`Ke`) scalar colors when no texture image is bound, defaulting every imported `MeshPart` to `Medium stone grey (163, 162, 165)`.
2. **Single-Mesh Multi-Primitive `.glb` Collapse**: In the previous `.glb` files, each tile had **1 `mesh` node with 4 material `primitives`** (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_*`), and **no `COLOR_0` vertex colors or `TEXCOORD_0` texture**. When a single mesh contains multiple material primitives without a texture, or when **"Import As Single Mesh"** is checked in Roblox Studio, the importer merges all 4 primitives into a single `MeshPart` and strips per-primitive `baseColorFactor` and `emissiveFactor`.
3. **Single `MeshPart` Material & Color Limitation in Roblox**: A single Roblox `MeshPart` only supports **one `Color` (`Color3`)** and **one `Material` (`Enum.Material`)** across the entire part. Even if you manually changed `MeshPart.Color` in Studio on the previous single-node mesh, it tinted the entire tile one flat color and could not combine `Enum.Material.Metal` (on structural armor) with `Enum.Material.Neon` (on hazard accents).
4. **Emissive (`Ke` / `emissiveFactor`) Does Not Auto-Convert to `Enum.Material.Neon`**: Neither `.obj`/`.mtl` nor `.glb` automatically switches a Roblox `MeshPart.Material` to `Enum.Material.Neon`. Achieving true self-illuminated hazard glow in Roblox Studio requires the emissive geometry (`EMI_*`) to be a separate child `MeshPart` set to `Enum.Material.Neon`.

## 2. How the Corrected Package Fixes Material Transfer & Studio Usability (Without Altering Geometry)
All locked geometric dimensions (`11.80 × 2.00 × 11.80` studs, centered origin `(0,0,0)`, `+Y` Up, `+Z` Forward, `84` base tris + `128–150` overlay tris = `212–234` complete tris `< 250`) are preserved 100% unchanged. The material definitions and scene hierarchy have been upgraded across every file:

1. **Multi-Node `.glb` Scene Hierarchy (`Part_<MaterialSlot>` Child Meshes)**:
   Every `.glb` file now exports a root model node (`SM_ArenaTile_01_SafeNormal`, etc.) with **separate named child nodes/meshes per material slot**:
   - `Part_MAT_DarkNeutral`
   - `Part_MAT_AltNeutral`
   - `Part_MAT_LightTrim`
   - `Part_EMI_Cyan` / `Part_EMI_Amber` / `Part_EMI_Ice` / `Part_EMI_Magnetic` / `Part_EMI_Kinetic` / `Part_EMI_DangerRed`
   When imported into Roblox Studio with **"Import As Model"** enabled (and **"Merge Meshes"** unchecked), Studio creates a `Model` with 4 cleanly separated `MeshPart` children that share the exact centered pivot `(0, 0, 0)`.
2. **Multi-Object `.obj` Grouping (`o <AssetName>__<MaterialSlot>`)**:
   Every `.obj` file now groups faces under distinct `o <AssetName>__<MaterialSlot>` object headers so `.obj` imports also split cleanly into 4 per-material child `MeshPart` instances.
3. **Baked Per-Vertex Colors (`COLOR_0`) + Palette Texture Atlas (`TEXCOORD_0` + Embedded PNG)**:
   Every `.glb` primitive now embeds `COLOR_0` (`VEC4` float32 vertex colors), `TEXCOORD_0` UV coordinates, and an embedded 96×96 PNG 3×3 swatch texture (`textures/SphereBrawl_ArenaTile_PaletteAtlas.png`, also referenced via `map_Kd` in every `.mtl`). Thus, even if imported as a single mesh or previewed with textures in Studio/Blender, the 9 approved RGB colors appear immediately instead of pale grey.

## 3. Exact Step-by-Step Roblox Studio Import & Material Setup Procedure

### Step A — 3D Importer Settings (`Asset Manager -> 3D Importer`)
1. Open **Roblox Studio** and click **Import 3D** (or **Asset Manager -> Bulk Import**).
2. Select the `.glb` (recommended) or `.obj` files from `meshes/complete_states/` (or `meshes/modular_base_and_overlays/`).
3. In the **3D Importer** panel on the left:
   - Under **Hierarchy / General**, keep **"Import As Model"** checked and make sure **"Merge Meshes" / "Import As Single Mesh" is UNCHECKED** so the 4 child parts (`Part_MAT_DarkNeutral`, `Part_MAT_AltNeutral`, `Part_MAT_LightTrim`, `Part_EMI_*`) remain separate `MeshPart` instances inside the imported `Model`.
   - Set **Scale Unit** = `Studs` (`1.0 unit = 1.0 stud`), **Up Axis** = `+Y`, **Forward Axis** = `+Z`.
   - Confirm that the root `Model` bounding box measures **`11.8 × 2.0 × 11.8` studs**. Do **not** resize the visual model to `12 × 2 × 12`; the `0.2`-stud border gap on a `12.0`-stud grid pitch is intentional, and the `12 × 2 × 12` gameplay collider is separate and owned by gameplay code.

### Step B — Applying Native `Enum.Material.Metal` & `Enum.Material.Neon` in Studio
Because glTF/OBJ exports cannot automatically set Roblox's proprietary `Enum.Material.Neon` shader or `Enum.Material.Metal` reflectance, apply the native Roblox materials to the 4 child `MeshPart` instances inside each imported `Model` using **either** the Explorer/Properties panel or the one-line Command Bar helper:

| Child `MeshPart` Name (in Imported Model) | Approved RGB (`0–255`) | sRGB Hex | Exact Roblox `Color3` Value | Required Roblox `Material` | Surface Role & Studio Notes |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **`Part_MAT_DarkNeutral`** | `(32, 38, 54)` | `#202636` | `Color3.fromRGB(32, 38, 54)` | `Enum.Material.Metal` | Primary dark metallic hull, corner bolsters, and top armor plates. Clear `TextureID` (`""`) if using `Part.Color`. |
| **`Part_MAT_AltNeutral`** | `(42, 50, 70)` | `#2A3246` | `Color3.fromRGB(42, 50, 70)` | `Enum.Material.Metal` | Recessed interior deck floor (`Y = +0.86` studs). Clear `TextureID` (`""`) if using `Part.Color`. |
| **`Part_MAT_LightTrim`** | `(170, 190, 215)` | `#AABED7` | `Color3.fromRGB(170, 190, 215)` | `Enum.Material.Metal` | Chamfered upper perimeter frame (`Y = +1.00`), inductor poles, and rail cleats. |
| **`Part_EMI_Cyan`** *(State 1: Safe / Normal)* | `(0, 195, 255)` | `#00C3FF` | `Color3.fromRGB(0, 195, 255)` | `Enum.Material.Neon` | Restrained cross-axis cyan seam inlays. **Must be set to `Neon` in Studio** for emissive glow. |
| **`Part_EMI_Amber`** *(State 2: Warning)* | `(255, 170, 0)` | `#FFAA00` | `Color3.fromRGB(255, 170, 0)` | `Enum.Material.Neon` | Amber caution perimeter and radial warning bars. **Must be set to `Neon` in Studio**. |
| **`Part_EMI_Ice`** *(State 3: Ice Corridor — active)* | `(0, 235, 255)` | `#00EBFF` | `Color3.fromRGB(0, 235, 255)` | `Enum.Material.Neon` | Four longitudinal ice-blue cryo channels & frost bridges. **Must be set to `Neon` in Studio**. |
| **`Part_EMI_Magnetic`** *(State 4: Magnetic Storm — active)* | `(165, 55, 255)` | `#A537FF` | `Color3.fromRGB(165, 55, 255)` | `Enum.Material.Neon` | Symmetric concentric octagonal purple field rings. **Must be set to `Neon` in Studio**. |
| **`Part_EMI_Kinetic`** *(State 5: Boost Runway — active)* | `(255, 125, 0)` | `#FF7D00` | `Color3.fromRGB(255, 125, 0)` | `Enum.Material.Neon` | Three forward (`+Z`) orange acceleration chevrons. **Must be set to `Neon` in Studio**. |
| **`Part_EMI_DangerRed`** *(State 6: Ring Collapse — warning)* | `(255, 40, 40)` | `#FF2828` | `Color3.fromRGB(255, 40, 40)` | `Enum.Material.Neon` | Danger-red perimeter bars, diagonal X-motif, and center core. **Must be set to `Neon` in Studio**. |
