"""Shot I3 keyframe: composite the approved Ward hand (sheet v2, panel 1) onto the AKOOL table plate.
    python3 comp_i3.py PLATE.jpg WARD_HAND_SHEET_V2.png OUT.jpg
Image-to-image re-posed the hand and redrew the scar every time, so the hand is pasted from the sheet
to keep the scar identical to the gloved hand in C2. Panel 1 = x 0..681 of the 2752x1536 sheet."""
import sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

plate_path, sheet_path, out_path = sys.argv[1:4]
plate = Image.open(plate_path).convert("RGB").resize((1920, 1080))

# 1. panel 1, trimmed off the gutter, turned so the cuff is at the top and the fingers point down
p = Image.open(sheet_path).convert("RGB").crop((0, 0, 681, 1340))
p = p.crop((14, 0, p.width - 14, p.height)).rotate(180)
a = np.asarray(p).astype(float)
H, W, _ = a.shape

# 2. key out the grey backdrop: flood-fill backdrop-like pixels from the borders
bg = np.asarray(p.filter(ImageFilter.GaussianBlur(60))).astype(float)
sat = a.max(axis=2) - a.min(axis=2)
cand = (sat < 18) & (np.abs(a - bg).sum(axis=2) < 40)
mask = np.zeros((H, W), bool)
q = deque((y, x) for x in range(W) for y in (0, H - 1) if cand[y, x])
q.extend((y, x) for y in range(H) for x in (0, W - 1) if cand[y, x])
for y, x in q: mask[y, x] = True
while q:
    y, x = q.popleft()
    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
        if 0 <= ny < H and 0 <= nx < W and cand[ny, nx] and not mask[ny, nx]:
            mask[ny, nx] = True; q.append((ny, nx))
alpha = np.asarray(Image.fromarray((~mask * 255).astype("uint8")).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(2))).astype(float) / 255

# 3. grey shadow left inside the cut (not the watch) becomes a multiply shadow instead of paint
lum = a.mean(axis=2)
watch = np.zeros_like(alpha, bool); watch[200:320, 100:430] = True
greyish = (sat < 16) & (lum > 60) & ~watch
shadow = np.where(greyish, np.clip(1 - lum / 165.0, 0, 1), 0) * alpha
alpha = np.where(greyish, 0, alpha)

# 4. grade toward the plate: a little cooler and less saturated
g = a.mean(axis=2, keepdims=True)
rgb = (g + (a - g) * 0.85) * np.array([0.96, 0.99, 1.04])
hand = Image.fromarray(np.dstack([rgb.clip(0, 255), alpha * 255]).astype("uint8"), "RGBA")
shad = Image.fromarray((shadow * 255).astype("uint8"), "L")

# 5. scale and turn like the whitebox guide (sleeve from the top, fingers down-left), add a contact shadow
s = 1180 / H
size = (int(W * s), int(H * s))
hand = hand.resize(size, Image.LANCZOS).rotate(-18, expand=True, resample=Image.BICUBIC)
shad = shad.resize(size).rotate(-18, expand=True)
x0, y0 = 1920 // 2 - hand.width // 2 + 40, -40
sil = hand.split()[3].filter(ImageFilter.GaussianBlur(28))
d1 = Image.new("L", plate.size, 0); d1.paste(sil, (x0 + 18, y0 + 26))
d2 = Image.new("L", plate.size, 0); d2.paste(shad, (x0, y0))
d = np.asarray(d1).astype(float) / 255 * 0.35 + np.asarray(d2).astype(float) / 255 * 0.6
base = Image.fromarray((np.asarray(plate).astype(float) * (1 - d[..., None].clip(0, 0.8))).clip(0, 255).astype("uint8"))
base.paste(hand, (x0, y0), hand)
base.save(out_path, quality=93)
