#!/usr/bin/env python3
r"""receipts.py - the receipts table, built from what is actually on disk.

    python receipts.py jobs/<house>            # one house  -> jobs/<house>/receipts.md
    python receipts.py jobs --all              # every house -> jobs/RECEIPTS.md (the comparison)

A receipts table nobody can regenerate is a claim. This reads hvac_scan.json, hvac_takeoff.json, the renders,
the viewer payload, the bid and the PDF, and reports what ran, what was read off the plan text, what the
electrical job supplied, and what is an assumption. Every row is derived; nothing is typed in.
"""
import argparse, json, os, sys, glob
from collections import Counter
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
YN = lambda b: 'y' if b else '**n**'


def load(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return None


def house(d):
    job = load(os.path.join(d, 'job.json'))
    if not job:
        return None
    S = load(os.path.join(d, 'hvac_scan.json')); T = load(os.path.join(d, 'hvac_takeoff.json')); B = load(os.path.join(d, 'hvac_bid.json'))
    shots = sorted(glob.glob(os.path.join(d, 'shot_*.png')))
    payload = glob.glob(os.path.join(d, '*_app.json')); pdf = glob.glob(os.path.join(d, '*.pdf'))
    r = dict(dir=d, slug=job.get('slug'), address=job.get('address'), permit=job.get('permit'), job=job, S=S, T=T, B=B, shots=shots,
             payload=payload[0] if payload else None, pdf=pdf[0] if pdf else None)
    P = load(payload[0]) if payload else None
    if P:
        r['groups'] = Counter(o['g'] for o in P.get('objects', []))
        r['walls'] = (P.get('framing') or {}).get('walls')
    return r


def one(r):
    L = [f"# Receipts - {r['address']}", f"\n`{r['slug']}` · permit {r.get('permit') or '-'} · generated {datetime.now():%Y-%m-%d %H:%M} by `receipts.py` from the files in this folder.\n",
         '| Step | Ran | Receipt |', '|---|---|---|']
    job = r['job']; H = job.get('hvac', {})
    L.append(f"| sheets | {YN(bool(job.get('storeys')))} | " + '; '.join(f"p{s['page']} = {s['name']} (plate {s.get('plate')} ft)" for s in job.get('storeys', [])) + " · the finish skill's interior.json is the room source |")
    S = r.get('S')
    if S:
        sysd = S.get('system') or {}
        cr = ', '.join(f"{c['option']} ({c.get('meaning', '')[:40]})" for c in S.get('credits', []))
        L.append(f"| plan text read (hvacscan) | y | {S.get('text_chars', 0):,} characters, WSEC {S['code'].get('wsec')}, {S['code'].get('credits_required') or '-'} credits required · "
                 f"credits read: {cr or 'none'} · system named: **{sysd.get('kind') or 'unknown'}** · {len((S.get('openings') or {}).get('rows', []))} schedule openings · "
                 f"{len(S.get('conflicts', []))} conflict(s) |")
    else:
        L.append('| plan text read (hvacscan) | **n** | no hvac_scan.json - the set has no text layer here (scanned) or was not read; job.json carries the system |')
    T = r.get('T')
    if T:
        LT = T['loads']['totals']; D = T['design']; t = T['totals']; sp = T['spec']
        L.append(f"| loads (hvac_load) | y | heating **{LT['heat_btuh']:,} Btuh** ({LT['heat_per_sf']} Btuh/sf) at {D['heat']} F ({D.get('station', D.get('town'))}{', STAND-IN' if D.get('stand_in') else ''}) · "
                 f"cooling {LT['cool_sens_btuh']:,} + {LT['cool_lat_btuh']:,} latent ({LT.get('cool_per_sf')} Btuh/sf) · WSU sheet {LT['wsu_btuh']:,} · glazing {T['loads']['glazing']['used_sf']:,} sf ({T['loads']['glazing']['why'][:60]}) · "
                 f"{len(T['rooms'])} rooms · {len(T['loads']['warnings'])} load warning(s) |")
        V = T['loads']['ventilation']
        L.append(f"| ventilation | y | {V['kind']} {V['cfm']} cfm = Qr {V.get('qr')} x Csystem {V.get('csystem')} (WA M1505.4.3) · load {V['heat_btuh']:,} Btuh |")
        for s in T['systems']:
            outs = ', '.join(f"{o['kbtuh']}k {o['kind']} ({o.get('where', '')[:50]})" for o in s['outdoor'])
            extra = (f"{len(s.get('heads', []))} heads " + ', '.join(f"{h['kbtuh']}k {h['room']}" for h in s.get('heads', []))) if s.get('heads') else \
                    (', '.join(f"{x['kbtuh']}k in {x['room']}" for x in s.get('indoor', [])) + f" · {len(s.get('registers', []))} registers, {len(s.get('returns', []))} returns")
            L.append(f"| system, unit {s['unit']} | y | {s['kind']}: {outs}; {extra} · capacity at design {s.get('cap_at_design', 0):,} vs load {s['total_heat']:,} Btuh |")
        L.append(f"| runs | y | line sets {t['lineset_ft']:,} ft ({sp['lineset_route']}) · duct {t['duct_ft']:,} ft · vent / exhaust {t['vent_ft']:,} ft |")
        el = T.get('electrical') or {}
        L.append(f"| electrical layout read | {YN(el.get('devices_read'))} | {el.get('source') or 'none'} ({el.get('devices_read', 0)} devices): bath fans, the dryer and range outlets, the outdoor-unit disconnect and air-handler junction positions |")
        c = Counter(x['level'] for x in T['checks'])
        L.append(f"| the checker | y | **{c.get('code', 0)} code**, {c.get('practice', 0)} practice, {c.get('data', 0)} data: " + ' / '.join(f"{x['where']}: {x['what'][:70]}" for x in T['checks'][:4]) + ' |')
        lb = T['labour']
        L.append(f"| labour | y | {lb['total_hours']} crew-hours -> **{lb['total_days']} days** ({', '.join(f'{k} {v}' for k, v in lb['days'].items())}). PLACEHOLDER minutes. |")
    else:
        L.append('| hvackit | **n** | no hvac_takeoff.json |')
    g = r.get('groups') or {}
    w = r.get('walls') or {}
    L.append(f"| model + renders | {YN(r['payload'] and r['shots'])} | {os.path.basename(r['payload']) if r['payload'] else '-'} · groups {dict(g)} · walls {w.get('segments', '-')} generated centrelines · {len(r['shots'])} render(s) |")
    if r.get('B'):
        BT = r['B']['totals']
        L.append(f"| draft bid | y | equipment {BT['equipment']['lines']} / rough-in {BT['rough']['lines']} / trim {BT['trim']['lines']} lines, {len(r['B']['options'])} option(s) · **{BT['priced_lines']} priced**, "
                 f"{len(r['B']['unpriced'])} labels need a price · fee {BT.get('fee_rate', 0):.0%} · prices: {r['B']['price_source']} |")
    else:
        L.append('| draft bid | **n** | no hvac_bid.json |')
    L.append(f"| PDF parts list | {YN(r['pdf'])} | {os.path.basename(r['pdf']) if r['pdf'] else '-'} |")
    L.append('\n## What is measured, what the plan text said, and what is an assumption\n')
    L.append('**Measured off the traced interior:** every room area, exterior wall length and facing, ceiling and floor exposure, the head and register positions, every run length (L-paths in the crawl and joist bays).\n')
    if S:
        L.append('**Read off the plan text:** ' + '; '.join(f"{c['option']} = {c.get('meaning', '')}" for c in S.get('credits', []))[:500] + '\n')
    L.append('**From the electrical job:** the bath fans (the electrician supplies them; HVAC ducts them), the dryer and range outlet positions, the outdoor-unit disconnect and air-handler junction.\n')
    L.append('**Assumed, or answered by job.json rather than the plan:**')
    for k, v in H.items():
        if k.startswith('_'):
            L.append(f"- **{k[1:]}** - {v}")
    L.append('- install minutes, the day rate and the crew rates are PLACEHOLDERS; every price is blank until Genaro sets it')
    return '\n'.join(L)


def compare(rs):
    L = ['# HVAC - receipts, five houses', f'\nGenerated {datetime.now():%Y-%m-%d %H:%M} by `scripts/receipts.py` from each house\'s files. {len(rs)} houses.\n',
         '## What ran, per house\n', '| house | scan | takeoff | report | model | renders | bid | PDF |', '|---|---|---|---|---|---|---|---|']
    for r in rs:
        L.append(f"| **{r['address'][:44]}** | {'✅' if r.get('S') else '— (no text layer)'} | {'✅' if r.get('T') else '❌'} | {'✅' if os.path.exists(os.path.join(r['dir'], 'hvac_report.md')) else '❌'} | "
                 f"{'✅' if r['payload'] else '❌'} | {len(r['shots'])} | {'✅' if r.get('B') else '❌'} | {'✅' if r['pdf'] else '❌'} |")
    L += ['\n## Loads\n', '| house | design | heating Btuh | Btuh/sf | WSU sheet | cooling tons | cool Btuh/sf | glazing sf | ACH50 | ventilation |', '|---|---|---|---|---|---|---|---|---|---|']
    for r in rs:
        T = r.get('T')
        if not T:
            continue
        LT = T['loads']['totals']; D = T['design']; V = T['loads']['ventilation']
        L.append(f"| {r['address'][:30]} | {D['heat']} F{' (stand-in)' if D.get('stand_in') else ''} | {LT['heat_btuh']:,} | {LT['heat_per_sf']} | {LT['wsu_btuh']:,} | {LT['cool_tons']} | {LT.get('cool_per_sf')} | "
                 f"{T['loads']['glazing']['used_sf']:,.0f} | {T['loads']['infiltration']['ach50']:g} | {V['kind']} {V['cfm']:.0f} cfm |")
    L += ['\n## Systems\n', '| house | kind | outdoor | indoor | line sets ft | duct ft | vent ft | days | code / practice / data |', '|---|---|---|---|---|---|---|---|---|']
    for r in rs:
        T = r.get('T')
        if not T:
            continue
        t = T['totals']
        outs = ' + '.join(f"{o['kbtuh']}k {o['kind']}" for s in T['systems'] for o in s['outdoor'])
        ind = f"{t['heads']} heads" if t['heads'] else f"{t['indoor_ducted']} ducted unit(s), {t['registers']} registers"
        L.append(f"| {r['address'][:30]} | {T['spec']['kind']} | {outs} | {ind} | {t['lineset_ft']:,} | {t['duct_ft']:,} | {t['vent_ft']:,} | {T['labour']['total_days']} | {t['codes']} / {t['practice']} / {t['data']} |")
    L += ['\n## What the checker found\n']
    for r in rs:
        T = r.get('T')
        if not T:
            continue
        L.append(f"**{r['address'][:44]}**\n")
        for c in T['checks']:
            L.append(f"- {c['level'].upper()} {c['where']}: {c['what']}")
        L.append('')
    L += ['## What the plans never said (the assumptions, per house)\n']
    for r in rs:
        L.append(f"**{r['address'][:44]}**\n")
        for k, v in r['job'].get('hvac', {}).items():
            if k.startswith('_') and ('ASSUMED' in str(v) or 'NOT' in str(v) or 'UNREAD' in str(v) or 'ask' in str(v)):
                L.append(f"- {k[1:]}: {v}")
        L.append('')
    return '\n'.join(L)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('--all', action='store_true')
    a = ap.parse_args()
    if a.all:
        rs = [h for h in (house(d) for d in sorted(glob.glob(os.path.join(a.path, '*'))) if os.path.isdir(d)) if h]
        for r in rs:
            open(os.path.join(r['dir'], 'receipts.md'), 'w', encoding='utf-8').write(one(r))
        open(os.path.join(a.path, 'RECEIPTS.md'), 'w', encoding='utf-8').write(compare(rs))
        print(f'{len(rs)} houses -> RECEIPTS.md')
    else:
        r = house(a.path)
        open(os.path.join(a.path, 'receipts.md'), 'w', encoding='utf-8').write(one(r)); print('wrote receipts.md')
