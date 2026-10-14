"""The "ceiling" of constructions that glue k copies of a lattice modulo 2.

If R is built from k copies of an even lattice L of minimum m in such a way that R contains
(0, ..., 0, 2y, 0, ..., 0)/sqrt(2) for every y in L (true for the mod-2 gluing of two copies used here,
and for Quebbemann's construction L(M, N, k) with the Turyn-type case k = 3), then min(R) <= 2m.
So an extremal lattice of dimension k*n can come out of such a construction only if
    mu(k*n) <= 2*mu(n),      mu(n) = 2*floor(n/24) + 2.
This script lists, for k = 2, 3, 4, the dimensions n (multiples of 8) for which this holds.
Pure Python.  Run:  python3 verify/ceiling.py
"""


def mu(n):
    return 2 * (n // 24) + 2


if __name__ == "__main__":
    N = range(8, 241, 8)
    for k in (2, 3, 4):
        ok = [n for n in N if mu(k * n) <= 2 * mu(n)]
        tight = [n for n in ok if mu(k * n) == 2 * mu(n)]
        print(f"k = {k}: possible for n = {ok if len(ok) < len(N) else 'all n in 8..240'}; with no slack (mu(kn) = 2 mu(n)) for n = {tight}")
    assert all(mu(2 * n) <= 2 * mu(n) for n in range(8, 10 ** 5, 8))
    assert all((mu(2 * n) == 2 * mu(n)) == (n % 24 == 16) for n in range(8, 10 ** 5, 8))
    assert [n for n in range(8, 10 ** 5, 8) if mu(3 * n) <= 2 * mu(n)] == [8, 24]
    print("checked for all n < 100000: k = 2 always possible, no slack exactly when n = 16 mod 24; k = 3 only n = 8, 24")
