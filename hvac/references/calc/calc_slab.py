import math
def f_value(k_soil, thick=4.0, perim_depth=0, perim_r=0, under_width=0, under_r=0, under_full=False, ext_h_r=0, ext_h_depth=0, ext_h_width=0):
    r_gravel_per_in=0.65
    fvals=[]
    for path_radius in range(8,14):
        ueff=[]
        for radius in range(0,path_radius+1):
            spl=max(math.pi*radius-1,0)
            r_ins=0.0
            if radius==0:
                r_conc=0.0; r_grav=0.0
                if perim_depth>0: r_ins=perim_r
            else:
                r_conc=thick*0.08
                r_grav=max(r_gravel_per_in*(12.0-thick),0)
                if under_full: r_ins+=under_r
                elif radius<=under_width: r_ins+=under_r
                if radius<=perim_depth: r_ins+=perim_r
                if ext_h_r>0 and radius>=ext_h_depth:
                    hyp=math.sqrt(ext_h_depth**2+ext_h_width**2)
                    if radius<=hyp: r_ins+=ext_h_r
            r_air=0.05+0.92+0.17
            r_soil=spl/k_soil
            ueff.append(1.0/(r_conc+r_grav+r_ins+r_air+r_soil))
        fvals.append(sum(ueff))
    return sum(fvals)/len(fvals)
cases=[("uninsulated",{}),
       ("R-10 vertical perimeter 2 ft",dict(perim_depth=2,perim_r=10)),
       ("R-10 vertical perimeter 4 ft",dict(perim_depth=4,perim_r=10)),
       ("R-10 under slab 4 ft wide (horizontal perimeter)",dict(under_width=4,under_r=10)),
       ("R-10 under entire slab + R-10 edge",dict(under_full=True,under_r=10,perim_depth=1,perim_r=10)),
       ("R-15 under entire slab + R-10 edge",dict(under_full=True,under_r=15,perim_depth=1,perim_r=10)),
      ]
for k in (0.8,1.0):
    print("k_soil",k)
    for n,kw in cases:
        print(f"   {n}: F = {f_value(k,**kw):.3f} Btu/h-ft-F")
