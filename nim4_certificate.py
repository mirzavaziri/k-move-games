"""
Certificate of periodicity for two-move Nim on four heaps (Theorem 6.5).
Input: the output file of nim4_rows.c (P-positions a b c d, sorted).
Usage: python3 nim4_certificate.py FILE A B P
  A = largest row, B = largest level computed, P = candidate joint period.
Prints the first level b1 with S_{b1} = S_{b1+P} (window width A+2),
and the least period and starting level of each row a <= A.
"""
import sys
from collections import defaultdict

fn, A, B, P = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
lev = defaultdict(set)
rows = defaultdict(lambda: defaultdict(set))
for line in open(fn):
    a, b, c, d = map(int, line.split())
    if a <= A:
        lev[b].add((a, c - b, d - b))
        rows[a][b].add((c - b, d - b))

W = A + 2
def window(b):
    return tuple(frozenset(lev[s]) for s in range(b - W, b + 1))

b1 = next((b for b in range(2 * A + W + 2, B - P) if window(b) == window(b + P)), None)
print(f"rows 0..{A}: S_b1 = S_(b1+{P}) for b1 = {b1}")

for a in range(A + 1):
    R = rows[a]
    for p in range(1, B // 2):
        st = a
        for b in range(B - p, a - 1, -1):
            if R[b] != R[b + p]:
                st = b + 1
                break
        if st <= B // 2:
            print(f"row {a}: least period {p}, from level {st}")
            break
