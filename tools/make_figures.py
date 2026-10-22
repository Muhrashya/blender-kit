#!/usr/bin/env python3
"""Generates the kit's original diagrams from data and VERIFIES the geometry/numbers they show.
Run: python3 tools/make_figures.py   (needs numpy + matplotlib)
Output: skills/blender-setup/templates/reference/figures/*.png + verified-patterns.json
Nothing here copies third-party images: every figure is drawn from the kit's own tables and computed meshes."""
import json, math, pathlib, re, random, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, Wedge, FancyBboxPatch

ROOT = pathlib.Path(__file__).resolve().parents[1]
REF = ROOT / "skills/blender-setup/templates/reference"
OUT = REF / "figures"
OUT.mkdir(parents=True, exist_ok=True)
DPI = 130
BLUE, RED, GREEN, GREY, ORANGE = "#2b6cb0", "#c53030", "#2f855a", "#4a5568", "#dd6b20"

# ============================================================ 1. quad transition patterns (constructed + verified)
H = 2.0
def build_pattern(N, groups, sides):
    """groups: list of (type, sl, sr); type S=1 column->1, A=2->1, C=3->1. sides: edge counts of the G+1 vertical lines."""
    G = len(groups)
    vs = []
    def add(x, y): vs.append((x, y)); return len(vs) - 1
    B = [add(i, 0.0) for i in range(N + 1)]
    T = [add(j * N / G, H) for j in range(G + 1)]
    starts, c = [], 0
    for t, _, _ in groups:
        starts.append(c); c += {"S": 1, "A": 2, "C": 3}[t]
    assert c == N, "groups must consume N columns"
    mid = {}
    for j in range(G + 1):
        bx = starts[j] if j < G else N
        if sides[j] == 2:
            mid[j] = add((bx + j * N / G) / 2, H / 2)
    faces = []
    for j, (t, sl, sr) in enumerate(groups):
        a = starts[j]
        assert sl == sides[j] and sr == sides[j + 1]
        Ml, Mr = mid.get(j), mid.get(j + 1)
        if t == "S":
            if (sl, sr) == (1, 1):
                faces.append([B[a], B[a + 1], T[j + 1], T[j]])
            elif (sl, sr) == (2, 2):
                faces += [[B[a], B[a + 1], Mr, Ml], [Ml, Mr, T[j + 1], T[j]]]
            else:
                raise ValueError("S needs equal sides")
        elif t == "A":
            P = add(a + 1, H / 2)
            if (sl, sr) == (1, 2):
                faces += [[B[a], B[a + 1], P, T[j]], [B[a + 1], B[a + 2], Mr, P], [P, Mr, T[j + 1], T[j]]]
            elif (sl, sr) == (2, 1):
                faces += [[B[a + 1], B[a + 2], T[j + 1], P], [B[a], B[a + 1], P, Ml], [P, Ml, T[j], T[j + 1]]]
            else:
                raise ValueError("A needs sides (1,2) or (2,1)")
        elif t == "C":
            assert (sl, sr) == (1, 1)
            P, Q = add(a + 1, H / 2), add(a + 2, H / 2)
            faces += [[B[a], B[a + 1], P, T[j]], [B[a + 1], B[a + 2], Q, P], [B[a + 2], B[a + 3], T[j + 1], Q], [P, Q, T[j + 1], T[j]]]
    out = []
    for f in faces:
        cx = sum(vs[i][0] for i in f) / 4; cy = sum(vs[i][1] for i in f) / 4
        out.append(sorted(f, key=lambda i: math.atan2(vs[i][1] - cy, vs[i][0] - cx)))
    return vs, out

def area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))) / 2

def verify(name, N, groups, sides, vs, fs):
    M = len(groups)
    errs = []
    if any(len(set(f)) != 4 for f in fs): errs.append("face with repeated vertex")
    for f in fs:                                   # convex, CCW
        pts = [vs[i] for i in f]
        for k in range(4):
            a, b, c = pts[k], pts[(k + 1) % 4], pts[(k + 2) % 4]
            if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) <= 1e-9: errs.append("non-convex or reversed quad")
    total = sum(area([vs[i] for i in f]) for f in fs)
    if abs(total - N * H) > 1e-6: errs.append(f"area {total} != {N*H}")
    ecount = {}
    for f in fs:
        for k in range(4):
            e = tuple(sorted((f[k], f[(k + 1) % 4]))); ecount[e] = ecount.get(e, 0) + 1
    if any(v > 2 for v in ecount.values()): errs.append("edge shared by more than 2 faces")
    bedges = [e for e, v in ecount.items() if v == 1]
    expected_b = N + M + sides[0] + sides[-1]
    if len(bedges) != expected_b: errs.append(f"boundary edges {len(bedges)} != {expected_b}")
    for (a, b) in bedges:                          # boundary must lie on the rectangle border
        for i in (a, b):
            x, y = vs[i]
            if not (abs(y) < 1e-9 or abs(y - H) < 1e-9 or abs(x) < 1e-9 or abs(x - N) < 1e-9): errs.append("boundary vertex not on border")
    V, E, F = len(vs), len(ecount), len(fs)
    if V - E + F != 1: errs.append(f"Euler {V-E+F} != 1")
    bverts = {i for e in bedges for i in e}
    val = {i: 0 for i in range(V)}
    for (a, b) in ecount: val[a] += 1; val[b] += 1
    interior = [val[i] for i in range(V) if i not in bverts]
    if any(v not in (3, 4, 5) for v in interior): errs.append(f"interior valence outside 3-5: {interior}")
    parity = (N + M + sides[0] + sides[-1]) % 2 == 0
    if not parity: errs.append("parity rule violated")
    aspect = min(min(math.dist(vs[f[k]], vs[f[(k + 1) % 4]]) for k in range(4)) / max(math.dist(vs[f[k]], vs[f[(k + 1) % 4]]) for k in range(4)) for f in fs)
    return {"pattern": name, "columns_bottom": N, "columns_top": M, "outer_sides": [sides[0], sides[-1]],
            "vertices": V, "faces": F, "all_quads": True, "boundary_edges": len(bedges), "parity_even": parity,
            "interior_valences": sorted(interior), "poles_3": interior.count(3), "poles_5": interior.count(5),
            "min_edge_ratio": round(aspect, 2), "errors": errs, "ok": not errs}, val, bverts

def subdivide(vs, fs):
    vs = list(vs); emap = {}; out = []
    def mid(a, b):
        k = tuple(sorted((a, b)))
        if k not in emap:
            emap[k] = len(vs); vs.append(((vs[a][0] + vs[b][0]) / 2, (vs[a][1] + vs[b][1]) / 2))
        return emap[k]
    for f in fs:
        c = len(vs); vs.append((sum(vs[i][0] for i in f) / 4, sum(vs[i][1] for i in f) / 4))
        m = [mid(f[i], f[(i + 1) % 4]) for i in range(4)]
        for i in range(4): out.append([f[i], m[i], c, m[(i - 1) % 4]])
    return vs, out

PATTERNS = [
    ("1 to 1", 1, [("S", 1, 1)], [1, 1]),
    ("2 to 1", 2, [("A", 1, 2)], [1, 2]),
    ("3 to 1", 3, [("C", 1, 1)], [1, 1]),
    ("3 to 2", 3, [("A", 1, 2), ("S", 2, 2)], [1, 2, 2]),
    ("4 to 2", 4, [("A", 1, 2), ("A", 2, 1)], [1, 2, 1]),
    ("5 to 3", 5, [("A", 1, 2), ("A", 2, 1), ("S", 1, 1)], [1, 2, 1, 1]),
]

EXTRA = [
    ("6 to 3", 6, [("A", 1, 2), ("A", 2, 1), ("A", 1, 2)], [1, 2, 1, 2]),
    ("6 to 2", 6, [("C", 1, 1), ("C", 1, 1)], [1, 1, 1]),
]

def draw_mesh(ax, vs, fs, val=None, bverts=None, poles=True, lw=1.4, dots=True):
    for f in fs:
        ax.add_patch(Polygon([vs[i] for i in f], closed=True, fc="#edf2f7", ec="#1a202c", lw=lw))
    if poles and val is not None:
        for i, v in enumerate(vs):
            if i < len(val) and i not in bverts:
                if val[i] == 3: ax.add_patch(Circle(v, 0.11, fc=BLUE, ec="white", lw=0.8, zorder=5))
                if val[i] == 5: ax.add_patch(Circle(v, 0.11, fc=RED, ec="white", lw=0.8, zorder=5))
    ax.set_aspect("equal"); ax.axis("off")

def fig_transitions():
    results = []
    fig, axes = plt.subplots(2, len(PATTERNS), figsize=(3.0 * len(PATTERNS), 4.7))
    for k, (name, N, groups, sides) in enumerate(PATTERNS):
        vs, fs = build_pattern(N, groups, sides)
        res, val, bverts = verify(name, N, groups, sides, vs, fs)
        res["drawn"] = True
        results.append(res)
        ax = axes[0][k]; draw_mesh(ax, vs, fs, val, bverts)
        ax.set_xlim(N / 2 - 2.9, N / 2 + 2.9); ax.set_ylim(-1.0, H + 0.4)
        ax.set_title(f"{name}  (sides {sides[0]}/{sides[-1]})", fontsize=11, fontweight="bold")
        ax.text(N / 2, -0.55, f"{res['faces']} quads, 3-poles {res['poles_3']}, 5-poles {res['poles_5']}", ha="center", fontsize=8.5, color=GREY)
        vs2, fs2 = subdivide(vs, fs)
        ax2 = axes[1][k]; draw_mesh(ax2, vs2, fs2, poles=False, lw=0.8)
        ax2.set_xlim(N / 2 - 2.9, N / 2 + 2.9); ax2.set_ylim(-1.0, H + 0.4)
        ax2.text(N / 2, -0.55, f"subdivided: {len(fs2)} quads", ha="center", fontsize=8.5, color=GREY)
    for name, N, groups, sides in EXTRA:
        vs, fs = build_pattern(N, groups, sides)
        res, _, _ = verify(name, N, groups, sides, vs, fs); res["drawn"] = False; results.append(res)
    fig.text(0.5, 0.95, "Quad-only loop transitions (columns at bottom -> columns at top)", ha="center", fontsize=13, fontweight="bold")
    fig.text(0.5, 0.90, "blue dot = 3-pole, red dot = 5-pole. Constructed by script and verified: all quads, convex, area exact, manifold, interior valence 3-5, parity rule.", ha="center", fontsize=8.5, color=GREY)
    fig.subplots_adjust(top=0.84, bottom=0.02, left=0.01, right=0.99, wspace=0.04, hspace=0.04)
    fig.savefig(OUT / "transition-patterns.png", dpi=DPI); plt.close(fig)
    (OUT / "verified-patterns.json").write_text(json.dumps(results, indent=2))
    return results

# ============================================================ 2. hand tiers (data shared with hand-topology.md)
TIERS = {
    "Ultra": dict(sides=4, L=1, Lm=1, extra=0, te=0, pal=(20, 40)),
    "Low": dict(sides=6, L=2, Lm=1, extra=0, te=0, pal=(60, 100)),
    "Mid": dict(sides=8, L=3, Lm=2, extra=0, te=0, pal=(150, 250)),
    "Hero": dict(sides=8, L=3, Lm=2, extra=3, te=2, pal=(300, 500)),
}
def tier_numbers(t):
    rings = t["Lm"] + 2 * t["L"] + 1 + t["extra"]; rows = rings - 1
    fin = 2 * t["sides"] * rows + (t["sides"] - 2)
    trings = t["Lm"] + t["L"] + 1 + t["te"]; trows = trings - 1
    thumb = 2 * t["sides"] * trows + (t["sides"] - 2)
    total = 4 * fin + thumb
    return dict(rings=rings, rows=rows, finger=fin, thumb=thumb, fingers_sum=total, hand=(total + t["pal"][0], total + t["pal"][1]))

PH = (1.0, 0.65, 0.5)           # phalanx length ratios proximal:middle:distal [START]
def ring_positions(t):
    j1, j2, j3 = 0.0, PH[0], PH[0] + PH[1]
    total = sum(PH)
    def spread(center, d, n): return [center] if n == 1 else [center + (i - (n - 1) / 2) * d for i in range(n)] if n == 2 else [center + (i - 1) * d for i in range(n)]
    pos = [i * 0.07 for i in range(t["Lm"])]
    pos += spread(j2, 0.1 * PH[0], t["L"]) + spread(j3, 0.1 * PH[1], t["L"])
    if t["extra"]: pos += [PH[0] / 2, PH[0] + PH[1] / 2, PH[0] + PH[1] + PH[2] / 2]
    pos.append(total)
    pos = sorted(pos)
    assert len(pos) == t["Lm"] + 2 * t["L"] + 1 + t["extra"]
    return pos

def check_hand_doc():
    doc = (REF / "hand-topology.md").read_text()
    problems = []
    for name, t in TIERS.items():
        n = tier_numbers(t)
        row = re.search(rf"\|\s*{name}\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d,]+)-?([\d,]*)", doc)
        m = re.search(rf"\|\s*{name}\s*\|\s*{n['finger']}\s*\|\s*{n['thumb']}\s*\|\s*{n['fingers_sum']}\s*\|", doc)
        lo, hi = n['hand']; fmt = lambda v: f"{v:,}"
        if f"{fmt(lo)}-{fmt(hi)}" not in doc: problems.append(f"{name}: hand total {fmt(lo)}-{fmt(hi)} not found in hand-topology.md")
        if not m: problems.append(f"{name}: computed finger {n['finger']}, thumb {n['thumb']}, sum {n['fingers_sum']} not found in hand-topology.md table")
    return problems

def fig_finger_tiers():
    fig, axes = plt.subplots(4, 1, figsize=(9, 7.4))
    total = sum(PH)
    for ax, (name, t) in zip(axes, TIERS.items()):
        n = tier_numbers(t); pos = ring_positions(t)
        ax.add_patch(Polygon([(0, -0.25), (total - 0.1, -0.25), (total, -0.1), (total, 0.1), (total - 0.1, 0.25), (0, 0.25)], fc="#fefcbf", ec="#744210", lw=1.3))
        for p in pos: ax.plot([p, p], [-0.25 if p < total - 0.1 else -0.1, 0.25 if p < total - 0.1 else 0.1], color="#1a202c", lw=1.3)
        for jx, lab in ((0, "MCP"), (PH[0], "PIP"), (PH[0] + PH[1], "DIP")):
            ax.plot([jx], [0.42], marker="v", color=RED, ms=7); ax.text(jx, 0.55, lab, ha="center", fontsize=8, color=RED)
        ax.set_xlim(-0.2, 3.9); ax.set_ylim(-0.5, 0.85); ax.axis("off")
        ax.text(-0.18, 0.0, name, fontsize=12, fontweight="bold", va="center", ha="right") if False else None
        ax.text(2.45, 0.05, f"{name}: sides {t['sides']}, joint loops {t['L']}, rings {n['rings']}, rows {n['rows']}\n= {n['finger']} tris per finger | thumb {n['thumb']} | 4 fingers + thumb = {n['fingers_sum']}\nhand with palm and wrist about {n['hand'][0]}-{n['hand'][1]} tris", fontsize=8.6, va="center", color="#1a202c")
        ax.text(-0.15, 0.0, name, fontsize=12, fontweight="bold", va="center")
    fig.suptitle("Finger ring layout per tier (red = joints; loops straddle each joint)", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96]); fig.savefig(OUT / "finger-tiers.png", dpi=DPI); plt.close(fig)

def fig_hand_layout():
    fig, ax = plt.subplots(figsize=(6.6, 7.2))
    ax.add_patch(Polygon([(-1.6, 0), (1.6, 0), (1.7, 3.0), (-1.7, 3.0)], fc="#fbd38d", ec="#744210", lw=1.5))
    names = [("index", -1.2, 0.9), ("middle", -0.4, 1.0), ("ring", 0.4, 0.9), ("pinky", 1.2, 0.7)]
    scale = 3.0
    for nm, x, r in names:
        L = r * scale
        ax.add_patch(FancyBboxPatch((x - 0.3, 3.0), 0.6, L, boxstyle="round,pad=0.0,rounding_size=0.28", fc="#fbd38d", ec="#744210", lw=1.5))
        tot = sum(PH)
        for frac, lab in ((0, "MCP"), (PH[0] / tot, "PIP"), ((PH[0] + PH[1]) / tot, "DIP")):
            y = 3.0 + frac * L
            ax.add_patch(Circle((x, y), 0.2, fc="none", ec=RED, lw=1.6, ls="--"))
            if nm == "middle": ax.text(x + 0.42, y, lab, color=RED, fontsize=8, va="center")
        ax.text(x, 3.0 + L + 0.2, nm, ha="center", fontsize=8)
    ang = math.radians(125); base = np.array([-1.6, 1.0]); tl = 2.1
    tip = base + tl * np.array([math.cos(ang), math.sin(ang)])
    ax.plot([base[0], tip[0]], [base[1], tip[1]], color="#744210", lw=24, solid_capstyle="round", alpha=0.9)
    ax.plot([base[0], tip[0]], [base[1], tip[1]], color="#fbd38d", lw=21, solid_capstyle="round")
    ax.text(tip[0] - 0.35, tip[1] + 0.7, "thumb\n30-45 deg from index", ha="center", fontsize=8)
    ax.add_patch(Circle((0, 1.1), 0.45, fc=GREEN, alpha=0.25, ec=GREEN)); ax.text(0, 1.1, "palm center\npoles OK", ha="center", va="center", fontsize=8, color=GREEN)
    for x in (-0.8, 0.0, 0.8): ax.add_patch(Circle((x, 3.18), 0.1, fc=GREEN, alpha=0.7)); 
    ax.text(0, 3.42 + 0.0, "", fontsize=1)
    ax.plot([-1.6, 1.6], [-0.15, -0.15], color=BLUE, lw=3); ax.text(0, -0.55, "wrist ring: vertex count = forearm ring count", ha="center", fontsize=8.5, color=BLUE)
    ax.text(0, 2.25, "webbing (green dots): poles allowed,\nnever within 1 ring of MCP", ha="center", fontsize=7.5, color=GREEN)
    ax.set_xlim(-3.6, 2.4); ax.set_ylim(-1.1, 6.9); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Hand layout (back view): rest pose, gaps between fingers, joint zones in red", fontsize=10, fontweight="bold")
    fig.tight_layout(); fig.savefig(OUT / "hand-layout.png", dpi=DPI); plt.close(fig)

# ============================================================ 3. joint loops + rig-ready zones
def fig_joint_loops():
    cfg = [("Low (2 loops)", [-0.1, 0.1], [-0.55, 0.55]), ("Mid (3 loops)", [-0.15, 0.0, 0.15], [-0.6, 0.6]), ("Hero (4 loops + outer-elbow point)", [-0.21, -0.07, 0.07, 0.21], [-0.62, -0.4, 0.4, 0.62])]
    fig, axes = plt.subplots(3, 1, figsize=(9, 6.6))
    for ax, (title, jl, ml) in zip(axes, cfg):
        ax.add_patch(Rectangle((-1.0, -0.22), 2.0, 0.44, fc="#e2e8f0", ec="#2d3748", lw=1.3))
        zone = max(abs(x) for x in jl) + 0.1
        ax.add_patch(Rectangle((-zone, -0.42), 2 * zone, 0.84, fc=RED, alpha=0.12, ec=RED, ls="--"))
        for x in jl: ax.plot([x, x], [-0.22, 0.22], color="#1a202c", lw=2.2)
        for x in ml: ax.plot([x, x], [-0.22, 0.22], color="#718096", lw=1.2)
        ax.plot([-1.0, 1.0], [0, 0], color=BLUE, lw=1.3, ls=":"); ax.plot([0], [0], marker="o", color=BLUE, ms=8)
        ax.text(0, 0.55, "joint center (bone head)", ha="center", fontsize=8, color=BLUE)
        ax.text(zone + 0.03, -0.38, "no poles inside the red zone (within 1 ring of the joint)", fontsize=8, color=RED, va="center")
        ax.set_xlim(-1.1, 1.6); ax.set_ylim(-0.6, 0.8); ax.axis("off")
        ax.text(-1.05, 0.62, title, fontsize=10.5, fontweight="bold")
    fig.suptitle("Joint loops straddle the joint, rings are perpendicular to the bone", fontsize=11.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95]); fig.savefig(OUT / "joint-loops.png", dpi=DPI); plt.close(fig)

def fig_rig_zones():
    J = {"neck": (0, 8.5), "L shoulder": (-0.9, 8.1), "R shoulder": (0.9, 8.1), "L elbow": (-1.9, 6.7), "R elbow": (1.9, 6.7),
         "L wrist": (-2.7, 5.4), "R wrist": (2.7, 5.4), "L hip": (-0.55, 5.0), "R hip": (0.55, 5.0), "L knee": (-0.65, 2.7), "R knee": (0.65, 2.7),
         "L ankle": (-0.7, 0.5), "R ankle": (0.7, 0.5)}
    fig, ax = plt.subplots(figsize=(6.4, 8.6))
    bones = [("neck", "L shoulder"), ("neck", "R shoulder"), ("L shoulder", "L elbow"), ("L elbow", "L wrist"), ("R shoulder", "R elbow"), ("R elbow", "R wrist"),
             ("L hip", "L knee"), ("L knee", "L ankle"), ("R hip", "R knee"), ("R knee", "R ankle"), ("L hip", "R hip")]
    ax.add_patch(Circle((0, 9.3), 0.6, fc="#e2e8f0", ec="#2d3748"))
    ax.plot([0, 0], [8.5, 5.0], color="#2d3748", lw=3)
    for a, b in bones: ax.plot([J[a][0], J[b][0]], [J[a][1], J[b][1]], color="#2d3748", lw=3)
    labels = {"neck": "neck 3", "shoulder": "shoulder 4-5", "elbow": "elbow 3", "wrist": "wrist 2-3", "hip": "hip 4", "knee": "knee 3", "ankle": "ankle 3"}
    for nme, (x, y) in J.items():
        ax.add_patch(Circle((x, y), 0.42, fc=RED, alpha=0.22, ec=RED, ls="--"))
        if nme.startswith("R ") or nme == "neck":
            key = nme.split(" ")[-1]; ax.text(x + 0.55 if nme != "neck" else x + 0.55, y + (0.1 if nme == "neck" else 0), labels[key] if key in labels else key, fontsize=8, color=RED, va="center")
    for (x, y, t) in ((0, 7.0, "torso center / back\npole parking"), (-1.55, 6.05, ""), (-0.6, 3.8, ""), (0.6, 3.8, "")):
        ax.add_patch(Circle((x, y), 0.4, fc=GREEN, alpha=0.25, ec=GREEN))
        if t: ax.text(x, y, t, ha="center", va="center", fontsize=7.5, color=GREEN)
    ax.text(-3.4, 3.8, "mid-limb sections:\npoles OK (green)", fontsize=8, color=GREEN)
    ax.set_xlim(-3.6, 3.8); ax.set_ylim(-0.4, 10.2); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Rig-ready zones (Mid tier loop counts): red = no poles, green = pole parking", fontsize=9.5, fontweight="bold")
    fig.tight_layout(); fig.savefig(OUT / "rig-ready-zones.png", dpi=DPI); plt.close(fig)

# ============================================================ 4. camera moves
def cam(ax, x, y, heading, fov, length=2.0, color="#2b6cb0", alpha=0.18, body=True):
    ax.add_patch(Wedge((x, y), length, heading - fov / 2, heading + fov / 2, fc=color, ec=color, alpha=alpha, lw=1))
    if body: ax.add_patch(Circle((x, y), 0.12, fc="#1a202c", zorder=5))

def arrow(ax, a, b, color="#1a202c", rad=0.0):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, connectionstyle=f"arc3,rad={rad}"))

def fig_camera_moves():
    fig, axes = plt.subplots(3, 4, figsize=(13, 9.2))
    A = axes.ravel()
    def setup(ax, title, lim=(-2.2, 4.6, -2.6, 2.6)):
        ax.set_xlim(lim[0], lim[1]); ax.set_ylim(lim[2], lim[3]); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(title, fontsize=10.5, fontweight="bold")
    subj = lambda ax, x, y, r=0.28: ax.add_patch(Circle((x, y), r, fc=ORANGE, ec="#7b341e", zorder=4))
    # 1 static
    ax = A[0]; setup(ax, "Static (plan view)"); cam(ax, 0, 0, 0, 40, 3.2); subj(ax, 3, 0); ax.text(0, -1.6, "locked, only subject moves", ha="center", fontsize=8)
    # 2 pan
    ax = A[1]; setup(ax, "Pan / whip pan (plan)"); cam(ax, 0, 0, 25, 36, 3.0, alpha=0.12); cam(ax, 0, 0, -25, 36, 3.0, alpha=0.3); subj(ax, 2.7, 1.3); subj(ax, 2.7, -1.3)
    arrow(ax, (1.0, 0.55), (1.0, -0.55), rad=-0.5); ax.text(0, -2.1, "rotates horizontally in place", ha="center", fontsize=8)
    # 3 tilt (side)
    ax = A[2]; setup(ax, "Tilt (side view)"); cam(ax, 0, 0, 22, 34, 3.0, alpha=0.12); cam(ax, 0, 0, -22, 34, 3.0, alpha=0.3)
    ax.add_patch(Rectangle((2.9, -1.4), 0.4, 3.0, fc=ORANGE, ec="#7b341e")); arrow(ax, (1.0, 0.5), (1.0, -0.5), rad=-0.5); ax.text(0, -2.1, "rotates vertically in place", ha="center", fontsize=8)
    # 4 push in / pull out
    ax = A[3]; setup(ax, "Push in / Pull out (plan)"); cam(ax, -1.4, 0, 0, 36, 2.6, alpha=0.12); cam(ax, 1.0, 0, 0, 36, 2.6, alpha=0.3); subj(ax, 3.3, 0)
    arrow(ax, (-1.2, -0.6), (0.8, -0.6)); ax.text(0, -1.5, "camera travels toward (push) or away (pull)", ha="center", fontsize=8)
    # 5 zoom
    ax = A[4]; setup(ax, "Zoom (plan)"); cam(ax, 0, 0, 0, 62, 3.2, alpha=0.1); cam(ax, 0, 0, 0, 22, 3.2, alpha=0.35); subj(ax, 3, 0); ax.text(0, -1.9, "same position, focal length changes", ha="center", fontsize=8)
    # 6 dolly zoom
    ax = A[5]; setup(ax, "Dolly zoom (plan)", lim=(-3.4, 4.8, -2.8, 2.8))
    d_far, d_near, sx = 4.5, 2.0, 3.0
    f_far = 2 * math.degrees(math.atan(0.5 / (d_far * 0.5))); f_near = 2 * math.degrees(math.atan(0.5 / (d_near * 0.5)))
    cam(ax, sx - d_far, 0, 0, f_far, 4.6, alpha=0.12); cam(ax, sx - d_near, 0, 0, f_near, 2.5, alpha=0.3); subj(ax, sx, 0, 0.5)
    ax.plot([4.2, 4.2], [-2.2, 2.2], color="#718096", lw=3); ax.text(4.25, 2.3, "background", fontsize=7.5, color="#718096")
    arrow(ax, (-1.2, -1.0), (0.6, -1.0)); ax.text(0.2, -2.4, "move in while zooming out (lens/distance constant)", ha="center", fontsize=7.8)
    # 7 roll
    ax = A[6]; setup(ax, "Roll (front view)", lim=(-2.6, 2.6, -2.2, 2.2))
    for ang, a in ((0, 0.9), (22, 0.35)):
        r = math.radians(ang); R = np.array([[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]])
        pts = np.array([[-1.4, -0.8], [1.4, -0.8], [1.4, 0.8], [-1.4, 0.8]]) @ R.T
        ax.add_patch(Polygon(pts, fc="none", ec="#2b6cb0", lw=2, alpha=a))
    ax.plot([0], [0], "k+", ms=10); arrow(ax, (1.7, 0.2), (1.5, 1.0), rad=0.5); ax.text(0, -1.6, "rotates around the lens axis", ha="center", fontsize=8)
    # 8 tracking / truck
    ax = A[7]; setup(ax, "Tracking / Truck (plan)")
    for y in (-1.3, 0.0, 1.3): cam(ax, 0, y, 0, 30, 1.6, alpha=0.15); 
    cam(ax, 0, 1.3, 0, 30, 1.6, alpha=0.3); arrow(ax, (-0.6, -1.5), (-0.6, 1.6)); subj(ax, 3.2, -1.3); subj(ax, 3.2, 1.3); arrow(ax, (3.9, -1.3), (3.9, 1.3), color=ORANGE)
    ax.text(1.3, -2.3, "camera travels parallel to the subject", ha="center", fontsize=8)
    # 9 arc
    ax = A[8]; setup(ax, "Arc (plan)", lim=(-3.4, 3.4, -3.2, 3.2)); subj(ax, 0, 0, 0.35)
    ax.add_patch(Circle((0, 0), 2.4, fc="none", ec="#a0aec0", ls="--"))
    for a in (-60, -20, 20, 60):
        x, y = 2.4 * math.cos(math.radians(a)), 2.4 * math.sin(math.radians(a)); cam(ax, x, y, a + 180, 26, 1.2, alpha=0.22)
    arrow(ax, (2.1, -1.6), (2.1, 1.6), rad=0.35); ax.text(0, -3.0, "circles the subject, radius constant", ha="center", fontsize=8)
    # 10 boom
    ax = A[9]; setup(ax, "Boom / Crane (side view)"); cam(ax, 0, -1.2, 0, 30, 2.6, alpha=0.15); cam(ax, 0, 1.4, 0, 30, 2.6, alpha=0.3); subj(ax, 3, 0.1); arrow(ax, (-0.6, -1.2), (-0.6, 1.4)); ax.text(0.5, -2.2, "moves vertically (no tilt)", ha="center", fontsize=8)
    # 11 handheld
    ax = A[10]; setup(ax, "Handheld (plan)"); rng = random.Random(4); xs, ys = [0.0], [0.0]
    for _ in range(26): xs.append(xs[-1] * 0.6 + rng.uniform(-0.45, 0.45)); ys.append(ys[-1] * 0.6 + rng.uniform(-0.45, 0.45))
    ax.plot(xs, ys, color="#c05621", lw=1.4); cam(ax, 0, 0, 0, 36, 3.0, alpha=0.15); subj(ax, 3, 0); ax.text(0, -1.5, "small seeded wobble (use sparingly)", ha="center", fontsize=8)
    # 12 bird's eye
    ax = A[11]; setup(ax, "Bird's-eye (side view)", lim=(-3, 3, -0.6, 4.8)); cam(ax, 0, 4.0, -90, 40, 3.9, alpha=0.2); ax.plot([-3, 3], [0, 0], color="#718096", lw=2); subj(ax, 0, 0.2, 0.22); ax.text(0, -0.45, "looks straight down", ha="center", fontsize=8)
    fig.suptitle("Camera moves: what moves, what stays (blue wedge = field of view, dark = end state)", fontsize=12.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96]); fig.savefig(OUT / "camera-moves.png", dpi=DPI); plt.close(fig)
    return {"dolly_zoom_fov_far": round(f_far, 1), "dolly_zoom_fov_near": round(f_near, 1)}

# ============================================================ 5. VFX
def fig_vfx_life():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 6.2), gridspec_kw={"height_ratios": [1.2, 1.4]})
    b, p, f = 0.15, 0.25, 0.60
    t = np.linspace(0, 1, 400)
    y = np.where(t < b, (t / b) ** 1.6, np.where(t < b + p, 1.0 - 0.15 * (t - b) / p, (1 - 0.15) * (1 - (t - b - p) / f) ** 1.5))
    a1.fill_between(t, 0, y, color="#fbd38d", alpha=0.8); a1.plot(t, y, color="#c05621", lw=2)
    for x0, x1, c, l in ((0, b, "#bee3f8", "build 10-20%"), (b, b + p, "#c6f6d5", "peak 20-30%"), (b + p, 1, "#fed7d7", "fade 50-70%")):
        a1.axvspan(x0, x1, color=c, alpha=0.5, zorder=0); a1.text((x0 + x1) / 2, 1.12, l, ha="center", fontsize=9)
    a1.axvspan(0.15, 0.45, ymin=0, ymax=0.06, color=GREEN); a1.text(0.3, -0.16, "audit_fx_style peak window 0.15-0.45", ha="center", fontsize=8, color=GREEN)
    a1.set_xlim(0, 1); a1.set_ylim(-0.25, 1.3); a1.set_yticks([]); a1.set_xlabel("t (fraction of lifetime)"); a1.set_title("Life curve (all styles): build, peak, fade; last frame at most 10% of peak", fontsize=10.5, fontweight="bold")
    layers = [("flash (T/M)", 0.0, 0.10, "#faf089"), ("fireball (F)", 0.0, 0.50, "#f6ad55"), ("shockwave (M)", 0.0, 0.40, "#90cdf4"), ("smoke (F)", 0.30, 1.0, "#a0aec0")]
    for i, (n, s, e, c) in enumerate(layers):
        a2.barh(len(layers) - 1 - i, e - s, left=s, color=c, ec="#2d3748", height=0.6); a2.text(s + 0.01, len(layers) - 1 - i, n, va="center", fontsize=9)
    a2.set_xlim(0, 1); a2.set_yticks([]); a2.set_xlabel("t"); a2.set_title("Layer timeline example: small explosion (cookbook)", fontsize=10.5, fontweight="bold")
    fig.tight_layout(); fig.savefig(OUT / "vfx-life-curve.png", dpi=DPI); plt.close(fig)

def fig_vfx_styles():
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.9), facecolor="#111")
    yy, xx = np.mgrid[-1:1:240j, -1:1:240j]; r = np.sqrt(xx ** 2 + yy ** 2)
    rs = np.random.RandomState(3)
    noise = sum(np.cos(xx * f1 + rs.rand() * 6) * np.cos(yy * f2 + rs.rand() * 6) for f1, f2 in ((4, 5), (9, 7), (15, 13), (23, 19))) / 4
    alpha = np.clip(1 - r + 0.18 * noise, 0, 1) ** 1.4
    img = np.zeros((240, 240, 4)); img[..., 0] = 1.0; img[..., 1] = 0.55 + 0.4 * (1 - r).clip(0, 1); img[..., 2] = 0.1 + 0.6 * (1 - r).clip(0, 1) ** 3; img[..., 3] = alpha
    axes[0].imshow(img, extent=(-1, 1, -1, 1)); axes[0].set_title("Realistic: soft alpha, noise, wide ramp", color="w", fontsize=9)
    s = lambda e0, e1, v: np.clip((v - e0) / (e1 - e0), 0, 1)
    img2 = np.zeros((240, 240, 4)); col = np.array([[0.9, 0.2, 0.1], [1.0, 0.6, 0.1], [1.0, 0.95, 0.5]])
    wob = 1 + 0.12 * np.cos(np.arctan2(yy, xx) * 5)
    for k, rad in enumerate((0.85, 0.6, 0.32)):
        m = 1 - s(rad * wob - 0.05, rad * wob + 0.05, r); img2[m > 0.5, :3] = col[k]; img2[..., 3] = np.maximum(img2[..., 3], m)
    axes[1].imshow(img2, extent=(-1, 1, -1, 1)); axes[1].set_title("Stylized: 3 bands, semi-soft edge", color="w", fontsize=9)
    axes[2].set_facecolor("#111"); ang = np.linspace(0, 2 * math.pi, 17)[:-1]
    for rad, c in ((0.85, "#c53030"), (0.62, "#ed8936"), (0.34, "#faf089")):
        pts = [((rad if i % 2 == 0 else rad * 0.55) * math.cos(a), (rad if i % 2 == 0 else rad * 0.55) * math.sin(a)) for i, a in enumerate(ang)]
        axes[2].add_patch(Polygon(pts, fc=c, ec="none"))
    for a in (0.3, 1.9, 3.4, 4.7):
        axes[2].add_patch(Polygon([(0.95 * math.cos(a), 0.95 * math.sin(a)), (0.75 * math.cos(a + 0.12), 0.75 * math.sin(a + 0.12)), (0.75 * math.cos(a - 0.12), 0.75 * math.sin(a - 0.12))], fc="#fff", ec="none"))
    axes[2].set_xlim(-1, 1); axes[2].set_ylim(-1, 1); axes[2].set_title("Low-poly: hard flat shards, 3-4 colors", color="w", fontsize=9)
    axes[3].set_xlim(0, 12); axes[3].set_ylim(0, 12); pal = ["#c53030", "#ed8936", "#faf089"]
    for i in range(12):
        for j in range(12):
            d = math.hypot(i - 5.5, j - 5.5)
            if d < 5.4 and (d < 4.2 or (i + j) % 2 == 0): axes[3].add_patch(Rectangle((i, j), 1, 1, fc=pal[0 if d > 3.6 else 1 if d > 1.8 else 2], ec="none"))
    axes[3].set_title("Voxel: grid-aligned cubes, game palette", color="w", fontsize=9)
    for ax in axes: ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); fig.savefig(OUT / "vfx-style-compare.png", dpi=DPI, facecolor="#111"); plt.close(fig)

# ============================================================ 6. pipeline
def fig_pipeline():
    fig, ax = plt.subplots(figsize=(15, 7.4)); ax.set_xlim(0, 16); ax.set_ylim(0, 8.4); ax.axis("off")
    def box(x, y, w, h, t, fc="#ebf8ff", ec="#2b6cb0", fs=9, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec, lw=1.5))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal")
    def arr(a, b, c="#2d3748", ls="-", rad=0.0): ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=c, lw=1.6, ls=ls, connectionstyle=f"arc3,rad={rad}"))
    box(0.3, 7.0, 7.4, 1.0, "/blender router + state.md\nclassify every message, one stage per turn, invalidate STALE", "#fefcbf", "#b7791f", 10, True)
    box(8.3, 7.0, 4.2, 1.0, "blender-diagnose\nany question -> check -> fix -> route", "#e9d8fd", "#6b46c1", 9.5)
    box(13.0, 7.0, 2.7, 1.0, "blender-setup\n(once per project)", "#e2e8f0", "#4a5568", 9.5)
    names = ["ref", "model", "hands", "topology", "uv-bake", "material", "rig", "animate"]
    xs = [0.3 + i * 1.95 for i in range(len(names))]
    for x, n in zip(xs, names): box(x, 5.0, 1.65, 0.95, n, "#ebf8ff" if n != "topology" else "#c6f6d5", "#2b6cb0" if n != "topology" else "#2f855a", 10, n == "topology")
    for i in range(len(names) - 1): arr((xs[i] + 1.65, 5.47), (xs[i + 1], 5.47))
    ax.text(0.3, 6.25, "asset chain (mode prop / char / env ...)", fontsize=9, color=GREY)
    tx = xs[3] + 0.82
    box(xs[3] - 1.1, 2.9, 2.2, 0.9, "topology-fix\nmap -> repair -> verify", "#fed7d7", "#c53030", 9)
    box(xs[3] + 1.4, 2.9, 1.9, 0.9, "retopo\nhigh -> low", "#fed7d7", "#c53030", 9)
    arr((tx - 0.3, 5.0), (xs[3] - 0.3, 3.8), c=RED, ls="--"); arr((tx + 0.3, 5.0), (xs[3] + 2.3, 3.8), c=RED, ls="--"); ax.text(tx + 1.2, 4.35, "fail / messy mesh", fontsize=8, color=RED)
    box(0.3, 2.9, 3.4, 0.9, "vfx (+mesh, flipbook,\ntexture, sim) | style axis", "#feebc8", "#c05621", 9)
    box(0.3, 1.5, 2.2, 0.9, "camera\nshots, moves, showcase", "#feebc8", "#c05621", 9)
    box(8.4, 1.0, 2.3, 1.0, "qa\naudits + verdict", "#c6f6d5", "#2f855a", 10, True)
    box(12.0, 1.0, 2.3, 1.0, "export\nengine profile", "#c6f6d5", "#2f855a", 10, True)
    arr((10.7, 1.5), (12.0, 1.5), c=GREEN); ax.text(11.35, 1.75, "SHIP", fontsize=9, color=GREEN, ha="center")
    arr((9.4, 2.0), (xs[3] + 1.5, 2.9), c=RED, ls="--", rad=-0.2); ax.text(8.0, 2.55, "NO-SHIP -> fix skill", fontsize=8.5, color=RED)
    for src in ((3.7, 3.2), (2.5, 1.9), (xs[7] + 0.8, 5.0)): arr(src, (8.4, 1.5), c="#718096", rad=0.0)
    ax.text(0.3, 0.45, "side question: push stage -> answer with the matching skill -> BACK TO stage.  Change at stage S marks later stages STALE (re-audit).", fontsize=9, color=GREY)
    fig.tight_layout(); fig.savefig(OUT / "pipeline.png", dpi=DPI); plt.close(fig)

if __name__ == "__main__":
    res = fig_transitions()
    bad = [r for r in res if not r["ok"]]
    for r in res: print(r["pattern"], "ok" if r["ok"] else r["errors"], "| poles3", r["poles_3"], "poles5", r["poles_5"], "| min edge ratio", r["min_edge_ratio"])
    fig_finger_tiers(); fig_hand_layout(); fig_joint_loops(); fig_rig_zones()
    print("camera:", fig_camera_moves()); fig_vfx_life(); fig_vfx_styles(); fig_pipeline()
    for name, t in TIERS.items(): print("tier", name, tier_numbers(t))
    problems = check_hand_doc()
    for p in problems: print("DOC MISMATCH:", p)
    if bad or problems: sys.exit(1)
    print("figures OK:", sorted(p.name for p in OUT.glob("*.png")))
