# Flipbook render

Contents: 1 grid | 2 render setup | 3 loop | 4 packing

## 1. Grid [START]
| Use | Grid | Frame px | Sheet px |
|---|---|---|---|
| Small hit or puff | 4x4 | 128 | 512 |
| Smoke or fire | 6x6 or 8x8 | 128-256 | 768-2048 |
| Mobile | 4x4 | 64-128 | 256-512 |
Sheet and frame sizes power-of-two where the engine requires it (e.g. 4x4 of 128 = 512). A 6x6 grid of 128 gives 768, not a power of two: use 8x8 or 4x4 when engine.md requires power-of-two sheets.

## 2. Render setup
```python
import bpy
sc = bpy.context.scene
print([i.identifier for i in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items])   # pick the real EEVEE id
sc.render.film_transparent = True
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'Standard'
sc.render.resolution_x = sc.render.resolution_y = 128
sc.render.resolution_percentage = 100
sc.frame_start, sc.frame_end = 1, 16
sc.render.filepath = '//blender-out/FX_Name/flipbook_frames/f_'
cam = bpy.data.objects['CAM_FX']; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 3.0
sc.camera = cam
bpy.ops.render.render(animation=True)
```
World background black or transparent; emission-only materials for glow.

## 3. Loop
Render frames 1..N+1, delete the last file, or use a cache that loops. audit_flipbook loop_seam_ratio <= 1.5 [START].

## 4. Packing
`pack_sheet.py` reads PNGs sorted by name, scales to FRAME_PX if needed, packs frame 0 at top-left. Confirm with audit_flipbook.
