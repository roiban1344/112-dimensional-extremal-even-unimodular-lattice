# Verification data / 検証用データ

This directory contains verification data: orbit representatives, coset representatives establishing minimum-norm bounds (certificates), change-of-basis matrices, and supporting data. The main inputs are checked by `code/verify/`; supplementary inputs are identified below. The computational part of the proof uses the checked properties, together with the mathematical lemmas in the paper, and does not rely on the programs that produced the data.

このディレクトリには、軌道代表、剰余類の最小ノルムの下界を保証する代表元（英語では certificate）、基底変換行列、補足計算の入力を収めます。一式を「検証用データ」と呼びます。主検算の入力は `code/verify/` が検査し、補足用の入力は下で区別します。証明では検査した性質と論文の数学的な補題を使い、データを生成したプログラムの正しさには依拠しません。

The large `.npz` files are attached to the GitHub Release, not stored in git. `SHA256SUMS`
(in git) fixes their content; every reader in `code/lib/certs.py` checks the hash before use.
Download them with `code/verify/fetch.sh`.

大きな `.npz` は git に入れず、GitHub Release に添付します。`SHA256SUMS`（git に入っています）が中身を固定し、
`code/lib/certs.py` の読み込みは使う前にハッシュを照合します。取得は `code/verify/fetch.sh` で行います。

File names keep the letter R of an earlier draft for the 112-dimensional lattice (`outer_automorphism_R.txt`, `reduction_R.txt`; also `data/R112_gram_LLL.txt`); the paper calls it L₁₁₂.
ファイル名には、112 次元格子の以前の呼び名 R が残っています（`outer_automorphism_R.txt`、`reduction_R.txt`、`data/R112_gram_LLL.txt`）。論文では L₁₁₂ と呼びます。

All `.npz` files are plain NumPy archives without Python objects; they are read with
`numpy.load(..., allow_pickle=False)`. Vectors are integer row vectors in the basis of
`data/L56_gram.txt`.

`.npz` はすべて Python のオブジェクトを含まない NumPy の書庫で、`numpy.load(..., allow_pickle=False)` で読みます。
ベクトルは `data/L56_gram.txt` の基底に関する整数の行ベクトルです。

| file / ファイル | array / 配列 | content / 中身 | checked by / 検算 | produced by / 作成 |
|---|---|---|---|---|
| `reduction_R.txt` | 112 × 112 integers | basis change U with U (3.1) Uᵀ = `data/R112_gram_LLL.txt` / (3.1) から配布の Gram 行列への基底変換 | v0 | p6 |
| `reduction_L.txt` | 56 × 56 integers | BKZ-40 basis change of L used by the enumeration / 列挙に使う L の BKZ-40 基底変換 | v1 | p6 |
| `min_reps.npz` | `reps` int16 (656, 56) | representatives r_j of the S-orbits on L₆ (F2) / L₆ の S-軌道の代表 | v3 | p2 |
| `centralizer.npz` | `units` int64 (6, 56, 56) | representatives u_k of C/{±1} (§4.2), in the order used for `even_bounding.npz` / C/{±1} の代表（`even_bounding.npz` の並びで） | v4 | p1 |
| `norm8_reps.npz` | `reps` int16 (254664, 56) | representatives x_i of the S*-orbits on L₈ (F3) / L₈ の S*-軌道の代表 | v4 | p3 |
| `odd_bounding.npz` | `w0` int16 (656, 56) | row j: odd-class certificate of r_j τ + 2L (F5a) / 第 j 行: r_j τ + 2L の奇の類の下界を保証する代表元 | v5 | p4 |
| `even_bounding.npz` | `w0` int16 (1527984, 56) | row 6i + k: even-class certificate of x_i u_k τ + 2L (F5b) / 第 6i+k 行: x_i u_k τ + 2L の偶の類の下界を保証する代表元 | v7 | p5 |

Data for cross-checks and supplementary computations / 別実装の検算・補足計算用のデータ:

| file / ファイル | arrays / 配列 | content / 中身 | used by / 使うもの |
|---|---|---|---|
| `commutant.npz` | `basis` int64 (8, 56, 56) | a Z-basis of M' = End_{SL2(29)}(L) / M' の Z-基底 | crosscheck/all_data, supplementary |
| `negative_control_B.npz` | `tau_class_B` int64 (56, 56) | an element of M' with τ² = −5 in the other class (gluing B) / τ² = −5 で他方の類（貼り方 B）の M' の元 | supplementary |
| | `tau_B`, `x`, `v`, `hit_pairs` | the gluing map of gluing B as found in the search (a lift modulo 2, not of square −5), a collision (x, v), and the colliding pairs / 探索で見つけた貼り方 B の写像（2 を法とした持ち上げで、2 乗は −5 ではない）、衝突 (x, v)、衝突する組 | crosscheck/all_data (negative controls) |
| `outer_automorphism_R.txt` | 112 × 112 integers | an automorphism of L₁₁₂ inducing the outer automorphism of SL₂(29) / SL₂(29) の外部自己同型を与える L₁₁₂ の自己同型 | supplementary/automorphisms |
| `gram_A.txt` | 112 × 112 integers | Gram matrix G_A of gluing A (Nebe's L_{56,2}(M) glued by a lift of a map in the class of 48), in the basis (3.1) / 貼り方 A の Gram 行列 G_A（基底 (3.1)） | supplementary/isometry_ab.py ([C28]) |
| `isometry_AB.txt` | 112 × 112 integers | basis change T with T G_B Tᵀ = G_A, det T = ±1 (G_B = (3.1) for tau_class_B), an isometry from gluing A onto gluing B / T G_B Tᵀ = G_A、det T = ±1 の基底変換（貼り方 A から B への等長写像） | supplementary/isometry_ab.py ([C28]) |

Route T (supplement §S4.1, [C21]; not used in the proof of Theorem A) / 経路 T（補遺 §S4.1、[C21]。定理 A の証明には使わない）:

| file / ファイル | arrays / 配列 | content / 中身 | checked by / 検算 | produced by / 作成 |
|---|---|---|---|---|
| `route_t_search3.npz` | `w0` int16 (3936, 56) | certificates for the 3,936 classes r u_k μ + 2L of search (3), order in `code/supplementary/route_t/common.py` / 探索 (3) の 3,936 類の下界を保証する代表元（順序は common.py） | route_t/check.py | route_t/certify.py |
| `route_t_search2.npz` | `w0` int16 (763992, 56), `done` bool (763992) | certificates for the classes x_i u_k (1+τ) + 2L of search (2); rows with `done = False` are not yet computed (zero) / 探索 (2) の類の下界を保証する代表元。`done = False` の行は未計算（0） | route_t/check.py | route_t/certify.py |

`route_t_search2.npz` is incomplete in this release: the computation was still running when the files were published, and the file will be replaced when it is complete. `check.py` reports how many classes are certified and checks exactly those; the remaining classes are covered only by the floating-point search (`route_t/float_cvp.py`).
`route_t_search2.npz` はこの版では途中までです。公開の時点で計算が続いており、完了したら差し替えます。`check.py` は 代表元を生成済みの類の数を報告し、
ちょうどそれらを検算します。残りの類は浮動小数点の探索（`route_t/float_cvp.py`）だけで調べてあります。
