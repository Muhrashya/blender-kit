# UV rules

Contents: 1 seams | 2 packing and margin | 3 section A palette | 4 section B baked | 5 sizes

## 1. Seams
| Where | Why |
|---|---|
| On hard edges | the shading break hides the seam |
| In hidden areas (underside, back, inside) | invisible |
| Along edge loops | clean island edges |
| Never across a hand/face front view, never through the middle of a flat visible face | visible seam |
| Characters: down the inner arm/leg, behind the ear/neck, under the jaw | convention that hides seams |

## 2. Packing and margin
| Item | Rule |
|---|---|
| Margin (padding) between islands | at least 2 px at 128, 4 px at 256-512, 8 px at 1024 [START] |
| Bake margin | at least the same as the island margin |
| Rotation | allow only if the texture has no directional detail |
| Coverage | aim for over 80 percent of UV space used [START] |

## 3. Section A: palette textures (voxel, lowpoly)
| Item | Rule |
|---|---|
| Texture | 16x16 to 64x64 palette, one texel per color |
| UV | island collapsed onto the texel center of its color: place UVs at (x + 0.5)/W, (y + 0.5)/H |
| Filtering | nearest in the engine; mention in the export report |
| Gradients | a ramp row in the palette if the style needs smooth shading |
| Audit | audit_uv density does not apply; check UVs inside 0-1 and unique colors count |

## 4. Section B: baked textures (stylized, realistic)
| Item | Rule |
|---|---|
| Unwrap | angle-based or conformal; then pack |
| Maps | normal (required for realistic), AO optional, curvature optional, base color painted or projected |
| HP/LP | `_HP` and `_LP` names; same origin and scale |
| Verification | LP + normal map vs HP in the same light |

## 5. Sizes [START]
Use `texture_size_by_role` in config.md. Smaller first; raise only if the density audit fails at the size you picked.
