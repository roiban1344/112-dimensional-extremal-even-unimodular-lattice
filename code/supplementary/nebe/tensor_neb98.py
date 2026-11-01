r"""Nebe's tensor-product construction [Neb98, §5] for (p, q) = (5, 29), which would have dimension 112
(paper §1.4, Table D2 [C33]). Not used in the proof of Theorem A. Requires SageMath.
Nebe のテンソル積の構成 [Neb98, §5] を (p, q) = (5, 29) に当てる。次元は 112 になる（論文 §1.4、表 D2 の [C33]）。
定理 A の証明には使わない。SageMath が要る。

[Neb98, §5] tensors two lattices L_{2(p-1),2}(M_1), L_{2(q-1),2}(M_2) over a common quaternion order O
(O acts on the right of L_1 and, through the canonical involution, on the left of L_2) and chooses an
invariant form; (p, q) = (5, 13) gives the extremal lattice L_48 [Neb98, Thm. 5.3]. The paper does not treat
(5, 29). Here O is a maximal order of S = Q_{inf,2} (the Hurwitz order) or of S = Q_{inf,3}, the definite
quaternion algebras over Q that embed into both Q_{sqrt5,inf,inf} and Q_{sqrt29,inf,inf}.
[Neb98, §5] は 2 つの格子 L_{2(p-1),2}(M_1), L_{2(q-1),2}(M_2) を共通の四元数整環 O の上でテンソルし（O は L_1 に右から、
L_2 に標準対合を通して左から働く）、不変形式を選ぶ。(p, q) = (5, 13) で極値格子 L_48 が得られる [Neb98, Thm. 5.3]。
(5, 29) は原文で扱われていない。ここでは O として、Q_{√5,∞,∞} と Q_{√29,∞,∞} の両方に入る Q 上の定値四元数環
S = Q_{∞,2}（Hurwitz 整環）と S = Q_{∞,3} の極大整環をとる。

Steps / 手順:
  1. For p = 5, 13, 29 build L_{2(p-1),2}(M) for every conjugacy class of maximal orders M of
     Q_{sqrt p,inf,inf} (cycloquat.py; the SL_2(p)-invariant one of the two unimodular choices, with the
     generators checked exactly).
     p = 5, 13, 29 について、Q_{√p,∞,∞} の極大整環の各共役類 M の L_{2(p-1),2}(M) を作る（cycloquat.py。ユニモジュラーな
     2 つの選択肢のうち SL_2(p) で不変な方。生成元は厳密に確かめる）。
  2. Embeddings O -> M: all pairs of units (a, j) of reduced norm 1 of M satisfying the defining relations
     of O, grouped up to conjugation by the units of M. For p = 29 this also checks [Neb98, p. 483]: the
     class with 24 units of reduced norm 1 (M) contains the Hurwitz order and not a maximal order of
     Q_{inf,3}; the class with 12 (M~) the other way round.
     埋め込み O -> M: O の定義関係を満たす M の被約ノルム 1 の単数の組 (a, j) をすべて求め、M の単数による共役で類別する。
     p = 29 では [Neb98, p. 483] も確かめる: 被約ノルム 1 の単数が 24 個の類（M）は Hurwitz 整環を含み Q_{∞,3} の極大整環を
     含まない。12 個の類（M~）はその逆。
  3. For every pair of embedding classes, Lambda = L_1 (x)_O L_2 is computed as the projection of
     L_1 (x)_Z L_2 to U = W^perp, where W is spanned by the relations x s (x) y - x (x) y conj(s) (s in a
     Z-basis of O). Checked: rank 112 (48 for the control); the relation module is saturated in L_1 (x) L_2, so the projection is
     L_1 (x)_O L_2 itself (no torsion); Lambda^# = (L_1 (x) L_2) cap U is stable under O_K',
     K' = Q(sqrt p, sqrt q). Units conjugating an embedding give isometric tensor products, so the pairs of
     classes cover all embeddings.
     埋め込みの類の各組について、Lambda = L_1 ⊗_O L_2 を、L_1 ⊗_Z L_2 の U = W^⊥ への射影として求める。W は関係式
     x s ⊗ y - x ⊗ y conj(s)（s は O の Z-基底）が張る。確かめること: 階数 112（対照では 48）。関係式の加群は L_1 ⊗ L_2 の中で飽和しており、
     射影は L_1 ⊗_O L_2 そのもの（捩れが無い）。Lambda^# = (L_1 ⊗ L_2) ∩ U は O_K'（K' = Q(√p, √q)）で安定。埋め込みを単数で
     共役しても等長なテンソル積になるので、類の組ですべての埋め込みを尽くす。
  4. The ideal a of O_K' with Lambda^# = Lambda a (found among the ideals of the right norm, unique).
     The invariant symmetric forms are F_c(x, y) = <x c, y> with c in K' (Lambda (x) C is a sum of four
     pairwise distinct irreducible characters psi_i (x) theta_j of SL_2(p) o SL_2(q), so the commutant is
     K'), positive definite iff c is totally positive, and the F_c-dual of Lambda b (b a fractional ideal)
     is Lambda^# b^-1 c^-1. Hence (Lambda b, F_c) is unimodular iff a = b^2 (c): this is possible for some b
     and some totally positive c iff the class of a in the narrow class group of K' is a square. For
     (5, 29) it is not (the class group of Q(sqrt5, sqrt29) is Z/2, narrow as well, and a is not
     principal), so no choice of form, and no twist by an ideal, gives a unimodular lattice.
     Lambda^# = Lambda a となる O_K' のイデアル a（ノルムの合うイデアルの中から求め、一意）。不変な対称形式は
     F_c(x, y) = <x c, y>（c ∈ K'）で尽きる（Lambda ⊗ C は SL_2(p) ∘ SL_2(q) の互いに異なる 4 つの既約指標 psi_i ⊗ theta_j の和
     なので、可換子環は K'）。正定値なのは c が総正のとき。Lambda b（b は分数イデアル）の F_c に関する双対は Lambda^# b^-1 c^-1。
     よって (Lambda b, F_c) がユニモジュラー ⇔ a = b^2 (c)。b と総正な c が存在する ⇔ a の狭義類群での類が平方。(5, 29) では
     平方でない（Q(√5, √29) の類群は Z/2、狭義でも同じで、a は単項でない）ので、形式の選び方でもイデアルでのひねりでも
     ユニモジュラーにならない。
  5. Positive control (5, 13): a has a totally positive generator, and the resulting form is even unimodular
     of dimension 48 with no nonzero vector of norm <= 4 (enumeration that cannot miss vectors), i.e. Nebe's
     extremal L_48. The class groups of Q(sqrt5, sqrt13) and Q(sqrt5, sqrt17) are trivial (narrow as well).
     陽性対照 (5, 13): a は総正な生成元をもち、得られる形式は 48 次元の偶ユニモジュラーで、ノルム 4 以下の非零ベクトルが無い
     （取りこぼしの無い列挙）。すなわち Nebe の極値格子 L_48。Q(√5, √13)、Q(√5, √17) の類群は自明（狭義でも）。

All steps are exact (rational and integer linear algebra, Sage number fields with proof=True); the Weyl
element is computed numerically and then checked exactly. Signs at the real places (total positivity) are decided
in the field AA of real algebraic numbers, where comparisons are exact. Class groups: PARI's bnfinit with bnfcertify.
すべて厳密な計算（有理数・整数の線形代数、proof=True の Sage の数体）。Weyl 元は数値計算で求めてから厳密に確かめる。
実素点での符号（総正）は、比較が厳密な実代数的数の体 AA で判定する。類群は PARI の bnfinit と bnfcertify による。

Run time: 20 to 36 minutes on one core, depending on the load of the machine (8 pairs for (5, 29), 4 for (5, 13)). Memory: below 5 GB.
実行時間: 1 コアで 20〜36 分、計算機の負荷による（(5, 29) で 8 組、(5, 13) で 4 組）。メモリ: 5 GB 未満。
Run / 実行:  python3 code/supplementary/nebe/tensor_neb98.py
"""
import argparse
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "produce"))
from lib import require  # noqa: E402
from lib.report import Report  # noqa: E402


def hmat(X, h):
    """Matrix of right multiplication by h in H (coordinates) on Q(zeta)^2 = Q^{2(p-1)} (row vectors).
    H の元 h（座標）の右乗法の行列（Q(ζ)^2 = Q^{2(p-1)} の行ベクトルに右から）。"""
    from sage.all import QQ, block_matrix
    x, y = X.helt(h)
    m = X._mulmat
    return block_matrix(QQ, [[m(x), m(y)], [-m(X.conj(y)), m(X.conj(x))]], subdivide=False)


def hstar(X, h):
    """Canonical involution of H. / H の標準対合。"""
    x, y = X.helt(h)
    return X.hcoords((X.conj(x), -y))


def build(p, rep):
    """[(name, X, M, Gram, basis)] for the classes of maximal orders of Q_{sqrt p,inf,inf}: the
    SL_2(p)-invariant lattice L_{2(p-1),2}(M), with z, w checked exactly.
    Q_{√p,∞,∞} の極大整環の各類について SL_2(p) で不変な L_{2(p-1),2}(M)。z, w は厳密に確かめる。"""
    from sage.all import QQ, ZZ, block_matrix, identity_matrix, matrix, zero_matrix
    from cycloquat import CycloQuat, maximal_order_classes, weyl_element
    X = CycloQuat(p)
    h, n = p - 1, 2 * (p - 1)
    Mz = matrix(QQ, [(X.z ** (k + 1)).list() for k in range(h)])
    Z = zero_matrix(QQ, h, h)
    Zr = block_matrix(QQ, [[Mz, Z], [Z, Mz]], subdivide=False)
    I = identity_matrix(QQ, n)
    Wr = None
    for sg in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
        try:
            W_, _ = weyl_element(X, sg)
        except Exception:  # noqa: BLE001 (a sign choice that does not work / 合わない符号の選び方)
            continue
        if W_ * W_ == -I and (Zr * W_) ** 3 in (I, -I):
            Wr = W_
            break
    rep.check(f"p = {p}: Weyl element w with w^2 = -1, (z w)^3 = +-1", Wr is not None)
    out = []
    for ci, (M, _) in enumerate(maximal_order_classes(X)):
        for ch in range(2):
            G, Lb = X.lattice(M, ch)
            Li = Lb.inverse()
            WL = Lb * Wr * Li
            if all(x in ZZ for x in WL.list()):
                break
        ZL = Lb * Zr * Li
        ok = all(x in ZZ for x in WL.list() + ZL.list())
        ok = ok and WL * G * WL.transpose() == G and ZL * G * ZL.transpose() == G
        ok = ok and G.det() == 1 and all(G[i, i] % 2 == 0 for i in range(n))
        rep.check(f"p = {p}, class {ci}: even unimodular of dimension {n}, invariant under SL_2({p}) = <z, w>", ok)
        out.append(dict(p=p, ci=ci, X=X, M=M, G=G, Lb=Lb))
    return out


def units1(X, M):
    """Elements of reduced norm 1 of the order M (coordinates in H). / 整環 M の被約ノルム 1 の元（H の座標）。"""
    from sage.all import QQ, ZZ, QuadraticForm, vector
    G = X.norm_gram(M).change_ring(ZZ)
    vs = QuadraticForm(ZZ, G).short_vector_list_up_to_length(3)[2]
    us = []
    for v in vs:
        x = vector(QQ, v) * M
        if X.nrd(x) == (1, 0):
            us.append(x)
    return us


def in_order(M, x):
    from sage.all import ZZ
    return all(c in ZZ for c in M.solve_left(x))


def embeddings(X, M, kind):
    """Units U of reduced norm 1 of M and all pairs (a, j) in U giving an embedding O -> M.
    kind 2: a^2 = j^2 = -1, a j = -j a and (-1 + a + j + a j)/2 in M (the Hurwitz order).
    kind 3: a^2 + a + 1 = 0, j^2 = -1, j a = a^2 j (Z[a] + Z[a] j, the maximal order of Q_{inf,3}).
    M の被約ノルム 1 の単数 U と、埋め込み O -> M を与える U の組 (a, j) すべて。"""
    U = units1(X, M)
    one, mul = X.one, X.hmul
    o4 = [u for u in U if mul(u, u) == -one]
    res = []
    if kind == 2:
        for a in o4:
            for j in o4:
                if mul(a, j) == -mul(j, a) and in_order(M, (-one + a + j + mul(a, j)) / 2):
                    res.append((a, j))
    else:
        o3 = [u for u in U if mul(u, u) + u + one == 0]
        for a in o3:
            for j in o4:
                if mul(j, a) == mul(mul(a, a), j):
                    res.append((a, j))
    return U, res


def obasis(X, a, j, kind):
    """A Z-basis of O (coordinates in H). / O の Z-基底（H の座標）。"""
    one, mul = X.one, X.hmul
    if kind == 2:
        return [one, a, j, (-one + a + j + mul(a, j)) / 2]
    return [one, a, j, mul(a, j)]


def conj_classes(X, U, pairs):
    """Representatives of the pairs (a, j) up to conjugation by U. / U による共役での組 (a, j) の代表。"""
    mul = X.hmul
    seen, reps = set(), []
    for a, j in pairs:
        if (tuple(a), tuple(j)) in seen:
            continue
        reps.append((a, j))
        for u in U:
            ui = hstar(X, u)
            seen.add((tuple(mul(mul(u, a), ui)), tuple(mul(mul(u, j), ui))))
    return reps


def hnf(A):
    from sage.all import QQ, ZZ, lcm
    d = lcm([x.denominator() for x in A.list()] + [1])
    return (d * A).change_ring(ZZ).hermite_form(include_zero_rows=False).change_ring(QQ) / d


def tensor(B1, e1, B2, e2, kind, rep, tag):
    """Lambda^# = (L_1 (x) L_2) cap U (basis Ub in L_1 (x) L_2), its Gram matrix Gd for G_1 (x) G_2, and the
    matrices of 1, f_1, f_2, f_1 f_2 (f_i = (1 + sqrt p_i)/2) on Lambda^#.
    Lambda^# = (L_1 ⊗ L_2) ∩ U（L_1 ⊗ L_2 の中の基底 Ub）、G_1 ⊗ G_2 での Gram 行列 Gd、Lambda^# 上の 1, f_1, f_2, f_1 f_2 の行列。"""
    from sage.all import QQ, ZZ, block_matrix, identity_matrix, matrix
    X1, X2 = B1["X"], B2["X"]
    n1, n2 = B1["G"].nrows(), B2["G"].nrows()
    I1, I2 = identity_matrix(ZZ, n1), identity_matrix(ZZ, n2)

    def on(B, X, h):
        R = B["Lb"] * hmat(X, h) * B["Lb"].inverse()
        require(all(x in ZZ for x in R.list()), "the order acts integrally on the lattice")
        return R.change_ring(ZZ)
    s1, s2 = obasis(X1, *e1, kind), obasis(X2, *e2, kind)
    rel = [on(B1, X1, a).tensor_product(I2) - I1.tensor_product(on(B2, X2, hstar(X2, b))) for a, b in zip(s1, s2)]
    R = block_matrix(ZZ, [[r] for r in rel], subdivide=False)               # relation vectors (rows) / 関係式（行）
    Gt = B1["G"].tensor_product(B2["G"])
    Ub = block_matrix(ZZ, [rel], subdivide=False).left_kernel().basis_matrix()   # (L_1 (x) L_2) cap U
    r = n1 * n2 // 4
    rep.check(f"{tag}: rank of L_1 (x)_O L_2 is {r}", Ub.nrows() == r)
    rep.check(f"{tag}: the relations span U^perp (orthogonal to U, rank {n1 * n2 - r})",
              R.rank() == n1 * n2 - r and (R * Gt * Ub.transpose()).is_zero())
    sat = matrix(ZZ, (Gt * Ub.transpose())).left_kernel().basis_matrix()    # (L_1 (x) L_2) cap U^perp
    rep.check(f"{tag}: the relation module is saturated (L_1 (x)_O L_2 has no torsion)", hnf(R) == hnf(sat))
    Gd = Ub * Gt * Ub.transpose()

    def cen(B, X):
        return on(B, X, (X.one + X.hcoords((X.sqrtp, X.F(0)))) / 2)
    C1, C2 = cen(B1, X1), cen(B2, X2)
    UbT = matrix(QQ, Ub.transpose())
    Cs = []
    for O_ in (I1.tensor_product(I2), C1.tensor_product(I2), I1.tensor_product(C2), C1.tensor_product(C2)):
        C = UbT.solve_right(matrix(QQ, (Ub * O_).transpose())).transpose()
        Cs.append(C)
    rep.check(f"{tag}: Lambda^# is stable under O_K'", all(x in ZZ for C in Cs for x in C.list()))
    return Gd, [C.change_ring(ZZ) for C in Cs]


def field(p1, p2):
    """K' = Q(sqrt p1, sqrt p2) as an absolute field, with the integral basis 1, f1, f2, f1 f2.
    K' = Q(√p1, √p2)（絶対体）と整基底 1, f1, f2, f1 f2。"""
    from sage.all import QQ, NumberField, PolynomialRing
    x = PolynomialRing(QQ, "x").gen()
    K = NumberField([x ** 2 - x - (p1 - 1) // 4, x ** 2 - x - (p2 - 1) // 4], names="f1,f2")
    Ka = K.absolute_field("t")
    fr = Ka.structure()[1]
    f1, f2 = [fr(g) for g in K.gens()]
    return Ka, [Ka(1), f1, f2, f1 * f2]


def class_groups(p1, p2):
    Ka, _ = field(p1, p2)
    return Ka.class_group(proof=True).invariants(), Ka.narrow_class_group(proof=True).invariants()


def analyse(p1, p2, Gd, Cs, rep, tag, control):
    """Find a with Lambda^# = Lambda a; decide whether its narrow class is a square. For the control, build
    the unimodular form and return its Gram matrix.
    Lambda^# = Lambda a となる a を求め、狭義類が平方かどうかを決める。対照ではユニモジュラーな形式の Gram 行列を返す。"""
    from sage.all import AA, QQ, ZZ, factor, identity_matrix, matrix, prod, vector
    Ka, bas = field(p1, p2)
    Bm = matrix(QQ, [list(b.vector()) for b in bas])
    n = Gd.nrows()
    Gdi = Gd.inverse()                              # basis of Lambda in the coordinates of Lambda^# / Lambda の基底

    def op(x):                                      # action of x in K' on Lambda^# (row vectors) / K' の元の作用
        co = Bm.solve_left(vector(QQ, list(x.vector())))
        return sum(QQ(c) * C for c, C in zip(co, Cs))
    idx = abs(Gd.det())                             # [Lambda : Lambda^#]
    Na = ZZ(round(float(idx) ** (4.0 / n)))
    rep.check(f"{tag}: [Lambda : Lambda^#] = {factor(idx)} is the {n // 4}-th power of an integer", QQ(Na) ** (n // 4) == idx)
    target = hnf(identity_matrix(QQ, n))
    found = [I for I in Ka.ideals_of_bdd_norm(Na)[Na]
             if hnf(matrix(QQ, sum([list((Gdi * op(g)).rows()) for g in I.gens()], []))) == target]
    rep.check(f"{tag}: exactly one ideal a of O_K' with Lambda^# = Lambda a", len(found) == 1)
    a = found[0]
    embs = Ka.embeddings(AA)                        # exact real embeddings: e(c) > 0 is decided exactly / 厳密な実埋め込み（符号を厳密に判定）
    ug = [Ka(u) for u in Ka.unit_group(proof=True).gens_values()]

    def positive_generator(I):
        """A totally positive generator of I, or None (units modulo squares suffice).
        I の総正な生成元。無ければ None（単数は平方を法として調べれば足りる）。"""
        if not I.is_principal(proof=True):
            return None
        g0 = I.gens_reduced()[0]
        for es in itertools.product(range(2), repeat=len(ug)):
            c = g0 * prod(u ** k for u, k in zip(ug, es))
            if all(e(c) > 0 for e in embs):
                return c
        return None
    c = positive_generator(a)
    rep.value(f"{tag}: a (factorization); principal; totally positive generator", [str(a.factor()), bool(a.is_principal(proof=True)), str(c)])
    if not control:
        # Cl(K') = Z/2 = narrow Cl(K') (checked in main), so the narrow class group maps isomorphically onto the class
        # group, and the narrow class of a is a square iff it is trivial iff a is principal.
        # Cl(K') = Z/2 = 狭義 Cl(K')（main で確かめた）なので狭義類群は類群に同型に写り、a の狭義類が平方 ⇔ 自明 ⇔ a が単項。
        rep.check(f"{tag}: a is not principal, so its narrow class is not a square and no (Lambda b, F_c) is unimodular",
                  not a.is_principal(proof=True))
        return None
    rep.check(f"{tag}: a has a totally positive generator c", c is not None)
    G = Gdi * op(c)                                 # Gram matrix of (Lambda, F_c) / (Lambda, F_c) の Gram 行列
    ok = G.is_symmetric() and all(x in ZZ for x in G.list()) and G.det() == 1 and all(G[i, i] % 2 == 0 for i in range(n))
    rep.check(f"{tag}: (Lambda, F_c) is even unimodular", ok)
    return G.change_ring(ZZ)


def main():
    import numpy as np
    from lib import enumerate as exact_enum
    from lib import exact
    from p6_reduction import bkz_transform
    ap = argparse.ArgumentParser(description="Nebe's tensor products [Neb98, §5] for (5, 29) and (5, 13)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rep = Report("nebe_tensor", a.out)

    cl = {pq: class_groups(*pq) for pq in [(5, 29), (5, 13), (5, 17)]}
    rep.value("class group and narrow class group of Q(sqrt p, sqrt q)", {f"{p},{q}": [list(c), list(cn)] for (p, q), (c, cn) in cl.items()})
    rep.check("Q(sqrt5, sqrt29): class group Z/2 and narrow class group Z/2", cl[(5, 29)] == ((2,), (2,)))
    rep.check("Q(sqrt5, sqrt13), Q(sqrt5, sqrt17): class number 1, narrow class number 1",
              cl[(5, 13)] == ((), ()) and cl[(5, 17)] == ((), ()))

    base = {p: build(p, rep) for p in (5, 13, 29)}
    rep.check("one class of maximal orders for p = 5 and 13, two for p = 29",
              [len(base[p]) for p in (5, 13, 29)] == [1, 1, 2])
    emb = {}
    for p in (5, 13, 29):
        for B in base[p]:
            for kind in (2, 3):
                U, E = embeddings(B["X"], B["M"], kind)
                B["units"] = len(U)
                emb[(p, B["ci"], kind)] = (U, E, conj_classes(B["X"], U, E) if E else [])
    names = {}
    for B in base[29]:
        k2, k3 = bool(emb[(29, B["ci"], 2)][1]), bool(emb[(29, B["ci"], 3)][1])
        names[B["ci"]] = {24: "M", 12: "M~"}.get(B["units"], "?")
        rep.value(f"p = 29, class {B['ci']}: units of reduced norm 1, contains a maximal order of Q_inf,2 / Q_inf,3",
                  [B["units"], k2, k3])
    rep.check("[Neb98, p. 483]: M (24 units) contains the Hurwitz order and no maximal order of Q_inf,3; "
              "M~ (12 units) a maximal order of Q_inf,3 and not the Hurwitz order",
              sorted(names.values()) == ["M", "M~"]
              and all(bool(emb[(29, ci, 2)][1]) == (nm == "M") and bool(emb[(29, ci, 3)][1]) == (nm == "M~")
                      for ci, nm in names.items()))

    for p1, p2, control in [(5, 13, True), (5, 29, False)]:
        count = 0
        for kind in (2, 3):
            for B1 in base[p1]:
                for B2 in base[p2]:
                    _, _, R1 = emb[(p1, B1["ci"], kind)]
                    _, _, R2 = emb[(p2, B2["ci"], kind)]
                    for i1, e1 in enumerate(R1):
                        for i2, e2 in enumerate(R2):
                            tag = f"({p1},{p2}) S = Q_inf,{kind}, embeddings {i1}/{i2}"
                            if p2 == 29:
                                tag = f"({p1},{p2}) S = Q_inf,{kind} in {names[B2['ci']]}, embeddings {i1}/{i2}"
                            Gd, Cs = tensor(B1, e1, B2, e2, kind, rep, tag)
                            G = analyse(p1, p2, Gd, Cs, rep, tag, control)
                            count += 1
                            if G is not None:
                                # BKZ-20 basis (floating point inside fpylll; U is checked exactly) / BKZ-20 基底（U は厳密に確かめる）
                                Gn = np.array(G.rows(), dtype=np.int64)
                                T = bkz_transform(Gn, 20)
                                require(abs(exact.det_bareiss(T)) == 1, "abs(exact.det_bareiss(T)) == 1")
                                Gr = exact.i64_matmul(exact.i64_matmul(T, Gn), T.T)
                                found, nodes = exact_enum.short_vectors(Gr, 4, os.path.join(rep.out_dir, "build"))
                                rep.check(f"{tag}: no nonzero vector of norm <= 4 ({nodes} nodes), so minimum 6: "
                                          f"Nebe's extremal L_48", len(found) == 0)
        rep.value(f"({p1},{p2}): pairs of embedding classes treated", count)
        kinds = (2, 3) if p2 == 29 else (2,)        # 3 splits in Q(sqrt13) / 3 は Q(√13) で分解する
        rep.check(f"({p1},{p2}): at least one pair of embedding classes for S = " + ", ".join(f"Q_inf,{k}" for k in kinds),
                  all(emb[(p1, B1["ci"], k)][2] and any(emb[(p2, B2["ci"], k)][2] for B2 in base[p2])
                      for k in kinds for B1 in base[p1]))
    rep.finish()


if __name__ == "__main__":
    main()
