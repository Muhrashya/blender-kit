---
name: blender-vfx-texture
description: Use when making effect textures - gradient ramps, soft circles, streaks, swirls, noise, crack masks, dissolve noise, ring masks, trail strips - baked to small grayscale or RGBA PNGs with correct channel packing and tiling flags for VFX.
---
# VFX textures

## Requires
FX spec started (blender-vfx). engine.md Materials rows (channel packing, color space) and VFX rows (UV scroll, dissolve support).

## Inputs
Texture kind (list in `references/texture-types.md`) | size | tileable? | channel plan.

## Steps
1. PICK kind and recipe from `references/texture-types.md` section 1.
2. SIZE + STYLE: per `docs/blender/reference/vfx-styles.md` (realistic 256-512, stylized 128-256, low-poly 64-128, voxel 16-64 nearest). Low-poly/voxel masks use hard edges (threshold the gradient), no noise.
3. BUILD procedurally in Blender (shader nodes -> bake) or paint in numpy via `bpy.data.images.new` pixels.
4. RANGE: grayscale masks use the full 0-1 range; alpha masks keep a fully transparent border (at least 2 px).
5. TILING: if the effect scrolls, check wrap continuity: left edge equals right edge, top equals bottom (difference under 0.02 on mean [START]).
6. PACKING: pack masks into R/G/B only if engine.md lists the channel order; else keep separate files.
7. COLOR SPACE: masks are Non-Color; color textures sRGB.
8. NAME: `T_FX_<Name>_<Mask|Noise|Ramp|Trail>`; save to `blender-out/<fx>/textures/`.
9. SPEC: add each file with size, tiling flag, channel meaning.

## Hard rules
| Rule | Detail |
|---|---|
| Small | 128-256; a bigger texture needs a stated reason |
| Grayscale first | tint in the engine |
| Border | transparent border for sprites and strips |
| Tileable flag | stated in the spec |
| No procedural nodes shipped | bake |

## Done when
Files exist with sizes in the spec; tiling check passes for scrolling textures; screenshots on dark and light backgrounds.

## On fail
| Failure | Action |
|---|---|
| Visible tile seam | offset and blend the edges, or generate with a periodic function |
| Banding | add 1-2 percent noise before 8-bit save |
| Engine ignores channels | keep separate textures |

## Next
blender-vfx-mesh (mesh effects) or blender-qa.
