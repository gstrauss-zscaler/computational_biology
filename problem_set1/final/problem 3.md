## a
> Suggest a DP algorithm which takes a genome sequence, 𝑇, a paired-end read, $S = (S_1, l, S_2)$, and an alignment scoring function 𝜎, and computes in $𝑂(|𝑆||𝑇|)$ complexity a maximum score mapping.

Give $T$ and $S = (S_1, l, S_2)$.
1. We will run global alignment with the first row being set to 0, as we can start from any point in $T$ but we must align all of $S_1$ and $S_2$
2. For $S_1$, run SW on $(S_1, T)$ and denote as $H_{s1}$. Then, we are interested to find in every $0...len(T)$ the best local alignment score that ends at $T[j]$. This array is the last row in $H_{s1}$ meaning for the sequence $S_1$ the best local alignment for $T[1..j]$ ending in $T[j]$ is $H_{s1}[|S_1|,j]$
3. To enforce the that $A_2$ will start exactly $l$ bases after, we will run SW on the reversed sequences $S^{rev}_2$ and $T^{rev}$, noted as $H_{s2}$, and compute look at the same row storing the best local alignment score of $S_2$ that ended at $|T| - j + 1]$
4. We will couple every cell $H_{s1}[|S_1|,j]$ with the cell $H_{s2}[|S_2|,|T| - j - l]$.
5. From those couples we will choose the one with the highest sum.

### Matrix Cell
* Holds both the score of the local alignment, with update formula of 
$$ 
H[i, 0] = 0
$$
$$
H[i,j] = \max\Big(
    0,\;
    H[i-1,j-1] + \sigma(S[i], T[j]),\;
    H[i-1,j]   + \text{gap},\;
    H[i,j-1]   + \text{gap}
  \Big)
$$
and track of the previous step that was taken beforehand

Each cell  $H_{s2}[|S_2|,|T| - j - l]$ holds the global alignment for $S^{rev}_2$ with suffix of $T^{rev}[0..|T| - j - l]$
When unreversing the sequences we get:
global alignment of $S_2$ with prefix of $T[j+l..|T|]$

## b
> consider a scenario where the distance between alignments, $𝑙$, is not known.

We reuse parts 1–3 from (a), computing $H_{s1}$, $H_{s2}$, $\text{max}_{s1}$, $\text{max}_{s2}$ as before, and add additional steps

1. Compute $\text{rolling max}_{s1}$, $\text{left arg}_{s1}$ (prefix maxima of $\text{max}_{s1}$), and $\text{rolling max}_{s2}$, $\text{right arg}_{s2}$ (suffix maxima of $\text{max}_{s2}$).

2. For each $k = 0 \ldots |T|-1$, compute  
   $$
   \text{Score}(k)
   = \text{rolling max}_{s1}[k]
   + \text{rolling max}_{s2}[k+1]
   $$
   and take the maximal score.

3. Let $k^*$ be the maximizing cut.  
   Set  
   $$
   i^* = \text{left arg}_{s1}[k^*], \qquad
   j^* = \text{right arg}_{s2}[k^*+1].
   $$
   Using these indices, perform traceback in $H_{s1}$ and $H_{s2}$ as in part (a) to output $A_1$ and $A_2$.