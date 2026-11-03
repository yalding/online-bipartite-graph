# Session log

## 2026-11-02 proof review

Reviewed the [optimality proof](OPTIMALITY_PROOF.md) from the conditional
cost game through the finite unweighted construction. The earlier theorem
statement allowed an edgeless witness with zero optimum. The construction
gives a strict ratio on a graph containing an edge. The statement and final
cost calculation now say so explicitly.

The main review question was whether another component can reveal an
unseen local coin at a simultaneous arrival. The revised argument fixes
the other component's coins and conditions only on the sign word and own
choices consumed through the current arrival. This determines the joint
public past and leaves the local continuation law intact. Conditional
expectations at consecutive prefixes then give a feasible local strategy.
The proof now spells out the minimax margin, the order of quantifiers in
the fork inequalities, and the use of a common horizon before evaluating
any randomized algorithm. The resulting integral bound agrees with
Section 4.1, equation (1), of [Wang and Wong](https://arxiv.org/abs/1305.1694).

Expanded the [exact interleaving check](../scripts/interleaving_check.py)
to include root-only stops, hidden intermediate decisions, and distinct
terminal labels with the same root status. The original fixture checked
18 decision-prefix laws. The new fixture checked 17 under each tie order.
All distributions had unit mass and zero incompatible mass. See the
[saved results](../experiments/interleaving-check.json).

Replayed the integer verifier and independently reconstructed the saved
fork lines with rational arithmetic. For each stored child, substituted
its slope into the formula for $h$ in Section 6, evaluated inequality
(4), and rounded its intercept down to the $1/S$ grid. The first crossing
in row 126 was column 4105 with integer margin 76,706,847. An end-to-end
check of the witness generator with an algorithm that buys each vertex on
its first incident edge returned four vertices, optimum one, and a cost
lower bound of three. These finite checks complement the analytic argument.

## 2026-11-01: seventh research session

Derived the [universal lower bound](OPTIMALITY_PROOF.md) for vertex arrivals
on unweighted bipartite graphs. The proof uses an ordered coupling of
posterior probabilities on two rooted subtrees. Finite minimax and this
coupling turn the ability of an arbitrary full-history algorithm to handle
every interleaving into two necessary local budget inequalities. Taking
small rational child weights recovers the Wang–Wong variational bound.
Compactness, a finite LP search, private leaves, and a common integer
blowup complete the finite oblivious construction.

Generated and replayed the compressed fork certificate excluding $1.9005$.
Its integer intercept exceeds the root budget by 76,706,847 at scale
$4\cdot 10^{12}$. An exact ordered-walk fixture separately checks the
conditional test distributions and terminal compatibility. The all-epsilon
argument is analytic and awaits independent review.

Found a finite counterexample to the Session 5 tree-of-pools ceiling,
certified a $1.84$ strategy when just one endpoint survives, and proved
a $13/7$ bound when each pool has at most two later neighboring batches.
The untracked biclique heuristic's Lu birth rule has an unbounded ratio on
geometrically growing cohorts. See [tree continuations](TREE_CONTINUATIONS.md)
and [bounded reuse](BOUNDED_REUSE.md).

## 2026-11-01: first research session

### Plan written before the main investigation

Read the original model and Section 7; identify later papers; separate
algorithm-specific tightness from universal hardness; reconstruct promising
recurrences; retain papers, calculations, and next steps on disk.

### Completed

- Read the original Algorithm 3, allocation-function optimization, paired
  primal-dual identity, and Section 7 from downloaded TeX.
- Located Tang's February 2026 tight matching result and Lu's August 2026
  cover lower bound. Verified titles, authors, dates, models, and main theorem
  statements against primary arXiv pages and source.
- Read Tang's active-pool construction, recursive payoff accounting, and
  fixed-point optimization argument. Not a formal proof verification.
- Read Lu's finite continuation budget, discrete recurrence, scaling argument,
  and fixed-point classification. Reproduced its critical profile substitution
  to about 60-digit precision at representative points.
- Derived a center-last star family approaching the original cover algorithm's
  exact `1.9007616968738465...` guarantee. Saved proof, error estimate,
  high-precision evaluator, and a 1,001-vertex concrete input.
- Derived the paired-objective explanation for why Tang's matching-hard
  witnesses are nearly optimal for the paired cover algorithm.
- Reproduced Lu's near-threshold directed integer certificate: first budget
  violation at depth 754 for the proposed ratio 1.82435. Saved exact integers.
- Observed that a 12,000-cell floating grid misses that near-threshold
  violation. Saved the negative numerical result and its limitation.
- Built a finite public-prefix LP with exact rational primal/dual checking.
  Pilot values: `3/2` for single-neighbor trees through five vertices, and
  `26/17` for a four-pool family with sizes 1 and 4 and root size 4.
- Downloaded five PDFs and source archives, with version and hash manifest.

### Operational notes

The folder was initially empty and is not a Git repository. No user work was
overwritten. Initial network access from the sandbox failed; authorized network
downloads succeeded with sandbox escalation. A guessed `1904.08255v3` URL
returned 404; it was corrected to the verified existing v1. All five downloads
and extractions subsequently completed.

The downloaded original PDF displays a later compilation date despite its v1
identifier. The manifest records the actual downloaded bytes. Use pinned arXiv
identifiers and source content rather than inferring a new revision from that
printed date.

### Current conclusion and outstanding work

Algorithm-specific cover tightness: proved by stars.
Fractional matching optimality: settled by Tang (2026).
Universal cover optimality: not settled; known interval located is
`[1.824360635350064..., 1.900761696873847...]`.

No new universal lower bound beyond the literature was obtained. The next
session should extend the finite family search and derive a comparator-aware
recurrence, while also considering a better algorithm. See `NEXT_SESSION.md`.

## 2026-11-01: second research session

The user asked to continue toward settling the universal open problem. See
`SESSION_2_WORKING.md` for the full record, `PRIVATE_LEAF_BUDGET.md`,
`PROFILE_AWARE_BOUND.md`, and `VERTEX_BLUEPRINT_CLEANUP.md` for the mathematics,
and `FINITE_DISTRIBUTIONS.md` for explicit inputs and independent certificates.

Stronger necessary conditions and a legal blueprint reduction were investigated.
Neither has yet improved the universal lower bound. The interval is unchanged.
The revised plan is `NEXT_SESSION.md`; the earlier plan is `SESSION_1_PLAN.md`.

## User clarification after session 2

The user emphasized that a matching hardness construction settling optimality,
not incremental lower-bound progress, is the objective. The previous work drifted
toward exploratory bounds and infrastructure. `CONSTRUCTION_TARGET.md` now fixes
the theorem, proof obligations, and direct adversarial-recursion strategy.
`NEXT_SESSION.md` makes this objective take precedence over the earlier search
agenda, which is preserved as `SESSION_2_PLAN.md`.

## 2026-11-01: third research session

Continued the clarified matching-construction objective. The universal
hypothesis remains unresolved, with no interval improvement claimed.

Proved a forest obstruction ruling out the entire existing blueprint cleanup
above 11/6, using a newly located primary forest-cover result. Proved a
3/2 upper bound for a cycle-preserving three-edge-path encoding of late
edges, including every stopping prefix. Derived exact retired-region
boundary tables, a finite legal adversarial recurrence, and a nonnegative
four-parameter interface closed under alternating two-pool phases.

Saved proofs, a concrete failed-compression example, and rational exhaustive
checks in `CONSTRUCTION_OBSTRUCTIONS.md`, `BOUNDARY_STATE.md`, and
`experiments/construction-obstructions.json`. The new small-state recurrence
has not been solved or shown to reach the target. See `SESSION_3_WORKING.md`
for the complete checkpoint. Downloaded an eighth paper with pinned hashes.

## 2026-11-01: fourth research session

Continued the matching-construction objective. The target remains unresolved;
no stronger universal lower bound is claimed. See `SESSION_4_WORKING.md`.

Derived lazy full-history response normalization, convex polyhedral
continuation values, and exact two-line response certificates. Classified
the two-pool phase algebra. A primary bounded-degree cover algorithm gives
a 15/8 obstruction to equal-size strictly retired announced-batch phases.
A conditional finite trap exceeds B but has no forced-prefix argument.

Changed the candidate by allowing terminal private leaves, including on
phase-retired vertices. Its exact surplus is sunk cost minus a minimum cover
with weights w_i*(beta+y_i). This has a four-parameter retired interface with
exact phase closure and four graph-realized terminal planes. It removes the
particular degree-four obstruction, without establishing the target value.
The forcing inequality from the reachable initial state is still missing.

Saved `TWO_POOL_RESPONSE.md`, `COMPLETION_GAME.md`, and exact diagnostics in
`experiments/two-pool-response.json`: 600 response certificates/LP comparisons,
9,216 phase identities, and 2,592 reweighted phase/terminal cases. Downloaded
the ESA 2017 bounded-degree primary PDF, recorded its hash, and updated the
resume plan. No subagents or external messages were used.

## 2026-11-01: deep research review and revised plan

Reviewed the research status, plans, mathematical notes, response and LP code,
and relevant primary-source arguments; searched for later results. No later
settlement of the cover question was located. The universal interval is
unchanged, and no new hardness theorem is claimed.

The assessment is `RESEARCH_REVIEW.md`. It identifies the completion terminal
test with the earlier private-leaf budget, explains the loss of repeated
old-pool reuse under strict retirement, derives the accounting normalization
`s=A-c` and its retirement update, and records the response-dependent table
integration obligation. The active plan now asks for a graph-realized forcing
lemma or a precisely scoped safety invariant before more expansion of the
candidate; selective persistence is the preferred extension when justified.

Re-ran `two_pool_response.py --lp-check` and `construction_obstructions.py`;
all local response, table, phase, and obstruction checks passed. These do not
compute a positive initial completion-game value. Preserved the previous
resume plan as `SESSION_4_PLAN.md`, replaced `NEXT_SESSION.md`, and linked the
review from the README and status note. No agents or external messages were
used. The repository is initialized but has no commits; research files remain
untracked.

## 2026-11-01: commit workflow preference

The user requested commits by default for completed changes. Recorded the
preference in the root `AGENTS.md`, ignored local research dependencies and
Python caches, and prepared the research workspace for its initial checkpoint
commit, including the deep review and revised plan.

## 2026-11-01: fifth research session (Session 5 structural analysis)

Proved mathematical obstructions for tree-of-pools and two-pool completion games:
- Theorem 1: exact affine-simplex representation of $W_h$ via retired surplus table $E(S) = A_{\text{ret}} - H(S)$.
- Theorem 2: tree-of-pools obstruction proving any rooted tree of pools is capped at $1 + 1/\sqrt{2} \approx 1.707107$ under an explicit ODE.
- Proposition 1: exact Depth-1 conservation identity relating online stopping times to the Wang--Wong recurrence.
- Evaluated two-pool completion game pathwidth bottleneck: $|U| \le 2$ restricts Phase 2 to at most 2 surviving pools, capping the ratio below $1.7273$.
- Theorem 3: graded $k$-phase upper bound showing layer-dependent GreedyAllocation achieves $(1 + \gamma_k)$ competitiveness ($\gamma_1 \approx 0.7071$, $\gamma_2 \approx 0.7825$, $\gamma_k \uparrow \beta^* \approx 0.900762$).
- Resumable Phase-1 alternation: proved that resuming Phase 1 on undivided $L_0$ after Phase-2 bursts penalizes coordinate jumps, raising the 2-alternation continuum threshold from $\approx 0.7620$ (`lu_baseline`) to $\approx 0.7654$ (`depth1_D`), and sparse LP with two Phase-2 bursts (`full_D_phase2`) extrapolating to $\approx 0.772$ at $\beta = 0.75$.
- Saved `COMPLETION_GAME_OBSTRUCTIONS.md`, `scripts/completion_game_obstructions.py`, `scripts/resumable_alternation_check.py`, and `experiments/resumable-alternation-check.json`.

## 2026-11-01: sixth research session (Opus audit and structural synthesis)

Audited the Graded $k$-Phase Allocation Theorem and audited Tang's (2026) matching proof:
- Audited the layer-dependent allocation operator under two distinct terminal boundaries:
  * Variant A (constant terminal $f_0(y) = \gamma$, applicable to terminal private leaves): $\gamma_1 = 1/\sqrt{2} \approx 0.707107$, $\gamma_2 \approx 0.782525$, ..., $\gamma_{14} \approx 0.891031 \uparrow \beta^*$.
  * Variant B (linear terminal $f_0(y) = \gamma + y$, applicable to bare terminal layer): $\gamma_1 = 1/(e-1) \approx 0.581977$ (recovering the classic 1-sided KVV / WW bipartite theorem!), $\gamma_2 \approx 0.746826$, ..., $\gamma_{14} \approx 0.890365 \uparrow \beta^*$.
  * Both boundary conditions converge to Wang and Wong's continuous fixed point $f(z) f'(1-z) = z - 1$ at $B^* \approx 1.90076170$.
- Analyzed Tang's (2026) matching construction:
  * Deconstructs why Tang reaches $\Gamma^* = 1/B^*$ for matching via active partition branching and selective deactivation of least-matched vertices.
  * Identified the duality asymmetry: matching deactivation succeeds because disjoint complete bipartite components decompose additively without cross liability, whereas in vertex cover, historical cross edges prevent localized deactivation.
- Saved `GRADED_PHASES_AND_PARTITIONS.md`, `scripts/graded_phase_recursion.py`, and `experiments/graded-phase-recursion.json`.
