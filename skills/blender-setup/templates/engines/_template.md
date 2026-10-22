---
engine: <name>
version: <engine version this profile was checked against, or UNVERIFIED>
source: <official docs URL(s)>
verified: <YYYY-MM-DD, or never>
status: SEED | VERIFIED
---
# Engine profile: <name>

RULES FOR WHOEVER FILLS THIS FILE (the AI or the user)
1. Every value gets a label: [DOC] (copied from the source URL above, with the page named), [RECALLED] (from memory, not confirmed), [USER], or UNVERIFIED.
2. Never write a number you did not read in the source. If you cannot read the source, write UNVERIFIED.
3. Set `status: VERIFIED` and `verified:` only after every Limits row is [DOC] or [USER].
4. Keep rows even when unknown; an empty row hides a gap.

## Import
| Item | Value | Label |
|---|---|---|
| Preferred mesh format | | |
| Other accepted formats | | |
| Import path / tool | | |

## Coordinates and scale
| Item | Value | Label |
|---|---|---|
| Up axis | | |
| Forward axis | | |
| Handedness | | |
| 1 engine unit = | | |
| Blender export axis / scale settings | | |

## Limits
| Item | Value | Label |
|---|---|---|
| Max triangles per mesh | | |
| Max bones per skeleton | | |
| Max bone influences per vertex | | |
| Max texture size | | |
| Max materials per mesh | | |
| Max vertices per mesh | | |

## Mesh rules
| Item | Value | Label |
|---|---|---|
| Triangulate on export | | |
| Custom normals supported | | |
| Collision naming / method | | |
| LOD naming / method | | |
| Pivot / origin convention | | |

## Naming
(file and object naming rules the engine requires or reads as import hints)

## Rig
| Item | Value | Label |
|---|---|---|
| Required skeleton type | | |
| Bone naming | | |
| Root bone | | |
| Deform-only export | | |

## Animation
| Item | Value | Label |
|---|---|---|
| Frame rate | | |
| Clip source (actions / NLA / scene) | | |
| Loop flag mechanism | | |
| Root motion | | |
| Clip naming | | |

## Materials
| Item | Value | Label |
|---|---|---|
| Workflow (metallic-roughness / other) | | |
| Channel packing | | |
| Normal map convention (OpenGL +Y or DirectX -Y) | | |
| Color spaces (base color / data maps) | | |
| Vertex color used | | |
| Transparency modes | | |

## VFX
| Item | Value | Label |
|---|---|---|
| Particle system | | |
| Flipbook support + layouts | | |
| Blend modes (additive / alpha / multiply) | | |
| Mesh particles / trails / beams | | |
| UV scroll / dissolve in materials | | |
| Vertex animation textures | | |
| Max simultaneous particles / instances | | |

## Camera
| Item | Value | Label |
|---|---|---|
| Camera animation import | | |
| In-engine cinematic tool | | |
| FOV convention (vertical or horizontal) | | |
| Sensor / physical camera | | |
| Depth of field | | |
| Motion blur | | |

## Export call
Exact operator and arguments for this engine (the script filters unsupported arguments):
```python
# bpy.ops.export_scene.<fbx|gltf>(...)
```

## Import test
Steps to prove the asset works in this engine (scale, orientation, materials, skeleton, clips). Record the result in docs/blender/assets.md.
