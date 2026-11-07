"""Render clean whitebox guide frames for keyframes: blender -b BLEND -P this.py -- OUTDIR SHOT:TIME ..."""
import bpy, sys, os, json
args = sys.argv[sys.argv.index("--") + 1:]
out = args[0]
sc = bpy.context.scene
shots = {s["n"]: s for s in json.loads(sc["previs_shots"])}
for m in sc.timeline_markers:
    m.camera = None
for o in bpy.data.objects:
    if o.type == "FONT":
        o.hide_render = True
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
sc.cycles.samples = 24
for item in args[1:]:
    n, t = item.split(":")
    sc.camera = bpy.data.objects[shots[n]["cam"]]
    sc.frame_set(int(round(float(t) * 24)) + 1)
    sc.render.filepath = os.path.join(out, f"guide_{n}_{float(t):.2f}.png")
    bpy.ops.render.render(write_still=True)
