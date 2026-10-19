"""lib/certs.py: certificate files are checked against the repository's certificates/SHA256SUMS, also when
they are read from another directory; another list of hashes is used only with --hashes FILE.
lib/certs.py: 検証用データは、別のディレクトリから読む場合もリポジトリの certificates/SHA256SUMS と照合する。
別のハッシュの一覧は --hashes FILE を指定したときにだけ使う。

Uses the text file reduction_L.txt, which is in git (no download needed).
git に入っているテキストのファイル reduction_L.txt を使う（取得は要らない）。
"""
import argparse
import hashlib
import json
import os
import shutil

import pytest

from conftest import CERTIFICATES, CODE, run_python
from lib import certs

NAME = "reduction_L.txt"


def write_sums(directory, names):
    with open(directory / "SHA256SUMS", "w") as f:
        for name in names:
            f.write(hashlib.sha256((directory / name).read_bytes()).hexdigest() + "  " + name + "\n")
    return directory / "SHA256SUMS"


@pytest.fixture
def modified(tmp_path):
    """A directory with a modified reduction_L.txt and a SHA256SUMS that matches it.
    改変した reduction_L.txt と、それに合わせた SHA256SUMS を置いたディレクトリ。"""
    d = tmp_path / "certificates"
    d.mkdir()
    text = open(os.path.join(CERTIFICATES, NAME)).read()
    (d / NAME).write_text(text.replace("1", "2", 1))
    return d, write_sums(d, [NAME])


def test_copy_in_another_directory_passes(tmp_path):
    shutil.copy(os.path.join(CERTIFICATES, NAME), tmp_path / NAME)
    assert certs.path_checked(NAME, str(tmp_path)) == os.path.join(str(tmp_path), NAME)


def test_modified_file_fails_despite_its_own_sha256sums(modified):
    d, _ = modified
    with pytest.raises(ValueError, match="differs from .*certificates/SHA256SUMS"):
        certs.path_checked(NAME, str(d))


def test_modified_file_passes_only_with_explicit_hashes(modified, monkeypatch):
    d, sums = modified
    monkeypatch.setattr(certs, "HASHES_FILE", str(sums))
    assert certs.path_checked(NAME, str(d)) == os.path.join(str(d), NAME)


def test_hashes_option_warns_and_is_recorded(modified, tmp_path):
    # --hashes changes the list in use, prints a warning, and the JSON of the run records it.
    # --hashes は使う一覧を変え、警告を表示し、実行の JSON に記録される。
    d, sums = modified
    out = tmp_path / "out"
    src = (f"import argparse, sys; sys.path.insert(0, {CODE!r})\n"
           "from lib import certs\nfrom lib.report import Report\n"
           "ap = argparse.ArgumentParser(); certs.add_arguments(ap)\n"
           f"a = ap.parse_args(['--certificates', {str(d)!r}, '--hashes', {str(sums)!r}])\n"
           f"rep = Report('t', {str(out)!r})\n"
           f"certs.path_checked({NAME!r}, a.certificates)\nrep.finish()\n")
    proc = run_python(["-c", src])
    assert proc.returncode == 0, proc.stdout
    assert "[warning] certificate hashes are read from" in proc.stdout
    with open(out / "t.json") as f:
        res = json.load(f)
    assert res["passed"] is True and res["certificate_hashes"] == str(sums)


def test_default_run_records_no_foreign_hashes(tmp_path):
    ap = argparse.ArgumentParser()
    certs.add_arguments(ap)
    a = ap.parse_args([])
    assert a.hashes is None and certs.HASHES_FILE == certs.DEFAULT_HASHES


def test_missing_hashes_file_is_an_error(tmp_path):
    ap = argparse.ArgumentParser()
    certs.add_arguments(ap)
    with pytest.raises(SystemExit):
        ap.parse_args(["--hashes", str(tmp_path / "absent")])
