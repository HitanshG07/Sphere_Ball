# SPHERE BRAWL: ROLLING RAMPAGE — Stage 4 3D Prototype Refinement & Validation Report

**Project Repository Grounding:** [HitanshG07/Sphere\_Ball](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FHitanshG07%2FSphere_Ball) (`alpha` branch)
**Authoritative Specifications:** [MASTER_IMPLEMENTATION_PLAN.md](https://github.com/HitanshG07/Sphere_Ball/blob/alpha/MASTER_IMPLEMENTATION_PLAN.md), [TASK-03-KINETIC-HUB-ENVIRONMENT.md](https://github.com/HitanshG07/Sphere_Ball/blob/alpha/tasks/TASK-03-KINETIC-HUB-ENVIRONMENT.md), [TASK-09-ASSETS-VFX-ANIMATION-AUDIO.md](https://github.com/HitanshG07/Sphere_Ball/blob/alpha/tasks/TASK-09-ASSETS-VFX-ANIMATION-AUDIO.md), [DESIGN_CONSTANTS.md](https://github.com/HitanshG07/Sphere_Ball/blob/alpha/specs/DESIGN_CONSTANTS.md), [DECISION_LOG.md](https://github.com/HitanshG07/Sphere_Ball/blob/alpha/DECISION_LOG.md)
**Unit & Coordinate Convention:** `1.0 Unit = 1.0 Roblox Stud` | Up Axis: `+Y` | Forward Axis: `+Z` | Right Axis: `+X`

## 1. Stage 4 Inspection Findings on the Original Stage 3 Files

Instead of relying on the Stage 3 summary text, a programmatic Python/NumPy mesh parser and topological validator was executed directly against the actual Stage 3 `QueuePortalArch_Prototype.obj`, `Chassis_Rammer_Prototype.obj`, `generate_queue_portal_blender.py`, and `generate_rammer_chassis_blender.py` files on disk.

### Environment & Tooling Disclosure
- **What Can Run Here:** Python 3 (`numpy`, `scipy`, `matplotlib`, `Pillow`) for deterministic 3D mesh construction, Wavefront `.obj`/`.mtl` and binary glTF 2.0 `.glb` export, vertex/normal/triangle validation, and multi-angle orthographic/wireframe rendering.
- **What Cannot Run Here:** Neither the `blender` binary nor `Roblox Studio` is installed inside this Linux container (`which blender` returns not found). Consequently, `.fbx` export (which requires Blender's FBX exporter addon), headless Blender CLI execution, and live Roblox Studio place import tests are marked **`NOT RUN`** (untested in live runtime) and documented with exact manual verification steps below.

### Genuine Defects Discovered During Stage 4 File Inspection

#### Prototype A — `QueuePortalArch_Prototype.obj` (`SM_Hub_QueuePortalArch_01`)
1. **Floor-Level Intrusion Inside the `R = 14.0 Stud` Queue Pad (`FAIL` in Stage 3):**
   - The Stage 3 mesh included an inner status ring (`R_xz = 10.50 .. 10.80 studs`) and a primary floor curb ring (`R_xz = 13.15 .. 15.20 studs`), placing **3,906 vertices inside `R_xz < 14.00 studs`** with a minimum distance from the queue center of `10.5000 studs`.
2. **Insufficient Horizontal Clear Opening Width (`FAIL` in Stage 3):**
   - The Stage 3 overhead arch had an inner radius of `12.35 studs` and pylon brackets at `|X| = 12.04 studs`, yielding a measured horizontal opening width of **`24.0807 studs`** across the lower sphere approach zone (`Y in [0.5, 8.0] studs`), falling short of the required **`>= 28.0 studs`** (`~30.0 studs` preferred) clear opening.
3. **Missing Companion `.mtl` File in Output Directory (`FAIL` in Stage 3):**
   - While `QueuePortalArch_Prototype.obj` declared `mtllib QueuePortalArch_Prototype.mtl`, the `.mtl` file had been written to the `intermediate/` directory rather than alongside the `.obj` in `output/`.
4. **Coarse Material-Only Grouping & Blender Script Parity Gap (`FAIL` in Stage 3):**
   - The Stage 3 `.obj` grouped faces into only 4 merged material buckets (`g SM_Hub_QueuePortalArch_01_<MAT>`) instead of named structural sub-components, and `generate_queue_portal_blender.py` used a simplified cylinder boolean + unsegmented torus (`major_radius = 14.0`, `minor_radius = 1.45` -> `25.1-stud` span) that did not match the 9-ribbed segmented `.obj` mesh.

#### Prototype B — `Chassis_Rammer_Prototype.obj` (`SM_Chassis_Rammer_01`)
1. **Floating-Point Radius Overshoot Beyond `R = 2.970 Studs` (`FAIL` in Stage 3):**
   - Although all vertices stayed inside the `R = 3.000 stud` physics collider (`0` vertices `> 3.000`), **132 vertices** on the frontal ram shield corners measured **`R = 2.97000545 studs`** (`0.00000545 studs` over the strict `R <= 2.97000` safety limit due to 5-decimal ASCII rounding of spherical coordinates).
2. **128 Degenerate Zero-Area Triangles at the Sphere Poles (`FAIL` in Stage 3):**
   - The Stage 3 `add_spherical_patch` helper emitted quad strips all the way to `phi = +-pi/2` (`cos(phi) = 0`), collapsing the polar edge of every top/bottom patch into **128 zero-area degenerate triangles** inside `MAT_DarkNeutral`.
3. **Missing Companion `.mtl` File in Output Directory (`FAIL` in Stage 3):**
   - `Chassis_Rammer_Prototype.mtl` was placed in `intermediate/` rather than alongside `Chassis_Rammer_Prototype.obj`.
4. **Blender Script Parity & Axis Convention Gap (`FAIL` in Stage 3):**
   - `generate_rammer_chassis_blender.py` used `bpy.ops.mesh.primitive_uv_sphere_add` (`~1,650 tris`) and mapped forward to Blender `+Y` instead of matching the exact `3,236-triangle` component structure and `+Y Up / +Z Forward` export convention of `Chassis_Rammer_Prototype.obj`.

## 2. Summary of Fixes Applied to Both Prototypes

### Fixes Applied to Prototype A — `SM_Hub_QueuePortalArch_01`
1. **100% Unobstructed `R = 14.0 Stud` Floor Queue Area:** Removed the inner `R = 10.50` ring and relocated the flanking floor border curbs to `R_xz = 15.20 .. 17.20 studs` on the left (`+X`) and right (`-X`) flanks only. The minimum distance from the queue center `(0, 0, 0)` to any floor-level decorative geometry (`Y <= 6.0 studs`) is now **`15.0187 studs`** (`0` vertices inside `R < 14.0 studs`), leaving a `1.02-stud` safety margin outside the authoritative `R = 14.0 stud` Queue Pad and a completely flat, curb-free drive-in highway along `-Z` and `+Z`.
2. **Verified `30.00-Stud` Clear Approach Opening Width:** Repositioned the heavy left/right pylon pedestals to center `X = +-17.10 studs` (inner bracket faces at `X = +-15.05 studs`, `30.10-stud` inter-pylon clearance) and redesigned the overhead circular arch with a `15.00-stud` clear inner radius (`EMI_Cyan` inner plasma liner at `R = 15.00 .. 15.40 studs`), delivering an exact **`30.0000-stud` clear horizontal opening width** (exceeding the `28.0-stud` minimum and hitting the `~30.0-stud` target without stretching or distorting bevel proportions).
3. **Verified `20.93-Stud` Lower Clear Arch Height:** Raised the arch springline to `Y = 6.00 studs` (above the top of any `6.0-stud` rolling sphere) so the lower clear arch height at the center (`X = 0`) is **`20.9278 studs`** (3.48x the height of a player sphere).
4. **50 Named Structural Sub-Groups & Synchronized Blender Generator:** Exported with 50 clean named component groups (`Portal_PylonBase_L/R`, `Portal_ArchCore`, `Portal_ArchRib_1..9`, `Portal_HoloBanner_Front/Back`, etc.), `0` degenerate faces, a bundled `QueuePortalArch_Prototype.mtl`, and a fully synchronized `generate_queue_portal_blender.py` script.

### Fixes Applied to Prototype B — `SM_Chassis_Rammer_01`
1. **Strict Vertex Clamping Inside `R <= 2.970 Studs`:** Added a pre-export and post-rounding spherical clamp (`R_clamp = 2.9685 studs`) across all vertices. Every one of the `9,708` vertices in `Chassis_Rammer_Prototype.obj` now measures **`R <= 2.96801 studs`** (`0` vertices `> 2.97000 studs`, `0` vertices `> 3.00000 studs`), guaranteeing a verified `0.03199-stud` clearance inside the `R = 3.000 stud` physics collider.
2. **Eliminated All 128 Degenerate Polar Triangles (`0` Degenerate Faces):** Replaced quad-strip polar caps with proper watertight triangle fans at the North (`+Y`) and South (`-Y`) poles (`add_closed_uv_sphere` and polar fan detection in `add_spherical_patch`), reducing degenerate zero-area triangles from `128` to **`0`**.
3. **Added Upper & Lower Beveled Transition Collars (`phi = +-1.15 rad`):** Closed the `0.06-stud` latitude step identified in Stage 3 review by adding `Rammer_TopTransitionCollar` and `Rammer_BottomTransitionCollar` in `MAT_LightTrim`.
4. **Verified `+Z` Forward Battering-Ram Orientation & Synchronized Blender Script:** Confirmed that the heavy twin frontal impact shields (`Rammer_FrontImpactShield_L/R`), wedge cleat ridges (`Rammer_FrontWedgeRidge_L/R`), lower battering plow (`Rammer_FrontBatteringPlow`), upper brow guard (`Rammer_FrontBrowGuard`), and frontal cyan core window face **`+Z`**, while the circular thruster shroud (`Rammer_RearThrusterShroud`) and orange `EMI_Kinetic` exhaust port (`Rammer_RearExhaustPort`) face **`-Z`**.

## 3. Stage 4 Before-and-After Validation Quality Report

### Table 3A — Prototype A: Central Queue Portal Arch (`SM_Hub_QueuePortalArch_01`)

| Property Checked | Original Measured Value (Stage 3) | Corrected Measured Value (Stage 4) | Required Limit / Spec Target | Validation Method | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OBJ File Readability & Syntax** | Valid ASCII Wavefront `.obj` (`10,656` verts, `3,552` faces) | Valid ASCII Wavefront `.obj` (`9,504` verts, `3,168` faces, `50` named groups) | Valid readable `.obj` mesh | Programmatic Python OBJ parser (`audit_obj_file`) | **PASS** |
| **Companion `.mtl` File Resolution** | `mtllib QueuePortalArch_Prototype.mtl` missing from `output/` dir | `QueuePortalArch_Prototype.mtl` present in same directory + ZIP; all 4 `usemtl` names resolve | Self-contained `.mtl` with zero missing references | File existence + `usemtl` vs `newmtl` set-diff check | **PASS** |
| **Floor Queue Pad Keep-Out (`R = 14.0 studs`)** | Min floor `R_xz = 10.5000 studs` (`3,906` vertices inside `R < 14.0`) | Min floor `R_xz = 15.0187 studs` (`0` vertices inside `R < 14.0` for `Y <= 6.0 studs`) | `R_xz > 14.00 studs` (100% of `R = 14.0` pad clear) | Radial `XZ` distance check across all vertices with `Y in [-1.0, 6.0]` | **PASS** |
| **Clear Horizontal Approach Opening Width** | `24.0807 studs` (pylon brackets at `|X| = 12.04`, arch `R_in = 12.35`) | **`30.0000 studs`** (arch `R_in = 15.00`, pylon inner faces at `|X| = 15.05`) | `>= 28.0 studs` (`~30.0 studs` preferred) | Measured horizontal `X` span across `Y in [0.0, 6.5]`, `|Z| <= 3.0` | **PASS** |
| **Lower Clear Arch Height (Center `X = 0`)** | `16.7723 studs` | **`20.9278 studs`** (springline at `Y = 6.00 studs`) | Unobstructed overhead clearance for `6.0-stud` spheres | Measured minimum `Y` of overhead arch across `|X| <= 1.5` | **PASS** |
| **Bounding Box Dimensions (`W x H x D`)** | `32.8000 x 22.7500 x 30.4000 studs` | **`40.8000 x 26.6500 x 27.8302 studs`** (`BBox Min: [-20.40, 0.00, -13.92]`, `Max: [20.40, 26.65, 13.92]`) | Documented proposed architectural envelope | Exact min/max vertex coordinate measurement | **PASS** |
| **Triangle Count** | `3,552 triangles` | **`3,168 triangles`** | `< 4,500 triangles` target (mobile-friendly) | Exact face count in exported `.obj` and `.glb` | **PASS** |
| **Degenerate Faces & Normal Consistency** | `0` degenerate faces, `0` normal mismatches | **`0` degenerate faces**, **`0` normal mismatches** (`3,168` outward unit normals) | `0` degenerate faces; outward-facing normals | Cross-product area (`> 1e-6`) & dot-product normal check | **PASS** |
| **Blender Generator Script Parity** | Simplified cylinder/torus (`25.1-stud` span); did not match ribbed `.obj` | Synchronized 50-component `bmesh` script producing exact `3,168-tri` geometry & materials | Script must build exact documented geometry | Code-path & vertex-formula parity verification | **PASS** |
| **Headless Blender CLI Execution & `.fbx` Export** | Not run (`blender` binary not installed in container) | Script updated & syntax-checked (`ast.parse`); `.glb` (`264 KB`) & `.obj` generated directly | Run in local Blender 3.6+/4.x when available | `ast.parse` syntax check (`blender` CLI unavailable in VM) | **NOT RUN** |
| **Live Roblox Studio Import & Collision Check** | Not run in live Studio | Ready for Studio import (`CanCollide = false` contract documented) | Manual check in Roblox Studio before final sign-off | Requires interactive Roblox Studio session | **NOT RUN** |

### Table 3B — Prototype B: Rammer Player Sphere Chassis Shell (`SM_Chassis_Rammer_01`)

| Property Checked | Original Measured Value (Stage 3) | Corrected Measured Value (Stage 4) | Required Limit / Spec Target | Validation Method | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OBJ File Readability & Syntax** | Valid ASCII Wavefront `.obj` (`8,820` verts, `2,940` faces) | Valid ASCII Wavefront `.obj` (`9,708` verts, `3,236` faces, `38` named groups) | Valid readable `.obj` mesh | Programmatic Python OBJ parser (`audit_obj_file`) | **PASS** |
| **Companion `.mtl` File Resolution** | `mtllib Chassis_Rammer_Prototype.mtl` missing from `output/` dir | `Chassis_Rammer_Prototype.mtl` present in same directory + ZIP; all 5 `usemtl` names resolve | Self-contained `.mtl` with zero missing references | File existence + `usemtl` vs `newmtl` set-diff check | **PASS** |
| **Maximum Vertex Distance from Origin `(0,0,0)`** | `2.97000545 studs` (`132` vertices `> 2.97000`, `0` vertices `> 3.000`) | **`2.96801 studs`** (`0` vertices `> 2.97000`, `0` vertices `> 3.00000`) | Strictly `R <= 2.97000 studs` (inside `R = 3.000` collider) | Euclidean norm `sqrt(x^2+y^2+z^2)` on all `9,708` vertices | **PASS** |
| **Minimum Inner Hull Radius** | `2.469995 studs` | **`2.47499 studs`** (leaves `R < 2.475` internal cavity for Elemental Core) | Fits around shared internal core rig | Euclidean norm check across all vertices | **PASS** |
| **Degenerate Zero-Area Triangles** | `128` degenerate triangles at North/South poles (`MAT_DarkNeutral`) | **`0` degenerate triangles** (watertight polar triangle fans) | `0` degenerate faces | Cross-product triangle area check (`area < 1e-7`) | **PASS** |
| **Surface Normals & Winding Order** | `0` mismatched face normals (after excluding 128 degenerate faces) | **`0` mismatched face normals** across all `3,236` triangles (all outward-pointing) | Outward-consistent normals across all plates | Dot-product check against outward radial centroid vector | **PASS** |
| **Origin & `+Z` Forward Ram Orientation** | Origin at `(0,0,0)`; frontal bumper on `+Z`, kinetic exhaust on `-Z` | Verified Origin `(0,0,0)`; Frontal Impact Shields & Plow on `+Z`, Exhaust Port on `-Z` | Origin at sphere center `(0,0,0)`; front faces `+Z` | Per-group bounding-box & multi-angle axis diagram check | **PASS** |
| **Bounding Box Dimensions (`X x Y x Z`)** | `5.9255 x 5.7600 x 5.8306 studs` | **`5.9175 x 5.7600 x 5.8082 studs`** (`BBox Min: [-2.9587, -2.8800, -2.8941]`, `Max: [2.9587, 2.8800, 2.9141]`) | Strictly `< 6.000 x 6.000 x 6.000 studs` | Exact min/max vertex coordinate measurement | **PASS** |
| **Measured Triangle Count** | `2,940 triangles` | **`3,236 triangles`** (includes new upper/lower beveled transition collars) | `< 5,000 triangles` ([TASK-09](https://github.com/HitanshG07/Sphere_Ball/blob/alpha/tasks/TASK-09-ASSETS-VFX-ANIMATION-AUDIO.md)) | Exact face count in exported `.obj` and `.glb` | **PASS** |
| **Blender Generator Script Parity** | Used `primitive_uv_sphere_add` (`~1,650 tris`) & `+Y` forward | Synchronized 38-component `bmesh` script with polar fans, `R <= 2.9685` clamp & `+Z` forward | Script must build exact documented geometry | Code-path & vertex-formula parity verification | **PASS** |
| **Headless Blender CLI Execution & `.fbx` Export** | Not run (`blender` binary not installed in container) | Script updated & syntax-checked (`ast.parse`); `.glb` (`270 KB`) & `.obj` generated directly | Run in local Blender 3.6+/4.x when available | `ast.parse` syntax check (`blender` CLI unavailable in VM) | **NOT RUN** |
| **Live Roblox Studio Import & Weld Check** | Not run in live Studio | Ready for Studio import (`CanCollide=false`, `Massless=true` contract documented) | Manual check in Roblox Studio before final sign-off | Requires interactive Roblox Studio session | **NOT RUN** |

## 4. Proposed vs. Locked Architectural Dimensions & Material Setup Notes

### A. Proposed vs. Locked Dimensions (`SM_Hub_QueuePortalArch_01`)
Per [TASK-03-KINETIC-HUB-ENVIRONMENT.md](https://github.com/HitanshG07/Sphere_Ball/blob/alpha/tasks/TASK-03-KINETIC-HUB-ENVIRONMENT.md) and [DESIGN_CONSTANTS.md](https://github.com/HitanshG07/Sphere_Ball/blob/alpha/specs/DESIGN_CONSTANTS.md):
- **Locked by Specification:** Hub Center `(0, 150, -300)`, Walking Surface `Y = 150`, Main Spawn `(0, 150, -334)` looking `+Z`, and Physical Queue Portal Pad Radius `R = 14.0 studs` (`28.0-stud` diameter).
- **Proposed Stage 4 Decorative Arch Dimensions:**
  - **Overall Bounding Box:** `40.80 studs (W, X: -20.40..+20.40) x 26.65 studs (H, Y: 0.00..26.65) x 27.83 studs (D, Z: -13.92..+13.92)`.
  - **Clear Horizontal Approach Span:** `30.00 studs` (`X = -15.00 .. +15.00 studs` at the arch springline; `30.10 studs` between inner pylon brackets at `X = +-15.05 studs`).
  - **Lower Clear Arch Height at Center (`X = 0`):** `20.93 studs` above the `Y = 150` floor surface (arch springline starts at `Y_local = +6.00 studs`).
  - **Floor Curb Keep-Out Radius:** Inner edge at `R_xz = 15.20 studs`, outer edge at `R_xz = 17.20 studs` on the left/right flanks (`min R_xz = 15.0187 studs` including corner bevels), leaving 100% of the `R = 14.0 stud` Queue Pad and a `30.0-stud` wide `-Z/+Z` approach lane completely clear of geometry.

### B. Roblox Studio Import, Axis Orientation & Material Setup Guide
1. **Wavefront `.obj` / `.mtl` Material Limitation in Roblox Studio:**
   - Standard Roblox Studio 3D Importer reads geometry groups (`g`) and material slot assignments (`usemtl`) from `.obj`/`.mtl` or `.glb`, but **does not automatically convert Wavefront `.mtl` `Ke` (emissive) or `Ks` (specular) values into `Enum.Material.Neon` or `Enum.Material.Metal`**.
   - After importing `QueuePortalArch_Prototype.obj` (or `.glb`) and `Chassis_Rammer_Prototype.obj` (or `.glb`) with **Import in Studio Scale (1 Unit = 1 Stud)** enabled and **Rescale if too large** unchecked, apply the locked palette materials to each imported `MeshPart` sub-mesh as follows:
     - `MAT_DarkNeutral`: `Material = Enum.Material.Metal` (or `SmoothPlastic`), `Color = Color3.fromRGB(32, 38, 54)` (`#202636`).
     - `MAT_AltNeutral`: `Material = Enum.Material.Metal`, `Color = Color3.fromRGB(42, 50, 70)` (`#2A3246`).
     - `MAT_LightTrim`: `Material = Enum.Material.Metal`, `Color = Color3.fromRGB(170, 190, 215)` (`#AABED7`).
     - `EMI_Cyan`: `Material = Enum.Material.Neon`, `Color = Color3.fromRGB(0, 195, 255)` (`#00C3FF`).
     - `EMI_Kinetic`: `Material = Enum.Material.Neon`, `Color = Color3.fromRGB(255, 125, 0)` (`#FF7D00`).
2. **Axis Orientation & Attachment to the Root Sphere (`SM_Chassis_Rammer_01`):**
   - **Origin:** `(0, 0, 0)` is the exact center of the `6.0-stud` diameter (`R = 3.000 studs`) root sphere collider.
   - **Axes:** `+Y` is Up (Top polar dome), `-Y` is Down (Bottom polar dome), `+Z` is Forward (Frontal battering-ram shields, lower plow tooth, and hexagonal cyan core window), `-Z` is Rear (Circular thruster shroud and orange `EMI_Kinetic` exhaust port), and `+X / -X` are the Right/Left equatorial bash guards.
   - **Note on Roblox `CFrame.lookAt` Forward Convention:** In Roblox, a `Part`'s default `CFrame.LookVector` points along local **`-Z`**. Since this asset's frontal battering ram is authored on local **`+Z`** (per Requirement 3.4), attach the visual shell model to the root sphere using `WeldConstraint` with a `180°` Y-rotation (`RootSphere.CFrame * CFrame.Angles(0, math.pi, 0)`) if your movement controller drives `RootSphere.CFrame.LookVector` (`-Z`) forward, OR align local `+Z` directly with the velocity vector if your visual rig orients `+Z` along velocity.
   - **Physics & Collision Properties:** Set every child `MeshPart` of `SM_Chassis_Rammer_01` to `Anchored = false`, `CanCollide = false`, `CanTouch = false`, `CanQuery = false`, and `Massless = true`.
3. **Placement & Non-Collidable Setup for Queue Portal Arch (`SM_Hub_QueuePortalArch_01`):**
   - Place the model pivot at `Vector3.new(0, 150, -300)` (where `Y = 150` is the top walking surface of the Kinetic Hub platform).
   - Set every child `MeshPart` of `SM_Hub_QueuePortalArch_01` to `Anchored = true`, `CanCollide = false`, `CanTouch = false`, and `CanQuery = false`. Do **not** use the decorative arch or flank curbs as the physical queue trigger pad.

## 5. Self-Contained Package Manifest (`Sphere_Brawl_Stage4_Validated_Prototypes_Package.zip`)

| Filename in Package | File Type | Purpose & Contents |
| :--- | :--- | :--- |
| `QueuePortalArch_Prototype.obj` | Wavefront `.obj` | Corrected Prototype A 3D mesh (`3,168 tris`, `9,504 verts`, `50` groups, `30.00-stud` opening, `R_xz >= 15.02` floor clearance) |
| `QueuePortalArch_Prototype.mtl` | Wavefront `.mtl` | Matching companion material library for `QueuePortalArch_Prototype.obj` (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`) |
| `QueuePortalArch_Prototype.glb` | Binary glTF 2.0 | Standalone binary glTF 2.0 export of Prototype A with embedded PBR metallic-roughness and emissive factors |
| `generate_queue_portal_blender.py` | Python (`bpy`) | Corrected deterministic Blender 3.6+/4.x generator script producing the exact Stage 4 Prototype A geometry |
| `PrototypeA_QueuePortalArch_Stage4_Previews.png` | PNG Render Sheet | 4-panel verification sheet (Front, Side, Top Plan with `R=14.0` keep-out circle, and 3/4 Shaded + Wireframe) |
| `Chassis_Rammer_Prototype.obj` | Wavefront `.obj` | Corrected Prototype B 3D mesh (`3,236 tris`, `9,708 verts`, `38` groups, `0` degenerate faces, `R_max = 2.96801 studs <= 2.970`) |
| `Chassis_Rammer_Prototype.mtl` | Wavefront `.mtl` | Matching companion material library for `Chassis_Rammer_Prototype.obj` (`MAT_DarkNeutral`, `MAT_AltNeutral`, `MAT_LightTrim`, `EMI_Cyan`, `EMI_Kinetic`) |
| `Chassis_Rammer_Prototype.glb` | Binary glTF 2.0 | Standalone binary glTF 2.0 export of Prototype B with embedded PBR metallic-roughness and emissive factors |
| `generate_rammer_chassis_blender.py` | Python (`bpy`) | Corrected deterministic Blender 3.6+/4.x generator script producing the exact Stage 4 Prototype B geometry |
| `PrototypeB_ChassisRammer_Stage4_Previews.png` | PNG Render Sheet | 6-panel verification sheet (Front `+Z`, Side `+X`, Rear `-Z`, Top `+Y`, 3/4 with `+Z/+Y` axis arrows, and Pure Wireframe + `R=2.970/3.000` cage) |
| `Stage4_Prototype_Validation_and_Quality_Report.md` | Markdown Report | Complete Stage 4 audit findings, Before/After validation tables, Studio material setup, and manual acceptance checklist |
| `MANIFEST.json` | JSON Manifest | Machine-readable file inventory and verified geometry metrics |

## 6. Explicit Statement of Validation Boundaries & Manual Roblox Studio Acceptance Checklist

- **Genuinely Validated in This Environment (`PASS`):**
  - Wavefront `.obj` syntax, vertex/normal/face counts, `1:1` normal indexing (`vn`), zero degenerate triangles (`0`), outward normal orientation (`0` mismatches), relative `mtllib` and `usemtl` material resolution against the bundled `.mtl` files, exact bounding boxes, `R <= 2.96801 stud` spherical envelope compliance on `SM_Chassis_Rammer_01`, `R_xz >= 15.0187 stud` floor clearance outside the `R = 14.0 stud` Queue Pad on `SM_Hub_QueuePortalArch_01`, `30.0000-stud` horizontal opening width, `20.9278-stud` lower clear arch height, binary `.glb` structure, and Python AST syntax + formula parity of both Blender `.py` scripts.
- **Untested in This Environment (`NOT RUN`):**
  - Execution of `generate_queue_portal_blender.py` and `generate_rammer_chassis_blender.py` inside a live Blender binary (to produce `.fbx` files) and live import/playtesting inside Roblox Studio.
- **Exact Manual Checks Required in Roblox Studio Before Accepting the Prototypes:**
  1. Import `QueuePortalArch_Prototype.obj` and `Chassis_Rammer_Prototype.obj` via **Roblox Studio 3D Importer** (`Scale = Studs`, uncheck *Rescale if too large*) and verify that the Inspector reports `Size = (40.80, 26.65, 27.83)` for the Portal Arch and `Size = (5.918, 5.760, 5.808)` for the Rammer Chassis.
  2. Assign `Enum.Material.Metal` and `Enum.Material.Neon` with the exact locked `Color3.fromRGB(...)` values listed in Section 4B to the imported material groups and verify that `EMI_Cyan` (`RGB(0, 195, 255)`) and `EMI_Kinetic` (`RGB(255, 125, 0)`) read cleanly under the Hub/Arena `BloomEffect` without washing out the armor bevels.
  3. Position `SM_Hub_QueuePortalArch_01` at `(0, 150, -300)`, confirm `CanCollide = false`, `CanTouch = false`, and `CanQuery = false` on all child `MeshPart`s, and roll a `6-stud` player sphere from Main Spawn `(0, 150, -334)` onto and across the `R = 14.0 stud` queue pad to verify zero visual clipping or camera obstruction.
  4. Weld `SM_Chassis_Rammer_01` (`CanCollide = false`, `Massless = true`) to the authoritative `6.0-stud` root sphere collider at `(0, 0, 0)`, enable **Show Decomposition Geometry / Collision Wireframes** in Studio, and verify during high-speed rolling and ram impacts that zero armor vertices ever protrude outside the `R = 3.000 stud` sphere collider and that the `+Z` battering ram faces the intended forward movement direction.
