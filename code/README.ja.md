# 「112 次元の極値偶ユニモジュラー格子」のコード

[English](README.md)

このディレクトリには、論文で使った計算がすべて入っています。論文の表 D2 はそれを [C1]〜[C32] として並べており、
このファイルの最後の節で、各行とここのスクリプトを対応させます。

記号: コードと検証用データのファイルでは、L は論文の 56 次元の素材の格子 L₅₆ を指し、L_m（L_6、L_8）はノルム m のベクトルの殻 L₅₆(m) を指す。

## 何が示され、何に依拠するか

定理 A（L₁₁₂ の最小は 10）は、§3〜§6 で手で証明した結果（補題 3.2・4.2・5.1、系 4.3・5.2・5.3、命題 6.3）、既知の上界 (1.1)、§4.3 の計算事実 F0〜F5 から従います。
計算事実から定理を導く部分（補題 4.2、系 4.3、補題 5.1 とその系、最後の導出）は Lean でも検査済みです（`lean/`、§7.1 の表 9）。補題 3.2（ユニモジュラー性）、命題 6.3、(1.2) による組 (x, xτ + 2y) から L₁₁₂ のベクトルへの移行は Lean の外にあります。Lean の外にあるものの一覧は §7.1 にあります。
**`verify/`** のスクリプトは、2 種類の入力から F0〜F5 を確かめます:

* `data/` の公開済みの 4 ファイル（L の Gram 行列、SL₂(29) の生成元、τ、L₁₁₂ の簡約 Gram 行列）。SHA-256 は `lib/data.py` に固定してあります。
* `certificates/` の**検証用データ**（軌道代表、最小ノルムの下界を保証する代表元、基底変換行列。`certificates/MANIFEST.ja.md` を参照）。SHA-256 は
  `certificates/SHA256SUMS` に固定してあります。`--certificates DIR` を指定するとファイルは `DIR` から読みますが、照合するのは
  リポジトリの `certificates/SHA256SUMS` のままです。別のハッシュの一覧は `--hashes FILE` で明示したとき（改変したデータでの試験など）
  にだけ使い、警告を表示して JSON に `certificate_hashes` として記録します。

ここでは配布する補助的な入力の一式を「検証用データ」と呼びます。英語の certificate は、そのうち剰余類の最小ノルムの下界を保証する代表元を指します。`odd_bounding.npz`・`even_bounding.npz` の各行がその代表元です。検算器は、指定した剰余類に属すること、ノルムの条件、最小ベクトルとの内積の条件を検査し、論文の補題から下界を導きます。軌道代表や基底変換行列は、それぞれの具体名で呼びます。

定理 A の証明が依拠するのは、検算のコードと手で証明した結果です。検算のコードは `verify/` の v0〜v7 と `lib/` の Python 約 2,000 行（英日 2 言語の冒頭コメントを含む）と C のプログラム 1 本で、Python が使う外部パッケージは numpy だけです。
検証用データを作ったコード（`produce/`）の正しさには依拠**しません**。証明が使うデータの性質は、すべて `verify/` が確かめ直します。

## 構成

| ディレクトリ | 中身 |
|---|---|
| `lib/` | 共有の小さなライブラリ（numpy のみ）: データの読み込み、厳密さの確認、群、2 を法とした標準形、最小ベクトル |
| `verify/` | F0〜F5 の検算（v0〜v7）と整合性の検査（v8） |
| `produce/` | 検証用データの生成（p1〜p6）。証明の検算には不要 |
| `crosscheck/` | 検算の第 2 の実装。`verify/`・`produce/`・`lib/` のコードを読まずに、Claude を用いて別に書いた。同じデータを別のコードで確かめるので、主な実装に誤りがあれば結果の食い違いとして現れる: `all_data/`（すべての検証用データと F1 を別の方法で）、`second_impl/`（標準形、デザインの恒等式、奇の類） |
| `supplementary/` | 論文の主張のうち、定理 A の証明には使わないものの計算（貼り方の分類、自己同型群など） |
| `tests/` | 小さな例による試験（pytest。[試験](#試験)を参照）。`proof.sh` の代わりにはならない |

ディレクトリの間の依存: `verify/` は `lib/` だけを import する。`lib/` は `code/` のほかのものを使わない。`crosscheck/` は自分のディレクトリの外の
`code/` を import せず、`data/` と `certificates/` を読むだけである。`produce/` は `lib/` と自分の補助を使う。`supplementary/` は `lib/`、
`produce/` のいくつかの関数（`p1_centralizer`、`exact_qfminim`、`descent`。`nebe/tables.py` では p2・p3・p6 も）と自分のモジュールを使うので、
生成スクリプトを変えると補足の計算が壊れうる。`tests/test_layout.py` がこの規則を確かめる。段の間のファイルの受け渡しは `out/` だけを通る:
v4 が v6・v8・`supplementary/gluing_b.py` のために `out/K8.npy` と `out/K8_first.npy` を書き、v6・v8 はそれを v4 の JSON の記録（合格したこと、
ファイル・入力・コードの SHA-256）と照合する。

### ファイル

| ファイル | 中身 |
|---|---|
| `lib/__init__.py` | `require`（`assert` の代わりに例外を投げる検査）、`CheckError`、定数 \|L₆\| と \|L₈\|（`N6`、`N8`。v2 が確かめる）、整数の厳密な線形代数 |
| `lib/data.py` | `data/` の 4 つのファイルの読み込みと SHA-256 の照合 |
| `lib/certs.py` | `certificates/` の検証用データの読み込みと `certificates/SHA256SUMS` との照合 |
| `lib/exact.py` | 整数行列の浮動小数点による積が厳密であることを保証する検査 |
| `lib/enumerate.py` | 区間演算による列挙 `verify/enum_interval.c` の呼び出し |
| `lib/group.py` | g₁, g₂ が生成する群と、±1 を法とした元 |
| `lib/mod2.py` | 2L を法とする類の 56 ビット整数による表現と標準形（§6.5） |
| `lib/shells.py` | L の最小ベクトルと、それとの内積（§5）。途中経過の保存を含む |
| `lib/report.py` | `[ok]`/`[FAIL]` の表示と `out/<step>.json` |
| `verify/v0_inputs.py` 〜 `v8_design_identities.py`、`enum_interval.c` | 検算スクリプト v0〜v8 と、v1 が使う列挙のプログラム（各スクリプトの内容は次の節） |
| `verify/fetch.sh`・`proof.sh`・`full.sh`・`quick.sh`・`preflight.sh` | 検証用データの取得、3 つの水準の検算、最初の段の前の numpy とデータの確認 |
| `verify/controls/leech.txt` | Leech 格子の Gram 行列。検算スクリプト v1 の陽性対照 |
| `produce/p1_centralizer.py` 〜 `p6_reduction.py`、`descent.py` | 検証用データの生成（[検証用データの生成](#検証用データの生成)の節）。`descent.py` は p4 と p5 が共有する代表元の探索（類の元 w から始め、内積 ⟨w, u⟩ ≥ 7 となる最小ベクトル u がある限り w を w − 2u に置き換える。ノルムが必ず下がるので止まり、§5 の条件を満たせば w が代表元になる） |
| `produce/exact_qfminim.py` | PARI の `qfminim` の結果を区間演算の列挙で網羅性まで確かめる関数（`p1` と `supplementary/` が使う） |
| `crosscheck/second_impl/odd_classes.py`・`even_classes.py`・`design_identities.py` | F5a、F5b、デザインの恒等式の第 2 の実装（numpy のみ） |
| `crosscheck/all_data/`・`supplementary/` | [第 2 の実装](#第-2-の実装と補足の計算)・[証明経路 T](#証明経路-t補遺-s4表-d2-の-c20c21c32)・[表 D2 との対応](#論文の表-d2-との対応)の節を参照。`supplementary/nebe/isometry.py` は `identify_nebe.py` と `reduction_to_nebe.py` のために SL₂(29) 同変な等長写像を求める |
| `run_supplementary.sh` | `supplementary/` の計算をまとめて実行する |
| `tests/conftest.py`・`tests/test_*.py` | [試験](#試験)の節の試験。`test_exact`（厳密さの検査）、`test_enumerate`（列挙）、`test_group_mod2`（群と標準形）、`test_report_checkpoint`（報告と途中経過）、`test_certs`（検証用データのハッシュ）、`test_scripts`（v0、v1 の対照、v2、シェルの構文）、`test_data`（マーカー `data`）、`test_route_t_exclusion`（[C32] の数行）、`test_check_paper`（`paper/tools/check-paper.py`）、`test_docs`（追跡しているファイルがすべて README で説明されていること）、`test_shells`（小さな格子でのすべての最小ベクトルとの内積）、`test_layout`（依存の規則） |

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

`fetch.sh` の引数は Release のタグで、省略すると `certificates-v2` です。

**(iii) すべて。** 全検算は約 26 CPU 時間、3 並列で経過時間約 9.5〜10 時間が目安です。`proof.sh` の全部に加えて、F5b を偶の剰余類の下界を保証する代表元で確かめる代替の検査（v7、約 24 CPU 時間）と、球面デザインの恒等式の整合性の検査（v8）を行います。

```bash
bash code/verify/full.sh 3
```

`bash code/verify/quick.sh`（約 40〜50 分）は短縮した検査です。F1 は陽性対照だけに対して実行し、v7 と v8 を省くので、通過しても定理の全検算にはなりません。

各段は検査ごとに `[ok]`/`[FAIL]` を表示し、結果・ソフトウェアの版・実行時間を `out/<段>.json` に書きます。各段は開始時に古い `out/<段>.json` を消し、エラー（ハッシュの不一致など）で止まったときは `"passed": false` とエラーを書くので、このファイルが古い合格を示すことはありません。合否の正本は終了コード（失敗があれば 0 以外）です。シェルスクリプトは Python を `-I`（隔離モード）で呼び、ライブラリは `python -O` の下での実行を拒否します。`proof.sh`・`full.sh`・`quick.sh` は、最初の段の前に、Python が numpy を読み込めることと、使う検証用データが `certificates/SHA256SUMS` のハッシュのとおりにそろっていることを確かめる（`verify/preflight.sh`）。`fetch.sh` を忘れても、v1 の 34 分のあとではなく、すぐに分かる。通過したときの表示と `out/` のファイルは[ルートの README](../README.ja.md#最初に実行すること)で説明する。

### JSON の記録

`lib/report.py` を使うスクリプト（`verify/`・`produce/`・`supplementary/` のすべて）は、次の鍵をもつ `out/<段>.json` を書く（形式 2）。

| 鍵 | 内容 |
|---|---|
| `format` | 2（v2026-10-25 までの形式 1 には `format`、`arguments`、`code`、`inputs`、`blas`、`compiler` が無い） |
| `step`、`passed`、`error` | 段の名前。すべての検査が通り、スクリプトが最後まで進んだときだけ `true`。捕まえられなかったエラー（あれば） |
| `checks` | 表示した順の検査の一覧 `{"check": 見出し, "ok": true/false}` |
| `values` | 計算した値 `{見出し: 値}`。論文に載せた数や、後の段のために書いたファイルの SHA-256 を含む |
| `seconds`、`finished` | 実行時間と終了の時刻 |
| `arguments` | コマンドラインの引数 |
| `code` | `git`: 作業ツリーの `git describe --always --dirty`（コンテナのイメージのように git が無ければ `null`）。`files`: スクリプトと、それが読み込んだ `code/` のモジュールの、それぞれを読み込んだ時点の SHA-256、およびコンパイルした C のソースの SHA-256。実行中にファイルが書き換えられると実行は失敗になる（終了コード 1、`passed: false`） |
| `inputs` | 読んだ `data/` と `certificates/` の入力ファイルの SHA-256（それぞれ `lib/data.py` か `certificates/SHA256SUMS` と照合済み） |
| `python`、`numpy`、`blas`、`platform` | Python と numpy のバージョン、numpy をビルドしたときの BLAS（`numpy.show_config`）、OS |
| `compiler` | 列挙器 `verify/enum_interval.c` をコンパイルしたときだけ: コマンド、そのパス、`--version` の 1 行目、オプション、コンパイルしたソースの SHA-256（`source_sha256`。ハッシュを取ったバイト列そのものをコンパイルする）と実行ファイルの SHA-256（`executable_sha256`） |
| `certificate_hashes` | `--hashes FILE` を指定したときだけ: `certificates/SHA256SUMS` の代わりに使ったハッシュの一覧 |

終了コードはどのスクリプトでも、すべての検査が通れば 0、検査の失敗かエラーなら 1、使い方の誤り（未知のオプションや段名）なら 2 である。
`crosscheck/` の第 2 の実装は、`lib/` とコードを共有しないよう、意図して別の形の記録を書く（`out/crosscheck_all_data/<段>.json`、
または表示する `RESULT:` の行と入力のハッシュ）。

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
| `v7_even_bounding.py` | F5b、系 5.3、表 8 | 1,527,984 個の偶の類の下界を保証する代表元（再開可能。途中経過は SHA-256 で入力に結び付ける。`--threads`） | 24 CPU 時間（3 スレッドで 7.9 時間） | 3 GB |
| `v8_design_identities.py` | §6.3 | 球面デザインの恒等式 18 個（整合性の検査。証明には不要） | 14 分 | 2 GB |

F5b は無関係な 2 つの議論（v6 と v7）で確かめます。証明にはどちらか一方で足ります。

### 厳密さの確保

判定はすべて整数演算で行います。整数行列の積を（速さのために）浮動小数点で計算するところでは、実際の入力から、すべての部分和が 2²⁴（float32）
または 2⁵³（float64）未満の整数であることを先に確かめます。そのような積は厳密です。補助関数は `lib/exact.py` にあり、各スクリプトの冒頭に、
どの積をこの方法で計算するかを書いてあります。この保証と、結果が依存するほかの条件（int64 があふれないこと、展開や列挙が完全なこと）は、
`python -O` で取り除かれる `assert` ではなく、例外を送出する `require(...)` で書きます。さらに `-O` の下では各段が開始を拒否します（古い `out/<段>.json` を消し、拒否したことをそこに記録します）。
F1 の列挙は外向きに丸める区間演算を使います（`verify/enum_interval.c` の冒頭）。

これらの論拠は、計算機についての前提に依る。前提は、明記したもののほかはコードで確かめない。部分和の上界による議論は、足し算の順序や
積和演算（FMA）の有無によらず浮動小数点の積を厳密にする。ただし、BLAS が行列の積を個々の積の IEEE 浮動小数点の和として計算することを
仮定する。OpenBLAS、MKL、BLIS、Accelerate はこれを満たし、Strassen 型の算法や精度を落とした計算核はこれを満たさない。`enum_interval.c` の
区間演算は、IEEE の binary64、最近接丸め、余分な精度なしを仮定する。`FLT_EVAL_METHOD` が 0 でなければコンパイルを止め、丸めのモードは
実行時に確かめ、区間の端点は C が厳密に読める 16 進表記で Python から渡す。使った BLAS と C コンパイラは JSON の記録に残る。

## 動作環境

* `verify/`、`crosscheck/second_impl/`: Python 3.10 以上と numpy（Python 3.12、numpy 2.5 で確認）。v1 には 128 ビット整数をもつ C コンパイラ（gcc か clang。`$CC` があればそれ、無ければ `cc`・`gcc`・`clang` の順に探す）。`fetch.sh` には `curl` が必要です。ほかのパッケージは要りません。
* `produce/`、`supplementary/`、`crosscheck/all_data/`: SageMath 10（PARI/GP、GAP、fpylll を含む）。SageMath 10.9 で確認。リポジトリのルートの
  `environment.yml` で conda/micromamba から入れられます。これらのスクリプトは、その環境の `python3` で実行します（`python3 -I code/...`）。
  conda-forge 版の SageMath では `sage -python` は使えません。
* コンテナ: リポジトリのルートの `Dockerfile` は、`verify/` のためにこれらを備えたイメージを作ります（SageMath 入りのイメージは `Dockerfile.sage`）。ルートの README を参照してください。
* `lean/`: Lean 4 と Mathlib（版は `lean/lean-toolchain` と `lean/lake-manifest.json` に固定）。

## 試験

`tests/` には小さな例による試験（スモークテスト）があり、[pytest](https://pytest.org) で書いてあります。pytest が必要なのはこの試験だけで、
検算そのものは numpy だけを使います。リポジトリのルートから次のように実行します。

```bash
pip install pytest
python -m pytest code/tests                  # 実行できるものすべて。検証用データが無ければ約 40 秒
python -m pytest code/tests -m "not slow"    # 数秒
python -m pytest code/tests -m data          # certificates/*.npz（fetch.sh）が必要。約 10 分、3 GB
```

マーカーは `slow`（検算スクリプト全体を子プロセスで走らせるもの。数秒より長い）と `data`（大きな検証用データが必要。無ければ飛ばす）です。
CI は pull request ごとに `-m "not data"` を実行し、`data` の試験は週に 1 回と手動で実行します（`.github/workflows/data-tests.yml`）。

対象: 厳密さの保証と線形代数、総当たり・既知の格子との比較による列挙器の検査、L に対する列挙器の入力（列挙の手前までの v1 の経路）、
群の閉包と 2 を法とする標準形、すべての最小ベクトルとの内積の最大（v5・v7 が使う `MinimalVectors.max_abs_inner`）の、群をもつ小さな格子での
総当たりとの比較、結果の記録・JSON の形式・途中経過の扱い、v4 から v6・v8 への受け渡し（`load_output_of`。変わったファイル、別の入力、
別のコードを拒否しなければならない）、v0・v2・`v1 --controls-only`、公開ハッシュとの一致と改変した入力の拒否、データが無いときに `proof.sh` が
計算の前に止まること（`preflight.sh`）、ディレクトリの間の依存の規則、`code/` と `lean/` のシェル構文。`data` の試験では、公開したデータと改変した certificate で v5、別の入力のための途中経過の有無を変えて
`v7 --limit 64` を走らせます。個々の例は `tests/test_*.py` を参照してください。

対象外: これらの試験は定理の検算ではなく、`proof.sh` や `full.sh` の代わりにはなりません。L についての v1 の列挙、v3、v4、v6、v8、64 組を超える v7、
`produce/`、`crosscheck/`、`supplementary/`、`lean/` は走らせません。

## 検証用データの生成

| スクリプト | 作るもの | 時間 |
|---|---|---|
| `produce/p1_centralizer.py` | M′ と中心化群 C（`centralizer.npz`、`commutant.npz`） | 10 分 |
| `produce/p2_minimal_orbits.py` | `min_reps.npz`（閉包、§6.2） | 10 分 |
| `produce/p3_norm8_orbits.py` | `norm8_reps.npz`（印の付く元（2 本の最小ベクトルの和）、§6.4） | 1.2 時間（メモリ: 最初からなら最大 7.3 GB、再開なら約 4.5 GB） |
| `produce/p4_odd_descent.py` | `odd_bounding.npz`（降下、§6.6） | 6 分 |
| `produce/p5_even_descent.py` | `even_bounding.npz`（降下、§6.7。6 分割、再開可能） | 約 190 CPU 時間 |
| `produce/p6_reduction.py` | `reduction_L.txt`、`reduction_L112.txt` | 1 分 |

`produce/descent.py`（p4・p5 の降下）と `produce/exact_qfminim.py`（PARI の `qfminim` に、`verify/` の列挙器による完全性の検査を加えたもの）は、
これらのスクリプトと `supplementary/` が使う補助である。

生成スクリプトは `certificates/` には書きません（そこのファイルは `certificates/SHA256SUMS` で固定されています）。各スクリプトは、配布ファイルと
同じ名前で `out/p<k>/` の下に書き（たとえば `out/p4/odd_bounding.npz`）、そのあと配布した検証用データと比べます。違いがあれば `[FAIL]` と
終了コード 1 で報告します。p3・p4・p5・p6 は配布ファイルをビット単位で再現しなければなりません（p6 はテキストのファイルをバイト単位で比べ、
p3 はまず類 x u_k + 2L の標準形の集合、軌道の個数、軌道の大きさの多重集合を比べ、そのあとファイルを比べます）。p1 は C/{±1} の 6 元を符号を除いた
集合として、M′ の基底を張る Z-格子（Hermite 標準形の一致）で比べる。実際には p1 のファイルも配布ファイルと同一である。p2 は類 r + 2L の標準形の
集合（最小ベクトルではこれが同じ軌道を意味します）と代表の個数で比べます。試しの実行（`p3 --trial`、`p5 --limit`）は別の名前のファイルを使い、
本番の実行のファイルや途中経過を上書きしません。

ここでの「再現」の意味: 各生成スクリプトは、前の生成スクリプトの出力ではなく、配布した上流のファイルを読む（p3 と p4 は `certificates/min_reps.npz`、
p5 は `certificates/norm8_reps.npz`、どれも `certificates/centralizer.npz` を読む）。したがって、比べているのは段ごとの再現である。配布した
`min_reps.npz` は、p2 を今の形に書く前に、元の計算で見つけたものである。閉包は同じだが、SageMath の標本抽出で無作為に選んだ最小ベクトルから
始めた。p2 は同じ 656 軌道を別の代表で見つけ（符号を除いても配布した代表と一致するものは無い）、配布したファイルそのものは作り直せない。証明は
代表の見つけ方に依らない（v3 が代表を確かめる）。p3 は、元の計算と同じく、SL₂(29) の各組 {g, −g} から先に見つかった元を取るので、
`norm8_reps.npz` を同じ並びで再現する（符号の取り方によらず軌道は同じだが、別の取り方では別の代表が別の並びで出る）。

`supplementary/genus/genus.py` のデータを作る段（`enum`、`build`、`witness`、`identify`）は、既定では `certificates/` ではなく `out/genus/` に書き、
書いたファイルを配布したファイルと比べます（同じ、整数が同じ、違う、のいずれかを報告します。`genus_classes.txt` は一致しなければならず、
ほかのファイルは近傍の歩き方や PARI の列挙順によって違うことがあります）。配布したファイルを置き換えるには `--dest certificates/` を指定します。

## 第 2 の実装と補足の計算

`crosscheck/all_data/check_all.py <段>`（SageMath を含む Python。docstring を参照）は、段 `theta`、`v0`、`v1`（後の段が使う
最小ベクトルの表を作る）、`v2`、`v3cheap`、`v4`、`v3full`、`neg`、`summary` をこの順に走らせます。各段は判定が FAIL なら
終了コード 1 で終わります。`summary` は、必須の段がすべて今の入力で合格していなければ終了コード 1 で終わります（入力は
`SHA256SUMS` と照合し、キャッシュは入力のダイジェストごとに分けて置きます）。`min_L.py 4` と `min_L.py 4 --test e8x7` は F1 と
その陽性対照を確かめます。`crosscheck/second_impl/` の 3 本（numpy のみ。引数は `--help` で表示する）は、結果を論文の数と比べ、
`RESULT: PASS`（終了コード 0）か `RESULT: FAIL`（終了コード 1）で終わります。

```bash
python3 -I code/crosscheck/second_impl/odd_classes.py           # F5a、表 7（数分、2 GB）
python3 -I code/crosscheck/second_impl/even_classes.py C B      # 標準形による F5b。B は陰性対照
python3 -I code/crosscheck/second_impl/design_identities.py 3   # norm8_reps.npz に対するデザインの恒等式（試験ベクトル 3 本）
```

第 2 の実装はどれも、入力ファイルを自前のコードで `data/SHA256SUMS` と `certificates/SHA256SUMS` に照合し、ハッシュを表示または記録する。

`bash code/run_supplementary.sh [段名…]` は `supplementary/` の計算を走らせます（既定では 30 段すべてで、1 コアで約 6 時間かかる。
そのうち `float_cvp610` が約 2.5 時間。一覧、各段の時間、収録していないものはスクリプトの冒頭にある）。SageMath を含む Python を `PYTHON` で
（既定は `python3`。例えば `environment.yml` の conda 環境のもの。SageMath の配布物なら `PYTHON="sage -python"`。`-I` を付けて呼ぶ）、
CTblLib を含む GAP を `GAP` で（既定は `gap`）与え、`fetch.sh` でデータを取得しておきます。段 `gluing_b` には `verify/v4_norm8_orbits.py` が
書く `out/K8.npy` が要ります。先の段の出力を読む段がある（`identify_nebe` と `nebe_tables` は `nebe_lattices` の、`nebe_gluings` と
`reduction_to_nebe` は `nebe_tables` の、`anatomy_b` は `gluing_b` の、`route_t_recount` は `route_t_classify` の出力）。入力が無い段は、先に
走らせる段を示して失敗とする。失敗した段があっても残りは続け、最後に失敗した段を一覧にして終了コード 1 で終わります。各段は `out/logs/<段>.log` を
書き、Python の段は段の名前の JSON の記録も書く（`out/gluings.json` など。`route_t_check_search3.json`、`route_t_exclusion_check.json`、
`isometry_ab_check.json` はモードを付けた名前）。いくつかのスクリプトが共有する関数（偶奇を保つ写像の類、
同変な等長写像の探索など）は `supplementary/_shared.py` にあります。

## 証明経路 T（補遺 §S4、表 D2 の [C20]・[C21]・[C32]）

`supplementary/route_t/` は、L₁₁₂ のエルミート構造を使う極値性の別証明（証明経路 T）の計算です。定理 A の証明には使いません。証明経路 T（補遺の定理 S4.1）は、追加の有限の検査（`exclusion.py`、[C32]）によって、主証明と同じ計算 F5a・F5b に帰着します。不変量による分類と三つの探索は照合のための計算です。

| スクリプト | 内容 | 時間 |
|---|---|---|
| `exclusion.py` | [C32] 証明経路 T の最後の検査: 命題 S4.2 の範囲の危険な台加群はどれも F5a か F5b に反する配置を含む（`check`: Python の標準ライブラリだけ、自前の列挙。`make`: 証拠を作る） | check 約 8 分、make 約 1 分（SageMath） |
| `classify.py`, `recount.py` | [C20] 照合: 階数 2 の台加群の分類（2 通りの独立な数え上げ。97 型・危険 63 型と、粗い不変量で 58 型の一致） | 各 1〜2 分（SageMath） |
| `certify.py` | [C21] 探索 (2)・(3) の代表元の生成（分割・再開可能） | 探索 (3) 約 25 分、探索 (2) 約 13 CPU 日 |
| `check.py` | [C21] 代表元の整数演算による検算（numpy だけ） | 探索 (3) 約 2 分、探索 (2) 約 7 CPU 時間（単一スレッド試験からの見積もり。分割 A の実測: 共用機で 2 スレッド、経過 4.7 時間） |
| `float_cvp.py` | [C21] 探索 (2) の浮動小数点の最近ベクトル列挙（補助） | 約 3 × 13 時間（SageMath） |

**この版の状態**: 両方の探索の代表元がそろっています。探索 (3) の 3,936 類と探索 (2) の 763,992 類すべてで、`check.py` の検算が通ります。公開タグ `certificates-v2` と Release の添付ファイルを使い、ネットワークを遮断しソースを読み取り専用にしたコンテナでも `check.py search2` を一度流し、763,992 類すべてで通りました（公開パッケージの再現性の確認であり、独立な証明ではありません）。
最初の Release `certificates-v1` の `certificates/route_t_search2.npz` は探索 (2) の 610,664 類分でした。`certificates-v2` で差し替えました
（以前からある行は変わっていません）。`fetch.sh` は古い複製の代わりに新しいファイルを取得します。途中のファイルの欠けた行を作り直すには、
P = 0, …, Q−1 について `certify.py search2 --missing --part P --nparts Q`（再開可能）を実行し、`certify.py collect --base` のあと、もう一度 `check.py` を実行します。

## 論文の表 D2 との対応

| 表 D2 | スクリプト |
|---|---|
| [C1] | verify/v2_theta.py |
| [C2] | verify/v0_inputs.py, supplementary/gluings.py (d), produce/p1_centralizer.py |
| [C3] | supplementary/gluings.py, supplementary/nebe/gluings_m.py (a), (b) (with supplementary/_shared.py) |
| [C4] | supplementary/gluing_b.py, supplementary/nebe/gluings_m.py (c), (d) (with supplementary/_shared.py) |
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
| [C18] | supplementary/fixed_sublattices.py（貼り方 B は `--tau B`。既定で BKZ-20〜BKZ-60。L₁₁₂ で約 10 分、B で約 18 分（大半は BKZ-60）。`--bkz 30,40` なら 1 分未満） |
| [C19] | supplementary/anatomy_b.py |
| [C20] | supplementary/route_t/classify.py, recount.py (with route_t/hermitian.py) |
| [C21] | supplementary/route_t/certify.py, check.py, float_cvp.py (with route_t/common.py) |
| [C32] | supplementary/route_t/exclusion.py (certificates/route_t_exclusion.json) |
| [C22] | lean/ (EEUL/L112/Chain.lean, check.sh) |
| [C23] | supplementary/nebe/identify_nebe.py (with nebe/lattices.py, nebe/cycloquat.py) |
| [C24] | supplementary/automorphisms/aut_normalizer.py (with automorphisms/aut_common.py, supplementary/_shared.py) |
| [C25] | supplementary/automorphisms/group_facts.g, out_facts.g, aut_diagonal.py (with automorphisms/aut_common.py, supplementary/_shared.py) |
| [C26] | supplementary/automorphisms/aut_structure.py, aut_character.py, endomorphisms.py (with automorphisms/aut_common.py, supplementary/_shared.py) |
| [C27] | crosscheck/all_data/check_all.py, min_L.py, min_L_enum.c |
| [C28] | supplementary/isometry_ab.py (find, check) (with supplementary/_shared.py) |
| [C29] | supplementary/genus/genus.py local, mass, enum (with genus/genus_steps.py, genus_lattice.py, genus_data.py) |
| [C30] | supplementary/genus/genus.py build, frames, witness (with genus/genus_steps.py, genus_lattice.py, genus_data.py) |
| [C31] | supplementary/genus/genus.py identify, check (with genus/genus_steps.py, genus_lattice.py, genus_check.py, genus_data.py, supplementary/_shared.py) |
