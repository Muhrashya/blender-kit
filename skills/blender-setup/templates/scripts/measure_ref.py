# measure_ref.py - MEASURES a reference image: subject bounding box, aspect ratio, coverage, top colors.
# Output is [MEASURED] evidence for ref-analysis.md. Colors are the raw sRGB values (hex).
import bpy, numpy as np, json

PATH = "//reference.png"
BG_DISTANCE = 0.08       # used only when the image has no transparency

img = bpy.data.images.load(bpy.path.abspath(PATH), check_existing=False)
try:
    img.colorspace_settings.name = "Non-Color"
    img.alpha_mode = "STRAIGHT"
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)[::-1]            # flip so row 0 = top of the image
finally:
    bpy.data.images.remove(img)

rgb, a = px[..., :3], px[..., 3]
if a.min() < 0.99:
    mask = a > 0.05
    mode = "alpha"
else:
    corners = np.concatenate([rgb[:4, :4].reshape(-1, 3), rgb[:4, -4:].reshape(-1, 3),
                              rgb[-4:, :4].reshape(-1, 3), rgb[-4:, -4:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    mask = np.linalg.norm(rgb - bg, axis=2) > BG_DISTANCE
    mode = "background-difference"
if not mask.any():
    raise RuntimeError("no subject found; image may be uniform")
ys, xs = np.where(mask)
x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
bw, bh = x1 - x0 + 1, y1 - y0 + 1

q = (np.clip(rgb[mask], 0, 1) * 15).round().astype(int)       # 4 bits per channel
keys, counts = np.unique(q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2], return_counts=True)
top = np.argsort(counts)[::-1][:6]
palette = []
for t in top:
    k = int(keys[t]); r_, g_, b_ = k // 256, (k // 16) % 16, k % 16
    palette.append({"hex": "#%02x%02x%02x" % (r_ * 17, g_ * 17, b_ * 17), "share": round(float(counts[t] / counts.sum()), 3)})

print(json.dumps({
    "file": PATH, "size_px": [w, h], "subject_mask_mode": mode,
    "subject_bbox_px": {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "w": bw, "h": bh},
    "aspect_w_over_h": round(bw / bh, 3), "coverage_of_image": round(float(mask.mean()), 3),
    "padding_ratio": {"left": round(x0 / w, 3), "right": round((w - 1 - x1) / w, 3),
                      "top": round(y0 / h, 3), "bottom": round((h - 1 - y1) / h, 3)},
    "palette_top6": palette,
    "note": "bbox and colors are MEASURED from pixels; part proportions inside the subject still need visual estimation (label [ESTIMATED])."
}, indent=2))
