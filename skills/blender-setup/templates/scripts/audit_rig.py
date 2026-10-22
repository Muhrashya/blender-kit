# audit_rig.py - skin and skeleton checks. Select the armature AND its meshes, then run. Prints JSON.
import bpy, json

MAX_INFLUENCES = 4      # from engine.md; if engine.md says UNVERIFIED keep 4 as [START]
MAX_BONES = None        # from engine.md or None (then report only)
WEIGHT_MIN = 0.001

arm = next((o for o in bpy.context.selected_objects if o.type == "ARMATURE"), None)
meshes = [o for o in bpy.context.selected_objects if o.type == "MESH"]
res = {"armature": arm.name if arm else None}
if not arm:
    res["pass"] = False
    res["failed"] = ["no_armature_selected"]
else:
    bones = list(arm.data.bones)
    deform = [b for b in bones if b.use_deform]
    roots = [b for b in bones if b.parent is None]
    names = {b.name for b in bones}
    lr_missing = [n for n in names if n.endswith(".L") and n[:-2] + ".R" not in names] + \
                 [n for n in names if n.endswith(".R") and n[:-2] + ".L" not in names]
    res.update({
        "bone_count": len(bones), "deform_bone_count": len(deform), "root_bones": [b.name for b in roots],
        "mirror_name_missing": lr_missing,
        "scale_applied": all(abs(s - 1.0) < 1e-4 for s in arm.scale),
        "meshes": [],
    })
    deform_names = {b.name for b in deform}
    for m in meshes:
        group_names = {g.index: g.name for g in m.vertex_groups}
        max_inf, unweighted, unnormalized = 0, 0, 0
        used_groups = set()
        for v in m.data.vertices:
            w = [(group_names[g.group], g.weight) for g in v.groups if g.weight > WEIGHT_MIN and g.group in group_names]
            for n, _ in w:
                used_groups.add(n)
            max_inf = max(max_inf, len(w))
            if not w:
                unweighted += 1
            elif abs(sum(x for _, x in w) - 1.0) > 0.01:
                unnormalized += 1
        res["meshes"].append({
            "mesh": m.name, "max_influences": max_inf, "unweighted_verts": unweighted,
            "unnormalized_verts": unnormalized,
            "deform_bones_without_weights": sorted(deform_names - used_groups),
            "has_armature_modifier": any(md.type == "ARMATURE" for md in m.modifiers),
        })
    checks = {
        "single_root": len(roots) == 1,
        "bones_within_limit": MAX_BONES is None or len(bones) <= MAX_BONES,
        "influences_ok": all(x["max_influences"] <= MAX_INFLUENCES for x in res["meshes"]),
        "no_unweighted": all(x["unweighted_verts"] == 0 for x in res["meshes"]),
        "normalized": all(x["unnormalized_verts"] == 0 for x in res["meshes"]),
        "armature_modifier_present": all(x["has_armature_modifier"] for x in res["meshes"]),
        "armature_scale_applied": res["scale_applied"],
    }
    res["checks"] = checks
    res["failed"] = [k for k, v in checks.items() if not v]
    res["pass"] = not res["failed"]
print(json.dumps(res, indent=2))
print("AUDIT_PASS=" + str(res["pass"]))
