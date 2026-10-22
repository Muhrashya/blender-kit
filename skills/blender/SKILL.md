---
name: blender
description: Use for ANY Blender or 3D game-asset request and for EVERY follow-up message in a Blender session - props, characters, hands, environments, VFX, retopology, fixing topology, rigging, animation, export, troubleshooting. Classifies each message, loads the right skill, keeps state, switches skills when the question changes.
---
# /blender - router

## Requires
- `docs/blender/config.md`, `docs/blender/ground-rules.md`, `docs/blender/assets.md`. Missing: run `blender-setup`, stop.
- Blender MCP connected, or SCRIPT MODE (ground-rules.md section 7).

## Inputs
`/blender <mode> "<what>" [ref=<file>] [role=<budget row>] [tris=<n>] [style=<name>] [engine=<name>] [platform=pc|mobile]`
Modes: `prop char hands env match rig anim fx cam retopo fix optimize export audit ask doctor`. No mode: classify with `references/intents.md`. Argument grammar: `references/arguments.md`.

## Steps
1. PRE-FLIGHT once per session: read config.md, ground-rules.md, assets.md. Run `docs/blender/scripts/scene_info.py`. Quote Blender version.
2. RIGOR: read `rigor` from config.md (or `rigor=`) and follow ground-rules.md section 10. Waiver words (waive, skip this check, abaikan, lewati): record in state.md `waivers`, mark the gate WAIVED, continue; never waive the never-list.
2b. CLASSIFY every user message with `references/intents.md` BEFORE acting. Output one line: `INTENT: <intent> -> <skill>`.
3. SAME TOPIC as current stage: continue. DIFFERENT TOPIC: push current stage to `paused` in state.md, load the matching skill, answer, then print `BACK TO: <stage>`.
4. NEW ASSET: print the matching card of `docs/blender/reference/build-guide.md` as at most 5 short plan lines (diagram: `docs/blender/reference/figures/pipeline.png`), then write `blender-out/<asset>/brief.md` from `docs/blender/templates/brief.md`, then `state.md` from `docs/blender/templates/state.md`, with the chain from `references/routes.md`. Ask max 3 questions, only for missing facts.
5. RUN one stage: load that skill, do only its Steps, run its audit.
6. REPORT with the Stage report format below. Update state.md and assets.md.
7. INVALIDATE: when a stage changed the mesh/rig/UV, mark every later stage STALE using the table in `references/routes.md`.
8. GATE: PASS -> next stage in chain. FAIL -> follow that skill's On fail table. Never skip a failed stage.

## Stage report format (no other prose)
```
STAGE: <skill> | ASSET: <name>
RESULT: PASS | FAIL
NUMBERS: <key>=<value> [MEASURED] ...
SCREENS: <file names or none>
OPEN ASSUMPTIONS: <list or none>
NEXT: <skill or question>
```

## Hard rules
| Rule | Detail |
|---|---|
| No fluff | No greeting, praise, recap or explanation of what you are about to do. Report format only |
| Stages per turn | strict: one; balanced: chain consecutive PASS stages for low-risk assets; flex: chain until the first FAIL. "run all" always stops at the first FAIL |
| Interrupt safe | A side question never loses the current stage: state.md `paused` stack |
| Non-Blender message | Answer normally. Do not load skills. Do not touch state.md |
| Evidence | Every number in a report is [MEASURED] from an audit script of this session |
| No export without SHIP | blender-export requires a PASS from blender-qa for the same asset version |
| Ask rule | Max 3 questions per turn; never ask what config.md, engine.md or state.md already says |

## Done when
state.md `status` = SHIP and blender-export produced a verified file, or the user ends the task.

## On fail
| Situation | Action |
|---|---|
| config.md missing | run blender-setup init |
| MCP not connected | script mode; show `docs/blender/` mcp-setup note via blender-setup |
| Two skills match equally | take the earlier row of intents.md; ask 1 question only if the result differs a lot |
| Audit script errors | print the error, fix the script call, never skip the audit |
| User asks to skip an audit | refuse; offer to run it |

## Next
The next stage in `references/routes.md` for the asset mode, or the stage popped from `paused`.
