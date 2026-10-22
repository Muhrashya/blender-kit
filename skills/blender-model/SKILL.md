---
name: blender-model
description: Use when building a 3D asset from the brief - blockout, proportions, silhouette, props, hard-surface objects, modular environment pieces, characters, creatures. Builds to real size with clean transforms and the right primitives so topology work stays small.
---
# Model (blockout -> clean base mesh)

## Requires
`blender-out/<asset>/brief.md` (budget, style, engine). ref-analysis.md when a reference exists. state.md.

## Inputs
Asset class (prop / hard-surface / env-kit / character / creature) -> read ONE file from `variants/`.

## Steps
1. SCENE: units metric, unit_scale 1.0 (check with scene_info.py). Collection `COL_<Asset>`. Object names per config.md.
2. REFERENCE: if a reference exists, set it up with `references/reference-setup.md` (ortho cameras + image empties).
3. BLOCKOUT: primitives at real dimensions from the brief [USER]/[ASSUMED]. One object per rigid part. Apply scale and rotation after every resize (recipe R1 in docs/blender/reference/bpy-recipes.md).
3b. OPTIONS (no reference, open look; balanced or flex rigor): build 3 quick blockouts with different proportions or silhouettes, screenshot them side by side, ask the user to pick one (1 question). Strict rigor: ask the usual questions instead.
4. SILHOUETTE: render front and side screenshots in ortho; compare with the reference overlay; fix the largest mismatch first (T1 forms), then T2.
5. BASE MESH: follow the variant file for the class. Symmetric assets: model one half + Mirror modifier (keep the modifier until blender-topology).
6. DETAIL PLAN: write which T3 details become texture/normal map (list in state.md Decisions).
7. CLEAN: no booleans left unapplied; no interior faces; origin at the placement point from the variant file.
8. AUDIT: run `audit_mesh.py` with BUDGET = 1.5 x budget at this stage (final budget is enforced in blender-topology).
9. SCREENS: front, side, 3/4 in `blender-out/<asset>/screens/`.

## Hard rules
| Rule | Detail |
|---|---|
| Real size | Dimensions come from [USER] or are labeled [ASSUMED]; never "looks about right" |
| Primitives first | Start from the simplest primitive that has the right silhouette; do not subdivide to get shape |
| No subdivision for volume | Subdivision modifiers are not allowed on the exported mesh |
| Transforms applied | scale 1, rotation 0 before any later stage |
| Characters | A-pose or the pose engine.md requires; slight elbow/knee bend (5-10 degrees); symmetric |
| Separate what moves | Parts that move independently are separate objects (or separate vertex groups with rigid weights) |

## Done when
audit_mesh: no ngons, no doubles, transforms applied, tris <= 1.5 x budget; silhouette screenshots match the reference (or brief); state.md Decisions list T3 details.

## On fail
| Failure | Action |
|---|---|
| tris > 1.5 x budget at blockout | remove detail, not segments; reread variant file |
| silhouette mismatch | fix the largest T1 form; re-screenshot |
| hands needed for a character | run blender-hands before topology |
| sculpt-based source | blender-retopo |

## Next
blender-topology (then uv-bake). Characters: blender-hands first.
