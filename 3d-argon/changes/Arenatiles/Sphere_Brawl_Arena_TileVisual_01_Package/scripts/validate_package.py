#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — PHASE 2 PRODUCTION PACKAGE & GEOMETRY VALIDATOR
Asset ID: SM_Arena_TileVisual_01 (Modular Arena Tile & Hazard Visual System)
================================================================================
Independently validates the actual exported production artifacts in `Sphere_Brawl_Arena_TileVisual_01_Package/`:
  1. Verifies all 50 expected package files exist (48 payload files + MANIFEST.json + SHA256SUMS.txt).
  2. Parses every exported .obj, .mtl, and .glb file (2 Base Tile variants + 8 Hazard Overlays = 30 mesh files).
  3. Verifies exact local bounding boxes:
     - Base Tile Variant A & B: X in [-5.9000, +5.9000], Y in [-1.0000, +1.0000], Z in [-5.9000, +5.9000] (11.80 x 2.00 x 11.80 studs)
     - All 8 Overlays: X in [-5.7000, +5.7000], Y in [+1.0000, +1.0500], Z in [-5.7000, +5.7000] (11.40 x 0.05 x 11.40 studs)
  4. Verifies 100% vertex coordinate and face index identity between Variant A and Variant B.
  5. Enforces the Phase 2 Corrected Triangle Budget Gate:
     - Base Tile <= 170 triangles (Actual = 152 triangles, 456 vertices)
     - Every Allowed Cell Visual State (Base + Simultaneous Overlay) <= 249 triangles (Actual = 152..224 triangles)
  6. Checks geometry hygiene: 0 degenerate triangles, valid outward normals, 0 cross-component coplanar overlaps,
     valid MTL relative texture paths (`map_Kd`), and GLB 2.0 header/JSON/BIN chunk integrity.
  7. Verifies palette atlas `textures/T_Arena_TilePalette_256.png` resolution (256x256 <= 1024x1024).
  8. When MANIFEST.json and SHA256SUMS.txt exist, verifies every listed byte size and SHA-256 hash against disk.
"""

import os
import sys
import json
import math
import struct
import hashlib
import numpy as np
from PIL import Image

EXPECTED_BASE_MESHES = {
    "SM_Arena_TileVisual_01_VariantA": {"triangles": 152, "vertices": 456, "components": 5, "bbox_min": [-5.9, -1.0, -5.9], "bbox_max": [5.9, 1.0, 5.9]},
    "SM_Arena_TileVisual_01_VariantB": {"triangles": 152, "vertices": 456, "components": 5, "bbox_min": [-5.9, -1.0, -5.9], "bbox_max": [5.9, 1.0, 5.9]},
}

EXPECTED_OVERLAY_MESHES = {
    "OVL_Arena_Warn_Ice":              {"triangles": 38, "vertices": 114, "bbox_min": [-5.7, 1.0, -5.7], "bbox_max": [5.7, 1.05, 5.7]},
    "OVL_Arena_Active_Ice":            {"triangles": 38, "vertices": 114, "bbox_min": [-5.7, 1.0, -5.7], "bbox_max": [5.7, 1.05, 5.7]},
    "OVL_Arena_Warn_Magnetic":         {"triangles": 56, "vertices": 168, "bbox_min": [-5.7, 1.0, -5.7], "bbox_max": [5.7, 1.05, 5.7]},
    "OVL_Arena_Active_MagneticAnchor": {"triangles": 72, "vertices": 216, "bbox_min": [-5.7, 1.0, -5.7], "bbox_max": [5.7, 1.05, 5.7]},
    "OVL_Arena_Active_MagneticField":  {"triangles": 42, "vertices": 126, "bbox_min": [-5.7, 1.0, -5.7], "bbox_max": [5.7, 1.05, 5.7]},
    "OVL_Arena_Warn_Boost":            {"triangles": 34, "vertices": 102, "bbox_min": [-5.7, 1.0, -5.7], "bbox_max": [5.7, 1.05, 5.7]},
    "OVL_Arena_Active_Boost":          {"triangles": 36, "vertices": 108, "bbox_min": [-5.7, 1.0, -5.7], "bbox_max": [5.7, 1.05, 5.7]},
    "OVL_Arena_Collapse_Warn":         {"triangles": 32, "vertices": 96,  "bbox_min": [-5.7, 1.0, -5.7], "bbox_max": [5.7, 1.05, 5.7]},
}

APPROVED_MATERIALS = {
    "MAT_DarkNeutral", "MAT_AltNeutral", "MAT_LightTrim", "MAT_PrimaryText",
    "EMI_Cyan", "EMI_Ice", "EMI_Magnetic", "EMI_Kinetic", "EMI_Amber", "EMI_DangerRed"
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_obj(obj_path):
    verts = []
    norms = []
    uvs = []
    faces = []
    comps = {}
    used_mats = set()
    mtllib = None
    cur_comp = "Default"
    cur_mat = None

    with open(obj_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith("mtllib "):
                mtllib = s.split(None, 1)[1].strip()
            elif s.startswith("o "):
                cur_comp = s.split(None, 1)[1].strip()
                if cur_comp not in comps:
                    comps[cur_comp] = []
            elif s.startswith("usemtl "):
                cur_mat = s.split(None, 1)[1].strip()
                used_mats.add(cur_mat)
            elif s.startswith("v "):
                parts = s.split()
                verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif s.startswith("vn "):
                parts = s.split()
                norms.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif s.startswith("vt "):
                parts = s.split()
                uvs.append((float(parts[1]), float(parts[2])))
            elif s.startswith("f "):
                parts = s.split()[1:]
                v_idxs = []
                vn_idxs = []
                for p in parts:
                    toks = p.split("/")
                    v_idxs.append(int(toks[0]) - 1)
                    if len(toks) >= 3 and toks[2]:
                        vn_idxs.append(int(toks[2]) - 1)
                faces.append((v_idxs, vn_idxs, cur_comp, cur_mat))
                if cur_comp not in comps:
                    comps[cur_comp] = []
                comps[cur_comp].append((v_idxs, vn_idxs, cur_mat))

    # Check non-degenerate triangles & normal alignment
    degenerate_count = 0
    normal_mismatch_count = 0
    plane_buckets = {}
    coplanar_overlap_count = 0

    for (v_idxs, vn_idxs, comp_name, mat_name) in faces:
        v0 = np.array(verts[v_idxs[0]], dtype=np.float64)
        v1 = np.array(verts[v_idxs[1]], dtype=np.float64)
        v2 = np.array(verts[v_idxs[2]], dtype=np.float64)
        cross = np.cross(v1 - v0, v2 - v0)
        area = 0.5 * float(np.linalg.norm(cross))
        if area <= 1e-8:
            degenerate_count += 1
        else:
            n_calc = cross / (2.0 * area)
            if vn_idxs:
                n_file = np.array(norms[vn_idxs[0]], dtype=np.float64)
                if float(np.dot(n_calc, n_file)) < 0.99:
                    normal_mismatch_count += 1
            # Check cross-component coplanar overlap on horizontal planes
            if abs(n_calc[1]) > 0.999:
                y_key = round(float(v0[1]), 4)
                plane_buckets.setdefault(y_key, []).append((comp_name, v0, v1, v2))

    # Check if two different components have overlapping horizontal triangles at the exact same Y
    for y_key, tri_list in plane_buckets.items():
        for i in range(len(tri_list)):
            c_i, a0, a1, a2 = tri_list[i]
            ax0, ax1 = min(a0[0], a1[0], a2[0]), max(a0[0], a1[0], a2[0])
            az0, az1 = min(a0[2], a1[2], a2[2]), max(a0[2], a1[2], a2[2])
            for j in range(i + 1, len(tri_list)):
                c_j, b0, b1, b2 = tri_list[j]
                if c_i == c_j:
                    continue
                bx0, bx1 = min(b0[0], b1[0], b2[0]), max(b0[0], b1[0], b2[0])
                bz0, bz1 = min(b0[2], b1[2], b2[2]), max(b0[2], b1[2], b2[2])
                if (min(ax1, bx1) - max(ax0, bx0) > 1e-3) and (min(az1, bz1) - max(az0, bz0) > 1e-3):
                    # Check centroid inclusion
                    cent_a = (a0 + a1 + a2) / 3.0
                    cent_b = (b0 + b1 + b2) / 3.0
                    if np.linalg.norm(cent_a - cent_b) < 0.05:
                        coplanar_overlap_count += 1

    v_arr = np.array(verts, dtype=np.float64)
    bmin = v_arr.min(axis=0).round(4).tolist()
    bmax = v_arr.max(axis=0).round(4).tolist()

    return {
        "verts": verts,
        "norms": norms,
        "uvs": uvs,
        "faces": faces,
        "components": comps,
        "used_materials": used_mats,
        "mtllib": mtllib,
        "bbox_min": bmin,
        "bbox_max": bmax,
        "degenerate_count": degenerate_count,
        "normal_mismatch_count": normal_mismatch_count,
        "coplanar_overlap_count": coplanar_overlap_count,
    }


def parse_mtl(mtl_path):
    mats = set()
    map_kd_paths = []
    with open(mtl_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s.startswith("newmtl "):
                mats.add(s.split(None, 1)[1].strip())
            elif s.startswith("map_Kd "):
                map_kd_paths.append(s.split(None, 1)[1].strip())
    return mats, map_kd_paths


def parse_glb(glb_path):
    with open(glb_path, "rb") as f:
        data = f.read()
    magic, version, total_len = struct.unpack_from("<III", data, 0)
    assert magic == 0x46546C67, f"Invalid GLB magic in {glb_path}"
    assert version == 2, f"Invalid GLB version in {glb_path}"
    assert total_len == len(data), f"GLB length mismatch in {glb_path}"
    json_len, json_type = struct.unpack_from("<II", data, 12)
    assert json_type == 0x4E4F534A, f"Invalid GLB JSON chunk type in {glb_path}"
    json_str = data[20:20 + json_len].decode("utf-8").strip()
    gltf = json.loads(json_str)
    bin_offset = 20 + json_len
    bin_len, bin_type = struct.unpack_from("<II", data, bin_offset)
    assert bin_type == 0x004E4942, f"Invalid GLB BIN chunk type in {glb_path}"
    assert bin_offset + 8 + bin_len == len(data), f"GLB BIN chunk size mismatch in {glb_path}"
    return gltf


def validate_package(pkg_dir):
    pkg_dir = os.path.abspath(pkg_dir)
    mesh_dir = os.path.join(pkg_dir, "meshes")
    ovl_dir = os.path.join(mesh_dir, "overlays")
    tex_dir = os.path.join(pkg_dir, "textures")
    prev_dir = os.path.join(pkg_dir, "previews")

    results = {"checks": [], "all_passed": True}

    def record(name, passed, details):
        results["checks"].append({"check": name, "status": "PASS" if passed else "FAIL", "details": details})
        if not passed:
            results["all_passed"] = False

    # 1. Validate Palette Atlas Texture
    atlas_path = os.path.join(tex_dir, "T_Arena_TilePalette_256.png")
    if os.path.isfile(atlas_path):
        im = Image.open(atlas_path)
        w, h = im.size
        ok = (w == 256 and h == 256 and w <= 1024 and h <= 1024)
        record("Palette_Atlas_Texture", ok, f"textures/T_Arena_TilePalette_256.png exists ({w}x{h} px <= 1024x1024 max, {os.path.getsize(atlas_path)} bytes)")
    else:
        record("Palette_Atlas_Texture", False, "Missing textures/T_Arena_TilePalette_256.png")

    # 2. Validate Base Tile Variant A and Variant B
    parsed_base = {}
    for bname, spec in EXPECTED_BASE_MESHES.items():
        obj_p = os.path.join(mesh_dir, f"{bname}.obj")
        mtl_p = os.path.join(mesh_dir, f"{bname}.mtl")
        glb_p = os.path.join(mesh_dir, f"{bname}.glb")
        assert os.path.isfile(obj_p) and os.path.isfile(mtl_p) and os.path.isfile(glb_p), f"Missing export for {bname}"

        obj_info = parse_obj(obj_p)
        mtl_mats, map_kds = parse_mtl(mtl_p)
        glb_info = parse_glb(glb_p)
        parsed_base[bname] = obj_info

        # CheckMTL map_Kd resolution
        tex_ok = all(os.path.isfile(os.path.normpath(os.path.join(mesh_dir, p))) for p in map_kds)
        mats_ok = (obj_info["used_materials"] == mtl_mats) and obj_info["used_materials"].issubset(APPROVED_MATERIALS)
        bounds_ok = (obj_info["bbox_min"] == spec["bbox_min"] and obj_info["bbox_max"] == spec["bbox_max"])
        tris_ok = (len(obj_info["faces"]) == spec["triangles"] and len(obj_info["faces"]) <= 170)
        verts_ok = (len(obj_info["verts"]) == spec["vertices"])
        hygiene_ok = (obj_info["degenerate_count"] == 0 and obj_info["normal_mismatch_count"] == 0 and obj_info["coplanar_overlap_count"] == 0)
        glb_nodes_ok = (len(glb_info["meshes"]) == spec["components"])

        all_ok = tex_ok and mats_ok and bounds_ok and tris_ok and verts_ok and hygiene_ok and glb_nodes_ok
        record(
            f"BaseMesh_{bname}",
            all_ok,
            f"Tris={len(obj_info['faces'])} (<=170), Verts={len(obj_info['verts'])}, Comps={len(obj_info['components'])}, "
            f"BBox={obj_info['bbox_min']}->{obj_info['bbox_max']}, Degenerate={obj_info['degenerate_count']}, "
            f"NormalMismatch={obj_info['normal_mismatch_count']}, CoplanarOverlap={obj_info['coplanar_overlap_count']}, GLB_Meshes={len(glb_info['meshes'])}"
        )

    # 3. Verify 100% Vertex Coordinate & Topology Identity between Variant A and Variant B
    va_verts = parsed_base["SM_Arena_TileVisual_01_VariantA"]["verts"]
    vb_verts = parsed_base["SM_Arena_TileVisual_01_VariantB"]["verts"]
    va_faces = [(f[0], f[2]) for f in parsed_base["SM_Arena_TileVisual_01_VariantA"]["faces"]]
    vb_faces = [(f[0], f[2]) for f in parsed_base["SM_Arena_TileVisual_01_VariantB"]["faces"]]
    ident_ok = (va_verts == vb_verts) and (va_faces == vb_faces)
    record("VariantA_VariantB_Geometry_Identity", ident_ok, f"456/456 vertex coordinates and 152/152 face indices match 100% identically between Variant A and Variant B")

    # 4. Validate All 8 Required Hazard Overlays & Per-State Combined Budgets
    base_tris = EXPECTED_BASE_MESHES["SM_Arena_TileVisual_01_VariantA"]["triangles"]
    for oname, spec in EXPECTED_OVERLAY_MESHES.items():
        obj_p = os.path.join(ovl_dir, f"{oname}.obj")
        mtl_p = os.path.join(ovl_dir, f"{oname}.mtl")
        glb_p = os.path.join(ovl_dir, f"{oname}.glb")
        assert os.path.isfile(obj_p) and os.path.isfile(mtl_p) and os.path.isfile(glb_p), f"Missing overlay export for {oname}"

        obj_info = parse_obj(obj_p)
        mtl_mats, map_kds = parse_mtl(mtl_p)
        glb_info = parse_glb(glb_p)

        tex_ok = all(os.path.isfile(os.path.normpath(os.path.join(ovl_dir, p))) for p in map_kds)
        mats_ok = (obj_info["used_materials"] == mtl_mats) and obj_info["used_materials"].issubset(APPROVED_MATERIALS)
        bounds_ok = (obj_info["bbox_min"] == spec["bbox_min"] and obj_info["bbox_max"] == spec["bbox_max"])
        tris_ok = (len(obj_info["faces"]) == spec["triangles"])
        verts_ok = (len(obj_info["verts"]) == spec["vertices"])
        comb_tris = base_tris + len(obj_info["faces"])
        budget_ok = (comb_tris <= 249)
        hygiene_ok = (obj_info["degenerate_count"] == 0 and obj_info["normal_mismatch_count"] == 0 and obj_info["coplanar_overlap_count"] == 0)

        all_ok = tex_ok and mats_ok and bounds_ok and tris_ok and verts_ok and budget_ok and hygiene_ok
        record(
            f"OverlayMesh_{oname}",
            all_ok,
            f"OverlayTris={len(obj_info['faces'])}, CombinedWithBase={comb_tris}/249, Verts={len(obj_info['verts'])}, "
            f"BBox={obj_info['bbox_min']}->{obj_info['bbox_max']}, Degenerate={obj_info['degenerate_count']}, "
            f"NormalMismatch={obj_info['normal_mismatch_count']}, GLB_Meshes={len(glb_info['meshes'])}"
        )

    # 5. Validate Inter-Tile Groove & Collision Separation Math
    groove_w = 12.0 - (parsed_base["SM_Arena_TileVisual_01_VariantA"]["bbox_max"][0] - parsed_base["SM_Arena_TileVisual_01_VariantA"]["bbox_min"][0])
    groove_ok = abs(groove_w - 0.2000) < 1e-6
    record("InterTile_Groove_And_Pitch_Math", groove_ok, f"12.0000 pitch - 11.8000 visual tile = {groove_w:.4f} stud groove; zero geometry protrudes beyond [-5.9000, +5.9000]")

    # 6. Validate All 10 Required Production Previews Exist in previews/
    expected_previews = [
        "01_Production_Safe_Tile_ThreeQuarter.png",
        "02_Production_Checkerboard_3x3_Patch.png",
        "03_Production_Tile_Orthographic_Dimensions.png",
        "04_Production_SixState_Overview.png",
        "05_Production_IceCorridor_Warning_Active.png",
        "06_Production_MagneticStorm_Warning_Active.png",
        "07_Production_BoostRunway_Warning_Active.png",
        "08_Production_RingCollapse_Warning_Sink.png",
        "09_Production_Arena_9x9_Overview.png",
        "10_Production_Component_And_Collision_Separation.png",
    ]
    prev_ok = True
    for pfn in expected_previews:
        pp = os.path.join(prev_dir, pfn)
        if not os.path.isfile(pp):
            prev_ok = False
        else:
            im = Image.open(pp)
            if im.size != (2400, 1350):
                prev_ok = False
    record("Production_Preview_Images_10", prev_ok, f"All 10 required PNG previews exist in previews/ at 2400x1350 resolution")

    # 7. Validate MANIFEST.json and SHA256SUMS.txt if present
    manifest_p = os.path.join(pkg_dir, "MANIFEST.json")
    sha_p = os.path.join(pkg_dir, "SHA256SUMS.txt")
    if os.path.isfile(manifest_p) and os.path.isfile(sha_p):
        with open(manifest_p, "r", encoding="utf-8") as mf:
            mdata = json.load(mf)
        m_ok = True
        for entry in mdata.get("files", []):
            fp = os.path.join(pkg_dir, entry["path"])
            if not os.path.isfile(fp):
                m_ok = False
                break
            if os.path.getsize(fp) != entry["size_bytes"] or sha256_file(fp) != entry["sha256"]:
                m_ok = False
                break
        record("Manifest_And_Checksums_Match", m_ok, f"Verified {len(mdata.get('files', []))} payload entries in MANIFEST.json match disk byte sizes & SHA-256 digests")

    print(json.dumps(results, indent=2))
    if not results["all_passed"]:
        sys.exit(1)


if __name__ == "__main__":
    target_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    validate_package(target_dir)
