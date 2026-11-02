# Handoff after Session 7

The [new optimality proof](OPTIMALITY_PROOF.md) reaches the requested
$B^*-\epsilon$ against arbitrary randomized fractional algorithms.
Sections 2–3 are the main argument. Independent marginal tests can be
interleaved under an ordered joint walk, so the joint online strategy
induces feasible local strategies at their own decision times. Section 4
obtains the exact analytic threshold. Section 5 gives finite unweighted
inputs with oblivious selection. The result is ready for independent
mathematical review.

The [finite example at 1.9005](../experiments/fork-1801-2000.json) records
the strict integer comparison. Replay it with
`python scripts/fork_certificate.py --check experiments/fork-1801-2000.npz`.
Run `python scripts/interleaving_check.py` for the exact finite conditional-law
fixture. The [tree counterexample](TREE_CONTINUATIONS.md) and the
[bounded-reuse upper bound](BOUNDED_REUSE.md) correct the earlier handoff.
In particular, the old claim about all trees of pools is false.

The material below is the historical Session 6 handoff. Its open questions
and proposed directions predate the proof.

## Session 6 handoff (archived)

Read `GRADED_PHASES_AND_PARTITIONS.md` and `COMPLETION_GAME_OBSTRUCTIONS.md` first,
then `RESEARCH_REVIEW.md`, `CONSTRUCTION_TARGET.md`, `COMPLETION_GAME.md`, and `TWO_POOL_RESPONSE.md`.

### Summary of Session 5 Findings

1. **Resolution of the `COMPLETION_GAME.md` Two-Pool Candidate (Commit `c459d62`)**:
   - **Theorem 1** (`COMPLETION_GAME_OBSTRUCTIONS.md`): The retired-surplus table
     $E(S) = A_{\text{ret}} - H(S)$ gives an exact affine-simplex representation
     of $W_h$ on any active boundary $U$.
   - **Theorem 2 & Proposition 1**: Rooted trees of pools of arbitrary depth are
     capped at $1 + \frac{1}{\sqrt{2}} \approx 1.707107$. In `COMPLETION_GAME.md`
     Eq. (6), the active boundary bound $|U| \le 2$ restricts Phase 2 to at most
     $k = 2$ surviving pools of $R_1$, replacing $f_0(y) = \beta$ by
     $f_1(y_i) = \beta - \frac{y_i^2}{2\beta}$ on at most $k = 2$ discrete points
     ($\approx 1.7219$--$1.7273$ at 2 alternations, verified in
     `scripts/completion_game_obstructions.py`).
2. **Graded $k$-Phase Upper Bound and Resumable Alternation (`scripts/resumable_alternation_check.py`)**:
   - **Theorem 3** (`COMPLETION_GAME_OBSTRUCTIONS.md` Section 5): Any online
     bipartite graph graded into $k$ online layers $V_1, \dots, V_k$ (plus initial
     offline $V_0$ and terminal private leaves $V_{k+1}$) where vertices in $V_m$
     only have past neighbors in $V_{m-1}$ and future neighbors in $V_{m+1}$ admits
     an explicit $(1 + \gamma_k)$-competitive layer-dependent `GreedyAllocation`
     algorithm ($\gamma_1 = 1/\sqrt{2} \approx 0.707107$, $\gamma_2 \approx 0.78252452$,
     $\gamma_k \uparrow \beta^* \approx 0.90076170$).
   - **Why Naive KVV Splitting on $L_0$ Fails**: Splitting $L_0 = A_1 \cup \dots \cup A_K$
     and progressively retiring slices during Phase 1 freezes retired slices at
     $y_{A_i}(i) < 1$, reducing the total online payment on $L_0$ and worsening
     the minimax surplus.
   - **Why Resumable Phase-1 / Interleaved Phase-2 Strictly Beats `lu_baseline`**:
     Allowing the adversary to **resume Phase 1 on the undivided $L_0$** after
     stopping a Phase-2 burst on $R_1([0, r])$ at $\xi$ penalizes any coordinate
     jump on $R_1([0, r])$ via the resumed full in-cover $L_0 \in C, R_1([0, l]) \notin C$.
     At $k = 2$:
     - Wang--Wong Prop. 2 (pigeonhole): $\beta_{\text{WW2}} \approx 0.75343722$
     - Continuum `lu_baseline` (exact monotone profile): $\beta_{\text{lu\_cont}} \approx 0.76202043$
     - Continuum `depth1_D` (Depth-1 resumed Phase 1): $\beta_{\text{D1\_cont}} \approx 0.76535003$
     - Two-burst `full_D_phase2` (resumed Phase 1 with a second Phase-2 burst and
       mixed prefix covers): strictly beats both `lu_baseline` and `depth1_D` across
       $K \in \{6, 8, 10, 12, 14\}$ with a growing gap (`+0.01002` at $K=12$,
       `+0.01048` at $K=14$ for $\beta = 0.75$), extrapolating to $\beta_c(\infty) \approx 0.772$.

### Immediate Next Steps

1. **Infinite-Round Resumable 2-Alternation Fixed Point ($k = 2$)**:
   Formulate and solve the continuum fixed-point operator where Phase 1 can be
   resumed after *every* Phase-2 burst (eliminating the residual suffix slack
   $\int_l^{R_{\max}} z^{\text{D}}(\tau)\,d\tau$ at the second burst in
   `full_D_phase2`) and determine whether infinite-round resumption at $k = 2$
   reaches $\gamma_2 \approx 0.78252452$ or an intermediate barrier.
2. **Multi-Layer Recursive Extension ($k \to \infty$)**:
   Extend the resumable alternation operator from $k = 2$ to general depth $k$
   and analyze the $k \to \infty$ fixed-point threshold against
   $\gamma_\infty = \beta^* \approx 0.90076170$.
3. **Finite-Witness Bridge**:
   Convert any strict continuum violation above $1 + \sqrt{e}/2$ into a certified
   finite realization-oblivious bipartite instance via rational grid discretization.

---

### Previous Review Plan (Archived Context)

Read `RESEARCH_REVIEW.md` first, then `CONSTRUCTION_TARGET.md`,
`COMPLETION_GAME.md`, and `TWO_POOL_RESPONSE.md`. The pre-review plan is
archived as `SESSION_4_PLAN.md`. Earlier session records remain historical.

The target is unchanged: finite, legal, realization-oblivious hardness
approaching B* = 1.90076169687384654357728936308... against arbitrary online
fractional cover algorithms. An incremental lower constant or algorithm-specific
example does not complete the task. The universal optimum is not known to be
B*. No new universal lower bound has been established here; the located
interval remains [1.824360635350064..., 1.900761696873847...].

The current candidate has exact local accounting but no initial-state forcing
result. Its terminal completion test is exactly the session-2 private-leaf
budget. The response checker uses synthetic planes and has not propagated an
actual completion-game value. Strict retirement also prevents the candidate
from literally containing arbitrarily many complete-bipartite alternating
phases. Cycles and a small exact state alone are not evidence of target hardness.

The next work should resolve the forcing-versus-safety question for this family
in a bounded investigation, then change its structural operations if warranted.

1. Specify the exact finite game before evaluating it. Include initial pool
   cardinalities, finite integer arrival menus, neighborhoods, retirement
   announcements, the two separate decisions per phase, and stopping/private
   completions after either arrival. Keep actual graph and terminal-cover
   backpointers. Use R = 1+beta for a trial ratio, reserving B* for the target.

2. Remove the redundant common table offset. For

       H = (c+p+q+k, c+q+k, c+p+k, c),  s = A-c,

   terminal surplus is

       s - min {p+q+k,
                w_a(beta+x_a)+q+k,
                w_c(beta+x_c)+p+k,
                w_a(beta+x_a)+w_c(beta+x_c)}.

   On retiring a,c at coordinates r_a,r_c, put

       theta_a=w_a(beta+r_a), theta_c=w_c(beta+r_c),
       m=min {p+q+k,theta_a+q+k,theta_c+p+k,theta_a+theta_c}.

   Then s_new=s+Delta-m, and p,q,k follow the existing exact phase update
   with weights theta_a,theta_c. Delta includes both arrivals. Retain protocol
   position and witnesses alongside the numerical state. Do not replace the
   actual old graph. Scale normalization is valid only with correspondingly
   scaled action menus.

3. Establish the response/compression interface. Reweighted retirement depends
   on the response, so H_new must not be frozen while retiring coordinates
   vary. Apply the convex response calculation to the actual pre-retirement
   continuation function, then justify compression, or prove the equivalent
   joint property in H. Include intermediate mixed-side boundaries. Preserve
   the full history dependence available to an arbitrary algorithm.

4. Compose graph-realized terminal envelopes through two complete phases,
   with unequal sizes and all specified stop points. Evaluate selected trial
   ratios B* - epsilon rather than chase successively larger lower constants.
   Use exact continuous scalar response minimization, not a sampled player
   grid. Reuse the existing public-prefix LP for an independent finite-game
   comparison where useful. Export branch certificates AND a response policy.
   Determine whether shared liability amplifies after paying retirement cost
   m, and attempt a symbolic recursive inequality or invariant suggested by
   the result. Increase depth only to test that identified mechanism. Use
   existing tools and small symbolic compositions; do not make a new general
   Bellman solver the deliverable.

5. Require a concrete family decision. A forcing proof must start at the
   reachable isolated state and handle every response. A safety proof needs
   an invariant region containing that state, nonpositive terminal surplus,
   and a feasible response to every permitted adversary action, at every
   horizon. A below-B* strategy rules out only the family and size range
   actually covered. A low finite-horizon value or a safe finite submenu
   does not rule out arbitrary unequal sizes or longer play. If the bounded
   investigation yields no amplification lemma or all-horizon invariant,
   mark this candidate unvalidated and move the main effort to a justified
   structural extension rather than more of the same enumeration.

6. Prefer selective persistence as the next structural extension when an
   identified counterstrategy shows the need. Permit an old pool/partition
   to participate in more future phases, or retire only a selected part.
   Choose the smallest operation that defeats the identified strategy.
   Give legal arrivals and exact conditional comparator updates first.
   General boundaries need the full table. If future neighborhoods split
   twins, retain their potential profile or prove an extremal reduction;
   equal averages do not justify forgetting individual irreversible loads.
   Any model claimed to contain general biclique alternations should
   reproduce Lu's finite recurrence as a calibration check.

7. Derive necessary limiting inequalities from that graph construction.
   Do not assume a universal response f, substitute the Wang–Wong minimax
   as an adversarial recurrence, or identify a conditional bad state as
   reachable without proof. The allocation-function optimization is an
   analytic benchmark. A valid extraction must establish the required
   function class and quantifiers; a multivariable limit may be necessary.

8. Complete a successful argument with finite rational pool sizes, an
   accumulated approximation-error bound smaller than the strict surplus,
   sequential unweighted blowups, and explicit terminal offline certificates.
   Use deterministic expected marginals to select an algorithm-dependent
   finite input independent of its realized random seed. Producing one
   distribution hard for all algorithms is an optional separate step.

Useful certificate forms are:

- For hardness: graph-realized lower continuation functions whose exact
  response backup yields positive initial surplus at every R < B*.
- For rejecting a family: a feasible invariant strategy maintaining
  A <= tau_(w(beta+y))(G) for every permitted prefix and terminal completion
  at some R < B*. State its menus, weights, and horizon scope precisely.

Do not reopen blueprint deletion cleanup (forest upper bound 11/6), private
three-edge-path substitution (3/2), or the equal-size strictly retired batch
game without terminal completions (15/8). The 801/421 continuation assumes an
unforced 0.9 old-side average; at R=B* even the one-batch necessary cap is
about 0.8980283877. It is a reachability warning, not a universal witness.
Lu's fixed point limits its recurrence, not all biclique proofs or algorithms.

The review reran `python scripts/two_pool_response.py --lp-check` and
`python scripts/construction_obstructions.py`; all checks passed. Their
outputs remain local identity/obstruction diagnostics. The sparse LP and
independent distribution verifier are available for targeted checks; there
is no need to rebuild generic infrastructure or search larger families
without a mathematical question. SciPy is available in `.research-deps`.

The next deliverable is a forcing lemma, a precisely scoped safety invariant,
or a specific legal extension motivated by a demonstrated response failure.
Report which of these was obtained. Do not treat verification counts or lower
constants as completion milestones. No agents or external messages have been
authorized. Commit completed repository changes as required by the root
`AGENTS.md` and report the resulting hash.
