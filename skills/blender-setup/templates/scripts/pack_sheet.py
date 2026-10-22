# pack_sheet.py - packs a rendered PNG sequence into one sprite sheet. Prints JSON.
# Frame 0 = top-left, left->right, top->bottom. Straight alpha, raw values (Non-Color).
import bpy, numpy as np, os, json

FRAMES_DIR = "//flipbook_frames"       # folder with the PNG sequence
COLS, ROWS = 6, 6
FRAME_PX = 128                         # output frame size (square)
OUT_PATH = "//T_FX_Smoke_FB_6x6.png"

d = bpy.path.abspath(FRAMES_DIR)
files = sorted(f for f in os.listdir(d) if f.lower().endswith(".png"))
need = COLS * ROWS
if len(files) < need:
    raise RuntimeError(f"need {need} frames, found {len(files)} in {d}")
files = files[:need]
W, H = COLS * FRAME_PX, ROWS * FRAME_PX
sheet = np.zeros((H, W, 4), dtype=np.float32)     # row 0 = bottom
for i, fn in enumerate(files):
    img = bpy.data.images.load(os.path.join(d, fn), check_existing=False)
    try:
        img.colorspace_settings.name = "Non-Color"
        img.alpha_mode = "STRAIGHT"
        if tuple(img.size) != (FRAME_PX, FRAME_PX):
            img.scale(FRAME_PX, FRAME_PX)
        px = np.empty(FRAME_PX * FRAME_PX * 4, dtype=np.float32)
        img.pixels.foreach_get(px)
        px = px.reshape(FRAME_PX, FRAME_PX, 4)
    finally:
        bpy.data.images.remove(img)
    c, r = i % COLS, i // COLS
    y0 = H - (r + 1) * FRAME_PX
    sheet[y0:y0 + FRAME_PX, c * FRAME_PX:(c + 1) * FRAME_PX] = px

out_abs = bpy.path.abspath(OUT_PATH)
out = bpy.data.images.new(os.path.basename(out_abs), W, H, alpha=True, float_buffer=False)
out.colorspace_settings.name = "Non-Color"
out.alpha_mode = "STRAIGHT"
out.pixels.foreach_set(sheet.ravel())
out.filepath_raw = out_abs
out.file_format = "PNG"
out.save()
bpy.data.images.remove(out)
print(json.dumps({"sheet": out_abs, "size": [W, H], "grid": [COLS, ROWS], "frames": need,
                  "exists": os.path.exists(out_abs), "bytes": os.path.getsize(out_abs) if os.path.exists(out_abs) else 0}, indent=2))
