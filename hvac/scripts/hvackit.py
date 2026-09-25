#!/usr/bin/env python3
r"""hvackit.py - the HVAC engine: room loads -> the system -> every head, register, duct, line set, vent and cap ->
the order, the checker, the labour, the inspections, the takeoff.

    python hvackit.py job.json [--interior interior.json] [--scan hvac_scan.json] [--out hvac_takeoff.json]

In the order a mechanical contractor lays a house out:

  1. LOADS (hvac_load.py): room-by-room heat loss and gain off the traced interior, per dwelling unit.
  2. THE SYSTEM, per dwelling unit, from job.json `hvac.system.kind` (the plan's WSEC credit, read by hvacscan.py):
       ductless          ZONES first: bedrooms each their own, the open plan (living / kitchen / dining and the halls
                         cased into them) one zone per storey, closets / baths / laundry carried by the zone they open
                         into. A wall head per zone, sized to the zone's larger of heating and cooling load; one
                         outdoor unit per head (1-2 heads) or a multi-zone sized so its capacity AT THE DESIGN
                         TEMPERATURE carries the whole unit - WSEC option 3.7 says exactly that.
       ducted            a centrally ducted cold-climate heat pump + variable-speed air handler sized to the heating
                         load at the design temperature, a backup strip for the difference (never less than 5 kW,
                         locked out by the thermostat - WSEC R403.1.2), room airflow in proportion to the room load,
                         registers under the exterior walls, a trunk per storey, flex branches, a central return per
                         storey and a transfer path out of every bedroom with a door.
       ducted_multizone  a multi-zone outdoor unit with a DUCTED indoor unit per storey (Semiahmoo's MXZ-SM60NAM on a
                         'centrally ducted' credit) - the duct layout of `ducted`, the refrigerant of `ductless`.
  3. REFRIGERANT: every line set ROUTED - along the generated wall network (the electrical skill's WallNet) to the
     stair riser, down into the crawl and out the rim beside the outdoor unit (concealed, the default on a crawl
     foundation), or through the wall behind the head and down a line-hide cover (exterior). Sized by capacity,
     extra charge past the pre-charged length, condensate beside it, a pump where it cannot fall.
  4. VENTILATION: the WA whole-house rate (0.01 x CFA + 7.5 x (bedrooms + 1)) delivered either exhaust-only - a
     continuous-duty fan on a labelled 24 h control and an OUTDOOR AIR INLET in every habitable room (WA) - or balanced
     by an ERV / HRV with supply to the bedrooms and living spaces and exhaust from the baths and laundry.
  5. EXHAUST the electrical skill leaves to HVAC: a duct and a cap for every bath fan the electrician placed
     (electrical/jobs/<h>/devices.json), the dryer vent measured against the 35 ft equivalent length, the range hood
     duct sized by its CFM and make-up air above 400 cfm (M1503.6).
  6. SUPPORT, PROTECTION, TESTS: pads, stands, sleeves, bores and nail plates, firestops at the garage, the duct
     leakage test (ducts outside the envelope), the ventilation flow test (WA), start-up per outdoor unit.
  7. THE CHECKER, the LABOUR (crew minutes -> days), the INSPECTIONS and the permit line.

Nothing here is priced. Every default is printed with where it came from.
"""
import argparse, json, math, os, re, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hvac_common as C
import hvac_parts as HP
import hvac_load as HL

C.utf8()

HEADABLE = {'bedroom', 'living', 'kitchen', 'dining', 'office', 'den', 'media'}
HOST_PRI = {'living': 0, 'dining': 0, 'media': 1, 'den': 1, 'office': 1, 'bedroom': 1, 'kitchen': 3}
PRIVATE = {'closet', 'bath', 'powder', 'linen', 'pantry', 'storage'}
OPEN_TYPES = ('door_cased', 'opening', 'cased')
SUPPLY_USES = {'bedroom', 'living', 'kitchen', 'dining', 'office', 'den', 'media', 'circulation', 'stair', 'bath', 'powder', 'utility', 'laundry'}
HEAD_Z = 7.0            # ft above the finished floor, top of a wall head
CRAWL_Z = -1.2          # ft, where concealed lines and crawl ducts run under the main floor
REG_INSET = 1.0         # ft in from the exterior wall
ROOF_RUN_FT = 8.0       # fan housing to the roof jack through the attic / rafter bay


def near(p, q):
    return math.dist(p[:2], q[:2])


def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def norm_name(n):
    return re.sub(r'[^A-Z0-9]+', ' ', (n or '').upper()).strip()


class Kit:
    def __init__(self, job, I, S, job_dir):
        self.job, self.S, self.job_dir = job, S or {}, job_dir
        self.H = job.get('hvac') or {}
        lo = HL.Loads(job, I, S, job_dir)
        self.lo = lo
        self.I = lo.I
        self.L = lo.run()
        self.rooms = {r['key']: r for r in self.L['rooms']}
        self.storeys = sorted(self.I['storeys'], key=lambda s: s['z'])
        self.st = {s['name']: s for s in self.storeys}
        self.main = self.storeys[0]['name']
        self.order, self.checks, self.notes, self.runs, self.items, self.systems = [], [], [], [], [], []
        self.D = self.L['design']
        self.T = float(self.D['heat'])
        self.found = (self.H.get('foundation') or 'crawl').lower()
        sysd = self.H.get('system') or {}
        self.kind = sysd.get('kind') or ((S or {}).get('system') or {}).get('kind') or 'unknown'
        self.route_mode = sysd.get('lineset_route') or ('concealed' if self.found == 'crawl' else 'exterior')
        self.doors = self.I.get('doors', [])
        self.all_rooms = {r['key']: r for r in self.I['rooms'] if len(r.get('poly') or []) >= 3}
        self.dev, self.dev_src = self.elec_devices()
        self.build_spaces()

    # ============================================================ small helpers
    def check(self, level, where, what):
        self.checks.append(dict(level=level, where=where, what=what))

    def fit(self, part, n, note=''):
        if n:
            self.order.append(dict(part=part, qty=float(n), note=note))

    def line(self, part, lf, note=''):
        if lf and lf > 0.05:
            self.order.append(dict(part=part, lf=float(lf), note=note))

    def run(self, system, size, pts, note, storey=None, ft=None):
        pts = [tuple(round(v, 3) for v in p) for p in pts]
        L = ft if ft is not None else sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
        self.runs.append(dict(system=system, size=size, pts=[list(p) for p in pts], ft=round(L, 1), storey=storey, note=note))
        return L

    def item(self, kind, part, pos, z, storey, room=None, note='', **kw):
        self.items.append(dict(kind=kind, part=part, pos=[round(pos[0], 2), round(pos[1], 2)], z=round(z, 2), storey=storey, room=room, note=note, **kw))

    def zof(self, storey):
        return float(self.st[storey]['z'])

    def plate(self, storey):
        return float(self.st[storey].get('plate') or 9.0)

    def rname(self, key):
        r = self.rooms.get(key) or self.all_rooms.get(key) or {}
        return r.get('name') or key

    def unit_at(self, pos):
        units = self.H.get('units') or []
        if not units:
            return 'house'
        for u in units:
            if (u.get('x_min') is None or pos[0] >= u['x_min']) and (u.get('x_max') is None or pos[0] < u['x_max']) and \
               (u.get('y_min') is None or pos[1] >= u['y_min']) and (u.get('y_max') is None or pos[1] < u['y_max']):
                return u.get('name', 'house')
        return units[0].get('name', 'house')

    def ext_walls(self, storey, unit=None):
        out = []
        for r in self.L['rooms']:
            if r['storey'] != storey or (unit and r['unit'] != unit):
                continue
            for w in r['walls']:
                out.append(dict(w, room=r['key']))
        return out

    def exit_point(self, target, storey, unit=None, side=None, porch_penalty=6.0):
        """the point just inside an exterior wall of `storey` nearest `target`, the outward normal, and the point
        2.5 ft outside it where an outdoor unit / cap sits. Never a wall onto the garage or shop (no unit, cap or
        vent terminates there); a wall onto a deck or porch costs `porch_penalty` ft."""
        best = None
        for w in self.ext_walls(storey, unit):
            if side and side != 'auto' and w['facing'] != side:
                continue
            if w.get('beyond') == 'garage':
                continue
            a, b = w['a'], w['b']
            L = C.dist(a, b)
            if L < 1.5:
                continue
            t = ((target[0] - a[0]) * (b[0] - a[0]) + (target[1] - a[1]) * (b[1] - a[1])) / (L * L)
            t = min(max(t, 0.1), 0.9)
            q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            d = C.dist(q, target) + (porch_penalty if w.get('beyond') == 'porch' else 0.0)
            if best is None or d < best[0]:
                best = (d, q, w['n'], w['facing'], w['room'], w.get('beyond'))
        if best is None:
            return None
        d, q, n, face, room, bey = best
        outside = (q[0] + n[0] * 2.5, q[1] + n[1] * 2.5)
        return dict(inside=q, outside=outside, n=n, facing=face, room=room, dist=d, beyond=bey)

    # ============================================================ the electrical skill's layout (read, never written)
    def elec_devices(self):
        dev = self.H.get('electrical_devices')
        guess = None
        m = re.search(r'finish/jobs/([^/\\]+)/', (self.job.get('interior') or '').replace('\\', '/'))
        if m:
            guess = os.path.join(C.skills_dir(), 'electrical', 'jobs', m.group(1), 'devices.json')
        for p in ([C.resolve(dev, self.job_dir)] if dev else []) + ([guess] if guess else []):
            if p and os.path.exists(p):
                D = C.load(p)
                out = []
                for d in D.get('devices', []):
                    if not d.get('pos'):
                        continue
                    st = d.get('storey') or (self.all_rooms.get(d.get('room')) or {}).get('storey')
                    if st not in self.st:
                        continue
                    out.append(dict(d, storey=st, unit_here=self.unit_at(d['pos'])))
                return out, os.path.relpath(p, C.skills_dir())
        return [], None

    def elec_find(self, pat, unit=None):
        return [d for d in self.dev if re.search(pat, d.get('appliance') or '', re.I) and (unit is None or d['unit_here'] == unit or len(self.L['units']) == 1)]

    # ============================================================ spaces: the tracer's fragments merged back into rooms
    def build_spaces(self):
        from shapely.geometry import Polygon
        rs = self.L['rooms']
        P = {r['key']: Polygon(r['poly']).buffer(0) for r in rs}
        parent = {r['key']: r['key'] for r in rs}

        def find(k):
            while parent[k] != k:
                parent[k] = parent[parent[k]]
                k = parent[k]
            return k
        for i, a in enumerate(rs):
            na = norm_name(a['name'])
            if not na:
                continue
            for b in rs[i + 1:]:
                if b['storey'] == a['storey'] and b['unit'] == a['unit'] and norm_name(b['name']) == na and P[a['key']].distance(P[b['key']]) <= 1.0:
                    ra, rb = find(a['key']), find(b['key'])
                    if ra != rb:
                        parent[rb] = ra
        groups = defaultdict(list)
        for r in rs:
            groups[find(r['key'])].append(r)
        self.spaces, self.space_of = [], {}
        merged = []
        for gi, (g, mem) in enumerate(sorted(groups.items(), key=lambda kv: kv[0])):
            big = max(mem, key=lambda r: r['area_sf'])
            area = sum(r['area_sf'] for r in mem)
            use = big['use']
            sp = dict(id=gi, keys=[r['key'] for r in mem], name=big['name'] or big['key'], use=use, storey=big['storey'], unit=big['unit'],
                      area=area, heat=sum(r['heat_btuh'] for r in mem), cool=sum(r['cool_btuh'] for r in mem),
                      heat_share=sum(r['heat_share'] for r in mem), cool_share=sum(r['cool_share'] for r in mem),
                      walls=[dict(w, room=r['key']) for r in mem for w in r['walls']], centroid=tuple(big['centroid']), big=big['key'],
                      habitable=use in HEADABLE and area >= HP.HABITABLE_MIN_SF, fragment=use in HEADABLE and area < HP.HABITABLE_MIN_SF)
            self.spaces.append(sp)
            for r in mem:
                self.space_of[r['key']] = gi
            if len(mem) > 1:
                merged.append(f"{sp['name']} ({sp['storey']}: {len(mem)} pieces, {area:.0f} sf)")
        if merged:
            self.notes.append('tracer fragments merged into one space (same name, touching): ' + '; '.join(merged))
        frags = [s for s in self.spaces if s['fragment']]
        if frags:
            self.notes.append(f"under {HP.HABITABLE_MIN_SF:.0f} sf (IRC R304.1 - not a habitable room), so carried by a neighbour and never given a head or an ERV supply: "
                              + ', '.join(f"{s['name']} {s['area']:.0f} sf" for s in frags))

    # ============================================================ zoning (ductless)
    def zones(self, unit):
        S = [s for s in self.spaces if s['unit'] == unit]
        ids = [s['id'] for s in S]
        sp = {s['id']: s for s in S}
        parent = {i: i for i in ids}

        def find(k):
            while parent[k] != k:
                parent[k] = parent[parent[k]]
                k = parent[k]
            return k
        adj = defaultdict(set)
        open_uses = HP.ZONE_OPEN_USES | {'circulation', 'stair'}
        for d in self.doors:
            rs = [self.space_of.get(k) for k in (d.get('rooms') or [])]
            rs = [x for x in rs if x in sp]
            if len(rs) != 2 or rs[0] == rs[1]:
                continue
            a, b = rs
            adj[a].add(b); adj[b].add(a)
            typ = str(d.get('type', ''))
            opn = typ.startswith(OPEN_TYPES)
            ua, ub = sp[a]['use'], sp[b]['use']
            if opn and ua in open_uses and ub in open_uses and 'bedroom' not in (ua, ub) and sp[a]['storey'] == sp[b]['storey'] \
                    and not sp[a]['fragment'] and not sp[b]['fragment']:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[rb] = ra
        groups = defaultdict(list)
        for i in ids:
            groups[find(i)].append(i)
        gid_of = {i: g for g, mem in groups.items() for i in mem}
        headed = {g for g, mem in groups.items() if any(sp[i]['habitable'] for i in mem)}

        def gpri(g):
            return min(HOST_PRI.get(sp[i]['use'], 2) for i in groups[g] if sp[i]['habitable'])

        def gcent(g):
            return sp[max(groups[g], key=lambda i: sp[i]['area'])]['centroid']
        carried = defaultdict(list)
        for g, mem in groups.items():
            if g in headed:
                continue
            private = all(sp[i]['use'] in PRIVATE or sp[i]['fragment'] for i in mem)
            # breadth-first through the non-headed rooms, doors only
            seen, frontier, cands = {g}, [g], []
            for depth in range(1, 5):
                nxt = []
                for x in frontier:
                    for i in groups[x]:
                        for nb in adj[i]:
                            y = gid_of[nb]
                            if y in seen:
                                continue
                            seen.add(y)
                            if y in headed:
                                cands.append((depth, gpri(y), y))
                            else:
                                nxt.append(y)
                frontier = nxt
            if cands:
                key = (lambda c: (c[0], c[1])) if private else (lambda c: (c[1], c[0]))
                # a bedroom takes its own closet and bath; a hall, landing or laundry goes to the living zone it reaches
                best = min(cands, key=key)[2]
            else:
                # no traced door: the nearest headed zone on the storey - a bedroom counts double for anything but a closet or bath
                c = gcent(g)
                same = [h for h in headed if sp[groups[h][0]]['storey'] == sp[mem[0]]['storey']] or list(headed)
                pen = (lambda h: 1.0) if private else (lambda h: 2.0 if gpri(h) >= 1 else 1.0)
                best = min(same, key=lambda h: near(c, gcent(h)) * pen(h)) if same else None
            if best is not None:
                carried[best] += mem
        out = []
        for g in headed:
            mem = groups[g]
            ks = [k for i in mem for k in sp[i]['keys']]
            ck = [k for i in carried[g] for k in sp[i]['keys']]
            heat = sum(self.rooms[k]['heat_btuh'] for k in ks + ck)
            cool = sum(self.rooms[k]['cool_btuh'] for k in ks + ck)
            host = min((i for i in mem if sp[i]['habitable']), key=lambda i: (HOST_PRI.get(sp[i]['use'], 2), -sp[i]['area']))
            out.append(dict(spaces=mem, carries=carried[g], rooms=ks, carried_rooms=ck, host=host, host_key=sp[host]['big'], storey=sp[host]['storey'],
                            heat=heat, cool=cool, names=[sp[i]['name'] for i in mem], carried_names=[sp[i]['name'] for i in carried[g]]))
        # the ventilation load arrives with the air - shared out by the heat each zone already loses
        un = next(u for u in self.L['units'] if u['name'] == unit)
        tot = sum(z['heat'] for z in out) or 1
        for z in out:
            z['heat'] += round(un['vent_heat_btuh'] * z['heat'] / tot)
        # a zone too small for a head joins its neighbour on the storey (a bedroom keeps its own)
        merged = True
        while merged:
            merged = False
            for z in sorted(out, key=lambda z: z['heat']):
                if max(z['heat'], z['cool']) >= HP.HEAD_MIN_LOAD or sp[z['host']]['use'] == 'bedroom':
                    continue
                others = [o for o in out if o is not z and o['storey'] == z['storey'] and sp[o['host']]['use'] != 'bedroom']
                if not others:
                    continue
                o = min(others, key=lambda o: near(sp[o['host']]['centroid'], sp[z['host']]['centroid']))
                for k in ('spaces', 'carries', 'rooms', 'carried_rooms', 'names', 'carried_names'):
                    o[k] = o[k] + z[k]
                o['heat'] += z['heat']; o['cool'] += z['cool']
                out.remove(z); merged = True
                break
        self.sp = {s['id']: s for s in self.spaces}
        return sorted(out, key=lambda z: (self.zof(z['storey']), -z['heat']))

    def habitable_spaces(self, unit):
        """what WA counts for outdoor-air inlets: each habitable SPACE - the open plan is one"""
        n = 0
        for z in self.zones(unit):
            n += 1
        return n

    def head_size(self, heat, cool):
        for n in HP.HEAD_SIZES:
            if HP.capacity_at(n * 1000, self.T, 'ductless') >= heat and n * 1000 >= 0.9 * cool:
                return n
        return None

    def head_pos(self, space):
        walls = sorted([w for w in space['walls'] if w.get('beyond') != 'garage'], key=lambda w: -w['ft'])
        if walls:
            w = walls[0]
            m = ((w['a'][0] + w['b'][0]) / 2, (w['a'][1] + w['b'][1]) / 2)
            return (m[0] - w['n'][0] * 0.4, m[1] - w['n'][1] * 0.4), True, w
        r = self.rooms[space['big']]
        P = r['poly']
        best = max(range(len(P)), key=lambda i: C.dist(P[i], P[(i + 1) % len(P)]))
        a, b = P[best], P[(best + 1) % len(P)]
        c = r['centroid']
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        d = C.dist(m, c) or 1
        return (m[0] + (c[0] - m[0]) / d * 0.4, m[1] + (c[1] - m[1]) / d * 0.4), False, None

    # ============================================================ refrigerant routing
    def main_cover(self):
        cov = self.lo.cover.get(self.main)
        return cov

    def drop_point(self, pos, storey):
        """where a line set from `pos` on `storey` goes down to the crawl: straight down when the main floor is under
        it (stacked walls), else the nearest point of the main-floor footprint (a run in the floor cavity first)"""
        if storey == self.main:
            return tuple(pos), 0.0
        cov = self.main_cover()
        if cov is None:
            return tuple(pos), 0.0
        from shapely.geometry import Point
        from shapely.ops import nearest_points
        p = Point(pos)
        if cov.buffer(0.5).contains(p):
            return tuple(pos), 0.0
        q = nearest_points(cov, p)[0]
        return (q.x, q.y), C.dist(pos, (q.x, q.y))

    def route_lineset(self, pos, storey, z_top, ex):
        """concealed (crawl): down the stud bay under the head (or the nearest stacked wall), across the crawl on
        strut / J-hooks (an L along the joists), out the rim beside the outdoor unit. exterior: through the wall
        behind the head, down a line-hide cover, along the foundation to the unit.
        Returns dict(ft, pts, exterior_ft, cond_ft, drop_ft)"""
        o = ex['outside']
        if self.route_mode == 'exterior' or self.found != 'crawl':
            down = max(0.0, z_top - 1.0)
            along = manhattan(pos, o)
            pts = [(pos[0], pos[1], z_top), (pos[0], pos[1], 1.0), (o[0], pos[1], 1.0), (o[0], o[1], 1.0)]
            ext = down + along + 1.0
            return dict(ft=ext + 2.0, pts=pts, exterior_ft=ext, cond_ft=down + 1.0, drop_ft=down)
        d, cav = self.drop_point(pos, storey)
        q = ex['inside']
        drop = z_top - CRAWL_Z
        crawl = manhattan(d, q)
        pts = [(pos[0], pos[1], z_top)]
        if cav > 0.05:
            zc = self.zof(storey) - 0.5
            pts += [(pos[0], pos[1], zc), (d[0], d[1], zc)]
        pts += [(d[0], d[1], CRAWL_Z), (q[0], d[1], CRAWL_Z), (q[0], q[1], CRAWL_Z), (o[0], o[1], 0.5)]
        ft = cav + drop + crawl + 2.5 + 2.0            # + out through the rim to the unit, + two service loops
        # condensate: down with the lines, then the shortest way out of the crawl to daylight (not into the crawl)
        ex2 = self.exit_point(d, self.main)
        cond = drop + cav + (manhattan(d, ex2['inside']) if ex2 else crawl) + 2.0
        return dict(ft=ft, pts=pts, exterior_ft=0.0, cond_ft=cond, drop_ft=drop, cavity_ft=cav)

    def overhang_note(self, pos, what):
        """an outdoor unit under a cantilevered upper storey: out of the snow, but its vibration goes into the room above"""
        from shapely.geometry import Point
        for s in self.storeys[1:]:
            cov = self.lo.cover.get(s['name'])
            if cov is not None and cov.contains(Point(pos)):
                above = [r for r in self.L['rooms'] if r['storey'] == s['name'] and self.lo.poly[r['key']].buffer(0.5).contains(Point(pos))]
                nm = above[0]['name'] if above else s['name']
                self.check('practice', what, f"it sits under the {s['name']} storey ({nm} above): out of the snow, but set it on a ground stand with isolation pads, "
                           'never a wall bracket - compressor vibration carries into the room above')
                return

    def outdoor_spot(self, target, unit, used):
        """1. job.json hvac.outdoor.pos; 2. the electrician's condenser / mini-split disconnect for this unit (one per
        system, snapped to the wall); 3. the open-air wall of the main storey nearest the equipment"""
        O = self.H.get('outdoor') or {}
        uname = unit if len(self.L['units']) > 1 else None
        if O.get('pos'):
            return self.exit_point(tuple(O['pos']), self.main, uname, None), 'job.json hvac.outdoor.pos'
        cands = [d for d in self.elec_find(r'mini-split outdoor|heat pump condenser|condenser|outdoor unit', unit) if id(d) not in used]
        if cands and not O.get('ignore_electrical'):
            d = min(cands, key=lambda d: near(d['pos'], target))
            used.add(id(d))
            ex = self.exit_point(tuple(d['pos']), self.main, uname, O.get('side'))
            if ex:
                return ex, f"at the electrician's {d.get('appliance')} ({self.rname(d.get('room'))}, {self.dev_src})"
        return self.exit_point(target, self.main, uname, O.get('side')), 'nearest open-air wall to the equipment'

    # ============================================================ ductless
    def design_ductless(self, un):
        unit = un['name']
        zs = self.zones(unit)
        sp = self.sp
        heads = []
        for z in zs:
            n = self.head_size(z['heat'], z['cool'])
            count = 1
            if n is None:
                count = math.ceil(max(z['heat'] / HP.capacity_at(24000, self.T, 'ductless'), z['cool'] / 24000.0))
                n = self.head_size(z['heat'] / count, z['cool'] / count) or 24
            host = sp[z['host']]
            pos, on_ext, wall = self.head_pos(host)
            for i in range(count):
                p = pos if i == 0 else (pos[0] + 4.0 * i * (-wall['n'][1] if wall else 1.0), pos[1] + 4.0 * i * (wall['n'][0] if wall else 0.0))
                heads.append(dict(zone=z, kbtuh=n, pos=p, storey=z['storey'], host=z['host_key'], host_name=host['name'], exterior_wall=on_ext,
                                  heat=round(z['heat'] / count), cool=round(z['cool'] / count), n=list(wall['n']) if wall else None))
            mn = HP.min_output_at(n * 1000, self.T, 'ductless')
            if mn > HP.MIN_COMP_MAX * z['heat'] / count:
                self.check('practice', host['name'], f"a {n}k head turns down to ~{mn:,.0f} Btuh at {self.T:g} F against a {z['heat'] / count:,.0f} Btuh zone - over Manual S's 0.80 x load: it will cycle; "
                           'carry this room from the zone next door or serve it with a slim ducted unit')
        layout = (self.H.get('system') or {}).get('layout') or 'auto'
        forced = (self.H.get('system') or {}).get('outdoor_kbtuh')
        groups = []
        if layout == 'singles' or (layout == 'auto' and len(heads) <= 2 and not forced):
            for h in heads:
                groups.append(dict(kind='single', heads=[h]))
        else:
            groups = self.mz_groups(heads, un['heat_btuh'], forced)
        sysrec = dict(unit=unit, kind='ductless', zones=[], outdoor=[], heads=[], total_heat=un['heat_btuh'], total_cool=un['cool_sens_btuh'] + un['cool_lat_btuh'])
        for z in zs:
            sysrec['zones'].append(dict(host=sp[z['host']]['name'], names=z['names'], carries=z['carried_names'], heat=z['heat'], cool=z['cool'], storey=z['storey']))
        used = set()
        for g in groups:
            self.place_outdoor_and_lines(g, un, sysrec, used)
        cap = sum(o['cap_at_design'] for o in sysrec['outdoor'])
        sysrec['cap_at_design'] = round(cap)
        if cap < un['heat_btuh']:
            self.check('code', f'unit {unit}', f"the outdoor capacity at {self.T:g} F is {cap:,.0f} Btuh against a {un['heat_btuh']:,} Btuh heating load - WSEC 3.7 wants the ductless system to heat the entire dwelling at design temperature; go up a size")
        bath_like = [s for s in self.spaces if s['unit'] == unit and s['use'] in ('bath', 'powder')]
        if bath_like:
            self.notes.append(f"unit {unit}: {len(bath_like)} bath / powder room(s) have no head - they are carried by the zone they open into; "
                              "WSEC allows resistance heat up to 0.5 W/sf or 500 W if a bath needs its own (an option line, not in the base)")
        self.systems.append(sysrec)

    def mz_groups(self, heads, unit_load, forced=None):
        heads = list(heads)

        def fits(n, hs, load):
            return (sum(h['kbtuh'] for h in hs) <= HP.MZ_CONNECT_MAX * n + 0.1 and len(hs) <= HP.MZ_MAX_HEADS[n]
                    and HP.capacity_at(n * 1000, self.T, 'ductless') >= load)
        if forced:
            return [dict(kind='multi', heads=heads, kbtuh=int(forced), forced=True)]
        load = sum(h['heat'] for h in heads)
        for n in HP.MZ_SIZES:
            if fits(n, heads, load):
                return [dict(kind='multi', heads=heads, kbtuh=n)]
        # too much for one: one multi-zone per storey
        by = defaultdict(list)
        for h in heads:
            by[h['storey']].append(h)
        out = []
        for s, hs in by.items():
            ld = sum(h['heat'] for h in hs)
            if len(hs) <= 1:
                out.append(dict(kind='single', heads=hs))
                continue
            n = next((n for n in HP.MZ_SIZES if fits(n, hs, ld)), HP.MZ_SIZES[-1])
            out.append(dict(kind='multi', heads=hs, kbtuh=n))
        return out

    def place_outdoor_and_lines(self, g, un, sysrec, used):
        heads = g['heads']
        cx = sum(h['pos'][0] for h in heads) / len(heads); cy = sum(h['pos'][1] for h in heads) / len(heads)
        ex, why = self.outdoor_spot((cx, cy), un['name'], used)
        if g['kind'] == 'single':
            pid, n = HP.eq_part('eq_ds', max(heads[0]['kbtuh'], 9), [9, 12, 15, 18, 24])
        else:
            n = g['kbtuh']
            pid = f"eq_mz_{n:02d}" if f"eq_mz_{n:02d}" in HP.byId else HP.eq_part('eq_mz', n, HP.MZ_SIZES)[0]
        cap = HP.capacity_at(n * 1000, self.T, 'ductless')
        o = dict(part=pid, kbtuh=n, heads=len(heads), pos=list(ex['outside']), wall=list(ex['inside']), facing=ex['facing'], where=why,
                 cap_at_design=round(cap), kind=g['kind'], forced=bool(g.get('forced')), unit=un['name'])
        sysrec['outdoor'].append(o)
        self.fit(pid, 1, f"{g['kind']}-zone outdoor unit, {n}k nominal, ~{cap:,.0f} Btuh at {self.T:g} F (ResStock cold-climate curve), {why}, {ex['facing']} wall")
        self.item('outdoor', pid, ex['outside'], 0.0, self.main, note=f'{n}k outdoor unit', kbtuh=n, n=list(ex['n']))
        self.overhang_note(ex['outside'], f"{n}k outdoor unit (unit {un['name']})")
        self.fit('rp_pad', 1, 'outdoor unit pad'); self.fit('rp_vib', 1, ''); self.fit('rp_stand', 1, 'snow / drainage stand (NW practice: 12-18 in clear of grade)')
        total = 0.0
        extra_oz = 0.0
        for h in heads:
            hid = f"eq_head_{h['kbtuh']:02d}"
            nm = h['host_name']
            self.fit(hid, 1, f"{nm}: zone {', '.join(h['zone']['names'])[:80]} - heat {h['heat']:,} / cool {h['cool']:,} Btuh")
            z_top = self.zof(h['storey']) + HEAD_Z
            self.item('head', hid, h['pos'], z_top, h['storey'], room=h['host'], note=f"{h['kbtuh']}k head", kbtuh=h['kbtuh'], n=h.get('n'))
            sysrec['heads'].append(dict(room=nm, key=h['host'], kbtuh=h['kbtuh'], heat=h['heat'], cool=h['cool'], storey=h['storey'], exterior_wall=h['exterior_wall']))
            R = self.route_lineset(h['pos'], h['storey'], z_top, ex)
            ft = R['ft']
            liq, suc = HP.line_set(h['kbtuh'])
            part = {(0.25, 0.375): 'rp_ls_1438', (0.25, 0.5): 'rp_ls_1412', (0.375, 0.625): 'rp_ls_3858', (0.375, 0.75): 'rp_ls_3834'}[(liq, suc)]
            self.run('refrigerant', f'{liq:g}x{suc:g}', R['pts'], f"line set {nm} head -> outdoor ({self.route_mode})", h['storey'], ft)
            self.line(part, ft, f"{nm} {h['kbtuh']}k head, {ft:.0f} ft {self.route_mode}")
            self.line('rp_comm', ft, 'with the line set (powers and talks to the head)')
            self.run('condensate', 0.75, [(p[0], p[1], p[2] - 0.15) for p in R['pts'][:max(2, len(R['pts']) - 3)]], 'condensate down with the line set, then out to grade', h['storey'], R['cond_ft'])
            self.line('cd_line', R['cond_ft'], 'condensate: gravity, 1/8 in per ft, to daylight (M1411.3) - never into the crawl')
            if not h['exterior_wall'] and self.found != 'crawl':
                self.fit('cd_pump', 1, f"{nm}: head on an interior wall over a slab - no fall to outside")
            if R['exterior_ft']:
                self.line('rp_linehide', R['exterior_ft'], 'exterior run in a painted cover')
                self.fit('rp_lh_fit', 3, 'wall inlet, elbow, end')
                self.fit('rp_sleeve', 1, 'through the wall behind the head')
            self.fit('sp_blocking', 1, 'head mounting plate blocking')
            if self.route_mode == 'concealed':
                n_up = 1 if h['storey'] != self.main else 0
                self.fit('sp_bore', 2 + 2 * n_up, 'plates the line set passes (bottom plate + subfloor per storey)')
                self.fit('sp_plate', 2 + 2 * n_up, 'nail plates at those bores')
            total += ft
            pre = HP.LS_PRECHARGE_FT['single'] if g['kind'] == 'single' else HP.LS_PRECHARGE_FT['multi_per_head']
            extra_oz += max(0.0, ft - pre) * HP.LS_ADD_OZ_PER_FT.get(liq, 0.22)
            lim = HP.LS_MAX_FT['multi_branch'] if g['kind'] == 'multi' else (HP.LS_MAX_FT['single_small'] if h['kbtuh'] <= 12 else HP.LS_MAX_FT['single'])
            if ft > lim:
                self.check('practice', nm, f"line set {ft:.0f} ft > the ~{lim:.0f} ft this unit class allows [U - the model's manual governs] - move the outdoor unit or the head")
            if ft < HP.LS_MIN_FT:
                self.check('practice', nm, f"line set {ft:.0f} ft < the ~{HP.LS_MIN_FT:.0f} ft minimum most makers want - coil the extra behind the unit")
        if self.route_mode == 'concealed':
            self.fit('rp_sleeve', 1, 'rim-joist penetration for the line-set bundle beside the outdoor unit')
        if g['kind'] == 'multi':
            lim = HP.LS_MZ_TOTAL_FT.get(n, 262.0)
            if total > lim:
                self.check('practice', 'multi-zone', f'total piping {total:.0f} ft > ~{lim:.0f} ft for a {n}k multi-zone [U] - split the zones over two outdoor units')
        self.fit('rp_nitro', 1, 'per refrigerant system')
        if extra_oz > 0:
            self.fit('rp_charge', math.ceil(extra_oz / 16 * 10) / 10, f'{extra_oz:.0f} oz past the pre-charged length [U: the maker\'s oz / ft]')
        self.fit('cm_startup', 1, f'{n}k system')
        o['lineset_ft'] = round(total)

    # ============================================================ ducted
    def find_room(self, want, storey=None):
        """a room of the interior - kept or skipped (a mechanical room under the stairs is usually skipped) - by
        key or name, 'storey/NAME'"""
        w = str(want).upper()
        st = None
        if '/' in w and w.split('/')[0].lower() in self.st:
            st, w = w.split('/')[0].lower(), w.split('/', 1)[1]
        st = st or storey
        for r in self.all_rooms.values():
            if st and r['storey'] != st:
                continue
            if r['key'].upper() == str(want).upper() or (r.get('name') or '').upper() == w:
                return r
        for r in self.all_rooms.values():
            if st and r['storey'] != st:
                continue
            if w and re.search(re.escape(w), (r.get('name') or '').upper()):
                return r
        return None

    def ahu_spot(self, unit, storey, want=None, elec=True):
        """where an air handler / ducted indoor unit sits: job.json names the room; else the electrician's air-handler
        junction (unless it is in the garage or the shop); else a MECH / LAUNDRY / storage / hall-closet room"""
        def pack(r, src, pos=None):
            p = tuple(pos) if pos else tuple(C.centroid([tuple(q) for q in r['poly']]))
            return dict(pos=p, storey=r['storey'], name=r.get('name') or r['key'], key=r['key'], src=src,
                        inside=not r.get('skip') or (r.get('use') == 'mech'))
        if want:
            r = self.find_room(want, storey)
            if r:
                return pack(r, f'job.json ({want})')
            self.check('data', 'air handler', f"job.json names '{want}' for the air handler - no such room traced; placed by rule")
        if elec:
            for d in self.elec_find(r'air handler|furnace', unit):
                r = self.all_rooms.get(d.get('room'))
                if not r or r['storey'] != storey:
                    continue
                nm = (r.get('name') or '').upper()
                if r.get('use') == 'garage' or re.search(r'GARAGE|SHOP|WORKBENCH', nm) or r['key'] in self.lo.excluded:
                    self.notes.append(f"the electrician put the air handler in {r.get('name')} (outside the conditioned space) - not followed; tell the electrician where it moved")
                    continue
                return pack(r, f"the electrician's air-handler junction ({self.dev_src})", d['pos'])
        rs = [r for r in self.all_rooms.values() if r['storey'] == storey and (unit is None or len(self.L['units']) == 1 or self.unit_at(C.centroid([tuple(q) for q in r['poly']])) == unit)]
        for pat in (r'MECH', r'LAUNDRY|UTIL', r'STOR', r'CLOS|CLST|HALL|LANDING'):
            for r in rs:
                if re.search(pat, (r.get('name') or '').upper()) and not re.search(r'GARAGE|SHOP', (r.get('name') or '').upper()):
                    return pack(r, f'rule: first {pat} room')
        kept = [r for r in rs if not r.get('skip')]
        if not kept:
            return None
        cx = sum(C.centroid([tuple(q) for q in r['poly']])[0] for r in kept) / len(kept)
        cy = sum(C.centroid([tuple(q) for q in r['poly']])[1] for r in kept) / len(kept)
        r = min(kept, key=lambda r: near(C.centroid([tuple(q) for q in r['poly']]), (cx, cy)))
        return pack(r, 'rule: the most central room')

    def central_size(self, heat, cool):
        """the smallest ducted heat pump whose capacity AT DESIGN carries the load (Manual S 2023: >= 1.00 x; taken at
        0.95 x with the strip covering the rest) and whose nominal covers 0.9 x the cooling load"""
        for n in HP.CENTRAL_SIZES:
            if HP.capacity_at(n * 1000, self.T, 'ducted') >= HP.HSF_ACCEPT * heat and n * 1000 >= 0.9 * cool:
                return n, False
        return HP.CENTRAL_SIZES[-1], True

    def design_cfm(self, cap_btuh, heat, cool_sens):
        """blower airflow at the design point: 375 cfm per ton of capacity at design, never under what the heating load
        needs at a 105 F heat-pump supply or the sensible cooling load at 55 F leaving air"""
        return max(HP.CFM_PER_TON_DESIGN * cap_btuh / 12000.0, heat / (HP.AIR_SENS * (HP.SAT_HP - HP.INDOOR_HEAT_F)),
                   cool_sens / (HP.AIR_SENS * (HP.INDOOR_COOL_F - HP.LAT_COOL)))

    def design_ducted(self, un, multizone=False):
        unit = un['name']
        sysd = self.H.get('system') or {}
        rooms = [self.rooms[k] for k in un['rooms']]
        storeys = sorted({r['storey'] for r in rooms}, key=lambda s: self.zof(s))
        sysrec = dict(unit=unit, kind='ducted_multizone' if multizone else 'ducted', outdoor=[], indoor=[], registers=[], returns=[],
                      total_heat=un['heat_btuh'], total_cool=un['cool_sens_btuh'] + un['cool_lat_btuh'])
        fam = 'ductless' if multizone else 'ducted'
        # ---- equipment
        if multizone:
            forced = sysd.get('outdoor_kbtuh')
            n = int(forced) if forced else next((n for n in HP.MZ_SIZES if HP.capacity_at(n * 1000, self.T, fam) >= un['heat_btuh']), HP.MZ_SIZES[-1])
            pid = f'eq_mz_{n:02d}' if f'eq_mz_{n:02d}' in HP.byId else HP.eq_part('eq_mz', n, HP.MZ_SIZES)[0]
        else:
            n, short = self.central_size(un['heat_btuh'], un['cool_sens_btuh'] + un['cool_lat_btuh'])
            pid = f'eq_hp_{n:02d}'
            if short:
                self.check('practice', f'unit {unit}', f"the heating load {un['heat_btuh']:,} Btuh is more than the biggest catalog heat pump carries at {self.T:g} F - two systems")
        cap = HP.capacity_at(n * 1000, self.T, fam)
        if not multizone:
            hsf = cap / max(1, un['heat_btuh'])
            i = HP.CENTRAL_SIZES.index(n)
            if i > 0:
                n2 = HP.CENTRAL_SIZES[i - 1]
                c2 = HP.capacity_at(n2 * 1000, self.T, 'ducted')
                if c2 / max(1, un['heat_btuh']) >= 0.85 and un['heat_btuh'] - c2 <= HP.SUPP_SMALL_BTUH:
                    self.notes.append(f"alternate: a {n2}k ({n2 / 12:g} ton) carries {c2:,.0f} Btuh at {self.T:g} F ({c2 / un['heat_btuh']:.2f} x the load); the 5 kW strip covers the "
                                      f"{un['heat_btuh'] - c2:,.0f} Btuh shortfall (Manual S: <= 5 kW under 15,000) - one size down, a cheaper unit and a lower balance point cost; Genaro's call")
            if hsf < HP.HSF_MIN:
                self.notes.append(f"the {n}k carries {hsf:.2f} x the heating load at {self.T:g} F - inside the 5 % the takeoff accepts; the strip carries the rest")
        # ---- the indoor unit(s): one air handler (ducted), one ducted indoor unit per storey (ducted multi-zone)
        ahus = []
        if multizone:
            for s in storeys:
                srooms = [r for r in rooms if r['storey'] == s]
                sheat = sum(r['heat_btuh'] for r in srooms) + un['vent_heat_btuh'] * sum(r['heat_btuh'] for r in srooms) / max(1, un['heat_rooms_btuh'])
                scool = sum(r['cool_btuh'] for r in srooms)
                kb = next((k for k in HP.DUCTED_INDOOR_SIZES if HP.capacity_at(k * 1000, self.T, 'ductless') >= sheat and k * 1000 >= 0.9 * scool), HP.DUCTED_INDOOR_SIZES[-1])
                spot = self.ahu_spot(unit, s, sysd.get('ahu_room') if s == self.main else sysd.get('ahu_room_' + s), elec=(s == self.main))
                cfm = self.design_cfm(HP.capacity_at(kb * 1000, self.T, 'ductless'), sheat, scool)
                ahus.append(dict(storey=s, spot=spot, kbtuh=kb, cfm=cfm, rooms=srooms, part=f'eq_duin_{kb:02d}', heat=sheat))
        else:
            spot = self.ahu_spot(unit, self.main, sysd.get('ahu_room'))
            cfm = self.design_cfm(cap, un['heat_btuh'], un['cool_sens_btuh'])
            ahus.append(dict(storey=self.main, spot=spot, kbtuh=n, cfm=cfm, rooms=rooms, part=f'eq_ahu_{n:02d}', heat=un['heat_btuh']))
        # ---- the outdoor unit and its line sets
        tgt = ahus[0]['spot']['pos'] if ahus[0]['spot'] else tuple(rooms[0]['centroid'])
        ex, why = self.outdoor_spot(tgt, unit, set())
        o = dict(part=pid, kbtuh=n, pos=list(ex['outside']), wall=list(ex['inside']), facing=ex['facing'], cap_at_design=round(cap), kind='multi' if multizone else 'central',
                 forced=bool(sysd.get('outdoor_kbtuh')), where=why, unit=unit)
        sysrec['outdoor'].append(o)
        self.fit(pid, 1, f"{'multi-zone' if multizone else 'ducted heat pump'} outdoor unit {n}k (~{cap:,.0f} Btuh at {self.T:g} F), {why}, {ex['facing']} wall"
                 + (' - AS SPECIFIED on the plan' if o['forced'] else ''))
        self.item('outdoor', pid, ex['outside'], 0.0, self.main, note=f'{n}k outdoor unit', kbtuh=n, n=list(ex['n']))
        self.overhang_note(ex['outside'], f'{n}k outdoor unit')
        self.fit('rp_pad', 1, 'outdoor unit pad'); self.fit('rp_vib', 1, ''); self.fit('rp_stand', 1, 'snow / drainage stand')
        if not multizone:
            deficit = max(0.0, un['heat_btuh'] - cap)
            if deficit <= HP.SUPP_SMALL_BTUH:
                strip = 5
            else:
                need = 0.95 * deficit / 3412.0
                strip = next((k for k in (5, 8, 10, 15) if k >= need), 15)
            self.fit(f'eq_strip_{strip:02d}', 1, f'backup / defrost tempering {strip} kW (heat-pump shortfall at design {deficit:,.0f} Btuh; Manual S: <= 5 kW while it is under 15,000) - '
                     'the thermostat locks it out while the compressor carries the load (WSEC R403.1.2)')
            sysrec['backup_kw'] = strip
            sysrec['deficit_btuh'] = round(deficit)
        total_ls = 0.0
        for a in ahus:
            sp_ = a['spot']
            apos = sp_['pos'] if sp_ else tuple(rooms[0]['centroid'])
            az = self.zof(a['storey'])
            where = f"{sp_['name']} ({a['storey']}; {sp_['src']})" if sp_ else '?'
            self.fit(a['part'], 1, f"{'ducted indoor unit' if multizone else 'air handler'} {a['kbtuh']}k in {where}")
            self.item('ahu', a['part'], apos, az, a['storey'], room=sp_['key'] if sp_ else None, note=f"{a['kbtuh']}k {'ducted unit' if multizone else 'air handler'}", kbtuh=a['kbtuh'])
            sysrec['indoor'].append(dict(part=a['part'], kbtuh=a['kbtuh'], room=sp_['name'] if sp_ else None, storey=a['storey'], cfm=round(a['cfm']), src=sp_['src'] if sp_ else None))
            R = self.route_lineset(apos, a['storey'], az + 1.0, ex)
            ft = R['ft']
            liq, suc = HP.line_set(n if not multizone else a['kbtuh'])
            part = {(0.25, 0.375): 'rp_ls_1438', (0.25, 0.5): 'rp_ls_1412', (0.375, 0.625): 'rp_ls_3858', (0.375, 0.75): 'rp_ls_3834'}[(liq, suc)]
            self.run('refrigerant', f'{liq:g}x{suc:g}', R['pts'], f"line set {sp_['name'] if sp_ else ''} -> outdoor", a['storey'], ft)
            self.line(part, ft, f"{a['kbtuh']}k indoor unit, {ft:.0f} ft"); self.line('rp_comm', ft, 'with the line set')
            total_ls += ft
            # condensate: gravity to daylight; a pan + float switch where the unit sits over finished space
            self.line('cd_line', max(8.0, R['cond_ft']), 'air handler condensate to an approved discharge'); self.fit('cd_trap', 1, 'trap + cleanout tee')
            if a['storey'] != self.main:
                self.fit('cd_pan', 1, f"{a['storey']} unit sits over finished space (M1411.3.1)")
            self.duct_system(a, apos, sysrec, un, multizone)
        self.fit('rp_sleeve', 1, 'rim penetration for the line set')
        self.fit('rp_nitro', 1, 'per refrigerant system')
        liq0 = HP.line_set(n)[0]
        extra = max(0.0, total_ls - HP.LS_PRECHARGE_FT['central'] * len(ahus)) * HP.LS_ADD_OZ_PER_FT.get(liq0, 0.54)
        if extra:
            self.fit('rp_charge', math.ceil(extra / 16 * 10) / 10, f'{extra:.0f} oz past the pre-charge [U: the maker\'s oz / ft]')
        self.fit('cm_startup', 1, f'{n}k system')
        self.fit('eq_tstat', len(ahus), 'WSEC R403.1.1 programmable; heat-pump aux lockout R403.1.2')
        self.fit('tr_filter', len(ahus), 'first filter set')
        self.fit('cm_balance', len(ahus), 'register balance')
        o['lineset_ft'] = round(total_ls)
        sysrec['cap_at_design'] = round(cap)
        self.systems.append(sysrec)

    def trunk_tree(self, origin, targets):
        """a trunk along the long axis of the targets through the origin, a branch square off it to each target:
        (a0, a1, along_x, trunk_ft, [(foot, target, ft)])"""
        xs = [t[0] for t in targets] + [origin[0]]; ys = [t[1] for t in targets] + [origin[1]]
        along_x = (max(xs) - min(xs)) >= (max(ys) - min(ys))
        if along_x:
            a0, a1 = (min(xs), origin[1]), (max(xs), origin[1])
        else:
            a0, a1 = (origin[0], min(ys)), (origin[0], max(ys))
        br = []
        for t in targets:
            foot = (t[0], a0[1]) if along_x else (a0[0], t[1])
            br.append((foot, t, C.dist(foot, t)))
        return a0, a1, along_x, C.dist(a0, a1), br

    def duct_system(self, a, apos, sysrec, un, multizone):
        """registers under the exterior walls of every served SPACE, a trunk per storey, flex branches, a central
        return per storey and a transfer path out of every closed room with a supply"""
        keys = {r['key'] for r in a['rooms']}
        spaces = [s for s in self.spaces if any(k in keys for k in s['keys'])]
        ahu_key = (a['spot'] or {}).get('key')
        served = [s for s in spaces if s['use'] in SUPPLY_USES and s['area'] >= 25 and not s['fragment'] and ahu_key not in s['keys']]
        share_tot = sum(max(s['heat_share'], s['cool_share']) for s in served) or 1
        ducts_out = (self.H.get('ducts') or 'inside') not in ('inside', 'crawl_conditioned')
        per_storey = defaultdict(list)
        for s in served:
            cfm = max(30.0, a['cfm'] * max(s['heat_share'], s['cool_share']) / share_tot)
            nreg = max(1, math.ceil(cfm / HP.REG_MAX_CFM['floor_4x10']))
            walls = sorted([w for w in s['walls'] if w.get('beyond') != 'garage'], key=lambda w: -w['ft'])
            for i in range(nreg):
                if walls:
                    w = walls[i % len(walls)]
                    k = i // len(walls)
                    per = math.ceil(nreg / len(walls))
                    t = (k + 1) / (per + 1)
                    q = (w['a'][0] + (w['b'][0] - w['a'][0]) * t - w['n'][0] * REG_INSET, w['a'][1] + (w['b'][1] - w['a'][1]) * t - w['n'][1] * REG_INSET)
                else:
                    q = tuple(s['centroid'])
                per_storey[s['storey']].append(dict(pos=q, cfm=cfm / nreg, space=s))
        for st_, regs in per_storey.items():
            z_floor = self.zof(st_)
            zd = CRAWL_Z if (st_ == self.main and self.found == 'crawl') else z_floor - 0.6
            a0, a1, along_x, tlen, br = self.trunk_tree(apos, [g['pos'] for g in regs])
            cfm_s = sum(g['cfm'] for g in regs)
            trunk_d = HP.round_for(cfm_s, flex=False)
            riser = 0.0
            if st_ != a['storey']:
                riser = abs(self.zof(st_) - self.zof(a['storey'])) + 1.0
                self.run('supply', trunk_d, [(apos[0], apos[1], self.zof(a['storey']) + 1.0), (apos[0], apos[1], zd)], f'supply riser to the {st_} storey (duct chase)', st_)
            self.run('trunk', trunk_d, [(a0[0], a0[1], zd), (a1[0], a1[1], zd)], f'{st_} supply trunk {trunk_d} in, {cfm_s:.0f} cfm', st_)
            self.line('dt_trunk', tlen + riser, f'{st_}: {trunk_d} in equivalent, {cfm_s:.0f} cfm' + (' - reducing past 24 ft' if tlen > HP.TRUNK_MAX_FT else ''))
            if ducts_out and st_ == self.main and self.found == 'crawl':
                self.line('dt_wrap', tlen, f'{st_} trunk in the vented crawl - R-8 (WSEC R403.3.1)')
            for g, (foot, p, L0) in zip(regs, br):
                L = L0 + 2.0 + (0.0 if st_ == self.main else 1.0)
                d = HP.round_for(g['cfm'], flex=True)
                nm = g['space']['name']
                self.run('supply', d, [(foot[0], foot[1], zd), (p[0], p[1], zd), (p[0], p[1], z_floor)], f"branch to {nm} {g['cfm']:.0f} cfm", st_, L)
                self.line(f'dt_flex_{d:02d}', L, f"{nm}: {g['cfm']:.0f} cfm")
                self.fit('dt_takeoff', 1, ''); self.fit('dt_boot', 1, ''); self.fit('tr_reg_floor', 1, nm)
                self.fit('dt_hanger', math.ceil(L / 4), '')
                self.item('register', 'tr_reg_floor', p, z_floor, st_, room=g['space']['big'], cfm=round(g['cfm']))
                sysrec['registers'].append(dict(room=nm, storey=st_, cfm=round(g['cfm']), duct_in=d))
            self.fit('dt_hanger', math.ceil(tlen / 8), 'trunk')
            # the return: a central grille in a hall / circulation space of the storey
            circ = [s for s in spaces if s['storey'] == st_ and s['use'] in ('circulation', 'stair', 'living') and not s['fragment']]
            rr = min(circ, key=lambda s: near(s['centroid'], apos)) if circ else None
            if rr:
                rpos = tuple(rr['centroid'])
                rd = HP.round_for(cfm_s, flex=False)
                grille = HP.return_grille(cfm_s)
                rl = manhattan(rpos, apos) + (abs(self.zof(st_) - self.zof(a['storey'])) if st_ != a['storey'] else 0) + 3.0
                zr = z_floor + (self.plate(st_) - 0.5 if st_ != self.main else 0.5)
                self.run('return', rd, [(rpos[0], rpos[1], zr), (rpos[0], rpos[1], zd), (apos[0], rpos[1], zd), (apos[0], apos[1], zd)], f'{st_} central return {rd} in', st_, rl)
                self.line('dt_return', rl, f'{st_} central return {rd} in, {cfm_s:.0f} cfm, {grille} filter grille')
                self.fit('tr_return', 1, f"{rr['name']} ({st_}): {grille} at <= 300 fpm")
                self.item('return', 'tr_return', rpos, zr, st_, room=rr['big'], cfm=round(cfm_s))
                sysrec['returns'].append(dict(room=rr['name'], storey=st_, cfm=round(cfm_s), duct_in=rd, grille=grille))
            # closed-door rooms need a way back to the return (+/- 3 Pa)
            for g in {id(g['space']): g['space'] for g in regs}.values():
                if g['use'] in ('bedroom', 'office', 'den', 'media'):
                    c = sum(x['cfm'] for x in regs if x['space'] is g)
                    self.fit('dt_transfer', 1, f"{g['name']}: {c:.0f} cfm needs ~{c * HP.TRANSFER_IN2_PER_CFM:.0f} sq in free area at 3 Pa - transfer grille pair or jumper duct")
        self.fit('dt_plenum', 1, 'supply + return plenums at the unit')
        dlf = sum(o.get('lf', 0) for o in self.order if o['part'].startswith(('dt_flex', 'dt_trunk', 'dt_return')))
        self.fit('dt_mastic', max(1, math.ceil(dlf / 100)), 'mastic by the gallon per 100 ft of duct')
        if ducts_out:
            self.fit('cm_duct_test', 1, 'ducts outside the thermal envelope (vented crawl): total leakage test (WSEC R403.3.5)')

    # ============================================================ ventilation + exhaust
    FAN_CFM = {'fan_bath_50': 50, 'fan_bath_110': 110, 'fan_fanlight': 50}

    def fans(self):
        """the electrical skill's bath fans (devices.json); else one per bath / powder space"""
        cand = []
        for d in self.dev:
            if d.get('kind') == 'fan' and d.get('room') in self.rooms:
                cand.append(dict(room=d['room'], pos=tuple(d['pos']), storey=d['storey'], part=d.get('part') or 'fan_bath_50',
                                 cfm=self.FAN_CFM.get(d.get('part'), 50), src='electrical devices.json'))
        if cand:
            self.notes.append(f'bath fans: {len(cand)} read from the electrical skill ({self.dev_src}) - the electrician supplies and wires them; HVAC ducts and caps each one')
            return cand
        for s in self.spaces:
            if s['use'] in ('bath', 'powder') and s['area'] >= 20:
                cand.append(dict(room=s['big'], pos=tuple(s['centroid']), storey=s['storey'], part='fan_bath_50', cfm=50, src='rule: one per bath / powder'))
        self.notes.append(f'bath fans: {len(cand)} placed by rule (no electrical devices.json beside this job)')
        return cand

    def duct_to_outside(self, pos, storey, unit=None, prefer_roof=False):
        """an exhaust / vent duct from a ceiling point to the nearest open-air exterior wall of its storey (or up through
        the roof over the top storey when that is shorter): returns (ft, cap_kind, pts, exit, elbows)"""
        ex = self.exit_point(pos, storey, unit, porch_penalty=3.0)
        z = self.zof(storey)
        top = storey == self.storeys[-1]['name']
        ceil_z = z + self.plate(storey)
        wall_ft = (manhattan(pos, ex['inside']) + 1.5) if ex else 1e9
        roof_ft = ROOF_RUN_FT if top else 1e9
        if roof_ft < wall_ft * 0.6 or (prefer_roof and top):
            pts = [(pos[0], pos[1], ceil_z), (pos[0], pos[1], ceil_z + 2.0), (pos[0] + 4.0, pos[1], ceil_z + 4.0)]
            return roof_ft, 'roof', pts, None, 2
        pts = [(pos[0], pos[1], ceil_z), (ex['inside'][0], pos[1], ceil_z), (ex['inside'][0], ex['inside'][1], ceil_z), (ex['outside'][0], ex['outside'][1], ceil_z)]
        elbows = 2 + (1 if abs(pos[0] - ex['inside'][0]) > 0.5 and abs(pos[1] - ex['inside'][1]) > 0.5 else 0)
        return wall_ft, 'wall', pts, ex, elbows

    def exhaust_run(self, f, cfm, label, whole_house=False):
        ft, cap, pts, ex, elbows = self.duct_to_outside(f['pos'], f['storey'], self.rooms[f['room']]['unit'])
        d, kind, lim = HP.bath_duct(cfm, ft, elbows)
        part = 'vx_bath_duct' if d <= 4 else 'vx_duct6'
        self.run('exhaust', d, pts, f"{label} -> {cap} cap ({cfm} cfm on {d} in {kind})", f['storey'], ft)
        self.line(part, ft, f"{label}: {cfm} cfm, {ft:.0f} ft, {elbows} elbows -> {d} in {kind} (Table M1505.4.4.2 allows {('no limit' if (lim or 0) > 1e6 else f'{lim:.0f} ft') if lim else 'n/a'})"
                  + (' - size up to 6 in smooth' if d > 4 and kind == 'smooth' else ''))
        cap_part = 'vx_cap6' if d > 4 else ('vx_cap4_roof' if cap == 'roof' else 'vx_cap4_wall')
        self.fit(cap_part, 1, f'{label}: {cap} cap with backdraft damper')
        if lim is None or d >= 7:
            self.check('code', label, f'{cfm} cfm fan over {ft:.0f} ft with {elbows} elbows is past Table M1505.4.4.2 at 6 in - move the termination or use a higher-static fan')
        return ft, cap, d

    def ventilation(self):
        V = self.H.get('ventilation') or {}
        vkind = self.L['ventilation']['kind']
        fans = self.fans()
        whf_room = (V.get('whf_room') or '').strip()
        for un in self.L['units']:
            unit = un['name']
            ufans = [f for f in fans if self.rooms[f['room']]['unit'] == unit]
            host = None
            if vkind not in ('erv', 'hrv', 'balanced'):
                # exhaust-only whole-house ventilation: one fan on continuous duty per unit
                if whf_room:
                    r = self.find_room(whf_room)
                    host = next((f for f in ufans if r and f['room'] == r['key']), None)
                    if host is None:
                        self.check('data', f'unit {unit}', f"job.json whf_room '{whf_room}' has no electrical bath fan in it - the whole-house fan went to the central top-floor bath")
                if host is None and ufans:
                    top = max(self.zof(f['storey']) for f in ufans)
                    tops = [f for f in ufans if self.zof(f['storey']) == top]
                    host = min(tops, key=lambda f: near(f['pos'], self.center(unit)))
            for f in ufans:
                label = self.rname(f['room'])
                if f is host:
                    cfm = max(f['cfm'], math.ceil(un['vent_cfm'] / 10) * 10, int(V.get('whf_cfm') or 0))
                    self.exhaust_run(f, cfm, f'{label} whole-house fan', whole_house=True)
                    self.item('fan', 'vx_whf_fan', f['pos'], self.zof(f['storey']) + self.plate(f['storey']), f['storey'], room=f['room'], note=f'whole-house fan {cfm} cfm')
                else:
                    self.exhaust_run(f, f['cfm'], label)
                    self.item('fan', f['part'], f['pos'], self.zof(f['storey']) + self.plate(f['storey']), f['storey'], room=f['room'], note='bath fan (electrical allowance)')
            if vkind in ('erv', 'hrv', 'balanced'):
                self.erv(un)
            else:
                self.fit('vx_whf_fan', 1, f"unit {unit}: whole-house fan {un['vent_cfm']:.0f} cfm continuous (Qr {un['vent_qr']:.0f} x Csystem {un['vent_csystem']:g}, one fan = unbalanced, not distributed) "
                         f"in {self.rname(host['room']) if host else '?'} - strike that bath fan from the electrical allowance")
                self.fit('vx_whf_ctrl', 1, 'labelled "WHOLE HOUSE VENTILATION - LEAVE ON" 24 h control with manual override (WA M1505.4.2); the electrician wires it')
                hab = self.habitable_spaces(unit)
                self.fit('vx_air_inlet', hab, f'unit {unit}: an outdoor-air inlet (4 sq in NFA) in each of {hab} habitable spaces (WA exhaust-only systems) - window trickle vents of the same area count instead')
                wcfm = V.get('whf_cfm')
                if wcfm and wcfm < un['vent_cfm']:
                    self.check('code', f'unit {unit}', f"the plan's whole-house fan ({wcfm} cfm) is under the required continuous rate {un['vent_cfm']:.0f} cfm "
                               f"= (0.01 x {un['cfa_sf']} + 7.5 x ({un['bedrooms']} + 1)) x {un['vent_csystem']:g} (WA Eq. 15-1 / 15-2)")
                elif wcfm:
                    self.notes.append(f"unit {unit}: the plan's {wcfm} cfm whole-house fan covers the {un['vent_cfm']:.0f} cfm WA rate (Qr {un['vent_qr']:.0f} x 1.5 for one exhaust fan)")
            self.fit('cm_vent_test', 1, f'unit {unit}: whole-house {un["vent_cfm"]:.0f} cfm + every local exhaust measured at the grille (WA M1505.4.3 / M1505.4.4)')

    def center(self, unit):
        rs = [r for r in self.L['rooms'] if r['unit'] == unit]
        return (sum(r['centroid'][0] for r in rs) / len(rs), sum(r['centroid'][1] for r in rs) / len(rs))

    def erv(self, un):
        unit = un['name']
        V = self.H.get('ventilation') or {}
        spot = self.ahu_spot(unit, self.main, V.get('erv_room') or (self.H.get('system') or {}).get('ahu_room'), elec=False)
        epos = spot['pos'] if spot else self.center(unit)
        ez = self.zof(self.main) + self.plate(self.main) - 1.0
        cfm = un['vent_cfm']
        part = 'eq_erv_s' if cfm <= 110 else 'eq_erv_m'
        self.fit(part, 1, f"unit {unit}: {V.get('model') or 'ERV / HRV'} - {cfm:.0f} cfm continuous (balanced, ducted to every habitable room: Csystem 1.0), "
                          f"SRE >= {self.L['ventilation']['sre']:g} (the credit's number) in {spot['name'] if spot else '?'}")
        self.item('erv', part, epos, ez - 1.0, self.main, room=spot['key'] if spot else None, note='ERV / HRV')
        sp = [s for s in self.spaces if s['unit'] == unit]
        sup = [s for s in sp if s['use'] in ('bedroom', 'living', 'office', 'den', 'media', 'dining') and s['habitable']]
        exh = [s for s in sp if s['use'] in ('bath', 'powder', 'laundry', 'utility') and s['area'] >= 20]
        tot = 0.0
        for kind, ss in (('erv_supply', sup), ('erv_exhaust', exh)):
            for st_ in sorted({s['storey'] for s in ss}, key=self.zof):
                grp = [s for s in ss if s['storey'] == st_]
                vaulted = any(k_ in self.lo.vaulted for s in grp for k_ in s['keys'])
                if vaulted and st_ != self.main:
                    # a vaulted storey has no attic: the trunk runs in the floor cavity below, each branch rises in the wall
                    # to a high-sidewall grille
                    zr, zg, rise = self.zof(st_) - 0.6, self.zof(st_) + 7.0, 7.6
                else:
                    zr = zg = self.zof(st_) + self.plate(st_) - 0.3
                    rise = 0.0
                a0, a1, along_x, tlen, br = self.trunk_tree(epos, [tuple(s['centroid']) for s in grp])
                riser = abs(zr - ez)
                d_tr = 6 if kind == 'erv_supply' else 5
                self.run(kind, d_tr, [(epos[0], epos[1], ez), (epos[0], epos[1], zr), (a0[0], a0[1], zr), (a1[0], a1[1], zr)], f"ERV {'supply' if kind == 'erv_supply' else 'exhaust'} trunk ({st_})", st_, tlen + riser)
                self.line('vx_erv_duct', tlen + riser, f"{'supply' if kind == 'erv_supply' else 'exhaust'} trunk, {st_}" + (' - in the floor cavity (vaulted storey)' if rise else ''))
                tot += tlen + riser
                for s, (foot, p, L0) in zip(grp, br):
                    L = L0 + 2.0 + rise
                    pts = [(foot[0], foot[1], zr), (p[0], p[1], zr)] + ([(p[0], p[1], zg)] if rise else [])
                    self.run(kind, 4, pts, f"{'supply to' if kind == 'erv_supply' else 'exhaust from'} {s['name']}" + (' (high sidewall)' if rise else ''), st_, L)
                    self.line('vx_erv_duct', L, f"{'supply' if kind == 'erv_supply' else 'exhaust'} {s['name']}")
                    self.fit('vx_erv_grille', 1, s['name'])
                    self.item('grille', 'vx_erv_grille', p, zg, st_, room=s['big'], kind2=kind)
                    tot += L
        ex = self.exit_point(epos, self.main, unit if len(self.L['units']) > 1 else None)
        if ex:
            L = near(epos, ex['inside']) + 3.0
            for i, nm in enumerate(('outdoor-air intake', 'exhaust outlet')):
                off = (-ex['n'][1] * (6 if i else -6), ex['n'][0] * (6 if i else -6))
                o = (ex['outside'][0] + off[0] - ex['n'][0] * 2.0, ex['outside'][1] + off[1] - ex['n'][1] * 2.0)
                self.run('erv_outdoor', 6, [(epos[0], epos[1], ez), (o[0], o[1], ez)], f'ERV {nm}', self.main, L + 6)
                self.line('vx_erv_insul', L + 6, f'ERV {nm} to its wall hood (insulated, vapour jacket)')
                self.fit('vx_erv_hood', 1, f'{nm} - 12 ft apart on the {ex["facing"]} wall (M1504.3: exhaust >= 10 ft from an intake)')
                self.item('hood', 'vx_erv_hood', o, ez, self.main, note=nm)
        self.notes.append(f"unit {unit}: ERV supplies {len(sup)} habitable rooms and exhausts {len(exh)} wet rooms on a trunk-and-branch layout - {tot:.0f} ft of 4-6 in duct")

    def fuel_inside(self):
        """a fuel-burning appliance inside the air barrier that is neither direct-vent nor mechanical-draft - what
        makes WA M1503.6 make-up air a requirement"""
        out = []
        fp = self.H.get('fireplace') or {}
        if fp.get('present') and (fp.get('fuel') or 'unknown') not in ('electric',) and (fp.get('vent') or '') not in ('direct', 'direct-vent'):
            out.append(f"{fp.get('fuel', 'unknown')}-fuel fireplace ({fp.get('vent') or 'vent type not stated'})")
        for k in ('range', 'dryer', 'water_heater'):
            a = self.H.get(k) or {}
            if (a.get('fuel') or 'electric') in ('gas', 'propane') and (a.get('vent') or '') not in ('direct', 'direct-vent', 'power'):
                out.append(f"{a['fuel']} {k}")
        return out

    def kitchen_and_dryer(self):
        hood = self.H.get('hood') or {}
        dry = self.H.get('dryer') or {}
        fuel = self.fuel_inside()
        for un in self.L['units']:
            unit = un['name']
            kits = [s for s in self.spaces if s['unit'] == unit and s['use'] == 'kitchen']
            rng = self.elec_find(r'^range', unit)
            if kits or rng:
                cfm = float(hood.get('cfm') or 300)
                d = HP.hood_duct(cfm)
                if rng:
                    pos, storey, src = tuple(rng[0]['pos']), rng[0]['storey'], f"the electrician's range outlet ({self.dev_src})"
                else:
                    k = kits[0]
                    walls = sorted(k['walls'], key=lambda w: -w['ft'])
                    pos = ((walls[0]['a'][0] + walls[0]['b'][0]) / 2 - walls[0]['n'][0] * 1.0, (walls[0]['a'][1] + walls[0]['b'][1]) / 2 - walls[0]['n'][1] * 1.0) if walls else tuple(k['centroid'])
                    storey, src = k['storey'], 'the kitchen\'s longest outside wall (no range outlet on the electrical job)'
                ft, cap, pts, ex, elbows = self.duct_to_outside(pos, storey, unit if len(self.L['units']) > 1 else None)
                self.run('hood', d, pts, f'range hood {cfm:.0f} cfm, {d} in', storey, ft)
                self.line('vx_hood_duct', ft, f'{d} in rigid for a {cfm:.0f} cfm hood at {src} (M1503.3); the hood itself is the appliance supplier\'s')
                self.fit('vx_hood_cap', 1, f'{d} in {cap} cap with damper')
                self.item('hood_cap', 'vx_hood_cap', ex['outside'] if ex else pos, self.zof(storey) + self.plate(storey), storey, note=f'range hood {cfm:.0f} cfm')
                if cfm > HP.HOOD_MUA_CFM:
                    if hood.get('makeup_air') or fuel:
                        why = ('the plan calls for it' if hood.get('makeup_air') else '') + ((' and ' if hood.get('makeup_air') else '') + 'WA M1503.6: ' + ', '.join(fuel) + ' inside the air barrier' if fuel else '')
                        self.fit('vx_mua', 1, f'{cfm:.0f} cfm hood > 400 cfm: motorised make-up air damper interlocked with the hood - {why}')
                        self.line('vx_hood_duct', 12.0, 'make-up air duct from its outside hood to the kitchen')
                        if fuel and not hood.get('makeup_air'):
                            self.check('code', 'kitchen', f'{cfm:.0f} cfm range hood with {", ".join(fuel)} inside and no make-up air on the plan - WA M1503.6 requires it')
                    else:
                        self.notes.append(f'{cfm:.0f} cfm range hood, but no non-direct-vent fuel appliance inside: WA M1503.6 make-up air is NOT triggered (all-electric); '
                                          'a tight house still starves a big hood - offer a passive make-up air damper or a <= 400 cfm hood')
            if dry.get('present', True):
                dd = self.elec_find(r'^dryer', unit)
                if dd:
                    pos, storey, rk = tuple(dd[0]['pos']), dd[0]['storey'], dd[0].get('room')
                    src = f"the electrician's dryer outlet in {self.rname(rk)}"
                else:
                    lau = [s for s in self.spaces if s['unit'] == unit and (s['use'] in ('laundry', 'utility') or re.search(r'LAUNDRY|LNDRY|W/D', (s['name'] or '').upper()))]
                    if not lau:
                        self.check('data', f'unit {unit}', 'no laundry traced and no dryer outlet on the electrical job - the dryer vent is not counted; name the laundry in job.json')
                        continue
                    s = lau[0]
                    walls = sorted(s['walls'], key=lambda w: -w['ft'])
                    pos = ((walls[0]['a'][0] + walls[0]['b'][0]) / 2 - walls[0]['n'][0] * 1.5, (walls[0]['a'][1] + walls[0]['b'][1]) / 2 - walls[0]['n'][1] * 1.5) if walls else tuple(s['centroid'])
                    storey, rk, src = s['storey'], s['big'], f"the {s['name']} wall"
                ex = self.exit_point(pos, storey, unit if len(self.L['units']) > 1 else None, porch_penalty=3.0)
                z = self.zof(storey) + 1.0
                straight = (manhattan(pos, ex['inside']) + 2.0) if ex else 10.0
                elbows = 2 + (1 if ex and abs(pos[0] - ex['inside'][0]) > 0.5 and abs(pos[1] - ex['inside'][1]) > 0.5 else 0)
                eq = straight + elbows * HP.DRYER_90_FT
                pts = [(pos[0], pos[1], z), (ex['inside'][0], pos[1], z), (ex['inside'][0], ex['inside'][1], z), (ex['outside'][0], ex['outside'][1], z)] if ex else [(pos[0], pos[1], z), (pos[0] + 2, pos[1], z)]
                self.run('dryer', 4, pts, f'dryer vent {straight:.0f} ft + {elbows} elbows = {eq:.0f} ft equivalent (M1502.4.6.1)', storey, straight)
                self.line('vx_dryer_pipe', straight, f"from {src}: {straight:.0f} ft")
                self.fit('vx_dryer_ell', elbows, ''); self.fit('vx_dryer_box', 1, ''); self.fit('vx_dryer_cap', 1, '')
                self.item('dryer_cap', 'vx_dryer_cap', ex['outside'] if ex else pos, z, storey, note='dryer cap')
                if eq > HP.DRYER_MAX_EQ_FT:
                    self.check('code', self.rname(rk), f'dryer vent {eq:.0f} ft equivalent > 35 ft (M1502.4.6.1) - the dryer maker\'s longer table or a UL 705 duct power ventilator (booster fans are prohibited)')
                    self.fit('vx_dryer_depv', 1, 'run over 35 ft equivalent')

    # ============================================================ the checker (the rest) and the other trades
    def checker(self):
        H = self.H
        S = self.S
        sysd = H.get('system') or {}
        for c in S.get('conflicts', []):
            self.check('data', 'plan set', f"{c['what']} -> {c['use']} ({c['why']})")
        if self.kind == 'ductless' and any(c.get('system') == 'ducted' for c in S.get('credits', [])):
            self.check('code', 'WSEC', 'job.json says ductless but the energy sheet selects a centrally ducted credit - the permit was issued on the credit')
        if self.kind in ('ducted', 'ducted_multizone') and any(c.get('system') == 'ductless' for c in S.get('credits', [])):
            self.check('code', 'WSEC', 'job.json says ducted but the energy sheet selects the ductless credit (3.7)')
        hspf = sysd.get('hspf2_min')
        if hspf:
            self.notes.append(f'equipment must meet HSPF2 >= {hspf:g} (the WSEC credit); design temperature {self.T:g} F '
                              + ('<= 23 F: a NEEP-listed cold-climate variable-capacity unit (the 3.6 note)' if self.T <= 23 else '> 23 F'))
        wsu_max = self.L['totals'].get('wsu_max_hp_btuh')
        for s in self.systems:
            for o in s['outdoor']:
                ratio = o['cap_at_design'] / max(1, s['total_heat'])
                if ratio > 1.6:
                    self.check('practice', f"unit {s['unit']}", f"the {o['kbtuh']}k outdoor unit carries {o['cap_at_design']:,} Btuh at {self.T:g} F against a {s['total_heat']:,} Btuh load - {ratio:.1f}x"
                               + (' AS SPECIFIED on the plan: ask how it was sized (Manual S 2023 wants >= 1.00 x at design and the minimum output <= 0.80 x; WA M1401.3 lets variable-capacity equipment run over, but not forever)' if o.get('forced') else ''))
                if wsu_max and len(self.L['units']) == 1 and o['kbtuh'] * 1000 > wsu_max and o.get('kind') != 'single':
                    self.notes.append(f"the {o['kbtuh']}k nominal is over the WSU sizing sheet's heat-pump maximum ({wsu_max:,} Btuh = 1.25 x its {self.L['totals']['wsu_btuh']:,}) - if the permit used the WSU sheet, the reviewer can ask")
                fam = 'ducted' if o.get('kind') == 'central' else 'ductless'
                mn = HP.min_output_at(o['kbtuh'] * 1000, self.T, fam)
                if mn > HP.MIN_COMP_MAX * s['total_heat']:
                    self.check('practice', f"unit {s['unit']}", f"the {o['kbtuh']}k unit's minimum output (~{mn:,.0f} Btuh at {self.T:g} F) is over 0.80 x the {s['total_heat']:,} Btuh load (Manual S) - it will cycle at design")
        if self.found == 'crawl' and self.kind in ('ducted', 'ducted_multizone') and (H.get('ducts') or 'inside') == 'crawl_vented':
            self.notes.append('ducts in the vented crawl are outside the thermal envelope: R-8 on every duct, mastic-sealed, and the total duct leakage test before final')
        if self.L['ventilation']['kind'] == 'exhaust' and any(c.get('vent') == 'hrv' for c in S.get('credits', [])):
            self.check('code', 'WSEC', 'the credit needs heat-recovery ventilation but job.json ventilation is exhaust-only')
        self.notes.append('refrigerant: a split system installed from 1/1/2026 is an A2L (R-454B / R-32) unit under the EPA Technology Transitions rule; '
                          'R-410A equipment is out. A2L units carry leak detection / mitigation per their listing - it rides with the equipment line')
        fp = H.get('fireplace') or {}
        if fp.get('present'):
            self.notes.append(f"a {fp.get('fuel', 'unknown')}-fuel fireplace is on the set - not in this bid (the fireplace installer's); a sealed direct-vent unit needs no combustion air from the house")
        if self.kind == 'ductless':
            self.notes.append('ductless: each head\'s programmable wireless controller meets WSEC R403.1.1; a wired wall controller per zone is an option line')
            self.fit('eq_zone_ctrl', sum(len(s.get('heads', [])) for s in self.systems), 'wired wall controller per head (option)')
        if self.D.get('stand_in'):
            self.check('data', 'design temperature', f"{self.D['heat']} F is a stand-in ({self.D['src']}) - pull WSEC Table RC-1 for {self.D.get('town')} before this goes out")

    def cross_trade(self):
        """what the electrical job has to carry for this HVAC design - the breaker most estimators still miss"""
        if not self.dev:
            self.notes.append('no electrical devices.json beside this job - the equipment circuits are not cross-checked')
            return
        e_out = self.elec_find(r'mini-split outdoor|heat pump condenser|condenser|outdoor unit')
        e_ahu = self.elec_find(r'air handler|furnace')
        e_heads = self.elec_find(r'indoor head')
        mine = [o for s in self.systems for o in s['outdoor']]
        if len(e_out) != len(mine):
            self.check('practice', 'electrical', f"the electrical job carries {len(e_out)} outdoor-unit circuit(s); this design has {len(mine)} outdoor unit(s) - "
                       'tell the electrician (one 240 V circuit + disconnect within sight per outdoor unit, NEC 440.14)')
        e_amps = sorted((d.get('amps') or 0) for d in e_out)
        for o in sorted(mine, key=lambda o: -o['kbtuh']):
            need = HP.BREAKER_A.get((o['kind'] if o['kind'] != 'central' else 'central', o['kbtuh']))
            have = e_amps.pop() if e_amps else None
            if need and have and have < need:
                self.check('practice', 'electrical', f"the {o['kbtuh']}k {o['kind']} outdoor unit typically needs a {need} A circuit [U: the nameplate MOCP governs]; the electrical job carries {have} A")
        for s in self.systems:
            if s.get('backup_kw'):
                need = HP.STRIP_BREAKER_A.get(s['backup_kw'])
                have = max([d.get('amps') or 0 for d in e_ahu] or [0])
                if not e_ahu:
                    self.check('practice', 'electrical', f"no air-handler circuit on the electrical job - the air handler with its {s['backup_kw']} kW strip needs ~{need} A")
                elif need and have < need:
                    self.check('practice', 'electrical', f"the air handler with a {s['backup_kw']} kW strip needs ~{need} A [U]; the electrical job carries {have} A")
        if e_heads and self.kind == 'ductless':
            self.notes.append(f"the electrical job carries a separate circuit for the indoor heads ({e_heads[0].get('amps')} A): on Mitsubishi / Fujitsu / Daikin splits the heads are powered "
                              'from the outdoor unit through the 14/4 - that circuit comes off unless the chosen model needs it')
        if self.kind in ('ducted', 'ducted_multizone') and not e_ahu:
            self.check('practice', 'electrical', 'the electrical job has no air-handler / indoor-unit circuit')
        flip = [d for d in self.dev if d.get('unit') and len(self.L['units']) > 1 and d['unit'] != d['unit_here']]
        if flip:
            ex = flip[0]
            self.check('data', 'electrical', f"the electrical job labels {len(flip)} device(s) with the other unit's name - e.g. its '{ex.get('appliance') or ex.get('part')}' "
                       f"marked unit {ex['unit']} sits in unit {ex['unit_here']}'s footprint ({self.rname(ex.get('room'))}); this takeoff follows the plan (job.json units) - "
                       'tell the electrician before the panel schedule goes out')
        n_fans = sum(1 for d in self.dev if d.get('kind') == 'fan')
        if self.L['ventilation']['kind'] == 'exhaust' and n_fans:
            self.notes.append('electrical: one of its bath-fan allowances becomes the HVAC whole-house fan (supplied here) - strike it from the electrical allowance, keep the wiring and add the 24 h control')

    # ============================================================ tally, labour, inspections
    def tally(self):
        agg = {}
        for o in self.order:
            p = HP.byId[o['part']]
            a = agg.setdefault(o['part'], dict(part=o['part'], cat=p['cat'], label=p['label'], group=p['group'], phase=p.get('phase', 'rough'),
                                              unit='LF' if p['kind'] == 'line' else p.get('unit', 'EA'), qty=0.0, notes=[], option=bool(p.get('option'))))
            a['qty'] += o.get('lf', o.get('qty', 0))
            if o.get('note') and len(a['notes']) < 6 and o['note'] not in a['notes']:
                a['notes'].append(o['note'])
        lines = []
        for a in agg.values():
            p = HP.byId[a['part']]
            if a['unit'] == 'LF':
                w = p.get('waste', 0.1)
                a['order_qty'] = math.ceil(a['qty'] * (1 + w)); a['waste'] = w
                for key in ('coil', 'bag', 'stick'):
                    if p.get(key):
                        a['packs'] = math.ceil(a['order_qty'] / p[key]); a['pack_ft'] = p[key]; a['pack'] = key
            else:
                a['order_qty'] = math.ceil(a['qty'] * 10) / 10 if a['unit'] == 'lb' else int(math.ceil(a['qty']))
            a['qty'] = round(a['qty'], 1)
            a['note'] = ' · '.join(a['notes'])[:240]
            del a['notes']
            lines.append(a)
        PH = ['equip', 'rough', 'vent', 'trim', 'test']
        lines.sort(key=lambda a: (PH.index(a['phase']) if a['phase'] in PH else 9, a['group'], a['label']))
        mins = defaultdict(float)
        for a in lines:
            p = HP.byId[a['part']]
            if a.get('option') or a['qty'] <= 0:
                continue
            ph = {'equip': 'set', 'rough': 'rough', 'vent': 'rough', 'trim': 'trim', 'test': 'startup'}.get(a['phase'], 'rough')
            mins[ph] += (p.get('site') or 0) * a['qty']
        lab = self.H.get('labour') or {}
        crew = int(lab.get('crew', 2)); cap = float(lab.get('capacity_hr', 6.25))
        hours = {k: round(v / 60, 1) for k, v in mins.items()}
        days = {k: max(1, math.ceil(v / cap - 0.2)) if v > 0 else 0 for k, v in hours.items()}
        return lines, dict(crew_hours=hours, days=days, total_hours=round(sum(hours.values()), 1), total_days=sum(days.values()), crew=crew, capacity_hr=cap,
                           note='crew minutes are PLACEHOLDERS (no task-level install hours were found: references/research-hvac-market.md 3.3) - set them from a sub or the crew')

    def inspections(self):
        j = (self.H.get('jurisdiction') or 'whatcom').lower()
        who = {'whatcom': 'Whatcom County PDS', 'bellingham': 'City of Bellingham Permit Center', 'blaine': 'City of Blaine',
               'skagit': 'Skagit County', 'sanjuan': 'San Juan County CD&P'}.get(j, j)
        n_app = sum(int(a['order_qty']) for a in self.lines if a['part'].startswith(('eq_ds', 'eq_mz', 'eq_head', 'eq_duin', 'eq_hp', 'eq_ahu', 'eq_erv')))
        n_fan = sum(int(a['order_qty']) for a in self.lines if a['part'] in ('vx_cap4_wall', 'vx_cap4_roof', 'vx_whf_fan', 'vx_hood_cap', 'vx_dryer_cap'))
        seq = [dict(name='Mechanical rough-in (cover)', when='after framing, before insulation', test='line sets pressure-tested and in place; ducts, boots, exhaust ducts and caps; firestops at the garage separation'),
               dict(name='Duct leakage test', when='rough-in or final', test='total leakage at 25 Pa per WSEC R403.3.5 - waived only when every duct and the air handler are inside the envelope') if any(s['kind'].startswith('ducted') for s in self.systems) else None,
               dict(name='Ventilation flow test', when='before final', test='whole-house rate and every local exhaust measured (WA M1505.4)'),
               dict(name='Final mechanical', when='equipment set, started, labelled', test='equipment listing / HSPF2 on the certificate, controls, condensate, clearances')]
        return dict(jurisdiction=j, authority=who, appliances=n_app, fans_and_vents=n_fan, permit_fee=None,
                    fee_source=f'{who} residential mechanical fee schedule - NOT FOUND in the 9/25 research (references/research-hvac-code.md 8): price it from the county sheet',
                    sequence=[s for s in seq if s])

    # ============================================================ run
    def run_all(self):
        units = self.L['units']
        for un in units:
            if self.kind in ('ductless',):
                self.design_ductless(un)
            elif self.kind == 'ducted':
                self.design_ducted(un)
            elif self.kind == 'ducted_multizone':
                self.design_ducted(un, multizone=True)
            else:
                self.check('data', f"unit {un['name']}", f"system kind '{self.kind}' - hvacscan could not name it and job.json does not: set hvac.system.kind (ductless / ducted / ducted_multizone) after LOOKING at the energy sheet")
        self.ventilation()
        self.kitchen_and_dryer()
        self.fit('cm_design', 1, 'room-by-room loads for the permit (this takeoff is the draft)')
        self.fit('cm_labels', len(units), 'per dwelling unit')
        self.fit('sp_caulk', max(1, math.ceil(sum(o.get('qty', 0) for o in self.order if o['part'] in ('sp_bore', 'rp_sleeve')) / 12)), 'fire caulk / sealant at the penetrations')
        self.checker()
        self.cross_trade()
        self.lines, self.labour = self.tally()
        ins = self.inspections()
        runs_by = defaultdict(float)
        for r in self.runs:
            runs_by[f"{r['system']} {r['size']}"] += r['ft']
        T = self.L['totals']
        out = dict(address=self.job.get('address'), slug=self.job.get('slug'), permit=self.job.get('permit'), generated='hvackit.py',
                   spec=dict(kind=self.kind, foundation=self.found, lineset_route=self.route_mode, ducts=self.H.get('ducts') or 'inside',
                             ventilation=self.L['ventilation']['kind'], jurisdiction=self.H.get('jurisdiction'),
                             system=self.H.get('system'), sources={k: v for k, v in self.H.items() if k.startswith('_')} | {k: v for k, v in self.job.items() if k.startswith('_')}),
                   design=self.L['design'], loads=dict(totals=T, units=self.L['units'], u_src=self.L['u_src'], glazing=self.L['glazing'], alt=self.L.get('alt'),
                                                        infiltration=self.L['infiltration'], ventilation=self.L['ventilation'], area=self.L['area'],
                                                        duct=self.L['duct'], notes=self.L['notes'], warnings=self.L['warnings']),
                   rooms=[{k: r[k] for k in ('key', 'name', 'use', 'unit', 'storey', 'area_sf', 'heat_btuh', 'cool_btuh', 'win_sf', 'ext_wall_ft', 'ceil_sf', 'floor_sf', 'centroid', 'poly', 'z')} for r in self.L['rooms']],
                   systems=self.systems, items=self.items, runs=self.runs, run_ft={k: round(v, 1) for k, v in sorted(runs_by.items())},
                   order=self.lines, labour=self.labour, inspections=ins, checks=self.checks, notes=self.notes,
                   routing=dict(mode=self.route_mode,
                                source=('line sets drop in the stud bay under each indoor unit (or the nearest stacked wall) and cross the crawl on an L along the joists to the rim beside the outdoor unit'
                                        if self.route_mode == 'concealed' and self.found == 'crawl' else 'line sets leave through the wall behind each head and run down a painted line-hide to the unit')
                                + '; ducts run a trunk per storey with square branches in the joist bays'),
                   electrical=dict(source=self.dev_src, devices_read=len(self.dev)),
                   spaces=[{k: s[k] for k in ('id', 'name', 'use', 'storey', 'unit', 'area', 'keys', 'habitable', 'fragment')} for s in self.spaces],
                   totals=dict(heat_btuh=T['heat_btuh'], cool_tons=T['cool_tons'], outdoor_units=sum(len(s['outdoor']) for s in self.systems),
                               heads=sum(len(s.get('heads', [])) for s in self.systems), indoor_ducted=sum(len(s.get('indoor', [])) for s in self.systems),
                               registers=sum(len(s.get('registers', [])) for s in self.systems),
                               lineset_ft=round(sum(r['ft'] for r in self.runs if r['system'] == 'refrigerant')),
                               duct_ft=round(sum(r['ft'] for r in self.runs if r['system'] in ('supply', 'trunk', 'return'))),
                               vent_ft=round(sum(r['ft'] for r in self.runs if r['system'] in ('exhaust', 'erv_supply', 'erv_exhaust', 'erv_outdoor', 'hood', 'dryer'))),
                               codes=sum(1 for c in self.checks if c['level'] == 'code'), practice=sum(1 for c in self.checks if c['level'] == 'practice'),
                               data=sum(1 for c in self.checks if c['level'] == 'data')))
        return out


# ================================================================== report
def report(o):
    T = o['totals']; L = o['loads']; D = o['design']; sp = o['spec']
    R = [f"# HVAC takeoff - {o['address']}\n", f"`{o['slug']}` · permit {o.get('permit') or '-'} · generated by `hvackit.py`\n"]
    R.append(f"**System** {sp['kind']} · **foundation** {sp['foundation']} · **line sets** {sp['lineset_route']} · **ducts** {sp['ducts']} · **ventilation** {sp['ventilation']} · "
             f"**design** {D['heat']} F / {D['cool']} F ({D['town']})\n")
    R.append(f"**Heating {L['totals']['heat_btuh']:,} Btuh** ({L['totals']['heat_per_sf']} Btuh/sf) · cooling {L['totals']['cool_sens_btuh']:,} + {L['totals']['cool_lat_btuh']:,} latent = {L['totals']['cool_tons']} tons · "
             f"WSU worksheet {L['totals']['wsu_btuh']:,} Btuh · {T['outdoor_units']} outdoor unit(s), {T['heads']} head(s), {T['indoor_ducted']} ducted indoor unit(s), {T['registers']} register(s) · "
             f"line sets {T['lineset_ft']:,} ft · duct {T['duct_ft']:,} ft · vent / exhaust duct {T['vent_ft']:,} ft\n")
    R.append('## The system\n')
    for s in o['systems']:
        R.append(f"### unit {s['unit']} - {s['kind']}: heat {s['total_heat']:,} Btuh, cool {s['total_cool']:,} Btuh sensible, capacity at design {s.get('cap_at_design', 0):,} Btuh\n")
        for x in s['outdoor']:
            R.append(f"- outdoor **{x['part']}** {x['kbtuh']}k ({x['kind']}) on the {x['facing']} wall, {x.get('where', '')} - {x['cap_at_design']:,} Btuh at design, {x.get('lineset_ft', 0)} ft of line set" + (' - as specified on the plan' if x.get('forced') else ''))
        if s.get('zones'):
            R.append('\n| zone (head in) | rooms in the zone | carried rooms | heat Btuh | cool Btuh |'); R.append('|---|---|---|---|---|')
            for z in s['zones']:
                R.append(f"| {z['host']} ({z['storey']}) | {', '.join(z['names'])[:70]} | {', '.join(z['carries'])[:60]} | {z['heat']:,} | {z['cool']:,} |")
        if s.get('heads'):
            R.append('\n| head | room | storey | heat | cool | wall |'); R.append('|---|---|---|---|---|---|')
            for h in s['heads']:
                R.append(f"| {h['kbtuh']}k | {h['room']} | {h['storey']} | {h['heat']:,} | {h['cool']:,} | {'exterior' if h['exterior_wall'] else 'interior'} |")
        for x in s.get('indoor', []):
            R.append(f"- indoor **{x['part']}** {x['kbtuh']}k in {x['room']} ({x['storey']}; {x.get('src')}), {x['cfm']} cfm")
        if s.get('registers'):
            R.append(f"- {len(s['registers'])} supply registers: " + ', '.join(f"{g['room']} {g['cfm']} cfm/{g['duct_in']} in" for g in s['registers'][:30]))
            R.append("- returns: " + ', '.join(f"{g['room']} ({g['storey']}) {g['cfm']} cfm / {g['duct_in']} in, {g.get('grille')} grille" for g in s['returns']))
        if s.get('backup_kw'):
            R.append(f"- backup strip {s['backup_kw']} kW (locked out above the balance point)")
    R.append('\n## Loads\n')
    t = L['totals']
    R.append('| component | Btuh |'); R.append('|---|---|')
    for k, v in t['by_component'].items():
        R.append(f'| {k} | {v:,} |')
    R.append("\nU-factors: " + '; '.join(f'{k} {v}' for k, v in L['u_src'].items()))
    V = L['ventilation']; inf = L['infiltration']
    R.append(f"\nglazing {L['glazing']['used_sf']:,} sf ({L['glazing']['why']}); infiltration {inf['ach50']:g} ACH50 -> {inf['ach_nat']} ACH at design (MJ8 blower-door, ACH50 / {inf.get('n_equiv')}); "
             f"ventilation {V['cfm']} cfm = Qr {V.get('qr')} x Csystem {V.get('csystem')} ({V['kind']}, SRE {V['sre']:g}; {V.get('how', '')}); area traced {L['area']['traced_sf']:,} sf vs plan {L['area']['plan_sf'] or '-'} sf\n")
    if L.get('alt'):
        R.append(f"- {L['alt']['note']}\n")
    R.append('| room | unit | storey | sf | heat Btuh | cool Btuh | glass sf | ext wall ft |'); R.append('|---|---|---|---|---|---|---|---|')
    for r in sorted(o['rooms'], key=lambda r: -r['heat_btuh']):
        R.append(f"| {r['name'] or r['key']} | {r['unit']} | {r['storey']} | {r['area_sf']:.0f} | {r['heat_btuh']:,} | {r['cool_btuh']:,} | {r['win_sf']:.0f} | {r['ext_wall_ft']:.0f} |")
    for w in L['warnings']:
        R.append(f'- **load warning**: {w}')
    for n in L['notes']:
        R.append(f'- load note: {n}')
    R.append('\n## Runs (measured, before waste)\n')
    R.append('| system / size | ft |'); R.append('|---|---|')
    for k, v in o['run_ft'].items():
        R.append(f'| {k} | {v:,.0f} |')
    rt = o['routing']
    R.append(f"\n**Routing.** {rt['source']}. Electrical layout read: {o['electrical']['source'] or 'none'} ({o['electrical']['devices_read']} devices).\n")
    R.append('## The checker\n')
    if not o['checks']:
        R.append('- clean')
    for c in o['checks']:
        R.append(f"- **{c['level'].upper()}** {c['where']}: {c['what']}")
    for n in o['notes']:
        R.append(f'- note: {n}')
    R.append('\n## The order (quantities only - no prices here)\n')
    R.append('| phase | group | item | measured | order | unit | note |'); R.append('|---|---|---|---|---|---|---|')
    for a in o['order']:
        R.append(f"| {a['phase']} | {a['group']} | {a['label'][:70]}{' (option)' if a.get('option') else ''} | {a['qty']:g} | {a['order_qty']}{(' = ' + str(a['packs']) + ' x ' + str(a['pack_ft']) + ' ft') if a.get('packs') else ''} | {a['unit']} | {a['note'][:120]} |")
    lb = o['labour']
    R.append(f"\n## Labour\n\ncrew of {lb['crew']}: {lb['crew_hours']} crew-hours -> {lb['days']} days ({lb['total_days']} total at {lb['capacity_hr']} h/day). {lb['note']}\n")
    ins = o['inspections']
    R.append(f"## Inspections - {ins['authority']}\n")
    for s in ins['sequence']:
        R.append(f"- **{s['name']}** - {s['when']}; {s['test']}")
    R.append(f"\npermit: {ins['appliances']} appliances, {ins['fans_and_vents']} fans / vents; fee: {ins['fee_source']}\n")
    if sp.get('sources'):
        R.append("## What job.json said, and where it came from\n")
        for k, v in sp['sources'].items():
            R.append(f"- **{k.lstrip('_')}** - {v}")
    return '\n'.join(R)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('job'); ap.add_argument('--interior', default=None); ap.add_argument('--scan', default=None); ap.add_argument('--out', default=None)
    a = ap.parse_args()
    job = C.load(a.job); d = os.path.dirname(os.path.abspath(a.job))
    I = C.load(a.interior or C.resolve(job.get('interior', 'interior.json'), d))
    sp = a.scan or os.path.join(d, 'hvac_scan.json')
    S = C.load(sp) if os.path.exists(sp) else {}
    o = Kit(job, I, S, d).run_all()
    out = a.out or os.path.join(d, 'hvac_takeoff.json')
    json.dump(o, open(out, 'w', encoding='utf-8'), indent=1)
    open(os.path.join(os.path.dirname(out), 'hvac_report.md'), 'w', encoding='utf-8').write(report(o))
    T = o['totals']
    print(f"{o['slug']}: {o['spec']['kind']} · heat {T['heat_btuh']:,} Btuh · {T['outdoor_units']} outdoor / {T['heads']} heads / {T['indoor_ducted']} ducted units / {T['registers']} registers · "
          f"line sets {T['lineset_ft']} ft · duct {T['duct_ft']} ft · vent {T['vent_ft']} ft · {len(o['order'])} order lines · {o['labour']['total_days']} days · "
          f"{T['codes']} code / {T['practice']} practice / {T['data']} data findings")


if __name__ == '__main__':
    main()
