# VFX cookbook

Contents: 1 how to read | 2 impacts and melee | 3 explosions and elements | 4 magic and buffs | 5 projectiles and beams | 6 environment and misc

## 1. How to read
Layers use fractions of the lifetime (t from 0 to 1). Asset kinds: M = mesh effect, F = flipbook, T = texture, C = chunks. Style columns come from `docs/blender/reference/vfx-styles.md` (Realistic | Low-poly game-like; stylized sits between them; voxel replaces curves with cubes). Every row is a starting recipe [START]; the engine recipe values still come from engine.md.
Layer stack order (back to front): glow, core, secondary shapes, sparks or debris, smoke or dust. Cap layers: pc 4-6, mobile 2-3.

## 2. Impacts and melee
| Effect | Layers (kind, t-range) | Low-poly game-like | Realistic |
|---|---|---|---|
| Hit / impact | flash M or T 0-0.15; burst ring M 0-0.4; sparks F 0.05-0.6 | star-shaped flat flash, 6-8 shard meshes flying outward, hard alpha | bright flash, spark flipbook with motion blur, short dust puff |
| Slash | arc strip M 0-0.5 (U scroll); streak T; afterimage F optional | 1 tapered strip, 2 flat colors, scale pop | strip with noise mask, thin sparks, motion blur |
| Shockwave | ring M 0-0.6 (scale up, fade); dust F 0.1-0.8 | flat annulus, hard edge, 1 color | ring with refraction-like highlight (if engine supports) + dust |
| Ground slam | crack decal T; ring M; debris C 0-1 | low-poly rock chunks (<= 10, <= 40 tris), cutout dust | cracks + 20-30 debris chunks + volumetric dust |
| Footstep dust | puff F 0-1 | 2-3 flat puff cutouts | soft dust flipbook, grayscale tinted |

## 3. Explosions and elements
| Effect | Layers | Low-poly game-like | Realistic |
|---|---|---|---|
| Small explosion | flash 0-0.1; fireball F 0-0.5; shockwave M 0-0.4; smoke F 0.3-1 | 3-layer: star flash, orange blob cutouts (6-8 frames), gray puffs | simulated fire + smoke flipbook (32-64 frames), spark particles, light flash in engine |
| Big explosion | add debris C, screen shake in engine | faceted rock shards, thick outlines | volumetric bake, debris chunks, heat haze (engine support UNVERIFIED) |
| Smoke puff / column | puffs F loop or one-shot | stacked low-poly spheres or cutout puffs | simulation, lit, tintable grayscale |
| Fire / torch | flame F loop; embers T | 3 stacked cutout flames, flicker by scale | simulated flame flipbook loop 16-32 frames |
| Lightning | jagged strip M; flash T | thick zigzag strips, 2-3 variants | thin branching strips + glow + flicker |
| Water splash | crown M; droplets F | low-poly crown shards + blue cutout drops | simulated splash flipbook |

## 4. Magic and buffs
| Effect | Layers | Low-poly game-like | Realistic |
|---|---|---|---|
| Magic cast + circle | circle T/M ground 0-1; rising particles F; burst 0.7-1 | flat glyph disc, 6-10 star sparks | layered noise glow, light shafts (engine) |
| Aura / buff | shell M (UV scroll); sparkle F loop | flat translucent low-poly shell, hard stripes | noise-scrolled shell + soft particles |
| Heal / sparkle | rising sparks F loop; ring M 0-0.5 | plus-signs and stars, hard alpha | soft glints + glow |
| Shield / barrier | dome M; hit ripple (dissolve or scroll) | hex-faceted dome, flat color | fresnel-like rim, noise distortion (engine support UNVERIFIED) |
| Portal / vortex | swirl M strips; particles F | spinning strips, 2 colors | volumetric swirl bake + glow |
| Level-up / burst | ground ring M; vertical beam M; sparks F | flat beam, star sparks | volumetric beam + particle trails |

## 5. Projectiles and beams
| Effect | Layers | Low-poly game-like | Realistic |
|---|---|---|---|
| Projectile + trail | core M; trail strip T/M; impact (see Hit) | low-poly orb or dart, flat strip trail | glowing core, noise strip trail, motion blur |
| Beam / laser | tube M (UV scroll); muzzle F; impact F | open box/tube, 2 colors | layered tubes with noise, bloom |
| Muzzle flash | star M or F 0-0.15 | 4-6 point star, flat | brief sprite flipbook, light flash (engine) |

## 6. Environment and misc
| Effect | Layers | Low-poly game-like | Realistic |
|---|---|---|---|
| Pickup / collect | ring M; sparks F; glow T | spinning ring + star pop | glow + sparkle trail |
| Death / dissolve | dissolve mask T; fragments C; smoke F | low-poly shards, dissolve threshold in engine | noise dissolve + ash/ember particles |
| Dust / debris ambience | motes F loop | few flat motes | soft motes with depth |
| Spawn / teleport | ring M; beam M; sparks F | flat beam + ring | volumetric beam + particles |
No match for the request: build from the closest row, say which, and write the layers in the FX spec.
