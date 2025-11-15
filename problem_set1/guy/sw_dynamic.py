import numpy as np
import pandas as pd


def scoring(a: str, b: str) -> int:
    if a == b:
        return 2
    if a == "-" or b == "-":
        return -3
    return -2


def main():
    s = "ATAAGGCATTGACCGTATTGCCAA"
    t = "CCCATAGGTGCGGTAGCC"

    matrix = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]
    backtracking = [[None] * (len(t) + 1) for _ in range(len(s) + 1)]
    best_score = 0
    best_i = 0
    best_j = 0

    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            diag = matrix[i - 1][j - 1] + scoring(s[i - 1], t[j - 1])
            up = matrix[i - 1][j] + scoring("-", t[j - 1])
            left = matrix[i][j - 1] + scoring(s[i - 1], "-")
            best = max(0, diag, up, left)
            matrix[i][j] = best

            if best > best_score:
                best_score = best
                best_i = i
                best_j = j

            if best == diag:
                backtracking[i][j] = "D"
            if best == up:
                backtracking[i][j] = "U"
            if best == left:
                backtracking[i][j] = "L"

    print(pd.DataFrame(matrix))
    print("Best score:", best_score, "at indexes:", best_i, best_j)

    def traceback(start_i, start_j, forbidden_i=None, forbidden_j=None):
        if forbidden_i is None:
            forbidden_i = set()
        if forbidden_j is None:
            forbidden_j = set()

        i = start_i
        j = start_j
        aligned_s = []
        aligned_t = []
        idx_s = []
        idx_t = []
        path = []

        while matrix[i][j] != 0:
            if i in forbidden_i or j in forbidden_j:
                return None, None, None, None, None
            move = backtracking[i][j]
            path.append((i, j))
            if move == "D":
                aligned_s.append(s[i - 1])
                aligned_t.append(t[j - 1])
                idx_s.append(i - 1)
                idx_t.append(j - 1)
                i -= 1
                j -= 1
            elif move == "U":
                aligned_s.append(s[i - 1])
                aligned_t.append("-")
                idx_s.append(i - 1)
                idx_t.append("-")
                i -= 1
            elif move == "L":
                aligned_s.append("-")
                aligned_t.append(t[j - 1])
                idx_s.append("-")
                idx_t.append(j - 1)
                j -= 1
            else:
                break

        aligned_s = list(reversed(aligned_s))
        aligned_t = list(reversed(aligned_t))
        idx_s = list(reversed(idx_s))
        idx_t = list(reversed(idx_t))
        path = list(reversed(path))

        return aligned_s, aligned_t, idx_s, idx_t, path

    first_s, first_t, first_idx_s, first_idx_t, first_path = traceback(best_i, best_j)

    print("First optimal alignment:")
    print("S:", "".join(first_s))
    print("T:", "".join(first_t))
    print("S idx:", first_idx_s)
    print("T idx:", first_idx_t)

    masked_bt = []
    first_path_set = set(first_path)
    for i in range(len(backtracking)):
        row = []
        for j in range(len(backtracking[0])):
            if (i, j) in first_path_set:
                row.append(backtracking[i][j])
            else:
                row.append(".")
        masked_bt.append(row)

    print(pd.DataFrame(masked_bt))

    used_i = {i for i, _ in first_path}
    used_j = {j for _, j in first_path}

    second_s = None

    for i in range(1, len(s) + 1):
        if second_s is not None:
            break
        for j in range(1, len(t) + 1):
            if matrix[i][j] == best_score:
                a_s, a_t, is_s, it_t, p = traceback(i, j, used_i, used_j)
                if a_s is not None:
                    second_s = a_s
                    second_t = a_t
                    second_idx_s = is_s
                    second_idx_t = it_t
                    break

    if second_s is not None:
        print("Second optimal alignment (non-overlapping):")
        print("S:", "".join(second_s))
        print("T:", "".join(second_t))
        print("S idx:", second_idx_s)
        print("T idx:", second_idx_t)


if __name__ == '__main__':
    main()
