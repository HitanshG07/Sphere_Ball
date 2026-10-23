# Hub Spatial Integration & Clearance Report — `SM_Hub_CustomizeKiosk_01`

## 1. Inspected Reference Assets (Unmodified)

1. **`SM_Hub_PlazaPlatform_01` (Step 1):**
   - Path inspected: `/working_dir/c_5ea4f32289a6a5cc/artifacts/file_generation/ttl=63d/output/SM_Hub_PlazaPlatform_01.obj` (`2,688 triangles`, `140.0 × 12.0 × 140.0 studs`).
   - Top walking surface at `World Y = 150.0000` (`Local Y = 0.0000`).
   - Peripheral Station Plaza Ring spans `R = 37.0000 to 52.5000 studs` (`100%` flat at `World Y = 150.0000`).
2. **`SM_Hub_QueuePadRing_01` (Step 2):**
   - Path inspected: `/tmp/verify_zip_extract/Sphere_Brawl_Hub_QueuePadRing_01_Package/SM_Hub_QueuePadRing_01.obj` (`960 triangles`, `28.0 × 0.076 × 28.0 studs`).
   - Centered at `World (0, 150, -300)` with outer radius `R_outer = 14.0000 studs` (`World X in [-14.0000, +14.0000]`).
3. **`SM_Hub_QueuePortalArch_01` (Stage 4):**
   - Path inspected: `/working_dir/c_81d349259c19ffa4/artifacts/file_generation/ttl=63d/output/QueuePortalArch_Prototype.obj` (`3,168 triangles`, `40.80 × 26.65 × 27.83 studs`).
   - Centered at `World (0, 150, -300)` with floor pylon brackets spanning `|X| in [15.0500, 20.4000] studs`.

## 2. Valid Right-Handed Placement Transform & Exact World-Space Clearances

When `SM_Hub_CustomizeKiosk_01` (`10.0 × 9.5 × 8.0 studs` local) is placed at `World (-43.0000, 150.0000, -300.0000)` using the valid right-handed `+90°` yaw rotation:

```luau
local targetCFrame =
    CFrame.new(-43, 150, -300)
    * CFrame.Angles(0, math.rad(90), 0)
-- Equivalent to:
-- CFrame.fromMatrix(
--     Vector3.new(-43, 150, -300),
--     Vector3.new(0, 0, -1), -- local +X / RightVector
--     Vector3.new(0, 1, 0),  -- local +Y / UpVector
--     Vector3.new(1, 0, 0)   -- local +Z / ZVector
-- )
```

Every local coordinate `(x_local, y_local, z_local)` transforms to `World = (-43.0 + z_local, 150.0 + y_local, -300.0 - x_local)`:

- **World Bounding Box:**
  - `World X`: `[-47.0000, -39.0000]` (`8.0000 studs`; rear gantry spine at `-47.00`, front approach toe at `-39.00`)
  - `World Y`: `[150.0000, 159.5000]` (`9.5000 studs`; base flush on `World Y = 150.0000` walking deck)
  - `World Z`: `[-305.0000, -295.0000]` (`10.0000 studs`; symmetric around `Z = -300.0000`)
- **Four Placeholder Sphere World Positions (`R = 0.9000 studs`):**
  - `GEO_CustomizeKiosk_PreviewSphere_01`: `Local (-3.35, 3.05, +0.55)` -> **`World (-42.4500, 153.0500, -296.6500)`**
  - `GEO_CustomizeKiosk_PreviewSphere_02`: `Local (-1.15, 3.50, -0.45)` -> **`World (-43.4500, 153.5000, -298.8500)`**
  - `GEO_CustomizeKiosk_PreviewSphere_03`: `Local (+1.15, 3.50, -0.45)` -> **`World (-43.4500, 153.5000, -301.1500)`**
  - `GEO_CustomizeKiosk_PreviewSphere_04`: `Local (+3.35, 3.05, +0.55)` -> **`World (-42.4500, 153.0500, -303.3500)`**
- **Radial Distance from Hub Center `(0, 150, -300)`:**
  - Nearest point on front approach step (`(-39.00, 150.00, -300.00)`): `R_min = 39.0000 studs` (`+2.0000 studs` outside the `R = 37.00` mid-deck guide ring).
  - Farthest rear corners (`(-47.00, 150.00, -305.00)` and `(-47.00, 150.00, -295.00)`): `R_max = sqrt((-47)^2 + (5)^2) = 47.2652 studs` (`5.2348 studs` inside the `R = 52.50` station ring outer edge).
  - Consequently, **100% of the kiosk footprint sits inside the flat `R = 37.0..52.5 stud` Peripheral Station Plaza Ring** on `SM_Hub_PlazaPlatform_01`.
- **Measured Clearances to Adjacent Hub Features:**
  - **To `SM_Hub_QueuePadRing_01` (`R = 14.0000`, `X = -14.0000`):** `39.0000 - 14.0000 = 25.0000 studs` of unobstructed flat plaza floor.
  - **To `SM_Hub_QueuePortalArch_01` West Pylon (`X = -15.0500`):** `39.0000 - 15.0500 = 23.9500 studs` of horizontal clearance.
  - **To `SM_Hub_PlazaPlatform_01` Inner Framing Ring (`R = 21.2000`):** `39.0000 - 21.2000 = 17.8000 studs` of horizontal clearance.
  - **To `SM_Hub_PlazaPlatform_01` Outer Curb Bezel (`R = 63.2000`):** `63.2000 - 47.2652 = 15.9348 studs` of rear perimeter walkway clearance.
  - **To `SM_Hub_PlazaPlatform_01` Outer Rim (`R = 70.0000`):** `70.0000 - 47.2652 = 22.7348 studs` of clearance.
  - **To Optional Reward Display Station (`(-38, 150, -326)`):** Center-to-center distance = `sqrt(5^2 + 26^2) = 26.4764 studs` (`> 21 studs` edge-to-edge clearance).
