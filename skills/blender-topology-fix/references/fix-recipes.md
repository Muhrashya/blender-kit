# Fix recipes

Contents: 1 defect -> recipe | 2 done thresholds | 3 escalation | 4 recipe details

Snippets: `docs/blender/reference/bpy-recipes.md` holds the recipe ids R1-R11 (apply transforms, normals, doubles, triangulate, join tris, dissolve, interior faces, apply modifier, shading, origin, mirror). If a bmesh call raises TypeError, print the message, read the expected arguments from it, retry once, then report.

## 1. Defect -> recipe
| Group | Defect (audit field) | Severity | Recipe |
|---|---|---|---|
| A | doubles | high | R3 merge doubles (1e-5) |
| A | loose verts / loose edges | high | delete them (bmesh: remove verts/edges with no faces) |
| A | zero-area faces | high | dissolve or delete, then R3 |
| A | negative scale / unapplied transforms | high | R1 |
| A | flipped normals | high | R2 |
| A | interior faces | high | R7: select, check count, delete if never visible |
| B | ngon on a static prop | high | triangulate that face only (`bmesh.ops.triangulate` with faces=[ngon faces]) |
| B | ngon in a deforming zone | blocker | rebuild with edge cuts so the area becomes quads: local patch (section 3) |
| B | tris (static) | none | keep if they save budget |
| B | tris in deforming zone | blocker | R5 join tris to quads on those faces; leftovers: local patch |
| B | non-planar quads (static) | medium | triangulate those faces |
| B | non-planar quads (deforming) | high | relax by moving the vertices toward the plane, or add an edge; verify |
| C | thin quads | medium | add a loop across the long side (`bmesh.ops.bisect_plane` on a tube/strip) or dissolve the short edge when two thin quads are neighbors |
| C | density spikes | medium | even the area: slide edges, merge short edges, add edge to long ones |
| C | poles near joints | blocker | move the pole: rotate an adjacent edge (`bmesh.ops.rotate_edges`) so the pole shifts one ring away from the joint; repeat until outside the joint zone; else local patch |
| C | missing joint loops | blocker | cut a loop perpendicular to the bone: `bmesh.ops.bisect_plane` with plane_no = bone axis, plane_co = joint position +- 10 percent of segment length; works cleanly only when quads are ring-aligned; verify ngons = 0 after |
| C | ring vertex count mismatch | high | transition pattern (docs/blender/reference/transition-patterns.md), placed mid-segment |
| C | asymmetry | high | R11 (mirror from the clean half) when asymmetry is unintended |
| D | pole balance not multiple of 8 on a closed all-quad mesh | info | indicates hidden ngons/tris/non-manifold: re-run counts |
| D | everything messy (AI or scan mesh) | blocker | blender-retopo |

Recipe notes:
- `bisect_plane` call: `bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], dist=1e-5, plane_co=Vector, plane_no=Vector)`. It cuts every face the plane crosses. On quads cut across two opposite edges it yields two quads (the loop you want); on faces cut diagonally it makes triangles/ngons. Run audit after; revert if ngons or tris rise.
- `rotate_edges`: `bmesh.ops.rotate_edges(bm, edges=[edge], use_ccw=False)` rotates the edge inside its two adjacent faces; it changes valence of the 4 end vertices by +-1.

## 2. Done thresholds
| Count | Static | Deforming |
|---|---|---|
| ngons | 0 | 0 |
| tri faces near joints | n/a | 0 |
| poles near joints | n/a | 0 |
| nonplanar quads | 0 or triangulated | 0 |
| thin quads | 0 (or triangulated) | 0 in zones |
| density spikes | under 1 percent of edges | under 1 percent |
| symmetry unmatched | 0 if symmetric | 0 if symmetric |
| doubles / loose / zero-area | 0 | 0 |

## 3. Escalation
Defect rate = (ngons + tri faces in zones + poles in zones + thin quads + nonplanar quads) / total faces, from the audit JSON.
| Rate or situation | Action |
|---|---|
| under 5 percent and recipes A-C finished | done after verify |
| 5 to 15 percent, or joint loops missing on 2 or more joints | local patch: delete the bad region, re-bridge with quads (blender-retopo manual method, patch only), keep boundary vertices |
| over 15 percent, or the mesh is a sculpt/scan/AI mesh | full blender-retopo |

## 4. Local patch (summary)
1. Select the bad region + one ring around it; duplicate the region as reference; delete the original region.
2. Rebuild the hole as quads whose boundary vertex count equals the surrounding ring counts (use a transition pattern if counts differ).
3. Bridge with `bmesh.ops.bridge_loops` for tube-to-tube gaps, or fill with grid fill (check `bpy.ops.mesh.fill_grid` availability by introspection) when the boundary has an even vertex count.
4. Shrinkwrap the patch to the duplicated reference to keep the shape; remove the reference.
5. Audit; screenshots.
