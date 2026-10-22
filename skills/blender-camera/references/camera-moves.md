# Camera moves

Contents: 1 purpose -> move | 2 Blender recipes and timing | 3 combos and transitions | 4 source

Diagram of all moves: `docs/blender/reference/figures/camera-moves.png`.

## 1. Purpose -> move
Move list and storytelling purposes follow StudioBinder's guide to camera movement (paraphrased); Blender recipes and numbers are the kit's own.
| Move | What the camera does | Storytelling purpose | Good for game assets and scenes |
|---|---|---|---|
| Static | locked in place; only subjects move | focus on performance, dialogue, precise composition | model sheets, UI-like showcases, calm beats |
| Pan | rotates horizontally | follow a subject, reveal new information | follow a character, reveal a vista |
| Whip pan | very fast pan | energy, link two subjects or places without a cut | transition between two characters or locations |
| Tilt | rotates vertically | show scale, dominance, awe; capture verticality | towering boss, tall building reveal |
| Push in | moves toward the subject | build tension or intimacy; imply inner thought | focus on a hero or item, boss reaction |
| Pull out | moves away from the subject | isolation, detachment, reveal the setting or scope | end of a scene, reveal the arena |
| Zoom | changes focal length without moving | draw attention to a detail; can feel unnatural, unease | horror or thriller beats, detail focus |
| Dolly zoom | dolly one way, zoom the opposite way | warps depth: disorientation, dread, internal conflict (or a link between characters) | rare dramatic moment |
| Roll | rotates around the lens axis | disorient, instability, discomfort | quake, madness, power shift (sparingly) |
| Tracking | travels through the scene following the action | immersion, fluid energy | chase, walk-and-talk, run cycle showcase |
| Truck | tracking shot sideways | follow lateral motion | side-scrolling style showcase |
| Arc | circles the subject | dynamism, menace, energy around a subject | hero reveal, turntable |
| Boom / crane | moves vertically | grand establishing shots, scale, subtle reveals | location establishing shot |
| Handheld | random shake | documentary realism, subjectivity, chaos | impact moments, found-footage feel (restraint) |
| Bird's-eye | looks down from above | distance, insignificance, surveillance, map-like overview | tactical overview, arena layout |
General: a push-in or other move works best after the camera has been still, so the move itself becomes the event.

## 2. Blender recipes and timing [START] (frames at 24 fps; scale by fps / 24)
| Move | Rig in camera_rig.py | Keys | Interpolation | Frames | Pitfalls |
|---|---|---|---|---|---|
| Static | camera + optional Track To target | none | n/a | any | accidental tripod drift: no keys |
| Pan | camera fixed, Track To target empty moves sideways | target location keys | Bezier ease | 48-120 | target moves faster than the subject: reads as whip |
| Whip pan | same, short distance in few frames | target keys; motion blur on | linear or strong ease | 3-8 | no motion blur: looks like a jump cut |
| Tilt | camera fixed, target moves vertically | target keys | Bezier ease | 48-96 | target path not vertical: diagonal drift |
| Push in / pull out | camera location along the view axis | camera location keys | Bezier ease (subtle) or linear | 96-192 subtle, 48-96 dramatic | camera passes through the subject: clip |
| Zoom | lens keys only | lens keys | Bezier ease | 48-120 | combine with a move only as dolly zoom |
| Dolly zoom | camera location + lens keyed with lens proportional to distance | both channels | LINEAR for both | 48-120 | subject size drifts when the formula is off: audit frac |
| Roll | no Track To; baked quaternion keys | rotation_quaternion every 4 frames | linear | 48-120 | accumulated rotation over 180 degrees: split keys |
| Tracking / truck | camera location keys parallel to subject path | location keys | LINEAR (constant speed) | match the subject motion | speed mismatch: sliding subject |
| Arc | camera child of a pivot empty; pivot rotates about Z | pivot rotation keys | Bezier ease or linear | 96-192 for 90-180 degrees | radius changes: keep radius constant |
| Boom / crane | camera location Z keys, target fixed or none | location keys | Bezier ease | 72-192 | tilt from Track To when a pure boom is wanted: disable the constraint |
| Handheld | baked seeded wobble on camera and target | keys every 2 frames | Bezier | any | strength too high: motion discomfort; keep location 0.005-0.02 m, rotation 0.2-0.6 degrees equivalent [START] |
| Bird's-eye | camera high, looking straight down | optional slow descent | Bezier ease | 72-192 | gimbal at straight down: build with rotation (0,0,0) default |
Ease guidance: starts and ends of human-feeling moves use ease in/out; mechanical, constant-speed moves (tracks, turntables, dolly zoom) use linear.

## 3. Combos and transitions
| Combo | How |
|---|---|
| Static then push in | hold 24-72 frames, then move; the contrast is the effect |
| Whip pan transition | whip out of shot A, whip into shot B with matching direction and blur |
| Boom + tilt reveal | rise while the target moves up: scale reveal |
| Arc + push in | dramatic hero reveal; keep subject size stable |
| Pull out after tracking | end a chase by releasing the camera |
Never stack three moves in one shot without a written reason.

## 4. Source
StudioBinder, "Types of Camera Movements in Film Explained: Definitive Guide" (public article of The Shot List series). Re-read it for film examples; this file keeps only the kit's paraphrase.
