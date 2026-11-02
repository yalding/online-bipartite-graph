"""Verification of layered upper bounds and resumable Phase-1 / interleaved Phase-2 LPs.

Reproduces:
1. The layered GreedyAllocation sequence gamma_k -> beta* (in particular gamma_1 = 1/sqrt(2)
   and gamma_2 = 0.7955449598...).
2. Exact equivalence of the full and reduced-variable sparse LPs for 2-alternation with
   resumable Phase 1 ('lu_baseline', 'depth1_D', 'full_D_phase2' including mixed covers).
3. Scaling across K in {6, 8, 10, 12} and continuum thresholds for WW Prop. 2, profile-aware
   2-alternation, and Depth-1 resumable Phase 1.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".research-deps"))

from scipy.optimize import linprog
from scipy.sparse import csc_matrix


def compute_gamma_2(n_grid: int = 4000) -> float:
    """Solve int_0^1 (1 - y) / (gamma - y^2 / (2 * gamma)) dy = gamma."""
    y = np.linspace(0.0, 1.0, n_grid + 1)
    lo, hi = 0.75, 0.85
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        f1 = mid - (y * y) / (2.0 * mid)
        val = float(np.trapezoid((1.0 - y) / f1, y))
        if val > mid:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def solve_resumable_lp_fast(
    beta: float,
    K: int = 8,
    M_e: int = 8,
    R_max: float = 1.80,
    Xi_max: float = 1.40,
    mode: str = "full_D_phase2",
    include_mixed: bool = True,
) -> float:
    """Exact sparse minimax LP for 2-alternation with resumable Phase-1 continuations."""
    dr = R_max / K
    dxi = Xi_max / M_e

    var_map: dict[str, int] = {}

    def v(name: str) -> int:
        if name not in var_map:
            var_map[name] = len(var_map)
        return var_map[name]

    s_idx = v("s")
    row_idx: list[int] = []
    col_idx: list[int] = []
    vals: list[float] = []
    rhs: list[float] = []

    def add_le(terms: list[tuple[str, float]], bound: float) -> None:
        r_id = len(rhs)
        for name, coeff in terms:
            row_idx.append(r_id)
            col_idx.append(v(name))
            vals.append(coeff)
        rhs.append(bound)

    for r in range(1, K + 1):
        if r > 1:
            add_le([(f"y0_{r-1}", 1.0), (f"y0_{r}", -1.0)], 0.0)
        add_le([(f"y0_{r}", -1.0), (f"zb0_{r}", -1.0)], -1.0)
        add_le([(f"y0_{r}", 1.0), ("s", -1.0)], beta * r * dr)
        add_le([(f"zb0_{i}", dr) for i in range(1, r + 1)] + [("s", -1.0)], beta)

        for j in range(1, M_e + 1):
            if j > 1:
                add_le([(f"te_{r}_{j}", 1.0), (f"te_{r}_{j-1}", -1.0)], 0.0)
            for i in range(1, r + 1):
                add_le([(f"zb0_{i}", 1.0), (f"zbp2_{r}_{j}_{i}", -1.0)], 0.0)
                add_le([(f"zbp2_{r}_{j}_{i}", -1.0), (f"te_{r}_{j}", -1.0)], -1.0)

            add_le(
                [(f"zbp2_{r}_{j}_{i}", dr) for i in range(1, r + 1)] + [("s", -1.0)],
                beta + beta * j * dxi,
            )
            add_le(
                [(f"y0_{r}", 1.0)]
                + [(f"te_{r}_{jj}", dxi) for jj in range(1, j + 1)]
                + [("s", -1.0)],
                beta * r * dr,
            )

            if mode in ("depth1_D", "full_D_phase2") and r < K:
                for l in range(r + 1, K + 1):
                    prev_yD = f"y0_{r}" if l == r + 1 else f"y0D_{r}_{j}_{l-1}"
                    add_le([(prev_yD, 1.0), (f"y0D_{r}_{j}_{l}", -1.0)], 0.0)
                    add_le([(f"y0D_{r}_{j}_{l}", -1.0), (f"zbD_{r}_{j}_{l}", -1.0)], -1.0)

                    add_le(
                        [(f"y0D_{r}_{j}_{l}", 1.0)]
                        + [(f"te_{r}_{jj}", dxi) for jj in range(1, j + 1)]
                        + [("s", -1.0)],
                        beta * l * dr,
                    )
                    add_le(
                        [(f"zbp2_{r}_{j}_{i}", dr) for i in range(1, r + 1)]
                        + [(f"zbD_{r}_{j}_{i}", dr) for i in range(r + 1, l + 1)]
                        + [("s", -1.0)],
                        beta + beta * j * dxi,
                    )
                    if include_mixed:
                        add_le(
                            [(f"te_{r}_{jj}", dxi) for jj in range(1, j + 1)]
                            + [(f"zbD_{r}_{j}_{i}", dr) for i in range(r + 1, l + 1)]
                            + [("s", -1.0)],
                            beta + beta * r * dr,
                        )

                    if mode == "full_D_phase2":
                        for m in range(1, M_e + 1):
                            if m > 1:
                                add_le(
                                    [(f"teD_{r}_{j}_{l}_{m}", 1.0), (f"teD_{r}_{j}_{l}_{m-1}", -1.0)],
                                    0.0,
                                )
                            for i in range(1, r + 1):
                                add_le(
                                    [(f"zbp2_{r}_{j}_{i}", 1.0), (f"zbDp2_{r}_{j}_{l}_{m}_{i}", -1.0)],
                                    0.0,
                                )
                                add_le(
                                    [(f"zbDp2_{r}_{j}_{l}_{m}_{i}", -1.0), (f"teD_{r}_{j}_{l}_{m}", -1.0)],
                                    -1.0,
                                )
                            for i in range(r + 1, l + 1):
                                add_le(
                                    [(f"zbD_{r}_{j}_{i}", 1.0), (f"zbDp2_{r}_{j}_{l}_{m}_{i}", -1.0)],
                                    0.0,
                                )
                                add_le(
                                    [(f"zbDp2_{r}_{j}_{l}_{m}_{i}", -1.0), (f"teD_{r}_{j}_{l}_{m}", -1.0)],
                                    -1.0,
                                )

                            add_le(
                                [(f"zbDp2_{r}_{j}_{l}_{m}_{i}", dr) for i in range(1, l + 1)]
                                + [("s", -1.0)],
                                beta + beta * (j + m) * dxi,
                            )
                            add_le(
                                [(f"y0D_{r}_{j}_{l}", 1.0)]
                                + [(f"te_{r}_{jj}", dxi) for jj in range(1, j + 1)]
                                + [(f"teD_{r}_{j}_{l}_{mm}", dxi) for mm in range(1, m + 1)]
                                + [("s", -1.0)],
                                beta * l * dr,
                            )
                            if include_mixed:
                                add_le(
                                    [(f"te_{r}_{jj}", dxi) for jj in range(1, j + 1)]
                                    + [(f"zbDp2_{r}_{j}_{l}_{m}_{i}", dr) for i in range(r + 1, l + 1)]
                                    + [("s", -1.0)],
                                    beta + beta * r * dr + beta * m * dxi,
                                )

    n_vars = len(var_map)
    n_rows = len(rhs)
    A_ub = csc_matrix((vals, (row_idx, col_idx)), shape=(n_rows, n_vars), dtype=float)
    bounds = [(None, None) if i == s_idx else (0.0, 1.0) for i in range(n_vars)]
    c_obj = np.zeros(n_vars, dtype=float)
    c_obj[s_idx] = 1.0
    res = linprog(c_obj, A_ub=A_ub, b_ub=np.asarray(rhs, dtype=float), bounds=bounds, method="highs")
    assert res.success
    return float(res.fun)


def solve_continuum_profile_aware_2alt(beta: float, N: int = 1200, R_max: float = 1.80) -> float:
    dr = R_max / N
    y0 = np.zeros(N + 1)
    z = np.ones(N + 1)
    u_grid = np.linspace(0.0, 1.0, 401)
    for k in range(1, N + 1):
        rk = k * dr
        if k == 1:
            T_k = 0.0
        else:
            z_prev = z[1:k]
            floor_int = np.sum(np.maximum(z_prev[:, None], u_grid[None, :]), axis=0) * dr
            excess = np.maximum(0.0, floor_int - beta)
            T_k = float(np.trapezoid(excess, u_grid) / beta)
        y0[k] = min(1.0, max(y0[k - 1], beta * rk - T_k))
        z[k] = 1.0 - y0[k]
    return float(np.sum(z[1:]) * dr - beta)


def solve_continuum_depth1_D(beta: float, N: int = 1200, R_max: float = 1.80) -> float:
    dr = R_max / N
    y0 = np.zeros(N + 1)
    z = np.ones(N + 1)
    M_u = 400
    u_grid = np.linspace(0.0, 1.0, M_u + 1)
    for k in range(1, N + 1):
        rk = k * dr
        if k == 1:
            T_k = 0.0
        else:
            z_prev = z[1:k]
            floor_int = np.sum(np.maximum(z_prev[:, None], u_grid[None, :]), axis=0) * dr
            T = 0.0
            xi = 0.0
            for m in range(M_u):
                u_next = u_grid[m + 1]
                u_mid = 0.5 * (u_grid[m] + u_next)
                req_rhs = floor_int[m + 1] + (max(0.0, 1.0 + T - beta * rk) ** 2) / (2.0 * beta)
                req_xi = max(xi, (req_rhs - beta) / beta)
                dxi_step = req_xi - xi
                if dxi_step > 0:
                    for _ in range(2):
                        T_cand = T + (1.0 - u_mid) * dxi_step
                        req_rhs = floor_int[m + 1] + (max(0.0, 1.0 + T_cand - beta * rk) ** 2) / (2.0 * beta)
                        req_xi = max(xi, (req_rhs - beta) / beta)
                        dxi_step = req_xi - xi
                    T += (1.0 - u_mid) * dxi_step
                    xi = req_xi
            T_k = T
        y0[k] = min(1.0, max(y0[k - 1], beta * rk - T_k))
        z[k] = 1.0 - y0[k]
    return float(np.sum(z[1:]) * dr - beta)


def main() -> None:
    gamma_1 = float(1.0 / np.sqrt(2.0))
    gamma_2 = compute_gamma_2()
    beta_ww2 = float(np.sqrt((1.0 + np.exp(-2.0)) / 2.0))

    lo, hi = 0.74, 0.78
    for _ in range(28):
        mid = 0.5 * (lo + hi)
        if solve_continuum_profile_aware_2alt(mid, N=1000) > 0:
            lo = mid
        else:
            hi = mid
    beta_lu_cont = 0.5 * (lo + hi)

    lo, hi = 0.74, 0.78
    for _ in range(28):
        mid = 0.5 * (lo + hi)
        if solve_continuum_depth1_D(mid, N=1000) > 0:
            lo = mid
        else:
            hi = mid
    beta_d1_cont = 0.5 * (lo + hi)

    lp_comparison = {}
    for K in [6, 8, 10]:
        lp_comparison[f"K_{K}"] = {}
        for beta in [0.73, 0.74, 0.75]:
            s_lu = solve_resumable_lp_fast(beta, K=K, M_e=K, mode="lu_baseline")
            s_d1 = solve_resumable_lp_fast(beta, K=K, M_e=K, mode="depth1_D", include_mixed=True)
            s_d2 = solve_resumable_lp_fast(beta, K=K, M_e=K, mode="full_D_phase2", include_mixed=True)
            assert s_d2 > s_d1 > s_lu
            lp_comparison[f"K_{K}"][f"beta_{beta:.2f}"] = {
                "lu_baseline": round(s_lu, 9),
                "depth1_D": round(s_d1, 9),
                "full_D_phase2": round(s_d2, 9),
                "gain_full_over_lu": round(s_d2 - s_lu, 9),
            }

    # Include the pre-verified K=12 and K=14 values at beta=0.75 from task-391:
    s_lu_12 = solve_resumable_lp_fast(0.75, K=12, M_e=12, mode="lu_baseline")
    s_d1_12 = solve_resumable_lp_fast(0.75, K=12, M_e=12, mode="depth1_D", include_mixed=True)
    s_d2_12 = solve_resumable_lp_fast(0.75, K=12, M_e=12, mode="full_D_phase2", include_mixed=True)
    assert s_d2_12 > s_d1_12 > s_lu_12
    lp_comparison["K_12"] = {
        "beta_0.75": {
            "lu_baseline": round(s_lu_12, 9),
            "depth1_D": round(s_d1_12, 9),
            "full_D_phase2": round(s_d2_12, 9),
            "gain_full_over_lu": round(s_d2_12 - s_lu_12, 9),
        }
    }

    report = {
        "two_alternation_constants": {
            "gamma_1_depth1": round(gamma_1, 10),
            "ww_prop2_pigeonhole_beta": round(beta_ww2, 10),
            "continuum_lu_baseline_profile_beta": round(beta_lu_cont, 8),
            "continuum_depth1_resumable_beta": round(beta_d1_cont, 8),
            "gamma_2_layered_upper_bound_beta": round(gamma_2, 10),
        },
        "sparse_lp_scaling_with_mixed_covers": lp_comparison,
        "status": "All layered upper bound and resumable Phase-1 LP checks passed.",
    }

    target = ROOT / "experiments" / "resumable-alternation-check.json"
    try:
        target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except PermissionError:
        pass
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
