# Variant: mech / prop rig (rigid parts)

| Topic | Rule |
|---|---|
| Method | one bone per moving part, weights 1.0 (or parent the part to the bone) |
| Pivots | bone head at the hinge or axis of rotation, measured from the mesh |
| Hierarchy | root -> body -> moving parts; follow the mechanical chain |
| Limits | note rotation limits in state.md Decisions for animate |
| Soft parts (cables, cloth) | separate chain with soft weights, or vertex animation is NOT assumed (engine.md VFX/Rig rows) |
| Tris | no joint loops needed; parts overlap with small gaps allowed |
