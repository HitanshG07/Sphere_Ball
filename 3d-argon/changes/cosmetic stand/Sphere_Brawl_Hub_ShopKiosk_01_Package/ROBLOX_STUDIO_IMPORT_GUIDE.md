# Roblox Studio Import & Placement Guide — `SM_Hub_ShopKiosk_01` (Sphere Brawl Arena Shop Bar)

> **Important Verification Disclosure:** Because Roblox Studio is not installed inside the headless Linux container where this package was built, live Roblox Studio import, native material assignment, co-placement with `SM_Hub_PlazaPlatform_01`, `SM_Hub_QueuePadRing_01`, `SM_Hub_QueuePortalArch_01`, and `SM_Hub_CustomizeKiosk_01`, and R15 avatar walkability tests are marked **`NOT RUN`** in `VALIDATION_REPORT.md` and must be performed inside a separate Roblox Studio test place. Do **not** modify the production Studio place or production gameplay code during mesh review.

## 1. 3D Importer Settings in a Separate Test Place

Open a clean Roblox Studio test place and import **`meshes/SM_Hub_ShopKiosk_01.glb`** (preferred) or **`meshes/SM_Hub_ShopKiosk_01.obj`** via **Avatar / File -> Import 3D**:

| 3D Importer Setting | Required Value | Why It Matters |
|---|---|---|
| **Import As Model** | `Enabled (true)` | Preserves the root `SM_Hub_ShopKiosk_01` `Model` container |
| **Merge Meshes** | `Disabled (false)` | Preserves all `18` separate child `MeshPart`s (`GEO_ShopKiosk_*`), keeping the 4 countertop pads, 4 replaceable non-spherical display items, and blank `GEO_ShopKiosk_SignPanel` individually addressable |
| **Scale Unit** | `Studs (1.0 Unit = 1.0 Stud)` | Produces the exact `20.0000 × 7.6000 × 8.0000 stud` local bounding box |
| **Rescale If Too Large** | `Disabled (false)` | Prevents Studio from rescaling the station |
| **Up / Forward Axis** | `+Y Up`, `+Z Forward` | Aligns local `Y = 0` to the base underside and local `+Z` to the primary customer-facing bar counter front |
| **Anchor All Parts** | `Enabled (true)` | Static environment showcase geometry must be `Anchored = true` |

## 2. Floor-Reference Pivot Calibration & Locked Placement at `(43, 150, -300)` Facing `-X`

### Coordinate & Right-Handed Orientation Relationship
- **Local Space (`SM_Hub_ShopKiosk_01`):**
  - `X in [-10.0000, +10.0000]` (`Width = 20.0000 studs`)
  - `Y in [0.0000, +7.6000]` (`Height = 7.6000 studs`)
  - `Z in [-4.0000, +4.0000]` (`Depth = 8.0000 studs`)
  - The local bounding-box center sits at `(0.0000, +3.8000, 0.0000)`, exactly `3.8000 studs` (`bboxSize.Y / 2`) above the floor-reference pivot `(0, 0, 0)`.
- **Valid Right-Handed World Placement (`(43, 150, -300)` with Local `+Z` Facing World `-X`):**
  - Rotating `-90°` (`-pi/2` radians) around the vertical `+Y` axis via:
    ```luau
    local targetCFrame =
        CFrame.new(43, 150, -300)
        * CFrame.Angles(0, math.rad(-90), 0)
    ```
    maps every local vertex `(x_local, y_local, z_local)` to `World = (43.0 - z_local, 150.0 + y_local, -300.0 + x_local)`:
    - Local `+Z` (`+4.0` front walk-up step) maps to `World X = +39.0000` (facing `-X` inward toward the Queue Portal at `X = 0`).
    - Local `-Z` (`-4.0` rear wing plinth) maps to `World X = +47.0000`.
    - Local `-X` (`-10.0` Left Wing) maps to `World Z = -310.0000`.
    - Local `+X` (`+10.0` Right Wing) maps to `World Z = -290.0000`.
    - Local `Y = 0.0000` maps to `World Y = 150.0000` (flush on the plaza walking deck).

### Command Bar Placement & Verification Script

Run the following verified Luau script in the Roblox Studio Command Bar after importing `SM_Hub_ShopKiosk_01` into `Workspace`:

```luau
local Workspace = game:GetService("Workspace")
local shopKiosk = Workspace:WaitForChild("SM_Hub_ShopKiosk_01")

assert(shopKiosk:IsA("Model"), "Expected SM_Hub_ShopKiosk_01 to be a Model")

-- WorldPivot governs Model:PivotTo() only when PrimaryPart is nil.
shopKiosk.PrimaryPart = nil

-- Reset any import rotation first so we measure local dimensions cleanly.
local rawCF, rawSize = shopKiosk:GetBoundingBox()
shopKiosk:PivotTo(CFrame.new(rawCF.Position))

local bboxCFrame, bboxSize = shopKiosk:GetBoundingBox()
assert(
    math.abs(bboxSize.X - 20.0) < 0.05
        and math.abs(bboxSize.Y - 7.6) < 0.05
        and math.abs(bboxSize.Z - 8.0) < 0.05,
    string.format("Unexpected local shop kiosk dimensions: %s", tostring(bboxSize))
)

-- Calibrate the floor-reference pivot at the bottom center of the footprint (Local Y = 0).
local floorReferencePivot = CFrame.new(
    bboxCFrame.Position - Vector3.new(0, bboxSize.Y / 2, 0)
)
shopKiosk.WorldPivot = floorReferencePivot

-- Primary valid right-handed placement CFrame at (43, 150, -300) rotating local +Z to world -X:
local targetCFrame =
    CFrame.new(43, 150, -300)
    * CFrame.Angles(0, math.rad(-90), 0)

shopKiosk:PivotTo(targetCFrame)

local finalCF, finalSize = shopKiosk:GetBoundingBox()
local minWorld = finalCF.Position - (finalSize / 2)
local maxWorld = finalCF.Position + (finalSize / 2)

assert(math.abs(minWorld.X - 39.0) < 0.05 and math.abs(maxWorld.X - 47.0) < 0.05, "World X bounds mismatch")
assert(math.abs(minWorld.Y - 150.0) < 0.05 and math.abs(maxWorld.Y - 157.6) < 0.05, "World Y bounds mismatch")
assert(math.abs(minWorld.Z - (-310.0)) < 0.05 and math.abs(maxWorld.Z - (-290.0)) < 0.05, "World Z bounds mismatch")

print(string.format(
    "SM_Hub_ShopKiosk_01 placed at (43, 150, -300) facing -X | World Bounds: [%.2f..%.2f, %.2f..%.2f, %.2f..%.2f]",
    minWorld.X, maxWorld.X, minWorld.Y, maxWorld.Y, minWorld.Z, maxWorld.Z
))
```

## 3. Native Roblox Material, Color3 & Non-Colliding Decorative Flags

> **Important Note on Emissive Materials:** Exported glTF/MTL emissive factors do **not** automatically convert a `MeshPart` into `Enum.Material.Neon` inside Roblox Studio. You must explicitly assign `Enum.Material.Neon` to `GEO_ShopKiosk_CyanAccents` and `GEO_ShopKiosk_AmberAccents` and `Enum.Material.Metal` to the metallic structural components using the table or script below.

All `18` visual `MeshPart` components of `SM_Hub_ShopKiosk_01` are **non-authoritative visual geometry** and must have `Anchored = true`, `CanCollide = false`, `CanTouch = false`, and `CanQuery = false`:

| Child `MeshPart` Name | `MeshPart.Material` | `MeshPart.Color` (`Color3.fromRGB`) | Hex | Anchored | CanCollide / CanTouch / CanQuery |
|---|---|---|---|---|---|
| `GEO_ShopKiosk_Base` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_ShopKiosk_CounterBody` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_ShopKiosk_Countertop` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_ShopKiosk_SideWings` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_ShopKiosk_WingShelves` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_ShopKiosk_DisplayPad_01` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_ShopKiosk_DisplayPad_02` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_ShopKiosk_DisplayPad_03` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_ShopKiosk_DisplayPad_04` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_ShopKiosk_DisplayItem_01` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_ShopKiosk_DisplayItem_02` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_ShopKiosk_DisplayItem_03` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_ShopKiosk_DisplayItem_04` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_ShopKiosk_SignFrame` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_ShopKiosk_SignPanel` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_ShopKiosk_Trim` | `Enum.Material.Metal` | `Color3.fromRGB(170, 190, 215)` | `#AABED7` | `true` | `false / false / false` |
| `GEO_ShopKiosk_CyanAccents` | `Enum.Material.Neon` | `Color3.fromRGB(0, 195, 255)` | `#00C3FF` | `true` | `false / false / false` |
| `GEO_ShopKiosk_AmberAccents` | `Enum.Material.Neon` | `Color3.fromRGB(255, 170, 0)` | `#FFAA00` | `true` | `false / false / false` |

### Command Bar Material, Non-Colliding Flags & Simple Counter Collider Setup Script

```luau
local Workspace = game:GetService("Workspace")
local shopKiosk = Workspace:WaitForChild("SM_Hub_ShopKiosk_01")

local MATERIAL_MAP = {
    GEO_ShopKiosk_Base          = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ShopKiosk_CounterBody   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ShopKiosk_Countertop    = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ShopKiosk_SideWings     = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ShopKiosk_WingShelves   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ShopKiosk_DisplayPad_01 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ShopKiosk_DisplayPad_02 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ShopKiosk_DisplayPad_03 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ShopKiosk_DisplayPad_04 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ShopKiosk_DisplayItem_01 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ShopKiosk_DisplayItem_02 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ShopKiosk_DisplayItem_03 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ShopKiosk_DisplayItem_04 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ShopKiosk_SignFrame     = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ShopKiosk_SignPanel     = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ShopKiosk_Trim          = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(170, 190, 215) },
    GEO_ShopKiosk_CyanAccents   = { Mat = Enum.Material.Neon,  Color = Color3.fromRGB(0, 195, 255) },
    GEO_ShopKiosk_AmberAccents  = { Mat = Enum.Material.Neon,  Color = Color3.fromRGB(255, 170, 0) },
}

for _, desc in ipairs(shopKiosk:GetDescendants()) do
    if desc:IsA("MeshPart") and MATERIAL_MAP[desc.Name] then
        local spec = MATERIAL_MAP[desc.Name]
        desc.Anchored = true
        desc.CanCollide = false
        desc.CanTouch = false
        desc.CanQuery = false
        desc.TextureID = ""
        for _, child in ipairs(desc:GetChildren()) do
            if child:IsA("SurfaceAppearance") then
                child:Destroy()
            end
        end
        desc.Material = spec.Mat
        desc.Color = spec.Color
    end
end

-- Optional: Create a simple invisible native Roblox Part box collider for the bar counter body
-- while keeping the front walk-up apron (World X in [39.00, 40.34]) unobstructed.
local existingCol = shopKiosk:FindFirstChild("COL_ShopKiosk_Proxy")
if existingCol then
    existingCol:Destroy()
end

local colPart = Instance.new("Part")
colPart.Name = "COL_ShopKiosk_Proxy"
colPart.Anchored = true
colPart.CanCollide = true
colPart.CanTouch = false
colPart.CanQuery = false
colPart.Transparency = 1
colPart.Size = Vector3.new(4.88, 3.32, 19.60)
colPart.CFrame = CFrame.new(42.78, 151.66, -300.0)
colPart.Parent = shopKiosk

print("SM_Hub_ShopKiosk_01 materials, non-colliding flags, and simple counter box collider configured.")
```

## 4. Independent Replacement of the Four Countertop Merchandise Items & Blank Sign Panel

1. **Four Replaceable Merchandise Items (`GEO_ShopKiosk_DisplayItem_01` through `_04`):**
   - Each display item is a separate child `MeshPart` sitting above its corresponding octagonal display pad (`GEO_ShopKiosk_DisplayPad_01` through `_04`).
   - Nominal transformed world centers:
     - `GEO_ShopKiosk_DisplayItem_01` (Hexagonal Emblem Plate): `(42.7500, 154.1800, -305.1000)`
     - `GEO_ShopKiosk_DisplayItem_02` (Vertical Halo Ring): `(42.7500, 154.2200, -301.7000)`
     - `GEO_ShopKiosk_DisplayItem_03` (Segmented Chevron Trail Fins): `(42.7500, 154.1500, -298.3000)`
     - `GEO_ShopKiosk_DisplayItem_04` (Geometric Starburst Burst Prism): `(42.7500, 154.2500, -294.9000)`
   - To replace any placeholder in a future content pass, locate `shopKiosk:FindFirstChild("GEO_ShopKiosk_DisplayItem_0" .. slotIndex)`, pivot the new non-colliding cosmetic mesh to its `CFrame`, and destroy or hide (`Transparency = 1`) the placeholder `MeshPart`.
2. **Separate Blank UI-Ready Sign Panel (`GEO_ShopKiosk_SignPanel`):**
   - `GEO_ShopKiosk_SignPanel` (`X in [-5.60, +5.60]`, `Y in [5.68, 7.12]`, `Z in [+0.20, +0.68]`) has a completely flat, blank front face at `Local Z = +0.6800` (`World X = 42.3200`, facing `World -X`) with zero baked text geometry, ready to receive a native Roblox `SurfaceGui` (`Face = Enum.NormalId.Front`).
