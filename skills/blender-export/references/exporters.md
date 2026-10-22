# Exporters

Contents: 1 selection | 2 introspection | 3 verification | 4 common option families

## 1. Clean selection
```python
import bpy
bpy.ops.object.select_all(action='DESELECT')
for n in ['SK_Name_LP']:                       # deliverables only
    bpy.data.objects[n].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects['SK_Name_LP']
```
Hidden objects are skipped by selection-based export; unhide deliverables first. Armature included with skinned meshes. Remove helper/control bones from the export armature or keep them in a non-deform collection (check the exporter's deform-only option via introspection).

## 2. Introspection (do this every time; options change between Blender versions)
```python
import bpy
print(bpy.app.version_string)
print([p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties])
print([p.identifier for p in bpy.ops.export_scene.fbx.get_rna_type().properties])
```
`export_asset.py` does this filtering for you and prints `options_dropped_unsupported`.

## 3. Verification
| Check | How |
|---|---|
| File exists, size | `os.path.getsize` (export_asset.py prints it) |
| Re-import | import into a new scene: object count, dimensions in meters, material count, animation clips |
| Names | `audit_naming.py` before export |

## 4. Option families (names are examples; confirm by introspection)
| Family | glTF examples | FBX examples |
|---|---|---|
| Format | export_format (GLB / GLTF_SEPARATE / GLTF_EMBEDDED) | n/a |
| Selection | use_selection | use_selection |
| Modifiers | export_apply | use_mesh_modifiers |
| Axis | export_yup | axis_forward, axis_up |
| Scale | n/a (meters) | apply_scale_options |
| Rig | export_skins | object_types, add_leaf_bones, use_armature_deform_only |
| Animation | export_animations plus a mode option (name differs by version) | bake_anim and its sub-options |
| Materials | export_materials, image format options | path_mode, embed_textures |
| Shading | export_normals | mesh_smooth_type |
