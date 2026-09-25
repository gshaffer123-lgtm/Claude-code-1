#!/usr/bin/env python3
r"""hvac_parts.py - the residential HVAC parts catalog in the app's takeoff shape, plus the design tables the
engine sizes from.

    python hvac_parts.py --json    > ../references/hvac_parts.json     # the data, for any consumer
    python hvac_parts.py --js      > ../references/hvac_parts.js       # drop-in module for public/js/takeoff/
    python hvac_parts.py --catalog > ../references/hvac_catalog_rows.js  # rows for the app's catalog.js
    python hvac_parts.py --table                                       # read it

SINGLE SOURCE OF TRUTH. `hvac_load.py`, `hvackit.py`, `hvac_model.py`, `hvac_bid.py`, `hvac_pdf.py` all import
from here. Shape follows `public/js/takeoff/parts.js` (the plumbing and electrical catalogs do the same):

    kind   'line'  billed by the linear foot   (line set, duct, flex, condensate, exhaust pipe, line-hide)
           'point' billed by the each          (equipment, heads, registers, caps, dampers, tests, pads)
    id     stable key
    cat    the CATALOG label the live price list is matched on (/api/pricing). PRICES ARE NOT HERE.
    phase  'equip' | 'rough' | 'vent' | 'trim' | 'test' - the bid section the line lands in
    site   install minutes per unit, CREW duration (installer + helper). PLACEHOLDERS: the market research found
           no task-level install hours (references/research-hvac-market.md 3.3 - every row 'price to set'); these
           are set so a single-zone lands in the sourced 3-8 h band and a ducted 2,500 sf house near a week of
           rough-in. Replace them with a sub's numbers or Genaro's crew
    allowance / option  True = passed through / priced only when the client ticks it

Every design number carries the section of references/ that sources it.
"""
import json, math, sys

# Tags carried from the research digests: [V] read from the source, [S] search extract of the named document,
# [C] computed here from a [V] formula, [U] trade literature not fetched - check the submittal before it is relied on.

# ================================================================== DESIGN CONDITIONS          (loads 1; code 7)
INDOOR_HEAT_F = 70.0          # MJ8 and the WSU sizing sheet design to 70 F [V]; WSEC R302.1 allows up to 72 F
INDOOR_COOL_F = 75.0          # MJ8 cooling indoor design [V]
# The WSEC permit path takes the outdoor design temperature from Appendix RC, Table RC-1 (WAC 51-11R-60100, R302.2);
# Manual J's own Table 1A uses the 99 % value and says to use it "unless superseded by code" - in WA the code
# supersedes it. What was found (loads 1):
#   Table RC-1: Bellingham 19 F heating / 78 F cooling [S]. No other row was reachable (code 7: NOT FOUND).
#   MJ8 Table 1A (ACCA Outdoor Design Conditions, v2.0) [V], the WA stations near the work:
STATIONS = {   # heating 99 %, cooling 1 % dry bulb / coincident wet bulb, design grains at 50 % RH, daily range, elevation ft
    'Bellingham IAP':        dict(mj8_heat=23, mj8_cool=76, wb=64, grains=4, range='M', elev=151),
    'Arlington Municipal AP': dict(mj8_heat=25, mj8_cool=79, wb=64, grains=1, range='M', elev=138),
    'Everett, Paine AFB':    dict(mj8_heat=25, mj8_cool=76, wb=64, grains=6, range='M', elev=596),
    'Whidbey Island NAS':    dict(mj8_heat=27, mj8_cool=70, wb=61, grains=-1, range='L', elev=46),
    'Friday Harbor AP':      dict(mj8_heat=30, mj8_cool=75, wb=62, grains=-4, range='M', elev=108),
    'Seattle-Tacoma IAP':    dict(mj8_heat=29, mj8_cool=81, wb=64, grains=-5, range='M', elev=433),
}
RC1 = {'Bellingham IAP': (19, 78)}    # the Table RC-1 rows actually read [S]
RC1_OFFSET = (-4, +2)                 # Bellingham's RC-1 sits 4 F under its MJ8 99 % heating and 2 F over its 1 % cooling:
                                      # a STAND-IN for the towns whose RC-1 row was not read - flagged on every job that uses it


def _town(station, why):
    s = STATIONS[station]
    if station in RC1:
        h, c = RC1[station]
        src = f'WSEC Table RC-1 {station} {h} F / {c} F [S]; MJ8 Table 1A {s["mj8_heat"]} F / {s["mj8_cool"]} F [V]'
    else:
        h, c = s['mj8_heat'] + RC1_OFFSET[0], s['mj8_cool'] + RC1_OFFSET[1]
        src = f'STAND-IN: MJ8 Table 1A {station} {s["mj8_heat"]} F / {s["mj8_cool"]} F [V] shifted by Bellingham\'s RC-1 gap ({RC1_OFFSET[0]:+d} / {RC1_OFFSET[1]:+d} F) - pull Table RC-1'
    return dict(heat=h, cool=c, wb=s['wb'], grains=max(0, s['grains']), range={'L': 12, 'M': 20, 'H': 28}[s['range']],
                mj8_heat=s['mj8_heat'], mj8_cool=s['mj8_cool'], station=station, src=src + (f' ({why})' if why else ''))


DESIGN = {
    'bellingham':    _town('Bellingham IAP', ''),
    'sudden valley': _town('Bellingham IAP', 'Sudden Valley is ~8 mi from the airport, 300-700 ft up - STAND-IN on the Bellingham row'),
    'glenhaven':     _town('Bellingham IAP', 'Glenhaven Lakes, Whatcom Co. foothills - STAND-IN on the Bellingham row'),
    'sedro-woolley': _town('Bellingham IAP', 'Skagit foothills: the Bellingham row is the colder neighbour - STAND-IN'),
    'ferndale':      _town('Bellingham IAP', 'STAND-IN on the Bellingham row'),
    'blaine':        _town('Bellingham IAP', 'Fraser outflow country - STAND-IN on the Bellingham row'),
    'lynden':        _town('Bellingham IAP', 'Fraser outflow country, likely colder than the airport - STAND-IN'),
    'mount vernon':  _town('Arlington Municipal AP', 'the nearest Table 1A station'),
    'burlington':    _town('Arlington Municipal AP', 'the nearest Table 1A station'),
    'anacortes':     _town('Whidbey Island NAS', 'the nearest Table 1A station'),
    'friday harbor': _town('Friday Harbor AP', ''),
    'shaw island':   _town('Friday Harbor AP', 'Shaw is 3 mi from the Friday Harbor station'),
    'orcas':         _town('Friday Harbor AP', 'the nearest Table 1A station'),
    'lopez':         _town('Friday Harbor AP', 'the nearest Table 1A station'),
    'everett':       _town('Everett, Paine AFB', ''),
    'seattle':       _town('Seattle-Tacoma IAP', 'the WSU sheet reportedly uses dT 46 = 70 - 24 (unverified)'),
}
for _k, _v in DESIGN.items():
    _v['stand_in'] = _v['src'].startswith('STAND-IN') or 'STAND-IN' in _v['src']

# ================================================================== ENVELOPE                    (code 4; loads 2-3)
# 2021 WSEC-R prescriptive U-factor alternative (Table R402.1.3), marine WA. The plan's own R-values override
# through R_TO_U below; these are what the load uses when the set is silent.
U_DEFAULT = dict(ceiling=0.024, vault=0.026, wall=0.056, floor=0.029, below_grade=0.042, window=0.28, skylight=0.50, door=0.20,
                 slab_f=0.54)
# assembly U-factor for the R-labels plans print (wood frame, framing fraction included) - WSEC Chapter 10 /
# Appendix A default-table class, rounded to 3 places (code 4)
R_TO_U = {
    'ceiling': {30: 0.035, 38: 0.030, 49: 0.026, 60: 0.024, 70: 0.021},
    'vault':   {30: 0.036, 38: 0.028, 49: 0.026},
    'wall':    {'R-13': 0.089, 'R-15': 0.082, 'R-19': 0.063, 'R-21': 0.056, 'R-13+5': 0.064, 'R-13+10': 0.044,
                'R-20+5': 0.044, 'R-21+5': 0.043, 'R-21+7.5': 0.039, 'R-21+10': 0.035, 'R-21+12': 0.033, 'R-21+15': 0.030},
    'floor':   {19: 0.047, 25: 0.036, 30: 0.033, 38: 0.029, 49: 0.024},
}
GAP_CLOSE_FT = 2.5            # a gap under 2 x 2.5 ft between traced rooms (an untraced stair, a chase) is inside the house
ACH50_DEFAULT = 5.0           # 2021 WSEC-R R402.4.1.2 maximum when the set names no tighter target (code 4)
AIR_SENS = 1.1                # Btuh per cfm per F (MJ8, x altitude factor ~1 at the coast) [V] (loads 3.4)
AIR_LAT = 0.68                # Btuh per cfm per grain [V]
# Design infiltration, MJ8 blower-door method (the LBL model as NREL's MJ8 code implements it) [V] (loads 3.4):
#   ICFM = 0.05488 x Q50 x sqrt(0.015 x storeys x dT + Cw x wind^2),  Q50 = ACH50 x volume / 60
#   Cw = (0.0065 - 0.00266 x (shielding - 3)) x storeys^0.4, shielding class 4 (default), 15 mph heating / 7.5 mph cooling
# In Bellingham that is ACH50 / 14.5 (1 storey), / 11.4 (2), / 9.8 (3) at design [C] - not the seasonal LBL N-factor.
ELA_K = 0.05488
SHIELDING = 4
WIND_HEAT_MPH, WIND_COOL_MPH = 15.0, 7.5

def icfm(ach50, volume, storeys, dT, wind, shielding=SHIELDING):
    cs = 0.015 * storeys
    cw = (0.0065 - 0.00266 * (shielding - 3)) * storeys ** 0.4
    return ELA_K * ach50 * volume / 60.0 * math.sqrt(max(0.0, cs * dT + cw * wind * wind))

# a floor over a VENTED crawl sees a partition temperature difference, not the full dT: MJ8 Figure A12-6
# PTDH = dT / (1 + 4 Uf / (Uw + 0.11)) = 0.76 x dT for an R-38 floor and uninsulated crawl walls [C from V] (loads 3.2, 10.1)
CRAWL_PTD = 0.76
# duct loss outside the envelope, fraction of the room load. MJ8 Table 7 needs duct R and leakage the set rarely
# gives; the WSU sizing sheet screens it at x 1.10 for ducts in unconditioned space [S] (loads 2, 3.6)
DUCT_LOSS = {'inside': 0.00, 'crawl_conditioned': 0.00, 'crawl_vented': 0.10, 'attic': 0.15, 'garage': 0.10}

# cooling - MJ8 heat-transfer multipliers at 48.8 N (loads 4)
# glass: solar part PSF x CLF x SHGC / 0.87, SHGC 0.28, NO internal shading (the 'peak' procedure MJ8 asks for on
# zoned / ductless systems - default drapes would take ~30 % off) [C]; conduction U x dTc is added separately
GLF_SHGC_REF = 0.28
GLF = {'N': 5.0, 'NE': 16.0, 'E': 26.0, 'SE': 23.0, 'S': 14.0, 'SW': 23.0, 'W': 26.0, 'NW': 16.0, 'H': 48.0}
# opaque surfaces: cooling temperature difference = max(0, dTc + offset), medium colour, medium daily range [V]/[C]
#   wall: group C-D CLTD 17.6 - 20 -> dTc - 2.4 (walls are ~0 in Bellingham); ceiling under a vented attic, dark
#   shingles: T_attic = T_out + 35; vaulted R-38+: 27 - 95 + T_out -> dTc + 7; door: dTc + 11
CLTD_OFFSET = dict(wall=-2.4, ceiling=35.0, vault=7.0, door=11.0)
PEOPLE_SENS, PEOPLE_LAT = 230.0, 200.0   # per occupant, occupants = bedrooms + 1 [V]
APPLIANCE_SENS = 2400.0                  # NREL's 'per Manual J' default with one refrigerator [V]: 1,200 in the kitchen,
APPLIANCE_KITCHEN = 1200.0               # the rest spread over the living spaces (the older 1,200 is MJ8's earlier text [U])

# checker bands for a new WSEC-2021 house (loads 10.2) [C]
BAND_HEAT_PER_SF = (5.0, 18.0)           # Manual J heating Btuh / sf CFA: expected 7-12, flag outside 5-18
BAND_COOL_PER_SF = (2.5, 8.0)            # expected 3.5-5.5
BAND_COOL_OVER_HEAT = (0.25, 0.80)       # expected 0.40-0.55
WSU_ACH, WSU_AIR = 0.6, 0.018            # WSU 'Simple Heating System Size' sheet: dT x (UA + 0.018 x 0.6 ACH x volume) [S]
WSU_DUCT_UNCOND = 1.10                   # x 1.10 when ducts are in unconditioned space [S]
WSU_MAX_HP = 1.25                        # the sheet's maximum heat-pump output = 1.25 x its load [S]

# ================================================================== EQUIPMENT                  (loads 5, 6)
HEAD_SIZES = [6, 9, 12, 15, 18, 24]       # kBtuh nominal, wall-mounted indoor units [U]
MZ_SIZES = [18, 24, 30, 36, 42, 48, 60]   # multi-zone outdoor nominal kBtuh [U]
MZ_MAX_HEADS = {18: 2, 24: 3, 30: 4, 36: 5, 42: 5, 48: 8, 60: 8}   # ports (48 / 60 with branch boxes) [U]
MZ_CONNECT_MAX = 1.30                     # connected indoor nominal up to ~130 % of the outdoor nominal [U]
CENTRAL_SIZES = [24, 30, 36, 42, 48, 60]  # ducted heat pump nominal kBtuh (2 - 5 ton)
DUCTED_INDOOR_SIZES = [9, 12, 18, 24, 36] # slim / mid-static ducted indoor units for a multi-zone [U]
# maximum heating capacity as a fraction of NOMINAL, NREL ResStock typical cold-climate heat pumps [V] (loads 5.4):
# never size on nominal. A ductless cc unit keeps ~0.93 of nominal at 19 F, a ducted one ~0.78.
CAP_MAX = {'ductless': [(47, 1.216), (17, 0.913), (5, 0.867), (-15, 0.630)],
           'ducted':   [(47, 1.028), (17, 0.766), (5, 0.688), (-15, 0.507)]}
CAP_MIN = {'ductless': [(47, 0.300), (17, 0.203), (5, 0.167)],        # minimum-compressor output, same source [V]
           'ducted':   [(47, 0.308), (17, 0.353), (5, 0.371)]}
# Manual S 2023 (ACCA addendum c draft, 3/2025) variable-capacity heat pump: capacity at design >= 1.00 x heating
# load, minimum-compressor output <= 0.80 x load; cooling total <= 1.30 x on the simplified path, no cap on the
# advanced path (heating governs here). WA M1401.3 exempts multistage / VRF sizing within the maker's range [V] (loads 5)
HSF_MIN, MIN_COMP_MAX = 1.00, 0.80
HSF_ACCEPT = 0.95        # a unit within 5 % of the load at design is taken - inside a Manual J's accuracy, and the
                         # 5 kW strip Manual S allows for a shortfall under 15,000 Btuh carries the rest
CFM_PER_TON_DESIGN = 375.0   # blower airflow per ton of capacity AT THE DESIGN POINT (350-400 band) - ducts are
                             # sized for what the coil moves at design, not the nameplate tons (loads 7.1)
SAT_HP, LAT_COOL = 105.0, 55.0   # heat-pump supply air / cooling leaving air, F - the airflow floor (loads 4.5)
COOL_SF_MAX_SIMPLE = 1.30
SUPP_SMALL_BTUH, SUPP_SMALL_KW = 15000.0, 5.0     # supplemental load <= 15 kBtuh: heater <= 5 kW; above: 0.95-1.75 x [V]
HEAD_MIN_LOAD = 1500                      # Btuh: a room below this is served from the zone next door, not given a head
HABITABLE_MIN_SF = 70.0                   # IRC R304.1: a habitable room is >= 70 sf - a smaller 'bedroom' is a tracer fragment
ZONE_OPEN_USES = {'living', 'kitchen', 'dining', 'circulation', 'stair', 'office', 'den', 'media'}
NO_HEAD_USES = {'closet', 'pantry', 'utility', 'storage', 'linen', 'bath', 'powder', 'garage', 'mech', 'laundry'}

# line set by indoor capacity (liquid x suction, in) [U] (loads 6.3)
def line_set(kbtuh):
    if kbtuh <= 12:
        return (0.25, 0.375)
    if kbtuh <= 18:
        return (0.25, 0.5)
    if kbtuh <= 36:
        return (0.375, 0.625)
    return (0.375, 0.75)
LS_PRECHARGE_FT = {'single': 25.0, 'multi_per_head': 25.0, 'central': 25.0}   # factory charge covers this much [U]
LS_ADD_OZ_PER_FT = {0.25: 0.22, 0.375: 0.54}                                  # extra charge by liquid size [U]
# maximum piping by class [U] (loads 6.4): single-zone 6-12k 65 ft / 40 ft lift, 15-24k 100 ft / 50 ft;
# multi-zone about 82 ft a branch and 98-262 ft in total by model, 49 ft lift; minimum ~10 ft
LS_MAX_FT = {'single_small': 65.0, 'single': 100.0, 'multi_branch': 82.0, 'central': 150.0}
LS_MZ_TOTAL_FT = {18: 164.0, 24: 164.0, 30: 229.0, 36: 229.0, 42: 262.0, 48: 262.0, 60: 262.0}
LS_MAX_LIFT_FT = {'single': 50.0, 'multi': 49.0, 'central': 100.0}
LS_MIN_FT = 10.0

# the electrical nameplate the electrician has to wire (minimum circuit ampacity class, 240 V) [U] - the
# cross-trade check against electrical/jobs/<h>/devices.json; the nameplate MCA / MOCP wins
BREAKER_A = {('single', 9): 15, ('single', 12): 15, ('single', 15): 20, ('single', 18): 20, ('single', 24): 25,
             ('multi', 18): 20, ('multi', 24): 25, ('multi', 30): 25, ('multi', 36): 30, ('multi', 42): 35, ('multi', 48): 40, ('multi', 60): 50,
             ('central', 24): 20, ('central', 30): 25, ('central', 36): 30, ('central', 42): 35, ('central', 48): 40, ('central', 60): 50}
STRIP_BREAKER_A = {5: 30, 8: 45, 10: 60, 15: 90}    # air handler with its strip (blower included) [U]

# ducts (loads 7) - round duct at 0.08 in.w.c. / 100 ft, galvanized, Darcy-Colebrook [C]; flex = rigid x 0.85 [C]
ROUND_CFM = {4: 33, 5: 60, 6: 98, 7: 148, 8: 212, 9: 291, 10: 386, 12: 628, 14: 947, 16: 1351, 18: 1850}
FLEX_DERATE = 0.85
CFM_PER_TON = 400.0                       # rated airflow (RESNET) [V]; design band 350-450
REG_MAX_CFM = {'floor_4x10': 90, 'floor_4x12': 110, 'ceiling_6x10': 130}   # ~500-600 fpm through ~0.6 free area [C/U]
RETURN_GRILLES = [('14x20', 583), ('16x20', 667), ('20x20', 833), ('20x25', 1042), ('20x30', 1250)]   # cfm at 300 fpm face [C]
TRANSFER_IN2_PER_CFM = 0.55               # free area for a closed bedroom at 3 Pa [C] (loads 7.9)
TRUNK_MAX_FT = 24.0                       # a non-reducing extended plenum past ~20-24 ft reduces or splits [U]

def round_for(cfm, flex=True):
    cap = FLEX_DERATE if flex else 1.0
    for d in sorted(ROUND_CFM):
        if ROUND_CFM[d] * cap >= cfm:
            return d
    return 18

def return_grille(cfm):
    for name, c in RETURN_GRILLES:
        if c >= cfm:
            return name
    return RETURN_GRILLES[-1][0]

# ventilation - WA IRC 2021 as amended (WAC 51-51-1505) [V] (loads 8.1; code 5.8)
#   Qr = 0.01 x CFA + 7.5 x (bedrooms + 1), not less than 30 cfm         (Equation 15-1)
#   Qv = Qr x Csystem                                                    (Equation 15-2, Table M1505.4.3(2))
CSYSTEM = {('balanced', True): 1.0, ('balanced', False): 1.25, ('unbalanced', True): 1.25, ('unbalanced', False): 1.5}

def vent_rate(cfa_sf, bedrooms, balanced=False, distributed=False):
    qr = max(30.0, 0.01 * cfa_sf + 7.5 * (bedrooms + 1))
    c = CSYSTEM[('balanced' if balanced else 'unbalanced', bool(distributed))]
    return qr, c, qr * c
LOCAL_EXHAUST = dict(bath_int=50, bath_cont=20, hood_electric=160, hood_gas=250)   # Table M1505.4.4.1 [V]
HOOD_MUA_CFM = 400        # WA M1503.6: make-up air over 400 cfm ONLY where a fuel appliance that is neither direct-vent
                          # nor mechanical-draft sits inside the air barrier [V] - an all-electric house does not trigger it
DRYER_MAX_EQ_FT = 35.0    # M1502.4.6.1: 35 ft less the fittings [V]
DRYER_90_FT, DRYER_45_FT = 5.0, 2.5       # 4 in-radius mitered elbows (smooth 6 in-radius: 1.75 / 1.0) [V]
# local exhaust duct, WA Table M1505.4.4.2 (fan rated at 0.25 in.w.c.), max length ft with <= 3 elbows, 10 ft less
# per extra elbow; None = not allowed, 1e9 = no limit [V] (loads 9.1)
BATH_DUCT = {(50, 'flex', 4): 25, (50, 'smooth', 4): 70, (50, 'flex', 5): 90, (50, 'smooth', 5): 100, (50, 'flex', 6): 1e9, (50, 'smooth', 6): 1e9,
             (80, 'flex', 4): None, (80, 'smooth', 4): 20, (80, 'flex', 5): 15, (80, 'smooth', 5): 100, (80, 'flex', 6): 90, (80, 'smooth', 6): 1e9,
             (100, 'flex', 5): None, (100, 'smooth', 5): 50, (100, 'flex', 6): 45, (100, 'smooth', 6): 1e9,
             (125, 'flex', 6): 15, (125, 'smooth', 6): 1e9, (125, 'flex', 7): 70, (125, 'smooth', 7): 1e9}

def bath_duct(cfm, ft, elbows=2):
    """the duct a local-exhaust fan of `cfm` needs over `ft` (Table M1505.4.4.2): insulated flex first (what goes in
    an attic or joist bay), else smooth rigid. Returns (dia_in, 'flex' | 'smooth', limit_ft)"""
    rated = next((c for c in (50, 80, 100, 125) if c >= cfm - 0.1), 125)
    eff = ft + max(0, elbows - 3) * 10.0
    for kind in ('flex', 'smooth'):
        for d in (4, 5, 6):
            lim = BATH_DUCT.get((rated, kind, d))
            if lim is not None and eff <= lim:
                return d, kind, lim
    return 7, 'flex', BATH_DUCT.get((125, 'flex', 7))
HOOD_DUCT_IN = [(300, 6), (400, 7), (600, 8), (1200, 10)]   # maker norms [U]; physics check 6 in ~190 cfm, 8 in ~360 at 40 ft eq [C]

def hood_duct(cfm):
    for c, d in HOOD_DUCT_IN:
        if cfm <= c:
            return d
    return 12

# ================================================================== THE CATALOG
def _eq(kind, n, label, cat, site, note='', **kw):
    return dict(id=f'{kind}_{n:02d}', kind='point', group='Equipment', label=label, cat=cat, phase='equip', site=site, note=note, kbtuh=n, **kw)

PARTS = []
for n in [9, 12, 15, 18, 24]:
    PARTS.append(_eq('eq_ds', n, f'Ductless outdoor unit - single-zone {n}k, cold-climate (NEEP-listed), R-454B/R-32',
                     f'Ductless outdoor unit {n}k single-zone', 150, 'matched to one wall head; pad or bracket, line set and whip separate'))
for n in MZ_SIZES:
    PARTS.append(_eq('eq_mz', n, f'Multi-zone outdoor unit - {n}k, cold-climate, up to {MZ_MAX_HEADS[n]} indoor units',
                     f'Multi-zone outdoor unit {n}k', 210, 'branch box where the maker needs one for the port count'))
for n in HEAD_SIZES:
    PARTS.append(_eq('eq_head', n, f'Ductless wall head {n}k', f'Ductless wall head {n}k', 150,
                     'mount plate on blocking, line-set / drain / comm through a 3 in sleeve, wireless remote included'))
for n in [9, 12, 18, 24, 36]:
    PARTS.append(_eq('eq_duin', n, f'Ducted indoor unit (slim / multi-position) {n}k', f'Ducted indoor unit {n}k', 240,
                     'short-run duct system on its own storey; return filter box'))
for n in CENTRAL_SIZES:
    PARTS.append(_eq('eq_hp', n, f'Heat pump outdoor unit - centrally ducted {n}k ({n / 12:g} ton), cold-climate variable capacity',
                     f'Heat pump outdoor unit {n}k ducted', 240, 'NEEP cc-VCHP where design temp <= 23 F (WSEC 3.6 note)'))
    PARTS.append(_eq('eq_ahu', n, f'Air handler - variable speed, {n}k ({n / 12:g} ton)', f'Air handler {n}k', 300,
                     'multi-position; filter rack; secondary pan where above finished space'))
PARTS += [
    dict(id='eq_strip_05', kind='point', group='Equipment', label='Backup heat strip 5 kW (controlled per WSEC R403.1.2)', cat='Heat strip 5 kW', phase='equip', site=40),
    dict(id='eq_strip_08', kind='point', group='Equipment', label='Backup heat strip 8 kW', cat='Heat strip 8 kW', phase='equip', site=40),
    dict(id='eq_strip_10', kind='point', group='Equipment', label='Backup heat strip 10 kW', cat='Heat strip 10 kW', phase='equip', site=45),
    dict(id='eq_strip_15', kind='point', group='Equipment', label='Backup heat strip 15 kW', cat='Heat strip 15 kW', phase='equip', site=45),
    dict(id='eq_erv_s', kind='point', group='Equipment', label='ERV / HRV - balanced whole-house, 50-150 cfm (SRE per the credit)', cat='ERV whole-house 150 cfm', phase='equip', site=300,
         note='hung in the mechanical room / attic-free location; condensate for an HRV'),
    dict(id='eq_erv_m', kind='point', group='Equipment', label='ERV / HRV - balanced whole-house, 150-250 cfm', cat='ERV whole-house 250 cfm', phase='equip', site=330),
    dict(id='eq_tstat', kind='point', group='Equipment', label='Thermostat - programmable, heat pump with aux-heat lockout (WSEC R403.1.1 / R403.1.2)', cat='Thermostat heat pump programmable', phase='equip', site=45),
    dict(id='eq_zone_ctrl', kind='point', group='Equipment', label='Wired wall controller per ductless zone (optional)', cat='Ductless wired controller', phase='equip', site=30, option=True,
         note='each head ships with a wireless remote; a wall controller is the upgrade'),
    dict(id='eq_bath_heater', kind='point', group='Equipment', label='Supplemental bath heater <= 500 W (WSEC resistance allowance)', cat='Bath heater 500 W', phase='equip', site=60, option=True,
         note='WSEC allows resistance heat up to 0.5 W/sf or 500 W; the electrician wires it'),

    # -------------------------------------------------- REFRIGERANT PIPING                     (loads 5)
    dict(id='rp_ls_1438', kind='line', group='Refrigerant piping', label='Line set 1/4 x 3/8 insulated (pre-flared or brazed)', cat='Line set 1/4 x 3/8', phase='rough', site=2.0, waste=0.10, coil=50),
    dict(id='rp_ls_1412', kind='line', group='Refrigerant piping', label='Line set 1/4 x 1/2 insulated', cat='Line set 1/4 x 1/2', phase='rough', site=2.0, waste=0.10, coil=50),
    dict(id='rp_ls_3858', kind='line', group='Refrigerant piping', label='Line set 3/8 x 5/8 insulated', cat='Line set 3/8 x 5/8', phase='rough', site=2.5, waste=0.10, coil=50),
    dict(id='rp_ls_3834', kind='line', group='Refrigerant piping', label='Line set 3/8 x 3/4 insulated', cat='Line set 3/8 x 3/4', phase='rough', site=2.5, waste=0.10, coil=50),
    dict(id='rp_comm', kind='line', group='Refrigerant piping', label='Communication cable 14/4 stranded (outdoor unit to each indoor unit)', cat='Mini-split cable 14/4', phase='rough', site=0.2, waste=0.10, coil=250),
    dict(id='rp_linehide', kind='line', group='Refrigerant piping', label='Line-set cover 4 in (exterior, painted), per foot', cat='Line-set cover 4 in', phase='rough', site=2.0, waste=0.10, stick=8),
    dict(id='rp_lh_fit', kind='point', group='Refrigerant piping', label='Line-set cover fittings (wall inlet, elbows, coupler, end)', cat='Line-set cover fitting', phase='rough', site=5),
    dict(id='rp_sleeve', kind='point', group='Refrigerant piping', label='Wall penetration - 3 in sleeve, sealed and flashed', cat='Line-set wall penetration', phase='rough', site=30),
    dict(id='rp_nitro', kind='point', group='Refrigerant piping', label='Nitrogen pressure test + evacuation to 500 micron (per system)', cat='Pressure test and evacuation', phase='test', site=90),
    dict(id='rp_charge', kind='point', group='Refrigerant piping', label='Refrigerant - additional charge beyond the pre-charge (lb)', cat='Refrigerant additional charge (lb)', phase='test', site=0, unit='lb'),
    dict(id='rp_pad', kind='point', group='Refrigerant piping', label='Equipment pad - composite, sized to the outdoor unit', cat='Equipment pad', phase='rough', site=20),
    dict(id='rp_stand', kind='point', group='Refrigerant piping', label='Outdoor unit stand / wall bracket (snow and drainage clearance)', cat='Outdoor unit stand', phase='rough', site=45),
    dict(id='rp_vib', kind='point', group='Refrigerant piping', label='Anti-vibration pads (set of 4)', cat='Anti-vibration pads', phase='rough', site=5),

    # -------------------------------------------------- CONDENSATE                              (research-hvac-code.md 5, M1411)
    dict(id='cd_line', kind='line', group='Condensate', label='Condensate line 3/4 in PVC (or 5/8 vinyl with the line set)', cat='Condensate line 3/4 PVC', phase='rough', site=1.0, waste=0.10, stick=10),
    dict(id='cd_pump', kind='point', group='Condensate', label='Condensate mini-pump (head on an interior wall / no fall to outside)', cat='Condensate mini pump', phase='rough', site=45),
    dict(id='cd_pan', kind='point', group='Condensate', label='Secondary drain pan + float switch (M1411.3.1: equipment above finished space)', cat='Secondary pan and float switch', phase='rough', site=45),
    dict(id='cd_trap', kind='point', group='Condensate', label='Condensate trap + cleanout tee', cat='Condensate trap', phase='rough', site=15),

    # -------------------------------------------------- DUCTWORK                                (loads 6)
    dict(id='dt_plenum', kind='point', group='Ductwork', label='Supply + return plenums (fabricated, sealed, lined where required)', cat='Plenum set supply and return', phase='rough', site=120),
    dict(id='dt_trunk', kind='line', group='Ductwork', label='Supply trunk - galvanized rectangular / 10-14 in round (extended plenum)', cat='Supply trunk duct', phase='rough', site=5, waste=0.05),
    dict(id='dt_return', kind='line', group='Ductwork', label='Return duct 12-16 in (panned joist not allowed for a new return)', cat='Return duct', phase='rough', site=5, waste=0.05),
    dict(id='dt_takeoff', kind='point', group='Ductwork', label='Takeoff / starting collar with balancing damper', cat='Duct takeoff with damper', phase='rough', site=10),
    dict(id='dt_boot', kind='point', group='Ductwork', label='Register boot (4x10 / 4x12 floor or 6x10 ceiling)', cat='Register boot', phase='rough', site=12),
    dict(id='dt_hanger', kind='point', group='Ductwork', label='Duct hanger strap / saddle (flex every 4 ft, rigid every 10 ft)', cat='Duct hanger', phase='rough', site=1),
    dict(id='dt_mastic', kind='point', group='Ductwork', label='Duct mastic (gal) + UL-181 foil tape', cat='Duct mastic and tape', phase='rough', site=0),
    dict(id='dt_wrap', kind='line', group='Ductwork', label='Duct insulation R-8 wrap (rigid duct outside the envelope, WSEC R403.3.1)', cat='Duct wrap R-8', phase='rough', site=2, waste=0.10),
    dict(id='dt_transfer', kind='point', group='Ductwork', label='Transfer grille pair / jumper duct (closed-door pressure relief)', cat='Transfer grille or jumper', phase='rough', site=45),
]
for d in [4, 5, 6, 7, 8, 10, 12, 14]:
    PARTS.append(dict(id=f'dt_flex_{d:02d}', kind='line', group='Ductwork', label=f'Flex duct R-8 {d} in', cat=f'Flex duct R-8 {d} in', phase='rough',
                      site=2.0 if d <= 8 else 3.0, waste=0.05, bag=25))
PARTS += [
    # -------------------------------------------------- VENTILATION & EXHAUST                   (research-hvac-code.md 5; loads 7-8)
    dict(id='vx_bath_duct', kind='line', group='Ventilation', label='Bath fan exhaust duct 4 in insulated flex (50 cfm fan: <= 25 ft, Table M1505.4.4.2)', cat='Exhaust duct 4 in', phase='vent', site=3, waste=0.10, bag=25),
    dict(id='vx_duct6', kind='line', group='Ventilation', label='Exhaust duct 6 in insulated (80-110 cfm fans, whole-house fan: Table M1505.4.4.2)', cat='Exhaust duct 6 in', phase='vent', site=3.5, waste=0.10, bag=25),
    dict(id='vx_cap6', kind='point', group='Ventilation', label='Wall / roof cap 6 in with backdraft damper', cat='Wall cap 6 in', phase='vent', site=30),
    dict(id='vx_cap4_wall', kind='point', group='Ventilation', label='Wall cap 4 in with backdraft damper', cat='Wall cap 4 in', phase='vent', site=25),
    dict(id='vx_cap4_roof', kind='point', group='Ventilation', label='Roof jack 4 in with damper (roofer flashes it)', cat='Roof jack 4 in', phase='vent', site=30),
    dict(id='vx_dryer_pipe', kind='line', group='Ventilation', label='Dryer duct 4 in rigid metal, smooth wall (M1502.4.2)', cat='Dryer duct 4 in rigid', phase='vent', site=5, waste=0.10, stick=5),
    dict(id='vx_dryer_ell', kind='point', group='Ventilation', label='Dryer duct 4 in 90 elbow', cat='Dryer elbow 4 in', phase='vent', site=5),
    dict(id='vx_dryer_box', kind='point', group='Ventilation', label='Dryer vent box (recessed)', cat='Dryer vent box', phase='vent', site=20),
    dict(id='vx_dryer_cap', kind='point', group='Ventilation', label='Dryer wall cap with damper, no screen (M1502.3)', cat='Dryer wall cap', phase='vent', site=25),
    dict(id='vx_dryer_depv', kind='point', group='Ventilation', label='Dryer exhaust duct power ventilator (DEPV, UL 705) where the run is over 35 ft equivalent (M1502.4.6.3; booster fans are prohibited, M1502.4.5)',
         cat='Dryer exhaust duct power ventilator', phase='vent', site=90, option=True,
         note='or the dryer maker\'s longer-run table (M1502.4.6.2) - then this line comes off; the electrician wires it'),
    dict(id='vx_hood_duct', kind='line', group='Ventilation', label='Range hood duct 6-10 in rigid, sealed (M1503.3)', cat='Range hood duct rigid', phase='vent', site=6, waste=0.10, stick=5),
    dict(id='vx_hood_cap', kind='point', group='Ventilation', label='Range hood wall / roof cap with damper', cat='Range hood cap', phase='vent', site=35),
    dict(id='vx_mua', kind='point', group='Ventilation', label='Make-up air damper (motorised) + hood interlock + duct (WA M1503.6: hood > 400 cfm with a non-direct-vent fuel appliance inside)', cat='Make-up air damper kit', phase='vent', site=120,
         note='the electrician wires the interlock; the duct runs to the kitchen from an outside hood'),
    dict(id='vx_erv_duct', kind='line', group='Ventilation', label='ERV duct 5-6 in (supply to bedrooms / living, exhaust from baths / kitchen / laundry)', cat='ERV duct 6 in', phase='vent', site=2.5, waste=0.10, bag=25),
    dict(id='vx_erv_insul', kind='line', group='Ventilation', label='ERV outdoor-air / exhaust duct, insulated with vapour jacket (to the hoods)', cat='ERV insulated duct 6 in', phase='vent', site=4, waste=0.10, bag=25),
    dict(id='vx_erv_hood', kind='point', group='Ventilation', label='ERV intake / exhaust hood 6 in (intake >= 10 ft from any exhaust, R303.5 / M1505.2)', cat='ERV wall hood 6 in', phase='vent', site=35),
    dict(id='vx_erv_grille', kind='point', group='Ventilation', label='ERV supply / exhaust grille or valve 4-6 in', cat='ERV grille', phase='vent', site=15),
    dict(id='vx_whf_fan', kind='point', group='Ventilation', label='Whole-house exhaust fan, continuous duty, <= 1.0 sone (M1505.4) - replaces one electrical allowance fan', cat='Whole-house exhaust fan continuous', phase='vent', site=60),
    dict(id='vx_whf_ctrl', kind='point', group='Ventilation', label='Whole-house ventilation control - 24 h timer / override, labelled (WA M1505.4.2)', cat='Whole-house ventilation control', phase='vent', site=20),
    dict(id='vx_air_inlet', kind='point', group='Ventilation', label='Outdoor air inlet 4 sq in NFA, through-wall with screen (WA exhaust-only whole-house ventilation, one per habitable room)', cat='Outdoor air inlet', phase='vent', site=30,
         note='window trickle vents of the same net free area count instead - then this line comes off'),

    # -------------------------------------------------- SUPPORT, PROTECTION                     (R302.5, R302.11, R302.4)
    dict(id='sp_firestop', kind='point', group='Support + protection', label='Firestopped penetration (garage separation / rated assembly)', cat='Firestop penetration', phase='rough', site=10),
    dict(id='sp_plate', kind='point', group='Support + protection', label='Nail plate at a line-set / cable bore within 1-1/4 in of the face', cat='Nail plate', phase='rough', site=2),
    dict(id='sp_bore', kind='point', group='Support + protection', label='Bore through a stud / plate (counted, not priced)', cat='Framing bore', phase='rough', site=2),
    dict(id='sp_caulk', kind='point', group='Support + protection', label='Fire caulk / sealant (tube)', cat='Fire caulk', phase='rough', site=0),
    dict(id='sp_blocking', kind='point', group='Support + protection', label='Head / controller blocking (framer or HVAC)', cat='Mounting blocking', phase='rough', site=10),

    # -------------------------------------------------- REGISTERS, GRILLES (trim)
    dict(id='tr_reg_floor', kind='point', group='Registers + grilles', label='Floor register 4x10 / 4x12', cat='Floor register', phase='trim', site=8),
    dict(id='tr_reg_ceiling', kind='point', group='Registers + grilles', label='Ceiling / sidewall diffuser 6x10', cat='Ceiling diffuser', phase='trim', site=10),
    dict(id='tr_return', kind='point', group='Registers + grilles', label='Return / filter grille 20x25 (or 14x30)', cat='Return filter grille', phase='trim', site=15),
    dict(id='tr_filter', kind='point', group='Registers + grilles', label='Filters MERV 8-13 (first set)', cat='Filter', phase='trim', site=2),

    # -------------------------------------------------- COMMISSIONING, TESTS, DESIGN           (research-hvac-code.md 8)
    dict(id='cm_design', kind='point', group='Commissioning', label='Load calculation + equipment selection for the permit (Manual J / S or the WSU sizing form)', cat='HVAC design and load calc', phase='test', site=0),
    dict(id='cm_startup', kind='point', group='Commissioning', label='Start-up, charge verification, controls set-up (per outdoor unit)', cat='HVAC start-up', phase='test', site=120),
    dict(id='cm_balance', kind='point', group='Commissioning', label='Air balance of supply registers (per ducted system)', cat='Air balance', phase='test', site=90),
    dict(id='cm_duct_test', kind='point', group='Commissioning', label='Duct leakage test, total cfm25 (WSEC R403.3.5) - certified tester', cat='Duct leakage test', phase='test', site=0),
    dict(id='cm_vent_test', kind='point', group='Commissioning', label='Ventilation flow test - whole-house + local exhaust (WA M1505.4.3 / M1505.4.4)', cat='Ventilation flow test', phase='test', site=60),
    dict(id='cm_labels', kind='point', group='Commissioning', label='Equipment labels, WSEC certificate data, owner hand-over', cat='HVAC hand-over', phase='test', site=30),
]
byId = {p['id']: p for p in PARTS}


def eq_part(prefix, kbtuh, sizes):
    """the smallest catalog size >= kbtuh"""
    for n in sizes:
        if n >= kbtuh - 0.1:
            return f'{prefix}_{n:02d}', n
    n = sizes[-1]
    return f'{prefix}_{n:02d}', n


def _interp(pts, t_f):
    if t_f >= pts[0][0]:
        return pts[0][1]
    for (t1, f1), (t2, f2) in zip(pts, pts[1:]):
        if t2 <= t_f <= t1:
            return f2 + (f1 - f2) * (t_f - t2) / (t1 - t2)
    (t1, f1), (t2, f2) = pts[-2], pts[-1]                 # below the last point: extrapolate the last segment
    return max(0.0, f2 - (f1 - f2) / (t1 - t2) * (t2 - t_f))


def capacity_at(nominal_btuh, t_f, family='ductless'):
    """maximum heating output of a cold-climate variable-capacity heat pump at outdoor t_f (F): nominal x the
    ResStock curve for its family ('ductless' = mini-split heads and multi-zones, 'ducted' = unitary)"""
    return nominal_btuh * _interp(CAP_MAX[family], t_f)


def min_output_at(nominal_btuh, t_f, family='ductless'):
    """minimum-compressor heating output at t_f - the Manual S turndown check"""
    return nominal_btuh * _interp(CAP_MIN[family], t_f)


# ================================================================== emitters
def as_json():
    return json.dumps(dict(parts=PARTS, design=DESIGN, u_default=U_DEFAULT, r_to_u={k: {str(a): b for a, b in v.items()} for k, v in R_TO_U.items()},
                           head_sizes=HEAD_SIZES, mz_sizes=MZ_SIZES, central_sizes=CENTRAL_SIZES, round_cfm=ROUND_CFM,
                           cap_max=CAP_MAX, cap_min=CAP_MIN, local_exhaust=LOCAL_EXHAUST, csystem={f'{k[0]}/{"distributed" if k[1] else "not distributed"}': v for k, v in CSYSTEM.items()}), indent=1)


def as_js():
    L = ["// hvac_parts.js - generated by ~/.claude/skills/hvac/scripts/hvac_parts.py --js",
         "// The HVAC parts catalog in the same shape as parts.js: line / point parts with the physical facts",
         "// baked in and the PRICES filled at load time from the live price list, matched on `cat`.",
         "import { CATALOG } from '../catalog.js';", "", "export const PARTS = ["]
    for p in PARTS:
        L.append('  ' + json.dumps(p) + ',')
    L += ["];", "",
          "export const HEAD_SIZES = " + json.dumps(HEAD_SIZES) + ";",
          "export const MZ_SIZES = " + json.dumps(MZ_SIZES) + ";",
          "export const CENTRAL_SIZES = " + json.dumps(CENTRAL_SIZES) + ";",
          "export const ROUND_CFM = " + json.dumps({str(k): v for k, v in ROUND_CFM.items()}) + ";",
          "", "// prices from the live list, exactly as parts.js does it",
          "export function priced(overrides = {}) {",
          "  const byLabel = new Map(CATALOG.map(c => [c.label, c]));",
          "  return PARTS.map(p => { const c = overrides[p.cat] || byLabel.get(p.cat) || {}; return { ...p, rate: c.rate ?? null, cost: c.cost ?? null }; });",
          "}", ""]
    return '\n'.join(L)


def as_catalog():
    L = ["  // ---- HVAC (hvac_parts.py --catalog): rate / cost are Genaro's to set ----"]
    seen = set()
    for p in PARTS:
        if p['cat'] in seen:
            continue
        seen.add(p['cat'])
        unit = 'LF' if p['kind'] == 'line' else p.get('unit', 'EA')
        L.append("  { label: %s, emoji: '❄️', unit: '%s', rate: null, cost: null, def: 1, step: 1, trade: 'hvac', desc: %s }," % (json.dumps(p['cat']), unit, json.dumps(p['label'])))
    return '\n'.join(L)


def as_table():
    return '\n'.join(f"{p['id']:14s} {p['kind']:5s} {p.get('phase', ''):6s} {p['group']:22s} {p['label'][:80]}" for p in PARTS)


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    if '--json' in sys.argv:
        print(as_json())
    elif '--js' in sys.argv:
        print(as_js())
    elif '--catalog' in sys.argv:
        print(as_catalog())
    else:
        print(as_table())
        print(f'\n{len(PARTS)} parts, {len(set(p["cat"] for p in PARTS))} catalog labels')
