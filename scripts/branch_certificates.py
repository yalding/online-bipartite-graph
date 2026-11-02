"""Exact arithmetic checks for the finite witnesses and all-horizon invariants."""

import json
from fractions import Fraction as Q
from pathlib import Path


def tree_witness():
    # Counts are divided by the size of the initial pool (10).
    beta = Q(71, 100)
    step, heavy = Q(1, 10), Q(11, 10)
    spent = sum(step * (1 - beta * i * step) for i in range(1, 10))
    root_floor = 1 - (beta - spent) / heavy
    grandchild_floors = [
        max(0, root_floor - beta * j * step / heavy) for j in range(1, 14)
    ]
    outside = root_floor + step * sum(grandchild_floors)
    budget = beta * (9 * step + heavy)
    assert outside - budget == Q(481, 22000)
    return dict(beta=beta, old_right_cost=spent, root_floor=root_floor,
                outside_cost=outside, budget=budget, strict_excess=outside - budget)


def spine_invariant():
    beta = Q(21, 25)
    knots = [Q(i, 4) for i in range(5)]
    values = [Q(3, 20) * (1-p) + Q(3, 5) * (1-p)**2 for p in knots]
    # Each supporting line is a - b*p. The final line extends over p >= 1.
    lines = [(Q(0), Q(0))]
    for p, end, value, end_value in zip(knots, knots[1:], values, values[1:]):
        b = (value - end_value) / (end - p)
        lines.append((value + b * p, b))
    assert all(max(a-b*p for a, b in lines) == value
               for p, value in zip(knots, values))
    assert values[0] <= beta
    checks = 0
    for p, value in zip(knots, values):
        for ai, bi in lines:
            for aj, bj in lines:
                # A*h^2 + B*h + C must be nonnegative for every h >= 0.
                A = beta - ai
                B = bi * value - 1 + p + beta * bj
                C = value - aj + bj * p
                assert A > 0 and C >= 0
                assert B >= 0 or B**2 <= 4*A*C, (p, ai, bi, aj, bj)
                checks += 1
    return dict(beta=beta, knots=knots, values=values,
                lines=lines, nonnegative_quadratics=checks)


def two_pool_bound():
    # The only nontrivial endpoint comparison reduces to cube_root(4) >= 311/196.
    a, b = Q(6, 7), Q(9, 14)
    c = a - b
    required_root = (a + 2*c - b**3) / (3*c)
    assert a/c == 4 and required_root == Q(311, 196)
    assert required_root**3 < 4
    return dict(beta=a, slope=b, required_root=required_root,
                cube_comparison_margin=4 - required_root**3)


def biclique_probe():
    # On the linear part of Lu's critical profile, 1-D(t) = sqrt(e)*t/2.
    # sqrt(e)/2 > 4/5 follows from e > 1 + 1 + 1/2 + 1/6 > (8/5)^2.
    rounds = 9
    lower_slope = Q(4, 5)
    spent = Q(0)
    old_left = 0
    for j in range(1, rounds + 1):
        left = 2**j
        t = Q(j, left)
        assert t <= Q(1, 2)  # < 1/sqrt(e) since e < 4
        spent += (left - old_left) * lower_slope * t
        old_left = left
    assert spent / rounds > 2
    return dict(rounds=rounds, left=old_left, right=rounds,
                lower_bound_left_cost=spent, lower_bound_ratio=spent / rounds)


if __name__ == "__main__":
    report = dict(tree_witness=tree_witness(), spine_invariant=spine_invariant(),
                  two_pool_bound=two_pool_bound(), biclique_probe=biclique_probe())
    encoded = json.dumps(report, indent=2, default=str) + "\n"
    target = Path(__file__).resolve().parents[1] / "experiments" / "branch-certificates.json"
    target.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
