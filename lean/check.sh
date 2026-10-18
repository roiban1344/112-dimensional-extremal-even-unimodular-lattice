#!/usr/bin/env bash
# Check of the Lean package (ledger entry C22 of the paper):
#   1. `lake build` succeeds (the Lean kernel has checked every proof);
#   2. the sources contain no forbidden keyword outside comments
#      (sorry, admit, axiom, native_decide, ofReduceBool, unsafe, implemented_by, extern, csimp);
#   3. the axioms each theorem depends on (`lake env lean CheckAxioms.lean`) equal expected-axioms.txt
#      (subsets of propext, Classical.choice, Quot.sound).
# Needs the toolchain of lean-toolchain and python3; run `lake exe cache get` once before.
# Lean パッケージの検査（論文の C22）: 1. ビルドが通る、2. コメントの外に禁止語が無い、
# 3. 各定理が依存する公理が expected-axioms.txt と一致する。事前に一度 `lake exe cache get`。
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "== 1. lake build"
lake build

echo "== 2. forbidden keywords outside comments"
python3 -I - <<'PY'
import pathlib, re, sys
bad = re.compile(r"\b(sorry|admit|axiom|native_decide|ofReduceBool|unsafe|implemented_by|extern|csimp)\b")
hit = False
for p in sorted(pathlib.Path("EEUL").rglob("*.lean")) + [pathlib.Path("EEUL.lean"), pathlib.Path("CheckAxioms.lean")]:
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"/-.*?-/", lambda m: "\n" * m.group(0).count("\n"), s, flags=re.S)  # block comments and docstrings
    for i, line in enumerate(s.split("\n"), 1):
        line = line.split("--")[0]  # line comments
        if bad.search(line):
            print(f"{p}:{i}: {line.strip()}")
            hit = True
sys.exit(1 if hit else 0)
PY
echo "none"

echo "== 3. axioms"
actual="$(mktemp)"
trap 'rm -f "$actual"' EXIT
lake env lean CheckAxioms.lean > "$actual"
diff -u expected-axioms.txt "$actual"

echo "PASS: build, no forbidden keywords, axioms as in expected-axioms.txt"
