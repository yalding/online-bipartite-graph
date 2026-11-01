# Session 3: construction audit and exact boundary accounting

Date: 2026-11-01 (America/Los_Angeles).

The requested universal hardness construction approaching
1.9007616968738465... has **not** been obtained. The hypothesis is neither
proved nor disproved here. No stronger universal lower bound is claimed.

## Mathematical results

1. Proved that the existing blueprint deletion cleanup, including its final
   private-leaf completion, always produces a forest. Located and read the
   source of Baligacs et al.'s forest cover algorithm (arXiv:2608.24630v1,
   Theorem 3), which gives an 11/6 upper bound even under edge arrivals.
   Therefore the entire cleanup route cannot reach the target. It also
   imposes F <= (5/3)(n-m), hence asymptotic F/m <= 5/6 at blueprint value
   2/3. This replaces the earlier suggestion to try larger cleanup MILPs.
2. Tested a cycle-preserving replacement for each illegal late edge: a
   three-edge path with two fresh internal vertices. Derived an explicit
   integral online algorithm with ratio at most 3/2 on this whole encoding
   family. A matching certificate proves the bound at every vertex prefix,
   including a stop after the first internal vertex. This rules out that
   replacement even on general original graphs.
3. Derived an exact conditional-cost table for retired regions of a bipartite
   pool graph, its fractional threshold extension, and its update on adding
   and retiring pools. Gave a concrete pair of histories with identical
   coarse all-out/all-in costs and current optimum, but future optima 4 and
   3 under the same continuation. This identifies a specific invalid state
   compression rather than assuming an arbitrary algorithm is scalar.
4. Wrote a finite minimax recurrence using those interfaces, online boundary
   averages, and sunk cost. Its legal finite menus handle all batch-player
   responses and allow marginalization of randomized algorithms.
5. Proved that with exactly two same-side boundary pools the offline table
   has four nonnegative parameters, with fractional cost

       c0 + p(1-x_a) + q(1-x_c) + k(1-min(x_a,x_c)).

   This class closes under an alternating two-pool phase containing a
   K_2,2 cycle. The phase update is a minimum over four subsets. This gives
   a specific small state for a direct construction attempt. It does not
   solve its minimax recurrence or establish its limiting ratio.

Proofs: `CONSTRUCTION_OBSTRUCTIONS.md` and `BOUNDARY_STATE.md`.

## Exact verification

Run `python scripts/construction_obstructions.py`. The saved output is
`experiments/construction-obstructions.json`. No optimizer is run.

* 4,080 fixed-boundary cases on every 2+2 bipartite graph agree with exact
  half-grid cover enumeration. Bipartite total unimodularity ensures a
  half-grid optimum for these half-grid boundary values.
* 1,040 retirement tables agree with direct cover enumeration.
* 4,608 alternating two-pool phase updates agree with covers of the actual
  graphs, testing all 3+3 old bipartite graphs and the nine nonempty
  neighborhood pairs. The four-parameter representations are nonnegative.
* All 75,972 oriented ordered completed-gadget prefixes on four originals,
  and the corresponding 75,972 halfway prefixes, satisfy the subdivision
  algorithm's 3/2 bound against an explicit feasible matching.
* Reconstructed all 60 shifts in the four saved cleanup experiments;
  union-find verified acyclicity, and rational forcing credits agree with
  the existing files and the analytic forcing cap.

These are finite checks supporting the proofs. They do not verify the
universal conjecture, establish a new lower constant, or solve the new game.

## Sources and operational record

Rechecked primary arXiv pages and searched for later general vertex-arrival
results. No paper settling the remaining cover question was located.
Downloaded the forest paper's pinned PDF and source, extracted its text,
and recorded SHA-256 hashes in `papers/manifest.json`. There are now eight
papers. The first download attempt failed on sandbox DNS; the authorized
network retry succeeded. Existing pinned paper hashes remain unchanged.
No agents were spawned and no external messages were sent.

## Exact remaining obstacle

The original allocation-function minimax remains an upper-bound analysis.
Nothing here proves its inequalities necessary for arbitrary online cover
strategies. The two-pool closed state offers a way to seek such a reduction
without losing old edges, but a surplus inequality attaining the exact
constant, and the consequent finite strict violation, are still missing.
