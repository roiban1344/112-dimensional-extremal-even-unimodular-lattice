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
import math
import os
import shutil
import subprocess

from . import exact, require

_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "verify", "enum_interval.c")
_FLAGS = ["-O2", "-std=c11", "-fno-fast-math", "-ffp-contract=off"]

# The compiler used by compile_enumerator in this run, with the SHA-256 of the compiled source and of the executable
# (recorded by report.Report as "compiler"), or None.
# この実行で compile_enumerator が使ったコンパイラと、コンパイルしたソース・実行ファイルの SHA-256（report.Report が "compiler"
# として記録する）。無ければ None。
COMPILED = None


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
    hash of the source, the compiler (resolved path and version) and the flags, so a cached executable is reused
    only for exactly the same source and compiler, and the recorded compiler is the one that built it; `force`
    recompiles anyway.
    verify/enum_interval.c を build_dir にコンパイルし、実行ファイルを返す。ファイル名にソース・コンパイラ（解決したパスと版）・
    オプションのハッシュを含めるので、キャッシュした実行ファイルを再利用するのは、まったく同じソースとコンパイラのときだけで、記録するコンパイラは実際に作ったものになる。
    `force` なら常にコンパイルし直す。"""
    global COMPILED
    cc = c_compiler()
    try:
        version = subprocess.run([cc, "--version"], capture_output=True, text=True, timeout=60).stdout.splitlines()[0]
    except (OSError, subprocess.SubprocessError, IndexError):
        version = None
    COMPILED = {"command": cc, "path": shutil.which(cc), "version": version, "flags": _FLAGS}
    # Compile a copy of exactly the bytes that are hashed, so that the recorded hash is that of the compiled source.
    # ハッシュを取ったバイト列そのものの写しをコンパイルする。記録するハッシュがコンパイルしたソースのものになる。
    with open(_SRC, "rb") as f:
        src = f.read()
    src_sha = hashlib.sha256(src).hexdigest()
    h = hashlib.sha256(src)
    resolved = shutil.which(cc) or cc
    h.update("\0".join([resolved, os.path.realpath(resolved), version or ""] + _FLAGS).encode())
    exe = os.path.join(build_dir, "enum_interval-" + h.hexdigest()[:16])
    os.makedirs(build_dir, exist_ok=True)
    if force or not os.path.exists(exe):
        tmp = f"{exe}.{os.getpid()}.tmp"
        src_copy = tmp + ".c"
        with open(src_copy, "wb") as f:
            f.write(src)
        try:
            subprocess.run([cc] + _FLAGS + ["-o", tmp, src_copy, "-lm"], check=True)
        finally:
            os.remove(src_copy)
        os.replace(tmp, exe)
    with open(exe, "rb") as f:
        exe_sha = hashlib.sha256(f.read()).hexdigest()
    COMPILED.update({"source": os.path.relpath(_SRC, os.path.dirname(os.path.dirname(os.path.dirname(_SRC)))),
                     "source_sha256": src_sha, "executable_sha256": exe_sha})
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
        lines.append(f"{lo.hex()} {hi.hex()}")      # exact in C (scanf "%lf" reads hexadecimal floats) / C で厳密に読める
    for i in range(n):
        for j in range(i + 1, n):
            lo, hi = interval(V[i][j])
            lines.append(f"{lo.hex()} {hi.hex()}")
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
