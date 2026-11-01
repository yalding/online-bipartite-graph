# Resume here after session 2

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

B. Analyze a structured vertex-arrival blueprint.

Cleanup gives ratio 1+F/[2(n-m)], where m/n is blueprint value and F is expected
surviving forcing credit. If m/n tends to 2/3 and F/m tends to rho, the ratio
tends to 1+rho. Exceeding Lu needs rho>0.82436; reaching the original algorithm
needs rho near 0.90076. The structured random-walk blueprint paper is downloaded.
Do not infer asymptotic behavior from tiny time-limited MILPs. Derive its
cleanup survival probability, or design a replacement preserving hidden-set
symmetry while obeying vertex revelation.

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
been authorized. Seven PDFs and seven source archives are in the manifest.

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
