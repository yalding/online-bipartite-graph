"""Exact finite checks of the session-3 mathematical claims.

No numerical optimizer is used. These checks supplement the analytic proofs
in notes/CONSTRUCTION_OBSTRUCTIONS.md and notes/BOUNDARY_STATE.md.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def conditional_table(weights, edges, boundary):
    """Enumerate integral covers, excluding boundary weights from the cost."""
    boundary = tuple(boundary)
    retired = tuple(i for i in range(len(weights)) if i not in boundary)
    table = {}
    for bits in product((0, 1), repeat=len(boundary)):
        best = None
        for tail in product((0, 1), repeat=len(retired)):
            x = dict(zip(boundary, bits)) | dict(zip(retired, tail))
            if all(x[u] + x[v] >= 1 for u, v in edges):
                cost = sum(weights[i] * x[i] for i in retired)
                best = cost if best is None else min(best, cost)
        table[bits] = best
    return table


def threshold_extension(table, boundary, sides, x):
    cuts = sorted({F(0), F(1)} | {
        x[i] if sides[i] == 0 else 1 - x[i] for i in boundary})
    result = F(0)
    for a, b in zip(cuts, cuts[1:]):
        theta = (a + b) / 2
        bits = tuple(int(theta <= x[i]) if sides[i] == 0
                     else int(theta > 1 - x[i]) for i in boundary)
        if table[bits] is None:
            return None
        result += (b - a) * table[bits]
    return result


def boundary_checks():
    # Exhaust all 2+2 bipartite graphs, nonempty boundary sets, and half-grid
    # boundary values. Compare with rational enumeration of retired half-grid
    # covers. Their constraint matrices with half-integral right sides are TU,
    # so a half-grid optimum exists; the general identity has a separate proof.
    vertices = range(4)
    sides = (0, 0, 1, 1)
    candidates = [(u, v) for u in (0, 1) for v in (2, 3)]
    grid = (F(0), F(1, 2), F(1))
    weights = (2, 3, 1, 4)
    checked = 0
    retirements = 0
    for edge_bits in product((0, 1), repeat=4):
        edges = [e for bit, e in zip(edge_bits, candidates) if bit]
        for boundary_mask in range(1, 16):
            boundary = tuple(i for i in vertices if boundary_mask >> i & 1)
            retired = tuple(i for i in vertices if i not in boundary)
            table = conditional_table(weights, edges, boundary)
            for retired_mask in range(1, 1 << len(boundary)):
                moving = tuple(i for j, i in enumerate(boundary) if retired_mask >> j & 1)
                kept = tuple(i for i in boundary if i not in moving)
                direct = conditional_table(weights, edges, kept)
                for bits in product((0, 1), repeat=len(kept)):
                    best = None
                    for tail in product((0, 1), repeat=len(moving)):
                        assignment = dict(zip(kept, bits)) | dict(zip(moving, tail))
                        old = table[tuple(assignment[i] for i in boundary)]
                        if old is not None:
                            cost = old + sum(weights[i] * assignment[i] for i in moving)
                            best = cost if best is None else min(best, cost)
                    assert best == direct[bits]
                retirements += 1
            for values in product(grid, repeat=len(boundary)):
                x = dict(zip(boundary, values))
                best = None
                for tail in product(grid, repeat=len(retired)):
                    y = x | dict(zip(retired, tail))
                    if all(y[u] + y[v] >= 1 for u, v in edges):
                        cost = sum(weights[i] * y[i] for i in retired)
                        best = cost if best is None else min(best, cost)
                predicted = threshold_extension(table, boundary, sides, x)
                assert predicted == best, (edges, boundary, values, predicted, best)
                checked += 1

    shared = conditional_table((2, 2, 2), [(0, 2), (1, 2)], (0, 1))
    separate = conditional_table((2, 2, 1, 1), [(0, 2), (1, 3)], (0, 1))
    assert [shared[b] for b in ((0, 0), (1, 0), (0, 1), (1, 1))] == [2, 2, 2, 0]
    assert [separate[b] for b in ((0, 0), (1, 0), (0, 1), (1, 1))] == [2, 1, 1, 0]
    shared_after = conditional_table((2, 2, 2, 4), [(0, 2), (1, 2), (1, 3)], ())
    separate_after = conditional_table((2, 2, 1, 1, 4),
                                       [(0, 2), (1, 3), (1, 4)], ())
    assert shared_after[()] == 4 and separate_after[()] == 3
    # Exhaust all 3+3 graphs for the four-parameter, same-side closure.
    closed = 0
    candidates = [(u, v) for u in range(3) for v in range(3, 6)]
    for edge_bits in product((0, 1), repeat=9):
        edges = [e for bit, e in zip(edge_bits, candidates) if bit]
        table = conditional_table((2, 3, 4, 1, 2, 3), edges, (0, 1))
        t00, t10, t01, t11 = [table[b] for b in ((0, 0), (1, 0), (0, 1), (1, 1))]
        c0, p, q, k = t11, t00 - t10, t00 - t01, t10 + t01 - t00 - t11
        assert min(c0, p, q, k) >= 0
        for xa, xc in product(grid, repeat=2):
            predicted = c0 + p * (1 - xa) + q * (1 - xc) + k * (1 - min(xa, xc))
            assert predicted == threshold_extension(table, (0, 1), (0, 0), {0: xa, 1: xc})
        # Compare the four-state phase formula to covers of the full actual
        # graph after two arrivals and retirement of both old boundary pools.
        for nb, nd in product(((0,), (1,), (0, 1)), repeat=2):
            extended_edges = edges + [(i, 6) for i in nb] + [(i, 7) for i in nd]
            direct = conditional_table((2, 3, 4, 1, 2, 3, 2, 3), extended_edges, (6, 7))
            for sb, sd in product((0, 1), repeat=2):
                required = set(() if sb else nb) | set(() if sd else nd)
                predicted = min(2 * a + 3 * c + table[(a, c)]
                                for a, c in product((0, 1), repeat=2)
                                if all((a, c)[i] for i in required))
                assert predicted == direct[(sb, sd)]
            closed += 1
    return dict(exact_fractional_interface_cases=checked,
                exact_retirement_tables=retirements, exact_two_pool_phases=closed,
                coarse_state_counterexample_optima=[4, 3])


def subdivision_checks():
    # All ordered simple graphs on four named originals, with both choices
    # of which endpoint is exposed first in every gadget. Check every half
    # gadget prefix too, using an explicit matching as the lower certificate.
    originals = 4
    available = tuple(combinations(range(originals), 2))
    completed = 0
    half = 0
    largest = F(0)

    def check(y, edges, witness):
        nonlocal largest
        assert all(y[u] + y[v] >= 1 for u, v in edges)
        assert all(tuple(sorted(e)) in edges for e in witness)
        endpoints = [v for e in witness for v in e]
        assert len(endpoints) == len(set(endpoints))
        cost = sum(y)
        assert 2 * cost <= 3 * len(witness)
        largest = max(largest, F(cost, len(witness)))

    def grow(remaining, y, edges, original_matching, gadgets):
        nonlocal completed, half
        selected = {v for e in original_matching for v in e}
        witness = []
        for u, v, a, b in gadgets:
            if tuple(sorted((u, v))) in original_matching:
                witness.extend(((u, a), (b, v)))
            else:
                witness.append((a, b))
        for uv in remaining:
            for u, v in (uv, uv[::-1]):
                a, b = len(y), len(y) + 1
                ya = int(u not in selected)
                first = y + [ya]
                first_edges = edges | {tuple(sorted((u, a)))}
                first_witness = witness + ([(u, a)] if ya else [])
                check(first, first_edges, first_witness)
                half += 1
                after = first + [1 - ya]
                new_matching = original_matching
                if u not in selected and v not in selected:
                    after[u] = after[v] = 1
                    new_matching = original_matching | {tuple(sorted(uv))}
                assert all(x <= z for x, z in zip(first, after))
                after_edges = first_edges | {tuple(sorted((a, b))), tuple(sorted((b, v)))}
                new_gadgets = gadgets + [(u, v, a, b)]
                new_witness = []
                for uu, vv, aa, bb in new_gadgets:
                    if tuple(sorted((uu, vv))) in new_matching:
                        new_witness.extend(((uu, aa), (bb, vv)))
                    else:
                        new_witness.append((aa, bb))
                check(after, after_edges, new_witness)
                completed += 1
                grow(tuple(e for e in remaining if e != uv), after, after_edges,
                     new_matching, new_gadgets)

    grow(available, [0] * originals, set(), set(), [])
    return dict(completed_gadget_prefixes=completed, half_gadget_prefixes=half,
                maximum_cost_over_matching_certificate=str(largest))


def forest_checks():
    # Reconstruct cleanup from saved instances without running a MILP or
    # treating a solver's bound as a certificate.
    from vertex_blueprint_probe import shift, verify
    outputs = []
    for path in sorted((ROOT / 'experiments').glob('vertex-blueprint-P*-C*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        P, C, edges = data['phases'], data['alphabet'], data['edges']
        n = verify(P, C, edges)
        total_credit = F(0)
        for z in range(n):
            parent = list(range(2 * n))

            def find(v):
                while v != parent[v]:
                    v = parent[v]
                return v

            seen, retained = set(), set()
            credit = F(0)
            for p, a, b in sorted(edges):
                block = C ** (P - p + 1)
                aa = shift(a, z, P, C) // block * block
                bb = shift(b, z, P, C) // block * block
                good = 0
                for c in range(block):
                    u, v = aa + c, n + bb + c
                    if (u, v) in retained:
                        good += 1
                    elif u not in seen or v not in seen:
                        assert find(u) != find(v)
                        parent[find(u)] = find(v)
                        retained.add((u, v))
                        seen.update((u, v))
                        good += 1
                credit += F(good, block)
            total_credit += credit
        forcing = total_credit / n
        assert forcing == F(data['average_forced_hidden_weight'])
        assert forcing <= F(5, 3) * (n - len(edges))
        outputs.append(dict(file=path.name, shifts_checked=n, exact_forcing=str(forcing)))
    return outputs


def main():
    result = dict(scope='Exact checks of restricted construction obstructions; universal hypothesis unresolved',
                  boundary=boundary_checks(), subdivision=subdivision_checks(),
                  cleanup=forest_checks())
    target = ROOT / 'experiments' / 'construction-obstructions.json'
    target.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
