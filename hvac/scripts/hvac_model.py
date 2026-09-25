#!/usr/bin/env python3
r"""hvac_model.py - the HVAC drawn INSIDE THE HOUSE for the RVM viewer: every outdoor unit, head, air handler,
ERV, register, grille, fan and cap as a box where it goes, every line set, duct and vent as a run coloured by
system, in the ELECTRICAL skill's wall visual (the plumbing skill does the same).

    python hvac_model.py hvac_takeoff.json [--job job.json] [--interior interior.json] [--out <slug>_app.json]

The house is the electrical skill's GENERATED wall set (`elec_route.WallNet`): every edge of every kept room
polygon, the two faces of a shared wall merged onto one centreline - drawn full height and translucent, no
roof, no windows, so a line set inside a wall or a duct in a joist bay reads through it.

Groups (the viewer draws any group as a mesh, keyed by `g`):
    floors / walls   the house (painted first)
    equipment        outdoor units on their stands, wall heads, air handlers / ducted units, the ERV
    terminals        supply registers, returns, ERV grilles and hoods, bath / whole-house fans, caps
    hvac             one object per run, named "<SYSTEM> <size> - <note>", coloured by system:
                       refrigerant copper, condensate pale cyan, supply trunk / branch blue, return green,
                       bath exhaust violet, ERV supply teal, ERV exhaust orange, ERV outdoor air grey-teal,
                       range hood dark grey, dryer brown
                     a run is a square-section box of its real size along each segment

Metres, Y up, plan x east, plan y south - the RVM frame (flooring's floormodel.Mesh), so it drops onto the card.
The legend is in the payload (`hvac.legend`) for the viewer and the renderer.
"""
import argparse, json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hvac_common as C
import hvac_load as HL

C.utf8()
C.sibling('electrical'); C.sibling('flooring')
import elec_route as ER                 # the electrical skill's wall generator
from floormodel import Mesh

SYS_COL = {'refrigerant': '#b87333', 'condensate': '#7fd3e6', 'trunk': '#1f4fa0', 'supply': '#2f6fd0', 'return': '#3a9a5a',
           'exhaust': '#8a5ac0', 'erv_supply': '#159a9a', 'erv_exhaust': '#d07a20', 'erv_outdoor': '#4a7f86', 'hood': '#4a4a4a', 'dryer': '#8a6040'}
SYS_LABEL = {'refrigerant': 'line set', 'condensate': 'condensate', 'trunk': 'supply trunk', 'supply': 'supply branch', 'return': 'return',
             'exhaust': 'bath / whole-house exhaust', 'erv_supply': 'ERV supply', 'erv_exhaust': 'ERV exhaust', 'erv_outdoor': 'ERV outdoor air / exhaust',
             'hood': 'range hood', 'dryer': 'dryer vent'}
EQ_COL = {'outdoor': '#5f6b73', 'head': '#c3d0d8', 'ahu': '#6f7c85', 'erv': '#3f8f8f', 'register': '#2f6fd0', 'return': '#3a9a5a',
          'grille': '#159a9a', 'hood': '#4a7f86', 'fan': '#8a5ac0', 'hood_cap': '#4a4a4a', 'dryer_cap': '#8a6040'}
FLOOR_COL = '#cdd3d8'
WALL_COL = '#8f9aa3'
WALL_THK_FT = 0.42


def run_size_ft(r):
    """the drawn section of a run: ducts at their diameter, line sets at the bundle, condensate thin"""
    s = r['system']
    if s == 'refrigerant':
        return 0.16
    if s == 'condensate':
        return 0.08
    try:
        return max(0.25, float(r['size']) / 12.0)
    except Exception:
        return 0.3


def segment(M, name, g, colour, a, b, w):
    ax, ay, az = a; bx, by, bz = b
    if math.dist(a, b) < 0.02:
        return
    if abs(ax - bx) < 1e-6 and abs(ay - by) < 1e-6:
        M.box(name, g, colour, ax - w / 2, ax + w / 2, ay - w / 2, ay + w / 2, min(az, bz), max(az, bz))
        return
    if abs(az - bz) < 1e-6:
        M.strip(name, g, colour, (ax, ay), (bx, by), w, az - w / 2, az + w / 2)
        return
    # sloped (a cap through the roof, a line set out to the unit): two steps
    mid = ((ax + bx) / 2, (ay + by) / 2, (az + bz) / 2)
    M.strip(name, g, colour, (ax, ay), (mid[0], mid[1]), w, min(az, mid[2]) - w / 2, max(az, mid[2]) + w / 2)
    M.strip(name, g, colour, (mid[0], mid[1]), (bx, by), w, min(mid[2], bz) - w / 2, max(mid[2], bz) + w / 2)


def oriented_box(M, name, g, colour, pos, n, along, deep, z0, z1):
    """a box `along` ft wide parallel to the wall whose outward normal is n, `deep` ft off it, centred on pos"""
    if not n:
        M.box(name, g, colour, pos[0] - along / 2, pos[0] + along / 2, pos[1] - deep / 2, pos[1] + deep / 2, z0, z1)
        return
    tx, ty = -n[1], n[0]
    a = (pos[0] - tx * along / 2, pos[1] - ty * along / 2)
    b = (pos[0] + tx * along / 2, pos[1] + ty * along / 2)
    M.strip(name, g, colour, a, b, deep, z0, z1)


def shell(M, I, storeys):
    zof = {s['name']: float(s.get('z', 0.0)) for s in storeys}
    plate = {s['name']: float(s.get('plate', 9.0)) for s in storeys}
    for r in I.get('rooms', []):
        if r.get('skip') or len(r.get('poly') or []) < 3:
            continue
        z = zof.get(r.get('storey'), float(r.get('z', 0.0)))
        M.slab(f"floor {r.get('storey', 'main')} {r.get('name') or r.get('key')}", 'floors', FLOOR_COL, [tuple(p) for p in r['poly']], z - 0.08, z)
    net = ER.WallNet(I)
    walls = net.wall_segments()
    n = 0
    for st, segs in walls.items():
        z = zof.get(st, 0.0)
        for a, b in segs:
            M.strip(f'wall {st}', 'walls', WALL_COL, a, b, WALL_THK_FT, z, z + plate.get(st, 9.0))
            n += 1
    return dict(source='electrical skill (elec_route.WallNet) - every room-polygon edge, shared faces merged to one centreline',
                segments=n, by_storey={st: len(v) for st, v in walls.items()}, height='full plate', thick_in=round(WALL_THK_FT * 12, 1))


def build(T, I, job):
    M = Mesh()
    storeys = sorted(I['storeys'], key=lambda s: s['z'])
    plate = {s['name']: float(s.get('plate', 9.0)) for s in storeys}
    info = dict(walls=shell(M, I, storeys))
    for it in T['items']:
        k, p, z, st = it['kind'], it['pos'], it['z'], it.get('storey')
        col = EQ_COL.get(k, '#999999')
        nm = f"{k.upper()} {it.get('note') or it.get('part')}"
        if k == 'outdoor':
            big = (it.get('kbtuh') or 24) >= 36
            oriented_box(M, nm, 'equipment', col, p, it.get('n'), 3.3 if big else 2.8, 1.3, 1.0, 1.0 + (4.4 if big else 2.6))
            oriented_box(M, nm + ' stand', 'equipment', '#3a3f44', p, it.get('n'), 3.0, 1.2, 0.0, 1.0)
        elif k == 'head':
            oriented_box(M, nm, 'equipment', col, (p[0], p[1]), it.get('n'), 2.7 if (it.get('kbtuh') or 9) <= 12 else 3.4, 0.75, z - 0.95, z)
        elif k == 'ahu':
            if 'duin' in (it.get('part') or '') and st and z > 1.0:
                zc = z + plate.get(st, 9.0) - 1.1
                M.box(nm, 'equipment', col, p[0] - 1.6, p[0] + 1.6, p[1] - 1.1, p[1] + 1.1, zc, zc + 0.9)
            elif 'duin' in (it.get('part') or ''):
                zc = z + plate.get(st, 9.0) - 1.1
                M.box(nm, 'equipment', col, p[0] - 1.6, p[0] + 1.6, p[1] - 1.1, p[1] + 1.1, zc, zc + 0.9)
            else:
                M.box(nm, 'equipment', col, p[0] - 1.0, p[0] + 1.0, p[1] - 1.0, p[1] + 1.0, z, z + 4.5)
        elif k == 'erv':
            M.box(nm, 'equipment', col, p[0] - 1.3, p[0] + 1.3, p[1] - 0.8, p[1] + 0.8, z, z + 1.6)
        elif k == 'register':
            M.box(nm, 'terminals', col, p[0] - 0.45, p[0] + 0.45, p[1] - 0.45, p[1] + 0.45, z, z + 0.08)
        elif k == 'return':
            M.box(nm, 'terminals', col, p[0] - 0.85, p[0] + 0.85, p[1] - 0.7, p[1] + 0.7, z - 0.05, z + 0.05)
        elif k == 'grille':
            c2 = EQ_COL['grille'] if it.get('kind2') == 'erv_supply' else SYS_COL['erv_exhaust']
            M.box(nm, 'terminals', c2, p[0] - 0.3, p[0] + 0.3, p[1] - 0.3, p[1] + 0.3, z - 0.05, z + 0.05)
        elif k == 'fan':
            M.box(nm, 'terminals', col, p[0] - 0.45, p[0] + 0.45, p[1] - 0.45, p[1] + 0.45, z - 0.4, z)
        else:
            M.box(nm, 'terminals', col, p[0] - 0.35, p[0] + 0.35, p[1] - 0.35, p[1] + 0.35, z - 0.35, z + 0.35)
    for r in T['runs']:
        col = SYS_COL.get(r['system'], '#ff00ff')
        w = run_size_ft(r)
        name = f"{SYS_LABEL.get(r['system'], r['system']).upper()} {r['size']} - {r['note']}"
        pts = [tuple(p) for p in r['pts']]
        for i in range(len(pts) - 1):
            segment(M, name, 'hvac', col, pts[i], pts[i + 1], w)
    return M, info


def payload(T, M, info):
    objs = M.objs
    xs = [v for o in objs for v in o['v'][0::3]]; zs = [v for o in objs for v in o['v'][2::3]]
    return dict(job=T.get('slug'), address=T.get('address'), permit=T.get('permit'), system='hvac', unit='m',
                objects=objs, parts=[], planes=[], roof_sf=0, tris=sum(len(o['f']) // 3 for o in objs),
                hvac=dict(legend=[dict(system=k, label=SYS_LABEL[k], hex=SYS_COL[k]) for k in SYS_COL],
                          equipment_legend=[dict(kind=k, hex=v) for k, v in EQ_COL.items()],
                          totals=T['totals'], spec={k: T['spec'][k] for k in ('kind', 'foundation', 'lineset_route', 'ducts', 'ventilation')},
                          checks=T['checks']),
                framing=info, bbox=dict(x=[min(xs), max(xs)], z=[min(zs), max(zs)]))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('takeoff'); ap.add_argument('--interior', default=None); ap.add_argument('--out', default=None); ap.add_argument('--job', default=None)
    a = ap.parse_args()
    T = json.load(open(a.takeoff, encoding='utf-8'))
    d = os.path.dirname(os.path.abspath(a.takeoff))
    jp = a.job or os.path.join(d, 'job.json')
    job = C.load(jp)
    I = C.load(a.interior or C.resolve(job.get('interior', 'interior.json'), d))
    if job.get('storey_shift'):
        I = HL.shift_interior(I, job['storey_shift'])      # the same frame the takeoff was measured in
    M, info = build(T, I, job)
    P = payload(T, M, info)
    out = a.out or os.path.join(d, f"{T.get('slug')}_app.json")
    json.dump(P, open(out, 'w', encoding='utf-8'))
    from collections import Counter
    w = info['walls']
    print(f"{out}: {len(P['objects'])} objects {dict(Counter(o['g'] for o in P['objects']))}, {P['tris']} tris; "
          f"walls {w['segments']} generated centrelines {w['by_storey']}")
