---
engine: roblox
version: UNVERIFIED
source: https://create.roblox.com/docs
verified: never
status: SEED
---
# Engine profile: Roblox (SEED: run `/blender-setup engine roblox` to verify against the official docs)

Everything marked [RECALLED] must be confirmed before you claim compliance.

## Import
| Item | Value | Label |
|---|---|---|
| Preferred mesh format | FBX | [RECALLED] |
| Other accepted formats | OBJ; glTF may be supported in recent versions | [RECALLED] confirm |
| Import path / tool | Studio 3D Importer / Asset Manager | [RECALLED] |

## Coordinates and scale
| Item | Value | Label |
|---|---|---|
| Up axis | +Y | [RECALLED] |
| Forward axis | UNVERIFIED | UNVERIFIED |
| 1 engine unit = | 1 stud, about 0.28 m | [RECALLED] |
| Blender export setting | UNVERIFIED; test with a 1 m cube import | UNVERIFIED |

## Limits
| Item | Value | Label |
|---|---|---|
| Max triangles per mesh | 21,844 per MeshPart | [RECALLED] confirm |
| Max bones per skeleton | UNVERIFIED | UNVERIFIED |
| Max bone influences per vertex | UNVERIFIED | UNVERIFIED |
| Max texture size | UNVERIFIED (1024 recalled for some texture types) | [RECALLED] confirm |
| Max materials per mesh | UNVERIFIED | UNVERIFIED |

## Mesh rules
| Item | Value | Label |
|---|---|---|
| Triangulate on export | importer triangulates; keep source quads | [ASSUMED] |
| Custom normals | UNVERIFIED | UNVERIFIED |
| Collision | per-part collision fidelity setting in Studio | [RECALLED] |
| LOD | engine-side LOD distances exist | [RECALLED] confirm |
| Pivot | UNVERIFIED | UNVERIFIED |

## Naming
UNVERIFIED. Do not invent naming hints; read the official import docs.

## Rig
| Item | Value | Label |
|---|---|---|
| Required skeleton type | R15 / R6 for avatars; custom rigs for other models | [RECALLED] |
| Bone naming | R15 body part names (e.g. UpperTorso, LowerTorso, LeftUpperArm, RightFoot) | [RECALLED] confirm |
| Root bone | UNVERIFIED | UNVERIFIED |
| Deform-only export | UNVERIFIED | UNVERIFIED |

## Animation
| Item | Value | Label |
|---|---|---|
| Frame rate | UNVERIFIED | UNVERIFIED |
| Clip source | animation editor / import UNVERIFIED | UNVERIFIED |
| Loop flag | set in Studio animation properties | [RECALLED] |
| Root motion | UNVERIFIED | UNVERIFIED |

## Materials
| Item | Value | Label |
|---|---|---|
| Workflow | PBR via SurfaceAppearance (color, normal, metalness, roughness) | [RECALLED] confirm |
| Channel packing | UNVERIFIED | UNVERIFIED |
| Normal map | UNVERIFIED (check green-channel convention in docs) | UNVERIFIED |
| Color spaces | UNVERIFIED | UNVERIFIED |
| Vertex color | UNVERIFIED | UNVERIFIED |
| Transparency | UNVERIFIED | UNVERIFIED |

## VFX
| Item | Value | Label |
|---|---|---|
| Particle system | ParticleEmitter | [RECALLED] |
| Flipbook support | ParticleEmitter flipbook layouts 2x2, 4x4, 8x8 | [RECALLED] confirm |
| Blend modes | LightEmission property for additive-like look | [RECALLED] confirm |
| Mesh particles / trails / beams | Trail and Beam objects exist; mesh as part | [RECALLED] |
| UV scroll / dissolve in materials | UNVERIFIED (custom shaders not available recalled) | UNVERIFIED |
| Vertex animation textures | UNVERIFIED; assume NO and use flipbook | [ASSUMED] |
| Max simultaneous particles | UNVERIFIED | UNVERIFIED |

## Camera
| Item | Value | Label |
|---|---|---|
| Camera animation import | no camera animation import recalled; cameras are driven by scripts | [RECALLED] confirm |
| In-engine cinematic tool | scripted Camera CFrame / FieldOfView tweening, or Studio cinematic tools | [RECALLED] confirm |
| FOV convention (vertical or horizontal) | vertical FieldOfView (default 70) | [RECALLED] confirm |
| Sensor / physical camera | n/a | UNVERIFIED |
| Depth of field | UNVERIFIED | UNVERIFIED |
| Motion blur | UNVERIFIED | UNVERIFIED |

## Export call
```python
# FBX example (test with a 1 m cube first):
# bpy.ops.export_scene.fbx(use_selection=True, apply_scale_options='FBX_SCALE_ALL', axis_forward='-Z', axis_up='Y',
#                          object_types={'MESH','ARMATURE'}, add_leaf_bones=False, mesh_smooth_type='FACE')
```

## Import test
1. Import a 1 m cube: measure it in Studio and write down the real scale factor here [MEASURED by user].
2. Import the asset: orientation, scale, textures, collision.
3. For rigs: play one clip.
4. Record in docs/blender/assets.md.
