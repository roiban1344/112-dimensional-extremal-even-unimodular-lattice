"""lib/report.py (no stale JSON, failures recorded, -O refused) and the checkpoint logic of lib/shells.py.
lib/report.py（古い JSON を残さない、失敗を記録する、-O を拒否する）と lib/shells.py の途中経過の扱い。

Report installs an excepthook and an atexit handler, so it is exercised in subprocesses.
Report は excepthook と atexit を設定するので、子プロセスで試す。
"""
import json
import os
import subprocess
import sys

import numpy as np
import pytest

from conftest import CODE, run_python, run_step
from lib import certs, shells


def run_snippet(body, out_dir):
    """Run a short script that creates Report("t", out_dir) and then executes `body`.
    Report("t", out_dir) を作ってから `body` を実行する短いスクリプトを走らせる。"""
    src = (f"import sys; sys.path.insert(0, {CODE!r})\n"
           "from lib import require\nfrom lib.report import Report\n"
           f"rep = Report('t', {str(out_dir)!r})\n" + body)
    proc = run_python(["-c", src])
    path = os.path.join(out_dir, "t.json")
    res = None
    if os.path.exists(path):
        with open(path) as f:
            res = json.load(f)
    return proc, res


def test_stale_json_is_removed_at_start(tmp_path):
    with open(tmp_path / "t.json", "w") as f:
        json.dump({"step": "t", "passed": True}, f)
    proc, res = run_snippet("import os; print('exists', os.path.exists(rep.path), flush=True); os._exit(3)", tmp_path)
    assert "exists False" in proc.stdout and proc.returncode == 3
    assert res is None


def test_passed_run(tmp_path):
    proc, res = run_snippet("rep.check('one', True); rep.value('x', 7); rep.finish()", tmp_path)
    assert proc.returncode == 0
    assert res["passed"] is True and res["error"] is None and res["values"] == {"x": 7}


def test_failed_check(tmp_path):
    proc, res = run_snippet("rep.check('one', False); print('not reached')", tmp_path)
    assert proc.returncode == 1 and "not reached" not in proc.stdout
    assert res["passed"] is False and res["checks"] == [{"check": "one", "ok": False}]


def test_exception_writes_passed_false(tmp_path):
    proc, res = run_snippet("rep.check('one', True); require(False, 'boom')", tmp_path)
    assert proc.returncode == 1
    assert res["passed"] is False and res["error"] == "CheckError: boom"


def test_exit_without_finish(tmp_path):
    proc, res = run_snippet("sys.exit(0)", tmp_path)
    assert res["passed"] is False and res["error"] == "exited without calling finish()"


def test_optimized_mode_is_refused(tmp_path):
    # A stale "passed": true must be replaced by the refusal. / 古い "passed": true は拒否の記録に置き換わる。
    with open(tmp_path / "v2_theta.json", "w") as f:
        json.dump({"step": "v2_theta", "passed": True}, f)
    code, res, out = run_step("v2_theta.py", tmp_path, flags=["-O"])
    assert code == 1, out
    assert res["passed"] is False and "refused" in res["error"]
    assert "refusing to run under python -O" in out


def test_pythonoptimize_is_ignored_with_isolated_mode(tmp_path):
    # The shell scripts use python -I, which ignores PYTHONOPTIMIZE, so the checks still run.
    # シェルスクリプトは python -I を使い、PYTHONOPTIMIZE は無視されるので、検査は実行される。
    env = dict(os.environ, PYTHONOPTIMIZE="1")
    proc = subprocess.run([sys.executable, "-I", os.path.join(CODE, "verify", "v2_theta.py"), "--out", str(tmp_path)],
                          env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert proc.returncode == 0, proc.stdout


# --- checkpoints of lib.shells.max_abs_inner_checkpointed / 途中経過 ------------------------------------

class FakeMinimalVectors:
    """Stands in for shells.MinimalVectors: max |w_k| instead of max |<w, u>|; counts the rows computed.
    shells.MinimalVectors の代わり: max |<w, u>| の代わりに max |w_k| を返す。計算した行数を数える。"""

    def __init__(self):
        self.rows = 0

    def max_abs_inner(self, W, threads=1):
        self.rows += len(W)
        return np.abs(np.asarray(W, dtype=np.int64)).max(axis=1)


class FakeReport:
    """Stands in for report.Report: a failed check raises SystemExit(1) as Report.check does.
    report.Report の代わり: 失敗した検査は Report.check と同じく SystemExit(1) を送出する。"""

    def __init__(self):
        self.lines = []

    def log(self, *args):
        self.lines.append(" ".join(map(str, args)))

    def check(self, label, ok, stop=True):
        if not ok:
            raise SystemExit(1)


@pytest.fixture
def rows_and_fp(tmp_path):
    rng = np.random.default_rng(13)
    W = rng.integers(-9, 10, size=(40, 56)).astype(np.int16)
    inp = tmp_path / "input.txt"
    inp.write_text("1 2 3\n")
    return W, inp, shells.fingerprint(W, [str(inp)] + shells.CODE_FILES, {"n": len(W), "limit": None})


def test_checkpoint_fresh_run(tmp_path, rows_and_fp):
    W, _, fp = rows_and_fp
    mv = FakeMinimalVectors()
    mx, _, resumed = shells.max_abs_inner_checkpointed(mv, W, 1, 7, str(tmp_path / "s.npz"), fp, FakeReport())
    assert resumed == 0 and mv.rows == len(W)
    assert (mx == np.abs(W.astype(np.int64)).max(axis=1)).all()


def test_checkpoint_resumes_with_same_fingerprint(tmp_path, rows_and_fp):
    W, _, fp = rows_and_fp
    state = str(tmp_path / "s.npz")
    saved = np.full(len(W), -1, dtype=np.int64)
    saved[:15] = 99                                  # marks rows taken over / 引き継いだ行の印
    certs.save_npz(state, mx=saved, done=np.int64(15), seconds=np.float64(1.0), fingerprint=np.str_(fp))
    mv = FakeMinimalVectors()
    mx, secs, resumed = shells.max_abs_inner_checkpointed(mv, W, 1, 7, state, fp, FakeReport())
    assert resumed == 15 and mv.rows == len(W) - 15 and secs >= 1.0
    assert (mx[:15] == 99).all() and (mx[15:] == np.abs(W[15:].astype(np.int64)).max(axis=1)).all()
    assert not os.path.exists(state), "the checkpoint is removed when all rows are done"


@pytest.mark.parametrize("change", ["rows", "input", "limit", "none"])
def test_checkpoint_of_other_inputs_fails(tmp_path, rows_and_fp, change):
    W, inp, fp = rows_and_fp
    if change == "rows":
        W2 = W.copy()
        W2[3, 0] += 1
        other = shells.fingerprint(W2, [str(inp)] + shells.CODE_FILES, {"n": len(W), "limit": None})
    elif change == "input":
        inp2 = tmp_path / "other.txt"
        inp2.write_text("1 2 4\n")
        other = shells.fingerprint(W, [str(inp2)] + shells.CODE_FILES, {"n": len(W), "limit": None})
    elif change == "limit":
        other = shells.fingerprint(W, [str(inp)] + shells.CODE_FILES, {"n": len(W), "limit": 40})
    else:
        other = None                                 # a checkpoint without a fingerprint / 指紋の無い途中経過
    assert other != fp
    state = str(tmp_path / "s.npz")
    extra = {} if other is None else {"fingerprint": np.str_(other)}
    certs.save_npz(state, mx=np.zeros(len(W), dtype=np.int64), done=np.int64(len(W)), seconds=np.float64(0), **extra)
    mv, rep = FakeMinimalVectors(), FakeReport()
    with pytest.raises(SystemExit):
        shells.max_abs_inner_checkpointed(mv, W, 1, 7, state, fp, rep)
    assert mv.rows == 0
    assert os.path.exists(state), "a foreign checkpoint is not deleted silently"
    if other is not None:
        assert any(line.startswith("  differs:") for line in rep.lines)
