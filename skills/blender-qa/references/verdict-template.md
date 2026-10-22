# Verdict template

Contents: 1 verdict block | 2 defect severity

## 1. Verdict block (write to blender-out/<asset>/qa.md)
```
ASSET: <name>   TYPE: <type>   ENGINE: <profile> (status SEED|VERIFIED)
DATE: <YYYY-MM-DD>   BLENDER: <version>
AUDITS: audit_mesh pass=<bool> tris=<n>/<budget> | audit_topology ngons=<n> joint_poles=<n> | audit_uv density=<n> | audit_rig pass=<bool> | audit_anim pass=<bool> | audit_flipbook pass=<bool>
SCREENS: <files>
DEFECTS: <table: id | severity | description | evidence | route>
OPEN ASSUMPTIONS: <list or none>
VERDICT: SHIP | NO-SHIP
```
## 2. Defect severity
| Severity | Examples | Effect on verdict |
|---|---|---|
| Blocker | any audit fail, over budget, STALE stage, ngon, pole at joint, missing deliverable | NO-SHIP |
| Major | silhouette mismatch to reference, visible bake artifact, naming errors, texel density off | NO-SHIP |
| Minor | small shading nit, optional detail missing, cosmetic naming | SHIP with the list |
