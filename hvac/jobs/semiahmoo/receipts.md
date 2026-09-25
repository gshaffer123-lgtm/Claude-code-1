# Receipts - 8835 Semiahmoo Dr, Blaine WA 98230

`8835-semiahmoo-hvac` · permit SFR2026-00068 · generated 2026-09-25 08:09 by `receipts.py` from the files in this folder.

| Step | Ran | Receipt |
|---|---|---|
| sheets | y | p5 = main (plate 10.0 ft); p6 = upper (plate 9.0 ft) · the finish skill's interior.json is the room source |
| plan text read (hvacscan) | y | 77,491 characters, WSEC 2021, - credits required · credits read: 2.3 (air leakage 0.6 ACH50 + whole-house vent), 3.6 (air-source CENTRALLY DUCTED heat pump, H) · system named: **ducted_multizone** · 0 schedule openings · 1 conflict(s) |
| loads (hvac_load) | y | heating **23,560 Btuh** (6.9 Btuh/sf) at 19 F (Bellingham IAP, STAND-IN) · cooling 20,857 + 920 latent (6.3 Btuh/sf) · WSU sheet 39,604 · glazing 735.1 sf (traced windows (interior.json)) · 36 rooms · 1 load warning(s) |
| ventilation | y | erv 64.3 cfm = Qr 64.3 x Csystem 1.0 (WA M1505.4.3) · load 722 Btuh |
| system, unit house | y | ducted_multizone: 60k multi (at the electrician's Heat pump condenser (LIVING R); 18k in LAUNDRY, 12k in HALL · 20 registers, 2 returns · capacity at design 55,992 vs load 23,560 Btuh |
| runs | y | line sets 111 ft (concealed) · duct 522 ft · vent / exhaust 511 ft |
| electrical layout read | y | electrical/jobs/semiahmoo/devices.json (286 devices): bath fans, the dryer and range outlets, the outdoor-unit disconnect and air-handler junction positions |
| the checker | y | **0 code**, 2 practice, 2 data: plan set: credit 2.3 (heat-recovery ventilation) AND a whole-house exhaust fan a / unit house: the 60k outdoor unit carries 55,992 Btuh at 19 F against a 23,560 Btuh / design temperature: 19 F is a stand-in (WSEC Table RC-1 Bellingham IAP 19 F / 78 F [S]; MJ / electrical: the 60k multi outdoor unit typically needs a 50 A circuit [U: the name |
| labour | y | 108.5 crew-hours -> **19 days** (set 3, rough 13, trim 1, startup 2). PLACEHOLDER minutes. |
| model + renders | y | 8835-semiahmoo-hvac_app.json · groups {'floors': 39, 'walls': 580, 'equipment': 5, 'terminals': 47, 'hvac': 104} · walls 580 generated centrelines · 3 render(s) |
| draft bid | y | equipment 6 / rough-in 34 / trim 12 lines, 0 option(s) · **3 priced**, 49 labels need a price · fee 5% · prices: none (--no-live) |
| PDF parts list | y | 8835-semiahmoo-hvac.pdf |

## What is measured, what the plan text said, and what is an assumption

**Measured off the traced interior:** every room area, exterior wall length and facing, ceiling and floor exposure, the head and register positions, every run length (L-paths in the crawl and joist bays).

**Read off the plan text:** 2.3 = air leakage 0.6 ACH50 + whole-house ventilation with heat recovery (SRE >= 0.80); 3.6 = air-source CENTRALLY DUCTED heat pump, HSPF2 >= 9.4 (HSPF 11.0); a NEEP cold-climate VCHP where the design temperature is 23 F or below

**From the electrical job:** the bath fans (the electrician supplies them; HVAC ducts them), the dryer and range outlet positions, the outdoor-unit disconnect and air-handler junction.

**Assumed, or answered by job.json rather than the plan:**
- **code** - the energy sheet is the WSU 2021 WSEC-R prescriptive form with the Table R406.2/R406.3 summary
- **system** - Energy sheet: 'X NOTES FOR ENERGY OPTION 3.6 (1 CREDIT) Air-source, centrally ducted heat pump with minimum HSPF2 of 9.4 (HSPF of 11.0) ... In areas where the winter design temperature ... is 23 F or below, an air source centrally ducted heat pump shall be a cold climate variable capacity heat pump as listed on the NEEP qualified product list'; 'Heat Source: Electric heat pump'; the cut sheet is a Mitsubishi MXZ-SM60NAM (5-ton multi-zone Hyper-Heat, rated Non-Ducted // Mix // Ducted). The credit is only earned with DUCTED indoor units - one per storey is ASSUMED (the set names none). The plumbing skill read 'ductless' and the electrical skill an air handler: both were half right.
- **cfa_sf** - A-2/A-3 level tags: Main Level Living 2,120.95 sf + Upper 1,310.38 sf
- **bedrooms** - PRIMARY (main), two BEDROOMs (upper); the DEN, YOGA and ROOM are not bedrooms
- **exclude_rooms** - the 537 sf WORKBENCH / SHOP is garage-side (the sheet's own 'AREA OF FIRST FLOOR & GARAGE = 1992+537'); the two STAIR OPENING regions are voids in the upper floor, open to the main floor - not floor area
- **envelope** - energy sheet prescriptive table: 'VERTICAL FENESTRATION U=0.25, ROOF/CEILING JOIST VAULTED R-60 ADVANCED, WOOD FRAME WALL R-21 BATT INSULATION W/ R-12 CONTINUOUS INSULATION, FLOOR OVER UNHEATED SPACE R-38, SLAB ON GRADE R-10'; option 2.3 = 0.6 ACH50
- **foundation** - crawl ASSUMED for the house (TJI on p16), as the plumbing skill read it
- **ducts** - a multi-zone with ducted indoor units per storey keeps the short duct runs in the floor / ceiling cavities inside the envelope - ASSUMED; if the main-floor unit goes in the crawl, set crawl_vented
- **ventilation** - energy sheet: 'X NOTES FOR ENERGY OPTION 2.3 (2 CREDITS) ... 0.6 air changes per hour' + the VENTS Frigate ERV 150 cut sheet ('the complete whole house ventilation system'); the plan also prints WHOLE HOUSE FAN and two EXHAUST FAN * tags - with the ERV they are local exhaust
- **hood** - A2.1 kitchen: 400 CFM - exactly the M1503.6 threshold (make-up air is required ABOVE 400 cfm); the electrical job wires an interlock anyway
- **dryer** - LAUNDRY on the main floor; 'D' electric per the plumbing job (the plumbing reads a gas dryer stub on another sheet - the finish skill's appliance check flags the conflict)
- **fireplace** - p5 'GAS fp' in the living room (Cascade Natural Gas serves Blaine) - a direct-vent gas fireplace ASSUMED (the modern default; a natural-draft unit would trigger WA M1503.6 make-up air) - the fireplace installer's, not HVAC scope
- install minutes, the day rate and the crew rates are PLACEHOLDERS; every price is blank until Genaro sets it