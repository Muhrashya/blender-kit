# Topology rules (full)

Contents: 1 definitions | 2 quads vs tris | 3 hard rules | 4 poles | 5 density | 6 minimum-triangle method | 7 reduction toolbox | 8 segments | 9 triangle math | 10 static vs deforming | 11 verification

## 1. Definitions
Quad = 4-vertex face (2 triangles). Triangle count of a mesh = sum over faces of (vertices - 2). Pole = interior vertex whose valence (edge count) is not 4: valence 3 = N-pole, valence 5 or more = E-pole. Edge loop = chain of edges running through quads. Ring = parallel edges across a strip.

## 2. Quads vs tris
| Situation | Use | Why |
|---|---|---|
| Deforming zone (joints, face, shoulders) | quads | predictable bending, weight painting, loops |
| Flat static surface, hard-surface prop | triangles allowed | engine triangulates anyway; saves budget |
| Silhouette curve on a static prop | quads or tris, whichever keeps the outline with fewer faces | budget |
| Mesh later bakes with a normal map | keep source quads, triangulate on export | avoids baked shading mismatch |
| N-gon (5+) anywhere | never | triangulates unpredictably, breaks shading |

## 3. Hard rules (final mesh) - checked by audit_mesh.py / audit_topology.py
| Check | Static | Deforming |
|---|---|---|
| n-gons | 0 | 0 |
| Doubles, zero-area faces, loose verts/edges | 0 | 0 |
| Non-manifold edges | 0 (open cards only with ALLOW_OPEN) | 0 |
| Scale/rotation applied, no negative scale | yes | yes |
| Triangles | allowed | none in joint zones |
| Non-planar quads | 0 (static: triangulate them) | 0 |
| Thin quads (aspect over 4:1 [START]) | 0 | 0 |

## 4. Poles
| Where | Allowed |
|---|---|
| Flat or low-motion areas (back, flat of torso, palm center, top of head) | yes, 3-pole and 5-pole |
| Within 1 ring of a joint (elbow, knee, shoulder, wrist, hip, ankle, finger joints) | NO |
| Around eyes / mouth openings | only 5-poles at the outer corners, outside the lip/eyelid fold |
| On silhouette curves of a static prop | avoid; shading may pinch |
Rules: poles come in pairs (every loop reduction adds a 3-pole and a 5-pole). Push poles toward areas that never bend, hidden areas, or texture seams. Closed all-quad mesh invariant: sum over vertices of (4 - valence) = 4 x Euler characteristic = 8 for a sphere-like mesh; a closed all-quad mesh that does not give a multiple of 8 has hidden non-quad faces or non-manifold geometry.

## 5. Density
| Rule | Value |
|---|---|
| Quad size | even across a form; denser only at silhouette curves and joints |
| Quad aspect | longest/shortest edge at most 4:1 [START] |
| Density gradient | change by at most one transition pattern at a time (transition-patterns.md) |
| Spikes | edges longer than 3x or shorter than 1/3 of the median [START] are defects |
| Ring vertex count | constant along limbs and tubes |

## 6. Minimum-triangle method (do in this order, stop when measured tris <= budget)
| Step | Action | Typical saving |
|---|---|---|
| 1 Budget | write the number; label [START] or [USER] | n/a |
| 2 Silhouette | place edges only where the outline curves at gameplay distance | largest |
| 3 Remove hidden | delete faces never visible: bottoms, backs, interior, joins | large on kits and props |
| 4 Bake | normal map / texture instead of bevels, screws, panels | large on hard-surface |
| 5 Dissolve flat | `bmesh.ops.dissolve_limit` (recipe R6) on coplanar edges | medium |
| 6 Reduce segments | round shapes per section 8 | medium |
| 7 Merge repeats | instance/mirror, share one mesh | n/a |
| 8 Measure | audit_mesh.py | n/a |
If still over budget, cut in THIS order: hidden faces -> tiny details -> density on flat or straight parts -> cylinder segments -> real bevels. Never cut joint loops of a deforming asset first.

## 7. Reduction toolbox
| Method | Use for | Risk | Recipe |
|---|---|---|---|
| Delete hidden faces | any static asset | none if truly hidden | R7 to find interior faces |
| Dissolve limited | coplanar patches | merges needed edges if angle too big | R6, angle 5 degrees |
| Merge doubles | cleanup | none at 1e-5 | R3 |
| Segment reduction | cylinders, spheres | faceting | rules section 8 |
| Join tris to quads | cleanup | uneven quads | R5 |
| Decimate (collapse) | static organic props only | destroys loops; never rigged | modifier `DECIMATE`, re-audit |
| Retopo | sculpts, bad flow | time | blender-retopo |

## 8. Segments for round shapes (static)
| Screen size at gameplay distance | Sides |
|---|---|
| tiny or far | 6-8 |
| medium | 8-12 |
| large or close | 12-24 |
Only silhouette-critical rings get more.

## 9. Triangle math
| Item | Formula |
|---|---|
| Face triangles | vertices - 2 |
| Quad count -> tris | tris = 2 x quads (when all quads) |
| Tube (open) | tris = 2 x sides x rows |
| Capped tube | open tube + 2 x (sides - 2) |
| Quadriflow target | `target_faces` counts quads: target_faces = budget_tris / 2 |
| Closed all-quad mesh | vertices = faces + Euler characteristic (2 for sphere-like) |
Engines count vertices after splitting at UV seams, hard edges and material borders; compare triangles, not vertices.

## 10. Static vs deforming
| | Static | Deforming |
|---|---|---|
| Priority | silhouette per triangle | loops at joints, then silhouette |
| Tris | allowed | quads only in zones |
| Cut candidates | bevels, flat density | flat limb mid-sections, hidden faces |
| Never cut | silhouette curves | joint loops |

## 11. Verification
Scripts: `audit_mesh.py` (budget, ngons, doubles, transforms, UV), `audit_topology.py` (defect map, poles near joints, symmetry, pole balance). Quote JSON numbers. Wireframe screenshots front/side/joint close-ups are required for deforming assets.
