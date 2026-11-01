r"""最小ベクトルの軌道代表 656 個（produce/p2 と verify/v3 が作り、検査する）を、別の実装で点検する（論文 §6.2 の最後の文、§6.3 の m = 6）。

  (b) 656 個の代表の SL$_2$(29)-軌道を全部展開し、互いに交わらないこと、大きさの合計が 15,590,400（テータ級数の係数）になることを確かめる。
      さらに、展開した全最小ベクトルで球面デザインの恒等式（次数 2, 4, 6）が整数として成り立つことを、乱数の $a$ 3 本で確かめる:
      $$\sum_{N(x)=6}(x,a)^{2}=N_6\frac{6\,(a,a)}{56},\quad \sum(x,a)^4=N_6\frac{3\cdot6^2(a,a)^2}{56\cdot58},\quad
        \sum(x,a)^6=N_6\frac{15\cdot6^3(a,a)^3}{56\cdot58\cdot60}.$$
群の元は生成元から自分で列挙し、実装 1 のコードは読み込まない（共有するのはデータ: Gram 行列、生成元、代表）。
すべての検査が通らなければ終了コード 1 で終わる。
(b) The 656 S-orbits of the representatives are expanded; they are pairwise disjoint and their sizes add up to
15,590,400 (the theta-series coefficient); the design identities of degree 2, 4, 6 hold exactly on the expanded
minimal vectors for 3 random vectors a. The group is enumerated from the generators; no code of the main
implementation is read (shared: the Gram matrix, the generators, the representatives). Exit code 1 unless every
check passes.

実行（リポジトリの根から）/ Run from the repository root:  python3 -I code/crosscheck/second_impl/minimal_orbits.py
Run time: about 80 seconds. Memory: about 3.5 GB.
実行時間: 約 80 秒。メモリ: 約 3.5 GB。

data/ の 2 ファイルと certificates/min_reps.npz を読む。テータ係数は定数 15,590,400 とする。ノルム 4 以下の PARI qfminim による列挙は
supplementary/float_enumerations.py qfminim にある。code/lib・code/verify とはコードを共有しない。
Reads two files of data/ and certificates/min_reps.npz; the theta coefficient is the constant 15,590,400. The
enumeration of norm <= 4 with PARI qfminim is in supplementary/float_enumerations.py qfminim. Shares no code with
code/lib or code/verify. Needs only numpy.
"""
import argparse
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
DATA, CERT = ROOT / "data", ROOT / "certificates"
if not __debug__:
    sys.exit("run without -O: the exactness guards are assert statements / -O を付けずに実行すること（厳密性の検査は assert で書かれている）")
FAILS = []
N6 = 15590400                                        # 極値テータ級数の q^3 の係数（code/verify/v2_theta.py）


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


def key(g):
    """± を同一視した行列の鍵（最初の非零成分を正にする）。/ Key of a matrix up to sign (first nonzero entry positive)."""
    i = np.flatnonzero(g.ravel())[0]
    assert np.abs(g).max() < 2 ** 15
    return (g if g.ravel()[i] > 0 else -g).astype(np.int16).tobytes()   # entries up to 248: int8 would wrap / 成分は最大 248 で int8 では折り返す


def group_mod_sign(H):
    """SL_2(29)/±1 を生成元 H から幅優先で列挙する。/ SL_2(29)/±1 by breadth-first search from the generators H."""
    n = H[0].shape[0]
    E0 = np.eye(n, dtype=np.int64); seen = {key(E0): E0}; frontier = [E0]
    while frontier:
        new = []
        for g in frontier:
            for h in H:
                p = g @ h; k = key(p)
                if k not in seen:
                    seen[k] = p; new.append(p)
        frontier = new
    return np.stack(list(seen.values()))


def expand_orbits(R, S):
    """各代表 r の軌道 {± r s} の鍵（± の片方）を作り、軌道どうしが交わらないことを確かめる。
    返り値: 軌道の大きさ（± を両方数える）の一覧、全ベクトル（± の片方、int16）、交わりが無かったか。
    Keys of the orbits {±rs} (one of ±), sizes (both signs counted), all vectors (one of ±, int16), and whether
    the orbits were pairwise disjoint."""
    n = R.shape[1]
    sizes, allkeys, disjoint = [], set(), True
    for r in R:
        Y = r @ S                                       # (|S/±|, n) = r·s
        assert np.abs(Y).max() < 2 ** 15
        sgn = np.sign(Y[np.arange(len(Y)), (Y != 0).argmax(axis=1)])[:, None]
        ks = {row.tobytes() for row in (Y * sgn).astype(np.int16)}
        disjoint &= not (ks & allkeys)
        allkeys |= ks; sizes.append(2 * len(ks))
    V = np.frombuffer(b"".join(allkeys), dtype=np.int16).reshape(-1, n)
    return sizes, V, disjoint


def design_sums(V, Gn, a, chunk=500000):
    """Σ (x, a)^k over x = ±V (k = 2, 4, 6), exactly (Python integers).
    x = ±V にわたる Σ (x, a)^k（k = 2, 4, 6）を厳密に（Python の整数で）。"""
    w = Gn @ a
    tot = {2: 0, 4: 0, 6: 0}
    for i in range(0, len(V), chunk):
        p = (V[i:i + chunk].astype(np.int64) @ w).tolist()
        for v in p:
            v2 = v * v
            tot[2] += 2 * v2; tot[4] += 2 * v2 * v2; tot[6] += 2 * v2 * v2 * v2
    return tot


def design_values(Nm, m, Na, n=56):
    """The right-hand sides of the design identities for a shell of Nm vectors of norm m in dimension n.
    次元 n、ノルム m のベクトル Nm 本の殻についてのデザインの恒等式の右辺。"""
    return {2: Fraction(Nm * m * Na, n), 4: Fraction(Nm * 3 * m ** 2 * Na ** 2, n * (n + 2)),
            6: Fraction(Nm * 15 * m ** 3 * Na ** 3, n * (n + 2) * (n + 4))}


def main():
    argparse.ArgumentParser(description="Second implementation: expansion of the 656 minimal-vector orbits, "
                                        "disjointness, size sum and the design identities for m = 6").parse_args()
    n = 56; t0 = time.time()
    Gn = _ints(DATA / "L56_gram.txt").reshape(n, n)
    H = [h.reshape(n, n) for h in _ints(DATA / "sl2_29_generators.txt").reshape(2, -1)]
    assert all((h @ Gn @ h.T == Gn).all() for h in H)
    S = group_mod_sign(H)
    check("|SL_2(29)/{±1}| = 12180", len(S) == 12180)
    with np.load(CERT / "min_reps.npz", allow_pickle=False) as z:
        R = z["reps"].astype(np.int64)
    check("656 representatives, all of norm 6", len(R) == 656 and ((R @ Gn) * R).sum(axis=1).tolist() == [6] * len(R))
    sizes, V, disjoint = expand_orbits(R, S)
    print(f"(b) 最小ベクトルの代表 {len(R)} 個: 大きさの合計 {sum(sizes)}（テータ級数の係数 {N6}）  [{round(time.time() - t0)} s]", flush=True)
    check("(b) the 656 orbits are pairwise disjoint", disjoint)
    check("(b) their sizes add up to N_6 = 15,590,400", sum(sizes) == N6 and 2 * len(V) == N6)
    rng = np.random.default_rng(7)
    for trial in range(3):
        a = rng.integers(-1, 2, size=n); Na = int(a @ Gn @ a)
        tot, exp = design_sums(V, Gn, a), design_values(N6, 6, Na)
        print(f"    a#{trial} (N(a) = {Na}): {[(k, tot[k], exp[k]) for k in (2, 4, 6)]}  [{round(time.time() - t0)} s]", flush=True)
        for k in (2, 4, 6):
            check(f"(b) design identity of degree {k} for a#{trial} (m = 6)", tot[k] == exp[k])
    finish()


if __name__ == "__main__":
    main()
