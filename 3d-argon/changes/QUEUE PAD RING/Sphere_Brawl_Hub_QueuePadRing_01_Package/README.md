# Sphere Brawl: Rolling Rampage — Hub Queue Pad Ring (`SM_Hub_QueuePadRing_01`)

**Package Path:** `3d-argon/changes/4/Sphere_Brawl_Hub_QueuePadRing_01_Package/`  
**Asset ID:** `SM_Hub_QueuePadRing_01`  
**Asset Type:** Static Decorative Environment Mesh (14-Stud-Radius Hub Queue Boundary Ring)  
**Scope:** `TASK-03` Kinetic Hub Environment + `TASK-09` Assets, VFX, Animation and Audio  
**Authoritative References:** `tasks/TASK-03-KINETIC-HUB-ENVIRONMENT.md`, `tasks/TASK-09-ASSETS-VFX-ANIMATION-AUDIO.md`, `MASTER_IMPLEMENTATION_PLAN.md` (§2.2, §2.4, §5.1, §11.1, §11.3), `specs/DESIGN_CONSTANTS.md`, `DECISION_LOG.md`, `assets/asset-manifest.json`, `3d-argon/sphere_brawl_master_3d_art_bible_and_technical_handoff.md`

---

## 1. Executive Summary

This package delivers the production-ready static 3D mesh asset **`SM_Hub_QueuePadRing_01`**, which visually defines the `14.0-stud` outer radius (`28.0-stud` diameter) physical matchmaking queue boundary centered at `World (0, 150, -300)` on the Kinetic Hub plaza platform:

- **Exact Measured Dimensions:**
  - **Outer Radius (`R_outer`):** `14.0000 studs` (`Outer Diameter = 28.0000 studs`, `X/Z in [-14.0000, +14.0000]`)
  - **Inner Radius (`R_inner`):** `12.8000 studs` (`Inner Clear Diameter = 25.6000 studs`)
  - **Radial Band Width:** `1.2000 studs` (`R in [12.8000, 14.0000] studs`)
  - **Vertical Profile & Thickness:** `Local Y in [+0.0040, +0.0800] studs` (`0.0760-stud` structural thickness; `0.0800-stud` max height above the `World Y = 150.0000` walking deck; `0.0440-stud` height across the 4 cardinal walk-through threshold gates; `+0.0040-stud` non-coplanar bottom offset to eliminate Z-fighting against the plaza floor)
  - **Polygon Count:** `960 triangles` (`2,880 export vertices`) across `4` material-separated child components (`GEO_QueuePadRing_BaseCollar`, `GEO_QueuePadRing_ChannelInlay`, `GEO_QueuePadRing_TrimBezels`, `GEO_QueuePadRing_CyanConduit`)
- **100% Unobstructed Central Standing Area & Zero Duplication:**
  - Zero triangles or vertices exist inside `R < 12.8000 studs`, preserving a `25.60-stud` diameter open standing area on `SM_Hub_PlazaPlatform_01`'s top deck.
  - Sits cleanly inside `SM_Hub_QueuePortalArch_01` (`+1.0500 studs` horizontal clearance to inner pylon brackets at `|X| = 15.0500 studs`; `+1.2000 studs` radial clearance to portal flank glow rims at `R = 15.2000 studs`) and inside `SM_Hub_PlazaPlatform_01`'s recessed inner framing ring (`+7.2000 studs` clearance to `R = 21.2000 studs`).

---

## 2. Package Contents

| Relative Path in Package (`33` Total Files) | Description |
|---|---|
| `SM_Hub_QueuePadRing_01.obj` | Root Wavefront OBJ mesh (`960 triangles`, `2,880 vertices`, 4 `o GEO_QueuePadRing_*` objects, UVs, vertex colors) |
| `SM_Hub_QueuePadRing_01.mtl` | Root Wavefront MTL material library (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`) |
| `SM_Hub_QueuePadRing_01.glb` | Root Binary glTF 2.0 export (4 child mesh nodes under root `SM_Hub_QueuePadRing_01`, `COLOR_0`, `TEXCOORD_0`, embedded PNG atlas) |
| `SphereBrawl_QueuePadRing_PaletteAtlas.png` | Root `64×64` 2×2 sRGB palette swatch texture referenced by `.glb` and `.obj`/`.mtl` |
| `generate_hub_queue_pad_ring_blender.py` | Root deterministic generator script (runs in standard Python 3 AND inside Blender 3.6+/4.x `bpy`/`bmesh`) |
| `meshes/SM_Hub_QueuePadRing_01.obj` | Subdirectory mirror of `SM_Hub_QueuePadRing_01.obj` (`960 triangles`) |
| `meshes/SM_Hub_QueuePadRing_01.mtl` | Subdirectory mirror of `SM_Hub_QueuePadRing_01.mtl` |
| `meshes/SM_Hub_QueuePadRing_01.glb` | Subdirectory mirror of `SM_Hub_QueuePadRing_01.glb` |
| `meshes/SphereBrawl_QueuePadRing_PaletteAtlas.png` | Companion `64×64` palette atlas alongside `meshes/SM_Hub_QueuePadRing_01.mtl` |
| `textures/SphereBrawl_QueuePadRing_PaletteAtlas.png` | Subdirectory mirror of `64×64` palette swatch texture |
| `scripts/generate_hub_queue_pad_ring_blender.py` | Subdirectory mirror of deterministic generator script |
| `config/queue_pad_ring_parameters.json` | Machine-readable dimensional, material, and per-component metrics |
| `manifest/SM_Hub_QueuePadRing_01.manifest.json` | Canonical asset-manifest entry conforming to `specs/ASSET_MANIFEST.schema.json` |
| `previews/01_Preview_ThreeQuarter_Perspective.png` | Preview 1: Three-quarter perspective view & low-profile rim thickness |
| `previews/02_Preview_Top_Orthographic_14Stud_Boundary.png` | Preview 2: Top orthographic view verifying 14.0-stud outer radius & clear centre |
| `previews/03_Preview_LowAngle_Player_Walkability.png` | Preview 3: Low-angle player camera view & south threshold walkability grazing view |
| `previews/04_Preview_NeutralClay_Geometry.png` | Preview 4: Neutral studio clay geometry view (zero colour distraction) |
| `previews/05_Preview_Wireframe_Topology.png` | Preview 5: Technical wireframe view showing 32-sector topology & 16 clasps |
| `previews/06_Preview_Integration_Portal_and_Plaza.png` | Preview 6: Combined integration scene with `SM_Hub_QueuePortalArch_01` & `SM_Hub_PlazaPlatform_01` |
| `previews/07_Preview_Clearance_Diagram.png` | Preview 7: Labeled radial & cross-sectional clearance diagram |
| `previews/08_Preview_Material_and_Trim_CloseUp.png` | Preview 8: Macro close-up of metallic trim, threshold clasps, and recessed cyan conduit |
| `README.md` | Root package overview and quick-start guide |
| `MODEL_SPECIFICATION.md` | Root full geometric, coordinate, pivot, and per-component specification |
| `ROBLOX_STUDIO_IMPORT_GUIDE.md` | Root step-by-step Roblox Studio import, `WorldPivot`, native material, and test-place guide |
| `VALIDATION_REPORT.md` | Root validation checklist with `PASS` / `NOT RUN` / `REQUIRES OWNER REVIEW` / `ASSET_PENDING` statuses |
| `PORTAL_AND_PLAZA_CLEARANCE_REPORT.md` | Root measured spatial integration and clearance report against Portal Arch & Plaza Platform |
| `docs/README.md` | `docs/` mirror of `README.md` |
| `docs/MODEL_SPECIFICATION.md` | `docs/` mirror of `MODEL_SPECIFICATION.md` |
| `docs/ROBLOX_STUDIO_IMPORT_GUIDE.md` | `docs/` mirror of `ROBLOX_STUDIO_IMPORT_GUIDE.md` |
| `docs/VALIDATION_REPORT.md` | `docs/` mirror of `VALIDATION_REPORT.md` |
| `docs/PORTAL_AND_PLAZA_CLEARANCE_REPORT.md` | `docs/` mirror of `PORTAL_AND_PLAZA_CLEARANCE_REPORT.md` |
| `MANIFEST.json` | Root machine-readable package manifest describing the 31 content files, byte sizes, SHA-256 digests, and measured metrics |
| `SHA256SUMS.txt` | Root `sha256sum -c` compatible checksum manifest covering all 32 package files (`31` content files + `MANIFEST.json`) |

---

## 3. Reproducible Generation Commands

To deterministically regenerate `.obj`, `.mtl`, `.glb`, and the palette atlas in standard Python 3:

```bash
python3 scripts/generate_hub_queue_pad_ring_blender.py --out_dir ./repro_exports
```

To run inside Blender 3.6+ / 4.x and also save an editable `.blend` file:

```bash
blender --background --python scripts/generate_hub_queue_pad_ring_blender.py -- --out_dir ./repro_exports
```
