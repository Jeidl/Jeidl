"""EXHIBIT 47 rough cut v4: the picture (about 86 s, 24 fps), evidence readable and every source believable.

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

v4 answers the third review:
- the wall is a command-post LIVE UPLINK with a header clock: every cell shows the same moment
  (04:09 calm search, 05:02 the firefight, 05:12 only Nora's link), no feed repeats another
  camera's view, links already lost read SIGNAL LOST; the cameras still record on the device;
- FEED 13 (UNREGISTERED DEVICE, AX-118 S/N 0412, its own running clock) shows new footage after
  every link is dead: from between the crates, the cold-room door as Nora stumbles in;
- the scar shot is CAM 11 itself, zoomed 4x in playback (a chest camera cannot look down at its
  own chest): the hand comes out of the crates, Nora turns to look at it, and the scar is Ward's
  scar from I3, traced and composited in the same direction through a ragged rip in the glove;
- C2's pull is re-made without sparks, so the room no longer relights or changes; the sparks are
  composited on the door frame instead;
- LOST is on the register from the first frame; the logo card no longer says "goes here";
- the interview recorder names SUBJECT N. KADE (7-12) and INTERVIEWER INSP. E. WARD, so the hand
  in I3 belongs to someone the viewer has already been told about;
- each device has its own look as well as its label (overlays.LOOK): body cams wide and vignetted,
  the old AX-118 half-resolution amber, CCTV at 12 fps;
- the montage is evidence only (scar, 47, LOST, red light, FEED 13, the boy's hands), each already
  shown clearly once, shorter and shorter; ENDING=B renders the shorter, quieter ending.


Needs ffmpeg, numpy and Pillow. Stills come from previs/keyframes/v2/frames. Cards are
placeholders (Liberation Sans); the AKOOL card still needs the official logo."""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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
# The wall is the command post's LIVE UPLINK from Team 7's twelve body cams (FEED 01-12, all
# body-worn; CCTV never appears on it). Every cell shows the same moment, given by the header
# clock. "SIGNAL LOST" means the link is gone; the cameras keep recording on the device, which
# is why their footage exists. FEED 12 is Nora's (call sign 7-12), the last link to die.
HDR = int(H * 0.065)
CW, CH = W // 4, (H - HDR) // 3
WALL1 = [('05_B1__akp', 3.5), ('19a_B5__akp', 2.5), ('13_B3__akp', 0.5), ('19b_B9__akp', 0.2), None, ('19d_B10__akp', 2.5),
         None, None, None, None, None, ('10_B2a__sdfast', 0.6)]          # 04:09, searching, nothing yet; every live cell a different camera
WALL2 = [('19a_B5__sdfast', 0.2), None, None, ('19e_B6__akp', 0.2), None, ('19d_B10__akp', 0.2),
         None, None, None, None, None, ('15_B4__sdfast', 0.2)]                             # 05:02, the firefight
WALL3 = [None] * 11 + [('19e_B6__sdfast', 3.5)]                                           # 05:12, only Nora's link left


def cell_frames(name, t0, frames, w, h):
    """Frames of a clip for one cell; if the clip runs out, the feed freezes on its last frame."""
    d = tempfile.mkdtemp(dir=T) + '/'
    run(['ffmpeg', '-y', '-ss', str(t0), '-i', C + name + '.mp4', '-frames:v', str(frames),
         '-vf', f'fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}', d + 'c_%04d.png'])
    ims = [Image.open(d + f).convert('RGB') for f in sorted(os.listdir(d))]
    return ims + [ims[-1]] * (frames - len(ims)) if ims else [None] * frames


def wall(frames, feeds, lost, ep, feed13=None):
    """feeds: 12 x (clip, in-point) or None (link already lost); lost = {index: frame it dies};
    ep: header clock at frame 0; feed13 = (clip, in-point, its own clock) for the extra feed."""
    fm = ImageFont.truetype(MONO, int(CH * 0.085)); fl = ImageFont.truetype(BOLD, int(CH * 0.11))
    fh_ = ImageFont.truetype(MONO, int(HDR * 0.5))
    live = [cell_frames(f[0], f[1], frames, CW, CH) if f else None for f in feeds]
    fw, fh = int(CW * 1.5), int(CH * 1.5)
    x13 = cell_frames(feed13[0], feed13[1], frames, fw, fh) if feed13 else None
    out = []
    for k in range(frames):
        im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
        t = OV.datetime.datetime.fromtimestamp(ep + k / FPS, OV.datetime.timezone.utc)
        d.rectangle((0, 0, W, HDR - 1), fill=(18, 18, 18))
        d.text((12, HDR * 0.22), 'NPD COMMAND   TEAM 7   LIVE UPLINK', font=fh_, fill=(236, 232, 224))
        ts = t.strftime('%Y-%m-%d %H:%M:%S'); d.text((W - 12 - d.textlength(ts, font=fh_), HDR * 0.22), ts, font=fh_, fill=(236, 232, 224))
        for i in range(12):
            x, y = (i % 4) * CW, HDR + (i // 4) * CH
            dead = live[i] is None or (i in lost and k >= lost[i])
            if dead:
                d.rectangle((x, y, x + CW - 1, y + CH - 1), fill=(0, 0, 0))
                tt = 'SIGNAL LOST'; w = d.textlength(tt, font=fl)
                d.text((x + (CW - w) / 2, y + CH / 2 - CH * 0.06), tt, font=fl, fill=(170, 170, 170))
            elif live[i][k] is not None:
                im.paste(live[i][k], (x, y))
            d.rectangle((x, y, x + CW - 1, y + CH - 1), outline=(40, 40, 40))
            d.text((x + 6, y + 4), f'FEED {i + 1:02d}', font=fm, fill=(120, 120, 120) if dead else (230, 230, 230))
        if feed13 and k >= 2:                                   # two frames of nothing, then it is just there
            x0, y0 = (W - fw) // 2, HDR + (H - HDR - fh) // 2
            if x13[k] is not None:
                im.paste(x13[k], (x0, y0))
            d.rectangle((x0 - 2, y0 - 2, x0 + fw + 1, y0 + fh + 1), outline=(236, 232, 224), width=2)
            fb = ImageFont.truetype(MONO, int(fh * 0.07)); big = ImageFont.truetype(BOLD, int(fh * 0.20))
            d.rectangle((x0, y0, x0 + fw, y0 + int(fh * 0.11)), fill=(0, 0, 0))
            d.text((x0 + 8, y0 + 4), 'FEED 13   UNREGISTERED DEVICE', font=fb, fill=(236, 232, 224))
            d.text((x0 + 10, y0 + int(fh * 0.13)), '13', font=big, fill=(236, 232, 224))
            ct = OV.datetime.datetime.fromtimestamp(feed13[2] + k / FPS, OV.datetime.timezone.utc).strftime('%m/%d/%Y %H:%M:%S')
            d.text((x0 + 8, y0 + fh - int(fh * 0.1)), f'AX-118  S/N 0412   {ct}', font=fb, fill=(232, 200, 96))
            if (k // 12) % 2 == 0:
                r = int(fh * 0.03); cx, cy = x0 + fw - 18, y0 + int(fh * 0.055)
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(224, 40, 28))
        out.append(im)
    return out


def wall_seg(sid, frames, feeds, lost, ep, feed13=None, **meta):
    ims = wall(frames, feeds, lost, ep, feed13)
    d = tempfile.mkdtemp(dir=T) + '/'
    for k, im in enumerate(ims):
        im.save(f'{d}g_{k:04d}.png')
    o = new_seg()
    run(['ffmpeg', '-y', '-framerate', str(FPS), '-i', d + 'g_%04d.png', '-vf', VF] + ENC + [o])
    meta.setdefault('kind', 'wall')
    add(sid, o, frames, **meta)
    return ims


# ---------------------------------------------------------------- shared material
E2 = '24_E2__sdfast720'
tag_at = OV.tag_frames(OVL + E2 + '.track.json', W, H)


def tagged(src_in):
    """Overlay function for E2 starting at src_in: the tag text where the tag is."""
    return lambda i: tag_at(int(round(src_in * FPS)) + i)


reg_frame = frame_of('18_E3_register__sdfast', 1.0)
reg_text, reg_stamp = OV.register_layers(reg_frame.resize((1280, 720)), 1280, 720)
reg_text, reg_stamp = reg_text.resize((W, H)), reg_stamp.resize((W, H))
reg_all = reg_text.copy(); reg_all.alpha_composite(reg_stamp)       # LOST is on the page from the start: it is part of the evidence
REG_FRAMES = 89
LOOK = OV.LOOK
bwc = lambda unit, ep: OV.osd('bwc', H, ep, unit)
old = lambda ep, unit='7-12': OV.osd('old', H, ep, unit)
room = lambda ep, cam: OV.osd('room', H, ep, cam=cam, alpha=0.75)
CCTV_IR = 'hue=s=0,eq=contrast=1.06,' + LOOK['cctv']
REFRAME_B8 = f'crop=iw*0.8:ih*0.8:iw*0.2:ih*0.121,scale={W}:{H}'   # puts the reflection's red light on the lens axis
zoom = Image.open(KF + '21_C2_cam11_zoom.jpg').convert('RGB')     # CAM 11 played back at 4x: the hand, the scar, Nora looking at it
ENDING = os.environ.get('ENDING', 'A')                               # A: hand 2.5 s, Nora 4 s; B: shorter, cut on the eyes


def sparks(i0, n=4):
    """A burst on the door frame where Nora stood (composited: the generator relit the whole room when asked for it)."""
    import random
    rnd = random.Random(7)

    def at(i):
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        k = i - i0
        if 0 <= k < n:
            a = [1.0, 0.65, 0.35, 0.15][k]
            d = ImageDraw.Draw(im); cx, cy = int(W * 0.745), int(H * 0.40)
            for rr in range(int(W * 0.10), 0, -6):
                d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 255, 255, int(255 * a * (1 - rr / (W * 0.10)) ** 2)))
            for _ in range(14):
                ang = rnd.uniform(0, 6.28); ln = rnd.uniform(W * 0.02, W * 0.07) * (1 + k * 0.4)
                d.line((cx, cy, cx + ln * OV.np.cos(ang), cy + ln * OV.np.sin(ang)), fill=(255, 255, 255, int(220 * a)), width=2)
        return im.filter(ImageFilter.GaussianBlur(1.2))
    return at


# ---------------------------------------------------------------- ACT 1: 12 -> 1 -> 13 (by 11.6 s)
card('LOGO', ['AKOOL'], 36, size=0.09)                               # placeholder until the official logo file is in
clip('C3', '04_C3__sdfast', 0.6, 72, extra=LOOK['cctv'], osd=OV.osd('cctv', H, EP(2026, 2, 9, 3, 59, 38), cam='CAM 02  NORTHGATE COLD STORE'))
card('CARD12', ['12 OFFICERS WENT IN.'], 29)
clip('B1', '05_B1__sdfast', 1.65, 29, extra=LOOK['bwc'], osd=bwc('7-04', EP(2026, 2, 9, 4, 1, 5)), note='swing, hit at +0.56 s, door gives')
color('B1F', (232, 232, 228), 2, note='flare over the cut past the second swing')
clip('B1b', '05_B1__sdfast', 3.70, 22, extra=LOOK['bwc'], osd=bwc('7-04', EP(2026, 2, 9, 4, 1, 9)), note='team goes in')
card('CARD1', ['1 CAME OUT.'], 29)
clip('D1', '02_D1__akp', 0.0, 60, osd=OV.osd('drone', H, EP(2026, 2, 9, 7, 40, 12)), note='07:40, the survivor walks out')
card('CARD13', ['13 CAMERAS WERE RECOVERED.'], 36)
clip('E1', '09_E1__sdfast720', 1.5, 60)
clip('I1', '07_I1__sdfast', 0.2, 60, osd=room(EP(2026, 2, 10, 14, 22, 5), 'INTERVIEW 3'), note='the survivor, named; the interviewer, named')
# B2 is Nora's own camera (7-12): count off, she says twelve, then the view swings to the back of the line
clip('B2', '10_B2a__sdfast', 0.4, 58, extra=LOOK['bwc'], osd=bwc('7-12', EP(2026, 2, 9, 4, 3, 8)), note='descent, count off')
clip('B2w', '10_B2b__akp', 0.0, 12, extra=LOOK['bwc'], osd=bwc('7-12', EP(2026, 2, 9, 4, 3, 10)), note='whip to the back of the line')
clip('B2h', '10_B2b__sdfast', 0.3, 26, extra=LOOK['bwc'], osd=bwc('7-12', EP(2026, 2, 9, 4, 3, 11)), note='the 13th, red light on')
color('BLACK1', (0, 0, 0), 12)
wall_seg('GRID1', 72, WALL1, {2: F(1.2), 1: F(2.0)}, EP(2026, 2, 9, 4, 9, 12), note='04:09 live: FEED 03 and 02 die')

# ---------------------------------------------------------------- ACT 2: the camera that should not exist
clip('B3', '13_B3__akp', 0.3, 72, extra=LOOK['bwc'], osd=bwc('7-07', EP(2026, 2, 9, 4, 9, 31)))
card('CARD_ONLY12', ['ONLY 12 CAMERAS WERE ISSUED.'], 48)
clip('B4', '15_B4_quiet__sdfast', 1.2, 60, extra=LOOK['bwc'], osd=bwc('7-09', EP(2026, 2, 9, 4, 38, 2)), note='restrained; mouth moves +0.46-1.17 s')
card('CARD_DEAD', ['ONE CAMERA BELONGED', 'TO A DEAD MAN.'], 45)
clip('O1F', 'S2_O1__akp', 1.0, 3, extra=LOOK['old'], osd=OV.osd('archive', H, EP(2023, 2, 9, 1, 11, 2), '7-12'))
clip('O2', '17_O2__sdfast', 1.5, 60, extra=LOOK['old'], osd=OV.osd('archive', H, EP(2023, 2, 9, 1, 12, 40), '7-05'), note='2023: they switch their cameras off')
push = (f"scale={W * 2}:{H * 2},zoompan=z='1+0.30*on/{REG_FRAMES}':"
        f"x='max(0,min(iw-iw/zoom,(0.5+0.23*on/{REG_FRAMES})*iw-iw/zoom/2))':"
        f"y='max(0,min(ih-ih/zoom,(0.5-0.17*on/{REG_FRAMES})*ih-ih/zoom/2))':d=1:s={W}x{H}:fps={FPS},"
        f"avgblur=sizeX={W // 24}:sizeY=1:enable='gte(n,{REG_FRAMES - 4})'")
clip('E3REG', '18_E3_register__sdfast', 0.5, REG_FRAMES, extra=push, ovl=lambda i: reg_all)
clip('E3TAG', E2, 2.2, 31, extra=f"avgblur=sizeX={W // 24}:sizeY=1:enable='lt(n,3)'", ovl=tagged(2.2), note='EXHIBIT 47 readable')
# the firefight: a retreat order, the gas cuts the stairs off, the wall dies
clip('B5', '19a_B5__sdfast', 0.6, 24, extra=LOOK['bwc'], osd=bwc('7-03', EP(2026, 2, 9, 5, 2, 44)), flash=True)
clip('B9', '19b_B9__sdfast720', 1.4, 24, extra=LOOK['bwc'], osd=bwc('7-06', EP(2026, 2, 9, 5, 2, 46)), flash=True, note='hit at +0.5 s, flashlight lands +0.7 s')
clip('C1', '19c_C1__sdfast720', 3.0, 24, extra='hue=s=0.2,eq=contrast=1.08:brightness=-0.03,' + LOOK['cctv'],
     osd=OV.osd('cctv', H, EP(2026, 2, 9, 5, 2, 48), cam='CAM 07  HALL B'), flash=True)
clip('B10', '19d_B10__akp', 0.4, 24, extra=LOOK['bwc'], osd=bwc('7-01', EP(2026, 2, 9, 5, 2, 50)))
clip('B6', '19e_B6__sdfast', 0.5, 30, extra=LOOK['bwc'], osd=bwc('7-10', EP(2026, 2, 9, 5, 2, 53)), note='pipe bursts: the way to the stairs is gas')
wall_seg('GRID2', 24, WALL2, {3: F(0.2), 0: F(0.5), 5: F(0.8)}, EP(2026, 2, 9, 5, 2, 55), note='05:02 live: FEED 04, 01, 06 die')
clip('B7', '19g_B7__sdfast720', 1.0, 36, extra=LOOK['bwc'], osd=bwc('7-11', EP(2026, 2, 9, 5, 4, 2)), note='Brandt loses it')
clip('X1', '19h_X1__sdfast', 1.0, 36, extra=LOOK['old'], osd=old(EP(2026, 2, 9, 5, 6, 51)), note='the 13th: AX-118, calm')
clip('B8s', '19i_B8_start__akp', 2.8, 17, extra=LOOK['old'], osd=old(EP(2026, 2, 9, 5, 10, 14)))
clip('B8r', '19i_B8_reflection__sdfast720', 1.0, 31, extra=REFRAME_B8 + ',' + LOOK['old'], osd=old(EP(2026, 2, 9, 5, 10, 15)),
     note='the wearer of the old camera, seen in the steel: its red light on the lens axis')
wall_seg('GRID3', 24, WALL3, {11: F(0.6)}, EP(2026, 2, 9, 5, 12, 6), note='05:12:06 live: FEED 12 (Nora) dies last')
wall_seg('DEAD', 36, [None] * 12, {}, EP(2026, 2, 9, 5, 12, 7), kind='silence')
wall_seg('FEED13', 54, [None] * 12, {}, EP(2026, 2, 9, 5, 12, 8) + 0.5, feed13=('S3_feed13__sdfast720', 1.0, EP(2026, 2, 9, 5, 12, 10)),
         note='after every link is dead, a thirteenth feed: from between the crates, watching the cold-room door')
# C2: CAM 11 from the empty room to the empty room; the scar seen on a 4x playback zoom of the same camera
cam11 = lambda s: OV.osd('cctv', H, EP(2026, 2, 9, 5, 12, s), cam='CAM 11  COLD ROOM 4')
PULL = '21_C2_pull2a__sdfast'
clip('C2e', '21_C2_enter__sdfast', 1.6, 38, extra=CCTV_IR, osd=cam11(31))
color('C2d', (12, 12, 12), 2, note='CCTV dropout')
clip('C2g', PULL, 0.0, 14, extra=CCTV_IR, osd=cam11(34), note='the hand takes her vest strap')
zpush = f"zoompan=z='1+0.05*on/20':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={FPS}"
still('C2z', zoom, 20, extra=zpush, osd=OV.osd('cctv', H, EP(2026, 2, 9, 5, 12, 34), cam='CAM 11  PLAYBACK  ZOOM 4X'),
      note='same camera, zoomed in playback: the scar through the torn glove, Nora looking at it')
clip('C2p', PULL, 0.6, 72, extra=CCTV_IR, osd=cam11(35), ovl=sparks(9), note='sparks +0.38, off balance +1.0, dragged in +2.2, gone +2.8')

# ---------------------------------------------------------------- ACT 3: the evidence, then the man
tag = frame_of(E2, 3.4).convert('RGBA')
tag.alpha_composite(tag_at(int(3.4 * FPS)))
lost_img = reg_frame.resize((W, H)).convert('RGBA'); lost_img.alpha_composite(reg_all)
lost_img = lost_img.crop((int(W * 0.55), int(H * 0.15), int(W * 0.95), int(H * 0.15) + int(W * 0.4 * H / W))).resize((W, H))
refl = frame_of('19i_B8_reflection__sdfast720', 2.5, REFRAME_B8)
refl = refl.crop((int(W * 0.30), int(H * 0.25), int(W * 0.70), int(H * 0.25) + int(W * 0.4 * H / W))).resize((W, H))
f13 = wall(3, [None] * 12, {}, EP(2026, 2, 9, 5, 12, 9), feed13=('S3_feed13__sdfast720', 2.0, EP(2026, 2, 9, 5, 12, 11)))[2]
scar = zoom.crop((int(zoom.width * 0.22), int(zoom.height * 0.30), int(zoom.width * 0.62), int(zoom.height * 0.30) + int(zoom.width * 0.40 * 9 / 16))).resize((W, H))
clip('M_I2', 'S1_I2__talk', 0.2, 36, note='"There were thirteen of us." (the audio runs on)')
color('M_w1', (255, 255, 255), 2)
for sid, img, n_ in (('M_scar', scar, 8), ('M_b1', None, 2), ('M_tag', tag, 8), ('M_lost', lost_img, 6), ('M_refl', refl, 6), ('M_f13', f13, 6)):
    color(sid, (0, 0, 0), n_) if img is None else still(sid, img, n_)
clip('M_O1', 'S2_O1__akp', 0.5, 6, extra=LOOK['old'])
color('M_b2', (0, 0, 0), 2)
for sid, img, n_ in (('M_s2', scar, 4), ('M_t2', tag, 3), ('M_l2', lost_img, 3), ('M_f2', f13, 3), ('M_s3', scar, 2), ('M_t3', tag, 2), ('M_f3', f13, 2)):
    still(sid, img, n_)
color('M_end', (0, 0, 0), 4, note='the riser stops dead here')
color('BLACK2', (0, 0, 0), 24, kind='silence')
if ENDING == 'B':
    clip('I3', '25a_I3__sdfast', 0.3, 40, osd=room(EP(2026, 2, 10, 14, 31, 40), 'INTERVIEW 3  CAM B'))
    clip('I4', '25b_I4__kling', 1.0, 50, osd=room(EP(2026, 2, 10, 14, 31, 42), 'INTERVIEW 3'), note='cut as her eyes land on him')
else:
    clip('I3', '25a_I3__sdfast', 0.3, 60, osd=room(EP(2026, 2, 10, 14, 31, 40), 'INTERVIEW 3  CAM B'))
    clip('I4', '25b_I4__kling', 0.6, 96, osd=room(EP(2026, 2, 10, 14, 31, 43), 'INTERVIEW 3'), note='looks at the hand, eyes rise, recognition')
title = (f"drawtext=fontfile={BOLD}:text='EXHIBIT 47':fontcolor=white:fontsize={int(H * 0.075)}:x=w*0.07:y=h*0.44:"
         f"shadowcolor=black@0.8:shadowx=2:shadowy=2:enable='gte(t,0.6)'")
clip('TITLE', E2, 1.6, 72, extra=title, ovl=tagged(1.6), title_at=0.6)
card('CN', ['COMING NEVER'], 60, size=0.06, sub='AKOOL')
for k in range(3):                                         # the thirteenth feed's red dot: still recording
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
json.dump({'fps': FPS, 'size': [W, H], 'duration': total, 'ending': ENDING, 'segments': TL},
          open(os.path.splitext(OUT)[0] + '.timeline.json', 'w'), indent=1)
d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', OUT],
                         capture_output=True, text=True).stdout)
print(len(segs), 'segments,', round(d, 2), 's (timeline', round(total, 3), 's)')
