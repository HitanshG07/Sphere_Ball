#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — DETERMINISTIC BLENDER 3.6+ / 4.x & PYTHON PRODUCTION GENERATOR
Asset ID: SM_Hub_ModeBoard_01 (Tactical Arena Mode Selection Command Gantry — Step 5, Phase 2 Production)
=========================================================================================================
- Canonical Asset ID: SM_Hub_ModeBoard_01
- Descriptive Name: Tactical Arena Mode Selection Command Gantry
- Approved Phase 1 Concept Source: Sphere_Brawl_Hub_ModeBoard_Concept_01.zip
  (Verified SHA-256: e76c211dd44fc5c36d71a546ef8e683de05923e8ee142e203173caabeeaddeb6)
- Authoritative World Position: (35.0000, 150.0000, -326.0000) (LOCKED by TASK-03 & Master Plan §2.4)
- Authoritative Floor Reference: World Y = 150.0000 (Local Y = 0.0000)
- Verified Radial Inward Yaw: theta_yaw = -53.39292061° (-0.93188189 rad, atan2(-35, 26))
- Required Roblox Placement Transform:
    local targetCFrame =
        CFrame.new(35, 150, -326)
        * CFrame.Angles(0, math.rad(-53.39292061), 0)
- Equivalent Right-Handed Matrix:
    CFrame.fromMatrix(
        Vector3.new(35, 150, -326),
        Vector3.new( 0.59632400, 0.0,  0.80274385), -- RightVector (Local +X)
        Vector3.new( 0.00000000, 1.0,  0.00000000), -- UpVector    (Local +Y)
        Vector3.new(-0.80274385, 0.0,  0.59632400)  -- ZVector     (Local +Z, Front facing (0, 150, -300))
    )
- Measured Local Bounding Envelope:
  * Width  (Local X): 14.4000 studs (X in [-7.2000, +7.2000])
  * Depth  (Local Z):  3.8000 studs (Z in [-1.9000, +1.9000])
  * Height (Local Y):  8.8000 studs (Y in [ 0.0000, +8.8000])
  * Command Matrix Tilt: 14.0° backward from vertical (front normal = (0.000000, +0.241922, +0.970296))
- Five Separate UI-Ready Replaceable Surface Components (Zero Baked Text):
  1. GEO_ModeBoard_UIPanel_01_FFA       (FREE-FOR-ALL — ACTIVE, left hero bay)
  2. GEO_ModeBoard_UIPanel_02_Duel      (DUEL — COMING SOON, top-right bay)
  3. GEO_ModeBoard_UIPanel_03_TeamClash (TEAM CLASH — COMING SOON, middle-right bay)
  4. GEO_ModeBoard_UIPanel_04_KingTile  (KING TILE — COMING SOON, bottom-right bay)
  5. GEO_ModeBoard_HeaderSign           (ARENA MODE SELECT header marquee)

Usage:
  1. In standard Python 3 (builds deterministic .obj, .mtl, .glb, palette atlas, and optional collision proxy):
     python3 generate_mode_board_blender.py --out_dir ./meshes
  2. In Blender 3.6+ / 4.x (builds scene, saves .blend, and exports .obj/.mtl/.glb):
     blender --background --python generate_mode_board_blender.py -- --out_dir ./meshes
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
    "MAT_DarkNeutral": (32, 38, 54),     # #202636 — Primary structural body
    "MAT_AltNeutral":  (42, 50, 70),     # #2A3246 — Secondary panels, frames, and UI-ready backing plates
    "MAT_LightTrim":   (170, 190, 215),  # #AABED7 — Metallic trim, collar clamps, bezels, lock bars, and relief icons
    "EMI_Cyan":        (0, 195, 255),    # #00C3FF — Active Free-for-All energy frame, reticle ring, and header/floor conduits
    "EMI_Amber":       (255, 170, 0),    # #FFAA00 — Restrained Coming Soon lock indicators
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
        "surface_role": "Dominant structural dark alloy: grounded lower anchor plinth, inclined main command matrix chassis, left/right A-frame buttress piers, overhead canopy hood, and 4 UI-ready mode panel surfaces",
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
        "surface_role": "Secondary slate metallic: upper stepped plinth & walk-up threshold inlays, outer buttress cheek plates, rear diagonal spine struts, active hero surround, recessed locked bay frames, and separate UI-ready header sign panel",
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
        "surface_role": "Light metallic mechanical trim: base bumper rail & floor tie-down cleats, buttress collar clamps, central vertical divider, active bay corner chevrons, physical lockdown clamp bars, padlock reliefs, mode icon reliefs, and header sign bezel",
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
        "surface_role": "Primary active-mode accent: Free-for-All perimeter energy conduit frame, active status header pill, central sphere-clash reticle ring, left buttress conduit, left approach floor guide strip, and top visor illumination bar",
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
        "surface_role": "Restrained Coming Soon indicators: 3 compact lock-status ticks on the right-hand disabled bays, right lower buttress tick, and right floor standby tick",
    },
}

# Tilted command board plane mathematics:
# Bottom hinge of display deck: y_hinge = 1.65, z_hinge = +0.88
# Tilt angle backward from vertical: alpha = 14.0 degrees
TILT_DEG = 14.0
TILT_RAD = math.radians(TILT_DEG)
COS_T = math.cos(TILT_RAD)   # 0.97029573
SIN_T = math.sin(TILT_RAD)   # 0.24192190
Y_HINGE = 1.6500
Z_HINGE = 0.8800

# Placement transform constants
WORLD_POS = (35.0, 150.0, -326.0)
HUB_CENTER = (0.0, 150.0, -300.0)
YAW_RAD = math.atan2(-35.0, 26.0)        # -0.93188189 rad
YAW_DEG = math.degrees(YAW_RAD)          # -53.39292061 deg
COS_YAW = math.cos(YAW_RAD)              # +0.59632400
SIN_YAW = math.sin(YAW_RAD)              # -0.80274385


def board_pt(x_loc, s_along, d_norm):
    """
    Maps board-plane coordinates (x_loc, s_along, d_norm) into local (X, Y, Z):
    - x_loc: horizontal X along board width [-7.20, +7.20]
    - s_along: distance up along the 14.0° inclined board plane from hinge
    - d_norm: perpendicular offset along the outward front normal (0, sin(14°), cos(14°))
    """
    y = Y_HINGE + s_along * COS_T + d_norm * SIN_T
    z = Z_HINGE - s_along * SIN_T + d_norm * COS_T
    return (round(float(x_loc), 5), round(float(y), 5), round(float(z), 5))


def local_to_world_pt(pt_loc):
    lx, ly, lz = pt_loc
    wx = WORLD_POS[0] + lx * COS_YAW + lz * SIN_YAW
    wy = WORLD_POS[1] + ly
    wz = WORLD_POS[2] - lx * SIN_YAW + lz * COS_YAW
    return [round(float(wx), 4), round(float(wy), 4), round(float(wz), 4)]


def local_to_world_vec(vec_loc):
    vx, vy, vz = vec_loc
    wx = vx * COS_YAW + vz * SIN_YAW
    wy = vy
    wz = -vx * SIN_YAW + vz * COS_YAW
    return [round(float(wx), 6), round(float(wy), 6), round(float(wz), 6)]


# Documented UI-Ready Panel Specifications (5 separate replaceable surfaces)
UI_PANEL_SPECS = [
    {
        "component_name": "GEO_ModeBoard_UIPanel_01_FFA",
        "mode_id": "FreeForAll",
        "display_title": "FREE-FOR-ALL",
        "required_state": "ACTIVE",
        "panel_plane_type": "inclined_14deg",
        "tilt_deg_from_vertical": 14.0,
        "local_x_span": [-5.0400, -0.9600],
        "local_s_span": [0.9600, 4.7400],
        "local_d_span": [0.2200, 0.3000],
        "panel_width_studs": 4.0800,
        "panel_height_studs": 3.7800,
        "panel_thickness_studs": 0.0800,
        "front_face_local_center": list(board_pt(-3.0000, 2.8500, 0.3000)),
        "front_face_world_center": local_to_world_pt(board_pt(-3.0000, 2.8500, 0.3000)),
        "front_face_local_normal": [0.000000, round(SIN_T, 6), round(COS_T, 6)],
        "front_face_world_normal": local_to_world_vec((0.0, SIN_T, COS_T)),
        "clear_ui_text_zones_local_s": {
            "top_status_pill_s": [4.18, 4.58],
            "center_reticle_emblem_s": [2.05, 3.85],
            "primary_title_band_s": [1.62, 2.38],
            "bottom_sublabel_band_s": [1.10, 1.54],
        },
    },
    {
        "component_name": "GEO_ModeBoard_UIPanel_02_Duel",
        "mode_id": "Duel",
        "display_title": "DUEL",
        "required_state": "COMING SOON",
        "panel_plane_type": "inclined_14deg",
        "tilt_deg_from_vertical": 14.0,
        "local_x_span": [0.3600, 5.4000],
        "local_s_span": [3.9000, 5.1000],
        "local_d_span": [0.0500, 0.1300],
        "panel_width_studs": 5.0400,
        "panel_height_studs": 1.2000,
        "panel_thickness_studs": 0.0800,
        "front_face_local_center": list(board_pt(2.8800, 4.5000, 0.1300)),
        "front_face_world_center": local_to_world_pt(board_pt(2.8800, 4.5000, 0.1300)),
        "front_face_local_normal": [0.000000, round(SIN_T, 6), round(COS_T, 6)],
        "front_face_world_normal": local_to_world_vec((0.0, SIN_T, COS_T)),
        "clear_ui_text_zone_local_x": [1.8000, 3.5800],
        "badge_text_zone_local_x": [3.7000, 4.8200],
    },
    {
        "component_name": "GEO_ModeBoard_UIPanel_03_TeamClash",
        "mode_id": "TeamClash",
        "display_title": "TEAM CLASH",
        "required_state": "COMING SOON",
        "panel_plane_type": "inclined_14deg",
        "tilt_deg_from_vertical": 14.0,
        "local_x_span": [0.3600, 5.4000],
        "local_s_span": [2.2400, 3.4400],
        "local_d_span": [0.0500, 0.1300],
        "panel_width_studs": 5.0400,
        "panel_height_studs": 1.2000,
        "panel_thickness_studs": 0.0800,
        "front_face_local_center": list(board_pt(2.8800, 2.8400, 0.1300)),
        "front_face_world_center": local_to_world_pt(board_pt(2.8800, 2.8400, 0.1300)),
        "front_face_local_normal": [0.000000, round(SIN_T, 6), round(COS_T, 6)],
        "front_face_world_normal": local_to_world_vec((0.0, SIN_T, COS_T)),
        "clear_ui_text_zone_local_x": [1.8000, 3.5800],
        "badge_text_zone_local_x": [3.7000, 4.8200],
    },
    {
        "component_name": "GEO_ModeBoard_UIPanel_04_KingTile",
        "mode_id": "KingTile",
        "display_title": "KING TILE",
        "required_state": "COMING SOON",
        "panel_plane_type": "inclined_14deg",
        "tilt_deg_from_vertical": 14.0,
        "local_x_span": [0.3600, 5.4000],
        "local_s_span": [0.5800, 1.7800],
        "local_d_span": [0.0500, 0.1300],
        "panel_width_studs": 5.0400,
        "panel_height_studs": 1.2000,
        "panel_thickness_studs": 0.0800,
        "front_face_local_center": list(board_pt(2.8800, 1.1800, 0.1300)),
        "front_face_world_center": local_to_world_pt(board_pt(2.8800, 1.1800, 0.1300)),
        "front_face_local_normal": [0.000000, round(SIN_T, 6), round(COS_T, 6)],
        "front_face_world_normal": local_to_world_vec((0.0, SIN_T, COS_T)),
        "clear_ui_text_zone_local_x": [1.8000, 3.5800],
        "badge_text_zone_local_x": [3.7000, 4.8200],
    },
    {
        "component_name": "GEO_ModeBoard_HeaderSign",
        "mode_id": "HeaderSign",
        "display_title": "ARENA MODE SELECT",
        "required_state": "STATIC_HEADER",
        "panel_plane_type": "vertical_upright",
        "tilt_deg_from_vertical": 0.0,
        "local_x_span": [-5.7400, +5.7400],
        "local_y_span": [7.5400, 8.3600],
        "local_z_span": [0.4800, 0.8800],
        "panel_width_studs": 11.4800,
        "panel_height_studs": 0.8200,
        "panel_thickness_studs": 0.4000,
        "front_face_local_center": [0.0000, 7.9500, 0.8800],
        "front_face_world_center": local_to_world_pt((0.0000, 7.9500, 0.8800)),
        "front_face_local_normal": [0.000000, 0.000000, 1.000000],
        "front_face_world_normal": local_to_world_vec((0.0, 0.0, 1.0)),
        "clear_ui_text_zone_local_x": [-5.4000, +5.4000],
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
ATLAS_FILENAME = "SphereBrawl_ModeBoard_PaletteAtlas.png"


# ==============================================================================
# DETERMINISTIC MULTI-COMPONENT HARD-SURFACE MESH BUILDER
# ==============================================================================
class ModeBoardMeshBuilder:
    def __init__(self, name="SM_Hub_ModeBoard_01"):
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

    def add_simple_box(self, comp_name, mat_name, x0, x1, y0, y1, z0, z1, cap_bot=True, cap_top=True):
        loop_b = [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)]
        loop_t = [(x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)]
        self.add_closed_loft(comp_name, mat_name, loop_b, loop_t, cap_bot=cap_bot, cap_top=cap_top)

    def add_oct_box(self, comp_name, mat_name, x0, x1, y0, y1, z0, z1, ch_xz=0.15, cap_bot=True, cap_top=True):
        """
        Builds an 8-sided XZ-chamfered box with verified outward normals.
        """
        c = min(ch_xz, 0.38 * (x1 - x0), 0.38 * (z1 - z0))
        if c <= 1e-5:
            self.add_simple_box(comp_name, mat_name, x0, x1, y0, y1, z0, z1, cap_bot=cap_bot, cap_top=cap_top)
            return

        def ring(yv):
            return [
                (x0 + c, yv, z1),
                (x1 - c, yv, z1),
                (x1,     yv, z1 - c),
                (x1,     yv, z0 + c),
                (x1 - c, yv, z0),
                (x0 + c, yv, z0),
                (x0,     yv, z0 + c),
                (x0,     yv, z1 - c),
            ]

        self.add_closed_loft(comp_name, mat_name, ring(y0), ring(y1), cap_bot=cap_bot, cap_top=cap_top)

    def add_tilted_box(self, comp_name, mat_name, x0, x1, s0, s1, d0, d1, ch=0.0, cap_back=True, cap_front=True):
        """
        Builds a closed box or 8-sided chamfered prism on the 14.0° inclined board plane.
        Outward front normal is (0, SIN_T, COS_T); outward back normal is (0, -SIN_T, -COS_T).
        """
        n_front = (0.0, SIN_T, COS_T)
        n_back = (0.0, -SIN_T, -COS_T)
        c = min(ch, 0.35 * (x1 - x0), 0.35 * (s1 - s0))

        if c <= 1e-5:
            ring_b = [board_pt(x0, s0, d0), board_pt(x1, s0, d0), board_pt(x1, s1, d0), board_pt(x0, s1, d0)]
            ring_f = [board_pt(x0, s0, d1), board_pt(x1, s0, d1), board_pt(x1, s1, d1), board_pt(x0, s1, d1)]
        else:
            def make_ring(dv):
                return [
                    board_pt(x0 + c, s0,     dv),
                    board_pt(x1 - c, s0,     dv),
                    board_pt(x1,     s0 + c, dv),
                    board_pt(x1,     s1 - c, dv),
                    board_pt(x1 - c, s1,     dv),
                    board_pt(x0 + c, s1,     dv),
                    board_pt(x0,     s1 - c, dv),
                    board_pt(x0,     s0 + c, dv),
                ]
            ring_b = make_ring(d0)
            ring_f = make_ring(d1)

        n = len(ring_b)
        pts_b = [np.array(p, dtype=np.float64) for p in ring_b]
        pts_f = [np.array(p, dtype=np.float64) for p in ring_f]
        center_mid = 0.5 * (np.mean(pts_b, axis=0) + np.mean(pts_f, axis=0))

        for i in range(n):
            j = (i + 1) % n
            b0, b1 = pts_b[i], pts_b[j]
            f0, f1 = pts_f[i], pts_f[j]
            quad_mid = 0.25 * (b0 + b1 + f0 + f1)
            out_dir = quad_mid - center_mid
            if np.linalg.norm(out_dir) < 1e-6:
                out_dir = np.array(n_front)
            self.add_quad(comp_name, mat_name, b0, b1, f1, f0, expected_normal=out_dir)

        if cap_front:
            for i in range(1, n - 1):
                self.add_tri(comp_name, mat_name, pts_f[0], pts_f[i], pts_f[i + 1], expected_normal=n_front)

        if cap_back:
            for i in range(1, n - 1):
                self.add_tri(comp_name, mat_name, pts_b[0], pts_b[i + 1], pts_b[i], expected_normal=n_back)

    def add_tilted_disc(self, comp_name, mat_name, xc, sc, d0, d1, r_outer, r_inner, n_seg, rot_deg=0.0, cap_back=True, cap_front=True):
        """
        Builds a regular polygonal disc or hollow ring on the 14.0° inclined board plane.
        """
        n_front = (0.0, SIN_T, COS_T)
        n_back = (0.0, -SIN_T, -COS_T)
        angles = [math.radians(rot_deg + 360.0 * i / n_seg) for i in range(n_seg)]

        if r_inner <= 1e-5:
            ring_b = [board_pt(xc + r_outer * math.cos(a), sc + r_outer * math.sin(a), d0) for a in angles]
            ring_f = [board_pt(xc + r_outer * math.cos(a), sc + r_outer * math.sin(a), d1) for a in angles]
            pts_b = [np.array(p, dtype=np.float64) for p in ring_b]
            pts_f = [np.array(p, dtype=np.float64) for p in ring_f]
            center_mid = 0.5 * (np.mean(pts_b, axis=0) + np.mean(pts_f, axis=0))
            for i in range(n_seg):
                j = (i + 1) % n_seg
                b0, b1 = pts_b[i], pts_b[j]
                f0, f1 = pts_f[i], pts_f[j]
                out_dir = 0.25 * (b0 + b1 + f0 + f1) - center_mid
                self.add_quad(comp_name, mat_name, b0, b1, f1, f0, expected_normal=out_dir)
            if cap_front:
                for i in range(1, n_seg - 1):
                    self.add_tri(comp_name, mat_name, pts_f[0], pts_f[i], pts_f[i + 1], expected_normal=n_front)
            if cap_back:
                for i in range(1, n_seg - 1):
                    self.add_tri(comp_name, mat_name, pts_b[0], pts_b[i + 1], pts_b[i], expected_normal=n_back)
        else:
            center_pt = np.array(board_pt(xc, sc, 0.5 * (d0 + d1)), dtype=np.float64)
            for i in range(n_seg):
                j = (i + 1) % n_seg
                ci, si = math.cos(angles[i]), math.sin(angles[i])
                cj, sj = math.cos(angles[j]), math.sin(angles[j])
                p_fo_i = np.array(board_pt(xc + r_outer * ci, sc + r_outer * si, d1), dtype=np.float64)
                p_fo_j = np.array(board_pt(xc + r_outer * cj, sc + r_outer * sj, d1), dtype=np.float64)
                p_fi_i = np.array(board_pt(xc + r_inner * ci, sc + r_inner * si, d1), dtype=np.float64)
                p_fi_j = np.array(board_pt(xc + r_inner * cj, sc + r_inner * sj, d1), dtype=np.float64)

                p_bo_i = np.array(board_pt(xc + r_outer * ci, sc + r_outer * si, d0), dtype=np.float64)
                p_bo_j = np.array(board_pt(xc + r_outer * cj, sc + r_outer * sj, d0), dtype=np.float64)
                p_bi_i = np.array(board_pt(xc + r_inner * ci, sc + r_inner * si, d0), dtype=np.float64)
                p_bi_j = np.array(board_pt(xc + r_inner * cj, sc + r_inner * sj, d0), dtype=np.float64)

                if cap_front:
                    self.add_quad(comp_name, mat_name, p_fi_i, p_fo_i, p_fo_j, p_fi_j, expected_normal=n_front)
                if cap_back:
                    self.add_quad(comp_name, mat_name, p_bo_i, p_bi_i, p_bi_j, p_bo_j, expected_normal=n_back)

                out_dir = 0.25 * (p_bo_i + p_bo_j + p_fo_j + p_fo_i) - center_pt
                in_dir = center_pt - 0.25 * (p_bi_i + p_bi_j + p_fi_j + p_fi_i)
                self.add_quad(comp_name, mat_name, p_bo_i, p_bo_j, p_fo_j, p_fo_i, expected_normal=out_dir)
                self.add_quad(comp_name, mat_name, p_fi_i, p_fi_j, p_bi_j, p_bi_i, expected_normal=in_dir)

    def export_obj_and_mtl(self, obj_path, mtl_path):
        mtl_filename = os.path.basename(mtl_path)
        used_mats = [m for m in PALETTE_ORDER if m in set(self.comp_mat.values())]

        local_atlas_path = os.path.join(os.path.dirname(mtl_path), ATLAS_FILENAME)
        with open(local_atlas_path, "wb") as af:
            af.write(ATLAS_PNG_BYTES)

        with open(mtl_path, "w", encoding="utf-8") as mf:
            mf.write("# Sphere Brawl: Rolling Rampage — Material Library\n")
            mf.write(f"# Asset: {self.name} (Tactical Arena Mode Selection Command Gantry — 14.4 x 3.8 x 8.8 Studs)\n")
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
            of.write("# Sphere Brawl: Rolling Rampage — Kinetic Hub Mode Selection Board 3D Asset\n")
            of.write(f"# Asset Name: {self.name} (Phase 2 Approved Production — 14.4 x 3.8 x 8.8 Studs)\n")
            of.write("# Unit Scale: 1.0 Unit = 1.0 Roblox Stud | Up Axis: +Y | Forward Axis: +Z\n")
            of.write("# Local Origin (0,0,0): Floor-Reference Center of Footprint (Maps to World (35, 150, -326) at Yaw = -53.39292061 deg)\n")
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
            "name": "SphereBrawl_ModeBoard_PaletteAtlas",
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
            "name": "SphereBrawl_ModeBoard_PaletteAtlas_Tex",
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
                "generator": "Sphere Brawl Mode Selection Board Production Pipeline (14.4 x 3.8 x 8.8 Studs)",
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
# PROCEDURAL PRODUCTION GEOMETRY FOR SM_Hub_ModeBoard_01 (14.4 x 3.8 x 8.8 STUDS)
# ==============================================================================
def build_hub_mode_board():
    """
    Builds the approved 14.4000 (W) x 3.8000 (D) x 8.8000 (H) stud Tactical Arena Mode Selection
    Command Gantry (`SM_Hub_ModeBoard_01`) across 18 cleanly separated, non-overlapping named components:
      1.  GEO_ModeBoard_BasePlinth         (MAT_DarkNeutral) — Lower grounded anchor plinth (Y = 0.00..0.42, X in [-7.20, +7.20], Z in [-1.90, +1.90]) & central console riser
      2.  GEO_ModeBoard_BaseUpperTier      (MAT_AltNeutral)  — Upper stepped plinth tier, walk-up threshold plates, angled knee fascia & 3 rear diagonal spine ribs
      3.  GEO_ModeBoard_MainChassis        (MAT_DarkNeutral) — 14.0° inclined main command matrix chassis backplane
      4.  GEO_ModeBoard_LeftButtress       (MAT_DarkNeutral) — Left A-frame structural side buttress (X in [-7.12, -5.82])
      5.  GEO_ModeBoard_RightButtress      (MAT_DarkNeutral) — Right A-frame structural side buttress (X in [+5.82, +7.12])
      6.  GEO_ModeBoard_SideCollars        (MAT_LightTrim)   — Base bumper rail, 8 floor anchor cleats, buttress collar clamps, cheek trims & rear spine clamps
      7.  GEO_ModeBoard_CommandMatrixFrame (MAT_AltNeutral)  — Outer buttress cheek plates, active hero bay surround, and 3 recessed locked bay pocket frames
      8.  GEO_ModeBoard_UIPanel_01_FFA     (MAT_DarkNeutral) — Separate flat UI-ready surface for FREE-FOR-ALL — ACTIVE (4.08 W x 3.78 H studs on 14° plane)
      9.  GEO_ModeBoard_UIPanel_02_Duel    (MAT_DarkNeutral) — Separate flat UI-ready surface for DUEL — COMING SOON (5.04 W x 1.20 H studs on 14° plane)
      10. GEO_ModeBoard_UIPanel_03_TeamClash (MAT_DarkNeutral) — Separate flat UI-ready surface for TEAM CLASH — COMING SOON (5.04 W x 1.20 H studs on 14° plane)
      11. GEO_ModeBoard_UIPanel_04_KingTile  (MAT_DarkNeutral) — Separate flat UI-ready surface for KING TILE — COMING SOON (5.04 W x 1.20 H studs on 14° plane)
      12. GEO_ModeBoard_HeaderCanopy       (MAT_DarkNeutral) — Cantilevered overhead command visor hood & top crest (Y = 7.45..8.80)
      13. GEO_ModeBoard_HeaderSign         (MAT_AltNeutral)  — Separate flat UI-ready header marquee panel (11.48 W x 0.82 H studs, upright at Z = +0.88)
      14. GEO_ModeBoard_ActiveModeReticle  (MAT_LightTrim)   — Active hero bay metallic bezel, corner chevron brackets, central sphere-clash reticle disc & 4 directional arrows
      15. GEO_ModeBoard_LockReliefs        (MAT_LightTrim)   — Physical mechanical lockdown clamp bars, right-hand lock badge housings & 3D padlock relief icons on Bays 02..04
      16. GEO_ModeBoard_ModeReliefs        (MAT_LightTrim)   — Mode-specific 3D relief motifs on Bays 02..04 (opposing 1v1 hexagons, twin team shields, crowned diamond tile) + central matrix divider & header bezel
      17. GEO_ModeBoard_CyanAccents        (EMI_Cyan)        — Active Free-for-All perimeter energy conduit, status header pill, reticle energy ring, left buttress conduit, left floor strip & top visor light bar
      18. GEO_ModeBoard_AmberAccents       (EMI_Amber)       — Restrained Coming Soon lock-status ticks on Bays 02..04, right lower buttress tick & right floor standby tick
    """
    mb = ModeBoardMeshBuilder("SM_Hub_ModeBoard_01")

    comp_specs = [
        ("GEO_ModeBoard_BasePlinth",         "MAT_DarkNeutral"),
        ("GEO_ModeBoard_BaseUpperTier",      "MAT_AltNeutral"),
        ("GEO_ModeBoard_MainChassis",        "MAT_DarkNeutral"),
        ("GEO_ModeBoard_LeftButtress",       "MAT_DarkNeutral"),
        ("GEO_ModeBoard_RightButtress",      "MAT_DarkNeutral"),
        ("GEO_ModeBoard_SideCollars",        "MAT_LightTrim"),
        ("GEO_ModeBoard_CommandMatrixFrame", "MAT_AltNeutral"),
        ("GEO_ModeBoard_UIPanel_01_FFA",     "MAT_DarkNeutral"),
        ("GEO_ModeBoard_UIPanel_02_Duel",    "MAT_DarkNeutral"),
        ("GEO_ModeBoard_UIPanel_03_TeamClash", "MAT_DarkNeutral"),
        ("GEO_ModeBoard_UIPanel_04_KingTile",  "MAT_DarkNeutral"),
        ("GEO_ModeBoard_HeaderCanopy",       "MAT_DarkNeutral"),
        ("GEO_ModeBoard_HeaderSign",         "MAT_AltNeutral"),
        ("GEO_ModeBoard_ActiveModeReticle",  "MAT_LightTrim"),
        ("GEO_ModeBoard_LockReliefs",        "MAT_LightTrim"),
        ("GEO_ModeBoard_ModeReliefs",        "MAT_LightTrim"),
        ("GEO_ModeBoard_CyanAccents",        "EMI_Cyan"),
        ("GEO_ModeBoard_AmberAccents",       "EMI_Amber"),
    ]
    for cname, mname in comp_specs:
        mb.ensure_component(cname, mname)

    # --------------------------------------------------------------------------
    # 1. GEO_ModeBoard_BasePlinth (MAT_DarkNeutral)
    #    Strict outer footprint: X in [-7.2000, +7.2000], Z in [-1.9000, +1.9000], Y_min = 0.0000
    # --------------------------------------------------------------------------
    mb.add_oct_box(
        "GEO_ModeBoard_BasePlinth", "MAT_DarkNeutral",
        x0=-7.2000, x1=+7.2000, y0=0.0000, y1=0.4200, z0=-1.9000, z1=+1.9000,
        ch_xz=0.4500, cap_bot=True, cap_top=True
    )
    # Central console pedestal riser supporting the inclined board hinge (Y = 0.8800 .. 1.7200)
    mb.add_oct_box(
        "GEO_ModeBoard_BasePlinth", "MAT_DarkNeutral",
        x0=-5.7600, x1=+5.7600, y0=0.8800, y1=1.7200, z0=-1.4500, z1=+1.0200,
        ch_xz=0.2200, cap_bot=False, cap_top=True
    )

    # --------------------------------------------------------------------------
    # 2. GEO_ModeBoard_BaseUpperTier (MAT_AltNeutral)
    #    Upper stepped plinth deck (Y = 0.4200 .. 0.8800), walk-up threshold plates,
    #    lower console knee fascia, and 3 rear diagonal structural spine ribs
    # --------------------------------------------------------------------------
    mb.add_oct_box(
        "GEO_ModeBoard_BaseUpperTier", "MAT_AltNeutral",
        x0=-6.8500, x1=+6.8500, y0=0.4200, y1=0.8800, z0=-1.7200, z1=+1.5200,
        ch_xz=0.3500, cap_bot=False, cap_top=True
    )
    # Front walk-up threshold plates (Y = 0.4200 .. 0.5000, Z = +1.5200 .. +1.7400)
    for (xp0, xp1) in [(-5.4500, -0.5500), (+0.2500, +5.4500)]:
        mb.add_simple_box(
            "GEO_ModeBoard_BaseUpperTier", "MAT_AltNeutral",
            x0=xp0, x1=xp1, y0=0.4200, y1=0.5000, z0=+1.5200, z1=+1.7400,
            cap_bot=False, cap_top=True
        )
    # Angled lower console knee armor fascia (Y = 0.9400 .. 1.5800, Z = +1.0200 .. +1.3400)
    mb.add_simple_box(
        "GEO_ModeBoard_BaseUpperTier", "MAT_AltNeutral",
        x0=-5.5500, x1=-0.4500, y0=0.9400, y1=1.5800, z0=+1.0200, z1=+1.3400,
        cap_bot=True, cap_top=True
    )
    mb.add_simple_box(
        "GEO_ModeBoard_BaseUpperTier", "MAT_AltNeutral",
        x0=+0.1500, x1=+5.5500, y0=0.9400, y1=1.5800, z0=+1.0200, z1=+1.3400,
        cap_bot=True, cap_top=True
    )
    # Three rear diagonal structural spine ribs bracing the inclined command matrix (X = -4.20, 0.00, +4.20)
    for xr in (-4.2000, 0.0000, +4.2000):
        mb.add_simple_box(
            "GEO_ModeBoard_BaseUpperTier", "MAT_AltNeutral",
            x0=xr - 0.3400, x1=xr + 0.3400, y0=0.8800, y1=7.4500, z0=-1.7600, z1=-0.6200,
            cap_bot=False, cap_top=False
        )

    # --------------------------------------------------------------------------
    # 3. GEO_ModeBoard_MainChassis (MAT_DarkNeutral)
    #    14.0° inclined main command matrix chassis backplane (s in [0.00, 5.75], d in [-0.72, +0.02])
    # --------------------------------------------------------------------------
    mb.add_tilted_box(
        "GEO_ModeBoard_MainChassis", "MAT_DarkNeutral",
        x0=-5.8000, x1=+5.8000, s0=0.0000, s1=5.7500, d0=-0.7200, d1=+0.0200,
        ch=0.1000, cap_back=True, cap_front=True
    )

    # --------------------------------------------------------------------------
    # 4 & 5. GEO_ModeBoard_LeftButtress & GEO_ModeBoard_RightButtress (MAT_DarkNeutral)
    # --------------------------------------------------------------------------
    for side, comp_b in [(-1.0, "GEO_ModeBoard_LeftButtress"), (+1.0, "GEO_ModeBoard_RightButtress")]:
        xa = min(5.8200 * side, 7.0800 * side)
        xb = max(5.8200 * side, 7.0800 * side)
        # Lower A-frame buttress anchor leg (Y = 0.8800 .. 4.1500, Z = -1.6600 .. +1.3600)
        mb.add_oct_box(
            comp_b, "MAT_DarkNeutral",
            x0=xa, x1=xb, y0=0.8800, y1=4.1500, z0=-1.6600, z1=+1.3600,
            ch_xz=0.1600, cap_bot=False, cap_top=True
        )
        # Upper inclined gantry pillar (Y = 4.1500 .. 8.3500, Z = -1.7400 .. +0.6800)
        mb.add_oct_box(
            comp_b, "MAT_DarkNeutral",
            x0=xa + 0.0400, x1=xb - 0.0400, y0=4.1500, y1=8.3500, z0=-1.7400, z1=+0.6800,
            ch_xz=0.1400, cap_bot=False, cap_top=True
        )

    # --------------------------------------------------------------------------
    # 6. GEO_ModeBoard_SideCollars (MAT_LightTrim)
    #    Base front bumper rail, 8 floor anchor cleats, buttress collar clamps,
    #    tilted side bumper rails, and rear spine collar clamps
    # --------------------------------------------------------------------------
    # Front lower bumper rail (Z = +1.7600 .. +1.9000)
    mb.add_simple_box(
        "GEO_ModeBoard_SideCollars", "MAT_LightTrim",
        x0=-6.2000, x1=+6.2000, y0=0.1200, y1=0.3400, z0=+1.7600, z1=+1.8950,
        cap_bot=True, cap_top=True
    )
    # 4 front and 4 rear floor anchor cleats (COMP_Hub_CornerBracket_01 family)
    for xc in (-6.5500, -2.2000, +2.2000, +6.5500):
        mb.add_simple_box(
            "GEO_ModeBoard_SideCollars", "MAT_LightTrim",
            x0=xc - 0.3600, x1=xc + 0.3600, y0=0.0200, y1=0.5200, z0=+1.4400, z1=+1.8800,
            cap_bot=True, cap_top=True
        )
        mb.add_simple_box(
            "GEO_ModeBoard_SideCollars", "MAT_LightTrim",
            x0=xc - 0.3600, x1=xc + 0.3600, y0=0.0200, y1=0.5200, z0=-1.8800, z1=-1.4400,
            cap_bot=True, cap_top=True
        )
    # Side buttress collar clamps at Y = 2.25..2.65 and Y = 5.65..6.05 + tilted front bumper fin
    for side in (-1.0, +1.0):
        xa = min(5.7800 * side, 7.1400 * side)
        xb = max(5.7800 * side, 7.1400 * side)
        mb.add_simple_box(
            "GEO_ModeBoard_SideCollars", "MAT_LightTrim",
            x0=xa, x1=xb, y0=2.2500, y1=2.6500, z0=-1.4800, z1=+1.1600,
            cap_bot=True, cap_top=True
        )
        mb.add_simple_box(
            "GEO_ModeBoard_SideCollars", "MAT_LightTrim",
            x0=xa, x1=xb, y0=5.6500, y1=6.0500, z0=-1.5800, z1=+0.6200,
            cap_bot=True, cap_top=True
        )
        txa = min(6.0200 * side, 6.8800 * side)
        txb = max(6.0200 * side, 6.8800 * side)
        mb.add_tilted_box(
            "GEO_ModeBoard_SideCollars", "MAT_LightTrim",
            x0=txa, x1=txb, s0=0.3500, s1=5.3000, d0=+0.2800, d1=+0.4000,
            ch=0.0, cap_back=False, cap_front=True
        )
    # Rear spine mid-height collar clamps
    for xr in (-4.2000, 0.0000, +4.2000):
        mb.add_simple_box(
            "GEO_ModeBoard_SideCollars", "MAT_LightTrim",
            x0=xr - 0.4000, x1=xr + 0.4000, y0=3.8000, y1=4.2000, z0=-1.8200, z1=-0.5600,
            cap_bot=True, cap_top=True
        )

    # --------------------------------------------------------------------------
    # 7. GEO_ModeBoard_CommandMatrixFrame (MAT_AltNeutral)
    #    Outer buttress cheek armor plates (reaching X = +-7.2000), tilted buttress fins,
    #    raised active Free-for-All surround, and 3 recessed Coming Soon bay pocket frames
    # --------------------------------------------------------------------------
    for side in (-1.0, +1.0):
        c0 = min(7.0800 * side, 7.2000 * side)
        c1 = max(7.0800 * side, 7.2000 * side)
        mb.add_simple_box(
            "GEO_ModeBoard_CommandMatrixFrame", "MAT_AltNeutral",
            x0=c0, x1=c1, y0=1.1000, y1=7.2000, z0=-1.3200, z1=+0.8200,
            cap_bot=True, cap_top=True
        )
        fa = min(5.9200 * side, 6.9800 * side)
        fb = max(5.9200 * side, 6.9800 * side)
        mb.add_tilted_box(
            "GEO_ModeBoard_CommandMatrixFrame", "MAT_AltNeutral",
            x0=fa, x1=fb, s0=0.1200, s1=5.5500, d0=+0.0200, d1=+0.2800,
            ch=0.0, cap_back=False, cap_front=True
        )

    # Left Hero Bay (Free-for-All) raised armor surround (X in [-5.58, -0.42], s in [0.42, 5.28], d in [+0.02, +0.22])
    mb.add_tilted_box(
        "GEO_ModeBoard_CommandMatrixFrame", "MAT_AltNeutral",
        x0=-5.5800, x1=-0.4200, s0=0.4200, s1=5.2800, d0=+0.0200, d1=+0.2200,
        ch=0.0800, cap_back=False, cap_front=True
    )
    # Active status sub-banner backing bar at bottom of Free-for-All panel
    mb.add_tilted_box(
        "GEO_ModeBoard_CommandMatrixFrame", "MAT_AltNeutral",
        x0=-4.7500, x1=-1.2500, s0=1.1200, s1=1.5200, d0=+0.3000, d1=+0.3800,
        ch=0.0, cap_back=False, cap_front=True
    )

    # Three Right-Hand Recessed Coming Soon Bay Pocket Frames (d in [+0.02, +0.05])
    # and right-hand lock badge backing plates (d in [+0.13, +0.22])
    for (s_bot, s_top) in [(3.7600, 5.2400), (2.1000, 3.5800), (0.4400, 1.9200)]:
        s_mid = 0.5 * (s_bot + s_top)
        mb.add_tilted_box(
            "GEO_ModeBoard_CommandMatrixFrame", "MAT_AltNeutral",
            x0=+0.1800, x1=+5.5800, s0=s_bot, s1=s_top, d0=+0.0200, d1=+0.0500,
            ch=0.0500, cap_back=False, cap_front=True
        )
        mb.add_tilted_box(
            "GEO_ModeBoard_CommandMatrixFrame", "MAT_AltNeutral",
            x0=+3.6400, x1=+5.0200, s0=s_mid - 0.2600, s1=s_mid + 0.2600, d0=+0.1300, d1=+0.2200,
            ch=0.0, cap_back=False, cap_front=True
        )

    # --------------------------------------------------------------------------
    # 8, 9, 10, 11. FOUR SEPARATE UI-READY MODE PANEL SURFACES (MAT_DarkNeutral)
    #    - GEO_ModeBoard_UIPanel_01_FFA       (d = +0.2200 .. +0.3000 -> raised +0.17 studs ahead of locked panels!)
    #    - GEO_ModeBoard_UIPanel_02_Duel      (d = +0.0500 .. +0.1300)
    #    - GEO_ModeBoard_UIPanel_03_TeamClash (d = +0.0500 .. +0.1300)
    #    - GEO_ModeBoard_UIPanel_04_KingTile  (d = +0.0500 .. +0.1300)
    #    ZERO baked text triangles! Flat, clean, replaceable SurfaceGui target planes.
    # --------------------------------------------------------------------------
    mb.add_tilted_box(
        "GEO_ModeBoard_UIPanel_01_FFA", "MAT_DarkNeutral",
        x0=-5.0400, x1=-0.9600, s0=0.9600, s1=4.7400, d0=+0.2200, d1=+0.3000,
        ch=0.0, cap_back=False, cap_front=True
    )
    mb.add_tilted_box(
        "GEO_ModeBoard_UIPanel_02_Duel", "MAT_DarkNeutral",
        x0=+0.3600, x1=+5.4000, s0=3.9000, s1=5.1000, d0=+0.0500, d1=+0.1300,
        ch=0.0, cap_back=False, cap_front=True
    )
    mb.add_tilted_box(
        "GEO_ModeBoard_UIPanel_03_TeamClash", "MAT_DarkNeutral",
        x0=+0.3600, x1=+5.4000, s0=2.2400, s1=3.4400, d0=+0.0500, d1=+0.1300,
        ch=0.0, cap_back=False, cap_front=True
    )
    mb.add_tilted_box(
        "GEO_ModeBoard_UIPanel_04_KingTile", "MAT_DarkNeutral",
        x0=+0.3600, x1=+5.4000, s0=0.5800, s1=1.7800, d0=+0.0500, d1=+0.1300,
        ch=0.0, cap_back=False, cap_front=True
    )

    # --------------------------------------------------------------------------
    # 12. GEO_ModeBoard_HeaderCanopy (MAT_DarkNeutral)
    #     Cantilevered overhead command visor hood & top crest (Y = 7.4500 .. 8.8000)
    # --------------------------------------------------------------------------
    mb.add_oct_box(
        "GEO_ModeBoard_HeaderCanopy", "MAT_DarkNeutral",
        x0=-6.8000, x1=+6.8000, y0=7.4500, y1=8.5500, z0=-1.5500, z1=+0.4800,
        ch_xz=0.2800, cap_bot=True, cap_top=True
    )
    mb.add_oct_box(
        "GEO_ModeBoard_HeaderCanopy", "MAT_DarkNeutral",
        x0=-5.6000, x1=+5.6000, y0=8.5500, y1=8.8000, z0=-1.2500, z1=+0.3500,
        ch_xz=0.2200, cap_bot=False, cap_top=True
    )

    # --------------------------------------------------------------------------
    # 13. GEO_ModeBoard_HeaderSign (MAT_AltNeutral)
    #     Separate flat UI-ready header marquee panel (11.48 W x 0.82 H studs, front face at Z = +0.8800)
    # --------------------------------------------------------------------------
    mb.add_simple_box(
        "GEO_ModeBoard_HeaderSign", "MAT_AltNeutral",
        x0=-5.7400, x1=+5.7400, y0=7.5400, y1=8.3600, z0=+0.4800, z1=+0.8800,
        cap_bot=False, cap_top=False
    )

    # --------------------------------------------------------------------------
    # 14. GEO_ModeBoard_ActiveModeReticle (MAT_LightTrim)
    #     Active Free-for-All perimeter metallic bezel, 4 corner chevron brackets,
    #     central 3D sphere-clash reticle disc & 4 inward directional arrows
    # --------------------------------------------------------------------------
    # Perimeter bezel rails around Free-for-All (d in [+0.2200, +0.4000])
    mb.add_tilted_box("GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim", -5.5400, -0.4600, 4.9200, 5.2400, +0.2200, +0.4000, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim", -5.5400, -0.4600, 0.4600, 0.7800, +0.2200, +0.4000, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim", -5.5400, -5.2200, 0.7800, 4.9200, +0.2200, +0.4000, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim", -0.7800, -0.4600, 0.7800, 4.9200, +0.2200, +0.4000, cap_back=False, cap_front=True)

    # 4 corner chevron brackets (d in [+0.4000, +0.4800])
    for (cx0, cx1) in [(-5.6000, -4.8600), (-1.1400, -0.4000)]:
        for (cs0, cs1) in [(0.4000, 1.0400), (4.6600, 5.3000)]:
            mb.add_tilted_box("GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim", cx0, cx1, cs0, cs1, +0.4000, +0.4800, cap_back=True, cap_front=True)

    # Central 3D Arena Sphere core disc (xc = -3.0000, sc = 2.9500, r = 0.4600, d in [+0.3000, +0.4500])
    mb.add_tilted_disc(
        "GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim",
        xc=-3.0000, sc=2.9500, d0=+0.3000, d1=+0.4500, r_outer=0.4600, r_inner=0.0, n_seg=12,
        cap_back=False, cap_front=True
    )
    # 4 directional clash reticle bars around the sphere emblem
    mb.add_tilted_box("GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim", -4.2400, -3.9600, 2.8300, 3.0700, +0.3000, +0.4300, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim", -2.0400, -1.7600, 2.8300, 3.0700, +0.3000, +0.4300, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim", -3.1200, -2.8800, 3.9100, 4.1400, +0.3000, +0.4300, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_ActiveModeReticle", "MAT_LightTrim", -3.1200, -2.8800, 1.7600, 1.9900, +0.3000, +0.4300, cap_back=False, cap_front=True)

    # --------------------------------------------------------------------------
    # 15. GEO_ModeBoard_LockReliefs (MAT_LightTrim)
    #     Physical mechanical lockdown clamp bars, right-hand lock badge bezel rails,
    #     and 3D padlock relief icons on the 3 Coming Soon bays
    # --------------------------------------------------------------------------
    for (s_bot, s_top) in [(3.7600, 5.2400), (2.1000, 3.5800), (0.4400, 1.9200)]:
        s_mid = 0.5 * (s_bot + s_top)
        # Left & right vertical mechanical lockdown clamp bars (d in [+0.1300, +0.2600])
        mb.add_tilted_box("GEO_ModeBoard_LockReliefs", "MAT_LightTrim", +0.1600, +0.6800, s_bot + 0.0800, s_top - 0.0800, +0.1300, +0.2600, cap_back=True, cap_front=True)
        mb.add_tilted_box("GEO_ModeBoard_LockReliefs", "MAT_LightTrim", +5.0800, +5.6000, s_bot + 0.0800, s_top - 0.0800, +0.1300, +0.2600, cap_back=True, cap_front=True)
        # Horizontal lock badge top/bottom clamp rails
        mb.add_tilted_box("GEO_ModeBoard_LockReliefs", "MAT_LightTrim", +3.6600, +5.0000, s_mid - 0.3400, s_mid - 0.2600, +0.1300, +0.2600, cap_back=False, cap_front=True)
        mb.add_tilted_box("GEO_ModeBoard_LockReliefs", "MAT_LightTrim", +3.6600, +5.0000, s_mid + 0.2600, s_mid + 0.3400, +0.1300, +0.2600, cap_back=False, cap_front=True)
        # 3D Padlock relief icon (body + shackle ring at x = +0.9500)
        mb.add_tilted_box("GEO_ModeBoard_LockReliefs", "MAT_LightTrim", +0.7200, +1.1800, s_mid - 0.3200, s_mid + 0.0400, +0.1300, +0.2400, cap_back=False, cap_front=True)
        mb.add_tilted_disc(
            "GEO_ModeBoard_LockReliefs", "MAT_LightTrim",
            xc=+0.9500, sc=s_mid + 0.0800, d0=+0.1300, d1=+0.2200, r_outer=0.1800, r_inner=0.1000, n_seg=6,
            cap_back=False, cap_front=True
        )

    # --------------------------------------------------------------------------
    # 16. GEO_ModeBoard_ModeReliefs (MAT_LightTrim)
    #     Distinct mode-specific 3D relief icons for Duel, Team Clash & King Tile,
    #     plus the main command matrix top/bottom/center divider bezels & header sign bezel
    # --------------------------------------------------------------------------
    # Duel (s_mid = 4.50): Twin opposing 1v1 hexagonal clash emblems
    mb.add_tilted_disc("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", +1.3400, 4.5000, +0.1300, +0.2300, 0.1400, 0.0, 6, rot_deg=0.0, cap_back=False, cap_front=True)
    mb.add_tilted_disc("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", +1.5800, 4.5000, +0.1300, +0.2300, 0.1400, 0.0, 6, rot_deg=180.0, cap_back=False, cap_front=True)

    # Team Clash (s_mid = 2.84): Interlocking twin team-shield rings
    mb.add_tilted_disc("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", +1.3600, 2.9000, +0.1300, +0.2300, 0.1500, 0.0600, 6, rot_deg=30.0, cap_back=False, cap_front=True)
    mb.add_tilted_disc("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", +1.5600, 2.7800, +0.1300, +0.2300, 0.1500, 0.0600, 6, rot_deg=30.0, cap_back=False, cap_front=True)

    # King Tile (s_mid = 1.18): Diamond arena tile + crown bar
    mb.add_tilted_disc("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", +1.4600, 1.1300, +0.1300, +0.2300, 0.1700, 0.0, 4, rot_deg=0.0, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", +1.3200, +1.6000, 1.3200, 1.4100, +0.1300, +0.2300, cap_back=False, cap_front=True)

    # Main command matrix top, bottom, and central vertical spine divider bezels
    mb.add_tilted_box("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", -5.8000, +5.8000, 0.0500, 0.3500, +0.0200, +0.2400, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", -5.8000, +5.8000, 5.3800, 5.6800, +0.0200, +0.2400, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", -0.2400, +0.0200, 0.3500, 5.3800, +0.0200, +0.2800, cap_back=False, cap_front=True)

    # Overhead Header Sign metallic top/bottom/side bezel frame
    mb.add_simple_box("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", -5.9500, +5.9500, 8.3600, 8.5200, +0.4800, +0.9600, cap_bot=True, cap_top=True)
    mb.add_simple_box("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", -5.9500, +5.9500, 7.3800, 7.5400, +0.4800, +0.9600, cap_bot=True, cap_top=True)
    mb.add_simple_box("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", -6.0400, -5.7400, 7.5400, 8.3600, +0.4800, +0.9600, cap_bot=False, cap_top=False)
    mb.add_simple_box("GEO_ModeBoard_ModeReliefs", "MAT_LightTrim", +5.7400, +6.0400, 7.5400, 8.3600, +0.4800, +0.9600, cap_bot=False, cap_top=False)

    # --------------------------------------------------------------------------
    # 17. GEO_ModeBoard_CyanAccents (EMI_Cyan)
    #     Active Free-for-All perimeter energy conduit frame, active status header pill,
    #     central sphere-clash reticle ring, left/right upper buttress conduits,
    #     left approach floor guide strip, knee fascia strip & top visor light bar
    # --------------------------------------------------------------------------
    # Perimeter cyan energy frame around Free-for-All UI panel (d in [+0.2200, +0.3500])
    mb.add_tilted_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -5.2200, -0.7800, 4.7400, 4.9200, +0.2200, +0.3500, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -5.2200, -0.7800, 0.7800, 0.9600, +0.2200, +0.3500, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -5.2200, -5.0400, 0.9600, 4.7400, +0.2200, +0.3500, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -0.9600, -0.7800, 0.9600, 4.7400, +0.2200, +0.3500, cap_back=False, cap_front=True)

    # Top 'ACTIVE — ALPHA' status pill housing on Free-for-All panel
    mb.add_tilted_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -4.7500, -1.2500, 4.1800, 4.5800, +0.3000, +0.4000, cap_back=False, cap_front=True)
    # Bottom active sub-banner accent line
    mb.add_tilted_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -4.6500, -1.3500, 1.0200, 1.1200, +0.3000, +0.4000, cap_back=False, cap_front=True)

    # Central 3D sphere-clash outer cyan energy ring (xc = -3.0000, sc = 2.9500, r = 0.68..0.92)
    mb.add_tilted_disc(
        "GEO_ModeBoard_CyanAccents", "EMI_Cyan",
        xc=-3.0000, sc=2.9500, d0=+0.3000, d1=+0.4200, r_outer=0.9200, r_inner=0.6800, n_seg=12,
        cap_back=False, cap_front=True
    )

    # Left & Right side buttress cyan conduits
    mb.add_tilted_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -6.5800, -6.3200, 0.6000, 5.0500, +0.4000, +0.4600, cap_back=False, cap_front=True)
    mb.add_tilted_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", +6.3200, +6.5800, 3.6000, 5.0500, +0.4000, +0.4600, cap_back=False, cap_front=True)

    # Left floor walk-up guide strip & lower knee fascia cyan bar
    mb.add_simple_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -5.5000, -0.4500, 0.4200, 0.4800, +1.7400, +1.8400, cap_bot=False, cap_top=True)
    mb.add_simple_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -5.3000, -0.7000, 1.2000, 1.3000, +1.3400, +1.4000, cap_bot=True, cap_top=True)

    # Overhead Header Sign upper cyan illumination bar & active-side canopy beacon
    mb.add_simple_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -5.6500, +5.6500, 8.2600, 8.3500, +0.8800, +0.9400, cap_bot=True, cap_top=True)
    mb.add_simple_box("GEO_ModeBoard_CyanAccents", "EMI_Cyan", -5.2000, -0.6000, 8.6200, 8.7400, +0.3500, +0.4200, cap_bot=True, cap_top=True)

    # --------------------------------------------------------------------------
    # 18. GEO_ModeBoard_AmberAccents (EMI_Amber)
    #     Restrained Coming Soon lock-status ticks on Bays 02..04, right buttress
    #     lower standby tick & right floor standby tick
    # --------------------------------------------------------------------------
    for s_mid in (4.5000, 2.8400, 1.1800):
        mb.add_tilted_box(
            "GEO_ModeBoard_AmberAccents", "EMI_Amber",
            x0=+4.8400, x1=+5.0200, s0=s_mid - 0.1600, s1=s_mid + 0.1600, d0=+0.2200, d1=+0.2700,
            cap_back=False, cap_front=True
        )
    mb.add_tilted_box("GEO_ModeBoard_AmberAccents", "EMI_Amber", +6.3200, +6.5800, 0.6000, 1.8000, +0.4000, +0.4600, cap_back=False, cap_front=True)
    mb.add_simple_box("GEO_ModeBoard_AmberAccents", "EMI_Amber", +1.8000, +3.9000, 0.4200, 0.4800, +1.7400, +1.8200, cap_bot=False, cap_top=True)

    return mb


def build_collision_proxy():
    """
    Constructs an optional, isolated simplified structural collision proxy (`COL_ModeBoard_Body`, 36 triangles)
    that blocks the grounded base and main gantry hull without filling the player approach space in front of
    the panels (`Local Z > +1.36` remains open above `Y = 0.88`) or creating thin snagging protrusions.
    """
    cb = ModeBoardMeshBuilder("COL_ModeBoard_Body")
    cb.ensure_component("COL_ModeBoard_BaseHull", "MAT_DarkNeutral")
    cb.ensure_component("COL_ModeBoard_MainGantryHull", "MAT_DarkNeutral")
    cb.ensure_component("COL_ModeBoard_CanopyHull", "MAT_DarkNeutral")

    # 1. Lower base step hull (X in [-7.20, +7.20], Y in [0.00, 0.88], Z in [-1.90, +1.52])
    cb.add_simple_box(
        "COL_ModeBoard_BaseHull", "MAT_DarkNeutral",
        x0=-7.2000, x1=+7.2000, y0=0.0000, y1=0.8800, z0=-1.9000, z1=+1.5200
    )
    # 2. Main gantry & buttress core hull (X in [-7.08, +7.08], Y in [0.88, 7.45], Z in [-1.76, +1.02])
    cb.add_simple_box(
        "COL_ModeBoard_MainGantryHull", "MAT_DarkNeutral",
        x0=-7.0800, x1=+7.0800, y0=0.8800, y1=7.4500, z0=-1.7600, z1=+1.0200
    )
    # 3. Upper canopy hood hull (X in [-6.80, +6.80], Y in [7.45, 8.80], Z in [-1.55, +0.88])
    cb.add_simple_box(
        "COL_ModeBoard_CanopyHull", "MAT_DarkNeutral",
        x0=-6.8000, x1=+6.8000, y0=7.4500, y1=8.8000, z0=-1.5500, z1=+0.8800
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
    out_dir = "./meshes"
    if "--out_dir" in sys.argv:
        idx = sys.argv.index("--out_dir")
        if idx + 1 < len(sys.argv):
            out_dir = sys.argv[idx + 1]
    os.makedirs(out_dir, exist_ok=True)

    mb = build_hub_mode_board()
    obj_out = os.path.join(out_dir, "SM_Hub_ModeBoard_01.obj")
    mtl_out = os.path.join(out_dir, "SM_Hub_ModeBoard_01.mtl")
    glb_out = os.path.join(out_dir, "SM_Hub_ModeBoard_01.glb")
    mb.export_obj_and_mtl(obj_out, mtl_out)
    mb.export_glb(glb_out)

    col_dir = os.path.join(out_dir, "collision_proxy")
    os.makedirs(col_dir, exist_ok=True)
    cb = build_collision_proxy()
    cb.export_obj_and_mtl(
        os.path.join(col_dir, "COL_ModeBoard_Body.obj"),
        os.path.join(col_dir, "COL_ModeBoard_Body.mtl"),
    )
    cb.export_glb(os.path.join(col_dir, "COL_ModeBoard_Body.glb"))

    if HAS_BPY:
        blend_out = os.path.join(out_dir, "SM_Hub_ModeBoard_01.blend")
        build_in_blender(mb, save_blend_path=blend_out)
        print(f"Saved Blender source to {blend_out}")

    total_tris = sum(len(t) for t in mb.comp_tris.values())
    print(f"Successfully generated production SM_Hub_ModeBoard_01 in {out_dir} ({total_tris} triangles across {len(mb.comp_order)} components).")
