---
name: blender-retopo
description: "Use when converting a high-poly sculpt, scan, boolean-heavy or AI-generated mesh into a clean low-poly game mesh with proper edge flow, then preparing it for bake, UV and rigging. Triggers: retopo, retopology, remesh, high poly to low poly, sculpt to game mesh, messy AI mesh."
---
# Retopology (high -> low, rig-ready)

## Requires
Source mesh (HP). Brief with budget, style, deforming yes/no. Checkpoint. `docs/blender/engine.md` Rig section.

## Inputs
HP object name | target tris | deforming? | symmetric?

## Steps
1. CHECKPOINT (`checkpoint.py`, STAGE = "pre-retopo"). Duplicate HP as `SM_<Name>_HP`, hide it. Never edit the original.
2. CLEAN HP: merge doubles (R3), fill holes, recalc normals (R2), apply scale (R1). Run `audit_mesh.py` on HP with a huge BUDGET to read tris; no budget check on HP.
3. PLAN (write in state.md Decisions): method from `references/methods.md` section 1, target quads = budget / 2, guide loops for joints and eyes/mouth from `docs/blender/reference/deformation-zones.md`.
4. BUILD LP: follow the chosen method in methods.md. Create the LP as a new object `SM_<Name>_LP` (characters: `SK_<Name>_LP`).
5. CLEAN LP: `audit_topology.py` (ARMATURE if exists). Apply blender-topology-fix recipes until its Done thresholds hold.
6. PROJECT: shrinkwrap LP onto HP (nearest surface point), apply (methods.md section 3). Re-audit.
7. SILHOUETTE: screenshots HP vs LP, front, side, 3/4, same camera. Reject if the outline differs visibly.
8. BUDGET: tris <= budget, else cut with the blender-topology section 6 order (never joint loops first).
9. KEEP HP until the bake is verified (blender-uv-bake).

## Hard rules
| Rule | Detail |
|---|---|
| Quadriflow counts quads | target_faces = budget_tris / 2 |
| Auto result is a start | after quadriflow always run blender-topology-fix on the LP |
| Hard-surface | rebuild by hand from primitives; no auto-remesh |
| Rigged targets | no decimate, ever |
| Names | LP/HP suffixes per config.md |
| Poles | outside joint zones; jaw/eye/mouth rings preserved |
| HP | hidden, never deleted before bake verification |

## Done when
LP passes audit_mesh and audit_topology Done thresholds; tris <= budget; silhouette HP vs LP matches; LP and HP named; screenshots saved; state.md updated.

## On fail
| Failure | Action |
|---|---|
| Auto remesh ignores joints/eyes | add guide loops (methods.md section 2) and rerun, or build those regions by hand |
| LP loses silhouette | raise target quads by 10 percent, remove detail elsewhere |
| Over budget | blender-topology cut order |
| HP unusable (non-manifold, holes) | clean HP (methods.md section 4) before remesh |

## Next
blender-uv-bake (HP + LP) then blender-material, blender-rig (deforming).
