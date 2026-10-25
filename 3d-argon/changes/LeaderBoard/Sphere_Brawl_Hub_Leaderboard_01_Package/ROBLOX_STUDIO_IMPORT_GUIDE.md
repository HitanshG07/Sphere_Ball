# Roblox Studio Import, Placement, UI & Avatar Integration Guide — `SM_Hub_Leaderboard_01`

- **Canonical Asset ID:** `SM_Hub_Leaderboard_01`
- **Target Studio Container:** `Workspace.KineticHub.Stations.SM_Hub_Leaderboard_01`
- **Authoritative World Anchor:** `(35, 150, -274)` (`World Y = 150.0000` plaza walking surface)
- **Approved Inward Yaw:** `-126.60707939°` (`math.rad(-126.60707939)`) facing Hub Center `(0, 150, -300)`

---

## 1. Importing `SM_Hub_Leaderboard_01.glb` (or `.obj`) into Roblox Studio

1. Open the target *Sphere Brawl: Rolling Rampage* place in **Roblox Studio** and go to **Avatar / Home -> Import 3D**.
2. Select **`meshes/SM_Hub_Leaderboard_01.glb`** (recommended, as it preserves the root `Model` node `SM_Hub_Leaderboard_01` and all `53` named child `MeshPart` nodes) or **`meshes/SM_Hub_Leaderboard_01.obj`**.
3. Configure the **Import 3D** settings:
   - **File General -> Import Only As Model:** `false` (insert into workspace or Asset Manager).
   - **File General -> Merge Meshes:** `false` (**mandatory** so all `53` named components, including the `15` replaceable UI-ready surfaces and `9` podiums, import as separate `MeshPart` children).
   - **Transform -> Scale Unit:** `Studs` (`1.0 unit = 1.0 stud`).
   - **Transform -> Forward Axis / Up Axis:** `+Z` Forward, `+Y` Up.
   - **Object General -> Anchored:** `true`.
4. Click **Import** and place the resulting `Model` named `SM_Hub_Leaderboard_01` under `Workspace.KineticHub.Stations` (or `Workspace` during isolated station testing).

---

## 2. Exact Placement, Grounding & Material Configuration (Command Bar Luau Script)

Run the following verified Luau script in the **Roblox Studio Command Bar** after importing `SM_Hub_Leaderboard_01.glb` with `Merge Meshes = false`. It sets the model's `WorldPivot` to its local origin `(0, 0, 0)`, places the station at `(35, 150, -274)` with `Yaw = -126.60707939°` via `Model:PivotTo(targetCFrame)`, anchors all static `MeshPart`s, and applies the approved material and color settings:

```lua
-- Verified Roblox Studio Command Bar Setup Script for SM_Hub_Leaderboard_01
local model = workspace:FindFirstChild("SM_Hub_Leaderboard_01", true)
assert(model and model:IsA("Model"), "SM_Hub_Leaderboard_01 Model not found in Workspace!")

-- 1. Set WorldPivot to the model's exported local origin (bottom-floor reference at Y = 0.0000)
-- Because the exported local bounds are X in [-11.0, +31.0], Y in [0.0, +26.0], Z in [-4.2, +4.8],
-- the bounding-box center is at local offset (+10.0, +13.0, +0.3) from the local origin (0, 0, 0).
local bboxCFrame, bboxSize = model:GetBoundingBox()
local localOriginCFrame = bboxCFrame * CFrame.new(-10.0, -13.0, -0.3)
model.WorldPivot = localOriginCFrame

-- 2. Place SM_Hub_Leaderboard_01 at locked world anchor (35, 150, -274) facing (0, 150, -300)
local targetCFrame =
    CFrame.new(35, 150, -274)
    * CFrame.Angles(0, math.rad(-126.60707939), 0)

model:PivotTo(targetCFrame)

-- 3. Apply locked Kinetic Grid materials, colors, and collision flags across all 53 child MeshParts
local COLOR_DARK_NEUTRAL = Color3.fromRGB(32, 38, 54)    -- #202636
local COLOR_ALT_NEUTRAL  = Color3.fromRGB(42, 50, 70)    -- #2A3246
local COLOR_LIGHT_TRIM   = Color3.fromRGB(170, 190, 215) -- #AABED7
local COLOR_EMI_CYAN     = Color3.fromRGB(0, 195, 255)   -- #00C3FF
local COLOR_EMI_AMBER    = Color3.fromRGB(255, 170, 0)   -- #FFAA00
local COLOR_EMI_MAGNETIC = Color3.fromRGB(165, 55, 255)  -- #A537FF

local ALT_NEUTRAL_COMPS = {
    GEO_Leaderboard_WallPedestal = true,
    GEO_Leaderboard_CrossGirders = true,
    GEO_Leaderboard_Module_A_Bezel = true,
    GEO_Leaderboard_Module_B_Bezel = true,
    GEO_Leaderboard_Module_C_Bezel = true,
    GEO_Leaderboard_RearSpine = true,
    GEO_Leaderboard_PodiumStage_A_Deck = true,
    GEO_Leaderboard_PodiumStage_B_Deck = true,
    GEO_Leaderboard_PodiumStage_C_Deck = true,
}

for _, desc in ipairs(model:GetDescendants()) do
    if desc:IsA("MeshPart") then
        desc.Anchored = true
        desc.CastShadow = true
        local name = desc.Name

        if string.find(name, "Accent_A", 1, true) then
            desc.Material = Enum.Material.Neon
            desc.Color = COLOR_EMI_CYAN
        elseif string.find(name, "Accent_B", 1, true) then
            desc.Material = Enum.Material.Neon
            desc.Color = COLOR_EMI_AMBER
        elseif string.find(name, "Accent_C", 1, true) then
            desc.Material = Enum.Material.Neon
            desc.Color = COLOR_EMI_MAGNETIC
        elseif string.find(name, "LightTrim", 1, true) or string.find(name, "CollarClamps", 1, true) then
            desc.Material = Enum.Material.Metal
            desc.Color = COLOR_LIGHT_TRIM
        elseif ALT_NEUTRAL_COMPS[name] then
            desc.Material = Enum.Material.Metal
            desc.Color = COLOR_ALT_NEUTRAL
        else
            desc.Material = Enum.Material.Metal
            desc.Color = COLOR_DARK_NEUTRAL
        end
    end
end

print("SM_Hub_Leaderboard_01 placed at (35, 150, -274) with Yaw = -126.60707939 deg.")
```

---

## 3. Configuring the Optional Collision Proxy (`COL_Leaderboard_Body`)

For optimal physics performance and smooth R15 walk-up navigation around the nine stepped podiums:
1. Set `CanCollide = false`, `CanTouch = false`, and `CanQuery = false` on the visual `MeshPart`s of `SM_Hub_Leaderboard_01` (or keep `CanCollide = true` only on the base plinth and podium stage components).
2. Import **`meshes/collision_proxy/COL_Leaderboard_Body.glb`** (`168` triangles across `5` convex hull components: `COL_Leaderboard_WallPlinthHull`, `COL_Leaderboard_MainWallHull`, `COL_Leaderboard_Stage_A_Hull`, `COL_Leaderboard_Stage_B_Hull`, `COL_Leaderboard_Stage_C_Hull`) with `Merge Meshes = false`.
3. Align `COL_Leaderboard_Body` to the exact same `targetCFrame` (`CFrame.new(35, 150, -274) * CFrame.Angles(0, math.rad(-126.60707939), 0)`), and set every hull `MeshPart` to:
   - `Anchored = true`
   - `Transparency = 1`
   - `CanCollide = true`
   - `CanQuery = false`
   - `CastShadow = false`

---

## 4. Mounting `SurfaceGui` Elements Onto All 15 UI-Ready Surfaces

The production mesh exports **15 dedicated, flat, zero-baked-text `MeshPart` components**:
- **3 Header Surfaces:**
  - `GEO_Leaderboard_UIHeader_A_SessionKOs` (`11.8000 W × 2.3500 H studs`, front `Z = +0.1800`)
  - `GEO_Leaderboard_UIHeader_B_SessionWins` (`11.8000 W × 2.6000 H studs`, front `Z = +0.2800`)
  - `GEO_Leaderboard_UIHeader_C_SessionStandings` (`11.8000 W × 2.3500 H studs`, front `Z = +0.1800`)
- **3 Main Table Surfaces:**
  - `GEO_Leaderboard_UIMain_A_SessionKOs` (`11.8000 W × 13.0000 H studs`, front `Z = +0.1800`)
  - `GEO_Leaderboard_UIMain_B_SessionWins` (`11.8000 W × 13.4000 H studs`, front `Z = +0.2800`)
  - `GEO_Leaderboard_UIMain_C_SessionStandings` (`11.8000 W × 13.0000 H studs`, front `Z = +0.1800`)
- **9 Podium Nameplate Surfaces:**
  - Stage A (`SESSION KOs`): `GEO_Leaderboard_PodiumNameplate_A2_2ND` (`2.90 × 0.98`), `GEO_Leaderboard_PodiumNameplate_A1_1ST` (`3.10 × 1.32`), `GEO_Leaderboard_PodiumNameplate_A3_3RD` (`2.90 × 0.68`)
  - Stage B (`SESSION WINS`): `GEO_Leaderboard_PodiumNameplate_B2_2ND` (`2.90 × 0.98`), `GEO_Leaderboard_PodiumNameplate_B1_1ST` (`3.10 × 1.32`), `GEO_Leaderboard_PodiumNameplate_B3_3RD` (`2.90 × 0.68`)
  - Stage C (`SESSION STANDINGS`): `GEO_Leaderboard_PodiumNameplate_C2_2ND` (`2.90 × 0.98`), `GEO_Leaderboard_PodiumNameplate_C1_1ST` (`3.10 × 1.32`), `GEO_Leaderboard_PodiumNameplate_C3_3RD` (`2.90 × 0.68`)

### Recommended `SurfaceGui` Attachment Method
Because Roblox's FBX/GLB importer maps a `MeshPart`'s local `-Z` face to `Enum.NormalId.Front` while our model's outward UI normal is `Local +Z = (0, 0, +1)`:
- **Option 1 (Direct `MeshPart` Adornee):** Parent or set `SurfaceGui.Adornee = uiMeshPart` and set `SurfaceGui.Face = Enum.NormalId.Back` (which corresponds to `Local +Z` in Roblox's `CFrame` convention where `LookVector = -ZVector`), or verify visually in Studio and toggle between `Enum.NormalId.Back` and `Enum.NormalId.Front`.
- **Option 2 (Explicit Adornee `Part` — Recommended for Exact `LookVector` Control):** Create a thin, transparent, non-collidable `Part` aligned so its `CFrame.LookVector` equals the outward world normal `(-0.80274385, 0, -0.59632400)` and mount the `SurfaceGui` with `Face = Enum.NormalId.Front`, `SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud`, and `PixelsPerStud = 50`.

---

## 5. Runtime Placement of the Nine `4.0000-Stud` Podium Display Avatars

No dummy avatar geometry is baked into `SM_Hub_Leaderboard_01`. Later runtime code can place nine `4.0000-stud` display avatars (`Scale = 4.0000 / 5.5000 = 0.727273` via `Model:ScaleTo(0.727273)`) at these exact local offsets relative to `targetCFrame`:

```lua
-- Reference table of the 9 podium avatar foot-level anchors in SM_Hub_Leaderboard_01 local space:
-- Note: In Roblox CFrame.lookAt, a character facing Local +Z has LookVector = targetCFrame:VectorToWorldSpace(Vector3.new(0, 0, 1))
local PODIUM_AVATAR_LOCAL_ANCHORS = {
    A2 = Vector3.new(-7.5500, 1.9500, 3.0500),
    A1 = Vector3.new(-3.7000, 2.5000, 3.0250),
    A3 = Vector3.new( 0.1500, 1.5000, 3.0500),
    B2 = Vector3.new( 6.1500, 1.9500, 3.0500),
    B1 = Vector3.new(10.0000, 2.5000, 3.0250),
    B3 = Vector3.new(13.8500, 1.5000, 3.0500),
    C2 = Vector3.new(19.8500, 1.9500, 3.0500),
    C1 = Vector3.new(23.7000, 2.5000, 3.0250),
    C3 = Vector3.new(27.5500, 1.5000, 3.0500),
}
```

---

## 6. Manual Roblox Studio Verification Checklist (`NOT RUN` in Headless Linux VM)

Because Roblox Studio is unavailable in the build container, execute the following manual checks when importing into the live Studio place:
1. **Live Import & Orientation (`NOT RUN`):** Confirm `SM_Hub_Leaderboard_01` at `(35, 150, -274)` (`Yaw = -126.60707939°`) faces radially inward toward `(0, 150, -300)` with the three podium stages (`Stage A`, `Stage B`, `Stage C`) in front of the wall.
2. **Base Grounding on `World Y = 150.0000` (`NOT RUN`):** Confirm `GEO_Leaderboard_WallPlinth` and `GEO_Leaderboard_PodiumStage_A/B/C_Base` sit flush on `SM_Hub_PlazaPlatform_01` with zero floating gap or floor penetration.
3. **`SurfaceGui` Rendering on All 15 Surfaces (`NOT RUN`):** Attach test `SurfaceGui` instances to the 3 headers, 3 main tables, and 9 podium nameplates and verify crisp text rendering without Z-fighting.
4. **Nine `4.0-Stud` Avatar Stand-In Placement (`NOT RUN`):** Place 9 test R15 rigs scaled to `4.0` studs (`Model:ScaleTo(4.0 / 5.5)`) on `A2..C3` and verify they stand cleanly on the podium tops below the `Y = 6.20` main table rows.
5. **R15 Walkability & Shop Bar Clearance (`NOT RUN`):** Spawn a standard R15 character at `(0, 150, -334)`, walk to `(35, 150, -274)`, walk through the `5.71–7.25-stud` corridor next to `SM_Hub_ShopKiosk_01`, and walk through the two `1.70-stud` inter-stage gaps without snagging on `COL_Leaderboard_Body`.
