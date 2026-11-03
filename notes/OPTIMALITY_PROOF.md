# Optimal fractional vertex cover under vertex arrivals

Research proof, revised November 2, 2026. Write $B^*=1.9007616968738465\ldots$
for Wang and Wong's upper bound. The new ingredient below is an interleaving
lemma for two rooted subproblems with a single connecting edge.

**Theorem.** For every $\epsilon>0$ and every randomized online fractional
vertex-cover algorithm there is a finite, unweighted bipartite vertex-arrival
input, independent of the algorithm's realized random bits, with $\mathrm{OPT}_f>0$ and
$\mathbb E[\mathrm{ALG}]> (B^*-\epsilon)\mathrm{OPT}_f$.
The core inputs are blowups of rooted trees. Each new pool is adjacent
to just one old pool, and old pools can receive arbitrarily many children.
Together with the upper bound this gives the optimal ratio, also for the
general-graph fractional problem. [Wang and Wong](https://arxiv.org/abs/1305.1694)

Explicitly, let $k>1$ solve $k=\coth k$, put
$a=(k+1)/2,\ b=(k-1)/2$, and write $B^*=1+a^{a/k}b^{b/k}$.
The proof keeps track of the worst cost separately according to whether
the offline cover includes the root. After a child arrives there are
three compatible pairs of root choices. A full-history strategy might
try to spend less by observing which of the two branches grows first.
Sections 2–3 show that the adversary can order the two tests so this
information has no value at either branch's decisions. Section 4 converts those conditional costs into a feasible function for
Wang and Wong's minimax problem.

## 1. A countable game and its conditional costs

Normalize the root pool to weight one. A core move adds an independent pool
of announced positive rational weight joined completely to its named parent.
There are no other new edges. Number pools in local arrival order and use
the opposite color of the parent. Allow every finite such history, including
a stop just after the root. An online response gives monotone coordinates
in $[0,1]$ satisfying each edge inequality. A pool represents an average
over twins. Section 5 removes the batch and rational-weight conventions.

Fix a rational $0<\beta<B^*-1$. For any integral cover $C$ of a core
prefix, put

$$
L(C)=\sum_{v\notin C}w_v y_v-\beta\sum_{v\in C}w_v .
$$

To see how a positive surplus forces a violation, use a common integer
scale for all pool weights in this prefix. Attach a
private leaf to each individual vertex represented by $C$. The completed
graph has an offline cover $C$ and a disjoint private matching of the same
cardinality. Each private matching edge costs at least one unit, and
monotonicity preserves the weight outside $C$. In units of the common
scale the cost is at least $w(C)+\sum_{v\notin C}w_v y_v$, while
$\mathrm{OPT}_f=w(C)=\sum_{v\in C}w_v$. Lu uses a complete-bipartite
extension with the same matching accounting. The edge-arrival construction
uses private edges. [Lu](https://arxiv.org/abs/2608.09210)
[Tang and Zhang](https://arxiv.org/abs/2608.04994)

Start the isolated root at zero. Assume for contradiction that every
finite family of core prefixes admits a strategy with $L(C)\le0$ for
every prefix and cover in the family. For real $p\ge0$, define $F(p)$
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
outcomes. Several outcomes may have the same last public prefix. Both roots
and their connecting edge are already present. A local arrival in the lemma
is a subsequent arrival in that component.

**Interleaving lemma.** Take two finite rational distributions of tests on
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
inequality is that $L_A+hL_B$ be at most $p$ or $q-\beta$, according
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

As a check on the three masks, take two adjacent unit pools and allow
one further child of weight $h=1/2$ on each endpoint, in either order.
The exact excess ratio with terminal completions is $3/5$. Label the
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

The function $f_\eta$ is continuous, positive, and
$(1-u)/f_\eta(u)=g_\eta(1-u)$ is decreasing. Wang and Wong (Section 4.1, Eq. (1)) minimize the
supremum of the left side of (3) plus one over this class. Their
equalization argument and solution of the differential equation
reduce the optimum excess to minimizing $G(k)=a^{a/k}b^{b/k}$ with
$a=(k+1)/2$, $b=(k-1)/2$. For $k>1$,
$$
  \frac{d}{dk}\log G(k)
   = \frac{k-\frac12\log((k+1)/(k-1))}{k^2}.
$$
The numerator increases from $-\infty$ to $+\infty$ and vanishes at
$k=\coth k$. This gives the minimum, including comparison with the
endpoint limit $G(1)=1$. Thus (3) forces $B^*-1\le\beta+\eta$ for
every $\eta>0$, contradicting $\beta<B^*-1$. [Wang and Wong](https://arxiv.org/abs/1305.1694)

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
3. Multiply all weights in this stage by $\mathrm{lcm}(1,\ldots,n)$.
   Replace each pool by that many independent twin vertices, presented
   consecutively, with all edges to the already present parent pool.
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
   before sampling the algorithm's seed. In integer units the private
   matching and monotonicity outside $C$ give
$$
  \mathbb E[\mathrm{ALG}]\ \ge\ w(C)+\sum_{v\notin C}w_v y_v
    \ >\ (1+\beta)w(C)\ >\ (B^*-\epsilon)\mathrm{OPT}_f.
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

Take $M=4000,\ S=4\cdot10^{12},\ \beta=1801/2000$. Slopes are
$\ell/M$ and intercepts are integer multiples of $1/S$. Row zero
uses only root-only records. Record $(k,\ell)$ uses parent $(k,\ell-1)$.
A stored child index $i\ge0$ uses child $(k-1,i)$ and
$h=M/(M^2-\ell i)$ in (4). A value of $-1$ just increases the slope.
Column zero is always the trivial line. These instructions are acyclic.
They specify actual relative pool weights, allowed interleavings, and the
arrival graphs for the witness in compressed form. Subtree weights are
multiplied by the child's weight at each use and can all be given a common
integer denominator on expansion.

At record $(126,4105)$ the verified intercept numerator is
$3{,}602{,}076{,}706{,}847$, strictly above
$S\beta=3{,}602{,}000{,}000{,}000$. Thus $p=0,q=\beta$ is impossible
on that single family. The verifier recomputes the integer inequalities
from the recorded child choices using Python arbitrary-precision integers.
The certificate checks the finite claim conditional on the interleaving
lemma. Sections 1–5 prove the limit independently of this example.

Run `python scripts/fork_certificate.py --check experiments/fork-1801-2000.npz`
to replay it, or `python scripts/fork_certificate.py` to regenerate it.
`python scripts/interleaving_check.py` separately checks a finite ordered
walk with exact fractions, including coincident arrival ticks and an
equal-mark split. A second fixture includes a hidden stop at the root, private splits,
and distinct terminal labels with the same root status. It checks both
tie priorities. In each case the verifier checks the full local test law
at every decision prefix and zero mass on incompatible terminal labels. These finite checks supplement the proof of the general lemma.
