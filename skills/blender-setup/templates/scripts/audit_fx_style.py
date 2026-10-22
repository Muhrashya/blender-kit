# audit_fx_style.py - measures a packed flipbook against its FX style and life curve. Prints JSON. Needs numpy.
import bpy, numpy as np, json

PATH = "//T_FX_Smoke_FB_4x4.png"
COLS, ROWS = 4, 4
FRAMES = None            # None = COLS*ROWS
STYLE = "stylized"       # realistic | stylized | lowpoly | voxel
LOOP = False             # one-shot effects must end clear; loops skip that check
PEAK_RANGE = (0.15, 0.45)   # [START] peak intensity position as a fraction of life (one-shot)
END_ENERGY_MAX = 0.10       # [START] last frame energy / peak energy (one-shot)
# [START] style presets: (max soft-alpha ratio, max quantized colors, frame count range)
PRESETS = {
    "realistic": (None, None, (16, 64)),
    "stylized": (0.50, 24, (8, 24)),
    "lowpoly": (0.15, 8, (4, 12)),
    "voxel": (0.05, 6, (4, 8)),
}

def analyse():
    img = bpy.data.images.load(bpy.path.abspath(PATH), check_existing=False)
    try:
        img.colorspace_settings.name = "Non-Color"
        img.alpha_mode = "STRAIGHT"
        w, h = img.size
        px = np.empty(w * h * 4, dtype=np.float32)
        img.pixels.foreach_get(px)
        px = px.reshape(h, w, 4)                     # row 0 = bottom
    finally:
        bpy.data.images.remove(img)
    fw, fh = w // COLS, h // ROWS
    n = FRAMES or COLS * ROWS

    def frame(i):
        c, r = i % COLS, i // COLS
        y0 = h - (r + 1) * fh
        return px[y0:y0 + fh, c * fw:(c + 1) * fw]

    energy, coverage, soft, colors = [], [], [], set()
    for i in range(n):
        f = frame(i)
        a = f[..., 3]
        lum = 0.2126 * f[..., 0] + 0.7152 * f[..., 1] + 0.0722 * f[..., 2]
        energy.append(float((a * lum).mean()))
        vis = a > 0.05
        coverage.append(float(vis.mean()))
        soft.append(float(((a > 0.05) & (a < 0.95)).sum()) / max(1, int(vis.sum())))
        q = (np.clip(f[vis][:, :3], 0, 1) * 7).round().astype(int)     # 3 bits per channel
        colors.update(map(tuple, np.unique(q, axis=0))) if len(q) else None
    return n, energy, coverage, soft, len(colors)

n, energy, coverage, soft, ncolors = analyse()
peak = int(np.argmax(energy))
peak_ratio = peak / max(1, n - 1)
end_ratio = energy[-1] / max(max(energy), 1e-9)
max_soft, max_colors, frange = PRESETS[STYLE]
soft_ratio = float(np.mean(soft))
checks = {
    "frame_count_in_style_range": frange[0] <= n <= frange[1],
    "soft_alpha_ok": max_soft is None or soft_ratio <= max_soft,
    "color_count_ok": max_colors is None or ncolors <= max_colors,
    "peak_position_ok": LOOP or (PEAK_RANGE[0] <= peak_ratio <= PEAK_RANGE[1]),
    "ends_clear": LOOP or end_ratio <= END_ENERGY_MAX,
}
res = {
    "file": PATH, "style": STYLE, "frames": n, "peak_frame": peak, "peak_ratio": round(peak_ratio, 3),
    "end_energy_ratio": round(end_ratio, 3), "max_coverage": round(max(coverage), 3),
    "overdraw_proxy_note": "max_coverage is the largest fraction of the frame covered by visible pixels; stacked layers multiply it",
    "soft_alpha_ratio_mean": round(soft_ratio, 3), "quantized_colors_3bit": ncolors,
    "energy_per_frame": [round(e, 4) for e in energy],
    "checks": checks, "failed": [k for k, v in checks.items() if not v], "pass": all(checks.values()),
}
print(json.dumps(res, indent=2))
print("AUDIT_PASS=" + str(res["pass"]))
