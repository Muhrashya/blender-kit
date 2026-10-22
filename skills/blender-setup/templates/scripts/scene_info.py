# scene_info.py - "doctor": read-only facts about the open Blender session. Run first in every session.
import bpy, json

def tri_count(obj):
    try:
        dg = bpy.context.evaluated_depsgraph_get()
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        n = len(me.loop_triangles)
        ev.to_mesh_clear()
        return n
    except Exception as e:
        return f"error: {e}"

sc = bpy.context.scene
info = {
    "blender_version": bpy.app.version_string,
    "file_path": bpy.data.filepath or "UNSAVED",
    "file_dirty": bpy.data.is_dirty,
    "scene": sc.name,
    "unit_system": sc.unit_settings.system,
    "unit_scale": sc.unit_settings.scale_length,
    "fps": sc.render.fps,
    "frame_range": [sc.frame_start, sc.frame_end],
    "render_engine": sc.render.engine,
    "render_engine_choices": [i.identifier for i in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items],
    "has_cell_fracture_op": hasattr(bpy.ops.object, "add_fracture_cell_objects"),
    "selected": [o.name for o in bpy.context.selected_objects],
    "active": bpy.context.view_layer.objects.active.name if bpy.context.view_layer.objects.active else None,
    "collections": [c.name for c in bpy.data.collections],
    "objects": [],
}
for o in bpy.data.objects:
    row = {"name": o.name, "type": o.type, "parent": o.parent.name if o.parent else None,
           "dims_m": [round(v, 4) for v in o.dimensions], "scale": [round(v, 4) for v in o.scale],
           "modifiers": [m.type for m in o.modifiers]}
    if o.type == "MESH":
        row["tris_evaluated"] = tri_count(o)
        row["materials"] = [s.material.name if s.material else None for s in o.material_slots]
        row["uv_layers"] = [u.name for u in o.data.uv_layers]
    info["objects"].append(row)
info["actions"] = [{"name": a.name, "frame_range": list(a.frame_range)} for a in bpy.data.actions]
info["images"] = [i.name for i in bpy.data.images]
print(json.dumps(info, indent=2))
