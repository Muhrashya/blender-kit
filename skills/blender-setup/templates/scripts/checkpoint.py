# checkpoint.py - save a COPY of the current scene before a destructive step. Does not change the open file.
import bpy, os

ASSET = "asset"      # <- set
STAGE = "stage"      # <- set, e.g. "pre-retopo"

base = os.path.dirname(bpy.data.filepath) or os.path.expanduser("~")
out_dir = os.path.join(base, "blender-out", ASSET, "checkpoints")
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, f"{STAGE}.blend")
bpy.ops.wm.save_as_mainfile(filepath=path, copy=True)
print({"checkpoint": path, "exists": os.path.exists(path), "bytes": os.path.getsize(path) if os.path.exists(path) else 0})
