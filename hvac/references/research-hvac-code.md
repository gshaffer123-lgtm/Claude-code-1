# HVAC code, energy code, ventilation, permits and inspections - WA - research digest (agent, 9/25/2026)

Scope: new single-family houses and duplexes in northwest Washington: Whatcom County (unincorporated, including Sudden Valley and Glenhaven Lakes), the City of Bellingham, the City of Blaine, Skagit County, and San Juan County (including Shaw Island). The permit is assumed to be applied for in calendar 2026. The digest feeds an HVAC takeoff and bidding skill. Every figure carries a URL. Anything not confirmed in this session is tagged as described in section 0.

---

## 0. How to read this digest (confidence tags and retrieval notes)

### 0.1 Confidence tags (every figure carries one)

| Tag | Meaning | How the bidding skill should treat it |
|---|---|---|
| **[V]** | Verified this session from a search-engine extract of the cited page. The page itself could not be opened (see 0.2), so the wording is an extract or paraphrase, not a full reading. | Usable. Re-read the cited page before the number goes on a contract. |
| **[P]** | Partial. The extract was ambiguous, the edition was uncertain, or a number was inferred from surrounding text. | Show it as "probable", and always confirm it. |
| **[U]** | UNVERIFIED. This comes from the agent's background knowledge (model code text, training data up to mid-2026). It was not confirmed this session. The URL shows where to verify it and was not opened. | Do not treat it as sourced. Confirm it before use. The IRC model-code text is generally reliable, but Washington amendments may differ. |
| **NOT FOUND** | Could not be located before the search budget ran out. | Leave blank in the skill, or ask the user. |

### 0.2 Retrieval notes (why so much is [U])

- **WebFetch was blocked by the network egress proxy for every domain tried**: `app.leg.wa.gov`, `lawfilesext.leg.wa.gov`, `sbcc.wa.gov`, `energy.wsu.edu`, `wpcdn.web.wsu.edu`, `up.codes`, `codes.iccsafe.org`, `www.law.cornell.edu`, `www.islandcountywa.gov`, `washingtonstatestandard.com`, `www.knkx.org`, `www.epa.gov`, and `www.ecfr.gov`. Each returned `EGRESS_BLOCKED`.
- **A direct `curl` from the shell** to `https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40300` failed with `CONNECT tunnel failed, response 403`.
- **WebSearch was the only working channel.** Its result extracts were used as quoted evidence. Partway through this task the session-wide cap was reached ("200 of 200 WebSearch calls", shared with other agents in the session). No further searches were possible. As a result:
  - Sections 1 and 3 are largely [V] or [P].
  - Sections 2, 4, 5 and 6 are mostly [U].
  - Sections 7 and 8 (design temperatures and fee schedules) are mostly NOT FOUND.
- A follow-up verification pass needs either a higher search cap (`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`) or egress allow-listing for `app.leg.wa.gov`, `lawfilesext.leg.wa.gov`, `sbcc.wa.gov` and `energy.wsu.edu`. Section 10 lists the exact pages to open.

### 0.3 Ten bid facts (details in the sections below)

1. The code in force for 2026 applications is the **2021 WSEC-R** (chapter 51-11R WAC), effective **March 15, 2024** [V]. The **2024 codes** are scheduled to take effect **May 3, 2027** [V-extract]. See section 1.
2. **No heat pump is mandated.** The 2021 heat-pump space-heating section R403.13 was deleted before the code took effect (WSR 23-21-105, then WSR 24-03-084) [V]. Gas furnaces and electric resistance are legal. The penalty is paid in R406 credits. See sections 1.4 and 3.
3. **I-2066 is dead.** The WA Supreme Court struck it down 6-3 on **September 17, 2026**, affirming the King County Superior Court ruling of **March 21, 2025** [V]. The SBCC told jurisdictions to apply the 2021 standards [V-extract].
4. **Credits required (2021, per dwelling unit):** small **5.0**, medium **8.0**, large **9.0** [V]. The 2018 code required **3.0 / 6.0 / 7.0** [V].
5. **Table R406.2 (2021), credits by heating system:**
   - combustion: **0**
   - heat pump with supplemental resistance or furnace: **1.5**
   - electric resistance only: **0.5**
   - resistance plus an inverter ductless heat pump in the largest zone: **2.0**
   - heat pump (including air-to-water): **3.0** [V]
6. **Option number to system type (2021 Table R406.3):**
   - 3.1: 95% furnace or 90% boiler (System Type 1)
   - 3.2: 95% backup furnace for a System Type 2 hybrid
   - 3.3: ducted air-source heat pump, HSPF2 ≥ 8.1
   - 3.4: ground source
   - 3.5: ductless mini-split
   - 3.6: ducted air-source heat pump, HSPF2 ≥ 9.4
   - 3.7: air-to-water heat pump [V/P]
   - Most credit values beyond 3.1 = 1 are NOT FOUND. The full mapping, including 2018, is in section 3.8.
7. **Whole-house mechanical ventilation** is required in every new WA dwelling. The rate is 0.01 × CFA + 7.5 × (bedrooms + 1) [U]. Duct leakage and ventilation-flow test reports are part of final [U]. See sections 2 and 5.
8. **Refrigerant:** new split AC and heat pump systems must use a GWP < 700 refrigerant (R-454B or R-32, which are A2L). The EPA installation deadline for R-410A split systems built before 2025 was **January 1, 2026** [U]. Section 6 has the rest.
9. **Design temperatures and permit fees for the five jurisdictions were NOT FOUND.** The WSEC-R's own design-temperature source is **Appendix RC**. A winter design temperature of **≤ 23°F** triggers a cold-climate heat pump requirement for credit 3.3 [V]. See sections 7 and 8.
10. **Open question: resistance backup strips.** Does a ducted heat pump with electric strips count as System Type 5 (3.0 credits) or Type 2 (1.5 credits)? The code note describes a **38°F changeover** for Type 2 [P]. Resolve this against the WAC footnotes before pricing hybrid or strip-heat designs (section 3.2).

---

## 1. Codes in force for a permit applied for in 2026

### 1.1 Adopted codes and effective dates

| Code | WAC chapter | Effective | Status for a 2026 application | Source / tag |
|---|---|---|---|---|
| 2021 WA State Energy Code - Residential (WSEC-R) | 51-11R | **March 15, 2024**, "in all counties and cities" | **In force** | WSR 24-03-084 (permanent rule, effective 3/15/2024) https://lawfilesext.leg.wa.gov/law/wsr/2024/03/24-03-084.htm ; SBCC order https://sbcc.wa.gov/sites/default/files/2024-01/WSR_24_03_084_WSEC_R_Comb.pdf **[V]** |
| 2018 WSEC-R (prior edition) | 51-11R (prior text) | Superseded 3/15/2024. The WAC archive copy is marked "(Effective until March 15, 2024)". | Applies only to applications vested before 3/15/2024. **Older plan sets still carry 2018 option numbers.** | https://lawfilesext.leg.wa.gov/law/WACArchive/2023/htm/WAC%20%2051%20%20TITLE/WAC%20%2051%20-%2011R%20CHAPTER/WAC%20%2051%20-%2011R-40610.htm **[V]** (start date 2/1/2021 **[U]**) |
| 2021 IRC as amended by WA | 51-51 | 3/15/2024 | In force | **[U]**. The date matches the energy code, but no IRC-specific source was opened. Verify at https://app.leg.wa.gov/wac/default.aspx?cite=51-51 (not opened). |
| 2021 IMC / IFGC / NFPA 54/58 as amended | 51-52 | 3/15/2024 | In force (fuel gas, IMC items) | **[U]**. Verify at https://app.leg.wa.gov/wac/default.aspx?cite=51-52 (not opened). |
| 2021 UPC (plumbing, used instead of the IRC plumbing chapters) | 51-56 | 3/15/2024 | In force | **[U]**. Verify at https://app.leg.wa.gov/wac/default.aspx?cite=51-56 (not opened). |
| **2024 WA codes** (IBC, IRC, IMC, WSEC and others) | 51-11R, 51-51 and others | **May 3, 2027** (per SBCC) | Not yet in force. A permit applied for in 2026 is under the 2021 codes. | SBCC site extract: "As per the SBCC meeting on January 23, 2026, the Council unanimously approved to delay the final adoption of the 2024 Washington State Building Codes until August 21, 2026 ... The effective date of the 2024 codes will be May 3, 2027." https://sbcc.wa.gov/ and https://sbcc.wa.gov/state-codes-regulations-guidelines/rulemaking **[V-extract]**. Whether final adoption actually happened on 8/21/2026 is NOT FOUND. |

### 1.2 2024 WSEC-R rulemaking trail (for when the 2027 edition arrives)

- **CR-101 (preproposal)** for the 2024 WSEC-R was filed on **April 1, 2025** as WSR 25-08-086: https://lawfilesext.leg.wa.gov/law/wsr/2025/08/25-08-086.htm **[V-extract]**.
- The SBCC received **48 petitions** for the 2024 WSEC-R and approved **22** for the draft rule [V-extract]. The public comment period ran **May 6 to June 12, 2026** (https://sbcc.wa.gov/state-codes-regulations-guidelines/rulemaking) [V-extract].
- **CR-102 (proposed rule)** for the 2024 WSEC-R was filed on 7/1/2026, judging by the file name:
  - https://sbcc.wa.gov/sites/default/files/2026-07/2024WSEC_R_FiledCR102_070126.pdf
  - WSR 26-14-101: https://lawfilesext.leg.wa.gov/law/wsr/2026/14/26-14-101.htm **[P]** (title and URL only)
- Draft "2024 Washington State Energy Code - Residential Provisions, June 2026": https://sbcc.wa.gov/sites/default/files/2026-06/ResNRG_pCBA_full_v2_062426.pdf **[V-title]**. Its content was not reviewed.
- WSU has published a 2024 forms page: https://energy.wsu.edu/our-work/building-efficiency/washington-state-residential-energy-code-technical-support-and-education/wsec-r-2024-code-forms-and-resources/ **[V-title]**.
- A BIAW analysis exists: https://housingstudies.biaw.com/reports/washingtons-2024-residential-energy-code **[V-title]**.
- **What the 2024 WSEC-R does to heat pumps and credits: NOT FOUND.**

### 1.3 How the 2021 WSEC-R reached its current form (the heat pump mandate)

1. **As adopted in November 2022**, the 2021 WSEC-R required heat pumps. Energy Trust quotes it: "The 2021 WSEC-R explicitly states that 'space heating shall be provided by a heat pump system.'" (https://insider.energytrust.org/new-2021-washington-state-energy-code/) **[V-extract]**. That text never took effect.
2. **Legal trigger:** "legal uncertainty stemming from the decision in California Restaurant Association v. City of Berkeley recently issued by the Ninth Circuit" (WSR 24-03-084 purpose statement, https://lawfilesext.leg.wa.gov/law/wsr/2024/03/24-03-084.htm) **[V]**.
3. **Proposed fix, WSR 23-21-105 (October 2023):**
   - "Section R403.13 (Heat pump space heating) was removed and reserved."
   - Table R406.3 "was modified to reorder the high efficiency HVAC equipment options and update the user notes for those options, as well as provide HSPF2 efficiency values in addition to HSPF values."
   - Sources: https://lawfilesext.leg.wa.gov/law/wsr/2023/21/23-21-105.htm and https://lawfilesext.leg.wa.gov/law/wsrpdf/2023/21/23-21-105.pdf **[V-extract]**
4. **Final rule:** adopted as WSR 24-03-084, **effective March 15, 2024** [V].
5. BetterBuiltNW summarizes the result:
   - "Changes from the draft to the final 2021 WSEC include removing the heat pump requirement for space and water heating."
   - "There are five heating system types, and credits range from zero for combustible fuels to three for a heating system using an efficient electric heat pump."
   - "Homes with combustible fuels, like natural gas, must obtain more energy credits than homes using electric heat pumps."
   - The final code has "29 different energy credits across seven categories."
   - Source: https://betterbuiltnw.com/news/washington-state-energy-code-updates-what-to-know **[V-extract]**

### 1.4 Initiative 2066: timeline and legal status

| Date | Event | Source / tag |
|---|---|---|
| Nov 5, 2024 | I-2066 approved by voters. It barred the SBCC and local governments from prohibiting, penalizing or discouraging gas. | https://en.wikipedia.org/wiki/2024_Washington_Initiative_2066 ; https://ballotpedia.org/Washington_Initiative_2066,_Natural_Gas_Policies_Measure_(2024) **[V-extract]** |
| ~Dec 5, 2024 | Effective date (30 days after the election) | **[U]** |
| Nov 2024 | SBCC "not ready to scrap" the targeted codes, then began a review | https://washingtonstatestandard.com/2024/11/15/state-panel-not-ready-to-scrap-building-codes-targeted-by-gas-initiative/ ; https://washingtonstatestandard.com/2024/11/22/state-panel-will-begin-review-of-building-codes-targeted-by-gas-initiative/ **[V-title]** |
| Feb 10 to Apr 7, 2025 | SBCC submittal window for "I-2066 compliance amendments" to the 2021 WSEC-C and WSEC-R | https://sbcc.wa.gov/state-codes-regulations-guidelines/rulemaking **[V-extract]** |
| Feb 14, 2025 | A judge declined to compel the SBCC to scrap the targeted codes | https://washingtonstatestandard.com/2025/02/14/judge-wont-compel-state-panel-to-scrap-building-codes-targeted-by-gas-initiative/ **[V-title]** |
| 2025 (date not captured) | SBCC voted **10-2** against finding an emergency on a BIAW petition. No emergency rule was adopted. | https://citizenportal.ai/articles/6338802/washington/executive/governors-office-boards-commissions/building-code-council/state-building-code-council-rejects-emergency-rulemaking-request-tied-to-initiative-2066 **[V-extract]** |
| **Mar 21, 2025** | King County Superior Court Judge **Sandra Widlan** held I-2066 unconstitutional: "I-2066 violates the single subject requirement, the subject and title requirement, and the section-amended-shall-be-set-forth-at-full-length requirement." | https://washingtonstatestandard.com/2025/03/21/judge-overturns-washington-natural-gas-measure-approved-by-voters/ ; https://www.columbian.com/news/2025/mar/23/king-county-judge-natural-gas-measure-is-unconstitutional/ **[V]** |
| June 2025 | Appeal filed by Attorney General Nick Brown and BIAW | https://washingtonstatestandard.com/2026/01/22/legal-fight-over-natural-gas-initiative-crescendoes-at-wa-supreme-court/ **[V-extract]** |
| Jan 2026 | WA Supreme Court oral argument | same URL **[V-extract]** |
| **Sept 17, 2026** | WA Supreme Court **6-3 affirmed**: I-2066 is "unconstitutional in its entirety" under the single-subject rule and cannot be severed. Justice Sal Mungia dissented, joined by Justices Gordon McCloud and C. Johnson. | https://washingtonstatestandard.com/2026/09/17/wa-high-court-tosses-natural-gas-measure-approved-by-voters/ ; https://www.axios.com/local/seattle/2026/09/17/washington-supreme-court-strikes-down-natural-gas-initiative-2066 ; https://www.sierraclub.org/press-releases/2026/09/momentous-win-clean-air-and-energy-affordability-wa-supreme-court-strikes **[V]** |
| After Sept 17, 2026 | "The Washington State Building Code Council has advised local jurisdictions ... to abide by 2021 standards that disincentivize natural gas." | https://www.koin.com/news/washington/taken-that-choice-away-washington-supreme-court-blocks-voter-backed-energy-choice-initiative/ **[V-extract]** |

**How jurisdictions handled 2025-2026 (the gap years):**

- **Pierce County:** after the Superior Court ruling, it "will continue accepting, processing, and reviewing building permits under the currently adopted building codes, including the 2021 Washington State Energy Code" [V-extract]. Earlier it had issued a bulletin on "how they are interpreting the application of energy equalization credits" and an amended Single-Family Worksheet [V-extract]. Sources: https://www.piercecountywa.gov/CivicSend/ViewMessage/message/256424 and https://www.piercecountywa.gov/m/newsflash/Archive/Item/6772?arcId=11930
- **Clark County:** "implemented a temporary solution to align with the intent of the law" (https://www.biaw.com/news/initiative-2066---whats-the-latest) [V-extract].
- **Mountlake Terrace:** issued an "Energy Code & I-2066 Compliance" technical bulletin (https://www.cityofmlt.com/DocumentCenter/View/38060/MLT-Energy-Code-Technical-Bulletin) [V-title].
- **Whatcom County, Bellingham, Blaine, Skagit County, San Juan County:** interim I-2066 policies NOT FOUND. Treat any plan set from 2025 or 2026 that claims "equalization" credits for gas with suspicion.

### 1.5 Bottom line: what a builder must install today (a 2026 application under the 2021 WSEC-R)

- **A heat pump is NOT required** for primary space heating. R403.13 was deleted before the 2021 code took effect [V: WSR 23-21-105 / 24-03-084].
- **Gas or propane furnaces, boilers and electric resistance are all legal.** The price is energy credits. The total required is the same for every fuel (section 3.1). The heating-system credit from Table R406.2 differs, so a non-heat-pump house must buy more credits from Table R406.3.
- **Credits still needed from Table R406.3 after the Table R406.2 heating credit** (2021; small / medium / large require 5.0 / 8.0 / 9.0) [V arithmetic on V values]:

| Primary heating (Table R406.2 row) | R406.2 credit | Small still needs | Medium still needs | Large still needs |
|---|---|---|---|---|
| Heat pump, including air-to-water (type 5*) | 3.0 | 2.0 | 5.0 | 6.0 |
| Zonal or forced-air resistance plus an inverter ductless heat pump in the largest zone (type 4*) | 2.0 | 3.0 | 6.0 | 7.0 |
| Heat pump plus supplemental resistance or combustion furnace (type 2) | 1.5 | 3.5 | 6.5 | 7.5 |
| Electric resistance only (type 3*) | 0.5 | 4.5 | 7.5 | 8.5 |
| Combustion: gas or propane furnace or boiler (type 1) | 0 | 5.0 | 8.0 | 9.0 |

*Type numbers marked * are inferred from ordering. The credit values are [V]. See section 3.2.

- **Cost to a gas-furnace house:** it needs **3 more R406.3 credits** than a heat pump house of the same size. Option 3.1 (95% AFUE Energy Star furnace) gives back about 1 credit [P]. In practice gas houses stack envelope options, air-leakage and HRV options, and heat pump water heating.
- **Duplexes:** the credits apply **per dwelling unit** ("Each dwelling unit in a residential building shall comply with sufficient options ...", https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40620) [V-extract]. Each side needs its own compliant system.
- **Local ordinances to check (NOT VERIFIED):**
  - Whether the City of Bellingham has a local electrification amendment for new residential construction was NOT checked this session. It is the most likely local deviation in the study area.
  - The I-2066 ruling removes the state-law bar on such local measures.
  - Confirm with the Bellingham Permit Center before bidding gas heat in city limits.

---

## 2. WSEC-R 2021 Section R403 (systems) as adopted in WA

The WAC section pages could not be opened. The known WAC cite is **WAC 51-11R-40320 = "Section R403.3 - Ducts"** (https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40320) [V-title]. The whole chapter is at https://app.leg.wa.gov/wac/default.aspx?cite=51-11R&full=true. The best single verification source is the SBCC 2021 WSEC-R 2nd edition PDF: https://sbcc.wa.gov/sites/default/files/2024-01/2021_WSEC_R_2ndEd_012524.pdf (not opened).

Items tagged [U] below follow the **2021 IECC model text, which WA adopts with amendments**. WA-specific wording may differ.

### 2.1 R403.1 Controls (Mandatory) [U]

- **R403.1:** at least one thermostat for each separate heating and cooling system [U].
- **R403.1.1 Programmable thermostat** [U]:
  - It must hold different setpoints by time of day and day of week.
  - It must be able to set back to **55°F** and set up to **85°F**.
  - Factory default setpoints: heating no higher than **70°F**, cooling no lower than **78°F**.
  - A WSEC-R 2021 section titled "Dwelling unit HVAC controls" exists (https://up.codes/s/dwelling-unit-hvac-controls) [V-title]. Its content was not read.
- **R403.1.2 Heat pump supplementary heat (Mandatory)** [U]:
  - "Heat pumps having supplementary electric-resistance heat shall have controls that, except during defrost, prevent supplemental heat operation when the heat pump compressor can meet the heating load."
  - Bid implication: an outdoor-temperature lockout or a smart thermostat with auxiliary-heat lockout, plus staging.
  - Any WA-specific lockout temperature: NOT FOUND.

### 2.2 R403.3 Ducts

| Item | Requirement | Tag / source |
|---|---|---|
| Duct insulation outside conditioned space | Attic supply and return ducts: **R-8** for ducts ≥ 3 in. diameter, **R-6** for ducts < 3 in. Other unconditioned locations (crawl, garage): **R-6** for ≥ 3 in., **R-4.2** for < 3 in. (2021 IECC R403.3.1). WA has historically also said ducts buried beneath a building must be insulated per this section or have an equivalent listed thermal distribution efficiency. | **[U]** Verify at https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40320 |
| Deeply buried ducts (attic) | "Where supply and return air ducts are partially or completely buried in ceiling insulation, such ducts shall have an insulation R-value not less than **R-8**, and at all points along each duct, the sum of the ceiling insulation R-value against and above the top of the duct, and against and below the bottom of the duct, shall be not less than **R-19**, excluding the R-value of the duct insulation." | **[V-extract]**, from search results listing https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40320 and https://up.codes/viewer/washington/wa-energy-code-residential-provisions-2021/chapter/RE_4/re-residential-energy-efficiency |
| Ducts "inside conditioned space" | "All duct systems shall be located completely within the continuous air barrier and within the building thermal envelope." | **[V-extract]**, same sources |
| Sealing (Mandatory) | Ducts, air handlers and filter boxes sealed per IRC M1601.4.1 (UL 181A/B tapes and mastics, mechanically fastened connections). Building framing cavities are not used as supply ducts. | **[U]** |
| Duct testing (Mandatory) | Total leakage measured at **25 Pa (0.1 in. w.c.)**, either at rough-in (air handler installed or not) or post-construction. Registers taped. A signed written report goes to the code official. The code official may require an approved third party. | **[U]** (2021 IECC R403.3.5). A WA-specific article exists: https://www.pnwig.com/blog-category/energy-efficiency/blogs?blog_id=duct-testing-requirement-for-2021-wa-state-code **[V-title only]** |
| Duct leakage limits (Prescriptive), total leakage | Rough-in with air handler installed: **≤ 4.0 cfm25 per 100 sf CFA**. Rough-in without air handler: **≤ 3.0 cfm25/100 sf**. Post-construction: **≤ 4.0 cfm25/100 sf**. All ducts and air handler inside the thermal envelope: **≤ 8.0 cfm25/100 sf** (2021 IECC R403.3.6). | **[U]**. WA 2021 values NOT VERIFIED. WA 2018 used 4.0 / 3.0 / 4.0 **[U]**. |
| Exceptions | 2021 IECC: no test for ducts serving HRVs or ERVs that are not integrated with heating or cooling ducts. Under 2021 IECC, ducts entirely inside the envelope are still tested, against the 8.0 limit. Whether WA kept an "all inside the envelope = no test" exception: NOT VERIFIED. | **[U]** |

### 2.3 R403.4 Mechanical system piping insulation (Mandatory) [U]

- Piping that carries fluids **above 105°F or below 55°F** must be insulated to at least **R-3**. That covers hydronic and chilled-water piping.
- Insulation exposed to weather must be protected from sun, moisture and wind (R403.4.1).
- **Refrigerant suction lines** are also covered by IRC M1411: **R-4** minimum, vapor-retarding (see section 5.4).
- Source: 2021 IECC R403.4. Verify in https://sbcc.wa.gov/sites/default/files/2024-01/2021_WSEC_R_2ndEd_012524.pdf

### 2.4 R403.6 Mechanical ventilation (Mandatory)

- **Whole-house ventilation is required** in every new WA dwelling. It is sized under IRC M1505 as amended by WA (section 5.8) [U].
- Outdoor air intakes and exhausts need automatic or gravity dampers that close when the system is off [U].
- **Fan efficacy** [U]. 2021 IECC Table R403.6.2 values. WA's 2021 table is NOT VERIFIED:

| Fan type | Airflow range | Minimum efficacy |
|---|---|---|
| HRV / ERV | any | 1.2 cfm/W |
| In-line supply or exhaust fan | any | 3.8 cfm/W |
| Other exhaust fan | < 90 cfm | 2.8 cfm/W |
| Other exhaust fan | ≥ 90 cfm | 3.5 cfm/W |
| Air handler integrated into tested and listed HVAC equipment | any | 1.2 cfm/W |

  - The WA 2018 table was: HRV/ERV 1.2; range hood 2.8; in-line fan 2.8; bath or utility fan 10 to < 90 cfm 1.4; bath or utility ≥ 90 cfm 2.8 cfm/W [U].
- **Heat recovery ventilation:** not mandatory for single-family homes [U]. It becomes required only when the builder selects the R406 air-leakage and ventilation credits 2.2 and up (section 3.5).
- **Ventilation flow testing** [U]:
  - 2021 IECC R403.6.3 requires mechanical ventilation systems to be "tested and verified to provide the minimum ventilation flow rates," using a flow hood, flow grid or other airflow measuring device.
  - The code official may require a third party. A signed report is required.
  - The only exception is range hoods ducted with 6-in. or larger duct and at most one 90° elbow.
  - WA adoption and wording: NOT VERIFIED. A WA IRC ventilation-flow verification also exists in M1505 [U] (section 5.8).

### 2.5 R403.7 Equipment sizing (Mandatory) [U]

- "Heating and cooling equipment shall be sized in accordance with **ACCA Manual S** based on building loads calculated in accordance with **ACCA Manual J** or other approved heating and cooling calculation methodologies."
- New equipment must meet the federal minimum efficiency.
- The same rule appears in IRC M1401.3 (section 5.2).
- The WSU "Simple Heating System Size: Washington State" calculator and its location list: NOT FOUND. energy.wsu.edu was egress-blocked. The user reports that it shows a Seattle design temperature difference of 46 (70 − 24); that is unverified here.
- **Code design temperatures:** the 2021 WSEC-R cites "the winter design temperature as specified in **Appendix RC**" [V-extract, from https://www.kirklandwa.gov/files/sharedassets/public/v/3/development-services/pdfs/building-pdfs/wsec-r-plan-sheet.pdf and the WSU worksheets]. See section 7.

### 2.6 R403.13 Heat pump space heating: DELETED

- It was removed and reserved by WSR 23-21-105 and adopted in WSR 24-03-084, effective 3/15/2024 [V].
- What it said (never in force): "space heating shall be provided by a heat pump system" [V-extract, Energy Trust].
- Its resistance allowance: an extract describes "an alternative heating source sized at a maximum of **0.5 Watts/ft²** (equivalent) of heated floor area or **500 Watts**, whichever is bigger" [P; edition and section uncertain]. Search results pointed at https://sbcc.wa.gov/sites/default/files/2022-06/065_TM_HP_Space_060722.pdf and https://sbcc.wa.gov/sites/default/files/2021-06/2021%20WA%20Code%20Change%20-%20Heat%20Pump%20Space%20Heating.pdf

### 2.7 Electric-resistance limits that still matter

- **2018 WSEC-R, Table R406.2 footnote a:** a **0.5 W/sf** resistance "budget" alongside a heat pump or ductless heat pump.
  - WSU FAQ extract: "if 1,500 watts of electric resistance heat is installed in smaller zones and exceeds the 0.5 watt per square foot budget in footnote a, this would qualify as System Type 4 for 0.5 fuel normalization credits" (https://www.energy.wsu.edu/documents/FAQ%20Two%20heating%20systems.pdf) [V-extract].
  - The same FAQ says that with two heating systems, credits follow the **primary** system, meaning the one serving the larger heating load [V-extract].
- **2021 WSEC-R:** there is no mandatory resistance cap for single-family homes. Resistance only moves the Table R406.2 row: resistance only = 0.5, resistance plus a ductless heat pump in the largest zone = 2.0 [V].
  - An extract (Clark County checklist) mentions an inverter mini-split in the largest zone "or electric resistance heating, with the combined system not exceeding 2kW" (https://clark.wa.gov/sites/default/files/media/document/2024-11/2021-wsec-compliance-checklist_0.pdf) [P].
  - Another extract ties "**2 kW or less** total installed heating capacity per dwelling" to the ductless option. This appears to be the Group R-2 (apartment) variant [P].

---

## 3. WSEC-R R406 additional energy-efficiency credits (key deliverable)

Primary tables:

- 2021: Section R406.3 at https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40620 and Table R406.3 at https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40621 (archived HTML: https://lawfilesext.leg.wa.gov/Law/WACArchive/2024/htm/WAC%20%2051%20-%2011R%20CHAPTER/WAC%20%2051%20-%2011R-40621.htm).
- 2018: https://lawfilesext.leg.wa.gov/law/WACArchive/2020/pdf/WAC%20%2051%20%20TITLE/WAC%20%2051%20-%2011R%20CHAPTER/WAC%20%2051%20-%2011R-40621.pdf
- Best consolidated secondary sources:
  - WSU 2021 Single Family Work Sheet: https://www.energy.wsu.edu/documents/2021%20WSEC-R%20Single%20Family%20Work%20Sheet%2020241212.pdf (mirror: https://wpcdn.web.wsu.edu/cahnrs/uploads/sites/60/2026/05/2021-WSEC-R-Single-Family-Work-Sheet-20241212.pdf)
  - WSU "Energy Credit Requirements and Credit Options R406.3": https://wpcdn.web.wsu.edu/cahnrs/uploads/sites/60/2026/05/Energy-Credit-Requirements-and-Credit-Options-R406.3.pdf

None of these could be opened. Everything below comes from search extracts plus clearly tagged recall.

### 3.1 Credits required per dwelling unit

| Dwelling category | Definition | 2021 WSEC-R (≥ 3/15/2024) | 2018 WSEC-R (2021 to 3/14/2024) |
|---|---|---|---|
| Small | < 1,500 sf conditioned floor area **and** < 300 sf fenestration | **5.0** [V] | **3.0** [V] |
| Medium | Everything not small or large | **8.0** [V] | **6.0** [V] |
| Large | > 5,000 sf conditioned floor area | **9.0** [V] | **7.0** [V] |
| Group R-2 dwelling units (apartments, not IRC duplexes) | Per R-2 column | 6.5 [P] | NOT FOUND |
| Additions | Smaller credit requirement | 1.5 for < 500 sf **[U]** | **[U]** |

Sources:
- 2021: https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40620 ; https://sbcc.wa.gov/sites/default/files/2024-01/2021_WSEC_R_2ndEd_012524.pdf ; https://www.islandcountywa.gov/DocumentCenter/View/6622/2021WSEC-R-SingleFamilyWorkSheet [V-extract]
- 2018: https://up.codes/viewer/washington/wa-energy-code-residential-provisions-2018/chapter/RE_4/re-residential-energy-efficiency ; https://sanjuancountywa.gov/DocumentCenter/View/10444/Energy-form---standard-residential-2018-WSEC---PDF ; Cascade Natural Gas "Pathway to 6.0 Credits" handout https://www.cngc.com/wp-content/uploads/PDFs/energy_choice/washington/2018_WSEC-R-Pathway-to-6.0-Credits_Handout.pdf [V-extract]

How the two tables combine:
- "Each dwelling unit in a residential building shall comply with sufficient options from Tables R406.2 and R406.3 to achieve the following minimum number of credits" [V-extract].
- R406.2 is titled "Carbon emission equalization" (https://up.codes/s/carbon-emission-equalization) [V-title].
- "The permit shall define the base fuel selection to be used and the points specified in Table R406.2 shall be used to modify the requirements in Section R406.3" [V-extract].

### 3.2 2021 WSEC-R Table R406.2: heating system type credits (in force)

| System type | Description of primary heating source (extract wording) | Credits, "All Other" (single-family and duplex) | Tag |
|---|---|---|---|
| **1** | Heating system based on **combustion** equipment meeting minimum federal efficiency standards (Tables C403.3.2(4) / C403.3.2(5)) | **0** | [V]. Type number confirmed by the Kirkland plan sheet: "For a System Type 1 in Table R406.2: Energy Star rated (U.S. North) Gas or propane furnace ..." |
| **2** | "Initial heating system using a **heat pump** that meets federal standards for the equipment listed in Table C403.3.2(2) AND **supplemental heating provided by electric resistance or a combustion furnace** meeting minimum standards listed in Table C403.3.2(5)" | **1.5** | [V]. Type number confirmed by extracts. |
| 3 (inferred) | Heating system based on **electric resistance only** (either forced air or zonal) | **0.5** | [V] value; [P] type number |
| 4 (inferred) | Heating system based on **electric resistance with an inverter-driven ductless mini-split heat pump** installed in the **largest zone** of the dwelling | **2.0** | [V] value; [P] type number |
| 5 (inferred) | Heating system using a **heat pump** meeting federal standards (Tables C403.3.2(2) or C403.3.2(9)), **or air-to-water heat pump** units configured for both heating and cooling and rated to AHRI 550/590 | **3.0** | [V] value; [P] type number |

- Group R-2 column: NOT FOUND. It is not needed for IRC single-family and duplex work.
- Sources: extracts from searches returning https://www.kirklandwa.gov/files/sharedassets/public/v/3/development-services/pdfs/building-pdfs/wsec-r-plan-sheet.pdf ; https://clark.wa.gov/sites/default/files/media/document/2024-11/2021-wsec-compliance-checklist_0.pdf ; https://wpcdn.web.wsu.edu/cahnrs/uploads/sites/60/2026/05/2021-WSEC-R-Single-Family-Work-Sheet-20241212.pdf ; https://sbcc.wa.gov/sites/default/files/2022-09/OTS-4009.2%20Replacement%20page%2056.pdf ; https://betterbuiltnw.com/news/washington-state-energy-code-updates-what-to-know

**Type 2 vs Type 5, the backup-heat question (bid-critical, [P]):**
- A search restricted to app.leg.wa.gov (WAC 51-11R-40620) returned this note: "a gas back-up furnace will operate as fan-only when the heat pump is operating, with the heat pump operating at all temperatures above **38°F**, and below that 'changeover' temperature, the heat pump would not operate to provide space heating."
- So Type 2 is the "initial heat pump plus backup" design: dual-fuel, or a heat pump that hands off to resistance below a changeover temperature.
- A heat pump sized for the design load, with strips only for defrost or emergency and locked out per R403.1.2, is most plausibly Type 5 (3.0).
- Confirm against the Table R406.2 footnotes before pricing a strip-heat air handler as "3.0 credits".

### 3.3 2018 WSEC-R Table R406.2: fuel normalization credits (older plan sets)

| System type | Description | Credit | Tag / source |
|---|---|---|---|
| 1 | Combustion heating meeting minimum (NAECA) efficiency | **0** | [V-extract], from searches returning https://customdiggs.com/wp-content/uploads/2022/04/2018-Energy-Credits-Table.pdf and https://go2kennewick.com/DocumentCenter/View/14434/2018-Energy-Code-Credits |
| 2 | Heat pump | **1.0** | [V-extract], https://www.energy.wsu.edu/documents/FAQ%20Two%20heating%20systems.pdf |
| 3 (inferred) | Electric resistance heat only, forced air or zonal | **−1.0** (All Other and R-2) | [V-extract] value; [P] type number. Searches returned https://sbcc.wa.gov/sites/default/files/2019-12/R406%20retitled%20amalgamated.pdf |
| 4 | Ductless heat pump plus zonal electric resistance | **0.5** | [V-extract], WSU FAQ |
| 5 | All other heating system types (e.g. PTAC) | **−1.0** | [V-extract] value. "PTAC ... would be considered system type 5", https://www.energy.wsu.edu/Documents/Compliance%20Certificate%20Instructions%202018%20WSEC_rev%2007-21-21.pdf |
| Footnote a | 0.5 W/sf resistance budget with heat pump or ductless systems | n/a | [V-extract], WSU FAQ |

### 3.4 2021 WSEC-R Table R406.3, category 3: high-efficiency HVAC equipment (in force)

Rule: "Only one option" from category 3 may be selected [V-extract]. A user note says some options "**may only be claimed if serving System Type 4 or 5** from Table R406.2" [V-extract].

| Option | Description (extract wording) | Credits (All Other) | Tag / source |
|---|---|---|---|
| **3.1** | For a **System Type 1**: Energy Star (U.S. North) gas or propane **furnace AFUE ≥ 95%**, or Energy Star gas or propane **boiler AFUE ≥ 90%** | **1** (plan-sheet text order "3.1a, 1") | [V] description; [P] credit. Kirkland plan sheet (updated 11/26/24) and Clark County checklist |
| **3.2** | For the **secondary heating system serving System Type 2**: the same 95% furnace or 90% boiler, i.e. the dual-fuel backup | NOT FOUND | [V-extract] description |
| **3.3** | **Air-source centrally ducted heat pump, HSPF2 ≥ 8.1 (HSPF 9.5).** "In areas where the winter design temperature as specified in Appendix RC is **23°F or below**, a cold climate heat pump found on the **NEEP cc ASHP** qualified product list shall be used." | 1.5 (weak extract) | [V] description; [P] credit. Kirkland sheet and WSU worksheet extracts |
| **3.4** | **Ground source (geothermal).** Closed loop COP ≥ 3.3, or open-loop water-source COP ≥ 3.6 | NOT FOUND | [P]. The COP values may come from the 2018 wording. Mercer Island / Clark extracts |
| **3.5** | **Ductless mini-split heat pump system.** The extract hints at a ductless system of HSPF2 ≥ 9 (HSPF 10) installed in the largest zone where primary heat is zonal resistance. | NOT FOUND | [P]. Sammamish handout extract https://www.sammamish.us/media/drjlljvj/2021-wesc-final.pdf |
| **3.6** | **Air-source centrally ducted heat pump, HSPF2 ≥ 9.4 (HSPF 11.0).** Alternative (Energy Trust extract): a centrally ducted cold-climate variable-capacity heat pump on the NEEP cc VCHP list with ≥ 8.5 HSPF2 (10 HSPF) | NOT FOUND (one garbled extract was rejected) | [V] description. https://insider.energytrust.org/new-2021-washington-state-energy-code/ ; Clark checklist |
| 3.7 | **Air-to-water heat pump** (credit for air-to-water units rated by COP rather than HSPF) | 1.5 | [P]. Edition uncertain. Extract from searches returning the SBCC cost-benefit analysis https://sbcc.wa.gov/sites/default/files/2023-02/Cost-Effectiveness%20of%202021%20WSEC-R.pdf |
| 3.8 to 3.11? | One extract said "Items 3.1 through 3.10". An Everett checklist header lists "3.6 3.9 3.11". | NOT FOUND | [P]. It is possible the category runs past 3.7. Check https://everettwa.gov/DocumentCenter/View/37109/2021-Residential-Energy-Code-Compliance-Checklist-PDF?bidId= |

### 3.5 2021 WSEC-R Table R406.3, category 2: air leakage and ventilation [P/U]

- Only one option may be selected from category 2 ("Items 2.1 through 2.3" per one extract) [P].
- An extract requires HRV and ERV **Sensible Recovery Efficiency ≥ 75% at 32°F at the lowest listed net airflow** "for measures requiring either an ERV or HRV" [P; could be 2024 draft text].
- R-2 compartmentalization alternatives appear in cfm/sf at 50 Pa: 0.25 and 0.20 cfm/sf [P].
- Agent recall of the 2018/2021 structure [U]:

| Option | Air leakage | Ventilation | Credits |
|---|---|---|---|
| 2.1 | Tested ≤ 3.0 ACH50 | High-efficiency whole-house fans, ≤ 0.35 W/cfm, not interlocked with the furnace fan | 0.5 |
| 2.2 | ≤ 2.0 ACH50 | HRV, SRE ≥ 0.65 | 1.0 |
| 2.3 | ≤ 1.5 ACH50 | HRV, SRE ≥ 0.75 | 1.5 |
| 2.4 (2018) | ≤ 0.6 ACH50 | HRV, SRE ≥ 0.80 | 2.0 |

- Bid implication: any plan set claiming **2.2 or higher needs a ducted HRV or ERV** (supply to bedrooms and living areas, exhaust from baths and kitchen) plus blower-door and flow testing. **2.1 needs efficient continuous fans** and no HRV.

### 3.6 2021 WSEC-R Table R406.3, category 4: HVAC distribution [P]

- An SBCC 2025 proposal says: "Energy savings from locating the air handler and associated ductwork in the conditioned space is currently worth **0.5** energy credits as noted in the 2021 energy credits '4 High Efficiency HVAC Distribution System' option" (https://sbcc.wa.gov/sites/default/files/2025-06/24_RE_034v3_062325.pdf) [V-extract].
- Another extract gives "Option 4.2 is worth **1.0** credit for 'All interior HVAC'" [P].
- The "inside conditioned space" test is in section 2.2 [V]: ducts inside the continuous air barrier and the thermal envelope.
- The 2018-era wording of this option, per agent recall [U]:
  - "All heating and cooling system components installed inside the conditioned space ... all combustion equipment shall be direct vent or sealed combustion ... a maximum of 10 linear feet of return duct and 5 linear feet of supply duct connections to the plenum may be located outside the conditioned space ... Electric resistance heat and ductless heat pumps are not permitted under this option."
  - The Sammamish handout extract confirms an option where "electric resistance heat and ductless heat pumps are not permitted" [V-extract].

### 3.7 2018 WSEC-R Table R406.3: HVAC-related options (for decoding old plan sets)

The 2018 archive extract says "Only one option from Items 3.1 through 3.6 may be selected ... options including Energy Star rated gas or propane furnaces and air-source centrally ducted heat pumps with minimum HSPF of 9.5" (https://lawfilesext.leg.wa.gov/law/WACArchive/2020/pdf/WAC%20%2051%20%20TITLE/WAC%20%2051%20-%2011R%20CHAPTER/WAC%20%2051%20-%2011R-40621.pdf) [V-extract]. Everything else in this table is agent recall [U].

| 2018 option | Description | Credits |
|---|---|---|
| 3.1 | Energy Star (U.S. North) gas or propane furnace, AFUE ≥ 95% [P] | 1.0 [U] |
| 3.2 | Air-source centrally ducted heat pump, HSPF ≥ 9.5 [P] | 1.0 [U] |
| 3.3 | Closed-loop ground-source heat pump COP ≥ 3.3, or open-loop water-source COP ≥ 3.6 with ≤ 150 ft pumping head [U] | 1.5 [U] |
| 3.4 | Ductless split heat pumps with **no electric resistance in the primary living areas**; HSPF ≥ 10; sized and installed to heat the **entire** dwelling at the design temperature [U] | 1.5 [U] |
| 3.5 | Air-source centrally ducted heat pump, HSPF ≥ 11.0 [U] | 1.5 [U] |
| 3.6 | Ductless split heat pump (HSPF ≥ 10) in a home whose primary heat is **zonal electric resistance**, installed in the **largest zone** [U] | 2.0 [U] |
| 4.1 | All heating and cooling components and ducts inside conditioned space; no resistance or ductless-only systems [U] | 1.0 [U] |
| 2.1 to 2.4 | As in 3.5 above [U] | as above |

**Pre-2018 lettered numbering (e.g. "3b", "4c"):** the 2012 and 2015 WSEC-R used letter-suffixed options. WSU tables:
- 2015: https://www.energy.wsu.edu/Documents/Table_406.2_2015_Energy_Credits.pdf [V-title]
- 2012: https://www.energy.wsu.edu/Documents/Table_406_2_Energy_Credits_2012_WSEC.pdf [V-title]

Their contents are NOT FOUND. "4c" is **not** a 2018 or 2021 option number. If it appears, the plan set predates 2021 or is non-standard; ask the designer.

### 3.8 MAPPING: energy-sheet option number to HVAC system (2018 vs 2021)

How to tell the edition from the plan set: application or vesting date before or after 3/15/2024; required credits of 6.0 (2018 medium) versus 8.0 (2021 medium); HSPF2 values only appear in 2021; "System Type 1 to 5" credits of 1.0 / −1.0 (2018) versus 0 / 1.5 / 0.5 / 2.0 / 3.0 (2021).

| Printed option | If 2018 WSEC-R, it means | If 2021 WSEC-R, it means | HVAC takeoff consequence | Confidence |
|---|---|---|---|---|
| R406.2 "Type 1" | Gas or propane furnace or boiler (0) | Gas or propane furnace or boiler (0) | Gas or propane furnace or boiler; flue or PVC venting; gas piping | 2018 [V] / 2021 [V] |
| R406.2 "Type 2" | Any heat pump (1.0) | Heat pump with supplemental resistance **or** backup furnace (hybrid, ~38°F changeover) (1.5) | 2018: ducted heat pump. 2021: dual-fuel heat pump plus furnace, or heat pump plus significant strip heat. | [V] / [V]+[P] |
| R406.2 "Type 3" | Resistance only (−1.0) | Resistance only (0.5) | Baseboard, wall heaters or electric furnace; no heat pump | [P] / [P] |
| R406.2 "Type 4" | Ductless heat pump plus zonal resistance (0.5) | Resistance plus inverter ductless heat pump in the largest zone (2.0) | One ductless head in the great room plus resistance heaters elsewhere | [V] / [P] |
| R406.2 "Type 5" | All other (−1.0) | Heat pump (air-source, ground, or air-to-water) (3.0) | 2021: ducted or ductless whole-house heat pump, or air-to-water | [V] / [P] |
| 3.1 | 95% gas furnace | 95% gas furnace or 90% boiler (Type 1 only) | Condensing furnace, 2-pipe PVC | [P] / [V] |
| 3.2 | Ducted heat pump HSPF ≥ 9.5 | 95% backup furnace for a Type 2 hybrid | 2018: heat pump. 2021: dual fuel (heat pump **and** 95% furnace). | [P] / [V] |
| 3.3 | Ground-source heat pump | Ducted air-source heat pump HSPF2 ≥ 8.1 (cold-climate NEEP unit if design temperature ≤ 23°F) | 2018: geothermal. 2021: standard ducted heat pump. | [U] / [V] |
| 3.4 | Whole-house ductless heat pump, no resistance in living areas | Ground source / geothermal | 2018: multi-zone ductless. 2021: geothermal. | [U] / [P] |
| 3.5 | Ducted heat pump HSPF ≥ 11 | Ductless mini-split | 2018: high-efficiency ducted heat pump. 2021: ductless. | [U] / [P] |
| 3.6 | Ductless heat pump in the largest zone plus zonal resistance | Ducted air-source heat pump HSPF2 ≥ 9.4 (or cold-climate variable-capacity ≥ 8.5 HSPF2) | **The same number means opposite systems.** 2018: one ductless head plus baseboards. 2021: high-efficiency variable-speed ducted heat pump. | [U] / [V] |
| 3.7 | (not used) | Air-to-water heat pump | Hydronic heat pump | n/a / [P] |
| 2.1 | 3.0 ACH50 plus efficient fans | Similar [P] | Continuous efficient exhaust fans, no HRV | [U] / [P] |
| 2.2 to 2.4 | Tighter house plus HRV | Similar, SRE ≥ 75% at 32°F [P] | Ducted HRV or ERV plus flow balancing | [U] / [P] |
| 4.1 / 4.2 | All HVAC and ducts inside conditioned space | Air handler and ducts inside conditioned space (0.5) / all interior HVAC (1.0) [P] | No attic or vented-crawl ductwork; air handler in a conditioned closet; ducts in soffits or open-web floors | [U] / [P] |

### 3.9 Worked credit arithmetic (2021, medium house, 8.0 required) [V arithmetic, P option credits]

- **Heat pump house (Type 5, 3.0):** needs 5.0 more. Example: 3.6 high-efficiency ducted heat pump (credit NOT FOUND) + 2.x + envelope options + heat pump water heater.
- **Gas furnace house (Type 1, 0):** needs 8.0 from R406.3. Option 3.1 is worth about 1 [P], so 7.0 must come from envelope, air leakage/HRV, water heating, renewables and appliances.
- **Dual-fuel (Type 2, 1.5) plus 3.2:** needs 6.5 from R406.3, including the 3.2 credit (NOT FOUND).

---

## 4. WSEC-R 2021 prescriptive envelope, climate zones 4C and 5 (marine WA)

**This whole section is [U]; nothing here was retrieved.** Verify in Table R402.1.3 and the U-factor table of https://sbcc.wa.gov/sites/default/files/2024-01/2021_WSEC_R_2ndEd_012524.pdf or https://app.leg.wa.gov/wac/default.aspx?cite=51-11R&full=true.

WA uses one column for zone 5 and marine 4 [U]. The base values below are inferred to match 2018 because the 2021 R406 envelope options are written as improvements over them (fenestration U 0.28 / 0.25 / 0.22 / 0.18; walls R-21 + ci; floors R-38 / R-48) [U].

| Component | Prescriptive R-value (Table R402.1.3) [U] | U-factor alternative [U] |
|---|---|---|
| Vertical fenestration | U-0.30 | 0.30 |
| Skylight | U-0.50 | 0.50 |
| Glazed fenestration SHGC | NR | n/a |
| Ceiling (attic) | R-49 (vaulted and single-rafter ceilings typically R-38) | U-0.026 |
| Wood-frame wall | R-21 intermediate framing | U-0.056 |
| Mass wall | R-21 / R-21 | NOT FOUND |
| Floor over unconditioned space | R-30 | U-0.029 |
| Below-grade wall | 10/15/21 int + TB (exterior ci / interior cavity / interior + thermal break) | U-0.042 |
| Slab-on-grade | R-10, 2 ft (heated slab: R-10 perimeter and under the entire slab) | F-factor NOT FOUND |
| Opaque doors | One side-hinged opaque door ≤ 24 sf exempt; otherwise about U-0.20 | NOT FOUND |

**Air leakage, R402.4 [U]:**
- Mandatory blower-door test at 50 Pa per RESNET/ICC 380, ASTM E779 or ASTM E1827, performed after all envelope penetrations are made.
- Signed report to the code official; third party if the code official requires it.
- **Maximum 5.0 ACH50** (the 2018 WSEC-R limit, believed unchanged in 2021 for single-family; WA did not adopt the 2021 IECC's 3.0).
- The R406 credit ladder starts at 3.0 ACH50 (option 2.1), which is consistent with a looser base.
- WA 2021 wording NOT VERIFIED.
- Mechanical-ventilation link: see sections 5.8 and 5.11.

---

## 5. 2021 IRC as amended by WAC 51-51: mechanical items an HVAC bid depends on

- **Structure [U]:**
  - WA adopts the 2021 IRC with amendments in chapter 51-51 WAC (https://app.leg.wa.gov/wac/default.aspx?cite=51-51, not opened).
  - IRC Chapter 11 (energy) is replaced by the WSEC-R (51-11R).
  - The IRC plumbing chapters are replaced by the UPC (51-56).
  - Amended IRC sections live at `WAC 51-51-<section>`, e.g. WAC 51-51-1503 and 51-51-1505. Those pages were not opened.
- **Model text below is the 2021 IRC [U]** (https://codes.iccsafe.org/content/IRC2021P1, not opened). Where a WA amendment is known from agent recall it is marked "WA amendment [U]".

### 5.1 Chapter 11 and energy [U]

IRC N11xx is not used in WA. The WSEC-R governs duct insulation, duct testing, piping insulation, thermostats and fan efficacy (section 2).

### 5.2 M1401.3 Equipment sizing [U]

- Size per **ACCA Manual S** using **Manual J** loads, or another approved method.
- 2021 exception: sizing is not limited to Manual S where either
  - (1) multistage or variable-refrigerant-flow equipment has published capacities that bracket the calculated loads, or
  - (2) no published capacity satisfies both the total and sensible loads, and the next larger standard size is specified.
- Bid implication: **attach a Manual J/S** to the mechanical permit; most WA jurisdictions ask for it.

### 5.3 M1403 Heat pumps and M1401.4 / M1308.3 outdoor installation [U]

- Heat pumps must be listed to UL 1995 or UL/CSA 60335-2-40.
- M1403.2: the outdoor unit must be raised **≥ 3 in. above grade** for defrost drainage.
- Outdoor equipment must be listed for outdoor use.
- Outdoor supports must sit ≥ 3 in. above finished grade.
- In snow areas (Whatcom foothills, Sudden Valley, Glacier-side), manufacturers call for elevated stands. Price wall brackets or 12 to 18 in. stands.

### 5.4 M1411 Refrigeration, condensate and refrigerant piping [U]

Subsection numbers shift between IRC printings; verify them.

- **Condensate disposal (M1411.3):**
  - Route from the drain-pan outlet to an approved place of disposal.
  - Slope **≥ 1/8 in. per ft (1%)**.
  - No discharge to a street or alley, or anywhere it causes a nuisance.
- **Auxiliary / secondary protection (M1411.3.1)**, one of the following where overflow could damage the building:
  - (1) auxiliary pan with its own drain to a conspicuous point. The pan must be **≥ 1.5 in. deep**, **≥ 3 in. larger** than the unit in length and width, and made of corrosion-resistant material: galvanized steel ≥ 0.0236 in. (No. 24 gage), or nonmetallic ≥ 0.0625 in.
  - (2) separate overflow drain from the equipment pan, connected above the primary.
  - (3) auxiliary pan with **no drain** plus a **water-level switch** that shuts the unit off.
  - (4) water-level shutoff in the primary drain line, overflow line or equipment pan.
- **M1411.3.1.1 water-level monitoring:** required inside the primary pan on down-flow units and coils without provision for a secondary pan. Externally installed or in-line devices do not satisfy it.
- **Drain pipe (M1411.3.2):**
  - ≥ **3/4 in. ID**, not reduced along its run.
  - Materials: CPVC, PVC, ABS, copper, PEX and others.
  - Manifolded drains must be sized by an approved method.
  - **M1411.3.3:** drains must be cleanable without cutting.
- **Condensate pumps (M1411.4):** a pump in an attic or crawl space must be interlocked so the equipment stops if the pump fails.
- **Refrigerant piping insulation:** suction (vapor) lines insulated to **≥ R-4**, with external surface permeance **≤ 0.05 perm** (ASTM E96).
- **Locking access-port caps:** outdoor refrigerant access ports need **locking tamper-resistant caps** or other securing.
- Bid line items: aux pan with float switch for any attic or closet-over-finished-space air handler; condensate pump interlock; line-set insulation (3/4 in. wall, about R-4); locking caps. Condensate disposal on sites with septic systems: see section 9.

### 5.5 M1305 Appliance access and clearances [U]

- **General (M1305.1):**
  - Appliances must be accessible without removing permanent construction.
  - Provide a level working space **30 × 30 in.** at the control side.
- **Appliance rooms (M1305.1.2):**
  - Door and passageway **36 in. wide × 80 in. high**.
  - Exception within a dwelling unit: a compartment or alcove opening ≥ **24 in. wide** and large enough to remove the appliance, with a 30 in. deep service space in front.
- **Attics (M1305.1.3):**
  - Opening and passageway large enough to remove the largest appliance, and at least **30 in. high × 22 in. wide**.
  - Passageway **≤ 20 ft long** with **continuous solid flooring ≥ 24 in. wide**.
  - Level service space **30 × 30 in.** at each side needing access.
  - Clear access opening ≥ **20 × 30 in.**
  - Exception: a passageway up to **50 ft** long is allowed if it is ≥ 6 ft high and 22 in. wide.
  - **M1305.1.3.1:** a **luminaire switched at the passage opening** and a **receptacle at or near the appliance**. That is an electrician line item.
- **Under-floor / crawl (M1305.1.4):**
  - Passageway **≥ 30 in. high × 22 in. wide**, **≤ 20 ft long**.
  - Service space **30 × 30 in.** at the service side.
  - Rough opening ≥ **22 × 30 in.**
  - If the passage or service space is more than 12 in. below grade, it needs concrete or masonry walls extending 4 in. above grade.
  - **M1305.1.4.1:**
    - Ground-supported equipment goes on a slab or approved material **≥ 3 in. above grade**.
    - Suspended units need **≥ 6 in.** clearance to the ground.
    - Excavate 6 in. below the appliance and 12 in. around it, with 30 in. on the control side.
  - **M1305.1.4.3:** light and receptacle required.

### 5.6 M1502 Clothes-dryer exhaust [U]

- **Independent system**, discharged to the outdoors. No screen at the terminal. **Backdraft damper** required.
- Terminate **≥ 3 ft** from openings into the building.
- **Duct:** **4 in.** nominal, rigid metal **≥ 0.016 in. (No. 28 gage)**, smooth interior.
  - Joints lapped in the direction of airflow.
  - No fasteners protruding more than **1/8 in.**
  - Supported at **≤ 12 ft** intervals.
  - Shield plates where the duct is within 1.25 in. of the face of framing.
- **Transition duct:** one listed length (UL 2158A), **≤ 8 ft**, not concealed.
- **Maximum length (M1502.4.5.1):** **35 ft** from the transition-duct connection to the terminal, reduced for fittings per the table below. Alternatively, use the dryer manufacturer's instructions (a copy is required at the concealment inspection) or a listed dryer-exhaust booster fan.

| Fitting | Equivalent length deduction [U] |
|---|---|
| 4 in. radius mitered 45° | 2 ft 6 in. |
| 4 in. radius mitered 90° | 5 ft |
| 6 in. radius smooth 45° | 1 ft |
| 6 in. radius smooth 90° | 1 ft 9 in. |
| 8 in. radius smooth 45° | 1 ft |
| 8 in. radius smooth 90° | 1 ft 7 in. |
| 10 in. radius smooth 45° | 9 in. |
| 10 in. radius smooth 90° | 1 ft 6 in. |

- **Label (M1502.4.6):** where the equivalent length exceeds 35 ft, post a permanent label within **6 ft** of the connection.
- **Duct required (M1502.4.7):** where dryer space is provided, install the exhaust duct even without a dryer; cap it and mark it "future use". A listed condensing dryer is excepted.
- WA amendments to M1502: none known [U].

### 5.7 M1503 Range hoods and the WA makeup-air amendment

- **Hood duct [U]:**
  - Discharge outdoors through a smooth, airtight duct with a backdraft damper, independent of other systems.
  - Not terminated in an attic or crawl space.
  - Single-wall duct of **galvanized steel, stainless steel or copper**.
  - Schedule 40 PVC is allowed only for downdraft units under a slab (backfilled, ≤ 1 in. projection above the floor and above grade, solvent-welded).
  - Listed ductless hoods are allowed only where ventilation is otherwise provided.
- **Makeup air, model IRC [U]:** hoods able to exhaust **more than 400 cfm** need makeup air at approximately the exhaust rate, with a damper that opens automatically.
- **WA amendment [U, agent recall; verify at https://app.leg.wa.gov/wac/default.aspx?cite=51-51-1503]:**
  - Hoods "capable of exhausting in excess of **400 cfm** shall be mechanically or passively provided with makeup air at a rate approximately equal to the **difference between the exhaust air rate and 400 cfm**," with a means of closure and automatic interlock.
  - Exception: "Where all appliances in the house are of **sealed combustion, power-vent, unvented, or electric**, the exhaust hood system shall be permitted to exhaust up to **600 cfm** without providing makeup air." Above 600 cfm, makeup air equals the exhaust minus 600 cfm.
- **Makeup-air location [U]:** the same room, or rooms connected to it by permanent openings.
- Bid implication: count hoods rated above 400 cfm (above 600 cfm in all-electric or sealed-combustion houses). Add a motorized makeup damper and duct, plus a tempering heater where specified.

### 5.8 M1505 Mechanical ventilation, as amended by WA

Everything in this subsection is [U]: agent recall of the WA text plus the 2021 IRC base. Verify at https://app.leg.wa.gov/wac/default.aspx?cite=51-51-1505 (not opened).

- **Whole-house system (M1505.4) [U]:**
  - One or more supply and/or exhaust fans with ducts and controls.
  - Local exhaust fans may serve as the system.
  - An outdoor-air duct to the air-handler return counts as supply ventilation (with a motorized damper and fan-cycling or ECM low-speed control).
  - In WA it is required for every new dwelling (section 5.11).
- **Rate (M1505.4.3):** continuous airflow from Table M1505.4.3(1), or **Equation 15-1: Q (cfm) = 0.01 × CFA (sf) + 7.5 × (bedrooms + 1)** [U]. Table M1505.4.3(1), continuous whole-house rate in cfm [U]:

| CFA (sf) | 0-1 BR | 2-3 BR | 4-5 BR | 6-7 BR | > 7 BR |
|---|---|---|---|---|---|
| < 1,500 | 30 | 45 | 60 | 75 | 90 |
| 1,501-3,000 | 45 | 60 | 75 | 90 | 105 |
| 3,001-4,500 | 60 | 75 | 90 | 105 | 120 |
| 4,501-6,000 | 75 | 90 | 105 | 120 | 135 |
| 6,001-7,500 | 90 | 105 | 120 | 135 | 150 |
| > 7,500 | 105 | 120 | 135 | 150 | 165 |

- **Occupant density [U]:** the table assumes 2 people in a studio or 1-bedroom unit, plus 1 per additional bedroom. Add **7.5 cfm per extra known occupant**.
- **Intermittent operation, Table M1505.4.3(2) [U]:** multiply the continuous rate by the factor for the percentage of run time in each 4-hour segment.

| Run time per 4-hour segment | Factor |
|---|---|
| 25% | 4.0 |
| 33% | 3.0 |
| 50% | 2.0 |
| 66% | 1.5 |
| 75% | 1.3 |
| 100% | 1.0 |

  - Interpolation is allowed; extrapolation below 25% is not.
- **Controls (M1505.4.2), WA [U]:**
  - Automatic operation (timer or controller able to run continuously) with occupant override.
  - Readily accessible.
  - Permanently labeled with text or a symbol. WA recommends a label such as "Leave on unless outdoor air quality is very poor".
- **Exhaust-only systems, WA outdoor-air inlets [U, strong recall]:**
  - Each habitable room needs an outdoor-air inlet ("trickle vent") with controllable, secure openings.
  - Minimum **4 sq in. net free area** per habitable room. An inlet delivering **10 cfm at 10 Pa** (HVI test) is deemed equivalent.
  - Inlets must be screened and kept away from contaminant sources.
  - Where doors separate inlets from exhaust points, provide transfer paths. **Door undercuts ≥ 1/2 in.** above the finished floor.
  - Bid implication: count trickle vents (window-frame or wall vents) per bedroom and living room when the design is exhaust-only.
- **Fan noise, WA [U, strong recall]:**
  - Whole-house fans located **≤ 4 ft** from the interior grille: **≤ 1.0 sone** at 0.1 in. w.c.
  - Remote-mounted fans must be acoustically isolated from structure and ducts (insulated flex or approved material).
  - Local bath fans commonly spec'd at ≤ 1.0 to 1.5 sone. Any separate WA limit for local fans is NOT VERIFIED.
- **Local exhaust (M1505.4.4 / Table M1505.4.4) [U]:**

| Space | Intermittent | Continuous |
|---|---|---|
| Kitchen | 100 cfm | 25 cfm |
| Bathroom / toilet room | 50 cfm | 20 cfm |

  - A "5 ACH continuous kitchen" alternative (ASHRAE 62.2 style) was not confirmed in the WA text.
  - WA historically also requires local exhaust in **laundry rooms** [U; verify].
  - Bath exhaust may double as whole-house exhaust if sized and controlled for it.
- **Flow testing and verification [U]:**
  - WA requires whole-house ventilation flow to be **measured and verified**: flow hood, flow grid or other airflow device at the terminals or in the duct, or per the manufacturer's method. There is a written report, and a third party if the building official requires one.
  - Paired with WSEC-R R403.6.3 (section 2.4).
  - Numeric acceptance tolerance: NOT FOUND.
- **Bath and kitchen exhaust terminations (M1501.1 / M1505.2) [U]:** directly outdoors. **Never into an attic, soffit vent, ridge vent or crawl space.** Bath exhaust air is not recirculated.

### 5.9 Exhaust and intake openings [U]

- **Exhaust openings (M1504.3):**
  - **≥ 3 ft** from property lines.
  - **≥ 3 ft** from operable and nonoperable openings into the building.
  - **≥ 10 ft** from mechanical air intakes, unless 3 ft above the intake.
  - Not directed onto walkways (R303.5.2).
- **Intakes (R303.5.1):**
  - **≥ 10 ft** horizontally from contaminant sources (vents, streets, parking, chimneys, dryer terminals), or 2 ft below the source if within 10 ft.
  - Bath and kitchen exhaust is **not** treated as a noxious source.
- **Duct-length table:** the IRC includes a prescriptive fan-duct length table (derived from ASHRAE 62.2) for ventilation fans by cfm, diameter, and flex versus smooth duct. Table number and values NOT VERIFIED.

### 5.10 M1601-M1602 Ducts and return air [U]

- **Duct systems (M1601.1.1):**
  - Factory-made ducts: UL 181, installed per the manufacturer.
  - Metal ducts per SMACNA.
  - Flame spread ≤ 200.
  - **Stud cavities and joist spaces may be return plenums only.** They may not serve as supply, may not be part of a fire-rated assembly, may not convey air from more than one floor, must be fire-blocked, and **exterior-wall cavities may not be used**.
  - Gypsum-lined shafts: returns only, air ≤ 125°F.
- **Minimum sheet-metal thickness, Table M1601.1.1:**

| Duct | Size | Galvanized steel |
|---|---|---|
| Round or enclosed rectangular | ≤ 12 in. | 0.013 in. (30 ga) |
| Round or enclosed rectangular | > 12 in. | 0.016 in. (28 ga) |
| Exposed rectangular | ≤ 14 in. | 0.016 in. (28 ga) |
| Exposed rectangular | > 14 in. | 0.019 in. (26 ga) |

- **Sealing (M1601.4.1):**
  - All joints, seams and connections sealed with welds, gaskets, mastics, mastic plus fabric, liquid sealants or tapes.
  - Tapes and mastics: **UL 181B-FX** (pressure-sensitive tape) or **181B-M** (mastic) for metal and flex; UL 181A for ductboard.
  - Flex duct mechanical fasteners (clamps or ties): **UL 181B-C**.
  - Equipment flange connections: **sealed and mechanically fastened**.
  - Round crimp joints: **≥ 1 in.** lap with **≥ 3 screws or rivets** equally spaced.
  - Exceptions: spray foam; continuously welded or locking seams (not snap-lock or button-lock) below 2 in. w.c.
- **Support (M1601.4.4):**
  - Factory-made UL 181 ducts, including flex, are supported per the **manufacturer's instructions**. Field metal and flex per SMACNA.
  - The IRC gives no fixed flex spacing. Industry practice (ADC Flexible Duct Performance & Installation Standards) is support at **≤ 4 to 5 ft** with sag **≤ 1/2 in. per ft**. NOT VERIFIED here.
- **Other duct rules:**
  - Ducts ≥ **4 in.** from earth unless encased (M1601.4.8).
  - Under-slab ducts per M1601.1.2.
  - Ducts in garages per R302.5.2 (section 5.12).
- **Return air (M1602.2):**
  - (1) ≥ **10 ft** from an open combustion chamber or draft hood in the same space.
  - (2) Not from hazardous or insanitary locations.
  - (3) Return from a room ≤ the supply to that room.
  - (4) Sized per the manufacturer, Manual D or the designer.
  - (5) Not between dwelling units. This matters for duplexes: **separate systems per unit**.
  - (6) Crawl-space return not by direct connection to the furnace return.
  - (7) **No return from a closet, bathroom, toilet room, kitchen, garage, mechanical room, boiler or furnace room, or unconditioned attic.**
  - Exceptions: kitchen return ≥ 10 ft from cooking appliances; a system dedicated to the garage.

### 5.11 R303.4 Mechanical ventilation trigger [U]

- **Model IRC:** a dwelling tested at **< 5 ACH50** must have whole-house mechanical ventilation per M1505.4.
- **WA amendment [U]:** whole-house mechanical ventilation is required for **all** new dwelling units, regardless of test result. This is WA's long-standing ventilation and indoor air quality policy.
- Either way, 2021 WSEC-R houses are tested at 5.0 ACH50 or tighter [U], so budget a whole-house ventilation system in every bid.

### 5.12 Garage separations (R302.5.2) and independent garage systems (M1601.6) [U]

- **R302.5.2:** ducts in the garage, or penetrating walls and ceilings between the dwelling and the garage, must be **≥ No. 26 gage (0.48 mm) sheet steel** or other approved material, with **no openings into the garage**. Flex duct in the garage is not allowed.
- **M1601.6:** furnaces and air handlers serving living spaces must not **supply air to or return air from a garage**. A garage heater needs its own system.

---

## 6. Refrigerant rules affecting 2026 installs

**This whole section is [U]; no refrigerant source could be retrieved.**
- Verify EPA items at https://www.epa.gov/climate-hfcs-reduction/technology-transitions and 40 CFR 84.54 at https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-84/subpart-B/section-84.54 (both egress-blocked).
- Verify WA items at https://app.leg.wa.gov/rcw/default.aspx?cite=70A.60 and https://app.leg.wa.gov/wac/default.aspx?cite=173-443 (not opened).

**EPA AIM Act Technology Transitions rule** [U] (final rule October 2023, 88 FR 73098; 40 CFR part 84, subpart B):
- Residential and light-commercial AC and heat pumps (self-contained and split) may not use a refrigerant with **GWP ≥ 700**.
- **Manufacture and import compliance date: January 1, 2025.**
- **New split systems:** components made or imported before 1/1/2025 (e.g. R-410A condensers) could be **installed until January 1, 2026**. After that, a new R-410A split system cannot be installed.
- VRF systems had a one-year-later schedule (manufacture 1/1/2026, installation 1/1/2027).
- Repairs to existing R-410A systems are not restricted by this rule.
- EPA announced a reconsideration of parts of the rule in 2025. Whether anything changed for residential AC and heat pumps by 9/2026: NOT VERIFIED.

**Washington HFC law** [U]:
- RCW 70A.60 (HB 1112, 2019; amended by HB 1050, 2021) and Ecology's WAC 173-443 prohibit high-GWP HFCs by end use.
- The residential and non-residential AC and heat pump limit is **GWP < 750** for new equipment. Ecology aligned its rule timing with the EPA dates.
- Exact WA dates, and whether WA has an installation-date provision for split systems: NOT VERIFIED.
- The EPA 700 limit is the tighter one and controls in practice.
- WA's refrigerant management program (leak inspections and registration) targets large systems (≥ 50 lb) and does not affect single-family work [U].

**What a 2026 bid should specify** [U]:
- New AC and heat pump equipment on **R-454B or R-32 (A2L, mildly flammable)**. No new R-410A split systems.
- **A2L installation requirements** per the manufacturer and UL 60335-2-40:
  - Refrigerant leak **detection sensors** and a **mitigation or blower-activation board**. These are factory or kit items on most ducted indoor units.
  - Minimum room-area and charge limits for ductless heads.
  - A2L-rated recovery equipment and tools.
  - Brazed or listed mechanical joints.
- Whether WA's 2021 IRC/IMC amendments add A2L-specific rules (the 2024 IRC/IMC have them; the 2021 base does not): NOT VERIFIED.
- Line-set length and size per the manufacturer; nitrogen pressure test and evacuation, with readings recorded on the start-up sheet.
- **EPA Section 608** certified technicians.

---

## 7. Outdoor design temperatures for load calculations

**Status: no values found this session.** The WSU calculator (energy.wsu.edu), the WAC appendix (app.leg.wa.gov) and all ASHRAE sources were unreachable, and the search budget ran out before any design-temperature queries.

- **WA code's own source:** the 2021 WSEC-R uses "the winter design temperature as specified in **Appendix RC**" [V-extract, from the Kirkland plan sheet and WSU worksheet extracts]. At or below 23°F, option 3.3 needs a NEEP-listed cold-climate heat pump [V].
  - The table is in the WSEC-R: https://sbcc.wa.gov/sites/default/files/2024-01/2021_WSEC_R_2ndEd_012524.pdf or https://app.leg.wa.gov/wac/default.aspx?cite=51-11R&full=true
  - **Pull it before quoting any NW WA job.** If Bellingham, Lynden, Blaine or Sedro-Woolley are listed at ≤ 23°F, every "3.3" credit there needs a cold-climate unit.
- The user reports that the WSU "Simple Heating System Size: Washington State" calculator uses Seattle design temperature difference = 46 (70°F − 24°F). This is unverified here.
- Puget Sound Chapter ASHRAE "Recommended Outdoor Design Temperatures": NOT FOUND.
- ASHRAE Fundamentals climatic data (99%/99.6% heating, 1%/2.5% cooling DB/MCWB): NOT FOUND.

| Location | Heating 99% or 99.6% DB (°F) | Cooling 1% or 2.5% DB / MCWB (°F) | WSEC-R Appendix RC winter design temperature | Status |
|---|---|---|---|---|
| Bellingham | NOT FOUND | NOT FOUND | NOT FOUND | Nearest ASHRAE station: Bellingham Intl AP [U] |
| Blaine | NOT FOUND | NOT FOUND | NOT FOUND | Use Bellingham or Blaine municipal AP data [U] |
| Lynden | NOT FOUND | NOT FOUND | NOT FOUND | Colder inland; Fraser outflow wind [U] |
| Ferndale | NOT FOUND | NOT FOUND | NOT FOUND | [U] |
| Sedro-Woolley | NOT FOUND | NOT FOUND | NOT FOUND | [U] |
| Mount Vernon | NOT FOUND | NOT FOUND | NOT FOUND | Skagit Regional AP station [U] |
| Anacortes | NOT FOUND | NOT FOUND | NOT FOUND | Marine-moderated [U] |
| Friday Harbor / Shaw Island | NOT FOUND | NOT FOUND | NOT FOUND | Friday Harbor AP station [U] |
| Everett | NOT FOUND | NOT FOUND | NOT FOUND | Paine Field station [U] |
| Seattle | 24°F implied by the user-reported WSU DTD of 46 (unverified) | NOT FOUND | NOT FOUND | Sea-Tac station [U] |

**Design note for the skill [U]:** Whatcom County (Lynden, Everson, Sumas, Blaine, north Bellingham) sees **Fraser River outflow** events: arctic air with strong NE winds. Designers commonly use a lower heating design temperature and higher infiltration there than in Skagit or San Juan. Size heat pumps to the **Appendix RC** or ASHRAE 99% value and check low-ambient capacity (cold-climate units).

---

## 8. Mechanical permits, fees and inspections for a new single-family house

**Status: fee schedules NOT FOUND** (search budget exhausted). Issuing agencies below are agent recall [U]. Permit portals are known from the user's other skills: Bellingham uses eTRAKiT; Whatcom County and Skagit County use Tyler EnerGov (Skagit at `skagitcountywa-energovweb.tylerhost.net`). That is internal context, not a web source.

| Jurisdiction | Who issues mechanical | Fee basis | Tag |
|---|---|---|---|
| Unincorporated Whatcom County (including Sudden Valley and Glenhaven Lakes) | Whatcom County Planning & Development Services | NOT FOUND. Likely a separate mechanical permit with a base fee plus per-appliance and per-fan items. Some counties fold mechanical into the new-SFR building permit. | [U] / NOT FOUND |
| City of Bellingham | City of Bellingham Permit Center (Planning & Community Development) | NOT FOUND. Separate mechanical permit expected [U]. | [U] / NOT FOUND |
| City of Blaine | City of Blaine Community Development Services / Building | NOT FOUND | [U] / NOT FOUND |
| Skagit County (unincorporated) | Skagit County Planning & Development Services | NOT FOUND | [U] / NOT FOUND |
| San Juan County (including Shaw Island) | San Juan County Community Development (Building) | NOT FOUND | [U] / NOT FOUND |

- **Electrical for HVAC [U]:** in WA, electrical permits and inspections come from **L&I** unless the city runs its own program. Whether Bellingham inspects its own electrical work: NOT VERIFIED.
- **Licensing [U]:** HVAC line and low-voltage wiring requires a WA electrical contractor license and an **06A (HVAC/refrigeration)** specialty electrician certificate. The mechanical contractor needs L&I contractor registration.
- **Energy forms that jurisdictions accept [V-title]:**
  - WSU Single Family Work Sheet (see section 3).
  - WSU "Code Compliance Calculator" printout: example at https://permitbulletin.mercerisland.gov/public/2509-220/SUB1/2509-220%20wsec-energy%20code%20worksheet.pdf and https://www.sultanwa.gov/DocumentCenter/View/7936/Energy-Calculations
  - WSU 2021 WSEC-R Compliance Certificate: https://www.energy.wsu.edu/documents/2021%20WSEC-R%20Compliance%20Certificate.pdf
  - Skagit County example: Sedro-Woolley posts the 2021 WSEC-R multifamily worksheet at https://cms5.revize.com/revize/cityofsedrowoolley/Departments/Building/Forms%20&%20Documents/2021%20WSEC-R%20Multifamily%20Work%20Sheet%2020240307.pdf
  - San Juan County has a 2018 residential energy form and a "2021 WSEC Significant Changes" handout: https://sanjuancountywa.gov/DocumentCenter/View/29469/2021-Washington-State-Energy-Code-Significant-Changes

**Typical inspection sequence for new SFR mechanical work in WA [U]:**
1. Underfloor / under-slab rough, for any ducts or piping under slabs or in crawls (duct separation from earth, insulation).
2. **Mechanical rough-in / cover**, at framing. Ducts, flue and vent, bath and kitchen exhaust ducts, dryer duct (with the dryer installation instructions if the manufacturer's length method is used), line sets, condensate routing, fire-blocking, garage-separation ducts.
3. **Duct leakage test.** Rough-in test report (air handler installed or not), or leave it to post-construction.
4. Insulation inspection (energy): duct insulation outside the envelope, buried-duct depth.
5. **Blower-door test report** (5.0 ACH50 max [U], or the credit target).
6. **Whole-house ventilation flow verification report** and fan labels and controls.
7. Gas piping pressure test, if there is gas.
8. **Mechanical final:** equipment, aux pans and float switches, condensate disposal, locking caps, refrigerant line insulation, attic light and receptacle, labels, thermostat programming, makeup-air interlock.
9. Building final with the **energy compliance certificate** posted.

**Who performs tests [U]:**
- The WSEC-R and IRC allow the contractor or tester to submit a signed report. The code official **may require an approved third party**.
- In practice, northwest WA builders hire independent HERS or energy raters and blower-door and duct-test companies. The HVAC bid should state whether duct testing and ventilation flow testing are included, and which test (rough-in or final).

---

## 9. WA-specific items that trip HVAC bids (checklist)

| Item | Rule | Tag / source |
|---|---|---|
| Heat pump backup | Supplemental resistance must be locked out when the compressor can carry the load (R403.1.2). In 2021, backup design changes the credit: Type 2 (1.5) vs Type 5 (3.0), with a 38°F changeover note. | [U] R403.1.2; [P] 38°F note, https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40620 |
| Same option number, different meaning | "3.6" is a ductless heat pump plus baseboards under 2018 and a high-efficiency ducted heat pump under 2021. Always identify the code edition first. | section 3.8 [V/U] |
| Cold climate | With an Appendix RC winter design temperature ≤ 23°F, a ducted heat pump credit needs a NEEP-listed cold-climate unit | [V] (section 3.4) |
| Returns | None from bathrooms, toilet rooms, closets, kitchens (unless ≥ 10 ft from cooking appliances), garages, mechanical rooms or unconditioned attics (M1602.2) | [U] |
| Garage | Ducts in or through the garage separation: ≥ 26 ga steel, no openings (R302.5.2). No supply or return to the garage from the house system (M1601.6). | [U] |
| Duplex | Separate system per unit; no return air between units (M1602.2 item 5). Credits are counted per dwelling unit. | [U] / [V] |
| Attic equipment | 22 × 30 in. passage ≤ 20 ft with 24 in. solid floor; 30 × 30 in. service platform; **switched light at the opening plus a receptacle** (M1305.1.3 / .3.1); aux pan plus float switch | [U] |
| Crawl equipment | 22 × 30 in. access; 30 × 30 in. service space; ≥ 3 in. pad or 6 in. suspended clearance; light plus receptacle (M1305.1.4); crawl ducts insulated to R-8; condensate pump interlock | [U] |
| Heat pump outdoor unit | ≥ 3 in. above grade (M1403.2); snow stands in Whatcom foothills; exhaust and intake separations (section 5.9) | [U] |
| Whole-house ventilation | Required in every WA dwelling. 0.01·CFA + 7.5·(BR+1). Timer or controls with a label. **≤ 1.0 sone** if the fan is within 4 ft of the grille. **Trickle vents (4 sq in. per habitable room)** for exhaust-only systems. Flow verification report. | [U] section 5.8 |
| Range hood makeup air | WA: makeup air above **400 cfm** (the difference over 400), or up to **600 cfm** with no makeup air if all appliances are sealed-combustion, power-vent or electric | [U] section 5.7 |
| Dryer | 4 in. rigid metal, 35 ft minus fittings, backdraft damper, no screen, 3 ft from openings, label if over 35 ft | [U] section 5.6 |
| Bath and kitchen exhaust | Must terminate outdoors, **not into a soffit, ridge vent, attic or crawl** (M1501.1) | [U] |
| Condensate to septic | NOT FOUND. Many NW WA on-site sewage rules discourage clear-water (condensate) discharge into septic systems. Default to a splash block or drywell to grade, or confirm with Whatcom County, Skagit County or San Juan County Health on-site sewage staff. | NOT FOUND |
| Gas fireplace | **Direct-vent** units need no indoor combustion air. Count the fireplace as a fuel-fired appliance: it triggers the carbon monoxide alarm rules (IRC R315). WA law requires CO alarms in new residential construction (RCW 19.27.530). | [U] |
| Wood fireplace | WSEC-R R402.4.2: tight-fitting flue dampers or doors plus **outdoor combustion air**. IRC R1006: exterior air supply unless the room is mechanically kept at neutral or positive pressure. | [U] |
| Garage appliances | Ignition sources ≥ 18 in. above the garage floor and protected from vehicle impact (M1307.3 / M1307.3.1). A2L equipment adds manufacturer siting rules. | [U] |
| Seismic | WA is Seismic Design Category D. Anchor and strap appliances per M1307.2 and the manufacturer (water heaters, air handlers, outdoor units on pads). | [U] |
| Refrigerant | A2L (R-454B or R-32) equipment only for new systems; leak sensors and mitigation per the manufacturer; locking caps; R-4 suction insulation | [U] section 6 |
| Fuel availability | San Juan County (including Shaw Island) has no piped natural gas; propane or electric only. Much of Whatcom and Skagit is served by Cascade Natural Gas. | [U]; Cascade Natural Gas WSEC handout exists: https://www.cngc.com/wp-content/uploads/PDFs/energy_choice/washington/2018_WSEC-R-Pathway-to-6.0-Credits_Handout.pdf **[V-title]** |
| Local electrification | Possible City of Bellingham local requirement for all-electric new construction. Unverified, and legally unblocked again after the 9/17/2026 ruling. | NOT VERIFIED |
| HOA / community rules | Sudden Valley and similar communities may review outdoor-unit placement and noise | [U] |

---

## 10. Open items: verification queue for the next pass (exact pages)

1. **Table R406.3 (2021):** exact credits for 3.2 through 3.7 (and any 3.8 to 3.11), 2.x, and 4.x. Also the Table R406.2 footnotes (Type 2 vs Type 5, changeover temperature) and the Group R-2 column.
   - https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40621
   - https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40620
   - https://lawfilesext.leg.wa.gov/Law/WACArchive/2024/htm/WAC%20%2051%20-%2011R%20CHAPTER/WAC%20%2051%20-%2011R-40621.htm
   - https://wpcdn.web.wsu.edu/cahnrs/uploads/sites/60/2026/05/Energy-Credit-Requirements-and-Credit-Options-R406.3.pdf
2. **Table R406.3 (2018):** option text and credits.
   - https://lawfilesext.leg.wa.gov/law/WACArchive/2020/pdf/WAC%20%2051%20%20TITLE/WAC%20%2051%20-%2011R%20CHAPTER/WAC%20%2051%20-%2011R-40621.pdf
   - https://customdiggs.com/wp-content/uploads/2022/04/2018-Energy-Credits-Table.pdf
3. **R403 and R402 (2021 WA):** duct leakage limits, duct insulation, fan efficacy, ventilation testing, ACH50 limit, Table R402.1.3, **Appendix RC design temperatures**.
   - https://sbcc.wa.gov/sites/default/files/2024-01/2021_WSEC_R_2ndEd_012524.pdf
   - https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40320
4. **WA IRC amendments:** WAC 51-51-0303 (R303), 51-51-1503 (M1503 makeup air), 51-51-1505 (M1505 ventilation, inlets, sones, testing), and any 51-51-1411 or 51-51-1601 changes. Chapter: https://app.leg.wa.gov/wac/default.aspx?cite=51-51
5. **2024 codes:** did the SBCC take final adoption on 8/21/2026? Is May 3, 2027 still the effective date? What does the 2024 WSEC-R do to heat pumps and credits?
   - https://sbcc.wa.gov/state-codes-regulations-guidelines/rulemaking
   - https://sbcc.wa.gov/sites/default/files/2026-07/2024WSEC_R_FiledCR102_070126.pdf
6. **Local policy after 9/17/2026:** Whatcom County PDS, City of Bellingham (including any electrification ordinance), City of Blaine, Skagit County PDS, and San Juan County CD&P. Any I-2066 interim bulletins issued in 2025-2026 that are now withdrawn?
7. **Fee schedules:** the mechanical permit fee tables for the same five jurisdictions.
8. **Design temperatures:** WSEC-R Appendix RC; the WSU sizing-calculator location list; the Puget Sound ASHRAE chapter table; ASHRAE 2021 Fundamentals stations for Bellingham, Friday Harbor, Everett (Paine), Skagit Regional, and Sea-Tac.
9. **Refrigerant:** EPA technology-transitions status in 2026 (any reconsideration outcome); WAC 173-443 residential AC and heat pump dates and GWP limits; WA A2L code amendments.

---

## 11. Source index (every URL surfaced this session, and what it supports)

| URL | Supports | Access |
|---|---|---|
| https://lawfilesext.leg.wa.gov/law/wsr/2024/03/24-03-084.htm | 2021 WSEC-R effective 3/15/2024; EPCA purpose | search extract |
| https://sbcc.wa.gov/sites/default/files/2024-01/WSR_24_03_084_WSEC_R_Comb.pdf | same (SBCC copy) | title |
| https://lawfilesext.leg.wa.gov/law/wsr/2023/21/23-21-105.htm | R403.13 deleted; Table R406.3 reordered with HSPF2 added | search extract |
| https://lawfilesext.leg.wa.gov/law/WACArchive/2023/htm/WAC%20%2051%20%20TITLE/WAC%20%2051%20-%2011R%20CHAPTER/WAC%20%2051%20-%2011R-40610.htm | 2018 WSEC-R "effective until March 15, 2024" | title |
| https://lawfilesext.leg.wa.gov/law/wsr/2025/08/25-08-086.htm | 2024 WSEC-R CR-101, 4/1/2025 | search extract |
| https://lawfilesext.leg.wa.gov/law/wsr/2026/14/26-14-101.htm | 2024 WSEC-R proposed rule (probable) | title |
| https://sbcc.wa.gov/sites/default/files/2026-07/2024WSEC_R_FiledCR102_070126.pdf | 2024 WSEC-R CR-102, 7/1/2026 | title |
| https://sbcc.wa.gov/sites/default/files/2026-06/ResNRG_pCBA_full_v2_062426.pdf | 2024 WSEC-R draft, June 2026 | title |
| https://sbcc.wa.gov/ ; https://sbcc.wa.gov/state-codes-regulations-guidelines/rulemaking | 2024 code adoption delay and May 3, 2027 effective date; I-2066 submittal window | search extract |
| https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40620 | Credit requirements 5.0 / 8.0 / 9.0; per-dwelling-unit rule; 38°F changeover note | search extract |
| https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40621 | Table R406.3 (2021) | title |
| https://app.leg.wa.gov/wac/default.aspx?cite=51-11R-40320 | R403.3 Ducts; buried-duct and inside-envelope definitions | title and extract |
| https://lawfilesext.leg.wa.gov/law/WACArchive/2020/pdf/WAC%20%2051%20%20TITLE/WAC%20%2051%20-%2011R%20CHAPTER/WAC%20%2051%20-%2011R-40621.pdf | 2018 Table R406.3; one option from 3.1 to 3.6; furnace and HSPF 9.5 heat pump options | search extract |
| https://sbcc.wa.gov/sites/default/files/2024-01/2021_WSEC_R_2ndEd_012524.pdf | Full 2021 WSEC-R (verification target) | title |
| https://www.kirklandwa.gov/files/sharedassets/public/v/3/development-services/pdfs/building-pdfs/wsec-r-plan-sheet.pdf | Option 3.1 (Type 1, 95% / 90%); 3.3 HSPF2 8.1; Appendix RC ≤ 23°F cold-climate rule | search extract |
| https://clark.wa.gov/sites/default/files/media/document/2024-11/2021-wsec-compliance-checklist_0.pdf | Heating options 3.1 to 3.7; 2 kW note; "heat pump (w/ supplemental elec. resist. or gas heat)" | search extract |
| https://www.energy.wsu.edu/documents/2021%20WSEC-R%20Single%20Family%20Work%20Sheet%2020241212.pdf | 2021 SF worksheet | title |
| https://wpcdn.web.wsu.edu/cahnrs/uploads/sites/60/2026/05/2021-WSEC-R-Single-Family-Work-Sheet-20241212.pdf | same (mirror) | title |
| https://wpcdn.web.wsu.edu/cahnrs/uploads/sites/60/2026/05/Energy-Credit-Requirements-and-Credit-Options-R406.3.pdf | R406 credit options summary | title |
| https://www.islandcountywa.gov/DocumentCenter/View/6622/2021WSEC-R-SingleFamilyWorkSheet | Credit requirements | search extract |
| https://www.energy.wsu.edu/documents/FAQ%20Two%20heating%20systems.pdf | 2018 Type 2 = 1.0; Type 4 = 0.5; 0.5 W/sf footnote; primary-system rule | search extract |
| https://www.energy.wsu.edu/Documents/Compliance%20Certificate%20Instructions%202018%20WSEC_rev%2007-21-21.pdf | 2018 Type 5 = other (PTAC) | search extract |
| https://customdiggs.com/wp-content/uploads/2022/04/2018-Energy-Credits-Table.pdf ; https://go2kennewick.com/DocumentCenter/View/14434/2018-Energy-Code-Credits | 2018 Type 1 = 0; Type 4 = 0.5 | search extract |
| https://sbcc.wa.gov/sites/default/files/2019-12/R406%20retitled%20amalgamated.pdf | 2018 resistance-only −1.0; all other −1.0 | search extract |
| https://up.codes/s/carbon-emission-equalization | R406.2 title | title |
| https://up.codes/viewer/washington/wa-energy-code-residential-provisions-2018/chapter/RE_4/re-residential-energy-efficiency | 2018 credits 3 / 6 / 7 | search extract |
| https://sanjuancountywa.gov/DocumentCenter/View/10444/Energy-form---standard-residential-2018-WSEC---PDF | 2018 San Juan County form | title |
| https://sanjuancountywa.gov/DocumentCenter/View/29469/2021-Washington-State-Energy-Code-Significant-Changes | 2021 San Juan County handout | title |
| https://cms5.revize.com/revize/cityofsedrowoolley/Departments/Building/Forms%20&%20Documents/2021%20WSEC-R%20Multifamily%20Work%20Sheet%2020240307.pdf | Sedro-Woolley 2021 form | title |
| https://www.sammamish.us/media/drjlljvj/2021-wesc-final.pdf | Ductless option; "ER and DHP not permitted" distribution option | search extract |
| https://sbcc.wa.gov/sites/default/files/2025-06/24_RE_034v3_062325.pdf | 2021 "4" option worth 0.5 credit | search extract |
| https://betterbuiltnw.com/news/washington-state-energy-code-updates-what-to-know | Five system types, 0 to 3 credits; 29 options; heat pump requirement removed | search extract |
| https://insider.energytrust.org/new-2021-washington-state-energy-code/ | Original heat pump mandate text; 3.6 HSPF2 9.4; cold-climate variable-capacity 8.5 HSPF2 | search extract |
| https://everettwa.gov/DocumentCenter/View/37109/2021-Residential-Energy-Code-Compliance-Checklist-PDF?bidId= | Hints at options up to 3.11 | title |
| https://sbcc.wa.gov/sites/default/files/2023-02/Cost-Effectiveness%20of%202021%20WSEC-R.pdf | Air-to-water heat pump option, 1.5 | search extract |
| https://www.pnwig.com/blog-category/energy-efficiency/blogs?blog_id=duct-testing-requirement-for-2021-wa-state-code | WA 2021 duct-testing change | title |
| https://washingtonstatestandard.com/2025/03/21/judge-overturns-washington-natural-gas-measure-approved-by-voters/ | 3/21/2025 Superior Court ruling | search extract |
| https://www.columbian.com/news/2025/mar/23/king-county-judge-natural-gas-measure-is-unconstitutional/ | same | title |
| https://washingtonstatestandard.com/2026/01/22/legal-fight-over-natural-gas-initiative-crescendoes-at-wa-supreme-court/ | Appeal June 2025; argument January 2026 | search extract |
| https://washingtonstatestandard.com/2026/09/17/wa-high-court-tosses-natural-gas-measure-approved-by-voters/ | 9/17/2026 decision, 6-3 | search extract |
| https://www.axios.com/local/seattle/2026/09/17/washington-supreme-court-strikes-down-natural-gas-initiative-2066 | same | title |
| https://www.sierraclub.org/press-releases/2026/09/momentous-win-clean-air-and-energy-affordability-wa-supreme-court-strikes | same | search extract |
| https://www.koin.com/news/washington/taken-that-choice-away-washington-supreme-court-blocks-voter-backed-energy-choice-initiative/ | SBCC advised jurisdictions to apply the 2021 standards | search extract |
| https://www.biaw.com/news/initiative-2066---whats-the-latest | Clark County interim approach | search extract |
| https://citizenportal.ai/articles/6338802/washington/executive/governors-office-boards-commissions/building-code-council/state-building-code-council-rejects-emergency-rulemaking-request-tied-to-initiative-2066 | SBCC 10-2 vote, no emergency | search extract |
| https://www.piercecountywa.gov/CivicSend/ViewMessage/message/256424 | Pierce County continues the 2021 WSEC | search extract |
| https://www.cityofmlt.com/DocumentCenter/View/38060/MLT-Energy-Code-Technical-Bulletin | Mountlake Terrace I-2066 bulletin | title |
| https://washingtonstatestandard.com/2025/02/14/judge-wont-compel-state-panel-to-scrap-building-codes-targeted-by-gas-initiative/ | 2/14/2025 ruling | title |
| https://www.cngc.com/wp-content/uploads/PDFs/energy_choice/washington/2018_WSEC-R-Pathway-to-6.0-Credits_Handout.pdf | 2018 medium house = 6.0 credits | title |
| https://permitbulletin.mercerisland.gov/public/2509-220/SUB1/2509-220%20wsec-energy%20code%20worksheet.pdf | WSU Code Compliance Calculator output format | title |
| https://www.energy.wsu.edu/documents/2021%20WSEC-R%20Compliance%20Certificate.pdf | 2021 compliance certificate | title |

End of digest.
