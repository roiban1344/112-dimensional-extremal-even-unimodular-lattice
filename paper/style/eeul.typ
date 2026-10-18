// このリポジトリの文書の共通書式（Typst 0.14）。
// 使い方:
//   #import "/typst/eeul.typ": *
//   #show: doc.with(title: [...], subtitle: [...], meta: [...])
// 組版: scripts/typst compile <file>.typ（初回は scripts/setup-typst.sh）。
// 約束: 数式は Typst の数式で書く（Unicode の上付き・下付き文字や ℤ などで代用しない）。

// ---- 書体 ----
#let font-serif = ("New Computer Modern", "IPAexMincho")
#let font-sans = ("DejaVu Sans", "IPAexGothic")

// ---- 数式の略記 ----
#let SL = math.op("SL")
#let GL = math.op("GL")
#let PSL = math.op("PSL")
#let PGL = math.op("PGL")
#let Aut = math.op("Aut")
#let End = math.op("End")
#let Hom = math.op("Hom")
#let Gal = math.op("Gal")
#let tr = math.op("tr")
#let Tr = math.op("Tr")
#let Nm = math.op("N")
#let rank = math.op("rank")
#let disc = math.op("disc")
#let Im = math.op("Im")
#let Ker = math.op("Ker")
#let OO = $cal(O)$
#let nm(x) = $(#x, #x)$ // ノルム (x,x)

// ---- 文書全体 ----
#let doc(title: none, subtitle: none, meta: none, body) = {
  set document(title: title)
  set page(paper: "a4", margin: (x: 22mm, top: 22mm, bottom: 24mm), numbering: "1")
  set text(font: font-serif, size: 10.5pt, lang: "ja", cjk-latin-spacing: auto)
  set par(justify: true, leading: 0.85em, first-line-indent: (amount: 1em, all: false), spacing: 1.2em)
  set heading(numbering: "1.1")
  show heading: set text(font: font-sans, weight: "bold")
  show heading.where(level: 1): it => { v(0.8em); it; v(0.3em) }
  set math.equation(numbering: "(1)", number-align: right)
  show math.equation: set text(font: ("New Computer Modern Math", "IPAexMincho"))
  show link: set text(fill: rgb("#1f4e9c"))
  show raw: set text(font: ("DejaVu Sans Mono", "IPAexGothic"), size: 0.92em)
  set table(stroke: 0.5pt + luma(160), inset: 5pt)
  show table: set text(size: 0.92em)
  set list(indent: 0.6em)
  set enum(indent: 0.6em)

  if title != none {
    align(center, block(width: 100%, {
      text(font: font-sans, size: 16pt, weight: "bold", title)
      if subtitle != none { linebreak(); v(0.2em); text(size: 11pt, subtitle) }
    }))
    v(0.4em)
  }
  if meta != none {
    block(width: 100%, inset: 8pt, fill: luma(245), radius: 3pt, text(size: 0.88em, meta))
    v(0.6em)
  }
  body
}

// ---- 囲み ----
#let _box(label, color, body) = block(
  width: 100%, inset: (x: 9pt, y: 7pt), radius: 3pt,
  fill: color.lighten(88%), stroke: (left: 2.5pt + color),
  { text(font: font-sans, weight: "bold", size: 0.92em, fill: color.darken(20%), label); h(0.6em); body },
)
#let policy(body) = _box([方針.], rgb("#3a6ea5"), body)        // 節の冒頭の方針
#let aside(body) = _box([補助線.], rgb("#4a8a4a"), body)       // 読解の補助（訳・ノートで原文に無いもの）
#let trnote(body) = _box([訳注.], rgb("#a0662a"), body)        // 翻訳者の注
#let caution(body) = _box([注意.], rgb("#b03a3a"), body)

// 原文のページ・節の目印（翻訳で原文と対照するため）
#let orig(p) = text(size: 0.8em, fill: luma(110), [［原文 #p］])

// ---- 定理環境（通し番号 1 本） ----
#let _thm-counter = counter("eeul-thm")
#let _thm(kind, name: none, body) = {
  _thm-counter.step()
  block(width: 100%, above: 1em, below: 1em, {
    text(font: font-sans, weight: "bold", { kind; " "; context _thm-counter.display() })
    if name != none { [（#name）] }
    text(font: font-sans, weight: "bold", [.])
    h(0.5em)
    body
  })
}
#let theorem(name: none, body) = _thm([定理], name: name, body)
#let lemma(name: none, body) = _thm([補題], name: name, body)
#let proposition(name: none, body) = _thm([命題], name: name, body)
#let corollary(name: none, body) = _thm([系], name: name, body)
#let definition(name: none, body) = _thm([定義], name: name, body)
#let remark(name: none, body) = _thm([注意], name: name, body)
#let example(name: none, body) = _thm([例], name: name, body)
#let proof(body) = block(width: 100%, {
  text(font: font-sans, [証明.]); h(0.5em); body; h(1fr); $square$
})

// ---- 主張のラベル（docs/02-plan.md 冒頭） ----
#let claim(kind, detail: none) = {
  let c = (
    "既知": rgb("#2f6f3e"), "孫引き": rgb("#7a6a2a"), "検証済": rgb("#1f4e9c"),
    "スケッチ": rgb("#7a4a9c"), "予想": rgb("#9c4a7a"), "記憶": rgb("#b03a3a"),
    "考察": rgb("#5a5a5a"), "未着手": rgb("#5a5a5a"),
  ).at(kind, default: luma(90))
  text(size: 0.85em, fill: c, {
    "［"; kind
    if detail != none { [: #detail] }
    "］"
  })
}
