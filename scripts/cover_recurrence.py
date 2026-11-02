"""Reproduce Lu (arXiv:2608.09210), including a directed integer certificate.

The certificate proves a violation of the truncated continuous recurrence.
The paper's finite-witness argument is still needed to obtain graph instances.
The fast floating-point sweep is exploratory, not a rigorous certificate.
"""
from pathlib import Path
import argparse
import json
import math
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def grid(n, cutoff):
    a = np.arange(1, n*cutoff+1, dtype=np.int64)
    k = n*n//a
    valid = k < len(a)
    return a, k, valid

def floating(beta, n=12000, cutoff=2, max_depth=3000):
    a,k,valid = grid(n,cutoff)
    base = 1-beta*a/n
    d = np.maximum(0,base)
    # Endpoint/cell method, in floating point; infinity tail is discarded.
    for h in range(max_depth+1):
        integral = float(np.sum(d)/n)
        if integral > beta:
            return dict(beta=beta, depth=h, integral=integral, violation=True,
                        grid_per_unit=n, cutoff=cutoff, method='float, not certified')
        tail = np.r_[np.cumsum(d[::-1])[::-1],0.0]
        contribution = np.zeros_like(d)
        av,kv = a[valid],k[valid]
        contribution[valid] = (av*tail[kv+1]+d[kv]*(av*(kv+1)-n*n))/(n*n)
        d = np.maximum(0,base+contribution)
    return dict(beta=beta, depth=max_depth, integral=integral, violation=False,
                grid_per_unit=n, cutoff=cutoff, method='float, not certified')

def certified(p=82435,q=100000,n=24000,cutoff=2,max_depth=1200,scale=10**18):
    """Python arbitrary precision integers via NumPy object arrays.

    Every d_j/scale lower-bounds D_h on [j/n,(j+1)/n]. The update evaluates
    the raw operator at the right endpoint, then rounds DOWN. Before the
    first violation, monotonicity follows from integral(d_h)<=beta.
    Integral comparisons are exact integer comparisons.
    """
    started=time.monotonic()
    a,k,valid=grid(n,cutoff)
    ao=a.astype(object)
    # floor(scale*(1-p*a/(q*n))), including negative baselines.
    base=(scale*(q*n-p*ao))//(q*n)
    d=np.maximum(0,base)
    previous=None
    for h in range(max_depth+1):
        total=int(sum(d))
        denominator=scale*n
        record=dict(depth=h, integral_numerator=str(total),
                    integral_denominator=str(denominator), integral=total/denominator)
        if total*q > p*denominator:
            result=dict(beta_numerator=p,beta_denominator=q,grid_per_unit=n,cutoff=cutoff,
                        scale=str(scale), first_violation=record,previous=previous,
                        elapsed_seconds=time.monotonic()-started,
                        exact_integer_comparison=True,
                        scope='Truncated continuous recurrence; not an explicit graph')
            return result
        previous=record
        tail=np.concatenate((np.cumsum(d[::-1])[::-1],np.array([0],dtype=object)))
        increment=np.zeros(len(d),dtype=object)
        av,kv=ao[valid],k[valid]
        increment[valid]=(av*tail[kv+1]+d[kv]*(av*(kv+1)-n*n))//(n*n)
        updated=np.maximum(0,base+increment)
        # No monotonicity repair: if this fails, inspect the proof or discretization.
        assert all(updated>=d)
        assert all(updated[:-1]>=updated[1:])
        d=updated
        if h%100==0:
            print(f'cert depth={h} integral={total/denominator:.15f}',flush=True)
    raise RuntimeError('No violation within depth limit; no conclusion')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',action='store_true')
    args=parser.parse_args()
    if args.certificate:
        result=certified()
        output=ROOT/'experiments'/'lu-directed-certificate.json'
    else:
        result=[floating(beta) for beta in [0.707,0.75,0.78,0.80,0.81,0.82,0.824,0.8243,0.82435,
                                             math.sqrt(math.e)/2,0.83,0.9007616968738465]]
        output=ROOT/'experiments'/'lu-recurrence-sweep.json'
    try:
        output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    except PermissionError:
        pass
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    main()
