#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — STANDALONE DETERMINISTIC BLENDER 3.x / 4.x GENERATOR
====================================================================================
Recreates the exact 6-State Arena Tile Collection and Shared Base geometry AND
all 9 approved materials deterministically from scratch inside Blender (`bpy`),
or runs in standalone Python mode (`generate_arena_tiles_pipeline.py` compatible)
when invoked outside Blender.
"""

import os
import sys
import math

try:
    import bpy
    HAS_BPY = True
except ImportError:
    HAS_BPY = False

PALETTE_SRGB = {
    "MAT_DarkNeutral": (32, 38, 54),
    "MAT_AltNeutral":  (42, 50, 70),
    "MAT_LightTrim":   (170, 190, 215),
    "EMI_Cyan":        (0, 195, 255),
    "EMI_Ice":         (0, 235, 255),
    "EMI_Magnetic":    (165, 55, 255),
    "EMI_Kinetic":     (255, 125, 0),
    "EMI_Amber":       (255, 170, 0),
    "EMI_DangerRed":   (255, 40, 40),
}

PALETTE_RGBA = {
    k: (v[0] / 255.0, v[1] / 255.0, v[2] / 255.0, 1.0)
    for k, v in PALETTE_SRGB.items()
}


class DeterministicGeometryCollector:
    """Collects deterministic triangles grouped by `(group_name, mat_name)` with outward CCW normals."""

    def __init__(self, name):
        self.name = name
        self.groups = {}

    @staticmethod
    def _cross(a, b):
        return (
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        )

    @staticmethod
    def _sub(a, b):
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    @staticmethod
    def _dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def add_tri(self, group_name, mat_name, v0, v1, v2, expected_normal=None):
        p0 = tuple(round(float(x), 5) for x in v0)
        p1 = tuple(round(float(x), 5) for x in v1)
        p2 = tuple(round(float(x), 5) for x in v2)
        cr = self._cross(self._sub(p1, p0), self._sub(p2, p0))
        if expected_normal is not None and self._dot(cr, expected_normal) < 0.0:
            p1, p2 = p2, p1
        self.groups.setdefault((group_name, mat_name), []).append((p0, p1, p2))

    def add_quad(self, group_name, mat_name, v0, v1, v2, v3, expected_normal=None):
        self.add_tri(group_name, mat_name, v0, v1, v2, expected_normal)
        self.add_tri(group_name, mat_name, v0, v2, v3, expected_normal)

    def merge_from(self, other):
        for k, tris in other.groups.items():
            self.groups.setdefault(k, []).extend(tris)

    def add_frustum_pad(self, group_name, mat_name, x0, x1, z0, z1, y0, y1, inset_top=0.04, include_bottom=False):
        ix0, ix1 = x0 + inset_top, x1 - inset_top
        iz0, iz1 = z0 + inset_top, z1 - inset_top
        t_nw, t_sw, t_se, t_ne = (ix0, y1, iz0), (ix0, y1, iz1), (ix1, y1, iz1), (ix1, y1, iz0)
        b_nw, b_sw, b_se, b_ne = (x0, y0, z0), (x0, y0, z1), (x1, y0, z1), (x1, y0, z0)
        self.add_quad(group_name, mat_name, t_nw, t_sw, t_se, t_ne, (0, 1, 0))
        self.add_quad(group_name, mat_name, b_sw, b_se, t_se, t_sw, (0, 0.2, 1))
        self.add_quad(group_name, mat_name, b_ne, b_nw, t_nw, t_ne, (0, 0.2, -1))
        self.add_quad(group_name, mat_name, b_se, b_ne, t_ne, t_se, (1, 0.2, 0))
        self.add_quad(group_name, mat_name, b_nw, b_sw, t_sw, t_nw, (-1, 0.2, 0))
        if include_bottom:
            self.add_quad(group_name, mat_name, b_nw, b_ne, b_se, b_sw, (0, -1, 0))

    def add_extruded_polygon_y(self, group_name, mat_name, poly_xz, y0, y1, tris_indices):
        n_pts = len(poly_xz)
        for (i0, i1, i2) in tris_indices:
            self.add_tri(
                group_name, mat_name,
                (poly_xz[i0][0], y1, poly_xz[i0][1]),
                (poly_xz[i1][0], y1, poly_xz[i1][1]),
                (poly_xz[i2][0], y1, poly_xz[i2][1]),
                (0, 1, 0),
            )
        for i in range(n_pts):
            x_a, z_a = poly_xz[i]
            x_b, z_b = poly_xz[(i + 1) % n_pts]
            dx, dz = x_b - x_a, z_b - z_a
            self.add_quad(
                group_name, mat_name,
                (x_a, y0, z_a), (x_b, y0, z_b), (x_b, y1, z_b), (x_a, y1, z_a),
                (dz, 0.0, -dx),
            )

    def add_annular_ring_y(self, group_name, mat_name, r_in, r_out, y0, y1, n_segs=8, theta_offset=0.0):
        for i in range(n_segs):
            t0 = theta_offset + (2.0 * math.pi * i) / n_segs
            t1 = theta_offset + (2.0 * math.pi * (i + 1)) / n_segs
            c0, s0 = math.cos(t0), math.sin(t0)
            c1, s1 = math.cos(t1), math.sin(t1)
            ti0, ti1 = (r_in * c0, y1, r_in * s0), (r_in * c1, y1, r_in * s1)
            to1, to0 = (r_out * c1, y1, r_out * s1), (r_out * c0, y1, r_out * s0)
            bi0, bi1 = (r_in * c0, y0, r_in * s0), (r_in * c1, y0, r_in * s1)
            bo1, bo0 = (r_out * c1, y0, r_out * s1), (r_out * c0, y0, r_out * s0)
            tm = 0.5 * (t0 + t1)
            self.add_quad(group_name, mat_name, ti0, ti1, to1, to0, (0, 1, 0))
            self.add_quad(group_name, mat_name, bo0, bo1, to1, to0, (math.cos(tm), 0.0, math.sin(tm)))
            self.add_quad(group_name, mat_name, bi1, bi0, ti0, ti1, (-math.cos(tm), 0.0, -math.sin(tm)))

    def add_chevron_z(self, group_name, mat_name, z_tip, z_mid, z_tail, half_w, y0, y1):
        poly_xz = [(0.0, z_tip), (-half_w, z_mid), (-half_w, z_tail), (0.0, z_mid), (half_w, z_tail), (half_w, z_mid)]
        tris = [(0, 1, 3), (1, 2, 3), (0, 3, 5), (3, 4, 5)]
        self.add_extruded_polygon_y(group_name, mat_name, poly_xz, y0, y1, tris)


def build_shared_base(name="SM_ArenaTile_SharedBase"):
    mb = DeterministicGeometryCollector(name)
    b0, b1, b2, b3 = (-5.42, -1.00, -5.42), (5.42, -1.00, -5.42), (5.42, -1.00, 5.42), (-5.42, -1.00, 5.42)
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b0, b1, b2, b3, (0, -1, 0))
    m0, m1, m2, m3 = (-5.90, -0.45, -5.90), (-5.90, -0.45, 5.90), (5.90, -0.45, 5.90), (5.90, -0.45, -5.90)
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b3, b2, m2, m1, (0, -0.5, 1))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b1, b0, m0, m3, (0, -0.5, -1))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b2, b1, m3, m2, (1, -0.5, 0))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", b0, b3, m1, m0, (-1, -0.5, 0))
    u0, u1, u2, u3 = (-5.90, 0.72, -5.90), (-5.90, 0.72, 5.90), (5.90, 0.72, 5.90), (5.90, 0.72, -5.90)
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", m1, m2, u2, u1, (0, 0, 1))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", m3, m0, u0, u3, (0, 0, -1))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", m2, m3, u3, u2, (1, 0, 0))
    mb.add_quad("TileBase_LowerHull", "MAT_DarkNeutral", m0, m1, u1, u0, (-1, 0, 0))
    r_out0, r_out1, r_out2, r_out3 = (-5.68, 1.00, -5.68), (-5.68, 1.00, 5.68), (5.68, 1.00, 5.68), (5.68, 1.00, -5.68)
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", u1, u2, r_out2, r_out1, (0, 0.7, 1))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", u3, u0, r_out0, r_out3, (0, 0.7, -1))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", u2, u3, r_out3, r_out2, (1, 0.7, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", u0, u1, r_out1, r_out0, (-1, 0.7, 0))
    r_in0, r_in1, r_in2, r_in3 = (-5.16, 1.00, -5.16), (-5.16, 1.00, 5.16), (5.16, 1.00, 5.16), (5.16, 1.00, -5.16)
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_out1, r_out2, r_in2, r_in1, (0, 1, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_out3, r_out0, r_in0, r_in3, (0, 1, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_out2, r_out3, r_in3, r_in2, (0, 1, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_out0, r_out1, r_in1, r_in0, (0, 1, 0))
    d0, d1, d2, d3 = (-4.96, 0.86, -4.96), (-4.96, 0.86, 4.96), (4.96, 0.86, 4.96), (4.96, 0.86, -4.96)
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_in1, r_in2, d2, d1, (0, 0.7, -1))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_in3, r_in0, d0, d3, (0, 0.7, 1))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_in2, r_in3, d3, d2, (-1, 0.7, 0))
    mb.add_quad("TileBase_BeveledRim", "MAT_LightTrim", r_in0, r_in1, d1, d0, (1, 0.7, 0))
    mb.add_quad("TileBase_RecessedDeck", "MAT_AltNeutral", d0, d1, d2, d3, (0, 1, 0))
    for cname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        cx, cz = sx * 4.34, sz * 4.34
        mb.add_frustum_pad(f"TileBase_CornerBolster_{cname}", "MAT_DarkNeutral", cx - 0.58, cx + 0.58, cz - 0.58, cz + 0.58, 0.86, 0.99, 0.06)
    return mb


def build_all_overlays():
    ov1 = DeterministicGeometryCollector("SM_ArenaTile_Overlay_01_SafeNormal")
    for qname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        x0, x1 = (0.52, 3.62) if sx > 0 else (-3.62, -0.52)
        z0, z1 = (0.52, 3.62) if sz > 0 else (-3.62, -0.52)
        ov1.add_frustum_pad(f"Safe_QuadArmor_{qname}", "MAT_DarkNeutral", x0, x1, z0, z1, 0.86, 0.98, 0.06)
    ov1.add_frustum_pad("Safe_CenterCoreHub", "MAT_LightTrim", -0.44, 0.44, -0.44, 0.44, 0.86, 0.99, 0.05)
    ov1.add_frustum_pad("Safe_CyanSeam_North", "EMI_Cyan", -0.22, 0.22, -3.55, -0.62, 0.86, 0.93, 0.02)
    ov1.add_frustum_pad("Safe_CyanSeam_South", "EMI_Cyan", -0.22, 0.22,  0.62,  3.55, 0.86, 0.93, 0.02)
    ov1.add_frustum_pad("Safe_CyanSeam_West",  "EMI_Cyan", -3.55, -0.62, -0.22, 0.22, 0.86, 0.93, 0.02)
    ov1.add_frustum_pad("Safe_CyanSeam_East",  "EMI_Cyan",  0.62,  3.55, -0.22, 0.22, 0.86, 0.93, 0.02)
    ov1.add_frustum_pad("Safe_CyanNode_North", "EMI_Cyan", -1.40, 1.40, -4.55, -4.18, 0.86, 0.94, 0.02)
    ov1.add_frustum_pad("Safe_CyanNode_South", "EMI_Cyan", -1.40, 1.40,  4.18,  4.55, 0.86, 0.94, 0.02)
    ov1.add_frustum_pad("Safe_CyanNode_West",  "EMI_Cyan", -4.55, -4.18, -1.40, 1.40, 0.86, 0.94, 0.02)
    ov1.add_frustum_pad("Safe_CyanNode_East",  "EMI_Cyan",  4.18,  4.55, -1.40, 1.40, 0.86, 0.94, 0.02)

    ov2 = DeterministicGeometryCollector("SM_ArenaTile_Overlay_02_Warning")
    ov2.add_frustum_pad("Warn_AmberPerimeter_N", "EMI_Amber", -3.40, 3.40, -4.65, -4.10, 0.86, 0.96, 0.03)
    ov2.add_frustum_pad("Warn_AmberPerimeter_S", "EMI_Amber", -3.40, 3.40,  4.10,  4.65, 0.86, 0.96, 0.03)
    ov2.add_frustum_pad("Warn_AmberPerimeter_W", "EMI_Amber", -4.65, -4.10, -3.40, 3.40, 0.86, 0.96, 0.03)
    ov2.add_frustum_pad("Warn_AmberPerimeter_E", "EMI_Amber",  4.10,  4.65, -3.40, 3.40, 0.86, 0.96, 0.03)
    for qname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        x0, x1 = (1.35, 3.75) if sx > 0 else (-3.75, -1.35)
        z0, z1 = (1.35, 3.75) if sz > 0 else (-3.75, -1.35)
        ov2.add_frustum_pad(f"Warn_DarkPlate_{qname}", "MAT_DarkNeutral", x0, x1, z0, z1, 0.86, 0.98, 0.05)
    ov2.add_frustum_pad("Warn_AmberStripe_N", "EMI_Amber", -0.65, 0.65, -3.75, -1.45, 0.86, 0.96, 0.03)
    ov2.add_frustum_pad("Warn_AmberStripe_S", "EMI_Amber", -0.65, 0.65,  1.45,  3.75, 0.86, 0.96, 0.03)
    ov2.add_frustum_pad("Warn_AmberStripe_W", "EMI_Amber", -3.75, -1.45, -0.65, 0.65, 0.86, 0.96, 0.03)
    ov2.add_frustum_pad("Warn_AmberStripe_E", "EMI_Amber",  1.45,  3.75, -0.65, 0.65, 0.86, 0.96, 0.03)
    ov2.add_frustum_pad("Warn_CentralBeaconOuter", "EMI_Amber", -1.20, 1.20, -1.20, 1.20, 0.86, 0.97, 0.04)
    ov2.add_frustum_pad("Warn_CentralBeaconInner", "MAT_DarkNeutral", -0.55, 0.55, -0.55, 0.55, 0.97, 0.995, 0.03)

    ov3 = DeterministicGeometryCollector("SM_ArenaTile_Overlay_03_IceCorridor")
    for idx, xc in enumerate([-3.30, -1.15, 1.15, 3.30]):
        ov3.add_frustum_pad(f"Ice_CryoChannel_{idx+1}", "EMI_Ice", xc - 0.32, xc + 0.32, -4.55, 4.55, 0.86, 0.95, 0.03)
    for idx, (x0, x1) in enumerate([(-2.75, -1.65), (-0.65, 0.65), (1.65, 2.75)]):
        ov3.add_frustum_pad(f"Ice_SledDeck_{idx+1}", "MAT_DarkNeutral", x0, x1, -4.35, 4.35, 0.86, 0.98, 0.05)
    for idx, zc in enumerate([-2.20, 2.20]):
        ov3.add_frustum_pad(f"Ice_FrostCrossLink_{idx+1}", "EMI_Ice", -3.60, 3.60, zc - 0.24, zc + 0.24, 0.86, 0.94, 0.02)
    for cname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        ov3.add_frustum_pad(f"Ice_FrostEndTrim_{cname}", "MAT_LightTrim", sx * 2.20 - 0.85, sx * 2.20 + 0.85, sz * 4.58 - 0.22, sz * 4.58 + 0.22, 0.86, 0.99, 0.03)

    ov4 = DeterministicGeometryCollector("SM_ArenaTile_Overlay_04_MagneticStorm")
    rot_oct = math.pi / 8.0
    ov4.add_annular_ring_y("Mag_OuterFieldRing", "EMI_Magnetic", 3.10, 3.78, 0.86, 0.95, 8, rot_oct)
    ov4.add_annular_ring_y("Mag_InnerFieldRing", "EMI_Magnetic", 1.35, 1.95, 0.86, 0.96, 8, rot_oct)
    ov4.add_frustum_pad("Mag_PoleShoe_North", "MAT_LightTrim", -0.48, 0.48, -4.55, -2.05, 0.86, 0.985, 0.04)
    ov4.add_frustum_pad("Mag_PoleShoe_South", "MAT_LightTrim", -0.48, 0.48,  2.05,  4.55, 0.86, 0.985, 0.04)
    ov4.add_frustum_pad("Mag_PoleShoe_West",  "MAT_LightTrim", -4.55, -2.05, -0.48, 0.48, 0.86, 0.985, 0.04)
    ov4.add_frustum_pad("Mag_PoleShoe_East",  "MAT_LightTrim",  2.05,  4.55, -0.48, 0.48, 0.86, 0.985, 0.04)
    ov4.add_frustum_pad("Mag_CenterCoreCap", "MAT_DarkNeutral", -0.78, 0.78, -0.78, 0.78, 0.86, 0.99, 0.05)

    ov5 = DeterministicGeometryCollector("SM_ArenaTile_Overlay_05_BoostRunway")
    for cname, z_tip, z_mid, z_tail in [("Rear", -0.95, -2.45, -3.55), ("Mid", 1.55, 0.05, -1.05), ("Front", 4.05, 2.55, 1.45)]:
        ov5.add_chevron_z(f"Boost_Chevron_{cname}", "EMI_Kinetic", z_tip, z_mid, z_tail, 2.55, 0.86, 0.965)
    ov5.add_frustum_pad("Boost_GuideRail_Left",  "MAT_DarkNeutral", -4.45, -3.45, -4.45, 4.45, 0.86, 0.985, 0.05)
    ov5.add_frustum_pad("Boost_GuideRail_Right", "MAT_DarkNeutral",  3.45,  4.45, -4.45, 4.45, 0.86, 0.985, 0.05)
    ov5.add_frustum_pad("Boost_SideStrip_Left",  "EMI_Kinetic", -3.25, -2.90, -4.20, 4.20, 0.86, 0.94, 0.02)
    ov5.add_frustum_pad("Boost_SideStrip_Right", "EMI_Kinetic",  2.90,  3.25, -4.20, 4.20, 0.86, 0.94, 0.02)
    for cname, sx, sz in [("NW", -1, -1), ("NE", 1, -1), ("SE", 1, 1), ("SW", -1, 1)]:
        ov5.add_frustum_pad(f"Boost_RailCleat_{cname}", "MAT_LightTrim", sx * 3.95 - 0.38, sx * 3.95 + 0.38, sz * 2.25 - 0.85, sz * 2.25 + 0.85, 0.985, 1.00, 0.03)

    ov6 = DeterministicGeometryCollector("SM_ArenaTile_Overlay_06_RingCollapse")
    ov6.add_frustum_pad("Collapse_RedPerimeter_N", "EMI_DangerRed", -3.65, 3.65, -4.78, -4.18, 0.86, 0.97, 0.03)
    ov6.add_frustum_pad("Collapse_RedPerimeter_S", "EMI_DangerRed", -3.65, 3.65,  4.18,  4.78, 0.86, 0.97, 0.03)
    ov6.add_frustum_pad("Collapse_RedPerimeter_W", "EMI_DangerRed", -4.78, -4.18, -3.65, 3.65, 0.86, 0.97, 0.03)
    ov6.add_frustum_pad("Collapse_RedPerimeter_E", "EMI_DangerRed",  4.18,  4.78, -3.65, 3.65, 0.86, 0.97, 0.03)
    L, W = 3.55, 0.34
    ov6.add_extruded_polygon_y("Collapse_RedXBar_Diag1", "EMI_DangerRed", [(-L - W, -L + W), (L - W, L + W), (L + W, L - W), (-L + W, -L - W)], 0.86, 0.96, [(0, 1, 2), (0, 2, 3)])
    ov6.add_extruded_polygon_y("Collapse_RedXBar_Diag2", "EMI_DangerRed", [(-L + W, L + W), (L + W, -L + W), (L - W, -L - W), (-L - W, L - W)], 0.86, 0.96, [(0, 1, 2), (0, 2, 3)])
    ov6.add_frustum_pad("Collapse_Shutter_North", "MAT_DarkNeutral", -1.45, 1.45, -3.85, -1.95, 0.86, 0.985, 0.05)
    ov6.add_frustum_pad("Collapse_Shutter_South", "MAT_DarkNeutral", -1.45, 1.45,  1.95,  3.85, 0.86, 0.985, 0.05)
    ov6.add_frustum_pad("Collapse_Shutter_West",  "MAT_DarkNeutral", -3.85, -1.95, -1.45, 1.45, 0.86, 0.985, 0.05)
    ov6.add_frustum_pad("Collapse_Shutter_East",  "MAT_DarkNeutral",  1.95,  3.85, -1.45, 1.45, 0.86, 0.985, 0.05)
    ov6.add_frustum_pad("Collapse_CenterDangerCore", "EMI_DangerRed", -1.15, 1.15, -1.15, 1.15, 0.86, 0.98, 0.04)
    ov6.add_frustum_pad("Collapse_RimClamp_N", "MAT_LightTrim", -0.80, 0.80, -5.60, -5.20, 0.98, 1.00, 0.02)
    ov6.add_frustum_pad("Collapse_RimClamp_S", "MAT_LightTrim", -0.80, 0.80,  5.20,  5.60, 0.98, 1.00, 0.02)
    ov6.add_frustum_pad("Collapse_RimClamp_W", "MAT_LightTrim", -5.60, -5.20, -0.80, 0.80, 0.98, 1.00, 0.02)
    ov6.add_frustum_pad("Collapse_RimClamp_E", "MAT_LightTrim",  5.20,  5.60, -0.80, 0.80, 0.98, 1.00, 0.02)

    return [
        ("SM_ArenaTile_01_SafeNormal",    ov1),
        ("SM_ArenaTile_02_Warning",       ov2),
        ("SM_ArenaTile_03_IceCorridor",   ov3),
        ("SM_ArenaTile_04_MagneticStorm", ov4),
        ("SM_ArenaTile_05_BoostRunway",   ov5),
        ("SM_ArenaTile_06_RingCollapse",  ov6),
    ]


def create_or_get_blender_material(mat_name):
    if mat_name in bpy.data.materials:
        return bpy.data.materials[mat_name]
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    rgba = PALETTE_RGBA[mat_name]
    mat.diffuse_color = rgba
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        is_emi = mat_name.startswith("EMI_")
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = 0.1 if is_emi else (0.78 if mat_name == "MAT_LightTrim" else 0.58)
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = 0.15 if is_emi else 0.34
        if is_emi:
            for emi_key in ("Emission Color", "Emission"):
                if emi_key in bsdf.inputs:
                    bsdf.inputs[emi_key].default_value = rgba
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = 2.5
    return mat


def build_blender_model_from_collector(collector, offset_x=0.0):
    root_empty = bpy.data.objects.new(collector.name, None)
    root_empty.location = (offset_x, 0.0, 0.0)
    bpy.context.collection.objects.link(root_empty)

    by_mat = {}
    for (_, mat_name), tris in collector.groups.items():
        by_mat.setdefault(mat_name, []).extend(tris)

    for mat_name in sorted(by_mat.keys()):
        tris = by_mat[mat_name]
        verts = []
        faces = []
        for i, (v0, v1, v2) in enumerate(tris):
            verts.extend([v0, v1, v2])
            faces.append((3 * i, 3 * i + 1, 3 * i + 2))

        mesh_data = bpy.data.meshes.new(f"{collector.name}__Mesh_{mat_name}")
        mesh_data.from_pydata(verts, [], faces)
        mesh_data.update()

        mat = create_or_get_blender_material(mat_name)
        mesh_data.materials.append(mat)

        rgba = PALETTE_RGBA[mat_name]
        if hasattr(mesh_data, "color_attributes"):
            col_attr = mesh_data.color_attributes.new(name="COLOR_0", type="BYTE_COLOR", domain="CORNER")
            for loop_i in range(len(col_attr.data)):
                col_attr.data[loop_i].color = rgba

        part_obj = bpy.data.objects.new(f"Part_{mat_name}", mesh_data)
        part_obj.parent = root_empty
        bpy.context.collection.objects.link(part_obj)


def run_blender_generation(output_dir):
    if not HAS_BPY:
        print(
            "Notice: `bpy` not detected in standard Python environment.\n"
            "  - To run inside Blender: `blender --background --python scripts/generate_arena_tiles_blender.py -- --output-dir ./blender_exports`\n"
            "  - To run standalone Python generation without Blender: `python3 scripts/generate_arena_tiles_pipeline.py`"
        )
        return

    os.makedirs(output_dir, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for mname in PALETTE_RGBA:
        create_or_get_blender_material(mname)

    overlays = build_all_overlays()
    for idx, (comp_name, ov_collector) in enumerate(overlays):
        comp = build_shared_base(comp_name)
        comp.merge_from(ov_collector)
        build_blender_model_from_collector(comp, offset_x=idx * 14.0)

    fbx_out = os.path.join(output_dir, "Sphere_Brawl_Arena_Tiles_All6States.fbx")
    glb_out = os.path.join(output_dir, "Sphere_Brawl_Arena_Tiles_All6States.glb")
    if hasattr(bpy.ops.export_scene, "fbx"):
        bpy.ops.export_scene.fbx(filepath=fbx_out, axis_forward="Z", axis_up="Y", apply_unit_scale=True)
    if hasattr(bpy.ops.export_scene, "gltf"):
        bpy.ops.export_scene.gltf(filepath=glb_out, export_format="GLB", export_yup=True)
    print(f"Deterministically generated and exported 6-State Arena Tile collection in Blender to: {output_dir}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(script_dir, "..", "blender_exports"))
    if "--output-dir" in sys.argv:
        idx = sys.argv.index("--output-dir")
        if idx + 1 < len(sys.argv):
            out_dir = os.path.abspath(sys.argv[idx + 1])
    run_blender_generation(out_dir)
