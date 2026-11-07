"""Download the AKOOL clips listed in ../clips_v1.json.

    python3 fetch_clips.py OUT_DIR            # selected takes only (what roughcut.py needs)
    python3 fetch_clips.py OUT_DIR --all      # every take

Each clip is saved as OUT_DIR/<name>.mp4 (e.g. 02_D1__akp.mp4)."""
import json, os, sys, urllib.request

here = os.path.dirname(os.path.abspath(__file__))
log = json.load(open(os.path.join(here, "..", "clips_v1.json"), encoding="utf-8"))
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for c in log["clips"]:
    if not (c["selected"] or "--all" in sys.argv):
        continue
    dst = os.path.join(out, c["name"] + ".mp4")
    if os.path.exists(dst):
        continue
    urllib.request.urlretrieve(c["video_url"], dst)
    print("saved", dst)
