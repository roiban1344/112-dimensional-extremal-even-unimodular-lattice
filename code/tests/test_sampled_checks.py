"""The sampled checks (crosscheck/second_impl/minimal_orbits.py, coset_enumeration.py,
supplementary/k8_checks.py; Table D2 [C8], [C11], [C34]) on small examples, and their --help.
抜き取りの検査（crosscheck/second_impl/minimal_orbits.py、coset_enumeration.py、supplementary/k8_checks.py。
表 D2 の [C8]、[C11]、[C34]）を小さな例で試す。あわせて --help。"""
import importlib.util
import itertools
import os

import numpy as np
import pytest

from conftest import CODE, run_python


def load(rel):
    spec = importlib.util.spec_from_file_location(os.path.basename(rel)[:-3], os.path.join(CODE, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("rel", ["crosscheck/second_impl/minimal_orbits.py", "crosscheck/second_impl/coset_enumeration.py",
                                 "supplementary/k8_checks.py"])
def test_help_does_not_start_the_computation(rel):
    # --help prints the usage and stops (it must not start a long run). / --help は使い方を表示して止まる（長い計算を始めない）。
    proc = run_python([os.path.join(CODE, rel), "--help"])
    assert proc.returncode == 0, proc.stdout
    assert "usage:" in proc.stdout


def e8_roots_doubled():
    """The 240 roots of E_8 in orthonormal coordinates, times 2 (integers; norm 8 with the form I).
    正規直交座標での E_8 の根 240 本の 2 倍（整数。形式 I でノルム 8）。"""
    out = []
    for i, j in itertools.combinations(range(8), 2):
        for si, sj in itertools.product((2, -2), repeat=2):
            v = [0] * 8; v[i] = si; v[j] = sj; out.append(v)
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            out.append(list(signs))
    return np.array(out, dtype=np.int64)


def test_design_identities_hold_on_the_e8_roots():
    # The roots of E_8 form a spherical 7-design: the identities of degree 2, 4, 6 hold exactly.
    # E_8 の根は球面 7-デザイン: 次数 2, 4, 6 の恒等式が厳密に成り立つ。
    mo = load("crosscheck/second_impl/minimal_orbits.py")
    V = e8_roots_doubled()
    half = V[[i for i, v in enumerate(V) if v[np.flatnonzero(v)[0]] > 0]]     # one of each +-pair
    assert len(V) == 240 and len(half) == 120
    I8 = np.eye(8, dtype=np.int64)
    rng = np.random.default_rng(1)
    for _ in range(3):
        a = rng.integers(-2, 3, size=8)
        tot = mo.design_sums(half.astype(np.int16), I8, a)
        assert tot == mo.design_values(240, 8, int(a @ a), n=8)
    # A shell with one pair removed and another doubled violates them. / 1 対を落とし別の対を重ねた殻では崩れる。
    bad = np.concatenate([half[1:], half[1:2]])
    a = np.arange(1, 9)
    assert mo.design_sums(bad.astype(np.int16), I8, a) != mo.design_values(240, 8, int(a @ a), n=8)


def test_orbit_expansion_and_disjointness():
    mo = load("crosscheck/second_impl/minimal_orbits.py")
    S = mo.group_mod_sign([np.array([[0, 1], [1, 0]], dtype=np.int64)])           # {I, swap}
    assert len(S) == 2
    sizes, V, disjoint = mo.expand_orbits(np.array([[1, 0], [1, 1]]), S)
    assert sizes == [4, 2] and disjoint and len(V) == 3
    sizes, V, disjoint = mo.expand_orbits(np.array([[1, 0], [0, 1]]), S)          # the same orbit twice
    assert not disjoint
    assert len(mo.group_mod_sign([np.array([[0, 1], [-1, 0]], dtype=np.int64)])) == 2   # order 4, 2 modulo sign


def test_k8_sampling_helpers():
    k8 = load("supplementary/k8_checks.py")
    idx = k8.evenly_spaced(1527984, 3000)
    assert len(idx) == len(set(idx.tolist())) == 3000 and idx.max() < 1527984
    # Two vectors of norm 6 with inner product -2: their sum has norm 8. / ノルム 6、内積 -2 の 2 本の和はノルム 8。
    G = np.array([[6, -2], [-2, 6]], dtype=np.int64)
    I2 = np.eye(2, dtype=np.int64)
    V = k8.sums_of_two_minimal(I2, I2[None].astype(np.int16), I2[None], G, 5, np.random.default_rng(0))
    assert len(V) == 5 and all(int(v @ G @ v) == 8 for v in V)
