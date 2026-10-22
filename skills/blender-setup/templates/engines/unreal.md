---
engine: unreal
version: UNVERIFIED
source: https://dev.epicgames.com/documentation/en-us/unreal-engine
verified: never
status: SEED
---
# Engine profile: Unreal Engine (SEED: verify with `/blender-setup engine unreal`)

## Import
| Item | Value | Label |
|---|---|---|
| Preferred mesh format | FBX | [RECALLED] |
| Other accepted formats | glTF via Interchange / plugins | [RECALLED] confirm |
| Import path | Content Browser import | [RECALLED] |

## Coordinates and scale
| Item | Value | Label |
|---|---|---|
| Up axis | +Z | [RECALLED] |
| Forward axis | +X | [RECALLED] |
| Handedness | left-handed | [RECALLED] |
| 1 unit = | 1 centimeter | [RECALLED] |
| Blender export setting | UNVERIFIED; Blender 1 unit = 1 m becomes 100 UE units only with correct FBX scale; test with a 1 m cube | UNVERIFIED |

## Limits
| Item | Value | Label |
|---|---|---|
| Max triangles per mesh | UNVERIFIED | UNVERIFIED |
| Max bones | UNVERIFIED | UNVERIFIED |
| Max influences per vertex | UNVERIFIED (4 and 8 recalled) | [RECALLED] confirm |
| Max texture size | UNVERIFIED | UNVERIFIED |
| Max materials per mesh | UNVERIFIED | UNVERIFIED |

## Mesh rules
| Item | Value | Label |
|---|---|---|
| Triangulate on export | importer triangulates | [RECALLED] |
| Custom normals | supported | [RECALLED] |
| Collision | FBX prefixes UCX_, UBX_, USP_, UCP_ + mesh name | [RECALLED] confirm |
| LOD | _LOD0, _LOD1 suffix on meshes in one FBX | [RECALLED] confirm |
| Pivot | object origin | [RECALLED] |

## Naming
Collision prefixes as above. Sockets: UNVERIFIED naming. Do not invent others.

## Rig
| Item | Value | Label |
|---|---|---|
| Required skeleton type | any; UE5 mannequin retarget is optional | [RECALLED] |
| Bone naming | free; retargeting maps chains | [RECALLED] |
| Root bone | single root recommended | [ASSUMED] |
| Deform-only export | `add_leaf_bones=False` | [RECALLED] |

## Animation
| Item | Value | Label |
|---|---|---|
| Frame rate | UNVERIFIED | UNVERIFIED |
| Clip source | one action per FBX or baked takes | [RECALLED] |
| Loop flag | set on the animation asset | [RECALLED] |
| Root motion | Enable Root Motion on the sequence | [RECALLED] |

## Materials
| Item | Value | Label |
|---|---|---|
| Workflow | metallic-roughness | [RECALLED] |
| Channel packing | commonly ORM: occlusion R, roughness G, metallic B | [RECALLED] confirm |
| Normal map | DirectX (-Y, green down): flip green when baking for UE | [RECALLED] confirm |
| Color spaces | base color sRGB; data maps linear | [RECALLED] |
| Vertex color | supported | [RECALLED] |
| Transparency | blend modes in material | [RECALLED] |

## VFX
| Item | Value | Label |
|---|---|---|
| Particle system | Niagara | [RECALLED] |
| Flipbook support | SubUV in sprite renderer | [RECALLED] |
| Blend modes | additive / translucent in material | [RECALLED] |
| Mesh particles / trails / ribbons | supported in Niagara | [RECALLED] |
| UV scroll / dissolve | material nodes | [RECALLED] |
| Vertex animation textures | supported via material setup | [RECALLED] |
| Max simultaneous particles | per emitter setting | [RECALLED] |

## Camera
| Item | Value | Label |
|---|---|---|
| Camera animation import | FBX camera animation import into Sequencer | [RECALLED] confirm |
| In-engine cinematic tool | Sequencer + Cine Camera Actor | [RECALLED] |
| FOV convention (vertical or horizontal) | horizontal FOV for regular cameras; Cine Camera uses filmback and focal length | [RECALLED] confirm |
| Sensor / physical camera | filmback / sensor settings | [RECALLED] |
| Depth of field | post-process settings | [RECALLED] |
| Motion blur | post-process settings | [RECALLED] |

## Export call
```python
# bpy.ops.export_scene.fbx(use_selection=True, apply_scale_options='FBX_SCALE_ALL', axis_forward='-Z', axis_up='Y',
#                          object_types={'MESH','ARMATURE'}, add_leaf_bones=False, mesh_smooth_type='FACE')
```

## Import test
1. 1 m cube must measure 100 cm.
2. Collision and LOD naming recognized.
3. Normal map shading correct (green channel).
4. Record in docs/blender/assets.md.
