# Optimal fractional vertex cover under vertex arrivals

Research proof, revised November 2, 2026. Write $B^*=1.9007616968738465\ldots$
for Wang and Wong's upper bound. The new ingredient below is an interleaving
lemma for two rooted subproblems with a single connecting edge.

**Theorem.** For every $\epsilon>0$ and every randomized online fractional
vertex-cover algorithm there is a finite, unweighted bipartite vertex-arrival
input, independent of the algorithm's realized random bits, with $\mathrm{OPT}_f>0$ and
$\mathbb E[\mathrm{ALG}]> (B^*-\epsilon)\mathrm{OPT}_f$.
Together with Wang and Wong's upper bound, this gives the optimal competitive
ratio on bipartite graphs and on general graphs. [Wang and Wong](https://arxiv.org/abs/1305.1694)

Explicitly, let $k>1$ solve $k=\coth k$, put
$a=(k+1)/2,\ b=(k-1)/2$, and write $B^*=1+a^{a/k}b^{b/k}$.
We build the input in two stages. The first stage, called the *core*,
starts with a rooted tree and replaces each node by a *pool*: a group
of vertices with no edges between them and identical neighbors in the
core. For every parent and child in the tree, we put an edge between
every vertex of the parent's pool and every vertex of the child's pool.
These are all the core edges. For example, a parent with three vertices
and a child with two give the six edges of $K_{3,2}$. The second stage
adds individual leaves to selected vertices of the core.

The proof keeps track of the worst cost separately according to whether
the offline cover includes the root. After a child arrives there are
three ways to cover their connecting edge: select the parent only, the
child only, or both. A full-history strategy might
try to spend less by observing which of the two branches grows first.
Sections 2–3 show that the adversary can order the two tests so this
information has no value at either branch's decisions. Section 4 converts those conditional costs into a feasible function for
Wang and Wong's minimax problem. Section 5 then constructs the finite input and completes the theorem. Section 6 gives a separate numerical example.

## 1. A countable game and its conditional costs

We first describe the core by its tree of pools. A positive rational
weight $w_P$ specifies the size of pool $P$ relative to the root, whose
weight is one. In any finite core, choose an integer $d$ that clears
all weight denominators. Pool $P$ then stands for $d w_P$ ordinary
vertices, called twins because they have the same core neighbors. For
example, weights $1$ and $2/3$ on a parent and child give the $K_{3,2}$
above when $d=3$. The two pools lie on opposite sides of the bipartition.

At each move the adversary announces the new pool's weight and its
parent among earlier pools. The parent may acquire further children at
later moves. A public prefix is the ordered list of weights and parent
choices seen so far. A causal strategy assigns its response from this
prefix alone. The adversary may stop after any move, including the root.

A pool coordinate $y_P\in[0,1]$ represents the mean of the fractions
bought on its twins. Their individual fractions may differ. At the end
of a pool's arrivals, summing those fractions gives $d w_P y_P$, and
averaging the edge inequalities between adjacent pools $P,Q$ gives
$y_P+y_Q\ge1$. Thus in units of $d$ the total cost is
$\sum_P w_P y_P$. In the pool game a response maintains these edge
inequalities and may only increase old coordinates. Section 5 obtains such responses from algorithms that see ordinary vertices one at a time.

Fix a rational $0<\beta<B^*-1$. We test the proposed competitive ratio
$1+\beta$. An integral pool cover $C$ is a set of pools containing at
least one endpoint of each tree edge in the prefix. In the expanded
graph it selects every twin in every pool in $C$. Write
$w(C)=\sum_{v\in C}w_v$, where $v$ indexes pools. Define the surplus

$$
L(C)=\sum_{v\notin C}w_v y_v-\beta\sum_{v\in C}w_v .
$$

If $L(C)>0$, the algorithm has spent more than $\beta w(C)$ outside
the proposed cover. To turn this into a violation of $1+\beta$, complete
the core by presenting one new vertex for each selected twin. This
vertex is a private leaf: its only edge joins it to that twin. The
$d w(C)$ private edges have disjoint endpoints. Even a fractional
offline cover must pay at least one on each of these edges, and the
selected twins cover the entire completed graph for exactly $d w(C)$.
The online algorithm must pay for the same private edges while retaining
its earlier purchases outside $C$. Hence in ordinary vertex units
$$
\mathrm{OPT}_f=d w(C),\qquad \mathrm{ALG}\ge d w(C)+d\sum_{v\notin C} w_v y_v.
$$ Lu uses a complete-bipartite
extension with the same matching accounting. The edge-arrival construction
uses private edges. [Lu](https://arxiv.org/abs/2608.09210)
[Tang and Zhang](https://arxiv.org/abs/2608.04994)

Start the isolated root at zero. Assume for contradiction that every
finite family of core prefixes admits a strategy with $L(C)\le0$ for
every prefix and cover in the family. Split the covers into two classes according to whether they
select the root. We allow a different upper bound on surplus in each class.
For real $p\ge0$, define $F(p)$
as the infimum of the values $q$ for which a **single causal strategy on all core histories**
can maintain both promises

$$
L(C)\le p\quad(\text{root outside }C),\qquad
L(C)\le q-\beta\quad(\text{root inside }C).                 \tag{1}
$$

The strategy space uses countably many coordinates in $[0,1]$, one vector
per public history. Feasibility, monotonicity and the promises at a given
prefix are closed finite-coordinate conditions. Compactness, equivalently
diagonal subsequence extraction, gives one strategy for all histories.
Thus $F(0)\le\beta$. The root-only inside test gives $F\ge0$.
The infimum is attained by compactness. The set of attainable pairs $(p,q)$ is the epigraph of $F$. It is
closed by compactness of the strategy space and convex by coordinatewise
mixing of strategies.
Consequently $0\le F\le\beta$, $F$ is nonincreasing and convex, and
it is continuous on $[0,\infty)$, including at zero by closedness and
monotonicity. No scalar state assumption has been made about the algorithm.

## 2. Interleaving two finite tests

A *local test* is a pair consisting of a finite rooted input and a terminal
cover of that input. Only the sequence of core arrivals is public. The
terminal cover is a hidden label. A finite distribution of tests is a tree
of public prefixes, with termination and its hidden label as possible final
outcomes. Several outcomes may have the same last public prefix. An interleaving merges two such input sequences while preserving the order
within each one. Both roots and their connecting edge are already present. A local arrival in the lemma
is a subsequent arrival in that component.

**Interleaving lemma.** Take two distributions, each with finite support and rational probabilities, on tests in
disjoint rooted components $A,B$. Write
$\alpha=\Pr(A\text{'s root outside})$ and
$\delta=\Pr(B\text{'s root inside})$. If $\alpha\le\delta$, there
is a distribution of interleaved tests with these properties.

1. Both local marginals are preserved, including their entire input and
   hidden cover. The two selected covers jointly cover the connecting
   root edge on every outcome of positive probability.
2. At **each local arrival** in either component, conditional on its local
   public prefix, the joint public past available for that decision gives
   no further information about the rest of that component's test. This
   includes its hidden cover.

**Construction.** In the first local prefix tree mark each node by the
conditional probability that its terminal cover excludes its root. In the
second tree use the probability that its cover includes its root. Terminal
labels are marked zero or one. Each mark is the probability-weighted mean
of its children's marks. Implement a multiway transition by a finite binary
tree of choices, marking each internal split with its corresponding weighted
mean. Only the resulting next public arrival is revealed. Zero-probability
outcomes can be dropped. Choose a common denominator $M$ for all marks.

Place two particles at $M\alpha,M\delta$ in $\{0,\ldots,M\}$.
They use the **same sequence** of independent fair signs. At each tick add
the sign to each interior particle and leave an absorbed particle fixed.
For a local binary choice with distinct child marks, wait until its particle
first hits either scaled child mark on this lattice and take that branch.
From $m$ between child positions $l<u$, the probability of hitting $u$
first is $(m-l)/(u-l)$. This equals the prescribed mass of the upper
child since the parent mark is the mean of the two child marks.
For equal child marks use a fresh independent coin with the prescribed
probability and advance no ticks. Continue this procedure through local
arrivals and the final hidden label. Once absorbed, all remaining choices
in that local tree have equal marks and use the coin rule.

Merge the local arrivals by tick, keeping local order. Break ties by a
fixed component priority. Reveal only actual arriving pools and their
parents. Hidden transitions and termination labels are not announcements.
The particles remain ordered at every tick, including when one is absorbed.
Every required hit occurs almost surely and there are only finitely many
local transitions. At termination the two binary marks are ordered. Thus
if $A$'s root is outside, $B$'s root is inside. The unbounded number
of possible *private walk ticks* causes no long public input. There are
only finitely many local paths and shuffles.

Fix a local public prefix $v$ in component $A$. Write $T_A$ for its full
test and $v\preceq T_A$ for the event that the test reaches $v$. On this
event let $H_v$ be the joint public history up to and including the
arrival at $v$. For every possible $H$ ending there and every full local
test $\tau$, we claim
$$
  \Pr(T_A=\tau\mid H_v=H)=\Pr(T_A=\tau\mid v\preceq T_A).
$$

Fix the other component's independent coins. On reaching $v$, record
the finite word of signs used and the outcomes of the own equal-mark
choices made through that arrival. End the record before the next own
choice, even if it will use the same tick. For any particular record,
the event of reaching $v$ with that record depends only on the signs
and own choices it contains. The unused signs and fresh own coins
therefore have their original law. The sampler resumes at the node for
$v$, at that node's mark, so the remaining test has precisely the
standalone law at $v$.

Given the other coins, this record also determines $H_v$. If the record
uses $m$ signs, it determines all other arrivals before tick $m$.
Fixed component priority specifies whether the other arrivals at tick
$m$ precede this decision. Those arrivals use only the first $m$ signs
and the other coins. The conditional law is the same for each such record, so averaging over
records and other coins consistent with $H$ proves the claim. The same argument applies on $B$.

## 3. Why the budgets must separate

Fix $p\ge0$ and a strategy attaining (1) at $q=F(p)$. Offer a first
child of rational weight $h>0$. Fix the resulting root coordinates
$r,z$, with $r+z\ge1$. There are now two rooted components if their
connecting edge is set aside. Each can undergo every rational rooted-tree
continuation, in any interleaving. Scale the child's subsequent weights by
$h$. Its local surplus will be expressed in units of $h$. Arrival
indices in each local test can be translated canonically to global indices.

We claim there exist **two independent local strategies**, starting at
$r,z$, that meet the global promises against *every compatible pair*
of local tests. This is a consequence of the interleaving lemma, even
though the original strategy sees both histories.

For each side, a local strategy assigns a response to each of its own
prefixes. Independence here means that each assignment uses only that
side's history. If there were no such pair, compactness of the product
of the two strategy spaces would give a finite list of test pairs whose
inequalities no pair of local strategies satisfies. For each test pair the
local surpluses $L_A,L_B$ are computed with each component's root
normalized to weight one. Thus the required inequality is that
$L_A+hL_B$ be at most $p$ or $q-\beta$, according
to $A$'s root status. Compatibility here means the two roots are not
both outside. The product of local strategy polytopes on these finite
prefix trees is compact and convex, and each performance inequality is
affine. Write $e_i(x)$ for the excess above the threshold on test
pair $i$, where $x$ ranges over that product polytope. Then
$\min_x\max_i e_i(x)>0$, since the minimum is attained. By finite
minimax there are weights $\lambda_i\ge0$ summing to one for which
$\min_x\sum_i\lambda_i e_i(x)>0$. Approximation within the probability
simplex preserves this strict inequality because the finitely many
$e_i$ are bounded. We may therefore take rational weights supported on
the same compatible test pairs.

Keep only the two local marginals of this distribution. Their ordered
root probabilities allow the interleaving construction in Section 2.
The expected threshold depends only on $A$'s marginal root status.
The expected performance of independent strategies likewise depends only
on the two marginals.

To apply separation to the joint strategy, simulate it internally from
the fixed coordinates $r,z$. At each subsequent arrival copy its
newborn coordinate $y$. Replace each older neighbor's current value
$x$ by $\max(x,1-y)$, and keep every other old value. The simulated
neighbor value is at least $x$ by induction and at least $1-y$ by
feasibility. Thus each coordinate stays at most its simulated value,
and all old and new edges are covered. This strategy meets the original
promises and changes each component only at its own arrivals.

Let $Y_v$ be its vector on $A$ just after local arrival $v$. This
vector is a function of $H_v$. Define the local strategy by
$\bar y_v=\mathbb E[Y_v\mid v\preceq T_A]$. The lemma gives
$$
  \mathbb E[Y_v\mid T_A=\tau]=\bar y_v\qquad(v\preceq\tau)
$$
for every full test of positive mass, including its hidden cover.
For a child prefix $v'$ of $v$, average this equality over the tests
reaching $v'$. On coordinates already present at $v$ this gives
$$
  \bar y_v=\mathbb E[Y_v\mid v'\preceq T_A]
  \ \le\ \mathbb E[Y_{v'}\mid v'\preceq T_A]=\bar y_{v'}.
$$
The local edge inequalities hold by linearity. Start at $r$ and set all
coordinates to one on prefixes outside the sampled tree. Do the same
on $B$, starting at $z$.

Given a full local test, the final local vector equals the vector at its
last local arrival, or the fixed initial vector if there was none. Thus
the expected surplus conditional on this test equals the surplus of
its local mean strategy. Summing over the two marginals, the joint
strategy has the same expected excess as this pair of local strategies.
Separation makes that excess strictly positive, contradicting the
promises on every interleaving.

For the independent strategies let $s,t$ be the suprema of their
outside-root surpluses. Pairing each with the other root's root-only
inside test gives $s\le p+h\beta$ and $ht\le q$, so both are finite. They are at least $r,z$ by the root-only outside
tests. A local strategy starting at a positive coordinate can be simulated
from zero by postponing that initial purchase until the first local move.
This can only improve its root-only outside test. Its supremal inside
surplus is consequently at least $F(s)-\beta$ or $F(t)-\beta$,
respectively. In independent strategies the two inputs can be chosen
separately for any compatible pair of root statuses. Taking suprema in
the outside/inside and inside/outside inequalities shows that for every
$p\ge0$ and rational $h>0$ there exist $s,t\ge0$ satisfying

$$
 s+h(F(t)-\beta)\le p,\qquad F(s)+ht\le F(p),\qquad s+t\ge1.  \tag{2}
$$

The initial promises $p$ need not be reachable from a particular play.
Their frontier was defined using the very same rooted input family;
the actual isolated-state consequence is $F(0)\le\beta$.

### A fork that can be checked directly

For a small example, take two adjacent pools of weight one and allow
one further child of weight $h=1/2$ on each endpoint, in either order.
Allow a private-leaf completion after any core prefix. The smallest feasible
$\beta$ in this example is $3/5$, so its optimal ratio is $8/5$. Label the
endpoints $U,V$ so that $V$'s initial coordinate is at least $1/2$.
Attach the first child to $U$, and let $r$ be $U$'s coordinate
then. The cover consisting of $U$ requires $1/2+h(1-r)\le\beta$.
Attach the second child to $V$ and write $s$ for $V$'s coordinate.
The two covers that exclude one endpoint require

$$
r+h(1-s)\le\beta(1+h),\qquad s+h(1-r)\le\beta(1+h).
$$

At $h=1/2$, weight the one-child inequality by $3$ and the two
displayed inequalities by $2$ and $1$, respectively. The coefficients
of $r,s$ cancel, giving $9/2\le(15/2)\beta$, hence $\beta\ge3/5$.
Conversely keep the isolated root at zero until the connecting edge
arrives, then set both endpoints to $1/2$. If a child arrives, raise
its parent to $4/5$ and give the child $1/5$. At $\beta=3/5$ the
outside surplus at an endpoint with a child is
$4/5-(3/5)(1/2)=1/2$. Its inside surplus is at most
$(1/2)(1/5)-3/5=-1/2$. Without a child the corresponding bounds
are $1/2$ and $-3/5$. Every compatible pair therefore has nonpositive
total surplus. On completion give each private leaf the complement of
its neighbor's current value. Each matched pair now costs exactly one,
so the completed cost is at most $(1+\beta)w(C)$. In the blowup by two,
a core arrival sees both twins of its parent, whereas a private leaf
sees a single vertex. Thus the completion rule can be implemented from
the revealed edges alone.

## 4. Recovering the exact constant

Put $D=\beta-F$. It is nonnegative, concave, and bounded by $\beta$.
For a differentiability point $0<p<1$, convexity and (2) give

$$
 t\le -F'(p)D(t),\qquad t\ge1-p-h\beta .
$$

Indeed $ht\le-F'(p)(s-p)$ by the supporting-line inequality, and
$s-p\le hD(t)$ with $-F'(p)\ge0$. For $\eta>0$ write
$g_\eta(v)=v/(D(v)+\eta)$. Concavity and $D(0)\ge0$ give
$D(x)+\eta>(x/y)(D(y)+\eta)$ for $0\le x<y$, so $g_\eta$ is strictly
increasing. For every sufficiently small rational $h>0$,
$$
  -F'(p)\ \ge\ g_\eta(t)\ \ge\ g_\eta(1-p-h\beta).
$$
The right side converges as $h\downarrow0$, regardless of the choice of
$t$ for each $h$. Hence
$$
  -F'(p)\ \ge\ \frac{1-p}{\beta+\eta-F(1-p)} .
$$

Define $f_\eta(u)=\beta+\eta-F(1-u)>0$ on the closed unit interval.
Integrate from $p$ to 1, using local absolute continuity of convex
functions, $F(1)\ge0$, and continuity to extend to $p=0$. Then

$$
 f_\eta(1-p)+\int_p^1\frac{1-u}{f_\eta(u)}\,du\ \le\ \beta+\eta
 \qquad(0\le p\le1).                                      \tag{3}
$$

The function $f_\eta$ is continuous and strictly positive on $[0,1]$.
We show that every continuous function $f:[0,1]\to(0,\infty)$ satisfying
$$
  f(1-p)+\int_p^1\frac{1-u}{f(u)}\,du\ \le\ \gamma \qquad(0\le p\le1)
$$
must satisfy $\gamma\ge B^*-1$, following Wang and Wong's equalization argument (Section 4.1).

First, equalize the inequality to an exact identity. Set $r_1(p)=f(1-p)$ and
$$
  R_1(p)=r_1(p)+\int_{1-p}^1\frac{1-x}{r_1(x)}\,dx\ \le\ \gamma .
$$
Define two sequences of functions recursively by
$$
  r_{i+1}\ =\ r_i+\gamma-R_i,\qquad
  R_{i+1}(p)\ =\ r_{i+1}(p)+\int_{1-p}^1\frac{1-x}{r_{i+1}(x)}\,dx .
$$
Since $R_1\le\gamma$, we have $r_1\le r_2$. If $r_i\le r_{i+1}$ and $R_i\le\gamma$ hold for some $i$, then
$$
  R_{i+1}(p)
  \ \le\ r_{i+1}(p)+\int_{1-p}^1\frac{1-x}{r_i(x)}\,dx
  \ =\ r_{i+1}(p)+R_i(p)-r_i(p)
  \ =\ \gamma .
$$
By induction the sequence $\{r_i\}$ is pointwise nondecreasing and bounded above by $\gamma$. Its pointwise limit $r_\infty=\lim_{i\to\infty} r_i$ is continuous and satisfies $R_\infty\equiv\gamma$. By the dominated convergence theorem,
$$
  r_\infty(p)+\int_{1-p}^1\frac{1-x}{r_\infty(x)}\,dx\ =\ \gamma \qquad(0\le p\le1).
$$
Setting $u=1-p$, this is $r_\infty(1-u)+\int_u^1\frac{1-x}{r_\infty(x)}\,dx=\gamma$. Since the integral is differentiable in $u$, $r_\infty$ is differentiable on $[0,1]$ and satisfies $-r_\infty'(1-u)-\frac{1-u}{r_\infty(u)}=0$, or equivalently
$$
  r_\infty(u)\,r_\infty'(1-u)\ =\ u-1 .
$$

Next, solve this differential equation. Replacing $u$ by $1-u$ yields $r_\infty(1-u)\,r_\infty'(u)=-u$.
Differentiating the product $r_\infty(u)r_\infty(1-u)$ gives
$$
  \frac{d}{du}\bigl[r_\infty(u)\,r_\infty(1-u)\bigr]
  \ =\ r_\infty'(u)\,r_\infty(1-u) - r_\infty(u)\,r_\infty'(1-u)
  \ =\ -u - (u-1)
  \ =\ 1-2u .
$$
Integrating from $0$ gives $r_\infty(u)\,r_\infty(1-u)=u-u^2+c$ for the constant $c=r_\infty(0)r_\infty(1)\ge0$.
Write $k=\sqrt{1+4c}\ge1$, $a=(k+1)/2$, and $b=(k-1)/2$, so $a+b=k$, $a-b=1$, and $u-u^2+c=(a-u)(u+b)$.
Dividing $r_\infty'(u)r_\infty(1-u)=-u$ by $r_\infty(u)r_\infty(1-u)=(a-u)(u+b)$ gives the separable equation
$$
  \frac{r_\infty'(u)}{r_\infty(u)}
  \ =\ \frac{-u}{(a-u)(u+b)}
  \ =\ -\frac{a}{k(a-u)} + \frac{b}{k(u+b)} .
$$
Integrating with the boundary condition $r_\infty(0)r_\infty(1)=ab$ yields the unique solution
$$
  r_\infty(u)\ =\ (a-u)^{a/k}(u+b)^{b/k} .
$$
Evaluating the identity $r_\infty(1-u)+\int_u^1\frac{1-x}{r_\infty(x)}\,dx=\gamma$ at $u=1$ gives
$$
  \gamma\ =\ r_\infty(0)\ =\ a^{a/k}b^{b/k}\ =:\ G(k) .
$$

Finally, minimize $G(k)$ over $k\ge1$. Since $\log G(k)=\frac{a}{k}\log a+\frac{b}{k}\log b$, differentiating with respect to $k$ with $a'=\frac12$ and $b'=\frac12$ gives
$$
  \frac{d}{dk}\log G(k)
   = \frac{k-\frac12\log((k+1)/(k-1))}{k^2}.
$$
The numerator increases strictly from $-\infty$ (as $k\downarrow1$) to $+\infty$ (as $k\to\infty$) and vanishes uniquely at $k=\coth k$. The unique minimum of $G(k)$ on $[1,\infty)$ is therefore achieved at this root, giving $G(k)=B^*-1$ (and strictly beating $G(1)=1$).
Consequently, (3) implies $B^*-1\le\gamma\le\beta+\eta$ for every $\eta>0$. Taking $\eta\downarrow0$ gives $B^*-1\le\beta$, contradicting $\beta<B^*-1$. [Wang and Wong](https://arxiv.org/abs/1305.1694)

## 5. Constructing a finite ordinary input

For a requested $\epsilon$, choose a rational
$\max(0,B^*-1-\epsilon)<\beta<B^*-1$. The following terminating search
specifies finite adversarial families even when a manageable size bound
is unavailable.

1. For $n=1,2,\ldots$, take all core histories with at most $n$ pools,
   root weight one, nonroot weights $a/b$ with $1\le a,b\le n$, and
   every single-parent choice. Prefixes are shared across all continuations.
2. Test rational linear feasibility with one vector $y\in[0,1]^k$ per
   public prefix of $k$ pools. Impose monotonicity from its parent
   prefix, each new edge inequality, zero at the isolated root, and
   $L(C)\le0$ for every integral pool cover at that prefix. Exact rational
   linear programming or Fourier–Motzkin elimination decides each stage.
   Stop at the first infeasible stage. If every stage were feasible,
   compactness would give the strategy ruled out by Sections 1–4. The
   weights used in the scaled child subgames are rational and thus all
   occur in this exhaustion.
3. Let $d=\operatorname{lcm}(1,\ldots,n)$, the least common multiple
   of the integers from $1$ to $n$. Every allowed denominator $b$ divides
   $d$, so $d w_P$ is a positive integer for every pool $P$ in this stage.
   For instance, stage $n=3$ uses $d=6$ and represents weights $1$ and
   $2/3$ by six and four twins. Replace each pool $P$ by $d w_P$
   consecutive vertex arrivals, each joined to all vertices of the
   previously arrived parent pool. Present the root vertices first as
   isolated vertices. Multiplying costs by the same $d$ preserves the
   ratio.
   If the horizon is announced, fix it now at the maximum length of all
   completed inputs of this stage, and pad shorter ones at the end with
   isolated vertices. On each fixed expanded prefix take expectations
   over the algorithm's bits and average over the twins of each pool.
   Averaging the edge inequalities over all pairs of twins across a
   parent-child edge gives the pool inequality. Use the same seed on a
   prefix and its extensions to obtain monotonicity of these means.
   Set the vector at the root-only prefix to zero and keep the actual
   means at every later prefix. This preserves feasibility and
   monotonicity even for algorithms that buy at an isolated root.
4. Infeasibility supplies a prefix and cover $C$ with strictly positive
   surplus on this evaluation. Finish that prefix with the private matching
   from Section 1. Both root-only tests have nonpositive surplus, so
   the prefix contains an edge and $w(C)>0$. At this prefix the vector
   equals the algorithm's actual mean. Fix the prefix and its completion
   before sampling the algorithm's seed. As in Section 1, the private
   matching and monotonicity outside $C$ give
$$
  \mathbb E[\mathrm{ALG}]\ \ge\ d\left(w(C)+\sum_{v\notin C}w_v y_v\right)
    \ >\ (1+\beta)d w(C)\ >\ (B^*-\epsilon)\mathrm{OPT}_f.
$$

All core and terminal edges are revealed with a new endpoint. The continuum
limit in Section 4 tests rational offers of arbitrarily small size under
the contrary hypothesis. The output graph itself uses no limiting weights
or rounded player responses. The finite search is an existence construction
and has no practical near-target runtime guarantee.

[The input generator](../scripts/tree_witness.py) also implements the
algorithm-dependent version. Given a callable `marginals(core_prefix)`,
`find_witness(beta, marginals)` evaluates the actual oracle on each scaled
family, checks the cover budgets, and returns the completed unweighted
arrival list, an offline cover, its optimum and the guaranteed ratio.
This permits skipping the LP search for a family hard for every strategy.
Given exact comparisons of marginal surpluses and a subcritical target,
the search succeeds no later than the first infeasible stage.

## 6. A concrete finite certificate at $1.9005$

The [saved certificate](../experiments/fork-1801-2000.npz) describes a
particular finite family without enumerating all its interleavings. The
following recursion explains how to expand it and why it is a lower
certificate. It also checks the direction of the inequalities in (2)
without numerical differentiation or evaluating the Wang–Wong function.

A record with rational $a,b\ge0$ denotes a finite rooted test family
on which the promises (1) require $q+bp\ge a$. A root-only record with
intercept zero is valid for every nonnegative slope. If a strategy starts
the root with a positive coordinate, the same lower bound holds by
simulation from zero. At a fork, join two records with lines
$a_j-b_j s$ on the parent side and $a_i-b_i t$ on the child side.
Offer the child of weight $h$, then allow all order-preserving shuffles
of their core arrivals. A local stop leaves that component idle. Take
private completions only after the global core stops, using a compatible
pair of terminal covers. Include root-only stops in each component. Section 3's **finite**
separation argument applies directly to these two finite test
families at any feasible $(p,q)$ because it uses only the global promises on
their shuffles. For the resulting local strategies, let $s,t$ be their
maximum outside surpluses. The parent record bounds its maximum inside
surplus below by $a_j-b_j s-\beta$, and the child record bounds its own
by $a_i-b_i t-\beta$. The root-only outside tests give $s+t\ge1$.
Taking maxima for the two mixed root choices gives

$$
p\ge s+h(a_i-\beta-b_i t),\qquad q\ge a_j-b_j s+ht .
$$

For a desired $b>b_j$ with $b b_i<1$, choose
$h=(b-b_j)/(1-b b_i)>0$. Multiply the first inequality by $b$ and
add the second. The coefficients of $s,t$ are now both $b-b_j$.
Hence the following line is valid for the forked family:

$$
q+b p\ \ge\ a_j+(b-b_j)-bh(\beta-a_i).                    \tag{4}
$$

Rounding the right side down preserves validity. An alternative operation
increases the slope of any old line at unchanged intercept using $p\ge0$.
This uses the same family.

### The discrete integer recurrence

To implement (4) without floating-point error, choose a mesh
$M=4000$, a common integer scale $S=4\cdot10^{12}$, and the excess ratio
$\beta=1801/2000$ (corresponding to $1+\beta=1.9005$). The root budget in
units of $S$ is the integer $B = S\beta = 3{,}602{,}000{,}000{,}000$.

Discretize slopes as $b = \ell/M$ for integers $0\le\ell\le L$, where
$L=\lfloor 5M/4\rfloor=5000$. Subtree intercepts are represented by integer
numerators $A^{(k)}[\ell]$ such that the intercept is $A^{(k)}[\ell]/S$.
Candidate child slopes are indexed by $i\in\{0,\ldots,L\}$ on a subgrid with
step $\lfloor M/150\rfloor=26$.

The recurrence proceeds in sweeps $k=0,1,2,\ldots$:
1. **Base sweep ($k=0$):** Root-only records have intercept zero:
   $A^{(0)}[\ell]=0$ for all $0\le\ell\le L$.
2. **Sweep update ($k\ge1$):** Set $A^{(k)}[0]=0$. For each slope index
   $\ell=1,2,\ldots,L$:
   The parent slope index is $j=\ell-1$, with slope $b_j=(\ell-1)/M$ and
   intercept numerator $A^{(k)}[\ell-1]$.
   For each candidate child slope index $i$ from sweep $k-1$ such that
   $M^2-\ell i>0$, setting $h=M/(M^2-\ell i)$ in (4) yields the
   integer intercept gain
   $$
     \Delta(\ell,i)\ =\ \left\lfloor
       \frac{S(M^2-\ell i) - M\ell\bigl(B - A^{(k-1)}[i]\bigr)}{M(M^2-\ell i)}
     \right\rfloor .
   $$
   Let $\Delta^*(\ell)=\max_i \Delta(\ell,i)$. If $\Delta^*(\ell)>0$, we choose the
   maximizing child index $i^*(\ell)=\arg\max_i \Delta(\ell,i)$ and advance the
   intercept:
   $$
     A^{(k)}[\ell]\ =\ A^{(k)}[\ell-1] + \Delta^*(\ell).
   $$
   If $\Delta^*(\ell)\le0$, no child improves the bound; we set $i^*(\ell)=-1$
   (pure slope increase at unchanged intercept) and $A^{(k)}[\ell]=A^{(k)}[\ell-1]$.

These instructions are completely deterministic and acyclic. They specify
relative pool weights $h$, allowed interleavings, and the finite trees in
compressed form. Subtree weights are multiplied by $h$ at each fork and can all
be cleared to a common integer denominator on expansion.

At sweep $k=126$ and slope index $\ell=4105$ (slope $4105/4000=1.02625$), the
accumulated intercept numerator reaches
$$
  A^{(126)}[4105]\ =\ 3{,}602{,}076{,}706{,}847\ >\ B\ =\ 3{,}602{,}000{,}000{,}000 .
$$
Since $q+b p\ge A^{(126)}[4105]/S > \beta$, the point $p=0,q=\beta$ is strictly
infeasible on this finite family. The verifier in `scripts/fork_certificate.py` recomputes
the integer inequalities from the recorded child choices using Python
arbitrary-precision integers. The certificate checks the finite claim
conditional on the interleaving lemma. Sections 1–5 prove the limit
independently of this example.

Run `python scripts/fork_certificate.py --check experiments/fork-1801-2000.npz`
to replay it, or `python scripts/fork_certificate.py` to regenerate it.
`python scripts/interleaving_check.py` separately checks a finite ordered
walk with exact fractions, including coincident arrival ticks and an
equal-mark split. A second fixture includes a hidden stop at the root, private splits,
and distinct terminal labels with the same root status. It checks both
tie priorities. In each case the verifier checks the full local test law
at every decision prefix and zero mass on incompatible terminal labels. These finite checks supplement the proof of the general lemma.
