"""Download the AKOOL clips listed in ../clips_v2.json.

    python3 fetch_clips.py OUT_DIR            # takes used in rough cut v3 (what roughcut.py needs)
    python3 fetch_clips.py OUT_DIR --v2       # takes used in rough cut v2
    python3 fetch_clips.py OUT_DIR --v1       # takes used in rough cut v1
    python3 fetch_clips.py OUT_DIR --all      # every take

Each clip is saved as OUT_DIR/<name>.mp4 (e.g. 02_D1__akp.mp4)."""
import json, os, sys, urllib.request

here = os.path.dirname(os.path.abspath(__file__))
log = json.load(open(os.path.join(here, "..", "clips_v2.json"), encoding="utf-8"))
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for c in log["clips"]:
    cut = "v1" if "--v1" in sys.argv else "v2" if "--v2" in sys.argv else "v3"
    used = c["used_in_cut_" + cut]
    if not (used or "--all" in sys.argv):
        continue
    dst = os.path.join(out, c["name"] + ".mp4")
    if os.path.exists(dst):
        continue
    urllib.request.urlretrieve(c["video_url"], dst)
    print("saved", dst)
