"""paper/tools/check-paper.py: its checks use a raising require, so they also run under python -O.
paper/tools/check-paper.py: 検査は例外を投げる require なので、python -O でも実行される。
"""
import os

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
