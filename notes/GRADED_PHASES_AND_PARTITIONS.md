# Graded Phase Recursion, Terminal Boundary Conditions, and Active Partition Dynamics

Session 6, 2026-11-01.

Session 7 corrected the limiting-threshold calculation below and
disproved the tree ceiling used in the historical synthesis. See
[the finite counterexample](TREE_CONTINUATIONS.md) and the
[optimality proof](OPTIMALITY_PROOF.md).

This note documents the audit and structural analysis of the Graded $k$-Phase
Allocation Theorem (Session 5 Theorem 3), its exact terminal boundary conditions,
and its synthesis with Tang's (2026) active partition construction for two-sided
online bipartite matching.

---

## 1. Audit of the Graded $k$-Phase Allocation Recursion

In `COMPLETION_GAME_OBSTRUCTIONS.md` (Session 5 Theorem 3), we established that on
any online bipartite graph $G = (V, E)$ graded into $k$ online layers
$V_0, V_1, \dots, V_k$ where vertices in $V_m$ have past neighbors only in
$V_{m-1}$ and future neighbors only in $V_{m+1}$, Wang--Wong `GreedyAllocation`
with layer-dependent allocation functions $f_{k-m}(y)$ is $(1 + \gamma_k)$-competitive.

Auditing this recursion reveals that the behavior of the base layer $f_0(y)$
depends crucially on the **terminal boundary condition** of the instance:

### Variant A: Constant Terminal Boundary ($f_0(y) = \gamma$)
- **Applies to:** Instances where the terminal layer $V_k$ receives terminal
  private leaves (or is evaluated against arbitrary terminal offline vertex covers
  $C \subseteq V_0 \cup \dots \cup V_k$).
- **Derivation:** A vertex $v \in V_k$ in the cover is responsible for its birth
  charge $z_v + f_0(1 - z_v) = z_v + \gamma$, and its private leaf liability
  $\int_{z_v}^1 \frac{1-t}{\beta}\,dt = \frac{(1 - z_v)^2}{2\beta}$. Balancing
  these requires $f_0(y) \equiv \gamma$.
- **Sequence:**
  $$\gamma_1 = \frac{1}{\sqrt{2}} \approx 0.70710678, \quad
    \gamma_2 \approx 0.78252453, \quad
    \gamma_3 \approx 0.82161879, \quad \dots, \quad
    \gamma_k \uparrow \beta^* \approx 0.90076170.$$

### Variant B: Linear Terminal Boundary ($f_0(y) = \gamma + y$)
- **Applies to:** Instances where the graph strictly terminates at layer $V_k$
  (no future arrivals and no private leaves on $V_k$).
- **Derivation:** An online vertex $v \in V_k$ receives **no future edges**, so it
  never absorbs future neighbor charges. Its total budget during processing is
  $y_v + f_0(1 - y_v) = (1 - y) + f_0(y)$. Choosing $f_0(y) = \gamma + y$ yields
  a constant investment $(1 - y) + (\gamma + y) = 1 + \gamma$.
- **Sequence:**
  - At $k = 1$ (1-sided bipartite vertex cover: offline $V_0$, online $V_1$):
    $$\int_0^1 \frac{1 - t}{\gamma + t}\,dt = (1 + \gamma)\ln\left(1 + \frac{1}{\gamma}\right) - 1 = \gamma
      \implies \ln\left(1 + \frac{1}{\gamma}\right) = 1
      \implies \gamma_1 = \frac{1}{e - 1} \approx 0.58197671.$$
    This **exactly reproduces** the celebrated Karp--Vazirani--Vazirani (1990)
    and Wang--Wong (2013) 1-sided bipartite competitive ratio:
    $$1 + \gamma_1 = 1 + \frac{1}{e - 1} = \frac{e}{e - 1} \approx 1.58197671.$$
  - For $k \ge 2$, intermediate layers use the integral recurrence
    $f_j(y) = \gamma - \int_{1-y}^1 \frac{1-t}{f_{j-1}(t)}\,dt$:
    $$\gamma_2 \approx 0.74682639, \quad
      \gamma_3 \approx 0.80266708, \quad \dots, \quad
      \gamma_k \uparrow \beta^* \approx 0.90076170.$$

### Numerical Convergence Table ($k = 1 \dots 14$)

The numerical solutions (verified in `scripts/graded_phase_recursion.py` and
recorded in `experiments/graded-phase-recursion.json`) are:

| Layer $k$ | Variant A: $\gamma_k$ (Const Terminal) | Ratio $1 + \gamma_k$ | Variant B: $\gamma_k$ (Linear Terminal) | Ratio $1 + \gamma_k$ | Gap to $\beta^*$ |
|---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 0.70710678 | 1.70710678 | 0.58197671 | 1.58197671 | 0.193655 / 0.318785 |
| 2 | 0.78252453 | 1.78252453 | 0.74682639 | 1.74682639 | 0.118237 / 0.153935 |
| 3 | 0.82161879 | 1.82161879 | 0.80266708 | 1.80266708 | 0.079143 / 0.098095 |
| 4 | 0.84341458 | 1.84341458 | 0.83248662 | 1.83248662 | 0.057347 / 0.068275 |
| 5 | 0.85716847 | 1.85716847 | 0.85015212 | 1.85015212 | 0.043593 / 0.050610 |
| 6 | 0.86641028 | 1.86641028 | 0.86163112 | 1.86163112 | 0.034351 / 0.039131 |
| 7 | 0.87295230 | 1.87295230 | 0.86953581 | 1.86953581 | 0.027809 / 0.031226 |
| 8 | 0.87776295 | 1.87776295 | 0.87523109 | 1.87523109 | 0.022999 / 0.025531 |
| 10 | 0.88424526 | 1.88424526 | 0.88273640 | 1.88273640 | 0.016516 / 0.018025 |
| 12 | 0.88830954 | 1.88830954 | 0.88733570 | 1.88733570 | 0.012452 / 0.013426 |
| 14 | 0.89103097 | 1.89103097 | 0.89036504 | 1.89036504 | 0.009731 / 0.010397 |
| $\infty$ | **0.90076170** | **1.90076170** | **0.90076170** | **1.90076170** | 0.000000 |

### Limiting threshold (corrected in Session 7)

The finite calibration makes the *last* iterate zero at 1. The Wang–Wong
optimizer has $f_*(1)>0$ and satisfies
$\int_0^1(1-t)/f_*(t)\,dt=\beta^*-f_*(1)$.
One cannot pass the finite zero endpoint directly to this optimizer.

Instead, fix a trial $\gamma$ and iterate the operator in (13) of the
Session 5 note. It preserves order, and the first iterate is at most either
initial function, so the sequence is decreasing as long as it stays
positive. At $\gamma=\beta^*$, both initial functions dominate $f_*$,
which is a fixed point. Thus all depths are feasible. Feasibility is
monotone in $\gamma$ and in decreasing the depth.

If $\gamma<\beta^*$ works at every depth, the decreasing iterates have a
nonnegative limit $f$. Their integrals over $[0,1]$ are at most
$\gamma$. Monotone convergence gives the limiting integral equation
$f(y)=\gamma-\int_{1-y}^1(1-t)/f(t)\,dt$, so $f$ is continuous.
It is nonincreasing and positive on $[0,1)$, since a zero strictly before
1 would make the integral infinite. Differentiation in the interior gives
$f(1-y)f'(y)=-y$ and hence
$f(y)f(1-y)=y(1-y)+f(0)f(1)$. If $f(1)=0$, then
$f'/f=-1/(1-y)$, which gives $f(y)=\gamma(1-y)$ and $\gamma=1$,
a contradiction. If $f(1)>0$, the same product identity implies
$(1-y)/f(y)$ is decreasing and $f$ is a positive admissible equalizer.
Its value $\gamma$ contradicts Wang and Wong's minimax bound.
This proves convergence of the finite **allocation thresholds** to
$\beta^*$ without a universal hardness inference.
[Wang and Wong, Section 4](https://arxiv.org/abs/1305.1694)

---

## 2. Analysis of Tang's (2026) Matching Construction vs. Vertex Cover

Tang (arXiv:2602.18049) proved an optimal competitive ratio upper bound of
$\Gamma^* = \frac{1}{B^*} \approx 0.526105$ for two-sided online bipartite matching.
We audited the structure of Tang's construction (`arxiv.tex` Sections 2--4):

### Tang's Two-Pronged Adversarial Mechanism
Tang maintains a dynamic partition of vertices: $V = A \cup I = (\bigcup_i A_i) \cup I$.
In step $k$, for an active partition $A_i$ with matched level $x_{A_i}$, a batch $B_i$ arrives
with size $\epsilon |A_i|$ forming a complete bipartite graph with $A_i$. The online algorithm
matches $a \cdot |B_i|$ edges. The adversary evaluates two terms:

1. **Against Aggressive Algorithms ($a$ is large):**
   $$F_{k-1}(x_{A_i} + \epsilon a) + \epsilon F_{k-1}(a)$$
   If this term is smaller, the adversary **keeps both $A_i$ and $B_i$ active**,
   branching $B_i$ into a **new, independent active partition**. Future arrivals will
   separately attack $A_i$ and $B_i$.
2. **Against Conservative Algorithms ($a$ is small):**
   $$(1 - \epsilon) F_{k-1}(x_{A_i} + \epsilon a) + \epsilon \left(\frac{(1+\epsilon)a + x_{A_i}}{2} - \Gamma\right)$$
   If this term is smaller, the adversary **deactivates $B_i$ and the $|B_i|$ least-matched
   vertices of $A_i$** (denoted $C_i$). The pair $B_i \cup C_i$ is moved to $I$, and the
   adversary recurses on the active remainder $A_i \setminus C_i$.

### Why Tang's Construction Settles Matching Optimality
In matching:
- **Additivity on Inactive Subgraphs:** The subgraph induced by $B_i \cup C_i$ forms a
  complete bipartite graph with $|B_i| = |C_i|$ vertices on each side, which admits a
  **perfect matching of size $|B_i|$**. Crucially, this matching is purely internal to
  $B_i \cup C_i$ and requires zero edges to any other part of the graph.
- Therefore, the offline optimum decomposes additively:
  $$\operatorname{OPT}_{\text{matching}}(V) = \frac{1}{2}|I| + \operatorname{OPT}_{\text{matching}}(A).$$
- Deactivating $B_i \cup C_i$ locks in an irreversible deficit for the online algorithm
  without creating any cross-component liability for the offline comparator!

### The Fundamental Duality Obstruction for Vertex Cover
Why cannot Tang's deactivation mechanism be directly transferred to online vertex cover?
- In vertex cover, covering $B_i \cup C_i$ requires choosing either $B_i \subseteq C$
  or $C_i \subseteq C$.
  - If the offline cover chooses $B_i \subseteq C$, then $C_i \cap C = \emptyset$. But
    $C_i \subset A_i$ already has edges to **earlier arrivals** in the graph! Any earlier
    neighbor of $C_i$ must then be forced into $C$.
  - If the offline cover chooses $C_i \subseteq C$, then $C_i$ incurs offline cost $\beta |C_i|$
    that depends on the past history of $A_i$.
- Thus, unlike matching (where disjoint perfect matchings decouple completely), **vertex
  cover cannot simply freeze and discard subsets of vertices without accounting for the
  global cover consistency of their historical edges**.
- This is precisely why Session 3 and Session 5 proved that single-pool pathwidth $\le 2$
  and rooted trees of pools are strictly capped below $1 + 1/\sqrt{2} \approx 1.7071$.

---

## 3. Synthesis: How to Close the Gap to $B^*$

The synthesis of Theorem 3, the resumable alternation results, and Tang's active partition
dynamics reveals the precise architecture required for a universal vertex cover lower bound:

1. **Graded Layering with $k \to \infty$:**
   As proved in Section 1, the graded layer-dependent upper bound $\gamma_k$ approaches
   $\beta^* \approx 0.90076170$ only as the depth of alternation $k \to \infty$. Finite $k$
   is strictly bounded ($\gamma_1 \approx 0.7071$, $\gamma_2 \approx 0.7825$, $\gamma_3 \approx 0.8216$).
2. **Resumable / Interleaved Alternation Across Layers:**
   The `resumable_alternation_check.py` experiments proved that allowing the adversary
   to **resume Phase 1 on the undivided initial pool $L_0$** after Phase-2 bursts on
   $R_1([0, r])$ closes more than half the gap between Lu's baseline ($\approx 0.7620$)
   and the graded 2-phase ceiling $\gamma_2 \approx 0.7825$ (reaching $\approx 0.772$).
   Extending resumption to arbitrary layer depths $m \in \{1, \dots, k\}$ prevents the
   online player from exploiting slack at any phase transition.
3. **Active Partition Splitting Without Sunk-Cost Isolation:**
   To mimic Tang's branching against aggressive algorithms without falling into the
   offline cover deactivation trap, the adversary must split active pools into sub-pools
   that **continue to participate in future bicliques**, preserving global offline cover
   consistency while forcing the online algorithm to distribute its potential across
   asymmetric branches.
