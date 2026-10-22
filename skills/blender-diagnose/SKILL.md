---
name: blender-diagnose
description: Use when something looks wrong or the user asks why/what/how in Blender or 3D asset work - dark or black shading, flipped normals, stretched textures, bake artifacts, wrong scale or rotation in the engine, mesh tearing when posed, animation pops, missing export data, or concept questions (what is a pole, ngon, texel density).
---
# Diagnose (symptom -> check -> fix -> route)

## Requires
Blender session reachable (or script mode). `docs/blender/engine.md` for engine-related symptoms.

## Inputs
The user's symptom in their own words, plus screenshot if given.

## Steps
1. RESTATE the symptom in one line.
2. MATCH rows in `references/symptoms.md` (search by Symptom column; take up to 2 rows).
3. RUN the row's CHECK (script or MCP call). Quote the result as [MEASURED].
4. APPLY the row's FIX with a snippet from `docs/blender/reference/bpy-recipes.md`, or ROUTE to the skill named in the row. Checkpoint first if the fix is destructive.
5. RE-RUN the CHECK. Report before/after numbers.
6. NO MATCHING ROW: collect `scene_info.py` + one screenshot, list max 3 hypotheses with ONE check each, run them in order. Never present an untested hypothesis as the cause.
7. CONCEPT QUESTION ("what is", "apa itu"): answer from `references/glossary.md` in at most 5 lines; add one check the user can run when it applies.

## Hard rules
| Rule | Detail |
|---|---|
| Cause needs evidence | No cause is stated without a check result from this session |
| No guessing parameters | Operator parameters and enum values come from introspection (ground-rules.md section 3) |
| Engine facts | Read engine.md; if the row is UNVERIFIED say so; never fill from memory |
| Minimal fix | Apply the smallest fix that changes the failing number; do not redo the stage |
| Return | After the answer, the router prints BACK TO: <stage> |

## Done when
The failing check now passes, or the user gets the exact next check and the reason a fix cannot be applied yet.

## On fail
| Situation | Action |
|---|---|
| Check cannot run (no MCP) | give the script for script mode, ask for the output |
| Fix made it worse | restore the checkpoint, report, try the next hypothesis |
| Symptom is a topology flaw | blender-topology-fix |
| Symptom needs a new bake/UV | blender-uv-bake |
| Symptom is engine-side only | state what to test in the engine (import test cube) and stop |

## Next
Back to the paused stage (router), or the skill named in the matched row.
