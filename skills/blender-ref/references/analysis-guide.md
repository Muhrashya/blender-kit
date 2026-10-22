# Analysis guide (how to fill ref-analysis.md without inventing)

Contents: 1 views | 2 proportions | 3 silhouette tiers | 4 parts | 5 colors | 6 hidden sides | 7 object classes

## 1. Views
| View | What it gives | Limit |
|---|---|---|
| Orthographic front/side | reliable proportions | none |
| Perspective 3/4 | shape, volume | distorts ratios; label [ESTIMATED] |
| Photo | materials, wear | perspective + lighting; no exact edges |

## 2. Proportions (ratios to total height = 1.0)
1. Take the subject bbox from measure_ref.py: height_px = bbox.h.
2. For each part, measure its pixel box inside the subject; ratio = part_px / height_px. Mark [ESTIMATED] (measured by eye) unless computed by script.
3. Write width, height, and bottom-offset ratios. Round to 0.01.

## 3. Silhouette tiers
| Tier | Content | Goes to |
|---|---|---|
| T1 | largest forms that define the outline | geometry first |
| T2 | medium forms (straps, pockets, handles) | geometry if the budget allows |
| T3 | small detail (screws, stitches, engraving) | texture or normal map by default |

## 4. Parts
List parts that move separately (doors, hands, weapon, cape). Each becomes a separate mesh or a rig element. Parts that never move stay one mesh.

## 5. Colors
Palette from measure_ref.py -> use as the palette texture entries. Other regions: write a hex guess and mark [ESTIMATED].

## 6. Hidden sides
| Situation | Rule |
|---|---|
| Back of a prop | mirror or extrude the front silhouette; [ASSUMED] |
| Underside | flat; [ASSUMED] |
| Character back | follow front proportions, simple; [ASSUMED] |
| Hands not visible | default to relaxed hand from blender-hands; [ASSUMED] |
Ask the user only when the hidden part is large (more than a quarter of the object) or changes how it works.

## 7. Object classes
| Class | Next skill detail |
|---|---|
| prop, hard-surface | blender-model variants/prop.md or hard-surface.md |
| environment piece | variants/env-kit.md |
| humanoid | variants/character.md + blender-hands |
| animal, monster | variants/creature.md |
| effect | blender-vfx |
