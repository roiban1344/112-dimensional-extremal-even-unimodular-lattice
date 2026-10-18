"""Uniform reporting for the scripts: every check is printed as [ok]/[FAIL] and collected
into a JSON file out/<step>.json together with the software versions and the run time.
スクリプト共通の報告: 各検査を [ok]/[FAIL] で表示し、ソフトウェアの版と実行時間とともに out/<step>.json にまとめる。

The JSON file never shows a stale result: an existing out/<step>.json is deleted when the
Report is created, and if the script ends without calling finish() (an uncaught exception such
as a hash mismatch or a failed guard, KeyboardInterrupt, sys.exit), the file is written at exit
with "passed": false and the error. The exit code is not changed (1 for a failed check or an
uncaught exception). The exit code remains the primary verdict; the JSON is the record.
JSON ファイルが古い結果を示すことはない: Report を作る時点で既存の out/<step>.json を消す。スクリプトが finish() を呼ばずに
終わったとき（ハッシュの不一致や保証の検査の失敗などの捕まえられない例外、KeyboardInterrupt、sys.exit）は、終了時に
"passed": false とエラーを書く。終了コードは変えない（検査の失敗と捕まえられない例外では 1）。合否の正本は終了コードで、
JSON はその記録である。
"""
import atexit
import hashlib
import json
import os
import platform
import sys
import time

try:  # numpy is optional here (v2_theta.py runs without it) / ここでは numpy は任意（v2_theta.py は numpy なしで動く）
    import numpy as np
except ImportError:
    np = None

DEFAULT_OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "out")


def _plain(o):
    """JSON fallback for numpy/Sage numbers: integers as int, everything else as str.
    numpy・Sage の数のための JSON の代替: 整数は int、それ以外は文字列。"""
    try:
        if int(o) == o:
            return int(o)
    except (TypeError, ValueError):
        pass
    return str(o)


def load_result(step, out_dir=None):
    """The JSON written by an earlier step (dict), or None if there is none.
    前の段が書いた JSON（dict）。無ければ None。"""
    path = os.path.join(out_dir or DEFAULT_OUT, step + ".json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def load_output_of(rep, step, name, input_hashes):
    """Load out/<name> (.npy) written by an earlier step, after checking with rep.check that the JSON of
    that step says "passed", records the same SHA-256 for the file ("SHA-256 of out/<name>") and the
    same SHA-256 of its inputs ("SHA-256 of the inputs" == input_hashes).
    前の段が書いた out/<name>（.npy）を読む。その前に rep.check で、その段の JSON が "passed" であること、ファイルの SHA-256
    （"SHA-256 of out/<name>"）と入力の SHA-256（"SHA-256 of the inputs" == input_hashes）が一致することを確かめる。"""
    path = os.path.join(rep.out_dir, name)
    res = load_result(step, rep.out_dir)
    if res is None or not os.path.exists(path):
        rep.log(f"out/{step}.json or out/{name} is missing: run {step} first / 先に {step} を実行する")
    rep.check(f"out/{step}.json records a passed run", res is not None and res.get("passed") is True)
    values = res["values"]
    rep.check(f"out/{step}.json was made from the same certificate files", values.get("SHA-256 of the inputs") == input_hashes)
    h = hashlib.sha256()
    if os.path.exists(path):
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(1 << 20), b""):
                h.update(block)
    rep.check(f"out/{name} has the SHA-256 recorded by {step}",
              os.path.exists(path) and values.get(f"SHA-256 of out/{name}") == h.hexdigest())
    return np.load(path, allow_pickle=False)


class Report:
    def __init__(self, step, out_dir=None):
        self.step = step
        self.out_dir = out_dir or DEFAULT_OUT
        self.t0 = time.time()
        self.checks = []
        self.values = {}
        self.failed = False
        self.finished = False
        self.error = None
        # Remove a result of an earlier run, so that a crash cannot leave it in place.
        # 前回の実行の結果を消す。異常終了したときに古い結果が残らないようにする。
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass
        self._previous_hook = sys.excepthook
        sys.excepthook = self._excepthook
        atexit.register(self._at_exit)

    @property
    def path(self):
        return os.path.join(self.out_dir, self.step + ".json")

    def _excepthook(self, typ, value, tb):
        # Remember the uncaught exception for the JSON, then print the traceback as usual.
        # 捕まえられなかった例外を JSON のために覚えてから、通常どおり traceback を表示する。
        self.error = f"{typ.__name__}: {value}"
        self._previous_hook(typ, value, tb)

    def _at_exit(self):
        if not self.finished:
            self.failed = True
            if self.error is None:
                self.error = "exited without calling finish()"
            self.finish()

    def log(self, *args):
        print(f"[{time.time() - self.t0:8.1f} s]", *args, flush=True)

    def check(self, label, ok, stop=True):
        """Record a yes/no check; by default stop at the first failure.
        はい・いいえの検査を記録する。既定では最初の失敗で止める。"""
        ok = bool(ok)
        self.checks.append({"check": label, "ok": ok})
        self.log("[ok]  " if ok else "[FAIL]", label)
        if not ok:
            self.failed = True
            if stop:
                self.finish()
                sys.exit(1)

    def value(self, key, v):
        """Record a computed value (number, list, ...). / 計算した値を記録する。"""
        self.values[key] = v
        self.log(f"{key} = {v}")

    def finish(self):
        self.finished = True
        os.makedirs(self.out_dir, exist_ok=True)
        result = {
            "step": self.step,
            "passed": not self.failed,
            "error": self.error,
            "checks": self.checks,
            "values": self.values,
            "seconds": round(time.time() - self.t0, 1),
            "finished": time.strftime("%Y-%m-%d %H:%M:%S %z"),
            "python": platform.python_version(),
            "numpy": np.__version__ if np is not None else None,
            "platform": platform.platform(),
        }
        path = self.path
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(result, f, indent=1, default=_plain)
            f.write("\n")
        os.replace(tmp, path)
        self.log(("PASSED" if not self.failed else "FAILED") + f": {self.step} -> {path}")
