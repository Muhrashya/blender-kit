# Architecture

Contents: 1 layers | 2 skill graph | 3 contracts | 4 state machine | 5 invalidation | 6 failure routes | 7 anti-hallucination design | 8 file ownership

## 1. Layers
| Layer | Skills | Job |
|---|---|---|
| Intelligence | blender (router), blender-diagnose, blender-setup | classify every message, keep state, answer out-of-context questions with checks, configure the project |
| Geometry | blender-ref, blender-model, blender-topology, blender-topology-fix, blender-retopo, blender-hands | analysis, base mesh, clean light rig-ready topology, repair |
| Surface | blender-uv-bake, blender-material | UV, bake, exportable PBR |
| Motion | blender-rig, blender-animate | skeleton, weights, clips |
| Effects | blender-vfx, -vfx-mesh, -vfx-flipbook, -vfx-texture, -vfx-sim | game effects (realistic, stylized, low-poly, voxel) as exportable assets + layers + engine recipe |
| Cinematics | blender-camera | shot list, camera moves, showcase renders, camera audit |
| Delivery | blender-qa, blender-export | verdict, engine-ready files |

## 2. Skill graph
```
                          /blender  (router + state)
                              |
        +------------+--------+---------+-------------+------------+
     ref/model   topology  retopo     hands         vfx          diagnose
        |        + fix        |         |         (4 subskills)      |
        +------> topology <---+---------+                            +--> routes to any skill
                    |
                uv-bake -> material -> rig -> animate
                    \________________|________________/
                                    qa  --(SHIP)--> export
                         qa --(NO-SHIP)--> fix skill (routes.md section 4)
```

## 3. Contracts (every SKILL.md has the same 7 sections)
| Section | Meaning |
|---|---|
| Requires | files and PASS states needed before it may run |
| Inputs | what it needs from the user or state |
| Steps | numbered procedure |
| Hard rules | table of non-negotiables |
| Done when | measurable gate |
| On fail | failure -> action or skill |
| Next | handoff |

## 4. State machine
Per asset: `blender-out/<asset>/state.md`. Stage status: TODO -> PASS | FAIL; a PASS becomes STALE when an earlier stage changed. Asset status: IN-PROGRESS -> SHIP | NO-SHIP | BLOCKED. The router reads state.md every turn and pushes interrupted stages on `paused`.

## 5. Invalidation
Defined in `skills/blender/references/routes.md` section 3. Example: topology-fix changes the mesh, so uv-bake, material, hands, rig, animate, qa and export become STALE.

## 6. Failure routes
Defined in routes.md section 4 and in each skill's On fail table. Example: rig pinches at an elbow -> diagnose -> topology-fix (joint loops) -> topology -> rig.

## 7. Anti-hallucination design
| Mechanism | Where |
|---|---|
| Evidence labels ([MEASURED], [DOC], [RECALLED], [START], [ASSUMED], [UNVERIFIED]) | ground-rules.md, every report |
| Audit scripts produce the numbers | docs/blender/scripts/ |
| Introspect before calling | ground-rules.md section 3; export_asset.py filters unsupported options |
| Engine profiles are data, not memory | engines/*.md, UNVERIFIED rows disclosed |
| One stage per turn + gates | router rules |
| State file survives long chats | state.md |
| Fixed report format, no filler | router |

## 8. File ownership
| Path | Owner | Overwritten by update? |
|---|---|---|
| skills/** | kit | yes (npx skills update) |
| docs/blender/scripts, ground-rules.md | kit copy | yes (blender-setup update) |
| docs/blender/config.md, engine.md, style.md, assets.md | project | never |
| blender-out/** | project | never |

## 9. Cinematics and VFX style (v0.2)
- `blender-camera` is independent of the asset chain: mode `cam` (camera -> qa -> export when engine.md Camera rows allow). VFX can request a showcase shot from it.
- VFX style is an axis (`fx_style`): the same recipe (cookbook.md) renders differently per style (vfx-styles.md). `audit_fx_style.py` measures style compliance and the life curve.

## 10. Visuals and flexibility (v0.3)
- Diagrams live in `skills/blender-setup/templates/reference/figures/` (copied to `docs/blender/reference/figures/`). They are generated and verified by `tools/make_figures.py`, so pictures cannot drift from the numbers.
- Rigor modes and waivers are defined in ground-rules.md section 10; skip rules in routes.md section 5; the plan cards in reference/build-guide.md.
