# Examples: how the skills link

Contents: 1 prop from a reference | 2 character with a mid-flow question | 3 fix topology on an existing mesh | 4 effect | 5 same effect, two styles | 6 cinematic camera | 7 flexible run with a waiver

## 1. Prop from a reference
`/blender prop "WoodCrate" ref=crate.png role=prop-small style=lowpoly`
| Turn | Router action | Skill | Report highlights |
|---|---|---|---|
| 1 | pre-flight, brief.md, state.md (chain: ref -> model -> topology -> uv-bake -> material -> qa -> export) | blender-ref | measure_ref bbox aspect 1.02 [MEASURED], back side [ASSUMED] |
| 2 | next stage | blender-model | audit_mesh tris 410 <= 1.5 x 800 |
| 3 | next | blender-topology | tris 330/800, ngons 0, hidden faces removed, PASS |
| 4 | next | blender-uv-bake (palette path) | UVs in 0-1, PASS |
| 5 | next | blender-material | Principled + image only, PASS |
| 6 | next | blender-qa | SHIP |
| 7 | next | blender-export | EXPORT_OK=True, file bytes, UNVERIFIED rows disclosed |

## 2. Character with a side question
`/blender char "Knight" role=char-npc rig anim=idle,walk style=stylized`
State: current_stage = blender-rig, topology PASS.
User asks: "kenapa siku karakter gepeng saat ditekuk?"
| Step | What happens |
|---|---|
| 1 | router prints `INTENT: diagnose -> blender-diagnose`, pushes `blender-rig` to paused |
| 2 | diagnose matches symptoms.md row D "Pinching or flattening at elbow/knee"; runs audit_topology.py with ARMATURE set: poles_near_joints = [412, 977] [MEASURED] |
| 3 | route: blender-topology-fix: checkpoint, recipe C (move poles with rotate_edges, add elbow loop with bisect_plane), re-audit: poles_near_joints = [] |
| 4 | router marks uv-bake, material, hands, rig, animate, qa, export STALE |
| 5 | `BACK TO: blender-rig` (re-audit weights, re-run 3 elbow test poses) |
Then the user asks "berapa tris ideal untuk tangan?" -> blender-hands answers from the tier table (Mid: 772-872 total, Low: 356-396), then BACK TO.
A message like "resep nasi goreng?" is answered normally; state.md is untouched.

## 3. Fix topology on an existing mesh
`/blender fix` with a messy mesh selected.
| Turn | Skill | Result |
|---|---|---|
| 1 | blender-topology-fix | before: ngons 41, tri faces near joints 63, thin quads 18; defect rate 11.4 percent -> local patch route |
| 2 | blender-topology-fix | recipes A-C done, patch rebuilt; after: ngons 0, joints clean, silhouette unchanged |
| 3 | blender-topology | audit_mesh pass; rig-ready table all yes |
| 4 | blender-qa | SHIP |
(Illustrative numbers.)

## 4. Effect
`/blender fx "CyanSlash" style=stylized`
| Turn | Skill | Result |
|---|---|---|
| 1 | blender-vfx | type mesh (cheapest); spec written; engine VFX rows labeled [RECALLED] |
| 2 | blender-vfx-texture | T_FX_CyanSlash_Mask 256x64 |
| 3 | blender-vfx-mesh | 32 tris, UV in 0-1, dark/light screenshots |
| 4 | blender-qa -> blender-export | SHIP, export report with recipe |

## 5. Same effect, two styles
`/blender fx "Explosion" fx=lowpoly` vs `/blender fx "Explosion" fx=realistic`
| Item | lowpoly | realistic |
|---|---|---|
| Recipe | cookbook "Small explosion", Low-poly column | same row, Realistic column |
| Layers | star flash, orange cutout blobs, gray puffs (3 layers) | flash, simulated fireball, shockwave, smoke, sparks (5 layers) |
| Route | vfx -> vfx-mesh + vfx-flipbook (no simulation) | vfx -> vfx-sim (realistic path) -> vfx-flipbook |
| Sheet | 8 frames, 64-128 px, stepped | 32-64 frames, 128-256 px |
| Style audit | audit_fx_style lowpoly: soft alpha <= 0.15, colors <= 8, frames 4-12 | realistic: frames 16-64 |
Both: peak at 15-45 percent of the life, last frame at most 10 percent of the peak energy.

## 6. Cinematic camera
`/blender cam "HeroReveal" shots=3`
| Shot | Move | Why (shot list Purpose) | Rig |
|---|---|---|---|
| 01 | static, wide, 24 mm | establish the arena | camera + target |
| 02 | boom up + tilt | reveal the boss's scale | camera location Z keys, Track To target moving up |
| 03 | arc + push in, 50 mm | menace on the hero | pivot rotation + camera location |
audit_camera checks subject framing at start/middle/end, horizon level (roll within 1 degree), clip planes, duration and speed. The engine recipe in the shot list states the FOV convention from engine.md Camera rows.

## 7. Flexible run with a waiver
`/blender prop "Barrel" role=prop-small style=voxel rigor=flex`
| Turn | What happens |
|---|---|
| 1 | no reference: ref skipped [ASSUMED]; router offers 3 blockout options (A/B/C screenshot); user picks B |
| 2 | quick path runs model -> topology -> uv-bake (palette) + material in one report; all PASS |
| 3 | audit_mesh shows tris 168 of 180 budget; the user says "waive the naming check, this is a prototype" |
| 4 | state.md waivers: naming (reason: prototype); QA verdict SHIP with accepted risk listed; export checks the file exists (never waivable) |
