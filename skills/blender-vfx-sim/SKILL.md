---
name: blender-vfx-sim
description: Use when an effect needs simulation or fracture in Blender - smoke, fire, fluid-like motion, destruction chunks, debris - and the result must be baked into something a game engine can use (flipbook frames, chunk meshes with pivots, or baked motion if supported).
---
# VFX simulation -> exportable result

## Requires
FX spec (blender-vfx) naming the type: flipbook (volumetric) or chunks. `scene_info.py` output (Blender version, add-ons). engine.md VFX rows (VAT support) and Mesh rules.

## Inputs
Effect kind | size | duration | chunk count limit | platform.

## Steps
1. CHECKPOINT (`checkpoint.py`).
2. CHOOSE the path from `references/sim-notes.md` section 1. Realistic style: follow `references/realistic-path.md`. Low-poly or voxel style: do NOT simulate smoke/fire; build it from shapes (blender-vfx cookbook, Low-poly column) and go to blender-vfx-mesh or -flipbook. Chunks need the Cell Fracture operator: check `hasattr(bpy.ops.object, 'add_fracture_cell_objects')` (scene_info.py has_cell_fracture_op); absent -> tell the user to enable the add-on, or split manually.
3. SMOKE / FIRE: low-resolution domain, short cache, bake once (sim-notes.md section 2). Introspect domain properties before setting them.
4. CHUNKS: pieces <= 30 (mobile <= 15), each <= 100 tris, pivot at the piece center, transforms baked at the project fps (sim-notes.md section 3).
5. BAKE: simulation -> sprite frames (then blender-vfx-flipbook) or chunk meshes + baked transforms.
6. DELETE the domain, particle systems and forces from the export set; they never ship.
7. AUDIT: chunk meshes with `audit_mesh.py` (ALLOW_OPEN false, per-piece budget); flipbook via audit_flipbook.
8. SPEC: chunk list, pivots, clip name and fps, or the flipbook grid.

## Hard rules
| Rule | Detail |
|---|---|
| Never export a domain | bake to frames or meshes |
| Low resolution first | raise only if the flipbook reads badly |
| Chunk limits | counts and tris as above [START]; engine physics rebuilds motion |
| Fps | scene fps = engine.md fps before baking |
| Checkpoint | before fracture or bake |
| Baked motion | only when engine.md VFX row says supported; else flipbook |

## Done when
Exportable assets exist and pass their audits; simulation objects are excluded from the export; spec updated.

## On fail
| Failure | Action |
|---|---|
| Add-on missing | ask user to enable it, or build chunks by manual cuts |
| Bake too slow | lower resolution/steps; shorten duration |
| Chunks over budget | fewer pieces; merge small ones |
| Engine lacks baked motion | flipbook fallback |

## Next
blender-vfx-flipbook (frames) or blender-qa -> blender-export.
