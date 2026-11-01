# A general continuation constraint

Derived during session 2, 2026-11-01. No novelty claim is made: private-leaf
continuations are also used in the recent edge-arrival work. The point here
is a necessary condition applicable to every public vertex-arrival prefix.

Let a hypothetical algorithm be B-competitive on every finite input. At any
prefix graph G=(V,E), let y be its present fractional cover. For every integral
vertex cover C of G,

    sum_(v outside C) y_v <= (B-1) |C|.                         (PL)

Proof: append one fresh private leaf adjacent only to c for each c in C.
These edges are legal vertex arrivals. Their disjoint endpoint pairs cost at
least |C| in every fractional cover. Weight already on V\C persists and lies
outside all these pairs. Choosing C covers all old and new edges, and the
private edges certify that the offline optimum is exactly |C|. Thus the
algorithm's eventual cost is at least |C|+sum_(V\C)y_v, proving (PL).

For randomized algorithms take expectations coordinatewise; no branch needs
to see a realized random seed. If one constraint fails, its particular finite
private-leaf continuation is already a witness.

The quotient version for independent twin groups of integer cardinality w_v is

    sum_(v outside C) w_v y_v <= (B-1) sum_(v in C) w_v.

For each selected group introduce a new opposite group of the same cardinality
and connect it completely only to that selected group. Each such pair contains
a perfect matching. This is an unweighted graph blow-up, not an assumption that
arbitrary weighted instances have the same lower bound.

Only inclusion-minimal covers need testing: adding vertices to C decreases the
left side and increases the right side when B>=1. On a complete bipartite
prefix the only minimal covers are its two sides, recovering the continuation
budgets already used in the earlier proof. On nonhomogeneous graphs there are
other minimal covers and genuinely different inequalities.

An equivalent separation form is

    sum_v y_v <= min_(C a cover) sum_(v in C) (B-1+y_v).

For bipartite graphs the right side is a weighted minimum vertex cover and
can be computed by min-cut. For a twin-group quotient, multiply each summand
by its group cardinality.

## What this does not prove

These are necessary conditions for an algorithm competitive on every input.
Satisfying them at one prefix does not guarantee a competitive extension after
arbitrary future arrivals. The LP uses them as valid relaxations, with an actual
finite continuation attached to any violation. No improved universal constant
has yet followed from them in this project.

## Arbitrary subsets and the fractional comparator

There is a stronger version for a subset S which need not cover the old graph:

    sum_(v outside S) y_v <= (B-1)|S| + B*tau_f(G[V outside S]). (PLS)

Attach a private leaf to each v in S. In the final covering LP the new leaves
can be eliminated: each old v in S and its leaf cost at least 1, and setting
those old vertices to 1 is always optimal. The offline fractional optimum is
exactly |S|+tau_f(G[V outside S]). The online algorithm pays at least |S| plus
its persistent outside weight, proving (PLS). For twin groups multiply costs
by cardinality and attach an equal-size private group to each chosen group.

On bipartite graphs this adds no inequalities beyond (PL) and y_v<=1. Choose
an optimal integral cover D of G[V outside S]. Then S union D covers G, and

    sum_(V outside S)y
      <= sum_D y + (B-1)(|S|+|D|)
      <= (B-1)|S| + B*tau_f(G[V outside S]).

For general graphs the last identity between integral and fractional optima
fails, so (PLS) may add information. This suggests a separate nonbipartite
search, while keeping the comparator fractional throughout.

The first such pilot used 879 public prefixes on at most five twin groups,
with single-subset constraints and all minimal-cover constraints. Its floating
value is 1.6410256410; a verified normalized dual certifies 1.6410256338.
The extracted seven-input distribution uses only whole-cover private-leaf
completions, so it supplies no evidence of an odd-cycle improvement.

The implementation computes every fractional optimum using a primal/dual LP
pair, rounds the proposed pair to half-integers, and verifies both feasibility
and equal objectives in exact integer arithmetic. It does not infer an exact
offline optimum from a floating objective alone.
