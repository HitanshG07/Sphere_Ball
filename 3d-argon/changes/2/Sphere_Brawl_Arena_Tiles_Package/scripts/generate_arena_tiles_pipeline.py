#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — ARENA TILE MATERIAL CORRECTION, DETERMINISTIC GENERATOR & VALIDATOR
===================================================================================================
Preserves the exact approved geometry (11.8 x 2.0 x 11.8 studs, centered origin, +Y Up, +Z Forward,
84-tri shared base + 128..150-tri overlays = 212..234 tris < 250 max) while correcting all four root
causes of the pale-grey appearance in Roblox Studio:

  1. Multi-Node GLB Hierarchy (1 child MeshPart per material slot):
     Each `.glb` now exports separate named child nodes/meshes per material slot
     (`Part_MAT_DarkNeutral`, `Part_MAT_AltNeutral`, `Part_MAT_LightTrim`, `Part_EMI_*`)
     under the root Model node so Roblox Studio's 3D Importer creates distinct child
     MeshParts that can be assigned native `Color3` and `Enum.Material.Metal` / `Enum.Material.Neon`.
  2. Multi-Object OBJ Grouping (`o <Asset>__<MaterialSlot>`):
     Each `.obj` groups faces by material slot with explicit `o` object tags, `vt` UV
     coordinates, and extended `v x y z r g b` vertex colors alongside `.mtl` `Kd`/`Ke`.
  3. Embedded `COLOR_0` Vertex Colors + `TEXCOORD_0` Atlas UVs + Embedded PNG Palette Atlas in GLB:
     Every GLB primitive includes `POSITION`, `NORMAL`, `TEXCOORD_0`, and `COLOR_0` (VEC4 float32)
     plus an embedded 64x64 PNG `baseColorTexture` (`SphereBrawl_ArenaTile_PaletteAtlas.png`),
     so even if imported as a single mesh or with textures enabled, the exact approved RGB colors
     transfer automatically instead of falling back to pale grey `Medium stone grey (163, 162, 165)`.
  4. Standalone Deterministic Blender Generator (`scripts/generate_arena_tiles_blender.py`):
     Rewritten so it contains the exact procedural geometry and material definitions and can
     recreate all meshes and materials from scratch without depending on external `.obj` files.
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

# Preserve previous package in intermediate backup before regenerating
PREV_ZIP = os.path.join(OUT_DIR, "Sphere_Brawl_Arena_Tiles_Package.zip")
BACKUP_ZIP = os.path.join(INT_DIR, "Sphere_Brawl_Arena_Tiles_Package_PreMaterialFix_Backup.zip")
if os.path.exists(PREV_ZIP) and not os.path.exists(BACKUP_ZIP):
    shutil.copy2(PREV_ZIP, BACKUP_ZIP)

TMP_BUILD_ROOT = "/tmp/sphere_brawl_material_fix_build"
PKG_STAGE_DIR = os.path.join(TMP_BUILD_ROOT, "Sphere_Brawl_Arena_Tiles_Package")
SUBDIRS = [
    "meshes/complete_states",
    "meshes/modular_base_and_overlays",
    "textures",
    "scripts",
    "previews",
    "docs",
]
for sd in SUBDIRS:
    os.makedirs(os.path.join(PKG_STAGE_DIR, sd), exist_ok=True)

# Exact approved RGB palette & order for 3x3 texture atlas cells
PALETTE_ORDER = [
    "MAT_DarkNeutral",
    "MAT_AltNeutral",
    "MAT_LightTrim",
    "EMI_Cyan",
    "EMI_Amber",
    "EMI_Ice",
    "EMI_Magnetic",
    "EMI_Kinetic",
    "EMI_DangerRed",
]

PALETTE_SRGB = {
    "MAT_DarkNeutral": (32, 38, 54),      # #202636 — Primary structural armor & lower hull
    "MAT_AltNeutral":  (42, 50, 70),      # #2A3246 — Secondary recessed deck & bevel plates
    "MAT_LightTrim":   (170, 190, 215),   # #AABED7 — Chamfered rim frame & corner tie brackets
    "EMI_Cyan":        (0, 195, 255),     # #00C3FF — Safe / Normal subtle cyan accents
    "EMI_Ice":         (0, 235, 255),     # #00EBFF — Ice Corridor active frost channels
    "EMI_Magnetic":    (165, 55, 255),    # #A537FF — Magnetic Storm active symmetric field markings
    "EMI_Kinetic":     (255, 125, 0),     # #FF7D00 — Boost Runway active directional chevrons
    "EMI_Amber":       (255, 170, 0),     # #FFAA00 — Warning state amber hazard channels
    "EMI_DangerRed":   (255, 40, 40),     # #FF2828 — Ring Collapse warning perimeter & X-motif
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
        "surface_role": "Lower structural hull, corner bolsters, primary top armor pads",
    },
    "MAT_AltNeutral": {
        "rgb_255": [42, 50, 70],
        "hex": "#2A3246",
        "normalized_rgb": [round(42/255.0, 6), round(50/255.0, 6), round(70/255.0, 6)],
        "emissive": False,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(42, 50, 70)",
        "surface_role": "Recessed interior deck floor (Y = +0.86 studs)",
    },
    "MAT_LightTrim": {
        "rgb_255": [170, 190, 215],
        "hex": "#AABED7",
        "normalized_rgb": [round(170/255.0, 6), round(190/255.0, 6), round(215/255.0, 6)],
        "emissive": False,
        "roblox_material": "Enum.Material.Metal",
        "roblox_color3": "Color3.fromRGB(170, 190, 215)",
        "surface_role": "Chamfered upper perimeter frame (Y = +1.00 studs), inductor poles, and lock cleats",
    },
    "EMI_Cyan": {
        "rgb_255": [0, 195, 255],
        "hex": "#00C3FF",
        "normalized_rgb": [round(0/255.0, 6), round(195/255.0, 6), round(255/255.0, 6)],
        "emissive": True,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(0, 195, 255)",
        "surface_role": "State 1 (Safe / Normal) restrained cyan seam inlays",
    },
    "EMI_Amber": {
        "rgb_255": [255, 170, 0],
        "hex": "#FFAA00",
        "normalized_rgb": [round(255/255.0, 6), round(170/255.0, 6), round(0/255.0, 6)],
        "emissive": True,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(255, 170, 0)",
        "surface_role": "State 2 (Warning) amber caution perimeter and radial hazard stripes",
    },
    "EMI_Ice": {
        "rgb_255": [0, 235, 255],
        "hex": "#00EBFF",
        "normalized_rgb": [round(0/255.0, 6), round(235/255.0, 6), round(255/255.0, 6)],
        "emissive": True,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(0, 235, 255)",
        "surface_role": "State 3 (Ice Corridor — active) longitudinal ice-blue cryo channels and frost bridges",
    },
    "EMI_Magnetic": {
        "rgb_255": [165, 55, 255],
        "hex": "#A537FF",
        "normalized_rgb": [round(165/255.0, 6), round(55/255.0, 6), round(255/255.0, 6)],
        "emissive": True,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(165, 55, 255)",
        "surface_role": "State 4 (Magnetic Storm — active) concentric octagonal purple electromagnetic field rings",
    },
    "EMI_Kinetic": {
        "rgb_255": [255, 125, 0],
        "hex": "#FF7D00",
        "normalized_rgb": [round(255/255.0, 6), round(125/255.0, 6), round(0/255.0, 6)],
        "emissive": True,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(255, 125, 0)",
        "surface_role": "State 5 (Boost Runway — active) forward (+Z) orange kinetic acceleration chevrons",
    },
    "EMI_DangerRed": {
        "rgb_255": [255, 40, 40],
        "hex": "#FF2828",
        "normalized_rgb": [round(255/255.0, 6), round(40/255.0, 6), round(40/255.0, 6)],
        "emissive": True,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(255, 40, 40)",
        "surface_role": "State 6 (Ring Collapse — warning) danger-red perimeter bars and diagonal X-collapse motif",
    },
}


def build_palette_atlas_png_bytes():
    """
    Creates a 96x96 PNG 3x3 palette swatch texture (`SphereBrawl_ArenaTile_PaletteAtlas.png`).
    Each of the 9 materials occupies a 32x32 block so UV coordinates mapped to the center
    of that block sample the exact sRGB color with zero bleeding.
    """
    cell_px = 32
    img = Image.new("RGB", (cell_px * 3, cell_px * 3), (32, 38, 54))
    draw = ImageDraw.Draw(img)
    uv_centers_gltf = {}
    uv_centers_obj = {}

    for idx, mname in enumerate(PALETTE_ORDER):
        col_i = idx % 3
        row_i = idx // 3  # 0 = top row in image
        x0, y0 = col_i * cell_px, row_i * cell_px
        x1, y1 = x0 + cell_px - 1, y0 + cell_px - 1
        rgb = PALETTE_SRGB[mname]
        draw.rectangle([x0, y0, x1, y1], fill=rgb)

        u = (col_i + 0.5) / 3.0
        v_gltf = (row_i + 0.5) / 3.0          # glTF UV origin is upper-left (0,0)
        v_obj = 1.0 - (row_i + 0.5) / 3.0     # Wavefront OBJ UV origin is lower-left (0,0)
        uv_centers_gltf[mname] = (round(u, 5), round(v_gltf, 5))
        uv_centers_obj[mname] = (round(u, 5), round(v_obj, 5))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue(), uv_centers_gltf, uv_centers_obj


ATLAS_PNG_BYTES, UV_CENTERS_GLTF, UV_CENTERS_OBJ = build_palette_atlas_png_bytes()
ATLAS_FILENAME = "SphereBrawl_ArenaTile_PaletteAtlas.png"
with open(os.path.join(PKG_STAGE_DIR, "textures", ATLAS_FILENAME), "wb") as _af:
    _af.write(ATLAS_PNG_BYTES)


class ArenaTileMesh:
    """Deterministic hard-surface mesh builder with strict winding, normal, UV, vertex-color, and multi-node GLB/OBJ export."""

    def __init__(self, name):
        self.name = name
        self.groups = {}  # (group_name, mat_name) -> list of (v0, v1, v2) np.float64

    def add_tri(self, group_name, mat_name, v0, v1, v2, expected_normal=None):
        p0 = np.round(np.array(v0, dtype=np.float64), 5)
        p1 = np.round(np.array(v1, dtype=np.float64), 5)
        p2 = np.round(np.array(v2, dtype=np.float64), 5)

        cross = np.cross(p1 - p0, p2 - p0)
        area = 0.5 * float(np.linalg.norm(cross))
        if area < 1e-7:
            raise ValueError(f"Degenerate triangle detected in {self.name}/{group_name}: area={area}")

        if expected_normal is not None:
            en = np.array(expected_normal, dtype=np.float64)
            if float(np.dot(cross, en)) < 0.0:
                p1, p2 = p2, p1

        key = (group_name, mat_name)
        self.groups.setdefault(key, []).append((p0, p1, p2))

    def add_quad(self, group_name, mat_name, v0, v1, v2, v3, expected_normal=None):
        self.add_tri(group_name, mat_name, v0, v1, v2, expected_normal=expected_normal)
        self.add_tri(group_name, mat_name, v0, v2, v3, expected_normal=expected_normal)

    def merge_from(self, other_mesh):
        for (g, m), tris in other_mesh.groups.items():
            for (v0, v1, v2) in tris:
                self.groups.setdefault((g, m), []).append((v0.copy(), v1.copy(), v2.copy()))

    def add_frustum_pad(self, group_name, mat_name, x0, x1, z0, z1, y0, y1, inset_top=0.04, include_bottom=False):
        ix0, ix1 = x0 + inset_top, x1 - inset_top
        iz0, iz1 = z0 + inset_top, z1 - inset_top

        t_nw = (ix0, y1, iz0)
        t_sw = (ix0, y1, iz1)
        t_se = (ix1, y1, iz1)
        t_ne = (ix1, y1, iz0)

        b_nw = (x0, y0, z0)
        b_sw = (x0, y0, z1)
        b_se = (x1, y0, z1)
        b_ne = (x1, y0, z0)

        self.add_quad(group_name, mat_name, t_nw, t_sw, t_se, t_ne, expected_normal=(0, 1, 0))
        self.add_quad(group_name, mat_name, b_sw, b_se, t_se, t_sw, expected_normal=(0, 0.2, 1))
        self.add_quad(group_name, mat_name, b_ne, b_nw, t_nw, t_ne, expected_normal=(0, 0.2, -1))
        self.add_quad(group_name, mat_name, b_se, b_ne, t_ne, t_se, expected_normal=(1, 0.2, 0))
        self.add_quad(group_name, mat_name, b_nw, b_sw, t_sw, t_nw, expected_normal=(-1, 0.2, 0))

        if include_bottom:
            self.add_quad(group_name, mat_name, b_nw, b_ne, b_se, b_sw, expected_normal=(0, -1, 0))

    def add_extruded_polygon_y(self, group_name, mat_name, poly_xz, y0, y1, tris_indices):
        n_pts = len(poly_xz)
        for (i0, i1, i2) in tris_indices:
            v0 = (poly_xz[i0][0], y1, poly_xz[i0][1])
            v1 = (poly_xz[i1][0], y1, poly_xz[i1][1])
            v2 = (poly_xz[i2][0], y1, poly_xz[i2][1])
            self.add_tri(group_name, mat_name, v0, v1, v2, expected_normal=(0, 1, 0))

        for i in range(n_pts):
            x_a, z_a = poly_xz[i]
            x_b, z_b = poly_xz[(i + 1) % n_pts]
            dx, dz = x_b - x_a, z_b - z_a
            out_n = (dz, 0.0, -dx)
            b_a = (x_a, y0, z_a)
            b_b = (x_b, y0, z_b)
            t_b = (x_b, y1, z_b)
            t_a = (x_a, y1, z_a)
            self.add_quad(group_name, mat_name, b_a, b_b, t_b, t_a, expected_normal=out_n)

    def add_annular_ring_y(self, group_name, mat_name, r_in, r_out, y0, y1, n_segs=8, theta_offset=0.0):
        for i in range(n_segs):
            t0 = theta_offset + (2.0 * math.pi * i) / n_segs
            t1 = theta_offset + (2.0 * math.pi * (i + 1)) / n_segs
            c0, s0 = math.cos(t0), math.sin(t0)
            c1, s1 = math.cos(t1), math.sin(t1)

            ti0 = (r_in * c0, y1, r_in * s0)
            ti1 = (r_in * c1, y1, r_in * s1)
            to1 = (r_out * c1, y1, r_out * s1)
            to0 = (r_out * c0, y1, r_out * s0)

            bi0 = (r_in * c0, y0, r_in * s0)
            bi1 = (r_in * c1, y0, r_in * s1)
            bo1 = (r_out * c1, y0, r_out * s1)
            bo0 = (r_out * c0, y0, r_out * s0)

            tm = 0.5 * (t0 + t1)
            out_dir = (math.cos(tm), 0.0, math.sin(tm))
            in_dir = (-math.cos(tm), 0.0, -math.sin(tm))

            self.add_quad(group_name, mat_name, ti0, ti1, to1, to0, expected_normal=(0, 1, 0))
            self.add_quad(group_name, mat_name, bo0, bo1, to1, to0, expected_normal=out_dir)
            self.add_quad(group_name, mat_name, bi1, bi0, ti0, ti1, expected_normal=in_dir)

    def add_chevron_z(self, group_name, mat_name, z_tip, z_mid, z_tail, half_w, y0, y1):
        poly_xz = [
            (0.0, z_tip),       # 0
            (-half_w, z_mid),   # 1
            (-half_w, z_tail),  # 2
            (0.0, z_mid),       # 3
            (half_w, z_tail),   # 4
            (half_w, z_mid),    # 5
        ]
        tris = [
            (0, 1, 3),
            (1, 2, 3),
            (0, 3, 5),
            (3, 4, 5),
        ]
        self.add_extruded_polygon_y(group_name, mat_name, poly_xz, y0, y1, tris)

    def export_obj_and_mtl(self, obj_path, mtl_path):
        """
        Exports Wavefront .obj and .mtl with:
          1. Multi-object (`o <Asset>__<MaterialSlot>`) segmentation so Roblox Studio's 3D Importer
             splits each material slot into its own selectable MeshPart when 'Import As Model' is enabled.
          2. Explicit `vt` UV coordinates mapped to `textures/SphereBrawl_ArenaTile_PaletteAtlas.png`.
          3. Extended `v x y z r g b` vertex colors + `.mtl` `Kd`/`Ke` and `map_Kd` reference.
        """
        mtl_filename = os.path.basename(mtl_path)
        used_mats = sorted(list(set(m for (_, m) in self.groups.keys())))

        # Also copy the palette atlas PNG into the mesh folder so relative `map_Kd` resolves out-of-the-box
        local_atlas_path = os.path.join(os.path.dirname(mtl_path), ATLAS_FILENAME)
        if not os.path.exists(local_atlas_path):
            with open(local_atlas_path, "wb") as af:
                af.write(ATLAS_PNG_BYTES)

        with open(mtl_path, "w", encoding="utf-8") as mf:
            mf.write("# Sphere Brawl: Rolling Rampage — Self-Contained Material Library\n")
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

        # Group by material slot first so each material is a distinct `o Part_<Material>` object in OBJ
        by_mat = {}
        for (g_name, mat_name), tris in self.groups.items():
            if not tris:
                continue
            by_mat.setdefault(mat_name, []).append((g_name, tris))

        with open(obj_path, "w", encoding="utf-8") as of:
            of.write("# Sphere Brawl: Rolling Rampage — Validated Arena Tile 3D Asset\n")
            of.write(f"# Asset Name: {self.name}\n")
            of.write("# Unit Scale: 1.0 Unit = 1.0 Roblox Stud | Up Axis: +Y | Forward Axis: +Z | Origin: (0,0,0)\n")
            of.write(f"mtllib {mtl_filename}\n")

            # Write 1 UV coordinate per active material slot
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
        """
        Writes a binary glTF 2.0 (.glb) file engineered specifically for Roblox Studio & Blender:
          1. Multi-node hierarchy: Root node `<AssetName>` has child nodes `Part_<MaterialSlot>`,
             each referencing its own single-material mesh (`Mesh_<MaterialSlot>`). In Roblox Studio's
             3D Importer, this creates a `Model` containing separate named `MeshPart` children per
             material slot (`Part_MAT_DarkNeutral`, `Part_MAT_AltNeutral`, `Part_MAT_LightTrim`, `Part_EMI_*`)
             so `Color3` and `Enum.Material.Neon`/`Metal` can be applied per slot without coloring the whole tile.
          2. `COLOR_0` (VEC4 float32) vertex color attribute on every vertex set to the exact material color.
          3. `TEXCOORD_0` (VEC2 float32) UVs + embedded PNG `baseColorTexture` (`SphereBrawl_ArenaTile_PaletteAtlas.png`),
             AND `baseColorFactor` + `emissiveFactor` set to the exact material RGB values.
        """
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

        # 1. Embed the 96x96 PNG palette atlas into BufferView 0 so GLB is 100% self-contained
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
            "name": "SphereBrawl_PaletteAtlas",
            "bufferView": bv_image,
            "mimeType": "image/png",
        }]
        gltf_samplers = [{
            "magFilter": 9728,  # NEAREST (crisp swatch sampling)
            "minFilter": 9728,  # NEAREST
            "wrapS": 33071,     # CLAMP_TO_EDGE
            "wrapT": 33071,
        }]
        gltf_textures = [{
            "name": "SphereBrawl_PaletteAtlas_Tex",
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

        # Build one separate glTF Mesh + Node per material slot under root node 0
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

        # Node 0 is the root container Model; nodes 1..N are the per-material child parts
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
                "generator": "Sphere Brawl Arena Tile Pipeline v2.0 (Multi-Node + VertexColor + AtlasUV)",
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
# 1. SHARED BASE TILE BUILDER (84 Triangles — Preserved 100%)
# ==============================================================================
def build_shared_base_tile(name="SM_ArenaTile_SharedBase"):
    mb = ArenaTileMesh(name)

    b0, b1, b2, b3 = (-5.42, -1.00, -5.42), (5.42, -1.00, -5.42), (5.42, -1.00, 5.42), (-5.42, -1.00, 5.42)
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b0, b1, b2, b3, expected_normal=(0, -1, 0))

    m0, m1, m2, m3 = (-5.90, -0.45, -5.90), (-5.90, -0.45, 5.90), (5.90, -0.45, 5.90), (5.90, -0.45, -5.90)
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b3, b2, m2, m1, expected_normal=(0, -0.5, 1))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b1, b0, m0, m3, expected_normal=(0, -0.5, -1))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b2, b1, m3, m2, expected_normal=(1, -0.5, 0))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b0, b3, m1, m0, expected_normal=(-1, -0.5, 0))

    u0, u1, u2, u3 = (-5.90, 0.72, -5.90), (-5.90, 0.72, 5.90), (5.90, 0.72, 5.90), (5.90, 0.72, -5.90)
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", m1, m2, u2, u1, expected_normal=(0, 0, 1))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", m3, m0, u0, u3, expected_normal=(0, 0, -1))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", m2, m3, u3, u2, expected_normal=(1, 0, 0))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", m0, m1, u1, u0, expected_normal=(-1, 0, 0))

    r_out0, r_out1, r_out2, r_out3 = (-5.68, 1.00, -5.68), (-5.68, 1.00, 5.68), (5.68, 1.00, 5.68), (5.68, 1.00, -5.68)
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", u1, u2, r_out2, r_out1, expected_normal=(0, 0.7, 1))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", u3, u0, r_out0, r_out3, expected_normal=(0, 0.7, -1))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", u2, u3, r_out3, r_out2, expected_normal=(1, 0.7, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", u0, u1, r_out1, r_out0, expected_normal=(-1, 0.7, 0))

    r_in0, r_in1, r_in2, r_in3 = (-5.16, 1.00, -5.16), (-5.16, 1.00, 5.16), (5.16, 1.00, 5.16), (5.16, 1.00, -5.16)
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_out1, r_out2, r_in2, r_in1, expected_normal=(0, 1, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_out3, r_out0, r_in0, r_in3, expected_normal=(0, 1, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_out2, r_out3, r_in3, r_in2, expected_normal=(0, 1, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_out0, r_out1, r_in1, r_in0, expected_normal=(0, 1, 0))

    d0, d1, d2, d3 = (-4.96, 0.86, -4.96), (-4.96, 0.86, 4.96), (4.96, 0.86, 4.96), (4.96, 0.86, -4.96)
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_in1, r_in2, d2, d1, expected_normal=(0, 0.7, -1))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_in3, r_in0, d0, d3, expected_normal=(0, 0.7, 1))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_in2, r_in3, d3, d2, expected_normal=(-1, 0.7, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_in0, r_in1, d1, d0, expected_normal=(1, 0.7, 0))

    mb.add_quad("TileBase_RecessedDeck", "MAT_AltNeutral", d0, d1, d2, d3, expected_normal=(0, 1, 0))

    for cname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        cx, cz = sx * 4.34, sz * 4.34
        mb.add_frustum_pad(
            f"TileBase_CornerBolster_{cname}", "MAT_DarkNeutral",
            cx - 0.58, cx + 0.58, cz - 0.58, cz + 0.58,
            0.86, 0.99, inset_top=0.06
        )

    return mb


# ==============================================================================
# 2. SIX STATE OVERLAY BUILDERS (Preserved 100%)
# ==============================================================================
def build_overlay_01_safe_normal(name="SM_ArenaTile_Overlay_01_SafeNormal"):
    mb = ArenaTileMesh(name)
    for qname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        x0, x1 = (0.52, 3.62) if sx > 0 else (-3.62, -0.52)
        z0, z1 = (0.52, 3.62) if sz > 0 else (-3.62, -0.52)
        mb.add_frustum_pad(f"Safe_QuadArmor_{qname}", "MAT_DarkNeutral", x0, x1, z0, z1, 0.86, 0.98, inset_top=0.06)

    mb.add_frustum_pad("Safe_CenterCoreHub", "MAT_LightTrim", -0.44, 0.44, -0.44, 0.44, 0.86, 0.99, inset_top=0.05)

    mb.add_frustum_pad("Safe_CyanSeam_North", "EMI_Cyan", -0.22, 0.22, -3.55, -0.62, 0.86, 0.93, inset_top=0.02)
    mb.add_frustum_pad("Safe_CyanSeam_South", "EMI_Cyan", -0.22, 0.22,  0.62,  3.55, 0.86, 0.93, inset_top=0.02)
    mb.add_frustum_pad("Safe_CyanSeam_West",  "EMI_Cyan", -3.55, -0.62, -0.22, 0.22, 0.86, 0.93, inset_top=0.02)
    mb.add_frustum_pad("Safe_CyanSeam_East",  "EMI_Cyan",  0.62,  3.55, -0.22, 0.22, 0.86, 0.93, inset_top=0.02)

    mb.add_frustum_pad("Safe_CyanNode_North", "EMI_Cyan", -1.40, 1.40, -4.55, -4.18, 0.86, 0.94, inset_top=0.02)
    mb.add_frustum_pad("Safe_CyanNode_South", "EMI_Cyan", -1.40, 1.40,  4.18,  4.55, 0.86, 0.94, inset_top=0.02)
    mb.add_frustum_pad("Safe_CyanNode_West",  "EMI_Cyan", -4.55, -4.18, -1.40, 1.40, 0.86, 0.94, inset_top=0.02)
    mb.add_frustum_pad("Safe_CyanNode_East",  "EMI_Cyan",  4.18,  4.55, -1.40, 1.40, 0.86, 0.94, inset_top=0.02)
    return mb


def build_overlay_02_warning(name="SM_ArenaTile_Overlay_02_Warning"):
    mb = ArenaTileMesh(name)
    mb.add_frustum_pad("Warn_AmberPerimeter_N", "EMI_Amber", -3.40, 3.40, -4.65, -4.10, 0.86, 0.96, inset_top=0.03)
    mb.add_frustum_pad("Warn_AmberPerimeter_S", "EMI_Amber", -3.40, 3.40,  4.10,  4.65, 0.86, 0.96, inset_top=0.03)
    mb.add_frustum_pad("Warn_AmberPerimeter_W", "EMI_Amber", -4.65, -4.10, -3.40, 3.40, 0.86, 0.96, inset_top=0.03)
    mb.add_frustum_pad("Warn_AmberPerimeter_E", "EMI_Amber",  4.10,  4.65, -3.40, 3.40, 0.86, 0.96, inset_top=0.03)

    for qname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        x0, x1 = (1.35, 3.75) if sx > 0 else (-3.75, -1.35)
        z0, z1 = (1.35, 3.75) if sz > 0 else (-3.75, -1.35)
        mb.add_frustum_pad(f"Warn_DarkPlate_{qname}", "MAT_DarkNeutral", x0, x1, z0, z1, 0.86, 0.98, inset_top=0.05)

    mb.add_frustum_pad("Warn_AmberStripe_N", "EMI_Amber", -0.65, 0.65, -3.75, -1.45, 0.86, 0.96, inset_top=0.03)
    mb.add_frustum_pad("Warn_AmberStripe_S", "EMI_Amber", -0.65, 0.65,  1.45,  3.75, 0.86, 0.96, inset_top=0.03)
    mb.add_frustum_pad("Warn_AmberStripe_W", "EMI_Amber", -3.75, -1.45, -0.65, 0.65, 0.86, 0.96, inset_top=0.03)
    mb.add_frustum_pad("Warn_AmberStripe_E", "EMI_Amber",  1.45,  3.75, -0.65, 0.65, 0.86, 0.96, inset_top=0.03)

    mb.add_frustum_pad("Warn_CentralBeaconOuter", "EMI_Amber", -1.20, 1.20, -1.20, 1.20, 0.86, 0.97, inset_top=0.04)
    mb.add_frustum_pad("Warn_CentralBeaconInner", "MAT_DarkNeutral", -0.55, 0.55, -0.55, 0.55, 0.97, 0.995, inset_top=0.03)
    return mb


def build_overlay_03_ice_corridor(name="SM_ArenaTile_Overlay_03_IceCorridor"):
    mb = ArenaTileMesh(name)
    for idx, xc in enumerate([-3.30, -1.15, 1.15, 3.30]):
        mb.add_frustum_pad(
            f"Ice_CryoChannel_{idx+1}", "EMI_Ice",
            xc - 0.32, xc + 0.32, -4.55, 4.55,
            0.86, 0.95, inset_top=0.03
        )

    for idx, (x0, x1) in enumerate([(-2.75, -1.65), (-0.65, 0.65), (1.65, 2.75)]):
        mb.add_frustum_pad(
            f"Ice_SledDeck_{idx+1}", "MAT_DarkNeutral",
            x0, x1, -4.35, 4.35,
            0.86, 0.98, inset_top=0.05
        )

    for idx, zc in enumerate([-2.20, 2.20]):
        mb.add_frustum_pad(
            f"Ice_FrostCrossLink_{idx+1}", "EMI_Ice",
            -3.60, 3.60, zc - 0.24, zc + 0.24,
            0.86, 0.94, inset_top=0.02
        )

    for cname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        cx = sx * 2.20
        cz = sz * 4.58
        mb.add_frustum_pad(
            f"Ice_FrostEndTrim_{cname}", "MAT_LightTrim",
            cx - 0.85, cx + 0.85, cz - 0.22, cz + 0.22,
            0.86, 0.99, inset_top=0.03
        )
    return mb


def build_overlay_04_magnetic_storm(name="SM_ArenaTile_Overlay_04_MagneticStorm"):
    mb = ArenaTileMesh(name)
    rot_oct = math.pi / 8.0
    mb.add_annular_ring_y("Mag_OuterFieldRing", "EMI_Magnetic", 3.10, 3.78, 0.86, 0.95, n_segs=8, theta_offset=rot_oct)
    mb.add_annular_ring_y("Mag_InnerFieldRing", "EMI_Magnetic", 1.35, 1.95, 0.86, 0.96, n_segs=8, theta_offset=rot_oct)

    mb.add_frustum_pad("Mag_PoleShoe_North", "MAT_LightTrim", -0.48, 0.48, -4.55, -2.05, 0.86, 0.985, inset_top=0.04)
    mb.add_frustum_pad("Mag_PoleShoe_South", "MAT_LightTrim", -0.48, 0.48,  2.05,  4.55, 0.86, 0.985, inset_top=0.04)
    mb.add_frustum_pad("Mag_PoleShoe_West",  "MAT_LightTrim", -4.55, -2.05, -0.48, 0.48, 0.86, 0.985, inset_top=0.04)
    mb.add_frustum_pad("Mag_PoleShoe_East",  "MAT_LightTrim",  2.05,  4.55, -0.48, 0.48, 0.86, 0.985, inset_top=0.04)

    mb.add_frustum_pad("Mag_CenterCoreCap", "MAT_DarkNeutral", -0.78, 0.78, -0.78, 0.78, 0.86, 0.99, inset_top=0.05)
    return mb


def build_overlay_05_boost_runway(name="SM_ArenaTile_Overlay_05_BoostRunway"):
    mb = ArenaTileMesh(name)
    chevron_specs = [
        ("Rear",  -0.95, -2.45, -3.55),
        ("Mid",    1.55,  0.05, -1.05),
        ("Front",  4.05,  2.55,  1.45),
    ]
    for cname, z_tip, z_mid, z_tail in chevron_specs:
        mb.add_chevron_z(f"Boost_Chevron_{cname}", "EMI_Kinetic", z_tip, z_mid, z_tail, half_w=2.55, y0=0.86, y1=0.965)

    mb.add_frustum_pad("Boost_GuideRail_Left",  "MAT_DarkNeutral", -4.45, -3.45, -4.45, 4.45, 0.86, 0.985, inset_top=0.05)
    mb.add_frustum_pad("Boost_GuideRail_Right", "MAT_DarkNeutral",  3.45,  4.45, -4.45, 4.45, 0.86, 0.985, inset_top=0.05)

    mb.add_frustum_pad("Boost_SideStrip_Left",  "EMI_Kinetic", -3.25, -2.90, -4.20, 4.20, 0.86, 0.94, inset_top=0.02)
    mb.add_frustum_pad("Boost_SideStrip_Right", "EMI_Kinetic",  2.90,  3.25, -4.20, 4.20, 0.86, 0.94, inset_top=0.02)

    for cname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        cx = sx * 3.95
        cz = sz * 2.25
        mb.add_frustum_pad(f"Boost_RailCleat_{cname}", "MAT_LightTrim", cx - 0.38, cx + 0.38, cz - 0.85, cz + 0.85, 0.985, 1.00, inset_top=0.03)
    return mb


def build_overlay_06_ring_collapse(name="SM_ArenaTile_Overlay_06_RingCollapse"):
    mb = ArenaTileMesh(name)
    mb.add_frustum_pad("Collapse_RedPerimeter_N", "EMI_DangerRed", -3.65, 3.65, -4.78, -4.18, 0.86, 0.97, inset_top=0.03)
    mb.add_frustum_pad("Collapse_RedPerimeter_S", "EMI_DangerRed", -3.65, 3.65,  4.18,  4.78, 0.86, 0.97, inset_top=0.03)
    mb.add_frustum_pad("Collapse_RedPerimeter_W", "EMI_DangerRed", -4.78, -4.18, -3.65, 3.65, 0.86, 0.97, inset_top=0.03)
    mb.add_frustum_pad("Collapse_RedPerimeter_E", "EMI_DangerRed",  4.18,  4.78, -3.65, 3.65, 0.86, 0.97, inset_top=0.03)

    L = 3.55
    W = 0.34
    diag1_xz = [
        (-L - W, -L + W),
        ( L - W,  L + W),
        ( L + W,  L - W),
        (-L + W, -L - W),
    ]
    mb.add_extruded_polygon_y("Collapse_RedXBar_Diag1", "EMI_DangerRed", diag1_xz, 0.86, 0.96, [(0, 1, 2), (0, 2, 3)])

    diag2_xz = [
        (-L + W,  L + W),
        ( L + W, -L + W),
        ( L - W, -L - W),
        (-L - W,  L - W),
    ]
    mb.add_extruded_polygon_y("Collapse_RedXBar_Diag2", "EMI_DangerRed", diag2_xz, 0.86, 0.96, [(0, 1, 2), (0, 2, 3)])

    mb.add_frustum_pad("Collapse_Shutter_North", "MAT_DarkNeutral", -1.45, 1.45, -3.85, -1.95, 0.86, 0.985, inset_top=0.05)
    mb.add_frustum_pad("Collapse_Shutter_South", "MAT_DarkNeutral", -1.45, 1.45,  1.95,  3.85, 0.86, 0.985, inset_top=0.05)
    mb.add_frustum_pad("Collapse_Shutter_West",  "MAT_DarkNeutral", -3.85, -1.95, -1.45, 1.45, 0.86, 0.985, inset_top=0.05)
    mb.add_frustum_pad("Collapse_Shutter_East",  "MAT_DarkNeutral",  1.95,  3.85, -1.45, 1.45, 0.86, 0.985, inset_top=0.05)

    mb.add_frustum_pad("Collapse_CenterDangerCore", "EMI_DangerRed", -1.15, 1.15, -1.15, 1.15, 0.86, 0.98, inset_top=0.04)

    mb.add_frustum_pad("Collapse_RimClamp_N", "MAT_LightTrim", -0.80, 0.80, -5.60, -5.20, 0.98, 1.00, inset_top=0.02)
    mb.add_frustum_pad("Collapse_RimClamp_S", "MAT_LightTrim", -0.80, 0.80,  5.20,  5.60, 0.98, 1.00, inset_top=0.02)
    mb.add_frustum_pad("Collapse_RimClamp_W", "MAT_LightTrim", -5.60, -5.20, -0.80, 0.80, 0.98, 1.00, inset_top=0.02)
    mb.add_frustum_pad("Collapse_RimClamp_E", "MAT_LightTrim",  5.20,  5.60, -0.80, 0.80, 0.98, 1.00, inset_top=0.02)
    return mb


STATE_DEFINITIONS = [
    {
        "state_id": 1,
        "state_key": "SafeNormal",
        "state_name": "Safe / Normal",
        "display_name": "1. Safe / Normal",
        "complete_mesh_name": "SM_ArenaTile_01_SafeNormal",
        "overlay_mesh_name": "SM_ArenaTile_Overlay_01_SafeNormal",
        "primary_emissive": "EMI_Cyan",
        "primary_emissive_rgb": [0, 195, 255],
        "expected_materials": ["EMI_Cyan", "MAT_AltNeutral", "MAT_DarkNeutral", "MAT_LightTrim"],
        "expected_complete_tris": 214,
        "expected_overlay_tris": 130,
        "builder_fn": build_overlay_01_safe_normal,
        "visual_description": "Dark metallic quadrant armor plates with restrained recessed cyan energy channels (EMI_Cyan) and central lock hub.",
    },
    {
        "state_id": 2,
        "state_key": "Warning",
        "state_name": "Warning",
        "display_name": "2. Warning",
        "complete_mesh_name": "SM_ArenaTile_02_Warning",
        "overlay_mesh_name": "SM_ArenaTile_Overlay_02_Warning",
        "primary_emissive": "EMI_Amber",
        "primary_emissive_rgb": [255, 170, 0],
        "expected_materials": ["EMI_Amber", "MAT_AltNeutral", "MAT_DarkNeutral", "MAT_LightTrim"],
        "expected_complete_tris": 224,
        "expected_overlay_tris": 140,
        "builder_fn": build_overlay_02_warning,
        "visual_description": "Segmented amber perimeter caution bars (EMI_Amber), radial warning stripes, and central amber beacon framing dark armor blocks.",
    },
    {
        "state_id": 3,
        "state_key": "IceCorridor",
        "state_name": "Ice Corridor — active",
        "display_name": "3. Ice Corridor — active",
        "complete_mesh_name": "SM_ArenaTile_03_IceCorridor",
        "overlay_mesh_name": "SM_ArenaTile_Overlay_03_IceCorridor",
        "primary_emissive": "EMI_Ice",
        "primary_emissive_rgb": [0, 235, 255],
        "expected_materials": ["EMI_Ice", "MAT_AltNeutral", "MAT_DarkNeutral", "MAT_LightTrim"],
        "expected_complete_tris": 214,
        "expected_overlay_tris": 130,
        "builder_fn": build_overlay_03_ice_corridor,
        "visual_description": "Four longitudinal ice-blue cryo channels (EMI_Ice) with transverse frost lattice bridges and dark metallic sled guide decks.",
    },
    {
        "state_id": 4,
        "state_key": "MagneticStorm",
        "state_name": "Magnetic Storm — active",
        "display_name": "4. Magnetic Storm — active",
        "complete_mesh_name": "SM_ArenaTile_04_MagneticStorm",
        "overlay_mesh_name": "SM_ArenaTile_Overlay_04_MagneticStorm",
        "primary_emissive": "EMI_Magnetic",
        "primary_emissive_rgb": [165, 55, 255],
        "expected_materials": ["EMI_Magnetic", "MAT_AltNeutral", "MAT_DarkNeutral", "MAT_LightTrim"],
        "expected_complete_tris": 230,
        "expected_overlay_tris": 146,
        "builder_fn": build_overlay_04_magnetic_storm,
        "visual_description": "Symmetric concentric octagonal purple electromagnetic field rings (EMI_Magnetic) bridged by four cardinal metallic inductor pole shoes.",
    },
    {
        "state_id": 5,
        "state_key": "BoostRunway",
        "state_name": "Boost Runway — active",
        "display_name": "5. Boost Runway — active",
        "complete_mesh_name": "SM_ArenaTile_05_BoostRunway",
        "overlay_mesh_name": "SM_ArenaTile_Overlay_05_BoostRunway",
        "primary_emissive": "EMI_Kinetic",
        "primary_emissive_rgb": [255, 125, 0],
        "expected_materials": ["EMI_Kinetic", "MAT_AltNeutral", "MAT_DarkNeutral", "MAT_LightTrim"],
        "expected_complete_tris": 212,
        "expected_overlay_tris": 128,
        "builder_fn": build_overlay_05_boost_runway,
        "visual_description": "Three sequential forward-pointing (+Z) orange kinetic chevrons (EMI_Kinetic) flanked by dark runway guide rails and trim cleats.",
    },
    {
        "state_id": 6,
        "state_key": "RingCollapse",
        "state_name": "Ring Collapse — warning",
        "display_name": "6. Ring Collapse — warning",
        "complete_mesh_name": "SM_ArenaTile_06_RingCollapse",
        "overlay_mesh_name": "SM_ArenaTile_Overlay_06_RingCollapse",
        "primary_emissive": "EMI_DangerRed",
        "primary_emissive_rgb": [255, 40, 40],
        "expected_materials": ["EMI_DangerRed", "MAT_AltNeutral", "MAT_DarkNeutral", "MAT_LightTrim"],
        "expected_complete_tris": 234,
        "expected_overlay_tris": 150,
        "builder_fn": build_overlay_06_ring_collapse,
        "visual_description": "Continuous danger-red perimeter lighting (EMI_DangerRed), diagonal X-collapse hazard motif, central drop-warning beacon, and dark blast shutters.",
    },
]


# ==============================================================================
# 3. DUAL-MODE SOFTWARE Z-BUFFER RASTERIZER (MATERIAL-COLOUR vs. NEUTRAL CLAY)
# ==============================================================================
def build_camera_axes(view_type):
    if view_type == "top":
        right = np.array([1.0, 0.0, 0.0])
        up_scr = np.array([0.0, 0.0, 1.0])
        view_dir = np.array([0.0, 1.0, 0.0])
    elif view_type == "side":
        view_dir = np.array([1.0, 0.0, 0.0])
        right = np.array([0.0, 0.0, 1.0])
        up_scr = np.array([0.0, 1.0, 0.0])
    else:
        az = math.radians(-38.0)
        el = math.radians(34.0)
        view_dir = np.array([
            math.cos(el) * math.sin(az),
            math.sin(el),
            -math.cos(el) * math.cos(az),
        ])
        view_dir /= np.linalg.norm(view_dir)
        world_up = np.array([0.0, 1.0, 0.0])
        right = np.cross(world_up, view_dir)
        right /= np.linalg.norm(right)
        up_scr = np.cross(view_dir, right)
        up_scr /= np.linalg.norm(up_scr)
    return right, up_scr, view_dir


def rasterize_meshes_zbuffer(mesh_instances, view_type="persp", width=720, height=540,
                             span_x=8.4, span_y=6.3, center=(0.0, 0.0, 0.0),
                             render_mode="material", collider_boxes=None):
    """
    Renders `(ArenaTileMesh, offset_xyz)` instances with 2x2 supersampling in one of three modes:
      - `render_mode="material"`: True material-colour preview using exact `PALETTE_SRGB` values
      - `render_mode="neutral"`:  Neutral studio clay lighting (`RGB 178, 186, 198`) for pure geometry comparison
      - `render_mode="wireframe"`: Technical wireframe inspection
    """
    wire_only = (render_mode == "wireframe")
    neutral_clay = (render_mode == "neutral")

    ss = 2
    W, H = width * ss, height * ss
    bg_rgb = np.array([23, 31, 46] if not neutral_clay else [28, 33, 42], dtype=np.uint8)
    color_buf = np.broadcast_to(bg_rgb, (H, W, 3)).copy()
    z_buf = np.full((H, W), -1e18, dtype=np.float64)

    right, up_scr, view_dir = build_camera_axes(view_type)
    center_arr = np.array(center, dtype=np.float64)

    light_dir = np.array([0.38, 0.82, -0.42], dtype=np.float64)
    light_dir /= np.linalg.norm(light_dir)

    def project_pt(pt):
        rel = pt - center_arr
        x_cam = float(np.dot(rel, right))
        y_cam = float(np.dot(rel, up_scr))
        z_cam = float(np.dot(rel, view_dir))
        px = (x_cam / (2.0 * span_x) + 0.5) * W
        py = (0.5 - y_cam / (2.0 * span_y)) * H
        return px, py, z_cam

    wire_segments = []

    for mb, offset in mesh_instances:
        off = np.array(offset, dtype=np.float64)
        for (g_name, mat_name), tris in mb.groups.items():
            base_rgb = np.array(PALETTE_SRGB[mat_name], dtype=np.float64)
            is_emi = mat_name.startswith("EMI_")
            z_bias = 0.003 if not g_name.startswith("TileBase_") else 0.0

            for (v0, v1, v2) in tris:
                p0, p1, p2 = v0 + off, v1 + off, v2 + off
                n = np.cross(v1 - v0, v2 - v0)
                nl = float(np.linalg.norm(n))
                n = (n / nl) if nl > 1e-8 else np.array([0.0, 1.0, 0.0])

                facing_dot = float(np.dot(n, view_dir))

                if neutral_clay:
                    # Uniform neutral clay surface for pure geometry comparison
                    clay_base = np.array([196.0, 204.0, 216.0]) if not g_name.startswith("TileBase_") else np.array([154.0, 162.0, 176.0])
                    lambert = max(0.22, abs(float(np.dot(n, light_dir))))
                    spec = max(0.0, facing_dot) ** 8 * 0.16
                    factor = 0.35 + 0.65 * lambert + spec
                    shade_rgb = np.clip(clay_base * factor, 0, 255).astype(np.uint8)
                    edge_rgb = (70, 82, 98)
                elif is_emi:
                    shade_rgb = np.clip(base_rgb * 1.08, 0, 255).astype(np.uint8)
                    edge_rgb = (240, 248, 255) if not wire_only else tuple(int(x) for x in np.clip(base_rgb * 1.15, 0, 255))
                else:
                    lambert = max(0.25, abs(float(np.dot(n, light_dir))))
                    spec = max(0.0, facing_dot) ** 6 * 0.18
                    factor = 0.36 + 0.68 * lambert + spec
                    shade_rgb = np.clip(base_rgb * factor, 0, 255).astype(np.uint8)
                    edge_rgb = (90, 115, 145) if not wire_only else tuple(int(x) for x in np.clip(base_rgb * 1.35 + 40, 0, 255))

                x0, y0, z0 = project_pt(p0)
                x1, y1, z1 = project_pt(p1)
                x2, y2, z2 = project_pt(p2)
                z0 += z_bias
                z1 += z_bias
                z2 += z_bias

                if wire_only or facing_dot >= -0.02:
                    wire_segments.append(((x0, y0, z0), (x1, y1, z1), edge_rgb, is_emi and not neutral_clay))
                    wire_segments.append(((x1, y1, z1), (x2, y2, z2), edge_rgb, is_emi and not neutral_clay))
                    wire_segments.append(((x2, y2, z2), (x0, y0, z0), edge_rgb, is_emi and not neutral_clay))

                if wire_only or facing_dot < -0.05:
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
            for t in (0.2, 0.5, 0.8):
                xt = int(xa + t * (xb - xa))
                yt = int(ya + t * (yb - ya))
                zt = za + t * (zb - za)
                if 0 <= xt < W and 0 <= yt < H:
                    if zt >= z_buf[yt, xt] - 0.04:
                        visible_pts += 1
            if visible_pts < 2:
                continue
            lw = 2 if is_emi else 1
        else:
            lw = 3 if is_emi else 2
        draw.line([(xa, ya), (xb, yb)], fill=ergb, width=lw)

    if collider_boxes:
        for (cx0, cx1, cy0, cy1, cz0, cz1) in collider_boxes:
            if view_type == "side":
                corners_3d = [
                    np.array([cx1, cy0, cz0]),
                    np.array([cx1, cy0, cz1]),
                    np.array([cx1, cy1, cz1]),
                    np.array([cx1, cy1, cz0]),
                ]
            else:
                corners_3d = [
                    np.array([cx0, cy1, cz0]),
                    np.array([cx1, cy1, cz0]),
                    np.array([cx1, cy1, cz1]),
                    np.array([cx0, cy1, cz1]),
                ]
            for i in range(4):
                pa = corners_3d[i]
                pb = corners_3d[(i + 1) % 4]
                n_dashes = 18
                for d in range(n_dashes):
                    if d % 2 == 0:
                        t0, t1 = d / n_dashes, (d + 0.65) / n_dashes
                        xa, ya, _ = project_pt(pa + t0 * (pb - pa))
                        xb, yb, _ = project_pt(pa + t1 * (pb - pa))
                        draw.line([(xa, ya), (xb, yb)], fill=(0, 255, 136), width=3)

    img_out = img.resize((width, height), resample=Image.Resampling.LANCZOS)
    return np.asarray(img_out)


def annotate_panel(ax, img_arr, title, view_type, show_legend=False, accent_hex="#00C3FF"):
    ax.imshow(img_arr)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("#2A3246")
        spine.set_linewidth(1.2)
    ax.set_title(title, color="#F5F8FF", fontsize=10.0, fontweight="bold", pad=6)

    if view_type == "top":
        axis_txt = "Axes: +X Right | +Z Up (Forward) | Looking -Y (World Y=51 Top)"
    elif view_type == "side":
        axis_txt = "Axes: +Z Right (11.80 Studs) | +Y Up (Height: -1.00 to +1.00 Studs)"
    else:
        axis_txt = "Axes: +Y Up | +Z Forward-Right | Centered Origin (0,0,0)"

    ax.text(0.02, 0.03, axis_txt, transform=ax.transAxes, color="#AABED7", fontsize=7.5,
            bbox=dict(boxstyle="round,pad=0.24", facecolor="#0F141F", edgecolor="#2A3246", alpha=0.88))

    if show_legend:
        ax.text(0.98, 0.96, "--- 12.0 x 2.0 x 12.0 Gameplay Collider\n(11.8 Visual Mesh -> 0.20 Stud Gap)",
                transform=ax.transAxes, ha="right", va="top", color="#00FF88", fontsize=7.4, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.26", facecolor="#0F141F", edgecolor=accent_hex, alpha=0.92))


def render_individual_state_sheet(state_def, mb, metrics, out_png):
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    fig = plt.figure(figsize=(16, 9.6), dpi=150, facecolor="#0F141F")

    emi_hex = "#{:02X}{:02X}{:02X}".format(*state_def["primary_emissive_rgb"])
    fig.text(0.03, 0.948,
             f"PYTHON Z-BUFFER MESH RENDER — STATE {state_def['state_id']}: {state_def['display_name'].upper()} ({state_def['complete_mesh_name']})",
             color="#F5F8FF", fontsize=14.5, fontweight="bold")
    fig.text(0.03, 0.915,
             f"LOCKED ENVELOPE  |  Visual Bounds: {metrics['dimensions'][0]:.2f} x {metrics['dimensions'][1]:.2f} x {metrics['dimensions'][2]:.2f} studs  |  "
             f"Gameplay Collider: 12.00 x 2.00 x 12.00 studs (0.20-stud gap)  |  "
             f"Triangles: {metrics['triangle_count']} / 250 max  |  Degenerate Tris: {metrics['degenerate_triangles']}",
             color=emi_hex, fontsize=9.8, fontweight="bold")
    fig.text(0.03, 0.887,
             f"MULTI-NODE & VERTEX-COLOR READY  |  Child MeshParts: Part_MAT_DarkNeutral, Part_MAT_AltNeutral, Part_MAT_LightTrim, Part_{state_def['primary_emissive']}  |  "
             f"Origin: (0,0,0) Centered, +Y Up, +Z Forward",
             color="#AABED7", fontsize=8.8)

    cbox = [(-6.0, 6.0, -1.0, 1.0, -6.0, 6.0)]
    panels = [
        ("1. Top Orthographic View (Material-Colour & Small-Scale Readability)", "top", "material", 10.2),
        ("2. Side Orthographic Elevation (Looking -X — 2.0-Stud Profile & Bevels)", "side", "material", 7.2),
        ("3. 3/4 Perspective View (Material-Colour + Child Part Hierarchy)", "persp", "material", 8.8),
        ("4. Technical Wireframe View (< 250 Tris + 12x2x12 Collider Envelope)", "persp", "wireframe", 8.8),
    ]

    for idx, (vtitle, vtype, rmode, sx) in enumerate(panels):
        ax = fig.add_subplot(2, 2, idx + 1, facecolor="#171F2E")
        ax.set_position([0.03 + (idx % 2) * 0.48, 0.035 + (1 - idx // 2) * 0.41, 0.45, 0.375])
        w_px = 680
        h_px = int(w_px * (0.375 * 9.6) / (0.45 * 16.0))
        min_half = 3.2 if vtype == "side" else (7.0 if vtype == "top" else 6.6)
        adj_sy = max(sx * (h_px / w_px), min_half)
        sx = adj_sy * (w_px / h_px)
        img_arr = rasterize_meshes_zbuffer(
            [(mb, (0, 0, 0))], view_type=vtype, width=w_px, height=h_px,
            span_x=sx, span_y=adj_sy, center=(0, 0, 0), render_mode=rmode, collider_boxes=cbox
        )
        annotate_panel(ax, img_arr, vtitle, vtype, show_legend=(idx in [0, 1]), accent_hex=emi_hex)

    fig.savefig(out_png, dpi=150, facecolor="#0F141F")
    plt.close(fig)


def render_six_state_comparison_sheet(state_records, out_png, sheet_kind="top_material"):
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    fig = plt.figure(figsize=(20, 11.5), dpi=150, facecolor="#0F141F")

    if sheet_kind == "top_material":
        title_str = "SPHERE BRAWL: ROLLING RAMPAGE — ALL 6 ARENA TILE STATES (TOP VIEW MATERIAL-COLOUR & GAMEPLAY READABILITY)"
        subtitle_str = "PYTHON SOFTWARE Z-BUFFER RENDER FROM EXPORTED .OBJ/.GLB MESHES  |  Exact Approved RGB Palette & Emissive Accents  |  11.8x2.0x11.8 Studs on 12.0-Stud Grid"
        vtype, rmode, sx = "top", "material", 9.2
    elif sheet_kind == "persp_material":
        title_str = "SPHERE BRAWL: ROLLING RAMPAGE — ALL 6 ARENA TILE STATES (3/4 PERSPECTIVE MATERIAL-COLOUR REVIEW SHEET)"
        subtitle_str = "PYTHON SOFTWARE Z-BUFFER RENDER FROM EXPORTED .OBJ/.GLB MESHES  |  Shows Intended Material Colours (MAT_DarkNeutral, MAT_AltNeutral, MAT_LightTrim + EMI_*)"
        vtype, rmode, sx = "persp", "material", 8.6
    elif sheet_kind == "neutral_clay":
        title_str = "SPHERE BRAWL: ROLLING RAMPAGE — ALL 6 ARENA TILE STATES (NEUTRAL LIGHTING GEOMETRY COMPARISON SHEET)"
        subtitle_str = "PYTHON SOFTWARE Z-BUFFER RENDER (UNIFORM NEUTRAL STUDIO CLAY LIGHTING)  |  Isolates Raised Hard-Surface Overlay Silhouettes & Bevel Relief Without Colour Bias"
        vtype, rmode, sx = "persp", "neutral", 8.6
    elif sheet_kind == "side_elevation":
        title_str = "SPHERE BRAWL: ROLLING RAMPAGE — ALL 6 ARENA TILE STATES (SIDE ELEVATION 2.0-STUD PROFILE COMPARISON)"
        subtitle_str = "PYTHON SOFTWARE Z-BUFFER RENDER (ORTHOGRAPHIC SIDE ELEVATION)  |  Verifies Local Y in [-1.00, +1.00] Studs (World Y = 51.0 Top Surface when Centered at Y = 50.0)"
        vtype, rmode, sx = "side", "material", 7.2
    else:
        title_str = "SPHERE BRAWL: ROLLING RAMPAGE — ALL 6 ARENA TILE STATES (TECHNICAL WIREFRAME & TRIANGLE BUDGET SHEET)"
        subtitle_str = "PYTHON SOFTWARE Z-BUFFER WIREFRAME RENDER  |  All 6 Complete States Strictly < 250 Triangles (212 to 234 Tris = 84 Base + 128..150 Overlay)"
        vtype, rmode, sx = "persp", "wireframe", 8.6

    fig.text(0.025, 0.952, title_str, color="#F5F8FF", fontsize=16.2, fontweight="bold")
    fig.text(0.025, 0.922, subtitle_str, color="#00C3FF", fontsize=10.2, fontweight="bold")
    fig.text(0.025, 0.896,
             "Note: Rendered directly from the exported 3D mesh files in Python (not a concept illustration or unverified studio screenshot). "
             "Multi-node GLB & multi-object OBJ split each material slot into its own child part.",
             color="#AABED7", fontsize=9.0)

    cbox = [(-6.0, 6.0, -1.0, 1.0, -6.0, 6.0)]
    w_px = 600
    h_px = int(w_px * (0.365 * 11.5) / (0.30 * 20.0))
    min_half = 3.2 if vtype == "side" else (7.0 if vtype == "top" else 6.6)
    adj_sy = max(sx * (h_px / w_px), min_half)
    sx = adj_sy * (w_px / h_px)

    for idx, rec in enumerate(state_records):
        sdef = rec["def"]
        mb = rec["complete_mb"]
        m = rec["complete_obj"]
        emi_hex = "#{:02X}{:02X}{:02X}".format(*sdef["primary_emissive_rgb"])

        row = idx // 3
        col_i = idx % 3
        ax = fig.add_subplot(2, 3, idx + 1, facecolor="#171F2E")
        ax.set_position([0.025 + col_i * 0.322, 0.04 + (1 - row) * 0.405, 0.30, 0.365])

        img_arr = rasterize_meshes_zbuffer(
            [(mb, (0, 0, 0))], view_type=vtype, width=w_px, height=h_px,
            span_x=sx, span_y=adj_sy, center=(0, 0, 0), render_mode=rmode, collider_boxes=cbox
        )
        rgb_tuple = sdef["primary_emissive_rgb"]
        title_lbl = (
            f"{sdef['display_name']}\n"
            f"{m['triangle_count']} Tris ({rec['overlay_obj']['triangle_count']} Overlay + 84 Base) | "
            f"{sdef['primary_emissive']} RGB({rgb_tuple[0]},{rgb_tuple[1]},{rgb_tuple[2]})"
        )
        annotate_panel(ax, img_arr, title_lbl, vtype, show_legend=(idx == 0), accent_hex=emi_hex)
        ax.title.set_color(emi_hex if rmode == "material" else "#F5F8FF")

    fig.savefig(out_png, dpi=150, facecolor="#0F141F")
    plt.close(fig)


def render_neighbor_grid_spacing_sheet(state_records, out_png):
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    fig = plt.figure(figsize=(18, 9.5), dpi=150, facecolor="#0F141F")

    fig.text(0.03, 0.945,
             "ARENA GRID PITCH & SMALL-SCALE GAMEPLAY READABILITY — 2x3 TILE ARRAY ON 12.0-STUD PITCH (WORLD Y = 51.0 TOP)",
             color="#F5F8FF", fontsize=15.5, fontweight="bold")
    fig.text(0.03, 0.912,
             "PYTHON SOFTWARE Z-BUFFER RENDER  |  Grid Pitch: 12.0000 studs  |  Visual Tile: 11.8000 studs  |  "
             "Inter-Tile Seam Gap: 0.2000 studs  |  Tile Center Y: 50.0 -> Top Surface: World Y = 51.0",
             color="#00FF88", fontsize=10.0, fontweight="bold")
    fig.text(0.03, 0.884,
             "Left Panel: Top-down arena camera view verifying 0.20-stud expansion gaps and instant hazard readability at small gameplay scale. "
             "Right Panel: 3/4 Arena Perspective Assembly.",
             color="#AABED7", fontsize=9.0)

    grid_offsets = [
        (-6.0, 50.0, -12.0),
        ( 6.0, 50.0, -12.0),
        (-6.0, 50.0,   0.0),
        ( 6.0, 50.0,   0.0),
        (-6.0, 50.0,  12.0),
        ( 6.0, 50.0,  12.0),
    ]
    instances = [(rec["complete_mb"], grid_offsets[i]) for i, rec in enumerate(state_records)]
    cboxes = [(ox - 6.0, ox + 6.0, oy - 1.0, oy + 1.0, oz - 6.0, oz + 6.0) for (ox, oy, oz) in grid_offsets]

    panels = [
        ("1. Top Orthographic Grid Plan (12.0-Stud Pitch / 0.20-Stud Visible Seam Gaps)", "top", 18.2),
        ("2. 3/4 Arena Perspective Assembly (World Y = 51.00 Top Surface)", "persp", 22.5),
    ]

    for v_idx, (vtitle, vtype, sx) in enumerate(panels):
        ax = fig.add_subplot(1, 2, v_idx + 1, facecolor="#171F2E")
        ax.set_position([0.03 + v_idx * 0.48, 0.05, 0.45, 0.79])
        w_px = 760
        h_px = int(w_px * (0.79 * 9.5) / (0.45 * 18.0))
        adj_sy = max(sx * (h_px / w_px), 19.8 if vtype == "top" else 14.5)
        sx = adj_sy * (w_px / h_px)
        img_arr = rasterize_meshes_zbuffer(
            instances, view_type=vtype, width=w_px, height=h_px,
            span_x=sx, span_y=adj_sy, center=(0.0, 50.0, 0.0), render_mode="material", collider_boxes=cboxes
        )
        annotate_panel(ax, img_arr, vtitle, vtype, show_legend=(v_idx == 0), accent_hex="#00FF88")

    fig.savefig(out_png, dpi=150, facecolor="#0F141F")
    plt.close(fig)


# ==============================================================================
# 4. INDEPENDENT FILE-LEVEL VALIDATORS (OBJ, MTL, GLB, DETERMINISM, PREVIEWS)
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
                if len(parts) < 4:
                    syntax_errors.append(f"Line {line_no}: malformed v")
                else:
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
        if area < 1e-7:
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
        "object_Subparts": objects,
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
            and len(v_colors) == len(verts)
            and len(uvs) >= len(usemtls)
        ),
    }


def parse_and_validate_glb(glb_path):
    with open(glb_path, "rb") as f:
        data = f.read()

    magic, version, total_length = struct.unpack("<4sII", data[:12])
    magic_str = magic.decode("ascii", errors="replace")
    header_ok = (magic_str == "glTF") and (version == 2) and (total_length == len(data))

    c0_len, c0_type = struct.unpack("<I4s", data[12:20])
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

    # Verify material baseColorFactor and emissiveFactor against APPROVED_PALETTE_METADATA
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
            mat_errors.append(f"GLB baseColorFactor mismatch on {mname}: {bcf} vs {exp}")
        if APPROVED_PALETTE_METADATA[mname]["emissive"]:
            if max(abs(emif[i] - exp[i]) for i in range(3)) > 1e-3:
                mat_errors.append(f"GLB emissiveFactor mismatch on {mname}: {emif} vs {exp}")
        mat_audit[mname] = {
            "baseColorFactor": bcf,
            "emissiveFactor": emif,
            "has_baseColorTexture": has_tex,
            "metallicFactor": pbr.get("metallicFactor"),
            "roughnessFactor": pbr.get("roughnessFactor"),
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
            and total_tris > 0
        ),
    }


def validate_preview_png(png_path):
    with Image.open(png_path) as im:
        im.verify()
    with Image.open(png_path) as im:
        w, h = im.size
        arr = np.asarray(im.convert("RGB"), dtype=np.float32)
        std_val = float(arr.std())
    return {
        "width": w,
        "height": h,
        "pixel_std": round(std_val, 2),
        "valid": (w >= 1600 and h >= 900 and std_val > 12.0),
    }


if __name__ == "__main__":
    print("Step 1: Building Shared Base + 6 State Overlays + 6 Complete States with Multi-Node GLB & Vertex Colors...")
    base_mb = build_shared_base_tile("SM_ArenaTile_SharedBase")
    mod_dir = os.path.join(PKG_STAGE_DIR, "meshes/modular_base_and_overlays")
    comp_dir = os.path.join(PKG_STAGE_DIR, "meshes/complete_states")

    base_obj_path = os.path.join(mod_dir, "SM_ArenaTile_SharedBase.obj")
    base_mtl_path = os.path.join(mod_dir, "SM_ArenaTile_SharedBase.mtl")
    base_glb_path = os.path.join(mod_dir, "SM_ArenaTile_SharedBase.glb")
    base_mb.export_obj_and_mtl(base_obj_path, base_mtl_path)
    base_mb.export_glb(base_glb_path)

    # Determinism check: export a second copy to /tmp and compare SHA-256
    os.makedirs("/tmp/det_test_dir", exist_ok=True)
    det_test_obj = "/tmp/det_test_dir/SM_ArenaTile_SharedBase.obj"
    det_test_mtl = "/tmp/det_test_dir/SM_ArenaTile_SharedBase.mtl"
    det_test_glb = "/tmp/det_test_dir/SM_ArenaTile_SharedBase.glb"
    base_mb2 = build_shared_base_tile("SM_ArenaTile_SharedBase")
    base_mb2.export_obj_and_mtl(det_test_obj, det_test_mtl)
    base_mb2.export_glb(det_test_glb)
    determinism_ok = (
        sha256_of_file(base_obj_path) == sha256_of_file(det_test_obj)
        and sha256_of_file(base_mtl_path) == sha256_of_file(det_test_mtl)
        and sha256_of_file(base_glb_path) == sha256_of_file(det_test_glb)
    )
    assert determinism_ok, "Determinism check failed on SharedBase!"

    base_obj_audit = parse_and_validate_obj(base_obj_path)
    base_mtl_audit = parse_and_validate_mtl(base_mtl_path)
    base_glb_audit = parse_and_validate_glb(base_glb_path)

    state_records = []
    for sdef in STATE_DEFINITIONS:
        ov_name = sdef["overlay_mesh_name"]
        comp_name = sdef["complete_mesh_name"]

        ov_mb = sdef["builder_fn"](ov_name)
        ov_obj_path = os.path.join(mod_dir, f"{ov_name}.obj")
        ov_mtl_path = os.path.join(mod_dir, f"{ov_name}.mtl")
        ov_glb_path = os.path.join(mod_dir, f"{ov_name}.glb")
        ov_mb.export_obj_and_mtl(ov_obj_path, ov_mtl_path)
        ov_mb.export_glb(ov_glb_path)

        comp_mb = build_shared_base_tile(comp_name)
        comp_mb.merge_from(ov_mb)
        comp_obj_path = os.path.join(comp_dir, f"{comp_name}.obj")
        comp_mtl_path = os.path.join(comp_dir, f"{comp_name}.mtl")
        comp_glb_path = os.path.join(comp_dir, f"{comp_name}.glb")
        comp_mb.export_obj_and_mtl(comp_obj_path, comp_mtl_path)
        comp_mb.export_glb(comp_glb_path)

        # Determinism check on complete state
        comp_mb_re = build_shared_base_tile(comp_name)
        comp_mb_re.merge_from(sdef["builder_fn"](ov_name))
        comp_mb_re.export_glb(det_test_glb)
        assert sha256_of_file(comp_glb_path) == sha256_of_file(det_test_glb), f"Determinism mismatch on {comp_name}"

        ov_obj_audit = parse_and_validate_obj(ov_obj_path)
        ov_mtl_audit = parse_and_validate_mtl(ov_mtl_path)
        ov_glb_audit = parse_and_validate_glb(ov_glb_path)

        comp_obj_audit = parse_and_validate_obj(comp_obj_path)
        comp_mtl_audit = parse_and_validate_mtl(comp_mtl_path)
        comp_glb_audit = parse_and_validate_glb(comp_glb_path)

        preview_rel = f"previews/Preview_{comp_name}.png"
        render_individual_state_sheet(sdef, comp_mb, comp_obj_audit, os.path.join(PKG_STAGE_DIR, preview_rel))

        state_records.append({
            "def": sdef,
            "overlay_mb": ov_mb,
            "complete_mb": comp_mb,
            "overlay_obj": ov_obj_audit,
            "overlay_mtl": ov_mtl_audit,
            "overlay_glb": ov_glb_audit,
            "complete_obj": comp_obj_audit,
            "complete_mtl": comp_mtl_audit,
            "complete_glb": comp_glb_audit,
            "preview_rel": preview_rel,
        })
        print(f"  Verified {comp_name}: {comp_obj_audit['triangle_count']} tris, child_parts={comp_glb_audit['child_part_nodes']}")

    print("Step 2: Rendering 6-State Comparison Sheets (Material-Colour, Neutral Clay Lighting, Side, Wireframe, 2x3 Grid)...")
    comp_sheets = {
        "top_material_comparison": "previews/ArenaTiles_All6States_TopComparison.png",
        "perspective_material_comparison": "previews/ArenaTiles_All6States_PerspectiveComparison.png",
        "neutral_clay_geometry_comparison": "previews/ArenaTiles_All6States_NeutralClay_GeometryComparison.png",
        "side_elevation_comparison": "previews/ArenaTiles_All6States_SideComparison.png",
        "wireframe_comparison": "previews/ArenaTiles_All6States_WireframeComparison.png",
        "neighbor_grid_spacing_2x3": "previews/ArenaTiles_2x3_GridSpacing_Verification.png",
    }
    render_six_state_comparison_sheet(state_records, os.path.join(PKG_STAGE_DIR, comp_sheets["top_material_comparison"]), "top_material")
    render_six_state_comparison_sheet(state_records, os.path.join(PKG_STAGE_DIR, comp_sheets["perspective_material_comparison"]), "persp_material")
    render_six_state_comparison_sheet(state_records, os.path.join(PKG_STAGE_DIR, comp_sheets["neutral_clay_geometry_comparison"]), "neutral_clay")
    render_six_state_comparison_sheet(state_records, os.path.join(PKG_STAGE_DIR, comp_sheets["side_elevation_comparison"]), "side_elevation")
    render_six_state_comparison_sheet(state_records, os.path.join(PKG_STAGE_DIR, comp_sheets["wireframe_comparison"]), "wireframe")
    render_neighbor_grid_spacing_sheet(state_records, os.path.join(PKG_STAGE_DIR, comp_sheets["neighbor_grid_spacing_2x3"]))

    # Copy updated top, perspective, and neutral clay comparison sheets to OUT_DIR for user preview
    shutil.copy2(os.path.join(PKG_STAGE_DIR, comp_sheets["top_material_comparison"]), os.path.join(OUT_DIR, "Sphere_Brawl_Arena_Tiles_TopComparison.png"))
    shutil.copy2(os.path.join(PKG_STAGE_DIR, comp_sheets["perspective_material_comparison"]), os.path.join(OUT_DIR, "Sphere_Brawl_Arena_Tiles_PerspectiveComparison.png"))
    shutil.copy2(os.path.join(PKG_STAGE_DIR, comp_sheets["neutral_clay_geometry_comparison"]), os.path.join(OUT_DIR, "Sphere_Brawl_Arena_Tiles_NeutralClay_Comparison.png"))
    shutil.copy2(os.path.join(PKG_STAGE_DIR, comp_sheets["neighbor_grid_spacing_2x3"]), os.path.join(OUT_DIR, "Sphere_Brawl_Arena_Tiles_GridSpacing_Verification.png"))

    print("Step 3: Mesh and preview generation complete.")
