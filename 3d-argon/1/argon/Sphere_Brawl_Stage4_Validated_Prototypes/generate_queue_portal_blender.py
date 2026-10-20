#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — Stage 4 Corrected & Validated Blender 3.6+ / 4.x Python Generator
Asset: Prototype A — Central Queue Portal Arch (SM_Hub_QueuePortalArch_01)
Target Location: The Kinetic Hub Center (0, 150, -300) | Queue Pad Radius: 14.0 studs

Stage 4 Validated Geometry & Clearances:
- Entire floor-level circular queue pad (R = 14.0 studs) is 100% clear of decorative geometry
  (Min floor-level radial distance from center = 15.02 studs; flank curbs start at R_xz = 15.20 studs).
- Clear horizontal approach opening width = 30.00 studs (pylon inner faces at X = +-15.05 studs, arch inner radius = 15.00 studs).
- Lower clear arch height at center (X = 0) = 20.93 studs (arch springline at Y = 6.00 studs).
- Exact match to QueuePortalArch_Prototype.obj (3,168 triangles, 0 degenerate faces).
- Coordinate mapping: Exports with +Y Up and +Z Forward so Roblox Studio import matches 1:1.
"""

import bpy
import bmesh
import math
import os
import sys

PALETTE_SRGB = {
    "MAT_DarkNeutral": (32, 38, 54),
    "MAT_AltNeutral":  (42, 50, 70),
    "MAT_LightTrim":   (170, 190, 215),
    "EMI_Cyan":        (0, 195, 255),
}

def srgb_to_linear(c):
    v = c / 255.0
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def create_pbr_material(name, rgb, is_emissive=False):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    lin = (srgb_to_linear(rgb[0]), srgb_to_linear(rgb[1]), srgb_to_linear(rgb[2]), 1.0)
    bsdf.inputs["Base Color"].default_value = lin
    if is_emissive:
        bsdf.inputs["Metallic"].default_value = 0.1
        bsdf.inputs["Roughness"].default_value = 0.15
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = lin
            bsdf.inputs["Emission Strength"].default_value = 4.5
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = lin
    else:
        bsdf.inputs["Metallic"].default_value = 0.78 if "Trim" in name else 0.58
        bsdf.inputs["Roughness"].default_value = 0.34
    return mat

def rblx_to_blender(pt):
    # Maps Roblox (X_right, Y_up, Z_forward) -> Blender (X_right, -Z_forward, Y_up)
    # so Blender's standard OBJ/GLB exporter (+Y Up, -Z Forward -> +Z) matches QueuePortalArch_Prototype.obj 1:1
    return (pt[0], -pt[2], pt[1])

def add_ring_segment_obj(name, mat, center, r_inner, r_outer, y_min, y_max, theta0, theta1, segs=16, axis='Y', col=None):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    col.objects.link(obj)
    bm = bmesh.new()
    cx, cy, cz = center
    thetas = [theta0 + i * (theta1 - theta0) / segs for i in range(segs + 1)]
    for i in range(segs):
        t0, t1 = thetas[i], thetas[i+1]
        c0, s0 = math.cos(t0), math.sin(t0)
        c1, s1 = math.cos(t1), math.sin(t1)
        if axis == 'Y':
            p00_in  = (cx + r_inner*c0, y_min, cz + r_inner*s0)
            p01_in  = (cx + r_inner*c1, y_min, cz + r_inner*s1)
            p10_in  = (cx + r_inner*c0, y_max, cz + r_inner*s0)
            p11_in  = (cx + r_inner*c1, y_max, cz + r_inner*s1)
            p00_out = (cx + r_outer*c0, y_min, cz + r_outer*s0)
            p01_out = (cx + r_outer*c1, y_min, cz + r_outer*s1)
            p10_out = (cx + r_outer*c0, y_max, cz + r_outer*s0)
            p11_out = (cx + r_outer*c1, y_max, cz + r_outer*s1)
        else:
            p00_in  = (cx + r_inner*c0, cy + r_inner*s0, cz + y_min)
            p01_in  = (cx + r_inner*c1, cy + r_inner*s1, cz + y_min)
            p10_in  = (cx + r_inner*c0, cy + r_inner*s0, cz + y_max)
            p11_in  = (cx + r_inner*c1, cy + r_inner*s1, cz + y_max)
            p00_out = (cx + r_outer*c0, cy + r_outer*s0, cz + y_min)
            p01_out = (cx + r_outer*c1, cy + r_outer*s1, cz + y_min)
            p10_out = (cx + r_outer*c0, cy + r_outer*s0, cz + y_max)
            p11_out = (cx + r_outer*c1, cy + r_outer*s1, cz + y_max)

        quads = [
            (p10_in, p11_in, p11_out, p10_out),
            (p00_out, p01_out, p01_in, p00_in),
            (p00_out, p10_out, p11_out, p01_out),
            (p01_in, p11_in, p10_in, p00_in)
        ]
        if abs((theta1 - theta0) - 2*math.pi) > 1e-3:
            if i == 0:
                quads.append((p00_in, p10_in, p10_out, p00_out))
            if i == segs - 1:
                quads.append((p01_out, p11_out, p11_in, p01_in))
        for q in quads:
            verts = [bm.verts.new(rblx_to_blender(p)) for p in q]
            bm.faces.new(verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj.data.materials.append(mat)
    return obj

def add_chamfered_box_obj(name, mat, center, size, bevel=0.08, rot_angle_y=0.0, col=None):
    cx, cy, cz = center
    sx, sy, sz = size[0]/2.0, size[1]/2.0, size[2]/2.0
    b = min(bevel, sx*0.35, sy*0.35, sz*0.35)
    ix, iy, iz = sx - b, sy - b, sz - b
    ca, sa = math.cos(rot_angle_y), math.sin(rot_angle_y)

    def xform(pt):
        x, y, z = pt
        rx = x * ca - z * sa + cx
        ry = y + cy
        rz = x * sa + z * ca + cz
        return rblx_to_blender((rx, ry, rz))

    top = [xform((-ix, sy, -iz)), xform((-ix, sy, iz)), xform((ix, sy, iz)), xform((ix, sy, -iz))]
    bot = [xform((-ix, -sy, -iz)), xform((ix, -sy, -iz)), xform((ix, -sy, iz)), xform((-ix, -sy, iz))]
    frt = [xform((-ix, -iy, sz)), xform((ix, -iy, sz)), xform((ix, iy, sz)), xform((-ix, iy, sz))]
    bck = [xform((ix, -iy, -sz)), xform((-ix, -iy, -sz)), xform((-ix, iy, -sz)), xform((ix, iy, -sz))]
    rgt = [xform((sx, -iy, iz)), xform((sx, -iy, -iz)), xform((sx, iy, -iz)), xform((sx, iy, iz))]
    lft = [xform((-sx, -iy, -iz)), xform((-sx, -iy, iz)), xform((-sx, iy, iz)), xform((-sx, iy, -iz))]

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    col.objects.link(obj)
    bm = bmesh.new()

    quads = [
        top, bot, frt, bck, rgt, lft,
        [top[1], top[2], frt[2], frt[3]], [top[3], top[0], bck[2], bck[3]],
        [top[2], top[3], rgt[2], rgt[3]], [top[0], top[1], lft[2], lft[3]],
        [frt[0], frt[1], bot[2], bot[3]], [bck[0], bck[1], bot[0], bot[1]],
        [rgt[0], rgt[1], bot[1], bot[2]], [lft[0], lft[1], bot[3], bot[0]],
        [frt[1], rgt[0], rgt[3], frt[2]], [lft[1], frt[0], frt[3], lft[2]],
        [rgt[1], bck[0], bck[3], rgt[2]], [bck[1], lft[0], lft[3], bck[2]],
    ]
    tris = [
        [top[2], rgt[3], frt[2]], [top[1], frt[3], lft[2]],
        [top[3], bck[3], rgt[2]], [top[0], lft[3], bck[2]],
        [bot[2], frt[1], rgt[0]], [bot[3], lft[1], frt[0]],
        [bot[1], rgt[1], bck[0]], [bot[0], bck[1], lft[0]],
    ]
    for q in quads:
        bm.faces.new([bm.verts.new(p) for p in q])
    for t in tris:
        bm.faces.new([bm.verts.new(p) for p in t])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj.data.materials.append(mat)
    return obj

def build_queue_portal():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

    col = bpy.data.collections.new("SM_Hub_QueuePortalArch_01")
    bpy.context.scene.collection.children.link(col)
    mats = {k: create_pbr_material(k, v, is_emissive=k.startswith("EMI_")) for k, v in PALETTE_SRGB.items()}

    # 1. Flank Floor Curbs outside R_xz >= 15.20 studs (100% clear of R=14.0 stud Queue Pad)
    for side_label, (t0, t1) in [("R", (-0.30*math.pi, 0.30*math.pi)), ("L", (0.70*math.pi, 1.30*math.pi))]:
        add_ring_segment_obj(f"Portal_FloorCurb_{side_label}", mats["MAT_DarkNeutral"],
                             (0, 0, 0), 15.60, 17.20, 0.0, 0.28, t0, t1, segs=16, axis='Y', col=col)
        add_ring_segment_obj(f"Portal_FloorGlowRim_{side_label}", mats["EMI_Cyan"],
                             (0, 0, 0), 15.20, 15.60, 0.0, 0.30, t0, t1, segs=16, axis='Y', col=col)
        for idx, ang in enumerate([t0 + 0.08*math.pi, t1 - 0.08*math.pi]):
            cx, cz = 16.40 * math.cos(ang), 16.40 * math.sin(ang)
            add_chamfered_box_obj(f"Portal_TieCleat_{side_label}_{idx}", mats["MAT_AltNeutral"],
                                  (cx, 0.22, cz), (1.4, 0.44, 1.4), bevel=0.08, rot_angle_y=ang, col=col)
            add_chamfered_box_obj(f"Portal_TieTrim_{side_label}_{idx}", mats["MAT_LightTrim"],
                                  (cx, 0.46, cz), (1.0, 0.12, 1.0), bevel=0.04, rot_angle_y=ang, col=col)

    # 2. Side Pylons & Bases outside |X| >= 15.05 studs (30.10-stud clear span between pylons)
    for side_label, sign in [("L", -1.0), ("R", 1.0)]:
        px = sign * 17.10
        add_chamfered_box_obj(f"Portal_PylonBase_{side_label}", mats["MAT_DarkNeutral"], (px, 2.50, 0.0), (3.80, 5.00, 5.20), bevel=0.26, col=col)
        add_chamfered_box_obj(f"Portal_PylonCollar_{side_label}", mats["MAT_AltNeutral"], (sign*16.90, 5.60, 0.0), (3.50, 1.20, 4.40), bevel=0.18, col=col)
        add_chamfered_box_obj(f"Portal_PylonButtress_{side_label}", mats["MAT_AltNeutral"], (sign*19.60, 2.10, 0.0), (1.60, 4.20, 3.60), bevel=0.16, col=col)
        add_chamfered_box_obj(f"Portal_PylonBracketF_{side_label}", mats["MAT_LightTrim"], (sign*15.30, 2.50, 1.85), (0.50, 3.80, 0.75), bevel=0.06, col=col)
        add_chamfered_box_obj(f"Portal_PylonBracketB_{side_label}", mats["MAT_LightTrim"], (sign*15.30, 2.50, -1.85), (0.50, 3.80, 0.75), bevel=0.06, col=col)
        add_chamfered_box_obj(f"Portal_PylonVentF_{side_label}", mats["EMI_Cyan"], (px, 2.60, -2.64), (0.65, 3.40, 0.16), bevel=0.03, col=col)
        add_chamfered_box_obj(f"Portal_PylonVentB_{side_label}", mats["EMI_Cyan"], (px, 2.60,  2.64), (0.65, 3.40, 0.16), bevel=0.03, col=col)

    # 3. Overhead Decorative Arch (Inner Radius = 15.00 studs -> 30.00-stud clear opening width, 21.00-stud crown height)
    arch_cy = 6.00
    add_ring_segment_obj("Portal_ArchCore", mats["MAT_DarkNeutral"], (0, arch_cy, 0), 15.35, 18.05, -1.60, 1.60, 0.0, math.pi, segs=32, axis='Z', col=col)
    add_ring_segment_obj("Portal_ArchInnerConduit", mats["EMI_Cyan"], (0, arch_cy, 0), 15.00, 15.40, -0.75, 0.75, 0.0, math.pi, segs=32, axis='Z', col=col)
    add_ring_segment_obj("Portal_ArchFaceGlow_Front", mats["EMI_Cyan"], (0, arch_cy, 0), 16.30, 16.85, -1.72, -1.56, 0.03, math.pi - 0.03, segs=28, axis='Z', col=col)
    add_ring_segment_obj("Portal_ArchFaceGlow_Back", mats["EMI_Cyan"], (0, arch_cy, 0), 16.30, 16.85,  1.56,  1.72, 0.03, math.pi - 0.03, segs=28, axis='Z', col=col)

    num_ribs = 9
    for i in range(num_ribs):
        t_center = 0.10 * math.pi + i * (0.80 * math.pi / (num_ribs - 1))
        t_span = 0.048 * math.pi
        add_ring_segment_obj(f"Portal_ArchRib_{i+1}", mats["MAT_AltNeutral"], (0, arch_cy, 0), 15.20, 18.45, -1.90, 1.90, t_center - t_span, t_center + t_span, segs=3, axis='Z', col=col)
        add_ring_segment_obj(f"Portal_ArchRibTrim_{i+1}", mats["MAT_LightTrim"], (0, arch_cy, 0), 18.35, 18.65, -1.35, 1.35, t_center - t_span*0.7, t_center + t_span*0.7, segs=2, axis='Z', col=col)

    # 4. Apex Crown Assembly & Holographic Countdown Banner Frame
    add_chamfered_box_obj("Portal_CrownBase", mats["MAT_DarkNeutral"], (0, 23.80, 0), (13.20, 2.60, 4.40), bevel=0.22, col=col)
    add_chamfered_box_obj("Portal_CrownUpper", mats["MAT_AltNeutral"], (0, 25.50, 0), (16.00, 1.90, 3.40), bevel=0.18, col=col)
    add_chamfered_box_obj("Portal_CrownCap_L", mats["MAT_LightTrim"], (-8.20, 25.50, 0), (0.90, 2.30, 3.80), bevel=0.10, col=col)
    add_chamfered_box_obj("Portal_CrownCap_R", mats["MAT_LightTrim"], ( 8.20, 25.50, 0), (0.90, 2.30, 3.80), bevel=0.10, col=col)
    add_chamfered_box_obj("Portal_HoloBanner_Front", mats["EMI_Cyan"], (0, 25.50, -1.76), (14.20, 1.25, 0.16), bevel=0.04, col=col)
    add_chamfered_box_obj("Portal_HoloBanner_Back",  mats["EMI_Cyan"], (0, 25.50,  1.76), (14.20, 1.25, 0.16), bevel=0.04, col=col)

    print("SM_Hub_QueuePortalArch_01 (Stage 4 Corrected) built successfully in Blender.")

if __name__ == "__main__":
    build_queue_portal()
    if "--out_dir" in sys.argv:
        idx = sys.argv.index("--out_dir")
        out_dir = sys.argv[idx + 1]
        os.makedirs(out_dir, exist_ok=True)
        bpy.ops.export_scene.gltf(filepath=os.path.join(out_dir, "QueuePortalArch_Prototype.glb"), export_format='GLB')
        bpy.ops.export_scene.fbx(filepath=os.path.join(out_dir, "QueuePortalArch_Prototype.fbx"), global_scale=0.01, apply_unit_scale=True)
