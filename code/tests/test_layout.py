"""The dependency rules of code/README.md ("Layout"), checked on the import statements (ast):
verify/ imports only lib/; lib/ imports nothing else from code/; crosscheck/ imports nothing from code/
outside its own directory; produce/ imports lib/ and produce/; supplementary/ imports lib/, produce/ and
supplementary/.
code/README.ja.md の「構成」の依存の規則を、import 文（ast）で確かめる: verify/ は lib/ だけ、lib/ は code/ のほかを使わない、
crosscheck/ は自分のディレクトリの外の code/ を使わない、produce/ は lib/ と produce/、supplementary/ は lib/・produce/・supplementary/。
"""
import ast
import os

import pytest

from conftest import CODE

AREAS = ("lib", "verify", "produce", "crosscheck", "supplementary")
ALLOWED = {
    "lib": {"lib"},
    "verify": {"lib"},
    "produce": {"lib", "produce"},
    "crosscheck": set(),                 # only modules of the same directory (crosscheck/all_data, second_impl)
    "supplementary": {"lib", "produce", "supplementary"},
}


def sources():
    out = []
    for area in AREAS:
        for d, _, files in os.walk(os.path.join(CODE, area)):
            out += [os.path.join(d, f) for f in files if f.endswith(".py")]
    return sorted(out)


SOURCES = sources()
BY_STEM = {}
for _p in SOURCES:
    BY_STEM.setdefault(os.path.splitext(os.path.basename(_p))[0], []).append(_p)


def area_of(path):
    return os.path.relpath(path, CODE).split(os.sep)[0]


def imported_files(path):
    """The files under code/ that `path` imports: `lib...`, `supplementary...`, `produce...`, or a bare module
    name found by the sys.path entries the scripts insert (the same directory first, as Python does).
    `path` が import する code/ 以下のファイル。"""
    tree = ast.parse(open(path).read())
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module]
        elif isinstance(node, ast.ImportFrom):
            out.add(os.path.join(os.path.dirname(path), "__init__.py"))     # relative import: same package
            continue
        else:
            continue
        for name in names:
            top = name.split(".")[0]
            if top in AREAS:
                out.add(os.path.join(CODE, top, "__init__.py"))
            elif top in BY_STEM:
                same_dir = [q for q in BY_STEM[top] if os.path.dirname(q) == os.path.dirname(path)]
                out.update(same_dir or BY_STEM[top])
    return out


@pytest.mark.parametrize("path", SOURCES, ids=lambda p: os.path.relpath(p, CODE))
def test_imports_follow_the_layout(path):
    area = area_of(path)
    for q in imported_files(path):
        if area == "crosscheck":
            assert os.path.dirname(q) == os.path.dirname(path), f"{path} imports {q}"
        else:
            assert area_of(q) in ALLOWED[area], f"{path} imports {q}"
