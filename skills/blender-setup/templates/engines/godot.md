---
engine: godot
version: UNVERIFIED
source: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/index.html
verified: never
status: SEED
---
# Engine profile: Godot (SEED: verify with `/blender-setup engine godot`)

## Import
| Item | Value | Label |
|---|---|---|
| Preferred mesh format | glTF 2.0 (.glb) | [RECALLED] |
| Other accepted formats | FBX, OBJ, .blend direct import | [RECALLED] confirm |
| Import path | drop into project; Import dock | [RECALLED] |

## Coordinates and scale
| Item | Value | Label |
|---|---|---|
| Up axis | +Y | [RECALLED] |
| Forward axis | -Z is forward in Godot; glTF front faces +Z | [RECALLED] confirm |
| Handedness | right-handed | [RECALLED] |
| 1 unit = | 1 meter | [RECALLED] |
| Blender export setting | glTF with `export_yup=True` | [RECALLED] |

## Limits
| Item | Value | Label |
|---|---|---|
| Max triangles per mesh | UNVERIFIED | UNVERIFIED |
| Max bones | UNVERIFIED | UNVERIFIED |
| Max influences per vertex | UNVERIFIED (4 or 8 recalled) | [RECALLED] confirm |
| Max texture size | UNVERIFIED | UNVERIFIED |
| Max materials per mesh | UNVERIFIED | UNVERIFIED |

## Mesh rules
| Item | Value | Label |
|---|---|---|
| Triangulate on export | glTF triangulates | [RECALLED] |
| Custom normals | supported | [RECALLED] |
| Collision | name suffix hints on the object | [RECALLED] confirm |
| LOD | automatic LOD generation on import | [RECALLED] confirm |
| Pivot | object origin | [RECALLED] |

## Naming
Import hint suffixes recalled by the kit author (confirm in the source page before using): `-col`, `-convcol`, `-colonly`, `-convcolonly`, `-noimp` on objects; `-loop` or `-cycle` on animation names. Label [RECALLED].

## Rig
| Item | Value | Label |
|---|---|---|
| Required skeleton type | any; SkeletonProfileHumanoid optional for retarget | [RECALLED] |
| Bone naming | free | [RECALLED] |
| Root bone | single root recommended | [ASSUMED] |
| Deform-only export | check exporter option | UNVERIFIED |

## Animation
| Item | Value | Label |
|---|---|---|
| Frame rate | set by import / AnimationPlayer | UNVERIFIED |
| Clip source | glTF animations from Blender actions | [RECALLED] |
| Loop flag | suffix hint or edit in AnimationPlayer | [RECALLED] confirm |
| Root motion | RootMotionTrack option | [RECALLED] |

## Materials
| Item | Value | Label |
|---|---|---|
| Workflow | metallic-roughness (StandardMaterial3D) | [RECALLED] |
| Channel packing | ORM channels selectable per slot | [RECALLED] |
| Normal map | OpenGL (+Y) | [RECALLED] |
| Color spaces | base color sRGB; data maps linear | [RECALLED] |
| Vertex color | supported | [RECALLED] |
| Transparency | per-material modes | [RECALLED] |

## VFX
| Item | Value | Label |
|---|---|---|
| Particle system | GPUParticles3D / CPUParticles3D | [RECALLED] |
| Flipbook support | particles animation (h_frames x v_frames) | [RECALLED] |
| Blend modes | add / mix / sub / mul | [RECALLED] |
| Mesh particles / trails | mesh draw pass; trail option | [RECALLED] |
| UV scroll / dissolve | visual shader or shader code | [RECALLED] |
| Vertex animation textures | via shader | [RECALLED] |
| Max simultaneous particles | per node setting | [RECALLED] |

## Camera
| Item | Value | Label |
|---|---|---|
| Camera animation import | glTF camera nodes import; animation via AnimationPlayer | [RECALLED] confirm |
| In-engine cinematic tool | AnimationPlayer or code-driven Camera3D | [RECALLED] |
| FOV convention (vertical or horizontal) | Camera3D fov (vertical by default via keep aspect) | [RECALLED] confirm |
| Sensor / physical camera | n/a | UNVERIFIED |
| Depth of field | environment / camera attributes | [RECALLED] |
| Motion blur | environment / camera attributes | [RECALLED] |

## Export call
```python
# bpy.ops.export_scene.gltf(export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
```

## Import test
1. 1 m cube = 1 m.
2. Facing direction correct.
3. Animations listed in AnimationPlayer; loop flags right.
4. Record in docs/blender/assets.md.
