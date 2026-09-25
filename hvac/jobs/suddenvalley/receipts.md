# Receipts - 312 Sudden Valley Dr, Bellingham WA 98229 (Sudden Valley, unincorporated Whatcom County)

`312-suddenvalley-hvac` · permit SFR2025-00185 · generated 2026-09-25 08:09 by `receipts.py` from the files in this folder.

| Step | Ran | Receipt |
|---|---|---|
| sheets | y | p4 = main (plate 9.1 ft); p6 = upper (plate 9.1 ft) · the finish skill's interior.json is the room source |
| plan text read (hvacscan) | y | 20,574 characters, WSEC 2021, 8.0 credits required · credits read: 2.2 (air leakage 1.5 ACH50 + whole-house vent), 3.6a (air-source CENTRALLY DUCTED heat pump, H), 4c (heat pump meeting the federal standard (), 5.6 () · system named: **ducted** · 23 schedule openings · 1 conflict(s) |
| loads (hvac_load) | y | heating **18,306 Btuh** (12.2 Btuh/sf) at 19 F (Bellingham IAP, STAND-IN) · cooling 10,763 + 902 latent (7.8 Btuh/sf) · WSU sheet 24,190 · glazing 510.8 sf (traced windows (interior.json)) · 19 rooms · 0 load warning(s) |
| ventilation | y | erv 45.0 cfm = Qr 45.0 x Csystem 1.0 (WA M1505.4.3) · load 758 Btuh |
| system, unit house | y | ducted: 24k central (at the electrician's Heat pump condenser (LIVING R); 24k in MECHANICAL ROOM UNDER STAIRS · 13 registers, 2 returns · capacity at design 18,803 vs load 18,306 Btuh |
| runs | y | line sets 26 ft (concealed) · duct 337 ft · vent / exhaust 285 ft |
| electrical layout read | y | electrical/jobs/suddenvalley/devices.json (126 devices): bath fans, the dryer and range outlets, the outdoor-unit disconnect and air-handler junction positions |
| the checker | y | **0 code**, 0 practice, 2 data: plan set: credit 2.2 (heat-recovery ventilation) AND a whole-house exhaust fan a / design temperature: 19 F is a stand-in (WSEC Table RC-1 Bellingham IAP 19 F / 78 F [S]; MJ |
| labour | y | 75.6 crew-hours -> **14 days** (set 3, rough 9, trim 1, startup 1). PLACEHOLDER minutes. |
| model + renders | y | 312-suddenvalley-hvac_app.json · groups {'floors': 19, 'walls': 212, 'equipment': 4, 'terminals': 28, 'hvac': 74} · walls 212 generated centrelines · 3 render(s) |
| draft bid | y | equipment 6 / rough-in 35 / trim 13 lines, 0 option(s) · **3 priced**, 51 labels need a price · fee 5% · prices: none (--no-live) |
| PDF parts list | y | 312-suddenvalley-hvac.pdf |

## What is measured, what the plan text said, and what is an assumption

**Measured off the traced interior:** every room area, exterior wall length and facing, ceiling and floor exposure, the head and register positions, every run length (L-paths in the crawl and joist bays).

**Read off the plan text:** 2.2 = air leakage 1.5 ACH50 + whole-house ventilation with heat recovery (SRE >= 0.70); 3.6a = air-source CENTRALLY DUCTED heat pump, HSPF2 >= 9.4 (HSPF 11.0); 4c = heat pump meeting the federal standard (Table C403.3.2(2) or (9)) or air-to-water; 5.6 = 

**From the electrical job:** the bath fans (the electrician supplies them; HVAC ducts them), the dryer and range outlet positions, the outdoor-unit disconnect and air-handler junction.

**Assumed, or answered by job.json rather than the plan:**
- **code** - A500 / A700: 'WSEC 2021 MEDIUM DWELLING UNIT REQUIRING 8 CREDITS'
- **system** - A500: 'PRIMARY HEATING SOURCE (4c) HEATING SYSTEM USING A HEAT PUMP ... = 3.0 CREDITS' and 'AIR-SOURCE, CENTRALLY DUCTED HEAT PUMP WITH MINIMUM HSPF2 OF 9.4 (HSPF OF 11.0) (3.6a) = 1.0 CREDIT'; the lower floor plan labels a MECHANICAL ROOM UNDER STAIRS ('3.6a & 4c') and a DUCT CHASE. READ off the plan.
- **cfa_sf** - A500 BUILDING SIZE: FIRST FLOOR = 598 SF, SECOND FLOOR = 905 SF, TOTAL HEATED AREA = 1503 SF (the R1 cloud's 601 + 806 disagrees; the table is what the energy reviewer read)
- **bedrooms** - MSTR BEDROOM (upper), BDRM 2 and BDRM 3 (lower)
- **envelope** - A900/A1000: 2X12 DF RAFTERS @ 24 in with R-38 BATT (the whole upper storey is a rafter-vaulted ceiling), 2X6 R-21 + 1 in R-5 CONTINUOUS INSULATION, R-38 floor over the crawl, five SKYLIGHTS on A900; option 2.2 = 1.5 ACH50
- **foundation** - A300: 541.7 SQ FT CRAWLSPACE, Class 1 vapour retarder alternative (vented); the lower-floor supplies run in it, so the ducts are OUTSIDE the envelope unless the crawl is sealed
- **ventilation** - A500 option 2.2: 'REDUCE AIR LEAKAGE TO 1.5 ACH AND A WHOLE HOUSE VENTILATION SYSTEM WITH MINIMUM SENSIBLE HEAT RECOVERY EFFICIENCY OF 0.7 = 1.5 CREDITS'; 'ERV' is labelled on the lower floor plan. CONFLICT: the same sheets also draw a 116 CFM WHF ('WHOLE HOUSE FAN WITH TIMER CAPABLE OF CONTINUOUS OPERATION ... AIRKING AK150LS OR SIMILAR') - an exhaust-only whole-house fan cannot earn 2.2. Bid the ERV as the whole-house system and the WHF as bath exhaust; ask the designer
- **hood** - A700 kitchen 'Range' - no hood CFM on the sheet; 300 cfm ASSUMED (under the 400 cfm make-up air trigger)
- **dryer** - A500: STACKED WASHER/DRYER in the LAUNDRY; electric (the plumbing job: all-electric)
- install minutes, the day rate and the crew rates are PLACEHOLDERS; every price is blank until Genaro sets it