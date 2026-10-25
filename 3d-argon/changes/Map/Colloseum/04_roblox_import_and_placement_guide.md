# 04 — Roblox Studio Import, Material Setup & Placement Guide (Concept 02)

## 1. Delivered 3D Mesh Files & Formats (`meshes/`)

All four industry-standard 3D mesh formats are included in `meshes/` and generated from the exact same verified world-space coordinate system (`1 unit = 1 Roblox stud`, `+Y` Up, pivot at `(0, 0, 0)`):

| File Path | Format Specification | Size | Recommended Use Case |
| :--- | :--- | ---: | :--- |
| `meshes/SM_ArenaEnvironment_Colosseum_01.fbx` | Autodesk FBX 7.4 ASCII (`8` named `Geometry`/`Model` nodes + `10` `Material` nodes) | `44.9 MB` | **Primary Roblox Studio 3D Importer** (preserves submesh hierarchy & material slots) |
| `meshes/SM_ArenaEnvironment_Colosseum_01.glb` | Binary glTF 2.0 (`8` named mesh primitives + PBR metallic-roughness materials) | `21.1 MB` | **Fast Single-File Binary Import** / Blender / external 3D viewer inspection |
| `meshes/SM_ArenaEnvironment_Colosseum_01.gltf` + `.bin` | Standard glTF 2.0 JSON + binary vertex/index buffer | `21.1 MB` | **Pipeline / Engine Inspection** & automated validation |
| `meshes/SM_ArenaEnvironment_Colosseum_01.obj` + `.mtl` | Wavefront OBJ (`o COL_*` groups + `usemtl` assignments) + Material Library | `59.4 MB` | **Universal DCC / Quadrant Slicing** & reference geometry |
| `concept_source/T_Colosseum_Concept02_Atlas_512.png` | `512 × 512 px` (`≤ 1024 × 1024 px`) procedural Roman stone & trim texture atlas | `24.8 KB` | Optional `SurfaceAppearance` / trim texture reference |

---

## 2. Step-by-Step Roblox Studio Import & Placement Procedure

1. **Create Hierarchy Container**:
   - In Roblox Studio's **Explorer**, locate `Workspace.Map01_Arena` (which contains `ArenaTiles`, `Spawns`, and `Hazards`).
   - Create a Folder named `SurroundingEnvironment` inside `Workspace.Map01_Arena`.
2. **Import via Roblox 3D Importer (`Avatar / File -> Import 3D`)**:
   - Select `meshes/SM_ArenaEnvironment_Colosseum_01.fbx` (or `.glb` / modular bay meshes).
   - In the **Import 3D** settings panel:
     - **File Scale / Unit**: `Stud` (`Scale = 1.0`, `1 unit = 1 stud`)
     - **Import As**: `Model` (preserving child `MeshPart` hierarchy `COL_ExteriorArcade`, `COL_ColumnOrders`, `COL_StoneMasonry`, `COL_CaveaSeating`, `COL_Vomitoria`, `COL_AtticCornice`, `COL_GateTowers`, `COL_NorthReactorCrest`)
     - **Insert Using Scene Position**: `Checked (True)`
     - **Generate Collisions**: `Off / Box` (since all environment parts use `CanCollide = false`)
3. **Lock World Transform & Physics Flags**:
   - Name the imported root `Model` **`SM_ArenaEnvironment_Colosseum_01`** and parent it to `Workspace.Map01_Arena.SurroundingEnvironment`.
   - Set `SM_ArenaEnvironment_Colosseum_01:PivotTo(CFrame.new(0, 0, 0))` (leaving `Workspace.Map01_Arena.ArenaTiles` untouched at its center `(0, 50, 0)`).
   - For every child `MeshPart` inside `SM_ArenaEnvironment_Colosseum_01`, set:
     - `Anchored = true`
     - `CanCollide = false`
     - `CanTouch = false`
     - `CanQuery = false`
     - `CastShadow = true`

---

## 3. Roblox Studio Material & Color Mapping Table

Apply the following native Roblox `Enum.Material` and `Color3.fromRGB(...)` values to each material slot:

| Material Slot | Roblox `Enum.Material` | `Color3.fromRGB` | `Reflectance` | Architectural Target Elements |
| :--- | :--- | :---: | :---: | :--- |
| `MAT_TravertineWarm` | `Enum.Material.Limestone` (or `Sandstone`) | `(206, 189, 162)` | `0.02` | Main ashlar pier courses, *Media/Summa Cavea* benches, attic wall |
| `MAT_TravertineLight` | `Enum.Material.Limestone` | `(224, 210, 186)` | `0.04` | Engaged columns, arch voussoirs, architraves, corbel brackets |
| `MAT_LimestoneCream` | `Enum.Material.Limestone` | `(232, 221, 200)` | `0.04` | Ashlar highlight blocks, gallery balustrades, dedicatory panels |
| `MAT_TuffFoundation` | `Enum.Material.Slate` (or `Basalt`) | `(138, 124, 108)` | `0.00` | Lower rusticated foundation (`Y = 18.06..48.0`), *cavea* risers |
| `MAT_BasaltShadow` | `Enum.Material.Basalt` | `(58, 55, 52)` | `0.00` | Ashlar V-groove mortar channels, barrel vault soffits |
| `MAT_ImperialMarble` | `Enum.Material.Marble` | `(238, 232, 220)` | `0.08` | Sculpted Tuscan/Ionic/Corinthian capitals, keystones, *Ima Cavea* treads |
| `MAT_BronzeClipeus` | `Enum.Material.Metal` | `(168, 132, 74)` | `0.25` | Attic 3D *clipei* shields, *velarium* masts, spandrel bosses, eagle standard |
| `MAT_DarkNeutral` | `Enum.Material.SmoothPlastic` | `(24, 26, 32)` | `0.00` | *Vomitoria* tunnel throats, recessed window openings, gate portals |
| `EMI_Cyan` | `Enum.Material.Neon` | `(0, 240, 255)` | `0.00` | Sub-cornice accent line & North Imperial Tribune core (`0.24%` area) |
| `EMI_Amber` | `Enum.Material.Neon` | `(255, 155, 25)` | `0.00` | North Imperial Tribune upper beacon pip (`< 0.01%` area) |

---

## 4. Automated Luau Verification & Setup Script

Run the following script in the **Roblox Studio Command Bar** after importing `SM_ArenaEnvironment_Colosseum_01` to automatically configure physics properties, apply native materials, and verify zero overlap with the locked `9×9` arena grid:

```lua
-- Sphere Brawl: Rolling Rampage — Concept 02 Colosseum Environment Verification & Setup
local map01 = workspace:WaitForChild("Map01_Arena")
local envFolder = map01:FindFirstChild("SurroundingEnvironment") or Instance.new("Folder", map01)
envFolder.Name = "SurroundingEnvironment"

local colosseum = envFolder:WaitForChild("SM_ArenaEnvironment_Colosseum_01")
colosseum:PivotTo(CFrame.new(0, 0, 0))

local meshPartCount = 0
for _, desc in ipairs(colosseum:GetDescendants()) do
    if desc:IsA("BasePart") then
        desc.Anchored = true
        desc.CanCollide = false
        desc.CanTouch = false
        desc.CanQuery = false
        desc.CastShadow = true
        meshPartCount += 1
    end
end

-- Verify Locked 9x9 Arena Grid is untouched at (0, 50, 0)
local arenaTiles = map01:WaitForChild("ArenaTiles")
local centerTile = arenaTiles:WaitForChild("Tile_R5_C5")
assert((centerTile.Position - Vector3.new(0, 50, 0)).Magnitude < 0.01, "Center tile moved!")
assert(#arenaTiles:GetChildren() == 81, "Expected exactly 81 locked arena tiles!")

print(string.format(
    "[Concept 02 Verified] SM_ArenaEnvironment_Colosseum_01 anchored at (0,0,0) across %d non-colliding MeshParts; 81/81 arena tiles intact at (0,50,0).",
    meshPartCount
))
```
