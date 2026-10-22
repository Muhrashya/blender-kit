# Variant: character (humanoid)

| Topic | Rule |
|---|---|
| Pose | A-pose (arms about 40-45 degrees down) unless engine.md demands T-pose; knees and elbows slightly bent (5-10 degrees) to fix bend direction |
| Symmetry | model one half, mirror; keep the center line vertices on x = 0 |
| Parts | head, torso, arms, hands, legs, feet; hands via blender-hands |
| Clothes | separate objects only if the engine/brief needs swapping; otherwise merge after weights |
| Proportion source | ref-analysis section 4 ratios; no ref: default heads-tall from brief [USER] |
| Budget split [START] | head 20-25 percent, torso 25, arms 15-20, hands 10-15, legs 20-25 |
| Hidden surfaces | delete inside mouth/eyes (unless needed), under clothing when clothing is separate |
| Pitfalls | no loops at joints (fix later is costly), pole at shoulder/elbow, fingers merged |
| Next | hands -> topology (deformation-zones.md) -> uv-bake -> material -> rig |
