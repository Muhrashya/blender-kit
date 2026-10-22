# Variant: hard-surface (weapons, machines, vehicles)

| Topic | Rule |
|---|---|
| Method | primitives + planar cuts; booleans allowed while blocking, APPLIED and cleaned before topology |
| After boolean | run audit_topology: ngons and interior faces must be fixed (blender-topology-fix) |
| Bevels | real bevels only on the main silhouette edges; others by normal map (needs bake: HP bevelled, LP sharp) |
| Panels | panel lines are texture/normal detail, not geometry |
| Parts that move | separate objects with pivot at the hinge/axis |
| Cylinders | segment count from deformation-free table: far 6-8, mid 8-12, hero 16-24 |
| Pitfalls | tiny bevel triangles, shading streaks from ngons, non-planar quads after boolean |
| Quick tri estimate | beveled box (1 segment, 12 edges) = 44 tris |
