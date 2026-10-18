r"""S26. Route T, classification of the rank-2 support modules (supplement §S4.1; Table D2 [C20], first count).
Not used in the proof of Theorem A. The second, independent count is recount.py.
S26. 経路 T、階数 2 の台加群の分類（補遺 §S4.1、表 D2 の [C20] の 1 通り目）。定理 A の証明には使わない。独立な 2 通り目は recount.py。

Enumerates the hermitian Z[sqrt(-5)]-lattices N of rank 2 with even integral trace form, real minimum
>= 6 and det_h N <= 4 (free or not), and groups them by invariants (real determinant, theta
coefficients up to norm 16, minimum and short vectors of H (x) N). Expected: 97 types, 63 dangerous
(H (x) N has a vector of norm < 10: 30 with minimum 6, 33 with minimum 8), and every dangerous candidate
(all of them, not only the representatives) contains a configuration detected by one of the three
searches of §S4.1.
トレース形式が偶・整数、実の最小 6 以上、det_h N ≤ 4 の階数 2 のエルミート Z[√-5]-格子 N を（自由・非自由を問わず）列挙し、不変量
（実の行列式、ノルム 16 までのテータ係数、H ⊗ N の最小と短いベクトル）でまとめる。期待: 97 型、うち危険 63（H ⊗ N にノルム 10 未満の
ベクトル。最小 6 が 30、最小 8 が 33）。危険な候補はすべて（代表だけでなく）§S4.1 の 3 つの探索のどれかが検出する配置を含む。

The expected numbers are checked (Report: out/s26_route_t_classify.json; exit code 1 on a mismatch), as is
that no candidate is dropped by a failed internal check. The table of types is written to
out/route_t/classify.json (read by recount.py).
期待する数を検査する（Report: out/s26_route_t_classify.json。食い違えば終了コード 1）。内部の検査に落ちて捨てられた候補が無いことも
確かめる。型の表は out/route_t/classify.json に書く（recount.py が読む）。

Requires SageMath (PARI). Run time: about 2 minutes.
SageMath（PARI）が要る。実行時間: 約 2 分。
Run / 実行:  python3 -I code/supplementary/route_t/classify.py [--amax 24] [--out DIR]   (Python with SageMath / SageMath を含む Python)

Method (Japanese) / 方法:
「危険な台加群」の分類を、非自由な加群も含めて完全にする。

対象: ℤ[√-5] 上の階数 2 のエルミート格子 N（√-5 は実の 4 次元格子の上の τ, τ² = -5 として作用）で
  (i) トレース形式 (u,v) = Tr h(u,v) が整数で偶、(ii) 実の最小 ≥ 6（L の部分加群なので）、(iii) det_h N ≤ 4
     （z ∈ H ⊗ N がノルム 8 なら Coulangeon の不等式 h(z) ≥ 2√(det H · det N), det H = 1 から det N ≤ 4）。
完全性の議論（概略）:
  * 類数 2 なので N ≅ O ⊕ 𝔞, 𝔞 ∈ {O, 𝔭2}（Steinitz）。どちらでも、指数 1 か 2 の自由な部分加群 F = Ox ⊕ Oy を含む（[𝔭2 : 2O] = 2）。
    F は最小 ≥ 6、det_h F = det_h N·[N:F] ≤ 8（エルミート格子では指数は 1 乗で効く。補遺 §S4.1）。
  * 自由な F は、第 1 基底ベクトル x（h(x) = a）と y で、h(x,y) = c を aO を法として簡約: c = p/2 − (q/10)√-5, p ∈ (−a, a], q ∈ (−5a, 5a]。
    N(c) ≤ 1.5a² なので b = h(y) ≤ (8 + 1.5a²)/a。x は「基底に延長できるベクトルのうち最短」（真の最短とは限らない:
    F ∩ Kx0 = 𝔭2^{-1}x0 のとき）。x0 + (1+√-5)w が基底ベクトルで h ≤ a0 + 6·8/a0 ≤ 8 + 16 なので a ≤ 24（--amax の既定値）。
  * N は F 自身か、F の τ-安定な指数 2 の上格子 F + Z·v/2（v ∈ F/2F で vτ ≡ 0 か v mod 2）。
各 N について: H ⊗ N（実 8 次元、hermitian.HermTensor。自由でなくてよい）の最小とノルム 6・8 の本数、
N がノルム 6 のベクトルを含むか、ノルム 8 の K-独立な組で x' ≡ μx (mod 2N), μ ∈ {τ, 1+τ} となるものがあるか、を調べる。
"""
import argparse, json, os, sys
from sage.all import ZZ, QQ, matrix, vector, QuadraticField, pari, identity_matrix, floor, sqrt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import hermitian as ts  # noqa: E402
from lib.report import Report  # noqa: E402

if not __debug__:
    sys.exit("run without -O: internal checks are assert statements / -O を付けずに実行すること（内部の検査は assert で書かれている）")

# Expected numbers (supplement §S4.1, Table D2 [C20]) / 期待する数（補遺 §S4.1、表 D2 の [C20]）
EXPECTED_TYPES, EXPECTED_DANGEROUS, EXPECTED_DANGEROUS_MIN6, EXPECTED_DANGEROUS_MIN8 = 97, 63, 30, 33
K = QuadraticField(-5, "s"); s = K.gen()
T4 = matrix(ZZ, [[0, 0, 1, 0], [0, 0, 0, 1], [-5, 0, 0, 0], [0, -5, 0, 0]])      # 基底 (e1, e2, s e1, s e2) での √-5 倍（行ベクトル）


def trace_gram(Hm):
    r = Hm.nrows(); un = [K(1), s]
    return matrix(QQ, 2 * r, 2 * r, lambda i, j: (un[i // r] * un[j // r].conjugate() * Hm[i % r, j % r]).trace())


def vectors(T, m):
    V = matrix(ZZ, pari(T).qfminim(m, None, 0)[2]).transpose().rows()
    out = [vector(ZZ, v) for v in V]; return out + [-v for v in out]


def analyse(B, T):
    """N = 行 B（F の座標、有理）が張る格子。T は F の実 Gram。τ は F の座標で T4。"""
    GN = (B * T * B.transpose()); assert all(x in ZZ for x in GN.list()); GN = GN.change_ring(ZZ)
    tauN = B * T4 * B.inverse(); assert all(x in ZZ for x in tauN.list()); tauN = tauN.change_ring(ZZ)
    assert ts.is_structure(GN, tauN, 5)
    GH = trace_gram(matrix(K, [[3, s], [-s, 2]])).change_ring(ZZ); AH = T4
    HT = ts.HermTensor(GH, AH, GN, tauN, 5); R = HT.R
    mR = ts.exact_minimum(R, 10)
    n6 = int(pari(R).qfminim(6, 0, 0)[0]); n8 = int(pari(R).qfminim(8, 0, 0)[0]) - n6
    U = matrix(ZZ, pari(GN).qflllgram()); GL = U.transpose() * GN * U
    minN = min(int(t) for t in [GL[i, i] for i in range(4)])
    # 厳密な最小
    q = pari(GL).qfminim(minN - 2, 1, 0)
    while int(q[0]):
        v = vector(ZZ, [int(t) for t in q[2][0]]); minN = int(v * GL * v); q = pari(GL).qfminim(minN - 2, 1, 0)
    V8 = vectors(GN, 8); V8 = [v for v in V8 if v * GN * v == 8]
    pair = {"tau": False, "1+tau": False}
    I4 = identity_matrix(ZZ, 4)
    for x in V8:
        for y in V8:
            if matrix(ZZ, [x, x * tauN, y]).rank() < 3:
                continue
            for name, mu in (("tau", tauN), ("1+tau", I4 + tauN)):
                if all(c % 2 == 0 for c in (y - x * mu)):
                    pair[name] = True
    half = any(all(c % 2 == 0 for c in (x + x * tauN)) for x in V8)     # x(1+τ) ∈ 2N（(1+√-5)x/2 ∈ N）: μ = 1+τ の類が 0 を含む
    # 最小 6 の N: ノルム 6 の u と K-独立な u' ≡ μu (mod 2N), |u'|² ≤ 10, μ ∈ {1, τ, 1+τ}
    V6 = [v for v in vectors(GN, 6) if v * GN * v == 6]; W10 = vectors(GN, 10); p6 = {}
    for u in V6:
        for name, mu in (("1", I4), ("tau", tauN), ("1+tau", I4 + tauN)):
            for w in W10:
                if matrix(ZZ, [u, u * tauN, w]).rank() == 3 and all(c % 2 == 0 for c in (w - u * mu)):
                    p6[name] = min(p6.get(name, 99), int(w * GN * w))
    pair["1+tau"] = pair["1+tau"] or half
    return dict(p6=p6, half=half, real_det=int(GN.det()), det_h=str(sqrt(QQ(GN.det())) / 20), min_N=minN, n8_N=len(V8),
                min_HN=None if mR is None else mR[0], n6_HN=n6, n8_HN=n8, pair_tau=pair["tau"], pair_1tau=pair["1+tau"],
                theta=[int(pari(GN).qfminim(m, 0, 0)[0]) for m in (6, 8, 10, 12, 14, 16)])


def min6_pairs(B, T):
    """最小 6 の N について: ノルム 6 の u と、K-独立な u' ≡ μu (mod 2N)（μ ∈ {1, τ, 1+τ}）の組で、|u'|² の最小を μ ごとに返す。"""
    GN = (B * T * B.transpose()).change_ring(ZZ); tauN = (B * T4 * B.inverse()).change_ring(ZZ); I4 = identity_matrix(ZZ, 4)
    V6 = [v for v in vectors(GN, 6) if v * GN * v == 6]; W = vectors(GN, 14)
    best = {}
    for u in V6:
        for name, mu in (("1", I4), ("tau", tauN), ("1+tau", I4 + tauN)):
            for w in W:
                if matrix(ZZ, [u, u * tauN, w]).rank() < 3:
                    continue
                if all(c % 2 == 0 for c in (w - u * mu)):
                    nw = int(w * GN * w); best[name] = min(best.get(name, 99), nw)
    return best


def index2_bases(T):
    """The τ-stable superlattices of index 2 of F (Gram T): bases B (rows, rational) of F + Z v/2.
    F の τ-安定な指数 2 の上格子 F + Z v/2 の基底 B（行、有理数）。"""
    out = []
    for bits in range(1, 16):
        v = vector(ZZ, [(bits >> i) & 1 for i in range(4)])
        w = (v * T4) % 2
        if not (w == 0 or w == v):
            continue
        out.append(matrix(QQ, (matrix(QQ, identity_matrix(QQ, 4).rows() + [v / 2]) * 2).change_ring(ZZ).hermite_form(include_zero_rows=False)) / 2)
    return out


def main():
    ap = argparse.ArgumentParser(description="S26: route T, classification of the rank-2 support modules")
    ap.add_argument("--amax", type=int, default=24, help="upper bound for a = h(x) (24 is the proved bound)")
    ap.add_argument("--out", default=None)
    a_ = ap.parse_args()
    rep = Report("s26_route_t_classify", a_.out)
    out_dir = os.path.join(rep.out_dir, "route_t")
    os.makedirs(out_dir, exist_ok=True)
    # 第 1 基底ベクトル x は「基底に延長できるベクトルのうち最短」（真の最短とは限らない: F' ∩ Kx0 = 𝔭2^{-1}x0 のとき）。
    # det_h F' ≤ 8（[N:F'] ≤ 2）。上界 a ≤ 24（x0 + (1+√-5)w が基底ベクトルで h ≤ a0 + 6·8/a0 ≤ 8 + 16）。
    DMAX = 8; AMAX = a_.amax
    frees = []
    for a in range(3, AMAX + 1):
        for b in range(a, int(floor((DMAX + QQ(3) / 2 * a * a) / a)) + 1):
            for p in range(-a + 1, a + 1):
                for q in range(-5 * a + 1, 5 * a + 1):
                    c = QQ(p) / 2 - QQ(q) / 10 * s; d = a * b - c.norm()
                    if not (0 < d <= DMAX):
                        continue
                    T = trace_gram(matrix(K, [[a, c], [c.conjugate(), b]]))
                    if not all(x in ZZ for x in T.list()) or any(T[i, i] % 2 for i in range(4)):
                        continue
                    T = T.change_ring(ZZ)
                    if not T.is_positive_definite():
                        continue
                    if int(pari(T).qfminim(4, 1, 0)[0]):                           # 最小 ≥ 6（x が最短であることは要求しない）
                        continue
                    frees.append((a, b, p, q, d, T))
    rep.value(f"free F (min >= 6, det_h <= {DMAX}, a <= {AMAX})", len(frees))
    found = {}; ALL = dict(n=0, dangerous=0, dangerous_min6=0, dangerous_min8=0, min8_without_pair=0,
                           min6_without_partner=0, min6_uncovered=0)
    dropped = []                    # candidates on which an internal check failed (never expected) / 内部の検査に落ちた候補（起きないはず）
    for a, b, p, q, d, T in frees:
        cands = []
        if d <= 4:
            cands.append(("free", identity_matrix(QQ, 4)))
        for B in index2_bases(T):
            GN = B * T * B.transpose()
            if not all(x in ZZ for x in GN.list()) or any(GN[i, i] % 2 for i in range(4)):
                continue
            if QQ(GN.det()) > 6400:
                continue
            if int(pari(GN.change_ring(ZZ)).qfminim(4, 1, 0)[0]):            # 最小 ≥ 6
                continue
            cands.append(("index2", B))
        for kind, B in cands:
            try:
                r = analyse(B, T)
            except AssertionError as e:
                dropped.append(dict(kind=kind, example=(a, b, p, q), error=str(e)))
                continue
            if r["real_det"] > 6400 or r["min_N"] < 6:
                continue
            key = (r["real_det"], tuple(r["theta"]), r["min_HN"], r["n6_HN"], r["n8_HN"])
            r["kind"] = kind; r["example"] = (a, b, p, q)
            found.setdefault(key, r)
            # 代表だけでなく全候補で: 危険な N が探索 (1)–(3) のどれかで検出される配置をもつか（不変量による同一視で見落とさないため）
            # On every candidate, not only one per type: does the dangerous N contain a configuration of searches (1)-(3)?
            ALL["n"] += 1
            if r["min_HN"] is not None:
                ALL["dangerous"] += 1
                if r["min_N"] == 6:
                    ALL["dangerous_min6"] += 1
                    if not r["p6"]:
                        ALL["min6_without_partner"] += 1
                    if not (r["p6"] or r["pair_tau"] or r["pair_1tau"]):
                        ALL["min6_uncovered"] += 1
                if r["min_N"] >= 8:
                    ALL["dangerous_min8"] += 1
                    if not (r["pair_tau"] or r["pair_1tau"]):
                        ALL["min8_without_pair"] += 1
    rep.value("all candidate N (before identification)", ALL)
    rep.value("candidates dropped by a failed internal check", dropped)
    rep.check("no candidate dropped by a failed internal check", not dropped)
    rep.check("every dangerous candidate is covered by one of the searches (1)-(3) (none uncovered with minimum 6 or 8)",
              ALL["min6_uncovered"] == 0 and ALL["min8_without_pair"] == 0)
    rows = sorted(found.values(), key=lambda r: (QQ(r["det_h"]), r["min_N"]))
    print("det_h   real_det  kind    min_N  #norm8(N)  min(H⊗N)  #6  #8   pair τ  pair 1+τ   example (a,b,p,q)")
    for r in rows:
        print(f"{r['det_h']:>7} {r['real_det']:>8}  {r['kind']:<7} {r['min_N']:>5} {r['n8_N']:>9} {str(r['min_HN']):>9} {r['n6_HN']:>4} {r['n8_HN']:>4}   {str(r['pair_tau']):<6} {str(r['pair_1tau']):<8}  {r['example']}")
    with open(os.path.join(out_dir, "classify.json"), "w") as f:
        json.dump(rows, f, indent=1)
    dang = [r for r in rows if r["min_HN"] is not None]
    counts = [len(rows), len(dang), sum(r["min_N"] == 6 for r in dang), sum(r["min_N"] >= 8 for r in dang)]
    rep.value("types (by real det, theta series up to 16, H⊗N data): all, dangerous, dangerous with min 6, with min >= 8", counts)
    rep.check(f"{EXPECTED_TYPES} types, {EXPECTED_DANGEROUS} dangerous ({EXPECTED_DANGEROUS_MIN6} with minimum 6, {EXPECTED_DANGEROUS_MIN8} with minimum 8)",
              counts == [EXPECTED_TYPES, EXPECTED_DANGEROUS, EXPECTED_DANGEROUS_MIN6, EXPECTED_DANGEROUS_MIN8])

    # A statistic only (not a claim): for one candidate per min-6 dangerous type, the smallest |u'|^2 (up to 14)
    # of a partner u' ≡ μu (mod 2N) of a norm-6 vector u. The types without one are covered by searches (1), (2).
    # 統計（主張ではない）: 最小 6 の危険な型ごとに候補 1 つで、ノルム 6 の u の相手 u' ≡ μu (mod 2N) の |u'|² の最小（14 まで）。
    # 相手が無い型は探索 (1)・(2) で覆われる（上の検査）。
    print("--- min-6 dangerous types: partners u' ≡ μu (mod 2N) of a norm-6 vector u (smallest |u'|² per μ, up to 14)")
    ok = 0; tot = 0
    for r in rows:
        if r["min_HN"] is None or r["min_N"] != 6:
            continue
        a, b, p, q = r["example"]
        c = QQ(p) / 2 - QQ(q) / 10 * s
        T = trace_gram(matrix(K, [[a, c], [c.conjugate(), b]])).change_ring(ZZ)
        if r["kind"] == "free":
            Bs = [identity_matrix(QQ, 4)]
        else:
            Bs = [B for B in index2_bases(T) if all(x in ZZ for x in (B * T * B.transpose()).list())
                  and int((B * T * B.transpose()).det()) == r["real_det"]]
        for B in Bs[:1]:
            bp = min6_pairs(B, T); tot += 1
            good = any(nm in bp and bp[nm] <= 10 for nm in bp)
            ok += good
            print(f"   det_h {r['det_h']:>6} ({r['kind']}): {bp}  {'(partner of norm ≤ 10 exists)' if good else ''}")
    rep.value("min-6 dangerous types with a partner u' of norm <= 10 (statistic)", f"{ok}/{tot}")
    rep.finish()


if __name__ == "__main__":
    main()
