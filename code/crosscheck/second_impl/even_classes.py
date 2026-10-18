r"""(8,8) 型の衝突の全数検査を、別実装でやり直す（考え方は元の計算（公開版では verify/v6）と同じ、コードは共有しない）。

主張: $x$ をノルム 8 の全ベクトルにわたらせたとき、類 $xX+2L$ がノルム 8 のベクトルを含むことは無い。
考え方: $L/2L$ の類を 56 ビットの整数で表す。SL$_2$(29) は $L/2L$ に作用し、$X$ と mod 2 で可換（ここで直接確かめる）。
類の「標準形」= 群の 12,180 個の元（±を同一視）で動かした像の最小値。
  K8 = { 標準形(類(r u)) : r はノルム 8 の軌道代表 254,664 個、u は単数 6 個 }  … ノルム 8 のベクトルの類の標準形の全体
  検査: すべての (r, u) について 標準形(類(r u X)) ∈ K8 か。（逆向き: X の代わりに X^{-1} mod 2）
代表の完全性は大きさの和（verify/v4、check_all.py v4）による。design_identities.py（球面デザインの恒等式）は整合性の検査である。

実装の点検（この中で行う）:
  - 群の元 12,180 個が mod 2 で相異なること、生成元を掛けても閉じていること。
  - 標準形が群の作用で不変なこと（乱数の類 × 乱数の元）。
  - 表引き（バイト表）による c·s が、素朴な行列積と一致すること。
  - (6,6) 型: 最小ベクトルの代表 656 個で同じ検査。貼り合わせが恒等写像なら全部衝突するはず（陽性対照）。

実行（リポジトリの根から）: python3 -I code/crosscheck/second_impl/even_classes.py [C] [B]
  C = 本論文の tau（data/tau.txt）、B = 陰性対照の貼り方 B（certificates/negative_control_B.npz）
期待値: K8 は 1,517,130 種、K6 は 656 種、陽性対照は 656 / 656。C ではどちらの向きでも (6,6)・(6,8)・(8,8) 型の衝突が 0。
B では (8,8) 型の衝突がある（陰性対照）。一つでも外れれば終了コード 1 で終わる。
Expected: |K8| = 1,517,130, |K6| = 656, positive control 656 / 656; for C no collision of type (6,6), (6,8) or (8,8)
in either direction; for B some collision of type (8,8) (negative control). Exit code 1 if any of these fails.

公開用の注記: 公開リポジトリ向けに変えたのは入力（data/ の 4 ファイルと
certificates/ の検証用データを読む。中心化群の元は Sage で求め直さず certificates/centralizer.npz から読む）だけで、検査そのものは変えていない。
Release note: for the public repository only the inputs were changed (the four files of data/ and the
certificate files of certificates/ are read; the centralizer elements are read from
certificates/centralizer.npz instead of being recomputed with Sage). The checks are unchanged.
Shares no code with code/lib or code/verify. Needs only numpy.
"""
import sys, time
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


g_ = _ints(DATA / "L56_gram.txt")
h_ = _ints(DATA / "sl2_29_generators.txt").reshape(2, -1)
classes = sys.argv[1:] or ["C"]
if not set(classes) <= {"C", "B"}:
    sys.exit(f"unknown gluing {classes}: use C and/or B / 貼り方は C か B")
n = 56; t0 = time.time()
Gn = np.array(g_, dtype=np.int64).reshape(n, n)
H = [np.array(h, dtype=np.int64).reshape(n, n) for h in h_]
units = [u.astype(np.int64) for u in _npz("centralizer.npz", "units")]
W = (np.uint64(1) << np.arange(n, dtype=np.uint64))


def pack(V):
    """整数ベクトル（行）の配列 → mod 2 の類を表す 56 ビット整数。"""
    return ((np.asarray(V) % 2).astype(np.uint64) * W).sum(axis=-1)


# --- 群 SL_2(29)/± を mod 2 の行列として列挙（幅優先）。mod 2 で忠実なことも同時に確かめる ---
H2 = [h % 2 for h in H]
E0 = np.eye(n, dtype=np.int64); seen = {pack(E0).tobytes(): E0}; frontier = [E0]
while frontier:
    new = []
    for g in frontier:
        for h in H2:
            p = (g @ h) % 2; k = pack(p).tobytes()
            if k not in seen:
                seen[k] = p; new.append(p)
    frontier = new
S2 = np.stack(list(seen.values()))
check("|PSL_2(29)| = 12180 distinct elements mod 2", len(S2) == 12180)   # mod 2 で相異なる
if FAILS:
    finish()
rows = pack(S2)                                        # (12180, 56): 元 s の第 i 行（56 ビット）
# バイト表: T[s, b, v] = XOR_{k: v のビット k} rows[s, 8b + k]
T = np.zeros((len(S2), 7, 256), dtype=np.uint64)
for b in range(7):
    for v in range(1, 256):
        low = v & (-v); k = low.bit_length() - 1
        T[:, b, v] = T[:, b, v ^ low] ^ rows[:, 8 * b + k]
SH = (np.uint64(8) * np.arange(7, dtype=np.uint64))


def images(c):
    """類の配列 c（長さ m）→ (12180, m): 各群元で動かした像 c·s。"""
    by = ((c[None, :] >> SH[:, None]) & np.uint64(255)).astype(np.intp)       # (7, m)
    out = T[:, 0, by[0]]
    for b in range(1, 7):
        out = out ^ T[:, b, by[b]]
    return out


def canon(c, batch=512):
    c = np.asarray(c, dtype=np.uint64); out = np.empty(len(c), dtype=np.uint64)
    for i in range(0, len(c), batch):
        out[i:i + batch] = images(c[i:i + batch]).min(axis=0)
    return out


# --- 実装の点検 ---
rng = np.random.default_rng(11)
v = rng.integers(0, 2, size=(40, n)); idx = rng.integers(0, len(S2), size=40)
naive = pack(np.einsum("ij,ijk->ik", v, S2[idx]) % 2)
assert (images(pack(v))[idx, np.arange(40)] == naive).all(), "表引きが行列積と合わない"
cv = canon(pack(v)); assert (canon(naive) == cv).all(), "標準形が群の作用で不変でない"
print(f"群 12180 元（mod 2 で相異）、単数 {len(units)} 個。表引きと標準形の点検 ok  [{round(time.time() - t0)} s]", flush=True)

R8 = _npz("norm8_reps.npz", "reps").astype(np.int64)
R6 = _npz("min_reps.npz", "reps").astype(np.int64)
check("the norm-8 representatives have norm 8 and the minimal ones norm 6",
      ((R8 @ Gn) * R8).sum(axis=1).tolist() == [8] * len(R8) and ((R6 @ Gn) * R6).sum(axis=1).tolist() == [6] * len(R6))
XU = np.concatenate([R8 @ u for u in units])           # (r u) の全体。1,527,984 個
K8 = set(canon(pack(XU)).tolist())
K6 = set(canon(pack(R6)).tolist())
print(f"ノルム 8: (代表, 単数) の組 {len(XU)} 個、類の標準形 {len(K8)} 種。ノルム 6: 代表 {len(R6)} 個、標準形 {len(K6)} 種  [{round(time.time() - t0)} s]", flush=True)
ctrl = sum(c in K6 for c in canon(pack(R6)).tolist())
print(f"陽性対照（恒等写像で貼る）: (6,6) 型の衝突 {ctrl} / {len(R6)}", flush=True)
check("1,527,984 pairs (r, u) with 1,517,130 class canonical forms; 656 forms of norm 6", (len(XU), len(K8), len(K6)) == (1527984, 1517130, 656))
check("positive control (identity gluing): 656 / 656 collisions of type (6,6)", ctrl == len(R6) == 656)

for K in classes:
    Xn = _ints(DATA / "tau.txt").reshape(n, n) if K == "C" else _npz("negative_control_B.npz", "tau_class_B").astype(np.int64)
    # Inverse modulo 2: tau^2 = -5 = 1 (mod 2) for both gluings, checked here. / 2 を法とした逆: どちらの貼り方も tau^2 ≡ 1 (mod 2)。ここで確かめる。
    check(f"{K}: X^2 ≡ 1 (mod 2)", ((Xn @ Xn - np.eye(n, dtype=np.int64)) % 2 == 0).all())
    Xi = Xn % 2
    comm = all(((Xn @ h - h @ Xn) % 2 == 0).all() for h in H)
    print(f"類 {K}: X は SL_2(29) の生成元と mod 2 で可換: {comm}", flush=True)
    check(f"{K}: X commutes with the generators of SL_2(29) mod 2", comm)
    hits88 = 0
    for name, M in (("f", Xn), ("f^-1", Xi)):
        c66 = canon(pack(R6 @ M)); h66 = sum(c in K6 for c in c66.tolist())
        c68 = sum(c in K8 for c in c66.tolist())                      # (6,8) 型は L_f が偶なので起きないはず（整合性の点検）
        c88 = canon(pack(XU @ M)); hit = [i for i, c in enumerate(c88.tolist()) if c in K8]
        orbs = {int(canon(pack(XU[i:i + 1]))[0]) for i in hit}
        print(f"  類 {K} 向き {name}: (6,6) 型 {h66} / {len(R6)}; (6,8) 型 {c68}（0 のはず）; "
              f"(8,8) 型: {len(XU)} 組のうち衝突 {len(hit)} 組、x の SL_2(29)-軌道 {len(orbs)} 個  [{round(time.time() - t0)} s]", flush=True)
        hits88 += len(hit)
        if K == "C":
            check(f"C, direction {name}: no collision of type (6,6), (6,8) or (8,8)", h66 == 0 and c68 == 0 and len(hit) == 0)
    if K == "B":
        check("B (negative control): some collision of type (8,8) is found", hits88 > 0)
finish()
