# Attack and hit timing [START] (at 30 fps)

| Phase | Frames | Purpose |
|---|---|---|
| Anticipation | 4-8 | wind-up so the player reads the attack |
| Strike (impact) | 2-4 | fast; the hit frame is marked in state.md for engine events |
| Hold / recover | 6-12 | settle back to idle |
Total light attack about 12-24 frames (0.4-0.8 s). Heavy attack: anticipation 8-14, strike 3-5, recover 10-18.
Rules: write the impact frame number in the clip table so the engine event and VFX (blender-vfx) line up; attacks are one-shot clips with in-place root unless root motion is required; weapon bone follows the hand with no weights hacks.
