#!/usr/bin/env python3
r"""hvacscan.py - read what the PLAN SET says about heating, cooling and ventilation, with the page and
the words for every finding.

    python hvacscan.py plans.pdf  --out hvac_scan.json [--png energy_p{N}.png]
    python hvacscan.py --text plans.txt --out hvac_scan.json          (a text dump: no pages, no renders)

A residential set in Washington almost never has a mechanical sheet. What it has instead is the ENERGY
sheet - the WSEC-R Table R406 credit options the designer picked to get the permit - and that table
names the heating system: option 3.7 is a ductless mini-split sized to heat the whole house at design
temperature, 3.6 / 3.6a a centrally ducted air-source heat pump, 4 / 4c the heat-pump fuel-normalisation
row, 2.2 / 2.3 a tight house WITH a heat-recovery ventilator. The same credit NUMBER means different
things in the 2018 and 2021 codes, so the code year is read first and every option is mapped through it
(references/hvac-research.md 2).

What this reads, each with its page and a short quote (never more than the finding - no owner lines):

  code       WSEC year, dwelling-unit size, credits required
  credits    every energy option the sheet SELECTS (an X / a check / "= n CREDITS" / "OPTIONS SELECTED"),
             kept apart from the options a WSU form merely PRINTS with an empty box
  system     what those options + the heat-source line + any cut sheet say the heating system is
  equipment  model numbers on cut sheets (Mitsubishi MXZ/MSZ/MUZ/SVZ/PVA/PEAD/SEZ, Fujitsu AOU/ASU/ARU,
             Daikin, Carrier, Bosch ...) and their nominal capacity
  ventilation  ERV / HRV (and its model), the whole-house fan and its CFM, continuous-duty notes
  fans       every exhaust-fan CFM call-out; the RANGE HOOD CFM and whether the sheet asks make-up air
  dryer, fireplace (fuel), mechanical room / duct chase words
  envelope   ceiling / vault / wall / floor / slab R-values, window / door / skylight U-factors, the
             air-leakage target (ACH50) - the numbers the load calculation leans on
  areas      heated area by floor, garage, crawl space
  tests      duct-leakage and ventilation-flow testing notes

It also lists CONFLICTS it can see (two air-leakage targets, an ERV credit next to an exhaust-only fan,
a ducted credit next to a multi-zone cut sheet) - the questions a person answers in job.json.

**Nothing here decides the design.** job.json does, with a `_key` receipt per answer. Render the energy
sheet (`--png`) and LOOK at it: a credit table drawn as linework (Aldrich) has no text to read, and a
scanned set (Shaw) has no text layer at all - both come back `system: unknown` and say so.
"""
import argparse, json, os, re, sys
from collections import Counter, defaultdict

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ------------------------------------------------------------------ WSEC credit options -> what they mean
# 2021 WSEC-R (WAC 51-11R) Table R406.2 (fuel normalization) and R406.3 (energy credits); 2018 numbering
# differs. Keys are (year, option). Only the options that decide the HVAC scope are here; the rest are
# recorded with their printed text. references/hvac-research.md 2 / research-hvac-code.md 3.
OPTION_MEANING = {
    # --- 2021: Table R406.2 fuel normalization (the primary heating system type)
    ('2021', '1'): dict(kind='heat_pump_backup', system=None, note='heat pump with electric-resistance or combustion supplemental heat'),
    ('2021', '2'): dict(kind='combustion', system='furnace', note='combustion (gas / propane / oil) heating'),
    ('2021', '3'): dict(kind='resistance', system='resistance', note='electric resistance only (forced air or zonal)'),
    ('2021', '4'): dict(kind='heat_pump', system=None, note='heat pump meeting the federal standard (Table C403.3.2(2) or (9))'),
    ('2021', '4a'): dict(kind='heat_pump', system=None, note='heat pump row of Table R406.2'),
    ('2021', '4b'): dict(kind='heat_pump', system=None, note='heat pump row of Table R406.2'),
    ('2021', '4c'): dict(kind='heat_pump', system=None, note='heat pump meeting the federal standard (Table C403.3.2(2) or (9)) or air-to-water'),
    ('2021', '5'): dict(kind='other', system=None, note='all other heating systems'),
    # --- 2021: Table R406.3 energy credits that name the HVAC
    ('2021', '2.1'): dict(kind='ventilation', vent=None, ach50=2.0, note='air leakage 2.0 ACH50'),
    ('2021', '2.2'): dict(kind='ventilation', vent='hrv', ach50=1.5, sre=0.70, note='air leakage 1.5 ACH50 + whole-house ventilation with heat recovery (SRE >= 0.70)'),
    ('2021', '2.3'): dict(kind='ventilation', vent='hrv', ach50=0.6, sre=0.80, note='air leakage 0.6 ACH50 + whole-house ventilation with heat recovery (SRE >= 0.80)'),
    ('2021', '2.4'): dict(kind='ventilation', vent='hrv', ach50=0.6, sre=0.85, note='air leakage + high-efficiency heat recovery ventilation'),
    ('2021', '3.1'): dict(kind='equipment', system=None, note='high-efficiency HVAC equipment option 3.1'),
    ('2021', '3.2'): dict(kind='equipment', system=None, note='high-efficiency HVAC equipment option 3.2'),
    ('2021', '3.3'): dict(kind='equipment', system=None, note='high-efficiency HVAC equipment option 3.3'),
    ('2021', '3.4'): dict(kind='equipment', system=None, note='high-efficiency HVAC equipment option 3.4'),
    ('2021', '3.5'): dict(kind='equipment', system=None, note='high-efficiency HVAC equipment option 3.5'),
    ('2021', '3.6'): dict(kind='equipment', system='ducted', hspf2=9.4, note='air-source CENTRALLY DUCTED heat pump, HSPF2 >= 9.4 (HSPF 11.0); a NEEP cold-climate VCHP where the design temperature is 23 F or below'),
    ('2021', '3.6a'): dict(kind='equipment', system='ducted', hspf2=9.4, note='air-source CENTRALLY DUCTED heat pump, HSPF2 >= 9.4 (HSPF 11.0)'),
    ('2021', '3.7'): dict(kind='equipment', system='ductless', hspf2=9.0, note='DUCTLESS mini-split heat pump, no electric resistance in the primary living areas, HSPF2 >= 9 (HSPF 10), sized to heat the ENTIRE dwelling at design temperature'),
    ('2021', '4.1'): dict(kind='distribution', ducts_inside=True, note='HVAC distribution option 4.1 (ducts inside the conditioned space)'),
    # --- 2018 WSEC-R Table 406.2 (older sets: Shaw BUILD-24-0020 prints 2018)
    ('2018', '3.5'): dict(kind='equipment', system='ducted', note='2018: air-source centrally ducted heat pump (HSPF 11)'),
    ('2018', '3.6'): dict(kind='equipment', system='ductless', note='2018: ductless split heat pump, zonal control, no resistance in the primary living areas'),
    ('2018', '2.1'): dict(kind='ventilation', vent=None, ach50=3.0, note='2018: air leakage + ventilation option 2.1'),
    ('2018', '2.2'): dict(kind='ventilation', vent='hrv', ach50=2.0, note='2018: air leakage 2.0 ACH50 + HRV'),
    ('2018', '2.3'): dict(kind='ventilation', vent='hrv', ach50=1.5, note='2018: air leakage 1.5 ACH50 + HRV'),
    ('2018', '2.4'): dict(kind='ventilation', vent='hrv', ach50=0.6, note='2018: air leakage 0.6 ACH50 + HRV'),
}

# descriptions that name a system type whatever number the drafter printed beside them
DESC_SYSTEM = [
    (re.compile(r'DUCTLESS\s+(MINI[-\s]?SPLIT|SPLIT|HEAT\s+PUMP)', re.I), 'ductless'),
    (re.compile(r'CENTRALLY\s+DUCTED\s+HEAT\s+PUMP', re.I), 'ducted'),
    (re.compile(r'(GAS|NATURAL\s+GAS|PROPANE)\s+(FORCED[-\s]AIR\s+)?FURNACE', re.I), 'furnace'),
    (re.compile(r'ELECTRIC\s+RESISTANCE\s+ONLY', re.I), 'resistance'),
    (re.compile(r'AIR[-\s]TO[-\s]WATER', re.I), 'hydronic'),
]

# model-number families (maker, family regex, what it is). The capacity is the kBtuh digits in the model.
MODEL_FAMILIES = [
    ('Mitsubishi', r'MXZ-[A-Z0-9]{2,4}?(\d{2})[A-Z]{2,5}\d?', 'multizone_outdoor'),
    ('Mitsubishi', r'MUZ-[A-Z]{2,3}(\d{2})[A-Z]{2,4}\d?', 'single_outdoor'),
    ('Mitsubishi', r'MSZ-[A-Z]{2,3}(\d{2})[A-Z]{2,4}\d?', 'wall_head'),
    ('Mitsubishi', r'SEZ-[A-Z]{2,3}(\d{2})[A-Z]{2,4}\d?', 'ducted_indoor'),
    ('Mitsubishi', r'PEAD-[A-Z]{1,3}(\d{2})[A-Z]{2,4}\d?', 'ducted_indoor'),
    ('Mitsubishi', r'SVZ-[A-Z]{2,3}(\d{2})[A-Z]{2,4}\d?', 'air_handler'),
    ('Mitsubishi', r'PVA-[A-Z]{1,3}(\d{2})[A-Z]{2,4}\d?', 'air_handler'),
    ('Mitsubishi', r'PU[ZY]-[A-Z]{1,3}(\d{2})[A-Z]{2,4}\d?', 'central_outdoor'),
    ('Mitsubishi', r'(?:MLZ|SLZ)-[A-Z]{2,3}(\d{2})[A-Z]{2,4}\d?', 'cassette'),
    ('Fujitsu', r'AOU(\d{2})[A-Z]{3,6}\d?', 'outdoor'),
    ('Fujitsu', r'ASU(\d{2})[A-Z]{3,6}\d?', 'wall_head'),
    ('Fujitsu', r'ARU(\d{2})[A-Z]{3,6}\d?', 'ducted_indoor'),
    ('Fujitsu', r'AUU(\d{2})[A-Z]{3,6}\d?', 'cassette'),
    ('Daikin', r'RX[A-Z]{1,3}(\d{2})[A-Z]{3,6}\d?', 'single_outdoor'),
    ('Daikin', r'[2-5]MXL?S?(\d{2})[A-Z]{3,6}\d?', 'multizone_outdoor'),
    ('Daikin', r'FTX[A-Z]{1,3}(\d{2})[A-Z]{3,6}\d?', 'wall_head'),
    ('Daikin', r'DZ\d{1,2}[A-Z]{2}(\d{2})\d{2}[A-Z]?', 'central_outdoor'),
    ('Carrier/Bryant', r'38MAR[A-Z]{1,2}(\d{2})[A-Z0-9]{2,4}', 'single_outdoor'),
    ('Bosch', r'BOVA-(\d{2})[A-Z]{3,5}', 'central_outdoor'),
    ('Goodman', r'GSZ[A-Z]{1,2}\d?(\d{2})\d{2}', 'central_outdoor'),
]
TON_KBTU = {'06', '09', '12', '15', '18', '24', '30', '36', '42', '48', '54', '60'}

VENT_MODELS = [
    (re.compile(r'Frigate\s+ERV\s*(\d{2,3})', re.I), 'erv', 'VENTS Frigate ERV'),
    (re.compile(r'FV-(\d{2})VE[CH]\d', re.I), 'erv', 'Panasonic Intelli-Balance'),
    (re.compile(r'ComfoAir\s*(Q?\d{3})', re.I), 'hrv', 'Zehnder ComfoAir'),
    (re.compile(r'EV\s*PREMIUM\s*([SML])', re.I), 'erv', 'RenewAire EV Premium'),
    (re.compile(r'\bLUNOS\b', re.I), 'hrv', 'Lunos e2 (decentralised)'),
    (re.compile(r'\bB(\d{3})[EH]\d?\b'), 'hrv', 'Broan AI series'),
]
EXHAUST_MODELS = [
    (re.compile(r'AIR\s*KING\s+MODELS?\s+(AK\d{2,3}[A-Z]{0,3})', re.I), 'Air King'),
    (re.compile(r'\bFV-0(\d{3})V[A-Z0-9]{1,4}\b', re.I), 'Panasonic WhisperGreen'),
]

PRIVATE = re.compile(r'OWNER|E:\s*\S+@|@[\w.-]+\.\w+|\(\d{3}\)\s*\d{3}|\b\d{3}[.\-]\d{3}[.\-]\d{4}\b|PARCEL|TAX ID', re.I)


def pages_of(pdf=None, text=None):
    """[(page_number or None, text)]"""
    if text is not None:
        return [(None, text)]
    import fitz
    doc = fitz.open(pdf)
    return [(i + 1, p.get_text()) for i, p in enumerate(doc)]


def quote(t, s, e, pad=90):
    """a short, single-line quote around a match - with anything that looks like an owner line cut out"""
    a = max(0, s - pad); b = min(len(t), e + pad)
    q = ' '.join(t[a:b].split())
    parts = [p for p in re.split(r'(?<=[.;:])\s+', q) if not PRIVATE.search(p)]
    q = ' '.join(parts) if parts else ''
    return q[:260]


def num(s):
    try:
        return float(str(s).replace(',', ''))
    except Exception:
        return None


class Scan:
    def __init__(self, pages):
        self.pages = pages
        self.out = dict(code={}, credits=[], credits_mentioned=[], system={}, equipment=[], ventilation={}, fans=[],
                        hood={}, dryer={}, fireplace={}, mech_rooms=[], envelope={}, areas={}, tests={},
                        heat_source=[], conflicts=[], warnings=[])
        self.text_chars = sum(len(t or '') for _, t in pages)

    def each(self, rx, flags=re.I):
        r = re.compile(rx, flags) if isinstance(rx, str) else rx
        for pno, t in self.pages:
            if not t:
                continue
            for m in r.finditer(t):
                yield pno, t, m

    # --------------------------------------------------------------- code year and credit count
    def code(self):
        years = Counter()
        for pno, t, m in self.each(r'(2015|2018|2021|2024)\s*(?:EDITION\s+OF\s+THE\s+)?(?:WA(?:SHINGTON)?\.?\s*(?:STATE)?\s*)?(?:ENERGY\s+(?:CODE|DOCE)|WSEC)|WSEC[\s-]*(?:R\s*)?(2015|2018|2021|2024)'):
            years[m.group(1) or m.group(2)] += 1
        c = self.out['code']
        if years:
            c['wsec'] = years.most_common(1)[0][0]
            c['wsec_votes'] = dict(years)
            if len(years) > 1:
                self.out['warnings'].append(f'the set names more than one WSEC edition {dict(years)} - the most frequent ({c["wsec"]}) maps the option numbers')
        for pno, t, m in self.each(r'(SMALL|MEDIUM|LARGE)\s+DWELLING\s+UNIT'):
            c.setdefault('dwelling', m.group(1).lower()); c.setdefault('dwelling_page', pno)
        for pno, t, m in self.each(r'(\d+(?:\.\d)?)\s*(?:ENERGY\s+)?CREDITS?\s+REQUIRED|REQUIRING\s+(\d+(?:\.\d)?)\s+CREDITS'):
            v = num(m.group(1) or m.group(2))
            if v and 'credits_required' not in c:
                c['credits_required'] = v; c['credits_page'] = pno
        for pno, t, m in self.each(r'TOTAL\s+(?:OF\s+ABOVE\s+OPTIONS\s*=\s*)?(\d+(?:\.\d)?)\s*CREDITS'):
            c.setdefault('credits_total', num(m.group(1)))

    # --------------------------------------------------------------- selected credit options
    def credits(self):
        year = self.out['code'].get('wsec', '2021')
        seen = {}
        pats = [
            # "X NOTES FOR ENERGY OPTION 2.3 (2 CREDITS)" - the WSU form's checked notes
            (r'(?:^|[\s\]])[X\u2612\u2611\u25a0\u2713\u2714]\s*NOTES\s+(?:FOR|ON)\s+ENERGY\s+OPTION\s+(\d\.\d{1,2}[a-z]?)', 'checked note'),
            # "OPTION (5.6) ... = 2.0 CREDITS" / "(3.6a) = 1.0 CREDIT" / "(2.2) ... = 1.5 CREDITS" - but never the
            # "(2)" of a code section like "TABLE C403.3.2(2) ... = 3.0 CREDITS" (Sudden Valley read that as option 2)
            (r'(?<![\w.])\((\d(?:\.\d{1,2})?[a-z]?)\)[^=\n]{0,260}?=\s*(\d+(?:\.\d+)?)\s*CREDITS?', 'option = credits'),
            # "PRIMARY HEATING SOURCE (4c)"
            (r'PRIMARY\s+HEATING\s+SO?URCE\s*\((\d[a-z]?)\)', 'primary heating source'),
            # "2.1 AIR LEAKAGE CONTROL ... OPTIONS" / "3.7 HIGH EFFICIENCY HVAC ... OPTIONS" (a selected-options list)
            (r'(?:^|\n)\s*(\d\.\d{1,2}[a-z]?)\s+(AIR\s+LEAKAGE[^\n]{0,60}|HIGH\s+EFFICIENCY\s+HVAC[^\n]{0,60}|EFFICIENT\s+WATER\s+HEATING[^\n]{0,40}|EFFICIENT\s+BUILDING\s+ENVELOPE[^\n]{0,40})\s*OPTIONS?', 'options-selected list'),
            # "4 FOR HEATING SYSTEM USING A HEAT PUMP" under "OPTIONS SELECTED"
            (r'OPTIONS\s+SELECTED[^\n]{0,80}\n\s*(\d[a-z]?)\s+FOR\s+HEATING\s+SYSTEM', 'options-selected list'),
        ]
        for rx, how in pats:
            for pno, t, m in self.each(rx):
                opt = m.group(1).lower()
                # an empty checkbox right before it means PRINTED, not selected
                pre = t[max(0, m.start() - 4):m.start() + 1]
                if '\u2610' in pre:
                    continue
                credits = num(m.group(2)) if how == 'option = credits' else None
                key = opt
                meaning = OPTION_MEANING.get((year, opt)) or OPTION_MEANING.get((year, opt.rstrip('abc'))) or {}
                row = seen.get(key) or dict(option=opt, year=year, how=[], page=pno, quote=quote(t, m.start(), m.end()),
                                            meaning=meaning.get('note', ''), **{k: v for k, v in meaning.items() if k != 'note'})
                if how not in row['how']:
                    row['how'].append(how)
                if credits is not None:
                    row['credits'] = credits
                seen[key] = row
        # descriptions that are printed with a selected option's number nearby
        for pno, t, m in self.each(r'(\d\.\d{1,2}[a-z]?)\s+(?:[A-Z][A-Z &\-]{5,80}\n\s*)?(Ductless mini-split heat pump system[^\n]{0,200}|Air-source,? centrally ducted heat pump[^\n]{0,200})'):
            opt = m.group(1).lower()
            if opt in seen:
                seen[opt].setdefault('description', ' '.join(m.group(2).split())[:220])
        # the WSU form prints the WHOLE table: descriptions next to an empty box are only MENTIONED
        for pno, t, m in self.each(r'\u2610\s*(\d(?:\.\d{1,2})?[a-z]?)\b'):
            self.out['credits_mentioned'].append(dict(option=m.group(1).lower(), page=pno))
        self.out['credits'] = sorted(seen.values(), key=lambda r: [float(x) if x.replace('.', '').isdigit() else 99 for x in re.findall(r'[\d.]+', r['option'])[:1]] + [r['option']])

    # --------------------------------------------------------------- equipment on cut sheets
    def equipment(self):
        found = {}
        for maker, rx, kind in MODEL_FAMILIES:
            for pno, t, m in self.each(r'\b' + rx + r'\b', 0):
                model = m.group(0)
                kb = m.group(1)
                kbtuh = int(kb) if kb in TON_KBTU else None
                if model in found:
                    found[model]['pages'].add(pno)
                    continue
                found[model] = dict(model=model, maker=maker, kind=kind, kbtuh_nominal=kbtuh, pages={pno}, quote=quote(t, m.start(), m.end(), 60))
        rows = []
        for r in found.values():
            r['pages'] = sorted(p for p in r['pages'] if p is not None)
            rows.append(r)
        # rated heating capacity printed on a cut sheet ("Rated Capacity BTU/H 66,000", "Heating at 47")
        caps = []
        for pno, t, m in self.each(r'Rated\s+Capacity\s+BTU/?H\s+([\d,]{5,7})'):
            caps.append(dict(btuh=num(m.group(1)), page=pno, quote=quote(t, m.start(), m.end(), 60)))
        self.out['equipment'] = rows
        if caps:
            self.out['equipment_capacity'] = caps
        for pno, t, m in self.each(r'Heat\s+Source:\s*([A-Za-z \-]{4,40})'):
            self.out['heat_source'].append(dict(text=' '.join(m.group(1).split()), page=pno))
        for pno, t, m in self.each(r'MXZ[^\n]{0,80}|Non-Ducted\s*//\s*Mix\s*//\s*Ducted', 0):
            if 'Non-Ducted' in m.group(0):
                self.out['equipment_note'] = 'the cut sheet rates the outdoor unit Non-Ducted // Mix // Ducted - a multi-zone that is ducted or not depending on the INDOOR units chosen'

    # --------------------------------------------------------------- ventilation, fans, hood, dryer, fireplace
    def ventilation(self):
        v = self.out['ventilation']
        for rx, kind, name in VENT_MODELS:
            for pno, t, m in self.each(rx):
                v.setdefault('models', []).append(dict(kind=kind, name=name, model=' '.join(m.group(0).split()), page=pno))
        for pno, t, m in self.each(r'\b(ERV|HRV|ENERGY\s+RECOVERY\s+VENTILAT\w*|HEAT\s+RECOVERY\s+VENTILAT\w*)\b', 0):
            v.setdefault('hrv_words', []).append(dict(word=m.group(1), page=pno, quote=quote(t, m.start(), m.end(), 50)))
        for pno, t, m in self.each(r'SENSIBLE\s+HEAT\s+RECOVERY\s+EFFICIENCY\s+OF\s+(0\.\d+)'):
            v.setdefault('sre_required', num(m.group(1)))
        for pno, t, m in self.each(r'(\d{2,3})\s*CFM\s+FAN\s+MIN\.?\s+FOR\s+CONT\w*\.?\s+WHOLE\s+HOUSE'):
            v.setdefault('whf', []).append(dict(cfm=num(m.group(1)), page=pno, quote=quote(t, m.start(), m.end(), 40)))
        for pno, t, m in self.each(r'WHOLE[\s-]+HOUSE\s+(?:VENTILATION\s+)?FAN|HOUSE\s+WHOLE\s+FAN|\bWHF\b'):
            v.setdefault('whf_words', []).append(dict(page=pno, quote=quote(t, m.start(), m.end(), 60)))
        for rx, maker in EXHAUST_MODELS:
            for pno, t, m in self.each(rx):
                v.setdefault('exhaust_models', []).append(dict(maker=maker, model=' '.join(m.group(0).split()), page=pno))
        for pno, t, m in self.each(r'CONTINUOUS\s+OPERATION|CONT(?:INUOUS)?\.?\s+WHOLE\s+HOUSE\s+OPERATION|CAPABLE\s+OF\s+CONTINUO?US'):
            v['continuous_note'] = True
        # kind, from the evidence
        hrv = bool(v.get('models') or [w for w in v.get('hrv_words', []) if w['word'].upper() in ('ERV', 'HRV')])
        whf = bool(v.get('whf') or v.get('whf_words'))
        v['kind'] = 'erv' if hrv and not any(mm['kind'] == 'hrv' for mm in v.get('models', [])) else ('hrv' if hrv else ('exhaust' if whf else 'unknown'))
        if hrv and whf:
            v['both'] = True

    def fans(self):
        rows = []
        for pno, t, m in self.each(r'(\d{2,3})\s*CFM\b'):
            cfm = num(m.group(1))
            ctx = t[max(0, m.start() - 80):m.end() + 80].upper()
            if 'HOOD' in ctx or 'RANGE' in ctx:
                where = 'hood'
            elif 'WHOLE' in ctx or 'CONT' in ctx or 'WHF' in ctx:
                where = 'whole-house'
            elif 'MAKE' in ctx and 'AIR' in ctx:
                where = 'hood'
            else:
                where = 'exhaust'
            rows.append(dict(cfm=cfm, where=where, page=pno, quote=quote(t, m.start(), m.end(), 50)))
        self.out['fans'] = rows
        # the range hood: a CFM figure within reach of HOOD / RANGE, and a make-up air word near it
        hood = self.out['hood']
        for pno, t, m in self.each(r'(\d{3,4})\s*CFM'):
            ctx = t[max(0, m.start() - 120):m.end() + 120].upper()
            if ('HOOD' in ctx or 'RANGE' in ctx) and 'EXCEED' not in ctx[100:140]:
                c = num(m.group(1))
                if c and c >= 150 and (not hood.get('cfm') or c > hood['cfm']):
                    hood.update(cfm=c, page=pno, quote=quote(t, m.start(), m.end(), 70),
                                makeup_air=bool(re.search(r'MAKE-?\s?UP\s+AIR', ctx)))
        for pno, t, m in self.each(r'MAKE-?\s?UP\s+AIR\s+SHALL\s+BE\s+PROVIDED[^\n]{0,120}'):
            hood.setdefault('code_note', quote(t, m.start(), m.end(), 20))

    def appliances(self):
        d = self.out['dryer']
        for pno, t, m in self.each(r'\bDRYER\b|\bW\s*/\s*D\b|WASHER\s*/\s*DRYER'):
            d.setdefault('words', []).append(dict(page=pno, quote=quote(t, m.start(), m.end(), 40)))
        for pno, t, m in self.each(r'GAS\s+DRYER'):
            d['gas'] = True
        fp = self.out['fireplace']
        for pno, t, m in self.each(r'GAS\s+FP\b|GAS\s+FIRE\s*PLACE|FIRE\s*PLACE|WOOD\s*STOVE|\bFP\b'):
            q = quote(t, m.start(), m.end(), 60)
            note = bool(re.search(r'SHALL|COMPLY|SECTION|INSTALLATION|PER\s+(?:IRC|MFG)', q, re.I))
            fp.setdefault('callouts' if not note else 'code_notes', []).append(dict(word=' '.join(m.group(0).split()), page=pno, quote=q))
        callouts = fp.get('callouts', [])
        if any('GAS' in c['word'].upper() for c in callouts):
            fp['fuel'] = 'gas'
        elif callouts:
            fp['fuel'] = 'unknown'
        fp['present'] = bool(callouts)
        for pno, t, m in self.each(r'MECHANICAL\s+ROOM[^\n]{0,40}|\bMECH\.?\s*(?:ROOM|RM|CLOS\w*)\b|DUCT\s+CHASE|\bFURNACE\b|AIR\s+HANDLER|\bAHU\b'):
            self.out['mech_rooms'].append(dict(word=' '.join(m.group(0).split()), page=pno))

    # --------------------------------------------------------------- envelope and areas
    def envelope(self):
        e = self.out['envelope']
        def put(k, v, pno, q):
            if v is None:
                return
            e.setdefault(k, []).append(dict(v=v, page=pno, quote=q))
        for pno, t, m in self.each(r'(?<!VAULTED\s)CEILING\s+R-?VALUE\s+(\d{2})'):
            put('ceiling_r', num(m.group(1)), pno, quote(t, m.start(), m.end(), 20))
        for pno, t, m in self.each(r'VAULTED\s+CEILING\s+R-?VALUE\s+(\d{2})'):
            put('vault_r', num(m.group(1)), pno, quote(t, m.start(), m.end(), 20))
        for pno, t, m in self.each(r'WOOD\s+FRAME\s+WALL\s+(\d{2})\s*\+\s*(\d{1,2})'):
            put('wall', f'R-{m.group(1)}+{m.group(2)}', pno, quote(t, m.start(), m.end(), 20))
        for pno, t, m in self.each(r'\bR-(\d{2})\s*\+\s*(\d{1,2})\b'):
            put('wall', f'R-{m.group(1)}+{m.group(2)}', pno, quote(t, m.start(), m.end(), 30))
        for pno, t, m in self.each(r'FLOOR\s+R-?VALUE\s+(\d{2})|R-(\d{2})\s+(?:MIN\.?\s+)?(?:SUPPORTED\s+)?(?:BATT\s+)?FLOOR\s+INSULATION|R-(\d{2})\s+(?:SUPPORTED\s+)?BATT\s+INSULATION\s+(?:BETWEEN|UNDER)'):
            put('floor_r', num(m.group(1) or m.group(2) or m.group(3)), pno, quote(t, m.start(), m.end(), 30))
        # the WSU prescriptive table as a designer fills it in (Semiahmoo): "ROOF/CEILING ... R-60",
        # "WOOD FRAME WALL R-21 BATT INSULATION W/ R-12 CONTINUOUS", "FLOOR OVER UNHEATED SPACE R-38", "SLAB ON GRADE R-10"
        for pno, t, m in self.each(r'ROOF\s*/\s*CEILING[^\n]{0,40}?R-(\d{2})'):
            put('ceiling_r', num(m.group(1)), pno, quote(t, m.start(), m.end(), 20))
        for pno, t, m in self.each(r'WOOD\s+FRAME\s+WALL\s+R-(\d{2})\s+BATT\s+INSULATION\s+W/\s+R-(\d{1,2})\s+CONTINUOUS'):
            put('wall', f'R-{m.group(1)}+{m.group(2)}', pno, quote(t, m.start(), m.end(), 20))
        for pno, t, m in self.each(r'FLOOR\s+OVER\s+UNHEATED\s+SPACE\s+R-(\d{2})'):
            put('floor_r', num(m.group(1)), pno, quote(t, m.start(), m.end(), 20))
        for pno, t, m in self.each(r'SLAB\s+ON\s+GRADE\s+R-(\d{1,2})'):
            put('slab_r', num(m.group(1)), pno, quote(t, m.start(), m.end(), 20))
        for pno, t, m in self.each(r'VERTICAL\s+FENESTRATION\s+U\s*=\s*(0\.\d{2})'):
            put('window_u', num(m.group(1)), pno, quote(t, m.start(), m.end(), 20))
        # a batt in a ROOF / ceiling assembly, read only where the words BEFORE it say ceiling and not wall
        for pno, t, m in self.each(r'R-(\d{2})\s+BATT\s+INSULATION'):
            before = t[max(0, m.start() - 120):m.start()].upper()
            if re.search(r'CEIL|TRUSS|RAFTER|ROOF', before[-80:]) and not re.search(r'WALL|STUD', before[-60:]):
                put('ceiling_r_assembly', num(m.group(1)), pno, quote(t, m.start(), m.end(), 40))
        for pno, t, m in self.each(r'SLAB\s+R-?VALUE\s*/\s*DEPTH\s+(\d{1,2})\s*/\s*(\d)'):
            put('slab_r', num(m.group(1)), pno, quote(t, m.start(), m.end(), 20))
        for pno, t, m in self.each(r'SKYLIGHT\s+U-?FACTOR\s+(0\.\d{2})'):
            put('skylight_u', num(m.group(1)), pno, quote(t, m.start(), m.end(), 20))
        for pno, t, m in self.each(r'FENESTRATION\s+U-?FACTOR\s+(0\.\d{2})'):
            put('window_u', num(m.group(1)), pno, quote(t, m.start(), m.end(), 20))
        # a section drawn with bare R-labels (Aldrich A-7: "R-60 ... R-21+5 ... R-38 6 MIL. VAPOR BARRIER"): the
        # largest R >= 49 is the ceiling, an R-30/38 beside a vapour barrier / crawl / floor word is the floor
        if not e.get('ceiling_r'):
            bare = [(pno, t, m) for pno, t, m in self.each(r'(?<![\w+])R-(49|60|70)\b(?!\s*\+)')]
            if bare:
                pno, t, m = max(bare, key=lambda x: int(x[2].group(1)))
                put('ceiling_r', num(m.group(1)), pno, quote(t, m.start(), m.end(), 30) + ' [bare section label - the largest R on the set]')
        if not e.get('floor_r'):
            for pno, t, m in self.each(r'(?<![\w+])R-(30|38)\b(?!\s*\+)'):
                ctx = t[m.end():m.end() + 60].upper() + t[max(0, m.start() - 40):m.start()].upper()
                if re.search(r'VAPOR|CRAWL|FLOOR|JOIST', ctx):
                    put('floor_r', num(m.group(1)), pno, quote(t, m.start(), m.end(), 30) + ' [bare section label beside a floor / vapour-barrier word]')
                    break
        # WSEC's resistance-heat allowance printed with the credit table
        for pno, t, m in self.each(r'ALTERNATIVE\s+HEATING\s+SOURCE\s+SIZED\s+AT\s+A\s+MAXIMUM\s+OF\s+(0\.\d+)\s*W(?:ATTS)?\s*/\s*(?:FT2|SF|FT²)[^\n]{0,60}?(\d{3,4})\s*W'):
            e['resistance_allowance'] = dict(w_per_sf=num(m.group(1)), w_min=num(m.group(2)), page=pno, quote=quote(t, m.start(), m.end(), 10))
        us = Counter()
        for pno, t, m in self.each(r'U-?VALUE[\s\S]{0,400}'):
            for u in re.findall(r'\b0\.(1[4-9]|2\d|3[0-5])\b', m.group(0)):
                us['0.' + u] += 1
        if us:
            e['schedule_u'] = dict(us.most_common(6))
        for pno, t, m in self.each(r'(\d(?:\.\d{1,2})?)\s+AIR\s+CHANGES\s+PER\s+HOUR|(\d(?:\.\d{1,2})?)\s+(?:ACH|CPH)\b'):
            v = num(m.group(1) or m.group(2))
            if not v or v > 7:
                continue
            if re.search(r'SHALL\s+NOT\s+EXCEED', t[max(0, m.start() - 40):m.start()], re.I):
                e['ach50_code_max'] = v          # R402.4.1.2's ceiling, not this house's target
                continue
            put('ach50', v, pno, quote(t, m.start(), m.end(), 50))
        # the three that decide a load: collapse to one value each and say when the sheet disagrees with itself
        if not e.get('ceiling_r') and e.get('ceiling_r_assembly'):
            e['ceiling_r'] = e['ceiling_r_assembly']
        for k in ('ceiling_r', 'floor_r', 'ach50', 'wall', 'skylight_u', 'window_u', 'slab_r', 'vault_r'):
            vals = [r['v'] for r in e.get(k, [])]
            if not vals:
                continue
            c = Counter(vals)
            e[k + '_value'] = c.most_common(1)[0][0] if k != 'ach50' else min(vals)
            if len(c) > 1 and k in ('ach50', 'ceiling_r', 'floor_r'):
                self.out['conflicts'].append(dict(what=f'{k}: the set prints {dict(c)}', use=e[k + '_value'],
                                                  why='two values for one requirement; the tighter one is used for ACH50, the most frequent for R-values - confirm on the energy sheet'))

    def areas(self):
        a = self.out['areas']
        rx = [
            ('heated_sf', r'TOTAL\s+HEATED\s+AREA\s*=?\s*([\d,]{3,6})'),
            ('heated_sf', r'ACTUAL\s+S\.?F\.?\s+([\d,]{3,6})'),
            ('main_sf', r'MAIN\s+FLOOR\s+(?:AREA:?\s*)?([\d,]{3,6})\s*(?:S\.?F|FT)'),
            ('upper_sf', r'(?:UPPER|SECOND)\s+FLOOR\s+(?:AREA:?\s*)?=?\s*([\d,]{3,6})\s*(?:S\.?F|FT)'),
            ('garage_sf', r'GARAGE\s+(?:FLOOR\s+AREA:?\s*)?=?\s*([\d,]{3,6}(?:\.\d+)?)\s*(?:S\.?F|FT)'),
            ('crawl_sf', r'([\d,]{3,6})\s*SF\s+CRAWLSPACE|CRAWLSPACE\s*=?\s*([\d,]{3,6})\s*(?:SQ\.?\s*FT|SF)'),
            ('upper_sf', r'AREA\s+OF\s+UPPER\s+FLOOR\s*=\s*([\d,]{3,6})'),
            # the drafting software's level tags: "Main Level Living 2,120.95 sf", "Upper Level Living 1,290.96 sf"
            ('main_living_sf', r'(?:MAIN|FIRST)\s+LEVEL\s+LIVING\s+([\d,]{3,6}(?:\.\d+)?)\s*SF'),
            ('upper_living_sf', r'(?:UPPER|SECOND)\s+LEVEL\s+LIVING\s+([\d,]{3,6}(?:\.\d+)?)\s*SF'),
            ('lower_living_sf', r'LOWER\s+LEVEL\s+LIVING\s+([\d,]{3,6}(?:\.\d+)?)\s*SF'),
        ]
        for k, r in rx:
            for pno, t, m in self.each(r):
                v = num(next(g for g in m.groups() if g))
                if v and k not in a:
                    a[k] = v; a[k + '_page'] = pno

    # --------------------------------------------------------------- the window / glazed-door schedule
    def openings(self):
        """glazing is the biggest single heat-loss line on a WSEC house and the tracer finds a third to all of it
        (Ridgeway: 10 traced windows, 25 on the schedule + two 8-12 ft sliders). Two printed forms are read:
          '3/0 X 7/6 9'-0" CSMT 0.22'   (schedule rows: W ft/in X H ft/in, header height, operation, U)
          '6' - 0" x 6' - 0" XO'        (per-opening call-outs on the plan: XO / PIC / SH / TRAP / OHD)
        A door row only counts when it is a glazed PATIO door (a slider 5 ft or wider); interior and garage
        doors, and the parts of a mulled unit ('FIX OVER 3/0 X 3/0'), are left out. It is a CHECK on the traced
        count, not a replacement for reading the schedule: job.json `glazing` is the answer."""
        OPS = r'(DBL\s+SLIDER|SLIDER|FIXED|FIX|CSMT|CASEMENT|AWN\w*|SH|DH|SGL\s+HUNG|PIC|XO|OX|TRAP|OHD|SWING|POCKET|OVERHEAD)'
        rows = []
        f1 = re.compile(r'([A-Z][A-Z .0-9]{0,16}?)\s+(\d{1,2})/(\d{1,2})\s*X\s*(\d{1,2})/(\d{1,2})((?:\s+\d{1,2}\'-\d{1,2}")?(?:\s+' + OPS + r')?(?:\s+0\.\d{2})?)', re.I)
        for pno, t, m in self.each(f1):
            pre = t[max(0, m.start() - 12):m.start()].upper()
            post = t[m.end():m.end() + 14].upper()
            word = ' '.join(m.group(1).split()).upper()
            # the parts of a mulled unit ("3/0 X 5/0 FIX OVER 3/0 X 3/0 FIX, MULLED") - the unit row carries the whole
            if 'OVER' in pre or 'OVER' in word or 'OVER' in post or 'MULLED' in post:
                continue
            w = int(m.group(2)) + int(m.group(3)) / 12; h = int(m.group(4)) + int(m.group(5)) / 12
            tail = m.group(6) or ''
            op = (re.search(OPS, tail, re.I).group(1).upper() if re.search(OPS, tail, re.I) else '')
            hdr = bool(re.search(r"\d{1,2}'-\d{1,2}\"", tail))
            u = re.search(r'(0\.\d{2})', tail)
            interior = bool(re.search(r'\bCLOS|\bW\.?I\.?C|PANTRY|PTRY|LINEN|PWDR|\bBATH|MUDROOM|LAUNDRY|OFFICE|BED\b|BED\.', word))
            if 'GARAGE' in word or op in ('OHD', 'OVERHEAD'):
                kind = 'garage'
            elif op in ('SWING', 'POCKET') or (interior and h >= 6.6):
                kind = 'door'
            elif 'SLIDER' in op and h >= 6.6 and w >= 5:
                kind = 'patio'
            elif h >= 6.6 and not hdr and op not in ('FIXED', 'FIX', 'CSMT', 'CASEMENT', 'PIC', 'XO'):
                kind = 'door'
            else:
                kind = 'window'
            rows.append(dict(form='schedule', word=word, w_ft=round(w, 3), h_ft=round(h, 3), sf=round(w * h, 1), op=op, kind=kind,
                             u=num(u.group(1)) if u else None, page=pno))
        f2 = re.compile(r'(\d{1,2})\'\s*-\s*(\d{1,2}(?:\s+\d/\d)?)"?\s*x\s*(\d{1,2})\'\s*-\s*(\d{1,2}(?:\s+\d/\d)?)"?\s*' + OPS + r'?', re.I)
        for pno, t, m in self.each(f2):
            def ft(a, b):
                b = b.split()
                inch = float(b[0]) + (eval(b[1]) if len(b) > 1 else 0)
                return int(a) + inch / 12
            w = ft(m.group(1), m.group(2)); h = ft(m.group(3), m.group(4))
            op = (m.group(5) or '').upper()
            if op in ('OHD', 'OVERHEAD'):
                kind = 'garage'
            elif op in ('XO', 'OX', 'PIC', 'SH', 'DH', 'TRAP', 'FIX', 'FIXED', 'CSMT', 'CASEMENT', 'AWN', 'SLIDER'):
                kind = 'patio' if (h >= 6.6 and w >= 5) else 'window'
            elif h >= 6.6:
                kind = 'door'
            else:
                kind = 'window?'
            rows.append(dict(form='callout', word='', w_ft=round(w, 3), h_ft=round(h, 3), sf=round(w * h, 1), op=op, kind=kind, page=pno))
        tot = defaultdict(float)
        for r in rows:
            tot[r['kind']] += r['sf']
        us = [r['u'] for r in rows if r.get('u')]
        self.out['openings'] = dict(rows=rows, window_sf=round(tot['window'], 1), patio_sf=round(tot['patio'], 1),
                                    uncertain_sf=round(tot['window?'], 1), door_rows=sum(1 for r in rows if r['kind'] == 'door'),
                                    count=sum(1 for r in rows if r['kind'] in ('window', 'patio')),
                                    u_mean=round(sum(us) / len(us), 3) if us else None,
                                    note='read off the text layer; mulled parts and interior / garage doors left out - LOOK at the schedule before trusting the total')

    def tests(self):
        tt = self.out['tests']
        if any(True for _ in self.each(r'DUCT\s+LEAKAGE\s+TEST')):
            tt['duct_leakage'] = True
        if any(True for _ in self.each(r'NOT\s+REQUIRED\s+IF\s+DUCTS\s+AND\s+AIR\s+HANDLERS\s+ARE\s+LOCATED\s+ENTIRELY\s+WITHIN')):
            tt['duct_exception_note'] = True
        if any(True for _ in self.each(r'TESTING\s+SHALL\s+BE\s+PERFORMED\s+ACCORDING\s+TO\s+THE\s+VENTILATION|VENTILATION\s+(?:SYSTEM\s+)?(?:FLOW\s+)?TEST')):
            tt['ventilation_flow'] = True
        if any(True for _ in self.each(r'AIR\s+LEAKAGE\s+TEST|BLOWER\s+DOOR')):
            tt['blower_door'] = True

    # --------------------------------------------------------------- what it all says the system is
    def decide(self):
        s = self.out['system']
        votes = []
        for c in self.out['credits']:
            if c.get('system'):
                votes.append((c['system'], f"option {c['option']} ({c['year']}): {c.get('meaning', '')}", 3))
        # a bare description only votes when no SELECTED option named the system: a WSU form prints every
        # option's description (Semiahmoo's carries 'ductless', 'furnace' and 'air-to-water' it never chose)
        mentioned = []
        for rx, kind in DESC_SYSTEM:
            for pno, t, m in self.each(rx):
                pre = t[max(0, m.start() - 60):m.start()]
                if '\u2610' in pre:
                    continue
                mentioned.append((kind, f'p{pno}: "{quote(t, m.start(), m.end(), 30)}"', 1))
        if not votes:
            votes += mentioned
        else:
            self.out['system']['mentioned'] = sorted({k for k, _, _ in mentioned})
        eq = self.out['equipment']
        kinds = Counter(e['kind'] for e in eq)
        if kinds.get('multizone_outdoor'):
            votes.append(('multizone', 'a multi-zone outdoor unit on a cut sheet: ' + ', '.join(e['model'] for e in eq if e['kind'] == 'multizone_outdoor'), 2))
        if kinds.get('air_handler') or kinds.get('central_outdoor'):
            votes.append(('ducted', 'an air handler / central outdoor unit on a cut sheet', 2))
        if kinds.get('wall_head') and not kinds.get('air_handler'):
            votes.append(('ductless', 'wall-mounted indoor units on a cut sheet', 2))
        score = Counter()
        for k, why, w in votes:
            score[k] += w
        s['votes'] = [dict(kind=k, why=why, weight=w) for k, why, w in votes]
        if not score:
            s['kind'] = 'unknown'
            s['why'] = ('no credit option, heat-source line or cut sheet names the heating system'
                        + (' - the set has NO text layer (scanned): OCR it or read the energy sheet by eye' if self.text_chars < 200 else
                           ' - the credit table may be drawn as linework: render the energy sheet and LOOK'))
            return
        best = score.most_common()
        s['kind'] = best[0][0]
        s['why'] = '; '.join(v['why'] for v in s['votes'] if v['kind'] == s['kind'])[:500]
        if score.get('multizone') and score.get('ducted'):
            s['kind'] = 'ducted_multizone'
            s['why'] = ('a CENTRALLY DUCTED credit AND a multi-zone outdoor unit on a cut sheet: the credit is only earned if the indoor '
                        'units are ducted (an air handler or ducted indoor units per floor), not wall heads - '
                        + '; '.join(v['why'] for v in s['votes'] if v['kind'] in ('ducted', 'multizone')))[:600]
        elif s['kind'] == 'multizone':
            s['kind'] = 'ductless'
            s['why'] = 'a multi-zone outdoor unit and no ducted credit: wall heads (ductless) unless the plans name ducted indoor units - ' + s['why']
        if len([k for k in score if k not in ('multizone',)]) > 1:
            self.out['conflicts'].append(dict(what='the set points at more than one system: ' + ', '.join(f'{k} ({v})' for k, v in best),
                                              use=s['kind'], why='the credit option outranks a description; a cut sheet outranks both only when it names the indoor units'))

    def cross_checks(self):
        v = self.out['ventilation']
        hr = [c for c in self.out['credits'] if c.get('vent') == 'hrv']
        if hr and v.get('kind') == 'exhaust':
            self.out['conflicts'].append(dict(what=f"credit {hr[0]['option']} needs a whole-house ventilation system WITH heat recovery, but the plan shows only an exhaust / whole-house fan",
                                              use='hrv', why='the credit is the permit; an exhaust-only fan cannot earn it'))
        if hr and v.get('both'):
            self.out['conflicts'].append(dict(what=f"credit {hr[0]['option']} (heat-recovery ventilation) AND a whole-house exhaust fan are both on the set",
                                              use='hrv', why='if the ERV/HRV is the whole-house system the fan is local exhaust only; if the fan is the whole-house system the credit fails - ask the designer'))
        ach = self.out['envelope'].get('ach50_value')
        for c in self.out['credits']:
            if c.get('ach50') and ach and abs(c['ach50'] - ach) > 0.05:
                self.out['conflicts'].append(dict(what=f"credit {c['option']} sets {c['ach50']} ACH50 but the notes print {ach}", use=min(c['ach50'], ach),
                                                  why='the tighter target governs the blower-door test and the infiltration load'))
        hood = self.out['hood']
        if hood.get('cfm') and hood['cfm'] > 400 and not hood.get('makeup_air'):
            self.out['conflicts'].append(dict(what=f"a {hood['cfm']:.0f} cfm range hood with no make-up air called out next to it", use='makeup air',
                                              why='IRC M1503.6: a hood over 400 cfm needs make-up air (motorised damper interlocked with the hood)'))
        if self.text_chars < 200:
            self.out['warnings'].append('the PDF has no text layer - every finding below is empty for that reason, not because the set is silent. OCR it (rapidocr) or read the sheets by eye.')

    def run(self):
        self.code(); self.credits(); self.equipment(); self.ventilation(); self.fans(); self.appliances()
        self.envelope(); self.areas(); self.openings(); self.tests(); self.decide(); self.cross_checks()
        self.out['text_chars'] = self.text_chars
        self.out['pages'] = len(self.pages)
        return self.out


def energy_pages(o):
    ps = Counter()
    for c in o['credits']:
        if c.get('page'):
            ps[c['page']] += 1
    if o['code'].get('credits_page'):
        ps[o['code']['credits_page']] += 1
    return [p for p, _ in ps.most_common(3)]


def render(pdf, pages, pattern, zoom=1.5):
    import fitz
    doc = fitz.open(pdf)
    out = []
    for p in pages:
        pix = doc[p - 1].get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        fn = pattern.replace('{N}', str(p))
        pix.save(fn)
        out.append(fn)
    return out


def summary(o):
    L = []
    c = o['code']
    L.append(f"WSEC {c.get('wsec', '?')} · {c.get('dwelling', '?')} dwelling · {c.get('credits_required', '?')} credits required · {o['pages']} page(s), {o['text_chars']:,} text chars")
    for r in o['credits']:
        L.append(f"  option {r['option']:5s} p{r.get('page')}  {r.get('credits', '')!s:4s} {r.get('meaning', '')[:90]}  [{', '.join(r['how'])}]")
    s = o['system']
    L.append(f"system: {s.get('kind')} - {s.get('why', '')[:160]}")
    for e in o['equipment']:
        L.append(f"  equipment {e['maker']} {e['model']} ({e['kind']}, {e['kbtuh_nominal']} kBtuh) p{e['pages']}")
    v = o['ventilation']
    L.append(f"ventilation: {v.get('kind')} {[m['model'] for m in v.get('models', [])]} whf={[w['cfm'] for w in v.get('whf', [])]} sre>={v.get('sre_required')}")
    h = o['hood']
    if h:
        L.append(f"hood: {h.get('cfm')} cfm, make-up air {'on the sheet' if h.get('makeup_air') else 'NOT called out'}")
    fp = o['fireplace']
    if fp.get('present'):
        L.append(f"fireplace: {fp.get('fuel')} ({len(fp.get('callouts', []))} call-outs)")
    e = o['envelope']
    L.append('envelope: ' + ', '.join(f"{k[:-6]} {e[k]}" for k in e if k.endswith('_value')))
    L.append('areas: ' + ', '.join(f"{k} {v:g}" for k, v in o['areas'].items() if not k.endswith('_page')))
    op = o.get('openings') or {}
    if op.get('rows'):
        L.append(f"openings read: {op['count']} windows / patio doors = {op['window_sf']:g} sf windows + {op['patio_sf']:g} sf patio"
                 + (f" (+{op['uncertain_sf']:g} sf unclassified)" if op.get('uncertain_sf') else '') + (f", mean U {op['u_mean']}" if op.get('u_mean') else ''))
    for x in o['conflicts']:
        L.append(f"CONFLICT: {x['what']} -> {x['use']} ({x['why'][:100]})")
    for w in o['warnings']:
        L.append(f"warning: {w}")
    return '\n'.join(L)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf', nargs='?'); ap.add_argument('--text', default=None); ap.add_argument('--out', default=None)
    ap.add_argument('--png', default=None, help='render the energy sheet(s): pattern with {N}, e.g. energy_p{N}.png')
    a = ap.parse_args()
    if not a.pdf and not a.text:
        sys.exit('give plans.pdf or --text plans.txt')
    pages = pages_of(text=open(a.text, encoding='utf-8', errors='replace').read()) if a.text else pages_of(pdf=a.pdf)
    o = Scan(pages).run()
    o['source'] = dict(kind='text' if a.text else 'pdf', file=os.path.basename(a.text or a.pdf))
    if a.png and a.pdf and not a.text:
        ps = energy_pages(o)
        o['renders'] = render(a.pdf, ps, a.png) if ps else []
        if not ps:
            o['warnings'].append('no page carries a credit option - render the cover / energy sheet by hand and LOOK')
    out = a.out or 'hvac_scan.json'
    json.dump(o, open(out, 'w', encoding='utf-8'), indent=1, default=list)
    print(summary(o))
    print('->', out)
