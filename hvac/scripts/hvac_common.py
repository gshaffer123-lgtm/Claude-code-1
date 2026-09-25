#!/usr/bin/env python3
r"""hvac_common.py - the small things every HVAC script shares: where the sibling skills are, how a job's
paths resolve, and the plan-frame geometry (x east, y SOUTH, feet - the RVM frame every model uses).

Sibling skills this one reads (never writes):
    finish      interior.json (rooms, wall runs, doors, windows, storeys) and rooms_p<N>.json (tracer footprints)
    electrical  elec_route.WallNet (the generated wall network + Dijkstra) - line sets and exhaust ducts route on it
    flooring    floormodel.Mesh (the RVM viewer payload builder)
    bidding     references/formula.md + scripts/bidcalc.py (the money model)

They are found at $CLAUDE_SKILLS, else next to this skill (~/.claude/skills/hvac -> ~/.claude/skills), else
~/.claude/skills.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)


def skills_dir():
    for c in (os.environ.get('CLAUDE_SKILLS'), os.path.dirname(SKILL), os.path.expanduser('~/.claude/skills')):
        if c and os.path.exists(os.path.join(c, 'finish', 'scripts')):
            return c
    return os.path.dirname(SKILL)


def sibling(skill, sub='scripts'):
    p = os.path.join(skills_dir(), skill, sub)
    if p not in sys.path:
        sys.path.insert(0, p)
    return p


def resolve(path, job_dir):
    """a job.json path: as written (relative to the job folder), else - for a sibling-skill path written the way the
    electrical jobs write it ('../../../finish/jobs/<h>/interior.json') - under skills_dir()"""
    if not path:
        return None
    cands = [path if os.path.isabs(path) else os.path.normpath(os.path.join(job_dir, path))]
    rel = path.replace('\\', '/')
    while rel.startswith('../'):
        rel = rel[3:]
    cands.append(os.path.join(skills_dir(), rel))
    for c in cands:
        if os.path.exists(c):
            return c
    return cands[0]


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def utf8():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


# ------------------------------------------------------------------ geometry (plan ft, x east, y south)
def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def poly_area(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2


def centroid(P):
    a = 0.0; cx = cy = 0.0
    n = len(P)
    for i in range(n):
        x0, y0 = P[i]; x1, y1 = P[(i + 1) % n]
        c = x0 * y1 - x1 * y0
        a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
    if abs(a) < 1e-9:
        return (sum(p[0] for p in P) / n, sum(p[1] for p in P) / n)
    return (cx / (3 * a), cy / (3 * a))


COMPASS8 = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']


def facing(nx, ny, north_deg=0.0):
    """the compass direction an outward normal (plan frame: +x east, +y SOUTH on a north-up sheet) faces.
    north_deg = where true north points on the page, clockwise from page-up (0 = the sheet is north-up)."""
    bearing = (math.degrees(math.atan2(nx, -ny)) - north_deg) % 360.0
    return COMPASS8[int(((bearing + 22.5) % 360) // 45)], bearing


def lpath(a, b, first='x'):
    """an L between two plan points (ducts run in joist bays and chases, not through studs)"""
    if first == 'x':
        mid = (b[0], a[1])
    else:
        mid = (a[0], b[1])
    pts = [tuple(a), mid, tuple(b)]
    out = [pts[0]]
    for p in pts[1:]:
        if dist(p, out[-1]) > 1e-6:
            out.append(p)
    return out


def plen(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
