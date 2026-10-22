# export_asset.py - exports selected objects with FBX or GLB, filtering options to what THIS Blender version supports.
# Unsupported options are dropped and REPORTED (never guessed). Verifies the file exists. Prints JSON.
import bpy, os, json

FORMAT = "GLB"                      # "FBX" or "GLB"
OBJECTS = ["SM_Crate_LP"]           # names to export
OUT_PATH = "//blender-out/Crate/export/SM_Crate.glb"
# Options come from docs/blender/engine.md "Export call". Keys that this Blender does not have are dropped.
OPTIONS = {
    # GLB examples:  "export_format": "GLB", "export_yup": True, "export_apply": True, "export_materials": "EXPORT"
    # FBX examples:  "apply_scale_options": "FBX_SCALE_ALL", "axis_forward": "-Z", "axis_up": "Y",
    #                "object_types": {"MESH"}, "add_leaf_bones": False, "mesh_smooth_type": "FACE"
    "export_format": "GLB", "export_yup": True, "export_apply": True,
}

op = bpy.ops.export_scene.gltf if FORMAT == "GLB" else bpy.ops.export_scene.fbx
props = {p.identifier for p in op.get_rna_type().properties}
opts = dict(OPTIONS)
opts["use_selection"] = True
opts["filepath"] = bpy.path.abspath(OUT_PATH)
kept = {k: v for k, v in opts.items() if k in props}
dropped = sorted(set(opts) - set(kept))

missing = [n for n in OBJECTS if n not in bpy.data.objects]
if missing:
    raise RuntimeError(f"objects not found: {missing}")
os.makedirs(os.path.dirname(kept["filepath"]), exist_ok=True)
bpy.ops.object.select_all(action="DESELECT")
for n in OBJECTS:
    bpy.data.objects[n].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[OBJECTS[0]]
result = op(**kept)
ok = os.path.exists(kept["filepath"]) and os.path.getsize(kept["filepath"]) > 0
print(json.dumps({"format": FORMAT, "operator_result": list(result), "file": kept["filepath"], "exists_nonempty": ok,
                  "bytes": os.path.getsize(kept["filepath"]) if ok else 0,
                  "options_used": {k: (list(v) if isinstance(v, set) else v) for k, v in kept.items()},
                  "options_dropped_unsupported": dropped,
                  "blender_version": bpy.app.version_string}, indent=2))
print("EXPORT_OK=" + str(ok))
