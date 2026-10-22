# audit_naming.py - checks names against the convention in docs/blender/config.md. Prints JSON.
import bpy, json

PREFIX = {"MESH": ("SM_", "SK_"), "ARMATURE": ("ARM_",)}
MATERIAL_PREFIX = "MAT_"
IMAGE_PREFIX = ("T_",)
ACTION_PREFIX = "AN_"
COLLECTION_PREFIX = "COL_"
IGNORE_OBJECT_PREFIXES = ("CAM_", "LGT_", "Empty", "REF_")   # edit if your project differs

bad = []
for o in bpy.data.objects:
    if o.name.startswith(IGNORE_OBJECT_PREFIXES):
        continue
    want = PREFIX.get(o.type)
    if want and not o.name.startswith(want):
        bad.append({"kind": "object", "name": o.name, "expected_prefix": list(want)})
for m in bpy.data.materials:
    if m.users and not m.name.startswith(MATERIAL_PREFIX):
        bad.append({"kind": "material", "name": m.name, "expected_prefix": [MATERIAL_PREFIX]})
for i in bpy.data.images:
    if i.users and i.name not in ("Render Result", "Viewer Node") and not i.name.startswith(IMAGE_PREFIX):
        bad.append({"kind": "image", "name": i.name, "expected_prefix": list(IMAGE_PREFIX)})
for a in bpy.data.actions:
    if not a.name.startswith(ACTION_PREFIX):
        bad.append({"kind": "action", "name": a.name, "expected_prefix": [ACTION_PREFIX]})
for c in bpy.data.collections:
    if not c.name.startswith(COLLECTION_PREFIX):
        bad.append({"kind": "collection", "name": c.name, "expected_prefix": [COLLECTION_PREFIX]})
print(json.dumps({"violations": bad, "pass": not bad}, indent=2))
print("AUDIT_PASS=" + str(not bad))
