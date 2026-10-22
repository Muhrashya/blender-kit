# FX spec: <FX_Name>

Written by blender-vfx. This file is the contract between Blender and the game engine.
Blender cannot export its particles, simulations or geometry nodes. The engine rebuilds the effect from the assets + this recipe.

type: mesh | flipbook | trail | texture | chunks | baked
fx_style: realistic | stylized | lowpoly | voxel
trigger: loop | one-shot | on-hit
duration_s:                      fps:
style:                           palette: #hex, #hex
blend: additive | alpha | cutout | multiply
engine_profile:                  platform: pc | mobile
camera_distance: close | mid | far

## Layers (back to front; t = fraction of lifetime)
| Layer | Kind (M mesh / F flipbook / T texture / C chunks) | t start | t end | Asset | Blend |
|---|---|---|---|---|---|

## Assets
| File | Kind | Spec (size / tris / UV convention) | Audit result |
|---|---|---|---|

## Engine recipe
Fill with values the engine exposes. Anything not confirmed in engine.md is written UNVERIFIED.
- spawn (burst count / rate / lifetime):
- size over life (t -> scale):
- alpha over life (t -> alpha):
- color over life (t -> hex):
- material (unlit/lit, texture slots, UV scroll speed, dissolve threshold):
- flipbook (grid CxR, frames, play rate = frames / lifetime):
- facing: billboard | none | velocity
- sorting / layer:

## Budgets
tris: / texture KB: / max simultaneous instances: / estimated overdraw (stacked transparent screen area):

## Style audit (flipbooks)
audit_fx_style: peak_ratio= | end_energy_ratio= | soft_alpha_ratio= | colors= | pass=

## Readability test
dark background: pass/fail (screenshot) | light background: pass/fail (screenshot) | gameplay distance: pass/fail

## Open assumptions
-
