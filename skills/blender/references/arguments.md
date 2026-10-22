# Argument grammar and defaults

| Argument | Values | Default | Notes |
|---|---|---|---|
| mode | prop char hands env match rig anim fx cam retopo fix optimize export audit ask doctor | classify from text | first token |
| "<what>" | free text in quotes | required for new asset | becomes the asset name (PascalCase) |
| ref= | path to image(s), comma separated | none | triggers blender-ref first |
| role= | row name from config.md Triangle budgets | ask or classify [ASSUMED] | picks the budget row |
| tris= | integer | from role | overrides the budget; label [USER] |
| style= | voxel lowpoly stylized realistic | config.md style | |
| rigor= | strict balanced flex | config.md rigor | how rigid the workflow is |
| fx= | realistic stylized lowpoly voxel | config.md fx_style | VFX style for this effect |
| engine= | profile name in docs/blender/engines/ | config.md engine | |
| platform= | pc mobile | config.md platform | mobile = Mobile column |
| anim= | clip names, comma separated | none | animate stage |
| rig | flag | no | adds rig + animate stages to prop/char |
| shots= | integer | 1 | number of shots for mode cam |
| run all | phrase | no | run chain until first FAIL |

Examples:
- `/blender prop "WoodCrate" ref=crate.png role=prop-small style=lowpoly`
- `/blender char "Knight" role=char-npc rig anim=idle,walk`
- `/blender hands "KnightHand" style=stylized`
- `/blender fix` (operates on the selected mesh in Blender)
- `/blender fx "CyanSlash" fx=lowpoly`
- `/blender cam "HeroReveal" shots=3`
