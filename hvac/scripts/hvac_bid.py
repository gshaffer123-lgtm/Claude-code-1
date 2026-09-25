#!/usr/bin/env python3
r"""hvac_bid.py - the DRAFT HVAC bid: the takeoff turned into RVM bid line items, split the way a mechanical
contractor bills it - EQUIPMENT / ROUGH-IN / TRIM + START-UP - with the options priced on their own.

    python hvac_bid.py hvac_takeoff.json [--job job.json] [--out hvac_bid.json] [--prices prices.json] [--no-live]
                                         [--result trades/hvac/result.json]

Same line shape as every other RVM bid (`bidding/scripts/bidcalc.py`):

    {label, desc, qty, unit, rate, cost, price, cst, note}

and the money model bidcalc.py runs TODAY (references/formula.md Part A, as amended in the code):
materials off the LIVE price list matched on the catalog label; site time in whole DAYS at the day rate
("Site labor"); labour COST = paid hours (crew hours + 1 h a day) x (crew $70 + lead $80); the OWNER SALES FEE
5 % of the sale - the 2.75 % partner fee came off every calc 7/25 (bidcalc.py). The electrical, plumbing and
finish bids still carry the old 7.75 %; this one does not copy it.

    equipment  the outdoor unit(s), heads / air handler / ducted units, strip, ERV, thermostats - and the SET days
    rough-in   line sets, condensate, ducts, boots, registers' boots, exhaust ducts and caps, dryer and hood
               vents, the whole-house fan and its inlets, supports, sleeves, firestops - and the ROUGH days
    trim       registers and grilles, filters, start-up, air balance, the duct-leakage and ventilation flow
               tests, the permit load calc, labels - and the TRIM / START-UP days; the MECHANICAL PERMIT line
    options    wired zone controllers, a bath heater, a dryer duct power ventilator - priced, never in the sum

**Every HVAC price is unset today** - RVM has never sold HVAC and none of these labels are on the price list
(the market research gives street bands in references/research-hvac-market.md; they are not rates). The
quantities are real; the money prints blank; `references/prices-to-set.md` is the list Genaro has to fill.
`--prices prices.json` ({"label": {"rate": x, "cost": y}}) tries a scenario.

`--result` also writes the worker's trades/hvac/result.json (rvm-app scripts/order_trades.mjs contract) with
the /api/docs create body in "bid" - the office gets a draft bid filed under the HVAC trade. Nothing is sent.
"""
import argparse, json, os, re, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hvac_parts as HP

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = 'https://rvm-app.pages.dev'
LEAD_HR = 80.0      # bidcalc.py's crew rates - the roofing crew; placeholders for an HVAC crew
CREW_HR = 70.0
DAY_RATE_DEFAULT = 3000.0
FEE_OWNER = 0.05    # bidcalc.py: owner sales fee only (the 2.75 % partner fee came off 7/25)
SECTION_OF_PHASE = {'equip': 'equipment', 'rough': 'rough', 'vent': 'rough', 'trim': 'trim', 'test': 'trim'}
SECTION_OF_LABOUR = {'set': 'equipment', 'rough': 'rough', 'trim': 'trim', 'startup': 'trim'}
TITLE = {'equipment': 'Equipment', 'rough': 'Rough-in', 'trim': 'Trim, start-up and tests'}


def api_key():
    for p in (os.path.join('C:' + os.sep, 'Users', 'Naro2', 'Claud', 'build-radar', 'data', '.secrets'),
              os.path.expanduser('~/Claud/build-radar/data/.secrets'),
              os.path.join('C:' + os.sep, 'Users', 'Naro2', 'Claud', 'rvm-app', 'API-ACCESS.txt')):
        if os.path.exists(p):
            txt = open(p, encoding='utf-8').read()
            m = re.search(r'RVM_API_KEY\s*=\s*(\S+)', txt) or re.search(r'Bearer\s+([A-Za-z0-9_\-.]+)', txt)
            if m:
                return m.group(1)
    return os.environ.get('RVM_API_KEY', '')


def load_live(timeout=20):
    try:
        req = urllib.request.Request((os.environ.get('RVM_APP_URL') or BASE) + '/api/pricing',
                                     headers={'Authorization': 'Bearer ' + api_key(), 'User-Agent': 'Mozilla/5.0 curl/8.5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            j = json.loads(r.read().decode())
        out = {}
        for i in j.get('items', []) + j.get('custom', []):
            out[i['label']] = {'rate': i.get('rate'), 'cost': i.get('cost'), 'unit': i.get('unit'), 'desc': i.get('desc')}
        return out, f'live price list ({len(out)} labels)'
    except Exception as e:
        return {}, f'live price list unreachable ({e.__class__.__name__}) - every rate blank'


def build(tk, job=None, prices=None, source='none'):
    job = job or {}
    prices = prices or {}
    sections = {'equipment': [], 'rough': [], 'trim': []}
    options, unpriced = [], []

    def row(label, qty, unit, note='', desc=None):
        p = prices.get(label) or {}
        rate, cost = p.get('rate'), p.get('cost')
        return dict(label=label, desc=desc or p.get('desc') or label, qty=round(qty, 1), unit=unit, rate=rate, cost=cost,
                    price=None if rate is None else round(rate * qty, 2), cst=None if cost is None else round(cost * qty, 2), note=note)

    for o in tk['order']:
        p = HP.byId[o['part']]
        q = o['order_qty']
        if not q:
            continue
        if o['unit'] == 'LF':
            note = f"measured {o['qty']:,.0f} LF + {o.get('waste', 0):.0%} waste"
            if o.get('packs'):
                note += f" = {o['packs']} x {o['pack_ft']:g} ft {o['pack']}"
        else:
            note = ''
        if o.get('note'):
            note = (note + ' · ' if note else '') + o['note'][:160]
        r = row(p['cat'], q, o['unit'], note, desc=p['label'])
        if p.get('option'):
            options.append(r)
        else:
            sections[SECTION_OF_PHASE.get(o['phase'], 'rough')].append(r)
        if r['rate'] is None:
            unpriced.append((p['cat'], o['unit']))

    # site time: whole days per section at the day rate
    lb = tk['labour']
    sl = prices.get('Site labor') or {}
    day_rate = float(job.get('day_rate') or sl.get('rate') or DAY_RATE_DEFAULT)
    day_rate_src = 'job.json' if job.get('day_rate') else ('live price list "Site labor"' if sl.get('rate') else 'the ROOFING day rate ($3,000 placeholder) - NOT an HVAC day rate')
    days, hrs = {}, {}
    for ph, sec in SECTION_OF_LABOUR.items():
        days[sec] = days.get(sec, 0) + lb['days'].get(ph, 0)
        hrs[sec] = hrs.get(sec, 0) + lb['crew_hours'].get(ph, 0)
    for sec in sections:
        if days.get(sec):
            sections[sec].append(dict(label='Site labor', desc=f'HVAC {TITLE[sec].lower()} site time', qty=days[sec], unit='days', rate=day_rate, cost=None,
                                      price=round(days[sec] * day_rate, 2), cst=None,
                                      note=f"{hrs[sec]:,.1f} crew-hours at {lb['capacity_hr']} h/day (placeholder install minutes) · day rate from {day_rate_src}"))
    # the mechanical permit: a line to price, never guessed
    ins = tk.get('inspections') or {}
    fee = ins.get('permit_fee')
    sections['trim'].append(dict(label='Mechanical permit', desc=f"Mechanical permit - {ins.get('authority', ins.get('jurisdiction', ''))} ({ins.get('appliances', 0)} appliances, {ins.get('fans_and_vents', 0)} fans / vents)",
                                 qty=1, unit='EA', rate=fee, cost=fee, price=fee, cst=fee, note=ins.get('fee_source', '')))
    if fee is None:
        unpriced.append(('Mechanical permit', 'EA'))

    tot = {}
    for sec, rows in sections.items():
        mp = sum(r['price'] or 0 for r in rows if r['label'] != 'Site labor')
        mc = sum(r['cst'] or 0 for r in rows if r['label'] != 'Site labor')
        sp = sum(r['price'] or 0 for r in rows if r['label'] == 'Site labor')
        tot[sec] = dict(material_price=round(mp, 2), material_cost=round(mc, 2), site_price=round(sp, 2), sale=round(mp + sp, 2), lines=len(rows),
                        priced=sum(1 for r in rows if r['rate'] is not None))
    paid_hr = lb['total_hours'] + lb['total_days'] * 1.0
    labour_cost = paid_hr * (LEAD_HR + CREW_HR)
    sale = sum(t['sale'] for t in tot.values())
    fees = sale * FEE_OWNER
    cost = sum(t['material_cost'] for t in tot.values()) + labour_cost + fees
    T = tk['totals']
    sysw = []
    for s in tk['systems']:
        outs = ', '.join(f"{o['kbtuh']}k {'multi-zone' if o['kind'] == 'multi' else ('single-zone' if o['kind'] == 'single' else 'ducted heat pump')}" for o in s['outdoor'])
        if s.get('heads'):
            sysw.append(f"unit {s['unit']}: {outs} outdoor, {len(s['heads'])} wall heads (" + ', '.join(f"{h['kbtuh']}k {h['room']}" for h in s['heads']) + ')')
        if s.get('indoor'):
            sysw.append(f"unit {s['unit']}: {outs} outdoor, " + ', '.join(f"{x['kbtuh']}k {'air handler' if x['part'].startswith('eq_ahu') else 'ducted unit'} in {x['room']}" for x in s['indoor'])
                        + f", {len(s.get('registers', []))} supply registers, {len(s.get('returns', []))} returns" + (f", {s['backup_kw']} kW strip" if s.get('backup_kw') else ''))
    V = tk['loads']['ventilation']
    scope = dict(
        equipment=[f"design: {tk['design']['heat']} F heating / {tk['design']['cool']} F cooling ({tk['design'].get('town')}); heating load {T['heat_btuh']:,} Btuh, cooling {T['cool_tons']} tons (room-by-room, Manual J method)"]
                  + sysw + [f"cold-climate variable-capacity heat pump(s), A2L refrigerant, HSPF2 >= {(tk['spec'].get('system') or {}).get('hspf2_min', '-')} per the WSEC credit"],
        rough=[f"line sets {T['lineset_ft']:,} ft ({tk['spec']['lineset_route']}), condensate to daylight, communication cable",
               (f"ductwork {T['duct_ft']:,} ft: trunks, flex branches, boots, returns, transfer paths" if T['duct_ft'] else 'no ductwork (ductless)'),
               f"ventilation: {V['kind']} {V['cfm']} cfm continuous (WA M1505.4) - " + ('ERV with ducted supply / exhaust' if V['kind'] in ('erv', 'hrv') else 'whole-house fan on a 24 h control, outdoor-air inlets'),
               f"exhaust: every bath fan ducted and capped, dryer vent, range hood duct and cap - {T['vent_ft']:,} ft"],
        trim=['registers and grilles, first filters, start-up and charge verification, controls set-up',
              'tests: ventilation flow test' + (', duct leakage test' if any((o['part'] == 'cm_duct_test') for o in tk['order']) else '') + ', the permit load calculation',
              'inspections: ' + ', '.join(s['name'] for s in ins.get('sequence', []))])
    b = dict(address=tk.get('address'), slug=tk.get('slug'), permit=tk.get('permit'), trade='HVAC', price_source=source,
             sections=sections, options=options, unpriced=sorted(set(unpriced)), scope=scope,
             totals=dict(equipment=tot['equipment'], rough=tot['rough'], trim=tot['trim'], site_days=lb['total_days'], day_rate=day_rate,
                         paid_hours=round(paid_hr, 1), labour_cost=round(labour_cost, 2), sales_fees=round(fees, 2), fee_rate=FEE_OWNER, sale=round(sale, 2), cost=round(cost, 2),
                         margin=round(sale - cost, 2), option_price=round(sum(o['price'] or 0 for o in options), 2),
                         priced_lines=sum(t['priced'] for t in tot.values()), total_lines=sum(t['lines'] for t in tot.values())),
             caveats=['DRAFT. Nothing is sent, nothing is pushed to a client.',
                      f'{len(set(unpriced))} line labels have NO price on the RVM price list - the quantities are real, the money is not. See references/prices-to-set.md.',
                      f'The day rate used is {day_rate_src}.',
                      f'Labour COST uses bidcalc.py\'s crew rates (crew ${CREW_HR:.0f}/h + lead ${LEAD_HR:.0f}/h per paid hour) - a roofing crew, a placeholder for an HVAC crew.',
                      'Install minutes are PLACEHOLDERS - no task-level HVAC install hours were found (references/research-hvac-market.md 3.3).',
                      f'Sales fee {FEE_OWNER:.0%} (owner) - the current bidcalc.py rule.',
                      'The electrician wires every outdoor unit, air handler, fan and control; the fireplace, the range hood and the bath fans themselves are other trades\' supply.',
                      'The load calculation is the takeoff\'s own Manual J-method estimate; the permit may want it stamped on the jurisdiction\'s form (the "HVAC design and load calc" line).'])
    b['doc'] = doc_body(b, tk)
    return b


def doc_body(b, tk):
    """the POST /api/docs create body (rvm-app functions/api/docs.js) - a DRAFT bid filed under trade 'hvac'"""
    items = []
    for sec in ('equipment', 'rough', 'trim'):
        for r in b['sections'][sec]:
            rate = r['rate'] if r['rate'] is not None else 0
            items.append(dict(desc=f"[{TITLE[sec]}] {r['desc']}"[:160], qty=r['qty'], unit=r['unit'], rate=rate, cost=r['cost'] or 0,
                              amount=round(rate * r['qty'], 2), auto=True))
    scope = [f"{TITLE[k]}: " + '; '.join(v) for k, v in b['scope'].items()]
    return dict(action='create', type='bid', trade='hvac', scope=scope, lineItems=items, showLineItems=True,
                summary=summary(b, tk), propertyAddress=tk.get('address') or '')


def summary(b, tk):
    T = tk['totals']; t = b['totals']
    sys_ = '; '.join(b['scope']['equipment'][1:-1]) or tk['spec']['kind']
    codes = [c for c in tk['checks'] if c['level'] == 'code']
    data = [c for c in tk['checks'] if c['level'] == 'data']
    s = (f"HVAC takeoff from the plan set: {tk['spec']['kind']} ({(tk['spec'].get('system') or {}).get('option') or 'credit not read'}), heating load {T['heat_btuh']:,} Btuh at "
         f"{tk['design']['heat']} F, cooling {T['cool_tons']} tons. {sys_}. Ventilation {tk['loads']['ventilation']['kind']} {tk['loads']['ventilation']['cfm']} cfm. "
         f"{T['lineset_ft']:,} ft of line set, {T['duct_ft']:,} ft of duct, {T['vent_ft']:,} ft of vent / exhaust duct; {t['site_days']} crew-days (placeholder minutes). ")
    s += (f"{len(codes)} code finding(s), {len(data)} data finding(s) to confirm. " if (codes or data) else 'The checker is clean on code. ')
    s += (f"UNPRICED: {len(b['unpriced'])} labels have no rate on the RVM price list (references/prices-to-set.md)." if b['unpriced'] else f"Priced off {b['price_source']}: sale ${t['sale']:,.2f}.")
    return s[:1900]


def result_json(b, tk, job, report='hvac_report.md', model=None):
    """the worker's trades/hvac/result.json (rvm-app scripts/order_trades.mjs)"""
    lines = []
    for sec in ('equipment', 'rough', 'trim'):
        for r in b['sections'][sec]:
            l = dict(desc=f"[{TITLE[sec]}] {r['desc']}"[:160], qty=r['qty'], unit=r['unit'])
            if r['rate'] is not None:
                l['rate'] = r['rate']; l['amount'] = r['price']
            if r['cost'] is not None:
                l['cost'] = r['cost']
            lines.append(l)
    unknowns = [f"{c['where']}: {c['what']}" for c in tk['checks'] if c['level'] == 'data']
    for k, v in ((tk.get('spec') or {}).get('sources') or {}).items():
        if 'ASSUMED' in str(v) or 'NOT FOUND' in str(v) or 'UNREAD' in str(v):
            unknowns.append(f"{k.lstrip('_')}: {str(v)[:260]}")
    unknowns.append('mechanical permit fee: ' + ((tk.get('inspections') or {}).get('fee_source') or 'not found'))
    priced = b['totals']['priced_lines'] > 0 and not b['unpriced']
    return dict(trade='hvac', status='ok', priced=priced, subtotal=b['totals']['sale'] if priced else None, summary=b['doc']['summary'],
                lines=lines[:200], unknowns=unknowns[:40],
                options=[dict(label=o['desc'][:120], qty=o['qty'], unit=o['unit'], **({'price': o['price']} if o['price'] is not None else {})) for o in b['options']],
                report_file=report, model_file=model, bid=b['doc'], record_patch=None)


def md(b):
    T = b['totals']
    L = [f"# DRAFT HVAC bid - {b['address']}", f"\n`{b['slug']}` · permit {b.get('permit') or '-'} · prices: **{b['price_source']}** · {T['priced_lines']}/{T['total_lines']} lines have a rate\n",
         '> **This is a draft.** Nothing sent, nothing pushed. Every unpriced line is listed at the bottom - those are the prices to set.\n']
    for sec in ('equipment', 'rough', 'trim'):
        L.append(f"## {TITLE[sec]}\n")
        for s in b['scope'][sec]:
            L.append(f'- {s}')
        L.append('\n| item | qty | unit | rate | price | note |'); L.append('|---|---|---|---|---|---|')
        for l in b['sections'][sec]:
            L.append(f"| {l['desc'][:72]} | {l['qty']:,} | {l['unit']} | {('$%.2f' % l['rate']) if l['rate'] is not None else '—'} | {('$' + format(l['price'], ',.2f')) if l['price'] is not None else '—'} | {l['note'][:130]} |")
        t = T[sec]
        L.append(f"\n{TITLE[sec].lower()} subtotal: materials ${t['material_price']:,.2f} + site ${t['site_price']:,.2f} = **${t['sale']:,.2f}** ({t['priced']}/{t['lines']} lines priced)\n")
    L.append('## Options (priced on their own, not in the sale)\n')
    L.append('| item | qty | unit | rate | price |'); L.append('|---|---|---|---|---|')
    for a in b['options']:
        L.append(f"| {a['desc'][:90]} | {a['qty']:g} | {a['unit']} | {('$%.2f' % a['rate']) if a['rate'] is not None else '—'} | {('$' + format(a['price'], ',.2f')) if a['price'] is not None else '—'} |")
    L.append(f"\n## Totals\n\nsale **${T['sale']:,.2f}** · {T['site_days']} days at ${T['day_rate']:,.0f} · labour cost ${T['labour_cost']:,.2f} ({T['paid_hours']} paid h) · "
             f"owner fee {T['fee_rate']:.0%} ${T['sales_fees']:,.2f} · margin ${T['margin']:,.2f} · options ${T['option_price']:,.2f}\n")
    L.append('## Caveats\n')
    for c in b['caveats']:
        L.append(f'- {c}')
    L.append('\n## Prices to set (labels with no rate)\n')
    for label, unit in b['unpriced']:
        L.append(f'- {label} ({unit})')
    return '\n'.join(L)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('takeoff'); ap.add_argument('--job', default=None); ap.add_argument('--out', default=None)
    ap.add_argument('--prices', default=None); ap.add_argument('--no-live', action='store_true')
    ap.add_argument('--result', default=None, help='also write the worker result.json here')
    ap.add_argument('--model-file', default=None, help='the viewer payload named in result.json')
    a = ap.parse_args()
    tk = json.load(open(a.takeoff, encoding='utf-8'))
    d = os.path.dirname(os.path.abspath(a.takeoff))
    jp = a.job or os.path.join(d, 'job.json')
    job = json.load(open(jp, encoding='utf-8')) if os.path.exists(jp) else {}
    if a.prices:
        prices, src = json.load(open(a.prices, encoding='utf-8')), f'scenario file {os.path.basename(a.prices)}'
    elif a.no_live:
        prices, src = {}, 'none (--no-live)'
    else:
        prices, src = load_live()
    b = build(tk, job, prices, src)
    out = a.out or os.path.join(d, 'hvac_bid.json')
    json.dump(b, open(out, 'w', encoding='utf-8'), indent=1)
    open(os.path.join(os.path.dirname(out), 'hvac_bid.md'), 'w', encoding='utf-8').write(md(b))
    if a.result:
        os.makedirs(os.path.dirname(os.path.abspath(a.result)), exist_ok=True)
        rd = os.path.dirname(os.path.abspath(a.result))
        rel = lambda p: os.path.relpath(p, rd).replace('\\', '/') if p else None
        R = result_json(b, tk, job, report=rel(os.path.join(d, 'hvac_report.md')), model=rel(a.model_file) if a.model_file else None)
        json.dump(R, open(a.result, 'w', encoding='utf-8'), indent=1)
    T = b['totals']
    print(f"{b['slug']}: equipment {T['equipment']['lines']} / rough {T['rough']['lines']} / trim {T['trim']['lines']} lines, {len(b['options'])} options; "
          f"{T['priced_lines']}/{T['total_lines']} priced; {len(b['unpriced'])} labels to set; sale ${T['sale']:,.0f} ({src})")
