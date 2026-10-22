---
name: blender-topology-fix
description: Use when a mesh has bad topology and must be repaired - ngons, triangles in bend zones, poles at joints, uneven density, thin or non-planar quads, missing joint loops, asymmetry, messy AI or sculpt-derived meshes, "fix topology", "rapikan topologi". Diagnoses with a defect map, applies ordered fixes, escalates to retopo when needed.
---
# Topology fix (diagnose -> repair -> verify -> escalate)

## Requires
A mesh object. Checkpoint saved. Armature if it exists (for joint checks). brief.md budget and style.

## Inputs
Object name. Optional: deforming? yes/no, symmetric? yes/no.

## Steps
1. CHECKPOINT: `scripts/checkpoint.py` (STAGE = "pre-fix").
2. MAP: run `audit_mesh.py` and `audit_topology.py` (set ARMATURE and SYMMETRIC when they apply; SELECT_DEFECTS = True). Save both JSON outputs to `blender-out/<asset>/audit/fix_before.json`.
3. CLASSIFY every nonzero count with `references/fix-recipes.md` section 1 (severity + recipe). Order: A (safe cleanup) -> B (face-type fixes) -> C (flow fixes) -> D (rebuild).
4. REPAIR in that order. After EACH recipe group re-run `audit_topology.py`; stop a recipe that makes any count worse and restore the checkpoint.
5. ESCALATE using the thresholds in `references/fix-recipes.md` section 3: local patch retopo or full blender-retopo.
6. VERIFY: `audit_mesh.py` + `audit_topology.py` again; wireframe screenshots front, side, each joint close-up.
7. REPORT before/after table (counts per defect type) + screenshots. Update state.md: topology, uv-bake, hands, rig, animate, qa, export -> STALE.

## Hard rules
| Rule | Detail |
|---|---|
| Checkpoint first | no repair without `pre-fix.blend` |
| Measure after each group | no batch of fixes without re-audit |
| Original untouched | work on a duplicate when the user did not ask for in-place edits |
| Deforming zones | quads only; do not "fix" an ngon there by triangulating |
| Static props | triangulating a flat ngon or a non-planar quad is allowed |
| Silhouette | compare front/side silhouette before/after; revert if it changes visibly |
| Decimate | never as a fix for rigged meshes |
| No invented parameters | bmesh op kwargs that raise errors are reported, then adapted from the error text |

## Done when
Thresholds in fix-recipes.md section 2 met: ngons = 0; tris/poles/ngons near joints = 0 (deforming); nonplanar = 0 and thin = 0 in zones (or triangulated on static props); density_spikes under 1 percent of edges; symmetry unmatched = 0 (symmetric assets); tris within budget.

## On fail
| Failure | Action |
|---|---|
| Defects remain after recipes A-C | escalate (section 3) |
| Silhouette changed | restore checkpoint, apply recipes more locally |
| Budget exceeded after fixes | blender-topology cut order |
| Joint loops missing and no room to add | blender-retopo (local patch) |

## Next
blender-topology (full audit) then the paused or next stage in the chain.
