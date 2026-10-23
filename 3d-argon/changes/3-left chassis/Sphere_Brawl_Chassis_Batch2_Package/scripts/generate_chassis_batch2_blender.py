#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — STANDALONE DETERMINISTIC BLENDER 3.x / 4.x CHASSIS BATCH 2 GENERATOR
=====================================================================================================
Deterministically generates the three Batch 2 cosmetic sphere chassis models inside Blender (`bpy`):
  1. SM_Chassis_Trickster_01  (236 triangles, Max Radius <= 2.945 studs < 2.970 limit)
  2. SM_Chassis_Magnetar_01   (232 triangles, Max Radius <= 2.955 studs < 2.970 limit)
  3. SM_Chassis_Bulwark_01    (232 triangles, Max Radius <= 2.962 studs < 2.970 limit)

Key Features for Roblox Studio Material Compatibility:
  - Creates a parent Empty (`SM_Chassis_Trickster_01`, etc.) at `(0,0,0)` with separate child Mesh
    objects per material slot (`Part_MAT_DarkNeutral`, `Part_MAT_AltNeutral`, `Part_MAT_LightTrim`,
    `Part_EMI_*`) so Roblox Studio's 3D Importer creates distinct selectable `MeshPart` children.
  - Assigns Principled BSDF `Base Color`, `Metallic`, `Roughness`, and `Emission Color` matching
    the approved Sphere Brawl RGB palette.
  - Bakes per-vertex color attributes (`COLOR_0`) onto every mesh so colors survive `.fbx` and `.glb` export.

Usage (Headless Blender CLI):
  blender --background --python scripts/generate_chassis_batch2_blender.py -- --output-dir ./blender_exports
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
    "EMI_Magnetic":    (165, 55, 255),
    "EMI_Kinetic":     (255, 125, 0),
}

PALETTE_RGBA = {
    k: (v[0] / 255.0, v[1] / 255.0, v[2] / 255.0, 1.0)
    for k, v in PALETTE_SRGB.items()
}


def sph_pt(r, phi, theta):
    cp = math.cos(phi)
    return (
        r * cp * math.sin(theta),
        r * math.sin(phi),
        r * cp * math.cos(theta),
    )


class DeterministicChassisCollector:
    """Pure-Python deterministic geometry collector matching `generate_chassis_batch2_pipeline.py` 1:1."""

    def __init__(self, name, max_radius_clamp=2.965):
        self.name = name
        self.max_radius_clamp = max_radius_clamp
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

    def _clamp(self, v):
        x, y, z = float(v[0]), float(v[1]), float(v[2])
        r = math.sqrt(x * x + y * y + z * z)
        if r > self.max_radius_clamp:
            s = self.max_radius_clamp / r
            x, y, z = x * s, y * s, z * s
        return (round(x, 5), round(y, 5), round(z, 5))

    def add_tri(self, group_name, mat_name, v0, v1, v2, expected_normal=None):
        p0, p1, p2 = self._clamp(v0), self._clamp(v1), self._clamp(v2)
        cr = self._cross(self._sub(p1, p0), self._sub(p2, p0))
        ref = expected_normal if expected_normal is not None else ((p0[0]+p1[0]+p2[0])/3.0, (p0[1]+p1[1]+p2[1])/3.0, (p0[2]+p1[2]+p2[2])/3.0)
        if self._dot(cr, ref) < 0.0:
            p1, p2 = p2, p1
        self.groups.setdefault((group_name, mat_name), []).append((p0, p1, p2))

    def add_quad(self, group_name, mat_name, v0, v1, v2, v3, expected_normal=None):
        self.add_tri(group_name, mat_name, v0, v1, v2, expected_normal)
        self.add_tri(group_name, mat_name, v0, v2, v3, expected_normal)

    def add_segmented_core_sphere(self, r_base, phis, n_segs, band_mat_fn, theta_twist_per_ring=None):
        n_rings = len(phis) - 1
        if theta_twist_per_ring is None:
            theta_twist_per_ring = [0.0] * (n_rings + 1)
        south_pole = (0.0, -r_base, 0.0)
        north_pole = (0.0,  r_base, 0.0)

        for i in range(n_rings):
            p0, p1 = phis[i], phis[i + 1]
            p_mid = 0.5 * (p0 + p1)
            tw0, tw1 = theta_twist_per_ring[i], theta_twist_per_ring[i + 1]
            for j in range(n_segs):
                t0_base = -math.pi + (2.0 * math.pi * j) / n_segs
                t1_base = -math.pi + (2.0 * math.pi * (j + 1)) / n_segs
                t_mid = 0.5 * (t0_base + t1_base)
                g_name, m_name = band_mat_fn(i, j, p_mid, t_mid)
                out_dir = sph_pt(1.0, p_mid, t_mid)
                if i == 0:
                    v1 = sph_pt(r_base, p1, t0_base + tw1)
                    v2 = sph_pt(r_base, p1, t1_base + tw1)
                    self.add_tri(g_name, m_name, south_pole, v2, v1, out_dir)
                elif i == n_rings - 1:
                    v0 = sph_pt(r_base, p0, t0_base + tw0)
                    v1 = sph_pt(r_base, p0, t1_base + tw0)
                    self.add_tri(g_name, m_name, v0, v1, north_pole, out_dir)
                else:
                    v00 = sph_pt(r_base, p0, t0_base + tw0)
                    v10 = sph_pt(r_base, p0, t1_base + tw0)
                    v11 = sph_pt(r_base, p1, t1_base + tw1)
                    v01 = sph_pt(r_base, p1, t0_base + tw1)
                    self.add_quad(g_name, m_name, v00, v10, v11, v01, out_dir)

    def add_spherical_frustum_plate(self, group_name, mat_name, r_base, r_top,
                                    phi0, phi1, theta0, theta1,
                                    inset_phi=0.04, inset_theta=0.05):
        ip0, ip1 = phi0 + inset_phi, phi1 - inset_phi
        it0, it1 = theta0 + inset_theta, theta1 - inset_theta
        b00, b10 = sph_pt(r_base, phi0, theta0), sph_pt(r_base, phi0, theta1)
        b11, b01 = sph_pt(r_base, phi1, theta1), sph_pt(r_base, phi1, theta0)
        t00, t10 = sph_pt(r_top, ip0, it0), sph_pt(r_top, ip0, it1)
        t11, t01 = sph_pt(r_top, ip1, it1), sph_pt(r_top, ip1, it0)
        p_mid, t_mid = 0.5 * (phi0 + phi1), 0.5 * (theta0 + theta1)
        self.add_quad(group_name, mat_name, t00, t10, t11, t01, sph_pt(1.0, p_mid, t_mid))
        self.add_quad(group_name, mat_name, b00, b10, t10, t00, sph_pt(1.0, phi0 - 0.35, t_mid))
        self.add_quad(group_name, mat_name, b11, b01, t01, t11, sph_pt(1.0, phi1 + 0.35, t_mid))
        self.add_quad(group_name, mat_name, b01, b00, t00, t01, sph_pt(1.0, p_mid, theta0 - 0.45))
        self.add_quad(group_name, mat_name, b10, b11, t11, t10, sph_pt(1.0, p_mid, theta1 + 0.45))

    def add_skewed_spherical_blade(self, group_name, mat_name, r_base, r_top,
                                   base_phi_theta_quad, top_phi_theta_quad):
        b_pts = [sph_pt(r_base, p, t) for (p, t) in base_phi_theta_quad]
        t_pts = [sph_pt(r_top, p, t) for (p, t) in top_phi_theta_quad]
        top_centroid = (
            sum(p[0] for p in t_pts) / 4.0,
            sum(p[1] for p in t_pts) / 4.0,
            sum(p[2] for p in t_pts) / 4.0,
        )
        self.add_quad(group_name, mat_name, t_pts[0], t_pts[1], t_pts[2], t_pts[3], top_centroid)
        plate_mid = (
            sum(p[0] for p in b_pts) / 4.0,
            sum(p[1] for p in b_pts) / 4.0,
            sum(p[2] for p in b_pts) / 4.0,
        )
        for i in range(4):
            ni = (i + 1) % 4
            b_a, b_b = b_pts[i], b_pts[ni]
            t_b, t_a = t_pts[ni], t_pts[i]
            face_mid = (
                0.25 * (b_a[0] + b_b[0] + t_b[0] + t_a[0]),
                0.25 * (b_a[1] + b_b[1] + t_b[1] + t_a[1]),
                0.25 * (b_a[2] + b_b[2] + t_b[2] + t_a[2]),
            )
            out_vec = (
                (face_mid[0] - plate_mid[0]) + 0.35 * face_mid[0],
                (face_mid[1] - plate_mid[1]) + 0.35 * face_mid[1],
                (face_mid[2] - plate_mid[2]) + 0.35 * face_mid[2],
            )
            self.add_quad(group_name, mat_name, b_a, b_b, t_b, t_a, out_vec)

    def add_equatorial_band_segment(self, group_name, mat_name, r_base, r_top,
                                    phi0, phi1, theta0, theta1, inset_phi=0.02, cap_ends=False):
        ip0, ip1 = phi0 + inset_phi, phi1 - inset_phi
        b00, b10 = sph_pt(r_base, phi0, theta0), sph_pt(r_base, phi0, theta1)
        b11, b01 = sph_pt(r_base, phi1, theta1), sph_pt(r_base, phi1, theta0)
        t00, t10 = sph_pt(r_top, ip0, theta0), sph_pt(r_top, ip0, theta1)
        t11, t01 = sph_pt(r_top, ip1, theta1), sph_pt(r_top, ip1, theta0)
        p_mid, t_mid = 0.5 * (phi0 + phi1), 0.5 * (theta0 + theta1)
        self.add_quad(group_name, mat_name, t00, t10, t11, t01, sph_pt(1.0, p_mid, t_mid))
        self.add_quad(group_name, mat_name, b00, b10, t10, t00, sph_pt(1.0, phi0 - 0.3, t_mid))
        self.add_quad(group_name, mat_name, b11, b01, t01, t11, sph_pt(1.0, phi1 + 0.3, t_mid))
        if cap_ends:
            self.add_quad(group_name, mat_name, b01, b00, t00, t01, sph_pt(1.0, p_mid, theta0 - 0.3))
            self.add_quad(group_name, mat_name, b10, b11, t11, t10, sph_pt(1.0, p_mid, theta1 + 0.3))


def build_all_batch2_collectors():
    # 1. Trickster (236 tris)
    c1 = DeterministicChassisCollector("SM_Chassis_Trickster_01")
    phis1 = [-math.pi / 2.0, -0.88, -0.26, 0.26, 0.88, math.pi / 2.0]
    twists1 = [-0.28, -0.16, -0.05, 0.05, 0.16, 0.28]
    def trickster_core_mat(i, j, p_mid, t_mid):
        if i in (0, 4):
            return ("Trickster_CorePolarCap", "MAT_DarkNeutral")
        dm = (j + i) % 5
        if dm == 0:
            return (f"Trickster_CoreSlashChannel_R{i}_S{j}", "EMI_Cyan")
        elif dm in (1, 3):
            return (f"Trickster_CoreSleekShell_R{i}_S{j}", "MAT_AltNeutral")
        return (f"Trickster_CoreBaseHull_R{i}_S{j}", "MAT_DarkNeutral")
    c1.add_segmented_core_sphere(2.66, phis1, 10, trickster_core_mat, twists1)
    for sname, b_quad, t_quad, mname, r_top in [
        ("FrontRight", [(-0.42, 0.18), (-0.18, 0.82), (0.04, 0.72), (-0.20, 0.08)], [(-0.36, 0.24), (-0.14, 0.76), (0.00, 0.68), (-0.22, 0.14)], "MAT_LightTrim", 2.91),
        ("CenterSlash",[(-0.12, -0.45), (0.28, 0.15), (0.46, 0.02), (0.06, -0.58)], [(-0.08, -0.40), (0.24, 0.10), (0.40, -0.02), (0.08, -0.52)], "EMI_Cyan", 2.89),
        ("UpperLeft",  [(0.18, -1.18), (0.55, -0.52), (0.72, -0.66), (0.35, -1.32)], [(0.22, -1.12), (0.50, -0.58), (0.65, -0.70), (0.36, -1.25)], "MAT_LightTrim", 2.91),
    ]:
        c1.add_skewed_spherical_blade(f"Trickster_AsymSash_{sname}", mname, 2.64, r_top, b_quad, t_quad)
    for fname, mname, p0, p1, t0, t1, r_top in [
        ("FrontRight_Upper", "MAT_AltNeutral", 0.08, 0.58,  0.32,  1.12, 2.88),
        ("FrontLeft_Lower",  "MAT_DarkNeutral", -0.58, -0.08, -1.12, -0.32, 2.88),
        ("RearRight_Lower",  "MAT_DarkNeutral", -0.52, -0.04,  1.62,  2.48, 2.87),
        ("RearLeft_Upper",   "MAT_AltNeutral",  0.04,  0.52, -2.48, -1.62, 2.87),
    ]:
        c1.add_spherical_frustum_plate(f"Trickster_Fairing_{fname}", mname, 2.64, r_top, p0, p1, t0, t1, 0.05, 0.07)
    c1.add_skewed_spherical_blade("Trickster_SweptWing_Right", "MAT_LightTrim", 2.64, 2.945, [(-0.22, 1.18), (-0.02, 1.92), (0.20, 1.84), (0.00, 1.10)], [(-0.17, 1.25), (-0.01, 1.85), (0.15, 1.78), (0.01, 1.18)])
    c1.add_skewed_spherical_blade("Trickster_SweptWing_Left", "MAT_LightTrim", 2.64, 2.945, [(-0.02, -1.92), (-0.22, -1.18), (0.00, -1.10), (0.20, -1.84)], [(-0.01, -1.85), (-0.17, -1.25), (0.01, -1.18), (0.15, -1.78)])
    c1.add_spherical_frustum_plate("Trickster_FrontSensorVisor", "EMI_Cyan", 2.64, 2.90, -0.16, 0.24, -0.28, 0.22, 0.04, 0.04)
    c1.add_spherical_frustum_plate("Trickster_DorsalSpeedFin", "MAT_LightTrim", 2.64, 2.93, 0.42, 0.84, -0.22, 0.34, 0.05, 0.06)
    c1.add_spherical_frustum_plate("Trickster_VentralSkidFin", "MAT_LightTrim", 2.64, 2.92, -0.84, -0.42, -0.34, 0.22, 0.05, 0.06)
    c1.add_spherical_frustum_plate("Trickster_KineticVent_Right", "EMI_Kinetic", 2.64, 2.91, 0.14, 0.42, 1.18, 1.68, 0.03, 0.05)
    c1.add_spherical_frustum_plate("Trickster_KineticVent_Left",  "EMI_Kinetic", 2.64, 2.91, -0.42, -0.14, -1.68, -1.18, 0.03, 0.05)
    c1.add_equatorial_band_segment("Trickster_RearThrusterCollar", "MAT_LightTrim", 2.64, 2.91, -0.24, 0.24, 2.76, 3.52, 0.03, False)
    c1.add_spherical_frustum_plate("Trickster_RearKineticNozzle", "EMI_Kinetic", 2.64, 2.93, -0.20, 0.20, 2.86, 3.42, 0.04, 0.05)

    # 2. Magnetar (232 tris)
    c2 = DeterministicChassisCollector("SM_Chassis_Magnetar_01")
    phis2 = [-math.pi / 2.0, -0.92, -0.30, 0.30, 0.92, math.pi / 2.0]
    def magnetar_core_mat(i, j, p_mid, t_mid):
        if i in (0, 4):
            return (f"Magnetar_PolarCoreCap_R{i}", "EMI_Magnetic")
        elif i == 2:
            return (f"Magnetar_EquatorialChannel_S{j}", "MAT_DarkNeutral")
        return (f"Magnetar_CoilHousing_R{i}_S{j}", "MAT_AltNeutral")
    c2.add_segmented_core_sphere(2.64, phis2, 8, magnetar_core_mat)
    for j in range(8):
        t0, t1 = -math.pi + (2.0 * math.pi * j) / 8, -math.pi + (2.0 * math.pi * (j + 1)) / 8
        c2.add_equatorial_band_segment(f"Magnetar_EquatorialFluxRing_Seg{j+1}", "EMI_Magnetic", 2.62, 2.935, -0.17, 0.17, t0, t1, 0.03, False)
    for pname, tc in [("Front_PosZ", 0.0), ("Right_PosX", 0.5 * math.pi), ("Rear_NegZ", math.pi), ("Left_NegX", -0.5 * math.pi)]:
        c2.add_spherical_frustum_plate(f"Magnetar_InductorShoe_{pname}", "MAT_LightTrim", 2.62, 2.948, -0.52, 0.52, tc - 0.20, tc + 0.20, 0.05, 0.03)
    for iname, tc in [("FrontRight", 0.25 * math.pi), ("FrontLeft", -0.25 * math.pi), ("RearRight", 0.75 * math.pi), ("RearLeft", -0.75 * math.pi)]:
        c2.add_spherical_frustum_plate(f"Magnetar_StabilizerPad_{iname}", "MAT_DarkNeutral", 2.62, 2.86, -0.68, 0.68, tc - 0.22, tc + 0.22, 0.05, 0.04)
    c2.add_spherical_frustum_plate("Magnetar_CyanNode_FrontPosZ", "EMI_Cyan", 2.62, 2.955, -0.14, 0.14, -0.12, 0.12, 0.02, 0.02)
    c2.add_spherical_frustum_plate("Magnetar_CyanNode_RightPosX", "EMI_Cyan", 2.62, 2.955, -0.14, 0.14, 0.5*math.pi - 0.12, 0.5*math.pi + 0.12, 0.02, 0.02)
    c2.add_spherical_frustum_plate("Magnetar_CyanNode_LeftNegX",  "EMI_Cyan", 2.62, 2.955, -0.14, 0.14, -0.5*math.pi - 0.12, -0.5*math.pi + 0.12, 0.02, 0.02)
    c2.add_spherical_frustum_plate("Magnetar_RearFluxThruster_NegZ", "EMI_Magnetic", 2.62, 2.955, -0.22, 0.22, math.pi - 0.18, math.pi + 0.18, 0.03, 0.03)

    # 3. Bulwark (232 tris)
    c3 = DeterministicChassisCollector("SM_Chassis_Bulwark_01")
    phis3 = [-math.pi / 2.0, -0.90, -0.32, 0.32, 0.90, math.pi / 2.0]
    def bulwark_core_mat(i, j, p_mid, t_mid):
        if i in (0, 4):
            return (f"Bulwark_UnderFramePolar_R{i}", "MAT_LightTrim")
        return (f"Bulwark_UnderFrameRecess_R{i}_S{j}", "MAT_AltNeutral")
    c3.add_segmented_core_sphere(2.62, phis3, 8, bulwark_core_mat)
    for j in range(8):
        tc = -math.pi + (2.0 * math.pi * j) / 8
        c3.add_spherical_frustum_plate(f"Bulwark_EquatorialBastionPlate_{j+1}", "MAT_DarkNeutral", 2.60, 2.955, -0.34, 0.34, tc - 0.31, tc + 0.31, 0.04, 0.04)
    for idx, tc in enumerate([-0.75 * math.pi, -0.25 * math.pi, 0.25 * math.pi, 0.75 * math.pi]):
        c3.add_spherical_frustum_plate(f"Bulwark_UpperCasematePlate_{idx+1}", "MAT_DarkNeutral", 2.60, 2.945, 0.38, 0.88, tc - 0.58, tc + 0.58, 0.05, 0.06)
        c3.add_spherical_frustum_plate(f"Bulwark_LowerCasematePlate_{idx+1}", "MAT_DarkNeutral", 2.60, 2.945, -0.88, -0.38, tc - 0.58, tc + 0.58, 0.05, 0.06)
    c3.add_equatorial_band_segment("Bulwark_FrontTacticalVisorSlit", "EMI_Cyan", 2.60, 2.962, -0.09, 0.09, -0.24, 0.24, 0.015, False)
    v_brow0, v_brow1 = sph_pt(2.958, 0.12, -0.24), sph_pt(2.958, 0.12, 0.24)
    v_brow2, v_brow3 = sph_pt(2.958, 0.30, 0.20), sph_pt(2.958, 0.30, -0.20)
    c3.add_quad("Bulwark_FrontBrowReinforcement", "MAT_LightTrim", v_brow0, v_brow1, v_brow2, v_brow3, sph_pt(1.0, 0.21, 0.0))

    return [c1, c2, c3]


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
            "  - To run inside Blender: `blender --background --python scripts/generate_chassis_batch2_blender.py -- --output-dir ./blender_exports`\n"
            "  - To run standalone Python generation without Blender: `python3 scripts/generate_chassis_batch2_pipeline.py`"
        )
        return

    os.makedirs(output_dir, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for mname in PALETTE_RGBA:
        create_or_get_blender_material(mname)

    for idx, collector in enumerate(build_all_batch2_collectors()):
        build_blender_model_from_collector(collector, offset_x=idx * 8.0)

    fbx_out = os.path.join(output_dir, "Sphere_Brawl_Chassis_Batch2_All3.fbx")
    glb_out = os.path.join(output_dir, "Sphere_Brawl_Chassis_Batch2_All3.glb")
    if hasattr(bpy.ops.export_scene, "fbx"):
        bpy.ops.export_scene.fbx(filepath=fbx_out, axis_forward="Z", axis_up="Y", apply_unit_scale=True)
    if hasattr(bpy.ops.export_scene, "gltf"):
        bpy.ops.export_scene.gltf(filepath=glb_out, export_format="GLB", export_yup=True)
    print(f"Deterministically generated and exported Batch 2 Chassis collection in Blender to: {output_dir}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(script_dir, "..", "blender_exports"))
    if "--output-dir" in sys.argv:
        idx = sys.argv.index("--output-dir")
        if idx + 1 < len(sys.argv):
            out_dir = os.path.abspath(sys.argv[idx + 1])
    run_blender_generation(out_dir)
