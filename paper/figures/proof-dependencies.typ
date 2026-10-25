// 図 1（定理 A の証明の依存関係）。英日の本文が同じ原本から描く: #proof-dependencies(lang: "en" | "ja")
// 列: 計算を支える命題 | 有限計算 F0–F5 | 手の証明 | 上下の評価 | 定理 A。矢印は左から右へ（例外は補題 3.2 → 補題 4.2 の下向き 1 本）。
#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

#let _blue = rgb("#e6f0fa")
#let _green = rgb("#e7f2e9")
#let _line = rgb("#50677a")

#let proof-dependencies(lang: "en") = {
  let ja = lang == "ja"
  let t(en, jp) = if ja { jp } else { en }
  // 箱の中身: 1 行目に番号と参照、2 行目以降に内容
  let head(label, ref) = text(font: ("DejaVu Sans", "IPAexGothic"), weight: "bold", size: 0.95em, label) + if ref != none { text(size: 0.85em, fill: luma(90), [ · #ref]) }
  let box-body(label, ref, body) = align(left, head(label, ref) + linebreak() + body)
  let comp(pos, key, label, ref, body) = node(pos, box-body(label, ref, body), fill: _blue, width: 40mm, name: key)
  let ded(pos, label, ref, body, name: none, width: 31mm) = node(pos, box-body(label, ref, body), fill: _green, width: width, name: name)
  let arrow = "-|>"

  set text(size: 7.4pt)
  set par(justify: false, leading: 0.5em)
  diagram(
    spacing: (4mm, 2.4mm),
    node-stroke: 0.6pt + _line,
    node-corner-radius: 3pt,
    node-inset: 4pt,
    edge-stroke: 0.7pt + _line,

    // 有限計算（第 1 列）
    comp((1, 0), <F0>, [F0], [§4.3, C2], t([$G$ and (3.1) are positive definite, even, of determinant 1], [$G$ と (3.1) は正定値・偶・行列式 1])),
    comp((1, 1), <F4t>, [F4 ($tau$)], [§4.3, C2], t([$tau^2 = -5$, $tau G tau^sans(T) = 5 G$], [$tau^2 = -5$, $tau G tau^sans(T) = 5 G$])),
    comp((1, 2), <F1>, [F1], [§6.1, C5], t([$min L_56 = 6$ (exact enumeration)], [$min L_56 = 6$（厳密な列挙）])),
    comp((1, 3), <F4s>, [F4 ($S$)], [§4.3, C2], t([$S = chevron.l g_1, g_2 chevron.r$ preserves $G$, $|S| = 24 thin 360$, $S$ commutes with $tau$], [$S = chevron.l g_1, g_2 chevron.r$ は $G$ を保ち、$|S| = 24 thin 360$、$tau$ と可換])),
    comp((1, 4), <F2>, [F2], [§6.2, C8], t([$L_56(6)$ is the union of 656 listed #box[$S$-orbits]], [$L_56(6)$ は一覧の 656 個の $S$-軌道の和])),
    comp((1, 5), <F3>, [F3], [§6.4, C9], t([$L_56(8)$ is the union of the #box[$S$-orbits] of $1 thin 527 thin 984$ listed vectors], [$L_56(8)$ は一覧の $1 thin 527 thin 984$ 本のベクトルの $S$-軌道の和])),
    comp((1, 6), <F5a>, [F5a], [§6.6, C10], t([odd cosets: #box($min(r tau + 2 L_56) >= 14$)], [奇の剰余類: #box($min(r tau + 2 L_56) >= 14$)])),
    comp((1, 7), <F5b>, [F5b], [§6.7, C13], t([even cosets: #box($min(x tau + 2 L_56) >= 12$), by certificates], [偶の剰余類: #box($min(x tau + 2 L_56) >= 12$)（代表元による）])),
    comp((1, 8), <F5b2>, [F5b], [§6.5, C11], t([the same bound, by canonical forms], [同じ下界（標準形による）])),

    // 計算を支える命題（第 0 列）
    ded((0, 4.5), t([Theta series], [テータ級数]), none, t([shell sizes (§2.3), compared with orbit-size sums (§6.3)], [殻の大きさ（§2.3）。軌道の大きさの和と比べる（§6.3）]), name: <theta>, width: 27mm),
    ded((0, 6.5), t([Lemma 5.1, Cor. 5.2, 5.3], [補題 5.1, 系 5.2, 5.3]), none, t([a certificate bounds a coset minimum], [代表元が剰余類の最小を下から抑える]), name: <cert>, width: 27mm),
    ded((0, 8), t([Prop. 6.3], [命題 6.3]), none, t([norm 8 in a coset $<=>$ canonical form in $K_8$], [剰余類にノルム 8 $<=>$ 標準形が $K_8$ に属する]), name: <can>, width: 27mm),
    edge(<theta>, <F2>, arrow),
    edge(<theta>, <F3>, arrow),
    edge(<cert>, <F5a>, arrow),
    edge(<cert>, <F5b>, arrow),
    edge(<can>, <F5b2>, arrow),

    // 手の証明（第 2 列）
    ded((2, 0.5), t([Lemma 3.2], [補題 3.2]), none, t([$L_112$ is even unimodular of dimension 112], [$L_112$ は 112 次元の偶ユニモジュラー格子]), name: <l32>),
    ded((2, 2), t([Lemma 4.2], [補題 4.2]), none, t([a vector of norm $<= 8$ gives a collision of type (6,6), (6,10), (10,6) or (8,8)], [ノルム 8 以下のベクトルは (6,6), (6,10), (10,6), (8,8) 型の衝突を与える]), name: <l42>),
    ded((2, 4), [§4.2], none, t([one representative per #box[$S$-orbit] suffices], [$S$-軌道ごとに代表 1 個で足りる]), name: <sym>),
    node((2, 7.5), text(size: 1.2em, $or$), shape: circle, fill: white, inset: 2pt, name: <or>),
    edge(<F0>, <l32>, arrow),
    edge(<F4t>, <l32>, arrow),
    edge(<l32>, <l42>, arrow),
    edge(<F1>, <l42>, arrow),
    edge(<F4s>, <sym>, arrow),
    edge(<F2>, <sym>, arrow),
    edge(<F3>, <sym>, arrow),
    edge(<F5b>, <or>, arrow, stroke: (dash: "dashed")),
    edge(<F5b2>, <or>, arrow, stroke: (dash: "dashed")),

    // 上下の評価（第 3 列）と定理 A（第 4 列）
    ded((3, 0.5), t([Upper bound], [上界]), none, t([#box($min L_112 <= 10$) by (1.1)], [(1.1) より #box($min L_112 <= 10$)]), name: <le>, width: 24mm),
    ded((3, 4.5), t([Lower bound], [下界]), none, t([#box($min L_112 >= 10$) by Cor. 4.3 and App. C.4], [系 4.3 と付録 C.4 より #box($min L_112 >= 10$)]), name: <ge>, width: 24mm),
    edge(<l32>, <le>, arrow),
    edge(<l42>, <ge>, arrow),
    edge(<sym>, <ge>, arrow),
    edge(<F5a>, (2.55, 6), <ge>, arrow),
    edge(<or>, (2.55, 7.5), <ge>, arrow),
    node((4, 2.5), box-body(t([Theorem A], [定理 A]), none, t([$min L_112 = 10$: $L_112$ is extremal], [$min L_112 = 10$: $L_112$ は極値である])), fill: _green, stroke: 1.1pt + _line, width: 24mm, name: <thmA>),
    edge(<le>, <thmA>, arrow),
    edge(<ge>, <thmA>, arrow),
  )
}
