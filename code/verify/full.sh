#!/usr/bin/env bash
# Full verification of Theorem A (about 26 CPU hours; about 9.5-10 hours elapsed with 3 threads for v7,
# of which v7 itself takes 7.9 hours; under 4 GB of memory):
#   v0 F0, F4 | v1 F1 (interval enumeration, 34 min) | v2 theta series | v3 F2 | v4 F3 |
#   v5 F5a | v6 F5b by canonical forms | v7 F5b by even-class certificates (~24 CPU hours) |
#   v8 design identities (consistency test, not needed for the proof).
#   (proof.sh = v0-v6, about 1.2 CPU hours; full.sh adds the alternative even-coset certificate check v7 and the consistency test v8.)
#   proof.sh = v0〜v6（約 1.2 CPU 時間）。full.sh は代替の偶の剰余類の代表元の検査 v7 と整合性の検査 v8 を加える。
# Each step writes out/<step>.json; v7 can be interrupted and resumed (its checkpoint is bound to the inputs by SHA-256).
# Python is run with -I (isolated mode: PYTHON* environment variables such as PYTHONOPTIMIZE are ignored).
# 定理 A の全部の検算（約 26 CPU 時間。v7 を 3 スレッドで走らせると経過時間は約 9.5〜10 時間で、そのうち v7 が 7.9 時間。メモリ 4 GB 未満）。
# 各段は out/<step>.json を書く。v7 は中断して再開できる（途中経過は SHA-256 で入力に結び付ける）。
# Python は -I（隔離モード。PYTHONOPTIMIZE などの PYTHON* 環境変数を無視する）で走らせる。
# Run from the repository root / リポジトリの根から:  bash code/verify/full.sh [threads for v7]
set -euo pipefail
PY=${PYTHON:-python3}
T=${1:-1}
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
$PY -I "$D/v0_inputs.py"
$PY -I "$D/v1_min_L.py"
$PY -I "$D/v2_theta.py"
$PY -I "$D/v3_minimal_orbits.py"
$PY -I "$D/v4_norm8_orbits.py"
$PY -I "$D/v5_odd_bounding.py"
$PY -I "$D/v6_canonical_lookup.py"
$PY -I "$D/v7_even_bounding.py" --threads "$T"
$PY -I "$D/v8_design_identities.py"
echo "full verification passed / 全部の検算は通過"
