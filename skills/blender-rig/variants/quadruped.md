# Variant: quadruped / creature

| Chain | Bones |
|---|---|
| Spine | root -> pelvis -> spine_01 -> spine_02 -> spine_03 -> neck_01 -> neck_02 -> head |
| Jaw | head -> jaw |
| Tail | pelvis -> tail_01 .. tail_N (N by length: one bone per 1.5 x body segment width [START]) |
| Front leg .L/.R | spine_03 -> shoulder -> upperarm -> forearm -> paw (digits per blender-hands claw-paw) |
| Hind leg .L/.R | pelvis -> thigh -> shin -> metatarsus -> paw |
Notes: hind leg has an extra joint (hock) between shin and paw: give it joint loops like a knee. Wings or ears: chains of 2-4 bones, rings every half bone length. Bone count = sum of chains; report it against engine.md max bones.
