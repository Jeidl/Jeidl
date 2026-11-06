"""Assemble the 89-second whitebox animatic from the per-shot renders.

    python3 previs/compose_animatic.py META.json FRAMES_DIR OUT.mp4 [STORYBOARD.jpg]

META.json comes from `exhibit47_whitebox.py -- --meta`, FRAMES_DIR from `--render`.
Needs Pillow and ffmpeg. Cards, the 4x3 monitor wall, the montage and all
overlays are drawn here, as they will be in the real edit.
"""
import json, os, sys, glob, subprocess
from PIL import Image, ImageDraw, ImageFont

META, FRAMES, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SHEET = sys.argv[4] if len(sys.argv) > 4 else None
W, H, FPS = 640, 360, 24
BAR = 22                                    # top title bar (holds the AKOOL logo in the edit)
meta = json.load(open(META))
SHOTS = {s["n"]: s for s in meta["shots"]}
EDIT = meta["edit"]
EVENTS = meta["events"]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
f_small, f_mono, f_card, f_tile = ImageFont.truetype(FONT, 11), ImageFont.truetype(MONO, 11), ImageFont.truetype(BOLD, 24), ImageFont.truetype(MONO, 9)
CACHE = {}

def fr(t):
    return int(round(t * FPS)) + 1

def shot_frame(n, t):
    """Image of shot n at master time t (clamped to the shot window)."""
    s = SHOTS[n]
    t = min(max(t, s["t0"]), s["t1"] - 1e-3)
    files = CACHE.get(n)
    if files is None:
        files = sorted(glob.glob(os.path.join(FRAMES, n, "f_*.png")))
        CACHE[n] = files
    if not files:
        return Image.new("RGB", (W, H), (40, 0, 0))
    want = fr(t)
    best = files[0]
    for fp in files:
        if int(os.path.basename(fp)[2:7]) <= want:
            best = fp
        else:
            break
    return Image.open(best).convert("RGB").resize((W, H))

def card(lines, red_dot=False):
    im = Image.new("RGB", (W, H), "black")
    d = ImageDraw.Draw(im)
    ys = H // 2 - 16 * len(lines)
    for i, ln in enumerate(lines):
        f = f_card if i == 0 else f_small
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2, ys + i * 34), ln, fill=(237, 232, 224), font=f)
    if red_dot:
        d.ellipse((W / 2 - 5, H / 2 - 5, W / 2 + 5, H / 2 + 5), fill=(230, 20, 10))
    return im

# feed -> (source shot, offset into it, loop length or None for the whole shot)
TILE_SRC = {"7-01": ("05", 0.0, None), "7-02": ("13", 0.0, None), "7-03": ("15", 0.0, None), "7-04": ("19a", 0.0, None),
            "7-05": ("19b", 0.0, None), "7-06": ("13", 2.0, None), "7-07": ("19e", 0.0, None), "7-08": ("19g", 0.0, None),
            "7-09": ("17", 0.0, None), "7-10": ("13", 1.0, None), "7-11": ("15", 1.0, None),
            "7-12": ("10", 0.0, 1.9)}   # Nora's feed: only before the swing, so the 13th never shows on the wall
THIRTEENTH_SHOTS = {"10": "13TH #1", "19i": "13TH #2 mirror", "21": "13TH #3 hand", "25a": "13TH #4 identity: same scar"}
ORDER = list(TILE_SRC)

def grid(t, rel, lost, thirteenth=None):
    im = Image.new("RGB", (W, H), "black")
    th = (H - BAR - 36 - 10) // 4             # 3 rows of the wall + 1 row for the 13th feed
    tw = th * 16 // 9
    x0 = (W - (4 * tw + 6)) // 2
    d = ImageDraw.Draw(im)
    for i, cam in enumerate(ORDER):
        x, y = x0 + (i % 4) * (tw + 2), BAR + 2 + (i // 4) * (th + 2)
        if cam in lost:
            d.rectangle((x, y, x + tw, y + th), fill=(8, 8, 8))
            d.text((x + tw / 2 - 30, y + th / 2 - 5), "SIGNAL LOST", fill=(200, 200, 200), font=f_tile)
        else:
            n, off, loop = TILE_SRC[cam]
            s = SHOTS[n]
            span = loop or (s["t1"] - s["t0"])
            src = shot_frame(n, s["t0"] + (off + rel) % span).convert("L").convert("RGB").resize((tw, th))
            im.paste(src, (x, y))
        d.text((x + 3, y + 2), cam, fill=(255, 255, 255), font=f_tile)
    if thirteenth is not None:
        alpha, blink = thirteenth
        x, y = (W - tw) // 2, BAR + 2 + 3 * (th + 2) + 2
        src = shot_frame("19h", SHOTS["19h"]["t0"] + rel % 1.4).convert("L").convert("RGB").resize((tw, th))
        black = Image.new("RGB", src.size, "black")
        im.paste(Image.blend(black, src, alpha), (x, y))
        d.text((x + 3, y + 2), "UNKNOWN", fill=(255, 255, 255), font=f_tile)
        if blink:
            d.ellipse((x + tw - 10, y + 3, x + tw - 4, y + 9), fill=(230, 20, 10))
    return im

def grid_state(n, t):
    s0 = [e for e in EDIT if e[0] == n][0][1]
    rel = t - s0
    if n == "12":
        lost = {c for c, at in (("7-03", 0.7), ("7-09", 1.5)) if rel >= at}
        return grid(t, rel, lost)
    if n == "19f":
        lost = {"7-03", "7-09"} | ({"7-01", "7-05", "7-10"} if rel >= 0.1 else set())
        return grid(t, rel, lost)
    lost = set(ORDER[:-1]) | ({"7-12"} if rel >= 0.6 else set())   # shot 20
    if rel < 2.1:
        return grid(t, rel, lost)
    a = min(1.0, (rel - 2.1) / 0.8)
    return grid(t, rel, lost, thirteenth=(a, int(rel * 3) % 2 == 0))

ENH = meta.get("enhance", {})

def zoom(im, x, y, f, label, tag_text=None):
    """Freeze-frame 'enhance': crop around (x, y) (0..1 from the top-left) and scale up."""
    cw, ch = W / f, H / f
    cx = min(max(x * W, cw / 2), W - cw / 2)
    cy = min(max(y * H, ch / 2), H - ch / 2)
    out = im.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H))
    d = ImageDraw.Draw(out)
    px, py = (x * W - (cx - cw / 2)) * f, (y * H - (cy - ch / 2)) * f
    d.rectangle((px - 40, py - 28, px + 40, py + 28), outline=(255, 255, 255), width=2)
    if tag_text:
        w = d.textlength(tag_text, font=f_card)
        d.text((px - w / 2, py - 14), tag_text, fill=(245, 240, 230), font=f_card)
    d.rectangle((0, BAR, 230, BAR + 18), fill=(0, 0, 0))
    d.text((6, BAR + 3), f"ENHANCE x{f:.1f} · {label}", fill=(255, 255, 255), font=f_mono)
    return out

def montage(t, data, s0):
    segs = [(p.split(":")[0], float(p.split(":")[1])) for p in data.split(",")]
    rel, acc = t - s0, 0.0
    for name, dur in segs:
        if rel < acc + dur or (name, dur) == segs[-1]:
            r = rel - acc
            u = min(1.0, r / dur)
            if name == "10pre":
                return shot_frame("10", 23.0 + r), "B2 before the swing"
            if name == "grid13":
                im = grid(t, 3.0, set(ORDER), thirteenth=(1.0, int(r * 6) % 2 == 0))
                return im, "the 13th feed: UNKNOWN"
            if name.endswith("z") and name in ENH:
                e = ENH[name]
                src = shot_frame(e["shot"], e["t"])
                tag = "EXHIBIT 47" if name == "09z" else None
                return zoom(src, e["x"], e["y"], 2.2 + 1.6 * u, e["label"], tag), f"{SHOTS[e['shot']]['code']} enhance: {e['label']}"
            return shot_frame(name, SHOTS[name]["t0"] + r), SHOTS[name]["code"]
        acc += dur

def register_card(rel):
    im = Image.new("RGB", (W, H), "black")
    d = ImageDraw.Draw(im)
    ink, dim, red = (237, 232, 224), (150, 150, 150), (225, 30, 20)
    x, y = 70, 92
    d.text((x, y), "NORTHGATE SHOOTING · 3 YEARS AGO", fill=dim, font=f_mono)
    d.text((x, y + 20), "EVIDENCE REGISTER", fill=ink, font=f_mono)
    d.line((x, y + 40, W - 70, y + 40), fill=dim)
    rows = [("45", "9 MM SHELL CASINGS (9)", ""), ("46", "HANDGUN, RECOVERED AT SCENE", ""), ("47", "BODY CAMERA · UNIT 7-12", "LOST")]
    for i, (no, item, st) in enumerate(rows):
        yy = y + 54 + i * 26
        d.text((x, yy), no, fill=ink, font=f_mono)
        d.text((x + 40, yy), item, fill=ink, font=f_mono)
        if st and rel >= 1.2:
            d.rectangle((W - 150, yy - 4, W - 72, yy + 16), outline=red, width=2)
            d.text((W - 136, yy), st, fill=red, font=f_mono)
    return im

def overlay(im, t, label, sub=""):
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, BAR), fill="black")
    d.text((6, 5), "EXHIBIT 47 · WHITEBOX PREVIS", fill=(200, 200, 200), font=f_small)
    d.rectangle((W - 64, 4, W - 6, BAR - 4), outline=(200, 200, 200))
    d.text((W - 58, 5), "AKOOL", fill=(200, 200, 200), font=f_small)
    m, s = divmod(t, 60)
    txt = f"{int(m)}:{s:04.1f}  {label}"
    if sub:
        if len(sub) > 100:
            sub = sub[:97] + "..."
        d.rectangle((0, H - 34, W, H - 18), fill=(0, 0, 0))
        d.text((6, H - 31), sub, fill=(255, 210, 120), font=f_small)
    d.rectangle((0, H - 18, W, H), fill=(0, 0, 0))
    d.text((6, H - 15), txt[:100], fill=(255, 255, 255), font=f_mono)
    return im

def event_at(n, t):
    best = None
    for sn, et, desc in EVENTS:
        if sn == n and et - 0.05 <= t <= et + 0.9:
            best = desc
    return best or ""

def frame_at(t):
    for n, s0, dur, kind, data in EDIT:
        if s0 <= t < s0 + dur:
            break
    else:
        return Image.new("RGB", (W, H), "black"), "end"
    if kind == "shot":
        s = SHOTS[data]
        im = shot_frame(data, t)
        sub = event_at(data, t)
        if data == "24" and t >= s0 + 0.4:      # title card: the text goes on the evidence tag in the edit
            d = ImageDraw.Draw(im)
            w = d.textlength("EXHIBIT 47", font=f_card)
            d.text(((W - w) / 2, H / 2 - 30), "EXHIBIT 47", fill=(245, 240, 230), font=f_card)
        tag = f"  [{THIRTEENTH_SHOTS[data]}]" if data in THIRTEENTH_SHOTS else ""
        return overlay(im, t, f"#{n} {s['code']}  {s['style']} {s['lens']:.0f}mm  (clip {t - s0:.1f}s){tag}", sub), n
    if kind == "grid":
        return overlay(grid_state(n, t), t, f"#{n} GRID 4x3"), n
    if kind == "montage":
        im, what = montage(t, data, s0)
        return overlay(im, t, f"#22 MONTAGE  {what}"), n
    if kind == "register":
        return overlay(register_card(t - s0), t, f"#{n} CARD  evidence register"), n
    parts = data.split("|")
    lines = [p for p in parts if p and not p.startswith(("flash:", "dot"))]
    if n == "01":
        im = card(["AKOOL", "(logo card)"])
    elif "flash:S2" in parts and t >= s0 + dur - 3 / FPS:
        im = shot_frame("S2", 95.0)
    else:
        rel = t - s0
        blink = "dotlong" in parts and (0.5 <= rel < 0.9 or 1.3 <= rel < 1.7 or 2.1 <= rel < 3.3)
        im = card(lines or [""], red_dot=blink)
    return overlay(im, t, f"#{n} CARD"), n

def main():
    total = max(s0 + d for _, s0, d, _, _ in EDIT)
    n_frames = int(round(total * FPS))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", OUT], stdin=subprocess.PIPE)
    thumbs = {}
    for i in range(n_frames):
        t = i / FPS
        im, n = frame_at(t)
        p.stdin.write(im.tobytes())
        e = [e for e in EDIT if e[0] == n]
        if e and n not in thumbs and t >= e[0][1] + e[0][2] / 2:
            thumbs[n] = im.copy()
    p.stdin.close()
    p.wait()
    if SHEET:
        cols, tw, th = 6, 320, 180
        keys = [e[0] for e in EDIT]
        rows = (len(keys) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * th), "black")
        for k, n in enumerate(keys):
            if n in thumbs:
                sheet.paste(thumbs[n].resize((tw, th)), ((k % cols) * tw, (k // cols) * th))
        sheet.save(SHEET, quality=88)

if __name__ == "__main__":
    main()
