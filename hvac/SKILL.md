---
name: hvac
description: HVAC takeoff, 3D model and draft bid (equipment / rough-in / trim) for a new house in the RVM app / Build Radar - the WSEC energy sheet read for the system it commits the house to (2021 option 3.7 ductless, 3.6 / 3.6a centrally ducted, 2.2 / 2.3 heat-recovery ventilation, the 2018 numbering on older sets), room-by-room heat loss and gain off the finish skill's traced interior (ACCA Manual J method as NREL's open-source MJ8 code implements it - blower-door infiltration, the WA ventilation rate x Csystem, MJ8 cooling multipliers) with the WSU sizing sheet as a cross-check, the system sized AT THE DESIGN TEMPERATURE (cold-climate capacity curves, Manual S 2023): ductless zones and heads on a multi-zone or single-zone units, a ducted heat pump + air handler + strip with registers, trunks, returns and transfer paths, or a multi-zone with ducted indoor units; line sets routed down the stud bay and across the crawl, condensate to daylight, every bath fan the electrician placed ducted and capped by WA Table M1505.4.4.2, the dryer vent against 35 ft, the range hood and WA make-up air, the whole-house fan or the ERV, outdoor-air inlets, the duct-leakage and ventilation flow tests, a checker (code / practice / data), the cross-trade circuit check against the electrical job, the model drawn in the electrical skill's wall visual, a PDF parts list, the worker's result.json, and the prices Genaro has to set. Triggers - "HVAC takeoff", "HVAC bid", "heat pump bid", "mini-split layout", "ductless heads", "how many heads", "heat loss", "Manual J", "load calc", "duct layout", "line sets", "ERV", "whole-house fan", "ventilation", "bath fan ducts", "dryer vent", "make-up air", "mechanical bid for <address>".
---

# HVAC: every load, head, register, duct, line set and vent - sized, counted and shown

Genaro (9/25/2026): "Can you look at how we built the skills for the other trades, and let's do a full deep
dive into building a skill for HVAC bids?"

HVAC is the trade where the plan does not draw the thing being bid. The electrician counts symbols; the
plumber reads fixtures off the ink. The HVAC contractor is handed two sentences on the energy sheet ("3.7 -
ductless heat pump ... sized to heat the entire dwelling at design temperature") and has to work out the rest:
**how much heat each room loses**, what that asks of the equipment at 19 F, where the heads or registers go,
and how every line set, duct and vent gets out of the house. So the skill works in that order - the **energy
sheet** (`hvacscan.py`) says which system the permit bought, the **loads** (`hvac_load.py`) size it room by room,
the **engine** (`hvackit.py`) lays it out and counts it, the **model** shows it inside the house, the **bid**
splits equipment / rough-in / trim. Nothing is sent; every price is Genaro's.

## The eight moves

| # | step | script | out |
|---|---|---|---|
| 0 | the interior: rooms, wall runs, doors, windows, storeys | `finish/scripts/interior.py` (already run on the five houses) | `interior.json` |
| 1 | **the energy sheet**: WSEC edition, credits and what each MEANS, the system they name, envelope, window schedule, fans / hood / dryer, conflicts | `hvacscan.py plans.pdf --out hvac_scan.json --png energy_p{N}.png` | `hvac_scan.json` + the energy sheet rendered - **look at it** |
| 2 | **the loads**, room by room (runs inside step 3; alone for a load calc) | `hvac_load.py job.json` | `hvac_loads.json` |
| 3 | **the system, the runs, the parts, the checks** | `hvackit.py job.json` | `hvac_takeoff.json`, `hvac_report.md` |
| 4 | the model | `hvac_model.py hvac_takeoff.json --job job.json` | `<slug>_app.json` (groups `floors`, `walls`, `equipment`, `terminals`, `hvac` - no glass) |
| 5 | three renders | `hvac_render.py` (the skill's own) | `shot_35.png`, `shot_215.png`, `shot_top.png` (straight down = the mechanical plan) |
| 6 | the draft bid (+ the worker's result) | `hvac_bid.py hvac_takeoff.json [--result trades/hvac/result.json]` | `hvac_bid.json`, `hvac_bid.md` (equipment / rough-in / trim + options) |
| 7 | the PDF parts list, the receipts | `hvac_pdf.py`, `receipts.py` | `<slug>.pdf`, `receipts.md` |

One command: `python ~/.claude/skills/hvac/scripts/hvac_run.py jobs/<house>/job.json [--pdf plans.pdf] [--skip-scan] [--no-live] [--result trades/hvac/result.json]`.
`hvac_pdf.py --all jobs <dir>` prints every house; `receipts.py jobs --all` writes `jobs/RECEIPTS.md`.

## What it needs on the machine

- The sibling skills beside it: **finish** (`interior.json`), **electrical** (`elec_route.WallNet` draws the house;
  its `jobs/<h>/devices.json` is read when it is there), **flooring** (`floormodel.Mesh`, the viewer payload), and
  **bidding** for the money rule. They are found at `$CLAUDE_SKILLS`, else next to this skill (`~/.claude/skills/hvac`
  -> `~/.claude/skills`). The skill never writes into them.
- Python: `shapely`, `numpy`, `opencv-python-headless`, `pymupdf` (the same set the plumbing and electrical skills use).
- This skill was built in the `Claude-code-1` repo (`hvac/`); it runs from there with `CLAUDE_SKILLS` pointing at the
  skills clone, and it belongs in `claude-skills/hvac/` next to its siblings (then `setup_worker.ps1` installs it).

## 1. The energy sheet decides the system (`hvacscan.py`)

The permit was issued on the credits the designer ticked. **Read the option's DESCRIPTION, never its number alone**
- 2021 3.6 is a ducted heat pump, 2018 3.6 is ductless; 2021 2.2 and 2.3 carry an ACH50 target AND a heat-recovery
requirement. `OPTION_MEANING` keys on (edition, option). What it does, in order:

1. The edition (2018 / 2021 votes), the dwelling size and credits required, the **selected credits** - the
   'options selected' list, the WSU form's X rows, a '(3.6a) ... = 1.0 CREDIT' line - with the quote kept.
2. The system: every credit votes (weight 3), a cut sheet votes (a multi-zone model number), words vote (1).
   A multi-zone outdoor unit on a **centrally ducted** credit is `ducted_multizone` (Semiahmoo).
3. The envelope R / U values, ACH50 targets, the window schedule (sizes, operation, U), heated areas.
4. Fans (a whole-house fan's cfm), the hood cfm and make-up air words, the dryer, the fireplace, mechanical rooms.
5. **Conflicts** - an ERV credit and an exhaust-only whole-house fan on the same set, two ACH50 targets, a
   centrally-ducted credit and a ductless cut sheet - each with the value used and why.
6. Owner, e-mail, phone and parcel lines are dropped before anything is quoted.

A scanned set (no text layer - Shaw) or a credit table drawn as linework (Aldrich) comes back `unknown`: then
**job.json carries the system, marked ASSUMED, and the checker says so**. Render the energy sheet
(`--png`) and LOOK before a bid goes out - a 3.7 in place of a 3.6 changes every line.

## 2. The loads - room by room (`hvac_load.py`)

Every other interior trade counts something drawn. HVAC counts heat, built the way ACCA Manual J builds it -
component by component, per room - off the same traced interior (`references/hvac-research.md` 2-3):

| piece | how | source |
|---|---|---|
| design temperature | WSEC Table RC-1 where a row was read (Bellingham 19 F / 78 F); otherwise the nearest MJ8 Table 1A station shifted by Bellingham's RC-1 gap, flagged STAND-IN | loads 1 [S]/[V] |
| exposure | a room edge is exterior where probes 1.5 and 4 ft out land in no room; a skipped region wrapped >= 70 % by rooms (a chase, the fireplace mass) is inside, gaps under 5 ft (an untraced stair) are closed first; a wall onto the garage is exterior for the load but never takes a unit, a cap or a vent | - |
| envelope | the plan's R-values through `R_TO_U`, else the 2021 prescriptive defaults; the window schedule when the tracer found less glass (spread by exterior wall length) | code 4 |
| heating | U x A x dT per wall, window, door, ceiling; the floor over a vented crawl at 0.76 x dT; slab edge F x P x dT; ducts in a vented crawl +10 % | MJ8 [V]/[C] |
| infiltration | ICFM = 0.05488 x Q50 x sqrt(0.015 N dT + Cw 15^2) - ACH50 / 11.4 at design on two storeys | MJ8 [V] |
| ventilation | Qr = 0.01 CFA + 7.5 (Nbr + 1) >= 30, **Qv = Qr x Csystem** (1.5 for one exhaust fan, 1.0 for an ERV to every room); exhaust combines with infiltration as (ICFM^1.5 + Qv^1.5)^0.67; an ERV pays (1 - SRE) | WA M1505.4.3 [V] |
| cooling | MJ8 glass multipliers at 48.8 N (SHGC 0.28, no drapes - the 'peak' procedure for zoned systems) + U x dT; walls ~0; attic ceiling dT + 35, vault dT + 7; people 230 / 200; appliances 2,400 | MJ8 [V]/[C] |
| cross-checks | the WSU 'Simple Heating System Size' sheet (x 1.25 = its heat-pump maximum); bands 7-12 Btuh/sf heating (flag 5-18), cooling 3.5-5.5, cooling / heating 0.40-0.55; the load at Manual J's own 99 % temperature | loads 2, 10 |

## 3. The system (`hvackit.py`)

**ductless** (3.7): tracer fragments with the same name that touch are merged into one space; a 'bedroom' under
70 sf is a fragment (IRC R304.1) and never gets a head. Rooms joined by cased openings on one storey are one
zone (never a bedroom); closets and baths ride with the room their door opens into (a bedroom takes its own),
halls and landings with the living zone they reach. **A head per zone**, the smallest whose capacity at the design
temperature carries the zone (heads 6-24k), the host preferring living / dining over the kitchen; a zone under
1,500 Btuh joins its neighbour. Two heads or fewer -> single-zone units; more -> **one multi-zone** whose capacity
AT DESIGN carries the whole unit (3.7 says exactly that), within its ports and ~130 % connection; else one per
storey. The checker flags a head whose minimum output is over 0.80 x its zone (Manual S: it will cycle).

**ducted** (3.6 / 3.6a): the smallest ducted heat pump whose capacity at design is >= 0.95 x the load (Manual S
2023 wants 1.00; the 5 kW strip Manual S allows under a 15,000 Btuh shortfall carries the rest) - and the one size
down is printed as the alternate. The air handler goes where job.json says (a skipped MECH room is fine), else the
electrician's air-handler junction (unless it is in the garage or shop), else MECH / LAUNDRY / storage. Airflow is
**375 cfm per ton of capacity at design**, never under what the heating load needs at 105 F supply. Registers per
space in proportion to its load (<= 90 cfm a 4x10), along its exterior walls; a trunk per storey along the long axis
through the unit, flex branches sized off the round-duct table x 0.85; a central return per storey at <= 300 fpm; a
transfer grille or jumper out of every closed room with a supply (0.55 sq in a cfm at 3 Pa). Ducts in a vented
crawl get R-8 and the duct leakage test.

**ducted_multizone** (a multi-zone outdoor unit on a ducted credit): the ducted layout per storey with a slim
ducted indoor unit on each, the refrigerant of a multi-zone. `outdoor_kbtuh` in job.json forces the plan's size -
and the checker asks why when it is 2x the load.

## 4. The runs

- **Line sets, concealed** (the default on a crawl): down the stud bay under the head (or the nearest stacked wall
  when the storey above overhangs), across the crawl on an L along the joists, out the rim beside the outdoor
  unit, + two service loops. **Exterior** (slab, or `lineset_route: exterior`): through the wall behind the head,
  down a painted line-hide, along the foundation. Sized by capacity, extra charge past the pre-charged 25 ft;
  branch / total / minimum lengths checked against the class limits (the model's manual governs).
- **The outdoor unit** goes where job.json `hvac.outdoor.pos` says, else **at the electrician's condenser /
  mini-split disconnect** (one per system), else on the open-air wall nearest the equipment - never onto the
  garage, a deck costs a little. Under a cantilevered storey it is flagged: ground stand, isolation pads.
- **Condensate**: down with the lines, then the shortest way out of the crawl to daylight (never into the crawl).
- **Exhaust**: every bath fan the electrician placed (they supply and wire it; HVAC ducts and caps it) - to the
  roof over the top storey or the nearest open-air wall, the duct sized by WA Table M1505.4.4.2 (4 in flex for a
  50 cfm fan to 25 ft; 6 in for 80-110 cfm). The **whole-house fan** is one of them, upgraded to continuous duty.
- **Dryer**: from the electrician's dryer outlet, 35 ft less 5 ft an elbow; over that, a UL 705 duct power
  ventilator option (booster fans are prohibited). **Range hood**: from the electrician's range outlet, sized by
  cfm; make-up air only where WA M1503.6 wants it (> 400 cfm AND a non-direct-vent fuel appliance inside) or the
  plan asks. **ERV**: trunk-and-branch - supply to bedrooms and living spaces, exhaust from baths and laundry; a
  vaulted storey's trunk runs in the floor cavity below to high-sidewall grilles; intake and exhaust hoods 12 ft apart.

## 5. Reading the other trades

The HVAC takeoff leans on work already done, and says so in every report:

- **finish** - the rooms, walls, doors, windows and storeys (`interior.json`); `storey_shift` in job.json applies
  the finish job's measured offset (Aldrich) without touching its file.
- **electrical** - `devices.json`: the bath fans, the dryer and range outlets, the condenser / mini-split
  disconnect and the air-handler junction. Then the **cross-trade check**: one 240 V circuit and a disconnect per
  outdoor unit, sized to the unit (`BREAKER_A` [U] - the nameplate governs); the air-handler circuit against its
  strip; a separate 'indoor heads' circuit that most splits do not need; one bath-fan allowance that becomes the
  whole-house fan; an electrical job whose unit labels are the reverse of the plan's (Shaw).
- **electrical `elec_route.WallNet`** draws the house in the model, the way the plumbing skill does it.

## 6. The checker

Three levels, each with where and why:

- **code** - WSEC 3.7 capacity short of the whole-house load at design; a whole-house fan under the WA rate; a
  hood over 400 cfm with a non-direct-vent fuel appliance and no make-up air; a dryer run over 35 ft; an exhaust
  duct past Table M1505.4.4.2; the plan's credit and job.json disagreeing on the system.
- **practice** - oversized equipment (2x the load; the plan's specified unit flagged 'as specified'); a head or unit
  whose minimum output is over 0.80 x its load; line sets past their class limits; the electrical job's circuits
  smaller than the equipment wants; an outdoor unit under a bedroom.
- **data** - conflicts on the set (two ACH50 targets, an ERV credit with an exhaust fan), a STAND-IN design
  temperature, a room job.json names that is not traced, the electrical job's unit labels reversed.

## job.json

```json
{
 "address": "...", "slug": "<number>-<street>-hvac", "permit": "...", "plans": "<plans pdf name>",
 "interior": "../../../finish/jobs/<h>/interior.json",
 "storeys": [{"name": "main", "page": 6, "z": 0.0, "plate": 10.0}],
 "storey_shift": {"upper": [-2.16, -7.48]},                     // optional: the finish job's measured offset
 "hvac": {
  "jurisdiction": "whatcom | bellingham | blaine | skagit | sanjuan",
  "code": {"wsec": "2021", "credits_required": 8.0},
  "system": {"kind": "ductless | ducted | ducted_multizone", "option": "3.7", "hspf2_min": 9.0,
             "layout": "auto | singles", "outdoor_kbtuh": 60, "ahu_room": "main/MECH", "lineset_route": "concealed | exterior"},
  "design": {"heat": 19, "cool": 78},                            // optional: overrides the town table
  "cfa_sf": 2436, "bedrooms": 2,
  "units": [{"name": "A", "x_max": 70.0, "cfa_sf": 1301, "bedrooms": 3}],   // a duplex: one system per unit
  "envelope": {"ceiling_r": 60, "vault_r": 38, "wall": "R-20+5", "floor_r": 38, "window_u": 0.24, "ach50": 2.0},
  "vaulted_rooms": "upper/*", "exclude_rooms": ["WORKBENCH / SHOP"],
  "foundation": "crawl | slab", "ducts": "inside | crawl_vented | crawl_conditioned | attic",
  "ventilation": {"kind": "exhaust | erv | hrv", "sre": 0.7, "whf_cfm": 90, "whf_room": "upper/BATH. 2", "model": "..."},
  "hood": {"cfm": 600, "makeup_air": true}, "dryer": {"present": true, "fuel": "electric"},
  "fireplace": {"present": true, "fuel": "gas", "vent": "direct"},
  "outdoor": {"side": "auto", "pos": [x, y]},
  "labour": {"crew": 2, "capacity_hr": 6.25}
 }
}
```

Every key the plan answered carries a `_key` receipt beside it - the sheet and the words, or **ASSUMED** and why.
The report and the receipts print them back.

## The draft bid (`hvac_bid.py`)

Same line shape as every RVM bid - `{label, desc, qty, unit, rate, cost, price, cst, note}` - and the money rule
`bidding/scripts/bidcalc.py` runs **today**: materials off the live price list by catalog label; site time in whole
days at "Site labor"; labour cost = paid hours x (crew $70 + lead $80); the **owner sales fee 5 %** (the 2.75 %
partner fee came off 7/25 - the electrical, plumbing and finish bids still carry the old 7.75 %; this one does not).

| section | what | days |
|---|---|---|
| **Equipment** | outdoor unit(s), heads / air handler / ducted units, strip, ERV, thermostats | set |
| **Rough-in** | line sets, comm cable, condensate, ducts, boots, takeoffs, returns, transfers, exhaust / dryer / hood ducts and caps, whole-house fan, inlets, supports, sleeves, firestops | rough |
| **Trim, start-up and tests** | registers, grilles, filters, start-up, air balance, duct-leakage + ventilation flow tests, the permit load calc, labels, **the mechanical permit line (unpriced)** | trim + start-up |
| options | wired zone controllers, a dryer duct power ventilator - priced, never in the sum | - |

`--result` also writes the worker's `trades/hvac/result.json` in the `rvm-app scripts/order_trades.mjs` contract
(lines, unknowns, options, report_file, model_file, and the `/api/docs` create body filed under trade `hvac`).

## The model

Metres, Y up, plan x east, plan y south - the RVM frame (`floormodel.Mesh`), so it drops onto the card. The
house is the electrical skill's generated wall set, full height, translucent, no roof, no glass. `equipment`
(outdoor units on their stands, heads on their walls, air handlers, ducted units in the ceiling, the ERV),
`terminals` (registers, returns, grilles, hoods, fans, caps), `hvac` (every run at its real size): line set copper,
condensate pale cyan, trunk dark blue, branch blue, return green, bath exhaust violet, ERV supply teal, ERV exhaust
orange, ERV outdoor air grey-teal, hood dark grey, dryer brown. The legend is in the payload. **Render two yaws and
the plan view and LOOK before believing a run** - the Sudden Valley render is what caught ERV ducts hanging over a
vaulted ceiling.

## Receipts table (every run ends with it)

`receipts.py` reads what is on disk - the scan, the takeoff, the model, the renders, the bid, the PDF - and prints
what ran, what the plan text said, what the electrical job supplied and what is an assumption. `jobs/RECEIPTS.md`
compares the five.

## The five houses (9/25/2026)

| house | system (credit) | heating load at design | equipment | runs | days* | findings |
|---|---|---|---|---|---|---|
| **4407 Aldrich Rd**, Bellingham, SFR2025-00084 | ducted - ASSUMED (the credit table is linework) | 33,420 Btuh at 19 F (12.3 Btuh/sf) | 42k ducted cold-climate HP (0.98 x at design) + 5 kW strip, air handler in the LAUNDRY, 21 registers | line set 34 ft, duct 449 ft (crawl: R-8 + leakage test) | 12 | 0 code / 1 practice / 0 data |
| **340 Ridgeway Pl**, Glenhaven, SFR2025-00214 | ductless 3.7 (read) | 25,039 at 19 F stand-in (10.3) | 36k multi-zone, 5 heads (9k dining, 9k master, 6k office, media, bed 2) | line sets 253 ft concealed | 9 | 0 / 4 / 3 |
| **8835 Semiahmoo Dr**, Blaine, SFR2026-00068 | ducted multi-zone 3.6 + ERV 2.3 (read; MXZ-SM60NAM specified) | 23,560 at 19 F stand-in (6.9) | 60k multi-zone as specified (2.4x the load), ducted 12k + 18k, VENTS ERV 64 cfm | duct 522 ft, ERV duct 511 ft | 19 | 0 / 2 / 2 |
| **2168 Blind Bay Rd**, Shaw Island, BUILD-24-0020 (duplex) | ductless, 2018 3.6 - job.json (scanned set) | 24,719 at 26 F stand-in (12.4) | unit A 30k multi 4 heads; unit B 24k multi 3 heads | line sets 285 ft | 11 | 0 / 6 / 2 |
| **312 Sudden Valley Dr**, SFR2025-00185 | ducted 3.6a + 4c, ERV 2.2 (read) | 18,306 at 19 F stand-in (12.2) | 24k ducted HP + 5 kW, air handler in the MECHANICAL ROOM UNDER STAIRS, 13 registers, ERV 45 cfm | duct 337 ft, ERV duct 285 ft | 14 | 0 / 0 / 2 |

\* crew-days at PLACEHOLDER install minutes (2-person crew, 6.25 h a day).

What each one taught:

- **aldrich** - the credit table is drawn, not written: `hvacscan` says `unknown` and job.json carries 'ducted'
  from the electrical job, UNREAD - render A-1 before this goes out. The upper storey needed the finish job's
  measured shift or every ceiling reads as open to the sky. Sizing to 1.00 x would have bought a 4-ton; 0.95 x with
  the strip is a 3.5-ton.
- **ridgeway** - the only house where the ductless credit is plain text. The tracer split the master suite into
  three 'MASTER' rooms (three heads until the spaces merged); an untraced stair gap read as outside wall (and the
  outdoor unit landed in it) until gaps under 5 ft were closed. 745 sf of glass makes cooling 8.1 Btuh/sf - the
  checker flags it. The 600 cfm hood gets make-up air because the plan asks and the fireplace is vented gas. The
  electrical job carries a 20 A circuit where a 36k multi-zone wants ~30 A.
- **semiahmoo** - the plan specifies a 60k multi-zone for a 23,560 Btuh house: 2.4x, over the WSU sheet's own
  heat-pump maximum. The ducted credit means ducted indoor units, not the ductless heads the plumbing skill read;
  the electrician put the air handler in the shop (outside the envelope). 0.6 ACH50 and an 80 % ERV make it the
  tightest load of the five (6.9 Btuh/sf).
- **shaw** - a duplex: one system per unit, split at x = 70. Port count, not load, sized both multi-zones (2.5x /
  1.9x); two 6k bedroom heads will cycle (Manual S turndown). The electrical job's unit labels are the reverse of
  the plan's LIVING A / LIVING B - 16 devices - and it is flagged. No text layer: every envelope value is ASSUMED.
- **suddenvalley** - the ERV credit (2.2) and a 116 cfm whole-house fan on the same set: bid the ERV, ask the
  designer. The air handler's room is a SKIPPED mechanical room under the stairs - found by name anyway. A vaulted
  upper storey has no attic, so its ERV trunk runs in the floor cavity (the render caught the first version).

## Prices to set

`references/prices-to-set.md`: all 113 labels, the eight that decide the bid, the street figure the market research
found beside each (MXZ-SM36 $5,473, MSZ-FX09 head $879-987, ducted 3-ton system $8,015, ERV $1,037-1,415, line set
$2.31/ft ...), and the install minutes to replace. `references/hvac_catalog_rows.js` is the paste-ready block for
`public/js/catalog.js` (rate / cost null, `trade: 'hvac'`); `hvac_parts.js` / `.json` the catalog for any consumer.

## Into the app

`references/rvm-app-hvac.patch` (apply in `rvm-app` with `git apply`): the HVAC bid on the card's order menu and
in `DOC_TRADES`, the worker's `TRADE_SKILL` / `TRADE_NEEDS` (finish + electrical) / `TRADE_LABEL` / `DOC_TRADE` /
`STEPS.hvac` (the agent runs `hvac_run.py ... --result trades/hvac/result.json`), and `hvac` in `setup_worker.ps1`'s
skill list. `node scripts/tests/order_trades_test.mjs` passes with it applied (menu, result, runTrade, failures).

## Still owed

1. **WSEC Table RC-1** for every town but Bellingham - four of the five houses run on a STAND-IN design temperature.
2. **Mechanical permit fees** and inspection names for Whatcom PDS, Bellingham, Blaine, Skagit, San Juan.
3. **Install minutes** from a sub or the crew; the HVAC day rate; the third-party test prices.
4. **The model's own limits** - line-set lengths, ports, pre-charge, MCA / MOCP - from the submittal of the unit bid
   (`hvac_parts` carries typical classes, tagged [U]).
5. **Aldrich's energy sheet** read by eye (the system is assumed); **Shaw's** envelope off the scanned sheet.
6. Hourly glass loads (MJ8's AED excursion) for west-glass houses; skylights as their own glass class.
7. A dryer or equipment in a skipped storage room vents from that room's own wall (today the nearest kept room's).

## Reference

- `references/hvac-research.md` - the decisions and their sources, in one page
- `references/research-hvac-code.md` - codes, credits, ventilation, refrigerant, permits (the code digest)
- `references/research-hvac-loads-sizing.md` - Manual J / S / D, capacity curves, duct and exhaust tables (the loads digest)
- `references/research-hvac-market.md` - equipment and material prices, labour, sub norms (the market digest)
- `references/prices-to-set.md`, `hvac_parts.json` / `.js`, `hvac_catalog_rows.js`, `rvm-app-hvac.patch`
- `scripts/hvac_parts.py` - the catalog and every design table (single source of truth)
