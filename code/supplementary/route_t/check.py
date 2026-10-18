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
verify/v7 (float32 with the exactness bound asserted).
展開ですべての最小ベクトルが得られることは F2（verify/v3）。(c) は verify/v7 と同じ厳密な手続き（float32、厳密さの上界を確かめる）。

Search (2) may be incomplete in the distributed file (the computation was still running when the
files were published); the number of certified classes is reported, and the check covers exactly
those. The file will be replaced when the computation is complete.
探索 (2) は配布ファイルで途中のことがある（公開の時点で計算が続いていた）。certificate のある類の数を報告し、検算はちょうどそれらを
対象にする。計算が終わったらファイルを差し替える。

Run time: search (3) about 2 minutes; search (2) about 12 CPU hours when complete (resumable, --threads).
実行時間: 探索 (3) 約 2 分。探索 (2) は全部そろうと約 12 CPU 時間（再開可能、--threads）。
Run / 実行:  python3 code/supplementary/route_t/check.py [search3|search2|both] [--threads T] [--limit N]
"""
import os
import sys

if "--threads" in sys.argv:
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"

import argparse  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from common import ALLOWED, N_SEARCH2, N_SEARCH3, kept_units, search2_starts, search3_classes  # noqa: E402
from lib import certs, data, exact, group, shells  # noqa: E402
from lib.report import Report  # noqa: E402


def check_c(mv, W, threads, chunk, state, rep):
    """max |<w0, y>| per row, with a checkpoint. / 行ごとの max |<w0, y>|。途中経過を保存する。"""
    n = len(W)
    if os.path.exists(state):
        with np.load(state, allow_pickle=False) as z:
            mx, done = z["mx"].copy(), int(z["done"])
        assert len(mx) == n
        rep.log(f"resuming at {done} / {n}")
    else:
        mx, done = np.full(n, -1, dtype=np.int8), 0
    last = time.time()
    while done < n:
        e = min(n, done + chunk)
        mx[done:e] = mv.max_abs_inner(W[done:e], threads=threads)
        done = e
        if time.time() - last > 300 or done == n:
            certs.save_npz(state, mx=mx, done=np.int64(done))
            last = time.time()
            rep.log(f"(c) {done} / {n}, max so far {int(mx[:done].max())}")
    return mx


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
        mx = check_c(mv, W, a.threads, a.chunk, os.path.join(rep.out_dir, f"{rep.step}.{tag}.state.npz"), rep)
        table = {}
        for nv, m, tg in zip(norms.tolist(), mx.tolist(), targets):
            k = f"target {tg}: norm {nv}, max {m}"
            table[k] = table.get(k, 0) + 1
        rep.value(f"{label}: (target, norm, max |<w0, y>|) -> count", table)
        rep.check(f"{label} (c): max |<w0, y>| <= 6 for all {len(W)} certificates", bool((mx <= 6).all() and (mx >= 0).all()))
    rep.finish()


if __name__ == "__main__":
    main()
