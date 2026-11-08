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

## Video clips and rough cut v3 (AKOOL video, LibTV sound, evidence in post)

`clips/` holds all image-to-video work, done in AKOOL from the v2 keyframes: 61 clips,
1210 credits. Round one used Akool Premium (8 credits per 5 s clip); later rounds upgraded
shots with Seedance 1.0 Pro Fast (25 credits at 1080p, 13 at 720p) and Seedance 1.0 Lite;
I4 uses Kling 3.0 Omni (100). Round four (after the second review) re-made the C2 cold room
as one fixed camera and a restrained B4. I2 is lip-synced with AKOOL Talking Photo.
`audio/voice/` has every dialogue line from AKOOL text-to-speech. AKOOL has no music or
sound-effect generation, so the music bed and the effects in `audio/music/` and `audio/sfx/`
come from LibTV (ElevenMusic V3, Seed Audio 1.0). Readable evidence (the register, the tag,
every device's on-screen display) is composited in post, never generated.

Rough cut v3 is built in three steps; the picture step also writes a timeline that the
sound step uses to put every line and effect on its frame:

```
python3 clips/tools/fetch_clips.py /tmp/clips
python3 clips/tools/roughcut.py /tmp/cut.mp4 /tmp/clips          # picture, 1280x720 + /tmp/cut.timeline.json
python3 clips/tools/soundmix.py /tmp/cut.mp4 /tmp/cut_sound.mp4 /tmp/clips
```

| File | What it is |
|---|---|
| `clips/roughcut_v3_540p.mp4` | **Current.** Rough cut v3, 85.2 s, after the second review: readable register and tag, device OSDs, FEED 01-12 + FEED 13, C2 as one camera, sound on the picture's frames (-14.0 LUFS). |
| `clips/roughcut_v3.timeline.json`, `clips/roughcut_v3.cues.json` | Every segment (start, clip, in-point, muzzle flashes) and every sound cue of v3. |
| `clips/roughcut_v2_540p.mp4` | Rough cut v2 with dialogue, music and effects. |
| `clips/clips_v2.json` | Log of all 57 videos: round, model, credits, first/last frame, audio, prompt, negative prompt, AKOOL id, video URL, verdict, `used_in_cut_v1` and `used_in_cut_v2`. |
| `clips/clips_v1.json` | Round-one log (29 Akool Premium / Kling / Seedance Pro generations), kept for reference. |
| `clips/strips/` | Six frames from each clip. |
| `clips/roughcut_v1_540p.mp4` | Rough cut v1, dialogue only (its dialogue sits about 3 s early; fixed in v2). |
| `clips/roughcut_v0_540p.mp4` | Silent rough cut v0 (round one only). |
| `clips/tools/fetch_clips.py` | Downloads the clips cut v3 uses (`--v2`, `--v1` for older cuts, `--all` for every take). |
| `clips/tools/roughcut.py` | Builds the v3 picture and its timeline: `python3 roughcut.py OUT.mp4 CLIP_DIR [W H]`. |
| `clips/tools/overlays.py`, `clips/tools/track_plane.py`, `clips/overlays/` | Register text laid on the page's ruled lines, tag text moved with the tag (optical-flow homographies), device OSD helpers. |
| `clips/tools/breakdown.py` | Timecoded breakdown of any video (shots, black, silences, hits, contact sheet), for the reference trailers. |
| `clips/tools/soundmix.py` | Mixes dialogue, music, effects and room tone onto a cut, anchored to its timeline: `python3 soundmix.py CUT.mp4 OUT.mp4 [CLIP_DIR]`. |
| `audio/voice/*.mp3`, `audio/voice_lines.json` | The dialogue lines, with voice, speed and AKOOL task id per line. |
| `audio/sfx/*.mp3`, `audio/music/SC1_music_bed.mp3`, `audio/sfx_music.json` | Effects (peak-normalised to -1 dBFS) and the music bed, with prompts and LibTV node and task ids. |

The originals stay on AKOOL's CDN. Notes, casting and lessons:
`knowledge-base/topics/production/exhibit-47-video-clips.md`; sound:
`knowledge-base/topics/production/exhibit-47-sound-mix.md`; second review and v3:
`knowledge-base/topics/production/exhibit-47-review-2.md`.

## Keyframes v2 (current)

`keyframes/v2/` is the current set: 30 frames, redone to the live-action
standard with the evidence-camera look (body-cam fisheye and compression, CCTV
infrared, old-camera colour cast) generated into the image itself. Only
on-screen text (timestamps, IDs, REC, tag text) is left for the edit.

- Shots with people (23): LibTV, Chinese prompts, with the whitebox guide frame
  for composition and the v3 character sheets for faces, gear and the scarred hand.
- Environments and props (7): AKOOL (flux-krea text-to-image, flux-kontext edits).

| File | What it is |
|---|---|
| `keyframes/v2/frames/` | The 30 selected frames (1280x720 copies; full-size source URLs are in the log). |
| `keyframes/v2/contact_sheet.jpg` | All 30, labelled with the tool that made each one. |
| `keyframes/v2/keyframes_v2.json` | `selected` (30 frames) and `attempts` (all 45 generations: prompt, references or source image, LibTV node and task id or AKOOL id, result URL, verdict). |
| `keyframes/tools/paint_out_box.py` | Paints a rectangle out of a frame with mirrored texture; used once, for the text box AKOOL drew on `21_C2_start`. |

Notes, per-frame table and lessons: the v2 section of
`knowledge-base/topics/production/exhibit-47-keyframes.md`.

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
