# ROBLOX STUDIO IMPORT & INTEGRATION GUIDE — `SM_Arena_TileVisual_01`

| Property | Value |
| :--- | :--- |
| **Target Engine** | Roblox Studio (Luau `--!strict`) |
| **Scale Ratio** | `1 Blender/OBJ/GLB unit = 1.0 Roblox stud` |
| **Recommended Destination** | `ReplicatedStorage.Assets.ArenaTiles` (Templates) -> Cloned into `Workspace.Arena.VisualTiles` & `Workspace.Arena.HazardOverlays` |
| **Collision Contract** | **`CanCollide = false`, `CanTouch = false`, `CanQuery = false`, `Anchored = true`, `Massless = true`** on ALL visual tile and overlay MeshParts |

## 1. Importing the Base Visual Tiles & Overlays into Roblox Studio

1. Open **Roblox Studio** -> **Asset Manager** -> **Bulk Import** (or **Avatar / 3D Importer**).
2. Select the `.glb` (or `.obj`) files from `meshes/` and `meshes/overlays/`:
   - `meshes/SM_Arena_TileVisual_01_VariantA.glb`
   - `meshes/SM_Arena_TileVisual_01_VariantB.glb`
   - `meshes/overlays/OVL_Arena_Warn_Ice.glb`
   - `meshes/overlays/OVL_Arena_Active_Ice.glb`
   - `meshes/overlays/OVL_Arena_Warn_Magnetic.glb`
   - `meshes/overlays/OVL_Arena_Active_MagneticAnchor.glb`
   - `meshes/overlays/OVL_Arena_Active_MagneticField.glb`
   - `meshes/overlays/OVL_Arena_Warn_Boost.glb`
   - `meshes/overlays/OVL_Arena_Active_Boost.glb`
   - `meshes/overlays/OVL_Arena_Collapse_Warn.glb`
3. In the **3D Importer** settings:
   - **Unit Scale:** `Stud` (`1.0`, so Base Tile dimensions read exactly `11.8 × 2.0 × 11.8` and Overlays read `11.4 × 0.05 × 11.4`).
   - **Import As Model:** Checked (preserves sub-component `MeshPart` hierarchy so material/color slots can be styled per component or via the embedded `T_Arena_TilePalette_256.png` texture).
   - **Insert at Scene Origin / Preserve Pivot:** Checked.
4. Store the imported templates in `ReplicatedStorage.Assets.ArenaTiles`:
   ```text
   ReplicatedStorage
   └── Assets
       └── ArenaTiles
           ├── SM_Arena_TileVisual_01_VariantA (Model, PrimaryPart/Pivot at (0,0,0), Size 11.8 × 2.0 × 11.8)
           ├── SM_Arena_TileVisual_01_VariantB (Model, PrimaryPart/Pivot at (0,0,0), Size 11.8 × 2.0 × 11.8)
           └── Overlays (Folder)
               ├── OVL_Arena_Warn_Ice
               ├── OVL_Arena_Active_Ice
               ├── OVL_Arena_Warn_Magnetic
               ├── OVL_Arena_Active_MagneticAnchor
               ├── OVL_Arena_Active_MagneticField
               ├── OVL_Arena_Warn_Boost
               ├── OVL_Arena_Active_Boost
               └── OVL_Arena_Collapse_Warn
   ```

## 2. Configuring Non-Colliding Flags & Material Properties

Every `MeshPart` inside `SM_Arena_TileVisual_01_VariantA`, `SM_Arena_TileVisual_01_VariantB`, and `Overlays/*` **must** have the following Roblox properties set on the template before runtime cloning:

| Roblox `MeshPart` Property | Base Visual Tile (`SM_Arena_TileVisual_01`) | Hazard Overlays (`OVL_Arena_*`) | Authoritative Server `CollisionTile` (Separate `Part`) |
| :--- | :--- | :--- | :--- |
| `Anchored` | `true` | `true` | `true` |
| `CanCollide` | **`false`** | **`false`** | **`true`** |
| `CanTouch` | **`false`** | **`false`** | `true` |
| `CanQuery` | **`false`** | **`false`** | `true` |
| `Massless` | `true` | `true` | `false` |
| `CastShadow` | `true` | `false` | `false` |
| `Transparency` | `0.0` | `0.0` | **`1.0` (Invisible at runtime)** |
| `Size` | `Vector3.new(11.8, 2.0, 11.8)` | `Vector3.new(11.4, 0.05, 11.4)` | `Vector3.new(12.0, 2.0, 12.0)` |

### Applying Native Roblox Materials & Colors (Optional Enhancement Over Palette Texture)
If you wish to use native Roblox `Enum.Material.Metal` and `Enum.Material.Neon` on the child `MeshPart` components (clear `TextureID = ""` on the child `MeshPart` and set `Material` + `Color`):
- `MAT_DarkNeutral`: `Enum.Material.Metal`, `Color3.fromRGB(32, 38, 54)`
- `MAT_AltNeutral`: `Enum.Material.Metal`, `Color3.fromRGB(42, 50, 70)`
- `MAT_LightTrim`: `Enum.Material.Metal`, `Color3.fromRGB(170, 190, 215)`
- `MAT_PrimaryText`: `Enum.Material.Neon`, `Color3.fromRGB(245, 248, 255)`
- `EMI_Cyan`: `Enum.Material.Neon`, `Color3.fromRGB(0, 195, 255)`
- `EMI_Ice`: `Enum.Material.Neon`, `Color3.fromRGB(0, 235, 255)`
- `EMI_Magnetic`: `Enum.Material.Neon`, `Color3.fromRGB(165, 55, 255)`
- `EMI_Kinetic`: `Enum.Material.Neon`, `Color3.fromRGB(255, 125, 0)`
- `EMI_Amber`: `Enum.Material.Neon`, `Color3.fromRGB(255, 170, 0)`
- `EMI_DangerRed`: `Enum.Material.Neon`, `Color3.fromRGB(255, 40, 40)`

## 3. Grid Placement, Checkerboard Parity & Overlay Alignment Contract

Per `MASTER_IMPLEMENTATION_PLAN.md` Section 6, the arena grid center is `ArenaCFrame = CFrame.new(0, 50, 0)` and the pitch is `12.0` studs:

```luau
--!strict
-- Reference Integration Snippet for Arena Visualizer (Documentation Only — Do Not Modify Server Physics)
local ARENA_CFRAME = CFrame.new(0, 50, 0)
local TILE_PITCH = 12.0

-- 1. Compute locked cell world CFrame (apply ArenaCFrame ONCE)
local function getCellWorldCFrame(gridX: number, gridZ: number): CFrame
    return ARENA_CFRAME * CFrame.new(TILE_PITCH * gridX, 0, TILE_PITCH * gridZ)
end

-- 2. Select Checkerboard Variant A (Even) vs. Variant B (Odd)
local function getBaseTileTemplateName(gridX: number, gridZ: number): string
    if ((gridX + gridZ) % 2) == 0 then
        return "SM_Arena_TileVisual_01_VariantA"
    else
        return "SM_Arena_TileVisual_01_VariantB"
    end
end

-- 3. Place Base Visual Tile at Cell Center (World Y = 50.0 -> Top Surface at World Y = 51.0)
local function placeBaseVisualTile(tileModel: Model, gridX: number, gridZ: number)
    local cellCF = getCellWorldCFrame(gridX, gridZ)
    tileModel:PivotTo(cellCF)
end

-- 4. Place & Orient Non-Colliding Hazard Overlay
-- Note: Every overlay mesh has its local origin at (0,0,0) with vertices in Local Y in [+1.00, +1.05].
-- If the Model's WorldPivot is preserved at local (0,0,0), PivotTo(cellCF * rotCF) places the overlay
-- at World Y in [51.00, 51.05] (center Y = 51.025). If Studio auto-centered the Model pivot to its
-- bounding box center (0, 1.025, 0), use cellCF * CFrame.new(0, 1.025, 0) * rotCF.
local function placeHazardOverlay(overlayModel: Model, gridX: number, gridZ: number, yawDegrees: number, pivotIsBBoxCenter: boolean)
    local cellCF = getCellWorldCFrame(gridX, gridZ)
    local rotCF = CFrame.Angles(0, math.rad(yawDegrees), 0)
    if pivotIsBBoxCenter then
        overlayModel:PivotTo(cellCF * CFrame.new(0, 1.025, 0) * rotCF)
    else
        overlayModel:PivotTo(cellCF * rotCF)
    end
end
```

## 4. Handling Overlay Directional Orientation & Ring-Collapse Visual Sink

1. **Directional Orientation (`yawDegrees` around `+Y`):**
   - **Ice Corridor (`OVL_Arena_Warn_Ice`, `OVL_Arena_Active_Ice`):** Supports `0°`, `45°`, `90°`, and `135°` lane orientations. When rotating at `45°` or `135°`, if you want the outer square border (`OVL_WarnIce_AmberBorder` / `OVL_ActiveIce_FrostBorder`) to remain parallel to the tile edges while the inner chevrons/snowflake rotate, rotate only the child motif `MeshPart`s (`OVL_ActiveIce_PaleChevrons`, `OVL_ActiveIce_SnowflakeIcon`) by `45°`/`135°` around the cell's Y-axis, or rotate the entire overlay for cardinal `0°`/`90°` lanes.
   - **Boost Runway (`OVL_Arena_Warn_Boost`, `OVL_Arena_Active_Boost`):** Supports `0°` (`-Z`), `90°` (`-X`), `180°` (`+Z`), and `270°` (`+X`). Every cell in a given runway uses the exact same `yawDegrees`.
   - **Magnetic Storm (`OVL_Arena_Active_MagneticAnchor` vs. `OVL_Arena_Active_MagneticField`):** The designated anchor cell uses `OVL_Arena_Active_MagneticAnchor` (`yaw = 0°`). Surrounding affected cells within the active radius (`2.8` / `2.0` / `1.0` tiles) use `OVL_Arena_Active_MagneticField` rotated so its `-Z` chevron points toward the anchor cell (`yaw = math.deg(math.atan2(dx, dz))` snapped or continuous).
2. **Ring-Collapse Visual Sequence (`D=4` at `T=56s`, `D=3` at `T=98s`):**
   - **Warning Phase (`3.0 seconds` before collapse):** Attach `OVL_Arena_Collapse_Warn` to all cells where `max(math.abs(x), math.abs(z)) == collapsingRingIndex`. Keep the authoritative `12 × 2 × 12` `CollisionTile` active (`CanCollide = true`).
   - **Collapse Timestamp (`T = 0.0s`):** Server `GridService` disables/removes the cell's authoritative `CollisionTile`. Client visualizer tweens the cell's `SM_Arena_TileVisual_01` (and its attached `OVL_Arena_Collapse_Warn`) downward and slightly tilted over `0.5–0.8 seconds` (e.g., `cellCF * CFrame.new(0, -6.0, 0) * CFrame.Angles(math.rad(16), 0, math.rad(-12))`), then hides or destroys the visual instance.

## 5. Manual Studio Seam & Collision Verification Checklist

After importing into Roblox Studio, run these verification checks:
- [ ] **Check 1 (Visual Bounds):** Select `SM_Arena_TileVisual_01_VariantA` and `VariantB` in Explorer; confirm `GetExtentsSize()` / bounding box is `11.8, 2.0, 11.8` studs.
- [ ] **Check 2 (Top Surface Alignment):** Place a tile at `(0, 50, 0)` and a `12 × 2 × 12` `CollisionTile` at `(0, 50, 0)`; confirm both top faces lie at `World Y = 51.0`.
- [ ] **Check 3 (0.20-Stud Inter-Tile Groove):** Place a `3 × 3` patch on `12.0`-stud centers (`x, z in {-1, 0, 1}`); verify a uniform `0.20`-stud visual groove between adjacent tiles.
- [ ] **Check 4 (Non-Colliding Overlays):** Place `OVL_Arena_Active_Boost` or `OVL_Arena_Active_MagneticAnchor` at `(0, 51.025, 0)`; roll a `6.0`-stud sphere across the cell at `42 studs/s` and confirm zero physical bump, snag, or collision with the visual tile or overlay.
