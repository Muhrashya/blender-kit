---
engine: generic-gltf
version: glTF 2.0
source: https://www.khronos.org/gltf/
verified: never
status: SEED
---
# Engine profile: generic-gltf (fallback for any engine or viewer that reads glTF 2.0)

Use when the engine is unknown, or as the common denominator. Limits below depend on the runtime that loads the file: ask the user which runtime, or label UNVERIFIED.

## Import
| Item | Value | Label |
|---|---|---|
| Preferred mesh format | GLB (single binary file) | [RECALLED] |
| Other accepted formats | glTF + .bin + textures | [RECALLED] |
| Import path / tool | depends on runtime | UNVERIFIED |

## Coordinates and scale
| Item | Value | Label |
|---|---|---|
| Up axis | +Y | [RECALLED] glTF 2.0 spec |
| Forward axis | +Z (front of the asset faces +Z) | [RECALLED] |
| Handedness | right-handed | [RECALLED] |
| 1 unit = | 1 meter | [RECALLED] |
| Blender export setting | `export_yup=True` (Blender converts Z-up to Y-up) | [RECALLED] verify with operator introspection |

## Limits
| Item | Value | Label |
|---|---|---|
| Max triangles per mesh | runtime dependent | UNVERIFIED |
| Max bones | runtime dependent | UNVERIFIED |
| Max bone influences per vertex | 4 is the most common runtime limit | [RECALLED] |
| Max texture size | runtime dependent | UNVERIFIED |
| Max materials per mesh | each material = one primitive | [RECALLED] |

## Mesh rules
| Item | Value | Label |
|---|---|---|
| Triangulate on export | glTF stores triangles; the exporter triangulates | [RECALLED] |
| Custom normals | exported | [RECALLED] |
| Collision / LOD | none in core spec | [RECALLED] |
| Pivot | object origin; set origin to base-center for props | [ASSUMED] |
| Modifiers | `export_apply=True` applies them; reported incompatible with shape keys | [RECALLED] verify |

## Naming
No naming rules in core spec. Animation clip name = Blender action name. [RECALLED]

## Rig
| Item | Value | Label |
|---|---|---|
| Skeleton type | any; joints become nodes | [RECALLED] |
| Bone naming | free | [RECALLED] |
| Root bone | single root recommended | [ASSUMED] |
| Deform-only export | check exporter option via introspection | UNVERIFIED |

## Animation
| Item | Value | Label |
|---|---|---|
| Frame rate | times stored in seconds; fps is not stored | [RECALLED] |
| Clip source | actions / NLA tracks / scene (option name differs by Blender version: introspect `export_animation_mode` vs older `export_nla_strips`) | [RECALLED] |
| Loop flag | none in core spec; runtime decides | [RECALLED] |
| Root motion | runtime decides | UNVERIFIED |

## Materials
| Item | Value | Label |
|---|---|---|
| Workflow | metallic-roughness PBR | [RECALLED] |
| Channel packing | roughness = G, metallic = B in the metallicRoughness texture | [RECALLED] |
| Normal map | OpenGL (+Y, green up) | [RECALLED] |
| Color spaces | base color and emissive sRGB; other maps linear | [RECALLED] |
| Vertex color | supported (COLOR_0) | [RECALLED] |
| Transparency | OPAQUE / MASK / BLEND | [RECALLED] |

## VFX
No particle system in glTF. Deliver meshes + textures + FX spec; the runtime rebuilds the effect. Everything else: UNVERIFIED.

## Camera
| Item | Value | Label |
|---|---|---|
| Camera animation import | glTF supports camera nodes; the Blender exporter has a camera option (introspect `export_cameras`) | [RECALLED] |
| In-engine cinematic tool | none in core spec | [RECALLED] |
| FOV convention (vertical or horizontal) | vertical (yfov) in glTF perspective cameras | [RECALLED] |
| Sensor / physical camera | n/a (FOV only) | [RECALLED] |
| Depth of field | runtime decides | UNVERIFIED |
| Motion blur | runtime decides | UNVERIFIED |

## Export call
```python
# bpy.ops.export_scene.gltf(export_format='GLB', use_selection=True, export_apply=True, export_yup=True,
#                           export_materials='EXPORT', export_animations=True)
# Introspect first; export_asset.py drops unsupported keys and reports them.
```

## Import test
1. Re-import the GLB into a clean Blender scene: dimensions match (meters), orientation correct, materials present.
2. Load it in the target runtime or any glTF viewer: scale, facing, textures, animation clips play.
3. Record in docs/blender/assets.md.
