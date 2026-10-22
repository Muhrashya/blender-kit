---
engine: web-three
version: UNVERIFIED
source: https://threejs.org/docs/
verified: never
status: SEED
---
# Engine profile: Web / three.js (and similar glTF web renderers)

## Import
| Item | Value | Label |
|---|---|---|
| Preferred mesh format | GLB via GLTFLoader | [RECALLED] |
| Other accepted formats | FBX, OBJ loaders exist | [RECALLED] |
| Compression | Draco or meshopt geometry; KTX2 textures optional | [RECALLED] confirm |

## Coordinates and scale
| Item | Value | Label |
|---|---|---|
| Up axis | +Y | [RECALLED] |
| Forward axis | +Z front of glTF asset | [RECALLED] |
| Handedness | right-handed | [RECALLED] |
| 1 unit = | 1 meter by convention | [RECALLED] |
| Blender export setting | glTF `export_yup=True` | [RECALLED] |

## Limits
| Item | Value | Label |
|---|---|---|
| Max triangles per mesh | device dependent; ask for target device | UNVERIFIED |
| Max bones | shader uniform limits depend on GPU | UNVERIFIED |
| Max influences | 4 common | [RECALLED] |
| Max texture size | GPU dependent | UNVERIFIED |
| Download size budget | project decision; ask the user | [USER] needed |

## Mesh rules
| Item | Value | Label |
|---|---|---|
| Triangulate | glTF triangles | [RECALLED] |
| Custom normals | supported | [RECALLED] |
| Collision / LOD | none built in; you author it | [RECALLED] |
| Pivot | object origin | [RECALLED] |

## Naming
Free. Names are readable from the loaded scene graph. [RECALLED]

## Rig
Any glTF skeleton. Single root recommended [ASSUMED]. Bone count limits UNVERIFIED.

## Animation
Clips = Blender actions exported as glTF animations; loop is a runtime setting. [RECALLED]

## Materials
metallic-roughness PBR; base color sRGB; others linear; normal +Y; fewer, atlased materials reduce draw calls [RECALLED].

## VFX
| Item | Value | Label |
|---|---|---|
| Particle system | none built in; custom Points/Sprites/Instanced meshes | [RECALLED] |
| Flipbook | custom shader or sprite sheet animators | [RECALLED] |
| Blend modes | additive / normal blending in material | [RECALLED] |
| Mesh effects | plain meshes with custom materials | [RECALLED] |
| UV scroll / dissolve | custom shader | [RECALLED] |
| Max instances | device dependent | UNVERIFIED |

## Camera
| Item | Value | Label |
|---|---|---|
| Camera animation import | glTF cameras can be read by loaders; most projects rebuild cameras in code | [RECALLED] |
| In-engine cinematic tool | code-driven animation (mixer or tweening) | [RECALLED] |
| FOV convention (vertical or horizontal) | PerspectiveCamera fov is vertical | [RECALLED] |
| Sensor / physical camera | n/a | UNVERIFIED |
| Depth of field | custom passes | [RECALLED] |
| Motion blur | custom passes | [RECALLED] |

## Export call
```python
# bpy.ops.export_scene.gltf(export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
```

## Import test
Load in the target page; check scale, facing, textures, clip playback, frame time on the weakest target device.
