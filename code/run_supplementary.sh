#!/usr/bin/env bash
# Run the supplementary computations one after another (each writes a log out/logs/<name>.log, and most write
# out/<step>.json); a failing step does not stop the others. At the end the failed steps are listed and the
# exit code is 1 if any failed (2 for an unknown step name).
# 補足の計算を順に走らせる（各段はログ out/logs/<名前>.log を書き、多くは out/<step>.json も書く）。失敗した段があっても残りは続ける。
# 最後に失敗した段を一覧にし、一つでも失敗すれば終了コード 1 で終わる（未知の段名では 2）。
#
# Run from the repository root / リポジトリの根から:  bash code/run_supplementary.sh [names...]
#   (no names: all steps in the order below / 段名を省くと下の順にすべて)
#
# Prerequisites / 前提:
#   * PYTHON: a Python with SageMath (default python3, e.g. that of the conda environment of environment.yml;
#     PYTHON="sage -python" for a SageMath distribution). GAP with CTblLib as GAP (default gap).
#     SageMath を含む Python（既定は python3。例えば environment.yml の conda 環境のもの。SageMath の配布物なら PYTHON="sage -python"）。
#     CTblLib を含む GAP を GAP で（既定は gap）。
#   * the .npz files of certificates/ (bash code/verify/fetch.sh). / certificates/ の .npz（bash code/verify/fetch.sh）。
#   * gluing_b needs out/K8.npy from code/verify/v4_norm8_orbits.py (about 9 min); anatomy_b needs the output of
#     gluing_b, route_t_recount that of route_t_classify (both are earlier in the default order).
#     gluing_b には code/verify/v4_norm8_orbits.py の out/K8.npy（約 9 分）が要る。anatomy_b は gluing_b の、route_t_recount は
#     route_t_classify の出力を使う（どちらも既定の順では先に走る）。
# Not included (long or producing data; see the docstrings and code/README.md): float_enumerations.py cvp88,
#   route_t/certify.py, route_t/check.py search2, route_t/float_cvp.py, isometry_ab.py find, identify_nebe.py --check,
#   the genus.py steps other than check, and the --tau B variants other than fixed_sublattices_B.
# 収録していないもの（長時間か、データを作るもの。docstring と code/README.md を参照）: float_enumerations.py cvp88、
#   route_t/certify.py、route_t/check.py search2、route_t/float_cvp.py、isometry_ab.py find、identify_nebe.py --check、
#   genus.py の check 以外の段、fixed_sublattices_B 以外の --tau B の変種。
set -u
PY=${PYTHON:-python3}          # word-split on purpose, so that PYTHON="sage -python" works / PYTHON="sage -python" のため意図して分割する
GAP=${GAP:-gap}
C="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S="$C/supplementary"
LOG="$C/../out/logs"
mkdir -p "$LOG"

ORDER=(gluings frame_stabilizer node_estimate sample_check frames gluing_b anatomy_b fixed_sublattices fixed_sublattices_B
       float_svp float_qfminim float_cvp610 aut_normalizer aut_diagonal aut_structure aut_character endomorphisms
       group_facts out_facts nebe_lattices identify_nebe nebe_tables nebe_gluings reduction_to_nebe route_t_classify
       route_t_recount route_t_check3 route_t_exclusion isometry_ab genus_check)

step() {   # run step $1 / 段 $1 を実行する
  case "$1" in
    gluings)             $PY "$S/gluings.py" ;;
    frame_stabilizer)    $PY "$S/frame_stabilizer.py" ;;
    node_estimate)       $PY "$S/node_estimate.py" ;;
    sample_check)        $PY "$S/sample_check.py" ;;
    frames)              $PY "$S/frames.py" ;;
    gluing_b)            $PY "$S/gluing_b.py" ;;
    anatomy_b)           $PY "$S/anatomy_b.py" ;;
    fixed_sublattices)   $PY "$S/fixed_sublattices.py" ;;
    fixed_sublattices_B) $PY "$S/fixed_sublattices.py" --tau B ;;
    float_svp)           $PY "$S/float_enumerations.py" svp ;;
    float_qfminim)       $PY "$S/float_enumerations.py" qfminim ;;
    float_cvp610)        $PY "$S/float_enumerations.py" cvp610 ;;
    aut_normalizer)      $PY "$S/automorphisms/aut_normalizer.py" ;;
    aut_diagonal)        $PY "$S/automorphisms/aut_diagonal.py" ;;
    aut_structure)       $PY "$S/automorphisms/aut_structure.py" ;;
    aut_character)       $PY "$S/automorphisms/aut_character.py" ;;
    endomorphisms)       $PY "$S/automorphisms/endomorphisms.py" ;;
    group_facts)         $GAP -q --quitonbreak "$S/automorphisms/group_facts.g" < /dev/null ;;
    out_facts)           $GAP -q --quitonbreak "$S/automorphisms/out_facts.g" < /dev/null ;;
    nebe_lattices)       $PY "$S/nebe/lattices.py" ;;
    identify_nebe)       $PY "$S/nebe/identify_nebe.py" ;;
    nebe_tables)         $PY "$S/nebe/tables.py" ;;
    nebe_gluings)        $PY "$S/nebe/gluings_m.py" ;;
    reduction_to_nebe)   $PY "$S/nebe/reduction_to_nebe.py" ;;
    route_t_classify)    $PY "$S/route_t/classify.py" ;;
    route_t_recount)     $PY "$S/route_t/recount.py" ;;
    route_t_check3)      $PY "$S/route_t/check.py" search3 ;;
    route_t_exclusion)   $PY "$S/route_t/exclusion.py" check ;;
    isometry_ab)         $PY "$S/isometry_ab.py" check ;;
    genus_check)         $PY "$S/genus/genus.py" check ;;
    *)                   return 127 ;;
  esac
}

if [ $# -gt 0 ]; then
  for s in "$@"; do
    case " ${ORDER[*]} " in
      *" $s "*) ;;
      *) echo "unknown step: $s" >&2; echo "steps / 段: ${ORDER[*]}" >&2; exit 2 ;;
    esac
  done
  ORDER=("$@")
fi

FAILED=()
for s in "${ORDER[@]}"; do
  echo "=== $s ($(date '+%F %T'))"
  if step "$s" > "$LOG/$s.log" 2>&1; then
    echo "    ok"
  else
    echo "    FAILED (see out/logs/$s.log)"
    FAILED+=("$s")
  fi
done
if [ ${#FAILED[@]} -gt 0 ]; then
  echo "FAILED steps (${#FAILED[@]} of ${#ORDER[@]}): ${FAILED[*]}"
  exit 1
fi
echo "all ${#ORDER[@]} steps passed"
