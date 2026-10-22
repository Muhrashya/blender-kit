---
style: voxel
---
# Style: voxel (cube-based, blocky)

| Topic | Rule |
|---|---|
| Unit | one voxel = a fixed edge length (choose one for the whole project, write it in config.md Project overrides); every vertex sits on the voxel grid |
| Geometry | axis-aligned boxes only; no bevels, no curves |
| Triangle strategy | greedy-merge: coplanar neighbouring faces with the SAME color become one rectangle. Delete every face between two touching boxes. Count tris AFTER merging |
| Color | palette texture (16x16 to 64x64) with NEAREST filtering, one texel per color; UVs point at texel centers. No per-voxel texture |
| Shading | flat; no normal map; no AO bake unless the project asks |
| Silhouette | exaggerate: big head, thick limbs; details are colored faces, not geometry |
| Rig | few joints; limbs as blocks; split meshes at joints OR use rigid weights (1 bone = 1.0). Joint rows: 0 extra loops (rigid) or 1 loop pair (soft) |
| Hands | block or mitten (see blender-hands variants/blocky) |
| Pitfalls | T-junction gaps between merged rectangles: keep vertices welded; float drift off-grid: snap and round to 1e-4 |
| Audit overrides | ngons allowed = 0; tris allowed (boxes merge to quads/tris freely); poles allowed on flat areas |
