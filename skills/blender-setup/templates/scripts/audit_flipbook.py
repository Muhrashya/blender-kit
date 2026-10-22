# audit_flipbook.py - checks a packed sprite sheet. Prints JSON. Needs numpy (bundled with Blender).
import bpy, numpy as np, json

PATH = "//T_FX_Smoke_FB_6x6.png"   # sheet path (// = relative to the .blend)
COLS, ROWS = 6, 6
FRAMES = None                      # None = COLS*ROWS
LOOP = False                       # True: last frame must flow into the first
SEAM_MAX_RATIO = 1.5               # [START] loop seam change vs average frame-to-frame change

def audit_sheet(path, cols, rows, frames, loop):
    frames = frames or cols * rows
    img = bpy.data.images.load(bpy.path.abspath(path), check_existing=False)
    try:
        img.colorspace_settings.name = "Non-Color"     # read raw values, no transform
        img.alpha_mode = "STRAIGHT"
        w, h = img.size
        px = np.empty(w * h * 4, dtype=np.float32)
        img.pixels.foreach_get(px)
        px = px.reshape(h, w, 4)                       # row 0 = BOTTOM of the image
        fw, fh = w // cols, h // rows

        def frame(i):                                  # frame 0 = top-left, left->right, top->bottom
            c, r = i % cols, i // cols
            y0 = h - (r + 1) * fh
            return px[y0:y0 + fh, c * fw:(c + 1) * fw]

        pad = max(1, fw // 50)
        empty, clipped = [], []
        for i in range(frames):
            a = frame(i)[..., 3]
            if a.max() < 0.01:
                empty.append(i)
            edge = np.concatenate([a[:pad].ravel(), a[-pad:].ravel(), a[:, :pad].ravel(), a[:, -pad:].ravel()])
            if edge.max() > 0.05:
                clipped.append(i)
        diffs = [float(np.abs(frame(i + 1) - frame(i)).mean()) for i in range(frames - 1)]
        avg = max(float(np.mean(diffs)), 1e-6) if diffs else 1e-6
        seam = float(np.abs(frame(frames - 1) - frame(0)).mean()) / avg
        r = {
            "file": path, "size": [w, h], "grid": [cols, rows], "frames": frames, "frame_px": [fw, fh],
            "pow2": all(v > 0 and (v & (v - 1)) == 0 for v in (w, h)),
            "grid_divides": w % cols == 0 and h % rows == 0,
            "square_frames": fw == fh,
            "has_alpha": bool(px[..., 3].min() < 0.01 and px[..., 3].max() > 0.9),
            "empty_frames": empty, "clipped_frames": clipped,
            "loop_seam_ratio": round(seam, 2),
        }
    finally:
        bpy.data.images.remove(img)
    checks = {
        "pow2": r["pow2"], "grid_divides": r["grid_divides"], "square_frames": r["square_frames"],
        "has_alpha": r["has_alpha"], "no_empty_frames": not empty, "no_clipped_frames": not clipped,
        "loop_ok": (not loop) or seam <= SEAM_MAX_RATIO,
    }
    r["checks"] = checks
    r["failed"] = [k for k, v in checks.items() if not v]
    r["pass"] = not r["failed"]
    return r

res = audit_sheet(PATH, COLS, ROWS, FRAMES, LOOP)
print(json.dumps(res, indent=2))
print("AUDIT_PASS=" + str(res["pass"]))
