# 論証の形式化

[English](README.md)

`EEUL/L112/Chain.lean` は、格子と検証用データに関する明示した仮定から短いベクトルが存在しないことへの導出を形式化します。数値入力や検証用データの計算そのものは検査しません。対象範囲は論文を参照してください。

Lean と Mathlib の版は `lean-toolchain` と `lake-manifest.json` で固定してあります。対応する Lean ツールチェーンを入れて、次を実行します。

```bash
cd lean
lake exe cache get
lake build
lake env lean CheckAxioms.lean
```

最初のコマンドは Mathlib のキャッシュを取得します。このパッケージには、本論文の論証（計算事実を仮定として置いた部分）を収めます。

`CheckAxioms.lean` で主要な定理の公理への依存を表示します。標準の `propext`・`Classical.choice`・`Quot.sound` だけであることを確認します。計算事実についての仮定は残ります。
