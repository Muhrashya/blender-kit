# audit_camera.py - measures shots: framing, horizon, clip planes, duration, speed. Prints JSON.
# NOT yet run inside Blender: run evals/cases.md section F first.
import bpy, math, json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

# edit: one dict per shot
SHOTS = [
    {"camera": "CAM_Shot01", "subject": "SM_Name_LP", "frames": (1, 48), "movement": "static",
     "allow_roll": False, "subject_inside": True},
]
SAMPLES = 5                  # frames sampled per shot (start, middle, end, ...)
LEVEL_TOL_DEG = 1.0          # [START]

def roll_deg_of(cam_obj):
    right = cam_obj.matrix_world.to_quaternion() @ Vector((1, 0, 0))
    return math.degrees(math.asin(max(-1.0, min(1.0, right.z))))

def frame_metrics(sc, cam_obj, subj):
    corners = [subj.matrix_world @ Vector(c) for c in subj.bound_box]
    pts = [world_to_camera_view(sc, cam_obj, p) for p in corners]
    xs, ys, zs = [p.x for p in pts], [p.y for p in pts], [p.z for p in pts]
    cam_pos = cam_obj.matrix_world.translation
    dists = [(p - cam_pos).length for p in corners]
    return {
        "inside": min(zs) > 0 and min(xs) >= 0 and max(xs) <= 1 and min(ys) >= 0 and max(ys) <= 1,
        "frame_height_fraction": round(max(0.0, min(1.0, max(ys)) - max(0.0, min(ys))), 3),
        "min_dist": round(min(dists), 3), "max_dist": round(max(dists), 3),
        "roll_deg": round(roll_deg_of(cam_obj), 3), "lens": round(cam_obj.data.lens, 3),
        "cam_pos": [round(v, 4) for v in cam_pos],
    }

sc = bpy.context.scene
orig_frame = sc.frame_current
fps = sc.render.fps
out = []
for s in SHOTS:
    cam, subj = bpy.data.objects[s["camera"]], bpy.data.objects[s["subject"]]
    f0, f1 = s["frames"]
    frames = sorted({int(round(f0 + (f1 - f0) * i / max(1, SAMPLES - 1))) for i in range(SAMPLES)})
    ms = []
    for f in frames:
        sc.frame_set(f)
        m = frame_metrics(sc, cam, subj)
        m["frame"] = f
        ms.append(m)
    path = 0.0
    for a, b in zip(ms, ms[1:]):
        path += (Vector(b["cam_pos"]) - Vector(a["cam_pos"])).length
    dur = (f1 - f0) / fps
    clip_ok = cam.data.clip_start < min(m["min_dist"] for m in ms) and cam.data.clip_end > max(m["max_dist"] for m in ms)
    checks = {
        "frame_range_valid": f1 > f0,
        "subject_framed": (not s.get("subject_inside", True)) or all(m["inside"] for m in ms),
        "horizon_level": s.get("allow_roll", False) or all(abs(m["roll_deg"]) <= LEVEL_TOL_DEG for m in ms),
        "clip_planes_ok": clip_ok,
        "static_has_no_motion": s.get("movement") != "static" or path < 1e-4,
    }
    out.append({
        "shot": s["camera"], "movement": s.get("movement"), "duration_s": round(dur, 3),
        "camera_path_length_m_sampled": round(path, 3),
        "avg_speed_mps_sampled": round(path / dur, 3) if dur > 0 else None,
        "samples": ms, "clip_start": cam.data.clip_start, "clip_end": cam.data.clip_end,
        "checks": checks, "failed": [k for k, v in checks.items() if not v], "pass": all(checks.values()),
    })
sc.frame_set(orig_frame)
print(json.dumps(out, indent=2))
print("AUDIT_PASS=" + str(bool(out) and all(o["pass"] for o in out)))
