# An exact two-pool game with terminal private leaves

Session 4, 2026-11-01. This is a stronger concrete candidate construction,
not a proof of the target hardness. The missing obligation is a forcing
inequality from its initial state.

## Why change the previous game?

The strictly retired alternating two-pool game from `BOUNDARY_STATE.md` has a
15/8 counterstrategy when all pool cardinalities are equal and public. Its
quotient degree is at most four; see `TWO_POOL_RESPONSE.md`, Section 5. It is
therefore useful to add an operation that changes this family.

Permit a final private-leaf completion at any stopping prefix. A retired pool
receives no further *phase* edges, but may receive its private leaves in this
final operation. This protocol is public. It is a legal vertex-arrival
construction: all new edges have a new leaf endpoint. A pool quotient cycle
created during the phases persists. With unit-size pools the final quotient
degree can be five, so the former degree-four upper bound no longer applies.
The same dyadic method at degree five gives 31/16, above the target; this is
only removal of an obstruction, not evidence that the new game reaches B.

The previous offline table alone cannot evaluate these terminal choices:
their payoff depends on old coordinates of retired vertices. A reweighted
interface retains exactly the needed information.

## The graph-realized terminal payoff

Fix a proposed ratio B=1+beta, beta>0. At a bipartite pool-graph prefix G,
let w_i be pool cardinalities and y_i the present monotone coordinates.
Let A=sum_i w_i*y_i be sunk cost. For any integral quotient cover C, append
an equal-size private twin group for each pool in C, adjacent only to it.

The resulting graph has exact fractional optimum w(C): selecting C is an
upper certificate and its private perfect matchings give a lower certificate.
The minimum possible extra online cost, from this state, is exactly

    w(C) - sum_(i in C) w_i*y_i.

Every private pair must pay its full cardinality; equality is achievable by
raising all pools in C to one and assigning their new leaves zero. Thus the
minimum final competitive surplus is exactly

    A - sum_(i in C) w_i*(beta+y_i).

Define positive weights

    theta_i = w_i*(beta+y_i).

The adversary's best terminal completion has exact minimized surplus

    A - tau_theta(G),                                     (1)

where tau_theta is the minimum theta-weight integral cover of the old graph.
This also equals its fractional minimum because the quotient is bipartite.
The minimizing weighted cover identifies which actual old pools receive
leaves. An optimizing table entry must retain a witness cover or backpointer
for this realization; it does not authorize graph replacement.

Completion dominates ordinary stopping. An original minimum cover C* has
w(C*)=OPT_fractional(G), and y_i<=1 implies

    tau_theta(G) <= sum_(i in C*) theta_i <= B*OPT(G).

Therefore A-tau_theta(G)>=A-B*OPT(G). For a lower-bound construction with
this terminal option one can restrict stopping to private-leaf completions.

## Four parameters still suffice at a two-pool boundary

Let U={a,c} be the active pools, on the same side. Retired coordinates are
frozen until the final completion. This loses no algorithmic power: a lazy
simulation postpones every gratuitous retired raise until an incident leaf
actually arrives. Let R be the retired region and define

    H(S) = min sum_(i in selected retired pools) theta_i
           over covers of G selecting exactly S in U.     (2)

Active theta weights are excluded from H. Its four entries satisfy the same
monotonicity and same-side inequality as the ordinary offline table:

    H00>=H10,H01>=H11,  H00+H11<=H10+H01.

These follow from relaxing boundary selection and the union/intersection
cover argument; it holds for all positive real theta weights. Consequently
there are four nonnegative real parameters

    c=H11, p=H00-H10, q=H00-H01,
    k=H10+H01-H00-H11.

The retired fractional interface is

    c+p*(1-z_a)+q*(1-z_c)+k*(1-min(z_a,z_c)).

The z here are comparator boundary coordinates, not the online y. The direct
terminal formula uses just the four binary entries:

    tau_theta(G) = min {
        H00,
        theta_a+H10,
        theta_c+H01,
        theta_a+theta_c+H11 }.                             (3)

Hence, with sunk A excluded as in the earlier recurrence, the exact terminal
value is the following graph-realized convex envelope:

    W0(w,x,H) = max {
        -H00,
        -w_a*(beta+x_a)-H10,
        -w_c*(beta+x_c)-H01,
        -w_a*(beta+x_a)-w_c*(beta+x_c)-H11 }.               (4)

Every active-coordinate slope is either zero or minus its cardinality.
Unlike arbitrary synthetic planes, all four alternatives have an explicit
legal graph continuation with an exact offline certificate.

For this fixed-B surplus game H can REPLACE the old offline table T: ordinary
stopping is dominated, and every final comparator is certified by the selected
completion. One may retain T as an optional independent audit of prefix OPT.
It is not necessary to double the parameter count merely to evaluate (1).

## Exact phase update, including the dependence on the response

Add new opposite-side pools b,d with neighborhoods among {a},{c},{a,c}, then
retire a,c. Respect the two separate arrival decisions. At retirement let
r_a,r_c be their final online coordinates; they may have increased during
both arrivals. The new reweighted table is

    H_new(S) = min_(Q superset R(S)) [
        H_old(Q) + w_a*(beta+r_a)*1_(a in Q)
                 + w_c*(beta+r_c)*1_(c in Q) ],            (5)

where R(S) is the set of old neighbors of unselected new pools. The new
boundary weights are w_b,w_d and their current online coordinates. All
previously retired theta weights remain unchanged. Formula (5) follows by
partitioning selected old pools exactly as in ordinary table retirement.
No old edge is deleted, and the sunk cost A is updated by all actual
coordinate increments before retirement.

The phase algebra in `TWO_POOL_RESPONSE.md`, Section 4 applies with

    A_in_that_formula = w_a*(beta+r_a),
    C_in_that_formula = w_c*(beta+r_c),

and with p,q,k taken from H. These quantities now depend on the algorithm's
response. Substituting the original pool weights there would be incorrect.

Intermediate prefixes have a mixed-side boundary of at most three pools.
Adding a new pool sets H_plus(S)=H_old(S intersect U) when S covers all new
edges, and infinity otherwise. Include the new pool's theta weight only in
the minimization for its active selection. This evaluates a terminal
completion after the first arrival too; no decision may see the second
arrival before it is revealed.

## The finite recursive candidate

Choose finite integer menus of pool sizes, neighborhoods, and legal phase
retirements. Keep weights w, active coordinates x, reweighted table H, and
sunk A. The initial isolated pools have H identically zero, x=0, A=0.

Let W_h exclude sunk A, with W0 given by the negative weighted minimum-cover
formula above. For one new pool of weight b and neighborhood N, let

    Delta = sum_i w_i*(r_i-x_i)+b*t.

The exact finite game obeys

    W_h = max { W0,
        max_(b,N) inf_(feasible r,t) [
            Delta + max_(permitted retirements D)
                         W_(h-1)(w_new,x_new,H_new) ] }.   (6)

Here H_new uses reweighted retirement, with each retiring coordinate at its
actual updated value. Permitted actions must encode whether a phase's first
or second new pool is due. Lazy normal form reduces the player response to
one scalar t, with r_i=max(x_i,1-t) on neighbors. Its complete-history strategy
is not assumed to have a universal scalar response function. The convex
response calculation and two-line certificates in `TWO_POOL_RESPONSE.md`
can be applied to graph-realized continuation envelopes before retirement.

A strict positive initial value A+W_h would give a finite hard input. The
terminal cover witness then gives its exact comparator, and following only
deterministic marginals makes the chosen graph independent of the realized
random seed. As before, this quantifier argument gives an algorithm-dependent
fixed input, not automatically a single distribution hard for every algorithm.

## What this changes and what it does not establish

This changes the construction rather than merely trying larger instances of
the previous equal-size phase game. It supplies a graph-realized terminal
envelope and exact small-state updates, incorporates sunk online information
needed by the leaf continuations, and removes the particular degree-four
obstruction. The conditional 801/421 continuation in `TWO_POOL_RESPONSE.md`
is one example of these terminal operations exceeding B from a specified
state; reaching such a state remains the central issue.

No positive initial surplus at ratios approaching B has been proved or
computed for (6). No limiting differential inequality or finite
discretization attaining B is supplied. The universal hypothesis is still
unresolved. The next mathematical task is to find a graph-realized envelope
propagated by (5)--(6) that forces that surplus, or give an upper strategy
below B on this extended family and change the construction again.

Exact checks: `python scripts/two_pool_response.py --lp-check` compares
2,592 reweighted phase/terminal cases against direct cover enumeration on
the actual graphs. Its other response and phase checks are described in
`TWO_POOL_RESPONSE.md`. These support the identities, not the target theorem.
