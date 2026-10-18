"""The minimal vectors of L and inner products with them (paper §5, Check 5.4 (c)).
L の最小ベクトルと、それとの内積（論文 §5、検査 5.4 (c)）。

The 15,590,400 minimal vectors are the S-orbits of the 656 representatives of F2.
Since -1 is in G, it suffices to keep one of each pair +-u: the set
    V = { sign-normalized r_j s : j < 656, s in S/{+-1} }
has 7,795,200 elements, which is checked when it is built. For a certificate
we need max_{u in L_6} |<w, u>| = max_{v in V} |<w, v>|.
15,590,400 本の最小ベクトルは、F2 の 656 個の代表の S-軌道。-1 ∈ S なので ±u の片方だけ持てばよい。
    V = { r_j s の符号を正規化したもの : j < 656, s ∈ S/{±1} }
は 7,795,200 個で、作るときにこの個数を確かめる。certificate に必要なのは max_{u ∈ L_6} |<w, u>| = max_{v ∈ V} |<w, v>|。

Exactness: the products V @ (G W^T) are computed in float32 in blocks; for every block
the bound of lib.exact (all partial sums < 2^24) is checked, so the results are exact.
厳密さ: V @ (G W^T) はブロックごとに float32 で計算する。各ブロックで lib.exact の上界（部分和がすべて 2^24 未満）を確かめるので、結果は厳密。
"""
import hashlib
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from . import certs, exact, require
from .data import sha256_file

# |L_6| and |L_8|: coefficients of the extremal theta series in dimension 56, derived in verify/v2_theta.py.
# |L_6| と |L_8|: 56 次元の極値テータ級数の係数。verify/v2_theta.py で導く。
N6 = 15590400
N8 = 36957286800


def expand_half_shell(reps, S):
    """V = one of each pair +-u of the vectors r s (r in reps, s in S), as int16 (k, 56).
    Duplicates inside one orbit (from a nontrivial stabilizer) are removed; the caller
    checks that different orbits do not overlap (see `MinimalVectors`).
    r s（r ∈ reps, s ∈ S）の ±u の片方ずつ（int16 (k, 56)）。1 つの軌道の中の重複（固定群が自明でないときに生じる）は除く。
    異なる軌道が重ならないことは呼び出し側で確かめる（`MinimalVectors`）。"""
    S = np.asarray(S)
    S32 = S.astype(np.float32)
    smax = int(np.abs(S).max())
    parts = []
    for r in np.asarray(reps, dtype=np.int64):
        # r s in float32 is exact if sum_j |r_j| max|s| < 2^24. / 厳密さの条件を確かめる。
        require(int(np.abs(r).sum()) * smax < 2 ** 24, "float32 product r s would not be exact")
        Y = np.rint(r.astype(np.float32) @ S32).astype(np.int64)            # (|S|, 56)
        # Normalize the sign: first nonzero coordinate positive. / 符号の正規化: 最初の 0 でない座標を正に。
        first = (Y != 0).argmax(axis=1)
        sgn = np.sign(Y[np.arange(len(Y)), first])
        require((sgn != 0).all(), "zero vector in an orbit")
        parts.append(np.unique((Y * sgn[:, None]).astype(np.int16), axis=0))
    return np.concatenate(parts)


def count_distinct_rows(V, seed=20261017):
    """Number of distinct 64-bit hashes of the rows of V. Equal rows have equal hashes, so
    this is at most the number of distinct rows; if it equals len(V), all rows are distinct.
    V の行の 64 ビットのハッシュの種類数。等しい行は等しいハッシュをもつので、これは相異なる行の数以下。
    len(V) に等しければ、すべての行は相異なる。"""
    rng = np.random.default_rng(seed)
    h = rng.integers(1, 2 ** 62, size=V.shape[1], dtype=np.int64) | 1
    # int64 matrix products wrap around modulo 2^64; that is fine for hashing. Blocks keep memory small.
    # int64 の行列積は 2^64 を法として回り込むが、ハッシュとしては問題ない。ブロックに分けてメモリを抑える。
    keys = np.concatenate([V[i:i + (1 << 20)].astype(np.int64) @ h for i in range(0, len(V), 1 << 20)])
    return len(np.unique(keys))


class MinimalVectors:
    """All minimal vectors of L (one of each +-pair) and maximal inner products with them.
    L のすべての最小ベクトル（±の片方ずつ）と、それとの内積の最大。"""

    def __init__(self, G, reps, S):
        self.G = np.asarray(G, dtype=np.int64)
        self.V = expand_half_shell(reps, S)
        require(2 * len(self.V) == N6, f"{2 * len(self.V)} minimal vectors, expected {N6}")
        require(count_distinct_rows(self.V) == len(self.V), "two orbits overlap")
        # Every expanded vector has norm 6 (checked exactly in int64).
        # 展開したベクトルがすべてノルム 6 であることを int64 で厳密に確かめる。
        require((exact.norms(self.V, self.G) == 6).all(), "an expanded vector does not have norm 6")
        self.count = len(self.V)
        self.vmax = int(np.abs(self.V).max())

    def max_abs_inner(self, W, threads=1, block_w=512, block_v=1 << 16):
        """For each row w of W (int, (m, 56)): max over all minimal vectors u of |<w, u>|.
        The rows of W are processed in blocks of `block_w`, in `threads` Python threads
        (numpy releases the GIL inside matrix products; set the BLAS to one thread then).
        W の各行 w について、すべての最小ベクトル u にわたる |<w, u>| の最大。
        W の行を `block_w` 行ずつ、`threads` 本の Python のスレッドで処理する（numpy は行列積の中で GIL を手放す。
        そのときは BLAS を 1 スレッドにする）。"""
        GW = exact.i64_matmul(np.asarray(W, dtype=np.int64), self.G)          # (m, 56): rows w G
        # (w, u) = (w G) . u; every partial sum is bounded by sum_k |(wG)_k| |u_k|.
        # (w, u) = (w G)·u。部分和はすべて Σ_k |(wG)_k||u_k| で抑えられる。
        bound = exact.max_row_l1(GW) * self.vmax
        require(bound < 2 ** 24, f"float32 product would not be exact (bound {bound})")
        A = GW.astype(np.float32)
        V = self.V

        def run(Ab):
            buf = np.empty((len(Ab), block_v), dtype=np.float32)
            hi = np.full(len(Ab), -np.inf, dtype=np.float32)
            lo = np.full(len(Ab), np.inf, dtype=np.float32)
            for i in range(0, len(V), block_v):
                # V is kept as int16 and converted per block (exact; saves 1.75 GB).
                # V は int16 で持ち、ブロックごとに変換する（厳密。1.75 GB の節約）。
                Vb = V[i:i + block_v].astype(np.float32)
                out = buf[:, :len(Vb)]
                np.matmul(Ab, Vb.T, out=out)
                np.maximum(hi, out.max(axis=1), out=hi)
                np.minimum(lo, out.min(axis=1), out=lo)
            return np.maximum(hi, -lo)

        blocks = [A[i:i + block_w] for i in range(0, len(A), block_w)]
        if threads > 1:
            with ThreadPoolExecutor(threads) as ex:
                res = list(ex.map(run, blocks))
        else:
            res = [run(b) for b in blocks]
        r = np.concatenate(res)
        ri = np.rint(r).astype(np.int64)
        require((ri.astype(np.float32) == r).all(), "non-integral float32 inner product")
        return ri


def fingerprint(W, files, extra):
    """What a checkpoint of (c) depends on, as a JSON string: the shape, dtype and SHA-256 of the rows W
    that are checked, the SHA-256 of the given files (inputs and the code computing (c)), and `extra`
    (n, --limit, ...).
    (c) の途中経過が依存するもの（JSON 文字列）: 検査する行 W の形・型・SHA-256、与えたファイル（入力と (c) を計算するコード）の
    SHA-256、`extra`（n、--limit など）。"""
    W = np.ascontiguousarray(W)
    d = {"rows": list(W.shape), "dtype": str(W.dtype), "rows_sha256": hashlib.sha256(W.tobytes()).hexdigest(),
         "files": {os.path.basename(p): sha256_file(p) for p in files}}
    d.update(extra)
    return json.dumps(d, sort_keys=True)


CODE_FILES = [os.path.join(os.path.dirname(os.path.abspath(__file__)), f) for f in ("shells.py", "exact.py", "group.py")]


def max_abs_inner_checkpointed(mv, W, threads, chunk, state, fp, rep):
    """max |<w, u>| over all minimal vectors u, for every row w of W (integer array), in chunks of `chunk`
    rows, saving a checkpoint to the file `state` at most every 5 minutes, so that an interrupted run resumes.
    The checkpoint stores the fingerprint `fp` (see `fingerprint`). On resumption it must equal the
    fingerprint of the present run, else the run FAILS (rep.check) and the user is told to delete the
    file: a checkpoint made for other data or other code is never used, and is not deleted silently
    (it may be the result of many hours of computation for another data set). When all rows are done
    the checkpoint is removed, so a later run computes (c) from the start.
    Returns (mx, seconds spent, rows taken over from the checkpoint).
    W の各行 w について、すべての最小ベクトル u にわたる max |<w, u>|。`chunk` 行ずつ計算し、高々 5 分ごとに途中経過をファイル
    `state` に保存するので、中断しても再開できる。途中経過には指紋 `fp`（`fingerprint` を参照）を保存する。再開するときは、それが
    今回の実行の指紋と一致しなければならない。一致しなければ不合格（rep.check）とし、ファイルを消すよう利用者に示す。
    別のデータや別のコードのための途中経過を使うことはなく、黙って消すこともない（別のデータについての何時間分もの計算結果
    かもしれないので）。全行が終わったら途中経過を消すので、後の実行は (c) を最初から計算する。
    (mx, かかった秒数, 途中経過から引き継いだ行数) を返す。"""
    n = len(W)
    if os.path.exists(state):
        with np.load(state, allow_pickle=False) as z:
            saved = str(z["fingerprint"]) if "fingerprint" in z.files else None
            mx, done, secs = z["mx"].astype(np.int64), int(z["done"]), float(z["seconds"]) if "seconds" in z.files else 0.0
        if saved != fp:
            rep.log(f"the checkpoint {state} was made for other inputs, code or options; "
                    "delete it to compute (c) from the start / この途中経過は別の入力・コード・指定で作られた。"
                    "(c) を最初から計算するには、このファイルを消す")
            old = json.loads(saved) if saved else {}
            new = json.loads(fp)
            old.update({f"file {k}": v for k, v in old.pop("files", {}).items()})
            new.update({f"file {k}": v for k, v in new.pop("files", {}).items()})
            for k in sorted(set(old) | set(new)):
                if old.get(k) != new.get(k):
                    rep.log(f"  differs: {k}: checkpoint {old.get(k)}, this run {new.get(k)}")
        rep.check(f"the checkpoint {os.path.basename(state)} belongs to these inputs (SHA-256 of the rows, inputs and code; n)",
                  saved == fp and len(mx) == n and 0 <= done <= n)
        rep.log(f"resuming at {done} / {n}")
    else:
        mx, done, secs = np.full(n, -1, dtype=np.int64), 0, 0.0
    resumed = done
    last = time.time()
    while done < n:
        t1 = time.time()
        e = min(n, done + chunk)
        # int64: no wrap-around is possible (an int8 array would wrap values >= 128 silently).
        # int64 なので回り込みは起きない（int8 の配列なら 128 以上の値が黙って回り込む）。
        mx[done:e] = mv.max_abs_inner(W[done:e], threads=threads)
        secs += time.time() - t1
        done = e
        if time.time() - last > 300 and done < n:
            os.makedirs(os.path.dirname(state) or ".", exist_ok=True)
            certs.save_npz(state, mx=mx, done=np.int64(done), seconds=np.float64(secs), fingerprint=np.str_(fp))
            last = time.time()
            rep.log(f"(c) {done} / {n}: {1000 * secs / done:.1f} ms per row, max so far {int(mx[:done].max())}")
    rep.log(f"(c) {n} / {n} done" + (f": {1000 * secs / n:.1f} ms per row" if n else ""))
    if os.path.exists(state):
        os.remove(state)
    return mx, secs, resumed
