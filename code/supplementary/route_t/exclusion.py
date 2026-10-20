r"""S28. Route T, the final step: every dangerous support module contains a configuration excluded by F5a or F5b
(supplement §S4.1, Proposition S4.3; Table D2 [C32]). Not used in the proof of Theorem A.
S28. 経路 T の最後の段: 危険な台加群はどれも F5a か F5b に反する配置を含む（補遺 §S4.1 の命題 S4.3、表 D2 の [C32]）。
定理 A の証明には使わない。

The range is that of Proposition S4.2: pseudo-bases N = A x + B y with A, B in {O, p2^-1}, 3 <= a = h(x) <= 6,
b = h(y) >= a, c = h(x, y) = p/2 - (q/10) sqrt(-5) with |p| <= m a, |q| <= 5 m a (m = 2 for (A, B) = (O, p2^-1),
otherwise 1), det_h N <= 4. Among the N with even integral trace form, tau integral and real minimum >= 6, the
dangerous ones (H (x) N has a nonzero vector of norm <= 8) each get one witness, in the coordinates of the
Z-basis (alpha_1 x, alpha_2 x, beta_1 y, beta_2 y):
  s1:    x, w with <x,x> = <w,w> = 8 and w = x tau (mod 2N)          (contradicts F5b)
  s3tau: u, w with <u,u> = 6, 0 < <w,w> <= 10 and w = u tau (mod 2N) (contradicts F5a)
命題 S4.2 の範囲（上の英文）で、トレース形式が偶・整数、τ が整数行列、実の最小 6 以上の N のうち、危険なもの（H ⊗ N にノルム 8 以下の
0 でないベクトル）それぞれに、擬基底の Z-基底 (α₁x, α₂x, β₁y, β₂y) の座標で証拠を 1 つ付ける。形は上の s1（F5b に反する）か s3tau
（F5a に反する）。

  check  (Python standard library only) enumerates the range itself, builds the real Gram matrix and tau itself,
         decides the minimum and dangerousness by its own short-vector enumeration (pairwise reduction, then the
         box x_i^2 <= B (G^-1)_ii), and checks the witness of every dangerous N in integers. It accepts only the
         forms s1 and s3tau, and counts them. Expected: 63,996 parameters, 1,171 valid N, 631 dangerous, 631
         checked (s1 541, s3tau 90), 0 failed, no extra or duplicate rows. About 8 minutes.
         （Python の標準ライブラリだけ）範囲を自分で回し、実 Gram と τ を自分で作り、最小と危険かどうかを自前の短いベクトルの列挙
         （対ごとの簡約のあと箱 x_i² ≤ B(G⁻¹)_ii をしらみつぶし）で判定し、危険な N すべての証拠を整数で確かめる。受け付ける形は
         s1 と s3tau だけで、その数も数える。期待: パラメータ 63,996、有効な N 1,171、危険 631、検算 631（s1 541、s3tau 90）、
         失敗 0、余分な行・重複 0。約 8 分。
  make   (SageMath, for LLL only) produces the witnesses with the exact rational Fincke-Pohst enumeration of
         recount.py, writes out/route_t/exclusion.json and compares it with the distributed file.
         （SageMath。LLL だけ）recount.py の有理数の Fincke–Pohst 列挙で証拠を作り、out/route_t/exclusion.json に書き、配布ファイルと比べる。

The two enumerations are different code; check does not use anything computed by make except the witnesses.
検算（check）は作成（make）の結果を証拠の座標にしか使わない。列挙も別のコード。

Input: certificates/route_t_exclusion.json (checked against certificates/SHA256SUMS).
Report: out/s28_route_t_exclusion_<check|make>.json; exit code 1 on a mismatch.
Run / 実行:  python3 -I code/supplementary/route_t/exclusion.py check [--certificates DIR] [--out DIR]
             python3 -I code/supplementary/route_t/exclusion.py make [--out DIR]   (Python with SageMath / SageMath を含む Python)
"""
import argparse
import hashlib
import itertools
import json
import os
import sys
from fractions import Fraction as Fr
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from lib.report import Report  # noqa: E402

CERT = "route_t_exclusion.json"
EXPECTED = dict(params=63996, valid_N=1171, dangerous=631, checked=631, fail=0, types={"s1": 541, "s3tau": 90},
                extra=0, dup=0)
ALLOWED = ("s1", "s3tau")

# K = Q(sqrt(-5)): (r, s) = r + s sqrt(-5) / K の元 (r, s) = r + s√-5
def km(u, v): return (u[0] * v[0] - 5 * u[1] * v[1], u[0] * v[1] + u[1] * v[0])
def kc(u): return (u[0], -u[1])
def kn(u): return u[0] * u[0] + 5 * u[1] * u[1]
def kt(u): return 2 * u[0]


ZB = {"O": [(Fr(1), Fr(0)), (Fr(0), Fr(1))], "P": [(Fr(1), Fr(0)), (Fr(1, 2), Fr(1, 2))]}   # P = p2^-1
NI = {"O": Fr(1), "P": Fr(1, 2)}                                                            # norms of the ideals
HM = [[(Fr(3), Fr(0)), (Fr(0), Fr(1))], [(Fr(0), Fr(-1)), (Fr(2), Fr(0))]]                  # Gram of H


def zcoords(u, ideal):
    (a, b), (c, d) = ZB[ideal]; det = a * d - b * c
    return ((u[0] * d - u[1] * c) / det, (a * u[1] - b * u[0]) / det)


def structure(Hm, ideals):
    """Real Gram matrix and tau (acting on row vectors) in the Z-basis of a pseudo-basis.
    擬基底のエルミート Gram と係数イデアル → Z-基底での実 Gram と τ（行ベクトルへの作用）。"""
    basis = [(i, g) for i, ideal in enumerate(ideals) for g in ZB[ideal]]
    n = len(basis)
    G = [[kt(km(km(g, kc(g2)), Hm[i][i2])) for (i2, g2) in basis] for (i, g) in basis]
    T = [[Fr(0)] * n for _ in range(n)]
    for k, (i, g) in enumerate(basis):
        T[k][2 * i], T[k][2 * i + 1] = zcoords(km((Fr(0), Fr(1)), g), ideals[i])
    return G, T


def det(M):
    M = [list(map(Fr, r)) for r in M]; n = len(M); d = Fr(1)
    for i in range(n):
        piv = next((r for r in range(i, n) if M[r][i] != 0), None)
        if piv is None:
            return Fr(0)
        if piv != i:
            M[i], M[piv] = M[piv], M[i]; d = -d
        d *= M[i][i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            for c in range(i, n):
                M[r][c] -= f * M[i][c]
    return d


def inverse(M):
    n = len(M); A = [list(map(Fr, r)) + [Fr(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for i in range(n):
        piv = next(r for r in range(i, n) if A[r][i] != 0); A[i], A[piv] = A[piv], A[i]
        p = A[i][i]; A[i] = [x / p for x in A[i]]
        for r in range(n):
            if r != i and A[r][i] != 0:
                f = A[r][i]; A[r] = [x - f * y for x, y in zip(A[r], A[i])]
    return [r[n:] for r in A]


def posdef(G):
    return all(det([r[:k] for r in G[:k]]) > 0 for k in range(1, len(G) + 1))


def qf(G, v):
    return sum(G[i][j] * v[i] * v[j] for i in range(len(v)) for j in range(len(v)))


def pair_reduce(G):
    """Pairwise reduction; returns (G', U) with G' = U G U^T. A step b_i -= t b_j (t = round(G_ij/G_jj)) is made
    only when 2|G_ij| > G_jj; then |r - t| <= 1/2 < |r| for r = G_ij/G_jj, so G_ii strictly decreases and the
    loop stops. Correctness does not depend on it (det U = +-1 is checked).
    対ごとの簡約。2|G_ij| > G_jj のときだけ b_i から t b_j（t = round(G_ij/G_jj)）を引く。r = G_ij/G_jj について |r − t| ≤ 1/2 < |r|
    なので G_ii は真に減り、有限回で止まる。正しさは簡約に依らない（det U = ±1 を確認）。"""
    n = len(G); G = [r[:] for r in G]; U = [[int(i == j) for j in range(n)] for i in range(n)]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                t = round(Fr(G[i][j]) / G[j][j])
                if t == 0 or 2 * abs(G[i][j]) <= G[j][j]:
                    continue
                U[i] = [x - t * y for x, y in zip(U[i], U[j])]
                for k in range(n):
                    G[i][k] -= t * G[j][k]
                for k in range(n):
                    G[k][i] -= t * G[k][j]
                changed = True
    if det(U) not in (1, -1):
        raise RuntimeError("pair_reduce: the basis change is not unimodular")
    return G, U


def short(G, B):
    """Integer vectors with 0 < v^T G v <= B, in the coordinates of the original basis.
    0 < vᵀGv ≤ B の整数ベクトル（元の基底の座標）。"""
    Gr, U = pair_reduce(G); Gi = inverse(Gr); n = len(G)
    rng = []
    for i in range(n):
        r = B * Gi[i][i]; k = isqrt(r.numerator // r.denominator)
        while (k + 1) ** 2 <= r:
            k += 1
        rng.append(range(-k, k + 1))
    out = []
    for v in itertools.product(*rng):
        if any(v) and qf(Gr, v) <= B:
            out.append(tuple(sum(v[i] * U[i][j] for i in range(n)) for j in range(n)))
    return out


def parameters():
    """The range of Proposition S4.2 (a superset: non-shortest x and repeated N are included).
    命題 S4.2 の範囲（上集合: x が最短でないもの・同じ N の重複を含む）。"""
    for A, Bi in itertools.product("OP", repeat=2):
        m = 2 if (A, Bi) == ("O", "P") else 1
        for a in range(3, 7):
            for p in range(-m * a, m * a + 1):
                for q in range(-5 * m * a, 5 * m * a + 1):
                    c = (Fr(p, 2), Fr(-q, 10))
                    bmax = (4 / (NI[A] * NI[Bi]) + kn(c)) / a
                    b = a
                    while b <= bmax:
                        yield A, Bi, a, b, p, q, c
                        b += 1


def module(A, Bi, a, b, c):
    """(G, T, G_H) of a valid N (G, T integral, G even, positive definite, minimum >= 6), else None.
    有効な N なら (G, T, H ⊗ N の Gram)、そうでなければ None。"""
    Hn = [[(Fr(a), Fr(0)), c], [kc(c), (Fr(b), Fr(0))]]
    if kn(c) >= a * b:
        return None
    G, T = structure(Hn, [A, Bi])
    if any(x.denominator != 1 for r in G + T for x in r) or any(G[i][i] % 2 for i in range(4)):
        return None
    if det(G) > 6400 or not posdef(G):              # det <= 6400 holds by the bound on b (a redundant guard)
        return None
    G = [[int(x) for x in r] for r in G]; T = [[int(x) for x in r] for r in T]
    if short(G, 4):                                 # real minimum >= 6 / 実の最小 ≥ 6
        return None
    GH, _ = structure([[km(HM[i // 2][j // 2], Hn[i % 2][j % 2]) for j in range(4)] for i in range(4)], [A, Bi, A, Bi])
    if any(x.denominator != 1 for r in GH for x in r):
        raise RuntimeError(f"H (x) N has a non-integral Gram matrix: {A}, {Bi}, a = {a}, b = {b}, c = {c}")
    return G, T, [[int(x) for x in r] for r in GH]


def witness_ok(G, T, e):
    """Check one witness in integers; only the forms s1 and s3tau are accepted.
    証拠を 1 つ整数で確かめる。受け付ける形は s1 と s3tau だけ。"""
    if e.get("type") not in ALLOWED:
        return False
    isint = lambda v: isinstance(v, list) and len(v) == 4 and all(type(t) is int for t in v)
    if not (isint(e.get("x")) and isint(e.get("w"))):
        return False
    x, w = tuple(e["x"]), tuple(e["w"])
    xt = tuple(sum(x[i] * T[i][j] for i in range(4)) for j in range(4))
    if any((u - v) % 2 for u, v in zip(w, xt)):     # w = x tau (mod 2N)
        return False
    nx, nw = qf(G, x), qf(G, w)
    if e["type"] == "s1":
        return nx == 8 and nw == 8
    return nx == 6 and 0 < nw <= 10


def check(rep, directory):
    path = os.path.join(directory, CERT)
    sums = os.path.join(ROOT, "certificates", "SHA256SUMS")
    want = {ln.split()[1]: ln.split()[0] for ln in open(sums) if ln.strip()}
    got = hashlib.sha256(open(path, "rb").read()).hexdigest()
    rep.check(f"{CERT} matches certificates/SHA256SUMS", want.get(CERT) == got)
    table, dup = {}, 0
    for e in json.load(open(path))["entries"]:
        k = tuple(e["key"]); dup += k in table; table[k] = e
    st = dict(params=0, valid_N=0, dangerous=0, checked=0, fail=0)
    types, seen = {}, set()
    for A, Bi, a, b, p, q, c in parameters():
        st["params"] += 1
        mod = module(A, Bi, a, b, c)
        if mod is None:
            continue
        G, T, GH = mod
        st["valid_N"] += 1
        if not short(GH, 8):
            continue
        st["dangerous"] += 1
        key = (A, Bi, a, int(b), p, q); seen.add(key)
        e = table.get(key)
        if e is not None and witness_ok(G, T, e):
            st["checked"] += 1; types[e["type"]] = types.get(e["type"], 0) + 1
        else:
            st["fail"] += 1; rep.log(f"FAIL {key} {e}")
        if st["params"] % 4000 == 0:
            rep.log(f"  {st}")
    st["types"] = dict(sorted(types.items()))
    st["extra"] = len(set(table) - seen)            # rows for keys that are not dangerous or out of range
    st["dup"] = dup
    rep.value("parameters, valid N, dangerous, checked, failed, forms, extra rows, duplicate rows", st)
    rep.check("631 dangerous N, each with a witness of form s1 (541, contradicts F5b) or s3tau (90, contradicts F5a); "
              "63,996 parameters, 1,171 valid N; no failure, extra or duplicate row", st == EXPECTED)


def make(rep):
    """Produce the witnesses with recount.py's enumeration (not with short() of this file).
    証拠を recount.py の列挙で作る（このファイルの short() は使わない）。"""
    import recount as rc                            # exact rational Fincke-Pohst, Sage LLL / 有理数の Fincke–Pohst、Sage の LLL
    entries = []
    for A, Bi, a, b, p, q, c in parameters():
        Hn = [[(Fr(a), Fr(0)), c], [kc(c), (Fr(b), Fr(0))]]
        if kn(c) >= a * b:
            continue
        G, T = rc.real_structure(Hn, [A, Bi])
        if not (rc.is_int(G) and rc.is_int(T)) or any(G[i][i] % 2 for i in range(4)):
            continue
        G = [[int(x) for x in r] for r in G]; T = [[int(x) for x in r] for r in T]
        if rc.det_int(G) > 6400 or rc.short_vectors(rc.lll_basis(G)[0], 4):
            continue
        GH, _ = rc.real_structure(rc.kron(rc.H, Hn), [A, Bi, A, Bi])
        if rc.minimum_exact([[int(x) for x in r] for r in GH], 8)[0] is None:
            continue
        Gl, U = rc.lll_basis(G)
        Ut = [[int(x) for x in r] for r in U.transpose().rows()]
        V = [tuple(sum(v[i] * Ut[i][j] for i in range(4)) for j in range(4)) for v in rc.short_vectors(Gl, 10)]
        nrm = {v: rc.qf(G, v) for v in V}
        act = lambda v: tuple(sum(v[i] * T[i][j] for i in range(4)) for j in range(4))
        found = None
        for typ, n0, ok in (("s1", 8, lambda n: n == 8), ("s3tau", 6, lambda n: 0 < n <= 10)):
            for x in (v for v in V if nrm[v] == n0):
                xt = act(x)
                w = next((w for w in V if ok(nrm[w]) and all((s - t) % 2 == 0 for s, t in zip(w, xt))), None)
                if w is not None:
                    found = dict(type=typ, x=list(x), w=list(w)); break
            if found:
                break
        if found is None:
            rep.log(f"UNCOVERED {A} {Bi} {a} {b} {p} {q}")
            continue
        entries.append(dict(key=[A, Bi, a, int(b), p, q], **found))
    types = {}
    for e in entries:
        types[e["type"]] = types.get(e["type"], 0) + 1
    out_dir = os.path.join(rep.out_dir, "route_t"); os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "exclusion.json")
    with open(out + ".tmp", "w") as f:
        json.dump(dict(types=dict(sorted(types.items())), entries=entries), f)
    os.replace(out + ".tmp", out)
    rep.value("dangerous N with a witness, forms", [len(entries), dict(sorted(types.items()))])
    rep.check("631 witnesses (s1 541, s3tau 90)", len(entries) == 631 and types == EXPECTED["types"])
    dist = json.load(open(os.path.join(ROOT, "certificates", CERT)))["entries"]
    rep.check(f"out/route_t/exclusion.json has the same rows as certificates/{CERT}",
              sorted(map(json.dumps, entries)) == sorted(map(json.dumps, dist)))


def main():
    ap = argparse.ArgumentParser(description="S28: route T, the final step (F5a/F5b witnesses)")
    ap.add_argument("what", choices=("check", "make"))
    ap.add_argument("--certificates", default=os.path.join(ROOT, "certificates"))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rep = Report(f"s28_route_t_exclusion_{a.what}", a.out)
    if a.what == "check":
        check(rep, a.certificates)
    else:
        make(rep)
    rep.finish()


if __name__ == "__main__":
    main()
