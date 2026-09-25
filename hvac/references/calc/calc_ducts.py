import math
# ASHRAE HOF Ch.21 (I-P): dp_f[in.w.c.] = 12 f L/D * rho * (V/1097)^2 ; Re = 8.56 D V (D in, V fpm, std air)
rho=0.075
def colebrook(Re, eps_in, D_in):
    f=0.02
    for _ in range(100):
        rhs=-2*math.log10(eps_in/(3.7*D_in)+2.51/(Re*math.sqrt(f)))
        fn=1/rhs**2
        if abs(fn-f)<1e-10: break
        f=fn
    return f
def fr_per100(D_in, cfm, eps_ft):
    A=math.pi*(D_in/12)**2/4
    V=cfm/A
    Re=8.56*D_in*V
    f=colebrook(Re, eps_ft*12, D_in)
    return 12*f*100/D_in*rho*(V/1097)**2, V
def cfm_at_fr(D_in, fr, eps_ft):
    lo,hi=1,20000
    for _ in range(200):
        mid=(lo+hi)/2
        v,_=fr_per100(D_in,mid,eps_ft)
        if v>fr: hi=mid
        else: lo=mid
    return mid
sizes=[4,5,6,7,8,9,10,12,14,16]
print("Rigid galvanized eps=0.0003 ft")
print("D | cfm@0.06 | cfm@0.08 | cfm@0.10 | V@0.08 fpm")
for D in sizes:
    c=[cfm_at_fr(D,fr,0.0003) for fr in (0.06,0.08,0.10)]
    A=math.pi*(D/12)**2/4
    print(D, [round(x) for x in c], round(c[1]/A))
print("Flex fully extended eps=0.003 ft (ASHRAE lower bound of 0.003-0.015 ft)")
for D in sizes:
    c=[cfm_at_fr(D,fr,0.003) for fr in (0.06,0.08,0.10)]
    print(D, [round(x) for x in c])
print("Flex eps=0.015 ft (upper bound)")
for D in sizes:
    c=[cfm_at_fr(D,fr,0.015) for fr in (0.06,0.08,0.10)]
    print(D, [round(x) for x in c])
