# State: <asset>

Single source of truth for one asset. Read at the start of EVERY turn about this asset. Update at the end of every stage.
Stage status values: TODO | PASS | FAIL | STALE (an earlier stage changed after this one passed: re-audit).

asset: <name>
mode: prop | char | hands | env | fx | rig | anim | retopo | fix | optimize | export | audit
role: <budget row>
chain: [stage, stage, ...]
rigor: strict | balanced | flex
current_stage: <skill name>
status: IN-PROGRESS | BLOCKED | SHIP | NO-SHIP
paused: []            # stack of stages interrupted by a side question, newest last
last_checkpoint: <path or none>

| Stage | Status | Evidence (audit JSON file / screenshot) | Date |
|---|---|---|---|

## Waivers (accepted risk)
| Check / gate | Reason | Date |
|---|---|---|

## Decisions (each with a label)
-

## Open assumptions
-
