"""Extremal theta series of even unimodular lattices of rank n = 8k, written as polynomials in
A = theta series of E8 (= Eisenstein series E_4) and B = theta series of the Leech lattice (= E_4^3 - 720*Delta).

The space of modular forms of weight n/2 = 4k for SL_2(Z) has basis A^(k-3j) * B^j (0 <= j <= floor(k/3)).
The extremal theta series is the unique element 1 + 0*q + ... + 0*q^m + a_{m+1} q^{m+1} + ... with m = floor(n/24);
here q^j counts vectors of norm 2j.  An even unimodular lattice is extremal iff its theta series is this one.

Run:  sage -python verify/theta_series.py [n ...]      (needs SageMath; exact rational arithmetic)
      sage -python verify/theta_series.py --table      (the table of the README)
"""
import sys
from sage.all import QQ, PowerSeriesRing, PolynomialRing, eisenstein_series_qexp, delta_qexp, matrix, vector


def extremal_theta(n, prec=8):
    assert n % 8 == 0
    k = n // 8; m = n // 24; prec = max(prec, m + 5)
    A = eisenstein_series_qexp(4, prec, normalization="constant")     # 1 + 240 q + 2160 q^2 + ...
    B = A ** 3 - 720 * delta_qexp(prec)                               # 1 + 196560 q^2 + ...
    basis = [A ** (k - 3 * j) * B ** j for j in range(m + 1)]
    M = matrix(QQ, [[f[i] for i in range(m + 1)] for f in basis])     # rows: basis elements, columns: coefficients of q^0..q^m
    c = M.solve_left(vector(QQ, [1] + [0] * m))
    theta = sum(ci * f for ci, f in zip(c, basis))
    return c, theta


def as_polynomial(n, c):
    k = n // 8
    terms = []
    for j, cj in enumerate(c):
        if cj == 0:
            continue
        a = k - 3 * j
        mon = "".join([f"A^{a}" if a > 1 else ("A" if a == 1 else ""), " " if a and j else "", f"B^{j}" if j > 1 else ("B" if j == 1 else "")]) or "1"
        terms.append((cj, mon))
    s = ""
    for cj, mon in terms:
        sign = "-" if cj < 0 else "+"
        co = "" if abs(cj) == 1 and mon != "1" else f"({abs(cj)}) " if abs(cj).denominator() != 1 else f"{abs(cj)} "
        s += f" {sign} {co}{mon}"
    return s.strip().lstrip("+ ").strip()


def tex_polynomial(n, c):
    """TeX for the polynomial in A, B, written as (1/N) * (polynomial with integer coefficients), N = common denominator."""
    from sage.all import lcm, ZZ
    k = n // 8; N = lcm([cj.denominator() for cj in c]); out = ""
    for j, cj in enumerate(c):
        cj = ZZ(cj * N)
        if cj == 0:
            continue
        a = k - 3 * j
        mon = (("A" if a == 1 else f"A^{{{a}}}") if a else "") + (("B" if j == 1 else f"B^{{{j}}}") if j else "")
        co = "" if abs(cj) == 1 else str(abs(cj))
        out += (" - " if cj < 0 else (" + " if out else "")) + co + mon
    out = out.strip()
    return out if N == 1 else rf"\tfrac{{1}}{{{N}}}\left({out}\right)"


def markdown_table(ns, nterms=3):
    """Rows of the table in the README (GitHub-flavoured Markdown with TeX)."""
    for n in ns:
        c, th = extremal_theta(n); m = n // 24
        terms = " + ".join(f"{th[i]}q" + ("" if i == 1 else f"^{{{i}}}") for i in range(m + 1, m + 1 + nterms))
        b = "**" if n == 112 else ""
        print(f"| {b}{n}{b} | {b}{2 * m + 2}{b} | ${tex_polynomial(n, c)}$ | $1 + {terms} + \\cdots$ |")


if __name__ == "__main__":
    if "--table" in sys.argv:
        markdown_table(list(range(8, 121, 8))); sys.exit()
    ns = [int(a) for a in sys.argv[1:]] or list(range(8, 121, 8))
    for n in ns:
        c, th = extremal_theta(n)
        m = n // 24
        coeffs = [th[i] for i in range(m + 4)]
        assert all(x.denominator() == 1 for x in coeffs)
        print(f"n = {n:3d}  min = {2 * m + 2:2d}  kissing number = {coeffs[m + 1]}")
        print(f"   theta = {as_polynomial(n, c)}")
        print("         = 1 + " + " + ".join(f"{coeffs[i]} q^{i}" for i in range(m + 1, m + 4)) + " + ...")
