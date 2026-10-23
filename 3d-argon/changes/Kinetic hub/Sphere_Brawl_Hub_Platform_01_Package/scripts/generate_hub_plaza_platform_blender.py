#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — DETERMINISTIC BLENDER 3.6+ / 4.x & PYTHON GENERATOR
Asset ID: SM_Hub_PlazaPlatform_01 (Main Kinetic Hub Platform — Argon Step 1)
===================================================================================
- Outer Diameter: Exactly 140.0000 studs (R_outer = 70.0000 studs)
- Maximum XZ Footprint: 140.0000 x 140.0000 studs (X in [-70.0, +70.0], Z in [-70.0, +70.0])
- Local Origin / Pivot: (0.0000, 0.0000, 0.0000) at the center of the top walking surface
- Top Walking Surface Elevation: Local Y = 0.0000 -> World Y = 150.0000 when placed at (0, 150, -300)
- Total Structural Thickness: 12.0000 studs (Local Y in [-12.0000, 0.0000] -> World Y in [138.0, 150.0])
- Coordinate Orientation: +Y Up, +Z Forward, +X Right (1.0 Unit = 1.0 Roblox Stud)

Usage:
  1. In Blender 3.6+ / 4.x (builds scene, saves .blend, and exports .obj/.mtl/.glb/.fbx):
     blender --background --python generate_hub_plaza_platform_blender.py -- --out_dir ./exports
  2. In standard Python 3 (builds deterministic .obj, .mtl, and .glb directly without requiring Blender):
     python3 generate_hub_plaza_platform_blender.py --out_dir ./exports
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
    "MAT_DarkNeutral": (32, 38, 54),     # #202636 — Main deck and primary structural body (~70%)
    "MAT_AltNeutral":  (42, 50, 70),     # #2A3246 — Secondary armor plates and inset structural layers
    "MAT_LightTrim":   (170, 190, 215),  # #AABED7 — Select metallic highlights, bevels and hardware
    "EMI_Cyan":        (0, 195, 255),    # #00C3FF — Recessed energy accents and restrained status details
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
        "surface_role": "Main walking deck, outer load-bearing rim hull, and tapered lower keel shell",
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
        "surface_role": "Secondary deck panel inlays, stepped mid-hull structural bays, and radial underside box-girders",
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
        "surface_role": "Precision-machined rim bevels, perimeter mounting brackets, tie cleats, and truss gussets",
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
        "surface_role": "Recessed top-deck framing conduits, outer rim status channels, and underside bay diagnostic strips",
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
ATLAS_FILENAME = "SphereBrawl_HubPlatform_PaletteAtlas.png"
# Palette atlas PNG bytes generated in memory


# ==============================================================================
# 2. DETERMINISTIC MULTI-COMPONENT MESH BUILDER
# ==============================================================================
class HubPlatformMeshBuilder:
    def __init__(self, name="SM_Hub_PlazaPlatform_01"):
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

        if normal_dir == "up":
            en = (0.0, 1.0, 0.0)
        elif normal_dir == "down":
            en = (0.0, -1.0, 0.0)
        elif normal_dir == "out":
            en = (cm, 0.0, sm)
        elif normal_dir == "in":
            en = (-cm, 0.0, -sm)
        elif normal_dir == "up_out":
            en = (cm * 0.7, 0.7, sm * 0.7)
        elif normal_dir == "up_in":
            en = (-cm * 0.7, 0.7, -sm * 0.7)
        elif normal_dir == "down_out":
            en = (cm * 0.7, -0.7, sm * 0.7)
        elif normal_dir == "down_in":
            en = (-cm * 0.7, -0.7, -sm * 0.7)
        else:
            en = normal_dir

        self.add_quad(comp_name, mat_name, p00, p01, p11, p10, expected_normal=en)

    def add_radial_box_module(self, comp_name, mat_name, r_in, r_out, half_w_in, half_w_out,
                              y_bot_in, y_bot_out, y_top_in, y_top_out, theta_center,
                              bevel_w=0.18, include_top=False, include_bottom=True,
                              include_inner_cap=True, include_outer_cap=True):
        ca, sa = math.cos(theta_center), math.sin(theta_center)
        def to_world(u, y, v):
            return (u * ca - v * sa, y, u * sa + v * ca)

        def n_world(nu, ny, nv):
            return (nu * ca - nv * sa, ny, nu * sa + nv * ca)

        b = min(bevel_w, 0.3 * min(half_w_in, half_w_out))
        bi_l = to_world(r_in, y_bot_in, -(half_w_in - b))
        bi_r = to_world(r_in, y_bot_in,  (half_w_in - b))
        bo_r = to_world(r_out, y_bot_out, (half_w_out - b))
        bo_l = to_world(r_out, y_bot_out, -(half_w_out - b))

        sbi_l = to_world(r_in, y_bot_in + b, -half_w_in)
        sbi_r = to_world(r_in, y_bot_in + b,  half_w_in)
        sbo_r = to_world(r_out, y_bot_out + b, half_w_out)
        sbo_l = to_world(r_out, y_bot_out + b, -half_w_out)

        ti_l = to_world(r_in, y_top_in, -half_w_in)
        ti_r = to_world(r_in, y_top_in,  half_w_in)
        to_r = to_world(r_out, y_top_out, half_w_out)
        to_l = to_world(r_out, y_top_out, -half_w_out)

        if include_bottom:
            self.add_quad(comp_name, mat_name, bi_l, bi_r, bo_r, bo_l, expected_normal=n_world(0.15, -1.0, 0.0))
            self.add_quad(comp_name, mat_name, bi_l, bo_l, sbo_l, sbi_l, expected_normal=n_world(0.0, -0.7, -0.7))
            self.add_quad(comp_name, mat_name, bi_r, sbi_r, sbo_r, bo_r, expected_normal=n_world(0.0, -0.7, 0.7))
        else:
            sbi_l, sbi_r, sbo_r, sbo_l = bi_l, bi_r, bo_r, bo_l

        self.add_quad(comp_name, mat_name, sbi_l, sbo_l, to_l, ti_l, expected_normal=n_world(0.0, 0.0, -1.0))
        self.add_quad(comp_name, mat_name, sbi_r, ti_r, to_r, sbo_r, expected_normal=n_world(0.0, 0.0, 1.0))

        if include_top:
            self.add_quad(comp_name, mat_name, ti_l, to_l, to_r, ti_r, expected_normal=n_world(0.0, 1.0, 0.0))

        if include_inner_cap:
            self.add_quad(comp_name, mat_name, sbi_l, ti_l, ti_r, sbi_r, expected_normal=n_world(-1.0, 0.0, 0.0))
            if include_bottom:
                self.add_quad(comp_name, mat_name, bi_l, sbi_l, sbi_r, bi_r, expected_normal=n_world(-1.0, -0.3, 0.0))

        if include_outer_cap:
            self.add_quad(comp_name, mat_name, sbo_l, sbo_r, to_r, to_l, expected_normal=n_world(1.0, 0.0, 0.0))
            if include_bottom:
                self.add_quad(comp_name, mat_name, bo_l, bo_r, sbo_r, sbo_l, expected_normal=n_world(1.0, -0.3, 0.0))

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
            of.write("# Sphere Brawl: Rolling Rampage — Main Kinetic Hub Platform 3D Asset\n")
            of.write(f"# Asset Name: {self.name}\n")
            of.write("# Unit Scale: 1.0 Unit = 1.0 Roblox Stud | Up Axis: +Y | Forward Axis: +Z\n")
            of.write("# Local Origin (0,0,0): Center of Top Walking Surface (Maps to World (0, 150, -300))\n")
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
            "name": "SphereBrawl_HubPlatform_PaletteAtlas",
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
            "name": "SphereBrawl_HubPlatform_PaletteAtlas_Tex",
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
                "generator": "Sphere Brawl Hub Platform Pipeline v1.0 (Multi-Node + VertexColor + AtlasUV)",
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
# 3. PROCEDURAL GEOMETRY CONSTRUCTION FOR SM_Hub_PlazaPlatform_01
# ==============================================================================
PLATFORM_PARAMS = {
    "asset_name": "SM_Hub_PlazaPlatform_01",
    "outer_diameter_studs": 140.0,
    "outer_radius_studs": 70.0,
    "max_xz_footprint_studs": [140.0, 140.0],
    "top_walking_surface_local_y": 0.0,
    "top_walking_surface_world_y": 150.0,
    "world_pivot_position": [0.0, 150.0, -300.0],
    "total_thickness_studs": 12.0,
    "local_y_bounds": [-12.0, 0.0],
    "radial_segments": 32,
    "buttress_count": 8,
    "underside_rib_count": 8,
    "queue_pad_clear_radius_studs": 14.0,
    "portal_arch_clearance_radius_studs": 21.2,
}


def build_hub_plaza_platform():
    mb = HubPlatformMeshBuilder("SM_Hub_PlazaPlatform_01")

    mb.ensure_component("GEO_PlazaPlatform_Deck", "MAT_DarkNeutral")
    mb.ensure_component("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral")
    mb.ensure_component("GEO_PlazaPlatform_Rim", "MAT_DarkNeutral")
    mb.ensure_component("GEO_PlazaPlatform_Structure", "MAT_AltNeutral")
    mb.ensure_component("GEO_PlazaPlatform_Underside", "MAT_DarkNeutral")
    mb.ensure_component("GEO_PlazaPlatform_Trim", "MAT_LightTrim")
    mb.ensure_component("GEO_PlazaPlatform_CyanAccents", "EMI_Cyan")

    N = 32
    thetas = [2.0 * math.pi * i / N for i in range(N + 1)]

    cardinal_sectors = {0, 31, 7, 8, 15, 16, 23, 24}
    primary_walkway_sectors = {0, 8, 16, 24}
    diagonal_station_sectors = {4, 12, 20, 28}
    buttress_sectors = {0, 4, 8, 12, 16, 20, 24, 28}

    for i in range(N):
        t0, t1 = thetas[i], thetas[i + 1]
        c0, s0 = math.cos(t0), math.sin(t0)
        c1, s1 = math.cos(t1), math.sin(t1)

        # A. TOP WALKING DECK (Local Y = 0.0000, R = 0.00 to 65.80 studs)
        r_c1 = 6.50
        mb.add_tri(
            "GEO_PlazaPlatform_Deck", "MAT_DarkNeutral",
            (0.0, 0.0, 0.0),
            (r_c1 * c0, 0.0, r_c1 * s0),
            (r_c1 * c1, 0.0, r_c1 * s1),
            expected_normal=(0.0, 1.0, 0.0),
        )
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Deck", "MAT_DarkNeutral", 6.50, 0.0, 14.00, 0.0, t0, t1, "up")

        if i in diagonal_station_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 14.00, 0.0, 21.20, 0.0, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Deck", "MAT_DarkNeutral", 14.00, 0.0, 21.20, 0.0, t0, t1, "up")

        # Inner Plaza Framing Ring & Recessed Cyan Conduit (R = 21.20 to 23.00, outside R=20.48 Portal Pylons)
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 21.20, 0.0, 21.55, 0.0, t0, t1, "up")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 21.55, 0.0, 21.65, -0.06, t0, t1, "up_out")
        if i in primary_walkway_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 21.65, -0.06, 22.55, -0.06, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_CyanAccents", "EMI_Cyan", 21.65, -0.06, 22.55, -0.06, t0, t1, "up")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 22.55, -0.06, 22.65, 0.0, t0, t1, "up_in")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 22.65, 0.0, 23.00, 0.0, t0, t1, "up")

        if i in cardinal_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 23.00, 0.0, 29.50, 0.0, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Deck", "MAT_DarkNeutral", 23.00, 0.0, 29.50, 0.0, t0, t1, "up")

        if i in buttress_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 29.50, 0.0, 36.20, 0.0, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Deck", "MAT_DarkNeutral", 29.50, 0.0, 36.20, 0.0, t0, t1, "up")

        if i in buttress_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 36.20, 0.0, 37.00, 0.0, t0, t1, "up")
        elif (i % 4) == 2:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_CyanAccents", "EMI_Cyan", 36.20, 0.0, 37.00, 0.0, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 36.20, 0.0, 37.00, 0.0, t0, t1, "up")

        if i in cardinal_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 37.00, 0.0, 44.50, 0.0, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Deck", "MAT_DarkNeutral", 37.00, 0.0, 44.50, 0.0, t0, t1, "up")

        if i in diagonal_station_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 44.50, 0.0, 52.50, 0.0, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Deck", "MAT_DarkNeutral", 44.50, 0.0, 52.50, 0.0, t0, t1, "up")

        if i in primary_walkway_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 52.50, 0.0, 63.20, 0.0, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Deck", "MAT_DarkNeutral", 52.50, 0.0, 63.20, 0.0, t0, t1, "up")

        # Outer Deck Curb Bezel & Recessed Perimeter Energy Channel (R = 63.20 to 65.80)
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 63.20, 0.0, 63.75, 0.0, t0, t1, "up")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 63.75, 0.0, 63.95, -0.18, t0, t1, "up_out")
        if i in buttress_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 63.95, -0.18, 65.15, -0.18, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_CyanAccents", "EMI_Cyan", 63.95, -0.18, 65.15, -0.18, t0, t1, "up")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_DeckInlays", "MAT_AltNeutral", 65.15, -0.18, 65.35, 0.0, t0, t1, "up_in")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 65.35, 0.0, 65.80, 0.0, t0, t1, "up")

        # B. OUTER STRUCTURAL RIM & SIDEWALL (R = 65.80 to 70.0000, Y = 0.0 to -6.20)
        if i in buttress_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Structure", "MAT_AltNeutral", 65.80, 0.0, 68.80, 0.0, t0, t1, "up")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Rim", "MAT_DarkNeutral", 65.80, 0.0, 68.80, 0.0, t0, t1, "up")

        if i in buttress_sectors:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 68.80, 0.0, 70.00, -1.20, t0, t1, "up_out")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Rim", "MAT_DarkNeutral", 68.80, 0.0, 70.00, -1.20, t0, t1, "up_out")

        mb.add_sector_ring_quad("GEO_PlazaPlatform_Rim", "MAT_DarkNeutral", 70.00, -1.20, 70.00, -3.40, t0, t1, "out")

        mb.add_sector_ring_quad("GEO_PlazaPlatform_Structure", "MAT_AltNeutral", 70.00, -3.40, 69.25, -3.75, t0, t1, "down_out")
        if (i % 2) == 1:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_CyanAccents", "EMI_Cyan", 69.25, -3.75, 69.25, -4.65, t0, t1, "out")
        elif (i % 4) == 0:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 69.25, -3.75, 69.25, -4.65, t0, t1, "out")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Structure", "MAT_AltNeutral", 69.25, -3.75, 69.25, -4.65, t0, t1, "out")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Structure", "MAT_AltNeutral", 69.25, -4.65, 69.85, -5.00, t0, t1, "up_out")

        mb.add_sector_ring_quad("GEO_PlazaPlatform_Rim", "MAT_DarkNeutral", 69.85, -5.00, 68.20, -6.20, t0, t1, "down_out")

        # C. STEPPED MID-HULL & TAPERED UNDERSIDE SHELL (Y = -6.20 down to -12.00)
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Underside", "MAT_DarkNeutral", 68.20, -6.20, 61.00, -6.50, t0, t1, "down_out")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Structure", "MAT_AltNeutral", 61.00, -6.50, 56.00, -7.60, t0, t1, "down_out")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Underside", "MAT_DarkNeutral", 56.00, -7.60, 38.00, -8.90, t0, t1, "down_out")

        if (i % 2) == 1:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_CyanAccents", "EMI_Cyan", 38.00, -8.90, 34.50, -9.60, t0, t1, "down_out")
        else:
            mb.add_sector_ring_quad("GEO_PlazaPlatform_Trim", "MAT_LightTrim", 38.00, -8.90, 34.50, -9.60, t0, t1, "down_out")

        mb.add_sector_ring_quad("GEO_PlazaPlatform_Underside", "MAT_DarkNeutral", 34.50, -9.60, 22.00, -12.00, t0, t1, "down_out")
        mb.add_sector_ring_quad("GEO_PlazaPlatform_Structure", "MAT_AltNeutral", 22.00, -12.00, 10.50, -12.00, t0, t1, "down")

        mb.add_tri(
            "GEO_PlazaPlatform_Underside", "MAT_DarkNeutral",
            (0.0, -12.00, 0.0),
            (10.50 * c1, -12.00, 10.50 * s1),
            (10.50 * c0, -12.00, 10.50 * s0),
            expected_normal=(0.0, -1.0, 0.0),
        )

    # D. 3D INTEGRATED UNDERSIDE RADIAL BOX-GIRDERS & PERIMETER BRACKETS
    for b_idx in range(8):
        ang = b_idx * (2.0 * math.pi / 8.0) + (math.pi / N)
        mb.add_radial_box_module(
            "GEO_PlazaPlatform_Structure", "MAT_AltNeutral",
            r_in=21.50, r_out=64.50,
            half_w_in=1.55, half_w_out=2.10,
            y_bot_in=-11.92, y_bot_out=-8.60,
            y_top_in=-9.40, y_top_out=-6.20,
            theta_center=ang,
            bevel_w=0.26,
            include_top=True, include_bottom=True,
            include_inner_cap=True, include_outer_cap=True,
        )
        mb.add_radial_box_module(
            "GEO_PlazaPlatform_Trim", "MAT_LightTrim",
            r_in=60.50, r_out=67.60,
            half_w_in=1.15, half_w_out=1.35,
            y_bot_in=-9.05, y_bot_out=-7.45,
            y_top_in=-6.50, y_top_out=-6.20,
            theta_center=ang,
            bevel_w=0.16,
            include_top=True, include_bottom=True,
            include_inner_cap=True, include_outer_cap=True,
        )

    for k_idx in range(16):
        ang = k_idx * (2.0 * math.pi / 16.0) + (math.pi / N)
        mb.add_radial_box_module(
            "GEO_PlazaPlatform_Trim", "MAT_LightTrim",
            r_in=68.55, r_out=69.92,
            half_w_in=0.68, half_w_out=0.62,
            y_bot_in=-3.55, y_bot_out=-3.35,
            y_top_in=-0.15, y_top_out=-1.15,
            theta_center=ang,
            bevel_w=0.10,
            include_top=True, include_bottom=True,
            include_inner_cap=True, include_outer_cap=True,
        )

    return mb


def build_collision_proxy_mesh():
    cb = HubPlatformMeshBuilder("COL_PlazaPlatform_Deck")
    cb.ensure_component("COL_PlazaPlatform_Deck", "MAT_DarkNeutral")
    N = 32
    thetas = [2.0 * math.pi * i / N for i in range(N + 1)]
    R = 70.00
    y_top = 0.00
    y_bot = -2.00
    for i in range(N):
        t0, t1 = thetas[i], thetas[i + 1]
        c0, s0 = math.cos(t0), math.sin(t0)
        c1, s1 = math.cos(t1), math.sin(t1)
        cb.add_tri("COL_PlazaPlatform_Deck", "MAT_DarkNeutral", (0.0, y_top, 0.0), (R * c0, y_top, R * s0), (R * c1, y_top, R * s1), expected_normal=(0.0, 1.0, 0.0))
        cb.add_tri("COL_PlazaPlatform_Deck", "MAT_DarkNeutral", (0.0, y_bot, 0.0), (R * c1, y_bot, R * s1), (R * c0, y_bot, R * s0), expected_normal=(0.0, -1.0, 0.0))
        cb.add_sector_ring_quad("COL_PlazaPlatform_Deck", "MAT_DarkNeutral", R, y_top, R, y_bot, t0, t1, "out")
    return cb




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

    col = bpy.data.collections.new("SM_Hub_PlazaPlatform_01")
    bpy.context.scene.collection.children.link(col)

    # Create Principled BSDF materials matching the locked Sphere Brawl palette
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

    root_empty = bpy.data.objects.new("SM_Hub_PlazaPlatform_01", None)
    root_empty.empty_display_type = "ARROWS"
    root_empty.empty_display_size = 5.0
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

    mb = build_hub_plaza_platform()
    cb = build_collision_proxy_mesh()

    obj_out = os.path.join(out_dir, "SM_Hub_PlazaPlatform_01.obj")
    mtl_out = os.path.join(out_dir, "SM_Hub_PlazaPlatform_01.mtl")
    glb_out = os.path.join(out_dir, "SM_Hub_PlazaPlatform_01.glb")
    mb.export_obj_and_mtl(obj_out, mtl_out)
    mb.export_glb(glb_out)

    col_dir = os.path.join(out_dir, "collision_proxy")
    os.makedirs(col_dir, exist_ok=True)
    cb.export_obj_and_mtl(os.path.join(col_dir, "COL_PlazaPlatform_Deck.obj"), os.path.join(col_dir, "COL_PlazaPlatform_Deck.mtl"))
    cb.export_glb(os.path.join(col_dir, "COL_PlazaPlatform_Deck.glb"))

    if HAS_BPY:
        blend_out = os.path.join(out_dir, "SM_Hub_PlazaPlatform_01.blend")
        build_in_blender(mb, save_blend_path=blend_out)
        print(f"Saved Blender source to {blend_out}")

    print(f"Successfully generated SM_Hub_PlazaPlatform_01 in {out_dir} ({sum(len(t) for t in mb.comp_tris.values())} triangles).")
