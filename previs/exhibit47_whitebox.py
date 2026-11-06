"""EXHIBIT 47 — whitebox previs generator (Blender 4.2+ / 5.x).

Builds a box-only whitebox of every location in the trailer from the AKOOL
scene images in previs/scene_refs (one set per image), places the characters
for each shot, keys every camera move to the 89-second shot list, and binds
cameras to timeline markers so playing the timeline plays the edit.

Run headless:
    blender -b -P previs/exhibit47_whitebox.py -- --save previs/exhibit47_whitebox.blend
    blender -b -P previs/exhibit47_whitebox.py -- --save X.blend --analyze previs/out
    blender -b -P previs/exhibit47_whitebox.py -- --refs previs/out/refs
    blender -b -P previs/exhibit47_whitebox.py -- --render previs/out/frames --sample [--only 10,21]
Or open Blender, Scripting tab, open this file, Run Script (builds the scene).

Everything is in metres, Z up. Each set has its own origin (P["*_origin"]);
inside a set +Y is "into the picture" of its scene image. All dimensions live
in P: change them, re-run, and every set, actor and camera follows.
CAM_REF_<set> reproduces the scene image's viewpoint for side-by-side checks.
"""
import bpy, math, json, os, sys, random
from mathutils import Vector, Quaternion

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default=None, flag=False):
    if name not in ARGS:
        return default
    if flag:
        return True
    i = ARGS.index(name)
    return ARGS[i + 1] if i + 1 < len(ARGS) else default

FPS = 24
TINY = (1e-3, 1e-3, 1e-3)   # "hidden" scale: exactly 0 makes Cycles render black frames
def fr(t):
    """Master timeline seconds -> frame number (frame 1 = 0.0 s)."""
    return int(round(t * FPS)) + 1

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
COLL, MATS = {}, {}
UNIT = None
EVENTS = []          # (shot id, master time, description)
SHOTS = []           # shot dicts, filled by shot builders
LABELS = []          # viewport-only text labels

def ev(shot, t, desc):
    EVENTS.append((shot, round(t, 2), desc))

def coll(name, parent=None):
    if name in COLL:
        return COLL[name]
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    COLL[name] = c
    return c

def _principled(m):
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
        out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None) or nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(bsdf.outputs[0], out.inputs[0])
    return bsdf

def mat(name, rgb, metal=0.0, rough=0.85, emit=0.0, alpha=1.0):
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new(name)
    b = _principled(m)
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1)
        b.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    m.diffuse_color = (*rgb, max(alpha, 0.3))
    MATS[name] = m
    return m

def unit_mesh():
    global UNIT
    if UNIT is None:
        h = 0.5
        v = [(-h, -h, -h), (h, -h, -h), (h, h, -h), (-h, h, -h), (-h, -h, h), (h, -h, h), (h, h, h), (-h, h, h)]
        f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        UNIT = bpy.data.meshes.new("UnitBox")
        UNIT.from_pydata(v, [], f)
        UNIT.update()
        UNIT.materials.append(mat("clay", (0.8, 0.8, 0.8)))
    return UNIT

def box(name, center, size, m, col, rot=(0, 0, 0), parent=None, lid=False):
    o = bpy.data.objects.new(name, unit_mesh())
    col.objects.link(o)
    o.material_slots[0].link = "OBJECT"
    o.material_slots[0].material = m
    if parent is not None:
        o.parent = parent
    o.location = center
    o.scale = size
    o.rotation_euler = rot
    if lid:  # roofs and ceilings let skylight through so interiors stay readable
        o.visible_shadow = False
    return o

def boxr(name, x0, x1, y0, y1, z0, z1, m, col, lid=False):
    return box(name, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)), m, col, lid=lid)

def rect_minus(r, h):
    """r, h = (x0, x1, y0, y1); returns up to 4 rects covering r minus h."""
    x0, x1, y0, y1 = r
    hx0, hx1, hy0, hy1 = max(h[0], x0), min(h[1], x1), max(h[2], y0), min(h[3], y1)
    if hx0 >= hx1 or hy0 >= hy1:
        return [r]
    out = []
    if hy0 > y0: out.append((x0, x1, y0, hy0))
    if hy1 < y1: out.append((x0, x1, hy1, y1))
    if hx0 > x0: out.append((x0, hx0, hy0, hy1))
    if hx1 < x1: out.append((hx1, x1, hy0, hy1))
    return out

def wall_x(name, x0, x1, y0, y1, z0, z1, holes, m, col):
    """Wall running along X with rectangular holes [(xc, w, zb, zt)]."""
    holes = sorted(holes)
    cur = x0
    for i, (xc, w, zb, zt) in enumerate(holes):
        a, b = xc - w / 2, xc + w / 2
        if a > cur:
            boxr(f"{name}_{i}a", cur, a, y0, y1, z0, z1, m, col)
        if zb > z0:
            boxr(f"{name}_{i}lo", a, b, y0, y1, z0, zb, m, col)
        if zt < z1:
            boxr(f"{name}_{i}hi", a, b, y0, y1, zt, z1, m, col)
        cur = b
    if cur < x1:
        boxr(f"{name}_end", cur, x1, y0, y1, z0, z1, m, col)

def wall_y(name, x0, x1, y0, y1, z0, z1, holes, m, col):
    """Wall running along Y with rectangular holes [(yc, w, zb, zt)]."""
    holes = sorted(holes)
    cur = y0
    for i, (yc, w, zb, zt) in enumerate(holes):
        a, b = yc - w / 2, yc + w / 2
        if a > cur:
            boxr(f"{name}_{i}a", x0, x1, cur, a, z0, z1, m, col)
        if zb > z0:
            boxr(f"{name}_{i}lo", x0, x1, a, b, z0, zb, m, col)
        if zt < z1:
            boxr(f"{name}_{i}hi", x0, x1, a, b, zt, z1, m, col)
        cur = b
    if cur < y1:
        boxr(f"{name}_end", x0, x1, cur, y1, z0, z1, m, col)

CUR_INTERP = ["BEZIER"]

def interp(kind):
    """Interpolation for the keys inserted next (Blender 5 ignores the user
    preference for keys inserted from Python, so ins() sets it per key)."""
    CUR_INTERP[0] = kind
    try:
        bpy.context.preferences.edit.keyframe_new_interpolation_type = kind
    except Exception:
        pass

def fcurves(obj):
    ad = obj.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    try:
        return list(act.fcurves)          # Blender 4.x
    except Exception:
        pass
    out = []                               # Blender 4.4+/5.x slotted actions
    for layer in act.layers:
        for strip in layer.strips:
            cb = strip.channelbag(ad.action_slot)
            if cb:
                out.extend(cb.fcurves)
    return out

def ins(obj, path, frame):
    obj.keyframe_insert(path, frame=frame)
    for fc in fcurves(obj):
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.5:
                    kp.interpolation = CUR_INTERP[0]

def key(obj, path, t, value, kind="LINEAR"):
    interp(kind)
    setattr(obj, path, value)
    ins(obj, path, fr(t))

def window(obj, t0, t1):
    """Object exists only during [t0, t1): scale 0 outside (constant keys)."""
    interp("CONSTANT")
    s = tuple(obj.scale)
    obj.scale = TINY; ins(obj, "scale", 1)
    obj.scale = s;         ins(obj, "scale", fr(t0))
    obj.scale = TINY; ins(obj, "scale", fr(t1))
    obj.scale = s

def heading(dx, dy):
    """Z rotation that turns local +Y towards (dx, dy)."""
    return math.atan2(-dx, dy)

def look(loc, tgt, roll=0.0):
    q = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y")
    if roll:
        q = q @ Quaternion((0, 0, 1), roll)
    return q.to_euler("XYZ")

def label(text, parent, z, col):
    cu = bpy.data.curves.new(f"lbl_{parent.name}", "FONT")
    cu.body = text
    cu.size = 0.22
    cu.align_x = "CENTER"
    o = bpy.data.objects.new(f"lbl_{parent.name}", cu)
    col.objects.link(o)
    o.parent = parent
    o.location = (0, 0, z)
    o.rotation_euler = (math.pi / 2, 0, 0)
    o.hide_render = True
    LABELS.append(o)
    return o

# --------------------------------------------------------------------------
# materials (previs colour code: environment is clay, people are coloured)
# --------------------------------------------------------------------------
def make_materials():
    mat("clay", (0.80, 0.80, 0.80))
    mat("clay_dark", (0.45, 0.45, 0.47))
    mat("concrete", (0.62, 0.62, 0.62))
    mat("snow", (0.93, 0.94, 0.96))
    mat("road", (0.55, 0.56, 0.58))
    mat("water", (0.05, 0.07, 0.09), rough=0.2)
    mat("rust", (0.42, 0.33, 0.28))
    mat("shutter", (0.52, 0.52, 0.55))
    mat("void", (0.02, 0.02, 0.02))
    mat("steel", (0.70, 0.72, 0.75), metal=1.0, rough=0.35)
    mat("mirror", (0.90, 0.92, 0.95), metal=1.0, rough=0.04)
    mat("oneway", (0.03, 0.03, 0.035), metal=0.0, rough=0.05)
    mat("frost", (0.86, 0.90, 0.95))
    mat("crate", (0.72, 0.66, 0.56))
    mat("curtain", (0.85, 0.90, 0.95), rough=0.3, alpha=0.45)
    mat("fog", (0.95, 0.95, 0.95), alpha=0.25)
    mat("gas", (0.97, 0.97, 0.97), emit=0.5, alpha=0.6)
    mat("panel_light", (1.0, 0.98, 0.92), emit=6.0)
    mat("flash", (1.0, 0.85, 0.55), emit=40.0)
    mat("flashbang", (1.0, 1.0, 1.0), emit=60.0)
    mat("torch", (1.0, 0.95, 0.8), emit=25.0)
    mat("van", (0.20, 0.21, 0.23))
    mat("glass_dark", (0.05, 0.05, 0.06), rough=0.1)
    mat("bag", (0.70, 0.82, 0.92), rough=0.2, alpha=0.6)
    mat("tag_white", (0.95, 0.95, 0.95))
    mat("tag_red", (0.80, 0.05, 0.04))
    mat("rec_red", (1.0, 0.05, 0.02), emit=12.0)
    mat("footprint", (0.55, 0.58, 0.64))
    # people
    mat("officer", (0.33, 0.36, 0.41))
    mat("officer_past", (0.28, 0.30, 0.33))
    mat("helmet", (0.10, 0.10, 0.11))
    mat("nora", (0.05, 0.65, 0.78))
    mat("thirteenth", (1.00, 0.42, 0.02))
    mat("brandt", (0.95, 0.78, 0.08))
    mat("ward", (0.50, 0.30, 0.72))
    mat("leo", (0.20, 0.68, 0.30))
    mat("skin", (0.80, 0.62, 0.52))
    mat("scar", (0.95, 0.35, 0.45))
    mat("pen", (0.02, 0.02, 0.02))
    mat("bodycam", (0.06, 0.06, 0.06))

# --------------------------------------------------------------------------
# people: box mannequins (root empty at the feet, local +Y = facing)
# --------------------------------------------------------------------------
ROLE = {
    "officer": ("officer", "helmet"), "officer_past": ("officer_past", "helmet"),
    "nora": ("nora", "helmet"), "nora_room": ("nora", None),
    "thirteenth": ("thirteenth", "helmet"), "brandt": ("brandt", "helmet"),
    "ward": ("ward", None), "leo": ("leo", None),
}

def person(name, role, pos, face, col, pose="stand", tag=None, wearer=False, z=0.0):
    body_m, helm_m = ROLE[role]
    bm, hm = MATS[body_m], (MATS[helm_m] if helm_m else None)
    root = bpy.data.objects.new(name, None)
    col.objects.link(root)
    root.empty_display_size = 0.3
    root.location = (pos[0], pos[1], z)
    root.rotation_euler = (0, 0, face)
    root["role"] = role
    parts = {}
    sit = pose in ("sit", "crouch")
    hip = 0.46 if sit else 0.84
    if sit:
        for s, x in (("l", -0.1), ("r", 0.1)):
            parts["thigh_" + s] = box(f"{name}_thigh_{s}", (x, 0.22, hip), (0.16, 0.46, 0.16), bm, col, parent=root)
            parts["shin_" + s] = box(f"{name}_shin_{s}", (x, 0.42, hip / 2), (0.15, 0.15, hip), bm, col, parent=root)
    else:
        for s, x in (("l", -0.1), ("r", 0.1)):
            parts["leg_" + s] = box(f"{name}_leg_{s}", (x, 0, hip / 2), (0.16, 0.18, hip), bm, col, parent=root)
    top = hip + 0.62
    parts["torso"] = box(f"{name}_torso", (0, 0, (hip + top) / 2), (0.42, 0.25, 0.62), bm, col, parent=root)
    if helm_m:  # tactical vest
        parts["vest"] = box(f"{name}_vest", (0, 0, top - 0.24), (0.46, 0.32, 0.44), MATS["helmet"] if role != "officer" else bm, col, parent=root)
        parts["vest"].material_slots[0].material = MATS["clay_dark"] if role == "officer" else bm
        parts["cam"] = box(f"{name}_bodycam", (0, 0.17, top - 0.12), (0.07, 0.04, 0.1), MATS["bodycam"], col, parent=root)
        parts["rec"] = box(f"{name}_rec", (0.025, 0.195, top - 0.08), (0.02, 0.01, 0.02), MATS["rec_red"], col, parent=root)
    head_z = top + 0.18
    parts["head"] = box(f"{name}_head", (0, 0.01, head_z), (0.2, 0.23, 0.25), MATS["skin"] if not helm_m else hm, col, parent=root)
    if helm_m:
        parts["helmet"] = box(f"{name}_helmet", (0, 0, head_z + 0.11), (0.27, 0.30, 0.13), hm, col, parent=root)
    for s, x in (("l", -0.27), ("r", 0.27)):
        piv = bpy.data.objects.new(f"{name}_shoulder_{s}", None)
        col.objects.link(piv)
        piv.parent = root
        piv.location = (x, 0, top - 0.05)
        piv.empty_display_size = 0.05
        parts["arm_" + s] = box(f"{name}_arm_{s}", (0, 0, -0.31), (0.11, 0.11, 0.62), bm, col, parent=piv)
        hand_m = MATS["skin"] if role in ("ward", "leo", "nora_room") else (MATS["helmet"] if helm_m else bm)
        parts["hand_" + s] = box(f"{name}_hand_{s}", (0, 0, -0.68), (0.1, 0.07, 0.17), hand_m, col, parent=piv)
        parts["sh_" + s] = piv
    if role in ("ward", "thirteenth"):  # the burn scar on the back of the right hand
        parts["scar"] = box(f"{name}_scar", (0, 0.04, -0.66), (0.05, 0.01, 0.11), MATS["scar"], col, parent=parts["sh_r"])
    set_pose(parts, pose)
    if pose == "rifle":
        parts["rifle"] = box(f"{name}_rifle", (0.12, 0.42, top - 0.2), (0.07, 0.85, 0.09), MATS["helmet"], col, parent=root)
        parts["muzzle"] = box(f"{name}_muzzle", (0.12, 0.88, top - 0.2), (0.16, 0.16, 0.16), MATS["flash"], col, parent=root)
        parts["muzzle"].scale = TINY
    label(tag or name, root, top + 0.55, col)
    root["parts"] = [o.name for o in parts.values() if o.type == "MESH"]
    if wearer:  # the camera wearer: invisible to the camera, visible in mirrors
        for o in parts.values():
            if o.type == "MESH":
                o.visible_camera = False
        root["pov_wearer"] = True
    return root, parts

def set_pose(parts, pose):
    a = {"stand": 0.08, "rifle": 1.15, "hands_up": 2.95, "sit": 1.2, "crouch": 0.6}.get(pose, 0.08)
    for s in ("l", "r"):
        parts["sh_" + s].rotation_euler = (a, 0, 0)
    if pose == "rifle":
        parts["sh_l"].rotation_euler = (1.25, 0, -0.35)
    if pose == "hands_up":
        parts["sh_l"].rotation_euler = (2.95, 0.25, 0)
        parts["sh_r"].rotation_euler = (2.95, -0.25, 0)

def arm(parts, side, t, rot, kind="LINEAR"):
    key(parts["sh_" + side], "rotation_euler", t, rot, kind)

def move(root, t, loc, kind="LINEAR"):
    key(root, "location", t, loc, kind)

def turn(root, t, face, kind="LINEAR", tilt=0.0):
    key(root, "rotation_euler", t, (tilt, 0, face), kind)

def flash(obj, times):
    """Muzzle / flash boxes: 2-frame pops at the given master times."""
    interp("CONSTANT")
    obj.scale = TINY; ins(obj, "scale", 1)
    for t in times:
        obj.scale = (1, 1, 1); ins(obj, "scale", fr(t))
        obj.scale = TINY; ins(obj, "scale", fr(t) + 2)

# --------------------------------------------------------------------------
# cameras
# --------------------------------------------------------------------------
def camera(name, lens, col, clip=0.03):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = 36.0
    cd.sensor_fit = "HORIZONTAL"
    cd.clip_start = clip
    cd.clip_end = 600
    o = bpy.data.objects.new(name, cd)
    col.objects.link(o)
    return o

def shake(t, seed, amp):
    r = random.Random(seed)
    ph = [r.uniform(0, 6.283) for _ in range(9)]
    f = (1.9, 3.3, 5.1)
    def s(i):
        return sum(math.sin(6.283 * f[k] * t + ph[i * 3 + k]) * (0.55, 0.3, 0.15)[k] for k in range(3))
    return Vector((s(0), s(1), s(2))) * amp

def cam_keys(cam, t0, t1, pose, shake_amp=0.0, seed=1, step=1):
    """pose(u, t) -> (loc, target, roll). Keys every `step` frames."""
    interp("LINEAR")
    prev = None
    f0, f1 = fr(t0), fr(t1)
    for f in list(range(f0, f1, step)) + [f1 - 1]:
        t = (f - 1) / FPS
        u = 0.0 if f1 - 1 == f0 else (f - f0) / (f1 - 1 - f0)
        loc, tgt, roll = pose(u, t)
        e = look(loc, tgt, roll)
        if shake_amp:
            sh = shake(t, seed, shake_amp)
            e.x += sh.x; e.y += sh.y * 0.6; e.z += sh.z
            loc = Vector(loc) + Vector((0, 0, sh.x * 0.25))
        if prev is not None:
            e.make_compatible(prev)
        prev = e
        cam.location = loc
        cam.rotation_euler = e
        ins(cam, "location", f)
        ins(cam, "rotation_euler", f)

def ease(u):
    return u * u * (3 - 2 * u)

def lerp(a, b, u):
    return Vector(a).lerp(Vector(b), u)

def shot(n, code, t0, dur, cam, loc, style, prompt, actors, notes="", source=False):
    s = dict(n=n, code=code, t0=t0, t1=t0 + dur, dur=dur, cam=cam.name, lens=cam.data.lens,
             loc=loc, style=style, prompt=prompt, actors=[a.name for a in actors], notes=notes, source=source)
    SHOTS.append(s)
    for a in actors:
        window(a, t0, t0 + dur)
    return s

# --------------------------------------------------------------------------
# P: every dimension, measured from the AKOOL scene images (previs/scene_refs)
# --------------------------------------------------------------------------
P = dict(
    # SET 1 exterior, from ext_v1.jpg (drone view from the south, 24 mm assumed)
    ext_origin=(0.0, 0.0, 0.0),
    plant_x=(-17.7, 17.0), plant_depth=46.0, plant_h=8.5, wall_t=0.4,
    windows_x=[-15.4, -10.9, -6.8, -3.0], windows_z=(4.9, 6.6), window_w=1.3,
    door_x=-12.9, door_w=1.0, door_h=2.4,                 # personnel steel door (B1)
    bay_x=1.5, bay_w=4.6, bay_h=4.4,                      # the open loading bay (D1)
    canopy=(-0.8, 3.8, -1.6, 4.5),                        # x0, x1, front y, underside z
    shutters_x=[6.8, 13.0], shutter_w=4.1, shutter_h=6.0,
    gate_y=-19.9, gate_x=1.9, gate_w=7.7, fence_x=(-40.0, 40.0),
    # (x0, x1, y0, y1, height, z-rotation in degrees, material): the building density
    neighbours=[
        (-42.0, -21.0, -2.0, 26.0, 6.5, 0, "clay"),       # left warehouse, ~3 m gap
        (-60.0, -38.0, 30.0, 60.0, 7.0, 0, "clay"),
        (21.0, 33.0, -16.0, 14.0, 5.5, -12, "rust"),      # red shed, front right, ~4 m gap
        (20.0, 44.0, 18.0, 40.0, 7.0, 0, "clay"),         # grey warehouse behind right
        (-30.0, -8.0, 52.0, 66.0, 6.0, 0, "clay"),
        (10.0, 40.0, 50.0, 70.0, 8.0, 0, "clay"),
        (-24.0, -10.0, 47.0, 51.0, 5.0, 0, "clay"),
    ],
    containers=[(-34.0, -21.0, -8.0, -2.5, 2), (18.5, 26.0, 8.0, 16.0, 3), (-20.0, 20.0, 76.0, 86.0, 2), (30.0, 60.0, 72.0, 84.0, 3)],
    sea_y=92.0,
    ref_ext=((2.0, -42.7, 12.4), (2.0, 9.8, 0.0), 24),
    # SET 2 stairwell, from stair_v1.jpg: straight flight, then a turn to the right
    stair_origin=(300.0, 0.0, 0.0), stair_w=1.6, riser=0.18, tread=0.3, steps_a=12, steps_b=12,
    ref_stair=((0.05, -0.75, 1.6), (0.15, 3.2, -1.7), 24),
    # SET 3 freezer hall, from hall_v1.jpg: one long hall, hook rails both sides
    hall_origin=(400.0, 0.0, 0.0), hall_w=14.0, hall_len=56.0, hall_h=6.0,
    col_x=5.6, col_y0=4.0, col_step=5.0, rail_x=3.4, rail_z=4.0, hook_step=0.6,
    room4_door=3,                                          # 4th door on the right wall
    ref_hall=((0.0, 0.6, 1.6), (0.0, 56.0, 2.2), 24),
    # SET 4 freezer room 4, from room4_v1.jpg
    room4_origin=(500.0, 0.0, 0.0), room4=(3.8, 7.0, 3.2), room4_door_y=3.9,
    ref_room4=((0.35, -0.1, 2.0), (-0.35, 7.0, 1.15), 18),
    # SET 5 interview room, from interview_v1.jpg
    int_origin=(600.0, 0.0, 0.0), int_room=(3.6, 5.0, 2.7),
    ref_int=((0.95, 0.12, 2.35), (-0.25, 4.2, 0.8), 20),
    # SET 6 evidence room, from evidence_v2.jpg (the red tag is on the NEAREST bag)
    ev_origin=(700.0, 0.0, 0.0), ev_room=(5.0, 10.0, 3.0),
    ref_ev=((0.3, -0.5, 1.45), (1.1, 7.0, 0.6), 24),
)
SETS = {}
REFS = {}

def L(set_, x, y, z=0.0):
    o = SETS[set_]
    return Vector((o[0] + x, o[1] + y, o[2] + z))

def bl(set_, name, x0, x1, y0, y1, z0, z1, m, col, lid=False):
    o = SETS[set_]
    return boxr(name, o[0] + x0, o[0] + x1, o[1] + y0, o[1] + y1, o[2] + z0, o[2] + z1, m, col, lid=lid)

def ref_cam(set_, key_, col):
    loc, tgt, lens = P[key_]
    c = camera(f"CAM_REF_{set_}", lens, col)
    c.location = L(set_, *loc)
    c.rotation_euler = look(L(set_, *loc), L(set_, *tgt))
    REFS[set_] = c.name
    return c

def extra_materials():
    mat("window_light", (0.85, 0.90, 0.96), emit=2.5)
    mat("fence_mesh", (0.35, 0.36, 0.38), alpha=0.3)
    mat("blue_container", (0.18, 0.28, 0.45))
    mat("hall_glow", (0.92, 0.95, 1.0), emit=3.0)

# --------------------------------------------------------------------------
# SET 1: exterior (ext_v1)
# --------------------------------------------------------------------------
def set_exterior():
    S = "EXT"
    SETS[S] = P["ext_origin"]
    C = coll("SET_1_EXTERIOR (scene_refs/ext_v1.jpg)")
    x0, x1 = P["plant_x"]
    d, h, t = P["plant_depth"], P["plant_h"], P["wall_t"]
    gy, gx, gw = P["gate_y"], P["gate_x"], P["gate_w"]
    for i, r in enumerate(rect_minus((-220, 220, -220, P["sea_y"]), (x0, x1, 0, d))):
        bl(S, f"ground_snow_{i}", *r, -0.3, 0.0, MATS["snow"], C)
    bl(S, "road_south", gx - 3.5, gx + 3.5, -220, gy, 0.0, 0.02, MATS["road"], C)
    bl(S, "quay_wall", -220, 220, P["sea_y"], P["sea_y"] + 1, -2.4, 0.0, MATS["concrete"], C)
    bl(S, "sea", -400, 400, P["sea_y"] + 1, 600, -2.6, -2.4, MATS["water"], C)
    # facade with windows, personnel door, open bay and two shutters
    wz0, wz1 = P["windows_z"]
    holes = [(x, P["window_w"], wz0, wz1) for x in P["windows_x"]]
    holes += [(P["door_x"], P["door_w"], 0.0, P["door_h"]), (P["bay_x"], P["bay_w"], 0.0, P["bay_h"])]
    holes += [(x, P["shutter_w"], 0.0, P["shutter_h"]) for x in P["shutters_x"]]
    o = SETS[S]
    wall_x("facade", o[0] + x0, o[0] + x1, o[1], o[1] + t, 0.0, h, [(xc + o[0], w, zb, zt) for xc, w, zb, zt in holes], MATS["concrete"], C)
    bl(S, "wall_back", x0, x1, d - t, d, 0, h, MATS["concrete"], C)
    bl(S, "wall_left", x0, x0 + t, 0, d, 0, h, MATS["concrete"], C)
    bl(S, "wall_right", x1 - t, x1, 0, d, 0, h, MATS["concrete"], C)
    bl(S, "roof", x0 - 0.3, x1 + 0.3, -0.3, d + 0.3, h, h + 0.35, MATS["snow"], C)
    for x in P["windows_x"]:
        bl(S, f"window_pane_{x}", x - P["window_w"] / 2, x + P["window_w"] / 2, 0.25, 0.3, wz0, wz1, MATS["void"], C)
    for x in P["shutters_x"]:
        bl(S, f"shutter_{x}", x - P["shutter_w"] / 2, x + P["shutter_w"] / 2, 0.15, 0.25, 0.0, P["shutter_h"], MATS["shutter"], C)
        bl(S, f"shutter_lintel_{x}", x - P["shutter_w"] / 2 - 0.2, x + P["shutter_w"] / 2 + 0.2, -0.15, 0.0, P["shutter_h"], P["shutter_h"] + 0.45, MATS["rust"], C)
    bx = P["bay_x"]
    bl(S, "bay_darkness", bx - P["bay_w"] / 2, bx + P["bay_w"] / 2, 2.0, 2.2, 0.0, P["bay_h"], MATS["void"], C)
    cx0, cx1, cfy, cz = P["canopy"]
    bl(S, "bay_canopy", cx0, cx1, cfy, 0.0, cz, cz + 0.2, MATS["snow"], C)
    for x in (cx0 + 0.2, cx1 - 0.2):
        bl(S, f"canopy_post_{x}", x - 0.08, x + 0.08, cfy + 0.05, cfy + 0.2, 0.0, cz, MATS["rust"], C)
    hinge = bpy.data.objects.new("door_hinge", None)
    C.objects.link(hinge)
    hinge.location = L(S, P["door_x"] - P["door_w"] / 2, t / 2)
    box("door_leaf", (P["door_w"] / 2, 0, P["door_h"] / 2), (P["door_w"], 0.06, P["door_h"]), MATS["steel"], C, parent=hinge)
    # neighbours = building density
    for i, (a, b, c_, e, hh, rot, m) in enumerate(P["neighbours"]):
        ob = bl(S, f"building_{i}", a, b, c_, e, 0.0, hh, MATS[m], C)
        ob.rotation_euler = (0, 0, math.radians(rot))
        bl(S, f"building_{i}_roof", a, b, c_, e, hh, hh + 0.2, MATS["snow"], C).rotation_euler = (0, 0, math.radians(rot))
    r = random.Random(7)
    for k, (a, b, c_, e, hi) in enumerate(P["containers"]):
        x = a
        while x + 6.0 <= b:
            y = r.uniform(c_, max(c_, e - 2.5))
            for lvl in range(r.randint(1, hi)):
                m = MATS[r.choice(("rust", "blue_container", "clay_dark"))]
                bl(S, f"container_{k}_{int(x)}_{lvl}", x, x + 6.0, y, y + 2.45, lvl * 2.6, lvl * 2.6 + 2.55, m, C)
            x += 6.4
    for i, x in enumerate((60, 78, 95, 118, 140)):  # harbour cranes in the mist
        bl(S, f"crane_{i}_tower", x, x + 2.0, 200, 202, 0.0, 42.0, MATS["clay_dark"], C)
        bl(S, f"crane_{i}_boom", x - 4.0, x + 6.0, 190, 225, 40.0, 42.0, MATS["clay_dark"], C)
    # fence and gate
    fx0, fx1 = P["fence_x"]
    for a, b in ((fx0, gx - gw / 2), (gx + gw / 2, fx1)):
        bl(S, f"fence_{a}", a, b, gy - 0.02, gy + 0.02, 0.0, 2.2, MATS["fence_mesh"], C)
        x = a
        while x <= b:
            bl(S, f"fence_post_{x:.0f}", x - 0.04, x + 0.04, gy - 0.04, gy + 0.04, 0.0, 2.3, MATS["clay_dark"], C)
            x += 3.0
    for s in (-1, 1):
        bl(S, f"gate_leaf_{s}", min(gx, gx + s * gw / 2), max(gx, gx + s * gw / 2), gy - 0.04, gy + 0.04, 0.0, 2.1, MATS["fence_mesh"], C)
        bl(S, f"gate_frame_{s}", min(gx, gx + s * gw / 2), max(gx, gx + s * gw / 2), gy - 0.05, gy + 0.05, 2.0, 2.1, MATS["rust"], C)
        bl(S, f"gate_post_{s}", gx + s * gw / 2 - 0.08, gx + s * gw / 2 + 0.08, gy - 0.08, gy + 0.08, 0.0, 2.4, MATS["rust"], C)
    bl(S, "floodlight_pole_dead", 9.5, 9.7, -3.0, -2.8, 0.0, 7.0, MATS["clay_dark"], C)
    bl(S, "floodlight_head_dead", 9.2, 10.0, -3.2, -2.6, 6.7, 7.2, MATS["clay_dark"], C)
    ref_cam(S, "ref_ext", C)

def van(name, col):
    root = bpy.data.objects.new(name, None)
    col.objects.link(root)
    box(f"{name}_body", (0, -0.4, 1.35), (2.0, 4.2, 1.9), MATS["van"], col, parent=root)
    box(f"{name}_cab", (0, 2.1, 1.05), (2.0, 1.2, 1.3), MATS["van"], col, parent=root)
    box(f"{name}_windshield", (0, 2.72, 1.45), (1.8, 0.05, 0.6), MATS["glass_dark"], col, parent=root)
    door = box(f"{name}_sidedoor", (1.02, 0.4, 1.3), (0.05, 1.3, 1.7), MATS["van"], col, parent=root)
    for (x, y) in ((-0.95, 1.8), (0.95, 1.8), (-0.95, -1.6), (0.95, -1.6)):
        box(f"{name}_wheel_{x}_{y}", (x, y, 0.36), (0.28, 0.72, 0.72), MATS["void"], col, parent=root)
    label(name, root, 2.8, col)
    return root, door

# --------------------------------------------------------------------------
# SET 2: stairwell (stair_v1): top landing, flight A north, corner, flight B east
# --------------------------------------------------------------------------
def stair_z(lane, s):
    """Tread top for flight A (s = y) or flight B (s = x)."""
    r, tr = P["riser"], P["tread"]
    if lane == "A":
        i = min(P["steps_a"] - 1, max(0, int(s / tr)))
        return -(i + 1) * r
    za = -(P["steps_a"] + 1) * r
    i = min(P["steps_b"] - 1, max(0, int((s - 0.8) / tr)))
    return za - (i + 1) * r

def set_stair():
    S = "STAIR"
    SETS[S] = P["stair_origin"]
    C = coll("SET_2_STAIR (scene_refs/stair_v1.jpg)")
    w, r, tr = P["stair_w"], P["riser"], P["tread"]
    hw = w / 2
    na, nb = P["steps_a"], P["steps_b"]
    ya = na * tr                           # end of flight A (3.6)
    zc = -(na + 1) * r                     # corner landing
    xb = 0.8 + nb * tr                     # end of flight B (4.4)
    zb = zc - nb * r
    zbot = zb - 0.3
    bl(S, "landing_top", -hw, hw, -2.4, 0.0, zbot, 0.0, MATS["concrete"], C)
    for i in range(na):
        bl(S, f"step_A_{i:02d}", -hw, hw, i * tr, (i + 1) * tr, zbot, -(i + 1) * r, MATS["concrete"], C)
    bl(S, "landing_corner", -hw, hw, ya, ya + w, zbot, zc, MATS["concrete"], C)
    for i in range(nb):
        bl(S, f"step_B_{i:02d}", hw + i * tr, hw + (i + 1) * tr, ya, ya + w, zbot, zc - (i + 1) * r, MATS["concrete"], C)
    bl(S, "landing_bottom", xb, xb + 1.6, ya, ya + w, zbot, zb, MATS["concrete"], C)
    top = 2.8
    bl(S, "wall_left", -hw - 0.25, -hw, -2.4, ya + w + 0.25, zbot, top, MATS["concrete"], C)
    bl(S, "wall_right_inner", hw, hw + 0.25, -2.4, ya, zbot, top, MATS["concrete"], C)
    bl(S, "wall_inner_B", hw, xb + 1.6, ya - 0.25, ya, zbot, top, MATS["concrete"], C)
    bl(S, "wall_outer_B", -hw, xb + 1.6, ya + w, ya + w + 0.25, zbot, top, MATS["concrete"], C)
    bl(S, "wall_end_B", xb + 1.6, xb + 1.85, ya - 0.25, ya + w + 0.25, zbot, top, MATS["concrete"], C)
    bl(S, "wall_back_top", -hw - 0.25, hw + 0.25, -2.65, -2.4, 0.0, top, MATS["concrete"], C)
    bl(S, "door_from_corridor", -0.5, 0.5, -2.42, -2.38, 0.0, 2.1, MATS["steel"], C)
    bl(S, "ceiling", -hw - 0.25, xb + 1.85, -2.65, ya + w + 0.25, top, top + 0.2, MATS["concrete"], C, lid=True)
    # high wired window on the left wall at the turn (cold light source)
    bl(S, "window_left", -hw - 0.02, -hw + 0.02, ya - 0.9, ya + 0.3, zc + 2.2, zc + 3.6, MATS["window_light"], C)
    # frosted handrail on the right wall, sloping with flight A
    rail = box("handrail_A", L(S, hw - 0.06, ya / 2, -ya / 2 * r / tr + 0.9), (0.05, ya / math.cos(math.atan(r / tr)), 0.05), MATS["steel"], C)
    rail.rotation_euler = (-math.atan(r / tr), 0, 0)
    ref_cam(S, "ref_stair", C)

# --------------------------------------------------------------------------
# SET 3: freezer hall (hall_v1)
# --------------------------------------------------------------------------
def hall_doors():
    out, y = [], P["col_y0"] + P["col_step"] / 2
    while y < P["hall_len"] - 3:
        out.append(y)
        y += P["col_step"]
    return out

def set_hall():
    S = "HALL"
    SETS[S] = P["hall_origin"]
    C = coll("SET_3_FREEZER_HALL (scene_refs/hall_v1.jpg)")
    W, Ln, H = P["hall_w"], P["hall_len"], P["hall_h"]
    hw = W / 2
    bl(S, "floor", -hw, hw, -4.2, Ln, -0.2, 0.0, MATS["concrete"], C)
    bl(S, "ceiling", -hw - 0.2, hw + 0.2, -4.2, Ln + 0.2, H, H + 0.3, MATS["concrete"], C, lid=True)
    y = P["col_y0"]
    while y < Ln:
        bl(S, f"beam_{y:.0f}", -hw, hw, y - 0.2, y + 0.2, H - 0.45, H, MATS["concrete"], C, lid=True)
        for s in (-1, 1):
            bl(S, f"column_{s}_{y:.0f}", s * P["col_x"] - 0.3, s * P["col_x"] + 0.3, y - 0.3, y + 0.3, 0.0, H, MATS["concrete"], C)
        y += P["col_step"]
    bl(S, "end_wall", -hw, hw, Ln, Ln + 0.2, 0, H, MATS["frost"], C)
    bl(S, "end_fog", -hw, hw, Ln - 12.0, Ln, 0.0, 3.0, MATS["fog"], C)
    # south wall with the strip-curtain entrance, small anteroom behind it
    o = SETS[S]
    wall_x("south_wall", o[0] - hw, o[0] + hw, o[1] - 0.2, o[1], 0.0, H, [(o[0], 4.0, 0.0, 3.2)], MATS["frost"], C)
    curtain("curtain_entry", o[0], o[1] - 0.1, 4.0, "x", C, z0=0.0, z1=3.2)
    bl(S, "ante_wall_W", -2.4, -2.2, -4.2, -0.2, 0, 3.2, MATS["frost"], C)
    bl(S, "ante_wall_E", 2.2, 2.4, -4.2, -0.2, 0, 3.2, MATS["frost"], C)
    bl(S, "ante_wall_S", -2.4, 2.4, -4.4, -4.2, 0, 3.2, MATS["frost"], C)
    bl(S, "ante_ceiling", -2.4, 2.4, -4.4, -0.2, 3.2, 3.4, MATS["frost"], C, lid=True)
    # left wall: tall windows with sheer plastic curtains between the columns
    doors = hall_doors()
    wall_y("left_wall", o[0] - hw - 0.25, o[0] - hw, o[1], o[1] + Ln, 0.0, H, [(o[1] + yc, 3.6, 0.8, 5.2) for yc in doors], MATS["frost"], C)
    for yc in doors:
        bl(S, f"left_window_{yc:.1f}", -hw - 0.22, -hw - 0.18, yc - 1.8, yc + 1.8, 0.8, 5.2, MATS["window_light"], C)
        bl(S, f"left_sheer_{yc:.1f}", -hw + 0.1, -hw + 0.14, yc - 1.8, yc + 1.8, 0.4, 5.3, MATS["curtain"], C)
    # right wall: freezer doors between the columns, high windows above
    holes = [(o[1] + yc, 2.2, 0.0, 2.9) for yc in doors] + [(o[1] + yc, 1.4, 4.3, 5.4) for yc in doors]
    wall_y("right_wall", o[0] + hw, o[0] + hw + 0.25, o[1], o[1] + Ln, 0.0, H, holes, MATS["frost"], C)
    for k, yc in enumerate(doors):
        bl(S, f"right_highwin_{yc:.1f}", hw + 0.18, hw + 0.22, yc - 0.7, yc + 0.7, 4.3, 5.4, MATS["window_light"], C)
        if k == P["room4_door"]:
            d4 = bl(S, "ROOM4_door_MIRROR", hw - 0.14, hw - 0.04, yc - 1.1, yc + 1.1, 0.0, 2.9, MATS["mirror"], C)
            key(d4, "location", 0.0, d4.location.copy(), "CONSTANT")
        else:
            bl(S, f"freezer_door_{k + 1}", hw - 0.1, hw + 0.05, yc - 1.1, yc + 1.1, 0.0, 2.9, MATS["steel"], C)
        bl(S, f"door_back_void_{k}", hw + 0.3, hw + 0.4, yc - 1.1, yc + 1.1, 0.0, 2.9, MATS["void"], C)
    # hook rails both sides of the central aisle, ducts down the middle, pipe on the right
    for s in (-1, 1):
        x = s * P["rail_x"]
        bl(S, f"rail_{s}", x - 0.05, x + 0.05, 1.0, Ln - 2.0, P["rail_z"] - 0.06, P["rail_z"] + 0.06, MATS["steel"], C)
        yy, k = 1.3, 0
        while yy < Ln - 2.0:
            box(f"hook_{s}_{k:03d}", L(S, x, yy, P["rail_z"] - 0.5), (0.05, 0.05, 0.9), MATS["steel"], C)
            yy += P["hook_step"]
            k += 1
        bl(S, f"duct_{s}", s * 0.55 - 0.3, s * 0.55 + 0.3, 0.0, Ln, H - 0.75, H - 0.15, MATS["steel"], C)
    bl(S, "ammonia_pipe_right", hw - 1.2, hw - 0.95, 0.0, Ln, H - 0.95, H - 0.7, MATS["frost"], C)
    ref_cam(S, "ref_hall", C)

def curtain(name, cx, cy, width, axis, col, z0=0.0, z1=3.0):
    n = int(width / 0.26)
    for i in range(n):
        off = -width / 2 + (i + 0.5) * width / n
        j = 0.03 if i % 2 else -0.03
        if axis == "x":
            box(f"{name}_{i:02d}", (cx + off, cy + j, (z0 + z1) / 2), (0.24, 0.01, z1 - z0), MATS["curtain"], col)
        else:
            box(f"{name}_{i:02d}", (cx + j, cy + off, (z0 + z1) / 2), (0.01, 0.24, z1 - z0), MATS["curtain"], col)

# --------------------------------------------------------------------------
# SET 4: freezer room 4 (room4_v1)
# --------------------------------------------------------------------------
def set_room4():
    S = "ROOM4"
    SETS[S] = P["room4_origin"]
    C = coll("SET_4_ROOM4 (scene_refs/room4_v1.jpg)")
    W, D, H = P["room4"]
    hw = W / 2
    bl(S, "floor", -hw, hw + 2.0, -0.2, D, -0.2, 0.0, MATS["frost"], C)
    bl(S, "ceiling", -hw, hw, -0.2, D, H, H + 0.2, MATS["frost"], C, lid=True)
    bl(S, "wall_back", -hw, hw, D, D + 0.2, 0, H, MATS["frost"], C)
    bl(S, "wall_front", -hw, hw, -0.4, -0.2, 0, H, MATS["frost"], C)
    bl(S, "wall_left", -hw - 0.2, -hw, -0.4, D + 0.2, 0, H, MATS["frost"], C)
    o = SETS[S]
    dy = P["room4_door_y"]
    wall_y("wall_right", o[0] + hw, o[0] + hw + 0.2, o[1] - 0.4, o[1] + D + 0.2, 0.0, H, [(o[1] + dy, 1.1, 0.0, 2.3)], MATS["frost"], C)
    bl(S, "hall_beyond_glow", hw + 1.6, hw + 1.7, dy - 1.2, dy + 1.2, 0.0, 3.0, MATS["hall_glow"], C)
    door = bl(S, "sliding_door_MIRROR", hw - 0.16, hw - 0.06, dy - 2.75, dy - 0.55, 0.0, 2.45, MATS["mirror"], C)
    door["note"] = "slid open towards the camera, as in the scene image"
    bl(S, "door_rail", hw - 0.1, hw - 0.04, dy - 2.9, dy + 0.7, 2.55, 2.65, MATS["steel"], C)
    # crates: front-left open crate, the tall stack that hides the gap, the pallets
    bl(S, "crate_front", -hw + 0.05, -0.75, 0.9, 2.1, 0.0, 1.2, MATS["crate"], C)
    bl(S, "crate_stack_tall", -hw + 0.05, -0.7, 2.4, 3.2, 0.0, 1.75, MATS["crate"], C)
    bl(S, "pallet_stack", -0.2, 1.0, 3.5, 4.5, 0.0, 1.1, MATS["crate"], C)
    box("hook_ceiling_back", L(S, 0.4, 5.6, H - 0.25), (0.04, 0.04, 0.5), MATS["steel"], C)
    box("hook_ceiling_front", L(S, 0.35, 1.6, H - 0.2), (0.04, 0.04, 0.4), MATS["steel"], C)
    ref_cam(S, "ref_room4", C)

# --------------------------------------------------------------------------
# SET 5: interview room (interview_v1); SET 6: evidence room (evidence_v2)
# --------------------------------------------------------------------------
def set_interview():
    S = "INT"
    SETS[S] = P["int_origin"]
    C = coll("SET_5_INTERVIEW (scene_refs/interview_v1.jpg)")
    W, D, H = P["int_room"]
    hw = W / 2
    bl(S, "floor", -hw, hw, -0.2, D, -0.1, 0.0, MATS["concrete"], C)
    bl(S, "ceiling", -hw, hw, -0.2, D, H, H + 0.1, MATS["clay"], C, lid=True)
    bl(S, "wall_left", -hw - 0.2, -hw, -0.2, D + 0.2, 0, H, MATS["clay"], C)
    bl(S, "wall_right", hw, hw + 0.2, -0.2, D + 0.2, 0, H, MATS["clay"], C)
    bl(S, "wall_front", -hw, hw, -0.4, -0.2, 0, H, MATS["clay"], C)
    o = SETS[S]
    wall_x("wall_back", o[0] - hw, o[0] + hw, o[1] + D, o[1] + D + 0.2, 0.0, H, [(o[0] + 1.05, 0.9, 0.0, 2.1)], MATS["clay"], C)
    bl(S, "door", 0.6, 1.5, D + 0.05, D + 0.1, 0.0, 2.1, MATS["clay_dark"], C)
    bl(S, "oneway_mirror", -hw, -hw + 0.04, 1.0, 3.9, 0.9, 2.0, MATS["oneway"], C)
    bl(S, "light_panel", -0.6, 0.6, 1.4, 2.6, H - 0.04, H, MATS["panel_light"], C)
    bl(S, "table_top", -0.4, 0.4, 2.45, 3.75, 0.70, 0.74, MATS["steel"], C)
    for x, y in ((-0.35, 2.5), (0.35, 2.5), (-0.35, 3.7), (0.35, 3.7)):
        bl(S, f"table_leg_{x}_{y}", x - 0.02, x + 0.02, y - 0.02, y + 0.02, 0.0, 0.70, MATS["steel"], C)
    for nm, x, back in (("nora", -0.75, -0.97), ("ward", 0.75, 0.97)):
        y = 2.95 if nm == "nora" else 3.25
        bl(S, f"chair_{nm}_seat", x - 0.2, x + 0.2, y - 0.2, y + 0.2, 0.42, 0.46, MATS["clay_dark"], C)
        bl(S, f"chair_{nm}_back", back - 0.03, back + 0.03, y - 0.2, y + 0.2, 0.46, 0.92, MATS["clay_dark"], C)
    ref_cam(S, "ref_int", C)

def set_evidence():
    S = "EV"
    SETS[S] = P["ev_origin"]
    C = coll("SET_6_EVIDENCE (scene_refs/evidence_v2.jpg)")
    W, D, H = P["ev_room"]
    hw = W / 2
    bl(S, "floor", -hw, hw, -1.0, D, -0.1, 0.0, MATS["concrete"], C)
    bl(S, "ceiling", -hw, hw, -1.0, D, H, H + 0.1, MATS["clay"], C, lid=True)
    for nm, r in (("left", (-hw - 0.2, -hw, -1.0, D)), ("right", (hw, hw + 0.2, -1.0, D)), ("front", (-hw, hw, -1.2, -1.0))):
        bl(S, f"wall_{nm}", *r, 0, H, MATS["clay"], C)
    o = SETS[S]
    wall_x("wall_back", o[0] - hw, o[0] + hw, o[1] + D, o[1] + D + 0.2, 0.0, H, [(o[0] - 1.5, 0.9, 0.0, 2.1), (o[0] - 0.15, 0.9, 0.0, 2.1)], MATS["clay"], C)
    for k in range(3):
        bl(S, f"led_{k}", -0.6 + k * 1.2 - 0.4, -0.6 + k * 1.2 + 0.4, 1.5 + k * 2.6, 2.7 + k * 2.6, H - 0.04, H, MATS["panel_light"], C)
    bl(S, "table", 0.2, 1.2, 0.8, 7.6, 0.86, 0.90, MATS["steel"], C)
    for y in (1.0, 7.4):
        bl(S, f"table_leg_{y}", 0.3, 1.1, y - 0.05, y + 0.05, 0.0, 0.86, MATS["steel"], C)
    bl(S, "counter_left", -hw + 0.05, -1.75, 0.4, 5.0, 0.0, 0.95, MATS["steel"], C)
    bl(S, "shelving_back", 0.4, hw - 0.05, D - 0.55, D - 0.05, 0.0, 2.2, MATS["clay_dark"], C)
    for i in range(13):  # bag 13 (red tag) is the NEAREST, as in the scene image
        y = 1.2 + (12 - i) * 0.5
        n = i + 1
        bl(S, f"bag_{n:02d}", 0.55, 0.85, y - 0.19, y + 0.19, 0.90, 0.93, MATS["bag"], C)
        bl(S, f"bodycam_{n:02d}", 0.64, 0.76, y - 0.05, y + 0.05, 0.905, 0.96, MATS["bodycam"], C)
        bl(S, f"tag_{n:02d}", 0.86, 0.95, y - 0.04, y + 0.04, 0.90, 0.905, MATS["tag_red" if n == 13 else "tag_white"], C)
    bl(S, "EX47_rec_light", 0.69, 0.71, 1.135, 1.145, 0.95, 0.962, MATS["rec_red"], C)
    ref_cam(S, "ref_ev", C)

# --------------------------------------------------------------------------
# shots: times are master-timeline seconds from the 89 s shot list
# --------------------------------------------------------------------------
def build_shots():
    CH = 1.35  # chest-mounted camera height
    E = lambda x, y, z=0.0: L("EXT", x, y, z)
    H_ = lambda x, y, z=0.0: L("HALL", x, y, z)
    R4 = lambda x, y, z=0.0: L("ROOM4", x, y, z)
    I = lambda x, y, z=0.0: L("INT", x, y, z)
    V = lambda x, y, z=0.0: L("EV", x, y, z)
    ST = lambda x, y, z=0.0: L("STAIR", x, y, z)
    gy, gx = P["gate_y"], P["gate_x"]
    bx = P["bay_x"]

    # ---- 02 D1 drone: Nora walks out of the open bay alone (2.0-6.0)
    C = coll("SHOT_02_D1")
    start, end = E(bx, -1.2), E(bx + 0.4, -6.8)
    nora, _ = person("D1_nora", "nora", start, heading(0, -1), C, tag="NORA (helmet in hand)")
    move(nora, 2.0, start); move(nora, 6.0, end)
    p, k = E(bx, -0.1), 0
    step = (end - E(bx, -0.1)).normalized() * 0.36
    while (p - end).length > 0.3:
        fp = box(f"D1_footprint_{k:02d}", (p.x + (0.12 if k % 2 else -0.12), p.y, p.z + 0.01), (0.12, 0.28, 0.02), MATS["footprint"], C)
        u = max(0.0, (start.y - p.y) / (start.y - end.y))
        interp("CONSTANT")
        fp.scale = TINY; ins(fp, "scale", 1)
        fp.scale = (0.12, 0.28, 0.02); ins(fp, "scale", fr(2.0 + 4.0 * min(1.0, u)))
        fp.scale = TINY; ins(fp, "scale", fr(6.0))
        p = p + step
        k += 1
    ev("02", 2.0, "Nora is 1 m out of the bay; one line of footprints behind her; she walks 5.6 m towards the gate in 4 s")
    cam = camera("CAM_02_D1_drone", 24, C)
    cam_keys(cam, 2.0, 6.0, lambda u, t: (lerp(E(bx + 0.2, -4.2, 38.0), E(bx + 0.2, -4.8, 38.0), u), lerp(E(bx + 0.2, -4.2), E(bx + 0.2, -4.8), u), 0.0))
    shot("02", "D1", 2.0, 4.0, cam, "LOC-GATE", "S-DRONE", "D1", [nora],
         "ALT 38 m, north up: the gate sits on the bottom edge, the facade and roof fill the top third, Nora is the only mark in the middle.")

    # ---- 04 C3 CCTV: two vans pull up at the gate (7.5-11.5)
    C = coll("SHOT_04_C3")
    v1, d1 = van("C3_van_1", C)
    v2, d2 = van("C3_van_2", C)
    for v, xa, ya, yb, t_stop in ((v1, gx - 1.3, -80, gy - 4.3, 9.0), (v2, gx + 1.4, -88, gy - 11.0, 9.4)):
        v.location = E(xa, ya)
        move(v, 7.5, E(xa, ya)); move(v, t_stop, E(xa, yb), "BEZIER")
    for dd in (d1, d2):
        key(dd, "location", 9.6, dd.location.copy()); key(dd, "location", 10.0, dd.location + Vector((0, -1.3, 0)))
    team = []
    for i in range(5):
        o, _ = person(f"C3_officer_{i + 1}", "officer", E(gx - 0.2, gy - 4.4), heading(0, 1), C, pose="rifle", tag=f"7-0{i + 1}")
        t_out = 9.8 + i * 0.3
        move(o, 7.5, E(gx - 0.2, gy - 4.4), "CONSTANT")
        move(o, t_out, E(gx - 0.2, gy - 4.4)); move(o, t_out + 0.4, E(gx + 0.8, gy - 4.1))
        move(o, 11.5, E(gx + 0.6 + (i % 2) * 0.7 - 0.35, gy - 1.0 - i * 0.65))
        team.append(o)
    ev("04", 9.0, "van 1 stops outside the closed gate; 9.4 van 2 stops behind it")
    ev("04", 9.6, "side doors open; from 9.8 one officer every 0.3 s climbs out and stacks at the gate")
    cam = camera("CAM_04_C3_cctv", 18, C)
    cam_keys(cam, 7.5, 11.5, lambda u, t: (E(-1.3, -0.5, 5.6), E(gx, gy - 4.0, 0.0), 0.0))
    shot("04", "C3", 7.5, 4.0, cam, "LOC-GATE", "S-CCTV", "C3", [v1, v2] + team,
         "CCTV on the facade beside the bay canopy, 12 mm. Gate ~20 m away: vans read clearly in the centre third, the empty yard fills the lower half.")

    # ---- 05 B1 bodycam: two officers ram the personnel door (11.5-14.0)
    C = coll("SHOT_05_B1")
    dx = P["door_x"]
    o1, _ = person("B1_ram_1", "officer", E(dx - 0.2, -1.5), heading(0, 1), C, pose="rifle", tag="7-01 ram")
    o2, _ = person("B1_ram_2", "officer", E(dx + 0.5, -2.2), heading(0, 1), C, pose="rifle", tag="7-02")
    me, _ = person("B1_wearer_7-04", "officer", E(dx, -3.6), heading(0, 1), C, pose="rifle", wearer=True, tag="7-04 (camera)")
    for o, a, b in ((o1, -1.5, -0.55), (o2, -2.2, -1.2)):
        x = o.location.x - SETS["EXT"][0]
        move(o, 11.5, E(x, a)); move(o, 12.1, E(x, b), "BEZIER"); move(o, 14.0, E(x, 1.8))
    hinge = bpy.data.objects["door_hinge"]
    key(hinge, "rotation_euler", 12.1, (0, 0, 0)); key(hinge, "rotation_euler", 12.4, (0, 0, 1.75), "BEZIER")
    move(me, 11.5, E(dx, -3.6)); move(me, 14.0, E(dx + 0.1, -0.6))
    ev("05", 12.1, "the ram hits; the door swings in over 0.3 s; 12.4 the stack pours in")
    cam = camera("CAM_05_B1_bodycam", 14, C)
    cam_keys(cam, 11.5, 14.0, lambda u, t: (lerp(E(dx, -3.42, CH), E(dx + 0.1, -0.42, CH), u), lerp(E(dx, 3.0, 1.2), E(dx + 0.1, 6.0, 1.1), u), 0.0), shake_amp=0.035, seed=5)
    shot("05", "B1", 11.5, 2.5, cam, "LOC-GATE", "S-BCAM", "B1", [o1, o2, me])

    # ---- 07 I1 interview CCTV: Nora alone, the investigator never in frame (15.5-18.5)
    C = coll("SHOT_07_I1")
    nora_i1, _ = person("I1_nora", "nora_room", I(-0.75, 2.95), heading(1, 0), C, pose="sit", tag="NORA")
    ward_i1, _ = person("I1_WARD_offscreen", "ward", I(-1.35, 0.35), heading(1, 1), C, tag="WARD (must stay out of frame)")
    cam = camera("CAM_07_I1_cctv", 16, C)
    cam_keys(cam, 15.5, 18.5, lambda u, t: (I(0.9, 0.15, 2.3), I(-0.3, 3.5, 0.65), 0.0))
    shot("07", "I1", 15.5, 3.0, cam, "LOC-INTERVIEW", "S-ROOM", "I1", [nora_i1, ward_i1],
         "Same corner as the scene image. Nora on the mirror side facing the empty chair; Ward stands in the front-left corner, behind the lens.")

    # ---- 09 E1 evidence push-in from the far end to bag 13 (20.0-23.0)
    C = coll("SHOT_09_E1")
    b13 = V(0.7, 1.2, 0.93)
    cam = camera("CAM_09_E1_push", 35, C)
    cam_keys(cam, 20.0, 23.0, lambda u, t: (lerp(V(0.75, 8.8, 1.35), V(0.72, 2.05, 1.1), ease(u)), lerp(V(0.7, 1.2, 0.8), b13, ease(u)), 0.0))
    ev("09", 22.6, "push-in settles on bag 13, the red tag (the bag nearest the room door in the scene image)")
    shot("09", "E1", 20.0, 3.0, cam, "LOC-EVIDENCE", "S-ROOM", "E1", [],
         "The scene image put the red tag on the nearest bag, so the push runs from the far end back towards it.")

    # ---- 10 B2 stairwell count-off, swing to the 13th (23.0-27.0)
    C = coll("SHOT_10_B2")
    zc = -(P["steps_a"] + 1) * P["riser"]
    slots = [("A", 0.0, 1.0), ("A", 0.0, 2.0), ("A", 0.0, 3.0), ("C", -0.3, 4.1), ("C", 0.4, 4.6),
             ("B", 1.1, 4.4), ("B", 1.9, 4.4), ("B", 2.7, 4.4), ("B", 3.5, 4.4), ("B", 4.3, 4.4), ("B", 5.0, 4.4)]
    officers = []
    for k, (lane, x, y) in enumerate(slots):
        num = 11 - k
        z = zc if lane == "C" else stair_z(lane, y if lane == "A" else x)
        face = heading(0, 1) if lane == "A" else heading(1, 0)
        o, parts = person(f"B2_officer_{num:02d}", "officer", ST(x, y), face, C, pose="rifle", tag=f"7-{num:02d}", z=SETS["STAIR"][2] + z)
        officers.append(o)
        if num >= 8:
            tt = 23.3 + (num - 8) * 0.3
            arm(parts, "l", tt, (1.25, 0, -0.35)); arm(parts, "l", tt + 0.12, (1.7, 0, 0)); arm(parts, "l", tt + 0.35, (1.25, 0, -0.35))
    ny = -0.3
    nz = 0.0
    nora, _ = person("B2_nora_7-12_wearer", "nora", ST(0.0, ny), heading(0, 1), C, pose="rifle", wearer=True, tag="NORA 7-12 (camera)", z=nz)
    th, _ = person("B2_THIRTEENTH_7-12", "thirteenth", ST(0.0, -1.45), heading(0, 1), C, tag="13TH 7-12", z=0.0)
    ev("10", 23.3, "count-off reaches the visible men: 7-08 taps at 23.3 ... 7-11 at 24.2; the line turns right out of sight after 7-07")
    ev("10", 24.4, "Nora: 'Twelve.' (V7)"); ev("10", 25.2, "the 13th: 'Twelve.' (V8); he does not move")
    ev("10", 25.0, "swing starts; 25.6 the camera lands on the 13th, one step up on the landing; hold to 27.0")
    def b2(u, t):
        a = 0.0 if t < 25.0 else (math.pi if t > 25.6 else math.pi * ease((t - 25.0) / 0.6))
        yaw = heading(0, 1) + a
        fwd = Vector((-math.sin(yaw), math.cos(yaw), 0))
        loc = ST(0.0, ny, nz + CH) + fwd * 0.18
        pitch = -0.42 if t < 25.0 else (-0.42 + 0.5 * ease(min(1, (t - 25.0) / 0.6)))
        return loc, loc + fwd * 3.0 + Vector((0, 0, math.tan(pitch) * 3.0)), 0.0
    key(nora, "rotation_euler", 25.0, (0, 0, heading(0, 1))); key(nora, "rotation_euler", 25.6, (0, 0, heading(0, 1) + math.pi), "BEZIER")
    cam = camera("CAM_10_B2_bodycam_nora", 14, C)
    cam_keys(cam, 23.0, 27.0, b2, shake_amp=0.02, seed=10)
    shot("10", "B2", 23.0, 4.0, cam, "LOC-STAIR", "S-BCAM", "B2", officers + [nora, th],
         "13TH APPEARANCE #1. Before the swing the frame matches the scene image. The montage (22) may only use frames before 25.0.")

    # ---- 13 B3 through the entry curtain into the hall (30.5-33.5)
    C = coll("SHOT_13_B3")
    a1, _ = person("B3_officer_a", "officer", H_(-0.8, 3.0), heading(0, 1), C, pose="rifle", tag="7-02")
    a2, _ = person("B3_officer_b", "officer", H_(0.9, 5.0), heading(0, 1), C, pose="rifle", tag="7-03")
    for o, ph in ((a1, 0.0), (a2, 0.7)):
        for i in range(7):
            turn(o, 30.5 + i * 0.5, heading(0, 1) + math.sin(i * 1.3 + ph) * 0.5, "BEZIER")
        move(o, 30.5, o.location.copy()); move(o, 33.5, o.location + Vector((0, 2.2, 0)))
    me, _ = person("B3_wearer_7-04", "officer", H_(0.0, -3.0), heading(0, 1), C, pose="rifle", wearer=True, tag="7-04 (camera)")
    move(me, 30.5, H_(0.0, -3.0)); move(me, 33.5, H_(0.0, 1.2))
    cam = camera("CAM_13_B3_bodycam", 14, C)
    cam_keys(cam, 30.5, 33.5, lambda u, t: (lerp(H_(0.0, -2.82, CH), H_(0.0, 1.38, CH), u), lerp(H_(0.0, 6.0, 1.2), H_(0.0, 10.0, 1.3), u), 0.0), shake_amp=0.03, seed=13)
    ev("13", 31.6, "camera breaks through the strip curtain (y 0); the hall and the hook rails open up")
    shot("13", "B3", 30.5, 3.0, cam, "LOC-FREEZER", "S-BCAM", "B3", [a1, a2, me], "No 13th in frame.")

    # ---- 15 B4 masks off; Brandt yanks the camera (35.0-37.5)
    C = coll("SHOT_15_B4")
    cen = H_(-1.0, 14.0)
    ring = []
    for i, ang in enumerate((-2.2, -1.3, 0.4, 1.3, 2.2)):
        pos = cen + Vector((math.sin(ang) * 1.5, math.cos(ang) * 1.5, 0))
        o, pp = person(f"B4_officer_{i + 1}", "officer", pos, heading(cen.x - pos.x, cen.y - pos.y), C, pose="rifle", tag=f"7-0{i + 5}")
        tt = 35.2 + i * 0.15
        arm(pp, "r", tt, (1.15, 0, 0)); arm(pp, "r", tt + 0.3, (2.9, 0, 0.3)); arm(pp, "r", tt + 0.7, (1.4, 0, 0))
        ring.append(o)
    br, bp = person("B4_BRANDT_7-01", "brandt", cen + Vector((0, 0.9, 0)), heading(0, -1), C, tag="BRANDT 7-01")
    move(br, 35.0, br.location.copy()); move(br, 36.2, br.location.copy()); move(br, 36.5, cen + Vector((0, -1.0, 0)), "BEZIER")
    arm(bp, "r", 36.2, (0.1, 0, 0)); arm(bp, "r", 36.45, (1.45, 0, 0))
    me, _ = person("B4_wearer_7-06", "officer", cen + Vector((0, -1.6, 0)), heading(0, 1), C, pose="rifle", wearer=True)
    ev("15", 35.2, "masks come off around the ring, one every 0.15 s")
    ev("15", 36.2, "Brandt lunges; 36.5 he has the wearer by the vest, his face 0.6 m from the lens")
    def b4(u, t):
        y = ease(max(0.0, min(1.0, (t - 36.3) / 0.25)))
        loc = cen + Vector((0, -1.42, CH)) + Vector((0, 0.18, 0.08)) * y
        return loc, cen + Vector((0, 1.0, 1.45 + 0.1 * y)), 0.0
    cam = camera("CAM_15_B4_bodycam", 14, C)
    cam_keys(cam, 35.0, 37.5, b4, shake_amp=0.05, seed=15)
    shot("15", "B4", 35.0, 2.5, cam, "LOC-FREEZER", "S-BCAM", "B4", ring + [br, me])

    # ---- 17 O2 three years ago: they switch their cameras off (39.0-41.5)
    C = coll("SHOT_17_O2")
    line = []
    for i in range(6):
        pos = H_(-2.4 + i * 0.95, 30.0 + abs(i - 2.5) * 0.35)
        role = "brandt" if i == 2 else "officer_past"
        o, pp = person(f"O2_past_{i + 1}", role, pos, heading(0.35 if i < 3 else -0.35, 1), C, tag="BRANDT (past)" if i == 2 else f"past 7-{i + 1:02d}")
        tt = 39.35 + i * 0.3
        arm(pp, "r", tt, (0.08, 0, 0)); arm(pp, "r", tt + 0.2, (1.9, 0, 0.9)); arm(pp, "r", tt + 0.5, (0.3, 0, 0))
        rec = bpy.data.objects[f"O2_past_{i + 1}_rec"]
        interp("CONSTANT")
        rec.scale = (0.02, 0.01, 0.02); ins(rec, "scale", 1)
        rec.scale = TINY; ins(rec, "scale", fr(tt + 0.2))
        line.append(o)
    ev("17", 39.35, "first red light goes dark; one more every 0.3 s; the last at 40.85")
    cam = camera("CAM_17_O2_bodycam_reyes", 14, C)
    cam_keys(cam, 39.0, 41.5, lambda u, t: (H_(0.0, 26.5, CH), H_(0.0, 31.0, 1.2), 0.0), shake_amp=0.006, seed=17)
    shot("17", "O2", 39.0, 2.5, cam, "LOC-FREEZER (3 years ago)", "S-OLD", "O2", line,
         "Reyes's camera, the one that stays on: almost no shake. Ward is not in this line.")

    # ---- 19a B5 muzzle flashes down the aisle (43.5-44.5)
    C = coll("SHOT_19a_B5")
    sh = []
    for i, (x, y) in enumerate(((-0.6, 12.0), (1.2, 15.0), (-0.3, 18.0))):
        o, pp = person(f"B5_officer_{i + 1}", "officer", H_(x, y), heading(0.15 * (i - 1), 1), C, pose="rifle")
        flash(pp["muzzle"], [43.55 + i * 0.13 + k * 0.33 for k in range(3)])
        sh.append(o)
    cam = camera("CAM_19a_B5_bodycam", 14, C)
    cam_keys(cam, 43.5, 44.5, lambda u, t: (H_(0.0, 8.0, CH), H_(0.0, 18.0, 1.2), 0.0), shake_amp=0.05, seed=19)
    ev("19a", 43.55, "9 pops between 43.55 and 44.5; the hooks and silhouettes only exist in the flashes")
    shot("19a", "B5", 43.5, 1.0, cam, "LOC-FREEZER", "S-BCAM", "B5", sh)

    # ---- 19b B9 shooting through the entry curtain (44.5-45.5)
    C = coll("SHOT_19b_B9")
    tgt, _ = person("B9_silhouette_own_man", "officer", H_(-1.6, 1.4), heading(1, 0), C, pose="rifle", tag="7-08 (hit)")
    move(tgt, 44.5, H_(-1.6, 1.4)); move(tgt, 44.85, H_(0.3, 1.4))
    turn(tgt, 44.85, heading(1, 0)); turn(tgt, 45.15, heading(1, 0), tilt=-1.45)
    torch = box("B9_torch", H_(0.5, 1.6, 1.2), (0.08, 0.2, 0.08), MATS["torch"], C)
    key(torch, "location", 44.85, H_(0.5, 1.6, 1.2)); key(torch, "location", 45.1, H_(0.4, 1.1, 0.05)); key(torch, "location", 45.5, H_(0.2, 0.35, 0.05))
    key(torch, "rotation_euler", 44.85, (0, 0, 0)); key(torch, "rotation_euler", 45.5, (0, 0, 2.6))
    window(torch, 44.5, 45.5)
    me, mp = person("B9_wearer", "officer", H_(0.2, -2.6), heading(0, 1), C, pose="rifle", wearer=True)
    flash(mp["muzzle"], [44.72, 44.84])
    mp["muzzle"].visible_camera = True
    ev("19b", 44.72, "two shots through the curtain (44.72, 44.84); 44.9 the figure drops; the torch rolls back to the curtain by 45.5")
    cam = camera("CAM_19b_B9_bodycam", 14, C)
    cam_keys(cam, 44.5, 45.5, lambda u, t: (H_(0.2, -2.42, CH), H_(0.0, 3.0, 1.1), 0.0), shake_amp=0.06, seed=191)
    shot("19b", "B9", 44.5, 1.0, cam, "LOC-FREEZER", "S-BCAM", "B9", [tgt, me])

    # ---- 19c C1 CCTV crossfire (45.5-46.5)
    C = coll("SHOT_19c_C1")
    pts = [(-3.5, 30, 3), (-1.0, 34, 4), (2.0, 27, 0), (3.5, 36, 1), (0.5, 22, 5), (-2.5, 25, 2)]
    grp = []
    for i, (x, y, j) in enumerate(pts):
        tx_, ty_ = pts[j][0], pts[j][1]
        o, pp = person(f"C1_officer_{i + 1}", "officer", H_(x, y), heading(tx_ - x, ty_ - y), C, pose="rifle")
        flash(pp["muzzle"], [45.55 + 0.11 * i + 0.3 * k for k in range(3)])
        grp.append(o)
    turn(grp[3], 45.95, grp[3].rotation_euler.z); turn(grp[3], 46.25, grp[3].rotation_euler.z, tilt=1.4)
    cam = camera("CAM_19c_C1_cctv", 12, C)
    cam_keys(cam, 45.5, 46.5, lambda u, t: (H_(-4.4, 46.8, 5.2), H_(1.0, 29.0, 0.0), 0.0))
    ev("19c", 45.95, "one silhouette (C1_officer_4) falls")
    shot("19c", "C1", 45.5, 1.0, cam, "LOC-FREEZER", "S-CCTV", "C1", grp)

    # ---- 19d B10 flashbang (46.5-47.5)
    C = coll("SHOT_19d_B10")
    st = []
    for i, (x, y) in enumerate(((-0.8, 28.5), (1.0, 30.0))):
        o, _ = person(f"B10_officer_{i + 1}", "officer", H_(x, y), heading(0, -1), C)
        move(o, 46.5, H_(x, y)); move(o, 47.0, H_(x + 0.3, y - 0.2)); move(o, 47.5, H_(x - 0.2, y + 0.3))
        st.append(o)
    fb = box("B10_flashbang_burst", H_(0.0, 27.5, 0.4), (0.2, 0.2, 0.2), MATS["flashbang"], C)
    interp("CONSTANT"); fb.scale = TINY; ins(fb, "scale", 1)
    for tt, s in ((46.6, 0.3), (46.65, 7.0), (47.25, 7.0)):
        interp("LINEAR"); fb.scale = (s, s, s); ins(fb, "scale", fr(tt))
    interp("CONSTANT"); fb.scale = TINY; ins(fb, "scale", fr(47.3))
    cam = camera("CAM_19d_B10_bodycam", 14, C)
    cam_keys(cam, 46.5, 47.5, lambda u, t: (H_(0.0, 24.0, CH), H_(0.0, 30.0, 1.1), 0.0), shake_amp=0.07, seed=194)
    ev("19d", 46.62, "white-out (full frame by 46.65); exposure crawls back from 47.25")
    shot("19d", "B10", 46.5, 1.0, cam, "LOC-FREEZER", "S-BCAM", "B10", st)

    # ---- 19e B6 ammonia pipe bursts (47.5-48.5)
    C = coll("SHOT_19e_B6")
    pp_ = H_(P["hall_w"] / 2 - 1.08, 33.0, P["hall_h"] - 0.82)
    jet = box("B6_gas_jet", pp_, (0.3, 0.3, 0.1), MATS["gas"], C)
    interp("CONSTANT"); jet.scale = TINY; ins(jet, "scale", 1)
    for tt, (sx, sz, zc_) in ((47.72, (0.3, 0.2, pp_.z - 0.1)), (48.1, (1.6, 4.6, pp_.z - 2.3)), (48.5, (3.5, 5.2, pp_.z - 2.6))):
        interp("LINEAR"); jet.scale = (sx, sx, sz); jet.location = (pp_.x, pp_.y, zc_)
        ins(jet, "scale", fr(tt)); ins(jet, "location", fr(tt))
    of, _ = person("B6_officer", "officer", H_(4.4, 32.3), heading(0, -1), C, pose="rifle")
    move(of, 47.9, H_(4.4, 32.3)); move(of, 48.5, H_(4.0, 31.2)); turn(of, 47.9, heading(0, -1)); turn(of, 48.5, heading(0, -1), tilt=0.35)
    cam = camera("CAM_19e_B6_bodycam", 14, C)
    cam_keys(cam, 47.5, 48.5, lambda u, t: (H_(2.4, 29.5, CH), pp_ + Vector((0, 0, -0.9)), 0.0), shake_amp=0.05, seed=195)
    ev("19e", 47.72, "bullet hits the pipe on the right wall; gas reaches the floor by 48.1; the officer backs into it")
    shot("19e", "B6", 47.5, 1.0, cam, "LOC-FREEZER", "S-BCAM", "B6", [of])

    # ---- 19g B7 "We buried you!" (49.5-51.0)
    C = coll("SHOT_19g_B7")
    br7, bp7 = person("B7_BRANDT", "brandt", H_(-2.0, 38.0), heading(0, -1), C, tag="BRANDT")
    key(bp7["head"], "rotation_euler", 49.5, (0, 0, 0.35)); key(bp7["head"], "rotation_euler", 50.3, (0.15, 0, 0.45))
    cam = camera("CAM_19g_B7_bodycam", 14, C)
    cam_keys(cam, 49.5, 51.0, lambda u, t: (H_(-2.0, 37.0, 1.25), H_(-2.0, 38.0, 1.75), 0.0), shake_amp=0.045, seed=197)
    ev("19g", 49.7, "Brandt screams past the lens (head turned ~20 deg), lit from below")
    shot("19g", "B7", 49.5, 1.5, cam, "LOC-FREEZER", "S-BCAM", "B7", [br7])

    # ---- 19h X1 EX47 POV: calm through the gas (51.0-52.5)
    C = coll("SHOT_19h_X1")
    fog = box("X1_fog", H_(0.0, 43.0, 0.35), (13.0, 12.0, 0.7), MATS["fog"], C)
    window(fog, 51.0, 52.5)
    f1, _ = person("X1_officer_falls", "officer", H_(0.9, 42.6), heading(0, -1), C)
    turn(f1, 51.5, heading(0, -1)); turn(f1, 52.0, heading(0, -1), tilt=1.3)
    f2, fp2 = person("X1_officer_fires", "officer", H_(-1.6, 43.4), heading(-1, 0.2), C, pose="rifle")
    flash(fp2["muzzle"], [51.2, 51.6, 52.0])
    f3, _ = person("X1_officer_spins", "officer", H_(1.4, 41.0), heading(1, 0), C, pose="rifle")
    for i in range(6):
        turn(f3, 51.0 + i * 0.25, heading(1, 0) + (1.2 if i % 2 else -1.2), "BEZIER")
    me, _ = person("X1_wearer_THIRTEENTH", "thirteenth", H_(0.0, 39.0), heading(0, 1), C, wearer=True)
    move(me, 51.0, H_(0.0, 39.0)); move(me, 52.5, H_(0.0, 41.0))
    cam = camera("CAM_19h_X1_ex47", 14, C)
    cam_keys(cam, 51.0, 52.5, lambda u, t: (lerp(H_(0.0, 39.18, CH), H_(0.0, 41.18, CH), u), lerp(H_(0.0, 45.0, 1.25), H_(0.0, 47.0, 1.25), u), 0.0))
    ev("19h", 51.0, "steady 1.33 m/s glide, no shake, no turn; 51.5 an officer falls; 51.2/51.6/52.0 blind shots")
    shot("19h", "X1", 51.0, 1.5, cam, "LOC-FREEZER", "S-BCAM steady", "X1", [f1, f2, f3, me, fog], "The only steady image in the film.")

    # ---- 19i B8 mirror door of room 4: the reflection is the 13th (52.5-54.0)
    C = coll("SHOT_19i_B8")
    yd = hall_doors()[P["room4_door"]]
    me, mpp = person("B8_wearer_THIRTEENTH_7-12", "thirteenth", H_(4.4, yd - 2.4), heading(0, 1), C, wearer=True, tag="13TH (seen only in the mirror)")
    move(me, 52.5, H_(4.4, yd - 2.4)); move(me, 54.0, H_(4.4, yd - 0.4))
    key(mpp["head"], "rotation_euler", 53.3, (0, 0, 0)); key(mpp["head"], "rotation_euler", 53.6, (0, 0, -0.35), "BEZIER")
    cam = camera("CAM_19i_B8_ex47", 14, C)
    def b8(u, t):
        loc = H_(4.4, yd - 2.4 + 2.0 * u + 0.18, CH)
        yaw = 0.45 + 0.85 * ease(max(0.0, min(1.0, (t - 52.8) / 0.6)))
        return loc, loc + Vector((math.sin(yaw), math.cos(yaw), -0.08)), 0.0
    turn(me, 52.8, heading(0, 1)); turn(me, 53.4, heading(0, 1) - 0.85, "BEZIER")
    cam_keys(cam, 52.5, 54.0, b8)
    ev("19i", 52.8, "the wearer turns ~70 deg towards the mirror door (52.8-53.4); his reflection enters frame ~53.6 and turns its head")
    shot("19i", "B8", 52.5, 1.5, cam, "LOC-FREEZER (room 4 door)", "S-BCAM steady", "B8", [me],
         "13TH APPEARANCE #2: only as a reflection. The wearer is invisible to the camera but visible in the mirror.")

    # ---- 21 C2 room 4 CCTV: the scarred hand pulls Nora behind the crates (58.0-62.5)
    C = coll("SHOT_21_C2")
    hw4 = P["room4"][0] / 2
    dy4 = P["room4_door_y"]
    nora_c2, _ = person("C2_nora", "nora", R4(hw4 + 0.9, dy4), heading(-1, 0), C, tag="NORA")
    move(nora_c2, 58.0, R4(hw4 + 0.9, dy4)); move(nora_c2, 58.3, R4(hw4 + 0.9, dy4))
    move(nora_c2, 59.4, R4(0.9, 3.4), "BEZIER"); move(nora_c2, 60.2, R4(-0.3, 3.3))
    move(nora_c2, 60.5, R4(-0.6, 3.35)); move(nora_c2, 61.5, R4(-1.55, 3.5, -1.0), "BEZIER")
    turn(nora_c2, 59.4, heading(-1, 0)); turn(nora_c2, 60.2, heading(-1, 0.3)); turn(nora_c2, 61.5, heading(-1, 0.3), tilt=0.5)
    th2, thp2 = person("C2_THIRTEENTH_hidden", "thirteenth", R4(-1.3, 3.55), heading(0, 1), C, pose="crouch", tag="13TH (hand only)")
    # facing the back wall with the right arm tucked in; only that arm swings sideways out into the gap
    arm(thp2, "r", 58.0, (0.0, 0.3, 0.0)); arm(thp2, "r", 60.0, (0.0, 0.3, 0.0))
    arm(thp2, "r", 60.25, (0.0, -1.5, 0.0), "BEZIER"); arm(thp2, "r", 61.2, (0.0, 0.2, 0.0))
    ev("21", 58.3, "Nora stumbles in through the doorway on the right"); ev("21", 60.2, "the gloved, scarred right hand comes out from behind the tall crate stack and grabs her vest")
    ev("21", 60.5, "she is pulled into the gap behind the stack; gone by 61.5; hold the empty room to 62.5")
    cam = camera("CAM_21_C2_cctv_room4", 16, C)
    cam_keys(cam, 58.0, 62.5, lambda u, t: (R4(0.4, -0.05, 2.45), R4(-0.4, 4.5, 0.9), 0.0))
    shot("21", "C2", 58.0, 4.5, cam, "LOC-ROOM4", "S-CCTV", "C2", [nora_c2, th2],
         "13TH APPEARANCE #3: hand only. Same corner as the scene image; his body stays behind the tall crate stack.")

    # ---- 24 E2 macro on the red tag (70.5-74.0)
    C = coll("SHOT_24_E2")
    cam = camera("CAM_24_E2_macro", 100, C, clip=0.01)
    tag = V(0.905, 1.2, 0.905)
    cam_keys(cam, 70.5, 74.0, lambda u, t: (lerp(V(1.35, 0.85, 1.06), V(1.3, 0.9, 1.03), u), tag, 0.0))
    shot("24", "E2", 70.5, 3.5, cam, "LOC-EVIDENCE", "S-ROOM macro", "E2", [], "Title plate: EXHIBIT 47 is added on the tag in the edit.")

    # ---- 25a I3 Ward's hand turns the pen (74.0-76.5)
    C = coll("SHOT_25a_I3")
    ward3, wp = person("I3_WARD", "ward", I(0.75, 3.25), heading(-1, 0), C, pose="sit", tag="WARD (hand only)")
    arm(wp, "r", 74.0, (1.18, 0, 0.1)); arm(wp, "l", 74.0, (0.9, 0, -0.1))
    pen = box("I3_pen", I(0.28, 3.5, 0.765), (0.012, 0.14, 0.012), MATS["pen"], C)
    for i in range(6):
        key(pen, "rotation_euler", 74.0 + i * 0.5, (0, i * math.pi / 2, 0.3))
    window(pen, 74.0, 76.5)
    nora3, _ = person("I3_nora_offscreen", "nora_room", I(-0.75, 2.95), heading(1, 0), C, pose="sit", wearer=True)
    cam = camera("CAM_25a_I3_table", 50, C)
    cam_keys(cam, 74.0, 76.5, lambda u, t: (I(-0.3, 3.25, 1.14), I(0.28, 3.5, 0.76), 0.0))
    ev("25a", 74.0, "pen turns end over end, a half turn every 0.5 s; the scar catches the light")
    shot("25a", "I3", 74.0, 2.5, cam, "LOC-INTERVIEW", "S-ROOM", "I3", [ward3, nora3],
         "13TH APPEARANCE #4. Frame top must stay below Ward's chest.")

    # ---- 25b I4 Nora looks up (76.5-79.0)
    C = coll("SHOT_25b_I4")
    nora4, n4 = person("I4_nora", "nora_room", I(-0.75, 2.95), heading(1, 0), C, pose="sit", tag="NORA")
    key(n4["head"], "rotation_euler", 76.5, (-0.45, 0, 0)); key(n4["head"], "rotation_euler", 77.3, (-0.45, 0, 0))
    key(n4["head"], "rotation_euler", 78.1, (0.02, 0, 0), "BEZIER")
    ward4, _ = person("I4_WARD_offscreen", "ward", I(0.75, 3.25), heading(-1, 0), C, pose="sit", tag="WARD (must stay out of frame)")
    cam = camera("CAM_25b_I4_close", 50, C)
    cam_keys(cam, 76.5, 79.0, lambda u, t: (I(0.42, 3.05, 1.2), I(-0.75, 2.95, 1.24), 0.0))
    ev("25b", 77.3, "eyes start to rise; 78.1 she is looking at him; hold to 79.0")
    shot("25b", "I4", 76.5, 2.5, cam, "LOC-INTERVIEW", "S-ROOM", "I4", [nora4, ward4],
         "Camera sits in front of Ward's shoulder. The one-way mirror is directly behind Nora and reflects Ward at the right edge.")

    # ---- source-only shots (used by the montage and the 3-frame flash)
    C = coll("SHOT_S1_I2_source")
    nora2, _ = person("I2_nora", "nora_room", I(-0.75, 2.95), heading(1, 0), C, pose="sit", tag="NORA")
    ward2, _ = person("I2_WARD_offscreen", "ward", I(0.75, 3.25), heading(-1, 0), C, pose="sit")
    cam = camera("CAM_S1_I2_close", 50, C)
    cam_keys(cam, 90.0, 94.0, lambda u, t: (I(0.42, 2.8, 1.2), I(-0.75, 2.95, 1.25), 0.0))
    shot("S1", "I2", 90.0, 4.0, cam, "LOC-INTERVIEW", "S-ROOM", "I2", [nora2, ward2], "Lip-sync line. Used inside the montage (22).", source=True)

    C = coll("SHOT_S2_O1_source")
    leo, lp = person("O1_LEO_hands", "leo", H_(5.0, 44.0), heading(-1, 0), C, pose="hands_up", tag="LEO (hands only)")
    for i in range(8):
        arm(lp, "l", 94.0 + i * 0.5, (2.95 + (0.04 if i % 2 else -0.04), 0.25, 0))
    cam = camera("CAM_S2_O1_bodycam_reyes", 24, C)
    cam_keys(cam, 94.0, 98.0, lambda u, t: (H_(3.9, 44.0, CH), H_(5.0, 44.0, 2.5), 0.0), shake_amp=0.004, seed=2)
    shot("S2", "O1", 94.0, 4.0, cam, "LOC-FREEZER (3 years ago)", "S-OLD", "O1", [leo], "Hands only: needs the older camera's narrower view (~24 mm) from 1.1 m, tilted up ~46 deg; at 14 mm the face is always in frame. Used as a 3-frame flash (16) and in the montage (22).", source=True)

    C = coll("CARDS")
    boxr("black_box", -1, 1, -1, 1, -301, -299, MATS["void"], C)
    camb = camera("CAM_BLACK", 50, C)
    camb.location = (0, 0, -300)
    camb.rotation_euler = (0, 0, 0)
    return camb

def build_sets():
    extra_materials()
    set_exterior()
    set_stair()
    set_hall()
    set_room4()
    set_interview()
    set_evidence()

# --------------------------------------------------------------------------
# edit: the 89-second shot list (cards are composited later)
# --------------------------------------------------------------------------
EDIT = [
    ("01", 0.0, 2.0, "card", "AKOOL LOGO"),
    ("02", 2.0, 4.0, "shot", "02"),
    ("03", 6.0, 1.5, "card", "12 OFFICERS WENT IN."),
    ("04", 7.5, 4.0, "shot", "04"),
    ("05", 11.5, 2.5, "shot", "05"),
    ("06", 14.0, 1.5, "card", "1 CAME OUT."),
    ("07", 15.5, 3.0, "shot", "07"),
    ("08", 18.5, 1.5, "card", "13 CAMERAS WERE RECOVERED."),
    ("09", 20.0, 3.0, "shot", "09"),
    ("10", 23.0, 4.0, "shot", "10"),
    ("11", 27.0, 0.5, "card", ""),
    ("12", 27.5, 3.0, "grid", "lost:7-03@0.7,7-09@1.5"),
    ("13", 30.5, 3.0, "shot", "13"),
    ("14", 33.5, 1.5, "card", "ONE OF THEM"),
    ("15", 35.0, 2.5, "shot", "15"),
    ("16", 37.5, 1.5, "card", "BELONGED TO A DEAD MAN.|flash:S2"),
    ("17", 39.0, 2.5, "shot", "17"),
    ("18", 41.5, 2.0, "card", "IT HAD BEEN EVIDENCE ONCE BEFORE."),
    ("19a", 43.5, 1.0, "shot", "19a"),
    ("19b", 44.5, 1.0, "shot", "19b"),
    ("19c", 45.5, 1.0, "shot", "19c"),
    ("19d", 46.5, 1.0, "shot", "19d"),
    ("19e", 47.5, 1.0, "shot", "19e"),
    ("19f", 48.5, 1.0, "grid", "lost:7-01@0.1,7-05@0.1,7-10@0.1"),
    ("19g", 49.5, 1.5, "shot", "19g"),
    ("19h", 51.0, 1.5, "shot", "19h"),
    ("19i", 52.5, 1.5, "shot", "19i"),
    ("20", 54.0, 4.0, "grid", "final"),
    ("21", 58.0, 4.5, "shot", "21"),
    ("22", 62.5, 6.0, "montage", "S1:1.1,S2:1.0,19a:0.9,dot:0.8,10pre:0.7,17:0.6,19g:0.5,19a:0.4"),
    ("23", 68.5, 2.0, "card", ""),
    ("24", 70.5, 3.5, "shot", "24"),
    ("25a", 74.0, 2.5, "shot", "25a"),
    ("25b", 76.5, 2.5, "shot", "25b"),
    ("26", 79.0, 2.0, "card", "EVERY SHOT IN THIS FILM IS EVIDENCE."),
    ("27", 81.0, 1.5, "card", "THE CASE IS STILL OPEN."),
    ("28", 82.5, 2.5, "card", "THE THIRTEENTH APPEARS IN 4 SHOTS.|WATCH AGAIN."),
    ("29", 85.0, 2.0, "card", "COMING NEVER"),
    ("30", 87.0, 2.0, "card", "|dot"),
]

def bind_markers(camb):
    sc = bpy.context.scene
    by_n = {s["n"]: s for s in SHOTS}
    for n, t0, dur, kind, data in EDIT:
        m = sc.timeline_markers.new(f"{n} {by_n[data]['code'] if kind == 'shot' else kind.upper()}", frame=fr(t0))
        m.camera = bpy.data.objects[by_n[data]["cam"]] if kind == "shot" else camb
    for s in SHOTS:
        if s["source"]:
            m = sc.timeline_markers.new(f"SRC {s['code']}", frame=fr(s["t0"]))
            m.camera = bpy.data.objects[s["cam"]]

# --------------------------------------------------------------------------
# scene setup, analysis, render
# --------------------------------------------------------------------------
def setup_scene():
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start = 1
    sc.frame_end = fr(98.0)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 12
    try:
        sc.cycles.use_denoising = True
    except Exception:
        pass
    sc.cycles.max_bounces = 3
    sc.render.resolution_x, sc.render.resolution_y = 960, 540
    w = bpy.data.worlds.new("previs_sky")
    sc.world = w
    try:
        w.use_nodes = True
    except Exception:
        pass
    bg = next((n for n in w.node_tree.nodes if n.type == "BACKGROUND"), None)
    if bg is None:
        bg = w.node_tree.nodes.new("ShaderNodeBackground")
        out = next((n for n in w.node_tree.nodes if n.type == "OUTPUT_WORLD"), None) or w.node_tree.nodes.new("ShaderNodeOutputWorld")
        w.node_tree.links.new(bg.outputs[0], out.inputs[0])
    bg.inputs["Color"].default_value = (0.62, 0.65, 0.70, 1)
    bg.inputs["Strength"].default_value = 1.1
    sun = bpy.data.objects.new("sun_overcast", bpy.data.lights.new("sun_overcast", "SUN"))
    sc.collection.objects.link(sun)
    sun.data.energy = 1.6
    sun.data.angle = math.radians(25)
    sun.rotation_euler = (math.radians(50), 0, math.radians(35))

def world_to_cam(sc, cam, p):
    from bpy_extras.object_utils import world_to_camera_view
    return world_to_camera_view(sc, cam, p)

def analyze(outdir):
    """Ray-cast visibility per shot: who is in frame and who is occluded."""
    sc = bpy.context.scene
    for o in LABELS:
        o.hide_viewport = True
    report = []
    for s in SHOTS:
        cam = bpy.data.objects[s["cam"]]
        sc.camera = cam
        actors = [bpy.data.objects[a] for a in s["actors"] if bpy.data.objects[a].type == "EMPTY"]
        hidden = [a for a in actors if a.get("pov_wearer")]
        for a in hidden:
            for c in a.children_recursive:
                c.hide_viewport = True
        tracked = {}
        for a in actors:
            if a.get("pov_wearer"):
                continue
            names = a.get("parts") or [c.name for c in a.children_recursive if c.type == "MESH"]
            parts = [bpy.data.objects[n] for n in names]
            tracked[a.name] = parts
            for key_ in ("head", "hand_r", "scar"):
                sel = [p for p in parts if p.name.endswith("_" + key_)]
                if sel:
                    tracked[f"{a.name}.{key_}"] = sel
        stats = {k: [] for k in tracked}
        frames = list(range(fr(s["t0"]), fr(s["t1"]), 2))
        for f in frames:
            sc.frame_set(f)
            dg = bpy.context.evaluated_depsgraph_get()
            cl = cam.matrix_world.translation.copy()
            for lab, objs in tracked.items():
                names = {o.name for o in objs}
                tot = vis = 0
                for o in objs:
                    mw = o.matrix_world
                    if min(abs(v) for v in mw.to_scale()) < 3e-3:
                        continue
                    c = mw.translation
                    pts = [c] + [c.lerp(mw @ Vector(b), 0.85) for b in o.bound_box]
                    for p in pts:
                        co = world_to_cam(sc, cam, p)
                        if not (0.0 <= co.x <= 1.0 and 0.0 <= co.y <= 1.0 and co.z > 0):
                            continue
                        tot += 1
                        d = p - cl
                        hit, _, _, _, hobj, _ = sc.ray_cast(dg, cl, d.normalized(), distance=max(d.length - 0.005, 0.001))
                        if (not hit) or hobj.original.name in names:
                            vis += 1
                stats[lab].append((f, vis, tot))
        rows = []
        for lab, seq in stats.items():
            seen = [f for f, v, t in seq if v > 0]
            inframe = [f for f, v, t in seq if t > 0]
            frac = max((v / t) for f, v, t in seq if t > 0) if inframe else 0.0
            rows.append(dict(target=lab, frames_visible=len(seen), frames=len(seq),
                             first=round((seen[0] - 1) / FPS, 2) if seen else None,
                             last=round((seen[-1] - 1) / FPS, 2) if seen else None,
                             frames_in_frame=len(inframe), max_unoccluded=round(frac, 2)))
        report.append(dict(shot=s["n"], code=s["code"], rows=rows))
        for a in hidden:
            for c in a.children_recursive:
                c.hide_viewport = False
    for o in LABELS:
        o.hide_viewport = False
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "analysis.json"), "w") as fh:
        json.dump(report, fh, indent=1)
    return report

def unbind_markers():
    """Marker-bound cameras override scene.camera on every frame change."""
    for m in bpy.context.scene.timeline_markers:
        m.camera = None

def render(outdir, sample_only=False, step=1, res=None, samples=None, only=None):
    sc = bpy.context.scene
    unbind_markers()
    if res:
        sc.render.resolution_x, sc.render.resolution_y = res
    if samples:
        sc.cycles.samples = samples
    for o in LABELS:
        o.hide_render = True
    keep = set(only.split(",")) if only else None
    for s in SHOTS:
        if keep and s["n"] not in keep:
            continue
        cam = bpy.data.objects[s["cam"]]
        sc.camera = cam
        d = os.path.join(outdir, s["n"])
        os.makedirs(d, exist_ok=True)
        f0, f1 = fr(s["t0"]), fr(s["t1"]) - 1
        frames = [f0 + 4, (f0 + f1) // 2, f1 - 4] if sample_only else list(range(f0, f1 + 1, step))
        for f in frames:
            out = os.path.join(d, f"f_{f:05d}.png")
            if os.path.exists(out):
                continue
            sc.frame_set(f)
            sc.render.filepath = out
            bpy.ops.render.render(write_still=True)

def render_refs(outdir):
    """Render each set from the camera that matches its scene image (empty sets)."""
    sc = bpy.context.scene
    unbind_markers()
    for o in LABELS:
        o.hide_render = True
    sc.frame_set(fr(88.5))  # no shot is live here, so every actor is hidden
    os.makedirs(outdir, exist_ok=True)
    for set_, cam_name in REFS.items():
        sc.camera = bpy.data.objects[cam_name]
        sc.render.filepath = os.path.join(outdir, f"ref_{set_}.png")
        bpy.ops.render.render(write_still=True)

def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    make_materials()
    build_sets()
    camb = build_shots()
    bind_markers(camb)
    setup_scene()
    interp("BEZIER")
    sc = bpy.context.scene
    sc["previs_shots"] = json.dumps(SHOTS)
    sc["previs_edit"] = json.dumps(EDIT)
    sc["previs_events"] = json.dumps(EVENTS)
    sc.frame_set(fr(23.0))
    sc.camera = bpy.data.objects["CAM_10_B2_bodycam_nora"]
    out = arg("--meta")
    if out:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w") as fh:
            json.dump(dict(shots=SHOTS, edit=EDIT, events=EVENTS, params=P, refs=REFS, fps=FPS), fh, indent=1, ensure_ascii=False)
    if arg("--analyze"):
        analyze(arg("--analyze"))
    save = arg("--save")
    if save:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(save), compress=True)
    if arg("--refs"):
        render_refs(arg("--refs"))
    if arg("--render"):
        res = arg("--res")
        render(arg("--render"), sample_only=arg("--sample", flag=True), step=int(arg("--step", 1)),
               res=tuple(int(v) for v in res.split("x")) if res else None,
               samples=int(arg("--samples")) if arg("--samples") else None,
               only=arg("--only"))

if __name__ == "__main__":
    main()
