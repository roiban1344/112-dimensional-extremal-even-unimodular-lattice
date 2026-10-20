"""Route T, final step [C32]: the checker of supplementary/route_t/exclusion.py on a few rows of
certificates/route_t_exclusion.json (the full check takes about 8 minutes and is not run here).
経路 T の最後の段 [C32]: supplementary/route_t/exclusion.py の検算器を certificates/route_t_exclusion.json の数行に当てる
（全体の検算は約 8 分かかるので、ここでは走らせない）。"""
import json
import os
import sys
from fractions import Fraction as Fr

import pytest

from conftest import CERTIFICATES, CODE

sys.path.insert(0, os.path.join(CODE, "supplementary", "route_t"))
import exclusion as ex  # noqa: E402

pytestmark = pytest.mark.slow                          # about 15 s / 約 15 秒

ROWS = json.load(open(os.path.join(CERTIFICATES, ex.CERT)))["entries"]


def model(key):
    A, Bi, a, b, p, q = key
    return ex.module(A, Bi, a, Fr(b), (Fr(p, 2), Fr(-q, 10)))


def test_first_rows_are_valid_dangerous_and_witnessed():
    for e in ROWS[:5] + [r for r in ROWS if r["type"] == "s3tau"][:5]:
        G, T, GH = model(e["key"])
        assert ex.short(GH, 8), e["key"]                  # dangerous / 危険
        assert ex.witness_ok(G, T, e), e["key"]


def test_witness_check_rejects_other_forms_and_altered_rows():
    e = ROWS[0]
    G, T, _ = model(e["key"])
    assert not ex.witness_ok(G, T, dict(e, type="s2"))   # search (2) is not accepted / 探索 (2) の形は受け付けない
    w = list(e["w"]); w[0] += 1
    assert not ex.witness_ok(G, T, dict(e, w=w))
    assert not ex.witness_ok(G, T, dict(e, x=[float(t) for t in e["x"]]))


def test_structure_tau_squares_to_minus_five_and_scales_the_form_by_five():
    for e in ROWS[::97]:
        G, T, _ = model(e["key"])
        TT = [[sum(T[i][k] * T[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        assert TT == [[-5 * int(i == j) for j in range(4)] for i in range(4)]
        TGT = [[sum(T[i][k] * G[k][l] * T[j][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
        assert TGT == [[5 * x for x in r] for r in G]
