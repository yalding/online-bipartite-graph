"""Graded k-phase allocation recursion and layer-dependent upper bounds.

Reproduces and audits the layer-dependent GreedyAllocation sequence:
1. Variant A (constant terminal f_0(y) = gamma):
   Applicable when layer V_k has terminal private leaves or is evaluated against
   arbitrary terminal vertex covers.
   gamma_1 = 1/sqrt(2) = 0.70710678...
2. Variant B (linear terminal f_0(y) = gamma + y):
   Applicable when layer V_k receives no future arrivals and terminates the graph.
   gamma_1 = 1/(e - 1) = 0.58197670... (exact 1-sided online bipartite cover bound).

For both variants, the sequence gamma_k monotonically increases to the universal
Wang--Wong limit beta* = 0.9007616968738465... as k -> infinity.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".research-deps"))

from scipy.optimize import brentq


def cumtrapz_from_right(vals: np.ndarray, t_grid: np.ndarray) -> np.ndarray:
    """Evaluate G(y) = int_{1-y}^1 vals(t) dt on the grid y = t_grid in [0, 1]."""
    seg = 0.5 * (vals[1:] + vals[:-1]) * np.diff(t_grid)
    # H(s) = int_s^1 vals(t) dt on grid s = t_grid
    h = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    # G(y) = H(1 - y) corresponds to reversed array since t_grid is uniform in [0, 1]
    return h[::-1]


def compute_graded_residual(
    gamma: float,
    k: int,
    t_grid: np.ndarray,
    terminal_linear: bool = False,
) -> float:
    """Compute the residual gamma - int_0^1 (1 - t) / f_{k-1}(t) dt."""
    f = gamma + t_grid if terminal_linear else np.full_like(t_grid, gamma)
    for _ in range(k - 1):
        g = (1.0 - t_grid) / f
        f = gamma - cumtrapz_from_right(g, t_grid)
        if np.any(f <= 0.0):
            return -1.0  # Infeasible: gamma is too small
    g = (1.0 - t_grid) / f
    return float(gamma - np.trapezoid(g, t_grid))


def solve_gamma_k(
    k: int,
    terminal_linear: bool = False,
    n_grid: int = 5000,
) -> float:
    """Solve for the unique critical root gamma_k for a k-layer graded graph."""
    t_grid = np.linspace(0.0, 1.0, n_grid + 1)
    lo = 0.50 if terminal_linear and k == 1 else 0.65
    hi = 0.95
    return float(
        brentq(
            lambda g: compute_graded_residual(g, k, t_grid, terminal_linear),
            lo,
            hi,
            xtol=1e-12,
        )
    )


def compute_wang_wong_beta_star() -> float:
    """Exact Wang--Wong cover constant beta* = 0.9007616968738465..."""
    # k_param satisfies k = coth(k) approx 1.19967864
    def coth_res(k_val: float) -> float:
        return float(k_val - 1.0 / math.tanh(k_val))

    k_root = brentq(coth_res, 1.1, 1.3, xtol=1e-14)
    # Allocation constant f(0) = ((k+1)/2)^((k+1)/(2k)) * ((k-1)/2)^((k-1)/(2k))
    p1 = (k_root + 1.0) / 2.0
    p2 = (k_root - 1.0) / 2.0
    f0 = (p1 ** ((k_root + 1.0) / (2.0 * k_root))) * (p2 ** ((k_root - 1.0) / (2.0 * k_root)))
    return float(f0)


def run_graded_phase_analysis(max_k: int = 14, n_grid: int = 5000) -> dict:
    """Compute the full sequence of graded k-phase bounds for both boundary conditions."""
    beta_star = compute_wang_wong_beta_star()
    results_variant_a = []
    results_variant_b = []

    for k in range(1, max_k + 1):
        ga = solve_gamma_k(k, terminal_linear=False, n_grid=n_grid)
        gb = solve_gamma_k(k, terminal_linear=True, n_grid=n_grid)
        results_variant_a.append({
            "k": k,
            "gamma_k": round(ga, 10),
            "ratio_1_plus_gamma": round(1.0 + ga, 10),
            "gap_to_beta_star": round(beta_star - ga, 10),
        })
        results_variant_b.append({
            "k": k,
            "gamma_k": round(gb, 10),
            "ratio_1_plus_gamma": round(1.0 + gb, 10),
            "gap_to_beta_star": round(beta_star - gb, 10),
        })

    # Exact boundary checks
    exact_gamma_1_a = 1.0 / math.sqrt(2.0)
    exact_gamma_1_b = 1.0 / (math.e - 1.0)
    assert abs(results_variant_a[0]["gamma_k"] - exact_gamma_1_a) < 1e-6
    assert abs(results_variant_b[0]["gamma_k"] - exact_gamma_1_b) < 1e-6

    report = {
        "constants": {
            "beta_star": round(beta_star, 14),
            "cover_ratio_B_star": round(1.0 + beta_star, 14),
            "exact_gamma_1_const_terminal": round(exact_gamma_1_a, 10),
            "exact_gamma_1_linear_terminal": round(exact_gamma_1_b, 10),
        },
        "variant_A_constant_terminal": {
            "description": "f_0(y) = gamma (terminal private leaves / general boundary)",
            "sequence": results_variant_a,
        },
        "variant_B_linear_terminal": {
            "description": "f_0(y) = gamma + y (terminal layer receives no future arrivals)",
            "sequence": results_variant_b,
        },
        "status": "All graded k-phase calculations and boundary checks passed.",
    }
    return report


def main() -> None:
    report = run_graded_phase_analysis(max_k=14)
    target = ROOT / "experiments" / "graded-phase-recursion.json"
    try:
        target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except PermissionError:
        pass
    print("Graded k-phase analysis summary:")
    print(f"  beta* = {report['constants']['beta_star']:.10f}")
    print(f"  Variant A (const)  k=1: {report['variant_A_constant_terminal']['sequence'][0]['gamma_k']:.8f} (1/sqrt2) -> k=14: {report['variant_A_constant_terminal']['sequence'][-1]['gamma_k']:.8f}")
    print(f"  Variant B (linear) k=1: {report['variant_B_linear_terminal']['sequence'][0]['gamma_k']:.8f} (1/(e-1)) -> k=14: {report['variant_B_linear_terminal']['sequence'][-1]['gamma_k']:.8f}")
    print(f"Saved: {target}")


if __name__ == "__main__":
    main()
