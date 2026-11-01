"""lib/shells.py: MinimalVectors.max_abs_inner (the core of the checks of F5a and F5b in v5 and v7) against
brute force, on a small lattice with a nontrivial group.
lib/shells.py: MinimalVectors.max_abs_inner（v5・v7 の F5a・F5b の検査の核）を、自明でない群をもつ小さな格子で総当たりと比べる。

The lattice is 6 Z^4 (Gram matrix 6 I, minimum 6, minimal vectors +-e_i) with the group of signed permutation
matrices; modulo +-1 it has 192 elements, and the single representative e_1 gives all 8 minimal vectors.
格子は 6Z^4（Gram 行列 6I、最小 6、最小ベクトル ±e_i）、群は符号付き置換行列の群（±1 を法として 192 元）。代表 e_1 だけで
8 本の最小ベクトルがすべて得られる。
"""
import itertools

import numpy as np
import pytest

from lib import CheckError, group, shells

N = 4
G = 6 * np.eye(N, dtype=np.int64)


def signed_permutations_mod_sign():
    E = []
    for perm in itertools.permutations(range(N)):
        for signs in itertools.product((1, -1), repeat=N):
            P = np.zeros((N, N), dtype=np.int64)
            P[np.arange(N), perm] = signs
            E.append(P)
    return group.elements_mod_sign(np.stack(E))


S = signed_permutations_mod_sign()
REPS = np.array([[1, 0, 0, 0]], dtype=np.int64)


def brute_force(W):
    U = np.concatenate([np.eye(N, dtype=np.int64), -np.eye(N, dtype=np.int64)])
    return np.abs(np.asarray(W, dtype=np.int64) @ G @ U.T).max(axis=1)


def test_group_and_expansion():
    assert len(S) == 192
    mv = shells.MinimalVectors(G, REPS, S, expected=8)
    assert mv.count == 4
    assert sorted(map(tuple, mv.V.tolist())) == sorted(map(tuple, np.eye(N, dtype=int).tolist()))


@pytest.mark.parametrize("threads, block_w, block_v", [(1, 512, 1 << 16), (2, 3, 2), (1, 1, 1)])
def test_max_abs_inner_against_brute_force(threads, block_w, block_v):
    mv = shells.MinimalVectors(G, REPS, S, expected=8)
    W = np.random.default_rng(5).integers(-9, 10, size=(37, N))
    got = mv.max_abs_inner(W, threads=threads, block_w=block_w, block_v=block_v)
    assert got.dtype == np.int64 and (got == brute_force(W)).all()


def test_wrong_number_of_minimal_vectors_is_refused():
    with pytest.raises(CheckError, match="minimal vectors, expected"):
        shells.MinimalVectors(G, REPS, S)                     # expects |L_6| = 15,590,400


def test_exactness_guard_of_max_abs_inner():
    mv = shells.MinimalVectors(G, REPS, S, expected=8)
    with pytest.raises(CheckError, match="would not be exact"):
        mv.max_abs_inner(np.array([[2 ** 22, 0, 0, 0]]))     # 6 * 2^22 * 1 >= 2^24


def test_int16_guard_of_the_expansion():
    with pytest.raises(CheckError, match="does not fit in int16"):
        shells.expand_half_shell(np.array([[2 ** 15, 0, 0, 0]]), S)
