#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — DETERMINISTIC BLENDER 3.6+ / 4.x & PYTHON GENERATOR
Asset ID: SM_Hub_QueuePadRing_01 (Hub Queue Pad Ring — Argon Step 2)
===================================================================================
- Outer Queue Boundary Radius: Exactly 14.0000 studs (Outer Diameter = 28.0000 studs)
- Inner Queue Boundary Radius: Exactly 12.8000 studs (Inner Clear Diameter = 25.6000 studs)
- Radial Band Width: Exactly 1.2000 studs (R in [12.8000, 14.0000])
- Central Standing Area: 100% Unobstructed (0 vertices inside R_xz < 12.8000 studs)
- Local Origin / Pivot: (0.0000, 0.0000, 0.0000) at the center of the floor-level placement reference
  (Maps directly to World (0, 150, -300) at the approved plaza's top walking surface World Y = 150.0000)
- Vertical Profile & Z-Fighting Prevention:
  * Local Y_min = 0.0040 studs (4 mm non-coplanar clearance above Plaza Platform deck at Y = 0.0000 -> zero z-fighting)
  * Local Y_max = 0.0800 studs (Low-profile 0.0760-stud structural thickness / 0.0800-stud max elevation above deck)
  * Recessed Cyan Energy Channel at Y = 0.0360 studs (`0.0440 studs` recessed below bezel crest at Y = 0.0800)
  * Cardinal Threshold Crossing Ramps at Y = 0.0440 studs (`0.0400-stud` ultra-low bevel along +-Z and +-X)
- Radial Segmentation: 32 segments (11.25 deg per sector), matching SM_Hub_PlazaPlatform_01 1:1
- Coordinate Orientation: +Y Up, +Z Forward, +X Right (1.0 Unit = 1.0 Roblox Stud)

Usage:
  1. In Blender 3.6+ / 4.x (builds scene, saves .blend, and exports .obj/.mtl/.glb/.fbx):
     blender --background --python generate_hub_queue_pad_ring_blender.py -- --out_dir ./exports
  2. In standard Python 3 (builds deterministic .obj, .mtl, and .glb directly without requiring Blender):
     python3 generate_hub_queue_pad_ring_blender.py --out_dir ./exports
"""

import os
import sys
import io
import json
import math
import struct
import numpy as np
from PIL import Image, ImageDraw

try:
    import bpy
    import bmesh
    HAS_BPY = True
except ImportError:
    HAS_BPY = False

PALETTE_ORDER = [
    "MAT_DarkNeutral",
    "MAT_AltNeutral",
    "MAT_LightTrim",
    "EMI_Cyan",
]

PALETTE_SRGB = {
    "MAT_DarkNeutral": (32, 38, 54),     # #202636 — Primary structural collar & threshold base
    "MAT_AltNeutral":  (42, 50, 70),     # #2A3246 — Chamfered channel transition walls & intercardinal lock casings
    "MAT_LightTrim":   (170, 190, 215),  # #AABED7 — Precision inner/outer rim bezels & cardinal threshold bridge plates
    "EMI_Cyan":        (0, 195, 255),    # #00C3FF — Recessed segmented cyan boundary conduit & cardinal alignment diodes
}

PALETTE = {
    k: (v[0] / 255.0, v[1] / 255.0, v[2] / 255.0, 1.0)
    for k, v in PALETTE_SRGB.items()
}

APPROVED_PALETTE_METADATA = {
    "MAT_DarkNeutral": {
        "rgb_255": [32, 38, 54],
        "hex": "#202636",
        "normalized_rgb": [round(32/255.0, 6), round(38/255.0, 6), round(54/255.0, 6)],
        "emissive": False,
        "metallic": 0.55,
        "roughness": 0.42,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(32, 38, 54)",
        "surface_role": "Outer and inner low-profile chamfer skirts, structural collar ring decks, and base closure",
    },
    "MAT_AltNeutral": {
        "rgb_255": [42, 50, 70],
        "hex": "#2A3246",
        "normalized_rgb": [round(42/255.0, 6), round(50/255.0, 6), round(70/255.0, 6)],
        "emissive": False,
        "metallic": 0.60,
        "roughness": 0.35,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(42, 50, 70)",
        "surface_role": "Sloped channel walls, intercardinal structural lock casings, and cardinal threshold ramps",
    },
    "MAT_LightTrim": {
        "rgb_255": [170, 190, 215],
        "hex": "#AABED7",
        "normalized_rgb": [round(170/255.0, 6), round(190/255.0, 6), round(215/255.0, 6)],
        "emissive": False,
        "metallic": 0.78,
        "roughness": 0.28,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(170, 190, 215)",
        "surface_role": "Precision inner/outer boundary bezels, cardinal threshold bridge plates, and radial divider ribs",
    },
    "EMI_Cyan": {
        "rgb_255": [0, 195, 255],
        "hex": "#00C3FF",
        "normalized_rgb": [round(0/255.0, 6), round(195/255.0, 6), round(255/255.0, 6)],
        "emissive": True,
        "metallic": 0.10,
        "roughness": 0.15,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(0, 195, 255)",
        "surface_role": "Recessed segmented cyan boundary energy arcs and cardinal threshold alignment diodes",
    },
}


def build_palette_atlas_png_bytes():
    cell_px = 32
    img = Image.new("RGB", (cell_px * 2, cell_px * 2), (32, 38, 54))
    draw = ImageDraw.Draw(img)
    uv_centers_gltf = {}
    uv_centers_obj = {}

    for idx, mname in enumerate(PALETTE_ORDER):
        col_i = idx % 2
        row_i = idx // 2
        x0, y0 = col_i * cell_px, row_i * cell_px
        x1, y1 = x0 + cell_px - 1, y0 + cell_px - 1
        rgb = PALETTE_SRGB[mname]
        draw.rectangle([x0, y0, x1, y1], fill=rgb)

        u = (col_i + 0.5) / 2.0
        v_gltf = (row_i + 0.5) / 2.0
        v_obj = 1.0 - (row_i + 0.5) / 2.0
        uv_centers_gltf[mname] = (round(u, 5), round(v_gltf, 5))
        uv_centers_obj[mname] = (round(u, 5), round(v_obj, 5))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue(), uv_centers_gltf, uv_centers_obj


ATLAS_PNG_BYTES, UV_CENTERS_GLTF, UV_CENTERS_OBJ = build_palette_atlas_png_bytes()
ATLAS_FILENAME = "SphereBrawl_QueuePadRing_PaletteAtlas.png"


# ==============================================================================
# 2. DETERMINISTIC MULTI-COMPONENT MESH BUILDER
# ==============================================================================
class QueuePadRingMeshBuilder:
    def __init__(self, name="SM_Hub_QueuePadRing_01"):
        self.name = name
        self.comp_order = []
        self.comp_mat = {}
        self.comp_tris = {}

    def ensure_component(self, comp_name, mat_name):
        if comp_name not in self.comp_mat:
            self.comp_order.append(comp_name)
            self.comp_mat[comp_name] = mat_name
            self.comp_tris[comp_name] = []
        elif self.comp_mat[comp_name] != mat_name:
            raise ValueError(f"Component {comp_name} material mismatch: {self.comp_mat[comp_name]} vs {mat_name}")

    def add_tri(self, comp_name, mat_name, v0, v1, v2, expected_normal=None):
        self.ensure_component(comp_name, mat_name)
        p0 = np.round(np.array(v0, dtype=np.float64), 5)
        p1 = np.round(np.array(v1, dtype=np.float64), 5)
        p2 = np.round(np.array(v2, dtype=np.float64), 5)

        cross = np.cross(p1 - p0, p2 - p0)
        area = 0.5 * float(np.linalg.norm(cross))
        if area < 1e-6:
            raise ValueError(f"Degenerate triangle in {comp_name}: area={area}, pts={p0},{p1},{p2}")

        if expected_normal is not None:
            en = np.array(expected_normal, dtype=np.float64)
            if float(np.dot(cross, en)) < 0.0:
                p1, p2 = p2, p1

        self.comp_tris[comp_name].append((p0, p1, p2))

    def add_quad(self, comp_name, mat_name, v0, v1, v2, v3, expected_normal=None):
        self.add_tri(comp_name, mat_name, v0, v1, v2, expected_normal=expected_normal)
        self.add_tri(comp_name, mat_name, v0, v2, v3, expected_normal=expected_normal)

    def add_sector_ring_quad(self, comp_name, mat_name, r0, y0, r1, y1, theta0, theta1, normal_dir="up"):
        c0, s0 = math.cos(theta0), math.sin(theta0)
        c1, s1 = math.cos(theta1), math.sin(theta1)
        tm = 0.5 * (theta0 + theta1)
        cm, sm = math.cos(tm), math.sin(tm)

        p00 = (r0 * c0, y0, r0 * s0)
        p01 = (r0 * c1, y0, r0 * s1)
        p11 = (r1 * c1, y1, r1 * s1)
        p10 = (r1 * c0, y1, r1 * s0)

        # Compute exact outward normal from radial cross-section (dr = r1 - r0, dy = y1 - y0):
        # For an upper surface (normal_dir != "down"), the upward/radial normal has ny >= 0.
        if normal_dir == "down":
            en = (0.0, -1.0, 0.0)
        elif normal_dir == "up":
            en = (0.0, 1.0, 0.0)
        else:
            dr = r1 - r0
            dy = y1 - y0
            # Candidate normal perpendicular to (dr, dy) with positive Y component:
            if dr >= 0.0:
                nr = -dy
                ny = dr
            else:
                nr = dy
                ny = -dr
            en = (nr * cm, max(ny, 0.1), nr * sm)

        self.add_quad(comp_name, mat_name, p00, p01, p11, p10, expected_normal=en)

    def add_radial_cleat_module(self, comp_name, mat_name, r_in, r_out, half_w_in, half_w_out,
                                y_bot, y_top, theta_center, bevel_w=0.025):
        """Adds a precision-beveled radial clasp/divider rib across the ring channel."""
        ca, sa = math.cos(theta_center), math.sin(theta_center)
        def to_world(u, y, v):
            return (u * ca - v * sa, y, u * sa + v * ca)

        def n_world(nu, ny, nv):
            return (nu * ca - nv * sa, ny, nu * sa + nv * ca)

        b = min(bevel_w, 0.28 * min(half_w_in, half_w_out), 0.45 * (y_top - y_bot))
        ym = y_top - b

        # Top inset quad
        ti_l = to_world(r_in + b, y_top, -(half_w_in - b))
        ti_r = to_world(r_in + b, y_top,  (half_w_in - b))
        to_r = to_world(r_out - b, y_top, (half_w_out - b))
        to_l = to_world(r_out - b, y_top, -(half_w_out - b))

        # Mid shoulder quad
        mi_l = to_world(r_in, ym, -half_w_in)
        mi_r = to_world(r_in, ym,  half_w_in)
        mo_r = to_world(r_out, ym, half_w_out)
        mo_l = to_world(r_out, ym, -half_w_out)

        # Base quad
        bi_l = to_world(r_in, y_bot, -half_w_in)
        bi_r = to_world(r_in, y_bot,  half_w_in)
        bo_r = to_world(r_out, y_bot, half_w_out)
        bo_l = to_world(r_out, y_bot, -half_w_out)

        # Top face
        self.add_quad(comp_name, mat_name, ti_l, to_l, to_r, ti_r, expected_normal=n_world(0.0, 1.0, 0.0))
        # 4 top bevel faces
        self.add_quad(comp_name, mat_name, mi_l, mo_l, to_l, ti_l, expected_normal=n_world(0.0, 0.7, -0.7))
        self.add_quad(comp_name, mat_name, ti_r, to_r, mo_r, mi_r, expected_normal=n_world(0.0, 0.7, 0.7))
        self.add_quad(comp_name, mat_name, mi_l, ti_l, ti_r, mi_r, expected_normal=n_world(-0.7, 0.7, 0.0))
        self.add_quad(comp_name, mat_name, to_l, mo_l, mo_r, to_r, expected_normal=n_world(0.7, 0.7, 0.0))
        # 4 lower wall faces
        self.add_quad(comp_name, mat_name, bi_l, bo_l, mo_l, mi_l, expected_normal=n_world(0.0, 0.0, -1.0))
        self.add_quad(comp_name, mat_name, mi_r, mo_r, bo_r, bi_r, expected_normal=n_world(0.0, 0.0, 1.0))
        self.add_quad(comp_name, mat_name, bi_l, mi_l, mi_r, bi_r, expected_normal=n_world(-1.0, 0.0, 0.0))
        self.add_quad(comp_name, mat_name, mo_l, bo_l, bo_r, mo_r, expected_normal=n_world(1.0, 0.0, 0.0))

    def export_obj_and_mtl(self, obj_path, mtl_path):
        mtl_filename = os.path.basename(mtl_path)
        used_mats = [m for m in PALETTE_ORDER if m in set(self.comp_mat.values())]

        local_atlas_path = os.path.join(os.path.dirname(mtl_path), ATLAS_FILENAME)
        if not os.path.exists(local_atlas_path):
            with open(local_atlas_path, "wb") as af:
                af.write(ATLAS_PNG_BYTES)

        with open(mtl_path, "w", encoding="utf-8") as mf:
            mf.write("# Sphere Brawl: Rolling Rampage — Material Library\n")
            mf.write(f"# Asset: {self.name}\n")
            for mat_name in used_mats:
                rgba = PALETTE[mat_name]
                meta = APPROVED_PALETTE_METADATA[mat_name]
                mf.write(f"\nnewmtl {mat_name}\n")
                mf.write(f"Ka {rgba[0]*0.2:.4f} {rgba[1]*0.2:.4f} {rgba[2]*0.2:.4f}\n")
                mf.write(f"Kd {rgba[0]:.4f} {rgba[1]:.4f} {rgba[2]:.4f}\n")
                if meta["emissive"]:
                    mf.write(f"Ke {rgba[0]:.4f} {rgba[1]:.4f} {rgba[2]:.4f}\n")
                    mf.write("Ks 0.9000 0.9000 0.9000\nNs 90.0\n")
                else:
                    mf.write("Ke 0.0000 0.0000 0.0000\n")
                    mf.write("Ks 0.5500 0.6000 0.6800\nNs 50.0\n")
                mf.write("d 1.0\nillum 2\n")
                mf.write(f"map_Kd {ATLAS_FILENAME}\n")

        with open(obj_path, "w", encoding="utf-8") as of:
            of.write("# Sphere Brawl: Rolling Rampage — Kinetic Hub Queue Pad Ring 3D Asset\n")
            of.write(f"# Asset Name: {self.name}\n")
            of.write("# Unit Scale: 1.0 Unit = 1.0 Roblox Stud | Up Axis: +Y | Forward Axis: +Z\n")
            of.write("# Local Origin (0,0,0): Center of Queue Pad Ring Floor Reference (Maps to World (0, 150, -300))\n")
            of.write(f"mtllib {mtl_filename}\n")

            mat_to_vt_idx = {}
            for idx, m in enumerate(used_mats, 1):
                u_val, v_val = UV_CENTERS_OBJ[m]
                of.write(f"vt {u_val:.5f} {v_val:.5f}\n")
                mat_to_vt_idx[m] = idx

            v_idx = 1
            vn_idx = 1
            for comp_name in self.comp_order:
                tris = self.comp_tris[comp_name]
                if not tris:
                    continue
                mat_name = self.comp_mat[comp_name]
                rgba = PALETTE[mat_name]
                vt_i = mat_to_vt_idx[mat_name]
                of.write(f"o {comp_name}\n")
                of.write(f"g {comp_name}\n")
                of.write(f"usemtl {mat_name}\n")
                for (v0, v1, v2) in tris:
                    n = np.cross(v1 - v0, v2 - v0)
                    norm = float(np.linalg.norm(n))
                    n = (n / norm) if norm > 1e-8 else np.array([0.0, 1.0, 0.0])
                    for v in (v0, v1, v2):
                        of.write(
                            f"v {v[0]:.5f} {v[1]:.5f} {v[2]:.5f} "
                            f"{rgba[0]:.4f} {rgba[1]:.4f} {rgba[2]:.4f}\n"
                        )
                    of.write(f"vn {n[0]:.5f} {n[1]:.5f} {n[2]:.5f}\n")
                    of.write(
                        f"f {v_idx}/{vt_i}/{vn_idx} "
                        f"{v_idx+1}/{vt_i}/{vn_idx} "
                        f"{v_idx+2}/{vt_i}/{vn_idx}\n"
                    )
                    v_idx += 3
                    vn_idx += 1

    def export_glb(self, glb_path):
        used_mats = [m for m in PALETTE_ORDER if m in set(self.comp_mat.values())]
        mat_to_idx = {m: i for i, m in enumerate(used_mats)}

        buffer_bytes = bytearray()
        buffer_views = []
        accessors = []
        gltf_meshes = []
        child_node_indices = []

        img_offset = len(buffer_bytes)
        buffer_bytes.extend(ATLAS_PNG_BYTES)
        while len(buffer_bytes) % 4 != 0:
            buffer_bytes.append(0)
        bv_image = len(buffer_views)
        buffer_views.append({
            "buffer": 0,
            "byteOffset": img_offset,
            "byteLength": len(ATLAS_PNG_BYTES),
        })

        gltf_images = [{
            "name": "SphereBrawl_QueuePadRing_PaletteAtlas",
            "bufferView": bv_image,
            "mimeType": "image/png",
        }]
        gltf_samplers = [{
            "magFilter": 9728,
            "minFilter": 9728,
            "wrapS": 33071,
            "wrapT": 33071,
        }]
        gltf_textures = [{
            "name": "SphereBrawl_QueuePadRing_PaletteAtlas_Tex",
            "sampler": 0,
            "source": 0,
        }]

        gltf_materials = []
        for m in used_mats:
            rgba = PALETTE[m]
            meta = APPROVED_PALETTE_METADATA[m]
            mat_def = {
                "name": m,
                "pbrMetallicRoughness": {
                    "baseColorFactor": [round(rgba[0], 4), round(rgba[1], 4), round(rgba[2], 4), 1.0],
                    "baseColorTexture": {"index": 0, "texCoord": 0},
                    "metallicFactor": meta["metallic"],
                    "roughnessFactor": meta["roughness"],
                },
                "doubleSided": False,
            }
            if meta["emissive"]:
                mat_def["emissiveFactor"] = [round(rgba[0], 4), round(rgba[1], 4), round(rgba[2], 4)]
            gltf_materials.append(mat_def)

        def add_bv_and_acc(arr_bytes, target, comp_type, count, vtype, min_v=None, max_v=None):
            offset = len(buffer_bytes)
            buffer_bytes.extend(arr_bytes)
            while len(buffer_bytes) % 4 != 0:
                buffer_bytes.append(0)
            bv_i = len(buffer_views)
            bv_entry = {"buffer": 0, "byteOffset": offset, "byteLength": len(arr_bytes)}
            if target is not None:
                bv_entry["target"] = target
            buffer_views.append(bv_entry)
            acc_i = len(accessors)
            acc_entry = {
                "bufferView": bv_i,
                "byteOffset": 0,
                "componentType": comp_type,
                "count": count,
                "type": vtype,
            }
            if min_v is not None:
                acc_entry["min"] = min_v
            if max_v is not None:
                acc_entry["max"] = max_v
            accessors.append(acc_entry)
            return acc_i

        for comp_name in self.comp_order:
            tris = self.comp_tris[comp_name]
            if not tris:
                continue
            m = self.comp_mat[comp_name]
            mat_idx = mat_to_idx[m]
            rgba = PALETTE[m]
            u_val, v_val = UV_CENTERS_GLTF[m]

            pos_list = []
            norm_list = []
            uv_list = []
            col_list = []
            idx_list = []

            for i, (v0, v1, v2) in enumerate(tris):
                n = np.cross(v1 - v0, v2 - v0)
                nl = float(np.linalg.norm(n))
                n = (n / nl) if nl > 1e-8 else np.array([0.0, 1.0, 0.0])
                pos_list.extend([v0, v1, v2])
                norm_list.extend([n, n, n])
                uv_list.extend([[u_val, v_val], [u_val, v_val], [u_val, v_val]])
                col_list.extend([
                    [rgba[0], rgba[1], rgba[2], 1.0],
                    [rgba[0], rgba[1], rgba[2], 1.0],
                    [rgba[0], rgba[1], rgba[2], 1.0],
                ])
                idx_list.extend([3 * i, 3 * i + 1, 3 * i + 2])

            pos_arr = np.array(pos_list, dtype=np.float32)
            norm_arr = np.array(norm_list, dtype=np.float32)
            uv_arr = np.array(uv_list, dtype=np.float32)
            col_arr = np.array(col_list, dtype=np.float32)
            idx_arr = np.array(idx_list, dtype=np.uint32)

            acc_pos = add_bv_and_acc(
                pos_arr.tobytes(), 34962, 5126, len(pos_arr), "VEC3",
                [float(x) for x in pos_arr.min(axis=0)],
                [float(x) for x in pos_arr.max(axis=0)],
            )
            acc_norm = add_bv_and_acc(norm_arr.tobytes(), 34962, 5126, len(norm_arr), "VEC3")
            acc_uv = add_bv_and_acc(uv_arr.tobytes(), 34962, 5126, len(uv_arr), "VEC2")
            acc_col = add_bv_and_acc(col_arr.tobytes(), 34962, 5126, len(col_arr), "VEC4")
            acc_idx = add_bv_and_acc(idx_arr.tobytes(), 34963, 5125, len(idx_arr), "SCALAR")

            mesh_idx = len(gltf_meshes)
            gltf_meshes.append({
                "name": f"Mesh_{comp_name}",
                "primitives": [{
                    "attributes": {
                        "POSITION": acc_pos,
                        "NORMAL": acc_norm,
                        "TEXCOORD_0": acc_uv,
                        "COLOR_0": acc_col,
                    },
                    "indices": acc_idx,
                    "material": mat_idx,
                    "mode": 4,
                }],
            })
            child_node_indices.append((comp_name, mesh_idx))

        gltf_nodes = [{
            "name": self.name,
            "children": list(range(1, len(child_node_indices) + 1)),
        }]
        for comp_name, m_idx in child_node_indices:
            gltf_nodes.append({
                "name": comp_name,
                "mesh": m_idx,
            })

        gltf_dict = {
            "asset": {
                "version": "2.0",
                "generator": "Sphere Brawl Queue Pad Ring Pipeline v1.0 (Multi-Node + VertexColor + AtlasUV)",
            },
            "scene": 0,
            "scenes": [{"name": self.name, "nodes": [0]}],
            "nodes": gltf_nodes,
            "meshes": gltf_meshes,
            "materials": gltf_materials,
            "textures": gltf_textures,
            "images": gltf_images,
            "samplers": gltf_samplers,
            "accessors": accessors,
            "bufferViews": buffer_views,
            "buffers": [{"byteLength": len(buffer_bytes)}],
        }

        json_bytes = json.dumps(gltf_dict, separators=(",", ":")).encode("utf-8")
        while len(json_bytes) % 4 != 0:
            json_bytes += b" "

        total_len = 12 + 8 + len(json_bytes) + 8 + len(buffer_bytes)
        with open(glb_path, "wb") as f:
            f.write(struct.pack("<III", 0x46546C67, 2, total_len))
            f.write(struct.pack("<II", len(json_bytes), 0x4E4F534A))
            f.write(json_bytes)
            f.write(struct.pack("<II", len(buffer_bytes), 0x004E4942))
            f.write(buffer_bytes)


# ==============================================================================
# 3. PROCEDURAL GEOMETRY CONSTRUCTION FOR SM_Hub_QueuePadRing_01
# ==============================================================================
QUEUE_RING_PARAMS = {
    "asset_name": "SM_Hub_QueuePadRing_01",
    "outer_radius_studs": 14.0000,
    "outer_diameter_studs": 28.0000,
    "inner_radius_studs": 12.8000,
    "inner_diameter_studs": 25.6000,
    "band_width_studs": 1.2000,
    "max_xz_footprint_studs": [28.0000, 28.0000],
    "local_y_min_studs": 0.0040,
    "local_y_max_studs": 0.0800,
    "structural_thickness_studs": 0.0760,
    "max_height_above_deck_studs": 0.0800,
    "recessed_cyan_channel_y_studs": 0.0360,
    "cardinal_threshold_top_y_studs": 0.0440,
    "reference_walking_surface_local_y": 0.0000,
    "reference_walking_surface_world_y": 150.0000,
    "world_pivot_position": [0.0, 150.0, -300.0],
    "radial_segments": 32,
    "portal_arch_min_floor_radius_studs": 15.0500,
    "portal_arch_radial_clearance_studs": 1.0500,
    "plaza_inner_framing_ring_radius_studs": 21.2000,
    "plaza_framing_ring_clearance_studs": 7.2000,
}


def build_hub_queue_pad_ring():
    """
    Constructs SM_Hub_QueuePadRing_01 with 4 material-separated child components:
      1. GEO_QueuePadRing_BaseCollar  (MAT_DarkNeutral) — Outer R=14.0000 and Inner R=12.8000 chamfered collar & base frame
      2. GEO_QueuePadRing_ChannelInlay (MAT_AltNeutral)  — Sloped channel transition walls, intercardinal lock casings & threshold ramps
      3. GEO_QueuePadRing_TrimBezels   (MAT_LightTrim)   — Precision inner/outer rim bezels, cardinal threshold bridge plates & radial ribs
      4. GEO_QueuePadRing_CyanConduit  (EMI_Cyan)        — Recessed segmented cyan boundary conduit & cardinal entry alignment diodes
    """
    mb = QueuePadRingMeshBuilder("SM_Hub_QueuePadRing_01")

    mb.ensure_component("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral")
    mb.ensure_component("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral")
    mb.ensure_component("GEO_QueuePadRing_TrimBezels", "MAT_LightTrim")
    mb.ensure_component("GEO_QueuePadRing_CyanConduit", "EMI_Cyan")

    N = 32
    thetas = [2.0 * math.pi * i / N for i in range(N + 1)]

    cardinal_threshold_sectors = {31, 0, 7, 8, 15, 16, 23, 24}
    intercardinal_lock_sectors = {3, 4, 11, 12, 19, 20, 27, 28}

    # Radial profile (R in [12.8000, 14.0000], total width = 1.2000 studs):
    r0 = 12.8000  # Exact inner boundary radius (Diameter = 25.6000 studs; 100% open central standing area)
    r1 = 12.9000  # Inner low-angle chamfer toe -> shoulder (MAT_DarkNeutral)
    r2 = 13.0600  # Inner structural collar flat (MAT_DarkNeutral)
    r3 = 13.1800  # Inner metallic bezel flat (MAT_LightTrim)
    r4 = 13.2600  # Inner channel bevel wall (MAT_AltNeutral)
    r5 = 13.5400  # Outer edge of recessed cyan boundary channel (EMI_Cyan in [13.26, 13.54], width = 0.28 studs)
    r6 = 13.6200  # Outer channel bevel wall (MAT_AltNeutral)
    r7 = 13.7400  # Outer metallic bezel flat (MAT_LightTrim)
    r8 = 13.9000  # Outer structural collar flat (MAT_DarkNeutral)
    r9 = 14.0000  # Exact outer boundary radius (Diameter = 28.0000 studs; TASK-03 & GameConfig.Lobby.QueuePadRadius = 14)

    # Elevations (Local Y in [0.0040, 0.0800], zero coplanar overlap with Plaza Platform at Y = 0.0000):
    y_base = 0.0040       # 4 mm non-coplanar offset above Plaza Platform top deck (Y = 0.0000)
    y_collar = 0.0680     # Dark-neutral structural collar deck elevation
    y_chan = 0.0360       # Recessed cyan energy channel elevation (44 mm below bezel crest)
    y_thresh = 0.0440     # Cardinal walk-through threshold bridge elevation
    y_lock = 0.0740       # Intercardinal structural lock plate elevation
    y_crest = 0.0800      # Main inner/outer bezel crest elevation (80 mm = 0.08 studs max height)

    for i in range(N):
        t0, t1 = thetas[i], thetas[i + 1]

        if i in cardinal_threshold_sectors:
            # --- CARDINAL THRESHOLD CROSSING SECTORS (+Z, -Z, +X, -X) ---
            # Gentle walk-through ramp profile (max height 0.0440 studs) marking the 4 cardinal entry/exit gates
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r0, y_base, r1, y_thresh, t0, t1, "up_in")
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r1, y_thresh, r2, y_thresh, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral", r2, y_thresh, r3, y_thresh, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_TrimBezels", "MAT_LightTrim", r3, y_thresh, r4, y_thresh, t0, t1, "up")
            # Recessed cardinal alignment diode strip (centered at R = 13.40)
            mb.add_sector_ring_quad("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral", r4, y_thresh, 13.3400, y_chan, t0, t1, "up_out")
            mb.add_sector_ring_quad("GEO_QueuePadRing_CyanConduit", "EMI_Cyan", 13.3400, y_chan, 13.4600, y_chan, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral", 13.4600, y_chan, r5, y_thresh, t0, t1, "up_in")
            mb.add_sector_ring_quad("GEO_QueuePadRing_TrimBezels", "MAT_LightTrim", r5, y_thresh, r6, y_thresh, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral", r6, y_thresh, r7, y_thresh, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r7, y_thresh, r8, y_thresh, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r8, y_thresh, r9, y_base, t0, t1, "up_out")

        elif i in intercardinal_lock_sectors:
            # --- INTERCARDINAL STRUCTURAL LOCK SECTORS (45, 135, 225, 315 deg) ---
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r0, y_base, r1, y_collar, t0, t1, "up_in")
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r1, y_collar, r2, y_collar, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_TrimBezels", "MAT_LightTrim", r2, y_collar, r3, y_crest, t0, t1, "up_in")
            mb.add_sector_ring_quad("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral", r3, y_crest, r4, y_chan, t0, t1, "up_out")
            mb.add_sector_ring_quad("GEO_QueuePadRing_CyanConduit", "EMI_Cyan", r4, y_chan, r5, y_chan, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral", r5, y_chan, r6, y_lock, t0, t1, "up_in")
            mb.add_sector_ring_quad("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral", r6, y_lock, r7, y_lock, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r7, y_lock, r8, y_collar, t0, t1, "up_out")
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r8, y_collar, r9, y_base, t0, t1, "up_out")

        else:
            # --- MAIN RECESSED BOUNDARY CONDUIT SECTORS ---
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r0, y_base, r1, y_collar, t0, t1, "up_in")
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r1, y_collar, r2, y_collar, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_TrimBezels", "MAT_LightTrim", r2, y_collar, r3, y_crest, t0, t1, "up_in")
            mb.add_sector_ring_quad("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral", r3, y_crest, r4, y_chan, t0, t1, "up_out")
            mb.add_sector_ring_quad("GEO_QueuePadRing_CyanConduit", "EMI_Cyan", r4, y_chan, r5, y_chan, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral", r5, y_chan, r6, y_crest, t0, t1, "up_in")
            mb.add_sector_ring_quad("GEO_QueuePadRing_TrimBezels", "MAT_LightTrim", r6, y_crest, r7, y_collar, t0, t1, "up_out")
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r7, y_collar, r8, y_collar, t0, t1, "up")
            mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r8, y_collar, r9, y_base, t0, t1, "up_out")

        # Bottom structural closure face (r0 -> r9 at y_base = 0.0040, normal pointing -Y)
        mb.add_sector_ring_quad("GEO_QueuePadRing_BaseCollar", "MAT_DarkNeutral", r9, y_base, r0, y_base, t0, t1, "down")

    # Add 16 precision radial divider ribs / clasps around the ring
    rib_sector_indices = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
    for s_idx in rib_sector_indices:
        ang = thetas[s_idx]
        is_threshold_edge = s_idx in {1, 7, 9, 15, 17, 23, 25, 31}
        if is_threshold_edge:
            # Precision light-metal clasp framing each cardinal threshold gate
            mb.add_radial_cleat_module(
                "GEO_QueuePadRing_TrimBezels", "MAT_LightTrim",
                r_in=12.9200, r_out=13.8800,
                half_w_in=0.1400, half_w_out=0.1600,
                y_bot=0.0120, y_top=0.0780,
                theta_center=ang, bevel_w=0.018,
            )
        else:
            # Dark-slate segmentation bridge dividing the cyan conduit into crisp arc segments
            mb.add_radial_cleat_module(
                "GEO_QueuePadRing_ChannelInlay", "MAT_AltNeutral",
                r_in=13.1200, r_out=13.6800,
                half_w_in=0.1100, half_w_out=0.1250,
                y_bot=0.0120, y_top=0.0740,
                theta_center=ang, bevel_w=0.015,
            )

    return mb


def rblx_to_blender(pt):
    """
    Maps Roblox local coordinates (X_right, Y_up, Z_forward) -> Blender (X_right, -Z_forward, Y_up)
    so Blender's Z-up viewport and glTF/OBJ (+Y Up) exporters preserve 1:1 Roblox orientation.
    """
    return (float(pt[0]), float(-pt[2]), float(pt[1]))


def srgb_to_linear(c):
    v = c / 255.0
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def build_in_blender(mb, save_blend_path=None):
    if not HAS_BPY:
        raise RuntimeError("Blender bpy module is not available in this Python environment.")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0

    col = bpy.data.collections.new("SM_Hub_QueuePadRing_01")
    bpy.context.scene.collection.children.link(col)

    b_mats = {}
    for mname in PALETTE_ORDER:
        rgb = PALETTE_SRGB[mname]
        meta = APPROVED_PALETTE_METADATA[mname]
        mat = bpy.data.materials.new(name=mname)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        lin = (srgb_to_linear(rgb[0]), srgb_to_linear(rgb[1]), srgb_to_linear(rgb[2]), 1.0)
        if bsdf:
            bsdf.inputs["Base Color"].default_value = lin
            bsdf.inputs["Metallic"].default_value = meta["metallic"]
            bsdf.inputs["Roughness"].default_value = meta["roughness"]
            if meta["emissive"]:
                if "Emission Color" in bsdf.inputs:
                    bsdf.inputs["Emission Color"].default_value = lin
                    bsdf.inputs["Emission Strength"].default_value = 4.0
                elif "Emission" in bsdf.inputs:
                    bsdf.inputs["Emission"].default_value = lin
        b_mats[mname] = mat

    root_empty = bpy.data.objects.new("SM_Hub_QueuePadRing_01", None)
    root_empty.empty_display_type = "ARROWS"
    root_empty.empty_display_size = 2.0
    col.objects.link(root_empty)

    for comp_name in mb.comp_order:
        tris = mb.comp_tris[comp_name]
        mname = mb.comp_mat[comp_name]
        mesh = bpy.data.meshes.new(comp_name)
        obj = bpy.data.objects.new(comp_name, mesh)
        obj.parent = root_empty
        col.objects.link(obj)

        bm = bmesh.new()
        for (v0, v1, v2) in tris:
            verts = [bm.verts.new(rblx_to_blender(p)) for p in (v0, v1, v2)]
            bm.faces.new(verts)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
        obj.data.materials.append(b_mats[mname])

    if save_blend_path:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(save_blend_path))


if __name__ == "__main__":
    out_dir = "./exports"
    if "--out_dir" in sys.argv:
        idx = sys.argv.index("--out_dir")
        if idx + 1 < len(sys.argv):
            out_dir = sys.argv[idx + 1]
    os.makedirs(out_dir, exist_ok=True)

    mb = build_hub_queue_pad_ring()

    obj_out = os.path.join(out_dir, "SM_Hub_QueuePadRing_01.obj")
    mtl_out = os.path.join(out_dir, "SM_Hub_QueuePadRing_01.mtl")
    glb_out = os.path.join(out_dir, "SM_Hub_QueuePadRing_01.glb")
    mb.export_obj_and_mtl(obj_out, mtl_out)
    mb.export_glb(glb_out)

    if HAS_BPY:
        blend_out = os.path.join(out_dir, "SM_Hub_QueuePadRing_01.blend")
        build_in_blender(mb, save_blend_path=blend_out)
        print(f"Saved Blender source to {blend_out}")

    total_tris = sum(len(t) for t in mb.comp_tris.values())
    print(f"Successfully generated SM_Hub_QueuePadRing_01 in {out_dir} ({total_tris} triangles).")
