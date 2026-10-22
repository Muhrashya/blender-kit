---
name: blender-qa
description: Use when verifying an asset before export or when asked "is it ready/ship?", audit, review, QA - runs the required audits per asset type, collects screenshots, classifies defects and gives a SHIP or NO-SHIP verdict recorded in assets.md and state.md.
---
# QA (audit + verdict)

## Requires
state.md for the asset; all earlier stages PASS (no STALE). Screenshot tool via MCP (or user-provided images in script mode).

## Inputs
Asset name | asset type (prop / env / char / hands / fx-mesh / fx-flipbook / fx-chunks / anim / camera).

## Steps
1. GATES: read `references/gates.md` for the asset type; list the required audits.
2. RUN every required audit now (do not reuse old JSON for STALE stages): audit_mesh, audit_topology, audit_uv, audit_naming, audit_rig, audit_anim, audit_flipbook, audit_fx_style, audit_camera as listed.
3. SCREENS per `references/screenshot-angles.md`; save to `blender-out/<asset>/screens/qa_*.png`.
4. COMPARE with the reference or brief (silhouette, color, proportions).
5. DEFECTS: classify per `references/verdict-template.md` section 2 (blocker, major, minor).
6. VERDICT: SHIP only with zero blockers and zero majors; minors listed. Else NO-SHIP with the route for each defect (routes.md section 4).
7. RECORD: write the verdict block (verdict-template.md section 1) to `blender-out/<asset>/qa.md`; update assets.md row and state.md.

## Hard rules
| Rule | Detail |
|---|---|
| Fresh audits | every required audit runs in this QA pass |
| Numbers | every pass/fail cites a JSON value |
| No verdict without screenshots | for visual assets (all types except pure data) |
| Open assumptions | listed in the verdict; [UNVERIFIED] engine limits never count as compliance |
| Blockers | any audit fail, budget overrun, STALE stage, missing file |
| No self-approval | do not edit thresholds to make an asset pass |
| Waivers | state.md waivers are listed in the verdict as accepted risk; a WAIVED gate is never reported as PASS |

## Done when
qa.md written with verdict; assets.md and state.md updated; each defect has a routed fix.

## On fail
| Failure | Action |
|---|---|
| Audit fails | route per routes.md section 4 |
| Screenshot unavailable | script mode: ask the user for images; verdict stays NO-SHIP until received |
| Stage STALE | re-run that stage's audit first |

## Next
SHIP -> blender-export. NO-SHIP -> the first routed fix skill.
