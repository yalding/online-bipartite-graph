"""Explore iterating the initial-phase birth profile with forced old floors.

This is a floating discovery experiment. Any contradiction needs independent
directed rounding or exact arithmetic and a finite-witness proof.
"""
from pathlib import Path
import argparse,json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=300)
    p.add_argument('--steps',type=int,default=80)
    p.add_argument('--radius',type=float,default=float(np.sqrt(np.e)))
    args=p.parse_args()
    R=args.radius
    beta=R/(1+2*np.log(R))
    def base_tail(q):
        q=np.asarray(q)
        mid=np.maximum(q,1/R)
        out=np.where(q<R,beta/R*(R-mid*(np.log(R/mid)+1)),0.)
        return np.where(q<1/R,out+(1/R-q)-beta*((1/R)**2-q*q)/2,out)
    base_integral=float(base_tail(0))
    slack=beta-base_integral
    s=np.linspace(0,4,args.n+1)
    d=np.where(s<=1/R,1-beta*s,np.where(s<R,beta/R*np.log(R/np.maximum(s,1e-100)),0))
    d=np.maximum(0,d)
    v=np.linspace(0,1,args.n+1)
    r=1+np.maximum(0,s[:,None]/slack-1)*v
    cap=r*(beta-base_tail(np.divide(s[:,None],r)))
    records=[]
    for h in range(args.steps+1):
        cumulative=np.r_[0,np.cumsum((d[:-1]+d[1:])/2*np.diff(s))]
        total=float(cumulative[-1])
        capacity_slack=float(np.min(cap-cumulative[:,None]))
        record=dict(depth=h,integral=total,min_capacity_slack=capacity_slack,max_value=float(d.max()))
        records.append(record)
        print(record,flush=True)
        if total>beta+1e-6 or capacity_slack < -1e-6 or d.max()>1+1e-6:
            break
        assert np.max(np.diff(d))<1e-6, 'Nonmonotone birth profile; inversion invalid'
        def floor_cost(w):
            # d decreases, so this finds the length of its superlevel set.
            tw=np.interp(w,d[::-1],s[::-1])
            x=np.minimum(s[:,None],tw)
            return np.interp(x,s,cumulative)+(s[:,None]-x)*w
        lo=np.zeros_like(cap);hi=np.ones_like(cap)
        for _ in range(36):
            mid=(lo+hi)/2
            below=floor_cost(mid)<=cap
            lo=np.where(below,mid,lo);hi=np.where(below,hi,mid)
        accumulated=np.trapezoid(1-lo,r,axis=1)
        updated=np.maximum(d,np.maximum(0,1-beta*s+accumulated))
        if np.max(updated-d)<1e-10:
            break
        d=updated
    result=dict(beta=beta,radius=R,grid=args.n,records=records,
                final_profile=[list(map(float,x)) for x in zip(s,d)],
                status='Exploratory float profile iteration; not certified')
    (ROOT/'experiments'/f'profile-iterate-{args.n}-R{R:.6f}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')

if __name__=='__main__':
    main()
