# audit_mesh.py - measures the FINAL (modifier-evaluated) mesh and prints JSON.
# Configure the 4 variables, run through execute_blender_code. Quote the numbers; never estimate.
import bpy, bmesh, json, math

BUDGET = 2000            # triangle budget from docs/blender/config.md (or user)
ALLOW_OPEN = False       # True for single-sided cards, FX strips, planes
CHECK_UV_RANGE = False   # True for FX meshes: UVs must stay inside 0-1
TARGETS = "SELECTED"     # "SELECTED" or a list of object names

def audit(obj, budget, allow_open, check_uv_range):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    bm = bmesh.new()
    try:
        bm.from_mesh(me)
        tris = sum(len(f.verts) - 2 for f in bm.faces)
        uv_lay = bm.loops.layers.uv.active
        uv_out = 0
        if uv_lay is not None:
            for f in bm.faces:
                for l in f.loops:
                    u, v = l[uv_lay].uv
                    if u < -1e-4 or u > 1 + 1e-4 or v < -1e-4 or v > 1 + 1e-4:
                        uv_out += 1
        r = {
            "object": obj.name,
            "verts": len(bm.verts), "faces": len(bm.faces),
            "tris": tris, "tri_budget": budget,
            "quads": sum(1 for f in bm.faces if len(f.verts) == 4),
            "tri_faces": sum(1 for f in bm.faces if len(f.verts) == 3),
            "ngons": sum(1 for f in bm.faces if len(f.verts) > 4),
            "non_manifold_edges": sum(1 for e in bm.edges if not e.is_manifold),
            "loose_verts": sum(1 for v in bm.verts if not v.link_edges),
            "loose_edges": sum(1 for e in bm.edges if not e.link_faces),
            "zero_area_faces": sum(1 for f in bm.faces if f.calc_area() < 1e-8),
            "doubles": len(bmesh.ops.find_doubles(bm, verts=bm.verts, dist=1e-5)["targetmap"]),
            "poles_3_interior": sum(1 for v in bm.verts if len(v.link_edges) == 3 and not v.is_boundary),
            "poles_5plus_interior": sum(1 for v in bm.verts if len(v.link_edges) >= 5 and not v.is_boundary),
            "scale_applied": all(abs(s - 1.0) < 1e-4 for s in obj.scale),
            "rotation_applied": all(abs(a) < 1e-4 for a in obj.rotation_euler),
            "negative_scale": any(s < 0 for s in obj.scale),
            "has_uv": uv_lay is not None,
            "uv_loops_outside_0_1": uv_out,
            "dimensions_m": [round(d, 4) for d in ev.dimensions],
        }
    finally:
        bm.free()
        ev.to_mesh_clear()
    checks = {
        "within_budget": r["tris"] <= budget,
        "no_ngons": r["ngons"] == 0,
        "no_doubles": r["doubles"] == 0,
        "no_zero_area": r["zero_area_faces"] == 0,
        "no_loose": r["loose_verts"] == 0 and r["loose_edges"] == 0,
        "transforms_ok": r["scale_applied"] and not r["negative_scale"],
        "closed_or_allowed_open": allow_open or r["non_manifold_edges"] == 0,
        "uv_in_range": (not check_uv_range) or (r["has_uv"] and r["uv_loops_outside_0_1"] == 0),
    }
    r["checks"] = checks
    r["pass"] = all(checks.values())
    r["failed"] = [k for k, v in checks.items() if not v]
    return r

objs = bpy.context.selected_objects if TARGETS == "SELECTED" else [bpy.data.objects[n] for n in TARGETS]
out = [audit(o, BUDGET, ALLOW_OPEN, CHECK_UV_RANGE) for o in objs if o.type == "MESH"]
print(json.dumps(out, indent=2))
print("AUDIT_PASS=" + str(bool(out) and all(x["pass"] for x in out)))
