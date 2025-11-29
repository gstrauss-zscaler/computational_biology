# A

## DP states

Define two DP tables for $0\le i\le m$, $0\le j\le n$:

- $E[i][j]$: minimum cost to align $t_1\ldots t_i$ such that **$t_i$ is aligned to $s_j$** (we end in an exon).
- $I[i][j]$: minimum cost to align $t_1\ldots t_i$ such that **$s_j$ is aligned to a gap** (we end inside an intron).

Let
$$
\text{sub}(i,j)=\begin{cases}
0 & t_i=s_j\\
\alpha & t_i\neq s_j
\end{cases}
$$

---

## Initialization

We treat “not started yet” as free skipping of a prefix of $S$:
- $E[0][j]=0$ for all $j$ (we matched 0 chars of $T$ and can start later).
- $I[0][j]=+\infty$ for all $j$ (can’t be inside an intron before starting).
- For $i>0$: $E[i][0]=I[i][0]=+\infty$.

---

## Transitions

For $i\ge 1, j\ge 1$:

**End in exon (diagonal):**
$$
E[i][j] \;=\; \min\{E[i-1][j-1],\, I[i-1][j-1]\} \;+\; \text{sub}(i,j).
$$

**End in intron (vertical):**
(open costs $+1$, extend costs $+0$)
$$
I[i][j] \;=\; \min\{E[i][j-1]+1,\; I[i][j-1]\}.
$$

---

## Answer

We want all of $T$ aligned and end with a character-character alignment:
$$
\text{OPT} \;=\; \min_{1\le j\le n} E[m][j].
$$
## Correctness

The DP maintains two meanings:

- $E[i][j]$ = minimum cost of aligning $t_1\ldots t_i$ such that the last aligned pair is $(t_i,s_j)$ (so we end in an exon).
- $I[i][j]$ = minimum cost of aligning $t_1\ldots t_i$ such that the last aligned column aligns $s_j$ to a gap in $T$ (so we end inside an intron).

For $E[i][j]$: if an alignment ends with $(t_i,s_j)$, the previous column must be at $(i-1,j-1)$. Just before aligning $(t_i,s_j)$ we were either:
1) already in exon: cost $E[i-1][j-1]$, or
2) in an intron and we now return to exon: cost $I[i-1][j-1]$.
The last aligned pair adds exactly $\text{sub}(i,j)\in\{0,\alpha\}$, so taking the better of the only two valid predecessors gives
$$
E[i][j]=\min\{E[i-1][j-1],\, I[i-1][j-1]\}+\text{sub}(i,j).
$$

For $I[i][j]$: if an alignment ends with $s_j$ aligned to a gap, we must come from $(i,j-1)$ There are only two cases:
1) we open a new intron after an exon: add $1$, giving $E[i][j-1]+1$;
2) we extend an existing intron: add $0$, giving $I[i][j-1]$.
So
$$
I[i][j]=\min\{E[i][j-1]+1,\; I[i][j-1]\}.
$$

Finally, any valid alignment of all of $T$ must end with $t_m$ aligned to some $s_j$ (character-character), so its cost is captured by $E[m][j]$ for that $j$. Minimizing over all possible end positions in $S$ gives the optimal value:
$$
\text{OPT}=\min_{1\le j\le n} E[m][j].
$$

## Complexity

There are $(m+1)(n+1)$ DP cells for each of $E$ and $I$
So total time is:
$$
O(mn).
$$

Space if we store the full tables $E,I$ is:
$$
O(mn).
$$

# B

Let $S=s_1\ldots s_n$, $T=t_1\ldots t_m$.
We use $k+1$ layers indexed by $r\in\{0,\dots,k\}$ = introns used so far, and two types of states:

- $E_r[i][j]$: best score aligning $T[1..i]$ to $S[1..j]$ when we are currently aligning **inside an exon** using the standard alignment rules of $\sigma$.
- $N_r[i][j]$: best score aligning $T[1..i]$ to $S[1..j]$ when we are currently **inside an intron**, i.e. we skip bases of $S$ without consuming $T$.

To keep the exon DP general under $\sigma$, write the standard alignment recurrence as:
$$
E_r[i][j] \;=\; \max\Big(
E_r[i-1][j-1]+\sigma(t_i,s_j),\;
\max_{\ell\ge 1}\{E_r[i][j-\ell]+\sigma(-,S[j-\ell+1..j])\},\;
\max_{\ell\ge 1}\{E_r[i-\ell][j]+\sigma(T[i-\ell+1..i],-)\},\;
N_r[i-1][j-1]+\sigma(t_i,s_j)
\Big)
$$
where $\sigma(-,S[a..b])$ is the additive gap-score of aligning $S[a..b]$ to gaps in $T$ (an exon indel), and similarly for $\sigma(T[a..b],-)$.

Intron transitions (separate from exon gaps):
- extend an intron by skipping $s_j$:
$$
N_r[i][j] = \max\big(N_r[i][j],\; N_r[i][j-1]+\tau(s_j)\big)
$$
- open a new intron (spend one intron) from an exon state:
$$
N_r[i][j] = \max\Big(N_r[i][j],\; E_{r-1}[i][j-1] + P_{\text{intron}} + \tau(s_j)\Big),\quad r\ge 1
$$
Here $\tau(s_j)$ is the additive per-base score while skipping inside an intron (often $0$), and $P_{\text{intron}}$ is an intron-open score/penalty.

Final answer:
$$
\text{OPT}=\max_{0\le r\le k}\ \max_{0\le j\le n} E_r[m][j].
$$

---

## Correctness

The only ambiguity introduced by allowing indels is that a run of gaps in $T$ could be interpreted either as an exonic indel (must be scored by $\sigma$) or as an intron (must count toward the bound $k$). The DP resolves this by splitting them into different states:

- $E_r$ represents alignments that are currently inside an exon and therefore follow exactly the usual additive alignment recurrence derived from $\sigma$. This is the same argument as standard alignment DP (and parallels part (a)): the last step is either a character-character alignment, a gap block in $T$, or a gap block in $S$, and additivity makes “best prefix + score of last step” optimal.

- $N_r$ represents being inside an intron. Its recurrence is exhaustive: the last skipped base $s_j$ is either part of an already-open intron (extend from $N_r[i][j-1]$) or it starts a new intron (transition from $E_{r-1}[i][j-1]$ and spend one intron). Because the only way to increase the intron counter is via the $r-1\to r$ transition, any DP path uses at most $k$ introns when $r\le k$.

Thus every feasible alignment with $\le k$ introns corresponds to some DP path ending in $E_r[m][j]$, and the DP considers all such paths and takes the maximum, so $\text{OPT}$ is the maximum-score feasible alignment.

---

## Complexity

Let $C_\sigma$ be the per-cell cost to compute the exon recurrence under $\sigma$.
- For standard scores (linear or affine gaps), $C_\sigma=O(1)$.
- For a completely general gap scoring without extra structure, the explicit $\max_{\ell\ge 1}$ terms make $C_\sigma=O(m+n)$, so you usually assume linear/affine (as in standard alignment) to keep $O(1)$.

- Time:
$$
O(kmn)
$$
- Space:
  - storing all layers: $O(kmn)$