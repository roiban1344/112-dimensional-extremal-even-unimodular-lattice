"""S25. The 112-dimensional even unimodular lattices on which SL_2(29) acts as on L_112: the genus of rank-2
unimodular Hermitian lattices over the maximal order M (Table D2 [C29]-[C31]). Not used in the proof of
Theorem A.
S25. SL_2(29) が L_112 と同じ形で働く 112 次元の偶ユニモジュラー格子: 極大整環 M 上の階数 2 のユニモジュラーなエルミート格子の種
（表 D2 の [C29]〜[C31]）。定理 A の証明には使わない。

Setting. L = L_{56,2}(M) is Nebe's lattice for the maximal order M whose centralizer of SL_2(29) has order 24
(built from the definition by nebe/lattices.py, read from out/nebe/M_*), S = <z, w> = SL_2(29) acting on L,
H = Q_{sqrt29,inf,inf} acting on W = L tensor Q from the right (cycloquat.py), with M the right order of L.
For a rank-2 M-lattice Lambda in H^2 with h(l, m) = l_1 m_1* + l_2 m_2*, X = L tensor_M Lambda is the lattice
spanned by (x l_1, x l_2) (x in L, l in Lambda) in W^2 with the form diag(G_M, G_M); X is even unimodular
iff Lambda is unimodular for h. Lambda is stored by a 16 x 16 rational matrix C (rows: a Z-basis in the
coordinates of Lambda_0 = M + M). Isometry of two Lambda's is tested with PARI qfisom, and U(Lambda) computed
with qfauto, on the nine integral forms Tr_{K/Q} trd(m_k h), m_k running over 1 and a Z-basis of M (an
isometry preserving all nine is M-linear and preserves h), K = Q(sqrt29).
設定. L = L_{56,2}(M) は、SL_2(29) の中心化群の位数が 24 になる極大整環 M についての Nebe の格子（nebe/lattices.py が定義から作り、
out/nebe/M_* から読む）。S = <z, w> = SL_2(29) が L に働き、H = Q_{√29,∞,∞} が W = L ⊗ Q に右から働く（cycloquat.py）。M は L の右整環。
H^2 の中の階数 2 の M-格子 Λ（h(l, m) = l_1 m_1* + l_2 m_2*）に対して X = L ⊗_M Λ は W^2 の中で (x l_1, x l_2)（x ∈ L, l ∈ Λ）が張る格子で、
形式は diag(G_M, G_M)。X が偶ユニモジュラー ⟺ Λ が h についてユニモジュラー。Λ は 16 × 16 の有理行列 C（行が Λ_0 = M ⊕ M の座標での Z-基底）で持つ。
Λ どうしの等長は PARI の qfisom、U(Λ) は qfauto で、9 個の整数値の形式 Tr_{K/Q} trd(m_k h)（m_k は 1 と M の Z-基底）について計算する
（9 個をすべて保つ等長写像は M-線形で h を保つ）。K = Q(√29)。

Subcommands (SageMath unless stated otherwise) / サブコマンド（特記しない限り SageMath）:
  local     For p = 2, 3, 5, 7, 29 (the primes dividing |SL_2(29)|): the F_p-algebra spanned by z, w on L/pL has
            dimension 392 = dim End_{M/pM}(L/pL) (the latter computed as the commutant of the right action of M).
            So the image of Z[S] is End_M(L) tensor Z_p at every p (Nakayama), and every S-invariant lattice in W^2 is
            L tensor_M Lambda (Morita).
            p = 2, 3, 5, 7, 29（|SL_2(29)| を割る素数）で、z, w が L/pL 上に張る F_p-代数の次元が 392 = dim End_{M/pM}(L/pL)
            （後者は M の右作用の可換子として計算）。よって Z[S] の像は各 p で End_M(L) ⊗ Z_p に一致し（中山）、W^2 の中の S 不変格子は
            すべて L ⊗_M Λ（森田）。
  mass      zeta_K(-1) = 1/2 and zeta_K(-3) = 157/20 exactly from generalized Bernoulli numbers B_{k,chi_29}, compared
            with Siegel's divisor-sum formulas and with PARI lfun (numerically); the mass
            2^{-4} |zeta_K(-1) zeta_K(-3)| = 157/640 [Gan-Hanke-Yu 2001, Prop. 9.4; = Prop. 9.3 when S_D is empty]. Normalization check in rank 1:
            the unit groups {u : nrd u = 1} of the two classes of maximal orders have orders 24 and 12, and
            1/24 + 1/12 = 2^{-2} |zeta_K(-1)|.
            一般化 Bernoulli 数 B_{k,χ_29} から ζ_K(-1) = 1/2、ζ_K(-3) = 157/20 を厳密に求め、Siegel の約数和の公式と PARI の lfun（数値）と照合する。
            質量 2^{-4}|ζ_K(-1)ζ_K(-3)| = 157/640 [Gan–Hanke–Yu 2001, 命題 9.4。S_D が空なら命題 9.3 に一致]。階数 1 での正規化の確認: 極大整環の 2 類の {u : nrd u = 1} の
            位数は 24 と 12 で、1/24 + 1/12 = 2^{-2}|ζ_K(-1)|。
  enum      Kneser neighbours at the prime p = ((7 + sqrt29)/2) of norm 5 (Siegel type: N = Lambda cap Lambda'
            with h(N, N) in p M, Lambda' between N and pi^{-1} N), walked at random from Lambda_0 = M + M with a fixed
            seed (--seed, default 1) until sum 1/|U(Lambda)| reaches the mass 157/640. The classes are labelled 0-7
            by the invariants (|U|, number of vectors of each norm <= 14 of Tr trd h), independently of the order in
            which the walk finds them. Writes out/genus/lambda.txt and certificates/genus_classes.txt.
            ノルム 5 の素イデアル p = ((7 + √29)/2) での Kneser の近傍（Siegel 型: N = Λ ∩ Λ' で h(N, N) ⊂ pM、Λ' は N と π^{-1}N の間）を、
            Λ_0 = M ⊕ M から固定した乱数シード（--seed、既定 1）で無作為にたどり、Σ 1/|U(Λ)| が質量 157/640 に達するまで続ける。類の番号 0〜7 は
            不変量（|U| と Tr trd h のノルム 14 以下のベクトルの本数）で付け、見つかる順序によらない。out/genus/lambda.txt と
            certificates/genus_classes.txt を書く。
  build     X_j = L tensor_M Lambda_j for the 8 classes, LLL-reduced (PARI qflllgram). Writes the Gram matrices
            certificates/genus_class_<j>.txt and, in certificates/genus_basis_<j>.txt, the basis of X_j in the
            coordinates of data/L56_gram.txt (L~ below): through the embedding e: L~ -> L_{56,2}(M) of
            nebe/reduction_to_nebe.py (out/nebe/embedding_L_into_M.txt; <e x, e y> = 2 <x, y>), W^2 = (L~ tensor Q)^2,
            and the basis is scaled so that the form is diag(G, G)/2 as in (3.1). The file holds d, then
            D = d B (integers), B the rational basis matrix: D diag(G, G) D^T = 2 d^2 G_X.
            8 類の X_j = L ⊗_M Λ_j を作り LLL 簡約する（PARI の qflllgram）。Gram 行列を certificates/genus_class_<j>.txt に、
            data/L56_gram.txt（以下 L~）の座標での X_j の基底を certificates/genus_basis_<j>.txt に書く。nebe/reduction_to_nebe.py の
            埋め込み e: L~ -> L_{56,2}(M)（out/nebe/embedding_L_into_M.txt。<e x, e y> = 2<x, y>）で W^2 = (L~ ⊗ Q)^2 とし、形式が (3.1) と同じ
            diag(G, G)/2 になるように基底を倍する。ファイルには d と D = d B（整数。B は有理数の基底行列）を書く: D diag(G, G) D^T = 2 d^2 G_X。
  frames    For each class, the decompositions Lambda = J + J' (J = Lambda cap H v for v with h(v, v) in {2, 2pi, 2pi~},
            J' its orthogonal complement): those of index 2^8 with h(J, J), h(J', J') in 2M are the mod-2 gluings;
            type b = 2M (L_{56,2}(M) scaled by sqrt2), c = 2I (L_{56,2}(M~) scaled by sqrt2).
            各類で Λ = J ⊕ J' の分解（h(v, v) ∈ {2, 2π, 2π~} の v から J = Λ ∩ Hv、J' はその直交補）を調べる。指数 2^8 で h(J, J), h(J', J') ⊂ 2M
            のものが mod 2 の貼り合わせ。型 b = 2M（L_{56,2}(M) の √2 倍）、c = 2I（L_{56,2}(M~) の √2 倍）。
  witness   Norm-8 vectors for classes 3, 4 (in the fixed sublattice of s u, s = z w of order 3, u in U(Lambda) of
            order 3; PARI qfminim) and class 5 (fixed sublattice of s u, s = w of order 4, u of order 4, dimension 56;
            BKZ and pruned enumeration with fpylll, fixed seeds). Each vector is checked exactly (v G_X v^T = 8) and
            written, in the basis of genus_class_<j>.txt, to certificates/genus_witnesses.txt.
            類 3, 4（位数 3 の s = zw と位数 3 の u ∈ U(Λ) の積 s u の固定部分格子。PARI の qfminim）と類 5（位数 4 の s = w と位数 4 の u の積の
            固定部分格子、56 次元。fpylll の BKZ と枝刈りつき列挙、乱数シードは固定）のノルム 8 のベクトル。v G_X v^T = 8 を厳密に確かめ、
            genus_class_<j>.txt の基底での座標を certificates/genus_witnesses.txt に書く。
  identify  Explicit isometries class 7 -> L_112 (the basis (3.1) from data/) and class 3 -> gluing A
            (certificates/gram_A.txt), found as in isometry_ab.py: among the S-equivariant maps (32-dimensional) that
            are integral, those with Q(T) = tr(G_X^{-1} T G_Y T^T) <= 112 are enumerated (qfminim, checked complete)
            and T G_Y T^T = G_X is tested exactly. Class 7 is compared in the coordinates of L~ (data/), class 3 in
            the reduced coordinates of L_{56,2}(M) of isometry_ab.py. As a cross-check of the orders |U(Lambda)|
            (computed by qfauto in enum), the same enumeration with Y = X_j counts the S-equivariant automorphisms
            of X_j, which form U(Lambda_j) (Morita). Writes certificates/genus_isometry_7_L112.txt and
            certificates/genus_isometry_3_A.txt (rows: the basis of X_j in the basis of the target).
            明示的な等長写像 類 7 -> L_112（data/ からの基底 (3.1)）と 類 3 -> 貼り方 A（certificates/gram_A.txt）を isometry_ab.py と同じ方法で求める:
            S 同変な写像（32 次元）のうち整数のものの中で Q(T) = tr(G_X^{-1} T G_Y T^T) ≤ 112 となるものを列挙し（qfminim。完全性を確かめる）、
            T G_Y T^T = G_X を厳密に確かめる。類 7 は L~（data/）の座標で、類 3 は isometry_ab.py の L_{56,2}(M) の簡約座標で比べる。
            enum で qfauto が求めた位数 |U(Λ)| の検算として、Y = X_j とした同じ列挙で X_j の S 同変な自己同型（森田により U(Λ_j)）を数える。
            certificates/genus_isometry_7_L112.txt と certificates/genus_isometry_3_A.txt を書く（行は X_j の基底を行き先の基底で書いたもの）。
  check     (numpy only, integer arithmetic; no SageMath.) For each class j: G_X symmetric, even, det 1 (Bareiss);
            D diag(G, G) D^T = 2 d^2 G_X with G = data/L56_gram.txt; the generators g1, g2 of data/ act on X_j:
            s_i = D diag(g_i, g_i) D^{-1} = D diag(g_i, g_i) diag(G, G) D^T G_X^{-1} / (2 d^2) is an integer matrix
            (exact division; G_X^{-1} by exact inversion) with s_i G_X s_i^T = G_X. So X_j is an even unimodular
            lattice in (L~ tensor Q)^2, the space of (3.1), invariant under diag(g1, g1), diag(g2, g2). Then: the
            witnesses have norm 8 in their class; the isometries class 7 -> L_112 and class 3 -> gluing A satisfy
            T G_Y T^T = G_X, det T = +-1, and the one to L_112 commutes with the action of SL_2(29); the reported
            orders sum to the mass: sum_j 1/|U(Lambda_j)| = 157/640 (exact rationals). check verifies this sum, not
            the orders themselves, which come from PARI qfauto in enum (and are recounted in identify).
            （numpy のみ、整数演算。SageMath は不要。）各類 j について: G_X が対称・偶・行列式 1（Bareiss）。G = data/L56_gram.txt として
            D diag(G, G) D^T = 2 d^2 G_X。data/ の生成元 g1, g2 が X_j に働く: s_i = D diag(g_i, g_i) D^{-1}
            = D diag(g_i, g_i) diag(G, G) D^T G_X^{-1} / (2 d^2) が整数行列（割り算が割り切れる。G_X^{-1} は厳密な逆行列）で、s_i G_X s_i^T = G_X。
            したがって X_j は (3.1) と同じ空間 (L~ ⊗ Q)^2 の中の偶ユニモジュラー格子で、diag(g1, g1), diag(g2, g2) で不変。さらに: 証拠のベクトルが
            その類でノルム 8。類 7 -> L_112 と 類 3 -> 貼り方 A の等長写像が T G_Y T^T = G_X、det T = ±1 を満たし、L_112 への写像は SL_2(29) の
            作用と可換。報告した位数の和が質量になる: Σ_j 1/|U(Λ_j)| = 157/640（有理数の厳密計算）。check が確かめるのはこの和であって位数そのものでは
            ない。位数は enum の PARI qfauto による（identify で数え直す）。

Class 1 is not decided here: its extremality is the subject of a separate computation. A norm-8 vector of
class 1, if one is found, is added as a line of certificates/genus_witnesses.txt and check verifies it like the
others; check reports which classes have a witness.
類 1 はここでは決めない。極値かどうかは別の計算で調べる。類 1 のノルム 8 のベクトルが見つかれば certificates/genus_witnesses.txt に 1 行足すだけで、
check がほかと同じく確かめる。check はどの類に証拠があるかを報告する。

Prerequisites: out/nebe/M_* and Mtilde_order.txt (nebe/lattices.py), out/nebe/embedding_L_into_M.txt
(nebe/reduction_to_nebe.py; used by build and identify). The embedding is determined only up to an
automorphism of L~ normalizing SL_2(29), and reduction_to_nebe.py need not return the same one on every run; the
distributed bases genus_basis_<j>.txt were built with the embedding used for certificates/isometry_AB.txt.
check does not depend on this choice. Order of the steps: local, mass, enum, build, frames, witness, identify, check.
前提: out/nebe/M_* と Mtilde_order.txt（nebe/lattices.py）、out/nebe/embedding_L_into_M.txt（nebe/reduction_to_nebe.py。build と identify が使う）。
埋め込みは SL_2(29) を正規化する L~ の自己同型を除いてしか決まらず、reduction_to_nebe.py は実行ごとに同じものを返すとは限らない。配布した基底
genus_basis_<j>.txt は certificates/isometry_AB.txt と同じ埋め込みで作った。check はこの選び方によらない。
実行順: local, mass, enum, build, frames, witness, identify, check。

Run time (single thread, measured on a shared, loaded machine): local 20 minutes, mass 1 second, enum 16 minutes
(62 neighbours with seed 1), build 4 minutes, frames 12 minutes, witness 2 minutes, identify 13 minutes, check
80 seconds (numpy). Memory: each step ran under a 3-4 GB cap.
実行時間（1 スレッド。負荷のかかった共用の計算機で計測）: local 20 分、mass 1 秒、enum 16 分（種 1 で近傍 62 個）、build 4 分、frames 12 分、
witness 2 分、identify 13 分、check 80 秒（numpy）。メモリ: どの段も 3〜4 GB の上限の下で動いた。
Run / 実行:  python3 code/supplementary/genus/genus.py local|mass|enum|build|frames|witness|identify
             python3 code/supplementary/genus/genus.py check
"""
import argparse
import os
import random
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "nebe"))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "produce"))
from lib import certs, data, exact  # noqa: E402
from lib.report import Report  # noqa: E402

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
    4: (24, (0, 0, 0, 36, 0, 168, 0)),            # mod-2 gluing of type bc, norm 8
    5: (20, (0, 0, 0, 0, 0, 180, 120)),           # no mod-2 frame, norm 8
    6: (288, (0, 12, 0, 36, 0, 660, 72)),         # L + L~
    7: (48, (0, 0, 0, 0, 0, 216, 48)),            # L_112
}
# Types of the mod-2 frames (frames). / mod 2 の枠の型（frames）。
FRAME_TYPES = {0: ["bb"], 1: ["bc"], 2: ["cc"], 3: ["bb", "cc"], 4: ["bc"], 5: [], 6: [], 7: ["cc"]}
# Minimum norm: 6 for the orthogonal sums, 8 where a witness is distributed, 10 for L_112 (Theorem A).
# 最小ノルム: 直交和は 6、証拠を配布する類は 8、L_112 は 10（定理 A）。
STATUS = {0: "orthogonal sum L + L, min 6", 1: "open (decided by a separate computation)",
          2: "orthogonal sum L~ + L~, min 6", 3: "gluing A = gluing B, min 8", 4: "min 8", 5: "min 8",
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


# ---------------------------------------------------------------------------------------------------------
# SageMath part / SageMath の部分
# ---------------------------------------------------------------------------------------------------------

def rmul(X, h):
    """Matrix of right multiplication by h in H (coordinates) on Q(zeta)^2 = Q^56 (row vectors).
    H の元 h（座標）の右乗法の、Q(ζ)^2 = Q^56 の行ベクトルへの行列。"""
    from sage.all import QQ, block_matrix
    ux, uy = X.helt(h)
    mul = X._mulmat
    return block_matrix(QQ, [[mul(ux), mul(uy)], [-mul(X.conj(uy)), mul(X.conj(ux))]], subdivide=False)


def star(X, h):
    """The canonical involution h -> h*. / 標準対合 h -> h*。"""
    x, y = X.helt(h)
    return X.hcoords((X.conj(x), -y))


def trtrd(u):
    """Tr_{K/Q} trd(u) for u in H (coordinates); Tr eta_j = -1. / H の元 u の Tr_{K/Q} trd(u)（Tr η_j = -1）。"""
    return -(u[0] + u[1] + u[2] + u[3])


def kelt(X, a, b):
    """The element a + b sqrt29 of K, in coordinates of H. / K の元 a + b√29 を H の座標で。"""
    return a * X.one + b * X.hcoords((X.sqrtp, X.F(0)))


def kred(ab):
    """Reduction of A + B sqrt29 modulo p = (pi), pi = (7 + sqrt29)/2: F_5 with sqrt29 -> 3.
    A + B√29 の p = (π) での剰余（F_5、√29 ↦ 3）。"""
    from sage.all import GF
    A, B = ab
    return GF(5)(A) + 3 * GF(5)(B)


def _hnf_rational(S):
    from sage.all import ZZ, lcm
    d = lcm([x.denominator() for x in S.list()])
    return (d * S).change_ring(ZZ).hermite_form(include_zero_rows=False).change_ring(S.base_ring()) / d


class Genus:
    r"""The ambient space H^2 with h = l_1 m_1* + l_2 m_2*, the lattice Lambda_0 = M + M, and Kneser neighbours.
    周囲の空間 H^2（h = l_1 m_1* + l_2 m_2*）、基準の格子 Λ_0 = M ⊕ M、Kneser の近傍。"""

    def __init__(self, out_dir):
        from cycloquat import CycloQuat
        from lattices import read_mats
        from sage.all import QQ, ZZ, block_matrix, matrix, vector, zero_matrix
        d = os.path.join(out_dir, "nebe")
        self.X = X = CycloQuat(29)
        self.M = M = read_mats(os.path.join(d, "M_order.txt"), 8, QQ)[0]       # Z-basis of M (rows, H coordinates)
        self.Lb = read_mats(os.path.join(d, "M_basis.txt"), N, QQ)[0]          # basis of L in Q(zeta)^2
        self.G = read_mats(os.path.join(d, "M_gram.txt"), N)[0]                # Gram matrix of L in that basis
        self.Z, self.W = read_mats(os.path.join(d, "M_generators.txt"), N)     # z, w on L
        Z8 = zero_matrix(QQ, 8, 8)
        self.P0 = block_matrix(QQ, [[M, Z8], [Z8, M]], subdivide=False)        # basis of Lambda_0 in H^2
        rows = [vector(QQ, list(r[:8])) for r in self.P0.rows()], [vector(QQ, list(r[8:])) for r in self.P0.rows()]
        Z8v = vector(QQ, 8)
        mul = lambda u, v: X.hmul(u, v) + Z8v                                    # noqa: E731 (empty sum -> 0)
        self.mul = mul
        self.h = [[mul(rows[0][i], star(X, rows[0][j])) + mul(rows[1][i], star(X, rows[1][j])) for j in range(16)]
                  for i in range(16)]
        TM = matrix(QQ, 8, 8, lambda i, j: trtrd(mul(M[i], M[j])))
        self.Mdual = TM.inverse() * M                                            # Tr trd(m_i n_j) = delta_ij
        self.form = lambda a: matrix(QQ, 16, 16, lambda i, j: trtrd(mul(a, self.h[i][j])))   # noqa: E731
        self.F0 = self.form(X.one)                                               # Tr trd h, positive definite
        self.Fm = [self.form(m) for m in M.rows()]
        self.D = [self.form(n) for n in self.Mdual.rows()]                       # h(x, y) in M iff all integral
        Pinv = self.P0.inverse()
        self.Lm = [(self.P0 * block_matrix(QQ, [[X.lmul_matrix(m), Z8], [Z8, X.lmul_matrix(m)]], subdivide=False) * Pinv)
                   for m in M.rows()]
        assert all(x in ZZ for A in self.Lm for x in A.list())
        self.Lm = [A.change_ring(ZZ) for A in self.Lm]
        self.d0 = self.F0.det()
        assert X.nrd(X.hcoords((X.sqrtp, X.F(0)))) == (29, 0)
        self.pi = kelt(X, QQ(7) / 2, QQ(1) / 2)                                  # pi = (7 + sqrt29)/2, norm 5
        self.pinv = kelt(X, QQ(7) / 10, -QQ(1) / 10)                             # pi~/5
        assert X.hmul(self.pi, self.pinv) == X.one
        self.Dpi = [self.form(X.hmul(n, self.pinv)) for n in self.Mdual.rows()]
        self.Lpi, self.Lpinv = self.lmul(self.pi), self.lmul(self.pinv)
        # A rank-1 idempotent of M/pM = M_2(F_5): trd = 1, nrd = 0 mod p (fixed seed).
        # M/pM ≅ M_2(F_5) の階数 1 の冪等元: trd ≡ 1, nrd ≡ 0 (mod p)（乱数シードは固定）。
        rng = random.Random(1)
        while True:
            c = vector(QQ, [rng.randint(-2, 2) for _ in range(8)])
            m = c * M
            n = X.nrd(m)
            t = X.nrd(X.one + m)
            tr = (t[0] - n[0] - 1, t[1] - n[1])
            if kred(n) == 0 and kred(tr) == 1:
                break
        self.e = m
        self.Le = self.lmul(m)
        assert all(x in ZZ for x in self.Le.list()) and all(x in ZZ for x in self.Lpi.list())
        Lbi = self.Lb.inverse()
        self.R = lambda q: self.Lb * rmul(X, q) * Lbi                            # noqa: E731 (right mult. on L)

    def lmul(self, a):
        """Left multiplication by a in H (Lambda_0 coordinates). / 左から a ∈ H を掛ける写像（Λ_0 座標）。"""
        from sage.all import QQ, block_matrix, zero_matrix
        Z8 = zero_matrix(QQ, 8, 8)
        A = self.X.lmul_matrix(a)
        return self.P0 * block_matrix(QQ, [[A, Z8], [Z8, A]], subdivide=False) * self.P0.inverse()

    def integral(self, C):
        from sage.all import ZZ
        return all(x in ZZ for Dj in self.D for x in (C * Dj * C.transpose()).list())

    def is_module(self, C):
        from sage.all import ZZ
        Ci = C.inverse()
        return all(x in ZZ for A in self.Lm for x in (C * A * Ci).list())

    def is_unimodular(self, C):
        return self.integral(C) and (C * self.F0 * C.transpose()).det() == self.d0

    def forms(self, C):
        """The nine integral forms [Tr trd h, Tr trd(m_k h)] on Lambda. / Λ 上の 9 個の整数値の形式。"""
        from sage.all import ZZ
        return [(C * F * C.transpose()).change_ring(ZZ) for F in [self.F0] + self.Fm]

    def random_sub(self, C, rng):
        """pi Lambda < N < Lambda with N / pi Lambda generated (as an M-module) by a random 2-dimensional
        subspace of e(Lambda / pi Lambda). / N/πΛ が e(Λ/πΛ) の無作為な 2 次元部分空間から（M-加群として）生成される πΛ ⊂ N ⊂ Λ。"""
        from sage.all import GF, ZZ, identity_matrix, matrix
        F = GF(5)
        Ci = C.inverse()
        Pi = (C * self.Lpi * Ci).change_ring(ZZ)
        E = (C * self.Le * Ci).change_ring(ZZ)
        Lm = [(C * A * Ci).change_ring(ZZ) for A in self.Lm]
        Pb = Pi.change_ring(F).row_space()
        assert Pb.dimension() == 8
        V = F ** 16
        Q = V.quotient(Pb)
        Ue = [Q.lift(Q(r)) for r in E.change_ring(F).row_space().basis()]
        Ue = matrix(F, [Q.lift(x) for x in matrix(F, [Q(u) for u in Ue]).row_space().basis()])
        assert Ue.nrows() == 4
        while True:
            Wm = matrix(F, 2, 4, [F(rng.randrange(5)) for _ in range(8)])
            if Wm.rank() == 2:
                break
        w = Wm * Ue
        gens = [w[i] * A.change_ring(F) for i in range(2) for A in [identity_matrix(ZZ, 16)] + Lm]
        S = matrix(F, gens).row_space() + Pb
        assert S.dimension() == 12
        rows = matrix(ZZ, [[ZZ(x) for x in r] for r in S.basis()]).stack(5 * identity_matrix(ZZ, 16))
        Nb = rows.hermite_form(include_zero_rows=False)
        return Nb.change_ring(C.base_ring()) * C

    def neighbour(self, C, rng, tries=200):
        """A p-neighbour of Lambda (Siegel type). / Λ の p-近傍（Siegel 型）。"""
        from sage.all import ZZ
        for _ in range(tries):
            Nn = self.random_sub(C, rng)
            if all(x in ZZ for Dj in self.Dpi for x in (Nn * Dj * Nn.transpose()).list()):
                break
        else:
            raise RuntimeError("no Lagrangian N found")
        Np = Nn * self.Lpinv
        for _ in range(tries):
            C2 = self.random_sub(Np, rng)
            if not self.integral(C2):
                continue
            if abs(C.det()) / abs(_hnf_rational(C.stack(C2)).det()) == 5 ** 4:
                return C2
        raise RuntimeError("no neighbour found")

    def reduce(self, C):
        """LLL-reduced basis for Tr trd h. / Tr trd h について LLL 簡約した基底。"""
        from sage.all import ZZ, matrix, pari
        Gm = (C * self.F0 * C.transpose()).change_ring(ZZ)
        return matrix(ZZ, pari(Gm).qflllgram().mattranspose().sage()) * C

    def aut(self, C):
        from sage.all import ZZ, pari
        return ZZ(pari(self.forms(C)).qfauto()[0])

    def iso(self, C1, C2):
        from sage.all import pari
        return pari(self.forms(C1)).qfisom(pari(self.forms(C2))) != 0

    def invariant(self, C, bound=14):
        """Numbers of +-pairs of vectors of Tr trd h = 2, 4, ..., bound. / Tr trd h = 2, 4, …, bound の ± 対の本数。"""
        from sage.all import ZZ, pari, vector
        Gm = (C * self.F0 * C.transpose()).change_ring(ZZ)
        vs = pari(Gm).qfminim(bound)[2]
        cnt = [0] * (bound // 2 + 1)
        for j in range(len(vs)):
            v = vector(ZZ, [ZZ(t) for t in vs[j]])
            cnt[int(v * Gm * v) // 2] += 1
        return tuple(cnt[1:])

    def short(self, C, bound):
        """Vectors of Lambda with Tr trd h <= bound (one of each +-pair), in Lambda_0 coordinates.
        Tr trd h ≤ bound の Λ のベクトル（± の片方）、Λ_0 座標。"""
        from sage.all import ZZ, pari, vector
        Gm = (C * self.F0 * C.transpose()).change_ring(ZZ)
        vs = pari(Gm).qfminim(bound)[2]
        return [vector(ZZ, [ZZ(t) for t in vs[j]]) * C for j in range(len(vs))]

    def hval(self, Fs, v):
        """h(v, v) in K as (A, B) = A + B sqrt29: Tr trd h = 4A, Tr trd(sqrt29 h) = 116B.
        h(v, v) ∈ K を (A, B) = A + B√29 で。"""
        from sage.all import QQ
        return (QQ(v * self.F0 * v) / 4, QQ(v * Fs * v) / 116)

    def saturate(self, C, v):
        """J = Lambda cap H v (Lambda_0 coordinates). / J = Λ ∩ Hv（Λ_0 座標）。"""
        from sage.all import QQ, ZZ, identity_matrix, lcm, matrix
        Ci = C.inverse()
        V = matrix(QQ, [v * self.lmul(b) for b in identity_matrix(QQ, 8).rows()]) * Ci
        d = lcm([x.denominator() for x in V.list()])
        Jz = (d * V).change_ring(ZZ).row_module().basis_matrix().saturation()
        return Jz.change_ring(QQ) * C

    def build_X(self, C):
        """(B, G_X): basis of X = L tensor_M Lambda in the coordinates of L + L (basis Lb), Gram matrix for
        diag(G, G); then LLL-reduced. / X = L ⊗_M Λ の L ⊕ L 座標での基底と Gram 行列（diag(G, G)）。LLL 簡約したもの。"""
        from sage.all import QQ, ZZ, block_matrix, lcm, matrix, pari, zero_matrix
        Hc = C * self.P0
        blocks = [self.R(r[:8]).augment(self.R(r[8:])) for r in Hc.rows()]     # rows x_k tensor lambda
        Gen = block_matrix(QQ, [[b] for b in blocks], subdivide=False)
        d = lcm([x.denominator() for x in Gen.list()])
        Bx = (d * Gen).change_ring(ZZ).hermite_form(include_zero_rows=False).change_ring(QQ) / d
        G2 = block_matrix(QQ, [[self.G, zero_matrix(QQ, N, N)], [zero_matrix(QQ, N, N), self.G]], subdivide=False)
        Gx = Bx * G2 * Bx.transpose()
        assert all(x in ZZ for x in Gx.list())
        U = matrix(ZZ, pari(Gx.change_ring(ZZ)).qflllgram().mattranspose().sage())
        assert abs(U.det()) == 1
        Bx = U * Bx
        return Bx, (Bx * G2 * Bx.transpose()).change_ring(ZZ)

    def unit_actions(self, C):
        """Generators of U(Lambda) (qfauto) as matrices on L + L: u acts on Lambda by right multiplication by
        Q in GL_2(H), and on X by id tensor u. / U(Λ) の生成元（qfauto）を L ⊕ L 上の行列として。"""
        from sage.all import QQ, ZZ, block_matrix, matrix, pari, zero_matrix
        X = self.X
        gens = pari(self.forms(C)).qfauto()[1]
        out = []
        for g in gens:
            g = matrix(ZZ, g.sage())
            U0 = C.inverse() * g.transpose() * C
            T = self.P0.inverse() * U0 * self.P0
            Q = [[X.one * T[8 * a:8 * a + 8, 8 * b:8 * b + 8] for b in range(2)] for a in range(2)]
            for a in range(2):
                for b in range(2):
                    Rq = X.rmul_matrix(Q[a][b]) if Q[a][b] != 0 else zero_matrix(QQ, 8, 8)
                    assert Rq == T[8 * a:8 * a + 8, 8 * b:8 * b + 8], "not a right multiplication"
            Rb = [[self.R(Q[a][b]) for b in range(2)] for a in range(2)]
            out.append(block_matrix(QQ, Rb, subdivide=False))
        return out


def closure(gens, n):
    """All elements of the finite group generated by integer matrices. / 整数行列が生成する有限群の全元。"""
    from sage.all import ZZ, identity_matrix
    Id = identity_matrix(ZZ, n)
    elts = {tuple(Id.list()): Id}
    fr = [Id]
    while fr:
        nf = []
        for a in fr:
            for g in gens:
                b = a * g
                k = tuple(b.list())
                if k not in elts:
                    elts[k] = b
                    nf.append(b)
        fr = nf
    return list(elts.values())


def order_of(u, n):
    from sage.all import ZZ, identity_matrix
    Id = identity_matrix(ZZ, n)
    o, P = 1, u
    while P != Id:
        P, o = P * u, o + 1
    return o


def write_rational_mats(path, header, mats):
    with open(path, "w") as f:
        for line in header.splitlines():
            f.write("# " + line + "\n")
        for k, A in enumerate(mats):
            if k:
                f.write("\n")
            for r in A.rows():
                f.write(" ".join(str(x) for x in r) + "\n")


def gdir(out_dir):
    d = os.path.join(out_dir, "genus")
    os.makedirs(d, exist_ok=True)
    return d


def load_lambdas(out_dir):
    from lattices import read_mats
    from sage.all import QQ
    return read_mats(os.path.join(out_dir, "genus", "lambda.txt"), 16, QQ)


def algebra_dim(gens, p):
    """Dimension of the unital F_p-algebra generated by the integer matrices gens.
    整数行列 gens が F_p 上に生成する（単位元つき）代数の次元。"""
    from sage.all import GF, matrix
    F = GF(p)
    n = gens[0].nrows()
    gs = [g.change_ring(F) for g in gens]
    basis = matrix(F, 0, n * n)
    queue = [matrix(F, n, n, 1)]
    while queue:
        A = queue.pop()
        B = basis.stack(matrix(F, 1, n * n, A.list()))
        r = B.rank()
        if r > basis.nrows():
            basis = B.echelon_form()[:r]
            queue += [A * g for g in gs]
    return basis.nrows()


def commutant_dim(gens, p):
    """dim_{F_p} of {A : A g = g A for g in gens} on F_p^n. / F_p^n 上で gens と可換な行列の空間の次元。"""
    from sage.all import GF, identity_matrix
    F = GF(p)
    n = gens[0].nrows()
    I = identity_matrix(F, n)
    rows = None
    for g in gens:
        gp = g.change_ring(F)
        K = I.tensor_product(gp.transpose()) - gp.tensor_product(I)
        rows = K if rows is None else rows.stack(K)
    return n * n - rows.rank()


def cmd_local(a):
    from sage.all import ZZ
    rep = Report("s25_genus_local", a.out)
    S = Genus(rep.out_dir)
    Rm = [S.R(m) for m in S.M.rows()]
    rep.check("right multiplications by the Z-basis of M are integral on L and commute with z, w",
              all(x in ZZ for A in Rm for x in A.list()) and all(A * g == g * A for A in Rm for g in (S.Z, S.W)))
    Rm = [A.change_ring(ZZ) for A in Rm]
    rep.check("z, w preserve the Gram matrix of L", all(g * S.G * g.transpose() == S.G for g in (S.Z, S.W)))
    dims = {}
    for p in PRIMES:
        da = algebra_dim([S.Z, S.W], p)
        de = commutant_dim(Rm, p)
        dims[p] = [da, de]
        rep.value(f"p = {p}: dim of the algebra spanned by z, w on L/pL, dim End_(M/pM)(L/pL)", [da, de])
        rep.check(f"p = {p}: both are 392 (the image of the group ring is maximal at p)", da == de == 392)
    rep.finish()


def cmd_mass(a):
    from sage.all import QQ, ZZ, bernoulli, bernoulli_polynomial, kronecker, pari, polygen, sigma
    from lattices import read_mats
    rep = Report("s25_genus_mass", a.out)
    x = polygen(QQ)
    f = 29

    def Bchi(k):
        Bk = bernoulli_polynomial(x, k)
        return f ** (k - 1) * sum(kronecker(f, t) * Bk(QQ(t) / f) for t in range(1, f + 1))

    def zetaK(k):                                   # zeta_K(1 - k) = zeta(1 - k) L(1 - k, chi) = (-B_k/k)(-B_{k,chi}/k)
        return (-bernoulli(k) / k) * (-Bchi(k) / k)
    z1, z3 = zetaK(2), zetaK(4)
    rep.value("generalized Bernoulli numbers B_{2,chi}, B_{4,chi} (chi = (29/.))", [str(Bchi(2)), str(Bchi(4))])
    rep.value("zeta_K(-1), zeta_K(-3)", [str(z1), str(z3)])
    rep.check("zeta_K(-1) = 1/2 and zeta_K(-3) = 157/20", z1 == QQ(1) / 2 and z3 == QQ(157) / 20)
    # Siegel: zeta_K(-1) = (1/60) sum sigma_1((D - b^2)/4), zeta_K(-3) = (1/120) sum sigma_3((D - b^2)/4), b odd, b^2 < D.
    bs = [b for b in range(-5, 6) if b % 2 and b * b < f]
    s1 = QQ(sum(sigma((f - b * b) // 4, 1) for b in bs)) / 60
    s3 = QQ(sum(sigma((f - b * b) // 4, 3) for b in bs)) / 120
    rep.check("Siegel's divisor-sum formulas give the same values", s1 == z1 and s3 == z3)
    num = [float(pari(f"lfun(lfuncreate(x^2 - {f}), {s})")) for s in (-1, -3)]
    rep.value("PARI lfun (numerical) at -1, -3", num)
    rep.check("PARI lfun agrees to 1e-12", abs(num[0] - 0.5) < 1e-12 and abs(num[1] - 7.85) < 1e-12)
    mass = abs(z1 * z3) / 16
    rep.value("mass 2^{-4} |zeta_K(-1) zeta_K(-3)| [GHY01, Prop. 9.4 (= 9.3 for S_D empty); rank 2, d = 2, D unramified at finite places]",
              str(mass))
    rep.check("the mass is 157/640", mass == QQ(MASS.numerator) / MASS.denominator)
    from cycloquat import CycloQuat
    X = CycloQuat(29)
    d = os.path.join(rep.out_dir, "nebe")
    u = [2 * X.units_mod_center(read_mats(os.path.join(d, f"{nm}_order.txt"), 8, QQ)[0]) for nm in ("M", "Mtilde")]
    rep.value("|{u in O : nrd u = 1}| for O = M, M~", u)
    rep.check("rank 1: 1/24 + 1/12 = 2^{-2} |zeta_K(-1)|", u == [24, 12] and QQ(1) / u[0] + QQ(1) / u[1] == abs(z1) / 4)
    rep.finish()


def cmd_enum(a):
    from sage.all import QQ, identity_matrix
    rep = Report("s25_genus_enum", a.out)
    S = Genus(rep.out_dir)
    rng = random.Random(a.seed)
    rep.value("seed of the walk", a.seed)
    C0 = identity_matrix(QQ, 16)
    rep.check("Lambda_0 = M + M is an M-module, unimodular for h", S.is_module(C0) and S.is_unimodular(C0))
    cls = [dict(C=C0, U=S.aut(C0), inv=S.invariant(C0), step=0)]
    mass = lambda: sum(Fraction(1, int(c["U"])) for c in cls)    # noqa: E731
    step = 0
    while mass() < MASS and step < a.max_steps:
        src = cls[rng.randrange(len(cls))]
        try:
            C = S.reduce(S.neighbour(src["C"], rng))
        except RuntimeError as e:
            rep.log("skip:", e)
            continue
        step += 1
        assert S.is_module(C) and S.is_unimodular(C)
        inv = S.invariant(C)
        U = None
        found = None
        for j, c in enumerate(cls):
            if c["inv"] != inv:
                continue
            if U is None:
                U = S.aut(C)
            if c["U"] == U and S.iso(c["C"], C):
                found = j
                break
        if found is None:
            U = U or S.aut(C)
            cls.append(dict(C=C, U=U, inv=inv, step=step))
            rep.log(f"step {step}: new class, |U| = {U}, invariants {inv}; mass {mass()} = {float(mass() / MASS):.4f} of 157/640")
    rep.value("steps of the walk", step)
    rep.check("the mass 157/640 is reached", mass() == MASS)
    labels = {}
    for c in cls:
        key = (int(c["U"]), tuple(int(t) for t in c["inv"]))
        j = next((j for j, v in LABELS.items() if v == key), None)
        rep.check(f"class found at step {c['step']} (|U| = {key[0]}) has the invariants of a labelled class", j is not None)
        rep.check(f"label {j} is not taken twice", j not in labels)
        labels[j] = c
    rep.check("8 classes, labels 0-7", sorted(labels) == list(range(NCLASS)))
    rep.value("|U(Lambda_j)|, j = 0..7", [int(labels[j]["U"]) for j in range(NCLASS)])
    rep.value("step at which class j was found", [labels[j]["step"] for j in range(NCLASS)])
    write_rational_mats(os.path.join(gdir(rep.out_dir), "lambda.txt"),
                        "Lambda_j, j = 0..7: 16 x 16 rational basis matrices in the coordinates of Lambda_0 = M + M "
                        f"(genus.py enum, seed {a.seed})", [labels[j]["C"] for j in range(NCLASS)])
    cdir = a.certificates or certs.DEFAULT_DIR
    tmp = os.path.join(cdir, CLASSES_FILE + ".tmp")
    with open(tmp, "w") as f:
        f.write("# The genus of rank-2 unimodular Hermitian lattices Lambda over the maximal order M (centralizer order 24),\n"
                "# K = Q(sqrt29); X_j = L_{56,2}(M) tensor_M Lambda_j. One line per class j:\n"
                "#   j  |U(Lambda_j)|  n_2 n_4 ... n_14\n"
                "# where n_k is the number of +-pairs of vectors of Lambda_j with Tr_{K/Q} trd h(v, v) = k.\n"
                "# |U| by PARI qfauto (code/supplementary/genus/genus.py enum, seed %d); sum 1/|U| = 157/640.\n"
                "# 種の 8 類: 類の番号 j、|U(Λ_j)|、Tr trd h = 2, 4, …, 14 のベクトルの ± 対の本数。\n" % a.seed)
        for j in range(NCLASS):
            c = labels[j]
            f.write(" ".join(str(int(t)) for t in [j, c["U"]] + list(c["inv"])) + "\n")
    os.replace(tmp, os.path.join(cdir, CLASSES_FILE))
    rep.log(f"wrote {gdir(rep.out_dir)}/lambda.txt and {cdir}/{CLASSES_FILE}")
    rep.finish()


def embedding_coords(S, out_dir, rep, data_dir=None):
    """P (56 x 56 rational): coordinates in the basis Lb of L_{56,2}(M) -> coordinates in the basis of
    data/L56_gram.txt, through the embedding e of nebe/reduction_to_nebe.py (rows of Emb = e(basis of L~) in the
    LLL-reduced basis of L_{56,2}(M)). / L_{56,2}(M) の基底 Lb での座標 -> data/L56_gram.txt の基底での座標。"""
    from lattices import read_mats
    from sage.all import ZZ, matrix, pari
    U = pari(S.G).qflllgram().sage().transpose().change_ring(ZZ)                  # as in lattices.load(reduce=True)
    assert abs(U.det()) == 1
    Gred = U * S.G * U.transpose()
    Emb = read_mats(os.path.join(out_dir, "nebe", "embedding_L_into_M.txt"), N)[0]
    G = matrix(ZZ, data.gram(data_dir).tolist())
    rep.check("the embedding e satisfies Emb G_M Emb^T = 2 G (G = data/L56_gram.txt)", Emb * Gred * Emb.transpose() == 2 * G)
    return U, Emb, U.inverse() * Emb.inverse()


def cmd_build(a):
    from sage.all import QQ, ZZ, block_matrix, identity_matrix, lcm, matrix, zero_matrix
    rep = Report("s25_genus_build", a.out)
    S = Genus(rep.out_dir)
    lams = load_lambdas(rep.out_dir)
    _, _, P = embedding_coords(S, rep.out_dir, rep, a.data)
    G = matrix(ZZ, data.gram(a.data).tolist())
    g1, g2 = [matrix(ZZ, g.tolist()) for g in data.generators(a.data)]
    Z = zero_matrix(QQ, N, N)
    PP = block_matrix(QQ, [[P, Z], [Z, P]], subdivide=False)
    GG = block_matrix(ZZ, [[G, zero_matrix(ZZ, N, N)], [zero_matrix(ZZ, N, N), G]], subdivide=False)
    cdir = a.certificates or certs.DEFAULT_DIR
    info = []
    for j, C in enumerate(lams):
        Bx, Gx = S.build_X(C)
        ok = Gx.is_symmetric() and all(Gx[i, i] % 2 == 0 for i in range(NX)) and Gx.det() == 1
        rep.check(f"class {j}: X = L tensor Lambda is even unimodular of dimension 112", ok and Gx.nrows() == NX)
        B = 2 * Bx * PP                                                       # form diag(G, G)/2 as in (3.1)
        d = lcm([x.denominator() for x in B.list()])
        D = (d * B).change_ring(ZZ)
        rep.check(f"class {j}: D diag(G, G) D^T = 2 d^2 G_X", D * GG * D.transpose() == 2 * d * d * Gx)
        Di = D.change_ring(QQ).inverse()
        for k, g in enumerate((g1, g2)):
            s = D * block_matrix(ZZ, [[g, zero_matrix(ZZ, N, N)], [zero_matrix(ZZ, N, N), g]], subdivide=False) * Di
            rep.check(f"class {j}: g{k + 1} (data/) acts on X_j by an integer matrix preserving G_X",
                      all(x in ZZ for x in s.list()) and s.change_ring(ZZ) * Gx * s.change_ring(ZZ).transpose() == Gx)
        mn = min(Gx.diagonal())
        info.append([j, int(d), int(max(abs(x) for x in Gx.list())), int(max(abs(x) for x in D.list())), int(mn)])
        certs.save_matrix(os.path.join(cdir, gram_file(j)), np.array(Gx.rows(), dtype=np.int64),
                          f"G_X (112 x 112): Gram matrix of X_{j} = L_(56,2)(M) tensor_M Lambda_{j}, class {j} of the genus of\n"
                          "rank-2 unimodular Hermitian lattices over M (LLL-reduced basis; PARI qflllgram).\n"
                          "The basis in the coordinates of (3.1) is certificates/" + basis_file(j) + ".\n"
                          "Written by code/supplementary/genus/genus.py build.\n"
                          f"G_X（112 × 112）: 種の類 {j} の X_{j} = L_(56,2)(M) ⊗_M Λ_{j} の Gram 行列（LLL 簡約した基底）。")
        tmp = os.path.join(cdir, basis_file(j) + ".tmp")
        with open(tmp, "w") as f:
            for line in (f"d and D = d B (112 x 112): B is the basis of X_{j} (rows) in the coordinates of L + L, L = data/L56_gram.txt,\n"
                         "with the form diag(G, G)/2 as in (3.1): D diag(G, G) D^T = 2 d^2 G_X, G_X = certificates/" + gram_file(j) + ".\n"
                         "The generators g1, g2 of data/sl2_29_generators.txt act on X_j: D diag(g, g) D^-1 is an integer matrix.\n"
                         "Written by code/supplementary/genus/genus.py build.\n"
                         f"d と D = d B: B は (3.1) と同じ座標（L ⊕ L、形式 diag(G, G)/2）での X_{j} の基底。最初の整数が d。").splitlines():
                f.write("# " + line + "\n")
            f.write(f"{int(d)}\n")
            for r in D.rows():
                f.write(" ".join(str(int(v)) for v in r) + "\n")
        os.replace(tmp, os.path.join(cdir, basis_file(j)))
    rep.value("per class: [j, d, max |G_X|, max |D|, min diagonal of G_X]", info)
    rep.finish()


def cmd_frames(a):
    from sage.all import QQ, ZZ, lcm
    rep = Report("s25_genus_frames", a.out)
    S = Genus(rep.out_dir)
    lams = load_lambdas(rep.out_dir)
    Fs = S.form(kelt(S.X, 0, 1))
    want = {(QQ(2), QQ(0)), (QQ(7), QQ(1)), (QQ(7), QQ(-1))}                       # h = 2, 2 pi, 2 pi~
    HNAMES = {(QQ(2), QQ(0)): "2", (QQ(7), QQ(1)): "2pi", (QQ(7), QQ(-1)): "2pi~"}
    for j, C in enumerate(lams):
        det = (C * S.F0 * C.transpose()).det()
        Js = {}                                                              # J -> h-values of its short vectors
        for v in S.short(C, a.bound):
            hv = S.hval(Fs, v)
            if hv not in want:
                continue
            J = S.saturate(C, v)
            key0 = tuple(J.echelon_form().list())
            Js.setdefault(key0, [J, set()])[1].add(hv)
        types, mod2 = {}, set()
        for J, hvs in Js.values():
            K = (C * S.F0 * J.transpose()).change_ring(QQ).left_kernel().basis_matrix()
            dd = lcm([x.denominator() for x in K.list()] + [1])
            Jp = (dd * K).change_ring(ZZ).row_module().basis_matrix().saturation().change_ring(QQ) * C
            dJ = (J * S.F0 * J.transpose()).det()
            dJp = (Jp * S.F0 * Jp.transpose()).det()
            idx = (dJ * dJp / det).sqrt()
            mJ = [m for m in (1, 2, 3, 4, 5, 6)
                  if all(x in ZZ for Dj in S.D for Y in (J, Jp) for x in (Y * Dj * Y.transpose() / m).list())]
            hs = " and ".join(HNAMES[h] for h in sorted(hvs))
            t = (hs, str(idx.factor()) if idx != 1 else "1", max(mJ))
            if idx == 2 ** 8 and max(mJ) == 2:
                typ = lambda Y: "b" if any(S.hval(Fs, w) == (2, 0) for w in S.short(Y, 8)) else "c"   # noqa: E731
                tt = "".join(sorted(typ(J) + typ(Jp)))
                t = t + (tt,)
                mod2.add(tt)
            types[str(t)] = types.get(str(t), 0) + 1
        rep.value(f"class {j}: (values h(v, v) in {{2, 2pi, 2pi~}} of the vectors v of J with Tr trd h <= {a.bound}, "
                  "[Lambda : J + J'], largest m with h(J, J), h(J', J') in mM[, type of the mod-2 frame]): number of J",
                  dict(sorted(types.items())))
        rep.value(f"class {j}: types of the mod-2 frames", sorted(mod2))
        rep.check(f"class {j}: mod-2 frames of types {FRAME_TYPES[j]}", sorted(mod2) == FRAME_TYPES[j])
    rep.finish()


def fixed_basis(g):
    """Basis (rows) of the fixed sublattice {v : v g = v} (saturated). / 固定部分格子の基底（行）。"""
    from sage.all import ZZ, identity_matrix
    return (g - identity_matrix(ZZ, g.nrows())).left_kernel().basis_matrix()


def pruned_witness(Gs, rep, trials=20):
    """A vector of norm <= 8 of the positive definite integer Gram matrix Gs by BKZ-30 and pruned enumeration
    (fpylll), with fixed random seeds, or None. / BKZ-30 と枝刈りつき列挙（fpylll、乱数シードは固定）でノルム 8 以下のベクトルを探す。"""
    from fpylll import BKZ, GSO, LLL, Enumeration, EnumerationError, IntegerMatrix, Pruning
    from fpylll.algorithms.bkz2 import BKZReduction
    from sage.all import ZZ, identity_matrix, matrix, random_matrix, set_random_seed, vector
    n = Gs.nrows()
    for trial in range(trials):
        set_random_seed(trial)
        T = identity_matrix(ZZ, n) if trial == 0 else random_matrix(ZZ, n, n, algorithm="unimodular", upper_bound=2)
        Gt = T * Gs * T.transpose()
        A = IntegerMatrix.from_matrix([[int(v) for v in r] for r in Gt.rows()])
        Um = IntegerMatrix.identity(n)
        Mg = GSO.Mat(A, U=Um, gram=True, float_type="mpfr", flags=GSO.INT_GRAM)
        Mg.update_gso()
        LLL.Reduction(Mg)()
        BKZReduction(Mg)(BKZ.Param(block_size=30, max_loops=6, strategies=BKZ.DEFAULT_STRATEGY))
        Uq = matrix(ZZ, n, n, lambda i, k: Um[i, k]) * T
        Gr = Uq * Gs * Uq.transpose()
        M2 = GSO.Mat(IntegerMatrix.from_matrix([[int(v) for v in r] for r in Gr.rows()]), gram=True, float_type="ld",
                     flags=GSO.INT_GRAM)
        M2.update_gso()
        r = [M2.get_r(i, i) for i in range(n)]
        pr = Pruning.run(8.5, 10 ** 7, [r], 0.5, flags=Pruning.GRADIENT)
        try:
            sol = Enumeration(M2).enumerate(0, n, 8.5, 0, pruning=pr.coefficients)
        except EnumerationError:
            rep.log(f"  trial {trial}: nothing found (pruned enumeration)")
            continue
        c = vector(ZZ, [int(round(x)) for x in sol[0][1]])
        v = c * Uq
        nv = v * Gs * v
        rep.log(f"  trial {trial}: vector of norm {nv}")
        if 0 < nv <= 8:
            return v
    return None


def cmd_witness(a):
    from sage.all import ZZ, block_matrix, matrix, pari, vector, zero_matrix
    rep = Report("s25_genus_witness", a.out)
    S = Genus(rep.out_dir)
    lams = load_lambdas(rep.out_dir)
    two = lambda A: block_matrix(ZZ, [[A, zero_matrix(ZZ, N, N)], [zero_matrix(ZZ, N, N), A]], subdivide=False)   # noqa: E731
    cdir = a.certificates or certs.DEFAULT_DIR
    rows = []
    for j in WITNESS_CLASSES:
        C = lams[j]
        Bx, Gx = S.build_X(C)
        rep.check(f"class {j}: G_X equals certificates/{gram_file(j)}",
                  np.array_equal(np.array(Gx.rows(), dtype=np.int64), certs.load_matrix(gram_file(j), NX, cdir)))
        Bxi = Bx.inverse()
        toX = lambda A: (Bx * A * Bxi).change_ring(ZZ)                         # noqa: E731
        Uel = closure([toX(A) for A in S.unit_actions(C)], NX)
        rep.check(f"class {j}: U(Lambda) acting on X_j has order {LABELS[j][0]} and preserves G_X",
                  len(Uel) == LABELS[j][0] and all(u * Gx * u.transpose() == Gx for u in Uel))
        Zx, Wx = toX(two(S.Z)), toX(two(S.W))
        v = None
        if j in (3, 4):
            s = Zx * Wx
            if s ** 3 != identity(NX):
                s = -s
            rep.check(f"class {j}: s = +-z w has order 3", s ** 3 == identity(NX) and s != identity(NX))
            for u in Uel:
                if u == identity(NX) or u ** 3 != identity(NX):
                    continue
                K = fixed_basis(s * u)
                Gk = K * Gx * K.transpose()
                U = matrix(ZZ, pari(Gk).qflllgram().mattranspose().sage())
                Gr = U * Gk * U.transpose()
                r = pari(Gr).qfminim(8, 10)
                if ZZ(r[0]) > 0:
                    c = vector(ZZ, [ZZ(t) for t in r[2][0]])
                    v = c * U * K
                    rep.value(f"class {j}: fixed sublattice of s u (s of order 3, u of order 3): dimension, vectors of norm <= 8 "
                              "(qfminim, +- counted twice)", [K.nrows(), int(ZZ(r[0]))])
                    break
        else:
            s = Wx
            rep.check(f"class {j}: s = w has order 4", order_of(s, NX) == 4)
            for u in Uel:
                if order_of(u, NX) != 4:
                    continue
                K = fixed_basis(s * u)
                if K.nrows() != N:
                    continue
                Gk = K * Gx * K.transpose()
                rep.log(f"class {j}: fixed sublattice of s u (s = w, u of order 4): dimension {K.nrows()}, det {Gk.det()}")
                c = pruned_witness(Gk, rep)
                if c is not None:
                    v = c * K
                    rep.value(f"class {j}: fixed sublattice of s u (s = w of order 4, u of order 4): dimension, det",
                              [K.nrows(), int(Gk.det())])
                    break
        rep.check(f"class {j}: a vector v with v G_X v^T = 8 (exact)", v is not None and v * Gx * v == 8)
        rows.append([j] + [int(t) for t in v])
    tmp = os.path.join(cdir, WITNESS_FILE + ".tmp")
    with open(tmp, "w") as f:
        f.write("# Norm-8 vectors of X_j, one per line: the class j, then the 112 coordinates in the basis of\n"
                "# certificates/genus_class_<j>.txt (v G_X v^T = 8). Classes 3, 4, 5. Written by code/supplementary/genus/genus.py witness.\n"
                "# X_j のノルム 8 のベクトル（1 行に 1 本）: 類 j と、genus_class_<j>.txt の基底での座標 112 個。\n")
        for r in rows:
            f.write(" ".join(str(t) for t in r) + "\n")
    os.replace(tmp, os.path.join(cdir, WITNESS_FILE))
    rep.log(f"wrote {cdir}/{WITNESS_FILE}")
    rep.finish()


def identity(n):
    from sage.all import ZZ, identity_matrix
    return identity_matrix(ZZ, n)


def equivariant_isometries(BX, GX, BY, GY, comm, rep, label):
    """S-equivariant isometries X -> Y for two lattices in the same space V + V (bases BX, BY, rational rows),
    S acting diagonally and comm a Q-basis of End_S(V). T = BX Phi BY^-1 with Phi = [[a, b], [c, d]], a, ..., d
    in span(comm); on the integral T, Q(T) = tr(GX^-1 T GY T^T) is positive definite and 112 on isometries;
    all T with Q <= 112 are enumerated (qfminim_checked) and T GY T^T = GX is tested exactly. Returns the
    isometries up to sign (rows of T: basis of X in the basis of Y).
    同じ空間 V ⊕ V の中の 2 つの格子の間の S 同変な等長写像（isometry_ab.py と同じ方法）。符号を除いて返す。"""
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
    rows = {tuple(col) for col in zip(*[g.list() for g in gens])}
    rows.discard(tuple([QQ(0)] * k))
    rows = [list(r) for r in rows]
    d = lcm([QQ(x).denominator() for r in rows for x in r])
    span = matrix(ZZ, 0, k)
    for i in range(0, len(rows), 200):
        span = span.stack(matrix(ZZ, [[int(d * x) for x in r] for r in rows[i:i + 200]])).hermite_form(include_zero_rows=False)
    assert span.nrows() == k
    Hb = (span.change_ring(QQ) / d).inverse().transpose()
    Xs = []
    for row in Hb.rows():
        T = sum(c * g for c, g in zip(row, gens))
        assert all(x in ZZ for x in T.list())
        Xs.append(T.change_ring(ZZ))
    GXi = GX.inverse()
    assert all(x in ZZ for x in GXi.list())
    GXi = GXi.change_ring(ZZ)
    Ys = [GXi * T * GY for T in Xs]
    Q = matrix(ZZ, [Y.list() for Y in Ys]) * matrix(ZZ, [T.list() for T in Xs]).transpose()
    Q = Q + Q.transpose()                                                    # 2 Q
    assert Q.is_positive_definite()
    cands = qfminim_checked(Q, 2 * NX)
    isos = [T for T in (sum(ci * Ti for ci, Ti in zip(c, Xs)) for c in cands) if T * GY * T.transpose() == GX]
    rep.value(f"{label}: integral S-equivariant maps with Q <= 112 (up to sign), isometries among them", [len(cands), len(isos)])
    return isos


def read_basis(j, cdir):
    """(d, D) from certificates/genus_basis_<j>.txt. / genus_basis_<j>.txt の (d, D)。"""
    v = data.read_integers(certs.path_checked(basis_file(j), cdir))
    assert v.size == 1 + NX * NX, basis_file(j)
    return int(v[0]), v[1:].reshape(NX, NX)


def cmd_identify(a):
    from isometry_ab import lift_class_A
    from lattices import load as load_nebe
    from p1_centralizer import commutant_basis
    from sage.all import QQ, ZZ, block_matrix, identity_matrix, matrix, zero_matrix
    rep = Report("s25_genus_identify", a.out)
    cdir = a.certificates or certs.DEFAULT_DIR
    g1, g2 = [matrix(ZZ, g.tolist()) for g in data.generators(a.data)]
    tau = matrix(ZZ, data.tau(a.data).tolist())
    I, Z = identity_matrix(ZZ, N), zero_matrix(ZZ, N, N)
    commL = commutant_basis([g1, g2], N)
    rep.check("End_S(L~) (data/) has rank 8", len(commL) == 8)
    GX = {}
    BX = {}
    for j in range(NCLASS):
        GX[j] = matrix(ZZ, certs.load_matrix(gram_file(j), NX, cdir).tolist())
        d, D = read_basis(j, cdir)
        BX[j] = matrix(ZZ, D.tolist()).change_ring(QQ) / d
    # class 7 -> L_112, basis (3.1) / 類 7 -> L_112（基底 (3.1)）
    BR = block_matrix(ZZ, [[I, tau], [Z, 2 * I]], subdivide=False).change_ring(QQ)
    GR = matrix(ZZ, data.gram_R(data.gram(a.data), data.tau(a.data)).tolist())
    isos = equivariant_isometries(BX[7], GX[7], BR, GR, commL, rep, "class 7 -> L_112")
    rep.check("class 7 is S-equivariantly isometric to L_112", len(isos) > 0)
    T7 = min(isos, key=lambda T: (max(abs(x) for x in T.list()), sum(abs(x) for x in T.list())))
    rep.check("T G_R T^T = G_7 and det T = +-1", T7 * GR * T7.transpose() == GX[7] and abs(T7.det()) == 1)
    certs.save_matrix(os.path.join(cdir, ISO7_FILE), np.array(T7.rows(), dtype=np.int64),
                      "T (112 x 112): T G_R T^T = G_X, det T = +-1, G_X = certificates/genus_class_7.txt, G_R = (3.1) from data/\n"
                      "([[3G, tau G], [(tau G)^T, 2G]]); rows: the basis of X_7 in the basis (3.1) of L_112. T commutes with the\n"
                      "action of SL_2(29) (diag(g, g) on (3.1)). Found by code/supplementary/genus/genus.py identify.\n"
                      "T（112 × 112）: 類 7 から L_112（基底 (3.1)）への SL_2(29) 同変な等長写像。T G_R T^T = G_X、det T = ±1。")
    # class 3 -> gluing A, in the reduced coordinates of L_{56,2}(M) / 類 3 -> 貼り方 A（L_{56,2}(M) の簡約座標）
    S = Genus(rep.out_dir)
    Gs, gens_s = load_nebe("M", rep.out_dir, reduce=True)
    _, Emb, _ = embedding_coords(S, rep.out_dir, rep, a.data)
    XA, commM = lift_class_A(Gs, gens_s, rep)
    BA = block_matrix(ZZ, [[I, XA], [Z, 2 * I]], subdivide=False)
    GA = matrix(ZZ, certs.load_matrix("gram_A.txt", NX, cdir).tolist())
    rep.check("gram_A.txt = B_A diag(G_M, G_M) B_A^T / 2 with the recomputed lift X_A",
              BA * block_matrix(ZZ, [[Gs, Z], [Z, Gs]], subdivide=False) * BA.transpose() == 2 * GA)
    # X_3 in reduced coordinates of L_{56,2}(M): B (L~ coords, form diag(G,G)/2) -> B diag(Emb, Emb) (form diag(G_M,G_M)/4)
    E2 = block_matrix(QQ, [[Emb, zero_matrix(QQ, N, N)], [zero_matrix(QQ, N, N), Emb]], subdivide=False)   # rows y -> y Emb
    B3 = BX[3] * E2
    isos = equivariant_isometries(B3, GX[3], BA.change_ring(QQ), GA, commM, rep, "class 3 -> gluing A")
    rep.check("class 3 is S-equivariantly isometric to gluing A", len(isos) > 0)
    T3 = min(isos, key=lambda T: (max(abs(x) for x in T.list()), sum(abs(x) for x in T.list())))
    rep.check("T G_A T^T = G_3 and det T = +-1", T3 * GA * T3.transpose() == GX[3] and abs(T3.det()) == 1)
    certs.save_matrix(os.path.join(cdir, ISO3_FILE), np.array(T3.rows(), dtype=np.int64),
                      "T (112 x 112): T G_A T^T = G_X, det T = +-1, G_X = certificates/genus_class_3.txt, G_A = certificates/gram_A.txt;\n"
                      "rows: the basis of X_3 in the basis of gluing A. SL_2(29)-equivariant. Found by\n"
                      "code/supplementary/genus/genus.py identify.\n"
                      "T（112 × 112）: 類 3 から貼り方 A への SL_2(29) 同変な等長写像。T G_A T^T = G_X、det T = ±1。")
    # cross-check of |U(Lambda_j)|: S-equivariant automorphisms of X_j / |U(Λ_j)| の検算: X_j の S 同変な自己同型
    if not a.skip_units:
        orders = []
        for j in range(NCLASS):
            auts = equivariant_isometries(BX[j], GX[j], BX[j], GX[j], commL, rep, f"class {j}: X_j -> X_j")
            orders.append(2 * len(auts))
        rep.value("|centralizer of SL_2(29) in Aut(X_j)| = |U(Lambda_j)|, j = 0..7 (recounted)", orders)
        rep.check("the recounted orders agree with qfauto in enum", orders == [LABELS[j][0] for j in range(NCLASS)])
    rep.finish()


# ---------------------------------------------------------------------------------------------------------
# check: numpy only / check: numpy のみ
# ---------------------------------------------------------------------------------------------------------

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
    rep.value("status of the minimum norm per class", {j: STATUS[j] + (" [witness]" if j in have else "") for j in range(NCLASS)})
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


def main():
    ap = argparse.ArgumentParser(description="S25: the genus of rank-2 unimodular Hermitian lattices over M (classes of X = L tensor Lambda)")
    ap.add_argument("mode", choices=["local", "mass", "enum", "build", "frames", "witness", "identify", "check"])
    ap.add_argument("--seed", type=int, default=1, help="seed of the neighbour walk (enum)")
    ap.add_argument("--max-steps", type=int, default=400, help="maximal number of neighbours (enum)")
    ap.add_argument("--bound", type=int, default=28, help="bound on Tr trd h for the frame search (frames)")
    ap.add_argument("--skip-units", action="store_true", help="identify: skip the recount of |U(Lambda_j)|")
    ap.add_argument("--data", default=None)
    ap.add_argument("--certificates", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.mode == "check":
        check(a)
    else:
        globals()["cmd_" + a.mode](a)


if __name__ == "__main__":
    main()
