"""Exact-to-high-precision evaluation of center-last stars for GreedyAllocation.

Run from any directory. Uses mpmath (a dependency of SymPy).
This is algorithm-specific tightness, not a lower bound against all algorithms.
"""
from pathlib import Path
import json
import mpmath as mp

mp.mp.dps = 70
ROOT = Path(__file__).resolve().parents[1]
K = mp.findroot(lambda k: k - mp.coth(k), (mp.mpf('1.1'), mp.mpf('1.3')))
A = (K + 1) / 2
B = (K - 1) / 2

def allocation(z):
    z = mp.mpf(z)
    return (A-z)**(A/K) * (z+B)**(B/K)

def water_level(degree):
    """Unique solution d*t=f(t); f is decreasing and positive."""
    left, right = mp.mpf(0), mp.mpf(1)
    for _ in range(250):
        middle = (left+right)/2
        if degree*middle < allocation(middle):
            left = middle
        else:
            right = middle
    return (left+right)/2

def main():
    beta = 1 + allocation(0)
    rows = []
    for degree in [1, 2, 5, 10, 100, 1000, 10000, 1000000]:
        t = water_level(degree)
        cost = 1 + (degree-1)*t
        assert abs(degree*t-allocation(t)) < mp.mpf('1e-65')
        assert 0 < t < 1
        assert cost <= beta
        rows.append(dict(leaves=degree, water_level=str(t), center_potential=str(1-t),
                         cover_cost=str(cost), optimum=1, gap_to_beta=str(beta-cost)))
        print(f'd={degree:8d}  ALG/OPT={float(cost):.12f}  gap={float(beta-cost):.6g}')
    result = dict(k=str(K), f0=str(allocation(0)), beta=str(beta),
                  matching_ratio=str(1/beta), rows=rows,
                  scope='Specific GreedyAllocation algorithm; not universal hardness')
    (ROOT/'experiments'/'star-tightness.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    # A finite, explicit graph with no stored quadratic adjacency matrix.
    degree = 1000
    instance = dict(description='Leaves 0..999 arrive isolated; center 1000 arrives last.',
                    model='unweighted bipartite vertex arrivals',
                    arrival_order=list(range(degree+1)),
                    left_vertices=list(range(degree)), right_vertices=[degree],
                    edges=[[u,degree] for u in range(degree)],
                    optimal_cover=[degree])
    (ROOT/'experiments'/'center-last-star-1000.json').write_text(json.dumps(instance,indent=2),encoding='utf-8')
    print('k =',mp.nstr(K,30),'beta =',mp.nstr(beta,30))

if __name__ == '__main__':
    main()
