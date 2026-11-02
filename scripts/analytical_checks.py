"""Independent numerical checks of the symbolic identities used in the notes."""
from pathlib import Path
import json
import mpmath as mp
from star_tightness import K, allocation

mp.mp.dps=70
ROOT=Path(__file__).resolve().parents[1]

def main():
    B=1+allocation(0)
    points=list(map(mp.mpf,['0','0.1','0.5','0.9','1']))
    charge_residual=max(abs(1+allocation(1-z)+mp.quad(
        lambda t:(1-t)/allocation(t),[z,1])-B) for z in points)
    derivative_residual=max(abs(mp.diff(allocation,z)+z/allocation(1-z)) for z in points)
    r=mp.sqrt(mp.e)
    beta=r/2
    def profile(t):
        if t<=1/r:
            return 1-beta*t
        if t<r:
            return mp.log(r/t)/2
        return mp.mpf(0)
    def tail(q):
        if q>=r:
            return mp.mpf(0)
        if q>=1/r:
            return (r-q*(mp.log(r/q)+1))/2
        s=1/r
        return s-q-beta*(s*s-q*q)/2+tail(s)
    ts=[mp.mpf('0.1'),1/r,mp.mpf('0.9'),mp.mpf(1),mp.mpf('1.5'),r,mp.mpf(2),mp.mpf(10)]
    fixed_residual=max(abs(profile(t)-max(0,1-beta*t+t*tail(1/t))) for t in ts)
    integral=tail(mp.mpf(0))
    assert max(charge_residual,derivative_residual,fixed_residual)<mp.mpf('1e-60')
    assert abs(integral-(beta-1/(4*r)))<mp.mpf('1e-60')
    result={key:str(value) for key,value in dict(k=K,cover_upper=B,matching_optimum=1/B,
        cover_lower=1+beta,remaining_gap=B-1-beta,
        charging_identity_max_residual=charge_residual,
        allocation_derivative_max_residual=derivative_residual,
        critical_fixed_point_max_residual=fixed_residual,
        critical_profile_integral=integral,critical_budget_slack=1/(4*r)).items()}
    result['scope']='High precision numerical identity checks; analytic arguments are in notes and papers'
    try:
        (ROOT/'experiments'/'analytical-checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    except PermissionError:
        pass
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
