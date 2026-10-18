"""check of supplementary/genus/genus.py: numpy only, integer arithmetic (see the docstring of genus.py). This is the
step run in CI; it reads only the distributed files.
supplementary/genus/genus.py の check: numpy のみ、整数演算（genus.py の docstring を参照）。CI で走る段で、配布ファイルだけを読む。
"""
import os
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from genus_data import (CLASSES_FILE, ISO3_FILE, ISO7_FILE, LABELS, MASS, N, NCLASS, NX, STATUS, WITNESS_CLASSES,  # noqa: E402
                        WITNESS_FILE, gram_file, read_basis)
from lib import certs, data, exact  # noqa: E402
from lib.report import Report  # noqa: E402

def mm(A, B):
    """Exact integer product: int64 with the overflow guard of lib/exact.py when it applies, Python integers
    otherwise. / 厳密な整数の積: lib/exact.py の上界が成り立てば int64、そうでなければ Python の整数。"""
    if exact.partial_sum_bound(A, B) < 2 ** 62:
        return exact.i64_matmul(A, B)
    return np.asarray(A, dtype=object) @ np.asarray(B, dtype=object)


def check(a):
    rep = Report("s25_genus_check", a.out)
    cdir = a.certificates
    G = data.gram(a.data).astype(np.int64)
    gens = data.generators(a.data).astype(np.int64)
    tau = data.tau(a.data).astype(np.int64)
    Zn = np.zeros((N, N), dtype=np.int64)
    GG = np.block([[G, Zn], [Zn, G]])
    gg = [np.block([[g, Zn], [Zn, g]]) for g in gens]
    # the reported orders and the mass / 報告した位数と質量
    tab = data.read_integers(certs.path_checked(CLASSES_FILE, cdir)).reshape(-1, 9)
    rep.check("genus_classes.txt lists the classes 0-7", [int(t) for t in tab[:, 0]] == list(range(NCLASS)))
    orders = [int(t) for t in tab[:, 1]]
    rep.value("|U(Lambda_j)|, j = 0..7 (as reported by PARI qfauto in enum)", orders)
    rep.check("the orders are those of the paper: 1152, 12, 288, 24, 24, 20, 288, 48",
              orders == [LABELS[j][0] for j in range(NCLASS)])
    total = sum(Fraction(1, u) for u in orders)
    rep.value("sum_j 1/|U(Lambda_j)| (exact)", str(total))
    rep.check("sum_j 1/|U(Lambda_j)| = 157/640 = 2^-4 |zeta_K(-1) zeta_K(-3)|, the mass (this checks the sum, not the orders)",
              total == MASS)
    # the eight lattices / 8 つの格子
    GX, SX = {}, {}
    for j in range(NCLASS):
        Gx = certs.load_matrix(gram_file(j), NX, cdir).astype(np.int64)
        GX[j] = Gx
        rep.check(f"class {j}: G_X symmetric and even", (Gx == Gx.T).all() and (np.diag(Gx) % 2 == 0).all())
        rep.check(f"class {j}: det G_X = 1 (Bareiss)", exact.det_bareiss(Gx) == 1)
        d, D = read_basis(j, cdir)
        lhs = mm(mm(D, GG), D.T)
        rep.check(f"class {j}: D diag(G, G) D^T = 2 d^2 G_X (d = {d})", (np.asarray(lhs, dtype=object) == 2 * d * d * Gx.astype(object)).all())
        Gi = exact.inverse_unimodular(Gx)
        SX[j] = []
        for k, g in enumerate(gg):
            num = mm(mm(mm(mm(D, g), GG), D.T), Gi)                       # D g diag(G,G) D^T G_X^-1 = 2 d^2 s
            num = np.asarray(num, dtype=object)
            ok = all(int(t) % (2 * d * d) == 0 for t in num.flat)
            s = np.array([[int(t) // (2 * d * d) for t in r] for r in num], dtype=np.int64) if ok else None
            ok = ok and (mm(s, D) == mm(D, g)).all() and (mm(mm(s, Gx), s.T) == Gx).all()
            rep.check(f"class {j}: g{k + 1} acts on X_j: s = D diag(g, g) D^-1 is integral, s D = D diag(g, g), s G_X s^T = G_X", ok)
            SX[j].append(s)
        rep.value(f"class {j}: max |G_X|, max |D|, smallest diagonal entry of G_X", [int(np.abs(Gx).max()), int(np.abs(D).max()),
                                                                                    int(np.diag(Gx).min())])
    # witnesses / 証拠
    W = data.read_integers(certs.path_checked(WITNESS_FILE, cdir)).reshape(-1, 1 + NX)
    have = []
    for row in W:
        j, v = int(row[0]), row[1:].astype(np.int64)
        nv = int(mm(mm(v[None, :], GX[j]), v[:, None])[0, 0])
        rep.check(f"class {j}: the witness v has v G_X v^T = 8", nv == 8)
        have.append(j)
    rep.value("classes with a norm-8 witness", sorted(have))
    rep.check("witnesses for classes 3, 4, 5", set(WITNESS_CLASSES) <= set(have))
    rep.value("status of the minimum norm per class (as in Table S10; [witness]: a norm-8 vector checked above)", {j: STATUS[j] + (" [witness]" if j in have else "") for j in range(NCLASS)})
    # isometries / 等長写像
    GR = data.gram_R(G, tau)
    T7 = certs.load_matrix(ISO7_FILE, NX, cdir).astype(np.int64)
    rep.check("class 7 -> L_112: T G_R T^T = G_7 (G_R = (3.1) from data/)", (mm(mm(T7, GR), T7.T) == GX[7]).all())
    d7 = exact.det_bareiss(T7)
    rep.check(f"class 7 -> L_112: det T = +-1 ({d7})", abs(d7) == 1)
    ok = all((mm(s, T7) == mm(T7, g)).all() for s, g in zip(SX[7], gg))
    rep.check("class 7 -> L_112: T commutes with SL_2(29) (s T = T diag(g, g) for g1, g2)", ok)
    GA = certs.load_matrix("gram_A.txt", NX, cdir).astype(np.int64)
    T3 = certs.load_matrix(ISO3_FILE, NX, cdir).astype(np.int64)
    rep.check("class 3 -> gluing A: T G_A T^T = G_3 (G_A = certificates/gram_A.txt)", (mm(mm(T3, GA), T3.T) == GX[3]).all())
    d3 = exact.det_bareiss(T3)
    rep.check(f"class 3 -> gluing A: det T = +-1 ({d3})", abs(d3) == 1)
    rep.finish()
