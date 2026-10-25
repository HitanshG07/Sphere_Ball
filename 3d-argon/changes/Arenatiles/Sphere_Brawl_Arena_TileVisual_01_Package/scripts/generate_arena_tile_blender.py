#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — DETERMINISTIC BLENDER 3.6+ / 4.x & PYTHON PRODUCTION GENERATOR
Asset ID: SM_Arena_TileVisual_01 (Modular Arena Tile & Hazard Visual System — Phase 2 Final Production)
===========================================================================================================
- Canonical Asset ID: SM_Arena_TileVisual_01
- Approved Phase 1 Concept Baseline: Sphere_Brawl_Arena_TileVisual_Concept_01.zip
  (Verified SHA-256: fe40cd09419b86b915a896c90d37b3ea8978e0607bb4171c0a13bbc3b1b714d7)
- Locked Grid Architecture:
  * Grid Dimensions: 9 x 9 cells (81 initial cells), integer coordinates X, Z in [-4, +4]
  * Tile Pitch: 12.0000 studs center-to-center
  * Grid Centre (ArenaCFrame): (0.0000, 50.0000, 0.0000); Top Surface World Y = 51.0000
  * Tile Centre Transform: local tileCenter = (ArenaCFrame * CFrame.new(12 * x, 0, 12 * z)).Position
  * Authoritative CollisionTile: 12.0000 x 2.0000 x 12.0000 studs (CanCollide=true, Transparency=1, NOT in visual mesh)
  * Base VisualTile (SM_Arena_TileVisual_01): 11.8000 x 2.0000 x 11.8000 studs (CanCollide=false, CanTouch=false)
  * Visible Inter-Tile Groove: 0.2000 studs (0.1000 stud inset per visual tile edge)
  * Local Origin: (0.0000, 0.0000, 0.0000) at geometric center of the 11.8 x 2.0 x 11.8 visual tile
  * Local Bounds (Base Tile): X in [-5.9000, +5.9000], Y in [-1.0000, +1.0000], Z in [-5.9000, +5.9000]
  * Local Bounds (Overlays):  X in [-5.7000, +5.7000], Y in [+1.0000, +1.0500], Z in [-5.7000, +5.7000] (11.40 x 0.05 x 11.40 studs)
- Phase 2 Corrected Triangle Budget Gate:
  * Base Tile Target <= 170 triangles -> Actual Measured Production Base Tile = 152 triangles (456 vertices)
  * Every Overlay Measured Independently (32 to 72 triangles)
  * Every Allowed Cell Visual State (Base + Simultaneous Overlay) <= 249 triangles -> Max Combined = 224 triangles!

Usage:
  1. In standard Python 3 (builds deterministic .obj, .mtl, .glb, palette atlas):
     python3 scripts/generate_arena_tile_blender.py --out_dir ./meshes
  2. In Blender 3.6+ / 4.x (builds scene, saves .blend if available, and exports .obj/.mtl/.glb):
     blender --background --python scripts/generate_arena_tile_blender.py -- --out_dir ./meshes
"""

import os
import sys
import io
import json
import math
import struct
import hashlib
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
    "MAT_PrimaryText",
    "EMI_Cyan",
    "EMI_Ice",
    "EMI_Magnetic",
    "EMI_Kinetic",
    "EMI_Amber",
    "EMI_DangerRed",
]

PALETTE_SRGB = {
    "MAT_DarkNeutral": (32, 38, 54),     # #202636 — Main body and primary tile surfaces
    "MAT_AltNeutral":  (42, 50, 70),     # #2A3246 — Alternate checkerboard and inset regions
    "MAT_LightTrim":   (170, 190, 215),  # #AABED7 — Restrained brackets and edge details
    "MAT_PrimaryText": (245, 248, 255),  # #F5F8FF — High-contrast visual markings
    "EMI_Cyan":        (0, 195, 255),    # #00C3FF — Base tile energy and safe state
    "EMI_Ice":         (0, 235, 255),    # #00EBFF — Ice Corridor active state
    "EMI_Magnetic":    (165, 55, 255),   # #A537FF — Magnetic Storm
    "EMI_Kinetic":     (255, 125, 0),    # #FF7D00 — Boost Runway
    "EMI_Amber":       (255, 170, 0),    # #FFAA00 — Hazard warning
    "EMI_DangerRed":   (255, 40, 40),    # #FF2828 — Ring-collapse warning
}

PALETTE = {
    k: (v[0] / 255.0, v[1] / 255.0, v[2] / 255.0, 1.0)
    for k, v in PALETTE_SRGB.items()
}

APPROVED_PALETTE_METADATA = {
    "MAT_DarkNeutral": {
        "rgb_255": [32, 38, 54],
        "hex": "#202636",
        "emissive": False,
        "metallic": 0.55,
        "roughness": 0.42,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(32, 38, 54)",
        "purpose": "Main body and primary tile surfaces (Variant A outer bevel frame, Variant B center deck & ribs, overlay carrier)",
    },
    "MAT_AltNeutral": {
        "rgb_255": [42, 50, 70],
        "hex": "#2A3246",
        "emissive": False,
        "metallic": 0.60,
        "roughness": 0.35,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(42, 50, 70)",
        "purpose": "Alternate checkerboard and inset regions (Variant B outer bevel frame, Variant A center deck & ribs, Ice carrier)",
    },
    "MAT_LightTrim": {
        "rgb_255": [170, 190, 215],
        "hex": "#AABED7",
        "emissive": False,
        "metallic": 0.78,
        "roughness": 0.28,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(170, 190, 215)",
        "purpose": "Restrained corner brackets and edge details (GEO_Tile_CornerTrimLock_04)",
    },
    "MAT_PrimaryText": {
        "rgb_255": [245, 248, 255],
        "hex": "#F5F8FF",
        "emissive": True,
        "metallic": 0.10,
        "roughness": 0.20,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(245, 248, 255)",
        "purpose": "High-contrast visual markings (pale ice chevrons, snowflake core, magnetic pull arrows, boost turbine bar)",
    },
    "EMI_Cyan": {
        "rgb_255": [0, 195, 255],
        "hex": "#00C3FF",
        "emissive": True,
        "metallic": 0.10,
        "roughness": 0.15,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(0, 195, 255)",
        "purpose": "Base tile energy circuit inlay and safe state accent (GEO_Tile_CyanCircuitInlay)",
    },
    "EMI_Ice": {
        "rgb_255": [0, 235, 255],
        "hex": "#00EBFF",
        "emissive": True,
        "metallic": 0.10,
        "roughness": 0.15,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(0, 235, 255)",
        "purpose": "Ice Corridor active frost frame, 6-bar snowflake icon, and warning preview motif",
    },
    "EMI_Magnetic": {
        "rgb_255": [165, 55, 255],
        "hex": "#A537FF",
        "emissive": True,
        "metallic": 0.12,
        "roughness": 0.16,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(165, 55, 255)",
        "purpose": "Magnetic Storm anchor core, concentric 2D pull rings, and surrounding field chevrons",
    },
    "EMI_Kinetic": {
        "rgb_255": [255, 125, 0],
        "hex": "#FF7D00",
        "emissive": True,
        "metallic": 0.14,
        "roughness": 0.18,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(255, 125, 0)",
        "purpose": "Boost Runway directional chevrons, lateral runway guide rails, and turbine intake bars",
    },
    "EMI_Amber": {
        "rgb_255": [255, 170, 0],
        "hex": "#FFAA00",
        "emissive": True,
        "metallic": 0.15,
        "roughness": 0.18,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(255, 170, 0)",
        "purpose": "Pre-hazard warning perimeter border, corner alert triangles, and secondary boost accents",
    },
    "EMI_DangerRed": {
        "rgb_255": [255, 40, 40],
        "hex": "#FF2828",
        "emissive": True,
        "metallic": 0.15,
        "roughness": 0.18,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(255, 40, 40)",
        "purpose": "Ring-collapse 3.0s warning border flash and asymmetric structural fracture crack lines",
    },
}

ATLAS_FILENAME = "T_Arena_TilePalette_256.png"


def build_palette_atlas_bytes():
    """
    Builds a deterministic 256x256 PNG palette atlas (5 columns x 2 rows = 10 swatches, each 51x128 px).
    Strictly within the 1024x1024 project maximum texture resolution.
    """
    w, h = 256, 256
    img = Image.new("RGBA", (w, h), (32, 38, 54, 255))
    draw = ImageDraw.Draw(img)
    col_bounds = [(0, 51), (51, 102), (102, 153), (153, 204), (204, 256)]
    row_bounds = [(0, 128), (128, 256)]
    uv_obj = {}
    uv_gltf = {}
    for idx, mname in enumerate(PALETTE_ORDER):
        c_i = idx % 5
        r_i = idx // 5
        x0, x1 = col_bounds[c_i]
        y0, y1 = row_bounds[r_i]
        rgb = PALETTE_SRGB[mname]
        draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=(rgb[0], rgb[1], rgb[2], 255))
        uc = 0.5 * (x0 + x1) / float(w)
        vc_top = 0.5 * (y0 + y1) / float(h)
        uv_gltf[mname] = (round(uc, 5), round(vc_top, 5))
        uv_obj[mname] = (round(uc, 5), round(1.0 - vc_top, 5))
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=False)
    return buf.getvalue(), uv_obj, uv_gltf


ATLAS_PNG_BYTES, UV_CENTERS_OBJ, UV_CENTERS_GLTF = build_palette_atlas_bytes()


class TileMeshBuilder:
    def __init__(self, name):
        self.name = name
        self.comp_order = []
        self.comp_tris = {}
        self.comp_mat = {}

    def ensure_component(self, comp_name, mat_name):
        if comp_name not in self.comp_tris:
            self.comp_order.append(comp_name)
            self.comp_tris[comp_name] = []
            self.comp_mat[comp_name] = mat_name

    def add_tri(self, comp_name, mat_name, p0, p1, p2):
        self.ensure_component(comp_name, mat_name)
        v0 = np.array(p0, dtype=np.float64)
        v1 = np.array(p1, dtype=np.float64)
        v2 = np.array(p2, dtype=np.float64)
        if np.linalg.norm(np.cross(v1 - v0, v2 - v0)) > 1e-8:
            self.comp_tris[comp_name].append((v0, v1, v2))

    def add_quad(self, comp_name, mat_name, p0, p1, p2, p3):
        self.add_tri(comp_name, mat_name, p0, p1, p2)
        self.add_tri(comp_name, mat_name, p0, p2, p3)

    def add_poly_cap(self, comp_name, mat_name, pts, flip=False):
        n = len(pts)
        if n < 3:
            return
        for i in range(1, n - 1):
            if not flip:
                self.add_tri(comp_name, mat_name, pts[0], pts[i], pts[i + 1])
            else:
                self.add_tri(comp_name, mat_name, pts[0], pts[i + 1], pts[i])

    def add_closed_loft(self, comp_name, mat_name, ring_bot, ring_top, cap_bot=True, cap_top=True):
        n = len(ring_bot)
        for i in range(n):
            j = (i + 1) % n
            self.add_quad(comp_name, mat_name, ring_bot[i], ring_bot[j], ring_top[j], ring_top[i])
        if cap_bot:
            self.add_poly_cap(comp_name, mat_name, ring_bot, flip=False)
        if cap_top:
            self.add_poly_cap(comp_name, mat_name, ring_top, flip=True)

    def add_box(self, comp_name, mat_name, x0, x1, y0, y1, z0, z1, cap_bot=True, cap_top=True):
        b = [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)]
        t = [(x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)]
        self.add_closed_loft(comp_name, mat_name, b, t, cap_bot=cap_bot, cap_top=cap_top)

    def add_flat_top_quad(self, comp_name, mat_name, x0, x1, y, z0, z1):
        self.add_quad(comp_name, mat_name, (x0, y, z1), (x1, y, z1), (x1, y, z0), (x0, y, z0))

    def add_flat_top_poly(self, comp_name, mat_name, y, xz_pts_ccw):
        pts3 = [(p[0], y, p[1]) for p in xz_pts_ccw]
        self.add_poly_cap(comp_name, mat_name, pts3, flip=False)

    def add_flat_ring_frame(self, comp_name, mat_name, y, x_out, z_out, width):
        xi = x_out - width
        zi = z_out - width
        self.add_flat_top_quad(comp_name, mat_name, -x_out, +x_out, y, -z_out, -zi)
        self.add_flat_top_quad(comp_name, mat_name, -x_out, +x_out, y, +zi, +z_out)
        self.add_flat_top_quad(comp_name, mat_name, -x_out, -xi, y, -zi, +zi)
        self.add_flat_top_quad(comp_name, mat_name, +xi, +x_out, y, -zi, +zi)

    def get_all_tris_with_mat(self):
        out = []
        for cname in self.comp_order:
            mname = self.comp_mat[cname]
            for (v0, v1, v2) in self.comp_tris[cname]:
                out.append((v0, v1, v2, mname, cname))
        return out

    def compute_metrics(self):
        total_tris = 0
        mat_area = {}
        comp_stats = {}
        all_v = []
        for cname in self.comp_order:
            tris = self.comp_tris[cname]
            mname = self.comp_mat[cname]
            c_area = 0.0
            c_v = []
            for (v0, v1, v2) in tris:
                all_v.extend([v0, v1, v2])
                c_v.extend([v0, v1, v2])
                a = 0.5 * float(np.linalg.norm(np.cross(v1 - v0, v2 - v0)))
                c_area += a
                mat_area[mname] = mat_area.get(mname, 0.0) + a
            c_pts = np.array(c_v, dtype=np.float64)
            comp_stats[cname] = {
                "material": mname,
                "triangles": len(tris),
                "vertices": len(tris) * 3,
                "surface_area_sq_studs": round(c_area, 4),
                "bbox_min": c_pts.min(axis=0).round(4).tolist(),
                "bbox_max": c_pts.max(axis=0).round(4).tolist(),
            }
            total_tris += len(tris)
        pts = np.array(all_v, dtype=np.float64)
        bmin = pts.min(axis=0).round(4).tolist()
        bmax = pts.max(axis=0).round(4).tolist()
        dims = (pts.max(axis=0) - pts.min(axis=0)).round(4).tolist()
        tot_a = sum(mat_area.values()) if mat_area else 1.0
        mat_pct = {k: round(100.0 * v / tot_a, 2) for k, v in mat_area.items()}
        return {
            "name": self.name,
            "total_triangles": total_tris,
            "total_vertices": total_tris * 3,
            "component_count": len(self.comp_order),
            "bbox_min": bmin,
            "bbox_max": bmax,
            "dimensions_xyz": dims,
            "material_area_pct": mat_pct,
            "used_materials": [m for m in PALETTE_ORDER if m in set(self.comp_mat.values())],
            "components": comp_stats,
        }

    def export_obj_and_mtl(self, obj_path, mtl_path, tex_rel_path):
        mtl_filename = os.path.basename(mtl_path)
        used_mats = [m for m in PALETTE_ORDER if m in set(self.comp_mat.values())]

        with open(mtl_path, "w", encoding="utf-8") as mf:
            mf.write("# Sphere Brawl: Rolling Rampage — Production Material Library\n")
            mf.write(f"# Asset: {self.name} (Phase 2 Approved Production Asset)\n")
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
                mf.write(f"map_Kd {tex_rel_path}\n")

        with open(obj_path, "w", encoding="utf-8") as of:
            of.write("# Sphere Brawl: Rolling Rampage — Modular Arena Tile & Hazard Visual System\n")
            of.write(f"# Asset Name: {self.name} (Phase 2 Production Geometry)\n")
            of.write("# Unit Scale: 1.0 Unit = 1.0 Roblox Stud | Up Axis: +Y | Forward Axis: -Z\n")
            of.write("# Local Origin (0,0,0): Geometric Center of Base Visual Tile (Top Surface at Local Y = +1.0000)\n")
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
            "name": "T_Arena_TilePalette_256",
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
            "name": "T_Arena_TilePalette_256_Tex",
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
                [round(float(x), 5) for x in pos_arr.min(axis=0)],
                [round(float(x), 5) for x in pos_arr.max(axis=0)],
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
                "generator": "Sphere Brawl Modular Arena Tile Production Pipeline (SM_Arena_TileVisual_01)",
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
        with open(glb_path, "wb") as gf:
            gf.write(struct.pack("<III", 0x46546C67, 2, total_len))
            gf.write(struct.pack("<II", len(json_bytes), 0x4E4F534A))
            gf.write(json_bytes)
            gf.write(struct.pack("<II", len(buffer_bytes), 0x004E4942))
            gf.write(buffer_bytes)


def make_oct_ring(half_span, y, corner_cut):
    h = float(half_span)
    c = float(corner_cut)
    return [
        (-h + c, y, +h),
        (+h - c, y, +h),
        (+h,     y, +h - c),
        (+h,     y, -h + c),
        (+h - c, y, -h),
        (-h + c, y, -h),
        (-h,     y, -h + c),
        (-h,     y, +h - c),
    ]


# ==============================================================================
# 1. PRODUCTION BASE VISUAL TILE: SM_Arena_TileVisual_01 (Variant A & Variant B)
#    - Target: <= 170 triangles (Corrected Phase 2 requirement)
#    - Measured Production Topology: 152 triangles (456 vertices) across 5 components
#    - Exact Local Bounds: X in [-5.9000, +5.9000], Y in [-1.0000, +1.0000], Z in [-5.9000, +5.9000]
#    - Exact Dimensions: 11.8000 x 2.0000 x 11.8000 studs
#    - Identical vertex coordinates & component topology across Variant A & Variant B
# ==============================================================================
def build_production_base_tile(variant="A"):
    primary_mat = "MAT_DarkNeutral" if variant == "A" else "MAT_AltNeutral"
    secondary_mat = "MAT_AltNeutral" if variant == "A" else "MAT_DarkNeutral"

    mb = TileMeshBuilder(f"SM_Arena_TileVisual_01_Variant{variant}")

    # 1. COMP_Arena_TileBevelFrame_118 (70 triangles)
    r_bot = make_oct_ring(5.6500, -1.0000, 0.3500)
    r_low = make_oct_ring(5.9000, -0.7500, 0.4500)
    r_mid = make_oct_ring(5.9000, +0.7500, 0.4500)
    r_top = make_oct_ring(5.6500, +1.0000, 0.3500)
    r_rim_in = make_oct_ring(4.6000, +1.0000, 0.2800)

    mb.add_closed_loft("COMP_Arena_TileBevelFrame_118", primary_mat, r_bot, r_low, cap_bot=True, cap_top=False)     # 22 tris
    mb.add_closed_loft("COMP_Arena_TileBevelFrame_118", primary_mat, r_low, r_mid, cap_bot=False, cap_top=False)    # 16 tris
    mb.add_closed_loft("COMP_Arena_TileBevelFrame_118", primary_mat, r_mid, r_top, cap_bot=False, cap_top=False)    # 16 tris
    mb.add_closed_loft("COMP_Arena_TileBevelFrame_118", primary_mat, r_top, r_rim_in, cap_bot=False, cap_top=False) # 16 tris

    # 2. GEO_Tile_CyanCircuitInlay (24 triangles)
    r_cir_in = make_oct_ring(4.4000, +0.9850, 0.2600)
    mb.add_closed_loft("GEO_Tile_CyanCircuitInlay", "EMI_Cyan", r_rim_in, r_cir_in, cap_bot=False, cap_top=False)   # 16 tris
    mb.add_flat_top_quad("GEO_Tile_CyanCircuitInlay", "EMI_Cyan", -0.3500, +0.3500, +0.9990, -5.2500, -4.6500)
    mb.add_flat_top_quad("GEO_Tile_CyanCircuitInlay", "EMI_Cyan", -0.3500, +0.3500, +0.9990, +4.6500, +5.2500)
    mb.add_flat_top_quad("GEO_Tile_CyanCircuitInlay", "EMI_Cyan", -5.2500, -4.6500, +0.9990, -0.3500, +0.3500)
    mb.add_flat_top_quad("GEO_Tile_CyanCircuitInlay", "EMI_Cyan", +4.6500, +5.2500, +0.9990, -0.3500, +0.3500)

    # 3. GEO_Tile_CenterDeckPlate (22 triangles)
    r_deck_top = make_oct_ring(4.3600, +1.0000, 0.2500)
    mb.add_closed_loft("GEO_Tile_CenterDeckPlate", secondary_mat, r_cir_in, r_deck_top, cap_bot=False, cap_top=True) # 22 tris

    # 4. GEO_Tile_CornerTrimLock_04 (16 triangles)
    for sx in (-1.0, +1.0):
        for sz in (-1.0, +1.0):
            xa0, xa1 = sorted([sx * 3.5500, sx * 5.1000])
            za0, za1 = sorted([sz * 4.7200, sz * 5.1800])
            mb.add_flat_top_quad("GEO_Tile_CornerTrimLock_04", "MAT_LightTrim", xa0, xa1, +0.9990, za0, za1)
            xb0, xb1 = sorted([sx * 4.7200, sx * 5.1800])
            zb0, zb1 = sorted([sz * 3.5500, sz * 4.7200])
            mb.add_flat_top_quad("GEO_Tile_CornerTrimLock_04", "MAT_LightTrim", xb0, xb1, +0.9990, zb0, zb1)

    # 5. GEO_Tile_UndersideRibs (20 triangles)
    mb.add_box("GEO_Tile_UndersideRibs", secondary_mat, -5.8000, +5.8000, -0.9500, -0.4500, -1.6500, -1.0500, cap_bot=True, cap_top=False)
    mb.add_box("GEO_Tile_UndersideRibs", secondary_mat, -5.8000, +5.8000, -0.9500, -0.4500, +1.0500, +1.6500, cap_bot=True, cap_top=False)

    return mb


# ==============================================================================
# 2. PRODUCTION MODULAR NON-COLLIDING HAZARD OVERLAYS (8 REQUIRED ASSETS)
# ==============================================================================
def add_overlay_carrier_slab(ob, comp_name, mat_name):
    ob.add_box(comp_name, mat_name, -5.7000, +5.7000, +1.0000, +1.0460, -5.7000, +5.7000, cap_bot=False, cap_top=True)


def add_amber_warning_perimeter(ob, comp_name="OVL_Warning_AmberBorder"):
    ob.add_flat_ring_frame(comp_name, "EMI_Amber", +1.0480, 5.5500, 5.5500, 0.4800)
    for sx in (-1.0, +1.0):
        for sz in (-1.0, +1.0):
            pts = [
                (sx * 4.8500, sz * 4.8500),
                (sx * 3.6500, sz * 4.8500),
                (sx * 4.8500, sz * 3.6500),
            ]
            v0 = np.array([pts[0][0], 1.0490, pts[0][1]])
            v1 = np.array([pts[1][0], 1.0490, pts[1][1]])
            v2 = np.array([pts[2][0], 1.0490, pts[2][1]])
            if np.cross(v1 - v0, v2 - v0)[1] > 0:
                ob.add_tri(comp_name, "EMI_Amber", v0, v1, v2)
            else:
                ob.add_tri(comp_name, "EMI_Amber", v0, v2, v1)


def add_chevron_ribbon(ob, comp_name, mat_name, y, z_tip, z_tail, x_half, thickness):
    p_l = [
        (-x_half, z_tail + thickness),
        (0.0,     z_tip + thickness),
        (0.0,     z_tip),
        (-x_half, z_tail),
    ]
    ob.add_flat_top_poly(comp_name, mat_name, y, p_l)
    p_r = [
        (0.0,     z_tip + thickness),
        (+x_half, z_tail + thickness),
        (+x_half, z_tail),
        (0.0,     z_tip),
    ]
    ob.add_flat_top_poly(comp_name, mat_name, y, p_r)


def add_snowflake_icon(ob, comp_name, mat_name, y, cx=0.0, cz=0.0, radius=1.95, arm_half_w=0.22):
    for idx, ang_deg in enumerate((0.0, 60.0, 120.0)):
        rad = math.radians(ang_deg)
        dx, dz = math.cos(rad), math.sin(rad)
        nx, nz = -dz, dx
        pts = [
            (cx - dx * radius + nx * arm_half_w, cz - dz * radius + nz * arm_half_w),
            (cx + dx * radius + nx * arm_half_w, cz + dz * radius + nz * arm_half_w),
            (cx + dx * radius - nx * arm_half_w, cz + dz * radius - nz * arm_half_w),
            (cx - dx * radius - nx * arm_half_w, cz - dz * radius - nz * arm_half_w),
        ]
        ob.add_flat_top_poly(comp_name, mat_name, y + idx * 0.0002, pts)
    r_hub = radius * 0.42
    pts_hub = [
        (cx, cz + r_hub),
        (cx + r_hub, cz),
        (cx, cz - r_hub),
        (cx - r_hub, cz),
    ]
    ob.add_flat_top_poly(comp_name, "MAT_PrimaryText", 1.0500, pts_hub)


def add_octagonal_flat_ring(ob, comp_name, mat_name, y, r_out, r_in, cx=0.0, cz=0.0):
    n = 8
    for i in range(n):
        a0 = 2.0 * math.pi * i / n + (math.pi / 8.0)
        a1 = 2.0 * math.pi * (i + 1) / n + (math.pi / 8.0)
        c0, s0 = math.cos(a0), math.sin(a0)
        c1, s1 = math.cos(a1), math.sin(a1)
        pts = [
            (cx + r_out * c0, cz + r_out * s0),
            (cx + r_in  * c0, cz + r_in  * s0),
            (cx + r_in  * c1, cz + r_in  * s1),
            (cx + r_out * c1, cz + r_out * s1),
        ]
        v0 = np.array([pts[0][0], y, pts[0][1]])
        v1 = np.array([pts[1][0], y, pts[1][1]])
        v2 = np.array([pts[2][0], y, pts[2][1]])
        v3 = np.array([pts[3][0], y, pts[3][1]])
        if np.cross(v1 - v0, v2 - v0)[1] > 0:
            ob.add_quad(comp_name, mat_name, v0, v1, v2, v3)
        else:
            ob.add_quad(comp_name, mat_name, v0, v3, v2, v1)


OVERLAY_ASSET_NAMES = [
    "OVL_Arena_Warn_Ice",
    "OVL_Arena_Active_Ice",
    "OVL_Arena_Warn_Magnetic",
    "OVL_Arena_Active_MagneticAnchor",
    "OVL_Arena_Active_MagneticField",
    "OVL_Arena_Warn_Boost",
    "OVL_Arena_Active_Boost",
    "OVL_Arena_Collapse_Warn",
]


def build_production_overlay(overlay_name):
    ob = TileMeshBuilder(overlay_name)

    if overlay_name == "OVL_Arena_Warn_Ice":
        add_overlay_carrier_slab(ob, "OVL_Carrier_WarnIce", "MAT_DarkNeutral")
        add_amber_warning_perimeter(ob, "OVL_WarnIce_AmberBorder")
        add_snowflake_icon(ob, "OVL_WarnIce_PreviewSnowflake", "EMI_Ice", +1.0492, radius=1.80, arm_half_w=0.20)
        add_chevron_ribbon(ob, "OVL_WarnIce_PreviewChevrons", "EMI_Ice", +1.0500, z_tip=-3.95, z_tail=-2.75, x_half=2.60, thickness=0.42)
        add_chevron_ribbon(ob, "OVL_WarnIce_PreviewChevrons", "EMI_Ice", +1.0500, z_tip=+2.35, z_tail=+3.55, x_half=2.60, thickness=0.42)

    elif overlay_name == "OVL_Arena_Active_Ice":
        add_overlay_carrier_slab(ob, "OVL_Carrier_ActiveIce", "MAT_AltNeutral")
        ob.add_flat_ring_frame("OVL_ActiveIce_FrostBorder", "EMI_Ice", +1.0480, 5.5500, 5.5500, 0.4500)
        ob.add_flat_top_quad("OVL_ActiveIce_FrostRails", "EMI_Cyan", -4.6500, -4.1500, +1.0485, -4.7500, +4.7500)
        ob.add_flat_top_quad("OVL_ActiveIce_FrostRails", "EMI_Cyan", +4.1500, +4.6500, +1.0485, -4.7500, +4.7500)
        add_chevron_ribbon(ob, "OVL_ActiveIce_PaleChevrons", "MAT_PrimaryText", +1.0500, z_tip=-4.55, z_tail=-3.15, x_half=3.25, thickness=0.52)
        add_chevron_ribbon(ob, "OVL_ActiveIce_PaleChevrons", "MAT_PrimaryText", +1.0500, z_tip=+2.55, z_tail=+3.95, x_half=3.25, thickness=0.52)
        add_snowflake_icon(ob, "OVL_ActiveIce_SnowflakeIcon", "EMI_Ice", +1.0492, radius=1.95, arm_half_w=0.24)

    elif overlay_name == "OVL_Arena_Warn_Magnetic":
        add_overlay_carrier_slab(ob, "OVL_Carrier_WarnMagnetic", "MAT_DarkNeutral")
        add_amber_warning_perimeter(ob, "OVL_WarnMag_AmberBorder")
        add_octagonal_flat_ring(ob, "OVL_WarnMag_PreviewRings", "EMI_Magnetic", +1.0492, r_out=3.75, r_in=3.30)
        add_octagonal_flat_ring(ob, "OVL_WarnMag_PreviewRings", "EMI_Magnetic", +1.0495, r_out=2.15, r_in=1.75)
        pts_anchor = [(0.0, +1.05), (+1.05, 0.0), (0.0, -1.05), (-1.05, 0.0)]
        ob.add_flat_top_poly("OVL_WarnMag_PreviewAnchor", "EMI_Amber", +1.0500, pts_anchor)

    elif overlay_name == "OVL_Arena_Active_MagneticAnchor":
        add_overlay_carrier_slab(ob, "OVL_Carrier_ActiveMagAnchor", "MAT_DarkNeutral")
        ob.add_flat_ring_frame("OVL_ActiveMag_Border", "EMI_Magnetic", +1.0480, 5.5500, 5.5500, 0.3800)
        add_octagonal_flat_ring(ob, "OVL_ActiveMag_OuterRing", "EMI_Magnetic", +1.0488, r_out=4.55, r_in=4.00)
        add_octagonal_flat_ring(ob, "OVL_ActiveMag_InnerRing", "EMI_Magnetic", +1.0492, r_out=2.85, r_in=2.30)
        add_octagonal_flat_ring(ob, "OVL_ActiveMag_AnchorCore", "EMI_Magnetic", +1.0496, r_out=1.25, r_in=0.45)
        pts_core = [(0.0, +0.55), (+0.55, 0.0), (0.0, -0.55), (-0.55, 0.0)]
        ob.add_flat_top_poly("OVL_ActiveMag_AnchorCenter", "MAT_PrimaryText", +1.0500, pts_core)
        ob.add_tri("OVL_ActiveMag_InwardVectors", "MAT_PrimaryText", (-0.65, 1.0500, -4.85), (0.0, 1.0500, -3.15), (+0.65, 1.0500, -4.85))
        ob.add_tri("OVL_ActiveMag_InwardVectors", "MAT_PrimaryText", (+0.65, 1.0500, +4.85), (0.0, 1.0500, +3.15), (-0.65, 1.0500, +4.85))
        ob.add_tri("OVL_ActiveMag_InwardVectors", "MAT_PrimaryText", (-4.85, 1.0500, +0.65), (-3.15, 1.0500, 0.0), (-4.85, 1.0500, -0.65))
        ob.add_tri("OVL_ActiveMag_InwardVectors", "MAT_PrimaryText", (+4.85, 1.0500, -0.65), (+3.15, 1.0500, 0.0), (+4.85, 1.0500, +0.65))

    elif overlay_name == "OVL_Arena_Active_MagneticField":
        add_overlay_carrier_slab(ob, "OVL_Carrier_ActiveMagField", "MAT_DarkNeutral")
        ob.add_flat_ring_frame("OVL_ActiveMagField_Border", "EMI_Magnetic", +1.0480, 5.5500, 5.5500, 0.2800)
        add_octagonal_flat_ring(ob, "OVL_ActiveMagField_Ring", "EMI_Magnetic", +1.0490, r_out=3.85, r_in=3.35)
        add_chevron_ribbon(ob, "OVL_ActiveMagField_PullVector", "EMI_Magnetic", +1.0496, z_tip=-2.40, z_tail=-0.40, x_half=2.40, thickness=0.55)
        add_chevron_ribbon(ob, "OVL_ActiveMagField_PullVector", "MAT_PrimaryText", +1.0500, z_tip=+0.40, z_tail=+2.40, x_half=2.00, thickness=0.42)

    elif overlay_name == "OVL_Arena_Warn_Boost":
        add_overlay_carrier_slab(ob, "OVL_Carrier_WarnBoost", "MAT_DarkNeutral")
        add_amber_warning_perimeter(ob, "OVL_WarnBoost_AmberBorder")
        add_chevron_ribbon(ob, "OVL_WarnBoost_PreviewArrows", "EMI_Kinetic", +1.0494, z_tip=-3.85, z_tail=-1.95, x_half=3.10, thickness=0.58)
        add_chevron_ribbon(ob, "OVL_WarnBoost_PreviewArrows", "EMI_Amber",   +1.0496, z_tip=-0.85, z_tail=+1.05, x_half=3.10, thickness=0.58)
        ob.add_flat_top_quad("OVL_WarnBoost_TurbinePreview", "EMI_Kinetic", -2.80, +2.80, +1.0498, +2.35, +2.85)
        ob.add_flat_top_quad("OVL_WarnBoost_TurbinePreview", "EMI_Amber",   -2.20, +2.20, +1.0500, +3.25, +3.70)

    elif overlay_name == "OVL_Arena_Active_Boost":
        add_overlay_carrier_slab(ob, "OVL_Carrier_ActiveBoost", "MAT_DarkNeutral")
        ob.add_flat_top_quad("OVL_ActiveBoost_RunwayRails", "EMI_Kinetic", -5.4500, -4.7500, +1.0485, -5.3000, +5.3000)
        ob.add_flat_top_quad("OVL_ActiveBoost_RunwayRails", "EMI_Kinetic", +4.7500, +5.4500, +1.0485, -5.3000, +5.3000)
        ob.add_flat_top_quad("OVL_ActiveBoost_InnerRails",  "EMI_Amber",   -4.4500, -4.1500, +1.0490, -5.0000, +5.0000)
        ob.add_flat_top_quad("OVL_ActiveBoost_InnerRails",  "EMI_Amber",   +4.1500, +4.4500, +1.0490, -5.0000, +5.0000)
        add_chevron_ribbon(ob, "OVL_ActiveBoost_Chevron1", "EMI_Kinetic", +1.0495, z_tip=-4.85, z_tail=-2.65, x_half=3.75, thickness=0.72)
        add_chevron_ribbon(ob, "OVL_ActiveBoost_Chevron2", "EMI_Amber",   +1.0497, z_tip=-1.95, z_tail=+0.25, x_half=3.75, thickness=0.72)
        add_chevron_ribbon(ob, "OVL_ActiveBoost_Chevron3", "EMI_Kinetic", +1.0499, z_tip=+0.95, z_tail=+3.15, x_half=3.75, thickness=0.72)
        ob.add_flat_top_quad("OVL_ActiveBoost_TurbineGrille", "MAT_PrimaryText", -3.4000, +3.4000, +1.0500, +3.5500, +3.9500)
        ob.add_flat_top_quad("OVL_ActiveBoost_TurbineGrille", "EMI_Kinetic",     -2.8000, +2.8000, +1.0500, +4.2000, +4.6000)
        ob.add_flat_top_quad("OVL_ActiveBoost_TurbineGrille", "EMI_Amber",       -2.1000, +2.1000, +1.0500, +4.8500, +5.2000)

    elif overlay_name == "OVL_Arena_Collapse_Warn":
        add_overlay_carrier_slab(ob, "OVL_Carrier_Collapse", "MAT_DarkNeutral")
        ob.add_flat_ring_frame("OVL_Collapse_RedBorder", "EMI_DangerRed", +1.0485, 5.5800, 5.5800, 0.5800)
        crack_segments = [
            ((-4.40, -4.10), (-4.05, -4.45), (-0.80, -0.35), (-1.15,  0.00)),
            ((-1.15,  0.00), (-0.80, -0.35), (+1.45, +0.85), (+1.10, +1.20)),
            ((+1.10, +1.20), (+1.45, +0.85), (+4.35, +4.05), (+4.00, +4.40)),
            ((+3.95, -4.35), (+4.30, -4.00), (+0.65, -0.85), (+0.30, -1.20)),
            ((+0.30, -1.20), (+0.65, -0.85), (-3.85, +4.25), (-4.20, +3.90)),
            ((-4.60, +0.45), (-4.60, +0.10), (-1.10, -0.15), (-1.10, +0.20)),
        ]
        for idx, pts in enumerate(crack_segments):
            yc = 1.0490 + idx * 0.0001
            v0 = np.array([pts[0][0], yc, pts[0][1]])
            v1 = np.array([pts[1][0], yc, pts[1][1]])
            v2 = np.array([pts[2][0], yc, pts[2][1]])
            v3 = np.array([pts[3][0], yc, pts[3][1]])
            if np.cross(v1 - v0, v2 - v0)[1] > 0:
                ob.add_quad("OVL_Collapse_CrackDecals", "EMI_DangerRed", v0, v1, v2, v3)
            else:
                ob.add_quad("OVL_Collapse_CrackDecals", "EMI_DangerRed", v0, v3, v2, v1)
        pts_core = [(0.0, +0.85), (+0.85, 0.0), (0.0, -0.85), (-0.85, 0.0)]
        ob.add_flat_top_poly("OVL_Collapse_CenterAlert", "MAT_PrimaryText", +1.0500, pts_core)

    return ob


def main():
    out_dir = "./meshes"
    if "--out_dir" in sys.argv:
        idx = sys.argv.index("--out_dir")
        if idx + 1 < len(sys.argv):
            out_dir = sys.argv[idx + 1]

    out_dir = os.path.abspath(out_dir)
    ovl_dir = os.path.join(out_dir, "overlays")
    pkg_root = os.path.dirname(out_dir)
    tex_dir = os.path.join(pkg_root, "textures")

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(ovl_dir, exist_ok=True)
    os.makedirs(tex_dir, exist_ok=True)

    atlas_path = os.path.join(tex_dir, ATLAS_FILENAME)
    with open(atlas_path, "wb") as tf:
        tf.write(ATLAS_PNG_BYTES)

    var_a = build_production_base_tile("A")
    var_b = build_production_base_tile("B")

    var_a.export_obj_and_mtl(
        os.path.join(out_dir, "SM_Arena_TileVisual_01_VariantA.obj"),
        os.path.join(out_dir, "SM_Arena_TileVisual_01_VariantA.mtl"),
        f"../textures/{ATLAS_FILENAME}",
    )
    var_a.export_glb(os.path.join(out_dir, "SM_Arena_TileVisual_01_VariantA.glb"))

    var_b.export_obj_and_mtl(
        os.path.join(out_dir, "SM_Arena_TileVisual_01_VariantB.obj"),
        os.path.join(out_dir, "SM_Arena_TileVisual_01_VariantB.mtl"),
        f"../textures/{ATLAS_FILENAME}",
    )
    var_b.export_glb(os.path.join(out_dir, "SM_Arena_TileVisual_01_VariantB.glb"))

    ovl_metrics = {}
    for ovl_name in OVERLAY_ASSET_NAMES:
        ob = build_production_overlay(ovl_name)
        ob.export_obj_and_mtl(
            os.path.join(ovl_dir, f"{ovl_name}.obj"),
            os.path.join(ovl_dir, f"{ovl_name}.mtl"),
            f"../../textures/{ATLAS_FILENAME}",
        )
        ob.export_glb(os.path.join(ovl_dir, f"{ovl_name}.glb"))
        ovl_metrics[ovl_name] = ob.compute_metrics()

    base_a_m = var_a.compute_metrics()
    base_tris = base_a_m["total_triangles"]

    allowed_states = [
        {"state_id": "State_A_Safe_VariantA", "base_mesh": "SM_Arena_TileVisual_01_VariantA", "overlay_mesh": None, "base_triangles": base_tris, "overlay_triangles": 0, "combined_triangles": base_tris, "budget_cap": 249, "status": "PASS" if base_tris <= 249 else "FAIL"},
        {"state_id": "State_A_Safe_VariantB", "base_mesh": "SM_Arena_TileVisual_01_VariantB", "overlay_mesh": None, "base_triangles": base_tris, "overlay_triangles": 0, "combined_triangles": base_tris, "budget_cap": 249, "status": "PASS" if base_tris <= 249 else "FAIL"},
    ]
    for ovl_name in OVERLAY_ASSET_NAMES:
        otris = ovl_metrics[ovl_name]["total_triangles"]
        comb = base_tris + otris
        allowed_states.append({
            "state_id": f"State_With_{ovl_name}",
            "base_mesh": "SM_Arena_TileVisual_01_VariantA_or_B",
            "overlay_mesh": ovl_name,
            "base_triangles": base_tris,
            "overlay_triangles": otris,
            "combined_triangles": comb,
            "budget_cap": 249,
            "status": "PASS" if comb <= 249 else "FAIL",
        })

    print(f"Generated SM_Arena_TileVisual_01 Variant A & Variant B ({base_tris} tris each) and {len(OVERLAY_ASSET_NAMES)} overlays in {out_dir}")
    for st in allowed_states:
        print(f"  {st['state_id']:45s}: Base={st['base_triangles']:3d} + Overlay={st['overlay_triangles']:2d} = {st['combined_triangles']:3d} / {st['budget_cap']} -> {st['status']}")


if __name__ == "__main__":
    main()
