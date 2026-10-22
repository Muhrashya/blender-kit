---
name: blender-camera
description: Use when planning or animating cinematic camera work in Blender - shot lists, shot sizes, angles, lenses, camera moves (static, pan, whip pan, tilt, push in, pull out, zoom, dolly zoom, roll, tracking/truck, arc, boom/crane, handheld, bird's-eye), turntables, hero reveals, VFX showcase and trailer shots. Triggers: camera, shot, cinematic, dolly, tracking, kamera, sinematik.
---
# Camera (cinematic shots)

## Requires
brief.md (asset or scene, purpose). Subject objects exist in the scene. `docs/blender/engine.md` Camera rows when the camera animation leaves Blender. Scene fps from engine.md or the render target.

## Inputs
Per shot: purpose (story beat or showcase goal) | subject object name | duration | deliverable (rendered frames/video, or camera animation for the engine).

## Steps
1. SHOT LIST: copy `docs/blender/templates/shot-list.md` to `blender-out/<scene>/shot-list.md`; one row per shot: id, purpose, size, angle, lens mm, movement, rig, frames, subject.
2. MOVE FROM PURPOSE: use `references/camera-moves.md` section 1 (purpose -> move). Default is static; motion needs a written reason.
3. SIZE, ANGLE, LENS: `references/shot-vocabulary.md`; lens values are [START]; compute FOV with its formulas.
4. RIG: run `docs/blender/scripts/camera_rig.py` (edit the SHOTS list at the bottom): target-driven pan/tilt, straight dolly/track/boom, zoom, dolly zoom, arc pivot, roll, baked handheld, bird's-eye. Names: `CAM_<Shot>`, `CAMRIG_<Shot>_Target`, `CAMRIG_<Shot>_Pivot`.
5. TIMING + EASING: `camera-moves.md` section 2 [START]; Bezier ease for human-feeling moves, linear for constant-speed tracks, dolly zoom and turntables.
6. SEQUENCE: each camera is bound to a timeline marker by the script; cut pace from `references/showcase-and-render.md` section 3.
7. LIGHT + RENDER: `showcase-and-render.md` sections 1 and 2 (aspect, fps, shutter, depth of field, composition guides).
8. AUDIT: `docs/blender/scripts/audit_camera.py` (edit its SHOTS list): subject framed at start/mid/end, horizon level unless roll, clip planes, duration, speed.
9. PREVIEW: viewport screenshots at start, middle, end of each shot to `blender-out/<scene>/screens/cam_<shot>_<n>.png`.
10. DELIVER: rendered frames/video, or camera animation export only when engine.md Camera rows say it is supported; otherwise write the engine recipe (FOV convention, path, timing) in the shot list.

## Hard rules
| Rule | Detail |
|---|---|
| Motivated movement | every move has a purpose in the shot list; no purpose, no move |
| Static first | movement lands harder after a stable stretch; start static when the purpose is emphasis |
| One main move per shot | combine only listed combos (dolly zoom = dolly + zoom) |
| Level horizon | roll_deg within 1 degree unless the shot is roll or Dutch |
| Subject framed | fully inside the frame at the sample frames unless the shot is a written reveal |
| FOV convention | convert per engine.md Camera rows; never assume vertical vs horizontal |
| Clip planes | clip_start below the nearest subject distance, clip_end above the farthest |
| Rare moves | handheld, roll, whip pan, zoom: used sparingly, each with a reason |
| Numbers | speeds, durations, angles are [START]; the audit reports measured values |

## Done when
audit_camera pass for every shot; screenshots saved; shot list complete (no empty Purpose); deliverable produced or engine recipe written.

## On fail
| Failure | Action |
|---|---|
| Subject cut off | move camera back or widen lens; re-audit |
| Horizon tilted by accident | remove roll; check constraint up axis; re-audit |
| Move feels mechanical | add ease in/out (Bezier) except for constant-speed moves |
| Jitter or pops | check interpolation and duplicate keys; in baked handheld lower step amplitude |
| Subject clipped by near plane | raise clip_start margin rules in showcase-and-render.md |
| Engine camera differs | recheck FOV convention (engine.md Camera) |

## Next
blender-qa (camera gate) then deliver renders, or blender-export when engine.md allows camera export. For VFX showcase: after blender-vfx.
