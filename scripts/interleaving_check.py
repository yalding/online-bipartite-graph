"""Enumerate a small instance of the ordered-walk lemma in exact fractions."""

from collections import defaultdict
from fractions import Fraction as Q
import json
from pathlib import Path


# Scale probabilities by five. A terminal '+' has mark five, '-' has zero.
# Nodes 'e' and 'f' exercise a private equal-mark choice at 'b'.
MARK = dict(A=2, a=1, b=3, c=0, d=3, e=3, f=3,
            B=3, g=1, h=4, i=0, j=2, k=2, l=5)
CHILDREN = dict(A=("a", "b"), a=("c", "d"), b=("e", "f"),
                B=("g", "h"), g=("i", "j"), h=("k", "l"))
MARK.update({"+": 5, "-": 0})


def children(node):
    return CHILDREN.get(node, ("-", "+"))


def high_probability(node):
    lo, hi = children(node)
    if MARK[lo] == MARK[hi]:
        return Q(1, 3)
    return Q(MARK[node] - MARK[lo], MARK[hi] - MARK[lo])


def local_tests(root):
    mass = {}

    def descend(path, weight):
        if path[-1] in ("-", "+"):
            mass[path[1:]] = weight
            return
        lo, hi = children(path[-1])
        probability = high_probability(path[-1])
        if probability < 1:
            descend(path + (lo,), weight * (1-probability))
        if probability:
            descend(path + (hi,), weight * probability)

    descend((root,), Q(1))
    return mass


def joint_tests():
    distribution = defaultdict(Q)

    def visit(nodes, positions, public, weight):
        if all(node in ("-", "+") for node in nodes):
            distribution[(public, nodes)] += weight
            return
        distances = []
        for side, (node, position) in enumerate(zip(nodes, positions)):
            if node in ("-", "+"):
                continue
            lo, hi = children(node)
            left, right = position - MARK[lo], MARK[hi] - position
            if min(left, right) == 0:
                if left == right:
                    pr = high_probability(node)
                    moves = [(lo, 1-pr), (hi, pr)]
                else:
                    moves = [(lo if left == 0 else hi, Q(1))]
                for child, pr in moves:
                    updated = list(nodes)
                    updated[side] = child
                    arrivals = public if child in ("-", "+") else public + (child,)
                    visit(tuple(updated), positions, arrivals, weight * pr)
                return
            distances.append((left, right))
        # Until the first pending split is hit, all unfinished particles
        # move by exactly the same displacement. Skip interior walk ticks.
        down = min(pair[0] for pair in distances)
        up = min(pair[1] for pair in distances)
        for shift, pr in [(-down, Q(up, up+down)), (up, Q(down, up+down))]:
            moved = tuple(pos if node in ("-", "+") else pos+shift
                          for node, pos in zip(nodes, positions))
            assert moved[0] <= moved[1]
            visit(nodes, moved, public, weight * pr)

    visit(("A", "B"), (2, 3), (), Q(1))
    return distribution


def main():
    distribution = joint_tests()
    assert sum(distribution.values()) == 1
    assert all(labels != ("+", "-") for _, labels in distribution)
    prefix_count = 0
    for side, (root, letters) in enumerate([("A", "abcdef"), ("B", "ghijkl")]):
        reference = local_tests(root)
        observed = defaultdict(lambda: defaultdict(Q))
        for (arrivals, labels), mass in distribution.items():
            test = tuple(n for n in arrivals if n in letters) + (labels[side],)
            observed[()][test] += mass
            for length, node in enumerate(arrivals, start=1):
                if node in letters:
                    observed[arrivals[:length]][test] += mass
        for prefix, measure in observed.items():
            local = tuple(node for node in prefix if node in letters)
            possible = {test: pr for test, pr in reference.items() if test[:len(local)] == local}
            total, expected_total = sum(measure.values()), sum(possible.values())
            assert {test: pr/total for test, pr in measure.items()} == {
                test: pr/expected_total for test, pr in possible.items()
            }
            prefix_count += bool(prefix)
    report = dict(public_paths_and_labels=len(distribution),
                  decision_prefix_laws_checked=prefix_count,
                  incompatible_mass="0", total_mass="1")
    output = json.dumps(report, indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "experiments" / "interleaving-check.json"
    path.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
