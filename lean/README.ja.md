# 論証の形式化

[English](README.md)

## 何を証明しているか

`EEUL/L112/Chain.lean` は、論文の計算事実 F1〜F5 から「L₁₁₂ にノルム 10 未満のベクトルが無い」への導出を、Lean 4 と Mathlib で証明します。計算事実は仮定で、構造体 `Setting`・`Data`・`DataCert`・`DataCanonical` のフィールドとして置きます。行列を読むことも、証明書の検算を走らせることもしません。形式化した主張と Lean の外に残るものは論文 §7.1（表 9）にあります。

## Chain.lean の読み方

- まず冒頭のモジュールコメント（証明すること、読む順、仮定、記法）を読みます。次に `theoremA`（F5b を証明書で確かめた場合）と `theoremA_canonical`（F5b を標準形で確かめた場合）の主張と、それらが仮定する `Setting`・`Data` のフィールドを見ます。残りは証明です。
- 写像は左から書きます。`S.τ x`・`g r` は論文の xτ・rg です。`S.N x` はノルム ⟨x, x⟩、`2 • y` は y + y です。
- 証明は短いタクティク列で、論文の整数の場合分けは `omega` が閉じます。

## 検査の仕方

Lean と Mathlib の版は `lean-toolchain` と `lake-manifest.json` で固定してあります。`elan` が `lean-toolchain` の版を入れます。そのうえで次を実行します。

```bash
cd lean
lake exe cache get   # Mathlib のキャッシュ（初回のみ。数百 MB）
./check.sh
```

`check.sh` は Lean のリファレンスの手順（[Validating Proofs](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)）に従い、警告をエラーとしてパッケージをビルドし（`sorry` はどこにあっても警告になり、Mathlib の標準 linter の警告も同じ）、各定理が依存する公理（`lake env lean CheckAxioms.lean`）を `expected-axioms.txt` と比較し（公理は `propext`・`Classical.choice`・`Quot.sound` だけ。`sorry`・`native_decide`・追加の `axiom` はここに現れる）、`leanchecker` で宣言をカーネルに検査し直させます（カーネルを迂回した宣言もここで捕まる）。計算事実についての仮定は仮定のまま残ります。個別のコマンドは `lake build --wfail`、`lake env lean CheckAxioms.lean`、`lake env leanchecker EEUL.L112.Chain` です。`./check.sh --fresh` は読み込む Mathlib のモジュールも検査し直します（約 3 分）。CI はこれを各プルリクエストで実行します。

Mathlib のキャッシュがあれば、ビルドは 1 分程度、メモリは 2 GB 程度です（Lean 4.34.1 で実測 52 秒、1.7 GB）。メモリを制限するなら cgroup（例: `systemd-run --user -p MemoryMax=5G`）を使ってください。`ulimit -v` では Lean がスレッドを作れずに落ちます。
