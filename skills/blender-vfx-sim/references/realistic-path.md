# Realistic VFX path (simulate, render, pack)

Contents: 1 when | 2 steps | 3 lighting and color | 4 render and pack | 5 checks

## 1. When
Style realistic (or stylized with volumetric look) AND type flipbook or chunks. Low-poly/voxel styles skip simulation: draw the shapes with geometry (blender-vfx cookbook, Low-poly column).

## 2. Steps
1. CHECKPOINT. Introspect before setting anything: `[p.identifier for p in bpy.types.FluidDomainSettings.bl_rna.properties]`.
2. SETUP a small domain around the effect; resolution as low as still reads (start 48-64 [START]); duration = effect lifetime plus 20 percent tail.
3. FLOW: fire needs a flow type that produces fire (check the flow type enum by introspection); add small initial velocity; keep one emitter.
4. BAKE the cache once; scrub to check that the shape peaks at 20-30 percent of the life.
5. TIME REMAP if the sim is too slow or fast: adjust frame mapping in the render step, not by re-simulating.

## 3. Lighting and color
| Effect | Render look | Why |
|---|---|---|
| Fire / explosion fireball | emission-driven color ramp (dark red, orange, yellow, white core); read the volume shader sockets by introspection (`[i.name for i in node.inputs]`) | color comes from temperature, not from scene light |
| Smoke / dust | lit by a soft neutral key + fill; render grayscale; tint in the engine | engine tint keeps it reusable |
| Debris | normal mesh materials | handled as chunks |
Rule: no colored scene lights in the bake; the effect must work on different game backgrounds.

## 4. Render and pack
Use blender-vfx-flipbook (camera, transparent film, Standard view transform, straight alpha). Frames 32-64 for realistic [START]; sheet 8x8 at 128-256 per frame; motion blur on when the engine will not add it. Denoise only if grain flickers between frames.

## 5. Checks
`audit_flipbook.py` (sheet integrity) and `audit_fx_style.py` with STYLE = "realistic" (peak position, end clear, frame range). Compare the dark and light background screenshots.
