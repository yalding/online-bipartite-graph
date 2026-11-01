# Two-pool response analysis and a conditional trap

Session 4, 2026-11-01. The universal target remains unresolved. These results
analyze the candidate in `BOUNDARY_STATE.md`; no novelty claim is made.
The resulting stronger construction and its reweighted terminal interface
are stated separately in `COMPLETION_GAME.md`.

## 1. A lazy response retains the full power of an arbitrary algorithm

At a single new pool arrival, let the old pool weights be w_i, their current
coordinates be x_i, the new weight be b, and its neighborhood be N. After
choosing its new coordinate t, the minimal feasible old response is

    r_i(t) = max(x_i,1-t) if i is in N, and x_i otherwise.       (1)

This is a normal form, not an assumption that an algorithm has a scalar state.
Simulate any algorithm A internally. Use A's new coordinate as t, and perform
only (1) externally. Inductively, the external coordinates never exceed A's:
A's updated neighbors are at least 1-t, and its other coordinates cannot
decrease. The external cover is feasible, monotone, and no more expensive at
every public prefix. Future choices can still depend on the complete simulated
history. Apply this to deterministic fractional marginals for randomized
algorithms. For public whole-pool batch games, average within each pool first.

The threshold description is already present in Gamlath et al. (2019),
Section III; the useful additional point here is its application to the exact
continuation value, without imposing the Wang--Wong response function f.

## 2. Finite continuation values are convex polyhedral functions

Fix a discrete offline state and a finite remaining input menu/horizon. Let
V(x) be future increments minus B times the final offline optimum, with sunk
online cost excluded, as in equation (6) of `BOUNDARY_STATE.md`. Then

    V is convex and piecewise affine, and for x <= z,

    -sum_i w_i(z_i-x_i) <= V(z)-V(x) <= 0.                   (2)

The terminal value is constant in x. Inductively, a particular arrival has a
linear increment plus a maximum of convex continuation values, minimized over
a response polytope whose constraints are jointly linear in x and the response.
Partial minimization preserves convexity. The adversary's finite maximum,
including stopping and retirement choices, preserves convexity. Polyhedral
projection gives a finite piecewise-affine value; rational data give rational
planes.

For the right inequality in (2), simulate a strategy starting from x at the
higher initial coordinates z, using coordinatewise maxima externally. This
cannot increase future increments on any continuation. For the left inequality,
starting from x one can pay at most sum w_i(z_i-x_i) to simulate a strategy
starting from z when a future arrival actually occurs. A stop before that costs
nothing. Both comparisons hold uniformly over all graph paths; the adversary
may choose its path after seeing the responses.

For this argument one can extend the value to the whole coordinate cube by
enforcing only future constraints, treating all old constraints as already
satisfied. On physically feasible states this agrees with the real game;
monotonicity maintains all old edges. The extension permits the usual convex
analysis without asserting that every artificial coordinate vector has the
same sunk history cost.

Consequently V can be represented on the cube by finitely many supporting
planes whose slope on coordinate i lies in [-w_i,0]. Retirement is harmless:
pad a plane with zero slopes on retired coordinates. Taking a maximum over
retirement choices just collects their planes.

## 3. Every response step has a two-line exact certificate

Suppose the continuation after a new arrival has the representation

    V_next(r,t) = max_j [a_j + sum_i v_ji r_i + v_jn t],
    -w_i <= v_ji <= 0,  -b <= v_jn <= 0.                    (3)

The whole response objective is

    sum_i w_i(r_i-x_i) + b*t + V_next(r,t).

The coefficient of each old r_i in every plane of this objective is w_i+v_ji,
which is nonnegative. Thus replacing r by the minimal response (1) cannot
increase the objective. This also proves directly that proactive old raises
are unnecessary for this statewise minimax step.

Put d_ji=w_i+v_ji. Expanding each nonnegative positive-part term gives exactly

    H(t) = max_(j,S subset N) [c_jS + m_jS*t],               (4)

where

    c_jS = a_j - sum_i w_i*x_i
           + sum_(i in S) d_ji + sum_(i outside S) d_ji*x_i,
    m_jS = b + v_jn - sum_(i in S) d_ji.

The response value is min_(0<=t<=1) H(t). It suffices to consider the endpoints
and intersections of two lines in (4). There is an exact lower certificate:

* At an interior optimum, a zero-slope active line or a convex combination
  of two active lines with opposite slopes has slope zero and intercept H(t).
* At t=0, an active nonnegative slope certifies the answer; at t=1 use an
  active nonpositive slope.

Each expanded line is a valid lower bound on the full response objective:
use r_i>=1-t for i in S and r_i>=x_i for other i. Therefore this certificate
also handles unrestricted old responses, rather than just a sampled threshold
grid. With rational planes all arithmetic and the witness are rational.

This is the precise two-branch response reduction available at this checkpoint.
It does NOT say that arbitrary desired planes are realizable by graph
continuations, or that the original allocation-function minimax is necessary.
Graph realization and propagation of a strong enough envelope remain missing.

## 4. The nine phase choices have only three algebraic forms

Write the old interface as

    c0 + p(1-x_a) + q(1-x_c) + k(1-min(x_a,x_c)),

and let old pool weights be A,C. For each old selected subset Q, put

    g(Q) = sum_(i in Q) w_i + T_old(Q),
    h(R) = min_(Q superset R) g(Q).

Set h0=h(empty), alpha=h({a})-h0, gamma=h({c})-h0, and
kap=h({a,c})-h0. These are nonnegative, with

    max(alpha,gamma) <= kap <= alpha+gamma.

For new neighborhoods N_b,N_d in {{a},{c},{a,c}}, exact retirement is

    (T'_00,T'_10,T'_01,T'_11)
      = (h(N_b union N_d),h(N_d),h(N_b),h0).                 (5)

Up to exchanging labels, the resulting private/shared parameters are:

| Neighborhood pair | p' | q' | k' |
|---|---:|---:|---:|
| {a}, {c} | kap-gamma | kap-alpha | alpha+gamma-kap |
| {a}, {a} | 0 | 0 | alpha |
| {a}, {a,c} | 0 | kap-alpha | alpha |
| {a,c}, {a,c} | 0 | 0 | kap |

The other cases exchange a,c or b,d. In every case c0'=h0, including the old
c0 contribution. In particular every nonparallel phase leaves at most one
positive private parameter. For the parallel phase the shared parameter has
the explicit formula

    k' = [min(k,A-p) + min(k,C-q) - k]_+ <= k.              (6)

To check (6), subtract c0+p+q from the four g values; the remainder is
(k,A-p+k,C-q+k,A-p+C-q). Evaluating their relevant minima gives the formula.
If either A-p or C-q is negative, the positive part is zero. Otherwise split
according to whether each is below k. Thus parallel transport cannot amplify
the shared liability. Nested and shared phases can regenerate it, so (6) is
not an obstruction to the entire unequal-weight game.

Pool labels must be preserved even when their current neighborhoods coincide:
future phases can distinguish them. Comparator equivalence still does not
authorize replacing old vertices or forgetting sunk cost.

## 5. Equal-size batch phases have a 15/8 counterstrategy

In the alternating two-pool family, an actual quotient pool has at most two
neighbors in the preceding layer and two in the following layer. Hence its
quotient degree is at most four. For unit-size pools a known edge-arrival
algorithm gives fractional cover ratio 15/8. It is Algorithm 2 / Theorem 6 of
Buchbinder, Segev, and Tkach, *Online Algorithms for Maximum Cardinality
Matching with Edge Arrivals*, ESA 2017:
[primary proceedings PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol087-esa2017/LIPIcs.ESA.2017.22/LIPIcs.ESA.2017.22.pdf).

Here is an integer accounting of that algorithm for degree bound d. Put
D=2^d-1 and start each vertex's load z at zero. When an edge uv arrives, take
the largest power s of two not exceeding D-max(z_u,z_v), and add s to both
loads. The cover coordinate is z_v/2^d; assign matching weight s/D to the edge.

Before an incident edge arrives, at most d-1 powers have entered that vertex's
load. A sum of at most d-1 such powers cannot equal D: binary carrying would
require d ones to represent D. The load is bounded by D throughout, so a
positive s exists. Maximality gives 2s>D-max(z_u,z_v), whence after the update
z_u+z_v>=D+1=2^d. Thus the cover is feasible and monotone. The edge matching is
feasible because loads are at most D, and cover cost is exactly

    (2D/2^d) * matching value <= (2-2^(1-d))*OPT_fractional.

For d=4 this is 15/8=1.875, strictly below B. Process a newly revealed vertex's
edges in any fixed order to simulate edge arrivals. This is a cover upper
bound from an explicit online primal-dual construction, not an inference from
an arbitrary matching hardness theorem.

For announced equal-cardinality whole-pool batches, run the algorithm on the
quotient and assign its coordinate uniformly within each batch. Both online
and fractional offline costs scale by the common cardinality, so 15/8 holds
at every permitted batch stopping point. The same argument applies to the
still stronger version revealing both new pools together. This rules out the
equal-size specialization of that batch proof program.

Scope matters: this does NOT give a 15/8 bound for arbitrary unequal weights,
arbitrary splitting of pools, or unannounced sequential blowups that may stop
inside a batch. With unit-size pools it does cover every vertex prefix.
It also excludes adding unrestricted final private-leaf completions, which
can increase quotient degree above four. Those completions would be a change
to the restricted phase game, not an instance of this bound.

## 6. A finite conditional continuation already crosses the target

Consider a prefix K_20,20 whose old left coordinates have total at least 18.
Append a new left vertex v adjacent to all 20 old right vertices. Let its
assigned coordinate be t, and allow every possible proactive old raise.
There are two finite legal completions:

* R completion: attach one private leaf to each old right vertex. OPT=20,
  certified by its private matching and the cover R. Old left cost persists
  and lies outside the matching, as does v, so ALG>=38+t.
* L+v completion: attach private leaves to all 21 left vertices. OPT=21.
  Feasibility at v forces every old right coordinate to be at least 1-t;
  they lie outside this private matching, so ALG>=41-20t.

Choose these two completions with fixed probabilities 20/21 and 1/21. For
every response, including asymmetric ones,

    E ALG >= 801/21,  E OPT = 421/21,
    E ALG / E OPT >= 801/421 = 1.9026128266... > B.          (7)

The probabilities are independent of the response and random realization.
Alternatively the best response balances the normalized bounds at
t=22/421. If all old coordinates are 9/10, these bounds are attainable and
give the exact local minimax value, including the old-right persistent floor.

The qualification is essential: nothing forces an arbitrary algorithm to
reach the stipulated old-left cost. This is a conditional continuation, not
a universal 1.9026 lower bound (which would contradict the known upper bound).
The argument is a finite one-step private-leaf budget, subordinate to the
stronger multi-arrival deficits already used by Lu. Its role is to identify
the reachability obligation explicitly, not to claim a new lower constant.
These private leaves may touch earlier retired vertices, so (7) is a legal
continuation in the original model, not a move inside the strictly retired
two-pool game without an expressly added terminal-completion operation.

For general balanced K_m,m with old-left average x and one new pool of
relative size r=b/m, the same two normalized affine bounds meet at

    1 + (x+r)/(1+r+r^2).

For a hypothetical ratio 1+beta this gives the necessary cap

    x <= beta - (1-beta)*r + beta*r^2.

Optimizing r gives x<=beta-(1-beta)^2/(4*beta). This is a one-batch necessary
condition; repeated sequential arrivals yield stronger constraints. It is not
the missing extraction of a universal scalar f.

## Verification and remaining proof task

Run `python scripts/two_pool_response.py --lp-check`.
`experiments/two-pool-response.json` records 600 exact scalar-response
certificates, agreement with 600 unrestricted-response LPs, 9,216 exact phase
identities, and all local dyadic load pairs for degree bounds 1 through 6.
It also verifies 2,592 reweighted phase/terminal cases for the completion game
against direct cover enumeration on the actual graphs.
The response planes in this diagnostic are synthetic slope-bounded planes;
their certificates verify the elimination lemma, not graph realizability.
The phase checks are exact integer arithmetic. The dyadic argument above is
analytic; the finite checks are supplementary.

The next construction must generate a graph-realized convex continuation
envelope and propagate a strict positive surplus from a reachable initial
state. Equations (4)--(6) are concrete local operations for doing so. Neither
arbitrary supporting planes nor the conditional state in (7) may be assumed
available. Unequal sizes, or a carefully specified terminal-completion option,
are necessary changes to evade the equal-size restricted-game obstruction;
they have not been shown sufficient.
