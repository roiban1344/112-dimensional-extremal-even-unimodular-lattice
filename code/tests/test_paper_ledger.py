"""Consistency of the paper with the code and the data (no computation): the bold rows of Table D2 against
verify/proof.sh, the times of Table D2 against the docstrings (the canonical source), the hashes printed in
Appendix D against certificates/SHA256SUMS, and the Lean statements printed in §7.1 against Chain.lean.
論文とコード・データの整合（計算はしない）: 表 D2 の太字と verify/proof.sh、表 D2 の時間と docstring（正本）、付録 D に印刷した
ハッシュと certificates/SHA256SUMS、§7.1 に印刷した Lean の主張と Chain.lean。"""
import hashlib
import os
import re

import pytest

from conftest import CERTIFICATES, CODE, REPO

PAPER = os.path.join(REPO, "paper")


def read(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as f:
        return f.read()


def ledger_rows():
    """[(id, files, time)] from paper/computations.typ. / paper/computations.typ の行。"""
    text = read(PAPER, "computations.typ")
    rows = []
    for block in re.findall(r'\(id: "C\d+".*?(?=\n  \(id:|\n\))', text, re.S):
        cid = re.search(r'id: "(C\d+)"', block)[1]
        files = re.findall(r'"((?:code|lean|certificates)/[^"\n]+)"', block)
        time = re.search(r"time: \[(.*)\]\),?\s*$", block, re.S)[1]
        rows.append((cid, files, time))
    return rows


def test_bold_rows_of_table_d2_are_the_steps_of_proof_sh():
    text = read(PAPER, "computations.typ")
    bold = set(re.findall(r'"([^"]+)"', re.search(r"#let proof-checks = \((.*?)\)\n", text, re.S)[1]))
    steps = {"code/verify/" + s for s in re.findall(r'"\$D/(v\d_\w+\.py)"', read(CODE, "verify", "proof.sh"))}
    assert bold == steps | {"code/verify/enum_interval.c"}


UNITS = {"s": "s", "second": "s", "seconds": "s", "min": "min", "minute": "min", "minutes": "min",
         "h": "h", "hour": "h", "hours": "h", "day": "d", "days": "d"}
QUANTITY = re.compile(r"(\d+(?:\.\d+)?)\s*(?:CPU\s+)?(seconds?|s|minutes?|min|hours?|h|days?)\b")


def quantities(text):
    return {(float(n), UNITS[u]) for n, u in QUANTITY.findall(text)}


def header(path):
    """The first 150 lines of a file (docstring or header comment). / ファイルの先頭 150 行（docstring か冒頭の注釈）。"""
    with open(path, encoding="utf-8") as f:
        return "".join(f.readline() for _ in range(150))


@pytest.mark.parametrize("cid,files,time", ledger_rows())
def test_times_of_table_d2_are_those_of_the_docstrings(cid, files, time):
    # Every "number unit" in the time column of Table D2 also appears in the header of one of the row's files
    # (lean/README.md for the Lean row): the docstrings are the canonical source of the run times.
    # 表 D2 の時間の列の「数 単位」は、その行のファイルのどれかの冒頭（Lean の行は lean/README.md）にもある。時間の正本は docstring。
    sources = "".join(header(os.path.join(REPO, f)) for f in files if not f.startswith("lean/"))
    if any(f.startswith("lean/") for f in files):
        sources += read(REPO, "lean", "README.md")
    missing = quantities(time) - quantities(sources)
    assert not missing, f"{cid}: {sorted(missing)} not in the docstrings of {files}"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


@pytest.mark.parametrize("lang", ["en", "ja"])
def test_hashes_printed_in_appendix_d(lang):
    text = read(PAPER, f"paper.{lang}.typ")
    printed = dict((name, h) for h, name in re.findall(r'raw\("([0-9a-f]{64})  ([\w.]+)"\)', text))
    sums = dict((name, h) for h, name in (line.split() for line in read(CERTIFICATES, "SHA256SUMS").splitlines() if line.strip()))
    assert printed.pop("SHA256SUMS") == sha256(os.path.join(CERTIFICATES, "SHA256SUMS"))
    assert len(printed) == 7 and all(sums[name] == h for name, h in printed.items())


@pytest.mark.parametrize("lang", ["en", "ja"])
def test_lean_statements_printed_in_section_7_1(lang):
    # Every line of the Lean listing in §7.1 occurs verbatim in Chain.lean. / §7.1 の Lean の各行は Chain.lean にそのままある。
    block = re.search(r"```lean\n(.*?)\n```", read(PAPER, f"paper.{lang}.typ"), re.S)[1]
    chain = read(REPO, "lean", "EEUL", "L112", "Chain.lean")
    lines = [line for line in block.splitlines() if line.strip()]
    assert len(lines) > 25
    assert [line for line in lines if line not in chain] == []
