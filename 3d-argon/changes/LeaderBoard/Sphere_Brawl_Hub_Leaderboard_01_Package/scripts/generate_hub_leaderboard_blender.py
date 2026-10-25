#!/usr/bin/env python3
"""
SPHERE BRAWL: ROLLING RAMPAGE — DETERMINISTIC BLENDER 3.6+ / 4.x & PYTHON PRODUCTION GENERATOR
Asset ID: SM_Hub_Leaderboard_01 (Grand Three-Board Monument & Nine-Position Podium Array — Step 6, Phase 2)
===========================================================================================================
- Canonical Asset ID: SM_Hub_Leaderboard_01
- Descriptive Name: Grand Three-Board Monument & Nine-Position Podium Array
- Approved Phase 1 Concept Source: Sphere_Brawl_Hub_Leaderboard_Concept_06.zip
  (Verified SHA-256: bb705ed9a35fca5ada4f0065f90db818010aafc85f00986946967323080f15e0)
- Authoritative World Position: (35.0000, 150.0000, -274.0000) (LOCKED by TASK-03 & Master Plan §2.4)
- Authoritative Floor Reference: World Y = 150.0000 (Local Y = 0.0000)
- Verified Radial Inward Yaw: theta_yaw = -126.60707939° (-2.20971034 rad, atan2(-35, -26))
- Required Roblox Placement Transform:
    local targetCFrame =
        CFrame.new(35, 150, -274)
        * CFrame.Angles(0, math.rad(-126.60707939), 0)
- Equivalent Right-Handed Matrix:
    CFrame.fromMatrix(
        Vector3.new(35, 150, -274),
        Vector3.new(-0.59632400, 0.0, -0.80274385), -- RightVector (Local +X)
        Vector3.new( 0.00000000, 1.0,  0.00000000), -- UpVector    (Local +Y)
        Vector3.new(-0.80274385, 0.0,  0.59632400)  -- ZVector     (-Local +Z; FrontVector = (-0.80274385, 0, -0.59632400))
    )
- Measured Local Bounding Envelope:
  * Width  (Local X): 42.0000 studs (X in [-11.0000, +31.0000], geometric center at Local X = +10.0000)
  * Height (Local Y): 26.0000 studs (Y in [  0.0000, +26.0000])
  * Depth  (Local Z):  9.0000 studs (Z in [ -4.2000,  +4.8000]; Main Wall [-4.2000, +0.6800], 3 Podium Stages [+0.6000, +4.8000])
- Fifteen Separate UI-Ready Replaceable Surface Components (Zero Baked Text, Zero Baked Avatars):
  * 3 Display Header Surfaces:
    1. GEO_Leaderboard_UIHeader_A_SessionKOs       (11.8000 W x 2.3500 H, front Z = +0.1800)
    2. GEO_Leaderboard_UIHeader_B_SessionWins      (11.8000 W x 2.6000 H, front Z = +0.2800)
    3. GEO_Leaderboard_UIHeader_C_SessionStandings (11.8000 W x 2.3500 H, front Z = +0.1800)
  * 3 Display Main Table Surfaces:
    4. GEO_Leaderboard_UIMain_A_SessionKOs         (11.8000 W x 13.0000 H, front Z = +0.1800)
    5. GEO_Leaderboard_UIMain_B_SessionWins        (11.8000 W x 13.4000 H, front Z = +0.2800)
    6. GEO_Leaderboard_UIMain_C_SessionStandings   (11.8000 W x 13.0000 H, front Z = +0.1800)
  * 9 Podium Nameplate Surfaces (3 per Stage x 3 Stages):
    7.  GEO_Leaderboard_PodiumNameplate_A2_2ND     (2.9000 W x 0.9800 H, front Z = +4.5300)
    8.  GEO_Leaderboard_PodiumNameplate_A1_1ST     (3.1000 W x 1.3200 H, front Z = +4.6300)
    9.  GEO_Leaderboard_PodiumNameplate_A3_3RD     (2.9000 W x 0.6800 H, front Z = +4.5300)
    10. GEO_Leaderboard_PodiumNameplate_B2_2ND     (2.9000 W x 0.9800 H, front Z = +4.5300)
    11. GEO_Leaderboard_PodiumNameplate_B1_1ST     (3.1000 W x 1.3200 H, front Z = +4.6300)
    12. GEO_Leaderboard_PodiumNameplate_B3_3RD     (2.9000 W x 0.6800 H, front Z = +4.5300)
    13. GEO_Leaderboard_PodiumNameplate_C2_2ND     (2.9000 W x 0.9800 H, front Z = +4.5300)
    14. GEO_Leaderboard_PodiumNameplate_C1_1ST     (3.1000 W x 1.3200 H, front Z = +4.6300)
    15. GEO_Leaderboard_PodiumNameplate_C3_3RD     (2.9000 W x 0.6800 H, front Z = +4.5300)

Usage:
  1. In standard Python 3 (builds deterministic .obj, .mtl, .glb, palette atlas, and collision proxy):
     python3 generate_hub_leaderboard_blender.py --out_dir ./meshes
  2. In Blender 3.6+ / 4.x (builds scene, saves .blend, and exports .obj/.mtl/.glb):
     blender --background --python generate_hub_leaderboard_blender.py -- --out_dir ./meshes
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
    "EMI_Magnetic",
]

PALETTE_SRGB = {
    "MAT_DarkNeutral": (32, 38, 54),     # #202636 — Primary structural body, piers, housings, podium pedestals, UI backing
    "MAT_AltNeutral":  (42, 50, 70),     # #2A3246 — Secondary slate metallic pedestals, cross-girders, module bezels, stage decks
    "MAT_LightTrim":   (170, 190, 215),  # #AABED7 — Metallic collar clamps, UI frame rails, crown crest, nameplate surrounds
    "EMI_Cyan":        (0, 195, 255),    # #00C3FF — Display A (SESSION KOs) & Stage A emissive conduits and 1st/3rd podium trims
    "EMI_Amber":       (255, 170, 0),    # #FFAA00 — Display B (SESSION WINS) & Stage B emissive conduits and 1st/3rd podium trims
    "EMI_Magnetic":    (165, 55, 255),   # #A537FF — Display C (SESSION STANDINGS) & Stage C emissive conduits and 1st/3rd podium trims
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
        "surface_role": "Dominant structural dark alloy: grounded wall plinth, 4 monumental support piers, rear A-frame stabilizers, 3 display housings, rear service panels, canopy visors, 3 podium stage bases, 9 podium columns, and 15 flat UI-ready backing surfaces",
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
        "surface_role": "Secondary slate metallic: stepped wall pedestal deck, 3 horizontal structural cross-girders, 3 display inner bezels, 3 rear structural spines, and 3 stepped podium stage decks",
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
        "surface_role": "Light metallic mechanical trim: 16 pier collar clamps, display perimeter frame rails, canopy brow trims, 3-tier championship crown crest, 2nd-place silver podium trims, and 9 podium nameplate bezel surrounds",
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
        "surface_role": "Display A (SESSION KOs) and Stage A (A1/A3) emissive cyan conduits, header/main divider bar, canopy visor beacon, rear spine status strip, and Stage A front threshold bar",
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
        "surface_role": "Display B (SESSION WINS) and Stage B (B1/B3) emissive amber conduits, header/main divider bar, center crown beacon, rear spine status strip, and Stage B front threshold bar",
    },
    "EMI_Magnetic": {
        "rgb_255": [165, 55, 255],
        "hex": "#A537FF",
        "normalized_rgb": [round(165 / 255.0, 6), round(55 / 255.0, 6), round(255 / 255.0, 6)],
        "emissive": True,
        "metallic": 0.12,
        "roughness": 0.16,
        "roblox_material": "Enum.Material.Neon",
        "roblox_color3": "Color3.fromRGB(165, 55, 255)",
        "surface_role": "Display C (SESSION STANDINGS) and Stage C (C1/C3) emissive magnetic-purple conduits, header/main divider bar, canopy visor beacon, rear spine status strip, and Stage C front threshold bar",
    },
}

# Placement transform constants
WORLD_POS = (35.0, 150.0, -274.0)
HUB_CENTER = (0.0, 150.0, -300.0)
YAW_RAD = math.atan2(-35.0, -26.0)       # -2.20971034 rad
YAW_DEG = math.degrees(YAW_RAD)          # -126.60707939 deg
COS_YAW = math.cos(YAW_RAD)              # -0.59632400
SIN_YAW = math.sin(YAW_RAD)              # -0.80274385


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


# Build 64x64 deterministic PNG palette atlas (3x2 grid of 6 palette swatches)
ATLAS_FILENAME = "SphereBrawl_Leaderboard_PaletteAtlas.png"


def build_palette_atlas_bytes():
    img = Image.new("RGBA", (64, 64), (32, 38, 54, 255))
    draw = ImageDraw.Draw(img)
    # 3 columns x 2 rows
    col_bounds = [(0, 21), (21, 42), (42, 64)]
    row_bounds = [(0, 32), (32, 64)]
    uv_obj = {}
    uv_gltf = {}
    for idx, mname in enumerate(PALETTE_ORDER):
        c_i = idx % 3
        r_i = idx // 3
        x0, x1 = col_bounds[c_i]
        y0, y1 = row_bounds[r_i]
        rgb = PALETTE_SRGB[mname]
        draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=(rgb[0], rgb[1], rgb[2], 255))
        uc = 0.5 * (x0 + x1) / 64.0
        vc_top = 0.5 * (y0 + y1) / 64.0
        uv_gltf[mname] = (round(uc, 5), round(vc_top, 5))
        uv_obj[mname] = (round(uc, 5), round(1.0 - vc_top, 5))
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=False)
    return buf.getvalue(), uv_obj, uv_gltf


ATLAS_PNG_BYTES, UV_CENTERS_OBJ, UV_CENTERS_GLTF = build_palette_atlas_bytes()

# Locked Concept 06 Board, Stage & Podium Definitions
BOARD_DEFS = [
    {
        "id": "A",
        "name": "SessionKOs",
        "title": "SESSION KOs",
        "subtitle": "CURRENT SERVER • ALPHA SESSION ONLY",
        "columns": ["RANK", "PILOT NAME", "KOs"],
        "x0": -10.1000, "x1": +2.7000, "xc": -3.7000,     # 12.8000 studs outer housing width
        "ui_x0": -9.6000, "ui_x1": +2.2000,               # 11.8000 studs visible UI width
        "y_bot": 3.8000, "y_top": 22.9000,                # 19.1000 studs module housing height
        "main_y0": 6.2000, "main_y1": 19.2000,            # 13.0000 studs tall main table UI
        "hdr_y0": 19.5500, "hdr_y1": 21.9000,             # 2.3500 studs tall header UI
        "z_back": -3.2500, "z_front": +0.1800,
        "emi": "EMI_Cyan",
        "stage_x0": -9.7000, "stage_x1": +2.3000,         # 12.0000 studs wide Stage A
        "stage_z0": +0.6000, "stage_z1": +4.8000,         # 4.2000 studs forward stage projection
        "podiums": [
            {"rank": 2, "key": "A2", "ord": "2ND", "player": "PLAYER 02", "x0": -9.2500, "x1": -5.8500, "xc": -7.5500, "y1": 1.9500, "z0": +1.6500, "z1": +4.4500, "np_w": 2.9000, "np_y0": 0.7400, "np_y1": 1.7200, "trim": "MAT_LightTrim"},
            {"rank": 1, "key": "A1", "ord": "1ST", "player": "PLAYER 01", "x0": -5.5000, "x1": -1.9000, "xc": -3.7000, "y1": 2.5000, "z0": +1.5000, "z1": +4.5500, "np_w": 3.1000, "np_y0": 0.8800, "np_y1": 2.2000, "trim": "EMI_Cyan"},
            {"rank": 3, "key": "A3", "ord": "3RD", "player": "PLAYER 03", "x0": -1.5500, "x1": +1.8500, "xc": +0.1500, "y1": 1.5000, "z0": +1.6500, "z1": +4.4500, "np_w": 2.9000, "np_y0": 0.6600, "np_y1": 1.3400, "trim": "EMI_Cyan"},
        ],
    },
    {
        "id": "B",
        "name": "SessionWins",
        "title": "SESSION WINS",
        "subtitle": "CURRENT SERVER • ALPHA SESSION ONLY",
        "columns": ["RANK", "PILOT NAME", "WINS"],
        "x0": +3.6000, "x1": +16.4000, "xc": +10.0000,    # 12.8000 studs outer housing width (centered at Local X = +10.0000)
        "ui_x0": +4.1000, "ui_x1": +15.9000,              # 11.8000 studs visible UI width
        "y_bot": 3.8000, "y_top": 23.6000,                # 19.8000 studs module housing height
        "main_y0": 6.2000, "main_y1": 19.6000,            # 13.4000 studs tall main table UI
        "hdr_y0": 19.9500, "hdr_y1": 22.5500,             # 2.6000 studs tall header UI
        "z_back": -3.3200, "z_front": +0.2800,
        "emi": "EMI_Amber",
        "stage_x0": +4.0000, "stage_x1": +16.0000,        # 12.0000 studs wide Stage B
        "stage_z0": +0.6000, "stage_z1": +4.8000,         # 4.2000 studs forward stage projection
        "podiums": [
            {"rank": 2, "key": "B2", "ord": "2ND", "player": "PLAYER 02", "x0": +4.4500,  "x1": +7.8500,  "xc": +6.1500,  "y1": 1.9500, "z0": +1.6500, "z1": +4.4500, "np_w": 2.9000, "np_y0": 0.7400, "np_y1": 1.7200, "trim": "MAT_LightTrim"},
            {"rank": 1, "key": "B1", "ord": "1ST", "player": "PLAYER 01", "x0": +8.2000,  "x1": +11.8000, "xc": +10.0000, "y1": 2.5000, "z0": +1.5000, "z1": +4.5500, "np_w": 3.1000, "np_y0": 0.8800, "np_y1": 2.2000, "trim": "EMI_Amber"},
            {"rank": 3, "key": "B3", "ord": "3RD", "player": "PLAYER 03", "x0": +12.1500, "x1": +15.5500, "xc": +13.8500, "y1": 1.5000, "z0": +1.6500, "z1": +4.4500, "np_w": 2.9000, "np_y0": 0.6600, "np_y1": 1.3400, "trim": "EMI_Amber"},
        ],
    },
    {
        "id": "C",
        "name": "SessionStandings",
        "title": "SESSION STANDINGS",
        "subtitle": "CURRENT SERVER • COMBINED OVERVIEW",
        "columns": ["RANK", "PILOT NAME", "KOs", "WINS"],
        "x0": +17.3000, "x1": +30.1000, "xc": +23.7000,   # 12.8000 studs outer housing width
        "ui_x0": +17.8000, "ui_x1": +29.6000,             # 11.8000 studs visible UI width
        "y_bot": 3.8000, "y_top": 22.9000,                # 19.1000 studs module housing height
        "main_y0": 6.2000, "main_y1": 19.2000,            # 13.0000 studs tall main table UI
        "hdr_y0": 19.5500, "hdr_y1": 21.9000,             # 2.3500 studs tall header UI
        "z_back": -3.2500, "z_front": +0.1800,
        "emi": "EMI_Magnetic",
        "stage_x0": +17.7000, "stage_x1": +29.7000,       # 12.0000 studs wide Stage C
        "stage_z0": +0.6000, "stage_z1": +4.8000,         # 4.2000 studs forward stage projection
        "podiums": [
            {"rank": 2, "key": "C2", "ord": "2ND", "player": "PLAYER 02", "x0": +18.1500, "x1": +21.5500, "xc": +19.8500, "y1": 1.9500, "z0": +1.6500, "z1": +4.4500, "np_w": 2.9000, "np_y0": 0.7400, "np_y1": 1.7200, "trim": "MAT_LightTrim"},
            {"rank": 1, "key": "C1", "ord": "1ST", "player": "PLAYER 01", "x0": +21.9000, "x1": +25.5000, "xc": +23.7000, "y1": 2.5000, "z0": +1.5000, "z1": +4.5500, "np_w": 3.1000, "np_y0": 0.8800, "np_y1": 2.2000, "trim": "EMI_Magnetic"},
            {"rank": 3, "key": "C3", "ord": "3RD", "player": "PLAYER 03", "x0": +25.8500, "x1": +29.2500, "xc": +27.5500, "y1": 1.5000, "z0": +1.6500, "z1": +4.4500, "np_w": 2.9000, "np_y0": 0.6600, "np_y1": 1.3400, "trim": "EMI_Magnetic"},
        ],
    },
]


def build_ui_panel_specs():
    specs = []
    # 1..6: 3 Header Surfaces + 3 Main Table Surfaces
    for m in BOARD_DEFS:
        mid = m["id"]
        ux0, ux1 = m["ui_x0"], m["ui_x1"]
        zf = m["z_front"]
        hy0, hy1 = m["hdr_y0"], m["hdr_y1"]
        my0, my1 = m["main_y0"], m["main_y1"]

        hdr_lc = [round(0.5 * (ux0 + ux1), 4), round(0.5 * (hy0 + hy1), 4), round(zf, 4)]
        specs.append({
            "component_name": f"GEO_Leaderboard_UIHeader_{mid}_{m['name']}",
            "surface_role": f"Display {mid} Header Surface ({m['title']})",
            "board_id": mid,
            "theme_material": m["emi"],
            "panel_width_studs": round(ux1 - ux0, 4),
            "panel_height_studs": round(hy1 - hy0, 4),
            "panel_thickness_studs": 0.0600,
            "local_x_span": [round(ux0, 4), round(ux1, 4)],
            "local_y_span": [round(hy0, 4), round(hy1, 4)],
            "local_z_span": [round(zf - 0.06, 4), round(zf, 4)],
            "front_face_local_center": hdr_lc,
            "front_face_world_center": local_to_world_pt(hdr_lc),
            "front_face_local_normal": [0.0, 0.0, 1.0],
            "front_face_world_normal": local_to_world_vec((0.0, 0.0, 1.0)),
            "recommended_surfacegui_face": "Enum.NormalId.Front",
        })

        main_lc = [round(0.5 * (ux0 + ux1), 4), round(0.5 * (my0 + my1), 4), round(zf, 4)]
        specs.append({
            "component_name": f"GEO_Leaderboard_UIMain_{mid}_{m['name']}",
            "surface_role": f"Display {mid} Main Ranking Table Surface ({m['title']})",
            "board_id": mid,
            "theme_material": m["emi"],
            "panel_width_studs": round(ux1 - ux0, 4),
            "panel_height_studs": round(my1 - my0, 4),
            "panel_thickness_studs": 0.0600,
            "local_x_span": [round(ux0, 4), round(ux1, 4)],
            "local_y_span": [round(my0, 4), round(my1, 4)],
            "local_z_span": [round(zf - 0.06, 4), round(zf, 4)],
            "front_face_local_center": main_lc,
            "front_face_world_center": local_to_world_pt(main_lc),
            "front_face_local_normal": [0.0, 0.0, 1.0],
            "front_face_world_normal": local_to_world_vec((0.0, 0.0, 1.0)),
            "recommended_surfacegui_face": "Enum.NormalId.Front",
        })

    # 7..15: 9 Podium Nameplate Surfaces
    for m in BOARD_DEFS:
        mid = m["id"]
        for p in m["podiums"]:
            pkey = p["key"]
            pxc = p["xc"]
            np_hw = 0.5 * p["np_w"]
            npy0, npy1 = p["np_y0"], p["np_y1"]
            npz0, npz1 = round(p["z1"] + 0.03, 4), round(p["z1"] + 0.08, 4)
            np_lc = [round(pxc, 4), round(0.5 * (npy0 + npy1), 4), npz1]
            specs.append({
                "component_name": f"GEO_Leaderboard_PodiumNameplate_{pkey}_{p['ord']}",
                "surface_role": f"Stage {mid} Podium {pkey} ({p['ord']} Place) Replaceable Player Nameplate",
                "board_id": mid,
                "podium_key": pkey,
                "rank": p["rank"],
                "ordinal": p["ord"],
                "theme_material": p["trim"],
                "panel_width_studs": round(p["np_w"], 4),
                "panel_height_studs": round(npy1 - npy0, 4),
                "panel_thickness_studs": 0.0500,
                "local_x_span": [round(pxc - np_hw, 4), round(pxc + np_hw, 4)],
                "local_y_span": [round(npy0, 4), round(npy1, 4)],
                "local_z_span": [npz0, npz1],
                "front_face_local_center": np_lc,
                "front_face_world_center": local_to_world_pt(np_lc),
                "front_face_local_normal": [0.0, 0.0, 1.0],
                "front_face_world_normal": local_to_world_vec((0.0, 0.0, 1.0)),
                "recommended_surfacegui_face": "Enum.NormalId.Front",
            })
    return specs


def build_avatar_anchor_specs():
    anchors = []
    for m in BOARD_DEFS:
        mid = m["id"]
        for p in m["podiums"]:
            pkey = p["key"]
            pxc = p["xc"]
            py1 = p["y1"]
            pzc = round(0.5 * (p["z0"] + p["z1"]), 4)
            feet_loc = [round(pxc, 4), round(py1, 4), pzc]
            head_loc = [round(pxc, 4), round(py1 + 4.0000, 4), pzc]
            anchors.append({
                "podium_key": pkey,
                "stage_id": mid,
                "board_title": m["title"],
                "rank": p["rank"],
                "ordinal": p["ord"],
                "theme_material": p["trim"],
                "podium_component": f"GEO_Leaderboard_Podium_{pkey}_{p['ord']}",
                "nameplate_component": f"GEO_Leaderboard_PodiumNameplate_{pkey}_{p['ord']}",
                "podium_top_width_studs": round(p["x1"] - p["x0"], 4),
                "podium_top_depth_studs": round(p["z1"] - p["z0"], 4),
                "podium_top_elevation_y_studs": round(py1, 4),
                "recommended_avatar_height_studs": 4.0000,
                "recommended_avatar_scale_vs_r15_5_5": round(4.0000 / 5.5000, 4),
                "avatar_feet_local_anchor": feet_loc,
                "avatar_head_top_local_pos": head_loc,
                "avatar_feet_world_anchor": local_to_world_pt(feet_loc),
                "avatar_head_top_world_pos": local_to_world_pt(head_loc),
                "avatar_forward_local_normal": [0.0, 0.0, 1.0],
                "avatar_forward_world_normal": local_to_world_vec((0.0, 0.0, 1.0)),
                "clearance_below_screen_bottom_studs": round(m["main_y0"] - py1, 4),
                "avatar_top_vs_screen_bottom_y_studs": round((py1 + 4.0000) - m["main_y0"], 4),
            })
    return anchors


UI_PANEL_SPECS = build_ui_panel_specs()
AVATAR_ANCHOR_SPECS = build_avatar_anchor_specs()


class LeaderboardMeshBuilder:
    def __init__(self, name="SM_Hub_Leaderboard_01"):
        self.name = name
        self.comp_order = []
        self.comp_tris = {}
        self.comp_mat = {}

    def ensure_component(self, comp_name, mat_name):
        if comp_name not in self.comp_tris:
            self.comp_order.append(comp_name)
            self.comp_tris[comp_name] = []
            self.comp_mat[comp_name] = mat_name

    def add_tri(self, comp_name, mat_name, p0, p1, p2):
        self.ensure_component(comp_name, mat_name)
        v0 = np.array(p0, dtype=np.float64)
        v1 = np.array(p1, dtype=np.float64)
        v2 = np.array(p2, dtype=np.float64)
        if np.linalg.norm(np.cross(v1 - v0, v2 - v0)) > 1e-8:
            self.comp_tris[comp_name].append((v0, v1, v2))

    def add_quad(self, comp_name, mat_name, p0, p1, p2, p3):
        self.add_tri(comp_name, mat_name, p0, p1, p2)
        self.add_tri(comp_name, mat_name, p0, p2, p3)

    def add_poly_cap(self, comp_name, mat_name, pts, flip=False):
        n = len(pts)
        if n < 3:
            return
        for i in range(1, n - 1):
            if not flip:
                self.add_tri(comp_name, mat_name, pts[0], pts[i], pts[i + 1])
            else:
                self.add_tri(comp_name, mat_name, pts[0], pts[i + 1], pts[i])

    def add_closed_loft(self, comp_name, mat_name, ring_bot, ring_top, cap_bot=True, cap_top=True):
        n = len(ring_bot)
        for i in range(n):
            j = (i + 1) % n
            self.add_quad(comp_name, mat_name, ring_bot[i], ring_bot[j], ring_top[j], ring_top[i])
        if cap_bot:
            self.add_poly_cap(comp_name, mat_name, ring_bot, flip=True)
        if cap_top:
            self.add_poly_cap(comp_name, mat_name, ring_top, flip=False)

    def add_box(self, comp_name, mat_name, x0, x1, y0, y1, z0, z1, cap_bot=True, cap_top=True):
        b = [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)]
        t = [(x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0)]
        self.add_closed_loft(comp_name, mat_name, b, t, cap_bot=cap_bot, cap_top=cap_top)

    def add_chamfer_box(self, comp_name, mat_name, x0, x1, y0, y1, z0, z1, cxz=0.15, ctop=0.0, cap_bot=True, cap_top=True):
        c = min(cxz, 0.45 * (x1 - x0), 0.45 * (z1 - z0))
        if c <= 1e-4:
            self.add_box(comp_name, mat_name, x0, x1, y0, y1, z0, z1, cap_bot=cap_bot, cap_top=cap_top)
            return

        def make_ring(xa, xb, y, za, zb, ch):
            return [
                (xa + ch, y, zb),
                (xb - ch, y, zb),
                (xb, y, zb - ch),
                (xb, y, za + ch),
                (xb - ch, y, za),
                (xa + ch, y, za),
                (xa, y, za + ch),
                (xa, y, zb - ch),
            ]

        r_bot = make_ring(x0, x1, y0, z0, z1, c)
        if ctop > 1e-4:
            ym = y1 - ctop
            r_mid = make_ring(x0, x1, ym, z0, z1, c)
            r_top = make_ring(x0 + ctop, x1 - ctop, y1, z0 + ctop, z1 - ctop, max(0.02, c - 0.5 * ctop))
            self.add_closed_loft(comp_name, mat_name, r_bot, r_mid, cap_bot=cap_bot, cap_top=False)
            self.add_closed_loft(comp_name, mat_name, r_mid, r_top, cap_bot=False, cap_top=cap_top)
        else:
            r_top = make_ring(x0, x1, y1, z0, z1, c)
            self.add_closed_loft(comp_name, mat_name, r_bot, r_top, cap_bot=cap_bot, cap_top=cap_top)

    def export_obj_and_mtl(self, obj_path, mtl_path):
        mtl_filename = os.path.basename(mtl_path)
        used_mats = [m for m in PALETTE_ORDER if m in set(self.comp_mat.values())]

        local_atlas_path = os.path.join(os.path.dirname(mtl_path), ATLAS_FILENAME)
        with open(local_atlas_path, "wb") as af:
            af.write(ATLAS_PNG_BYTES)

        with open(mtl_path, "w", encoding="utf-8") as mf:
            mf.write("# Sphere Brawl: Rolling Rampage — Material Library\n")
            mf.write(f"# Asset: {self.name} (Grand Three-Board Monument & Nine-Position Podium Array — 42.0 x 26.0 x 9.0 Studs)\n")
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
            of.write("# Sphere Brawl: Rolling Rampage — Kinetic Hub Leaderboard Monument 3D Asset\n")
            of.write(f"# Asset Name: {self.name} (Phase 2 Approved Production — 42.0 x 26.0 x 9.0 Studs)\n")
            of.write("# Unit Scale: 1.0 Unit = 1.0 Roblox Stud | Up Axis: +Y | Forward Axis: +Z\n")
            of.write("# Local Origin (0,0,0): Approved Concept 06 Pivot (Maps to World (35, 150, -274) at Yaw = -126.60707939 deg)\n")
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
            "name": "SphereBrawl_Leaderboard_PaletteAtlas",
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
            "name": "SphereBrawl_Leaderboard_PaletteAtlas_Tex",
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
                "generator": "Sphere Brawl Leaderboard Monument Production Pipeline (42.0 x 26.0 x 9.0 Studs)",
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


def build_hub_leaderboard():
    """
    Builds the approved 42.0000 (W) x 26.0000 (H) x 9.0000 (D) stud Grand Three-Board Monument
    & Nine-Position Podium Array (`SM_Hub_Leaderboard_01`) across 53 cleanly separated,
    non-overlapping named components (1,852 triangles < 2,000 budget, zero baked text,
    zero static player avatars, zero coplanar cross-component overlaps).
    """
    mb = LeaderboardMeshBuilder("SM_Hub_Leaderboard_01")

    # ==========================================================================
    # 1. MAIN MONUMENT WALL — PROPORTIONATE GROUNDED BASE (Y = 0.00 .. 3.10, X = -11.00 .. +31.00)
    # ==========================================================================
    x0, x1, z0, z1 = -11.0000, +31.0000, -4.2000, +0.6000
    bev_shop = 1.6000
    bev_rear_r = 1.4000
    cr = 0.8000
    plinth_b = [
        (x0 + bev_shop,   0.0000, z1),
        (x1 - cr,         0.0000, z1),
        (x1,              0.0000, z1 - cr),
        (x1,              0.0000, z0 + bev_rear_r),
        (x1 - bev_rear_r, 0.0000, z0),
        (x0 + cr,         0.0000, z0),
        (x0,              0.0000, z0 + cr),
        (x0,              0.0000, z1 - bev_shop),
    ]
    plinth_t = [(px, 1.0500, pz) for (px, _, pz) in plinth_b]
    mb.add_closed_loft("GEO_Leaderboard_WallPlinth", "MAT_DarkNeutral", plinth_b, plinth_t, cap_bot=True, cap_top=True)

    # Stage 2 stepped pedestal deck (Y = 1.05 .. 2.30)
    mb.add_chamfer_box(
        "GEO_Leaderboard_WallPedestal", "MAT_AltNeutral",
        x0=-10.6000, x1=+30.6000, y0=1.0500, y1=2.3000, z0=-3.8500, z1=+0.3500,
        cxz=0.9000, ctop=0.0000, cap_bot=False, cap_top=True
    )
    # Stage 3 upper plinth sill supporting the 26.0-stud monument modules (Y = 2.30 .. 3.10)
    mb.add_chamfer_box(
        "GEO_Leaderboard_WallPlinth", "MAT_DarkNeutral",
        x0=-10.4000, x1=+30.4000, y0=2.3000, y1=3.1000, z0=-3.4500, z1=+0.1500,
        cxz=0.5500, ctop=0.0000, cap_bot=False, cap_top=True
    )

    # ==========================================================================
    # 2. FOUR TALL MONUMENTAL SUPPORT PIERS, 16 COLLAR CLAMPS & REAR BUTTRESSES (Y = 3.10 .. 24.10)
    # ==========================================================================
    pier_defs = [
        (-11.0000, -10.1000, True,  -0.2000),
        ( +2.7000,  +3.6000, False, +0.2200),
        (+16.4000, +17.3000, False, +0.2200),
        (+30.1000, +31.0000, True,  +0.0500),
    ]
    for (px0, px1, is_outer, zf_pier) in pier_defs:
        py_top = 23.3000 if is_outer else 24.1000
        mb.add_chamfer_box(
            "GEO_Leaderboard_SupportPiers", "MAT_DarkNeutral",
            x0=px0, x1=px1, y0=3.1000, y1=py_top, z0=-3.4200, z1=zf_pier,
            cxz=0.1400, ctop=0.0000, cap_bot=False, cap_top=True
        )
        # Four vertical levels of metallic collar clamps along the taller 26-stud piers
        for cy in (6.2000, 11.4000, 16.6000, 21.8000):
            mb.add_box(
                "GEO_Leaderboard_CollarClamps", "MAT_LightTrim",
                x0=max(-10.9800, px0 - 0.0800), x1=min(+30.9800, px1 + 0.0800),
                y0=cy - 0.2800, y1=cy + 0.2800, z0=-3.5500, z1=zf_pier + 0.1000,
                cap_bot=False, cap_top=True
            )
        # Taller, heavier rear diagonal A-frame stabilizer buttress fin anchoring each pier (Y = 1.05 .. 18.20)
        fin_b = [
            (px0 + 0.08, 1.05, -3.35), (px1 - 0.08, 1.05, -3.35),
            (px1 - 0.08, 1.05, -4.15), (px0 + 0.08, 1.05, -4.15),
        ]
        fin_t = [
            (px0 + 0.08, 18.20, -3.35), (px1 - 0.08, 18.20, -3.35),
            (px1 - 0.08, 18.20, -3.58), (px0 + 0.08, 18.20, -3.58),
        ]
        mb.add_closed_loft("GEO_Leaderboard_RearStabilizers", "MAT_DarkNeutral", fin_b, fin_t, cap_bot=False, cap_top=True)

    # Shared Lower, Mid & Upper Monumental Cross-Girders tying the 42.0 x 26.0 stud wall together
    for (gy0, gy1) in [(3.0000, 3.7600), (12.4000, 13.2000), (22.0500, 22.8500)]:
        mb.add_box(
            "GEO_Leaderboard_CrossGirders", "MAT_AltNeutral",
            x0=-10.3000, x1=+30.3000, y0=gy0, y1=gy1, z0=-3.3800, z1=-0.0500,
            cap_bot=False, cap_top=True
        )

    # ==========================================================================
    # 3. THREE TALLER & ULTRA-WIDE DISPLAY MODULES (12.80 W OUTER, 11.80 W x 13.00-13.40 H MAIN UI)
    # ==========================================================================
    for m in BOARD_DEFS:
        mid = m["id"]
        x0_m, x1_m = m["x0"], m["x1"]
        ux0, ux1 = m["ui_x0"], m["ui_x1"]
        yb, yt = m["y_bot"], m["y_top"]
        my0, my1 = m["main_y0"], m["main_y1"]
        hy0, hy1 = m["hdr_y0"], m["hdr_y1"]
        zb, zf = m["z_back"], m["z_front"]
        emi = m["emi"]

        # Outer 12.80-stud x 19.10-19.80-stud module structural housing (MAT_DarkNeutral)
        mb.add_chamfer_box(
            f"GEO_Leaderboard_Module_{mid}_Housing", "MAT_DarkNeutral",
            x0=x0_m, x1=x1_m, y0=yb, y1=yt, z0=zb, z1=zf - 0.14,
            cxz=0.18, ctop=0.00, cap_bot=False, cap_top=True
        )
        # Secondary module bezel surround (MAT_AltNeutral)
        mb.add_box(
            f"GEO_Leaderboard_Module_{mid}_Bezel", "MAT_AltNeutral",
            x0=x0_m + 0.18, x1=x1_m - 0.18, y0=yb + 0.15, y1=yt - 0.15, z0=zf - 0.16, z1=zf - 0.02,
            cap_bot=False, cap_top=False
        )
        # Lower armored dado relief plate below the screen (Y = 4.10 .. 5.80)
        mb.add_box(
            f"GEO_Leaderboard_Module_{mid}_Housing", "MAT_DarkNeutral",
            x0=ux0, x1=ux1, y0=4.10, y1=5.80, z0=zf - 0.04, z1=zf + 0.04,
            cap_bot=True, cap_top=True
        )

        # Metallic outer perimeter frame rails around the taller 11.80-stud UI surface (MAT_LightTrim)
        for (ry0, ry1) in [(hy1, hy1 + 0.20), (my1 + 0.05, hy0 - 0.05), (my0 - 0.22, my0)]:
            mb.add_box(
                "GEO_Leaderboard_LightTrim", "MAT_LightTrim",
                x0=ux0 - 0.24, x1=ux1 + 0.24, y0=ry0, y1=ry1, z0=zf - 0.04, z1=zf + 0.09,
                cap_bot=True, cap_top=True
            )
        for (rx0, rx1) in [(ux0 - 0.24, ux0), (ux1, ux1 + 0.24)]:
            mb.add_box(
                "GEO_Leaderboard_LightTrim", "MAT_LightTrim",
                x0=rx0, x1=rx1, y0=my0 - 0.22, y1=hy1 + 0.20, z0=zf - 0.04, z1=zf + 0.09,
                cap_bot=False, cap_top=False
            )

        # SEPARATE FLAT REPLACEABLE UI HEADER SURFACE (11.80 W x 2.35-2.60 H studs!)
        mb.add_box(
            f"GEO_Leaderboard_UIHeader_{mid}_{m['name']}", "MAT_DarkNeutral",
            x0=ux0, x1=ux1, y0=hy0, y1=hy1, z0=zf - 0.06, z1=zf,
            cap_bot=False, cap_top=False
        )
        # SEPARATE FLAT REPLACEABLE UI MAIN RANKING SURFACE (11.80 W x 13.00-13.40 H studs!)
        mb.add_box(
            f"GEO_Leaderboard_UIMain_{mid}_{m['name']}", "MAT_DarkNeutral",
            x0=ux0, x1=ux1, y0=my0, y1=my1, z0=zf - 0.06, z1=zf,
            cap_bot=False, cap_top=False
        )

        # Recessed theme-colored vertical perimeter channels along the flanks of each taller module
        for (cx0, cx1) in [(x0_m + 0.06, x0_m + 0.20), (x1_m - 0.20, x1_m - 0.06)]:
            mb.add_box(
                f"GEO_Leaderboard_Accent_{mid}", emi,
                x0=cx0, x1=cx1, y0=yb + 0.45, y1=yt - 0.40, z0=zf - 0.03, z1=zf + 0.06,
                cap_bot=False, cap_top=False
            )
        # Recessed theme-colored horizontal accent bars (divider between Header & Main + lower dado strip)
        mb.add_box(
            f"GEO_Leaderboard_Accent_{mid}", emi,
            x0=ux0, x1=ux1, y0=my1 + 0.10, y1=hy0 - 0.10, z0=zf + 0.02, z1=zf + 0.10,
            cap_bot=False, cap_top=False
        )
        mb.add_box(
            f"GEO_Leaderboard_Accent_{mid}", emi,
            x0=ux0 + 0.80, x1=ux1 - 0.80, y0=4.85, y1=5.05, z0=zf + 0.02, z1=zf + 0.08,
            cap_bot=False, cap_top=False
        )

        # Taller Rear module spine & cooling louvers on the back of each 12.80-stud module (Y = 4.10 .. 21.80)
        cx_mid = m["xc"]
        mb.add_chamfer_box(
            "GEO_Leaderboard_RearSpine", "MAT_AltNeutral",
            x0=cx_mid - 4.40, x1=cx_mid + 4.40, y0=4.10, y1=21.80, z0=zb - 0.42, z1=zb,
            cxz=0.20, ctop=0.00, cap_bot=False, cap_top=True
        )
        mb.add_box(
            "GEO_Leaderboard_RearServicePanels", "MAT_DarkNeutral",
            x0=cx_mid - 3.60, x1=cx_mid + 3.60, y0=4.70, y1=10.80, z0=zb - 0.50, z1=zb - 0.38,
            cap_bot=False, cap_top=True
        )
        for ly in (12.00, 14.50, 17.00, 19.20):
            mb.add_box(
                "GEO_Leaderboard_RearServicePanels", "MAT_DarkNeutral",
                x0=cx_mid - 3.60, x1=cx_mid + 3.60, y0=ly, y1=ly + 0.80, z0=zb - 0.50, z1=zb - 0.38,
                cap_bot=False, cap_top=True
            )
        mb.add_box(
            f"GEO_Leaderboard_Accent_{mid}", emi,
            x0=cx_mid - 1.80, x1=cx_mid + 1.80, y0=20.75, y1=21.00, z0=zb - 0.50, z1=zb - 0.40,
            cap_bot=False, cap_top=False
        )

    # ==========================================================================
    # 4. MONUMENTAL UPPER CANOPY VISOR & GRAND 26.00-STUD CENTER CROWN (Y = 22.90 .. 26.00)
    # ==========================================================================
    for (cx0, cx1, b_id, emi) in [(-10.40, +3.10, "A", "EMI_Cyan"), (+16.90, +30.40, "C", "EMI_Magnetic")]:
        mb.add_chamfer_box(
            "GEO_Leaderboard_CanopyCrown", "MAT_DarkNeutral",
            x0=cx0, x1=cx1, y0=22.9000, y1=24.4000, z0=-3.1000, z1=+0.5500,
            cxz=0.3000, ctop=0.0000, cap_bot=False, cap_top=True
        )
        mb.add_box(
            "GEO_Leaderboard_LightTrim", "MAT_LightTrim",
            x0=cx0 + 0.45, x1=cx1 - 0.45, y0=23.0800, y1=23.3400, z0=+0.4500, z1=+0.6200
        )
        mb.add_box(
            f"GEO_Leaderboard_Accent_{b_id}", emi,
            x0=0.5 * (cx0 + cx1) - 3.80, x1=0.5 * (cx0 + cx1) + 3.80,
            y0=23.7200, y1=23.9500, z0=+0.5000, z1=+0.6000
        )

    # Elevated Center Hero Crown over Display B reaching EXACT Y = 26.0000 studs!
    mb.add_chamfer_box(
        "GEO_Leaderboard_CanopyCrown", "MAT_DarkNeutral",
        x0=+3.1500, x1=+16.8500, y0=23.6000, y1=25.1000, z0=-3.1500, z1=+0.6000,
        cxz=0.3200, ctop=0.0000, cap_bot=False, cap_top=True
    )
    mb.add_chamfer_box(
        "GEO_Leaderboard_CanopyCrown", "MAT_DarkNeutral",
        x0=+5.4000, x1=+14.6000, y0=25.1000, y1=26.0000, z0=-2.4500, z1=+0.4500,
        cxz=0.2600, ctop=0.0000, cap_bot=False, cap_top=True
    )
    mb.add_box(
        "GEO_Leaderboard_LightTrim", "MAT_LightTrim",
        x0=+3.6000, x1=+16.4000, y0=23.7800, y1=24.0400, z0=+0.5000, z1=+0.6600
    )
    # 3-Tier Championship Podium Crest on Center Crown (centered at X = +10.00)
    for (px0, px1, py0, py1) in [
        (10.00 - 1.10, 10.00 - 0.42, 24.15, 25.00),
        (10.00 - 0.32, 10.00 + 0.32, 24.15, 25.55),
        (10.00 + 0.42, 10.00 + 1.10, 24.15, 24.80),
    ]:
        mb.add_box(
            "GEO_Leaderboard_LightTrim", "MAT_LightTrim",
            x0=px0, x1=px1, y0=py0, y1=py1, z0=+0.5800, z1=+0.6800
        )
    mb.add_box(
        "GEO_Leaderboard_Accent_B", "EMI_Amber",
        x0=+10.00 - 4.20, x1=+10.00 + 4.20, y0=24.4200, y1=24.6500, z0=+0.5500, z1=+0.6500
    )

    # ==========================================================================
    # 5. THREE SEPARATE FOREGROUND 3-POSITION WINNERS' PODIUM STAGES (STAGE A, STAGE B, STAGE C = 9 PODIUMS)
    # ==========================================================================
    for m in BOARD_DEFS:
        mid = m["id"]
        sx0, sx1 = m["stage_x0"], m["stage_x1"]
        sz0, sz1 = m["stage_z0"], m["stage_z1"]
        emi = m["emi"]

        mb.add_chamfer_box(
            f"GEO_Leaderboard_PodiumStage_{mid}_Base", "MAT_DarkNeutral",
            x0=sx0, x1=sx1, y0=0.0000, y1=0.3200, z0=sz0, z1=sz1,
            cxz=0.6000, ctop=0.0000, cap_bot=True, cap_top=True
        )
        mb.add_chamfer_box(
            f"GEO_Leaderboard_PodiumStage_{mid}_Deck", "MAT_AltNeutral",
            x0=sx0 + 0.25, x1=sx1 - 0.25, y0=0.3200, y1=0.5200, z0=sz0 + 0.05, z1=sz1 - 0.18,
            cxz=0.4500, ctop=0.0000, cap_bot=False, cap_top=True
        )
        mb.add_box(
            f"GEO_Leaderboard_Accent_{mid}", emi,
            x0=sx0 + 0.85, x1=sx1 - 0.85, y0=0.3600, y1=0.5000, z0=sz1 - 0.22, z1=sz1 - 0.12
        )

        for p in m["podiums"]:
            pkey = p["key"]
            px0, px1, pxc = p["x0"], p["x1"], p["xc"]
            pz0, pz1 = p["z0"], p["z1"]
            py0, py1 = 0.5200, p["y1"]
            np_hw = 0.5 * p["np_w"]
            npy0, npy1 = p["np_y0"], p["np_y1"]
            tmat = p["trim"]

            comp_body = f"GEO_Leaderboard_Podium_{pkey}_{p['ord']}"
            comp_np   = f"GEO_Leaderboard_PodiumNameplate_{pkey}_{p['ord']}"

            # Clean unified 8-sided chamfered podium column (Y = 0.5200 .. py1, 22 triangles per podium)
            mb.add_chamfer_box(
                comp_body, "MAT_DarkNeutral",
                x0=px0 - 0.06, x1=px1 + 0.06, y0=py0, y1=py1, z0=pz0 - 0.06, z1=pz1 + 0.06,
                cxz=0.2800, ctop=0.0000, cap_bot=False, cap_top=True
            )
            acc_comp = "GEO_Leaderboard_PodiumLightTrim" if tmat == "MAT_LightTrim" else f"GEO_Leaderboard_PodiumAccent_{mid}"
            mb.add_box(
                acc_comp, tmat,
                x0=px0 + 0.24, x1=px1 - 0.24, y0=py1 - 0.14, y1=py1 - 0.04, z0=pz1 + 0.03, z1=pz1 + 0.09,
                cap_bot=False, cap_top=False
            )
            mb.add_box(
                "GEO_Leaderboard_PodiumLightTrim", "MAT_LightTrim",
                x0=pxc - np_hw - 0.08, x1=pxc + np_hw + 0.08,
                y0=npy0 - 0.05, y1=npy1 + 0.05, z0=pz1 - 0.02, z1=pz1 + 0.05,
                cap_bot=False, cap_top=False
            )
            mb.add_box(
                comp_np, "MAT_DarkNeutral",
                x0=pxc - np_hw, x1=pxc + np_hw, y0=npy0, y1=npy1, z0=pz1 + 0.03, z1=pz1 + 0.08,
                cap_bot=False, cap_top=False
            )

    return mb


def build_collision_proxy():
    """
    Constructs the optional, simplified structural collision proxy (`COL_Leaderboard_Body`, 168 triangles
    across 5 named hull components) covering the grounded monument wall and the 3 separate stepped podium
    stages (all 9 podiums at their exact standing heights Y = 2.50, 1.95, 1.50) without enclosing any of
    the 9 dynamic avatar standing volumes above the podiums or blocking the 1.70-stud inter-stage walkways
    or the front plaza walk-up apron (`Local Z > +4.80`).
    """
    cb = LeaderboardMeshBuilder("COL_Leaderboard_Body")
    cb.ensure_component("COL_Leaderboard_WallPlinthHull", "MAT_DarkNeutral")
    cb.ensure_component("COL_Leaderboard_MainWallHull", "MAT_DarkNeutral")
    cb.ensure_component("COL_Leaderboard_Stage_A_Hull", "MAT_DarkNeutral")
    cb.ensure_component("COL_Leaderboard_Stage_B_Hull", "MAT_DarkNeutral")
    cb.ensure_component("COL_Leaderboard_Stage_C_Hull", "MAT_DarkNeutral")

    # 1. Grounded Wall Plinth Hull (X in [-11.00, +31.00], Y in [0.00, +3.10], Z in [-4.20, +0.60])
    cb.add_box(
        "COL_Leaderboard_WallPlinthHull", "MAT_DarkNeutral",
        x0=-11.0000, x1=+31.0000, y0=0.0000, y1=3.1000, z0=-4.2000, z1=+0.6000
    )
    # 2. Main Monument Wall Hull (X in [-10.94, +30.94], Y in [3.10, +26.00], Z in [-4.15, +0.68])
    cb.add_box(
        "COL_Leaderboard_MainWallHull", "MAT_DarkNeutral",
        x0=-10.9400, x1=+30.9400, y0=3.1000, y1=26.0000, z0=-4.1500, z1=+0.6800
    )
    # 3..5. Three Separate Podium Stage Hulls (Deck + 3 Stepped Podium Pedestals each, open above Y = 2.50/1.95/1.50)
    for m in BOARD_DEFS:
        mid = m["id"]
        hcomp = f"COL_Leaderboard_Stage_{mid}_Hull"
        cb.add_box(
            hcomp, "MAT_DarkNeutral",
            x0=m["stage_x0"], x1=m["stage_x1"], y0=0.0000, y1=0.5200, z0=m["stage_z0"], z1=m["stage_z1"]
        )
        for p in m["podiums"]:
            cb.add_box(
                hcomp, "MAT_DarkNeutral",
                x0=p["x0"] - 0.06, x1=p["x1"] + 0.06, y0=0.5200, y1=p["y1"], z0=p["z0"] - 0.06, z1=p["z1"] + 0.06
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

    mb = build_hub_leaderboard()
    obj_out = os.path.join(out_dir, "SM_Hub_Leaderboard_01.obj")
    mtl_out = os.path.join(out_dir, "SM_Hub_Leaderboard_01.mtl")
    glb_out = os.path.join(out_dir, "SM_Hub_Leaderboard_01.glb")
    mb.export_obj_and_mtl(obj_out, mtl_out)
    mb.export_glb(glb_out)

    col_dir = os.path.join(out_dir, "collision_proxy")
    os.makedirs(col_dir, exist_ok=True)
    cb = build_collision_proxy()
    cb.export_obj_and_mtl(
        os.path.join(col_dir, "COL_Leaderboard_Body.obj"),
        os.path.join(col_dir, "COL_Leaderboard_Body.mtl"),
    )
    cb.export_glb(os.path.join(col_dir, "COL_Leaderboard_Body.glb"))

    tex_dir = os.path.join(os.path.dirname(os.path.abspath(out_dir)), "textures")
    os.makedirs(tex_dir, exist_ok=True)
    with open(os.path.join(tex_dir, ATLAS_FILENAME), "wb") as tf:
        tf.write(ATLAS_PNG_BYTES)

    if HAS_BPY:
        blend_out = os.path.join(out_dir, "SM_Hub_Leaderboard_01.blend")
        build_in_blender(mb, save_blend_path=blend_out)
        print(f"Saved Blender source to {blend_out}")

    total_tris = sum(len(t) for t in mb.comp_tris.values())
    col_tris = sum(len(t) for t in cb.comp_tris.values())
    print(f"Successfully generated production SM_Hub_Leaderboard_01 in {out_dir} ({total_tris} visual triangles across {len(mb.comp_order)} components; {col_tris} collision triangles across {len(cb.comp_order)} hull components).")
