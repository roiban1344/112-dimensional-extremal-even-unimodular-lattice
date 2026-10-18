# Paper

[日本語](README.ja.md)

- [English PDF](paper.en.pdf) · [source](paper.en.typ)
- [Japanese PDF](paper.ja.pdf) · [source](paper.ja.typ)
- [English supplement](supplement.en.pdf) · [source](supplement.en.typ)
- [Japanese supplement](supplement.ja.pdf) · [source](supplement.ja.typ)

Build from the repository root with Typst 0.14.2:

```bash
typst compile --root . paper/paper.en.typ paper/paper.en.pdf
typst compile --root . paper/paper.ja.typ paper/paper.ja.pdf
typst compile --root . paper/supplement.en.typ paper/supplement.en.pdf
typst compile --root . paper/supplement.ja.typ paper/supplement.ja.pdf
```

The styles use New Computer Modern, IPAexMincho, IPAexGothic and DejaVu fonts. Install these for matching typography. `style/eeul.typ`, `paper.typ` and `computations.typ` are included, so the sources are self-contained.

The PDFs, sources, code and verification-data hashes belong to the same release; the paths in Table D2 are those of that release.
