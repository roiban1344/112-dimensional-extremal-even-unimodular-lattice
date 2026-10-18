# Paper / 論文

- [English PDF](paper.en.pdf) · [source](paper.en.typ)
- [日本語 PDF](paper.ja.pdf) · [ソース](paper.ja.typ)
- [English supplement](supplement.en.pdf) · [source](supplement.en.typ)
- [日本語補遺](supplement.ja.pdf) · [ソース](supplement.ja.typ)

Build from the repository root with Typst 0.14.2:

```bash
typst compile --root . paper/paper.en.typ paper/paper.en.pdf
typst compile --root . paper/paper.ja.typ paper/paper.ja.pdf
typst compile --root . paper/supplement.en.typ paper/supplement.en.pdf
typst compile --root . paper/supplement.ja.typ paper/supplement.ja.pdf
```

The styles use New Computer Modern, IPAexMincho, IPAexGothic and DejaVu fonts. Install these for matching typography. `style/eeul.typ`, `paper.typ` and `computations.typ` are included, so the sources are self-contained.

同じ組版には New Computer Modern・IPAex 明朝／ゴシック・DejaVu の各書体を用います。書式と計算参照の定義も同梱しており、このディレクトリだけで組版できます。

The PDFs, sources, code and verification-data hashes belong to the same release; the paths in Table D2 are those of that release.

PDF・ソース・コード・検証用データのハッシュは同じ版のものを使ってください。表 D2 の計算参照は、その版に同梱されたパスに対応します。
