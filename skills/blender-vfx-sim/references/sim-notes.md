# Simulation notes

Contents: 1 path choice | 2 smoke and fire | 3 chunks | 4 baking and cleanup

## 1. Path choice
| Effect | Path | Output |
|---|---|---|
| Smoke, fire, explosion volume | smoke/fire simulation -> render frames | flipbook |
| Breaking prop | cell fracture -> chunks | meshes + pivots (+ baked clip if wanted) |
| Cloth/flag | rigged strips or baked motion only if engine.md supports it | rig or baked |
| Fluid | avoid: flipbook or mesh effect | flipbook |

## 2. Smoke and fire
Introspect: `[p.identifier for p in bpy.types.FluidDomainSettings.bl_rna.properties]` before setting resolution or time properties. Quick effect operators exist (`bpy.ops.object.quick_smoke`); check with `hasattr`. Keep resolution low (such as a 32-64 maximum cell resolution [START]), bake the cache, render a few frames, then raise only if unreadable.

## 3. Chunks (Cell Fracture)
1. Use the Cell Fracture operator on the LP prop (ground truth names via introspection of `bpy.ops.object.add_fracture_cell_objects.get_rna_type().properties`).
2. Limits: pieces <= 30 (mobile <= 15) [START]; each <= 100 tris.
3. Each piece: origin at its center, normals consistent, material kept.
4. Name `SM_FX_<Name>_Chunk_##`; group in `COL_FX_<Name>`.
5. If a clip is wanted: bake rigid-body motion to keyframes at the project fps (operator `bpy.ops.rigidbody.bake_to_keyframes`, confirm presence with hasattr), name `AN_FX_<Name>`.

## 4. Baking and cleanup
Before export remove: domain objects, flow/effector objects, rigid-body world, particle systems. Verify with scene_info.py that only deliverables remain selected.
