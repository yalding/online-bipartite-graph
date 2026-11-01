# Explicit finite oblivious hardness distributions

The session-2 sparse LP can export a fixed rational distribution of complete
inputs, not merely an adaptive algorithm-dependent witness. This is a concrete
reproduction tool; the resulting constants do not improve the known bound.

## Certificates

| Distribution | Inputs | Vertices per expanded input | Certified ratio |
|---|---:|---:|---:|
| `biclique-6-12-3-ext-yao.json.gz` | 624 | 8--64 | 1764759524/999995889 = 1.764766778956... |
| `adaptive-biclique-m10-p5-yao.json.gz` | 480 | 120--5,440 | 1781280579/999885815 = 1.781483997750... |

A later general-graph pilot additionally exports
`general-5-1-4-subset-yao.json.gz` with seven inputs and certified ratio
`1641025601/999999980 = 1.6410256338...`. It does not improve the bound and its
support shows no odd-cycle advantage. General exports mark the comparator as
fractional; half-integral optima are verified against exact LP dual witnesses.

Files are under `experiments/`. A group is an independent twin set with the
given integer cardinality. Its neighborhood lists earlier group indices;
each such adjacency expands to a complete biclique. Group sizes may be
revealed at arrival, which strengthens the algorithm. Hence lower bounds for
this batch player remain valid for ordinary sequential vertex arrivals.

Each input has an integer weight. Its probability is that weight divided by
`probability_denominator`. All offline optima in the exported distribution
are independently recomputed, and their weighted sum is checked against the
dual normalization. Scaling every group cardinality preserves the game and
makes an additive competitive constant negligible.

## Exact normalized-dual argument

Let A*x<=b be the online feasibility and cost LP, with x_0 the competitive
ratio and all other variables cover coordinates in [0,1]. Choose arbitrary
nonnegative integer row multipliers lambda. Let

    Q = -(A^T lambda)_0 > 0,
    r_j = max(0,-(A^T lambda)_j) for j>0.

Add r_j times the valid constraint x_j<=1. After division by Q, the ratio
column equals -1 and every cover-coordinate column is nonnegative. Weak
duality gives the exact lower bound

    [-lambda*b - sum_j r_j]/Q.

No feasibility assumption about floating multipliers is needed: their integer
roundings and every repaired column are checked directly. No cap on the
competitive ratio is needed for this normalized certificate.

Multipliers of cost and continuation rows determine the distribution on actual
inputs. A continuation row is replaced by its explicit private-leaf or
universal-extension completion. The other dual rows are graph feasibility
and nonanticipation constraints. This is the standard factor-revealing LP
duality mechanism, with exact residual repairs.

## Independent check against actual inputs

`scripts/check_yao_distribution.py` rebuilds all actual public input histories
and minimizes expected cost. It includes only edge feasibility, monotonicity,
and potential caps. It assumes no competitive ratio and no continuation
budgets. The numerical optima are 1.764767250958... and 1.781512687026...,
respectively, both above the independently certified lower bounds.

Reproduce without solving the original minimax LP:

```powershell
python scripts/sparse_adversary_lp.py --verify experiments/biclique-6-12-3-ext.json --export-yao --check-known
python scripts/sparse_adversary_lp.py --verify experiments/adaptive-biclique-m10-p5.json --export-yao
python scripts/check_yao_distribution.py experiments/biclique-6-12-3-ext-yao.json.gz
python scripts/check_yao_distribution.py experiments/adaptive-biclique-m10-p5-yao.json.gz
```

The first command also confirms that the known Wang--Wong weighted algorithm
satisfies every candidate LP inequality at its proven ratio. It is a useful
check against proposing an invalid lower-bound constraint.
