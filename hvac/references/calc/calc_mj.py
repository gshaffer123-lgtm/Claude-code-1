import math
lat=48.8
# MJ8 Table 3D-2 PSF (as implemented in NREL OpenStudio-HPXML hvac_sizing.rb)
psf_lats=[28,34,40,46,52,60]
psf={'S':[91,121,149,173,193,211],'SW':[172,185,196,205,212,217],'W':[220,219,216,213,208,199],
     'NW':[149,140,135,130,124,114],'N':[38,37,35,34,32,28],'NE':[149,140,135,130,124,114],
     'E':[220,219,216,213,208,199],'SE':[172,185,196,205,212,217]}
psf_h=[272,261,247,230,208,176]
def interp(x,xs,ys):
    for i in range(len(xs)-1):
        if xs[i]<=x<=xs[i+1]:
            return ys[i]+(ys[i+1]-ys[i])*(x-xs[i])/(xs[i+1]-xs[i])
P={k:interp(lat,psf_lats,v) for k,v in psf.items()}
Ph=interp(lat,psf_lats,psf_h)
print("PSF at lat 48.8:",{k:round(v,1) for k,v in P.items()},"H",round(Ph,1))
clf_nois={'S':0.24,'SW':0.35,'W':0.38,'NW':0.40,'N':0.48,'NE':0.40,'E':0.38,'SE':0.35}
clf_is={'S':0.18,'SW':0.29,'W':0.32,'NW':0.32,'N':0.29,'NE':0.32,'E':0.32,'SE':0.29}
dirs=['N','NE','E','SE','S','SW','W','NW']
def htm(d,shgc,u,ctd,isc):
    clf = clf_is[d] if isc<1 else clf_nois[d]
    return P[d]*clf*shgc*isc/0.87 + u*ctd
for (shgc,u) in [(0.25,0.28),(0.28,0.28),(0.30,0.30)]:
  for isc in [1.0,0.835,0.67]:
    for ctd in [1,5]:
        row=[round(htm(d,shgc,u,ctd,isc),1) for d in dirs]
        print(f"SHGC {shgc} U {u} ISC {isc} CTD {ctd}:",dict(zip(dirs,row)))
# skylight horizontal (flat) HTM: (PSF_h*CLF_h)*(SHGC*ISC/0.87)+U*(CTD+15)
for shgc,u in [(0.25,0.50),(0.30,0.50)]:
    for ctd in [1,5]:
        print("skylight flat",shgc,u,ctd, round(Ph*0.68*shgc/0.87 + u*(ctd+15),1))
# heating HTM
for htd in [47,51]:
    print("HTD",htd,"window U0.28:",round(0.28*htd,2),"U0.30:",round(0.30*htd,2))
