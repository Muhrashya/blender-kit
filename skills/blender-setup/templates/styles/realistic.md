---
style: realistic
---
# Style: realistic (PBR, baked detail)

| Topic | Rule |
|---|---|
| Workflow | high-poly or sculpt (HP) -> retopo (LP) -> bake normal, AO, curvature -> PBR textures |
| Geometry | LP carries silhouette and deformation; HP carries detail |
| Textures | base color, normal, roughness, metallic (+ AO packed if engine.md says so); one texel density per project |
| Normal maps | required for hero assets; tangent space; convention from engine.md |
| Rig | Hero column of deformation-zones.md; corrective shapes only if engine.md lists support |
| Hands | 8 sides, 3 loops per joint, full 15-bone fingers |
| Triangle strategy | after retopo: remove hidden faces, bake what you can, keep loops at joints |
| Pitfalls | bake skew from bad cage; seams on smooth areas; texel density drift between assets |
| Audit overrides | HP is excluded from budget checks; LP must pass all audits |
