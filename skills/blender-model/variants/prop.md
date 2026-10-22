# Variant: prop (static object)

| Topic | Rule |
|---|---|
| Start | one primitive per rigid part; real size |
| Origin | base center on the floor plane (Z = 0 at the bottom) unless engine.md says otherwise |
| Symmetry | mirror one half; keep center vertices exactly on the mirror plane (x = 0) |
| Edge budget | edges only where the outline curves; flat areas get none |
| Hidden faces | delete bottoms, backs against walls, faces inside joined parts |
| Handles / straps | boxes or 6-8 sided tubes by role |
| Detail | T3 -> texture / normal map |
| Pitfalls | floating bevels (use normal map), subdivision "for roundness", forgotten interior faces |
| Quick tri estimate | box = 12 tris, 8-sided cylinder (capped) = 28 tris, 12-sided = 44 tris, 16-sided = 60 tris |
