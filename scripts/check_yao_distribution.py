"""Independently optimize expected online cost for an exported input distribution.

This rebuilds only actual graph histories, edge feasibility and monotonicity.
It does NOT assume any competitive ratio or continuation-budget inequality.
The solve is numerical; the original distribution's lower certificate is exact.
"""
from pathlib import Path
import argparse,gzip,json,sys
from fractions import Fraction
from sparse_adversary_lp import public_prefixes,build,linprog,np,ROOT,mincover,induced_fractional_optimum_twice

def main():
    p=argparse.ArgumentParser()
    p.add_argument('distribution',type=Path)
    args=p.parse_args()
    with gzip.open(args.distribution,'rt',encoding='utf-8') as f:
        data=json.load(f)
    paths=[item['groups'] for item in data['instances']]
    nodes=public_prefixes(paths)
    fractional=data.get('fractional_comparator',False)
    base,A,b,labels,offsets=build(nodes,fractional=fractional)
    keep=[i for i,label in enumerate(labels) if label[0] in ('cover','monotone')]
    A=A[keep];b=b[keep]
    c=np.zeros(len(base))
    ids={path:i for i,path in enumerate(nodes)}
    denominator=data['weighted_optimum_numerator']
    for item in data['instances']:
        path=tuple((s,tuple(ns),w) for s,ns,w in item['groups'])
        if fractional:
            assert Fraction(induced_fractional_optimum_twice(path),2)==Fraction(item['optimum'])
        else:
            assert mincover(path)==item['optimum']
        node=ids[path]
        for v,(_,_,weight) in enumerate(path):
            c[offsets[node]+v]+=item['weight']*weight/denominator
    result=linprog(c,A_ub=A,b_ub=b,bounds=[(0,0)]+[(0,1)]*(len(c)-1),
                   method='highs',options={'time_limit':60})
    if not result.success:
        raise RuntimeError(result.message)
    target=data['certified_ratio']['decimal']
    assert result.fun>=target-1e-7
    report=dict(distribution=str(args.distribution),instances=len(paths),prefixes=len(nodes),
                optimal_expected_ratio=float(result.fun),certified_lower_ratio=target,
                max_primal_residual=float(np.max(A@result.x-b)),
                scope='Independent float optimization of actual inputs; no continuation-budget constraints')
    out=args.distribution.with_name(args.distribution.name.removesuffix('.json.gz')+'-check.json')
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
    main()
