---
style: lowpoly
---
# Style: lowpoly (faceted or simply smoothed, few triangles)

| Topic | Rule |
|---|---|
| Geometry | simple forms; keep only edges that change the silhouette |
| Shading | flat shading for faceted look, or smooth with hard edges at 30-60 degrees (pick one per project) |
| Color | palette or gradient texture (no unique texture unless a role needs it); vertex color only if engine.md says it is supported |
| Normal maps | optional; skip for background props |
| Cylinders | far 6-8 sides, mid 8-12, hero 12-16 |
| Rig | 1 loop pair at each bending joint (2 loops), poles away from joints |
| Triangle strategy | dissolve coplanar edges; remove hidden faces; reuse mirrored halves |
| Pitfalls | shading artifacts from long thin triangles: avoid sliver faces; keep aspect ratio under 4:1 |
| Audit overrides | triangles are fine on static props; deforming zones stay quads |
