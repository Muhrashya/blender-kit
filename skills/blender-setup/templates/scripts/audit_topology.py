# audit_topology.py - defect MAP of the BASE mesh (what you edit, not the evaluated mesh). Prints JSON.
# Finds: ngons, tris, non-planar quads, thin faces, poles, density spikes, poles/tris/ngons near joints,
# symmetry breaks, pole balance. Optionally selects the defects so the user can see them.
import bpy, bmesh, json, math, statistics
from mathutils import Vector, kdtree

TARGET = None              # object name, or None = active object
ARMATURE = None            # armature object name (enables joint checks), or None
JOINT_RADIUS_EDGES = 3.0   # [START] joint zone radius = this x median edge length
THIN_RATIO = 4.0           # [START] quad longest/shortest edge ratio flagged above this
SPIKE_RATIO = 3.0          # [START] edge length vs median flagged above this (or below 1/this)
NONPLANAR = 0.05           # [START] max vertex distance from face plane / mean edge length
SYMMETRIC = False          # True: check X mirror symmetry (local space)
SYM_TOL = 1e-3
SELECT_DEFECTS = True
LIMIT = 30                 # max indices listed per defect

obj = bpy.data.objects[TARGET] if TARGET else bpy.context.view_layer.objects.active
if obj is None or obj.type != "MESH":
    raise RuntimeError("select or name a mesh object")
me = obj.data
bm = bmesh.new()
bm.from_mesh(me)
bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()
bm.normal_update()

lengths = [e.calc_length() for e in bm.edges]
med = statistics.median(lengths) if lengths else 0.0

ngons = [f.index for f in bm.faces if len(f.verts) > 4]
tris = [f.index for f in bm.faces if len(f.verts) == 3]
nonplanar, thin = [], []
for f in bm.faces:
    if len(f.verts) != 4:
        continue
    vs = [v.co for v in f.verts]
    n = (vs[2] - vs[0]).cross(vs[3] - vs[1])
    if n.length < 1e-12:
        nonplanar.append(f.index)
        continue
    n.normalize()
    c = sum(vs, Vector()) / 4
    el = [e.calc_length() for e in f.edges]
    mean_el = sum(el) / 4
    if mean_el > 0 and max(abs(n.dot(v - c)) for v in vs) / mean_el > NONPLANAR:
        nonplanar.append(f.index)
    if min(el) > 0 and max(el) / min(el) > THIN_RATIO:
        thin.append(f.index)

interior = [v for v in bm.verts if not v.is_boundary and v.link_edges]
poles3 = [v.index for v in interior if len(v.link_edges) == 3]
poles5 = [v.index for v in interior if len(v.link_edges) == 5]
poles6p = [v.index for v in interior if len(v.link_edges) >= 6]
spikes = [e.index for e in bm.edges if med > 0 and (e.calc_length() > SPIKE_RATIO * med or e.calc_length() < med / SPIKE_RATIO)]

closed = bool(bm.edges) and all(e.is_manifold for e in bm.edges)
all_quads = all(len(f.verts) == 4 for f in bm.faces)
pole_balance = sum(4 - len(v.link_edges) for v in bm.verts) if closed and all_quads else None

joint_report = None
if ARMATURE:
    arm = bpy.data.objects[ARMATURE]
    joints = [arm.matrix_world @ b.head_local for b in arm.data.bones if b.parent]
    inv = obj.matrix_world.inverted()
    joints = [inv @ j for j in joints]
    rad = JOINT_RADIUS_EDGES * med
    near = lambda p: any((p - j).length <= rad for j in joints)
    joint_report = {
        "joints_checked": len(joints), "radius": round(rad, 5),
        "poles_near_joints": [i for i in poles3 + poles5 + poles6p if near(bm.verts[i].co)][:LIMIT],
        "tris_near_joints": [i for i in tris if near(bm.faces[i].calc_center_median())][:LIMIT],
        "ngons_near_joints": [i for i in ngons if near(bm.faces[i].calc_center_median())][:LIMIT],
    }

sym_report = None
if SYMMETRIC:
    kd = kdtree.KDTree(len(bm.verts))
    for v in bm.verts:
        kd.insert(v.co, v.index)
    kd.balance()
    unmatched = [v.index for v in bm.verts if v.co.x > SYM_TOL and kd.find(Vector((-v.co.x, v.co.y, v.co.z)))[2] > SYM_TOL]
    off_plane = [v.index for v in bm.verts if 0 < abs(v.co.x) < SYM_TOL]
    sym_report = {"mirror_unmatched_verts": unmatched[:LIMIT], "count_unmatched": len(unmatched),
                  "center_verts_off_plane": off_plane[:LIMIT], "count_off_plane": len(off_plane)}

res = {
    "object": obj.name, "faces": len(bm.faces), "tris_faces": len(tris), "ngons": len(ngons),
    "median_edge_length": round(med, 5),
    "counts": {"ngons": len(ngons), "tri_faces": len(tris), "nonplanar_quads": len(nonplanar), "thin_quads": len(thin),
               "poles_3": len(poles3), "poles_5": len(poles5), "poles_6plus": len(poles6p), "density_spikes": len(spikes)},
    "indices": {"ngons": ngons[:LIMIT], "tri_faces": tris[:LIMIT], "nonplanar_quads": nonplanar[:LIMIT],
                "thin_quads": thin[:LIMIT], "poles_5": poles5[:LIMIT], "poles_6plus": poles6p[:LIMIT],
                "density_spike_edges": spikes[:LIMIT]},
    "closed_manifold": closed, "all_quads": all_quads,
    "pole_balance_sum_4_minus_valence": pole_balance,
    "pole_balance_note": "For a closed all-quad mesh this sum = 4 x Euler characteristic, so it must be a multiple of 8 (8 for a sphere-like mesh). Otherwise the mesh is not a clean closed quad mesh.",
    "pole_balance_multiple_of_8": (pole_balance % 8 == 0) if pole_balance is not None else None,
    "joints": joint_report, "symmetry": sym_report,
}

if SELECT_DEFECTS:
    bad_faces = set(ngons) | set(nonplanar) | set(thin)
    bad_verts = set(poles6p)
    if joint_report:
        bad_verts |= set(joint_report["poles_near_joints"])
        bad_faces |= set(joint_report["tris_near_joints"]) | set(joint_report["ngons_near_joints"])
    for p in me.polygons:
        p.select = p.index in bad_faces
    for v in me.vertices:
        v.select = v.index in bad_verts
    me.update()
    res["selected_for_user"] = {"faces": len(bad_faces), "verts": len(bad_verts)}
bm.free()
print(json.dumps(res, indent=2))
