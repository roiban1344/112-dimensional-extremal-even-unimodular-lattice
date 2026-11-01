"""lib/enumerate.py and verify/enum_interval.c: known lattices and a brute-force comparison.
lib/enumerate.py と verify/enum_interval.c: 既知の格子と、総当たりとの比較。"""
import itertools

import numpy as np
import pytest

from lib import CheckError
from lib import enumerate as en

E8 = np.array([
    [2, 1, 1, -1, 1, 1, 1, 1], [1, 2, 1, 0, 1, 1, 0, 1], [1, 1, 2, -1, 1, 0, 1, 1], [-1, 0, -1, 2, 0, 0, -1, -1],
    [1, 1, 1, 0, 2, 0, 0, 0], [1, 1, 0, 0, 0, 2, 0, 1], [1, 0, 1, -1, 0, 0, 2, 1], [1, 1, 1, -1, 0, 1, 1, 2]], dtype=np.int64)
A2 = np.array([[2, -1], [-1, 2]], dtype=np.int64)
D4 = np.array([[2, -1, 0, 0], [-1, 2, -1, -1], [0, -1, 2, 0], [0, -1, 0, 2]], dtype=np.int64)


def rand_unimodular(rng, n, steps=40, c=2):
    U = np.eye(n, dtype=np.int64)
    for _ in range(steps):
        i, j = rng.choice(n, 2, replace=False)
        U[i] += int(rng.integers(-c, c + 1)) * U[j]
    return U


def counts(exe, G, bound):
    return en.run_enumerator(exe, G, bound)["counts"]


@pytest.mark.parametrize("n", [1, 3, 8])
def test_cubic_lattice(enum_exe, n):
    # Z^n: 2n vectors of norm 1, 2n(n-1) of norm 2.
    # Z^n: ノルム 1 が 2n 本、ノルム 2 が 2n(n-1) 本。
    Z = np.eye(n, dtype=np.int64)
    expected = {1: 2 * n}
    if n > 1:
        expected[2] = 2 * n * (n - 1)
    assert counts(enum_exe, Z, 2) == expected


def test_root_lattices(enum_exe):
    assert counts(enum_exe, A2, 8) == {2: 6, 6: 6, 8: 6}
    assert counts(enum_exe, D4, 4) == {2: 24, 4: 24}
    assert counts(enum_exe, E8, 4) == {2: 240, 4: 2160}
    assert counts(enum_exe, 2 * E8, 8) == {4: 240, 8: 2160}


def test_e8_in_skewed_bases(enum_exe):
    # The counts do not depend on the basis; a skewed basis exercises long enumeration paths.
    # 本数は基底に依らない。歪めた基底は長い列挙の経路を通る。
    rng = np.random.default_rng(5)
    for _ in range(5):
        U = rand_unimodular(rng, 8)
        Gs = U @ E8 @ U.T
        assert counts(enum_exe, Gs, 4) == {2: 240, 4: 2160}


def brute_force(G, bound):
    """All x != 0 with x G x^T <= bound, one of each +-pair (last nonzero coordinate positive), by a box search.
    x G x^T ≤ bound となる 0 でない x（±の片方。最後の 0 でない座標が正）を箱の中の総当たりで。"""
    n = len(G)
    Gi = np.linalg.inv(G.astype(float))
    # |x_i| <= sqrt(bound (G^-1)_ii); +1 for safety. / |x_i| ≤ √(bound (G^-1)_ii)。安全のため +1。
    box = [int(np.sqrt(bound * Gi[i, i])) + 1 for i in range(n)]
    X = np.array(list(itertools.product(*[range(-b, b + 1) for b in box])), dtype=np.int64)
    q = np.einsum("ij,jk,ik->i", X, G, X)
    X, q = X[(q <= bound) & X.any(axis=1)], q[(q <= bound) & X.any(axis=1)]
    last = np.array([x[np.flatnonzero(x)[-1]] for x in X], dtype=np.int64) if len(X) else np.zeros(0)
    return sorted((tuple(int(v) for v in x), int(qq)) for x, qq in zip(X[last > 0], q[last > 0]))


def test_random_forms_against_brute_force(enum_exe, tmp_path):
    rng = np.random.default_rng(7)
    for _ in range(60):
        n = int(rng.integers(2, 6))
        B = rng.integers(-3, 4, size=(n, n))
        G = B @ B.T + np.eye(n, dtype=np.int64)
        bound = int(rng.integers(1, 15))
        got, _ = en.short_vectors(G, bound, str(tmp_path))
        got = sorted((tuple(int(v) for v in x), q) for x, q in got)
        exp = brute_force(G, bound)
        # The enumerator returns one of each +-pair, not necessarily with the same sign convention.
        # 列挙器は ±の片方を返すが、符号の決め方は同じとは限らない。
        canon = lambda x: x if x[max(i for i, v in enumerate(x) if v)] > 0 else tuple(-v for v in x)  # noqa: E731
        assert sorted((canon(x), q) for x, q in got) == exp, (G.tolist(), bound)
        for x, q in got:
            assert int(np.array(x) @ G @ np.array(x)) == q


def test_untabulated_leaves_are_reported(enum_exe):
    # Norm 2 k^2 <= 5000: k = 1..50; the norms 2 k^2 >= 4096 (k = 46..50) are outside the table of the
    # enumerator, which must report them, and run_enumerator must then refuse the result.
    # ノルム 2k^2 ≤ 5000 なら k = 1..50。2k^2 ≥ 4096（k = 46..50）は列挙器の表の外にあり、列挙器はそれを報告し、
    # run_enumerator は結果を拒否しなければならない。
    import subprocess
    out = subprocess.run([enum_exe, "0"], input=en.enumerator_input([[2]], 5000), stdout=subprocess.PIPE,
                         text=True, check=True).stdout
    assert "untabulated vectors of norm >= 4096: 10" in out
    with pytest.raises(CheckError, match="outside the table"):
        en.run_enumerator(enum_exe, [[2]], 5000)
    assert counts(enum_exe, [[2]], 4095) == {2 * k * k: 2 for k in range(1, 46)}


def test_input_of_the_enumerator_for_L():
    # The path of v1 on L up to the enumeration itself (which takes 34 minutes, and more than 10^8 nodes even at
    # radius 2): reduction_L.txt is unimodular, G' = U G U^T is even with det 1, and the intervals written for the
    # enumerator (hexadecimal floats, read exactly by C) contain the exact rationals D_i and V_ij of G' = V^T diag(D) V.
    # L に対する v1 の経路のうち、列挙そのもの（34 分。半径 2 でも 10^8 節点を超える）の手前まで: reduction_L.txt はユニモジュラー、
    # G' = U G U^T は偶で det 1、列挙器に書く区間（C が厳密に読む 16 進の浮動小数点）は G' = V^T diag(D) V の厳密な有理数 D_i, V_ij を含む。
    from lib import certs, data, exact
    U = certs.load_matrix("reduction_L.txt", 56)
    assert abs(exact.det_bareiss(U)) == 1
    Gr = exact.i64_matmul(exact.i64_matmul(U, data.gram()), U.T)
    assert (Gr == Gr.T).all() and (np.diag(Gr) % 2 == 0).all() and exact.det_bareiss(Gr) == 1
    lines = en.enumerator_input(Gr, 4).splitlines()
    assert lines[0] == "56 4" and len(lines) == 1 + 56 + 56 + 56 * 55 // 2
    D, V = exact.ldl_exact(Gr)
    exact_values = list(D) + [V[i][j] for i in range(56) for j in range(i + 1, 56)]
    for line, q in zip(lines[57:], exact_values):
        lo, hi = (float.fromhex(t) for t in line.split())
        assert lo <= q <= hi and lo < hi
