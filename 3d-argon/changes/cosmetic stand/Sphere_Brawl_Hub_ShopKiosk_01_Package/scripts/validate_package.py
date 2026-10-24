#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — PACKAGE INTEGRITY, TRANSFORM & MANIFEST AUDIT TOOL
Asset ID: SM_Hub_ShopKiosk_01 (Argon Step 4 Phase 2 — Approved Arena Shop Bar Production: 20.0 x 8.0 x 7.6 Studs)
=================================================================================================================
Audits the package directory and/or extracted ZIP archive to verify:
1. Every required handoff file, mesh, script, config, texture, and preview (01..10) exists (30 total files).
2. README.md inventory, MANIFEST.json entries (28 payload files), SHA256SUMS.txt entries (29 entries), and actual files match 1:1.
3. Every file size and SHA-256 digest in MANIFEST.json and SHA256SUMS.txt matches the actual payload bytes.
4. Explicit mathematical validation of the Roblox Studio placement transform:
   - Verifies that CFrame.new(43, 150, -300) * CFrame.Angles(0, math.rad(-90), 0) and
     CFrame.fromMatrix(Vector3.new(43, 150, -300), Vector3.new(0, 0, 1), Vector3.new(0, 1, 0), Vector3.new(-1, 0, 0))
     are identical, right-handed (Right x Up == ZVector, det(R) == +1.0), and orthonormal (R^T R == I).
   - Verifies that local +Z (model front) transforms to world -X (-1, 0, 0), local +Y to world +Y (0, 1, 0),
     and local +X to world +Z (0, 0, 1).
   - Transforms all 7272 actual OBJ vertices and verifies world-aligned bounds X=[39.0, 47.0], Y=[150.0, 157.6], Z=[-310.0, -290.0],
     radial vertex fit R in [37.0, 52.5], and exact per-slot world XZ coordinates for GEO_ShopKiosk_DisplayItem_01..04.
   - Verifies that GLB total file size (399176 bytes) and chunk sizes match VALIDATION_REPORT.md and config.
5. If --zip is passed, verifies ZIP archive integrity (zipfile.testzip()), extracts to a clean
   temporary directory, and verifies all checksums, transforms, and manifest entries inside the extracted archive.
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
import numpy as np

REQUIRED_FILES = [
    "README.md",
    "MODEL_SPECIFICATION.md",
    "ROBLOX_STUDIO_IMPORT_GUIDE.md",
    "VALIDATION_REPORT.md",
    "MANIFEST.json",
    "SHA256SUMS.txt",
    "meshes/SM_Hub_ShopKiosk_01.obj",
    "meshes/SM_Hub_ShopKiosk_01.mtl",
    "meshes/SM_Hub_ShopKiosk_01.glb",
    "meshes/SphereBrawl_ShopKiosk_PaletteAtlas.png",
    "meshes/collision_proxy/COL_ShopKiosk_Body.obj",
    "meshes/collision_proxy/COL_ShopKiosk_Body.mtl",
    "meshes/collision_proxy/COL_ShopKiosk_Body.glb",
    "meshes/collision_proxy/SphereBrawl_ShopKiosk_PaletteAtlas.png",
    "textures/SphereBrawl_ShopKiosk_PaletteAtlas.png",
    "scripts/generate_hub_shop_kiosk_blender.py",
    "scripts/validate_package.py",
    "config/shop_kiosk_parameters.json",
    "manifest/SM_Hub_ShopKiosk_01.manifest.json",
    "docs/HUB_INTEGRATION_AND_CLEARANCE_REPORT.md",
    "previews/01_Preview_ThreeQuarter_Perspective.png",
    "previews/02_Preview_Front_Inward_Presentation.png",
    "previews/03_Preview_Top_Orthographic_Arrangement.png",
    "previews/04_Preview_Low_PlayerHeight_Approach.png",
    "previews/05_Preview_Rear_Side_Underside_Construction.png",
    "previews/06_Preview_NeutralClay_Geometry.png",
    "previews/07_Preview_Wireframe_Topology.png",
    "previews/08_Preview_Material_CloseUp.png",
    "previews/09_Preview_Integration_Hub_Overview.png",
    "previews/10_Preview_Visual_Comparison_Customize_vs_Shop.png",
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


def validate_placement_transform_and_glb(pkg_root):
    errors = []

    pos = np.array([43.0, 150.0, -300.0], dtype=np.float64)
    vX = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    vY = np.array([0.0, 1.0, 0.0], dtype=np.float64)
    vZ = np.array([-1.0, 0.0, 0.0], dtype=np.float64)
    R_matrix = np.column_stack([vX, vY, vZ])

    theta = math.radians(-90.0)
    R_angles = np.array([
        [math.cos(theta), 0.0, math.sin(theta)],
        [0.0,             1.0, 0.0],
        [-math.sin(theta), 0.0, math.cos(theta)],
    ], dtype=np.float64)

    if not np.allclose(R_matrix, R_angles, atol=1e-9):
        errors.append("CFrame.fromMatrix basis does not match CFrame.Angles(0, math.rad(-90), 0)")

    if not np.allclose(R_matrix.T @ R_matrix, np.eye(3), atol=1e-9):
        errors.append("Placement rotation matrix is not orthonormal (R^T R != I)")

    det_r = float(np.linalg.det(R_matrix))
    cross_xy = np.cross(vX, vY)
    if abs(det_r - 1.0) > 1e-9 or not np.allclose(cross_xy, vZ, atol=1e-9):
        errors.append(f"Placement matrix is not right-handed: det={det_r}, vX x vY={cross_xy}")

    world_fwd = R_matrix @ np.array([0.0, 0.0, 1.0])
    world_up = R_matrix @ np.array([0.0, 1.0, 0.0])
    world_right = R_matrix @ np.array([1.0, 0.0, 0.0])
    if not np.allclose(world_fwd, [-1.0, 0.0, 0.0], atol=1e-9):
        errors.append(f"Local +Z did not map to World -X: got {world_fwd}")
    if not np.allclose(world_up, [0.0, 1.0, 0.0], atol=1e-9):
        errors.append(f"Local +Y did not map to World +Y: got {world_up}")
    if not np.allclose(world_right, [0.0, 0.0, 1.0], atol=1e-9):
        errors.append(f"Local +X did not map to World +Z: got {world_right}")

    obj_path = os.path.join(pkg_root, "meshes/SM_Hub_ShopKiosk_01.obj")
    w_min = None
    w_max = None
    r_min_v = None
    r_max_v = None
    if os.path.isfile(obj_path):
        all_verts = []
        comp_verts = {}
        cur_comp = None
        with open(obj_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s.startswith("o "):
                    cur_comp = s.split()[1]
                    comp_verts.setdefault(cur_comp, [])
                elif s.startswith("v "):
                    p = s.split()
                    pt = np.array([float(p[1]), float(p[2]), float(p[3])], dtype=np.float64)
                    all_verts.append(pt)
                    if cur_comp is not None:
                        comp_verts[cur_comp].append(pt)

        V_local = np.array(all_verts)
        V_world = (V_local @ R_matrix.T) + pos
        w_min = np.round(V_world.min(axis=0), 4)
        w_max = np.round(V_world.max(axis=0), 4)
        if not np.allclose(w_min, [39.0, 150.0, -310.0], atol=1e-3):
            errors.append(f"Transformed world min bounds mismatch: {w_min}")
        if not np.allclose(w_max, [47.0, 157.6, -290.0], atol=1e-3):
            errors.append(f"Transformed world max bounds mismatch: {w_max}")

        radii = np.sqrt((V_world[:, 0] - 0.0) ** 2 + (V_world[:, 2] - (-300.0)) ** 2)
        r_min_v = round(float(radii.min()), 4)
        r_max_v = round(float(radii.max()), 4)
        if r_min_v < 37.0 or r_max_v > 52.5:
            errors.append(f"Vertex radial footprint outside R=[37.0, 52.5]: got [{r_min_v}, {r_max_v}]")

        expected_items_world_xz = {
            "GEO_ShopKiosk_DisplayItem_01": [42.75, -305.10],
            "GEO_ShopKiosk_DisplayItem_02": [42.75, -301.70],
            "GEO_ShopKiosk_DisplayItem_03": [42.75, -298.30],
            "GEO_ShopKiosk_DisplayItem_04": [42.75, -294.90],
        }
        for iname, exp_xz in expected_items_world_xz.items():
            pts_c = np.array(comp_verts.get(iname, []))
            if len(pts_c) == 0:
                errors.append(f"Missing display item component in OBJ: {iname}")
                continue
            pts_w = (pts_c @ R_matrix.T) + pos
            center_w = 0.5 * (pts_w.min(axis=0) + pts_w.max(axis=0))
            if not np.allclose([center_w[0], center_w[2]], exp_xz, atol=0.15):
                errors.append(f"World XZ center mismatch for {iname}: got {[center_w[0], center_w[2]]}, expected {exp_xz}")

    glb_path = os.path.join(pkg_root, "meshes/SM_Hub_ShopKiosk_01.glb")
    val_rep_path = os.path.join(pkg_root, "VALIDATION_REPORT.md")
    if os.path.isfile(glb_path) and os.path.isfile(val_rep_path):
        glb_size = os.path.getsize(glb_path)
        with open(glb_path, "rb") as gf:
            g_bytes = gf.read()
        magic, ver, total_len = struct.unpack("<III", g_bytes[:12])
        j_len, _ = struct.unpack("<II", g_bytes[12:20])
        b_len, _ = struct.unpack("<II", g_bytes[20 + j_len:28 + j_len])
        if glb_size != 399176 or total_len != 399176 or (12 + 8 + j_len + 8 + b_len) != 399176:
            errors.append(f"GLB size/chunk mismatch: file={glb_size}, header={total_len}, j={j_len}, b={b_len}")
        with open(val_rep_path, "r", encoding="utf-8") as vrf:
            vr_text = vrf.read()
        if "399,176 bytes" not in vr_text:
            errors.append("VALIDATION_REPORT.md does not report exact 399,176 bytes GLB size")

    return {
        "matrix_orthonormal_right_handed": len(errors) == 0,
        "determinant": det_r,
        "local_z_to_world": world_fwd.tolist(),
        "local_y_to_world": world_up.tolist(),
        "local_x_to_world": world_right.tolist(),
        "transformed_world_bounds_min": w_min.tolist() if w_min is not None else None,
        "transformed_world_bounds_max": w_max.tolist() if w_max is not None else None,
        "vertex_radial_min_studs": r_min_v,
        "vertex_radial_max_studs": r_max_v,
        "errors": errors,
    }


def audit_directory(pkg_root):
    errors = []
    actual_files_set = set()
    scan_dirs = [
        "",
        "meshes",
        "meshes/collision_proxy",
        "textures",
        "scripts",
        "config",
        "manifest",
        "docs",
        "previews",
    ]
    for sd in scan_dirs:
        full_sd = os.path.join(pkg_root, sd) if sd else pkg_root
        if os.path.isdir(full_sd):
            try:
                for entry in os.listdir(full_sd):
                    if entry in ("__pycache__", ".", "..") or entry.endswith(".pyc"):
                        continue
                    full_entry = os.path.join(full_sd, entry)
                    if os.path.isfile(full_entry):
                        rel = f"{sd}/{entry}" if sd else entry
                        actual_files_set.add(rel)
            except OSError:
                pass
    for req in REQUIRED_FILES:
        if os.path.isfile(os.path.join(pkg_root, req)):
            actual_files_set.add(req)
    actual_files = sorted(list(actual_files_set))

    for req in REQUIRED_FILES:
        if req not in actual_files:
            errors.append(f"MISSING REQUIRED FILE: {req}")

    for af in actual_files:
        if af.endswith(".zip") or af.endswith(".tmp"):
            errors.append(f"FORBIDDEN NESTED ARCHIVE OR TEMP FILE: {af}")

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
            missing_in_man = set(expected_payload) - set(manifest_paths)
            extra_in_man = set(manifest_paths) - set(expected_payload)
            if missing_in_man:
                errors.append(f"Files missing from MANIFEST.json: {sorted(list(missing_in_man))}")
            if extra_in_man:
                errors.append(f"Extra non-existent files in MANIFEST.json: {sorted(list(extra_in_man))}")

        for entry in manifest_files:
            p = entry["path"]
            full_p = os.path.join(pkg_root, p)
            if not os.path.exists(full_p):
                errors.append(f"MANIFEST path does not resolve: {p}")
                continue
            actual_sz = os.path.getsize(full_p)
            actual_sha = sha256_of_file(full_p)
            if actual_sz != entry["size_bytes"]:
                errors.append(f"Size mismatch for {p}: MANIFEST={entry['size_bytes']} vs ACTUAL={actual_sz}")
            if actual_sha != entry["sha256"]:
                errors.append(f"SHA256 mismatch in MANIFEST for {p}: {entry['sha256']} vs {actual_sha}")

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
            errors.append(f"SHA256SUMS.txt path list mismatch: {chk_paths} vs {expected_chk}")

        for digest, rel_p in checksum_entries:
            full_p = os.path.join(pkg_root, rel_p)
            if not os.path.exists(full_p):
                errors.append(f"SHA256SUMS target missing: {rel_p}")
                continue
            actual_sha = sha256_of_file(full_p)
            if actual_sha != digest:
                errors.append(f"SHA256SUMS digest mismatch for {rel_p}: expected {digest}, got {actual_sha}")

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as rf:
            readme_txt = rf.read()
        for af in actual_files:
            if f"`{af}`" not in readme_txt:
                errors.append(f"File `{af}` is not listed in README.md file inventory table")

    transform_check = validate_placement_transform_and_glb(pkg_root)
    if transform_check["errors"]:
        errors.extend(transform_check["errors"])

    return {
        "package_root": pkg_root,
        "total_actual_files": len(actual_files),
        "manifest_payload_files": len(manifest_files),
        "checksum_entries": len(checksum_entries),
        "placement_transform_validation": transform_check,
        "errors": errors,
        "status": "PASS" if len(errors) == 0 else "FAIL",
    }


def audit_zip(zip_path):
    if not os.path.isfile(zip_path):
        return {"status": "FAIL", "errors": [f"ZIP file not found: {zip_path}"]}

    errors = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        bad_member = zf.testzip()
        if bad_member is not None:
            errors.append(f"ZIP CRC integrity failure on entry: {bad_member}")
        namelist = [n for n in zf.namelist() if not n.endswith("/")]

    tmp_dir = tempfile.mkdtemp(prefix="audit_shop_kiosk_zip_")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_dir)

        sub_root = os.path.join(tmp_dir, "Sphere_Brawl_Hub_ShopKiosk_01_Package")
        target_root = sub_root if os.path.isdir(sub_root) else tmp_dir
        dir_report = audit_directory(target_root)
        errors.extend(dir_report["errors"])

        return {
            "zip_path": os.path.abspath(zip_path),
            "zip_size_bytes": os.path.getsize(zip_path),
            "zip_file_entries_count": len(namelist),
            "crc_integrity_test": "PASS" if bad_member is None else f"FAIL ({bad_member})",
            "extracted_audit": dir_report,
            "status": "PASS" if len(errors) == 0 else "FAIL",
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_pkg_root = os.path.abspath(os.path.join(script_dir, ".."))

    if "--zip" in sys.argv:
        idx = sys.argv.index("--zip")
        if idx + 1 >= len(sys.argv):
            print("ERROR: --zip requires a path argument")
            sys.exit(1)
        zpath = sys.argv[idx + 1]
        res = audit_zip(zpath)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["status"] == "PASS" else 1)
    else:
        res = audit_directory(default_pkg_root)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["status"] == "PASS" else 1)
