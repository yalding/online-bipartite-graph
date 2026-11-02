# Finite future neighborhoods and repeated biclique probes

November 1, 2026. These two calculations distinguish a restriction on the
adversary from a restriction on the online strategy.

## An all-horizon upper bound for the retired two-pool game

In the game of [Session 4](COMPLETION_GAME.md) each pool has at most two
later neighboring pools before terminal completion. Sizes can be arbitrary
and unequal. Core arrivals are announced whole batches with a common
neighborhood. The following algorithm guarantees $13/7$ at every horizon,
including any permitted private completion.

Let $f(t)=a-bt$, with $a=6/7,\ b=9/14,\ c=a-b=3/14$.
At the arrival of a pool of weight $w$, pick the largest $t\in[0,1]$
such that the total cost of raising its old neighbors to at least $t$
is at most $w f(t)$. Perform those raises and assign the new pool $1-t$.
This is weighted GreedyAllocation. Its spending limit holds with equality
whenever $t<1$, by continuity.

Fix any integral quotient cover $C$ at the current prefix. To bound the
cost **outside** $C$, charge a new pool in $C$ at most $wf(t)$ for
its old neighbors' increases. A new pool outside $C$ has every neighbor
in $C$. Charge its birth cost $w(1-t)$ to these neighbors in proportion
to their increases. A neighbor of weight $w_i$ raised from $s$ to $t$
then receives charge $w_i(t-s)g(t)$, where $g(t)=(1-t)/f(t)$.
If $t=1$ there is no birth charge. Charges can include old in-cover
increases as an overestimate. This accounts for every out-of-cover
coordinate with no assumptions on the final cover other than feasibility.

Consequently a cover pool born at $z$ is charged, per unit weight, at
most $f(1-z)+S_d(z)$, where $S_d(z)$ maximizes
$\sum_j(t_j-t_{j-1})g(t_j)$ over at most $d$ later increases from
$t_0=z$. Append $t_{d+1}=1$ and pad with zero-length intervals. Since
$g(1)=0$, the sum does not change. Writing $u_j=f(t_j)$ gives

$$
S_d(z)=\frac{f(z)+dc-(d+1)c(f(z)/c)^{1/(d+1)}}{b^2}.
$$

Indeed each summand is
$(u_{j-1}-u_j-c(u_{j-1}/u_j-1))/b^2$. The product of the $d+1$
ratios is $f(z)/c$, and equal ratios minimize their sum by AM–GM.
The resulting water levels are feasible. The formula is convex in $z$.
Adding the affine $f(1-z)$ preserves convexity, so only its endpoints
need checking. For $d=2,z=1$ the bound is $a$. For $z=0$,
$c+S_2(0)\le a$ is equivalent to $4^{1/3}\ge311/196$.
The exact margin after cubing is $37913/7529536>0$.

Thus outside cost is at most $(6/7)w(C)$ simultaneously for every cover.
At an ordinary stop choose a minimum cover and bound in-cover coordinates by
one. For the private completion on $C$, raise selected pools to one upon
their first private neighbors, assigning the leaves zero. The completed
cost is at most $(13/7)w(C)$ and the private matching certifies optimum
$w(C)$. This covers stops after either arrival decision within a phase.
The upper bound uses the public batch protocol. Unannounced sequential
arrivals can have many more positive raises on the same old pool.

### Any fixed bound on the number of later pools costs a strict gap

The argument also gives a strict gap below $B^*$ for each fixed finite
$d$, with a strategy allowed to depend on $d$. Let $f_*$ be the
Wang–Wong equalizing allocation, $g_*=(1-t)/f_*(t)$, and
$J(z)=\int_z^1 g_*(t)\,dt$. Its closed form, with
$a_*=(k+1)/2,\ b_*=(k-1)/2,\ k=\coth k$, gives

$$
-g_*'(t)=\frac{a_* b_*}{f_*(t)(a_*-t)(t+b_*)}\ge m>0
$$

on the closed unit interval. Take $m=\min(-g_*')$. The error in each
right-endpoint rectangle of length $\ell$ is at least $m\ell^2/2$.
The $d+1$ intervals have total length $1-z$. Cauchy–Schwarz and
$J(z)\le(1-z)^2/(2 f_*(1))$ yield

$$
S_d(z)\le (1-\lambda_d)J(z),\qquad
\lambda_d=\frac{m f_*(1)}{d+1}.
$$

Here $S_d$ uses $g_*$, and $0<\lambda_d<1$ for $d\ge1$ since
$-g_*'(1)=1/f_*(1)$. Scale the actual allocation to
$\sqrt{1-\lambda_d}\, f_*$. This multiplies the birth charge by the
scale and divides the rectangle charges by it. The resulting excess is at
most $\sqrt{1-\lambda_d}(B^*-1)$ by the equalizing identity. Thus a
hardness program with a uniform bound on future neighboring batches cannot
approach the target, even with unequal sizes and terminal completions.
The gap depends on $d$. [Wang and Wong, Section 4](https://arxiv.org/abs/1305.1694)

## Lu's profile as a biclique response rule

The handoff simulator tries using Lu's deficit profile as the newcomer's
intended birth coordinate on a complete bipartite graph. It raises the
opposite side to at least $1-D(t)$, where $t$ is the newborn side's
new count divided by the opposite count. This interpretation has an
**unbounded** competitive ratio. Lu proves a necessary bound on births
using a recurrence and does not propose this policy. [Lu, critical fixed point](https://arxiv.org/abs/2608.09210)

For $j=1,\ldots,k$, grow the left side to $2^j$ vertices and then
introduce exactly one right vertex. Every arrival sees every earlier
opposite vertex. The $j$-th right birth has $t=j/2^j\le1/2$, where
the critical profile is exactly $D(t)=1-\beta t$,
$\beta=\sqrt e/2$. All left vertices born since the previous probe,
at least $2^{j-1}$ of them, now have coordinate at least $\beta j/2^j$.
Later raises are irreversible. These cohorts are disjoint, so left cost
alone is at least $\beta k(k+1)/4$, against offline optimum $k$.
The whole input is predetermined. Already $k=9$ gives 512 left and
nine right vertices and a ratio greater than $92/45>2$, using the
actual size two of the first cohort and the rational bound $\beta>4/5$.

For an arbitrary competitive algorithm, let $z_j$ be its expected
coordinate on the $j$-th right birth. The same graph gives the necessary
history-sensitive inequality

$$
\sum_{j=1}^k (2^j-2^{j-1})(1-z_j)\ \le\ (R-1)k
$$

for a strategy of universal ratio $R$. Use the right-side cover and
private leaves for this budget. The bound counts only one of the two
vertices in the first cohort. A strategy can satisfy it by spending more
on the rare newcomers. Thus the probe refutes the proposed policy, while
the general problem requires a second continuation that punishes that
response on the same public prefix.
