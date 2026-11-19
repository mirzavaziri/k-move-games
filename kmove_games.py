"""
Computations for the paper
"Games with k moves per turn: local freedom and global rigidity"
by M. Mirzavaziri and D. Yaqubi.

Convention: a game is a finite acyclic digraph; a turn consists of k
consecutive moves by the same player; play stops at a sink (even in the
middle of a turn) and the player who made the last move wins.

Usage:
    python3 kmove_games.py            # run all checks
    python3 kmove_games.py rigidity   # run one check
Checks: rigidity, units, nim, nim4
"""
import functools
import itertools
import math
import sys

sys.setrecursionlimit(100000)


# ---------------------------------------------------------------- core

def p_positions(children, k):
    """Return the set of P-positions of G^(k) on the digraph given by
    the adjacency lists `children` (vertices 0..n-1, acyclic)."""
    memo = {}

    def f(v, phase):  # True if the owner of the current turn wins
        key = (v, phase)
        if key in memo:
            return memo[key]
        ch = children[v]
        if not ch:
            res = phase > 0
        else:
            res = any((f(u, phase + 1) if phase + 1 < k else not f(u, 0))
                      for u in ch)
        memo[key] = res
        return res

    return frozenset(v for v in range(len(children)) if not f(v, 0))


def heights(children):
    n = len(children)
    order = topological_order(children)
    H = [0] * n
    for v in reversed(order):
        H[v] = max((H[u] + 1 for u in children[v]), default=0)
    return H


def topological_order(children):
    n = len(children)
    indeg = [0] * n
    for v in range(n):
        for u in children[v]:
            indeg[u] += 1
    stack = [v for v in range(n) if indeg[v] == 0]
    order = []
    while stack:
        v = stack.pop()
        order.append(v)
        for u in children[v]:
            indeg[u] -= 1
            if indeg[u] == 0:
                stack.append(u)
    return order


def all_dags(n):
    """All labelled acyclic digraphs on 0..n-1 with edges i -> j, i < j."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for mask in range(1 << len(pairs)):
        ch = [[] for _ in range(n)]
        for b, (i, j) in enumerate(pairs):
            if mask >> b & 1:
                ch[i].append(j)
        yield ch


# ---------------------------------------------------------- rigidity

def check_rigidity(max_n=6, K=7):
    """Theorem 3.1 and Corollary 3.2 on all DAGs with <= max_n vertices."""
    graphs = violations = 0
    INF = float("inf")
    for n in range(1, max_n + 1):
        for ch in all_dags(n):
            graphs += 1
            S = frozenset(v for v in range(n) if not ch[v])
            H = heights(ch)
            P = [p_positions(ch, k) for k in range(1, K + 1)]
            h = [min((H[v] for v in p if v not in S), default=INF) for p in P]
            for i in range(K):
                for j in range(i + 1, K):
                    # Theorem: non-sinks of height <= h_i are N in G^(j)
                    if any(v not in S and H[v] <= h[i] and v in P[j]
                           for v in range(n)):
                        violations += 1
                    if P[i] == P[j] and P[i] != S:
                        violations += 1
                    if P[i] == S and P[j] != S:
                        violations += 1
    print(f"rigidity: {graphs} digraphs, k <= {K}, violations: {violations}")


# --------------------------------------------------- unit gadgets

def separator(j, k):
    """t >= 1 with ceil(t/j) odd and ceil(t/k) even (Lemma 4.2)."""
    if k < j:
        return j if j < 2 * k else 2 * k
    t = k + 1
    while not (1 <= t % (2 * j) <= j):
        t += 1
    return t


def unit_tree(j, K):
    """The tree T_j of Theorem 4.3 (root = vertex 0)."""
    L = math.lcm(*range(1, K + 1))
    ch = [[]]
    cur = 0
    for _ in range(2 * L - 1):          # the stem
        ch.append([])
        ch[cur].append(len(ch) - 1)
        cur = len(ch) - 1
    x = cur
    for k in range(1, K + 1):           # the legs
        if k == j:
            continue
        prev = x
        for _ in range(separator(j, k) + 1):
            ch.append([])
            ch[prev].append(len(ch) - 1)
            prev = len(ch) - 1
    return ch


def check_units(K_max=7):
    ok = True
    for K in range(2, K_max + 1):
        for j in range(1, K + 1):
            ch = unit_tree(j, K)
            word = "".join("P" if 0 in p_positions(ch, k) else "N"
                           for k in range(1, K + 1))
            target = "".join("N" if k == j else "P" for k in range(1, K + 1))
            ok &= word == target
    print(f"unit gadgets for K <= {K_max}: {'all correct' if ok else 'ERROR'}")


# ---------------------------------------------------------- Nim

def nim_single_moves(p):
    for i, h in enumerate(p):
        for r in range(1, h + 1):
            q = list(p)
            q[i] -= r
            yield tuple(sorted(q))


def make_nim_solver(k):
    @functools.lru_cache(None)
    def turns(p):
        cur = {p}
        for _ in range(k):
            nxt = set()
            for q in cur:
                if sum(q) == 0:
                    nxt.add(q)          # game over, turn ends early
                else:
                    nxt |= set(nim_single_moves(q))
            cur = nxt
        return frozenset(cur)

    @functools.lru_cache(None)
    def is_p(p):
        return sum(p) == 0 or all(not is_p(q) for q in turns(p))

    return is_p


def nim_theorem(p, k):
    """Theorem 5.2 for k+1 heaps (p sorted)."""
    a = p[0]
    return sum(p) == 0 or (a % k == 1 and sum(h - a for h in p) <= k - 1)


def check_nim(bounds=((2, 30), (3, 13), (4, 9))):
    for k, N in bounds:
        is_p = make_nim_solver(k)
        bad = [p for p in itertools.combinations_with_replacement(range(N + 1), k + 1)
               if is_p(p) != nim_theorem(p, k)]
        print(f"{k}-move Nim on {k+1} heaps, heaps <= {N}: mismatches {len(bad)}")


def list_nim4(N=12):
    is_p = make_nim_solver(2)
    P = [p for p in itertools.combinations_with_replacement(range(N + 1), 4)
         if is_p(p) and p[0] > 0]
    print(f"two-move Nim, four non-empty heaps <= {N}, P-positions:")
    print(P)


if __name__ == "__main__":
    checks = {"rigidity": check_rigidity, "units": check_units,
              "nim": check_nim, "nim4": list_nim4}
    names = sys.argv[1:] or list(checks)
    for name in names:
        checks[name]()
