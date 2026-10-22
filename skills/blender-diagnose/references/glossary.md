# Glossary (answer concept questions from here, max 5 lines)

| Term | Meaning | Why it matters |
|---|---|---|
| Triangle (tri) | face with 3 vertices; engines render triangles | budgets are counted in triangles |
| Quad | face with 4 vertices = 2 triangles | quads deform and subdivide predictably |
| N-gon | face with 5+ vertices | triangulates unpredictably; must be 0 |
| Valence | number of edges at a vertex | poles are valence != 4 |
| Pole | vertex with valence 3 (N-pole) or 5+ (E-pole) | needed to change loop count; harmful at joints |
| Edge loop | continuous chain of edges through quads | loops at joints let the mesh bend cleanly |
| Edge ring | parallel edges crossing a strip of quads | rings define limb cross-sections |
| Manifold | each edge shared by exactly 2 faces | non-manifold edges break bakes and exports |
| Normal | direction a face points | wrong normals cause dark shading |
| Tangent-space normal map | normals stored relative to the surface | needs matching convention (OpenGL +Y or DirectX -Y) |
| HP / LP | high-poly bake source / low-poly game mesh | LP is exported, HP only bakes |
| Retopology | rebuilding a clean low mesh over a detailed one | clean flow for rig and UV |
| UV island | connected patch in UV space | seams separate islands |
| Texel density | texture pixels per meter of surface | keeps detail consistent across assets |
| Bake cage | slightly inflated LP used to cast rays to HP | wrong cage = skewed bake |
| Skin weights | per-vertex influence of each bone | max influences limited by engine |
| Influence | one bone's weight on one vertex | audit_rig counts influences |
| Rest pose | pose the mesh was skinned in | A-pose reduces shoulder deformation |
| Root motion | body movement stored in the root bone | engine can apply it to the character |
| Flipbook | sprite sheet played frame by frame | cheap smoke, fire, explosions |
| Overdraw | stacked transparent pixels drawn per frame | main cost of effects |
| LOD | lower-detail versions swapped by distance | optional per engine |
