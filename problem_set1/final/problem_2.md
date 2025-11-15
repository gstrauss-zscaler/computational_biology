# Ex 2

## a
The technique used in the NW algorithm assumes that the optimal alignment path must cross the middle section of the DP matrix, because it always begins at $(0,0)$ and ends at $(m,n)$. In local alignment this assumption fails: the optimal solution may be completely contained in an internal sub-matrix, never touching the mid column or any boundary. Therefore, the divide-and-conquer strategy of Hirschberg cannot be applied as is.

---

## b
The idea of our algorithm is to first locate the sub-matrix that contains the optimal local alignment, and then run NW with linear space only on that region.

---

1. Run SW while maintaining only the last 2 rows. Track the location $(i,j)$ of the maximum cell and denote it by $(i_{\text{end}}, j_{\text{end}})$. This gives the bottom-right endpoint of the optimal local alignment.

2. Take $S_{0..i_{\text{end}}}$ and $T_{0..j_{\text{end}}}$, reverse both, and run SW again in the same linear-space fashion. Let $(i,j)$ be the new maximum. Convert this to the original coordinates:
   $$
   i_{\text{start}} = |S| - i + 1,\quad
   j_{\text{start}} = |T| - j + 1.
   $$

3. Consider $S_{i_{\text{start}}..i_{\text{end}}}$ and $T_{j_{\text{start}}..j_{\text{end}}}$, and run NW with Hirschberg’s trick to recover the alignment in linear space.

---

## c
Steps **1** and **2** correctly identify the sub-matrix containing the optimal local alignment, with path starting at $(i_{\text{start}}, j_{\text{start}})$ and ending at $(i_{\text{end}}, j_{\text{end}})$.

Step **1** is immediate: the maximum cell of the Smith–Waterman matrix is exactly the end-point of the optimal local alignment.

The key part is step **2**. After reversing both sequences, the same local alignment appears reversed, and the original starting point becomes the ending point of a local alignment in the reversed prefixes. Running SW again therefore reveals precisely where the optimal alignment must begin in the original orientation. Converting back from reversed indices yields $(i_{\text{start}}, j_{\text{start}})$.

Conceptually, this produces a matrix of the following form:

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

Once both endpoints are known, the problem reduces to a global alignment inside this sub-region, and NW with Hirschberg reconstructs the alignment.

For the complexity: each SW pass takes $O(|S|\cdot|T|)$ time and only $O(|S|+|T|)$ space. The final NW reconstruction is also linear space. Thus, the entire algorithm runs in time  
$$O(|S|\cdot|T|)$$  
and space  
$$O(|S|+|T|).$$
