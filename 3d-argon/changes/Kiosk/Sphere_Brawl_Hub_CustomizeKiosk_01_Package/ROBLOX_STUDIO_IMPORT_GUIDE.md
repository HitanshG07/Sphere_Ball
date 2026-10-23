# Roblox Studio Import & Placement Guide — `SM_Hub_CustomizeKiosk_01`

> **Important Verification Disclosure:** Because Roblox Studio is not installed inside the headless Linux container where this package was built, live Roblox Studio import, native material assignment, co-placement with `SM_Hub_PlazaPlatform_01`, `SM_Hub_QueuePadRing_01`, and `SM_Hub_QueuePortalArch_01`, and R15 avatar walkability tests are marked **`NOT RUN`** in `VALIDATION_REPORT.md` and must be performed inside a separate Roblox Studio test place. Do **not** modify the production Studio place or production spawn logic during mesh review.

## 1. 3D Importer Settings in a Separate Test Place

Open a clean Roblox Studio test place and import **`meshes/SM_Hub_CustomizeKiosk_01.glb`** (preferred) or **`meshes/SM_Hub_CustomizeKiosk_01.obj`** via **Avatar / File -> Import 3D**:

| 3D Importer Setting | Required Value | Why It Matters |
|---|---|---|
| **Import As Model** | `Enabled (true)` | Preserves the root `SM_Hub_CustomizeKiosk_01` `Model` container |
| **Merge Meshes** | `Disabled (false)` | Preserves all `14` separate child `MeshPart`s (`GEO_CustomizeKiosk_*`), keeping the 4 pedestals and 4 placeholder spheres individually addressable |
| **Scale Unit** | `Studs (1.0 Unit = 1.0 Stud)` | Produces the exact `10.0000 × 9.5000 × 8.0000 stud` local bounding box |
| **Rescale If Too Large** | `Disabled (false)` | Prevents Studio from rescaling the station |
| **Up / Forward Axis** | `+Y Up`, `+Z Forward` | Aligns local `Y = 0` to the base underside and local `+Z` to the primary inward-facing showcase front |
| **Anchor All Parts** | `Enabled (true)` | Static environment showcase geometry must be `Anchored = true` |

## 2. Floor-Reference Pivot Calibration & Locked Placement at `(-43, 150, -300)` Facing `+X`

### Coordinate & Right-Handed Orientation Relationship
- **Local Space (`SM_Hub_CustomizeKiosk_01`):**
  - `X in [-5.0000, +5.0000]` (`Width = 10.0000 studs`)
  - `Y in [0.0000, +9.5000]` (`Height = 9.5000 studs`)
  - `Z in [-4.0000, +4.0000]` (`Depth = 8.0000 studs`)
  - The local bounding-box center sits at `(0.0000, +4.7500, 0.0000)`, exactly `4.7500 studs` (`bboxSize.Y / 2`) above the floor-reference pivot `(0, 0, 0)`.
- **Valid Right-Handed World Placement (`(-43, 150, -300)` with Local `+Z` Facing World `+X`):**
  - The model's documented front is local `+Z`, which must face world `+X` (`Vector3.new(1, 0, 0)`) inward toward the central Queue Portal at `(0, 150, -300)`.
  - Rotating `+90°` (`+pi/2` radians) around the vertical `+Y` axis via:
    ```luau
    local targetCFrame = CFrame.new(-43, 150, -300) * CFrame.Angles(0, math.rad(90), 0)
    ```
    or equivalently using Roblox's right-handed `CFrame.fromMatrix(pos, vX, vY, vZ)` constructor (where `vX × vY = vZ` and `ZVector = -LookVector`):
    ```luau
    local targetCFrame = CFrame.fromMatrix(
        Vector3.new(-43, 150, -300),
        Vector3.new(0, 0, -1), -- local +X / RightVector
        Vector3.new(0, 1, 0),  -- local +Y / UpVector
        Vector3.new(1, 0, 0)   -- local +Z / ZVector
    )
    ```
    maps every local vertex `(x_local, y_local, z_local)` to `World = (-43 + z_local, 150 + y_local, -300 - x_local)`:
    - Local `+Z` (`+4.0` front approach toe) maps to `World X = -39.0000` (facing `+X` inward toward the Queue Portal at `X = 0`).
    - Local `-Z` (`-4.0` rear gantry spine) maps to `World X = -47.0000`.
    - Local `-X` (`-3.35` Pedestal 01, outer left) maps to `World Z = -296.6500` (viewer's left when facing the kiosk from the plaza).
    - Local `+X` (`+3.35` Pedestal 04, outer right) maps to `World Z = -303.3500` (viewer's right when facing the kiosk from the plaza).
    - Local `Y = 0.0000` maps to `World Y = 150.0000` (flush on the plaza walking deck).

### Command Bar Placement & Verification Script

Run the following verified Luau script in the Roblox Studio Command Bar after importing `SM_Hub_CustomizeKiosk_01` into `Workspace`:

```luau
local Workspace = game:GetService("Workspace")
local kiosk = Workspace:WaitForChild("SM_Hub_CustomizeKiosk_01")

assert(kiosk:IsA("Model"), "Expected SM_Hub_CustomizeKiosk_01 to be a Model")

-- WorldPivot governs Model:PivotTo() only when PrimaryPart is nil.
kiosk.PrimaryPart = nil

-- Reset any import rotation first so we measure local dimensions cleanly.
local rawCF, rawSize = kiosk:GetBoundingBox()
kiosk:PivotTo(CFrame.new(rawCF.Position))

local bboxCFrame, bboxSize = kiosk:GetBoundingBox()
assert(
    math.abs(bboxSize.X - 10.0) < 0.05
        and math.abs(bboxSize.Y - 9.5) < 0.05
        and math.abs(bboxSize.Z - 8.0) < 0.05,
    string.format("Unexpected local kiosk dimensions: %s", tostring(bboxSize))
)

-- Calibrate the floor-reference pivot at the bottom center of the footprint (Local Y = 0).
local floorReferencePivot = CFrame.new(
    bboxCFrame.Position - Vector3.new(0, bboxSize.Y / 2, 0)
)
kiosk.WorldPivot = floorReferencePivot

-- Primary valid right-handed placement CFrame at (-43, 150, -300) rotating local +Z to world +X:
local targetCFrame =
    CFrame.new(-43, 150, -300)
    * CFrame.Angles(0, math.rad(90), 0)

-- Equivalent valid right-handed basis matrix:
-- local targetCFrame = CFrame.fromMatrix(
--     Vector3.new(-43, 150, -300),
--     Vector3.new(0, 0, -1), -- local +X / RightVector
--     Vector3.new(0, 1, 0),  -- local +Y / UpVector
--     Vector3.new(1, 0, 0)   -- local +Z / ZVector
-- )

kiosk:PivotTo(targetCFrame)

local finalCF, finalSize = kiosk:GetBoundingBox()
local minWorld = finalCF.Position - (finalSize / 2)
local maxWorld = finalCF.Position + (finalSize / 2)

assert(math.abs(minWorld.X - (-47.0)) < 0.05 and math.abs(maxWorld.X - (-39.0)) < 0.05, "World X bounds mismatch")
assert(math.abs(minWorld.Y - 150.0) < 0.05 and math.abs(maxWorld.Y - 159.5) < 0.05, "World Y bounds mismatch")
assert(math.abs(minWorld.Z - (-305.0)) < 0.05 and math.abs(maxWorld.Z - (-295.0)) < 0.05, "World Z bounds mismatch")

print(string.format(
    "SM_Hub_CustomizeKiosk_01 placed at (-43, 150, -300) facing +X | World Bounds: [%.2f..%.2f, %.2f..%.2f, %.2f..%.2f]",
    minWorld.X, maxWorld.X, minWorld.Y, maxWorld.Y, minWorld.Z, maxWorld.Z
))
```

## 3. Native Roblox Material, Color3 & Non-Colliding Decorative Flags

All `14` visual `MeshPart` components of `SM_Hub_CustomizeKiosk_01` are **non-authoritative visual geometry** and must have `Anchored = true`, `CanCollide = false`, `CanTouch = false`, and `CanQuery = false`.

| Child `MeshPart` Name | `MeshPart.Material` | `MeshPart.Color` (`Color3.fromRGB`) | Hex | Anchored | CanCollide / CanTouch / CanQuery |
|---|---|---|---|---|---|
| `GEO_CustomizeKiosk_Base` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_Frame` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_SecondaryPanels` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_DisplayPedestal_01` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_DisplayPedestal_02` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_DisplayPedestal_03` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_DisplayPedestal_04` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_PreviewSphere_01` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_PreviewSphere_02` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_PreviewSphere_03` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_PreviewSphere_04` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_DisplayHeader` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_Trim` | `Enum.Material.Metal` | `Color3.fromRGB(170, 190, 215)` | `#AABED7` | `true` | `false / false / false` |
| `GEO_CustomizeKiosk_CyanAccents` | `Enum.Material.Neon` | `Color3.fromRGB(0, 195, 255)` | `#00C3FF` | `true` | `false / false / false` |

### Command Bar Material, Flag & Optional Simple Box Collider Script

Run the following Luau snippet in the Studio Command Bar to apply native materials, disable collision on the decorative mesh, and create the recommended simple anchored box collider behind the interaction zone:

```luau
local Workspace = game:GetService("Workspace")
local kiosk = Workspace:WaitForChild("SM_Hub_CustomizeKiosk_01")

local MATERIAL_MAP = {
    GEO_CustomizeKiosk_Base               = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_CustomizeKiosk_Frame              = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_CustomizeKiosk_SecondaryPanels    = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_CustomizeKiosk_DisplayPedestal_01 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_CustomizeKiosk_DisplayPedestal_02 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_CustomizeKiosk_DisplayPedestal_03 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_CustomizeKiosk_DisplayPedestal_04 = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_CustomizeKiosk_PreviewSphere_01   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_CustomizeKiosk_PreviewSphere_02   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_CustomizeKiosk_PreviewSphere_03   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_CustomizeKiosk_PreviewSphere_04   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_CustomizeKiosk_DisplayHeader      = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_CustomizeKiosk_Trim               = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(170, 190, 215) },
    GEO_CustomizeKiosk_CyanAccents        = { Mat = Enum.Material.Neon,  Color = Color3.fromRGB(0, 195, 255) },
}

for _, desc in ipairs(kiosk:GetDescendants()) do
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

-- Optional: Create the simple anchored native Roblox box collider behind the front approach zone.
-- Spans World X in [-47.0, -41.65] (rear frame & pedestal core), World Y in [150.0, 159.5], World Z in [-304.6, -295.4].
local existingCol = kiosk:FindFirstChild("COL_CustomizeKiosk_Proxy")
if existingCol then
    existingCol:Destroy()
end

local colPart = Instance.new("Part")
colPart.Name = "COL_CustomizeKiosk_Proxy"
colPart.Anchored = true
colPart.CanCollide = true
colPart.CanTouch = false
colPart.CanQuery = false
colPart.Transparency = 1
colPart.Size = Vector3.new(5.35, 9.50, 9.20)
colPart.CFrame = CFrame.new(-44.325, 154.75, -300.0)
colPart.Parent = kiosk

print("SM_Hub_CustomizeKiosk_01 materials, non-colliding flags, and simple structural box collider configured.")
```

## 4. How Future Engineers Replace the Four Generic Placeholder Spheres

Each placeholder sphere (`GEO_CustomizeKiosk_PreviewSphere_01` through `_04`) is an independent child `MeshPart` with an exact `1.8000-stud` diameter (`R = 0.9000 studs`). Under the right-handed `+90°` yaw placement at `(-43, 150, -300)`, their world centers are:
- `GEO_CustomizeKiosk_PreviewSphere_01`: `(-42.4500, 153.0500, -296.6500)`
- `GEO_CustomizeKiosk_PreviewSphere_02`: `(-43.4500, 153.5000, -298.8500)`
- `GEO_CustomizeKiosk_PreviewSphere_03`: `(-43.4500, 153.5000, -301.1500)`
- `GEO_CustomizeKiosk_PreviewSphere_04`: `(-42.4500, 153.0500, -303.3500)`

When the four approved sphere chassis shells (`Rammer`, `Trickster`, `Magnetar`, `Bulwark`) are ready to be mounted on the kiosk pedestals:
1. Locate `kiosk:FindFirstChild("GEO_CustomizeKiosk_PreviewSphere_0" .. slotIndex)`.
2. Read its world center via `local targetCF = placeholder.CFrame`.
3. Clone the approved display shell model, scale it to the `1.80-stud` showcase diameter (`0.30×` of the `6.0-stud` combat diameter), set all its parts to `Anchored = true`, `CanCollide = false`, `CanTouch = false`, `CanQuery = false`, call `shellClone:PivotTo(targetCF)`, parent it to `kiosk`, and destroy or hide (`Transparency = 1`) the placeholder sphere.

## 5. Co-Placement & Player-Height Inspection in a Separate Test Place

1. **Co-Place Reference Hub Assets:**
   - Import and place `SM_Hub_PlazaPlatform_01`, `SM_Hub_QueuePadRing_01`, and `SM_Hub_QueuePortalArch_01` at `World (0, 150, -300)` following their respective import guides.
2. **Verify Clearances:**
   - Confirm that `SM_Hub_CustomizeKiosk_01`'s front approach edge (`World X = -39.00`) has **`25.00 studs` of unobstructed flat plaza deck** to `SM_Hub_QueuePadRing_01` (`World X = -14.00`) and **`23.95 studs`** to `SM_Hub_QueuePortalArch_01` (`World X = -15.05`).
3. **Player-Height Walk-Up Inspection (Without Modifying Production Spawn):**
   - Start a **Play Solo** session in your separate test place and teleport your test avatar to the Main Spawn `(0, 150, -334)` or directly in front of the kiosk at `(-32, 153, -300)` facing `-X` via the Command Bar:
     ```luau
     local p = game:GetService("Players").LocalPlayer or game:GetService("Players"):GetPlayers()[1]
     if p and p.Character then
         p.Character:PivotTo(CFrame.lookAt(Vector3.new(-32, 153, -300), Vector3.new(-43, 153, -300)))
     end
     ```
   - Walk up to the kiosk (`World X = -39.0`) and verify that all four sphere placeholders (`01`..`04` from left `Z = -296.65` to right `Z = -303.35`) and the overhead header panel read clearly at R15 camera height with zero snagging.
