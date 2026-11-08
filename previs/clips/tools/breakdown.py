"""Timecoded breakdown of a trailer file (or of our own cut), measured, not remembered.

    python3 breakdown.py TRAILER.mp4 OUT_DIR [--from S] [--to S]

Writes to OUT_DIR:
  shots.csv     one row per shot: number, start, end, length (s and frames), mean brightness,
                whether it is a near-black frame (card or black), loudness at the cut
  events.csv    black stretches, silences (below -50 dB for 0.25 s or more), audio hits
                (short-term loudness jumps), each with its timecode
  sheet.jpg     one thumbnail per shot with its number and start time
Cuts come from ffmpeg's scene score (> 0.3) plus hard changes into or out of black.
It finds where things happen; why they happen there is still the reader's job.
Needs ffmpeg, numpy and Pillow."""
import csv, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
args = sys.argv[3:]
t0 = float(args[args.index('--from') + 1]) if '--from' in args else 0.0
t1 = float(args[args.index('--to') + 1]) if '--to' in args else None
os.makedirs(out, exist_ok=True)
rng = ['-ss', str(t0)] + (['-t', str(t1 - t0)] if t1 else [])
fps = eval(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                           '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip())
tc = lambda s: f'{int(s // 60)}:{s % 60:05.2f}'

# picture: per-frame brightness and scene score
log = subprocess.run(['ffmpeg', '-hide_banner'] + rng + ['-i', src, '-vf',
                      "scale=160:90,select='gte(scene,0)',signalstats,metadata=print",
                      '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
times, score, yavg = [], [], []
for line in log.splitlines():
    m = re.search(r'pts_time:([\d.]+)', line)
    if m:
        times.append(float(m.group(1)) + t0)
    m = re.search(r'scene_score=([\d.]+)', line)
    if m:
        score.append(float(m.group(1)))
    m = re.search(r'YAVG=([\d.]+)', line)
    if m:
        yavg.append(float(m.group(1)))
k = min(len(times), len(score), len(yavg))
times, score, yavg = np.array(times[:k]), np.array(score[:k]), np.array(yavg[:k])
black = yavg < 22
cuts = [0]
for i in range(1, k):
    if score[i] > 0.3 or black[i] != black[i - 1]:
        if i - cuts[-1] >= 2:
            cuts.append(i)
cuts.append(k)

# sound: short-term loudness every 0.1 s
el = subprocess.run(['ffmpeg', '-hide_banner', '-nostats'] + rng + ['-i', src, '-af', 'ebur128', '-f', 'null', '-'],
                    capture_output=True, text=True).stderr
lt, lm = [], []
for line in el.splitlines():
    m = re.search(r't:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+)', line)
    if m:
        lt.append(float(m.group(1)) + t0); lm.append(float(m.group(2)))
lt, lm = np.array(lt), np.array(lm)
loud_at = lambda t: float(lm[np.argmin(np.abs(lt - t))]) if len(lt) else float('nan')

with open(os.path.join(out, 'shots.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['shot', 'start', 'end', 'seconds', 'frames', 'brightness', 'black_or_card', 'loudness_LUFS_M'])
    for n, (a, b) in enumerate(zip(cuts[:-1], cuts[1:]), 1):
        s, e = times[a], (times[b] if b < k else times[-1] + 1 / fps)
        w.writerow([n, tc(s), tc(e), round(e - s, 3), b - a, round(float(yavg[a:b].mean()), 1),
                    'yes' if black[a:b].mean() > 0.6 else '', round(loud_at(s), 1)])

events = []
i = 0
while i < k:                                                   # black stretches
    if black[i]:
        j = i
        while j < k and black[j]:
            j += 1
        events.append((times[i], 'black', round(times[j - 1] - times[i] + 1 / fps, 2)))
        i = j
    else:
        i += 1
sil = subprocess.run(['ffmpeg', '-hide_banner'] + rng + ['-i', src, '-af', 'silencedetect=n=-50dB:d=0.25', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
for m in re.finditer(r'silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)', sil):
    events.append((float(m.group(1)) + t0, 'silence', round(float(m.group(2)) - float(m.group(1)), 2)))
for i in range(3, len(lm)):                                    # hits: momentary loudness jumps by 9 LU
    if lm[i] - lm[i - 3:i].min() > 9 and lm[i] > -30 and (not events or events[-1][1] != 'hit' or lt[i] - events[-1][0] > 0.4):
        events.append((lt[i], 'hit', round(lm[i], 1)))
events.sort()
with open(os.path.join(out, 'events.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['time', 'event', 'value (s or LUFS)'])
    for t, kind, v in events:
        w.writerow([tc(t), kind, v])

# contact sheet: one frame from the middle of each shot
tw, th, cols = 240, 135, 8
ns = len(cuts) - 1
sheet = Image.new('RGB', (tw * cols, (th + 16) * ((ns + cols - 1) // cols)), (0, 0, 0))
d = ImageDraw.Draw(sheet)
for n, (a, b) in enumerate(zip(cuts[:-1], cuts[1:])):
    t = times[(a + b - 1) // 2]
    p = os.path.join(out, '_f.jpg')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-vf', f'scale={tw}:{th}', p])
    x, y = (n % cols) * tw, (n // cols) * (th + 16)
    if os.path.exists(p):
        sheet.paste(Image.open(p), (x, y + 16))
    d.text((x + 3, y + 2), f'{n + 1}  {tc(times[a])}', fill=(255, 255, 0))
sheet.save(os.path.join(out, 'sheet.jpg'), quality=85)
if os.path.exists(os.path.join(out, '_f.jpg')):
    os.remove(os.path.join(out, '_f.jpg'))
print(ns, 'shots,', sum(1 for e in events if e[1] == 'hit'), 'hits,', sum(1 for e in events if e[1] == 'silence'), 'silences ->', out)
