# The argument in Lean / 論証の形式化

`EEUL/L112/Chain.lean` formalises the deductions from the stated lattice and certificate hypotheses to the absence of short vectors. It does not verify the numerical input or run the certificate checkers. See the paper for the scope of the formalisation.

`EEUL/L112/Chain.lean` は、格子と検証用データに関する明示した仮定から短いベクトルが存在しないことへの導出を形式化します。数値入力や検証用データの計算そのものは検査しません。対象範囲は論文を参照してください。

Lean and Mathlib versions are fixed by `lean-toolchain` and `lake-manifest.json`. With the matching Lean toolchain installed:

```bash
cd lean
lake exe cache get
lake build
lake env lean CheckAxioms.lean
```

The first command fetches the Mathlib cache; subsequent builds use the local dependencies. This package contains the argument of the paper (the part that takes the computational facts as hypotheses).

最初のコマンドは Mathlib のキャッシュを取得します。このパッケージには、本論文の論証（計算事実を仮定として置いた部分）を収めます。

`CheckAxioms.lean` lists the axioms used by the main results. The expected dependencies are only `propext`, `Classical.choice` and `Quot.sound`; the stated computational hypotheses remain hypotheses.

`CheckAxioms.lean` で主要な定理の公理への依存を表示します。標準の `propext`・`Classical.choice`・`Quot.sound` だけであることを確認します。計算事実についての仮定は残ります。
