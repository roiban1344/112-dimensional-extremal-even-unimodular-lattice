# 112 次元の極値偶ユニモジュラー格子

[English](README.md)

最小ノルム 10 の 112 次元偶ユニモジュラー格子を構成する論文の付属リポジトリです。格子を定義する行列、計算を用いた証明の検算プログラム、検証用データを配布します。

- **論文：** [英語 PDF](paper/paper.en.pdf)・[日本語 PDF](paper/paper.ja.pdf)・[本体・補遺のソースと組版手順](paper/README.ja.md)
- **検算：** [実行手順と論文との対応](code/README.ja.md)
- **データ：** [行列の約束](data/README.ja.md)・[検証用データの形式とハッシュ](certificates/MANIFEST.ja.md)
- **形式化：** [論証の Lean による検査](lean/README.ja.md)

## 最初に実行すること

リポジトリのルートで実行してください。主検算には Python 3.10 以降、NumPy、128 ビット整数に対応した GCC・Clang などの C コンパイラが必要です。

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-verify.txt
python3 code/verify/v0_inputs.py
```

最後のコマンドは、定義行列、群の作用、配布する Gram 行列への基底変換を検査します。**これだけでは最小ノルムは確定しません。**

証明で使う計算を検査するには、対象の版の検証用データを取得して実行します。

```bash
bash code/verify/fetch.sh certificates-v1
bash code/verify/full.sh 3
```

全検算には、素材となる 56 次元格子の最小ノルムが 6 であることの列挙、軌道代表の網羅性、剰余類の最小ノルムの下界を保証する代表元の検査が含まれます。CPU 時間の目安は約 26 時間です（3 並列で経過時間約 9.5〜10 時間）。[各段の所要時間とメモリ](code/README.ja.md)を参照してください。結論には論文中の数学的な補題も使います。

`bash code/verify/quick.sh` は短縮した検査です。56 次元格子の列挙は陽性対照だけに対して実行するため、**通過しても定理の全検算にはなりません。** 独立な実装と検証用データの生成プログラムは、コードの案内で説明しています。

## 版と再現性

論文・コード・検証用データのハッシュは、同じタグの版を使ってください。大きな検証用データは Release の添付ファイルで配布し、ハッシュを `certificates/SHA256SUMS` に記録します。プログラムは検証用データを使う前にハッシュを照合します。実行結果は `out/` に保存します。

補遺の経路 T（§S4）はこの版では未完了です。探索 (2) の整数演算で検算する代表元は一部の類にしかなく、範囲は[コードの案内](code/README.ja.md)に記しています。計算が完了し次第ファイルを差し替えます。定理 A はこれに依存しません。

主検算は Python・NumPy・C を使います。検証用データの生成と補足計算には SageMath を使います（[environment.yml](environment.yml)）。Lean の形式化は、明示した仮定からの論理的な導出を検査するもので、格子の計算そのものを実行するものではありません。

## 著者とライセンス

roiban1344 が作業を指揮し、公開に責任を持ちます。研究・コード・検算・執筆には Claude（Anthropic）と OpenAI Codex を含む AI システムが関与しています。役割の詳細は論文に記します。

コードは MIT、文章・データは CC BY 4.0 で配布します。[LICENSE](LICENSE) を参照してください。
