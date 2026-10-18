"""S22. Route T, checking the certificates of searches (2) and (3) in integer arithmetic (supplement §S4.1;
Table D2 [C21]). numpy only. Not used in the proof of Theorem A.
S22. 経路 T、探索 (2)・(3) の certificate を整数演算で検算する（補遺 §S4.1、表 D2 の [C21]）。numpy だけで動く。定理 A の証明には使わない。

For every certificate w0 of certificates/route_t_search3.npz (3,936 rows) and of
certificates/route_t_search2.npz (763,992 rows; only the rows with done = True), in the order of
common.py:
certificates/route_t_search3.npz（3,936 行）と certificates/route_t_search2.npz（763,992 行。done = True の行だけ）の各 certificate w0
について（順序は common.py）:
  (a) w0 minus the starting vector of its class has even coordinates (w0 lies in the class);
      w0 から類の始点を引いた座標がすべて偶数（w0 は類に入る）;
  (b) <w0, w0> is allowed by the lemma for the target (12, 16, 20 for norm 8; 14, 18 for norms 6, 10);
      <w0, w0> が目標に対して補題の許す値（ノルム 8 には 12, 16, 20、ノルム 6・10 には 14, 18）;
  (c) |<w0, y>| <= 6 for every minimal vector y of L (all 15,590,400, expanded from min_reps.npz).
      L のすべての最小ベクトル y（min_reps.npz から展開した 15,590,400 本）について |<w0, y>| ≤ 6。
That the expansion gives all minimal vectors is F2 (verify/v3). (c) uses the same exact routine as
verify/v7 (float32 with the exactness bound checked), with the same checkpoint
(out/<step>.<s3|s2>.state.npz): it records the SHA-256 of the certificate rows checked, of the inputs
and of the code computing (c); a checkpoint made for other data FAILS the run (delete it to recompute),
and it is deleted when (c) is complete.
展開ですべての最小ベクトルが得られることは F2（verify/v3）。(c) は verify/v7 と同じ厳密な手続き（float32、厳密さの上界を確かめる）で、
途中経過（out/<段>.<s3|s2>.state.npz）の扱いも同じ: 検査する certificate の行、入力、(c) を計算するコードの SHA-256 を記録する。
別のデータのための途中経過があれば不合格とし（再計算するには消す）、(c) が終わると消す。

The distributed file of search (2) is complete from Release certificates-v2 on (all 763,992 rows;
certificates-v1 had 610,664). For a partial file the number of certified classes is reported, and
the check covers exactly those.
探索 (2) の配布ファイルは Release certificates-v2 から完全（763,992 行すべて。certificates-v1 では 610,664 行）。途中のファイルでは
certificate のある類の数を報告し、検算はちょうどそれらを対象にする。

Run time: search (3) about 2 minutes; search (2) about 7 CPU hours (estimate from a single-thread trial; batch A: 4.7 h elapsed with 2 threads on a shared machine) (resumable, --threads).
実行時間: 探索 (3) 約 2 分。探索 (2) 約 7 CPU 時間（単一スレッド試験からの見積もり。分割 A の実測: 共用機で 2 スレッド、経過 4.7 時間）（再開可能、--threads）。
Run / 実行:  python3 code/supplementary/route_t/check.py [search3|search2|both] [--threads T] [--limit N]
"""
import os
import sys

if any(arg == "--threads" or arg.startswith("--threads=") for arg in sys.argv):
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"

import argparse  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from common import ALLOWED, N_SEARCH2, N_SEARCH3, kept_units, search2_starts, search3_classes  # noqa: E402
from lib import certs, data, exact, group, shells  # noqa: E402
from lib.report import Report  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="S22: check the route T certificates")
    ap.add_argument("which", nargs="?", choices=("search3", "search2", "both"), default="both")
    ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--limit", type=int, default=None, help="check only the first N certified classes of search (2)")
    ap.add_argument("--data", default=None)
    ap.add_argument("--certificates", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rep = Report("s22_route_t_check_" + a.which + (f"_first{a.limit}" if a.limit else ""), a.out)
    G = data.gram(a.data)
    t = data.tau(a.data)
    S = group.sl2_29_mod_sign(data.generators(a.data))
    R6 = certs.load("min_reps.npz", "reps", a.certificates).astype(np.int64)
    U = certs.load("centralizer.npz", "units", a.certificates).astype(np.int64)
    keep = kept_units(U, t)
    rep.value("kept units", keep)
    mv = shells.MinimalVectors(G, R6, S)
    rep.log(f"expanded {2 * mv.count} minimal vectors")
    # Files that determine the minimal vectors, for the checkpoint. / 最小ベクトルを決めるファイル（途中経過のため）。
    inputs = [certs.path_checked("min_reps.npz", a.certificates)]
    inputs += [os.path.join(a.data or data.DEFAULT_DIR, f) for f in ("L56_gram.txt", "sl2_29_generators.txt")]

    jobs = []
    if a.which in ("search3", "both"):
        W3 = certs.load("route_t_search3.npz", "w0", a.certificates).astype(np.int64)
        st3, tg3 = search3_classes(R6, U, t)
        rep.check("search (3): 3,936 certificates", W3.shape == (N_SEARCH3, 56))
        jobs.append(("search (3)", W3, st3, tg3))
    if a.which in ("search2", "both"):
        W2 = certs.load("route_t_search2.npz", "w0", a.certificates).astype(np.int64)
        done = certs.load("route_t_search2.npz", "done", a.certificates).astype(bool)
        rep.check("search (2): 763,992 rows", W2.shape == (N_SEARCH2, 56) and done.shape == (N_SEARCH2,))
        idx = np.flatnonzero(done)
        rep.value("search (2): classes with a certificate in the distributed file (of 763,992)", len(idx))
        if a.limit:
            idx = idx[:a.limit]
        X = certs.load("norm8_reps.npz", "reps", a.certificates).astype(np.int64)
        jobs.append(("search (2)", W2[idx], search2_starts(X, U, t, keep, idx), ["8"] * len(idx)))

    for label, W, starts, targets in jobs:
        ok_a = bool(((W - starts) % 2 == 0).all())
        rep.check(f"{label} (a): every w0 lies in its class", ok_a)
        norms = exact.norms(W, G)
        ok_b = all(int(nv) in ALLOWED[tg] for nv, tg in zip(norms, targets))
        rep.check(f"{label} (b): every norm is allowed by the lemma", ok_b)
        tag = "s3" if label == "search (3)" else "s2"
        fp = shells.fingerprint(W, inputs + shells.CODE_FILES, {"n": len(W), "which": label, "limit": a.limit})
        mx, _, resumed = shells.max_abs_inner_checkpointed(mv, W, a.threads, a.chunk,
                                                           os.path.join(rep.out_dir, f"{rep.step}.{tag}.state.npz"), fp, rep)
        rep.value(f"{label} (c): rows taken over from the checkpoint", resumed)
        table = {}
        for nv, m, tg in zip(norms.tolist(), mx.tolist(), targets):
            k = f"target {tg}: norm {nv}, max {m}"
            table[k] = table.get(k, 0) + 1
        rep.value(f"{label}: (target, norm, max |<w0, y>|) -> count", table)
        rep.check(f"{label} (c): max |<w0, y>| <= 6 for all {len(W)} certificates", bool((mx <= 6).all() and (mx >= 0).all()))
    rep.finish()


if __name__ == "__main__":
    main()
