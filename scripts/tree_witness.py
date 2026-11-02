"""Generate unweighted vertex-arrival witnesses given exact algorithm marginals.

An input is a tuple of earlier-neighbor tuples in vertex arrival order.
The callback receives only the public core prefix. It returns the original
algorithm's expected fractional coordinates there, in vertex order. For
exact comparisons use integers/Fractions, or comparable exact real values.
"""

from fractions import Fraction
from itertools import accumulate
from math import lcm


def core_histories(stage):
    """Stream the stage in Section 5, already scaled to integer pool sizes."""
    if stage < 1:
        raise ValueError("Stage must be positive")
    scale = lcm(*range(1, stage + 1))
    sizes = sorted({a * scale // b for a in range(1, stage + 1) for b in range(1, stage + 1)})

    # parents[j-1] names the unique parent of nonroot pool j.
    pending = [((), (scale,))]
    while pending:
        parents, weights = pending.pop()
        yield parents, weights
        if len(weights) < stage:
            for parent in reversed(range(len(weights))):
                for size in reversed(sizes):
                    pending.append((parents + (parent,), weights + (size,)))


def arrivals(parents, weights, cover=()):
    """Expand a pool history and optional private completion into a legal input."""
    if len(parents) + 1 != len(weights) or any(w < 1 for w in weights):
        raise ValueError("Need one positive size per pool")
    ends = (0, *accumulate(weights))
    graph = [()] * weights[0]
    for child, parent in enumerate(parents, start=1):
        if not 0 <= parent < child:
            raise ValueError("Parent must have already arrived")
        neighborhood = tuple(range(ends[parent], ends[parent + 1]))
        graph.extend([neighborhood] * weights[child])
    selected = set(cover)
    if not selected <= set(range(len(weights))) or (selected and any(
        child not in selected and parent not in selected
        for child, parent in enumerate(parents, start=1)
    )):
        raise ValueError("Invalid terminal cover")
    for pool in sorted(selected):
        graph.extend((vertex,) for vertex in range(ends[pool], ends[pool + 1]))
    return tuple(graph)


def find_witness(beta, marginals):
    """Search through finite stages until a strictly violated cover is found.

    For a legal marginal oracle the theorem guarantees termination when
    0 < beta < B* - 1. No efficiency or computability of a real oracle is
    assumed. Evaluating only a bounded stage does not have this guarantee.
    """
    if not 0 < beta < 1:
        raise ValueError("Expected an excess ratio between zero and one")
    stage = 2
    while True:
        for parents, weights in core_histories(stage):
            if not parents:
                continue
            graph = arrivals(parents, weights)
            coordinates = tuple(marginals(graph))
            if len(coordinates) != len(graph) or any(not 0 <= y <= 1 for y in coordinates):
                raise ValueError("Invalid marginal vector")
            ends = (0, *accumulate(weights))
            paid = [sum(coordinates[start:end]) for start, end in zip(ends, ends[1:])]
            for mask in range(1, 1 << len(weights)):
                cover = [v for v in range(len(weights)) if mask & (1 << v)]
                if any(v not in cover and u not in cover for v, u in enumerate(parents, start=1)):
                    continue
                optimum = sum(weights[v] for v in cover)
                outside = sum(paid[v] for v in range(len(weights)) if v not in cover)
                if outside > beta * optimum:
                    return dict(arrivals=arrivals(parents, weights, cover), parents=parents,
                                weights=weights, cover=cover, optimum=optimum,
                                ratio_floor=1 + outside / Fraction(optimum))
        stage += 1
