# Sphere Brawl: Rolling Rampage — Main Kinetic Hub Platform (`SM_Hub_PlazaPlatform_01`)

**Package Path:** `3d-argon/changes/3/Sphere_Brawl_Hub_Platform_01_Package/`  
**Asset ID:** `SM_Hub_PlazaPlatform_01`  
**Asset Type:** Static Environmental Platform / Floating Kinetic Hub Plaza  
**Authoritative References:** `tasks/TASK-03-KINETIC-HUB-ENVIRONMENT.md`, `MASTER_IMPLEMENTATION_PLAN.md` (§2.1–§2.4, §11.1, §11.3), `specs/DESIGN_CONSTANTS.md`, `3d-argon/sphere_brawl_master_3d_art_bible_and_technical_handoff.md`

## 1. Production Summary

This package delivers the complete, deterministic, production-ready 3D asset for **`SM_Hub_PlazaPlatform_01`**, the 140-stud floating Kinetic Hub platform defined by **TASK-03** and **Master Implementation Plan §2.4**.

- **Exact Locked Outer Diameter & Footprint:** `140.0000 studs` outer diameter (`R_outer = 70.0000 studs`), `140.0000 × 140.0000 studs` maximum XZ footprint (`X in [-70.0000, +70.0000]`, `Z in [-70.0000, +70.0000]`). Zero trim, bevels, undercuts, or brackets extend beyond `R = 70.0000 studs`.
- **Pivot & Top Walking Surface Alignment:** Local model origin `(0.0000, 0.0000, 0.0000)` is placed at the exact geometric center of the top walking surface (`Local Y = 0.0000`). All structural thickness extends into negative local Y (`Local Y in [-12.0000, 0.0000]`), so placing the model pivot at **`(0, 150, -300)`** places the walkable top deck at **`World Y = 150.0000`** with zero offset compensation.
- **Queue Portal Clearance Verified:** Inspected against `3d-argon/changes/1/argon/Sphere_Brawl_Stage4_Validated_Prototypes/QueuePortalArch_Prototype.obj`. The entire central queue pad (`R <= 14.0000 studs`) and portal pylon envelope (`R <= 20.4658 studs`) sit on a 100% flat, continuous `Local Y = 0.0000` surface with zero duplicated portal rings and zero raised obstructions (`0` vertices with `Y > 0.0000`). The platform's recessed inner framing conduit sits at `R in [21.2000, 23.0000] studs` (`0.7342 studs` radial clearance outside the outermost portal pylon buttress).
- **Multi-Node & Multi-Object Material Separation:** Exported `.glb` and `.obj` files preserve 7 named child components (`GEO_PlazaPlatform_Deck`, `GEO_PlazaPlatform_DeckInlays`, `GEO_PlazaPlatform_Rim`, `GEO_PlazaPlatform_Structure`, `GEO_PlazaPlatform_Underside`, `GEO_PlazaPlatform_Trim`, `GEO_PlazaPlatform_CyanAccents`) mapped to the 4 locked Hub materials (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`), with baked `COLOR_0` vertex colors, `TEXCOORD_0` UVs, and an embedded 64×64 PNG palette atlas (`SphereBrawl_HubPlatform_PaletteAtlas.png`).
- **Measured Geometry Budget:** `2,688 triangles` (`8,064 export vertices`), well within the proposed `<= 6,000 triangle` target, with `0` degenerate faces and `0` inverted normals.

## 2. Package Contents

| Relative Path | Description |
|---|---|
| `meshes/SM_Hub_PlazaPlatform_01.obj` | Wavefront OBJ export (`2,688 triangles`, 7 `o GEO_PlazaPlatform_*` objects, UVs, vertex colors) |
| `meshes/SM_Hub_PlazaPlatform_01.mtl` | Wavefront MTL material library (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`) |
| `meshes/SM_Hub_PlazaPlatform_01.glb` | Binary glTF 2.0 export (7 child mesh nodes under root `SM_Hub_PlazaPlatform_01`, `COLOR_0`, `TEXCOORD_0`, embedded PNG atlas) |
| `meshes/collision_proxy/COL_PlazaPlatform_Deck.obj` | Optional simplified 32-sided top-deck collision proxy (`128 triangles`, `R = 70.0`, `Y in [-2.0, 0.0]`) |
| `meshes/collision_proxy/COL_PlazaPlatform_Deck.mtl` | Companion MTL for optional collision proxy |
| `meshes/collision_proxy/COL_PlazaPlatform_Deck.glb` | Companion GLB for optional collision proxy |
| `textures/SphereBrawl_HubPlatform_PaletteAtlas.png` | 64×64 2×2 sRGB palette swatch texture used by `.glb` and `.obj`/`.mtl` |
| `scripts/generate_hub_plaza_platform_blender.py` | Deterministic procedural generator (runs in standard Python 3 AND inside Blender 3.6+/4.x `bpy`/`bmesh`) |
| `config/hub_plaza_platform_parameters.json` | Machine-readable dimensional, material, and component parameters |
| `previews/01_Preview_ThreeQuarter_Perspective.png` | Required Preview 1: Three-quarter perspective views (elevated, horizon, tactical) |
| `previews/02_Preview_Top_140Stud_Layout.png` | Required Preview 2: Top orthographic view & TASK-03 station/portal clearance overlay |
| `previews/03_Preview_Side_and_Underside_Structure.png` | Required Preview 3: Side orthographic elevation & underside structural truss views |
| `previews/04_Preview_Material_and_Rim_CloseUp.png` | Required Preview 4: Close-up renders of outer rim bevels, inner portal framing ring, and underside girders |
| `previews/05_Preview_NeutralClay_and_Wireframe.png` | Required Preview 5: Neutral studio clay renders and technical wireframe views |
| `docs/README.md` | Package overview and directory guide (also mirrored at package root `README.md`) |
| `docs/MODEL_SPECIFICATION.md` | Detailed architectural, dimensional, pivot, and material specification (mirrored at root) |
| `docs/ROBLOX_STUDIO_IMPORT_GUIDE.md` | Step-by-step Roblox Studio 3D Importer, pivot, material, and collision setup guide (mirrored at root) |
| `docs/VALIDATION_REPORT.md` | Full 18-check validation report with explicit `PASS` / `NOT RUN` / `REQUIRES OWNER REVIEW` statuses (mirrored at root) |
| `manifest/SM_Hub_PlazaPlatform_01.manifest.json` | Canonical asset-manifest entry conforming to `specs/ASSET_MANIFEST.schema.json` |
| `MANIFEST.json` | Complete package file inventory with byte sizes, triangle counts, and SHA-256 digests |
| `SHA256SUMS.txt` | Standard `sha256sum -c` compatible checksum manifest for all package files |

## 3. Reproducible Generation Command

To deterministically regenerate the `.obj`, `.mtl`, `.glb`, and optional collision proxy in standard Python 3:

```bash
python3 scripts/generate_hub_plaza_platform_blender.py --out_dir ./repro_exports
```

To generate inside Blender 3.6+ / 4.x and also save an editable `.blend` file:

```bash
blender --background --python scripts/generate_hub_plaza_platform_blender.py -- --out_dir ./repro_exports
```
