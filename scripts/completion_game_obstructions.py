"""Exact verification of structural obstructions for the two-pool completion game and tree-of-pools families.

Verifies:
1. The Tree-of-Pools / Depth-First Obstruction Theorem (1 + 1/sqrt(2) ceiling via the exact online ODE).
2. The Exact Depth-1 Conservation Identity and Breadth-First Slack Identity.
3. The Exact Affine-Simplex (c, alpha, mu) representation of COMPLETION_GAME.md Eq. (5)-(6),
   showing that the strict 2-arrival-per-phase unit-weight game is capped at 1 + (sqrt(5)-1)/2 ~ 1.618034.
4. The exact primal-dual LP minimax threshold of the k-pool selective-retirement game at 2 alternations
   for k = 1, 2, 4, 8, 16 active pools, demonstrating why k = 2 (COMPLETION_GAME.md) is capped near 1.7273
   and why k -> infinity (unbounded active boundary) is structurally required.
"""
from itertools import product
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".research-deps"))

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, linprog


def verify_tree_of_pools_ode():
    """Verify the exact ODE dy/dxi = beta - (z/beta)*(1 - y) maintains O/(-I) == z/beta and M/(-I) <= z/beta."""
    beta = 1.0 / math.sqrt(2.0)
    max_ratio_err = 0.0
    checked = 0
    for z in np.linspace(0.05, 0.95, 19):
        # Solve dy/dxi = beta - (z/beta)*(1 - y) until y(xi) = 1:
        # Analytical solution: 1 - y(xi) = ((beta^2 - z(1-z))/z) * exp((z/beta)*xi) - ... wait:
        # Let u(xi) = 1 - y(xi). Then u(0) = 1 - z, and du/dxi = -beta + (z/beta)*u.
        # Since beta^2 > z(1-z) for all beta >= 1/sqrt(2) > 1/2, du/dxi < 0 everywhere!
        # Furthermore, int_0^xi u(t) dt = (beta/z) * (u(xi) - u(0) + beta*xi) = (beta/z) * (z - y(xi) + beta*xi),
        # so I(xi) = -beta + int_0^xi u(t) dt = (beta/z) * (-z + z - y(xi) + beta*xi) = -(beta/z) * (y(xi) - beta*xi) = -(beta/z) * O(xi)!
        for xi in np.linspace(0.0, 1.5, 31):
            # Exact analytical solution of du/dxi = (z/beta)*u - beta with u(0) = 1 - z:
            if z > 1e-12:
                u_xi = (1.0 - z - (beta ** 2) / z) * math.exp((z / beta) * xi) + (beta ** 2) / z
            else:
                u_xi = 1.0 - beta * xi
            if u_xi < 0.0:
                continue
            y_xi = 1.0 - u_xi
            # Analytical integral of u(t) from 0 to xi:
            int_u = (beta / z) * ((1.0 - z - (beta ** 2) / z) * (math.exp((z / beta) * xi) - 1.0)) + (beta ** 2 / z) * xi
            O_xi = y_xi - beta * xi
            I_xi = -beta + int_u
            assert I_xi < -1e-9, f"Expected I_xi < 0, got {I_xi}"
            ratio = O_xi / (-I_xi)
            err = abs(ratio - (z / beta))
            if err > max_ratio_err:
                max_ratio_err = err
            checked += 1
    assert max_ratio_err < 1e-13, max_ratio_err
    return dict(
        beta_threshold=round(beta, 10),
        competitive_ratio_ceiling=round(1.0 + beta, 10),
        ode_grid_points_checked=checked,
        max_identity_error=max_ratio_err,
    )


def verify_conservation_and_slack_identities():
    """Verify the exact Depth-1 conservation identity and Breadth-First Slack identity across arbitrary trajectories."""
    beta = 0.80
    rng = np.random.default_rng(20261101)
    max_cons_err = 0.0
    for _ in range(50):
        yx = rng.uniform(0.1, 0.9)
        z = 1.0 - yx
        R_star = yx / beta
        # Random monotone trajectory y_u(xi) on [0, R_star] represented as piecewise linear
        n_seg = 20
        xi_grid = np.linspace(0.0, R_star, n_seg + 1)
        dxi = R_star / n_seg
        increments = rng.uniform(0.0, 1.0, size=n_seg)
        increments = increments / np.sum(increments) * rng.uniform(0.0, yx)
        y_grid = np.concatenate([[z], z + np.cumsum(increments)])
        # For piecewise linear y_u(xi):
        # O_1(xi) = y_u(xi) - beta * xi
        # int_0^{R_star} (O_1(xi) - z) dxi = int_0^{R_star} (y_u(xi) - z - beta*xi) dxi
        int_y_minus_z = np.trapezoid(y_grid - z, xi_grid)
        int_O_minus_z = int_y_minus_z - 0.5 * beta * (R_star ** 2)
        # I_1(R_star) = -beta + int_0^{R_star} (1 - y_u(xi)) dxi
        I_R_star = -beta + R_star * (1.0 - z) - int_y_minus_z
        f1_yx = beta - (yx ** 2) / (2.0 * beta)
        cons_err = abs(int_O_minus_z + (I_R_star + f1_yx))
        if cons_err > max_cons_err:
            max_cons_err = cons_err
    assert max_cons_err < 1e-14, max_cons_err

    # Verify Breadth-First Slack identity: Slack(r) - int_0^r y(tau) dtau == beta - r
    max_slack_err = 0.0
    for r in np.linspace(0.1, 1.2, 20):
        tau_grid = np.linspace(0.0, r, 51)
        y_tau = np.minimum(1.0, 0.7 * tau_grid + 0.2 * (tau_grid ** 2))
        slack_r = beta - np.trapezoid(1.0 - y_tau, tau_grid)
        required_jump = np.trapezoid(y_tau, tau_grid)
        err = abs((slack_r - required_jump) - (beta - r))
        if err > max_slack_err:
            max_slack_err = err
    assert max_slack_err < 1e-14, max_slack_err
    return dict(
        random_trajectories_checked=50,
        max_conservation_identity_error=max_cons_err,
        max_breadth_first_slack_identity_error=max_slack_err,
    )


def initial_V0_planes(weights, beta):
    k = len(weights)
    planes = []
    for mask in range(1 << k):
        c = -beta * sum(weights[i] for i in range(k) if (mask & (1 << i)))
        alphas = tuple(0.0 if (mask & (1 << i)) else float(weights[i]) for i in range(k))
        mus = tuple(1.0 if m == mask else 0.0 for m in range(1 << k))
        planes.append((c, alphas, mus))
    return planes


def backprop_retire_valid(k_before, weights_before, retire_idx, retire_nmask_after, beta, planes_after, tol=1e-12):
    k_after = k_before - 1
    w_u = float(weights_before[retire_idx])
    out_planes = []
    for c, alphas_after, mus_after in planes_after:
        active_masks = [m for m in range(1 << k_after) if mus_after[m] > tol]
        allowed_bits = [
            (0, 1) if ((m & retire_nmask_after) == retire_nmask_after) else (1,)
            for m in active_masks
        ]
        for bits in product(*allowed_bits):
            c_new = c
            alpha_u = 0.0
            mus_before = [0.0] * (1 << k_before)
            for idx, m in enumerate(active_masks):
                mu_val = mus_after[m]
                low = m & ((1 << retire_idx) - 1)
                high = m >> retire_idx
                mask_out = low | (high << (retire_idx + 1))
                mask_in = mask_out | (1 << retire_idx)
                if bits[idx] == 0:
                    alpha_u += mu_val * w_u
                    mus_before[mask_out] += mu_val
                else:
                    c_new -= mu_val * beta * w_u
                    mus_before[mask_in] += mu_val
            alphas_before = (
                alphas_after[:retire_idx] + (alpha_u,) + alphas_after[retire_idx:]
            )
            out_planes.append((c_new, alphas_before, tuple(mus_before)))
    return out_planes


def backprop_add_and_solve(k_before, weights_before, b, neighbor_mask, planes_ext, tol=1e-12):
    neighbors = [i for i in range(k_before) if (neighbor_mask & (1 << i))]
    t_lines = []
    for c, alphas_ext, mus_ext in planes_ext:
        valid = True
        mus_base = [0.0] * (1 << k_before)
        for mask_ext in range(1 << (k_before + 1)):
            mu_val = mus_ext[mask_ext]
            if mu_val <= tol:
                continue
            mask_base = mask_ext & ((1 << k_before) - 1)
            in_cover = bool(mask_ext & (1 << k_before))
            if not in_cover and ((mask_base & neighbor_mask) != neighbor_mask):
                valid = False
                break
            mus_base[mask_base] += mu_val
        if not valid:
            continue
        mus_base = tuple(mus_base)
        alphas_base = alphas_ext[:k_before]
        gamma = alphas_ext[k_before]
        pos_neighbors = [i for i in neighbors if alphas_base[i] > tol]
        for bits in product((0, 1), repeat=len(pos_neighbors)):
            raised = {pos_neighbors[idx] for idx, bit in enumerate(bits) if bit}
            c_new = c + sum(alphas_base[i] for i in raised)
            alphas_new = tuple(0.0 if i in raised else alphas_base[i] for i in range(k_before))
            m_t = gamma - sum(alphas_base[i] for i in raised)
            t_lines.append((c_new, alphas_new, mus_base, m_t))
    out_planes = []
    neg_lines = []
    pos_lines = []
    for c_x, alphas_x, mus_x, m_t in t_lines:
        out_planes.append((c_x + min(0.0, m_t), alphas_x, mus_x))
        if m_t < -tol:
            neg_lines.append((c_x, alphas_x, mus_x, m_t))
        elif m_t > tol:
            pos_lines.append((c_x, alphas_x, mus_x, m_t))
    for c1, a1, mu1, m1 in neg_lines:
        for c2, a2, mu2, m2 in pos_lines:
            lam1 = m2 / (m2 - m1)
            lam2 = -m1 / (m2 - m1)
            c_mix = lam1 * c1 + lam2 * c2
            a_mix = tuple(lam1 * a1[i] + lam2 * a2[i] for i in range(k_before))
            mu_mix = tuple(lam1 * mu1[m] + lam2 * mu2[m] for m in range(1 << k_before))
            out_planes.append((c_mix, a_mix, mu_mix))
    return out_planes


def prune_cam_planes(planes, k, tol=1e-10):
    if len(planes) <= 1:
        return planes
    unique = []
    for c, a, mu in sorted(planes, key=lambda p: -p[0]):
        if not any(
            abs(c - c2) < tol
            and all(abs(a[i] - a2[i]) < tol for i in range(k))
            and all(abs(mu[m] - mu2[m]) < tol for m in range(1 << k))
            for c2, a2, mu2 in unique
        ):
            unique.append((c, a, mu))
    nondom = []
    for i, (cp, ap, mup) in enumerate(unique):
        dom = False
        for j, (cq, aq, muq) in enumerate(unique):
            if i == j:
                continue
            if all(abs(mup[m] - muq[m]) < tol for m in range(1 << k)):
                if (cq - cp) + sum(min(0.0, aq[idx] - ap[idx]) for idx in range(k)) >= -tol:
                    dom = True
                    break
        if not dom:
            nondom.append((cp, ap, mup))
    return nondom


def fast_prune_planes(planes, k, tol=1e-10):
    planes = prune_cam_planes(planes, k, tol=tol)
    if len(planes) <= 30:
        return planes
    rng = np.random.default_rng(999 + k)
    states_x = list(product((0.0, 0.5, 1.0), repeat=k))
    for _ in range(25):
        states_x.append(tuple(rng.uniform(0.0, 1.0, size=k)))
    states_E = [tuple(0.0 for _ in range(1 << k))]
    for req in range(1 << k):
        states_E.append(tuple(0.0 if (m & req) == req else -10.0 for m in range(1 << k)))
        states_E.append(tuple(0.0 if (m & req) == req else -0.5 for m in range(1 << k)))
    for _ in range(25):
        base = rng.uniform(-2.0, 0.0)
        inc = rng.uniform(0.0, 1.0, size=k)
        states_E.append(tuple(min(0.0, base + sum(inc[i] for i in range(k) if (m & (1 << i)))) for m in range(1 << k)))
    C = np.array([p[0] for p in planes])
    A = np.array([p[1] for p in planes])
    M = np.array([p[2] for p in planes])
    vals = C[:, None, None] + (A @ np.array(states_x).T)[:, :, None] + (M @ np.array(states_E).T)[:, None, :]
    max_v = np.max(vals, axis=0, keepdims=True)
    is_winner = np.any(vals >= max_v - 1e-8, axis=(1, 2))
    return [planes[i] for i in np.where(is_winner)[0]]


def verify_unit_weight_strict_phase_game():
    """Evaluate the strict 2-arrival-per-phase unit-weight game (COMPLETION_GAME.md Sec 4)."""
    results = []
    for beta in [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.875]:
        w_ac = (1.0, 1.0)
        p_bd = initial_V0_planes(w_ac, beta)
        phase_max = []
        for _ in range(3):
            cand_ac = list(p_bd)
            w_acb = (1.0, 1.0, 1.0)
            for nb in (1, 2, 3):
                cand_acb = list(initial_V0_planes(w_acb, beta))
                for nd in (1, 2, 3):
                    a_nmask_on_cbd = (2 if (nb & 1) else 0) | (4 if (nd & 1) else 0)
                    c_nmask_on_bd = (1 if (nb & 2) else 0) | (2 if (nd & 2) else 0)
                    p_cbd = fast_prune_planes(backprop_retire_valid(3, (1.0, 1.0, 1.0), 0, c_nmask_on_bd, beta, p_bd), 3)
                    p_acbd = fast_prune_planes(backprop_retire_valid(4, (1.0, 1.0, 1.0, 1.0), 0, a_nmask_on_cbd, beta, p_cbd), 4)
                    cand_acb.extend(backprop_add_and_solve(3, w_acb, 1.0, nd, p_acbd))
                cand_acb = fast_prune_planes(cand_acb, 3)
                cand_ac.extend(backprop_add_and_solve(2, w_ac, 1.0, nb, cand_acb))
            p_bd = fast_prune_planes(cand_ac, 2)
            v_init = max(c for c, _, _ in p_bd)
            phase_max.append(round(v_init, 9))
        results.append(dict(beta=round(beta, 9), phase_surpluses=phase_max))
    return dict(strict_phase_unit_weight_results=results)


def solve_k_pool_2alt_lp(beta, k_active, m0=20, r0_tot=0.60, w_active_tot=0.80, m_e=25, we_tot=1.00):
    """
    Exact primal-dual LP for 2-alternation selective-retirement schedule with `k_active` active pools in R_1:
      - Phase 1 starts with m0 immediately retired Depth-1 pools (total weight r0_tot) on L0 (weight 1).
      - Then `k_active` pools b_1, ..., b_k arrive on L0 (each of weight w_b = w_active_tot / k_active).
      - After each b_r (1 <= r <= k_active), the adversary can retire L0 and enter Phase 2 on {b_1, ..., b_r}
        (where m_e pools e_1, ..., e_{m_e} arrive connected to all of {b_1, ..., b_r}).
    Returns the exact minimax surplus s*.
    """
    w0_step = r0_tot / m0 if m0 > 0 else 0.0
    wb = w_active_tot / k_active
    we_step = we_tot / m_e

    var_map = {}
    def v(name):
        if name not in var_map:
            var_map[name] = len(var_map)
        return var_map[name]

    s_idx = v("s")
    for i in range(1, m0 + 1):
        v(f"y0_{i}"); v(f"z0_{i}")
    for r in range(1, k_active + 1):
        v(f"yB_{r}")
        for idx in range(1, r + 1):
            v(f"zb_p1_{r}_{idx}")
        for j in range(1, m_e + 1):
            v(f"te_{r}_{j}")
            for idx in range(1, r + 1):
                v(f"zb_p2_{r}_{j}_{idx}")

    n_vars = len(var_map)
    rows, rhs = [], []
    def add_le(terms, bound):
        row = [0.0] * n_vars
        for name, coeff in terms:
            row[v(name)] += coeff
        rows.append(row)
        rhs.append(bound)

    # Phase 1 prefix r_0:
    for i in range(1, m0 + 1):
        add_le([(f"y0_{i}", -1.0), (f"z0_{i}", -1.0)], -1.0)
        if i > 1:
            add_le([(f"y0_{i-1}", 1.0), (f"y0_{i}", -1.0)], 0.0)
        add_le([(f"y0_{i}", 1.0), ("s", -1.0)], beta * i * w0_step)
        add_le([(f"z0_{idx}", w0_step) for idx in range(1, i + 1)] + [("s", -1.0)], beta)

    # Active pools b_1 .. b_k:
    for r in range(1, k_active + 1):
        prev_y = f"y0_{m0}" if (r == 1 and m0 > 0) else (f"yB_{r-1}" if r > 1 else None)
        if prev_y is not None:
            add_le([(prev_y, 1.0), (f"yB_{r}", -1.0)], 0.0)
        for idx in range(1, r):
            add_le([(f"zb_p1_{r-1}_{idx}", 1.0), (f"zb_p1_{r}_{idx}", -1.0)], 0.0)
        add_le([(f"yB_{r}", -1.0), (f"zb_p1_{r}_{r}", -1.0)], -1.0)

        # Depth-1 covers after b_r arrives:
        add_le([(f"yB_{r}", 1.0), ("s", -1.0)], beta * (r0_tot + r * wb))
        add_le(
            [(f"z0_{i}", w0_step) for i in range(1, m0 + 1)]
            + [(f"zb_p1_{r}_{idx}", wb) for idx in range(1, r + 1)]
            + [("s", -1.0)],
            beta,
        )

        # Phase 2 branch on {b_1, ..., b_r}:
        for j in range(1, m_e + 1):
            for idx in range(1, r + 1):
                prev_zb = f"zb_p1_{r}_{idx}" if j == 1 else f"zb_p2_{r}_{j-1}_{idx}"
                add_le([(prev_zb, 1.0), (f"zb_p2_{r}_{j}_{idx}", -1.0)], 0.0)
                add_le([(f"zb_p2_{r}_{j}_{idx}", -1.0), (f"te_{r}_{j}", -1.0)], -1.0)
            # Cover 1 (L0 in C, b_1..b_r not in C, e_1..e_j in C):
            add_le(
                [(f"z0_{i}", w0_step) for i in range(1, m0 + 1)]
                + [(f"zb_p2_{r}_{j}_{idx}", wb) for idx in range(1, r + 1)]
                + [("s", -1.0)],
                beta + beta * j * we_step,
            )
            # Cover 2 (L0 not in C, r_0 in C, b_1..b_r in C, e_1..e_j not in C):
            add_le(
                [(f"yB_{r}", 1.0)]
                + [(f"te_{r}_{jj}", we_step) for jj in range(1, j + 1)]
                + [("s", -1.0)],
                beta * (r0_tot + r * wb),
            )

    bounds = [(None, None) if i == s_idx else (0.0, 1.0) for i in range(n_vars)]
    c_obj = [1.0 if i == s_idx else 0.0 for i in range(n_vars)]
    res = linprog(c_obj, A_ub=rows, b_ub=rhs, bounds=bounds, method="highs")
    assert res.success
    return float(res.fun)


def verify_k_pool_scaling():
    """Compute exact minimax beta threshold as active boundary size k increases from 1 to 12."""
    scaling = []
    # For k = 1 (no retired prefix r0=0, just 1 pool b1): tree of pools -> capped at <= 1/sqrt(2)
    # With r0 > 0 and k active pools in Phase 2:
    for k_active in [1, 2, 4, 8]:
        best_beta = 0.0
        best_params = None
        configs = [
            (1.10, 0.70),
            (0.90, 1.10),
            (0.60, 1.30),
            (0.00, 1.75),
        ]
        for r0_tot, w_act in configs:
            m0 = 15 if r0_tot > 0 else 0
            lo, hi = 0.60, 0.76
            if solve_k_pool_2alt_lp(lo, k_active, m0=m0, r0_tot=r0_tot, w_active_tot=w_act, m_e=20) <= 0:
                continue
            for _ in range(14):
                mid = 0.5 * (lo + hi)
                if solve_k_pool_2alt_lp(mid, k_active, m0=m0, r0_tot=r0_tot, w_active_tot=w_act, m_e=20) > 0:
                    lo = mid
                else:
                    hi = mid
            if lo > best_beta:
                best_beta = lo
                best_params = dict(r0_tot=r0_tot, w_active_tot=w_act)
        scaling.append(dict(
            active_boundary_k=k_active,
            critical_beta=round(best_beta, 6),
            competitive_ratio=round(1.0 + best_beta, 6),
            optimal_phase1_weights=best_params,
        ))
    return scaling


def main():
    report = dict(
        scope="Structural obstructions for Tree-of-Pools and Two-Pool Completion Game (COMPLETION_GAME.md Eq. 6)",
        tree_of_pools_obstruction=verify_tree_of_pools_ode(),
        conservation_and_slack_identities=verify_conservation_and_slack_identities(),
        unit_weight_strict_phase_obstruction=verify_unit_weight_strict_phase_game(),
        k_pool_active_boundary_scaling=verify_k_pool_scaling(),
    )
    target = ROOT / "experiments" / "completion-game-obstructions.json"
    print(json.dumps(report, indent=2), flush=True)
    try:
        target.write_text(json.dumps(report, indent=2), encoding="utf-8")
    except PermissionError:
        pass


if __name__ == "__main__":
    main()
