# VALIDATION REPORT — `SM_ArenaEnvironment_Colosseum_01` (Phase 2 Production Kit)

| Validation Summary | Result |
| :--- | :--- |
| **Canonical Asset ID** | `SM_ArenaEnvironment_Colosseum_01` |
| **Approved Concept 02 Input Hash Check** | **`78a010a3d194f4c2b4577265c4628d8266e7bc7323efa32a5082bae4934b85d4` — PASS (Exact Match)** |
| **Automated Validator Script** | `scripts/validate_package.py` — **PASS (Exit Code `0`)** |
| **2-Run Deterministic Generator Repeatability** | **PASS (`100%` bit-for-bit identical SHA-256 across Run 1 and Run 2)** |
| **Per-MeshPart `< 20,000`-Triangle Hard Gate** | **PASS (`5/5` reusable archetypes `3,496..8,680` tris; `33/33` section MeshParts `1,668..16,832` tris)** |
| **OBJ / MTL / UV / Normal / Texture Audit** | **PASS (`100%` of `.obj` files have `v`, `vt`, `vn` & valid local `mtllib` + relative `map_Kd`)** |
| **Spatial Alignment & `Y < 15.0` Void Clearance** | **PASS (`0` vertices inside `98×104` inner ellipse; `Y_min = 18.06 > 15.0` void threshold)** |
| **Live Roblox Studio & Blender `.blend` Checks** | **`NOT RUN` (`/usr/bin/blender` and Roblox Studio are unavailable in the Linux VM sandbox)** |

---

## 1. Detailed Automated Validation Matrix (`scripts/validate_package.py`)

| Check Category | Evaluated Target | Measured Result | Gate Status |
| :--- | :--- | :--- | :--- |
| **1. Input Archive Integrity** | `Sphere_Brawl_Colosseum_Environment_Concept_02.zip` | `SHA-256 = 78a010a3d194f4c2b4577265c4628d8266e7bc7323efa32a5082bae4934b85d4` | **PASS** |
| **2. Texture Atlas Verification** | `textures/T_Colosseum_Production_Atlas_512.png` | `512 × 512 px` (`≤ 1024 × 1024` limit), `SHA-256 = 6bbec54b5e9b72dd...` | **PASS** |
| **3. Reusable Archetype Mesh Gate** | `meshes/archetypes/UMOD_01..UMOD_05.{obj,mtl,glb,fbx}` | `UMOD_01 = 6,018t`, `UMOD_02 = 5,982t`, `UMOD_03 = 6,712t`, `UMOD_04 = 8,680t`, `UMOD_05 = 3,496t` (`30,888` unique tris total; max `8,680 < 20,000`) | **PASS** |
| **4. Archetype Instance Accounting** | `12×UMOD_01 + 20×UMOD_02 + 8×UMOD_03 + 4×UMOD_04 + 1×UMOD_05` | `72,216 + 119,640 + 53,696 + 34,720 + 3,496 = 283,768` tris (`0` uncounted or duplicate tris) | **PASS** |
| **5. Section MeshPart `< 20k` Gate** | `meshes/sections/COL_*.{obj,mtl,glb}` (`33` sections) | All `33` sections between `1,668` and `16,832` tris; sum = `283,768` tris (`100% < 20,000` limit) | **PASS** |
| **6. Assembled Multi-Format Parity** | `meshes/SM_ArenaEnvironment_Colosseum_01.{obj,mtl,glb,gltf,bin,fbx}` | Identical `33` submesh nodes & `283,768` triangles (`851,304` vertices) across `.obj`, `.glb`, `.gltf`, and `.fbx` | **PASS** |
| **7. OBJ / MTL / UV / Normal Fix** | All `39` `.obj` and `39` `.mtl` files in package | Every `.obj` has `v`, `vt`, `vn` (`851,304` each in assembled `.obj`), valid same-folder `mtllib`, and valid relative `map_Kd` to `T_Colosseum_Production_Atlas_512.png` | **PASS** |
| **8. GLB / GLTF / FBX Material Parity** | `12` canonical PBR materials across all formats | All `12` materials (`MAT_TravertineLight` .. `EMI_Amber`) present with `POSITION`, `NORMAL`, `TEXCOORD_0`, and `COLOR_0` | **PASS** |
| **9. Geometry Hygiene & Normals** | Degenerate triangles & normal unit length | `0` degenerate (zero-area) triangles; `100%` outward unit normals | **PASS** |
| **10. World Bounds & Pivot** | Assembled vertex array (`851,304` vertices) | Pivot `(0,0,0)`; `X ∈ [-130.0917, +130.0917]`, `Y ∈ [18.0600, 125.0000]`, `Z ∈ [-136.0917, +136.0917]` | **PASS** |
| **11. Inner Elliptical Void & Grid Gap** | `(X / 98.0)^2 + (Z / 104.0)^2 >= 1.0` | `0` intruding vertices; `44.00` studs (`±X`), `50.00` studs (`±Z`), `24.50` studs (`45°`), `24.8145` studs 3D corner distance | **PASS** |
| **12. Canonical `Y < 15.0` Void Safety** | Lowest vertex elevation vs. `World Y < 15.0` | `Y_min = 18.0600` studs (`+3.0600` studs safely above `Y = 15.0`; older Concept 02 `Y < 10` typo corrected) | **PASS** |
| **13. Source Generator Repeatability** | 2 consecutive runs of `generate_colosseum_environment_blender.py` | `diff -u` on SHA-256 hashes of all exported `.obj`, `.mtl`, `.glb`, `.gltf`, `.bin`, `.fbx` files = `0` differences (`100%` bit-for-bit deterministic) | **PASS** |
| **14. Production Previews Audit** | `previews/01..11_*.png` (`11` sheets) | All `11` PNGs verified at `1920 × 1080` resolution; Previews `01..10` are clean shaded renders without wireframe overlay | **PASS** |

---

## 2. Two-Run Deterministic Generator Repeatability Evidence

Executing `python3 source/generate_colosseum_environment_blender.py` twice in succession produced identical byte sizes and SHA-256 digests across every output file:

| Generated Production Artifact | Deterministic SHA-256 Digest (Identical on Run 1 & Run 2) |
| :--- | :--- |
| `meshes/SM_ArenaEnvironment_Colosseum_01.obj` | `1c3a7e061676713c8e9714f01b612693d71cd6f5bc0ef2f3bc7fdad5ff1c093b` |
| `meshes/SM_ArenaEnvironment_Colosseum_01.mtl` | `6825337a592318bcf6f43126995e3b36ecba91b60b55b6c5c237e87d38fce36a` |
| `meshes/SM_ArenaEnvironment_Colosseum_01.glb` | `792a84d2689d52ed6d6332fb50c35ee6db5b0a34857752fdc8eba94f96c9df6d` |
| `meshes/SM_ArenaEnvironment_Colosseum_01.gltf` | `674ad92f19065209bb9fd483a61c8c498e66a6e1e56fbff98bd2a8f35a320b8b` |
| `meshes/SM_ArenaEnvironment_Colosseum_01.bin` | `00310352768507b3ee60baba12cf8acc7529b85ec8e95c625868b1f54d13ebe5` |
| `meshes/SM_ArenaEnvironment_Colosseum_01.fbx` | `3e842d6837c8a3dff3393a825bae10e2f1cc1951ffb6c5ab0bf3529ded16f0f9` |
| `textures/T_Colosseum_Production_Atlas_512.png` | `6bbec54b5e9b72dddf443ef33d2292420656309b7ec820ecc362199b8181ae0e` |

---

## 3. Unrun Checks Requiring Live Roblox Studio / Blender (`NOT RUN`)

- **Blender `.blend` File Generation**: **`NOT GENERATED — BLENDER UNAVAILABLE`** (`/usr/bin/blender` is not installed in the VM).
- **Live Roblox Studio Import, Material Appearance, and Playtest Checks (`STU-01`..`STU-05`)**: **`NOT RUN`** (Roblox Studio is unavailable in the Linux VM sandbox; complete manual verification steps are provided in `ROBLOX_STUDIO_IMPORT_GUIDE.md`).
