# Objective: a hardness construction matching the algorithmic bound

Session 7 supplies the [proof and finite construction](OPTIMALITY_PROOF.md)
for the target below. The remaining text states the original objective.

User clarification, 2026-11-01: incremental lower-bound improvements are not
the objective. The objective is a construction that settles optimality.

## Required theorem

Let B=1.90076169687384654357728936308... be the Wang--Wong cover bound.
For every epsilon>0 and every randomized online fractional cover algorithm A,
construct a finite legal vertex-arrival input sigma such that

    E[ALG_A(sigma)] >= (B-epsilon) * OPT_fractional(sigma).

The input must be independent of the realized random seed. Prefer bipartite
instances, but a general-graph construction would already settle optimality
for the general fractional problem. State explicitly which class is proved.

An equivalent sufficient deliverable is an explicit finite distribution with
that expected-ratio lower bound against every deterministic fractional strategy.
Smaller numerical ratios, a tight example for the known algorithm alone, or a
new computational framework do not fulfill this target.

## Primary proof program

Reverse-engineer an adversarial game from the exact minimax optimization in
the original paper. A successful construction must force every algorithm's
present investment versus future liability tradeoff, rather than merely make
the particular Wang--Wong charging analysis tight.

The candidate analytic target is to show that avoiding a bad continuation
induces a response envelope f satisfying inequalities whose optimum equals

    inf_f sup_(z in [0,1])
      [1 + f(1-z) + integral_z^1 (1-t)/f(t) dt] = B.

This is a proposed route, NOT an established necessary condition on arbitrary
algorithms. Proving the reduction is the central missing argument. In particular:

- Do not assume the algorithm is a water-filling algorithm or has scalar state.
- Explain how f is extracted from arbitrary choices and unequal old potentials.
- Justify positivity and regularity, or prove an appropriate relaxed minimax
  lower bound. Do not silently impose the original algorithm's assumptions.
- Every analytic branch must correspond to a legal graph continuation with a
  certified fractional offline comparator.

Use recursive pool gadgets with explicit boundary state. Track sunk algorithm
cost and conditional offline-cover costs; introduce additional potential-profile
state only where a concrete failure requires it. For each possible algorithm
response, give a continuation that either yields the target bad ratio or passes
a quantitatively specified deficit to a smaller recursive gadget.

The two conditional offline costs at a rooted tree boundary are useful starting
data, but are not assumed sufficient for arbitrary pool graphs. All edges to
retired pools must remain accounted for.

Session 3 now supplies an exact interface and finite game in
`BOUNDARY_STATE.md`, including a four-parameter closure for two same-side
active pools. Its surplus recurrence has not been solved. Two proposed
edge-arrival transfers are ruled out in `CONSTRUCTION_OBSTRUCTIONS.md`;
neither is a route to the target at larger scale.

Session 4 now specifies the stronger completion game in `COMPLETION_GAME.md`.
Its terminal private leaves give an exact payoff using cover weights
w_i*(beta+y_i), with a four-parameter retired interface and graph-realized
terminal planes. Its forcing inequality is still missing. This supersedes
the equal-size strictly retired phase candidate, which has a 15/8 upper bound
in the public batch model. Unequal sizes in the old game remain unexcluded.

## What a complete construction must contain

1. A parameterized graph/input generator and arrival order, with no old-old
   edge revealed late.
2. A proof handling every allowed algorithm response, including asymmetric
   potential assignments.
3. An explicit offline fractional solution or exact optimum certificate for
   every branch.
4. A recursive/differential analysis reaching the exact constant B, rather
   than a numerical constant below it.
5. A finite discretization and an oblivious-adversary justification with the
   quantifiers in the required theorem.

## Role of computation and other approaches

Use the existing LP and exact certificates to falsify a proposed gadget,
check its accounting, or extract a missing inequality. Do not organize further
work as a march through larger finite families or successively better constants.
Do not count infrastructure or lower constants as completion milestones.

If a structural obstruction kills the proposed construction, record it precisely
and change the construction. An improved algorithm is relevant only if evidence
shows the conjectured matching hardness is false; it is not the current target.

The edge-blueprint route remains a backup only if it offers an analytic path to
the exact target. Its small cleanup experiments do not currently offer one.

## Communication standard

Report whether an argument advances the matching-construction proof, disproves
a candidate gadget, or merely verifies a calculation. Be candid that a complete
proof has not been found. Do not label an incremental lower bound as settling
the user's question.
