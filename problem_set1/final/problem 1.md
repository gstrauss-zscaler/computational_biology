##### how changes to the scoring function affect the maximum score alignment.
## a
> Prove formally that if the score of a gap is more than half the score of a substitution, then a maximum score alignment of any two sequences does not contain mismatches. In this question you may assume that all gap scores are equal and all substitution scores are equal.

Denote $Q$ as the score function such that:
For every $x$, $y$: $Q(x, -) = Q(-, y) > 1/2 * Q(x, y)$

Denote $T_m$ as a sequence $T$ of length $m$.


We will prove by contradiction.
Assume that exists a maximum score alignment of two sequences $T_m$, $U_n$ such that exists an index i, j where the alignment chose substitution (There can be a case where $i \neq j$ if we chose more gaps in one of the sequences then the other) ($Q(T[i], U[j])$)
We will denote the maximum score as $M$ (for maximum)

We will then choose the exact same sequence, but replacing the choice of substitution $Q(T[i], U[j])$ with two gaps $Q(T[i], -)$, $Q(-, U[j])$
The sum of any two gaps is larger then any single substitution so $S'$ (The new score)
Is equal to the equation:
$S' = S - Q(T[i], U[j]) + Q(T[i], -) + Q(-, U[j]) >$ (replacing two gaps) $S - Q(T[i], U[j]) + Q(T[i], U[j]) >$ (canceling terms out) $S$
$S' > S$
So we proved that if exists a score alignment containing a substitution there exists a new score alignment with higher value in contradiction to our assumption.

This means that if the statement in the question is true then any maximum score alignment of any two sequences will contain only gaps, and no substitution.

## b
> Demonstrate using an example that offsetting a scoring function by an additive constant can change the maximum score local alignment. The score function $Q’$ is said to be an $E$-offset of $Q$ if $Q’(x,y)= Q(x,y)+E$ for all $x,y∈ Σ⋃\{−\}$. Provide an explicit and fully detailed example

Because we only need an example, we can choose an easy case:
Take sequence $T = \{a\}$, $U = \{b\}$ for language $\{a,b\}$
Scoring function:
$Q(a, a) = Q(b, b) = 1$
$Q(a, b) = Q(b, a) = 1$
$Q(-, a) = Q(a, -) = Q(-, b) = Q(b, -) = -1$
Offset:
$E = 100$

The score function $Q$ will give the obvious solution:
$T' = T = U' = \{a\}$
With the score $1$
And the choices:
$Q(a, b)$
For the sequence.

The score function $Q'$ on the other hand will give a different solution (still in an obvious way):
$T' = \{a, -\}$
$U' = \{-, b\}$
With the score $198$
And the choices:
$Q'(a, -), Q'(-, b)$
For the sequence.

Just to show that it does in fact give different solutions (Those are the only two possible)
$Q(a, -), Q(-, b) = -2 < Q(a, b)$
$Q'(a, b) = 101 < Q'(a,-) + Q'(-, b)$

## c
> Can offsetting a scoring function by an additive constant influence the identity of the maximum score global alignment? If you think so, provide an explicit and detailed example to demonstrate this. If you think offsetting cannot influence the maximum score global alignment, then provide a proof of this claim.

Yes, the same example from before holds true,
We can notice that in the example from question $1_b$, the global alignment and local alignment are equal. (In both cases of $Q$ and $Q'$)