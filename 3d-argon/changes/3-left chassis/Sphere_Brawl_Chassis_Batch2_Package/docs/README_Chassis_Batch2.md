# Sphere Brawl: Rolling Rampage — TASK-09 Asset Batch 2: Chassis Models Guide

## 1. Overview & Cosmetic Parity Contract (`D-008`, `MASTER_IMPLEMENTATION_PLAN.md` §8.2)
This package delivers the three **TASK-09 Batch 2 Player Sphere Chassis** models:
1. **`SM_Chassis_Trickster_01`** (`sphere.shell.trickster`) — Agile, sleek, asymmetric diagonal slash vanes, canted swept stabilizer blades, cyan sensor visor (`EMI_Cyan`), and kinetic orange speed vents (`EMI_Kinetic`).
2. **`SM_Chassis_Magnetar_01`** (`sphere.shell.magnetar`) — Magnetic/energy-themed sphere with a raised 8-segment purple electromagnetic equatorial flux ring (`EMI_Magnetic`), polar inductor cores, four metallic horseshoe pole shoes (`MAT_LightTrim`), and cyan resonance emitters (`EMI_Cyan`).
3. **`SM_Chassis_Bulwark_01`** (`sphere.shell.bulwark`) — Sturdy, defensive, heavy-looking sphere built from 16 interlocking octagonal/geodesic dark bastion plates (`MAT_DarkNeutral` / `MAT_AltNeutral`), reinforced light-trim collars (`MAT_LightTrim`), and a narrow cyan tactical slit visor (`EMI_Cyan`).

**Hard Technical & Gameplay Constraints Preserved:**
- **Cosmetic-Only Parity (`D-008`)**: All four chassis (`Rammer`, `Trickster`, `Magnetar`, `Bulwark`) have identical gameplay stats (`OutgoingFactor = 1.0`, `ResistanceFactor = 1.0` in `src/shared/Config/ChassisConfig.luau`) and are strictly non-colliding client visual shells (`CanCollide = false`, `CanTouch = false`, `CanQuery = false`, `Massless = true`).
- **Sphere Collider Envelope (`R <= 2.970` Studs)**: Every vertex across all three chassis sits strictly inside `R <= 2.970` studs from the local origin `(0, 0, 0)` (`Trickster` max `R = 2.9450` studs, `Magnetar` max `R = 2.9550` studs, `Bulwark` max `R = 2.9620` studs), fitting safely inside the `R = 3.000`-stud (`6.0`-stud diameter) invisible `SphereRoot` physics collider.
- **Triangle Budget (`<= 250` Triangles)**: Every complete chassis stays strictly below `250` triangles (`Trickster = 236` tris, `Magnetar = 232` tris, `Bulwark = 232` tris) with `0` degenerate faces, `0` normal mismatches, and `0` floating/disconnected parts.

## 2. Proven Multi-Node `.glb` & Multi-Object `.obj` Material Workflow for Roblox Studio
Following the exact material workflow proven in the Arena Tile package, every `.glb` and `.obj` in `meshes/` is pre-split by material slot into named child `MeshPart` nodes (`Part_MAT_DarkNeutral`, `Part_MAT_AltNeutral`, `Part_MAT_LightTrim`, `Part_EMI_*`) AND includes baked `COLOR_0` vertex colors plus an embedded 96×96 PNG palette texture atlas (`textures/SphereBrawl_Chassis_PaletteAtlas.png`).

### Step-by-Step Roblox Studio Import Checklist (Recommended Format: `.glb`)
1. Open a **separate scratch Roblox Studio test place** (do **not** import into or save over `place/Gate0.rbxl`).
2. Open **Import 3D** (`Asset Manager -> Import 3D`) and select `SM_Chassis_Trickster_01.glb`, `SM_Chassis_Magnetar_01.glb`, and `SM_Chassis_Bulwark_01.glb` from `meshes/`.
3. In the **3D Importer** left panel:
   - **Import As Model**: **Checked** (`true`).
   - **Merge Meshes / Import As Single Mesh**: **UNCHECKED** (`false`) so the child `MeshPart`s (`Part_MAT_*`, `Part_EMI_*`) remain separate.
   - **Scale Unit**: `Studs` (`1.0 unit = 1.0 stud`), **Up Axis**: `+Y`, **Forward Axis**: `+Z`.
4. After inserting each `Model`, select all child `MeshPart`s and set:
   - `CanCollide = false`, `CanTouch = false`, `CanQuery = false`, `Massless = true`, `Anchored = false` (or `Anchored = true` only while inspecting statically; in gameplay, `SphereVisualRig` updates the visual shell CFrame in `PreRender` outside the physics assembly per `MASTER_IMPLEMENTATION_PLAN.md` §8.1).
5. To apply native Roblox `Metal` and `Neon` shaders on each child `MeshPart`, clear `TextureID = ""` and set:

| Child `MeshPart` Name | Approved RGB (`0–255`) | Hex | Exact Roblox `Color3` Value | Required Roblox `Material` | Used By Chassis |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **`Part_MAT_DarkNeutral`** | `(32, 38, 54)` | `#202636` | `Color3.fromRGB(32, 38, 54)` | `Enum.Material.Metal` | Trickster, Magnetar, Bulwark |
| **`Part_MAT_AltNeutral`** | `(42, 50, 70)` | `#2A3246` | `Color3.fromRGB(42, 50, 70)` | `Enum.Material.Metal` | Trickster, Magnetar, Bulwark |
| **`Part_MAT_LightTrim`** | `(170, 190, 215)` | `#AABED7` | `Color3.fromRGB(170, 190, 215)` | `Enum.Material.Metal` | Trickster, Magnetar, Bulwark |
| **`Part_EMI_Cyan`** | `(0, 195, 255)` | `#00C3FF` | `Color3.fromRGB(0, 195, 255)` | `Enum.Material.Neon` | Trickster, Magnetar, Bulwark |
| **`Part_EMI_Magnetic`** | `(165, 55, 255)` | `#A537FF` | `Color3.fromRGB(165, 55, 255)` | `Enum.Material.Neon` | Magnetar |
| **`Part_EMI_Kinetic`** | `(255, 125, 0)` | `#FF7D00` | `Color3.fromRGB(255, 125, 0)` | `Enum.Material.Neon` | Trickster |
