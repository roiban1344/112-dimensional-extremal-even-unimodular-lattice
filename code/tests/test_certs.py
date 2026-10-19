"""lib/certs.py: certificate files are checked against the repository's certificates/SHA256SUMS, also when
they are read from another directory; another list of hashes is used only with --hashes FILE.
lib/certs.py: 検証用データは、別のディレクトリから読む場合もリポジトリの certificates/SHA256SUMS と照合する。
別のハッシュの一覧は --hashes FILE を指定したときにだけ使う。

Uses the text file reduction_L.txt, which is in git (no download needed).
git に入っているテキストのファイル reduction_L.txt を使う（取得は要らない）。
"""
import hashlib
import json
import os
import shutil

import pytest

from conftest import CERTIFICATES, CODE, run_python
from lib import certs

NAME = "reduction_L.txt"


@pytest.fixture
def modified(tmp_path):
    """A directory with a modified reduction_L.txt and a SHA256SUMS that matches it.
    改変した reduction_L.txt と、それに合わせた SHA256SUMS を置いたディレクトリ。"""
    d = tmp_path / "certificates"
    d.mkdir()
    text = open(os.path.join(CERTIFICATES, NAME)).read()
    (d / NAME).write_text(text.replace("1", "2", 1))
    (d / "SHA256SUMS").write_text(hashlib.sha256((d / NAME).read_bytes()).hexdigest() + "  " + NAME + "\n")
    return d


def test_copy_in_another_directory_passes(tmp_path):
    shutil.copy(os.path.join(CERTIFICATES, NAME), tmp_path / NAME)
    assert certs.path_checked(NAME, str(tmp_path)) == os.path.join(str(tmp_path), NAME)


def test_modified_file_fails_despite_its_own_sha256sums(modified):
    with pytest.raises(ValueError, match="differs from .*certificates/SHA256SUMS"):
        certs.path_checked(NAME, str(modified))


@pytest.mark.parametrize("with_hashes", [False, True])
def test_hashes_option(modified, tmp_path, with_hashes):
    # Without --hashes the modified file is refused and the JSON has no "certificate_hashes"; with it the file
    # passes, a warning is printed, and the JSON records the list. Run in a subprocess, since --hashes sets
    # module state. / --hashes が無ければ改変したファイルは拒否され、JSON に "certificate_hashes" は無い。
    # あれば合格し、警告を表示し、JSON に一覧を記録する。--hashes はモジュールの状態を変えるので別プロセスで実行する。
    sums = str(modified / "SHA256SUMS")
    args = ["--certificates", str(modified)] + (["--hashes", sums] if with_hashes else [])
    out = tmp_path / "out"
    src = (f"import argparse, sys; sys.path.insert(0, {CODE!r})\n"
           "from lib import certs\nfrom lib.report import Report\n"
           f"ap = argparse.ArgumentParser(); certs.add_arguments(ap); a = ap.parse_args({args!r})\n"
           f"rep = Report('t', {str(out)!r})\n"
           f"certs.path_checked({NAME!r}, a.certificates)\nrep.finish()\n")
    proc = run_python(["-c", src])
    with open(out / "t.json") as f:
        res = json.load(f)
    assert res["passed"] is with_hashes, proc.stdout
    assert ("[warning] certificate hashes are read from" in proc.stdout) is with_hashes
    assert res.get("certificate_hashes") == (sums if with_hashes else None)
