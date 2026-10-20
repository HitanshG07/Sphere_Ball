#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — Deterministic Blender 3.6+ / 4.x Python Asset Generator
Asset: Prototype 1 — Central Queue Portal Arch (SM_Hub_QueuePortalArch_01)
Target Location: The Kinetic Hub Center (0, 150, -300) | Queue Pad Radius: 14.0 studs

Usage (Headless CLI or Blender Scripting Tab):
    blender --background --python generate_queue_portal_blender.py -- --out_dir ./exports

Unit Convention:
    1 Blender Meter (1.0 unit) = 1 Roblox Stud (export with FBX Scale = 0.01 or GLB 1:1)
Collision Rule:
    This arch is a visual-only decorative frame (CanCollide = false, CanTouch = false, CanQuery = false).
    The central 28-stud diameter floor pad remains 100% open and unobstructed for sphere entry.
"""

import bpy
import bmesh
import math
import os
import sys

# Locked Palette Constants from specs/DESIGN_CONSTANTS.md (sRGB -> Linear conversion handled via helper)
PALETTE_SRGB = {
    "MAT_DarkNeutral": (32, 38, 54),
    "MAT_AltNeutral":  (42, 50, 70),
    "MAT_LightTrim":   (170, 190, 215),
    "EMI_Cyan":        (0, 195, 255),
    "EMI_Amber":       (255, 170, 0),
}

def srgb_to_linear(c):
    v = c / 255.0
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def create_pbr_material(name, rgb, is_emissive=False, emission_strength=4.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    lin = (srgb_to_linear(rgb[0]), srgb_to_linear(rgb[1]), srgb_to_linear(rgb[2]), 1.0)
    bsdf.inputs["Base Color"].default_value = lin
    if is_emissive:
        bsdf.inputs["Metallic"].default_value = 0.0
        bsdf.inputs["Roughness"].default_value = 0.15
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = lin
            bsdf.inputs["Emission Strength"].default_value = emission_strength
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = lin
    else:
        bsdf.inputs["Metallic"].default_value = 0.75 if "Trim" in name else 0.55
        bsdf.inputs["Roughness"].default_value = 0.35
    return mat

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def add_beveled_box(name, location, dimensions, bevel_width, mat, collection):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (dimensions[0], dimensions[2], dimensions[1]) # Blender Z-up mapped from Roblox Y-up
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bev = obj.modifiers.new(name="HardSurfaceBevel", type='BEVEL')
    bev.width = bevel_width
    bev.segments = 2
    bev.limit_method = 'ANGLE'
    bpy.ops.object.modifier_apply(modifier=bev.name)

    obj.data.materials.append(mat)
    for col in obj.users_collection:
        col.objects.unlink(obj)
    collection.objects.link(obj)
    return obj

def build_queue_portal():
    clear_scene()
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

    col = bpy.data.collections.new("SM_Hub_QueuePortalArch_01")
    bpy.context.scene.collection.children.link(col)

    mats = {
        k: create_pbr_material(k, v, is_emissive=k.startswith("EMI_"))
        for k, v in PALETTE_SRGB.items()
    }

    # 1. Floor Perimeter Ring (framing the R=14.0 stud Queue Pad without blocking drive-in)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=15.2, depth=0.45, location=(0, 0, 0.0))
    outer_ring = bpy.context.active_object
    outer_ring.name = "Portal_PadOuterCurb"

    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=13.6, depth=0.8, location=(0, 0, 0.0))
    cutter = bpy.context.active_object
    bool_mod = outer_ring.modifiers.new(name="InnerCut", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter
    bpy.context.view_layer.objects.active = outer_ring
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    outer_ring.data.materials.append(mats["MAT_DarkNeutral"])

    # 2. Left & Right Pylon Pedestals (at X = -14.2 and +14.2 studs)
    for side, sx in [("L", -14.2), ("R", 14.2)]:
        add_beveled_box(f"Portal_PylonBase_{side}", (sx, 0.0, 2.2), (3.4, 4.4, 5.2), 0.22, mats["MAT_DarkNeutral"], col)
        add_beveled_box(f"Portal_PylonCollar_{side}", (sx, 0.0, 4.6), (3.0, 1.2, 4.4), 0.15, mats["MAT_AltNeutral"], col)
        add_beveled_box(f"Portal_PylonEmitterFront_{side}", (sx, 2.62, 2.3), (0.55, 3.0, 0.15), 0.03, mats["EMI_Cyan"], col)
        add_beveled_box(f"Portal_PylonEmitterBack_{side}", (sx, -2.62, 2.3), (0.55, 3.0, 0.15), 0.03, mats["EMI_Cyan"], col)

    # 3. Overhead Circular Arch Torus Segment (Clear Inner Span = 24.7 studs)
    bpy.ops.mesh.primitive_torus_add(
        align='WORLD',
        location=(0, 0, 4.5),
        rotation=(math.pi / 2.0, 0, 0),
        major_radius=14.0,
        minor_radius=1.45,
        major_segments=48,
        minor_segments=12
    )
    arch = bpy.context.active_object
    arch.name = "Portal_OverheadArch"
    # Slice lower half below Z = 0
    bpy.ops.mesh.primitive_cube_add(size=40.0, location=(0, 0, -20.0))
    lower_cut = bpy.context.active_object
    bmod = arch.modifiers.new(name="FloorTrim", type='BOOLEAN')
    bmod.operation = 'DIFFERENCE'
    bmod.object = lower_cut
    bpy.context.view_layer.objects.active = arch
    bpy.ops.object.modifier_apply(modifier=bmod.name)
    bpy.data.objects.remove(lower_cut, do_unlink=True)
    arch.data.materials.append(mats["MAT_AltNeutral"])

    # 4. Top Holographic Header Frame
    add_beveled_box("Portal_HeaderCrown", (0, 0, 19.8), (11.6, 2.6, 4.2), 0.20, mats["MAT_DarkNeutral"], col)
    add_beveled_box("Portal_HoloSign_Front", (0, -1.65, 21.4), (12.8, 1.15, 0.16), 0.04, mats["EMI_Cyan"], col)
    add_beveled_box("Portal_HoloSign_Back", (0, 1.65, 21.4), (12.8, 1.15, 0.16), 0.04, mats["EMI_Cyan"], col)

    print("SM_Hub_QueuePortalArch_01 built successfully in Blender.")

if __name__ == "__main__":
    build_queue_portal()
    if "--out_dir" in sys.argv:
        idx = sys.argv.index("--out_dir")
        out_dir = sys.argv[idx + 1]
        os.makedirs(out_dir, exist_ok=True)
        bpy.ops.export_scene.gltf(
            filepath=os.path.join(out_dir, "SM_Hub_QueuePortalArch_01.glb"),
            export_format='GLB'
        )
        bpy.ops.export_scene.fbx(
            filepath=os.path.join(out_dir, "SM_Hub_QueuePortalArch_01.fbx"),
            global_scale=0.01,
            apply_unit_scale=True
        )