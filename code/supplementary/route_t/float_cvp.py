"""S23. Route T, search (2) by floating-point closest-vector enumeration (supplement §S4.1; Table D2 [C21]).
Supplementary: fplll uses floating-point Gram-Schmidt data and does not guarantee completeness; the
integer certificates (certify.py, check.py) replace it class by class. Not used in the proof of Theorem A.
S23. 経路 T、探索 (2) を浮動小数点の最近ベクトル列挙で（補遺 §S4.1、表 D2 の [C21]）。補助: fplll は浮動小数点の Gram-Schmidt を使い完全性を
保証しない。整数の certificate（certify.py, check.py）が類ごとにこれを置き換える。定理 A の証明には使わない。

For each of the 763,992 classes x_i u_k (1 + tau) + 2L of search (2) (order and kept units as in
common.py): does the class contain a vector of norm <= 8 (0 included)? Closest-vector enumeration at
squared radius 2.05 in a BKZ-40 basis, with the routine of supplementary/float_enumerations.py (cvp88).
Expected: none; the run reported in the supplement (3 parts of about 13 hours) found none.
探索 (2) の 763,992 類 x_i u_k (1 + tau) + 2L（順序と残す単数は common.py）について: 類はノルム 8 以下（0 を含む）の元を含むか。BKZ-40 基底で
半径² 2.05 の最近ベクトル列挙（supplementary/float_enumerations.py の cvp88 と同じ手続き）。期待: 無し。補遺に報告した実行（約 13 時間の 3 分割）では無し。

A floating-point search for search (3) is not included:
all 3,936 classes of search (3) have integer certificates (check.py).
探索 (3) の浮動小数点の探索は収録しない: 探索 (3) の 3,936 類はすべて整数の
certificate がある（check.py）。

Requires SageMath (fpylll). Split with --part/--nparts; resumable (saved every 5,000 classes).
SageMath（fpylll）が要る。--part/--nparts で分割、再開可能（5,000 類ごとに保存）。
Run / 実行:  sage -python code/supplementary/route_t/float_cvp.py [--part P --nparts Q]
"""
import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from common import N_SEARCH2, kept_units, search2_starts  # noqa: E402
from float_enumerations import CosetMinimum, bkz_basis  # noqa: E402
from lib import certs, data  # noqa: E402
from lib.report import Report  # noqa: E402


def main():
    from sage.all import ZZ, matrix
    ap = argparse.ArgumentParser(description="S23: route T search (2) by floating-point CVP")
    ap.add_argument("--part", type=int, default=0)
    ap.add_argument("--nparts", type=int, default=1)
    ap.add_argument("--data", default=None)
    ap.add_argument("--certificates", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    tag = f"s23_route_t_float_cvp_part{a.part}of{a.nparts}"
    rep = Report(tag, a.out)
    Gn = data.gram(a.data)
    t = data.tau(a.data)
    X = certs.load("norm8_reps.npz", "reps", a.certificates).astype(np.int64)
    U = certs.load("centralizer.npz", "units", a.certificates).astype(np.int64)
    keep = kept_units(U, t)
    G = matrix(ZZ, Gn.tolist())
    cm = CosetMinimum(G, bkz_basis(G, 40))
    idx = np.arange(a.part, N_SEARCH2, a.nparts)
    os.makedirs(rep.out_dir, exist_ok=True)
    ck = os.path.join(rep.out_dir, tag + ".state.json")
    st = json.load(open(ck)) if os.path.exists(ck) else {"done": 0, "found": []}
    rep.log(f"part {a.part}/{a.nparts}: {len(idx)} of {N_SEARCH2} classes; resuming at {st['done']}")
    for pos in range(st["done"], len(idx)):
        w = search2_starts(X, U, t, keep, idx[pos:pos + 1])[0]
        v = cm.shortest_in_class(w, 2.05)
        if v is not None:
            assert int(v @ cm.G @ v) <= 8
            st["found"].append(int(idx[pos]))
        if (pos + 1) % 5000 == 0 or pos + 1 == len(idx):
            st["done"] = pos + 1
            tmp = ck + ".tmp"
            json.dump(st, open(tmp, "w"))
            os.replace(tmp, ck)
            rep.log(f"{pos + 1} / {len(idx)} classes, found {len(st['found'])}")
    rep.value("classes containing a vector of norm <= 8 (found by CVP)", st["found"])
    rep.check("none", not st["found"])
    rep.finish()


if __name__ == "__main__":
    main()
