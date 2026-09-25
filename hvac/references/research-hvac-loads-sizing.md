# HVAC loads, equipment sizing, distribution and ventilation sizing - research digest (agent, 9/25/2026)

Scope: engineering methods for a residential HVAC takeoff/bid engine for new houses in Bellingham / Whatcom County, WA (marine, heating-dominated). Output is intended to be transcribed into Python. Everything below is either (a) read from a primary/authoritative source in this session, (b) taken from a search-engine extract of the named document, (c) computed here from a cited formula, or (d) from manufacturer / trade literature that could NOT be fetched in this session. Each number carries a tag and a URL.

## 0. How to read this file (verification tags) and research constraints

| Tag | Meaning | How much to trust |
|---|---|---|
| [V] | Verified: read directly from the cited document or source code in this session | Use as-is |
| [S] | Search-extract: the value appeared in a web-search extract of the cited document; the full document could not be opened (egress proxy blocked the host) | Probably right; confirm against the document before release |
| [C] | Computed here from a [V] formula; the Python used is shown or described | Reproducible |
| [U] | UNVERIFIED: from manufacturer / trade literature recalled from training data; the host was blocked in this session | Must be checked against the current submittal / manual before production use |

Research constraints (so the caller can judge coverage):
- The session egress proxy blocked energy.wsu.edu, acca.org, ashrae.org, neep.org, energystar.gov, mitsubishicomfort.com, fujitsugeneral.com, daikin, panasonic, broan, zehnder, renewaire, hvi.org, basc.pnnl.gov, wikipedia and most municipal sites (tested with WebFetch and curl). Reachable: github.com (clone/raw), ACCA's public S3 bucket (higherlogicdownload.s3.amazonaws.com), pypi.
- The shared WebSearch budget for the session (200 calls) ran out partway through; later sections lean on GitHub-hosted primary implementations and on ACCA S3 documents.
- The single most useful verified source is NREL's open-source ACCA Manual J 8th edition implementation, OpenStudio-HPXML `hvac_sizing.rb` (commit f28d40e, 11 Sep 2026): https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb . Its code comments cite the Manual J tables and figures (Table 3D-2, 3D-3, 4A, 5A, 5D/5E, A12-6, A12-8, A12-16, A12-17, Table 7). It is an implementation of MJ8, not ACCA's text. Where NREL departs from MJ8 the code says so, and this file notes it.
- WA code text (IRC 2021 with Washington amendments, WAC 51-51) was read from a scraped copy on GitHub: https://github.com/thexqin/us-building-codes-dataset/tree/main/download-v2/washington/irc-2021 (third-party scrape of https://codes.iccsafe.org/content/WARC2021P1 ). The WA code agent should confirm the section numbers.

## 1. Bellingham design conditions (inputs to every calculation)

| Quantity | Value | Tag | Source URL |
|---|---|---|---|
| Heating 99% dry bulb, MJ8 Table 1A, "Bellingham IAP" | 23 F | [V] | https://higherlogicdownload.s3.amazonaws.com/ACCA/c6b38bda-2e04-4f93-bd51-7a80525ad936/UploadedImages/Outdoor-Design-Conditions-1.pdf (Table 1A, Washington, p. 29) |
| Cooling 1% dry bulb / coincident wet bulb, MJ8 Table 1A | 76 F / 64 F | [V] | same |
| Design grains (outdoor minus indoor), indoor 75 F at 55% / 50% / 45% RH | -3 / 4 / 10 gr | [V] | same |
| Daily range class | M (medium, 16-25 F swing) | [V] | same (notes: L < 16 F, M 16-25 F, H > 25 F) |
| HDD65 / CDD50 ratio (used by Manual S "cold climate" test) | 3.38 | [V] | same (last column "HDD65 CDD50 Ratio") |
| Elevation / latitude | 151 ft / 49 N | [V] | same |
| WSEC Table RC-1 heating design temp, Bellingham | 19 F | [S] | https://www.law.cornell.edu/regulations/washington/WAC-51-11R-60100 (WAC 51-11R-60100 Table RC-1) |
| WSEC Table RC-1 cooling design temp, Bellingham | 78 F | [S] | same |
| ASHRAE 2009 (TMY3 DDY) 99.6% heating DB | -7.8 C = 18.0 F | [V] | https://github.com/BuildingComponentLibrary/design-day-components-1/tree/master/lib/components/Design%20Day ("Bellingham Intl Ap_WA_[727976_TMY3]_Annual_Heating_99_6") |
| ASHRAE 2009 99% heating DB | -5.0 C = 23.0 F | [V] | same ("..._Annual_Heating_99") |
| ASHRAE 2009 0.4% / 1% / 2% cooling DB (MCWB) | 79.3 F (65.1) / 76.1 F (63.7) / 73.0 F (62.1) | [V] | same ("..._Annual_Cooling_(DB_MWB)_4 / _1 / _2") |
| ASHRAE 2009 cooling daily range | 9.2 C = 16.6 F (class M) | [V] | same |
| ASHRAE 2009 1% dew point (mean coincident DB) | 15.8 C = 60.4 F (69.3 F) | [V] | same ("..._Annual_Cooling_(DP_MDB)_1") |
| Design wind speed (heating / cooling design day) | 6.1 m/s / 3.6 m/s | [V] | same |
| Manual J indoor design | 70 F heating; 75 F cooling; 50% RH (45% where outdoor grains < 0) | [V] | https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/defaults.rb#L279-L300 ; ACCA ODC guide Ref 1 (URL above) |
| ASHRAE 62.2 weather-and-shielding factor (wsf), station 727976 Bellingham | 0.58 | [V] | https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/data/ashrae622_wsf.csv#L876 |
| Manual J altitude correction factor, ACF = 1 - 0.0000308 x elevation(ft) | 0.995 at 151 ft | [V]/[C] | https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L212 (MJ8 Table 10A) |

Design temperature differences to use:
- WSEC permit path (WSU calculator, Section 2): dT = 70 - 19 = 51 F (RC-1) [S] https://www.law.cornell.edu/regulations/washington/WAC-51-11R-60100 .
- Manual J path: HTD = 70 - 23 = 47 F; CTD = 76 - 75 = 1 F (Table 1A) [V] (ODC URL above). MJ8 says use Table 1A "unless superseded by code" and "do not add a safety factor" [V] (ODC guide, Refs 1 and 3). WSEC R302.2 requires outdoor design temperatures from Appendix Table RC-1 [S] https://codes.iccsafe.org/content/WAERC2021P1/appendix-rc-exterior-design-conditions , so a WA permit Manual J may be run at 19 F (HTD 51). The engine should expose both and record which one it used.
- Cooling in Bellingham is solar- and internal-gain driven: CTD is 1-5 F (76-80 F outdoor) and design grains are about 4 at 50% RH, so conduction, infiltration and latent loads are small (Section 4).

## 2. WSU Energy Program "Simple Heating System Size: Washington State" calculator (WSEC R403.7 path)

### 2.1 What it is
- An Excel calculator published by the WSU Energy Program. It is "based on the Prescriptive Requirements of the 2018 and 2021 Washington State Energy Code (WSEC)" (earlier: 2015 WSEC "and ACCA Manuals J and S"). It "will calculate heating loads only" [S] https://permitbulletin.mercerisland.gov/public/2407-071/SUB1/2018-2021%20heating%20system%20sizing%20worksheet20240326.pdf ; https://energy.wsu.edu/our-work/building-efficiency/washington-state-residential-energy-code-technical-support-and-education/wsec-r-2021-code-forms-and-resources/
- The glazing (window) and door portion "assumes the installed glazing and door products have an area weighted average U-factor of 0.30", and the insulation options are the WSEC prescriptive minimums [S] http://permits.kirklandwa.gov/WebDocs/2018061822/d81cf5af-080e-46f8-93ae-a369d2db2b10.pdf
- Jurisdictions (Seattle, Kirkland, Mercer Island, Bainbridge, and others) accept it with permit submittals [S] https://web.seattle.gov/dpd/edms/GetDocument?id=7446210 ; https://bainbridgewa.gov/DocumentCenter/View/14891/2018-Heating-System-Sizing-Calculator-Instructions
- Instructions PDF (2018 version): https://wpcdn.web.wsu.edu/cahnrs/uploads/sites/60/2026/05/2018-Heating-System-Sizing-Calculator-Instructions.pdf [S] (city dropdown sets the design temperature, e.g. Sammamish 26 F [S] https://www.sammamish.us/media/nmrd4hv2/residential-energy-ventilation-compliance-wsec-2018.pdf ).

### 2.2 Inputs (as laid out on the form) [S]
Project info; location (dropdown, which sets the outdoor design temperature); indoor temperature 70 F; conditioned floor area; average ceiling height; conditioned volume (= CFA x average ceiling height); then one row per component: area (sf) or length (lf) from the user, U-factor or F-factor from a dropdown, and computed UA. Components: glazing and doors; skylights; attic ceilings; single-rafter or joist vaulted ceilings; above-grade walls; floors; slab on grade (by perimeter, F-factor); below-grade walls and slabs; then air leakage from volume; then the duct and equipment multipliers. Sources: https://permitbulletin.mercerisland.gov/public/2512-087/SUB1/2021%20heating%20system%20sizing%20worksheet.pdf ; https://permitbulletin.mercerisland.gov/public/2407-069/SUB1/wsec-r%20heating%20system%20sizing%20worksheet.pdf

### 2.3 Equations (reproduce exactly)
```
dT                         = 70 - T_outdoor_design(location)              # F, indoor fixed at 70 F   [S]
UA_i                       = U_i * A_i            (glazing+doors at U=0.30, skylights, ceilings, walls, floors, below-grade)  [S]
UA_slab                    = F_slab * P_slab      (F-factor, Btu/h-ft-F, times slab perimeter ft)  [S]
Envelope_heat_load         = sum(UA_i) * dT                                                    # Btu/h
Air_leakage_heat_load      = Volume * 0.6 * dT * 0.018                                         # Btu/h  [S]
Building_design_heat_load  = Envelope_heat_load + Air_leakage_heat_load
Building_and_duct_load     = Building_design_heat_load * 1.10   # ducts in unconditioned space  [S]
                           = Building_design_heat_load * 1.00   # ducts in conditioned space (or no ducts)  [S]
Max_heat_equipment_output  = Building_and_duct_load * 1.40      # forced-air furnace  [S]
                           = Building_and_duct_load * 1.25      # heat pump  [S]
```
Sources for the equations: https://permitbulletin.mercerisland.gov/public/2407-071/SUB1/2018-2021%20heating%20system%20sizing%20worksheet20240326.pdf (air leakage "Volume x 0.6 x dT x .018"; duct x1.10 / x1; 1.40 furnace, 1.25 heat pump) [S]; http://permits.kirklandwa.gov/WebDocs/2018061822/d81cf5af-080e-46f8-93ae-a369d2db2b10.pdf [S].
- 0.6 is an air-change rate (ACH). WSU's Builder's Field Guide ch. 7: "For sizing purposes... 0.6 air changes/hour (ACH)... a liberal air infiltration estimate for homes meeting the Washington State Energy Code" [S] https://www.energy.wsu.edu/Documents/BFG%20Chapter%207-Jan2011.pdf
- 0.018 Btu/(ft3-F) is the volumetric heat capacity of air: 0.075 lb/ft3 x 0.24 Btu/lb-F = 0.018 [C]. Volume x ACH x 0.018 x dT equals 1.08 x cfm x dT with cfm = Volume x ACH / 60 [C].
- Output reported: "Building Design Heat Load", "Building and Duct Heat Load" and "Maximum Heat Equipment Output" in Btu/h. Mercer Island example sheets report maximum outputs of 31,600 to 34,282 Btu/h [S] https://permitbulletin.mercerisland.gov/public/2504-058/SUB1/lin%20kicska%20heating%20system%20sizing%20worksheet%2004.01.2025.pdf . Read it as: the selected heating equipment's output must be >= the building-and-duct load and <= the maximum. The sheet does not say at which outdoor temperature a heat pump's "output" is read. Flag this; see Section 5.4 for reading capacity at the design temperature.

### 2.4 U-/F-factor dropdown values seen in WSU worksheet copies
| Component | Option | U or F | Tag | Source |
|---|---|---|---|---|
| Glazing + doors | area-weighted assumption | U-0.30 | [S] | Kirkland PDF above |
| Attic | R-60 | U-0.024 | [S] | https://permitbulletin.mercerisland.gov/public/2512-087/SUB1/2021%20heating%20system%20sizing%20worksheet.pdf |
| Single rafter / joist vaulted | R-38 | U-0.026 | [S] | https://permitbulletin.mercerisland.gov/public/2407-069/SUB1/wsec-r%20heating%20system%20sizing%20worksheet.pdf |
| Single rafter / joist vaulted | R-60 | U-0.017 (as extracted; looks low for a framed vault, check) | [S] | 2512-087 PDF above |
| Above-grade wall | R-21 intermediate framing | U-0.056 | [S] | 2512-087 PDF above |
| Above-grade wall | R-21 int + R-4 ci | U-0.045 | [S] | https://permitbulletin.mercerisland.gov/public/2407-071/SUB1/2018-2021%20heating%20system%20sizing%20worksheet20240326.pdf |
| Above-grade wall | R-21 int + R-12 ci | U-0.032 | [S] | same |
| Floor | R-30 | U-0.029 | [S] | same |
| Floor | R-38 | U-0.025 | [S] | 2512-087 PDF above |
| Slab on grade | R-10 perimeter | F-0.540 | [S] | same |
| Slab on grade | R-10 fully insulated | F-0.360 | [S] | 2512-087 PDF above |
The full dropdown lists (older R-49 attic, below-grade walls, skylight U) were not recoverable. The engine should (a) carry the actual assembly U-factors from the WSEC Appendix default tables or the plan's compliance path, which the WA code agent owns, and (b) default glazing and doors to 0.30 when mimicking the WSU sheet.

### 2.5 Worked example and how it compares with Manual J [C]
Reference house A: 2 storeys, 2,400 sf CFA, 1,200 sf footprint (30 x 40 ft, perimeter 140 ft), 18 ft of exterior wall height, average ceiling 8.5 ft (20,400 ft3), 15% window-to-floor ratio (360 sf), 40 sf doors, walls U-0.056, attic U-0.024, floor over vented crawl U-0.029, ducts inside.
- WSU sheet at dT 51: UA = 400 x 0.30 + 2,120 x 0.056 + 1,200 x 0.024 + 1,200 x 0.029 = 302.3 Btu/h-F, so the envelope load is 15,418 Btu/h. Air leakage: 20,400 x 0.6 x 51 x 0.018 = 11,236 Btu/h. Building load: **26,655 Btu/h (11.1 Btu/h-sf)**. Maximum output: 33,318 Btu/h for a heat pump, 37,316 Btu/h for a furnace.
- Manual J (Section 3 method) for the same house at 3.0 ACH50 with exhaust-only ventilation: **20,454 Btu/h at HTD 47, or 22,293 Btu/h at HTD 51**.
- The WSU sheet runs about 15-50% above Manual J for tight new houses (Section 10.1 cases), almost entirely because 0.6 ACH is roughly 2.3 times the Manual J design infiltration of a 3 ACH50 house (0.26 ACH). Scripts: `references/calc/calc_house.py`; the numbers are reproduced in Section 10.

## 3. ACCA Manual J 8th edition heating load, room by room

All formulas in this section are [V] from NREL's MJ8 implementation (permalinks per item). Units: U in Btu/h-ft2-F, A in ft2, temperatures in F, loads in Btu/h.

### 3.1 Conduction (opaque, glazing, doors)
```
HTM_heat = U * HTD                         # windows, skylights, doors, exterior walls, ceilings, exterior floors
Q = HTM_heat * A_net
HTD = T_in_heat(70) - T_out_design
Partition to an unconditioned space:  Q = U * A * (70 - T_space_design)
```
- Windows: `htg_htm = window_ufactor * mj.htd` https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L749-L753 [V]
- Skylights: effective U includes curb and shaft (U_eff = U_sky + U_curb*A_curb/A_sky + U_shaft*A_shaft/A_sky) https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L860-L875 [V]
- Doors: HTM = (1/R_door) x HTD https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L987-L1010 [V]
- Walls use net area (gross - windows - doors). Foundation walls less than 2 ft below grade are treated as fully above grade https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1036-L1070 [V]
- Attached garage, completely above grade, heating design temperature: T_out + 5 x (fraction of garage under conditioned space) (MJ8 Table 4C, interpolated) https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L366-L372 [V]
- Vented attic: heating temperature = outdoor design temperature https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L345-L360 [V]

### 3.2 Floor over crawlspace (MJ8 Figure A12-6 partition temperature difference, PTDH)
```
Vented / leaky crawl:   PTDH = HTD_adj / (1 + 4*U_floor / (U_wall + 0.11))
Sealed (unvented) crawl or unconditioned basement:  PTDH = U_wall * HTD_adj / (4*U_floor + U_wall)
Q_floor = U_floor * A_floor * PTDH
U_wall = area-weighted U of the crawl's perimeter walls (above- and below-grade parts); HTD_adj = HTD (+25 F if radiant floor)
Floor directly over outdoor air (cantilever): Q = U * A * HTD
```
https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1274-L1345 [V]. Example [C]: U_floor 0.029 and uninsulated crawl walls with U_wall of about 0.25 give PTDH = 0.756 x HTD = 35.5 F at HTD 47.

### 3.3 Slab on grade (edge loss) and basement floors
```
Slab near grade (average depth < 2 ft):  Q = F * P_exposed * HTD_adj        (HTD_adj = HTD + 25 for a radiant slab)
Basement floor (>= 2 ft below grade):    Q = U_bf * A * HTD,
  U_bf = 0.85 * (2k/(pi*w_b)) * [ln(w_b/2 + z_f/2 + k*1.47/pi) - ln(z_f/2 + k*1.47/pi)]   (x0.70 if insulated)
  k = soil conductivity (MJ8 Table 4A default heavy moist soil: R-1.25 per ft, so k = 0.8 Btu/h-ft-F), w_b = shortest side (ft), z_f = depth (ft)
```
https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1370-L1455 (slabs); https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L4958-L4970 (basement floor); https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L236-L254 (soil k) [V].
NREL derives F from a radial soil-path model "calibrated to Table 4A values", averaging path radii of 8-13 ft, with gravel at R-0.65/in and air films R-1.14 https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L4892-L4956 [V]. Computed with that algorithm (4-in slab) [C]:

| Slab insulation | F (k=0.8, MJ8 default soil) | F (k=1.0, RESNET 301 default) | WSEC/WSU default F |
|---|---|---|---|
| Uninsulated | 1.35 | 1.42 | 0.73 [U] (IECC-family default) |
| R-10 vertical edge, 2 ft | 0.48 | 0.53 | 0.54 (R-10 perimeter) [S] |
| R-10 vertical edge, 4 ft | 0.44 | 0.49 | n/a |
| R-10 under entire slab + R-10 edge | 0.38 | 0.41 | 0.36 (R-10 fully insulated) [S] |
| R-15 under entire slab + R-10 edge | 0.34 | 0.37 | n/a |
Script `references/calc/calc_slab.py` reimplements https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L4892-L4956. Insulated-slab F-values agree within about 10% across methods. Uninsulated slabs differ by about 2x; follow the governing method.

### 3.4 Infiltration (heating)
Loads (MJ8 Worksheet E) [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1557-L1559 :
```
Q_infil_heat      = 1.1 * ACF * CFM_heat * HTD
Q_infil_cool_sens = 1.1 * ACF * CFM_cool * CTD
Q_infil_cool_lat  = 0.68 * ACF * CFM_cool * grains
```
**Method A, blower door (MJ8 Tables 5D/5E, the LBL model)** [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1461-L1495
```
Q50 [cfm] = ACH50 * Volume / 60
ELA_in2 [in2 @ 4 Pa] = 0.283316 * (4/50)^n * Q50 = 0.05488 * Q50     (n = 0.65)
Cs = 0.015 * N_stories                                   # stack coefficient
Cw = (0.0065 - 0.00266*(ShieldingClass - 3)) * N_stories^0.4   # wind coefficient; class 1 (exposed) .. 5 (well shielded); default 4 (+1 well-shielded, -1 exposed, +1 urban, -1 rural)
CFM_heat = ELA_in2 * sqrt(Cs*HTD + Cw*15^2)             # 15 mph heating wind
CFM_cool = ELA_in2 * sqrt(Cs*CTD + Cw*7.5^2)            # 7.5 mph cooling wind
Fireplace: +20 cfm heating (one fireplace, average leakiness)
```
ACH50-to-ELA conversion (ANSI/RESNET/ICC 301 Eq. 16, n = 0.65): https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/airflow.rb#L2817-L2819 [V] (SLA = ELA/CFA); 0.05488 = 0.283316 x (4/50)^0.65 [C]. Shielding-class defaults: https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/defaults.rb#L368-L392 [V]. Fireplace: https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1505-L1514 [V].

"Design N-factor" that this gives for Bellingham (N = ACH50 / ACHnat at HTD 47, shielding class 4) [C]:

| Storeys | Cs | Cw | sqrt(Cs*47 + Cw*225) | N = ACH50/ACHnat = 1/(0.05488*sqrt(...)), independent of volume |
|---|---|---|---|---|
| 1 | 0.015 | 0.00384 | 1.253 | 14.5 |
| 2 | 0.030 | 0.00507 | 1.597 | 11.4 |
| 3 | 0.045 | 0.00596 | 1.859 | 9.8 |
So for example 3.0 ACH50 on 2 storeys gives about 0.26 ACH design infiltration; 5.0 ACH50 gives about 0.44 ACH [C] (script `references/calc/calc_house.py`).

**Method B, MJ8 Table 5A default ACH (when no blower door)** [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L4698-L4770 . CFM = ACH x above-grade conditioned volume / 60. Floor-area bins: <=900 | 901-1500 | 1501-2000 | 2001-3000 | >3000 sf. MJ8 descriptors map to NREL's as Tight = "very tight", Semi-Tight = "tight", Average, Semi-Loose = "leaky", Loose = "very leaky" [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/docs/source/workflow_inputs.rst#L1123-L1136

| Single-family, heating ACH | <=900 | 901-1500 | 1501-2000 | 2001-3000 | >3000 |
|---|---|---|---|---|---|
| 1 storey, Tight | 0.21 | 0.16 | 0.14 | 0.11 | 0.10 |
| 1 storey, Semi-tight | 0.41 | 0.31 | 0.26 | 0.22 | 0.19 |
| 1 storey, Average | 0.61 | 0.45 | 0.38 | 0.32 | 0.28 |
| 2 storey, Tight | 0.27 | 0.20 | 0.18 | 0.15 | 0.13 |
| 2 storey, Semi-tight | 0.53 | 0.39 | 0.34 | 0.28 | 0.25 |
| 2 storey, Average | 0.79 | 0.58 | 0.50 | 0.41 | 0.37 |
| Cooling ACH, 1 storey Tight / Semi-tight / Average (2001-3000 sf) | | | | 0.06 / 0.11 / 0.16 | |
| Cooling ACH, 2 storey Tight / Semi-tight / Average (2001-3000 sf) | | | | 0.08 / 0.15 / 0.21 | |
(Semi-loose/Loose rows and the multifamily Table 5B are in the same code block.) A WSEC house tested at 5 ACH50 or less sits between "Tight" and "Semi-tight". Use Method A whenever an ACH50 target exists.

**LBL N-factor (seasonal) guidance.** N = ACH50 / ACHnat. It ranges from 9.8 to 29.4 and depends on climate zone (4 LBL zones), building height (storeys) and wind shielding; origin: M. Sherman, "Estimation of infiltration from leakage and climate indicators", Energy and Buildings 10(1):81-86, 1987 [S] https://www.greenbuildingadvisor.com/question/what-is-n-factor ; https://building-performance.org/bpa-journal/ach50-achnat/ . Commonly reproduced LBL table [U] (the internal pattern is consistent: the normal row is 0.833 x the well-shielded row, exposed is 0.9 x normal, and the 1.5/2/3-storey columns are 0.9/0.8/0.7 x the 1-storey column):

| LBL zone (Normal shielding) | 1 storey | 1.5 | 2 | 3 |
|---|---|---|---|---|
| Zone 1 | 15.5 | 14.0 | 12.4 | 10.9 |
| Zone 2 | 18.5 | 16.7 | 14.8 | 13.0 |
| Zone 3 | 21.5 | 19.4 | 17.2 | 15.1 |
| Zone 4 | 24.5 | 22.1 | 19.6 | 17.2 |
Well-shielded = normal / 0.833 (for example zone 4, 1 storey = 29.4); exposed = 0.9 x normal (for example zone 1, 3 storeys = 9.8) [U]. Which LBL zone western WA falls in was not verified [U]. Do not use seasonal N for design loads. The design-condition N from Method A (11-15 in Bellingham) is lower because design wind (15 mph) and dT are high. The annual-average N implied by ASHRAE 62.2 in Bellingham (wsf 0.58) is N = 1/(0.052 x 0.58 x (H/8.2)^0.4): about 31 for a 1-storey house (H 10 ft) and about 24 for 2 storeys (H 19 ft) [C] (formula in Section 8.2).

### 3.5 Ventilation load (with and without heat recovery)
[V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1516-L1575 and https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L3725-L3790
```
q_sup = supply + balanced + ERV/HRV cfm;  q_exh = exhaust + balanced + ERV/HRV cfm
q_imb = q_exh - q_sup                   # > 0 means exhaust-dominant (house depressurized)
q_oa  = q_sup (excluding CFIS)          # outdoor air delivered directly to the space
Net infiltration combined with imbalance (ICFM from 3.4):
  q_imb = 0 : NCFM = ICFM
  q_imb > 0 : NCFM = (ICFM^1.5 + q_imb^1.5)^0.67                      # exhaust-only systems
  q_imb < 0 : NCFM = (ICFM^1.5 - |q_imb|^1.5)^0.67, or 0 if ICFM < |q_imb|   # supply-only
Q_infil_heat = 1.1 * ACF * NCFM * HTD
Q_vent_heat  = 1.1 * ACF * q_oa * (1 - E_sens) * HTD                 # E_sens = apparent sensible effectiveness (ASE)
Q_vent_cool_sens = 1.1 * ACF * q_oa * (1 - E_sens) * CTD ;  Q_vent_cool_lat = 0.68 * ACF * q_oa * (1 - E_lat) * grains
```
- Exhaust-only continuous fan: q_oa = 0; the fan's cfm enters only through NCFM.
- HRV/ERV: balanced, so q_imb = 0 and the load is 1.1 x q x (1 - ASE) x HTD. NREL converts HVI/CSA 439 SRE (which excludes fan heat) to ASE (which includes supply-fan heat) with CSA 439 Clause 9.3.3.1 Eq. 12 at 0 C outdoor and 22 C exhaust https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/airflow.rb#L1804-L1845 [V]. Prefer the HVI-listed ASE at 32 F if available; otherwise ASE is roughly SRE plus a few points [U].
- Allocation to rooms: ventilation load by floor area (zone floor area / CFA); infiltration by exposed gross wall area (room exposed wall / total exposed wall) https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1577-L1600 [V].

### 3.6 Duct losses and gains
- Ducts in conditioned space: regain factor 1.0, so duct load = 0 [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1765-L1832 .
- Regain factors for ducts in unconditioned space (fraction of duct loss returned to the house; MJ8 p. 204 and Walker 1998) [V] same URL:

| Duct location | Condition | f_regain |
|---|---|---|
| Vented attic (also unvented attic in NREL) | - | 0.10 |
| Garage | - | 0.05 |
| Outside / roof deck | - | 0.0 |
| Vented crawl | floor insulated, walls uninsulated | 0.12 |
| Vented crawl | floor and walls insulated | 0.17 |
| Vented crawl | floor uninsulated, walls insulated | 0.66 |
| Vented crawl | floor and walls uninsulated | 0.50 |
| Unvented crawl | floor and walls insulated | 0.30 |
| Unvented crawl | floor insulated, walls uninsulated | 0.16 |
| Unvented crawl | floor uninsulated, walls insulated | 0.76 |
| Unvented crawl | floor and walls uninsulated | 0.60 |
| Unconditioned basement | ceiling insulated | 0.30 |
| Unconditioned basement | ceiling uninsulated, walls insulated / uninsulated | 0.75 / 0.50 |
- Two duct-load methods [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1846-L2020 : (1) MJ8 Table 7 default duct factors: duct heat loss = EHLF x (heating load before ducts), where EHLF = base heat loss factor (by table 7A-7P, floor area 1,000-3,000 sf and outdoor temperature -10 to 40 F) x R-value correction (R-2/4/6/8) x leakage correction (0.06/0.06 "extremely sealed" to 0.35/0.70 "not sealed" supply/return CFM25 per 100 sf); for example 7A-R at 20 F and 2,000 sf has a base factor of 0.12 (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L2047); (2) the ASHRAE 152 delivery-effectiveness iteration, used when no Table 7 input is given. Simplified engine rule: ducts inside means 0. Ducts in a vented attic or crawl: use Table 7 or, as a screening fallback, the WSU x1.10 multiplier from Section 2 [S].
- Blower heat (cooling only, if the equipment performance data does not already include it): MJ8 Section 25, default 1,707 Btu/h (500 W) [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/docs/source/workflow_inputs.rst#L3580-L3581
- Duct-load allocation to rooms: proportional to each room's load [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1985-L2019).

### 3.7 Simplified, defensible room-by-room procedure (from polygons)
Inputs per room: floor polygon (area), storey, ceiling height, list of exterior wall segments (length, azimuth, wall assembly), windows and doors (area, azimuth, U, SHGC, overhang depth and height above the window), ceiling adjacency (vented attic / roof / conditioned), floor adjacency (crawl vented/unvented / slab / garage / conditioned), slab exposed perimeter, below-grade wall area. Steps:
1. `A_gross_wall = sum(seg.length) * wall_height` (use floor-to-floor height for multi-storey walls so rim joists are included). `A_net_wall = A_gross_wall - A_win - A_door`.
2. `A_ceiling = floor_area` for flat ceilings under an attic; `= floor_area / cos(pitch)` for vaulted ceilings.
3. `A_floor = floor_area` if the room is on the lowest floor over a crawl or garage; slab: `P_exposed = sum(exterior segment lengths on the slab)`.
4. Heating: `Q_room = sum(U*A)*HTD + U_floor*A_floor*PTDH + F*P*HTD + Q_infil_bldg*(A_gross_wall_room/A_gross_wall_bldg) + Q_vent_bldg*(floor_area/CFA) + Q_duct_bldg*(Q_room_pre/Q_bldg_pre)`.
5. The block (whole-house) heating load is the sum of room loads; there is no heating diversity.
6. Cooling: see Section 4. Occupants and appliances default to allocation by floor area (NREL), or are assigned (occupants to bedrooms and living room, appliances to the kitchen). Room fenestration uses the "standard" procedure (average + AED excursion) for single-zone central systems and the "peak" procedure for multi-zone/ductless systems [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/docs/source/workflow_inputs.rst#L928-L931
Room-level example [C]: a 12x12 ft corner bedroom in house A (2 exterior walls, 204 sf gross wall, 20 sf window, attic above, crawl below) comes to about 1.6 kBtu/h heating at HTD 47: window 263 + walls 484 + ceiling 162 + floor 148 + infiltration share 580. That is why 6k mini-split heads (Section 6) are usually oversized for bedrooms in new WA houses.

## 4. Cooling load for Bellingham (simplified Manual J / HTM method)

### 4.1 Glass: MJ8 average-load-procedure heat transfer multiplier
Formula [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L783-L795 :
```
HTM_cool(dir) = PSF(lat, dir) * CLF(dir, shaded?) * SHGC * ISC / 0.87  +  U * CTD      [Btu/h-ft2]
Q_glass = HTM_cool * A_glass   (window esc: interior insect screen x(1 - 0.1*coverage); exterior x(1 - 0.2*coverage); solar screen/film: ESC 0.25 on the solar part)
Overhang: shade-line depth z = SLM(lat, dir) * overhang_depth; shaded fraction uses HTM(N) (north-facing HTM), unshaded uses HTM(dir)
Skylight: HTM = (cos(tilt)*PSF_h*CLF_h + sin(tilt)*PSF_dir*CLF_dir) * SHGC*ISC/0.87 + U_eff*(CTD + 15)
```
PSF = MJ8 Table 3D-2 peak solar factor; CLF = Table 3D-3 average cooling-load factor; ISC = interior shading coefficient (Table 3D-4); SLM = Table 3E-1 shade-line multipliers (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L661-L671); skylight formula https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L914 [V].

MJ8 Table 3D-2 PSF (Btu/h-ft2), latitude columns 28/34/40/46/52/60 N [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L673-L682), interpolated here to Bellingham 48.8 N [C]:

| Direction | 46 N | 52 N | 48.8 N (use) |
|---|---|---|---|
| N | 34 | 32 | 33.1 |
| NE / NW | 130 | 124 | 127.2 |
| E / W | 213 | 208 | 210.7 |
| SE / SW | 205 | 212 | 208.3 |
| S | 173 | 193 | 182.3 |
| Horizontal | 230 | 208 | 219.7 |

MJ8 Table 3D-3 average CLF [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L612-L619):

| | N | NE | E | SE | S | SW | W | NW | Horizontal |
|---|---|---|---|---|---|---|---|---|---|
| No internal shading | 0.48 | 0.40 | 0.38 | 0.35 | 0.24 | 0.35 | 0.38 | 0.40 | 0.68 |
| With internal shading (ISC < 1) | 0.29 | 0.32 | 0.32 | 0.29 | 0.18 | 0.29 | 0.32 | 0.32 | 0.52 |

Table 3D-4 ISC, double-pane low-SHGC low-e ("2P Low-e Option 3", SHGC < 0.38) [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L5058-L5071): dark/medium/light blinds 0.85/0.76/0.66; dark/medium/light shades 0.87/0.77/0.66; dark/medium/light curtains 0.89/0.78/0.67. Half-open blinds x1.175 (Table 3D-4 note 3). Effective ISC = f_covered x ISC + (1 - f_covered). Default when the plan says nothing: light curtains, 50% summer coverage (ANSI/RESNET/ICC 301-2022), so ISC = 0.5 x 0.67 + 0.5 = 0.835 [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/defaults.rb#L1640-L1670 . Caveat [V]: when the number of glass layers is not given, NREL infers the Table 3D-4 row from U and SHGC, and U < 0.30 is treated as triple-pane ("3P Heat Absorbing" when SHGC < 0.445). That row's light-curtain ISC is 0.75, so the effective ISC is 0.875 at 50% coverage https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L4974-L5010 . Pass glass layers explicitly for double-pane U-0.28 units.

Computed glass HTMs for Bellingham (lat 48.8, CTD = 1 F for 76 F outdoor, or 5 F for 80 F), Btu/h per ft2 of rough-opening glass [C] (script `references/calc/calc_mj.py`):

| Glazing / shading | CTD | N | NE | E | SE | S | SW | W | NW |
|---|---|---|---|---|---|---|---|---|---|
| SHGC 0.25, U 0.28, no shading (ISC 1.0) | 1 | 4.8 | 14.9 | 23.3 | 21.2 | 12.9 | 21.2 | 23.3 | 14.9 |
| SHGC 0.25, U 0.28, no shading | 5 | 6.0 | 16.0 | 24.4 | 22.3 | 14.0 | 22.3 | 24.4 | 16.0 |
| SHGC 0.25, U 0.28, default ISC 0.835 | 1 | 2.6 | 10.0 | 16.5 | 14.8 | 8.2 | 14.8 | 16.5 | 10.0 |
| SHGC 0.28, U 0.28, no shading | 1 | 5.4 | 16.7 | 26.0 | 23.7 | 14.4 | 23.7 | 26.0 | 16.7 |
| SHGC 0.28, U 0.28, default ISC 0.835 | 1 | 2.9 | 11.2 | 18.4 | 16.5 | 9.1 | 16.5 | 18.4 | 11.2 |
| SHGC 0.28, U 0.28, default ISC 0.835 | 5 | 4.0 | 12.3 | 19.5 | 17.6 | 10.2 | 17.6 | 19.5 | 12.3 |
| SHGC 0.30, U 0.30, no shading | 1 | 5.8 | 17.8 | 27.9 | 25.4 | 15.4 | 25.4 | 27.9 | 17.8 |
| SHGC 0.30, U 0.30, no shading | 5 | 7.0 | 19.0 | 29.1 | 26.6 | 16.6 | 26.6 | 29.1 | 19.0 |
| SHGC 0.30, U 0.30, default ISC 0.835 | 1 | 3.1 | 12.0 | 19.7 | 17.7 | 9.7 | 17.7 | 19.7 | 12.0 |
| SHGC 0.30, U 0.30, light curtains fully closed (0.67) | 1 | 2.5 | 9.7 | 15.9 | 14.3 | 7.9 | 14.3 | 15.9 | 9.7 |
Flat skylight (SHGC 0.25-0.30, U 0.50, no shading): 51-62 Btu/h-ft2 [C] (formula above). Heating HTM for comparison: U 0.28 gives 13.2 (HTD 47) or 14.3 (HTD 51) Btu/h-ft2 [C].

Adequate Exposure Diversity (AED) [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L966-L980): compute hourly fenestration loads for 8am-8pm using Table A11-5/A11-6 hourly CLFs and Table A11-3 hourly temperature adjustments. `DAL = mean(hourly)`, `ELL = 1.3*DAL`, `excursion = max(0, max(hourly) - ELL)`, which is added to the glass load for a single-zone system. The "peak" procedure uses max(hourly) for rooms served by zoned or ductless equipment. A plan with glass concentrated on west or east trips the excursion; the engine should implement the hourly tables (all present in https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L620-L650) rather than the averages alone.

### 4.2 Opaque surfaces
- Exterior walls [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1083-L1115): `CLTD = CLTD_base(ASHRAE wall group) * color_mult`; color multiplier light 0.65 / medium 0.83 / dark 1.0 (MJ8 Table 4B notes; light = solar absorptance <= 0.5, medium <= 0.75). If CTD >= 10: `CLTD += (T_out - 95) + DR_adj` with DR_adj = +4 (low), 0 (medium), -5 (high) (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L196). If CTD < 10 (Bellingham): `CLTD = max(CLTD + (CTD - 20 - DR_adj), 0)` (MJ8 A12-18/A12-19). Base CLTD by ASHRAE group: G 38.0, F-G 34.95, F 31.9, E-F 29.45, E 27.0, D-E 24.5, D 22.0, C-D 21.25, C 20.5, B-C 19.65, B 18.8 (MJ8 Figure A12-8). Wood-stud, non-masonry walls: U <= 0.048 is group J -> ASHRAE B-C; U <= 0.051 is I -> C; U <= 0.059 is H -> C-D (so an R-21 wall at U-0.056 is C-D) (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L4434-L4690).
  - Bellingham results [C]: a medium-color R-21 wall has CLTD = max(17.64 + CTD - 20, 0), which is 0 F at CTD 1 and 2.6 F at CTD 5, so HTM = 0 to 0.15 Btu/h-ft2. Dark color: 2.3-6.3 F, so HTM 0.13-0.35. Walls are negligible in cooling.
- Ceiling under a vented attic: treated as a partition to the attic at `T_attic = base + (T_out - 95) + DR_adj`, where base is 130 F for dark or medium-dark asphalt shingles, 120 F for lighter shingles or wood shakes, 95-130 F for metal or tile by color, and 10 F lower with a radiant barrier (MJ8 Figure A12-14) [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L398-L513). Bellingham [C]: at 76 F outdoor with dark shingles T_attic = 111 F, so HTM = U x 36; U-0.024 gives 0.86 Btu/h-ft2 and U-0.026 gives 0.94.
- Roof/ceiling sandwich (vaulted, no attic), MJ8 Figure A12-16 base CLTD by assembly R: <=R-6 50, <=R-13 45, <=R-15 38, <=R-21 31, <=R-30 30, >R-30 27 F; x0.83 for medium/light shingles; then + (T_out - 95) + DR_adj [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1163-L1225). Bellingham [C]: R-38+ vault, dark: CLTD = 27 - 19 = 8 F at 76 F outdoor, so HTM = 8/38, about 0.21 Btu/h-ft2.
- Doors [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L988-L995): CLTD = CTD + 15 (low DR) / CTD + 11 (medium) / CTD + 6 (high). Bellingham (M): 12-16 F, so a U-0.20 door gives HTM 2.4-3.2.
- Floors over crawl or outdoors [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1244): HTM = U x (CTD - 5 + DR_adj), which is negative or zero in Bellingham; take 0. Slabs: no cooling load.

### 4.3 Infiltration, ventilation and latent (marine climate)
- Sensible: 1.1 x ACF x CFM_cool x CTD, with CFM_cool from Section 3.4 at 7.5 mph wind. At CTD 1-5 F this is about 35-200 Btu/h for a 3 ACH50 house [C].
- Latent: 0.68 x ACF x CFM x grains. Bellingham has 4 grains at 50% RH (MJ8 Table 1A), so infiltration latent is about 50-170 Btu/h for 2,000-3,000 sf houses at 2.5-4 ACH50 [V]/[C]. Manual J's indoor RH defaults to 45% where outdoor grains are below 0 (dry summer); Bellingham shows -3 gr at 55% and +4 at 50% [V] (ODC URL in Section 1; https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/defaults.rb#L289-L300).
- Occupant latent (200 Btu/h each) dominates latent. The Manual J sensible heat ratio (JSHR) of new Bellingham houses computes to 0.89-0.92 [C], below the 0.95 threshold for Manual S's "dry" sizing condition (Section 5.1).

### 4.4 Internal gains
- Occupants: 230 Btu/h sensible + 200 Btu/h latent each; occupants = Nbr + 1 (or the actual resident count if larger) [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1604-L1618 ; https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/defaults.rb#L345-L356
- Appliances and plug loads (sensible), NREL's "per Manual J" default: 2,400 Btu/h with one refrigerator and no freezer; 3,600 Btu/h with two refrigerators or a refrigerator plus freezer. Latent default 0 [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/defaults.rb#L308-L318 ; https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/docs/source/workflow_inputs.rst#L854-L857
- CONFLICT: the task brief's "1,200-1,600 Btu/h per Manual J" corresponds to older MJ8 guidance [U]. NREL's current MJ8 implementation uses 2,400/3,600. Recommendation: default to 2,400 Btu/h (put 1,200 in the kitchen and spread the rest over the living areas), make it a parameter, and cite the MJ8 version used.

### 4.5 Supply-air temperatures used to derive airflow [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1653-L1690)
Cooling leaving-air temperature: 54 F if JSHR < 0.80; linear 54-58 F for JSHR 0.80-0.85; 58 F if JSHR >= 0.85. Heat-pump heating supply: 105 F; furnace: 120 F. Airflow check: `cfm_cool = Q_sens / (1.1 * ACF * (75 - LAT))`; `cfm_heat = Q_heat / (1.1 * ACF * (SAT - 70))` [C].

### 4.6 Bellingham cooling results for the reference houses [C]
| House | Cooling total (Btu/h) | Btu/h-sf | ft2 per ton | Cooling / MJ heating |
|---|---|---|---|---|
| A 2,400 sf, 2 storeys, 15% glass, CTD 1 | 9,761 (8,875 sens + 885 lat) | 4.1 | 2,951 | 0.48 |
| A at CTD 5 (80 F) | 10,808 | 4.5 | 2,665 | 0.53 |
| B 1,800 sf, 1 storey slab, 15% glass | 9,144 | 5.1 | 2,362 | 0.47 |
| C 3,000 sf, 20% glass, CTD 3 | 14,129 | 4.7 | 2,548 | 0.49 |
| D 2,000 sf, 12% glass | 8,089 | 4.0 | 2,967 | 0.54 |
Breakdown for A: glass 45%, internal 34%, ceiling 11% (script `references/calc/calc_house.py`). Windows were split equally over N/E/S/W; unequal orientation (for example a west-facing view wall) raises cooling mainly through the AED excursion.

## 5. Manual S equipment selection for heat pumps

### 5.1 ACCA Manual S (ANSI/ACCA 3, 2023 3rd edition), size-factor limits [V]
Source: ACCA public-review draft "Proposed Addendum c to ... ANSI/ACCA Manual S - 2023, Addendum a - 2024, and Addendum b - 2024" (Mar 2025) https://higherlogicdownload.s3.amazonaws.com/ACCA/c6b38bda-2e04-4f93-bd51-7a80525ad936/UploadedImages/Manual_S_Addendum_C_03062025.pdf . The draft's underline and strikethrough were lost in text extraction; the values below are taken from its numbered explanatory text, which is unambiguous. Confirm against the adopted edition.
Definitions: Size factor = capacity / load. Heating size factor (HSF) = heat-pump heating capacity (at the winter design condition) / heating load. HSF(47 F) = heat produced at maximum compressor capacity at 47 F / heating load at the winter design condition.

| Sizing condition | Equipment | Limits |
|---|---|---|
| Standard | single-speed, total cooling load <= 24,000 Btu/h | 0.90 <= total cooling SF <= 1.20; sensible SF >= 0.90; latent SF >= 1.00 |
| Standard | single-speed, total cooling load > 24,000 Btu/h | 0.90 <= total SF <= 1.15; sensible >= 0.90; latent >= 1.00 |
| Standard | two-speed | 0.90 <= total SF <= 1.25; sensible >= 0.90; latent >= 1.00 |
| Dry (JSHR >= 0.95) | single-speed | total capacity / (total load + 6,000 Btu/h) <= 1.00; total SF >= 0.90; sensible >= 0.90; latent >= 1.00 |
| Dry | two-speed | minimum-compressor total SF <= 1.15; sensible >= 0.90; latent >= 1.00 |
| Two-speed HP heating condition (JSHR >= 0.95 or active dehumidification) | two-speed HP | standard cooling limits, plus min-compressor cooling SF <= 0.80; HSF <= 1.20; min-compressor HSF <= 0.80; HSF(47 F) <= 1.50 |
| Variable capacity, simplified (single-split ducted or ductless, and multi-split outdoor units) | cooling-only | 0.90 <= total SF <= 1.30; latent SF >= 1.00 |
| Variable capacity, simplified | heat pump | cooling-only limits, plus HSF >= 1.00 and min-compressor HSF <= 0.80 |
| Variable capacity, advanced | heat pump | min-compressor cooling SF <= 0.80; min-compressor latent SF >= 1.00; HSF >= 1.00; min-compressor HSF <= 0.80 (no maximum on total cooling SF) |
| Variable capacity, advanced dry (JSHR >= 0.95 or active dehumidification) | heat pump | min-compressor cooling SF <= 0.80; HSF >= 1.00; min-compressor HSF <= 0.80; HSF(47 F) <= 1.50 |
Supplemental and emergency electric resistance heat (Tables N1.16.3.1-3) [V], same URL:
- Supplemental heat load = heating load minus heat-pump capacity at the design condition (thermal balance point method). If that load is <= 15,000 Btu/h, the heater may be at most 5 kW. If it is >= 15,000 Btu/h, 0.95 <= heater Btu/h / load <= 1.75.
- Emergency heat load = 85% of the total heating load, with the same 5 kW / 0.95-1.75 limits.
- Sole-source resistance heat: same limits against the full heating load.
- Zoned systems: use the minimum possible excess capacity against the MJ8 block load (N2.2).
Implication for Bellingham: a variable-speed heat pump may be sized to the heating load. HSF >= 1.00 at the design temperature is mandatory in the simplified and advanced paths. Because cooling is about half of heating (Section 4.6), HSF >= 1 usually puts total cooling SF at about 2.0-2.5 (house A: a ducted ccASHP with capacity at 23 F equal to the load has a nominal rating of about 25k against a 9.8k cooling load) [C], which fails the simplified 1.30 cap, so the engine should use the advanced path: min-compressor cooling capacity <= 0.80 x cooling load and min-compressor latent >= latent load. The Washington IRC exception below also relaxes Manual S limits for variable and multistage equipment.

### 5.2 Washington IRC M1401.3 exception (sizing not limited to Manual S) [V]
"Heating and cooling equipment... shall be sized in accordance with ACCA Manual S or other approved sizing methodologies based on building loads calculated in accordance with ACCA Manual J... Exception: ...sizing shall not be limited to the capacities determined in accordance with ACCA Manual S where... (1) the specified equipment utilizes multistage technology or variable refrigerant flow technology and the loads calculated... are within the range of the manufacturer's published capacities for that equipment; or (2) the manufacturer's published capacities cannot satisfy both the total and sensible heat gains... and the next larger standard size unit is specified." https://github.com/thexqin/us-building-codes-dataset/blob/main/download-v2/washington/irc-2021/chapter-14-heating-and-cooling-equipment-and-appliances.csv (M1401.3; WA code agent to confirm against WAC 51-51 and WSEC R403.7).
Engine rule: for inverter equipment, require min_capacity(design condition) <= load <= max_capacity(design condition), in both heating and cooling.

### 5.3 Manual S 2014 rules (as implemented by NREL) and the older "cold climate" allowances
- Cooling-sizing limits: single-speed 1.15, two-stage 1.20, variable-speed 1.30 x total cooling load; undersize limit 0.90 [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1725-L1740
- Heat pump whose heating need exceeds its cooling size (NREL "ACCA" method; Manual S 2014) [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L3683-L3700): if HDD65/CDD50 < 2.0 (mild winter) or JSHR < 0.95, capacity = min(oversize_limit x cooling load, capacity needed for heating). If HDD65/CDD50 >= 2.0 and JSHR >= 0.95 ("cold winter, no latent load", the "add a ton" rule), capacity = min(cooling load + 15,000 Btu/h, capacity needed for heating). Bellingham: HDD65/CDD50 = 3.38 [V], but JSHR is about 0.91 [C], so the 15,000 Btu/h allowance does not apply under this logic.
- Secondary summaries of Manual S 2014 [S]: "Heat pumps in a heating dominant climate are allowed to be 125% of the cooling" https://www.energyvanguard.com/attachment/acca-manual-s-air-conditioner-sizing-limits/ ; "Cold Climate Heat-Pumps can be sized to the total cooling building load + 15,000 btu/hr maximum... single-stage, two-stage, and variable capacity"; "total heating capacity... less than or equal to 140% of the designed total heating load" (furnaces) https://www.hvacproblog.com/top_5_changes_to_acca_manual_s . These disagree in detail with each other and with NREL's code; the 2023 edition (5.1) supersedes them.
- NREL's other sizing options (useful as engine modes) [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/docs/source/workflow_inputs.rst#L796-L815 : "HERS" (nominal capacity >= max(heating load, sensible cooling load)) and "MaxLoad" (nominal capacity sized so that capacity at the design temperature meets the larger of heating and cooling loads, so no backup is needed). For switchover or lockout temperatures above 25 F, NREL sizes the heat pump at min(switchover, 25 F) (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L3643).

### 5.4 Reading capacity at the design temperature
- With only 47 F and 17 F ratings, NREL interpolates linearly: `cap(T)/cap47 = 1 - (1 - q17)/(47 - 17) * (47 - T)`, where q17 = cap17/cap47 [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L2968-L2998 . Default q17 = 0.626 for single/two-stage and 0.69 for variable-speed and mini-split [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/docs/source/workflow_inputs.rst#L2851 ; https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/docs/source/workflow_inputs.rst#L2948 .
  - [C]: q17 = 0.626 gives 0.701 at 23 F and 0.651 at 19 F; q17 = 0.69 gives 0.752 at 23 F and 0.711 at 19 F.
- With manufacturer extended data (NEEP-style 47/17/5 F at min/rated/max), interpolate the maximum-capacity column between the bracketing temperatures and extrapolate below 5 F from the last two points. Use "maximum" capacity for variable-speed units and "nominal" for single/two-stage [V] (same function; data rules at https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/docs/source/workflow_inputs.rst#L3280-L3365). Also apply an indoor-temperature correction if the data were not taken at 70 F indoor (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L2953-L2958).
- Typical cold-climate heat-pump normalized performance (fraction of rated 47 F capacity), from the ResStock "Cold Climate Heat Pump" detailed-performance options [V] https://github.com/NREL/resstock/blob/dd25369f41a83a0767aefeeac0b6f8a0b0edd649/resources/options_lookup.tsv#L9679-L9680 :

| | 47 F max | 17 F max (nom) | 5 F max | -15 F max | COP 47 / 17 / 5 / -15 F (max) | min-speed capacity 47 / 17 / 5 F |
|---|---|---|---|---|---|---|
| ccASHP non-ducted | 1.216 | 0.913 (0.751) | 0.867 | 0.630 | 3.03 / 2.20 / 2.07 / 1.52 | 0.300 / 0.203 / 0.167 |
| ccASHP ducted | 1.028 | 0.766 (0.745) | 0.688 | 0.507 | 3.37 / 2.33 / 1.98 / 1.49 | 0.308 / 0.353 / 0.371 |
  - [C]: non-ducted max capacity is 0.974 x nominal at 23 F and 0.933 at 19 F; ducted is 0.818 at 23 F and 0.783 at 19 F.
- NEEP cold-climate ASHP specification (v4.0) and ENERGY STAR v6.1 cold-climate criteria: COP >= 1.75 at 5 F at maximum capacity; max capacity at 5 F / rated capacity at 47 F >= 70%; variable-capacity compressor; plus HSPF2/SEER2 minimums that differ for ducted and ductless [U] https://neep.org/heating-electrification/ccashp-specification-product-list ; https://www.energystar.gov/products/heat_pumps_air_source (not fetched; confirm the current thresholds and version).
- Hyper-heat mini-split families, manufacturer claims [U] (all hosts blocked; read the model's submittal "extended heating capacity" table):

| Family | Claim | Low-ambient limit | Where to verify |
|---|---|---|---|
| Mitsubishi M-Series Hyper-Heating INVERTER (H2i), e.g. MSZ-FS / MSZ-GL heads with MUZ-...NAH outdoor units | 100% of rated heating capacity at 5 F; capacity also listed at 17 F and -13 F | heats to -13 F (some H2i-plus models lower) | https://www.mitsubishicomfort.com (submittals on https://mylinkdrive.com) |
| Fujitsu Halcyon XLTH (e.g. ASU9/12/15RLS3(Y) + AOU9/12/15RLS3H) | 100% heating capacity at 5 F (9k/12k/15k) | heats to -15 F | https://www.fujitsugeneral.com/us/ |
| Daikin Aurora (low-ambient single-zone) | continuous heating to -13 F; reduced but high capacity at 5 F (model-specific) | -13 F | https://daikincomfort.com |
  - Cross-check with the WA code digest (`research-hvac-code.md`, same folder): WSEC-R 2021 credit option 3.3 requires a NEEP-listed cold-climate heat pump where the Appendix RC winter design temperature is <= 23 F [S] https://www.kirklandwa.gov/files/sharedassets/public/v/3/development-services/pdfs/building-pdfs/wsec-r-plan-sheet.pdf . Bellingham's RC-1 value is 19 F, so ducted heat pumps claiming that credit must be NEEP ccASHP-listed.
  - Engine rule: never use nominal heating capacity. Store the 47/17/5 F min/max table per model and interpolate to 23 F (or 19 F). NEEP's ccASHP list (https://ashp.neep.org) is the preferred machine-readable source [U].

### 5.5 Balance point, supplemental and backup heat
```
L(T)   = UA_eff * (70 - T)      with UA_eff = Q_heat_design / HTD   (ignoring internal gains is conservative)
C(T)   = interpolated heat-pump capacity (max column) at outdoor T
T_bal  : L(T_bal) = C(T_bal)                       # thermal balance point
Q_supp = max(0, L(T_design) - C(T_design))         # Manual S supplemental heat load
heater_kW: if Q_supp <= 15,000 Btu/h -> kW <= 5 ;  else 0.95 <= kW*3412/Q_supp <= 1.75
emergency (if required): Q_emerg = 0.85 * Q_heat_design, same limits
```
Sources: Manual S Addendum c tables N1.16.3.x [V] (URL in 5.1); NREL backup logic ("emergency" = full design load; "supplemental" = load minus heat-pump output at design, or the full load when the compressor lockout or switchover temperature is above design) [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L3590-L3615
Worked example [C] (house A, MJ 20,454 Btu/h at 23 F, UA_eff = 435 Btu/h-F, ResStock ccASHP curves from 5.4):
| Equipment (nominal at 47 F) | Capacity at 23 F | HSF | Balance point | Q_supp | HSF(47 F) |
|---|---|---|---|---|---|
| Ducted ccASHP 24k | 19,642 | 0.96 | 24.3 F | 812 Btu/h, so <= 5 kW strip allowed | 1.21 |
| Ducted ccASHP 30k | 24,552 | 1.20 | 17.2 F | 0 | 1.51 (just over 1.50 under the dry / two-speed rules) |
| Non-ducted ccASHP 24k | 23,366 | 1.14 | 18.8 F | 0 | 1.43 |
| Non-ducted ccASHP 18k | 17,525 | 0.86 | 27.8 F | 2,929 | 1.07 |

## 6. Ductless mini-split design practice
Most of the manufacturer-specific numbers in this section are [U]: the Mitsubishi, Fujitsu and Daikin sites and document hosts were blocked, so the values come from installation manuals as recalled from training data. They are typical and must be replaced by the model's installation manual or submittal. Code-derived items are [V].

### 6.1 Indoor unit (head) sizes [U]
| Family | Nominal cooling sizes (kBtu/h) |
|---|---|
| Mitsubishi wall-mount MSZ-FS (H2i) | 6, 9, 12, 15, 18 |
| Mitsubishi wall-mount MSZ-GL / MSZ-GS | 6, 9, 12, 15, 18, 24 (GL) |
| Mitsubishi 1-way ceiling cassette MLZ; 4-way 2x2 cassette SLZ; slim ducted SEZ; mid-static ducted PEAD | 9-18; 9-18; 9-18; 12-42 |
| Fujitsu wall-mount (RLS3 / RLFW / RLF1) | 9, 12, 15 (XLTH); 18, 24 |
| Fujitsu compact cassette AUU / slim duct ARU | 7-18 / 7-24 |
| Daikin wall-mount (FTX) | 9, 12, 15, 18, 24 |
Minimum modulated heating output of 6k-9k heads is roughly 1,500-3,000 Btu/h [U], so for a 1.6 kBtu/h bedroom (Section 3.7) even a 6k head sits near the variable-capacity rule of min-compressor HSF <= 0.80 (Section 5.1).

### 6.2 Assigning heads to rooms and zones (practice)
1. Compute room loads (Section 3.7) and group rooms into zones: an open living/kitchen/dining area is one zone; each bedroom is a candidate zone; closed bathrooms and closets usually have no head and rely on transfer or overflow.
2. Open area: choose the head with max capacity at 23 F (or 19 F) >= zone heating load, and check cooling with the "peak" fenestration procedure [V] (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/docs/source/workflow_inputs.rst#L928-L931).
3. Bedrooms, three options: (a) a 6k head per bedroom (simplest, often oversized: flag when zone load < 0.8 x the head's minimum output); (b) one slim-ducted concealed unit (for example 9k-18k) serving 2-4 bedrooms through short ducts (Section 7 duct rules); (c) no bedroom heads, with doors open or transfer fans and a small resistance heater per bedroom (a common WA budget design [U]).
4. Multi-zone outdoor unit: sum of connected head nominal capacities <= the outdoor unit's allowable combination (typically about 130% of outdoor nominal, sometimes up to about 150% [U]). Each head must be an allowed size for the port, and the outdoor unit's max heating capacity at design must be >= the sum of zone loads (block load, no diversity in heating).
5. Prefer single-zone systems for large zones: multi-zone outdoor units have poorer low-load efficiency and larger minimum output [U].

### 6.3 Line sets by head capacity [U]
| Head nominal (Btu/h) | Liquid OD | Gas (suction) OD |
|---|---|---|
| 6,000-12,000 | 1/4 in | 3/8 in |
| 15,000-18,000 | 1/4 in | 1/2 in |
| 24,000 | 3/8 in (some 1/4 in) | 5/8 in (some 1/2 in) |
| 30,000-36,000 | 3/8 in | 5/8 in |
Multi-zone ports are often 1/4 x 3/8 with factory reducers or increasers for 15k-18k heads. Insulate both lines separately; the WA IRC requires suction-line insulation of R-3 or more with permeance <= 0.05 perm, and protected insulation [V] https://github.com/thexqin/us-building-codes-dataset/blob/main/download-v2/washington/irc-2021/chapter-14-heating-and-cooling-equipment-and-appliances.csv (M1411.6, M1411.6.1). Outdoor access ports need locking caps (M1411.9) and piping must be supported within 6 ft of the condensing unit (M1411.8) [V] same URL.

### 6.4 Piping-length limits [U] (verify per model)
| System | Max line length | Max height difference | Pre-charged length | Added charge beyond pre-charge |
|---|---|---|---|---|
| Mitsubishi single-zone 6k-12k (MUZ-FS/GS/GL ...) | 65 ft (20 m) | 40 ft (12 m) | 25 ft (7.6 m) | about 0.22 oz/ft (20 g/m) |
| Mitsubishi single-zone 15k-24k | 100 ft (30 m) | 50 ft (15 m) | 25 ft | about 0.22 oz/ft |
| Fujitsu XLTH 9k/12k/15k | 66 ft (20 m) | 49 ft (15 m) | 49 ft (15 m) | about 0.21 oz/ft (20 g/m) |
| Mitsubishi MXZ multi-zone (2- to 5-port) | per-branch about 82 ft (25 m); total about 98-262 ft by model | 49 ft (15 m) outdoor-to-indoor; about 33 ft (10 m) between indoor units | model-specific | model-specific (per total length) |
| Fujitsu multi-zone (RLXFZH 2-5 port) | per-branch about 82 ft (25 m); total about 164-262 ft by model | 49 ft (15 m) | model-specific | model-specific |
Also: minimum line length of about 10 ft (3 m) for many units [U] (short lines cause noise and oil-return issues); count bends (for example 10 or fewer for Mitsubishi single-zone [U]).

### 6.5 Condensate
- WA IRC M1411.3: slope in the direction of discharge of at least 1/8 in per ft (1%); drain line at least 3/4 in nominal from the drain pan connection to the point of disposal; auxiliary or secondary drain protection (aux pan, overflow line, or UL 508 float switch) where overflow would damage the building [V] https://github.com/thexqin/us-building-codes-dataset/blob/main/download-v2/washington/irc-2021/chapter-14-heating-and-cooling-equipment-and-appliances.csv (M1411.3, M1411.3.1, M1411.3.2)
- M1411.4: a condensate pump in an uninhabitable space (attic, crawl) must be interlocked so the equipment stops if the pump fails [V] same URL.
- Practice [U]: wall-head drain hose about 5/8 in ID; run it down and outside through the line-set hole at 1/4 in per ft where possible; a mini-split condensate pump (in-head or line-hide mounted) is needed when the head is on an interior wall with no downhill path, when the drain must rise (for example a basement head), or when discharging to an interior drain. Provide a freeze-safe discharge; in Bellingham, discharge to grade away from walkways or to a drywell.

### 6.6 Wall penetration and line-hide [U]
- Wall-mount heads: drill a hole of about 2-9/16 in (65 mm) to 3 in (75 mm), sloping down toward the outside. 24k heads may need about 3-1/8 in [U] (Mitsubishi/Fujitsu installation manuals). Seal with a wall sleeve and cap.
- Exterior line-hide channels (for example Diversitech SpeediChannel, Fortress/Airtec) come in about 3 in, 4 in and 5 in widths. One head's line set plus drain plus communication cable fits the 3-4 in size; two heads need 4-5 in [U]. Takeoff item: linear ft of channel + elbows + wall inlet + end fitting.
- Communication/power cable between indoor and outdoor units: typically 14/4 stranded (Mitsubishi); follow the manual [U].
- Outdoor unit: listed for outdoor use, on a pad or stand at least 3 in above grade (WA IRC M1401.4 and M1305.1.3.1) [V] chapter-14 and chapter-13 CSVs; snow and rain stand plus wind baffle recommended for heat pumps in the NW [U].

## 7. Ducted heat pump design (Manual D basics)

### 7.1 Blower airflow
- Rated airflow for heat pump and AC ratings: 400 cfm per ton of rated capacity (RESNET HERS Addendum 82). Default actual installed airflow for DX systems: 360 cfm/ton (RESNET). Furnaces: 240 cfm per ton of heating capacity [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac.rb#L11-L13
- Design band 350-450 cfm/ton. In a low-latent marine climate run toward 400-450 cfm/ton; use the lower end only where dehumidification matters [U] (manufacturer blower tables).
- Check with a temperature-rise equation [C]: `cfm_heat = Q_heat / (1.1 * ACF * (SAT - 70))`; at SAT 105 F (heat pump, [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/hvac_sizing.rb#L1681) that is about 26 cfm per 1,000 Btu/h. `cfm_cool = Q_sens / (1.1 * ACF * (75 - LAT))` with LAT 54-58 F (Section 4.5).
- ResStock limits heat-pump capacity to the existing duct system's airflow / 400 cfm/ton to avoid excess fan pressure [V] https://github.com/NREL/resstock/blob/dd25369f41a83a0767aefeeac0b6f8a0b0edd649/docs/technical_development_guide/source/advanced_tutorial/heat_pump_upgrades.rst (section "Sizing Methodologies").

### 7.2 Room airflow (Manual D proportional method) [U] (standard Manual D practice; ACCA Manual D text not fetched: https://www.acca.org/standards/technical-manuals/manual-d )
```
cfm_room_heat = cfm_blower_heat * Q_room_heat / Q_total_heat
cfm_room_cool = cfm_blower_cool * Q_room_sens / Q_total_sens
cfm_room_design = max(cfm_room_heat, cfm_room_cool)       # heating usually governs in Bellingham
```
Sanity band [C] (house A, 24k ducted heat pump at 400 cfm/ton = 800 cfm): 0.33 cfm/sf overall, so a 144 sf bedroom at 1.64 kBtu/h of 20.45 kBtu/h gets about 64 cfm.

### 7.3 Friction-rate method [U] (Manual D procedure, widely documented; ACCA URL above; ACCA lesson-plan outline confirming the steps: https://higherlogicdownload.s3.amazonaws.com/ACCA/c6b38bda-2e04-4f93-bd51-7a80525ad936/UploadedImages/Lesson%20Plans/EDU4%20Instructors%20Lesson%20Plan%20Final%20-%20Copy.pdf [V for topic list only])
```
ASP [in.w.c.] = blower external static at design cfm - sum(component drops not in the rating)
                 (external coil if not in the air handler, filter/filter grille, supply outlet, return grille, balancing dampers, other accessories)
TEL [ft]      = (measured length + fitting equivalent lengths) of the longest supply run + the longest return run
FR_design [in.w.c./100 ft] = ASP * 100 / TEL
Size every section with FR_design; check velocity limits
```
Typical inputs [U]: ducted air-handler rated external static 0.5 in.w.c. (slim-duct mini-split air handlers are selectable, about 0.1-0.6); 1-in pleated MERV 8 filter grille 0.05-0.15; supply register 0.02-0.05; return grille 0.02-0.03; hand damper 0.03. Manual D friction-rate design window about 0.06-0.18 in/100 ft. Velocity guides: supply trunk <= 900 fpm, supply branch <= 600-700 fpm, return trunk <= 700 fpm, return branch and grille neck <= 600 fpm.

### 7.4 Round-duct capacity table [C]
Darcy-Weisbach with Colebrook friction factor, standard air (0.075 lb/ft3), galvanized steel roughness 0.0003 ft (ASHRAE "medium smooth"): `dp[in.w.c.] = 12*f*L/D * rho * (V/1097)^2`, `Re = 8.56*D*V` (D in inches, V in fpm) per ASHRAE Handbook - Fundamentals ch. 21 https://www.ashrae.org/technical-resources/ashrae-handbook [U for the URL, which was not fetched; the formula is standard]. Script `references/calc/calc_ducts.py`. The values match common ductulators (for example 6 in at 0.08 is about 100 cfm).

| Round dia (in) | cfm @ 0.06 | cfm @ 0.08 | cfm @ 0.10 | velocity @ 0.08 (fpm) | flex fully extended (e=0.003 ft) @ 0.08 | flex rough (e=0.015 ft) @ 0.08 |
|---|---|---|---|---|---|---|
| 4 | 28 | 33 | 37 | 375 | 28 | 21 |
| 5 | 51 | 60 | 68 | 439 | 51 | 39 |
| 6 | 83 | 98 | 111 | 499 | 83 | 65 |
| 7 | 126 | 148 | 168 | 555 | 126 | 98 |
| 8 | 181 | 212 | 240 | 608 | 180 | 141 |
| 9 | 248 | 291 | 329 | 659 | 247 | 194 |
| 10 | 329 | 386 | 436 | 707 | 327 | 258 |
| 12 | 537 | 628 | 709 | 799 | 532 | 422 |
| 14 | 810 | 947 | 1,068 | 886 | 801 | 638 |
| 16 | 1,156 | 1,351 | 1,524 | 967 | 1,142 | 912 |
Low-friction ERV/HRV ductwork, rigid, cfm at 0.04 / 0.05 in/100 ft [C]: 4 in 22/25; 5 in 41/46; 6 in 67/75; 7 in 101/114; 8 in 145/164.
Flex derating: ASHRAE gives flexible duct (fabric and wire, fully extended) an absolute roughness of 0.003-0.015 ft [U]. That costs about 15% of capacity when fully stretched and about 33% at the rough end, at equal friction rate [C]. Compressed or sagging flex is much worse (LBNL and ASHRAE compression-correction research) [U]. Engine rule: size flex at the rigid table / 0.85 (one size up when marginal) and assume at most 4% compression.

### 7.5 Trunk sizing (extended plenum) [U]
- The trunk section after each takeoff carries the sum of the downstream branch cfm. Size it from the table at FR_design; step it down when the remaining cfm fits the next smaller size, or after every 3-4 takeoffs (reducing extended plenum).
- Keep supply trunk velocity <= 900 fpm. Keep the first takeoff about 18-24 in or more from the air-handler plenum transition. Non-reducing extended plenums are commonly limited to about 20-24 ft; beyond that, reduce the trunk or add a second trunk.
- Rectangular equivalent: `De = 1.30*(a*b)^0.625/(a+b)^0.25` (Huebscher; ASHRAE Fundamentals) [U for the source URL; standard formula].

### 7.6 Fitting equivalent lengths
- Conversion [C]: `EL_ft = K * VP / (FR/100)` with `VP = (V/4005)^2` in.w.c. At 600 fpm, VP = 0.0224, so each unit of K equals 28.1 ft at FR 0.08 (37.4 ft at 0.06). At 900 fpm: 63.1 ft per K at 0.08.
- Loss coefficients (6 in duct, 600 fpm, Re about 31,000) from the `fluids` 1.3.1 library (Rennels/Crane/Miller/Ito correlations) [C] https://github.com/CalebBell/fluids ; https://fluids.readthedocs.io/fluids.fittings.html :

| Fitting | K | EL at FR 0.08, 600 fpm |
|---|---|---|
| Smooth 90 deg elbow, r/D 1.5 | 0.28-0.33 | 8-9 ft |
| Smooth 90 deg elbow, r/D 1.0 | 0.36-0.44 | 10-12 ft |
| Mitered 90 deg (single miter, no vanes) | 0.89-1.28 | 25-36 ft |
| 90 deg branch takeoff from 10 in trunk to 6 in branch (20% of flow) | 1.21 | 34 ft |
| 45 deg branch takeoff, same | 0.50 | 14 ft |
| Sharp-edged entrance / exit | 0.57 / 1.0 | 16 / 28 ft |
- ACCA Manual D Appendix 3 lists fitting ELs by group (plenum takeoffs, boots, elbows, returns). Typical magnitudes: supply boots about 30-60+ ft, trunk takeoffs about 20-65 ft, round elbows about 5-15 ft, return filter-grille or boot assemblies about 30+ ft [U] (Manual D URL above). Use the ACCA values if licensed; otherwise the K method above.
- Code data points [V]: WA IRC dryer-duct fitting ELs (4-in radius mitered 45/90 deg = 2 ft 6 in / 5 ft; 6-in radius smooth 45/90 = 1 ft / 1 ft 9 in; 8-in radius 1 ft / 1 ft 7 in; 10-in radius 9 in / 1 ft 6 in) and "15 ft of allowable length per elbow" for ventilation-fan ducts (Table M1504.2) https://github.com/thexqin/us-building-codes-dataset/blob/main/download-v2/washington/irc-2021/chapter-15-exhaust-systems.csv

### 7.7 Supply registers (free-area method) [C with U assumptions]
`cfm = Ak * V_outlet`. Assumptions [U]: Ak (free area) about 0.6 x nominal face area for stamped floor and sidewall registers; residential outlet velocity 400-700 fpm for acceptable noise and throw. Select the exact model from the manufacturer's throw/NC table.
| Register (nominal) | Ak (ft2) | cfm @ 400 fpm | cfm @ 700 fpm |
|---|---|---|---|
| 2 x 10 | 0.083 | 33 | 58 |
| 4 x 10 | 0.167 | 67 | 117 |
| 4 x 12 | 0.200 | 80 | 140 |
| 4 x 14 | 0.233 | 93 | 163 |
| 6 x 10 | 0.250 | 100 | 175 |
| 6 x 12 | 0.300 | 120 | 210 |
| 6 x 14 | 0.350 | 140 | 245 |
Heat-pump heating (supply air about 95-105 F) favors high sidewall or ceiling diffusers with enough throw to wash exterior walls. Floor registers under windows are traditional [U].

### 7.8 Return grilles and filter grilles [C with U limits]
Return grille face velocity <= 400 fpm (<= 300 fpm for quiet bedrooms); filter-grille face velocity <= 300 fpm for 1-in filters, and 200-250 fpm preferred for MERV 11-13 [U]. So face area = cfm / V.
| Grille | Face ft2 | cfm @ 200 fpm | @ 300 fpm | @ 400 fpm |
|---|---|---|---|---|
| 14 x 20 | 1.94 | 389 | 583 | 778 |
| 16 x 20 | 2.22 | 444 | 667 | 889 |
| 20 x 20 | 2.78 | 556 | 833 | 1,111 |
| 20 x 25 | 3.47 | 694 | 1,042 | 1,389 |
| 20 x 30 | 4.17 | 833 | 1,250 | 1,667 |
| 24 x 24 | 4.00 | 800 | 1,200 | 1,600 |

### 7.9 One central return vs bedroom returns: pressure relief for closed bedrooms
- Requirement (practice and programs): with its door closed, each ducted room should stay within about +/-3 Pa of the main body. Methods: a dedicated return, a transfer grille, a jumper (jump) duct, or door undercut (ENERGY STAR v3/3.1 Rater Field Checklist) [U] https://www.energystar.gov/partner_resources/residential_new/homes_prog_reqs/national_page
- Sizing physics (sharp-edged orifice, Cd 0.6, air density 1.2 kg/m3) [C]: `Q_cfm = 1.059 * A_free_in2 * sqrt(dP_Pa)`, so at 3 Pa, `A_free_in2 = Q_cfm / 1.83`. That is about 0.55 in2 of free area per cfm, or roughly 1 in2 of gross grille per cfm at 50-60% free area.
  - Examples [C]: a 3/4 in x 32 in door undercut (24 in2) passes about 44 cfm at 3 Pa (hard floor; less over carpet). A single-opening path (a grille in the door) for 100 cfm needs about 55 in2 free, about 100 in2 gross (for example 10x10). A through-wall transfer has two grilles in series at about 1.5 Pa each, so each needs about 77 in2 free, about 140 in2 gross (for example 14x10 or 12x12).
- A jumper duct (ceiling grille - duct - hall ceiling grille) with two grilles in series: keep the total loss <= 3 Pa (0.012 in.w.c.). For about 100 cfm: a 10 in duct (duct plus fittings about 0.8 Pa at 183 fpm with total K of about 1.5), plus two grilles sized for 150-200 fpm through the free area (about 12x12 or 14x10 each), about 1.1 Pa each [C]. An 8 in jumper would use about 1.9 Pa in the duct alone [C].
- Engine default for WSEC houses: one central return (or one per floor) plus transfer or jumper paths for every closed bedroom with a supply; flag any bedroom with supply > 0 and no return path.

### 7.10 Air-handler placement and what changes
| Location | Duct load (Section 3.6) | Code and constructability items |
|---|---|---|
| Conditioned space (closet, or a mechanical room inside the air barrier) | 0 (regain 1.0) [V] | Aux pan/overflow protection if overflow would cause damage (M1411.3.1) [V]; preferred in WSEC houses (WSEC duct credit and testing rules: WA code agent) |
| Crawlspace (vented or unvented) | regain 0.12-0.17 (vented, insulated floor) / 0.30 (unvented, insulated walls) [V] | Access: opening >= 22 x 30 in, passageway >= 30 in high x 22 in wide and <= 20 ft long, level service space 30 x 30 in, suspended appliances >= 6 in above ground, ground-supported appliances on a pad >= 3 in above grade; light and receptacle [V] (M1305.1.3, M1305.1.3.1) https://github.com/thexqin/us-building-codes-dataset/blob/main/download-v2/washington/irc-2021/chapter-13-general-mechanical-system-requirements.csv ; condensate pump interlock (M1411.4) [V] |
| Attic | regain 0.10 [V] | Access: clear opening >= 20 x 30 in, passageway >= 30 in high x 22 in wide, <= 20 ft (<= 50 ft if >= 6 ft high), 24 in wide solid floor, 30 x 30 in service space, switched light and receptacle (M1305.1.2, M1305.1.2.1) [V] same URL; aux drain pan / float switch (M1411.3.1) [V]; insulated ducts (R-8 typical, WSEC) [U] |

## 8. Ventilation sizing

### 8.1 Washington (IRC 2021 as amended, M1505.4) [V]
Source: https://github.com/thexqin/us-building-codes-dataset/blob/main/download-v2/washington/irc-2021/chapter-15-exhaust-systems.csv (M1505.4.3, M1505.4.3.1, M1505.4.3.2). The WA code agent should confirm against WAC 51-51 / https://codes.iccsafe.org/content/WARC2021P1 .
```
Qr [cfm] = 0.01 * CFA_total_sf + 7.5 * (Nbr + 1)        (Equation 15-1; not less than 30 cfm per dwelling unit)
Qv [cfm] = Qr * Csystem                                   (Equation 15-2)
Csystem (Table M1505.4.3(2)):  balanced + distributed 1.0 | balanced + not distributed 1.25 | not balanced + distributed 1.25 | not balanced + not distributed 1.5
Intermittent-off (Table M1505.4.3.2; must run >= 2 h in every 4 h segment): run-time 50% -> x2.0 ; 66% -> x1.5 ; 75% -> x1.3 ; 100% -> x1.0 (interpolate, do not extrapolate)
```
Cross-check note: the WA code digest (`research-hvac-code.md`) labels the intermittent-operation table "M1505.4.3(2)". In the WA 2021 text read here, Table M1505.4.3(2) is the system coefficient (Csystem) table and the intermittent factors are Table M1505.4.3.2 [V]. Table M1505.4.3(1) equals Equation 15-1 evaluated at the upper bound of each floor-area bin, rounded up to the next 5 cfm, with a 30 cfm minimum (for example 2,001-2,500 sf with 3 bedrooms = 55 cfm; < 500 sf with 4 bedrooms = 45 cfm) [V]/[C]. Balanced means supply and exhaust within 10% of each other (tested exhaust within 10% or 5 cfm of supply) (M1505.4.1.4) [V]. A supply system must deliver ducted outdoor air to each habitable space, except interior adjoining spaces served by a 30 cfm transfer fan or a permanent opening of at least 8% of floor area and at least 25 sf; outdoor-air supply must be filtered to MERV 8 or better (M1505.4.1.1, M1505.4.1.3) [V]. "Distributed" is defined in WA chapter 2 (WA code agent to confirm). Alternative balanced systems designed and commissioned to ASHRAE 62.2 are permitted (M1505.1 exception) [V]. Using a heating/cooling air handler for outdoor-air supply is not permitted unless its low speed is <= 25% of rated airflow with a motorized OA damper tracking exhaust within 10% (M1505.4.1.5) [V].

### 8.2 ASHRAE 62.2-2016/2019 (for the M1505.1 alternative, or where the program uses 62.2) [V via NREL implementation; the standard text was not fetched]
```
Qtot = 0.03 * CFA + 7.5 * (Nbr + 1)                              # https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/airflow.rb#L2861-L2863
Qinf = 0.052 * Q50 * wsf * (H / 8.2)^0.4                          # equivalent to NL*wsf*CFA*8.202/60, NL = 1000*ELA/CFA*(H/8.202)^0.4 (https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/airflow.rb#L2778-L2793, https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/airflow.rb#L2852-L2854)
Qfan = Qtot - Phi * (Qinf * Aext);  Phi = 1 (balanced), Phi = Qinf/Qtot (unbalanced); Aext = 1 for detached   # https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/airflow.rb#L2877-L2894 (ERI 2019 branch)
(older 62.2-2013 / ERI < 2019: Qfan = Qtot - Qinf, with Qinf capped at 2/3 of Qtot)
```
URLs: https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/airflow.rb#L2844-L2910 ; Bellingham wsf = 0.58 (Section 1).
Bellingham comparison [C]:
| House | 62.2 Qtot | Qinf | 62.2 Qfan balanced / exhaust-only | WA Qr | WA Qv balanced+distributed / exhaust-only not distributed |
|---|---|---|---|---|---|
| 2,400 sf, 3 BR, 3 ACH50, H 18 ft | 102 | 42 | 60 / 85 | 54 | 54 / 81 |
| 1,800 sf, 3 BR, 3 ACH50, H 10 ft | 84 | 26 | 58 / 76 | 48 | 48 / 72 |
| 3,000 sf, 4 BR, 4 ACH50, H 19 ft | 128 | 76 | 52 / 82 | 68 | 68 / 101 |
| 2,000 sf, 3 BR, 2.5 ACH50, H 18 ft | 90 | 29 | 61 / 80 | 50 | 50 / 75 |

### 8.3 Local exhaust (WA Table M1505.4.4.1 and M1505.4.4.3) [V] (chapter-15 URL above)
| Space | Intermittent | Continuous |
|---|---|---|
| Bathroom / toilet room | 50 cfm | 20 cfm |
| Enclosed kitchen | per M1505.4.4.3 | 5 ACH of kitchen volume |
| Open kitchen | per M1505.4.4.3 | not permitted |
| Range hood over electric range | >= 160 cfm or >= 65% capture efficiency (ASTM E3087) | - |
| Range hood over combustion range | >= 250 cfm or >= 80% CE | - |
| Other intermittent kitchen exhaust (downdraft etc.) | >= 300 cfm | - |
Sound: intermittent kitchen exhaust <= 3 sones at >= 100 cfm; continuous kitchen <= 1 sone; whole-house ventilation fans <= 1.0 sone at >= 0.1 in.w.c. (air handlers, ERV/HRV and remote fans with >= 4 ft of duct are exempt) (M1505.4.1.1, M1505.4.4.2) [V]. Installed flows must be field-tested with a flow hood or grid, unless the fan's 0.25 in.w.c. rating is used with duct sizes meeting Table M1505.4.4.2 (Section 9.1) [V].

### 8.4 ERV/HRV selection
- Recovery metrics (HVI 920 / CSA C439): SRE (sensible recovery efficiency) at 32 F (0 C) and -13 F (-25 C) excludes fan heat; ASE (apparent sensible effectiveness) includes it; TRE (total recovery efficiency) at 95 F is the cooling rating. Use ASE in the Manual J ventilation load (Section 3.5). NREL's SRE-to-ASE conversion is CSA 439 Clause 9.3.3.1 Eq. 12 [V] https://github.com/NREL/OpenStudio-HPXML/blob/f28d40e397e9972a19a366600207c754efbf2eec/HPXMLtoOpenStudio/resources/airflow.rb#L1804-L1845 . HVI certified-products directory: https://www.hvi.org/hvi-certified-products-directory/ [U, not fetched].
- Selection rule [C/U]: net supply airflow at the design external static (from HVI ratings, typically listed at 0.1-0.4 in.w.c.) >= Qv, plus 20-30% headroom for boost. Choose SRE >= 65-75% at 32 F; ERV rather than HRV where winter indoor RH runs low (small, tight houses) [U]. Fan efficacy (cfm/W) minimums are in WSEC (WA code agent).
- Common units [U] (hosts blocked; verify against the HVI 920 listing):

| Unit | Type | Airflow range (approx.) | Notes |
|---|---|---|---|
| Panasonic Intelli-Balance 100 (FV-10VEC2) | ERV, ceiling/wall-hung | about 40-100 cfm | small-house or unit-level balanced ventilation; 4 in / 6 in ports |
| Panasonic WhisperComfort (FV-04VE1) | spot ERV | about 20-40 cfm | single-room or small-unit supply plus exhaust |
| Broan-NuTone AI Series ERV / HRV (for example B130E / B160E / B210E) | ERV/HRV | about 50-200 cfm by model | 5 in / 6 in ports; "AI" auto-balancing |
| Zehnder ComfoAir 200 / 350; ComfoAir Q350 / Q450 / Q600 | HRV (ERV core option) | model number = max m3/h: 200 m3/h = 118 cfm; 350 = 206; 450 = 265; 600 = 353 cfm [C conversion] | high SRE; ComfoTube 75/90 mm semi-rigid distribution |
| RenewAire EV Premium S / M / L | ERV (static-plate) | roughly 50-250 cfm across S/M/L | 6 in ports typical |
| Lunos e2 (pairs) / eGO | decentralized reversing HRV | about 10-25 cfm per pair | through-wall 160 mm; counts as balanced when installed in pairs |

### 8.5 ERV duct design [U] (practice; sizes checked against the 7.4 low-friction table [C])
- Supply outdoor air to bedrooms and the living/family room; exhaust from bathrooms, laundry and kitchen (not over the range, and not from the garage). Keep supply and exhaust grilles in the same room at least 6-10 ft apart.
- Trunks: 6 in for <= 75 cfm and 7-8 in for <= 115-165 cfm at 0.04-0.05 in/100 ft [C]. Branches: 4 in for <= 20-25 cfm, 5 in for <= 40-45 cfm [C]. Use rigid or semi-rigid duct; add a balancing damper per branch.
- Outdoor intake and exhaust hoods: exhaust openings >= 10 ft from mechanical air intakes unless >= 3 ft above them; >= 3 ft from property lines, operable windows and doors (WA M1504.3) [V] (chapter-15 URL). Insulate and vapor-seal the cold-side ducts (outdoor air and exhaust) inside the envelope [U].
- Balance and test: within 10% (or 5 cfm), with a flow report posted (M1505.4.1.4, M1505.4.1.6, M1505.4.1.7) [V].

### 8.6 Exhaust-only whole-house ventilation with a continuous bath fan
- WA code items [V] (chapter-15 URL): the fan must be ducted to the outside, with backdraft or motorized dampers per WSEC, and HVI 915/916/920 rated (M1505.4.1.2). A bathroom fan designed for an intermittent rate above the continuous rate needs an occupancy or humidity sensor that automatically boosts it to the high rate (M1505.4.1.2). Controls must be readily accessible, allow a manual "off" override, carry a permanent label ("Leave on unless outdoor air quality is very poor") and run continuously unless intermittent-off sizing is used (M1505.4.2). Sound <= 1.0 sone at >= 0.1 in.w.c. (M1505.4.1.1). Airflow: Qv = 1.5 x Qr (not balanced, not distributed) [V].
- Example [C]: 2,400 sf, 3 BR gives Qr = 54 and Qv = 81 cfm. That is one fan continuous at 80 cfm, or two bath fans at 40-45 cfm continuous each. Each fan's duct must meet Table M1505.4.4.2 at its rated cfm (for example 80 cfm needs a 5 in smooth duct <= 100 ft, or 6 in flex <= 90 ft, with <= 3 elbows) [V].
- Panasonic WhisperGreen Select FV-0511VQ1 [U] https://na.panasonic.com/us/ (host blocked): "Pick-A-Flow" 50/80/110 cfm; 4 in or 6 in duct connection (adapter); continuous low-speed plus boost through plug-in modules (motion, humidity/condensation sensor, LED light); ENERGY STAR; sub-1 sone at the lower settings. Confirm the continuous-mode cfm steps, HVI-rated flow at 0.1 and 0.25 in.w.c., and the WSEC efficacy value.

## 9. Exhaust duct sizing (bath, kitchen, dryer)

### 9.1 WA prescriptive exhaust duct sizing, Table M1505.4.4.2 (local exhaust fans rated at 0.25 in.w.c.) [V] (chapter-15 URL)
| Fan cfm @ 0.25 in.w.c. | Min flex dia / max length | Min smooth dia / max length | Max elbows |
|---|---|---|---|
| 50 | 4 in / 25 ft | 4 in / 70 ft | 3 |
| 50 | 5 in / 90 ft | 5 in / 100 ft | 3 |
| 50 | 6 in / no limit | 6 in / no limit | 3 |
| 80 | 4 in / not allowed | 4 in / 20 ft | 3 |
| 80 | 5 in / 15 ft | 5 in / 100 ft | 3 |
| 80 | 6 in / 90 ft | 6 in / no limit | 3 |
| 100 | 5 in / not allowed | 5 in / 50 ft | 3 |
| 100 | 6 in / 45 ft | 6 in / no limit | 3 |
| 125 | 6 in / 15 ft | 6 in / no limit | 3 |
| 125 | 7 in / 70 ft | 7 in / no limit | 3 |
Footnote: subtract 10 ft of length for each additional elbow [V].

### 9.2 Ventilation-duct length limits, Table M1504.2 [V] (chapter-15 URL; fan rated per AMCA 210 at 0.25 in.w.c.; no elbows assumed; deduct 15 ft per elbow; NL = no limit; X = not allowed; non-circular D = 4A/P)
| Dia (in) | Flex: 50 / 80 / 100 / 125 / 150 / 200 / 250 / 300 cfm | Smooth: 50 / 80 / 100 / 125 / 150 / 200 / 250 / 300 cfm |
|---|---|---|
| 3 | X X X X X X X X | 5 X X X X X X X |
| 4 | 56 4 X X X X X X | 114 31 10 X X X X X |
| 5 | NL 81 42 16 2 X X X | NL 152 91 51 28 4 X X |
| 6 | NL NL 158 91 55 18 1 X | NL NL NL 168 112 53 25 9 |
| 7 | NL NL NL NL 161 78 40 19 | NL NL NL NL NL 148 88 54 |
| 8+ | NL NL NL NL NL 189 111 69 | NL NL NL NL NL NL 198 133 |
Exception: no length limit if the duct system follows the manufacturer's design criteria or the installed flow is verified with a flow hood or grid (M1504.2) [V].

### 9.3 Terminations and dampers [V] (chapter-15 URL)
Exhaust must discharge outdoors, never into an attic, soffit, ridge vent or crawl space (M1501.1, M1505.2). Terminations: >= 3 ft from property lines, operable windows, doors and gravity intakes; >= 10 ft from mechanical intakes unless >= 3 ft above them (M1504.3). Backdraft or motorized dampers per WSEC (M1505.4.1.2). Takeoff items per fan: duct run, roof or wall cap with damper (4 in / 6 in / 7 in), clamps and tape, and insulation where the duct runs through unconditioned space [U].

### 9.4 Kitchen range hood [V unless noted] (chapter-15 URL)
- Duct: smooth-interior, airtight, galvanized steel, stainless or copper; with a backdraft damper; independent of other exhausts; must not terminate in an attic, crawl or inside the building (M1503.3, M1503.4). Ductless hoods are allowed only with continuous 5 ACH enclosed-kitchen exhaust (M1503.3 exception).
- Makeup air (WA M1503.6): required for an exhaust system > 400 cfm only where a fuel-burning appliance that is neither direct-vent nor mechanical-draft sits inside the dwelling's air barrier. Then makeup air approximately equal to the exhaust rate, with a gravity damper or an electrically operated damper interlocked to open with the exhaust (M1503.6.2). A passive makeup-air damper must be rated for the design flow at <= 0.01 in.w.c. (3 Pa). All-electric heat-pump houses therefore do not trigger M1503.6 [C from V]. Large hoods in a tight house still starve; recommend a hood <= 400 cfm or interlocked makeup air anyway [U].
- Hood duct size by airflow (manufacturer norms) [U]: <= 300 cfm uses 6 in round (or 3-1/4 x 10); about 400 cfm 7 in; about 600 cfm 8 in; 900-1,200 cfm 10 in. Typical maximum equivalent run 30-50 ft (per hood manual) [U]. Physics check [C] (Darcy-Colebrook plus a termination and damper K of about 2.5; 0.25 in.w.c. total over a 40 ft equivalent run): 6 in carries about 190 cfm, 7 in about 270, 8 in about 360, 10 in about 590. So 7-8 in is warranted above about 250-300 cfm, and 10 in above about 600 cfm.

### 9.5 Clothes dryer [V] (chapter-15 URL)
- 4 in nominal duct, smooth interior, metal >= 0.0157 in (No. 28 gauge) (M1502.4.1); supported at <= 12 ft; joints sealed and mechanically fastened, no fasteners protruding > 1/8 in (M1502.4.2). Transition duct: single length, UL 2158A, <= 8 ft, not concealed (M1502.4.3).
- Maximum length (M1502.4.6.1): 35 ft from the transition connection to the outlet terminal, reduced by fitting ELs: 4-in radius mitered 45 deg = 2.5 ft, 90 deg = 5 ft; 6-in radius smooth 45 deg = 1 ft, 90 deg = 1.75 ft; 8-in radius 45 deg = 1 ft, 90 deg = 1.58 ft; 10-in radius 45 deg = 0.75 ft, 90 deg = 1.5 ft. (The familiar "5 ft per 90 deg, 2.5 ft per 45 deg" rule is the 4-in-radius mitered row.)
- Or use the dryer manufacturer's instructions (M1502.4.6.2; a copy is required at concealment inspection), or a dryer exhaust duct power ventilator (DEPV, UL 705) per its instructions (M1502.4.6.3, M1502.4.4). Domestic booster fans are prohibited (M1502.4.5). If the equivalent length exceeds 35 ft, label it within 6 ft of the connection (M1502.4.7).
- Termination: >= 3 ft from openings (including vented soffits) unless the dryer manual says otherwise; backdraft damper; no screen; outlet open area >= 12.5 in2 (M1502.3, M1502.3.1). Where a dryer space exists, the duct is required (capped "future use") unless a listed condensing dryer is installed (M1502.4.8). Shield plates where the duct is < 1-1/4 in from the framing face (M1502.5).
- Engine: `EL = straight_ft + sum(fitting_EL)`; allowed if EL <= 35, or if EL <= the manufacturer's maximum when a model is specified; otherwise add a DEPV line item (UL 705).

## 10. Rules of thumb and outlier checks for a load/bid checker

### 10.1 Reference-house results (Bellingham, 2021-WSEC-like envelope) [C]
Assumptions: walls U-0.056, attic U-0.024, crawl floor U-0.029 (vented crawl, PTDH factor 0.756), slab F-0.54, windows U-0.28 / SHGC-0.28, doors U-0.20, ducts inside, ventilation per WA Eq. 15-1 x Csystem, Manual J blower-door infiltration (shielding class 4), internal gains 2,400 Btu/h + occupants. Script: `references/calc/calc_house.py`; formulas from Sections 2-4.

| Case | CFA | ACH50 | Ventilation | MJ heat @ HTD 47 (Btu/h) | Btu/h-sf | MJ heat @ HTD 51 | WSU sheet (dT 51) | WSU x1.25 (HP max) | Cooling total | Clg/Htg (MJ) |
|---|---|---|---|---|---|---|---|---|---|---|
| A 2-storey crawl, 15% glass | 2,400 | 3.0 | exhaust-only 81 cfm | 20,454 | 8.5 | 22,293 | 26,655 | 33,318 | 9,761 | 0.48 |
| A | 2,400 | 3.0 | HRV 54 cfm, ASE 0.70 | 18,743 | 7.8 | - | 26,655 | 33,318 | 9,761 | 0.52 |
| A | 2,400 | 5.0 | exhaust-only | 23,183 | 9.7 | - | 26,655 | 33,318 | 9,841 | 0.42 |
| A | 2,400 | 5.0 | HRV | 21,824 | 9.1 | - | 26,655 | 33,318 | 9,841 | 0.45 |
| B 1-storey slab (R-10 perimeter), 15% glass | 1,800 | 3.0 | exhaust-only 72 cfm | 19,597 | 10.9 | - | 24,825 | 31,031 | 9,144 | 0.47 |
| B | 1,800 | 3.0 | HRV | 17,836 | 9.9 | - | 24,825 | 31,031 | 9,144 | 0.51 |
| C 2-storey, 20% glass, 4 BR | 3,000 | 4.0 | exhaust-only 101 cfm | 28,872 | 9.6 | - | 35,572 | 44,466 | 14,129 | 0.49 |
| D 2-storey, 12% glass | 2,000 | 2.5 | HRV 50 cfm | 15,005 | 7.5 | - | 22,131 | 27,664 | 8,089 | 0.54 |
External cross-check [S]: Mercer Island WSU-sheet submittals show "Maximum Heat Equipment Output" of 31,600-34,282 Btu/h https://permitbulletin.mercerisland.gov/public/2504-058/SUB1/lin%20kicska%20heating%20system%20sizing%20worksheet%2004.01.2025.pdf . This matches the WSU x1.25 column for 2,000-3,000 sf houses. Mercer Island's design dT is presumably about 44-46 F [U].

### 10.2 Proposed checker bands (new detached houses, Bellingham / Whatcom lowlands)
| Metric | Expected band | Flag if | Basis |
|---|---|---|---|
| Manual J heating intensity (HTD 47-51) | 7-12 Btu/h per sf CFA | < 5 or > 18 (vaulted or glass-heavy houses can reach about 15) | [C] 10.1 |
| WSU-sheet heating intensity (dT 51) | 10-15 Btu/h-sf | < 8 or > 20 | [C] 10.1; [S] Mercer Island |
| Total heating load, 2,000-3,000 sf | 15-29 kBtu/h (MJ) / 22-36 kBtu/h (WSU) | outside 12-40 | [C] |
| Brief's "15-35 Btu/h-sf" | too high for new WSEC-2021 construction; fits older or leaky stock or WSU x1.25-x1.4 outputs | - | disagreement noted [C] |
| Brief's "20-40 kBtu/h for 2,000-3,000 sf" | consistent with the WSU sheet and WSU x1.25 outputs, but high for Manual J | - | [C] |
| Cooling intensity | 3.5-5.5 Btu/h-sf (2,200-3,400 sf/ton) | > 8 Btu/h-sf (check west/east glass and skylights) or < 2.5 | [C] 4.6 |
| Cooling / heating ratio (MJ basis) | 0.40-0.55 (0.30-0.40 against the WSU heating number) | > 0.8 (likely wrong design temperature or glass) or < 0.25 | [C] |
| JSHR | 0.88-0.94 | > 0.97 or < 0.80 | [C] 4.3 |
| Heat-pump nominal (47 F) capacity / MJ heating load | ducted ccASHP 1.2-1.5 (HSF = 1 needs 1/0.818 = 1.22 at 23 F); ductless ccASHP 1.0-1.3 (1/0.974 = 1.03) | HSF (capacity at design / load) < 1.0 without supplemental heat; > 1.5 for fixed-speed | [V] 5.1 and [C] 5.5 |
| Min-compressor heating capacity / heating load | <= 0.80 | > 0.80 (short-cycling risk; Manual S variable-capacity rule) | [V] 5.1 |
| Supplemental strip heat | <= 5 kW if Q_supp <= 15 kBtu/h; otherwise 0.95-1.75 x Q_supp | outside the limits | [V] 5.1 |
| Airflow | 350-450 cfm/ton; about 0.25-0.6 cfm/sf | outside | [V] 7.1, [C] |
| Duct friction rate (Manual D) | 0.06-0.18 in/100 ft | outside | [U] 7.3 |
| Supply trunk velocity | <= 900 fpm | > 900 | [U] 7.3 |
| Whole-house ventilation (WA) | Qr = 0.01 x CFA + 7.5 x (Nbr + 1) >= 30; Qv = Qr x Csystem (1.0-1.5): typically 45-110 cfm | fan rated flow at design static < Qv | [V] 8.1 |
| Bath fan duct | per Table M1505.4.4.2 (for example 80 cfm needs 5 in smooth <= 100 ft) | 4 in duct on an 80+ cfm fan | [V] 9.1 |
| Dryer duct | EL <= 35 ft (or manufacturer max) | > 35 ft with no manufacturer data and no DEPV | [V] 9.5 |
| Range hood | >= 160 cfm (electric) / >= 250 cfm (gas) or CE >= 65% / 80% | > 400 cfm with a non-direct-vent combustion appliance inside and no makeup air | [V] 8.3, 9.4 |
| Design infiltration (MJ blower-door method) | ACHnat about ACH50/11 (2-storey) to ACH50/15 (1-storey) | N < 8 or > 20 | [C] 3.4 |

## 11. Python-ready constants (collected from the sections above)
```python
# ---- Bellingham design data ----
BELLINGHAM = dict(
    mj8_heat_99=23.0, mj8_cool_1=76.0, mj8_cwb=64.0, grains_50rh=4.0, grains_45rh=10.0, daily_range="M",
    hdd65_cdd50=3.38, elev_ft=151, lat=48.8,                        # ACCA ODC Table 1A [V]
    wsec_rc1_heat=19.0, wsec_rc1_cool=78.0,                          # WAC 51-11R-60100 [S]
    ashrae2009_heat_99_6=18.0, ashrae2009_cool_0_4=79.3, ashrae2009_cool_2=73.0,  # DDY [V]
    wsf_62_2=0.58)                                                   # ashrae622_wsf.csv [V]
T_IN_HEAT, T_IN_COOL = 70.0, 75.0                                    # MJ8 [V]
ACF = lambda elev_ft: 1 - 0.0000308 * elev_ft                         # [V]
# ---- WSU simple heating sizing ----
WSU_ACH, WSU_AIR_CP = 0.6, 0.018                                      # [S]
WSU_DUCT_UNCOND, WSU_DUCT_COND = 1.10, 1.00                           # [S]
WSU_MAX_FURNACE, WSU_MAX_HP = 1.40, 1.25                              # [S]
WSU_GLAZING_DOOR_U = 0.30                                             # [S]
# ---- Manual J (NREL MJ8 implementation) ----
SENS, LAT = 1.1, 0.68                                                 # Btu/h per cfm-F, per cfm-grain [V]
OCC_SENS, OCC_LAT = 230.0, 200.0                                      # per occupant; occupants = Nbr + 1 [V]
APPL_SENS_1FRIDGE, APPL_SENS_2FRIDGE = 2400.0, 3600.0                 # NREL "per Manual J" [V]
WIND_HEAT_MPH, WIND_COOL_MPH = 15.0, 7.5                              # Tables 5D/5E [V]
def ela_in2(ach50, vol_ft3): return 0.05488 * ach50 * vol_ft3 / 60.0  # n = 0.65 [V]/[C]
def cs(stories): return 0.015 * stories                               # [V]
def cw(stories, shielding_class=4): return (0.0065 - 0.00266*(shielding_class-3)) * stories**0.4  # [V]
def icfm(ach50, vol, stories, dT, wind, sc=4): return ela_in2(ach50, vol) * (cs(stories)*dT + cw(stories, sc)*wind**2) ** 0.5
def ncfm_exhaust(icfm_, q_exh): return (icfm_**1.5 + q_exh**1.5) ** 0.67  # [V]
def ptdh_vented_crawl(htd, u_floor, u_wall): return htd / (1 + 4*u_floor/(u_wall + 0.11))  # [V]
def ptdh_sealed_crawl(htd, u_floor, u_wall): return u_wall*htd / (4*u_floor + u_wall)     # [V]
RADIANT_HTD_ADDER = 25.0                                              # [V]
FIREPLACE_CFM = 20.0                                                  # [V]
DR_ADJ = {"L": 4.0, "M": 0.0, "H": -5.0}                              # CLTD adjust [V]
PSF_48_8 = {"N": 33.1, "NE": 127.2, "E": 210.7, "SE": 208.3, "S": 182.3, "SW": 208.3, "W": 210.7, "NW": 127.2, "H": 219.7}  # [C]
CLF_NOIS = {"N": .48, "NE": .40, "E": .38, "SE": .35, "S": .24, "SW": .35, "W": .38, "NW": .40, "H": .68}  # [V]
CLF_IS   = {"N": .29, "NE": .32, "E": .32, "SE": .29, "S": .18, "SW": .29, "W": .32, "NW": .32, "H": .52}  # [V]
def htm_glass(d, shgc, u, ctd, isc=1.0):
    clf = (CLF_IS if isc < 1 else CLF_NOIS)[d]
    return PSF_48_8[d]*clf*shgc*isc/0.87 + u*ctd                       # [V] formula
DUCT_REGAIN = {"conditioned": 1.0, "attic": 0.10, "garage": 0.05, "vented_crawl_ins_floor": 0.12,
               "vented_crawl_ins_floor_walls": 0.17, "unvented_crawl_ins_walls_floor": 0.30}  # [V]
BLOWER_HEAT_DEFAULT = 1707.0                                          # Btu/h, cooling [V]
# ---- Manual S (2023 + draft addendum c) ----
MS = dict(single_speed_max_le24k=1.20, single_speed_max_gt24k=1.15, two_speed_max=1.25, var_simplified_max=1.30,
          min_total=0.90, min_sens=0.90, min_lat=1.00, hsf_min_var=1.00, min_comp_hsf_max=0.80,
          min_comp_cool_max_adv=0.80, hsf47_max=1.50, two_speed_hsf_max=1.20,
          supp_small_load=15000.0, supp_small_kw_max=5.0, supp_sf_min=0.95, supp_sf_max=1.75, emergency_frac=0.85)  # [V]
Q17_DEFAULT = {"single_two_stage": 0.626, "variable": 0.69}            # [V]
def cap_frac_linear(T, q17): return 1 - (1 - q17)/30.0*(47 - T)       # [V]
CCASHP_MAX = {"ductless": {47: 1.216, 17: 0.913, 5: 0.867, -15: 0.630},
              "ducted":   {47: 1.028, 17: 0.766, 5: 0.688, -15: 0.507}}  # ResStock [V]
# ---- Airflow and ducts ----
CFM_PER_TON_RATED, CFM_PER_TON_ACTUAL_DEFAULT = 400.0, 360.0          # [V]
def vp(v_fpm): return (v_fpm/4005.0)**2                               # in.w.c. [C]
def el_from_k(K, v_fpm, fr): return K*vp(v_fpm)/(fr/100.0)            # ft [C]
def orifice_cfm(a_free_in2, dp_pa, cd=0.6): return cd*1.7649*a_free_in2*dp_pa**0.5   # [C]
# ---- WA ventilation (IRC 2021 as amended) ----
def wa_qr(cfa, nbr): return max(0.01*cfa + 7.5*(nbr + 1), 30.0)      # Eq. 15-1 [V]
CSYSTEM = {("balanced", "distributed"): 1.0, ("balanced", "not"): 1.25, ("unbalanced", "distributed"): 1.25, ("unbalanced", "not"): 1.5}  # [V]
INTERMITTENT_FACTOR = {0.50: 2.0, 0.66: 1.5, 0.75: 1.3, 1.00: 1.0}      # [V]
def q622_tot(cfa, nbr): return 0.03*cfa + 7.5*(nbr + 1)               # [V]
def q622_inf(q50, wsf, h_ft): return 0.052*q50*wsf*(h_ft/8.2)**0.4     # [V]/[C]
LOCAL_EXHAUST = {"bath_int": 50, "bath_cont": 20, "kitchen_enclosed_cont_ach": 5,
                 "hood_electric_cfm": 160, "hood_combustion_cfm": 250, "hood_electric_ce": .65, "hood_combustion_ce": .80,
                 "other_kitchen_int": 300}                             # [V]
DRYER_MAX_FT = 35.0
DRYER_FITTING_EL = {("mitered4", 45): 2.5, ("mitered4", 90): 5.0, ("r6", 45): 1.0, ("r6", 90): 1.75,
                    ("r8", 45): 1.0, ("r8", 90): 19/12, ("r10", 45): 0.75, ("r10", 90): 1.5}   # [V]
EXHAUST_ELBOW_DEDUCT_M1504_2, EXHAUST_ELBOW_DEDUCT_M1505_4_4_2 = 15.0, 10.0   # ft [V]
MAKEUP_AIR_TRIGGER_CFM = 400.0   # only with non-direct-vent / non-mechanical-draft fuel appliance inside the air barrier (WA) [V]
```

## 12. Open items and what to verify before production
1. WSU calculator: obtain the current (2021) spreadsheet from energy.wsu.edu (blocked here) and confirm the full dropdown U/F lists (below-grade options, skylight U, R-49 attic), whether "0.6 ACH" and "1.25 heat pump" are unchanged in the 2021 version, and the design-temperature table (RC-1). Sections 2.3-2.4 are [S].
2. Manual S 2023 final text (addendum c was a March 2025 public-review draft; the extracted text had lost its strike and underline marks). Confirm every 5.1 value against the purchased standard: https://www.acca.org/standards/technical-manuals/manual-s
3. Manual J appliance default: NREL's 2,400/3,600 Btu/h "per Manual J" vs the brief's 1,200-1,600. Check against the MJ8 version used (v2.50 or later).
4. Mini-split limits (Section 6): pull the installation manuals for the exact models bid (Mitsubishi MUZ-FS/GL/MXZ, Fujitsu RLS3H/RLXFZH, Daikin) for line sizes, lengths, lift, pre-charge, oz/ft, minimum length, combination tables and hole size. Every value there is [U].
5. NEEP ccASHP v4 and ENERGY STAR cold-climate thresholds (COP >= 1.75 at 5 F; 5 F / 47 F capacity >= 70%) are [U]. Pull per-model 5/17/47 F data from https://ashp.neep.org (API/CSV) into the equipment database.
6. The LBL N-factor table (3.4) is [U]; it is only needed for seasonal energy, not design loads.
7. ERV/HRV and bath-fan product specs (8.4, 8.6): pull HVI 920 listings (cfm at static, SRE, ASE, W).
8. WA-specific: the "distributed" definition for Csystem; WSEC fan efficacy; WSEC duct location and testing rules; confirm that the thexqin dataset text equals the WAC 51-51 amendments (WA code agent).
9. Manual D fitting equivalent lengths (7.6) and register and grille catalog data (7.7-7.8) are [U]/[C]; replace them with licensed Manual D tables and the chosen manufacturer's catalog.
10. Design temperature choice (19 F RC-1 vs 23 F MJ8): Manual J loads at 19 F are about 9% higher (22,293 vs 20,454 Btu/h for house A) [C]. The engine should compute both and report which one the jurisdiction accepts.

## 13. Source index (all URLs used)
- NREL OpenStudio-HPXML (MJ8/Manual S implementation, ASHRAE 62.2 code, defaults, docs), commit f28d40e: https://github.com/NREL/OpenStudio-HPXML/tree/f28d40e397e9972a19a366600207c754efbf2eec (files: HPXMLtoOpenStudio/resources/hvac_sizing.rb, airflow.rb, defaults.rb, hvac.rb, data/ashrae622_wsf.csv; docs/source/workflow_inputs.rst) [V]
- NREL ResStock options_lookup.tsv (ccASHP normalized performance), commit dd25369: https://github.com/NREL/resstock/blob/dd25369f41a83a0767aefeeac0b6f8a0b0edd649/resources/options_lookup.tsv [V]
- ACCA Outdoor Design Conditions guide (MJ8 v2 Table 1A): https://higherlogicdownload.s3.amazonaws.com/ACCA/c6b38bda-2e04-4f93-bd51-7a80525ad936/UploadedImages/Outdoor-Design-Conditions-1.pdf [V]; MJ8 Addendum E weather data: https://higherlogicdownload.s3.amazonaws.com/ACCA/8e4cf5b4-e984-4971-bb79-7889082c7cf2/UploadedImages/MJ8-Adden-E-Updated-Weather-Data-11Aug2014.pdf [V]
- ACCA Manual S 2023 proposed addendum c: https://higherlogicdownload.s3.amazonaws.com/ACCA/c6b38bda-2e04-4f93-bd51-7a80525ad936/UploadedImages/Manual_S_Addendum_C_03062025.pdf [V]
- ACCA code references (IRC M1401.3 / M1601.1 / IECC R403.7 point to Manuals J/S/D): https://higherlogicdownload.s3.amazonaws.com/ACCA/c6b38bda-2e04-4f93-bd51-7a80525ad936/UploadedImages/2018_Model_Code_References_42518.pdf [V]
- ASHRAE 2009 design days for Bellingham Intl AP (TMY3 727976): https://github.com/BuildingComponentLibrary/design-day-components-1 [V]
- WA IRC 2021 with amendments (scraped): https://github.com/thexqin/us-building-codes-dataset/tree/main/download-v2/washington/irc-2021 [V]; primary: https://codes.iccsafe.org/content/WARC2021P1 (not fetched)
- WSEC Table RC-1: https://www.law.cornell.edu/regulations/washington/WAC-51-11R-60100 [S]
- WSU heating-sizing calculator copies and instructions: https://permitbulletin.mercerisland.gov/public/2407-071/SUB1/2018-2021%20heating%20system%20sizing%20worksheet20240326.pdf ; https://permitbulletin.mercerisland.gov/public/2512-087/SUB1/2021%20heating%20system%20sizing%20worksheet.pdf ; https://permitbulletin.mercerisland.gov/public/2407-069/SUB1/wsec-r%20heating%20system%20sizing%20worksheet.pdf ; https://permitbulletin.mercerisland.gov/public/2504-058/SUB1/lin%20kicska%20heating%20system%20sizing%20worksheet%2004.01.2025.pdf ; http://permits.kirklandwa.gov/WebDocs/2018061822/d81cf5af-080e-46f8-93ae-a369d2db2b10.pdf ; https://web.seattle.gov/dpd/edms/GetDocument?id=7446210 ; https://wpcdn.web.wsu.edu/cahnrs/uploads/sites/60/2026/05/2018-Heating-System-Sizing-Calculator-Instructions.pdf ; https://bainbridgewa.gov/DocumentCenter/View/14891/2018-Heating-System-Sizing-Calculator-Instructions ; https://www.energy.wsu.edu/Documents/BFG%20Chapter%207-Jan2011.pdf ; https://energy.wsu.edu/our-work/building-efficiency/washington-state-residential-energy-code-technical-support-and-education/wsec-r-2021-code-forms-and-resources/ [S]
- N-factor: https://www.greenbuildingadvisor.com/question/what-is-n-factor ; https://building-performance.org/bpa-journal/ach50-achnat/ [S]
- Manual S secondary summaries: https://www.energyvanguard.com/attachment/acca-manual-s-air-conditioner-sizing-limits/ ; https://www.hvacproblog.com/top_5_changes_to_acca_manual_s [S]
- fluids library (fitting K correlations): https://github.com/CalebBell/fluids [C]
- Not fetched (blocked), cited for the reader to verify: https://www.acca.org/standards/technical-manuals/manual-d ; https://www.ashrae.org/technical-resources/ashrae-handbook ; https://neep.org/heating-electrification/ccashp-specification-product-list ; https://ashp.neep.org ; https://www.energystar.gov/products/heat_pumps_air_source ; https://www.hvi.org/hvi-certified-products-directory/ ; https://www.mitsubishicomfort.com ; https://mylinkdrive.com ; https://www.fujitsugeneral.com/us/ ; https://daikincomfort.com ; https://na.panasonic.com/us/ [U]
