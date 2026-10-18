"""Constants and file handling of supplementary/genus/genus.py (numpy only): the labels, orders and status of the
eight classes, the names of the distributed files, and where the steps write and read them.
supplementary/genus/genus.py の定数とファイルの扱い（numpy のみ）: 8 類の番号・位数・状態、配布ファイルの名前、各段がそれらを書き読む場所。
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from lib import certs, data, require  # noqa: E402

N = 56
NX = 2 * N
NCLASS = 8
MASS = Fraction(157, 640)                         # 2^{-4} |zeta_K(-1) zeta_K(-3)|, K = Q(sqrt 29)
PRIMES = (2, 3, 5, 7, 29)                         # the primes dividing |SL_2(29)| = 2^3 3 5 7 29
# Labels of the classes: (|U(Lambda)|, number of +-pairs of vectors of Tr trd h = 2, 4, ..., 14).
# 類の番号: (|U(Λ)|, Tr trd h = 2, 4, …, 14 のベクトルの ± 対の本数)。
LABELS = {
    0: (1152, (0, 24, 0, 312, 0, 672, 0)),        # L + L
    1: (12, (0, 0, 0, 12, 0, 192, 48)),           # mod-2 gluing of type bc; extremality decided separately
    2: (288, (0, 0, 0, 48, 0, 72, 144)),          # L~ + L~
    3: (24, (0, 0, 0, 24, 0, 144, 96)),           # gluing A = gluing B
    4: (24, (0, 0, 0, 36, 0, 168, 0)),            # mod-2 gluing of type bc, has a vector of norm 8
    5: (20, (0, 0, 0, 0, 0, 180, 120)),           # no mod-2 frame, has a vector of norm 8
    6: (288, (0, 12, 0, 36, 0, 660, 72)),         # L + L~
    7: (48, (0, 0, 0, 0, 0, 216, 48)),            # L_112
}
# Types of the mod-2 frames (frames). / mod 2 の枠の型（frames）。
FRAME_TYPES = {0: ["bb"], 1: ["bc"], 2: ["cc"], 3: ["bb", "cc"], 4: ["bc"], 5: [], 6: [], 7: ["cc"]}
# Minimum norm, as in Table S10 and Theorem S6.1 (c) of the supplement, with where it is proved. 6 for the orthogonal
# sums (min L = min L~ = 6); 8 for class 3 (gluing A = gluing B: isometry_ab.py [C28], min L_B = 8 by gluing_b.py
# [C4]); only <= 8 for classes 4 and 5, where the norm-8 witness gives an upper bound (no lower bound is computed);
# 10 for L_112 (Theorem A). check verifies the witnesses and the isometries, not these minima.
# 最小ノルム（補遺の表 S10・定理 S6.1 (c) のとおり）とその根拠。直交和は 6（min L = min L~ = 6）。類 3 は 8（貼り方 A = 貼り方 B:
# isometry_ab.py [C28]、min L_B = 8 は gluing_b.py [C4]）。類 4、5 はノルム 8 の証拠による上界 ≤ 8 だけ（下界は計算しない）。
# L_112 は 10（定理 A）。check が確かめるのは証拠と等長写像であって、これらの最小ではない。
STATUS = {0: "orthogonal sum L + L, min 6", 1: "open (decided by a separate computation)",
          2: "orthogonal sum L~ + L~, min 6",
          3: "gluing A = gluing B, min 8 (A = B: isometry_ab.py [C28]; min L_B = 8: gluing_b.py [C4])",
          4: "min <= 8 (norm-8 witness; not extremal)", 5: "min <= 8 (norm-8 witness; not extremal)",
          6: "orthogonal sum L + L~, min 6", 7: "L_112, min 10 (Theorem A)"}
WITNESS_CLASSES = (3, 4, 5)

CLASSES_FILE = "genus_classes.txt"
WITNESS_FILE = "genus_witnesses.txt"
ISO7_FILE = "genus_isometry_7_L112.txt"
ISO3_FILE = "genus_isometry_3_A.txt"


def gram_file(j):
    return f"genus_class_{j}.txt"


def basis_file(j):
    return f"genus_basis_{j}.txt"


def gdir(out_dir):
    d = os.path.join(out_dir, "genus")
    os.makedirs(d, exist_ok=True)
    return d


def dest_dir(a, rep):
    """Directory where enum, build, witness, identify write their certificate files: --dest, by default out/genus/
    (next to lambda.txt). The distributed files in certificates/ are replaced only when --dest names that directory.
    enum, build, witness, identify が検証用データのファイルを書くディレクトリ: --dest、既定は out/genus/（lambda.txt と同じ場所）。
    certificates/ の配布ファイルは、--dest でそのディレクトリを指定したときだけ置き換わる。"""
    d = a.dest or gdir(rep.out_dir)
    os.makedirs(d, exist_ok=True)
    return d


def produced(name, a, rep):
    """Path of a file written by an earlier step: in the output directory if it is there, otherwise the distributed
    file (SHA-256 checked). / 前の段が書いたファイルのパス: 出力先にあればそれ、無ければ配布ファイル（SHA-256 を照合）。"""
    p = os.path.join(dest_dir(a, rep), name)
    return p if os.path.exists(p) else certs.path_checked(name, a.certificates)


def compare_with_distributed(name, a, rep, canonical=False):
    """Compare a file just written with the distributed one: identical bytes, the same integers (only comment lines
    differ), or different. A difference is not an error in general (the walk, PARI's enumeration order and the
    embedding of nebe/reduction_to_nebe.py may vary; every distributed file is verified by check). With
    canonical=True the integers are a canonical invariant (genus_classes.txt: the labels do not depend on the walk)
    and must agree.
    書いたばかりのファイルを配布ファイルと比べる: バイト単位で同じ、整数が同じ（注釈行だけが違う）、違う、のいずれか。違うことは一般には誤りでない
    （近傍の歩き方、PARI の列挙順、nebe/reduction_to_nebe.py の埋め込みは変わりうる。配布ファイルはすべて check が確かめる）。canonical=True のときは
    整数が標準的な不変量なので（genus_classes.txt: 類の番号は歩き方によらない）、一致しなければならない。"""
    cdir = a.certificates or certs.DEFAULT_DIR
    new = os.path.join(dest_dir(a, rep), name)
    dist = os.path.join(cdir, name)
    if os.path.realpath(new) == os.path.realpath(dist):
        rep.log(f"{name}: written into the distributed directory {cdir}; update {cdir}/SHA256SUMS")
        return
    if not os.path.exists(dist):
        rep.value(f"{name}: compared with the distributed file", "no distributed file")
        return
    dist = certs.path_checked(name, cdir)
    with open(new, "rb") as f1, open(dist, "rb") as f2:
        same_bytes = f1.read() == f2.read()
    vn, vd = data.read_integers(new), data.read_integers(dist)
    same_ints = vn.shape == vd.shape and bool((vn == vd).all())
    verdict = ("identical" if same_bytes else "the same integers (comment lines differ)" if same_ints else "different" if canonical
               else "different (allowed: another walk, enumeration order or embedding; check verifies the distributed file)")
    rep.value(f"{name}: written to {new}; compared with the distributed file", verdict)
    if canonical:
        rep.check(f"{name}: the same integers as the distributed file (canonical labels)", same_ints)


def read_basis(j, cdir, path=None):
    """(d, D) from certificates/genus_basis_<j>.txt (or from path). / genus_basis_<j>.txt（または path）の (d, D)。"""
    v = data.read_integers(path or certs.path_checked(basis_file(j), cdir))
    require(v.size == 1 + NX * NX, basis_file(j))
    return int(v[0]), v[1:].reshape(NX, NX)
