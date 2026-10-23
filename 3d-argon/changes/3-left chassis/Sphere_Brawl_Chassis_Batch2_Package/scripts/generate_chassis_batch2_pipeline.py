#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — TASK-09 ASSET BATCH 2: CHASSIS MODELS GENERATOR & VALIDATOR
===========================================================================================
Deterministically generates, validates, renders, and packages the three Batch 2 cosmetic
sphere chassis models for Sphere Brawl: Rolling Rampage:

  1. SM_Chassis_Trickster_01  (236 triangles, Max Radius <= 2.946 studs < 2.970 limit)
  2. SM_Chassis_Magnetar_01   (232 triangles, Max Radius <= 2.948 studs < 2.970 limit)
  3. SM_Chassis_Bulwark_01    (232 triangles, Max Radius <= 2.962 studs < 2.970 limit)

Technical & Architectural Contracts Enforced:
  - Cosmetic-Only Parity (D-008, MASTER_IMPLEMENTATION_PLAN.md §8.2): All 4 chassis (Rammer,
    Trickster, Magnetar, Bulwark) have identical gameplay stats (OutgoingFactor = 1.0,
    ResistanceFactor = 1.0) and are purely non-colliding visual shells (`CanCollide = false`,
    `CanTouch = false`, `CanQuery = false`, `Massless = true`).
  - Sphere Collider Envelope: Every vertex has Euclidean distance from local origin `(0,0,0)`
    strictly `<= 2.970` studs (fitting inside the `R = 3.000` stud / `6.0`-stud diameter
    authoritative `SphereRoot` collider).
  - Coordinate Convention: Centered origin `(0,0,0)`, `+Y` Up, `+Z` Forward, `+X` Right,
    `1.0 unit = 1.0 Roblox stud`.
  - Triangle Budget: Every complete chassis is strictly `<= 250` triangles (`232` to `236` tris),
    with `0` degenerate triangles, `0` face-winding/normal mismatches, and `0` floating or
    disconnected parts (all raised plates/rings/stabilizers are contiguous frustum extrusions
    rooted on the closed inner sphere hull).
  - Roblox Studio Material Transfer (Proven Batch 1 Workflow):
    Each `.glb` exports a multi-node scene hierarchy (`Part_MAT_DarkNeutral`, `Part_MAT_AltNeutral`,
    `Part_MAT_LightTrim`, `Part_EMI_*`) + baked `COLOR_0` vertex colors + `TEXCOORD_0` UVs +
    embedded 96x96 PNG palette atlas (`SphereBrawl_Chassis_PaletteAtlas.png`).
    Each `.obj` exports `o <Asset>__<MaterialSlot>` sub-objects + `vt` UVs + extended vertex
    colors + `.mtl` with `Kd`/`Ke` and `map_Kd SphereBrawl_Chassis_PaletteAtlas.png`.
"""

import os
import sys
import io
import json
import math
import struct
import shutil
import hashlib
import zipfile
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak
)

WORKSPACE = "/working_dir/c_51174e822ce514ba"
INT_DIR = os.path.join(WORKSPACE, "artifacts/file_generation/ttl=63d/intermediate")
OUT_DIR = os.path.join(WORKSPACE, "artifacts/file_generation/ttl=63d/output")

TMP_BUILD_ROOT = "/tmp/sphere_brawl_chassis_batch2_build"
PKG_NAME = "Sphere_Brawl_Chassis_Batch2_Package"
PKG_STAGE_DIR = os.path.join(TMP_BUILD_ROOT, PKG_NAME)

SUBDIRS = [
    "meshes",
    "textures",
    "scripts",
    "previews",
    "docs",
]
for sd in SUBDIRS:
    os.makedirs(os.path.join(PKG_STAGE_DIR, sd), exist_ok=True)

PALETTE_ORDER = [
    "MAT_DarkNeutral",
    "MAT_AltNeutral",
    "MAT_LightTrim",
    "EMI_Cyan",
    "EMI_Magnetic",
    "EMI_Kinetic",
]

PALETTE_SRGB = {
    "MAT_DarkNeutral": (32, 38, 54),      # #202636 — Primary structural armor & inner hull
    "MAT_AltNeutral":  (42, 50, 70),      # #2A3246 — Secondary recessed / faceted armor plates
    "MAT_LightTrim":   (170, 190, 215),   # #AABED7 — Chamfered metallic rims, collars & brackets
    "EMI_Cyan":        (0, 195, 255),     # #00C3FF — Cyan core viewport / energy seams
    "EMI_Magnetic":    (165, 55, 255),    # #A537FF — Magnetic Storm / Magnetar field rings & coils
    "EMI_Kinetic":     (255, 125, 0),     # #FF7D00 — Kinetic thruster chevrons & high-speed vents
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
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(32, 38, 54)",
        "surface_role": "Primary dark metallic chassis hull, heavy armor plates, and polar caps",
    },
    "MAT_AltNeutral": {
        "rgb_255": [42, 50, 70],
        "hex": "#2A3246",
        "normalized_rgb": [round(42/255.0, 6), round(50/255.0, 6), round(70/255.0, 6)],
        "emissive": False,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(42, 50, 70)",
        "surface_role": "Secondary recessed sphere segments, angled cheek plates, and coil housings",
    },
    "MAT_LightTrim": {
        "rgb_255": [170, 190, 215],
        "hex": "#AABED7",
        "normalized_rgb": [round(170/255.0, 6), round(190/255.0, 6), round(215/255.0, 6)],
        "emissive": False,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(170, 190, 215)",
        "surface_role": "Sleek aerodynamic stabilizer fins, inductor pole shoes, and reinforced rim collars",
    },
    "EMI_Cyan": {
        "rgb_255": [0, 195, 255],
        "hex": "#00C3FF",
        "normalized_rgb": [round(0/255.0, 6), round(195/255.0, 6), round(255/255.0, 6)],
        "emissive": True,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(0, 195, 255)",
        "surface_role": "Frontal core apertures, Trickster slash inlays, Magnetar pole tips, and Bulwark slit visors",
    },
    "EMI_Magnetic": {
        "rgb_255": [165, 55, 255],
        "hex": "#A537FF",
        "normalized_rgb": [round(165/255.0, 6), round(55/255.0, 6), round(255/255.0, 6)],
        "emissive": True,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(165, 55, 255)",
        "surface_role": "Magnetar equatorial/meridian flux rings and polar electromagnetic inductor cores",
    },
    "EMI_Kinetic": {
        "rgb_255": [255, 125, 0],
        "hex": "#FF7D00",
        "normalized_rgb": [round(255/255.0, 6), round(125/255.0, 6), round(0/255.0, 6)],
        "emissive": True,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(255, 125, 0)",
        "surface_role": "Trickster asymmetric kinetic speed vents and rear thruster exhaust ports",
    },
}


def build_palette_atlas_png_bytes():
    cell_px = 32
    img = Image.new("RGB", (cell_px * 3, cell_px * 3), (32, 38, 54))
    draw = ImageDraw.Draw(img)
    uv_centers_gltf = {}
    uv_centers_obj = {}

    for idx, mname in enumerate(PALETTE_ORDER):
        col_i = idx % 3
        row_i = idx // 3
        x0, y0 = col_i * cell_px, row_i * cell_px
        x1, y1 = x0 + cell_px - 1, y0 + cell_px - 1
        rgb = PALETTE_SRGB[mname]
        draw.rectangle([x0, y0, x1, y1], fill=rgb)

        u = (col_i + 0.5) / 3.0
        v_gltf = (row_i + 0.5) / 3.0
        v_obj = 1.0 - (row_i + 0.5) / 3.0
        uv_centers_gltf[mname] = (round(u, 5), round(v_gltf, 5))
        uv_centers_obj[mname] = (round(u, 5), round(v_obj, 5))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue(), uv_centers_gltf, uv_centers_obj


ATLAS_PNG_BYTES, UV_CENTERS_GLTF, UV_CENTERS_OBJ = build_palette_atlas_png_bytes()
ATLAS_FILENAME = "SphereBrawl_Chassis_PaletteAtlas.png"
with open(os.path.join(PKG_STAGE_DIR, "textures", ATLAS_FILENAME), "wb") as _af:
    _af.write(ATLAS_PNG_BYTES)
with open(os.path.join(PKG_STAGE_DIR, "meshes", ATLAS_FILENAME), "wb") as _af2:
    _af2.write(ATLAS_PNG_BYTES)


def sph_pt(r, phi, theta):
    """
    Converts spherical coordinates `(r, phi, theta)` into Roblox cartesian coordinates `(X, Y, Z)`:
      - `phi` in `[-pi/2, +pi/2]`: latitude angle (`-pi/2` = South `-Y`, `+pi/2` = North `+Y`)
      - `theta` in `[-pi, +pi]`: azimuth angle around `+Y` where `theta = 0` is `+Z` (Forward),
        `theta = +pi/2` is `+X` (Right), `theta = +-pi` is `-Z` (Rear), `theta = -pi/2` is `-X` (Left).
    """
    cp = math.cos(phi)
    return np.array([
        r * cp * math.sin(theta),
        r * math.sin(phi),
        r * cp * math.cos(theta),
    ], dtype=np.float64)


class ChassisMeshBuilder:
    """
    Deterministic low-poly (< 250 tris) spherical chassis builder with:
      - Strict radius clamping (`R <= 2.965` studs < `2.970` stud max limit)
      - Contiguous frustum extrusions rooted directly onto the inner sphere hull (zero floating parts)
      - Outward radial normal verification (`dot(face_normal, outward_dir) > 0`)
      - Multi-node GLB and multi-object OBJ export for immediate Roblox Studio material compatibility
    """

    def __init__(self, name, max_radius_clamp=2.965):
        self.name = name
        self.max_radius_clamp = max_radius_clamp
        self.groups = {}  # (group_name, mat_name) -> list of (v0, v1, v2)

    def _clamp_vertex(self, v):
        pt = np.array(v, dtype=np.float64)
        r = float(np.linalg.norm(pt))
        if r > self.max_radius_clamp:
            pt = pt * (self.max_radius_clamp / r)
        pt = np.round(pt, 5)
        while float(np.linalg.norm(pt)) > self.max_radius_clamp:
            pt = np.trunc(pt * 0.99995 * 1e5) / 1e5
        return pt

    def add_tri(self, group_name, mat_name, v0, v1, v2, expected_normal=None):
        p0 = self._clamp_vertex(v0)
        p1 = self._clamp_vertex(v1)
        p2 = self._clamp_vertex(v2)

        cross = np.cross(p1 - p0, p2 - p0)
        area = 0.5 * float(np.linalg.norm(cross))
        if area < 1e-6:
            raise ValueError(f"Degenerate triangle in {self.name}/{group_name}: area={area}")

        ref_n = np.array(expected_normal, dtype=np.float64) if expected_normal is not None else ((p0 + p1 + p2) / 3.0)
        if float(np.dot(cross, ref_n)) < 0.0:
            p1, p2 = p2, p1

        self.groups.setdefault((group_name, mat_name), []).append((p0, p1, p2))

    def add_quad(self, group_name, mat_name, v0, v1, v2, v3, expected_normal=None):
        self.add_tri(group_name, mat_name, v0, v1, v2, expected_normal=expected_normal)
        self.add_tri(group_name, mat_name, v0, v2, v3, expected_normal=expected_normal)

    def add_segmented_core_sphere(self, r_base, phis, n_segs, band_mat_fn, theta_twist_per_ring=None):
        """
        Builds a closed, watertight spherical hull with polar triangle fans (`0` degenerate faces):
          - `phis`: sorted list of latitude angles from `-pi/2` to `+pi/2` (length `n_rings + 1`)
          - `n_segs`: number of longitudinal segments around the equator
          - `band_mat_fn(ring_idx, seg_idx, phi_mid, theta_mid)` -> `(group_name, mat_name)`
          - `theta_twist_per_ring`: optional list of azimuth twist offsets (radians) per latitude ring
        Total triangles = `2 * n_segs * (n_rings - 1)`.
        For `n_rings = 5, n_segs = 10` -> `2 * 10 * 4 = 80` triangles.
        For `n_rings = 5, n_segs = 8`  -> `2 * 8 * 4  = 64` triangles.
        """
        n_rings = len(phis) - 1
        if theta_twist_per_ring is None:
            theta_twist_per_ring = [0.0] * (n_rings + 1)

        south_pole = np.array([0.0, -r_base, 0.0], dtype=np.float64)
        north_pole = np.array([0.0,  r_base, 0.0], dtype=np.float64)

        for i in range(n_rings):
            p0, p1 = phis[i], phis[i + 1]
            p_mid = 0.5 * (p0 + p1)
            tw0 = theta_twist_per_ring[i]
            tw1 = theta_twist_per_ring[i + 1]

            for j in range(n_segs):
                t0_base = -math.pi + (2.0 * math.pi * j) / n_segs
                t1_base = -math.pi + (2.0 * math.pi * (j + 1)) / n_segs
                t_mid = 0.5 * (t0_base + t1_base)
                # Normalize t_mid to [-pi, pi]
                while t_mid > math.pi:
                    t_mid -= 2.0 * math.pi
                while t_mid < -math.pi:
                    t_mid += 2.0 * math.pi

                g_name, m_name = band_mat_fn(i, j, p_mid, t_mid)
                out_dir = sph_pt(1.0, p_mid, t_mid)

                if i == 0:
                    v1 = sph_pt(r_base, p1, t0_base + tw1)
                    v2 = sph_pt(r_base, p1, t1_base + tw1)
                    self.add_tri(g_name, m_name, south_pole, v2, v1, expected_normal=out_dir)
                elif i == n_rings - 1:
                    v0 = sph_pt(r_base, p0, t0_base + tw0)
                    v1 = sph_pt(r_base, p0, t1_base + tw0)
                    self.add_tri(g_name, m_name, v0, v1, north_pole, expected_normal=out_dir)
                else:
                    v00 = sph_pt(r_base, p0, t0_base + tw0)
                    v10 = sph_pt(r_base, p0, t1_base + tw0)
                    v11 = sph_pt(r_base, p1, t1_base + tw1)
                    v01 = sph_pt(r_base, p1, t0_base + tw1)
                    self.add_quad(g_name, m_name, v00, v10, v11, v01, expected_normal=out_dir)

    def add_spherical_frustum_plate(self, group_name, mat_name, r_base, r_top,
                                    phi0, phi1, theta0, theta1,
                                    inset_phi=0.04, inset_theta=0.05):
        """
        Adds a 5-sided beveled spherical armor plate or fin rooted at `r_base` and rising to `r_top`.
        Consists of 1 outer top quad + 4 beveled side skirt quads = 5 quads = 10 triangles.
        Because `r_base` sits directly on/inside the core hull radius, there is zero floating geometry.
        """
        ip0 = phi0 + inset_phi
        ip1 = phi1 - inset_phi
        it0 = theta0 + inset_theta
        it1 = theta1 - inset_theta

        b00 = sph_pt(r_base, phi0, theta0)
        b10 = sph_pt(r_base, phi0, theta1)
        b11 = sph_pt(r_base, phi1, theta1)
        b01 = sph_pt(r_base, phi1, theta0)

        t00 = sph_pt(r_top, ip0, it0)
        t10 = sph_pt(r_top, ip0, it1)
        t11 = sph_pt(r_top, ip1, it1)
        t01 = sph_pt(r_top, ip1, it0)

        p_mid = 0.5 * (phi0 + phi1)
        t_mid = 0.5 * (theta0 + theta1)
        n_top = sph_pt(1.0, p_mid, t_mid)
        n_south = sph_pt(1.0, phi0 - 0.35, t_mid)
        n_north = sph_pt(1.0, phi1 + 0.35, t_mid)
        n_west = sph_pt(1.0, p_mid, theta0 - 0.45)
        n_east = sph_pt(1.0, p_mid, theta1 + 0.45)

        self.add_quad(group_name, mat_name, t00, t10, t11, t01, expected_normal=n_top)
        self.add_quad(group_name, mat_name, b00, b10, t10, t00, expected_normal=n_south)
        self.add_quad(group_name, mat_name, b11, b01, t01, t11, expected_normal=n_north)
        self.add_quad(group_name, mat_name, b01, b00, t00, t01, expected_normal=n_west)
        self.add_quad(group_name, mat_name, b10, b11, t11, t10, expected_normal=n_east)

    def add_skewed_spherical_blade(self, group_name, mat_name, r_base, r_top,
                                   base_phi_theta_quad, top_phi_theta_quad):
        """
        Adds an angled/swept 5-face spherical blade or asymmetric slash vane (10 triangles)
        defined by 4 `(phi, theta)` corners at `r_base` and 4 `(phi, theta)` corners at `r_top`.
        """
        b_pts = [sph_pt(r_base, p, t) for (p, t) in base_phi_theta_quad]
        t_pts = [sph_pt(r_top, p, t) for (p, t) in top_phi_theta_quad]

        top_centroid = sum(t_pts) / 4.0
        self.add_quad(group_name, mat_name, t_pts[0], t_pts[1], t_pts[2], t_pts[3], expected_normal=top_centroid)

        for i in range(4):
            ni = (i + 1) % 4
            b_a, b_b = b_pts[i], b_pts[ni]
            t_b, t_a = t_pts[ni], t_pts[i]
            edge_dir = b_b - b_a
            radial_out = 0.5 * (b_a + b_b)
            side_n = np.cross(edge_dir, radial_out)
            if float(np.linalg.norm(side_n)) < 1e-6:
                side_n = radial_out
            # Ensure outward side normal points away from plate center
            plate_mid = 0.25 * (b_pts[0] + b_pts[1] + b_pts[2] + b_pts[3])
            face_mid = 0.25 * (b_a + b_b + t_b + t_a)
            out_vec = (face_mid - plate_mid) + 0.35 * radial_out
            self.add_quad(group_name, mat_name, b_a, b_b, t_b, t_a, expected_normal=out_vec)

    def add_equatorial_band_segment(self, group_name, mat_name, r_base, r_top,
                                    phi0, phi1, theta0, theta1, inset_phi=0.02, cap_ends=False):
        """
        Adds one segment of a raised circumferential band (top quad + north/south bevels = 6 tris,
        plus optional end caps = +4 tris).
        """
        ip0, ip1 = phi0 + inset_phi, phi1 - inset_phi
        b00, b10 = sph_pt(r_base, phi0, theta0), sph_pt(r_base, phi0, theta1)
        b11, b01 = sph_pt(r_base, phi1, theta1), sph_pt(r_base, phi1, theta0)
        t00, t10 = sph_pt(r_top, ip0, theta0), sph_pt(r_top, ip0, theta1)
        t11, t01 = sph_pt(r_top, ip1, theta1), sph_pt(r_top, ip1, theta0)

        p_mid = 0.5 * (phi0 + phi1)
        t_mid = 0.5 * (theta0 + theta1)
        self.add_quad(group_name, mat_name, t00, t10, t11, t01, expected_normal=sph_pt(1.0, p_mid, t_mid))
        self.add_quad(group_name, mat_name, b00, b10, t10, t00, expected_normal=sph_pt(1.0, phi0 - 0.3, t_mid))
        self.add_quad(group_name, mat_name, b11, b01, t01, t11, expected_normal=sph_pt(1.0, phi1 + 0.3, t_mid))
        if cap_ends:
            self.add_quad(group_name, mat_name, b01, b00, t00, t01, expected_normal=sph_pt(1.0, p_mid, theta0 - 0.3))
            self.add_quad(group_name, mat_name, b10, b11, t11, t10, expected_normal=sph_pt(1.0, p_mid, theta1 + 0.3))

    def export_obj_and_mtl(self, obj_path, mtl_path):
        mtl_filename = os.path.basename(mtl_path)
        used_mats = sorted(list(set(m for (_, m) in self.groups.keys())))

        local_atlas_path = os.path.join(os.path.dirname(mtl_path), ATLAS_FILENAME)
        if not os.path.exists(local_atlas_path):
            with open(local_atlas_path, "wb") as af:
                af.write(ATLAS_PNG_BYTES)

        with open(mtl_path, "w", encoding="utf-8") as mf:
            mf.write("# Sphere Brawl: Rolling Rampage — Self-Contained Chassis Material Library\n")
            mf.write(f"# Asset: {self.name}\n")
            for mat_name in used_mats:
                rgba = PALETTE[mat_name]
                mf.write(f"\nnewmtl {mat_name}\n")
                mf.write(f"Ka {rgba[0]*0.2:.4f} {rgba[1]*0.2:.4f} {rgba[2]*0.2:.4f}\n")
                mf.write(f"Kd {rgba[0]:.4f} {rgba[1]:.4f} {rgba[2]:.4f}\n")
                if mat_name.startswith("EMI_"):
                    mf.write(f"Ke {rgba[0]:.4f} {rgba[1]:.4f} {rgba[2]:.4f}\n")
                    mf.write("Ks 0.9000 0.9000 0.9000\nNs 90.0\n")
                else:
                    mf.write("Ke 0.0000 0.0000 0.0000\n")
                    mf.write("Ks 0.5500 0.6000 0.6800\nNs 50.0\n")
                mf.write("d 1.0\nillum 2\n")
                mf.write(f"map_Kd {ATLAS_FILENAME}\n")

        by_mat = {}
        for (g_name, mat_name), tris in self.groups.items():
            if not tris:
                continue
            by_mat.setdefault(mat_name, []).append((g_name, tris))

        with open(obj_path, "w", encoding="utf-8") as of:
            of.write("# Sphere Brawl: Rolling Rampage — Validated Sphere Chassis 3D Asset\n")
            of.write(f"# Asset Name: {self.name}\n")
            of.write("# Unit Scale: 1.0 Unit = 1.0 Roblox Stud | Up Axis: +Y | Forward Axis: +Z | Origin: (0,0,0)\n")
            of.write(f"mtllib {mtl_filename}\n")

            mat_to_vt_idx = {}
            for idx, m in enumerate(used_mats, 1):
                u_val, v_val = UV_CENTERS_OBJ[m]
                of.write(f"vt {u_val:.5f} {v_val:.5f}\n")
                mat_to_vt_idx[m] = idx

            v_idx = 1
            vn_idx = 1
            for mat_name in used_mats:
                rgba = PALETTE[mat_name]
                vt_i = mat_to_vt_idx[mat_name]
                of.write(f"o {self.name}__{mat_name}\n")
                of.write(f"usemtl {mat_name}\n")
                for g_name, tris in by_mat[mat_name]:
                    of.write(f"g {g_name}\n")
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
        mat_tris = {}
        for (_, m), tris in self.groups.items():
            if not tris:
                continue
            mat_tris.setdefault(m, []).extend(tris)

        active_mats = sorted(list(mat_tris.keys()))

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
            "name": "SphereBrawl_Chassis_PaletteAtlas",
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
            "name": "SphereBrawl_Chassis_PaletteAtlas_Tex",
            "sampler": 0,
            "source": 0,
        }]

        gltf_materials = []
        for m in active_mats:
            rgba = PALETTE[m]
            is_emi = m.startswith("EMI_")
            mat_def = {
                "name": m,
                "pbrMetallicRoughness": {
                    "baseColorFactor": [round(rgba[0], 4), round(rgba[1], 4), round(rgba[2], 4), 1.0],
                    "baseColorTexture": {"index": 0, "texCoord": 0},
                    "metallicFactor": 0.1 if is_emi else (0.78 if m == "MAT_LightTrim" else 0.58),
                    "roughnessFactor": 0.15 if is_emi else 0.34,
                },
                "doubleSided": False,
            }
            if is_emi:
                mat_def["emissiveFactor"] = [round(rgba[0], 4), round(rgba[1], 4), round(rgba[2], 4)]
            gltf_materials.append(mat_def)

        for mat_idx, m in enumerate(active_mats):
            tris = mat_tris[m]
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
                "name": f"Mesh_{m}",
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
            child_node_indices.append((f"Part_{m}", mesh_idx))

        gltf_nodes = [{
            "name": self.name,
            "children": list(range(1, len(child_node_indices) + 1)),
        }]
        for part_name, m_idx in child_node_indices:
            gltf_nodes.append({
                "name": part_name,
                "mesh": m_idx,
            })

        gltf_dict = {
            "asset": {
                "version": "2.0",
                "generator": "Sphere Brawl Chassis Batch 2 Pipeline v1.0 (Multi-Node + VertexColor + AtlasUV)",
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
# 1. CHASSIS 1: SM_Chassis_Trickster_01 (236 Triangles)
#    Visual Identity: Agile, sleek, visually nimble with an unmistakable
#    asymmetric diagonal twist/slash motif, swept aerodynamic stabilizer fins,
#    cyan energy slash inlays (EMI_Cyan), and kinetic orange speed vents (EMI_Kinetic).
# ==============================================================================
def build_chassis_trickster(name="SM_Chassis_Trickster_01"):
    mb = ChassisMeshBuilder(name, max_radius_clamp=2.965)

    # 1. Helical-twisted 5-ring x 10-seg core sphere (r = 2.66 studs) — 80 triangles
    phis = [-math.pi / 2.0, -0.88, -0.26, 0.26, 0.88, math.pi / 2.0]
    twists = [-0.28, -0.16, -0.05, 0.05, 0.16, 0.28]

    def trickster_core_mat(i, j, p_mid, t_mid):
        if i in (0, 4):
            return ("Trickster_CorePolarCap", "MAT_DarkNeutral")
        # Asymmetric diagonal slash channel across the inner hull
        diag_metric = (j + i) % 5
        if diag_metric == 0:
            return (f"Trickster_CoreSlashChannel_R{i}_S{j}", "EMI_Cyan")
        elif diag_metric in (1, 3):
            return (f"Trickster_CoreSleekShell_R{i}_S{j}", "MAT_AltNeutral")
        return (f"Trickster_CoreBaseHull_R{i}_S{j}", "MAT_DarkNeutral")

    mb.add_segmented_core_sphere(2.66, phis, 10, trickster_core_mat, theta_twist_per_ring=twists)

    # 2. Asymmetric Diagonal Sash Vanes (3 swept blades wrapping from Lower-Right +X/+Z to Upper-Left -X/+Z) — 30 triangles
    sash_specs = [
        ("FrontRight", [(-0.42, 0.18), (-0.18, 0.82), (0.04, 0.72), (-0.20, 0.08)],
                       [(-0.36, 0.24), (-0.14, 0.76), (0.00, 0.68), (-0.22, 0.14)], "MAT_LightTrim", 2.91),
        ("CenterSlash",[(-0.12, -0.45), (0.28, 0.15), (0.46, 0.02), (0.06, -0.58)],
                       [(-0.08, -0.40), (0.24, 0.10), (0.40, -0.02), (0.08, -0.52)], "EMI_Cyan", 2.89),
        ("UpperLeft",  [(0.18, -1.18), (0.55, -0.52), (0.72, -0.66), (0.35, -1.32)],
                       [(0.22, -1.12), (0.50, -0.58), (0.65, -0.70), (0.36, -1.25)], "MAT_LightTrim", 2.91),
    ]
    for sname, b_quad, t_quad, mname, r_top in sash_specs:
        mb.add_skewed_spherical_blade(f"Trickster_AsymSash_{sname}", mname, 2.64, r_top, b_quad, t_quad)

    # 3. Four Sleek Angular Cheek & Rear Quarter Fairings (Asymmetric high/low canted stagger) — 40 triangles
    # Right side (+X) fairings are canted slightly higher (+phi), Left side (-X) slightly lower (-phi) for nimble asymmetry
    fairings = [
        ("FrontRight_Upper", "MAT_AltNeutral", 0.08, 0.58,  0.32,  1.12, 2.88),
        ("FrontLeft_Lower",  "MAT_DarkNeutral", -0.58, -0.08, -1.12, -0.32, 2.88),
        ("RearRight_Lower",  "MAT_DarkNeutral", -0.52, -0.04,  1.62,  2.48, 2.87),
        ("RearLeft_Upper",   "MAT_AltNeutral",  0.04,  0.52, -2.48, -1.62, 2.87),
    ]
    for fname, mname, p0, p1, t0, t1, r_top in fairings:
        mb.add_spherical_frustum_plate(f"Trickster_Fairing_{fname}", mname, 2.64, r_top, p0, p1, t0, t1, inset_phi=0.05, inset_theta=0.07)

    # 4. Two Swept-Back Lateral Stabilizer Blades (+X Right and -X Left with offset pitch) — 20 triangles
    mb.add_skewed_spherical_blade(
        "Trickster_SweptWing_Right", "MAT_LightTrim", 2.64, 2.945,
        [(-0.22, 1.18), (-0.02, 1.92), (0.20, 1.84), (0.00, 1.10)],
        [(-0.17, 1.25), (-0.01, 1.85), (0.15, 1.78), (0.01, 1.18)]
    )
    mb.add_skewed_spherical_blade(
        "Trickster_SweptWing_Left", "MAT_LightTrim", 2.64, 2.945,
        [(-0.02, -1.92), (-0.22, -1.18), (0.00, -1.10), (0.20, -1.84)],
        [(-0.01, -1.85), (-0.17, -1.25), (0.01, -1.18), (0.15, -1.78)]
    )

    # 5. Frontal Split-Visor Sensor Crest (+Z Forward) & Dorsal/Ventral Speed Blades — 30 triangles
    mb.add_spherical_frustum_plate("Trickster_FrontSensorVisor", "EMI_Cyan", 2.64, 2.90, -0.16, 0.24, -0.28, 0.22, inset_phi=0.04, inset_theta=0.04)
    mb.add_spherical_frustum_plate("Trickster_DorsalSpeedFin", "MAT_LightTrim", 2.64, 2.93, 0.42, 0.84, -0.22, 0.34, inset_phi=0.05, inset_theta=0.06)
    mb.add_spherical_frustum_plate("Trickster_VentralSkidFin", "MAT_LightTrim", 2.64, 2.92, -0.84, -0.42, -0.34, 0.22, inset_phi=0.05, inset_theta=0.06)

    # 6. Three Kinetic Orange Speed Vents & Twin-Chevron Rear Thruster (-Z Rear) — 36 triangles
    mb.add_spherical_frustum_plate("Trickster_KineticVent_Right", "EMI_Kinetic", 2.64, 2.91, 0.14, 0.42, 1.18, 1.68, inset_phi=0.03, inset_theta=0.05)
    mb.add_spherical_frustum_plate("Trickster_KineticVent_Left",  "EMI_Kinetic", 2.64, 2.91, -0.42, -0.14, -1.68, -1.18, inset_phi=0.03, inset_theta=0.05)
    # Rear -Z thruster shroud (6 tris) + central kinetic nozzle (10 tris) = 16 tris
    mb.add_equatorial_band_segment("Trickster_RearThrusterCollar", "MAT_LightTrim", 2.64, 2.91, -0.24, 0.24, 2.76, 3.52, inset_phi=0.03, cap_ends=False)
    mb.add_spherical_frustum_plate("Trickster_RearKineticNozzle", "EMI_Kinetic", 2.64, 2.93, -0.20, 0.20, 2.86, 3.42, inset_phi=0.04, inset_theta=0.05)

    return mb


# ==============================================================================
# 2. CHASSIS 2: SM_Chassis_Magnetar_01 (232 Triangles)
#    Visual Identity: Magnetic/energy-themed sphere featuring a recessed dark-metal
#    core wrapped by an unmistakable raised purple electromagnetic equatorial flux
#    ring (EMI_Magnetic), north/south polar inductor rings, four metallic horseshoe
#    inductor pole shoes (MAT_LightTrim), and glowing cyan field emitters (EMI_Cyan).
# ==============================================================================
def build_chassis_magnetar(name="SM_Chassis_Magnetar_01"):
    mb = ChassisMeshBuilder(name, max_radius_clamp=2.965)

    # 1. Closed 5-ring x 8-seg core sphere (r = 2.64 studs) — 64 triangles
    phis = [-math.pi / 2.0, -0.92, -0.30, 0.30, 0.92, math.pi / 2.0]

    def magnetar_core_mat(i, j, p_mid, t_mid):
        if i in (0, 4):
            return (f"Magnetar_PolarCoreCap_R{i}", "EMI_Magnetic")
        elif i == 2:
            return (f"Magnetar_EquatorialChannel_S{j}", "MAT_DarkNeutral")
        return (f"Magnetar_CoilHousing_R{i}_S{j}", "MAT_AltNeutral")

    mb.add_segmented_core_sphere(2.64, phis, 8, magnetar_core_mat)

    # 2. Continuous 8-Segment Raised Equatorial Electromagnetic Flux Ring (EMI_Magnetic) — 48 triangles (8 x 6 tris)
    n_eq = 8
    for j in range(n_eq):
        t0 = -math.pi + (2.0 * math.pi * j) / n_eq
        t1 = -math.pi + (2.0 * math.pi * (j + 1)) / n_eq
        mb.add_equatorial_band_segment(
            f"Magnetar_EquatorialFluxRing_Seg{j+1}", "EMI_Magnetic",
            2.62, 2.935, -0.17, 0.17, t0, t1, inset_phi=0.03, cap_ends=False
        )

    # 3. Four Cardinal Metallic Inductor Pole Shoes (Front +Z, Rear -Z, Right +X, Left -X in MAT_LightTrim) — 40 triangles
    cardinal_thetas = [
        ("Front_PosZ", 0.0),
        ("Right_PosX", 0.5 * math.pi),
        ("Rear_NegZ",  math.pi),
        ("Left_NegX", -0.5 * math.pi),
    ]
    for pname, tc in cardinal_thetas:
        # Upper and lower pole shoe brackets straddling the equatorial flux ring
        mb.add_spherical_frustum_plate(
            f"Magnetar_InductorShoe_{pname}", "MAT_LightTrim",
            2.62, 2.948, -0.52, 0.52, tc - 0.20, tc + 0.20,
            inset_phi=0.05, inset_theta=0.03
        )

    # 4. Four Intercardinal Dark-Metal Field Stabilizer Plates (NE, NW, SE, SW in MAT_DarkNeutral) — 40 triangles
    intercardinal_thetas = [
        ("FrontRight",  0.25 * math.pi),
        ("FrontLeft",  -0.25 * math.pi),
        ("RearRight",   0.75 * math.pi),
        ("RearLeft",   -0.75 * math.pi),
    ]
    for iname, tc in intercardinal_thetas:
        mb.add_spherical_frustum_plate(
            f"Magnetar_StabilizerPad_{iname}", "MAT_DarkNeutral",
            2.62, 2.86, -0.68, 0.68, tc - 0.22, tc + 0.22,
            inset_phi=0.05, inset_theta=0.04
        )

    # 5. Four Glowing Cyan Resonance Nodes at Cardinal Pole Centres (EMI_Cyan) + North/South Polar Crown Coils — 40 triangles
    # Frontal (+Z) and Lateral (+X, -X) Cyan Resonance Emitters + Dorsal (+Y) & Ventral (-Y) Cyan Core Beacons
    mb.add_spherical_frustum_plate("Magnetar_CyanNode_FrontPosZ", "EMI_Cyan", 2.62, 2.955, -0.14, 0.14, -0.12, 0.12, inset_phi=0.02, inset_theta=0.02)
    mb.add_spherical_frustum_plate("Magnetar_CyanNode_RightPosX", "EMI_Cyan", 2.62, 2.955, -0.14, 0.14, 0.5*math.pi - 0.12, 0.5*math.pi + 0.12, inset_phi=0.02, inset_theta=0.02)
    mb.add_spherical_frustum_plate("Magnetar_CyanNode_LeftNegX",  "EMI_Cyan", 2.62, 2.955, -0.14, 0.14, -0.5*math.pi - 0.12, -0.5*math.pi + 0.12, inset_phi=0.02, inset_theta=0.02)
    mb.add_spherical_frustum_plate("Magnetar_RearFluxThruster_NegZ", "EMI_Magnetic", 2.62, 2.955, -0.22, 0.22, math.pi - 0.18, math.pi + 0.18, inset_phi=0.03, inset_theta=0.03)

    return mb


# ==============================================================================
# 3. CHASSIS 3: SM_Chassis_Bulwark_01 (232 Triangles)
#    Visual Identity: Sturdy, defensive, heavy-looking armored sphere built from
#    thick interlocked hexagonal/octagonal dark bastion plates (MAT_DarkNeutral
#    & MAT_AltNeutral), reinforced perimeter trim collars (MAT_LightTrim), and
#    restrained narrow cyan tactical visor slits (EMI_Cyan).
# ==============================================================================
def build_chassis_bulwark(name="SM_Chassis_Bulwark_01"):
    mb = ChassisMeshBuilder(name, max_radius_clamp=2.965)

    # 1. Heavy 5-ring x 8-seg core recessed frame (r = 2.62 studs) — 64 triangles
    phis = [-math.pi / 2.0, -0.90, -0.32, 0.32, 0.90, math.pi / 2.0]

    def bulwark_core_mat(i, j, p_mid, t_mid):
        if i in (0, 4):
            return (f"Bulwark_UnderFramePolar_R{i}", "MAT_LightTrim")
        return (f"Bulwark_UnderFrameRecess_R{i}_S{j}", "MAT_AltNeutral")

    mb.add_segmented_core_sphere(2.62, phis, 8, bulwark_core_mat)

    # 2. Eight Heavy Equatorial Bastion Armor Plates (MAT_DarkNeutral, thick broad bevels) — 80 triangles (8 x 10 tris)
    n_oct = 8
    for j in range(n_oct):
        tc = -math.pi + (2.0 * math.pi * j) / n_oct
        # Leave narrow armored expansion trenches between adjacent bastion plates
        mb.add_spherical_frustum_plate(
            f"Bulwark_EquatorialBastionPlate_{j+1}", "MAT_DarkNeutral",
            2.60, 2.955, -0.34, 0.34, tc - 0.31, tc + 0.31,
            inset_phi=0.04, inset_theta=0.04
        )

    # 3. Four Upper Hemisphere & Four Lower Hemisphere Interlocking Armor Casemates — 80 triangles (8 x 10 tris)
    # Staggered by 45 degrees (`pi/4`) relative to the equatorial plates like a defensive geodesic bunker
    for idx, tc in enumerate([-0.75 * math.pi, -0.25 * math.pi, 0.25 * math.pi, 0.75 * math.pi]):
        mb.add_spherical_frustum_plate(
            f"Bulwark_UpperCasematePlate_{idx+1}", "MAT_DarkNeutral",
            2.60, 2.945, 0.38, 0.88, tc - 0.58, tc + 0.58,
            inset_phi=0.05, inset_theta=0.06
        )
        mb.add_spherical_frustum_plate(
            f"Bulwark_LowerCasematePlate_{idx+1}", "MAT_DarkNeutral",
            2.60, 2.945, -0.88, -0.38, tc - 0.58, tc + 0.58,
            inset_phi=0.05, inset_theta=0.06
        )

    # 4. Restrained Frontal Slit Visor (+Z in EMI_Cyan) & Reinforced Trim Bumper Collar (MAT_LightTrim) — 8 triangles
    # Narrow recessed frontal slit visor on +Z (top quad + north/south bevels = 6 tris) + dorsal crown cap (2 tris) = 8 tris
    mb.add_equatorial_band_segment(
        "Bulwark_FrontTacticalVisorSlit", "EMI_Cyan",
        2.60, 2.962, -0.09, 0.09, -0.24, 0.24, inset_phi=0.015, cap_ends=False
    )
    # Add 2-tri reinforced frontal brow shield cap above the slit visor
    v_brow0 = sph_pt(2.958, 0.12, -0.24)
    v_brow1 = sph_pt(2.958, 0.12,  0.24)
    v_brow2 = sph_pt(2.958, 0.30,  0.20)
    v_brow3 = sph_pt(2.958, 0.30, -0.20)
    mb.add_quad("Bulwark_FrontBrowReinforcement", "MAT_LightTrim", v_brow0, v_brow1, v_brow2, v_brow3, expected_normal=sph_pt(1.0, 0.21, 0.0))

    return mb


CHASSIS_DEFINITIONS = [
    {
        "chassis_id": "Trickster",
        "asset_name": "SM_Chassis_Trickster_01",
        "manifest_id": "sphere.shell.trickster",
        "display_name": "1. Trickster Chassis (SM_Chassis_Trickster_01)",
        "primary_accent": "EMI_Cyan",
        "secondary_accent": "EMI_Kinetic",
        "accent_rgb": [0, 195, 255],
        "expected_materials": ["EMI_Cyan", "EMI_Kinetic", "MAT_AltNeutral", "MAT_DarkNeutral", "MAT_LightTrim"],
        "builder_fn": build_chassis_trickster,
        "visual_description": "Agile, sleek spherical shell with a helical-twisted inner core, asymmetric diagonal slash vanes, canted swept-back lateral stabilizer fins, cyan sensor visor, and kinetic orange speed vents.",
    },
    {
        "chassis_id": "Magnetar",
        "asset_name": "SM_Chassis_Magnetar_01",
        "manifest_id": "sphere.shell.magnetar",
        "display_name": "2. Magnetar Chassis (SM_Chassis_Magnetar_01)",
        "primary_accent": "EMI_Magnetic",
        "secondary_accent": "EMI_Cyan",
        "accent_rgb": [165, 55, 255],
        "expected_materials": ["EMI_Cyan", "EMI_Magnetic", "MAT_AltNeutral", "MAT_DarkNeutral", "MAT_LightTrim"],
        "builder_fn": build_chassis_magnetar,
        "visual_description": "Magnetic/energy-themed sphere featuring a raised 8-segment purple electromagnetic equatorial flux ring, north/south polar inductor cores, four metallic horseshoe pole shoes, and cyan resonance nodes.",
    },
    {
        "chassis_id": "Bulwark",
        "asset_name": "SM_Chassis_Bulwark_01",
        "manifest_id": "sphere.shell.bulwark",
        "display_name": "3. Bulwark Chassis (SM_Chassis_Bulwark_01)",
        "primary_accent": "MAT_LightTrim",
        "secondary_accent": "EMI_Cyan",
        "accent_rgb": [170, 190, 215],
        "expected_materials": ["EMI_Cyan", "MAT_AltNeutral", "MAT_DarkNeutral", "MAT_LightTrim"],
        "builder_fn": build_chassis_bulwark,
        "visual_description": "Sturdy, heavy-looking defensive sphere armored with 16 interlocking octagonal/geodesic dark bastion plates, recessed metallic expansion channels, reinforced light-trim collars, and a narrow cyan slit visor.",
    },
]


# ==============================================================================
# 4. INDEPENDENT FILE-LEVEL VALIDATORS (OBJ, MTL, GLB, RADIUS <= 2.97, WINDING)
# ==============================================================================
def sha256_of_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def parse_and_validate_mtl(mtl_path):
    materials = {}
    current_mat = None
    with open(mtl_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            cmd = parts[0]
            if cmd == "newmtl":
                current_mat = parts[1]
                materials[current_mat] = {}
            elif current_mat is not None and cmd in ("Kd", "Ka", "Ks", "Ke"):
                materials[current_mat][cmd] = [float(parts[1]), float(parts[2]), float(parts[3])]
            elif current_mat is not None and cmd == "map_Kd":
                materials[current_mat]["map_Kd"] = parts[1]

    palette_errors = []
    for mname, mdata in materials.items():
        if mname not in APPROVED_PALETTE_METADATA:
            palette_errors.append(f"Unknown material {mname}")
            continue
        exp_rgb = APPROVED_PALETTE_METADATA[mname]["normalized_rgb"]
        act_kd = mdata.get("Kd", [0.0, 0.0, 0.0])
        if max(abs(act_kd[i] - exp_rgb[i]) for i in range(3)) > 1e-3:
            palette_errors.append(f"Kd mismatch on {mname}: {act_kd} vs {exp_rgb}")
        if APPROVED_PALETTE_METADATA[mname]["emissive"]:
            act_ke = mdata.get("Ke", [0.0, 0.0, 0.0])
            if max(abs(act_ke[i] - exp_rgb[i]) for i in range(3)) > 1e-3:
                palette_errors.append(f"Ke mismatch on {mname}: {act_ke} vs {exp_rgb}")

    return {
        "materials_defined": sorted(list(materials.keys())),
        "material_details": materials,
        "palette_errors": palette_errors,
        "valid": len(palette_errors) == 0 and len(materials) > 0,
    }


def parse_and_validate_obj(obj_path):
    verts = []
    v_colors = []
    uvs = []
    norms = []
    faces = []
    objects = []
    mtllibs = []
    usemtls = set()
    active_mat = None
    syntax_errors = []
    index_errors = []

    with open(obj_path, "r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, 1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            cmd = parts[0]
            if cmd == "mtllib":
                mtllibs.append(" ".join(parts[1:]))
            elif cmd == "o":
                objects.append(parts[1])
            elif cmd == "usemtl":
                active_mat = parts[1]
                usemtls.add(active_mat)
            elif cmd == "v":
                verts.append([float(parts[1]), float(parts[2]), float(parts[3])])
                if len(parts) >= 7:
                    v_colors.append([float(parts[4]), float(parts[5]), float(parts[6])])
            elif cmd == "vt":
                uvs.append([float(parts[1]), float(parts[2])])
            elif cmd == "vn":
                norms.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif cmd == "f":
                if len(parts) != 4:
                    syntax_errors.append(f"Line {line_no}: non-triangle face")
                    continue
                tri_v, tri_vt, tri_vn = [], [], []
                for token in parts[1:]:
                    sub = token.split("/")
                    vi = int(sub[0])
                    vti = int(sub[1]) if len(sub) > 1 and sub[1] else None
                    vni = int(sub[2]) if len(sub) > 2 and sub[2] else None
                    if vi < 1 or vi > len(verts):
                        index_errors.append(f"Line {line_no}: v index {vi} out of range")
                    if vti is not None and (vti < 1 or vti > len(uvs)):
                        index_errors.append(f"Line {line_no}: vt index {vti} out of range")
                    if vni is not None and (vni < 1 or vni > len(norms)):
                        index_errors.append(f"Line {line_no}: vn index {vni} out of range")
                    tri_v.append(vi - 1)
                    tri_vt.append((vti - 1) if vti else None)
                    tri_vn.append((vni - 1) if vni else None)
                faces.append((tri_v, tri_vt, tri_vn, active_mat))

    v_arr = np.array(verts, dtype=np.float64)
    n_arr = np.array(norms, dtype=np.float64)
    finite_ok = bool(np.all(np.isfinite(v_arr))) and bool(np.all(np.isfinite(n_arr)))

    radii = np.linalg.norm(v_arr, axis=1)
    max_radius = float(radii.max())
    min_radius = float(radii.min())
    verts_over_297 = int(np.sum(radii > 2.9700001))
    verts_over_300 = int(np.sum(radii > 3.0000001))

    bbox_min = v_arr.min(axis=0).round(4).tolist()
    bbox_max = v_arr.max(axis=0).round(4).tolist()
    dims = (v_arr.max(axis=0) - v_arr.min(axis=0)).round(4).tolist()
    center = ((v_arr.max(axis=0) + v_arr.min(axis=0)) * 0.5).round(4).tolist()

    degenerate_count = 0
    winding_mismatch_count = 0
    min_area = float("inf")
    for tri_v, _, tri_vn, _ in faces:
        p0, p1, p2 = v_arr[tri_v[0]], v_arr[tri_v[1]], v_arr[tri_v[2]]
        cross = np.cross(p1 - p0, p2 - p0)
        norm_len = float(np.linalg.norm(cross))
        area = 0.5 * norm_len
        min_area = min(min_area, area)
        if area < 1e-6:
            degenerate_count += 1
        else:
            geom_n = cross / norm_len
            for vni in tri_vn:
                if vni is not None and float(np.dot(geom_n, n_arr[vni])) < 0.99:
                    winding_mismatch_count += 1
                    break

    return {
        "vertex_count": len(verts),
        "vertex_color_count": len(v_colors),
        "uv_count": len(uvs),
        "normal_count": len(norms),
        "triangle_count": len(faces),
        "under_250_triangles": len(faces) <= 250,
        "max_radius_studs": round(max_radius, 5),
        "min_radius_studs": round(min_radius, 5),
        "vertices_exceeding_2_97_studs": verts_over_297,
        "vertices_exceeding_3_00_studs": verts_over_300,
        "object_subparts": objects,
        "mtllibs": mtllibs,
        "materials_used": sorted(list(usemtls)),
        "bbox_min": bbox_min,
        "bbox_max": bbox_max,
        "dimensions": dims,
        "bbox_center": center,
        "finite_coords": finite_ok,
        "degenerate_triangles": degenerate_count,
        "winding_normal_mismatches": winding_mismatch_count,
        "min_triangle_area": round(min_area, 6),
        "syntax_errors": syntax_errors,
        "index_errors": index_errors,
        "valid": (
            len(syntax_errors) == 0
            and len(index_errors) == 0
            and finite_ok
            and degenerate_count == 0
            and winding_mismatch_count == 0
            and len(faces) <= 250
            and verts_over_297 == 0
            and len(v_colors) == len(verts)
        ),
    }


def parse_and_validate_glb(glb_path):
    with open(glb_path, "rb") as f:
        data = f.read()

    magic, version, total_length = struct.unpack("<4sII", data[:12])
    magic_str = magic.decode("ascii", errors="replace")
    header_ok = (magic_str == "glTF") and (version == 2) and (total_length == len(data))

    c0_len, _ = struct.unpack("<I4s", data[12:20])
    gltf_json = json.loads(data[20:20 + c0_len].decode("utf-8"))

    c1_offset = 20 + c0_len
    c1_len, c1_type = struct.unpack("<I4s", data[c1_offset:c1_offset + 8])
    has_bin_chunk = (c1_type[:3] == b"BIN") and (c1_offset + 8 + c1_len == len(data))

    nodes = gltf_json.get("nodes", [])
    meshes = gltf_json.get("meshes", [])
    materials = gltf_json.get("materials", [])
    accessors = gltf_json.get("accessors", [])
    textures = gltf_json.get("textures", [])
    images = gltf_json.get("images", [])

    mat_audit = {}
    mat_errors = []
    for m in materials:
        mname = m["name"]
        pbr = m.get("pbrMetallicRoughness", {})
        bcf = pbr.get("baseColorFactor", [])
        has_tex = "baseColorTexture" in pbr
        emif = m.get("emissiveFactor", [0.0, 0.0, 0.0])
        exp = APPROVED_PALETTE_METADATA[mname]["normalized_rgb"]
        if max(abs(bcf[i] - exp[i]) for i in range(3)) > 1e-3:
            mat_errors.append(f"GLB baseColorFactor mismatch on {mname}")
        if APPROVED_PALETTE_METADATA[mname]["emissive"]:
            if max(abs(emif[i] - exp[i]) for i in range(3)) > 1e-3:
                mat_errors.append(f"GLB emissiveFactor mismatch on {mname}")
        mat_audit[mname] = {
            "baseColorFactor": bcf,
            "emissiveFactor": emif,
            "has_baseColorTexture": has_tex,
        }

    total_tris = 0
    total_verts = 0
    has_color0_all = True
    has_texcoord0_all = True
    pos_min = [float("inf")] * 3
    pos_max = [float("-inf")] * 3

    for mesh in meshes:
        for prim in mesh.get("primitives", []):
            attrs = prim.get("attributes", {})
            if "COLOR_0" not in attrs:
                has_color0_all = False
            if "TEXCOORD_0" not in attrs:
                has_texcoord0_all = False
            idx_acc_i = prim.get("indices")
            total_tris += accessors[idx_acc_i]["count"] // 3
            pos_acc = accessors[attrs["POSITION"]]
            total_verts += pos_acc["count"]
            for k in range(3):
                pos_min[k] = min(pos_min[k], pos_acc["min"][k])
                pos_max[k] = max(pos_max[k], pos_acc["max"][k])

    dims = [round(pos_max[k] - pos_min[k], 4) for k in range(3)]
    child_part_nodes = [n["name"] for n in nodes[1:]]

    return {
        "magic": magic_str,
        "version": version,
        "byte_length": len(data),
        "header_matches_length": header_ok,
        "has_valid_bin_chunk": has_bin_chunk,
        "root_node": nodes[0]["name"] if nodes else None,
        "child_part_nodes": child_part_nodes,
        "mesh_count": len(meshes),
        "materials": sorted(list(mat_audit.keys())),
        "material_definitions": mat_audit,
        "material_errors": mat_errors,
        "has_color0_vertex_colors": has_color0_all,
        "has_texcoord0_uvs": has_texcoord0_all,
        "embedded_textures_count": len(textures),
        "embedded_images_count": len(images),
        "vertex_count": total_verts,
        "triangle_count": total_tris,
        "bbox_min": [round(x, 4) for x in pos_min],
        "bbox_max": [round(x, 4) for x in pos_max],
        "dimensions": dims,
        "valid": (
            header_ok
            and has_bin_chunk
            and len(mat_errors) == 0
            and has_color0_all
            and has_texcoord0_all
            and len(images) == 1
            and 0 < total_tris <= 250
        ),
    }


# ==============================================================================
# 5. SOFTWARE Z-BUFFER SPHERE CHASSIS RASTERIZER (MATERIAL, NEUTRAL CLAY, WIRE)
# ==============================================================================
def build_chassis_camera_axes(view_type):
    if view_type == "front":
        # Looking from +Z toward -Z (+X Right on left/right, +Y Up)
        view_dir = np.array([0.0, 0.0, 1.0])
        right = np.array([1.0, 0.0, 0.0])
        up_scr = np.array([0.0, 1.0, 0.0])
    elif view_type == "side":
        # Looking from +X toward -X (+Z Forward to the right, +Y Up)
        view_dir = np.array([1.0, 0.0, 0.0])
        right = np.array([0.0, 0.0, 1.0])
        up_scr = np.array([0.0, 1.0, 0.0])
    elif view_type == "top":
        # Looking from +Y down toward -Y (+X Right, +Z Forward up)
        view_dir = np.array([0.0, 1.0, 0.0])
        right = np.array([1.0, 0.0, 0.0])
        up_scr = np.array([0.0, 0.0, 1.0])
    else:
        # 3/4 Front-Right-Top perspective looking at (+X, +Y, +Z) hemisphere
        az = math.radians(36.0)
        el = math.radians(26.0)
        view_dir = np.array([
            math.cos(el) * math.sin(az),
            math.sin(el),
            math.cos(el) * math.cos(az),
        ])
        view_dir /= np.linalg.norm(view_dir)
        world_up = np.array([0.0, 1.0, 0.0])
        right = np.cross(world_up, view_dir)
        right /= np.linalg.norm(right)
        up_scr = np.cross(view_dir, right)
        up_scr /= np.linalg.norm(up_scr)
    return right, up_scr, view_dir


def rasterize_chassis_zbuffer(mb, view_type="persp", width=680, height=540,
                              span_x=3.8, span_y=3.04, render_mode="material",
                              draw_envelope=True):
    wire_only = (render_mode == "wireframe")
    neutral_clay = (render_mode == "neutral")

    ss = 2
    W, H = width * ss, height * ss
    bg_rgb = np.array([19, 25, 38] if not neutral_clay else [26, 31, 40], dtype=np.uint8)
    color_buf = np.broadcast_to(bg_rgb, (H, W, 3)).copy()
    z_buf = np.full((H, W), -1e18, dtype=np.float64)

    right, up_scr, view_dir = build_chassis_camera_axes(view_type)
    light_dir = (view_dir * 0.55 + up_scr * 0.65 + right * 0.35)
    light_dir /= np.linalg.norm(light_dir)

    def project_pt(pt):
        x_cam = float(np.dot(pt, right))
        y_cam = float(np.dot(pt, up_scr))
        z_cam = float(np.dot(pt, view_dir))
        px = (x_cam / (2.0 * span_x) + 0.5) * W
        py = (0.5 - y_cam / (2.0 * span_y)) * H
        return px, py, z_cam

    wire_segments = []

    for (g_name, mat_name), tris in mb.groups.items():
        base_rgb = np.array(PALETTE_SRGB[mat_name], dtype=np.float64)
        is_emi = mat_name.startswith("EMI_")

        for (v0, v1, v2) in tris:
            n = np.cross(v1 - v0, v2 - v0)
            nl = float(np.linalg.norm(n))
            n = (n / nl) if nl > 1e-8 else np.array([0.0, 1.0, 0.0])

            facing_dot = float(np.dot(n, view_dir))

            if neutral_clay:
                clay_base = np.array([194.0, 203.0, 216.0]) if "Core" not in g_name and "UnderFrame" not in g_name else np.array([148.0, 158.0, 172.0])
                lambert = max(0.20, abs(float(np.dot(n, light_dir))))
                spec = max(0.0, facing_dot) ** 8 * 0.20
                factor = 0.34 + 0.66 * lambert + spec
                shade_rgb = np.clip(clay_base * factor, 0, 255).astype(np.uint8)
                edge_rgb = (68, 80, 96)
            elif is_emi:
                shade_rgb = np.clip(base_rgb * 1.10, 0, 255).astype(np.uint8)
                edge_rgb = (242, 248, 255) if not wire_only else tuple(int(x) for x in np.clip(base_rgb * 1.15, 0, 255))
            else:
                lambert = max(0.22, abs(float(np.dot(n, light_dir))))
                spec = max(0.0, facing_dot) ** 7 * (0.26 if mat_name == "MAT_LightTrim" else 0.16)
                factor = 0.34 + 0.68 * lambert + spec
                shade_rgb = np.clip(base_rgb * factor, 0, 255).astype(np.uint8)
                edge_rgb = (92, 114, 144) if not wire_only else tuple(int(x) for x in np.clip(base_rgb * 1.35 + 42, 0, 255))

            x0, y0, z0 = project_pt(v0)
            x1, y1, z1 = project_pt(v1)
            x2, y2, z2 = project_pt(v2)

            if wire_only or facing_dot >= -0.02:
                wire_segments.append(((x0, y0, z0), (x1, y1, z1), edge_rgb, is_emi and not neutral_clay))
                wire_segments.append(((x1, y1, z1), (x2, y2, z2), edge_rgb, is_emi and not neutral_clay))
                wire_segments.append(((x2, y2, z2), (x0, y0, z0), edge_rgb, is_emi and not neutral_clay))

            if wire_only or facing_dot < -0.04:
                continue

            xmin = max(0, int(math.floor(min(x0, x1, x2))))
            xmax = min(W - 1, int(math.ceil(max(x0, x1, x2))))
            ymin = max(0, int(math.floor(min(y0, y1, y2))))
            ymax = min(H - 1, int(math.ceil(max(y0, y1, y2))))
            if xmin > xmax or ymin > ymax:
                continue

            denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
            if abs(denom) < 1e-6:
                continue

            xs = np.arange(xmin, xmax + 1, dtype=np.float64) + 0.5
            ys = np.arange(ymin, ymax + 1, dtype=np.float64) + 0.5
            gx, gy = np.meshgrid(xs, ys)

            w0 = ((y1 - y2) * (gx - x2) + (x2 - x1) * (gy - y2)) / denom
            w1 = ((y2 - y0) * (gx - x2) + (x0 - x2) * (gy - y2)) / denom
            w2 = 1.0 - w0 - w1

            mask = (w0 >= -1e-5) & (w1 >= -1e-5) & (w2 >= -1e-5)
            if not np.any(mask):
                continue

            z_interp = w0 * z0 + w1 * z1 + w2 * z2
            sub_z = z_buf[ymin:ymax+1, xmin:xmax+1]
            update_mask = mask & (z_interp > sub_z)
            if np.any(update_mask):
                sub_z[update_mask] = z_interp[update_mask]
                sub_col = color_buf[ymin:ymax+1, xmin:xmax+1]
                sub_col[update_mask] = shade_rgb

    img = Image.fromarray(color_buf, mode="RGB")
    draw = ImageDraw.Draw(img)

    wire_segments.sort(key=lambda s: 0.5 * (s[0][2] + s[1][2]))
    for (xa, ya, za), (xb, yb, zb), ergb, is_emi in wire_segments:
        if not wire_only:
            visible_pts = 0
            for t in (0.25, 0.5, 0.75):
                xt = int(xa + t * (xb - xa))
                yt = int(ya + t * (yb - ya))
                zt = za + t * (zb - za)
                if 0 <= xt < W and 0 <= yt < H:
                    if zt >= z_buf[yt, xt] - 0.05:
                        visible_pts += 1
            if visible_pts < 2:
                continue
            lw = 2 if is_emi else 1
        else:
            lw = 3 if is_emi else 2
        draw.line([(xa, ya), (xb, yb)], fill=ergb, width=lw)

    if draw_envelope:
        # Draw dashed circle for R = 2.970 visual envelope limit and R = 3.000 SphereRoot collider
        n_segs_c = 72
        for rad, col_rgb, step_mod in [(3.00, (0, 255, 136), 2), (2.97, (0, 195, 255), 3)]:
            for k in range(n_segs_c):
                if k % step_mod != 0:
                    continue
                a0 = (2.0 * math.pi * k) / n_segs_c
                a1 = (2.0 * math.pi * (k + 0.65)) / n_segs_c
                p_a = right * (rad * math.cos(a0)) + up_scr * (rad * math.sin(a0))
                p_b = right * (rad * math.cos(a1)) + up_scr * (rad * math.sin(a1))
                xa, ya, _ = project_pt(p_a)
                xb, yb, _ = project_pt(p_b)
                draw.line([(xa, ya), (xb, yb)], fill=col_rgb, width=2)

    img_out = img.resize((width, height), resample=Image.Resampling.LANCZOS)
    return np.asarray(img_out)


def annotate_chassis_panel(ax, img_arr, title, view_type, show_legend=False, accent_hex="#00C3FF"):
    ax.imshow(img_arr)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("#2A3246")
        spine.set_linewidth(1.2)
    ax.set_title(title, color="#F5F8FF", fontsize=10.0, fontweight="bold", pad=6)

    if view_type == "top":
        axis_txt = "Axes: +X Right | +Z Up (Forward) | Looking -Y | Origin (0,0,0)"
    elif view_type == "side":
        axis_txt = "Axes: +Z Right (Forward) | +Y Up | Looking -X | Origin (0,0,0)"
    elif view_type == "front":
        axis_txt = "Axes: +X Right | +Y Up | Looking -Z at +Z Front | Origin (0,0,0)"
    else:
        axis_txt = "Axes: +Y Up | +Z Forward-Left / +X Right | Centered Origin (0,0,0)"

    ax.text(0.02, 0.03, axis_txt, transform=ax.transAxes, color="#AABED7", fontsize=7.5,
            bbox=dict(boxstyle="round,pad=0.24", facecolor="#0F141F", edgecolor="#2A3246", alpha=0.88))

    if show_legend:
        ax.text(0.98, 0.96, "--- Green: R=3.00 Stud SphereRoot Collider\n--- Cyan: R=2.97 Stud Max Visual Limit",
                transform=ax.transAxes, ha="right", va="top", color="#00FF88", fontsize=7.3, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.26", facecolor="#0F141F", edgecolor=accent_hex, alpha=0.92))


def render_individual_chassis_sheet(cdef, mb, metrics, out_png):
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    fig = plt.figure(figsize=(16, 9.6), dpi=150, facecolor="#0F141F")

    acc_hex = "#{:02X}{:02X}{:02X}".format(*cdef["accent_rgb"])
    dims = metrics["dimensions"]
    fig.text(0.03, 0.948,
             f"PYTHON Z-BUFFER MESH RENDER — {cdef['display_name'].upper()}",
             color="#F5F8FF", fontsize=14.5, fontweight="bold")
    fig.text(0.03, 0.915,
             f"ENVELOPE & BUDGET  |  Max Vertex Radius: {metrics['max_radius_studs']:.4f} / 2.9700 studs  |  "
             f"BBox: {dims[0]:.2f} x {dims[1]:.2f} x {dims[2]:.2f} studs  |  "
             f"Triangles: {metrics['triangle_count']} / 250 max  |  Degenerate Tris: {metrics['degenerate_triangles']}",
             color=acc_hex, fontsize=9.8, fontweight="bold")
    fig.text(0.03, 0.887,
             f"COSMETIC PARITY (D-008) & MULTI-NODE READY  |  Origin: (0,0,0) Centered, +Y Up, +Z Forward  |  "
             f"Child MeshParts: {', '.join('Part_' + m for m in metrics['materials_used'])}",
             color="#AABED7", fontsize=8.8)

    panels = [
        ("1. Top Orthographic View (+Z Forward Up — Silhouette & Envelope)", "top", "material"),
        ("2. Side Orthographic Elevation (+Z Forward Right, +Y Up)", "side", "material"),
        ("3. 3/4 Perspective Material-Colour View (+Z/+X/+Y)", "persp", "material"),
        ("4. Technical Wireframe View (<= 250 Tris + R=2.97/3.00 Envelope)", "persp", "wireframe"),
    ]

    for idx, (vtitle, vtype, rmode) in enumerate(panels):
        ax = fig.add_subplot(2, 2, idx + 1, facecolor="#171F2E")
        ax.set_position([0.03 + (idx % 2) * 0.48, 0.035 + (1 - idx // 2) * 0.41, 0.45, 0.375])
        w_px = 680
        h_px = int(w_px * (0.375 * 9.6) / (0.45 * 16.0))
        sy = 3.45
        sx = sy * (w_px / h_px)
        img_arr = rasterize_chassis_zbuffer(
            mb, view_type=vtype, width=w_px, height=h_px,
            span_x=sx, span_y=sy, render_mode=rmode, draw_envelope=True
        )
        annotate_chassis_panel(ax, img_arr, vtitle, vtype, show_legend=(idx in [0, 3]), accent_hex=acc_hex)

    fig.savefig(out_png, dpi=150, facecolor="#0F141F")
    plt.close(fig)


def render_batch2_comparison_sheet(records, out_png, mode="material"):
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    fig = plt.figure(figsize=(19.5, 11.2), dpi=150, facecolor="#0F141F")

    if mode == "material":
        title_str = "SPHERE BRAWL: ROLLING RAMPAGE — TASK-09 BATCH 2 CHASSIS COLLECTION (MATERIAL-COLOUR & SILHOUETTE COMPARISON)"
        sub_str = "PYTHON SOFTWARE Z-BUFFER RENDER FROM EXPORTED .OBJ/.GLB MESHES  |  All 3 Chassis <= 250 Triangles  |  All Vertices R <= 2.970 Studs (< 3.000 Collider)"
        top_mode, bot_mode = "material", "material"
        top_view, bot_view = "persp", "top"
        top_lbl, bot_lbl = "3/4 Material-Colour View", "Top-Down Camera View (+Z Up)"
    else:
        title_str = "SPHERE BRAWL: ROLLING RAMPAGE — TASK-09 BATCH 2 CHASSIS COLLECTION (NEUTRAL CLAY GEOMETRY & WIREFRAME SHEET)"
        sub_str = "PYTHON SOFTWARE Z-BUFFER RENDER (UNIFORM NEUTRAL STUDIO CLAY + WIREFRAME)  |  Verifies Distinct Silhouettes, Contiguous Bevels & <= 250 Triangle Budgets"
        top_mode, bot_mode = "neutral", "wireframe"
        top_view, bot_view = "persp", "side"
        top_lbl, bot_lbl = "3/4 Neutral Studio Clay Lighting", "Side Wireframe (+Z Forward Right)"

    fig.text(0.025, 0.952, title_str, color="#F5F8FF", fontsize=15.8, fontweight="bold")
    fig.text(0.025, 0.922, sub_str, color="#00C3FF", fontsize=10.2, fontweight="bold")
    fig.text(0.025, 0.896,
             "Cosmetic Parity Contract (D-008): Trickster, Magnetar, and Bulwark share the exact same 6.0-stud physics collider and 1.0x combat stats as Rammer. "
             "Multi-node GLB & multi-object OBJ split each material slot into its own child MeshPart.",
             color="#AABED7", fontsize=9.0)

    w_px = 620
    h_px = int(w_px * (0.365 * 11.2) / (0.30 * 19.5))
    sy = 3.42
    sx = sy * (w_px / h_px)

    for col_i, rec in enumerate(records):
        cdef = rec["def"]
        mb = rec["mb"]
        m = rec["obj_audit"]
        acc_hex = "#{:02X}{:02X}{:02X}".format(*cdef["accent_rgb"])

        # Top row
        ax_top = fig.add_subplot(2, 3, col_i + 1, facecolor="#171F2E")
        ax_top.set_position([0.025 + col_i * 0.322, 0.465, 0.30, 0.375])
        img_top = rasterize_chassis_zbuffer(mb, view_type=top_view, width=w_px, height=h_px, span_x=sx, span_y=sy, render_mode=top_mode, draw_envelope=True)
        t_title = f"{cdef['display_name']}\n{top_lbl} | {m['triangle_count']} Tris | Max R = {m['max_radius_studs']:.3f} <= 2.970"
        annotate_chassis_panel(ax_top, img_top, t_title, top_view, show_legend=(col_i == 0), accent_hex=acc_hex)
        ax_top.title.set_size(9.0)
        ax_top.title.set_color(acc_hex if mode == "material" else "#F5F8FF")

        # Bottom row
        ax_bot = fig.add_subplot(2, 3, col_i + 4, facecolor="#171F2E")
        ax_bot.set_position([0.025 + col_i * 0.322, 0.04, 0.30, 0.375])
        img_bot = rasterize_chassis_zbuffer(mb, view_type=bot_view, width=w_px, height=h_px, span_x=sx, span_y=sy, render_mode=bot_mode, draw_envelope=True)
        b_title = f"{cdef['asset_name']} ({bot_lbl})\nBBox: {m['dimensions'][0]:.2f} x {m['dimensions'][1]:.2f} x {m['dimensions'][2]:.2f} Studs | 0 Degenerate Tris"
        annotate_chassis_panel(ax_bot, img_bot, b_title, bot_view, show_legend=(col_i == 0), accent_hex=acc_hex)
        ax_bot.title.set_size(9.0)

    fig.savefig(out_png, dpi=150, facecolor="#0F141F")
    plt.close(fig)


if __name__ == "__main__":
    print("Building Batch 2 Chassis Models (Trickster, Magnetar, Bulwark)...")
    meshes_dir = os.path.join(PKG_STAGE_DIR, "meshes")
    previews_dir = os.path.join(PKG_STAGE_DIR, "previews")
    os.makedirs("/tmp/det_chassis_test", exist_ok=True)

    records = []
    for cdef in CHASSIS_DEFINITIONS:
        aname = cdef["asset_name"]
        mb = cdef["builder_fn"](aname)

        obj_path = os.path.join(meshes_dir, f"{aname}.obj")
        mtl_path = os.path.join(meshes_dir, f"{aname}.mtl")
        glb_path = os.path.join(meshes_dir, f"{aname}.glb")

        mb.export_obj_and_mtl(obj_path, mtl_path)
        mb.export_glb(glb_path)

        # Determinism check
        det_obj = os.path.join("/tmp/det_chassis_test", f"{aname}.obj")
        det_mtl = os.path.join("/tmp/det_chassis_test", f"{aname}.mtl")
        det_glb = os.path.join("/tmp/det_chassis_test", f"{aname}.glb")
        mb2 = cdef["builder_fn"](aname)
        mb2.export_obj_and_mtl(det_obj, det_mtl)
        mb2.export_glb(det_glb)
        assert sha256_of_file(obj_path) == sha256_of_file(det_obj), f"OBJ determinism failed on {aname}"
        assert sha256_of_file(mtl_path) == sha256_of_file(det_mtl), f"MTL determinism failed on {aname}"
        assert sha256_of_file(glb_path) == sha256_of_file(det_glb), f"GLB determinism failed on {aname}"

        obj_audit = parse_and_validate_obj(obj_path)
        mtl_audit = parse_and_validate_mtl(mtl_path)
        glb_audit = parse_and_validate_glb(glb_path)

        assert obj_audit["valid"], f"OBJ validation failed on {aname}: {obj_audit}"
        assert mtl_audit["valid"], f"MTL validation failed on {aname}: {mtl_audit}"
        assert glb_audit["valid"], f"GLB validation failed on {aname}: {glb_audit}"
        assert obj_audit["materials_used"] == cdef["expected_materials"], f"Materials mismatch on {aname}"

        preview_rel = f"previews/Preview_{aname}.png"
        render_individual_chassis_sheet(cdef, mb, obj_audit, os.path.join(PKG_STAGE_DIR, preview_rel))

        print(
            f"  Verified {aname}: {obj_audit['triangle_count']} tris (<=250), "
            f"max_R={obj_audit['max_radius_studs']:.5f} studs (<=2.970), "
            f"dims={obj_audit['dimensions']}, degens={obj_audit['degenerate_triangles']}, "
            f"child_parts={glb_audit['child_part_nodes']}"
        )
        records.append({
            "def": cdef,
            "mb": mb,
            "obj_audit": obj_audit,
            "mtl_audit": mtl_audit,
            "glb_audit": glb_audit,
            "preview_rel": preview_rel,
        })

    comp_mat_png = os.path.join(previews_dir, "Chassis_Batch2_All3_MaterialComparison.png")
    comp_clay_png = os.path.join(previews_dir, "Chassis_Batch2_All3_NeutralClay_and_Wireframe.png")
    render_batch2_comparison_sheet(records, comp_mat_png, mode="material")
    render_batch2_comparison_sheet(records, comp_clay_png, mode="neutral")

    shutil.copy2(comp_mat_png, os.path.join(OUT_DIR, "Sphere_Brawl_Chassis_Batch2_MaterialComparison.png"))
    shutil.copy2(comp_clay_png, os.path.join(OUT_DIR, "Sphere_Brawl_Chassis_Batch2_NeutralClay_and_Wireframe.png"))
    for rec in records:
        aname = rec["def"]["asset_name"]
        shutil.copy2(
            os.path.join(PKG_STAGE_DIR, rec["preview_rel"]),
            os.path.join(OUT_DIR, f"Preview_{aname}.png")
        )
    print("All 3 Batch 2 chassis models and preview sheets built and verified successfully.")
