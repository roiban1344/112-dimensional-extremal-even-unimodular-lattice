"""Basic exact checks on the data (integer arithmetic only; a few seconds).

  L     : 56-dimensional lattice, Gram matrix G            (data/L56_gram.txt)
  g1,g2 : generators of SL_2(29) acting on L               (data/sl2_29_generators.txt)
  tau   : endomorphism of L with tau^2 = -5                (data/tau.txt)
  R     : {(x, x*tau + 2y)/sqrt(2) : x, y in L}, rank 112  (constructed here; data/R112_gram_LLL.txt is an LLL-reduced copy)

Row-vector convention: a matrix M acts by x -> x*M, and isometries satisfy M G M^T = G.
Run:  sage -python verify/01_basic.py      (from the repository root)
"""
from pathlib import Path
from sage.all import ZZ, matrix, identity_matrix, block_matrix, zero_matrix

DATA = Path(__file__).resolve().parent.parent / "data"


def read(name, n, count=1):
    rows = [[int(v) for v in line.split()] for line in (DATA / name).read_text().splitlines() if line.strip() and not line.startswith("#")]
    assert len(rows) == n * count and all(len(r) == n for r in rows), name
    mats = [matrix(ZZ, rows[i * n:(i + 1) * n]) for i in range(count)]
    return mats[0] if count == 1 else mats


def check(label, ok):
    print(f"[{'ok' if ok else 'FAIL'}] {label}")
    assert ok, label


n = 56; I = identity_matrix(ZZ, n); Z = zero_matrix(ZZ, n)
G = read("L56_gram.txt", n); g1, g2 = read("sl2_29_generators.txt", n, 2); tau = read("tau.txt", n)

check("L: Gram matrix symmetric, even diagonal, determinant 1, positive definite",
      G.is_symmetric() and all(G[i, i] % 2 == 0 for i in range(n)) and G.det() == 1 and G.is_positive_definite())
check("g1, g2 are isometries of L", g1 * G * g1.transpose() == G and g2 * G * g2.transpose() == G)
check("g1 has order 5, g2 has order 7", g1 ** 5 == I and g1 != I and g2 ** 7 == I and g2 != I)
check("tau^2 = -5", tau * tau == -5 * I)
check("tau is a similitude of norm 5:  tau G tau^T = 5 G", tau * G * tau.transpose() == 5 * G)
check("tau is skew:  tau G = -(tau G)^T   (so (x tau, y) = -(x, y tau))", tau * G == -(tau * G).transpose())
check("tau commutes with g1 and g2", tau * g1 == g1 * tau and tau * g2 == g2 * tau)

# R = {(x, x tau + 2y)/sqrt2}: basis rows (I | tau), (0 | 2I); Gram = B diag(G, G) B^T / 2
B = block_matrix(ZZ, [[I, tau], [Z, 2 * I]])
GR2 = B * block_matrix(ZZ, [[G, Z], [Z, G]]) * B.transpose()
check("R: Gram matrix is integral", all(v % 2 == 0 for v in GR2.list()))
GR = (GR2 / 2).change_ring(ZZ)
check("R: rank 112, even, determinant 1, positive definite",
      GR.nrows() == 112 and all(GR[i, i] % 2 == 0 for i in range(112)) and GR.det() == 1 and GR.is_positive_definite())
check("R: Gram matrix equals [[3G, tau G], [(tau G)^T, 2G]]  (so R = H (x) L with H = [[3, tau], [-tau, 2]], det H = 6 - 5 = 1)",
      GR == block_matrix(ZZ, [[3 * G, tau * G], [(tau * G).transpose(), 2 * G]]))
Binv = B.change_ring(G.base_ring().fraction_field()).inverse()
for name, g in (("g1", g1), ("g2", g2)):
    M = B * block_matrix(ZZ, [[g, Z], [Z, g]]) * Binv
    check(f"R: the diagonal action of {name} preserves R and its Gram matrix", all(v in ZZ for v in M.list()) and M * GR * M.transpose() == GR)
GL = read("R112_gram_LLL.txt", 112)
check("R112_gram_LLL.txt: symmetric, even, determinant 1 (a reduced Gram matrix of the same lattice; isometry is not re-checked here)",
      GL.is_symmetric() and all(GL[i, i] % 2 == 0 for i in range(112)) and GL.det() == 1)
print("all basic checks passed")
