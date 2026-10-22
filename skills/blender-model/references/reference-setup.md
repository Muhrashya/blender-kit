# Reference setup in Blender

Contents: 1 image empties | 2 orthographic cameras | 3 overlay compare

## 1. Image empties
```python
import bpy
def add_ref(path, name, rot_deg, loc=(0, 0, 0), size=2.0, opacity=0.5):
    bpy.ops.object.empty_image_add(filepath=bpy.path.abspath(path), align='WORLD', location=loc)
    e = bpy.context.active_object
    e.name = name
    e.empty_display_size = size
    e.rotation_euler = [r * 3.14159265 / 180 for r in rot_deg]
    e.color[3] = opacity
    e.show_in_front = False
    return e
# front view image faces -Y -> rotation (90, 0, 0); side view -> (90, 0, 90). Confirm by screenshot.
```
Name them `REF_Front`, `REF_Side`. They are not exported.

## 2. Orthographic cameras
```python
cam_data = bpy.data.cameras.new("CAM_Front"); cam_data.type = 'ORTHO'; cam_data.ortho_scale = 2.5
cam = bpy.data.objects.new("CAM_Front", cam_data); bpy.context.collection.objects.link(cam)
cam.location = (0, -10, 1); cam.rotation_euler = (1.5708, 0, 0)
bpy.context.scene.camera = cam
```
Side camera: location (10, 0, 1), rotation (1.5708, 0, 1.5708). `ortho_scale` must be at least the larger asset dimension plus 10 percent.

## 3. Overlay compare
Take the same screenshot with the reference visible and hidden. Compare silhouette extents (left/right/top/bottom) and part positions. Report differences as ratios of height [ESTIMATED]. Fix the largest first.
