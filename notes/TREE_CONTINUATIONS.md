# Which branches must survive?

November 1, 2026. These intermediate results led to the
[optimality proof](OPTIMALITY_PROOF.md). A finite tree
contradicts the earlier tree-of-pools upper bound. There is nevertheless a
below-target strategy if only one of the parent and child can receive future
arrivals. Allowing both to survive leads to the Wang–Wong inequality under
a specific extra assumption about the strategy. Sections 2–3 of the
optimality proof subsequently justify the two budgets for arbitrary strategies.

## A tree contradicting Session 5, Theorem 2

For a trial ratio $1+\beta$, every prefix and every cover $C$ must satisfy
$\sum_{v\notin C}y_v\le\beta |C|$. Otherwise append one private leaf
to each member of $C$. These private edges form a matching of size $|C|$,
and $C$ covers the completed graph, so its fractional optimum is exactly
$|C|$. All previously accumulated weight outside $C$ persists.

Take $\beta=71/100>1/\sqrt2$. Use the following finite main path.

1. Introduce ten isolated left vertices $A$. Introduce nine right vertices
   one at a time, each adjacent to all of $A$.
2. Introduce eleven more right vertices $B$, each adjacent to all of $A$.
3. Introduce thirteen left vertices one at a time, each adjacent to all
   eleven vertices of $B$ and to nobody else.

The quotient is a rooted tree of pools. The new pool $B$ has one parent
and thirteen children. Earlier singleton children of $A$ stay in the graph.
All counts and costs below are divided by ten. Set $h=1/10$ and $w=11/10$.

After the $i$-th singleton in step 1, the cover consisting of all right
vertices caps the average on $A$ at $\beta i h$. Feasibility forces that
singleton's coordinate to be at least $1-\beta i h$. The nine singletons
therefore have persistent normalized cost at least

$$
H=h\sum_{i=1}^9(1-\beta i h)=1161/2000.
$$

At the end of step 2, the cover $A$ caps total right cost at $\beta$.
The average on $B$ is at most $(\beta-H)/w$, hence the average on $A$
is at least $l=1-(\beta-H)/w=1941/2200$. After the $j$-th new left
vertex, all left vertices form a cover of normalized size $1+jh$.
This caps total right cost at $\beta(1+jh)$. The newcomer is adjacent
to all of $B$, so its coordinate is at least $[l-\beta jh/w]_+$.
At the final prefix the cover consisting of all right vertices requires

$$
l+h\sum_{j=1}^{13}[l-\beta jh/w]_+
=31721/22000\ \le\ 2\beta=71/50.
$$

The left side exceeds the right by $481/22000$. At least one of the listed
prefixes and covers therefore violates its budget. Give that cover its
private leaves. The construction works against arbitrary asymmetric
assignments, including algorithms told the eleven-vertex batch size. For a
randomized algorithm run the argument on its expected coordinates along
the fixed main path. Select a violated prefix before running the algorithm
on the completed input. The resulting input has at most 66 unweighted
vertices and is independent of its realized random seed.

The ODE in Session 5 uses the eventual conditional surplus of a child's
subtree as the clock increment for a decision at the child's arrival. The
algorithm does not yet know that surplus. The arithmetic identity for an
already specified clock cannot give the claimed causal strategy. This
counterexample removes the earlier basis for discarding all rooted trees.

## Exact transition when one endpoint survives

Consider a game with one live pool $u$ of weight $w$ and coordinate $x$.
An arriving child has weight $hw$, with arbitrary announced $h>0$, and
is joined to the whole parent. After the response the adversary can keep
either endpoint live, retiring the other from future core arrivals. It may
stop with a private completion at any step. Ordinary stops are covered by
the same budget. The example with an initial ten-vertex pool fits this game.

For a prefix, maximize the terminal surplus
$\sum_{v\notin C}w_v y_v-\beta\sum_{v\in C}w_v$ separately for $u$
outside or inside $C$. Write the results as $w(x-p)$ and $-wq$.
All retired edges and coordinates are included in these two maxima. An
isolated initial pool at zero has $(x,p,q)=(0,0,\beta)$. Stopping is safe
exactly when $x\le p$ and $q\ge0$.

Let the child receive $z$ and raise the parent to $r=\max(x,1-z)$.
Gratuitous increases can be postponed by simulating a strategy internally
and doing just the raises required by its new coordinate. Keeping the
parent or the child gives the following exact states, normalized by the
weight of the surviving pool.

| Survivor | Coordinate | $p_{\rm new}$ | $q_{\rm new}$ |
|---|---:|---:|---:|
| Parent | $r$ | $p+\beta h$ | $q-hz$ |
| Child | $z$ | $q/h$ | $\beta+\min(p-r,q)/h$ |

For the first row, excluding the parent forces the child into the cover.
Including the parent permits the worse of the child's two statuses, namely
outside. For the second row, excluding the child forces the parent in.
Including the child permits whichever of $w(r-p)$ and $-wq$ is larger.
These arguments also retain witness covers for both rows.

## An all-horizon strategy for the one-survivor game

There is a $46/25=1.84$ strategy for every such game. Set $\beta=21/25$
and use the invariant $x\le p,\ q\ge F(p)$, where $F$ interpolates
linearly through the points below and is zero for $p\ge1$.

| $p$ | 0 | 1/4 | 1/2 | 3/4 | 1 |
|---|---:|---:|---:|---:|---:|
| $F(p)$ | 3/4 | 9/20 | 9/40 | 3/40 | 0 |

On a child of relative weight $h$, set

$$
r_0=\min\{1,\ p+h(\beta-F(q/h))\},\qquad z=1-r_0.
$$

Since $F\le\beta$, this is feasible with $r=r_0\ge x$. The single
inequality needed at the boundary $q=F(p)$ is

$$
F(p+\beta h)+h[1-p-h(\beta-F(F(p)/h))]_+\le F(p).       \tag{1}
$$

Larger $q$ can only decrease $z$. Equation (1) therefore gives
$q-hz\ge F(p+\beta h)$, implying both parent safety and $z\le q/h$.
For the child row, $p-r\ge h(F(q/h)-\beta)$ and $q\ge0$ give
$q_{\rm new}\ge F(q/h)$. Both branches preserve the invariant, even
when the adversary chooses the survivor after seeing $z$.

Here is a finite verification of (1) for **all real** $p\ge0,h>0$.
Write $F(p)=\max_i(a_i-b_i p)$ using the zero line and the four
interpolation lines. The positive-part zero branch follows from
monotonicity. For each pair of lines $i,j$, the other branch is
equivalent collectively to requiring

$$
(\beta-a_i)h^2+(b_iF(p)-1+p+\beta b_j)h+F(p)-a_j+b_jp\ \ge0. \tag{2}
$$

For fixed $h$ this is affine between successive knots. At $p\ge1$,
(1) is immediate. At each of the five knots check (2) as $Ah^2+Bh+C$
by verifying $A>0,\ C\ge0$, and either $B\ge0$ or $B^2\le4AC$.
All 125 rational
comparisons pass in the certificate script. The initial state satisfies
the invariant. At a terminal completion, raise each selected old pool to
one as its private leaves arrive, which attains the surplus being bounded.
The upper strategy uses the announced batch and terminal protocol.

## If both endpoints survive

Here is a legal extension. After an arrival, retain **both** the parent
and child, and let future children of each arrive in any interleaving.
This still builds rooted trees of pools and includes the one-survivor game.

One way to handle it would be to give each live subtree two fixed promises.
In units of its root weight, promise that its maximum surplus conditional
on its root being outside the comparator is at most $p$, and that the
maximum conditional on being inside is at most $F(p)-\beta$.
Here $p$ also bounds the root's present coordinate. If the old root had
the first promise $p$, and the two independently continuing subtrees
receive promises $s,t$, respectively, local certification requires

$$
s+h(F(t)-\beta)\le p,\qquad
F(s)+ht\le F(p),\qquad s+t\ge1.                         \tag{3}
$$

The three tests use, respectively, the parent outside and child inside,
the parent inside and child outside, and feasibility of the new edge.
Both vertices inside also satisfies the second test when $F(t)\le\beta$
and $t\ge0$. For the one-survivor game the two endpoints could use
different resources on mutually exclusive branches. Here both promises
must be met on the same play.

The certified $F$ above fails this test already at $p=1/2,\ h=1/100$.
The first and third inequalities require $t\ge1-p-h\beta=0.4916$.
The supporting line of slope $-3/5$ at $p$ in the second inequality
gives $t\le(3/5)(\beta-F(t))\le0.504$. Throughout this range
$F(t)\ge F(0.504)>0.222$, forcing $t<0.371$. This is a failure to
extend the certificate. The state is not asserted to be forced on an
arbitrary strategy.

There is an analytic reason (3) leads back to the target. Suppose $F$
is a nonincreasing convex Lipschitz promise function on $[0,\infty)$
with $0\le F\le\beta$, and (3) is feasible for every $p\in[0,1)$
and $h>0$. Put $D(t)=\beta-F(t)$. At a differentiability point $p$,
convexity and (3) give $t\le -F'(p)D(t)$ exactly. Also
$t\ge1-p-h\beta$. By concavity of $D$ and $D(0)\ge0$,
$v/D(v)$ is nondecreasing wherever positive and defined. Sending
$h$ to zero gives

$$
 -F'(p)\ \ge\ (1-p)/D(1-p) \quad\text{a.e. on }(0,1).
$$

For example, division by zero can be avoided throughout the argument
by using $D+\eta$ for any $\eta>0$. With
$f_\eta(t)=\beta+\eta-F(1-t)$, integrating from $p$ to 1 gives

$$
 f_\eta(1-p)+\int_p^1 (1-t)/f_\eta(t)\,dt\ \le\ \beta+\eta .
$$

The function $f_\eta$ is positive and continuous, and
$(1-t)/f_\eta(t)$ is nonincreasing by the same concavity argument.
Wang and Wong's function-class lower bound, followed by $\eta\downarrow0$,
implies $\beta\ge B^*-1$. This derives the target from the constraints
of **independently assigned subtree promises**. It does not derive (3)
from competitiveness of an arbitrary online algorithm. A history-dependent
strategy may change how it allocates the shared surplus as it observes
which subtree grows. [Wang and Wong, Section 4](https://arxiv.org/abs/1305.1694)

The [interleaving lemma](OPTIMALITY_PROOF.md) resolves the missing step.
It preserves the three allowed root masks while keeping each subtree's
future hidden at its own decision times. The local budget inequalities
then follow by minimax and conditional averaging.
