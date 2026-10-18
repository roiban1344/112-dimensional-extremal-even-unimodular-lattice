#!/usr/bin/env python3
"""Check the bilingual paper/supplement's identifiers and distribution paths.

This is an editorial check; it does not run the mathematical computations.
Run from the repository root (any directory works) with Python 3, without additional dependencies:

    python3 -I paper/tools/check-paper.py

It reads the files of the repository that contains this script, never another tree.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent.parent  # paper/tools/check-paper.py -> repository root
PAPER = ROOT / 'paper'


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
        assert len(ids) == len(set(ids)), f'code/{name}: duplicate Table D2 rows: {sorted(i for i in set(ids) if ids.count(i) > 1)}'
        assert set(ids) == calc_ids, f'code/{name}: Table D2 rows differ from computations.typ: {set(ids) ^ calc_ids}'
        for calc_id, cell in rows:
            for token in re.findall(r'[\w./-]+\.(?:py|c|g|lean)\b|\blean/', cell):
                if token == 'lean/':
                    assert (ROOT / 'lean').is_dir(), f'code/{name}: {calc_id}: lean/ is absent'
                    continue
                assert any(f == token or f.endswith('/' + token) for f in code_files), \
                    f'code/{name}: {calc_id}: absent path {token}'


def main():
    sources = {(kind, lang): (PAPER / f'{kind}.{lang}.typ').read_text()
               for kind in ('paper', 'supplement') for lang in ('ja', 'en')}
    for kind in ('paper', 'supplement'):
        ja = identifiers(sources[kind, 'ja'])
        en = identifiers(sources[kind, 'en'])
        assert ja == en, f'Japanese/English identifiers differ in {kind}: {ja!r} != {en!r}'
        for category in ja:
            assert len(set(category)) == len(category), f'duplicate identifiers in {kind}: {category}'
    ledger = (PAPER / 'computations.typ').read_text()
    blocks = re.findall(r'\(id: "C\d+".*?(?=\n  \(id:|\n\))', ledger, re.S)
    calc_ids = {re.search(r'id: "(C\d+)"', b)[1] for b in blocks}
    assert calc_ids == {f'C{i}' for i in range(1, 1 + len(blocks))}
    unpublished = []
    for block in blocks:
        calc_id = re.search(r'id: "(C\d+)"', block)[1]
        if 'published: false' in block:
            unpublished.append(calc_id)
            assert '未公開' in block and 'not distributed' in block
            continue
        for file in re.findall(r'"((?:code|lean)/[^"\n]+)"', block):
            path = ROOT / file
            assert path.is_file(), f'{calc_id}: absent distribution path {file}'

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
            assert section in headings, f'{lang}: unknown section {section}'
        for table in re.findall(r'(?:(?<!代)表\s*|Tables? )([A-GS]?\d+)(?!\d)', refs):
            assert table in tables, f'{lang}: unknown table {table}'
        for theorem in re.findall(r'(?:補題|命題|系|定義|検査|Lemma|Proposition|Corollary|Definition|Check)\s+(\d+\.\d+)', refs):
            assert theorem in statements, f'{lang}: unknown statement {theorem}'
        cited = {c for call in re.findall(r'#calc\((.*?)\)', all_text)
                 for c in re.findall(r'"(C\d+)"', call)}
        assert cited == calc_ids, f'{lang}: uncited or undefined computations: {cited ^ calc_ids}'
        for forbidden in ('G^(*)', 'G_R', 'VERIFICATION-ROUTES.md', 'extremal norm', '極値ノルム', 'MathComp', 'critical_p_stab_Aut', '系 S2', 'Corollary S2', 'cosetes'):
            assert forbidden not in all_text, f'{lang}: residual {forbidden!r}'
        assert '#pending[' not in main_text, f'{lang}: main paper has a pending assertion'
        assert '#pending[' not in supplement, f'{lang}: supplement has a pending assertion'
        status = '経路 T は未完了' if lang == 'ja' else 'Route T is incomplete'
        assert status in supplement, f'{lang}: route T incompleteness must remain explicit'
        assert 'Schreier' in main_text and 'Schreier conjecture is not used' not in main_text
        assert 'lean/EEUL/L112/Chain.lean' in main_text
    if unpublished:
        print('Unpublished supplementary code:', ', '.join(unpublished))
    print(f'PASS: bilingual headings, statements, tables, references, C1-C{len(calc_ids)} and distributed paths')


if __name__ == '__main__':
    main()
