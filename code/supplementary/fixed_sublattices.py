"""S14. Fixed sublattices of elements of order 3, 5, 7 of SL_2(29) in L_112, and BKZ on L_112 (supplement §S3.5;
Table D2 [C18]). These are consistency tests that are NOT evidence for extremality (they cannot tell
gluing B from gluing C); they are not used in the proof of Theorem A.
S14. L_112 における SL_2(29) の位数 3, 5, 7 の元の固定部分格子と、L_112 への BKZ（補遺 §S3.5。表 D2 の [C18]）。極値性の証拠に**ならない**整合性の検査
（貼り方 B と C を区別できない）。定理 A の証明には使わない。

For an element h of prime order p, the fixed sublattice L_112^h = { z in L_112 : z diag(h, h) = z } is computed
exactly (kernel over Q, saturated in Z^112). Its dimension and determinant are exact, and its minimum m is
established exactly: a vector of norm m is exhibited (found by PARI, its norm checked in integers), and the
enumeration that cannot miss vectors (verify/enum_interval.c) finds no nonzero vector of norm <= m - 2.
Checked against the paper: dimensions 32, 16, 16, determinants 3^32, 5^16, 7^16, minima 12, 10, 14. The
order-5 section contains vectors of norm 10, so min L_112 <= 10.
素数位数 p の元 h について、固定部分格子 L_112^h を厳密に求める（Q 上の核、Z^112 で飽和）。次元と行列式は厳密で、最小 m も厳密に決める:
ノルム m のベクトルを示し（PARI で見つけ、ノルムを整数で確かめる）、取りこぼしの無い列挙（verify/enum_interval.c）でノルム m - 2 以下の
0 でないベクトルが無いことを確かめる。論文の値（次元 32, 16, 16、行列式 3^32, 5^16, 7^16、最小 12, 10, 14）と照合する。位数 5 の固定部分格子は
ノルム 10 のベクトルを含むので min L_112 ≤ 10。

With --tau B the same is done for the negative control B (tau_class_B from certificates/negative_control_B.npz):
the fixed sublattices have the same dimensions, determinants and minima (checked), while min L_B = 8 (proved by
supplementary/gluing_b.py [C4], which constructs its 292,320 vectors of norm 8; only recorded here).
--tau B では陰性対照 B（certificates/negative_control_B.npz の tau_class_B）について同じことを行う: 固定部分格子の次元・行列式・最小は同じ
（検査する）だが、min L_B = 8 である（supplementary/gluing_b.py [C4] がノルム 8 のベクトル 292,320 本を作って証明する。ここでは記録するだけ）。

BKZ on the whole lattice (L_112, or L_B with --tau B), progressively with the block sizes of --bkz (default
20, 30, 40, 50, 60; each stage starts from the basis of the previous one; LLL in mpfr first, then LLL and BKZ
with 6 tours in long double, as in the research computation): the shortest norm in the reduced basis at each
stage, computed in integers from the transformation matrix. These are recorded values, not checks: BKZ only
gives upper bounds, and it does not find the norm-8 vectors of B.
格子全体（L_112、--tau B では L_B）への BKZ。--bkz のブロック幅（既定 20, 30, 40, 50, 60）で順に、前の段の基底から続けて簡約する
（研究時の計算と同じく、最初に mpfr で LLL、そのあと long double で LLL と 6 巡の BKZ）。各段の簡約基底の最短のノルムを、変換行列から整数で計算する。
これは記録する値であって検査ではない: BKZ は上界を与えるだけで、B のノルム 8 のベクトルも見つけない。

Recorded in the research (2026-10-13, experiments/2026-10-13-112-init-bkz.py, same procedure): on L_112 BKZ-20
to BKZ-50 give 16, 16, 16, 14 and BKZ-60 gives 10 (3 vectors; 177 s for the stage); on gluing B, built there
from another lift of its gluing map (an isometric lattice in another basis), every stage gives 12 (BKZ-60: 169 s).
研究時の記録（2026-10-13、experiments/2026-10-13-112-init-bkz.py、同じ手順）: L_112 では BKZ-20〜50 が 16, 16, 16, 14、BKZ-60 が 10
（3 本、この段 177 秒）。貼り方 B（研究時は貼り合わせの写像の別の持ち上げから作った。等長で基底が違う格子）では、どの段も 12（BKZ-60 は 169 秒）。

Requires SageMath (PARI, fpylll) and a C compiler. Run time: fixed sublattices about 10 seconds; BKZ under a
minute with --bkz 30,40. With the default block sizes almost all of the time is BKZ-60, and it depends on the
basis: measured 2026-10-18 on a loaded machine, L_112 took 538 s for BKZ-60 (BKZ-20 to BKZ-50: 2, 4, 7, 36 s,
giving 16, 16, 16, 14; BKZ-60 gave 10 with 3 vectors, as in the research), and L_B took 1,008 s for BKZ-60
(BKZ-20 to BKZ-50: 3, 3, 5, 33 s, giving 16, 16, 16, 18; BKZ-60 gave 10 with 3 vectors, not the norm-8 vectors);
the whole run with --tau B took 18 minutes. Memory: about 1 GB.
SageMath（PARI, fpylll）と C コンパイラが要る。実行時間: 固定部分格子は約 10 秒。--bkz 30,40 なら BKZ は 1 分未満。既定のブロック幅では
時間のほとんどが BKZ-60 で、基底によって変わる: 2026-10-18 に負荷のかかった計算機で計測すると、L_112 の BKZ-60 は 538 秒（BKZ-20〜50 は
2, 4, 7, 36 秒で 16, 16, 16, 14、BKZ-60 は 10（3 本）で研究時と同じ）。L_B の BKZ-60 は 1,008 秒（BKZ-20〜50 は
3, 3, 5, 33 秒で 16, 16, 16, 18。BKZ-60 は 10（3 本）で、ノルム 8 のベクトルは見つけない）。--tau B の実行全体は 18 分。メモリ: 約 1 GB。
Run / 実行:  python3 code/supplementary/fixed_sublattices.py [--tau B] [--bkz 30,40]
"""
import argparse
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from lib import certs, data, require  # noqa: E402
from lib import enumerate as exact_enum  # noqa: E402
from lib.report import Report  # noqa: E402

# p -> (dimension, minimum, determinant) of the fixed sublattice (paper, supplement §S3.5); the same for B.
# p -> 固定部分格子の（次元, 最小, 行列式）（論文の補遺 §S3.5）。B でも同じ。
EXPECTED = {3: (32, 12, 3 ** 32), 5: (16, 10, 5 ** 16), 7: (16, 14, 7 ** 16)}
BKZ_DEFAULT = "20,30,40,50,60"
BKZ_TOURS = 6


def bkz_stages(G112, block_sizes, rep, label):
    """Progressive BKZ on the Gram matrix G112 (as in the research computation): LLL in mpfr, then for each block
    size LLL and BKZ in long double from the previous basis. Records the shortest norm of each reduced basis,
    computed exactly as the diagonal of T G112 T^T. / Gram 行列 G112 への段階的な BKZ（研究時の計算と同じ）。"""
    from fpylll import BKZ, GSO, LLL, IntegerMatrix
    from fpylll.algorithms.bkz2 import BKZReduction
    from sage.all import ZZ, matrix
    n = G112.nrows()

    def reduce(G, float_type, bs):
        A = IntegerMatrix.from_matrix([[int(c) for c in r] for r in G.rows()])
        U = IntegerMatrix.identity(n)
        M = GSO.Mat(A, U=U, gram=True, float_type=float_type)
        M.update_gso()
        LLL.Reduction(M)()
        if bs:
            BKZReduction(M)(BKZ.Param(block_size=bs, max_loops=BKZ_TOURS, strategies=BKZ.DEFAULT_STRATEGY))
        T = matrix(ZZ, n, n, lambda i, j: U[i, j])
        require(abs(T.det()) == 1, "abs(T.det()) == 1")
        return T * G * T.transpose()                       # exact; floating point only steers the reduction

    cur = reduce(G112, "mpfr", 0)
    for bs in block_sizes:
        t0 = time.time()
        cur = reduce(cur, "ld", bs)
        d = sorted(int(c) for c in cur.diagonal())
        rep.value(f"BKZ-{bs} on {label}: shortest norm in the reduced basis (upper bound only), its multiplicity, seconds",
                  [d[0], d.count(d[0]), round(time.time() - t0)])


def main():
    from sage.all import QQ, ZZ, block_matrix, identity_matrix, matrix, pari
    ap = argparse.ArgumentParser(description="S14: fixed sublattices and BKZ")
    ap.add_argument("--tau", choices=("C", "B"), default="C", help="C: L_112 (default); B: the negative control B")
    ap.add_argument("--bkz", default=BKZ_DEFAULT,
                    help=f"block sizes of the progressive BKZ, comma-separated (default {BKZ_DEFAULT}, as in the paper; "
                         "empty: no BKZ)")
    ap.add_argument("--data", default=None)
    certs.add_arguments(ap)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    block_sizes = [int(t) for t in a.bkz.split(",") if t.strip()]
    name = "L_112" if a.tau == "C" else "L_B"
    rep = Report("s14_fixed_sublattices" + ("_B" if a.tau == "B" else ""), a.out)
    n = 56
    G = matrix(ZZ, data.gram(a.data).tolist())
    g1, g2 = [matrix(ZZ, g.tolist()) for g in data.generators(a.data)]
    X = matrix(ZZ, (data.tau(a.data) if a.tau == "C" else certs.load("negative_control_B.npz", "tau_class_B", a.certificates)).tolist())
    I = identity_matrix(ZZ, n)
    B = block_matrix(ZZ, [[I, X], [0 * I, 2 * I]], subdivide=False)
    G112 = (B * block_matrix(ZZ, [[G, 0], [0, G]], subdivide=False) * B.transpose() / 2).change_ring(ZZ)
    rep.check(f"Gram matrix of {name}: even, det 1", all(G112[i, i] % 2 == 0 for i in range(112)) and G112.det() == 1)
    rep.check(f"g1, g2 commute with tau ({a.tau}), so diag(h, h) acts on {name}", all(g * X == X * g for g in (g1, g2)))
    if a.tau == "B":
        rep.value("min L_B (not computed here; proved by supplementary/gluing_b.py [C4])", 8)
    Binv = B.change_ring(QQ).inverse()
    # Elements of order 3, 5, 7 as powers of words in g1, g2 (g1 has order 5). / g1, g2 の語の冪として位数 3, 5, 7 の元。
    elts = {5: g1}
    for word in (g2, g1 * g2, g1 * g1 * g2, g1 * g2 * g2, g1 * g2 * g1 * g2 * g2):
        o = word.multiplicative_order()
        for p in (3, 7):
            if o % p == 0 and p not in elts:
                elts[p] = word ** (o // p)
    rep.check("elements of order 3, 5, 7 found", sorted(elts) == [3, 5, 7])
    build = os.path.join(rep.out_dir, "build")
    for p, h in sorted(elts.items()):
        rep.check(f"order {p}: h^{p} = 1, h != 1", h ** p == I and h != I)
        hh = block_matrix(ZZ, [[h, 0 * h], [0 * h, h]], subdivide=False)
        Kc = (B * hh * Binv - 1).change_ring(QQ).left_kernel().basis_matrix()       # L_112-coordinates fixed by h
        Kc = (Kc * Kc.denominator()).change_ring(ZZ).saturation()
        Gs = Kc * G112 * Kc.transpose()
        dim, det = Kc.nrows(), Gs.det()
        U = pari(Gs).qflllgram().sage().transpose()
        require(abs(U.det()) == 1, "abs(U.det()) == 1")
        Gr = U * Gs * U.transpose()
        res = pari(Gr).qfminim(None, 1, 0)                         # PARI: the minimum and one minimal vector
        m = int(res[1])
        w = matrix(ZZ, [list(res[2].sage().column(0))])
        rep.check(f"order {p}: the vector found by PARI has norm {m} (exact)", int((w * Gr * w.transpose())[0, 0]) == m)
        found, nodes = exact_enum.short_vectors([[int(c) for c in r] for r in Gr.rows()], m - 2, build)
        rep.value(f"order {p}: dimension, determinant, minimum, nodes of the exact enumeration below the minimum",
                  [dim, str(det.factor()), m, nodes])
        rep.check(f"order {p}: exact minimum {m} (a vector of norm {m}; none of norm <= {m - 2})", len(found) == 0)
        e_dim, e_min, e_det = EXPECTED[p]
        rep.check(f"order {p}: dimension {e_dim}, determinant {p}^{e_dim}, minimum {e_min} as in the paper",
                  (dim, int(det), m) == (e_dim, e_det, e_min))
    if block_sizes:
        bkz_stages(G112, block_sizes, rep, name)
    rep.finish()


if __name__ == "__main__":
    main()
