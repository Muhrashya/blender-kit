# Effect types

Contents: 1 classification | 2 timing | 3 effect recipes | 4 what never ships

Style (realistic, stylized, low-poly game-like, voxel) is defined in `docs/blender/reference/vfx-styles.md`; full per-effect recipes are in `cookbook.md`.

## 1. Classification
| Type | Good for | Method in Blender | Delivered | Skill |
|---|---|---|---|---|
| Texture (D) | masks, noise, ramps, glow shapes | procedural or painted, baked to PNG | PNG 128-256 | blender-vfx-texture |
| Mesh (B) | slash, shockwave ring, beam, dome, aura, vortex | low-poly shape + UVs for scrolling | FBX/GLB + mask | blender-vfx-mesh |
| Flipbook (A) | smoke, fire, explosion, dust, magic burst | render frames, pack sheet | PNG sheet | blender-vfx-flipbook |
| Trail (C) | sword or projectile tail | strip texture (+ strip mesh) | texture + recipe | blender-vfx-texture |
| Chunks (F) | breakable props, debris | cell fracture or manual pieces | FBX pieces + pivots | blender-vfx-sim |
| Baked motion (E) | cloth, fluid-like motion | simulation baked to textures | only if engine.md VFX row says VAT supported | blender-vfx-sim |
Order of cost: D + B, then A, C, F, E.

## 2. Timing [START]
| Effect | Seconds |
|---|---|
| Hit / impact | 0.15-0.4 |
| Slash | 0.2-0.5 |
| Explosion | 0.5-1.5 |
| Magic cast | 0.6-2 |
| Ambient loop | 2-4 |
Life curve: build 10-20 percent -> peak 20-30 percent -> fade 50-70 percent.

## 3. Effect recipes (engine-agnostic outline)
| Effect | Type | Assets | Recipe highlights |
|---|---|---|---|
| Slash | mesh | curved strip (about 32 tris) + streak mask | UV scroll along length, scale up, fade out, additive |
| Shockwave | mesh | annulus (about 64 tris) + ring mask | scale 0 -> max, alpha fade, additive |
| Beam | mesh | open tube 8 sides (no caps) + gradient mask | UV scroll, width pulse |
| Smoke puff | flipbook | 4x4 or 6x6 sheet, grayscale + alpha | tint in engine, alpha blend |
| Explosion | flipbook + mesh | sheet + shockwave ring | stagger: flash, fireball, smoke |
| Aura | mesh | scaled copy shell + noise mask | scroll noise, fresnel-like fade if the engine supports it |
| Shield dome | mesh | hemisphere (about 100 tris) + hex mask | hit ripple by dissolve/scroll |
| Debris | chunks | pieces <= 100 tris each | physics in engine |

## 4. What never ships
Blender particle systems, fluid/smoke/rigid-body simulation domains, geometry-nodes setups, procedural shader nodes. Bake them to textures, meshes, or sprite sheets and describe the rebuild in the FX spec.
