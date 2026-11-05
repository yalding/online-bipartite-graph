# Optimal fractional vertex cover under vertex arrivals

Research proof for review, revised November 4, 2026. The lower-bound
argument is given in full below; the matching upper bound is the theorem
of Wang and Wong cited after the statement. The proof has not received
independent review.

In the **vertex-arrival model**, a new vertex reveals all its edges to
earlier vertices. An online fractional vertex-cover algorithm assigns a
number $y_v\in[0,1]$ to every vertex seen so far. It may increase these
numbers after an arrival, but never decrease them. After every arrival,
each revealed edge $uv$ must satisfy $y_u+y_v\ge1$. All vertices have
unit cost, so $\mathrm{ALG}=\sum_v y_v$ at the end of the input.
The offline optimum $\mathrm{OPT}_f$ is the minimum of the same sum over
all fractional covers of the completed graph, with full knowledge of
that graph. We use the competitive-ratio convention
$\mathbb E[\mathrm{ALG}]\le R\,\mathrm{OPT}_f$ on every finite input,
without an additive constant. The expectation is over the algorithm's
random bits.

**Theorem.** For every $\epsilon>0$ and every randomized online fractional
vertex-cover algorithm there is a finite, unweighted bipartite vertex-arrival
input, independent of the algorithm's realized random bits, with $\mathrm{OPT}_f>0$ and
$\mathbb E[\mathrm{ALG}]> (B^*-\epsilon)\mathrm{OPT}_f$.
The input may depend on the algorithm's rule, but is fixed before its
random seed is drawn. Together with Wang and Wong's upper bound, this
gives the optimal competitive ratio on bipartite graphs and on general
graphs: the lower-bound inputs are bipartite, and the upper bound holds
for general graphs. [Wang and Wong](https://arxiv.org/abs/1305.1694)

Here $B^*=1.9007616968738465\ldots$. Explicitly, let $k>1$ solve
$k=\coth k=(e^{2k}+1)/(e^{2k}-1)$, put
$a=(k+1)/2,\ b=(k-1)/2$, and write $B^*=1+a^{a/k}b^{b/k}$.

### How the proof fits together

We build the input in two stages. The first stage, called the *core*,
starts with a rooted tree and replaces each node by a *pool*: a group
of vertices with no edges between them and identical neighbors in the
core. For every parent and child in the tree, we put an edge between
every vertex of the parent's pool and every vertex of the child's pool.
These are all the core edges. For example, a parent with three vertices
and a child with two give the six edges of $K_{3,2}$. The second stage
adds individual leaves to selected vertices of the core.

The argument has five steps.

1. **Turn a cover into a test of past spending.** Private leaves force
   the online algorithm to pay for every vertex of a chosen offline
   cover, in addition to what it already spent outside that cover.
   This makes the surplus $L(C)$ in Section 1 the quantity to control.
2. **Describe all possible strategies by two budgets.** The function
   $F(p)$ records the smallest inside-root budget compatible with an
   outside-root budget $p$. It allows strategies to use their entire
   history; it does not assume they use a scalar state.
3. **Separate the two sides of a new edge.** Both endpoints can receive
   later children. Sections 2–3 show how to interleave their continuations
   so that observing the other side cannot improve a local decision.
   This gives the three inequalities (2) for $F$.
4. **Extract the constant.** Section 4 turns (2) into an integral
   inequality and solves it, proving that no proposed ratio below $B^*$
   can satisfy every test.
5. **Return to ordinary finite inputs.** Section 5 clears the rational
   pool sizes, takes the algorithm's expected responses, and chooses a
   violating input before its random seed is drawn.

Section 6 is an optional exact certificate at ratio $1.9005$. It is not
needed for the proof of the limiting constant. The main notation is:

| Symbol | Meaning |
| --- | --- |
| $\beta$ | Proposed ratio minus one: $0<\beta<B^*-1$ |
| $w_P$, $y_P$ | Relative size and mean fractional purchase of pool $P$ |
| $C$, $w(C)$ | A cover consisting of whole pools, and its total weight |
| $L(C)$ | Spending outside $C$, minus $\beta w(C)$ |
| $p$, $q$ | Bounds $L(C)\le p$ outside the root and $L(C)\le q-\beta$ inside it |
| $F(p)$ | Smallest achievable $q$ at outside budget $p$ |
| $h$, $s$, $t$ | Child weight, parent outside budget, child outside budget |

## 1. A countable game and its conditional costs

### 1.1. Pools and causal strategies

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
choices seen so far. A **causal strategy** assigns a vector of coordinates
to each such prefix, using only the information in that prefix. In
particular, two inputs with the same prefix receive the same vector
there. The adversary may stop after any move, including the root.
Since all weights are rational and every prefix is finite, the set of
public prefixes is countable.

A pool coordinate $y_P\in[0,1]$ represents the mean of the fractions
bought on its twins. Their individual fractions may differ. At the end
of a pool's arrivals, summing those fractions gives $d w_P y_P$, and
averaging the edge inequalities between adjacent pools $P,Q$ gives
$y_P+y_Q\ge1$. Thus in units of $d$ the total cost is
$\sum_P w_P y_P$. In the pool game a response maintains these edge
inequalities and may only increase old coordinates. Section 5 obtains such responses from algorithms that see ordinary vertices one at a time.

### 1.2. Why surplus measures the obstruction

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
$$
Subtracting $(1+\beta)\mathrm{OPT}_f$ shows that the excess cost is at
least $dL(C)$. Thus a strictly positive surplus supplies the desired
violation. The cover $C$ is a choice for the eventual completion; it is
not announced while the core arrives. Lu uses a complete-bipartite
extension with the same matching accounting, and the edge-arrival
construction of Tang and Zhang uses private edges.
[Lu](https://arxiv.org/abs/2608.09210)
[Tang and Zhang](https://arxiv.org/abs/2608.04994)

### 1.3. Passing from finite families to a single strategy

For now require the isolated root to start at zero. Section 5 explains
why this normalization does not restrict the algorithms covered by the
theorem. Assume for contradiction that every finite, prefix-closed
family of core histories has a causal strategy satisfying $L(C)\le0$
for every cover of every prefix in the family.

This assumption gives a single strategy satisfying all the tests at
once. To see this, enumerate the countably many histories and take
increasing finite, prefix-closed families containing them. Choose a
feasible strategy on each family and extend its assignment arbitrarily
to the remaining histories. Each coordinate belongs to $[0,1]$.
Successively extract subsequences on which the first coordinate, the
second coordinate, and so on converge, and then take a diagonal
subsequence. Every particular feasibility, monotonicity, or surplus
inequality uses only finitely many coordinates. It holds eventually
along this subsequence and is preserved in the limit. The limiting
assignment is the required causal strategy.

### 1.4. The two root budgets

We now allow different bounds according to whether the test cover
contains the root. For $p\ge0$, let $F(p)$ be the infimum of the values
$q$ for which a **single causal strategy on all core histories**, with
the isolated root at zero, satisfies

$$
L(C)\le p\quad(\text{root outside }C),\qquad
L(C)\le q-\beta\quad(\text{root inside }C).                 \tag{1}
$$

The offset $-\beta$ accounts for the root's weight when it belongs to
$C$. On the root-only input, the two covers are the empty set and the
root itself. Their surpluses are $0$ and $-\beta$, respectively.
Consequently $q\ge0$ for every feasible pair. The strategy from
Section 1.3 gives the feasible pair $(0,\beta)$, so $F(0)\le\beta$.

We will use the following properties:

- **Bounds and monotonicity:** $0\le F(p)\le\beta$ for all $p\ge0$,
  and $F$ is nonincreasing, because increasing $p$ relaxes a promise.
- **Attainment and closedness:** a convergent sequence of feasible budget
  pairs has a feasible limit, by the same diagonal argument applied to
  their strategies. In particular, the infimum defining $F(p)$ is
  attained.
- **Convexity:** coordinatewise convex combinations of two strategies
  preserve edge feasibility and monotonicity. Since surplus is affine
  in the coordinates, the same combination of their budget pairs is
  feasible. Thus $F$ is convex.
- **Continuity:** a finite convex function is continuous in the interior
  of its domain. At zero, monotonicity gives a right limit at most
  $F(0)$, and closedness of the feasible pairs gives the reverse
  inequality. Hence $F$ is continuous on $[0,\infty)$.

The variable $p$ describes a guarantee over all continuations, not the
algorithm's current coordinate or internal state. Strategies in the
definition of $F$ may still use their full histories.

## 2. Interleaving two finite tests

The difficulty is that a strategy can observe both sides of an edge.
If we simply reveal one whole continuation before the other, the first
may reveal information about which cover will be used on the second.
The lemma below couples the hidden covers while withholding that extra
information at every decision that matters.

### 2.1. What is public and what must be preserved

A *local test* is a pair consisting of a finite rooted input and a terminal
cover of that input. Only the sequence of core arrivals is public. The
terminal cover is a hidden label. A finite distribution of tests is a tree
of public prefixes, with termination and its hidden label as possible final
outcomes. Several outcomes may have the same last public prefix. An interleaving merges two such input sequences while preserving the order
within each one. Both roots and their connecting edge are already
present. A local arrival in the lemma is a subsequent arrival in that
component. Stopping a component does not announce that it has stopped;
the other component may continue to receive arrivals.

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

The probability condition is necessary for compatible covers: whenever
$A$'s root is outside its cover, $B$'s root must be inside its cover.
It is not enough just to couple these two final bits. We must also
preserve the conditional laws of the input sequences seen along the way.

### 2.2. Sampling both tests with an ordered walk

In the first local prefix tree mark each node by the
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
first is $(m-l)/(u-l)$. One elementary justification is that the hitting
probability $H(j)$ solves $H(l)=0$, $H(u)=1$, and
$H(j)=(H(j-1)+H(j+1))/2$ at each interior site. Its successive
differences are constant, giving $H(j)=(j-l)/(u-l)$. The walk reaches
a boundary almost surely: in each block of $u-l$ ticks, a run of signs
all in one direction has a fixed positive chance of forcing a hit.
The hitting probability equals the prescribed mass of the upper child
because the parent mark is the mean of the two child marks.
For equal child marks use a fresh independent coin with the prescribed
probability and advance no ticks. Continue this procedure through local
arrivals and the final hidden label. Once absorbed, all remaining choices
in that local tree have equal marks and use the coin rule.

Merge the local arrivals by tick, keeping local order. Break ties by a
fixed component priority. Reveal only actual arriving pools and their
parents. Hidden transitions and termination labels are not announcements.
The particles remain ordered: while both are interior their difference
does not change, and a particle at $0$ or $M$ cannot be crossed. Equal-mark
choices do not move either particle. Every required hit occurs almost
surely and there are only finitely many local transitions. Each local
branch has its prescribed probability, so each full local test has its
original marginal law. At termination the two binary marks are ordered. Thus
if $A$'s root is outside, $B$'s root is inside. The unbounded number
of possible *private walk ticks* causes no long public input. There are
only finitely many local paths and shuffles. In particular, this is a
distribution on finite inputs of bounded length. Walk ticks are private
sampling steps, not elapsed time or extra information shown to the algorithm.

### 2.3. Why the public past reveals no extra local information

Fix a local public prefix $v$ in component $A$. Write $T_A$ for its full
test and $v\preceq T_A$ for the event that the test reaches $v$. On this
event let $H_v$ be the joint public history up to and including the
arrival at $v$. For every possible $H$ ending there and every full local
test $\tau$, we claim
$$
  \Pr(T_A=\tau\mid H_v=H)=\Pr(T_A=\tau\mid v\preceq T_A).
$$

Here the left-hand side conditions on the entire merged past; the
right-hand side conditions only on the local prefix. We consider only
conditioning events of positive probability.

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

This proves the lemma at local arrivals. It makes no independence claim
at arbitrary times when only the other component has just changed.
The next section first ensures that a component's coordinates change
only at its own arrivals, which is why this precise form is sufficient.

## 3. Why the budgets must separate

### 3.1. The three compatible root choices

Fix $p\ge0$ and a strategy attaining (1) at $q=F(p)$. Offer a first
child of rational weight $h>0$. Fix the resulting root coordinates
$r,z$, with $r+z\ge1$. There are now two rooted components if their
connecting edge is set aside. Each can undergo every rational rooted-tree
continuation, in any interleaving. Scale the child's subsequent weights by
$h$. Its local surplus will be expressed in units of $h$. Arrival
indices in each local test can be translated canonically to global indices.

Let $L_A$ and $L_B$ denote the local surpluses, with each local root
normalized to weight one. The global surplus is $L_A+hL_B$. There are
exactly three compatible choices of terminal covers:

| Root of $A$ | Root of $B$ | Required global bound |
| --- | --- | --- |
| Outside | Inside | $L_A+hL_B\le p$ |
| Inside | Outside | $L_A+hL_B\le q-\beta$ |
| Inside | Inside | $L_A+hL_B\le q-\beta$ |

The fourth choice, both roots outside, leaves their connecting edge
uncovered. Although we will derive (2) from the first two rows, all
three rows are included in the argument below.

We claim there exist **two independent local strategies**, starting at
$r,z$, that meet the global promises against *every compatible pair*
of local tests. This is a consequence of the interleaving lemma, even
though the original strategy sees both histories.

### 3.2. If local strategies failed, a finite average would witness failure

For each side, a local strategy assigns a response to each of its own
prefixes. Independence here means that each assignment uses only that
side's history; these are deterministic assignments, not an assertion
about two random seeds. If there were no such pair, compactness of the product
of the two strategy spaces would give a finite list of test pairs whose
inequalities no pair of local strategies satisfies. Close the two
finite sets of local histories under prefixes. On these finite trees,
the pairs of feasible local strategies form a compact convex polytope
$X$: their coordinates lie in $[0,1]$, and their feasibility and
monotonicity conditions are linear. Any such assignment extends to all
histories by setting every coordinate to one as soon as a history
leaves the finite tree.

For test pair $i$, let $e_i(x)$ be $L_A+hL_B$ minus its required bound
from the table. Each $e_i$ is affine. No $x\in X$ makes every
$e_i(x)\le0$. We next show that a fixed probability distribution on
these tests defeats every $x\in X$ in expectation.

Here is a direct finite separation argument. Minimize the continuous
function $\Phi(x)=\sum_i\max(e_i(x),0)^2$ on $X$, and let $x_*$ be a
minimizer. Put $c_i=\max(e_i(x_*),0)$. Since no feasible point satisfies
all tests, $\sum_i c_i^2>0$. For any $x\in X$, the segment from $x_*$
to $x$ stays in $X$. Its one-sided derivative at the minimum is
nonnegative, so
$$
  \sum_i c_i\bigl(e_i(x)-e_i(x_*)\bigr)\ge0,
  \qquad \sum_i c_i e_i(x)\ge\sum_i c_i^2>0.
$$
Normalize by $\sum_i c_i$ to obtain probabilities $\lambda_i$ with
$\min_{x\in X}\sum_i\lambda_i e_i(x)>0$. Because the finitely many
$e_i$ are bounded on $X$, sufficiently close rational probabilities
preserve this strict positive margin. Use those rational probabilities
on the same compatible test pairs.

Keep only the two local marginals of this distribution. Every original
pair was compatible, so $\Pr(A\text{'s root outside})\le
\Pr(B\text{'s root inside})$. The interleaving lemma therefore gives
a new joint distribution with these same marginals and compatible
terminal covers.
The expected threshold depends only on $A$'s marginal root status.
The expected performance of independent strategies likewise depends only
on the two marginals.

### 3.3. Extracting local strategies from a joint strategy

We will contradict the positive expected excess just obtained. First
modify the given global strategy so that the vector on a component
does not change between that component's own arrivals.

To apply separation to the joint strategy, simulate it internally from
the fixed coordinates $r,z$. At each subsequent arrival copy its
newborn coordinate $y$. Replace each older neighbor's current value
$x$ by $\max(x,1-y)$, and keep every other old value. The simulated
neighbor value is at least $x$ by induction and at least $1-y$ by
feasibility. Thus each coordinate stays at most its simulated value,
and all old and new edges are covered. This strategy meets the original
promises: decreasing coordinates can only decrease $L(C)$ for every
cover $C$. After the first connecting edge, every new pool has its
parent in its own component, so the modified strategy changes a
component only at its own arrivals. The initial connecting edge remains
covered because the coordinates $r,z$ never decrease.

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

Thus every finite list of compatible test pairs has feasible local
strategies. The diagonal compactness argument of Section 1.3 now gives
one pair of local strategies satisfying all compatible pairs at once.

### 3.4. The inequalities forced by a new child

For the independent strategies let $s,t$ be the suprema of their
outside-root surpluses. Pairing each with the other root's root-only
inside test gives $s-h\beta\le p$ and $-\beta+ht\le q-\beta$,
so $s,t$ are finite. The root-only outside tests give $s\ge r$ and
$t\ge z$, hence $s+t\ge1$.

Let $I_A,I_B$ be the suprema of the respective inside-root surpluses.
They too are finite: pair either with the other side's root-only inside
test. A local strategy starting at a positive coordinate can be simulated
from zero by postponing that initial purchase until the first local move.
This only improves its root-only outside test and preserves all other
test values. The resulting zero-start strategy has feasible budgets
$(s,I_A+\beta)$ on $A$, and similarly $(t,I_B+\beta)$ on $B$.
By definition of $F$,
$$
  I_A\ge F(s)-\beta,\qquad I_B\ge F(t)-\beta.
$$
The two local tests may be chosen separately, as long as their root
statuses are compatible. Taking suprema in the first two rows of the
table therefore gives
$s+hI_B\le p$ and $I_A+ht\le q-\beta$. A supremum need not be
attained: choosing each local test within any positive error of its
supremum gives the same inequalities after the error tends to zero.
Substitute the lower bounds on $I_A,I_B$ and recall $q=F(p)$.
We have proved that for every
$p\ge0$ and rational $h>0$ there exist $s,t\ge0$ satisfying

$$
 s+h(F(t)-\beta)\le p,\qquad F(s)+ht\le F(p),\qquad s+t\ge1.  \tag{2}
$$

The initial promises $p$ need not be reachable from a particular play.
Their frontier was defined using the very same rooted input family;
the actual isolated-state consequence is $F(0)\le\beta$.

### 3.5. A fork that can be checked directly

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

This section uses only the properties of $F$ in Section 1 and the
inequalities (2). We first turn the effect of an arbitrarily small
child into a differential inequality. We then integrate it and solve
the resulting optimization problem explicitly.

### 4.1. From a small child to an integral inequality

Put $D=\beta-F$. It is nonnegative, concave, and bounded by $\beta$.
Fix a point $0<p<1$ where $F$ is differentiable. Such points have full
measure because $F$ is convex. For each rational $h>0$, choose $s,t$
from (2). Convexity gives the supporting-line inequality
$F(s)\ge F(p)+F'(p)(s-p)$. Combining it with (2) gives

$$
 t\le -F'(p)D(t),\qquad t\ge1-p-h\beta .
$$

Indeed,
$$
  ht\le F(p)-F(s)\le -F'(p)(s-p)
     \le -F'(p)hD(t),
$$
where the last inequality uses $s-p\le hD(t)$ and $-F'(p)\ge0$.
Also $s\le p+h\beta$, so $s+t\ge1$ gives the stated lower bound on
$t$. The choice of $t$ can depend on $h$; we do not assume it converges.

To avoid dividing by a possible zero of $D$, fix $\eta>0$ and write
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
A convex function is absolutely continuous on each closed interval
inside its domain. Integrating the last inequality from $p>0$ to $1$
therefore gives
$$
  \int_p^1\frac{1-u}{f_\eta(u)}\,du
     \le F(p)-F(1)\le F(p).
$$
Since $f_\eta(1-p)=\beta+\eta-F(p)$, adding this identity yields

$$
 f_\eta(1-p)+\int_p^1\frac{1-u}{f_\eta(u)}\,du\ \le\ \beta+\eta
 \qquad(0\le p\le1).                                      \tag{3}
$$

Continuity extends (3) to $p=0$; the integrand is bounded by $1/\eta$.
The function $f_\eta$ is continuous and strictly positive on $[0,1]$.

### 4.2. Equalizing the inequality

We show that every continuous function $f:[0,1]\to(0,\infty)$ satisfying
$$
  f(1-p)+\int_p^1\frac{1-u}{f(u)}\,du\ \le\ \gamma \qquad(0\le p\le1)
$$
must satisfy $\gamma\ge B^*-1$. We reproduce Wang and Wong's
equalization argument and the ensuing calculation, so no result about
this functional inequality is needed from their paper.

Replace $p$ by $1-p$ in the displayed inequality. It becomes
$f(p)+\int_{1-p}^1(1-x)/f(x)\,dx\le\gamma$.
Thus, with $r_1=f$ (the function itself, without reflecting its argument),
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
By induction, $r_i\le r_{i+1}$ and $R_i\le\gamma$ for every $i$.
Also $r_i\le R_i\le\gamma$, so $r_i$ has a finite pointwise limit
$r_\infty$. If $m=\min_{[0,1]}f>0$, then
$m\le r_i\le\gamma$. The recurrence gives
$\gamma-R_i=r_{i+1}-r_i\to0$ pointwise. Moreover,
$0\le(1-x)/r_i(x)\le1/m$. Dominated convergence now yields
$$
  r_\infty(p)+\int_{1-p}^1\frac{1-x}{r_\infty(x)}\,dx\ =\ \gamma \qquad(0\le p\le1).
$$
This identity also proves the regularity we need. Its integral has a
bounded integrand, so it is continuous in its endpoint. Hence
$r_\infty$ is continuous. The integrand is then continuous as well,
so $r_\infty$ is continuously differentiable, with one-sided derivatives
at the endpoints. Setting $u=1-p$ and differentiating gives
$-r_\infty'(1-u)-(1-u)/r_\infty(u)=0$, or
$$
  r_\infty(u)\,r_\infty'(1-u)\ =\ u-1 .
$$

### 4.3. Solving the equality and minimizing its value

Replacing $u$ by $1-u$ in this differential equation yields
$r_\infty(1-u)\,r_\infty'(u)=-u$.
Differentiating the product $r_\infty(u)r_\infty(1-u)$ gives
$$
  \frac{d}{du}\bigl[r_\infty(u)\,r_\infty(1-u)\bigr]
  \ =\ r_\infty'(u)\,r_\infty(1-u) - r_\infty(u)\,r_\infty'(1-u)
  \ =\ -u - (u-1)
  \ =\ 1-2u .
$$
Integrating from $0$ gives
$r_\infty(u)\,r_\infty(1-u)=u-u^2+c$, where
$c=r_\infty(0)r_\infty(1)>0$. Write $k=\sqrt{1+4c}>1$,
$a=(k+1)/2$, and $b=(k-1)/2$. Then $a+b=k$, $a-b=1$,
$ab=c$, and $u-u^2+c=(a-u)(u+b)$.
Dividing $r_\infty'(u)r_\infty(1-u)=-u$ by $r_\infty(u)r_\infty(1-u)=(a-u)(u+b)$ gives the separable equation
$$
  \frac{r_\infty'(u)}{r_\infty(u)}
  \ =\ \frac{-u}{(a-u)(u+b)}
  \ =\ -\frac{a}{k(a-u)} + \frac{b}{k(u+b)} .
$$
Integration gives
$r_\infty(u)=K(a-u)^{a/k}(u+b)^{b/k}$ for a constant $K>0$.
At $u=0,1$, the product of these two expressions is $K^2ab$.
The identity $r_\infty(0)r_\infty(1)=ab>0$ forces $K=1$. Thus
$$
  r_\infty(u)\ =\ (a-u)^{a/k}(u+b)^{b/k} .
$$
Evaluating the identity $r_\infty(1-u)+\int_u^1\frac{1-x}{r_\infty(x)}\,dx=\gamma$ at $u=1$ gives
$$
  \gamma\ =\ r_\infty(0)\ =\ a^{a/k}b^{b/k}\ =:\ G(k) .
$$

Finally, minimize $G(k)$ over $k>1$. Since
$\log G(k)=(a/k)\log a+(b/k)\log b$, differentiation gives
$$
  \frac{d}{dk}\log G(k)
   = \frac{k-\frac12\log((k+1)/(k-1))}{k^2}.
$$
The numerator $N(k)=k-\tfrac12\log((k+1)/(k-1))$ has derivative
$N'(k)=1+1/(k^2-1)>0$. It tends to $-\infty$ as $k\downarrow1$
and to $+\infty$ as $k\to\infty$. Its unique zero satisfies
$e^{2k}=(k+1)/(k-1)$, equivalently $k=\coth k$. Therefore $G$
decreases up to this root and increases thereafter; its minimum is
$B^*-1$.

Apply this result to (3) with $f=f_\eta$ and $\gamma=\beta+\eta$.
For every $\eta>0$ we obtain $B^*-1\le\beta+\eta$. Letting
$\eta\downarrow0$ contradicts $\beta<B^*-1$.
This completes the contradiction to the finite-family assumption in
Section 1.3. [Wang and Wong](https://arxiv.org/abs/1305.1694)

## 5. Constructing a finite ordinary input

For a requested $\epsilon$, choose a rational
$\max(0,B^*-1-\epsilon)<\beta<B^*-1$. The following terminating search
specifies finite adversarial families even when a manageable size bound
is unavailable.

### 5.1. Find a finite family with inconsistent budgets

For $n=1,2,\ldots$, take all core histories with at most $n$ pools,
root weight one, nonroot weights $a/b$ with $1\le a,b\le n$, and
every single-parent choice. Prefixes are shared across all continuations.
Test rational linear feasibility with one vector $y\in[0,1]^k$ per
public prefix of $k$ pools. Impose monotonicity from its parent
prefix, each new edge inequality, zero at the isolated root, and
$L(C)\le0$ for every integral pool cover at that prefix. Exact rational
linear programming or Fourier–Motzkin elimination decides each stage.
Stop at the first infeasible stage. If every stage were feasible,
compactness would give the strategy ruled out by Sections 1–4. The
weights used in the scaled child subgames are rational and thus all
occur in this exhaustion.

### 5.2. Expand every pool using the same integer scale

Let $d=\operatorname{lcm}(1,\ldots,n)$, the least common multiple
of the integers from $1$ to $n$. Every allowed denominator $b$ divides
$d$, so $d w_P$ is a positive integer for every pool $P$ in this stage.
For instance, stage $n=3$ uses $d=6$ and represents weights $1$ and
$2/3$ by six and four twins. Replace each pool $P$ by $d w_P$
consecutive vertex arrivals, each joined to all vertices of the
previously arrived parent pool. Present the root vertices first as
isolated vertices. Multiplying costs by the same $d$ preserves the
ratio. Using a common $d$ for the entire family is essential:
two abstract histories with the same prefix must expand to the same
ordinary vertex prefix.

If the horizon is announced, fix it now at the maximum length of all
completed inputs of this stage, and pad shorter ones at the end with
isolated vertices. Use a fixed ordering of the twins and of the
terminal private leaves. Thus the algorithm receives the same
advance information on every input in the family.

### 5.3. A randomized algorithm induces a causal pool strategy

Fix the algorithm. At each expanded core prefix $H$, let $Y_u(H)$ be
the random fraction on ordinary vertex $u$. For a pool $P$, define
$$
  y_P(H)=\frac{1}{d w_P}\sum_{u\in P}\mathbb E[Y_u(H)].
$$
These are deterministic numbers obtained from the algorithm's law,
not observations of a realized run. Causality of the algorithm makes
them the same on common prefixes.

Averaging the edge inequalities over all pairs of twins across a
parent-child edge gives the pool inequality. Use the same seed on a
prefix and its extensions to obtain monotonicity of these means.
Set the vector at the root-only prefix to zero and keep the actual
means at every later prefix. The root-only prefix has no edges, and
all later coordinates are nonnegative. Lowering just this initial
vector to zero therefore preserves feasibility and monotonicity,
even for algorithms that buy at an isolated root.

### 5.4. Choose the completion before the random seed

The resulting assignment satisfies all constraints of the finite
linear system except, potentially, its surplus inequalities.
Infeasibility therefore supplies a prefix and cover $C$ with strictly positive
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

The graph is bipartite: color each core pool by the parity of its depth
in the tree, and color every private leaf opposite its neighbor.
All core and terminal edges are revealed with a new endpoint. The continuum
limit in Section 4 tests rational offers of arbitrarily small size under
the contrary hypothesis. The output graph itself uses no limiting weights
or rounded player responses. The finite search is an existence construction
and has no practical near-target runtime guarantee.

The script [tree_witness.py](../scripts/tree_witness.py) implements
this algorithm-dependent construction.
Given a callable `marginals(core_prefix)`,
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
on which the promises (1) require $q+bp\ge a$. The letters $a,b$ in
this section are line coefficients, unrelated to the constants in
Section 4. A root-only record with
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
step $\lfloor M/150\rfloor=26$, namely $0,26,52,\ldots,4992$.
The sweep index $k$ below is also unrelated to the real parameter $k$
used to compute $B^*$.

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
   smallest maximizing child index $i^*(\ell)$ and advance the
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
