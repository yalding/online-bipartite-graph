# The original cover algorithm is tight on center-last stars

Derived in this project on 2026-11-01. This is an elementary consequence of
Algorithm 3, not a claim of a new universal online lower bound.

Let `k > 1` solve `k = coth(k)`, put `a=(k+1)/2`, `b=(k-1)/2`, and define

    f(t) = (a-t)^(a/k) (t+b)^(b/k),   B = 1+f(0).

Here `B` denotes the paper's approximately 1.901 competitive guarantee. We use
`B` to avoid confusing it with the excess ratio called beta in Lu's paper.

## Finite unweighted bipartite example

1. Introduce `d` isolated leaves. Algorithm 3 gives each potential zero: its
   maximal feasible water level on arrival is 1.
2. Introduce their common center, adjacent to every leaf.
3. The chosen water level `t_d` is the unique root of `d*t_d=f(t_d)`.
   Every leaf is raised to `t_d`; the center is assigned `1-t_d`.

Therefore

    ALG_d = d*t_d + 1-t_d = 1+f(t_d)-t_d.
    OPT_d = 1.

The allocation function is positive, continuous, and nonincreasing. In fact,
the paper's identity is `f'(t) = -t/f(1-t)`. Thus `d*t-f(t)` is strictly
increasing, is negative at zero, and is positive at one (`f(1)<1`). Its root
is precisely the maximal feasible water level required by Algorithm 3.

Since `t_d <= f(0)/d`, it tends to zero as `d` grows. It follows that

    lim ALG_d/OPT_d = 1+f(0) = B.

This matches the paper's upper guarantee even on unweighted bipartite graphs.
It also applies to the paper's threshold-rounded randomized integral cover:
rounding preserves expected cost exactly when the bipartition is known.

## Explicit error estimate

The identity `f'(s)=-s/f(1-s)` and `f(1-s)>=f(1)>0` give

    0 <= B-ALG_d
       = t_d + f(0)-f(t_d)
       <= f(0)/d + f(0)^2/(2*f(1)*d^2).

Thus a finite degree can be selected for any requested accuracy. No continuum
or infinite input is needed. The script uses high precision arithmetic and
checks the defining root; the convergence and error bound above are analytic.

## Why this does not settle Section 7's optimality question

A different online algorithm can pay only for the center on this particular
arrival sequence. Hence the family proves tightness of GreedyAllocation, not
an impossibility result for arbitrary online algorithms. A universal adversary
must punish an algorithm that anticipates the center being the cheap cover,
as well as algorithms that invest early in leaves.

Source: Wang--Wong, Algorithm 3 and Section 4,
https://arxiv.org/abs/1305.1694 .

Reproduce: `python scripts/star_tightness.py`.
Outputs: `experiments/star-tightness.json` and
`experiments/center-last-star-1000.json`.
