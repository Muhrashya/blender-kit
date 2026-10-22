# Weights and tests

Contents: 1 auto weights | 2 cleanup | 3 mirror | 4 test poses | 5 artifacts

## 1. Auto weights
Select the mesh(es), then the armature (active), run parent with automatic weights. Check heat-weight failures: audit_rig `unweighted_verts` > 0 means bones outside the volume or non-manifold mesh.

## 2. Cleanup order
| Step | Action |
|---|---|
| 1 | remove weights below 0.001 and clean empty groups |
| 2 | limit total influences to the engine value (operator `bpy.ops.object.vertex_group_limit_total` with `limit` = value; if the poll fails, print the error and report, do not guess a mode) |
| 3 | normalize all (`bpy.ops.object.vertex_group_normalize_all`) |
| 4 | smooth only the joint zones, not whole limbs |
| 5 | hands: apply the ramp table from hand-topology.md section 8 |
| 6 | rigid parts: set 1.0 on one bone |

## 3. Mirror
Only when the mesh is symmetric (`audit_topology.py` SYMMETRIC unmatched = 0). Mirror vertex groups from the cleaner side using the `.L`/`.R` names; re-run normalize and audit_rig.

## 4. Test poses (screenshot each, front and bend side)
| Joint | Pose 1 | Pose 2 | Pose 3 |
|---|---|---|---|
| Shoulder | arm up 90 degrees | arm forward 90 degrees | arm across chest |
| Elbow | 90 degrees | full bend (about 140) | straight |
| Wrist | 45 up | 45 down | twist 90 around the forearm |
| Fingers | 90 curl | fist | full spread |
| Hip | leg forward 90 | leg side 45 | leg back 30 |
| Knee | 90 | full bend (about 130) | straight |
| Ankle | toes up 30 | toes down 45 | roll 20 |
| Neck/head | look 60 left | nod 40 down | tilt 30 |
| Spine | bend forward 30 | twist 30 | lean side 20 |
Pass: no vertex spikes, no self-intersection beyond the style, no volume collapse worse than the style allows.

## 5. Artifacts
| Artifact | Likely cause | Fix |
|---|---|---|
| Spiky vertices | unweighted or wrong weights | weights, normalize |
| Volume loss at elbow/knee | few loops | topology-fix joint loops |
| Candy wrapper | twist concentrated at the wrist | twist bones |
| Shoulder collapse | one loop around the shoulder | more shoulder rings (deformation-zones.md) |
| Bleed between fingers | cross-finger weights | finger isolation |
