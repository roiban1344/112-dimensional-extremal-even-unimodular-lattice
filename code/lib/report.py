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

Format of out/<step>.json (FORMAT = 2; the keys are described in code/README.md, "The JSON records"):
out/<段>.json の形式（FORMAT = 2。鍵の説明は code/README.ja.md の「JSON の記録」）:
  format, step, passed, error, checks [{check, ok}], values {label: value}, seconds, finished, arguments,
  code {git, files {path: SHA-256 when loaded}}, inputs {path: SHA-256}, python, numpy, blas, platform,
  compiler (only if the enumerator was compiled; with the SHA-256 of its source and executable),
  certificate_hashes (only with --hashes). A source file of code/ edited during the run makes the run fail.
"""
import atexit
import hashlib
import importlib.machinery
import json
import os
import platform
import subprocess
import sys
import time

try:  # numpy is optional here (v2_theta.py runs without it) / ここでは numpy は任意（v2_theta.py は numpy なしで動く）
    import numpy as np
except ImportError:
    np = None

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE_DIR = os.path.join(ROOT, "code")
DEFAULT_OUT = os.path.join(ROOT, "out")
FORMAT = 2          # 1: until 2026-10-25 (without format, arguments, code, inputs, blas, compiler)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# SHA-256 of every source file under code/ that this process has loaded, taken when the module is loaded (or, for
# modules loaded before this file, when this file is imported). finish() records these values, which describe the
# code that ran, and fails the run if a file has changed since.
# このプロセスが読み込んだ code/ 以下のソースの SHA-256。モジュールを読み込む時点で取る（この file より先に読み込まれた
# モジュールは、この file を import する時点で取る）。finish() はこの値を記録し（実行したコードを指す）、その後に
# ファイルが変わっていれば実行を失敗とする。
_CODE_HASHES = {}


def _note_source(path):
    path = os.path.abspath(path)
    if path not in _CODE_HASHES and path.startswith(CODE_DIR + os.sep) and os.path.isfile(path):
        _CODE_HASHES[path] = _sha256(path)


def _note_loaded_modules():
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None)
        if f and f.endswith(".py"):
            _note_source(f)


_exec_module = importlib.machinery.SourceFileLoader.exec_module


def _exec_module_noting_source(loader, module):
    # Every later import of a source file passes here: hash the file as it is loaded.
    # これ以後のソースの import はすべてここを通る。読み込む時点のファイルのハッシュを取る。
    _note_source(loader.path)
    return _exec_module(loader, module)


importlib.machinery.SourceFileLoader.exec_module = _exec_module_noting_source
_note_loaded_modules()


def code_files():
    """{path relative to the repository root: SHA-256 when loaded} of the running script and of every module under
    code/ that it has loaded (lib/ and, for the supplementary computations, produce/ and supplementary/).
    実行中のスクリプトと、それが読み込んだ code/ 以下のすべてのモジュールの {リポジトリの根からのパス: 読み込んだ時点の SHA-256}。"""
    _note_loaded_modules()
    return {os.path.relpath(f, ROOT): h for f, h in sorted(_CODE_HASHES.items())}


def changed_code_files():
    """The loaded source files whose content differs now from when they were loaded (edited during the run).
    読み込んだ時点と今とで内容が違うソース（実行中に書き換えられたもの）。"""
    return sorted(os.path.relpath(f, ROOT) for f, h in _CODE_HASHES.items()
                  if not os.path.isfile(f) or _sha256(f) != h)


def git_version():
    """`git describe --always --dirty` of this repository, or None (no git, no .git as in the container
    images, or the code is a copy inside another repository).
    このリポジトリの `git describe --always --dirty`。取れなければ None（git が無い、コンテナのイメージのように .git が無い、
    別のリポジトリの中の写しである場合）。"""
    try:
        top = subprocess.run(["git", "-C", ROOT, "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=20)
        if top.returncode != 0 or os.path.realpath(top.stdout.strip()) != os.path.realpath(ROOT):
            return None
        d = subprocess.run(["git", "-C", ROOT, "describe", "--always", "--dirty"], capture_output=True, text=True, timeout=20)
        return (d.stdout.strip() or None) if d.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def blas_info():
    """Name and version of the BLAS that numpy was built against (numpy.show_config), or None.
    numpy をビルドしたときの BLAS の名前と版（numpy.show_config）。取れなければ None。"""
    try:
        b = np.show_config(mode="dicts")["Build Dependencies"]["blas"]
        return {k: b.get(k) for k in ("name", "version", "openblas configuration") if k in b}
    except Exception:  # noqa: BLE001  (numpy without numpy.show_config(mode=...), or another layout)
        return None


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
    # The code that produced the file (the script and the modules it loaded) must be the code of this checkout.
    # ファイルを作ったコード（スクリプトと、それが読み込んだモジュール）は、この作業ツリーのコードと同じでなければならない。
    recorded = (res.get("code") or {}).get("files") or {}
    current = {f: (_sha256(os.path.join(ROOT, f)) if os.path.isfile(os.path.join(ROOT, f)) else None) for f in recorded}
    for f in sorted(recorded):
        if current[f] != recorded[f]:
            rep.log(f"  {f} has changed since {step} was run / {step} の実行後に変わった")
    rep.check(f"out/{step}.json was made by the same code ({len(recorded)} files, SHA-256)",
              len(recorded) > 0 and current == recorded)
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
        self._exiting = False
        self.error = None
        # Remove a result of an earlier run, so that a crash cannot leave it in place.
        # 前回の実行の結果を消す。異常終了したときに古い結果が残らないようにする。
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass
        if not __debug__:
            # Refuse a run under -O (see lib/__init__.py), after removing the old result, and record why.
            # -O の下での実行を拒否する（lib/__init__.py を参照）。古い結果を消したうえで、理由を記録する。
            from . import OPTIMIZED_MESSAGE
            self.failed = True
            self.error = "refused: python -O / PYTHONOPTIMIZE"
            self.finish()
            print(OPTIMIZED_MESSAGE, file=sys.stderr)
            sys.exit(1)
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
        self._exiting = True
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
        data = sys.modules.get(__package__ + ".data")
        files = code_files()
        enum = sys.modules.get(__package__ + ".enumerate")
        if enum is not None and enum.COMPILED:
            files[enum.COMPILED["source"]] = enum.COMPILED["source_sha256"]
        # A source file edited during the run: the record would not describe the code that ran, so the run fails.
        # 実行中に書き換えられたソース: 記録が実行したコードを指さなくなるので、実行を失敗とする。
        changed = changed_code_files()
        if changed:
            self.failed = True
            msg = "source files changed during the run: " + ", ".join(changed)
            self.error = msg if self.error is None else f"{self.error}; {msg}"
        result = {
            "format": FORMAT,
            "step": self.step,
            "passed": not self.failed,
            "error": self.error,
            "checks": self.checks,
            "values": self.values,
            "seconds": round(time.time() - self.t0, 1),
            "finished": time.strftime("%Y-%m-%d %H:%M:%S %z"),
            "arguments": sys.argv[1:],
            "code": {"git": git_version(), "files": files},
            "inputs": dict(sorted(data.CHECKED_INPUTS.items())) if data is not None else {},
            "python": platform.python_version(),
            "numpy": np.__version__ if np is not None else None,
            "blas": blas_info() if np is not None else None,
            "platform": platform.platform(),
        }
        # The C compiler and the compiled source and executable of the enumerator (v1 and the users of lib.enumerate).
        # 列挙器の C コンパイラと、コンパイルしたソース・実行ファイル。
        if enum is not None and enum.COMPILED:
            result["compiler"] = enum.COMPILED
        # Certificate files checked against a list of hashes other than certificates/SHA256SUMS (--hashes).
        # certificates/SHA256SUMS 以外のハッシュの一覧（--hashes）と照合した場合はそれを記録する。
        certs = sys.modules.get(__package__ + ".certs")
        if certs is not None and certs.HASHES_FILE != certs.DEFAULT_HASHES:
            result["certificate_hashes"] = certs.HASHES_FILE
        path = self.path
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(result, f, indent=1, default=_plain)
            f.write("\n")
        os.replace(tmp, path)
        self.log(("PASSED" if not self.failed else "FAILED") + f": {self.step} -> {path}")
        if changed and not self._exiting:
            # The exit code is the primary verdict, so an edited source fails it too. / 合否の正本は終了コードなので、書き換えも失敗にする。
            sys.exit(1)
