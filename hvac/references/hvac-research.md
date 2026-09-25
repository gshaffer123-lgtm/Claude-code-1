# HVAC - what the engine leans on, and where each number came from (9/25/2026)

Three research digests sit beside this file, each number tagged **[V]** read from the source, **[S]** a search
extract of the named document, **[C]** computed from a [V] formula, **[D]** derived, **[U]** trade literature not
fetched (check the submittal), **PTS / NOT FOUND**:

| digest | what it covers |
|---|---|
| `research-hvac-code.md` | codes in force for a 2026 permit (2021 WSEC-R, WA-amended 2021 IRC), the WSEC credit tables 2018 vs 2021 and what each option number means, R403 controls / ducts / ventilation, M1401-M1602, refrigerant (A2L), design temperatures (mostly NOT FOUND), permits and inspections (fees NOT FOUND), I-2066 |
| `research-hvac-loads-sizing.md` | Manual J (NREL's open-source MJ8 code), the WSU sizing sheet, Manual S 2023, capacity at the design temperature, mini-split practice, Manual D, WA ventilation and exhaust duct tables, the checker bands |
| `research-hvac-market.md` | equipment street prices, line-set prices, labour (no task-level hours were found), sub pricing norms, what a bid includes, supply houses, rebates, the prices-to-set master list |

This file is the short version: the decisions the scripts make and the source each one stands on.

## 1. The codes (code 1-3)

- A permit applied for in 2026 runs on the **2021 WSEC-R** (effective 3/15/2024) and the **2021 IRC as amended by
  WAC 51-51**. The heat-pump mandate R403.13 was deleted; Initiative 2066 was struck down 9/17/2026. [V]
- **The energy sheet decides the system.** Credits required: small 5 / medium 8 / large 9 (2018: 3 / 6 / 7). The
  option numbers mean different things in 2018 and 2021 - `hvacscan.py OPTION_MEANING` keys on (edition, option)
  and reads the option's DESCRIPTION, never the number alone (code 3.8):
  - 2021 **3.7** ductless heat pump, no resistance in the primary living areas, HSPF2 >= 9, **sized to heat the whole
    dwelling at the design temperature** -> `ductless`
  - 2021 **3.6 / 3.6a** centrally ducted heat pump HSPF2 >= 9.4; where the Appendix RC design temperature is <= 23 F
    it must be a **NEEP-listed cold-climate variable-capacity** unit -> `ducted` (or `ducted_multizone` when the cut
    sheet is a multi-zone outdoor unit)
  - 2021 **2.2** 1.5 ACH50 + balanced ventilation with SRE >= 0.70; **2.3** 0.6 ACH50 + SRE >= 0.80 -> an ERV / HRV
  - 2021 **4 / 4c** heat pump as the primary heating source
  - 2018 **3.5** ducted / **3.6** ductless (older sets, e.g. Shaw)
- **Refrigerant**: a split system installed from 1/1/2026 is an A2L (R-454B / R-32) unit (EPA Technology
  Transitions); A2L leak detection / mitigation rides with the equipment listing. [V]

## 2. Design conditions (loads 1; code 7)

- The WSEC path uses **Table RC-1** (WAC 51-11R-60100): **Bellingham 19 F / 78 F** [S]. No other row was
  reachable. Manual J's own Table 1A (the ACCA Outdoor Design Conditions guide, read on ACCA's public bucket) [V]
  gives the WA stations near the work: Bellingham IAP 23 / 76 F, Arlington 25 / 79, Everett 25 / 76, Whidbey
  NAS 27 / 70, Friday Harbor 30 / 75, Sea-Tac 29 / 81.
- `hvac_parts.DESIGN`: a town uses its Table RC-1 row where one was read; otherwise the nearest Table 1A station
  shifted by Bellingham's RC-1 gap (-4 F heating / +2 F cooling), **flagged STAND-IN** on every job that uses it.
  The report prints the load at Manual J's 99 % temperature too.
- Indoor 70 F heating (MJ8, the WSU sheet) / 75 F cooling.

## 3. Loads (loads 3-4, 10)

- **Room by room** off the traced interior: exposure by probing outside each room edge (a skipped region wrapped
  >= 70 % by rooms is a chase / void, and gaps under 5 ft are closed first - an untraced stair is inside), U x A x dT
  per component, the floor over a vented crawl at 0.76 x dT (MJ8 Figure A12-6 [C]), slab edge F x P x dT.
- **Infiltration, MJ8 blower-door method** [V]: ICFM = 0.05488 x Q50 x sqrt(0.015 N dT + Cw 15^2), shielding 4 -
  ACH50 / 11.4 at design for two storeys, not the seasonal LBL N-factor.
- **Ventilation, WA** [V]: Qr = 0.01 x CFA + 7.5 x (bedrooms + 1), min 30; **Qv = Qr x Csystem** - 1.5 for a single
  exhaust fan (unbalanced, not distributed), 1.0 for an ERV ducted to every habitable room. An exhaust fan combines
  with infiltration as (ICFM^1.5 + Qv^1.5)^0.67 (MJ8); an ERV pays 1.1 x Qv x (1 - SRE) x dT.
- **Cooling** [V]/[C]: MJ8 glass multipliers at 48.8 N, SHGC 0.28, no internal shading (the 'peak' procedure for
  zoned / ductless systems); walls ~0 in Bellingham (CLTD = dTc - 2.4); a vented-attic ceiling at dTc + 35; a vault at
  dTc + 7; people 230 / 200 Btuh; appliances 2,400 Btuh (1,200 in the kitchen).
- **Cross-checks**: the WSU "Simple Heating System Size" sheet dT x (UA + 0.018 x 0.6 ACH x V) x 1.10 with ducts
  outside [S]; its heat-pump maximum is 1.25 x its load [S]. Bands [C]: Manual J heating 7-12 Btuh/sf (flag outside
  5-18), cooling 3.5-5.5 (flag > 8), cooling / heating 0.40-0.55.

## 4. Equipment (loads 5-6)

- **Never size on nominal.** Maximum heating capacity as a fraction of nominal, NREL ResStock cold-climate curves
  [V]: ductless 1.216 / 0.913 / 0.867 / 0.630 at 47 / 17 / 5 / -15 F (0.933 at 19 F); ducted 1.028 / 0.766 / 0.688 /
  0.507 (0.783 at 19 F). Minimum-compressor output from the same source.
- **Manual S 2023** (ACCA addendum c draft, 3/2025) [V]: variable-capacity heat pump capacity at design >= 1.00 x the
  load, minimum output <= 0.80 x; the supplemental heater <= 5 kW while the shortfall is under 15,000 Btuh. The
  takeoff accepts 0.95 x (a Manual J's accuracy; the strip carries the rest) and prints the one-size-down alternate.
  WA M1401.3 exempts multistage / VRF sizing within the maker's published range [V].
- **Mini-split practice** [U]: heads 6-24k; multi-zone ports 2-8; connected up to ~130 % of the outdoor nominal;
  line sets 1/4 x 3/8 to 12k, 1/4 x 1/2 to 18k, 3/8 x 5/8 to 36k; ~25 ft pre-charged, ~0.22 oz/ft past it; single
  6-12k 65 ft, 15-24k 100 ft; multi-zone ~82 ft a branch, 98-262 ft in total by model; lift ~49 ft; minimum ~10 ft.
  **The model's installation manual governs every one of these.**
- **Airflow** [V]: 400 cfm/ton rated; the ducts are sized for 375 cfm per ton of capacity AT DESIGN, never under
  the heating load at a 105 F supply or the sensible cooling at 55 F leaving air.
- **Ducts** [C]: round duct at 0.08 in / 100 ft - 4 in 33, 5 in 60, 6 in 98, 7 in 148, 8 in 212, 10 in 386, 12 in
  628, 14 in 947 cfm; flex = rigid x 0.85. Return grilles at <= 300 fpm. A closed bedroom needs ~0.55 sq in of
  free area per cfm at 3 Pa (transfer grille / jumper).

## 5. Exhaust and ventilation hardware (loads 8-9; code 5.6-5.8)

- **Bath / whole-house fan ducts**, WA Table M1505.4.4.2 [V]: a 50 cfm fan on 4 in flex <= 25 ft (smooth 70); an 80
  cfm fan cannot use 4 in flex (4 in smooth <= 20 ft; 6 in flex <= 90); 100 cfm needs 6 in (flex <= 45); 10 ft less
  per elbow past three.
- **Exhaust-only whole-house ventilation** (WA) [U, strong recall]: a continuous fan <= 1.0 sone on a labelled 24 h
  control with a manual override, and an **outdoor-air inlet (4 sq in NFA) in each habitable space** - trickle vents
  count.
- **Range hood make-up air** (WA M1503.6) [V]: required over 400 cfm **only** where a fuel-burning appliance that is
  neither direct-vent nor mechanical-draft sits inside the air barrier. An all-electric house does not trigger it.
- **Dryer** [V]: 4 in smooth metal, 35 ft less the fittings (5 ft per 4 in-radius mitered 90); past that, the
  dryer maker's table or a UL 705 duct power ventilator - **booster fans are prohibited** (M1502.4.5).
- **Tests**: the duct leakage test (WSEC R403.3.5) when any duct or the air handler is outside the envelope; the
  ventilation flow test (WA M1505.4) always.

## 6. Money (market 1-4, 8; bidding/scripts/bidcalc.py)

- The bid follows `bidcalc.py` today: materials off the live price list, site days at "Site labor", labour cost =
  paid hours x ($70 crew + $80 lead), **owner sales fee 5 %** (the 2.75 % partner fee came off 7/25).
- No HVAC label is priced; `prices-to-set.md` lists every one with the street figure found.
- Install minutes are **placeholders** - no task-level hours were found (market 3.3).

## 7. Still unverified (the verification queue)

1. WSEC Table RC-1 for every town but Bellingham; the WSU sheet's current location list.
2. Mechanical permit fees and inspection names for Whatcom County PDS, the City of Bellingham, Blaine, Skagit and
   San Juan County.
3. Every mini-split limit in section 4 (per model), multi-zone port counts, and the MCA / MOCP classes the
   electrical cross-check uses (`hvac_parts.BREAKER_A`).
4. Manual S 2023 final text (the values are from the 3/2025 public-review draft).
5. WA "distributed" definition for Csystem; the outdoor-air inlet rule's exact section; WSEC fan efficacy.
6. Install hours by task; the crew's day rate; the third-party test prices.
