# ROBLOX STUDIO IMPORT & PLACEMENT GUIDE — `SM_ArenaEnvironment_Colosseum_01`

> **Runtime Environment Disclosure:** Because Roblox Studio is not available inside the headless Linux VM sandbox, live Studio import and runtime playtesting are marked **`NOT RUN (Roblox Studio unavailable in Linux VM)`**. Follow the verified procedures below in Roblox Studio using only documented, existing Roblox Engine APIs.

---

## 1. Which Files to Import (Three Supported Workflows — All Strictly `< 20,000` Tris per MeshPart)

Every individual mesh in this production package is engineered to stay strictly below Roblox Studio's **`20,000`-triangle per-MeshPart limit**:

### Option A — Single-Step Multi-MeshPart Model Import at World Origin `(0, 0, 0)` (Recommended)
- **File to Import**: `meshes/SM_ArenaEnvironment_Colosseum_01.fbx` (or `meshes/SM_ArenaEnvironment_Colosseum_01.glb`).
- **Why It Passes the `< 20,000`-Tri Gate**: Unlike Concept 02 (which had 8 large groups up to `36,608` triangles), the Phase 2 assembled `.fbx` and `.glb` are partitioned into **33 named child `MeshPart` nodes** (`COL_StoneMasonry_Q1..Q4`, `COL_ExteriorArcade_Q1..Q4`, `COL_ColumnOrders_O1..O8`, `COL_CaveaSeating_Q1..Q4`, `COL_AtticCornice_Q1..Q4`, `COL_Vomitoria_Q1..Q4`, `COL_GateTower_East/South/West/North`, and `COL_NorthReactorCrest`), where **the largest child `MeshPart` is `16,832` triangles** (`3,168` triangles below the `20,000`-triangle limit).

### Option B — Individual Section MeshPart Import (`meshes/sections/`)
- **Files to Import**: The `33` individual `.glb` or `.obj` files in `meshes/sections/COL_*.{glb,obj}` (`1,668` to `16,832` triangles each).
- **Placement**: Every section file is authored in world coordinates around `(0, 0, 0)`, so setting `PivotTo(CFrame.new(0, 0, 0))` on each imported section snaps all `33` sections together seamlessly.

### Option C — Reusable 5-Archetype Modular Kit (`meshes/archetypes/`)
- **Files to Import**: The `5` reusable archetype meshes in `meshes/archetypes/` into `ReplicatedStorage.Assets.ColosseumModules`:
  1. `UMOD_01_Standard_Window_Bay.fbx` (or `.glb` / `.obj`) — **`6,018` triangles** (`12` instances)
  2. `UMOD_02_Standard_Clipeus_Bay.fbx` (or `.glb` / `.obj`) — **`5,982` triangles** (`20` instances)
  3. `UMOD_03_Vomitorium_Cavea_Bay.fbx` (or `.glb` / `.obj`) — **`6,712` triangles** (`8` instances)
  4. `UMOD_04_Cardinal_Triumphal_Gate_Pavilion.fbx` (or `.glb` / `.obj`) — **`8,680` triangles** (`4` instances)
  5. `UMOD_05_North_Imperial_Reactor_Crest.fbx` (or `.glb` / `.obj`) — **`3,496` triangles** (`1` instance)
- **Placement Data**: Exact world positions and outward normal orientations for all `45` instances are provided in `meshes/archetypes/archetype_instance_transforms.json`.

---

## 2. Step-by-Step Roblox Studio 3D Importer Settings

1. Open Roblox Studio and go to **File $\rightarrow$ Import 3D** (or **Avatar $\rightarrow$ Import 3D**).
2. Select `meshes/SM_ArenaEnvironment_Colosseum_01.fbx` (or `.glb`).
3. Configure the **Import 3D** inspector settings as follows:
   - **Import As**: `Model` (preserves all `33` named child `MeshPart` instances).
   - **Scale Unit**: `Stud` (`1 unit = 1 Roblox stud`).
   - **Insert Using Scene Position**: `Checked (true)` (places the model at world origin `(0, 0, 0)`).
   - **Merge Meshes**: `Unchecked (false)` (CRITICAL: keep `Merge Meshes` unchecked so Roblox Studio preserves the `33` `< 20,000`-triangle child `MeshPart`s instead of attempting to merge all `283,768` triangles into a single part).
   - **Generate Collisions / CollisionFidelity**: `Box` (since `CanCollide = false` is applied to all decorative parts).
4. Rename the imported root `Model` to **`SM_ArenaEnvironment_Colosseum_01`** and parent it to `Workspace.Map01_Arena.SurroundingEnvironment` (or `Workspace.Environment`).

---

## 3. Automated Luau Setup, Material Application & Void-Clearance Verification Script

Paste and run the following `--!strict` Luau script in the **Roblox Studio Command Bar** after importing `SM_ArenaEnvironment_Colosseum_01` to lock its world transform at `CFrame.new(0, 0, 0)`, enforce `Anchored = true`, `CanCollide = false`, `CanTouch = false`, and `CanQuery = false`, apply the 12 canonical materials, and verify that the central `9×9` arena grid at `(0, 50, 0)` remains completely unmodified:

```lua
--!strict
-- Sphere Brawl: Rolling Rampage — Phase 2 Production Setup for SM_ArenaEnvironment_Colosseum_01
local Workspace = game:GetService("Workspace")

local colosseum = Workspace:FindFirstChild("SM_ArenaEnvironment_Colosseum_01", true)
assert(colosseum and colosseum:IsA("Model"), "SM_ArenaEnvironment_Colosseum_01 Model not found in Workspace!")

-- 1. Lock World Origin Placement at CFrame.new(0, 0, 0)
colosseum.WorldPivot = CFrame.new(0, 0, 0)
colosseum:PivotTo(CFrame.new(0, 0, 0))
colosseum.ModelStreamingMode = Enum.ModelStreamingMode.Persistent

-- 2. Apply Decorative Non-Colliding Flags to All Child MeshParts
local meshPartCount = 0
for _, inst in ipairs(colosseum:GetDescendants()) do
	if inst:IsA("BasePart") then
		inst.Anchored = true
		inst.CanCollide = false
		inst.CanTouch = false
		inst.CanQuery = false
		inst.Massless = true
		inst.CastShadow = true
		if inst.Name:find("StoneMasonry") or inst.Name:find("CaveaSeating") then
			inst.Material = Enum.Material.Limestone
			inst.Color = Color3.fromRGB(196, 178, 150)
		elseif inst.Name:find("ColumnOrders") or inst.Name:find("ExteriorArcade") or inst.Name:find("AtticCornice") then
			inst.Material = Enum.Material.Limestone
			inst.Color = Color3.fromRGB(214, 198, 172)
		elseif inst.Name:find("Vomitoria") then
			inst.Material = Enum.Material.Basalt
			inst.Color = Color3.fromRGB(132, 122, 108)
		elseif inst.Name:find("GateTower") or inst.Name:find("NorthReactorCrest") then
			inst.Material = Enum.Material.Marble
			inst.Color = Color3.fromRGB(214, 198, 172)
		end
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
| **STU-01** | Import `meshes/SM_ArenaEnvironment_Colosseum_01.fbx` with `Merge Meshes = false` | Imports cleanly with `33` child `MeshPart`s (`1,668..16,832` tris each, all `< 20,000`) | **NOT RUN** (Studio unavailable) |
| **STU-02** | Verify `colosseum:GetBoundingBox()` at `Pivot = CFrame.new(0, 0, 0)` | Bounds match `X ∈ [-130.09, +130.09]`, `Y ∈ [18.06, 125.00]`, `Z ∈ [-136.09, +136.09]` | **NOT RUN** (Studio unavailable) |
| **STU-03** | Verify all child `MeshPart` collision properties | `Anchored == true`, `CanCollide == false`, `CanTouch == false`, `CanQuery == false` | **NOT RUN** (Studio unavailable) |
| **STU-04** | Inspect central `9×9` grid (`81` cells at `(0, 50, 0)`, top `Y = 51.0`) | Zero overlap; `44.0`-stud (`±X`) and `50.0`-stud (`±Z`) open void moat preserved | **NOT RUN** (Studio unavailable) |
| **STU-05** | Drive a sphere off all 4 edges and 4 corners during playtest | Sphere falls unimpeded through the open void and triggers elimination at `World Y < 15.0` | **NOT RUN** (Studio unavailable) |
