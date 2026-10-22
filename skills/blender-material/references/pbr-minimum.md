# PBR minimum (exportable)

Contents: 1 node set | 2 socket introspection | 3 snippet | 4 audit | 5 transparency and emission

## 1. Node set
Image Texture -> (Normal Map) -> Principled BSDF -> Material Output. Nothing else.

## 2. Socket introspection (names changed between Blender 3.x and 4.x)
```python
mat = bpy.data.materials['MAT_Name']; mat.use_nodes = True
bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
print([i.name for i in bsdf.inputs])
```
Use only names printed. Example: Base Color, Metallic, Roughness, Normal exist in the lists of recent versions; emission and alpha socket names differ: read them.

## 3. Snippet
```python
nt = mat.node_tree
def tex(path, name, noncolor):
    n = nt.nodes.new('ShaderNodeTexImage')
    n.image = bpy.data.images.load(bpy.path.abspath(path)); n.image.name = name
    if noncolor: n.image.colorspace_settings.name = 'Non-Color'
    return n
base = tex('//textures/T_Name_BaseColor.png', 'T_Name_BaseColor', False)
nt.links.new(base.outputs['Color'], bsdf.inputs['Base Color'])
nrm = tex('//textures/T_Name_Normal.png', 'T_Name_Normal', True)
nmap = nt.nodes.new('ShaderNodeNormalMap')
nt.links.new(nrm.outputs['Color'], nmap.inputs['Color'])
nt.links.new(nmap.outputs['Normal'], bsdf.inputs['Normal'])
```
Palette material: base color texture with `interpolation = 'Closest'` on the Image Texture node.

## 4. Audit
```python
for m in bpy.data.materials:
    if m.users and m.use_nodes:
        print(m.name, sorted({n.type for n in m.node_tree.nodes}))
```
Allowed types: BSDF_PRINCIPLED, TEX_IMAGE, NORMAL_MAP, OUTPUT_MATERIAL (+ UVMAP/MAPPING only if engine.md allows). Anything else: bake and replace.

## 5. Transparency and emission
Alpha/blend mode properties differ by version (`blend_method` older, `surface_render_method` newer): introspect with `[p.identifier for p in bpy.types.Material.bl_rna.properties]`. Emission: set the Principled emission color/strength sockets read in section 2; glTF supports an emissive strength extension (engine support from engine.md).
