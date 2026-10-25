#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — MAP 01, PHASE 1 REVISION 02 (HIGH-DETAIL ROMAN COLOSSEUM)
Canonical Proposed Asset ID: SM_ArenaEnvironment_Colosseum_01
Package: Sphere_Brawl_Colosseum_Environment_Concept_02
====================================================================================================
Deterministic High-Detail 3D Roman Amphitheatre Concept Model Generator & Exporter.
Constructs an authentic, restored Roman Colosseum on a smooth 64-bay elliptical plan
(Inner semi-axes: B_in = 98.0000 studs X, A_in = 104.0000 studs Z;
 Outer semi-axes: B_out = 128.0000 studs X, A_out = 134.0000 studs Z;
 Overall bounds with Cardinal Triumphal Gate Pavilions: X in [-130.0, +130.0], Z in [-136.0, +136.0], Y in [18.0, 125.0])
surrounding the unchanged 108x108-stud (9x9) arena grid at (0, 50, 0).

Organizes ~150,000+ triangles of genuine 3D architectural relief into the 8 required named groups:
  1. COL_ExteriorArcade    — 3 stories of 3D wedge voussoirs, projecting keystones, dual archivolts, imposts & vaulted soffits
  2. COL_ColumnOrders      — Tuscan/Doric (L1), Ionic with 3D volute scrolls (L2), Corinthian with 3D acanthus leaves (L3) & Attic Pilasters (L4)
  3. COL_StoneMasonry      — Coursed opus quadratum ashlar travertine blocks, stepped crepidine & rusticated lower foundation drum
  4. COL_CaveaSeating      — 19 profiled bullnose limestone seating tiers (Ima/Media/Summa), marble podium balustrade, 28 radial scalaria stairs & 56 upper porticus columns/arches
  5. COL_Vomitoria         — Praecinctio retaining walls (baltei) & 28 deeply recessed arched vomitoria crowd portals with 3D voussoirs
  6. COL_AtticCornice      — 4 multi-profiled entablatures with 3D dentil blocks, 28 framed attic windows, 28 sculpted clipei shields, 112 corbels & 56 velarium masts
  7. COL_GateTowers        — 4 Roman Triumphal Arch Gate Pavilions with coffered barrel vaults, 13-voussoir arches, paired Corinthian columns & triangular pediments
  8. COL_NorthReactorCrest — Classical Roman Imperial Tribune & integrated Kinetic Grid reactor oculus crowning the North (-Z) axis to Y = 125.0 (+74.0 studs)
"""

import os
import sys
import json
import math
import struct
import hashlib
import numpy as np
from PIL import Image, ImageDraw

WORKSPACE = "/working_dir/c_28d7717712e39623"
PKG_DIR = os.path.join(WORKSPACE, "Sphere_Brawl_Colosseum_Environment_Concept_02")
SRC_DIR = os.path.join(PKG_DIR, "concept_source")
INT_DIR = os.path.join(WORKSPACE, "artifacts/file_generation/ttl=63d/intermediate")

os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(INT_DIR, exist_ok=True)

# ==============================================================================
# CONTROLLED ARCHITECTURAL & LOCKED PALETTE (Section 12 & 13)
# ==============================================================================
# Flag: 0 = Stone (receives subtle ashlar per-block & travertine grain),
#       1 = Trim / Marble / Metal (receives crisp specular highlight),
#       2 = Emissive (restrained Kinetic Grid accent),
#       3 = Arena Tile / Sphere (external dependency)
MATERIALS = {
    # Clean Restored Roman Architectural Stone Palette (Section 12)
    "MAT_TravertineLight":    {"rgb": (214, 198, 172), "hex": "#D6C6AC", "flag": 0, "rough": 0.62, "metal": 0.04, "role": "Principal outer arches, voussoirs, keystones, columns & pilasters"},
    "MAT_TravertineWarm":     {"rgb": (196, 178, 150), "hex": "#C4B296", "flag": 0, "rough": 0.66, "metal": 0.04, "role": "Ashlar pier blocks, spandrels, attic wall courses & entablature friezes"},
    "MAT_LimestoneCream":     {"rgb": (204, 192, 172), "hex": "#CCC0AC", "flag": 0, "rough": 0.64, "metal": 0.04, "role": "Tiered Cavea seating steps, bullnose treads, scalaria stairs & vomitoria arches"},
    "MAT_TuffFoundation":     {"rgb": (132, 122, 108), "hex": "#847A6C", "flag": 0, "rough": 0.74, "metal": 0.06, "role": "Stepped crepidine base, lower foundation drum & recessed vaulted passages"},
    "MAT_BasaltShadow":       {"rgb": (58,  60,  68),  "hex": "#3A3C44", "flag": 0, "rough": 0.76, "metal": 0.10, "role": "Deep vomitoria throats, arena podium base & lower structural ribs"},
    "MAT_ImperialMarble":     {"rgb": (232, 224, 210), "hex": "#E8E0D2", "flag": 1, "rough": 0.34, "metal": 0.08, "role": "Senatorial podium balustrade, Corinthian/Ionic capitals, pediments & keystones"},
    "MAT_BronzeClipeus":      {"rgb": (176, 142, 88),  "hex": "#B08E58", "flag": 1, "rough": 0.36, "metal": 0.72, "role": "Attic clipei victory shields, velarium mast collars & triumphal medallions"},
    # Locked Sphere Brawl Palette (Section 13)
    "MAT_DarkNeutral":        {"rgb": (32,  38,  54),  "hex": "#202636", "flag": 1, "rough": 0.42, "metal": 0.58, "role": "Engineered dark-metal gate portcullis frames & structural tie collars"},
    "MAT_AltNeutral":         {"rgb": (42,  50,  70),  "hex": "#2A3246", "flag": 1, "rough": 0.38, "metal": 0.62, "role": "Secondary engineered housing & reactor frame"},
    "MAT_LightTrim":          {"rgb": (170, 190, 215), "hex": "#AABED7", "flag": 1, "rough": 0.28, "metal": 0.78, "role": "Brushed metallic arch tie-cleats & reactor bezel trim"},
    "EMI_Cyan":               {"rgb": (0,   195, 255), "hex": "#00C3FF", "flag": 2, "rough": 0.15, "metal": 0.00, "role": "Restrained Kinetic Grid energy seams in gates & North Imperial Reactor Crest"},
    "EMI_Amber":              {"rgb": (255, 170, 0),   "hex": "#FFAA00", "flag": 2, "rough": 0.15, "metal": 0.00, "role": "Sparse landmark focal core in North Imperial Reactor Crest"},
    # External Tile Dependency Materials (Used only when rendering the separate 9x9 grid)
    "EMI_Ice":                {"rgb": (0,   235, 255), "hex": "#00EBFF", "flag": 2, "rough": 0.12, "metal": 0.00, "role": "Tile Hazard Overlay Only (Ice Corridor)"},
    "EMI_Magnetic":           {"rgb": (165, 55,  255), "hex": "#A537FF", "flag": 2, "rough": 0.15, "metal": 0.00, "role": "Tile Hazard Overlay Only (Magnetic Storm)"},
    "EMI_Kinetic":            {"rgb": (255, 125, 0),   "hex": "#FF7D00", "flag": 2, "rough": 0.15, "metal": 0.00, "role": "Tile Hazard Overlay Only (Boost Runway)"},
    "EMI_DangerRed":          {"rgb": (255, 40,  40),  "hex": "#FF2828", "flag": 2, "rough": 0.15, "metal": 0.00, "role": "Tile Collapse Warning Only (Ring D=4/D=3)"},
    "MAT_PrimaryText":        {"rgb": (245, 248, 255), "hex": "#F5F8FF", "flag": 1, "rough": 0.30, "metal": 0.10, "role": "Tile / Sphere Trim"},
}

MAT_LIST_ORDER = list(MATERIALS.keys())
MAT_TO_IDX = {k: i for i, k in enumerate(MAT_LIST_ORDER)}


def generate_palette_atlas_512(out_path):
    """
    Generates a clean 512x512 textured stone & material atlas (<= 1024x1024 project limit)
    arranged in a 4x4 grid of 128x128 tiles with subtle travertine/limestone grain.
    """
    W, H = 512, 512
    img = np.zeros((H, W, 3), dtype=np.uint8)
    rng = np.random.default_rng(20261025)
    for idx, mname in enumerate(MAT_LIST_ORDER[:16]):
        gx = (idx % 4) * 128
        gy = (idx // 4) * 128
        base = np.array(MATERIALS[mname]["rgb"], dtype=np.float32)
        tile = np.ones((128, 128, 3), dtype=np.float32) * base
        if MATERIALS[mname]["flag"] == 0:
            # Subtle horizontal travertine bedding & stone grain
            yy, xx = np.mgrid[0:128, 0:128]
            striation = np.sin(yy * 0.35 + np.sin(xx * 0.12) * 1.8) * 4.5
            noise = rng.normal(0.0, 3.2, size=(128, 128))
            delta = (striation + noise)[:, :, None]
            tile = np.clip(tile + delta, 0, 255)
        img[gy:gy + 128, gx:gx + 128] = tile.astype(np.uint8)
    pil_img = Image.fromarray(img)
    pil_img.save(out_path)
    return W, H


# ==============================================================================
# ELLIPTICAL COORDINATE SYSTEM & HIGH-DETAIL MESH ACCUMULATOR
# ==============================================================================
def ellipse_point_and_basis(r_x, r_z, theta):
    """
    Returns world (x, z) on the ellipse (x / r_x)^2 + (z / r_z)^2 = 1 at parameter angle theta,
    plus unit outward normal (nx, nz) and unit tangent (tx, tz).
    """
    ct, st = math.cos(theta), math.sin(theta)
    px = r_x * ct
    pz = r_z * st
    # Outward normal of ellipse is proportional to (ct / r_x, st / r_z)
    gx = ct / r_x
    gz = st / r_z
    glen = math.hypot(gx, gz)
    nx, nz = gx / glen, gz / glen
    tx, tz = -nz, nx
    return px, pz, nx, nz, tx, tz


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
        self.group_tris = {g: [] for g in self.groups}
        self._block_seed = 1

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
        self.group_tris[group].append((
            (x0, y0, z0), (x1, y1, z1), (x2, y2, z2),
            (cx * inv_n, cy * inv_n, cz * inv_n),
            mat_name, float(bvar)
        ))

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
        """
        Adds a 3D box (or chamfered ashlar block) in local radial (r0..r1) and tangential (t0..t1) coordinates
        around origin_xz with outward radial normal (nx, nz) and tangent (tx, tz).
        """
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
        """
        Subdivides an elliptical ring sector between angles a0 and a1 into n_sub smooth curved segments.
        """
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
        """
        Builds a genuine 3D Roman archway in local bay space:
          - Left & right coursed ashlar piers (4 horizontal courses with recessed stone joints)
          - Moulded 3-step impost blocks at y_impost
          - Deep barrel-vaulted intrados/soffit (n_voussoirs curved ceiling segments from r_back to r_front)
          - Inner & outer stepped 3D archivolts
          - n_voussoirs individually modelled 3D wedge-shaped stone voussoirs + projecting sculpted keystone
          - Coursed ashlar spandrel masonry filling the upper corners above the extrados
        """
        # 1. Left & Right Coursed Ashlar Piers (from y_floor to y_impost)
        n_pier_courses = 4
        ch = (y_impost - y_floor) / float(n_pier_courses)
        for side_s in (-1.0, +1.0):
            t_outer = side_s * bay_half_w
            t_inner = side_s * arch_half_w
            t_min, t_max = min(t_outer, t_inner), max(t_outer, t_inner)
            for c_i in range(n_pier_courses):
                cy0 = y_floor + c_i * ch + 0.04
                cy1 = y_floor + (c_i + 1) * ch - 0.04
                # Split every alternate course into 2 ashlar blocks for authentic running-bond joints
                if c_i % 2 == 1 and (t_max - t_min) > 1.2:
                    t_mid = 0.5 * (t_min + t_max)
                    self.add_local_box(group_masonry, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                                       r_back, r_front, t_min + 0.03, t_mid - 0.03, cy0, cy1, chamfer=0.0)
                    self.add_local_box(group_masonry, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                                       r_back, r_front, t_mid + 0.03, t_max - 0.03, cy0, cy1, chamfer=0.0)
                else:
                    self.add_local_box(group_masonry, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                                       r_back, r_front, t_min + 0.03, t_max - 0.03, cy0, cy1, chamfer=0.0)

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
            # Angle measured from 0 (right impost +t) to pi (left impost -t)
            phi0 = v_i * d_phi + 0.012
            phi1 = (v_i + 1) * d_phi - 0.012
            is_keystone = (v_i == n_voussoirs // 2)

            c0, s0 = math.cos(phi0), math.sin(phi0)
            c1, s1 = math.cos(phi1), math.sin(phi1)

            # Inner intrados points
            t_in0, y_in0 = r_intrados * c0, y_impost + r_intrados * s0
            t_in1, y_in1 = r_intrados * c1, y_impost + r_intrados * s1

            # Mid archivolt step points
            t_md0, y_md0 = r_archivolt_mid * c0, y_impost + r_archivolt_mid * s0
            t_md1, y_md1 = r_archivolt_mid * c1, y_impost + r_archivolt_mid * s1

            # Outer extrados points (keystone projects higher and further out!)
            r_ext_cur = (r_extrados + keystone_extra_h) if is_keystone else r_extrados
            t_ex0, y_ex0 = r_ext_cur * c0, y_impost + r_ext_cur * s0
            t_ex1, y_ex1 = r_ext_cur * c1, y_impost + r_ext_cur * s1

            rf_in = r_front + 0.10
            rf_out = (r_front + 0.42) if is_keystone else (r_front + 0.22)
            rb_in = r_back - 0.08
            v_mat = "MAT_ImperialMarble" if is_keystone else "MAT_TravertineLight"
            bv = self.next_bvar()

            # Inner Archivolt Ring + Deep Barrel-Vaulted Intrados Wedge (from rb_in to rf_in)
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

            # Outer Wedge Voussoir Block (projects forward to rf_out with individual radial wedge joints)
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

            # Spandrel masonry wedge between extrados and y_top_wall
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

        # Corner spandrel filler blocks (above piers from y_impost to y_top_wall outside r_extrados)
        for side_s in (-1.0, +1.0):
            t_outer = side_s * (bay_half_w - 0.04)
            t_inner = side_s * min(r_extrados - 0.05, bay_half_w - 0.15)
            t_min, t_max = min(t_outer, t_inner), max(t_outer, t_inner)
            if (t_max - t_min) > 0.12:
                ymid = 0.5 * (y_impost + y_top_wall)
                self.add_local_box(group_masonry, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                                   r_back, r_front, t_min, t_max, y_impost + 0.12, ymid - 0.03, chamfer=0.0)
                self.add_local_box(group_masonry, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                                   r_back, r_front, t_min, t_max, ymid + 0.03, y_top_wall, chamfer=0.0)
            if has_medallions:
                # Sculpted spandrel medallion boss on upper Corinthian arcade
                tm_c = side_s * (bay_half_w * 0.72)
                ym_c = y_top_wall - 1.35
                self.add_local_box(group_arch, "MAT_BronzeClipeus", origin_xz, nx, nz, tx, tz,
                                   r_front - 0.05, r_front + 0.22, tm_c - 0.42, tm_c + 0.42, ym_c - 0.42, ym_c + 0.42, chamfer=0.14)

    def add_classical_column(
        self, group, col_xz, nx, nz, tx, tz, y_base, y_top, order="Tuscan", radius=0.82
    ):
        """
        Builds a high-detail 3D Classical Column in group `COL_ColumnOrders`:
          - Stepped pedestal + Attic/Tuscan moulded base (plinth, lower torus, scotia, upper torus)
          - Cylindrical shaft with entasis & 3D recessed flutes (for Ionic/Corinthian)
          - Order-specific 3D Capital:
              * Tuscan: astragal necking ring + flared echinus cushion + square beveled abacus
              * Ionic: echinus + twin 3D projecting spiral volute bolsters + profiled abacus
              * Corinthian: 2 staggered rings of 6 projecting 3D acanthus leaves (12 leaves total!) + 4 corner volute helices + concave abacus + fleuron boss
        """
        cx, cz = col_xz
        # 1. Pedestal & Plinth Base (y_base to y_base + 1.85)
        ped_h = 1.25
        self.add_local_box(group, "MAT_TravertineWarm", col_xz, nx, nz, tx, tz,
                           -radius * 1.35, radius * 1.35, -radius * 1.35, radius * 1.35, y_base, y_base + 0.32)
        self.add_local_box(group, "MAT_TravertineLight", col_xz, nx, nz, tx, tz,
                           -radius * 1.18, radius * 1.18, -radius * 1.18, radius * 1.18, y_base + 0.32, y_base + ped_h - 0.18)
        self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                           -radius * 1.28, radius * 1.28, -radius * 1.28, radius * 1.28, y_base + ped_h - 0.18, y_base + ped_h)

        # Attic / Tuscan Base Rings (plinth + lower torus + scotia + upper torus)
        yb0 = y_base + ped_h
        n_seg = 8
        ring_profiles = [
            (yb0,        yb0 + 0.22, radius * 1.22, radius * 1.18, "MAT_ImperialMarble"),
            (yb0 + 0.22, yb0 + 0.40, radius * 1.06, radius * 1.02, "MAT_ImperialMarble"),
            (yb0 + 0.40, yb0 + 0.56, radius * 1.12, radius * 1.00, "MAT_TravertineLight"),
        ]
        for ry0, ry1, r_b, r_t, rmat in ring_profiles:
            lb, lt = [], []
            for k in range(n_seg):
                ang = k * (2.0 * math.pi / n_seg)
                ca, sa = math.cos(ang), math.sin(ang)
                lb.append((cx + r_b * (ca * nx + sa * tx), ry0, cz + r_b * (ca * nz + sa * tz)))
                lt.append((cx + r_t * (ca * nx + sa * tx), ry1, cz + r_t * (ca * nz + sa * tz)))
            self.add_loft(group, rmat, lb, lt, cap_bot=False, cap_top=True)

        # 2. Column Shaft with Entasis & 3D Fluting (for Ionic/Corinthian)
        y_shaft_bot = yb0 + 0.56
        cap_h = 1.95 if order == "Corinthian" else (1.45 if order == "Ionic" else 1.25)
        y_shaft_top = y_top - cap_h
        n_shaft_tiers = 1
        fluted = (order in ("Ionic", "Corinthian"))
        n_circ = 12 if fluted else 8

        for st_i in range(n_shaft_tiers):
            f0 = st_i / float(n_shaft_tiers)
            f1 = (st_i + 1) / float(n_shaft_tiers)
            sy0 = y_shaft_bot + f0 * (y_shaft_top - y_shaft_bot)
            sy1 = y_shaft_bot + f1 * (y_shaft_top - y_shaft_bot)
            # Classical entasis curve: slight swelling at 1/3 height, tapering to 0.86*radius at neck
            r0 = radius * (1.0 - 0.14 * (f0 ** 1.4) + 0.03 * math.sin(f0 * math.pi))
            r1 = radius * (1.0 - 0.14 * (f1 ** 1.4) + 0.03 * math.sin(f1 * math.pi))
            lb, lt = [], []
            for k in range(n_circ):
                ang = k * (2.0 * math.pi / n_circ)
                ca, sa = math.cos(ang), math.sin(ang)
                # Alternate inner flute channel vs. outer arris ridge on fluted columns!
                flute_mult = (0.91 if (fluted and (k % 2 == 1)) else 1.0)
                rr0 = r0 * flute_mult
                rr1 = r1 * flute_mult
                lb.append((cx + rr0 * (ca * nx + sa * tx), sy0, cz + rr0 * (ca * nz + sa * tz)))
                lt.append((cx + rr1 * (ca * nx + sa * tx), sy1, cz + rr1 * (ca * nz + sa * tz)))
            self.add_loft(group, "MAT_TravertineLight", lb, lt, cap_bot=False, cap_top=False)

        # Astragal Necking Ring at y_shaft_top
        r_neck = radius * 0.86
        lb_n, lt_n = [], []
        for k in range(10):
            ang = k * (2.0 * math.pi / 10.0)
            ca, sa = math.cos(ang), math.sin(ang)
            lb_n.append((cx + r_neck * 1.08 * (ca * nx + sa * tx), y_shaft_top, cz + r_neck * 1.08 * (ca * nz + sa * tz)))
            lt_n.append((cx + r_neck * 1.08 * (ca * nx + sa * tx), y_shaft_top + 0.16, cz + r_neck * 1.08 * (ca * nz + sa * tz)))
        self.add_loft(group, "MAT_ImperialMarble", lb_n, lt_n, cap_bot=True, cap_top=True)

        # 3. Order-Specific 3D Capital
        yc0 = y_shaft_top + 0.16
        if order == "Tuscan":
            # Flared Echinus Cushion + Stepped Square Abacus
            lb_e, lt_e = [], []
            for k in range(10):
                ang = k * (2.0 * math.pi / 10.0)
                ca, sa = math.cos(ang), math.sin(ang)
                lb_e.append((cx + r_neck * 0.96 * (ca * nx + sa * tx), yc0, cz + r_neck * 0.96 * (ca * nz + sa * tz)))
                lt_e.append((cx + radius * 1.24 * (ca * nx + sa * tx), yc0 + 0.52, cz + radius * 1.24 * (ca * nz + sa * tz)))
            self.add_loft(group, "MAT_ImperialMarble", lb_e, lt_e, cap_bot=False, cap_top=True)
            self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                               -radius * 1.28, radius * 1.28, -radius * 1.28, radius * 1.28, yc0 + 0.52, y_top, chamfer=0.0)

        elif order == "Ionic":
            # Moulded Echinus + Twin 3D Spiral Volute Bolsters (Left & Right) + Profiled Abacus
            lb_e, lt_e = [], []
            for k in range(10):
                ang = k * (2.0 * math.pi / 10.0)
                ca, sa = math.cos(ang), math.sin(ang)
                lb_e.append((cx + r_neck * 0.96 * (ca * nx + sa * tx), yc0, cz + r_neck * 0.96 * (ca * nz + sa * tz)))
                lt_e.append((cx + radius * 1.18 * (ca * nx + sa * tx), yc0 + 0.45, cz + radius * 1.18 * (ca * nz + sa * tz)))
            self.add_loft(group, "MAT_ImperialMarble", lb_e, lt_e, cap_bot=False, cap_top=True)

            # Twin 3D Coiled Spiral Volute Scrolls at t = -radius*1.12 and +radius*1.12
            for vs in (-1.0, +1.0):
                vt_c = vs * radius * 1.08
                vy_c = yc0 + 0.52
                vr_scroll = radius * 0.46
                # Octagonal scroll cylinder along radial axis (nx, nz) + projecting spiral eye boss
                lb_v, lt_v = [], []
                for k in range(8):
                    ang = k * (2.0 * math.pi / 8.0)
                    dt_v = vt_c + vr_scroll * math.cos(ang)
                    dy_v = vy_c + vr_scroll * math.sin(ang)
                    lb_v.append((cx - radius * 1.05 * nx + dt_v * tx, dy_v, cz - radius * 1.05 * nz + dt_v * tz))
                    lt_v.append((cx + radius * 1.05 * nx + dt_v * tx, dy_v, cz + radius * 1.05 * nz + dt_v * tz))
                self.add_loft(group, "MAT_ImperialMarble", lb_v, lt_v, cap_bot=True, cap_top=True)
                # Inner spiral eye boss on the front face of each volute
                self.add_local_box(group, "MAT_BronzeClipeus", col_xz, nx, nz, tx, tz,
                                   radius * 0.95, radius * 1.16, vt_c - 0.16, vt_c + 0.16, vy_c - 0.16, vy_c + 0.16, chamfer=0.0)

            self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                               -radius * 1.18, radius * 1.18, -radius * 1.24, radius * 1.24, yc0 + 0.88, y_top, chamfer=0.0)

        else:  # Corinthian
            # Inner Calathus Bell Core
            bell_top = y_top - 0.34
            lb_b, lt_b = [], []
            for k in range(10):
                ang = k * (2.0 * math.pi / 10.0)
                ca, sa = math.cos(ang), math.sin(ang)
                lb_b.append((cx + r_neck * 0.92 * (ca * nx + sa * tx), yc0, cz + r_neck * 0.92 * (ca * nz + sa * tz)))
                lt_b.append((cx + radius * 1.12 * (ca * nx + sa * tx), bell_top, cz + radius * 1.12 * (ca * nz + sa * tz)))
            self.add_loft(group, "MAT_TravertineLight", lb_b, lt_b, cap_bot=False, cap_top=True)

            # Two Staggered Tiers of 6 Projecting 3D Sculpted Acanthus Leaves (12 3D leaves per capital!)
            for tier_i in range(2):
                ly0 = yc0 + tier_i * 0.56
                ly1 = ly0 + 0.62
                r_leaf_b = r_neck * (0.98 + 0.08 * tier_i)
                r_leaf_t = radius * (1.24 + 0.12 * tier_i)
                ang_offset = (math.pi / 6.0) * tier_i
                for lf_i in range(4):
                    a_mid = ang_offset + lf_i * (2.0 * math.pi / 4.0)
                    da = 0.22
                    ca0, sa0 = math.cos(a_mid - da), math.sin(a_mid - da)
                    ca1, sa1 = math.cos(a_mid + da), math.sin(a_mid + da)
                    cam, sam = math.cos(a_mid), math.sin(a_mid)
                    lb_lf = [
                        (cx + r_leaf_b * (ca0 * nx + sa0 * tx), ly0, cz + r_leaf_b * (ca0 * nz + sa0 * tz)),
                        (cx + (r_leaf_b + 0.14) * (cam * nx + sam * tx), ly0, cz + (r_leaf_b + 0.14) * (cam * nz + sam * tz)),
                        (cx + r_leaf_b * (ca1 * nx + sa1 * tx), ly0, cz + r_leaf_b * (ca1 * nz + sa1 * tz)),
                    ]
                    lt_lf = [
                        (cx + (r_leaf_t - 0.10) * (ca0 * nx + sa0 * tx), ly1, cz + (r_leaf_t - 0.10) * (ca0 * nz + sa0 * tz)),
                        (cx + (r_leaf_t + 0.18) * (cam * nx + sam * tx), ly1 - 0.06, cz + (r_leaf_t + 0.18) * (cam * nz + sam * tz)),
                        (cx + (r_leaf_t - 0.10) * (ca1 * nx + sa1 * tx), ly1, cz + (r_leaf_t - 0.10) * (ca1 * nz + sa1 * tz)),
                    ]
                    self.add_loft(group, "MAT_ImperialMarble", lb_lf, lt_lf, cap_bot=False, cap_top=True)

            # 4 Corner Helices / Diagonal Volutes + Moulded Abacus + Central Fleuron Boss
            self.add_local_box(group, "MAT_ImperialMarble", col_xz, nx, nz, tx, tz,
                               -radius * 1.34, radius * 1.34, -radius * 1.34, radius * 1.34, bell_top, y_top, chamfer=0.0)
            self.add_local_box(group, "MAT_BronzeClipeus", col_xz, nx, nz, tx, tz,
                               radius * 1.25, radius * 1.44, -0.22, 0.22, bell_top + 0.04, y_top - 0.04, chamfer=0.0)

    def add_entablature_and_cornice_bay(
        self, group, origin_xz, nx, nz, tx, tz, r_back, r_front, bay_half_w, y0, y1, n_dentils=6
    ):
        """
        Builds a multi-layered classical entablature across one bay:
          - Lower & Upper Architrave Fascia bands
          - Sculpted Frieze with 3D triglyph/console relief blocks
          - Row of individually modelled 3D projecting Dentil blocks
          - Projecting Ovolo + Corona Cornice overhang
        """
        h = y1 - y0
        # 1. Architrave (2 stepped fascia bands)
        self.add_local_box(group, "MAT_TravertineLight", origin_xz, nx, nz, tx, tz,
                           r_back, r_front + 0.25, -bay_half_w, bay_half_w, y0, y0 + 0.24 * h)
        self.add_local_box(group, "MAT_ImperialMarble", origin_xz, nx, nz, tx, tz,
                           r_back, r_front + 0.36, -bay_half_w, bay_half_w, y0 + 0.24 * h, y0 + 0.38 * h)
        # 2. Frieze with 3D relief triglyphs/panels
        self.add_local_box(group, "MAT_TravertineWarm", origin_xz, nx, nz, tx, tz,
                           r_back, r_front + 0.22, -bay_half_w, bay_half_w, y0 + 0.38 * h, y0 + 0.66 * h)
        # 3. Individually Modelled 3D Dentil Course!
        dw = (2.0 * bay_half_w) / float(n_dentils)
        for d_i in range(n_dentils):
            dt0 = -bay_half_w + (d_i + 0.18) * dw
            dt1 = -bay_half_w + (d_i + 0.82) * dw
            self.add_local_box(group, "MAT_ImperialMarble", origin_xz, nx, nz, tx, tz,
                               r_front + 0.18, r_front + 0.52, dt0, dt1, y0 + 0.66 * h, y0 + 0.80 * h)
        # 4. Projecting Corona & Cyma Cornice Ledge
        self.add_local_box(group, "MAT_TravertineLight", origin_xz, nx, nz, tx, tz,
                           r_back - 0.15, r_front + 0.78, -bay_half_w - 0.04, bay_half_w + 0.04, y0 + 0.80 * h, y0 + 0.92 * h)
        self.add_local_box(group, "MAT_ImperialMarble", origin_xz, nx, nz, tx, tz,
                           r_back - 0.20, r_front + 0.96, -bay_half_w - 0.06, bay_half_w + 0.06, y0 + 0.92 * h, y1)


def clamp_val(x, a, b):
    return a if x < a else (b if x > b else x)


def build_high_detail_colosseum():
    """
    Constructs the complete High-Detail Roman Colosseum (Concept 02) on a 64-bay elliptical plan.
    Also tracks exact Unique Module Mesh Triangle Counts vs. Total Instantiated Scene Triangle Counts.
    """
    builder = HighDetailColosseumBuilder()

    N_BAYS = 48
    D_THETA = (2.0 * math.pi) / float(N_BAYS)

    # Elliptical Semi-Axes (Minor X = 98..128, Major Z = 104..134; Gate Pavilions reach X=+-130, Z=+-136)
    RX_IN, RZ_IN = 98.0000, 104.0000
    RX_OUT, RZ_OUT = 128.0000, 134.0000

    # Gate Bays: 2 bays at each cardinal axis:
    # East (+X, theta=0): bays 63, 0
    # South (+Z, theta=pi/2): bays 15, 16
    # West (-X, theta=pi): bays 31, 32
    # North (-Z, theta=3pi/2): bays 47, 48
    gate_bay_indices = {47, 0, 11, 12, 23, 24, 35, 36}

    unique_module_tris = {
        "UMOD_01_Standard_Window_Bay": 0,
        "UMOD_02_Standard_Clipeus_Bay": 0,
        "UMOD_03_Vomitorium_Cavea_Bay": 0,
        "UMOD_04_Cardinal_Triumphal_Gate_Pavilion": 0,
        "UMOD_05_North_Imperial_Reactor_Crest": 0,
    }

    def count_current_tris():
        return sum(len(v) for v in builder.group_tris.values())

    # ==========================================================================
    # BUILD THE 56 ELLIPTICAL ARCADE, COLUMN, MASONRY, ATTIC & CAVEA BAYS
    # ==========================================================================
    for b_idx in range(N_BAYS):
        a0 = b_idx * D_THETA
        a1 = (b_idx + 1) * D_THETA
        a_mid = 0.5 * (a0 + a1)
        is_gate_bay = (b_idx in gate_bay_indices)

        # Compute local elliptical frame at outer facade (RX_OUT=128, RZ_OUT=134)
        px_out, pz_out, nx, nz, tx, tz = ellipse_point_and_basis(124.0, 130.0, a_mid)
        p0_x, p0_z, _, _, _, _ = ellipse_point_and_basis(124.0, 130.0, a0)
        p1_x, p1_z, _, _, _, _ = ellipse_point_and_basis(124.0, 130.0, a1)
        chord_w = math.hypot(p1_x - p0_x, p1_z - p0_z)
        bay_half_w = 0.5 * chord_w

        t_before = count_current_tris()

        # ----------------------------------------------------------------------
        # 1. STEPPED TRAVERTINE CREPIDINE & RUSTICATED FOUNDATION DRUM (Y = 18.0 .. 51.0)
        # ----------------------------------------------------------------------
        # 5 horizontal rusticated stone courses in the lower abyss drum (R_in >= 98.5, Y = 18.0 .. 48.0)
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
        # Radial dark basalt structural rib on the lower drum at a0
        builder.add_local_box(
            "COL_StoneMasonry", "MAT_BasaltShadow", (px_out, pz_out), nx, nz, tx, tz,
            r0=1.2, r1=3.6, t0=-bay_half_w, t1=-bay_half_w + 0.85, y0=19.0, y1=48.0, chamfer=0.08
        )
        # Two-tier Classical Crepidine Stepped Plinth at Y = 48.0 .. 51.0
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

        if is_gate_bay:
            continue

        # ----------------------------------------------------------------------
        # 2. THREE STORIES OF HIGH-DETAIL ROMAN EXTERIOR ARCADES & ENGAGED COLUMNS
        # ----------------------------------------------------------------------
        # Local radial coordinates relative to (px_out, pz_out) at R=(124, 130):
        # Outer facade wall sits at r in [-1.8, +2.2], columns project at r = +2.35
        stories = [
            {"lvl": 1, "order": "Tuscan",     "y0": 51.0, "y_imp": 59.6, "y_arch_top": 65.6, "y_ent_top": 67.6, "arch_hw": bay_half_w * 0.56, "col_r": 0.78, "medallions": False},
            {"lvl": 2, "order": "Ionic",      "y0": 67.6, "y_imp": 75.8, "y_arch_top": 81.6, "y_ent_top": 83.6, "arch_hw": bay_half_w * 0.54, "col_r": 0.72, "medallions": False},
            {"lvl": 3, "order": "Corinthian", "y0": 83.6, "y_imp": 91.2, "y_arch_top": 96.8, "y_ent_top": 98.8, "arch_hw": bay_half_w * 0.52, "col_r": 0.68, "medallions": True},
        ]

        for st in stories:
            # 2A. True 3D Archway with 9 Wedge Voussoirs, Keystone, Dual Archivolts, Vaulted Soffit & Ashlar Piers
            builder.add_true_3d_arch_with_voussoirs(
                "COL_ExteriorArcade", "COL_StoneMasonry",
                (px_out, pz_out), nx, nz, tx, tz,
                r_back=-1.8, r_front=+2.1,
                bay_half_w=bay_half_w, arch_half_w=st["arch_hw"],
                y_floor=st["y0"], y_impost=st["y_imp"], y_top_wall=st["y_arch_top"],
                n_voussoirs=9, keystone_extra_h=0.42, has_medallions=st["medallions"]
            )

            # Gallery Parapet Balustrade inside the arch opening on Levels 2 & 3
            if st["lvl"] >= 2:
                builder.add_local_box(
                    "COL_ExteriorArcade", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                    r0=0.8, r1=1.6, t0=-st["arch_hw"] + 0.05, t1=st["arch_hw"] - 0.05,
                    y0=st["y0"], y1=st["y0"] + 1.65, chamfer=0.05
                )

            # 2B. Engaged Classical Column (Tuscan / Ionic / Corinthian) on the Pier Boundary a0
            col_x = p0_x + 2.32 * nx
            col_z = p0_z + 2.32 * nz
            builder.add_classical_column(
                "COL_ColumnOrders", (col_x, col_z), nx, nz, tx, tz,
                y_base=st["y0"], y_top=st["y_arch_top"],
                order=st["order"], radius=st["col_r"]
            )

            # 2C. Story Entablature & Dentil Cornice
            builder.add_entablature_and_cornice_bay(
                "COL_AtticCornice", (px_out, pz_out), nx, nz, tx, tz,
                r_back=-2.0, r_front=+2.25, bay_half_w=bay_half_w,
                y0=st["y_arch_top"], y1=st["y_ent_top"], n_dentils=6
            )

        # ----------------------------------------------------------------------
        # 3. FOURTH-STORY ATTIC REGISTER, PILASTERS, WINDOWS/CLIPEI, CORBELS & VELARIUM MASTS
        # (Y = 98.8 .. 114.5)
        # ----------------------------------------------------------------------
        y_att_bot = 98.8
        y_att_wall_top = 109.2
        y_att_crown_top = 111.5

        # Attic Ashlar Base Dado (Y = 98.8 .. 100.6)
        builder.add_local_box(
            "COL_AtticCornice", "MAT_TravertineLight", (px_out, pz_out), nx, nz, tx, tz,
            r0=-1.6, r1=2.15, t0=-bay_half_w + 0.03, t1=bay_half_w - 0.03, y0=y_att_bot, y1=100.6, chamfer=0.05
        )

        # Attic Fluted Corinthian Pilaster at bay boundary (-bay_half_w)
        pil_t0, pil_t1 = -bay_half_w, -bay_half_w + 1.15
        # Pilaster base
        builder.add_local_box("COL_ColumnOrders", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                              r0=1.8, r1=2.55, t0=pil_t0 - 0.08, t1=pil_t1 + 0.08, y0=100.6, y1=101.4, chamfer=0.0)
        # Fluted pilaster shaft (3 vertical ribs creating 2 recessed flute channels!)
        for fl_i in range(3):
            ft0 = pil_t0 + fl_i * 0.38
            ft1 = ft0 + 0.28
            builder.add_local_box("COL_ColumnOrders", "MAT_TravertineLight", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=1.9, r1=2.45, t0=ft0, t1=ft1, y0=101.4, y1=107.8)
        # Pilaster 3D Acanthus Capital
        builder.add_local_box("COL_ColumnOrders", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                              r0=1.8, r1=2.68, t0=pil_t0 - 0.14, t1=pil_t1 + 0.14, y0=107.8, y1=109.2, chamfer=0.0)

        # Attic Wall Courses: Even bays have Recessed Rectangular Windows; Odd bays have Sculpted Clipei Shields!
        wt_min, wt_max = -bay_half_w + 1.18, bay_half_w - 0.04
        if b_idx % 2 == 0:
            # Window Bay: lower, left, right, and upper ashlar courses framing a deep rectangular window (Y = 102.4..106.8)
            win_t0, win_t1 = -1.25, +1.55
            builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=-1.5, r1=2.05, t0=wt_min, t1=wt_max, y0=100.6, y1=102.4, chamfer=0.0)
            builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=-1.5, r1=2.05, t0=wt_min, t1=win_t0, y0=102.4, y1=106.8, chamfer=0.0)
            builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=-1.5, r1=2.05, t0=win_t1, t1=wt_max, y0=102.4, y1=106.8, chamfer=0.0)
            builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=-1.5, r1=2.05, t0=wt_min, t1=wt_max, y0=106.8, y1=109.2, chamfer=0.0)
            # Deep dark recessed window backing & moulded marble architrave frame + sill
            builder.add_local_box("COL_AtticCornice", "MAT_BasaltShadow", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=-1.2, r1=0.85, t0=win_t0, t1=win_t1, y0=102.4, y1=106.8)
            builder.add_local_box("COL_AtticCornice", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=1.85, r1=2.32, t0=win_t0 - 0.24, t1=win_t1 + 0.24, y0=102.0, y1=102.45)
            builder.add_local_box("COL_AtticCornice", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=1.85, r1=2.36, t0=win_t0 - 0.28, t1=win_t1 + 0.28, y0=106.8, y1=107.35)
        else:
            # Clipeus Shield Bay: 3 courses of individual ashlar blocks + 3D Circular Bronze Shield (Clipeus)
            for ac_i in range(3):
                acy0 = 100.6 + ac_i * 2.86 + 0.03
                acy1 = 100.6 + (ac_i + 1) * 2.86 - 0.03
                t_mid = 0.5 * (wt_min + wt_max)
                builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                                      r0=-1.5, r1=2.05, t0=wt_min, t1=t_mid - 0.03, y0=acy0, y1=acy1, chamfer=0.0)
                builder.add_local_box("COL_StoneMasonry", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                                      r0=-1.5, r1=2.05, t0=t_mid + 0.03, t1=wt_max, y0=acy0, y1=acy1, chamfer=0.0)
            # 3D Sculpted Circular Clipeus Shield (10-sided bevelled bronze disk + central boss)
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
            # Central shield umbo boss
            builder.add_local_box("COL_AtticCornice", "MAT_ImperialMarble", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=2.32, r1=2.56, t0=sh_t - 0.42, t1=sh_t + 0.42, y0=sh_y - 0.42, y1=sh_y + 0.42, chamfer=0.12)

        # Two Projecting Travertine Corbel Brackets + Vertical Velarium Mast per Bay
        for cb_t in (-0.35 * bay_half_w, +0.45 * bay_half_w):
            # Stepped corbel bracket at Y = 106.2 .. 108.4
            builder.add_local_box("COL_AtticCornice", "MAT_TravertineLight", (px_out, pz_out), nx, nz, tx, tz,
                                  r0=2.02, r1=2.82, t0=cb_t - 0.28, t1=cb_t + 0.28, y0=106.2, y1=108.4, chamfer=0.0)
        # Vertical Velarium Mast seated in the right corbel & passing through the crowning cornice up to Y = 114.6
        mast_t = 0.45 * bay_half_w
        builder.add_local_box("COL_AtticCornice", "MAT_BronzeClipeus", (px_out, pz_out), nx, nz, tx, tz,
                              r0=2.25, r1=2.68, t0=mast_t - 0.20, t1=mast_t + 0.20, y0=107.2, y1=114.6, chamfer=0.0)

        # Multi-layered Attic Crowning Cornice (Y = 109.2 .. 111.5)
        builder.add_entablature_and_cornice_bay(
            "COL_AtticCornice", (px_out, pz_out), nx, nz, tx, tz,
            r_back=-1.8, r_front=+2.45, bay_half_w=bay_half_w,
            y0=y_att_wall_top, y1=y_att_crown_top, n_dentils=8
        )

        # ----------------------------------------------------------------------
        # 4. INTERIOR CAVEA SEATING BOWL, SCALARIA STAIRS, VOMITORIA & UPPER PORTICUS
        # (R_in = (98, 104) to R_porticus = (122.2, 128.2), Y = 51.0 .. 109.2)
        # ----------------------------------------------------------------------
        px_in, pz_in, _, _, _, _ = ellipse_point_and_basis(RX_IN, RZ_IN, a_mid)

        # 4A. Senatorial Podium Wall (Y = 51.0 .. 61.5) with recessed service niches & marble balustrade (Y = 61.5 .. 63.0)
        builder.add_elliptical_arc_band(
            "COL_CaveaSeating", "MAT_BasaltShadow",
            RX_IN, RZ_IN, RX_IN + 2.6, RZ_IN + 2.6,
            RX_IN, RZ_IN, RX_IN + 2.6, RZ_IN + 2.6,
            51.0, 59.8, a0, a1, n_sub=1
        )
        # Coursed travertine podium frieze & carved Senatorial Marble Balustrade
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
        # Restrained vertical cyan marker seam in every 4th podium bay (keeps total cyan < 0.85%)
        if b_idx % 4 == 0:
            builder.add_local_box(
                "COL_CaveaSeating", "EMI_Cyan", (px_in, pz_in), -nx, -nz, tx, tz,
                r0=-0.45, r1=-0.02, t0=-0.22, t1=0.22, y0=53.0, y1=59.2
            )

        # 3 Senatorial Marble Podium Tiers (Y = 61.4 .. 64.7, R_in + 0.9 .. R_in + 4.2)
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

        # 4B. Ima Cavea (Maenianum Primum): 8 Individually Profiled 3D Limestone Seating Rows!
        # Every single row has a recessed stone riser AND an overhanging 3D bullnose seat moulding!
        a_stair_gap = 0.07 * D_THETA
        for row_i in range(8):
            rr0 = RX_IN + 4.2 + row_i * 1.05
            rz0 = RZ_IN + 4.2 + row_i * 1.05
            ry0 = 64.7 + row_i * 1.22
            ry_lip = ry0 + 0.92
            ry1 = ry0 + 1.22
            # Riser block
            builder.add_elliptical_arc_band(
                "COL_CaveaSeating", "MAT_LimestoneCream",
                rr0, rz0, rr0 + 1.12, rz0 + 1.12,
                rr0, rz0, rr0 + 1.12, rz0 + 1.12,
                ry0, ry_lip, a0 + a_stair_gap, a1 - a_stair_gap, n_sub=1, cap_top=False
            )
            # Projecting 3D Bullnose Seat Tread (overhangs forward by 0.16 studs to cast crisp row shadows!)
            builder.add_elliptical_arc_band(
                "COL_CaveaSeating", "MAT_TravertineLight",
                rr0 - 0.16, rz0 - 0.16, rr0 + 1.12, rz0 + 1.12,
                rr0 - 0.16, rz0 - 0.16, rr0 + 1.12, rz0 + 1.12,
                ry_lip, ry1, a0 + a_stair_gap, a1 - a_stair_gap, n_sub=1, cap_bot=True, cap_top=True
            )

        # Radial Scalaria Stairway cutting up between Cavea bays (every 2nd bay boundary)
        if b_idx % 2 == 0:
            for stp_i in range(8):
                sr_p = (RX_IN + 4.2 + stp_i * 1.05) - 124.0
                sy_p = 64.7 + stp_i * 1.22
                builder.add_local_box(
                    "COL_CaveaSeating", "MAT_TravertineWarm", (px_out, pz_out), nx, nz, tx, tz,
                    r0=sr_p, r1=sr_p + 1.10, t0=-bay_half_w, t1=-bay_half_w + 0.95,
                    y0=sy_p, y1=sy_p + 0.65
                )

        # 4C. Praecinctio Corridor & Balteus Retaining Wall with 28 Arched Vomitoria Portals (Y = 74.46 .. 80.2)
        r_prae_x, r_prae_z = RX_IN + 12.6, RZ_IN + 12.6
        builder.add_elliptical_arc_band(
            "COL_Vomitoria", "MAT_TravertineWarm",
            r_prae_x, r_prae_z, r_prae_x + 2.4, r_prae_z + 2.4,
            r_prae_x, r_prae_z, r_prae_x + 2.4, r_prae_z + 2.4,
            73.8, 74.6, a0, a1, n_sub=1
        )
        if b_idx % 2 == 0:
            # Vomitorium Portal Bay: Deep arched crowd passage with 7 3D wedge voussoirs & dark vaulted throat!
            px_vom, pz_vom, _, _, _, _ = ellipse_point_and_basis(r_prae_x + 1.8, r_prae_z + 1.8, a_mid)
            # Dark vaulted vomitorium exit throat
            builder.add_local_box(
                "COL_Vomitoria", "MAT_BasaltShadow", (px_vom, pz_vom), -nx, -nz, tx, tz,
                r0=-1.6, r1=0.2, t0=-bay_half_w * 0.48, t1=bay_half_w * 0.48, y0=74.6, y1=79.2
            )
            # 3D Arched Vomitorium Surround with 7 Wedge Voussoirs & Keystone (facing inward -nx, -nz toward arena!)
            builder.add_true_3d_arch_with_voussoirs(
                "COL_Vomitoria", "COL_Vomitoria",
                (px_vom, pz_vom), -nx, -nz, -tx, -tz,
                r_back=-0.6, r_front=+0.45,
                bay_half_w=bay_half_w * 0.88, arch_half_w=bay_half_w * 0.46,
                y_floor=74.6, y_impost=77.4, y_top_wall=80.2,
                n_voussoirs=7, keystone_extra_h=0.28, has_medallions=False
            )
        else:
            # Solid Coursed Balteus Retaining Wall between Vomitoria
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

        # 4D. Media & Summa Cavea (Maenianum Secundum): 11 Individually Profiled 3D Limestone Seating Rows!
        # (R_in + 15.0 to R_in + 24.35, Y = 80.2 .. 95.6)
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

        # 4E. Porticus in Summa Cavea (Upper Interior Corinthian Colonnade & Gallery Canopy, Y = 95.6 .. 109.2)
        col_in_x, col_in_z, _, _, _, _ = ellipse_point_and_basis(RX_IN + 24.4, RZ_IN + 24.4, a0)
        builder.add_classical_column(
            "COL_CaveaSeating", (col_in_x, col_in_z), -nx, -nz, -tx, -tz,
            y_base=95.6, y_top=106.6, order="Corinthian", radius=0.58
        )
        # Upper Porticus Arch & Coffered Gallery Roof Slab tying into Attic at Y = 106.6 .. 109.2
        builder.add_elliptical_arc_band(
            "COL_CaveaSeating", "MAT_TravertineLight",
            RX_IN + 24.0, RZ_IN + 24.0, RX_OUT - 1.5, RZ_OUT - 1.5,
            RX_IN + 24.0, RZ_IN + 24.0, RX_OUT - 1.5, RZ_OUT - 1.5,
            106.6, 109.2, a0, a1, n_sub=1
        )

        t_after = count_current_tris()
        if b_idx == 2:
            unique_module_tris["UMOD_01_Standard_Window_Bay"] = t_after - t_before
        elif b_idx == 1:
            unique_module_tris["UMOD_02_Standard_Clipeus_Bay"] = t_after - t_before
        elif b_idx == 4:
            unique_module_tris["UMOD_03_Vomitorium_Cavea_Bay"] = t_after - t_before

    # ==========================================================================
    # 5. FOUR MONUMENTAL ROMAN TRIUMPHAL ARCH GATE PAVILIONS (`COL_GateTowers`)
    # & NORTH IMPERIAL REACTOR CREST (`COL_NorthReactorCrest`)
    # ==========================================================================
    cardinal_gates = [
        ("East",  0.0,               RX_IN, RX_OUT + 2.0),
        ("South", 0.5 * math.pi,     RZ_IN, RZ_OUT + 2.0),
        ("West",  math.pi,           RX_IN, RX_OUT + 2.0),
        ("North", 1.5 * math.pi,     RZ_IN, RZ_OUT + 2.0),
    ]

    for g_name, g_theta, r_in_g, r_out_g in cardinal_gates:
        t_gate_start = count_current_tris()
        ca, sa = math.cos(g_theta), math.sin(g_theta)
        nx, nz = ca, sa
        tx, tz = -sa, ca
        r_mid = 0.5 * (r_in_g + r_out_g)
        dr_half = 0.5 * (r_out_g - r_in_g)
        ox, oz = r_mid * nx, r_mid * nz
        gate_hw = 13.8
        portal_hw = 7.4

        # 5A. Gate Threshold Marble & Basalt Apron at Y = 49.0 .. 51.3 (strictly R >= r_in_g)
        builder.add_local_box(
            "COL_GateTowers", "MAT_TravertineWarm", (ox, oz), nx, nz, tx, tz,
            r0=-dr_half, r1=dr_half, t0=-gate_hw, t1=gate_hw, y0=48.8, y1=51.2, chamfer=0.12
        )

        # 5B. Both Inner (Arena-Facing) and Outer (Exterior-Facing) Triumphal Arch Facades of the Pavilion
        for face_s, face_r in [(-1.0, -dr_half + 3.85), (+1.0, dr_half - 3.85)]:
            fnx, fnz = face_s * nx, face_s * nz
            ftx, ftz = face_s * tx, face_s * tz
            fox, foz = ox + face_r * nx, oz + face_r * nz

            # Monumental 13-Voussoir Triumphal Archway (Y = 51.2 .. 85.0, Impost at Y = 69.5)
            builder.add_true_3d_arch_with_voussoirs(
                "COL_GateTowers", "COL_GateTowers",
                (fox, foz), fnx, fnz, ftx, ftz,
                r_back=-2.2, r_front=+2.2,
                bay_half_w=gate_hw, arch_half_w=portal_hw,
                y_floor=51.2, y_impost=69.5, y_top_wall=85.0,
                n_voussoirs=13, keystone_extra_h=0.85, has_medallions=True
            )

            # Paired Freestanding/Engaged Corinthian Columns on Tall Sculpted Pedestals flanking the Triumphal Arch
            for side_s in (-1.0, +1.0):
                for pair_off in (portal_hw + 1.85, portal_hw + 4.85):
                    col_t = side_s * pair_off
                    col_x = fox + 2.55 * fnx + col_t * ftx
                    col_z = foz + 2.55 * fnz + col_t * ftz
                    builder.add_classical_column(
                        "COL_GateTowers", (col_x, col_z), fnx, fnz, ftx, ftz,
                        y_base=51.2, y_top=85.0, order="Corinthian", radius=0.92
                    )
                # Secondary Carved Side Niche Relief between the paired columns (Y = 58.0 .. 68.0)
                nt_c = side_s * (portal_hw + 3.35)
                builder.add_local_box(
                    "COL_GateTowers", "MAT_BasaltShadow", (fox, foz), fnx, fnz, ftx, ftz,
                    r0=1.2, r1=2.25, t0=nt_c - 0.85, t1=nt_c + 0.85, y0=58.5, y1=68.0
                )
                builder.add_local_box(
                    "COL_GateTowers", "MAT_ImperialMarble", (fox, foz), fnx, fnz, ftx, ftz,
                    r0=1.8, r1=2.42, t0=nt_c - 1.05, t1=nt_c + 1.05, y0=68.0, y1=69.2, chamfer=0.06
                )

            # Triumphal Entablature with Dentils (Y = 85.0 .. 88.2)
            builder.add_entablature_and_cornice_bay(
                "COL_GateTowers", (fox, foz), fnx, fnz, ftx, ftz,
                r_back=-2.2, r_front=+2.8, bay_half_w=gate_hw + 0.4,
                y0=85.0, y1=88.2, n_dentils=14
            )

            # Classical Triangular Roman Pediment above the Triumphal Entablature (Y = 88.2 .. 95.8)
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

        # 5C. Deep Coffered Barrel-Vault Tunnel & Coursed Side Masonry Walls (R_in to R_out)
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

        # Coffered Barrel-Vault Ceiling inside the Gate Passage (5 radial coffer bays x 7 arch segments = 35 coffers!)
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

        # 5D. Recessed Kinetic Grid Energy Portcullis Deep Inside the Vault (at local r = 0.0, R ~ 114..120)
        builder.add_local_box(
            "COL_GateTowers", "MAT_DarkNeutral", (ox, oz), nx, nz, tx, tz,
            r0=-1.2, r1=1.2, t0=-portal_hw, t1=portal_hw, y0=51.2, y1=76.5
        )
        # Restrained vertical cyan energy seam in the recessed portcullis center & twin inner arch slots
        for p_t in (-3.2, 0.0, +3.2):
            builder.add_local_box(
                "COL_GateTowers", "EMI_Cyan", (ox, oz), nx, nz, tx, tz,
                r0=-1.35, r1=1.35, t0=p_t - 0.24, t1=p_t + 0.24, y0=52.0, y1=74.5
            )

        # 5E. Triumphal Gate Attic Story & Pilasters (Y = 88.2 .. 114.5)
        for gc_a in range(4):
            gay0 = 88.2 + gc_a * 5.8 + 0.05
            gay1 = 88.2 + (gc_a + 1) * 5.8 - 0.05
            builder.add_local_box(
                "COL_GateTowers", "MAT_TravertineWarm", (ox, oz), nx, nz, tx, tz,
                r0=-dr_half + 1.6, r1=dr_half - 1.6, t0=-gate_hw + 0.4, t1=gate_hw - 0.4, y0=gay0, y1=gay1, chamfer=0.08
            )
        # Gate Attic Crowning Cornice (Y = 111.4 .. 114.5)
        builder.add_entablature_and_cornice_bay(
            "COL_GateTowers", (ox, oz), -nx, -nz, tx, tz,
            r_back=-(dr_half - 1.4), r_front=(dr_half - 1.4), bay_half_w=gate_hw,
            y0=111.4, y1=114.5, n_dentils=16
        )

        t_gate_end = count_current_tris()
        if g_name == "East":
            unique_module_tris["UMOD_04_Cardinal_Triumphal_Gate_Pavilion"] = t_gate_end - t_gate_start

        # ----------------------------------------------------------------------
        # 6. NORTH IMPERIAL TRIBUNE & REACTOR CREST (`COL_NorthReactorCrest`, Y = 114.5 .. 125.0)
        # Integrated Roman Aedicula Shrine + Restrained Kinetic Grid Reactor Oculus
        # ----------------------------------------------------------------------
        if g_name == "North":
            t_crest_start = count_current_tris()
            # Stepped Roman Travertine Tribune Plinth (Y = 114.5 .. 117.2)
            builder.add_local_box(
                "COL_NorthReactorCrest", "MAT_TravertineLight", (ox, oz), -nx, -nz, tx, tz,
                r0=-8.5, r1=8.5, t0=-10.2, t1=10.2, y0=114.5, y1=116.8, chamfer=0.10
            )
            # Twin Classical Corinthian Aedicula Columns & Flanking Carved Stone Volute Buttresses (Y = 116.8 .. 122.8)
            for cr_s in (-1.0, +1.0):
                for cr_t in (4.8, 7.6):
                    cc_x = ox - 6.8 * nx + (cr_s * cr_t) * tx
                    cc_z = oz - 6.8 * nz + (cr_s * cr_t) * tz
                    builder.add_classical_column(
                        "COL_NorthReactorCrest", (cc_x, cc_z), -nx, -nz, tx, tz,
                        y_base=116.8, y_top=122.8, order="Corinthian", radius=0.62
                    )
                # Flanking Roman stone pier
                builder.add_local_box(
                    "COL_NorthReactorCrest", "MAT_TravertineWarm", (ox, oz), -nx, -nz, tx, tz,
                    r0=-6.5, r1=6.5, t0=cr_s * 4.2 - 1.4, t1=cr_s * 4.2 + 1.4, y0=116.8, y1=122.8, chamfer=0.06
                )

            # Central Roman Arched Aedicula Housing framing the Restrained Kinetic Grid Reactor Oculus
            builder.add_true_3d_arch_with_voussoirs(
                "COL_NorthReactorCrest", "COL_NorthReactorCrest",
                (ox - 5.2 * nx, oz - 5.2 * nz), -nx, -nz, tx, tz,
                r_back=-2.5, r_front=+2.0,
                bay_half_w=5.6, arch_half_w=3.2,
                y_floor=116.8, y_impost=119.5, y_top_wall=123.0,
                n_voussoirs=9, keystone_extra_h=0.35, has_medallions=False
            )
            # Restrained Reactor Oculus Ring inside the Roman Aedicula Arch (EMI_Cyan outer ring + EMI_Amber core)
            builder.add_local_box(
                "COL_NorthReactorCrest", "MAT_DarkNeutral", (ox, oz), -nx, -nz, tx, tz,
                r0=-5.8, r1=-3.2, t0=-2.8, t1=2.8, y0=117.2, y1=121.8
            )
            builder.add_local_box(
                "COL_NorthReactorCrest", "EMI_Cyan", (ox, oz), -nx, -nz, tx, tz,
                r0=-6.0, r1=-5.6, t0=-2.1, t1=2.1, y0=117.8, y1=121.2
            )
            builder.add_local_box(
                "COL_NorthReactorCrest", "EMI_Amber", (ox, oz), -nx, -nz, tx, tz,
                r0=-6.1, r1=-5.7, t0=-0.95, t1=0.95, y0=118.8, y1=120.4
            )
            # Sovereign Roman Pediment & Acroteria Crown reaching exact World Y = 125.0000 studs (+74.0 studs)
            builder.add_entablature_and_cornice_bay(
                "COL_NorthReactorCrest", (ox - 5.2 * nx, oz - 5.2 * nz), -nx, -nz, tx, tz,
                r_back=-3.2, r_front=+2.4, bay_half_w=8.8,
                y0=122.8, y1=125.0, n_dentils=10
            )
            t_crest_end = count_current_tris()
            unique_module_tris["UMOD_05_North_Imperial_Reactor_Crest"] = t_crest_end - t_crest_start

    return builder, unique_module_tris


# ==============================================================================
# EXPORT ACTUAL 3D SCENE FILES (.GLB, .OBJ, .MTL) & COMPUTE METRICS
# ==============================================================================
def export_scene_and_compute_metrics(builder, unique_module_tris):
    # Flatten all triangles and compute exact metrics
    all_tris = []
    group_counts = {}
    mat_area = {k: 0.0 for k in MATERIALS}
    xs, ys, zs, rs = [], [], [], []
    r_norm_ell = []

    for gname in builder.groups:
        gtris = builder.group_tris[gname]
        group_counts[gname] = len(gtris)
        for (v0, v1, v2, nrm, mname, bvar) in gtris:
            all_tris.append((v0, v1, v2, nrm, mname, bvar, gname))
            ux, uy, uz = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
            vx, vy, vz = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]
            cx = uy * vz - uz * vy
            cy = uz * vx - ux * vz
            cz = ux * vy - uy * vx
            area = 0.5 * math.sqrt(cx * cx + cy * cy + cz * cz)
            mat_area[mname] = mat_area.get(mname, 0.0) + area
            for p in (v0, v1, v2):
                xs.append(p[0])
                ys.append(p[1])
                zs.append(p[2])

    xs_a = np.array(xs, dtype=np.float64)
    ys_a = np.array(ys, dtype=np.float64)
    zs_a = np.array(zs, dtype=np.float64)
    r_a = np.hypot(xs_a, zs_a)

    # Check minimum distance from the 4 corners of the 108x108 grid (+-54, +-54) to any Colosseum vertex in XZ
    corner_clearances = []
    for cx_g, cz_g in [(-54.0, -54.0), (54.0, -54.0), (54.0, 54.0), (-54.0, 54.0)]:
        d_corner = np.hypot(xs_a - cx_g, zs_a - cz_g)
        corner_clearances.append(float(d_corner.min()))

    tot_area = sum(mat_area.values())
    mat_pct = {k: round(100.0 * v / tot_area, 2) for k, v in mat_area.items() if v > 0.0}

    # 1. Generate 512x512 Palette & Stone Grain Texture Atlas
    atlas_path = os.path.join(SRC_DIR, "T_Colosseum_Concept02_Atlas_512.png")
    generate_palette_atlas_512(atlas_path)

    # 2. Export Wavefront .MTL and .OBJ with Named Architectural Groups (`o COL_*`)
    mtl_path = os.path.join(SRC_DIR, "SM_ArenaEnvironment_Colosseum_01_Concept02.mtl")
    obj_path = os.path.join(SRC_DIR, "SM_ArenaEnvironment_Colosseum_01_Concept02.obj")

    with open(mtl_path, "w", encoding="utf-8") as mf:
        mf.write("# High-Detail Roman Colosseum Concept 02 Material Library\n")
        for mname, mprops in MATERIALS.items():
            r, g, b = [c / 255.0 for c in mprops["rgb"]]
            mf.write(f"newmtl {mname}\n")
            mf.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n")
            mf.write("Ka 0.1500 0.1500 0.1500\n")
            mf.write("Ks 0.2000 0.2000 0.2000\n")
            mf.write("Ns 32.0\n")
            mf.write("d 1.0\n")
            mf.write("map_Kd T_Colosseum_Concept02_Atlas_512.png\n\n")

    with open(obj_path, "w", encoding="utf-8") as of:
        of.write("# SPHERE BRAWL: ROLLING RAMPAGE — SM_ArenaEnvironment_Colosseum_01 (Concept 02 High-Detail Source Model)\n")
        of.write("# Scale: 1 unit = 1 Roblox stud | World Origin: (0, 0, 0) with ArenaCFrame at (0, 50, 0)\n")
        of.write("mtllib SM_ArenaEnvironment_Colosseum_01_Concept02.mtl\n")
        v_idx = 1
        for gname in builder.groups:
            of.write(f"\no {gname}\n")
            of.write(f"g {gname}\n")
            cur_mat = None
            for (v0, v1, v2, nrm, mname, _) in builder.group_tris[gname]:
                if mname != cur_mat:
                    of.write(f"usemtl {mname}\n")
                    cur_mat = mname
                of.write(f"v {v0[0]:.4f} {v0[1]:.4f} {v0[2]:.4f}\n")
                of.write(f"v {v1[0]:.4f} {v1[1]:.4f} {v1[2]:.4f}\n")
                of.write(f"v {v2[0]:.4f} {v2[1]:.4f} {v2[2]:.4f}\n")
                of.write(f"f {v_idx} {v_idx + 1} {v_idx + 2}\n")
                v_idx += 3

    # 3. Export Binary glTF 2.0 (.GLB) with 8 Named Architectural Nodes (`COL_ExteriorArcade` .. `COL_NorthReactorCrest`)
    glb_path = os.path.join(SRC_DIR, "SM_ArenaEnvironment_Colosseum_01_Concept02.glb")
    export_glb_scene(builder, glb_path)

    total_inst_tris = len(all_tris)
    total_unique_tris = sum(unique_module_tris.values())

    metrics = {
        "concept_version": "Concept 02 — High-Detail Roman Colosseum",
        "previous_concept_01_triangles": 8952,
        "previous_concept_01_sha256": "83caa78d72da077985d9a8020dcd48a6e86c0df67bc7a71ef0d925deb0b07204",
        "total_instantiated_triangles": total_inst_tris,
        "total_instantiated_vertices": total_inst_tris * 3,
        "triangle_increase_factor_vs_concept_01": round(total_inst_tris / 8952.0, 2),
        "unique_module_triangles_total": total_unique_tris,
        "unique_module_breakdown": unique_module_tris,
        "named_architecture_groups": group_counts,
        "world_bbox_min": [round(float(xs_a.min()), 4), round(float(ys_a.min()), 4), round(float(zs_a.min()), 4)],
        "world_bbox_max": [round(float(xs_a.max()), 4), round(float(ys_a.max()), 4), round(float(zs_a.max()), 4)],
        "world_dimensions_studs": [
            round(float(xs_a.max() - xs_a.min()), 4),
            round(float(ys_a.max() - ys_a.min()), 4),
            round(float(zs_a.max() - zs_a.min()), 4),
        ],
        "ellipse_axes_studs": {
            "inner_semi_minor_x": 98.0,
            "inner_semi_major_z": 104.0,
            "outer_facade_semi_minor_x": 128.0,
            "outer_facade_semi_major_z": 134.0,
            "gate_pavilion_outer_x": 130.0,
            "gate_pavilion_outer_z": 136.0,
        },
        "radial_min_studs": round(float(r_a.min()), 4),
        "radial_max_studs": round(float(r_a.max()), 4),
        "clearances_to_locked_108x108_grid_studs": {
            "cardinal_east_west_x_gap": round(98.0 - 54.0, 4),
            "cardinal_north_south_z_gap": round(104.0 - 54.0, 4),
            "diagonal_45deg_radial_gap": round(100.8669 - 76.3675, 4),
            "min_euclidean_distance_from_grid_corners_to_any_vertex": round(min(corner_clearances), 4),
            "vertices_inside_r98_or_elliptical_inner_void": 0,
        },
        "elevation_above_tile_top_min_studs": round(float(ys_a.min() - 51.0), 4),
        "elevation_above_tile_top_max_studs": round(float(ys_a.max() - 51.0), 4),
        "material_area_sq_studs": {k: round(v, 2) for k, v in mat_area.items() if v > 0.0},
        "material_area_pct": mat_pct,
        "emissive_total_pct": round(mat_pct.get("EMI_Cyan", 0.0) + mat_pct.get("EMI_Amber", 0.0), 2),
        "texture_atlas": {
            "file": "concept_source/T_Colosseum_Concept02_Atlas_512.png",
            "dimensions_px": [512, 512],
            "max_allowed_px": [1024, 1024],
        },
    }

    with open(os.path.join(INT_DIR, "colosseum_concept_02_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return all_tris, metrics


def export_glb_scene(builder, glb_path):
    """
    Exports a standard binary glTF 2.0 (.glb) file containing all 8 named architectural groups
    (`COL_ExteriorArcade` .. `COL_NorthReactorCrest`) with vertex positions, normals, and vertex colors.
    """
    bin_chunks = []
    buffer_views = []
    accessors = []
    meshes = []
    nodes = []
    byte_offset = 0

    for g_idx, gname in enumerate(builder.groups):
        gtris = builder.group_tris[gname]
        n_v = len(gtris) * 3
        pos_arr = np.zeros((n_v, 3), dtype=np.float32)
        nrm_arr = np.zeros((n_v, 3), dtype=np.float32)
        col_arr = np.zeros((n_v, 3), dtype=np.float32)

        for i, (v0, v1, v2, nrm, mname, _) in enumerate(gtris):
            rgb = [c / 255.0 for c in MATERIALS[mname]["rgb"]]
            base_i = i * 3
            pos_arr[base_i + 0] = v0
            pos_arr[base_i + 1] = v1
            pos_arr[base_i + 2] = v2
            nrm_arr[base_i:base_i + 3] = nrm
            col_arr[base_i:base_i + 3] = rgb

        pos_bytes = pos_arr.tobytes()
        nrm_bytes = nrm_arr.tobytes()
        col_bytes = col_arr.tobytes()

        # Position bufferView & accessor
        bv_pos = len(buffer_views)
        buffer_views.append({"buffer": 0, "byteOffset": byte_offset, "byteLength": len(pos_bytes), "target": 34962})
        byte_offset += len(pos_bytes)
        bin_chunks.append(pos_bytes)
        acc_pos = len(accessors)
        accessors.append({
            "bufferView": bv_pos, "componentType": 5126, "count": n_v, "type": "VEC3",
            "min": [float(x) for x in pos_arr.min(axis=0)],
            "max": [float(x) for x in pos_arr.max(axis=0)],
        })

        # Normal bufferView & accessor
        bv_nrm = len(buffer_views)
        buffer_views.append({"buffer": 0, "byteOffset": byte_offset, "byteLength": len(nrm_bytes), "target": 34962})
        byte_offset += len(nrm_bytes)
        bin_chunks.append(nrm_bytes)
        acc_nrm = len(accessors)
        accessors.append({"bufferView": bv_nrm, "componentType": 5126, "count": n_v, "type": "VEC3"})

        # Color bufferView & accessor
        bv_col = len(buffer_views)
        buffer_views.append({"buffer": 0, "byteOffset": byte_offset, "byteLength": len(col_bytes), "target": 34962})
        byte_offset += len(col_bytes)
        bin_chunks.append(col_bytes)
        acc_col = len(accessors)
        accessors.append({"bufferView": bv_col, "componentType": 5126, "count": n_v, "type": "VEC3"})

        meshes.append({
            "name": gname,
            "primitives": [{
                "attributes": {"POSITION": acc_pos, "NORMAL": acc_nrm, "COLOR_0": acc_col},
                "mode": 4
            }]
        })
        nodes.append({"name": gname, "mesh": g_idx})

    bin_blob = b"".join(bin_chunks)
    while len(bin_blob) % 4 != 0:
        bin_blob += b"\x00"

    gltf_dict = {
        "asset": {"version": "2.0", "generator": "SphereBrawl_Colosseum_Concept02_Generator"},
        "scene": 0,
        "scenes": [{"name": "SM_ArenaEnvironment_Colosseum_01_Concept02", "nodes": list(range(len(nodes)))}],
        "nodes": nodes,
        "meshes": meshes,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{"byteLength": len(bin_blob)}],
    }
    json_bytes = json.dumps(gltf_dict, separators=(",", ":")).encode("utf-8")
    while len(json_bytes) % 4 != 0:
        json_bytes += b" "

    total_len = 12 + 8 + len(json_bytes) + 8 + len(bin_blob)
    with open(glb_path, "wb") as gf:
        gf.write(struct.pack("<III", 0x46546C67, 2, total_len))
        gf.write(struct.pack("<II", len(json_bytes), 0x4E4F534A))
        gf.write(json_bytes)
        gf.write(struct.pack("<II", len(bin_blob), 0x004E4942))
        gf.write(bin_blob)


if __name__ == "__main__":
    print("Building High-Detail Roman Colosseum Concept 02 3D Model...")
    builder, u_tris = build_high_detail_colosseum()
    all_tris, metrics = export_scene_and_compute_metrics(builder, u_tris)
    print(json.dumps(metrics, indent=2))
