# Changelog

## 0.3.0
- Visual builds: 9 original diagrams generated from the kit's own data by `tools/make_figures.py` (pipeline, verified quad loop transitions with subdivision, joint loops, rig-ready zones, finger tiers, hand layout, 12 camera moves, VFX life curve + layers, VFX style comparison). The script verifies the transition meshes (all quads, convex, exact area, manifold, valence 3-5, parity) and checks the hand numbers against the docs.
- Fixed: Ultra hand tier numbers were wrong (missing base ring); now 26 / 18 / 122 tris, hand 142-162. Caught by the new doc check.
- transition-patterns.md rewritten from verified constructions + block grammar + parity rule (N + M + left + right even).
- Less rigid: `rigor` (strict, balanced, flex), waivers with accepted-risk reporting, adaptive skip rules and quick path, 3 blockout options when there is no reference.
- New build-guide.md with cards for prop, character, hands, fix, VFX, camera. Router prints the plan card for a new asset.

## 0.2.0
- New skill blender-camera: shot list, shot sizes/angles/lenses, 15 camera moves (static, pan, whip pan, tilt, push in, pull out, zoom, dolly zoom, roll, tracking/truck, arc, boom/crane, handheld, bird's-eye), turntable/hero/VFX showcase, audit_camera, camera_rig.py.
- VFX: style axis (realistic, stylized, lowpoly, voxel) via reference/vfx-styles.md, 20-effect cookbook with layers and timing, realistic simulation path, audit_fx_style.py (life curve, soft alpha, palette, frame range), layers table in the FX spec, `fx=` argument.
- Engine profiles gained a Camera section (FOV convention, cinematic tool); router gained mode `cam` and intent row 10b; QA gates for camera and FX style.
- Tested with mocks: dolly-zoom math, FOV formulas, audit_fx_style. Not tested in Blender: camera_rig.py, audit_camera.py.

## 0.1.0
- 20 skills: router (intent switching + state), setup, diagnose, ref, model, topology, topology-fix, retopo, hands, uv-bake, material, rig, animate, vfx (+mesh, flipbook, texture, sim), qa, export.
- Engine profiles (generic-gltf, roblox, unity, unreal, godot, web-three) as SEED data; 4 style files; shared reference docs copied to docs/blender/reference/.
- Audit scripts: mesh, topology (defect map), uv, naming, rig, anim, flipbook; helpers: scene_info, checkpoint, pack_sheet, measure_ref, export_asset.
- Tested: lint (npm run validate), Python syntax, and flipbook pack/audit + measure_ref logic with a mocked bpy.
- NOT tested: scripts that need Blender's bmesh/bpy.ops (audit_mesh, audit_topology, audit_rig, audit_anim, audit_uv, export_asset, scene_info). Run evals/cases.md section F first.
