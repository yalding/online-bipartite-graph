# Online vertex cover and matching: tightness research

Research started 2026-11-01 (America/Los_Angeles).

## Result

The [optimality proof](notes/OPTIMALITY_PROOF.md) derives a lower bound of
$B^*-\epsilon$ for every randomized online fractional vertex-cover
algorithm on a finite unweighted bipartite input fixed independently of
its random seed. With Wang and Wong's upper bound, the optimal ratio is
$B^*=1.9007616968738465\ldots$. This is a new research proof in this
repository and has not received independent review.

The core graph is a tree of pools. After each parent-child edge, both
endpoints may have future children. A shared random walk interleaves
their continuations, preserving what an algorithm can learn at each
arrival while ensuring that the two hidden offline covers jointly cover
the connecting edge. This yields a necessary inequality for arbitrary
algorithms and gives the Wang–Wong constant.

The proof includes a terminating finite-witness construction for every
strictly smaller ratio. For the concrete ratio $1.9005$, a separate
[finite fork certificate](experiments/fork-1801-2000.npz) can be replayed
with exact integer arithmetic. The [handoff](notes/NEXT_SESSION.md) lists
the checks and proof locations.

## Findings at the first checkpoint

The specific cover algorithm is tight on center-last stars. Its exact bound
is `1.9007616968738465...`. The universal matching question is settled by Tang
(2026). The primary sources available at that checkpoint placed the
universal fractional cover ratio between `1.824360635350064...` and
`1.900761696873847...`.

Start with [the research report](notes/RESEARCH_STATUS.md),
[the star proof](notes/STAR_TIGHTNESS.md), and
[the next-session plan](notes/NEXT_SESSION.md).

Session 2 continued with stronger continuation budgets, profile inequalities,
blueprint cleanup, and explicit finite oblivious hardness distributions. It did
not improve the known universal lower bound. See
[the session-2 log](notes/SESSION_2_WORKING.md) and
[the finite distributions](notes/FINITE_DISTRIBUTIONS.md).

Session 3 ruled out two candidate transfers of edge-arrival hardness and
derived an exact offline state closed under alternating two-pool phases.
The universal hypothesis was unresolved at that checkpoint. See
[the session-3 report](notes/SESSION_3_WORKING.md),
[the construction obstructions](notes/CONSTRUCTION_OBSTRUCTIONS.md), and
[the exact boundary state](notes/BOUNDARY_STATE.md).

Session 4 derived exact scalar-response certificates, identified a 15/8
obstruction for equal-size strictly retired batch phases, and changed the
candidate to permit terminal private-leaf completions. A reweighted
four-parameter interface gives their exact payoff. See
[the session-4 report](notes/SESSION_4_WORKING.md)
and [the completion game](notes/COMPLETION_GAME.md).

Session 5 studied a proposed upper bound for rooted trees of pools. A
[finite counterexample](notes/TREE_CONTINUATIONS.md) disproves its
$1+1/\sqrt2$ claim. Graded $k$-phase graphs admit a $(1 + \gamma_k)$-competitive
layer-dependent algorithm ($\gamma_k \uparrow \beta^*$). Resumable Phase-1 / interleaved
Phase-2 alternation strictly beats Lu's baseline, extrapolating to $\approx 1.772$
at $k=2$. See [the completion game obstructions note](notes/COMPLETION_GAME_OBSTRUCTIONS.md).

Session 6 audited the graded allocation operator under constant vs. linear terminal
boundaries, recovering the classic Karp--Vazirani--Vazirani $1 + 1/(e-1)$ bound at $k=1$,
and analyzed the active partition dynamics of Tang's (2026) matching proof vs.
vertex cover. See [the graded phases and partitions note](notes/GRADED_PHASES_AND_PARTITIONS.md).

## Relevant recent papers

- Zhihao Gavin Tang, *Optimal Competitive Ratio of Two-sided Online Bipartite
  Matching*, arXiv:2602.18049, submitted 2026-02-20. Proves a matching
  impossibility bound equal to Wang--Wong's approximately 0.526 guarantee.
- Tianhang Lu, *A New Lower Bound for Online Vertex Cover under Vertex Arrivals*,
  arXiv:2608.09210, submitted 2026-08-10. Proves a lower bound
  `1 + sqrt(e)/2 = 1.824360635...`, and a limitation of the homogeneous
  complete-bipartite recurrence at that same value.
- Baligacs et al., *Online and Incremental Fractional Vertex Cover on Trees*,
  arXiv:2608.24630v1 / ESA 2026. Its online forest upper bound of `11/6`
  rules out the project's blueprint deletion cleanup as a route to `B`.

## Project layout

- `papers/`: downloaded PDFs, source archives, and extracted text.
- `notes/`: proof notes, literature status, and session logs.
- `scripts/`: reproducible computations and adversarial-instance generators.
- `experiments/`: machine-readable results.

## Reproduce the main calculations

```powershell
python scripts/star_tightness.py
python scripts/analytical_checks.py
python scripts/cover_recurrence.py --certificate
python scripts/finite_adversary_lp.py --vertices 5
python scripts/finite_adversary_lp.py --vertices 4 --sizes 1,4 --root-size 4
python scripts/construction_obstructions.py
python scripts/two_pool_response.py --lp-check
python scripts/resumable_alternation_check.py
python scripts/graded_phase_recursion.py
python scripts/branch_certificates.py
python scripts/interleaving_check.py
python scripts/fork_certificate.py --check experiments/fork-1801-2000.npz
```

The fork certificate and ordered-walk check use exact arithmetic. The
universal limit and the general interleaving lemma have separate analytic
proofs in the optimality note.

See `notes/SESSION_LOG.md` for the audit trail. The Python dependencies are
listed in `requirements.txt`; all are already installed in this environment.
