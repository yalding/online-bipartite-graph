"""Check complete local test laws at public arrivals using exact fractions."""

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
# X and Y have equal initial marks. Each has a private split at the root,
# so a root-only stop is possible alongside two different public arrivals.
MARK.update(X=3, Y=3, hiddenX=4, hiddenY=1, x=1, y=2, z=3, u=2, v=2,
            m=3, n=2, w=5, t=5, hiddenLabel=5)
CHILDREN.update(X=("x", "hiddenX"), hiddenX=("y", "+"), x=("-", "z"),
                y=("u", "v"), Y=("hiddenY", "w"), hiddenY=("-", "m"),
                m=("n", "+"), w=("t", "+"), t=("-", "hiddenLabel"),
                hiddenLabel=("+", "+alternate"))
TERMINALS = {"-": 0, "+": 5, "+alternate": 5}
MARK.update(TERMINALS)


def children(node):
    return CHILDREN.get(node, ("-", "+"))


def high_probability(node):
    lo, hi = children(node)
    if MARK[lo] == MARK[hi]:
        return Q(1, 3)
    return Q(MARK[node] - MARK[lo], MARK[hi] - MARK[lo])


def local_tests(root, public_nodes):
    mass = defaultdict(Q)

    def descend(node, public, weight):
        if node in TERMINALS:
            mass[public + (node,)] += weight
            return
        lo, hi = children(node)
        pr = high_probability(node)
        for child, chance in ((lo, 1-pr), (hi, pr)):
            if chance:
                path = public + (child,) if child in public_nodes else public
                descend(child, path, weight * chance)

    descend(root, (), Q(1))
    return mass


def joint_tests(roots, public_nodes, priority):
    distribution = defaultdict(Q)

    def visit(nodes, positions, public, weight):
        if all(node in TERMINALS for node in nodes):
            distribution[(public, nodes)] += weight
            return
        distances = []
        for side in priority:
            node, position = nodes[side], positions[side]
            if node in TERMINALS:
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
                    arrivals = public + (child,) if child in public_nodes[side] else public
                    visit(tuple(updated), positions, arrivals, weight * pr)
                return
            distances.append((left, right))
        # Until the first pending split is hit, all unfinished particles
        # move by exactly the same displacement. Skip interior walk ticks.
        down = min(pair[0] for pair in distances)
        up = min(pair[1] for pair in distances)
        for shift, pr in [(-down, Q(up, up+down)), (up, Q(down, up+down))]:
            moved = tuple(pos if node in TERMINALS else pos+shift
                          for node, pos in zip(nodes, positions))
            assert moved[0] <= moved[1]
            visit(nodes, moved, public, weight * pr)

    visit(roots, tuple(MARK[root] for root in roots), (), Q(1))
    return distribution


def check(roots, public_nodes, priority):
    distribution = joint_tests(roots, public_nodes, priority)
    assert sum(distribution.values()) == 1
    assert all(MARK[a] <= MARK[b] for _, (a, b) in distribution)
    prefix_count = 0
    for side, (root, letters) in enumerate(zip(roots, public_nodes)):
        reference = local_tests(root, letters)
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
    return dict(public_paths_and_labels=len(distribution),
                decision_prefix_laws_checked=prefix_count,
                incompatible_mass="0", total_mass="1")


def main():
    report = check(("A", "B"), (set("abcdef"), set("ghijkl")), (0, 1))
    for priority in ((0, 1), (1, 0)):
        name = "hidden_stops_" + ("parent_first" if priority[0] == 0 else "child_first")
        report[name] = check(("X", "Y"), (set("xyzuv"), set("mntw")), priority)
    output = json.dumps(report, indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "experiments" / "interleaving-check.json"
    path.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
