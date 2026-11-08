"""EXHIBIT 47 rough cut v3: the picture (about 85 s, 24 fps) with the evidence made readable.

    python3 fetch_clips.py /tmp/clips
    python3 roughcut.py /tmp/cut.mp4 /tmp/clips [W H]
    python3 soundmix.py /tmp/cut.mp4 /tmp/cut_sound.mp4 /tmp/clips

Writes OUT.mp4 (silent picture) and OUT.timeline.json: every segment's id, start, length,
source clip and in-point, and the muzzle flashes found in the gunfire shots. soundmix.py
reads it, so each line and effect sits on the frame it belongs to, not on a fixed second.

v3 answers the second review:
- the 12 -> 1 -> 13 conflict lands by 11.6 s: the 911 call over the vans, the breach, then
  "1 CAME OUT." straight into D1, so the lone figure reads as the survivor;
- the register and the red tag carry readable text composited in post (overlays.py; the tag
  follows track_plane.py's homographies): case NORTHGATE 09 FEB 2023, row 47 BODY CAMERA
  7-12, S/N AX-118-0412, a red LOST stamp, and EXHIBIT 47 on the tag;
- every source has its own on-screen display: Team 7 body cams (AX-220, ISO date), the old
  AX-118 unit (amber, US date) on the 13th's camera, CCTV, drone, interview room, and an
  ARCHIVE banner with the 2023 date on the old footage;
- the monitor wall is the twelve body cams, FEED 01-12; after the last one dies and the
  silence, a thirteenth feed appears with live footage and the AX-118 serial;
- C2 is one fixed camera from the empty room to the empty room: Nora stumbles in, the hand
  grabs her, her own body cam sees the scar through the torn glove, sparks hit where she
  stood, she is dragged behind the crates;
- the breach is one action (swing, hit, door gives, team in); the first Brandt beat is
  restrained; the B8 reflection is reframed so its red light sits where the lens is;
- the black after the montage is 1 s.

Needs ffmpeg, numpy and Pillow. Stills come from previs/keyframes/v2/frames. Cards are
placeholders (Liberation Sans); the AKOOL card still needs the official logo."""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import overlays as OV

OUT, C = sys.argv[1], os.path.abspath(sys.argv[2]) + '/'
W, H = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1280, 720)
T = tempfile.mkdtemp() + '/'
KF = os.path.normpath(os.path.join(HERE, '..', '..', 'keyframes', 'v2', 'frames')) + '/'
OVL = os.path.normpath(os.path.join(HERE, '..', 'overlays')) + '/'
FPS = 24
BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
VF = f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p'
ENC = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-r', str(FPS), '-video_track_timescale', '12288']
F = lambda s: int(round(s * FPS))
segs, TL, pos, n = [], [], [0], [0]
EP = OV.epoch


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def frames_in(p):
    return int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                               'stream=nb_read_frames', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip() or 0)


def new_seg():
    n[0] += 1
    return f'{T}s{n[0]:03d}.mp4'


def add(sid, path, frames, **meta):
    got = frames_in(path)
    if got != frames:
        print('short segment', sid, frames, got)
    TL.append(dict(id=sid, start=round(pos[0] / FPS, 4), frames=frames, dur=round(frames / FPS, 4), **meta))
    pos[0] += frames
    segs.append(path)


def flashes(path):
    """Frames where the picture suddenly brightens (muzzle flashes), as seconds into the segment:
    the mean jumps by 5 or the brightest 1% jumps by 14 levels from the frame before."""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', 'scale=64:36,format=gray', '-f', 'rawvideo', '-'],
                         capture_output=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, 36 * 64).astype(float)
    L, P = f.mean(1), np.percentile(f, 99, axis=1)
    out, last = [], -9
    for i in range(1, len(L)):
        if (L[i] - L[i - 1] > 5 or P[i] - P[i - 1] > 14) and i - last > 2:
            out.append(round(i / FPS, 3)); last = i
    return out


def overlay_seq(fn, frames):
    """Write fn(i) -> RGBA for every frame; return the ffmpeg input args for the sequence."""
    d = tempfile.mkdtemp(dir=T) + '/'
    for i in range(frames):
        fn(i).save(f'{d}o_{i:04d}.png')
    return ['-framerate', str(FPS), '-i', f'{d}o_%04d.png']


def clip(sid, name, start, frames, extra='', osd='', ovl=None, flash=False, **meta):
    """A piece of a clip: scale/crop -> optional per-frame overlay -> extra filters -> OSD."""
    o = new_seg()
    ins = ['-ss', str(start), '-i', C + name + '.mp4']
    chain = f'[0:v]{VF}[b]'
    last = '[b]'
    if ovl is not None:
        ins += overlay_seq(ovl, frames)
        chain += ';[1:v]format=rgba[o];[b][o]overlay=0:0:eof_action=pass,format=yuv420p[c]'
        last = '[c]'
    post = ','.join(x for x in (extra, osd, f'tpad=stop_mode=clone:stop={frames}') if x)
    chain += f';{last}{post}[v]'
    run(['ffmpeg', '-y'] + ins + ['-filter_complex', chain, '-map', '[v]', '-frames:v', str(frames), '-an'] + ENC + [o])
    meta.update(clip=name, src_in=start)
    if flash:
        meta['flashes'] = flashes(o)
    add(sid, o, frames, **meta)


def still(sid, img, frames, extra='', osd='', **meta):
    p = T + f'still{n[0] + 1}.png'
    img.convert('RGB').resize((W, H)).save(p)
    post = ','.join(x for x in (VF, extra, osd) if x)
    o = new_seg()
    run(['ffmpeg', '-y', '-loop', '1', '-i', p, '-frames:v', str(frames), '-vf', post] + ENC + [o])
    add(sid, o, frames, **meta)


def jolt():
    """Handheld jolt for a still: a hard knock that settles (the body cam is being grabbed)."""
    a = '(14*exp(-n/3)+2)'
    return (f"crop=w=iw*0.92:h=ih*0.92:x='(iw-ow)/2+{a}*sin(n*2.1)':y='(ih-oh)/2+{a}*cos(n*1.7)',"
            f"scale={W}:{H}")


def card(sid, lines, frames, size=0.052, color=(236, 232, 224), sub=None, dot=None):
    im = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(BOLD, int(H * size)); lh = int(H * size * 1.35)
    y0 = H // 2 - lh * len(lines) // 2
    for i, t in enumerate(lines):
        w = d.textlength(t, font=f); d.text(((W - w) / 2, y0 + i * lh), t, font=f, fill=color)
    if sub:
        fs = ImageFont.truetype(BOLD, int(H * 0.026)); w = d.textlength(sub, font=fs)
        d.text(((W - w) / 2, y0 + len(lines) * lh + H * 0.02), sub, font=fs, fill=(150, 150, 150))
    if dot:
        r = int(H * 0.012); x, y = dot; d.ellipse((x - r, y - r, x + r, y + r), fill=(224, 40, 28))
    still(sid, im, frames, kind='card', text=' / '.join(lines))


def color(sid, rgb, frames, **meta):
    still(sid, Image.new('RGB', (W, H), rgb), frames, **meta)


def frame_of(name, t, extra=''):
    p = T + f'grab_{name}_{t}.png'
    run(['ffmpeg', '-y', '-ss', str(t), '-i', C + name + '.mp4', '-frames:v', '1', '-vf', ','.join(x for x in (VF, extra) if x), p])
    return Image.open(p).convert('RGB').copy()


# ---------------------------------------------------------------- monitor wall
# FEED 01-12 are the twelve Team 7 body cams (all body-worn; CCTV never appears on the wall).
# FEED 12 is Nora's (call sign 7-12), the last one to die. (clip, in-point at the first wall)
FEEDS = [('05_B1__akp', 2.0), ('15_B4__akp', 0.3), ('13_B3__akp', 0.5), ('19a_B5__akp', 1.5),
         ('19e_B6__akp', 0.0), ('19b_B9__akp', 0.0), ('19g_B7__akp', 0.0), ('19d_B10__akp', 0.0),
         ('05_B1__sdfast', 3.8), ('10_B2a__akp', 0.5), ('15_B4__sdfast', 0.0), ('10_B2a__sdfast', 0.6)]
CW, CH = W // 4, H // 3


def cell_frames(name, t0, frames, w, h):
    d = tempfile.mkdtemp(dir=T) + '/'
    run(['ffmpeg', '-y', '-ss', str(t0), '-i', C + name + '.mp4', '-frames:v', str(frames),
         '-vf', f'fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}', d + 'c_%04d.png'])
    files = sorted(os.listdir(d))
    return [Image.open(d + f).convert('RGB') for f in files] + [None] * (frames - len(files))


def wall(frames, lost, shift=0.0, feed13=None, dim=False):
    """lost = {feed_index: frame it dies}; feed13 = (clip, in-point) for the extra feed."""
    fm = ImageFont.truetype(MONO, int(CH * 0.085)); fl = ImageFont.truetype(BOLD, int(CH * 0.11))
    live = [None if dim else cell_frames(c, t + shift, frames, CW, CH) for c, t in FEEDS]
    fw, fh = int(CW * 1.5), int(CH * 1.5)
    x13 = cell_frames(feed13[0], feed13[1], frames, fw, fh) if feed13 else None
    out = []
    for k in range(frames):
        im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
        for i in range(12):
            x, y = (i % 4) * CW, (i // 4) * CH
            dead = dim or (i in lost and k >= lost[i])
            if dead:
                d.rectangle((x, y, x + CW - 1, y + CH - 1), fill=(0, 0, 0))
                t = 'SIGNAL LOST'; w = d.textlength(t, font=fl)
                d.text((x + (CW - w) / 2, y + CH / 2 - CH * 0.06), t, font=fl, fill=(150, 150, 150) if dim else (200, 200, 200))
            elif live[i][k] is not None:
                im.paste(live[i][k], (x, y))
            d.rectangle((x, y, x + CW - 1, y + CH - 1), outline=(40, 40, 40))
            d.text((x + 6, y + 4), f'FEED {i + 1:02d}', font=fm, fill=(120, 120, 120) if dead else (230, 230, 230))
        if feed13 and k >= 2:                                   # two frames of nothing, then it is just there
            x0, y0 = (W - fw) // 2, (H - fh) // 2
            if x13[k] is not None:
                im.paste(x13[k], (x0, y0))
            d.rectangle((x0 - 2, y0 - 2, x0 + fw + 1, y0 + fh + 1), outline=(236, 232, 224), width=2)
            fb = ImageFont.truetype(MONO, int(fh * 0.07))
            d.rectangle((x0, y0, x0 + fw, y0 + int(fh * 0.11)), fill=(0, 0, 0))
            d.text((x0 + 8, y0 + 4), 'FEED 13   UNKNOWN DEVICE', font=fb, fill=(236, 232, 224))
            d.text((x0 + 8, y0 + fh - int(fh * 0.1)), 'AX-118  S/N 0412', font=fb, fill=(232, 200, 96))
            if (k // 12) % 2 == 0:
                r = int(fh * 0.03); cx, cy = x0 + fw - 18, y0 + int(fh * 0.055)
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(224, 40, 28))
        out.append(im)
    return out


def wall_seg(sid, frames, lost, shift=0.0, feed13=None, dim=False, **meta):
    ims = wall(frames, lost, shift, feed13, dim)
    d = tempfile.mkdtemp(dir=T) + '/'
    for k, im in enumerate(ims):
        im.save(f'{d}g_{k:04d}.png')
    o = new_seg()
    run(['ffmpeg', '-y', '-framerate', str(FPS), '-i', d + 'g_%04d.png', '-vf', VF] + ENC + [o])
    add(sid, o, frames, kind='wall', **meta)


# ---------------------------------------------------------------- shared material
E2 = '24_E2__sdfast720'
tag_at = OV.tag_frames(OVL + E2 + '.track.json', W, H)


def tagged(src_in):
    """Overlay function for E2 starting at src_in: the tag text where the tag is."""
    return lambda i: tag_at(int(round(src_in * FPS)) + i)


reg_frame = frame_of('18_E3_register__sdfast', 1.0)
reg_text, reg_stamp = OV.register_layers(reg_frame.resize((1280, 720)), 1280, 720)
reg_text, reg_stamp = reg_text.resize((W, H)), reg_stamp.resize((W, H))
REG_FRAMES, STAMP_AT = 89, 24


def reg_ovl(i):
    im = reg_text.copy()
    if i >= STAMP_AT:
        im.alpha_composite(reg_stamp)
    return im


pov = Image.open(KF + '21_C2_pov_scar.jpg').convert('RGB')
CCTV_IR = 'hue=s=0,eq=contrast=1.06'
REFRAME_B8 = f'crop=iw*0.8:ih*0.8:iw*0.2:ih*0.121,scale={W}:{H}'   # puts the reflection's red light on the lens axis
bwc = lambda unit, ep: OV.osd('bwc', H, ep, unit)
old = lambda ep, unit='7-12': OV.osd('old', H, ep, unit)

# ---------------------------------------------------------------- ACT 1: 12 -> 1 -> 13 (by 11.6 s)
card('LOGO', ['AKOOL'], 36, size=0.09, sub='official logo goes here')
clip('C3', '04_C3__sdfast', 0.6, 72, osd=OV.osd('cctv', H, EP(2026, 2, 9, 3, 59, 38), cam='CAM 02  NORTHGATE COLD STORE'))
card('CARD12', ['12 OFFICERS WENT IN.'], 29)
clip('B1', '05_B1__sdfast', 1.65, 29, osd=bwc('7-04', EP(2026, 2, 9, 4, 1, 5)), note='swing, hit at +0.56 s, door gives')
color('B1F', (232, 232, 228), 2, note='flare over the cut past the second swing')
clip('B1b', '05_B1__sdfast', 3.70, 22, osd=bwc('7-04', EP(2026, 2, 9, 4, 1, 9)), note='team goes in')
card('CARD1', ['1 CAME OUT.'], 29)
clip('D1', '02_D1__akp', 0.0, 60, osd=OV.osd('drone', H, EP(2026, 2, 9, 7, 40, 12)), note='07:40, the survivor walks out')
card('CARD13', ['13 CAMERAS WERE RECOVERED.'], 36)
clip('E1', '09_E1__sdfast720', 1.5, 60)
clip('I1', '07_I1__sdfast', 0.2, 60, osd=OV.osd('room', H, EP(2026, 2, 10, 14, 22, 5), cam='INTERVIEW 3', alpha=0.7))
# B2 is Nora's own camera (7-12): count off, she says twelve, then the view swings to the back of the line
clip('B2', '10_B2a__sdfast', 0.4, 58, osd=bwc('7-12', EP(2026, 2, 9, 4, 3, 8)), note='descent, count off')
clip('B2w', '10_B2b__akp', 0.0, 12, osd=bwc('7-12', EP(2026, 2, 9, 4, 3, 10)), note='whip to the back of the line')
clip('B2h', '10_B2b__sdfast', 0.3, 26, osd=bwc('7-12', EP(2026, 2, 9, 4, 3, 11)), note='the 13th, red light on')
color('BLACK1', (0, 0, 0), 12)
wall_seg('GRID1', 72, {2: F(1.2), 8: F(2.0)}, note='FEED 03 and 09 die')

# ---------------------------------------------------------------- ACT 2: the camera that should not exist
clip('B3', '13_B3__akp', 0.3, 72, osd=bwc('7-07', EP(2026, 2, 9, 4, 9, 31)))
card('CARD_ONLY12', ['ONLY 12 CAMERAS WERE ISSUED.'], 48)
clip('B4', '15_B4_quiet__sdfast', 1.2, 60, osd=bwc('7-09', EP(2026, 2, 9, 4, 38, 2)), note='restrained: suspicion, low voice')
card('CARD_DEAD', ['ONE CAMERA BELONGED', 'TO A DEAD MAN.'], 45)
clip('O1F', 'S2_O1__akp', 1.0, 3, osd=OV.osd('archive', H, EP(2023, 2, 9, 1, 11, 2), '7-12'))
clip('O2', '17_O2__sdfast', 1.5, 60, osd=OV.osd('archive', H, EP(2023, 2, 9, 1, 12, 40), '7-05'), note='2023: they switch their cameras off')
# E3: the register with the text on its lines, a slow push toward row 47, LOST at +1 s, whip to the tag
push = (f"scale={W * 2}:{H * 2},zoompan=z='1+0.30*on/{REG_FRAMES}':"
        f"x='max(0,min(iw-iw/zoom,(0.5+0.23*on/{REG_FRAMES})*iw-iw/zoom/2))':"
        f"y='max(0,min(ih-ih/zoom,(0.5-0.17*on/{REG_FRAMES})*ih-ih/zoom/2))':d=1:s={W}x{H}:fps={FPS},"
        f"avgblur=sizeX={W // 24}:sizeY=1:enable='gte(n,{REG_FRAMES - 4})'")
clip('E3REG', '18_E3_register__sdfast', 0.5, REG_FRAMES, extra=push, ovl=reg_ovl, stamp_at=round(STAMP_AT / FPS, 3))
clip('E3TAG', E2, 2.2, 31, extra=f"avgblur=sizeX={W // 24}:sizeY=1:enable='lt(n,3)'", ovl=tagged(2.2), note='EXHIBIT 47 readable')
# the firefight: a retreat order, the corridor fills with gas, the wall starts to die
clip('B5', '19a_B5__sdfast', 0.6, 24, osd=bwc('7-03', EP(2026, 2, 9, 5, 2, 44)), flash=True)
clip('B9', '19b_B9__sdfast720', 1.4, 24, osd=bwc('7-06', EP(2026, 2, 9, 5, 2, 46)), flash=True, note='hit at +0.5 s, flashlight lands +0.7 s')
clip('C1', '19c_C1__sdfast720', 3.0, 24, extra='hue=s=0.2,eq=contrast=1.08:brightness=-0.03',
     osd=OV.osd('cctv', H, EP(2026, 2, 9, 5, 2, 48), cam='CAM 07  HALL B'), flash=True)
clip('B10', '19d_B10__akp', 0.4, 24, osd=bwc('7-01', EP(2026, 2, 9, 5, 2, 50)))
clip('B6', '19e_B6__sdfast', 0.5, 30, osd=bwc('7-10', EP(2026, 2, 9, 5, 2, 53)), note='pipe bursts: the way back is gas')
wall_seg('GRID2', 24, {2: 0, 8: 0, 3: F(0.2), 6: F(0.5), 10: F(0.8)}, shift=2.0, note='FEED 04, 07, 11 die')
clip('B7', '19g_B7__sdfast720', 1.0, 36, osd=bwc('7-11', EP(2026, 2, 9, 5, 4, 2)), note='Brandt loses it')
clip('X1', '19h_X1__sdfast', 1.0, 36, osd=old(EP(2026, 2, 9, 5, 6, 51)), note='the 13th: AX-118, calm')
clip('B8s', '19i_B8_start__akp', 2.8, 17, osd=old(EP(2026, 2, 9, 5, 10, 14)))
clip('B8r', '19i_B8_reflection__sdfast720', 1.0, 19, extra=REFRAME_B8, osd=old(EP(2026, 2, 9, 5, 10, 15)),
     note='his own reflection: the red light is where the lens is')
wall_seg('GRID3', 24, {i: 0 for i in range(11)} | {11: F(0.6)}, shift=3.0, note='FEED 12 (Nora) dies last')
still('DEAD', wall(1, {}, dim=True)[0], 36, kind='silence')
wall_seg('FEED13', 54, {}, dim=True, feed13=('19h_X1__akp', 0.5), note='a thirteenth feed, still recording')
# C2: one fixed camera, CAM 11, from the empty room to the empty room
cam11 = lambda s: OV.osd('cctv', H, EP(2026, 2, 9, 5, 12, s), cam='CAM 11  COLD ROOM 4')
clip('C2e', '21_C2_enter__sdfast', 1.6, 38, extra=CCTV_IR, osd=cam11(31))
color('C2d', (12, 12, 12), 2, note='CCTV dropout')
clip('C2g', '21_C2_pull__sdfast', 0.0, 12, extra=CCTV_IR, osd=cam11(34), note='the hand takes her vest strap')
still('C2i', pov, 17, extra=jolt(), osd=bwc('7-12', EP(2026, 2, 9, 5, 12, 35)), note="Nora's own camera sees the scar")
clip('C2p', '21_C2_pull__sdfast', 0.5, 58, extra=CCTV_IR, osd=cam11(35), note='sparks +0.3, yanked left +0.7, gone +1.5')

# ---------------------------------------------------------------- ACT 3: the evidence
tag = frame_of(E2, 3.4).convert('RGBA')
tag.alpha_composite(tag_at(int(3.4 * FPS)))
refl = frame_of('19i_B8_reflection__sdfast720', 2.5, REFRAME_B8)
f13 = wall(3, {}, dim=True, feed13=('19h_X1__akp', 1.5))[2]
clip('M_I2', 'S1_I2__talk', 0.2, 36, note='"There were thirteen of us." (the audio runs on)')
color('M_w1', (255, 255, 255), 2)
clip('M_O1', 'S2_O1__akp', 0.5, 10)
color('M_b1', (0, 0, 0), 2); still('M_scar', pov, 6); color('M_b2', (0, 0, 0), 2)
clip('M_B2', '10_B2a__akp', 1.0, 12)
color('M_w2', (255, 255, 255), 2)
still('M_tag', tag, 6)
clip('M_O2', '17_O2__sdfast', 2.5, 10)
still('M_refl', refl, 4)
clip('M_B7', '19g_B7__sdfast720', 2.0, 10)
color('M_w3', (255, 255, 255), 2)
still('M_f13', f13, 4)
clip('M_B5', '19a_B5__sdfast', 1.0, 8)
still('M_s2', pov, 2); still('M_t2', tag, 2); still('M_f2', f13, 2)
color('M_end', (0, 0, 0), 4, note='the riser stops dead here')
color('BLACK2', (0, 0, 0), 24, kind='silence')
clip('I3', '25a_I3__sdfast', 0.3, 60, osd=OV.osd('room', H, EP(2026, 2, 10, 14, 31, 40), cam='INTERVIEW 3  CAM B', alpha=0.7))
clip('I4', '25b_I4__kling', 0.6, 96, osd=OV.osd('room', H, EP(2026, 2, 10, 14, 31, 43), cam='INTERVIEW 3', alpha=0.7),
     note='looks at the hand, eyes rise, recognition')
title = (f"drawtext=fontfile={BOLD}:text='EXHIBIT 47':fontcolor=white:fontsize={int(H * 0.075)}:x=w*0.07:y=h*0.44:"
         f"shadowcolor=black@0.8:shadowx=2:shadowy=2:enable='gte(t,0.6)'")
clip('TITLE', E2, 1.6, 72, extra=title, ovl=tagged(1.6), title_at=0.6)
card('CN', ['COMING NEVER'], 60, size=0.06, sub='AKOOL')
for k in range(3):                                         # the thirteenth feed's red dot, still recording
    card(f'DOT{k}', [''], 11, dot=(W // 2, H // 2)); color(f'DOT{k}x', (0, 0, 0), 8)
card('DOTHOLD', [''], 27, dot=(W // 2, H // 2))

# ---------------------------------------------------------------- concat + timeline
inp = []
for sp in segs:
    inp += ['-i', sp]
run(['ffmpeg', '-y'] + inp + ['-filter_complex', ''.join(f'[{i}:v]' for i in range(len(segs))) +
     f'concat=n={len(segs)}:v=1:a=0,fps={FPS}[v]', '-map', '[v]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
     '-pix_fmt', 'yuv420p', OUT])
total = pos[0] / FPS
json.dump({'fps': FPS, 'size': [W, H], 'duration': total, 'segments': TL},
          open(os.path.splitext(OUT)[0] + '.timeline.json', 'w'), indent=1)
d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', OUT],
                         capture_output=True, text=True).stdout)
print(len(segs), 'segments,', round(d, 2), 's (timeline', round(total, 3), 's)')
