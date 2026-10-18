"""lib/exact.py and lib/__init__.py: the exactness guards at their edges, and the exact linear algebra.
lib/exact.py と lib/__init__.py: 厳密さの保証の境界と、厳密な線形代数。"""
import itertools
from fractions import Fraction

import numpy as np
import pytest

from lib import CheckError, exact, require

INT64_MIN = np.iinfo(np.int64).min


# --- require / CheckError ---------------------------------------------------------------------------

def test_require_raises_check_error():
    require(True, "not raised")
    with pytest.raises(CheckError, match="boom"):
        require(False, "boom")


def test_check_error_is_not_an_assertion_error():
    # A failed guard must not be swallowed by code that catches AssertionError.
    # 失敗した保証の検査が、AssertionError を捕まえるコードに握りつぶされてはならない。
    assert not issubclass(CheckError, AssertionError)
    with pytest.raises(CheckError):
        try:
            exact.f32_matmul(np.array([[1]]), np.array([[2 ** 24]]))
        except AssertionError:
            pass


# --- bounds at 2^24, 2^53, 2^62 / 2^24, 2^53, 2^62 の境界 -----------------------------------------------

@pytest.mark.parametrize("matmul, p", [(exact.f32_matmul, 24), (exact.f64_matmul, 53), (exact.i64_matmul, 62)])
def test_bound_edges(matmul, p):
    # Bound 2^p - 1 is accepted and the product is exact; bound 2^p is refused.
    # 上界 2^p - 1 は受け付けて積は厳密。上界 2^p は拒否する。
    one = np.array([[1]])
    assert int(matmul(one, np.array([[2 ** p - 1]]))[0, 0]) == 2 ** p - 1
    assert int(matmul(-one, np.array([[2 ** p - 1]]))[0, 0]) == -(2 ** p - 1)
    with pytest.raises(CheckError):
        matmul(one, np.array([[2 ** p]]))
    with pytest.raises(CheckError):
        matmul(np.array([[2 ** (p // 2), 2 ** (p // 2)]]), np.array([[2 ** (p - p // 2 - 1)], [2 ** (p - p // 2 - 1)]]))


def test_partial_sum_bound_values():
    A = np.array([[-3000, 4000, -5000], [1, 2, 3]])
    B = np.array([[-1000], [1000], [-1000]])
    assert exact.partial_sum_bound(A, B) == 12000 * 1000
    assert (exact.f32_matmul(A, B) == A @ B).all()
    assert exact.partial_sum_bound(np.zeros((0, 3), dtype=np.int64), B) == 0


def test_cancellation_is_refused():
    # The result is 0, but the partial sums reach 3 * 2^24: the bound must refuse it.
    # 結果は 0 だが部分和は 3·2^24 に達する。上界で拒否しなければならない。
    A = np.array([[2 ** 23, 2 ** 23, -2 ** 23, -2 ** 23]])
    B = np.full((4, 1), 3, dtype=np.int64)
    assert int((A @ B)[0, 0]) == 0
    with pytest.raises(CheckError):
        exact.f32_matmul(A, B)
    assert int(exact.f64_matmul(A, B)[0, 0]) == 0


def test_int64_min():
    a = np.array([INT64_MIN, 5], dtype=np.int64)
    assert exact.max_abs(a) == 2 ** 63
    assert exact.max_row_l1(np.array([[INT64_MIN, INT64_MIN]], dtype=np.int64)) == 2 ** 64
    with pytest.raises(CheckError):
        exact.i64_matmul(np.array([[INT64_MIN]]), np.array([[1]]))


def test_large_rows_use_python_integers():
    # max|a| times the row length >= 2^62: the row sums are taken in Python integers (no wrap-around).
    # max|a| と行の長さの積が 2^62 以上: 行の和は Python の整数で取る（回り込まない）。
    A = np.full((2, 4), 2 ** 61, dtype=np.int64)
    A[1, 0] = -2 ** 61
    assert exact.max_row_l1(A) == 2 ** 63


def test_float_input_is_refused():
    with pytest.raises(CheckError):
        exact.max_abs(np.array([1.5]))
    with pytest.raises(CheckError):
        exact.f32_matmul(np.array([[1.0]]), np.array([[1]]))
    with pytest.raises(CheckError):
        exact.partial_sum_bound(np.array([[1]]), np.array([[2.0]]))
    # dtype object: integers are accepted, a fraction is not. / object 型: 整数は受け付け、分数は拒否する。
    assert exact.max_abs(np.array([3, -2 ** 70], dtype=object)) == 2 ** 70
    with pytest.raises(CheckError):
        exact.max_abs(np.array([Fraction(1, 2)], dtype=object))


# --- exact linear algebra / 厳密な線形代数 ---------------------------------------------------------------

def det_leibniz(M):
    n = len(M)
    total = 0
    for p in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        prod = 1
        for i in range(n):
            prod *= int(M[i][p[i]])
        total += (-1) ** inv * prod
    return total


def rand_unimodular(rng, n, steps=40, c=2):
    U = np.eye(n, dtype=np.int64)
    for _ in range(steps):
        i, j = rng.choice(n, 2, replace=False)
        U[i] += int(rng.integers(-c, c + 1)) * U[j]
    if rng.integers(2):
        U[0] *= -1
    return U


def test_det_bareiss_small():
    rng = np.random.default_rng(1)
    for _ in range(200):
        n = int(rng.integers(1, 6))
        M = rng.integers(-9, 10, size=(n, n))
        if rng.integers(4) == 0:
            M[:, int(rng.integers(n))] = 0          # singular / 特異
        assert exact.det_bareiss(M) == det_leibniz(M)
    # Zero pivots that need row swaps. / 行の入れ替えが必要な 0 の枢軸。
    assert exact.det_bareiss([[0, 1], [1, 0]]) == -1
    assert exact.det_bareiss([[0, 1, 0], [0, 0, 1], [1, 0, 0]]) == 1
    assert exact.det_bareiss([[0, 0], [0, 1]]) == 0
    # Entries beyond int64: Python integers throughout. / int64 を超える成分: 最後まで Python の整数。
    big = [[2 ** 40, 1], [3, 2 ** 40]]
    assert exact.det_bareiss(np.array(big, dtype=object)) == 2 ** 80 - 3


def test_ldl_exact():
    G = [[2, 1, 0], [1, 2, 1], [0, 1, 2]]
    D, V = exact.ldl_exact(G)
    assert D == [Fraction(2), Fraction(3, 2), Fraction(4, 3)]
    for i in range(3):
        for j in range(3):
            assert sum(V[k][i] * D[k] * V[k][j] for k in range(3)) == G[i][j]
    with pytest.raises(ValueError):
        exact.ldl_exact([[2, 3], [3, 2]])
    assert exact.is_positive_definite([[2, 1], [1, 2]])
    assert not exact.is_positive_definite([[2, 3], [3, 2]])
    assert not exact.is_positive_definite([[1, 0], [0, 0]])


def test_inverse_unimodular():
    rng = np.random.default_rng(2)
    for _ in range(30):
        n = int(rng.integers(2, 7))
        U = rand_unimodular(rng, n)
        Ui = exact.inverse_unimodular(U)
        assert (U @ Ui == np.eye(n, dtype=np.int64)).all()
    with pytest.raises(CheckError):
        exact.inverse_unimodular([[2, 0], [0, 1]])


def test_norms():
    rng = np.random.default_rng(3)
    B = rng.integers(-3, 4, size=(5, 5))
    G = B @ B.T
    X = rng.integers(-50, 51, size=(101, 5))
    expected = np.einsum("ij,jk,ik->i", X, G, X)
    assert (exact.norms(X, G, block=7) == expected).all()
    with pytest.raises(CheckError):
        exact.norms(np.array([[2 ** 40, 0]]), np.eye(2, dtype=np.int64) * 2 ** 20)
