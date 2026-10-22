# FX mesh shapes

| Shape | Construction | Segments | UV | Notes |
|---|---|---|---|---|
| Shockwave ring | flat annulus (circle with inner hole) | 16-32 | U around, V inner -> outer | scale from 0 in the engine |
| Slash arc | strip along an arc, width tapers to points at both ends | 8-16 along | U along the arc, V across | handle end is the pivot |
| Beam | open tube | 8-12 sides, 1-2 rings per meter [START] | V along length | no caps |
| Cone | open cone, tip at the origin | 8-12 sides | V from tip to base | no cap |
| Dome | hemisphere without the base | 12 x 6 | planar or spherical, 0-1 | base center pivot |
| Aura shell | slightly scaled copy of the character LP | reuse | reuse base UV or planar | engine renders it additively |
| Vortex strip | twisted strip, 1-2 turns | 12-24 along | U along the spiral | scroll U |
Triangle formula for open tubes: 2 x sides x rows (see blender-topology rules section 9).
