# Shot vocabulary

Contents: 1 shot sizes | 2 angles | 3 lenses and FOV | 4 composition | 5 formats

Conventional cinematography terms; values are [START] unless computed. The shot-list columns follow the idea of a StudioBinder shot list (size, angle, movement, lens, rig).

## 1. Shot sizes (for a human-sized subject)
| Size | Abbr | Frames |
|---|---|---|
| Extreme close-up | ECU | a detail: eyes, hand, item |
| Close-up | CU | face, head and shoulders cut off at the chest |
| Medium close-up | MCU | head to mid-chest |
| Medium | MS | head to waist |
| Medium long (cowboy) | MLS | head to mid-thigh |
| Full | FS | whole body with a little margin |
| Long / wide | LS | subject small within the location |
| Extreme long | ELS | location dominates; subject tiny |
Rule: change size by at least one step between cuts so the cut reads.

## 2. Angles
| Angle | Effect |
|---|---|
| Eye level | neutral |
| Low (camera below, looking up) | power, scale, threat |
| High (camera above, looking down) | vulnerability, smallness |
| Bird's-eye / overhead | overview, detachment |
| Dutch (rolled horizon) | unease, instability |
| Over the shoulder | connection in conversations |
| POV | subjective view |

## 3. Lenses and field of view
Blender default sensor width is a property to read, not assume: `cam.data.sensor_width` (commonly 36 mm). The table below uses 36 mm width and a 16:9 sensor (height 20.25 mm), computed as FOV = 2 x atan(sensor / (2 x lens)).
| Lens | Horizontal FOV (deg) | Vertical FOV 16:9 (deg) |
|---|---|---|
| 14 mm | 104.3 | 71.7 |
| 18 mm | 90.0 | 58.7 |
| 24 mm | 73.7 | 45.7 |
| 28 mm | 65.5 | 39.8 |
| 35 mm | 54.4 | 32.3 |
| 50 mm | 39.6 | 22.9 |
| 85 mm | 23.9 | 13.6 |
| 135 mm | 15.2 | 8.6 |

| Lens range | Look |
|---|---|
| 14-24 mm | wide, expansive, visible perspective distortion near edges |
| 28-35 mm | moderate wide, natural storytelling |
| 40-60 mm | normal view |
| 70-135 mm | telephoto: compressed depth, isolated subject |
Convert for engines: engines differ on vertical vs horizontal FOV (see engine.md Camera rows). Vertical FOV from horizontal: vfov = 2 x atan(tan(hfov / 2) x height / width).
Dolly zoom: keep subject size constant with lens / distance constant: lens(t) = lens0 x distance(t) / distance0.

## 4. Composition
| Aid | Rule |
|---|---|
| Rule of thirds | place the eyes or the subject center on a third line; enable `cam.data.show_composition_thirds` while framing |
| Headroom | small gap above the head; more for wide shots |
| Lead room | leave space in the direction the subject faces or moves |
| Depth | foreground, mid, background layers; use depth of field when the style allows |

## 5. Formats
| Item | Value [START] |
|---|---|
| Aspect | 16:9 (1920x1080); wide cinema 2.39:1 (for example 2048x858) |
| FPS | 24 for cinematic look; use the engine.md fps for game-captured cinematics |
| Shutter | 180 degrees = 0.5 (`scene.render.motion_blur_shutter`) when motion blur is on |
