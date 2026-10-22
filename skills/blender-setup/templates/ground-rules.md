# Ground rules (read at the start of every Blender task)

Purpose: stop invented facts. Any number, API name or engine rule that is not covered below is a guess.

## 1. Evidence labels
Put a label on every limit, engine fact and measurement you write in a brief, spec or report.

| Label | Meaning | Allowed source |
|---|---|---|
| [USER] | the user stated it in chat or in docs/blender/config.md | user text |
| [MEASURED] | produced by a script or MCP call in THIS session | audit JSON, scene_info JSON, screenshot file |
| [DOC] | copied from a docs/blender/ file that has a `source:` URL and a real `verified:` date | engine.md, style.md |
| [RECALLED] | written from the kit author's memory, not confirmed | seed engine profiles |
| [START] | starting-point default from this kit, NOT an engine limit | config.md budgets |
| [ASSUMED] | you chose it because nothing else was available | your own choice |
| [UNVERIFIED] | unknown | never use it to claim compliance |

[RECALLED], [START], [ASSUMED] and [UNVERIFIED] values may be used as defaults, but never presented as an official limit and never used to say "within the engine limit".

## 2. Never invent
1. Engine limits (triangles, bones, influences, texture sizes), import rules, naming rules.
2. Blender operator names and parameters, node socket names, enum values, render-engine ids.
3. MCP tool names.
4. File paths, object names, bone names you did not read from the scene.
5. Hidden sides of a reference image (label them [ASSUMED]).
If you need one of these: verify it (section 3) or label it [UNVERIFIED] and take the safest option.

## 3. Verify before you call
| Need | Check (run through the Blender MCP / script mode) |
|---|---|
| Blender version | `import bpy; print(bpy.app.version_string)` |
| Operator parameters | `print([p.identifier for p in bpy.ops.export_scene.fbx.get_rna_type().properties])` |
| Enum values | `print([i.identifier for i in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items])` |
| Node socket names | `print([i.name for i in bsdf.inputs])` |
| Add-on present | `print('NAME' in bpy.context.preferences.addons.keys())` or `hasattr(bpy.ops.object, 'OPERATOR')` |
| MCP tools | read the tool list you were given; map tools by purpose, not by remembered name |
| File written | `os.path.getsize(path) > 0` |
If a check fails: report it. Do not retry with a guess.

## 4. Measure, do not eyeball
Triangles, ngons, UV range, bones, influences, frames, sheet sizes: run the audit script and quote its numbers.
Visual claims need a screenshot file name.

## 5. Stage protocol
1. Name the stage you are in.
2. Do only that stage.
3. Run the stage audit.
4. Report numbers + screenshot names + pass/fail.
5. On fail: stop, fix, re-audit. Never continue past a failed audit.
6. Never write "done", "ready" or "exported" without an audit pass; for export also a file-exists check.

## 6. Safety
- First code execution of a session: ask the user to save the .blend, or save a copy yourself with `bpy.ops.wm.save_as_mainfile(filepath=..., copy=True)` (templates/scripts/checkpoint.py).
- Checkpoint before destructive steps: retopo, decimate, apply modifiers, join, delete.
- Never delete or overwrite the user's source objects. Duplicate first.
- Do not run code you cannot explain.

## 7. No MCP?
If no tool can run Python in Blender: SCRIPT MODE. Write one self-contained script per stage. Tell the user to paste it in Blender > Scripting and paste the printed output back. Labels, audits and gates still apply.

## 8. Open assumptions
At the end of every stage reply print `Open assumptions:` and list every [UNVERIFIED], [ASSUMED], [RECALLED], [START] item you relied on. Empty list = `none`.

## 9. Asking
Ask at most 3 questions, only for facts you cannot verify and that change the result. Otherwise choose the safest default, label it, continue.

## 10. Rigor and waivers (so the workflow adapts instead of blocking)
`rigor` in config.md (override per request with `rigor=`):
| Rigor | Behavior |
|---|---|
| strict | one stage per turn; every gate mandatory; only Minor findings can be waived |
| balanced (default) | consecutive PASS stages may run in one turn for low-risk assets (prop, env, fx, cam); gates stay mandatory; Major and Minor findings can be waived with a reason; at most 1 question |
| flex | the user may waive any gate except the never-waive list; at creative decisions offer options (A/B/C); chain stages until the first FAIL; one combined report per batch |
Skip rules (routes.md section 5) apply in every mode; each skip is a Decision labeled [ASSUMED] and the user can reverse it.
Waiver: when the user says "waive", "skip this check", "ignore", "lewati" or "abaikan", record in state.md `waivers` (check, reason, date), mark that gate WAIVED (not PASS), continue. QA lists waived gates as accepted risk in the verdict.
Never waivable: checkpoint before destructive steps; saving the .blend before running code; file-exists check after export; evidence labels (no claiming compliance with an UNVERIFIED limit); honest reporting of an audit result.
