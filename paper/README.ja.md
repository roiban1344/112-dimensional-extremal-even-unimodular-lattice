# 論文

[English](README.md)

- [英語 PDF](paper.en.pdf)・[ソース](paper.en.typ)
- [日本語 PDF](paper.ja.pdf)・[ソース](paper.ja.typ)
- [英語補遺](supplement.en.pdf)・[ソース](supplement.en.typ)
- [日本語補遺](supplement.ja.pdf)・[ソース](supplement.ja.typ)

`figures/` には図 1（`proof-dependencies.*`）を、`tools/check-paper.py` にはこのページの最後で説明する整合性の検査を置きます。`style/eeul.typ` と `paper.typ` は書式を、`computations.typ` は表 D2 の元になる計算の台帳を定義します。

リポジトリのルートから Typst 0.14.2 で組版します。

```bash
typst compile --root . paper/paper.en.typ paper/paper.en.pdf
typst compile --root . paper/paper.ja.typ paper/paper.ja.pdf
typst compile --root . paper/supplement.en.typ paper/supplement.en.pdf
typst compile --root . paper/supplement.ja.typ paper/supplement.ja.pdf
```

同じ組版には New Computer Modern・IPAex 明朝／ゴシック・DejaVu の各書体を用います。書式と計算参照の定義、図 1 の原本（`figures/proof-dependencies.typ`）も同梱しています。図 1 は Typst のパッケージ `@preview/fletcher:0.5.8` で描きます。このパッケージは最初の組版のときに Typst Universe から自動で取得されて保存され、2 回目以降はネットワークを使いません。

PDF・ソース・コード・検証用データのハッシュは同じ版のものを使ってください。表 D2 の計算参照は、その版に同梱されたパスに対応します。 プルリクエストではソースだけを変更します。コミット済みの PDF は版ごとに 1 回、タグを打つ直前のコミットで再生成します。本文の小さな修正にバイナリの差分が付かないようにするためで、版と版の間は PDF がソースより古いことがあります。各 GitHub Release に添付された PDF は、`release-pdfs` ワークフローがタグのソースから作ったもので、配布物はこちらです。

整合性の検査: リポジトリ直下で `python3 -I paper/tools/check-paper.py` を実行します。必要なのは Python 3 だけで、このスクリプトが置かれたリポジトリのファイルを読みます。`paper.en`/`paper.ja` と `supplement.en`/`supplement.ja` で節・定理類・表の番号が一致し（それぞれ重複なし）、本文が参照する節・表・定理類が存在し、`#calc("Cn")` のラベルがすべて `computations.typ` に定義されて台帳の各行が引用され、`computations.typ` と `code/README.md`・`code/README.ja.md` の表 D2 の対応に現れる `code/`・`lean/` のパスがすべて存在することを確かめます。数学的な計算は走らせません。成功すると `PASS` の行を 1 行出力して終了コード 0 で終わり、失敗すると `FAIL:` で始まるメッセージを出して終了コード 1 で終わります。ワークフロー `.github/workflows/checks.yml` が、プルリクエストと `main` への push のたびに、4 文書の Typst 組版とともにこれを実行します。
