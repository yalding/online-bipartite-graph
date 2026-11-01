# Legalizing a blueprint by deleting late old-old edges

**Session-3 correction:** this cleanup always yields a forest, including
the final private leaves. A verified literature upper bound of 11/6 on
forests therefore rules out reaching the target with this route at any
scale. See `CONSTRUCTION_OBSTRUCTIONS.md`. The calculations below remain
valid, but the proposed larger-scale continuation at the end is superseded.

Session 2 exploratory reduction. No improved universal bound has been obtained.
The starting proper-blueprint construction is from Assadi--Jiang--Xiang and
its hidden-independent-set use is from Tang--Zhang's edge-arrival paper:

- https://arxiv.org/abs/2607.14656
- https://arxiv.org/abs/2608.04994

Their matching batches cannot simply be called vertex arrivals. We tested the
following explicit legal replacement, rather than assuming such a transfer.

## Cleanup rule

Process the prescribed batches in their original order. A vertex is introduced
when first used by a retained edge. Keep a new edge only when at least one of
its endpoints is still unintroduced. If both endpoints are new, introduce one
as an isolate and the other with this edge. Repeated already-retained edges
need not be revealed again but remain usable covering inequalities. Delete a
new edge whose endpoints have both previously arrived.

This is a legal vertex-arrival input: later retained edges never connect two
old vertices. At the end introduce every remaining vertex as an isolate, then
attach the private leaves outside the hidden independent set.

## Forcing calculation

Use a proper blueprint with n=C^P labels on each side and m matching edges.
Let g_e(z_<p) be the fraction of the phase-p matching batch for blueprint edge
e that either survives cleanup or was already retained. It depends only on the
public shift prefix z_<p. Define

    F = sum_e E_Z[g_e(Z_<p)].

Condition on that public prefix. The remaining cyclic-shift suffix is uniform.
The expected sum of potentials of the two hidden endpoints of e is the
average sum over its matching batch. Surviving/already-present edges contribute
at least one; deleted pairs contribute at least zero. Hence its expectation is
at least g_e. Blueprint matching makes all hidden endpoints distinct, and
properness makes the hidden set independent even before deletion. Therefore

    E_Z[weight on hidden independent set] >= F.

Adding private leaves outside that set gives a fixed oblivious distribution
with competitive-ratio lower bound

    1 + F/[2(n-m)].

This proof permits the algorithm to know vertex labels and the blueprint: the
unrevealed shift suffix is still independent of its observed prefix. The
definition of every retained batch is independent of the algorithm's seed.

## Quantitative target and present limitation

If m/n tends to 2/3 and the average retained forcing fraction F/m tends to rho,
the resulting ratio tends to 1+rho. Thus exceeding the current 1.82436 lower
bound would require rho>0.82436; matching the 1.90076 algorithm would require
rho approaching 0.90076. Perfect forcing still requires blueprint value at
least 0.6430513476 to reach the latter target.

The small MILP probes in `scripts/vertex_blueprint_probe.py` have not come
close. Some timed-out MILPs return poor feasible blueprints; the script checks
matching, every ban constraint, and independence for every shift directly.
Their solver dual bounds are not mathematical certificates and are not used
in the argument. These experiments establish no barrier for larger structured
blueprints. The next meaningful test needs a structured random-walk blueprint
and a symbolic or efficient probabilistic analysis of its cleanup loss.
