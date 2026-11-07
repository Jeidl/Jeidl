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

## Keyframes (AKOOL, v1)

`keyframes/` holds the keyframes generated from the whitebox: each shot's guide frame
(the whitebox at the same timecode, text hidden) went into AKOOL image-to-image
(flux-kontext-dev) with a prompt that maps every colour block to the real thing.
Notes, per-frame table and lessons:
`knowledge-base/topics/production/exhibit-47-keyframes.md`.

| File | What it is |
|---|---|
| `keyframes/frames/` | The 30 selected keyframes (1280x720 copies; full-size originals are on AKOOL's CDN). |
| `keyframes/contact_sheet.jpg` | Guide frame next to keyframe for every selected frame. |
| `keyframes/keyframes.json` | Production log: all 53 attempts with prompt, negative prompt, source, similarity, AKOOL id, result URL and verdict. |
| `keyframes/tools/render_guides.py` | Renders clean guide frames (1280x720, text objects hidden) from the `.blend`. |
| `keyframes/tools/run_guides.py` | Same, through `pip install bpy` instead of the blender binary. |
| `keyframes/tools/comp_i3.py` | Composites the approved Ward hand sheet onto the AKOOL table plate for shot I3. |

    blender -b previs/exhibit47_whitebox.blend -P previs/keyframes/tools/render_guides.py -- /tmp/guides 02:3.0 10:23.2
