"""Render whitebox guide frames without the blender binary (pip install bpy):
    python previs/keyframes/tools/run_guides.py -- OUTDIR SHOT:TIME [SHOT:TIME ...]
e.g. python previs/keyframes/tools/run_guides.py -- /tmp/guides 02:3.0 10:23.2 25b:75.3
TIME is the edit time in seconds (the timeline of exhibit47_whitebox.blend)."""
import bpy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
items = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "..", "..", "exhibit47_whitebox.blend"))
sys.argv = ["blender", "--"] + items
exec(open(os.path.join(HERE, "render_guides.py")).read())
