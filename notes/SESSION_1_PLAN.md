# Resume here

User objective: investigate whether the Section 7 ratios in Wang--Wong are
optimal and construct hardness examples. Continue the remaining **universal
fractional vertex-cover** question. Keep plans, findings, and failed approaches
in this folder and give progress updates during work.

## Read first

1. `RESEARCH_STATUS.md`: literature and distinctions between three notions of tightness.
2. `STAR_TIGHTNESS.md`: algorithm-specific cover tightness is already settled.
3. `SESSION_LOG.md`: completed computations and limitations.

Do not redo the literature search or the star proof unless new evidence requires
it. Do not infer cover hardness from matching hardness. No subagents have been
authorized. No external messages or publication have been authorized.

## Priority 1: expand the finite adversary search

The rational LP tool is `scripts/finite_adversary_lp.py`. It builds one cover
coordinate per vertex/group and **public prefix**, imposes monotonicity along
parent-child histories, covers every current edge, and bounds cost by `B*OPT`
at each allowed stopping point. It solves the primal and dual and checks both
with exact arithmetic. The objective is the best possible ratio within the
specified finite game. Randomized algorithms are covered by expected marginals.

The next useful extension is **arbitrary prescribed prefix families**, not
exhaustive enumeration of every small graph. Add a JSON loader and store each
node's public observation, parent, new pool, neighborhood, and group size.
Group labels and group sizes may be revealed to strengthen the player, which
preserves a hardness lower bound. Do not merge distinct information histories
merely because side counts coincide.

Then search a small library of operations:

- add a new twin pool adjacent to one active pool;
- add a pool adjacent to a chosen union of existing opposite-side pools;
- stop, or give private future neighbors to selected pools;
- split a pool into future-distinguishable subsets (handle public history and
  pre-split potential distribution carefully; averaging may cease to suffice).

Start with multiple pool sizes such as 1, 4, 16 and conditional continuations.
Use a floating LP solver for discovery if the rational solver becomes too slow,
then recover and verify exact rational dual certificates. SciPy is **not**
installed in the active Python as of this checkpoint; NumPy, SymPy, mpmath,
requests, and pypdf are present. Do not confuse a numerical solver value with
a proof. No improvement beyond 1.82436 has been found here.

## Priority 2: track offline cover information in a recursion

Tang's matching recursion counts deactivated vertices using a perfect matching.
For cover, retiring a pool does not erase its edges to active pools. A scalar
"old sunk cost" is therefore unlikely to be enough.

For a rooted tree of twin pools, retain two offline costs at each boundary:

    I_v = w_v + sum_children min(I_child, O_child)
    O_v =       sum_children I_child.

`I_v` means the whole boundary pool is selected, `O_v` means it is omitted;
`w_v` is its cardinality. This exactly computes an optimal cover of the
complete-biclique blow-up of a pool tree. It supplies a concrete comparator
state for a possible recursion. General pool graphs need a larger boundary
state or a min-cut calculation.

Try to derive a recurrence that tracks algorithm cost, boundary potential,
and these two comparator values. Use the finite LP dual to identify useful
linear combinations before attempting an analytic fixed point.

Success criterion for an initial advance: a rigorously verified new necessary
inequality that is not implied by Lu's homogeneous recurrence. A ratio below
the known lower bound is only a regression test, not progress on the open bound.

## Priority 3: do not neglect the algorithmic direction

The star example exposes a concrete inefficiency: on a single large new star,
GreedyAllocation spends almost `f(0)` on leaves although buying the center
costs one. A better algorithm could condition allocation on the distribution
of old potentials or neighborhood structure, rather than one fixed `f(y)`.
Any proposed modification must be tested against subsequent arrivals that make
the old leaves useful and against overlapping neighborhoods.

The hypothesis "the optimum is below 1.9007616969" remains viable. Try to
falsify the conjectured tightness instead of optimizing only toward 1.901.

## Optional follow-up

- Read the full 2019 rounding proof and the EC 2024 matching algorithm; PDFs
  and sources are already saved but only their relevance was checked.
- Build an explicit finite witness extractor for Lu's counterfactual recurrence.
  The existing integer certificate is not such an extractor.
- Read the August 2026 edge-arrival blueprint reduction for ideas, while
  explicitly identifying which edges would violate vertex-arrival revelation.
- Inspect the stronger condition `current total cost <= B*min(m,n)` together
  with continuation budgets on homogeneous prefixes. Lu's fixed-point barrier
  is a limitation of that recurrence, not a proof that every possible argument
  on complete-bipartite prefixes has the same barrier.

## Reproduction

From `D:\Users\yaldi\online-bipartite-graph`:

```powershell
python scripts/star_tightness.py
python scripts/cover_recurrence.py --certificate
python scripts/finite_adversary_lp.py --vertices 5
python scripts/finite_adversary_lp.py --vertices 4 --sizes 1,4 --root-size 4
```

Network access is only needed for `scripts/fetch_papers.py`. All five pinned
papers are already present and recorded in `papers/manifest.json`.
