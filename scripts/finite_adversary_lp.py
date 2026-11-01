"""Exact minimax LP for a finite family of ordered bipartite inputs.

One variable for each vertex at each distinct PUBLIC prefix enforces online
nonanticipation. Coordinates can increase along tree edges. Each public
prefix may be the stopping point. Randomized algorithms have feasible marginal
trajectories, so a certified LP lower bound also applies to randomized algorithms.

Default experiment: all rooted trees on at most n vertices where each arriving
vertex attaches to exactly one previous vertex. With --sizes, vertices represent
independent twin groups joined by complete bicliques, and the group size is
revealed on batch arrival. This strengthens the player, so its lower bound also
applies to sequential unweighted inputs. Its upper bound is only for that batch
game. This is a pilot family. Uses SymPy's rational simplex for small instances.
"""
from pathlib import Path
import argparse
import json
from sympy import Matrix
from sympy.solvers.simplex import linprog

ROOT=Path(__file__).resolve().parents[1]

def tree_prefixes(n,sizes=(1,),root_size=1):
    # Entry = (revealed side, earlier neighboring groups, group cardinality).
    root=((0,(),root_size),)
    nodes=[root]
    frontier=[root]
    for length in range(1,n):
        new=[]
        for prefix in frontier:
            for parent in range(length):
                for size in sizes:
                    new.append(prefix+((1-prefix[parent][0],(parent,),size),))
        nodes.extend(new)
        frontier=new
    return nodes

def optimum_cover(prefix):
    # A group represents independent twins; every quotient edge is blown up
    # to a complete biclique. An optimal cover can select entire groups.
    # Brute force is exact and cheap for the small number of groups here.
    edges=[(u,v) for v,(_,neighbors,_) in enumerate(prefix) for u in neighbors]
    return min(sum(size for v,(_,_,size) in enumerate(prefix) if mask>>v&1)
               for mask in range(1<<len(prefix))
               if all((mask>>u&1) or (mask>>v&1) for u,v in edges))

def build(nodes):
    index={}
    names=['competitive_ratio']
    for prefix in nodes:
        for v in range(len(prefix)):
            index[prefix,v]=len(names)
            names.append(f'y_node{nodes.index(prefix)}_v{v}')
    rows=[]; rhs=[]; labels=[]
    def constraint(entries,b,label):
        row=[0]*len(names)
        for j,value in entries:
            row[j]+=value
        rows.append(row); rhs.append(b); labels.append(label)
    for node_id,prefix in enumerate(nodes):
        for v in range(len(prefix)):
            j=index[prefix,v]
            constraint([(j,1)],1,f'upper_node{node_id}_v{v}')
            if v<len(prefix)-1:
                constraint([(index[prefix[:-1],v],1),(j,-1)],0,
                           f'monotone_node{node_id}_v{v}')
        for v,(_,neighbors,_) in enumerate(prefix):
            for u in neighbors:
                constraint([(index[prefix,u],-1),(index[prefix,v],-1)],-1,
                           f'cover_node{node_id}_{u}_{v}')
        optimum=optimum_cover(prefix)
        constraint([(index[prefix,v],prefix[v][2]) for v in range(len(prefix))]+[(0,-optimum)],0,
                   f'cost_node{node_id}_opt{optimum}')
    c=[1]+[0]*(len(names)-1)
    return Matrix(c),Matrix(rows),Matrix(rhs),names,labels

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--vertices',type=int,default=4)
    parser.add_argument('--sizes',default='1',help='Comma-separated positive twin-group cardinalities')
    parser.add_argument('--root-size',type=int,default=1)
    args=parser.parse_args()
    sizes=tuple(int(x) for x in args.sizes.split(','))
    assert min(sizes)>0 and args.root_size>0
    nodes=tree_prefixes(args.vertices,sizes,args.root_size)
    c,A,b,names,labels=build(nodes)
    print(f'prefixes={len(nodes)} variables={len(c)} constraints={len(b)}',flush=True)
    value,x=linprog(list(c),A,b)
    x=Matrix(x)
    assert all(v>=0 for v in x)
    assert all(v<=0 for v in A*x-b)
    assert (c.T*x)[0]==value
    # Independently obtain a dual witness, then verify it with exact arithmetic.
    dual_min,z=linprog(list(b),-A.T,c)
    z=Matrix(z)
    assert all(v>=0 for v in z)
    assert all(v<=0 for v in -A.T*z-c)
    assert -dual_min==value==-(b.T*z)[0]
    result=dict(family='Every twin group after the first connects completely to exactly one earlier group',
                maximum_groups=args.vertices,group_sizes=sizes,root_size=args.root_size,public_prefixes=len(nodes),
                exact_minimax_ratio=str(value), decimal_ratio=float(value),
                primal={names[i]:str(v) for i,v in enumerate(x) if v},
                dual={labels[i]:str(v) for i,v in enumerate(z) if v},
                exact_primal_and_dual_verified=True,
                model='Public twin-group batch arrivals; expands to unweighted bipartite graphs',
                transfer='Batch-game lower bound transfers to sequential inputs; batch-game upper bound need not',
                limitation='Small pilot family, not a tight bound for general vertex arrivals')
    suffix='' if sizes==(1,) and args.root_size==1 else '-sizes'+'-'.join(map(str,sizes))+f'-root{args.root_size}'
    target=ROOT/'experiments'/f'tree-adversary-lp-{args.vertices}{suffix}.json'
    target.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('Exact minimax ratio:',value,flush=True)

if __name__=='__main__':
    main()
