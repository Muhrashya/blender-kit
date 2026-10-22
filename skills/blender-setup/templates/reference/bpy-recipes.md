# bpy recipes (verified patterns; adapt names, never invent parameters)

Contents: R1 apply transforms | R2 normals | R3 merge doubles | R4 triangulate | R5 tris to quads | R6 dissolve flat | R7 interior faces | R8 apply modifier | R9 shading | R10 origin | R11 mirror fix

Always: checkpoint first (`scripts/checkpoint.py`). If a call raises TypeError or RuntimeError, print the error and introspect; do not guess a different signature.

```python
import bpy, bmesh, math
def ctx(obj):   # context override for operators that need an active/selected object (Blender 3.2+)
    return bpy.context.temp_override(object=obj, active_object=obj, selected_objects=[obj], selected_editable_objects=[obj])
def with_bm(obj, fn):                      # edit base mesh data in object mode
    bm = bmesh.new(); bm.from_mesh(obj.data)
    try:
        fn(bm)
        bm.to_mesh(obj.data); obj.data.update()
    finally:
        bm.free()
```
| Id | Goal | Snippet |
|---|---|---|
| R1 | apply scale and rotation | `with ctx(obj): bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)` |
| R2 | recalc normals outward | `with_bm(obj, lambda bm: bmesh.ops.recalc_face_normals(bm, faces=bm.faces))` |
| R3 | merge doubles | `with_bm(obj, lambda bm: bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5))` |
| R4 | triangulate (export copy only) | `with_bm(obj, lambda bm: bmesh.ops.triangulate(bm, faces=bm.faces))` |
| R5 | join triangles into quads | `with_bm(obj, lambda bm: bmesh.ops.join_triangles(bm, faces=bm.faces, angle_face_threshold=math.radians(40), angle_shape_threshold=math.radians(40)))` |
| R6 | dissolve flat edges (static props) | `with_bm(obj, lambda bm: bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(5), verts=bm.verts, edges=bm.edges))` |
| R7 | find interior faces | needs edit mode: `bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.mesh.select_interior_faces()` then inspect the selection count before deleting |
| R8 | apply a modifier | `with ctx(obj): bpy.ops.object.modifier_apply(modifier="ModName")` |
| R9 | smooth shading | `with ctx(obj): bpy.ops.object.shade_smooth()`; auto-smooth handling differs between Blender versions: introspect (`hasattr(bpy.ops.object, 'shade_auto_smooth')`) |
| R10 | origin to bounds center | `with ctx(obj): bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')` |
| R11 | make a symmetric mesh from the +X half | delete verts with x < -1e-4 (bmesh), add Mirror modifier (use_axis[0]=True, use_clip=True, use_mirror_merge=True), apply (R8), re-run audit_topology SYMMETRIC=True |

Mirror modifier properties used in R11 must be confirmed with `[p.identifier for p in bpy.types.MirrorModifier.bl_rna.properties]` before setting.
