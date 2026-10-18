"""V7. F5b by even-class certificates: min(x_i u_k tau + 2L) >= 12 for all 1,527,984 pairs
(paper §4.3 F5b, Corollary 5.3, Check 5.4, §6.7, Table 8).
V7. 偶の類の certificate による F5b: 1,527,984 組すべてについて min(x_i u_k tau + 2L) ≥ 12
（論文 §4.3 の F5b、系 5.3、検査 5.4、§6.7、表 8）。

Row 6 i + k of certificates/even_bounding.npz is a vector w0 with
certificates/even_bounding.npz の第 6i+k 行はベクトル w0 で、
  (a) w0 - x_i u_k tau has even coordinates (w0 lies in the class);
      w0 - x_i u_k tau の座標がすべて偶数（w0 は類に入る）;
  (b) <w0, w0> is 12, 16 or 20;
      <w0, w0> は 12, 16, 20 のどれか;
  (c) |<w0, u>| <= 6 for every minimal vector u of L.
      L のすべての最小ベクトル u について |<w0, u>| ≤ 6。
By Corollary 5.3 the class contains no vector of norm 8. Together with F3 (V4) this proves
condition (ii) of Corollary 4.3 without canonical forms (an alternative to V6).
系 5.3 より、類はノルム 8 のベクトルを含まない。F3（V4）と合わせて、標準形を使わずに系 4.3 の条件 (ii) が示される（V6 の代わり）。

(c) is the expensive part: 1.5 million x 7.8 million inner products. It is done in chunks with
a checkpoint (out/v7_even_bounding.state.npz, or out/v7_even_bounding_first<N>.state.npz with
--limit N), so an interrupted run resumes with the same command. The checkpoint records the SHA-256
of the certificate rows checked, of min_reps.npz, L56_gram.txt, sl2_29_generators.txt and of the
code computing (c) (lib/shells.py, exact.py, group.py), and n and --limit. If any of them differs
when resuming, the run FAILS and asks to delete the checkpoint (it is never used for other data,
and never deleted silently). The checkpoint is deleted when (c) is complete, so every complete run
computes (c) from the start. Use --threads to run several BLAS-free Python threads (each matrix
product is single-threaded then).
(c) が重い部分で、150 万 × 780 万の内積。チャンクごとに途中経過（out/v7_even_bounding.state.npz。--limit N のときは
out/v7_even_bounding_first<N>.state.npz）を保存するので、止まっても同じコマンドで再開する。途中経過には、検査する certificate の行、
min_reps.npz、L56_gram.txt、sl2_29_generators.txt、(c) を計算するコード（lib/shells.py, exact.py, group.py）の SHA-256 と、
n と --limit を記録する。再開するときにどれかが異なれば不合格とし、途中経過を消すよう求める（別のデータに使うことはなく、
黙って消すこともない）。(c) が終わると途中経過を消すので、最後まで走る実行は毎回 (c) を最初から計算する。
--threads で複数の Python のスレッドを使う（そのとき各行列積は 1 スレッド）。

Exactness: (a), (b) in int64; (c) in float32 with the exactness bound checked for every chunk.
The maxima are kept in int64 (no wrap-around).
厳密さ: (a), (b) は int64。(c) は float32 で、チャンクごとに厳密さの上界を確かめる。最大値は int64 で持つ（回り込まない）。

Run time: about 24 CPU hours for (c) (7.9 hours with --threads 3). Memory: about 3 GB.
実行時間: (c) に約 24 CPU 時間（--threads 3 で 7.9 時間）。メモリ: 約 3 GB。

Run / 実行:  python3 code/verify/v7_even_bounding.py [--threads T] [--limit N] [--data DIR] [--certificates DIR] [--out DIR]
             (--limit N checks only the first N pairs, for a quick test / 先頭の N 組だけを確かめる。試験用)
"""
import os
import sys

if any(arg == "--threads" or arg.startswith("--threads=") for arg in sys.argv):
    # One BLAS thread per Python thread. Must be set before numpy is imported.
    # Python のスレッド 1 本につき BLAS も 1 スレッド。numpy を読み込む前に設定する。
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"

import argparse  # noqa: E402

import numpy as np  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import certs, data, exact, group, shells  # noqa: E402
from lib.report import Report  # noqa: E402

NPAIRS = 1527984


def main():
    ap = argparse.ArgumentParser(description="V7: F5b by even-class certificates")
    ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--chunk", type=int, default=8192, help="pairs per checkpoint / 途中経過の保存ごとの組数")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--data", default=None)
    ap.add_argument("--certificates", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rep = Report("v7_even_bounding" + (f"_first{a.limit}" if a.limit else ""), a.out)

    G = data.gram(a.data)
    t = data.tau(a.data)
    S = group.sl2_29_mod_sign(data.generators(a.data))
    R6 = certs.load("min_reps.npz", "reps", a.certificates).astype(np.int64)
    X = certs.load("norm8_reps.npz", "reps", a.certificates).astype(np.int64)
    U = certs.load("centralizer.npz", "units", a.certificates).astype(np.int64)
    W = certs.load("even_bounding.npz", "w0", a.certificates)
    rep.check("254664 representatives x_i and 6 matrices u_k", X.shape == (NPAIRS // 6, 56) and U.shape == (6, 56, 56))
    rep.check("1527984 certificates, one per pair (row 6 i + k)", W.shape == (NPAIRS, 56))
    n = a.limit or NPAIRS
    rep.check("1 <= --limit <= 1527984", 1 <= n <= NPAIRS)
    mm = exact.i64_matmul

    # (a), (b): grouped by k, rows k, k + 6, k + 12, ... / k ごとにまとめる（第 k, k+6, k+12, … 行）
    ok_a = True
    norms = np.full(NPAIRS, -1, dtype=np.int64)
    for k, u in enumerate(U):
        Wk = W[k::6].astype(np.int64)
        start = mm(mm(X, u), t)
        ok_a &= bool(((Wk - start) % 2 == 0).all())
        norms[k::6] = exact.norms(Wk, G)
    rep.check("(a) w0 - x_i u_k tau has even coordinates, for all pairs", ok_a)
    hist_norm = {int(v): int(c) for v, c in zip(*np.unique(norms, return_counts=True))}
    rep.value("(b) norms {norm: count}", hist_norm)
    rep.check("(b) every <w0, w0> is 12, 16 or 20", np.isin(norms, (12, 16, 20)).all())

    # (c) with checkpoints / 途中経過を保存しながら
    mv = shells.MinimalVectors(G, R6, S)
    rep.log(f"expanded {2 * mv.count} minimal vectors; checking (c) for {n} pairs with {a.threads} thread(s)")
    state = os.path.join(rep.out_dir, rep.step + ".state.npz")
    inputs = [certs.path_checked("min_reps.npz", a.certificates)]
    inputs += [os.path.join(a.data or data.DEFAULT_DIR, f) for f in ("L56_gram.txt", "sl2_29_generators.txt")]
    fp = shells.fingerprint(W[:n], inputs + shells.CODE_FILES, {"n": n, "limit": a.limit})
    mx, secs, resumed = shells.max_abs_inner_checkpointed(mv, W[:n], a.threads, a.chunk, state, fp, rep)
    rep.value("(c) pairs taken over from the checkpoint", resumed)
    table = {}
    for (nn, m), c in zip(*np.unique(np.stack([norms[:n], mx], axis=1), axis=0, return_counts=True)):
        table[f"norm {nn}, max {m}"] = int(c)
    rep.value("Table 8: (norm, max |<w0, u>|) -> count", table)
    rep.value("seconds spent in (c)", round(secs))
    rep.check(f"(c) max |<w0, u>| <= 6 over all minimal vectors u, for all {n} pairs", (mx <= 6).all() and (mx >= 0).all())
    if n < NPAIRS:
        rep.log(f"NOTE: only the first {n} pairs were checked (--limit)")
    rep.finish()


if __name__ == "__main__":
    main()
