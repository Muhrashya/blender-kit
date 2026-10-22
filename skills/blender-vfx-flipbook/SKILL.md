---
name: blender-vfx-flipbook
description: Use when making a sprite-sheet (flipbook) effect - smoke, fire, explosion, dust, magic burst, impact frames - rendered from Blender and packed into a power-of-two sheet with transparent background, loop checks and engine play-rate in the FX spec.
---
# Flipbook

## Requires
FX spec (blender-vfx). engine.md VFX row "Flipbook support + layouts" (grid sizes). For volumetric effects: baked simulation from blender-vfx-sim.

## Inputs
Frames | frame size | loop? | tint in engine? (grayscale + alpha) | duration | grid (from engine.md layouts; UNVERIFIED -> power-of-two square grids).

## Steps
1. STYLE + GRID: frame count and size from `docs/blender/reference/vfx-styles.md` (realistic 16-64 frames, stylized 8-24, low-poly 4-12 stepped, voxel 4-8); grid from `references/flipbook-render.md` section 1; only layouts engine.md lists, else square power-of-two.
2. CAMERA: orthographic, locked, subject centered, 8-10 percent padding on every side.
3. RENDER SETUP: section 2 of flipbook-render.md (transparent film, RGBA PNG, Standard view transform, engine id introspected, no motion blur unless baked).
4. LOOK: additive/glow -> emission only; smoke/dust -> soft low-contrast light. Tint in the engine: render grayscale + alpha. Low-poly and voxel: flat emissive colors, hard alpha, stepped timing (render every 2nd or 3rd frame and hold).
5. LOOP: render N+1 frames and drop the last, or use a looping cache.
6. RENDER the PNG sequence to `blender-out/<fx>/flipbook_frames/`.
7. PACK: `docs/blender/scripts/pack_sheet.py` (set FRAMES_DIR, COLS, ROWS, FRAME_PX, OUT_PATH).
8. AUDIT: `docs/blender/scripts/audit_flipbook.py` (PATH, COLS, ROWS, LOOP) and `docs/blender/scripts/audit_fx_style.py` (STYLE, LOOP). Fix every failure.
9. SPEC: grid CxR, frames, play rate = frames / lifetime, blend, tint plan, straight vs premultiplied alpha expectation (UNVERIFIED unless engine.md states it).

## Hard rules
| Rule | Detail |
|---|---|
| Power of two | sheet and frame sizes; square frames |
| Frame order | frame 0 top-left, left to right, top to bottom unless engine.md says otherwise |
| Straight alpha | render straight alpha; state it in the spec |
| No clipping | no frame touches its border |
| Size | smallest frame size that reads; shrink before adding frames |
| Grayscale | when the engine tints |

## Done when
audit_flipbook pass (pow2, grid divides, square frames, alpha, no empty or clipped frames, loop seam) AND audit_fx_style pass (frame range, soft alpha, color count, peak position, ends clear for one-shots); spec filled with play rate.

## On fail
| Failure | Action |
|---|---|
| clipped frames | widen padding or reduce subject scale; re-render |
| loop seam above limit | re-time the last frames; use a looping cache |
| Sheet too big | reduce frame size or frame count |
| Colors shift | Standard view transform; check color management |

## Next
blender-qa -> blender-export.
