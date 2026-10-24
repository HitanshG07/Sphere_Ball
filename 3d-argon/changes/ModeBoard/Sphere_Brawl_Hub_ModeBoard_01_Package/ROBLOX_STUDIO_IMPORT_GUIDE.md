# Roblox Studio Import, Placement & UI Mounting Guide — `SM_Hub_ModeBoard_01`

> **Important Verification Disclosure:** Because Roblox Studio is not available inside the headless Linux container where this package was generated, live Roblox Studio import, native material conversion (`Enum.Material.Metal` / `Enum.Material.Neon`), `SurfaceGui` attachment, and live R15 avatar walkability tests are marked **`NOT RUN`** in `VALIDATION_REPORT.md`. All steps below distinguish between **programmatically verified geometry/math** (tested in Python) and **manual Studio verification steps** (to be executed in a separate Roblox Studio test place). Do **not** implement mode-selection logic, remotes, or server state changes during asset import.

---

## 1. 3D Importer Settings in a Separate Roblox Studio Test Place

Open a clean Roblox Studio test place and import **`meshes/SM_Hub_ModeBoard_01.glb`** (preferred, preserves the parent-child node hierarchy) or **`meshes/SM_Hub_ModeBoard_01.obj`** via **Avatar / File -> Import 3D**:

| 3D Importer Setting | Required Value | Why It Matters |
|---|---|---|
| **Import As Model** | `Enabled (true)` | Preserves the root `SM_Hub_ModeBoard_01` `Model` container |
| **Merge Meshes** | `Disabled (false)` | Preserves all `18` separate child `MeshPart`s (`GEO_ModeBoard_*`), keeping the 5 UI-ready surfaces (`GEO_ModeBoard_UIPanel_01..04` and `GEO_ModeBoard_HeaderSign`) and modular 3D relief badges individually addressable |
| **Scale Unit** | `Studs (1.0 Unit = 1.0 Stud)` | Produces the exact `14.4000 (W) × 8.8000 (H) × 3.8000 (D) stud` local bounding box |
| **Rescale If Too Large** | `Disabled (false)` | Prevents Studio from rescaling the station |
| **Up / Forward Axis** | `+Y Up`, `+Z Forward` | Aligns local `Y = 0.0000` to the base underside and local `+Z` to the player-facing front |
| **Anchor All Parts** | `Enabled (true)` | Static Hub station geometry must be `Anchored = true` |

> **Format Hierarchy Note (`.glb` vs. `.obj`):** Binary glTF 2.0 (`SM_Hub_ModeBoard_01.glb`) natively stores the root node `SM_Hub_ModeBoard_01` with all `18` named child nodes (`GEO_ModeBoard_*`). Wavefront OBJ (`SM_Hub_ModeBoard_01.obj`) stores all `18` named `o GEO_ModeBoard_*` objects at a single flat level inside the imported `Model`. With **Merge Meshes = Disabled**, both formats produce the exact same `18` named `MeshPart` children inside the root `SM_Hub_ModeBoard_01` `Model`.

---

## 2. Floor-Reference Pivot Calibration & Locked Placement at `(35, 150, -326)`

### Coordinate & Right-Handed Orientation Relationship
- **Local Space (`SM_Hub_ModeBoard_01`):**
  - `X in [-7.2000, +7.2000]` (`Width = 14.4000 studs`)
  - `Y in [0.0000, +8.8000]` (`Height = 8.8000 studs`)
  - `Z in [-1.9000, +1.9000]` (`Depth = 3.8000 studs`)
  - The local bounding-box center sits at `(0.0000, +4.4000, 0.0000)`, exactly `4.4000 studs` (`bboxSize.Y / 2`) above the floor-reference pivot `(0, 0, 0)`.
- **Verified Radial Inward Placement Transform (`θ_yaw = -53.39292061°`):**
  ```luau
  local targetCFrame =
      CFrame.new(35, 150, -326)
      * CFrame.Angles(0, math.rad(-53.39292061), 0)
  ```
  This maps:
  - `Local +Z` (`[0, 0, 1]^T`, model front) to **`FrontVector = (-0.802744, 0, +0.596324)`**, pointing radially inward from `(35, 150, -326)` directly toward the Hub center and Queue Portal at `(0, 150, -300)`.
  - `Local +Y` (`[0, 1, 0]^T`) to **`UpVector = (0, 1, 0)`** (`World Y = 150.0000` at the base underside).
  - `Local +X` (`[1, 0, 0]^T`, model right) to **`RightVector = (+0.596324, 0, +0.802744)`**.

### Command Bar Placement, Material & Collision Setup Script (Integration Example — Untested in Live Studio)

Run the following Luau script in the Roblox Studio Command Bar after importing `SM_Hub_ModeBoard_01` into `Workspace`:

```luau
local Workspace = game:GetService("Workspace")
local modeBoard = Workspace:WaitForChild("SM_Hub_ModeBoard_01")

assert(modeBoard:IsA("Model"), "Expected SM_Hub_ModeBoard_01 to be a Model")

-- 1. Clear PrimaryPart so Model.WorldPivot governs Model:PivotTo()
modeBoard.PrimaryPart = nil

-- Reset any import rotation first so we measure local unrotated dimensions cleanly
local rawCF, rawSize = modeBoard:GetBoundingBox()
modeBoard:PivotTo(CFrame.new(rawCF.Position))

local bboxCFrame, bboxSize = modeBoard:GetBoundingBox()
assert(
    math.abs(bboxSize.X - 14.4) < 0.05
        and math.abs(bboxSize.Y - 8.8) < 0.05
        and math.abs(bboxSize.Z - 3.8) < 0.05,
    string.format("Unexpected local mode board dimensions: %s", tostring(bboxSize))
)

-- 2. Calibrate the floor-reference pivot at the bottom center of the footprint (Local Y = 0)
local floorReferencePivot = CFrame.new(
    bboxCFrame.Position - Vector3.new(0, bboxSize.Y / 2, 0)
)
modeBoard.WorldPivot = floorReferencePivot

-- 3. Apply the verified right-handed radial inward placement CFrame at (35, 150, -326)
local targetCFrame =
    CFrame.new(35, 150, -326)
    * CFrame.Angles(0, math.rad(-53.39292061), 0)

modeBoard:PivotTo(targetCFrame)

-- Verify that the placed front direction (+Z_local = -LookVector of CFrame) points toward (0, 150, -300)
local frontVector = targetCFrame.ZVector
local expectedDir = (Vector3.new(0, 150, -300) - Vector3.new(35, 150, -326)).Unit
assert(frontVector:Dot(expectedDir) > 0.99999, "Front direction validation failed!")

-- 4. Configure native Roblox Materials, Color3, and non-colliding visual flags on all 18 MeshParts
local MATERIAL_MAP = {
    GEO_ModeBoard_BasePlinth         = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ModeBoard_BaseUpperTier      = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ModeBoard_MainChassis        = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ModeBoard_LeftButtress       = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ModeBoard_RightButtress      = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ModeBoard_SideCollars        = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(170, 190, 215) },
    GEO_ModeBoard_CommandMatrixFrame = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ModeBoard_UIPanel_01_FFA     = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ModeBoard_UIPanel_02_Duel    = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ModeBoard_UIPanel_03_TeamClash = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ModeBoard_UIPanel_04_KingTile  = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ModeBoard_HeaderCanopy       = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(32, 38, 54) },
    GEO_ModeBoard_HeaderSign         = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(42, 50, 70) },
    GEO_ModeBoard_ActiveModeReticle  = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(170, 190, 215) },
    GEO_ModeBoard_LockReliefs        = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(170, 190, 215) },
    GEO_ModeBoard_ModeReliefs        = { Mat = Enum.Material.Metal, Color = Color3.fromRGB(170, 190, 215) },
    GEO_ModeBoard_CyanAccents        = { Mat = Enum.Material.Neon,  Color = Color3.fromRGB(0, 195, 255) },
    GEO_ModeBoard_AmberAccents       = { Mat = Enum.Material.Neon,  Color = Color3.fromRGB(255, 170, 0) },
}

for _, desc in ipairs(modeBoard:GetDescendants()) do
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

-- 5. Create simplified invisible structural collision proxy (matches COL_ModeBoard_Body)
-- Blocks physical station body while keeping the front walk-up approach (Local Z > +1.52) 100% open
local existingCol = modeBoard:FindFirstChild("COL_ModeBoard_Proxy")
if existingCol then
    existingCol:Destroy()
end

local colPart = Instance.new("Part")
colPart.Name = "COL_ModeBoard_Proxy"
colPart.Anchored = true
colPart.CanCollide = true
colPart.CanTouch = false
colPart.CanQuery = false
colPart.Transparency = 1
colPart.Size = Vector3.new(14.16, 8.80, 2.78)
colPart.CFrame = targetCFrame * CFrame.new(0, 4.40, -0.37)
colPart.Parent = modeBoard

print("SM_Hub_ModeBoard_01 placed at (35, 150, -326) with materials and non-snagging collider proxy configured.")
```

---

## 3. Distinction Between Visual MeshParts, Structural Collider & UI-Ready Helper Planes

| Role Category | Included Objects / Components | `Anchored` | `CanCollide` | `CanTouch` / `CanQuery` | Purpose |
|---|---|---|---|---|---|
| **Visual `MeshPart`s** | All `18` `GEO_ModeBoard_*` components (`1,612` tris) | `true` | `false` | `false / false` | High-detail hard-surface visual presentation without snagging R15 avatars on bevels or clamps |
| **Simplified Collision Proxy** | `COL_ModeBoard_Proxy` (`Part`) or imported `meshes/collision_proxy/COL_ModeBoard_Body.glb` (`36` tris) | `true` | `true` (`CollisionGroup = "LobbyWorld"`) | `false / false` | Prevents players from walking through the station core (`Local Z in [-1.76, +1.02]`) while keeping the front walk-up step (`Local Z > +1.52`) completely open |
| **UI-Ready Display Surfaces / Helper Planes** | `GEO_ModeBoard_UIPanel_01_FFA`, `_02_Duel`, `_03_TeamClash`, `_04_KingTile`, and `GEO_ModeBoard_HeaderSign` (or thin invisible `Part` adornees aligned to their front faces) | `true` | `false` | `false / false` (`CanQuery = true` only if future interactive `SurfaceGui` buttons are added) | Provides exact flat planes for mounting `SurfaceGui` elements |

---

## 4. Mounting `SurfaceGui` Elements onto the Five UI-Ready Surfaces (Integration Reference)

Because a Roblox `SurfaceGui` projects onto one axis-aligned face (`Enum.NormalId`) of its `Adornee` `BasePart`, and the four mode panels (`GEO_ModeBoard_UIPanel_01..04`) are inclined at **`14.0°` backward from vertical** inside a model whose `MeshPart` bounding boxes are world/model-axis-aligned upon import, the cleanest studio-standard method to mount crisp `SurfaceGui` elements onto the inclined panels is to spawn thin, transparent, non-colliding `Part` adornees aligned to each panel's exact local center and `14.0°` normal (`CFrame.Angles(math.rad(-14), 0, 0)` so the `Part`'s `Enum.NormalId.Back` (`+Z` face) or `CFrame.Angles(math.rad(14), math.pi, 0)` so `Enum.NormalId.Front` (`-Z` face) points along the outward panel normal `(0, +0.241922, +0.970296)`):

```luau
-- INTEGRATION EXAMPLE ONLY (Not executed in live Studio; does not implement gameplay logic)
-- Spawns 5 thin transparent Adornee Parts flush on the 5 UI-ready surfaces so SurfaceGui.Face = Enum.NormalId.Front
-- faces directly outward toward the approaching player.
local PANEL_ADORNEE_SPECS = {
    {
        Name = "UIAdornee_01_FFA",
        LocalCenter = Vector3.new(-3.0000, 4.4879, 0.4813),
        Size = Vector3.new(4.08, 3.78, 0.02),
        TiltDeg = 14.0,
    },
    {
        Name = "UIAdornee_02_Duel",
        LocalCenter = Vector3.new(2.8800, 6.0478, -0.0825),
        Size = Vector3.new(5.04, 1.20, 0.02),
        TiltDeg = 14.0,
    },
    {
        Name = "UIAdornee_03_TeamClash",
        LocalCenter = Vector3.new(2.8800, 4.4371, 0.3190),
        Size = Vector3.new(5.04, 1.20, 0.02),
        TiltDeg = 14.0,
    },
    {
        Name = "UIAdornee_04_KingTile",
        LocalCenter = Vector3.new(2.8800, 2.8264, 0.7206),
        Size = Vector3.new(5.04, 1.20, 0.02),
        TiltDeg = 14.0,
    },
    {
        Name = "UIAdornee_HeaderSign",
        LocalCenter = Vector3.new(0.0000, 7.9500, 0.8800),
        Size = Vector3.new(11.48, 0.82, 0.02),
        TiltDeg = 0.0,
    },
}

for _, spec in ipairs(PANEL_ADORNEE_SPECS) do
    local adornee = Instance.new("Part")
    adornee.Name = spec.Name
    adornee.Anchored = true
    adornee.CanCollide = false
    adornee.CanTouch = false
    adornee.CanQuery = false
    adornee.Transparency = 1
    adornee.Size = spec.Size
    -- Rotating by math.pi about Y and +TiltDeg about local X makes Enum.NormalId.Front (-Z of Part)
    -- point along (0, sin(TiltDeg), cos(TiltDeg)) in SM_Hub_ModeBoard_01 local space!
    local localCF =
        CFrame.new(spec.LocalCenter)
        * CFrame.Angles(0, math.pi, 0)
        * CFrame.Angles(math.rad(spec.TiltDeg), 0, 0)
    adornee.CFrame = targetCFrame * localCF
    adornee.Parent = modeBoard
end
```
