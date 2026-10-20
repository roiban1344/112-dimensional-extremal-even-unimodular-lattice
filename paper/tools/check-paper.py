#!/usr/bin/env python3
"""Check the bilingual paper/supplement's identifiers and distribution paths.

This is an editorial check; it does not run the mathematical computations.
Run from the repository root (any directory works) with Python 3, without additional dependencies:

    python3 -I paper/tools/check-paper.py

It reads the files of the repository that contains this script, never another tree.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent.parent  # paper/tools/check-paper.py -> repository root
PAPER = ROOT / 'paper'


def require(cond, msg):
    """A check that also runs under python -O (unlike assert). / python -O でも実行される検査（assert と違う）。"""
    if not cond:
        sys.exit(f'FAIL: {msg}')


def citations_removed(text):
    return re.sub(r'\\\[.*?\\\]', '', text, flags=re.S)


def identifiers(text):
    headings = re.findall(r'^={1,2} (?:(?:付録|Appendix) )?([A-GS\d]+(?:\.\d+)?)(?:\.| )', text, re.M)
    statements = re.findall(r'#strong\[(?:定理|補題|命題|系|定義|検査|Theorem|Lemma|Proposition|Corollary|Definition|Check) ([AB]|\d+\.\d+)(?=\.|（| \()', text)
    tables = re.findall(r'caption: \[(?:表|Table) ([A-GS]?\d+(?:\.\d+)?)\.', text)
    return headings, statements, tables


def check_d2_correspondence(calc_ids):
    """code/README.md and code/README.ja.md: the table 'Table D2 | scripts' lists every [Cn] once,
    and every script path in it exists under code/ (bare names and 'dir/name' are resolved by suffix)."""
    code_files = [p.relative_to(ROOT / 'code').as_posix() for p in (ROOT / 'code').rglob('*') if p.is_file()]
    code_files += [p.relative_to(ROOT).as_posix() for p in (ROOT / 'lean').rglob('*') if p.is_file()]
    for name in ('README.md', 'README.ja.md'):
        rows = re.findall(r'^\| \[(C\d+)\] \| (.*) \|\s*$', (ROOT / 'code' / name).read_text(), re.M)
        ids = [r[0] for r in rows]
        require(len(ids) == len(set(ids)), f'code/{name}: duplicate Table D2 rows: {sorted(i for i in set(ids) if ids.count(i) > 1)}')
        require(set(ids) == calc_ids, f'code/{name}: Table D2 rows differ from computations.typ: {set(ids) ^ calc_ids}')
        for calc_id, cell in rows:
            for token in re.findall(r'[\w./-]+\.(?:py|c|g|lean)\b|\blean/', cell):
                if token == 'lean/':
                    require((ROOT / 'lean').is_dir(), f'code/{name}: {calc_id}: lean/ is absent')
                    continue
                require(any(f == token or f.endswith('/' + token) for f in code_files),
                        f'code/{name}: {calc_id}: absent path {token}')


def main():
    sources = {(kind, lang): (PAPER / f'{kind}.{lang}.typ').read_text()
               for kind in ('paper', 'supplement') for lang in ('ja', 'en')}
    for kind in ('paper', 'supplement'):
        ja = identifiers(sources[kind, 'ja'])
        en = identifiers(sources[kind, 'en'])
        require(ja == en, f'Japanese/English identifiers differ in {kind}: {ja!r} != {en!r}')
        for category in ja:
            require(len(set(category)) == len(category), f'duplicate identifiers in {kind}: {category}')
    ledger = (PAPER / 'computations.typ').read_text()
    blocks = re.findall(r'\(id: "C\d+".*?(?=\n  \(id:|\n\))', ledger, re.S)
    calc_ids = {re.search(r'id: "(C\d+)"', b)[1] for b in blocks}
    require(calc_ids == {f'C{i}' for i in range(1, 1 + len(blocks))}, f'computations.typ: ids are not C1-C{len(blocks)}')
    unpublished = []
    for block in blocks:
        calc_id = re.search(r'id: "(C\d+)"', block)[1]
        if 'published: false' in block:
            unpublished.append(calc_id)
            require('未公開' in block and 'not distributed' in block, f'{calc_id}: unpublished entry not marked as such')
            continue
        for file in re.findall(r'"((?:code|lean)/[^"\n]+)"', block):
            path = ROOT / file
            require(path.is_file(), f'{calc_id}: absent distribution path {file}')

    check_d2_correspondence(calc_ids)

    for lang in ('ja', 'en'):
        main_text = sources['paper', lang]
        supplement = sources['supplement', lang]
        all_text = main_text + supplement
        headings = set(identifiers(main_text)[0] + identifiers(supplement)[0])
        statements = set(identifiers(main_text)[1])
        tables = set(identifiers(main_text)[2] + identifiers(supplement)[2] + ['D2'])
        refs = citations_removed(all_text)
        for section in re.findall(r'§+\s*([A-GS]?\d+(?:\.\d+)?|[A-G]\.\d+)', refs):
            require(section in headings, f'{lang}: unknown section {section}')
        for table in re.findall(r'(?:(?<!代)表\s*|Tables? )([A-GS]?\d+)(?!\d)', refs):
            require(table in tables, f'{lang}: unknown table {table}')
        for theorem in re.findall(r'(?:補題|命題|系|定義|検査|Lemma|Proposition|Corollary|Definition|Check)\s+(\d+\.\d+)', refs):
            require(theorem in statements, f'{lang}: unknown statement {theorem}')
        cited = {c for call in re.findall(r'#calc\((.*?)\)', all_text)
                 for c in re.findall(r'"(C\d+)"', call)}
        require(cited == calc_ids, f'{lang}: uncited or undefined computations: {cited ^ calc_ids}')
        for forbidden in ('G^(*)', 'G_R', 'VERIFICATION-ROUTES.md', 'extremal norm', '極値ノルム', 'MathComp', 'critical_p_stab_Aut', '系 S2', 'Corollary S2', 'cosetes'):
            require(forbidden not in all_text, f'{lang}: residual {forbidden!r}')
        require('#pending[' not in main_text, f'{lang}: main paper has a pending assertion')
        require('#pending[' not in supplement, f'{lang}: supplement has a pending assertion')
        # Route T shares the computations F5a and F5b with the main proof; the supplement must say so.
        # 経路 T は計算 F5a・F5b を主証明と共有する。補遺はそれを明記すること。
        shared = '主証明と同じ計算 F5a・F5b' if lang == 'ja' else 'the same computations F5a and F5b as the main proof'
        require(shared in supplement, f'{lang}: route T must state that it shares F5a and F5b with the main proof')
        require('Schreier' in main_text and 'Schreier conjecture is not used' not in main_text, f'{lang}: Schreier wording')
        require('lean/EEUL/L112/Chain.lean' in main_text, f'{lang}: lean/EEUL/L112/Chain.lean is not cited')
    if unpublished:
        print('Unpublished supplementary code:', ', '.join(unpublished))
    print(f'PASS: bilingual headings, statements, tables, references, C1-C{len(calc_ids)} and distributed paths')


if __name__ == '__main__':
    main()
