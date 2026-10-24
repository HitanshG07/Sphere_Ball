# Hub Spatial & Repository Integration Report — `SM_Hub_ModeBoard_01`

- **Canonical Asset ID:** `SM_Hub_ModeBoard_01`
- **Package Directory:** `3d-argon/changes/7/Sphere_Brawl_Hub_ModeBoard_01_Package/`
- **Archive Name:** `Sphere_Brawl_Hub_ModeBoard_01_Package.zip`
- **Approved Concept Baseline:** `Sphere_Brawl_Hub_ModeBoard_Concept_01.zip` (`SHA-256: e76c211dd44fc5c36d71a546ef8e683de05923e8ee142e203173caabeeaddeb6`)

---

## 1. Ready-to-Merge `assets/asset-manifest.json` Entry

The entry below (also saved as a standalone file at `manifest/SM_Hub_ModeBoard_01.manifest.json`) strictly conforms to `specs/ASSET_MANIFEST.schema.json` (`additionalProperties: false`, all required fields present, `robloxAssetId: null` until published in Roblox Studio):

```json
{
  "id": "hub.station.mode_board",
  "name": "SM_Hub_ModeBoard_01",
  "kind": "model",
  "status": "EXPORTED",
  "destination": "Workspace.KineticHub.Stations.SM_Hub_ModeBoard_01",
  "source": "3d-argon/changes/7/Sphere_Brawl_Hub_ModeBoard_01_Package/scripts/generate_mode_board_blender.py",
  "rightsStatus": "ORIGINAL_GENERATED",
  "robloxAssetId": null,
  "triangles": 1612,
  "textureResolution": "64x64",
  "collision": "VISUAL_ONLY",
  "platformBudget": "DESKTOP_AND_MOBILE",
  "notes": "Physical four-mode selection command gantry at (35, 150, -326) oriented radially inward toward Hub center (0, 150, -300) via CFrame.new(35, 150, -326) * CFrame.Angles(0, math.rad(-53.39292061), 0). Local envelope 14.4000(W) x 3.8000(D) x 8.8000(H) studs with 14.0-degree inclined command matrix. Contains 18 named components including 5 separate flat UI-ready replaceable surfaces (GEO_ModeBoard_UIPanel_01_FFA, GEO_ModeBoard_UIPanel_02_Duel, GEO_ModeBoard_UIPanel_03_TeamClash, GEO_ModeBoard_UIPanel_04_KingTile, GEO_ModeBoard_HeaderSign) with zero baked text, plus optional 36-triangle collision proxy COL_ModeBoard_Body."
}
```

---

## 2. Inspected Neighbouring Hub Assets & Measured Production Clearances

All existing approved Kinetic Hub assets in the workspace were inspected directly at the vertex level (without modifying any existing file):

| Neighbour Asset ID | Inspected Package Path | World Placement & Orientation | Measured Production Clearance to `SM_Hub_ModeBoard_01` (`(35, 150, -326)`, `Yaw = -53.3929°`) | Status |
|---|---|---|---|---|
| **`SM_Hub_PlazaPlatform_01`** | `/working_dir/c_5ea4f32289a6a5cc/3d-argon/changes/3/Sphere_Brawl_Hub_Platform_01_Package/meshes/SM_Hub_PlazaPlatform_01.obj` (`2,688 tris`) | `(0, 150, -300)`, `D = 140.0 studs`, flat Peripheral Station Ring `R in [37.0000, 52.5000] studs` at `World Y = 150.0000` | Transformed production vertices span **`R_vertex in [41.7610, 46.0024] studs`** (`+4.7610 studs` inside inner edge `R = 37.0`, `+6.4976 studs` inside outer edge `R = 52.5`, **`17.1976 studs` clear** of outer curb bezel `R = 63.2`, and **`23.9976 studs` clear** of outer rim `R = 70.0`). Base sits flush on `World Y = 150.0000`. | **MEASURED — PASS** |
| **`SM_Hub_ShopKiosk_01`** | `/working_dir/c_41d135f96d245249/3d-argon/changes/6/Sphere_Brawl_Hub_ShopKiosk_01_Package/meshes/SM_Hub_ShopKiosk_01.obj` (`2,424 tris`) | `(43, 150, -300)`, `Yaw = -90°`, world bounds `X in [39.00, 47.00]`, `Z in [-310.00, -290.00]` | **`10.1829 studs` minimum pairwise XZ vertex distance** (`9.3320 studs` along World Z between Shop Bar south wing `Z = -310.0000` and Mode Board north-east vertex `Z = -319.3320`). Leaves an unobstructed `> 9.3-stud` player walkway between stations. | **MEASURED — PASS** |
| **`SM_Hub_QueuePadRing_01`** | `/working_dir/c_5b3a5c0f9b5080c8/3d-argon/changes/4/Sphere_Brawl_Hub_QueuePadRing_01_Package/meshes/SM_Hub_QueuePadRing_01.obj` (`960 tris`) | `(0, 150, -300)`, `R_outer = 14.0000 studs` | **`27.7610 studs` radial edge-to-edge clearance** (`41.7610 - 14.0000`) across open flat plaza floor. | **MEASURED — PASS** |
| **`SM_Hub_QueuePortalArch_01`** | `/working_dir/c_81d349259c19ffa4/artifacts/file_generation/ttl=63d/output/QueuePortalArch_Prototype.obj` (`3,168 tris`) | `(0, 150, -300)`, East Pylon floor footprint `X in [+15.05, +20.40]`, `Z in [-304.80, -295.20]` | **`24.5615 studs` minimum pairwise XZ vertex distance** from the East Portal Pylon to the Mode Board's closest vertex. | **MEASURED — PASS** |
| **`SM_Hub_CustomizeKiosk_01`** | `/working_dir/c_b4ea4482df5e6ac6/3d-argon/changes/5/Sphere_Brawl_Hub_CustomizeKiosk_01_Package/meshes/SM_Hub_CustomizeKiosk_01.obj` (`2,038 tris`) | `(-43, 150, -300)`, `Yaw = +90°`, world bounds `X in [-47.00, -39.00]`, `Z in [-305.00, -295.00]` | **`68.3702 studs` along X** across the central plaza (`29.3702 - (-39.0000)`). | **MEASURED — PASS** |
| **Main Spawn-to-Portal Corridor** | `GameConfig.Lobby.SpawnCFrame` (`(0, 150, -334)` facing `+Z` to `(0, 150, -300)` along `X = 0`, `D-015`) | `X = 0.0000`, `Z in [-334.0, -300.0]` | **`29.3702 studs` lateral clearance** from the `X = 0` sightline centerline (`26.3702 studs` from a `6-stud` wide spawn corridor). | **MEASURED — PASS** |
| **`SM_Hub_Leaderboard_01` (Future Step 6)** | Not yet built as a production mesh package; Art Bible proposed reference envelope `6.5 (W) × 4.5 (D) × 16.0 (H) studs` | Locked center `(35, 150, -274)` (`52.0000 studs` north along Z) | **`42.3018 studs` estimated edge-to-edge Z clearance** (`-277.03 - (-319.3320)`). Marked **`ESTIMATED`** until `SM_Hub_Leaderboard_01` production geometry exists. | **ESTIMATED — PASS** |

---

## 3. UI-Ready Surface Mounting Guidance & Required Studio Verification Steps

1. **Five Separate Replaceable UI-Ready Components:**
   - `GEO_ModeBoard_UIPanel_01_FFA` (`4.0800 W × 3.7800 H studs`, `14.0°` tilt, world front center `(32.8248, 154.4879, -328.1204)`)
   - `GEO_ModeBoard_UIPanel_02_Duel` (`5.0400 W × 1.2000 H studs`, `14.0°` tilt, world front center `(36.7836, 156.0478, -323.7370)`)
   - `GEO_ModeBoard_UIPanel_03_TeamClash` (`5.0400 W × 1.2000 H studs`, `14.0°` tilt, world front center `(36.4613, 154.4371, -323.4976)`)
   - `GEO_ModeBoard_UIPanel_04_KingTile` (`5.0400 W × 1.2000 H studs`, `14.0°` tilt, world front center `(36.1389, 152.8264, -323.2581)`)
   - `GEO_ModeBoard_HeaderSign` (`11.4800 W × 0.8200 H studs`, `0.0°` upright, world front center `(34.2936, 157.9500, -325.4752)`)
2. **Modular 3D Relief Components:**
   - `GEO_ModeBoard_ActiveModeReticle`, `GEO_ModeBoard_LockReliefs`, and `GEO_ModeBoard_ModeReliefs` are separate child `MeshPart`s so UI engineers can keep them visible alongside `SurfaceGui` labels or hide/toggle individual lock reliefs when future game modes unlock.
3. **Required Manual Verification Steps in Roblox Studio (`NOT RUN` in Linux VM):**
   - Import `meshes/SM_Hub_ModeBoard_01.glb` into a Studio test place with `Merge Meshes = false` and run the Command Bar script in `ROBLOX_STUDIO_IMPORT_GUIDE.md` §2.
   - Verify that the base underside rests flush on `SM_Hub_PlazaPlatform_01` at `World Y = 150.0000` with zero floating gap or floor penetration.
   - Spawn an R15 test character at `(0, 150, -334)` and walk to `(35, 150, -326)` to confirm smooth walk-up approach onto the front threshold plates and non-snagging collision against `COL_ModeBoard_Proxy`.
