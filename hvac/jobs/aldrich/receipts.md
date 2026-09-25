# Receipts - 4407 Aldrich Rd, Bellingham WA 98226

`4407-aldrich-hvac` · permit SFR2025-00084 · generated 2026-09-25 08:26 by `receipts.py` from the files in this folder.

| Step | Ran | Receipt |
|---|---|---|
| sheets | y | p2 = main (plate 10.0 ft); p3 = upper (plate 10.0 ft) · the finish skill's interior.json is the room source |
| plan text read (hvacscan) | y | 8,451 characters, WSEC 2021, - credits required · credits read: none · system named: **unknown** · 0 schedule openings · 0 conflict(s) |
| loads (hvac_load) | y | heating **33,420 Btuh** (12.3 Btuh/sf) at 19 F (Bellingham IAP) · cooling 11,504 + 1,159 latent (4.6 Btuh/sf) · WSU sheet 35,536 · glazing 388.6 sf (traced windows (interior.json)) · 20 rooms · 0 load warning(s) |
| ventilation | y | exhaust 85.9 cfm = Qr 57.3 x Csystem 1.5 (WA M1505.4.3) · load 2,374 Btuh |
| system, unit house | y | ducted: 42k central (at the electrician's Heat pump condenser (DEN ROOM); 42k in LAUNDRY · 21 registers, 2 returns · capacity at design 32,906 vs load 33,420 Btuh |
| runs | y | line sets 34 ft (concealed) · duct 449 ft · vent / exhaust 28 ft |
| electrical layout read | y | electrical/jobs/aldrich/devices.json (161 devices): bath fans, the dryer and range outlets, the outdoor-unit disconnect and air-handler junction positions |
| the checker | y | **0 code**, 1 practice, 0 data: electrical: the 42k central outdoor unit typically needs a 35 A circuit [U: the na |
| labour | y | 70.8 crew-hours -> **12 days** (set 2, rough 8, trim 1, startup 1). PLACEHOLDER minutes. |
| model + renders | y | 4407-aldrich-hvac_app.json · groups {'floors': 20, 'walls': 224, 'equipment': 3, 'terminals': 29, 'hvac': 68} · walls 224 generated centrelines · 3 render(s) |
| draft bid | y | equipment 5 / rough-in 34 / trim 13 lines, 0 option(s) · **3 priced**, 49 labels need a price · fee 5% · prices: none (--no-live) |
| PDF parts list | y | 4407-aldrich-hvac.pdf |

## What is measured, what the plan text said, and what is an assumption

**Measured off the traced interior:** every room area, exterior wall length and facing, ceiling and floor exposure, the head and register positions, every run length (L-paths in the crawl and joist bays).

**Read off the plan text:** 

**From the electrical job:** the bath fans (the electrician supplies them; HVAC ducts them), the dryer and range outlet positions, the outdoor-unit disconnect and air-handler junction.

**Assumed, or answered by job.json rather than the plan:**
- **jurisdiction** - SFR2025-00084 is a Whatcom County EnerGov case (Build Radar scripts/portal_all.json: Building (Residential) - SFR - New Construction, Issued 2025-10-02) - unincorporated county with a Bellingham mailing address, so Whatcom County PDS issues and inspects. (The electrical job has City of Bellingham; the plumbing job has whatcom.)
- **code** - A-1/A-2/A-3 'TABLE WASHINGTON STATE 2021 ENERGY CODE - OPTION / POINTS / COMPLIANCE PATHWAY' - the table's rows are drawn as linework: no text to read
- **system** - ASSUMED. The WSEC credit table on A-1..A-3 is drawn, not text - hvacscan comes back 'unknown'. The electrical skill's job carries 'air-source heat pump with a ducted air handler' in the LAUNDRY; that is carried here UNREAD. RENDER A-1 AND LOOK before this bid is shown - a ductless credit (3.7) would change every line
- **cfa_sf** - A-2 'Main Floor Area: 1363 ft2', A-3 'Upper Floor Area: 1363 ft2'
- **bedrooms** - BEDROOM 1, BEDROOM 2 (main), MASTER BEDROOM (upper); OFFICE and DEN ROOM are not counted
- **envelope** - A-7 section: R-60 ceiling, R-21+5 walls (continuous insulation outside the sheathing), R-38 floor over the crawl with 6 mil vapour barrier. No air-leakage target is legible: WSEC R402.4.1.2's maximum is used
- **foundation** - A-6: crawl space, 18x24 access, 9 vents
- **ducts** - a ducted system on a vented crawl with the living upstairs: main-floor supplies run in the crawl (outside the envelope - R-8 and the total duct leakage test), upper supplies in the floor cavity
- **ventilation** - A-2: 'House Whole Fan' in Lower Level Living and three 'FAN 96 CFM' tags - exhaust-only whole-house ventilation
- **hood** - no hood CFM on the set; 300 cfm ASSUMED
- **dryer** - LAUNDRY on A-2; electric ASSUMED (all-electric Bellingham norm per the electrical job)
- install minutes, the day rate and the crew rates are PLACEHOLDERS; every price is blank until Genaro sets it