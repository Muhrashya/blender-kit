# camera_rig.py - builds cinematic camera rigs and keys from a SHOTS list. Prints JSON.
# NOT yet run inside Blender: run evals/cases.md section F first. Property names are standard bpy;
# if an error names a missing property, introspect it (ground-rules.md section 3) instead of guessing.
import bpy, math, json, random
from mathutils import Vector, Quaternion

# ---------------- pure math (testable without Blender) ----------------
def vfov_deg(sensor_h, lens):
    return math.degrees(2 * math.atan(sensor_h / (2 * lens)))

def hfov_deg(sensor_w, lens):
    return math.degrees(2 * math.atan(sensor_w / (2 * lens)))

def dolly_zoom_lens(lens0, dist0, dist):
    """Subject size on the sensor is proportional to lens / distance; keep it constant."""
    return lens0 * dist / dist0

def lerp(a, b, t):
    return a + (b - a) * t

# ---------------- scene helpers ----------------
def _link(obj):
    bpy.context.scene.collection.objects.link(obj)
    return obj

def new_camera(name, lens, loc):
    data = bpy.data.cameras.new(name)
    data.lens = lens
    obj = _link(bpy.data.objects.new(name, data))
    obj.location = Vector(loc)
    return obj

def new_empty(name, loc):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = 'PLAIN_AXES'
    e.location = Vector(loc)
    return _link(e)

def look_at(cam, target):
    c = cam.constraints.new('TRACK_TO')
    c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'
    return c

def key(obj, path, frame, index=-1):
    if index >= 0:
        obj.keyframe_insert(data_path=path, index=index, frame=frame)
    else:
        obj.keyframe_insert(data_path=path, frame=frame)

def set_interp(owner, interp, easing=None):
    """owner = object or camera data. Returns True if applied. Layered actions (newer Blender) may not expose fcurves."""
    ad = getattr(owner, "animation_data", None)
    act = ad.action if ad else None
    if act is not None and hasattr(act, "fcurves"):
        for fc in act.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = interp
                if easing:
                    kp.easing = easing
        return True
    print(f"NOTE: interpolation not applied to {getattr(owner, 'name', owner)} (no fcurves access); set it in the Graph Editor.")
    return False

def bind_marker(name, frame, cam):
    m = bpy.context.scene.timeline_markers.new(name, frame=frame)
    m.camera = cam

# ---------------- shot builders ----------------
def shot_static(s):
    cam = new_camera(s["name"], s.get("lens", 35), s["cam_loc"])
    tgt = new_empty(f"CAMRIG_{s['name']}_Target", s["target_loc"])
    look_at(cam, tgt)
    return cam, [tgt]

def shot_target_move(s):
    """pan / whip pan / tilt: camera fixed, the look-at target travels from target_loc to target_loc_end."""
    cam, objs = shot_static(s)
    tgt = objs[0]
    f0, f1 = s["frames"]
    key(tgt, "location", f0)
    tgt.location = Vector(s["target_loc_end"])
    key(tgt, "location", f1)
    set_interp(tgt, s.get("interp", "BEZIER"), s.get("easing", "EASE_IN_OUT"))
    return cam, objs

def shot_move(s):
    """push in / pull out / track / truck / boom: camera translates cam_loc -> cam_loc_end."""
    cam = new_camera(s["name"], s.get("lens", 35), s["cam_loc"])
    objs = []
    if s.get("look_at", True):
        tgt = new_empty(f"CAMRIG_{s['name']}_Target", s["target_loc"])
        look_at(cam, tgt)
        objs.append(tgt)
    else:
        cam.rotation_euler = s.get("rotation_euler", (math.radians(90), 0, 0))
    f0, f1 = s["frames"]
    key(cam, "location", f0)
    cam.location = Vector(s["cam_loc_end"])
    key(cam, "location", f1)
    set_interp(cam, s.get("interp", "BEZIER"), s.get("easing", "EASE_IN_OUT"))
    return cam, objs

def shot_zoom(s):
    cam, objs = shot_static(s)
    f0, f1 = s["frames"]
    cam.data.lens = s["lens"]
    cam.data.keyframe_insert("lens", frame=f0)
    cam.data.lens = s["lens_end"]
    cam.data.keyframe_insert("lens", frame=f1)
    set_interp(cam.data, s.get("interp", "BEZIER"), s.get("easing", "EASE_IN_OUT"))
    return cam, objs

def shot_dolly_zoom(s):
    """camera moves along the line subject -> camera by distance d0 -> d1 while the lens follows lens0 * d / d0."""
    subj = Vector(s["target_loc"])
    direction = (Vector(s["cam_loc"]) - subj).normalized()
    d0, d1 = s["dist"], s["dist_end"]
    lens0 = s["lens"]
    cam = new_camera(s["name"], lens0, subj + direction * d0)
    tgt = new_empty(f"CAMRIG_{s['name']}_Target", s["target_loc"])
    look_at(cam, tgt)
    f0, f1 = s["frames"]
    key(cam, "location", f0)
    cam.data.lens = lens0
    cam.data.keyframe_insert("lens", frame=f0)
    cam.location = subj + direction * d1
    key(cam, "location", f1)
    cam.data.lens = dolly_zoom_lens(lens0, d0, d1)
    cam.data.keyframe_insert("lens", frame=f1)
    set_interp(cam, "LINEAR")
    set_interp(cam.data, "LINEAR")
    return cam, [tgt]

def shot_arc(s):
    """camera is a child of a pivot at the subject; the pivot rotates about Z. Radius stays constant."""
    pivot = new_empty(f"CAMRIG_{s['name']}_Pivot", s["target_loc"])
    cam = new_camera(s["name"], s.get("lens", 35), (0, 0, 0))
    cam.parent = pivot
    cam.location = Vector((s["radius"], 0, s.get("height", 0.0)))
    look_at(cam, pivot)
    f0, f1 = s["frames"]
    pivot.rotation_euler = (0, 0, math.radians(s["angle0"]))
    key(pivot, "rotation_euler", f0, 2)
    pivot.rotation_euler = (0, 0, math.radians(s["angle1"]))
    key(pivot, "rotation_euler", f1, 2)
    set_interp(pivot, s.get("interp", "BEZIER"), s.get("easing", "EASE_IN_OUT"))
    return cam, [pivot]

def shot_roll(s):
    """no Track To: orientation is baked as quaternion keys every `step` frames (roll about the view axis)."""
    loc = Vector(s["cam_loc"])
    cam = new_camera(s["name"], s.get("lens", 35), loc)
    base = (Vector(s["target_loc"]) - loc).to_track_quat('-Z', 'Y')
    cam.rotation_mode = 'QUATERNION'
    f0, f1 = s["frames"]
    step = s.get("step", 4)
    f = f0
    while True:
        t = (f - f0) / max(1, (f1 - f0))
        angle = math.radians(lerp(s["roll0"], s["roll1"], t))
        cam.rotation_quaternion = base @ Quaternion((0, 0, 1), angle)
        key(cam, "rotation_quaternion", f)
        if f >= f1:
            break
        f = min(f + step, f1)
    set_interp(cam, "LINEAR")
    return cam, []

def shot_handheld(s):
    """seeded, smoothed wobble baked as keys on camera location and on the look-at target."""
    cam, objs = shot_static(s)
    tgt = objs[0]
    rng = random.Random(s.get("seed", 7))
    f0, f1 = s["frames"]
    step = s.get("step", 2)
    amp_loc = s.get("amp_loc", 0.01)        # meters [START]
    amp_aim = s.get("amp_aim", 0.01)        # meters on the target [START]
    base_c, base_t = Vector(s["cam_loc"]), Vector(s["target_loc"])
    off_c, off_t = Vector((0, 0, 0)), Vector((0, 0, 0))
    f = f0
    while f <= f1:
        off_c = off_c * 0.6 + Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))) * amp_loc * 0.4
        off_t = off_t * 0.6 + Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))) * amp_aim * 0.4
        cam.location = base_c + off_c
        tgt.location = base_t + off_t
        key(cam, "location", f)
        key(tgt, "location", f)
        f += step
    set_interp(cam, "BEZIER")
    set_interp(tgt, "BEZIER")
    return cam, objs

def shot_birdseye(s):
    """camera above the subject looking straight down (rotation 0 looks down -Z); optional slow descent."""
    c = Vector(s["target_loc"])
    cam = new_camera(s["name"], s.get("lens", 35), (c.x, c.y, c.z + s["height"]))
    cam.rotation_euler = (0, 0, math.radians(s.get("yaw", 0)))
    if "height_end" in s:
        f0, f1 = s["frames"]
        key(cam, "location", f0)
        cam.location.z = c.z + s["height_end"]
        key(cam, "location", f1)
        set_interp(cam, s.get("interp", "BEZIER"), s.get("easing", "EASE_IN_OUT"))
    return cam, []

BUILDERS = {
    "static": shot_static, "pan": shot_target_move, "whip_pan": shot_target_move, "tilt": shot_target_move,
    "push_in": shot_move, "pull_out": shot_move, "track": shot_move, "truck": shot_move, "boom": shot_move,
    "zoom": shot_zoom, "dolly_zoom": shot_dolly_zoom, "arc": shot_arc, "roll": shot_roll,
    "handheld": shot_handheld, "birdseye": shot_birdseye,
}

# ---------------- edit this list ----------------
SHOTS = [
    {"type": "static", "name": "CAM_Shot01", "cam_loc": (0, -6, 1.5), "target_loc": (0, 0, 1.0), "lens": 35, "frames": (1, 48)},
    {"type": "push_in", "name": "CAM_Shot02", "cam_loc": (0, -6, 1.5), "cam_loc_end": (0, -3, 1.5), "target_loc": (0, 0, 1.2),
     "lens": 50, "frames": (49, 144)},
]
SHOT_RANGE_OFFSET = 0   # shift all frames if needed

built = []
for s in SHOTS:
    cam, extras = BUILDERS[s["type"]](s)
    bind_marker(s["name"], s["frames"][0], cam)
    built.append({"shot": s["name"], "type": s["type"], "camera": cam.name, "rig_objects": [o.name for o in extras],
                  "frames": list(s["frames"]), "lens": cam.data.lens})
sc = bpy.context.scene
sc.frame_start = min(b["frames"][0] for b in built)
sc.frame_end = max(b["frames"][1] for b in built)
print(json.dumps({"built": built, "fps": sc.render.fps, "frame_range": [sc.frame_start, sc.frame_end]}, indent=2))
