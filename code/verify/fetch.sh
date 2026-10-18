#!/usr/bin/env bash
# Download the large certificate files from the GitHub Release and check the SHA-256 hashes of all
# certificate files against certificates/SHA256SUMS (which is in git). The list of files to download
# is taken from SHA256SUMS itself (every .npz listed there), so the two cannot disagree.
# A file is downloaded only if it is missing or its hash differs from SHA256SUMS (an interrupted
# download, or a file replaced in a later release). It is downloaded to <file>.part, checked against
# its line of SHA256SUMS, and only then renamed to <file>; a file that fails the check is not kept.
# 大きな検証用データを GitHub Release から取得し、すべての検証用データの SHA-256 を certificates/SHA256SUMS（git に入っている）と照合する。
# 取得するファイルの一覧は SHA256SUMS そのもの（そこにあるすべての .npz）から取るので、両者が食い違うことはない。
# 取得するのは、ファイルが無いか、ハッシュが SHA256SUMS と違うとき（途中で切れた取得や、後のリリースで差し替えたファイル）だけである。
# <file>.part に取得し、SHA256SUMS のその行と照合してから <file> に改名する。照合に失敗したファイルは残さない。
# Run from the repository root / リポジトリの根から:  bash code/verify/fetch.sh [release tag]
# The environment variable CERT_BASE_URL replaces the download location
# https://github.com/.../releases/download/<tag> (e.g. a mirror, or a local server for testing).
# 環境変数 CERT_BASE_URL で取得元 https://github.com/.../releases/download/<tag> を置き換えられる（ミラーや試験用のローカルのサーバ）。
set -euo pipefail
TAG=${1:-certificates-v2}
BASE=${CERT_BASE_URL:-"https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/releases/download/$TAG"}
cd "$(dirname "${BASH_SOURCE[0]}")/../../certificates"
if command -v sha256sum >/dev/null; then SHA=(sha256sum); else SHA=(shasum -a 256); fi

# hash_of FILE: the SHA-256 of FILE. / FILE の SHA-256。
hash_of() { "${SHA[@]}" "$1" | awk '{print $1}'; }

for f in $(awk '{print $2}' SHA256SUMS | sed 's/^\*//' | grep '\.npz$'); do
  want=$(awk -v f="$f" '{n = $2; sub(/^\*/, "", n)} n == f {print $1}' SHA256SUMS)
  if [ -f "$f" ] && [ "$(hash_of "$f")" = "$want" ]; then
    continue
  fi
  [ -f "$f" ] && echo "$f: hash differs from SHA256SUMS; downloading it again / ハッシュが違うので取得し直す"
  rm -f "$f.part"
  curl -fL --retry 3 -o "$f.part" "$BASE/$f"
  got=$(hash_of "$f.part")
  if [ "$got" != "$want" ]; then
    rm -f "$f.part"
    echo "$f: downloaded file has SHA-256 $got, SHA256SUMS says $want / 取得したファイルのハッシュが SHA256SUMS と違う" >&2
    exit 1
  fi
  mv -f "$f.part" "$f"
done
"${SHA[@]}" -c SHA256SUMS
