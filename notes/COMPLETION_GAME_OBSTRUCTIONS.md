# Structural obstructions for tree-of-pools and two-pool completion games

Session 5, 2026-11-01. The universal target $B^* = 1 + \beta^* \approx 1.9007617$
remains unresolved. This note resolves the mathematical task posed at the end of
`COMPLETION_GAME.md` (lines 199--201):

> *"The next mathematical task is to find a graph-realized envelope propagated
> by (5)--(6) that forces that surplus, or give an upper strategy below B on
> this extended family and change the construction again."*

We prove both an exact closed-form representation of the continuation envelopes
propagated by Equations (5)--(6) of `COMPLETION_GAME.md` and a set of
structural upper bounds showing that **neither the two-pool completion game nor
any tree-of-pools generalization can close the gap to $B^*$**. We also identify
the exact structural synthesis required for the next candidate family.

---

## 1. Exact retired-surplus interface and affine-simplex envelope propagation

In `COMPLETION_GAME.md`, at any prefix graph $G = (V, E)$ with pool weights
$w_i > 0$ and monotone online coordinates $y_i \in [0, 1]$, appending private
twin leaves to an offline vertex cover $C$ yields the exact terminal competitive
surplus (Equation (1) of `COMPLETION_GAME.md`):

$$A - \tau_\theta(G)
  = \sum_{i \in V} w_i y_i - \min_{C \text{ cover of } G} \sum_{i \in C} w_i(\beta + y_i)
  = \max_{C \text{ cover of } G} \left(\sum_{i \notin C} w_i y_i - \beta \sum_{i \in C} w_i\right). \tag{1}$$

Let $U$ be the current active boundary ($|U| = k$), $A_{\text{ret}} = \sum_{i \notin U} w_i y_i$
be the sunk online cost of retired pools, and $H(S)$ ($S \subseteq U$) be the
reweighted conditional cover table of `COMPLETION_GAME.md` Equation (2). Define
the **retired surplus table**:

$$E(S) := A_{\text{ret}} - H(S)
  = \max_{\substack{C \text{ cover of } G \\ C \cap U = S}}
    \left(\sum_{i \notin (C \cup U)} w_i y_i - \beta \sum_{i \in C \setminus U} w_i\right). \tag{2}$$

Absorbing $A_{\text{ret}}$ into $E(S)$ eliminates the separate sunk-cost state
and makes every coordinate coefficient in (1) non-negative ($+w_i$ if $i \notin C$
and $0$ if $i \in C$). In total-surplus coordinates $V_h(w, x, E) := A + W_h(w, x, H)$:

1. **Terminal completion ($h = 0$)**:
   $$V_0(w, x, E) = \max_{S \subseteq U} \left( E(S) + \sum_{u \in U \setminus S} w_u x_u - \beta \sum_{u \in S} w_u \right). \tag{3}$$
2. **Pool addition ($U \to U \cup \{v\}$ with weight $b$ and neighborhood $N \subseteq U$)**:
   $$E_{\text{ext}}(S \cup \{v\}) = E(S), \qquad
     E_{\text{ext}}(S) = \begin{cases} E(S) & \text{if } N \subseteq S, \\ -\infty & \text{otherwise.} \end{cases} \tag{4}$$
3. **Pool retirement ($U_{\text{ext}} = U \cup \{u\} \to U$ at coordinate $r_u$)**:
   $$E_{\text{new}}(S) = \max\Big( E_{\text{ext}}(S) + w_u r_u, \; E_{\text{ext}}(S \cup \{u\}) - \beta w_u \Big). \tag{5}$$

### Theorem 1 (Exact Affine-Simplex Representation of $W_h$)

For every horizon $h \ge 0$ and active boundary $U$ of size $k$, the exact
minimax value $V_h(w, x, E) = A + W_h(w, x, H)$ of `COMPLETION_GAME.md`
Equation (6) is the pointwise maximum of finitely many affine functionals

$$V_h(w, x, E) = \max_{p \in \mathcal{P}_h}
  \left( c_p + \sum_{u \in U} \alpha_{p, u} x_u + \sum_{S \subseteq U} \mu_{p, S} E(S) \right), \tag{6}$$

where $0 \le \alpha_{p, u} \le w_u$ for all $u \in U$ and $\mu_p \in \Delta(2^U)$
($\mu_{p, S} \ge 0$, $\sum_{S \subseteq U} \mu_{p, S} = 1$). Equivalently, in the
original variables $(w, x, H)$ of `COMPLETION_GAME.md`:

$$W_h(w, x, H) = \max_{p \in \mathcal{P}_h}
  \left( c_p - \sum_{u \in U} (w_u - \alpha_{p, u}) x_u - \sum_{S \subseteq U} \mu_{p, S} H(S) \right). \tag{7}$$

*Proof.* At $h = 0$, Equation (3) has $2^k$ planes with $c_S = -\beta \sum_{u \in S} w_u$,
$\alpha_{S, u} = w_u \mathbf{1}_{u \notin S} \in [0, w_u]$, and $\mu_{S, S'} = \mathbf{1}_{S' = S} \in \Delta(2^U)$.
Inductively:
- Retiring $u \in U_{\text{ext}}$ substitutes (5) into $\sum_{S} \mu_{p, S} E_{\text{new}}(S)$.
  Because $\mu_{p, S} \ge 0$, each term branches into $\mu_{p, S} E_{\text{ext}}(S) + \mu_{p, S} w_u r_u$
  or $\mu_{p, S} E_{\text{ext}}(S \cup \{u\}) - \mu_{p, S} \beta w_u$ (with the second
  branch forced whenever $u$ has an uncovered active neighbor outside $S$).
  Summing over $S$ gives $\alpha_{p, u} = w_u \sum_{S : u \notin C} \mu_{p, S} \in [0, w_u]$
  and preserves $\sum \mu = 1$.
- Adding $v$ with weight $b$ and neighborhood $N \subseteq U$ drops any plane put
  weight on an invalid mask ($v \notin S$ and $N \not\subseteq S$), expands
  $\alpha_{p, i} \max(x_i, 1 - t)$ over $R \subseteq N$, and applies the exact
  two-line minimax identity (`TWO_POOL_RESPONSE.md` Section 3) over $t \in [0, 1]$.
  Since the $t$-slopes $m_{p, R} = \gamma_p - \sum_{i \in R} \alpha_{p, i}$ are
  independent of $(x, E)$, convex combinations $(\lambda_1, \lambda_2) \in \Delta_2$
  preserve both $\alpha_u \in [0, w_u]$ and $\mu \in \Delta(2^U)$. $\blacksquare$

---

## 2. The Tree-of-Pools / Depth-First Obstruction Theorem ($1 + 1/\sqrt{2}$ ceiling)

Before analyzing cycles created by multi-pool boundaries, consider any
**tree of pools** $T$ of arbitrary depth $h$, arbitrary branching, arbitrary
adaptive pool weights, and terminal private-leaf completions (1). For any
subtree $T_u$ rooted at $u$ with final coordinate $y_u^{\text{final}}$, let
$O(T_u)$ and $I(T_u)$ denote the maximum of (1) on $T_u$ subject to $u \notin C$
and $u \in C$, respectively, and $M(T_u) = \max(O(T_u), I(T_u))$. Then:

$$O(T_u) = y_u^{\text{final}} + \sum_{v \in \text{children}(u)} w_v I(T_v), \qquad
  I(T_u) = -\beta + \sum_{v \in \text{children}(u)} w_v M(T_v). \tag{8}$$

### Theorem 2 (Tree-of-Pools Obstruction)

For every $\beta \ge \frac{1}{\sqrt{2}} \approx 0.70710678$, there is an explicit
online coordinate strategy guaranteeing $M(T) \le 0$ at every prefix of every
rooted tree of pools $T$ of arbitrary depth $h$.

*Proof.* When a node $u$ arrives as a child of its parent $p$, set its birth
coordinate to $z_u = 1 - y_p \in [0, 1]$. As children $v(\xi)$ of $u$ arrive and
complete their subtrees $T_{v(\xi)}$ with $I(T_{v(\xi)}) < 0$, define the
rescaled cost clock $d\tilde{\xi} = \frac{-I(T_{v(\xi)})}{\beta}\,d\xi$. Evolve
$y_u(\tilde{\xi})$ via the linear ODE (capped at $1$):

$$y_u(0) = z_u, \qquad
  \frac{dy_u}{d\tilde{\xi}} = \beta - \frac{z_u}{\beta}\big(1 - y_u(\tilde{\xi})\big). \tag{9}$$

Inductively assuming $\frac{M(T_{v(\xi)})}{-I(T_{v(\xi)})} \le \frac{1 - y_u(\tilde{\xi})}{\beta}$
for each child subtree $T_{v(\xi)}$, we have:
1. **Strict monotonicity**: Since $z_u(1 - z_u) \le \frac{1}{4} < \beta^2$ for all
   $\beta \ge \frac{1}{\sqrt{2}} > \frac{1}{2}$, $\frac{dy_u}{d\tilde{\xi}}\big|_{\tilde{\xi}=0} = \frac{\beta^2 - z_u(1 - z_u)}{\beta} > 0$,
   so $1 - y_u(\tilde{\xi})$ decreases exponentially and $y_u(\tilde{\xi})$ is
   strictly increasing until reaching $1$.
2. **Exact constant ratio**: Integrating $\big(1 - y_u(\tilde{\xi})\big)\,d\tilde{\xi} = \frac{\beta}{z_u}\big(\beta\,d\tilde{\xi} - dy_u\big)$
   from $0$ to any stopping time $\tilde{\xi}$ before saturation gives:
   $$I(T_u; \tilde{\xi}) \le -\beta + \int_0^{\tilde{\xi}} \big(1 - y_u(t)\big)\,dt
     = -\frac{\beta}{z_u}\big(y_u(\tilde{\xi}) - \beta \tilde{\xi}\big)
     = -\frac{\beta}{z_u} O(T_u; \tilde{\xi}). \tag{10}$$
   Hence $\frac{O(T_u; \tilde{\xi})}{-I(T_u; \tilde{\xi})} \le \frac{z_u}{\beta}$
   and $\frac{M(T_u; \tilde{\xi})}{-I(T_u; \tilde{\xi})} \le \frac{z_u}{\beta}$ for
   **all** stopping times $\tilde{\xi} \ge 0$, matching the Depth-1 leaf ratio
   $\frac{z_u}{\beta}$. At the root $r$ ($z_r = 0$), $y_r(\tilde{\xi}) = \min(1, \beta \tilde{\xi})$
   gives $O(T_r; \tilde{\xi}) = 0$ and $I(T_r; \tilde{\xi}) \le -\beta + \int_0^{1/\beta}(1 - \beta t)\,dt = -\beta + \frac{1}{2\beta} \le 0$
   for all $\beta \ge \frac{1}{\sqrt{2}}$. $\blacksquare$

---

## 3. Exact Conservation Law and Breadth-First Slack Identity

Why does Theorem 2 allow the online player to evade the Wang--Wong recurrence
$f_1(y) = \beta - \frac{y^2}{2\beta}$ on any single node expansion, and why do
breadth-first alternation constructions (Wang--Wong Prop. 2; Lu 2026) beat
$1 + \frac{1}{\sqrt{2}}$ only to stall at $1 + \frac{\sqrt{e}}{2} \approx 1.82436$?

### Proposition 1 (Exact Depth-1 Conservation Identity)

For any node $u$ with birth potential $z_u = 1 - y_x$, let $R_u^* = y_x / \beta$.
For **every** integrable trajectory $y_u : [0, R_u^*] \to [z_u, 1]$:

$$\int_0^{R_u^*} \Big(O_1(u; \xi) - (1 - y_x)\Big)\,d\xi
  + \Big(I_1(u; R_u^*) + f_1(y_x)\Big) \equiv 0, \tag{11}$$

where $O_1(u; \xi) = y_u(\xi) - \beta \xi$, $I_1(u; R_u^*) = -\beta + \int_0^{R_u^*}(1 - y_u(\xi))\,d\xi$,
and $f_1(y_x) = \beta - \frac{y_x^2}{2\beta}$.

*Proof.* Substitute $y_u(\xi) - (1 - y_x) = (1 - z_u) - (1 - y_u(\xi))$ into the
first integral and note that $\int_0^{R_u^*} (y_x - \beta \xi)\,d\xi = \frac{y_x^2}{2\beta} = \beta - f_1(y_x)$. $\blacksquare$

- In a **tree of pools** (Theorem 2), the adversary must evaluate $O_1(u; \xi)$
  and $I_1(u; \xi)$ at the **same** stopping time $\xi$. The ODE (9) makes
  $O_1(u; \xi) < 1 - y_x$ for $\xi > 0$, paying for $I_1(u; R_u^*) > -f_1(y_x)$.
- In **breadth-first alternation** ($L_0 \to R_1 \to L_2$), stopping at $\xi = 0$
  (after Phase 1) evaluates $O_1(u; 0) = 1 - y_x$ with equality, while continuing
  to the end of Phase 2 ($\xi = R_u^*$) evaluates $I_1(u; R_u^*)$, and stopping
  *during* Phase 2 at $\xi \in (0, R_u^*)$ puts $L_0 \cup L_2(\xi) \in C$ and
  $R_1 \notin C$.
- However, if $L_0$ is an **undivided** pool of weight $1$ (as in Wang--Wong
  Prop. 2 and Lu 2026) and Phase 1 stops at $r < R_{\max}$ to enter Phase 2,
  putting $L_0 \in C$ costs the full $\beta$, leaving the **Breadth-First Slack**:
  $$\operatorname{Slack}(r) = \beta - \int_0^r \big(1 - y_{L_0}(\tau)\big)\,d\tau, \qquad
    \operatorname{Slack}(r) - \int_0^r y_{L_0}(\tau)\,d\tau = \beta - r. \tag{12}$$
  For all $r \le \beta$, $\operatorname{Slack}(r) \ge \int_0^r y_{L_0}(\tau)\,d\tau$,
  allowing the online player to jump all coordinates in $R_1([0, r])$ to $1$ at
  $\xi = 0^+$ without violating the Phase-2 cover $L_0 \in C$.

---

## 4. Why the Two-Pool Completion Game (`COMPLETION_GAME.md` Eq. (6)) Cannot Close the Gap

Evaluating Equation (6) of `COMPLETION_GAME.md` via Theorem 1 and exact
primal-dual LPs (`scripts/completion_game_obstructions.py`) reveals a sharp
bottleneck:

1. **Strict two-arrival-per-phase game (`COMPLETION_GAME.md` Section 4)**:
   When each phase adds two pools $b, d$ on the opposite side and then retires
   both $a, c$, every pool receives at most two phase children before retirement.
   With unit weights $w_i = 1$, the minimax initial surplus is positive at
   $\beta = 0.60$ (`+0.10096` at phase 3) and $0$ for all $\beta \ge 0.65$.
   Even with unequal weights, restricting each phase to two arrivals prevents
   multi-step ski rental on an active pool, capping the game below $1 + \frac{1}{\sqrt{2}} \approx 1.707107$.

2. **General two-pool selective-retirement game (`COMPLETION_GAME.md` Eq. (6))**:
   Allowing single-pool selective retirement after every arrival permits an
   arbitrary Depth-1 retired prefix $r_0$ on $L_0$ before two pools $b_1, b_2 \in R_1$
   are kept active and $L_0$ is retired, followed by an arbitrary Phase-2
   continuum $L_2$ on $\{b_1, b_2\}$. However, because the active boundary has
   size $|U| \le 2$ (pathwidth at most $2$):
   - **At most two pools $\{b_1, b_2\} \subseteq R_1$ can survive into Phase 2**
     to receive common neighbors in $L_2$. All earlier pools in $r_0 \subseteq R_1$
     must be retired while $L_0$ is still active, permanently locking them at
     Depth 1 ($f_0(y) = \beta$).
   - By Fubini's theorem, on $k$ active pools $b_1, \dots, b_k \in R_1$ with
     weights $w_i$ and birth coordinates $1 - y_i$, evolving $u(\xi)$ in Phase 2
     along $\sum_{i=1}^k w_i \max(1 - y_i, u(\xi)) - \beta \xi = \text{const}$
     yields total Phase-2 return $\sum_{i=1}^k \frac{w_i y_i^2}{2\beta}$,
     replacing $f_0(y) = \beta$ by $f_1(y_i) = \beta - \frac{y_i^2}{2\beta}$ on
     **at most $k$ discrete steps**.
   - At $k = 2$ (`COMPLETION_GAME.md`), the 2-alternation minimax competitive
     ratio is only $\approx 1.7219$ for equal active weights (and $\approx 1.7273$
     for unequal active weights), compared to $1.7157$ at $k = 1$ (breadth-first
     after retired prefix $r_0$), $1.7313$ at $k = 4$, $1.7401$ at $k = 8$, and
     $1.7530$ as $k \to \infty$.

---

## 5. Layered Phase Upper Bound and Resumable Alternation Analysis

### Theorem 3 (Exact Upper Bound for Graded $k$-Phase Graphs)

Suppose an online bipartite graph $G = (V, E)$ is graded into layers
$V_0, V_1, \dots, V_k, V_{k+1}$ where $V_0$ arrives isolated, each vertex
$v \in V_m$ ($1 \le m \le k$) arrives with edges only to $V_{m-1}$ (so each
$u \in V_{m-1}$ receives future neighbors only in $V_m$), $V_{k+1}$ consists of
terminal private leaves (or universal extensions) on $V_k$, and the layer index
$m$ is known upon arrival. Define the layer-dependent allocation functions:

$$f_0(y) = \gamma_k, \qquad
  f_j(y) = \gamma_k - \int_{1-y}^1 \frac{1-t}{f_{j-1}(t)}\,dt \quad (1 \le j \le k-1), \tag{13}$$

where $\gamma_k$ is the unique positive root of $\int_0^1 \frac{1-t}{f_{k-1}(t)}\,dt = \gamma_k$
($\gamma_1 = \frac{1}{\sqrt{2}} \approx 0.70710678$, $\gamma_2 \approx 0.78252452$,
and $\gamma_k \uparrow \beta^* \approx 0.90076170$ as $k \to \infty$). Then running
Wang--Wong `GreedyAllocation` with allocation function $f_{k-m}(y)$ on layer $V_m$
is $(1 + \gamma_k)$-competitive on **every** such graph $G$, regardless of
subset neighborhoods, weights, or branching structure between $V_{m-1}$ and $V_m$.

*Proof.* Extending Wang and Wong's 2-alternation charging lemma (`focs13_obvc.tex`
Lemma 5 / `appendix.tex` Section 4), when $v \in V_m$ arrives with water level
$y = 1 - z_v$, charge $w_v y_v^* \big(z_v + f_{k-m}(1 - z_v)\big)$ to $v$ and
$w_u y_u^* \big((y - y_u^{\text{old}}) + \int_{y_u^{\text{old}}}^y \frac{1-t}{f_{k-m}(t)}\,dt\big)$
to each neighbor $u \in N(v) \cap V_{m-1}$ whose coordinate increases. Because
every future neighbor of $u \in V_{m-1}$ lies in $V_m$ and uses the **same**
allocation function $f_{k-m}$, the integral charges on $u \in V_{m-1}$ telescope
as $y_u$ increases from $z_u$ to at most $1$, bounding the total charge on $u$ by
$w_u y_u^* \big(1 + f_{k+1-m}(1 - z_u) + \int_{z_u}^1 \frac{1-t}{f_{k-m}(t)}\,dt\big) \le w_u y_u^* (1 + \gamma_k)$. $\blacksquare$

### Exact Decomposition of the 2-Alternation Gap ($k = 2$)

At $k = 1$, Lu's recurrence and Theorem 3 coincide ($\beta_1^{\text{Lu}} = \gamma_1 = 1/\sqrt{2}$).
At $k = 2$ (two online layers $R_1, L_2$ plus terminal private leaves), they diverge:
Wang--Wong Prop. 2 / Lu ($h=1$) gives $\beta_{\text{WW2}} = \sqrt{\frac{1+e^{-2}}{2}} \approx 0.75343722$,
whereas Theorem 3 gives $\gamma_2 \approx 0.78252452$. By Proposition 1 (Eq. 11),
if at every step $r$ of Phase 1 the Phase-2 increment on $R_1([0, r])$ satisfied
$\int_0^r \big(z^{(r, \xi)}(\tau) - z^{(r, 0)}(\tau)\big)\,d\tau \le \beta \xi$
(zero free slack at $\xi = 0^+$), Fubini's theorem would force Phase-2 payment
$\int_0^\Xi t(\xi)\,d\xi = \int_0^r \frac{y_0(\tau)^2}{2\beta}\,d\tau$, yielding
$y_0'(r) = \beta - \frac{y_0(r)^2}{2\beta} = f_1(y_0(r))$ and $\beta = \gamma_2 \approx 0.78252452$.

Two distinct relaxations in Wang--Wong Prop. 2 / Lu ($h=1$) account for the gap
from $\gamma_2 \approx 0.78252452$ down to $\beta_{\text{WW2}} \approx 0.75343722$:

1. **Pigeonhole vs. exact monotone profile (`lu_baseline`)**:
   Wang--Wong Prop. 2 bounds $\min_{\tau \in [0, r]} z^{(r, \xi)}(\tau)$ by the
   average $\frac{\beta(1+\xi)}{r}$, ignoring the unequal Phase-1 birth profile
   $z(\tau) = 1 - y_0(\tau)$. Enforcing exact coordinate monotonicity
   $\int_0^r \max\big(1 - y_0(\tau), u\big)\,d\tau \le \beta(1 + \xi)$ raises the
   continuum 2-alternation threshold from $\beta_{\text{WW2}} \approx 0.75343722$
   to $\beta_{\text{lu\_cont}} \approx 0.76202043$.
2. **Terminal Phase 2 vs. Resumable Phase 1 (`depth1_D` and `full_D_phase2`)**:
   In `lu_baseline`, Phase 2 at time $r < R_{\max}$ is a terminal side-branch
   (no further Phase-1 vertices arrive on $L_0$), leaving unused in-cover slack
   $\beta - \int_0^r (1 - y_0(\tau))\,d\tau > 0$ that lets the online player jump
   the water level on $R_1([0, r])$ at $\xi = 0^+$.
   - Why naive KVV progressive retirement on $L_0$ fails: splitting
     $L_0 = A_1 \cup \dots \cup A_K$ and connecting $b_r$ only to $\{A_r, \dots, A_K\}$
     freezes retired slices $A_i$ ($i < r$) at $y_{A_i}(i) < 1$, reducing the
     online payment on $L_0$ and worsening the minimax surplus.
   - **Resumable Phase-1 / Interleaved Alternation**: When the adversary can
      instead **resume Phase 1 on the undivided $L_0$** ($b_{r+1}, \dots, b_K$)
     after stopping Phase 2 on $R_1([0, r])$ at $\xi$, any coordinate jump on
     $R_1([0, r])$ during Phase 2 is permanently locked in by monotonicity and
     penalized in the resumed full in-cover $L_0 \in C, R_1([0, l]) \notin C$.
   - With a Depth-1 resumed Phase-1 continuation (`depth1_D`), the in-cover budget
     at $(r, \xi)$ is tightened by $-\frac{(1 + T(r, \xi) - \beta r)_+^2}{2\beta}$,
     raising the continuum threshold to $\beta_{\text{D1\_cont}} \approx 0.76535003$.
   - With a Phase-2-equipped resumed Phase-1 continuation (`full_D_phase2`,
     including all mixed prefix covers $L_0 \in C, R_1([0, r]) \subseteq C, L_2^{(r)} \cap C = \emptyset, R_1([r, l]) \cap C = \emptyset, L_2^{(l)} \subseteq C$),
     the sparse LP (`scripts/resumable_alternation_check.py`) shows a strictly
     larger and growing gain over `lu_baseline` across $K \in \{6, 8, 10, 12, 14\}$
     (`+0.00632`, `+0.00829`, `+0.00895`, `+0.01002`, `+0.01048` at $\beta = 0.75$),
     extrapolating to $\beta_c(\infty) \approx 0.772$ for two Phase-2 bursts
     (more than halfway from $\beta_{\text{lu\_cont}} \approx 0.7620$ to
     $\gamma_2 \approx 0.7825$).

---

## 6. Next Steps to Close the Gap

1. **Infinite-round resumable / fully interleaved 2-alternation fixed point**:
   In `full_D_phase2` (two bursts), the second Phase-2 burst at step $l \in [r, R_{\max}]$
   still has terminal suffix slack $\int_l^{R_{\max}} z^{\text{D}}(\tau)\,d\tau$
   because Phase 1 does not resume a third time after the second burst. Formulate
   and solve the infinite-round resumable operator at $k = 2$ (where Phase 1 can
   resume after *every* Phase-2 burst) to determine whether infinite-round
   resumption at $k = 2$ reaches the Theorem 3 ceiling $\gamma_2 \approx 0.782525$
   or an intermediate threshold.
2. **Multi-layer recursive extension ($k \to \infty$)**:
   Combine multi-round resumable alternation across $k$ layers ($V_0, V_1, \dots, V_k$)
   and analyze the $k \to \infty$ fixed-point equation to test convergence toward
   $\gamma_\infty = \beta^* \approx 0.9007617$.
3. **Finite-witness bridge**:
   Convert any strict continuum violation above $1 + \sqrt{e}/2$ into a certified
   finite realization-oblivious bipartite instance via rational grid discretization.

---

## Verification

- Run `python scripts/completion_game_obstructions.py` to verify Theorem 1,
  Theorem 2, Proposition 1, symbolic plane propagations, and $k$-pool LP scaling
  (`experiments/completion-game-obstructions.json`).
- Run `python scripts/resumable_alternation_check.py` to verify Theorem 3
  ($\gamma_1, \gamma_2$), continuum thresholds ($\beta_{\text{WW2}}, \beta_{\text{lu\_cont}}, \beta_{\text{D1\_cont}}$),
  and sparse LP scaling across $K \in \{6, 8, 10, 12\}$ for `lu_baseline`,
  `depth1_D`, and `full_D_phase2` (`experiments/resumable-alternation-check.json`).
