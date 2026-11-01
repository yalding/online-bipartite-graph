# Two obstructions to transferring edge-arrival hardness

Session 3, 2026-11-01. These results eliminate two proposed constructions;
they do not settle the universal vertex-arrival hypothesis. No novelty claim.

## 1. The existing blueprint cleanup always produces a forest

The rule in `VERTEX_BLUEPRINT_CLEANUP.md` retains a distinct new edge only
when at least one endpoint is unintroduced. Such an edge either creates a
two-vertex component or attaches a new leaf to an old component. It never
joins two old vertices. Inductively, the retained simple graph is a forest.
Reusing an existing edge does not change this conclusion. Introducing unused
vertices as isolates and attaching private leaves also preserve it.

Baligacs et al., *Online and Incremental Fractional Vertex Cover on Trees*,
arXiv:2608.24630v1, Theorem 3, give an 11/6-competitive fractional cover
algorithm on forests, even under edge arrivals:
https://arxiv.org/html/2608.24630v1
Official proceedings: https://doi.org/10.4230/LIPIcs.ESA.2026.158 .
The vertex-arrival simulation runs that algorithm on each newly revealed edge.
Its rule only uses incident edge colors, so it needs no advance vertex inventory.
The paper's separate 3/2 result assumes knowledge of future edges and must not
be used here.

Consequently **no choice of proper blueprint or scale under the existing
cleanup rule can prove a lower bound above 11/6**. This is a structural
obstruction, stronger than the earlier unsuccessful small MILPs.

In the previous notation, each completed input has exact optimum 2(n-m):
the complement of the hidden independent set is a cover of that cardinality,
and its new private edges form a matching of that size. Apply the forest
algorithm to the fixed distribution. The forcing argument still gives

    E ALG >= 2(n-m) + F,
    E ALG <= (11/6) * 2(n-m).

Thus every such blueprint satisfies the analytic inequality

    F <= (5/3)(n-m).

If m/n -> 2/3, this implies limsup F/m <= 5/6. The target required about
0.90076, which is strictly larger than 5/6. This rules out the entire cleanup
route, including large structured random-walk blueprints.

This does NOT bound weighted tree quotients blown up into complete bicliques:
those expanded graphs can contain cycles. Nor does it bound arbitrary
vertex-arrival forests with weighted vertices using the unweighted theorem.

## 2. Replacing late edges by three-edge paths has a 3/2 upper bound

Consider the following different repair. Introduce all original vertices as
isolates. For each edge uv of an arbitrary original graph H, introduce two
fresh vertices a_e, b_e consecutively, revealing

    u--a_e, then a_e--b_e and b_e--v.

Every arrival is legal. Odd subdivision preserves bipartiteness if H is
bipartite, and it preserves cycles, so the forest obstruction does not apply.
Allow stopping at any vertex prefix, including after a_e.

Nevertheless this whole family has a deterministic integral 3/2-competitive
algorithm. It follows that it cannot force the target ratio even against
fractional algorithms. The algorithm knows the prescribed encoding protocol,
but does not know future edges or their endpoints.

Maintain a greedy matching M of the original edges and let C be its endpoints.
Original vertices receive weight 1 exactly when they enter C.

1. When a_e arrives adjacent to original u, set a_e=0 if u is in C, and
   a_e=1 otherwise.
2. When b_e arrives, its other old neighbor identifies v. If both u and v
   lie outside C, add uv to M and raise both original endpoints to 1.
3. Set b_e=1-a_e.

All assignments are monotone and integral. If a_e=0, u was already selected,
and b_e=1 covers its two edges. If a_e=1, u was outside C immediately before
this gadget. At its completion, either v was already selected or step 2
selects it. Thus b_e=0 is feasible. Each completed gadget costs exactly one
on its internal vertices. The selected original edges are disjoint.

After m completed gadgets, put k=|M|. The algorithm costs m+2k. Construct a
matching in the actual subdivided graph by taking the two outer edges from
each gadget corresponding to M and the middle edge from every other gadget.
This matching has size m+k: its original endpoints are disjoint because M
is a matching, and all internal vertices are private to their gadget.
Since k<=m,

    ALG = m+2k <= (3/2)(m+k) <= (3/2) OPT_fractional.

If the current prefix stops after a_e and u is already in C, no extra cost
has been incurred and the same certificate works. Otherwise the algorithm
cost is m+2k+1. The edge u--a_e is disjoint from the displayed matching,
because u is outside C. Therefore

    ALG = m+2k+1 <= (3/2)(m+k+1) <= (3/2) OPT_fractional.

Isolated original vertices cost zero. The proof handles every finite prefix,
both orientations of every encoded edge, and general original graphs.

For completeness, the offline identity for completed gadgets is

    tau_f(subdivided H) = m + tau_f(H).

With original endpoint values x_u,x_v, the minimum internal cost of a gadget
is max(1,2-x_u-x_v) = 1+[1-x_u-x_v]_+. For any fractional vector x on H,
repair the original edges one at a time by raising endpoints by the remaining
deficit. This costs at most the sum of their initial deficits. Hence
min_x (sum x + sum_e deficit_e)=tau_f(H), proving the identity. It is not
necessary to invoke this identity for the online upper bound above.

## Consequence for the construction program

Neither deleting illegal edges nor introducing one private three-edge path
per late edge can transfer the edge-arrival blueprint lower bound to the
desired vertex-arrival constant. A replacement must create shared constraints
using new vertices, and retain their conditional offline costs across phases.
`BOUNDARY_STATE.md` supplies an exact accounting method for such a recursion;
it does not yet supply a recursion reaching 1.9007616969.
