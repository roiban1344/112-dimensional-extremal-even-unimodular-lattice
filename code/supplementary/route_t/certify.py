"""S21. Route T, producing the certificates of searches (2) and (3) (supplement §S4.1; Table D2 [C21]).
Not used in the proof of Theorem A. The certificates are checked independently by check.py.
S21. 経路 T、探索 (2)・(3) の certificate を作る（補遺 §S4.1、表 D2 の [C21]）。定理 A の証明には使わない。certificate は check.py が別に検算する。

For each class (see common.py) a vector w0 of the class is reduced until |<w0, y>| <= 6 for all
minimal vectors y: while some y has <w0, y> >= 7 (up to sign), replace w0 by w0 - 2 sign y, which
stays in the class and lowers the norm. The result is a certificate if its norm is allowed by the
lemma (common.py); otherwise the class is recorded as unresolved. How w0 is found does not matter
for correctness: check.py re-checks every property used.
各類（common.py）の元 w0 を、すべての最小ベクトル y で |<w0, y>| ≤ 6 になるまで縮める: (符号を除き) <w0, y> ≥ 7 の y があれば
w0 を w0 - 2 sign y に替える（類にとどまり、ノルムが下がる）。結果のノルムが補題（common.py）の許す値なら certificate、そうでなければ
未解決として記録する。w0 の見つけ方は正しさに関係しない: 使う性質はすべて check.py が確かめ直す。

The inner products <r_j g, w> (656 orbit representatives r_j times the 12,180 elements g of
SL_2(29)/{+-1}) are computed in float64 with the exactness bound asserted (all partial sums are
integers below 2^52). The distributed certificates were produced with another table of SL_2(29)/{+-1} (the same group, other
signs and order), so a rerun may choose other certificates; both are valid.
内積 <r_j g, w>（656 個の軌道代表 r_j と SL_2(29)/{±1} の 12,180 元 g）は float64 で、厳密さの上界（部分和がすべて 2^52 未満の整数）を
確かめて計算する。配布した certificate は SL_2(29)/{±1} の別の表（同じ群で、符号と順序が違う）で作ったので、再実行では別の certificate が
選ばれることがある。どちらも有効。

Modes / モード:
  search3                         the 3,936 classes of search (3), about 25 minutes
                                  探索 (3) の 3,936 類、約 25 分
  search2 --part P --nparts Q     classes P, P + Q, P + 2Q, ... of search (2); optionally only positions
          [--lo A --hi B]         A..B-1 of that list (to split a slow part). About 1 to 2 s per class on
                                  one core, about 13 CPU days for all 763,992 classes
                                  探索 (2) の第 P, P+Q, P+2Q, … 類。--lo/--hi でその中の位置 A〜B-1 だけ（遅い分割を分けるため）。
                                  1 コアで 1 類 1〜2 秒、763,992 類の全部で約 13 CPU 日
  search2 --missing [--part P --nparts Q]
                                  only the classes without a certificate in certificates/route_t_search2.npz
                                  (to complete the distributed file); split among parts as above
                                  certificates/route_t_search2.npz で certificate の無い類だけ（配布ファイルを完成させるため）
  collect [--from DIR] [--base]   merge the outputs (in out/route_t/, or DIR with the same file names) into
                                  out/route_t/route_t_search3.npz and route_t_search2.npz, the files
                                  distributed in certificates/; search (2) may be incomplete (array done)
                                  (--base: start from the distributed certificates/route_t_search2.npz and add the
                                  --missing outputs) / （--base: 配布の route_t_search2.npz に --missing の出力を足す）
                                  出力（out/route_t/、または同じファイル名の DIR）を out/route_t/route_t_search3.npz・route_t_search2.npz に
                                  まとめる（certificates/ で配るファイル）。探索 (2) は途中でもよい（配列 done）
Every mode is resumable: outputs are saved every 1,000 classes (temporary file, then rename), and
the same command continues.
どのモードも再開できる: 1,000 類ごとに保存し（一時ファイルに書いてから改名）、同じコマンドで続きから。

Output names / 出力名: out/route_t/n6-C.{npz,json},
out/route_t/n8-C-1tau-part<P>of<Q>[-pos<A>-<B>].{npz,json}.
Run / 実行:  python3 code/supplementary/route_t/certify.py <search3|search2|collect> [...]
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from common import ALLOWED, N_SEARCH2, N_SEARCH3, kept_units, search2_starts, search3_classes  # noqa: E402
from lib import certs, data, group  # noqa: E402
from lib.report import Report  # noqa: E402


class Certifier:
    def __init__(self, G, S, R6):
        self.G = G
        self.E = S.astype(np.float64)                       # (12180, 56, 56)
        self.R = R6.astype(np.float64)
        self.RT = np.ascontiguousarray(self.R.T)
        self.emax, self.rmax = float(np.abs(self.E).max()), float(np.abs(self.R).max())

    def ips(self, w):
        """P[g, j] = <r_j g, w>; float64, exact (bound asserted). / float64 で厳密（上界を確かめる）。"""
        gw = (self.G @ w).astype(np.float64)
        assert self.emax * np.abs(gw).sum() < 2.0 ** 52
        t = self.E @ gw
        assert self.rmax * np.abs(t).sum(axis=1).max() < 2.0 ** 52
        return t @ self.RT

    def certify(self, w_start, target):
        w = w_start.copy()
        m = 99
        for _ in range(200):
            P = self.ips(w)
            k = int(np.abs(P).argmax())
            g, j = divmod(k, P.shape[1])
            m = int(round(P[g, j]))
            if abs(m) <= 6:
                break
            y = np.rint(self.R[j] @ self.E[g]).astype(np.int64)
            w = w - 2 * (1 if m > 0 else -1) * y
        N = int(w @ self.G @ w)
        assert ((w - w_start) % 2 == 0).all() and np.abs(w).max() < 2 ** 15
        return w, N, abs(m), (abs(m) <= 6 and N in ALLOWED[target])


def run(cz, out, name, starts, targets, rep):
    jf, nf = os.path.join(out, name + ".json"), os.path.join(out, name + ".npz")
    if os.path.exists(jf) and os.path.exists(nf):
        st = json.load(open(jf))
        W = list(np.load(nf)["w0"])[: st["done"]]
    else:
        st, W = {"done": 0, "hist": {}, "unresolved": []}, []

    def save():
        certs.save_npz(nf, w0=np.stack(W).astype(np.int16) if W else np.zeros((0, 56), np.int16))
        tmp = jf + ".tmp"
        json.dump(st, open(tmp, "w"))
        os.replace(tmp, jf)
    rep.log(f"{name}: {len(starts)} classes, resuming at {st['done']}")
    t0 = time.time()
    for pos in range(st["done"], len(starts)):
        w, N, m, ok = cz.certify(starts[pos], targets[pos])
        key = f"{targets[pos]}:{N},{m}"
        st["hist"][key] = st["hist"].get(key, 0) + 1
        if not ok:
            st["unresolved"].append([pos, N, m])
        W.append(w.astype(np.int16))
        if (pos + 1) % 1000 == 0 or pos + 1 == len(starts):
            st["done"] = pos + 1
            save()
            if (pos + 1) % 10000 == 0 or pos + 1 == len(starts):
                rep.log(f"   {pos + 1}/{len(starts)}  {round(time.time() - t0)} s  hist {st['hist']}  unresolved {len(st['unresolved'])}")
    return st


def collect(src, out, rep, base=None):
    """Merge into the distributed files. / 配布するファイルにまとめる。"""
    if base is not None:
        W3 = certs.load("route_t_search3.npz", "w0", base)
        W2 = certs.load("route_t_search2.npz", "w0", base).copy()
        done = certs.load("route_t_search2.npz", "done", base).copy()
        rep.log(f"base: {int(done.sum())} certified classes in the distributed file")
    else:
        W3 = np.load(os.path.join(src, "n6-C.npz"))["w0"]
        W2 = np.zeros((N_SEARCH2, 56), dtype=np.int16)
        done = np.zeros(N_SEARCH2, dtype=bool)
    rep.check("search (3): all 3,936 certificates present", W3.shape == (N_SEARCH3, 56))
    for f in sorted(glob.glob(os.path.join(src, "n8-missing-part*.npz"))):
        if f.endswith(".tmp.npz") or f.endswith(".idx.npz"):
            continue
        Wf = np.load(f)["w0"]
        n_done = json.load(open(f[:-4] + ".json"))["done"]
        idx = np.load(f[:-4] + ".idx.npz")["idx"][:n_done]
        W2[idx], done[idx] = Wf[:n_done], True
        rep.log(f"{os.path.basename(f)}: {n_done} certificates")
    pat = re.compile(r"n8-C-1tau-part(\d+)of(\d+)(?:-pos(\d+)-(\d+))?\.npz$")
    for f in sorted(glob.glob(os.path.join(src, "n8-C-1tau-part*.npz"))):
        if base is not None:
            break
        mt = pat.search(os.path.basename(f))
        if not mt or f.endswith(".tmp.npz"):
            continue
        part, nparts = int(mt.group(1)), int(mt.group(2))
        lo = int(mt.group(3)) if mt.group(3) else 0
        Wf = np.load(f)["w0"]
        n_done = json.load(open(f[:-4] + ".json"))["done"]
        idx = np.arange(part, N_SEARCH2, nparts)[lo:lo + n_done]
        rep.check(f"{os.path.basename(f)}: {n_done} certificates for as many classes", len(idx) == n_done <= len(Wf))
        W2[idx], done[idx] = Wf[:n_done], True
        rep.log(f"{os.path.basename(f)}: {n_done} certificates")
    rep.value("search (2): classes with a certificate (of 763,992)", int(done.sum()))
    os.makedirs(out, exist_ok=True)
    for name, arrays in (("route_t_search3.npz", dict(w0=W3)), ("route_t_search2.npz", dict(w0=W2, done=done))):
        p = os.path.join(out, name)
        certs.save_npz(p, **arrays)
        rep.value(f"sha256 {name}", hashlib.sha256(open(p, "rb").read()).hexdigest())


def main():
    ap = argparse.ArgumentParser(description="S21: route T certificates")
    ap.add_argument("mode", choices=("search3", "search2", "collect"))
    ap.add_argument("--part", type=int, default=0)
    ap.add_argument("--nparts", type=int, default=1)
    ap.add_argument("--lo", type=int, default=None)
    ap.add_argument("--hi", type=int, default=None)
    ap.add_argument("--missing", action="store_true")
    ap.add_argument("--base", action="store_true")
    ap.add_argument("--from", dest="src", default=None)
    ap.add_argument("--data", default=None)
    ap.add_argument("--certificates", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    tag = "s21_route_t_" + a.mode + (f"_part{a.part}of{a.nparts}" if a.mode == "search2" else "")
    rep = Report(tag, a.out)
    out = os.path.join(rep.out_dir, "route_t")
    os.makedirs(out, exist_ok=True)
    if a.mode == "collect":
        collect(a.src or out, out, rep, base=(a.certificates or "") if a.base else None)
        rep.finish()
        return
    G = data.gram(a.data)
    t = data.tau(a.data)
    S = group.sl2_29_mod_sign(data.generators(a.data)).astype(np.int64)
    R6 = certs.load("min_reps.npz", "reps", a.certificates).astype(np.int64)
    U = certs.load("centralizer.npz", "units", a.certificates).astype(np.int64)
    rep.check("SL_2(29)/{+-1} has 12,180 elements", len(S) == 12180)
    keep = kept_units(U, t)
    rep.value("kept units", keep)
    cz = Certifier(G, S, R6)
    if a.mode == "search3":
        starts, targets = search3_classes(R6, U, t)
        st = run(cz, out, "n6-C", starts, targets, rep)
    else:
        X = certs.load("norm8_reps.npz", "reps", a.certificates).astype(np.int64)
        pos = f"-pos{a.lo}-{a.hi}" if a.lo is not None else ""
        if a.missing:
            # The classes are those still missing in the distributed file, sliced by --lo/--hi; the list is saved
            # under the final name (collect reads it from there) and reused on a restart, so that certificates
            # made before a change of the distributed file keep their classes.
            # 対象は配布ファイルでまだ欠けている類（--lo/--hi で切り出す）。一覧は最終的な名前で保存し（collect はそこから読む）、
            # 再開時にはそれを使う。配布ファイルが途中で変わっても、それ以前に作った certificate の類はずれない。
            name = f"n8-missing-part{a.part}of{a.nparts}{pos}"
            idx_path = os.path.join(out, name + ".idx.npz")
            if os.path.exists(idx_path):
                idx = np.load(idx_path)["idx"]
                rep.log(f"reusing the class list {idx_path}")
            else:
                done = certs.load("route_t_search2.npz", "done", a.certificates).astype(bool)
                idx = np.flatnonzero(~done)[a.part::a.nparts]
                if a.lo is not None:
                    idx = idx[a.lo:a.hi]
                certs.save_npz(idx_path, idx=idx)
        else:
            idx = np.arange(a.part, N_SEARCH2, a.nparts)
            if a.lo is not None:
                idx = idx[a.lo:a.hi]
            name = f"n8-C-1tau-part{a.part}of{a.nparts}{pos}"
        starts = search2_starts(X, U, t, keep, idx)
        st = run(cz, out, name, starts, ["8"] * len(idx), rep)
    rep.value("(target: norm, max |<w0, y>|) -> count", st["hist"])
    rep.check("no unresolved class", not st["unresolved"])
    rep.finish()


if __name__ == "__main__":
    main()
