---
engine: unity
version: UNVERIFIED
source: https://docs.unity3d.com/Manual/index.html
verified: never
status: SEED
---
# Engine profile: Unity (SEED: verify with `/blender-setup engine unity`)

## Import
| Item | Value | Label |
|---|---|---|
| Preferred mesh format | FBX | [RECALLED] |
| Other accepted formats | OBJ, glTF via package | [RECALLED] |
| Import path | drop file into Assets | [RECALLED] |

## Coordinates and scale
| Item | Value | Label |
|---|---|---|
| Up axis | +Y | [RECALLED] |
| Forward axis | +Z | [RECALLED] |
| Handedness | left-handed | [RECALLED] |
| 1 unit = | 1 meter | [RECALLED] |
| Blender export setting | apply_scale_options FBX_SCALE_ALL, axis_forward -Z, axis_up Y; test with a 1 m cube | [RECALLED] verify by import test |

## Limits
| Item | Value | Label |
|---|---|---|
| Max triangles per mesh | UNVERIFIED (vertex index format limits exist; check docs) | UNVERIFIED |
| Max bones per skeleton | UNVERIFIED | UNVERIFIED |
| Max bone influences per vertex | quality setting (1, 2, 4 recalled) | [RECALLED] confirm |
| Max texture size | UNVERIFIED | UNVERIFIED |
| Max materials per mesh | UNVERIFIED | UNVERIFIED |

## Mesh rules
| Item | Value | Label |
|---|---|---|
| Triangulate on export | importer triangulates | [RECALLED] |
| Custom normals | import option Normals: Import | [RECALLED] |
| Collision | add collider components; or colliders from mesh | [RECALLED] |
| LOD | LOD Group component; suffix _LOD0, _LOD1 may auto-build groups | [RECALLED] confirm |
| Pivot | object origin | [RECALLED] |

## Naming
UNVERIFIED beyond LOD suffix above.

## Rig
| Item | Value | Label |
|---|---|---|
| Required skeleton type | Humanoid (mapped avatar) or Generic | [RECALLED] |
| Bone naming | Humanoid avatars are mapped; clear names help auto-map | [RECALLED] |
| Root bone | single root recommended | [ASSUMED] |
| Deform-only export | `add_leaf_bones=False`, only deform bones | [RECALLED] |

## Animation
| Item | Value | Label |
|---|---|---|
| Frame rate | clip sample rate set at import | [RECALLED] |
| Clip source | actions baked to FBX takes | [RECALLED] |
| Loop flag | Loop Time on the imported clip | [RECALLED] |
| Root motion | Root Transform options on import | [RECALLED] |

## Materials
| Item | Value | Label |
|---|---|---|
| Workflow | metallic-smoothness in Standard/URP/HDRP (smoothness = 1 - roughness) | [RECALLED] confirm |
| Channel packing | metallic R, smoothness A in the metallic-smoothness map | [RECALLED] confirm |
| Normal map | OpenGL (+Y) | [RECALLED] |
| Color spaces | base color sRGB; data maps linear | [RECALLED] |
| Vertex color | supported with shaders that read it | [RECALLED] |
| Transparency | per-material surface type | [RECALLED] |

## VFX
| Item | Value | Label |
|---|---|---|
| Particle system | Particle System (Shuriken) / VFX Graph | [RECALLED] |
| Flipbook support | Texture Sheet Animation module | [RECALLED] |
| Blend modes | additive / alpha / multiply via shader | [RECALLED] |
| Mesh particles / trails | mesh renderer in particle system; Trail Renderer | [RECALLED] |
| UV scroll / dissolve | via Shader Graph | [RECALLED] |
| Vertex animation textures | possible via custom shader | [RECALLED] |
| Max simultaneous particles | per system setting | [RECALLED] |

## Camera
| Item | Value | Label |
|---|---|---|
| Camera animation import | FBX camera import: UNVERIFIED; camera paths are usually rebuilt | UNVERIFIED |
| In-engine cinematic tool | Timeline + Cinemachine | [RECALLED] |
| FOV convention (vertical or horizontal) | vertical FOV (physical camera mode uses sensor size and focal length) | [RECALLED] confirm |
| Sensor / physical camera | physical camera sensor size and focal length | [RECALLED] |
| Depth of field | post-processing volume | [RECALLED] |
| Motion blur | post-processing volume | [RECALLED] |

## Export call
```python
# bpy.ops.export_scene.fbx(use_selection=True, apply_scale_options='FBX_SCALE_ALL', axis_forward='-Z', axis_up='Y',
#                          object_types={'MESH','ARMATURE'}, add_leaf_bones=False, mesh_smooth_type='FACE')
```

## Import test
1. 1 m cube: scale = 1, no unexpected rotation.
2. Asset: materials, normals, pivot, collider.
3. Rig: Humanoid mapping succeeds or Generic plays clips.
4. Record in docs/blender/assets.md.
