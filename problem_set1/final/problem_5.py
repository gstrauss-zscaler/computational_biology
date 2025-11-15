def scoring(a: str, b: str) -> int:
    if a == b:
        return 2
    if a == "-" or b == "-":
        return -3
    return -2


def smith_waterman_two_rows(s: str, t: str):
    m, n = len(s), len(t)
    prev = [0] * (n + 1)
    best_score = 0
    best_i = 0
    best_j = 0

    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            diag = prev[j - 1] + scoring(s[i - 1], t[j - 1])
            up = prev[j] + scoring(s[i - 1], "-")
            left = curr[j - 1] + scoring("-", t[j - 1])
            val = max(0, diag, up, left)
            curr[j] = val
            if val > best_score:
                best_score = val
                best_i = i - 1
                best_j = j - 1
        prev = curr

    return best_score, best_i, best_j


def nw_last_row(s: str, t: str):
    m, n = len(s), len(t)
    prev = [0] * (n + 1)
    for j in range(1, n + 1):
        prev[j] = prev[j - 1] + scoring("-", t[j - 1])
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        curr[0] = prev[0] + scoring(s[i - 1], "-")
        for j in range(1, n + 1):
            diag = prev[j - 1] + scoring(s[i - 1], t[j - 1])
            up = prev[j] + scoring(s[i - 1], "-")
            left = curr[j - 1] + scoring("-", t[j - 1])
            curr[j] = max(diag, up, left)
        prev = curr
    return prev


def needleman_wunsch_full(s: str, t: str):
    m, n = len(s), len(t)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]
    back = [[None] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        matrix[i][0] = matrix[i - 1][0] + scoring(s[i - 1], "-")
        back[i][0] = "U"
    for j in range(1, n + 1):
        matrix[0][j] = matrix[0][j - 1] + scoring("-", t[j - 1])
        back[0][j] = "L"

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diag = matrix[i - 1][j - 1] + scoring(s[i - 1], t[j - 1])
            up = matrix[i - 1][j] + scoring(s[i - 1], "-")
            left = matrix[i][j - 1] + scoring("-", t[j - 1])
            best = max(diag, up, left)
            matrix[i][j] = best
            if best == diag:
                back[i][j] = "D"
            elif best == up:
                back[i][j] = "U"
            else:
                back[i][j] = "L"

    i = m
    j = n
    aligned_s = []
    aligned_t = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and back[i][j] == "D":
            aligned_s.append(s[i - 1])
            aligned_t.append(t[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or back[i][j] == "U"):
            aligned_s.append(s[i - 1])
            aligned_t.append("-")
            i -= 1
        else:
            aligned_s.append("-")
            aligned_t.append(t[j - 1])
            j -= 1

    aligned_s.reverse()
    aligned_t.reverse()
    return "".join(aligned_s), "".join(aligned_t)


def hirschberg(s: str, t: str):
    m, n = len(s), len(t)
    if m == 0:
        return "-" * n, t
    if n == 0:
        return s, "-" * m
    if m == 1 or n == 1:
        return needleman_wunsch_full(s, t)

    mid = m // 2
    score_l = nw_last_row(s[:mid], t)
    score_r = nw_last_row(s[mid:][::-1], t[::-1])

    best = None
    split = 0
    for j in range(n + 1):
        val = score_l[j] + score_r[n - j]
        if best is None or val > best:
            best = val
            split = j

    left_s, left_t = hirschberg(s[:mid], t[:split])
    right_s, right_t = hirschberg(s[mid:], t[split:])
    return left_s + right_s, left_t + right_t


def main():
    s = "ATAAGGCATTGACCGTATTGCCAA"
    t = "CCCATAGGTGCGGTAGCC"

    best_score, i_end, j_end = smith_waterman_two_rows(s, t)

    s_pref = s[: i_end + 1]
    t_pref = t[: j_end + 1]
    s_rev = s_pref[::-1]
    t_rev = t_pref[::-1]

    _, i_rev_end, j_rev_end = smith_waterman_two_rows(s_rev, t_rev)

    i_start = len(s_pref) - 1 - i_rev_end
    j_start = len(t_pref) - 1 - j_rev_end

    s_sub = s[i_start : i_end + 1]
    t_sub = t[j_start : j_end + 1]

    aligned_s, aligned_t = hirschberg(s_sub, t_sub)

    print("Best local score:", best_score)
    print("S indices:", i_start, "to", i_end)
    print("T indices:", j_start, "to", j_end)
    print("Alignment:")
    print(aligned_s)
    print(aligned_t)


if __name__ == "__main__":
    main()
