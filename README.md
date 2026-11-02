# Online vertex cover and matching: tightness research

Research started 2026-11-01 (America/Los_Angeles).

## Objective

**Clarified target:** construct universal hardness approaching the exact
1.9007616968738465... cover bound and settle optimality. Incremental lower
bounds are not the project's objective. Read
[the construction target](notes/CONSTRUCTION_TARGET.md) before continuing.

Investigate Section 7 of Wang and Wong, *Online Vertex Cover and Matching:
Beating the Greedy Algorithm*, arXiv:1305.1694. Distinguish tightness of the
specific algorithms/analyses from optimality among all online algorithms.
Find, audit, and reproduce subsequent hardness constructions, with particular
attention to the remaining vertex-cover gap.

## Working plan

The [deep research review](notes/RESEARCH_REVIEW.md) assesses the current
proofs, restrictions, and missing forcing argument. The active execution plan
is [NEXT_SESSION.md](notes/NEXT_SESSION.md); the previous plan is archived as
[SESSION_4_PLAN.md](notes/SESSION_4_PLAN.md).

1. Specify the completion game precisely and integrate response elimination
   with its response-dependent retired table.
2. Test graph-realized forcing against an explicit safety strategy, using the
   normalized surplus state `A-c` and exact continuous responses.
3. Seek a recursive amplification lemma or a below-target invariant for the
   stated family; change its persistence/retirement operations if warranted.
4. Derive limiting necessary inequalities from legal graph continuations.
5. Complete any successful argument with finite witnesses and obliviousness.

## Findings at the first checkpoint

The specific cover algorithm is tight on center-last stars. Its exact bound
is `1.9007616968738465...`. The universal matching question is settled by Tang
(2026). The universal fractional cover question remains open in the literature
located, between `1.824360635350064...` and `1.900761696873847...`.

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
The universal hypothesis remains unresolved. Start with
[the session-3 report](notes/SESSION_3_WORKING.md),
[the construction obstructions](notes/CONSTRUCTION_OBSTRUCTIONS.md), and
[the exact boundary state](notes/BOUNDARY_STATE.md).

Session 4 derived exact scalar-response certificates, identified a 15/8
obstruction for equal-size strictly retired batch phases, and changed the
candidate to permit terminal private-leaf completions. A reweighted
four-parameter interface gives their exact payoff. The universal target
remains unresolved; start with [the session-4 report](notes/SESSION_4_WORKING.md)
and [the completion game](notes/COMPLETION_GAME.md).

Session 5 proved that rooted trees of pools are capped at $1 + 1/\sqrt{2} \approx 1.7071$
and that graded $k$-phase graphs admit an explicit $(1 + \gamma_k)$-competitive
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
```

The integer recurrence and rational LP scripts verify certificates. The star
limit has an analytic proof. High precision identity checks and floating-point
experiments are numerical checks, not replacements for proofs.

See `notes/SESSION_LOG.md` for the audit trail. The Python dependencies are
listed in `requirements.txt`; all are already installed in this environment.
