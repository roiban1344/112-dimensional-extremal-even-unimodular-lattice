# 論証の形式化

[English](README.md)

## 何を証明しているか

`EEUL/L112/Chain.lean` は、論文の計算事実 F1〜F5 から「L₁₁₂ にノルム 10 未満のベクトルが無い」への導出を、Lean 4 と Mathlib で証明します。計算事実は仮定で、構造体 `Setting`・`Data`・`DataCert`・`DataCanonical` のフィールドとして置きます。行列を読むことも、証明書の検算を走らせることもしません。形式化した主張と Lean の外に残るものは論文 §7.1（表 9）にあります。

## ファイル

| ファイル | 中身 |
|---|---|
| `EEUL/L112/Chain.lean` | 形式化の本体。仮定 F1〜F5 と表 9 の定理 |
| `EEUL.lean` | ライブラリの根のモジュール。`EEUL.L112.Chain` を読み込む |
| `CheckAxioms.lean` | 表 9 の各定理の `#print axioms` |
| `expected-axioms.txt` | `CheckAxioms.lean` の期待する出力 |
| `check.sh` | [検査の仕方](#検査の仕方)の節の 3 つの検査 |
| `lakefile.toml` | Lake のパッケージの定義（名前、Lean のオプション、Mathlib への依存とリンター） |
| `lean-toolchain`・`lake-manifest.json` | Lean と Mathlib の版の固定 |

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

`check.sh` は Lean のリファレンスの手順（[Validating Proofs](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)）に従い、次の三つを行います。

1. 警告をエラーとしてビルドする（`lake build --wfail`）。`sorry` はどこにあっても警告になる。Mathlib の標準 linter の警告も同じ。
2. 各定理が依存する公理（`lake env lean CheckAxioms.lean`）を `expected-axioms.txt` と比較する。公理は `propext`・`Classical.choice`・`Quot.sound` だけで、`sorry`・`native_decide`・追加の `axiom` はここに現れる。
3. `leanchecker` で宣言をカーネルに検査し直させる（`lake env leanchecker EEUL.L112.Chain`）。カーネルを迂回した宣言もここで捕まる。

計算事実についての仮定は仮定のまま残ります。`./check.sh --fresh` は読み込む Mathlib のモジュールも検査し直します（約 3 分）。CI はこれをプルリクエストごとに実行します。

Mathlib のキャッシュがあれば、ビルドは 1 分程度、メモリは 2 GB 程度です（Lean 4.34.1 で実測 52 秒、1.7 GB）。メモリを制限するなら cgroup（例: `systemd-run --user -p MemoryMax=5G`）を使ってください。`ulimit -v` では Lean がスレッドを作れずに落ちます。
