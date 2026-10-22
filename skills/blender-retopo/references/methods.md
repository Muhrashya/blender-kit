# Retopo methods

Contents: 1 method choice | 2 quadriflow | 3 shrinkwrap | 4 HP cleanup | 5 manual retopo | 6 character budget split

## 1. Method choice
| Source | Method |
|---|---|
| Static organic prop (rock, plant) | quadriflow -> topology-fix |
| Character / creature | quadriflow base with symmetry, then hand-fix loops at joints, eyes, mouth, hands |
| Hard-surface | manual rebuild from primitives (section 5) |
| AI-generated or scanned (messy, noisy) | voxel remesh HP (to close holes), then quadriflow, expect 2 cleanup passes |
| Sculpt with symmetric form | retopo one half, mirror |

## 2. Quadriflow
Introspect first: `print([p.identifier for p in bpy.ops.object.quadriflow_remesh.get_rna_type().properties])`.
```python
import bpy
obj = bpy.data.objects["SM_Name_LP"]            # duplicate of HP
budget_tris = 4000
with bpy.context.temp_override(object=obj, active_object=obj, selected_objects=[obj], selected_editable_objects=[obj]):
    bpy.ops.object.quadriflow_remesh(mode='FACES', target_faces=budget_tris // 2, use_mesh_symmetry=True)
```
Properties named above are the ones the Blender manual lists; keep only those present in the introspection output. Result: all-quad mesh near the target. Guide loops (joints, eyes, mouth): the operator has an option to preserve sharp edges and boundaries; for exact loop placement use manual cuts after remesh (topology-fix recipe for joint loops).

## 3. Shrinkwrap
```python
mod = lp.modifiers.new("SW_Project", 'SHRINKWRAP')
mod.target = hp
mod.wrap_method = 'NEAREST_SURFACEPOINT'
with bpy.context.temp_override(object=lp, active_object=lp, selected_objects=[lp], selected_editable_objects=[lp]):
    bpy.ops.object.modifier_apply(modifier=mod.name)
```
Confirm property names with `[p.identifier for p in bpy.types.ShrinkwrapModifier.bl_rna.properties]`.

## 4. HP cleanup
| Problem | Fix |
|---|---|
| holes | fill holes, or voxel remesh the HP duplicate (modifier REMESH, mode VOXEL; confirm properties by introspection) |
| non-manifold | audit_mesh non_manifold_edges; merge doubles; delete loose |
| millions of triangles | work on a decimated copy for remesh input only; keep the original for baking |
| inverted normals | R2 |

## 5. Manual retopo (hard-surface, hands, local patches)
1. Duplicate HP as reference; put it on a hidden-but-snappable collection.
2. Build the LP from primitives or by extruding edge loops, with a Shrinkwrap modifier (NEAREST_SURFACEPOINT) on the LP during editing so vertices stay on the HP surface (apply at the end).
3. Draw loops where bones bend first (deformation-zones.md), then fill the rest.
4. Boundary vertex counts of patches must match their neighbors (transition patterns if not).
5. Audit after each region.

## 6. Character budget split [START]
| Part | Share |
|---|---|
| Head | 20-25 percent |
| Torso | 25 percent |
| Arms | 15-20 percent |
| Hands | 10-15 percent |
| Legs and feet | 20-25 percent |
Remove share from flat torso and mid-limb first. Never take from joint loops.
