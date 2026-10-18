"""The genus of rank-2 unimodular Hermitian lattices over M (supplementary/genus/genus.py): the class Genus (the
ambient space H^2, Lambda_0 = M + M, Kneser neighbours, the lattices X = L tensor_M Lambda) and small helpers.
Requires SageMath (imported inside the functions).
M 上の階数 2 のユニモジュラーなエルミート格子の種（supplementary/genus/genus.py）: クラス Genus（周囲の空間 H^2、Λ_0 = M ⊕ M、Kneser の近傍、
格子 X = L ⊗_M Λ）と小さな補助関数。SageMath が要る（関数の中で読み込む）。
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "nebe"))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "produce"))
from genus_data import N  # noqa: E402
from lib import require  # noqa: E402

def rmul(X, h):
    """Matrix of right multiplication by h in H (coordinates) on Q(zeta)^2 = Q^56 (row vectors).
    H の元 h（座標）の右乗法の、Q(ζ)^2 = Q^56 の行ベクトルへの行列。"""
    from sage.all import QQ, block_matrix
    ux, uy = X.helt(h)
    mul = X._mulmat
    return block_matrix(QQ, [[mul(ux), mul(uy)], [-mul(X.conj(uy)), mul(X.conj(ux))]], subdivide=False)


def star(X, h):
    """The canonical involution h -> h*. / 標準対合 h -> h*。"""
    x, y = X.helt(h)
    return X.hcoords((X.conj(x), -y))


def trtrd(u):
    """Tr_{K/Q} trd(u) for u in H (coordinates); Tr eta_j = -1. / H の元 u の Tr_{K/Q} trd(u)（Tr η_j = -1）。"""
    return -(u[0] + u[1] + u[2] + u[3])


def kelt(X, a, b):
    """The element a + b sqrt29 of K, in coordinates of H. / K の元 a + b√29 を H の座標で。"""
    return a * X.one + b * X.hcoords((X.sqrtp, X.F(0)))


def kred(ab):
    """Reduction of A + B sqrt29 modulo p = (pi), pi = (7 + sqrt29)/2: F_5 with sqrt29 -> 3.
    A + B√29 の p = (π) での剰余（F_5、√29 ↦ 3）。"""
    from sage.all import GF
    A, B = ab
    return GF(5)(A) + 3 * GF(5)(B)


def _hnf_rational(S):
    from sage.all import ZZ, lcm
    d = lcm([x.denominator() for x in S.list()])
    return (d * S).change_ring(ZZ).hermite_form(include_zero_rows=False).change_ring(S.base_ring()) / d


class Genus:
    r"""The ambient space H^2 with h = l_1 m_1* + l_2 m_2*, the lattice Lambda_0 = M + M, and Kneser neighbours.
    周囲の空間 H^2（h = l_1 m_1* + l_2 m_2*）、基準の格子 Λ_0 = M ⊕ M、Kneser の近傍。"""

    def __init__(self, out_dir):
        from cycloquat import CycloQuat
        from lattices import read_mats
        from sage.all import QQ, ZZ, block_matrix, matrix, vector, zero_matrix
        d = os.path.join(out_dir, "nebe")
        self.X = X = CycloQuat(29)
        self.M = M = read_mats(os.path.join(d, "M_order.txt"), 8, QQ)[0]       # Z-basis of M (rows, H coordinates)
        self.Lb = read_mats(os.path.join(d, "M_basis.txt"), N, QQ)[0]          # basis of L in Q(zeta)^2
        self.G = read_mats(os.path.join(d, "M_gram.txt"), N)[0]                # Gram matrix of L in that basis
        self.Z, self.W = read_mats(os.path.join(d, "M_generators.txt"), N)     # z, w on L
        Z8 = zero_matrix(QQ, 8, 8)
        self.P0 = block_matrix(QQ, [[M, Z8], [Z8, M]], subdivide=False)        # basis of Lambda_0 in H^2
        rows = [vector(QQ, list(r[:8])) for r in self.P0.rows()], [vector(QQ, list(r[8:])) for r in self.P0.rows()]
        Z8v = vector(QQ, 8)
        mul = lambda u, v: X.hmul(u, v) + Z8v                                    # noqa: E731 (empty sum -> 0)
        self.mul = mul
        self.h = [[mul(rows[0][i], star(X, rows[0][j])) + mul(rows[1][i], star(X, rows[1][j])) for j in range(16)]
                  for i in range(16)]
        TM = matrix(QQ, 8, 8, lambda i, j: trtrd(mul(M[i], M[j])))
        self.Mdual = TM.inverse() * M                                            # Tr trd(m_i n_j) = delta_ij
        self.form = lambda a: matrix(QQ, 16, 16, lambda i, j: trtrd(mul(a, self.h[i][j])))   # noqa: E731
        self.F0 = self.form(X.one)                                               # Tr trd h, positive definite
        self.Fm = [self.form(m) for m in M.rows()]
        self.D = [self.form(n) for n in self.Mdual.rows()]                       # h(x, y) in M iff all integral
        Pinv = self.P0.inverse()
        self.Lm = [(self.P0 * block_matrix(QQ, [[X.lmul_matrix(m), Z8], [Z8, X.lmul_matrix(m)]], subdivide=False) * Pinv)
                   for m in M.rows()]
        require(all(x in ZZ for A in self.Lm for x in A.list()), "all(x in ZZ for A in self.Lm for x in A.list())")
        self.Lm = [A.change_ring(ZZ) for A in self.Lm]
        self.d0 = self.F0.det()
        require(X.nrd(X.hcoords((X.sqrtp, X.F(0)))) == (29, 0), "X.nrd(X.hcoords((X.sqrtp, X.F(0)))) == (29, 0)")
        self.pi = kelt(X, QQ(7) / 2, QQ(1) / 2)                                  # pi = (7 + sqrt29)/2, norm 5
        self.pinv = kelt(X, QQ(7) / 10, -QQ(1) / 10)                             # pi~/5
        require(X.hmul(self.pi, self.pinv) == X.one, "X.hmul(self.pi, self.pinv) == X.one")
        self.Dpi = [self.form(X.hmul(n, self.pinv)) for n in self.Mdual.rows()]
        self.Lpi, self.Lpinv = self.lmul(self.pi), self.lmul(self.pinv)
        # A rank-1 idempotent of M/pM = M_2(F_5): trd = 1, nrd = 0 mod p (fixed seed).
        # M/pM ≅ M_2(F_5) の階数 1 の冪等元: trd ≡ 1, nrd ≡ 0 (mod p)（乱数シードは固定）。
        rng = random.Random(1)
        while True:
            c = vector(QQ, [rng.randint(-2, 2) for _ in range(8)])
            m = c * M
            n = X.nrd(m)
            t = X.nrd(X.one + m)
            tr = (t[0] - n[0] - 1, t[1] - n[1])
            if kred(n) == 0 and kred(tr) == 1:
                break
        self.e = m
        self.Le = self.lmul(m)
        require(all(x in ZZ for x in self.Le.list()) and all(x in ZZ for x in self.Lpi.list()),
                "left multiplication by e and by pi preserves Lambda_0")
        Lbi = self.Lb.inverse()
        self.R = lambda q: self.Lb * rmul(X, q) * Lbi                            # noqa: E731 (right mult. on L)

    def lmul(self, a):
        """Left multiplication by a in H (Lambda_0 coordinates). / 左から a ∈ H を掛ける写像（Λ_0 座標）。"""
        from sage.all import QQ, block_matrix, zero_matrix
        Z8 = zero_matrix(QQ, 8, 8)
        A = self.X.lmul_matrix(a)
        return self.P0 * block_matrix(QQ, [[A, Z8], [Z8, A]], subdivide=False) * self.P0.inverse()

    def integral(self, C):
        from sage.all import ZZ
        return all(x in ZZ for Dj in self.D for x in (C * Dj * C.transpose()).list())

    def is_module(self, C):
        from sage.all import ZZ
        Ci = C.inverse()
        return all(x in ZZ for A in self.Lm for x in (C * A * Ci).list())

    def is_unimodular(self, C):
        return self.integral(C) and (C * self.F0 * C.transpose()).det() == self.d0

    def forms(self, C):
        """The nine integral forms [Tr trd h, Tr trd(m_k h)] on Lambda. / Λ 上の 9 個の整数値の形式。"""
        from sage.all import ZZ
        return [(C * F * C.transpose()).change_ring(ZZ) for F in [self.F0] + self.Fm]

    def random_sub(self, C, rng):
        """pi Lambda < N < Lambda with N / pi Lambda generated (as an M-module) by a random 2-dimensional
        subspace of e(Lambda / pi Lambda). / N/πΛ が e(Λ/πΛ) の無作為な 2 次元部分空間から（M-加群として）生成される πΛ ⊂ N ⊂ Λ。"""
        from sage.all import GF, ZZ, identity_matrix, matrix
        F = GF(5)
        Ci = C.inverse()
        Pi = (C * self.Lpi * Ci).change_ring(ZZ)
        E = (C * self.Le * Ci).change_ring(ZZ)
        Lm = [(C * A * Ci).change_ring(ZZ) for A in self.Lm]
        Pb = Pi.change_ring(F).row_space()
        require(Pb.dimension() == 8, "Pb.dimension() == 8")
        V = F ** 16
        Q = V.quotient(Pb)
        Ue = [Q.lift(Q(r)) for r in E.change_ring(F).row_space().basis()]
        Ue = matrix(F, [Q.lift(x) for x in matrix(F, [Q(u) for u in Ue]).row_space().basis()])
        require(Ue.nrows() == 4, "Ue.nrows() == 4")
        while True:
            Wm = matrix(F, 2, 4, [F(rng.randrange(5)) for _ in range(8)])
            if Wm.rank() == 2:
                break
        w = Wm * Ue
        gens = [w[i] * A.change_ring(F) for i in range(2) for A in [identity_matrix(ZZ, 16)] + Lm]
        S = matrix(F, gens).row_space() + Pb
        require(S.dimension() == 12, "S.dimension() == 12")
        rows = matrix(ZZ, [[ZZ(x) for x in r] for r in S.basis()]).stack(5 * identity_matrix(ZZ, 16))
        Nb = rows.hermite_form(include_zero_rows=False)
        return Nb.change_ring(C.base_ring()) * C

    def neighbour(self, C, rng, tries=200):
        """A p-neighbour of Lambda (Siegel type). / Λ の p-近傍（Siegel 型）。"""
        from sage.all import ZZ
        for _ in range(tries):
            Nn = self.random_sub(C, rng)
            if all(x in ZZ for Dj in self.Dpi for x in (Nn * Dj * Nn.transpose()).list()):
                break
        else:
            raise RuntimeError("no Lagrangian N found")
        Np = Nn * self.Lpinv
        for _ in range(tries):
            C2 = self.random_sub(Np, rng)
            if not self.integral(C2):
                continue
            if abs(C.det()) / abs(_hnf_rational(C.stack(C2)).det()) == 5 ** 4:
                return C2
        raise RuntimeError("no neighbour found")

    def reduce(self, C):
        """LLL-reduced basis for Tr trd h. / Tr trd h について LLL 簡約した基底。"""
        from sage.all import ZZ, matrix, pari
        Gm = (C * self.F0 * C.transpose()).change_ring(ZZ)
        return matrix(ZZ, pari(Gm).qflllgram().mattranspose().sage()) * C

    def aut(self, C):
        from sage.all import ZZ, pari
        return ZZ(pari(self.forms(C)).qfauto()[0])

    def iso(self, C1, C2):
        from sage.all import pari
        return pari(self.forms(C1)).qfisom(pari(self.forms(C2))) != 0

    def invariant(self, C, bound=14):
        """Numbers of +-pairs of vectors of Tr trd h = 2, 4, ..., bound. / Tr trd h = 2, 4, …, bound の ± 対の本数。"""
        from sage.all import ZZ, pari, vector
        Gm = (C * self.F0 * C.transpose()).change_ring(ZZ)
        vs = pari(Gm).qfminim(bound)[2]
        cnt = [0] * (bound // 2 + 1)
        for j in range(len(vs)):
            v = vector(ZZ, [ZZ(t) for t in vs[j]])
            cnt[int(v * Gm * v) // 2] += 1
        return tuple(cnt[1:])

    def short(self, C, bound):
        """Vectors of Lambda with Tr trd h <= bound (one of each +-pair), in Lambda_0 coordinates.
        Tr trd h ≤ bound の Λ のベクトル（± の片方）、Λ_0 座標。"""
        from sage.all import ZZ, pari, vector
        Gm = (C * self.F0 * C.transpose()).change_ring(ZZ)
        vs = pari(Gm).qfminim(bound)[2]
        return [vector(ZZ, [ZZ(t) for t in vs[j]]) * C for j in range(len(vs))]

    def hval(self, Fs, v):
        """h(v, v) in K as (A, B) = A + B sqrt29: Tr trd h = 4A, Tr trd(sqrt29 h) = 116B.
        h(v, v) ∈ K を (A, B) = A + B√29 で。"""
        from sage.all import QQ
        return (QQ(v * self.F0 * v) / 4, QQ(v * Fs * v) / 116)

    def saturate(self, C, v):
        """J = Lambda cap H v (Lambda_0 coordinates). / J = Λ ∩ Hv（Λ_0 座標）。"""
        from sage.all import QQ, ZZ, identity_matrix, lcm, matrix
        Ci = C.inverse()
        V = matrix(QQ, [v * self.lmul(b) for b in identity_matrix(QQ, 8).rows()]) * Ci
        d = lcm([x.denominator() for x in V.list()])
        Jz = (d * V).change_ring(ZZ).row_module().basis_matrix().saturation()
        return Jz.change_ring(QQ) * C

    def build_X(self, C):
        """(B, G_X): basis of X = L tensor_M Lambda in the coordinates of L + L (basis Lb), Gram matrix for
        diag(G, G); then LLL-reduced. / X = L ⊗_M Λ の L ⊕ L 座標での基底と Gram 行列（diag(G, G)）。LLL 簡約したもの。"""
        from sage.all import QQ, ZZ, block_matrix, lcm, matrix, pari, zero_matrix
        Hc = C * self.P0
        blocks = [self.R(r[:8]).augment(self.R(r[8:])) for r in Hc.rows()]     # rows x_k tensor lambda
        Gen = block_matrix(QQ, [[b] for b in blocks], subdivide=False)
        d = lcm([x.denominator() for x in Gen.list()])
        Bx = (d * Gen).change_ring(ZZ).hermite_form(include_zero_rows=False).change_ring(QQ) / d
        G2 = block_matrix(QQ, [[self.G, zero_matrix(QQ, N, N)], [zero_matrix(QQ, N, N), self.G]], subdivide=False)
        Gx = Bx * G2 * Bx.transpose()
        require(all(x in ZZ for x in Gx.list()), "all(x in ZZ for x in Gx.list())")
        U = matrix(ZZ, pari(Gx.change_ring(ZZ)).qflllgram().mattranspose().sage())
        require(abs(U.det()) == 1, "abs(U.det()) == 1")
        Bx = U * Bx
        return Bx, (Bx * G2 * Bx.transpose()).change_ring(ZZ)

    def unit_actions(self, C):
        """Generators of U(Lambda) (qfauto) as matrices on L + L: u acts on Lambda by right multiplication by
        Q in GL_2(H), and on X by id tensor u. / U(Λ) の生成元（qfauto）を L ⊕ L 上の行列として。"""
        from sage.all import QQ, ZZ, block_matrix, matrix, pari, zero_matrix
        X = self.X
        gens = pari(self.forms(C)).qfauto()[1]
        out = []
        for g in gens:
            g = matrix(ZZ, g.sage())
            U0 = C.inverse() * g.transpose() * C
            T = self.P0.inverse() * U0 * self.P0
            Q = [[X.one * T[8 * a:8 * a + 8, 8 * b:8 * b + 8] for b in range(2)] for a in range(2)]
            for a in range(2):
                for b in range(2):
                    Rq = X.rmul_matrix(Q[a][b]) if Q[a][b] != 0 else zero_matrix(QQ, 8, 8)
                    require(Rq == T[8 * a:8 * a + 8, 8 * b:8 * b + 8], "not a right multiplication")
            Rb = [[self.R(Q[a][b]) for b in range(2)] for a in range(2)]
            out.append(block_matrix(QQ, Rb, subdivide=False))
        return out


def closure(gens, n):
    """All elements of the finite group generated by integer matrices. / 整数行列が生成する有限群の全元。"""
    from sage.all import ZZ, identity_matrix
    Id = identity_matrix(ZZ, n)
    elts = {tuple(Id.list()): Id}
    fr = [Id]
    while fr:
        nf = []
        for a in fr:
            for g in gens:
                b = a * g
                k = tuple(b.list())
                if k not in elts:
                    elts[k] = b
                    nf.append(b)
        fr = nf
    return list(elts.values())


def order_of(u, n):
    from sage.all import ZZ, identity_matrix
    Id = identity_matrix(ZZ, n)
    o, P = 1, u
    while P != Id:
        P, o = P * u, o + 1
    return o
