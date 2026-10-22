---
name: blender-uv-bake
description: Use for UV unwrapping, seams, texel density, UV packing, and baking normal, AO or curvature maps from high-poly to low-poly, or palette UVs for voxel and lowpoly styles. Triggers: UV, unwrap, seam, texel density, bake, normal map, AO, texture stretched.
---
# UV and bake

## Requires
Low-poly mesh that passed blender-topology (audit_mesh pass). HP object for realistic/stylized bakes. config.md texel density + texture sizes. engine.md Materials row (normal map convention, color spaces).

## Inputs
Role | texture size (config.md) | style (palette or baked) | HP name if baking.

## Steps
1. PATH by style (`style.md`): palette (voxel, lowpoly) -> section A; baked (stylized, realistic) -> section B of `references/uv-rules.md`.
2. SEAMS: place per `uv-rules.md` section 1 (hard edges, hidden areas, along loops, never across a face's main view).
3. UNWRAP + PACK: margin per section 2; keep islands straight (align to axes where a texture has directional detail).
4. DENSITY: set TEXTURE_PX and TARGET_DENSITY in `audit_uv.py`, run it. Tolerance +-20 percent; fix by scaling islands, not the object.
5. BAKE (baked styles): follow `references/bake.md` (cage, ray distance, margin, naming `T_<Asset>_Normal`, AO, etc.). Verify by screenshot: LP with the baked map vs HP, same camera and light.
6. SAVE textures to `blender-out/<asset>/textures/`; pack or reference with relative paths; names per config.md.
7. AUDIT: `audit_mesh.py` CHECK_UV_RANGE as needed; `audit_uv.py`.

## Hard rules
| Rule | Detail |
|---|---|
| One UV set for the game texture | extra sets only if engine.md lists lightmap/second UV use |
| 0-1 space | all islands inside 0-1 unless the role is tiling (then state it in state.md) |
| Texel density | one project value; assets within +-20 percent |
| Mirrored UVs | allowed only when the style/role allows shared texels; normal-mapped assets never overlap mirrored islands unless flagged |
| Normal map convention | from engine.md; if UNVERIFIED label it and ask the user to confirm on the import test |
| Color spaces | base color sRGB; normal/roughness/metallic/AO Non-Color |
| Bake inputs | HP and LP aligned, scale applied, normals consistent |

## Done when
has_uv; audit_uv pass; baked maps exist and the verification screenshot shows no skew or seams; textures saved and named.

## On fail
| Failure | Action |
|---|---|
| Density out of tolerance | rescale islands; re-pack; rerun audit_uv |
| Bake artifacts | blender-diagnose row B (cage, ray distance, alignment) |
| Seams visible | raise margin; move seams to hard edges |
| Stretched UVs | add seams; unwrap method conformal/angle-based; check object scale |
| Topology changed after UV | blender-topology-fix -> redo UV (state.md STALE) |

## Next
blender-material -> blender-rig (deforming) or blender-qa.
