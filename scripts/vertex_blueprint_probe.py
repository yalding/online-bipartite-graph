"""Small proper blueprints and a legal vertex-arrival cleanup experiment.

The cleanup retains a new edge only if at least one endpoint has not arrived.
Already retained edges can still be used as covering inequalities. Exact
rational accounting measures how much of the hidden-set forcing survives.
The MILP only proposes a blueprint; all properness checks are combinatorial.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.research-deps'))
import argparse,json
from fractions import Fraction
from itertools import product
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix

def find_blueprint(P=3,C=2,seconds=20):
    N=C**P
    candidates=[(p,a,b) for p in range(1,P+1) for a in range(N) for b in range(N)
                if a%(C**(P-p+1))!=b%(C**(P-p+1))]
    left=[[] for _ in range(N)];right=[[] for _ in range(N)]
    for j,(_,a,b) in enumerate(candidates):
        left[a].append(j);right[b].append(j)
    rr=[];cc=[];dd=[];ub=[]
    def row(indices,bound):
        i=len(ub)
        for j in indices:
            rr.append(i);cc.append(j);dd.append(1)
        ub.append(bound)
    for js in left+right:
        row(js,1)
    for j,(p,a,b) in enumerate(candidates):
        block=C**(P-p+1)
        for suffix in range(block):
            aa=a//block*block+suffix;bb=b//block*block+suffix
            row([j]+left[aa]+right[bb],2)
    A=coo_matrix((np.array(dd,dtype=float),(rr,cc)),shape=(len(ub),len(candidates))).tocsc()
    # Preserve maximum cardinality as primary objective, prefer later phases
    # among ties to avoid needless early exposure of the entire label set.
    objective=np.array([-1-p/(1000*P*N) for p,_,_ in candidates])
    result=milp(objective,integrality=np.ones(len(candidates)),
                bounds=Bounds(0,1),constraints=LinearConstraint(A,-np.inf,np.array(ub)),
                options=dict(time_limit=seconds,mip_rel_gap=0))
    if result.x is None:
        raise RuntimeError(result.message)
    selected=[e for x,e in zip(result.x,candidates) if x>.5]
    return selected,dict(message=result.message,objective_dual_bound=float(result.mip_dual_bound),
                         mip_gap=float(result.mip_gap),variables=len(candidates),constraints=len(ub))

def verify(P,C,edges):
    N=C**P
    l={a for _,a,_ in edges};r={b for _,_,b in edges}
    assert len(l)==len(r)==len(edges)
    for p,a,b in edges:
        block=C**(P-p+1)
        for suffix in range(block):
            assert not(a//block*block+suffix in l and b//block*block+suffix in r)
    return N

def shift(x,z,P,C):
    result=0;place=1
    for _ in range(P):
        result+=((x%C+z%C)%C)*place
        x//=C;z//=C;place*=C
    return result

def cleanup(P,C,edges):
    N=verify(P,C,edges)
    forced=Fraction(0);per_shift=[]
    for z in range(N):
        seen=set();retained=set();credit=Fraction(0);deleted=0
        for p,a,b in sorted(edges):
            block=C**(P-p+1)
            aa=shift(a,z,P,C)//block*block
            bb=shift(b,z,P,C)//block*block
            good=0
            for c in range(block):
                u,v=aa+c,N+bb+c
                if (u,v) in retained:
                    good+=1
                elif u not in seen or v not in seen:
                    retained.add((u,v));seen.update((u,v));good+=1
                else:
                    deleted+=1
            credit+=Fraction(good,block)
        hidden={shift(a,z,P,C) for _,a,_ in edges}|{N+shift(b,z,P,C) for _,_,b in edges}
        assert all(not(u in hidden and v in hidden) for u,v in retained)
        forced+=credit
        per_shift.append(dict(shift=z,forcing_credit=str(credit),retained_edges=len(retained),
                              illegal_edges_discarded=deleted))
    average=forced/N
    ratio=1+average/(2*(N-len(edges)))
    return dict(blueprint_value=str(Fraction(len(edges),N)),average_forced_hidden_weight=str(average),
                vertex_arrival_lower_bound=str(ratio),decimal_ratio=float(ratio),
                properness_verified=True,independence_verified_all_shifts=True,
                per_shift=per_shift)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--phases',type=int,default=3)
    p.add_argument('--alphabet',type=int,default=2)
    p.add_argument('--seconds',type=int,default=20)
    args=p.parse_args()
    edges,solver=find_blueprint(args.phases,args.alphabet,args.seconds)
    result=cleanup(args.phases,args.alphabet,edges)
    result.update(phases=args.phases,alphabet=args.alphabet,edges=edges,solver=solver,
                  scope='Small blueprint cleanup experiment; not an improved universal bound')
    target=ROOT/'experiments'/f'vertex-blueprint-P{args.phases}-C{args.alphabet}.json'
    target.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='per_shift'},indent=2),flush=True)

if __name__=='__main__':
    main()
