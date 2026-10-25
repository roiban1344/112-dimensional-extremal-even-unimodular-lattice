# 112 次元の極値偶ユニモジュラー格子

[English](README.md)

最小ノルム 10 の 112 次元偶ユニモジュラー格子を構成する論文の付属リポジトリです。格子を定義する行列、計算を用いた証明の検算プログラム、検証用データを配布します。

- **論文：** [英語 PDF](paper/paper.en.pdf)・[日本語 PDF](paper/paper.ja.pdf)・[本体・補遺のソースと組版手順](paper/README.ja.md)
- **検算：** [実行手順と論文との対応](code/README.ja.md)
- **データ：** [行列の約束](data/README.ja.md)・[検証用データの形式とハッシュ](certificates/MANIFEST.ja.md)
- **形式化：** [論証の Lean による検査](lean/README.ja.md)

## 結果

論文の定理 A: このリポジトリのデータで定義する格子 L₁₁₂ は、最小ノルム 10 の 112 次元正定値偶ユニモジュラー格子である。112 次元で Mallows–Odlyzko–Sloane の上界 2⌊n/24⌋+2 が許す最大値が 10 なので、L₁₁₂ は極値である。定理 B でその自己同型群を決定し、位数は 1,169,280 である。補遺 §S6 では、SL₂(29) が L₁₁₂ と同じ形で作用する 112 次元の偶ユニモジュラー格子をすべて分類する。そのような格子は同変な等長同型を除いてちょうど 8 個あり、L₁₁₂ はその一つで、残りのうち一つを除くすべてはノルム 8 以下のベクトルを含む。

構成は、SL₂(29) を対称性としてもつ Nebe の 56 次元極値格子 2 枚を、この群と可換で τ² = −5 を満たす自己準同型 τ に沿って貼り合わせるものである。言い換えると、L₁₁₂ は ℤ[√−5] 上のエルミートテンソル積である。証明は計算機援用による。手で証明した補題によって極値性を 2L₅₆ を法とする有限個の剰余類の下界に帰着し、プログラムが配布データからその下界を整数演算で検査する（約 1.2 CPU 時間）。検査した事実から定理を導く論証は Lean 4 で形式化してある。

論文は草稿であり、査読を受けていない。計算・コード・執筆の大部分は、人間の指揮のもとで AI システムが行った（下の「著者とライセンス」を参照）。

## 背景

偶ユニモジュラー格子とは、ℝⁿ の格子で、すべてのベクトルの長さの二乗（ノルム）が偶数であり、Gram 行列の行列式が 1 のものをいう。このような格子は n が 8 の倍数のときにしか存在しない。モジュラー形式の理論から最小ノルムには上界 2⌊n/24⌋+2 があり、この上界に達する格子を極値格子と呼ぶ。極値格子では、0 でない最短のベクトルが理論の許す限り長い。すなわち、その次元の偶ユニモジュラー格子として可能な限り密な球充填を与える。極値格子は稀である。古典的な例は E₈（n = 8）と Leech 格子（n = 24）で、80 次元までの 8 の倍数の各次元には例が知られている（80 次元は 1998 年に Bachoc と Nebe が、72 次元は 2010 年に Nebe が構成した）。88 次元は 2026 年の坂本のプレプリントで構成された。96 次元と 104 次元は未解決である。L₁₁₂ は 88 次元より先で知られている最初の例であり、上界が 10 となる次元での最初の例でもある。96・104 ではなく 112 次元を選んだのは、Siegel の質量公式に基づく目安から、極値格子が最も見つけやすい次元だと見込まれたためである（補遺 §S1）。

## リポジトリの中身

追跡しているファイルはすべて、下の表からたどれるいずれかの README で説明しています（`code/tests/test_docs.py` がこれを確かめます）。

| 場所 | 中身 | 定理 A の検算に要るか |
|---|---|---|
| [`paper/`](paper/README.ja.md) | 論文と補遺（Typst のソースと PDF）、図 1 の原本、ソースの整合性の検査 | 読む |
| [`data/`](data/README.ja.md) | 格子を定義する 4 つの行列 | 要る |
| [`certificates/`](certificates/MANIFEST.ja.md) | 検証用データ。小さいファイルは git に、大きい `.npz` は Release の添付ファイルに置き、すべて `SHA256SUMS` で固定する | `verify/` が確かめるファイルは要る |
| [`code/verify/`](code/README.ja.md#検算の各段)・[`code/lib/`](code/README.ja.md#ファイル) | F0〜F5 の検算（`proof.sh`・`full.sh`・`quick.sh`・`fetch.sh`）とその共有ライブラリ（NumPy を使う Python と C のプログラム 1 本） | 要る |
| [`code/produce/`](code/README.ja.md#検証用データの生成) | 検証用データを生成したプログラム（SageMath） | 要らない。証明が使う性質はすべて `verify/` が確かめ直す |
| [`code/crosscheck/`](code/README.ja.md#第-2-の実装と補足の計算) | 検算の第 2 の実装 | 要らない（照合） |
| [`code/supplementary/`](code/README.ja.md#論文の表-d2-との対応) | 定理 A 以外の主張の計算（貼り方、自己同型群、経路 T、補遺 §S6 の種など） | 要らない |
| [`code/tests/`](code/README.ja.md#試験) | 小さな例による試験（pytest） | 要らない |
| [`lean/`](lean/README.ja.md) | F1〜F5 からノルム 10 未満のベクトルが無いことを導く論証の Lean 4 による形式化 | 要らない（論証の独立な検査） |
| `Dockerfile`・`.devcontainer/devcontainer.json`・`requirements-verify.txt` | 下の水準 (i)〜(iii) のための軽量なコンテナイメージ、それを使う開発コンテナ、NumPy の版の固定 | 任意 |
| `Dockerfile.sage`・`environment.yml` | `produce/`・`crosscheck/all_data/`・`supplementary/` のための SageMath の環境 | 要らない |
| `.github/` | CI。`checks.yml`（プルリクエストごとに入力・試験・コンテナ・Typst・Lean を検査し、Release ごとに PDF を添付する。PDF は `actions/build-pdfs/action.yml` が作る）と `data-tests.yml`（大きなデータを使う試験を毎週実行する） | 要らない |
| `CITATION.cff`・`LICENSE`・`.gitattributes`・`.gitignore`・`.dockerignore` | 引用のためのメタデータ、ライセンス、git と Docker の設定 | 要らない |

## 最初に実行すること

リポジトリのルートで実行してください。主検算には Python 3.10 以降、NumPy、128 ビット整数に対応した GCC・Clang などの C コンパイラが必要です。検査は 3 段あります。

**(i) 入力だけ（20 秒）。** Debian・Ubuntu では `python3 -m venv` にパッケージ `python3-venv` が必要です。

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-verify.txt
python3 code/verify/v0_inputs.py
```

最後のコマンドは、定義行列、群の作用、配布する Gram 行列への基底変換を検査します。**これだけでは最小ノルムは確定しません。**

**(ii) 証明に使う計算（約 1.2 CPU 時間）。** 対象の版の検証用データを取得して実行します。

```bash
bash code/verify/fetch.sh
bash code/verify/proof.sh
```

`fetch.sh` には `curl` が必要です。引数は Release のタグで、省略すると `certificates-v2` です。`certificates/SHA256SUMS` に載っているすべての `.npz` ファイル（9 個、約 150 MB）を取得し、`full.sh` や補足の検査だけが使うものも含みます。`SHA256SUMS` のハッシュと一致するファイルが既にあれば取得し直しません。無いファイル、途中で切れたファイル、古いファイルは `<file>.part` に取得し、ハッシュを確かめてから置き換えます。`proof.sh` は定理 A の証明で使う計算の検査をすべて行います。F1（素材となる 56 次元格子の最小ノルムが 6）は区間演算の列挙で、F2・F3（軌道代表の網羅性）、F5a（奇の剰余類の下界を保証する代表元）、F5b（標準形）を検査します。結論には論文中の数学的な補題も使います。[各段の所要時間とメモリ](code/README.ja.md#検算の各段)を参照してください。

**(iii) すべて（約 26 CPU 時間、3 並列で経過時間約 9.5〜10 時間）。**

```bash
bash code/verify/full.sh 3
```

`proof.sh` の全部に加えて、F5b を偶の剰余類の下界を保証する代表元で確かめる代替の検査（v7、約 24 CPU 時間）と、球面デザインの恒等式の整合性の検査（v8）を行います。

`bash code/verify/quick.sh` は約 40〜50 分の短縮した検査です。56 次元格子の列挙は陽性対照だけに対して実行し、v7 と v8 を省くので、**通過しても定理の全検算にはなりません。** 独立な実装と検証用データの生成プログラムは、コードの案内で説明しています。

### コンテナ

`Dockerfile` から軽量なイメージ（Debian 13、Python 3、仮想環境中の NumPy、GCC、curl。SageMath と Lean は含まない）を作り、3 つの水準をすべて実行できます。`docker build -t l112 .` でイメージを作り、`docker run --rm l112` で水準 (i) を、`mkdir -p out && docker run --rm -v "$PWD/certificates:/work/certificates" -v "$PWD/out:/work/out" l112 bash -c 'bash code/verify/fetch.sh && bash code/verify/proof.sh'` で水準 (ii) を実行します（ダウンロードしたデータと結果はホストに残ります。水準 (iii) では `proof.sh` を `full.sh 3` に替えます。`out/` は例のとおり先に作ってください。無いと Docker が root 所有で作り、コンテナから書き込めません。Linux で uid が 1000 でない場合は `--user "$(id -u):$(id -g)"` を付けます）。開発コンテナ（`.devcontainer/`）も同じイメージを用います。VS Code では「Reopen in Container」を選ぶか、GitHub Codespaces でリポジトリを開いてください。`Dockerfile.sage` は補足計算とデータ生成のための SageMath 入りの別イメージであり、証明には不要です。

## 版と再現性

版には日付のタグを付けます。この版は `v2026-10-25` です（同じ日に 2 度目の版を出す場合は末尾に番号を付けます）。論文・コード・検証用データのハッシュは、同じタグのものを使ってください。大きな検証用データは [Release `certificates-v2`](https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/releases/tag/certificates-v2) の添付ファイルで配布し、ハッシュを `certificates/SHA256SUMS` に記録します。プログラムは検証用データを使う前にハッシュを照合します。実行結果は `out/` に保存します。

引用には、GitHub の「Cite this repository」を使ってください。[CITATION.cff](CITATION.cff) を読みます。

Release `certificates-v2` には、補遺 §S4 の探索 (2) の 763,992 類と探索 (3) の 3,936 類すべてについて、整数演算で検算済みの代表元を収めています。これらの探索は照合のための計算です。経路 T（補遺 §S4.1）は、別の論証と追加の有限の検査によって、主証明と同じ計算 F5a・F5b に帰着します。定理 A は経路 T に依存しません。

主検算は Python・NumPy・C を使います。検証用データの生成と補足計算には SageMath を使います（[environment.yml](environment.yml)）。Lean の形式化は、明示した仮定からの論理的な導出を検査するもので、格子の計算そのものを実行するものではありません。

## 著者とライセンス

roiban1344 が作業を指揮し、公開に責任を持ちます。研究・コード・検算・執筆には Claude（Anthropic）と OpenAI Codex を含む AI システムが関与しています。役割の詳細は論文に記します。

コードは MIT、文章・データは CC BY 4.0 で配布します。[LICENSE](LICENSE) を参照してください。
