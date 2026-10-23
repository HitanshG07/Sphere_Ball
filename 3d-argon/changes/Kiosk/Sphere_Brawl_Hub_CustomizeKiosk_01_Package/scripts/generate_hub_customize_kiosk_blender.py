#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — DETERMINISTIC BLENDER 3.6+ / 4.x & PYTHON GENERATOR
Asset ID: SM_Hub_CustomizeKiosk_01 (Hub Customization Kiosk — Argon Step 3)
===================================================================================
- Locked World Placement: (-43.0000, 150.0000, -300.0000)
- Intended World Orientation: CFrame.lookAt(Vector3.new(-43, 150, -300), Vector3.new(0, 150, -300))
  (Rotates local +Z forward to face +X inward toward the main plaza and Queue Portal at (0, 150, -300))
- Local Origin / Pivot: (0.0000, 0.0000, 0.0000) at the floor-reference center of the kiosk footprint
- Local Bounding Envelope:
  * Width (Local X): 10.0000 studs (X in [-5.0000, +5.0000])
  * Height (Local Y): 9.5000 studs (Y in [0.0000, +9.5000])
  * Depth (Local Z): 8.0000 studs (Z in [-4.0000, +4.0000])
- World-Aligned Bounds when placed at (-43, 150, -300) facing +X:
  * World X: [-47.0000, -39.0000] (8.0000 studs along X; rear hull at -47.0, front approach toe at -39.0)
  * World Y: [150.0000, 159.5000] (9.5000 studs height; base flush on walking surface World Y = 150.0000)
  * World Z: [-305.0000, -295.0000] (10.0000 studs along Z; symmetric around Z = -300.0000)
- Four Separate Display Pedestals & Four Replaceable Generic Preview Spheres:
  * Stadium-stepped arc arrangement so all 4 preview spheres are 100% unobstructed from player height:
    - Pedestal 01 (Outer Left):  Local (-3.3500, Y, +0.5500) | Sphere 01 Center: (-3.3500, 3.0500, +0.5500), R = 0.9000
    - Pedestal 02 (Inner Left):  Local (-1.1500, Y, -0.4500) | Sphere 02 Center: (-1.1500, 3.5000, -0.4500), R = 0.9000
    - Pedestal 03 (Inner Right): Local (+1.1500, Y, -0.4500) | Sphere 03 Center: (+1.1500, 3.5000, -0.4500), R = 0.9000
    - Pedestal 04 (Outer Right): Local (+3.3500, Y, +0.5500) | Sphere 04 Center: (+3.3500, 3.0500, +0.5500), R = 0.9000

Usage:
  1. In standard Python 3 (builds deterministic .obj, .mtl, .glb, palette atlas, and optional collision proxy):
     python3 generate_hub_customize_kiosk_blender.py --out_dir ./exports
  2. In Blender 3.6+ / 4.x (builds scene, saves .blend, and exports .obj/.mtl/.glb):
     blender --background --python generate_hub_customize_kiosk_blender.py -- --out_dir ./exports
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
    "MAT_DarkNeutral": (32, 38, 54),     # #202636 — Main kiosk body, heavy base structures, principal pedestal shafts
    "MAT_AltNeutral":  (42, 50, 70),     # #2A3246 — Secondary panels, contrasting mounts, generic preview spheres, header signboard
    "MAT_LightTrim":   (170, 190, 215),  # #AABED7 — Selective bevels, metallic edge guards, cradle claws, display bezels
    "EMI_Cyan":        (0, 195, 255),    # #00C3FF — Recessed illuminated channels, pedestal emitter rings, status strips
}

PALETTE = {
    k: (v[0] / 255.0, v[1] / 255.0, v[2] / 255.0, 1.0)
    for k, v in PALETTE_SRGB.items()
}

APPROVED_PALETTE_METADATA = {
    "MAT_DarkNeutral": {
        "rgb_255": [32, 38, 54],
        "hex": "#202636",
        "normalized_rgb": [round(32 / 255.0, 6), round(38 / 255.0, 6), round(54 / 255.0, 6)],
        "emissive": False,
        "metallic": 0.55,
        "roughness": 0.42,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(32, 38, 54)",
        "surface_role": "Main kiosk body, heavy base platform, structural gantry pillars, and principal pedestal shafts",
    },
    "MAT_AltNeutral": {
        "rgb_255": [42, 50, 70],
        "hex": "#2A3246",
        "normalized_rgb": [round(42 / 255.0, 6), round(50 / 255.0, 6), round(70 / 255.0, 6)],
        "emissive": False,
        "metallic": 0.60,
        "roughness": 0.35,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(42, 50, 70)",
        "surface_role": "Secondary armor panels, contrasting pedestal collars, blank display header board, and neutral placeholder preview spheres",
    },
    "MAT_LightTrim": {
        "rgb_255": [170, 190, 215],
        "hex": "#AABED7",
        "normalized_rgb": [round(170 / 255.0, 6), round(190 / 255.0, 6), round(215 / 255.0, 6)],
        "emissive": False,
        "metallic": 0.78,
        "roughness": 0.28,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(170, 190, 215)",
        "surface_role": "Selective edge bevels, corner mounting cleats, display header bezels, and pedestal label plaques",
    },
    "EMI_Cyan": {
        "rgb_255": [0, 195, 255],
        "hex": "#00C3FF",
        "normalized_rgb": [round(0 / 255.0, 6), round(195 / 255.0, 6), round(255 / 255.0, 6)],
        "emissive": True,
        "metallic": 0.10,
        "roughness": 0.15,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(0, 195, 255)",
        "surface_role": "Recessed illuminated floor channels, pedestal holo-emitter rings, pillar conduit strips, and header accent bars",
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
ATLAS_FILENAME = "SphereBrawl_CustomizeKiosk_PaletteAtlas.png"


# ==============================================================================
# DETERMINISTIC MULTI-COMPONENT HARD-SURFACE MESH BUILDER
# ==============================================================================
class CustomizeKioskMeshBuilder:
    def __init__(self, name="SM_Hub_CustomizeKiosk_01"):
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

    def add_closed_loft(self, comp_name, mat_name, loop_bot, loop_top, cap_bot=True, cap_top=True):
        """
        Lofts a closed 3D solid between two loops with outward normals verified against the centroid.
        """
        n = len(loop_bot)
        assert len(loop_top) == n and n >= 3
        pts_b = [np.array(p, dtype=np.float64) for p in loop_bot]
        pts_t = [np.array(p, dtype=np.float64) for p in loop_top]
        center_b = np.mean(pts_b, axis=0)
        center_t = np.mean(pts_t, axis=0)
        center_mid = 0.5 * (center_b + center_t)

        for i in range(n):
            j = (i + 1) % n
            b0, b1 = pts_b[i], pts_b[j]
            t0, t1 = pts_t[i], pts_t[j]
            quad_mid = 0.25 * (b0 + b1 + t0 + t1)
            out_dir = quad_mid - center_mid
            out_dir[1] *= 0.25
            if np.linalg.norm(out_dir) < 1e-6:
                out_dir = np.array([0.0, 0.0, 1.0])
            self.add_quad(comp_name, mat_name, b0, b1, t1, t0, expected_normal=out_dir)

        if cap_top:
            for i in range(1, n - 1):
                self.add_tri(comp_name, mat_name, pts_t[0], pts_t[i], pts_t[i + 1], expected_normal=(0.0, 1.0, 0.0))

        if cap_bot:
            for i in range(1, n - 1):
                self.add_tri(comp_name, mat_name, pts_b[0], pts_b[i + 1], pts_b[i], expected_normal=(0.0, -1.0, 0.0))

    def add_beveled_box(self, comp_name, mat_name, x0, x1, y0, y1, z0, z1, b_xz=0.12, b_top=0.0, cap_bot=True, cap_top=True):
        """
        Builds an 8-sided chamfered box in XZ with optional top chamfer.
        - When b_top == 0: 8 side walls (16 tris) + top cap (6 tris) + bot cap (6 tris) = 28 tris (or 22 without bot cap).
        - When b_top > 0: 16 side + 16 top bevel + 6 top + 6 bot = 44 tris (or 38 without bot cap).
        """
        def oct_loop(xmin, xmax, y, zmin, zmax, c):
            return [
                (xmin + c, y, zmax),
                (xmax - c, y, zmax),
                (xmax, y, zmax - c),
                (xmax, y, zmin + c),
                (xmax - c, y, zmin),
                (xmin + c, y, zmin),
                (xmin, y, zmin + c),
                (xmin, y, zmax - c),
            ]

        c = min(b_xz, 0.35 * (x1 - x0), 0.35 * (z1 - z0))
        if b_top > 1e-4 and (y1 - y0) > 2.2 * b_top:
            ym = y1 - b_top
            loop_b = oct_loop(x0, x1, y0, z0, z1, c)
            loop_m = oct_loop(x0, x1, ym, z0, z1, c)
            loop_t = oct_loop(x0 + b_top, x1 - b_top, y1, z0 + b_top, z1 - b_top, c * 0.85)
            self.add_closed_loft(comp_name, mat_name, loop_b, loop_m, cap_bot=cap_bot, cap_top=False)
            self.add_closed_loft(comp_name, mat_name, loop_m, loop_t, cap_bot=False, cap_top=cap_top)
        else:
            loop_b = oct_loop(x0, x1, y0, z0, z1, c)
            loop_t = oct_loop(x0, x1, y1, z0, z1, c)
            self.add_closed_loft(comp_name, mat_name, loop_b, loop_t, cap_bot=cap_bot, cap_top=cap_top)

    def add_simple_box(self, comp_name, mat_name, x0, x1, y0, y1, z0, z1, cap_bot=True, cap_top=True):
        loop_b = [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)]
        loop_t = [(x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)]
        self.add_closed_loft(comp_name, mat_name, loop_b, loop_t, cap_bot=cap_bot, cap_top=cap_top)

    def add_frustum_prism(self, comp_name, mat_name, cx, cz, r_bot, r_top, y_bot, y_top, segs=8, rot_offset=math.pi / 8.0, cap_bot=True, cap_top=True):
        loop_b = []
        loop_t = []
        for i in range(segs):
            ang = rot_offset + 2.0 * math.pi * i / segs
            ca, sa = math.cos(ang), math.sin(ang)
            loop_b.append((cx + r_bot * ca, y_bot, cz + r_bot * sa))
            loop_t.append((cx + r_top * ca, y_top, cz + r_top * sa))
        self.add_closed_loft(comp_name, mat_name, loop_b, loop_t, cap_bot=cap_bot, cap_top=cap_top)

    def add_annulus_ring(self, comp_name, mat_name, cx, cz, r_in, r_out, y_bot, y_top, segs=8, rot_offset=math.pi / 8.0, cap_bot=False):
        """Builds a 3D ring collar with inner wall, outer wall, top face, and optional bottom face."""
        for i in range(segs):
            j = (i + 1) % segs
            a0 = rot_offset + 2.0 * math.pi * i / segs
            a1 = rot_offset + 2.0 * math.pi * j / segs
            am = 0.5 * (a0 + a1)
            c0, s0 = math.cos(a0), math.sin(a0)
            c1, s1 = math.cos(a1), math.sin(a1)
            cm, sm = math.cos(am), math.sin(am)

            ib0 = (cx + r_in * c0, y_bot, cz + r_in * s0)
            ib1 = (cx + r_in * c1, y_bot, cz + r_in * s1)
            it0 = (cx + r_in * c0, y_top, cz + r_in * s0)
            it1 = (cx + r_in * c1, y_top, cz + r_in * s1)

            ob0 = (cx + r_out * c0, y_bot, cz + r_out * s0)
            ob1 = (cx + r_out * c1, y_bot, cz + r_out * s1)
            ot0 = (cx + r_out * c0, y_top, cz + r_out * s0)
            ot1 = (cx + r_out * c1, y_top, cz + r_out * s1)

            self.add_quad(comp_name, mat_name, ob0, ob1, ot1, ot0, expected_normal=(cm, 0.0, sm))
            self.add_quad(comp_name, mat_name, ib1, ib0, it0, it1, expected_normal=(-cm, 0.0, -sm))
            self.add_quad(comp_name, mat_name, it0, it1, ot1, ot0, expected_normal=(0.0, 1.0, 0.0))
            if cap_bot:
                self.add_quad(comp_name, mat_name, ob0, ob1, ib1, ib0, expected_normal=(0.0, -1.0, 0.0))

    def add_uv_sphere(self, comp_name, mat_name, cx, cy, cz, radius=0.9000, n_lon=12, n_lat=6):
        """
        Builds a clean, watertight UV sphere for replaceable generic preview spheres.
        With n_lon=12, n_lat=6:
          - Top polar fan: 12 tris
          - Bottom polar fan: 12 tris
          - 3 middle latitude bands: 3 * 12 * 2 = 72 tris
          - Total = 96 triangles per sphere (384 triangles across all 4 spheres).
        """
        top_pole = (cx, cy + radius, cz)
        bot_pole = (cx, cy - radius, cz)

        rings = []
        for lat_i in range(1, n_lat):
            phi = math.pi * lat_i / n_lat
            y = cy + radius * math.cos(phi)
            r_ring = radius * math.sin(phi)
            ring_pts = []
            for lon_i in range(n_lon):
                theta = 2.0 * math.pi * lon_i / n_lon
                x = cx + r_ring * math.cos(theta)
                z = cz + r_ring * math.sin(theta)
                ring_pts.append((x, y, z))
            rings.append(ring_pts)

        first_ring = rings[0]
        for i in range(n_lon):
            j = (i + 1) % n_lon
            p0 = first_ring[i]
            p1 = first_ring[j]
            mid = np.mean([top_pole, p0, p1], axis=0) - np.array([cx, cy, cz])
            self.add_tri(comp_name, mat_name, top_pole, p1, p0, expected_normal=mid)

        for r_idx in range(len(rings) - 1):
            r_upper = rings[r_idx]
            r_lower = rings[r_idx + 1]
            for i in range(n_lon):
                j = (i + 1) % n_lon
                u0, u1 = r_upper[i], r_upper[j]
                l0, l1 = r_lower[i], r_lower[j]
                mid = 0.25 * (np.array(u0) + np.array(u1) + np.array(l0) + np.array(l1)) - np.array([cx, cy, cz])
                self.add_quad(comp_name, mat_name, l0, l1, u1, u0, expected_normal=mid)

        last_ring = rings[-1]
        for i in range(n_lon):
            j = (i + 1) % n_lon
            p0 = last_ring[i]
            p1 = last_ring[j]
            mid = np.mean([bot_pole, p0, p1], axis=0) - np.array([cx, cy, cz])
            self.add_tri(comp_name, mat_name, bot_pole, p0, p1, expected_normal=mid)

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
            of.write("# Sphere Brawl: Rolling Rampage — Kinetic Hub Customization Kiosk 3D Asset\n")
            of.write(f"# Asset Name: {self.name}\n")
            of.write("# Unit Scale: 1.0 Unit = 1.0 Roblox Stud | Up Axis: +Y | Forward Axis: +Z\n")
            of.write("# Local Origin (0,0,0): Floor-Reference Center of Footprint (Maps to World (-43, 150, -300) facing +X)\n")
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
            "name": "SphereBrawl_CustomizeKiosk_PaletteAtlas",
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
            "name": "SphereBrawl_CustomizeKiosk_PaletteAtlas_Tex",
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
                "generator": "Sphere Brawl Customization Kiosk Pipeline v1.0 (Multi-Node + VertexColor + AtlasUV)",
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
# PROCEDURAL GEOMETRY CONSTRUCTION FOR SM_Hub_CustomizeKiosk_01
# ==============================================================================
PEDESTAL_SPECS = [
    {
        "index": 1,
        "pedestal_name": "GEO_CustomizeKiosk_DisplayPedestal_01",
        "sphere_name": "GEO_CustomizeKiosk_PreviewSphere_01",
        "slot_label": "Slot 01 (Outer Left — Front Wing)",
        "cx": -3.3500,
        "cz": +0.5500,
        "tier": "front_outer",
        "mount_top_y": 2.0000,
        "sphere_center_y": 3.0500,
        "sphere_radius": 0.9000,
    },
    {
        "index": 2,
        "pedestal_name": "GEO_CustomizeKiosk_DisplayPedestal_02",
        "sphere_name": "GEO_CustomizeKiosk_PreviewSphere_02",
        "slot_label": "Slot 02 (Inner Left — Elevated Center-Rear)",
        "cx": -1.1500,
        "cz": -0.4500,
        "tier": "rear_inner",
        "mount_top_y": 2.4500,
        "sphere_center_y": 3.5000,
        "sphere_radius": 0.9000,
    },
    {
        "index": 3,
        "pedestal_name": "GEO_CustomizeKiosk_DisplayPedestal_03",
        "sphere_name": "GEO_CustomizeKiosk_PreviewSphere_03",
        "slot_label": "Slot 03 (Inner Right — Elevated Center-Rear)",
        "cx": +1.1500,
        "cz": -0.4500,
        "tier": "rear_inner",
        "mount_top_y": 2.4500,
        "sphere_center_y": 3.5000,
        "sphere_radius": 0.9000,
    },
    {
        "index": 4,
        "pedestal_name": "GEO_CustomizeKiosk_DisplayPedestal_04",
        "sphere_name": "GEO_CustomizeKiosk_PreviewSphere_04",
        "slot_label": "Slot 04 (Outer Right — Front Wing)",
        "cx": +3.3500,
        "cz": +0.5500,
        "tier": "front_outer",
        "mount_top_y": 2.0000,
        "sphere_center_y": 3.0500,
        "sphere_radius": 0.9000,
    },
]

CUSTOMIZE_KIOSK_PARAMS = {
    "asset_name": "SM_Hub_CustomizeKiosk_01",
    "proposed_envelope_studs": [10.0, 9.5, 8.0],
    "measured_local_envelope_studs": [10.0000, 9.5000, 8.0000],
    "local_bbox_min": [-5.0000, 0.0000, -4.0000],
    "local_bbox_max": [+5.0000, +9.5000, +4.0000],
    "local_pivot": [0.0000, 0.0000, 0.0000],
    "locked_world_position": [-43.0000, 150.0000, -300.0000],
    "intended_world_cframe": "CFrame.lookAt(Vector3.new(-43, 150, -300), Vector3.new(0, 150, -300))",
    "world_rotation_yaw_deg": -90.0,
    "world_facing_direction": "+X (Vector3.new(1, 0, 0)) inward toward Queue Portal at (0, 150, -300)",
    "world_aligned_bbox_min": [-47.0000, 150.0000, -305.0000],
    "world_aligned_bbox_max": [-39.0000, 159.5000, -295.0000],
    "world_aligned_dimensions": [8.0000, 9.5000, 10.0000],
    "design_triangle_target": 1850,
    "max_triangle_budget": 2500,
    "pedestals": PEDESTAL_SPECS,
}


def build_hub_customize_kiosk():
    """
    Constructs SM_Hub_CustomizeKiosk_01 with 14 material-separated, named child components:
      1.  GEO_CustomizeKiosk_Base               (MAT_DarkNeutral)
      2.  GEO_CustomizeKiosk_Frame              (MAT_DarkNeutral)
      3.  GEO_CustomizeKiosk_SecondaryPanels    (MAT_AltNeutral)
      4.  GEO_CustomizeKiosk_DisplayPedestal_01 (MAT_DarkNeutral)
      5.  GEO_CustomizeKiosk_DisplayPedestal_02 (MAT_DarkNeutral)
      6.  GEO_CustomizeKiosk_DisplayPedestal_03 (MAT_DarkNeutral)
      7.  GEO_CustomizeKiosk_DisplayPedestal_04 (MAT_DarkNeutral)
      8.  GEO_CustomizeKiosk_PreviewSphere_01   (MAT_AltNeutral)
      9.  GEO_CustomizeKiosk_PreviewSphere_02   (MAT_AltNeutral)
      10. GEO_CustomizeKiosk_PreviewSphere_03   (MAT_AltNeutral)
      11. GEO_CustomizeKiosk_PreviewSphere_04   (MAT_AltNeutral)
      12. GEO_CustomizeKiosk_DisplayHeader      (MAT_AltNeutral)
      13. GEO_CustomizeKiosk_Trim               (MAT_LightTrim)
      14. GEO_CustomizeKiosk_CyanAccents        (EMI_Cyan)

    Exact envelope:
      Local X in [-5.0000, +5.0000] (Width = 10.0000 studs)
      Local Y in [ 0.0000, +9.5000] (Height = 9.5000 studs)
      Local Z in [-4.0000, +4.0000] (Depth = 8.0000 studs)
    """
    mb = CustomizeKioskMeshBuilder("SM_Hub_CustomizeKiosk_01")

    comp_defs = [
        ("GEO_CustomizeKiosk_Base", "MAT_DarkNeutral"),
        ("GEO_CustomizeKiosk_Frame", "MAT_DarkNeutral"),
        ("GEO_CustomizeKiosk_SecondaryPanels", "MAT_AltNeutral"),
        ("GEO_CustomizeKiosk_DisplayPedestal_01", "MAT_DarkNeutral"),
        ("GEO_CustomizeKiosk_DisplayPedestal_02", "MAT_DarkNeutral"),
        ("GEO_CustomizeKiosk_DisplayPedestal_03", "MAT_DarkNeutral"),
        ("GEO_CustomizeKiosk_DisplayPedestal_04", "MAT_DarkNeutral"),
        ("GEO_CustomizeKiosk_PreviewSphere_01", "MAT_AltNeutral"),
        ("GEO_CustomizeKiosk_PreviewSphere_02", "MAT_AltNeutral"),
        ("GEO_CustomizeKiosk_PreviewSphere_03", "MAT_AltNeutral"),
        ("GEO_CustomizeKiosk_PreviewSphere_04", "MAT_AltNeutral"),
        ("GEO_CustomizeKiosk_DisplayHeader", "MAT_AltNeutral"),
        ("GEO_CustomizeKiosk_Trim", "MAT_LightTrim"),
        ("GEO_CustomizeKiosk_CyanAccents", "EMI_Cyan"),
    ]
    for cname, mname in comp_defs:
        mb.ensure_component(cname, mname)

    # ==========================================================================
    # 1. GEO_CustomizeKiosk_Base (MAT_DarkNeutral) — 116 triangles
    # ==========================================================================
    # Main stepped polygonal kiosk base platform spanning X in [-5.0, +5.0], Z in [-4.0, +4.0], Y in [0.0, 0.36]
    base_loop_bot = [
        (-3.9000, 0.0000, +4.0000),
        (+3.9000, 0.0000, +4.0000),
        (+5.0000, 0.0000, +2.8000),
        (+5.0000, 0.0000, -3.2000),
        (+4.2000, 0.0000, -4.0000),
        (-4.2000, 0.0000, -4.0000),
        (-5.0000, 0.0000, -3.2000),
        (-5.0000, 0.0000, +2.8000),
    ]
    base_loop_mid = [
        (-3.8200, 0.2400, +3.9200),
        (+3.8200, 0.2400, +3.9200),
        (+4.9200, 0.2400, +2.7400),
        (+4.9200, 0.2400, -3.1400),
        (+4.1400, 0.2400, -3.9200),
        (-4.1400, 0.2400, -3.9200),
        (-4.9200, 0.2400, -3.1400),
        (-4.9200, 0.2400, +2.7400),
    ]
    base_loop_top = [
        (-3.6500, 0.3600, +3.7200),
        (+3.6500, 0.3600, +3.7200),
        (+4.7200, 0.3600, +2.6000),
        (+4.7200, 0.3600, -3.0200),
        (+4.0000, 0.3600, -3.7600),
        (-4.0000, 0.3600, -3.7600),
        (-4.7200, 0.3600, -3.0200),
        (-4.7200, 0.3600, +2.6000),
    ]
    mb.add_closed_loft("GEO_CustomizeKiosk_Base", "MAT_DarkNeutral", base_loop_bot, base_loop_mid, cap_bot=True, cap_top=False)
    mb.add_closed_loft("GEO_CustomizeKiosk_Base", "MAT_DarkNeutral", base_loop_mid, base_loop_top, cap_bot=False, cap_top=True)

    # Rear-center stadium riser deck (elevates Pedestals 02 & 03 so rear spheres are never hidden behind front spheres)
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_Base", "MAT_DarkNeutral",
        x0=-2.5500, x1=+2.5500, y0=0.3600, y1=0.6800, z0=-2.6500, z1=+0.5500,
        b_xz=0.28, b_top=0.06, cap_bot=False, cap_top=True
    )

    # Rear structural spine plinth supporting the gantry columns (Z in [-3.72, -1.95], Y in [0.36, 1.30])
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_Base", "MAT_DarkNeutral",
        x0=-4.3500, x1=+4.3500, y0=0.3600, y1=1.3000, z0=-3.7200, z1=-1.9500,
        b_xz=0.30, b_top=0.08, cap_bot=False, cap_top=True
    )

    # ==========================================================================
    # 2. GEO_CustomizeKiosk_Frame (MAT_DarkNeutral) — 178 triangles
    # ==========================================================================
    # Left & Right Main Angled Gantry Pillars rising from rear plinth (Y = 1.25 to 7.85)
    for sx in (-1.0, +1.0):
        cx_bot = sx * 3.8500
        cx_mid = sx * 3.9500
        cx_top = sx * 3.6500

        p_b = [
            (cx_bot - 0.52, 1.2500, -2.0500),
            (cx_bot + 0.52, 1.2500, -2.0500),
            (cx_bot + 0.52, 1.2500, -3.5800),
            (cx_bot - 0.52, 1.2500, -3.5800),
        ]
        p_m = [
            (cx_mid - 0.48, 4.8000, -1.9500),
            (cx_mid + 0.48, 4.8000, -1.9500),
            (cx_mid + 0.48, 4.8000, -3.4800),
            (cx_mid - 0.48, 4.8000, -3.4800),
        ]
        p_t = [
            (cx_top - 0.44, 7.8500, -0.8500),
            (cx_top + 0.44, 7.8500, -0.8500),
            (cx_top + 0.44, 7.8500, -2.4500),
            (cx_top - 0.44, 7.8500, -2.4500),
        ]
        mb.add_closed_loft("GEO_CustomizeKiosk_Frame", "MAT_DarkNeutral", p_b, p_m, cap_bot=False, cap_top=False)
        mb.add_closed_loft("GEO_CustomizeKiosk_Frame", "MAT_DarkNeutral", p_m, p_t, cap_bot=False, cap_top=True)

        # Forward-cantilevered upper canopy arm (Y: 7.45 -> 8.65, reaching forward to Z = +1.25)
        arm_b = [
            (cx_top - 0.42, 7.4500, +1.2500),
            (cx_top + 0.42, 7.4500, +1.2500),
            (cx_top + 0.46, 7.4500, -2.5500),
            (cx_top - 0.46, 7.4500, -2.5500),
        ]
        arm_t = [
            (cx_top - 0.38, 8.6500, +1.0500),
            (cx_top + 0.38, 8.6500, +1.0500),
            (cx_top + 0.44, 8.6500, -2.3500),
            (cx_top - 0.44, 8.6500, -2.3500),
        ]
        mb.add_closed_loft("GEO_CustomizeKiosk_Frame", "MAT_DarkNeutral", arm_b, arm_t, cap_bot=True, cap_top=True)

        # Rear external diagonal buttress fin (gives finished industrial back/side silhouette)
        fin_b = [
            (cx_bot - 0.28, 0.3600, -3.4000),
            (cx_bot + 0.28, 0.3600, -3.4000),
            (cx_bot + 0.24, 0.3600, -3.9600),
            (cx_bot - 0.24, 0.3600, -3.9600),
        ]
        fin_t = [
            (cx_mid - 0.24, 4.4000, -3.2000),
            (cx_mid + 0.24, 4.4000, -3.2000),
            (cx_mid + 0.20, 4.4000, -3.6200),
            (cx_mid - 0.20, 4.4000, -3.6200),
        ]
        mb.add_closed_loft("GEO_CustomizeKiosk_Frame", "MAT_DarkNeutral", fin_b, fin_t, cap_bot=False, cap_top=True)

    # Central rear reactor/telemetry spine column (X in [-1.15, +1.15], Y in [1.25, 7.65], Z in [-3.62, -2.25])
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_Frame", "MAT_DarkNeutral",
        x0=-1.1500, x1=+1.1500, y0=1.2500, y1=7.6500, z0=-3.6200, z1=-2.2500,
        b_xz=0.22, b_top=0.0, cap_bot=False, cap_top=False
    )

    # Mid-height horizontal stabilizer crossbeam linking Left Pillar, Central Spine, and Right Pillar
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_Frame", "MAT_DarkNeutral",
        x0=-4.3000, x1=+4.3000, y0=4.5500, y1=5.3500, z0=-3.5500, z1=-2.3500,
        b_xz=0.16, b_top=0.0, cap_bot=True, cap_top=True
    )

    # Upper canopy structural crown bridge spanning X in [-4.45, +4.45], Y in [7.55, 9.22], Z in [-2.45, +0.85]
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_Frame", "MAT_DarkNeutral",
        x0=-4.4500, x1=+4.4500, y0=7.5500, y1=9.2200, z0=-2.4500, z1=+0.8500,
        b_xz=0.32, b_top=0.10, cap_bot=True, cap_top=True
    )
    # Uppermost crest cap reaching exact Local Y = 9.5000 studs
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_Frame", "MAT_DarkNeutral",
        x0=-3.2500, x1=+3.2500, y0=9.2200, y1=9.5000, z0=-1.8500, z1=+0.4500,
        b_xz=0.24, b_top=0.0, cap_bot=False, cap_top=True
    )

    # ==========================================================================
    # 3. GEO_CustomizeKiosk_SecondaryPanels (MAT_AltNeutral) — 152 triangles
    # ==========================================================================
    # Front approach step inlay plate on the main base
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_SecondaryPanels", "MAT_AltNeutral",
        x0=-3.1000, x1=+3.1000, y0=0.3600, y1=0.4200, z0=+1.1500, z1=+3.4500,
        b_xz=0.20, b_top=0.0, cap_bot=False, cap_top=True
    )

    # Rear engineering access panels on the back of the spine & crossbeam (finished rear detailing)
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_SecondaryPanels", "MAT_AltNeutral",
        x0=-3.4000, x1=-1.4500, y0=1.6500, y1=4.3500, z0=-3.5200, z1=-2.5500,
        b_xz=0.14, b_top=0.0, cap_bot=False, cap_top=True
    )
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_SecondaryPanels", "MAT_AltNeutral",
        x0=+1.4500, x1=+3.4000, y0=1.6500, y1=4.3500, z0=-3.5200, z1=-2.5500,
        b_xz=0.14, b_top=0.0, cap_bot=False, cap_top=True
    )

    # Central spine front telemetry housing shroud
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_SecondaryPanels", "MAT_AltNeutral",
        x0=-0.8800, x1=+0.8800, y0=4.2000, y1=7.2500, z0=-2.3000, z1=-1.7800,
        b_xz=0.12, b_top=0.0, cap_bot=True, cap_top=True
    )

    # Contrasting upper cradle emitter collars on each of the 4 pedestals
    for p in PEDESTAL_SPECS:
        cx, cz = p["cx"], p["cz"]
        m_top = p["mount_top_y"]
        mb.add_frustum_prism(
            "GEO_CustomizeKiosk_SecondaryPanels", "MAT_AltNeutral",
            cx=cx, cz=cz, r_bot=0.6800, r_top=0.8400,
            y_bot=m_top - 0.2800, y_top=m_top,
            segs=8, cap_bot=False, cap_top=True
        )

    # ==========================================================================
    # 4. GEO_CustomizeKiosk_DisplayPedestal_01 .. _04 (MAT_DarkNeutral) — 4 * 96 = 384 tris
    # ==========================================================================
    for p in PEDESTAL_SPECS:
        comp_p = p["pedestal_name"]
        cx, cz = p["cx"], p["cz"]
        m_top = p["mount_top_y"]
        y_floor = 0.3600 if p["tier"] == "front_outer" else 0.6800

        # 1) Distinct octagonal pedestal mounting foot (16 side + 6 top = 22 tris)
        mb.add_frustum_prism(
            comp_p, "MAT_DarkNeutral",
            cx=cx, cz=cz, r_bot=1.0200, r_top=0.8800,
            y_bot=y_floor, y_top=y_floor + 0.2600,
            segs=8, cap_bot=False, cap_top=True
        )
        # 2) Tapered vertical pedestal column body (16 tris)
        mb.add_frustum_prism(
            comp_p, "MAT_DarkNeutral",
            cx=cx, cz=cz, r_bot=0.6800, r_top=0.5800,
            y_bot=y_floor + 0.2600, y_top=m_top - 0.5200,
            segs=8, cap_bot=False, cap_top=False
        )
        # 3) Upper support flared base under the emitter collar (16 + 6 = 22 tris)
        mb.add_frustum_prism(
            comp_p, "MAT_DarkNeutral",
            cx=cx, cz=cz, r_bot=0.5800, r_top=0.7600,
            y_bot=m_top - 0.5200, y_top=m_top - 0.2800,
            segs=8, cap_bot=False, cap_top=True
        )
        # 4) 4 structural sphere-cradle prongs around the upper mount (4 * 10 = 40 tris -> total 100 tris/pedestal)
        for c_ang in (math.pi * 0.25, math.pi * 0.75, math.pi * 1.25, math.pi * 1.75):
            ux, uz = math.cos(c_ang), math.sin(c_ang)
            tx, tz = -uz, ux
            hw = 0.0950
            r_in_b, r_out_b = 0.6600, 0.8500
            r_in_t, r_out_t = 0.7600, 0.9200
            yb, yt = m_top, m_top + 0.2400

            def pt_prong(r, w, y):
                return (cx + r * ux + w * tx, y, cz + r * uz + w * tz)

            loop_pb = [
                pt_prong(r_in_b, -hw, yb),
                pt_prong(r_out_b, -hw, yb),
                pt_prong(r_out_b, +hw, yb),
                pt_prong(r_in_b, +hw, yb),
            ]
            loop_pt = [
                pt_prong(r_in_t, -hw * 0.85, yt),
                pt_prong(r_out_t, -hw * 0.85, yt),
                pt_prong(r_out_t, +hw * 0.85, yt),
                pt_prong(r_in_t, +hw * 0.85, yt),
            ]
            mb.add_closed_loft(comp_p, "MAT_DarkNeutral", loop_pb, loop_pt, cap_bot=False, cap_top=True)

    # ==========================================================================
    # 5. GEO_CustomizeKiosk_PreviewSphere_01 .. _04 (MAT_AltNeutral) — 4 * 96 = 384 tris
    # ==========================================================================
    # Four identical, neutral, replaceable preview spheres (R = 0.9000 studs, 96 tris each)
    for p in PEDESTAL_SPECS:
        mb.add_uv_sphere(
            p["sphere_name"], "MAT_AltNeutral",
            cx=p["cx"], cy=p["sphere_center_y"], cz=p["cz"],
            radius=p["sphere_radius"], n_lon=12, n_lat=6
        )

    # ==========================================================================
    # 6. GEO_CustomizeKiosk_DisplayHeader (MAT_AltNeutral) — 84 triangles
    # ==========================================================================
    # Blank, clearly bounded forward-facing signage header board (for future SurfaceGui / labels)
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_DisplayHeader", "MAT_AltNeutral",
        x0=-3.4500, x1=+3.4500, y0=7.7200, y1=9.0600, z0=+0.7800, z1=+1.2200,
        b_xz=0.14, b_top=0.0, cap_bot=True, cap_top=True
    )
    # Two secondary blank sub-header category display plaques (Left & Right under main header)
    for sx in (-1.0, +1.0):
        mb.add_beveled_box(
            "GEO_CustomizeKiosk_DisplayHeader", "MAT_AltNeutral",
            x0=sx * 2.1500 - 1.0500, x1=sx * 2.1500 + 1.0500,
            y0=7.1200, y1=7.5200, z0=+0.5500, z1=+0.9500,
            b_xz=0.08, b_top=0.0, cap_bot=True, cap_top=True
        )

    # ==========================================================================
    # 7. GEO_CustomizeKiosk_Trim (MAT_LightTrim) — 332 triangles
    # ==========================================================================
    # 1) 4 Precision Corner Mounting Cleats around the main base perimeter (COMP_Hub_CornerBracket_01 family)
    corner_cleats = [
        (-4.8200, -4.1500, +2.4500, +3.6500),
        (+4.1500, +4.8200, +2.4500, +3.6500),
        (-4.8200, -4.1500, -3.6500, -2.4500),
        (+4.1500, +4.8200, -3.6500, -2.4500),
    ]
    for (x0, x1, z0, z1) in corner_cleats:
        mb.add_beveled_box(
            "GEO_CustomizeKiosk_Trim", "MAT_LightTrim",
            x0=x0, x1=x1, y0=0.0400, y1=0.4200, z0=z0, z1=z1,
            b_xz=0.08, b_top=0.0, cap_bot=False, cap_top=True
        )

    # 2) Front approach threshold bevel guard (X in [-2.60, +2.60], Z in [+3.68, +3.96])
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_Trim", "MAT_LightTrim",
        x0=-2.6000, x1=+2.6000, y0=0.1800, y1=0.4100, z0=+3.6800, z1=+3.9600,
        b_xz=0.08, b_top=0.0, cap_bot=False, cap_top=True
    )

    # 3) 4 Blank Pedestal Front Label Plaques (on each pedestal foot for future chassis names)
    for p in PEDESTAL_SPECS:
        cx, cz = p["cx"], p["cz"]
        y_floor = 0.3600 if p["tier"] == "front_outer" else 0.6800
        mb.add_beveled_box(
            "GEO_CustomizeKiosk_Trim", "MAT_LightTrim",
            x0=cx - 0.4600, x1=cx + 0.4600,
            y0=y_floor + 0.0400, y1=y_floor + 0.3200,
            z0=cz + 0.7800, z1=cz + 1.0600,
            b_xz=0.05, b_top=0.0, cap_bot=False, cap_top=True
        )

    # 4) Main Display Header Upper & Lower Metallic Bezels
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_Trim", "MAT_LightTrim",
        x0=-3.6200, x1=+3.6200, y0=9.0600, y1=9.2400, z0=+0.7200, z1=+1.3000,
        b_xz=0.08, b_top=0.0, cap_bot=True, cap_top=True
    )
    mb.add_beveled_box(
        "GEO_CustomizeKiosk_Trim", "MAT_LightTrim",
        x0=-3.6200, x1=+3.6200, y0=7.5400, y1=7.7200, z0=+0.7200, z1=+1.3000,
        b_xz=0.08, b_top=0.0, cap_bot=True, cap_top=True
    )

    # 5) Gantry Pillar Forward Rib Guards (Left & Right)
    for sx in (-1.0, +1.0):
        cx_p = sx * 3.9000
        mb.add_beveled_box(
            "GEO_CustomizeKiosk_Trim", "MAT_LightTrim",
            x0=cx_p - 0.5600, x1=cx_p + 0.5600,
            y0=4.6200, y1=5.1200, z0=-2.0500, z1=-1.7500,
            b_xz=0.06, b_top=0.0, cap_bot=True, cap_top=True
        )

    # ==========================================================================
    # 8. GEO_CustomizeKiosk_CyanAccents (EMI_Cyan) — 264 triangles
    # ==========================================================================
    # 1) 4 Pedestal Upper Holo-Emitter Rings (4 * 48 = 192 tris)
    for p in PEDESTAL_SPECS:
        cx, cz = p["cx"], p["cz"]
        m_top = p["mount_top_y"]
        mb.add_annulus_ring(
            "GEO_CustomizeKiosk_CyanAccents", "EMI_Cyan",
            cx=cx, cz=cz, r_in=0.4200, r_out=0.6600,
            y_bot=m_top, y_top=m_top + 0.0500, segs=8, cap_bot=False
        )

    # 2) Main Display Header Recessed Top & Bottom Cyan Accent Strips (2 * 10 = 20 tris)
    mb.add_simple_box(
        "GEO_CustomizeKiosk_CyanAccents", "EMI_Cyan",
        x0=-3.2500, x1=+3.2500, y0=8.9400, y1=9.0400, z0=+1.1800, z1=+1.2600,
        cap_bot=False, cap_top=True
    )
    mb.add_simple_box(
        "GEO_CustomizeKiosk_CyanAccents", "EMI_Cyan",
        x0=-3.2500, x1=+3.2500, y0=7.7400, y1=7.8400, z0=+1.1800, z1=+1.2600,
        cap_bot=True, cap_top=False
    )

    # 3) Left & Right Gantry Pillar Vertical Cyan Energy Conduits (2 * 10 = 20 tris)
    for sx in (-1.0, +1.0):
        cx_p = sx * 3.9000
        mb.add_simple_box(
            "GEO_CustomizeKiosk_CyanAccents", "EMI_Cyan",
            x0=cx_p - 0.1200, x1=cx_p + 0.1200,
            y0=1.5500, y1=4.5500, z0=-2.0400, z1=-1.9200,
            cap_bot=False, cap_top=True
        )

    # 4) Central Spine Vertical Core Status Strip (10 tris)
    mb.add_simple_box(
        "GEO_CustomizeKiosk_CyanAccents", "EMI_Cyan",
        x0=-0.1600, x1=+0.1600, y0=4.4500, y1=7.0500, z0=-1.8200, z1=-1.7200,
        cap_bot=False, cap_top=True
    )

    # 5) Base Deck Recessed Cyan Guidance Strips (2 * 10 = 20 tris)
    mb.add_simple_box(
        "GEO_CustomizeKiosk_CyanAccents", "EMI_Cyan",
        x0=-2.4500, x1=+2.4500, y0=0.3600, y1=0.4350, z0=+3.4800, z1=+3.6400,
        cap_bot=False, cap_top=True
    )
    mb.add_simple_box(
        "GEO_CustomizeKiosk_CyanAccents", "EMI_Cyan",
        x0=-2.1500, x1=+2.1500, y0=0.6800, y1=0.7250, z0=+0.3800, z1=+0.5200,
        cap_bot=False, cap_top=True
    )

    # 6) Rear Spine Diagnostic Cyan Status Bar (10 tris)
    mb.add_simple_box(
        "GEO_CustomizeKiosk_CyanAccents", "EMI_Cyan",
        x0=-2.8000, x1=+2.8000, y0=4.8800, y1=5.0200, z0=-3.6000, z1=-3.5000,
        cap_bot=False, cap_top=True
    )

    return mb


def build_collision_proxy():
    """
    Constructs an optional, isolated simple structural collision proxy (COL_CustomizeKiosk_Body)
    protecting the rear structural body while keeping the front approach and all four sphere previews accessible.
    """
    cb = CustomizeKioskMeshBuilder("COL_CustomizeKiosk_Body")
    cb.ensure_component("COL_CustomizeKiosk_RearFrame", "MAT_DarkNeutral")
    cb.ensure_component("COL_CustomizeKiosk_PedestalPlinth", "MAT_DarkNeutral")

    # Rear structural gantry box (X in [-4.60, +4.60], Y in [0.00, 9.50], Z in [-4.00, -1.75])
    cb.add_simple_box(
        "COL_CustomizeKiosk_RearFrame", "MAT_DarkNeutral",
        x0=-4.6000, x1=+4.6000, y0=0.0000, y1=9.5000, z0=-4.0000, z1=-1.7500
    )
    # Lower display table core (X in [-4.20, +4.20], Y in [0.00, 2.35], Z in [-1.75, +1.35])
    cb.add_simple_box(
        "COL_CustomizeKiosk_PedestalPlinth", "MAT_DarkNeutral",
        x0=-4.2000, x1=+4.2000, y0=0.0000, y1=2.3500, z0=-1.7500, z1=+1.3500
    )
    return cb


def rblx_to_blender(pt):
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

    col = bpy.data.collections.new(mb.name)
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

    root_empty = bpy.data.objects.new(mb.name, None)
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

    mb = build_hub_customize_kiosk()
    obj_out = os.path.join(out_dir, "SM_Hub_CustomizeKiosk_01.obj")
    mtl_out = os.path.join(out_dir, "SM_Hub_CustomizeKiosk_01.mtl")
    glb_out = os.path.join(out_dir, "SM_Hub_CustomizeKiosk_01.glb")
    mb.export_obj_and_mtl(obj_out, mtl_out)
    mb.export_glb(glb_out)

    # Optional isolated collision proxy
    col_dir = os.path.join(out_dir, "collision_proxy")
    os.makedirs(col_dir, exist_ok=True)
    cb = build_collision_proxy()
    cb.export_obj_and_mtl(
        os.path.join(col_dir, "COL_CustomizeKiosk_Body.obj"),
        os.path.join(col_dir, "COL_CustomizeKiosk_Body.mtl"),
    )
    cb.export_glb(os.path.join(col_dir, "COL_CustomizeKiosk_Body.glb"))

    if HAS_BPY:
        blend_out = os.path.join(out_dir, "SM_Hub_CustomizeKiosk_01.blend")
        build_in_blender(mb, save_blend_path=blend_out)
        print(f"Saved Blender source to {blend_out}")

    total_tris = sum(len(t) for t in mb.comp_tris.values())
    print(f"Successfully generated SM_Hub_CustomizeKiosk_01 in {out_dir} ({total_tris} triangles).")
