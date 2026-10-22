# audit_uv.py - UV coverage and texel density per selected mesh. Prints JSON.
import bpy, bmesh, json, math

TEXTURE_PX = 512          # texture size this object will use
TARGET_DENSITY = 256      # px per meter from config.md
TOLERANCE = 0.20          # +-20 percent

out = []
for obj in bpy.context.selected_objects:
    if obj.type != "MESH":
        continue
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    uv = bm.loops.layers.uv.active
    if uv is None:
        out.append({"object": obj.name, "has_uv": False, "pass": False, "failed": ["no_uv"]})
        bm.free()
        continue
    s = obj.matrix_world.to_scale()
    world_area = 0.0
    uv_area = 0.0
    for f in bm.faces:
        world_area += f.calc_area() * abs(s.x * s.y * s.z) ** (2.0 / 3.0)
        pts = [l[uv].uv.copy() for l in f.loops]
        a = 0.0
        for i in range(len(pts)):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % len(pts)]
            a += x1 * y2 - x2 * y1
        uv_area += abs(a) * 0.5
    bm.free()
    density = TEXTURE_PX * math.sqrt(uv_area / world_area) if world_area > 0 and uv_area > 0 else 0
    ok = TARGET_DENSITY * (1 - TOLERANCE) <= density <= TARGET_DENSITY * (1 + TOLERANCE)
    out.append({
        "object": obj.name, "has_uv": True, "uv_area_sum": round(uv_area, 4),
        "world_area_m2": round(world_area, 4), "texel_density_px_per_m": round(density, 1),
        "target": TARGET_DENSITY, "pass": ok, "failed": [] if ok else ["texel_density_out_of_tolerance"],
    })
print(json.dumps(out, indent=2))
print("AUDIT_PASS=" + str(bool(out) and all(x["pass"] for x in out)))
