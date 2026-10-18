# 論文

[English](README.md)

- [英語 PDF](paper.en.pdf)・[ソース](paper.en.typ)
- [日本語 PDF](paper.ja.pdf)・[ソース](paper.ja.typ)
- [英語補遺](supplement.en.pdf)・[ソース](supplement.en.typ)
- [日本語補遺](supplement.ja.pdf)・[ソース](supplement.ja.typ)

リポジトリのルートから Typst 0.14.2 で組版します。

```bash
typst compile --root . paper/paper.en.typ paper/paper.en.pdf
typst compile --root . paper/paper.ja.typ paper/paper.ja.pdf
typst compile --root . paper/supplement.en.typ paper/supplement.en.pdf
typst compile --root . paper/supplement.ja.typ paper/supplement.ja.pdf
```

同じ組版には New Computer Modern・IPAex 明朝／ゴシック・DejaVu の各書体を用います。書式と計算参照の定義も同梱しており、このディレクトリだけで組版できます。

PDF・ソース・コード・検証用データのハッシュは同じ版のものを使ってください。表 D2 の計算参照は、その版に同梱されたパスに対応します。
