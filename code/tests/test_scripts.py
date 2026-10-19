"""The verification scripts that need no download (v0, v2, v1 --controls-only), the hash chain of data/,
a negative control, and the syntax of the shell scripts.
取得を要しない検算スクリプト（v0、v2、v1 --controls-only）、data/ のハッシュの連鎖、陰性対照、シェルスクリプトの構文。"""
import glob
import os
import shutil
import subprocess

import pytest

from conftest import CERTIFICATES, DATA, REPO, run_step
from lib import certs, data


def read_sums(path):
    out = {}
    with open(path) as f:
        for line in f:
            if line.strip():
                h, name = line.split()
                out[name.lstrip("*")] = h
    return out


def test_data_hashes_pinned_in_code_match_sha256sums():
    # lib/data.py pins the hashes of data/; data/SHA256SUMS lists the same; the files have them.
    # lib/data.py が data/ のハッシュを固定し、data/SHA256SUMS も同じものを挙げ、ファイルはそのハッシュをもつ。
    assert read_sums(os.path.join(DATA, "SHA256SUMS")) == data.SHA256
    for name, h in data.SHA256.items():
        assert data.sha256_file(os.path.join(DATA, name)) == h


def test_certificate_text_files_match_sha256sums():
    # The text files are in git; the .npz files are downloaded (checked by the `data` tests and fetch.sh).
    # テキストのファイルは git にある。.npz は取得するもの（`data` の試験と fetch.sh が確かめる）。
    sums = certs.expected_hashes(os.path.join(CERTIFICATES, "SHA256SUMS"))
    texts = [n for n in sums if not n.endswith(".npz")]
    assert texts
    for name in texts:
        assert data.sha256_file(os.path.join(CERTIFICATES, name)) == sums[name], name


@pytest.mark.slow
def test_v0_inputs(tmp_path):
    code, res, out = run_step("v0_inputs.py", tmp_path)
    assert code == 0, out
    assert res["step"] == "v0_inputs" and res["passed"] is True


def test_v2_theta(tmp_path):
    code, res, out = run_step("v2_theta.py", tmp_path)
    assert code == 0, out
    assert res["passed"] is True


@pytest.mark.slow
def test_v1_controls(tmp_path):
    code, res, out = run_step("v1_min_L.py", tmp_path, "--controls-only")
    assert code == 0, out
    assert res["step"] == "v1_min_L_controls" and res["passed"] is True


def test_negative_control_tau_changed_by_one_byte(tmp_path):
    # A copy of data/ in which one digit of tau.txt is changed: v0 must stop with exit code 1.
    # tau.txt の 1 桁を変えた data/ の写し: v0 は終了コード 1 で止まらなければならない。
    d = tmp_path / "data"
    shutil.copytree(DATA, d)
    raw = bytearray((d / "tau.txt").read_bytes())
    lines = raw.split(b"\n")
    k = next(i for i, line in enumerate(lines) if line and not line.startswith(b"#"))
    j = next(i for i, ch in enumerate(lines[k]) if chr(ch).isdigit() and chr(ch) != "0")
    lines[k][j] = ord("0") if lines[k][j] != ord("0") else ord("1")
    (d / "tau.txt").write_bytes(b"\n".join(lines))
    assert len((d / "tau.txt").read_bytes()) == len(raw)
    out_dir = tmp_path / "out"
    code, res, out = run_step("v0_inputs.py", out_dir, "--data", str(d))
    assert code == 1, out
    assert res["passed"] is False
    last = res["checks"][-1]
    assert last["check"].startswith("data/tau.txt has the published SHA-256") and last["ok"] is False, res


# Limit discovery to source directories so scratch files and nested worktrees are not tested.
# 作業用ファイルや内部の別 worktree を拾わないよう、ソースのディレクトリだけを探索する。
SHELL_SCRIPTS = sorted(
    p
    for directory in ("code", "lean")
    for p in glob.glob(os.path.join(REPO, directory, "**", "*.sh"), recursive=True)
)


@pytest.mark.skipif(shutil.which("bash") is None, reason="no bash")
@pytest.mark.parametrize("script", SHELL_SCRIPTS, ids=lambda p: os.path.relpath(p, REPO))
def test_shell_syntax(script):
    proc = subprocess.run(["bash", "-n", script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert proc.returncode == 0, proc.stdout
