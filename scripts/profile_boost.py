"""Exploratory profile-aware necessary inequality at Lu's critical profile.

Floating quadrature only. This does not by itself certify a lower bound.
"""
from pathlib import Path
import argparse
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BETA=np.sqrt(np.e)/2
R=np.sqrt(np.e)
SLACK=1/(4*R)

def tail(q):
    q=np.asarray(q)
    mid=np.maximum(q,1/R)
    out=np.where(q<R,(R-mid*(np.log(R/mid)+1))/2,0.)
    return np.where(q<1/R,out+(1/R-q)-BETA*((1/R)**2-q*q)/2,out)

I=float(tail(0.))

def floor_cost(s,w):
    tw=np.where(w>=.5,(1-w)/BETA,R*np.exp(-2*w))
    x=np.minimum(s,tw)
    return I-tail(x)+(s-x)*w

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--n',type=int,default=400)
    args=parser.parse_args()
    # s is initial opposite-side cardinality, normalized by initial pool size.
    s=np.linspace(0.00001,3,args.n)
    v=np.linspace(0,1,args.n+1)
    r=1+np.maximum(0,s[:,None]/SLACK-1)*v
    cap=r*(BETA-tail(s[:,None]/r))
    lo=np.zeros_like(cap);hi=np.ones_like(cap)
    feasible_floor=I-tail(s[:,None])
    min_capacity_slack=float(np.min(cap-feasible_floor))
    for _ in range(42):
        mid=(lo+hi)/2
        below=floor_cost(s[:,None],mid)<=cap
        lo=np.where(below,mid,lo);hi=np.where(below,hi,mid)
    accumulated=np.trapezoid(1-lo,r,axis=1)
    profile=np.maximum(0,1-BETA*s+accumulated)
    result=dict(beta=float(BETA),base_integral=I,
                boosted_integral=float(np.trapezoid(profile,s)),
                minimum_capacity_slack=min_capacity_slack,
                grid=args.n, scope='Floating calculation; no theorem of improved hardness',
                samples=[dict(s=float(s[j]),boost=float(profile[j]),future_cost=float(accumulated[j]))
                         for j in [int((args.n-1)*q) for q in [0,.2,.4,.6,.8,1]]])
    (ROOT/'experiments'/f'profile-boost-{args.n}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    main()
