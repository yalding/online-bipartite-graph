"""Exact response certificates and phase identities for the session-4 candidate.

These are local game calculations, not a universal hardness certificate.
Run with --lp-check to compare the exact scalar answer with an unrestricted
floating LP. Every saved response certificate is checked with Fractions.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]


def response_lines(weights, x, b, neighbors, planes):
    """Continuation planes are (intercept, old slopes, new slope).

    Require -w_i <= old slope_i <= 0 and -b <= new slope <= 0.
    Expand each positive-part term into its two affine alternatives.
    """
    neighbors = tuple(neighbors)
    lines = []
    sunk = sum(w * a for w, a in zip(weights, x))
    for j, (intercept, slopes, new_slope) in enumerate(planes):
        assert all(-w <= s <= 0 for w, s in zip(weights, slopes))
        assert -b <= new_slope <= 0
        coefficients = [w + s for w, s in zip(weights, slopes)]
        for bits in product((0, 1), repeat=len(neighbors)):
            raised = {i for i, bit in zip(neighbors, bits) if bit}
            c = intercept - sunk + sum(
                a if i in raised else a * x[i]
                for i, a in enumerate(coefficients))
            m = b + new_slope - sum(coefficients[i] for i in raised)
            lines.append((F(c), F(m), j, tuple(sorted(raised))))
    return lines


def solve_lines(lines):
    """Minimize max_j(c_j + m_j*t) on [0,1], with an exact dual witness."""
    candidates = {F(0), F(1)}
    for (c, m, *_), (d, n, *__) in combinations(lines, 2):
        if m != n:
            t = (d - c) / (m - n)
            if 0 <= t <= 1:
                candidates.add(t)
    value, t = min((max(c + m * u for c, m, *_ in lines), u)
                   for u in candidates)
    active = [j for j, (c, m, *_) in enumerate(lines) if c + m * t == value]
    certificate = None
    for j in active:
        slope = lines[j][1]
        if slope == 0 or (t == 0 and slope >= 0) or (t == 1 and slope <= 0):
            certificate = [(j, F(1))]
            break
    if certificate is None:
        lo = next(j for j in active if lines[j][1] < 0)
        hi = next(j for j in active if lines[j][1] > 0)
        a, z = lines[lo][1], lines[hi][1]
        certificate = [(lo, z / (z - a)), (hi, -a / (z - a))]
    assert sum(lam for _, lam in certificate) == 1
    assert all(lam >= 0 for _, lam in certificate)
    c = sum(lam * lines[j][0] for j, lam in certificate)
    m = sum(lam * lines[j][1] for j, lam in certificate)
    assert c + min(F(0), m) == value
    return value, t, certificate


def full_response_lp(weights, x, b, neighbors, planes):
    """Independent formulation permitting all proactive old-coordinate raises."""
    sys.path.insert(0, str(ROOT / '.research-deps'))
    from scipy.optimize import linprog
    n = len(weights)
    rows, rhs = [], []
    for i in neighbors:
        row = [0] * (n + 2)
        row[i] = row[n] = -1
        rows.append(row)
        rhs.append(-1)
    for intercept, slopes, new_slope in planes:
        rows.append([float(s) for s in slopes] + [float(new_slope), -1])
        rhs.append(-float(intercept))
    result = linprog(list(weights) + [b, 1], A_ub=rows, b_ub=rhs,
                     bounds=[(float(a), 1) for a in x] + [(0, 1), (None, None)],
                     method='highs')
    assert result.success, result.message
    return result.fun - float(sum(w * a for w, a in zip(weights, x)))


def response_checks(lp_check=False):
    rng = random.Random(20261101)
    count, comparisons = 0, 0
    example = None
    for _ in range(600):
        weights = tuple(rng.randint(1, 4) for _ in range(2))
        b = rng.randint(1, 4)
        x = tuple(F(rng.randrange(5), 4) for _ in range(2))
        neighbors = rng.choice(((0,), (1,), (0, 1)))
        planes = [(F(rng.randrange(-20, 21), 3),
                   tuple(F(rng.randint(-w, 0)) for w in weights),
                   F(rng.randint(-b, 0))) for _ in range(3)]
        lines = response_lines(weights, x, b, neighbors, planes)
        value, t, certificate = solve_lines(lines)
        r = tuple(max(a, 1 - t) if i in neighbors else a for i, a in enumerate(x))
        direct = sum(w * (a - old) for w, a, old in zip(weights, r, x)) + b * t
        direct += max(c + sum(s * a for s, a in zip(slopes, r)) + sn * t
                      for c, slopes, sn in planes)
        assert direct == value
        # Check the certificate's global lower affine bound on nonminimal
        # feasible responses too. The proof covers the full continuous cube.
        for u, a, z in product((F(0), F(1, 2), F(1)), repeat=3):
            rr = (a, z)
            if any(a < old for a, old in zip(rr, x)):
                continue
            if any(rr[i] + u < 1 for i in neighbors):
                continue
            cost = sum(w * (a - old) for w, a, old in zip(weights, rr, x)) + b * u
            cost += max(c + sum(s * a for s, a in zip(slopes, rr)) + sn * u
                        for c, slopes, sn in planes)
            assert cost >= value
        if lp_check:
            result = full_response_lp(weights, x, b, neighbors, planes)
            assert abs(result - float(value)) < 1e-8, (result, value)
            comparisons += 1
        if example is None and 0 < t < 1 and len(certificate) == 2:
            example = dict(weights=weights, old_coordinates=list(map(str, x)),
                           new_weight=b, neighbors=neighbors,
                           continuation_planes=[dict(intercept=str(c),
                               old_slopes=list(map(str, ss)), new_slope=str(sn))
                               for c, ss, sn in planes],
                           exact_value=str(value), response=str(t),
                           supporting_lines=[dict(intercept=str(lines[j][0]),
                               slope=str(lines[j][1]), multiplier=str(lam))
                               for j, lam in certificate])
        count += 1
    return dict(exact_response_certificates=count, unrestricted_lp_comparisons=comparisons,
                interior_two_line_example=example)


def phase_checks():
    checked = 0
    shapes = ((0,), (1,), (0, 1))
    masks = (0, 1, 2, 3)
    for a, c in product(range(1, 5), repeat=2):
        for p, q, k in product(range(4), repeat=3):
            old = (p + q + k, q + k, p + k, 0)
            g = tuple(old[mask] + (a if mask & 1 else 0) +
                      (c if mask & 2 else 0) for mask in masks)
            h = tuple(min(g[z] for z in masks if z & mask == mask) for mask in masks)
            alpha, gamma, kap = (h[i] - h[0] for i in (1, 2, 3))
            parallel = max(0, min(k, a - p) + min(k, c - q) - k)
            assert parallel == alpha + gamma - kap
            assert 0 <= parallel <= k
            for nb, nd in product(shapes, repeat=2):
                mb = sum(1 << i for i in nb)
                md = sum(1 << i for i in nd)
                table = (h[mb | md], h[md], h[mb], h[0])
                cp, pp, qp, kp = (table[3], table[0] - table[1],
                                   table[0] - table[2],
                                   table[1] + table[2] - table[0] - table[3])
                assert min(cp, pp, qp, kp) >= 0
                if nb != nd and len(nb) == len(nd) == 1:
                    assert kp == parallel
                else:
                    assert pp == 0 or qp == 0
                checked += 1
    return dict(exact_phase_identities=checked,
                parallel_coupling_never_increases=True,
                other_phases_have_at_most_one_positive_private_parameter=True)


def degree_checks():
    results = []
    for degree in range(1, 7):
        total = 2 ** degree - 1
        powers = [2 ** i for i in range(degree)]
        # Every possible load built from at most d-1 previous edge increments.
        loads = {0}
        frontier = {0}
        for _ in range(degree - 1):
            frontier = {s + p for s in frontier for p in powers if s + p <= total}
            loads |= frontier
        assert max(loads) < total
        pairs = 0
        for u, v in product(loads, repeat=2):
            power = max(p for p in powers if p <= total - max(u, v))
            assert max(u, v) + power <= total
            assert u + v + 2 * power >= 2 ** degree
            pairs += 1
        results.append(dict(degree=degree, exact_local_load_pairs=pairs,
                            cover_ratio=str(F(2 * total, 2 ** degree))))
    return results


def local_trap():
    # A conditional state obstruction, not a way to force that state.
    x, r = F(9, 10), F(1, 20)
    lines = [(1 + x, r, 0, ()),
             (1 + 1 / (1 + r), -1 / (1 + r), 1, ()),
             (1 + x / (1 + r), F(0), 1, ())]
    value, t, dual = solve_lines(lines)
    assert value == F(801, 421) and t == F(22, 421)
    return dict(prefix='K_20,20; every old coordinate is 9/10',
                next_arrival='one left vertex adjacent to all 20 old right vertices',
                alternatives='private-leaf completion of R or of L plus the new vertex',
                exact_local_minimax_ratio=str(value), exact_new_coordinate=str(t),
                mixture=[dict(branch=j, multiplier=str(lam)) for j, lam in dual],
                suffix_probabilities=dict(R_completion='20/21', L_plus_v_completion='1/21'),
                expected_cost_lower_bound='801/21', expected_optimum='421/21',
                limitation='No proof that every algorithm can be forced into this prefix state')


def completion_table_checks():
    """Compare the second interface with full weighted-cover enumeration."""
    from construction_obstructions import conditional_table
    checked = 0
    weights = (2, 3, 1, 4, 2, 3)
    masks = ((0, 0), (1, 0), (0, 1), (1, 1))
    shapes = ((0,), (1,), (0, 1))
    old_edges = ((0, 2), (0, 3), (1, 2), (1, 3))
    for edge_bits in product((0, 1), repeat=4):
        edges = [e for bit, e in zip(edge_bits, old_edges) if bit]
        for beta in (F(1, 2), F(9, 10)):
            for xa, xc in product((F(1, 2), F(3, 4), F(1)), repeat=2):
                y = (xa, xc, F(1), F(1), F(1, 2), F(1, 2))
                theta = tuple(w * (beta + a) for w, a in zip(weights, y))
                old = conditional_table(theta[:4], edges, (0, 1))
                for nb, nd in product(shapes, repeat=2):
                    extended = edges + [(i, 4) for i in nb] + [(i, 5) for i in nd]
                    assert all(y[u] + y[v] >= 1 for u, v in extended)
                    direct = conditional_table(theta, extended, (4, 5))
                    for sb, sd in masks:
                        required = set(() if sb else nb) | set(() if sd else nd)
                        predicted = min(theta[0] * a + theta[1] * c + old[(a, c)]
                                        for a, c in masks
                                        if all((a, c)[i] for i in required))
                        assert predicted == direct[(sb, sd)]
                    h00, h10, h01, h11 = (direct[bits] for bits in masks)
                    assert min(h11, h00 - h10, h00 - h01,
                               h10 + h01 - h00 - h11) >= 0
                    best = min(direct[(a, c)] + theta[4] * a + theta[5] * c
                               for a, c in masks)
                    assert best == conditional_table(theta, extended, ())[()]
                    # The maximizing completion's surplus equals sunk cost
                    # minus this reweighted minimum cover, exactly.
                    sunk = sum(w * a for w, a in zip(weights, y))
                    cover_surpluses = []
                    for bits in product((0, 1), repeat=6):
                        if all(bits[u] or bits[v] for u, v in extended):
                            outside = sum(w * a for w, a, s in zip(weights, y, bits) if not s)
                            selected = sum(w for w, s in zip(weights, bits) if s)
                            cover_surpluses.append(outside - beta * selected)
                    assert max(cover_surpluses) == sunk - best
                    checked += 1
    return dict(exact_reweighted_phase_and_completion_cases=checked,
                weights='w_i * (beta + current_coordinate_i)',
                terminal_surplus='sunk_online_cost - minimum_reweighted_cover')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lp-check', action='store_true')
    args = parser.parse_args()
    result = dict(scope='Local two-pool response and phase calculations; universal target unresolved',
                  responses=response_checks(args.lp_check), phases=phase_checks(),
                  dyadic_degree_algorithm=degree_checks(), conditional_trap=local_trap(),
                  completion_interface=completion_table_checks())
    target = ROOT / 'experiments' / 'two-pool-response.json'
    target.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
