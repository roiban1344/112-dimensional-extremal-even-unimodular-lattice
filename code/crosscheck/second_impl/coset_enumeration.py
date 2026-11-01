r"""(8,8) 型の衝突検査の抜き取り点検（別のアルゴリズム。論文 補遺 §S3.3 の「180 類」）。

verify/v6 と crosscheck/second_impl/even_classes.py は、「類 $x u \tau + 2L$ にノルム 8 があるか」を、類の標準形
（XOR）で判定する。ここでは同じ問いを、**格子 $L''=\langle 2L,\ t\rangle$（$t = x u \tau$）のノルム 8 以下の全列挙**（PARI qfminim）で判定する。
$2L$ の最小ノルムは $4\cdot6=24$ なので、$L''$ のノルム 8 以下のベクトルはすべて類 $t+2L$ に入る。標準形も表 $K_8$ も使わない。

  - 陽性対照: 貼り方 B の衝突する 10 組（certificates/negative_control_B.npz の hit_pairs と tau_B）で、どれもノルム 8 が見つかること。
  - 本論文の tau: 乱数で選んだ（ノルム 8 の軌道代表 x, 中心化群の元 u）の組 --samples 個（既定 180）で、ノルム 8 が無いこと。
抜き取りなので、全数検査の代わりにはならない（衝突の割合は貼り方 B でも 10^{-5} 程度）。検査の「向き・定義の取り違え」を見つけるためのもの。
PARI の qfminim は内部で浮動小数点を使うので、これは証明ではなく点検である。
Sample check of the test for type (8,8) by another algorithm (supplement §S3.3, "180 classes"): whether the class
x u tau + 2L contains a vector of norm 8 is decided by enumerating all vectors of norm <= 8 of the lattice
<2L, t> (t = x u tau) with PARI's qfminim, without canonical forms or K_8 (min 2L = 24, so every such vector lies in
t + 2L). Positive control: the 10 colliding pairs of gluing B (all must be found). For the tau of the paper: a random
sample of --samples pairs (default 180), none of which may contain a norm-8 vector. A sample, not a proof (qfminim
uses floating point internally); it detects mistakes in the direction or definition of the test.

実行（リポジトリの根から。SageMath を含む Python で）/ Run from the repository root with the Python of SageMath:
    python3 -I code/crosscheck/second_impl/coset_enumeration.py [--samples 180] [--seed 0]
Requires SageMath (PARI). Run time: about 34 seconds per pair, about 1.7 hours for 180 pairs and the control.
Memory: below 1 GB.
SageMath（PARI）が要る。実行時間: 1 組あたり約 34 秒、180 組と対照で約 1.7 時間。メモリ: 1 GB 未満。

data/ の 2 ファイルと certificates/ の norm8_reps.npz・centralizer.npz・negative_control_B.npz を読む。code/lib・code/verify とはコードを共有しない。
Reads two files of data/ and the certificate files norm8_reps.npz, centralizer.npz and negative_control_B.npz.
Shares no code with code/lib or code/verify.
"""
import argparse
import random
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
DATA, CERT = ROOT / "data", ROOT / "certificates"
if not __debug__:
    sys.exit("run without -O: the exactness guards are assert statements / -O を付けずに実行すること（厳密性の検査は assert で書かれている）")
FAILS = []


def check(name, ok):
    """Print [ok] or [FAIL]; the script ends with exit code 1 if any check failed (see finish).
    [ok] か [FAIL] を表示する。一つでも失敗すれば終了コード 1 で終わる（finish を参照）。"""
    ok = bool(ok)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}", flush=True)
    if not ok:
        FAILS.append(name)
    return ok


def finish():
    print("RESULT: PASS" if not FAILS else f"RESULT: FAIL ({len(FAILS)} failed: {FAILS})", flush=True)
    sys.exit(1 if FAILS else 0)


def _ints(path):
    return np.array([int(t) for l in open(path) if not l.startswith("#") for t in l.split()], dtype=np.int64)


def _npz(name, key):
    with np.load(CERT / name, allow_pickle=False) as z:
        return z[key]


def main():
    ap = argparse.ArgumentParser(description="Sample check of the (8,8) test by enumeration in <2L, t> (PARI qfminim)")
    ap.add_argument("--samples", type=int, default=180, help="number of random pairs (x, u) for the tau of the paper")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    from sage.all import ZZ, matrix, pari, vector
    n = 56; t0 = time.time()
    G = matrix(ZZ, n, n, _ints(DATA / "L56_gram.txt").tolist())
    units = [matrix(ZZ, n, n, u.astype(np.int64).ravel().tolist()) for u in _npz("centralizer.npz", "units")]
    X = matrix(ZZ, n, n, _ints(DATA / "tau.txt").tolist())
    XB = matrix(ZZ, n, n, _npz("negative_control_B.npz", "tau_B").astype(np.int64).ravel().tolist())
    T = G.LLL_gram()                                              # L の簡約基底（列が新基底の旧座標）
    Tb = T.transpose()                                            # 行 = 簡約基底ベクトル（旧座標）

    def coset_short(t):
        """類 t + 2L のノルム ≤ 8 のベクトル（± で 1 本ずつ）の本数と 1 例。
        Number of vectors of norm <= 8 in t + 2L (one of each ±pair) and one of them."""
        c = Tb.solve_left(vector(ZZ, t))                          # t の簡約基底での座標 c（t = c·Tb）
        e = vector(ZZ, [ci % 2 for ci in c])                      # 類は c mod 2 だけで決まる。e を類の代表に取り直す
        assert not e.is_zero(), "t lies in 2L"
        j = next(i for i in range(n) if e[i])
        Bm = (2 * Tb).change_ring(ZZ); Bm[j] = e * Tb             # ⟨2L, e⟩ の基底（e_j = 1 なので 2b_j も入る）
        G2 = Bm * G * Bm.transpose()
        U = G2.LLL_gram(); G2r = U.transpose() * G2 * U
        r = pari(G2r).qfminim(8, 4, 0)
        cnt = int(r[0]) // 2
        if cnt == 0:
            return 0, None
        v = (U * vector(ZZ, [int(a) for a in r[2][0]])) * Bm      # qfminim の列 = 簡約基底での座標
        assert v * G * v == 8 and all((a - b) % 2 == 0 for a, b in zip(Tb.solve_left(v), c))
        return cnt, v

    hits = _npz("negative_control_B.npz", "hit_pairs").astype(np.int64)
    ok = sum(coset_short(vector(ZZ, w.tolist()) * XB)[0] > 0 for w in hits)
    print(f"陽性対照（貼り方 B の衝突 {len(hits)} 組）: 全列挙でノルム 8 が出たもの {ok}  [{round(time.time() - t0)} s]", flush=True)
    check(f"positive control: a norm-8 vector in each of the {len(hits)} colliding classes of gluing B", len(hits) == 10 and ok == len(hits))

    R = _npz("norm8_reps.npz", "reps")
    rng = random.Random(1013 + a.seed)
    pos = neg = 0
    for s in range(a.samples):
        x = vector(ZZ, [int(v) for v in R[rng.randrange(len(R))]]); u = rng.choice(units)
        cnt, v = coset_short(x * u * X)
        pos += cnt > 0; neg += cnt == 0
        if cnt:
            print(f"  !! 衝突 / collision: x = {x}, 類にノルム 8 が {cnt} 対", flush=True)
        if (s + 1) % 20 == 0:
            print(f"  {s + 1} 組: 衝突あり {pos}, なし {neg}  [{round(time.time() - t0)} s]", flush=True)
    check(f"tau of the paper: none of {a.samples} random pairs (x, u) has a norm-8 vector in x u tau + 2L", pos == 0)
    finish()


if __name__ == "__main__":
    main()
