# Session 4: response elimination and a stronger completion game

Date: 2026-11-01 (America/Los_Angeles).

The universal hardness target B=1.9007616968738465... has not been obtained.
No improved universal lower bound is claimed. This session analyzed the
previous concrete candidate and changed it in response to a structural limit.

## Results and their roles

1. Supplied a lazy simulation of arbitrary strategies: one new-pool response
   is a scalar birth coordinate and minimal necessary neighbor raises, while
   retaining unrestricted dependence on past history. Proved the finite
   continuation value is convex, polyhedral, nonincreasing, and coordinatewise
   Lipschitz with constants equal to pool cardinalities. An explicit expansion
   reduces a response to a maximum of affine lines, with an exact optimality
   certificate supported on at most two lines. This advances the response
   analysis; it does not extract a universal f or realize arbitrary planes.
2. Classified the nine two-pool phase choices. Parallel transport cannot
   increase the shared comparator parameter; other phases leave at most one
   positive private parameter. These are exact algebraic restrictions, not a
   bound on the whole unequal-weight game's value.
3. Located and audited Buchbinder--Segev--Tkach (ESA 2017), Algorithm 2 /
   Theorem 6. Its explicit fractional cover algorithm gives 15/8 on degree-four
   graphs. Consequently the equal-size, announced-batch specialization of the
   strictly retired two-pool game cannot reach B. Unit-size pools have the
   same obstruction at every vertex prefix. Arbitrary unequal weights and
   unannounced partial batches are outside this statement.
4. Gave a finite conditional trap: on K_20,20 with old-left cost at least 18,
   add one universal left vertex and then choose private leaves for R or L+v
   with probabilities 20/21 and 1/21. Every response then has conditional
   expected ratio at least 801/421=1.9026128266... . This is a state obstruction,
   not universal hardness: the requisite state has not been forced. It is a
   concrete instance of the existing continuation-budget mechanism.
5. Changed the candidate to allow terminal private-leaf completions, including
   leaves on phase-retired vertices. Derived the exact terminal surplus

       sunk_online_cost - minimum cover with weights w_i*(beta+y_i).

   A reweighted four-entry retired table H captures the needed retired online
   information and closes under phase retirement using the actual coordinates
   at retirement. It provides four graph-realized terminal planes. Ordinary
   stopping is dominated on bipartite inputs, so H can replace the old offline
   table for a fixed-B surplus game; an extra four-parameter table is optional.
   Final leaves can increase quotient degree to five, removing the particular
   15/8 obstruction. The extended game's positive initial surplus remains
   unproved and uncomputed.

Proofs and limitations: `TWO_POOL_RESPONSE.md` and `COMPLETION_GAME.md`.
The latter is the next direct-construction candidate, rather than a claim
that more enumeration of the old game would solve the problem.

## Verification

`python scripts/two_pool_response.py --lp-check` passed:

* 600 exact rational response certificates; each agrees with an independent
  unrestricted-response LP, which permits proactive raises.
* 9,216 exact phase identities, including shared-parameter monotonicity.
* 2,592 reweighted phase and terminal-completion cases against direct covers
  of actual graphs, with nonnegative four-parameter representations.
* All possible local dyadic load pairs for degree bounds 1 through 6; 225
  pairs for degree four. The accompanying global bound has an analytic proof.
* The conditional trap's balancing response, probabilities, and expected
  costs are exact fractions.

Output: `experiments/two-pool-response.json`. Synthetic planes in the response
diagnostic test the elimination lemma only; they are not claimed to be
graph-realizable. No larger adversary LP family was searched.

## Sources and operational record

Read the saved primary sources and searched for relevant degree/weighted
results. The useful additional primary source was
https://doi.org/10.4230/LIPIcs.ESA.2017.22 . Its PDF and extracted text are now
saved, and its SHA-256 is in `papers/manifest.json`. There are nine saved
PDFs and eight arXiv source archives. The fetch script now preserves the
proceedings entry when rebuilding the manifest. The first network attempt
failed at sandbox DNS; the authorized network retry succeeded. No agents
were spawned and no external messages were sent.

## Remaining obligation

Construct a graph-realized envelope propagated by the reweighted phase game
that yields strict positive surplus from its reachable initial state for
every B below the target, and prove its finite limit and obliviousness.
Neither the conditional trap nor synthetic supporting planes can stand in
for this reachability/forcing argument. If an upper strategy below B rules
out the extended family, change the construction again.
