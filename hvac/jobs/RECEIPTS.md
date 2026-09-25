# HVAC - receipts, five houses

Generated 2026-09-25 08:26 by `scripts/receipts.py` from each house's files. 5 houses.

## What ran, per house

| house | scan | takeoff | report | model | renders | bid | PDF |
|---|---|---|---|---|---|---|---|
| **4407 Aldrich Rd, Bellingham WA 98226** | ✅ | ✅ | ✅ | ✅ | 3 | ✅ | ✅ |
| **340 Ridgeway Pl, Sedro-Woolley WA 98284 (Gle** | ✅ | ✅ | ✅ | ✅ | 3 | ✅ | ✅ |
| **8835 Semiahmoo Dr, Blaine WA 98230** | ✅ | ✅ | ✅ | ✅ | 3 | ✅ | ✅ |
| **2168 Blind Bay Rd, Shaw Island WA 98286 (San** | — (no text layer) | ✅ | ✅ | ✅ | 3 | ✅ | ✅ |
| **312 Sudden Valley Dr, Bellingham WA 98229 (S** | ✅ | ✅ | ✅ | ✅ | 3 | ✅ | ✅ |

## Loads

| house | design | heating Btuh | Btuh/sf | WSU sheet | cooling tons | cool Btuh/sf | glazing sf | ACH50 | ventilation |
|---|---|---|---|---|---|---|---|---|---|
| 4407 Aldrich Rd, Bellingham WA | 19 F | 33,420 | 12.3 | 35,536 | 1.06 | 4.6 | 389 | 5 | exhaust 86 cfm |
| 340 Ridgeway Pl, Sedro-Woolley | 19 F (stand-in) | 25,039 | 10.3 | 31,752 | 1.64 | 8.1 | 744 | 2 | exhaust 70 cfm |
| 8835 Semiahmoo Dr, Blaine WA 9 | 19 F (stand-in) | 23,560 | 6.9 | 39,604 | 1.81 | 6.3 | 735 | 0.6 | erv 64 cfm |
| 2168 Blind Bay Rd, Shaw Island | 26 F (stand-in) | 24,719 | 12.4 | 25,508 | 1.23 | 7.4 | 341 | 5 | exhaust 113 cfm |
| 312 Sudden Valley Dr, Bellingh | 19 F (stand-in) | 18,306 | 12.2 | 24,190 | 0.97 | 7.8 | 511 | 1.5 | erv 45 cfm |

## Systems

| house | kind | outdoor | indoor | line sets ft | duct ft | vent ft | days | code / practice / data |
|---|---|---|---|---|---|---|---|---|
| 4407 Aldrich Rd, Bellingham WA | ducted | 42k central | 1 ducted unit(s), 21 registers | 34 | 449 | 28 | 12 | 0 / 1 / 0 |
| 340 Ridgeway Pl, Sedro-Woolley | ductless | 36k multi | 5 heads | 253 | 0 | 47 | 9 | 0 / 4 / 3 |
| 8835 Semiahmoo Dr, Blaine WA 9 | ducted_multizone | 60k multi | 2 ducted unit(s), 20 registers | 111 | 522 | 511 | 19 | 0 / 2 / 2 |
| 2168 Blind Bay Rd, Shaw Island | ductless | 30k multi + 24k multi | 7 heads | 285 | 0 | 44 | 11 | 0 / 6 / 2 |
| 312 Sudden Valley Dr, Bellingh | ducted | 24k central | 1 ducted unit(s), 13 registers | 26 | 337 | 285 | 14 | 0 / 0 / 2 |

## What the checker found

**4407 Aldrich Rd, Bellingham WA 98226**

- PRACTICE electrical: the 42k central outdoor unit typically needs a 35 A circuit [U: the nameplate MOCP governs]; the electrical job carries 30 A

**340 Ridgeway Pl, Sedro-Woolley WA 98284 (Gle**

- PRACTICE 36k outdoor unit (unit house): it sits under the upper storey (BED. 2 above): out of the snow, but set it on a ground stand with isolation pads, never a wall bracket - compressor vibration carries into the room above
- PRACTICE MASTER: line set 86 ft > the ~82 ft this unit class allows [U - the model's manual governs] - move the outdoor unit or the head
- PRACTICE multi-zone: total piping 253 ft > ~229 ft for a 36k multi-zone [U] - split the zones over two outdoor units
- DATA plan set: ach50: the set prints {1.5: 1, 2.0: 1} -> 1.5 (two values for one requirement; the tighter one is used for ACH50, the most frequent for R-values - confirm on the energy sheet)
- DATA plan set: credit 2.1 sets 2.0 ACH50 but the notes print 1.5 -> 1.5 (the tighter target governs the blower-door test and the infiltration load)
- DATA design temperature: 19 F is a stand-in (WSEC Table RC-1 Bellingham IAP 19 F / 78 F [S]; MJ8 Table 1A 23 F / 76 F [V] (Skagit foothills: the Bellingham row is the colder neighbour - STAND-IN)) - pull WSEC Table RC-1 for sedro-woolley before this goes out
- PRACTICE electrical: the 36k multi outdoor unit typically needs a 30 A circuit [U: the nameplate MOCP governs]; the electrical job carries 20 A

**8835 Semiahmoo Dr, Blaine WA 98230**

- DATA plan set: credit 2.3 (heat-recovery ventilation) AND a whole-house exhaust fan are both on the set -> hrv (if the ERV/HRV is the whole-house system the fan is local exhaust only; if the fan is the whole-house system the credit fails - ask the designer)
- PRACTICE unit house: the 60k outdoor unit carries 55,992 Btuh at 19 F against a 23,560 Btuh load - 2.4x AS SPECIFIED on the plan: ask how it was sized (Manual S 2023 wants >= 1.00 x at design and the minimum output <= 0.80 x; WA M1401.3 lets variable-capacity equipment run over, but not forever)
- DATA design temperature: 19 F is a stand-in (WSEC Table RC-1 Bellingham IAP 19 F / 78 F [S]; MJ8 Table 1A 23 F / 76 F [V] (Fraser outflow country - STAND-IN on the Bellingham row)) - pull WSEC Table RC-1 for blaine before this goes out
- PRACTICE electrical: the 60k multi outdoor unit typically needs a 50 A circuit [U: the nameplate MOCP governs]; the electrical job carries 40 A

**2168 Blind Bay Rd, Shaw Island WA 98286 (San**

- PRACTICE BED 2: a 6k head turns down to ~1,393 Btuh at 26 F against a 1,619 Btuh zone - over Manual S's 0.80 x load: it will cycle; carry this room from the zone next door or serve it with a slim ducted unit
- PRACTICE BED 1: a 6k head turns down to ~1,393 Btuh at 26 F against a 867 Btuh zone - over Manual S's 0.80 x load: it will cycle; carry this room from the zone next door or serve it with a slim ducted unit
- PRACTICE unit A: the 30k outdoor unit carries 30,117 Btuh at 26 F against a 12,106 Btuh load - 2.5x
- PRACTICE unit B: the 24k outdoor unit carries 24,094 Btuh at 26 F against a 12,613 Btuh load - 1.9x
- DATA design temperature: 26 F is a stand-in (STAND-IN: MJ8 Table 1A Friday Harbor AP 30 F / 75 F [V] shifted by Bellingham's RC-1 gap (-4 / +2 F) - pull Table RC-1 (Shaw is 3 mi from the Friday Harbor station)) - pull WSEC Table RC-1 for shaw island before this goes out
- PRACTICE electrical: the 30k multi outdoor unit typically needs a 25 A circuit [U: the nameplate MOCP governs]; the electrical job carries 20 A
- PRACTICE electrical: the 24k multi outdoor unit typically needs a 25 A circuit [U: the nameplate MOCP governs]; the electrical job carries 20 A
- DATA electrical: the electrical job labels 16 device(s) with the other unit's name - e.g. its 'Range (unit B)' marked unit B sits in unit A's footprint (DINING); this takeoff follows the plan (job.json units) - tell the electrician before the panel schedule goes out

**312 Sudden Valley Dr, Bellingham WA 98229 (S**

- DATA plan set: credit 2.2 (heat-recovery ventilation) AND a whole-house exhaust fan are both on the set -> hrv (if the ERV/HRV is the whole-house system the fan is local exhaust only; if the fan is the whole-house system the credit fails - ask the designer)
- DATA design temperature: 19 F is a stand-in (WSEC Table RC-1 Bellingham IAP 19 F / 78 F [S]; MJ8 Table 1A 23 F / 76 F [V] (Sudden Valley is ~8 mi from the airport, 300-700 ft up - STAND-IN on the Bellingham row)) - pull WSEC Table RC-1 for sudden valley before this goes out

## What the plans never said (the assumptions, per house)

**4407 Aldrich Rd, Bellingham WA 98226**

- system: ASSUMED. The WSEC credit table on A-1..A-3 is drawn, not text - hvacscan comes back 'unknown'. The electrical skill's job carries 'air-source heat pump with a ducted air handler' in the LAUNDRY; that is carried here UNREAD. RENDER A-1 AND LOOK before this bid is shown - a ductless credit (3.7) would change every line
- hood: no hood CFM on the set; 300 cfm ASSUMED
- dryer: LAUNDRY on A-2; electric ASSUMED (all-electric Bellingham norm per the electrical job)

**340 Ridgeway Pl, Sedro-Woolley WA 98284 (Gle**

- hood: A1.1 kitchen: 'HOOD VENT 36" ... 600 CFM MAKE-UP AIR HOOD UNDER-CABINET' - over 400 cfm, so M1503.6 make-up air, and the sheet asks for it
- dryer: LAUNDRY / MUDROOM on A1.1; electric ASSUMED (the electrical job's 30 A dryer circuit; no gas at Glenhaven)
- fireplace: A4.1/A4.2 details 'ROOF DETAIL @ FIREPLACE EAVE', 'FLOOR TO WALL DETAIL @ FIREPLACE'; the electrical skill read 'VENTED GAS' on the set. Direct-vent or natural-draft is not stated - a natural-draft unit is what makes WA M1503.6 make-up air mandatory for the 600 cfm hood (the plan asks for it anyway). Not HVAC scope

**8835 Semiahmoo Dr, Blaine WA 98230**

- system: Energy sheet: 'X NOTES FOR ENERGY OPTION 3.6 (1 CREDIT) Air-source, centrally ducted heat pump with minimum HSPF2 of 9.4 (HSPF of 11.0) ... In areas where the winter design temperature ... is 23 F or below, an air source centrally ducted heat pump shall be a cold climate variable capacity heat pump as listed on the NEEP qualified product list'; 'Heat Source: Electric heat pump'; the cut sheet is a Mitsubishi MXZ-SM60NAM (5-ton multi-zone Hyper-Heat, rated Non-Ducted // Mix // Ducted). The credit is only earned with DUCTED indoor units - one per storey is ASSUMED (the set names none). The plumbing skill read 'ductless' and the electrical skill an air handler: both were half right.
- foundation: crawl ASSUMED for the house (TJI on p16), as the plumbing skill read it
- ducts: a multi-zone with ducted indoor units per storey keeps the short duct runs in the floor / ceiling cavities inside the envelope - ASSUMED; if the main-floor unit goes in the crawl, set crawl_vented
- ventilation: energy sheet: 'X NOTES FOR ENERGY OPTION 2.3 (2 CREDITS) ... 0.6 air changes per hour' + the VENTS Frigate ERV 150 cut sheet ('the complete whole house ventilation system'); the plan also prints WHOLE HOUSE FAN and two EXHAUST FAN * tags - with the ERV they are local exhaust
- fireplace: p5 'GAS fp' in the living room (Cascade Natural Gas serves Blaine) - a direct-vent gas fireplace ASSUMED (the modern default; a natural-draft unit would trigger WA M1503.6 make-up air) - the fireplace installer's, not HVAC scope

**2168 Blind Bay Rd, Shaw Island WA 98286 (San**

- units: two mirrored units on one sheet, split at plan x = 70 ft. The west unit carries LIVING A and three bedrooms (PRIMARY BED, BED 1, BED 2; ~1,090 sf traced) = the 3-bed 1,301 sf unit; the east unit (LIVING B, BED 1, BED 2; ~975 sf traced) = the 2-bed 980 sf unit. NOTE: the electrical job's calc_sqft_by_unit names the 980 sf unit 'A' - the reverse of the plan's own LIVING A / LIVING B
- envelope: 2018 WSEC-R prescriptive values ASSUMED (the scanned set cannot be read here): ceiling R-49, wall R-21 int, floor R-30, fenestration U-0.30, 5.0 ACH50 - read the energy sheet and correct
- ventilation: exhaust-only whole-house fan per unit ASSUMED (the 2018 credit path named no HRV)

**312 Sudden Valley Dr, Bellingham WA 98229 (S**

- ventilation: A500 option 2.2: 'REDUCE AIR LEAKAGE TO 1.5 ACH AND A WHOLE HOUSE VENTILATION SYSTEM WITH MINIMUM SENSIBLE HEAT RECOVERY EFFICIENCY OF 0.7 = 1.5 CREDITS'; 'ERV' is labelled on the lower floor plan. CONFLICT: the same sheets also draw a 116 CFM WHF ('WHOLE HOUSE FAN WITH TIMER CAPABLE OF CONTINUOUS OPERATION ... AIRKING AK150LS OR SIMILAR') - an exhaust-only whole-house fan cannot earn 2.2. Bid the ERV as the whole-house system and the WHF as bath exhaust; ask the designer
- hood: A700 kitchen 'Range' - no hood CFM on the sheet; 300 cfm ASSUMED (under the 400 cfm make-up air trigger)
