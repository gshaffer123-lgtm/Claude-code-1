# HVAC - the prices Genaro has to set (9/25/2026)

RVM has never sold HVAC, so **none** of the 113 catalog labels in `scripts/hvac_parts.py` exist on the live price
list. `hvac_bid.py` prints every quantity with a blank rate until they do. `hvac_catalog_rows.js` is the
paste-ready block for `public/js/catalog.js` (rate / cost null, `trade: 'hvac'`).

The street figures below are what the market research found on 9/25 (`research-hvac-market.md` section 8: online
distributors, Home Depot, HomeGuide / Angi). They are **street equipment prices, unmarked**, a sanity check - not a
rate. [S] = the figure was on the page; [S?] = a search extract; [D] = derived; PTS = nothing found, price to set.

## The eight that decide the bid

| label | unit | what the market says | how much a house (the five benchmark houses) |
|---|---|---|---|
| **Site labor (HVAC day rate)** | day | billed HVAC install labour $80-200+/h nationally, **$140-260/h in Seattle** (Angi) - a 2-person crew is $1,300-3,000+ a day billed; the roofing $3,000 is a placeholder | 9-19 days (placeholder minutes - see below) |
| **Multi-zone / single-zone outdoor unit** by size | EA | MXZ-3D24 $4,660 · MXZ-SM36 $5,473 · MXZ-SM48 $7,636 · Fujitsu 36k $5,180 · single-zone systems $2,300-4,200 | 1-2 a house |
| **Ductless wall head** by size | EA | MSZ-FX09 $879-987 · FX12 $1,034; installed per zone $2,500-5,000 (HomeGuide) | 5-7 on the ductless houses |
| **Heat pump outdoor unit (ducted)** + **Air handler** | EA | Mitsubishi 3-ton ducted system $8,015 · Bosch IDS 3-ton outdoor $3,888 · generic air handler $900-1,500; installed ducted heat pump in NW WA **$8,000-18,000+**, WA average $15,500 | 1 on the ducted houses |
| **Flex duct R-8 5 / 6 in** + **Supply trunk duct** + **Register boot** + **Duct takeoff** | LF / EA | not sourced (PTS); ductwork runs $270-500 installed per run (HomeGuide) | 200-420 LF flex, ~100 LF trunk, 13-21 runs |
| **ERV whole-house** + **ERV duct 6 in** | EA / LF | Panasonic FV-10VEC2 $1,037-1,132 · RenewAire EV Premium S $1,170; installed $1,500-2,500 | 1 unit + 260-470 LF on the ERV houses |
| **Line set 1/4 x 3/8** (and 1/4 x 1/2, 3/8 x 5/8, 3/8 x 3/4) | LF | $2.31/ft in a 50 ft set; $3.78-4.52/ft in a 25 ft 1/4 x 1/2 set; a long run adds $15-25/ft installed (HomeGuide) | 30-315 LF |
| **Mechanical permit** | EA | NOT FOUND for Whatcom, Bellingham, Blaine, Skagit or San Juan (`research-hvac-code.md` 8) - price it off each jurisdiction's fee sheet | 1 |

## Decide the model before the price

- **Per head / per system, or per part?** HVAC subs here quote per system or per zone ($2,500-5,000 a head installed;
  $12,000-20,000 for a ducted heat pump before ventilation). The catalog can do either: price the equipment lines at
  an installed number and leave the piping at $0, or price every part. Don't do both.
- **The install minutes are placeholders.** The research found no task-level HVAC install hours (every row of
  `research-hvac-market.md` 3.3 is PTS). The `site` minutes in `hvac_parts.py` are set so a single-zone lands inside
  the sourced 3-8 h band and a ducted 2,500 sf house near a week of rough-in. Replace them with a sub's numbers or
  the crew's before the day count is believed.
- **The labour cost** in the bid uses `bidcalc.py`'s roofing crew rates (crew $70 + lead $80 per paid hour) and the
  owner sales fee 5 % - the current bidcalc rule. An HVAC tech bills $140-260/h in Seattle.
- **Tests are subs.** The duct leakage test (WSEC R403.3.5, only when ducts leave the envelope) and the ventilation
  flow test (WA M1505.4) are third-party tests on most jobs: price them as the tester's invoice.
- **Equipment prices move with the refrigerant.** Everything bid from 2026 is an A2L (R-454B / R-32) unit; the
  R-410A list prices in older quotes do not apply.

## Every label, by section

### Equipment - 44

| label | unit | what it is | street figure (research-hvac-market.md 8) | install min (placeholder) |
|---|---|---|---|---|
| Ductless outdoor unit 9k single-zone | EA | Ductless outdoor unit - single-zone 9k, cold-climate (NEEP-listed), R-454B/R-32 | system (head + outdoor) Mitsubishi FX09 hyper-heat $2,812-3,093 [S]; the head alone $879-987 -> outdoor ~$1,900-2,100 [D] | 150 |
| Ductless outdoor unit 12k single-zone | EA | Ductless outdoor unit - single-zone 12k, cold-climate (NEEP-listed), R-454B/R-32 | Fujitsu XLTH 12k outdoor $2,169 [S]; Mitsubishi FX12 system $3,159 [S]; Daikin Aurora 12k system $2,290-2,339 [S] | 150 |
| Ductless outdoor unit 15k single-zone | EA | Ductless outdoor unit - single-zone 15k, cold-climate (NEEP-listed), R-454B/R-32 | Mitsubishi FX15 system $3,634 [S] | 150 |
| Ductless outdoor unit 18k single-zone | EA | Ductless outdoor unit - single-zone 18k, cold-climate (NEEP-listed), R-454B/R-32 | Mitsubishi FX18 system $4,231 [S?]; Daikin Aurora 18k system $3,571-4,113 [S] | 150 |
| Ductless outdoor unit 24k single-zone | EA | Ductless outdoor unit - single-zone 24k, cold-climate (NEEP-listed), R-454B/R-32 | PTS | 150 |
| Multi-zone outdoor unit 18k | EA | Multi-zone outdoor unit - 18k, cold-climate, up to 2 indoor units | PTS | 210 |
| Multi-zone outdoor unit 24k | EA | Multi-zone outdoor unit - 24k, cold-climate, up to 3 indoor units | Mitsubishi MXZ-3D24 hyper-heat $4,660 [S] | 210 |
| Multi-zone outdoor unit 30k | EA | Multi-zone outdoor unit - 30k, cold-climate, up to 4 indoor units | PTS | 210 |
| Multi-zone outdoor unit 36k | EA | Multi-zone outdoor unit - 36k, cold-climate, up to 5 indoor units | Mitsubishi MXZ-SM36 $5,473-5,477 [S]; Fujitsu AOUH36KWAH4 $5,180 [S] | 210 |
| Multi-zone outdoor unit 42k | EA | Multi-zone outdoor unit - 42k, cold-climate, up to 5 indoor units | PTS | 210 |
| Multi-zone outdoor unit 48k | EA | Multi-zone outdoor unit - 48k, cold-climate, up to 8 indoor units | Mitsubishi MXZ-SM48 $7,636 [S] | 210 |
| Multi-zone outdoor unit 60k | EA | Multi-zone outdoor unit - 60k, cold-climate, up to 8 indoor units | PTS | 210 |
| Ductless wall head 6k | EA | Ductless wall head 6k | PTS | 150 |
| Ductless wall head 9k | EA | Ductless wall head 9k | Mitsubishi MSZ-FX09 $879-987 [S] | 150 |
| Ductless wall head 12k | EA | Ductless wall head 12k | Mitsubishi MSZ-FX12 $1,034 [S] | 150 |
| Ductless wall head 15k | EA | Ductless wall head 15k | PTS | 150 |
| Ductless wall head 18k | EA | Ductless wall head 18k | PTS | 150 |
| Ductless wall head 24k | EA | Ductless wall head 24k | PTS | 150 |
| Ducted indoor unit 9k | EA | Ducted indoor unit (slim / multi-position) 9k | Mitsubishi SEZ-AD09 slim duct $1,232 [S] | 240 |
| Ducted indoor unit 12k | EA | Ducted indoor unit (slim / multi-position) 12k | PTS | 240 |
| Ducted indoor unit 18k | EA | Ducted indoor unit (slim / multi-position) 18k | PTS | 240 |
| Ducted indoor unit 24k | EA | Ducted indoor unit (slim / multi-position) 24k | PTS | 240 |
| Ducted indoor unit 36k | EA | Ducted indoor unit (slim / multi-position) 36k | PTS | 240 |
| Heat pump outdoor unit 24k ducted | EA | Heat pump outdoor unit - centrally ducted 24k (2 ton), cold-climate variable capacity | PTS | 240 |
| Air handler 24k | EA | Air handler - variable speed, 24k (2 ton) | PTS | 300 |
| Heat pump outdoor unit 30k ducted | EA | Heat pump outdoor unit - centrally ducted 30k (2.5 ton), cold-climate variable capacity | PTS | 240 |
| Air handler 30k | EA | Air handler - variable speed, 30k (2.5 ton) | PTS | 300 |
| Heat pump outdoor unit 36k ducted | EA | Heat pump outdoor unit - centrally ducted 36k (3 ton), cold-climate variable capacity | Mitsubishi PUZ-AK36 ducted SYSTEM $8,015 [S]; Bosch IDS 3-ton outdoor $3,888 [S] | 240 |
| Air handler 36k | EA | Air handler - variable speed, 36k (3 ton) | generic 3-ton air handler $900-1,500 [S] | 300 |
| Heat pump outdoor unit 42k ducted | EA | Heat pump outdoor unit - centrally ducted 42k (3.5 ton), cold-climate variable capacity | PTS | 240 |
| Air handler 42k | EA | Air handler - variable speed, 42k (3.5 ton) | PTS | 300 |
| Heat pump outdoor unit 48k ducted | EA | Heat pump outdoor unit - centrally ducted 48k (4 ton), cold-climate variable capacity | PTS | 240 |
| Air handler 48k | EA | Air handler - variable speed, 48k (4 ton) | PTS | 300 |
| Heat pump outdoor unit 60k ducted | EA | Heat pump outdoor unit - centrally ducted 60k (5 ton), cold-climate variable capacity | PTS | 240 |
| Air handler 60k | EA | Air handler - variable speed, 60k (5 ton) | PTS | 300 |
| Heat strip 5 kW | EA | Backup heat strip 5 kW (controlled per WSEC R403.1.2) | PTS | 40 |
| Heat strip 8 kW | EA | Backup heat strip 8 kW | PTS | 40 |
| Heat strip 10 kW | EA | Backup heat strip 10 kW | PTS | 45 |
| Heat strip 15 kW | EA | Backup heat strip 15 kW | PTS | 45 |
| ERV whole-house 150 cfm | EA | ERV / HRV - balanced whole-house, 50-150 cfm (SRE per the credit) | Panasonic FV-10VEC2 (<=100 cfm) $1,037-1,132 [S]; Broan B160E $1,141 [S?]; RenewAire EV Premium S $1,170 [S?] | 300 |
| ERV whole-house 250 cfm | EA | ERV / HRV - balanced whole-house, 150-250 cfm | RenewAire EV Premium M $1,415 [S?] | 330 |
| Thermostat heat pump programmable | EA | Thermostat - programmable, heat pump with aux-heat lockout (WSEC R403.1.1 / R403.1.2) | ecobee $190-250 [S] | 45 |
| Ductless wired controller | EA | Wired wall controller per ductless zone (optional) (option) | Mitsubishi MHK2 $415 [S?]; kumo adapter $189 [S] | 30 |
| Bath heater 500 W | EA | Supplemental bath heater <= 500 W (WSEC resistance allowance) (option) | PTS | 60 |

### Refrigerant piping - 13

| label | unit | what it is | street figure (research-hvac-market.md 8) | install min (placeholder) |
|---|---|---|---|---|
| Line set 1/4 x 3/8 | LF | Line set 1/4 x 3/8 insulated (pre-flared or brazed) | 50 ft set $115 (~$2.31/ft) [S]; 50 ft kit with wire, sleeve, hose $308 [S] | 2 |
| Line set 1/4 x 1/2 | LF | Line set 1/4 x 1/2 insulated | 25 ft set $94-113 (~$3.78-4.52/ft) [S] | 2 |
| Line set 3/8 x 5/8 | LF | Line set 3/8 x 5/8 insulated | PTS | 2.5 |
| Line set 3/8 x 3/4 | LF | Line set 3/8 x 3/4 insulated | PTS | 2.5 |
| Mini-split cable 14/4 | LF | Communication cable 14/4 stranded (outdoor unit to each indoor unit) | PTS | 0.2 |
| Line-set cover 4 in | LF | Line-set cover 4 in (exterior, painted), per foot | PTS | 2 |
| Line-set cover fitting | EA | Line-set cover fittings (wall inlet, elbows, coupler, end) | PTS | 5 |
| Line-set wall penetration | EA | Wall penetration - 3 in sleeve, sealed and flashed | PTS | 30 |
| Pressure test and evacuation | EA | Nitrogen pressure test + evacuation to 500 micron (per system) | PTS | 90 |
| Refrigerant additional charge (lb) | lb | Refrigerant - additional charge beyond the pre-charge (lb) | PTS | 0 |
| Equipment pad | EA | Equipment pad - composite, sized to the outdoor unit | concrete pad $300-500 INSTALLED [S] (composite pads are less) | 20 |
| Outdoor unit stand | EA | Outdoor unit stand / wall bracket (snow and drainage clearance) | PTS | 45 |
| Anti-vibration pads | EA | Anti-vibration pads (set of 4) | PTS | 5 |

### Condensate - 4

| label | unit | what it is | street figure (research-hvac-market.md 8) | install min (placeholder) |
|---|---|---|---|---|
| Condensate line 3/4 PVC | LF | Condensate line 3/4 in PVC (or 5/8 vinyl with the line set) | PTS | 1 |
| Condensate mini pump | EA | Condensate mini-pump (head on an interior wall / no fall to outside) | PTS | 45 |
| Secondary pan and float switch | EA | Secondary drain pan + float switch (M1411.3.1: equipment above finished space) | PTS | 45 |
| Condensate trap | EA | Condensate trap + cleanout tee | PTS | 15 |

### Ductwork - 17

| label | unit | what it is | street figure (research-hvac-market.md 8) | install min (placeholder) |
|---|---|---|---|---|
| Plenum set supply and return | EA | Supply + return plenums (fabricated, sealed, lined where required) | PTS | 120 |
| Supply trunk duct | LF | Supply trunk - galvanized rectangular / 10-14 in round (extended plenum) | PTS | 5 |
| Return duct | LF | Return duct 12-16 in (panned joist not allowed for a new return) | PTS | 5 |
| Duct takeoff with damper | EA | Takeoff / starting collar with balancing damper | PTS | 10 |
| Register boot | EA | Register boot (4x10 / 4x12 floor or 6x10 ceiling) | PTS | 12 |
| Duct hanger | EA | Duct hanger strap / saddle (flex every 4 ft, rigid every 10 ft) | PTS | 1 |
| Duct mastic and tape | EA | Duct mastic (gal) + UL-181 foil tape | PTS | 0 |
| Duct wrap R-8 | LF | Duct insulation R-8 wrap (rigid duct outside the envelope, WSEC R403.3.1) | PTS | 2 |
| Transfer grille or jumper | EA | Transfer grille pair / jumper duct (closed-door pressure relief) | PTS | 45 |
| Flex duct R-8 4 in | LF | Flex duct R-8 4 in | PTS | 2 |
| Flex duct R-8 5 in | LF | Flex duct R-8 5 in | PTS | 2 |
| Flex duct R-8 6 in | LF | Flex duct R-8 6 in | PTS | 2 |
| Flex duct R-8 7 in | LF | Flex duct R-8 7 in | PTS | 2 |
| Flex duct R-8 8 in | LF | Flex duct R-8 8 in | PTS | 2 |
| Flex duct R-8 10 in | LF | Flex duct R-8 10 in | PTS | 3 |
| Flex duct R-8 12 in | LF | Flex duct R-8 12 in | PTS | 3 |
| Flex duct R-8 14 in | LF | Flex duct R-8 14 in | PTS | 3 |

### Ventilation - 20

| label | unit | what it is | street figure (research-hvac-market.md 8) | install min (placeholder) |
|---|---|---|---|---|
| Exhaust duct 4 in | LF | Bath fan exhaust duct 4 in insulated flex (50 cfm fan: <= 25 ft, Table M1505.4.4.2) | PTS | 3 |
| Exhaust duct 6 in | LF | Exhaust duct 6 in insulated (80-110 cfm fans, whole-house fan: Table M1505.4.4.2) | PTS | 3.5 |
| Wall cap 6 in | EA | Wall / roof cap 6 in with backdraft damper | PTS | 30 |
| Wall cap 4 in | EA | Wall cap 4 in with backdraft damper | PTS | 25 |
| Roof jack 4 in | EA | Roof jack 4 in with damper (roofer flashes it) | PTS | 30 |
| Dryer duct 4 in rigid | LF | Dryer duct 4 in rigid metal, smooth wall (M1502.4.2) | PTS | 5 |
| Dryer elbow 4 in | EA | Dryer duct 4 in 90 elbow | PTS | 5 |
| Dryer vent box | EA | Dryer vent box (recessed) | Dryerbox 425 $46 [S] | 20 |
| Dryer wall cap | EA | Dryer wall cap with damper, no screen (M1502.3) | PTS | 25 |
| Dryer exhaust duct power ventilator | EA | Dryer exhaust duct power ventilator (DEPV, UL 705) where the run is over 35 ft equivalent (M150 (option) | Fantech DBF4XLT $144-397 [S?] | 90 |
| Range hood duct rigid | LF | Range hood duct 6-10 in rigid, sealed (M1503.3) | PTS | 6 |
| Range hood cap | EA | Range hood wall / roof cap with damper | PTS | 35 |
| Make-up air damper kit | EA | Make-up air damper (motorised) + hood interlock + duct (WA M1503.6: hood > 400 cfm with a non-d | Broan MD6TU $269 [S?]; Fantech kit from $145 [S] | 120 |
| ERV duct 6 in | LF | ERV duct 5-6 in (supply to bedrooms / living, exhaust from baths / kitchen / laundry) | PTS | 2.5 |
| ERV insulated duct 6 in | LF | ERV outdoor-air / exhaust duct, insulated with vapour jacket (to the hoods) | PTS | 4 |
| ERV wall hood 6 in | EA | ERV intake / exhaust hood 6 in (intake >= 10 ft from any exhaust, R303.5 / M1505.2) | PTS | 35 |
| ERV grille | EA | ERV supply / exhaust grille or valve 4-6 in | PTS | 15 |
| Whole-house exhaust fan continuous | EA | Whole-house exhaust fan, continuous duty, <= 1.0 sone (M1505.4) - replaces one electrical allow | Panasonic FV-0511VKS3 Pick-A-Flow 30-110 cfm $214 [S] | 60 |
| Whole-house ventilation control | EA | Whole-house ventilation control - 24 h timer / override, labelled (WA M1505.4.2) | AirCycler SmartExhaust $99-104 [S?] | 20 |
| Outdoor air inlet | EA | Outdoor air inlet 4 sq in NFA, through-wall with screen (WA exhaust-only whole-house ventilatio | PTS | 30 |

### Support + protection - 5

| label | unit | what it is | street figure (research-hvac-market.md 8) | install min (placeholder) |
|---|---|---|---|---|
| Firestop penetration | EA | Firestopped penetration (garage separation / rated assembly) | PTS | 10 |
| Nail plate | EA | Nail plate at a line-set / cable bore within 1-1/4 in of the face | PTS | 2 |
| Framing bore | EA | Bore through a stud / plate (counted, not priced) | PTS | 2 |
| Fire caulk | EA | Fire caulk / sealant (tube) | PTS | 0 |
| Mounting blocking | EA | Head / controller blocking (framer or HVAC) | PTS | 10 |

### Registers + grilles - 4

| label | unit | what it is | street figure (research-hvac-market.md 8) | install min (placeholder) |
|---|---|---|---|---|
| Floor register | EA | Floor register 4x10 / 4x12 | PTS | 8 |
| Ceiling diffuser | EA | Ceiling / sidewall diffuser 6x10 | PTS | 10 |
| Return filter grille | EA | Return / filter grille 20x25 (or 14x30) | PTS | 15 |
| Filter | EA | Filters MERV 8-13 (first set) | PTS | 2 |

### Commissioning - 6

| label | unit | what it is | street figure (research-hvac-market.md 8) | install min (placeholder) |
|---|---|---|---|---|
| HVAC design and load calc | EA | Load calculation + equipment selection for the permit (Manual J / S or the WSU sizing form) | PTS | 0 |
| HVAC start-up | EA | Start-up, charge verification, controls set-up (per outdoor unit) | PTS | 120 |
| Air balance | EA | Air balance of supply registers (per ducted system) | PTS | 90 |
| Duct leakage test | EA | Duct leakage test, total cfm25 (WSEC R403.3.5) - certified tester | PTS | 0 |
| Ventilation flow test | EA | Ventilation flow test - whole-house + local exhaust (WA M1505.4.3 / M1505.4.4) | PTS | 60 |
| HVAC hand-over | EA | Equipment labels, WSEC certificate data, owner hand-over | PTS | 30 |