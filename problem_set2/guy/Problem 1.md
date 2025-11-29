# Alignment With Omissions (AWO)

Let $S=s_1\ldots s_n$, $T=t_1\ldots t_m$.  
A non-contiguous substring is a subsequence.  
An AWO is an alignment of some subsequence of $S$ with some subsequence of $T$.

---

## A

Start from a valid global alignment $(S',T')$ of $S,T$. After deleting any subset of columns, the two strings are still the same length over $\Sigma\cup\{-\}$, so it’s still a valid alignment.

After column deletions, the letters that remain on the $S$-side (ignoring gaps) appear in the same left-to-right order as in $S$, just with some letters missing, so they form a subsequence of $S$. Same for the $T$-side. לכן the output is always an alignment of two subsequences, i.e. an AWO.

---

## B

Take
- $S=\texttt{BAAAAA}$
- $T=\texttt{AAAAAB}$

Scoring:
- $\sigma(x,x)=2$
- $\sigma(x,y)=-1$ for $x\ne y$
- $\sigma(x,-)=\sigma(-,x)=-100$

With these costs, any global alignment that uses a gap pays at least $-100$, so the best global alignment is gapless:

$$
\begin{aligned}
S &: \texttt{B A A A A A}\\
T &: \texttt{A A A A A B}
\end{aligned}
$$

This has 4 matches and 2 mismatches, score:
$$
4\cdot 2 + 2\cdot(-1)=6.
$$

Crude deletes all negative columns, i.e. it deletes the two mismatching columns $(\texttt{B},\texttt{A})$ and $(\texttt{A},\texttt{B})$ and keeps the 4 match columns. Output score:
$$
4\cdot 2=8.
$$

But there is a better AWO: omit the $\texttt{B}$ in both strings and align $\texttt{AAAAA}$ with $\texttt{AAAAA}$:

$$
\begin{aligned}
\texttt{A A A A A}\\
\texttt{A A A A A}
\end{aligned}
$$

Score:
$$
5\cdot 2=10 > 8,
$$
so Crude is not guaranteed to produce a max-score AWO.

---

## C
We assume that indels are not allowed in substring

Let $S=s_1\ldots s_n$, $T=t_1\ldots t_m$.

Define a DP table:
$$
A[i][j] = \text{maximum AWO score between } S[1..i] \text{ and } T[1..j].
$$

Base:
$$
A[0][j]=0 \quad (0\le j\le m), \qquad A[i][0]=0 \quad (0\le i\le n).
$$

Recurrence (for $i\ge 1, j\ge 1$):
$$
A[i][j] = \max\Big\{
A[i-1][j],\;
A[i][j-1],\;
A[i-1][j-1]+\sigma(s_i,t_j)
\Big\}.
$$

Return $A[n][m]$.

**Reconstruction:** keep a parent choice per cell. From $(n,m)$:
- if $A[i][j]=A[i-1][j]$, do $i\leftarrow i-1$ (omit $s_i$)
- else if $A[i][j]=A[i][j-1]$, do $j\leftarrow j-1$ (omit $t_j$)
- else take the pair $(s_i,t_j)$ into the alignment and do $(i,j)\leftarrow(i-1,j-1)$.

**Complexity:** time $O(nm)$, space $O(nm)$ with reconstruction.


---

## D

Let $\text{OPT}(i,j)$ be the maximum AWO score between prefixes $S[1..i]$ and $T[1..j]$

### Claim
For all $i,j$, $A[i][j]=\text{OPT}(i,j)$.

### Proof

**Base:** If $i=0$ or $j=0$, the only possible aligned subsequences have length $0$, so the best score is $0$. The initialization sets $A[0][j]=A[i][0]=0$, so $A=\text{OPT}$ on the boundary.

**Induction step:** Assume $A[i'][j']=\text{OPT}(i',j')$ for all $i'+j' < i+j$. Consider $(i,j)$ with $i,j\ge 1$.

Take an optimal AWO for $(i,j)$. Since gaps/indels are not allowed inside the alignment, the last characters $s_i$ and $t_j$ can appear only in the following mutually exclusive ways:

1. $s_i$ is **omitted** (not used in the chosen subsequence of $S$).  
   Then the solution is an AWO of $(i-1,j)$, so its score is at most $\text{OPT}(i-1,j)$.

2. $t_j$ is **omitted**.  
   Then the score is at most $\text{OPT}(i,j-1)$.

3. $s_i$ and $t_j$ are **paired together** as the last aligned column (because if both are used, with no indels they must be paired).  
   Removing that last paired column leaves an AWO for $(i-1,j-1)$, so the total score is at most
   $$
   \text{OPT}(i-1,j-1)+\sigma(s_i,t_j).
   $$

Therefore,
$$
\text{OPT}(i,j)\le \max\Big\{
\text{OPT}(i-1,j),\;
\text{OPT}(i,j-1),\;
\text{OPT}(i-1,j-1)+\sigma(s_i,t_j)
\Big\}.
$$
---

## E

Let:
$$
L[i][j] = \text{length of the longest common subsequence of } S[1..i],T[1..j].
$$

Recurrence:
$$
L[i][j]=
\begin{cases}
L[i-1][j-1]+1 & s_i=t_j\\
\max\{L[i-1][j],L[i][j-1]\} & s_i\ne t_j
\end{cases}
$$
Base:
$$
L[i][0]=0,\qquad L[0][j]=0.
$$

To output the subsequence, backtrack from $(n,m)$:
- if $s_i=t_j$, output $s_i$ and go to $(i-1,j-1)$
- else go to whichever of $(i-1,j)$ or $(i,j-1)$ attains the max.

Time $O(nm)$. Space $O(nm)$

if $s_i=t_j$ we can match them at the end; if not, an optimal solution must drop one of them so it reduces to one of the two prefix cases.
