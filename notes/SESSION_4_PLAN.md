# Resume here after session 4

## Latest checkpoint: a stronger exact completion game, still no target proof

Read `SESSION_4_WORKING.md`, `COMPLETION_GAME.md`, and `TWO_POOL_RESPONSE.md`
first. The universal target and known interval are unchanged.

The equal-size, announced-batch specialization of the strictly retired
two-pool game has a 15/8 upper bound: its quotient degree is at most four.
This does not rule out arbitrary unequal pool sizes, unannounced partial
batches, or the stronger completion game described next.

The new candidate allows terminal private leaves even on phase-retired
vertices. For B=1+beta, their exact terminal surplus is

    A - tau_theta(G),  theta_i=w_i*(beta+y_i),

where A is sunk cost. A reweighted retired table H closes under the same
two-pool phase operation, using w_i*(beta+r_i) as each retiring pool's cost,
with r_i its actual coordinate at retirement. It has four nonnegative real
parameters and provides four graph-realized terminal supporting planes.
For this surplus game H can replace T, since private completion dominates
ordinary stopping. Retain witnesses for selected retired covers so every
terminal branch can be expanded to an actual graph. See equations (4)--(6)
of `COMPLETION_GAME.md` for the precise new game.

Every single-arrival response reduces to a scalar threshold without assuming
scalar algorithmic state. Finite continuation envelopes are convex and
polyhedral, and a response can be certified by at most two supporting lines.
The synthetic plane checks establish this calculation, not graph realization.

A conditional K_20,20 trap crosses B, with exact local value 801/421, but
requires old-left cost at least 18. There is no argument forcing every
algorithm into that state. Do not report this as a universal lower bound.

**Next proof obligation:** propagate a graph-realized continuation envelope
through the new reweighted phase updates and force positive initial surplus,
or prove a below-B upper strategy for this family and change the construction.
The new game's value has not been computed or shown to reach B. Do not
substitute arbitrary planes, an assumed reachable state, or the original
allocation-function minimax for that missing argument.

Verification: `python scripts/two_pool_response.py --lp-check` passed 600
exact response certificates/independent LP comparisons, 9,216 phase
identities, and 2,592 reweighted phase/terminal cases against actual graphs.
The ninth PDF is Buchbinder--Segev--Tkach (ESA 2017), Algorithm 2 / Theorem 6;
its explicit online cover algorithm supplies the degree-four obstruction.

## Session-3 checkpoint retained for context

## Latest checkpoint: exact state, no matching lower-bound proof yet

Read `SESSION_3_WORKING.md`, `CONSTRUCTION_OBSTRUCTIONS.md`, and
`BOUNDARY_STATE.md` before the older agenda below. The target and universal
interval are unchanged; the hypothesis has not been settled.

Two routes are now analytically ruled out for the target:

* The existing blueprint deletion cleanup always yields forests, including
  the private-leaf completion. The forest 11/6 upper bound applies at every
  scale. Do not resume its MILP search or its random-walk survival analysis
  as a route to 1.90076. Its forcing satisfies F <= (5/3)(n-m).
* Replacing each late edge by a private three-edge path has a 3/2 upper
  bound, including midway stopping prefixes. It preserves cycles but cannot
  transfer the desired hardness.

The direct proof program now has an exact state to try. For two active
pools a,c on one bipartition side, retired fractional comparator cost is

    c0 + p(1-x_a) + q(1-x_c) + k(1-min(x_a,x_c)),

where all four parameters are nonnegative integers. This is an offline
interface, not permission to replace old vertices or discard sunk cost.
Adding two opposite-side pools with neighborhoods among {a}, {c}, {a,c},
then retiring a,c, closes this class by a minimum over four binary states.
The legal game can contain K_2,2 cycles. Its finite surplus recurrence is
equation (6) of `BOUNDARY_STATE.md`; the phase update is equation (9).

**Next proof obligation:** derive a surplus inequality for a particular
choice of these phases that reaches the exact target, or find a structural
upper bound that falsifies this candidate and change the gadget. There is
no evidence yet that the two-pool game's value reaches B. Do not substitute
the original allocation-function minimax for this missing game analysis.
If a strict violation is found, make its graph, offline certificate, finite
discretization, and realization-oblivious quantifiers explicit.

Verification already completed: 4,080 exact fractional-interface cases,
1,040 retirement tables, 4,608 two-pool phases, 151,944 subdivision prefixes,
and all 60 shifts of saved cleanup examples. Reproduce with
`python scripts/construction_obstructions.py`. These checks support the
stated lemmas and do not solve the universal problem.

An eighth paper is now downloaded: Baligacs et al., arXiv:2608.24630v1,
with PDF/source hashes in `papers/manifest.json`. Its online forest bound
is 11/6; its separate incremental 3/2 theorem assumes future knowledge.

## Earlier agenda retained for context (superseded where indicated above)

## User's corrected objective: read this first

The user explicitly clarified that improving the lower bound is not the goal.
The target is a finite hardness construction approaching the exact
1.9007616968738465... bound against arbitrary online algorithms.
Follow `CONSTRUCTION_TARGET.md`: reverse-engineer a universal adversarial
recursion matching the original minimax tradeoff, and prove its graph realization,
offline comparator, finite limit, and obliviousness. This is a proposed proof
route, not a claim that the necessary reduction is already known.

Do not spend another session on larger LP families or infrastructure as ends in
themselves. Computation should test or falsify a candidate matching construction.
The older exploratory targets below are background and subordinate to this
objective. The prior complete plan is archived as `SESSION_2_PLAN.md`.

The user wants a serious attempt to settle universal fractional vertex-cover
optimality under general vertex arrivals. Continue mathematical work with regular
updates and persistent notes. The problem is NOT settled here, and this session
did not improve the known universal lower bound.

## Established; do not redo

- The particular Wang--Wong cover algorithm is tight on center-last stars:
  1.9007616968738465... . See STAR_TIGHTNESS.md.
- Tang (2026) settled fractional matching optimality. Direct transfer to cover
  hardness fails; RESEARCH_STATUS.md explains the paired objective identity.
- Lu (2026) gives the cover lower bound 1+sqrt(e)/2 = 1.824360635350064... .
  Its directed integer recurrence certificate is already reproduced.
- The unresolved interval remains [1.824360635350064...,1.900761696873847...].

## Read the session-2 notes first

1. PRIVATE_LEAF_BUDGET.md: every prefix cover C yields the necessary condition
   sum_(V outside C)y <= (B-1)|C|. For twin groups use cardinality-weighted sums.
2. PROFILE_AWARE_BOUND.md: accounting for max(birth weight,later forced floor)
   strengthens an initial-phase profile, but numerically stabilizes near
   integral 0.70266, below the 0.82436 budget. It has not crossed the bound.
3. VERTEX_BLUEPRINT_CLEANUP.md: deleting illegal old-old edges gives a valid
   vertex-arrival reduction with measurable loss of hidden-set forcing.
4. FINITE_DISTRIBUTIONS.md: explicit oblivious input distributions, exact dual
   certificates, and independent checks using only actual graph histories.
5. SESSION_2_WORKING.md: completed work and failed approaches.

## Next mathematical targets

A. Retain a real state, not only a universal birth profile.

The profile-aware operator has a history-specific input d and universal D.
Promoting the improved initial-phase d to a universal D is invalid: all old
opposite vertices could have arrived isolated. A successful recursion must
retain the current potential distribution, or another sufficient history state.
Try a monotone envelope indexed by two pool sizes and old potential distributions,
or two conditional offline-cover costs at a boundary. Derive finite recurrences
before taking limits. Verify any numerical violation by directed arithmetic.
The floating critical-profile experiment is not a general impossibility barrier.

B. Replace the ruled-out blueprint cleanup only if a genuinely different
legal construction avoids the obstructions in `CONSTRUCTION_OBSTRUCTIONS.md`.
The earlier suggestion to analyze cleanup survival on large structured
blueprints is withdrawn: its 11/6 upper bound is now proved.

D. Test the nonbipartite comparator carefully.

PRIVATE_LEAF_BUDGET.md now also proves, for every subset S,
sum_(outside S)y <= (B-1)|S| + B*tau_f(G-S). On bipartite graphs this is implied
by the older constraints and potential caps. On general graphs it can add
information. The first general-graph pilot had no odd-cycle advantage: its
extracted dual used only whole-cover private leaves. The sparse LP supports
--general and --subset-budgets and verifies every fractional comparator with
an exact feasible half-integral primal/dual pair. This is worth targeted
structured exploration, not indiscriminate enumeration of small graphs.

C. Keep the improved-algorithm direction open.

The optimum may be below 1.90076. A fixed f(y) wastes nearly f(0) on late-star
leaves. A more adaptive cover algorithm might use neighbor potential
distributions or conditional cheap covers. It must also handle repeated
arrivals and overlapping neighborhoods.

## Tools and environment

- sparse_adversary_lp.py: prescribed JSON paths, mixed neighborhoods, tree/pool
  and biclique phase families; exact dual repair; --verify; --export-yao;
  --check-known. New outputs include stable matrix hashes.
- check_yao_distribution.py: independently minimizes expected cost on the actual
  exported distribution, using no competitive-ratio or continuation constraints.
- profile_iterate.py and profile_boost.py: floating mathematical probes.
- vertex_blueprint_probe.py: small MILP proposals followed by exact properness,
  independence, and rational forcing checks. Solver bounds are not certificates.
- finite_adversary_lp.py: original small exact SymPy primal/dual solver.

SciPy 1.18.1 is installed locally in .research-deps. The new scripts prepend it.
NumPy, SymPy/mpmath, requests, and pypdf are already installed globally.
The directory is not a Git repository. No subagents or external messages have
been authorized. Eight PDFs and eight source archives are in the manifest.

## Results not to rediscover

Tree and mixed-neighborhood families gave about 1.65--1.67. Three-phase unit-step
bicliques gave about 1.76477. Five-phase adaptive bicliques gave about 1.78153.
All fall below the known 1.82436 universal lower bound. Larger explicit trees
became expensive; increasing depth alone is not a substitute for state compression.

Exact fixed distributions certify 1.764766778956... (624 inputs, 8--64 vertices)
and 1.781483997750... (480 inputs, 120--5,440 vertices). These are working
hardness examples, not literature improvements. The commands for independent
verification are in FINITE_DISTRIBUTIONS.md.

The original session-1 agenda is retained as SESSION_1_PLAN.md.
