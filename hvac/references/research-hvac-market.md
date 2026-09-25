# HVAC equipment, parts, prices, labour and subs - Whatcom / Skagit / San Juan - research digest (agent, 9/25/2026)

Scope: residential new-construction HVAC in NW Washington (Bellingham/Whatcom, Skagit, San Juan), market side only: equipment, parts, material prices, labour, wages, sub pricing, scope norms, supply channels, incentives. It feeds the HVAC takeoff + bid engine's parts catalog and its "prices to set" list (section 8).

---

## 0. How to read this digest (evidence tags, limits)

### 0.1 Evidence tags used on every figure

| Tag | Meaning | How much to trust it |
|---|---|---|
| **[S]** | Figure read from the web-search tool's extract of the cited page on 2026-09-25. The page itself could not be opened (see 0.2). | Medium. It is the page's own text as indexed, but it is undated unless noted. Open the URL before locking a price. |
| **[S?]** | Figure appeared in a search extract, but the tool did not tie it to exactly one of the URLs given (candidates listed). | Low-medium. Use for bands, not for catalog cost. |
| **[D]** | Arithmetic derived from sourced figures. The formula is shown. | As good as its inputs. |
| **[K]** | Agent background knowledge; no URL captured this pass. | Verify before use. Never used for a price. |
| **PTS** | Price (or labour unit) **to set**. No sourced number found in this pass. | Needs a quote, counter price or published reference. |

### 0.2 What limited this pass (read before using the numbers)

- **Direct page fetches were blocked.** The org egress proxy refused WebFetch/curl for every domain tried: ecomfort.com, gotductless.com, hvacdirect.com, mitsubishicomfort.com, homeguide.com, bls.gov, supplyhouse.com, lni.wa.gov (all "EGRESS_BLOCKED" / "connect_rejected (organization policy)"). So **every number here comes from search-result extracts**, not from pages I opened.
- **The session web-search budget ran out** (200 of 200 calls, shared across agents) partway through the task. That left the following **mostly unfilled (PTS)**:
  - Section 2: all distribution materials except line sets (flex, pipe, boots, registers, line-hide, pumps, refrigerant, and so on).
  - Section 3: published task-level labour units (RSMeans or Craftsman-type).
  - Section 4.1: BLS OEWS and WA L&I prevailing wages.
  - Section 6: branch addresses of Bellingham supply houses.
  - Section 7: PSE new-construction, Cascade Natural Gas and OPALCO programs.
- **Price basis.** Equipment and parts prices are **US internet-retailer "street" prices** (HVACDirect/OnlineSupply, AC Wholesalers, Got Ductless, SupplyStop, Skip the Warehouse, Home Depot, Lowe's, SupplyHouse). They are national, not Whatcom counter prices. Contractor distributor pricing (Johnstone, Gensco, Ferguson and similar) is account-gated and was not observed.
- **Tax and shipping.** No WA sales tax or freight is included anywhere (the Bellingham/Whatcom tax rate is PTS).
- **Dates.** "Special price" and "was/list price" are the retailer's own labels. Retailer pages are undated in the extracts, so read them as "as indexed, 2025-2026". Where a source carries a date, it is given.

### 0.3 Regional vs national
- **PNW / local sources found:**
  - Barron Heating (Bellingham) blog.
  - Clean Air Heating & Cooling (Bellingham) pages.
  - Homeyou Bellingham cost page.
  - Angi Seattle pages.
  - WA-state heat-pump cost pages.
- **National:** everything else (HomeGuide, Angi national, Fixr, EnergySage, This Old House, Modernize, all online retailers).

---

## 1. Equipment classes and price bands

### 1.0 Refrigerant transition: what is current in 2025-2026 and model-number mapping

Most legacy R-410A lines that the brief names are listed as discontinued by retailers. The current (R-454B / R-32) successors are what a 2026 new-construction bid should carry.

| Class | Legacy (R-410A) named in brief | Current 2025-26 successor seen at retail | Refrigerant | Evidence |
|---|---|---|---|---|
| Mitsubishi single-zone hyper-heat wall (Deluxe) | MSZ-FS__NA / MUZ-FS__NAH (H2i Plus) | MSZ-FX__NL / MUZ-FX__NLHZ ("FX-Series H2i sumo") | R-454B | [S] FS listed discontinued: https://www.ecomfort.com/Mitsubishi-HVAC-MSZ-FS18NA-MUZ-FS18NA/p112559.html ; FX system pages: https://hvacdirect.com/12-000-btu-mitsubishi-fx-series-29-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx12nlhz-msz-fx12nl-199107.html |
| Mitsubishi mid-tier wall | (GL/GS family) | MSZ-GX__NL with MUZ-GX__NL or MUZ-GX__NLHZ | R-454B | [S] https://hvacdirect.com/12-000-btu-mitsubishi-gx-series-25-6-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-gx12nlhz-msz-gx12nl-199114.html |
| Mitsubishi multi-zone hyper-heat outdoor | MXZ-SM__NAMHZ (e.g. MXZ-SM48NAMHZ) | MXZ-SM36/42/48NLHZ; MXZ-3D24/30NLHZ | R-454B | [S] https://hvacdirect.com/mitsubishi-h2i-48-000-btu-multi-zone-ductless-heat-pump-condenser-mxz-sm48namhz-u1.html ; https://onlinesupply.com/48000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm48nlhz.html |
| Mitsubishi slim ducted | SEZ-KD__NA | SEZ-AD__NL (HVACDirect titles it "KD-Series ... SEZ-AD09NL") | R-454B | [S] https://hvacdirect.com/9-000-btu-mitsubishi-kd-series-concealed-duct-mini-split-air-handler-r454b-sez-ad09nl.html |
| Mitsubishi 4-way cassette | SLZ-KF__NA | SLZ-AF__NL (with SLP-18FAU grille) | R-454B | [S] https://hvacdirect.com/hvac/pdf/SLZ-KF12NA-Submittal.pdf ; https://www.acwholesalers.com/Mitsubishi-HVAC-SLZ-AF12NL/p168592.html |
| Mitsubishi P-series horizontal ducted | PEAD-A__AA7 | PEAD-AA__NL | R-454B | [S] https://www.acwholesalers.com/Mitsubishi-HVAC-PEAD-AA24NL/p160431.html |
| Mitsubishi multi-position air handler (ducted central) | PVA-A__AA7 + PUZ-HA__NHA5/NKA; SVZ-KP__NA + SUZ-KA__NAHZ | PVA-AA__NL + PUZ-AK__NL(HZ); SVZ-AP__NL + SUZ-AK__NLHZ / SUZ-AA__NL | R-454B | [S] https://hvacdirect.com/mitsubishi-3-ton-19-5-seer2-ducted-central-air-inverter-heat-pump-split-system-r454b-201915.html ; https://hvacdirect.com/mitsubishi-3-ton-15-2-seer2-ducted-central-air-inverter-h2i-heat-pump-split-system-r454b-198648.html |
| Fujitsu single-zone extra-low-temp | 9/12/15RLS3H (XLTH, "Halcyon") | AIRSTAGE Orion XLTH: ASUH__KZAS / AOUH__KZAH1; Orion XLTH+ (launched Jun 2025) | R-32 | [S] RLS3H discontinued: https://www.ecomfort.com/Fujitsu-12RLS3H/p65511.html ; Orion XLTH: https://www.fujitsugeneral.com/us/products/split/wall/r32/kzah1.html ; XLTH+: https://www.hvacrbusiness.com/news/2025/jun/11/fujitsu-introduces-airstage-orion-xlth-cold-climate-heat-pump/ |
| Fujitsu multi-zone extra-low-temp | AOU24/36/48RLXFZH | AOUH24KWAH3 (3-zone), AOUH36KWAH4 (4-zone) | R-32 | [S] AOU36RLXFZH discontinued: https://www.ecomfort.com/Fujitsu-AOU36RLXFZH/p72694.html ; https://gotductless.com/products/fujitsu-aouh24kwah3-3-zone-24-000-btu-extra-low-temperature-multi-zone-outdoor-unit |
| Daikin Aurora single-zone | FTX__AXVJU / RXL__QMVJU (older Aurora) | FTXV__AVJU9 / RXT__AVJU9 | R-32 | [S] https://hvacdirect.com/12-000-btu-daikin-aurora-21-seer2-single-zone-wall-mount-mini-split-heat-pump-system-r32-230v-194698.html |
| Bosch IDS ducted heat pump | BOVA (R-410A) [K] | BOVA-36RXB-M15S / BOVA-36RTB-M20S + BIVA air handlers | R-454B | [S] https://www.budgetheating.com/3-ton-bosch-ids-light-14-3-seer2-r454b-heat-pump-inverter-system-bova-36rxb-m15s-biva-36rxb-m15x/ |

**Facts that matter for bids:**
- **GWP.** R-454B has a GWP of 466, versus 2,088 for R-410A. [S] https://goendlessenergy.com/blog/hvac/comparing-mitsubishi-410a-models-to-454b-models/
- **Built-in Wi-Fi.** Mitsubishi's R-454B equipment now **includes Wi-Fi**, which cuts demand for the separate kumo adapter. Verify per model. [S] same URL.
- **Low-temperature operation.** Some R-454B Mitsubishi models operate down to -22°F (previously -15°F). [S] same URL.
- **Lower minimum capacity on the SM36.** The 4-port MXZ-SM36NLHZ has a lower minimum capacity. [S] same URL.
- **FX-Series heating.** A retailer extract describes the FX "H2i sumo" as delivering 100% heating capacity down to -10°F. [S?] https://www.acwholesalers.com/Mitsubishi-HVAC-MUZ-FX09NLHZ-MSZ-FX09NL/p168758.html
- **Orion XLTH+ (Fujitsu).** 9k, 12k and 15k BTU/h:
  - 100% rated capacity at -15°F and 90% at -22°F.
  - Up to 33.5 SEER2.
  - Maximum heating 24,000 / 27,300 / 28,000 BTU/h.
  - News item dated **2025-06-11**. [S] https://www.hvacrbusiness.com/news/2025/jun/11/fujitsu-introduces-airstage-orion-xlth-cold-climate-heat-pump/
- **R-454B launch date.** Mitsubishi's new-product page was summarised as "R-454B product launches effective April 1, 2026 for certain M-Series models". [S?] https://www.mitsubishicomfort.com/new-product

### 1a. Ductless mini-split, single-zone, cold-climate

#### 1a.1 Equipment street price: complete single-zone systems (indoor + outdoor)

| Model (system) | Nominal | Refrig. | SEER2 | Street price (retailer "special") | Retailer list / "was" | Derived $/nominal ton | Source |
|---|---|---|---|---|---|---|---|
| Mitsubishi MSZ-FX09NL / MUZ-FX09NLHZ | 9k | R-454B | 33.1 | **$2,811.75-$2,814.75**; a second listing shows $3,092.93 | $3,518.44 | $3,753 [D: 2,814.75/0.75] | [S] https://hvacdirect.com/9-000-btu-mitsubishi-fx-series-33-1-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx09nlhz-msz-fx09nl-199106.html ; https://onlinesupply.com/9-000-btu-mitsubishi-fx-series-33-1-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx09nlhz-msz-fx09nl-199106.html ; second listing [S?] https://hvacdirect.com/15000-btu-mitsubishi-fx-series-33-1-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx09nlhz-msz-fx09nl-199106.html |
| Mitsubishi MSZ-FX12NL / MUZ-FX12NLHZ | 12k | R-454B | 29.9 | **$3,159.00** | $3,948.75 | $3,159 [D] | [S] https://hvacdirect.com/12-000-btu-mitsubishi-fx-series-29-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx12nlhz-msz-fx12nl-199107.html ; https://onlinesupply.com/12-000-btu-mitsubishi-fx-series-29-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx12nlhz-msz-fx12nl-199107.html |
| Mitsubishi MSZ-FX15NL / MUZ-FX15NLHZ | 15k | R-454B | 25.9 | **$3,633.75** | $4,542.19 | $2,907 [D: 3,633.75/1.25] | [S] https://hvacdirect.com/15000-btu-mitsubishi-fx-series-25-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx15nlhz-msz-fx15nl-199108.html ; https://onlinesupply.com/15000-btu-mitsubishi-fx-series-25-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx15nlhz-msz-fx15nl-199108.html |
| Mitsubishi MSZ-FX18NL / MUZ-FX18NLHZ | 18k | R-454B | 25.5 | **$4,230.75** (OnlineSupply); a customer review cites paying $5,200 | $5,288.44 | $2,821 [D: 4,230.75/1.5] | [S?] https://hvacdirect.com/18000-btu-mitsubishi-fx-series-25-5-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx18nlhz-msz-fx18nl-199109.html |
| Mitsubishi MSZ-GX09NL / MUZ-GX09NL(HZ) (mid-tier) | 9k | R-454B | 28.4 | $2,466.00 | $3,082.50 | $3,288 [D] | [S?] (NL vs NLHZ outdoor not confirmed) https://hvacdirect.com/9-000-btu-mitsubishi-gx-series-28-4-seer2-single-wall-mounted-mini-split-heat-pump-system-r454b-muz-gx09nl-msz-gx09nl-199111.html |
| Mitsubishi MSZ-GX12NL / MUZ-GX12NLHZ (mid-tier hyper) | 12k | R-454B | 25.6 | $2,536.50 | $3,170.63 | $2,537 [D] | [S?] https://hvacdirect.com/12-000-btu-mitsubishi-gx-series-25-6-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-gx12nlhz-msz-gx12nl-199114.html |
| Mitsubishi MSZ-FS09NA / MUZ-FS09NAH (legacy, discontinued) | 9k | R-410A | 29.8 | $2,856 sale (one retailer) | $2,944 | n/a | [S?] retailer not identified. Candidates: https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FS09NA-MUZ-FS09NAH/p112561.html ; https://www.budgetheating.com/Mini-Split-9K-BTU-Mitsubishi-30-SEER-H2i-MUZ-MSZ-p/163118.htm |
| Mitsubishi MSZ-FS12NA + MUZ-FS12NA (legacy) | 12k | R-410A | 26.3 | $3,316.75 [D: indoor $1,049.04 + outdoor $2,267.71] | n/a | n/a | [S] Skip the Warehouse, prices shown July 2026: https://skipthewarehouse.com/product/mitsubishi-msz-fs12na-u1-1-ton-deluxe-h2i-plus-wall-mounted-indoor-unit/ |
| Fujitsu ASUH12KZAS / AOUH12KZAH1 (Orion XLTH) | 12k | R-32 | 30.5 | **PTS** (outdoor alone $2,169.30, see 1a.2) | n/a | n/a | [S] https://gotductless.com/products/fujitsu-asuh12kzas-aouh12kzah1-12-000-btu-30-5-seer2-extra-low-temperature-wall-mounted-system |
| Fujitsu ASUH09KZAS / AOUH09KZAH1 (Orion XLTH) | 9k | R-32 | 33.1 | PTS | n/a | n/a | [S] https://gotductless.com/products/fujitsu-asuh09kzas-aouh09kzah1-9-000-btu-33-1-seer2-extra-low-temperature-wall-mounted-heat-pump-system |
| Fujitsu ASUH15KZAS / AOUH15KZAH1 (Orion XLTH) | 15k | R-32 | 27.5 | PTS | n/a | n/a | [S] https://gotductless.com/products/fujitsu-asuh15kzas-aouh15kzah1-15-000-btu-27-5-seer2-extra-low-temperature-orion-xlth-wall-mounted-system |
| Daikin FTXV12AVJU9 / RXT12AVJU9 (Aurora) | 12k | R-32 | 21 | **$2,290.40-$2,339.00** | $2,938.80-$3,185.90 | $2,290-$2,339 [D] | [S] https://hvacdirect.com/12-000-btu-daikin-aurora-21-seer2-single-zone-wall-mount-mini-split-heat-pump-system-r32-230v-194698.html |
| Daikin FTXV18AVJU9 / RXT18AVJU9 (Aurora) | 18k | R-32 | 19.8-21 | **$3,571.00-$4,113.23** (HVACDirect $3,731.60) | $4,710.00 (one listing $7,142.40) | $2,381-$2,742 [D] | [S] https://hvacdirect.com/18-000-btu-daikin-aurora-21-seer2-single-zone-wall-mount-mini-split-heat-pump-system-r32-230v-194700.html ; other listings [S?] https://www.totalhomesupply.com/p/daikin-ftxv18avju9-rxt18avju9-18000-btu-19-8-seer2-aurora-series-heat-cool-single-zone-mini-split-system-r32-refrigerant ; https://heatandcool.com/products/daikin-18-000-btu-19-8-seer2-aurora-series-low-ambient-ductless-mini-split-wall-mount-heat-pump-air-conditioner-r32-wi-fi-enabled |
| Daikin FTX12AXVJU / RX12AXVJU ("19 Series", older, not Aurora) | 12k | R-410A | 19 | $1,591.26 | n/a | n/a | [S?] https://sharkaire.com/12000-BTU-Daikin-19-Series-RX12AXVJU-FTX12AXVJU |

Notes:
- **Daikin Aurora 12k performance.** 10,600 BTU/h cooling and 13,500 BTU/h heating; up to 21 SEER2, 10.2 HSPF2 and 12 EER2. [S] https://hvacdirect.com/12-000-btu-daikin-aurora-21-seer2-single-zone-wall-mount-mini-split-heat-pump-system-r32-230v-194698.html
- **Room sizing on retailer pages.** Retailers suggest FX09 for rooms up to about 350 sf, FX12 up to about 500 sf, FX15 up to about 650 sf and FX18 up to about 750 sf. These are marketing figures, not Manual J. [S] https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FX09NL/p160343.html ; https://hvacdirect.com/15000-btu-mitsubishi-fx-series-25-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx15nlhz-msz-fx15nl-199108.html

#### 1a.2 Equipment street price: indoor-only and outdoor-only (for catalog line items)

| Item | Price | Source |
|---|---|---|
| MSZ-FX09NL wall head (single or multi-zone use) | **$879.00** (AC Wholesalers); $987.00 (SupplyStop) | [S] https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FX09NL/p160343.html ; https://www.supplystop.com/products/msz-fx09nl-9-000-btu-h-wall-mounted-indoor-unit |
| MSZ-FX12NL wall head | **$1,034.00** (AC Wholesalers) | [S] https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FX12NL/p160344.html |
| MUZ-FX18NLHZ-U1 outdoor (1.5 ton, single-zone) | $3,261.86 | [S?] Skip the Warehouse listing, seen in the extract of https://skipthewarehouse.com/product/mitsubishi-msz-fx18nl-u1-15-ton-deluxe-wall-mounted-indoor-unit-r-454b/ |
| MSZ-FS12NA-U1 indoor (legacy R-410A) | $1,049.04 (July 2026) | [S] https://skipthewarehouse.com/product/mitsubishi-msz-fs12na-u1-1-ton-deluxe-h2i-plus-wall-mounted-indoor-unit/ |
| MUZ-FS12NA-U1 outdoor (legacy R-410A) | $2,267.71 (July 2026) | [S] same URL (related listing) |
| MUZ-FS09NAH-U1 outdoor (legacy) | $1,976.18 ("one distributor") | [S?] candidate: https://www.mylinkdrive.com/USA/MUZ_FS09NAH_U1?product=&categoryName=R410A_Outdoor |
| Fujitsu AOUH12KZAH1 outdoor (Orion XLTH 12k); must be matched with ASUH12KZAS | **$2,169.30** "regular price" | [S] https://gotductless.com/products/fujitsu-aouh12kzah1-12-000-btu-orion-xlth-extra-low-temperature-outdoor-heat-pump |
| Fujitsu ASUH12KZAS indoor (Orion XLTH 12k) | PTS | page: https://gotductless.com/products/fujitsu-asuh12kzas-9-000-btu-orion-xlth-wall-mounted-indoor-unit ; https://www.aprsupply.com/item/FUJ-ASUH12KZAS-12000-BTU-High-Tier |

**Derived split [D].** On the legacy FS12 pair, the outdoor unit is about 68% of system equipment cost (2,267.71 / 3,316.75). Use this only as a sanity check when a system price is known but the indoor/outdoor split is not.

#### 1a.3 Installed price bands, single-zone (national, WA and local)

| Source (date) | Scope | Installed band | Source URL |
|---|---|---|---|
| HomeGuide (2026) | Single-zone mini-split AC, installed | **$2,500-$6,000** | [S] https://homeguide.com/costs/ductless-mini-split-ac-cost |
| HomeGuide (2026) | Wall-mounted, **per zone** installed | **$2,500-$5,000 per zone** | [S] https://homeguide.com/costs/ductless-mini-split-ac-cost |
| HomeGuide (2026) | Floor-mounted, per zone installed | $3,000-$5,000 per zone | [S] https://homeguide.com/costs/ductless-mini-split-ac-cost |
| HomeGuide (2026) | Mini-split heat pump, single zone | $2,000-$4,000 | [S] https://homeguide.com/costs/ductless-heat-pump-cost |
| HomeGuide (2026) | Labour only, mini-split heat pump | $1,000-$5,000 | [S] https://homeguide.com/costs/ductless-mini-split-ac-cost |
| Angi (2026 data, national) | Labour only, single-zone | $300-$2,000 | [S] https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac.htm |
| **Angi Seattle, WA** | Mini-split installed | **$2,222-$5,555, average $3,333**; labour is 40-65% of cost | [S] https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/wa/seattle |
| Angi Seattle, WA | "Per project" for HVAC pros | $5,000-$14,000+ | [S] same URL |
| This Old House (2026) | Split AC install, average (all zone counts) | $11,000; single-zone about $3,250 | [S?] https://www.thisoldhouse.com/heating-cooling/split-ac-installation-cost |
| EnergySage (2025) | Ductless mini-split system, average after state/local incentives | $19,556 (read as a whole-home multi-head average) | [S?] https://www.energysage.com/heat-pumps/how-much-does-a-mini-split-cost/ |
| **Barron Heating (Bellingham), blog URL dated 2025/june** (extract says the page appears to be April 2026) | Ductless mini-split, Bellingham | **$3,000-$10,000** depending on zones | [S] https://www.barronheating.com/blog/2025/june/heat-pump-installation-cost-in-bellingham-wa/ |
| **Clean Air Heating & Cooling (Bellingham)** | Mini-split, Bellingham | **$3,000-$10,000+**; single-zone at the low end | [S] https://callcleanair.com/hvac-services/mini-splits/ |
| **Homeyou, Bellingham** (88 projects; "valid through 04/23/2026"; page labelled 08/2026) | "Heat pump", all types | average **$5,301-$6,973**; range $2,793-$10,058 | [S] https://www.homeyou.com/wa/heat-pump-bellingham-costs |
| 2026 aggregator guides | By capacity: 9k $1,200-$2,400; 12k $1,500-$3,100; 18k $1,900-$4,300 installed | Low; looks DIY-weighted, do not use for pro bids | [S?] candidates https://realcostiq.com/guides/mini-split-installation-cost/ ; https://filterbuy.com/heating-cooling/mini-splits/cost/mini-split-installation-cost/ |

**Implied labour hours, Seattle single-zone [D]:**
- On the average price: $3,333 × (40% to 65%) = $1,333 to $2,166 of labour. At $140-$260/h that is about **5.1-15.5 billed hours**.
- On the full price range: $2,222 × 40% at $260/h gives about 3.4 h; $5,555 × 65% at $140/h gives about 25.8 h.
- Inputs: https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/wa/seattle

### 1b. Multi-zone outdoor units and indoor units (wall, cassette, slim ducted)

#### 1b.1 Multi-zone outdoor units

| Model | Capacity / ports | Refrig. | Street price | "Was" / list | Derived $/ton | Source |
|---|---|---|---|---|---|---|
| Mitsubishi MXZ-3D24NLHZ (H2i) | 24k / up to 3 | R-454B | **$4,659.75** | $5,824.69 | $2,330 [D] | [S] https://onlinesupply.com/24000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-3d24nlhz.html |
| Mitsubishi MXZ-3D30NLHZ (H2i) | 30k / up to 3 | R-454B | **PTS** ("add to cart" price) | n/a | n/a | [S] https://hvacdirect.com/30000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-3d30nlhz.html |
| Mitsubishi MXZ-SM36NLHZ (Smart Multi H2i) | 36k / 2-4 | R-454B | **$5,473.00-$5,476.75** | $6,020.30 | $1,824 [D] | [S] https://onlinesupply.com/36000-btu-mitsubishi-m-series-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm36nlhz.html ; https://www.supplystop.com/products/mxz-sm36nlhz-36-000-btu-h-hyper-heat-pump-outdoor-unit |
| Mitsubishi MXZ-SM42NLHZ (Smart Multi H2i) | 42k / 2-5 | R-454B | **PTS** ("add to cart" price) | n/a | n/a | [S] https://onlinesupply.com/42000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm42nlhz.html |
| Mitsubishi MXZ-SM48NLHZ (Smart Multi H2i) | 48k / 2-8 | R-454B | **$7,635.75** | $9,544.69 | $1,909 [D] | [S] https://onlinesupply.com/48000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm48nlhz.html |
| Fujitsu AOUH36KWAH4 (XLTH multi) | 36k / 4 | R-32 | **$5,180.00** | n/a | $1,727 [D] | [S] https://skipthewarehouse.com/product/fujitsu-aouh36kwah4-3-ton-r-32-ductless-mini-split-outdoor-heat-pump/ |
| Fujitsu AOUH24KWAH3 (XLTH multi; -15°F; base-pan heater) | 24k / 3 | R-32 | PTS | n/a | n/a | [S] https://gotductless.com/products/fujitsu-aouh24kwah3-3-zone-24-000-btu-extra-low-temperature-multi-zone-outdoor-unit |
| Fujitsu AOU24RLXFZH (legacy XLTH; out of stock) | 24k / 2-3 | R-410A | $3,438.75 / $3,924.90 (the extract shows both "regular" and "current") | n/a | n/a | [S] https://gotductless.com/products/fujitsu-24-000-btu-extra-low-temp-outdoor-heat-pump-aou24rlxfzh |
| Fujitsu AOU36RLXFZH (legacy XLTH) | 36k / 2-4 | R-410A | discontinued | n/a | n/a | [S] https://www.ecomfort.com/Fujitsu-AOU36RLXFZH/p72694.html |

#### 1b.2 Indoor units for multi-zone (or single-zone) systems

| Indoor unit | Type | Refrig. | Street price | Source |
|---|---|---|---|---|
| MSZ-FX09NL | Deluxe wall | R-454B | **$879.00** / $987.00 | [S] https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FX09NL/p160343.html ; https://www.supplystop.com/products/msz-fx09nl-9-000-btu-h-wall-mounted-indoor-unit |
| MSZ-FX12NL | Deluxe wall | R-454B | **$1,034.00** | [S] https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FX12NL/p160344.html |
| MSZ-FX15NL / MSZ-FX18NL | Deluxe wall | R-454B | PTS | pages: https://hvacdirect.com/15000-btu-mitsubishi-fx-series-single-or-multi-zone-wall-mounted-mini-split-air-handler-r454b-msz-fx15nl.html ; https://hvacdirect.com/18000-btu-mitsubishi-fx-series-single-or-multi-zone-wall-mounted-mini-split-air-handler-r454b-msz-fx18nl.html |
| MSZ-GX09NL / MSZ-GX12NL | Mid-tier wall | R-454B | PTS (indoor-only price not in extract) | pages: https://gotductless.com/products/mitsubishi-msz-gx09nl-9-000-btu-wall-mounted-unit ; https://hvacdirect.com/12000-btu-mitsubishi-gx-series-single-or-multi-zone-wall-mounted-mini-split-air-handler-r454b-msz-gx12nl.html |
| **SEZ-AD09NL** | Slim/low-static ducted (7-7/8 in tall) | R-454B | **$1,232.00** (AC Wholesalers). HVACDirect shows "$2,715.00 special / was $3,393.76" on its SEZ-AD09NL listing, which is probably a system price. | [S] https://www.acwholesalers.com/Mitsubishi-HVAC-SEZ-AD09NL/p160495.html ; [S?] https://hvacdirect.com/9-000-btu-mitsubishi-kd-series-concealed-duct-mini-split-air-handler-r454b-sez-ad09nl.html |
| SEZ-AD12NL | Slim ducted | R-454B | PTS. HVACDirect "$3,028.50 special / was $3,785.63" is probably a system price. | [S?] https://hvacdirect.com/brands/mitsubishi-products/mitsubishi-mini-splits-by-mounting-type/mitsubishi-concealed-duct-mini-splits.html ; page: https://www.acwholesalers.com/Mitsubishi-HVAC-SEZ-AD12NL/p160496.html |
| **SLZ-AF12NL-U1** | 4-way ceiling cassette (2x2 grid) with grille | R-454B | **$1,266.94** | [S] https://skipthewarehouse.com/product/mitsubishi-slz-af12nl-u1-12000-btu-ceiling-cassette-indoor-unit-r454b/ |
| MLZ-KX12NL | One-way cassette | R-454B | PTS | page: https://gotductless.com/products/mitsubishi-mlz-kx12nl-12-000-btu-one-way-ceiling-cassette-unit-unit-only |
| MFZ-KX12NL | Floor console | R-454B | PTS | page: https://skipthewarehouse.com/product/mitsubishi-mfz-kx12nl-1-ton-idu-floor-mount-r454b/ |
| PEAD-A24AA7 (legacy) | P-series horizontal ducted, mid-static | R-410A | $2,235.00 "regular price" | [S?] https://www.acwholesalers.com/Mitsubishi-HVAC-PEAD-A24AA7/p84620.html |
| PEAD-AA24NL | P-series horizontal ducted | R-454B | PTS ("Contact us for best price") | [S] https://gotductless.com/products/mitsubishi-pead-aa24nl-24-000-btu-horizontal-ducted-indoor-unit ; https://www.acwholesalers.com/Mitsubishi-HVAC-PEAD-AA24NL/p160431.html |

**Single-zone ducted and cassette systems (useful when one ducted head serves a floor):**

| System | Street price | Source |
|---|---|---|
| SEZ-AD09NL + SUZ-AA09NLHZ (9k slim-ducted, hyper; 14.8 SEER2) | **$3,220.00** sale | [S] https://gotductless.com/products/mitsubishi-sez-ad09nl-suz-aa09nlhz-9-000-btu-horizontal-ducted-hyper-heatsystem |
| SEZ-AD09NL + SUZ-AA09NL (9k slim-ducted, standard; 17.6 SEER2) | $2,563.00 | [S] https://gotductless.com/products/mitsubishi-sez-ad09nl-suz-aa09nl-9-000-btu-horizontal-ducted-system |
| SUZ-AA12NL + SLZ-AF12NL (12k cassette) | $3,623.75 special | [S?] https://hvacdirect.com/brands/mitsubishi-products/mitsubishi-mini-splits/mitsubishi-single-zone-mini-split-systems/filter/ceiling-cassette.html |
| SUZ-AA09NLHZ + SLZ-AF09NL (9k cassette, hyper) | $3,195.00 special | [S?] same URL |

**Worked equipment bundles [D]** (mixed retailers, equipment only, no accessories):
- **3 heads on an SM36:** MXZ-SM36NLHZ $5,473.00 + 2 × MSZ-FX09NL $879.00 + 1 × MSZ-FX12NL $1,034.00 = **$8,265.00**, about **$2,755 per head**. Inputs: the OnlineSupply SM36 URL and the AC Wholesalers FX09/FX12 URLs in the tables above.
- **5 heads on an SM48:** MXZ-SM48NLHZ $7,635.75 + 4 × MSZ-FX09NL $879.00 + 1 × MSZ-FX12NL $1,034.00 = **$12,185.75**, about **$2,437 per head**. Same sources.

#### 1b.3 Installed price bands, multi-zone

| Source | Band | URL |
|---|---|---|
| HomeGuide (2026) | Multi-zone mini-split **$6,500-$15,000+** installed; ductless heat pump $2,000-$17,000+ depending on zones | [S] https://homeguide.com/costs/ductless-mini-split-ac-cost ; https://homeguide.com/costs/ductless-heat-pump-cost |
| Angi (2026, national) | Labour only, multi-zone **$700-$3,000** | [S] https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac.htm |
| 2026 guide (aggregator) | 3-zone (living, master, office) $6,500-$11,000; "mini split labor cost runs $500 to $2,000 per zone nationally" | [S?] candidates https://hvacprojectcost.com/mini-split-installation-cost/ ; https://realcostiq.com/guides/mini-split-installation-cost/ |
| Modernize | 4-zone ductless heat pump **$8,500-$10,000** "for installation costs" | [S?] https://modernize.com/hvac/heating-repair-installation/heat-pump/ductless |
| Barron / Clean Air (Bellingham) | $3,000-$10,000(+), rising with zones | [S] https://www.barronheating.com/blog/2025/june/heat-pump-installation-cost-in-bellingham-wa/ ; https://callcleanair.com/hvac-services/mini-splits/ |

### 1c. Centrally ducted air-source heat pump, 2-4 ton, air handler + electric strip

#### 1c.1 Equipment street price

| System | Size | Refrig. | Street price | List / SRP | Derived $/ton | Source |
|---|---|---|---|---|---|---|
| Mitsubishi **PUZ-AK36NL + PVA-AA36NL** (P-series multi-position air handler; the listing title says 18.1 SEER2, the text says 19.5 SEER2 / 8.5 HSPF2; outdoor is non-"HZ", so standard heat) | 3 ton | R-454B | **$8,015.25** | $9,485.59 | $2,672 [D] | [S] https://hvacdirect.com/mitsubishi-3-ton-19-5-seer2-ducted-central-air-inverter-heat-pump-split-system-r454b-201915.html |
| Mitsubishi PUZ-AK36NLHZ (hyper-heat P-series outdoor, R-454B) | 3 ton | R-454B | PTS | n/a | n/a | page: https://hvacdirect.com/36000-btu-mitsubishi-p-series-single-zone-mini-split-hyper-heat-pump-condenser-r454b-puz-ak36nlhz.html |
| Mitsubishi **PVA-A36AA7 + PUZ-HA36NHA5 + MHK2** (legacy H2i, 17.8 SEER) | 3 ton | R-410A | **$11,897.00** | SRP $13,219.00 | $3,966 [D] | [S] https://hvacdirect.com/mitsubishi-36-000-btu-17-8-seer-single-zone-heat-pump-system-id9753.html |
| Mitsubishi SVZ-AP36NL + SUZ-AK36NLHZ (M-series multi-position AH, H2i, 15.2 SEER2) | 3 ton | R-454B | PTS | n/a | n/a | page: https://hvacdirect.com/mitsubishi-3-ton-15-2-seer2-ducted-central-air-inverter-h2i-heat-pump-split-system-r454b-198648.html ; https://gotductless.com/products/mitsubishi-svz-ap36nl-suz-ak36nlhz-36-000-btu-hyper-heating-multi-position-air-handler-system |
| Mitsubishi SVZ-KP36NA air handler only (legacy) | 3 ton | R-410A | $2,188.00 "regular price" | n/a | n/a | [S?] https://gotductless.com/products/svz-kp36na-mitsubishi-kp-36-000-btu-multi-position-air-handler |
| Bosch **BOVA-36RXB-M15S** condenser only (IDS, variable speed, operating range 36-130%, up to 15 SEER2) | 3 ton | R-454B | **$3,888.00** | n/a | $1,296 condenser-only [D] | [S] https://shop.unicosystem.com/bosch-3-ton-r-454-b-variable-speed-15-seer2-heat-pump |
| Bosch IDS Light BOVA-36RXB-M15S + BIVA-36RXB-M15X (14.3 SEER2) | 3 ton | R-454B | PTS | n/a | n/a | page: https://www.budgetheating.com/3-ton-bosch-ids-light-14-3-seer2-r454b-heat-pump-inverter-system-bova-36rxb-m15s-biva-36rxb-m15x/ ; https://hvacdirect.com/bosch-ids-light-series-3-ton-14-5-seer2-ducted-central-air-inverter-heat-pump-split-system-r454b-201064.html |
| Bosch IDS Plus BOVA-36RXB-M15S + BIVA-36RCB-M20X (17 SEER2) | 3 ton | R-454B | PTS | n/a | n/a | page: https://www.budgetheating.com/3-ton-bosch-ids-plus-17-seer2-r454b-heat-pump-inverter-system-bova-36rxb-m15s-biva-36rcb-m20x/ |
| Bosch Premium Connected BOVA-36RTB-M20S + BIVA-36RCB-M20X (19 SEER2) | 3 ton | R-454B | PTS | n/a | n/a | page: https://www.budgetheating.com/3-ton-bosch-premium-connected-19-seer2-r454b-heat-pump-inverter-system-bova-36rtb-m20s-biva-36rcb-m20x/ |
| Bosch 2025 residential price book (list prices, manufacturer rep) | all | R-454B | **Unread PDF**. Read it for list prices. | n/a | n/a | https://tssassociatesinc.com/wp-content/uploads/2025/01/2025-Residential-AC-Price-Book-US-CA-R454B_76HPL1801V.pdf |
| Daikin FIT DZ17VSA361 (side-discharge) | 3 ton | R-410A (newer FIT is R-32 per 1c.2) | PTS (Ferguson page) | n/a | n/a | page: https://www.ferguson.com/product/daikin-dz17vsa-series-3-ton---up-to-18-seer-%2F-10-hspf-split-heat-pump---208%2F230%2F1---r-410a-ddz17vsa361ba/9766071.html |
| Carrier/Bryant, Trane/American Standard | 2-4 ton | R-454B | **PTS**. Dealer-only brands; no street price captured. | n/a | n/a | n/a |
| Generic 3-ton air handler, equipment only | 3 ton | n/a | **$900-$1,500** | n/a | n/a | [S] https://homeguide.com/costs/air-handler-cost |
| Electric strip-heat kits (5/8/10 kW) for the above air handlers | n/a | n/a | **PTS** | n/a | n/a | n/a |

#### 1c.2 Installed price bands, ducted

| Source (date) | Scope | Band | URL |
|---|---|---|---|
| HomeGuide (2026) | Air-source heat pump, average-size house | **$10,000-$25,000+** installed | [S] https://homeguide.com/costs/air-source-heat-pump-cost |
| HomeGuide (2026) | "Most common ... central ducted system" | **$4,000-$12,000** | [S] https://homeguide.com/costs/air-source-heat-pump-cost |
| 2026 guides | 3-ton heat pump incl. labour | $3,900-$6,200 | [S?] candidates https://homeguide.com/costs/heat-pump-cost ; https://www.hvacbase.org/heat-pump-cost-to-install |
| 2026 guides | New ductwork where none exists, added to heat pump cost | $5,000-$10,000 | [S?] candidates https://homeguide.com/costs/heat-pump-cost ; https://www.angi.com/articles/how-much-does-heat-pump-cost.htm |
| Fixr (2026) | Heat pump installed | **$5,000-$15,000**, national average $8,350 | [S] https://www.fixr.com/costs/heat-pump-installation |
| hvacprojectcost.com (2026 guide) | **Daikin FIT** installed | **$6,500-$16,500** by tonnage | [S] https://hvacprojectcost.com/daikin-fit-cost/ |
| hvacprojectcost.com | Homeowner-reported quotes (Reddit, cited on the page) | 4-ton **R-32** FIT **$13,140** (2026); 4-5 ton FIT $13,000-$14,000 (2025); side-discharge $6,000-$15,000 | [S] https://hvacprojectcost.com/daikin-fit-cost/ |
| hvacprojectcost.com | Exclusions from those ranges | Duct replacement, panel upgrade and permits add **$1,500-$5,000+** | [S] https://hvacprojectcost.com/daikin-fit-cost/ |
| heatpumpcostbystate.com (2026) | Washington average, installed | **$15,500** | [S] https://heatpumpcostbystate.com/states/washington |
| WA contractor/guide pages | "Most Puget Sound homes" ducted heat pump | $12,000-$18,000 | [S?] candidates https://varsityheating.com/blog/heat-pump-cost-washington/ ; https://heatpumpwa.com/blog/cost-of-heat-pump-in-washington-state/ |
| National 2026 guides | Average heat-pump install about $15,400; about $16,500 "after incentives" | Low confidence | [S?] candidates https://www.energysage.com/heat-pumps/costs-and-benefits-air-source-heat-pumps/ ; https://heatpumpcostcalculator.com/cost-by-state/washington |
| **Barron Heating (Bellingham)** | Air-source (ducted) | **$4,000-$8,000**; "most homeowners" $4,000-$10,000; geothermal $15,000-$35,000 | [S] https://www.barronheating.com/blog/2025/june/heat-pump-installation-cost-in-bellingham-wa/ |
| **Clean Air (Bellingham)** | Heat pump installs, NW Washington | **$8,000-$18,000+** | [S] https://callcleanair.com/hvac-services/heat-pump-installation/ |

Reading the bands:
- Barron's $4,000-$8,000 for ducted air-source is well below the WA average ($15,500) and the Clean Air band. It probably assumes a replacement on existing ducts.
- For **new construction with new ducts**, bid against the upper local bands (Clean Air) plus a separate duct line (1c.3). [D]

#### 1c.3 New-construction HVAC $/sf and ductwork

| Source | Metric | Value | URL |
|---|---|---|---|
| HomeGuide (2026) | HVAC for **new construction** | **$1.75-$2.50 per sf**, depending on system size and type | [S] https://homeguide.com/costs/hvac-cost |
| HomeGuide (2026) | New ductwork, added to system cost | **$2,000-$5,000** | [S] https://homeguide.com/costs/hvac-cost |
| HomeGuide (2026) | Ductwork install/replace (crawl, attic, basement) | **$25-$55 per LF**, or **$270-$500 per duct** | [S] https://homeguide.com/costs/cost-to-replace-ductwork |
| HomeGuide (2026) | Adding ducts to homes without them | $40-$65 per LF | [S] https://homeguide.com/costs/cost-to-replace-ductwork |
| HomeGuide (2026) | Ductwork insulation | $3-$13 per sf installed | [S] https://homeguide.com/costs/air-source-heat-pump-cost |
| Fixr | New ductwork for an average **2,500 sf home, 275 LF** of duct | **$1,436-$16,211** | [S] https://www.fixr.com/costs/ductwork |
| Fixr | Galvanized sheet-metal duct, retrofit | $19.51-$62.36 per LF | [S] https://www.fixr.com/costs/ductwork |
| Fixr | Central unit + install $5,050-$10,700; new ductwork $3,600-$9,500 (labour + material) | Band | [S?] https://www.fixr.com/costs/central-air-conditioner-installation |
| 2026 guides | "2,000 sf home, new HVAC system" | $9,000-$18,000 installed | [S?] candidates https://www.budgetheating.com/understanding-the-cost-of-a-new-hvac-system-guid/ ; https://buseheatandair.com/blog/new-hvac-system-cost/ ; https://costtobuildahouse.com/blog/articles/new-construction-hvac-cost |

Derived [D]:
- **Duct density.** Fixr's 275 LF per 2,500 sf is about **0.11 LF of duct per sf of house**. Use it as a takeoff sanity ratio.
- **Duct cost at HomeGuide rates.** 275 LF × $25-$55 = $6,875-$15,125. These are retrofit-leaning rates; new-construction duct labour should come in lower.
- **HomeGuide $/sf applied to 2,000-3,000 sf.** $1.75-$2.50/sf gives $3,500-$7,500, or **$5,500-$12,500** once the $2,000-$5,000 ductwork adder is included.
- **Conflict.** This band sits below the WA ducted-heat-pump average ($15,500) and the Clean Air band. For NW WA cold-climate heat-pump new construction, treat HomeGuide's $/sf as a **floor**, not typical.

### 1d. ERV / HRV units

#### 1d.1 Equipment street price

| Unit | Airflow / notes | Street price | Source |
|---|---|---|---|
| **Panasonic FV-10VEC2** Intelli-Balance 100 ERV (plug-in, cold climate) | 30-100 cfm | **$1,036.99** (Home Depot); $1,132.31 (Conservation Mart) | [S] https://www.homedepot.com/p/Panasonic-Intelli-Balance-100-Energy-Recovery-Ventilator-ERV-30-100-CFM-Standard-Plug-In-Cold-Climate-FV-10VEC2/332397326 ; https://www.conservationmart.com/panasonic-100-cfm-cold-climate-intelli-balance-erv-fv-10vec2/ |
| Panasonic FV-10VEC2 variants (R = mirror, H = hardwired, RH) | same | PTS | pages: https://www.supplyhouse.com/Panasonic-FV-10VEC2R-Panasonic-Intelli-Balance-100-Energy-Recovery-Ventilator-ERV-30-100-CFM-Standard-Plug-In-Any-Climate-Mirror-Model-FV-10VEC2R ; https://www.homedepot.com/p/Panasonic-Intelli-Balance-100-Energy-Recovery-Ventilator-ERV-30-100-CFM-Hardwired-Any-Climate-FV-10VEC2H/332397327 |
| **Broan AI Series B160E65RT** ERV (top ports, 67% efficiency) | 160 cfm class | **$1,141.00** | [S?] candidates https://www.conservationmart.com/broan-ai-series-160-cfm-energy-recovery-ventilator-erv-top-port-b160e65rt/ ; https://www.supplyhouse.com/Broan-B160E65RT-160-CFM-AI-Series-Energy-Recovery-Ventilator-w-Top-Ports-67-Efficiency |
| Broan B130E65RT / B210E65RT / B160E65RS | 130 / 210 cfm; side ports | PTS | pages: https://broan-nutone.com/en-us/product/freshairsystems/b130e65rt ; https://www.supplyhouse.com/Broan-B160E65RS-160-CFM-AI-Series-Energy-Recovery-Ventilator-w-Side-Ports-67-Efficiency |
| **RenewAire EV Premium S** | up to 130 cfm | **$1,170.00** sale (regular $1,558.00) | [S?] candidates https://ervdirect.com/products/ev-premium-s ; https://www.positive-energy.com/product/renewaire-premium-s-erv/ |
| **RenewAire EV Premium M** | 30-230 cfm | **$1,415.00** sale (regular $1,886.00) | [S?] candidates https://ervdirect.com/products/ev-premium-m ; https://www.positive-energy.com/product/ev-premium-m-renewaire-erv/ ; airflow: https://renewaire.com/product/ev-premium-m/ |
| **Zehnder ComfoAir Q350** ERV | up to about 208 cfm (about 4 bed / 3.5 bath); kit sized for 1,600-2,300 sf | **Unit price not published in extracts (PTS)**. Pre-heater option **+$262.00**. | [S] https://zehnroom.com/shop/erv-kits-2/comfoair-q350-erv-unit-with-optional-pre-heater ; https://www.zehnroom.com/q350/zehnder-comfoair-q350-complete-erv-kit ; https://mainstreamcorporation.com/index.php?option=com_eshop&view=product&id=174&catid=2&Itemid=314 |
| Zehnder ComfoAir 200 (CA200) ERV kit | max 118 cfm; 84% (PHI); kit for 1,000-1,600 sf | PTS | [S] https://zehnroom.com/ca200 |
| **Lunos e2** decentralised HRV, **pair** | about 22 cfm per pair (continuous) | Historic **$1,055 per pair** (2017-18 references). 2025: US pair with controller "just over $1,000" base; **kits $1,500-$2,000** with options (covers, filters); Canada $1,400-$2,000 CAD. | [S?] https://www.buildwithrise.com/stories/best-ductless-ervs-hrvs-2025 ; https://www.greenbuildingadvisor.com/question/lunos-e2-ductless-hrv-system-vs-ducted-system ; product page: https://475.supply/products/lunos-e-kit |

#### 1d.2 Installed ERV/HRV

| Source | Band | URL |
|---|---|---|
| HomeGuide (2026) | **ERV $1,500-$2,500 installed; HRV $1,300-$2,200 installed** | [S?] https://homeguide.com/costs/hvac-cost |
| Angi / This Old House / Fixr (extracts) | ERV unit $800-$1,500 + installation $1,000-$2,000; "$2,000 or more" for professional install; "budget $2,000-$3,000"; a separate estimate of $500-$1,700 for "energy recovery ventilation installation" | [S?] https://www.angi.com/articles/energy-recovery-ventilator-erv-system-scores-high-marks.htm ; https://www.fixr.com/costs/ventilation-installation ; https://www.thisoldhouse.com/heating-cooling/21016174/how-an-energy-recovery-ventilator-erv-works |
| GreenBuildingAdvisor forum (2021 thread) | **Complete Zehnder system quotes about $9,100-$9,200 including commissioning**; commissioning quoted at $550; Zehnder ducting about $3,000-$3,500; Panasonic 200 cfm Intelli-Balance "around $2,500" | [S?] https://www.greenbuildingadvisor.com/question/zehnder-erv-quote ; https://www.greenbuildingadvisor.com/question/zehnder-price-shock-best-bang-for-buck-alternative |

### 1e. Continuous bath fans for whole-house ventilation, controls, make-up air, dryer

| Item | Price | Source |
|---|---|---|
| **Panasonic WhisperGreen Select FV-0511VKS3**, dual-speed 30-110 cfm, Flex-Z bracket, 4/6 in adapter (the dual-speed model suits continuous low plus boost) | **$213.99** (Home Depot and SupplyHouse) | [S] https://www.homedepot.com/p/Panasonic-WhisperGreen-Select-Pick-A-Flow-30-to-110-CFM-Bathroom-Exhaust-Fan-Flex-Z-Fast-Bracket-4-or-6-in-Duct-Adapter-FV-0511VKS3/331412123 ; https://www.supplyhouse.com/Panasonic-FV-0511VKS3-Panasonic-WhisperGreen-Select-Dual-Speed-Ceiling-Mount-Exhaust-Fan-Customizable-30-to-110-CFM-FV-0511VKS3 |
| Panasonic FV-0511VK3, single-speed 50/80/110 cfm | **$192.99** (Home Depot and SupplyHouse) | [S] https://www.homedepot.com/p/Panasonic-WhisperGreen-Select-Pick-A-Flow-50-80-or-110-CFM-Bathroom-Exhaust-Fan-Flex-Z-Fast-bracket-dual-4-or-6-in-Duct-Adapter-FV-0511VK3/331412121 |
| Panasonic FV-0511VKS3S, dual-speed with designer grille | $232.99 | [S] https://www.homedepot.com/p/Panasonic-WhisperGreen-Select-Pick-A-Flow-30-to-110-CFM-Bathroom-Exhaust-Fan-Flex-ZFast-Bracket-4-6-in-Duct-Adapter-FV-0511VKS3S/331414384 |
| Panasonic FV-0511VQ1 WhisperCeiling DC (named in brief; it is WhisperCeiling, not WhisperGreen) | PTS | page: https://www.homedepot.com/p/Panasonic-WhisperCeiling-DC-Fan-with-Pick-A-Flow-Speed-Selector-50-80-or-110-CFM-and-Flex-Z-Fast-Installation-Bracket-FV-0511VQ1/303619101 |
| AirCycler SmartExhaust bath fan/light ASHRAE 62.2 timer switch | **$98.60** (toggle); $103.63 (rocker). AirCycler's own site says "contractors contact us for pricing". | [S?] https://www.conservationmart.com/aircycler-smart-exhaust-bathroom-fan-light-timer-switch/ ; https://www.conservationmart.com/p-2917-aircycler-smartexhaust-decorarocker-bath-fan-timer-switch.aspx ; [S] https://www.aircycler.com/products/smartexhaust |
| Tamarack Airetrak 1A Advantage (TTi-ATRAKAV) programmable duty-cycle fan control | PTS (Amazon listing unavailable) | page: https://www.supplyhouse.com/Tamarack-TTI-ATRAKAV-Airetrak-1A-Advantage-Bath-Fan-Control |
| Lutron Maestro MA-T51 countdown timer | PTS | page: https://www.homedepot.com/p/Lutron-Maestro-Digital-Timer-Switch-5-Amp-Fan-600-Watt-Incandescent-Bulbs-White-MA-T51-WH-MA-T51-WH/100652547 |
| **Broan MD6T** 6 in make-up-air damper | **Discontinued 2023-08-05**. Replacement MD6TU (6 in, with pressure-sensor kit) **$269.00**. | [S?] https://www.supplyhouse.com/Broan-MD6T-6-Automatic-Make-Up-Air-Damper-Direct-Wired ; https://www.supplyhouse.com/Broan-MD6TU-6-Automatic-Make-Up-Air-Damper-w-Pressure-Sensor-Kit |
| Fantech make-up-air damper kit (damper + pressure switch + 20 VA transformer) | **from $144.99** | [S] https://www.hvacquick.com/products/residential/Makeup-Air/Residential-Makeup-Air-Fans |
| Fantech MUAS unitary make-up-air system (2 Ruck fans, damper, MERV-13 box, controls) | from $2,190.30 | [S] https://www.hvacquick.com/products/residential/Makeup-Air/Residential-Makeup-Air-Fans/Fantech-MUAS-Unitary-Residential-Makeup-Air-Systems |
| AirScape make-up-air damper | PTS | n/a |
| **Dryerbox 425** recessed dryer vent box (2x6 wall) | **$45.97** (Home Depot, model 425THD); about $36 on eBay | [S] https://www.homedepot.com/p/DRYERBOX-4-25-in-Dryer-Box-Metal-Recess-425THD/313741358 ; https://www.ebay.com/itm/186237943133 |
| Fantech DBF 4XLT dryer booster kit (170 cfm fan, supports up to 130 ft of dryer duct) | $144-$397 across retailers (spread is wide; verify) | [S?] https://www.acwholesalers.com/Fantech-DBF4XLT/p31290.html ; https://www.hvacquick.com/products/residential/Dryer-boosting/dryer-booster-fans/fantech-dryer-boosters |

### 1f. Thermostats and controls

| Item | Price | Source |
|---|---|---|
| Mitsubishi kumo cloud Wi-Fi adapter **PAC-USWHS002-WF-2** (CN105 pass-through lets MHK2 and the adapter work together) | **$189.00** (AC Wholesalers; OnlineSupply shows "special $189, originally $428") | [S] https://www.acwholesalers.com/Mitsubishi-HVAC-PAC-USWHS002-WF-2/p102719.html ; https://onlinesupply.com/mitsubishi-kumo-cloud-wi-fi-adapter-pac-uswhs002-wf-2.html |
| Mitsubishi **MHK2** wireless wall controller kit | **$415.00** (AC Wholesalers); $414.75 (OnlineSupply, "originally $521.75") | [S?] https://onlinesupply.com/hvac-supply/thermostats/filter/mitsubishi.html ; https://www.acwholesalers.com/cooling/mitsubishi-ductless-mini-split-controls.html |
| Mitsubishi Kumo Touch PAR-CT01MAU-SB | PTS | page: https://www.amazon.com/Mitsubishi-PAR-CT01MAU-SB-Touch-Remote-Controller/dp/B07VPCSNHL |
| Note: new R-454B Mitsubishi equipment "includes Wi-Fi". Confirm whether FX/GX need the adapter before adding it by default. | n/a | [S] https://goendlessenergy.com/blog/hvac/comparing-mitsubishi-410a-models-to-454b-models/ |
| **ecobee Smart Thermostat Premium** | **$249-$250** (MSRP $249); August 2026 street $249-$299 | [S] https://www.ecobee.com/en-us/smart-thermostats/smart-thermostat-premium/ ; [S?] https://www.smarthomeexplorer.com/guides/ecobee-smart-thermostat-premium-price-2026 |
| ecobee Smart Thermostat Enhanced | **$190** | [S?] https://smarthomedock.com/ecobee-smart-thermostat-premium-enhanced-review/ |
| Honeywell T6 Pro TH6220U2000 (2H/1C heat pump) | PTS | page: https://www.supplyhouse.com/Honeywell-Home-TH6220U2000-T6-Pro-Programmable-Thermostat-2H-1C-Heat-Pump-2H-2C-Conventional |
| Honeywell T6 Pro Wi-Fi TH6220WF2006 | PTS | page: https://www.supplyhouse.com/Honeywell-Home-Resideo-TH6220WF2006-T6-Pro-Smart-Wi-Fi-Programmable-Thermostat-2H-2C |

---

## 2. Distribution material prices

### 2.1 Refrigerant line sets (sourced)

| Line set | Length | Price | Derived $/ft | Source |
|---|---|---|---|---|
| VEVOR 1/4 x 1/2 in, triple-layer insulation (12k-18k) | 25 ft | **$94.40** | $3.78 [D] | [S] https://www.homedepot.com/p/VEVOR-25-ft-Mini-Split-Line-Set-1-4-in-and-1-2-in-O-D-Copper-Pipes-Tubing-and-Triple-Layer-Insulation-for-Air-Conditioning-KDLJTG25FT141DPZLV0/330128279 |
| SKYSHALO 1/4 x 1/2 in, triple insulated | 25 ft | **$113.01** (after a $25 promo) | $4.52 [D] | [S] https://www.homedepot.com/p/SKYSHALO-25-ft-HVAC-Mini-Split-Line-Set-Triple-Insulated-1-4-in-and-1-2-in-Copper-Pipes-with-Wrapping-Strips-Included-KDLJTG25FT141DPZLV0-250612/336898130 |
| VEVOR 1/4 x 3/8 in | 50 ft | **$115.26** (after $25 off) | $2.31 [D] | [S] https://www.homedepot.com/p/VEVOR-50-ft-Mini-Split-Line-Set-1-4-in-3-8-in-O-D-Copper-Pipes-Tubing-and-Triple-Layer-Insulation-for-Air-Conditioning-KDLJTG50FT140P486V0/330127581 |
| MRCOOL MC50-1438 1/4 x 3/8 in flared **kit** (with communication wire, wall sleeve, drain hose) | 50 ft | **$308.00** | $6.16 incl. accessories [D] | [S] https://www.homedepot.com/p/MRCOOL-50-ft-1-4-in-x-3-8-in-Flared-Line-Set-Kit-with-Communication-Wire-Wall-Sleeve-and-Drain-Hose-MC50-1438/312540656 |
| Home Depot 50-ft insulated mini-split line sets (various, extract summary) | 50 ft | $135-$220 | $2.70-$4.40 [D] | [S?] https://www.homedepot.com/b/Heating-Venting-Cooling-Mini-Split-Air-Conditioners-Mini-Split-Parts/Mini-Split-Line-Sets/N-5yc1vZ1z18ggrZ1z19b6r |
| MRCOOL No-Vac **pre-charged quick-connect** 3/8 x 3/4 in, R-454B (DIY product, out of stock; not representative of pro flare/braze sets) | 25 ft | $418.26 | $16.73 [D] | [S] https://www.lowes.com/pd/MRCOOL-No-Vac-25ft-3-8-x-3-4-R454B-Line-set-0-75-in-W-x-0-375-in-H-Central-Air-conditioner-line-set/5016255613 |
| MRCOOL No-Vac 3/8 x 3/4 in, R-454B | 50 ft | $686.38 | $13.73 [D] | [S] https://www.lowes.com/pd/MRCOOL-No-Vac-50ft-3-8-x-3-4-R454B-Line-set-0-75-in-W-x-0-375-in-H-Central-Air-conditioner-line-set/5016255593 |
| HomeGuide installed adder: "refrigerant line sets for longer runs" | per ft | **$15-$25 per ft** (installed) | n/a | [S] https://homeguide.com/costs/air-source-heat-pump-cost |

**Line sets found but not priced (PTS).** Pro-grade SKUs to price at SupplyHouse or a distributor:

| Size | Length | SKU / page |
|---|---|---|
| 1/4 x 3/8 flared, both lines insulated | 25 ft | Hessaire 12000/25L: https://www.homedepot.com/p/Hessaire-1-4-in-x-3-8-in-x-25-ft-Line-set-for-12000-BTU-Mini-split-12000-25L/310499530 |
| 1/4 x 3/8 flared | 50 ft | JMF LS143850F: https://www.supplyhouse.com/Generic-LS143850F-1-4-LL-x-3-8-SL-x-50-ft-Refrigerant-Line-Set-Flare-Ends-12675000-p ; ICOOL B143812050F (1/2 in insulation): https://www.supplyhouse.com/ICOOL-B143812050F-1-4-LL-x-3-8-SL-Mini-Split-Refrigerant-Line-Set-w-Flare-Nuts-1-2-Insulation-50-Ft |
| 1/4 x 1/2 flared | 25 ft | JMF LS141225F: https://www.supplyhouse.com/Generic-LS141225F-1-4-LL-x-1-2-SL-x-25-ft-Refrigerant-Line-Set-Flare-Ends-12677000-p ; ICOOL B141238025F: https://www.supplyhouse.com/ICOOL-B141238025F-1-4-LL-x-1-2-SL-Mini-Split-Refrigerant-Line-Set-w-Flare-Nuts-3-8-Insulation-25-Ft ; Hessaire 18000/25L: https://www.homedepot.com/p/Hessaire-1-4-in-x-1-2-in-x-25-ft-Line-set-for-18000-BTU-Mini-split-18000-25L/310500980 |
| 1/4 x 1/2 flared, with wire | 50 ft | JMF 408-50-12-144EZ-A (EZ-pull insulation plus EZ-IN wire): https://www.supplyhouse.com/JMF-408-50-12-144EZ-A-1-4-LL-x-1-2-SL-x-1-2-Mini-Split-Line-Set-w-Flare-Nuts-EZ-Pull-Insulation-EZ-IN-Wire-50-Ft |
| 3/8 x 5/8 flared | 25 ft | JMF LS385825F: https://www.supplyhouse.com/Generic-LS385825F-3-8-LL-x-5-8-SL-x-25-ft-Refrigerant-Line-Set-Flare-Ends-12685000-p ; Hessaire 24000/25L: https://www.homedepot.com/p/Hessaire-3-8-in-x-5-8-in-x-25-ft-Line-set-for-24000-BTU-Mini-split-24000-25L/310499568 |
| 3/8 x 5/8 flared | 50 ft | ICOOL B385812050F: https://www.supplyhouse.com/ICOOL-B385812050F-3-8-LL-x-5-8-SL-Mini-Split-Refrigerant-Line-Set-w-Flare-Nuts-1-2-Insulation-50-Ft ; VEVOR: https://www.homedepot.com/p/VEVOR-50-ft-Mini-Split-Line-Set-3-8-in-and-5-8-in-O-D-Copper-Pipes-Tubing-and-Triple-Layer-Insulation-for-Air-Conditioning-KDLJTG50FT386YXZYV0/330127061 ; JMF LS385850F is **discontinued** [S] https://www.supplyhouse.com/Generic-LS385850F-3-8-LL-x-5-8-SL-x-50-ft-Refrigerant-Line-Set-Flare-Ends-12687000-p |
| 3/8 x 3/4 plain ends (ducted split), 3/8 in insulation on suction | 25 ft | JMF LS383425: https://www.supplyhouse.com/Generic-LS383425-3-8-LL-x-3-4-SL-x-25-ft-Refrigerant-Line-Set-12580000-p |
| 3/8 x 3/4 plain ends | 50 ft | JMF LS383450: https://www.supplyhouse.com/Generic-LS383450-3-8-LL-x-3-4-SL-x-50-ft-Refrigerant-Line-Set-12665000-p ; ICOOL F383438050 (suction-only insulation): https://www.supplyhouse.com/ICOOL-F383438050-3-8-LL-x-3-4-SL-x-50-ft-Refrigerant-Line-Set |

### 2.2 Everything else in the distribution list: PRICE TO SET

None of these were priced before the search budget ran out. There are no numbers here by design. Price them from a trade account (Johnstone, Gensco or Ferguson counter), SupplyHouse.com or Home Depot Pro, and record the date and URL.

| # | Item | Catalog unit | Spec notes for the catalog | Status |
|---|---|---|---|---|
| 1 | Line-hide cover (Slimduct SD 75/100, Fortress LineHide) | per 8-ft length | 3 in / 4 in width, paintable | PTS |
| 2 | Line-hide fittings: wall inlet, 90° elbow, flexible elbow, coupling, end cap | EA | match series | PTS |
| 3 | Wall sleeve / penetration sleeve | EA | 2.5-3.5 in, with sealing cap | PTS |
| 4 | Condensate drain hose / vinyl tube | per ft | 5/8 in ID typical for heads | PTS |
| 5 | Condensate PVC (3/4 in) and fittings | per 10 ft / EA | interior ducted units, air handlers | PTS |
| 6 | Mini condensate pump, Aspen Mini Orange | EA | wall heads without gravity drain | PTS |
| 7 | Mini condensate pump, Sauermann Si-30 | EA | line-hide-mountable | PTS |
| 8 | 14/4 stranded communication cable | per ft (or 250-ft spool) | Mitsubishi heads need 14 AWG x 4 (verify per install manual) | PTS |
| 9 | Outdoor equipment pad | EA | 16x36, 24x36, 36x36 composite or concrete (HomeGuide installed adder $300-$500 per concrete pad, see 1c) | PTS (material) |
| 10 | Wall bracket (e.g. QuickSling) | EA | for single-zone outdoor units | PTS |
| 11 | Snow stand / riser legs | EA | recommended in snow areas (Whatcom foothills, Mt Baker Hwy) [K] | PTS |
| 12 | Anti-vibration pads / isolators | set of 4 | n/a | PTS |
| 13 | Nitrogen cylinder refill / rental | per fill | pressure test + purge | PTS |
| 14 | Refrigerant R-410A | per lb (25-lb jug) | legacy service only | PTS |
| 15 | Refrigerant R-454B | per lb (cylinder) | Mitsubishi / Bosch / Carrier-family additional charge | PTS |
| 16 | Refrigerant R-32 | per lb | Fujitsu / Daikin additional charge | PTS |
| 17 | Flex duct R-8, 25-ft bag, 4 in | per bag | insulated, vapor jacket | PTS |
| 18 | Flex duct R-8, 25-ft bag, 5 / 6 / 7 / 8 in | per bag | n/a | PTS |
| 19 | Flex duct R-8, 25-ft bag, 10 / 12 / 14 in | per bag | returns / trunks | PTS |
| 20 | Galvanized round pipe, 5-ft joint, 4 / 5 / 6 / 7 / 8 in | per joint | 26-30 ga snap-lock | PTS |
| 21 | Galvanized round pipe, 5-ft joint, 10 / 12 in | per joint | trunk | PTS |
| 22 | Adjustable elbows, 4-8 in | EA | n/a | PTS |
| 23 | Register boots, 2-1/4x10, 4x10, 4x12, 6x10 (4 / 6 in collar) | EA | straight and 90° | PTS |
| 24 | Takeoffs / starting collars with damper, 5 / 6 / 7 / 8 in | EA | n/a | PTS |
| 25 | Floor/wall/ceiling registers, 2x10, 4x10, 4x12, 6x10 | EA | steel stamped vs wood (finish-grade allowance) | PTS |
| 26 | Return filter grille, 20x25 (also 14x25, 20x20) | EA | 1 in filter | PTS |
| 27 | Supply / return plenums | EA (fabricated) | sized to air-handler footprint | PTS |
| 28 | Duct mastic | per gal | UL 181 | PTS |
| 29 | Foil tape UL 181A/B | per roll | n/a | PTS |
| 30 | Hanger strap, 100-ft roll; draw bands / zip ties | per roll / EA | n/a | PTS |
| 31 | Duct board, 1 in / 1.5 in, 4x10 sheet | per sheet | n/a | PTS |
| 32 | Roof jack / roof cap, 4 / 6 / 8 in with damper | EA | bath fan, range hood, ERV | PTS |
| 33 | Wall cap / hood, 4 / 6 / 8 in with damper and screen | EA | bath fan, dryer, range hood, ERV | PTS |
| 34 | Dryer vent kit (4 in rigid, elbows, wall cap) | kit | Dryerbox priced in 1e | PTS |
| 35 | ERV ducting, 5-6 in insulated flex (R-6/R-8), 25-ft bag | per bag | fresh-air and exhaust-to-outdoors legs must be insulated | PTS |
| 36 | ERV exterior intake/exhaust hoods (tandem or two-hood) | EA | brand-matched (Broan/Panasonic/RenewAire) | PTS |
| 37 | Lunos e2 exterior cover (spare) | EA | page: https://475.supply/products/lunos-additional-exterior-cover | PTS |
| 38 | Range hood duct, 6 / 8 in rigid, per 5 ft, plus elbows | per joint | code requires rigid duct for hoods [K] | PTS |
| 39 | Electrical whips, disconnects, surge protection (if not "by electrician") | EA | usually by electrical sub (section 5) | PTS |

---

## 3. Labour (installer-hours, crew, per-task units)

### 3.1 Sourced duration and labour-cost figures

| Task / scope | Figure | Source |
|---|---|---|
| Heat pump / mini-split installation, standard | **3-8 hours**; complex systems **2+ days** | [S] https://homeguide.com/costs/ductless-mini-split-ac-cost ; https://homeguide.com/costs/air-source-heat-pump-cost |
| Ductless system (Bellingham contractor blog) | "may only take a day to install" | [S?] https://www.barronheating.com/blog/2025/june/heat-pump-installation-cost-in-bellingham-wa/ |
| Mini-split labour cost (national) | $1,000-$5,000 per job | [S] https://homeguide.com/costs/ductless-mini-split-ac-cost |
| Mini-split labour cost (national) | Single-zone $300-$2,000; multi-zone $700-$3,000 | [S] https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac.htm |
| Mini-split labour share, Seattle | **40-65% of installed cost** | [S] https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/wa/seattle |
| Mini-split labour per zone (national, aggregator) | $500-$2,000 per zone | [S?] https://hvacprojectcost.com/mini-split-installation-cost/ ; https://realcostiq.com/guides/mini-split-installation-cost/ |
| Survey of split-AC buyers | "72% paid $150 per hour in labor or more" | [S?] https://www.thisoldhouse.com/heating-cooling/split-ac-installation-cost |
| Dedicated electrical circuit for a mini-split (electrician) | about **$250** extra; electrician $50-$100/h | [S] https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac.htm |
| Ductwork quantity benchmark | **275 LF** for an average 2,500 sf home | [S] https://www.fixr.com/costs/ductwork |
| Ductwork, installed per run | $270-$500 per duct (install/replace) | [S] https://homeguide.com/costs/cost-to-replace-ductwork |
| Zehnder ERV commissioning (quote) | $550 | [S?] https://www.greenbuildingadvisor.com/question/zehnder-erv-quote |

### 3.2 Derived labour benchmarks [D]
- **Single-zone mini-split, Seattle-market billed hours:** about **5.1-15.5 h** on the average job; the full range is 3.4-25.8 h. Method in 1a.3. Inputs: https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/wa/seattle
- **Duct run count sanity check:**
  - At $270-$500 per run, a $2,000-$5,000 new-construction ductwork adder (HomeGuide) covers roughly 4-18 runs.
  - That is far fewer than a ducted 2,500 sf house needs (275 LF of duct per Fixr).
  - Read the HomeGuide "adds $2,000-$5,000" as an **incremental** cost for new construction, not a full duct system price.
  - Inputs: https://homeguide.com/costs/cost-to-replace-ductwork ; https://homeguide.com/costs/hvac-cost ; https://www.fixr.com/costs/ductwork

### 3.3 Task-level labour units requested: PTS

No RSMeans, Craftsman National Estimator, manufacturer install-guide or contractor-article **hour values** were captured. RSMeans and Craftsman are paywalled; manufacturer manuals were not reachable. Every row below needs a value.

| Task | Unit | Value | Where to get it |
|---|---|---|---|
| Set ductless outdoor unit (pad or wall bracket) | h/EA | PTS | RSMeans Residential Cost Data, ductless split lines; Craftsman "National Plumbing & HVAC Estimator" |
| Set indoor wall head (bracket, core-drill, connect) | h/EA | PTS | same |
| Set ceiling cassette / slim ducted indoor unit | h/EA | PTS | same |
| Line set run, installed (by size) | h/LF | PTS | same |
| Condensate (gravity or pump) | h/EA | PTS | same |
| Pressure test, evacuation, charge adjust, commissioning | h/system | PTS | Mitsubishi / Fujitsu install manuals (evacuation to 500 microns, standing test) [K] |
| Ducted rough-in, 2,000-3,000 sf, 2-storey | crew-days | PTS | local sub interview; RSMeans duct lines |
| Air handler set (incl. strip heat, drain pan) | h/EA | PTS | same |
| Supply run (boot + flex/pipe + takeoff) | h/EA | PTS | same |
| Return run / filter grille | h/EA | PTS | same |
| Plenum fabrication and install | h/EA | PTS | same |
| ERV install (unit, 4 duct legs, controls) | h/EA | PTS | Panasonic/Broan install manuals; local sub |
| Bath fan duct + roof/wall cap | h/EA | PTS | same |
| Dryer vent (box, rigid run, cap) | h/EA | PTS | same |
| Range hood duct + cap (+ MUA damper) | h/EA | PTS | same |
| Duct leakage test (third party) | $/test | PTS | local testing agencies / WSEC-R testers |
| Whole-house ventilation flow test | $/test | PTS | same |
| Start-up / owner training | h/system | PTS | n/a |
| Crew norm (installer + helper, or 2-person crew) | n/a | PTS ([K]: a 2-person crew is typical for ducted rough-in) | local sub interview |
| Island (San Juan) mobilisation: ferry, travel time | $/trip | PTS | local sub interview |

---

## 4. Wages and billing

### 4.1 Wages (BLS OEWS, WA L&I prevailing wage): PTS

Not captured. bls.gov and lni.wa.gov were egress-blocked and the search budget was exhausted. Where to get them:

| Figure needed | Where | Status |
|---|---|---|
| HVAC mechanics and installers (SOC 49-9021): mean, median, 10th/25th/75th/90th percentile hourly wage, **Bellingham, WA MSA** | BLS OEWS metro table, e.g. https://www.bls.gov/oes/current/oes_13380.htm (MSA code 13380 [K]; URL not opened) | PTS |
| Same, Mount Vernon-Anacortes MSA (Skagit) | BLS OEWS metro table (MSA code 34580 [K]) | PTS |
| Same, Washington statewide | BLS OEWS state table (WA) | PTS |
| HVAC apprentice wage | WA L&I apprenticeship wage progression / program standards | PTS |
| Prevailing wage, **Whatcom / Skagit / San Juan**: trades "Refrigeration & Air Conditioning Mechanics", "Heating Equipment Mechanics", "Sheet Metal Workers" (residential rates where published) [K] | WA L&I prevailing wage lookup: https://lni.wa.gov/licensing-permits/public-works-projects/prevailing-wage-rates/ (URL not opened) | PTS |

### 4.2 Billed hourly rates and call fees

| Source | Rate | URL |
|---|---|---|
| HomeGuide (2026), HVAC repair labour | **$75-$150/h** regular; **$160-$250/h** emergency, night or holiday; service-call minimum **$75-$200** (usually credited to the bill) | [S] https://homeguide.com/costs/hvac-repair-cost |
| HomeGuide (2026), heat-pump installation labour | **$80-$200+/h** | [S] https://homeguide.com/costs/air-source-heat-pump-cost |
| **Angi, Seattle WA** | **$140-$260/h** | [S] https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/wa/seattle |
| Angi, other metros (for scale) | Los Angeles $100-$225/h; Phoenix $90-$180/h; Tampa $75-$160/h; St. Louis $60-$140/h | [S] https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/ca/los-angeles ; https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/az/phoenix ; https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/fl/tampa ; https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/mo/st-louis |
| HVAC diagnostic fee guide (2026) | $89-$200 per diagnostic visit | [S] https://hvaccalculatorhub.com/blog/hvac-diagnostic-fee-guide-2026 |
| Service-call guide | $75-$200 business hours; $200-$500 after hours | [S?] https://www.essentrahvac.com/post/what-is-the-average-cost-of-an-hvac-service-call |
| Bellingham contractors' own rates (Feller Heating "flat rate"; Clean Air; Barron) | **PTS**: not published in extracts | https://www.fellerheating.com/service-repair/ ; https://callcleanair.com/ ; https://www.barronheating.com/ |

### 4.3 HVAC sub pricing norms (per sf, per ton, per head, per system)

| Metric | Value | Source |
|---|---|---|
| **$ per sf, new construction HVAC** | **$1.75-$2.50/sf** (national; likely low for cold-climate heat pump in WA, see 1c.3) | [S] https://homeguide.com/costs/hvac-cost |
| **$ per head (wall-mounted zone), installed** | **$2,500-$5,000 per zone**; floor units $3,000-$5,000 | [S] https://homeguide.com/costs/ductless-mini-split-ac-cost |
| Single-zone mini-split, Seattle average | **$3,333** (range $2,222-$5,555) | [S] https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/wa/seattle |
| Multi-zone mini-split | $6,500-$15,000+ (national) | [S] https://homeguide.com/costs/ductless-mini-split-ac-cost |
| 4-zone ductless | $8,500-$10,000 | [S?] https://modernize.com/hvac/heating-repair-installation/heat-pump/ductless |
| **$ per ton, installed** | 3-ton heat pump $3,900-$6,200 incl. labour, i.e. about **$1,300-$2,067/ton** [D] | [S?] https://homeguide.com/costs/heat-pump-cost ; https://www.hvacbase.org/heat-pump-cost-to-install |
| $ per ton, equipment only (street), from section 1 | Single-zone hyper-heat about $2,800-$3,750/ton; multi-zone outdoor about $1,700-$2,330/ton; ducted Mitsubishi P-series about $2,670-$3,970/ton | [D] from 1a.1, 1b.1 and 1c.1 URLs |
| Ducted heat pump, WA average (installed, 2026) | $15,500 | [S] https://heatpumpcostbystate.com/states/washington |
| Ducted heat pump, "most Puget Sound homes" | $12,000-$18,000 | [S?] https://varsityheating.com/blog/heat-pump-cost-washington/ |
| Heat pump installs, NW WA (local contractor) | $8,000-$18,000+ | [S] https://callcleanair.com/hvac-services/heat-pump-installation/ |
| Heat pump, Bellingham, all types (88 projects) | average $5,301-$6,973 | [S] https://www.homeyou.com/wa/heat-pump-bellingham-costs |
| Daikin FIT installed | $6,500-$16,500 | [S] https://hvacprojectcost.com/daikin-fit-cost/ |
| ERV installed | $1,500-$2,500 (HRV $1,300-$2,200) | [S?] https://homeguide.com/costs/hvac-cost |

**Worked new-construction envelope, 2,000-3,000 sf, 2 storeys [D]:**
- Ducted heat pump, low: HomeGuide $/sf plus the duct adder gives **$5,500-$12,500**. Inputs: https://homeguide.com/costs/hvac-cost
- Ducted heat pump, WA-market check: WA average $15,500 (https://heatpumpcostbystate.com/states/washington) and Clean Air $8,000-$18,000+ (https://callcleanair.com/hvac-services/heat-pump-installation/).
- **Suggested bid band to validate with local subs: about $12,000-$20,000**, before ventilation and exhaust scope. [D] This is a judgement span over the two sources above, not a quote.
- All-ductless, 4-6 heads: HomeGuide per-zone $2,500-$5,000 × 4-6 = **$10,000-$30,000**. Inputs: https://homeguide.com/costs/ductless-mini-split-ac-cost
- ERV added: HomeGuide $1,500-$2,500 (https://homeguide.com/costs/hvac-cost). A Zehnder-class system can reach about $9,000+ (https://www.greenbuildingadvisor.com/question/zehnder-erv-quote).

---

## 5. What a typical new-construction HVAC bid includes vs excludes

Evidence is thin because the search budget ran out. Each row says whether it rests on a source [S], an inference [D], or is general practice to verify [K]. Use it as the engine's default scope checklist and confirm it against 2-3 real Whatcom/Skagit sub bids.

| Scope line | Default treatment in a sub's NC bid | Evidence / cost hook | Tag |
|---|---|---|---|
| Mechanical permit | Usually **included by the HVAC sub** or carried as an allowance. Permitting and inspections in Bellingham/Whatcom add to cost. | Barron: "permitting and inspection requirements from Bellingham and Whatcom County can also add to the expense": https://www.barronheating.com/blog/2025/june/heat-pump-installation-cost-in-bellingham-wa/ ; published installed ranges often **exclude** permits (with ducts and panel, +$1,500-$5,000+): https://hvacprojectcost.com/daikin-fit-cost/ | [S] |
| Line-voltage electrical (dedicated circuit, disconnect, whip) | **Excluded; by electrical contractor** | A mini-split may need an electrician at $50-$100/h and a dedicated circuit at about $250: https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac.htm | [S] |
| Low-voltage control wiring (thermostat, 14/4 communication) | Included (HVAC) | n/a | [K] |
| Line-set penetrations, sleeves, sealing | Included (HVAC); framing/siding patch excluded | n/a | [K] |
| Line sets beyond a stated length | Included to a stated length (e.g. 15-25 ft per head), then **adder per ft** | Long-run line sets $15-$25/ft installed: https://homeguide.com/costs/air-source-heat-pump-cost | [S] adder / [K] allowance length |
| Line-hide exterior covers | Included, or an option priced per 8-ft piece | n/a | [K] |
| Condensate (gravity to exterior or drain; pumps where needed) | Included; pump as an adder where gravity is impossible | n/a | [K] |
| Equipment pads / wall brackets / snow stands | Included (pad or bracket); snow stand as an adder | Concrete pad $300-$500 installed: https://homeguide.com/costs/air-source-heat-pump-cost | [S] |
| Ductwork, boots, registers, returns, plenums | Included for ducted systems | New-construction ductwork adds $2,000-$5,000: https://homeguide.com/costs/hvac-cost | [S] |
| Duct insulation where outside the conditioned space | Included (or by insulation sub) | $3-$13/sf installed: https://homeguide.com/costs/air-source-heat-pump-cost | [S] |
| Startup, evacuation, charge, commissioning | Included | ERV commissioning quoted $550 (Zehnder): https://www.greenbuildingadvisor.com/question/zehnder-erv-quote | [S?] |
| Duct leakage test (WSEC-R) | Often **by third-party tester**, billed to the builder, or carried as an allowance | PTS (verify current 2021 WSEC-R duct-testing rule at https://sbcc.wa.gov) | [K] |
| Whole-house ventilation system and flow verification (WSEC-R / IRC M1505 as amended) | Included when HVAC-scoped (continuous fan or ERV); flow test by HVAC or third party | PTS (verify at https://sbcc.wa.gov) | [K] |
| Bath fans and ducts to exterior | **Varies**: HVAC sub or electrician sets the fan; HVAC or framer ducts it. State it explicitly. | Fan prices in 1e | [K] |
| Dryer vent (box, rigid run, termination) | Varies (HVAC or plumber/framer); state it explicitly | Dryerbox $45.97: https://www.homedepot.com/p/DRYERBOX-4-25-in-Dryer-Box-Metal-Recess-425THD/313741358 | [S] price / [K] scope |
| Range hood duct and termination; make-up-air damper when required by hood size | Varies; the MUA damper is often an HVAC adder | MD6TU $269: https://www.supplyhouse.com/Broan-MD6TU-6-Automatic-Make-Up-Air-Damper-w-Pressure-Sensor-Kit ; Fantech MUA kit from $144.99: https://www.hvacquick.com/products/residential/Makeup-Air/Residential-Makeup-Air-Fans | [S?] price / [K] scope |
| Thermostats / wall controllers | Included (one per system or zone), with upgrade options | Prices in 1f | [S] price |
| Manual J / S / D design | Often included for ducted NC (or by designer) | PTS | [K] |
| Warranty registration (manufacturer extended warranty) | Included (contractor registers) | PTS | [K] |
| Utility / rebate paperwork | Included where a program exists | Section 7 | [K] |
| Drywall/paint patch, framing blocking, roof flashing of jacks | Excluded (by GC / roofer); roof-jack flashing coordination noted | n/a | [K] |
| Gas piping / venting (if any gas appliance) | Excluded or separate line | n/a | [K] |
| Common allowances | Line-set length per head; number of registers/returns; exterior cover lengths; ERV duct length; permit-fee allowance | Line-set $/ft above | [S]/[K] |

---

## 6. Bellingham / Whatcom HVAC supply houses and dealer channels

**Status:** branch addresses, hours and phone numbers were **not verified** in this pass. Nothing below is an address. Treat every "Bellingham branch" as PTS until someone confirms it from the company's branch locator.

| Supplier | Channel evidence found | Bellingham / NW WA branch | Publishes prices online? | Source |
|---|---|---|---|---|
| **Ferguson** (ferguson.com; Ferguson Home / Build.com retail arms) | Carries Mitsubishi R-454B (e.g. MUZ-FX12NLHZ, MXZ-SM48NLHZ) and Fujitsu R-32 multi-zone (AOUH36KWAH4) | PTS (unverified) | Retail arms (fergusonhome.com / build.com) list system SKUs; trade pricing is account-gated [K] | [S] https://www.ferguson.com/product/mitsubishi-12k-btu---outdoor-ductless-heat-pump---hyper-heating-inverter---r-454b-mmuzfx12nlhz/11534663.html ; https://www.ferguson.com/product/mitsubishi-48k-btu---outdoor-multi-zone-heat-pump---hyper-heating-inverter---r-454b-mmxzsm48nlhz/11534701.html ; https://www.ferguson.com/product/fujitsu-36k-btu-multi-zone-outdoor-heat-pump---r-32-faouh36kwah4/11534515.html ; https://www.fergusonhome.com/mitsubishi-msz-fs12na-muz-fs12nah/s1972126?uid=4686210&searchId=be24fQlkJM |
| **Trane Supply** | Lists Mitsubishi MXZ-SM48NLHZ (Mitsubishi Electric Trane HVAC US channel) | PTS | Account-gated [K] | [S] https://www.tranesupply.com/product/mxzsm48nlhz/01t4w00000NkJ31AAF |
| **Mitsubishi Electric pro portal** (mitsubishipro.com) | Contractor catalog pages (e.g. MUZ-FX12NLHZ-U1, multi-zone outdoor catalog) | n/a | Contractor-facing [K] | [S] https://www.mitsubishipro.com/products/MUZ-FX12NLHZ-U1 ; https://www.mitsubishipro.com/catalog/outdoor/multi-zone |
| Johnstone Supply | Not verified | PTS | Typically trade-account pricing [K] | n/a |
| Gensco | Not verified | PTS | Typically trade-account pricing [K] | n/a |
| United Refrigeration | Not verified | PTS | Typically trade-account pricing [K] | n/a |
| Keller Supply | Not verified (plumbing-focused [K]) | PTS | PTS | n/a |
| Online retailers **with public prices** (used in sections 1-2) | HVACDirect / OnlineSupply, AC Wholesalers, Got Ductless, SupplyStop, Skip the Warehouse, SupplyHouse, Home Depot, Lowe's, Conservation Mart, HVACQuick | n/a | Yes, but some SKUs hide the price: "Prices so low we can't advertise! Add to cart" (MXZ-SM42NLHZ, MXZ-3D30NLHZ at HVACDirect/OnlineSupply) | [S] https://onlinesupply.com/42000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm42nlhz.html ; https://hvacdirect.com/30000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-3d30nlhz.html |
| Distributor web stores that gate prices | Young Supply, Insco show Mitsubishi R-454B SKUs; extracts note "Login for Price" | n/a | No (login) | [S?] https://shop.youngsupply.com/item/mitsubishi-electric-muz-fx12nlhz ; https://www.insco.com/2626285/p/n/mitsubishi-electric-muz-fx12nlhz |
| Manufacturer-direct gating | AirCycler: "CONTRACTORS CONTACT US FOR PRICING"; Got Ductless "Contact Us for Best Price" (PEAD-AA24NL) | n/a | Partly | [S] https://www.aircycler.com/products/smartexhaust ; https://gotductless.com/products/mitsubishi-pead-aa24nl-24-000-btu-horizontal-ducted-indoor-unit |

**Local installers found** (useful for sub quotes and for checking Mitsubishi Diamond / Fujitsu / Daikin dealer status, which was **not verified**):

| Company | Evidence | URL |
|---|---|---|
| Barron Heating, AC, Electrical & Plumbing (Bellingham; also Marysville) | Publishes Bellingham heat-pump cost bands (1a.3, 1c.2) | https://www.barronheating.com/ ; https://www.barronheating.com/service-area/bellingham-wa |
| Clean Air Heating & Cooling (Bellingham / NW WA; Nooksack, Whatcom County pages) | Publishes NW WA cost bands; "480+ 5-star Google reviews" per extract | https://callcleanair.com/ ; https://callcleanair.com/service-locations/whatcom-county-wa/ |
| Feller Heating (Bellingham) | Flat-rate service; rebates and specials page | https://www.fellerheating.com/service-repair/ ; https://www.fellerheating.com/residential-hvac/rebates-and-specials/ |
| Smith Mechanical (NW WA) | Ductless heat pump installation page | https://smithmechanical.com/residential-hvac/ductless-heat-pump/ |
| LaVergne's Plumbing and Heating (Bellingham) | Commercial HVAC page | https://www.lavergneplumbing.com/commercial-hvac |
| Clean Air Comfort Systems (Bellingham heat pumps page; may be related to Clean Air, unverified) | Heat-pump service page | https://cleanaircomfortsystems.com/heat-pumps-bellingham-wa/ |

---

## 7. Rebates and incentives that could still apply to NEW construction in 2026

| Program | Applies to new construction? | Amount / status | Dates | Source | Tag |
|---|---|---|---|---|---|
| Federal 25C (Energy Efficient Home Improvement Credit; heat pumps up to $2,000) | No (existing homes); in any case **ended** | Ended | Systems installed **after 2025-12-31** do not qualify | [S?] https://heatpumpcostbystate.com/states/washington ; https://www.energysage.com/heat-pumps/how-much-does-a-mini-split-cost/ | [S?] |
| Federal 25D (Residential Clean Energy Credit: geothermal heat pumps, solar) | Could apply to a new home the owner occupies | Believed terminated for expenditures after 2025-12-31 (One Big Beautiful Bill Act, 2025) | 2025-12-31 | Not captured; verify at irs.gov | [K] |
| Federal 45L (New Energy Efficient Home Credit, builder credit) | **Yes (builders)** | Believed terminated for homes **acquired after 2026-06-30** (OBBBA) | 2026-06-30 | Not captured; verify at irs.gov | [K] |
| PSE (Puget Sound Energy; electric utility for most of Whatcom/Skagit) retrofit heat-pump rebates | **No** (conversions of existing homes) | $1,500 for converting electric resistance to a qualifying heat pump; income-qualified gas conversions $4,000+; stack up to $4,400 | current per page | [S?] https://heatpumpcostbystate.com/states/washington | [S?] |
| PSE new-construction / builder programs | Unknown | **PTS** | n/a | Check pse.com rebates for builders (not captured) | PTS |
| Stacking claim "PSE/SCL/Snohomish + HEEHRA + IRA 25C up to $12,500" | n/a | **Stale** (25C ended) | n/a | [S?] https://heatpumpcostbystate.com/states/washington | [S?] |
| WA state (Commerce) low-cost heat pump program, $11.1M expansion | **No** (King, Pierce, Snohomish, Kitsap only; not Whatcom/Skagit/San Juan) | $11.1M | 2025-26 news | [S] https://www.thecooldown.com/green-home/heat-pump-program-king-pierce-snohomish-kitsap/ ; https://www.yahoo.com/news/us/articles/washington-state-expands-low-cost-224400884.html | [S] |
| State/utility incentives in general | Varies | "49 states and Washington, D.C. currently offer state- or utility-level heat pump incentives" | n/a | [S?] https://www.energysage.com/heat-pumps/how-much-does-a-mini-split-cost/ ; https://www.energysage.com/heat-pumps/heat-pump-incentives/ | [S?] |
| HEAR / HEEHRA (IRA state rebates, WA Commerce) | New-construction eligibility **unknown** | PTS | n/a | not captured | PTS |
| Cascade Natural Gas (gas utility, Bellingham/Skagit) new-construction incentives | Possibly (gas equipment) | PTS | n/a | not captured | PTS |
| OPALCO (San Juan Islands electric co-op) heat-pump programs (e.g. on-bill "Switch It Up" [K]) | Unknown | PTS | n/a | not captured | [K]/PTS |
| Local contractor rebate pages | Pointer only | n/a | n/a | https://www.fellerheating.com/residential-hvac/rebates-and-specials/ | [S] |

---

## 8. Prices-to-set master list (for the bid engine catalog)

Columns:
- **street cost** is the lowest sourced street price (equipment is not marked up here).
- **band** is the sourced range.
- **status** is SOURCED (S or S?), DERIVED (D) or PTS.

The engine should record the retrieval date (2026-09-25) and replace these with distributor counter quotes when an account is available.

| Key (suggested) | Unit | Street cost / band | Status | Source URL |
|---|---|---|---|---|
| eq.mitsu.fx09.sys (MSZ-FX09NL + MUZ-FX09NLHZ) | EA | $2,811.75-$3,092.93 | S | https://hvacdirect.com/9-000-btu-mitsubishi-fx-series-33-1-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx09nlhz-msz-fx09nl-199106.html |
| eq.mitsu.fx12.sys | EA | $3,159.00 | S | https://hvacdirect.com/12-000-btu-mitsubishi-fx-series-29-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx12nlhz-msz-fx12nl-199107.html |
| eq.mitsu.fx15.sys | EA | $3,633.75 | S | https://hvacdirect.com/15000-btu-mitsubishi-fx-series-25-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx15nlhz-msz-fx15nl-199108.html |
| eq.mitsu.fx18.sys | EA | $4,230.75 | S? | https://hvacdirect.com/18000-btu-mitsubishi-fx-series-25-5-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx18nlhz-msz-fx18nl-199109.html |
| eq.mitsu.gx09.sys / gx12.sys | EA | $2,466.00 / $2,536.50 | S? | https://hvacdirect.com/12-000-btu-mitsubishi-gx-series-25-6-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-gx12nlhz-msz-gx12nl-199114.html |
| eq.fujitsu.xlth12.odu (AOUH12KZAH1) | EA | $2,169.30 | S | https://gotductless.com/products/fujitsu-aouh12kzah1-12-000-btu-orion-xlth-extra-low-temperature-outdoor-heat-pump |
| eq.fujitsu.xlth12.idu / xlth09.sys / xlth15.sys | EA | PTS | PTS | https://gotductless.com/products/fujitsu-asuh12kzas-aouh12kzah1-12-000-btu-30-5-seer2-extra-low-temperature-wall-mounted-system |
| eq.daikin.aurora12.sys | EA | $2,290.40-$2,339.00 | S | https://hvacdirect.com/12-000-btu-daikin-aurora-21-seer2-single-zone-wall-mount-mini-split-heat-pump-system-r32-230v-194698.html |
| eq.daikin.aurora18.sys | EA | $3,571.00-$4,113.23 | S | https://hvacdirect.com/18-000-btu-daikin-aurora-21-seer2-single-zone-wall-mount-mini-split-heat-pump-system-r32-230v-194700.html |
| eq.mitsu.mxz3d24h.odu | EA | $4,659.75 | S | https://onlinesupply.com/24000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-3d24nlhz.html |
| eq.mitsu.mxz3d30h.odu | EA | PTS | PTS | https://hvacdirect.com/30000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-3d30nlhz.html |
| eq.mitsu.sm36h.odu | EA | $5,473.00-$5,476.75 | S | https://onlinesupply.com/36000-btu-mitsubishi-m-series-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm36nlhz.html |
| eq.mitsu.sm42h.odu | EA | PTS | PTS | https://onlinesupply.com/42000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm42nlhz.html |
| eq.mitsu.sm48h.odu | EA | $7,635.75 | S | https://onlinesupply.com/48000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm48nlhz.html |
| eq.fujitsu.kwah4_36.odu | EA | $5,180.00 | S | https://skipthewarehouse.com/product/fujitsu-aouh36kwah4-3-ton-r-32-ductless-mini-split-outdoor-heat-pump/ |
| eq.fujitsu.kwah3_24.odu | EA | PTS | PTS | https://gotductless.com/products/fujitsu-aouh24kwah3-3-zone-24-000-btu-extra-low-temperature-multi-zone-outdoor-unit |
| eq.mitsu.head.fx09 | EA | $879.00-$987.00 | S | https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FX09NL/p160343.html |
| eq.mitsu.head.fx12 | EA | $1,034.00 | S | https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FX12NL/p160344.html |
| eq.mitsu.head.fx15 / fx18 / gx09 / gx12 | EA | PTS | PTS | https://hvacdirect.com/18000-btu-mitsubishi-fx-series-single-or-multi-zone-wall-mounted-mini-split-air-handler-r454b-msz-fx18nl.html |
| eq.mitsu.slimduct.sez_ad09 | EA | $1,232.00 | S | https://www.acwholesalers.com/Mitsubishi-HVAC-SEZ-AD09NL/p160495.html |
| eq.mitsu.slimduct.sez_ad12 / ad15 / ad18 | EA | PTS | PTS | https://www.acwholesalers.com/Mitsubishi-HVAC-SEZ-AD12NL/p160496.html |
| eq.mitsu.cassette.slz_af12 | EA | $1,266.94 | S | https://skipthewarehouse.com/product/mitsubishi-slz-af12nl-u1-12000-btu-ceiling-cassette-indoor-unit-r454b/ |
| eq.mitsu.cassette.slz_af09 / mlz_kx | EA | PTS | PTS | https://www.acwholesalers.com/Mitsubishi-HVAC-SLZ-AF09NL/p168591.html |
| eq.mitsu.ducted.pead_aa24 | EA | PTS (legacy PEAD-A24AA7 $2,235.00) | PTS / S? | https://www.acwholesalers.com/Mitsubishi-HVAC-PEAD-A24AA7/p84620.html |
| eq.mitsu.central36.puz_ak36nl_pva | EA | $8,015.25 | S | https://hvacdirect.com/mitsubishi-3-ton-19-5-seer2-ducted-central-air-inverter-heat-pump-split-system-r454b-201915.html |
| eq.mitsu.central36.h2i (R-454B hyper) | EA | PTS (legacy R-410A H2i system $11,897.00) | PTS / S | https://hvacdirect.com/mitsubishi-36-000-btu-17-8-seer-single-zone-heat-pump-system-id9753.html |
| eq.mitsu.central24 / central48 | EA | PTS | PTS | n/a |
| eq.bosch.ids36.odu (BOVA-36RXB-M15S) | EA | $3,888.00 | S | https://shop.unicosystem.com/bosch-3-ton-r-454-b-variable-speed-15-seer2-heat-pump |
| eq.bosch.ids36.ahu (BIVA-36) | EA | PTS | PTS | https://www.budgetheating.com/3-ton-bosch-ids-plus-17-seer2-r454b-heat-pump-inverter-system-bova-36rxb-m15s-biva-36rcb-m20x/ |
| eq.generic.ahu3t | EA | $900-$1,500 | S | https://homeguide.com/costs/air-handler-cost |
| eq.stripheat.5_10kw | EA | PTS | PTS | n/a |
| eq.erv.panasonic.fv10vec2 | EA | $1,036.99-$1,132.31 | S | https://www.homedepot.com/p/Panasonic-Intelli-Balance-100-Energy-Recovery-Ventilator-ERV-30-100-CFM-Standard-Plug-In-Cold-Climate-FV-10VEC2/332397326 |
| eq.erv.broan.b160e65rt | EA | $1,141.00 | S? | https://www.conservationmart.com/broan-ai-series-160-cfm-energy-recovery-ventilator-erv-top-port-b160e65rt/ |
| eq.erv.renewaire.evps | EA | $1,170.00 | S? | https://ervdirect.com/products/ev-premium-s |
| eq.erv.renewaire.evpm | EA | $1,415.00 | S? | https://ervdirect.com/products/ev-premium-m |
| eq.erv.zehnder.q350 | EA | PTS (pre-heater +$262.00) | PTS / S | https://zehnroom.com/shop/erv-kits-2/comfoair-q350-erv-unit-with-optional-pre-heater |
| eq.hrv.lunos.e2pair | PR | about $1,000-$2,000 (base to optioned kit) | S? | https://www.buildwithrise.com/stories/best-ductless-ervs-hrvs-2025 |
| eq.fan.panasonic.fv0511vks3 | EA | $213.99 | S | https://www.homedepot.com/p/Panasonic-WhisperGreen-Select-Pick-A-Flow-30-to-110-CFM-Bathroom-Exhaust-Fan-Flex-Z-Fast-Bracket-4-or-6-in-Duct-Adapter-FV-0511VKS3/331412123 |
| eq.fan.panasonic.fv0511vk3 | EA | $192.99 | S | https://www.homedepot.com/p/Panasonic-WhisperGreen-Select-Pick-A-Flow-50-80-or-110-CFM-Bathroom-Exhaust-Fan-Flex-Z-Fast-bracket-dual-4-or-6-in-Duct-Adapter-FV-0511VK3/331412121 |
| ctl.fan.aircycler.smartexhaust | EA | $98.60-$103.63 | S? | https://www.conservationmart.com/aircycler-smart-exhaust-bathroom-fan-light-timer-switch/ |
| ctl.fan.timer.other (Airetrak, MA-T51) | EA | PTS | PTS | https://www.supplyhouse.com/Tamarack-TTI-ATRAKAV-Airetrak-1A-Advantage-Bath-Fan-Control |
| mua.damper.broan.md6tu | EA | $269.00 | S? | https://www.supplyhouse.com/Broan-MD6TU-6-Automatic-Make-Up-Air-Damper-w-Pressure-Sensor-Kit |
| mua.damper.fantech.kit | EA | from $144.99 | S | https://www.hvacquick.com/products/residential/Makeup-Air/Residential-Makeup-Air-Fans |
| mua.system.fantech.muas | EA | from $2,190.30 | S | https://www.hvacquick.com/products/residential/Makeup-Air/Residential-Makeup-Air-Fans/Fantech-MUAS-Unitary-Residential-Makeup-Air-Systems |
| dryer.box.db425 | EA | $45.97 | S | https://www.homedepot.com/p/DRYERBOX-4-25-in-Dryer-Box-Metal-Recess-425THD/313741358 |
| dryer.booster.fantech.dbf4xlt | EA | $144-$397 | S? | https://www.acwholesalers.com/Fantech-DBF4XLT/p31290.html |
| ctl.mitsu.kumo_adapter | EA | $189.00 | S | https://www.acwholesalers.com/Mitsubishi-HVAC-PAC-USWHS002-WF-2/p102719.html |
| ctl.mitsu.mhk2 | EA | $414.75-$415.00 | S? | https://onlinesupply.com/hvac-supply/thermostats/filter/mitsubishi.html |
| ctl.mitsu.kumo_touch | EA | PTS | PTS | https://www.amazon.com/Mitsubishi-PAR-CT01MAU-SB-Touch-Remote-Controller/dp/B07VPCSNHL |
| ctl.tstat.ecobee.premium / enhanced | EA | $249-$250 / $190 | S / S? | https://www.ecobee.com/en-us/smart-thermostats/smart-thermostat-premium/ |
| ctl.tstat.honeywell.t6pro | EA | PTS | PTS | https://www.supplyhouse.com/Honeywell-Home-TH6220U2000-T6-Pro-Programmable-Thermostat-2H-1C-Heat-Pump-2H-2C-Conventional |
| mat.lineset.1438.50 | set | $115.26 (about $2.31/ft) | S / D | https://www.homedepot.com/p/VEVOR-50-ft-Mini-Split-Line-Set-1-4-in-3-8-in-O-D-Copper-Pipes-Tubing-and-Triple-Layer-Insulation-for-Air-Conditioning-KDLJTG50FT140P486V0/330127581 |
| mat.lineset.1412.25 | set | $94.40-$113.01 (about $3.78-$4.52/ft) | S / D | https://www.homedepot.com/p/VEVOR-25-ft-Mini-Split-Line-Set-1-4-in-and-1-2-in-O-D-Copper-Pipes-Tubing-and-Triple-Layer-Insulation-for-Air-Conditioning-KDLJTG25FT141DPZLV0/330128279 |
| mat.lineset.kit.1438.50 (with wire, sleeve, hose) | kit | $308.00 | S | https://www.homedepot.com/p/MRCOOL-50-ft-1-4-in-x-3-8-in-Flared-Line-Set-Kit-with-Communication-Wire-Wall-Sleeve-and-Drain-Hose-MC50-1438/312540656 |
| mat.lineset.3858.25 / .50 | set | PTS | PTS | https://www.supplyhouse.com/Generic-LS385825F-3-8-LL-x-5-8-SL-x-25-ft-Refrigerant-Line-Set-Flare-Ends-12685000-p |
| mat.lineset.3834.25 / .50 | set | PTS (pre-charged DIY sets $418.26 / $686.38, not pro-grade) | PTS / S | https://www.supplyhouse.com/Generic-LS383450-3-8-LL-x-3-4-SL-x-50-ft-Refrigerant-Line-Set-12665000-p |
| lab.adder.lineset_long_run | per ft | $15-$25 installed | S | https://homeguide.com/costs/air-source-heat-pump-cost |
| lab.adder.concrete_pad | EA | $300-$500 installed | S | https://homeguide.com/costs/air-source-heat-pump-cost |
| lab.adder.dedicated_circuit (if not excluded) | EA | about $250 | S | https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac.htm |
| mat.* (all items in section 2.2 table, #1-#39) | various | PTS | PTS | see 2.2 |
| lab.* task units (all rows in 3.3) | h | PTS | PTS | see 3.3 |
| rate.billed.hvac_tech | $/h | $75-$150 (national); $80-$200+ (install); **$140-$260 (Seattle)** | S | https://homeguide.com/costs/hvac-repair-cost ; https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/wa/seattle |
| rate.wage.hvac_mech.bellingham | $/h | PTS | PTS | https://www.bls.gov/oes/current/oes_13380.htm (not opened) |
| rate.prevailing.whatcom.refrig_ac | $/h | PTS | PTS | https://lni.wa.gov/licensing-permits/public-works-projects/prevailing-wage-rates/ (not opened) |
| sub.nc.per_sf | $/sf | $1.75-$2.50 (national floor) | S | https://homeguide.com/costs/hvac-cost |
| sub.ductless.per_head | $/head | $2,500-$5,000 | S | https://homeguide.com/costs/ductless-mini-split-ac-cost |
| sub.ducted_hp.system_wa | $/system | $8,000-$18,000+ (NW WA); WA average $15,500 | S | https://callcleanair.com/hvac-services/heat-pump-installation/ ; https://heatpumpcostbystate.com/states/washington |
| sub.erv.installed | $/EA | $1,500-$2,500 | S? | https://homeguide.com/costs/hvac-cost |
| sub.duct_test.third_party | $/test | PTS | PTS | n/a |
| sub.vent_flow_test | $/test | PTS | PTS | n/a |
| fee.mech_permit.bellingham / whatcom / skagit / sanjuan | $ | PTS | PTS | n/a |
| tax.sales.whatcom | % | PTS | PTS | n/a |

---

## 9. Source index (every URL cited, grouped)

**Equipment, Mitsubishi (retail)**
- https://hvacdirect.com/9-000-btu-mitsubishi-fx-series-33-1-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx09nlhz-msz-fx09nl-199106.html
- https://onlinesupply.com/9-000-btu-mitsubishi-fx-series-33-1-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx09nlhz-msz-fx09nl-199106.html
- https://hvacdirect.com/15000-btu-mitsubishi-fx-series-33-1-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx09nlhz-msz-fx09nl-199106.html
- https://hvacdirect.com/12-000-btu-mitsubishi-fx-series-29-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx12nlhz-msz-fx12nl-199107.html
- https://onlinesupply.com/12-000-btu-mitsubishi-fx-series-29-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx12nlhz-msz-fx12nl-199107.html
- https://hvacdirect.com/15000-btu-mitsubishi-fx-series-25-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx15nlhz-msz-fx15nl-199108.html
- https://onlinesupply.com/15000-btu-mitsubishi-fx-series-25-9-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx15nlhz-msz-fx15nl-199108.html
- https://hvacdirect.com/18000-btu-mitsubishi-fx-series-25-5-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-fx18nlhz-msz-fx18nl-199109.html
- https://hvacdirect.com/9-000-btu-mitsubishi-gx-series-28-4-seer2-single-wall-mounted-mini-split-heat-pump-system-r454b-muz-gx09nl-msz-gx09nl-199111.html
- https://hvacdirect.com/12-000-btu-mitsubishi-gx-series-25-6-seer2-single-wall-mounted-mini-split-hyper-heat-pump-system-r454b-muz-gx12nlhz-msz-gx12nl-199114.html
- https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FX09NL/p160343.html
- https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FX12NL/p160344.html
- https://www.acwholesalers.com/Mitsubishi-HVAC-MUZ-FX09NLHZ-MSZ-FX09NL/p168758.html
- https://www.supplystop.com/products/msz-fx09nl-9-000-btu-h-wall-mounted-indoor-unit
- https://skipthewarehouse.com/product/mitsubishi-msz-fx18nl-u1-15-ton-deluxe-wall-mounted-indoor-unit-r-454b/
- https://skipthewarehouse.com/product/mitsubishi-msz-fs12na-u1-1-ton-deluxe-h2i-plus-wall-mounted-indoor-unit/
- https://www.acwholesalers.com/Mitsubishi-HVAC-MSZ-FS09NA-MUZ-FS09NAH/p112561.html
- https://www.budgetheating.com/Mini-Split-9K-BTU-Mitsubishi-30-SEER-H2i-MUZ-MSZ-p/163118.htm
- https://www.mylinkdrive.com/USA/MUZ_FS09NAH_U1?product=&categoryName=R410A_Outdoor
- https://www.ecomfort.com/Mitsubishi-HVAC-MSZ-FS18NA-MUZ-FS18NA/p112559.html
- https://onlinesupply.com/24000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-3d24nlhz.html
- https://hvacdirect.com/30000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-3d30nlhz.html
- https://onlinesupply.com/36000-btu-mitsubishi-m-series-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm36nlhz.html
- https://www.supplystop.com/products/mxz-sm36nlhz-36-000-btu-h-hyper-heat-pump-outdoor-unit
- https://onlinesupply.com/42000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm42nlhz.html
- https://onlinesupply.com/48000-btu-mitsubishi-m-series-h2i-multi-zone-mini-split-hyper-heat-pump-condenser-r454b-mxz-sm48nlhz.html
- https://hvacdirect.com/mitsubishi-h2i-48-000-btu-multi-zone-ductless-heat-pump-condenser-mxz-sm48namhz-u1.html
- https://www.acwholesalers.com/Mitsubishi-HVAC-SEZ-AD09NL/p160495.html
- https://www.acwholesalers.com/Mitsubishi-HVAC-SEZ-AD12NL/p160496.html
- https://hvacdirect.com/9-000-btu-mitsubishi-kd-series-concealed-duct-mini-split-air-handler-r454b-sez-ad09nl.html
- https://hvacdirect.com/brands/mitsubishi-products/mitsubishi-mini-splits-by-mounting-type/mitsubishi-concealed-duct-mini-splits.html
- https://gotductless.com/products/mitsubishi-sez-ad09nl-suz-aa09nlhz-9-000-btu-horizontal-ducted-hyper-heatsystem
- https://gotductless.com/products/mitsubishi-sez-ad09nl-suz-aa09nl-9-000-btu-horizontal-ducted-system
- https://skipthewarehouse.com/product/mitsubishi-slz-af12nl-u1-12000-btu-ceiling-cassette-indoor-unit-r454b/
- https://www.acwholesalers.com/Mitsubishi-HVAC-SLZ-AF12NL/p168592.html
- https://www.acwholesalers.com/Mitsubishi-HVAC-SLZ-AF09NL/p168591.html
- https://hvacdirect.com/brands/mitsubishi-products/mitsubishi-mini-splits/mitsubishi-single-zone-mini-split-systems/filter/ceiling-cassette.html
- https://hvacdirect.com/hvac/pdf/SLZ-KF12NA-Submittal.pdf
- https://gotductless.com/products/mitsubishi-mlz-kx12nl-12-000-btu-one-way-ceiling-cassette-unit-unit-only
- https://skipthewarehouse.com/product/mitsubishi-mfz-kx12nl-1-ton-idu-floor-mount-r454b/
- https://www.acwholesalers.com/Mitsubishi-HVAC-PEAD-A24AA7/p84620.html
- https://www.acwholesalers.com/Mitsubishi-HVAC-PEAD-AA24NL/p160431.html
- https://gotductless.com/products/mitsubishi-pead-aa24nl-24-000-btu-horizontal-ducted-indoor-unit
- https://gotductless.com/products/mitsubishi-msz-gx09nl-9-000-btu-wall-mounted-unit
- https://hvacdirect.com/12000-btu-mitsubishi-gx-series-single-or-multi-zone-wall-mounted-mini-split-air-handler-r454b-msz-gx12nl.html
- https://hvacdirect.com/15000-btu-mitsubishi-fx-series-single-or-multi-zone-wall-mounted-mini-split-air-handler-r454b-msz-fx15nl.html
- https://hvacdirect.com/18000-btu-mitsubishi-fx-series-single-or-multi-zone-wall-mounted-mini-split-air-handler-r454b-msz-fx18nl.html
- https://hvacdirect.com/mitsubishi-3-ton-19-5-seer2-ducted-central-air-inverter-heat-pump-split-system-r454b-201915.html
- https://hvacdirect.com/36000-btu-mitsubishi-p-series-single-zone-mini-split-hyper-heat-pump-condenser-r454b-puz-ak36nlhz.html
- https://hvacdirect.com/mitsubishi-36-000-btu-17-8-seer-single-zone-heat-pump-system-id9753.html
- https://hvacdirect.com/mitsubishi-3-ton-15-2-seer2-ducted-central-air-inverter-h2i-heat-pump-split-system-r454b-198648.html
- https://gotductless.com/products/mitsubishi-svz-ap36nl-suz-ak36nlhz-36-000-btu-hyper-heating-multi-position-air-handler-system
- https://gotductless.com/products/svz-kp36na-mitsubishi-kp-36-000-btu-multi-position-air-handler
- https://www.acwholesalers.com/Mitsubishi-HVAC-PAC-USWHS002-WF-2/p102719.html
- https://onlinesupply.com/mitsubishi-kumo-cloud-wi-fi-adapter-pac-uswhs002-wf-2.html
- https://onlinesupply.com/hvac-supply/thermostats/filter/mitsubishi.html
- https://www.acwholesalers.com/cooling/mitsubishi-ductless-mini-split-controls.html
- https://www.amazon.com/Mitsubishi-PAR-CT01MAU-SB-Touch-Remote-Controller/dp/B07VPCSNHL
- https://goendlessenergy.com/blog/hvac/comparing-mitsubishi-410a-models-to-454b-models/
- https://www.mitsubishicomfort.com/new-product
- https://www.mitsubishipro.com/products/MUZ-FX12NLHZ-U1
- https://www.mitsubishipro.com/catalog/outdoor/multi-zone

**Equipment: Fujitsu, Daikin, Bosch**
- https://gotductless.com/products/fujitsu-aouh12kzah1-12-000-btu-orion-xlth-extra-low-temperature-outdoor-heat-pump
- https://gotductless.com/products/fujitsu-asuh12kzas-aouh12kzah1-12-000-btu-30-5-seer2-extra-low-temperature-wall-mounted-system
- https://gotductless.com/products/fujitsu-asuh12kzas-9-000-btu-orion-xlth-wall-mounted-indoor-unit
- https://gotductless.com/products/fujitsu-asuh09kzas-aouh09kzah1-9-000-btu-33-1-seer2-extra-low-temperature-wall-mounted-heat-pump-system
- https://gotductless.com/products/fujitsu-asuh15kzas-aouh15kzah1-15-000-btu-27-5-seer2-extra-low-temperature-orion-xlth-wall-mounted-system
- https://www.aprsupply.com/item/FUJ-ASUH12KZAS-12000-BTU-High-Tier
- https://www.fujitsugeneral.com/us/products/split/wall/r32/kzah1.html
- https://www.hvacrbusiness.com/news/2025/jun/11/fujitsu-introduces-airstage-orion-xlth-cold-climate-heat-pump/
- https://www.ecomfort.com/Fujitsu-12RLS3H/p65511.html
- https://www.ecomfort.com/Fujitsu-AOU36RLXFZH/p72694.html
- https://skipthewarehouse.com/product/fujitsu-aouh36kwah4-3-ton-r-32-ductless-mini-split-outdoor-heat-pump/
- https://gotductless.com/products/fujitsu-aouh24kwah3-3-zone-24-000-btu-extra-low-temperature-multi-zone-outdoor-unit
- https://gotductless.com/products/fujitsu-24-000-btu-extra-low-temp-outdoor-heat-pump-aou24rlxfzh
- https://hvacdirect.com/12-000-btu-daikin-aurora-21-seer2-single-zone-wall-mount-mini-split-heat-pump-system-r32-230v-194698.html
- https://hvacdirect.com/18-000-btu-daikin-aurora-21-seer2-single-zone-wall-mount-mini-split-heat-pump-system-r32-230v-194700.html
- https://www.totalhomesupply.com/p/daikin-ftxv18avju9-rxt18avju9-18000-btu-19-8-seer2-aurora-series-heat-cool-single-zone-mini-split-system-r32-refrigerant
- https://heatandcool.com/products/daikin-18-000-btu-19-8-seer2-aurora-series-low-ambient-ductless-mini-split-wall-mount-heat-pump-air-conditioner-r32-wi-fi-enabled
- https://sharkaire.com/12000-BTU-Daikin-19-Series-RX12AXVJU-FTX12AXVJU
- https://www.ferguson.com/product/daikin-dz17vsa-series-3-ton---up-to-18-seer-%2F-10-hspf-split-heat-pump---208%2F230%2F1---r-410a-ddz17vsa361ba/9766071.html
- https://shop.unicosystem.com/bosch-3-ton-r-454-b-variable-speed-15-seer2-heat-pump
- https://www.budgetheating.com/3-ton-bosch-ids-light-14-3-seer2-r454b-heat-pump-inverter-system-bova-36rxb-m15s-biva-36rxb-m15x/
- https://www.budgetheating.com/3-ton-bosch-ids-plus-17-seer2-r454b-heat-pump-inverter-system-bova-36rxb-m15s-biva-36rcb-m20x/
- https://www.budgetheating.com/3-ton-bosch-premium-connected-19-seer2-r454b-heat-pump-inverter-system-bova-36rtb-m20s-biva-36rcb-m20x/
- https://hvacdirect.com/bosch-ids-light-series-3-ton-14-5-seer2-ducted-central-air-inverter-heat-pump-split-system-r454b-201064.html
- https://tssassociatesinc.com/wp-content/uploads/2025/01/2025-Residential-AC-Price-Book-US-CA-R454B_76HPL1801V.pdf

**Ventilation, fans, controls, dryer, make-up air**
- https://www.homedepot.com/p/Panasonic-Intelli-Balance-100-Energy-Recovery-Ventilator-ERV-30-100-CFM-Standard-Plug-In-Cold-Climate-FV-10VEC2/332397326
- https://www.conservationmart.com/panasonic-100-cfm-cold-climate-intelli-balance-erv-fv-10vec2/
- https://www.conservationmart.com/broan-ai-series-160-cfm-energy-recovery-ventilator-erv-top-port-b160e65rt/
- https://www.supplyhouse.com/Broan-B160E65RT-160-CFM-AI-Series-Energy-Recovery-Ventilator-w-Top-Ports-67-Efficiency
- https://broan-nutone.com/en-us/product/freshairsystems/b130e65rt
- https://ervdirect.com/products/ev-premium-s
- https://ervdirect.com/products/ev-premium-m
- https://www.positive-energy.com/product/renewaire-premium-s-erv/
- https://renewaire.com/product/ev-premium-m/
- https://zehnroom.com/shop/erv-kits-2/comfoair-q350-erv-unit-with-optional-pre-heater
- https://www.zehnroom.com/q350/zehnder-comfoair-q350-complete-erv-kit
- https://zehnroom.com/ca200
- https://mainstreamcorporation.com/index.php?option=com_eshop&view=product&id=174&catid=2&Itemid=314
- https://www.greenbuildingadvisor.com/question/zehnder-erv-quote
- https://www.greenbuildingadvisor.com/question/zehnder-price-shock-best-bang-for-buck-alternative
- https://www.buildwithrise.com/stories/best-ductless-ervs-hrvs-2025
- https://www.greenbuildingadvisor.com/question/lunos-e2-ductless-hrv-system-vs-ducted-system
- https://475.supply/products/lunos-e-kit
- https://475.supply/products/lunos-additional-exterior-cover
- https://www.homedepot.com/p/Panasonic-WhisperGreen-Select-Pick-A-Flow-30-to-110-CFM-Bathroom-Exhaust-Fan-Flex-Z-Fast-Bracket-4-or-6-in-Duct-Adapter-FV-0511VKS3/331412123
- https://www.supplyhouse.com/Panasonic-FV-0511VKS3-Panasonic-WhisperGreen-Select-Dual-Speed-Ceiling-Mount-Exhaust-Fan-Customizable-30-to-110-CFM-FV-0511VKS3
- https://www.homedepot.com/p/Panasonic-WhisperGreen-Select-Pick-A-Flow-50-80-or-110-CFM-Bathroom-Exhaust-Fan-Flex-Z-Fast-bracket-dual-4-or-6-in-Duct-Adapter-FV-0511VK3/331412121
- https://www.homedepot.com/p/Panasonic-WhisperGreen-Select-Pick-A-Flow-30-to-110-CFM-Bathroom-Exhaust-Fan-Flex-ZFast-Bracket-4-6-in-Duct-Adapter-FV-0511VKS3S/331414384
- https://www.homedepot.com/p/Panasonic-WhisperCeiling-DC-Fan-with-Pick-A-Flow-Speed-Selector-50-80-or-110-CFM-and-Flex-Z-Fast-Installation-Bracket-FV-0511VQ1/303619101
- https://www.conservationmart.com/aircycler-smart-exhaust-bathroom-fan-light-timer-switch/
- https://www.conservationmart.com/p-2917-aircycler-smartexhaust-decorarocker-bath-fan-timer-switch.aspx
- https://www.aircycler.com/products/smartexhaust
- https://www.supplyhouse.com/Tamarack-TTI-ATRAKAV-Airetrak-1A-Advantage-Bath-Fan-Control
- https://www.homedepot.com/p/Lutron-Maestro-Digital-Timer-Switch-5-Amp-Fan-600-Watt-Incandescent-Bulbs-White-MA-T51-WH-MA-T51-WH/100652547
- https://www.supplyhouse.com/Broan-MD6T-6-Automatic-Make-Up-Air-Damper-Direct-Wired
- https://www.supplyhouse.com/Broan-MD6TU-6-Automatic-Make-Up-Air-Damper-w-Pressure-Sensor-Kit
- https://www.hvacquick.com/products/residential/Makeup-Air/Residential-Makeup-Air-Fans
- https://www.hvacquick.com/products/residential/Makeup-Air/Residential-Makeup-Air-Fans/Fantech-MUAS-Unitary-Residential-Makeup-Air-Systems
- https://www.homedepot.com/p/DRYERBOX-4-25-in-Dryer-Box-Metal-Recess-425THD/313741358
- https://www.ebay.com/itm/186237943133
- https://www.acwholesalers.com/Fantech-DBF4XLT/p31290.html
- https://www.hvacquick.com/products/residential/Dryer-boosting/dryer-booster-fans/fantech-dryer-boosters
- https://www.ecobee.com/en-us/smart-thermostats/smart-thermostat-premium/
- https://www.smarthomeexplorer.com/guides/ecobee-smart-thermostat-premium-price-2026
- https://smarthomedock.com/ecobee-smart-thermostat-premium-enhanced-review/
- https://www.supplyhouse.com/Honeywell-Home-TH6220U2000-T6-Pro-Programmable-Thermostat-2H-1C-Heat-Pump-2H-2C-Conventional
- https://www.supplyhouse.com/Honeywell-Home-Resideo-TH6220WF2006-T6-Pro-Smart-Wi-Fi-Programmable-Thermostat-2H-2C

**Line sets**
- https://www.homedepot.com/p/VEVOR-25-ft-Mini-Split-Line-Set-1-4-in-and-1-2-in-O-D-Copper-Pipes-Tubing-and-Triple-Layer-Insulation-for-Air-Conditioning-KDLJTG25FT141DPZLV0/330128279
- https://www.homedepot.com/p/SKYSHALO-25-ft-HVAC-Mini-Split-Line-Set-Triple-Insulated-1-4-in-and-1-2-in-Copper-Pipes-with-Wrapping-Strips-Included-KDLJTG25FT141DPZLV0-250612/336898130
- https://www.homedepot.com/p/VEVOR-50-ft-Mini-Split-Line-Set-1-4-in-3-8-in-O-D-Copper-Pipes-Tubing-and-Triple-Layer-Insulation-for-Air-Conditioning-KDLJTG50FT140P486V0/330127581
- https://www.homedepot.com/p/MRCOOL-50-ft-1-4-in-x-3-8-in-Flared-Line-Set-Kit-with-Communication-Wire-Wall-Sleeve-and-Drain-Hose-MC50-1438/312540656
- https://www.homedepot.com/b/Heating-Venting-Cooling-Mini-Split-Air-Conditioners-Mini-Split-Parts/Mini-Split-Line-Sets/N-5yc1vZ1z18ggrZ1z19b6r
- https://www.lowes.com/pd/MRCOOL-No-Vac-25ft-3-8-x-3-4-R454B-Line-set-0-75-in-W-x-0-375-in-H-Central-Air-conditioner-line-set/5016255613
- https://www.lowes.com/pd/MRCOOL-No-Vac-50ft-3-8-x-3-4-R454B-Line-set-0-75-in-W-x-0-375-in-H-Central-Air-conditioner-line-set/5016255593
- SupplyHouse / Home Depot line-set SKU pages listed in 2.1 (PTS rows)

**Installed-cost guides and local contractors**
- https://homeguide.com/costs/ductless-mini-split-ac-cost
- https://homeguide.com/costs/ductless-heat-pump-cost
- https://homeguide.com/costs/air-source-heat-pump-cost
- https://homeguide.com/costs/air-handler-cost
- https://homeguide.com/costs/heat-pump-cost
- https://homeguide.com/costs/hvac-cost
- https://homeguide.com/costs/cost-to-replace-ductwork
- https://homeguide.com/costs/hvac-repair-cost
- https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac.htm
- https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/wa/seattle
- https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/ca/los-angeles
- https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/az/phoenix
- https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/fl/tampa
- https://www.angi.com/articles/how-much-does-it-cost-install-ductless-mini-split-ac/mo/st-louis
- https://www.angi.com/articles/how-much-does-heat-pump-cost.htm
- https://www.angi.com/articles/energy-recovery-ventilator-erv-system-scores-high-marks.htm
- https://www.fixr.com/costs/heat-pump-installation
- https://www.fixr.com/costs/ductwork
- https://www.fixr.com/costs/central-air-conditioner-installation
- https://www.fixr.com/costs/ventilation-installation
- https://www.thisoldhouse.com/heating-cooling/split-ac-installation-cost
- https://www.thisoldhouse.com/heating-cooling/21016174/how-an-energy-recovery-ventilator-erv-works
- https://modernize.com/hvac/heating-repair-installation/heat-pump/ductless
- https://www.energysage.com/heat-pumps/how-much-does-a-mini-split-cost/
- https://www.energysage.com/heat-pumps/costs-and-benefits-air-source-heat-pumps/
- https://www.energysage.com/heat-pumps/heat-pump-incentives/
- https://hvacprojectcost.com/daikin-fit-cost/
- https://hvacprojectcost.com/mini-split-installation-cost/
- https://realcostiq.com/guides/mini-split-installation-cost/
- https://filterbuy.com/heating-cooling/mini-splits/cost/mini-split-installation-cost/
- https://www.hvacbase.org/heat-pump-cost-to-install
- https://heatpumpcostbystate.com/states/washington
- https://heatpumpcostcalculator.com/cost-by-state/washington
- https://varsityheating.com/blog/heat-pump-cost-washington/
- https://heatpumpwa.com/blog/cost-of-heat-pump-in-washington-state/
- https://www.budgetheating.com/understanding-the-cost-of-a-new-hvac-system-guid/
- https://buseheatandair.com/blog/new-hvac-system-cost/
- https://costtobuildahouse.com/blog/articles/new-construction-hvac-cost
- https://hvaccalculatorhub.com/blog/hvac-diagnostic-fee-guide-2026
- https://www.essentrahvac.com/post/what-is-the-average-cost-of-an-hvac-service-call
- https://www.barronheating.com/blog/2025/june/heat-pump-installation-cost-in-bellingham-wa/
- https://www.barronheating.com/ ; https://www.barronheating.com/service-area/bellingham-wa
- https://callcleanair.com/hvac-services/heat-pump-installation/ ; https://callcleanair.com/hvac-services/mini-splits/ ; https://callcleanair.com/ ; https://callcleanair.com/service-locations/whatcom-county-wa/
- https://www.homeyou.com/wa/heat-pump-bellingham-costs
- https://www.fellerheating.com/service-repair/ ; https://www.fellerheating.com/residential-hvac/rebates-and-specials/
- https://smithmechanical.com/residential-hvac/ductless-heat-pump/
- https://www.lavergneplumbing.com/commercial-hvac
- https://cleanaircomfortsystems.com/heat-pumps-bellingham-wa/

**Channels and incentives**
- https://www.ferguson.com/product/mitsubishi-12k-btu---outdoor-ductless-heat-pump---hyper-heating-inverter---r-454b-mmuzfx12nlhz/11534663.html
- https://www.ferguson.com/product/mitsubishi-48k-btu---outdoor-multi-zone-heat-pump---hyper-heating-inverter---r-454b-mmxzsm48nlhz/11534701.html
- https://www.ferguson.com/product/fujitsu-36k-btu-multi-zone-outdoor-heat-pump---r-32-faouh36kwah4/11534515.html
- https://www.fergusonhome.com/mitsubishi-msz-fs12na-muz-fs12nah/s1972126?uid=4686210&searchId=be24fQlkJM
- https://www.tranesupply.com/product/mxzsm48nlhz/01t4w00000NkJ31AAF
- https://shop.youngsupply.com/item/mitsubishi-electric-muz-fx12nlhz
- https://www.insco.com/2626285/p/n/mitsubishi-electric-muz-fx12nlhz
- https://www.thecooldown.com/green-home/heat-pump-program-king-pierce-snohomish-kitsap/
- https://www.yahoo.com/news/us/articles/washington-state-expands-low-cost-224400884.html
- Not opened (egress-blocked) but named as where to fill PTS: https://www.bls.gov/oes/current/oes_13380.htm ; https://lni.wa.gov/licensing-permits/public-works-projects/prevailing-wage-rates/ ; https://sbcc.wa.gov

---

## 10. Open items to close before the engine goes live (ordered by bid impact)

1. **Local sub quotes (2-3 Whatcom/Skagit HVAC subs)** on one reference NC plan: ducted heat pump and all-ductless variants, plus ERV and exhaust scope. This replaces the national $/sf floor in 4.3.
2. **Distributor counter prices** (Johnstone / Gensco / Ferguson Bellingham, branches unverified) for every PTS row in 2.2, especially flex duct, boots, registers, line-hide, refrigerant R-454B / R-32 per lb and 14/4 wire.
3. **Labour units** (section 3.3), from RSMeans / Craftsman or sub interviews; crew norm; San Juan mobilisation adder.
4. **Wages**: BLS OEWS 49-9021 for Bellingham MSA and Mount Vernon-Anacortes MSA; L&I prevailing wage for Whatcom, Skagit and San Juan.
5. **Code-driven test costs**: third-party duct leakage and ventilation flow tests (2021 WSEC-R); mechanical permit fees for Bellingham, Whatcom County, Skagit County and San Juan County.
6. **Incentives**: confirm 25D / 45L termination dates at irs.gov; PSE builder programs; Cascade Natural Gas; OPALCO.
7. **Re-open every [S] and [S?] URL** above and record the live price and date. Retail "special" prices move weekly.
