"""All vectors of norm <= B of a positive definite integral quadratic form, by the enumeration that
cannot miss vectors (verify/enum_interval.c: interval arithmetic, exact norms at the leaves).
正定値な整数二次形式のノルム B 以下の全ベクトル。取りこぼしの無い列挙（verify/enum_interval.c: 区間演算、葉では厳密なノルム）による。

Used by verify/v1_min_L.py (F1; `interval`, `compile_enumerator`, `run_enumerator`), and to check that
PARI's qfminim, whose documentation does not guarantee completeness, has returned every short vector:
produce/exact_qfminim.py calls `short_vectors` for the automorphisms of L_112 (paper §8, Table D2
[C24], through supplementary/_shared.py) and the centralizer of SL_2(29) in Aut(L)
(produce/p1_centralizer.py). supplementary/fixed_sublattices.py, anatomy_b.py and nebe/tables.py
call `short_vectors` directly.
verify/v1_min_L.py（F1。`interval`, `compile_enumerator`, `run_enumerator`）が使う。また、文書に完全性の保証が無い PARI の
qfminim が、短いベクトルをすべて返したことを確かめるのに使う: produce/exact_qfminim.py が `short_vectors` を呼び、
L_112 の自己同型（論文 §8、表 D2 の [C24]。supplementary/_shared.py 経由）と、Aut(L) における SL_2(29) の
中心化群（produce/p1_centralizer.py）に使う。supplementary/fixed_sublattices.py, anatomy_b.py, nebe/tables.py は
`short_vectors` を直接呼ぶ。

The caller should pass a reasonably reduced Gram matrix (the running time depends on it, the
correctness does not). Only one of each pair +-x is returned.
呼び出し側は、ある程度簡約した Gram 行列を渡すこと（実行時間はそれに依存するが、正しさは依存しない）。±x の片方だけを返す。
"""
import hashlib
import itertools
import math
import os
import shutil
import subprocess
from fractions import Fraction

from . import exact, require

_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "verify", "enum_interval.c")
_FLAGS = ["-O2", "-std=c11", "-fno-fast-math", "-ffp-contract=off"]


def interval(q):
    """[nextbelow(f), nextabove(f)] for f = float(q) (nearest rounding), containing the rational q.
    f = float(q)（最近接丸め）の両隣の区間。有理数 q を含む。"""
    f = float(q)                                  # nearest rounding / 最近接丸め
    lo, hi = math.nextafter(f, -math.inf), math.nextafter(f, math.inf)
    require(lo <= q <= hi, f"interval does not contain {q}")
    return lo, hi


def c_compiler():
    """$CC if set, otherwise the first of cc, gcc, clang on the PATH (a clang-only system has no gcc).
    $CC があればそれ、無ければ PATH にある cc, gcc, clang の最初のもの（clang しかない環境には gcc が無い）。"""
    if os.environ.get("CC"):
        return os.environ["CC"]
    for cc in ("cc", "gcc", "clang"):
        if shutil.which(cc):
            return cc
    raise RuntimeError("no C compiler found (set CC) / C コンパイラが見つからない（CC を指定する）")


def compile_enumerator(build_dir, force=False):
    """Compile verify/enum_interval.c into build_dir and return the executable. The file name contains a
    hash of the source, the compiler (resolved path) and the flags, so a cached executable is reused only
    for exactly the same source and compiler; `force` recompiles anyway.
    verify/enum_interval.c を build_dir にコンパイルし、実行ファイルを返す。ファイル名にソース・コンパイラ（解決したパス）・
    オプションのハッシュを含めるので、キャッシュした実行ファイルを再利用するのは、まったく同じソースとコンパイラのときだけ。
    `force` なら常にコンパイルし直す。"""
    cc = c_compiler()
    h = hashlib.sha256()
    with open(_SRC, "rb") as f:
        h.update(f.read())
    h.update("\0".join([shutil.which(cc) or cc] + _FLAGS).encode())
    exe = os.path.join(build_dir, "enum_interval-" + h.hexdigest()[:16])
    os.makedirs(build_dir, exist_ok=True)
    if force or not os.path.exists(exe):
        tmp = f"{exe}.{os.getpid()}.tmp"
        subprocess.run([cc] + _FLAGS + ["-o", tmp, _SRC, "-lm"], check=True)
        os.replace(tmp, exe)
    return exe


def enumerator_input(G, bound):
    """The input of enum_interval.c for the Gram matrix G and the radius `bound`: G and intervals
    containing the exact rational D_i and V_ij of G = V^T diag(D) V.
    Gram 行列 G と半径 `bound` に対する enum_interval.c の入力: G と、G = V^T diag(D) V の厳密な有理数 D_i, V_ij を含む区間。"""
    G = exact.to_int_matrix(G)
    n = len(G)
    D, V = exact.ldl_exact(G)
    lines = [f"{n} {int(bound)}"]
    lines += [" ".join(str(v) for v in row) for row in G]
    for d in D:
        lo, hi = interval(d)
        lines.append(f"{lo!r} {hi!r}")
    for i in range(n):
        for j in range(i + 1, n):
            lo, hi = interval(V[i][j])
            lines.append(f"{lo!r} {hi!r}")
    return "\n".join(lines) + "\n"


def run_enumerator(exe, G, bound, max_print=5):
    """Run the enumerator; returns a dict with "counts" {norm: number of nonzero vectors (both signs)},
    "vectors" [(x, norm)] (one of each +-pair, at most max_print), "nodes" and "leaves".
    Checks that the enumerator finished and that no leaf of norm <= bound fell outside its table.
    列挙器を走らせ、"counts" {ノルム: 0 でないベクトルの本数（両符号）}、"vectors" [(x, ノルム)]（±の片方。max_print 本まで）、
    "nodes", "leaves" をもつ dict を返す。列挙器が最後まで走ったことと、ノルム bound 以下の葉が表の範囲外に落ちなかったことを確かめる。"""
    proc = subprocess.run([exe, str(max_print)], input=enumerator_input(G, bound),
                          stdout=subprocess.PIPE, text=True, check=True)
    res = {"counts": {}, "vectors": [], "nodes": None, "leaves": None, "untabulated": None}
    for line in proc.stdout.splitlines():
        if line.startswith("vector of norm"):
            head, coords = line.split(":")
            res["vectors"].append(([int(t) for t in coords.split()], int(head.split()[-1])))
        elif line.startswith("nodes"):
            parts = line.split()
            res["nodes"], res["leaves"] = int(parts[1]), int(parts[3])
        elif line.startswith("nonzero vectors of norm"):
            q, c = line[len("nonzero vectors of norm "):].split(":")
            res["counts"][int(q)] = int(c)
        elif line.startswith("untabulated"):
            res["untabulated"] = int(line.split(":")[1])
    require(proc.stdout.rstrip().endswith("done"), "enumerator did not finish")
    require(res["untabulated"] == 0, f"{res['untabulated']} vectors of norm <= {bound} outside the table of the enumerator")
    return res


def short_vectors(G, bound, build_dir, max_vectors=10 ** 7):
    """[(x, norm)] for all nonzero x (one of each +-pair) with x G x^T <= bound; G is a list of lists of
    integers (or an integer array). Returns also the number of enumeration nodes.
    x G x^T ≤ bound となる 0 でないすべての x（±の片方）と、そのノルム。列挙の節点数も返す。"""
    res = run_enumerator(compile_enumerator(build_dir), G, bound, max_vectors)
    total = sum(res["counts"].values()) // 2
    require(len(res["vectors"]) == total, "more vectors than max_vectors")
    return res["vectors"], res["nodes"]


def exhaustive_short_vectors(G, bound):
    """All nonzero x with x G x^T <= bound, one of each +-pair (the last nonzero coordinate positive), by
    exhaustive search in the box |x_i| <= sqrt(bound (G^-1)_ii) (Cauchy-Schwarz), with (G^-1)_ii computed
    exactly. Integer arithmetic only; for small dimensions (the box has prod (2 b_i + 1) points).
    x G x^T ≤ bound となる 0 でないすべての x（±の片方。最後の 0 でない座標が正）を、箱 |x_i| ≤ √(bound (G^-1)_ii)
    （Cauchy-Schwarz）の中の総当たりで求める。(G^-1)_ii は厳密に計算する。整数演算だけ。小さい次元用（箱の点は Π (2 b_i + 1) 個）。"""
    G = exact.to_int_matrix(G)
    n = len(G)
    D, V = exact.ldl_exact(G)                         # G = V^T diag(D) V, V unit upper triangular
    # (G^-1)_ii = sum_k (V^-1)_ik^2 / D_k, with V^-1 computed by back substitution over the rationals.
    Vinv = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for j in range(n):
        for i in range(j - 1, -1, -1):
            Vinv[i][j] = -sum(V[i][k] * Vinv[k][j] for k in range(i + 1, j + 1))
    box = []
    for i in range(n):
        gii = sum(Vinv[i][k] ** 2 / D[k] for k in range(n))
        box.append(math.isqrt(int(bound * gii)) + 1)
    out = []
    for x in itertools.product(*[range(-b, b + 1) for b in box]):
        if not any(x):
            continue
        last = next(v for v in reversed(x) if v)
        if last < 0:
            continue
        q = sum(x[i] * G[i][j] * x[j] for i in range(n) for j in range(n))
        if q <= bound:
            out.append((tuple(x), q))
    return sorted(out)


def random_forms_mismatches(exe, trials=60, seed=7):
    """Compare the enumerator with exhaustive search on `trials` random positive definite forms
    G = B B^T + I (dimension 2-5, entries of B in -3..3, radius 1-14), whose short vectors include vectors of
    norm exactly equal to the radius. Returns (number of forms on which they differ, number of +- pairs found,
    number of them of norm equal to the radius).
    列挙器を、`trials` 個の無作為に生成した正定値二次形式 G = B B^T + I（2〜5 次元、B の成分は -3..3、半径 1〜14）での総当たりと比べる。
    短いベクトルには、ノルムがちょうど半径に等しいものも含まれる。返り値は（食い違った形式の数、見つかった ± の対の数、
    そのうちノルムが半径に等しいものの数）。"""
    import numpy as np
    rng = np.random.default_rng(seed)
    bad = found = on_boundary = 0
    for _ in range(trials):
        n = int(rng.integers(2, 6))
        B = rng.integers(-3, 4, size=(n, n))
        G = (B @ B.T + np.eye(n, dtype=np.int64)).tolist()
        bound = int(rng.integers(1, 15))
        exp = exhaustive_short_vectors(G, bound)
        res = run_enumerator(exe, G, bound, max_print=10 ** 6)
        canon = lambda x: x if next(v for v in reversed(x) if v) > 0 else tuple(-v for v in x)  # noqa: E731
        got = sorted((canon(tuple(x)), q) for x, q in res["vectors"])
        bad += got != exp
        found += len(exp)
        on_boundary += sum(q == bound for _, q in exp)
    return bad, found, on_boundary


def skewed_basis_mismatches(exe, G, bound, expected, trials=5, seed=5, steps=40, c=2):
    """Run the enumerator on U G U^T for `trials` random unimodular U (products of `steps` elementary row
    operations with multipliers in -c..c) and count the bases for which the numbers of vectors by norm differ
    from `expected`. The entries of U G U^T are large, so the rounding of the floating-point bounds matters:
    with G = E_8 and radius 4 this detects the removal of the outward rounding from the enumerator, which the
    lattice controls in a reduced basis do not (code/tests/test_enumerate.py compiles such an enumerator).
    `trials` 個の乱数のユニモジュラー行列 U（係数 -c..c の基本変形 `steps` 回の積）について U G U^T で列挙器を走らせ、ノルムごとの
    本数が `expected` と違う基底の数を数える。U G U^T の成分は大きいので、浮動小数点の上界の丸めが効く。G = E_8、半径 4 なら、
    列挙器から外向きの丸めを外したことを検出する。簡約した基底での格子の対照では検出できない（code/tests/test_enumerate.py でそのような列挙器をコンパイルして確かめる）。"""
    import numpy as np
    rng = np.random.default_rng(seed)
    G = np.asarray(exact.to_int_matrix(G), dtype=np.int64)
    n = len(G)
    bad = 0
    for _ in range(trials):
        U = np.eye(n, dtype=np.int64)
        for _ in range(steps):
            i, j = rng.choice(n, 2, replace=False)
            U[i] += int(rng.integers(-c, c + 1)) * U[j]
        Gs = exact.i64_matmul(exact.i64_matmul(U, G), U.T)
        bad += run_enumerator(exe, Gs, bound)["counts"] != expected
    return bad
