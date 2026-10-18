# 検証用データ

[English](MANIFEST.md)

このディレクトリには、軌道代表、剰余類の最小ノルムの下界を保証する代表元（英語では certificate）、基底変換行列、補足計算の入力を収めます。一式を「検証用データ」と呼びます。主検算の入力は `code/verify/` が検査し、補足用の入力は下で区別します。証明では検査した性質と論文の数学的な補題を使い、データを生成したプログラムの正しさには依拠しません。

大きな `.npz` は git に入れず、GitHub Release に添付します。`SHA256SUMS`（git に入っています）が中身を固定し、
`code/lib/certs.py` の読み込みは使う前にハッシュを照合します。取得は `bash code/verify/fetch.sh` で行います。引数は Release のタグで、省略すると `certificates-v1` です。Release は <https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/releases/tag/certificates-v1> にあります。

ファイル名には、112 次元格子の以前の呼び名 R が残っています（`outer_automorphism_R.txt`、`reduction_R.txt`、`data/R112_gram_LLL.txt`）。論文では L₁₁₂ と呼びます。

`.npz` はすべて Python のオブジェクトを含まない NumPy の書庫で、`numpy.load(..., allow_pickle=False)` で読みます。
ベクトルは `data/L56_gram.txt` の基底に関する整数の行ベクトルです。

| ファイル | 配列 | 中身 | 検算 | 作成 |
|---|---|---|---|---|
| `reduction_R.txt` | 112 × 112 整数 | (3.1) から配布の Gram 行列への基底変換 U（U (3.1) Uᵀ = `data/R112_gram_LLL.txt`） | v0 | p6 |
| `reduction_L.txt` | 56 × 56 整数 | 列挙に使う L の BKZ-40 基底変換 | v1 | p6 |
| `min_reps.npz` | `reps` int16 (656, 56) | L₆ の S-軌道の代表 r_j（F2） | v3 | p2 |
| `centralizer.npz` | `units` int64 (6, 56, 56) | C/{±1} の代表 u_k（§4.2。`even_bounding.npz` の並びで） | v4 | p1 |
| `norm8_reps.npz` | `reps` int16 (254664, 56) | L₈ の S*-軌道の代表 x_i（F3） | v4 | p3 |
| `odd_bounding.npz` | `w0` int16 (656, 56) | 第 j 行: r_j τ + 2L の奇の類の下界を保証する代表元（F5a） | v5 | p4 |
| `even_bounding.npz` | `w0` int16 (1527984, 56) | 第 6i+k 行: x_i u_k τ + 2L の偶の類の下界を保証する代表元（F5b） | v7 | p5 |

別実装の検算・補足計算用のデータ:

| ファイル | 配列 | 中身 | 使うもの |
|---|---|---|---|
| `commutant.npz` | `basis` int64 (8, 56, 56) | M' = End_{SL2(29)}(L) の Z-基底 | crosscheck/all_data, supplementary |
| `negative_control_B.npz` | `tau_class_B` int64 (56, 56) | τ² = −5 で他方の類（貼り方 B）の M' の元 | supplementary |
| | `tau_B`, `x`, `v`, `hit_pairs` | 探索で見つけた貼り方 B の写像（2 を法とした持ち上げで、2 乗は −5 ではない）、衝突 (x, v)、衝突する組 | crosscheck/all_data（陰性対照） |
| `outer_automorphism_R.txt` | 112 × 112 整数 | SL₂(29) の外部自己同型を与える L₁₁₂ の自己同型 | supplementary/automorphisms |
| `gram_A.txt` | 112 × 112 整数 | 貼り方 A の Gram 行列 G_A（Nebe の L_{56,2}(M) を、48 個の類の写像の持ち上げで貼り合わせたもの。基底は (3.1)） | supplementary/isometry_ab.py（[C28]） |
| `isometry_AB.txt` | 112 × 112 整数 | T G_B Tᵀ = G_A、det T = ±1 を満たす基底変換 T（G_B は tau_class_B についての (3.1)）。貼り方 A から B への等長写像 | supplementary/isometry_ab.py（[C28]） |

経路 T（補遺 §S4.1、[C21]。定理 A の証明には使わない）:

| ファイル | 配列 | 中身 | 検算 | 作成 |
|---|---|---|---|---|
| `route_t_search3.npz` | `w0` int16 (3936, 56) | 探索 (3) の 3,936 類 r u_k μ + 2L の下界を保証する代表元（順序は `code/supplementary/route_t/common.py`） | route_t/check.py | route_t/certify.py |
| `route_t_search2.npz` | `w0` int16 (763992, 56), `done` bool (763992) | 探索 (2) の類 x_i u_k (1+τ) + 2L の下界を保証する代表元。`done = False` の行は未計算（0） | route_t/check.py | route_t/certify.py |

`route_t_search2.npz` はこの版では途中までです。公開の時点で計算が続いており、完了したら差し替えます。`check.py` は代表元を生成済みの類の数を報告し、
ちょうどそれらを検算します。残りの類は浮動小数点の探索（`route_t/float_cvp.py`）だけで調べてあります。
