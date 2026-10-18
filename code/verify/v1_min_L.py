"""V1. F1: min L = 6, by an enumeration that cannot miss vectors (paper §6.1 (a), Table 5).
V1. F1: min L = 6。取りこぼしの無い列挙による（論文 §6.1 (a)、表 5）。

Steps / 手順:
  1. Read the basis change U (certificates/reduction_L.txt), check exactly that det U = +-1,
     and compute G' = U G U^T in integers. (How U was found — BKZ-40 in floating point,
     code/produce/p6_reduction.py — does not matter: any unimodular U gives the same lattice.)
     基底変換 U を読み、det U = ±1 を厳密に確かめ、G' = U G U^T を整数で計算する。
     （U の作り方は関係ない。どんな U でも det U = ±1 なら同じ格子。）
  2. Compute G' = V^T diag(D) V exactly over the rationals.
     G' = V^T diag(D) V を有理数で厳密に求める。
  3. Replace each D_i and V_ij by the interval [nextbelow(f), nextabove(f)] around its nearest
     double f. Python's float(Fraction) rounds to nearest, so the true value lies inside.
     D_i, V_ij を、最も近い倍精度の値 f の両隣 [f の 1 つ下, f の 1 つ上] の区間に置き換える。
     Python の float(Fraction) は最近接丸めなので、真の値は区間に入る。
  4. Run enum_interval.c with radius 4. It reports every nonzero vector of norm <= 4.
     半径 4 で enum_interval.c を走らせる。ノルム 4 以下の 0 でないベクトルをすべて報告する。
  Since L is even with det 1 and dimension 56, min L <= 6 (Siegel's bound 2 floor(56/24) + 2);
  "no nonzero vector of norm <= 4" therefore means min L = 6.
  L は偶で det 1、56 次元なので min L ≤ 6（2⌊56/24⌋ + 2）。よって「ノルム 4 以下の 0 でないベクトルが無い」は min L = 6 を意味する。

Positive controls (same code path): E_8 at radius 2 (240 vectors), the Leech lattice at radius 4
(196,560 of norm 4, none of norm 2), and Leech + Leech + E_8 at radius 4 (240 and 395,280).
陽性対照（同じ経路）: E_8（半径 2、240 本）、Leech 格子（半径 4、ノルム 4 が 196,560 本、ノルム 2 は無し）、
Leech + Leech + E_8（半径 4、240 本と 395,280 本）。

The input of the enumerator (steps 2, 3), its compilation and the parsing of its output are in
lib/enumerate.py, shared with the other users of the enumerator. The enumerator is recompiled on every run.
列挙器の入力（手順 2, 3）、コンパイル、出力の解釈は lib/enumerate.py にあり、列挙器のほかの利用者と共有する。列挙器は毎回コンパイルし直す。

Run time: about 34 minutes (8.5 x 10^9 nodes) on one core; controls take seconds.
実行時間: 1 コアで約 34 分（8.5 × 10^9 節点）。対照は数秒。

Run / 実行:  python3 code/verify/v1_min_L.py [--controls-only] [--data DIR] [--certificates DIR] [--out DIR]
Requires a C compiler with 128-bit integers (gcc or clang; $CC, else cc, gcc, clang). / 128 ビット整数をもつ C コンパイラ（gcc か clang。$CC、無ければ cc, gcc, clang の順に探す）が要る。
"""
import argparse
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from lib import certs, data, exact  # noqa: E402
from lib import enumerate as exact_enum  # noqa: E402
from lib.report import Report  # noqa: E402

E8 = np.array([  # Gram matrix of E_8 (a reduced basis) / E_8 の Gram 行列（簡約基底）
    [2, 1, 1, -1, 1, 1, 1, 1], [1, 2, 1, 0, 1, 1, 0, 1], [1, 1, 2, -1, 1, 0, 1, 1], [-1, 0, -1, 2, 0, 0, -1, -1],
    [1, 1, 1, 0, 2, 0, 0, 0], [1, 1, 0, 0, 0, 2, 0, 1], [1, 0, 1, -1, 0, 0, 2, 1], [1, 1, 1, -1, 0, 1, 1, 2]], dtype=np.int64)


def enumerate_short(exe, G, radius, rep, name):
    """Run the enumerator on the Gram matrix G; returns {norm: count} and the node count.
    lib.enumerate.run_enumerator checks that the enumerator finished and that no vector fell outside its table.
    Gram 行列 G について列挙器を走らせ、{ノルム: 本数} と節点数を返す。
    列挙器が最後まで走ったことと、表の範囲外に落ちたベクトルが無いことは lib.enumerate.run_enumerator が確かめる。"""
    res = exact_enum.run_enumerator(exe, G, radius)
    rep.value(f"{name}: nodes", res["nodes"])
    rep.value(f"{name}: nonzero vectors by norm", res["counts"])
    return res["counts"], res["nodes"]


def main():
    ap = argparse.ArgumentParser(description="V1: F1 (min L = 6)")
    ap.add_argument("--controls-only", action="store_true")
    ap.add_argument("--data", default=None)
    ap.add_argument("--certificates", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rep = Report("v1_min_L" + ("_controls" if a.controls_only else ""), a.out)
    exe = exact_enum.compile_enumerator(os.path.join(rep.out_dir, "build"), force=True)

    # Positive controls. / 陽性対照。
    leech = data.read_integers(os.path.join(HERE, "controls", "leech.txt")).reshape(24, 24)
    c, _ = enumerate_short(exe, E8, 2, rep, "E8, radius 2")
    rep.check("E8: exactly 240 vectors of norm 2", c == {2: 240})
    c, _ = enumerate_short(exe, leech, 4, rep, "Leech, radius 4")
    rep.check("Leech: exactly 196560 vectors of norm 4 and none of norm 2", c == {4: 196560})
    Z = lambda p, q: np.zeros((p, q), dtype=np.int64)  # noqa: E731
    big = np.block([[leech, Z(24, 24), Z(24, 8)], [Z(24, 24), leech, Z(24, 8)], [Z(8, 24), Z(8, 24), E8]])
    c, _ = enumerate_short(exe, big, 4, rep, "Leech + Leech + E8, radius 4")
    rep.check("Leech + Leech + E8: 240 of norm 2 and 395280 = 2 x 196560 + 2160 of norm 4",
              c == {2: 240, 4: 395280})
    if a.controls_only:
        rep.finish()
        return

    # L. / L。
    G = data.gram(a.data)
    U = certs.load_matrix("reduction_L.txt", 56, a.certificates)
    rep.check("reduction_L.txt: det U = +-1", abs(exact.det_bareiss(U)) == 1)
    Gr = exact.i64_matmul(exact.i64_matmul(U, G), U.T)
    rep.value("diagonal of U G U^T (norms of the reduced basis)", sorted(set(int(v) for v in np.diag(Gr))))
    c, nodes = enumerate_short(exe, Gr, 4, rep, "L, radius 4")
    rep.check("L has no nonzero vector of norm <= 4, hence min L = 6", c == {})
    rep.finish()


if __name__ == "__main__":
    main()
