# Paper

[日本語](README.ja.md)

- [English PDF](paper.en.pdf) · [source](paper.en.typ)
- [Japanese PDF](paper.ja.pdf) · [source](paper.ja.typ)
- [English supplement](supplement.en.pdf) · [source](supplement.en.typ)
- [Japanese supplement](supplement.ja.pdf) · [source](supplement.ja.typ)

`figures/` holds Figure 1 (`proof-dependencies.*`), and `tools/check-paper.py` is the consistency check described at the end of this page. `style/eeul.typ` and `paper.typ` define the layout, and `computations.typ` the ledger of computations behind Table D2.

Build from the repository root with Typst 0.14.2:

```bash
typst compile --root . paper/paper.en.typ paper/paper.en.pdf
typst compile --root . paper/paper.ja.typ paper/paper.ja.pdf
typst compile --root . paper/supplement.en.typ paper/supplement.en.pdf
typst compile --root . paper/supplement.ja.typ paper/supplement.ja.pdf
```

The styles use New Computer Modern, IPAexMincho, IPAexGothic and DejaVu fonts. Install these for matching typography. `style/eeul.typ`, `paper.typ` and `computations.typ` are included, so the sources are self-contained.

The PDFs, sources, code and verification-data hashes belong to the same release; the paths in Table D2 are those of that release. Pull requests change only the sources. The committed PDFs are regenerated once per release, in the commit just before the tag, so that small changes to the text do not carry binary differences; between releases they may lag behind the sources. The PDFs attached to each GitHub Release are built by the `release-pdfs` workflow from the tagged sources and are the distributed copies.

Consistency check: `python3 -I paper/tools/check-paper.py`, run from the repository root, needs only Python 3 and reads the files of the repository it lives in. It checks that `paper.en`/`paper.ja` and `supplement.en`/`supplement.ja` carry the same section, theorem-type statement and table identifiers (each unique), that every section, table and statement referred to in the text exists, that every `#calc("Cn")` label is defined in `computations.typ` and every row of that ledger is cited, and that every `code/` and `lean/` path in `computations.typ` and in the Table D2 correspondence of `code/README.md` and `code/README.ja.md` exists. It does not run any mathematical computation; it prints one `PASS` line and exits with status 0, or stops with a `FAIL:` message and exit status 1. The workflow `.github/workflows/checks.yml` runs it on every pull request and every push to `main`, together with the Typst build of the four documents.
