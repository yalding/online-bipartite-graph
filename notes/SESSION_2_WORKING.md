# Session 2 working notes: 2026-11-01

Objective: attempt to settle universal fractional vertex-cover optimality,
continuing from the first checkpoint. The problem remains unresolved here.

## Current plan

1. Test the omitted maximum between birth weights and later forced levels.
2. Add finite continuation constraints for arbitrary prefix covers.
3. Search sparse LPs on prescribed prefix trees with several scales and
   neighborhood patterns; turn approximate duals into rigorous lower bounds.
4. Use the resulting duals or policies to seek an analytic recurrence or
   improved algorithm. Report failures as failures, not evidence of optimality.

## Infrastructure completed

SciPy 1.18.1 was installed locally under `.research-deps` (not system-wide).
`scripts/sparse_adversary_lp.py` supports prescribed JSON paths, bipartite
multi-phase families, twin-pool tree families, and continuation constraints.
It preserves distinct public histories. Old edge constraints are inherited
through monotonicity rather than redundantly repeated at every descendant.

For approximate multipliers lambda>=0 and bounded primal variables 0<=x<=U,

    c*x >= -lambda*b + sum_j U_j min(0, c_j+(A^T lambda)_j).

The tool rounds multipliers to a common integer denominator, verifies the
right side in exact integer arithmetic, and pays for negative dual slacks.
Cover coordinates have cap 1; the competitive ratio may be restricted to cap 2
because a known 2-competitive algorithm exists. A globally competitive ratio
above 2 already exceeds every reported lower bound.

## Results so far

- Complete-bipartite prefixes, initial side 10, runs at most 20, two phases:
  floating minimax value 1.7458282187 (before dual certificate code was added).
- Initial side 20, runs at most 40, two phases: 1.7561295929, also floating.
- Initial side 6, runs at most 12, three phases: floating 1.7647678967;
  certified rounded-dual lower bound 1.764759524.
- Root/last-parent twin-pool trees, pool sizes 1 or 4, root size 4:
  depth 6 floating 1.6462395543, certified 1.646239524;
  depth 8 floating 1.6685446009, certified 1.668544541.

These are bounds for restricted adversarial families and are all below the
known universal lower bound. They are useful regressions, not improvements.

The first large LP redundantly repeated old edge inequalities and was stopped;
the more compact formulation then completed. No mathematical conclusion was
drawn from the interrupted solve.

## New useful lemma

See `PRIVATE_LEAF_BUDGET.md`: every old cover C imposes a budget on present
weight outside C. It generalizes the two-side budget to nonhomogeneous graphs.

## Leads requiring further work

The recent edge-arrival blueprint reduction also uses private leaves, but its
earlier matching batches may reveal edges between already-arrived vertices.
It cannot be imported without identifying a valid vertex-arrival replacement.
Primary source checked: https://arxiv.org/html/2608.04994v1 .

The common-denominator certificates now have an optimizer-independent integer
verifier. New solves save matrix hashes. Legacy solves are rebuilt from their
saved parameters and their multipliers checked against those rows.

## Final checkpoint for this session

- Proved the general private-leaf budget and tested it on nonhomogeneous pools.
- Derived the profile-aware initial-phase operator. At 800 cells its integral
  evolves `0.67272978 -> 0.70265158 -> 0.70266232`, then stabilizes numerically.
  There is no contradiction at the critical beta. See `PROFILE_AWARE_BOUND.md`.
- Added a legal vertex-arrival cleanup of edge blueprints with rational forcing
  accounting. Tiny probes do not improve the bound; some MILPs timed out with
  poor feasible proposals. Their solver bounds are not used as certificates.
- Five-phase adaptive bicliques gave floating minimax value 1.7815271108. An
  exact normalized dual certifies `1781280579/999885815 = 1.781483997750...`.
- Exported a fixed distribution on 480 inputs (120--5,440 vertices) at that
  ratio. The smaller three-phase family gives 624 inputs of 8--64 vertices,
  certifying `1764759524/999995889 = 1.764766778956...`.
- Rebuilt both actual input distributions without continuation constraints.
  Minimum expected-cost ratios were numerically 1.7815126870 and 1.7647672510,
  above the exact lower certificates.
- Checked the known weighted Wang--Wong algorithm against the candidate
  constraints on two larger families; no constraint violations were detected.
- Downloaded two further papers; there are now seven PDFs and source archives.

An initial array probe had an accidental broadcasting dimension and failed to
allocate; the saved script fixes its shape and uses a smaller grid. Two costly
explicit-prefix runs were interrupted without conclusions. These operational
failures are not mathematical counterexamples.

Nothing here narrows the universal interval. Useful assets are the valid
constraints/reductions, concrete oblivious inputs, and independent verification
pipeline. See `NEXT_SESSION.md` for the revised mathematical targets.

### Late additional check: nonbipartite inputs

Extended the private-leaf argument to arbitrary old subsets S with fractional
offline comparator: outside weight is at most `(B-1)|S|+B*tau_f(G-S)`.
On bipartite graphs this follows from the earlier cover constraints and caps;
on general graphs it may be stronger. Added exact primal/dual verification of
fractional offline optima to the sparse LP.

A five-pool general-graph family (879 prefixes) gave floating 1.6410256410 and
certified `1641025601/999999980 = 1.6410256338...`. Its seven-input distribution
was independently optimized, giving 1.6410256408. Its support used only whole
cover completions on bipartite underlying graphs, so no odd-cycle advantage
was found. This result is another baseline, not a stronger universal bound.
