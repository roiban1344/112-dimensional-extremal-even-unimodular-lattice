"""Exact arithmetic helpers.
厳密な演算の補助。

Floating-point matrix products are used only when their result is provably exact:
an integer product A @ B computed in floating point is exact if every partial sum
is an integer of absolute value below 2^p (p = 24 for float32, 53 for float64),
because such integers and all intermediate sums are representable.
A bound for all partial sums of row a of A and column b of B is
    sum_k |a_k| |b_k| <= (max_a sum_k |a_k|) * max |B|.
The functions `f32_matmul` and `f64_matmul` check this bound from the actual inputs
before multiplying (with `require`, which -O cannot remove). The bound itself is computed in
Python integers, so it cannot overflow.

浮動小数点の行列積は、結果が厳密だと言えるときだけ使う。整数の積 A @ B は、すべての部分和が
絶対値 2^p 未満の整数なら（float32 で p = 24、float64 で p = 53）、途中の値がすべて表現できるので厳密。
A の行 a と B の列 b の部分和はすべて
    Σ_k |a_k||b_k| ≤ (max_a Σ_k |a_k|) · max|B|
で抑えられる。`f32_matmul` と `f64_matmul` は、掛ける前にこの上界を実際の入力から確かめる（-O で取り除かれない `require` で）。
上界そのものは Python の整数で計算するので、オーバーフローしない。
"""
from fractions import Fraction

import numpy as np

from . import require


def _integer_array(A):
    """A as a numpy array of integers: an integer dtype, or dtype object holding integers.
    Floating-point input is refused (converting it to int64 would truncate silently).
    A を整数の numpy 配列として返す（整数の型、または整数を持つ object 型）。浮動小数点の入力は拒否する
    （int64 への変換は黙って切り捨てるので）。"""
    A = np.asarray(A)
    if A.dtype == object:
        require(all(int(v) == v for v in A.flat), "non-integer entry in an integer matrix")
    else:
        require(np.issubdtype(A.dtype, np.integer) or A.dtype == np.bool_, f"integer array expected, got {A.dtype}")
    return A


def max_abs(A):
    """max |a| over the entries of an integer array, as a Python int (no overflow, also for INT64_MIN).
    整数配列の成分の絶対値の最大（Python の整数。INT64_MIN でもオーバーフローしない）。"""
    A = _integer_array(A)
    if A.size == 0:
        return 0
    if A.dtype == object:
        return max(abs(int(v)) for v in A.flat)
    return max(int(A.max()), -int(A.min()))


def max_row_l1(A):
    """max over rows a of sum_k |a_k| (rows along the last axis), as a Python int.
    The sums are taken in int64 only when max|a| times the row length is below 2^62, so they
    cannot overflow; otherwise in Python integers.
    行 a（最後の軸）にわたる Σ_k |a_k| の最大（Python の整数）。max|a| と行の長さの積が 2^62 未満のときだけ int64 で和を取るので、
    オーバーフローしない。そうでなければ Python の整数で取る。"""
    A = _integer_array(A)
    if A.size == 0:
        return 0
    m = max_abs(A)
    if A.dtype != object and m * A.shape[-1] < 2 ** 62:
        return int(np.abs(A.astype(np.int64)).sum(axis=-1).max())
    return max(sum(abs(int(v)) for v in row) for row in A.reshape(-1, A.shape[-1]))


def partial_sum_bound(A, B):
    """Upper bound for |partial sums| of the integer product A @ B (Python int, exact).
    整数の積 A @ B の部分和の絶対値の上界（Python の整数で厳密に計算）。"""
    A = _integer_array(A)
    B = _integer_array(B)
    if A.size == 0 or B.size == 0:
        return 0
    return max_row_l1(A) * max_abs(B)


def f32_matmul(A, B):
    """A @ B for integer arrays, computed in float32 after checking exactness; returns int64.
    整数配列の A @ B。厳密さを確かめてから float32 で計算し、int64 で返す。"""
    require(partial_sum_bound(A, B) < 2 ** 24, "float32 product would not be exact")
    return (np.asarray(A, dtype=np.float32) @ np.asarray(B, dtype=np.float32)).astype(np.int64)


def f64_matmul(A, B):
    """A @ B for integer arrays, computed in float64 after checking exactness; returns int64.
    整数配列の A @ B。厳密さを確かめてから float64 で計算し、int64 で返す。"""
    require(partial_sum_bound(A, B) < 2 ** 53, "float64 product would not be exact")
    return (np.asarray(A, dtype=np.float64) @ np.asarray(B, dtype=np.float64)).astype(np.int64)


def i64_matmul(A, B):
    """A @ B in int64 after checking that no overflow can occur.
    オーバーフローが起きないことを確かめてから int64 で計算する A @ B。"""
    require(partial_sum_bound(A, B) < 2 ** 62, "int64 product could overflow")
    return np.asarray(A, dtype=np.int64) @ np.asarray(B, dtype=np.int64)


def to_int_matrix(M):
    """numpy integer array -> list of lists of Python ints (arbitrary precision).
    numpy の整数配列 → Python の整数（多倍長）のリストのリスト。"""
    return [[int(v) for v in row] for row in np.asarray(M)]


def det_bareiss(M):
    """Exact determinant of an integer matrix (fraction-free Bareiss elimination, Python ints).
    整数行列の厳密な行列式（分数を使わない Bareiss の消去法、Python の整数）。"""
    A = to_int_matrix(M)
    n = len(A)
    sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            # Swap in a row with a nonzero pivot. / 0 でない枢軸の行と入れ替える。
            for i in range(k + 1, n):
                if A[i][k] != 0:
                    A[k], A[i] = A[i], A[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                # Exact division: Bareiss' identity guarantees divisibility.
                # 割り切れることは Bareiss の恒等式が保証する。
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def ldl_exact(G):
    """Exact decomposition G = V^T diag(D) V over the rationals (V unit upper triangular).
    Returns (D, V) as lists of Fractions; raises if G is not positive definite.
    有理数上の厳密な分解 G = V^T diag(D) V（V は対角成分 1 の上三角）。
    (D, V) を Fraction のリストで返す。G が正定値でなければ例外。"""
    A = to_int_matrix(G)
    n = len(A)
    D = [Fraction(0)] * n
    V = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        # Fraction(...) so that '/' below is exact rational division (int / int would be a float).
        # 下の '/' を有理数の厳密な割り算にするため Fraction にする（int / int は浮動小数点になる）。
        D[i] = Fraction(A[i][i]) - sum(V[k][i] ** 2 * D[k] for k in range(i))
        if D[i] <= 0:
            raise ValueError("matrix is not positive definite")
        V[i][i] = Fraction(1)
        for j in range(i + 1, n):
            V[i][j] = (A[i][j] - sum(V[k][i] * V[k][j] * D[k] for k in range(i))) / D[i]
    # Check the decomposition exactly. / 分解を厳密に検算する。
    for i in range(n):
        for j in range(i, n):
            require(sum(V[k][i] * D[k] * V[k][j] for k in range(i + 1)) == A[i][j], "LDL decomposition does not reproduce G")
    return D, V


def is_positive_definite(G):
    """Exact test (all pivots of the rational LDL decomposition positive).
    厳密な判定（有理数の LDL 分解の枢軸がすべて正）。"""
    try:
        ldl_exact(G)
        return True
    except ValueError:
        return False


def inverse_unimodular(M):
    """Exact inverse of an integer matrix of determinant +-1, as int64
    (Gauss-Jordan elimination over the rationals; integrality is checked).
    行列式 ±1 の整数行列の厳密な逆行列（有理数上の掃き出し法。整数であることを確かめる）。int64 で返す。"""
    A = [[Fraction(v) for v in row] for row in to_int_matrix(M)]
    n = len(A)
    B = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        B[c], B[p] = B[p], B[c]
        piv = A[c][c]
        A[c] = [v / piv for v in A[c]]
        B[c] = [v / piv for v in B[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
                B[r] = [a - f * b for a, b in zip(B[r], B[c])]
    require(all(v.denominator == 1 for row in B for v in row), "inverse is not integral")
    out = np.array([[int(v) for v in row] for row in B], dtype=np.int64)
    require((i64_matmul(np.asarray(M, dtype=np.int64), out) == np.eye(n, dtype=np.int64)).all(), "M M^-1 != I")
    return out


def norms(X, G, block=1 << 18):
    """<x, x> = x G x^T for every row x of X, exactly (int64). x G is computed in float64 after
    the exactness check, then the row-wise products are summed in int64 with an overflow check.
    X の各行 x について <x, x> = x G x^T を厳密に（int64）。x G は厳密さを確かめてから float64 で計算し、
    行ごとの積の和はオーバーフローを確かめて int64 で取る。"""
    X = np.asarray(X)
    out = np.empty(len(X), dtype=np.int64)
    for i in range(0, len(X), block):
        B = X[i:i + block].astype(np.int64)
        XG = f64_matmul(B, G)
        require(max_abs(XG) * max_abs(B) * B.shape[1] < 2 ** 62, "int64 row sums of norms could overflow")
        out[i:i + block] = (XG * B).sum(axis=1)
    return out
