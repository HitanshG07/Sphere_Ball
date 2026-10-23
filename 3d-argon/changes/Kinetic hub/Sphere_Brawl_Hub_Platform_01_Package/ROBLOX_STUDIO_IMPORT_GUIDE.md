# Roblox Studio Import & Integration Guide — `SM_Hub_PlazaPlatform_01`

## 1. Recommended Import File & 3D Importer Settings

Use **`meshes/SM_Hub_PlazaPlatform_01.glb`** (preferred) or **`meshes/SM_Hub_PlazaPlatform_01.obj`** via **Avatar / File -> Import 3D** in Roblox Studio.

| Importer Setting | Required Value | Why It Matters |
|---|---|---|
| **Import As Model** | `Enabled (true)` | Preserves the root `SM_Hub_PlazaPlatform_01` `Model` container |
| **Merge Meshes** | `Disabled (false)` | Keeps the 7 named `GEO_PlazaPlatform_*` child `MeshPart`s separate so native `Enum.Material.Metal` and `Enum.Material.Neon` can be assigned per component |
| **Scale Unit** | `Studs (1.0 Unit = 1.0 Stud)` | Produces the exact locked `140.0 × 12.0 × 140.0 stud` dimensions |
| **Up / Forward Axis** | `+Y Up`, `+Z Forward` (or `-Z Forward` standard glTF) | Symmetrical across cardinal axes (`±X`, `±Z`) with cardinal walkway bridges aligned to `0°, 90°, 180°, 270°` |
| **Anchor All Parts** | `Enabled (true)` | Static lobby environment platform must be `Anchored = true` |

## 2. Exact World Placement & Pivot Alignment (`World Y = 150.0000` Top Surface)

The mesh vertices are authored with **`Local (0, 0, 0)` at the exact center of the top walking surface** (`Local Y in [-12.0000, 0.0000]`).

When imported into Roblox Studio, verify or apply the placement using either method below in the Command Bar or `LobbyService.luau`:

```luau
local Workspace = game:GetService("Workspace")
local platform = Workspace:WaitForChild("SM_Hub_PlazaPlatform_01")

-- Ensure the Model pivot sits at Local (0, 0, 0) (the top walking surface center)
-- Note: Since the bounding box spans Y in [-12, 0], its geometric bounding-box center is 6 studs below the top surface.
local bboxCFrame, bboxSize = platform:GetBoundingBox()
-- Expected bboxSize: Vector3.new(140, 12, 140)
local topSurfaceWorldPivot = CFrame.new(bboxCFrame.Position + Vector3.new(0, bboxSize.Y * 0.5, 0))
platform.WorldPivotData = Instance.new("Pivot") -- or set WorldPivot directly:
platform.WorldPivot = topSurfaceWorldPivot

-- Pivot the platform to the locked Hub center (0, 150, -300)
platform:PivotTo(CFrame.new(0, 150, -300))
-- Verification: Bounding-box center is now (0, 144, -300) and top walking surface is at exact World Y = 150.0!
```

## 3. Native Roblox Material & Color3 Assignment

Although `SM_Hub_PlazaPlatform_01.glb` and `.obj` include baked vertex colors (`COLOR_0`) and an embedded PNG palette texture (`SphereBrawl_HubPlatform_PaletteAtlas.png`) so the model never imports as pale grey, **glTF/OBJ emissive factors do not automatically set `Enum.Material.Neon` in Roblox Studio**. Run the following setup snippet (or assign in the Properties panel) after import:

| Child `MeshPart` Name | `MeshPart.Material` | `MeshPart.Color` (`Color3.fromRGB`) | Hex | Role |
|---|---|---|---|---|
| `GEO_PlazaPlatform_Deck` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | Primary walkable deck surface |
| `GEO_PlazaPlatform_Rim` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | Outer structural rim & vertical sidewall |
| `GEO_PlazaPlatform_Underside` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | Lower hull & central keel |
| `GEO_PlazaPlatform_DeckInlays` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | Flush top-deck sector inlays & channel bevels |
| `GEO_PlazaPlatform_Structure` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | Stepped mid-hull & 8 radial underside box-girders |
| `GEO_PlazaPlatform_Trim` | `Enum.Material.Metal` | `Color3.fromRGB(170, 190, 215)` | `#AABED7` | Rim bevels, brackets, cleats, and soffit gussets |
| `GEO_PlazaPlatform_CyanAccents` | `Enum.Material.Neon` | `Color3.fromRGB(0, 195, 255)` | `#00C3FF` | Recessed cyan conduits & perimeter status diodes |

```luau
local MATERIAL_MAP = {
	GEO_PlazaPlatform_Deck        = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
	GEO_PlazaPlatform_Rim         = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
	GEO_PlazaPlatform_Underside   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
	GEO_PlazaPlatform_DeckInlays  = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
	GEO_PlazaPlatform_Structure   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
	GEO_PlazaPlatform_Trim        = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(170, 190, 215) },
	GEO_PlazaPlatform_CyanAccents = { Mat = Enum.Material.Neon,  Color = Color3.fromRGB(0, 195, 255) },
}

for _, desc in ipairs(platform:GetDescendants()) do
	if desc:IsA("MeshPart") then
		desc.Anchored = true
		local spec = MATERIAL_MAP[desc.Name]
		if spec then
			desc.TextureID = "" -- Clear atlas texture when using native Roblox Material + Color3
			desc.Material = spec.Mat
			desc.Color = spec.Color
		end
	end
end
```

## 4. Walkability & Collision Setup (`LobbyWorld` Collision Group)

To guarantee 100% smooth R15 avatar walkability across the entire 140-stud plaza with zero convex-hull seam snagging:

1. **Recommended Authoritative Collider Setup (Invisible Native Cylinder Part or `COL_PlazaPlatform_Deck`):**
   - Set all 7 visual `GEO_PlazaPlatform_*` `MeshPart`s to `CanCollide = false`, `CanTouch = false`, `CanQuery = false`.
   - Use either:
     - **Option A (Native Roblox Cylinder Part — Fastest Physics):** Create an anchored, invisible `Part` named `COL_PlazaPlatform_Deck` with `Shape = Enum.PartType.Cylinder`, `Size = Vector3.new(2, 140, 140)`, `CFrame = CFrame.new(0, 149, -300) * CFrame.Angles(0, 0, math.rad(90))` (so its top surface is at `World Y = 150.0000`), `Transparency = 1`, `CanCollide = true`, `CollisionGroup = "LobbyWorld"`.
     - **Option B (Exported Collision Proxy Mesh):** Import `meshes/collision_proxy/COL_PlazaPlatform_Deck.glb` (`128 triangles`, `140 × 2 × 140 studs`), set `CollisionFidelity = Enum.CollisionFidelity.PreciseConvexDecomposition` (or `Hull`), `Transparency = 1`, `CanCollide = true`, `CollisionGroup = "LobbyWorld"`, with its top surface aligned to `World Y = 150.0000`.
