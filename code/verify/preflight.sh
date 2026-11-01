#!/usr/bin/env bash
# Sourced by proof.sh, full.sh and quick.sh. `preflight PY FILE...` stops the script at once, before hours of
# computation, if PY cannot import numpy or a certificate file FILE is missing or differs from
# certificates/SHA256SUMS (each step checks the hashes again when it reads the files).
# proof.sh・full.sh・quick.sh が読み込む。`preflight PY FILE...` は、PY が numpy を読み込めないとき、または検証用データ FILE が
# 無いか certificates/SHA256SUMS と違うときに、何時間もの計算の前にすぐスクリプトを止める（各段もファイルを読むときにハッシュを照合する）。
preflight() {
  local py="$1"; shift
  # $py is split on purpose (PYTHON="sage -python") / $py は意図して分割する（PYTHON="sage -python" のため）
  # shellcheck disable=SC2086
  if ! $py -I -c 'import numpy' >/dev/null 2>&1; then
    echo "'$py' cannot import numpy: install it (python3 -m pip install -r requirements-verify.txt, see README.md)" >&2
    echo "'$py' が numpy を読み込めない。README.ja.md のとおり入れる" >&2
    exit 1
  fi
  local dir sha f want bad=()
  dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../certificates" && pwd)"
  if command -v sha256sum >/dev/null; then sha=(sha256sum); else sha=(shasum -a 256); fi
  for f in "$@"; do
    want=$(awk -v f="$f" '{n = $2; sub(/^\*/, "", n)} n == f {print $1}' "$dir/SHA256SUMS")
    if [ ! -f "$dir/$f" ] || [ -z "$want" ] || [ "$("${sha[@]}" "$dir/$f" | awk '{print $1}')" != "$want" ]; then
      bad+=("$f")
    fi
  done
  if [ ${#bad[@]} -gt 0 ]; then
    echo "certificates/: ${bad[*]}: missing or not the published file; run bash code/verify/fetch.sh first" >&2
    echo "certificates/ の ${bad[*]} が無いか、公開したファイルと違う。先に bash code/verify/fetch.sh を実行する" >&2
    exit 1
  fi
}
