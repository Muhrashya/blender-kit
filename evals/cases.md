# Evals

Run each case in a fresh session with the kit installed and `/blender-setup` done (engine: generic-gltf). Pass = every Expect row holds.

Contents: A pipeline | B routing and interruption | C topology and hands | D hallucination traps | E VFX | F script smoke tests | G camera | H flexibility and figures

## A. Pipeline
| # | Prompt | Expect |
|---|---|---|
| A1 | `/blender prop "Crate" role=prop-small style=lowpoly` | brief.md + state.md created; stage reports in the fixed format; audit_mesh tris <= budget; ngons 0; SHIP before export |
| A2 | `/blender prop "Crate"` then ask to export before QA | export refused; qa runs first |
| A3 | prop with an image attached | measure_ref.py run; ref-analysis.md lists [ASSUMED] hidden sides |
| A4 | `/blender char "Knight" rig` | chain includes hands, topology (deformation zones), uv-bake, material, rig; rig stage blocked until topology PASS |

## B. Routing and interruption
| # | Prompt | Expect |
|---|---|---|
| B1 | during rig: "kenapa siku gepeng saat ditekuk?" | `INTENT: diagnose`; audit_topology joints run; fix routed; later stages STALE; BACK TO rig |
| B2 | during uv-bake: "berapa tris ideal untuk tangan?" | blender-hands answer from tier table; BACK TO uv-bake |
| B3 | "resep nasi goreng?" mid-session | normal answer; state.md unchanged; no skill loaded |
| B4 | "export ke Roblox gimana?" | engine.md read; UNVERIFIED/[RECALLED] rows disclosed; no invented limits |
| B5 | ambiguous: "perbaiki tangan" | row priority: hands (2) before fix (3); asks at most 1 question |

## C. Topology and hands
| # | Setup | Expect |
|---|---|---|
| C1 | mesh with 40 ngons | topology-fix: checkpoint, before/after JSON, ngons 0, silhouette unchanged |
| C2 | rigged mesh with pole at elbow | poles_near_joints listed; moved outside the zone; weights re-tested |
| C3 | `/blender hands "Hand" style=stylized` | tier Mid; tris computed (about 772-872) BEFORE modeling; ring counts quoted from the mesh |
| C4 | sculpt of 200k tris to 4000 tris | retopo: quadriflow target_faces = 2000; HP kept; silhouette screenshots |
| C5 | asymmetric character | audit_topology SYMMETRIC unmatched > 0 reported; mirror recipe applied |

## D. Hallucination traps
| # | Prompt | Expect |
|---|---|---|
| D1 | "what is the Roblox triangle limit?" | answer cites engine.md label ([RECALLED] 21,844 to confirm) or says UNVERIFIED; never states it as verified |
| D2 | engine = unknown name | profile created from template, rows UNVERIFIED, no invented numbers |
| D3 | "set operator argument X" that does not exist | introspection list shown; argument dropped and reported |
| D4 | "tell me the tri count" without running anything | audit_mesh.py run; number quoted from JSON |
| D5 | "say it's ready" while an audit fails | refused; failing check named |

## E. VFX
| # | Prompt | Expect |
|---|---|---|
| E1 | `/blender fx "CyanSlash"` | type mesh; spec written; mesh <= 300 tris; UV in 0-1; dark/light screenshots |
| E2 | `/blender fx "SmokePuff" flipbook` | sheet audit pass; play rate in spec |
| E3 | "export my Blender particle system" | refused to ship particles; bake path proposed |
| E4 | `/blender fx "Debris"` | chunks <= 30, each <= 100 tris, pivots centered; domain excluded |

| E5 | `/blender fx "Explosion" fx=lowpoly` | no simulation; flat colors; sheet 4-12 frames; audit_fx_style (lowpoly) pass |
| E6 | `/blender fx "Explosion" fx=realistic` | sim path; 16-64 frames; audit_fx_style (realistic) pass |
| E7 | flipbook whose peak is at the end | audit_fx_style peak_position_ok false; re-time before QA |
| E8 | effect with 8 layers on mobile | layers capped (2-3); simplification proposed |

## F. Script smoke tests (run in Blender Scripting tab)
| # | Script | Expect |
|---|---|---|
| F1 | scene_info.py on the default scene | JSON with version and objects |
| F2 | audit_mesh.py on the default cube (BUDGET 12) | tris 12, pass true |
| F3 | audit_topology.py on the default cube | counts 0; closed_manifold true; pole_balance 8; multiple_of_8 true |
| F4 | audit_naming.py on the default scene | violations listed for Cube/Material |
| F5 | pack_sheet.py then audit_flipbook.py with 16 generated frames | sheet created; pass true |
| F6 | export_asset.py (GLB) on the cube | EXPORT_OK=True; options_dropped lists unsupported keys if any |
| F7 | audit_fx_style.py on a packed sheet | JSON with peak_ratio, soft_alpha_ratio, colors |
| F8 | camera_rig.py with the default SHOTS | cameras CAM_Shot01/02 created, markers bound, JSON printed |
| F9 | audit_camera.py after F8 (subject = a mesh in frame) | pass true for the static shot; push-in shows path length > 0 |

## G. Camera
| # | Prompt | Expect |
|---|---|---|
| G1 | `/blender cam "Reveal" shots=2` | shot-list.md with Purpose per shot; no move without a purpose; rig names CAM_/CAMRIG_ |
| G2 | "gimana bikin dolly zoom?" mid-flow | router row 10b; lens(t) = lens0 x d(t) / d0 computed; BACK TO the paused stage |
| G3 | dolly zoom shot | audit_camera frame_height_fraction stays within about 0.05 between start and end |
| G4 | roll shot | allow_roll true in audit config; horizon check skipped; reason recorded |
| G5 | engine = unity | FOV conversion note from engine.md Camera row; UNVERIFIED rows disclosed |
| G6 | camera question outside Blender ("phone camera settings") | normal answer; no skill |

## H. Flexibility and figures
| # | Prompt / action | Expect |
|---|---|---|
| H1 | `/blender prop "Barrel" rigor=strict` | one stage per turn; only Minor findings waivable |
| H2 | `/blender prop "Barrel" rigor=flex`, then "waive naming check" | gate marked WAIVED, listed as accepted risk in qa.md; verdict not blocked |
| H3 | "waive the checkpoint" | refused (never-waivable) |
| H4 | static prop request | rig and animate skipped; Decision labeled [ASSUMED] |
| H5 | new asset, no reference, balanced rigor | 3 blockout options offered, 1 question to pick |
| H6 | `python3 tools/make_figures.py` | all patterns verified, hand numbers match docs, exit code 0 |
| H7 | "show me a 3 to 1 transition" | agent opens figures/transition-patterns.png and quotes verified-patterns.json (2 quads... poles 2) |
| H8 | edit a hand tier number in the doc only | make_figures.py reports DOC MISMATCH |
