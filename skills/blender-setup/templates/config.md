# Blender Kit config (edit freely; every skill reads this first)

engine: generic-gltf        # name of the active profile; the full profile is docs/blender/engine.md
style: lowpoly              # voxel | lowpoly | stylized | realistic; the full file is docs/blender/style.md
rigor: balanced             # strict | balanced | flex (how rigid the workflow is; see ground-rules.md section 10)
fx_style: stylized          # realistic | stylized | lowpoly | voxel (defaults to style; override per effect with fx=)
platform: pc                # pc | mobile  (mobile = use the Mobile column)
up_axis_blender: Z
units: metric, unit_scale 1.0
output_root: blender-out/<asset>/     # brief.md, ref-analysis.md, audit/, screens/, checkpoints/, export/

## Naming (prefix_PascalCase_Variant)
| Type | Prefix | Example |
|---|---|---|
| Collection | COL_ | COL_Crate |
| Static mesh | SM_ | SM_Crate_LP |
| Skinned mesh | SK_ | SK_Knight_LP |
| High-poly (bake source) | suffix _HP | SM_Crate_HP |
| Low-poly (game mesh) | suffix _LP | SM_Crate_LP |
| Material | MAT_ | MAT_Crate |
| Texture | T_ | T_Crate_BaseColor |
| Armature | ARM_ | ARM_Knight |
| Animation action | AN_ | AN_Knight_Walk_loop |
| Effect object | FX_ / SM_FX_ / T_FX_ | SM_FX_Slash |
| Camera / Light | CAM_ / LGT_ | CAM_Ref |

## Triangle budgets  [START]  (starting points, NOT engine limits; engine limits live in engine.md)
Budget = triangles of the FINAL evaluated mesh (modifiers applied), per object.
| Role | PC | Mobile |
|---|---|---|
| prop-small | 300-800 | 150-400 |
| prop-mid | 800-2,500 | 400-1,200 |
| prop-hero | 2,500-6,000 | 1,200-3,000 |
| env-module | 500-2,000 | 250-1,000 |
| env-structure | 2,000-8,000 | 1,000-4,000 |
| char-npc | 3,000-8,000 | 1,500-4,000 |
| char-hero | 10,000-25,000 | 4,000-10,000 |
| creature | 5,000-20,000 | 2,000-8,000 |
| fx-mesh | 20-300 | 20-150 |
Rule: pick the LOW end of the row unless the silhouette fails the check in blender-topology. Exceeding a budget needs user approval.
Unknown role: pick the closest row, label it [ASSUMED], tell the user.

## Textures  [START]
texel_density_px_per_m: 256       # one value per project; keep every asset within +-20 percent
texture_size_by_role: prop-small 256 | prop-mid 512 | prop-hero 1024 | env-module 512 | char 1024 | fx-texture 128-256 | flipbook-frame 128-256
palette_texture_styles: voxel, lowpoly may use a tiny palette texture (16x16 to 64x64) with nearest filtering

## LOD  [START]
lods: none unless engine.md or the user asks. If asked: LOD1 about 50 percent, LOD2 about 25 percent of LOD0 triangles.

## Project overrides (user fills; wins over everything above)
-
