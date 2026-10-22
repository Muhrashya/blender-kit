---
name: blender-rig
description: Use when rigging a mesh for a game - armature, bone hierarchy and naming, skin weights, influence limits, rigid-part rigs, test poses, deform-only export skeleton. Triggers: rig, armature, bone, skin, weights, IK, deform, mesh tears when bent. Requires a topology-clean mesh.
---
# Rig (game skeleton + weights)

## Requires
Mesh with state.md topology = PASS (deforming rule set). Hands done (characters). `docs/blender/engine.md` Rig rows (skeleton type, bone naming, influences, max bones). Transforms applied.

## Inputs
Rig type (humanoid / quadruped / mech-prop) -> read ONE file from `variants/`. Rig tier (Full / Reduced / Rigid).

## Steps
1. PRE-CHECK: run `audit_topology.py` with SYMMETRIC when applicable. Joint-zone counts must be 0. Fail: blender-topology-fix first.
2. ARMATURE: `ARM_<Asset>`, one root bone, hierarchy and names from the variant file; engine.md naming rules override (never invent them).
3. BONE PLACEMENT: bone heads at joint centers measured from the mesh (read vertex positions), not by eye; bones inside the volume; symmetric `.L`/`.R` names.
4. DEFORM FLAGS: only game bones deform; helper/IK/control bones are `use_deform = False` and in a separate collection, not exported.
5. SKIN: parent with automatic weights (`bpy.ops.object.parent_set(type='ARMATURE_AUTO')` with the mesh selected and the armature active), then clean following `references/weights.md`.
6. LIMITS: limit influences to engine.md (default 4 labeled [START]), normalize.
7. HANDS: apply the weight ramps from docs/blender/reference/hand-topology.md section 8.
8. TEST POSES: `references/weights.md` section 4 (3 poses per joint) with screenshots.
9. AUDIT: `audit_rig.py` (MAX_INFLUENCES, MAX_BONES from engine.md); `audit_naming.py`.

## Hard rules
| Rule | Detail |
|---|---|
| One root bone | and a single armature object |
| Naming | engine.md rules first; else variant file names with `.L` / `.R` |
| Rest pose | the pose the mesh was modeled in; never skin in a different pose |
| Influences | never above the engine limit; default 4 [START] |
| Weights | normalized, no unweighted vertex |
| Armature modifier | present on every skinned mesh |
| Deform only | non-deform bones excluded from export |
| Scale | armature scale 1, rotation applied |
| Rigid parts | rigid weights (1.0) or parenting, no soft weights |

## Done when
audit_rig pass; test pose screenshots show no tears, no collapse; bone count within engine.md limit (or labeled UNVERIFIED); weights normalized; naming pass; state.md updated.

## On fail
| Failure | Action |
|---|---|
| Collapse or pinch at a joint | blender-diagnose row D -> blender-topology-fix (joint loops) |
| Too many influences | limit total + normalize; then re-test |
| Candy-wrapper forearm | twist bones (variants/humanoid.md section 3) |
| Asymmetric deformation | mirror weights from the clean side after mesh symmetry audit |
| Engine requires a specific skeleton | read engine.md Rig rows; if UNVERIFIED ask the user; do not invent |

## Next
blender-animate (clips) or blender-qa -> blender-export.
