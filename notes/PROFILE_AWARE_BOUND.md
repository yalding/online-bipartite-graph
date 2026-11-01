# A profile-aware initial-phase necessary condition

Session 2, 2026-11-01. This strengthens one necessary profile inequality but
has not improved the universal competitive lower bound.

Normalize an initial isolated left pool to mass 1. Introduce right vertices
continuously up to mass s. Suppose d(u) is a valid lower bound on the birth
weight of the right vertex arriving at index u. Initially Lu's global
birth-deficit bounds supply such a d. Subsequent iterations below describe
this special initial-phase history, not arbitrary histories.

Let D be a globally valid birth-deficit profile for arbitrary complete-bipartite
histories and write H(q)=integral_q^infinity D(u) du. Consider a counterfactual
phase growing the left side to mass r>=1. If its newest vertex has weight a,
all s old right vertices must have weight at least 1-a. Consequently their
current cost is at least

    F_d(s,1-a) := integral_0^s max(d(u),1-a) du.                (1)

If the right side is subsequently extended, global birth deficits and the
finite continuation budget cap that same old right cost by

    C_D(s,r) := r [ beta - H(s/r) ].                          (2)

This proves the necessary inequality F_d(s,1-a)<=C_D(s,r). Define

    W_d(s,c) = max{ w in [0,1] : F_d(s,w)<=c },
    A_d(s,r) = 1-W_d(s,C_D(s,r)).                            (3)

If c<F_d(s,0), the prefix already contradicts competitiveness. Otherwise
A_d is a lower bound on each new left birth weight. The initial old left
pool retains weight at least 1-q(s), where q(s) is the last initial-phase
right birth weight. Its own continuation budget gives

    q(s) >= E_D[d](s)
          := [1-beta*s + integral_1^infinity A_d(s,r) dr]_+.  (4)

Thus d can be replaced by max(d,E_D[d]) **for the initial one-sided phase**.
It cannot be substituted for D in arbitrary histories without a further proof:
old opposite vertices might all have arrived isolated, with birth weight zero.
This distinction prevents a tempting but invalid recursive strengthening.

## Critical-profile numerical experiment

For Lu's critical D*, beta=sqrt(e)/2 and integral D*=0.6727279704... .
Its residual budget is positive, beta-integral D*=0.1516326649... .
The linear lower bound

    C_D(s,r) >= r*(beta-integral D)

implies A_d(s,r)=0 once r>=s/(beta-integral D), provided F_d(s,1)=s.
This supplies a finite quadrature endpoint for the experiment.

`scripts/profile_iterate.py --n 800 --steps 10` gives initial and updated
integrals approximately

    0.67272978 -> 0.70265158 -> 0.70266232.

The slight difference in the initial integral from its analytic value is
quadrature error. No budget violation occurs, and the minimum numerical
capacity slack remains about 0.1217. The 200-cell calculation has the same
qualitative outcome. These are exploratory floating calculations, not a proof
that this enriched operator can never help.

## Remaining obligations for a lower-bound theorem

Equations (1)--(4) have finite-sum analogues: use integer block cardinalities,
the old birth weights, and finite counterfactual extensions. Before claiming
any improved constant from a numerical violation, prove directed bounds for
these finite sums and the common-history assumptions. In particular, do not
silently promote an initial-phase bound to a universal birth bound.

A deeper approach must retain the current distribution of old potentials,
not just this single initial birth profile.
