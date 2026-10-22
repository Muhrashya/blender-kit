# Routes (mode -> stage chain) and invalidation

Contents: 1 chains | 2 stage gates | 3 invalidation | 4 failure routing | 5 skip rules

## 1. Chains
| Mode | Chain (in order) |
|---|---|
| prop | ref? -> model -> topology -> uv-bake -> material -> qa -> export |
| env | ref? -> model(env-kit) -> topology -> uv-bake -> material -> qa -> export |
| char | ref? -> model(character) -> hands -> retopo? -> topology -> uv-bake -> material -> rig -> animate? -> qa -> export |
| hands | ref? -> hands -> topology -> qa |
| match | ref -> (chain of the object class found in ref-analysis.md) |
| retopo | retopo -> topology -> uv-bake -> qa |
| fix | topology-fix -> topology -> qa |
| rig | topology (rig-ready check) -> rig -> qa |
| anim | animate -> qa -> export |
| fx | vfx -> (vfx-texture / vfx-mesh / vfx-sim -> vfx-flipbook) -> qa -> export (optional showcase shot: camera) |
| cam | camera -> qa -> export (only if engine.md Camera rows allow; else deliver renders) |
| optimize | topology-fix -> topology -> qa |
| export | qa -> export |
| audit | topology -> qa |
`?` = only when the brief asks for it. `retopo?` = only when the source is a sculpt or an AI-generated mesh.

## 2. Stage gates (a stage PASSES only when)
| Stage | Gate (all required) |
|---|---|
| ref | ref-analysis.md complete; no critical unknown left |
| model | silhouette matches ref (screenshots front+side); objects named; transforms applied; tris <= 1.5 x budget |
| topology | audit_mesh pass; audit_topology: ngons 0; poles not near joints; tris <= budget |
| topology-fix | audit_topology counts at or below thresholds in blender-topology-fix; before/after numbers reported |
| retopo | audit pass; silhouette HP vs LP match; HP kept |
| hands | per-hand tris within the hand budget; ring continuity true; joint loops present |
| uv-bake | has_uv; texel density within tolerance; bake verified by screenshot |
| material | only exportable PBR; names MAT_/T_ |
| rig | audit_rig pass; 3 test poses per joint without artifacts (screenshots) |
| animate | audit_anim pass; loop clips closed |
| vfx-* | their own audit pass; flipbooks also audit_fx_style; FX spec complete |
| camera | audit_camera pass for every shot; shot list complete; screenshots saved |
| qa | verdict SHIP |
| export | file exists and non-empty; export report written |

## 3. Invalidation (a change at stage S marks these STALE)
| Changed | Stages that become STALE |
|---|---|
| model, retopo, topology-fix, topology (mesh edited) | uv-bake, material, hands, rig, animate, qa, export |
| uv-bake (UV edited) | material, qa, export |
| material | qa, export |
| rig (bones, weights) | animate, qa, export |
| animate | qa, export |
| vfx-* | qa, export |
| camera (shots or subject moved) | qa, export |
STALE stage = run its audit again before continuing. Do not redo the whole stage unless the audit fails.

## 4. Failure routing
| Failing check | Go to |
|---|---|
| ngons, thin or non-planar quads, poles near joints, missing joint loops | blender-topology-fix |
| topology-fix defect rate above its escalation threshold | blender-retopo |
| rig deformation artifacts | blender-diagnose -> topology-fix -> rig |
| bake artifacts, stretched textures | blender-uv-bake |
| wrong scale/axis in engine | blender-export (import test), then blender-diagnose |
| camera audit fails (framing, horizon, clip planes) | blender-camera |
| flipbook style audit fails | blender-vfx (style fixes), then the sub-skill |
| unknown symptom | blender-diagnose |

## 5. Skip rules (adaptive chain; every skip is a Decision labeled [ASSUMED], reversible by the user)
| Condition | Skip or shorten |
|---|---|
| no reference image | skip ref |
| static asset (no deforming, no animation) | skip rig and animate; topology uses static rules |
| source is not a sculpt, scan or AI mesh | skip retopo |
| style voxel or lowpoly with palette | uv-bake takes the short palette path |
| character with blocky hands (voxel) | blender-hands blocky variant |
| FX type texture or mesh only | skip flipbook and sim |
| camera-only request | skip every asset stage |
| quick path: role prop-small AND style voxel or lowpoly AND balanced or flex rigor | model -> topology -> uv-bake (palette) + material in one turn -> qa -> export |
