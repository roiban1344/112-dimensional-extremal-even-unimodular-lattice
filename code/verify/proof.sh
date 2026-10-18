#!/usr/bin/env bash
# Shortest complete check of the computational facts F0-F5 used in the proof of Theorem A
# (route A of Supplement Table S7): about 1.2 CPU hours (v1 is 34 min, v6 24 min, the rest minutes),
# under 4 GB of memory. It runs v0-v6. It omits the alternative even-coset certificate check v7
# (24 CPU hours) and the consistency test v8, which full.sh adds.
# Each step writes out/<step>.json.
# 定理 A の証明に使う計算事実 F0〜F5 を、すべて確かめる最短の検算（補遺 表 S7 の経路 A）。約 1.2 CPU 時間
# （v1 が 34 分、v6 が 24 分、残りは数分）、メモリ 4 GB 未満。v0〜v6 を走らせる。代替の偶の剰余類の代表元の検査 v7（24 CPU 時間）と
# 整合性の検査 v8 は省く（full.sh が加える）。各段は out/<段>.json を書く。
# Run from the repository root / リポジトリの根から:  bash code/verify/proof.sh
set -euo pipefail
PY=${PYTHON:-python3}
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
$PY "$D/v0_inputs.py"
$PY "$D/v1_min_L.py"
$PY "$D/v2_theta.py"
$PY "$D/v3_minimal_orbits.py"
$PY "$D/v4_norm8_orbits.py"
$PY "$D/v5_odd_bounding.py"
$PY "$D/v6_canonical_lookup.py"
echo "proof verification (v0-v6) passed / 証明に要る検算（v0〜v6）は通過"
