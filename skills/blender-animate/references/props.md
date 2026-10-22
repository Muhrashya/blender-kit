# Prop animations [START]

| Clip | Frames (30 fps) | Notes |
|---|---|---|
| Door / chest open | 15-30 | rigid parts on a hinge bone; ease in and out; overshoot 2-3 degrees then settle |
| Lever / button press | 6-12 | return clip separate |
| Pickup float loop | 60-90 | sine up/down, slow rotation, closed loop |
| Destroy (chunks) | see blender-vfx-sim | chunk transforms baked at the project fps |
Rule: each prop clip starts and ends in a named rest state recorded in state.md.
