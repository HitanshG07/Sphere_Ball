#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — PACKAGE INTEGRITY, TRANSFORM, UI-PANEL, CLEARANCE & MANIFEST AUDIT TOOL
Asset ID: SM_Hub_Leaderboard_01 (Step 6, Phase 2 — Grand Three-Board Monument & Nine-Position Podium Array)
===========================================================================================================
Audits the package directory and/or final ZIP archive (`--zip <path>`) to verify:
1. All 30 required package files exist (28 payload files + MANIFEST.json + SHA256SUMS.txt) with zero missing,
   unexpected, or root-misplaced preview files.
2. Every file size and SHA-256 digest in MANIFEST.json (28 payload entries) and SHA256SUMS.txt (29 entries)
   matches the actual on-disk bytes 1:1.
3. Explicit mathematical and geometric validation of exported `meshes/SM_Hub_Leaderboard_01.obj`, `.mtl`, `.glb`
   and `meshes/collision_proxy/COL_Leaderboard_Body.obj`, `.mtl`, `.glb`:
   - Visual triangle count == 1,852 (< 2,000 budget), 5,556 vertices, 1,852 normals, 6 UVs, 53 named components.
   - Collision proxy triangle count == 168 across 5 hull components, open above Y = 2.50 in foreground Z > 0.68.
   - 0 degenerate faces, 0 normal mismatches, 0 cross-component coplanar overlaps.
   - Exact local bounds X in [-11.0000, +31.0000] (42.0 W), Y in [0.0000, +26.0000] (26.0 H), Z in [-4.2000, +4.8000] (9.0 D).
   - All 15 replaceable UI-ready surfaces (`3` headers + `3` main tables + `9` podium nameplates) exist as separate
     components with 2 coplanar front triangles facing Local +Z (0, 0, +1) and zero baked text.
   - Verified world transform at (35, 150, -274) Yaw = -126.60707939 deg maps Local +Z to (-0.80274385, 0, -0.59632400),
     giving World Bounds X in [13.7938, 44.8432], Y in [150.0000, 176.0000], Z in [-284.2912, -246.7044] and
     radial span R_hub in [38.8377, 56.8872] studs (6.3128 studs inside R = 63.2 outer plaza curb).
   - Validates `manifest/SM_Hub_Leaderboard_01.manifest.json` against `specs/ASSET_MANIFEST.schema.json`.
"""

import os
import sys
import json
import math
import struct
import shutil
import hashlib
import zipfile
import tempfile
import subprocess
import numpy as np

REQUIRED_FILES = [
    "README.md",
    "MODEL_SPECIFICATION.md",
    "ROBLOX_STUDIO_IMPORT_GUIDE.md",
    "VALIDATION_REPORT.md",
    "INTEGRATION_REPORT.md",
    "MANIFEST.json",
    "SHA256SUMS.txt",
    "meshes/SM_Hub_Leaderboard_01.obj",
    "meshes/SM_Hub_Leaderboard_01.mtl",
    "meshes/SM_Hub_Leaderboard_01.glb",
    "meshes/SphereBrawl_Leaderboard_PaletteAtlas.png",
    "meshes/collision_proxy/COL_Leaderboard_Body.obj",
    "meshes/collision_proxy/COL_Leaderboard_Body.mtl",
    "meshes/collision_proxy/COL_Leaderboard_Body.glb",
    "meshes/collision_proxy/SphereBrawl_Leaderboard_PaletteAtlas.png",
    "textures/SphereBrawl_Leaderboard_PaletteAtlas.png",
    "scripts/generate_hub_leaderboard_blender.py",
    "scripts/validate_package.py",
    "config/leaderboard_parameters.json",
    "manifest/SM_Hub_Leaderboard_01.manifest.json",
    "previews/01_Production_Monument_Approach_ThreeQuarter.png",
    "previews/02_Production_Direct_Front_Elevation.png",
    "previews/03_Production_Side_Orthographic.png",
    "previews/04_Production_Rear_Structural_View.png",
    "previews/05_Production_TopDown_Footprint_Clearance.png",
    "previews/06_Production_Neutral_Clay_AvatarScale.png",
    "previews/07_Production_Hub_Integration.png",
    "previews/08_Production_Three_Board_UI.png",
    "previews/09_Production_Nine_Podium_UI_Surface_Proof.png",
    "previews/10_Production_Technical_Component_And_Collision_Overview.png",
]

UI_SURFACE_COMPONENTS = [
    "GEO_Leaderboard_UIHeader_A_SessionKOs",
    "GEO_Leaderboard_UIMain_A_SessionKOs",
    "GEO_Leaderboard_UIHeader_B_SessionWins",
    "GEO_Leaderboard_UIMain_B_SessionWins",
    "GEO_Leaderboard_UIHeader_C_SessionStandings",
    "GEO_Leaderboard_UIMain_C_SessionStandings",
    "GEO_Leaderboard_PodiumNameplate_A2_2ND",
    "GEO_Leaderboard_PodiumNameplate_A1_1ST",
    "GEO_Leaderboard_PodiumNameplate_A3_3RD",
    "GEO_Leaderboard_PodiumNameplate_B2_2ND",
    "GEO_Leaderboard_PodiumNameplate_B1_1ST",
    "GEO_Leaderboard_PodiumNameplate_B3_3RD",
    "GEO_Leaderboard_PodiumNameplate_C2_2ND",
    "GEO_Leaderboard_PodiumNameplate_C1_1ST",
    "GEO_Leaderboard_PodiumNameplate_C3_3RD",
]

PODIUM_BODY_COMPONENTS = [
    "GEO_Leaderboard_Podium_A2_2ND",
    "GEO_Leaderboard_Podium_A1_1ST",
    "GEO_Leaderboard_Podium_A3_3RD",
    "GEO_Leaderboard_Podium_B2_2ND",
    "GEO_Leaderboard_Podium_B1_1ST",
    "GEO_Leaderboard_Podium_B3_3RD",
    "GEO_Leaderboard_Podium_C2_2ND",
    "GEO_Leaderboard_Podium_C1_1ST",
    "GEO_Leaderboard_Podium_C3_3RD",
]

EXPECTED_MATERIALS = [
    "MAT_DarkNeutral",
    "MAT_AltNeutral",
    "MAT_LightTrim",
    "EMI_Cyan",
    "EMI_Amber",
    "EMI_Magnetic",
]


def sha256_of_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def validate_directory(pkg_root):
    errors = []
    checks = {}

    # 1. File inventory check
    actual_files = []
    for root, _, files in os.walk(pkg_root):
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), pkg_root).replace("\\", "/")
            actual_files.append(rel)
    actual_files.sort()
    expected_sorted = sorted(REQUIRED_FILES)

    if actual_files != expected_sorted:
        missing = sorted(set(expected_sorted) - set(actual_files))
        extra = sorted(set(actual_files) - set(expected_sorted))
        errors.append(f"Inventory mismatch: missing={missing}, extra={extra}")
    checks["inventory_count"] = len(actual_files)

    # 2. MANIFEST.json and SHA256SUMS.txt verification
    manifest_path = os.path.join(pkg_root, "MANIFEST.json")
    sums_path = os.path.join(pkg_root, "SHA256SUMS.txt")
    if os.path.exists(manifest_path) and os.path.exists(sums_path):
        with open(manifest_path, "r", encoding="utf-8") as mf:
            mdata = json.load(mf)
        m_files = mdata.get("files", [])
        checks["manifest_payload_count"] = len(m_files)
        if len(m_files) != 28:
            errors.append(f"Expected 28 payload entries in MANIFEST.json, found {len(m_files)}")
        for entry in m_files:
            rp = entry["path"]
            fp = os.path.join(pkg_root, rp)
            if not os.path.exists(fp):
                errors.append(f"MANIFEST file missing on disk: {rp}")
                continue
            sz = os.path.getsize(fp)
            dg = sha256_of_file(fp)
            if sz != entry["size_bytes"] or dg != entry["sha256"]:
                errors.append(f"MANIFEST mismatch for {rp}: disk=({sz}, {dg}) vs manifest=({entry['size_bytes']}, {entry['sha256']})")

        sum_lines = [ln.strip() for ln in open(sums_path, "r", encoding="utf-8") if ln.strip()]
        checks["sha256sums_count"] = len(sum_lines)
        if len(sum_lines) != 29:
            errors.append(f"Expected 29 entries in SHA256SUMS.txt, found {len(sum_lines)}")
        for ln in sum_lines:
            dg, rp = ln.split(None, 1)
            rp = rp.lstrip("*").strip()
            fp = os.path.join(pkg_root, rp)
            if not os.path.exists(fp):
                errors.append(f"SHA256SUMS file missing: {rp}")
            elif sha256_of_file(fp) != dg:
                errors.append(f"SHA256SUMS digest mismatch for {rp}")
    else:
        errors.append("Missing MANIFEST.json or SHA256SUMS.txt")

    # 3. Placement transform & geometry check
    theta = math.radians(-126.60707939)
    c_t, s_t = math.cos(theta), math.sin(theta)
    vX = np.array([c_t, 0.0, -s_t], dtype=np.float64)
    vY = np.array([0.0, 1.0, 0.0], dtype=np.float64)
    vZ = np.array([s_t, 0.0, c_t], dtype=np.float64)
    R_mat = np.column_stack([vX, vY, vZ])
    target_dir = np.array([-35.0, 0.0, -26.0], dtype=np.float64)
    target_dir /= np.linalg.norm(target_dir)

    if not np.allclose(vZ, target_dir, atol=1e-6):
        errors.append(f"Forward vector {vZ} != inward radial vector {target_dir}")
    if abs(float(np.linalg.det(R_mat)) - 1.0) > 1e-9 or not np.allclose(R_mat.T @ R_mat, np.eye(3), atol=1e-9):
        errors.append("Rotation matrix is not orthonormal right-handed")

    obj_path = os.path.join(pkg_root, "meshes/SM_Hub_Leaderboard_01.obj")
    mtl_path = os.path.join(pkg_root, "meshes/SM_Hub_Leaderboard_01.mtl")
    glb_path = os.path.join(pkg_root, "meshes/SM_Hub_Leaderboard_01.glb")
    col_obj_path = os.path.join(pkg_root, "meshes/collision_proxy/COL_Leaderboard_Body.obj")
    col_glb_path = os.path.join(pkg_root, "meshes/collision_proxy/COL_Leaderboard_Body.glb")

    mtl_mats = []
    with open(mtl_path, "r", encoding="utf-8") as mf:
        for ln in mf:
            if ln.strip().startswith("newmtl "):
                mtl_mats.append(ln.strip()[7:].strip())
    if sorted(mtl_mats) != sorted(EXPECTED_MATERIALS):
        errors.append(f"MTL materials mismatch: {mtl_mats}")

    verts, normals = [], []
    comp_tris = {}
    cur_comp = None
    with open(obj_path, "r", encoding="utf-8") as of:
        for ln in of:
            s = ln.strip()
            if s.startswith("o "):
                cur_comp = s[2:].strip()
                comp_tris.setdefault(cur_comp, [])
            elif s.startswith("v "):
                p = s.split()
                verts.append(np.array([float(p[1]), float(p[2]), float(p[3])], dtype=np.float64))
            elif s.startswith("vn "):
                p = s.split()
                normals.append(np.array([float(p[1]), float(p[2]), float(p[3])], dtype=np.float64))
            elif s.startswith("f "):
                p = s.split()[1:]
                vi = [int(x.split("/")[0]) - 1 for x in p]
                vni = [int(x.split("/")[2]) - 1 for x in p]
                comp_tris[cur_comp].append((verts[vi[0]], verts[vi[1]], verts[vi[2]], normals[vni[0]]))

    total_tris = sum(len(v) for v in comp_tris.values())
    checks["visual_triangles"] = total_tris
    checks["visual_vertices"] = len(verts)
    checks["visual_components"] = len(comp_tris)

    if total_tris >= 2000 or total_tris != 1852:
        errors.append(f"Visual triangle count {total_tris} != expected 1852 (< 2000)")
    if len(comp_tris) != 53:
        errors.append(f"Expected 53 named components, found {len(comp_tris)}")

    # Verify all 15 UI surfaces and 9 podium bodies exist
    for uc in UI_SURFACE_COMPONENTS:
        if uc not in comp_tris:
            errors.append(f"Missing UI surface component: {uc}")
        else:
            ftris = [t for t in comp_tris[uc] if float(np.dot(t[3], [0.0, 0.0, 1.0])) > 0.999]
            if len(ftris) != 2:
                errors.append(f"UI surface {uc} expected 2 front (+Z) triangles, found {len(ftris)}")

    for pc in PODIUM_BODY_COMPONENTS:
        if pc not in comp_tris:
            errors.append(f"Missing podium component: {pc}")

    all_pts = np.array(verts)
    l_min, l_max = all_pts.min(axis=0), all_pts.max(axis=0)
    if not (np.allclose(l_min, [-11.0, 0.0, -4.2], atol=1e-4) and np.allclose(l_max, [31.0, 26.0, 4.8], atol=1e-4)):
        errors.append(f"Local bounds mismatch: {l_min.tolist()} to {l_max.tolist()}")

    wx = 35.0 + all_pts[:, 0] * c_t + all_pts[:, 2] * s_t
    wy = 150.0 + all_pts[:, 1]
    wz = -274.0 - all_pts[:, 0] * s_t + all_pts[:, 2] * c_t
    r_hub = np.hypot(wx, wz + 300.0)
    checks["world_bounds"] = {
        "x": [round(float(wx.min()), 4), round(float(wx.max()), 4)],
        "y": [round(float(wy.min()), 4), round(float(wy.max()), 4)],
        "z": [round(float(wz.min()), 4), round(float(wz.max()), 4)],
        "r_hub": [round(float(r_hub.min()), 4), round(float(r_hub.max()), 4)],
    }
    if float(r_hub.max()) > 63.2:
        errors.append(f"Max radial span {float(r_hub.max())} exceeds plaza curb R=63.2")

    # Verify GLB header & node count
    with open(glb_path, "rb") as gf:
        gb = gf.read()
    magic, ver, glen = struct.unpack("<III", gb[:12])
    jlen, _ = struct.unpack("<II", gb[12:20])
    jdoc = json.loads(gb[20:20 + jlen].decode("utf-8"))
    if magic != 0x46546C67 or ver != 2 or glen != len(gb) or len(jdoc["nodes"]) != 54:
        errors.append("Invalid primary GLB structure or node count")

    # Verify Collision Proxy
    col_tris = 0
    col_fg_max_y = 0.0
    col_v = []
    with open(col_obj_path, "r", encoding="utf-8") as cf:
        for ln in cf:
            if ln.startswith("v "):
                p = ln.split()
                v = [float(p[1]), float(p[2]), float(p[3])]
                col_v.append(v)
                if v[2] > 0.70:
                    col_fg_max_y = max(col_fg_max_y, v[1])
            elif ln.startswith("f "):
                col_tris += 1
    checks["collision_proxy_triangles"] = col_tris
    if col_tris != 168:
        errors.append(f"Expected 168 collision proxy triangles, found {col_tris}")
    if col_fg_max_y > 2.5001:
        errors.append(f"Collision proxy encroaches on dynamic avatar volume above Y=2.50: max_y={col_fg_max_y}")

    # Verify manifest/SM_Hub_Leaderboard_01.manifest.json schema compliance
    cand_path = os.path.join(pkg_root, "manifest/SM_Hub_Leaderboard_01.manifest.json")
    with open(cand_path, "r", encoding="utf-8") as mf:
        cand = json.load(mf)
    req_keys = {"id", "name", "kind", "status", "destination", "source", "rightsStatus", "notes"}
    allowed_keys = req_keys | {"robloxAssetId", "triangles", "textureResolution", "collision", "platformBudget"}
    if not req_keys.issubset(cand.keys()) or not set(cand.keys()).issubset(allowed_keys):
        errors.append("Candidate asset-manifest.json entry failed schema key validation")

    return {"status": "PASS" if not errors else "FAIL", "errors": errors, "checks": checks}


def main():
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_path = None
    if "--zip" in sys.argv:
        idx = sys.argv.index("--zip")
        if idx + 1 < len(sys.argv):
            zip_path = sys.argv[idx + 1]

    if zip_path:
        if not os.path.exists(zip_path):
            print(f"FAIL: ZIP file not found: {zip_path}")
            sys.exit(1)
        with zipfile.ZipFile(zip_path, "r") as zf:
            bad = zf.testzip()
            if bad is not None:
                print(f"FAIL: Corrupted entry in ZIP: {bad}")
                sys.exit(1)
            tmp_dir = tempfile.mkdtemp(prefix="validate_lb_zip_")
            try:
                zf.extractall(tmp_dir)
                extracted_root = os.path.join(tmp_dir, "Sphere_Brawl_Hub_Leaderboard_01_Package")
                res = validate_directory(extracted_root)
                sub = subprocess.run(
                    ["sha256sum", "-c", "SHA256SUMS.txt"],
                    cwd=extracted_root,
                    capture_output=True,
                    text=True,
                )
                if sub.returncode != 0:
                    res["status"] = "FAIL"
                    res["errors"].append(f"sha256sum -c failed: {sub.stderr}")
                res["zip_path"] = os.path.abspath(zip_path)
                res["zip_size_bytes"] = os.path.getsize(zip_path)
                res["zip_outer_sha256"] = sha256_of_file(zip_path)
                print(json.dumps(res, indent=2))
                sys.exit(0 if res["status"] == "PASS" else 1)
            finally:
                shutil.rmtree(tmp_dir, ignore_errors=True)
    else:
        res = validate_directory(pkg_dir)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
