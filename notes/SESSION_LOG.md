# Session log

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
