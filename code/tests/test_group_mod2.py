"""lib/group.py and lib/mod2.py on a small group of 56 x 56 matrices.
56 × 56 行列の小さな群での lib/group.py と lib/mod2.py。

The group: P = the cyclic shift of the 28 blocks of size 2 (order 28), R = the matrix [[0, -1], [1, -1]]
(order 3, nontrivial modulo 2) on every block, and -I. They commute, so the group is cyclic of order
28 * 3 * 2 = 168 and has 84 elements modulo +-1.
群: P = 大きさ 2 の 28 個のブロックの巡回置換（位数 28）、R = 各ブロックに [[0, -1], [1, -1]]（位数 3。2 を法としても自明でない）、
-I。これらは可換なので、群は位数 28·3·2 = 168 の巡回群で、±1 を法として 84 元。
"""
import numpy as np
import pytest

from lib import CheckError, group, mod2

N = 56


def generators():
    P = np.zeros((N, N), dtype=np.int64)
    for i in range(N):
        P[i, (i + 2) % N] = 1
    R = np.zeros((N, N), dtype=np.int64)
    for b in range(0, N, 2):
        R[b:b + 2, b:b + 2] = [[0, -1], [1, -1]]
    return [P, R, -np.eye(N, dtype=np.int64)]


@pytest.fixture(scope="module")
def small_group():
    E = group.enumerate_group(generators())
    return E, group.elements_mod_sign(E)


def test_group_closure(small_group):
    E, S = small_group
    assert len(E) == 168 and len(S) == 84
    assert (E[0] == np.eye(N)).all()
    keys = {g.tobytes() for g in E}
    assert len(keys) == len(E)
    for g in E:
        for h in generators():
            assert (g.astype(np.int64) @ h).astype(np.int16).tobytes() in keys
    # One of each pair +-g, sign-normalized. / ±g の片方ずつ（符号を正規化したもの）。
    assert len({group.sign_normalize(g).tobytes() for g in E}) == len(S)


def test_group_without_minus_one_is_refused():
    E = group.enumerate_group(generators()[:2])
    assert len(E) == 84
    with pytest.raises(CheckError):
        group.elements_mod_sign(E)


def test_pack_unpack():
    rng = np.random.default_rng(11)
    V = rng.integers(-5, 6, size=(50, N))
    c = mod2.pack(V)
    assert (mod2.unpack(c) == V % 2).all()
    assert (mod2.pack(-V) == c).all() and (mod2.pack(V + 2 * rng.integers(-3, 4, size=V.shape)) == c).all()
    assert int(mod2.pack(np.eye(N, dtype=np.int64)[N - 1])) == 2 ** (N - 1)


def test_canonical_forms_are_invariant(small_group):
    _, S = small_group
    can = mod2.Canonical(S)
    rng = np.random.default_rng(12)
    can.self_test(S, rng)
    v = rng.integers(0, 2, size=(20, N))
    c = mod2.pack(v)
    k, size = can.canon_and_orbit_size(c, batch=7)
    assert (k == can.canon(c)).all()
    for i in range(len(c)):
        # The orbit by matrix products, computed independently of the tables.
        # 表を使わず行列の積で求めた軌道。
        orbit = {int(x) for x in mod2.pack(np.einsum("j,sjk->sk", v[i], S.astype(np.int64)) % 2)}
        assert int(k[i]) == min(orbit) and int(size[i]) == len(orbit)
        # Invariance: every element of the orbit has the same canonical form. / 不変性: 軌道のどの元も同じ標準形をもつ。
        assert (can.canon(np.array(sorted(orbit), dtype=np.uint64)) == k[i]).all()
    # The class 0 is fixed. / 類 0 は固定される。
    k0, s0 = can.canon_and_orbit_size(np.zeros(1, dtype=np.uint64))
    assert int(k0[0]) == 0 and int(s0[0]) == 1
