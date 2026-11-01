# Exact offline interfaces for a recursive pool adversary

Session 3, 2026-11-01. A mathematical state reduction, not a hardness theorem.
The target constant has not been reached.

Session-4 continuation: `TWO_POOL_RESPONSE.md` analyzes this game's response
steps and an equal-size batch obstruction. `COMPLETION_GAME.md` changes the
candidate by adding terminal private leaves and replacing T, for fixed-B
surplus purposes, by a reweighted table H that retains retired online cost.

## The information carried by a retired region

Use an integer-weighted bipartite quotient graph, realized by independent
twin groups of those cardinalities and complete bicliques. Let U be the
active boundary; retired vertices R will never receive new incident edges.
For each subset S of U define

    T(S) = minimum weight of selected retired vertices in a vertex cover
           whose selected boundary vertices are exactly S.

Boundary weights are excluded from T. Set T(S)=infinity if an edge inside
U is uncovered by S. The cover choosing every retired vertex is otherwise
available. Then the exact present offline optimum is

    OPT = min_(S subset U) [sum_(i in S) w_i + T(S)].          (1)

Bipartite weighted vertex cover is integral. For twin blowups the same
optimum follows directly: averaging any feasible cover within groups gives
a feasible quotient fractional cover with the same cost; conversely, any
quotient cover expands feasibly. This justifies (1) for the actual unweighted
graph and its fractional comparator.

## Exact fractional boundary extension

In fact T determines the entire fractional interface, not just its binary
endpoint values. Fix feasible boundary coordinates x in [0,1]^U. For
theta in (0,1), put

    S_theta(x) = {i in U intersect L: theta <= x_i}
                 union {j in U intersect R: theta > 1-x_j}.

If Phi(x) is the minimum retired fractional cost with boundary fixed to x,
then

    Phi(x) = integral_0^1 T(S_theta(x)) d theta.             (2)

Proof of >=: threshold-round any feasible fractional extension, selecting a
left vertex when theta<=its coordinate and a right vertex when theta>1-its
coordinate. Every edge is covered for almost every theta. Retired expected
cost equals its fractional cost, and each realized retired cover costs at
least T(S_theta).

Proof of <=: on each interval between consecutive boundary thresholds,
choose an optimal retired integral extension of that boundary state. Average
these covers over theta. Their boundary marginals are exactly x, feasibility
is preserved by averaging, and their retired expected cost is the right side.
There are finitely many intervals. This also gives a finite exact formula.

In particular, a single active vertex has an affine interface

    Phi(x) = (1-x) T(empty) + x T({root}).                   (3)

Two conditional costs suffice at a genuine single-vertex separator. With
several active pools the full interaction table is needed in general.

## A concrete failure of the all-out/all-in pair

Let active a,c have weight 2 each and lie on the same bipartition side.

* Shared history: one retired vertex b of weight 2 is adjacent to both a,c.
* Separate history: retired b_a,b_c of weight 1 each are adjacent only to
  a,c respectively.

All graphs are legal pool arrivals: a and c arrive isolated, followed by
the retired opposite groups. Both histories have retired total cardinality 2,
boundary weights (2,2), and the same two coarse conditional costs (2,0).
Their current optimum is 2. A feasible online state in both has a=c=0 and
all retired coordinates 1, so both can even have identical sunk online cost.

Their exact tables are different:

| Selected boundary S | Shared T(S) | Separate T(S) |
|---|---:|---:|
| empty | 2 | 2 |
| {a} | 2 | 1 |
| {c} | 2 | 1 |
| {a,c} | 0 | 0 |

Append a new group of weight 4 adjacent only to c. The shared graph's exact
optimum becomes 4, while the separate graph's becomes 3. Enumerating covers
verifies these values; all weights are integer group cardinalities. Thus
all-out/all-in data cannot distinguish future comparator costs even with the
same current optimum and online cost. This is an obstruction to a particular
state compression, not to every scalar inequality or every rooted recursion.

## Finite graph operations and exact retirement

For a new active pool j of weight b adjacent to N subset U on the opposite
bipartition side from j, add j to the
boundary and define

    T_plus(S) = T(S intersect U) if every new edge meets S,
                infinity otherwise.                       (4)

Every new edge is revealed on arrival of j, so the graph is legal. Next,
to retire D subset (U union {j}), keep W=(U union {j}) outside D and set

    T_new(S) = min_(Q subset D) [sum_(i in Q) w_i
                                 + T_plus(S union Q)].      (5)

Equation (5) retains all old edges, including edges joining a retired pool
to an active pool. It follows by partitioning any integral cover according
to its selected vertices in D. The retained graph is still bipartite.
For disconnected subgames tables can be added only when their retired
regions and unresolved boundary edges are accounted for consistently.

## A valid finite adversarial recurrence, before any continuum limit

Specify a finite menu of integer pool sizes, whole-pool neighborhoods, and
retirement choices; impose a horizon h on new pool arrivals. Work in the
stronger batch model, revealing each new pool and its entire size at once.
All subsequent neighborhoods treat an active pool as a whole, and no pool
may later be split.

For an arbitrary algorithm, average its coordinates within each pool.
Complete-biclique feasibility, monotonicity, and cost are preserved. Thus
the online boundary state is its vector x of pool averages. This argument
does not justify averaging if future continuations select individual twins.

It is harmless to strengthen the algorithm by informing it which pools have
retired. Raising a retired coordinate has no future feasibility benefit;
ignoring such raises only decreases cost. At fixed state (w,x,T), write
V_h for the largest surplus the adversary can force from future algorithmic
increments minus B times the final offline optimum. Current algorithm cost
is excluded; it is added back when testing the final surplus.

Let P(x;b,N) be the polytope of responses (x',t) with x'>=x,
0<=x',t<=1, and x'_i+t>=1 for i in N. The cost increment is

    Delta = sum_i w_i (x'_i-x_i) + b*t.

With V_0=-B*OPT(w,T), backward induction gives

    V_h(w,x,T) = max { -B*OPT(w,T),
        max_(b,N) inf_((x',t) in P(x;b,N))
             [ Delta + max_D V_(h-1)(w_W,(x',t)_W,T_new) ] }. (6)

T_new is (4)--(5); the retirement choice D can depend on the response.
All maxima range over the prescribed finite legal menus. To avoid any
irrelevant existence issue one may interpret each maximum as a supremum;
strict positive surplus suffices for a witness. Statewise backward induction
applies even when the actual algorithm uses its entire past history.
At the initial isolated pool, T=0, x=0, and current cost is zero. A strict
positive value in (6) would give a lower-bound witness for that finite game.

For randomized algorithms use the deterministic coordinatewise expectations
at public prefixes. Selecting actions using those marginals chooses a fixed
finite path depending on the algorithm's law, not its realized seed. This
does not automatically produce one distribution hard for every algorithm.

## An exact closed interface with two active pools on the same side

There is a useful compression beyond the general exponential table. Suppose
U={a,c} and both pools lie on the same bipartition side. Write T_00,T_10,
T_01,T_11 for the four costs. They obey

    T_00 >= T_10 >= T_11,   T_00 >= T_01 >= T_11,
    T_00 + T_11 <= T_10 + T_01.                            (7)

The first inequalities follow by selecting additional boundary vertices,
which only relaxes constraints. For the second, take optimal extensions
of boundary states 10 and 01. The union of their selected left vertices
together with the intersection of their selected right vertices is a cover;
the intersection on the left together with the union on the right is also
a cover. Their boundary states are 11 and 00. The sum of their retired costs
is unchanged, proving (7).

Define four nonnegative integers

    c0 = T_11,
    p = T_00-T_10,
    q = T_00-T_01,
    k = T_10+T_01-T_00-T_11.

Then (2) reduces exactly to

    Phi(x_a,x_c) = c0 + p(1-x_a) + q(1-x_c)
                       + k(1-min(x_a,x_c)).                (8)

Equivalently, for offline accounting the retired region can be represented
by a constant c0 and three opposite-side neighbors: weight p adjacent only
to a, weight q adjacent only to c, and weight k adjacent to both. A disjoint
retired edge of optimum c0 realizes the constant. Zero weights are omitted.
This is an equivalence of comparator costs, **not** permission to replace
the actual old graph during the online execution or discard its sunk cost.

This class closes under a genuine alternating phase. Add two new opposite-
side pools b,d, each adjacent to any nonempty subset of {a,c}; then retire
a,c. For each new selected-boundary subset S of {b,d}, let R(S) consist of
old pools adjacent to an unselected new pool. Exact retirement gives

    T_new(S) = min_(Q superset R(S))
                 [w_a*1_(a in Q)+w_c*1_(c in Q)+T_old(Q)]. (9)

Only four subsets Q are involved. The new boundary is again two pools on
one side, so (7)--(8) apply again. The phase choosing both neighborhoods
{a,c} contains a K_2,2 quotient cycle. Intermediate prefixes are evaluated
by (4) and (1); no late edge is introduced. The stronger batch version can
reveal the two new pools together, but an ordinary sequential proof must
respect their separate arrival decisions.

Thus a concrete direct-proof candidate can retain two active pool weights,
two online averages, these four offline parameters, and additive sunk
online cost. It needs no uncontrolled promotion of a history-specific
birth profile to a universal function. Equations (8)--(9) are exact closure
identities; no claim is made that this particular two-pool game is hard
enough or that its limiting value is B.

## What remains missing

Equation (6) is an exact finite recursion for the specified restricted game;
it has NOT been solved or shown to approach B. Its table can grow
exponentially with a general boundary. The two-pool closure above removes
that obstacle for one concrete family, but a surplus inequality reaching B
is still missing. Merely asserting a scalar response function
f, summing independent offline optima across an old biclique, or iterating
the original minimax expression does not establish that reduction.
