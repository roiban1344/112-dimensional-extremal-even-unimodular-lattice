"""Siegel mean of the number of "too short" vectors in even unimodular lattices of rank n.

By Siegel's theorem the average of the theta series over all even unimodular lattices of rank n = 2k
(each weighted by 1/|Aut|) is the Eisenstein series E_k = 1 + (2k/|B_k|) * sum_m sigma_{k-1}(m) q^m,
so the mean number of vectors of norm 2m is (2k/|B_k|) * sigma_{k-1}(m).
An extremal lattice has no vectors of norm 2m for 1 <= m <= floor(n/24).  We print

    S(n) = sum_{m=1}^{floor(n/24)} (2k/|B_k|) * sigma_{k-1}(m),

the mean number of vectors that an extremal lattice must not have.  Pure Python, exact arithmetic.
Run:  python3 verify/siegel_mean.py
"""
from fractions import Fraction
from math import comb


def bernoulli(k):
    B = [Fraction(1)]
    for m in range(1, k + 1):
        B.append(-sum(comb(m + 1, j) * B[j] for j in range(m)) / (m + 1))
    return B[k]


def sigma(e, m):
    return sum(d ** e for d in range(1, m + 1) if m % d == 0)


def S(n):
    k = n // 2
    return sum(Fraction(2 * k) / abs(bernoulli(k)) * sigma(k - 1, m) for m in range(1, n // 24 + 1))


if __name__ == "__main__":
    for n in range(24, 145, 8):
        print(f"n = {n:3d}   min of an extremal lattice = {2 * (n // 24) + 2:2d}   S(n) = {float(S(n)):.3g}")
