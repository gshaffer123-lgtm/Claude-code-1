# Receipts - 2168 Blind Bay Rd, Shaw Island WA 98286 (San Juan County) - duplex

`2168-blindbay-hvac` · permit BUILD-24-0020 · generated 2026-09-25 08:09 by `receipts.py` from the files in this folder.

| Step | Ran | Receipt |
|---|---|---|
| sheets | y | p8 = main (plate 9.0 ft) · the finish skill's interior.json is the room source |
| plan text read (hvacscan) | **n** | no hvac_scan.json - the set has no text layer here (scanned) or was not read; job.json carries the system |
| loads (hvac_load) | y | heating **24,719 Btuh** (12.4 Btuh/sf) at 26 F (Friday Harbor AP, STAND-IN) · cooling 13,051 + 1,759 latent (7.4 Btuh/sf) · WSU sheet 25,508 · glazing 340.9 sf (traced windows (interior.json)) · 23 rooms · 0 load warning(s) |
| ventilation | y | exhaust 112.9 cfm = Qr 75.3 x Csystem 1.5 (WA M1505.4.3) · load 3,540 Btuh |
| system, unit A | y | ductless: 30k multi (at the electrician's Ductless mini-split outdoor u); 4 heads 6k LIVING A, 6k BED 1, 6k PRIMARY BED, 6k BED 2 · capacity at design 30,117 vs load 12,106 Btuh |
| system, unit B | y | ductless: 24k multi (at the electrician's Ductless mini-split outdoor u); 3 heads 9k DINING, 6k BED 2, 6k BED 1 · capacity at design 24,094 vs load 12,613 Btuh |
| runs | y | line sets 285 ft (concealed) · duct 0 ft · vent / exhaust 44 ft |
| electrical layout read | y | electrical/jobs/shaw/devices.json (181 devices): bath fans, the dryer and range outlets, the outdoor-unit disconnect and air-handler junction positions |
| the checker | y | **0 code**, 6 practice, 2 data: BED 2: a 6k head turns down to ~1,393 Btuh at 26 F against a 1,619 Btuh zone  / BED 1: a 6k head turns down to ~1,393 Btuh at 26 F against a 867 Btuh zone -  / unit A: the 30k outdoor unit carries 30,117 Btuh at 26 F against a 12,106 Btuh / unit B: the 24k outdoor unit carries 24,094 Btuh at 26 F against a 12,613 Btuh |
| labour | y | 65.7 crew-hours -> **11 days** (set 4, rough 5, startup 2). PLACEHOLDER minutes. |
| model + renders | y | 2168-blindbay-hvac_app.json · groups {'floors': 23, 'walls': 256, 'equipment': 11, 'terminals': 7, 'hvac': 60} · walls 256 generated centrelines · 3 render(s) |
| draft bid | y | equipment 5 / rough-in 25 / trim 8 lines, 1 option(s) · **3 priced**, 36 labels need a price · fee 5% · prices: none (--no-live) |
| PDF parts list | y | 2168-blindbay-hvac.pdf |

## What is measured, what the plan text said, and what is an assumption

**Measured off the traced interior:** every room area, exterior wall length and facing, ceiling and floor exposure, the head and register positions, every run length (L-paths in the crawl and joist bays).

**From the electrical job:** the bath fans (the electrician supplies them; HVAC ducts them), the dryer and range outlet positions, the outdoor-unit disconnect and air-handler junction.

**Assumed, or answered by job.json rather than the plan:**
- **code** - 2018 WSEC-R per the plan's energy sheet (p21) - an older set (the electrical and plumbing jobs read it); the approved PDF has NO text layer
- **system** - the energy sheet's credit path is a ductless heat pump - '2018 WSEC option 3.6' as the plumbing job read it and 'DHP' as the electrical job read it; hvacscan cannot confirm it (scanned set). One system PER DWELLING UNIT
- **units** - two mirrored units on one sheet, split at plan x = 70 ft. The west unit carries LIVING A and three bedrooms (PRIMARY BED, BED 1, BED 2; ~1,090 sf traced) = the 3-bed 1,301 sf unit; the east unit (LIVING B, BED 1, BED 2; ~975 sf traced) = the 2-bed 980 sf unit. NOTE: the electrical job's calc_sqft_by_unit names the 980 sf unit 'A' - the reverse of the plan's own LIVING A / LIVING B
- **envelope** - 2018 WSEC-R prescriptive values ASSUMED (the scanned set cannot be read here): ceiling R-49, wall R-21 int, floor R-30, fenestration U-0.30, 5.0 ACH50 - read the energy sheet and correct
- **foundation** - p7/p8: crawl, one CRAWL ACCESS HATCH per unit; slab only at the carport / porches
- **ventilation** - exhaust-only whole-house fan per unit ASSUMED (the 2018 credit path named no HRV)
- **dryer** - no gas on Shaw Island; electric
- install minutes, the day rate and the crew rates are PLACEHOLDERS; every price is blank until Genaro sets it