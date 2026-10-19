"""P6. Produce the two basis-change certificates (paper §6.1 step 1, Appendix D).
P6. 検算に使う 2 つの基底変換を作る（論文 §6.1 の手順 1、付録 D）。

  reduction_L.txt   U (56 x 56) with U G U^T BKZ-40 reduced; used by verify/v1_min_L.py
                    U G U^T が BKZ-40 簡約になる U。verify/v1_min_L.py が使う
  reduction_R.txt   U (112 x 112) with U (3.1) U^T = data/R112_gram_LLL.txt
                    U (3.1) U^T = data/R112_gram_LLL.txt となる U

How they are found does not matter for the proof: the verification only checks that U is
an integer matrix of determinant +-1 (and, for L_112, the matrix identity).
作り方は証明に関係しない。検算は U が行列式 ±1 の整数行列であること（L_112 については行列の等式も）だけを確かめる。

Method / 方法:
  L: the Gram matrix is turned into an integer basis by scaling a floating-point Cholesky
     factor by 2^40 and rounding; fpylll's LLL and BKZ (block size 40, at most 4 tours)
     are applied to it, and only the accumulated transformation is kept.
     Gram 行列の浮動小数点の Cholesky 分解を 2^40 倍して丸めた整数基底に、fpylll の LLL と BKZ（ブロック 40、最大 4 周）を掛け、
     変換行列だけを使う。
  L_112: PARI's qflllgram on the Gram matrix (3.1) (this is how data/R112_gram_LLL.txt was made).
     (3.1) の Gram 行列に PARI の qflllgram（data/R112_gram_LLL.txt はこれで作った）。

Output: out/p6/reduction_L.txt and out/p6/reduction_R.txt (never certificates/: the distributed files
are fixed by certificates/SHA256SUMS). Both are compared byte for byte with the distributed files
certificates/reduction_L.txt and certificates/reduction_R.txt; a difference is reported as a failure
(exit code 1). BKZ is not guaranteed to give the same basis with other versions of fpylll; a
different but valid U would still pass verify/v0 and verify/v1 after replacing the file and its hash
(only the run time of v1 depends on the reduction).
出力: out/p6/reduction_L.txt と out/p6/reduction_R.txt（certificates/ には書かない。配布ファイルは certificates/SHA256SUMS で固定されている）。
どちらも配布ファイル certificates/reduction_L.txt・certificates/reduction_R.txt とバイト単位で比べ、違えば失敗（終了コード 1）とする。
fpylll の版が違うと BKZ が同じ基底を返す保証は無い。違っていても正しい U であれば、ファイルとハッシュを差し替えれば verify/v0・verify/v1 を通る
（簡約の良し悪しは v1 の実行時間にだけ影響する）。

Requires SageMath (PARI, fpylll). Run time about 1 minute (BKZ-40).
SageMath（PARI, fpylll）が要る。実行時間は約 1 分（BKZ-40）。

Run / 実行:  python3 code/produce/p6_reduction.py [--data DIR] [--certificates DIR] [--out DIR]
             (with the python3 of an environment that has SageMath / SageMath の入った環境の python3 で)
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import certs, data, exact  # noqa: E402
from lib.report import Report  # noqa: E402


def bkz_transform(G, block, loops=4):
    """U with U G U^T BKZ-reduced (row convention). / U G U^T が BKZ 簡約になる U（行の約束）。"""
    from fpylll import BKZ, GSO, LLL, IntegerMatrix
    from fpylll.algorithms.bkz2 import BKZReduction
    n = len(G)
    C = np.linalg.cholesky(np.asarray(G, dtype=float))          # G = C C^T; rows of C are basis vectors / C の行が基底
    A = IntegerMatrix.from_matrix([[int(round(v * 2 ** 40)) for v in row] for row in C])
    U = IntegerMatrix.identity(n)
    M = GSO.Mat(A, U=U, float_type="mpfr")
    LLL.Reduction(M)()
    BKZReduction(M)(BKZ.EasyParam(block, max_loops=loops))
    return np.array([[U[i, j] for j in range(n)] for i in range(n)], dtype=np.int64)


def same_bytes(path, name, directory):
    """Whether the file at `path` equals the distributed certificate `name` byte for byte
    (the distributed file is first checked against SHA256SUMS).
    `path` のファイルが配布した検証用データ `name` とバイト単位で同じか（配布ファイルはまず SHA256SUMS と照合する）。"""
    with open(path, "rb") as f, open(certs.path_checked(name, directory), "rb") as g:
        return f.read() == g.read()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data", default=None, help="directory of the four input files / 入力ファイルの置き場所")
    certs.add_arguments(ap, help="distributed data to compare with / 比べる配布データの置き場所")
    ap.add_argument("--out", default=None, help="output directory (default out/; the files go to <out>/p6/) / 出力先（既定は out/。ファイルは <out>/p6/ に書く）")
    ap.add_argument("--block", type=int, default=40)
    a = ap.parse_args()
    rep = Report("p6_reduction", a.out)
    pdir = os.path.join(rep.out_dir, "p6")
    os.makedirs(pdir, exist_ok=True)
    G = data.gram(a.data)
    t = data.tau(a.data)

    # L: BKZ-40 transformation. / L: BKZ-40 の変換。
    U = bkz_transform(G, a.block)
    rep.check("det U = +-1 (Bareiss)", abs(exact.det_bareiss(U)) == 1)
    Gr = exact.i64_matmul(exact.i64_matmul(U, G), U.T)
    diag = sorted(set(int(v) for v in np.diag(Gr)))
    rep.value(f"diagonal norms of U G U^T (BKZ-{a.block})", diag)
    path_L = os.path.join(pdir, "reduction_L.txt")
    certs.save_matrix(path_L, U,
                      f"U (56 x 56, rows = new basis in terms of the old): U G U^T is BKZ-{a.block} reduced.\n"
                      f"U（56 × 56、行 = 新しい基底を古い基底で表したもの）: U G U^T は BKZ-{a.block} 簡約。\n"
                      f"diagonal of U G U^T / U G U^T の対角: {diag}")

    # L_112: qflllgram, compared with the distributed reduced Gram matrix.
    # L_112: qflllgram。配布した簡約 Gram 行列と比べる。
    from sage.all import ZZ, matrix, pari
    B = data.gram_R(G, t)
    V = pari(matrix(ZZ, B.tolist())).qflllgram().sage()        # columns = new basis (PARI convention) / 列が新しい基底
    UR = np.array(V.transpose().rows(), dtype=np.int64)        # rows = new basis / 行が新しい基底
    rep.check("U (3.1) U^T = data/R112_gram_LLL.txt",
              (exact.i64_matmul(exact.i64_matmul(UR, B), UR.T) == data.gram_R_reduced(a.data)).all())
    path_R = os.path.join(pdir, "reduction_R.txt")
    certs.save_matrix(path_R, UR,
                      "U (112 x 112): U [[3G, tau G], [(tau G)^T, 2G]] U^T = data/R112_gram_LLL.txt (PARI qflllgram).\n"
                      "U（112 × 112）: U [[3G, tau G], [(tau G)^T, 2G]] U^T = data/R112_gram_LLL.txt（PARI の qflllgram）。")
    rep.log(f"wrote {path_L} and {path_R}")

    # Compare with the distributed files. / 配布ファイルと比べる。
    rep.check("reduction_L.txt is identical (byte for byte) to certificates/reduction_L.txt",
              same_bytes(path_L, "reduction_L.txt", a.certificates), stop=False)
    rep.check("reduction_R.txt is identical (byte for byte) to certificates/reduction_R.txt",
              same_bytes(path_R, "reduction_R.txt", a.certificates), stop=False)
    rep.finish()
    sys.exit(1 if rep.failed else 0)


if __name__ == "__main__":
    main()
