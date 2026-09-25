import math
def mj_infil_cfm(ach50, vol, stories, htd, wind_mph=15.0, sc=4):
    q50=ach50*vol/60.0
    ela=0.05488*q50   # in2 at 4 Pa, n=0.65 (NREL/RESNET 301 conversion)
    cs=0.015*stories
    cw=(0.0065-0.00266*(sc-3))*stories**0.4
    return ela*math.sqrt(cs*htd+cw*wind_mph**2), ela, q50
def house(name, cfa, stories, footprint_perim, ceil_h_avg, wall_h_total, wfr, nbr, fnd, ach50, vent, htd, ctd,
          u_win=0.28, shgc=0.28, u_wall=0.056, u_ceil=0.024, u_floor=0.029, f_slab=0.54, u_door=0.20, door_a=40, sc=4, isc=0.835):
    vol=cfa*ceil_h_avg
    win=wfr*cfa
    gross_wall=footprint_perim*wall_h_total
    net_wall=gross_wall-win-door_a
    ceil_a=cfa/stories
    q={}
    q['windows']=win*u_win*htd
    q['doors']=door_a*u_door*htd
    q['walls']=net_wall*u_wall*htd
    q['ceiling']=ceil_a*u_ceil*htd
    if fnd=='crawl':
        # MJ8 Fig A12-6 vented crawl PTDH; crawl wall U assumed 0.25
        ptdh=htd/(1+4*u_floor/(0.25+0.11))
        q['floor']=ceil_a*u_floor*ptdh
    else:
        q['slab']=f_slab*footprint_perim*htd
    icfm,ela,q50=mj_infil_cfm(ach50,vol,stories,htd,15.0,sc)
    # WA vent rate
    qr=max(0.01*cfa+7.5*(nbr+1),30)
    if vent=='exhaust':
        qv=qr*1.5
        ncfm=(icfm**1.5+qv**1.5)**0.67
        q['infil+vent']=1.1*ncfm*htd
    else: # balanced HRV/ERV distributed, apparent sens eff 0.70
        qv=qr*1.0
        q['infil']=1.1*icfm*htd
        q['vent']=1.1*qv*(1-0.70)*htd
    tot=sum(q.values())
    # WSU method
    ua=(win+door_a)*0.30+net_wall*u_wall+ceil_a*u_ceil
    if fnd=='crawl': ua+=ceil_a*u_floor
    else: ua+=f_slab*footprint_perim
    wsu_dt=51
    wsu=ua*wsu_dt+vol*0.6*wsu_dt*0.018
    # cooling (MJ8-like, CTD) windows equal on N/E/S/W, ISC
    P={'N':33.1,'E':210.7,'S':182.3,'W':210.7}
    clf_is={'N':0.29,'E':0.32,'S':0.18,'W':0.32}
    clf_no={'N':0.48,'E':0.38,'S':0.24,'W':0.38}
    cw=0
    for d in P:
        clf=clf_is[d] if isc<1 else clf_no[d]
        cw+=win/4*(P[d]*clf*shgc*isc/0.87+u_win*ctd)
    # attic ceiling: vented attic dark shingle 130F at 95F design -> +(Tout-95)
    tout=75+ctd
    attic=130+(tout-95)
    cc=ceil_a*u_ceil*(attic-75)
    cdoor=door_a*u_door*(ctd+11)
    # walls C-D group medium color
    cltd=max(21.25*0.83+(ctd-20),0)
    cwall=net_wall*u_wall*cltd
    icfm_c,_,_=mj_infil_cfm(ach50,vol,stories,ctd,7.5,sc)
    cinf=1.1*icfm_c*ctd
    occ=nbr+1
    cint=2400+230*occ
    csens=cw+cc+cdoor+cwall+cinf+cint
    clat=200*occ+0.68*icfm_c*4  # 4 grains @50%RH Bellingham
    print(f"--- {name}: CFA {cfa}, vol {vol:.0f}, win {win:.0f} sf, ACH50 {ach50}, vent {vent} Qr {qr:.0f} Qv {qv:.0f}, ICFM_htg {icfm:.1f} (ACHnat {icfm*60/vol:.3f}, N={ach50/(icfm*60/vol):.1f})")
    for k,v in q.items(): print(f"   {k}: {v:,.0f}")
    print(f"   MJ heating total @HTD {htd}: {tot:,.0f} Btuh = {tot/cfa:.1f} Btuh/sf")
    print(f"   WSU method @dT 51: {wsu:,.0f} Btuh ({wsu/cfa:.1f}/sf); x1.25 HP max {1.25*wsu:,.0f}; x1.40 furnace {1.40*wsu:,.0f}")
    print(f"   Cooling @CTD {ctd}: windows {cw:,.0f}, ceiling {cc:,.0f}, doors {cdoor:,.0f}, walls {cwall:,.0f}, infil {cinf:,.0f}, internal {cint:,.0f}; sens {csens:,.0f}; lat {clat:,.0f}; total {csens+clat:,.0f} ({(csens+clat)/cfa:.2f} Btuh/sf; {cfa/((csens+clat)/12000):,.0f} sf/ton); ratio clg/htg {(csens+clat)/tot:.2f}")
for ach in (3.0,5.0):
  for vent in ('exhaust','hrv'):
    house('A 2-story crawl',2400,2,140,8.5,18,0.15,3,'crawl',ach,vent,47,1)
house('A 2-story crawl CTD5',2400,2,140,8.5,18,0.15,3,'crawl',3.0,'exhaust',47,5)
house('A 2-story crawl HTD51',2400,2,140,8.5,18,0.15,3,'crawl',3.0,'exhaust',51,5)
house('B 1-story slab',1800,1,180,9.0,9.5,0.15,3,'slab',3.0,'exhaust',47,1)
house('B 1-story slab hrv',1800,1,180,9.0,9.5,0.15,3,'slab',3.0,'hrv',47,1)
house('C 2-story 3000 crawl 20% glass',3000,2,160,9.0,19,0.20,4,'crawl',4.0,'exhaust',47,3)
house('D 2-story 2000 crawl 12% glass',2000,2,128,8.5,18,0.12,3,'crawl',2.5,'hrv',47,1)
