# Variant: humanoid

Contents: 1 hierarchy | 2 counts | 3 twist and extras | 4 engine overrides

## 1. Hierarchy (Blender-style names; engine.md naming wins when it exists)
| Chain | Bones (parent -> child) |
|---|---|
| Root | root -> pelvis |
| Spine | pelvis -> spine_01 -> spine_02 -> spine_03 -> neck -> head |
| Arm .L/.R | spine_03 -> clavicle -> upperarm -> forearm -> hand |
| Fingers .L/.R | hand -> {thumb, index, middle, ring, pinky}_{01,02,03} |
| Leg .L/.R | pelvis -> thigh -> calf -> foot -> toe |

## 2. Counts [COMPUTED]
| Tier | Bones |
|---|---|
| Rigid / no fingers | 23 = root 1 + pelvis 1 + spine 3 + neck 1 + head 1 + arms 2x4 + legs 2x4 |
| Reduced fingers (2 per finger) | 43 = 23 + 2 x 5 x 2 |
| Full fingers (3 per finger) | 53 = 23 + 2 x 5 x 3 |
Check against engine.md max bones; if UNVERIFIED, state it.

## 3. Twist and extras
| Need | Solution |
|---|---|
| Forearm twist | 1-2 twist bones between forearm and hand sharing the roll (extra bone count +1 or +2 per arm) or limit roll on the hand bone; check engine.md for twist bone support |
| Shoulder volume | optional extra deform bone near the deltoid at Hero tier |
| IK | control bones in a separate non-deform collection; bake to deform bones for export |

## 4. Engine overrides
Read engine.md Rig rows: skeleton type (Humanoid mapping, R15, custom), bone names, root bone. If a row is UNVERIFIED, ask the user once, then label the choice [USER].
