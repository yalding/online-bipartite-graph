"""Sparse public-prefix LP for prescribed twin-group adversaries.

Float solves are discovery tools. A rationalized dual is verified separately
before its objective is called a rigorous lower bound. Public batch sizes make
the algorithm stronger than ordinary sequential arrivals.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.research-deps'))
import argparse
import hashlib
import gzip
from functools import lru_cache
import json
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

ROOT=Path(__file__).resolve().parents[1]

def public_prefixes(paths):
    nodes={}
    for path in paths:
        for k in range(1,len(path)+1):
            prefix=tuple((int(s),tuple(ns),int(w)) for s,ns,w in path[:k])
            nodes[prefix]=None
    return sorted(nodes,key=lambda x:(len(x),x))

def complete_bipartite_phase_paths(root=30,step=1,limit=60,alternations=2):
    """All phase lengths 1..limit, changing side at most alternations times.

    First phase is R arrivals after an initial isolated L pool. Every phase
    has the same length cap. All group-to-group opposite edges are present.
    """
    paths=[]
    initial=((0,(),root),)
    def grow(prefix,side,remaining):
        current=prefix
        for _ in range(limit):
            neighbors=tuple(i for i,(s,_,_) in enumerate(current) if s!=side)
            current=current+((side,neighbors,step),)
            if remaining>1:
                grow(current,1-side,remaining-1)
        paths.append(current)
    grow(initial,1,alternations)
    return public_prefixes(paths)

def pool_tree_prefixes(depth=6,sizes=(1,4),root_size=4,parents='root-last'):
    root=((0,(),root_size),)
    nodes=[root]; frontier=[root]
    for _ in range(depth-1):
        next_frontier=[]
        for p in frontier:
            choices=range(len(p)) if parents=='all' else sorted(set([0,len(p)-1]))
            if parents=='chain':
                choices=[len(p)-1]
            for parent in choices:
                for size in sizes:
                    next_frontier.append(p+((1-p[parent][0],(parent,),size),))
        nodes.extend(next_frontier);frontier=next_frontier
    return nodes

def adaptive_biclique_prefixes(root=100,mesh=10,phases=5,targets=(1.0,1.5,2.0)):
    """Alternating phases with step proportional to the fixed opposite side.

    Switches are allowed at prescribed side-size ratios. The algorithm can
    stop after any group, and continuation budgets attach to every prefix.
    """
    paths=[]
    def grow(prefix,side,remaining):
        own=sum(w for s,_,w in prefix if s==side)
        other=sum(w for s,_,w in prefix if s!=side)
        step=max(1,other//mesh)
        current=prefix
        for target in sorted(set(int(round(t*other)) for t in targets)):
            if target<=own:
                continue
            while own<target:
                size=min(step,target-own)
                ns=tuple(v for v,(s,_,_) in enumerate(current) if s!=side)
                current=current+((side,ns,size),)
                own+=size
            if remaining>1:
                grow(current,1-side,remaining-1)
        paths.append(current)
    grow(((0,(),root),),1,phases)
    return public_prefixes(paths)

def mixed_neighborhood_prefixes(depth=7,sizes=(1,4),root=4):
    """Alternate colors; connect to all, earliest, or latest opposite pool."""
    initial=((0,(),root),)
    nodes=[initial];frontier=[initial]
    for length in range(1,depth):
        side=length%2
        new=[]
        for p in frontier:
            opposite=tuple(v for v,(s,_,_) in enumerate(p) if s!=side)
            choices=sorted(set([opposite,(opposite[0],),(opposite[-1],)]))
            for ns in choices:
                for size in sizes:
                    new.append(p+((side,ns,size),))
        nodes.extend(new);frontier=new
    return nodes

def general_pool_prefixes(depth=5,sizes=(1,4),root=4):
    initial=((0,(),root),)
    nodes=[initial];frontier=[initial]
    for length in range(1,depth):
        new=[]
        for path in frontier:
            choices=sorted(set([(0,),(length-1,),tuple(range(length)),tuple(sorted(set([0,length-1])))]))
            for ns in choices:
                for size in sizes:
                    new.append(path+((0,ns,size),))
        nodes.extend(new);frontier=new
    return nodes

@lru_cache(maxsize=100000)
def fractional_optimum_twice(weights,edges):
    """Exact fractional-cover optimum after checking a half-integral LP pair."""
    if not edges:return 0
    rows=[];cols=[]
    for i,(u,v) in enumerate(edges):rows.extend([i,i]);cols.extend([u,v])
    A=coo_matrix((-np.ones(len(rows)),(rows,cols)),shape=(len(edges),len(weights))).tocsr()
    result=linprog(weights,A_ub=A,b_ub=-np.ones(len(edges)),bounds=(0,None),method='highs')
    if not result.success:raise RuntimeError(result.message)
    y=np.rint(2*result.x).astype(np.int64)
    dual=np.rint(-2*result.ineqlin.marginals).astype(np.int64)
    assert np.all(y>=0) and np.all(dual>=0)
    assert all(y[u]+y[v]>=2 for u,v in edges)
    loads=np.zeros(len(weights),dtype=np.int64)
    for lam,(u,v) in zip(dual,edges):loads[u]+=lam;loads[v]+=lam
    assert all(load<=2*w for load,w in zip(loads,weights))
    cost=sum(int(w)*int(v) for w,v in zip(weights,y))
    assert cost==sum(map(int,dual))
    return cost

def induced_fractional_optimum_twice(prefix,omit=0):
    kept=[v for v in range(len(prefix)) if not(omit>>v&1)]
    index={v:i for i,v in enumerate(kept)}
    weights=tuple(prefix[v][2] for v in kept)
    edges=tuple((index[u],index[v]) for v in kept for u in prefix[v][1] if u in index)
    return fractional_optimum_twice(weights,edges)

def minimal_covers(prefix):
    n=len(prefix)
    adj=[0]*n
    for v,(_,ns,_) in enumerate(prefix):
        for u in ns:
            adj[u]|=1<<v;adj[v]|=1<<u
    for mask in range(1<<n):
        if any(not(mask>>v&1) and adj[v]&~mask for v in range(n)):
            continue
        if any((mask>>v&1) and not(adj[v]&~mask) for v in range(n)):
            continue
        yield mask

def mincover(prefix):
    sides={s for s,_,_ in prefix}
    if len(sides)<2:
        return 0
    # Detect complete bipartite quotient for the main experiments.
    if all(tuple(ns)==tuple(u for u in range(v) if prefix[u][0]!=s)
           for v,(s,ns,_) in enumerate(prefix)):
        return min(sum(w for s,_,w in prefix if s==side) for side in (0,1))
    # Tree quotient: linear-time weighted vertex-cover DP.
    if all(len(ns)<=1 for _,ns,_ in prefix):
        inc=[w for _,_,w in prefix]; out=[0]*len(prefix)
        for v in reversed(range(len(prefix))):
            ns=prefix[v][1]
            if ns:
                u=ns[0]
                inc[u]+=min(inc[v],out[v]);out[u]+=inc[v]
        return sum(min(inc[v],out[v]) for v in range(len(prefix)) if not prefix[v][1])
    # General bipartite quotient, weighted min-cut through an integral max flow.
    from scipy.sparse.csgraph import maximum_flow
    n=len(prefix); source=n; sink=n+1
    rr=[];cc=[];dd=[]
    inf=sum(w for _,_,w in prefix)+1
    for v,(side,ns,w) in enumerate(prefix):
        rr.append(source if side==0 else v)
        cc.append(v if side==0 else sink);dd.append(w)
        for u in ns:
            assert prefix[u][0]!=side
            l,r=(u,v) if side==1 else (v,u)
            rr.append(l);cc.append(r);dd.append(inf)
    cap=coo_matrix((np.array(dd,dtype=np.int64),(rr,cc)),shape=(n+2,n+2)).tocsr()
    return int(maximum_flow(cap,source,sink).flow_value)

def build(nodes,extension_budgets=False,cover_extensions=False,fractional=False,subset_budgets=False):
    ids={p:i for i,p in enumerate(nodes)}
    offsets=[];variables=1
    for p in nodes:
        offsets.append(variables);variables+=len(p)
    rr=[];cc=[];dd=[];rhs=[];labels=[]
    def add(entries,b,label):
        row=len(rhs)
        for col,value in entries:
            if value:
                rr.append(row);cc.append(col);dd.append(value)
        rhs.append(b);labels.append(label)
    for i,p in enumerate(nodes):
        start=offsets[i]
        if len(p)>1:
            parent=offsets[ids[p[:-1]]]
            for v in range(len(p)-1):
                add([(parent+v,1),(start+v,-1)],0,('monotone',i,v))
        # Old edge inequalities are inherited by coordinatewise monotonicity.
        v=len(p)-1
        for u in p[v][1]:
            add([(start+u,-1),(start+v,-1)],-1,('cover',i,u,v))
        if fractional:
            opt2=induced_fractional_optimum_twice(p)
            add([(start+v,2*w) for v,(_,_,w) in enumerate(p)]+[(0,-opt2)],0,('fractional_cost',i,opt2))
        else:
            opt=mincover(p)
            add([(start+v,w) for v,(_,_,w) in enumerate(p)]+[(0,-opt)],0,('cost',i,opt))
        if extension_budgets:
            # Valid only for complete-bipartite prefixes. Each constraint has
            # an explicit finite universal-neighbor continuation certificate.
            assert all(tuple(ns)==tuple(u for u in range(v) if p[u][0]!=s)
                       for v,(s,ns,_) in enumerate(p))
            for side in (0,1):
                other=sum(w for s,_,w in p if s!=side)
                add([(start+v,w) for v,(s,_,w) in enumerate(p) if s==side]+[(0,-other)],
                    -other,('extension',i,side,other))
        if cover_extensions:
            for mask in minimal_covers(p):
                weight=sum(w for v,(_,_,w) in enumerate(p) if mask>>v&1)
                add([(start+v,w) for v,(_,_,w) in enumerate(p) if not(mask>>v&1)]+[(0,-weight)],
                    -weight,('private_leaves',i,mask,weight))
        if subset_budgets:
            # Single-vertex subsets are the initial non-bipartite pilot.
            for v in range(len(p)):
                mask=1<<v;weight=p[v][2]
                tau2=induced_fractional_optimum_twice(p,mask)
                add([(start+u,2*w) for u,(_,_,w) in enumerate(p) if u!=v]+[(0,-2*weight-tau2)],
                    -2*weight,('subset_private',i,mask,weight,tau2))
    A=coo_matrix((np.array(dd,dtype=np.int64),(rr,cc)),shape=(len(rhs),variables)).tocsr()
    b=np.array(rhs,dtype=np.int64)
    c=np.zeros(variables);c[0]=1
    return c,A,b,labels,offsets

def solve(nodes,extension_budgets=False,cover_extensions=False,seconds=60,fractional=False,subset_budgets=False):
    c,A,b,labels,offsets=build(nodes,extension_budgets,cover_extensions,fractional,subset_budgets)
    bounds=[(0,2)]+[(0,1)]*(len(c)-1)
    result=linprog(c,A_ub=A,b_ub=b,bounds=bounds,method='highs',options={'time_limit':seconds})
    if not result.success:
        raise RuntimeError(result.message)
    residual=float(np.max(A@result.x-b))
    assert residual<1e-7
    return result,dict(prefixes=len(nodes),variables=len(c),constraints=len(b),
                       ratio=float(result.fun),max_primal_residual=residual,
                       extension_budgets=extension_budgets,
                       cover_extensions=cover_extensions,
                       fractional=fractional,subset_budgets=subset_budgets,
                       status='Floating LP value; no exact dual certificate yet'),(c,A,b,labels,offsets)

def evaluate_dual(multipliers,problem,scale=10**9):
    """Exact weak-duality bound, allowing residuals via known variable caps.

    For lambda>=0, x>=0, A*x<=b, x<=U:
    c*x >= -lambda*b + sum_j U_j*min(0,c_j+(A^T lambda)_j).
    Integer arithmetic verifies this even when rounded multipliers are not
    dual-feasible. U_0=2 and all potential caps equal 1.
    """
    c,A,b,labels,offsets=problem
    assert multipliers.dtype==np.int64 and len(multipliers)==len(b)
    assert np.all(multipliers>=0)
    # Prove all subsequent signed int64 sums cannot overflow.
    maximum_row_sum=int(np.max(np.asarray(abs(A).sum(axis=1)).ravel()))
    bound=sum(int(x) for x in multipliers)*max(1,maximum_row_sum,int(np.max(np.abs(b))))
    assert bound+scale<2**60
    slack=np.asarray(A.T@multipliers).ravel()
    slack[0]+=scale
    correction=int(np.minimum(slack,0).sum())+min(0,int(slack[0]))
    numerator=-int(multipliers@b)+correction
    rational=Fraction(numerator,scale)
    return dict(lower_bound=str(rational),decimal=float(rational),
                numerator=numerator,denominator=scale,negative_slack_correction=correction,
                exact_integer_weak_duality=True)

def certify_dual(result,problem,scale=10**9):
    multipliers=np.maximum(0,np.floor(-result.ineqlin.marginals*scale)).astype(np.int64)
    return evaluate_dual(multipliers,problem,scale),multipliers

def normalized_dual(multipliers,problem):
    """Exact dual lower bound without a cap on the competitive ratio.

    Normalize cost-row multipliers by their weighted OPT sum. Repair negative
    potential-column slacks with multipliers of valid y_v<=1 constraints.
    """
    c,A,b,labels,offsets=problem
    assert np.all(multipliers>=0)
    bound=sum(map(int,multipliers))*max(1,int(np.max(np.asarray(abs(A).sum(axis=1)).ravel())),int(np.max(np.abs(b))))
    assert bound<2**60
    columns=np.asarray(A.T@multipliers).ravel()
    denominator=-int(columns[0])
    assert denominator>0
    repairs=np.maximum(0,-columns[1:])
    numerator=-int(multipliers@b)-int(repairs.sum())
    # The normalized competitive-ratio column equals -1; every potential
    # column is nonnegative after adding its upper-bound multiplier.
    assert np.all(columns[1:]+repairs>=0)
    value=Fraction(numerator,denominator)
    return dict(lower_bound=str(value),decimal=float(value),numerator=numerator,
                denominator=denominator,potential_cap_repair=int(repairs.sum()),
                exact_dual_feasibility=True,requires_ratio_cap=False)

def export_distribution(nodes,problem,multipliers,target):
    """Fixed rational distribution on finite, compressed unweighted inputs."""
    c,A,b,labels,offsets=problem
    instances=[];total=0;weighted_opt=Fraction(0)
    fractional_comparator=any(label[0]=='fractional_cost' for label in labels)
    for lam,label in zip(multipliers,labels):
        weight=int(lam)
        if not weight or label[0] not in ('cost','fractional_cost','extension','private_leaves','subset_private'):
            continue
        kind,node,*rest=label
        path=list(nodes[node])
        if kind=='cost':
            optimum=rest[0]
        elif kind=='fractional_cost':
            weight*=2
            optimum=Fraction(rest[0],2)
        elif kind=='extension':
            side,optimum=rest
            if optimum:
                path.append((side,tuple(v for v,(s,_,_) in enumerate(path) if s!=side),optimum))
        else:
            if kind=='subset_private':
                mask,cover_weight,tau2=rest
                weight*=2
                optimum=Fraction(2*cover_weight+tau2,2)
            else:
                mask,optimum=rest
            for v,(side,_,size) in enumerate(nodes[node]):
                if mask>>v&1:
                    path.append((1-side,(v,),size))
        if fractional_comparator:
            assert Fraction(induced_fractional_optimum_twice(tuple(path)),2)==optimum
        else:
            assert mincover(tuple(path))==optimum
        total+=weight;weighted_opt+=weight*optimum
        instances.append(dict(weight=weight,kind=kind,prefix_node=node,
                              optimum=str(optimum) if isinstance(optimum,Fraction) else optimum,groups=path))
    certificate=normalized_dual(multipliers,problem)
    assert weighted_opt==certificate['denominator']
    assert weighted_opt.denominator==1
    weighted_opt=int(weighted_opt)
    output=dict(probability_denominator=total,weighted_optimum_numerator=weighted_opt,
                fractional_comparator=fractional_comparator,
                expected_optimum=str(Fraction(weighted_opt,total)),
                certified_ratio=certificate,
                interpretation='Select each input with probability weight/probability_denominator. Expand each group into independent twins; listed cross-group adjacencies are complete.',
                public_information='Group sizes and labels may be revealed on batch arrival, strengthening the player.',
                instances=instances)
    with gzip.open(target,'wt',encoding='utf-8') as stream:
        json.dump(output,stream,separators=(',',':'))
    return dict(instances=len(instances),probability_denominator=total,
                certified_ratio=certificate['lower_bound'],file=str(target))

def signature(problem):
    c,A,b,labels,offsets=problem
    digest=hashlib.sha256()
    for array in [np.array(A.shape,dtype=np.int64),A.indptr,A.indices,A.data,b]:
        digest.update(np.asarray(array,dtype='<i8').tobytes())
    return digest.hexdigest()

def wang_wong_trajectory(nodes,problem):
    """Check a known globally competitive weighted algorithm against the LP."""
    c,A,b,labels,offsets=problem
    k=1.199678640257733833916369848641
    aa=(k+1)/2;bb=(k-1)/2
    def f(t):
        return (aa-t)**(aa/k)*(t+bb)**(bb/k)
    B=1+f(0)
    ids={p:i for i,p in enumerate(nodes)}
    x=np.zeros(len(c));x[0]=B
    for i,p in enumerate(nodes):
        start=offsets[i]
        v=len(p)-1
        if v:
            parent=offsets[ids[p[:-1]]]
            x[start:start+v]=x[parent:parent+v]
        _,ns,w=p[v]
        def excess(t):
            return sum(p[u][2]*max(0,t-x[start+u]) for u in ns)-w*f(t)
        if excess(1)<=0:
            t=1.
        else:
            lo=0.;hi=1.
            for _ in range(55):
                mid=(lo+hi)/2
                if excess(mid)<=0:lo=mid
                else:hi=mid
            t=(lo+hi)/2
        for u in ns:
            x[start+u]=max(x[start+u],t)
        x[start+v]=1-t
    residual=float(np.max(A@x-b))
    assert residual<1e-7, ('Known algorithm violates candidate constraints',residual)
    return dict(ratio=B,max_constraint_violation=residual,known_algorithm_feasible=True)

def generate(params):
    if params.get('family'):
        data=json.loads(Path(params['family']).read_text(encoding='utf-8'))
        return public_prefixes(data['paths'])
    if params.get('general'):
        return general_pool_prefixes(params['depth'],tuple(map(int,params['sizes'].split(','))),params['root'])
    if params.get('mixed'):
        return mixed_neighborhood_prefixes(params['depth'],tuple(map(int,params['sizes'].split(','))),params['root'])
    if params.get('adaptive'):
        return adaptive_biclique_prefixes(params['root'],params['mesh'],params['phases'],tuple(map(float,params['targets'].split(','))))
    if params.get('tree'):
        return pool_tree_prefixes(params['depth'],tuple(map(int,params['sizes'].split(','))),params['root'],params['parents'])
    return complete_bipartite_phase_paths(params['root'],params['step'],params['limit'],params['phases'])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--family',type=Path)
    parser.add_argument('--verify',type=Path,help='Verify saved JSON/NPZ certificate without optimizing')
    parser.add_argument('--seconds',type=int,default=60)
    parser.add_argument('--check-known',action='store_true')
    parser.add_argument('--export-yao',action='store_true')
    parser.add_argument('--tree',action='store_true')
    parser.add_argument('--general',action='store_true')
    parser.add_argument('--subset-budgets',action='store_true')
    parser.add_argument('--adaptive',action='store_true')
    parser.add_argument('--mixed',action='store_true')
    parser.add_argument('--mesh',type=int,default=10)
    parser.add_argument('--targets',default='1,1.5,2')
    parser.add_argument('--depth',type=int,default=6)
    parser.add_argument('--sizes',default='1,4')
    parser.add_argument('--parents',default='root-last',choices=['root-last','chain','all'])
    parser.add_argument('--root',type=int,default=10)
    parser.add_argument('--step',type=int,default=1)
    parser.add_argument('--limit',type=int,default=20)
    parser.add_argument('--phases',type=int,default=2)
    parser.add_argument('--extensions',action='store_true')
    parser.add_argument('--cover-extensions',action='store_true')
    parser.add_argument('--output',default='sparse-lp-latest')
    args=parser.parse_args()
    if args.verify:
        saved=json.loads(args.verify.read_text(encoding='utf-8'))
        nodes=generate(saved)
        problem=build(nodes,saved.get('extension_budgets',False),saved.get('cover_extensions',False),saved.get('fractional',False),saved.get('subset_budgets',False))
        if saved.get('matrix_sha256'):
            assert signature(problem)==saved['matrix_sha256']
        path=args.verify.with_name(args.verify.stem+'-dual.npz')
        with np.load(path,allow_pickle=False) as data:
            multipliers=data['multipliers']
        certificate=evaluate_dual(multipliers,problem,saved['certificate']['denominator'])
        assert certificate==saved['certificate']
        print('Independently verified:',certificate['lower_bound'],flush=True)
        print('Normalized dual:',normalized_dual(multipliers,problem),flush=True)
        if args.export_yao:
            target=args.verify.with_name(args.verify.stem+'-yao.json.gz')
            print('Fixed distribution:',export_distribution(nodes,problem,multipliers,target),flush=True)
        if args.check_known:
            print('Known algorithm:',wang_wong_trajectory(nodes,problem),flush=True)
        return
    params=vars(args).copy()
    params['family']=str(args.family.resolve()) if args.family else None
    nodes=generate(params)
    print('Generated',len(nodes),'prefixes',flush=True)
    result,summary,problem=solve(nodes,args.extensions,args.cover_extensions,args.seconds,args.general,args.subset_budgets)
    certificate,multipliers=certify_dual(result,problem)
    summary['certificate']=certificate
    summary['normalized_certificate']=normalized_dual(multipliers,problem)
    summary.update(root=args.root,step=args.step,limit=args.limit,phases=args.phases)
    summary.update(tree=args.tree,depth=args.depth,sizes=args.sizes,parents=args.parents)
    summary.update(adaptive=args.adaptive,mesh=args.mesh,targets=args.targets)
    summary['mixed']=args.mixed
    summary['general']=args.general
    summary['family']=params['family']
    summary['matrix_sha256']=signature(problem)
    if args.check_known:
        summary['known_algorithm_check']=wang_wong_trajectory(nodes,problem)
    summary['status']='Floating optimum plus exact rounded-dual lower bound'
    np.savez_compressed(ROOT/'experiments'/f'{args.output}-dual.npz',multipliers=multipliers)
    (ROOT/'experiments'/f'{args.output}.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':
    main()
