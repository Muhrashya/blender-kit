---
name: blender-vfx-mesh
description: Use when making mesh-based effects - slash arcs, shockwave rings, beams, cones, shield domes, aura shells, vortex strips - with UVs prepared for scrolling and gradient masks, minimal triangles and engine-ready pivots.
---
# Mesh VFX

## Requires
FX spec (blender-vfx), mask textures (blender-vfx-texture), engine.md VFX rows (UV scroll, vertex color, blend modes).

## Inputs
Shape type | size in meters | trigger | platform.

## Steps
1. SHAPE + STYLE: pick from `references/shapes.md`; triangle range from `docs/blender/reference/vfx-styles.md` (low-poly 8-60, voxel 12-120 boxes, stylized 30-150, realistic 100-500). Low-poly: faceted shards, flat discs/rings/stars, hard alpha mask.
2. UV: U runs in the direction of motion; V across; all UVs in 0-1.
3. PIVOT: origin at the effect origin (slash: handle end, ring: center, beam: start, dome: base center); apply scale and rotation.
4. VERTEX COLOR (only if engine.md says supported): R = fade along length/life, G = edge softness.
5. MATERIAL: unlit emissive look, grayscale mask, additive or alpha per spec; no custom nodes shipped.
6. ANIMATION: prefer engine-driven (scale, UV scroll, dissolve). Key in Blender only when needed: one action, fps from engine.md, curve recorded in the spec.
7. AUDIT: `audit_mesh.py` with ALLOW_OPEN = True and CHECK_UV_RANGE = True; BUDGET from config.md fx-mesh.
8. SCREENS: dark and light backgrounds, gameplay distance.
9. SPEC: blend mode, scroll speed, scale over life, dissolve threshold, pivot, facing.

## Shapes (summary; details in shapes.md)
| Effect | Geometry | Tris about |
|---|---|---|
| Slash | curved tapered strip | 32 |
| Shockwave | flat annulus 16-32 segments | 64 |
| Beam / cone | open tube 8-12 sides, no caps | 16-24 per ring pair |
| Shield dome | hemisphere 12x6 | 100 |
| Aura | scaled copy of the low mesh | reuse |
| Vortex | twisted strip | 48 |

## Hard rules
| Rule | Detail |
|---|---|
| Single-sided | no caps, no interior faces; double-sided look is an engine material setting |
| UV range | 0-1, U along motion |
| Budget | fx-mesh row; most shapes 20-300 tris |
| Pivot | stated and applied |
| Overdraw | count stacked transparent layers in the spec |

## Done when
audit_mesh pass (open allowed, UV in range); readability screenshots saved; spec filled.

## On fail
| Failure | Action |
|---|---|
| UV outside 0-1 | re-unwrap or scale UV islands |
| Over budget | halve segments; remove rings |
| Unreadable on light background | alpha or cutout blend; raise contrast |
| Sorting artifacts | additive, cutout, or fewer overlapping layers |

## Next
blender-qa -> blender-export.
