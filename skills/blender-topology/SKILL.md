---
name: blender-topology
description: Use for clean topology, edge flow, polycount and triangle budgets, quads vs tris, poles, edge loops, minimum-triangle modeling, rig-ready meshes, loop transitions - whenever a mesh must be light AND easy to rig, UV and export. Also use to answer topology questions and to check a mesh before UV, rig or export.
---
# Topology: clean flow + minimum triangles + rig-ready

## Requires
brief.md (budget, deforming yes/no, style, camera distance). A mesh from blender-model, blender-hands or blender-retopo. `docs/blender/engine.md` Rig section for influence/bone limits.

## Inputs
Budget (config.md row) | deforming? | camera distance | armature if it already exists.

## Steps
1. LOOK at `docs/blender/reference/figures/` when you need a picture (joint-loops, rig-ready-zones, transition-patterns). READ the rule files you need: `references/rules.md` (always), `docs/blender/reference/deformation-zones.md` (deforming assets), `docs/blender/reference/transition-patterns.md` (density changes).
2. BUDGET -> SILHOUETTE -> REMOVE -> BAKE -> MEASURE (details: rules.md section 6):
   1. Budget = config.md row for the role, Mobile column if platform = mobile.
   2. Silhouette: keep only edges that change the outline from the gameplay camera distance.
   3. Remove: delete every face the game camera cannot see (hidden joins, backs, bottoms, interior).
   4. Bake: move T3 detail to texture/normal map.
   5. Measure: `audit_mesh.py` (BUDGET set) then `audit_topology.py` (ARMATURE set when it exists).
3. DEFORMING ASSETS: place joint loops per `deformation-zones.md` for the style tier; keep ring vertex counts constant along limbs; move poles out of joint zones.
4. DENSITY: change loop count only with a pattern from `transition-patterns.md`, outside joint zones.
5. SYMMETRY: run `audit_topology.py` with SYMMETRIC=True when the asset is symmetric.
6. FIX defects: do not hand-edit blindly: run blender-topology-fix with the defect map.
7. RIG-READY CHECK (deforming only): table below must be all yes.
8. SCREENS: wireframe front, side, joint close-ups -> `screens/topo_*.png`.

## Rig-ready checklist (deforming assets)
| Check | Pass when | Source |
|---|---|---|
| Rest pose | A-pose (or engine pose), slight bend at elbows/knees | model variant |
| Symmetry | mirror_unmatched = 0, off-plane = 0 | audit_topology |
| Joint loops | per deformation-zones.md tier | visual + loop count |
| Poles near joints | 0 | audit_topology joints |
| Ngons / tris in joint zones | 0 / 0 | audit_topology joints |
| Ring vertex count | constant along each limb | visual + count |
| Quad aspect | thin_quads = 0 in zones | audit_topology |
| Transforms | scale/rotation applied | audit_mesh |
| Hands | ring continuity forearm -> wrist -> palm | blender-hands |
| Budget | tris <= budget | audit_mesh |

## Hard rules
| Rule | Detail |
|---|---|
| n-gons | 0 in every final mesh |
| Deforming zones | quads only; no triangles, no poles within 1 ring of a joint |
| Static props | triangles allowed where they save budget; source keeps quads where it is free |
| Subdivision | never used to get roundness; no subdivision modifier on exports |
| Decimate | never on rigged meshes; static props only as last resort, re-audit after |
| Triangulate | only on the export copy (or the last modifier), never on the working mesh |
| Numbers | every count quoted comes from the audit JSON of this session |
| Budget overrun | needs user approval; otherwise cut in the rules.md section 6 order |

## Done when
audit_mesh.pass = true AND audit_topology: ngons = 0, poles_near_joints = [] and tris_near_joints = [] (deforming), thin_quads = 0 in zones, pole_balance_multiple_of_8 true (closed all-quad meshes) AND rig-ready table all yes (deforming) AND wireframe screenshots saved.

## On fail
| Failure | Action |
|---|---|
| ngons, thin or non-planar quads, poles near joints, missing joint loops | blender-topology-fix |
| Defect rate above fix thresholds | blender-retopo |
| Over budget | rules.md section 6 cut order; then ask approval |
| Silhouette lost after cuts | restore the last cut; cut elsewhere |
| Hands wrong | blender-hands |

## Next
blender-uv-bake (static) or after hands/topology: blender-uv-bake -> blender-material -> blender-rig (deforming).
