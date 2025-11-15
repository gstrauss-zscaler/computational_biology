
# Ex 2

## a
The technique used in the NW algorithm assumes that the alignment will cross the middle section of the matrix, meaning it will start at $(0,0)$ and end at $(m,n)$. In the local alignment case, it's a possibility we will never cross the mid column of the matrix, because the solution might be contained in a sub matrix
## b
The idea of our algorithm is to first find the sub-matrix that contains the local alignment, and then use NW with linear space to find the actual sequences.

---
1. Run SW while maintaining only last 2 rows in memory. and save the indexes $(i,j)$ of the max value as $(i_{end}, j_{end})$. These will provide us with the bottom right corner
2. Take $S_{0..i_{end}}$  and $T_{0..j_{end}}$. reverse them, and run SW in the same fashion as we did in #1, and trace $argmax_{(i,j)}(max)$, and interpolate back the original values, $i_{start} = |S| - i + 1$ and $j_{start} = |T| - j + 1$
3. Look at $S_{i_{start}..i_{end}}$  and $T_{j_{start}..j_{end}}$, and run NW with linear space

----

## c
To prove correctness, we will argue that steps 1 & 2 results with a sub-matrix contains best local alignment path that start at $(i_{start}, j_{start})$ and ends at $(i_{end}, j_{end})$ - Like an internal case of global alignment. Because step 1 requires no additional explanation, we will focus on step #2. With reversing both sequences, we now interested in finding where the local alignment ends, which in turn tells us the starting place in the original sequences, after getting said indexes, our conceptual scoring matrix looks something of the following
$$
\begin{array}{c}
\begin{array}{cccccccc}
. & . & . & . & . & . & . & . \\
. & \text{start} & . & . & . & . & . & . \\
. & . & . & . & . & . & . & . \\
. & . & . & . & . & . & . & . \\
. & . & . & . & \text{end} & . & . & . \\
. & . & . & . & . & . & . & . \\
\end{array}
\end{array}
$$
Now, we just run DW to get the actual alignment.
As for time complexity, we still run at $O(|S|\times|T|)$, and our space is $O(|S|+|T|)$


# Ex 3

## a
Give $T$ and $S = (S_1, l, S_2)$.
1. For $S_1$, run SW on $(S_1, T)$ and denote as $H_{s1}$. Then, we are interested to find in every $0...len(T)$ the best local alignment score that ends at $T[j]$. This array $max_{s1}[j]=max(H_{s1}[1,j], H_{s1}[2,j]..., H_{s1}[|S_1|, j])$
2. To enforce the that $A_2$ will start exactly $l$ bases after, we will run SW on the reversed sequences $S^{rev}_2$ and $T^{rev}$, noted as $H_{s2}$, and compute $max_{s2}[j]=max(H_{s2}[1,j], H_{s2}[2,j]..., H_{s2}[|S_2|, j])$ storing the best local alignment score of $S_2$ that ended at $|T| - j + 1]$
3. Afterwards, we iterate over $max_{s1}$ and $max_{s2}$, and find $arg_i$ that satisfies max value for $max_{s1}[i] + max_{s2}[i+l+1]$. while $i+l+1\le |T|$ 
4. Then, using both matrix, output $A_1$ and $A_2$

### Matrix Cell
* Holds both the score of the local alignment, with update formula of 
$$
 H[i,j] = \max\Big(
    0,\;
    H[i-1,j-1] + \sigma(S[i], T[j]),\;
    H[i-1,j]   + \text{gap},\;
    H[i,j-1]   + \text{gap}
  \Big)
$$
and track of the previous step that was taken beforehand

## b
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


# Ex 4

```bash
    0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18
0    0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
1    0   0   0   0   2   0   2   0   0   0   0   0   0   0   0   2   0   0   0
2    0   0   0   0   0   4   1   0   0   2   0   0   0   0   2   0   0   0   0
3    0   0   0   0   2   1   6   3   0   0   0   0   0   0   0   4   1   0   0
4    0   0   0   0   2   0   3   4   1   0   0   0   0   0   0   2   2   0   0
5    0   0   0   0   0   0   0   5   6   3   2   0   2   2   0   0   4   1   0
6    0   0   0   0   0   0   0   2   7   4   5   2   2   4   1   0   2   2   0
7    0   2   2   2   0   0   0   0   4   5   2   7   4   1   2   0   0   4   4
8    0   0   0   0   4   1   2   0   1   2   3   4   5   2   0   4   1   1   2
9    0   0   0   0   1   6   3   0   0   3   0   1   2   3   4   1   2   0   0
10   0   0   0   0   0   3   4   1   0   2   1   0   0   0   5   2   0   0   0
11   0   0   0   0   0   0   1   6   3   0   4   1   2   2   2   3   4   1   0
12   0   0   0   0   2   0   2   3   4   1   1   2   0   0   0   4   1   2   0
13   0   2   2   2   0   0   0   0   1   2   0   3   0   0   0   1   2   3   4
14   0   2   4   4   1   0   0   0   0   0   0   2   1   0   0   0   0   4   5
15   0   0   1   2   2   0   0   2   2   0   2   0   4   3   0   0   2   1   2
16   0   0   0   0   0   4   1   0   0   4   1   0   1   2   5   2   0   0   0
17   0   0   0   0   2   1   6   3   0   1   2   0   0   0   2   7   4   1   0
18   0   0   0   0   0   4   3   4   1   2   0   0   0   0   2   4   5   2   0
19   0   0   0   0   0   2   2   1   2   3   0   0   0   0   2   1   2   3   0
20   0   0   0   0   0   0   0   4   3   0   5   2   2   2   0   0   3   0   1
21   0   2   2   2   0   0   0   1   2   1   2   7   4   1   0   0   0   5   2
22   0   2   4   4   1   0   0   0   0   0   0   4   5   2   0   0   0   2   7
23   0   0   1   2   6   3   2   0   0   0   0   1   2   3   0   2   0   0   4
24   0   0   0   0   4   4   5   2   0   0   0   0   0   0   1   2   0   0   1
Best score: 7 at indexes: 6 8
First optimal alignment:
S: ATAAGG
T: ATA-GG
S idx: [0, 1, 2, 3, 4, 5]
T idx: [3, 4, 5, '-', 6, 7]
   0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
0   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
1   .  .  .  .  D  .  .  .  .  .  .  .  .  .  .  .  .  .  .
2   .  .  .  .  .  D  .  .  .  .  .  .  .  .  .  .  .  .  .
3   .  .  .  .  .  .  D  .  .  .  .  .  .  .  .  .  .  .  .
4   .  .  .  .  .  .  U  .  .  .  .  .  .  .  .  .  .  .  .
5   .  .  .  .  .  .  .  D  .  .  .  .  .  .  .  .  .  .  .
6   .  .  .  .  .  .  .  .  D  .  .  .  .  .  .  .  .  .  .
7   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
8   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
9   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
10  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
11  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
12  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
13  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
14  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
15  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
16  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
17  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
18  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
19  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
20  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
21  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
22  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
23  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
24  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
Second optimal alignment (non-overlapping):
S: TGACCGTA
T: TG-CGGTA
S idx: [9, 10, 11, 12, 13, 14, 15, 16]
T idx: [8, 9, '-', 10, 11, 12, 13, 14]

```

## d
For finding another alignment, we just looked for another max score of 7

## e
```
S: A T A A G G (0 - 5)
T: A T - A G G (3 - 7)
```

# Ex 5

Attached separately 