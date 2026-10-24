# Hub Spatial Integration & Clearance Report — `SM_Hub_ShopKiosk_01` (Phase 2 Approved Arena Shop Bar)

## 1. Inspected Authoritative Sources & Local Reference Assets (Unmodified)

### Authoritative Project Specifications Inspected
- `tasks/TASK-03-KINETIC-HUB-ENVIRONMENT.md` (local clone in `/tmp/sphere_ball_repo/Sphere_Ball-alpha/tasks/TASK-03-KINETIC-HUB-ENVIRONMENT.md`)
- `tasks/TASK-09-ASSETS-VFX-ANIMATION-AUDIO.md` (local clone in `/tmp/sphere_ball_repo/Sphere_Ball-alpha/tasks/TASK-09-ASSETS-VFX-ANIMATION-AUDIO.md`)
- `MASTER_IMPLEMENTATION_PLAN.md` (§2.2, §2.4, §11.1, §11.3, §11.4)
- `specs/DESIGN_CONSTANTS.md` & `DECISION_LOG.md` (D-001..D-027)
- `3d-argon/sphere_brawl_master_3d_art_bible_and_technical_handoff.md` (inspected at `/working_dir/c_81d349259c19ffa4/artifacts/file_generation/ttl=63d/output/Sphere_Brawl_Master_3D_Art_Bible_and_Technical_Handoff.md`)
- Approved Phase 1 Concept Package: `3d-argon/changes/6/Sphere_Brawl_Shop_Bar_Concept_Reset_01.zip`

### Inspected Local Reference Packages (Unmodified)
1. **`SM_Hub_PlazaPlatform_01` (Step 1):**
   - Path inspected: `/working_dir/c_5ea4f32289a6a5cc/3d-argon/changes/3/Sphere_Brawl_Hub_Platform_01_Package/meshes/SM_Hub_PlazaPlatform_01.obj` (`2,688 triangles`, `140.0 × 12.0 × 140.0 studs`).
   - Top walking surface at `World Y = 150.0000` (`Local Y = 0.0000`).
   - Flat Peripheral Station Plaza Ring spans radial distance `R = 37.0000 to 52.5000 studs` from `(0, 150, -300)`.
2. **`SM_Hub_QueuePadRing_01` (Step 2):**
   - Path inspected: `/working_dir/c_5b3a5c0f9b5080c8/3d-argon/changes/4/Sphere_Brawl_Hub_QueuePadRing_01_Package/meshes/SM_Hub_QueuePadRing_01.obj` (`960 triangles`, `28.0 × 0.076 × 28.0 studs`).
   - Centered at `World (0, 150, -300)` with outer radius `R_outer = 14.0000 studs` (`World X in [-14.0000, +14.0000]`).
3. **`SM_Hub_QueuePortalArch_01` (Stage 4):**
   - Path inspected: `/working_dir/c_81d349259c19ffa4/artifacts/file_generation/ttl=63d/output/QueuePortalArch_Prototype.obj` (`3,168 triangles`, `40.80 × 26.65 × 27.83 studs`).
   - Centered at `World (0, 150, -300)` with floor pylon brackets spanning `|X| in [15.0500, 20.4000] studs`.
4. **`SM_Hub_CustomizeKiosk_01` (Step 3):**
   - Path inspected: `/working_dir/c_b4ea4482df5e6ac6/3d-argon/changes/5/Sphere_Brawl_Hub_CustomizeKiosk_01_Package/meshes/SM_Hub_CustomizeKiosk_01.obj` (`2,038 triangles`, `10.0 × 9.5 × 8.0 studs` local).
   - Placed at `World (-43, 150, -300)` facing `+X` with world-aligned bounds `World X in [-47.0000, -39.0000]`, `World Y in [150.0000, 159.5000]`, `World Z in [-305.0000, -295.0000]`.

## 2. Valid Right-Handed Placement Transform & Measured World-Space Footprint

When the approved `SM_Hub_ShopKiosk_01` Arena Shop Bar (`20.0000 (W) × 7.6000 (H) × 8.0000 (D) studs` local) is placed at `World (43.0000, 150.0000, -300.0000)` using the verified right-handed `-90°` yaw rotation:

```luau
local targetCFrame =
    CFrame.new(43, 150, -300)
    * CFrame.Angles(0, math.rad(-90), 0)
-- Equivalent right-handed orthonormal basis:
-- CFrame.fromMatrix(
--     Vector3.new(43, 150, -300),
--     Vector3.new(0, 0, 1),  -- local +X / RightVector
--     Vector3.new(0, 1, 0),  -- local +Y / UpVector
--     Vector3.new(-1, 0, 0)  -- local +Z / ZVector
-- )
```

Every exported local vertex `(x_local, y_local, z_local)` transforms via `World = (43.0 - z_local, 150.0 + y_local, -300.0 + x_local)`:
- **Measured World Bounding Box (across all `7,272` exported vertices):**
  - **`World X`:** `[39.0000, 47.0000]` (`8.0000 studs` radial depth; front walk-up step at `+39.0000`, rear wing plinth at `+47.0000`)
  - **`World Y`:** `[150.0000, 157.6000]` (`7.6000 studs` vertical height; base underside sits flush on `World Y = 150.0000`)
  - **`World Z`:** `[-310.0000, -290.0000]` (`20.0000 studs` tangential width; symmetric around `Z = -300.0000`)
- **Measured Radial Distance from Hub Center `(0, 150, -300)`:**
  - **Bounding-Box Radial Span:** `R_bbox_min = 39.0000 studs` (`+2.0000 studs` outside `R = 37.00`), `R_bbox_max = sqrt(47^2 + 10^2) = 48.0521 studs` (`4.4479 studs` inside `R = 52.50`).
  - **Actual Exported Mesh Vertex Radial Span (across all `7,272` vertices):**
    - **`R_vertex_min = 39.3026 studs`** (at front plinth chamfer vertex `(39.00, 150.00, -292.80)` and `(39.00, 150.00, -307.20)` — **`+2.3026 studs` outside `R = 37.00`**; along the centerline `Z = -300.0`, the front edge sits at `X = 39.0000`, `R = 39.0000 studs`).
    - **`R_vertex_max = 47.9210 studs`** (at rear wing chamfer vertex `(47.00, 150.00, -309.35)` and `(47.00, 150.00, -290.65)` — **`+4.5790 studs` inside `R = 52.50`**).
  - Consequently, **100% of the exported mesh vertices and bounding footprint fit inside the flat `R = 37.0..52.5 stud` Peripheral Station Plaza Ring** on `SM_Hub_PlazaPlatform_01`.

## 3. Measured Edge-to-Edge Clearances to Neighbouring Hub Stations & Routes

| Neighbouring Hub Feature | Feature World Envelope / Location | Center-to-Center Distance | Measured Edge-to-Edge Clearance | Status |
|---|---|---:|---:|---|
| **`SM_Hub_QueuePadRing_01`** | Centered at `(0, 150, -300)`, `R_outer = 14.0000` (`X_max = +14.0000`) | `43.0000 studs` | **`25.0000 studs`** (`39.0000 - 14.0000`) of unobstructed flat plaza floor | **PASS** |
| **`SM_Hub_QueuePortalArch_01` (East Pylon)** | Floor brackets span `X in [+15.0500, +20.4000]`, `Z in [-304.8, -295.2]` | `43.0000 studs` | **`18.6000 studs`** (`39.0000 - 20.4000`) to outer east pylon cleat (`23.9500 studs` to inner arch leg at `X = +15.05`) | **PASS** |
| **`SM_Hub_CustomizeKiosk_01`** | Placed at `(-43, 150, -300)`, `World X in [-47.0000, -39.0000]` | `86.0000 studs` | **`78.0000 studs`** (`39.0000 - (-39.0000)`) across the central plaza | **PASS** |
| **Main Spawn-to-Queue Route** | Spawn `(0, 150, -334)` -> Portal `(0, 150, -300)` (`X = 0` corridor) | `43.0000 studs` | **`39.0000 studs`** lateral clearance from the `X = 0` spawn-to-portal sightline | **PASS** |
| **Mode Selection Board (`SM_Hub_ModeBoard_01`)** | Locked center `(35, 150, -326)`, proposed `14.0 × 8.5 × 3.0 studs` | `27.2029 studs` | **`16.0000 studs`** along Z from `Z = -310.0` to Mode Board center (`> 9.0 studs` clear walkway to proposed envelope) | **PASS** |
| **Leaderboard Display (`SM_Hub_Leaderboard_01`)** | Locked center `(35, 150, -274)`, proposed `6.5 × 16.0 × 4.5 studs` | `27.2029 studs` | **`16.0000 studs`** along Z from `Z = -290.0` to Leaderboard center (`> 12.5 studs` clear walkway to proposed envelope) | **PASS** |
| **Plaza Outer Curb Bezel (`SM_Hub_PlazaPlatform_01`)** | `R_curb_inner = 63.2000 studs` (`R_outer = 70.0000 studs`) | — | **`15.2790 studs`** (`63.2000 - 47.9210`) of rear perimeter walkway clearance (`22.0790 studs` to outer rim) | **PASS** |
