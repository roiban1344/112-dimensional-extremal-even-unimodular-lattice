"""S24. Gluings A and B are isometric (paper §3.3, Supplement §S5; Table D2 [C28]). Not used in the proof
of Theorem A.
S24. 貼り方 A と B は等長同型（論文 §3.3、補遺 §S5。表 D2 の [C28]）。定理 A の証明には使わない。

Gluing A is L_f for Nebe's L_{56,2}(M) (centralizer order 24) and f in the class of 48 maps that contains no
element of C, with the same integral lift X_A of f as in supplementary/nebe/gluings_m.py; gluing B is L_B for
L = data/L56_gram.txt and tau_B = tau_class_B of certificates/negative_control_B.npz (supplementary/gluing_b.py).
Gram matrices (both in the basis (3.1), rows (e_i, e_i X), (0, 2 e_i), divided by sqrt2):
  G_A = [[I, X_A], [0, 2I]] diag(G_M, G_M) [[I, X_A], [0, 2I]]^T / 2,   G_M = Gram matrix of L_{56,2}(M) in the
        LLL-reduced basis of supplementary/nebe/lattices.py (load(..., reduce=True));
  G_B = [[I, tau_B], [0, 2I]] diag(G, G) [[I, tau_B], [0, 2I]]^T / 2 = [[3G, tau_B G], [(tau_B G)^T, 2G]].
Convention: T is a 112 x 112 integer matrix whose rows are the images of the basis of gluing A, written in the
basis of gluing B; T G_B T^T = G_A and det T = +-1.
貼り方 A は、Nebe の L_{56,2}(M)（中心化群の位数 24）と、C の元を含まない大きさ 48 の類の f についての L_f（f の整数の持ち上げ X_A は
supplementary/nebe/gluings_m.py と同じ）。貼り方 B は、L = data/L56_gram.txt と tau_B = certificates/negative_control_B.npz の tau_class_B
についての L_B（supplementary/gluing_b.py）。Gram 行列はどちらも基底 (3.1)（行 (e_i, e_i X), (0, 2 e_i) を √2 で割る）で上の式。
規約: T は 112 × 112 の整数行列で、行は貼り方 A の基底の像を貼り方 B の基底で書いたもの。T G_B T^T = G_A、det T = ±1。

  find   (SageMath; uses out/nebe/M_* from nebe/lattices.py and out/nebe/embedding_L_into_M.txt from
         nebe/reduction_to_nebe.py). By the embedding e: L -> L_{56,2}(M) (e(L) = L_{56,2}(M) X + 2 L_{56,2}(M),
         <e x, e y> = 2 <x, y>, SL_2(29)-equivariant), both gluings lie in the same rational space V + V,
         V = L_{56,2}(M) tensor Q, invariant under the same group S acting diagonally. The S-equivariant
         linear maps V + V -> V + V are the block matrices [[a, b], [c, d]], a, b, c, d in M'(L_{56,2}(M)) tensor Q
         (32-dimensional); in the bases of the two gluings they are T = B_A Phi B_B^{-1}. On the Z-lattice H of
         those T that are integral, Q(T) = tr(G_A^{-1} T G_B T^T) is positive definite and equals 112 on
         isometries; all T with Q(T) <= 112 are enumerated (qfminim, checked complete by produce/exact_qfminim.py)
         and T G_B T^T = G_A is tested exactly. Writes certificates/isometry_AB.txt (T) and
         certificates/gram_A.txt (G_A).
         SageMath。埋め込み e: L -> L_{56,2}(M)（e(L) = L_{56,2}(M) X + 2 L_{56,2}(M)、<e x, e y> = 2<x, y>、SL_2(29) 同変）により、二つの貼り方は
         同じ有理空間 V ⊕ V の中にあり、対角に作用する同じ群 S で不変。S 同変な線形写像は M'(L_{56,2}(M))⊗Q を成分とするブロック行列（32 次元）で、
         二つの貼り方の基底では T = B_A Phi B_B^{-1}。そのうち整数の T の Z-格子 H の上で Q(T) = tr(G_A^{-1} T G_B T^T) は正定値で、
         等長写像では 112。Q(T) ≤ 112 の T をすべて列挙し（qfminim。exact_qfminim.py で完全性を確かめる）、T G_B T^T = G_A を厳密に確かめる。
         certificates/isometry_AB.txt（T）と certificates/gram_A.txt（G_A）を書く。
  check  (numpy only, integer arithmetic). Rebuilds G_B from data/L56_gram.txt and tau_class_B (checking
         tau_B^2 = -5, tau_B commutes with SL_2(29), G_B even of determinant 1), reads G_A from
         certificates/gram_A.txt and T from certificates/isometry_AB.txt, and checks T G_B T^T = G_A,
         det T = +-1 (Bareiss), and that G_A is symmetric, even, of determinant 1. G_A itself is built from
         L_{56,2}(M), which needs SageMath (find), so check takes it as data.
         numpy のみ、整数演算。data/L56_gram.txt と tau_class_B から G_B を作り直し（tau_B^2 = -5、SL_2(29) と可換、G_B が偶で行列式 1 を確かめる）、
         certificates/gram_A.txt の G_A と certificates/isometry_AB.txt の T を読んで、T G_B T^T = G_A、det T = ±1（Bareiss）、G_A が対称・偶・
         行列式 1 であることを確かめる。G_A は L_{56,2}(M) から作るので SageMath が要り（find）、check はそれをデータとして受け取る。

Run time: find about 8 minutes (SageMath), check a few seconds. Memory: find about 3 GB.
実行時間: find 約 8 分（SageMath）、check 数秒。メモリ: find 約 3 GB。
Run / 実行:  sage -python code/supplementary/isometry_ab.py find
             python3 code/supplementary/isometry_ab.py check
"""
import argparse
import itertools
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "nebe"))
sys.path.insert(0, os.path.join(HERE, "..", "produce"))
from lib import certs, data, exact  # noqa: E402
from lib.report import Report  # noqa: E402

N = 56
T_FILE = "isometry_AB.txt"
GA_FILE = "gram_A.txt"


def lift_class_A(Gs, gens_s, rep):
    """The integral lift X_A in M'(L_{56,2}(M)) of an element of the class of size 48, chosen exactly as in
    nebe/gluings_m.py (c): the first element, in qfminim order and by increasing norm, whose reduction lies
    in the class. / 大きさ 48 の類の元の整数の持ち上げ X_A。nebe/gluings_m.py (c) と同じ選び方。"""
    from sage.all import GF, ZZ, identity_matrix, matrix
    from p1_centralizer import commutant_basis, elements_of_norm
    n = N
    F2 = GF(2)
    basis = commutant_basis(gens_s, n)
    I2 = identity_matrix(F2, n)
    rows = None
    for g in gens_s:
        g2 = g.change_ring(F2)
        Kx = I2.tensor_product(g2.transpose()) - g2.tensor_product(I2)
        rows = Kx if rows is None else rows.stack(Kx)
    E = rows.right_kernel()
    Gb = Gs.change_ring(F2)
    q0 = [int(Gs[i, i]) // 2 % 2 for i in range(n)]

    def parity_preserving(f):
        if f * Gb * f.transpose() != Gb:
            return False
        return all((f.row(i).change_ring(ZZ) * Gs * f.row(i).change_ring(ZZ)) // 2 % 2 == q0[i] for i in range(n))
    Eb = [matrix(F2, n, n, list(v)) for v in E.basis()]
    maps = []
    for coeffs in itertools.product([0, 1], repeat=8):
        f = sum((c * b for c, b in zip(coeffs, Eb)), matrix(F2, n, n))
        if f.is_invertible() and parity_preserving(f):
            f.set_immutable()
            maps.append(f)
    C2 = []
    for Y in elements_of_norm(basis, Gs, 1):
        Yb = Y.change_ring(F2)
        Yb.set_immutable()
        if Yb not in C2:
            C2.append(Yb)
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
    info = sorted(((len(o), any(u in o for u in C2)) for o in classes))
    rep.check("the 60 invertible parity-preserving maps form two classes: 12 (containing C) and 48 (gluing A)",
              len(maps) == 60 and info == [(12, True), (48, False)])
    clsA = next(o for o in classes if len(o) == 48)
    for Nq in range(1, 8):
        for Y in elements_of_norm(basis, Gs, Nq):
            Yb = Y.change_ring(F2)
            Yb.set_immutable()
            if Yb in clsA:
                rep.value("norm q of the lift X_A", Nq)
                return Y, basis
    return None, basis


def find(a):
    from sage.all import QQ, ZZ, block_matrix, identity_matrix, lcm, matrix, zero_matrix
    from exact_qfminim import qfminim_checked
    from lattices import load, read_mats
    rep = Report("s24_isometry_ab_find", a.out)
    n = N
    Gs, gens_s = load("M", rep.out_dir, reduce=True)               # same basis as gluings_m.py / gluings_m.py と同じ基底
    G = matrix(ZZ, data.gram(a.data).tolist())
    g1, g2 = [matrix(ZZ, g.tolist()) for g in data.generators(a.data)]
    Emb = read_mats(os.path.join(rep.out_dir, "nebe", "embedding_L_into_M.txt"), n)[0]
    rep.check("the embedding e (rows: e(basis of L) in L_{56,2}(M)) satisfies Emb G_M Emb^T = 2 G", Emb * Gs * Emb.transpose() == 2 * G)
    Embi = Emb.change_ring(QQ).inverse()
    rep.check("e(L) is invariant under z, w of L_{56,2}(M): Emb h Emb^-1 is integral",
              all(all(c in ZZ for c in (Emb * h * Embi).list()) for h in gens_s))
    tB = matrix(ZZ, certs.load("negative_control_B.npz", "tau_class_B", a.certificates).tolist())
    I, Z = identity_matrix(ZZ, n), zero_matrix(ZZ, n, n)
    rep.check("tau_B^2 = -5 and tau_B commutes with g1, g2", tB * tB == -5 * I and tB * g1 == g1 * tB and tB * g2 == g2 * tB)
    hL = [(Emb * h * Embi).change_ring(ZZ) for h in gens_s]          # z, w of L_{56,2}(M) acting on L / L 上に移した z, w
    rep.check("the transported generators are isometries of L commuting with tau_B",
              all(h * G * h.transpose() == G and h * tB == tB * h for h in hL))

    XA, basis = lift_class_A(Gs, gens_s, rep)
    rep.check("an integral lift X_A of an element of the class of size 48", XA is not None)
    BA = block_matrix(ZZ, [[I, XA], [Z, 2 * I]], subdivide=False)
    GA = BA * block_matrix(ZZ, [[Gs, Z], [Z, Gs]], subdivide=False) * BA.transpose() / 2
    rep.check("G_A is integral, even, of determinant 1",
              all(c in ZZ for c in GA.list()) and all(GA[i, i] % 2 == 0 for i in range(2 * n)) and GA.det() == 1)
    GA = GA.change_ring(ZZ)
    BL = block_matrix(ZZ, [[I, tB], [Z, 2 * I]], subdivide=False)
    GB = (BL * block_matrix(ZZ, [[G, Z], [Z, G]], subdivide=False) * BL.transpose() / 2).change_ring(ZZ)
    rep.check("G_B = [[3G, tau_B G], [(tau_B G)^T, 2G]], determinant 1",
              GB == block_matrix(ZZ, [[3 * G, tB * G], [(tB * G).transpose(), 2 * G]], subdivide=False) and GB.det() == 1)
    # Gluing B in V + V: rows (e(e_i), e(e_i tau_B)), (0, 2 e(e_i)), ambient form diag(G_M, G_M) / 4.
    # 貼り方 B を V ⊕ V の中で: 行 (e(e_i), e(e_i tau_B)), (0, 2 e(e_i))、周囲の形式は diag(G_M, G_M)/4。
    BB = block_matrix(ZZ, [[Emb, tB * Emb], [Z, 2 * Emb]], subdivide=False)
    D = block_matrix(ZZ, [[Gs, Z], [Z, Gs]], subdivide=False)
    rep.check("B_B diag(G_M, G_M) B_B^T / 4 = G_B", BB * D * BB.transpose() == 4 * GB)
    BBi = BB.change_ring(QQ).inverse()
    BAq = BA.change_ring(QQ)

    # The 32 equivariant maps T_k = B_A Phi_k B_B^{-1}. / 32 個の同変写像。
    Zq = zero_matrix(QQ, n, n)
    gens = []
    for t in basis:
        for pos in range(4):
            blocks = [[Zq, Zq], [Zq, Zq]]
            blocks[pos // 2][pos % 2] = t.change_ring(QQ)
            gens.append(BAq * block_matrix(QQ, blocks, subdivide=False) * BBi)
    k = len(gens)
    rep.value("dimension of the S-equivariant maps", k)
    rows = {tuple(col) for col in zip(*[g.list() for g in gens])}
    rows.discard(tuple([QQ(0)] * k))
    rows = [list(r) for r in rows]
    d = lcm([QQ(x).denominator() for r in rows for x in r])
    span = matrix(ZZ, 0, k)
    for i in range(0, len(rows), 200):
        span = span.stack(matrix(ZZ, [[int(d * x) for x in r] for r in rows[i:i + 200]])).hermite_form(include_zero_rows=False)
    rep.check("the coefficient rows span a lattice of full rank 32", span.nrows() == k)
    Hb = (span.change_ring(QQ) / d).inverse().transpose()
    Xs = []
    for row in Hb.rows():
        X = sum(c * g for c, g in zip(row, gens))
        assert all(x in ZZ for x in X.list())
        Xs.append(X.change_ring(ZZ))
    GAi = GA.inverse().change_ring(ZZ)
    Ys = [GAi * X * GB for X in Xs]
    Q = matrix(ZZ, [Y.list() for Y in Ys]) * matrix(ZZ, [X.list() for X in Xs]).transpose()
    Q = Q + Q.transpose()                                            # 2 Q / 2Q
    rep.check("Q(T) = tr(G_A^-1 T G_B T^T) is positive definite on H", Q.is_positive_definite())
    cands = qfminim_checked(Q, 2 * 2 * N)
    isos = [X for X in (sum(ci * Xi for ci, Xi in zip(c, Xs)) for c in cands) if X * GB * X.transpose() == GA]
    rep.value("integral equivariant maps with Q <= 112 (up to sign), isometries among them", [len(cands), len(isos)])
    rep.check("there is an S-equivariant isometry from gluing A onto gluing B", len(isos) > 0)
    T = min(isos, key=lambda X: (max(abs(x) for x in X.list()), sum(abs(x) for x in X.list())))
    rep.check("T G_B T^T = G_A and det T = +-1", T * GB * T.transpose() == GA and abs(T.det()) == 1)
    sA = [BA * block_matrix(QQ, [[h, Zq], [Zq, h]], subdivide=False) * BA.inverse() for h in gens_s]
    sB = [BL * block_matrix(QQ, [[h, Zq], [Zq, h]], subdivide=False) * BL.inverse() for h in hL]
    rep.check("T intertwines the actions of S: s_A T = T s_B for the generators", all(x * T == T * y for x, y in zip(sA, sB)))
    rep.value("max |entry| of T", max(abs(x) for x in T.list()))

    cdir = a.certificates or certs.DEFAULT_DIR
    Tn = np.array(T.rows(), dtype=np.int64)
    GAn = np.array(GA.rows(), dtype=np.int64)
    certs.save_matrix(os.path.join(cdir, T_FILE), Tn,
                      "T (112 x 112): T G_B T^T = G_A, det T = +-1 (rows: basis of gluing A in the basis of gluing B).\n"
                      "G_B = [[3G, tau_B G], [(tau_B G)^T, 2G]], G = data/L56_gram.txt, tau_B = tau_class_B of negative_control_B.npz;\n"
                      "G_A = certificates/gram_A.txt. T is SL_2(29)-equivariant. Found by code/supplementary/isometry_ab.py find.\n"
                      "T（112 × 112）: T G_B T^T = G_A、det T = ±1（行は貼り方 A の基底を貼り方 B の基底で書いたもの）。SL_2(29) 同変。")
    certs.save_matrix(os.path.join(cdir, GA_FILE), GAn,
                      "G_A (112 x 112): Gram matrix of gluing A, G_A = [[I, X_A], [0, 2I]] diag(G_M, G_M) [[I, X_A], [0, 2I]]^T / 2,\n"
                      "G_M = Gram matrix of Nebe's L_{56,2}(M) (centralizer order 24) in the LLL-reduced basis of\n"
                      "code/supplementary/nebe/lattices.py (load(..., reduce=True)), X_A in M'(L_{56,2}(M)) the lift of an element of the\n"
                      "class of 48 maps chosen as in code/supplementary/nebe/gluings_m.py. Written by code/supplementary/isometry_ab.py find.\n"
                      "G_A（112 × 112）: 貼り方 A の Gram 行列（Nebe の L_{56,2}(M) と大きさ 48 の類の f の持ち上げ X_A から）。")
    rep.log(f"wrote {cdir}/{T_FILE} and {cdir}/{GA_FILE}")
    rep.finish()


def check(a):
    rep = Report("s24_isometry_ab_check", a.out)
    mm = exact.i64_matmul
    n2 = 2 * N
    G = data.gram(a.data)
    gens = data.generators(a.data)
    tB = certs.load("negative_control_B.npz", "tau_class_B", a.certificates).astype(np.int64)
    I = np.eye(N, dtype=np.int64)
    rep.check("tau_B^2 = -5 I, tau_B G tau_B^T = 5 G, tau_B commutes with g1, g2",
              (mm(tB, tB) == -5 * I).all() and (mm(mm(tB, G), tB.T) == 5 * G).all()
              and all((mm(g, tB) == mm(tB, g)).all() for g in gens))
    GB = data.gram_R(G, tB)
    rep.check("G_B = [[3G, tau_B G], [(tau_B G)^T, 2G]] is symmetric, even, of determinant 1",
              (GB == GB.T).all() and (np.diag(GB) % 2 == 0).all() and exact.det_bareiss(GB) == 1)
    GA = certs.load_matrix(GA_FILE, n2, a.certificates)
    T = certs.load_matrix(T_FILE, n2, a.certificates)
    rep.value("max |entry| of T, of G_A", [int(np.abs(T).max()), int(np.abs(GA).max())])
    rep.check("G_A is symmetric and even", (GA == GA.T).all() and (np.diag(GA) % 2 == 0).all())
    rep.check("T G_B T^T = G_A (int64, overflow-checked)", (mm(mm(T, GB), T.T) == GA).all())
    dT = exact.det_bareiss(T)
    rep.value("det T", dT)
    rep.check("det T = +-1", abs(dT) == 1)
    rep.check("det G_A = 1 (Bareiss), so G_A is even unimodular", exact.det_bareiss(GA) == 1)
    rep.finish()


def main():
    ap = argparse.ArgumentParser(description="S24: an explicit isometry between gluings A and B")
    ap.add_argument("mode", choices=["find", "check"])
    ap.add_argument("--data", default=None)
    ap.add_argument("--certificates", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    (find if a.mode == "find" else check)(a)


if __name__ == "__main__":
    main()
