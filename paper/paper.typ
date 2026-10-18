// 112 次元の論文（英日）の書式。共通の書式 typst/eeul.typ の上に、この論文だけの囲みと印を足す。
// 使い方: #import "/docs/paper-112/r112.typ": *  ;  #show: paper.with(lang: "en" | "ja", title: [...], ...)
#import "style/eeul.typ": *

#let _lang = state("r112-lang", "en")

#let paper(lang: "en", title: none, subtitle: none, authors: none, date: none, body) = {
  show: doc.with(title: title, subtitle: subtitle, meta: none)
  set text(lang: lang)
  set heading(numbering: none)                 // 節番号は本文に手で書いてある（相互参照が「§4.4」の形のため）
  set math.equation(numbering: none)           // 番号は #tagged で手で付ける
  show figure.where(kind: table): set figure.caption(position: top)
  show figure.caption: set text(size: 0.92em)
  show figure.caption: set align(left)
  set figure(gap: 0.6em)
  _lang.update(lang)
  if authors != none or date != none {
    align(center, {
      if authors != none { authors; linebreak() }
      if date != none { text(size: 0.92em, date) }
    })
    v(0.8em)
  }
  body
}

#let small(body) = text(size: 0.9em, body)

// 状態の印（本稿の印。付録 G の表 G1 を参照）
#let _tagcolor = (
  "pf": rgb("#2f6f3e"), "ex": rgb("#1f4e9c"), "fp": rgb("#9c6a1f"),
  "kn": rgb("#5a5a5a"), "he": rgb("#7a4a9c"), "ip": rgb("#b03a3a"),
)
#let tag(kind, body) = box(
  inset: (x: 3pt, y: 1pt), outset: (y: 1.5pt), radius: 2pt,
  fill: _tagcolor.at(kind).lighten(85%),
  text(size: 0.78em, fill: _tagcolor.at(kind).darken(10%), font: font-sans, body),
)

// 囲み
#let _env(color, body) = block(
  width: 100%, inset: (x: 9pt, y: 7pt), radius: 2pt, breakable: true,
  fill: color.lighten(92%), stroke: (left: 2pt + color), body,
)
#let thm(body) = _env(rgb("#1f4e9c"), body)          // 定理・命題・補題・系・定義（見出しは本文の太字）
#let fact(body) = _env(rgb("#2f6f3e"), body)         // 計算事実 F1〜F5
#let rem(body) = _env(luma(120), body)               // 注意
#let proofbox(body) = block(width: 100%, inset: (left: 9pt, y: 2pt), stroke: (left: 0.6pt + luma(170)), breakable: true, body)
#let qed = h(1fr) + $square$
#let policy-box(body) = _env(rgb("#3a6ea5"), text(size: 0.95em, body))   // 節の冒頭の方針
#let status-box(body) = block(width: 100%, inset: 9pt, radius: 3pt, fill: rgb("#fff4e5"), stroke: 0.6pt + rgb("#d9a441"), breakable: true, body)
#let abstract-box(body) = block(width: 100%, inset: (x: 18pt, y: 8pt), breakable: true, {
  align(center, text(font: font-sans, weight: "bold", context if _lang.get() == "ja" { [要旨] } else { [Abstract] }))
  v(0.2em)
  set par(first-line-indent: 0pt)
  body
})

// 番号を手で付けた別行立ての式: #tagged("1.2", $ ... $)
#let tagged(t, eq) = block(width: 100%, grid(columns: (1fr, auto), align: (center + horizon, right + horizon), eq, [(#t)]))

// 表: 見出しは上、番号は見出しの文に手で書いてある
#let ptable(columns: 1, align: auto, caption: none, ..cells) = figure(
  kind: table, numbering: none, caption: caption,
  table(columns: columns, align: align, ..cells),
)

// 用語集: #gloss(([語], [説明]), ...)
#let gloss(..items) = {
  set par(first-line-indent: 0pt)
  for (t, d) in items.pos() {
    block(above: 0.7em, below: 0.7em, { strong(t); h(0.6em); d })
  }
}

// 文献
#let refs-list(..items) = {
  set par(first-line-indent: 0pt, hanging-indent: 1.5em)
  for it in items.pos() { block(above: 0.5em, below: 0.5em, it) }
}

// 図 1（依存関係）の部品: 青 = 整数演算の計算事実、緑 = 手で証明（Lean でも検査）
#let depbox(kind, body) = {
  let c = if kind == "pf" { rgb("#2f6f3e") } else { rgb("#1f4e9c") }
  block(width: 100%, inset: 6pt, radius: 3pt, stroke: 0.9pt + c, fill: c.lighten(92%), align(center, text(size: 0.85em, body)))
}
#let deparrow = align(center + horizon, text(size: 1.4em, fill: luma(90), sym.arrow.r))

// 未了の主張（作業用の印）: 内容は最終形で書き、まだ成り立っていないあいだだけ黄色で塗る。成り立ったら #pending を外す。
// 公開版には残さない（`grep -n "#pending" R112-paper.*.typ` で確認）。
#let pending(body) = highlight(fill: rgb("#fff1a8"), body)
