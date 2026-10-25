"""Every file tracked by git is described in a README (README.md, README.ja.md, MANIFEST.md, MANIFEST.ja.md).
git が追跡するファイルはすべて、いずれかの README（README.md、README.ja.md、MANIFEST.md、MANIFEST.ja.md）で説明されている。

A file counts as described if a README names it by its path or by a final part of its path (at least the
file name), for example `code/lib/mod2.py`, `lib/mod2.py` or `mod2.py`. A name may be a pattern: `*` stands
for any characters and `<j>` (any word in angle brackets) for a number, as in `genus_class_<j>.txt`. Skipped
when git or the .git directory is not available (for example in the container image).
README がファイルをパスか、パスの末尾の部分（少なくともファイル名）で書いていれば、説明されているとみなす（例 `code/lib/mod2.py`、
`lib/mod2.py`、`mod2.py`）。名前は型でもよい: `*` は任意の文字列、`<j>`（山括弧で囲んだ語）は数を表す（例 `genus_class_<j>.txt`）。
git か .git ディレクトリが無いとき（コンテナのイメージなど）は飛ばす。
"""
import os
import re
import shutil
import subprocess

import pytest

from conftest import REPO

DOC_NAMES = ("README.md", "README.ja.md", "MANIFEST.md", "MANIFEST.ja.md")


def tracked_files():
    if shutil.which("git") is None or not os.path.exists(os.path.join(REPO, ".git")):
        pytest.skip("git or .git is not available / git か .git が無い")
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return out.split()


def names_in(text):
    """The file names and paths written in the text (words containing a dot, or any word in backticks), as regular expressions."""
    pats = []
    words = re.findall(r"[\w.<>*/-]*\.[\w<>*]+", text) + re.findall(r"`([\w.<>*/-]+)`", text)
    for n in set(words):
        n = n.rstrip(".").removeprefix("./")
        if len(re.sub(r"\W", "", n)) < 3:   # Markdown such as **…** or a bare ellipsis, not a name
            continue
        p = re.escape(n)
        p = p.replace(r"\*", ".*")
        p = re.sub(r"<\w+>", r"\\d+", p)
        pats.append(re.compile(r"(?:.*/)?" + p + r"\Z"))
    return pats


def test_every_tracked_file_is_described():
    files = tracked_files()
    patterns = []
    for f in files:
        if os.path.basename(f) in DOC_NAMES:
            with open(os.path.join(REPO, f), encoding="utf-8") as fh:
                patterns += names_in(fh.read())
    missing = [f for f in files if os.path.basename(f) not in DOC_NAMES and not any(p.match(f) for p in patterns)]
    assert not missing, "files not described in any README / どの README にも説明が無いファイル:\n  " + "\n  ".join(missing)
