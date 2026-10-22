# Required audits by asset type

| Asset type | Required audits | Required screenshots |
|---|---|---|
| prop / env | audit_mesh (budget), audit_topology, audit_uv, audit_naming | front, side, 3/4, wireframe |
| char | audit_mesh, audit_topology (ARMATURE, SYMMETRIC), audit_uv, audit_rig, audit_naming | front, side, back, wireframe, 3 joint test poses |
| hands | audit_mesh (hand budget), audit_topology (ARMATURE), audit_rig if rigged | back, palm, side, 90-degree curl |
| anim | audit_anim, audit_naming | key poses per clip |
| fx-mesh | audit_mesh (ALLOW_OPEN, CHECK_UV_RANGE), audit_naming | dark bg, light bg, gameplay distance |
| fx-flipbook | audit_flipbook, audit_fx_style (STYLE) | sheet preview on dark and light |
| camera | audit_camera per shot; shot-list.md complete | start, middle, end per shot |
| fx-chunks | audit_mesh per piece, audit_naming | assembled and exploded view |
Any asset also: engine.md rows relied on are listed with their labels; state.md has no STALE stage.
