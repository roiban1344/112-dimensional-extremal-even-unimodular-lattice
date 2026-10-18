#!/usr/bin/env bash
# Quick check (about 40–50 minutes, under 4 GB of memory). NOT a complete verification of Theorem A:
# it runs v0–v6 like proof.sh, but F1 (the interval enumeration proving min L = 6) is run on the
# positive controls only (v1 --controls-only), and v7 and v8 are omitted. Use proof.sh for the complete check.
# 短縮した検査（約 40〜50 分、メモリ 4 GB 未満）。定理 A の全検算では**ない**: proof.sh と同じく v0〜v6 を走らせるが、
# F1（min L = 6 を示す区間演算の列挙）は陽性対照だけ（v1 --controls-only）で、v7 と v8 は省く。全検算には proof.sh を使う。
# Python is run with -I (isolated mode: PYTHON* environment variables such as PYTHONOPTIMIZE are ignored).
# Python は -I（隔離モード。PYTHONOPTIMIZE などの PYTHON* 環境変数を無視する）で走らせる。
# Run from the repository root / リポジトリの根から:  bash code/verify/quick.sh
set -euo pipefail
PY=${PYTHON:-python3}
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
$PY -I "$D/v0_inputs.py"
$PY -I "$D/v1_min_L.py" --controls-only
$PY -I "$D/v2_theta.py"
$PY -I "$D/v3_minimal_orbits.py"
$PY -I "$D/v4_norm8_orbits.py"
$PY -I "$D/v5_odd_bounding.py"
$PY -I "$D/v6_canonical_lookup.py"
echo "quick check passed (F1 itself is in proof.sh; v7 and v8 are in full.sh) / 短縮した検査は通過（F1 そのものは proof.sh、v7 と v8 は full.sh）"
