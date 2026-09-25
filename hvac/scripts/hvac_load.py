#!/usr/bin/env python3
r"""hvac_load.py - the house's heat loss and heat gain, ROOM BY ROOM, off the traced interior.

    python hvac_load.py job.json [--interior interior.json] [--scan hvac_scan.json] [--out hvac_loads.json]

Every other interior trade counts things that are drawn. HVAC has to count something that is not: how
much heat each room loses at the design temperature. That number sizes every head, every register, every
duct and the outdoor unit, so it is built the way ACCA Manual J builds it - component by component, per
room - off the same traced interior the electrical and plumbing skills use (finish/interior.py):

  1. EXPOSURE per room. A room edge is an EXTERIOR wall when a probe 1.5 ft and 4 ft outside it lands in
     no kept room of that storey (the garage and the perimeter slivers are outside - a wall to the garage
     loses heat like an outside wall, which is conservative and said so). Its facing (N/E/S/W ...) comes
     from the outward normal and job.json `north_deg`. The CEILING is exposed where no room of the storey
     above covers the room (a single-storey wing, the whole top floor); the FLOOR where no room of the
     storey below carries it (the crawl space under the main floor, the garage under a bonus room).
  2. OPENINGS. The traced windows (interior.json, re-attached to their rooms) - unless the plan's window
     schedule says there is more glass (hvac_scan.json `openings`) or job.json types it: then the extra is
     spread over the habitable rooms by exterior wall length, and the report says which total was used.
  3. HEATING, per room (ACCA Manual J 8th edition as NREL's open-source implementation codes it):
     sum(U x A) x dT for walls, windows, doors and ceiling; the floor over a VENTED crawl at 0.76 x dT (MJ8's
     partition temperature difference); a slab edge at F x perimeter x dT;
     + infiltration 1.1 x ICFM x dT, ICFM = 0.05488 x Q50 x sqrt(0.015 N dT + Cw 15^2) (MJ8 blower-door method),
       shared by exterior wall area;
     + the duct loss factor when ducts run outside the envelope (vented crawl +10 %, the WSU sheet's x 1.10).
     Each dwelling unit adds its VENTILATION: the WA rate Qv = (0.01 x CFA + 7.5 x (bedrooms + 1)) x Csystem
     (1.5 for one exhaust fan, 1.0 for an ERV ducted to every room). An exhaust fan and the infiltration it
     depressurises combine as (ICFM^1.5 + Qv^1.5)^0.67 (MJ8); an ERV / HRV pays 1.1 x Qv x (1 - SRE) x dT.
  4. COOLING, per room (MJ8 heat-transfer multipliers at 48.8 N): glass at its facing's solar multiplier (SHGC
     0.28, no drapes - the 'peak' procedure MJ8 asks for on zoned and ductless systems) plus U x dT; walls,
     ceilings and doors at MJ8's cooling temperature differences (walls are ~0 in Bellingham); people (bedrooms
     + 1, 230 Btuh each) in the bedrooms and living spaces; 2,400 Btuh of appliances (1,200 in the kitchen).
  5. TWO CROSS-CHECKS the permit office uses: the WSU "Simple Heating System Size" sheet (dT x (UA + 0.018 x
     0.6 ACH x volume), x 1.10 with ducts outside) and Btuh per square foot against the band a new WSEC-2021
     house lands in (7-12, flagged outside 5-18). When the traced area is short of the plan's heated area, the
     area-driven components are scaled to the plan's figure and the report prints both. Where the design town
     has a Manual J 99 % temperature as well as the code's Table RC-1 one, both loads are printed.

The U-factors are the plan's R-values through `hvac_parts.R_TO_U`, else the 2021 WSEC prescriptive
defaults; the design temperatures are `hvac_parts.DESIGN` by town. Every one of them is printed back.
"""
import argparse, json, os, re, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hvac_common as C
import hvac_parts as HP

C.utf8()

HABITABLE = {'living', 'kitchen', 'dining', 'bedroom', 'office', 'den', 'media', 'circulation', 'stair'}
WET = {'bath', 'powder'}
INTERIOR_SKIP_WORDS = re.compile(r'OPEN\s+TO\s+BELOW|STAIR|LANDING|CHASE|HALL|CLOS|MECH|HEADROOM', re.I)


def use_of(r):
    u = (r.get('use') or '').lower()
    n = (r.get('name') or '').upper()
    if u:
        return u
    if re.search(r'BED|BDRM|PRIMARY|MASTER|MSTR', n):
        return 'bedroom'
    if re.search(r'BATH|W\.?C\.?|SHOWER|VANITY|ENSUITE', n):
        return 'bath'
    if re.search(r'KITCHEN', n):
        return 'kitchen'
    if re.search(r'LIVING|GREAT|FAMILY|DINING|DEN|YOGA|MEDIA|GAME', n):
        return 'living'
    if re.search(r'CLOS|W\.?I\.?C|PANTRY|LINEN|STOR', n):
        return 'closet'
    return 'circulation'


def unit_of(r, units):
    """which dwelling unit a room belongs to: job.json hvac.units[] by the room centroid (x_min / x_max / y_min / y_max)"""
    if not units:
        return 'house'
    cx, cy = C.centroid([tuple(p) for p in r['poly']])
    for u in units:
        if (u.get('x_min') is None or cx >= u['x_min']) and (u.get('x_max') is None or cx < u['x_max']) and \
           (u.get('y_min') is None or cy >= u['y_min']) and (u.get('y_max') is None or cy < u['y_max']):
            return u.get('name', 'house')
    return units[0].get('name', 'house')


def shift_interior(I, shift):
    """a copy of interior.json with each named storey moved by (dx, dy) ft - job.json storey_shift"""
    import copy
    I = copy.deepcopy(I)
    def mv(p, dx, dy):
        return [p[0] + dx, p[1] + dy]
    for coll in ('rooms', 'windows', 'extdoors', 'doors', 'iwalls', 'ewalls', 'cabruns'):
        for o in I.get(coll, []):
            s = o.get('storey')
            if s not in shift:
                continue
            dx, dy = shift[s]
            for k in ('poly',):
                if o.get(k):
                    o[k] = [mv(p, dx, dy) for p in o[k]]
            for k in ('seg',):
                if o.get(k):
                    o[k] = [mv(p, dx, dy) for p in o[k]]
            for k in ('mid', 'a', 'b', 'center'):
                if o.get(k) and isinstance(o[k], list) and len(o[k]) == 2 and not isinstance(o[k][0], list):
                    o[k] = mv(o[k], dx, dy)
    return I


def design(job, scan=None):
    """design temperatures for the job's town: job.json hvac.design wins, else the town in the address"""
    H = job.get('hvac') or {}
    d = H.get('design') or {}
    if d.get('heat') is not None:
        return dict(heat=d['heat'], cool=d.get('cool', 80), wb=d.get('wb', 64), range=d.get('range', 18), grains=d.get('grains', 4),
                    mj8_heat=d.get('mj8_heat'), town=d.get('town', 'job.json'), src=d.get('_src') or 'job.json hvac.design')
    addr = (job.get('address') or '').lower()
    for town in sorted(HP.DESIGN, key=len, reverse=True):
        if town in addr:
            t = HP.DESIGN[town]
            return dict(town=town, **t)
    t = HP.DESIGN['bellingham']
    return dict(town='bellingham (default - the address names no listed town)', **t)


def wall_u(spec):
    if spec is None:
        return HP.U_DEFAULT['wall'], 'WSEC 2021 prescriptive default U-0.056'
    s = str(spec).upper().replace(' ', '')
    m = re.match(r'R-?(\d+)(?:\+(\d+(?:\.\d)?))?', s)
    if not m:
        return HP.U_DEFAULT['wall'], f'"{spec}" not understood - default U-0.056'
    key = f"R-{m.group(1)}" + (f"+{m.group(2)}" if m.group(2) else '')
    if key in HP.R_TO_U['wall']:
        return HP.R_TO_U['wall'][key], f'{key} -> U-{HP.R_TO_U["wall"][key]}'
    # parallel-path estimate: cavity at 23 % framing + continuous insulation in series
    cav = float(m.group(1)); ci = float(m.group(2) or 0)
    r_cav = 1 / (0.77 / (cav + 2.0) + 0.23 / (5.5 * 1.25 + 2.0))
    u = 1 / (r_cav + ci)
    return round(u, 3), f'{key} -> U-{u:.3f} (parallel-path estimate)'


def r_u(kind, r):
    if r is None:
        return HP.U_DEFAULT[kind], f'WSEC 2021 prescriptive default U-{HP.U_DEFAULT[kind]}'
    tbl = HP.R_TO_U.get(kind, {})
    best = min(tbl, key=lambda k: abs(k - r)) if tbl else None
    if best is not None and abs(best - r) <= 3:
        return tbl[best], f'R-{r:g} -> U-{tbl[best]}'
    u = 1 / (r * 1.05 + 1.5)
    return round(u, 3), f'R-{r:g} -> U-{u:.3f} (estimate)'


class Loads:
    def __init__(self, job, I, scan=None, job_dir='.'):
        from shapely.geometry import Polygon, Point, LineString
        from shapely.ops import unary_union
        self.P, self.Pt, self.LS, self.uu = Polygon, Point, LineString, unary_union
        self.job, self.I, self.scan, self.job_dir = job, I, scan or {}, job_dir
        self.H = job.get('hvac') or {}
        self.notes, self.warn = [], []
        self.storeys = sorted(I['storeys'], key=lambda s: s['z'])
        shift = job.get('storey_shift') or {}
        if shift:
            I = shift_interior(I, shift)
            self.I = I
            self.notes.append('storey shift applied (job.json storey_shift): ' + ', '.join(f'{k} {v}' for k, v in shift.items()))
        excl = [str(x).upper() for x in (self.H.get('exclude_rooms') or [])]
        def excluded(r):
            return (r.get('key') or '').upper() in excl or (r.get('name') or '').upper() in excl
        self.rooms = [r for r in I['rooms'] if not r.get('skip') and not excluded(r) and len(r.get('poly') or []) >= 3]
        self.skipped = [r for r in I['rooms'] if (r.get('skip') or excluded(r)) and len(r.get('poly') or []) >= 3]
        self.excluded = {r['key'] for r in I['rooms'] if excluded(r)}
        if self.excluded:
            self.notes.append("excluded from the conditioned space (job.json exclude_rooms): " + ', '.join(sorted(f"{k} {next((r.get('name') for r in I['rooms'] if r['key'] == k), '')}" for k in self.excluded)))
        for r in self.rooms:
            r['_use'] = use_of(r)
            r['_unit'] = unit_of(r, self.H.get('units'))
        vr = self.H.get('vaulted_rooms') or []
        vr = [vr] if isinstance(vr, str) else vr
        self.vaulted = {r['key'] for r in self.rooms if any(v == r['key'] or (v.endswith('/*') and r['storey'] == v[:-2]) for v in vr)}
        self.north = float(self.H.get('north_deg') or 0.0)
        if not self.H.get('north_deg'):
            self.notes.append('north_deg not set: the sheet is ASSUMED north-up, so window facings (cooling only) are page directions')
        self.D = design(job, scan)
        self.dT = HP.INDOOR_HEAT_F - self.D['heat']
        self.dTc = max(0.0, self.D['cool'] - HP.INDOOR_COOL_F)
        self.u = self.u_factors()
        self.poly = {r['key']: Polygon([tuple(p) for p in r['poly']]).buffer(0) for r in self.rooms}
        self.spoly = {r['key']: Polygon([tuple(p) for p in r['poly']]).buffer(0) for r in self.skipped}
        self.by_storey = defaultdict(list)
        for r in self.rooms:
            self.by_storey[r['storey']].append(r)
        self.cover = {}
        for s in self.storeys:
            polys = [self.poly[r['key']] for r in self.by_storey[s['name']]]
            # close the wall gaps between rooms so an upper floor over a lower one reads as one slab
            self.cover[s['name']] = unary_union(polys).buffer(0.6).buffer(-0.3) if polys else None
        # a skipped region the kept rooms wrap >= 70 % of the way round is INSIDE the house - a chase, the
        # fireplace mass, a wall void the tracer left unnamed. A wall onto it is not an exterior wall, and no
        # outdoor unit, cap or vent ever lands in it. (A garage, deck or porch is outside however wrapped.)
        self.enclosed = {}
        outside_kind = lambda r: (r.get('use') or '') in ('garage', 'exterior') or re.search(r'GARAGE|SHOP|DECK|PORCH|PATIO|CARPORT', (r.get('name') or '').upper())
        self.voids = set()
        for _pass in range(2):          # the second pass lets a region wrapped by rooms AND other voids (a stair opening) count
            for r in self.skipped:
                if outside_kind(r):
                    continue
                near_ = [self.poly[k['key']] for k in self.by_storey[r['storey']]] + \
                        [self.spoly[k['key']] for k in self.skipped if k['storey'] == r['storey'] and k['key'] != r['key'] and
                         (k['key'] in self.voids or (k['key'] in self.excluded and re.search(r'STAIR|OPEN', k.get('name') or '', re.I)))]
                if not near_:
                    continue
                K = unary_union(near_).buffer(1.0)
                B = self.spoly[r['key']].boundary
                self.enclosed[r['key']] = B.intersection(K).length / B.length if B.length else 0.0
                if self.enclosed[r['key']] >= 0.70:
                    self.voids.add(r['key'])
        # the storey's footprint with every gap under 5 ft closed: an untraced stair or a wall chase between two rooms
        # is inside the house, a real outside wall is not (a straight wall survives the closing; only notches do not)
        self.footprint = {}
        for s in self.storeys:
            polys = [self.poly[r['key']] for r in self.by_storey[s['name']]] + [self.spoly[k] for k in self.voids if next(r for r in self.skipped if r['key'] == k)['storey'] == s['name']]
            self.footprint[s['name']] = unary_union(polys).buffer(HP.GAP_CLOSE_FT).buffer(-HP.GAP_CLOSE_FT) if polys else None
        if self.voids:
            self.notes.append('inside the house though the tracer skipped them (>= 70 % wrapped by rooms - chases, the fireplace mass, wall voids): '
                              + ', '.join(f"{k} {next((r.get('name') or '') for r in self.skipped if r['key'] == k)} ({self.spoly[k].area:.0f} sf)".replace('  ', ' ') for k in sorted(self.voids)))

    # -------------------------------------------------------------- the U-factors
    def u_factors(self):
        E = self.H.get('envelope') or {}
        sc = (self.scan.get('envelope') or {})
        src = {}
        def pick(k, scan_key):
            v = E.get(k)
            if v is not None:
                return v, 'job.json'
            v = sc.get(scan_key)
            if v is not None:
                return v, 'hvac_scan (plan text)'
            return None, 'default'
        u = {}
        v, s = pick('ceiling_r', 'ceiling_r_value'); u['ceiling'], why = r_u('ceiling', v); src['ceiling'] = f'{why} [{s}]'
        v, s = pick('vault_r', 'vault_r_value'); u['vault'], why = r_u('vault', v if v is not None else 38); src['vault'] = f'{why} [{s}]'
        v, s = pick('floor_r', 'floor_r_value'); u['floor'], why = r_u('floor', v); src['floor'] = f'{why} [{s}]'
        v, s = pick('wall', 'wall_value'); u['wall'], why = wall_u(v); src['wall'] = f'{why} [{s}]'
        v, s = pick('window_u', 'window_u_value')
        sched = (self.scan.get('openings') or {}).get('u_mean')
        if v is None and sched:
            v, s = sched, 'hvac_scan (window schedule mean)'
        u['window'] = float(v) if v is not None else HP.U_DEFAULT['window']; src['window'] = f"U-{u['window']:.2f} [{s}]"
        v, s = pick('skylight_u', 'skylight_u_value'); u['skylight'] = float(v) if v is not None else HP.U_DEFAULT['skylight']; src['skylight'] = f"U-{u['skylight']:.2f} [{s}]"
        v, s = pick('door_u', 'door_u_value'); u['door'] = float(v) if v is not None else HP.U_DEFAULT['door']; src['door'] = f"U-{u['door']:.2f} [{s}]"
        v, s = pick('slab_f', 'slab_f_value'); u['slab_f'] = float(v) if v is not None else HP.U_DEFAULT['slab_f']; src['slab_f'] = f"F-{u['slab_f']:.2f} [{s}]"
        v, s = pick('ach50', 'ach50_value')
        u['ach50'] = float(v) if v is not None else HP.ACH50_DEFAULT
        src['ach50'] = f"{u['ach50']:g} ACH50 [{s if v is not None else 'WSEC R402.4.1.2 maximum - the set names no tighter target'}]"
        self.u_src = src
        return u

    # -------------------------------------------------------------- exposure
    def inside_other(self, pt, storey, own):
        for r in self.by_storey[storey]:
            if r['key'] != own and self.poly[r['key']].buffer(0.05).contains(pt):
                return r['key']
        for r in self.skipped:
            if r['storey'] != storey or not self.spoly[r['key']].contains(pt):
                continue
            if r['key'] in self.voids:
                return r['key']
            if INTERIOR_SKIP_WORDS.search(r.get('name') or '') and r['key'] not in self.excluded:
                return r['key']
            if r['key'] in self.excluded and re.search(r'STAIR|OPEN', r.get('name') or '', re.I):
                return r['key']            # an excluded VOID (stair opening) is still inside the house
        return None

    def exterior_edges(self, r):
        P = self.poly[r['key']]
        pts = [tuple(p) for p in r['poly']]
        out = []
        n = len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            L = C.dist(a, b)
            if L < 0.5:
                continue
            ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            nx, ny = -uy, ux
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            if P.contains(self.Pt(m[0] + nx * 0.3, m[1] + ny * 0.3)):
                nx, ny = -nx, -ny
            # sample three points along the edge; an edge is exterior where the probes find no room behind it
            ext_len = 0.0
            for t in (0.2, 0.5, 0.8):
                q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
                p1 = self.Pt(q[0] + nx * 1.5, q[1] + ny * 1.5)
                p2 = self.Pt(q[0] + nx * 4.0, q[1] + ny * 4.0)
                fp = self.footprint.get(r['storey'])
                if not self.inside_other(p1, r['storey'], r['key']) and not self.inside_other(p2, r['storey'], r['key']) and not P.contains(p1) \
                        and (fp is None or not fp.contains(p2) or self.beyond(p2, r['storey'])):
                    ext_len += L / 3
            if ext_len > 0.1:
                face, bearing = C.facing(nx, ny, self.north)
                beyond = self.beyond(self.Pt(m[0] + nx * 1.5, m[1] + ny * 1.5), r['storey'])
                out.append(dict(a=a, b=b, ft=round(ext_len, 2), facing=face, bearing=round(bearing), normal=(nx, ny), beyond=beyond))
        return out

    def beyond(self, pt, storey):
        """what an exterior wall looks onto: 'garage' (the garage / shop - no outdoor unit, cap or vent there),
        'porch' (a deck, porch or patio), or None (open air)"""
        for r in self.skipped:
            if r['storey'] != storey or not self.spoly[r['key']].buffer(0.3).contains(pt):
                continue
            nm = (r.get('name') or '').upper(); use = (r.get('use') or '').lower()
            if use == 'garage' or re.search(r'GARAGE|SHOP|CARPORT|WORKBENCH', nm):
                return 'garage'
            if use == 'exterior' or re.search(r'DECK|PORCH|PATIO|CVDECK|LANAI|VERANDA', nm):
                return 'porch'
        return None

    def exposed_ceiling(self, r):
        i = [s['name'] for s in self.storeys].index(r['storey'])
        if i == len(self.storeys) - 1:
            return self.poly[r['key']].area
        above = self.cover.get(self.storeys[i + 1]['name'])
        if above is None:
            return self.poly[r['key']].area
        return max(0.0, self.poly[r['key']].difference(above).area)

    def exposed_floor(self, r):
        i = [s['name'] for s in self.storeys].index(r['storey'])
        if i == 0:
            return self.poly[r['key']].area, (self.H.get('foundation') or 'crawl')
        below = self.cover.get(self.storeys[i - 1]['name'])
        if below is None:
            return self.poly[r['key']].area, 'over unconditioned space'
        a = max(0.0, self.poly[r['key']].difference(below).area)
        return a, 'over the garage / outside (no room below)'

    # -------------------------------------------------------------- openings
    def openings(self, rooms_x):
        by_room = defaultdict(list)
        for w in self.I.get('windows', []):
            if w.get('unfinished'):
                continue
            by_room[w.get('room')].append(dict(kind='window', w_ft=w['w_ft'], h_ft=w.get('h_ft') or 4.0, seg=w.get('seg'), src='traced'))
        for d in self.I.get('extdoors', []):
            if d.get('unfinished'):
                continue
            by_room[d.get('room')].append(dict(kind='door', w_ft=d['w_ft'], h_ft=d.get('h_ft') or 6.67, seg=d.get('seg'), src='traced'))
        traced = sum(o['w_ft'] * o['h_ft'] for v in by_room.values() for o in v if o['kind'] == 'window')
        G = self.H.get('glazing') or {}
        scan_op = self.scan.get('openings') or {}
        target, why = traced, 'traced windows (interior.json)'
        if G.get('sf'):
            target, why = float(G['sf']), f"job.json glazing.sf ({G.get('_src', 'typed')})"
        elif scan_op.get('window_sf', 0) + scan_op.get('patio_sf', 0) > traced * 1.15:
            target = scan_op.get('window_sf', 0) + scan_op.get('patio_sf', 0)
            why = f"the plan's window schedule as read ({scan_op.get('count')} units) - more than the {traced:.0f} sf traced"
        extra = max(0.0, target - traced)
        self.glazing = dict(traced_sf=round(traced, 1), used_sf=round(max(traced, target), 1), why=why, spread_sf=round(extra, 1))
        if extra > 1:
            wts = {}
            for r in self.rooms:
                ext = sum(e['ft'] for e in rooms_x.get(r['key'], []))
                w = {'bath': 0.3, 'powder': 0.3, 'closet': 0.0, 'utility': 0.2, 'laundry': 0.2}.get(r['_use'], 1.0)
                if ext > 0 and w > 0:
                    wts[r['key']] = ext * w
            tot = sum(wts.values()) or 1
            for k, v in wts.items():
                by_room[k].append(dict(kind='window', w_ft=round(extra * v / tot, 2), h_ft=1.0, seg=None, src='schedule spread'))
            self.notes.append(f"glazing: {why}; the {extra:.0f} sf the tracer did not find is spread over {len(wts)} rooms by exterior wall length")
        return by_room

    # -------------------------------------------------------------- the calc
    def run(self):
        H = self.H
        u = self.u
        rooms_x = {r['key']: self.exterior_edges(r) for r in self.rooms}
        ops = self.openings(rooms_x)
        n_st = max(1, min(len(self.storeys), 3))
        area_traced = sum(self.poly[r['key']].area for r in self.rooms)
        cfa_plan = float(H.get('cfa_sf') or (self.scan.get('areas') or {}).get('heated_sf') or 0) or None
        scale = (cfa_plan / area_traced) if (cfa_plan and area_traced and cfa_plan > area_traced * 1.03) else 1.0
        if scale > 1.0:
            self.notes.append(f'the traced rooms cover {area_traced:.0f} sf of the plan\'s {cfa_plan:.0f} sf heated area: ceiling, floor, infiltration and '
                              f'ventilation are scaled x{scale:.2f} to the plan figure (walls and glass are what the trace measured)')
        duct = H.get('ducts') or ('inside' if (H.get('system') or {}).get('kind') in ('ductless', None) else 'crawl_vented')
        duct_f = HP.DUCT_LOSS.get(duct, 0.0)
        beds = sum(1 for r in self.rooms if r['_use'] == 'bedroom' and self.poly[r['key']].area >= HP.HABITABLE_MIN_SF)
        beds = int(H.get('bedrooms') or beds or 3)
        shgc = float((H.get('envelope') or {}).get('shgc') or HP.GLF_SHGC_REF)
        rows = []
        vol_total = 0.0
        ext_area_total = 0.0
        for r in self.rooms:
            k = r['key']
            area = self.poly[k].area
            ceil = float(r.get('ceil_ft') or r.get('plate') or 9.0)
            vol = area * ceil
            vol_total += vol
            walls = rooms_x[k]
            wall_ft = sum(e['ft'] for e in walls)
            gross = wall_ft * ceil
            win = [o for o in ops.get(k, []) if o['kind'] == 'window']
            door = [o for o in ops.get(k, []) if o['kind'] == 'door']
            win_sf = sum(o['w_ft'] * o['h_ft'] for o in win)
            door_sf = sum(o['w_ft'] * o['h_ft'] for o in door)
            if win_sf + door_sf > gross * 0.9 and gross > 0:
                self.warn.append(f"{k} {r.get('name')}: {win_sf + door_sf:.0f} sf of openings on {gross:.0f} sf of traced exterior wall - capped at 90 %")
                f = gross * 0.9 / (win_sf + door_sf); win_sf *= f; door_sf *= f
            net = max(0.0, gross - win_sf - door_sf)
            ceil_sf = self.exposed_ceiling(r)
            vaulted = k in self.vaulted
            floor_sf, floor_kind = self.exposed_floor(r)
            ext_area_total += gross
            rows.append(dict(key=k, name=r.get('name'), use=r['_use'], unit=r['_unit'], storey=r['storey'], area_sf=round(area, 1), ceil_ft=ceil, volume=round(vol),
                             ext_wall_ft=round(wall_ft, 1), wall_gross_sf=round(gross, 1), wall_net_sf=round(net, 1), win_sf=round(win_sf, 1),
                             door_sf=round(door_sf, 1), ceil_sf=round(ceil_sf, 1), vaulted=vaulted, floor_sf=round(floor_sf, 1), floor_kind=floor_kind,
                             walls=[dict(ft=e['ft'], facing=e['facing'], a=[round(v, 2) for v in e['a']], b=[round(v, 2) for v in e['b']],
                                         n=[round(v, 3) for v in e['normal']], beyond=e.get('beyond')) for e in walls],
                             poly=[[round(p[0], 2), round(p[1], 2)] for p in self.poly[k].exterior.coords][:-1] if self.poly[k].geom_type == 'Polygon' else [list(p) for p in r['poly']],
                             z=float(next((s['z'] for s in self.storeys if s['name'] == r['storey']), 0.0)),
                             centroid=[round(v, 2) for v in C.centroid([tuple(p) for p in r['poly']])],
                             win_facing=self.window_facing(k, win, walls)))
        # ---- infiltration, whole house (MJ8 blower-door method), shared by exterior wall area
        vol_plan = vol_total * scale
        cfm_inf = HP.icfm(u['ach50'], vol_plan, n_st, self.dT, HP.WIND_HEAT_MPH)
        cfm_inf_c = HP.icfm(u['ach50'], vol_plan, n_st, self.dTc, HP.WIND_COOL_MPH)
        ach_nat = cfm_inf * 60.0 / vol_plan if vol_plan else 0.0
        cl = {k: max(0.0, self.dTc + v) for k, v in HP.CLTD_OFFSET.items()}      # cooling temperature differences
        for row in rows:
            share = row['wall_gross_sf'] / ext_area_total if ext_area_total else 1 / max(1, len(rows))
            if row['floor_kind'] == 'slab':
                floor_h = u['slab_f'] * row['ext_wall_ft'] * self.dT       # slab edge: F x exposed perimeter x dT
            elif row['floor_kind'] == 'crawl':
                floor_h = u['floor'] * row['floor_sf'] * scale * self.dT * HP.CRAWL_PTD
            else:
                floor_h = u['floor'] * row['floor_sf'] * scale * self.dT
            hc = dict(
                wall=u['wall'] * row['wall_net_sf'] * self.dT,
                window=u['window'] * row['win_sf'] * self.dT,
                door=u['door'] * row['door_sf'] * self.dT,
                ceiling=(u['vault'] if row['vaulted'] else u['ceiling']) * row['ceil_sf'] * scale * self.dT,
                floor=floor_h,
                infiltration=HP.AIR_SENS * cfm_inf * share * self.dT,
            )
            sub = sum(hc.values())
            hc['duct'] = sub * duct_f
            row['heat'] = {k: round(v) for k, v in hc.items()}
            row['heat_btuh'] = round(sum(hc.values()))
            row['inf_cfm'] = round(cfm_inf * share, 2)
            row['inf_cfm_c'] = round(cfm_inf_c * share, 2)
            # cooling
            glass = sum(sf * HP.GLF.get(face, 16.0) * shgc / HP.GLF_SHGC_REF for face, sf in row['win_facing'].items()) + u['window'] * row['win_sf'] * self.dTc
            people = 0.0
            if row['use'] == 'bedroom' and row['area_sf'] >= HP.HABITABLE_MIN_SF:
                people = HP.PEOPLE_SENS * (2 if re.search(r'MASTER|PRIMARY|MSTR', (row['name'] or '').upper()) else 1)
            cc = dict(wall=u['wall'] * row['wall_net_sf'] * cl['wall'],
                      ceiling=(u['vault'] if row['vaulted'] else u['ceiling']) * row['ceil_sf'] * scale * cl['vault' if row['vaulted'] else 'ceiling'],
                      door=u['door'] * row['door_sf'] * cl['door'],
                      glass=glass, infiltration=HP.AIR_SENS * cfm_inf_c * share * self.dTc,
                      people=people, appliances=HP.APPLIANCE_KITCHEN if row['use'] == 'kitchen' else 0.0)
            row['cool'] = {k: round(v) for k, v in cc.items()}
            row['cool_btuh'] = round(sum(cc.values()))
        # people not in a bedroom and the rest of the appliance allowance: the living spaces share them
        occ = beds + 1
        in_beds = sum((2 if re.search(r'MASTER|PRIMARY|MSTR', (r['name'] or '').upper()) else 1) for r in rows if r['cool'].get('people'))
        rest = max(0, occ - in_beds)
        liv = [r for r in rows if r['use'] in ('living', 'kitchen', 'dining')] or rows
        n_kit = sum(1 for r in rows if r['use'] == 'kitchen')
        for r in liv:
            add = HP.PEOPLE_SENS * rest / len(liv) + max(0.0, HP.APPLIANCE_SENS - HP.APPLIANCE_KITCHEN * max(1, n_kit)) / len(liv)
            r['cool']['people'] = r['cool'].get('people', 0) + round(add)
            r['cool_btuh'] += round(add)
        # ---- ventilation, per dwelling unit (a duplex ventilates each unit on its own)
        cfa = cfa_plan or area_traced
        V = H.get('ventilation') or {}
        vkind = V.get('kind') or (self.scan.get('ventilation') or {}).get('kind') or 'exhaust'
        if vkind == 'unknown':
            vkind = 'exhaust'
        balanced = vkind in ('erv', 'hrv', 'balanced')
        distributed = bool(V.get('distributed', balanced))
        sre = float(V.get('sre') or (0.7 if balanced else 0.0))
        units = H.get('units') or [dict(name='house', cfa_sf=cfa, bedrooms=beds)]
        unit_out = []
        grains = float(self.D.get('grains') or 4.0)
        for un in units:
            name = un.get('name', 'house')
            rs = [r for r in rows if r['unit'] == name] if len(units) > 1 else rows
            cfa_u = float(un.get('cfa_sf') or sum(r['area_sf'] for r in rs) * scale)
            beds_u = int(un.get('bedrooms') or sum(1 for r in rs if r['use'] == 'bedroom' and r['area_sf'] >= HP.HABITABLE_MIN_SF) or 2)
            qr, csys, q = HP.vent_rate(cfa_u, beds_u, balanced, distributed)
            inf_share = sum(r['wall_gross_sf'] for r in rs) / ext_area_total if ext_area_total else 1.0
            i_h, i_c = cfm_inf * inf_share, cfm_inf_c * inf_share
            if balanced:
                vh = HP.AIR_SENS * q * self.dT * (1 - sre)
                vc = HP.AIR_SENS * q * self.dTc * (1 - sre)
                q_lat = q * (1 - sre * 0.6)
                how = f'balanced {vkind.upper()}: 1.1 x {q:.0f} cfm x dT x (1 - SRE {sre:g})'
            else:
                n_h = (i_h ** 1.5 + q ** 1.5) ** 0.67
                n_c = (i_c ** 1.5 + q ** 1.5) ** 0.67
                vh = HP.AIR_SENS * (n_h - i_h) * self.dT
                vc = HP.AIR_SENS * (n_c - i_c) * self.dTc
                q_lat = n_c - i_c
                how = f'exhaust-only: (ICFM^1.5 + Qv^1.5)^0.67 = {n_h:.0f} cfm against {i_h:.0f} cfm of infiltration alone'
            lat_u = HP.PEOPLE_LAT * (beds_u + 1) + HP.AIR_LAT * (i_c + q_lat) * grains
            hr = sum(r['heat_btuh'] for r in rs); cr = sum(r['cool_btuh'] for r in rs)
            unit_out.append(dict(name=name, rooms=[r['key'] for r in rs], cfa_sf=round(cfa_u), bedrooms=beds_u, vent_qr=round(qr, 1), vent_csystem=csys,
                                 vent_cfm=round(q, 1), vent_how=how,
                                 vent_heat_btuh=round(vh), heat_rooms_btuh=round(hr), heat_btuh=round(hr + vh),
                                 cool_sens_btuh=round(cr + vc), cool_lat_btuh=round(lat_u),
                                 cool_tons=round((cr + vc + lat_u) / 12000, 2),
                                 heat_per_sf=round((hr + vh) / cfa_u, 1) if cfa_u else None))
        q_vent = sum(u_['vent_cfm'] for u_ in unit_out)
        vent_heat = sum(u_['vent_heat_btuh'] for u_ in unit_out)
        vent_cool = sum(u_['cool_sens_btuh'] for u_ in unit_out) - sum(r['cool_btuh'] for r in rows)
        heat_rooms = sum(r['heat_btuh'] for r in rows)
        cool_rooms = sum(r['cool_btuh'] for r in rows)
        lat = sum(u_['cool_lat_btuh'] for u_ in unit_out)
        heat_total = heat_rooms + vent_heat
        cool_total = cool_rooms + vent_cool
        # ---- the WSU "Simple Heating System Size" cross-check: dT x (UA + 0.018 x 0.6 ACH x volume) (x 1.10 ducts outside)
        UA = sum(u['wall'] * r['wall_net_sf'] + u['window'] * r['win_sf'] + u['door'] * r['door_sf'] +
                 (u['vault'] if r['vaulted'] else u['ceiling']) * r['ceil_sf'] * scale + u['floor'] * r['floor_sf'] * scale for r in rows)
        wsu_ach = float(H.get('wsu_ach') or HP.WSU_ACH)
        wsu = self.dT * (UA + HP.WSU_AIR * wsu_ach * vol_plan) * (HP.WSU_DUCT_UNCOND if duct_f > 0 else 1.0)
        per_sf = heat_total / cfa if cfa else 0
        cool_sf = (cool_total + lat) / cfa if cfa else 0
        lo, hi = HP.BAND_HEAT_PER_SF
        if per_sf and not (lo <= per_sf <= hi):
            self.warn.append(f'heating load {per_sf:.1f} Btuh/sf is outside {lo:g}-{hi:g} (a new WSEC-2021 house lands at 7-12) - look at the envelope inputs')
        lo, hi = HP.BAND_COOL_PER_SF
        if cool_sf and not (lo <= cool_sf <= hi):
            self.warn.append(f'cooling load {cool_sf:.1f} Btuh/sf is outside {lo:g}-{hi:g} (expected 3.5-5.5) - check the west / east glass and the skylights')
        ratio = (cool_total + lat) / heat_total if heat_total else 0
        lo, hi = HP.BAND_COOL_OVER_HEAT
        if ratio and not (lo <= ratio <= hi):
            self.warn.append(f'cooling / heating = {ratio:.2f}, outside {lo:g}-{hi:g} (expected 0.40-0.55) - a design temperature or the glass is off')
        for r in rows:
            r['heat_share'] = round(r['heat_btuh'] / heat_rooms, 4) if heat_rooms else 0
            r['cool_share'] = round(r['cool_btuh'] / cool_rooms, 4) if cool_rooms else 0
        alt = None
        if self.D.get('mj8_heat') is not None and self.D['mj8_heat'] != self.D['heat']:
            f = (HP.INDOOR_HEAT_F - self.D['mj8_heat']) / self.dT
            alt = dict(heat=self.D['mj8_heat'], heat_btuh=round(heat_total * f),
                       note=f"at Manual J's own 99 % design temperature ({self.D['mj8_heat']} F) the load is ~{heat_total * f:,.0f} Btuh; the equipment is sized on the code's Table RC-1 value ({self.D['heat']} F)")
        return dict(design=dict(self.D, indoor_heat=HP.INDOOR_HEAT_F, indoor_cool=HP.INDOOR_COOL_F, dT_heat=self.dT, dT_cool=self.dTc),
                    u=self.u, u_src=self.u_src, glazing=self.glazing, rooms=rows, units=unit_out,
                    infiltration=dict(ach50=u['ach50'], storeys=n_st, method='MJ8 blower-door (ICFM = 0.05488 Q50 sqrt(0.015 N dT + Cw 15^2), shielding 4)',
                                      ach_nat=round(ach_nat, 3), n_equiv=round(u['ach50'] / ach_nat, 1) if ach_nat else None,
                                      cfm_heat=round(cfm_inf, 1), cfm_cool=round(cfm_inf_c, 1), volume_traced=round(vol_total), volume_used=round(vol_plan)),
                    ventilation=dict(kind=vkind, balanced=balanced, distributed=distributed, cfm=round(q_vent, 1),
                                     qr=round(sum(u_['vent_qr'] for u_ in unit_out), 1), csystem=unit_out[0]['vent_csystem'] if unit_out else None,
                                     bedrooms=sum(u_['bedrooms'] for u_ in unit_out), cfa_sf=round(sum(u_['cfa_sf'] for u_ in unit_out)), sre=sre,
                                     heat_btuh=round(vent_heat), cool_btuh=round(vent_cool), how=unit_out[0]['vent_how'] if unit_out else '',
                                     formula='Qv = (0.01 x CFA + 7.5 x (bedrooms + 1), min 30) x Csystem (WA M1505.4.3, Eq. 15-1 / 15-2)'),
                    duct=dict(location=duct, factor=duct_f),
                    area=dict(traced_sf=round(area_traced), plan_sf=round(cfa_plan) if cfa_plan else None, scale=round(scale, 3)),
                    alt=alt,
                    totals=dict(heat_btuh=round(heat_total), heat_rooms_btuh=round(heat_rooms), cool_sens_btuh=round(cool_total),
                                cool_lat_btuh=round(lat), cool_tons=round((cool_total + lat) / 12000, 2), heat_per_sf=round(per_sf, 1),
                                cool_per_sf=round(cool_sf, 1), cool_over_heat=round(ratio, 2),
                                wsu_btuh=round(wsu), wsu_ach=wsu_ach, wsu_max_hp_btuh=round(wsu * HP.WSU_MAX_HP), UA=round(UA, 1),
                                by_component={k: round(sum(r['heat'].get(k, 0) for r in rows)) for k in ('wall', 'window', 'door', 'ceiling', 'floor', 'infiltration', 'duct')}
                                | {'ventilation': round(vent_heat)}),
                    notes=self.notes, warnings=self.warn)

    def window_facing(self, k, wins, walls):
        """glass area by facing: a traced window takes the facing of the exterior wall it sits on; spread glass
        follows the room's exterior walls in proportion"""
        out = defaultdict(float)
        for o in wins:
            sf = o['w_ft'] * o['h_ft']
            if o.get('seg') and walls:
                (x0, y0), (x1, y1) = o['seg']
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                best = min(walls, key=lambda e: self.LS([e['a'], e['b']]).distance(self.Pt(mx, my)))
                out[best['facing']] += sf
            elif walls:
                tot = sum(e['ft'] for e in walls)
                for e in walls:
                    out[e['facing']] += sf * e['ft'] / tot
            else:
                out['N'] += sf
        return {k2: round(v, 1) for k2, v in out.items()}


def report_md(o):
    T = o['totals']; D = o['design']
    L = [f"## Loads - {D['town']}: {D['heat']} F heating / {D['cool']} F cooling design (dT {D['dT_heat']:g} F / {D['dT_cool']:g} F)\n"]
    L.append(f"**Heating {T['heat_btuh']:,} Btuh** ({T['heat_per_sf']} Btuh/sf) · cooling {T['cool_sens_btuh']:,} sensible + {T['cool_lat_btuh']:,} latent = {T['cool_tons']} tons · "
             f"WSU sheet cross-check {T['wsu_btuh']:,} Btuh (UA {T['UA']:,.0f} + 0.018 x {T['wsu_ach']} ACH x volume; the sheet's heat-pump maximum is 1.25 x = {T['wsu_max_hp_btuh']:,}) · "
             f"{T['cool_per_sf']} Btuh/sf cooling, cooling / heating {T['cool_over_heat']}\n")
    L.append('| component | Btuh |'); L.append('|---|---|')
    for k, v in T['by_component'].items():
        L.append(f'| {k} | {v:,} |')
    L.append("\nU-factors: " + '; '.join(f'{k} {v}' for k, v in o['u_src'].items()))
    inf = o['infiltration']; V = o['ventilation']; A = o['area']; G = o['glazing']
    L.append(f"\ninfiltration {inf['ach50']:g} ACH50 -> {inf['ach_nat']} ACH at design (ACH50 / {inf['n_equiv']}) on {inf['volume_used']:,} cf = {inf['cfm_heat']} cfm ({inf['method']}) · "
             f"ventilation {V['cfm']} cfm continuous = {V['qr']} x Csystem {V['csystem']} ({V['formula']}; {V['bedrooms']} bedrooms, {V['cfa_sf']:,} sf) -> {V['heat_btuh']:,} Btuh, {V['how']} · "
             f"ducts {o['duct']['location']} (+{o['duct']['factor']:.0%}) · area traced {A['traced_sf']:,} sf vs plan {A['plan_sf'] or '-'} sf (x{A['scale']}) · "
             f"glazing {G['used_sf']:,} sf ({G['why']})\n")
    if o.get('alt'):
        L.append(f"- {o['alt']['note']}")
    L.append('| room | storey | use | sf | ext wall ft | glass sf | ceiling sf | floor sf | heat Btuh | cool Btuh |'); L.append('|---|---|---|---|---|---|---|---|---|---|')
    for r in sorted(o['rooms'], key=lambda r: -r['heat_btuh']):
        L.append(f"| {r['name'] or r['key']} | {r['storey']} | {r['use']} | {r['area_sf']:.0f} | {r['ext_wall_ft']:.0f} | {r['win_sf']:.0f} | {r['ceil_sf']:.0f} | {r['floor_sf']:.0f} | {r['heat_btuh']:,} | {r['cool_btuh']:,} |")
    for n in o['notes']:
        L.append(f'- note: {n}')
    for w in o['warnings']:
        L.append(f'- **warning**: {w}')
    return '\n'.join(L)


def run(job_path, interior=None, scan=None):
    job = C.load(job_path)
    d = os.path.dirname(os.path.abspath(job_path))
    I = C.load(interior or C.resolve(job.get('interior', 'interior.json'), d))
    sp = scan or os.path.join(d, 'hvac_scan.json')
    S = C.load(sp) if os.path.exists(sp) else {}
    return Loads(job, I, S, d).run()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('job'); ap.add_argument('--interior', default=None); ap.add_argument('--scan', default=None); ap.add_argument('--out', default=None)
    a = ap.parse_args()
    o = run(a.job, a.interior, a.scan)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.job)), 'hvac_loads.json')
    json.dump(o, open(out, 'w', encoding='utf-8'), indent=1)
    T = o['totals']
    print(f"heat {T['heat_btuh']:,} Btuh ({T['heat_per_sf']} Btuh/sf) · cool {T['cool_sens_btuh']:,}+{T['cool_lat_btuh']:,} = {T['cool_tons']} t · WSU {T['wsu_btuh']:,} · {len(o['rooms'])} rooms -> {out}")
    for w in o['warnings']:
        print('  warning:', w)
