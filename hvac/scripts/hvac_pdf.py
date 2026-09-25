#!/usr/bin/env python3
r"""hvac_pdf.py - the HVAC parts list as a printable PDF, one per model (the plumbing and framing lists do the same).

    python hvac_pdf.py <hvac_takeoff.json> <out.pdf> [--runs]        (--runs appends every run as a row)
    python hvac_pdf.py --all <jobs-dir> <pdf-dir>

The summary, the loads room by room, the system (zones and heads, or the air handler, registers and returns),
the ventilation, then the order by phase (equipment, rough-in, ventilation, trim, tests) and group, the
options, the checker's findings, the labour and the inspections. No prices: those are set on the price list.
PyMuPDF's Story lays the HTML out, the same way the plumbing and framing lists are printed.
"""
import sys, json, os, html, datetime, glob
import pymupdf

CSS = """
body { font-family: sans-serif; font-size: 8.5pt; color: #111; }
h1 { font-size: 15pt; margin: 0 0 2pt 0; }
h2 { font-size: 10.5pt; margin: 9pt 0 3pt 0; border-bottom: 0.6pt solid #888; padding-bottom: 1pt; }
p { margin: 1pt 0; }
.sub { color: #555; font-size: 8pt; }
table { border-collapse: collapse; width: 100%; margin: 2pt 0; }
th { text-align: left; font-size: 7.5pt; color: #444; border-bottom: 0.5pt solid #999; padding: 1pt 3pt; }
td { padding: 1pt 3pt; border-bottom: 0.3pt solid #ddd; vertical-align: top; }
td.n, th.n { text-align: right; }
.small { font-size: 7.5pt; color: #444; }
.warn { color: #a00; }
"""
PHASE_NAME = {'equip': 'Equipment', 'rough': 'Rough-in', 'vent': 'Ventilation and exhaust', 'trim': 'Trim', 'test': 'Start-up, tests and design'}


def esc(s):
    return html.escape(str(s if s is not None else ''))


def table(headers, rows, num_cols=()):
    h = '<table><tr>' + ''.join(f'<th class="{"n" if i in num_cols else ""}">{esc(x)}</th>' for i, x in enumerate(headers)) + '</tr>'
    for r in rows:
        h += '<tr>' + ''.join(f'<td class="{"n" if i in num_cols else ""}">{esc(x)}</td>' for i, x in enumerate(r)) + '</tr>'
    return h + '</table>'


def build_html(d, runs=False):
    T = d['totals']; sp = d['spec']; L = d['loads']; D = d['design']; LT = L['totals']
    out = [f'<h1>HVAC parts list - {esc(d.get("address") or d["slug"])}</h1>']
    out.append(f'<p class="sub">{esc(d.get("permit", ""))} &nbsp; model <b>{esc(d["slug"])}</b> &nbsp; printed {datetime.date.today()} &nbsp; '
               f'{esc(sp["kind"])} &nbsp; heat {T["heat_btuh"]:,} Btuh &nbsp; cooling {T["cool_tons"]} t &nbsp; {T["outdoor_units"]} outdoor &nbsp; {T["heads"]} heads &nbsp; '
               f'{T["indoor_ducted"]} ducted units &nbsp; {T["registers"]} registers &nbsp; line sets {T["lineset_ft"]:,} ft &nbsp; duct {T["duct_ft"]:,} ft &nbsp; vent {T["vent_ft"]:,} ft &nbsp; '
               f'{d["labour"]["total_days"]} days on site</p>')
    out.append(f'<p class="sub">Design {D["heat"]} F / {D["cool"]} F ({esc(D.get("town"))}: {esc(D.get("src"))}). Foundation {esc(sp["foundation"])}, line sets {esc(sp["lineset_route"])}, ducts {esc(sp["ducts"])}, '
               f'ventilation {esc(sp["ventilation"])}. Quantities only - the prices are set on the price list in the app.</p>')
    out.append('<h2>Loads</h2>')
    out.append(f'<p>heating {LT["heat_btuh"]:,} Btuh ({LT["heat_per_sf"]} Btuh/sf) · cooling {LT["cool_sens_btuh"]:,} + {LT["cool_lat_btuh"]:,} latent · WSU sheet {LT["wsu_btuh"]:,} Btuh · '
               f'infiltration {L["infiltration"]["ach50"]:g} ACH50 -> {L["infiltration"]["ach_nat"]} ACH at design · ventilation {L["ventilation"]["cfm"]} cfm ({esc(L["ventilation"]["kind"])})</p>')
    out.append(table(['room', 'storey', 'sf', 'heat Btuh', 'cool Btuh', 'glass sf', 'ext wall ft'],
                     [[r['name'] or r['key'], r['storey'], f"{r['area_sf']:.0f}", f"{r['heat_btuh']:,}", f"{r['cool_btuh']:,}", f"{r['win_sf']:.0f}", f"{r['ext_wall_ft']:.0f}"]
                      for r in sorted(d['rooms'], key=lambda r: -r['heat_btuh'])], (2, 3, 4, 5, 6)))
    out.append('<h2>The system</h2>')
    for s in d['systems']:
        out.append(f'<p><b>unit {esc(s["unit"])} - {esc(s["kind"])}</b>: heat {s["total_heat"]:,} Btuh, capacity at design {s.get("cap_at_design", 0):,} Btuh</p>')
        for o in s['outdoor']:
            out.append(f'<p class="small">outdoor {esc(o["part"])} {o["kbtuh"]}k ({esc(o["kind"])}) on the {esc(o["facing"])} wall, {esc(o.get("where", ""))}; {o.get("lineset_ft", 0)} ft of line set</p>')
        if s.get('zones'):
            out.append(table(['head in', 'zone rooms', 'carried', 'heat', 'cool'], [[z['host'], ', '.join(z['names'])[:60], ', '.join(z['carries'])[:50], f"{z['heat']:,}", f"{z['cool']:,}"] for z in s['zones']], (3, 4)))
        if s.get('heads'):
            out.append(table(['head', 'room', 'storey', 'heat', 'cool'], [[f"{h['kbtuh']}k", h['room'], h['storey'], f"{h['heat']:,}", f"{h['cool']:,}"] for h in s['heads']], (3, 4)))
        for x in s.get('indoor', []):
            out.append(f'<p class="small">indoor {esc(x["part"])} {x["kbtuh"]}k in {esc(x["room"])} ({esc(x["storey"])}), {x["cfm"]} cfm</p>')
        if s.get('registers'):
            out.append(table(['register room', 'storey', 'cfm', 'duct'], [[g['room'], g['storey'], g['cfm'], f"{g['duct_in']} in"] for g in s['registers']], (2,)))
            out.append(table(['return', 'storey', 'cfm', 'duct', 'grille'], [[g['room'], g['storey'], g['cfm'], f"{g['duct_in']} in", g.get('grille', '')] for g in s['returns']], (2,)))
    out.append('<h2>Runs (measured, before waste)</h2>')
    out.append(table(['system / size', 'LF'], [[k, f'{v:,.0f}'] for k, v in d['run_ft'].items()], (1,)))
    groups = {}
    for l in d['order']:
        groups.setdefault(l['phase'], {}).setdefault(l['group'], []).append(l)
    for ph in ['equip', 'rough', 'vent', 'trim', 'test']:
        if ph not in groups:
            continue
        out.append(f'<h2>{esc(PHASE_NAME[ph])}</h2>')
        for g, rows in groups[ph].items():
            out.append(f'<p class="small"><b>{esc(g)}</b></p>')
            out.append(table(['item', 'measured', 'order', 'unit', 'note'], [[r['label'] + (' (option)' if r.get('option') else ''), f"{r['qty']:g}", r['order_qty'], r['unit'], (r.get('note') or '')[:110]] for r in rows], (1, 2)))
    out.append('<h2>The checker</h2>')
    if not d['checks']:
        out.append('<p>clean</p>')
    for c in d['checks']:
        out.append(f'<p class="{"warn" if c["level"] == "code" else "small"}"><b>{esc(c["level"].upper())}</b> {esc(c["where"])}: {esc(c["what"])}</p>')
    for n in d['notes']:
        out.append(f'<p class="small">note: {esc(n)}</p>')
    lb = d['labour']
    out.append('<h2>Labour and inspections</h2>')
    out.append(f'<p>crew of {lb["crew"]}: ' + ', '.join(f'{k} {v} h / {lb["days"].get(k, 0)} d' for k, v in lb['crew_hours'].items()) + f' - {lb["total_days"]} days at {lb["capacity_hr"]} h. {esc(lb["note"])}</p>')
    ins = d.get('inspections') or {}
    for s in ins.get('sequence', []):
        out.append(f'<p class="small"><b>{esc(s["name"])}</b> - {esc(s["when"])}; {esc(s["test"])}</p>')
    out.append(f'<p class="small">permit: {esc(ins.get("fee_source", ""))}</p>')
    if runs:
        out.append('<h2>Every run</h2>')
        out.append(table(['system', 'size', 'LF', 'storey', 'note'], [[r['system'], r['size'], f"{r['ft']:.1f}", r['storey'], r['note'][:100]] for r in d['runs']], (2,)))
    return ''.join(out)


def write_pdf(d, out, runs=False):
    story = pymupdf.Story(html=build_html(d, runs), user_css=CSS)
    writer = pymupdf.DocumentWriter(out)
    rect = pymupdf.paper_rect('letter'); where = rect + (36, 36, -36, -36)
    more = True
    while more:
        dev = writer.begin_page(rect)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
    writer.close()
    return out


if __name__ == '__main__':
    if sys.argv[1] == '--all':
        src, dst = sys.argv[2], sys.argv[3]
        os.makedirs(dst, exist_ok=True)
        for p in sorted(glob.glob(os.path.join(src, '*', 'hvac_takeoff.json'))):
            d = json.load(open(p, encoding='utf-8'))
            o = os.path.join(dst, f"{d['slug']}.pdf")
            write_pdf(d, o); print('wrote', o)
    else:
        d = json.load(open(sys.argv[1], encoding='utf-8'))
        write_pdf(d, sys.argv[2], '--runs' in sys.argv); print('wrote', sys.argv[2])
