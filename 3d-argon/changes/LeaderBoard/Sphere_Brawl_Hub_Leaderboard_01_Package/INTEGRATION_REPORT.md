# Hub Spatial & Repository Integration Report — `SM_Hub_Leaderboard_01`

- **Canonical Asset ID:** `SM_Hub_Leaderboard_01`
- **Package Directory:** `3d-argon/changes/8/Sphere_Brawl_Hub_Leaderboard_01_Package/`
- **Archive Name:** `Sphere_Brawl_Hub_Leaderboard_01_Package.zip`
- **Approved Concept Baseline:** `Sphere_Brawl_Hub_Leaderboard_Concept_06.zip` (`SHA-256: bb705ed9a35fca5ada4f0065f90db818010aafc85f00986946967323080f15e0`)

---

## 1. Schema-Compliant Candidate `assets/asset-manifest.json` Entry

Inspected `assets/asset-manifest.json` and `specs/ASSET_MANIFEST.schema.json` (`additionalProperties: false`, required fields: `id`, `name`, `kind`, `status`, `destination`, `source`, `rightsStatus`, `notes`). The candidate entry below (also saved at `manifest/SM_Hub_Leaderboard_01.manifest.json`) is ready to merge when the owner integrates the asset into the repository. **No unrelated repository files were modified.**

```json
{
  "id": "hub.station.leaderboard",
  "name": "SM_Hub_Leaderboard_01",
  "kind": "model",
  "status": "EXPORTED",
  "destination": "Workspace.KineticHub.Stations.SM_Hub_Leaderboard_01",
  "source": "3d-argon/changes/8/Sphere_Brawl_Hub_Leaderboard_01_Package/scripts/generate_hub_leaderboard_blender.py",
  "rightsStatus": "ORIGINAL_GENERATED",
  "robloxAssetId": null,
  "triangles": 1852,
  "textureResolution": "64x64",
  "collision": "VISUAL_ONLY",
  "platformBudget": "DESKTOP_AND_MOBILE",
  "notes": "Grand three-board session leaderboard monument and 9-position podium array at (35, 150, -274) facing Hub center (0, 150, -300) via CFrame.new(35, 150, -274) * CFrame.Angles(0, math.rad(-126.60707939), 0). Local envelope 42.0000(W) x 26.0000(H) x 9.0000(D) studs (X in [-11.0, +31.0], Y in [0.0, +26.0], Z in [-4.2, +4.8]). Features 53 named components including 3 themed leaderboard modules (Cyan Session KOs, Amber Session Wins, Magnetic Purple Session Standings), 3 separate 3-place podium stages (9 podiums total), 15 separate flat replaceable UI-ready surfaces (3 headers, 3 main tables, 9 podium nameplates) with zero baked text and zero baked avatars, plus optional 168-triangle collision proxy COL_Leaderboard_Body."
}
```

---

## 2. Inspected Neighbouring Hub Assets & Measured Production Clearances

All existing approved Kinetic Hub station packages on disk (`3d-argon/changes/3..7`) were inspected directly at the vertex level and compared against the transformed vertices of `SM_Hub_Leaderboard_01.obj` at `(35, 150, -274)` (`Yaw = -126.60707939°`):

| Neighbour Asset / Feature | Inspected Source & World Placement | Measured / Calculated Production Clearance | Verification Status |
|---|---|---|---|
| **`SM_Hub_PlazaPlatform_01`** | `3d-argon/changes/3/.../SM_Hub_PlazaPlatform_01.obj` at `(0, 150, -300)` (`R_curb = 63.2000`, `R_platform = 64.0000`, `R_rim = 70.0000`) | Transformed vertices span **`R_hub in [38.8377, 56.8872] studs`**. Extends `4.3872 studs` past the nominal `R = 52.5` station band on the outer Starboard rear corner due to the locked `42.0-stud` straight wall, while remaining **`6.3128 studs` inside** the `R = 63.2` outer plaza curb (`7.1128 studs` inside `R = 64.0`). Base grounded flush at `World Y = 150.0000`. | **MEASURED — PASS** |
| **`SM_Hub_ShopKiosk_01` (Approved Package Placement)** | `3d-argon/changes/6/.../SM_Hub_ShopKiosk_01.obj` at `(43, 150, -300)` (`Yaw = -90°`, World AABB `X[39.0, 47.0], Y[150.0, 157.6], Z[-310.0, -290.0]`) | **`7.2474 studs` min pairwise XZ vertex distance** \| **`5.9254 studs` vertex-to-AABB distance** \| **`5.7088 studs` AABB-to-AABB Z gap** (`-284.2912 - (-290.0000)`). | **MEASURED — PASS** |
| **`SM_Hub_ShopKiosk_01` (Legacy `TASK-03` Placement)** | `SM_Hub_ShopKiosk_01.obj` placed at `(35, 150, -300)` (`Yaw = -90°`, World AABB `X[31.0, 39.0], Z[-310.0, -290.0]`) | **`5.8700 studs` 2D polygon-edge-to-polygon-edge gap** (`5.7340 studs` min pairwise XZ vertex distance; `5.7088 studs` AABB-to-AABB Z gap). Preserves an unobstructed walkable player corridor. | **MEASURED — PASS** |
| **`SM_Hub_ModeBoard_01` (Approved Package Placement)** | `3d-argon/changes/7/.../SM_Hub_ModeBoard_01.obj` at `(35, 150, -326)` (`Yaw = -53.39292061°`, World AABB `X[29.3702, 40.6298], Y[150.0, 158.8], Z[-332.6738, -319.3320]`) | **`35.0413 studs` min pairwise XZ vertex distance** \| **`35.0408 studs` AABB-to-AABB Z gap** (`-284.2912 - (-319.3320)`). | **MEASURED — PASS** |
| **`SM_Hub_ModeBoard_01` (Alternate North Station Placement)** | `SM_Hub_ModeBoard_01.obj` at `(0, 150, -245)` (`Yaw = 180°`, World AABB `X[-7.20, +7.20], Z[-246.90, -243.10]`) | **`9.0858 studs` min pairwise XZ vertex distance** \| **`8.8510 studs` vertex-to-AABB distance** (`8.57 studs` to `15×4` blockout). | **MEASURED — PASS** |
| **`SM_Hub_QueuePadRing_01`** | `3d-argon/changes/4/.../SM_Hub_QueuePadRing_01.obj` at `(0, 150, -300)` (`R_outer = 14.0000 studs`) | **`24.8377 studs` radial edge-to-edge clearance** (`38.8377 - 14.0000 studs`) across the open flat plaza deck, leaving a massive walk-up viewing apron in front of all 9 podiums. | **MEASURED — PASS** |
| **`SM_Hub_CustomizeKiosk_01`** | `3d-argon/changes/5/.../SM_Hub_CustomizeKiosk_01.obj` at `(-43, 150, -300)` (`Yaw = +90°`, World AABB `X[-47.0, -39.0], Z[-305.0, -295.0]`) | **`52.7938 studs` lateral X clearance** (`13.7938 - (-39.0000)`) across the central plaza. | **MEASURED — PASS** |
| **Main Spawn-to-Queue Sightline** | `SpawnCFrame` `(0, 150, -334)` facing `+Z` toward `(0, 150, -300)` along `X = 0` (`D-015`) | **`13.7938 studs` lateral X clearance** from `X = 0.0000` (`10.7938 studs` from a `6-stud` spawn corridor). Zero sightline obstruction. | **MEASURED — PASS** |

---

## 3. Deferred Runtime Integration Scope & Dependencies

In strict compliance with Alpha scope (`MASTER_IMPLEMENTATION_PLAN.md` §3, `TASK-03`, `TASK-09`), this package provides **static 3D geometry, collision proxy, and exact placement/UI/avatar coordinates only**. The following systems are intentionally excluded from this mesh task and remain separate runtime integration work:
1. **Session-Only Leaderboard Data Collection & Sorting:** Populating `SESSION KOs`, `SESSION WINS`, and `SESSION STANDINGS` from live server session state (no `DataStoreService`, no persistent cross-server rankings). The runtime sorting rule for `SESSION STANDINGS` (`KOs + WINS` vs. primary/tie-breaker sort) is deferred to the UI/gameplay integration task.
2. **Runtime `SurfaceGui` Creation & Binding:** Attaching and updating the 15 `SurfaceGui` instances on `GEO_Leaderboard_UIHeader_A..C`, `GEO_Leaderboard_UIMain_A..C`, and `GEO_Leaderboard_PodiumNameplate_A1..C3`.
3. **Runtime `4.0000-Stud` Podium Avatar Spawning:** Cloning or rendering the top-3 players' characters (or default stand-ins when fewer than 3 players are present) scaled to `4.0000` studs at the 9 documented podium anchor positions (`A2, A1, A3, B2, B1, B3, C2, C1, C3`).
