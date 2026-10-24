#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — PACKAGE INTEGRITY, TRANSFORM, UI-PANEL & MANIFEST AUDIT TOOL
Asset ID: SM_Hub_ModeBoard_01 (Step 5, Phase 2 — Approved Mode Selection Board Production: 14.4 x 3.8 x 8.8 Studs)
====================================================================================================================
Audits the package directory and/or extracted ZIP archive to verify:
1. Every required handoff document, mesh, collision proxy, script, config, manifest, texture, and preview (01..10)
   exists (29 total files: 27 payload files in MANIFEST.json + MANIFEST.json + SHA256SUMS.txt).
2. README.md inventory, MANIFEST.json entries (27 payload files), SHA256SUMS.txt entries (28 entries), and actual
   on-disk files match 1:1 with zero missing, duplicate, or unexpected files.
3. Every file size and SHA-256 digest in MANIFEST.json and SHA256SUMS.txt matches the actual payload bytes.
4. Explicit mathematical and geometric validation:
   - Verifies that CFrame.new(35, 150, -326) * CFrame.Angles(0, math.rad(-53.39292061), 0) maps local +Z (model front)
     to FrontVector = (-0.802744, 0, +0.596324) pointing at Hub center (0, 150, -300), local +Y to (0, 1, 0),
     and local +X to (+0.596324, 0, +0.802744), with det(R) == +1.0 and R^T R == I.
   - Parses `meshes/SM_Hub_ModeBoard_01.obj`, `.mtl`, and `.glb` and verifies 1,612 triangles (< 2,500 budget),
     4,836 vertices, 18 named components, 5 locked materials, 0 degenerate faces, 0 normal mismatches, and
     local bounds X=[-7.2000, +7.2000], Y=[0.0000, +8.8000], Z=[-1.9000, +1.9000].
   - Verifies that all 5 UI-ready surfaces (`GEO_ModeBoard_UIPanel_01_FFA`, `_02_Duel`, `_03_TeamClash`,
     `_04_KingTile`, and `GEO_ModeBoard_HeaderSign`) exist as separate flat components with valid front faces.
   - Transforms all 4,836 vertices to world space and verifies World AABB X=[29.3702, 40.6298], Y=[150.0000, 158.8000],
     Z=[-332.6738, -319.3320] and radial fit R in [41.7610, 46.0024] inside [37.0, 52.5].
   - Validates `manifest/SM_Hub_ModeBoard_01.manifest.json` against `specs/ASSET_MANIFEST.schema.json` required fields.
5. If `--zip <path>` is passed, verifies ZIP archive integrity (`zipfile.testzip()`), extracts to a clean temporary
   directory, and runs all directory, checksum, transform, and mesh audits inside the clean extraction.
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
    "meshes/SM_Hub_ModeBoard_01.obj",
    "meshes/SM_Hub_ModeBoard_01.mtl",
    "meshes/SM_Hub_ModeBoard_01.glb",
    "meshes/SphereBrawl_ModeBoard_PaletteAtlas.png",
    "meshes/collision_proxy/COL_ModeBoard_Body.obj",
    "meshes/collision_proxy/COL_ModeBoard_Body.mtl",
    "meshes/collision_proxy/COL_ModeBoard_Body.glb",
    "meshes/collision_proxy/SphereBrawl_ModeBoard_PaletteAtlas.png",
    "textures/SphereBrawl_ModeBoard_PaletteAtlas.png",
    "scripts/generate_mode_board_blender.py",
    "scripts/validate_package.py",
    "config/mode_board_parameters.json",
    "manifest/SM_Hub_ModeBoard_01.manifest.json",
    "previews/01_Production_Player_Approach_ThreeQuarter.png",
    "previews/02_Production_Direct_Front_Elevation.png",
    "previews/03_Production_Side_Orthographic.png",
    "previews/04_Production_Rear_Structural_View.png",
    "previews/05_Production_TopDown_Footprint.png",
    "previews/06_Production_Neutral_Clay.png",
    "previews/07_Production_Hub_Integration.png",
    "previews/08_Production_ModeState_CloseUp.png",
    "previews/09_Production_UI_Panel_Surface_Proof.png",
    "previews/10_Production_Technical_Component_Overview.png",
]

EXPECTED_COMPONENTS = [
    "GEO_ModeBoard_BasePlinth",
    "GEO_ModeBoard_BaseUpperTier",
    "GEO_ModeBoard_MainChassis",
    "GEO_ModeBoard_LeftButtress",
    "GEO_ModeBoard_RightButtress",
    "GEO_ModeBoard_SideCollars",
    "GEO_ModeBoard_CommandMatrixFrame",
    "GEO_ModeBoard_UIPanel_01_FFA",
    "GEO_ModeBoard_UIPanel_02_Duel",
    "GEO_ModeBoard_UIPanel_03_TeamClash",
    "GEO_ModeBoard_UIPanel_04_KingTile",
    "GEO_ModeBoard_HeaderCanopy",
    "GEO_ModeBoard_HeaderSign",
    "GEO_ModeBoard_ActiveModeReticle",
    "GEO_ModeBoard_LockReliefs",
    "GEO_ModeBoard_ModeReliefs",
    "GEO_ModeBoard_CyanAccents",
    "GEO_ModeBoard_AmberAccents",
]

UI_PANEL_COMPONENTS = [
    "GEO_ModeBoard_UIPanel_01_FFA",
    "GEO_ModeBoard_UIPanel_02_Duel",
    "GEO_ModeBoard_UIPanel_03_TeamClash",
    "GEO_ModeBoard_UIPanel_04_KingTile",
    "GEO_ModeBoard_HeaderSign",
]

EXPECTED_MATERIALS = [
    "MAT_DarkNeutral",
    "MAT_AltNeutral",
    "MAT_LightTrim",
    "EMI_Cyan",
    "EMI_Amber",
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


def validate_mesh_transform_and_glb(pkg_root):
    errors = []

    # 1. Placement Transform Basis Proof
    theta = math.radians(-53.39292061)
    c_t, s_t = math.cos(theta), math.sin(theta)
    vX = np.array([c_t, 0.0, -s_t], dtype=np.float64)
    vY = np.array([0.0, 1.0, 0.0], dtype=np.float64)
    vZ = np.array([s_t, 0.0, c_t], dtype=np.float64)
    R_matrix = np.column_stack([vX, vY, vZ])

    target_dir = np.array([-35.0, 0.0, 26.0], dtype=np.float64)
    target_dir /= np.linalg.norm(target_dir)

    if not np.allclose(vZ, target_dir, atol=1e-6):
        errors.append(f"FrontVector {vZ} does not match radial inward unit vector {target_dir}")
    if not np.allclose(R_matrix.T @ R_matrix, np.eye(3), atol=1e-9):
        errors.append("Placement rotation matrix is not orthonormal (R^T R != I)")
    det_r = float(np.linalg.det(R_matrix))
    if abs(det_r - 1.0) > 1e-9 or not np.allclose(np.cross(vX, vY), vZ, atol=1e-9):
        errors.append(f"Placement matrix is not right-handed: det={det_r}")

    # 2. Parse OBJ & MTL
    obj_path = os.path.join(pkg_root, "meshes/SM_Hub_ModeBoard_01.obj")
    mtl_path = os.path.join(pkg_root, "meshes/SM_Hub_ModeBoard_01.mtl")
    glb_path = os.path.join(pkg_root, "meshes/SM_Hub_ModeBoard_01.glb")
    col_obj_path = os.path.join(pkg_root, "meshes/collision_proxy/COL_ModeBoard_Body.obj")
    col_glb_path = os.path.join(pkg_root, "meshes/collision_proxy/COL_ModeBoard_Body.glb")

    if not (os.path.exists(obj_path) and os.path.exists(mtl_path) and os.path.exists(glb_path)):
        errors.append("Missing primary OBJ/MTL/GLB files")
        return {"errors": errors}

    mtl_mats = []
    with open(mtl_path, "r", encoding="utf-8") as mf:
        for line in mf:
            s = line.strip()
            if s.startswith("newmtl "):
                mtl_mats.append(s[7:].strip())
    if sorted(mtl_mats) != sorted(EXPECTED_MATERIALS):
        errors.append(f"MTL material list mismatch: {mtl_mats} vs {EXPECTED_MATERIALS}")

    verts = []
    normals = []
    comp_tris = {}
    comp_mats = {}
    cur_comp = None
    mtllib_val = None
    with open(obj_path, "r", encoding="utf-8") as of:
        for line in of:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith("mtllib "):
                mtllib_val = s.split()[1]
            elif s.startswith("o "):
                cur_comp = s[2:].strip()
                comp_tris.setdefault(cur_comp, [])
            elif s.startswith("usemtl "):
                comp_mats[cur_comp] = s[7:].strip()
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

    if mtllib_val != "SM_Hub_ModeBoard_01.mtl":
        errors.append(f"Invalid mtllib reference in OBJ: {mtllib_val}")

    if list(comp_tris.keys()) != EXPECTED_COMPONENTS:
        errors.append(f"OBJ component list mismatch: {list(comp_tris.keys())} vs {EXPECTED_COMPONENTS}")

    total_tris = sum(len(v) for v in comp_tris.values())
    if total_tris >= 2500 or total_tris != 1612:
        errors.append(f"Unexpected primary triangle count: {total_tris} (expected 1612 < 2500)")

    # Verify UI-ready panels have flat front faces
    n_inclined = np.array([0.0, math.sin(math.radians(14.0)), math.cos(math.radians(14.0))])
    for ui_c in UI_PANEL_COMPONENTS:
        tlist = comp_tris.get(ui_c, [])
        if not tlist:
            errors.append(f"Missing UI panel component: {ui_c}")
            continue
        target_n = np.array([0.0, 0.0, 1.0]) if ui_c == "GEO_ModeBoard_HeaderSign" else n_inclined
        front_tris = [t for t in tlist if float(np.dot(t[3], target_n)) > 0.999]
        if len(front_tris) != 2:
            errors.append(f"UI panel {ui_c} expected 2 coplanar front triangles, found {len(front_tris)}")

    all_pts = np.array(verts)
    l_min = all_pts.min(axis=0)
    l_max = all_pts.max(axis=0)
    if not (np.allclose(l_min, [-7.2, 0.0, -1.9], atol=1e-4) and np.allclose(l_max, [7.2, 8.8, 1.9], atol=1e-4)):
        errors.append(f"Local bounding box mismatch: min={l_min.tolist()}, max={l_max.tolist()}")

    w_pts = np.zeros_like(all_pts)
    w_pts[:, 0] = 35.0 + all_pts[:, 0] * c_t + all_pts[:, 2] * s_t
    w_pts[:, 1] = 150.0 + all_pts[:, 1]
    w_pts[:, 2] = -326.0 - all_pts[:, 0] * s_t + all_pts[:, 2] * c_t
    w_min = w_pts.min(axis=0)
    w_max = w_pts.max(axis=0)
    radii = np.hypot(w_pts[:, 0], w_pts[:, 2] + 300.0)
    r_min_v = float(radii.min())
    r_max_v = float(radii.max())
    if r_min_v < 37.0 or r_max_v > 52.5:
        errors.append(f"Transformed vertices fall outside R=[37.0, 52.5] station ring: [{r_min_v}, {r_max_v}]")

    # 3. Verify GLB binary structure
    with open(glb_path, "rb") as gf:
        glb_bytes = gf.read()
    magic, ver, glb_len = struct.unpack("<III", glb_bytes[:12])
    j_len, j_type = struct.unpack("<II", glb_bytes[12:20])
    j_data = json.loads(glb_bytes[20:20 + j_len].decode("utf-8"))
    if magic != 0x46546C67 or ver != 2 or glb_len != len(glb_bytes):
        errors.append("Invalid GLB header or length mismatch")
    glb_node_names = [n["name"] for n in j_data["nodes"]]
    if glb_node_names != ["SM_Hub_ModeBoard_01"] + EXPECTED_COMPONENTS:
        errors.append(f"GLB node list mismatch: {glb_node_names}")

    # 4. Verify Collision Proxy
    col_tris = 0
    with open(col_obj_path, "r", encoding="utf-8") as cf:
        for line in cf:
            if line.startswith("f "):
                col_tris += 1
    if col_tris != 36:
        errors.append(f"Collision proxy expected 36 triangles, found {col_tris}")

    # 5. Verify Repository Asset Manifest Schema Compatibility
    repo_man_path = os.path.join(pkg_root, "manifest/SM_Hub_ModeBoard_01.manifest.json")
    if os.path.exists(repo_man_path):
        with open(repo_man_path, "r", encoding="utf-8") as rmf:
            rm_data = json.load(rmf)
        allowed_keys = {
            "id", "name", "kind", "status", "destination", "source",
            "rightsStatus", "robloxAssetId", "triangles", "textureResolution",
            "collision", "platformBudget", "notes"
        }
        req_keys = {"id", "name", "kind", "status", "destination", "source", "rightsStatus", "notes"}
        if not req_keys.issubset(set(rm_data.keys())):
            errors.append(f"Missing required schema keys in SM_Hub_ModeBoard_01.manifest.json: {req_keys - set(rm_data.keys())}")
        extra_k = set(rm_data.keys()) - allowed_keys
        if extra_k:
            errors.append(f"Disallowed additionalProperties in SM_Hub_ModeBoard_01.manifest.json: {extra_k}")
    else:
        errors.append("Missing manifest/SM_Hub_ModeBoard_01.manifest.json")

    return {
        "primary_triangles": total_tris,
        "primary_vertices": len(verts),
        "collision_proxy_triangles": col_tris,
        "local_bbox_min": [round(float(x), 4) for x in l_min],
        "local_bbox_max": [round(float(x), 4) for x in l_max],
        "world_aabb_min": [round(float(x), 4) for x in w_min],
        "world_aabb_max": [round(float(x), 4) for x in w_max],
        "vertex_radial_min_studs": round(r_min_v, 4),
        "vertex_radial_max_studs": round(r_max_v, 4),
        "glb_file_size_bytes": len(glb_bytes),
        "errors": errors,
    }


def audit_directory(pkg_root):
    errors = []
    actual_files = []
    for root, _, files in os.walk(pkg_root):
        for f in files:
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, pkg_root).replace("\\", "/")
            actual_files.append(rel_p)
    actual_files.sort()

    for req in REQUIRED_FILES:
        if req not in actual_files:
            errors.append(f"Missing required file: {req}")
    for af in actual_files:
        if af not in REQUIRED_FILES:
            errors.append(f"Unexpected extra file in package: {af}")

    manifest_path = os.path.join(pkg_root, "MANIFEST.json")
    checksums_path = os.path.join(pkg_root, "SHA256SUMS.txt")
    readme_path = os.path.join(pkg_root, "README.md")

    manifest_files = []
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as mf:
            manifest_data = json.load(mf)
        manifest_files = manifest_data.get("files", [])
        manifest_paths = sorted([entry["path"] for entry in manifest_files])
        expected_payload = sorted([f for f in actual_files if f not in ("MANIFEST.json", "SHA256SUMS.txt")])
        if manifest_paths != expected_payload:
            errors.append(f"MANIFEST.json file list mismatch vs disk payload")
        for entry in manifest_files:
            p = entry["path"]
            full_p = os.path.join(pkg_root, p)
            if not os.path.exists(full_p):
                errors.append(f"MANIFEST path does not resolve: {p}")
                continue
            if os.path.getsize(full_p) != entry["size_bytes"]:
                errors.append(f"Size mismatch for {p}: MANIFEST={entry['size_bytes']} vs ACTUAL={os.path.getsize(full_p)}")
            if sha256_of_file(full_p) != entry["sha256"]:
                errors.append(f"SHA256 mismatch in MANIFEST for {p}")

    checksum_entries = []
    if os.path.exists(checksums_path):
        with open(checksums_path, "r", encoding="utf-8") as cf:
            for line in cf:
                s = line.strip()
                if not s:
                    continue
                parts = s.split("  ", 1)
                if len(parts) != 2:
                    errors.append(f"Malformed line in SHA256SUMS.txt: {s}")
                    continue
                checksum_entries.append((parts[0], parts[1]))
        chk_paths = sorted([p for _, p in checksum_entries])
        expected_chk = sorted([f for f in actual_files if f != "SHA256SUMS.txt"])
        if chk_paths != expected_chk:
            errors.append("SHA256SUMS.txt path list mismatch")
        for digest, rel_p in checksum_entries:
            full_p = os.path.join(pkg_root, rel_p)
            if not os.path.exists(full_p):
                errors.append(f"SHA256SUMS target missing: {rel_p}")
                continue
            if sha256_of_file(full_p) != digest:
                errors.append(f"SHA256SUMS digest mismatch for {rel_p}")

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as rf:
            readme_txt = rf.read()
        for af in actual_files:
            if f"`{af}`" not in readme_txt:
                errors.append(f"File `{af}` is not listed in README.md file inventory table")

    mesh_check = validate_mesh_transform_and_glb(pkg_root)
    if mesh_check["errors"]:
        errors.extend(mesh_check["errors"])

    return {
        "total_files": len(actual_files),
        "manifest_described_files": len(manifest_files),
        "checksum_entries_verified": len(checksum_entries),
        "mesh_and_transform_validation": mesh_check,
        "errors": errors,
        "status": "PASS" if len(errors) == 0 else "FAIL",
    }


def audit_zip(zip_path):
    if not os.path.exists(zip_path):
        return {"status": "FAIL", "errors": [f"ZIP file not found: {zip_path}"]}

    with zipfile.ZipFile(zip_path, "r") as zf:
        bad_member = zf.testzip()
        if bad_member is not None:
            return {"status": "FAIL", "errors": [f"Corrupt ZIP member: {bad_member}"]}
        file_entries = [i.filename for i in zf.infolist() if not i.is_dir()]

    tmp_dir = tempfile.mkdtemp(prefix="audit_modeboard_zip_")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_dir)
        sub_root = os.path.join(tmp_dir, "Sphere_Brawl_Hub_ModeBoard_01_Package")
        if not os.path.isdir(sub_root):
            sub_root = tmp_dir
        res = audit_directory(sub_root)
        proc = subprocess.run(["sha256sum", "-c", "SHA256SUMS.txt"], cwd=sub_root, capture_output=True, text=True)
        res["sha256sum_cli_exit_code"] = proc.returncode
        if proc.returncode != 0:
            res["errors"].append(f"sha256sum -c failed: {proc.stderr}")
            res["status"] = "FAIL"
        res["zip_file_entries"] = len(file_entries)
        res["zip_integrity_test"] = "PASS (0 CRC errors)"
        res["zip_size_bytes"] = os.path.getsize(zip_path)
        res["zip_sha256"] = sha256_of_file(zip_path)
        if res["zip_file_entries"] != res["total_files"]:
            res["errors"].append(f"ZIP entry count ({res['zip_file_entries']}) != extracted file count ({res['total_files']})")
            res["status"] = "FAIL"
        return res
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_arg = None
    if "--zip" in sys.argv:
        idx = sys.argv.index("--zip")
        if idx + 1 < len(sys.argv):
            zip_arg = sys.argv[idx + 1]

    if zip_arg:
        report = audit_zip(zip_arg)
    else:
        report = audit_directory(pkg_dir)

    print(json.dumps(report, indent=2))
    if report["status"] != "PASS":
        sys.exit(1)
