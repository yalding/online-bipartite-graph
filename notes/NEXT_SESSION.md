**Resume after the deep research review — November 1, 2026**

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
