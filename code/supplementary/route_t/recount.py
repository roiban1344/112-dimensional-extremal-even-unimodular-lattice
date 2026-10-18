r"""S27. Route T, second count of the rank-2 support modules (supplement §S4.1; Table D2 [C20], second count).
Not used in the proof of Theorem A.
S27. 経路 T、階数 2 の台加群の 2 通り目の数え上げ（補遺 §S4.1、表 D2 の [C20] の 2 通り目）。定理 A の証明には使わない。

A different enumeration (from a true shortest vector, with pseudo-bases) in exact rational arithmetic
(own Fincke-Pohst enumeration; LLL only for basis changes, checked to be unimodular). It groups the
dangerous candidates by a coarser invariant (real determinant, numbers of vectors of norm <= 6, 8, 10,
minimum of H (x) N). Expected: 468 candidates, 296 dangerous, 0 uncovered, 58 dangerous types; regrouping
the 63 dangerous types of classify.py by the same invariant gives the same 58.
別の列挙（真の最短ベクトルから、擬基底で）を有理数の厳密演算で行う（自前の Fincke–Pohst 列挙。LLL は基底の取り替えだけで、ユニモジュラーで
あることを確かめる）。危険な候補をより粗い不変量（実の行列式、ノルム 6・8・10 以下の本数、H ⊗ N の最小）でまとめる。期待: 候補 468、
危険 296、覆われないもの 0、危険な型 58。classify.py の危険な 63 型を同じ不変量でまとめ直すと同じ 58 になる。

The expected numbers and the agreement with classify.json are checked (Report: out/s27_route_t_recount.json;
exit code 1 on a mismatch or if classify.json is missing). The candidates are written to out/route_t/recount.json.
期待する数と classify.json との一致を検査する（Report: out/s27_route_t_recount.json。食い違うか classify.json が無ければ終了コード 1）。
候補は out/route_t/recount.json に書く。

Requires SageMath (for LLL only). Run time: about 1 minute. Run classify.py first for the comparison.
SageMath が要る（LLL だけ）。実行時間: 約 1 分。突き合わせのため classify.py を先に走らせる。
Run / 実行:  python3 -I code/supplementary/route_t/recount.py [--out DIR]   (Python with SageMath / SageMath を含む Python)

Method (Japanese) / 方法:
補遺 §S4.1 の分類を、別の列挙法と整数・有理数の厳密演算だけで数え直す。

classify.py（以下「1 通り目」）との違い:
- 列挙: 1 通り目は自由な部分加群 F'（指数 ≤ 2）の「基底に延長できる最短ベクトル」から入り、a ≤ 24 を別の議論で出した。
  ここでは N の**真の最短ベクトル** x から入る。x を含む直線との交わり N ∩ Kx = 𝔄x は 𝔄 ∈ {O, 𝔭₂⁻¹}
  （x が最短なので 𝔄 ⊇ O はノルム 1 未満の元を含まない。𝔭₂⁻¹ = Z + Z(1+√-5)/2 以外の候補 𝔭₃⁻¹ などは (1±√-5)/3 を含む）。
  N/𝔄x は階数 1 の射影加群なので N = 𝔄x ⊕ 𝔅y（擬基底）、𝔅 は類の代表 {O, 𝔭₂⁻¹} に取れる（y を K の元倍して）。
  y ↦ y + γx（γ ∈ 𝔄𝔅⁻¹）で c = h(x,y) は c + γ̄a に変わるので、c を格子 a·𝔄𝔅⁻¹ の基本平行四辺形の中に取れる。
  a の上界は Hermite: 実ノルム 2a、実の行列式 ≤ 6400（det_h ≤ 4）、γ₄⁴ = 4 から (2a)⁴ ≤ 25600、a ≤ 6。
  b ≥ a（y ∈ N、x が最短）、b の上界は実の行列式 ≤ 6400 から（b について単調増加）。
- 計算: 最小と短いベクトルは、有理数の LDL 分解による自前の Fincke–Pohst 列挙（浮動小数点なし）。LLL（Sage）は基底の取り替えにだけ使い、
  取り替え行列が整数・行列式 ±1 であることを確かめる（列挙の正しさは基底によらない）。pari・fpylll は使わない。

各 N について: 危険か（H ⊗ N にノルム 8 以下）、覆われるか（補遺 §S4.1 の 3 つの探索のどれか）を判定し、classify.py の classify.json の不変量と突き合わせる。
"""
import argparse, json, os, sys, itertools
from fractions import Fraction as Fr
from math import isqrt, floor, ceil

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from lib.report import Report  # noqa: E402

if not __debug__:
    sys.exit("run without -O: internal checks are assert statements / -O を付けずに実行すること（内部の検査は assert で書かれている）")

# Expected numbers (Table D2 [C20]) / 期待する数（表 D2 の [C20]）
EXPECTED = dict(N=468, dangerous=296, uncovered=0)
EXPECTED_DANGEROUS_TYPES = 58

# ---------- K = Q(√-5) の元は (r, s) = r + s√-5（Fraction） ----------

def kmul(u, v):
    return (u[0] * v[0] - 5 * u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def kconj(u):
    return (u[0], -u[1])


def knorm(u):
    return u[0] * u[0] + 5 * u[1] * u[1]


def ktr(u):
    return 2 * u[0]


ONE, W = (Fr(1), Fr(0)), (Fr(0), Fr(1))
IDEALS = {"O": [ONE, W], "P": [ONE, (Fr(1, 2), Fr(1, 2))]}       # Z-基底。P = 𝔭₂⁻¹ = Z + Z(1+√-5)/2
INV = {"O": IDEALS["O"], "P": [(Fr(2), Fr(0)), (Fr(1), Fr(1))]}  # 逆イデアル（𝔭₂ = Z·2 + Z(1+√-5)）


def coords(u, basis):
    """u を Z-基底 basis（2 元）で表す有理座標。"""
    (a, b), (c, d) = basis
    det = a * d - b * c
    return ((u[0] * d - u[1] * c) / det, (a * u[1] - b * u[0]) / det)


def real_structure(Hm, ideals):
    """エルミート Gram Hm（K の元の行列）と擬基底のイデアル列 → Z-基底での実 Gram（Tr h）と √-5 倍の行列（行ベクトル作用）。"""
    basis = [(i, beta) for i, I in enumerate(ideals) for beta in IDEALS[I]]
    n = len(basis)
    G = [[ktr(kmul(kmul(bk, kconj(bl)), Hm[ik][il])) for (il, bl) in basis] for (ik, bk) in basis]
    T = [[Fr(0)] * n for _ in range(n)]
    for k, (i, b) in enumerate(basis):
        wb = kmul(W, b)
        c = coords(wb, IDEALS[ideals[i]])
        T[k][2 * i], T[k][2 * i + 1] = c
    return G, T


def is_int(M):
    return all(x.denominator == 1 for r in M for x in r)


# ---------- 厳密な短ベクトル列挙 ----------

def ldl(G):
    n = len(G); A = [[Fr(x) for x in r] for r in G]
    d = [Fr(0)] * n; mu = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        d[i] = A[i][i] - sum(mu[i][k] ** 2 * d[k] for k in range(i))
        if d[i] <= 0:
            return None
        for j in range(i + 1, n):
            mu[j][i] = (A[j][i] - sum(mu[j][k] * mu[i][k] * d[k] for k in range(i))) / d[i]
    return d, mu


def int_range(c, r):
    """(k + c)² ≤ r を満たす整数 k の範囲（r ≥ 0、厳密）。"""
    # |k + c| ≤ √r。√r の上下を整数平方根で挟んでから厳密に詰める
    lo = floor(-c - Fr(isqrt(int(r) + 1) + 1)); hi = ceil(-c + Fr(isqrt(int(r) + 1) + 1))
    ks = [k for k in range(lo, hi + 1) if (k + c) ** 2 <= r]
    return ks


def short_vectors(G, B):
    """0 < x^T G x ≤ B の整数ベクトルをすべて（±両方）。G は整数の正定値 Gram。"""
    n = len(G)
    r = ldl(G); assert r is not None, "正定値でない"
    d, mu = r                       # q(x) = Σ_i d_i (x_i + Σ_{j>i} mu[j][i] x_j)²
    out = []
    x = [0] * n

    def rec(i, rem):
        c = sum(mu[j][i] * x[j] for j in range(i + 1, n))
        for k in int_range(c, rem / d[i]):
            x[i] = k
            used = d[i] * (k + c) ** 2
            if i == 0:
                if any(x):
                    out.append(tuple(x))
            else:
                rec(i - 1, rem - used)
        x[i] = 0
    rec(n - 1, Fr(B))
    return out


def qf(G, v):
    return sum(G[i][j] * v[i] * v[j] for i in range(len(v)) for j in range(len(v)))


def lll_basis(G):
    """Sage の LLL で基底を取り替える（U は整数・行列式 ±1 を確認）。返り値: (G', U)。"""
    from sage.all import matrix, ZZ
    M = matrix(ZZ, [[int(x) for x in r] for r in G])
    U = M.LLL_gram()
    if U.det() not in (1, -1):                  # the enumeration relies on it / 列挙の正しさがこれに依る
        raise RuntimeError("LLL_gram returned a non-unimodular transformation")
    Gp = U.transpose() * M * U
    return [[int(x) for x in r] for r in Gp.rows()], U


def minimum_exact(G, bound):
    Gp, _ = lll_basis(G)
    V = short_vectors(Gp, bound)
    return min((qf(Gp, v) for v in V), default=None), len(V), Gp


# ---------- 本体 ----------

H = [[(Fr(3), Fr(0)), (Fr(0), Fr(1))], [(Fr(0), Fr(-1)), (Fr(2), Fr(0))]]   # [[3, √-5], [-√-5, 2]]


def kron(A, Bm):
    m, n = len(A), len(Bm)
    return [[kmul(A[i // n][j // n], Bm[i % n][j % n]) for j in range(m * n)] for i in range(m * n)]


def det_int(G):
    from sage.all import matrix, ZZ
    return int(matrix(ZZ, G).det())


def c_candidates(a, IA, IB):
    """c = p/2 - (q/10)√-5 の格子点で、格子 Λ = a·𝔄·𝔅⁻¹ の基本平行四辺形 {s e1 + t e2 : 0 ≤ s, t < 1} を覆うもの（余分は可）。"""
    # Λ の Z-基底: a · (𝔄 の基底元 × 𝔅⁻¹ の基底元) の張る格子。積イデアルは 4 元で生成されるので HNF で 2 元に
    gens = [kmul((Fr(a), Fr(0)), kmul(u, v)) for u in IDEALS[IA] for v in INV[IB]]
    # c の格子 (1/2)Z + (1/10)Z√-5 の座標 (P, Q) = (2 re, 10 im) に直して HNF
    from sage.all import matrix, ZZ
    M = matrix(ZZ, [[int(2 * g[0]), int(10 * g[1])] for g in gens]).hermite_form(include_zero_rows=False)
    e1, e2 = M.rows()
    out = []
    # 平行四辺形の頂点を囲む箱の中の (P, Q) をすべて
    corners = [(0, 0), tuple(e1), tuple(e2), tuple(e1 + e2)]
    P0, P1 = min(c[0] for c in corners), max(c[0] for c in corners)
    Q0, Q1 = min(c[1] for c in corners), max(c[1] for c in corners)
    for P in range(P0, P1 + 1):
        for Q in range(Q0, Q1 + 1):
            out.append((Fr(P, 2), Fr(Q, 10)))
    return out


def analyse(Gn, Tn):
    """N（実 Gram Gn、τ 行列 Tn。整数）: 短ベクトル、mod 2 の関係。"""
    Gp, U = lll_basis(Gn)
    from sage.all import matrix, ZZ
    Ui = U.inverse()
    tau = U.transpose() * matrix(ZZ, Tn) * Ui.transpose()          # 新しい座標での τ（行ベクトル作用）
    tau = [[int(x) for x in r] for r in tau.rows()]
    n = 4
    V = short_vectors(Gp, 10)
    norm = {v: qf(Gp, v) for v in V}
    mn = min(norm.values()) if V else None

    def act(v, M):
        return tuple(sum(v[i] * M[i][j] for i in range(n)) for j in range(n))
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    tau1 = [[I[i][j] + tau[i][j] for j in range(n)] for i in range(n)]

    def indep(u, w):
        from sage.all import matrix, QQ
        return matrix(QQ, [u, act(u, tau), w]).rank() == 3

    def cong(u, w):
        return all((a - b) % 2 == 0 for a, b in zip(u, w))
    V6 = [v for v in V if norm[v] == 6]; V8 = [v for v in V if norm[v] == 8]
    cov = {"tau8": False, "1tau8": False, "half8": False, "min6": False}
    for x in V8:
        if all(c % 2 == 0 for c in act(x, tau1)):
            cov["half8"] = True
        tx, t1x = act(x, tau), act(x, tau1)
        for y in V8:
            if not cov["tau8"] and cong(y, tx) and indep(x, y):
                cov["tau8"] = True
            if not cov["1tau8"] and cong(y, t1x) and indep(x, y):
                cov["1tau8"] = True
    for u in V6:
        if cov["min6"]:
            break
        for M in (I, tau, tau1):
            mu_u = act(u, M)
            if any(cong(w, mu_u) and indep(u, w) for w in V):
                cov["min6"] = True; break
    theta = [sum(1 for v in V if norm[v] <= m) for m in (6, 8, 10)]
    return mn, theta, cov


def main():
    ap = argparse.ArgumentParser(description="S27: route T, second count of the rank-2 support modules")
    ap.add_argument("--out", default=None)
    a_ = ap.parse_args()
    rep = Report("s27_route_t_recount", a_.out)
    out_dir = os.path.join(rep.out_dir, "route_t")
    os.makedirs(out_dir, exist_ok=True)
    seen_N = []; stats = dict(N=0, dangerous=0, uncovered=0)
    classes = {}
    for IA, IB in itertools.product("OP", repeat=2):
        for a in range(3, 7):
            for c in c_candidates(a, IA, IB):
                b = a
                while True:
                    Hn = [[(Fr(a), Fr(0)), c], [kconj(c), (Fr(b), Fr(0))]]
                    if knorm(c) >= a * b:            # 正定値でない（b を増やす）
                        b += 1; continue
                    G, T = real_structure(Hn, [IA, IB])
                    if not is_int(G):
                        # Integrality depends only on a and c: the entries containing b (Tr of b times a norm from the
                        # ideal basis) are always integers, so no larger b can help.
                        # 整数性は a と c だけで決まる（b を含む成分はいつも整数）ので、b を増やしても変わらない。
                        break
                    G = [[int(x) for x in r] for r in G]
                    D = det_int(G)
                    if D > 6400:
                        break
                    b += 1
                    if any(G[i][i] % 2 for i in range(4)) or not is_int(T):
                        continue
                    T = [[int(x) for x in r] for r in T]
                    Gl = lll_basis(G)[0]
                    mnN = min(qf(Gl, v) for v in short_vectors(Gl, 2 * a))     # 座標は取り替え後の基底で
                    if mnN < 6 or mnN < 2 * a:       # 最小 ≥ 6、x（実ノルム 2a）が最短
                        continue
                    stats["N"] += 1
                    # H ⊗ N
                    Ht = kron(H, Hn)
                    GH, _ = real_structure(Ht, [IA, IB, IA, IB])
                    if not is_int(GH):
                        raise RuntimeError(f"H (x) N has a non-integral Gram matrix: {IA}, {IB}, a = {a}, c = {c}")
                    GH = [[int(x) for x in r] for r in GH]
                    mH, cnt, _ = minimum_exact(GH, 8)
                    if mH is None:
                        rec = None
                    else:
                        stats["dangerous"] += 1
                        mn, theta, cov = analyse(G, T)
                        covered = any(cov.values())
                        if not covered:
                            stats["uncovered"] += 1
                        key = (D, tuple(theta), mH)
                        classes.setdefault(str(key), dict(real_det=D, theta=theta, min_HN=mH, min_N=mn, cov=cov,
                                                          example=dict(A=IA, B=IB, a=a, b=b - 1, c=[str(c[0]), str(c[1])])))
        rep.log(f"  ({IA},{IB}) 済: {stats}")
    rep.value("all candidates: N, dangerous, uncovered", stats)
    rep.value("dangerous types (real det, numbers of vectors of norm <= 6/8/10, minimum of H⊗N)", len(classes))
    with open(os.path.join(out_dir, "recount.json"), "w") as f:
        json.dump(dict(stats=stats, classes=classes), f, indent=1)
    rep.check(f"{EXPECTED['N']} candidates, {EXPECTED['dangerous']} dangerous, {EXPECTED['uncovered']} uncovered", stats == EXPECTED)
    rep.check(f"{EXPECTED_DANGEROUS_TYPES} dangerous types", len(classes) == EXPECTED_DANGEROUS_TYPES)
    # Comparison with classify.py at the level of the coarse invariant (new in the published version).
    # classify.py との突き合わせ（粗い不変量の水準で。公開版で追加）。
    cj = os.path.join(out_dir, "classify.json")
    rep.check("out/route_t/classify.json exists (run classify.py first)", os.path.exists(cj))
    rows = json.load(open(cj))
    first = {(r["real_det"], tuple(r["theta"][:3]), r["min_HN"]) for r in rows if r["min_HN"] is not None}
    second = {(v["real_det"], tuple(v["theta"]), v["min_HN"]) for v in classes.values()}
    rep.value("dangerous types after regrouping: classify.json, here", [len(first), len(second)])
    rep.check(f"the same {EXPECTED_DANGEROUS_TYPES} dangerous types as classify.json after regrouping by the coarse invariant",
              first == second and len(first) == EXPECTED_DANGEROUS_TYPES)
    rep.finish()
    return stats, classes


if __name__ == "__main__":
    main()
