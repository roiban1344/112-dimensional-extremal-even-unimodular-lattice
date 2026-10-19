"""Tests on the large certificate files (marker `data`; skipped unless certificates/*.npz are present).
About 9 minutes and 3 GB of memory: four runs of about 2 minutes each (and one refused at the hash check),
mostly spent expanding the 7,795,200 minimal vectors.
大きな検証用データを使う試験（マーカー `data`。certificates/*.npz が無ければ飛ばす）。約 9 分、メモリ 3 GB:
約 2 分の実行を 4 回行う（ほかにハッシュの照合で拒否される 1 回）。時間の大部分は 7,795,200 本の最小ベクトルの展開にかかる。

  * v5 passes on the published data, and FAILS in (c) on a copy in which one row of odd_bounding.npz is
    replaced by w0 + 2u for a minimal vector u: the new row keeps (a) the parity and (b) an allowed norm,
    but has |<w0 + 2u, u>| = 7 > 6.
    v5 は公開したデータで合格し、odd_bounding.npz の 1 行を最小ベクトル u による w0 + 2u に置き換えた写しでは (c) で不合格になる。
    新しい行は (a) の偶奇と (b) の許されたノルムを保つが、|<w0 + 2u, u>| = 7 > 6 となる。
    The copy is checked against its own SHA256SUMS only with --hashes; without it, v5 refuses the file.
    写しは --hashes を付けたときだけそれ自身の SHA256SUMS と照合される。付けなければ v5 はそのファイルを拒否する。
  * v7 --limit 64 passes, and FAILS when a checkpoint made for other inputs is in place.
    v7 --limit 64 は合格し、別の入力のための途中経過が置かれていると不合格になる。
"""
import hashlib
import json
import os
import shutil

import numpy as np
import pytest

from conftest import CERTIFICATES, run_step
from lib import certs, data

pytestmark = [pytest.mark.data, pytest.mark.slow]


def test_v5_passes(tmp_path):
    code, res, out = run_step("v5_odd_bounding.py", tmp_path)
    assert code == 0, out[-2000:]
    assert res["passed"] is True


def mutated_odd_bounding():
    """odd_bounding.npz with one row w0 replaced by w0 + 2u, u one of the 656 representatives r_j (norm 6),
    chosen so that the new norm is 14 or 18 and |<w0 + 2u, u>| > 6. Returns (array, row, new norm).
    1 行 w0 を w0 + 2u に置き換えた odd_bounding.npz（u は 656 個の代表 r_j の 1 つ、ノルム 6）。新しいノルムが 14 か 18 で、
    |<w0 + 2u, u>| > 6 となるように選ぶ。(配列, 行, 新しいノルム) を返す。"""
    G = data.gram()
    R = certs.load("min_reps.npz", "reps").astype(np.int64)
    W = certs.load("odd_bounding.npz", "w0").astype(np.int64)
    ip = W @ G @ R.T
    norms = np.einsum("ij,jk,ik->i", W, G, W)
    for i in range(len(W)):
        for j in range(len(R)):
            for sgn in (1, -1):
                p = sgn * int(ip[i, j])
                # <w0 + 2u, w0 + 2u> = N + 4p + 24 and <w0 + 2u, u> = p + 12. / ノルムと内積。
                if norms[i] + 4 * p + 24 in (14, 18) and abs(p + 12) > 6:
                    W2 = W.copy()
                    W2[i] += 2 * sgn * R[j]
                    return W2.astype(np.int16), i, int(norms[i] + 4 * p + 24)
    raise AssertionError("no mutation found")


@pytest.fixture(scope="module")
def mutated_dir(tmp_path_factory):
    """A certificate directory with the mutated odd_bounding.npz and a SHA256SUMS that matches it.
    改変した odd_bounding.npz と、それに合わせた SHA256SUMS を置いたディレクトリ。"""
    W2, row, new_norm = mutated_odd_bounding()
    cdir = tmp_path_factory.mktemp("mutated") / "certificates"
    cdir.mkdir()
    os.symlink(os.path.realpath(os.path.join(CERTIFICATES, "min_reps.npz")), cdir / "min_reps.npz")
    np.savez_compressed(cdir / "odd_bounding.npz", w0=W2)
    with open(cdir / "SHA256SUMS", "w") as f:
        for name in ("min_reps.npz", "odd_bounding.npz"):
            f.write(hashlib.sha256((cdir / name).read_bytes()).hexdigest() + "  " + name + "\n")
    return cdir, row, new_norm


def test_v5_refuses_data_not_matching_the_repository_hashes(tmp_path, mutated_dir):
    # Without --hashes, the mutated file is checked against certificates/SHA256SUMS and refused.
    # --hashes が無ければ、改変したファイルは certificates/SHA256SUMS と照合され、拒否される。
    cdir, _, _ = mutated_dir
    code, res, out = run_step("v5_odd_bounding.py", tmp_path, "--certificates", str(cdir))
    assert code == 1, out[-2000:]
    assert res["passed"] is False
    assert "odd_bounding.npz: SHA-256" in res["error"] and "certificates/SHA256SUMS" in res["error"]


def test_v5_fails_on_a_mutated_row(tmp_path, mutated_dir):
    cdir, row, new_norm = mutated_dir
    code, res, out = run_step("v5_odd_bounding.py", tmp_path / "out", "--certificates", str(cdir),
                              "--hashes", str(cdir / "SHA256SUMS"))
    assert code == 1, out[-2000:]
    assert res["passed"] is False and res["certificate_hashes"] == str(cdir / "SHA256SUMS")
    labels = {c["check"]: c["ok"] for c in res["checks"]}
    assert labels["(a) w0 - r_j tau has even coordinates"] is True
    assert labels["(b) every <w0, w0> is 14 or 18"] is True
    assert labels["(c) max |<w0, u>| <= 6 over all minimal vectors u, for all 656"] is False
    assert res["values"]["Table 7: (norm, max |<w0, u>|) -> count"].get(f"norm {new_norm}, max 7", 0) >= 1, row


def test_v7_limit_passes(tmp_path):
    code, res, out = run_step("v7_even_bounding.py", tmp_path, "--limit", "64")
    assert code == 0, out[-2000:]
    assert res["passed"] is True
    assert not os.path.exists(tmp_path / "v7_even_bounding_first64.state.npz")


def test_v7_refuses_a_checkpoint_of_other_inputs(tmp_path):
    # A checkpoint whose fingerprint records another hash of even_bounding rows (as if made for other data).
    # even_bounding の行の別のハッシュを記録した指紋をもつ途中経過（別のデータのために作られたかのような）。
    fp = {"rows": [64, 56], "dtype": "int16", "rows_sha256": "0" * 64, "files": {}, "n": 64, "limit": 64}
    state = tmp_path / "v7_even_bounding_first64.state.npz"
    certs.save_npz(str(state), mx=np.zeros(64, dtype=np.int64), done=np.int64(64), seconds=np.float64(0),
                   fingerprint=np.str_(json.dumps(fp, sort_keys=True)))
    code, res, out = run_step("v7_even_bounding.py", tmp_path, "--limit", "64")
    assert code == 1, out[-2000:]
    assert res["passed"] is False
    assert res["checks"][-1]["check"].startswith("the checkpoint v7_even_bounding_first64.state.npz belongs to these inputs")
    assert "differs: rows_sha256" in out
    assert state.exists(), "the foreign checkpoint is kept"
