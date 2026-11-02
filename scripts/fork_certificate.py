"""Generate or independently replay a finite tree-of-pools lower certificate."""

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def generate(beta, mesh, sweep_limit):
    if not 0 < beta < 1 or mesh < 1 or sweep_limit < 1:
        raise ValueError("Need 0 < beta < 1, a positive mesh and a positive sweep limit")
    scale = 10**9 * math.lcm(mesh, beta.denominator)
    budget = int(beta * scale)
    last = 5 * mesh // 4
    if last * scale + mesh**2 >= 2**63:
        raise ValueError("Search products exceed the int64 limit")

    slopes = np.arange(last + 1, dtype=np.int64)
    candidates = slopes[::max(1, mesh // 150)]
    denominators = mesh**2 - slopes[:, None] * candidates
    divisors = np.maximum(denominators, 1)
    previous = np.zeros(last + 1, dtype=np.int64)
    trace = []
    for _ in range(sweep_limit):
        # A candidate child line comes from the preceding sweep. The parent
        # line is always the preceding slope of the current sweep.
        numerators = slopes[:, None] * (budget - previous[candidates])
        gains = np.where(
            denominators > 0,
            scale // mesh - (numerators + divisors - 1) // divisors,
            0,
        )
        best = np.argmax(gains, axis=1)
        increments = np.maximum(0, gains[slopes, best])
        choices = np.where(increments > 0, candidates[best], -1)
        choices[0] = -1
        increments[0] = 0
        if int(increments.max()) * last >= 2**63:
            raise ValueError("Sweep sum exceeds the int64 limit")
        current = np.cumsum(increments)
        trace.append(choices.astype(np.int32))
        if current[-1] > budget:
            return scale, np.stack(trace)
        if np.array_equal(current, previous):
            break
        previous = current
    raise ValueError("No strict certificate found with these search parameters")


def verify(beta, mesh, scale, choices):
    """Reconstruct each line with Python integers, without using the search."""
    if not 0 < beta < 1 or scale <= 0 or mesh <= 0 or (scale * beta).denominator != 1:
        raise ValueError("Invalid units")
    budget = int(scale * beta)
    rows, columns = choices.shape
    if rows < 1 or columns < 2 or not np.issubdtype(choices.dtype, np.signedinteger):
        raise ValueError("Invalid trace")
    previous = [0] * columns
    fork_count = 0
    for row in choices:
        if row[0] != -1:
            raise ValueError("Slope zero must use the zero line")
        current = [0]
        for level in range(1, columns):
            child = int(row[level])
            gain = 0
            if child != -1:
                if not 0 <= child < columns:
                    raise ValueError("Invalid child index")
                denominator = mesh**2 - level * child
                if denominator <= 0:
                    raise ValueError("Invalid fork weight")
                gain = (scale * denominator - mesh * level * (budget - previous[child])) // (
                    mesh * denominator
                )
                if gain <= 0:
                    raise ValueError("Fork failed its directed lower bound")
                fork_count += 1
            current.append(current[-1] + gain)
        previous = current

    crossing = next((index for index, value in enumerate(previous) if value > budget), None)
    if crossing is None:
        raise ValueError("No root violation")
    return dict(beta=str(beta), excluded_ratio=str(1 + beta), mesh=mesh, scale=scale,
                sweeps=rows, columns=columns, fork_records=fork_count,
                root_record=[rows, crossing], root_intercept=previous[crossing],
                root_budget=budget, integer_margin=previous[crossing] - budget,
                rule="fork child mass / parent mass = mesh / (mesh^2 - level * child_index)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="Verify an existing certificate")
    parser.add_argument("--beta", type=Fraction, default=Fraction(1801, 2000))
    parser.add_argument("--mesh", type=int, default=4000)
    parser.add_argument("--sweeps", type=int, default=200)
    parser.add_argument("--out", type=Path, help="Output NPZ (default name includes the trial ratio)")
    args = parser.parse_args()
    if args.check:
        with np.load(args.check, allow_pickle=False) as data:
            beta = Fraction(int(data["numerator"]), int(data["denominator"]))
            report = verify(beta, int(data["mesh"]), int(data["scale"]), data["choices"])
    else:
        scale, choices = generate(args.beta, args.mesh, args.sweeps)
        report = verify(args.beta, args.mesh, scale, choices)
        target = args.out or ROOT / "experiments" / f"fork-{args.beta.numerator}-{args.beta.denominator}.npz"
        if target.suffix != ".npz":
            parser.error("--out must name an .npz file")
        np.savez_compressed(target, numerator=args.beta.numerator,
                            denominator=args.beta.denominator, mesh=args.mesh,
                            scale=scale, choices=choices)
        target.with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
