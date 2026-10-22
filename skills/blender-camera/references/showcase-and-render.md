# Showcase shots and render setup

Contents: 1 lighting | 2 render setup | 3 cut pace | 4 showcase recipes | 5 comfort

## 1. Lighting for showcases [START]
| Setup | Use |
|---|---|
| Three-point (key, fill, rim) | assets and characters |
| Neutral studio (gray background, soft light) | QA turntables and model sheets |
| Moody single key + rim | hero reveals and trailers |
| Emission-only effects on a dark background | VFX showcase; also test on a light background |
Rule: never judge color or topology under colored light; use neutral light for QA.

## 2. Render setup
```python
import bpy
sc = bpy.context.scene
print(bpy.app.version_string)
print([i.identifier for i in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items])   # pick the real ids
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.fps = 24
sc.render.use_motion_blur = True                  # introspect: property location differs by version
sc.render.motion_blur_shutter = 0.5               # 180 degrees
cam = bpy.data.objects['CAM_Shot01'].data
cam.dof.use_dof = False                           # on only when the style needs it
cam.show_composition_thirds = True                # framing aid
cam.clip_start, cam.clip_end = 0.05, 200.0        # [START]; subject must lie between
sc.camera = bpy.data.objects['CAM_Shot01']
```
Output: image sequence by default (PNG); video formats depend on the Blender build: introspect `sc.render.image_settings` file format enum before choosing.
Depth of field: set `cam.dof.focus_object` to the subject and an aperture (`cam.dof.aperture_fstop`) only for shallow-focus styles. Low-poly and stylized game cinematics often leave it off.

## 3. Cut pace [START]
| Shot | Seconds |
|---|---|
| Establishing | 3-5 |
| Medium | 2-4 |
| Close | 1-3 |
| Action cut | 0.5-2 |
| Logo / end hold | 2-4 |
Alternate sizes between cuts; match direction of motion across cuts.

## 4. Showcase recipes
| Showcase | Rig | Frames (24 fps) | Notes |
|---|---|---|---|
| Turntable | camera orbit via arc pivot, 360 degrees, linear | 120-240, drop the last frame for a seamless loop | neutral light; also used for QA |
| Hero reveal | boom up + tilt (or arc + push in) | 96-144 | start static for 12-24 frames |
| VFX showcase | locked medium-wide, push in on impact | 48-96 around the effect | test dark and light backgrounds |
| Environment establishing | boom down or slow track | 96-192 | include foreground layer |
| Character intro | tilt up from feet to head or arc | 72-120 | low angle for power |
| Trailer sequence | list of shots with different sizes | per cut pace | shot list required |

## 5. Comfort
Roll, whip pan, fast zoom and strong handheld can cause discomfort when long or repeated: keep them short and rare; no roll above 180 degrees per shot without splitting.
