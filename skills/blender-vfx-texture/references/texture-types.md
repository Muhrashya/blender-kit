# Texture types

Contents: 1 recipes | 2 channel packing | 3 tiling check

## 1. Recipes
| Kind | Recipe | Size [START] | Tileable |
|---|---|---|---|
| Soft circle | radial gradient, smooth falloff to 0 at the edge | 128 | no |
| Radial ramp | radial gradient 0 -> 1 | 128 | no |
| Linear ramp | horizontal gradient 0 -> 1 | 128x16 or 128 | no |
| Streak | stretched noise or tapered line, fades at both ends | 256x64 | no |
| Ring | radial gradient band with soft edges | 256 | no |
| Swirl | noise with polar distortion | 256 | no |
| Noise | Perlin/Voronoi noise, mid-gray mean | 128-256 | yes |
| Crack mask | Voronoi edges | 256 | optional |
| Dissolve noise | noise with full 0-1 spread (engine thresholds it) | 128-256 | yes |
| Trail strip | gradient along U, soft edges along V | 256x32 | along U |

## 2. Channel packing
Only when engine.md names the channel order. Example plan: R = mask A, G = mask B, B = noise, A = unused. If order is UNVERIFIED keep separate grayscale files.

## 3. Tiling check
```python
import numpy as np
def tile_diff(px):            # px: H x W x C float array
    return float(np.abs(px[:, 0] - px[:, -1]).mean()), float(np.abs(px[0] - px[-1]).mean())
```
Both values under 0.02 [START] for a texture flagged tileable.
