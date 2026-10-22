# Bake (normal, AO) - Cycles

Contents: 1 introspection | 2 setup | 3 run | 4 verify | 5 common artifacts

## 1. Introspection (do this first; names differ by Blender version)
```python
import bpy
print(bpy.app.version_string)
print([i.identifier for i in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items])   # confirm CYCLES exists
print([p.identifier for p in bpy.types.BakeSettings.bl_rna.properties])                          # confirm the settings below
```

## 2. Setup
```python
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
b = sc.render.bake
b.use_selected_to_active = True      # HP selected, LP active
b.cage_extrusion = 0.02              # meters [START]; raise if rays miss the HP
b.max_ray_distance = 0.0             # 0 = unlimited [START]
b.margin = 8                         # pixels [START]; match uv-rules.md
b.normal_space = 'TANGENT'
```
Target image: create `T_<Asset>_Normal` (Non-Color, no alpha), add an Image Texture node to the LP material, select that node (active), do NOT connect it.
Convention: if engine.md says DirectX (-Y), flip the green channel after the bake.

## 3. Run
```python
hp, lp = bpy.data.objects['SM_Name_HP'], bpy.data.objects['SM_Name_LP']
bpy.ops.object.select_all(action='DESELECT')
hp.select_set(True); lp.select_set(True)
bpy.context.view_layer.objects.active = lp
bpy.ops.object.bake(type='NORMAL')
img.filepath_raw = '//blender-out/Name/textures/T_Name_Normal.png'; img.file_format = 'PNG'; img.save()
```
AO: `type='AO'` into its own image (Non-Color). Report the file path and bytes.

## 4. Verify
Screenshot LP lit with the map vs HP under the same light. Look for skewed lines, floating shapes, hard seams.

## 5. Common artifacts
| Artifact | Cause | Fix |
|---|---|---|
| Skewed detail | cage too small or LP/HP misaligned | raise cage_extrusion; align origins and scale |
| Floating dots | rays hit other parts | separate HP parts or use a custom cage |
| Seam lines | low margin; seam across smooth shading | raise margin; move seam to a hard edge |
| Wavy lines on flat LP faces | LP shading split without UV split | match UV seams to hard edges |
