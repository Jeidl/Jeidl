"""Track a flat object (the evidence tag) through a clip and save one homography per frame.

    python3 track_plane.py CLIP.mp4 OUT.json REF_T x1,y1,x2,y2,x3,y3,x4,y4 [W H]

The clip is read with the same scale-and-crop as roughcut.py (default 1280x720), so the
coordinates are in rough-cut frame space. The four points outline the object in the
reference frame (time REF_T); features inside that outline are matched in every frame
(optical flow chained frame to frame from the reference, refit with RANSAC each frame),
and the result is smoothed over 5 frames. OUT.json holds, per frame,
the 3x3 matrix that maps reference-frame coordinates to that frame.
Needs opencv-python-headless and numpy (only this tool; roughcut.py reads the JSON)."""
import json, subprocess, sys
import cv2
import numpy as np

clip, out, ref_t = sys.argv[1], sys.argv[2], float(sys.argv[3])
quad = np.array([float(v) for v in sys.argv[4].split(',')], np.float32).reshape(4, 2)
W, H = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (1280, 720)
FPS = 24
vf = f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=gray'
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', clip, '-vf', vf, '-f', 'rawvideo', '-'], capture_output=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
ref_i = int(round(ref_t * FPS))
mask = np.zeros((H, W), np.uint8)
cv2.fillConvexPoly(mask, quad.astype(np.int32), 255)
LK = dict(winSize=(31, 31), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))


def seed(img, Hm):
    """Fresh corners inside the tracked outline, with their reference-frame positions."""
    q = cv2.perspectiveTransform(quad[None], Hm)[0]
    m = np.zeros((H, W), np.uint8)
    cv2.fillConvexPoly(m, q.astype(np.int32), 255)
    m = cv2.erode(m, np.ones((9, 9), np.uint8))
    pts = cv2.goodFeaturesToTrack(img, 400, 0.01, 6, mask=m)
    if pts is None:
        return None, None
    ref = cv2.perspectiveTransform(pts.reshape(1, -1, 2), np.linalg.inv(Hm))[0]
    return pts.reshape(-1, 2), ref


def run(order):
    """Optical flow frame to frame from the reference, refitting reference->frame each step."""
    out = {ref_i: (np.eye(3), 999)}
    Hm = np.eye(3)
    cur, ref = seed(frames[ref_i], Hm)
    prev_img = frames[ref_i]
    for i in order:
        img = frames[i]
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev_img, img, cur.astype(np.float32), None, **LK)
        back, st2, _ = cv2.calcOpticalFlowPyrLK(img, prev_img, nxt, None, **LK)
        ok = (st.ravel() == 1) & (st2.ravel() == 1) & (np.linalg.norm(back - cur, axis=1) < 1.0)
        n = int(ok.sum())
        if n >= 10:
            Hn, inl = cv2.findHomography(ref[ok], nxt[ok], cv2.RANSAC, 2.5)
            if Hn is not None:
                Hm, keep = Hn, ok.copy()
                keep[ok] = inl.ravel() == 1
                cur, ref, n = nxt[keep], ref[keep], int(keep.sum())
        if n < 60:                      # top up the point set
            c2, r2 = seed(img, Hm)
            if c2 is not None:
                cur, ref = np.vstack([cur, c2]), np.vstack([ref, r2])
        out[i] = (Hm, n)
        prev_img = img
    return out


res = run(range(ref_i + 1, len(frames)))
res.update(run(range(ref_i - 1, -1, -1)))
Hs = [res[i][0] for i in range(len(frames))]
inl = [res[i][1] for i in range(len(frames))]
# smooth the projected corners (5-frame window), then refit each frame from the smoothed corners
corners = np.array([cv2.perspectiveTransform(quad[None], h)[0] for h in Hs])
sm = np.array([corners[max(0, i - 2):i + 3].mean(0) for i in range(len(corners))])
Hs = [cv2.getPerspectiveTransform(quad, c.astype(np.float32)) for c in sm]
json.dump({'clip': clip.split('/')[-1], 'fps': FPS, 'size': [W, H], 'ref_t': ref_t, 'quad': quad.tolist(),
           'inliers': inl, 'H': [h.flatten().round(6).tolist() for h in Hs]}, open(out, 'w'))
print(len(Hs), 'frames; tracked points min/median', min(inl), int(np.median(inl)))
