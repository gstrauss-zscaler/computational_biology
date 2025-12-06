## (a) Base-Pair Counts

Aligning the two sequences position-by-position yields the following 16 ordered pair counts:

| Seq1 \ Seq2 | A | C | G | T |
|-------------|---|---|---|---|
| **A** | 49 | 5 | 3 | 6 |
| **C** | 7 | 37 | 6 | 0 |
| **G** | 7 | 8 | 46 | 5 |
| **T** | 6 | 8 | 7 | 50 |

**Summary:**
- Total matches: $n_{xx} = 49 + 37 + 46 + 50 = 182$
- Total mismatches: $n_{xy} = 68$
- Unordered mismatch counts: $n_{\{A,C\}}=12$, $n_{\{A,G\}}=10$, $n_{\{A,T\}}=12$, $n_{\{C,G\}}=14$, $n_{\{C,T\}}=8$, $n_{\{G,T\}}=12$

---

## (b) MLE for Homology Model Parameters

### Log-Likelihood Function

$$\log L = n_{match} \cdot \ln(1-\lambda) + n_{mismatch} \cdot \ln(\lambda) + \sum_{x} n_{xx} \cdot \ln(p_{xx}) + \sum_{\{x,y\}} n_{xy} \cdot \ln(p_{xy})$$

### MLE Derivations

The log-likelihood separates into independent terms, each optimized by the standard multinomial MLE (observed proportions):

**For $\lambda$:** $\hat{\lambda} = \frac{n_{mismatch}}{n_{total}} = \frac{68}{250} = \mathbf{0.272}$

**For $p_{xx}$ (given NPAM):** $\hat{p}_{xx} = \frac{n_{xx}}{n_{match}}$

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| $p_{AA}$ | 49/182 | **0.269** |
| $p_{CC}$ | 37/182 | **0.203** |
| $p_{GG}$ | 46/182 | **0.253** |
| $p_{TT}$ | 50/182 | **0.275** |

**For $p_{\{x,y\}}$ (given PAM):** $\hat{p}_{xy} = \frac{n_{xy}}{n_{mismatch}}$

| Parameter | Calculation | Value |
|-----------|-------------|-------|
| $p_{\{A,C\}}$ | 12/68 | **0.176** |
| $p_{\{A,G\}}$ | 10/68 | **0.147** |
| $p_{\{A,T\}}$ | 12/68 | **0.176** |
| $p_{\{C,G\}}$ | 14/68 | **0.206** |
| $p_{\{C,T\}}$ | 8/68 | **0.118** |
| $p_{\{G,T\}}$ | 12/68 | **0.176** |

**Justification:** Each parameter group forms a multinomial distribution with sum-to-one constraint. The MLE for multinomial parameters is the observed frequency, which maximizes each independent term in the log-likelihood.

---

## (c) MLE for Unrelated Model Parameters

### Log-Likelihood Function

$$\log L = \sum_{x \in \{A,C,G,T\}} c_x \cdot \ln(q_x)$$

where $c_x$ = total count of nucleotide $x$ across both sequences.

### MLE Estimates

$\hat{q}_x = \frac{c_x}{2n} = \frac{c_x}{500}$

| Nucleotide | Count (both sequences) | $q_x$ |
|------------|------------------------|-------|
| A | 63 + 69 = 132 | **0.264** |
| C | 50 + 58 = 108 | **0.216** |
| G | 66 + 62 = 128 | **0.256** |
| T | 71 + 61 = 132 | **0.264** |

**Justification:** This is a multinomial MLE where the observed frequency of each nucleotide maximizes the log-likelihood.

---

## (d) Scoring Matrix with $\lambda = 0.01$

### Score Function

$$\sigma(x,y) = \begin{cases} \ln(1-\lambda) + \ln(p_{xx}) - 2\ln(q_x) & \text{if } x = y \\ \ln(\lambda) + \ln(p_{\{x,y\}}) - \ln(q_x) - \ln(q_y) & \text{if } x \neq y \end{cases}$$

### How to Calculate Scores (Base Matrix Approach)

*Note: A Python script was used to compute the full matrix. Below we show the underlying method.*

**Step 1:** Compute base matrix without λ using parameters from (b) and (c):
- Diagonal: $\sigma_{base}(x,x) = \ln(p_{xx}) - 2\ln(q_x)$
- Off-diagonal: $\sigma_{base}(x,y) = \ln(p_{\{x,y\}}) - \ln(q_x) - \ln(q_y)$

**Step 2:** Add $\ln(1-\lambda)$ to diagonal, $\ln(\lambda)$ to off-diagonal.

**Example - σ(A,A):**
$$\sigma_{base}(A,A) = \ln(0.269) - 2\ln(0.264) = -1.31 - (-2.66) = 1.35$$
$$\sigma(A,A) = 1.35 + \ln(0.99) = 1.35 + (-0.01) = 1.34$$

**Example - σ(A,C):**
$$\sigma_{base}(A,C) = \ln(0.176) - \ln(0.264) - \ln(0.216) = -1.73 - (-1.33) - (-1.53) = 1.13$$
$$\sigma(A,C) = 1.13 + \ln(0.01) = 1.13 + (-4.61) = -3.48$$

### Scoring Matrix ($\lambda = 0.01$)

|   | A | C | G | T |
|---|------|------|------|------|
| **A** | **1.34** | -3.48 | -3.83 | -3.68 |
| **C** | -3.48 | **1.46** | -3.29 | -3.88 |
| **G** | -3.83 | -3.29 | **1.34** | -3.65 |
| **T** | -3.68 | -3.88 | -3.65 | **1.36** |

---

## (e) Scoring Matrix with $\lambda = 0.1$

### Scoring Matrix ($\lambda = 0.1$)

|   | A | C | G | T |
|---|------|------|------|------|
| **A** | **1.25** | -1.17 | -1.53 | -1.37 |
| **C** | -1.17 | **1.37** | -0.99 | -1.58 |
| **G** | -1.53 | -0.99 | **1.24** | -1.34 |
| **T** | -1.37 | -1.58 | -1.34 | **1.27** |
