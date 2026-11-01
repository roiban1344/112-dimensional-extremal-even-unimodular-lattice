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


# --- the format of out/<step>.json / out/<段>.json の形式 ---------------------------------------------------

def test_json_records_format_code_and_inputs(tmp_path):
    proc, res = run_snippet("import os\nfrom lib import data, enumerate as en\ndata.gram()\n"
                            "en.compile_enumerator(os.path.join(rep.out_dir, 'build'))\nrep.finish()", tmp_path)
    assert proc.returncode == 0, proc.stdout
    assert res["format"] == 2 and res["passed"] is True
    assert {"step", "error", "checks", "values", "seconds", "finished", "arguments", "python", "numpy", "blas",
            "platform"} <= set(res)
    from lib import data
    assert res["inputs"] == {"data/L56_gram.txt": data.SHA256["L56_gram.txt"]}
    files = res["code"]["files"]
    assert "code/lib/report.py" in files and "code/lib/data.py" in files and all(len(h) == 64 for h in files.values())
    assert "git" in res["code"]
    assert res["compiler"]["flags"] == ["-O2", "-std=c11", "-fno-fast-math", "-ffp-contract=off"]
    # The compiled C source and the executable are identified by their hashes (F1 runs the C enumerator).
    # コンパイルした C のソースと実行ファイルをハッシュで特定する（F1 は C の列挙器で走る）。
    import hashlib
    with open(os.path.join(CODE, "verify", "enum_interval.c"), "rb") as f:
        src_sha = hashlib.sha256(f.read()).hexdigest()
    assert res["compiler"]["source"] == "code/verify/enum_interval.c"
    assert res["compiler"]["source_sha256"] == src_sha == files["code/verify/enum_interval.c"]
    assert len(res["compiler"]["executable_sha256"]) == 64


def test_source_edited_during_the_run_fails(tmp_path):
    # A module of code/ loaded with VALUE = 1 and then edited to VALUE = 2 before finish(): the record keeps the
    # hash of the loaded version and the run fails, since the JSON would otherwise not describe the code that ran.
    # VALUE = 1 で読み込んだ code/ のモジュールを finish() の前に VALUE = 2 に書き換える: 記録は読み込んだ版のハッシュを保ち、
    # 実行は失敗になる（さもないと JSON が実行したコードを指さない）。
    mod_dir = tmp_path / "code"
    mod_dir.mkdir()
    (mod_dir / "edited_module.py").write_text("VALUE = 1\n")
    body = ("import hashlib, lib.report as R\n"
            f"R.CODE_DIR = {str(mod_dir)!r}\n"
            f"sys.path.insert(0, {str(mod_dir)!r})\n"
            "import edited_module\n"
            f"open({str(mod_dir / 'edited_module.py')!r}, 'w').write('VALUE = 2\\n')\n"
            "print('value', edited_module.VALUE, flush=True)\n"
            "rep.check('one', True); rep.finish()\n")
    proc, res = run_snippet(body, tmp_path / "out")
    assert "value 1" in proc.stdout and proc.returncode == 1
    assert res["passed"] is False and "changed during the run" in res["error"]
    import hashlib
    (h,) = [h for f, h in res["code"]["files"].items() if f.endswith("edited_module.py")]
    assert h == hashlib.sha256(b"VALUE = 1\n").hexdigest()


def test_cached_enumerator_is_not_reused_after_a_compiler_update(tmp_path):
    # A compiler updated at the same path: the executable of the old compiler is not reused, so the recorded version
    # is that of the compiler that built the recorded executable. Separate processes, as in two runs.
    # 同じパスのコンパイラを更新した場合: 古いコンパイラの実行ファイルを再利用しない。記録する版は、記録する実行ファイルを作ったコンパイラのものになる。
    # 2 回の実行と同じく、別のプロセスで試す。
    version, cc = tmp_path / "version", tmp_path / "cc"
    cc.write_text('#!/bin/sh\nif [ "$1" = "--version" ]; then cat "%s"; exit 0; fi\necho x >> "%s"\nexec gcc "$@"\n'
                  % (version, tmp_path / "calls"))
    cc.chmod(0o755)
    src = (f"import sys, json; sys.path.insert(0, {CODE!r})\n"
           "from lib import enumerate as en\n"
           f"exe = en.compile_enumerator({str(tmp_path / 'build')!r})\n"
           "print(json.dumps([exe, en.COMPILED['version']]))\n")
    env = dict(os.environ, CC=str(cc))

    def run():
        out = subprocess.run([sys.executable, "-c", src], env=env, capture_output=True, text=True, check=True)
        return json.loads(out.stdout)
    version.write_text("cc 1.0\n")
    exe1, v1 = run()
    assert run() == [exe1, v1] and (tmp_path / "calls").read_text().count("x") == 1    # same compiler: reused
    version.write_text("cc 2.0\n")
    exe2, v2 = run()
    assert (v1, v2) == ("cc 1.0", "cc 2.0") and exe2 != exe1
    assert (tmp_path / "calls").read_text().count("x") == 2


def test_p3_checkpoint_is_tied_to_the_order_of_s(tmp_path):
    # The order of S decides the representatives, so a checkpoint made with another order is refused before computing.
    # S の順序が代表を決めるので、別の順序で作った途中経過は計算の前に拒否する。
    from produce.p3_norm8_orbits import State, fingerprint
    G = np.eye(2, dtype=np.int64)
    S = np.arange(24, dtype=np.int64).reshape(6, 2, 2)
    old, new = fingerprint(G, S[::-1]), fingerprint(G, S)
    assert old != new
    path = str(tmp_path / "state.npz")
    State(1, old).save(path)
    assert State.load(path, 1, old).inputs == old
    with pytest.raises(SystemExit, match="other inputs"):
        State.load(path, 1, new)


# --- lib.report.load_output_of (v4 -> v6, v8) ------------------------------------------------------------

LOAD = """
import json, os
import numpy as np
from lib import data
from lib.report import load_output_of
s = Report('s', rep.out_dir)
p = os.path.join(rep.out_dir, 'K.npy')
np.save(p, np.arange(5))
s.value('SHA-256 of out/K.npy', data.sha256_file(p))
s.value('SHA-256 of the inputs', {'a': '1'})
s.finish()
js = os.path.join(rep.out_dir, 's.json')
rec = json.load(open(js))
"""


@pytest.mark.parametrize("change, failed", [
    ("", None),
    ("rec['passed'] = False", "records a passed run"),
    ("expected = {'a': '2'}", "same certificate files"),
    ("np.save(p, np.arange(6))", "has the SHA-256 recorded by s"),
    ("f = sorted(rec['code']['files'])[0]; rec['code']['files'][f] = '0' * 64", "made by the same code"),
    ("del rec['code']", "made by the same code"),
])
def test_load_output_of(tmp_path, change, failed):
    body = (LOAD + "expected = {'a': '1'}\n" + change + "\njson.dump(rec, open(js, 'w'))\n"
            "K = load_output_of(rep, 's', 'K.npy', expected)\nrep.check('loaded', list(K) == list(range(5)))\nrep.finish()\n")
    proc, res = run_snippet(body, tmp_path)
    if failed is None:
        assert proc.returncode == 0 and res["passed"] is True, proc.stdout
    else:
        assert proc.returncode == 1 and res["passed"] is False, proc.stdout
        assert failed in res["checks"][-1]["check"] and res["checks"][-1]["ok"] is False


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
