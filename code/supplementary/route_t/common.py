"""Shared definitions for route T (supplement §S4, Table D2 [C20], [C21]): the list of classes of searches (2)
and (3), in a fixed order, and the lemma's allowed norms.
経路 T（補遺 §S4、表 D2 の [C20], [C21]）の共通の定義: 探索 (2)・(3) の類の一覧（順序は固定）と、補題が許すノルム。

Search (3): for each of the 656 orbit representatives r of minimal vectors, each kept unit u_k and
mu in (tau, 1 + tau), the class r u_k mu + 2L. 656 x 3 x 2 = 3,936 classes, in the order
(r, k, mu) with mu fastest. Target norms 6 and 10 for mu = tau, 8 for mu = 1 + tau.
Search (2): for each of the 254,664 representatives x_i of norm-8 orbits and each kept unit u_k, the
class x_i u_k (1 + tau) + 2L. 254,664 x 3 = 763,992 classes, in the order (i, k) with k fastest.
Target norm 8 (and 0).
探索 (3): 最小ベクトルの軌道代表 656 個 r、残す単数 u_k、mu ∈ (tau, 1 + tau) について類 r u_k mu + 2L。656 × 3 × 2 = 3,936 類、
(r, k, mu) の順（mu が最も速く回る）。目標ノルムは mu = tau で 6 と 10、mu = 1 + tau で 8。
探索 (2): ノルム 8 の軌道代表 254,664 個 x_i と残す単数 u_k について類 x_i u_k (1 + tau) + 2L。254,664 × 3 = 763,992 類、
(i, k) の順（k が速く回る）。目標ノルムは 8（と 0）。

Kept units: C/{+-1} has 6 elements u_0..u_5 (certificates/centralizer.npz). If u_a anticommutes with tau,
the classes for u and u u_a are related by an automorphism of the setting, and only the one with the
smaller index is kept (3 of the 6).
残す単数: C/{±1} は 6 元 u_0..u_5（certificates/centralizer.npz）。tau と反可換な u_a があれば、u と u u_a の類は対応するので、
添字の小さい方だけを残す（6 個中 3 個）。

Lemma (L even unimodular with minimum 6; paper §5, Corollary 5.3 and its variant): let w0 lie in the class
and |<w0, y>| <= 6 for every minimal vector y. If <w0, w0> is 12, 16 or 20, the class has no vector of
norm 8 (and is not 2L); if <w0, w0> is 14 or 18, the class has no vector of norm 6 or 10.
補題（L は偶ユニモジュラー、最小 6。論文 §5 の系 5.3 とその変形）: w0 が類に入り、すべての最小ベクトル y で |<w0, y>| ≤ 6 とする。
<w0, w0> が 12, 16, 20 なら類にノルム 8 の元は無い（2L でもない）。14, 18 なら類にノルム 6・10 の元は無い。
"""
import numpy as np

N_SEARCH3, N_SEARCH2 = 3936, 763992
ALLOWED = {"8": (12, 16, 20), "6/10": (14, 18)}


def kept_units(U, t):
    """Indices of the kept units (see above). / 残す単数の添字（上の説明）。"""
    anti = [k for k, u in enumerate(U) if (u @ t == -(t @ u)).all()]
    if not anti:
        return list(range(len(U)))
    ua = U[anti[0]]
    keep = []
    for j, u in enumerate(U):
        v = u @ ua
        p = [k for k, w in enumerate(U) if (w == v).all() or (w == -v).all()]
        if not p or min(j, p[0]) == j:
            keep.append(j)
    return keep


def search3_classes(R6, U, t):
    """(starting vectors, targets) for search (3), in the fixed order. / 探索 (3) の (始点, 目標)。固定の順序。"""
    keep = kept_units(U, t)
    mus = (("tau", t, "6/10"), ("1+tau", np.eye(56, dtype=np.int64) + t, "8"))
    starts, targets = [], []
    for r in R6:
        for k in keep:
            for _, mu, tg in mus:
                starts.append(r @ U[k] @ mu)
                targets.append(tg)
    return np.array(starts, dtype=np.int64), targets


def search2_starts(X, U, t, keep, p):
    """Starting vectors x_i u_k (1 + tau) of the classes with numbers p (an array) of search (2).
    探索 (2) の番号 p（配列）の類の始点 x_i u_k (1 + tau)。"""
    p = np.asarray(p)
    i, j = p // len(keep), p % len(keep)
    out = np.empty((len(p), 56), dtype=np.int64)
    one_t = np.eye(56, dtype=np.int64) + t
    for jj, k in enumerate(keep):
        sel = j == jj
        out[sel] = X[i[sel]] @ (U[k] @ one_t)
    return out
