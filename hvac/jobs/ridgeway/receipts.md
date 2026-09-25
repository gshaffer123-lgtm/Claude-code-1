# Receipts - 340 Ridgeway Pl, Sedro-Woolley WA 98284 (Glenhaven Lakes, unincorporated Whatcom County)

`340-ridgeway-hvac` · permit SFR2025-00214 · generated 2026-09-25 08:09 by `receipts.py` from the files in this folder.

| Step | Ran | Receipt |
|---|---|---|
| sheets | y | p6 = main (plate 10.0 ft); p7 = upper (plate 9.0 ft) · the finish skill's interior.json is the room source |
| plan text read (hvacscan) | y | 36,653 characters, WSEC 2021, 8.0 credits required · credits read: 2.1 (air leakage 2.0 ACH50), 3.7 (DUCTLESS mini-split heat pump, no electr), 4 (heat pump meeting the federal standard (), 5.6 () · system named: **ductless** · 42 schedule openings · 2 conflict(s) |
| loads (hvac_load) | y | heating **25,039 Btuh** (10.3 Btuh/sf) at 19 F (Bellingham IAP, STAND-IN) · cooling 18,820 + 823 latent (8.1 Btuh/sf) · WSU sheet 31,752 · glazing 744.5 sf (the plan's window schedule as read (24 units) - more than th) · 25 rooms · 1 load warning(s) |
| ventilation | y | exhaust 70.3 cfm = Qr 46.9 x Csystem 1.5 (WA M1505.4.3) · load 2,482 Btuh |
| system, unit house | y | ductless: 36k multi (at the electrician's Ductless mini-split outdoor u); 5 heads 9k DINING, 6k OFFICE, 9k MASTER, 6k MEDIA, 6k BED. 2 · capacity at design 33,595 vs load 25,039 Btuh |
| runs | y | line sets 253 ft (concealed) · duct 0 ft · vent / exhaust 47 ft |
| electrical layout read | y | electrical/jobs/ridgeway/devices.json (186 devices): bath fans, the dryer and range outlets, the outdoor-unit disconnect and air-handler junction positions |
| the checker | y | **0 code**, 4 practice, 3 data: 36k outdoor unit (unit house): it sits under the upper storey (BED. 2 above): out of the snow, but se / MASTER: line set 86 ft > the ~82 ft this unit class allows [U - the model's ma / multi-zone: total piping 253 ft > ~229 ft for a 36k multi-zone [U] - split the zon / plan set: ach50: the set prints {1.5: 1, 2.0: 1} -> 1.5 (two values for one requ |
| labour | y | 49.0 crew-hours -> **9 days** (set 3, rough 5, startup 1). PLACEHOLDER minutes. |
| model + renders | y | 340-ridgeway-hvac_app.json · groups {'floors': 25, 'walls': 396, 'equipment': 7, 'terminals': 6, 'hvac': 53} · walls 396 generated centrelines · 3 render(s) |
| draft bid | y | equipment 4 / rough-in 26 / trim 8 lines, 1 option(s) · **3 priced**, 36 labels need a price · fee 5% · prices: none (--no-live) |
| PDF parts list | y | 340-ridgeway-hvac.pdf |

## What is measured, what the plan text said, and what is an assumption

**Measured off the traced interior:** every room area, exterior wall length and facing, ceiling and floor exposure, the head and register positions, every run length (L-paths in the crawl and joist bays).

**Read off the plan text:** 2.1 = air leakage 2.0 ACH50; 3.7 = DUCTLESS mini-split heat pump, no electric resistance in the primary living areas, HSPF2 >= 9 (HSPF 10), sized to heat the ENTIRE dwelling at design temperature; 4 = heat pump meeting the federal standard (Table C403.3.2(2) or (9)); 5.6 = 

**From the electrical job:** the bath fans (the electrician supplies them; HVAC ducts them), the dryer and range outlet positions, the outdoor-unit disconnect and air-handler junction.

**Assumed, or answered by job.json rather than the plan:**
- **code** - A0.1 cover: 'PER WSEC SEC R406 ... FOR MEDIUM DWELLING UNIT : 8.0 ENERGY CREDITS REQUIRED' (2021 WSEC-R)
- **system** - A0.1 SELECTED ENERGY CREDITS: '3.7 HIGH EFFICIENCY HVAC DISTRIBUTION OPTIONS - Ductless mini-split heat pump system with no electric resistance heating in the primary living areas. A ductless heat pump system with a minimum HSPF2 of 9 (HSPF of 10) shall be sized and installed to provide heat to entire dwelling unit at design outdoor air temperature.' + Table 406.2 option 4 (heat pump). READ off the plan.
- **cfa_sf** - A0.1 AREA CALCULATIONS: MAIN FLOOR 1,155 S.F., UPPER FLOOR 1,281 S.F., TOTAL HEATED AREA 2,436 S.F.
- **bedrooms** - A1.2: MASTER BED. and BED. 2 (the main-floor OFFICE and MEDIA are not bedrooms) - the whole-house ventilation rate counts 2
- **envelope** - A0.1 note 8 (Table R402.1.3): ceiling R-60, vaulted R-38, wood frame wall 20+5 or 13+10, floor R-38, slab R-10/4 ft, skylight U-0.50; A0.2 schedule windows U-0.22 / 0.25 (mean 0.24). ACH50: the credit 2.1 says 2.0, general note 3 says 1.5 - the load uses the credit's 2.0 (the looser, so the equipment is not undersized) and the checker lists the conflict
- **foundation** - A1.0: CRAWLSPACE 1,163 SF, 9 foundation vents (vented crawl); TJI floor
- **ventilation** - A1.1/A1.2 legend: '90 CFM FAN MIN. FOR CONT. WHOLE HOUSE OPERATION'; floor plan note 5: 'INSTALL WHOLE HOUSE VENTILATION FAN PER 2021 IRC WA STATE AMENDMENTS ... TABLE M1505.4.3(1)'. Option 2.1 carries no heat-recovery requirement - exhaust-only is compliant
- **hood** - A1.1 kitchen: 'HOOD VENT 36" ... 600 CFM MAKE-UP AIR HOOD UNDER-CABINET' - over 400 cfm, so M1503.6 make-up air, and the sheet asks for it
- **dryer** - LAUNDRY / MUDROOM on A1.1; electric ASSUMED (the electrical job's 30 A dryer circuit; no gas at Glenhaven)
- **fireplace** - A4.1/A4.2 details 'ROOF DETAIL @ FIREPLACE EAVE', 'FLOOR TO WALL DETAIL @ FIREPLACE'; the electrical skill read 'VENTED GAS' on the set. Direct-vent or natural-draft is not stated - a natural-draft unit is what makes WA M1503.6 make-up air mandatory for the 600 cfm hood (the plan asks for it anyway). Not HVAC scope
- install minutes, the day rate and the crew rates are PLACEHOLDERS; every price is blank until Genaro sets it