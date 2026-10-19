"""P1. The commuting ring M' = End_{SL_2(29)}(L) and the centralizer C (paper §2.4, §4.2).
P1. 可換環 M' = End_{SL_2(29)}(L) と中心化群 C（論文 §2.4、§4.2）。

  * M' = { X in M_56(Z) : X g = g X for g = g1, g2 }: a Z-lattice of rank 8, computed as the
    kernel of a linear system modulo several primes, combined by the Chinese remainder theorem
    and rational reconstruction, and then saturated in Z^(56 x 56). The result is checked exactly.
    M' = { X ∈ M_56(Z) : g = g1, g2 について X g = g X }。階数 8 の Z-格子。いくつかの素数を法とした連立一次方程式の核を
    中国剰余定理と有理数復元でつなぎ、Z^(56×56) の中で飽和させる。結果は厳密に確かめる。
  * C = elements of M' that are isometries of L. On M' the form q(X) = tr(X X*) / 56 with
    X* = G X^T G^{-1} is positive definite and integral, and X is an isometry iff X X* = I, which
    implies q(X) = 1. So C is found among the finitely many X with q(X) = 1 (PARI qfminim, checked complete by exact_qfminim.py) and
    then checked one by one.
    C = M' の元で L の等長変換であるもの。M' 上の形式 q(X) = tr(X X*)/56（X* = G X^T G^{-1}）は正定値で整数値。
    X が等長変換 ⟺ X X* = I で、このとき q(X) = 1。よって C は q(X) = 1 となる有限個の X の中から見つかり、1 つずつ確かめる。
  * Output (never certificates/, whose files are fixed by certificates/SHA256SUMS):
    out/p1/commutant.npz (basis, the Z-basis of M' (8, 56, 56)) and out/p1/centralizer.npz (units, the 6
    elements of C/{+-1} in the order of PARI's qfminim, sign-normalized as returned). They are compared
    with the distributed certificates/commutant.npz (the same Z-lattice: equal Hermite normal forms of the
    8 x 3136 matrices of the two bases) and certificates/centralizer.npz (the same set up to sign; the order
    there is the one used when the certificates were produced). A difference is a failure (exit code 1).
    出力（certificates/ には書かない。そこのファイルは certificates/SHA256SUMS で固定されている）: out/p1/commutant.npz（basis。M' の
    Z-基底 (8, 56, 56)）と out/p1/centralizer.npz（units。C/{±1} の 6 元を PARI の qfminim の順に、返された符号のまま）。配布した
    certificates/commutant.npz とは同じ Z-格子であること（2 つの基底の 8 × 3136 行列の Hermite 標準形が等しいこと）、certificates/centralizer.npz とは
    符号を除いた集合として等しいことを確かめる（そちらの並びは、certificate を作ったときのもの）。違えば失敗（終了コード 1）とする。

Requires SageMath (PARI). Run time: about 10 minutes.
SageMath（PARI）が要る。実行時間: 約 10 分。

Run / 実行:  python3 code/produce/p1_centralizer.py [--data DIR] [--certificates DIR] [--out DIR]
             (with the python3 of an environment that has SageMath / SageMath の入った環境の python3 で)
"""
import argparse
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)                     # exact_qfminim (python -I does not add the script's directory) / python -I はスクリプトの置き場所を加えない
from lib import certs, data, group, require  # noqa: E402
from lib.report import Report  # noqa: E402


def commutant_basis(gens, n):
    """Z-basis of { X in M_n(Z) : X g = g X for all g in gens } (list of Sage integer matrices).
    { X ∈ M_n(Z) : すべての g ∈ gens について X g = g X } の Z-基底（Sage の整数行列のリスト）。"""
    from sage.all import GF, QQ, ZZ, identity_matrix, lcm, matrix, previous_prime

    def kernel_mod(p):
        F = GF(p)
        I = identity_matrix(F, n)
        rows = None
        for g in gens:
            gp = g.change_ring(F)
            # vec(X) row-major: (X g)_ij = sum_k X_ik g_kj, (g X)_ij = sum_k g_ik X_kj.
            # vec(X) は行優先。
            K = I.tensor_product(gp.transpose()) - gp.tensor_product(I)
            rows = K if rows is None else rows.stack(K)
        return rows.right_kernel().basis_matrix().echelon_form()

    p, P, acc, piv = ZZ(2 ** 23), ZZ(1), None, None
    for _ in range(60):
        p = previous_prime(p)
        K = kernel_mod(p).change_ring(ZZ)
        if acc is None:
            acc, P, piv = K, p, K.pivots()
        else:
            require(K.pivots() == piv, "kernel dimension or pivots changed between primes")
            u = P * P.inverse_mod(p)                     # = 0 mod P, = 1 mod p
            acc = (acc + (K - acc) * u) % (P * p)
            P = P * p
        try:
            rows = [[QQ(x.rational_reconstruction(P)) if x else QQ(0) for x in r] for r in acc.rows()]
        except (ArithmeticError, ValueError):
            continue
        cand = [matrix(QQ, n, n, r) for r in rows]
        if all(X * g == g * X for X in cand for g in gens):
            break
    else:
        raise RuntimeError("rational reconstruction did not converge")
    B = matrix(ZZ, [[x * lcm([y.denominator() for y in r]) for x in r] for r in rows]).saturation()
    basis = [matrix(ZZ, n, n, list(r)) for r in B.rows()]
    require(all(X * g == g * X for X in basis for g in gens), "all(X * g == g * X for X in basis for g in gens)")
    return basis


def elements_of_norm(basis, G, N):
    """Elements X of the Z-span of `basis` with q(X) = tr(X X*) / n = N, one of each +-pair
    (PARI qfminim on the Gram matrix of q, checked complete by exact_qfminim.py).
    `basis` の Z-結合 X で q(X) = tr(X X*)/n = N となるもの（± の片方ずつ。q の Gram 行列に PARI の qfminim。exact_qfminim.py で完全性を確かめる）。"""
    from sage.all import QQ, ZZ, matrix
    from exact_qfminim import qfminim_checked
    n = G.nrows()
    Ginv = G.inverse()
    adj = [G * X.transpose() * Ginv for X in basis]
    Q = matrix(QQ, len(basis), len(basis), lambda i, j: (basis[i] * adj[j]).trace())
    require(Q.is_symmetric() and all(x in ZZ for x in Q.list()), "Q.is_symmetric() and all(x in ZZ for x in Q.list())")
    Qz = Q.change_ring(ZZ)
    out = []
    for c in qfminim_checked(Qz, N * n):
        if c * Qz * c == N * n:
            out.append(sum(ci * X for ci, X in zip(c, basis)))
    return out


def main():
    from sage.all import ZZ, matrix
    ap = argparse.ArgumentParser(description="P1: commuting ring and centralizer")
    ap.add_argument("--data", default=None)
    certs.add_arguments(ap)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rep = Report("p1_centralizer", a.out)

    G = matrix(ZZ, data.gram(a.data).tolist())
    gens = [matrix(ZZ, g.tolist()) for g in data.generators(a.data)]
    basis = commutant_basis(gens, 56)
    rep.value("rank of M'", len(basis))
    rep.check("M' has rank 8", len(basis) == 8)
    half = elements_of_norm(basis, G, 1)
    rep.check("every X with q(X) = 1 is an isometry (X X* = I)", all(X * G * X.transpose() == G for X in half))
    rep.value("|C| (both signs)", 2 * len(half))
    rep.check("|C| = 12", len(half) == 6)
    rep.check("C commutes with g1, g2", all(X * g == g * X for X in half for g in gens))
    rep.check("C/{+-1} is closed under multiplication (a group)",
              all(any(X * Y == s * Z for Z in half for s in (1, -1)) for X in half for Y in half))

    pdir = os.path.join(rep.out_dir, "p1")
    os.makedirs(pdir, exist_ok=True)
    Bn = np.array([np.array(X.rows(), dtype=np.int64) for X in basis])
    U = np.array([np.array(X.rows(), dtype=np.int64) for X in half])
    certs.save_npz(os.path.join(pdir, "commutant.npz"), basis=Bn)
    certs.save_npz(os.path.join(pdir, "centralizer.npz"), units=U)
    rep.log(f"wrote {pdir}/commutant.npz and {pdir}/centralizer.npz")

    # Compare with the distributed data. / 配布データと比べる。
    old_basis = certs.load("commutant.npz", "basis", a.certificates).astype(np.int64)
    hnf = lambda M: matrix(ZZ, [[int(v) for v in X.reshape(-1)] for X in M]).echelon_form()   # noqa: E731
    rep.value("basis identical to certificates/commutant.npz (entry by entry)", bool(np.array_equal(Bn, old_basis)))
    rep.check("M' spans the same Z-lattice as certificates/commutant.npz (equal Hermite normal forms)",
              old_basis.shape == Bn.shape and hnf(Bn) == hnf(old_basis))
    old = certs.load("centralizer.npz", "units", a.certificates)
    same = {group.sign_normalize(u).tobytes() for u in U} == {group.sign_normalize(u.astype(np.int64)).tobytes() for u in old}
    rep.check("the same 6 elements up to sign as certificates/centralizer.npz", same)
    rep.finish()


if __name__ == "__main__":
    main()
