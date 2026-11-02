# Optimal fractional vertex cover under vertex arrivals

Research proof, November 1, 2026. Write $B^*=1.9007616968738465\ldots$
for Wang and Wong's upper bound. The new ingredient below is an interleaving
lemma for two rooted subproblems with a single connecting edge.

**Theorem.** For every $\epsilon>0$ and every randomized online fractional
vertex-cover algorithm there is a finite, unweighted bipartite vertex-arrival
input, independent of the algorithm's realized random bits, on which
$\mathbb E[\mathrm{ALG}]\ge (B^*-\epsilon)\mathrm{OPT}_f$.
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
information has no value at either branch's decisions. Section 4 then
extracts Wang and Wong's function from the frontier of those conditional
costs.

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

A strict positive value gives a finite violation of $1+\beta$. Attach a
private leaf to each individual vertex represented by $C$. The completed
graph has an offline cover $C$ and a disjoint private matching of the same
cardinality. The weight outside $C$ persists. Lu uses a complete-bipartite
extension with the same matching accounting. The edge-arrival construction
uses private edges. [Lu](https://arxiv.org/abs/2608.09210)
[Tang and Zhang](https://arxiv.org/abs/2608.04994)

Start the isolated root at zero. Define $F(p)$, for real $p\ge0$, as
the least $q$ for which a **single causal strategy on all core histories**
can maintain both promises

$$
L(C)\le p\quad(\text{root outside }C),\qquad
L(C)\le q-\beta\quad(\text{root inside }C).                 \tag{1}
$$

Assume for contradiction that all finite families of core prefixes admit
a strategy with $L(C)\le0$ for every prefix and cover. The complete
strategy space uses countably many coordinates in $[0,1]$, one vector
per public history. Feasibility, monotonicity and the promises at a given
prefix are closed finite-coordinate conditions. Compactness, equivalently
diagonal subsequence extraction, gives one strategy for all histories.
Thus $F(0)\le\beta$. The root-only inside test gives $F\ge0$.
The infimum is attained by compactness. The attainable epigraph of
$(p,q)$ is closed and convex by compactness and coordinatewise mixing.
Consequently $0\le F\le\beta$, $F$ is nonincreasing and convex, and
it is continuous on $[0,\infty)$, including at zero by closedness and
monotonicity. No scalar state assumption has been made about the algorithm.

## 2. Interleaving two finite tests

A *local test* is a pair consisting of a finite rooted input and a terminal
cover of that input. Only the sequence of core arrivals is public. The
terminal cover is a hidden label. A finite distribution of tests is a tree
of public prefixes, with termination and its hidden label as possible final
outcomes. Several outcomes may have the same last public prefix.

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
first hits either child mark on this lattice and take that branch. The
gambler's ruin hitting probabilities give exactly the required two weights.
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

For the information assertion, the tick of a specified local arrival
(on the event it is reached) is a stopping time of the signs and the
coins used to reach it. At that time its particle is at exactly the mark
of its **public prefix**. Future signs and fresh own coins give the same
law for its remaining test as in standalone sampling from that prefix.
The other component's arrivals already delivered are determined by the
signs up through that tick and the other component's independent coins.
This holds for ties as well, since their order does not depend on future
signs or unused own coins. One may condition on all other-component coins
and the stopped sign history in this argument. One must not condition on
unused own coins. This proves assertion 2. At intermediate ticks, while
a local move is pending, the other branch may convey information. No
decision on the pending branch is required then.

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

If there were no such pair of strategies, compactness would give finitely
many incompatible performance inequalities. For each test pair the
inequality is that $L_A+hL_B$ be at most $p$ or $q-\beta$, according
to $A$'s root status. Compatibility here means the two roots are not
both outside. The product of local strategy polytopes on these finite
prefix trees is compact and convex, and each performance inequality is
affine. Finite minimax, or separation from the nonpositive orthant, gives
a distribution on these compatible pairs for which **every independent
strategy pair** has strictly positive expected excess above the appropriate
threshold. Its weights can be taken rational by approximating within the
strict margin, uniformly on the bounded strategy polytope.

Keep only the two local marginals of this distribution. Their ordered
root probabilities allow the interleaving construction in Section 2.
The expected threshold depends only on $A$'s marginal root status.
The expected performance of independent strategies likewise depends only
on the two marginals.

To apply this argument to the original joint strategy, first postpone
gratuitous raises. Simulate it internally, copy each newborn coordinate,
and raise only its neighbors as needed for that coordinate. Induction
shows that the resulting feasible coordinates are bounded above by the
simulated ones at every prefix. This applies after the connecting edge
with $r,z$ fixed. In particular the strategy changes coordinates in a
component only at its own arrivals. It still meets (1).

Average this joint strategy's local vector at each local public arrival
conditional on that local prefix. By the lemma the mean is unchanged if
one also conditions on any particular subsequent local input and terminal
cover of positive conditional probability. Thus means at consecutive
local prefixes obey monotonicity, and all local edge inequalities hold by
linearity. Before the first local continuation use the fixed initial
coordinate. These are feasible independent local strategies on the sampled
prefixes and can be extended off support by raising coordinates to one.
For each terminal test the expected local surplus of the joint strategy
is exactly that of its mean strategy. This remains true if the last
arrival precedes other-component moves or if there is no local arrival.
The combined expected excess must therefore be strictly positive. This
contradicts the joint strategy's promises on every interleaving.

For the independent strategies let $s,t$ be the suprema of their
outside-root surpluses. Both are finite by pairing with the other root's
root-only inside test. They are at least $r,z$ by the root-only outside
tests. A local strategy starting at a positive coordinate can be simulated
from zero by postponing that initial purchase until the first local move.
This can only improve its root-only outside test. Its supremal inside
surplus is consequently at least $F(s)-\beta$ or $F(t)-\beta$,
respectively. In independent strategies the two inputs can be chosen
separately for any compatible pair of root statuses. Taking suprema in
the outside/inside and inside/outside inequalities proves

$$
 s+h(F(t)-\beta)\le p,\qquad F(s)+ht\le F(p),\qquad s+t\ge1.  \tag{2}
$$

This holds for **every** $p\ge0$ and rational $h>0$. Artificial
initial promises $p$ need not be reachable from a particular play.
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

Eliminating $s,r$ gives $\beta\ge(1+h)/(2(1+h^2))=3/5$.
Conversely start both endpoints at $1/2$ and raise each to $4/5$
if its child arrives. Each local outside surplus is at most $1/2$,
and each inside surplus is at most $-1/2$. Every compatible pair
therefore has nonpositive sum. The upper strategy uses only local
histories, while the lower argument permits both histories to influence
every response.

## 4. Recovering the exact constant

Put $D=\beta-F$. It is nonnegative, concave, and bounded by $\beta$.
For a differentiability point $0<p<1$, convexity and (2) give

$$
 t\le -F'(p)D(t),\qquad t\ge1-p-h\beta .
$$

Indeed $F(s)\ge F(p)+F'(p)(s-p)$, and $s-p\le hD(t)$.
For any $\eta>0$, $v/(D(v)+\eta)$ is nondecreasing for $v\ge0$
by concavity and $D(0)\ge0$. Let rational $h\downarrow0$. Continuity
on the interior yields

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

The function is continuous and $(1-u)/f_\eta(u)$ is nonincreasing by
the same concavity argument. The infimum over this class of the supremum
of the left side of (3) is $B^*-1$. Letting $\eta\downarrow0$
contradicts the choice of $\beta$. This invokes Wang and Wong's
optimization theorem only after deriving its hypotheses from arbitrary
causal cover strategies. [Wang and Wong, Section 4](https://arxiv.org/abs/1305.1694)

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
   Against the given randomized algorithm evaluate expected coordinates
   on each fixed public prefix, averaging over twins at batch boundaries.
   These vectors satisfy feasibility and monotonicity. One may simulate
   it lazily with a zero initial root, obtaining vectors no larger than
   the actual ones, including if it makes gratuitous isolated purchases.
4. Infeasibility supplies a prefix and cover $C$ with strictly positive
   surplus on this evaluation. Finish that prefix with the private matching
   from Section 1. Since the lazy root-only surplus is nonpositive, the
   witness has a nonempty comparator. The selected sequence depends on the
   algorithm and its marginal behavior on fixed histories, never its realized
   seed. Its expected cost is strictly greater than $(1+\beta)w(C)$, in
   the common integer scaling. If the horizon is known, choose a common
   upper bound on the vertex counts of all these completed inputs, announce
   that horizon before evaluating the algorithm, and pad every shorter
   completion with isolated vertices.

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
It must succeed no later than the first infeasible stage when given exact
marginals and a subcritical target.

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
of their core tests. Allow stopping, and a private completion on every
cover. Include root-only stops in each component. Section 3's **finite**
separation argument gives $s,t\ge0,\ s+t\ge1$ and

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
equal-mark split. It verifies the full conditional test law at each
sampled decision prefix and that incompatible terminal labels have mass
zero. These finite checks supplement the proof of the general lemma.
