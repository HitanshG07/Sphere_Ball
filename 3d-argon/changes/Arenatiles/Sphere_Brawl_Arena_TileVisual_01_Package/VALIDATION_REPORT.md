# VALIDATION REPORT — `SM_Arena_TileVisual_01` (Phase 2 Final Production Asset Package)

| Validation Metadata | Value |
| :--- | :--- |
| **Canonical Asset ID** | `SM_Arena_TileVisual_01` |
| **Package Directory** | `Sphere_Brawl_Arena_TileVisual_01_Package/` |
| **Outer ZIP Archive** | `Sphere_Brawl_Arena_TileVisual_01_Package.zip` |
| **Approved Concept Input** | `Sphere_Brawl_Arena_TileVisual_Concept_01.zip` (`SHA-256: fe40cd09419b86b915a896c90d37b3ea8978e0607bb4171c0a13bbc3b1b714d7` — **VERIFIED**) |
| **Automated Validator Script** | `scripts/validate_package.py` |
| **Overall Phase 2 Validation Verdict** | **PASS — ALL AUTOMATED GEOMETRY, BUDGET, EXPORT & ARCHIVE CHECKS PASSED** |

## 1. Automated Validation Check Summary (`PASS` / `FAIL` / `NOT RUN` / `NOT APPLICABLE`)

| Check Category | Test Method | Result & Measured Metrics | Status |
| :--- | :--- | :--- | :--- |
| **1. Approved Concept Input Hash** | `sha256sum Sphere_Brawl_Arena_TileVisual_Concept_01.zip` + `sha256sum -c SHA256SUMS.txt` | Exact match `fe40cd09419b86b915a896c90d37b3ea8978e0607bb4171c0a13bbc3b1b714d7`; all 14 concept files verified `OK` | **PASS** |
| **2. File & Export Existence** | `scripts/validate_package.py` directory enumeration | `2` base tile variants (`.obj`, `.mtl`, `.glb`) + `8` hazard overlays (`.obj`, `.mtl`, `.glb`) = `30` mesh files + `1` texture + `2` scripts + `10` PNG previews + `5` docs + `MANIFEST.json` + `SHA256SUMS.txt` = `50` files | **PASS** |
| **3. OBJ / MTL Path & Material Consistency** | `parse_obj()` + `parse_mtl()` in `validate_package.py` | All `mtllib` and `map_Kd` (`../textures/T_Arena_TilePalette_256.png` and `../../textures/T_Arena_TilePalette_256.png`) resolve cleanly on disk; 100% of `usemtl` names match `newmtl` definitions from the 10 approved palette materials | **PASS** |
| **4. GLB 2.0 Binary & Node Readability** | `parse_glb()` binary chunk & JSON parser in `validate_package.py` | All 10 `.glb` files have valid magic `0x46546C67`, version `2`, aligned `JSON` and `BIN` chunks, embedded `256×256` PNG texture, and named component nodes matching the `.obj` hierarchy 1:1 | **PASS** |
| **5. Variant A / Variant B Geometry Identity** | Vertex & face index equality check in `validate_package.py` | `456 / 456` vertex coordinates and `152 / 152` face indices are 100% identical between `SM_Arena_TileVisual_01_VariantA.obj` and `SM_Arena_TileVisual_01_VariantB.obj` | **PASS** |
| **6. Base Tile Local Bounds & Origin** | Vertex min/max audit in `validate_package.py` | Exact bounds `X in [-5.9000, +5.9000]`, `Y in [-1.0000, +1.0000]`, `Z in [-5.9000, +5.9000]` (`11.8000 × 2.0000 × 11.8000 studs`); origin `(0, 0, 0)` at geometric center; top face at `Local Y = +1.0000` | **PASS** |
| **7. Overlay Local Bounds & Top Offset** | Vertex min/max audit across all 8 overlays in `validate_package.py` | All 8 overlays span `X in [-5.7000, +5.7000]`, `Y in [+1.0000, +1.0500]`, `Z in [-5.7000, +5.7000]` (`11.4000 × 0.0500 × 11.4000 studs`), centered at `Local Y = +1.0250` (`World Y = 51.0250`) | **PASS** |
| **8. Base Tile Triangle Budget (`<= 170`)** | Face count audit in `validate_package.py` | **`152 triangles` (`456 vertices`)** per base tile (`18 triangles` below the `<= 170` Phase 2 target) | **PASS** |
| **9. Combined Per-Cell State Budgets (`<= 249`)** | Sum of Base (`152`) + Simultaneous Overlay (`32..72`) across all allowed states | All allowed states range from **`152` to `224` triangles** (worst-case `Base + OVL_Arena_Active_MagneticAnchor = 152 + 72 = 224 <= 249`) | **PASS** |
| **10. Normals, Winding, Degenerate & Coplanar Check** | Cross-product area & normal dot-product audit in `validate_package.py` | `0` degenerate faces (`area > 1e-8`), `0` normal mismatches (`dot(n_calc, n_file) > 0.99`), `0` cross-component coplanar overlaps across all 10 meshes | **PASS** |
| **11. Visual / Collision Separation & Groove Width** | Bounds vs. `12.0` pitch audit in `validate_package.py` | `12.0000 - 11.8000 = 0.2000 studs` visible groove; zero geometry protrudes beyond `±5.9000`; zero hidden collision parts in visual exports | **PASS** |
| **12. Texture Size & Material-Slot Check** | PIL image inspection of `textures/T_Arena_TilePalette_256.png` | `256 × 256 px` (`<= 1024 × 1024` limit), `933` bytes, `SHA-256: 3ab02901089d986685060313261da32d2f121c31979bb4b996dd41a3685f6e06` | **PASS** |
| **13. Deterministic Generator Execution** | Two consecutive runs of `scripts/generate_arena_tile_blender.py` | Repeated runs produce byte-identical `.obj`, `.mtl`, `.glb`, and `.png` outputs | **PASS** |
| **14. Editable `.blend` File Generation** | Check for `/usr/bin/blender` and `bpy` module in VM | Blender binary is not installed in the sandbox VM; `source/*.blend` is **`NOT GENERATED — BLENDER UNAVAILABLE`** | **NOT APPLICABLE / BLENDER UNAVAILABLE** |
| **15. Live Roblox Studio Import & Playtest** | Check for Roblox Studio in Linux sandbox VM | Headless Linux container has no Roblox Studio GUI; manual verification steps documented in `ROBLOX_STUDIO_IMPORT_GUIDE.md` | **NOT RUN** |

## 2. Measured Mesh-by-Mesh & Combined State Budget Table

| Mesh File | Role | Measured Triangles | Measured Vertices | Components | Local Bounds (`min` -> `max`) | Combined Cell Triangles (`Base + Overlay`) | Budget Verdict (`<= 249`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SM_Arena_TileVisual_01_VariantA` | Base Tile (Even Parity) | `152` | `456` | `5` | `[-5.9, -1.0, -5.9]` -> `[+5.9, +1.0, +5.9]` | **`152`** | **PASS (`<= 170` base & `<= 249` cell)** |
| `SM_Arena_TileVisual_01_VariantB` | Base Tile (Odd Parity) | `152` | `456` | `5` | `[-5.9, -1.0, -5.9]` -> `[+5.9, +1.0, +5.9]` | **`152`** | **PASS (`<= 170` base & `<= 249` cell)** |
| `OVL_Arena_Warn_Ice` | Ice Corridor Warning | `38` | `114` | `4` | `[-5.7, +1.0, -5.7]` -> `[+5.7, +1.05, +5.7]` | **`190`** (`152 + 38`) | **PASS (`59` tris under `249`)** |
| `OVL_Arena_Active_Ice` | Ice Corridor Active | `38` | `114` | `5` | `[-5.7, +1.0, -5.7]` -> `[+5.7, +1.05, +5.7]` | **`190`** (`152 + 38`) | **PASS (`59` tris under `249`)** |
| `OVL_Arena_Warn_Magnetic` | Magnetic Storm Warning | `56` | `168` | `4` | `[-5.7, +1.0, -5.7]` -> `[+5.7, +1.05, +5.7]` | **`208`** (`152 + 56`) | **PASS (`41` tris under `249`)** |
| `OVL_Arena_Active_MagneticAnchor` | Magnetic Storm Anchor | `72` | `216` | `7` | `[-5.7, +1.0, -5.7]` -> `[+5.7, +1.05, +5.7]` | **`224`** (`152 + 72`) | **PASS (`25` tris under `249`)** |
| `OVL_Arena_Active_MagneticField` | Magnetic Storm Field | `42` | `126` | `4` | `[-5.7, +1.0, -5.7]` -> `[+5.7, +1.05, +5.7]` | **`194`** (`152 + 42`) | **PASS (`55` tris under `249`)** |
| `OVL_Arena_Warn_Boost` | Boost Runway Warning | `34` | `102` | `4` | `[-5.7, +1.0, -5.7]` -> `[+5.7, +1.05, +5.7]` | **`186`** (`152 + 34`) | **PASS (`63` tris under `249`)** |
| `OVL_Arena_Active_Boost` | Boost Runway Active | `36` | `108` | `7` | `[-5.7, +1.0, -5.7]` -> `[+5.7, +1.05, +5.7]` | **`188`** (`152 + 36`) | **PASS (`61` tris under `249`)** |
| `OVL_Arena_Collapse_Warn` | Ring-Collapse Warning | `32` | `96` | `4` | `[-5.7, +1.0, -5.7]` -> `[+5.7, +1.05, +5.7]` | **`184`** (`152 + 32`) | **PASS (`65` tris under `249`)** |

## 3. On-Disk Payload Inventory (47 Non-Report Payload Files Verified)

| Relative Path | Byte Size | SHA-256 Digest |
| :--- | :--- | :--- |
| `INTEGRATION_REPORT.md` | `7,198` | `a30db4e583b98140fd6b875061b7d7272c13bd6cb72b7e5e3ae0ac8e6432e9ec` |
| `MODEL_SPECIFICATION.md` | `11,157` | `19e142e0a038ff6d4f5f677f020c026fd840caa7914fb305712131d4c7ba735b` |
| `README.md` | `11,776` | `f24029371cf45c93d353f5322d8542d72544d12b2875ce3d1e7143bdb93bd820` |
| `ROBLOX_STUDIO_IMPORT_GUIDE.md` | `9,546` | `13c1520eadd0b781fd8196652aa572b3d9a5bb0504cfb06c7ae30de613c4c9c1` |
| `meshes/SM_Arena_TileVisual_01_VariantA.glb` | `31,012` | `a8923466bb4f67db2cc23208384608076790780c3b7ecf6933d9510fd3909b65` |
| `meshes/SM_Arena_TileVisual_01_VariantA.mtl` | `887` | `e8acf4196214cb88f2b015b68bb8b62c9d5185ea272abf577b04e99848bf5e34` |
| `meshes/SM_Arena_TileVisual_01_VariantA.obj` | `31,522` | `10348eaea22096e32a909331fd93575833034f9d36cff4c7c09a5ec96d253b82` |
| `meshes/SM_Arena_TileVisual_01_VariantB.glb` | `31,012` | `8080f593c7605d015f16252e793e3ed9a3d8ba8ace81527caf312af79d99514b` |
| `meshes/SM_Arena_TileVisual_01_VariantB.mtl` | `887` | `ff1ac301b82f77b740e5d509893155f5efcb6e9e7602a7a2a79ca4cc74ead009` |
| `meshes/SM_Arena_TileVisual_01_VariantB.obj` | `31,523` | `f512f7b7de99cd6ea1f6f3b8df2a8ce6340e3bf813a4da371d8b40b6cdda87e6` |
| `meshes/overlays/OVL_Arena_Active_Boost.glb` | `14,876` | `c8404edaa64f61902536df74166bd66f5cd5d252b551f712a0d6541173ffc173` |
| `meshes/overlays/OVL_Arena_Active_Boost.mtl` | `890` | `f0b93e28c72f792d0ac09e25fc49be3ed65be273d3ad574d353eb93ec0f9651c` |
| `meshes/overlays/OVL_Arena_Active_Boost.obj` | `8,022` | `0df2fd1df841e72f4de14de9527370f08fd73b91067625f2a78d13dbaada7e65` |
| `meshes/overlays/OVL_Arena_Active_Ice.glb` | `13,232` | `98c5d191e044b6345c25a3344e76dc1d2bd8df0cfda2df82e53ebaae3a02a40d` |
| `meshes/overlays/OVL_Arena_Active_Ice.mtl` | `882` | `8e294ba3bb65f7c1144e38bbe78e432865b4efb94e7449c499465f370408c846` |
| `meshes/overlays/OVL_Arena_Active_Ice.obj` | `8,262` | `c75e7aab6f1fce1fdd7f6332e2835fac5674a7b57c2bdf7d0417ef890bfe7b9a` |
| `meshes/overlays/OVL_Arena_Active_MagneticAnchor.glb` | `20,324` | `810e55cd4653232144c5f2689b7ece1ef5cc9f71c31abda372ca4248ceb48f20` |
| `meshes/overlays/OVL_Arena_Active_MagneticAnchor.mtl` | `714` | `d0fc959eea9cf41228d7e4781dc34352551ee41ae6e928b8320767d07e5bc15c` |
| `meshes/overlays/OVL_Arena_Active_MagneticAnchor.obj` | `15,239` | `c559ec23a200c59d56e34f68498c49c7a5281033b297f22fe8ccdca33d999c49` |
| `meshes/overlays/OVL_Arena_Active_MagneticField.glb` | `12,468` | `6a50bb31bd54fa170383caadf5d98f481570e7fbc6a78b588edfeca27403e264` |
| `meshes/overlays/OVL_Arena_Active_MagneticField.mtl` | `521` | `b4c50af86df7e06deedc8690edba2fc21f93b221ab9abbf1a67805d7d2c587ec` |
| `meshes/overlays/OVL_Arena_Active_MagneticField.obj` | `8,989` | `95c8455b3ac72c7fdc68184791f3aada6faae27d4553ca33d894dbd667f40872` |
| `meshes/overlays/OVL_Arena_Collapse_Warn.glb` | `11,088` | `a13ab70b9c1142e5daba6473e4efcb73db12ea28cb8f1e04f1d153f3de1da8df` |
| `meshes/overlays/OVL_Arena_Collapse_Warn.mtl` | `707` | `81a86ed86942823b6decd09bbabee8e1ca0deaee64f5349648c8148d7044b561` |
| `meshes/overlays/OVL_Arena_Collapse_Warn.obj` | `6,980` | `acf2139b7201127d611f97f93944081ae638cc2559eeec28bca8a22055987776` |
| `meshes/overlays/OVL_Arena_Warn_Boost.glb` | `11,404` | `9fc962df873c95953425ab07a2158e25771dc91f1bfd9272758528af41af7d28` |
| `meshes/overlays/OVL_Arena_Warn_Boost.mtl` | `696` | `5d6cc4da8c445c60b06f573307f1e575f1cc96bca5abdbbc467d6f5298dfd57e` |
| `meshes/overlays/OVL_Arena_Warn_Boost.obj` | `7,382` | `10330ecbc5d1d33a030287222520b7b3a6b17aa5621297ded586c1c3a2ba84cf` |
| `meshes/overlays/OVL_Arena_Warn_Ice.glb` | `12,016` | `3dce625993ec6652a2c946220360ed1c1e16181e6eaeaa84f7e44901381a6d19` |
| `meshes/overlays/OVL_Arena_Warn_Ice.mtl` | `690` | `d4a9aed463f137da354cda10286c0c96e2352b1ccdb3a94265cbfb39024cda09` |
| `meshes/overlays/OVL_Arena_Warn_Ice.obj` | `8,160` | `133496be82723aa0528619285603eba622b99d76f7604c18de45171cae506511` |
| `meshes/overlays/OVL_Arena_Warn_Magnetic.glb` | `14,852` | `c240c59dce56efed7c53242b60ae4e70a6fa05ff82eae930d9d3e29beb4ff5ee` |
| `meshes/overlays/OVL_Arena_Warn_Magnetic.mtl` | `700` | `67f116a2d8f012523ea39c6d6b2996b06eb2650cf8708e822fb91a60a4a208a1` |
| `meshes/overlays/OVL_Arena_Warn_Magnetic.obj` | `11,784` | `2f12dbf50c97223629ec30af86177489d6786b329ad159de758a3131820bdb7c` |
| `previews/01_Production_Safe_Tile_ThreeQuarter.png` | `261,861` | `c0bb2ea708f38b567f364d802fbf4a413ea1c1fc26e143500242643025187001` |
| `previews/02_Production_Checkerboard_3x3_Patch.png` | `164,501` | `5f6035e11464e97c3fdfc10b87efc2c4d0fa7641a05ddd75fcd7d49a6263dbb2` |
| `previews/03_Production_Tile_Orthographic_Dimensions.png` | `196,937` | `ea39dcfa017f1545bdbf969459cd941936ec39762721d43122650be18f1c4c3c` |
| `previews/04_Production_SixState_Overview.png` | `176,308` | `656557cff4bbd1e99c0dd3b67cedc55fd078aec8fd09e0ce8a5fbbd8dfd2be86` |
| `previews/05_Production_IceCorridor_Warning_Active.png` | `193,044` | `424333e9909c4bdf1981f97aab127ad60f6b2cfcbc0f4ecd16ca50b56c044503` |
| `previews/06_Production_MagneticStorm_Warning_Active.png` | `205,589` | `3d3c0d561ab0f981610cfda25fad49346ddd2088d57dc515f194fbbc71af1482` |
| `previews/07_Production_BoostRunway_Warning_Active.png` | `183,512` | `36aac4383b116893a677a6988ee646e732adf608f6942746f2047406fb7ab170` |
| `previews/08_Production_RingCollapse_Warning_Sink.png` | `233,549` | `4c312c8af7538681698ddf4e9498444256048bc948850e5d18897f78d4b6605e` |
| `previews/09_Production_Arena_9x9_Overview.png` | `342,918` | `e377af3609b2672c6ead1aac8e41816bb7ce1fe3989798cfa1a501a9b42aa8a2` |
| `previews/10_Production_Component_And_Collision_Separation.png` | `299,618` | `4f9bad47692507b33b4aeacac3cc1eb93a6af8277c1a1cf17e7e4a05444e639a` |
| `scripts/generate_arena_tile_blender.py` | `42,681` | `8c78aed6e4050874b4ceef17ca3caa37ab98af8676aebb1331ecf5e6fbf1dd7a` |
| `scripts/validate_package.py` | `17,443` | `df672ecd6c629745b4998bc64cd2c5b98a17e498c57e7d1cc62af0e3e3738ba1` |
| `textures/T_Arena_TilePalette_256.png` | `933` | `3ab02901089d986685060313261da32d2f121c31979bb4b996dd41a3685f6e06` |
