**Research review and revised strategy — November 1, 2026**

The project has established useful accounting lemmas and eliminated several
constructions. It has not established that the latest construction is hard
enough to settle the problem. The next investment should resolve that question,
rather than add more local identities or assume that the Wang–Wong constant
must emerge from a sufficiently elaborate recursion.

The objective remains the theorem in `CONSTRUCTION_TARGET.md`: for every
epsilon > 0 and every randomized online fractional cover algorithm, produce
a finite, realization-oblivious vertex-arrival input with expected ratio at
least B* - epsilon, where

    B* = 1.90076169687384654357728936308...

A smaller lower bound is not the project's completion criterion. Conversely,
B* is a conjectured universal optimum, not a consequence of its optimality
inside the original allocation-function framework.

The review covered the session plans and mathematical notes, the response and
LP implementations, relevant saved primary-source arguments, and a fresh
primary-source literature search. The original paper explicitly distinguishes
optimality in its framework from optimality for the problem. No later
settlement of the remaining cover question was located in this search; this
is a literature-search conclusion, not a proof that none exists.

| Claim | Current assessment | Consequence |
|---|---|---|
| Wang–Wong cover guarantee B* | Published upper bound; the project's star calculation gives algorithm-specific tightness | Established baseline, not universal hardness |
| Fractional matching optimum 1/B* | Tang's 2026 result | Settles the matching question; does not settle covering |
| Universal cover lower bound 1 + sqrt(e)/2 | Lu's 2026 result, including a finite-oblivious bridge | Best lower bound located remains 1.824360635350064... |
| Lu's critical profile | A barrier for the stated homogeneous deficit recurrence | Not a cover algorithm or an impossibility theorem for every biclique argument |
| Blueprint deletion cleanup and private three-edge-path encoding | Project proofs give structural upper bounds of 11/6 and 3/2 respectively | These exact routes should stay closed |
| Equal-size strictly retired two-pool batch game | A 15/8 counterstrategy applies | That specialization cannot reach B* |
| Completion game with arbitrary permitted pool weights | Exact terminal accounting and phase updates; initial value unknown | A candidate requiring a forcing or safety theorem |
| Conditional 801/421 trap | Correct conditional obstruction; stipulated investment has not been forced | Does not advance a universal lower bound by itself |
| Saved finite LP distributions | Valid restricted-family certificates below the published lower bound | Useful diagnostic assets; not progress on the target constant |

The unresolved numerical interval is

    [1.824360635350064..., 1.900761696873847...],

with width approximately 0.0764010615237825. There has been no certified
narrowing of this interval in the project.

The strongest reusable assets are the exact conditional comparator table,
the private-leaf continuation argument, and the response elimination lemma.
They address genuine failure modes: forgetting edges to retired vertices,
confusing a history-specific profile with a universal one, and assuming an
arbitrary algorithm has a scalar internal state. The obstruction proofs are
also valuable because they rule out whole constructions at every scale.

The verification evidence is narrower than a forcing theorem. During this
review, `two_pool_response.py --lp-check` passed all 600 exact local response
certificates and numerical unrestricted-response comparisons, 9,216 phase
identities, and 2,592 reweighted-table/terminal cases.
`construction_obstructions.py` also passed its boundary, retirement,
subdivision-prefix, and cleanup checks. These checks support the local proofs.
The response script uses synthetic continuation planes; it does not implement
backward propagation of a graph-realized completion-game value. Neither script
computes positive surplus at the initial state. The earlier recurrence and
distribution certificates were inspected as saved work, not freshly rerun here.

The current plan's central weakness is therefore substantive: “propagate a
strong enough envelope” still contains almost the entire missing hardness
argument. There is no forced-prefix lemma, invariant amplification inequality,
or limiting equation connecting the completion game to B*. Exact local
algebra is necessary, but it does not supply this connection.

**The completion game has an especially useful interpretation.** Fix a trial
ratio R = 1 + beta. At a pool-graph prefix, write A = sum_i w_i y_i and
theta_i = w_i(beta + y_i). Its optimized terminal surplus is

    g_R(G,y) = A - tau_theta(G)
             = max_(C a cover) [sum_(i outside C) w_i y_i - beta w(C)].

Thus terminal safety, g_R <= 0, is exactly the private-leaf budget for every
cover from session 2. The reweighted table gives an efficient exact way to
carry those constraints through a particular adversarial protocol. It does
not introduce a new terminal inequality beyond them. This is still useful:
the open issue is whether the budgets can be maintained through repeated,
legal arrivals, not whether they hold at one isolated state.

This formulation exposes the two useful certificates to seek. A hardness
certificate chooses legal arrivals so that every continuous player response
eventually violates one of these budgets. A safety certificate gives a
response rule and an invariant region containing the initial state, keeps
g_R <= 0, and survives every allowed next arrival and adversarial retirement
choice. A safety theorem with R < B* would eliminate the specified family;
it would not by itself refute the conjecture for unrestricted graphs.

The conditional trap illustrates this distinction sharply. An old-left
average of 0.9 in K_20,20 leads to the 801/421 continuation. The more general
one-batch calculation already gives the necessary cap

    x <= beta - (1-beta)^2/(4 beta),

which is approximately 0.898028387708521 at R = B*. Such a high-investment
state must be excluded by any globally B*-competitive strategy. Finding a
continuation from that state is not a substitute for forcing the strategy
there, or forcing a different violation when it avoids it.

**The topology restriction deserves a separate decision.** In the present
two-pool phase protocol, each old pool receives phase edges from only its
preceding and following layers. Terminal private leaves change the possible
degree bound, but do not restore repeated future use of an old pool.

Consequently this family does not literally contain arbitrarily many phases
of the complete-bipartite alternating construction: those phases reconnect
later opposite-side arrivals to vertices from much earlier phases. The
strictly retired protocol forbids those edges. This noncontainment is not an
upper bound on the two-pool family's value. It does mean the candidate has
discarded a forcing mechanism known to work and needs an identified
replacement mechanism, not just cycles and exact comparator bookkeeping.

Tang's matching construction also does more than alternate two fixed pools:
it retains active partitions, can create additional active partitions, and
selectively deactivates subsets. These are structural ideas worth auditing
for cover. Its matching payoff cannot be reused: for the paired Wang–Wong
algorithms, C_A = B* M_A, so matching-hard inputs make the paired cover nearly
optimal. An offline duality argument supplies no missing online reduction.

The current restrictions strengthen the algorithm in other ways: whole pool
sizes and the retirement protocol are public, and future continuations never
split a pool. Those are valid lower-bound choices, but may weaken the
adversary substantially. If selective reuse or splitting becomes necessary,
pool averages alone cannot automatically remain the state. For example, the
vectors (0,1) and (1/2,1/2) have the same average but different costs when a
future neighbor singles out a lowest-coordinate vertex. Relabeling or
averaging cannot erase irreversible individual coordinates.

**There is a small exact simplification available before new search.** For
the same-side boundary {a,c}, write the reweighted table as

    (H00,H10,H01,H11) = (c+p+q+k, c+q+k, c+p+k, c).

Replace the pair (A,c) by s = A-c. The terminal surplus becomes

    s - min {p+q+k,
             w_a(beta+x_a)+q+k,
             w_c(beta+x_c)+p+k,
             w_a(beta+x_a)+w_c(beta+x_c)}.                 (R1)

Adding the same constant to A and all four table entries changes neither
terminal surplus nor future surplus. No old graph is replaced by making
this accounting substitution.

For a full phase, put theta_a = w_a(beta+r_a) and
theta_c = w_c(beta+r_c), using their actual coordinates at retirement, and
define

    m = min {p+q+k, theta_a+q+k, theta_c+p+k,
             theta_a+theta_c}.

Equation (5) of `COMPLETION_GAME.md` gives c_new = c+m, hence

    s_new = s + Delta - m.                                (R2)

Here Delta includes both arrival decisions and all actual coordinate
increments. The remaining p,q,k updates are the existing phase algebra
with retiring weights theta_a,theta_c. Stop after the first arrival must
still be evaluated on the mixed-side boundary.

The core state is therefore (w_a,w_c,x_a,x_c,p,q,k,s), together with protocol
position and graph/cover backpointers. With scale-covariant action menus,
weights, table costs, and surplus can also be normalized by a common positive
scale. This is a property of the mathematical game, not an assumption that
an arbitrary algorithm is scale-invariant. A fixed absolute size menu cannot
silently be normalized into a different menu. The reachable normalized set
has not been shown compact or invariant.

The response theorem also needs a precise interface in the new game. Its
convexity proof was stated for the old fixed offline table. Reweighted
retirement makes H depend on the response. Apply the theorem before
retirement to the actual graph's continuation function, with old coordinates
still explicit; prove that compression yields the same value afterward.
Alternatively prove the required joint convexity and monotonicity in the
table entries. Treating H_new as fixed while the retiring coordinates vary
would omit part of the payoff. No failing identity was found in the local
tests; this is an integration proof obligation that the synthetic tests do
not discharge.

The recommended work order is the following.

1. **Specify one complete finite game.** Fix the two initial isolated pools,
   finite integer size and neighborhood menus, allowed retirements, terminal
   completions, public announcements, and stopping after either new pool.
   Use (R1)–(R2), retain actual graph witnesses, and establish the response
   theorem across response-dependent retirement. This replaces an informal
   candidate with a precisely evaluable mathematical object.

2. **Give that game a bounded forcing-versus-safety investigation.** Compose
   graph-realized terminal values through two full alternating phases,
   including asymmetric weights and intermediate stops. Work at selected
   trial ratios B* - epsilon; do not optimize a sequence of incidental lower
   constants. Minimize over the full response interval exactly. Extract both
   the adversarial branch certificates and a player response rule. Inspect
   whether shared liability actually grows after paying the normalized
   retirement cost m. Then attempt one symbolic invariant or recursive
   amplification lemma suggested by those certificates. A larger horizon
   should test a specific such lemma, not stand in for one. Use the existing
   tools and small symbolic compositions; a general Bellman solver is not a
   deliverable for this step.

3. **Make an explicit family decision.** Continue the strictly retired
   completion game only with a concrete amplification mechanism or a
   structured unsolved inequality. An exact invariant safety strategy below
   B* eliminates its stated scope. If the bounded investigation produces
   neither certificate, record the candidate as unvalidated and move the
   main effort to selective persistence rather than expand the same search
   indefinitely. Numerical stability or a low finite-horizon value is not
   a mathematical upper bound.

4. **If needed, restore the missing structural operation.** Start with a
   persistent old pool, partial retirement, or a retained active partition,
   chosen to defeat an identified response rule. Give the exact graph,
   public information, and conditional comparator update first. General
   active boundaries use their full conditional table. If a continuation
   distinguishes members of a pool, retain their profile or prove a valid
   extremal reduction; do not merge histories because their averages match.
   Calibrate any claimed general alternating model against Lu's finite
   recurrence. This is a model check, not a new lower-bound milestone.

5. **Derive the limiting necessary inequalities from the chosen graph game.**
   Only then compare their critical constant with B*. If a scalar response
   envelope f can be extracted, prove its domain, quantifiers, positivity,
   and regularization, or use a justified relaxed function class. The
   original minimax is a benchmark to explain, not an adversary oracle.
   A multivariable or profile-valued limit may be the correct result.

6. **Finish with an explicit finite-witness bridge.** Preserve strict surplus
   after rational size approximation, response elimination, and horizon
   truncation. Record an accumulated error bound and the actual terminal
   cover/matching certificate. Expand integer pools into sequential
   unweighted arrivals. Choose branches using deterministic expected
   marginals at public histories, not realized random choices. This gives
   the required algorithm-dependent fixed input; a single hard distribution
   for every algorithm is a separate, optional minimax deliverable.

Lower and upper diagnostics have different scopes. A lower certificate using
a finite action submenu proves a valid lower bound for the original problem.
An upper strategy against that submenu is only a submenu upper bound. A
finite-horizon strategy is not an all-horizon strategy. Sampling player
responses can falsely increase a lower bound by restricting the algorithm;
use exact scalar elimination or a rigorous response-error allowance. Every
supporting plane used for hardness needs graph provenance or an inductive
lower-bound derivation, not merely admissible slopes.

The next concrete deliverable should be one of: a graph-realized recursive
forcing lemma with an initial-state consequence; a below-B* safety invariant
for a precisely stated candidate family; or a documented counterstrategy
failure motivating one specific legal extension. More local check counts,
larger generic LPs, and the assumed 0.9 investment state do not satisfy that
deliverable. The main target remains exact optimality, with the possibility
that the conjectured value is false kept logically open.

Primary sources used for the assessment:

- [Wang and Wong](https://arxiv.org/abs/1305.1694), original algorithm,
  optimization and open questions.
- [Tang](https://arxiv.org/abs/2602.18049), fractional matching optimality
  and active-partition construction.
- [Lu](https://arxiv.org/abs/2608.09210), cover lower bound and the scope
  of the critical recurrence.
- [Baligacs et al.](https://doi.org/10.4230/LIPIcs.ESA.2026.158), online
  forest upper bound.
- [Buchbinder, Segev and Tkach](https://doi.org/10.4230/LIPIcs.ESA.2017.22),
  explicit bounded-degree primal-dual algorithm.

The previous resume plan is preserved as `SESSION_4_PLAN.md`. The active
execution plan is now `NEXT_SESSION.md`. At the time of this review, the
repository was initialized but had no commits. The user subsequently requested
commits by default; the workflow is recorded in the root `AGENTS.md`.
