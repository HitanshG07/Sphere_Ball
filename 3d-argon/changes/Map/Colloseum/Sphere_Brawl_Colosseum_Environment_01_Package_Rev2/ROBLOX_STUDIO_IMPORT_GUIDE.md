# ROBLOX STUDIO IMPORT & PLACEMENT GUIDE — `SM_ArenaEnvironment_Colosseum_01` (Rev 2)

> **Runtime Environment Disclosure:** Because Roblox Studio is not available inside the headless Linux VM sandbox, live Studio import and runtime playtesting are marked **`NOT RUN (Roblox Studio unavailable in Linux VM)`**. Follow the verified procedures below in Roblox Studio using only documented, existing Roblox Engine APIs.
>
> **Verified Primary Formats vs. Secondary Formats:** **`OBJ` + `MTL` and `GLB`** are the **verified primary delivery formats** (`39/39` mesh sets audited for exact geometry, `vt` UVs, `vn` normals, portable relative `map_Kd` paths, and embedded `512×512` PNG texture bytes inside every `.glb`). The `.fbx` and `.gltf`/`.bin` files are included as secondary convenience exports.

---

## 1. Which Verified Files to Import (Three Supported Workflows — All Strictly `< 20,000` Tris per MeshPart)

Every individual section and archetype mesh in this production package is engineered to stay strictly below Roblox Studio's **`20,000`-triangle per-MeshPart limit**:

### Workflow A — Verified Section-Level Import (`meshes/sections/*.glb` or `*.obj` + `*.mtl`) (Most Reliable `< 20,000`-Tri Path)
- **Files to Import**: The **`33` individual section `.glb` files** (`meshes/sections/COL_*.glb`) or **`33` individual section `.obj` + `.mtl` pairs** (`meshes/sections/COL_*.obj` + `COL_*.mtl`).
- **How `meshes/sections/` Solves the Roblox `20,000`-Triangle Limit**:
  - The full `283,768`-triangle Colosseum is pre-split into `33` architectural section MeshParts ranging from **`1,668` triangles** (`COL_Vomitoria_Q1..Q4`) to **`16,832` triangles** (`COL_StoneMasonry_Q1..Q4`). Every file is strictly below the `20,000`-triangle cap (`3,168` triangles of safety headroom on the largest section).
- **Automatic Atlas & UV Mapping**:
  - Each section `.glb` embeds `textures/T_Colosseum_Production_Atlas_512.png` directly inside its binary buffer and binds `baseColorTexture` + `TEXCOORD_0`.
  - Each section `.obj` references its matching `.mtl` in `meshes/sections/`, whose `map_Kd ../../textures/T_Colosseum_Production_Atlas_512.png` resolves directly to the `512×512` atlas.
- **World-Origin Placement**: Every section mesh is authored in world coordinates around **`(0, 0, 0)`**, so importing with **Insert Using Scene Position = Checked** (or calling `PivotTo(CFrame.new(0, 0, 0))`) snaps all `33` sections together seamlessly around the `9×9` arena grid at `(0, 50, 0)`.

### Workflow B — Single-File Assembled Multi-Node Import (`meshes/SM_ArenaEnvironment_Colosseum_01.glb` or `.obj` + `.mtl`)
- **File to Import**: `meshes/SM_ArenaEnvironment_Colosseum_01.glb` (with embedded `512×512` PNG atlas) or `meshes/SM_ArenaEnvironment_Colosseum_01.obj` + `SM_ArenaEnvironment_Colosseum_01.mtl`.
- **Node Splitting Requirement**: The assembled `.glb` and `.obj` contain the exact same **`33` named child mesh nodes / `o` groups** (`1,668` to `16,832` triangles each). In Roblox Studio's **Import 3D** tool, ensure **Import As = Model** and **Merge Meshes = Unchecked (`false`)** so Studio preserves the `33` individual `< 20,000`-triangle child `MeshPart`s at world origin `(0, 0, 0)`. *(Note: `meshes/SM_ArenaEnvironment_Colosseum_01.fbx` and `.gltf`/`.bin` are also included as secondary convenience exports).*

### Workflow C — Reusable 5-Archetype Modular Kit (`meshes/archetypes/*.glb` or `*.obj` + `*.mtl`)
- **Files to Import**: Import the `5` reusable archetype meshes (`meshes/archetypes/UMOD_01..UMOD_05.glb` or `.obj` + `.mtl`) into `ReplicatedStorage.Assets.ColosseumModules`:
  1. `UMOD_01_Standard_Window_Bay.glb` (or `.obj`/`.mtl`) — **`6,018` triangles** (`12` instances)
  2. `UMOD_02_Standard_Clipeus_Bay.glb` (or `.obj`/`.mtl`) — **`5,982` triangles** (`20` instances)
  3. `UMOD_03_Vomitorium_Cavea_Bay.glb` (or `.obj`/`.mtl`) — **`6,712` triangles** (`8` instances)
  4. `UMOD_04_Cardinal_Triumphal_Gate_Pavilion.glb` (or `.obj`/`.mtl`) — **`8,680` triangles** (`4` instances)
  5. `UMOD_05_North_Imperial_Reactor_Crest.glb` (or `.obj`/`.mtl`) — **`3,496` triangles** (`1` instance)
- **Placement Data**: Exact world positions and outward normal orientations for all `45` instances (`283,768` total triangles) are provided in `meshes/archetypes/archetype_instance_transforms.json`.

---

## 2. Step-by-Step Roblox Studio 3D Importer Settings & Texture Application

1. Open Roblox Studio and select **File $ightarrow$ Import 3D** (or **Avatar $ightarrow$ Import 3D**).
2. Select either the `33` section files in `meshes/sections/COL_*.glb` (or `.obj`) **or** the assembled `meshes/SM_ArenaEnvironment_Colosseum_01.glb` (or `.obj`).
3. Configure the **Import 3D** settings:
   - **Import As**: `Model`
   - **Scale Unit**: `Stud` (`1 Blender unit = 1.0 Roblox stud`)
   - **Insert Using Scene Position**: `Checked (true)` (places the asset at world origin `(0, 0, 0)`)
   - **Merge Meshes**: `Unchecked (false)` (CRITICAL: keeps each of the `33` sections as an independent `< 20,000`-triangle `MeshPart`)
   - **Generate Collisions / CollisionFidelity**: `Box` (since all environment parts are non-colliding backdrop geometry)
4. **How `textures/T_Colosseum_Production_Atlas_512.png` Is Applied**:
   - **Via `.glb` Import**: Roblox Studio reads the embedded `512×512` PNG from `images[0]` (`baseColorTexture`) and automatically creates a `SurfaceAppearance` (or assigns `MeshPart.TextureID`) mapped via `TEXCOORD_0`.
   - **Via `.obj` + `.mtl` Import**: Roblox Studio resolves `mtllib` and the relative `map_Kd` path to `textures/T_Colosseum_Production_Atlas_512.png`.
   - **Manual Override / Verification**: If you upload `textures/T_Colosseum_Production_Atlas_512.png` separately to Roblox (`rbxassetid://<ATLAS_ID>`), set `MeshPart.TextureID = "rbxassetid://<ATLAS_ID>"` (or parent a `SurfaceAppearance` with `ColorMap = "rbxassetid://<ATLAS_ID>"`) on each of the `33` `MeshPart`s; all `vt` / `TEXCOORD_0` UVs are already pre-packed into the `512×512` atlas cells.
5. Group the imported parts under a `Model` named **`SM_ArenaEnvironment_Colosseum_01`** inside `Workspace.Map01_Arena.SurroundingEnvironment`.

---

## 3. Automated Luau Setup, Non-Collision & Void-Clearance Verification Script

Paste and run the following `--!strict` Luau script in the **Roblox Studio Command Bar** after importing `SM_ArenaEnvironment_Colosseum_01` to lock its world transform at `CFrame.new(0, 0, 0)` and enforce `Anchored = true`, `CanCollide = false`, `CanTouch = false`, and `CanQuery = false`:

```lua
--!strict
-- Sphere Brawl: Rolling Rampage — Phase 2 Rev 2 Setup for SM_ArenaEnvironment_Colosseum_01
local Workspace = game:GetService("Workspace")

local colosseum = Workspace:FindFirstChild("SM_ArenaEnvironment_Colosseum_01", true)
assert(colosseum and colosseum:IsA("Model"), "SM_ArenaEnvironment_Colosseum_01 Model not found in Workspace!")

-- 1. Lock World Origin Placement at CFrame.new(0, 0, 0)
colosseum.WorldPivot = CFrame.new(0, 0, 0)
colosseum:PivotTo(CFrame.new(0, 0, 0))
colosseum.ModelStreamingMode = Enum.ModelStreamingMode.Persistent

-- 2. Apply Decorative Non-Colliding Flags to All 33 Child MeshParts
local meshPartCount = 0
for _, inst in ipairs(colosseum:GetDescendants()) do
	if inst:IsA("BasePart") then
		inst.Anchored = true
		inst.CanCollide = false
		inst.CanTouch = false
		inst.CanQuery = false
		inst.Massless = true
		inst.CastShadow = true
		meshPartCount += 1
	end
end

print(string.format(
	"[SM_ArenaEnvironment_Colosseum_01] Configured %d non-colliding MeshParts at Pivot (0, 0, 0).",
	meshPartCount
))
```

---

## 4. Required Manual Verification Checklist in Roblox Studio (`NOT RUN` in Sandbox)

| Check ID | Studio Verification Step | Expected Result | Sandbox Status |
| :--- | :--- | :--- | :--- |
| **STU-01** | Import `meshes/sections/COL_*.glb` (or `SM_ArenaEnvironment_Colosseum_01.glb` with `Merge Meshes = false`) | Imports cleanly as `33` child `MeshPart`s (`1,668..16,832` tris each, all `< 20,000`) with embedded `512×512` atlas applied | **NOT RUN** (Studio unavailable) |
| **STU-02** | Verify `colosseum:GetBoundingBox()` at `Pivot = CFrame.new(0, 0, 0)` | Bounds match `X ∈ [-130.09, +130.09]`, `Y ∈ [18.06, 125.00]`, `Z ∈ [-136.09, +136.09]` | **NOT RUN** (Studio unavailable) |
| **STU-03** | Verify all child `MeshPart` collision properties | `Anchored == true`, `CanCollide == false`, `CanTouch == false`, `CanQuery == false` | **NOT RUN** (Studio unavailable) |
| **STU-04** | Inspect central `9×9` grid (`81` cells at `(0, 50, 0)`, top `Y = 51.0`) | Zero overlap; `44.0`-stud (`±X`) and `50.0`-stud (`±Z`) open void moat preserved | **NOT RUN** (Studio unavailable) |
| **STU-05** | Drive a sphere off all 4 edges and 4 corners during playtest | Sphere falls unimpeded through the open void and triggers elimination at `World Y < 15.0` | **NOT RUN** (Studio unavailable) |
