#!/usr/bin/env bash
# Check of the Lean package (ledger entry C22 of the paper), following the steps of the Lean reference
# manual (https://lean-lang.org/doc/reference/latest/ValidatingProofs/):
#   1. `lake build --wfail` succeeds: the Lean kernel has checked every proof, and there is no warning.
#      A `sorry` gives the warning "declaration uses 'sorry'", so it normally fails here, as do the
#      warnings of Mathlib's standard linters enabled in lakefile.toml. The guarantee is step 2: a
#      `sorry` can be hidden from the build (e.g. by `#guard_msgs in`), but not from `#print axioms`
#      of a theorem that uses it;
#   2. the axioms each theorem depends on (`lake env lean CheckAxioms.lean`) equal expected-axioms.txt
#      (subsets of propext, Classical.choice, Quot.sound). `sorry`, `native_decide` and any `axiom` the
#      proofs use would appear here as further axioms (sorryAx, ...);
#   3. `leanchecker` replays the declarations of EEUL.L112.Chain in the kernel, which also catches
#      declarations that bypassed the kernel (debug.skipKernelTC, addDeclWithoutChecking).
#      `./check.sh --fresh` replays the imported Mathlib modules as well (about 3 minutes).
# Needs the toolchain of lean-toolchain; run `lake exe cache get` once before.
# Lean パッケージの検査（論文の C22）。Lean リファレンスの手順に従う:
#   1. `lake build --wfail` が通る（カーネルがすべての証明を検査し、警告も無い）。`sorry` は警告
#      "declaration uses 'sorry'" になるので、通常はここで落ちる。lakefile.toml で有効にした Mathlib の
#      標準 linter の警告も同じ。保証の本体は手順 2: `sorry` はビルドからは隠せる（`#guard_msgs in` など）が、
#      それを使う定理の `#print axioms` からは隠せない;
#   2. 各定理が依存する公理が expected-axioms.txt と一致する。証明が使う `sorry`・`native_decide`・`axiom`
#      はここに別の公理（sorryAx など）として現れる;
#   3. `leanchecker` が EEUL.L112.Chain の宣言をカーネルで検査し直す。カーネルを迂回した宣言
#      （debug.skipKernelTC、addDeclWithoutChecking）もここで捕まる。`./check.sh --fresh` は読み込む
#      Mathlib のモジュールも検査し直す（約 3 分）。
# 事前に一度 `lake exe cache get`。
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "== 1. lake build --wfail"
lake build --wfail

echo "== 2. axioms"
actual="$(mktemp)"
trap 'rm -f "$actual"' EXIT
lake env lean CheckAxioms.lean > "$actual"
diff -u expected-axioms.txt "$actual"

echo "== 3. leanchecker $*"
lake env leanchecker "$@" EEUL.L112.Chain

echo "PASS: build without warnings, axioms as in expected-axioms.txt, kernel replay"
