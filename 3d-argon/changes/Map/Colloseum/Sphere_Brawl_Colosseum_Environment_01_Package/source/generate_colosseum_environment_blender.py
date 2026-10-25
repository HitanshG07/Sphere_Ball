#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — MAP 01, PHASE 2 FINAL PRODUCTION GENERATOR
Canonical Asset ID: SM_ArenaEnvironment_Colosseum_01
Package Directory:  Sphere_Brawl_Colosseum_Environment_01_Package/
====================================================================================================
Deterministic High-Detail 3D Roman Amphitheatre Production Kit Generator & Exporter.
Built directly upon the approved Concept 02 baseline (`Sphere_Brawl_Colosseum_Environment_Concept_02`,
input archive SHA-256: `78a010a3d194f4c2b4577265c4628d8266e7bc7323efa32a5082bae4934b85d4`) while
implementing all Phase 2 production refinements, modular archetype exports, quadrant-split MeshParts
(< 20,000 triangles each), and full UV/normal/material export consistency.

Can be executed either:
  1. Standalone via Python 3 (`python3 source/generate_colosseum_environment_blender.py`), or
  2. Inside Blender 3.6+/4.x (`blender --background --python source/generate_colosseum_environment_blender.py`).
     In the current Linux VM environment, `/usr/bin/blender` is unavailable, so `.blend` binary
     generation is recorded as `NOT GENERATED — BLENDER UNAVAILABLE` while all `.obj`, `.mtl`,
     `.glb`, `.gltf`, `.bin`, `.fbx`, and `.png` production files are deterministically generated.

Key Phase 2 Production Refinements (Section 4.1, 5, 6, 7):
  1. Refined Classical Capitals & Mouldings:
     - Tuscan/Doric (Story 1): Turned astragal necking ring, hypotrachelium neck, 3-ring curved
       echinus ovolo torus cushion, throat fillet, and 2-step cyma-moulded square abacus.
     - Ionic (Story 2): Carved echinus cushion, channel bridge (canalis), contoured side bolsters
       (pulvini) with waist cinch, and true multi-turn coiled 3D involute spiral volute ribbons
       (curling 2 full turns around a raised bronze oculus eye on both front and back faces).
     - Corinthian (Story 3, Interior Porticus & Triumphal Gates): Tapered inner calathus bell,
       two staggered tiers of 8 contoured 3D overhanging acanthus leaves (16 multi-segment leaves
       per capital with raised central midribs and recurved overhanging leaf tips), 4 diagonal
       corner caulicoli volute helices, 2-step concave-profiled abacus, and central bronze fleuron.
  2. Exact 5-Archetype Modular Kit (Zero Uncounted or Duplicate Geometry):
     - `UMOD_01_Standard_Window_Bay` (12 instances: Even window bays with solid balteus & scalaria stair)
     - `UMOD_02_Standard_Clipeus_Bay` (20 instances: Odd clipeus shield bays with solid balteus)
     - `UMOD_03_Vomitorium_Cavea_Bay` (8 instances: Even window bays with vaulted 7-voussoir vomitorium & scalaria stair)
     - `UMOD_04_Cardinal_Triumphal_Gate_Pavilion` (4 instances: North, East, South, West 2-bay Triumphal Gates including sub-arena foundation drum)
     - `UMOD_05_North_Imperial_Reactor_Crest` (1 instance: North Imperial Tribune & Reactor Oculus crowning North Gate to Y = 125.00)
     Every archetype is < 9,800 triangles, and `12*UMOD_01 + 20*UMOD_02 + 8*UMOD_03 + 4*UMOD_04 + 1*UMOD_05`
     equals the EXACT assembled scene triangle count with 0 leftover or double-counted triangles.
  3. Import-Safe Section MeshParts (< 20,000 Triangles Hard Gate):
     - Both the assembled exports (`meshes/SM_ArenaEnvironment_Colosseum_01.*`) and the individual
       section exports (`meshes/sections/COL_*`) are partitioned into 29 named MeshPart groups
       where every single MeshPart is strictly < 15,500 triangles (well below Roblox's 20,000 cap).
  4. Full UV, Normal & 12-Material PBR Consistency:
     - Every `.obj` includes `v`, `vt`, and `vn` (`f v/vt/vn`) with valid relative `mtllib` and `map_Kd`.
     - Every `.glb`/`.gltf` includes the 12 named PBR `materials`, `POSITION`, `NORMAL`, `TEXCOORD_0`, and `COLOR_0`.
"""

import os
import sys
import json
import math
import struct
import hashlib
import shutil
from collections import OrderedDict
import numpy as np
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PKG_DIR = os.path.dirname(SCRIPT_DIR)
MESH_DIR = os.path.join(PKG_DIR, "meshes")
ARCH_DIR = os.path.join(MESH_DIR, "archetypes")
SECT_DIR = os.path.join(MESH_DIR, "sections")
TEX_DIR = os.path.join(PKG_DIR, "textures")

for d in (PKG_DIR, SCRIPT_DIR, MESH_DIR, ARCH_DIR, SECT_DIR, TEX_DIR):
    os.makedirs(d, exist_ok=True)

APPROVED_CONCEPT_02_ZIP_SHA256 = "78a010a3d194f4c2b4577265c4628d8266e7bc7323efa32a5082bae4934b85d4"

# ==============================================================================
# 1. LOCKED ARENA & COLOSSEUM SPATIAL CONSTANTS (1 unit = 1 Roblox stud)
# ==============================================================================
ARENA_CENTER = (0.0, 50.0, 0.0)
ARENA_TILE_TOP_Y = 51.0
ARENA_GRID_HALF_SPAN = 54.0
ARENA_CORNER_RADIUS = math.hypot(54.0, 54.0)  # 76.36753236814714 studs
VOID_ELIMINATION_Y = 15.0            # Canonical void threshold World Y < 15.0

RX_IN, RZ_IN = 98.0000, 104.0000
RX_OUT, RZ_OUT = 128.0000, 134.0000
N_BAYS = 48
D_THETA = (2.0 * math.pi) / float(N_BAYS)

# ==============================================================================
# 2. CANONICAL 12-MATERIAL PALETTE & 4x3 UV ATLAS LAYOUT (512x512 px)
# ==============================================================================
MATERIALS = OrderedDict([
    ("MAT_TravertineLight", {"rgb": (214, 198, 172), "hex": "#D6C6AC", "flag": 0, "roughness": 0.62, "metallic": 0.04, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "Limestone",     "cell": (0, 0), "role": "Principal outer arches, voussoirs, keystones, columns & pilasters"}),
    ("MAT_TravertineWarm",  {"rgb": (196, 178, 150), "hex": "#C4B296", "flag": 0, "roughness": 0.66, "metallic": 0.04, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "Limestone",     "cell": (1, 0), "role": "Ashlar pier blocks, spandrels, attic wall courses & entablature friezes"}),
    ("MAT_LimestoneCream",  {"rgb": (204, 192, 172), "hex": "#CCC0AC", "flag": 0, "roughness": 0.64, "metallic": 0.04, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "Limestone",     "cell": (2, 0), "role": "Tiered Cavea seating steps, bullnose treads, scalaria stairs & vomitoria arches"}),
    ("MAT_TuffFoundation",  {"rgb": (132, 122, 108), "hex": "#847A6C", "flag": 0, "roughness": 0.74, "metallic": 0.06, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "Slate",         "cell": (3, 0), "role": "Stepped crepidine base, lower foundation drum & recessed vaulted passages"}),
    ("MAT_BasaltShadow",    {"rgb": (58,  60,  68),  "hex": "#3A3C44", "flag": 0, "roughness": 0.76, "metallic": 0.10, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "Basalt",        "cell": (0, 1), "role": "Deep vomitoria throats, arena podium base & lower structural ribs"}),
    ("MAT_ImperialMarble",  {"rgb": (232, 224, 210), "hex": "#E8E0D2", "flag": 1, "roughness": 0.34, "metallic": 0.08, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "Marble",        "cell": (1, 1), "role": "Senatorial podium balustrade, Corinthian/Ionic capitals, pediments & keystones"}),
    ("MAT_BronzeClipeus",   {"rgb": (176, 142, 88),  "hex": "#B08E58", "flag": 1, "roughness": 0.36, "metallic": 0.72, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "Metal",         "cell": (2, 1), "role": "Attic clipei victory shields, velarium mast collars & triumphal medallions"}),
    ("MAT_DarkNeutral",     {"rgb": (32,  38,  54),  "hex": "#202636", "flag": 1, "roughness": 0.42, "metallic": 0.58, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "SmoothPlastic", "cell": (3, 1), "role": "Engineered dark-metal gate portcullis frames & structural tie collars"}),
    ("MAT_AltNeutral",      {"rgb": (42,  50,  70),  "hex": "#2A3246", "flag": 1, "roughness": 0.38, "metallic": 0.62, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "Metal",         "cell": (0, 2), "role": "Secondary engineered housing & reactor frame"}),
    ("MAT_LightTrim",       {"rgb": (170, 190, 215), "hex": "#AABED7", "flag": 1, "roughness": 0.28, "metallic": 0.78, "emissive": (0.0, 0.0, 0.0), "roblox_mat": "Metal",         "cell": (1, 2), "role": "Brushed metallic arch tie-cleats & reactor bezel trim"}),
    ("EMI_Cyan",            {"rgb": (0,   195, 255), "hex": "#00C3FF", "flag": 2, "roughness": 0.15, "metallic": 0.00, "emissive": (0.0, 0.76, 1.0), "roblox_mat": "Neon",          "cell": (2, 2), "role": "Restrained Kinetic Grid energy seams in gates & North Imperial Reactor Crest"}),
    ("EMI_Amber",           {"rgb": (255, 170, 0),   "hex": "#FFAA00", "flag": 2, "roughness": 0.15, "metallic": 0.00, "emissive": (1.0, 0.67, 0.0), "roblox_mat": "Neon",          "cell": (3, 2), "role": "Sparse landmark focal core in North Imperial Reactor Crest"}),
])
MAT_NAMES = list(MATERIALS.keys())
MAT_INDEX = {name: idx for idx, name in enumerate(MAT_NAMES)}


def get_material_uv_box(mat_name):
    cx, cy = MATERIALS[mat_name]["cell"]
    u0 = (cx * 128.0 + 16.0) / 512.0
    u1 = ((cx + 1) * 128.0 - 16.0) / 512.0
    v_top = 1.0 - (cy * (512.0 / 3.0) + 16.0) / 512.0
    v_bot = 1.0 - ((cy + 1) * (512.0 / 3.0) - 16.0) / 512.0
    return (u0, v_bot, u1, v_top)


def generate_production_atlas_512(out_path):
    """Generates a clean 512x512 stone, marble, bronze & emissive texture atlas (<= 1024x1024 limit)."""
    W, H = 512, 512
    img = np.zeros((H, W, 3), dtype=np.uint8)
    rng = np.random.default_rng(20261025)
    for mname, mprops in MATERIALS.items():
        cx, cy = mprops["cell"]
        x0, x1 = cx * 128, (cx + 1) * 128
        y0 = int(round(cy * 512.0 / 3.0))
        y1 = int(round((cy + 1) * 512.0 / 3.0))
        th = y1 - y0
        tw = x1 - x0
        base = np.array(mprops["rgb"], dtype=np.float32)
        tile = np.ones((th, tw, 3), dtype=np.float32) * base
        if mprops["flag"] == 0:
            yy, xx = np.mgrid[0:th, 0:tw]
            striation = np.sin(yy * 0.35 + np.sin(xx * 0.12) * 1.8) * 4.5
            noise = rng.normal(0.0, 3.2, size=(th, tw))
            tile = np.clip(tile + (striation + noise)[:, :, None], 0, 255)
        elif mprops["flag"] == 1:
            yy, xx = np.mgrid[0:th, 0:tw]
            sheen = np.cos(xx * 0.18 + yy * 0.08) * 2.2
            tile = np.clip(tile + sheen[:, :, None], 0, 255)
        img[y0:y1, x0:x1, :] = tile.astype(np.uint8)
    Image.fromarray(img, mode="RGB").save(out_path, format="PNG", optimize=False)
    return W, H


def ellipse_point_and_basis(r_x, r_z, theta):
    ct, st = math.cos(theta), math.sin(theta)
    px = r_x * ct
    pz = r_z * st
    gx = ct / r_x
    gz = st / r_z
    glen = math.hypot(gx, gz)
    nx, nz = gx / glen, gz / glen
    tx, tz = -nz, nx
    return px, pz, nx, nz, tx, tz


def clamp_val(x, a, b):
    return a if x < a else (b if x > b else x)


def compute_tri_uvs(p0, p1, p2, nrm, mat_name):
    u0, v0, u1, v1 = get_material_uv_box(mat_name)
    du = u1 - u0
    dv = v1 - v0
    ax, ay, az = abs(nrm[0]), abs(nrm[1]), abs(nrm[2])
    uvs = []
    for p in (p0, p1, p2):
        if ay >= ax and ay >= az:
            su, sv = p[0] * 0.08, p[2] * 0.08
        elif ax >= az:
            su, sv = p[2] * 0.08, p[1] * 0.08
        else:
            su, sv = p[0] * 0.08, p[1] * 0.08
        fu = (su - math.floor(su)) * 0.90 + 0.05
        fv = (sv - math.floor(sv)) * 0.90 + 0.05
        uvs.append((round(u0 + fu * du, 5), round(v0 + fv * dv, 5)))
    return uvs[0], uvs[1], uvs[2]


# ==============================================================================
# 3. HIGH-DETAIL COLOSSEUM PRODUCTION BUILDER
# ==============================================================================
class HighDetailColosseumBuilder:
    def __init__(self):
        self.groups = [
            "COL_ExteriorArcade",
            "COL_ColumnOrders",
            "COL_StoneMasonry",
            "COL_CaveaSeating",
            "COL_Vomitoria",
            "COL_AtticCornice",
            "COL_GateTowers",
            "COL_NorthReactorCrest",
        ]
        self.tris = []
        self._block_seed = 1
        self.current_bay = 0

    def next_bvar(self):
        self._block_seed = (self._block_seed * 1103515245 + 12345) & 0x7FFFFFFF
        return ((self._block_seed % 1000) / 500.0) - 1.0

    def add_tri(self, group, mat_name, v0, v1, v2, expected_dir=None, bvar=0.0):
        x0, y0, z0 = float(v0[0]), float(v0[1]), float(v0[2])
        x1, y1, z1 = float(v1[0]), float(v1[1]), float(v1[2])
        x2, y2, z2 = float(v2[0]), float(v2[1]), float(v2[2])
        ux, uy, uz = x1 - x0, y1 - y0, z1 - z0
        vx, vy, vz = x2 - x0, y2 - y0, z2 - z0
        cx = uy * vz - uz * vy
        cy = uz * vx - ux * vz
        cz = ux * vy - uy * vx
        nlen = math.sqrt(cx * cx + cy * cy + cz * cz)
        if nlen < 1e-6:
            return
        if expected_dir is not None:
            dot = cx * expected_dir[0] + cy * expected_dir[1] + cz * expected_dir[2]
            if dot < 0.0:
                x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
                cx, cy, cz = -cx, -cy, -cz
        inv_n = 1.0 / nlen
        nrm = (round(cx * inv_n, 5), round(cy * inv_n, 5), round(cz * inv_n, 5))
        p0 = (round(x0, 4), round(y0, 4), round(z0, 4))
        p1 = (round(x1, 4), round(y1, 4), round(z1, 4))
        p2 = (round(x2, 4), round(y2, 4), round(z2, 4))
        uv0, uv1, uv2 = compute_tri_uvs(p0, p1, p2, nrm, mat_name)
        self.tris.append({
            "v0": p0, "v1": p1, "v2": p2,
            "nrm": nrm,
            "uv0": uv0, "uv1": uv1, "uv2": uv2,
            "mat": mat_name,
            "group": group,
            "bay": self.current_bay,
            "bvar": float(bvar),
        })

    def add_quad(self, group, mat_name, v0, v1, v2, v3, expected_dir=None, bvar=0.0):
        self.add_tri(group, mat_name, v0, v1, v2, expected_dir, bvar)
        self.add_tri(group, mat_name, v0, v2, v3, expected_dir, bvar)

    def add_loft(self, group, mat_name, loop_b, loop_t, cap_bot=True, cap_top=True, bvar=None):
        if bvar is None:
            bvar = self.next_bvar()
        n = len(loop_b)
        cb_x = sum(p[0] for p in loop_b) / n
        cb_y = sum(p[1] for p in loop_b) / n
        cb_z = sum(p[2] for p in loop_b) / n
        ct_x = sum(p[0] for p in loop_t) / n
        ct_y = sum(p[1] for p in loop_t) / n
        ct_z = sum(p[2] for p in loop_t) / n
        cm_x, cm_y, cm_z = 0.5 * (cb_x + ct_x), 0.5 * (cb_y + ct_y), 0.5 * (cb_z + ct_z)

        for i in range(n):
            j = (i + 1) % n
            b0, b1 = loop_b[i], loop_b[j]
            t0, t1 = loop_t[i], loop_t[j]
            mx = 0.25 * (b0[0] + b1[0] + t0[0] + t1[0]) - cm_x
            my = (0.25 * (b0[1] + b1[1] + t0[1] + t1[1]) - cm_y) * 0.25
            mz = 0.25 * (b0[2] + b1[2] + t0[2] + t1[2]) - cm_z
            self.add_quad(group, mat_name, b0, b1, t1, t0, (mx, my, mz), bvar)

        ax_x, ax_y, ax_z = ct_x - cb_x, ct_y - cb_y, ct_z - cb_z
        if abs(ax_x) + abs(ax_y) + abs(ax_z) < 1e-5:
            ax_x, ax_y, ax_z = 0.0, 1.0, 0.0
        if cap_top:
            for i in range(1, n - 1):
                self.add_tri(group, mat_name, loop_t[0], loop_t[i], loop_t[i + 1], (ax_x, ax_y, ax_z), bvar)
        if cap_bot:
            for i in range(1, n - 1):
                self.add_tri(group, mat_name, loop_b[0], loop_b[i + 1], loop_b[i], (-ax_x, -ax_y, -ax_z), bvar)

    def add_local_box(self, group, mat_name, origin_xz, nx, nz, tx, tz, r0, r1, t0, t1, y0, y1, chamfer=0.0, cap_bot=False, cap_top=True, bvar=None):
        if bvar is None:
            bvar = self.next_bvar()
        ox, oz = origin_xz
        if chamfer > 1e-4:
            cr = min(chamfer, 0.35 * (r1 - r0))
            ct = min(chamfer, 0.35 * (t1 - t0))
            cy = min(chamfer, 0.35 * (y1 - y0))
            pts_2d_outer = [(r0, t0), (r1, t0), (r1, t1), (r0, t1)]
            pts_2d_inner = [(r0 + cr, t0 + ct), (r1 - cr, t0 + ct), (r1 - cr, t1 - ct), (r0 + cr, t1 - ct)]
            lb_in = [(ox + r * nx + t * tx, y0, oz + r * nz + t * tz) for r, t in pts_2d_inner]
            lb_md = [(ox + r * nx + t * tx, y0 + cy, oz + r * nz + t * tz) for r, t in pts_2d_outer]
            lt_md = [(ox + r * nx + t * tx, y1 - cy, oz + r * nz + t * tz) for r, t in pts_2d_outer]
            lt_in = [(ox + r * nx + t * tx, y1, oz + r * nz + t * tz) for r, t in pts_2d_inner]
            self.add_loft(group, mat_name, lb_in, lb_md, cap_bot=cap_bot, cap_top=False, bvar=bvar)
            self.add_loft(group, mat_name, lb_md, lt_md, cap_bot=False, cap_top=False, bvar=bvar)
            self.add_loft(group, mat_name, lt_md, lt_in, cap_bot=False, cap_top=cap_top, bvar=bvar)
        else:
            pts_2d = [(r0, t0), (r1, t0), (r1, t1), (r0, t1)]
            lb = [(ox + r * nx + t * tx, y0, oz + r * nz + t * tz) for r, t in pts_2d]
            lt = [(ox + r * nx + t * tx, y1, oz + r * nz + t * tz) for r, t in pts_2d]
            self.add_loft(group, mat_name, lb, lt, cap_bot=cap_bot, cap_top=cap_top, bvar=bvar)

    def add_elliptical_arc_band(self, group, mat_name, rx_in_b, rz_in_b, rx_out_b, rz_out_b, rx_in_t, rz_in_t, rx_out_t, rz_out_t, y_bot, y_top, a0, a1, n_sub=2, cap_bot=False, cap_top=True, bvar=None):
        if bvar is None:
            bvar = self.next_bvar()
        da = (a1 - a0) / float(n_sub)
        for k in range(n_sub):
            t0 = a0 + k * da
            t1 = t0 + da
            c0, s0 = math.cos(t0), math.sin(t0)
            c1, s1 = math.cos(t1), math.sin(t1)
            lb = [
                (rx_in_b * c0,  y_bot, rz_in_b * s0),
                (rx_out_b * c0, y_bot, rz_out_b * s0),
                (rx_out_b * c1, y_bot, rz_out_b * s1),
                (rx_in_b * c1,  y_bot, rz_in_b * s1),
            ]
            lt = [
                (rx_in_t * c0,  y_top, rz_in_t * s0),
                (rx_out_t * c0, y_top, rz_out_t * s0),
                (rx_out_t * c1, y_top, rz_out_t * s1),
                (rx_in_t * c1,  y_top, rz_in_t * s1),
            ]
            self.add_loft(group, mat_name, lb, lt, cap_bot=cap_bot, cap_top=cap_top, bvar=bvar)

    def add_true_3d_arch_with_voussoirs(
        self, group_arch, group_masonry, origin_xz, nx, nz, tx, tz,
        r_back, r_front, bay_half_w, arch_half_w, y_floor, y_impost, y_top_wall,
        n_voussoirs=9, keystone_extra_h=0.45, has_medallions=False
    ):
        # 1. Left & Right Coursed Ashlar Piers (with bevelled ashlar relief courses)
        n_pier_courses = 4
        ch = (y_impost - y_floor) / float(n_pier_courses)
        for side_s in (-1.0, +1.0):
            t_outer = side_s * bay_half_w
            t_inner = side_s * arch_half_w
            t_min, t_max = min(t_outer, t_inner), max(t_outer, t_inner)
            for c_i in range(n_pier_courses):
                cy0 = y_floor + c_i * ch + 0.04
                cy1 = y_floor + (c_i + 1) * ch - 0.04
                if c_i % 2 == 1 and (t_max - t_min) > 1.2:
                    t_mid = 0.5 * (t_min + t_max)
                    self.add_local_box(group_masonry, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                                       r_back, r_front, t_min + 0.03, t_mid - 0.03, cy0, cy1, chamfer=0.04)
                    self.add_local_box(group_masonry, "MAT_TravertineLight", origin_xz, nx, nz, tx, tz,
                                       r_back, r_front, t_mid + 0.03, t_max - 0.03, cy0, cy1, chamfer=0.04)
                else:
                    self.add_local_box(group_masonry, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                                       r_back, r_front, t_min + 0.03, t_max - 0.03, cy0, cy1, chamfer=0.04)

            # 2. Projecting 2-Step Moulded Impost Capital Block at y_impost
            self.add_local_box(group_arch, "MAT_TravertineLight", origin_xz, nx, nz, tx, tz,
                               r_back - 0.12, r_front + 0.16, t_min - 0.10, t_max + 0.14, y_impost - 0.35, y_impost - 0.15)
            self.add_local_box(group_arch, "MAT_ImperialMarble", origin_xz, nx, nz, tx, tz,
                               r_back - 0.20, r_front + 0.26, t_min - 0.16, t_max + 0.22, y_impost - 0.15, y_impost + 0.12)

        # 3. Individually Modelled 3D Wedge Voussoirs, Dual Archivolts, Vaulted Soffit & Spandrel Masonry
        r_intrados = arch_half_w
        r_archivolt_mid = arch_half_w + 0.42
        r_extrados = arch_half_w + 0.92
        d_phi = math.pi / float(n_voussoirs)
        ox, oz = origin_xz

        for v_i in range(n_voussoirs):
            phi0 = v_i * d_phi + 0.012
            phi1 = (v_i + 1) * d_phi - 0.012
            is_keystone = (v_i == n_voussoirs // 2)

            c0, s0 = math.cos(phi0), math.sin(phi0)
            c1, s1 = math.cos(phi1), math.sin(phi1)

            t_in0, y_in0 = r_intrados * c0, y_impost + r_intrados * s0
            t_in1, y_in1 = r_intrados * c1, y_impost + r_intrados * s1
            t_md0, y_md0 = r_archivolt_mid * c0, y_impost + r_archivolt_mid * s0
            t_md1, y_md1 = r_archivolt_mid * c1, y_impost + r_archivolt_mid * s1

            r_ext_cur = (r_extrados + keystone_extra_h) if is_keystone else r_extrados
            t_ex0, y_ex0 = r_ext_cur * c0, y_impost + r_ext_cur * s0
            t_ex1, y_ex1 = r_ext_cur * c1, y_impost + r_ext_cur * s1

            rf_in = r_front + 0.10
            rf_out = (r_front + 0.42) if is_keystone else (r_front + 0.22)
            rb_in = r_back - 0.08
            v_mat = "MAT_ImperialMarble" if is_keystone else "MAT_TravertineLight"
            bv = self.next_bvar()

            lb_arch1 = [
                (ox + rb_in * nx + t_in0 * tx, y_in0, oz + rb_in * nz + t_in0 * tz),
                (ox + rf_in * nx + t_in0 * tx, y_in0, oz + rf_in * nz + t_in0 * tz),
                (ox + rf_in * nx + t_in1 * tx, y_in1, oz + rf_in * nz + t_in1 * tz),
                (ox + rb_in * nx + t_in1 * tx, y_in1, oz + rb_in * nz + t_in1 * tz),
            ]
            lt_arch1 = [
                (ox + rb_in * nx + t_md0 * tx, y_md0, oz + rb_in * nz + t_md0 * tz),
                (ox + rf_in * nx + t_md0 * tx, y_md0, oz + rf_in * nz + t_md0 * tz),
                (ox + rf_in * nx + t_md1 * tx, y_md1, oz + rf_in * nz + t_md1 * tz),
                (ox + rb_in * nx + t_md1 * tx, y_md1, oz + rb_in * nz + t_md1 * tz),
            ]
            self.add_loft(group_arch, "MAT_TravertineLight", lb_arch1, lt_arch1, cap_bot=True, cap_top=True, bvar=bv)

            lb_vous = [
                (ox + (rb_in - 0.06) * nx + t_md0 * tx, y_md0, oz + (rb_in - 0.06) * nz + t_md0 * tz),
                (ox + rf_out * nx + t_md0 * tx, y_md0, oz + rf_out * nz + t_md0 * tz),
                (ox + rf_out * nx + t_md1 * tx, y_md1, oz + rf_out * nz + t_md1 * tz),
                (ox + (rb_in - 0.06) * nx + t_md1 * tx, y_md1, oz + (rb_in - 0.06) * nz + t_md1 * tz),
            ]
            lt_vous = [
                (ox + (rb_in - 0.06) * nx + t_ex0 * tx, y_ex0, oz + (rb_in - 0.06) * nz + t_ex0 * tz),
                (ox + rf_out * nx + t_ex0 * tx, y_ex0, oz + rf_out * nz + t_ex0 * tz),
                (ox + rf_out * nx + t_ex1 * tx, y_ex1, oz + rf_out * nz + t_ex1 * tz),
                (ox + (rb_in - 0.06) * nx + t_ex1 * tx, y_ex1, oz + (rb_in - 0.06) * nz + t_ex1 * tz),
            ]
            self.add_loft(group_arch, v_mat, lb_vous, lt_vous, cap_bot=True, cap_top=True, bvar=bv)

            t_sp0 = clamp_val(t_ex0, -bay_half_w + 0.04, bay_half_w - 0.04)
            t_sp1 = clamp_val(t_ex1, -bay_half_w + 0.04, bay_half_w - 0.04)
            y_sp0 = min(y_ex0 + 0.04, y_top_wall - 0.15)
            y_sp1 = min(y_ex1 + 0.04, y_top_wall - 0.15)
            if abs(t_sp1 - t_sp0) > 0.08:
                lb_sp = [
                    (ox + r_back * nx + t_sp0 * tx, y_sp0, oz + r_back * nz + t_sp0 * tz),
                    (ox + r_front * nx + t_sp0 * tx, y_sp0, oz + r_front * nz + t_sp0 * tz),
                    (ox + r_front * nx + t_sp1 * tx, y_sp1, oz + r_front * nz + t_sp1 * tz),
                    (ox + r_back * nx + t_sp1 * tx, y_sp1, oz + r_back * nz + t_sp1 * tz),
                ]
                lt_sp = [
                    (ox + r_back * nx + t_sp0 * tx, y_top_wall, oz + r_back * nz + t_sp0 * tz),
                    (ox + r_front * nx + t_sp0 * tx, y_top_wall, oz + r_front * nz + t_sp0 * tz),
                    (ox + r_front * nx + t_sp1 * tx, y_top_wall, oz + r_front * nz + t_sp1 * tz),
                    (ox + r_back * nx + t_sp1 * tx, y_top_wall, oz + r_back * nz + t_sp1 * tz),
                ]
                self.add_loft(group_masonry, "MAT_TravertineWarm", lb_sp, lt_sp, cap_bot=False, cap_top=True)

        for side_s in (-1.0, +1.0):
            t_outer = side_s * (bay_half_w - 0.04)
            t_inner = side_s * min(r_extrados - 0.05, bay_half_w - 0.15)
            t_min, t_max = min(t_outer, t_inner), max(t_outer, t_inner)
            if (t_max - t_min) > 0.12:
                ymid = 0.5 * (y_impost + y_top_wall)
                self.add_local_box(group_masonry, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                                   r_back, r_front, t_min, t_max, y_impost + 0.12, ymid - 0.03, chamfer=0.04)
                self.add_local_box(group_masonry, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                                   r_back, r_front, t_min, t_max, ymid + 0.03, y_top_wall, chamfer=0.04)
            if has_medallions:
                tm_c = side_s * (bay_half_w * 0.72)
                ym_c = y_top_wall - 1.35
                self.add_local_box(group_arch, "MAT_BronzeClipeus", origin_xz, nx, nz, tx, tz,
                                   r_front - 0.05, r_front + 0.22, tm_c - 0.42, tm_c + 0.42, ym_c - 0.42, ym_c + 0.42, chamfer=0.14)

    def add_classical_column(
        self, group, col_xz, nx, nz, tx, tz, y_base, y_top, order="Tuscan", radius=0.82
    ):
        """
        Phase 2 Refined Classical Column (Section 4.1):
          - Stepped pedestal + Attic/Tuscan moulded base (plinth, lower torus, scotia, upper torus)
          - Cylindrical shaft with entasis & 3D recessed flutes (for Ionic/Corinthian)
          - Refined Order-Specific 3D Capitals:
              * Tuscan: Turned astragal ring, hypotrachelium neck, 3-ring curved echinus ovolo torus, throat fillet, and 2-step cyma abacus
              * Ionic: Carved echinus cushion, channel bridge, contoured bolster drums with waist cinch, and true multi-turn coiled 3D involute spiral volute ribbons + bronze oculus eye
              * Corinthian: Tapered inner calathus bell, 2 staggered rings of 8 contoured 3D overhanging acanthus leaves (16 multi-segment leaves with raised central midribs and recurved tips), 4 corner caulicoli volute helices, 2-step concave abacus, and central bronze fleuron
        """
        cx, cz = col_xz
        ped_h = 1.25
        self.add_local_box(group, "MAT_TravertineWarm", col_xz, nx, nz, tx, tz,
                           -radius * 1.35, radius * 1.35, -radius * 1.35, radius * 1.35, y_base, y_base + 0.32)
        self.add_local_box(group, "MAT_TravertineLight", col_xz, nx, nz, tx, tz,
                           -radius * 1.18, radius * 1.18, -radius * 1.18, radius * 1.18, y_base + 0.32, y_base + ped_h - 0.18)
        self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                           -radius * 1.28, radius * 1.28, -radius * 1.28, radius * 1.28, y_base + ped_h - 0.18, y_base + ped_h)

        # Attic / Tuscan Base Rings (plinth + lower torus + scotia + upper torus)
        yb0 = y_base + ped_h
        n_seg = 10
        ring_profiles = [
            (yb0,        yb0 + 0.22, radius * 1.24, radius * 1.18, "MAT_ImperialMarble"),
            (yb0 + 0.22, yb0 + 0.40, radius * 1.06, radius * 1.02, "MAT_ImperialMarble"),
            (yb0 + 0.40, yb0 + 0.56, radius * 1.14, radius * 1.00, "MAT_TravertineLight"),
        ]
        for ry0, ry1, r_b, r_t, rmat in ring_profiles:
            lb, lt = [], []
            for k in range(n_seg):
                ang = k * (2.0 * math.pi / n_seg)
                ca, sa = math.cos(ang), math.sin(ang)
                lb.append((cx + r_b * (ca * nx + sa * tx), ry0, cz + r_b * (ca * nz + sa * tz)))
                lt.append((cx + r_t * (ca * nx + sa * tx), ry1, cz + r_t * (ca * nz + sa * tz)))
            self.add_loft(group, rmat, lb, lt, cap_bot=False, cap_top=True)

        # 2. Column Shaft with Entasis & 3D Fluting (2 vertical shaft tiers for genuine entasis curve)
        y_shaft_bot = yb0 + 0.56
        cap_h = 2.05 if order == "Corinthian" else (1.55 if order == "Ionic" else 1.35)
        y_shaft_top = y_top - cap_h
        n_shaft_tiers = 2
        fluted = (order in ("Ionic", "Corinthian"))
        n_circ = 16 if fluted else 12

        for st_i in range(n_shaft_tiers):
            f0 = st_i / float(n_shaft_tiers)
            f1 = (st_i + 1) / float(n_shaft_tiers)
            sy0 = y_shaft_bot + f0 * (y_shaft_top - y_shaft_bot)
            sy1 = y_shaft_bot + f1 * (y_shaft_top - y_shaft_bot)
            r0 = radius * (1.0 - 0.14 * (f0 ** 1.4) + 0.03 * math.sin(f0 * math.pi))
            r1 = radius * (1.0 - 0.14 * (f1 ** 1.4) + 0.03 * math.sin(f1 * math.pi))
            lb, lt = [], []
            for k in range(n_circ):
                ang = k * (2.0 * math.pi / n_circ)
                ca, sa = math.cos(ang), math.sin(ang)
                flute_mult = (0.90 if (fluted and (k % 2 == 1)) else 1.0)
                rr0 = r0 * flute_mult
                rr1 = r1 * flute_mult
                lb.append((cx + rr0 * (ca * nx + sa * tx), sy0, cz + rr0 * (ca * nz + sa * tz)))
                lt.append((cx + rr1 * (ca * nx + sa * tx), sy1, cz + rr1 * (ca * nz + sa * tz)))
            self.add_loft(group, "MAT_TravertineLight", lb, lt, cap_bot=False, cap_top=False)

        # Turned Astragal Necking Ring at y_shaft_top
        r_neck = radius * 0.86
        lb_n, lt_n = [], []
        for k in range(12):
            ang = k * (2.0 * math.pi / 12.0)
            ca, sa = math.cos(ang), math.sin(ang)
            lb_n.append((cx + r_neck * 1.10 * (ca * nx + sa * tx), y_shaft_top, cz + r_neck * 1.10 * (ca * nz + sa * tz)))
            lt_n.append((cx + r_neck * 1.10 * (ca * nx + sa * tx), y_shaft_top + 0.16, cz + r_neck * 1.10 * (ca * nz + sa * tz)))
        self.add_loft(group, "MAT_ImperialMarble", lb_n, lt_n, cap_bot=True, cap_top=True)

        # 3. Refined Order-Specific 3D Capitals (Section 4.1)
        yc0 = y_shaft_top + 0.16
        if order == "Tuscan":
            # Coherent Hypotrachelium Neck + 3-Ring Curved Echinus Torus Cushion + Throat Fillet + 2-Step Cyma Abacus
            t_rings = [
                (yc0,        r_neck * 0.96),
                (yc0 + 0.16, r_neck * 0.98),  # Hypotrachelium neck
                (yc0 + 0.34, radius * 1.12),  # Echinus lower curve
                (yc0 + 0.54, radius * 1.26),  # Echinus upper ovolo crown
                (yc0 + 0.64, radius * 1.22),  # Throat fillet
            ]
            t_loops = []
            for yr, rr in t_rings:
                lp = []
                for k in range(12):
                    ang = k * (2.0 * math.pi / 12.0)
                    ca, sa = math.cos(ang), math.sin(ang)
                    lp.append((cx + rr * (ca * nx + sa * tx), yr, cz + rr * (ca * nz + sa * tz)))
                t_loops.append(lp)
            for i in range(len(t_loops) - 1):
                self.add_loft(group, "MAT_ImperialMarble", t_loops[i], t_loops[i + 1], cap_bot=False, cap_top=(i == len(t_loops) - 2))
            # Two-stepped square Abacus with Cymatium crown moulding
            self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                               -radius * 1.28, radius * 1.28, -radius * 1.28, radius * 1.28, yc0 + 0.64, y_top - 0.14)
            self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                               -radius * 1.36, radius * 1.36, -radius * 1.36, radius * 1.36, y_top - 0.14, y_top)

        elif order == "Ionic":
            # Carved Echinus Cushion + Canalis Bridge + Contoured Bolsters + True Coiled 3D Spiral Volute Scrolls
            ion_rings = [
                (yc0,        r_neck * 0.96),
                (yc0 + 0.28, radius * 1.18),
                (yc0 + 0.52, radius * 1.10),
            ]
            i_loops = []
            for yr, rr in ion_rings:
                lp = []
                for k in range(12):
                    ang = k * (2.0 * math.pi / 12.0)
                    ca, sa = math.cos(ang), math.sin(ang)
                    lp.append((cx + rr * (ca * nx + sa * tx), yr, cz + rr * (ca * nz + sa * tz)))
                i_loops.append(lp)
            for i in range(len(i_loops) - 1):
                self.add_loft(group, "MAT_ImperialMarble", i_loops[i], i_loops[i + 1], cap_bot=False, cap_top=(i == len(i_loops) - 2))

            # Canalis volute channel bridge & profiled Abacus above
            self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                               -radius * 1.02, radius * 1.02, -radius * 1.28, radius * 1.28, yc0 + 0.44, yc0 + 0.84)
            self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                               -radius * 1.18, radius * 1.18, -radius * 1.22, radius * 1.22, yc0 + 0.84, y_top)

            # Twin Coiled 3D Involute Spiral Volutes at left (-t) and right (+t)
            vy_c = yc0 + 0.48
            vr_scroll = radius * 0.50
            for vs in (-1.0, +1.0):
                vt_c = vs * radius * 1.14
                # Contoured 12-sided bolster drum with central waist cinch
                b_rings = [
                    (-radius * 1.06, vr_scroll * 1.00),
                    (0.0,            vr_scroll * 0.86),
                    (+radius * 1.06, vr_scroll * 1.00),
                ]
                b_loops = []
                for r_off, br in b_rings:
                    lp = []
                    for k in range(12):
                        ang = k * (2.0 * math.pi / 12.0)
                        dt_v = vt_c + br * math.cos(ang)
                        dy_v = vy_c + br * math.sin(ang)
                        lp.append((cx + r_off * nx + dt_v * tx, dy_v, cz + r_off * nz + dt_v * tz))
                    b_loops.append(lp)
                self.add_loft(group, "MAT_ImperialMarble", b_loops[0], b_loops[1], cap_bot=True, cap_top=False)
                self.add_loft(group, "MAT_ImperialMarble", b_loops[1], b_loops[2], cap_bot=False, cap_top=True)

                # Coiled 3D Involute Spiral Ribbon on front (+nx) and back (-nx) faces (10 spiral segments winding 1.75 turns)
                for face_s in (+1.0, -1.0):
                    r_f0 = face_s * (radius * 1.05)
                    r_f1 = face_s * (radius * 1.20)
                    n_sp = 10
                    for sp_i in range(n_sp):
                        f0 = sp_i / float(n_sp)
                        f1 = (sp_i + 1) / float(n_sp)
                        a0 = f0 * 3.5 * math.pi
                        a1 = f1 * 3.5 * math.pi
                        rad0_out = vr_scroll * (1.04 - 0.72 * f0)
                        rad0_in  = rad0_out * 0.72
                        rad1_out = vr_scroll * (1.04 - 0.72 * f1)
                        rad1_in  = rad1_out * 0.72

                        t0_out = vt_c + vs * rad0_out * math.cos(a0)
                        y0_out = vy_c + rad0_out * math.sin(a0)
                        t0_in  = vt_c + vs * rad0_in * math.cos(a0)
                        y0_in  = vy_c + rad0_in * math.sin(a0)

                        t1_out = vt_c + vs * rad1_out * math.cos(a1)
                        y1_out = vy_c + rad1_out * math.sin(a1)
                        t1_in  = vt_c + vs * rad1_in * math.cos(a1)
                        y1_in  = vy_c + rad1_in * math.sin(a1)

                        lp_sp0 = [
                            (cx + r_f0 * nx + t0_in * tx,  y0_in,  cz + r_f0 * nz + t0_in * tz),
                            (cx + r_f0 * nx + t0_out * tx, y0_out, cz + r_f0 * nz + t0_out * tz),
                            (cx + r_f1 * nx + t0_out * tx, y0_out, cz + r_f1 * nz + t0_out * tz),
                            (cx + r_f1 * nx + t0_in * tx,  y0_in,  cz + r_f1 * nz + t0_in * tz),
                        ]
                        lp_sp1 = [
                            (cx + r_f0 * nx + t1_in * tx,  y1_in,  cz + r_f0 * nz + t1_in * tz),
                            (cx + r_f0 * nx + t1_out * tx, y1_out, cz + r_f0 * nz + t1_out * tz),
                            (cx + r_f1 * nx + t1_out * tx, y1_out, cz + r_f1 * nz + t1_out * tz),
                            (cx + r_f1 * nx + t1_in * tx,  y1_in,  cz + r_f1 * nz + t1_in * tz),
                        ]
                        self.add_loft(group, "MAT_ImperialMarble", lp_sp0, lp_sp1, cap_bot=False, cap_top=False)

                # Bronze spiral oculus eye boss on front & back
                self.add_local_box(group, "MAT_BronzeClipeus", col_xz, nx, nz, tx, tz,
                                   -radius * 1.24, radius * 1.24, vt_c - 0.14, vt_c + 0.14, vy_c - 0.14, vy_c + 0.14)

        else:  # Corinthian
            # Inner Tapered Calathus Bell Core
            bell_top = y_top - 0.36
            lb_b, lt_b = [], []
            for k in range(12):
                ang = k * (2.0 * math.pi / 12.0)
                ca, sa = math.cos(ang), math.sin(ang)
                lb_b.append((cx + r_neck * 0.94 * (ca * nx + sa * tx), yc0, cz + r_neck * 0.94 * (ca * nz + sa * tz)))
                lt_b.append((cx + radius * 1.14 * (ca * nx + sa * tx), bell_top, cz + radius * 1.14 * (ca * nz + sa * tz)))
            self.add_loft(group, "MAT_TravertineLight", lb_b, lt_b, cap_bot=False, cap_top=True)

            # Two Staggered Rings of 8 Contoured 3D Overhanging Acanthus Leaves (16 multi-segment leaves per capital!)
            for tier_i in range(2):
                ly0 = yc0 + tier_i * 0.56
                ly_mid = ly0 + 0.34
                ly1 = ly0 + 0.66
                r_leaf_b = r_neck * (0.98 + 0.08 * tier_i)
                r_leaf_m = radius * (1.14 + 0.10 * tier_i)
                r_leaf_t = radius * (1.28 + 0.14 * tier_i)
                ang_offset = (math.pi / 8.0) * tier_i
                for lf_i in range(8):
                    a_mid = ang_offset + lf_i * (2.0 * math.pi / 8.0)
                    da = 0.17
                    ca0, sa0 = math.cos(a_mid - da), math.sin(a_mid - da)
                    ca1, sa1 = math.cos(a_mid + da), math.sin(a_mid + da)
                    cam, sam = math.cos(a_mid), math.sin(a_mid)
                    # 4-vertex diamond cross-section per leaf (inner backing + left lobe + raised central midrib + right lobe)
                    lb_lf = [
                        (cx + (r_leaf_b - 0.04) * (cam * nx + sam * tx), ly0, cz + (r_leaf_b - 0.04) * (cam * nz + sam * tz)),
                        (cx + r_leaf_b * (ca0 * nx + sa0 * tx),          ly0, cz + r_leaf_b * (ca0 * nz + sa0 * tz)),
                        (cx + (r_leaf_b + 0.14) * (cam * nx + sam * tx), ly0, cz + (r_leaf_b + 0.14) * (cam * nz + sam * tz)),
                        (cx + r_leaf_b * (ca1 * nx + sa1 * tx),          ly0, cz + r_leaf_b * (ca1 * nz + sa1 * tz)),
                    ]
                    lm_lf = [
                        (cx + (r_leaf_m - 0.05) * (cam * nx + sam * tx), ly_mid, cz + (r_leaf_m - 0.05) * (cam * nz + sam * tz)),
                        (cx + r_leaf_m * (ca0 * nx + sa0 * tx),          ly_mid, cz + r_leaf_m * (ca0 * nz + sa0 * tz)),
                        (cx + (r_leaf_m + 0.18) * (cam * nx + sam * tx), ly_mid, cz + (r_leaf_m + 0.18) * (cam * nz + sam * tz)),
                        (cx + r_leaf_m * (ca1 * nx + sa1 * tx),          ly_mid, cz + r_leaf_m * (ca1 * nz + sa1 * tz)),
                    ]
                    # Overhanging recurved leaf tip
                    lt_lf = [
                        (cx + (r_leaf_t - 0.12) * (cam * nx + sam * tx), ly1,        cz + (r_leaf_t - 0.12) * (cam * nz + sam * tz)),
                        (cx + (r_leaf_t - 0.06) * (ca0 * nx + sa0 * tx), ly1 - 0.03, cz + (r_leaf_t - 0.06) * (ca0 * nz + sa0 * tz)),
                        (cx + (r_leaf_t + 0.20) * (cam * nx + sam * tx), ly1 - 0.08, cz + (r_leaf_t + 0.20) * (cam * nz + sam * tz)),
                        (cx + (r_leaf_t - 0.06) * (ca1 * nx + sa1 * tx), ly1 - 0.03, cz + (r_leaf_t - 0.06) * (ca1 * nz + sa1 * tz)),
                    ]
                    self.add_loft(group, "MAT_ImperialMarble", lb_lf, lm_lf, cap_bot=False, cap_top=False)
                    self.add_loft(group, "MAT_ImperialMarble", lm_lf, lt_lf, cap_bot=False, cap_top=True)

            # 4 Diagonal Corner Caulicoli Volute Scrolls supporting the Abacus horns
            for c_ang in (0.25 * math.pi, 0.75 * math.pi, 1.25 * math.pi, 1.75 * math.pi):
                cnx = math.cos(c_ang) * nx + math.sin(c_ang) * tx
                cnz = math.cos(c_ang) * nz + math.sin(c_ang) * tz
                ctx = -math.sin(c_ang) * nx + math.cos(c_ang) * tx
                ctz = -math.sin(c_ang) * nz + math.cos(c_ang) * tz
                self.add_local_box(
                    group, "MAT_ImperialMarble", col_xz, cnx, cnz, ctx, ctz,
                    radius * 0.95, radius * 1.48, -radius * 0.16, radius * 0.16,
                    bell_top - 0.26, bell_top + 0.04
                )

            # Two-Step Concave-Profiled Abacus + Central Bronze Fleuron Boss
            self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                               -radius * 1.32, radius * 1.32, -radius * 1.32, radius * 1.32, bell_top, y_top - 0.14)
            self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                               -radius * 1.40, radius * 1.40, -radius * 1.40, radius * 1.40, y_top - 0.14, y_top)
            self.add_local_box(group, "MAT_BronzeClipeus", col_xz, nx, nz, tx, tz,
                               radius * 1.26, radius * 1.46, -0.22, 0.22, bell_top + 0.04, y_top - 0.04)

    def add_entablature_and_cornice_bay(
        self, group, origin_xz, nx, nz, tx, tz, r_back, r_front, bay_half_w, y0, y1, n_dentils=6
    ):
        h = y1 - y0
        self.add_local_box(group, "MAT_TravertineLight", origin_xz, nx, nz, tx, tz,
                           r_back, r_front + 0.25, -bay_half_w, bay_half_w, y0, y0 + 0.24 * h)
        self.add_local_box(group, "MAT_ImperialMarble", origin_xz, nx, nz, tx, tz,
                           r_back, r_front + 0.36, -bay_half_w, bay_half_w, y0 + 0.24 * h, y0 + 0.38 * h)
        self.add_local_box(group, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                           r_back, r_front + 0.22, -bay_half_w, bay_half_w, y0 + 0.38 * h, y0 + 0.66 * h)
        dw = (2.0 * bay_half_w) / float(n_dentils)
        for d_i in range(n_dentils):
            dt0 = -bay_half_w + (d_i + 0.18) * dw
            dt1 = -bay_half_w + (d_i + 0.82) * dw
            self.add_local_box(group, "MAT_ImperialMarble", origin_xz, nx, nz, tx, tz,
                               r_front + 0.18, r_front + 0.52, dt0, dt1, y0 + 0.66 * h, y0 + 0.80 * h)
        self.add_local_box(group, "MAT_TravertineLight", origin_xz, nx, nz, tx, tz,
                           r_back - 0.15, r_front + 0.78, -bay_half_w - 0.04, bay_half_w + 0.04, y0 + 0.80 * h, y0 + 0.92 * h)
        self.add_local_box(group, "MAT_ImperialMarble", origin_xz, nx, nz, tx, tz,
                           r_back - 0.20, r_front + 0.96, -bay_half_w - 0.06, bay_half_w + 0.06, y0 + 0.92 * h, y1)


# ==============================================================================
# 4. MODULAR ARCHETYPE & FULL SCENE CONSTRUCTION (ZERO UNCOUNTED GEOMETRY)
# ==============================================================================
GATE_BAY_INDICES = {47, 0, 11, 12, 23, 24, 35, 36}
# Out of the 20 even non-gate bays, 8 symmetric inter-cardinal bays are UMOD_03_Vomitorium_Cavea_Bay
# and 12 are UMOD_01_Standard_Window_Bay; all 20 odd non-gate bays are UMOD_02_Standard_Clipeus_Bay!
VOMITORIUM_EVEN_BAYS = {4, 8, 16, 20, 28, 32, 40, 44}


def build_foundation_drum_for_bay(builder, b_idx, a0, a1):
    a_mid = 0.5 * (a0 + a1)
    px_out, pz_out, nx, nz, tx, tz = ellipse_point_and_basis(124.0, 130.0, a_mid)
    p0_x, p0_z, _, _, _, _ = ellipse_point_and_basis(124.0, 130.0, a0)
    p1_x, p1_z, _, _, _, _ = ellipse_point_and_basis(124.0, 130.0, a1)
    bay_half_w = 0.5 * math.hypot(p1_x - p0_x, p1_z - p0_z)

    for fc_i in range(5):
        fy0 = 18.0 + fc_i * 6.0 + 0.06
        fy1 = 18.0 + (fc_i + 1) * 6.0 - 0.06
        shrink = (4 - fc_i) * 0.45
        builder.add_elliptical_arc_band(
            "COL_StoneMasonry", "MAT_TuffFoundation" if fc_i < 3 else "MAT_TravertineWarm",
            RX_IN + 1.5 + shrink, RZ_IN + 1.5 + shrink,
            RX_OUT - 1.2 - shrink, RZ_OUT - 1.2 - shrink,
            RX_IN + 1.2 + shrink, RZ_IN + 1.2 + shrink,
            RX_OUT - 1.0 - shrink, RZ_OUT - 1.0 - shrink,
            fy0, fy1, a0, a1, n_sub=1
        )
    builder.add_local_box(
        "COL_StoneMasonry", "MAT_BasaltShadow", (px_out, pz_out), nx, nz, tx, tz,
        r0=1.2, r1=3.6, t0=-bay_half_w, t1=-bay_half_w + 0.85, y0=19.0, y1=48.0, chamfer=0.08
    )
    builder.add_elliptical_arc_band(
        "COL_StoneMasonry", "MAT_TravertineWarm",
        RX_IN, RZ_IN, RX_OUT, RZ_OUT,
        RX_IN, RZ_IN, RX_OUT, RZ_OUT,
        48.0, 49.6, a0, a1, n_sub=1
    )
    builder.add_elliptical_arc_band(
        "COL_StoneMasonry", "MAT_TravertineLight",
        RX_IN, RZ_IN, RX_OUT - 0.6, RZ_OUT - 0.6,
        RX_IN, RZ_IN, RX_OUT - 0.6, RZ_OUT - 0.6,
        49.6, 51.0, a0, a1, n_sub=1
    )


def build_arcade_and_cavea_bay(builder, b_idx, a0, a1, archetype_id):
    """
    Builds one complete non-gate bay (`UMOD_01`, `UMOD_02`, or `UMOD_03`) including its foundation drum.
    Every instance of the same archetype_id generates the EXACT same triangle count!
    """
    builder.current_bay = b_idx
    a_mid = 0.5 * (a0 + a1)
    px_out, pz_out, nx, nz, tx, tz = ellipse_point_and_basis(124.0, 130.0, a_mid)
    p0_x, p0_z, _, _, _, _ = ellipse_point_and_basis(124.0, 130.0, a0)
    p1_x, p1_z, _, _, _, _ = ellipse_point_and_basis(124.0, 130.0, a1)
    bay_half_w = 0.5 * math.hypot(p1_x - p0_x, p1_z - p0_z)

    has_window = (archetype_id in ("UMOD_01_Standard_Window_Bay", "UMOD_03_Vomitorium_Cavea_Bay"))
    has_vomitorium = (archetype_id == "UMOD_03_Vomitorium_Cavea_Bay")
    has_scalaria = (archetype_id in ("UMOD_01_Standard_Window_Bay", "UMOD_03_Vomitorium_Cavea_Bay"))
    has_podium_cyan = (archetype_id == "UMOD_03_Vomitorium_Cavea_Bay")

    # 1. Foundation Drum & Crepidine Plinth (Y = 18.06 .. 51.0)
    build_foundation_drum_for_bay(builder, b_idx, a0, a1)

    # 2. Three Stories of Exterior Arcades & Refined Classical Columns
    stories = [
        {"lvl": 1, "order": "Tuscan",     "y0": 51.0, "y_imp": 59.6, "y_arch_top": 65.6, "y_ent_top": 67.6, "arch_hw": bay_half_w * 0.56, "col_r": 0.78, "medallions": False},
        {"lvl": 2, "order": "Ionic",      "y0": 67.6, "y_imp": 75.8, "y_arch_top": 81.6, "y_ent_top": 83.6, "arch_hw": bay_half_w * 0.54, "col_r": 0.72, "medallions": False},
        {"lvl": 3, "order": "Corinthian", "y0": 83.6, "y_imp": 91.2, "y_arch_top": 96.8, "y_ent_top": 98.8, "arch_hw": bay_half_w * 0.52, "col_r": 0.68, "medallions": True},
    ]
    for st in stories:
        builder.add_true_3d_arch_with_voussoirs(
            "COL_ExteriorArcade", "COL_StoneMasonry",
            (px_out, pz_out), nx, nz, tx, tz,
            r_back=-1.8, r_front=+2.1,
            bay_half_w=bay_half_w, arch_half_w=st["arch_hw"],
            y_floor=st["y0"], y_impost=st["y_imp"], y_top_wall=st["y_arch_top"],
            n_voussoirs=9, keystone_extra_h=0.42, has_medallions=st["medallions"]
        )
        if st["lvl"] >= 2:
            builder.add_local_box(
                "COL_ExteriorArcade", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                r0=0.8, r1=1.6, t0=-st["arch_hw"] + 0.05, t1=st["arch_hw"] - 0.05,
                y0=st["y0"], y1=st["y0"] + 1.65, chamfer=0.05
            )
        col_x = p0_x + 2.32 * nx
        col_z = p0_z + 2.32 * nz
        builder.add_classical_column(
            "COL_ColumnOrders", (col_x, col_z), nx, nz, tx, tz,
            y_base=st["y0"], y_top=st["y_arch_top"],
            order=st["order"], radius=st["col_r"]
        )
        builder.add_entablature_and_cornice_bay(
            "COL_AtticCornice", (px_out, pz_out), nx, nz, tx, tz,
            r_back=-2.0, r_front=+2.25, bay_half_w=bay_half_w,
            y0=st["y_arch_top"], y1=st["y_ent_top"], n_dentils=6
        )

    # 3. Fourth-Story Attic Register, Pilasters, Windows / Clipei, Corbels & Velarium Masts
    y_att_bot = 98.8
    y_att_wall_top = 109.2
    y_att_crown_top = 111.5
    builder.add_local_box(
        "COL_AtticCornice", "MAT_TravertineLight", (px_out, pz_out), nx, nz, tx, tz,
        r0=-1.6, r1=2.15, t0=-bay_half_w + 0.03, t1=bay_half_w - 0.03, y0=y_att_bot, y1=100.6, chamfer=0.05
    )
    pil_t0, pil_t1 = -bay_half_w, -bay_half_w + 1.15
    builder.add_local_box("COL_ColumnOrders", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                          r0=1.8, r1=2.55, t0=pil_t0 - 0.08, t1=pil_t1 + 0.08, y0=100.6, y1=101.4)
    for fl_i in range(3):
        ft0 = pil_t0 + fl_i * 0.38
        ft1 = ft0 + 0.28
        builder.add_local_box("COL_ColumnOrders", "MAT_TravertineLight", (px_out, pz_out), nx, nz, tx, tz,
                              r0=1.9, r1=2.45, t0=ft0, t1=ft1, y0=101.4, y1=107.8)
    builder.add_local_box("COL_ColumnOrders", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                          r0=1.8, r1=2.68, t0=pil_t0 - 0.14, t1=pil_t1 + 0.14, y0=107.8, y1=109.2)

    wt_min, wt_max = -bay_half_w + 1.18, bay_half_w - 0.04
    if has_window:
        win_t0, win_t1 = -1.25, +1.55
        builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                              r0=-1.5, r1=2.05, t0=wt_min, t1=wt_max, y0=100.6, y1=102.4)
        builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                              r0=-1.5, r1=2.05, t0=wt_min, t1=win_t0, y0=102.4, y1=106.8)
        builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                              r0=-1.5, r1=2.05, t0=win_t1, t1=wt_max, y0=102.4, y1=106.8)
        builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                              r0=-1.5, r1=2.05, t0=wt_min, t1=wt_max, y0=106.8, y1=109.2)
        builder.add_local_box("COL_AtticCornice", "MAT_BasaltShadow", (px_out, pz_out), nx, nz, tx, tz,
                              r0=-1.2, r1=0.85, t0=win_t0, t1=win_t1, y0=102.4, y1=106.8)
        builder.add_local_box("COL_AtticCornice", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                              r0=1.85, r1=2.32, t0=win_t0 - 0.24, t1=win_t1 + 0.24, y0=102.0, y1=102.45)
        builder.add_local_box("COL_AtticCornice", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                              r0=1.85, r1=2.36, t0=win_t0 - 0.28, t1=win_t1 + 0.28, y0=106.8, y1=107.35)
    else:
        for ac_i in range(3):
            acy0 = 100.6 + ac_i * 2.86 + 0.03
            acy1 = 100.6 + (ac_i + 1) * 2.86 - 0.03
            t_mid = 0.5 * (wt_min + wt_max)
            builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=-1.5, r1=2.05, t0=wt_min, t1=t_mid - 0.03, y0=acy0, y1=acy1)
            builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=-1.5, r1=2.05, t0=t_mid + 0.03, t1=wt_max, y0=acy0, y1=acy1)
        sh_t = 0.5 * (wt_min + wt_max)
        sh_y = 104.8
        sh_r = 1.65
        lb_s, lt_s = [], []
        for k in range(10):
            ang = k * (2.0 * math.pi / 10.0)
            dt = sh_t + sh_r * math.cos(ang)
            dy = sh_y + sh_r * math.sin(ang)
            lb_s.append((px_out + 2.02 * nx + dt * tx, dy, pz_out + 2.02 * nz + dt * tz))
            lt_s.append((px_out + 2.38 * nx + dt * tx, dy, pz_out + 2.38 * nz + dt * tz))
        builder.add_loft("COL_AtticCornice", "MAT_BronzeClipeus", lb_s, lt_s, cap_bot=False, cap_top=True)
        builder.add_local_box("COL_AtticCornice", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                              r0=2.32, r1=2.56, t0=sh_t - 0.42, t1=sh_t + 0.42, y0=sh_y - 0.42, y1=sh_y + 0.42, chamfer=0.12)

    for cb_t in (-0.35 * bay_half_w, +0.45 * bay_half_w):
        builder.add_local_box("COL_AtticCornice", "MAT_TravertineLight", (px_out, pz_out), nx, nz, tx, tz,
                              r0=2.02, r1=2.82, t0=cb_t - 0.28, t1=cb_t + 0.28, y0=106.2, y1=108.4)
    mast_t = 0.45 * bay_half_w
    builder.add_local_box("COL_AtticCornice", "MAT_BronzeClipeus", (px_out, pz_out), nx, nz, tx, tz,
                          r0=2.25, r1=2.68, t0=mast_t - 0.20, t1=mast_t + 0.20, y0=107.2, y1=114.6)
    builder.add_entablature_and_cornice_bay(
        "COL_AtticCornice", (px_out, pz_out), nx, nz, tx, tz,
        r_back=-1.8, r_front=+2.45, bay_half_w=bay_half_w,
        y0=y_att_wall_top, y1=y_att_crown_top, n_dentils=8
    )

    # 4. Interior Cavea Seating Bowl, Scalaria Stairs, Vomitoria & Upper Porticus
    px_in, pz_in, _, _, _, _ = ellipse_point_and_basis(RX_IN, RZ_IN, a_mid)
    builder.add_elliptical_arc_band(
        "COL_CaveaSeating", "MAT_BasaltShadow",
        RX_IN, RZ_IN, RX_IN + 2.6, RZ_IN + 2.6,
        RX_IN, RZ_IN, RX_IN + 2.6, RZ_IN + 2.6,
        51.0, 59.8, a0, a1, n_sub=1
    )
    builder.add_elliptical_arc_band(
        "COL_CaveaSeating", "MAT_TravertineWarm",
        RX_IN, RZ_IN, RX_IN + 3.2, RZ_IN + 3.2,
        RX_IN, RZ_IN, RX_IN + 3.2, RZ_IN + 3.2,
        59.8, 61.4, a0, a1, n_sub=1
    )
    builder.add_elliptical_arc_band(
        "COL_CaveaSeating", "MAT_ImperialMarble",
        RX_IN, RZ_IN, RX_IN + 0.9, RZ_IN + 0.9,
        RX_IN, RZ_IN, RX_IN + 0.9, RZ_IN + 0.9,
        61.4, 63.0, a0, a1, n_sub=1
    )
    if has_podium_cyan:
        builder.add_local_box(
            "COL_CaveaSeating", "EMI_Cyan", (px_in, pz_in), -nx, -nz, tx, tz,
            r0=-0.45, r1=-0.02, t0=-0.22, t1=0.22, y0=53.0, y1=59.2
        )
    for sp_i in range(3):
        sr0 = RX_IN + 0.9 + sp_i * 1.10
        sz0 = RZ_IN + 0.9 + sp_i * 1.10
        sy0 = 61.4 + sp_i * 1.10
        builder.add_elliptical_arc_band(
            "COL_CaveaSeating", "MAT_ImperialMarble",
            sr0, sz0, sr0 + 1.18, sz0 + 1.18,
            sr0, sz0, sr0 + 1.18, sz0 + 1.18,
            sy0, sy0 + 1.10, a0, a1, n_sub=1
        )

    a_stair_gap = 0.07 * D_THETA
    for row_i in range(8):
        rr0 = RX_IN + 4.2 + row_i * 1.05
        rz0 = RZ_IN + 4.2 + row_i * 1.05
        ry0 = 64.7 + row_i * 1.22
        ry_lip = ry0 + 0.92
        ry1 = ry0 + 1.22
        builder.add_elliptical_arc_band(
            "COL_CaveaSeating", "MAT_LimestoneCream",
            rr0, rz0, rr0 + 1.12, rz0 + 1.12,
            rr0, rz0, rr0 + 1.12, rz0 + 1.12,
            ry0, ry_lip, a0 + a_stair_gap, a1 - a_stair_gap, n_sub=1, cap_top=False
        )
        builder.add_elliptical_arc_band(
            "COL_CaveaSeating", "MAT_TravertineLight",
            rr0 - 0.16, rz0 - 0.16, rr0 + 1.12, rz0 + 1.12,
            rr0 - 0.16, rz0 - 0.16, rr0 + 1.12, rz0 + 1.12,
            ry_lip, ry1, a0 + a_stair_gap, a1 - a_stair_gap, n_sub=1, cap_bot=True, cap_top=True
        )

    if has_scalaria:
        for stp_i in range(8):
            sr_p = (RX_IN + 4.2 + stp_i * 1.05) - 124.0
            sy_p = 64.7 + stp_i * 1.22
            builder.add_local_box(
                "COL_CaveaSeating", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                r0=sr_p, r1=sr_p + 1.10, t0=-bay_half_w, t1=-bay_half_w + 0.95,
                y0=sy_p, y1=sy_p + 0.65
            )

    r_prae_x, r_prae_z = RX_IN + 12.6, RZ_IN + 12.6
    builder.add_elliptical_arc_band(
        "COL_Vomitoria", "MAT_TravertineWarm",
        r_prae_x, r_prae_z, r_prae_x + 2.4, r_prae_z + 2.4,
        r_prae_x, r_prae_z, r_prae_x + 2.4, r_prae_z + 2.4,
        73.8, 74.6, a0, a1, n_sub=1
    )
    if has_vomitorium:
        px_vom, pz_vom, _, _, _, _ = ellipse_point_and_basis(r_prae_x + 1.8, r_prae_z + 1.8, a_mid)
        builder.add_local_box(
            "COL_Vomitoria", "MAT_BasaltShadow", (px_vom, pz_vom), -nx, -nz, tx, tz,
            r0=-1.6, r1=0.2, t0=-bay_half_w * 0.48, t1=bay_half_w * 0.48, y0=74.6, y1=79.2
        )
        builder.add_true_3d_arch_with_voussoirs(
            "COL_Vomitoria", "COL_Vomitoria",
            (px_vom, pz_vom), -nx, -nz, -tx, -tz,
            r_back=-0.6, r_front=+0.45,
            bay_half_w=bay_half_w * 0.88, arch_half_w=bay_half_w * 0.46,
            y_floor=74.6, y_impost=77.4, y_top_wall=80.2,
            n_voussoirs=7, keystone_extra_h=0.28, has_medallions=False
        )
    else:
        builder.add_elliptical_arc_band(
            "COL_Vomitoria", "MAT_TravertineWarm",
            r_prae_x + 1.4, r_prae_z + 1.4, r_prae_x + 2.6, r_prae_z + 2.6,
            r_prae_x + 1.4, r_prae_z + 1.4, r_prae_x + 2.6, r_prae_z + 2.6,
            74.6, 80.2, a0, a1, n_sub=1
        )
        builder.add_elliptical_arc_band(
            "COL_Vomitoria", "MAT_ImperialMarble",
            r_prae_x + 1.2, r_prae_z + 1.2, r_prae_x + 2.7, r_prae_z + 2.7,
            r_prae_x + 1.2, r_prae_z + 1.2, r_prae_x + 2.7, r_prae_z + 2.7,
            79.8, 80.4, a0, a1, n_sub=1
        )

    for urow_i in range(11):
        ur0 = RX_IN + 15.0 + urow_i * 0.85
        uz0 = RZ_IN + 15.0 + urow_i * 0.85
        uy0 = 80.2 + urow_i * 1.40
        uy_lip = uy0 + 1.05
        uy1 = uy0 + 1.40
        builder.add_elliptical_arc_band(
            "COL_CaveaSeating", "MAT_LimestoneCream",
            ur0, uz0, ur0 + 0.92, uz0 + 0.92,
            ur0, uz0, ur0 + 0.92, uz0 + 0.92,
            uy0, uy_lip, a0 + a_stair_gap, a1 - a_stair_gap, n_sub=1, cap_top=False
        )
        builder.add_elliptical_arc_band(
            "COL_CaveaSeating", "MAT_TravertineLight",
            ur0 - 0.14, uz0 - 0.14, ur0 + 0.92, uz0 + 0.92,
            ur0 - 0.14, uz0 - 0.14, ur0 + 0.92, uz0 + 0.92,
            uy_lip, uy1, a0 + a_stair_gap, a1 - a_stair_gap, n_sub=1, cap_bot=True, cap_top=True
        )

    col_in_x, col_in_z, _, _, _, _ = ellipse_point_and_basis(RX_IN + 24.4, RZ_IN + 24.4, a0)
    builder.add_classical_column(
        "COL_CaveaSeating", (col_in_x, col_in_z), -nx, -nz, -tx, -tz,
        y_base=95.6, y_top=106.6, order="Corinthian", radius=0.58
    )
    builder.add_elliptical_arc_band(
        "COL_CaveaSeating", "MAT_TravertineLight",
        RX_IN + 24.0, RZ_IN + 24.0, RX_OUT - 1.5, RZ_OUT - 1.5,
        RX_IN + 24.0, RZ_IN + 24.0, RX_OUT - 1.5, RZ_OUT - 1.5,
        106.6, 109.2, a0, a1, n_sub=1
    )


def build_gate_pavilion_module(builder, g_name, g_theta, r_in_g, r_out_g, bay_pair):
    """
    Builds one complete 2-bay Cardinal Triumphal Gate Pavilion (`UMOD_04_Cardinal_Triumphal_Gate_Pavilion`),
    including its 2-bay foundation drum so 100% of gate triangles belong to `UMOD_04`.
    """
    for b_sub in bay_pair:
        builder.current_bay = b_sub
        a0 = b_sub * D_THETA
        a1 = (b_sub + 1) * D_THETA
        build_foundation_drum_for_bay(builder, b_sub, a0, a1)

    builder.current_bay = bay_pair[1]
    ca, sa = math.cos(g_theta), math.sin(g_theta)
    nx, nz = ca, sa
    tx, tz = -sa, ca
    r_mid = 0.5 * (r_in_g + r_out_g)
    dr_half = 0.5 * (r_out_g - r_in_g)
    ox, oz = r_mid * nx, r_mid * nz
    gate_hw = 13.8
    portal_hw = 7.4

    builder.add_local_box(
        "COL_GateTowers", "MAT_TravertineWarm", (ox, oz), nx, nz, tx, tz,
        r0=-dr_half, r1=dr_half, t0=-gate_hw, t1=gate_hw, y0=48.8, y1=51.2, chamfer=0.12
    )

    for face_s, face_r in [(-1.0, -dr_half + 3.85), (+1.0, dr_half - 3.85)]:
        fnx, fnz = face_s * nx, face_s * nz
        ftx, ftz = face_s * tx, face_s * tz
        fox, foz = ox + face_r * nx, oz + face_r * nz

        builder.add_true_3d_arch_with_voussoirs(
            "COL_GateTowers", "COL_GateTowers",
            (fox, foz), fnx, fnz, ftx, ftz,
            r_back=-2.2, r_front=+2.2,
            bay_half_w=gate_hw, arch_half_w=portal_hw,
            y_floor=51.2, y_impost=69.5, y_top_wall=85.0,
            n_voussoirs=13, keystone_extra_h=0.85, has_medallions=True
        )

        for side_s in (-1.0, +1.0):
            for pair_off in (portal_hw + 1.85, portal_hw + 4.85):
                col_t = side_s * pair_off
                col_x = fox + 2.55 * fnx + col_t * ftx
                col_z = foz + 2.55 * fnz + col_t * ftz
                builder.add_classical_column(
                    "COL_GateTowers", (col_x, col_z), fnx, fnz, ftx, ftz,
                    y_base=51.2, y_top=85.0, order="Corinthian", radius=0.92
                )
            nt_c = side_s * (portal_hw + 3.35)
            builder.add_local_box(
                "COL_GateTowers", "MAT_BasaltShadow", (fox, foz), fnx, fnz, ftx, ftz,
                r0=1.2, r1=2.25, t0=nt_c - 0.85, t1=nt_c + 0.85, y0=58.5, y1=68.0
            )
            builder.add_local_box(
                "COL_GateTowers", "MAT_ImperialMarble", (fox, foz), fnx, fnz, ftx, ftz,
                r0=1.8, r1=2.42, t0=nt_c - 1.05, t1=nt_c + 1.05, y0=68.0, y1=69.2, chamfer=0.06
            )

        builder.add_entablature_and_cornice_bay(
            "COL_GateTowers", (fox, foz), fnx, fnz, ftx, ftz,
            r_back=-2.2, r_front=+2.8, bay_half_w=gate_hw + 0.4,
            y0=85.0, y1=88.2, n_dentils=14
        )

        ped_w = portal_hw + 4.2
        ped_b = [
            (fox - 1.5 * fnx - ped_w * ftx, 88.2, foz - 1.5 * fnz - ped_w * ftz),
            (fox + 3.1 * fnx - ped_w * ftx, 88.2, foz + 3.1 * fnz - ped_w * ftz),
            (fox + 3.1 * fnx + ped_w * ftx, 88.2, foz + 3.1 * fnz + ped_w * ftz),
            (fox - 1.5 * fnx + ped_w * ftx, 88.2, foz - 1.5 * fnz + ped_w * ftz),
        ]
        ped_t = [
            (fox - 1.5 * fnx - 0.8 * ftx, 95.8, foz - 1.5 * fnz - 0.8 * ftz),
            (fox + 3.1 * fnx - 0.8 * ftx, 95.8, foz + 3.1 * fnz - 0.8 * ftz),
            (fox + 3.1 * fnx + 0.8 * ftx, 95.8, foz + 3.1 * fnz + 0.8 * ftz),
            (fox - 1.5 * fnx + 0.8 * ftx, 95.8, foz - 1.5 * fnz + 0.8 * ftz),
        ]
        builder.add_loft("COL_GateTowers", "MAT_ImperialMarble", ped_b, ped_t, cap_bot=False, cap_top=True)

    for side_s in (-1.0, +1.0):
        wt0 = min(side_s * portal_hw, side_s * gate_hw)
        wt1 = max(side_s * portal_hw, side_s * gate_hw)
        for gc_i in range(6):
            gy0 = 51.2 + gc_i * 5.6 + 0.04
            gy1 = 51.2 + (gc_i + 1) * 5.6 - 0.04
            builder.add_local_box(
                "COL_GateTowers", "MAT_TravertineWarm", (ox, oz), nx, nz, tx, tz,
                r0=-dr_half + 2.0, r1=dr_half - 2.0, t0=wt0, t1=wt1, y0=gy0, y1=gy1, chamfer=0.06
            )

    n_v_rad = 5
    n_v_ang = 7
    r_v_span = (2.0 * dr_half - 4.0) / float(n_v_rad)
    for vr_i in range(n_v_rad):
        vr0 = -dr_half + 2.0 + vr_i * r_v_span + 0.12
        vr1 = vr0 + r_v_span - 0.24
        for va_i in range(n_v_ang):
            phi0 = (va_i + 0.1) * (math.pi / n_v_ang)
            phi1 = (va_i + 0.9) * (math.pi / n_v_ang)
            vt0, vy0 = (portal_hw - 0.25) * math.cos(phi0), 69.5 + (portal_hw - 0.25) * math.sin(phi0)
            vt1, vy1 = (portal_hw - 0.25) * math.cos(phi1), 69.5 + (portal_hw - 0.25) * math.sin(phi1)
            lb_cf = [
                (ox + vr0 * nx + vt0 * tx, vy0, oz + vr0 * nz + vt0 * tz),
                (ox + vr1 * nx + vt0 * tx, vy0, oz + vr1 * nz + vt0 * tz),
                (ox + vr1 * nx + vt1 * tx, vy1, oz + vr1 * nz + vt1 * tz),
                (ox + vr0 * nx + vt1 * tx, vy1, oz + vr0 * nz + vt1 * tz),
            ]
            lt_cf = [
                (ox + vr0 * nx + vt0 * tx, vy0 + 0.45, oz + vr0 * nz + vt0 * tz),
                (ox + vr1 * nx + vt0 * tx, vy0 + 0.45, oz + vr1 * nz + vt0 * tz),
                (ox + vr1 * nx + vt1 * tx, vy1 + 0.45, oz + vr1 * nz + vt1 * tz),
                (ox + vr0 * nx + vt1 * tx, vy1 + 0.45, oz + vr0 * nz + vt1 * tz),
            ]
            builder.add_loft("COL_GateTowers", "MAT_ImperialMarble", lb_cf, lt_cf)

    builder.add_local_box(
        "COL_GateTowers", "MAT_DarkNeutral", (ox, oz), nx, nz, tx, tz,
        r0=-1.2, r1=1.2, t0=-portal_hw, t1=portal_hw, y0=51.2, y1=76.5
    )
    builder.add_local_box(
        "COL_GateTowers", "MAT_AltNeutral", (ox, oz), nx, nz, tx, tz,
        r0=-1.5, r1=1.5, t0=-portal_hw, t1=portal_hw, y0=51.2, y1=52.2
    )
    builder.add_local_box(
        "COL_GateTowers", "MAT_LightTrim", (ox, oz), nx, nz, tx, tz,
        r0=-1.4, r1=1.4, t0=-portal_hw, t1=portal_hw, y0=75.8, y1=76.6
    )
    for p_t in (-3.2, 0.0, +3.2):
        builder.add_local_box(
            "COL_GateTowers", "EMI_Cyan", (ox, oz), nx, nz, tx, tz,
            r0=-1.35, r1=1.35, t0=p_t - 0.24, t1=p_t + 0.24, y0=52.0, y1=74.5
        )

    for gc_a in range(4):
        gay0 = 88.2 + gc_a * 5.8 + 0.05
        gay1 = 88.2 + (gc_a + 1) * 5.8 - 0.05
        builder.add_local_box(
            "COL_GateTowers", "MAT_TravertineWarm", (ox, oz), nx, nz, tx, tz,
            r0=-dr_half + 1.6, r1=dr_half - 1.6, t0=-gate_hw + 0.4, t1=gate_hw - 0.4, y0=gay0, y1=gay1, chamfer=0.08
        )
    builder.add_entablature_and_cornice_bay(
        "COL_GateTowers", (ox, oz), -nx, -nz, tx, tz,
        r_back=-(dr_half - 1.4), r_front=(dr_half - 1.4), bay_half_w=gate_hw,
        y0=111.4, y1=114.5, n_dentils=16
    )


def build_north_crest_module(builder):
    """Builds the North Imperial Tribune & Reactor Crest (`UMOD_05_North_Imperial_Reactor_Crest`, Y = 114.5 .. 125.0)."""
    builder.current_bay = 36
    g_theta = 1.5 * math.pi
    r_in_g, r_out_g = RZ_IN, RZ_OUT + 2.0
    ca, sa = math.cos(g_theta), math.sin(g_theta)
    nx, nz = ca, sa
    tx, tz = -sa, ca
    r_mid = 0.5 * (r_in_g + r_out_g)
    ox, oz = r_mid * nx, r_mid * nz

    builder.add_local_box(
        "COL_NorthReactorCrest", "MAT_TravertineLight", (ox, oz), -nx, -nz, tx, tz,
        r0=-8.5, r1=8.5, t0=-10.2, t1=10.2, y0=114.5, y1=116.8, chamfer=0.10
    )
    for cr_s in (-1.0, +1.0):
        for cr_t in (4.8, 7.6):
            cc_x = ox - 6.8 * nx + (cr_s * cr_t) * tx
            cc_z = oz - 6.8 * nz + (cr_s * cr_t) * tz
            builder.add_classical_column(
                "COL_NorthReactorCrest", (cc_x, cc_z), -nx, -nz, tx, tz,
                y_base=116.8, y_top=122.8, order="Corinthian", radius=0.62
            )
        builder.add_local_box(
            "COL_NorthReactorCrest", "MAT_TravertineWarm", (ox, oz), -nx, -nz, tx, tz,
            r0=-6.5, r1=6.5, t0=cr_s * 4.2 - 1.4, t1=cr_s * 4.2 + 1.4, y0=116.8, y1=122.8, chamfer=0.06
        )

    builder.add_true_3d_arch_with_voussoirs(
        "COL_NorthReactorCrest", "COL_NorthReactorCrest",
        (ox - 5.2 * nx, oz - 5.2 * nz), -nx, -nz, tx, tz,
        r_back=-2.5, r_front=+2.0,
        bay_half_w=5.6, arch_half_w=3.2,
        y_floor=116.8, y_impost=119.5, y_top_wall=123.0,
        n_voussoirs=9, keystone_extra_h=0.35, has_medallions=False
    )
    builder.add_local_box(
        "COL_NorthReactorCrest", "MAT_DarkNeutral", (ox, oz), -nx, -nz, tx, tz,
        r0=-5.8, r1=-3.2, t0=-2.8, t1=2.8, y0=117.2, y1=121.8
    )
    builder.add_local_box(
        "COL_NorthReactorCrest", "MAT_AltNeutral", (ox, oz), -nx, -nz, tx, tz,
        r0=-5.9, r1=-5.4, t0=-2.5, t1=2.5, y0=117.4, y1=121.5
    )
    builder.add_local_box(
        "COL_NorthReactorCrest", "MAT_LightTrim", (ox, oz), -nx, -nz, tx, tz,
        r0=-5.95, r1=-5.55, t0=-2.3, t1=2.3, y0=117.6, y1=121.4
    )
    builder.add_local_box(
        "COL_NorthReactorCrest", "EMI_Cyan", (ox, oz), -nx, -nz, tx, tz,
        r0=-6.0, r1=-5.6, t0=-2.1, t1=2.1, y0=117.8, y1=121.2
    )
    builder.add_local_box(
        "COL_NorthReactorCrest", "EMI_Amber", (ox, oz), -nx, -nz, tx, tz,
        r0=-6.1, r1=-5.7, t0=-0.95, t1=0.95, y0=118.8, y1=120.4
    )
    builder.add_entablature_and_cornice_bay(
        "COL_NorthReactorCrest", (ox - 5.2 * nx, oz - 5.2 * nz), -nx, -nz, tx, tz,
        r_back=-3.2, r_front=+2.4, bay_half_w=8.8,
        y0=122.8, y1=125.0, n_dentils=10
    )


def build_production_colosseum():
    """
    Constructs the complete 48-bay Colosseum by instancing the 5 modular archetypes (`UMOD_01..UMOD_05`)
    and also builds standalone local-origin copies of each of the 5 reusable archetypes.
    """
    scene_builder = HighDetailColosseumBuilder()
    instance_manifest = []

    # 1. Instantiate all 40 non-gate bays (`12 x UMOD_01`, `20 x UMOD_02`, `8 x UMOD_03`)
    for b_idx in range(N_BAYS):
        if b_idx in GATE_BAY_INDICES:
            continue
        a0 = b_idx * D_THETA
        a1 = (b_idx + 1) * D_THETA
        a_mid = 0.5 * (a0 + a1)
        if b_idx % 2 == 1:
            arch_id = "UMOD_02_Standard_Clipeus_Bay"
        elif b_idx in VOMITORIUM_EVEN_BAYS:
            arch_id = "UMOD_03_Vomitorium_Cavea_Bay"
        else:
            arch_id = "UMOD_01_Standard_Window_Bay"

        t_before = len(scene_builder.tris)
        build_arcade_and_cavea_bay(scene_builder, b_idx, a0, a1, arch_id)
        t_after = len(scene_builder.tris)
        px_out, pz_out, nx, nz, _, _ = ellipse_point_and_basis(124.0, 130.0, a_mid)
        instance_manifest.append({
            "instance_index": len(instance_manifest) + 1,
            "archetype_id": arch_id,
            "bay_index": b_idx,
            "azimuth_deg": round(math.degrees(a_mid), 3),
            "reference_pivot_world": [round(px_out, 4), 51.0, round(pz_out, 4)],
            "outward_normal_xz": [round(nx, 5), round(nz, 5)],
            "triangles": t_after - t_before,
        })

    # 2. Instantiate the 4 Cardinal Triumphal Gate Pavilions (`4 x UMOD_04`)
    cardinal_gates = [
        ("East",  0.0,           RX_IN, RX_OUT + 2.0, (47, 0)),
        ("South", 0.5 * math.pi, RZ_IN, RZ_OUT + 2.0, (11, 12)),
        ("West",  math.pi,       RX_IN, RX_OUT + 2.0, (23, 24)),
        ("North", 1.5 * math.pi, RZ_IN, RZ_OUT + 2.0, (35, 36)),
    ]
    for g_name, g_theta, r_in_g, r_out_g, bay_pair in cardinal_gates:
        t_before = len(scene_builder.tris)
        build_gate_pavilion_module(scene_builder, g_name, g_theta, r_in_g, r_out_g, bay_pair)
        t_after = len(scene_builder.tris)
        r_mid = 0.5 * (r_in_g + r_out_g)
        nx, nz = math.cos(g_theta), math.sin(g_theta)
        instance_manifest.append({
            "instance_index": len(instance_manifest) + 1,
            "archetype_id": "UMOD_04_Cardinal_Triumphal_Gate_Pavilion",
            "cardinal_direction": g_name,
            "occupied_bays": list(bay_pair),
            "azimuth_deg": round(math.degrees(g_theta), 3),
            "reference_pivot_world": [round(r_mid * nx, 4), 51.0, round(r_mid * nz, 4)],
            "outward_normal_xz": [round(nx, 5), round(nz, 5)],
            "triangles": t_after - t_before,
        })

    # 3. Instantiate the North Imperial Reactor Crest (`1 x UMOD_05`)
    t_before = len(scene_builder.tris)
    build_north_crest_module(scene_builder)
    t_after = len(scene_builder.tris)
    instance_manifest.append({
        "instance_index": len(instance_manifest) + 1,
        "archetype_id": "UMOD_05_North_Imperial_Reactor_Crest",
        "cardinal_direction": "North",
        "occupied_bays": [35, 36],
        "azimuth_deg": 270.0,
        "reference_pivot_world": [0.0, 114.5, -120.0],
        "outward_normal_xz": [0.0, -1.0],
        "triangles": t_after - t_before,
    })

    # 4. Build standalone canonical Archetype Meshes (recentered to local module origin (0, 0, 0))
    archetype_builders = OrderedDict()
    for arch_id, sample_bay in [
        ("UMOD_01_Standard_Window_Bay",              2),
        ("UMOD_02_Standard_Clipeus_Bay",             1),
        ("UMOD_03_Vomitorium_Cavea_Bay",             4),
        ("UMOD_04_Cardinal_Triumphal_Gate_Pavilion", 0),
        ("UMOD_05_North_Imperial_Reactor_Crest",    36),
    ]:
        ab = HighDetailColosseumBuilder()
        if arch_id in ("UMOD_01_Standard_Window_Bay", "UMOD_02_Standard_Clipeus_Bay", "UMOD_03_Vomitorium_Cavea_Bay"):
            a0 = sample_bay * D_THETA
            a1 = (sample_bay + 1) * D_THETA
            a_mid = 0.5 * (a0 + a1)
            build_arcade_and_cavea_bay(ab, sample_bay, a0, a1, arch_id)
            px, pz, pnx, pnz, ptx, ptz = ellipse_point_and_basis(124.0, 130.0, a_mid)
            ref_y = 51.0
        elif arch_id == "UMOD_04_Cardinal_Triumphal_Gate_Pavilion":
            build_gate_pavilion_module(ab, "East", 0.0, RX_IN, RX_OUT + 2.0, (47, 0))
            px, pz, pnx, pnz, ptx, ptz = 0.5 * (RX_IN + RX_OUT + 2.0), 0.0, 1.0, 0.0, 0.0, 1.0
            ref_y = 51.0
        else:
            build_north_crest_module(ab)
            px, pz, pnx, pnz, ptx, ptz = 0.0, -0.5 * (RZ_IN + RZ_OUT + 2.0), 0.0, -1.0, 1.0, 0.0
            ref_y = 114.5

        for t in ab.tris:
            for vk in ("v0", "v1", "v2"):
                vx, vy, vz = t[vk]
                dx, dy, dz = vx - px, vy - ref_y, vz - pz
                lx = round(dx * ptx + dz * ptz, 4)
                ly = round(dy, 4)
                lz = round(dx * pnx + dz * pnz, 4)
                t[vk] = (lx, ly, lz)
            nx_w, ny_w, nz_w = t["nrm"]
            t["nrm"] = (
                round(nx_w * ptx + nz_w * ptz, 5),
                round(ny_w, 5),
                round(nx_w * pnx + nz_w * pnz, 5),
            )
        archetype_builders[arch_id] = ab

    return scene_builder, archetype_builders, instance_manifest


def assign_section_submesh_name(tri):
    """
    Maps every triangle in the assembled Colosseum into import-safe architectural
    MeshPart sections where EVERY section is strictly < 15,000 triangles (< 20,000 limit).
    """
    g = tri["group"]
    b = tri["bay"]
    if g == "COL_NorthReactorCrest":
        return "COL_NorthReactorCrest"
    if g == "COL_GateTowers":
        if b in (47, 0):
            return "COL_GateTower_East"
        elif b in (11, 12):
            return "COL_GateTower_South"
        elif b in (23, 24):
            return "COL_GateTower_West"
        else:
            return "COL_GateTower_North"
    if g == "COL_ColumnOrders":
        # Split ColumnOrders into 8 octants (O1..O8, 6 bays each) so each MeshPart is ~8,200 triangles (< 20,000)
        o = (b // 6) + 1
        return f"COL_ColumnOrders_O{o}"
    # Map bay 0..47 into 4 quadrants (Q1..Q4, 12 bays each)
    q = (b // 12) + 1
    return f"{g}_Q{q}"


# ==============================================================================
# 5. MULTI-FORMAT EXPORTERS (.OBJ+.MTL WITH UVS/NORMALS, .GLB, .GLTF+.BIN, .FBX)
# ==============================================================================
def write_mtl_file(mtl_path, rel_atlas_path):
    with open(mtl_path, "w", encoding="utf-8") as mf:
        mf.write("# Sphere Brawl: Rolling Rampage — SM_ArenaEnvironment_Colosseum_01 Production Material Library\n")
        for mname, mprops in MATERIALS.items():
            r, g, b = [c / 255.0 for c in mprops["rgb"]]
            er, eg, eb = mprops["emissive"]
            mf.write(f"newmtl {mname}\n")
            mf.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n")
            mf.write("Ka 0.1500 0.1500 0.1500\n")
            mf.write("Ks 0.2200 0.2200 0.2200\n")
            mf.write(f"Ke {er:.4f} {eg:.4f} {eb:.4f}\n")
            mf.write("Ns 36.0\n")
            mf.write("d 1.0\n")
            mf.write(f"map_Kd {rel_atlas_path}\n\n")


def export_obj_with_uvs_and_normals(tris_by_group, obj_path, mtl_filename):
    with open(obj_path, "w", encoding="utf-8") as of:
        of.write("# SPHERE BRAWL: ROLLING RAMPAGE — SM_ArenaEnvironment_Colosseum_01 (Phase 2 Production Mesh)\n")
        of.write("# Scale: 1 unit = 1 Roblox stud | World Origin: (0, 0, 0) | Locked Arena Grid: (0, 50, 0)\n")
        of.write(f"mtllib {mtl_filename}\n")
        v_idx = 1
        for gname, gtris in tris_by_group.items():
            of.write(f"\no {gname}\n")
            of.write(f"g {gname}\n")
            cur_mat = None
            for t in gtris:
                mname = t["mat"]
                if mname != cur_mat:
                    of.write(f"usemtl {mname}\n")
                    cur_mat = mname
                v0, v1, v2 = t["v0"], t["v1"], t["v2"]
                uv0, uv1, uv2 = t["uv0"], t["uv1"], t["uv2"]
                nx, ny, nz = t["nrm"]
                of.write(f"v {v0[0]:.4f} {v0[1]:.4f} {v0[2]:.4f}\n")
                of.write(f"v {v1[0]:.4f} {v1[1]:.4f} {v1[2]:.4f}\n")
                of.write(f"v {v2[0]:.4f} {v2[1]:.4f} {v2[2]:.4f}\n")
                of.write(f"vt {uv0[0]:.5f} {uv0[1]:.5f}\n")
                of.write(f"vt {uv1[0]:.5f} {uv1[1]:.5f}\n")
                of.write(f"vt {uv2[0]:.5f} {uv2[1]:.5f}\n")
                of.write(f"vn {nx:.5f} {ny:.5f} {nz:.5f}\n")
                of.write(f"vn {nx:.5f} {ny:.5f} {nz:.5f}\n")
                of.write(f"vn {nx:.5f} {ny:.5f} {nz:.5f}\n")
                of.write(f"f {v_idx}/{v_idx}/{v_idx} {v_idx+1}/{v_idx+1}/{v_idx+1} {v_idx+2}/{v_idx+2}/{v_idx+2}\n")
                v_idx += 3


def export_glb_and_gltf(tris_by_group, glb_path, gltf_path=None, bin_path=None, rel_tex_uri=None):
    bin_chunks = []
    buffer_views = []
    accessors = []
    meshes = []
    nodes = []
    byte_offset = 0

    gltf_materials = []
    for mname, mprops in MATERIALS.items():
        r, g, b = [c / 255.0 for c in mprops["rgb"]]
        pbr = {
            "baseColorFactor": [round(r, 4), round(g, 4), round(b, 4), 1.0],
            "metallicFactor": mprops["metallic"],
            "roughnessFactor": mprops["roughness"],
        }
        if rel_tex_uri is not None:
            pbr["baseColorTexture"] = {"index": 0}
        mat_entry = {
            "name": mname,
            "pbrMetallicRoughness": pbr,
            "doubleSided": False,
        }
        if sum(mprops["emissive"]) > 0.0:
            mat_entry["emissiveFactor"] = list(mprops["emissive"])
        gltf_materials.append(mat_entry)

    for g_idx, (gname, gtris) in enumerate(tris_by_group.items()):
        by_mat = OrderedDict()
        for t in gtris:
            by_mat.setdefault(t["mat"], []).append(t)

        primitives = []
        for mname, mtris in by_mat.items():
            n_v = len(mtris) * 3
            pos_arr = np.zeros((n_v, 3), dtype=np.float32)
            nrm_arr = np.zeros((n_v, 3), dtype=np.float32)
            uv_arr  = np.zeros((n_v, 2), dtype=np.float32)
            col_arr = np.zeros((n_v, 3), dtype=np.float32)
            rgb = [c / 255.0 for c in MATERIALS[mname]["rgb"]]

            for i, t in enumerate(mtris):
                base_i = i * 3
                pos_arr[base_i + 0] = t["v0"]
                pos_arr[base_i + 1] = t["v1"]
                pos_arr[base_i + 2] = t["v2"]
                nrm_arr[base_i:base_i + 3] = t["nrm"]
                uv_arr[base_i + 0] = t["uv0"]
                uv_arr[base_i + 1] = t["uv1"]
                uv_arr[base_i + 2] = t["uv2"]
                col_arr[base_i:base_i + 3] = rgb

            def add_attr(arr, acc_type, with_minmax=False):
                nonlocal byte_offset
                raw = arr.tobytes()
                bv_idx = len(buffer_views)
                buffer_views.append({"buffer": 0, "byteOffset": byte_offset, "byteLength": len(raw), "target": 34962})
                byte_offset += len(raw)
                bin_chunks.append(raw)
                acc_idx = len(accessors)
                acc_obj = {"bufferView": bv_idx, "componentType": 5126, "count": n_v, "type": acc_type}
                if with_minmax:
                    acc_obj["min"] = [float(x) for x in arr.min(axis=0)]
                    acc_obj["max"] = [float(x) for x in arr.max(axis=0)]
                accessors.append(acc_obj)
                return acc_idx

            acc_pos = add_attr(pos_arr, "VEC3", with_minmax=True)
            acc_nrm = add_attr(nrm_arr, "VEC3", with_minmax=False)
            acc_uv  = add_attr(uv_arr,  "VEC2", with_minmax=False)
            acc_col = add_attr(col_arr, "VEC3", with_minmax=False)

            primitives.append({
                "attributes": {
                    "POSITION": acc_pos,
                    "NORMAL": acc_nrm,
                    "TEXCOORD_0": acc_uv,
                    "COLOR_0": acc_col,
                },
                "material": MAT_INDEX[mname],
                "mode": 4,
            })

        meshes.append({"name": gname, "primitives": primitives})
        nodes.append({"name": gname, "mesh": g_idx})

    bin_blob = b"".join(bin_chunks)
    while len(bin_blob) % 4 != 0:
        bin_blob += b"\x00"

    glb_materials = []
    for m in gltf_materials:
        mc = json.loads(json.dumps(m))
        mc["pbrMetallicRoughness"].pop("baseColorTexture", None)
        glb_materials.append(mc)

    glb_dict = {
        "asset": {"version": "2.0", "generator": "SphereBrawl_Colosseum_Phase2_Production_Generator"},
        "scene": 0,
        "scenes": [{"name": "SM_ArenaEnvironment_Colosseum_01", "nodes": list(range(len(nodes)))}],
        "nodes": nodes,
        "meshes": meshes,
        "materials": glb_materials,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{"byteLength": len(bin_blob)}],
    }
    json_bytes = json.dumps(glb_dict, separators=(",", ":")).encode("utf-8")
    while len(json_bytes) % 4 != 0:
        json_bytes += b" "

    total_len = 12 + 8 + len(json_bytes) + 8 + len(bin_blob)
    with open(glb_path, "wb") as gf:
        gf.write(struct.pack("<III", 0x46546C67, 2, total_len))
        gf.write(struct.pack("<II", len(json_bytes), 0x4E4F534A))
        gf.write(json_bytes)
        gf.write(struct.pack("<II", len(bin_blob), 0x004E4942))
        gf.write(bin_blob)

    if gltf_path and bin_path:
        with open(bin_path, "wb") as bf:
            bf.write(bin_blob)
        gltf_ext_dict = {
            "asset": {"version": "2.0", "generator": "SphereBrawl_Colosseum_Phase2_Production_Generator"},
            "scene": 0,
            "scenes": [{"name": "SM_ArenaEnvironment_Colosseum_01", "nodes": list(range(len(nodes)))}],
            "nodes": nodes,
            "meshes": meshes,
            "materials": gltf_materials,
            "textures": [{"source": 0}] if rel_tex_uri else [],
            "images": [{"uri": rel_tex_uri}] if rel_tex_uri else [],
            "accessors": accessors,
            "bufferViews": buffer_views,
            "buffers": [{"uri": os.path.basename(bin_path), "byteLength": len(bin_blob)}],
        }
        with open(gltf_path, "w", encoding="utf-8") as gtf:
            json.dump(gltf_ext_dict, gtf, indent=2)


def export_fbx_ascii(tris_by_group, fbx_path):
    with open(fbx_path, "w", encoding="utf-8") as ff:
        ff.write("; FBX 7.4.0 project file\n")
        ff.write("; Sphere Brawl: Rolling Rampage — SM_ArenaEnvironment_Colosseum_01 (Phase 2 Production Model)\n")
        ff.write("FBXHeaderExtension:  {\n\tFBXHeaderVersion: 1003\n\tFBXVersion: 7400\n}\n")
        ff.write("GlobalSettings:  {\n\tVersion: 1000\n\tProperties70:  {\n")
        ff.write('\t\tP: "UpAxis", "int", "Integer", "",1\n')
        ff.write('\t\tP: "UpAxisSign", "int", "Integer", "",1\n')
        ff.write('\t\tP: "FrontAxis", "int", "Integer", "",2\n')
        ff.write('\t\tP: "FrontAxisSign", "int", "Integer", "",1\n')
        ff.write('\t\tP: "CoordAxis", "int", "Integer", "",0\n')
        ff.write('\t\tP: "CoordAxisSign", "int", "Integer", "",1\n')
        ff.write('\t\tP: "UnitScaleFactor", "double", "Number", "",1.0\n')
        ff.write("\t}\n}\n")
        ff.write("Objects:  {\n")

        for m_idx, (mname, mprops) in enumerate(MATERIALS.items()):
            mat_id = 300000 + m_idx
            r, g, b = [c / 255.0 for c in mprops["rgb"]]
            ff.write(f'\tMaterial: {mat_id}, "Material::{mname}", "" {{\n\t\tVersion: 102\n\t\tShadingModel: "phong"\n\t\tProperties70:  {{\n')
            ff.write(f'\t\t\tP: "DiffuseColor", "Color", "", "A",{r:.4f},{g:.4f},{b:.4f}\n')
            ff.write("\t\t}\n\t}\n")

        for g_idx, (gname, gtris) in enumerate(tris_by_group.items()):
            geom_id = 100000 + g_idx
            model_id = 200000 + g_idx
            n_v = len(gtris) * 3
            ff.write(f'\tGeometry: {geom_id}, "Geometry::{gname}", "Mesh" {{\n')
            v_strs, i_strs, n_strs, uv_strs, m_strs = [], [], [], [], []
            vi = 0
            for t in gtris:
                v0, v1, v2 = t["v0"], t["v1"], t["v2"]
                nrm = t["nrm"]
                uv0, uv1, uv2 = t["uv0"], t["uv1"], t["uv2"]
                v_strs.append(f"{v0[0]:.3f},{v0[1]:.3f},{v0[2]:.3f},{v1[0]:.3f},{v1[1]:.3f},{v1[2]:.3f},{v2[0]:.3f},{v2[1]:.3f},{v2[2]:.3f}")
                i_strs.append(f"{vi},{vi+1},{-(vi+3)}")
                n_strs.append(f"{nrm[0]:.3f},{nrm[1]:.3f},{nrm[2]:.3f},{nrm[0]:.3f},{nrm[1]:.3f},{nrm[2]:.3f},{nrm[0]:.3f},{nrm[1]:.3f},{nrm[2]:.3f}")
                uv_strs.append(f"{uv0[0]:.4f},{uv0[1]:.4f},{uv1[0]:.4f},{uv1[1]:.4f},{uv2[0]:.4f},{uv2[1]:.4f}")
                m_strs.append(str(MAT_INDEX[t["mat"]]))
                vi += 3
            ff.write(f"\t\tVertices: *{n_v * 3} {{\n\t\t\ta: " + ",".join(v_strs) + "\n\t\t}\n")
            ff.write(f"\t\tPolygonVertexIndex: *{n_v} {{\n\t\t\ta: " + ",".join(i_strs) + "\n\t\t}\n")
            ff.write('\t\tLayerElementNormal: 0 {\n\t\t\tVersion: 101\n\t\t\tMappingInformationType: "ByPolygonVertex"\n\t\t\tReferenceInformationType: "Direct"\n')
            ff.write(f"\t\t\tNormals: *{n_v * 3} {{\n\t\t\t\ta: " + ",".join(n_strs) + "\n\t\t\t}\n\t\t}\n")
            ff.write('\t\tLayerElementUV: 0 {\n\t\t\tVersion: 101\n\t\t\tMappingInformationType: "ByPolygonVertex"\n\t\t\tReferenceInformationType: "Direct"\n')
            ff.write(f"\t\t\tUV: *{n_v * 2} {{\n\t\t\t\ta: " + ",".join(uv_strs) + "\n\t\t\t}\n\t\t}\n")
            ff.write('\t\tLayerElementMaterial: 0 {\n\t\t\tVersion: 101\n\t\t\tMappingInformationType: "ByPolygon"\n\t\t\tReferenceInformationType: "IndexToDirect"\n')
            ff.write(f"\t\t\tMaterials: *{len(gtris)} {{\n\t\t\t\ta: " + ",".join(m_strs) + "\n\t\t\t}\n\t\t}\n")
            ff.write("\t}\n")
            ff.write(f'\tModel: {model_id}, "Model::{gname}", "Mesh" {{\n\t\tVersion: 232\n\t}}\n')
        ff.write("}\n")
        ff.write("Connections:  {\n")
        for g_idx in range(len(tris_by_group)):
            geom_id = 100000 + g_idx
            model_id = 200000 + g_idx
            ff.write(f'\tC: "OO",{model_id},0\n')
            ff.write(f'\tC: "OO",{geom_id},{model_id}\n')
            for m_idx in range(len(MATERIALS)):
                ff.write(f'\tC: "OO",{300000 + m_idx},{model_id}\n')
        ff.write("}\n")


def run_production_export():
    for d in (PKG_DIR, SCRIPT_DIR, MESH_DIR, ARCH_DIR, SECT_DIR, TEX_DIR):
        os.makedirs(d, exist_ok=True)
    atlas_path = os.path.join(TEX_DIR, "T_Colosseum_Production_Atlas_512.png")
    generate_production_atlas_512(atlas_path)

    scene_builder, archetype_builders, instance_manifest = build_production_colosseum()

    section_groups = OrderedDict()
    base_group_counts = OrderedDict([(g, 0) for g in scene_builder.groups])
    for t in scene_builder.tris:
        sec_name = assign_section_submesh_name(t)
        section_groups.setdefault(sec_name, []).append(t)
        base_group_counts[t["group"]] = base_group_counts.get(t["group"], 0) + 1

    # Export 5 Reusable Archetype Meshes in `meshes/archetypes/`
    archetype_summary = OrderedDict()
    instance_counts = {
        "UMOD_01_Standard_Window_Bay": 12,
        "UMOD_02_Standard_Clipeus_Bay": 20,
        "UMOD_03_Vomitorium_Cavea_Bay": 8,
        "UMOD_04_Cardinal_Triumphal_Gate_Pavilion": 4,
        "UMOD_05_North_Imperial_Reactor_Crest": 1,
    }
    for arch_id, ab in archetype_builders.items():
        arch_tris_dict = OrderedDict([(arch_id, ab.tris)])
        mtl_name = f"{arch_id}.mtl"
        write_mtl_file(os.path.join(ARCH_DIR, mtl_name), "../../textures/T_Colosseum_Production_Atlas_512.png")
        export_obj_with_uvs_and_normals(arch_tris_dict, os.path.join(ARCH_DIR, f"{arch_id}.obj"), mtl_name)
        export_glb_and_gltf(arch_tris_dict, os.path.join(ARCH_DIR, f"{arch_id}.glb"))
        export_fbx_ascii(arch_tris_dict, os.path.join(ARCH_DIR, f"{arch_id}.fbx"))

        xs = [p[0] for t in ab.tris for p in (t["v0"], t["v1"], t["v2"])]
        ys = [p[1] for t in ab.tris for p in (t["v0"], t["v1"], t["v2"])]
        zs = [p[2] for t in ab.tris for p in (t["v0"], t["v1"], t["v2"])]
        u_tris = len(ab.tris)
        inst_c = instance_counts[arch_id]
        archetype_summary[arch_id] = {
            "unique_triangles": u_tris,
            "unique_vertices": u_tris * 3,
            "instances_in_full_colosseum": inst_c,
            "instantiated_triangles_total": u_tris * inst_c,
            "local_bbox_min": [round(min(xs), 4), round(min(ys), 4), round(min(zs), 4)],
            "local_bbox_max": [round(max(xs), 4), round(max(ys), 4), round(max(zs), 4)],
            "under_20k_limit": u_tris < 20000,
        }

    with open(os.path.join(ARCH_DIR, "archetype_instance_transforms.json"), "w", encoding="utf-8") as f:
        json.dump({
            "asset_id": "SM_ArenaEnvironment_Colosseum_01",
            "world_origin": [0.0, 0.0, 0.0],
            "total_instances": len(instance_manifest),
            "instances": instance_manifest,
        }, f, indent=2)

    # Export Individual Section MeshParts in `meshes/sections/` (every single file < 20,000 tris)
    section_summary = OrderedDict()
    for sec_name, stris in section_groups.items():
        sec_dict = OrderedDict([(sec_name, stris)])
        mtl_name = f"{sec_name}.mtl"
        write_mtl_file(os.path.join(SECT_DIR, mtl_name), "../../textures/T_Colosseum_Production_Atlas_512.png")
        export_obj_with_uvs_and_normals(sec_dict, os.path.join(SECT_DIR, f"{sec_name}.obj"), mtl_name)
        export_glb_and_gltf(sec_dict, os.path.join(SECT_DIR, f"{sec_name}.glb"))
        s_xs = [p[0] for t in stris for p in (t["v0"], t["v1"], t["v2"])]
        s_ys = [p[1] for t in stris for p in (t["v0"], t["v1"], t["v2"])]
        s_zs = [p[2] for t in stris for p in (t["v0"], t["v1"], t["v2"])]
        section_summary[sec_name] = {
            "triangles": len(stris),
            "vertices": len(stris) * 3,
            "world_pivot": [0.0, 0.0, 0.0],
            "bbox_min": [round(min(s_xs), 4), round(min(s_ys), 4), round(min(s_zs), 4)],
            "bbox_max": [round(max(s_xs), 4), round(max(s_ys), 4), round(max(s_zs), 4)],
            "under_20k_limit": len(stris) < 20000,
        }

    # Export Complete Assembled Environment (`meshes/SM_ArenaEnvironment_Colosseum_01.*`)
    main_mtl = "SM_ArenaEnvironment_Colosseum_01.mtl"
    write_mtl_file(os.path.join(MESH_DIR, main_mtl), "../textures/T_Colosseum_Production_Atlas_512.png")
    export_obj_with_uvs_and_normals(section_groups, os.path.join(MESH_DIR, "SM_ArenaEnvironment_Colosseum_01.obj"), main_mtl)
    export_glb_and_gltf(
        section_groups,
        os.path.join(MESH_DIR, "SM_ArenaEnvironment_Colosseum_01.glb"),
        gltf_path=os.path.join(MESH_DIR, "SM_ArenaEnvironment_Colosseum_01.gltf"),
        bin_path=os.path.join(MESH_DIR, "SM_ArenaEnvironment_Colosseum_01.bin"),
        rel_tex_uri="../textures/T_Colosseum_Production_Atlas_512.png"
    )
    export_fbx_ascii(section_groups, os.path.join(MESH_DIR, "SM_ArenaEnvironment_Colosseum_01.fbx"))

    # Compute Exact Spatial, Material, and Void-Clearance Metrics
    xs_all, ys_all, zs_all = [], [], []
    mat_area = {k: 0.0 for k in MATERIALS}
    for t in scene_builder.tris:
        v0, v1, v2 = t["v0"], t["v1"], t["v2"]
        ux, uy, uz = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
        vx, vy, vz = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]
        cx = uy * vz - uz * vy
        cy = uz * vx - ux * vz
        cz = ux * vy - uy * vx
        area = 0.5 * math.sqrt(cx * cx + cy * cy + cz * cz)
        mat_area[t["mat"]] += area
        for p in (v0, v1, v2):
            xs_all.append(p[0])
            ys_all.append(p[1])
            zs_all.append(p[2])

    xs_a = np.array(xs_all, dtype=np.float64)
    ys_a = np.array(ys_all, dtype=np.float64)
    zs_a = np.array(zs_all, dtype=np.float64)
    r_a = np.hypot(xs_a, zs_a)
    ell_norm = np.sqrt((xs_a / RX_IN) ** 2 + (zs_a / RZ_IN) ** 2)
    intruding_verts = int(np.sum(ell_norm < 0.9999))

    corner_clearances = []
    for cx_g, cz_g in [(-54.0, -54.0), (54.0, -54.0), (54.0, 54.0), (-54.0, 54.0)]:
        corner_clearances.append(float(np.hypot(xs_a - cx_g, zs_a - cz_g).min()))

    tot_area = sum(mat_area.values())
    mat_pct = {k: round(100.0 * v / tot_area, 2) for k, v in mat_area.items() if v > 0.0}

    unique_sum = sum(v["unique_triangles"] for v in archetype_summary.values())
    inst_sum = sum(v["instantiated_triangles_total"] for v in archetype_summary.values())
    total_scene_tris = len(scene_builder.tris)
    assert inst_sum == total_scene_tris, f"Mismatch: inst_sum={inst_sum} vs total_scene_tris={total_scene_tris}"

    metrics = {
        "asset_id": "SM_ArenaEnvironment_Colosseum_01",
        "phase": "Phase 2 — Final High-Detail Production Kit",
        "approved_concept_02_zip_sha256": APPROVED_CONCEPT_02_ZIP_SHA256,
        "blender_binary_status": "NOT GENERATED — BLENDER UNAVAILABLE",
        "scale_convention": "1 Blender unit = 1 Roblox stud",
        "world_origin": [0.0, 0.0, 0.0],
        "locked_arena_grid": {
            "center": [0.0, 50.0, 0.0],
            "grid_cells": [9, 9],
            "tile_count": 81,
            "tile_pitch_studs": 12.0,
            "footprint_studs": [108.0, 108.0],
            "visual_tile_studs": [11.8, 2.0, 11.8],
            "collision_tile_studs": [12.0, 2.0, 12.0],
            "top_surface_world_y": 51.0,
            "sphere_diameter_studs": 6.0,
            "void_elimination_threshold_world_y": 15.0,
            "grid_corner_radius_studs": round(ARENA_CORNER_RADIUS, 4),
        },
        "previous_concept_02_triangles": 186588,
        "total_unique_archetype_triangles": unique_sum,
        "total_instantiated_scene_triangles": total_scene_tris,
        "total_instantiated_scene_vertices": total_scene_tris * 3,
        "additional_connector_or_trim_triangles": 0,
        "archetypes": archetype_summary,
        "base_architecture_groups": base_group_counts,
        "import_safe_section_meshparts_count": len(section_summary),
        "max_section_meshpart_triangles": max(v["triangles"] for v in section_summary.values()),
        "all_section_meshparts_under_20k": all(v["under_20k_limit"] for v in section_summary.values()),
        "section_meshparts": section_summary,
        "world_bbox_min": [round(float(xs_a.min()), 4), round(float(ys_a.min()), 4), round(float(zs_a.min()), 4)],
        "world_bbox_max": [round(float(xs_a.max()), 4), round(float(ys_a.max()), 4), round(float(zs_a.max()), 4)],
        "world_dimensions_studs": [
            round(float(xs_a.max() - xs_a.min()), 4),
            round(float(ys_a.max() - ys_a.min()), 4),
            round(float(zs_a.max() - zs_a.min()), 4),
        ],
        "inner_ellipse_axes_studs": {"rx": RX_IN, "rz": RZ_IN},
        "outer_ellipse_axes_studs": {"rx": RX_OUT, "rz": RZ_OUT},
        "radial_min_studs": round(float(r_a.min()), 4),
        "radial_max_studs": round(float(r_a.max()), 4),
        "clearances_to_locked_108x108_grid_studs": {
            "cardinal_east_west_x_gap": 44.0,
            "cardinal_north_south_z_gap": 50.0,
            "diagonal_45deg_radial_gap": round(100.8669 - ARENA_CORNER_RADIUS, 4),
            "min_euclidean_distance_from_grid_corners": round(min(corner_clearances), 4),
            "vertices_intruding_into_inner_ellipse": intruding_verts,
            "lowest_y_above_void_threshold_y15": round(float(ys_a.min() - VOID_ELIMINATION_Y), 4),
        },
        "material_area_sq_studs": {k: round(v, 2) for k, v in mat_area.items() if v > 0.0},
        "material_area_pct": mat_pct,
        "emissive_total_pct": round(mat_pct.get("EMI_Cyan", 0.0) + mat_pct.get("EMI_Amber", 0.0), 2),
        "texture_atlas": {
            "path": "textures/T_Colosseum_Production_Atlas_512.png",
            "resolution": [512, 512],
        },
    }

    metrics_path = os.path.join(SCRIPT_DIR, "colosseum_production_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as mf:
        json.dump(metrics, mf, indent=2)

    return scene_builder, archetype_builders, section_groups, metrics


if __name__ == "__main__":
    print("Generating Phase 2 High-Detail Roman Colosseum Production Kit...")
    _, _, _, m = run_production_export()
    print(json.dumps({
        "previous_concept_02_triangles": m["previous_concept_02_triangles"],
        "total_unique_archetype_triangles": m["total_unique_archetype_triangles"],
        "total_instantiated_scene_triangles": m["total_instantiated_scene_triangles"],
        "additional_connector_or_trim_triangles": m["additional_connector_or_trim_triangles"],
        "archetypes": {k: {"unique_tris": v["unique_triangles"], "instances": v["instances_in_full_colosseum"], "instantiated_tris": v["instantiated_triangles_total"]} for k, v in m["archetypes"].items()},
        "base_architecture_groups": m["base_architecture_groups"],
        "import_safe_section_meshparts_count": m["import_safe_section_meshparts_count"],
        "max_section_meshpart_triangles": m["max_section_meshpart_triangles"],
        "all_section_meshparts_under_20k": m["all_section_meshparts_under_20k"],
        "world_bbox_min": m["world_bbox_min"],
        "world_bbox_max": m["world_bbox_max"],
        "radial_min_studs": m["radial_min_studs"],
        "radial_max_studs": m["radial_max_studs"],
        "clearances": m["clearances_to_locked_108x108_grid_studs"],
        "emissive_total_pct": m["emissive_total_pct"],
    }, indent=2))
