"""Hermitian tensor products over O_K, K = Q(sqrt(-d)), for route T (supplement §S4.1; Table D2 [C20]).
Used by classify.py.
経路 T のための O_K 上のエルミートテンソル積（補遺 §S4.1、表 D2 の [C20]）。classify.py が使う。

Conventions / 約束:
  * O_K = Z[omega], omega = (1 + sqrt(-d))/2 (d = 3 mod 4) or sqrt(-d); omega^2 = t omega - n.
  * A lattice is a pair (G, A): an integral real Gram matrix G and an integral matrix A of
    multiplication by omega (row vectors: omega x = x A), with A^2 = t A - n and A G = G (t - A)^T.
    It need not be free over O_K.
  * The hermitian form h is determined by (x, y) = Tr_{K/Q} h(x, y), so (x, x) = 2 h(x, x).
  * 格子は (G, A) の対（整数の実 Gram 行列 G と、omega 倍の整数行列 A。行ベクトルで omega x = x A）。O_K 上自由でなくてよい。
    エルミート形式 h は (x, y) = Tr h(x, y) で決まる。

Requires SageMath. / SageMath が要る。
"""
from sage.all import ZZ, QQ, QuadraticField, matrix, vector, pari, identity_matrix


def omega(d):
    """ω² = tω - n となる (t, n)。"""
    return (1, (d + 1) // 4) if d % 4 == 3 else (0, d)


def is_structure(G, A, d):
    t, n = omega(d); I = identity_matrix(ZZ, G.nrows())
    return A * A == t * A - n * I and A * G == G * (t * I - A).transpose()


def hermitian_parts(G, A, d):
    """h(x, y) = x·P1·yᵀ + √-d · x·Q1·yᵀ となる有理行列 (P1, Q1)。"""
    P1 = G.change_ring(QQ) / 2
    Q1 = (P1 - A * G) / d if d % 4 == 3 else -(A * G).change_ring(QQ) / (2 * d)
    return P1, Q1


def hermitian_gram(G, A, d, rows):
    """行ベクトルの組 rows の、K 成分のエルミート Gram 行列 (h(x_i, x_j))。"""
    K = QuadraticField(-d, "s"); s = K.gen(); B = matrix(QQ, rows)
    P1, Q1 = hermitian_parts(G, A, d)
    return (B * P1 * B.transpose()).change_ring(K) + s * (B * Q1 * B.transpose()).change_ring(K)


def k_independent_rows(A):
    """単位ベクトルのうち K 上独立なもの n/2 本の添字と、(B; BA) の逆行列。"""
    n = A.nrows(); I = identity_matrix(ZZ, n); rows = []
    for i in range(n):
        trial = rows + [i]; B = I.matrix_from_rows(trial)
        if B.stack(B * A).rank() == 2 * len(trial):
            rows = trial
        if len(rows) == n // 2:
            break
    B = I.matrix_from_rows(rows)
    return B, B.stack(B * A).change_ring(QQ).inverse()


class HermTensor:
    """P ⊗_{O_K} Q を、どちらの因子も O_K-自由と仮定せずに作る。

    R         : 実 Gram 行列（整数になることを確かめる）。次元は rank_Z(P)·rank_Z(Q)/2。
    tens(x, y): x ⊗ y の座標（内部の Q-基底。R の基底に直すには coords）。
    """
    def __init__(self, G1, A1, G2, A2, d):
        assert is_structure(G1, A1, d) and is_structure(G2, A2, d)
        self.d = d; self.t, self.nrm = omega(d)
        self.G1, self.A1, self.G2, self.A2 = G1, A1, G2, A2
        self.n1 = n1 = G1.nrows(); self.n2 = n2 = G2.nrows(); self.r1 = n1 // 2; self.r2 = n2 // 2
        self.K = K = QuadraticField(-d, "s"); s = K.gen()
        self.w = w = (1 + s) / 2 if self.t == 1 else s
        self.B1, self.C1 = k_independent_rows(A1); self.B2, self.C2 = k_independent_rows(A2)
        H = hermitian_gram(G1, A1, d, self.B1.rows()).tensor_product(hermitian_gram(G2, A2, d, self.B2.rows()))
        k = self.r1 * self.r2; self.k = k; wb = w.conjugate()
        tr = lambda x: QQ(x.trace())
        Gq = matrix(QQ, 2 * k, 2 * k)
        for a in range(k):
            for b in range(k):
                x = H[a, b]
                Gq[a, b] = tr(x); Gq[a, k + b] = tr(x * wb); Gq[k + a, b] = tr(w * x); Gq[k + a, k + b] = tr(w * wb * x)
        self.Gq = Gq
        gens = [self.tens(x, y) for x in identity_matrix(ZZ, n1).rows() for y in identity_matrix(ZZ, n2).rows()]
        Mg = matrix(QQ, gens); den = Mg.denominator()
        Bz = (den * Mg).change_ring(ZZ).hermite_form(include_zero_rows=False)
        assert Bz.nrows() == 2 * k
        self.B = Bz.change_ring(QQ) / den; self.Binv = self.B.inverse()
        self.R = (self.B * Gq * self.B.transpose()).change_ring(ZZ)

    def _kcoords(self, v, C, r):
        c = vector(QQ, v) * C
        return [c[i] + c[r + i] * self.w for i in range(r)]

    def tens(self, x, y):
        out0 = []; out1 = []
        for a in self._kcoords(x, self.C1, self.r1):
            for b in self._kcoords(y, self.C2, self.r2):
                u, v = (a * b).list()                      # u + v√-d
                if self.t == 1:                            # = (u - v) + 2v ω
                    out0.append(u - v); out1.append(2 * v)
                else:
                    out0.append(u); out1.append(v)
        return vector(QQ, out0 + out1)

    def coords(self, v):
        """内部座標 → R の基底に関する整数座標。"""
        return (v * self.Binv).change_ring(ZZ)


def exact_minimum(G, below):
    """ノルム < below のベクトルがあれば (最小ノルム, その係数ベクトル)、無ければ None（PARI qfminim の全列挙。次元 40 程度まで）。

    qfminim の flag 1 は「境界以下のベクトルを 1 本」返すだけで最短とは限らないので、見つかったノルム未満で探し直す。"""
    T = matrix(ZZ, pari(G).qflllgram()); Gl = T.transpose() * G * T
    q = pari(Gl).qfminim(below - 1, 1, 0)
    if int(q[0]) == 0:
        return None
    while True:
        v = vector(ZZ, [int(x) for x in q[2][0]]); nv = int(v * Gl * v)
        q2 = pari(Gl).qfminim(nv - 1, 1, 0)
        if int(q2[0]) == 0:
            break
        q = q2
    c = T * v
    return int(c * G * c), c
