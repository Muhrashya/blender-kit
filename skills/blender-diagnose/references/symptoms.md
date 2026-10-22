# Symptom table

Contents: A shading and normals | B UV and bake | C scale, axis, export | D rig and deformation | E animation | F VFX | G modular and misc

CHECK scripts live in `docs/blender/scripts/`. Snippet names refer to `bpy-recipes.md`.

## A. Shading and normals
| Symptom | Likely cause | CHECK | FIX | Route |
|---|---|---|---|---|
| Black or dark patches | flipped face normals; negative scale | `audit_mesh.py` -> negative_scale; face-orientation overlay screenshot | apply scale (recipe R1); recalc normals (R2) | none |
| Faceted look on a mesh meant to be smooth | faces not smooth-shaded | read `me.polygons[i].use_smooth` ratio | shade smooth (R9, version dependent: introspect) | none |
| Weird smooth shading streaks | ngons or long thin triangles | `audit_topology.py` -> ngons, thin_quads | triangulate/rebuild those faces | blender-topology-fix |
| Hard edges look soft or soft edges look hard after export | smoothing / sharp data not exported or engine recalculates | `export_asset.py` options_used (normals) | export normals; engine import: use imported normals (engine.md) | blender-export |
| Shadow terminator artifacts | low-poly + smooth shading | screenshot under a grazing light | add one support loop or split hard edge | blender-topology |

## B. UV and bake
| Symptom | Likely cause | CHECK | FIX | Route |
|---|---|---|---|---|
| Texture stretched | non-uniform scale or bad unwrap | `audit_uv.py` density out of tolerance; scale in audit_mesh | apply scale; re-unwrap; repack | blender-uv-bake |
| Visible seams in the engine | low bake margin; seam across smooth area | bake margin value; screenshot | raise margin; move seams to hard edges | blender-uv-bake |
| Normal map bumps look inverted | green-channel convention mismatch | engine.md Materials row "Normal map" | flip green channel on bake/import | blender-material |
| Bake has skewed or floating artifacts | cage or ray distance wrong; HP/LP misaligned | cage_extrusion, max_ray_distance; overlay screenshot | tune cage; align HP and LP origins and scale | blender-uv-bake |
| Colors differ between Blender and engine | color space; lighting | texture colorspace per slot (engine.md) | base color sRGB, data maps Non-Color | blender-material |

## C. Scale, axis, export
| Symptom | Likely cause | CHECK | FIX | Route |
|---|---|---|---|---|
| Wrong size in engine | unit scale or FBX scale option | `scene_info.py` unit_scale; import test cube (engine.md) | set scale option per engine.md; apply transforms | blender-export |
| Rotated 90 degrees in engine | axis options; unapplied rotation | audit_mesh rotation_applied; axis in options_used | apply rotation; set forward/up per engine.md | blender-export |
| Textures or materials missing after export | textures not exportable (custom nodes) | material node types (blender-material pbr-minimum) | rebuild as Principled + image nodes | blender-material |
| Extra objects in the file | `use_selection` false | export_asset.py options_used | select only deliverables; use_selection True | blender-export |
| Animations missing | action not exported; option name differs by version | introspect the exporter properties | set the version's animation option | blender-export |
| Tri count higher in engine | engine counts after triangulation; modifiers not applied | audit_mesh `tris` (evaluated) vs engine number | compare triangles, not vertices; apply modifiers | blender-export |

## D. Rig and deformation
| Symptom | Likely cause | CHECK | FIX | Route |
|---|---|---|---|---|
| Mesh tears or spikes when posed | unweighted verts; > max influences | `audit_rig.py` unweighted_verts, max_influences | assign weights; limit total; normalize | blender-rig |
| Pinching or flattening at elbow/knee | too few loops; pole at joint | `audit_topology.py` ARMATURE set: poles_near_joints; loops count | add joint loops; move poles | blender-topology-fix |
| Candy-wrapper twist at forearm | one twist joint | pose forearm 90 degrees, screenshot | add 1-2 twist bones or distribute rotation (rig variants) | blender-rig |
| Fingers cross-influence | weights bleed between fingers | per-finger vertex group check (audit_rig deform_bones_without_weights) | isolate weights per finger | blender-hands |
| Left and right deform differently | asymmetric mesh or weights | `audit_topology.py` SYMMETRIC=True | mirror mesh/weights | blender-topology-fix, blender-rig |
| Mesh does not follow the bones | missing Armature modifier or parent | audit_rig armature_modifier_present | add modifier / re-parent | blender-rig |

## E. Animation
| Symptom | Likely cause | CHECK | FIX | Route |
|---|---|---|---|---|
| Loop pops | first and last pose differ | `audit_anim.py` loop_open_channels | copy first key to last frame | blender-animate |
| Foot sliding | travel speed vs stride | measure root drift per cycle (audit_anim ROOT_BONE) | match speed to stride or use engine root motion (engine.md) | blender-animate |
| Wrong clip length in engine | fps mismatch | scene fps vs engine.md fps | set fps before keying | blender-animate |

## F. VFX
| Symptom | Likely cause | CHECK | FIX | Route |
|---|---|---|---|---|
| Flipbook jitters or clips | subject touches frame edge; camera moved | `audit_flipbook.py` clipped_frames | widen padding; lock camera | blender-vfx-flipbook |
| Effect invisible on light background | additive blend on white | readability screenshots (dark + light) | alpha or cutout; raise contrast | blender-vfx |
| Transparent sorting glitches | overlapping alpha meshes | count overlapping layers | additive, cutout, or fewer layers | blender-vfx-mesh |
| Simulation too slow | resolution too high | domain resolution value | lower resolution, bake once | blender-vfx-sim |

## G. Modular and misc
| Symptom | Likely cause | CHECK | FIX | Route |
|---|---|---|---|---|
| Gaps or black lines between modules | pieces not snapped; mismatched edges | compare boundary vertex positions | snap to kit grid; weld | blender-model |
| Z-fighting | overlapping coplanar faces; interior faces | `audit_topology.py` / select interior faces (R7) | delete interior duplicates | blender-topology-fix |
| Jagged silhouette far away | too few segments on curves | silhouette screenshot at gameplay distance | add segments only on silhouette | blender-topology |
