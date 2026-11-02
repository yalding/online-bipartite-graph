# Research status: 2026-11-01

Session 5 (`COMPLETION_GAME_OBSTRUCTIONS.md`, `scripts/completion_game_obstructions.py`,
`scripts/resumable_alternation_check.py`) resolves the two-pool completion game
question from `COMPLETION_GAME.md` and `NEXT_SESSION.md`:
1. **Exact Affine-Simplex Representation (Theorem 1)**: Defining the retired
   surplus table $E(S) = A_{\text{ret}} - H(S)$ eliminates the separate sunk
   cost $A$ and makes pool retirement and arrival closed-form operations on
   affine-simplex planes (`c, alpha, mu`).
2. **Tree-of-Pools and Two-Pool Obstructions (Theorem 2, Proposition 1, Section 4)**:
   Rooted trees of pools of arbitrary depth are capped at $1 + \frac{1}{\sqrt{2}} \approx 1.707107$
   via an explicit online ODE. In `COMPLETION_GAME.md` Eq. (6), restricting the
   active boundary to $|U| \le 2$ allows at most $k = 2$ pools to survive into
   Phase 2, replacing $f_0(y) = \beta$ by $f_1(y_i) = \beta - \frac{y_i^2}{2\beta}$
   on at most two discrete points ($\approx 1.7219$--$1.7273$ at 2 alternations).
3. **Graded $k$-Phase Upper Bound (Theorem 3) and Resumable Alternation (Section 5)**:
   Extending Wang and Wong's 2-alternation charging lemma proves an exact
   $(1 + \gamma_k)$-competitive upper bound for any graded $k$-phase graph
   ($\gamma_1 = 1/\sqrt{2} \approx 0.707107$, $\gamma_2 \approx 0.78252452$,
   $\gamma_k \uparrow \beta^* \approx 0.90076170$). At $k = 2$, retaining exact
   monotone profiles (`lu_baseline`) raises Wang--Wong Prop. 2's threshold from
   $\beta_{\text{WW2}} \approx 0.753437$ to $\beta_{\text{lu\_cont}} \approx 0.762020$,
   and allowing **resumable Phase-1 / interleaved Phase-2** continuations
   (`depth1_D` and `full_D_phase2` with mixed prefix covers) strictly improves
   the minimax surplus across $K \in \{6, 8, 10, 12, 14\}$ ($\beta_{\text{D1\_cont}} \approx 0.765350$,
   and $\beta_c(\infty) \approx 0.772$ for two Phase-2 bursts).

The earlier [deep review](RESEARCH_REVIEW.md) leaves the universal interval
unchanged and replaces the resume plan in `NEXT_SESSION.md`. It identifies
terminal completion safety with the existing private-leaf budgets, notes that
strict retirement omits repeated use of old pools in general biclique
alternations, and removes a redundant state offset using `s=A-c`. The next
task is a graph-realized forcing lemma or a scoped safety invariant, with a
specific persistence extension if the current family lacks amplification.
The review reran the response and construction-obstruction checks successfully;
it did not compute the completion game's initial value or prove new hardness.

Session 4 analyzes the exact two-pool candidate and replaces its restricted
equal-size version, which has a 15/8 upper bound, with a stronger terminal
private-leaf completion game. A reweighted four-parameter interface captures
retired online cost and supplies graph-realized terminal planes. Response
steps admit exact two-line certificates. The extended game has not been
shown to reach B; a conditional 801/421 trap does not force its initial state
and is not a universal lower bound. See `SESSION_4_WORKING.md`,
`COMPLETION_GAME.md`, and `TWO_POOL_RESPONSE.md`. There are nine saved PDFs.

Session 3 proved two construction obstructions and derived an exact recursive
boundary state; it did not settle the universal hypothesis or narrow its
interval. See `SESSION_3_WORKING.md`, `CONSTRUCTION_OBSTRUCTIONS.md`, and
`BOUNDARY_STATE.md`. In particular, blueprint deletion cleanup is now ruled
out for the target at every scale, rather than merely unsuccessful in small
experiments. There are now eight downloaded papers.

Session 2 added stronger necessary constraints, profile experiments, a
vertex-arrival blueprint cleanup, and exact finite hardness distributions.
See `SESSION_2_WORKING.md` and `FINITE_DISTRIBUTIONS.md`. The universal interval
below is unchanged. There are now seven downloaded papers.

## Answer at this checkpoint

There are three different tightness questions:

| Question | Status established in this session |
|---|---|
| Is Wang--Wong's particular fractional cover algorithm tight? | Yes. Center-last stars approach `B = 1.9007616968738465...`; see `STAR_TIGHTNESS.md`. |
| Is the fractional matching competitive ratio optimal among all algorithms? | Tang (2026), Theorem 1.1, proves the matching impossibility bound `1/B = 0.5261048776628257...`, already on bipartite graphs. |
| Is the best possible fractional vertex-cover ratio `B`? | Still unresolved in the primary literature located. The interval is `[1+sqrt(e)/2, B] = [1.824360635350064..., 1.900761696873847...]`. |

The last question is the substantive remaining optimality question in Section 7.
This session does not prove a new universal lower bound of 1.901.

## Model and notation

Vertices arrive one at a time, revealing their edges to earlier vertices.
Fractional covers increase coordinatewise; matching edges receive irrevocable
weights at their reveal. The adversary is oblivious to the realized random
seed. For bipartite inputs, allowing the algorithm to see a consistent
bipartition only strengthens it and is compatible with the cited bounds.

Use `B` for a covering ratio; matching ratios are maximization ratios in `[0,1]`.
Lu writes the hypothetical covering ratio as `1+beta`, so his `beta` is **not**
Wang--Wong's full approximately 1.901 ratio.

## Primary sources located

1. Wang and Wong, [arXiv:1305.1694](https://arxiv.org/abs/1305.1694), 2013
   preprint; ICALP 2015 version has the title *Two-Sided Online Bipartite
   Matching and Vertex Cover: Beating the Greedy Algorithm*.
2. Tang, [arXiv:2602.18049](https://arxiv.org/abs/2602.18049), submitted
   February 20, 2026. This is the most likely paper the user remembered.
3. Lu, [arXiv:2608.09210](https://arxiv.org/abs/2608.09210), submitted
   August 10, 2026. Additional progress on the remaining cover problem.
4. Gamlath, Kapralov, Maggiori, Svensson, and Wajc,
   [arXiv:1904.08255](https://arxiv.org/abs/1904.08255), 2019. Gives a
   randomized integral matching algorithm beating one half with general
   vertex arrivals, resolving another Section 7 question.
5. Tang and Zhang, [arXiv:2202.02948](https://arxiv.org/abs/2202.02948),
   2022 preprint / EC 2024. Alternative matching algorithm and earlier
   hardness improvements; saved for further comparison.

All five PDFs and source archives are saved under `papers/`, together with
SHA-256 hashes and pinned versions in `papers/manifest.json`. Source extraction
keeps TeX/BibTeX/style files and rejects parent-relative archive paths. PDF text
extraction warns about rotated content, so equations were read from TeX.

The related [edge-arrival result](https://arxiv.org/abs/2608.04994) proves a
different theorem. It must not be used as a vertex-arrival lower bound.
Likewise, departure-time algorithms in the fully online model do not answer
the immediate-decision question here.

## Why matching hardness does not transfer

An offline LP duality theorem does not turn an online matching adversary into
an online cover adversary. There is an especially direct obstruction here.
For the paired Wang--Wong algorithms the exact objective identity is

    C_A(G) = B * M_A(G).

On a bipartite input, write `OPT` for the common offline cover/matching optimum.
Suppose Tang's adversary against this matching algorithm gives

    M_A(G)/OPT < 1/B + epsilon.

Cover feasibility and the objective identity then force

    1 <= C_A(G)/OPT < 1+B*epsilon.

Thus matching-hard witnesses for this paired algorithm make its cover nearly
optimal. This rules out reusing those same witnesses to prove cover ratio `B`.
It does not rule out borrowing the adversary's structural ideas.

The identity is interpreted with the intended pre-update value of `y_u` in
the matching increment. The displayed pseudocode assigns `y_u` before using
the difference, but the surrounding proof and increments make the intended
old-value semantics unambiguous.

## What was checked about the recent proofs

Tang's construction maintains active pools. A small new pool is connected to
an active pool; its future depends on how aggressively the algorithm matches.
The payoff recursion has two branches, and inactive vertices admit a perfect
matching. The mathematical fixed-point argument recovers the same optimized
constant as the positive algorithm. The construction and its payoff accounting
were read from source; this is a research audit, not formal verification.

Lu's lower bound uses finite continuations and a monotone deficit recurrence:

    D_0(t) = [1-beta*t]_+
    D_(h+1)(t) = [1-beta*t + t*integral_(1/t)^infinity D_h(u) du]_+.

A competitive trajectory would require `integral D_h <= beta` at every depth.
The fixed-point profile was independently substituted and integrated at high
precision. The finite continuation budget and discrete-to-continuous argument
were also read. The recurrence has a critical supersolution at
`beta=sqrt(e)/2`.

**Scope of this barrier:** that recurrence cannot establish a stronger bound.
It is not an algorithmic upper bound, and it does not by itself exclude every
possible proof using complete-bipartite inputs.

## Reproductions and original calculations

### Algorithm-specific construction

`python scripts/star_tightness.py`

The star calculation and finite error estimate are analytic. High precision
computations give these concrete ratios:

| Leaves | ALG / OPT |
|---:|---:|
| 10 | 1.791591388787 |
| 100 | 1.891441756664 |
| 1,000 | 1.899857628704 |
| 10,000 | 1.900671587447 |
| 1,000,000 | 1.900760796109 |

`experiments/center-last-star-1000.json` is an explicit unweighted input.
The large-degree examples are described parametrically rather than stored
as giant edge lists. A different algorithm can cover the center for cost one;
these examples are not universal hardness.

### Directed integer recurrence certificate

`python scripts/cover_recurrence.py --certificate`

Parameters: `beta=82435/100000`, 24,000 cells per unit, cutoff 2, scale `10^18`.
All rounding is downward. The exact comparison first violates the budget at
depth 754. The preceding and violating normalized integrals are approximately
`0.809481094836634` and `0.885466040865496`.

This independently reproduces the paper's depth and close numerical values;
the last digits differ because its appendix does not fix our integer scale.
The JSON saves exact integer numerators and denominators. The certificate
is for the continuous recurrence; it does not explicitly list the finite
graph selected by the paper's existence argument.

The exploratory command without `--certificate` uses floating point. Its
12,000-cell grid fails to detect the 1.82435 violation even at depth 3,000.
Failure on a fixed grid is **not** evidence of an achievable competitive ratio.

### Finite adversary LP

`python scripts/finite_adversary_lp.py --vertices 5`

The pilot family of trees formed by single-neighbor arrivals has minimax ratio
`3/2` through five vertices. Exact rational primal and dual solutions agree.

`python scripts/finite_adversary_lp.py --vertices 4 --sizes 1,4 --root-size 4`

The second pilot uses independent twin groups joined by complete bicliques,
with a tree as quotient graph. The exact batch-game ratio is `26/17`, verified
by rational primal and dual certificates. There are 59 public prefixes, 222
variables, and 604 inequalities. Group sizes are public at the batch arrival;
this strengthens the algorithm. Therefore its lower bound applies to sequential
unweighted inputs after blowing up groups, but the batch-game upper bound must
not be presented as an upper bound for unrestricted sequential inputs.

Neither pilot improves the literature. They validate a reusable way to test
nonhomogeneous adversarial families without accidentally making the algorithm
clairvoyant.

## Current technical direction

The latest candidate is the completion game in `COMPLETION_GAME.md`, using
the retired-region table for weights w_i*(beta+y_i), rather than just the
ordinary offline table. It has an exact graph-realized terminal envelope,
but the forcing inequality from the initial state is missing. The equal-size
strictly retired phase game cannot reach B in the public batch model.

Seek the requested matching hardness construction using recursive active
pools and exact conditional offline costs. Session 3 gives a four-parameter
offline interface closed under alternating two-pool phases with cycles.
Its competitive surplus recurrence has not been solved. Blueprint deletion
and private three-edge-path substitution are ruled out by upper bounds of
11/6 and 3/2 on those respective families. Do not assume the true optimum is
1.901 merely because that algorithm is tight. `NEXT_SESSION.md` records
the precise remaining proof obligation.
