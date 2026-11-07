"""Paint a rectangle out of a keyframe by mirroring the texture just above it.

Used once for v2 shot 21_C2_start: AKOOL drew an on-screen text box in the
top-left corner of the CCTV frame. The AKOOL edit that removed it also lost the
infrared noise, so the original was kept and the box painted out here.

    python3 paint_out_box.py IN.jpg OUT.jpg X0 Y0 X1 Y1
    python3 paint_out_box.py 21_C2_start.jpeg 21_C2_start_fix.jpeg 66 44 258 103

The box must sit at least (Y1 - Y0) / 2 pixels below the top edge.
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(int, sys.argv[3:7])
im = Image.open(src).convert("RGB")
h = y1 - y0
filled = 0
while filled < h:  # stack mirrored strips from above the box until it is covered
    n = min(y0, h - filled)
    im.paste(ImageOps.flip(im.crop((x0, y0 - n, x1, y0))), (x0, y0 + filled))
    filled += n
# soften the seam around the patch
pad = 4
band = im.crop((x0 - pad, y0 - pad, x1 + pad, y1 + pad)).filter(ImageFilter.GaussianBlur(1))
mask = Image.new("L", band.size, 0)
ImageDraw.Draw(mask).rectangle((0, 0, band.width - 1, band.height - 1), outline=255, width=6)
im.paste(band, (x0 - pad, y0 - pad), mask)
im.save(dst, quality=95)
