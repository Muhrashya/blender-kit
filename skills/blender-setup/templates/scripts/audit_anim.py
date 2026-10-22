# audit_anim.py - checks actions: fps, duration, loop closure, root drift. Prints JSON.
import bpy, json

LOOP_SUFFIX = "_loop"       # actions whose name ends with this must close
TOLERANCE = 1e-3
ROOT_BONE = None            # e.g. "root"; None = skip root drift check

sc = bpy.context.scene
res = {"fps": sc.render.fps, "actions": []}
for a in bpy.data.actions:
    f0, f1 = a.frame_range
    row = {
        "action": a.name, "frame_start": f0, "frame_end": f1,
        "frames": int(f1 - f0) + 1, "duration_s": round((f1 - f0) / sc.render.fps, 3),
        "fcurves": len(a.fcurves) if hasattr(a, "fcurves") else "n/a (layered actions: introspect action.layers)",
    }
    if a.name.endswith(LOOP_SUFFIX) and hasattr(a, "fcurves"):
        bad = []
        for fc in a.fcurves:
            d = abs(fc.evaluate(f0) - fc.evaluate(f1))
            if d > TOLERANCE:
                bad.append({"channel": f"{fc.data_path}[{fc.array_index}]", "diff": round(d, 4)})
        row["loop_open_channels"] = bad[:20]
        row["loop_closed"] = not bad
    if ROOT_BONE and hasattr(a, "fcurves"):
        p = f'pose.bones["{ROOT_BONE}"].location'
        drift = [round(fc.evaluate(f1) - fc.evaluate(f0), 4) for fc in a.fcurves if fc.data_path == p]
        row["root_location_drift_xyz"] = drift
    res["actions"].append(row)
res["pass"] = all(r.get("loop_closed", True) for r in res["actions"]) and len(res["actions"]) > 0
print(json.dumps(res, indent=2))
print("AUDIT_PASS=" + str(res["pass"]))
