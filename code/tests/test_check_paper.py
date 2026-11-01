"""paper/tools/check-paper.py: its checks use a raising require, so they also run under python -O.
paper/tools/check-paper.py: 検査は例外を投げる require なので、python -O でも実行される。
"""
import os
import runpy

import pytest

from conftest import REPO, run_python

SCRIPT = os.path.join(REPO, "paper", "tools", "check-paper.py")


def test_passes_also_under_optimize():
    for flags in ([], ["-O"]):
        proc = run_python(flags + [SCRIPT])
        assert proc.returncode == 0, proc.stdout
        assert proc.stdout.startswith("PASS:") or "\nPASS:" in proc.stdout


def test_failed_check_stops_under_optimize():
    # A false condition stops the run with exit 1 even under -O (an assert would be skipped).
    # 偽の条件は -O でも終了コード 1 で止める（assert なら飛ばされる）。
    src = f"import runpy; runpy.run_path({SCRIPT!r})['require'](False, 'deliberate')"
    proc = run_python(["-O", "-c", src])
    assert proc.returncode == 1
    assert "FAIL: deliberate" in proc.stdout


GOOD = 'code/verify/v2_theta.py'


@pytest.mark.parametrize("row, message", [
    ('(id: "C1", files: (),', "must have distributed code"),                               # no code at all / コードが無い
    ('(id: "C1", files: (), published: false,', "must have distributed code"),
    (f'(id: "C1", files: ("{GOOD}",), published:false,', "must have distributed code"),     # any spacing / 空白によらない
    (f'(id: "C1", files: ("{GOOD}",), published : false,', "must have distributed code"),
    ('(id: "C1", files: ("certificates/SHA256SUMS",),', "must have distributed code"),      # data only / データだけ
    ('(id: "C1", files: ("code/verify/no_such_file.py",),', "absent distribution path"),
    ('(id: "C1", en: [no list of files],', "no list of files"),
])
def test_ledger_row_without_distributed_code_is_refused(row, message):
    # A row of Table D2 that names no distributed code, or a file that does not exist, stops the run.
    # 配布するコードを指さない行や、存在しないファイルを挙げる行は、実行を止める。
    with pytest.raises(SystemExit) as stopped:
        runpy.run_path(SCRIPT)["check_ledger_row"](row)
    assert message in str(stopped.value)


def test_ledger_row_with_distributed_code_passes():
    runpy.run_path(SCRIPT)["check_ledger_row"](f'(id: "C1", files: ("{GOOD}",), en: [the published data],')
