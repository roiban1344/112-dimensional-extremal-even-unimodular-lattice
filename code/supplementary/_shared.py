"""Helpers shared by several supplementary scripts (each was previously copied into the scripts that use it).
Not used in the proof of Theorem A. The SageMath functions import Sage only when called, so a numpy-only script
can import this module.
複数の補助スクリプトが共有する関数（以前は使うスクリプトごとに写しがあった）。定理 A の証明には使わない。
SageMath を使う関数は呼ばれたときにだけ Sage を読み込むので、numpy だけのスクリプトもこのモジュールを読み込める。

  parity_preserving_classes  the invertible parity-preserving SL_2(29)-equivariant maps of L/2L and their classes
                             under f -> u f u' (u, u' in C) and inversion (gluings.py, nebe/gluings_m.py, isometry_ab.py)
                             L/2L の可逆で偶奇を保つ SL_2(29) 同変な写像と、f -> u f u'（u, u' ∈ C）と逆元による類
  short_lift                 the first integral lift, by increasing norm, of an element of a class (nebe/gluings_m.py,
                             isometry_ab.py: both must choose the same lift X_A)
                             類の元の整数の持ち上げのうち、ノルムの小さい順で最初のもの（両スクリプトは同じ X_A を選ばなければならない）
  equivariant_isometries     S-equivariant isometries between two lattices in V + V (isometry_ab.py,
                             automorphisms/aut_common.py, genus/genus_steps.py)
                             V ⊕ V の中の 2 つの格子の間の S 同変な等長写像
  word_lifter                integer matrices of group elements through GAP words in the generators
                             (automorphisms/aut_normalizer.py, aut_character.py, nebe/isometry.py)
                             生成元の GAP の語を経由した、群の元の整数行列
  norm8_distributions        inner-product distributions of the norm-8 vectors (+-x, +-v) of a gluing
                             (gluing_b.py, nebe/gluings_m.py)
                             貼り方のノルム 8 のベクトル (±x, ±v) の内積の分布

Import / 読み込み:  from supplementary._shared import ...   (with code/ on sys.path / code/ を sys.path に入れて)
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "produce"))   # p1_centralizer, exact_qfminim
from lib import exact, require  # noqa: E402


def parity_preserving_classes(G, gens, basis):
    """For a lattice with Gram matrix G (Sage, integral, even), the generators gens of SL_2(29) and a Z-basis
    `basis` of the commutant M' (Sage matrices), returns (E, maps, C2, classes):
      E        the F_2-space of the F_2-linear maps of L/2L commuting with gens (kernel of X g - g X);
      maps     its invertible parity-preserving elements (preserving q(x + 2L) = <x, x>/2 mod 2), immutable;
      C2       the distinct reductions mod 2 of the elements of C = { X in M' : q(X) = 1 } (-1 = 1 mod 2);
      classes  the classes of maps under f -> u f u' (u, u' in C2) and f -> f^-1, as sets, in the order in
               which they are found (each started from its least element in the order of f.list()).
    Gram 行列 G（Sage、整数、偶）、SL_2(29) の生成元 gens、可換子 M' の Z-基底 basis について (E, maps, C2, classes) を返す:
      E は gens と可換な L/2L の F_2-線形写像の空間、maps はそのうち可逆で偶奇を保つ（q(x + 2L) = <x,x>/2 mod 2 を保つ）元、
      C2 は C = { X ∈ M' : q(X) = 1 } の元の 2 を法とした相異なる像、classes は f -> u f u'（u, u' ∈ C2）と f -> f^-1 による maps の類
      （集合。見つけた順。各類は f.list() の順で最小の元から作る）。"""
    import itertools
    from p1_centralizer import elements_of_norm
    from sage.all import GF, ZZ, identity_matrix, matrix
    n = G.nrows()
    F2 = GF(2)
    I2 = identity_matrix(F2, n)
    rows = None
    for g in gens:
        g2 = g.change_ring(F2)
        K = I2.tensor_product(g2.transpose()) - g2.tensor_product(I2)       # vec(X g - g X), row-major
        rows = K if rows is None else rows.stack(K)
    E = rows.right_kernel()
    Gb = G.change_ring(F2)
    q0 = [int(G[i, i]) // 2 % 2 for i in range(n)]

    def parity_preserving(f):
        # f preserves the bilinear form mod 2 and q on a basis; then it preserves q everywhere
        # (q(x + y) = q(x) + q(y) + <x, y> mod 2).
        # f が 2 を法とした双線形形式と基底上の q を保てば、q 全体を保つ（q(x+y) = q(x) + q(y) + <x,y>）。
        if f * Gb * f.transpose() != Gb:
            return False
        for i in range(n):
            v = f.row(i).change_ring(ZZ)
            if (v * G * v) // 2 % 2 != q0[i]:
                return False
        return True
    Eb = [matrix(F2, n, n, list(v)) for v in E.basis()]
    maps = []
    for coeffs in itertools.product([0, 1], repeat=len(Eb)):
        f = sum((c * b for c, b in zip(coeffs, Eb)), matrix(F2, n, n))
        if f.is_invertible() and parity_preserving(f):
            f.set_immutable()
            maps.append(f)
    C2 = []
    for X in elements_of_norm(basis, G, 1):
        Xb = X.change_ring(F2)
        Xb.set_immutable()
        if Xb not in C2:
            C2.append(Xb)                                    # -1 = 1 mod 2 / 2 を法として -1 = 1
    todo, classes = set(maps), []
    while todo:
        f0 = min(todo, key=lambda f: tuple(f.list()))
        orb = set()
        for u in C2:
            for v in C2:
                for f in (f0, f0.inverse()):
                    h = u * f * v
                    h.set_immutable()
                    orb.add(h)
        classes.append(orb)
        todo -= orb
    return E, maps, C2, classes


def short_lift(basis, G, cls, max_norm=7):
    """(Y, q): the first element Y of M' (spanned by `basis`), by increasing norm q = 1, ..., max_norm and in the
    order of p1_centralizer.elements_of_norm (PARI qfminim) within a norm, whose reduction mod 2 lies in the set
    `cls`; (None, None) if there is none.
    `cls` に 2 を法とした像が入る M' の元 Y のうち、ノルム q = 1, …, max_norm の小さい順、同じノルムでは
    p1_centralizer.elements_of_norm（PARI の qfminim）の順で最初のものと、その q。無ければ (None, None)。"""
    from p1_centralizer import elements_of_norm
    from sage.all import GF
    F2 = GF(2)
    for q in range(1, max_norm + 1):
        for Y in elements_of_norm(basis, G, q):
            Yb = Y.change_ring(F2)
            Yb.set_immutable()
            if Yb in cls:
                return Y, q
    return None, None


def equivariant_isometries(BX, GX, BY, GY, comm, rep=None, label=""):
    """S-equivariant isometries X -> Y between two lattices of rank 2n in the same rational space V + V, with
    bases BX, BY (rational rows) and Gram matrices GX, GY (integral, GX unimodular), S acting diagonally and
    comm a basis of End_S(V) (n x n matrices). The S-equivariant maps are T = BX Phi BY^-1 with
    Phi = [[a, b], [c, d]], a, b, c, d in span(comm). On the Z-lattice H of the integral T (dual to the Z-span
    of the coefficient rows, one row per matrix entry), Q(T) = tr(GX^-1 T GY T^T) is positive definite and
    equals 2n on isometries, so all T with Q(T) <= 2n are enumerated (produce/exact_qfminim.qfminim_checked,
    checked complete) and T GY T^T = GX is tested exactly.
    Returns (isos, number of candidates with Q <= 2n up to sign, dimension 4 len(comm)); the isometries are
    up to sign, with rows of T = the basis of X written in the basis of Y. With a Report `rep`, the full rank of
    the coefficient rows and the positive definiteness of Q are recorded by rep.check (prefixed by `label`);
    without, they are guards (require).
    同じ有理空間 V ⊕ V の中の階数 2n の 2 つの格子（基底 BX, BY は有理数の行、Gram 行列 GX, GY は整数で GX はユニモジュラー）の間の
    S 同変な等長写像。S は対角に作用し、comm は End_S(V) の基底（n × n 行列）。S 同変な写像は T = BX Phi BY^-1
    （Phi = [[a, b], [c, d]]、a, b, c, d ∈ span(comm)）。整数の T の Z-格子 H（成分ごとの係数の行の Z-スパンの双対）の上で
    Q(T) = tr(GX^-1 T GY T^T) は正定値で、等長写像では 2n。Q(T) ≤ 2n の T をすべて列挙し（qfminim_checked で完全性を確かめる）、
    T GY T^T = GX を厳密に確かめる。(等長写像（符号を除く。T の行は X の基底を Y の基底で書いたもの）, Q ≤ 2n の候補の数, 次元) を返す。
    Report の rep を渡すと、係数の行が階数いっぱいであることと Q が正定値であることを rep.check で記録する（見出しに label を前置する）。
    渡さなければ、これらは保証の検査（require）になる。"""

    def guard(cond, msg):
        if rep is None:
            require(cond, msg)
        else:
            rep.check(label + msg, cond)
    from exact_qfminim import qfminim_checked
    from sage.all import QQ, ZZ, block_matrix, lcm, matrix, zero_matrix
    n = comm[0].nrows()
    BYi = BY.inverse()
    Zq = zero_matrix(QQ, n, n)
    gens = []
    for t in comm:
        for pos in range(4):
            blocks = [[Zq, Zq], [Zq, Zq]]
            blocks[pos // 2][pos % 2] = t.change_ring(QQ)
            gens.append(BX * block_matrix(QQ, blocks, subdivide=False) * BYi)
    k = len(gens)
    # H is dual to the Z-span of the coefficient rows (one row per matrix entry).
    # H は係数の行（行列の成分ごとに 1 行）の Z-スパンの双対。
    rows = {tuple(col) for col in zip(*[g.list() for g in gens])}
    rows.discard(tuple([QQ(0)] * k))
    rows = [list(r) for r in rows]
    d = lcm([QQ(x).denominator() for r in rows for x in r])
    span = matrix(ZZ, 0, k)
    for i in range(0, len(rows), 200):           # add rows in chunks to keep the HNF small / HNF を小さく保つため少しずつ足す
        span = span.stack(matrix(ZZ, [[int(d * x) for x in r] for r in rows[i:i + 200]])).hermite_form(include_zero_rows=False)
    guard(span.nrows() == k, f"the coefficient rows span a lattice of full rank {k}")
    Hb = (span.change_ring(QQ) / d).inverse().transpose()                    # rows: a basis of H / 行が H の基底
    Ts = []
    for row in Hb.rows():
        T = sum(c * g for c, g in zip(row, gens))
        require(all(x in ZZ for x in T.list()), "a basis element of H is not integral")
        Ts.append(T.change_ring(ZZ))
    GXi = GX.inverse()
    require(all(x in ZZ for x in GXi.list()), "G_X is not unimodular")
    GXi = GXi.change_ring(ZZ)
    Ys = [GXi * T * GY for T in Ts]
    Q = matrix(ZZ, [Y.list() for Y in Ys]) * matrix(ZZ, [T.list() for T in Ts]).transpose()
    Q = Q + Q.transpose()                                                    # 2 Q, integral / 2Q（整数）
    guard(Q.is_positive_definite(), "Q(T) = tr(G_X^-1 T G_Y T^T) is positive definite on H")
    cands = qfminim_checked(Q, 2 * GX.nrows())
    isos = [T for T in (sum(ci * Ti for ci, Ti in zip(c, Ts)) for c in cands) if T * GY * T.transpose() == GX]
    return isos, len(cands), k


def word_lifter(epi, gens):
    """A function sending an element of the GAP group image of `epi` (an epimorphism from a free group onto a
    group generated by the images of gens) to the integer matrix obtained by writing it as a word in the
    generators (PreImagesRepresentative) and multiplying out the integer matrices gens (Sage, invertible over Z).
    The caller checks the result where it matters (e.g. modulo p).
    epi（自由群から、gens の像が生成する群への全射）の像の元を、生成元の語で書いて（PreImagesRepresentative）整数行列 gens（Sage、Z 上で可逆）
    を掛け、整数行列にする関数を返す。必要な箇所では呼び出し側が結果を（例えば p を法として）確かめる。"""
    from sage.all import ZZ, identity_matrix, libgap
    gens = [g.change_ring(ZZ) for g in gens]
    invs = [g.inverse().change_ring(ZZ) for g in gens]
    n = gens[0].nrows()

    def lift(elt):
        word = libgap.LetterRepAssocWord(libgap.PreImagesRepresentative(epi, elt)).sage()
        A = identity_matrix(ZZ, n)
        for e in word:
            A = A * (gens[e - 1] if e > 0 else invs[-e - 1])
        return A
    return lift


def norm8_distributions(pairs, S, G):
    """Inner-product distributions of the norm-8 vectors z = (x, v)/sqrt2 of a gluing, given one pair (x, v)
    per S-orbit (numpy integer rows; S the 12,180 elements of SL_2(29)/{+-1}, G the Gram matrix of L). The
    vectors are (+-x s, +-v s) over s in S; returns (number of distinct vectors, {distribution: blocks}), where
    each block of len(S) vectors contributes the distribution of <z0, z> = (<x0, x> + <v0, v>)/2 over all z for
    its first vector z0 (float64: the products with G are checked exact by lib.exact; the inner products are
    small integers).
    貼り方のノルム 8 のベクトル z = (x, v)/√2 の内積の分布。S-軌道ごとに 1 組の (x, v)（numpy の整数の行。S は SL_2(29)/{±1} の
    12,180 元、G は L の Gram 行列）を与える。ベクトルは s ∈ S にわたる (±x s, ±v s)。(相異なるベクトルの数, {分布: ブロック数}) を返す。
    len(S) 本ずつのブロックごとに、その最初のベクトル z0 との <z0, z> = (<x0,x> + <v0,v>)/2 の分布を数える（float64。G との積が厳密であることは
    lib.exact で確かめる。内積は小さな整数）。"""
    S64 = S.astype(np.int64)
    XS, VS = [], []
    for x, v in pairs:
        xg, vg = np.einsum("j,gjk->gk", x, S64), np.einsum("j,gjk->gk", v, S64)
        for sx in (1, -1):
            for sv in (1, -1):
                XS.append(sx * xg)
                VS.append(sv * vg)
    XS, VS = np.concatenate(XS), np.concatenate(VS)
    ndistinct = len(np.unique(np.concatenate([XS, VS], axis=1), axis=0))
    XG, VG = exact.f64_matmul(XS, G).astype(np.float64), exact.f64_matmul(VS, G).astype(np.float64)
    dists = {}
    for i0 in range(0, len(XS), len(S)):
        ip = np.rint((XG @ XS[i0] + VG @ VS[i0]) / 2).astype(np.int64)      # <z0, z> = (1/2)(<x0,x> + <v0,v>)
        vals, cnt = np.unique(ip, return_counts=True)
        key = str(list(zip(vals.tolist(), cnt.tolist())))
        dists[key] = dists.get(key, 0) + 1
    return ndistinct, dists
