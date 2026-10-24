#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — DETERMINISTIC BLENDER 3.6+ / 4.x & PYTHON PRODUCTION GENERATOR
Asset ID: SM_Hub_ShopKiosk_01 (Sphere Brawl Arena Shop Bar — Argon Step 4 Phase 2 Approved Production)
======================================================================================================
- Canonical Asset ID: SM_Hub_ShopKiosk_01
- Descriptive Name: Sphere Brawl Arena Shop Bar
- Approved Concept Source of Truth: Sphere_Brawl_Shop_Bar_Concept_Reset_01.zip
- Architectural Identity: Wide, horizontal, open-front bar-counter arena shop (20.0 x 8.0 x 7.6 studs)
  featuring a continuous 15.10-stud customer-facing bar counter, four distinct non-spherical countertop
  merchandise displays in a single horizontal row, two extended side wings with open shelves, and a
  lightweight suspended SHOP sign panel (blank UI-ready face) held by two slender rear-set struts.
- Locked World Placement: (43.0000, 150.0000, -300.0000)
- Primary World Orientation: CFrame.new(43, 150, -300) * CFrame.Angles(0, math.rad(-90), 0)
- Equivalent Orthonormal Basis: CFrame.fromMatrix(Vector3.new(43, 150, -300), Vector3.new(0, 0, 1), Vector3.new(0, 1, 0), Vector3.new(-1, 0, 0))
  (Maps local +Z forward to world -X inward toward Queue Portal at (0, 150, -300); local +Y to world +Y; local +X right to world +Z)
- Local Origin / Pivot: (0.0000, 0.0000, 0.0000) at the floor-reference center of the footprint (base underside at Y = 0.0000)
- Measured Local Bounding Envelope:
  * Width  (Local X): 20.0000 studs (X in [-10.0000, +10.0000])
  * Height (Local Y):  7.6000 studs (Y in [  0.0000,  +7.6000])
  * Depth  (Local Z):  8.0000 studs (Z in [ -4.0000,  +4.0000])
- Measured World-Aligned Bounds when placed at (43, 150, -300) facing -X:
  * World X: [ 39.0000,  47.0000] ( 8.0000 studs radial depth; front walk-up step at +39.0, rear wing plinth at +47.0)
  * World Y: [150.0000, 157.6000] ( 7.6000 studs vertical height; base flush on walking surface World Y = 150.0000)
  * World Z: [-310.0000, -290.0000] (20.0000 studs tangential width; symmetric around Z = -300.0000)
- Four Non-Spherical Countertop Merchandise Displays (Single Row along Countertop at Z = +0.25):
  * Slot 01 (X = -5.10): GEO_ShopKiosk_DisplayPad_01 + GEO_ShopKiosk_DisplayItem_01 (Faceted Hexagonal Emblem / Shield Plate)
    - Local Item Center: (-5.1000, 4.1800, +0.2500) -> World Center: (42.7500, 154.1800, -305.1000)
  * Slot 02 (X = -1.70): GEO_ShopKiosk_DisplayPad_02 + GEO_ShopKiosk_DisplayItem_02 (Vertical Toroidal Halo / Energy-Ring Ornament)
    - Local Item Center: (-1.7000, 4.2200, +0.2500) -> World Center: (42.7500, 154.2200, -301.7000)
  * Slot 03 (X = +1.70): GEO_ShopKiosk_DisplayPad_03 + GEO_ShopKiosk_DisplayItem_03 (Segmented Triple-Chevron Trail-Effect Fins)
    - Local Item Center: (+1.7000, 4.1500, +0.2500) -> World Center: (42.7500, 154.1500, -298.3000)
  * Slot 04 (X = +5.10): GEO_ShopKiosk_DisplayPad_04 + GEO_ShopKiosk_DisplayItem_04 (Geometric Starburst Burst-Effect Prism)
    - Local Item Center: (+5.1000, 4.2500, +0.2500) -> World Center: (42.7500, 154.2500, -294.9000)

Usage:
  1. In standard Python 3 (builds deterministic .obj, .mtl, .glb, palette atlas, and optional collision proxy):
     python3 generate_hub_shop_kiosk_blender.py --out_dir ./exports
  2. In Blender 3.6+ / 4.x (builds scene, saves .blend, and exports .obj/.mtl/.glb):
     blender --background --python generate_hub_shop_kiosk_blender.py -- --out_dir ./exports
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
    "EMI_Amber",
]

PALETTE_SRGB = {
    "MAT_DarkNeutral": (32, 38, 54),     # #202636 — Stepped counter plinth, continuous counter body, side wing hulls, display pad bases, raked sign struts
    "MAT_AltNeutral":  (42, 50, 70),     # #2A3246 — Countertop deck, front fascia armor plates, wing shelves, blank sign panel, 4 non-spherical display items
    "MAT_LightTrim":   (170, 190, 215),  # #AABED7 — Counter front bullnose rail, fascia ribs, corner guards, display sockets/brackets/plaques, sign frame bezel
    "EMI_Cyan":        (0, 195, 255),    # #00C3FF — Recessed counter fascia energy channels, 4 octagonal display pad rings, approach floor guide, sign upper rail
    "EMI_Amber":       (255, 170, 0),    # #FFAA00 — Restrained shop-specific highlights: sign lower rail, top visor center bar, display pad ticks, wing-tip beacons
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
        "surface_role": "Dominant structural dark alloy: two-stage stepped counter plinth, continuous faceted bar counter body, extended side wing hulls, 4 octagonal display pad bases, and slender raked sign support frame",
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
        "surface_role": "Secondary slate metallic: continuous countertop display deck, 4 faceted front fascia armor panels, approach floor inlay plates, extended wing shelf decks, separate blank UI-ready sign panel, and 4 non-spherical display items",
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
        "surface_role": "Light metallic mechanical trim: countertop front bullnose rail, 3 vertical fascia ribs, corner guards, wing edge bumpers, 4 display mounting sockets, lateral presentation brackets, item plaques, and sign bezel frame",
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
        "surface_role": "Principal technology energy accent: upper and lower recessed counter fascia channels, 4 octagonal display pad emitter rings, approach floor guide strip, side wing front bevel strips, and sign top illumination bar",
    },
    "EMI_Amber": {
        "rgb_255": [255, 170, 0],
        "hex": "#FFAA00",
        "normalized_rgb": [round(255 / 255.0, 6), round(170 / 255.0, 6), round(0 / 255.0, 6)],
        "emissive": True,
        "metallic": 0.15,
        "roughness": 0.18,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(255, 170, 0)",
        "surface_role": "Restrained shop-specific highlight: suspended sign lower accent bar, top visor center crown indicator, 4 small countertop item-pad front ticks, and 2 outer wing-tip beacons",
    },
}

DISPLAY_SLOT_SPECS = [
    {
        "index": 1,
        "pad_name": "GEO_ShopKiosk_DisplayPad_01",
        "item_name": "GEO_ShopKiosk_DisplayItem_01",
        "slot_label": "Slot 01 (Countertop Left Outer — X = -5.10)",
        "placeholder_type": "Faceted Hexagonal Emblem / Shield Plate",
        "cx": -5.1000,
        "cy": 4.1800,
        "cz": +0.2500,
        "pad_top_y": 3.1600,
        "socket_top_y": 3.3000,
        "world_item_center": [42.7500, 154.1800, -305.1000],
        "world_pad_center": [42.7500, 153.0400, -305.1000],
    },
    {
        "index": 2,
        "pad_name": "GEO_ShopKiosk_DisplayPad_02",
        "item_name": "GEO_ShopKiosk_DisplayItem_02",
        "slot_label": "Slot 02 (Countertop Left Inner — X = -1.70)",
        "placeholder_type": "Vertical Toroidal Halo / Energy-Ring Ornament",
        "cx": -1.7000,
        "cy": 4.2200,
        "cz": +0.2500,
        "pad_top_y": 3.1600,
        "socket_top_y": 3.3000,
        "world_item_center": [42.7500, 154.2200, -301.7000],
        "world_pad_center": [42.7500, 153.0400, -301.7000],
    },
    {
        "index": 3,
        "pad_name": "GEO_ShopKiosk_DisplayPad_03",
        "item_name": "GEO_ShopKiosk_DisplayItem_03",
        "slot_label": "Slot 03 (Countertop Right Inner — X = +1.70)",
        "placeholder_type": "Segmented Triple-Chevron Trail-Effect Fins",
        "cx": +1.7000,
        "cy": 4.1500,
        "cz": +0.2500,
        "pad_top_y": 3.1600,
        "socket_top_y": 3.3000,
        "world_item_center": [42.7500, 154.1500, -298.3000],
        "world_pad_center": [42.7500, 153.0400, -298.3000],
    },
    {
        "index": 4,
        "pad_name": "GEO_ShopKiosk_DisplayPad_04",
        "item_name": "GEO_ShopKiosk_DisplayItem_04",
        "slot_label": "Slot 04 (Countertop Right Outer — X = +5.10)",
        "placeholder_type": "Geometric Starburst Burst-Effect Prism",
        "cx": +5.1000,
        "cy": 4.2500,
        "cz": +0.2500,
        "pad_top_y": 3.1600,
        "socket_top_y": 3.3000,
        "world_item_center": [42.7500, 154.2500, -294.9000],
        "world_pad_center": [42.7500, 153.0400, -294.9000],
    },
]


def build_palette_atlas_png_bytes():
    """
    Builds a compact 64x64 PNG palette swatch atlas (<= 1024x1024 limit per TASK-09)
    with a 4x2 grid covering all 5 locked materials cleanly.
    """
    img = Image.new("RGB", (64, 64), (32, 38, 54))
    draw = ImageDraw.Draw(img)
    uv_centers_gltf = {}
    uv_centers_obj = {}

    col_w = 16
    row_h = 32
    for idx, mname in enumerate(PALETTE_ORDER):
        col_i = idx % 4
        row_i = idx // 4
        x0, y0 = col_i * col_w, row_i * row_h
        x1, y1 = x0 + col_w - 1, y0 + row_h - 1
        rgb = PALETTE_SRGB[mname]
        draw.rectangle([x0, y0, x1, y1], fill=rgb)

        u = (col_i + 0.5) / 4.0
        v_gltf = (row_i + 0.5) / 2.0
        v_obj = 1.0 - (row_i + 0.5) / 2.0
        uv_centers_gltf[mname] = (round(u, 5), round(v_gltf, 5))
        uv_centers_obj[mname] = (round(u, 5), round(v_obj, 5))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue(), uv_centers_gltf, uv_centers_obj


ATLAS_PNG_BYTES, UV_CENTERS_GLTF, UV_CENTERS_OBJ = build_palette_atlas_png_bytes()
ATLAS_FILENAME = "SphereBrawl_ShopKiosk_PaletteAtlas.png"


# ==============================================================================
# DETERMINISTIC MULTI-COMPONENT HARD-SURFACE MESH BUILDER
# ==============================================================================
class ShopKioskMeshBuilder:
    def __init__(self, name="SM_Hub_ShopKiosk_01"):
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
        Lofts a closed 3D solid between two horizontal loops with outward normals verified against centroid.
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

    def add_closed_loft_axis(self, comp_name, mat_name, loop_front, loop_back, cap_front=True, cap_back=True):
        """
        Lofts a closed 3D solid between a front loop (+Z) and back loop (-Z) for vertical plates/rings.
        """
        n = len(loop_front)
        assert len(loop_back) == n and n >= 3
        pts_f = [np.array(p, dtype=np.float64) for p in loop_front]
        pts_b = [np.array(p, dtype=np.float64) for p in loop_back]
        center_f = np.mean(pts_f, axis=0)
        center_b = np.mean(pts_b, axis=0)
        center_mid = 0.5 * (center_f + center_b)

        for i in range(n):
            j = (i + 1) % n
            f0, f1 = pts_f[i], pts_f[j]
            b0, b1 = pts_b[i], pts_b[j]
            quad_mid = 0.25 * (f0 + f1 + b0 + b1)
            out_dir = quad_mid - center_mid
            out_dir[2] *= 0.25
            if np.linalg.norm(out_dir) < 1e-6:
                out_dir = np.array([0.0, 1.0, 0.0])
            self.add_quad(comp_name, mat_name, b0, b1, f1, f0, expected_normal=out_dir)

        if cap_front:
            for i in range(1, n - 1):
                self.add_tri(comp_name, mat_name, pts_f[0], pts_f[i], pts_f[i + 1], expected_normal=(0.0, 0.0, 1.0))

        if cap_back:
            for i in range(1, n - 1):
                self.add_tri(comp_name, mat_name, pts_b[0], pts_b[i + 1], pts_b[i], expected_normal=(0.0, 0.0, -1.0))

    def add_simple_box(self, comp_name, mat_name, x0, x1, y0, y1, z0, z1, cap_bot=True, cap_top=True):
        loop_b = [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)]
        loop_t = [(x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)]
        self.add_closed_loft(comp_name, mat_name, loop_b, loop_t, cap_bot=cap_bot, cap_top=cap_top)

    def add_beveled_box(self, comp_name, mat_name, x0, x1, y0, y1, z0, z1, b_xz=0.12, b_top=0.0, cap_bot=True, cap_top=True):
        """
        Builds an 8-sided chamfered box in XZ with optional top chamfer.
        """
        def oct_loop(xmin, xmax, y, zmin, zmax, c):
            c = min(c, 0.42 * (xmax - xmin), 0.42 * (zmax - zmin))
            if c <= 1e-5:
                return [(xmin, y, zmax), (xmax, y, zmax), (xmax, y, zmin), (xmin, y, zmin)]
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

        c = min(b_xz, 0.42 * (x1 - x0), 0.42 * (z1 - z0))
        if b_top > 1e-4 and (y1 - y0) > 2.2 * b_top:
            ym = y1 - b_top
            loop_b = oct_loop(x0, x1, y0, z0, z1, c)
            loop_m = oct_loop(x0, x1, ym, z0, z1, c)
            loop_t = oct_loop(x0 + b_top, x1 - b_top, y1, z0 + b_top, z1 - b_top, max(0.02, c - 0.5 * b_top))
            self.add_closed_loft(comp_name, mat_name, loop_b, loop_m, cap_bot=cap_bot, cap_top=False)
            self.add_closed_loft(comp_name, mat_name, loop_m, loop_t, cap_bot=False, cap_top=cap_top)
        else:
            loop_b = oct_loop(x0, x1, y0, z0, z1, c)
            loop_t = oct_loop(x0, x1, y1, z0, z1, c)
            self.add_closed_loft(comp_name, mat_name, loop_b, loop_t, cap_bot=cap_bot, cap_top=cap_top)

    def add_cylinder_y(self, comp_name, mat_name, cx, cz, y0, y1, r_bot, r_top, segs=8, cap_bot=True, cap_top=True):
        lb, lt = [], []
        for i in range(segs):
            ang = 2.0 * math.pi * i / segs
            ca, sa = math.cos(ang), math.sin(ang)
            lb.append((cx + r_bot * ca, y0, cz + r_bot * sa))
            lt.append((cx + r_top * ca, y1, cz + r_top * sa))
        self.add_closed_loft(comp_name, mat_name, lb, lt, cap_bot=cap_bot, cap_top=cap_top)

    def export_obj_and_mtl(self, obj_path, mtl_path):
        mtl_filename = os.path.basename(mtl_path)
        used_mats = [m for m in PALETTE_ORDER if m in set(self.comp_mat.values())]

        local_atlas_path = os.path.join(os.path.dirname(mtl_path), ATLAS_FILENAME)
        with open(local_atlas_path, "wb") as af:
            af.write(ATLAS_PNG_BYTES)

        with open(mtl_path, "w", encoding="utf-8") as mf:
            mf.write("# Sphere Brawl: Rolling Rampage — Material Library\n")
            mf.write(f"# Asset: {self.name} (Sphere Brawl Arena Shop Bar — 20.0 x 8.0 x 7.6 Studs)\n")
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
            of.write("# Sphere Brawl: Rolling Rampage — Kinetic Hub Arena Shop Bar 3D Asset\n")
            of.write(f"# Asset Name: {self.name} (Phase 2 Approved Production — 20.0 x 8.0 x 7.6 Studs)\n")
            of.write("# Unit Scale: 1.0 Unit = 1.0 Roblox Stud | Up Axis: +Y | Forward Axis: +Z\n")
            of.write("# Local Origin (0,0,0): Floor-Reference Center of Footprint (Maps to World (43, 150, -300) facing -X)\n")
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
            "name": "SphereBrawl_ShopKiosk_PaletteAtlas",
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
            "name": "SphereBrawl_ShopKiosk_PaletteAtlas_Tex",
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
                "generator": "Sphere Brawl Arena Shop Bar Production Pipeline (20.0 x 8.0 x 7.6 Studs)",
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
# PROCEDURAL PRODUCTION GEOMETRY FOR SM_Hub_ShopKiosk_01 (20.0 x 8.0 x 7.6 STUDS)
# ==============================================================================
def build_hub_shop_kiosk():
    """
    Builds the approved 20.0 (W) x 8.0 (D) x 7.6 (H) stud Sphere Brawl Arena Shop Bar
    across 15 cleanly separated, non-overlapping named components:
      1.  GEO_ShopKiosk_Base            (MAT_DarkNeutral) — Two-stage stepped counter plinth & wing floor pads
      2.  GEO_ShopKiosk_CounterBody     (MAT_DarkNeutral) — Continuous 15.1-stud faceted bar counter hull & rear service lip
      3.  GEO_ShopKiosk_Countertop      (MAT_AltNeutral)  — Broad continuous countertop deck, 4 front fascia armor plates & approach deck inlays
      4.  GEO_ShopKiosk_SideWings       (MAT_DarkNeutral) — Left & right extended side wing hulls & open shelf support posts
      5.  GEO_ShopKiosk_WingShelves     (MAT_AltNeutral)  — Extended side wing presentation shelf decks & upper floating wing vanes
      6.  GEO_ShopKiosk_DisplayPad_01   (MAT_DarkNeutral) — Slot 01 octagonal turntable pad base (X = -5.10, Z = +0.25)
      7.  GEO_ShopKiosk_DisplayPad_02   (MAT_DarkNeutral) — Slot 02 octagonal turntable pad base (X = -1.70, Z = +0.25)
      8.  GEO_ShopKiosk_DisplayPad_03   (MAT_DarkNeutral) — Slot 03 octagonal turntable pad base (X = +1.70, Z = +0.25)
      9.  GEO_ShopKiosk_DisplayPad_04   (MAT_DarkNeutral) — Slot 04 octagonal turntable pad base (X = +5.10, Z = +0.25)
      10. GEO_ShopKiosk_DisplayItem_01  (MAT_AltNeutral)  — Replaceable Non-Spherical Item 01: Faceted Hexagonal Emblem / Shield Plate
      11. GEO_ShopKiosk_DisplayItem_02  (MAT_AltNeutral)  — Replaceable Non-Spherical Item 02: Vertical Toroidal Halo / Energy-Ring Ornament
      12. GEO_ShopKiosk_DisplayItem_03  (MAT_AltNeutral)  — Replaceable Non-Spherical Item 03: Segmented Triple-Chevron Trail-Effect Fins
      13. GEO_ShopKiosk_DisplayItem_04  (MAT_AltNeutral)  — Replaceable Non-Spherical Item 04: Geometric Starburst Burst-Effect Prism
      14. GEO_ShopKiosk_SignFrame       (MAT_DarkNeutral) — Lightweight raked rear sign support struts & segmented overhead visor beam
      15. GEO_ShopKiosk_SignPanel       (MAT_AltNeutral)  — Separate blank UI-ready suspended SHOP sign panel (11.20 x 1.44 studs)
      16. GEO_ShopKiosk_Trim            (MAT_LightTrim)   — Counter front bullnose rail, fascia ribs, corner guards, display sockets/brackets/plaques, sign bezel
      17. GEO_ShopKiosk_CyanAccents     (EMI_Cyan)        — Recessed counter fascia energy channels, 4 octagonal pad rings, approach guide, sign top rail
      18. GEO_ShopKiosk_AmberAccents    (EMI_Amber)       — Restrained shop-specific highlights: sign lower rail, visor crown bar, pad ticks, wing-tip beacons
    """
    mb = ShopKioskMeshBuilder("SM_Hub_ShopKiosk_01")

    for cname, mname in [
        ("GEO_ShopKiosk_Base", "MAT_DarkNeutral"),
        ("GEO_ShopKiosk_CounterBody", "MAT_DarkNeutral"),
        ("GEO_ShopKiosk_Countertop", "MAT_AltNeutral"),
        ("GEO_ShopKiosk_SideWings", "MAT_DarkNeutral"),
        ("GEO_ShopKiosk_WingShelves", "MAT_AltNeutral"),
        ("GEO_ShopKiosk_DisplayPad_01", "MAT_DarkNeutral"),
        ("GEO_ShopKiosk_DisplayPad_02", "MAT_DarkNeutral"),
        ("GEO_ShopKiosk_DisplayPad_03", "MAT_DarkNeutral"),
        ("GEO_ShopKiosk_DisplayPad_04", "MAT_DarkNeutral"),
        ("GEO_ShopKiosk_DisplayItem_01", "MAT_AltNeutral"),
        ("GEO_ShopKiosk_DisplayItem_02", "MAT_AltNeutral"),
        ("GEO_ShopKiosk_DisplayItem_03", "MAT_AltNeutral"),
        ("GEO_ShopKiosk_DisplayItem_04", "MAT_AltNeutral"),
        ("GEO_ShopKiosk_SignFrame", "MAT_DarkNeutral"),
        ("GEO_ShopKiosk_SignPanel", "MAT_AltNeutral"),
        ("GEO_ShopKiosk_Trim", "MAT_LightTrim"),
        ("GEO_ShopKiosk_CyanAccents", "EMI_Cyan"),
        ("GEO_ShopKiosk_AmberAccents", "EMI_Amber"),
    ]:
        mb.ensure_component(cname, mname)

    # ==========================================================================
    # 1. GEO_ShopKiosk_Base (MAT_DarkNeutral) — Two-Stage Stepped Counter Plinth
    # ==========================================================================
    # Central main foundation pad (X in [-7.60, +7.60], Z in [-3.80, +4.00], Y in [0.00, 0.24])
    # Complete underside cap at Y = 0.0000 (outward normal (0, -1, 0))
    p_bot = [
        (-7.20, 0.00, +4.00), (+7.20, 0.00, +4.00),
        (+7.60, 0.00, +3.45), (+7.60, 0.00, -3.35),
        (+7.10, 0.00, -3.80), (-7.10, 0.00, -3.80),
        (-7.60, 0.00, -3.35), (-7.60, 0.00, +3.45),
    ]
    p_top = [
        (-7.08, 0.24, +3.90), (+7.08, 0.24, +3.90),
        (+7.48, 0.24, +3.38), (+7.48, 0.24, -3.25),
        (+6.98, 0.24, -3.70), (-6.98, 0.24, -3.70),
        (-7.48, 0.24, -3.25), (-7.48, 0.24, +3.38),
    ]
    mb.add_closed_loft("GEO_ShopKiosk_Base", "MAT_DarkNeutral", p_bot, p_top, cap_bot=True, cap_top=True)

    # Upper stepped counter plinth riser (X in [-7.25, +7.25], Z in [-2.40, +2.65], Y in [0.24, 0.48])
    p2_bot = [
        (-6.90, 0.24, +2.65), (+6.90, 0.24, +2.65),
        (+7.25, 0.24, +2.15), (+7.25, 0.24, -2.05),
        (+6.85, 0.24, -2.40), (-6.85, 0.24, -2.40),
        (-7.25, 0.24, -2.05), (-7.25, 0.24, +2.15),
    ]
    p2_top = [
        (-6.80, 0.48, +2.55), (+6.80, 0.48, +2.55),
        (+7.15, 0.48, +2.05), (+7.15, 0.48, -1.95),
        (+6.75, 0.48, -2.30), (-6.75, 0.48, -2.30),
        (-7.15, 0.48, -1.95), (-7.15, 0.48, +2.05),
    ]
    mb.add_closed_loft("GEO_ShopKiosk_Base", "MAT_DarkNeutral", p2_bot, p2_top, cap_bot=False, cap_top=True)

    # Left & Right Extended Wing Base Plinth Pads (reaching exact X = +/-10.0000 and Z = -4.0000, Y in [0.00, 0.28])
    for sx in (-1.0, +1.0):
        wb_b = [
            (sx * 7.20, 0.00, +2.60),
            (sx * 9.45, 0.00, +1.65),
            (sx * 10.00, 0.00, +0.85),
            (sx * 10.00, 0.00, -3.35),
            (sx * 9.35, 0.00, -4.00),
            (sx * 7.10, 0.00, -3.80),
        ]
        wb_t = [
            (sx * 7.15, 0.28, +2.48),
            (sx * 9.32, 0.28, +1.55),
            (sx * 9.86, 0.28, +0.78),
            (sx * 9.86, 0.28, -3.25),
            (sx * 9.22, 0.28, -3.88),
            (sx * 7.05, 0.28, -3.68),
        ]
        if sx < 0:
            wb_b = list(reversed(wb_b))
            wb_t = list(reversed(wb_t))
        mb.add_closed_loft("GEO_ShopKiosk_Base", "MAT_DarkNeutral", wb_b, wb_t, cap_bot=True, cap_top=True)

    # ==========================================================================
    # 2. GEO_ShopKiosk_CounterBody (MAT_DarkNeutral) — Continuous Faceted Bar Counter Hull
    # ==========================================================================
    c_y0 = [
        (-6.80, 0.48, +2.05), (+6.80, 0.48, +2.05),
        (+7.10, 0.48, +1.45), (+7.10, 0.48, -1.75),
        (+6.65, 0.48, -2.10), (-6.65, 0.48, -2.10),
        (-7.10, 0.48, -1.75), (-7.10, 0.48, +1.45),
    ]
    c_y1 = [
        (-6.92, 1.08, +2.22), (+6.92, 1.08, +2.22),
        (+7.25, 1.08, +1.60), (+7.25, 1.08, -1.75),
        (+6.75, 1.08, -2.10), (-6.75, 1.08, -2.10),
        (-7.25, 1.08, -1.75), (-7.25, 1.08, +1.60),
    ]
    c_y2 = [
        (-7.05, 2.08, +2.56), (+7.05, 2.08, +2.56),
        (+7.40, 2.08, +1.85), (+7.40, 2.08, -1.70),
        (+6.85, 2.08, -2.08), (-6.85, 2.08, -2.08),
        (-7.40, 2.08, -1.70), (-7.40, 2.08, +1.85),
    ]
    c_y3 = [
        (-6.95, 2.66, +2.38), (+6.95, 2.66, +2.38),
        (+7.32, 2.66, +1.72), (+7.32, 2.66, -1.68),
        (+6.80, 2.66, -2.04), (-6.80, 2.66, -2.04),
        (-7.32, 2.66, -1.68), (-7.32, 2.66, +1.72),
    ]
    mb.add_closed_loft("GEO_ShopKiosk_CounterBody", "MAT_DarkNeutral", c_y0, c_y1, cap_bot=False, cap_top=False)
    mb.add_closed_loft("GEO_ShopKiosk_CounterBody", "MAT_DarkNeutral", c_y1, c_y2, cap_bot=False, cap_top=False)
    mb.add_closed_loft("GEO_ShopKiosk_CounterBody", "MAT_DarkNeutral", c_y2, c_y3, cap_bot=False, cap_top=False)

    # Low rear counter service lip / rail (Y = 2.92 .. 3.32 along back edge of counter; completely open above Y = 3.32)
    mb.add_beveled_box(
        "GEO_ShopKiosk_CounterBody", "MAT_DarkNeutral",
        x0=-6.80, x1=+6.80, y0=2.92, y1=3.32, z0=-2.14, z1=-1.68,
        b_xz=0.12, b_top=0.05, cap_bot=False, cap_top=True
    )

    # ==========================================================================
    # 3. GEO_ShopKiosk_Countertop (MAT_AltNeutral) — Broad Countertop Deck & Fascia Plates
    # ==========================================================================
    # Broad, continuous low countertop display deck (Y = 2.66 .. 2.92, X in [-7.55, +7.55], Z in [-2.22, +2.72])
    top_b = [
        (-7.18, 2.66, +2.72), (+7.18, 2.66, +2.72),
        (+7.55, 2.66, +2.02), (+7.55, 2.66, -1.82),
        (+7.02, 2.66, -2.22), (-7.02, 2.66, -2.22),
        (-7.55, 2.66, -1.82), (-7.55, 2.66, +2.02),
    ]
    top_t = [
        (-7.12, 2.92, +2.66), (+7.12, 2.92, +2.66),
        (+7.48, 2.92, +1.96), (+7.48, 2.92, -1.76),
        (+6.96, 2.92, -2.16), (-6.96, 2.92, -2.16),
        (-7.48, 2.92, -1.76), (-7.48, 2.92, +1.96),
    ]
    mb.add_closed_loft("GEO_ShopKiosk_Countertop", "MAT_AltNeutral", top_b, top_t, cap_bot=True, cap_top=True)

    # Four faceted front fascia armor plates along the customer-facing bar front (aligned with the 4 display slots)
    for spec in DISPLAY_SLOT_SPECS:
        cx = spec["cx"]
        fb_b = [
            (cx - 1.32, 1.15, +2.28), (cx + 1.32, 1.15, +2.28),
            (cx + 1.42, 1.15, +2.12), (cx - 1.42, 1.15, +2.12),
        ]
        fb_t = [
            (cx - 1.32, 2.02, +2.64), (cx + 1.32, 2.02, +2.64),
            (cx + 1.42, 2.02, +2.44), (cx - 1.42, 2.02, +2.44),
        ]
        mb.add_closed_loft("GEO_ShopKiosk_Countertop", "MAT_AltNeutral", fb_b, fb_t, cap_bot=True, cap_top=True)

    # Four rear counter service inspection plates (gives finished industrial detail on the rear of the bar counter)
    for spec in DISPLAY_SLOT_SPECS:
        cx = spec["cx"]
        mb.add_beveled_box(
            "GEO_ShopKiosk_Countertop", "MAT_AltNeutral",
            x0=cx - 1.25, x1=cx + 1.25, y0=0.85, y1=2.35, z0=-2.18, z1=-2.06,
            b_xz=0.06, b_top=0.0, cap_bot=True, cap_top=True
        )

    # Three customer approach floor inlay plates along the front walk-up apron (Z in [+2.68, +3.74], Y = 0.24..0.30)
    for cx in (-4.80, 0.00, +4.80):
        mb.add_beveled_box(
            "GEO_ShopKiosk_Countertop", "MAT_AltNeutral",
            x0=cx - 1.95, x1=cx + 1.95, y0=0.24, y1=0.30, z0=+2.68, z1=+3.74,
            b_xz=0.12, b_top=0.02, cap_bot=False, cap_top=True
        )

    # ==========================================================================
    # 4. GEO_ShopKiosk_SideWings (MAT_DarkNeutral) & 5. GEO_ShopKiosk_WingShelves (MAT_AltNeutral)
    # ==========================================================================
    for sx in (-1.0, +1.0):
        # Lower wing counter extension body (Y = 0.28 .. 2.38)
        w_b = [
            (sx * 7.15, 0.28, +1.95),
            (sx * 9.35, 0.28, +1.15),
            (sx * 9.80, 0.28, +0.45),
            (sx * 9.80, 0.28, -2.95),
            (sx * 9.15, 0.28, -3.55),
            (sx * 7.05, 0.28, -3.25),
        ]
        w_t = [
            (sx * 7.25, 2.38, +1.85),
            (sx * 9.48, 2.38, +1.05),
            (sx * 9.92, 2.38, +0.38),
            (sx * 9.92, 2.38, -2.85),
            (sx * 9.25, 2.38, -3.45),
            (sx * 7.15, 2.38, -3.15),
        ]
        if sx < 0:
            w_b = list(reversed(w_b))
            w_t = list(reversed(wb_t_tmp := w_t))
        mb.add_closed_loft("GEO_ShopKiosk_SideWings", "MAT_DarkNeutral", w_b, w_t, cap_bot=False, cap_top=False)

        # Open presentation wing shelf deck (Y = 2.38 .. 2.60)
        ws_b = [
            (sx * 7.20, 2.38, +2.02),
            (sx * 9.55, 2.38, +1.18),
            (sx * 10.00, 2.38, +0.45),
            (sx * 10.00, 2.38, -2.95),
            (sx * 9.30, 2.38, -3.58),
            (sx * 7.15, 2.38, -3.25),
        ]
        ws_t = [
            (sx * 7.20, 2.60, +1.98),
            (sx * 9.52, 2.60, +1.14),
            (sx * 9.96, 2.60, +0.42),
            (sx * 9.96, 2.60, -2.90),
            (sx * 9.26, 2.60, -3.52),
            (sx * 7.15, 2.60, -3.20),
        ]
        if sx < 0:
            ws_b = list(reversed(ws_b))
            ws_t = list(reversed(ws_t))
        mb.add_closed_loft("GEO_ShopKiosk_WingShelves", "MAT_AltNeutral", ws_b, ws_t, cap_bot=True, cap_top=True)

        # Open support post rising from wing shelf to upper floating wing vane (Y = 2.60 .. 3.85)
        x_post1 = min(sx * 8.15, sx * 8.55)
        x_post2 = max(sx * 8.15, sx * 8.55)
        mb.add_beveled_box(
            "GEO_ShopKiosk_SideWings", "MAT_DarkNeutral",
            x0=x_post1, x1=x_post2, y0=2.60, y1=3.85, z0=-2.35, z1=-1.75,
            b_xz=0.06, b_top=0.0, cap_bot=False, cap_top=False
        )

        # Floating upper wing shelf / accent vane (Y = 3.85 .. 4.25)
        wf_b = [
            (sx * 7.45, 3.85, +0.45),
            (sx * 9.45, 3.85, -0.15),
            (sx * 9.85, 3.85, -0.75),
            (sx * 9.85, 3.85, -3.05),
            (sx * 9.20, 3.85, -3.55),
            (sx * 7.45, 3.85, -3.15),
        ]
        wf_t = [
            (sx * 7.45, 4.25, +0.40),
            (sx * 9.40, 4.25, -0.18),
            (sx * 9.80, 4.25, -0.78),
            (sx * 9.80, 4.25, -3.00),
            (sx * 9.15, 4.25, -3.50),
            (sx * 7.45, 4.25, -3.10),
        ]
        if sx < 0:
            wf_b = list(reversed(wf_b))
            wf_t = list(reversed(wf_t))
        mb.add_closed_loft("GEO_ShopKiosk_WingShelves", "MAT_AltNeutral", wf_b, wf_t, cap_bot=True, cap_top=True)

    # ==========================================================================
    # 6..9. GEO_ShopKiosk_DisplayPad_01..04 (MAT_DarkNeutral) — 4 Compact Display Pads
    # ==========================================================================
    for spec in DISPLAY_SLOT_SPECS:
        cx = spec["cx"]
        cz = spec["cz"]
        pad_name = spec["pad_name"]
        # Low, compact integrated octagonal turntable pad on the countertop (Y = 2.92 .. 3.10)
        mb.add_cylinder_y(
            pad_name, "MAT_DarkNeutral",
            cx=cx, cz=cz, y0=2.92, y1=3.10, r_bot=1.08, r_top=0.98, segs=8, cap_bot=False, cap_top=True
        )

    # ==========================================================================
    # 10..13. GEO_ShopKiosk_DisplayItem_01..04 (MAT_AltNeutral) — 4 Replaceable Non-Spherical Items
    # ==========================================================================
    # --- ITEM 01 (X = -5.10, Z = +0.25): FACETED HEXAGONAL EMBLEM / SHIELD PLATE ---
    cx1, cy1, cz1 = -5.10, 4.18, +0.25
    for sx in (-0.28, +0.28):
        mb.add_simple_box(
            "GEO_ShopKiosk_DisplayItem_01", "MAT_AltNeutral",
            x0=cx1 + sx - 0.07, x1=cx1 + sx + 0.07, y0=3.30, y1=3.65, z0=cz1 - 0.08, z1=cz1 + 0.08,
            cap_bot=False, cap_top=False
        )
    hex_r_x, hex_r_y = 0.88, 0.78
    hex_f, hex_b = [], []
    for k in range(6):
        ang = math.radians(30 + 60 * k)
        hx = cx1 + hex_r_x * math.cos(ang)
        hy = cy1 + hex_r_y * math.sin(ang)
        hex_f.append((hx, hy, cz1 + 0.16))
        hex_b.append((hx, hy, cz1 - 0.16))
    mb.add_closed_loft_axis("GEO_ShopKiosk_DisplayItem_01", "MAT_AltNeutral", hex_f, hex_b, cap_front=True, cap_back=True)
    mb.add_beveled_box(
        "GEO_ShopKiosk_DisplayItem_01", "MAT_AltNeutral",
        x0=cx1 - 0.22, x1=cx1 + 0.22, y0=cy1 - 0.52, y1=cy1 + 0.52, z0=cz1 + 0.16, z1=cz1 + 0.30,
        b_xz=0.05, b_top=0.03, cap_bot=True, cap_top=True
    )

    # --- ITEM 02 (X = -1.70, Z = +0.25): VERTICAL TOROIDAL HALO / ENERGY-RING ORNAMENT ---
    cx2, cy2, cz2 = -1.70, 4.22, +0.25
    mb.add_simple_box(
        "GEO_ShopKiosk_DisplayItem_02", "MAT_AltNeutral",
        x0=cx2 - 0.10, x1=cx2 + 0.10, y0=3.30, y1=3.55, z0=cz2 - 0.10, z1=cz2 + 0.10,
        cap_bot=False, cap_top=False
    )
    r_out, r_in = 0.86, 0.50
    segs_r = 8
    z0_r, z1_r = cz2 - 0.15, cz2 + 0.15
    for i in range(segs_r):
        j = (i + 1) % segs_r
        a0 = 2.0 * math.pi * i / segs_r
        a1 = 2.0 * math.pi * j / segs_r
        am = 0.5 * (a0 + a1)
        c0, s0 = math.cos(a0), math.sin(a0)
        c1, s1 = math.cos(a1), math.sin(a1)
        cm, sm = math.cos(am), math.sin(am)

        if0 = (cx2 + r_in * c0, cy2 + r_in * s0, z1_r)
        if1 = (cx2 + r_in * c1, cy2 + r_in * s1, z1_r)
        ib0 = (cx2 + r_in * c0, cy2 + r_in * s0, z0_r)
        ib1 = (cx2 + r_in * c1, cy2 + r_in * s1, z0_r)

        of0 = (cx2 + r_out * c0, cy2 + r_out * s0, z1_r)
        of1 = (cx2 + r_out * c1, cy2 + r_out * s1, z1_r)
        ob0 = (cx2 + r_out * c0, cy2 + r_out * s0, z0_r)
        ob1 = (cx2 + r_out * c1, cy2 + r_out * s1, z0_r)

        mb.add_quad("GEO_ShopKiosk_DisplayItem_02", "MAT_AltNeutral", if0, of0, of1, if1, expected_normal=(0.0, 0.0, 1.0))
        mb.add_quad("GEO_ShopKiosk_DisplayItem_02", "MAT_AltNeutral", ib1, ob1, ob0, ib0, expected_normal=(0.0, 0.0, -1.0))
        mb.add_quad("GEO_ShopKiosk_DisplayItem_02", "MAT_AltNeutral", ob0, ob1, of1, of0, expected_normal=(cm, sm, 0.0))
        mb.add_quad("GEO_ShopKiosk_DisplayItem_02", "MAT_AltNeutral", ib1, ib0, if0, if1, expected_normal=(-cm, -sm, 0.0))

    for sx in (-1.0, +1.0):
        x0_w = min(cx2 + sx * 0.86, cx2 + sx * 1.06)
        x1_w = max(cx2 + sx * 0.86, cx2 + sx * 1.06)
        mb.add_simple_box(
            "GEO_ShopKiosk_DisplayItem_02", "MAT_AltNeutral",
            x0=x0_w, x1=x1_w, y0=cy2 - 0.14, y1=cy2 + 0.14, z0=cz2 - 0.20, z1=cz2 + 0.20,
            cap_bot=True, cap_top=True
        )

    # --- ITEM 03 (X = +1.70, Z = +0.25): SEGMENTED TRIPLE-CHEVRON TRAIL-EFFECT FINS ---
    cx3, cz3 = +1.70, +0.25
    mb.add_beveled_box(
        "GEO_ShopKiosk_DisplayItem_03", "MAT_AltNeutral",
        x0=cx3 - 0.85, x1=cx3 + 0.85, y0=3.30, y1=3.52, z0=cz3 - 0.16, z1=cz3 + 0.16,
        b_xz=0.05, b_top=0.02, cap_bot=False, cap_top=True
    )
    for f_idx, fx_off in enumerate((-0.52, 0.00, +0.52)):
        bx = cx3 + fx_off
        h_top = 4.65 + 0.18 * f_idx
        fin_f = [
            (bx - 0.16, 3.52, cz3 + 0.14),
            (bx + 0.14, 3.52, cz3 + 0.14),
            (bx + 0.42, h_top, cz3 + 0.09),
            (bx + 0.08, h_top + 0.15, cz3 + 0.09),
        ]
        fin_b = [
            (bx - 0.16, 3.52, cz3 - 0.14),
            (bx + 0.14, 3.52, cz3 - 0.14),
            (bx + 0.42, h_top, cz3 - 0.09),
            (bx + 0.08, h_top + 0.15, cz3 - 0.09),
        ]
        mb.add_closed_loft_axis("GEO_ShopKiosk_DisplayItem_03", "MAT_AltNeutral", fin_f, fin_b, cap_front=True, cap_back=True)

    # --- ITEM 04 (X = +5.10, Z = +0.25): GEOMETRIC STARBURST BURST-EFFECT PRISM ---
    cx4, cy4, cz4 = +5.10, 4.25, +0.25
    mb.add_simple_box(
        "GEO_ShopKiosk_DisplayItem_04", "MAT_AltNeutral",
        x0=cx4 - 0.12, x1=cx4 + 0.12, y0=3.30, y1=3.62, z0=cz4 - 0.12, z1=cz4 + 0.12,
        cap_bot=False, cap_top=False
    )
    for ang_deg in (0.0, 60.0, -60.0):
        ar = math.radians(ang_deg)
        ca, sa = math.cos(ar), math.sin(ar)
        L_maj = 0.80 if ang_deg == 0.0 else 0.88
        L_min = 0.26 if ang_deg == 0.0 else 0.24
        zf = cz4 + (0.16 if ang_deg == 0.0 else (0.11 if ang_deg > 0 else 0.07))
        zb = cz4 - (0.16 if ang_deg == 0.0 else (0.11 if ang_deg > 0 else 0.07))
        raw_pts = [(0.0, +L_maj), (-L_min, 0.0), (0.0, -L_maj), (+L_min, 0.0)]
        bf, bb = [], []
        for (ux, uy) in raw_pts:
            rx = ux * ca - uy * sa
            ry = ux * sa + uy * ca
            bf.append((cx4 + rx, cy4 + ry, zf))
            bb.append((cx4 + rx, cy4 + ry, zb))
        mb.add_closed_loft_axis("GEO_ShopKiosk_DisplayItem_04", "MAT_AltNeutral", bf, bb, cap_front=True, cap_back=True)

    # ==========================================================================
    # 14. GEO_ShopKiosk_SignFrame (MAT_DarkNeutral) — Lightweight Support Struts & Visor
    # ==========================================================================
    for sx in (-1.0, +1.0):
        px = sx * 6.45
        st_b = [
            (px - 0.24, 3.20, -1.30), (px + 0.24, 3.20, -1.30),
            (px + 0.24, 3.20, -1.95), (px - 0.24, 3.20, -1.95),
        ]
        st_m = [
            (px - 0.22, 5.65, -0.75), (px + 0.22, 5.65, -0.75),
            (px + 0.22, 5.65, -1.35), (px - 0.22, 5.65, -1.35),
        ]
        st_t = [
            (px - 0.20, 7.28, +0.55), (px + 0.20, 7.28, +0.55),
            (px + 0.20, 7.28, -0.35), (px - 0.20, 7.28, -0.35),
        ]
        mb.add_closed_loft("GEO_ShopKiosk_SignFrame", "MAT_DarkNeutral", st_b, st_m, cap_bot=False, cap_top=False)
        mb.add_closed_loft("GEO_ShopKiosk_SignFrame", "MAT_DarkNeutral", st_m, st_t, cap_bot=False, cap_top=False)

        # Horizontal tie-brackets connecting rear struts cleanly into the sign panel end-brackets
        x_tie0 = min(sx * 5.86, sx * 6.23)
        x_tie1 = max(sx * 5.86, sx * 6.23)
        mb.add_simple_box(
            "GEO_ShopKiosk_SignFrame", "MAT_DarkNeutral",
            x0=x_tie0, x1=x_tie1, y0=6.20, y1=6.60, z0=-0.25, z1=+0.35,
            cap_bot=True, cap_top=True
        )

    # Lightweight segmented top cross-rail / open visor beam (Y = 7.28 .. 7.60, X in [-6.85, +6.85], Z in [-0.25, +0.85])
    mb.add_beveled_box(
        "GEO_ShopKiosk_SignFrame", "MAT_DarkNeutral",
        x0=-6.85, x1=+6.85, y0=7.28, y1=7.60, z0=-0.25, z1=+0.85,
        b_xz=0.14, b_top=0.05, cap_bot=True, cap_top=True
    )

    # ==========================================================================
    # 15. GEO_ShopKiosk_SignPanel (MAT_AltNeutral) — Separate Blank UI-Ready Sign Panel
    # ==========================================================================
    # Broad, horizontal suspended SHOP sign panel (X in [-5.60, +5.60], Y in [5.68, 7.12], Z in [+0.20, +0.68])
    # Blank front sign face at Z = +0.68 ready for native Roblox SurfaceGui / UI without baked-in geometry text.
    mb.add_beveled_box(
        "GEO_ShopKiosk_SignPanel", "MAT_AltNeutral",
        x0=-5.60, x1=+5.60, y0=5.68, y1=7.12, z0=+0.20, z1=+0.68,
        b_xz=0.12, b_top=0.0, cap_bot=False, cap_top=False
    )

    # ==========================================================================
    # 16. GEO_ShopKiosk_Trim (MAT_LightTrim) — Structural Brackets, Bullnose Rail & Bezels
    # ==========================================================================
    # 1) Three structural vertical counter ribs between the 4 fascia bays
    for rx in (-3.40, 0.00, +3.40):
        rb_b = [
            (rx - 0.16, 0.48, +2.12), (rx + 0.16, 0.48, +2.12),
            (rx + 0.16, 0.48, +1.85), (rx - 0.16, 0.48, +1.85),
        ]
        rb_t = [
            (rx - 0.16, 2.66, +2.58), (rx + 0.16, 2.66, +2.58),
            (rx + 0.16, 2.66, +2.25), (rx - 0.16, 2.66, +2.25),
        ]
        mb.add_closed_loft("GEO_ShopKiosk_Trim", "MAT_LightTrim", rb_b, rb_t, cap_bot=False, cap_top=False)

    # 2) Continuous customer-facing countertop front bullnose rail
    mb.add_beveled_box(
        "GEO_ShopKiosk_Trim", "MAT_LightTrim",
        x0=-7.12, x1=+7.12, y0=2.70, y1=2.90, z0=+2.68, z1=+2.84,
        b_xz=0.05, b_top=0.02, cap_bot=True, cap_top=True
    )

    # 3) Lower counter plinth front bumper guard bar
    mb.add_beveled_box(
        "GEO_ShopKiosk_Trim", "MAT_LightTrim",
        x0=-6.60, x1=+6.60, y0=0.48, y1=0.66, z0=+2.40, z1=+2.58,
        b_xz=0.05, b_top=0.02, cap_bot=False, cap_top=True
    )

    # 4) Corner structural guards on the bar counter ends & base tie-down cleats (COMP_Hub_CornerBracket_01 family)
    for sx in (-1.0, +1.0):
        mb.add_beveled_box(
            "GEO_ShopKiosk_Trim", "MAT_LightTrim",
            x0=sx * 7.25 - 0.22, x1=sx * 7.25 + 0.22,
            y0=0.48, y1=2.66, z0=+1.55, z1=+2.15,
            b_xz=0.06, b_top=0.0, cap_bot=False, cap_top=False
        )
        # Base corner tie-down cleats on front plinth corners
        mb.add_beveled_box(
            "GEO_ShopKiosk_Trim", "MAT_LightTrim",
            x0=sx * 7.15 - 0.32, x1=sx * 7.15 + 0.32,
            y0=0.04, y1=0.38, z0=+3.42, z1=+3.96,
            b_xz=0.06, b_top=0.03, cap_bot=True, cap_top=True
        )
        # Wing outer edge bumper trim (X near +/-10.00)
        x_trim0 = min(sx * 9.72, sx * 9.98)
        x_trim1 = max(sx * 9.72, sx * 9.98)
        mb.add_beveled_box(
            "GEO_ShopKiosk_Trim", "MAT_LightTrim",
            x0=x_trim0, x1=x_trim1, y0=2.34, y1=2.64, z0=-2.85, z1=+0.40,
            b_xz=0.04, b_top=0.02, cap_bot=True, cap_top=True
        )
        # Collar bracket at base of each raked sign support strut
        px = sx * 6.45
        mb.add_beveled_box(
            "GEO_ShopKiosk_Trim", "MAT_LightTrim",
            x0=px - 0.32, x1=px + 0.32, y0=2.92, y1=3.20, z0=-2.02, z1=-1.22,
            b_xz=0.05, b_top=0.02, cap_bot=False, cap_top=True
        )

    # 5) Four display mounting sockets, lateral presentation brackets, and front item plaques
    for spec in DISPLAY_SLOT_SPECS:
        cx = spec["cx"]
        cz = spec["cz"]
        # Central mounting socket on pad (Y = 3.16 .. 3.30)
        mb.add_cylinder_y(
            "GEO_ShopKiosk_Trim", "MAT_LightTrim",
            cx=cx, cz=cz, y0=3.16, y1=3.30, r_bot=0.58, r_top=0.48, segs=8, cap_bot=False, cap_top=True
        )
        # Front countertop merchandise item plaque (Y = 2.92 .. 3.06, Z = +2.05 .. +2.42)
        mb.add_beveled_box(
            "GEO_ShopKiosk_Trim", "MAT_LightTrim",
            x0=cx - 0.58, x1=cx + 0.58, y0=2.92, y1=3.06, z0=+2.05, z1=+2.42,
            b_xz=0.04, b_top=0.02, cap_bot=False, cap_top=True
        )
        # Short open lateral presentation brackets flanking each display pad
        for s_arm in (-1.0, +1.0):
            ax = cx + s_arm * 1.18
            mb.add_beveled_box(
                "GEO_ShopKiosk_Trim", "MAT_LightTrim",
                x0=ax - 0.08, x1=ax + 0.08, y0=2.92, y1=3.65, z0=cz - 0.14, z1=cz + 0.14,
                b_xz=0.02, b_top=0.02, cap_bot=False, cap_top=True
            )

    # 6) Suspended Sign Panel top & bottom metallic bezel bars & side end-caps
    mb.add_beveled_box(
        "GEO_ShopKiosk_Trim", "MAT_LightTrim",
        x0=-5.78, x1=+5.78, y0=7.12, y1=7.26, z0=+0.15, z1=+0.76,
        b_xz=0.06, b_top=0.02, cap_bot=True, cap_top=True
    )
    mb.add_beveled_box(
        "GEO_ShopKiosk_Trim", "MAT_LightTrim",
        x0=-5.78, x1=+5.78, y0=5.54, y1=5.68, z0=+0.15, z1=+0.76,
        b_xz=0.06, b_top=0.02, cap_bot=True, cap_top=True
    )
    for sx in (-1.0, +1.0):
        x_sb0 = min(sx * 5.60, sx * 5.86)
        x_sb1 = max(sx * 5.60, sx * 5.86)
        mb.add_beveled_box(
            "GEO_ShopKiosk_Trim", "MAT_LightTrim",
            x0=x_sb0, x1=x_sb1, y0=5.68, y1=7.12, z0=+0.16, z1=+0.74,
            b_xz=0.04, b_top=0.0, cap_bot=False, cap_top=False
        )

    # ==========================================================================
    # 17. GEO_ShopKiosk_CyanAccents (EMI_Cyan) — Recessed Energy Channels & Pad Rings
    # ==========================================================================
    # 1) Upper & lower continuous recessed cyan energy channels along the bar counter front fascia
    mb.add_simple_box(
        "GEO_ShopKiosk_CyanAccents", "EMI_Cyan",
        x0=-6.75, x1=+6.75, y0=2.48, y1=2.60, z0=+2.44, z1=+2.56,
        cap_bot=True, cap_top=True
    )
    mb.add_simple_box(
        "GEO_ShopKiosk_CyanAccents", "EMI_Cyan",
        x0=-6.65, x1=+6.65, y0=0.92, y1=1.04, z0=+2.18, z1=+2.30,
        cap_bot=True, cap_top=True
    )
    # 2) Approach floor cyan guide strip along the front walk-up step
    mb.add_simple_box(
        "GEO_ShopKiosk_CyanAccents", "EMI_Cyan",
        x0=-5.80, x1=+5.80, y0=0.24, y1=0.31, z0=+3.76, z1=+3.88,
        cap_bot=False, cap_top=True
    )
    # 3) Four octagonal display pad emitter rings (Y = 3.10 .. 3.16)
    for spec in DISPLAY_SLOT_SPECS:
        mb.add_cylinder_y(
            "GEO_ShopKiosk_CyanAccents", "EMI_Cyan",
            cx=spec["cx"], cz=spec["cz"], y0=3.10, y1=3.16, r_bot=0.90, r_top=0.84, segs=8, cap_bot=False, cap_top=True
        )
    # 4) Left & Right Extended Wing front cyan bevel strips
    for sx in (-1.0, +1.0):
        x_cy0 = min(sx * 7.45, sx * 9.35)
        x_cy1 = max(sx * 7.45, sx * 9.35)
        mb.add_simple_box(
            "GEO_ShopKiosk_CyanAccents", "EMI_Cyan",
            x0=x_cy0, x1=x_cy1, y0=1.55, y1=1.72, z0=+1.18, z1=+1.36,
            cap_bot=True, cap_top=True
        )
    # 5) Suspended Shop Sign upper cyan illumination rail
    mb.add_simple_box(
        "GEO_ShopKiosk_CyanAccents", "EMI_Cyan",
        x0=-5.35, x1=+5.35, y0=6.96, y1=7.08, z0=+0.68, z1=+0.75,
        cap_bot=True, cap_top=True
    )
    # 6) Rear counter service diagnostic strip
    mb.add_simple_box(
        "GEO_ShopKiosk_CyanAccents", "EMI_Cyan",
        x0=-4.20, x1=+4.20, y0=2.48, y1=2.60, z0=-2.16, z1=-2.05,
        cap_bot=True, cap_top=True
    )

    # ==========================================================================
    # 18. GEO_ShopKiosk_AmberAccents (EMI_Amber) — Restrained Shop-Specific Highlights
    # ==========================================================================
    # 1) Suspended Shop Sign lower amber accent rail
    mb.add_simple_box(
        "GEO_ShopKiosk_AmberAccents", "EMI_Amber",
        x0=-5.35, x1=+5.35, y0=5.72, y1=5.84, z0=+0.68, z1=+0.75,
        cap_bot=True, cap_top=True
    )
    # 2) Top visor center amber crown indicator bar
    mb.add_simple_box(
        "GEO_ShopKiosk_AmberAccents", "EMI_Amber",
        x0=-2.10, x1=+2.10, y0=7.44, y1=7.56, z0=+0.85, z1=+0.92,
        cap_bot=True, cap_top=True
    )
    # 3) Four small item-tier indicator ticks in front of each countertop display pad
    for spec in DISPLAY_SLOT_SPECS:
        cx = spec["cx"]
        mb.add_simple_box(
            "GEO_ShopKiosk_AmberAccents", "EMI_Amber",
            x0=cx - 0.36, x1=cx + 0.36, y0=2.92, y1=2.99, z0=+1.82, z1=+1.96,
            cap_bot=False, cap_top=True
        )
    # 4) Two small wing-tip amber beacons on upper wing rails
    for sx in (-1.0, +1.0):
        x_am0 = min(sx * 9.55, sx * 9.82)
        x_am1 = max(sx * 9.55, sx * 9.82)
        mb.add_simple_box(
            "GEO_ShopKiosk_AmberAccents", "EMI_Amber",
            x0=x_am0, x1=x_am1, y0=3.96, y1=4.14, z0=-2.65, z1=-0.95,
            cap_bot=True, cap_top=True
        )

    return mb


def build_collision_proxy():
    """
    Constructs an optional, isolated simple structural collision proxy (COL_ShopKiosk_Body, 36 triangles)
    protecting the main bar counter and side wings while keeping the front walk-up apron open.
    """
    cb = ShopKioskMeshBuilder("COL_ShopKiosk_Body")
    cb.ensure_component("COL_ShopKiosk_CounterHull", "MAT_DarkNeutral")
    cb.ensure_component("COL_ShopKiosk_WingHull_L", "MAT_DarkNeutral")
    cb.ensure_component("COL_ShopKiosk_WingHull_R", "MAT_DarkNeutral")

    # Central bar counter box (X in [-7.48, +7.48], Y in [0.00, 3.32], Z in [-2.22, +2.66])
    cb.add_simple_box(
        "COL_ShopKiosk_CounterHull", "MAT_DarkNeutral",
        x0=-7.4800, x1=+7.4800, y0=0.0000, y1=3.3200, z0=-2.2200, z1=+2.6600
    )
    # Left & Right wing hulls (X in [-10.00, -7.48] and [+7.48, +10.00], Y in [0.00, 2.60], Z in [-3.58, +1.95])
    cb.add_simple_box(
        "COL_ShopKiosk_WingHull_L", "MAT_DarkNeutral",
        x0=-10.0000, x1=-7.4800, y0=0.0000, y1=2.6000, z0=-3.5800, z1=+1.9500
    )
    cb.add_simple_box(
        "COL_ShopKiosk_WingHull_R", "MAT_DarkNeutral",
        x0=+7.4800, x1=+10.0000, y0=0.0000, y1=2.6000, z0=-3.5800, z1=+1.9500
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

    mb = build_hub_shop_kiosk()
    obj_out = os.path.join(out_dir, "SM_Hub_ShopKiosk_01.obj")
    mtl_out = os.path.join(out_dir, "SM_Hub_ShopKiosk_01.mtl")
    glb_out = os.path.join(out_dir, "SM_Hub_ShopKiosk_01.glb")
    mb.export_obj_and_mtl(obj_out, mtl_out)
    mb.export_glb(glb_out)

    col_dir = os.path.join(out_dir, "collision_proxy")
    os.makedirs(col_dir, exist_ok=True)
    cb = build_collision_proxy()
    cb.export_obj_and_mtl(
        os.path.join(col_dir, "COL_ShopKiosk_Body.obj"),
        os.path.join(col_dir, "COL_ShopKiosk_Body.mtl"),
    )
    cb.export_glb(os.path.join(col_dir, "COL_ShopKiosk_Body.glb"))

    if HAS_BPY:
        blend_out = os.path.join(out_dir, "SM_Hub_ShopKiosk_01.blend")
        build_in_blender(mb, save_blend_path=blend_out)
        print(f"Saved Blender source to {blend_out}")

    total_tris = sum(len(t) for t in mb.comp_tris.values())
    print(f"Successfully generated production SM_Hub_ShopKiosk_01 in {out_dir} ({total_tris} triangles across {len(mb.comp_order)} components).")
