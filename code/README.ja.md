# 「112 次元の極値偶ユニモジュラー格子」のコード

[English](README.md)

このディレクトリには、論文で使った計算がすべて入っています。論文の表 D2 はそれを [C1]〜[C31] として並べており、
このファイルの最後の節で、各行とここのスクリプトを対応させます。

## 何が示され、何に依拠するか

定理 A（L₁₁₂ の最小は 10）は、手で証明した補題 3.2・4.2（`lean/` で Lean でも検査済み）と、§4.3 の計算事実 F0〜F5 から従います。
**`verify/`** のスクリプトは、2 種類の入力から F0〜F5 を確かめます:

* `data/` の公開済みの 4 ファイル（L の Gram 行列、SL₂(29) の生成元、τ、L₁₁₂ の簡約 Gram 行列）。SHA-256 は `lib/data.py` に固定してあります。
* `certificates/` の**検証用データ**（軌道代表、最小ノルムの下界を保証する代表元、基底変換行列。`certificates/MANIFEST.ja.md` を参照）。SHA-256 は
  `certificates/SHA256SUMS` に固定してあります。

ここでは配布する補助的な入力の一式を「検証用データ」と呼びます。英語の certificate は、そのうち剰余類の最小ノルムの下界を保証する代表元を指します。`odd_bounding.npz`・`even_bounding.npz` の各行がその代表元です。検算器は、指定した剰余類に属すること、ノルムの条件、最小ベクトルとの内積の条件を検査し、論文の補題から下界を導きます。軌道代表や基底変換行列は、それぞれの具体名で呼びます。

定理 A の証明が依拠するのは、検算のコード（numpy だけを使う Python 約 1,500 行と C のプログラム 1 本）と、手で証明した補題です。
検証用データを作ったコード（`produce/`）の正しさには依拠**しません**。証明が使うデータの性質は、すべて `verify/` が確かめ直します。

## 構成

| ディレクトリ | 中身 |
|---|---|
| `lib/` | 共有の小さなライブラリ（numpy のみ）: データの読み込み、厳密さの確認、群、2 を法とした標準形、最小ベクトル |
| `verify/` | F0〜F5 の検算（v0〜v7）と整合性の検査（v8） |
| `produce/` | 検証用データの生成（p1〜p6）。証明の検算には不要 |
| `crosscheck/` | 検算の第 2 の実装。`verify/`・`produce/`・`lib/` のコードを読まずに、Claude を用いて別に書いた。同じデータを別のコードで確かめるので、主な実装に誤りがあれば結果の食い違いとして現れる: `all_data/`（すべての検証用データと F1 を別の方法で）、`second_impl/`（標準形、デザインの恒等式、奇の類） |
| `supplementary/` | 論文の主張のうち、定理 A の証明には使わないものの計算（貼り方の分類、自己同型群など） |

## 検算の実行

[動作環境](#動作環境)を準備し、以下はリポジトリのルートで実行します。Python 環境の準備手順は[ルートの README](../README.ja.md#最初に実行すること)を参照してください。検査は 3 段あります。

**(i) 入力だけ。** まず定義行列と群作用を検査できます（約 20 秒、追加データのダウンロードは不要）。これだけでは最小ノルムは確定しません。

```bash
python3 code/verify/v0_inputs.py
```

**(ii) 証明に使う計算。** 大きな検証用データを取得して、`proof.sh` を実行します。約 1.2 CPU 時間（v1 が 34 分、v6 が 24 分、残りは数分）で、v0〜v6 を走らせます。F1 は区間演算の列挙、F2・F3 は軌道代表の網羅性、F5a は奇の剰余類の下界を保証する代表元、F5b は標準形で検査します。これは、定理 A の証明に使う計算事実 F0〜F5 をすべて確かめる最短の経路です（補遺 表 S7 の経路 A）。

```bash
bash code/verify/fetch.sh
bash code/verify/proof.sh
```

`fetch.sh` の引数は Release のタグで、省略すると `certificates-v1` です。

**(iii) すべて。** 全検算は約 26 CPU 時間、3 並列で経過時間約 9.5〜10 時間が目安です。`proof.sh` の全部に加えて、F5b を偶の剰余類の下界を保証する代表元で確かめる代替の検査（v7、約 24 CPU 時間）と、球面デザインの恒等式の整合性の検査（v8）を行います。

```bash
bash code/verify/full.sh 3
```

`bash code/verify/quick.sh`（約 40〜50 分）は短縮した検査です。F1 は陽性対照だけに対して実行し、v7 と v8 を省くので、通過しても定理の全検算にはなりません。

各段は検査ごとに `[ok]`/`[FAIL]` を表示し、結果・ソフトウェアの版・実行時間を `out/<段>.json` に書きます。

## 検算の各段

時間は論文に使った計算機（8 コア、15 GB、ほかの計算と共用）での実測です。

| 段 | 論文 | 確かめること | 時間 | メモリ |
|---|---|---|---|---|
| `v0_inputs.py` | F0, F4, 補題 3.2 | L は偶ユニモジュラー。g₁, g₂ は G を保ち、−I を含む位数 24,360 の群を生成し、τ と可換。τ² = −5、τGτᵀ = 5G。(3.1) は偶ユニモジュラー。配布した L₁₁₂ の Gram 行列は同じ格子 | 20 秒 | 1 GB 未満 |
| `v1_min_L.py` + `enum_interval.c` | F1、§6.1 (a)、表 5 | 取りこぼしの無い区間演算の列挙で min L = 6。陽性対照 E₈、Leech、Leech ⊥ Leech ⊥ E₈ | 34 分 | 1 GB 未満 |
| `v2_theta.py` | §2.3、付録 B、補遺 §S1・§S2 | 極値テータ級数（\|L₆\|, \|L₈\|）、Siegel 平均、表 B1, S1, S2, S4, S5 | 1 秒 | — |
| `v3_minimal_orbits.py` | F2、§6.2 | 656 軌道が 15,590,400 本の最小ベクトルを覆う（展開と標準形の 2 通り） | 3 分 | 2 GB |
| `v4_norm8_orbits.py` | F3、§6.4 | 1,527,984 本の x_i u_k が、\|L₈\| を覆う相異なる 1,517,130 個の正則な軌道を与える | 9 分 | 2 GB |
| `v5_odd_bounding.py` | F5a、系 5.2、表 7 | 656 個の奇の類の下界を保証する代表元 | 2.5 分 | 2 GB |
| `v6_canonical_lookup.py` | F5b、命題 6.3、表 6 | 類 x_i u_k τ + 2L はどれもノルム 8 のベクトルを含まない（標準形）。型 (6,6) も | 24 分 | 2 GB |
| `v7_even_bounding.py` | F5b、系 5.3、表 8 | 1,527,984 個の偶の類の下界を保証する代表元（再開可能。`--threads`） | 24 CPU 時間（3 スレッドで 7.9 時間） | 3 GB |
| `v8_design_identities.py` | §6.3 | 球面デザインの恒等式 18 個（整合性の検査。証明には不要） | 14 分 | 2 GB |

F5b は無関係な 2 つの議論（v6 と v7）で確かめます。証明にはどちらか一方で足ります。

### 厳密さの確保

判定はすべて整数演算で行います。整数行列の積を（速さのために）浮動小数点で計算するところでは、実際の入力から、すべての部分和が 2²⁴（float32）
または 2⁵³（float64）未満の整数であることを先に確かめます。そのような積は厳密です。補助関数は `lib/exact.py` にあり、各スクリプトの冒頭に、
どの積をこの方法で計算するかを書いてあります。F1 の列挙は外向きに丸める区間演算を使います（`verify/enum_interval.c` の冒頭）。

## 動作環境

* `verify/`、`crosscheck/second_impl/`: Python 3.10 以上と numpy（Python 3.12、numpy 2.5 で確認）。v1 には 128 ビット整数をもつ C コンパイラ（gcc か clang。`$CC` があればそれ、無ければ `cc`・`gcc`・`clang` の順に探す）。ほかのパッケージは要りません。
* `produce/`、`supplementary/`、`crosscheck/all_data/`: SageMath 10（PARI/GP、GAP、fpylll を含む）。SageMath 10.9 で確認。リポジトリの根の
  `environment.yml` で conda/micromamba から入れられます。
* `lean/`: Lean 4 と Mathlib（版は `lean/lean-toolchain` と `lean/lake-manifest.json` に固定）。

## 検証用データの生成

| スクリプト | 作るもの | 時間 |
|---|---|---|
| `produce/p1_centralizer.py` | M′ と中心化群 C（`centralizer.npz`、`commutant.npz`） | 10 分 |
| `produce/p2_minimal_orbits.py` | `min_reps.npz`（閉包、§6.2） | 10 分 |
| `produce/p3_norm8_orbits.py` | `norm8_reps.npz`（印の付く元、§6.4） | 1.2 時間 |
| `produce/p4_odd_descent.py` | `odd_bounding.npz`（降下、§6.6） | 3 分 |
| `produce/p5_even_descent.py` | `even_bounding.npz`（降下、§6.7。6 分割、再開可能） | 約 190 CPU 時間 |
| `produce/p6_reduction.py` | `reduction_L.txt`、`reduction_R.txt` | 1 分 |

各生成スクリプトは、出力を配布した検証用データと比べます。p4 と p5 は配布したファイルをビット単位で再現します。p2 と p3 は別の代表を選びうるので、
標準形の集合（同じ軌道か）で比べます。

## 経路 T（補遺 §S4、表 D2 の [C20]・[C21]）

`supplementary/route_t/` は、L₁₁₂ のエルミート構造を使う補足の議論（経路 T）の計算です。定理 A の証明には使いません。

| スクリプト | 内容 | 時間 |
|---|---|---|
| `classify.py`, `recount.py` | [C20] 階数 2 の台加群の分類（2 通りの独立な数え上げ。97 型・危険 63 型と、粗い不変量で 58 型の一致） | 各 1〜2 分（SageMath） |
| `certify.py` | [C21] 探索 (2)・(3) の 代表元の生成（分割・再開可能） | 探索 (3) 約 25 分、探索 (2) 約 13 CPU 日 |
| `check.py` | [C21] 代表元の整数演算による検算（numpy だけ） | 探索 (3) 約 2 分、探索 (2) は全部で約 12 CPU 時間 |
| `float_cvp.py` | [C21] 探索 (2) の浮動小数点の最近ベクトル列挙（補助） | 約 3 × 13 時間（SageMath） |

**この版の状態**: 探索 (3) の代表元は 3,936 類すべてそろっています。探索 (2) は公開の時点で計算が続いており、
`certificates/route_t_search2.npz` は途中までです（763,992 類のうち代表元を生成済みの類の数は `check.py` が報告します）。
残りの類は浮動小数点の探索だけで調べてあります。完了したらファイルを差し替えます。自分で完成させるには、
P = 0, …, Q−1 について `certify.py search2 --missing --part P --nparts Q`（代表元を未生成の類だけ。再開可能）を実行し、
`certify.py collect --base` で配布ファイルに足してから、もう一度 `check.py` を実行します。

## 論文の表 D2 との対応

| 表 D2 | スクリプト |
|---|---|
| [C1] | verify/v2_theta.py |
| [C2] | verify/v0_inputs.py, supplementary/gluings.py (d), produce/p1_centralizer.py |
| [C3] | supplementary/gluings.py, supplementary/nebe/gluings_m.py (a), (b) |
| [C4] | supplementary/gluing_b.py, supplementary/nebe/gluings_m.py (c), (d) |
| [C5] | verify/v1_min_L.py + verify/enum_interval.c, produce/p6_reduction.py |
| [C6] | supplementary/nebe/reduction_to_nebe.py (with nebe/lattices.py, nebe/tables.py) |
| [C7] | supplementary/float_enumerations.py svp, qfminim |
| [C8] | produce/p2_minimal_orbits.py, verify/v3_minimal_orbits.py, verify/v8_design_identities.py |
| [C9] | produce/p3_norm8_orbits.py, verify/v4_norm8_orbits.py, verify/v8_design_identities.py |
| [C10] | produce/p4_odd_descent.py, verify/v5_odd_bounding.py, crosscheck/second_impl/odd_classes.py |
| [C11] | verify/v6_canonical_lookup.py, crosscheck/second_impl/even_classes.py |
| [C12] | supplementary/float_enumerations.py cvp610, cvp88 |
| [C13] | produce/p5_even_descent.py, verify/v7_even_bounding.py |
| [C14] | supplementary/frame_stabilizer.py |
| [C15] | supplementary/sample_check.py |
| [C16] | supplementary/node_estimate.py |
| [C17] | supplementary/frames.py |
| [C18] | supplementary/fixed_sublattices.py |
| [C19] | supplementary/anatomy_b.py |
| [C20] | supplementary/route_t/classify.py, recount.py (with route_t/hermitian.py) |
| [C21] | supplementary/route_t/certify.py, check.py, float_cvp.py (with route_t/common.py) |
| [C22] | lean/ (EEUL/L112/Chain.lean) |
| [C23] | supplementary/nebe/identify_nebe.py (with nebe/lattices.py, nebe/cycloquat.py) |
| [C24] | supplementary/automorphisms/aut_normalizer.py |
| [C25] | supplementary/automorphisms/group_facts.g, out_facts.g, aut_diagonal.py |
| [C26] | supplementary/automorphisms/aut_structure.py, aut_character.py, endomorphisms.py |
| [C27] | crosscheck/all_data/check_all.py, min_L.py, min_L_enum.c |
| [C28] | supplementary/isometry_ab.py (find, check) |
| [C29] | supplementary/genus/genus.py local, mass, enum |
| [C30] | supplementary/genus/genus.py build, frames, witness |
| [C31] | supplementary/genus/genus.py identify, check |
