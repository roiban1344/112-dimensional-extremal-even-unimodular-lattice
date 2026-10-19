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
            which the walk finds them. Writes out/genus/lambda.txt and genus_classes.txt (see Output below).
            ノルム 5 の素イデアル p = ((7 + √29)/2) での Kneser の近傍（Siegel 型: N = Λ ∩ Λ' で h(N, N) ⊂ pM、Λ' は N と π^{-1}N の間）を、
            Λ_0 = M ⊕ M から固定した乱数シード（--seed、既定 1）で無作為にたどり、Σ 1/|U(Λ)| が質量 157/640 に達するまで続ける。類の番号 0〜7 は
            不変量（|U| と Tr trd h のノルム 14 以下のベクトルの本数）で付け、見つかる順序によらない。out/genus/lambda.txt と
            genus_classes.txt を書く（下の「出力」を参照）。
  build     X_j = L tensor_M Lambda_j for the 8 classes, LLL-reduced (PARI qflllgram). Writes the Gram matrices
            genus_class_<j>.txt and, in genus_basis_<j>.txt, the basis of X_j in the
            coordinates of data/L56_gram.txt (L~ below): through the embedding e: L~ -> L_{56,2}(M) of
            nebe/reduction_to_nebe.py (out/nebe/embedding_L_into_M.txt; <e x, e y> = 2 <x, y>), W^2 = (L~ tensor Q)^2,
            and the basis is scaled so that the form is diag(G, G)/2 as in (3.1). The file holds d, then
            D = d B (integers), B the rational basis matrix: D diag(G, G) D^T = 2 d^2 G_X.
            8 類の X_j = L ⊗_M Λ_j を作り LLL 簡約する（PARI の qflllgram）。Gram 行列を genus_class_<j>.txt に、
            data/L56_gram.txt（以下 L~）の座標での X_j の基底を genus_basis_<j>.txt に書く。nebe/reduction_to_nebe.py の
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
            written, in the basis of genus_class_<j>.txt, to genus_witnesses.txt.
            類 3, 4（位数 3 の s = zw と位数 3 の u ∈ U(Λ) の積 s u の固定部分格子。PARI の qfminim）と類 5（位数 4 の s = w と位数 4 の u の積の
            固定部分格子、56 次元。fpylll の BKZ と枝刈りつき列挙、乱数シードは固定）のノルム 8 のベクトル。v G_X v^T = 8 を厳密に確かめ、
            genus_class_<j>.txt の基底での座標を genus_witnesses.txt に書く。
  identify  Explicit isometries class 7 -> L_112 (the basis (3.1) from data/) and class 3 -> gluing A
            (certificates/gram_A.txt), found as in isometry_ab.py: among the S-equivariant maps (32-dimensional) that
            are integral, those with Q(T) = tr(G_X^{-1} T G_Y T^T) <= 112 are enumerated (qfminim, checked complete)
            and T G_Y T^T = G_X is tested exactly. Class 7 is compared in the coordinates of L~ (data/), class 3 in
            the reduced coordinates of L_{56,2}(M) of isometry_ab.py. As a cross-check of the orders |U(Lambda)|
            (computed by qfauto in enum), the same enumeration with Y = X_j counts the S-equivariant automorphisms
            of X_j, which form U(Lambda_j) (Morita). Writes genus_isometry_7_L112.txt and
            genus_isometry_3_A.txt (rows: the basis of X_j in the basis of the target).
            明示的な等長写像 類 7 -> L_112（data/ からの基底 (3.1)）と 類 3 -> 貼り方 A（certificates/gram_A.txt）を isometry_ab.py と同じ方法で求める:
            S 同変な写像（32 次元）のうち整数のものの中で Q(T) = tr(G_X^{-1} T G_Y T^T) ≤ 112 となるものを列挙し（qfminim。完全性を確かめる）、
            T G_Y T^T = G_X を厳密に確かめる。類 7 は L~（data/）の座標で、類 3 は isometry_ab.py の L_{56,2}(M) の簡約座標で比べる。
            enum で qfauto が求めた位数 |U(Λ)| の検算として、Y = X_j とした同じ列挙で X_j の S 同変な自己同型（森田により U(Λ_j)）を数える。
            genus_isometry_7_L112.txt と genus_isometry_3_A.txt を書く（行は X_j の基底を行き先の基底で書いたもの）。
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

Output. enum, build, witness and identify write their files to --dest, by default out/genus/; the distributed
files in certificates/ are not overwritten (pass --dest certificates/ to replace them, then update
certificates/SHA256SUMS). A step that needs the output of an earlier step reads it from --dest if it is there,
otherwise the distributed file. Each written file is compared with the distributed one and reported as identical,
the same integers (only comment lines differ), or different. For genus_classes.txt the integers are a canonical
invariant (the labels do not depend on the walk) and must agree; the other files may legitimately differ (another
walk, PARI's enumeration order, another embedding e), and check verifies the distributed ones. check reads only the
distributed files (--certificates).
出力. enum, build, witness, identify はファイルを --dest（既定は out/genus/）に書き、certificates/ の配布ファイルは上書きしない（置き換えるには
--dest certificates/ を指定し、certificates/SHA256SUMS を更新する）。前の段の出力が要る段は、--dest にあればそれを、無ければ配布ファイルを読む。
書いたファイルはそれぞれ配布ファイルと比べ、同じ、整数が同じ（注釈行だけが違う）、違う、のいずれかを報告する。genus_classes.txt の整数は標準的な
不変量（類の番号は歩き方によらない）なので一致しなければならない。ほかのファイルは違ってもよく（別の歩き方、PARI の列挙順、別の埋め込み e）、
配布したものを check が確かめる。check は配布ファイル（--certificates）だけを読む。

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
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genus_check import check  # noqa: E402
from lib import certs  # noqa: E402

# The code is split into genus_data.py (constants and files; numpy only), genus_check.py (check; numpy only),
# genus_lattice.py (the class Genus; SageMath) and genus_steps.py (the SageMath steps). check imports no SageMath.
# コードは genus_data.py（定数とファイル。numpy のみ）、genus_check.py（check。numpy のみ）、genus_lattice.py（クラス Genus。SageMath）、
# genus_steps.py（SageMath の段）に分けてある。check は SageMath を読み込まない。


def main():
    ap = argparse.ArgumentParser(description="S25: the genus of rank-2 unimodular Hermitian lattices over M (classes of X = L tensor Lambda)")
    ap.add_argument("mode", choices=["local", "mass", "enum", "build", "frames", "witness", "identify", "check"])
    ap.add_argument("--seed", type=int, default=1, help="seed of the neighbour walk (enum)")
    ap.add_argument("--max-steps", type=int, default=400, help="maximal number of neighbours (enum)")
    ap.add_argument("--bound", type=int, default=28, help="bound on Tr trd h for the frame search (frames)")
    ap.add_argument("--skip-units", action="store_true", help="identify: skip the recount of |U(Lambda_j)|")
    ap.add_argument("--data", default=None)
    certs.add_arguments(ap, help="the distributed certificates (read by check and compared with)")
    ap.add_argument("--dest", default=None,
                    help="enum, build, witness, identify: directory for the files they write (default out/genus/); "
                         "pass certificates/ to replace the distributed files (then update SHA256SUMS)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.mode == "check":
        check(a)
    else:
        import genus_steps
        getattr(genus_steps, "cmd_" + a.mode)(a)


if __name__ == "__main__":
    main()
