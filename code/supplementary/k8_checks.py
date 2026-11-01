"""Sampled checks of the table K_8 and of the canonical-form test (paper §6.4, Table 6 first row, §6.5;
supplement §S3.6; Table D2 [C34]). Not used in the proof of Theorem A.
表 K_8 と標準形による検査の抜き取りの点検（論文 §6.4、表 6 の 1 行目、§6.5。補遺 §S3.6。表 D2 の [C34]）。定理 A の証明には使わない。

Uses out/K8.npy from verify/v4_norm8_orbits.py (checked against out/v4_norm8_orbits.json, as V6 does).
verify/v4_norm8_orbits.py の out/K8.npy を使う（V6 と同じく out/v4_norm8_orbits.json と照合する）。

  (a) positive control (Table 6, first row): for a gluing map f in C (an element of the centralizer other
      than +-1) every class x_i u_k f + 2L contains the norm-8 vector x_i u_k f, so its canonical form must
      be in K_8; checked on 3,000 pairs (x_i, u_k) spread evenly over the 1,527,984 pairs;
      陽性対照（表 6 の 1 行目）: C の元 f（中心化群の ±1 以外の元）で貼ると、類 x_i u_k f + 2L はノルム 8 のベクトル x_i u_k f を含むので、
      標準形は K_8 に入るはず。1,527,984 組から等間隔に選んだ 3,000 組で確かめる;
  (b) 2,000 norm-8 vectors generated independently of the orbit list (§6.4): v = a -+ b for minimal vectors
      a = r_j g u, b = r_j' g' u' (random j, g in S/{+-1}, u in C/{+-1}) with <a, b> = +-2; the class of every v
      must be in K_8;
      軌道の表と独立に作ったノルム 8 のベクトル 2,000 本（§6.4）: 最小ベクトル a = r_j g u、b = r_j' g' u'（j、g ∈ S/{±1}、u ∈ C/{±1} は乱数）
      で <a, b> = ±2 のとき v = a ∓ b。どの v の類も K_8 に入るはず;
  (c) the canonical-form test against closest-vector enumeration (fplll, squared radius 2.05, a BKZ-40 basis;
      CosetMinimum of supplementary/float_enumerations.py) (supplement §S3.6): on 150 random pairs for the
      tau of the paper (all without a norm-8 vector), on 150 random pairs for gluing B, and on the 10 colliding
      pairs of gluing B (certificates/negative_control_B.npz: hit_pairs, tau_B), the two tests agree. The 36
      colliding pairs of gluing A are checked in the same way by supplementary/nebe/gluings_m.py (e).
      標準形による検査と最近ベクトル列挙（fplll、半径² 2.05、BKZ-40 基底。supplementary/float_enumerations.py の CosetMinimum）の
      突き合わせ（補遺 §S3.6）: 本論文の tau の乱数の 150 組（どれもノルム 8 を含まない）、貼り方 B の乱数の 150 組、貼り方 B の衝突する 10 組
      （certificates/negative_control_B.npz の hit_pairs と tau_B）で、二つの検査が一致する。貼り方 A の衝突する 36 組は
      supplementary/nebe/gluings_m.py の (e) で同じように確かめる。
Requires SageMath (fpylll) for (c). Run time: about 3 minutes (after V4). Memory: about 1 GB.
(c) に SageMath（fpylll）が要る。実行時間: 約 3 分（V4 のあと）。メモリ: 約 1 GB。
Run / 実行:  python3 code/supplementary/k8_checks.py
"""
import argparse
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from lib import certs, data, exact, group, mod2  # noqa: E402
from lib.report import Report, load_output_of  # noqa: E402

TOTAL = 1527984


def evenly_spaced(total, k):
    """k indices spread evenly over range(total). / range(total) から等間隔に選んだ k 個の添字。"""
    step = total // k
    return np.arange(k) * step


def sums_of_two_minimal(R6, S, U, G, count, rng):
    """`count` norm-8 vectors a -+ b, with a, b random minimal vectors r g u and <a, b> = +-2.
    ノルム 8 のベクトル a ∓ b を count 本（a, b は乱数の最小ベクトル r g u、<a, b> = ±2）。"""
    mm = exact.i64_matmul
    out = []
    while len(out) < count:
        a = mm(mm(R6[rng.integers(len(R6))], S[rng.integers(len(S))].astype(np.int64)), U[rng.integers(len(U))])
        b = mm(mm(R6[rng.integers(len(R6))], S[rng.integers(len(S))].astype(np.int64)), U[rng.integers(len(U))])
        ip = int(a @ G @ b)
        if abs(ip) == 2:
            out.append(a - b if ip == 2 else a + b)
    return np.stack(out)


def main():
    ap = argparse.ArgumentParser(description="Sampled checks of K_8 and of the canonical-form test")
    ap.add_argument("--data", default=None)
    certs.add_arguments(ap)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rep = Report("k8_checks", a.out)
    mm = exact.i64_matmul
    G = data.gram(a.data)
    t = data.tau(a.data)
    gens = data.generators(a.data)
    S = group.sl2_29_mod_sign(gens)
    R6 = certs.load("min_reps.npz", "reps", a.certificates).astype(np.int64)
    X = certs.load("norm8_reps.npz", "reps", a.certificates).astype(np.int64)
    U = certs.load("centralizer.npz", "units", a.certificates).astype(np.int64)
    tB = certs.load("negative_control_B.npz", "tau_B", a.certificates).astype(np.int64)
    hitsB = certs.load("negative_control_B.npz", "hit_pairs", a.certificates).astype(np.int64)
    K8 = load_output_of(rep, "v4_norm8_orbits", "K8.npy", certs.file_hashes(certs.K8_INPUTS, a.certificates))
    rep.check("K_8 from V4 has 1517130 entries", len(K8) == 1517130)
    can = mod2.Canonical(S)
    I = np.eye(56, dtype=np.int64)

    def in_k8(V):
        return np.isin(can.canon(mod2.pack(V)), K8)

    def pairs(idx):
        i, k = np.divmod(idx, 6)
        return np.stack([mm(X[ii], U[kk]) for ii, kk in zip(i.tolist(), k.tolist())])

    # (a) / (a)
    f = next(u for u in U if not ((u == I).all() or (u == -I).all()))
    idx = evenly_spaced(TOTAL, 3000)
    hit = in_k8(mm(pairs(idx), f))
    rep.value("(a) pairs tested, and classes x_i u_k f + 2L in K_8 (f in C, not +-1)", [len(idx), int(hit.sum())])
    rep.check("(a) positive control: all 3000 classes x_i u_k f + 2L are in K_8", len(idx) == 3000 and hit.all())

    # (b) / (b)
    V = sums_of_two_minimal(R6, S, U, G, 2000, np.random.default_rng(5))
    rep.check("(b) 2000 vectors a -+ b of norm 8", len(V) == 2000 and (exact.norms(V, G) == 8).all())
    rep.check("(b) the class of every one of them is in K_8", in_k8(V).all())

    # (c) / (c)
    from float_enumerations import CosetMinimum, bkz_basis
    from sage.all import ZZ, matrix
    Gs = matrix(ZZ, G.tolist())
    cm = CosetMinimum(Gs, bkz_basis(Gs, 40))
    rep.value("(c) reduced diagonal of the basis", cm.Gr_diag)
    rng = np.random.default_rng(6)

    def compare(W):
        """For each row w: (canonical-form test, CVP test). / 各行 w について（標準形の検査, CVP の検査）。"""
        lookup = in_k8(W)
        found = []
        for w in W:
            v = cm.shortest_in_class(w, 2.05)
            found.append(v is not None and int(v @ G @ v) == 8)
        return lookup, np.array(found)

    for name, tt, W in (("tau of the paper, 150 random pairs", t, None), ("gluing B, 150 random pairs", tB, None),
                        ("gluing B, the 10 colliding pairs", tB, hitsB)):
        W = mm(pairs(rng.integers(0, TOTAL, size=150)) if W is None else W, tt)
        lookup, found = compare(W)
        rep.value(f"(c) {name}: classes with a norm-8 vector by canonical forms, by CVP", [int(lookup.sum()), int(found.sum())])
        rep.check(f"(c) {name}: the two tests agree on every pair", (lookup == found).all())
        if W.shape[0] == 10:
            rep.check("(c) the 10 colliding pairs of gluing B are found by both tests", lookup.all() and found.all())
        elif tt is t:
            rep.check("(c) no pair of the tau of the paper is found by either test", not lookup.any() and not found.any())
    rep.finish()


if __name__ == "__main__":
    main()
