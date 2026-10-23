# Roblox Studio Import & Integration Guide — `SM_Hub_QueuePadRing_01`

> **Important Verification Disclosure:** Because Roblox Studio is not installed inside the headless Linux container where this package was built, live Roblox Studio import, material assignment, co-placement with `SM_Hub_PlazaPlatform_01` and `SM_Hub_QueuePortalArch_01`, and R15 avatar walkability tests are marked **`NOT RUN`** in `VALIDATION_REPORT.md` and must be executed inside the owner's Roblox Studio test environment. Do **not** edit or publish the production Studio place during mesh review.

---

## 1. How to Import `SM_Hub_QueuePadRing_01` into Roblox Studio

Import **`meshes/SM_Hub_QueuePadRing_01.glb`** (preferred) or **`meshes/SM_Hub_QueuePadRing_01.obj`** via **Avatar / File -> Import 3D** in Roblox Studio using the settings below:

| 3D Importer Setting | Required Value | Why It Matters |
|---|---|---|
| **Import As Model** | `Enabled (true)` | Preserves the root `SM_Hub_QueuePadRing_01` `Model` container |
| **Merge Meshes** | `Disabled (false)` | Preserves the 4 separate named child `MeshPart`s (`GEO_QueuePadRing_BaseCollar`, `GEO_QueuePadRing_ChannelInlay`, `GEO_QueuePadRing_TrimBezels`, `GEO_QueuePadRing_CyanConduit`) |
| **Scale Unit** | `Studs (1.0 Unit = 1.0 Stud)` | Produces the exact `28.0000 × 0.0760 × 28.0000 stud` bounding box (`R_outer = 14.0000 studs`) |
| **Rescale If Too Large** | `Disabled (false)` | Prevents Studio from shrinking the 28-stud diameter ring |
| **Up / Forward Axis** | `+Y Up`, `+Z Forward` (upright orientation) | Aligns the ring horizontally on the XZ plane with its 4 cardinal threshold gates along `±X` and `±Z` |
| **Anchor All Parts** | `Enabled (true)` | Static environment decoration must remain `Anchored = true` |

---

## 2. How to Set the Intended Position Relative to `SM_Hub_PlazaPlatform_01`

### Coordinate & Pivot Relationship
- **Approved Plaza Platform (`SM_Hub_PlazaPlatform_01`):** Placed at `World (0, 150, -300)` with its top walking surface at `World Y = 150.0000` (`Local Y = 0.0000`).
- **Queue Pad Ring (`SM_Hub_QueuePadRing_01`):** Authored around the exact same local reference origin `(0, 0, 0)` where `Local Y = 0.0000` represents the plaza's top walking surface.
- **Vertical Bounds (`Local Y in [+0.0040, +0.0800]`):** The ring's bottom surface sits at `Local Y = +0.0040 studs` (`4 mm` above `Y = 0.0000` to prevent coplanar Z-fighting) and its top bezel crest sits at `Local Y = +0.0800 studs` (`bboxSize.Y = 0.0760 studs`).
- **Why `Model.WorldPivot` Calibration Is Needed:** When Roblox Studio imports a `Model`, its default bounding-box center sits at `Local Y = +0.0420 studs` (`0.0040 + 0.0760 / 2`). Remember that changing `Model.WorldPivot` does **not** automatically move child geometry—it defines the reference point that `Model:PivotTo(...)` aligns to the target `CFrame`, and `Model.WorldPivot` only governs a `Model` when `Model.PrimaryPart == nil`.

### Command Bar Placement & Dimension Verification Snippet

Run the following Luau snippet in the Roblox Studio Command Bar after importing `SM_Hub_QueuePadRing_01` into `Workspace`:

```luau
local Workspace = game:GetService("Workspace")
local ring = Workspace:WaitForChild("SM_Hub_QueuePadRing_01")

assert(ring:IsA("Model"), "Expected SM_Hub_QueuePadRing_01 to be a Model")

-- WorldPivot controls the pivot for a Model only when PrimaryPart is nil.
ring.PrimaryPart = nil

local bboxCFrame, bboxSize = ring:GetBoundingBox()

assert(
    math.abs(bboxSize.X - 28.0) < 0.05
        and math.abs(bboxSize.Y - 0.076) < 0.02
        and math.abs(bboxSize.Z - 28.0) < 0.05,
    string.format("Unexpected imported ring dimensions: %s", tostring(bboxSize))
)

-- The model is upright (+Y Up). Its bottom face sits 0.004 studs above the
-- Local Y = 0.0000 floor reference plane, so the floor-level pivot is
-- (bboxSize.Y / 2 + 0.004) below the bounding-box centre.
local floorReferencePivot = CFrame.new(
    bboxCFrame.Position - Vector3.new(0, (bboxSize.Y / 2) + 0.004, 0)
)

-- Setting WorldPivot calibrates the Model's pivot without moving child parts.
ring.WorldPivot = floorReferencePivot

-- Position the floor-reference pivot at the locked Hub centre (0, 150, -300).
ring:PivotTo(CFrame.new(0, 150, -300))

local finalCFrame, finalSize = ring:GetBoundingBox()
local bottomWorldY = finalCFrame.Position.Y - (finalSize.Y / 2)
local topWorldY = finalCFrame.Position.Y + (finalSize.Y / 2)

assert(math.abs(bottomWorldY - 150.004) < 0.01, "Ring bottom face is not at World Y = 150.004")
assert(math.abs(topWorldY - 150.080) < 0.01, "Ring top bezel crest is not at World Y = 150.080")

print(string.format(
    "SM_Hub_QueuePadRing_01 placed at (0, 150, -300) | Size: %s | World Y: [%.4f, %.4f]",
    tostring(finalSize), bottomWorldY, topWorldY
))
```

---

## 3. How to Assign Native Roblox Materials, Exact Colours & Physics Flags

### Required Anchoring & Collision Flags (Purely Decorative Mesh)
- Every child `MeshPart` of `SM_Hub_QueuePadRing_01` **must** have:
  - `Anchored = true`
  - `CanCollide = false`
  - `CanTouch = false`
  - `CanQuery = false`
  - `CastShadow = false` (recommended for thin floor inlays so the `0.004-stud` offset never casts shadow artifacts)
- **Why Collisions, Touch & Query Must Be Disabled:** The authoritative walkable floor collision is already provided by `COL_PlazaPlatform_Deck` at `World Y = 150.0000`, and queue entry/exit detection is handled by `QueueService`'s server-authoritative region/radius check (`R = 14.0 studs`, `1.0s` dwell, `0.5s` exit grace). Disabling `CanCollide`, `CanTouch`, and `CanQuery` on the decorative ring ensures avatars and raycasts never snag on the `0.08-stud` decorative bevels.

### Native Material & Colour Assignment Table

| Child `MeshPart` Name | Triangles | `MeshPart.Material` | `MeshPart.Color` (`Color3.fromRGB`) | Hex | Anchored | CanCollide / CanTouch / CanQuery |
|---|---:|---|---|---|---|---|
| `GEO_QueuePadRing_BaseCollar` | `320` | `Enum.Material.Metal` | `Color3.fromRGB(32, 38, 54)` | `#202636` | `true` | `false / false / false` |
| `GEO_QueuePadRing_ChannelInlay` | `320` | `Enum.Material.Metal` | `Color3.fromRGB(42, 50, 70)` | `#2A3246` | `true` | `false / false / false` |
| `GEO_QueuePadRing_TrimBezels` | `256` | `Enum.Material.Metal` | `Color3.fromRGB(170, 190, 215)` | `#AABED7` | `true` | `false / false / false` |
| `GEO_QueuePadRing_CyanConduit` | `64` | `Enum.Material.Neon` | `Color3.fromRGB(0, 195, 255)` | `#00C3FF` | `true` | `false / false / false` |

### Command Bar Material & Collision Setup Snippet

> **Note:** Both `.glb` and `.obj` exports include vertex colors and the `64×64` palette atlas texture (`SphereBrawl_QueuePadRing_PaletteAtlas.png`) so the mesh never imports as pale grey. When applying native Roblox `Enum.Material.Metal` and `Enum.Material.Neon`, clear `MeshPart.TextureID = ""` and remove any child `SurfaceAppearance` so the texture does not mute the native material reflectance or neon emission.

```luau
local Workspace = game:GetService("Workspace")
local ring = Workspace:WaitForChild("SM_Hub_QueuePadRing_01")

local MATERIAL_MAP = {
    GEO_QueuePadRing_BaseCollar   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_QueuePadRing_ChannelInlay = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_QueuePadRing_TrimBezels   = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(170, 190, 215) },
    GEO_QueuePadRing_CyanConduit  = { Mat = Enum.Material.Neon,  Color = Color3.fromRGB(0, 195, 255) },
}

for _, desc in ipairs(ring:GetDescendants()) do
    if desc:IsA("MeshPart") and MATERIAL_MAP[desc.Name] then
        local spec = MATERIAL_MAP[desc.Name]
        desc.Anchored = true
        desc.CanCollide = false
        desc.CanTouch = false
        desc.CanQuery = false
        desc.CastShadow = false
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

print("SM_Hub_QueuePadRing_01 materials and non-colliding flags applied.")
```

---

## 4. How to Inspect Central Standing Area, Portal Clearance & Walkability in a Separate Test Place

Because the owner tests assets in a separate Roblox test environment (whose default `SpawnLocation` may not match the production game's locked Main Spawn at `(0, 150, -334)`), use the following non-invasive verification steps without adding gameplay scripts or changing production lobby logic:

1. **Co-Place Reference Assets at `(0, 150, -300)`:**
   - Ensure `SM_Hub_PlazaPlatform_01` (with its `COL_PlazaPlatform_Deck` top surface at `World Y = 150.0000`) and `SM_Hub_QueuePortalArch_01` (`QueuePortalArch_Prototype.glb`) are positioned at `(0, 150, -300)` alongside `SM_Hub_QueuePadRing_01`.
2. **Inspect Central Standing Area & Portal Clearance:**
   - Verify visually from top-down and perspective camera angles that the central standing area (`R < 12.80 studs`, `25.60-stud` diameter) is completely unobstructed and exposes the plaza platform's `GEO_PlazaPlatform_Deck` surface cleanly.
   - Verify the `+1.05-stud` gap between `SM_Hub_QueuePadRing_01`'s outer edge (`R = 14.00 studs`) and `SM_Hub_QueuePortalArch_01`'s inner pylon brackets (`|X| = 15.05 studs`) and `+1.20-stud` gap to the portal flank glow rims (`R = 15.20 studs`).
   - Orbit the camera at low and high distances to confirm zero Z-fighting flicker between the ring (`World Y >= 150.0040`) and the plaza deck (`World Y = 150.0000`).
3. **Test Avatar Walkability Without Modifying Production Spawn Logic:**
   - Start a **Play Solo** session in the test environment. If your test place spawns the avatar elsewhere (e.g., near `(0, 5, 0)`), run this one-line Command Bar teleport in the **Client / Server** console to place your test avatar at the intended Hub Main Spawn `(0, 150, -334)` facing `+Z` toward the Queue Portal:
     ```luau
     local p = game:GetService("Players").LocalPlayer or game:GetService("Players"):GetPlayers()[1]
     if p and p.Character then
         p.Character:PivotTo(CFrame.lookAt(Vector3.new(0, 153, -334), Vector3.new(0, 153, -300)))
     end
     ```
   - Walk forward (`+Z`) across the south threshold gate of `SM_Hub_QueuePadRing_01`, across the `25.60-stud` open centre, and out through the north (`+Z`), west (`-X`), and east (`+X`) gates. Confirm that the ring is clearly readable at normal camera height and produces zero physical bump or snag.
