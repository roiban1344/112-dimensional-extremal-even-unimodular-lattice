"""Shared fixtures of the smoke tests (pytest). See code/README.md, section "Tests".
試験（pytest）の共通の fixture。code/README.ja.md の「試験」の節を参照。

Markers / マーカー:
  slow  takes more than a few seconds (a whole verification script as a subprocess)
        数秒より長くかかる（検算スクリプト全体を子プロセスで走らせる）
  data  needs the large certificate files certificates/*.npz (bash code/verify/fetch.sh);
        skipped when they are missing
        大きな検証用データ certificates/*.npz（bash code/verify/fetch.sh）が必要。無ければ飛ばす

Run from the repository root / リポジトリの根から実行する:
  python -m pytest code/tests                      everything available / 実行できるものすべて
  python -m pytest code/tests -m "not slow"        a few seconds / 数秒
  python -m pytest code/tests -m data              with the certificate files (about 10 min) / 検証用データを使う（約 10 分）
"""
import json
import os
import subprocess
import sys

import pytest

TESTS = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.dirname(TESTS)
REPO = os.path.dirname(CODE)
VERIFY = os.path.join(CODE, "verify")
CERTIFICATES = os.path.join(REPO, "certificates")
DATA = os.path.join(REPO, "data")

sys.path.insert(0, CODE)

# The certificate files the `data` tests use. / `data` の試験が使う検証用データ。
DATA_FILES = ("min_reps.npz", "odd_bounding.npz", "even_bounding.npz", "norm8_reps.npz", "centralizer.npz")


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: takes more than a few seconds / 数秒より長くかかる")
    config.addinivalue_line("markers", "data: needs certificates/*.npz (fetch.sh) / certificates/*.npz が必要")


def pytest_collection_modifyitems(config, items):
    missing = [f for f in DATA_FILES if not os.path.exists(os.path.join(CERTIFICATES, f))]
    if not missing:
        return
    skip = pytest.mark.skip(reason=f"certificates/{missing[0]} is missing: run bash code/verify/fetch.sh / 先に fetch.sh を実行する")
    for item in items:
        if "data" in item.keywords:
            item.add_marker(skip)


def run_python(args, **kw):
    """Run `python -I <args>` (as the shell scripts do) from the repository root; returns the CompletedProcess.
    リポジトリの根から `python -I <args>` を実行する（シェルスクリプトと同じ）。CompletedProcess を返す。"""
    return subprocess.run([sys.executable, "-I"] + list(args), cwd=REPO, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, **kw)


def run_step(script, out_dir, *args, flags=()):
    """Run code/verify/<script> with --out out_dir; returns (exit code, JSON of the step or None, output).
    code/verify/<script> を --out out_dir 付きで実行する。(終了コード, その段の JSON または None, 出力) を返す。"""
    proc = subprocess.run([sys.executable, "-I", *flags, os.path.join(VERIFY, script), "--out", str(out_dir), *args],
                          cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    results = [f for f in os.listdir(out_dir) if f.endswith(".json")] if os.path.isdir(out_dir) else []
    res = None
    if len(results) == 1:
        with open(os.path.join(out_dir, results[0])) as f:
            res = json.load(f)
    return proc.returncode, res, proc.stdout


@pytest.fixture(scope="session")
def enum_exe(tmp_path_factory):
    """verify/enum_interval.c compiled once per session. / セッションに 1 回コンパイルした verify/enum_interval.c。"""
    from lib import enumerate as en
    return en.compile_enumerator(str(tmp_path_factory.mktemp("build")))
