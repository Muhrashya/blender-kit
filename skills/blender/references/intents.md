# Intent table (classify EVERY message; first matching row wins unless noted)

Contents: 1 table | 2 interrupt protocol | 3 examples

## 1. Table
| # | Signals (any language: English, Indonesian) | Intent | Skill | Interrupts a running stage? |
|---|---|---|---|---|
| 1 | image attached, "like this", "from this picture", "dari gambar", "sesuai referensi" | reference analysis | blender-ref | yes if asset not started |
| 2 | hand, finger, thumb, glove, paw, claw, tangan, jari, sarung tangan | hands | blender-hands | yes |
| 3 | fix topology, repair, clean up mesh, bad flow, ngon, pole, uneven, rapikan, perbaiki topologi, bersihkan mesh | fix topology | blender-topology-fix | yes |
| 4 | topology, edge flow, loops, quads, triangles, polycount, tris, budget, reduce, lower poly, kurangi | topology rules | blender-topology | yes |
| 5 | retopo, high poly to low poly, sculpt, AI mesh messy, remesh, quadriflow | retopology | blender-retopo | yes |
| 6 | UV, unwrap, seam, texel, bake, normal map, AO, texture stretched | UV and bake | blender-uv-bake | yes |
| 7 | material, color, metal, glow, emission, transparent, PBR, palette | material | blender-material | yes |
| 8 | rig, bone, armature, skin, weights, IK, deform, mesh tears when bent, pinch | rigging | blender-rig | yes |
| 9 | animate, animation, walk, run, idle, attack, loop, clip, keyframe, NLA | animation | blender-animate | yes |
| 10 | effect, VFX, slash, explosion, smoke, fire, aura, shockwave, beam, trail, particle, hit, magic, efek | VFX | blender-vfx | yes |
| 10b | camera, shot, shot list, cinematic, dolly, pan, tilt, tracking shot, zoom, whip pan, crane, turntable, trailer, kamera, sinematik, sudut kamera | cinematic camera | blender-camera | yes |
| 11 | export, FBX, GLB, glTF, import into Roblox/Unity/Unreal/Godot, scale wrong, rotated 90, ekspor | export | blender-export | yes |
| 12 | check, audit, ready?, ship?, review, QA, cek | QA | blender-qa | yes |
| 13 | model, build, make, create, buat, bikin (new asset) | modeling | blender-model | no (new asset) |
| 14 | why, kenapa, wrong, looks weird, dark, black, flipped, missing, error, bug, not working, what is, apa itu, how do I, bagaimana | diagnose / concept | blender-diagnose | yes |
| 15 | install, setup, connect MCP, engine profile, config | setup | blender-setup | yes |
| 16 | anything not about Blender or 3D assets | outside | none (answer normally) | n/a |
| 17 | waive, skip this check, ignore the warning, lewati, abaikan | waiver | router (ground-rules.md section 10) | no |
Camera words alone (for example a phone camera question) are not Blender: row 10b applies only inside a Blender session or when a 3D scene, asset or render is mentioned.
Priority when several rows match: 2 > 3 > 5 > 8 > 4 > 14 (a specific object or action beats a general question).

## 2. Interrupt protocol
1. Print `INTENT: <intent> -> <skill>`.
2. state.md: push `current_stage` onto `paused`.
3. Load the skill; do its Steps for the question only.
4. If the side work changed the mesh, rig, UV or material: mark later stages STALE (routes.md section 3).
5. Print `BACK TO: <stage>` (pop `paused`). If the answer changes the plan, say so in one line and update `chain`.
6. Row 16: answer normally. state.md untouched.

## 3. Examples
| Message during stage `blender-rig` | Classified as | What happens |
|---|---|---|
| "kenapa siku karakter gepeng saat ditekuk?" | row 8/14 -> blender-diagnose (symptom: volume loss at elbow) | checks loops at elbow with audit_topology (joints), routes to topology-fix if loops missing, then BACK TO rig |
| "berapa tris ideal untuk tangan?" | row 2 -> blender-hands | answers from the hand budget table, BACK TO rig |
| "gimana bikin dolly zoom buat trailer?" | row 10b -> blender-camera | picks the dolly zoom recipe, computes the lens/distance keys, BACK TO <stage> |
| "export ke Roblox gimana?" | row 11 -> blender-export | reads engine.md, lists UNVERIFIED items, BACK TO rig |
| "resep nasi goreng?" | row 16 | normal answer, no skill, state untouched |
