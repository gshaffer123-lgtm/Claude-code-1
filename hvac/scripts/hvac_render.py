#!/usr/bin/env python3
r"""hvac_render.py - draw the HVAC model to PNG. No browser, no Blender, no WebGL.

    python hvac_render.py <slug>_app.json --out shot.png [--yaw 35] [--pitch 55] [--groups floors,walls,equipment,terminals,hvac]

The plumbing skill's painter's renderer in the electrical skill's look: translucent grey walls at 0.42,
floors at 0.5, the wall outlines stroked, then the equipment, the terminals and the runs painted LAST and
opaque - an HVAC drawing is read as an overlay, and a duct must never hide behind the wall in front of it.
Alpha is blended in batches (one addWeighted per alpha group), not per triangle.

Always render two yaws and the plan view, and LOOK at all three before believing a run.
"""
import argparse, json, math, os, sys
import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hvac_model import SYS_COL, SYS_LABEL, EQ_COL

LEGEND = [(SYS_LABEL[k], SYS_COL[k]) for k in SYS_COL] + [('outdoor unit', EQ_COL['outdoor']), ('head', EQ_COL['head']), ('air handler', EQ_COL['ahu']),
                                                          ('ERV', EQ_COL['erv']), ('wall', '#8f9aa3'), ('floor', '#cdd3d8')]
ORDER = {'floors': 0, 'walls': 1, 'equipment': 3, 'terminals': 3, 'hvac': 4}
ALPHA = {'floors': 0.5, 'walls': 0.42, 'equipment': 1.0, 'terminals': 1.0, 'hvac': 1.0}


def hex2bgr(h):
    h = str(h).lstrip('#')
    return (int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16))


def render(payload, out, yaw=35.0, pitch=55.0, W=1800, H=1080, groups=None, no_edges=False):
    objs = payload['objects']
    yaw, pitch = math.radians(yaw), math.radians(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)

    def proj(v):
        x, y, z = v
        xr = x * cy - z * sy
        zr = x * sy + z * cy
        return xr, -(y * cp + zr * sp), -(zr * cp - y * sp)

    tris, edges = [], []
    light = np.array([0.4, 0.8, 0.45]); light /= np.linalg.norm(light)
    for o in objs:
        g = o.get('g')
        if groups and g not in groups:
            continue
        V = np.array(o['v'], dtype=np.float64).reshape(-1, 3)
        F = np.array(o['f'], dtype=np.int64).reshape(-1, 3)
        col = np.array(hex2bgr(o['c']), dtype=np.float64)
        a = ALPHA.get(g, 1.0)
        P = np.array([proj(v) for v in V])
        if g == 'walls' and len(V) == 8:
            for u, v_ in ((4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)):
                edges.append((P[u][:2], P[v_][:2]))
        for i, j, k in F:
            n = np.cross(V[j] - V[i], V[k] - V[i])
            L = np.linalg.norm(n)
            if L < 1e-9:
                continue
            n = n / L
            shade = 0.55 + 0.45 * max(0.0, float(np.dot(n, light)))
            if abs(n[1]) > 0.9:
                shade = 0.8 + 0.2 * max(0.0, float(np.dot(n, light)))
            d = (P[i][2] + P[j][2] + P[k][2]) / 3
            tris.append((ORDER.get(g, 3), d, (P[i][:2], P[j][:2], P[k][:2]), col * shade, a))
    if not tris:
        sys.exit('nothing to draw')
    tris.sort(key=lambda t: (t[0], t[1]))
    pts = np.array([p for t in tris for p in t[2]])
    x0, y0 = pts[:, 0].min(), pts[:, 1].min()
    x1, y1 = pts[:, 0].max(), pts[:, 1].max()
    s = min((W - 60) / max(x1 - x0, 1e-6), (H - 190) / max(y1 - y0, 1e-6))
    ox = (W - (x1 - x0) * s) / 2 - x0 * s
    oy = (H - (y1 - y0) * s) / 2 - y0 * s + 40
    img = np.full((H, W, 3), 245, np.uint8)

    def paint(sub):
        i = 0; n = len(sub)
        while i < n:
            al = sub[i][4]
            j = i
            while j < n and sub[j][4] == al:
                j += 1
            target = img if al >= 0.999 else img.copy()
            for _o, _d, (a_, b_, c_), col, _a in sub[i:j]:
                poly = np.array([[a_[0] * s + ox, a_[1] * s + oy], [b_[0] * s + ox, b_[1] * s + oy], [c_[0] * s + ox, c_[1] * s + oy]], np.int32)
                cv2.fillPoly(target, [poly], tuple(int(min(255, max(0, v))) for v in col), lineType=cv2.LINE_AA if al >= 0.999 else cv2.LINE_8)
            if al < 0.999:
                cv2.addWeighted(target, al, img, 1 - al, 0, img)
            i = j

    paint([t for t in tris if t[0] <= 1])
    if edges and not no_edges:
        for a_, b_ in edges:
            cv2.line(img, (int(a_[0] * s + ox), int(a_[1] * s + oy)), (int(b_[0] * s + ox), int(b_[1] * s + oy)), (146, 152, 158), 1, cv2.LINE_AA)
    paint([t for t in tris if t[0] > 1])

    cv2.putText(img, payload.get('address') or payload.get('job', ''), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2, cv2.LINE_AA)
    hv = payload.get('hvac') or {}
    t = hv.get('totals') or {}
    spc = hv.get('spec') or {}
    sub = (f"{spc.get('kind', '')}  ·  heat {t.get('heat_btuh', 0):,} Btuh  ·  {t.get('outdoor_units', 0)} outdoor  ·  {t.get('heads', 0)} heads  ·  "
           f"{t.get('indoor_ducted', 0)} ducted units  ·  {t.get('registers', 0)} registers  ·  line sets {t.get('lineset_ft', 0):,} ft  ·  "
           f"duct {t.get('duct_ft', 0):,} ft  ·  vent {t.get('vent_ft', 0):,} ft  ·  {t.get('codes', 0)} code / {t.get('practice', 0)} practice / {t.get('data', 0)} data")
    cv2.putText(img, sub, (20, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (70, 70, 70), 1, cv2.LINE_AA)
    fr = (payload.get('framing') or {}).get('walls') or {}
    if fr:
        cv2.putText(img, f"walls generated by the electrical skill's WallNet: {fr.get('segments', 0)} centrelines {fr.get('by_storey', {})}, "
                         f"{fr.get('thick_in', 5)} in at {fr.get('height', 'full plate')} - no roof, no windows; line sets {spc.get('lineset_route', '')}",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (110, 100, 80), 1, cv2.LINE_AA)
    y = H - 20; x = 20
    for label, hexc in LEGEND:
        cv2.rectangle(img, (x, y - 14), (x + 20, y), hex2bgr(hexc), -1)
        cv2.putText(img, label, (x + 26, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (40, 40, 40), 1, cv2.LINE_AA)
        x += 34 + 9 * len(label)
        if x > W - 220:
            x = 20; y -= 24
    cv2.imwrite(out, img)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('payload'); ap.add_argument('--out', required=True)
    ap.add_argument('--yaw', type=float, default=35); ap.add_argument('--pitch', type=float, default=55)
    ap.add_argument('--w', type=int, default=1800); ap.add_argument('--h', type=int, default=1080)
    ap.add_argument('--groups', default=None); ap.add_argument('--no-edges', action='store_true')
    a = ap.parse_args()
    p = json.load(open(a.payload, encoding='utf-8'))
    render(p, a.out, a.yaw, a.pitch, a.w, a.h, set(a.groups.split(',')) if a.groups else None, a.no_edges)
    print('wrote', a.out)
