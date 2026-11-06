# EXHIBIT 47 whitebox previs

Box-only Blender whitebox of every location in the trailer, built from the AKOOL
scene images in `scene_refs/`. Every shot of the 89-second cut has its actors and
camera keyed to the shot-list timecodes. Full notes, findings and per-shot tables:
`knowledge-base/topics/production/exhibit-47-whitebox-previs.md`.

| File | What it is |
|---|---|
| `exhibit47_whitebox.py` | Generator. All dimensions live in `P` at the top. |
| `exhibit47_whitebox.blend` | The generated project (saved by Blender 5.2). |
| `compose_animatic.py` | Builds the animatic: cards, 4x3 monitor wall, montage, overlays. |
| `out/` | Animatic MP4, storyboard, scene-vs-whitebox comparison, visibility analysis. |
| `scene_refs/` | The six AKOOL scene images the sets are measured from. |

Open the `.blend` and press play: timeline markers switch cameras, so the timeline
plays the edit. If your Blender is older than 5.x, run the script from the
Scripting tab instead; it rebuilds the whole scene.

Headless (Blender 4.2+ or `pip install bpy`):

    blender -b -P previs/exhibit47_whitebox.py -- --save previs/exhibit47_whitebox.blend --meta previs/out/meta.json --analyze previs/out
    blender -b -P previs/exhibit47_whitebox.py -- --refs previs/out/refs
    blender -b -P previs/exhibit47_whitebox.py -- --render previs/out/frames --step 2 --res 640x360 --samples 6
    python3 previs/compose_animatic.py previs/out/meta.json previs/out/frames previs/out/exhibit47_whitebox_animatic.mp4 previs/out/storyboard.jpg

Colour code: environment clay, Nora cyan, the thirteenth orange, Brandt yellow,
Ward purple, Leo green, officers grey, burn scar pink, evidence red.
