// 計算の台帳: 本文の [C1], [C2], … と、付録の表「計算とコード」の正本（英日共通）。
// 本文では #calc("C5") や #calc("C10", "C13") と書く。付録の表は #calc-table() で作る。
// コードは公開リポジトリからの相対パス。未公開のものがあれば published: false を付けて明示する。
#let code-base = "https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/tree/main/"

#let calcs = (
  (id: "C1", files: ("code/verify/v2_theta.py",),
   en: [Extremal theta series of $L$ and $L_112$; Siegel means $Sigma(n)$; Siegel orbit excess (exact rational arithmetic)],
   ja: [$L$ と $L_112$ の極値テータ級数、Siegel 平均 $Sigma(n)$、Siegel 軌道余剰（有理数の厳密計算）], time: [1 s]),
  (id: "C2", files: ("code/verify/v0_inputs.py", "code/supplementary/gluings.py", "code/produce/p1_centralizer.py"),
   en: [Basic facts F0, F4: (3.1) is even with determinant 1; $g_1, g_2$ preserve $G$, commute with $tau$ and generate a group of order 24 360 isomorphic to $"SL"_2(29)$; $tau^2 = -5$, $tau G tau^sans(T) = 5G$; the centralizer has order 12; the 24 elements with $tau^2 = -5$ form 2 classes],
   ja: [基本的な事実 F0, F4: (3.1) は偶で行列式 1。$g_1, g_2$ は $G$ を保ち $tau$ と可換で、$"SL"_2(29)$ と同型な位数 24 360 の群を生成。$tau^2 = -5$、$tau G tau^sans(T) = 5G$。中心化群の位数 12。$tau^2 = -5$ の元 24 個は 2 類], time: [10 min]),
  (id: "C3", files: ("code/supplementary/gluings.py", "code/supplementary/nebe/gluings_m.py", "code/supplementary/_shared.py"),
   en: [Gluings: the commutant of $"SL"_2(29)$ on $L \/ 2L$ is 8-dimensional (the image of $M'$); 60 invertible parity-preserving maps; their classes (Proposition 3.3, Table 2); forced collisions],
   ja: [貼り方: $L \/ 2L$ 上の $"SL"_2(29)$ の可換子は 8 次元（$M'$ の像）。可逆で偶奇を保つ写像 60 個とその類（命題 3.3、表 2）。強制された衝突], time: [min]),
  (id: "C4", files: ("code/supplementary/gluing_b.py", "code/supplementary/nebe/gluings_m.py", "code/supplementary/_shared.py"),
   en: [Gluings A and B: minimum 8 and exactly 292 320 vectors of norm 8; invariants of A and B compared],
   ja: [貼り方 A, B: 最小ノルム 8、ノルム 8 のベクトルはちょうど 292 320 本。A と B の不変量の比較], time: [1.2 h]),
  (id: "C5", files: ("code/verify/v1_min_L.py", "code/verify/enum_interval.c", "code/produce/p6_reduction.py"),
   en: [F1: $min L = 6$ by Fincke–Pohst enumeration with exact rational $L D L^sans(T)$ and outward-rounded interval arithmetic (BKZ-40 basis, 8 454 837 756 nodes); controls $E_8$, Leech, Leech $perp$ Leech $perp E_8$],
   ja: [F1: 有理数の厳密な $L D L^sans(T)$ 分解と外向きに丸めた区間演算による Fincke–Pohst 列挙で $min L = 6$（BKZ-40 基底、8 454 837 756 節点）。対照 $E_8$、Leech、Leech $perp$ Leech $perp E_8$], time: [34 min]),
  (id: "C6", files: ("code/supplementary/nebe/reduction_to_nebe.py", "code/supplementary/nebe/lattices.py", "code/supplementary/nebe/tables.py"),
   en: [F1 by reduction to $L_(56,2)(M)$: no class of a norm-8 vector of $L_(56,2)(M)$ lies in the invariant subspace $W$ (linear algebra over $FF_2$); positive control],
   ja: [F1 の $L_(56,2)(M)$ への帰着: $L_(56,2)(M)$ のノルム 8 のベクトルの類は不変部分空間 $W$ に入らない（$FF_2$ 上の線形代数）。陽性対照], time: [31 min]),
  (id: "C7", files: ("code/supplementary/float_enumerations.py",),
   en: [F1 by floating-point enumeration (fplll on two bases, PARI `qfminim`); supplementary],
   ja: [F1 の浮動小数点の列挙（fplll の 2 基底、PARI の `qfminim`）。補助], time: [51 min–2.3 h]),
  (id: "C8", files: ("code/produce/p2_minimal_orbits.py", "code/verify/v3_minimal_orbits.py", "code/verify/v8_design_identities.py"),
   en: [F2: the 656 orbit representatives of $L(6)$; distinct orbits whose sizes add up to 15 590 400; spherical design identities of degree 2, 4, 6],
   ja: [F2: $L(6)$ の軌道代表 656 個。互いに異なる軌道で大きさの和が 15 590 400。次数 2, 4, 6 の球面デザインの恒等式], time: [≈ 25 min]),
  (id: "C9", files: ("code/produce/p3_norm8_orbits.py", "code/verify/v4_norm8_orbits.py", "code/verify/v8_design_identities.py"),
   en: [F3: orbit representatives of $L(8)$ by marking sums of two minimal vectors; 1 517 130 distinct orbits whose sizes add up to 36 957 286 800; design identities],
   ja: [F3: 最小ベクトル 2 本の和に印を付ける方法による $L(8)$ の軌道代表。互いに異なる 1 517 130 軌道で大きさの和が 36 957 286 800。デザインの恒等式], time: [1.2 h + 9 min]),
  (id: "C10", files: ("code/produce/p4_odd_descent.py", "code/verify/v5_odd_bounding.py", "code/crosscheck/second_impl/odd_classes.py"),
   en: [F5a: odd-class certificates for the 656 classes $r tau + 2L$ (norms 14, 18; inner products with all minimal vectors at most 6), and their re-check by separately written code],
   ja: [F5a: 656 個の類 $r tau + 2L$ の奇の類の代表元（ノルム 14, 18、全最小ベクトルとの内積の絶対値は 6 以下）と、別に書いたコードによる検算], time: [≈ 10 min]),
  (id: "C11", files: ("code/verify/v6_canonical_lookup.py", "code/crosscheck/second_impl/even_classes.py"),
   en: [F5b by canonical forms on $L \/ 2L$: the table $K_8$ and the look-up for all 1 527 984 pairs, in two implementations],
   ja: [標準形による F5b: 表 $K_8$ と、1 527 984 組すべての表引き（2 つの実装）], time: [20 min–2 h]),
  (id: "C12", files: ("code/supplementary/float_enumerations.py",),
   en: [Closest-vector enumerations (fplll, floating point) for the classes of F5a and F5b; supplementary],
   ja: [F5a・F5b の類の最近ベクトル列挙（fplll、浮動小数点）。補助], time: [2.7 h + 4 × 9 h]),
  (id: "C13", files: ("code/produce/p5_even_descent.py", "code/verify/v7_even_bounding.py"),
   en: [F5b by even-class certificates for all 1 527 984 pairs (norms 12, 16, 20; inner products with all minimal vectors at most 6), and their check],
   ja: [偶の類の代表元による F5b: 1 527 984 組すべて（ノルム 12, 16, 20、全最小ベクトルとの内積の絶対値は 6 以下）とその検査], time: [6 × 31 h + 7.9 h]),
  (id: "C14", files: ("code/supplementary/frame_stabilizer.py",),
   en: [Automorphisms preserving the standard frame; the halving of the pairs in route B],
   ja: [標準の枠を保つ自己同型と、経路 B での組の半減], time: [1 s]),
  (id: "C15", files: ("code/supplementary/sample_check.py",),
   en: [Route S: random sample of certificates re-checked with independent integer code],
   ja: [経路 S: 代表元の無作為抽出を、独立な整数演算のコードで検算], time: [8 min]),
  (id: "C16", files: ("code/supplementary/node_estimate.py",),
   en: [Gaussian estimate of the number of enumeration nodes for $L_112$ itself (LLL, BKZ-20, BKZ-30 bases)],
   ja: [$L_112$ そのものの列挙に要る節点数のガウスの見積もり（LLL、BKZ-20、BKZ-30 基底）], time: [3 s]),
  (id: "C17", files: ("code/supplementary/frames.py",),
   en: [Frame-change test: all 864 frames of $Lambda$ give the same class],
   ja: [枠の取り替えの検査: $Lambda$ の 864 個の枠がすべて同じ類を与える], time: [7 min]),
  (id: "C18", files: ("code/supplementary/fixed_sublattices.py",),
   en: [Fixed sublattices of elements of order 3, 5, 7 and their exact minima; BKZ on $L_112$ (tests that cannot separate B from C)],
   ja: [位数 3, 5, 7 の元の固定部分格子とその厳密な最小ノルム、$L_112$ への BKZ（B と C を区別できない検査）], time: [C 10 min; B 18 min]),
  (id: "C19", files: ("code/supplementary/anatomy_b.py",),
   en: [Support modules of the norm-8 vectors of B (Supplement Table S9)],
   ja: [B のノルム 8 のベクトルの台加群（補遺の表 S9）], time: [2 s]),
  (id: "C20", files: ("code/supplementary/route_t/classify.py", "code/supplementary/route_t/recount.py", "code/supplementary/route_t/hermitian.py"),
   en: [Supplement §S4: rank-2 support modules (free and non-free), grouped into 97 invariant types, 63 dangerous. Both enumerations agree on 58 dangerous types after regrouping by the same coarser invariant],
   ja: [補遺 §S4: 階数 2 の台加群（自由・非自由）の不変量による分類。97 型、うち危険 63 型。同じ粗い不変量でまとめ直すと両列挙で危険 58 型が一致する], time: [1–2 min each]),
  (id: "C21", files: ("code/supplementary/route_t/certify.py", "code/supplementary/route_t/check.py", "code/supplementary/route_t/float_cvp.py", "code/supplementary/route_t/common.py"),
   en: [Supplement §S4: three searches modulo 2. All 3 936 certificates for test (3) checked in integers. Test (2): all 763 992 representatives generated, none unresolved; all checked in integers (class membership, norm 12, 16 or 20, inner-product bound 6 against every minimal vector). Complete data: `certificates/route_t_search2.npz`],
   ja: [補遺 §S4: 2 を法とする三つの探索。(3) の代表元 3,936 個は整数で全数検査済み。(2) は 763,992 類すべての代表元を生成、未解決 0。類への所属、ノルム 12・16・20、全最小ベクトルとの内積の絶対値 6 以下を整数で全数検算済み。完成データ: `certificates/route_t_search2.npz`], time: [(2): generation#linebreak() ≈ 13 CPU days (est.)#linebreak() check ≈ 7 CPU h (est.)#linebreak() (3): generation 25 min]),
  (id: "C22", files: ("lean/EEUL/L112/Chain.lean", "lean/CheckAxioms.lean", "lean/check.sh", "lean/expected-axioms.txt"),
   en: [Lean formalization of the deduction from F1–F5 to Theorem A (F5b by certificates or by canonical forms), and its check: build, no forbidden keyword, axioms as in `expected-axioms.txt` (standard only)],
   ja: [F1〜F5 から定理 A を導く論理の Lean による形式化（F5b は証明書・標準形のどちらでも）と、その検査: ビルド、禁止語なし、公理が `expected-axioms.txt` のとおり（標準のみ）], time: [min]),
  (id: "C23", files: ("code/supplementary/nebe/identify_nebe.py", "code/supplementary/nebe/lattices.py", "code/supplementary/nebe/cycloquat.py"),
   en: [Identification of $L$ with Nebe's $L_(56,2)(tilde(M))$ built from the definition; $tau$ as right multiplication by an element of reduced norm 5],
   ja: [定義から作った Nebe の $L_(56,2)(tilde(M))$ と $L$ の同定。$tau$ は被約ノルム 5 の元の右乗法], time: [≈ 40 min]),
  (id: "C24", files: ("code/supplementary/automorphisms/aut_normalizer.py", "code/supplementary/automorphisms/aut_common.py", "code/supplementary/_shared.py"),
   en: [The centralizer of $"SL"_2(29)$ in $"Aut"(L_112)$ (order 48) and an automorphism of $L_112$ inducing the outer automorphism],
   ja: [$"Aut"(L_112)$ における $"SL"_2(29)$ の中心化群（位数 48）と、外部自己同型を与える $L_112$ の自己同型], time: [15 min]),
  (id: "C25", files: ("code/supplementary/automorphisms/group_facts.g", "code/supplementary/automorphisms/out_facts.g", "code/supplementary/automorphisms/aut_diagonal.py", "code/supplementary/automorphisms/aut_common.py", "code/supplementary/_shared.py"),
   en: [Finite group facts G-F1–G-F5 used in Appendix F (GAP), and the diagonal case; further checks G-F6–G-F12 are retained in the code],
   ja: [付録 F で使う有限群の事実 G-F1〜G-F5（GAP）と、対角の場合。追加検査 G-F6〜G-F12 はコードに保存], time: [min]),
  (id: "C26", files: ("code/supplementary/automorphisms/aut_structure.py", "code/supplementary/automorphisms/aut_character.py", "code/supplementary/automorphisms/endomorphisms.py", "code/supplementary/automorphisms/aut_common.py", "code/supplementary/_shared.py"),
   en: [Structure of $"Aut"(L_112)$: order of the generated group, non-split extension, quotients, Molien series; the $ZZ[sqrt(-29)]$- and $cal(O)_K$-structures],
   ja: [$"Aut"(L_112)$ の構造: 生成した群の位数、分裂しない拡大、商、Molien 級数。$ZZ[sqrt(-29)]$-構造と $cal(O)_K$-構造], time: [≈ 45 min]),
  (id: "C27", files: ("code/crosscheck/all_data/check_all.py", "code/crosscheck/all_data/min_L.py", "code/crosscheck/all_data/min_L_enum.c"),
   en: [Independent re-check of all certificates and of F1 by separately written code (integer arithmetic; float32 products only with proved bounds on all partial sums)],
   ja: [すべての代表元と F1 の、作成側と別に書いたコードによる検算（整数演算。float32 の積は部分和の上界を証明した場合だけ）], time: [≈ 10 h]),
  (id: "C28", files: ("code/supplementary/isometry_ab.py", "code/supplementary/_shared.py"),
   en: [Gluings A and B are isometric: an explicit basis change $T$ with $T G_B T^top = G_A$, checked in integer arithmetic ($det T = plus.minus 1$)],
   ja: [貼り方 A と B は等長同型: $T G_B T^top = G_A$ を満たす基底変換 $T$ を明示し、整数演算で検算（$det T = plus.minus 1$）], time: [find 8 min; check 2 s]),
  (id: "C29", files: ("code/supplementary/genus/genus.py", "code/supplementary/genus/genus_steps.py", "code/supplementary/genus/genus_lattice.py", "code/supplementary/genus/genus_data.py"),
   en: [The $"SL"_2(29)$-invariant even unimodular lattices of dimension 112 (`local`, `mass`, `enum`): the image of the group ring is maximal at $p = 2, 3, 5, 7, 29$ ($FF_p$-algebras of dimension 392), so every such lattice is $L_(56,2)(M) times.o_M Lambda$; $zeta_K (-1) = 1\/2$, $zeta_K (-3) = 157\/20$ ($K = QQ(sqrt(29))$, generalized Bernoulli numbers) and the mass $157\/640$; Kneser neighbours at the prime of norm 5 (fixed random seed) reach the mass with 8 classes, $|U(Lambda)| = 1152, 12, 288, 24, 24, 20, 288, 48$ (PARI `qfauto`)],
   ja: [112 次元の $"SL"_2(29)$ 不変な偶ユニモジュラー格子（`local`、`mass`、`enum`）: 群環の像は $p = 2, 3, 5, 7, 29$ で極大（$FF_p$-代数の次元 392）で、どれも $L_(56,2)(M) times.o_M Lambda$。$zeta_K (-1) = 1\/2$、$zeta_K (-3) = 157\/20$（$K = QQ(sqrt(29))$、一般化 Bernoulli 数）と質量 $157\/640$。ノルム 5 の素イデアルでの Kneser の近傍（乱数シードは固定）で質量に達し 8 類、$|U(Lambda)| = 1152, 12, 288, 24, 24, 20, 288, 48$（PARI の `qfauto`）], time: [local 20 min; mass 1 s; enum 16 min]),
  (id: "C30", files: ("code/supplementary/genus/genus.py", "code/supplementary/genus/genus_steps.py", "code/supplementary/genus/genus_lattice.py", "code/supplementary/genus/genus_data.py"),
   en: [The 8 lattices $X_j = L_(56,2)(frak(M)) times.o_(frak(M)) Lambda_j$ (`build`; Gram matrices and bases in the coordinates of (3.1) in the verification data), their mod-2 frames (`frames`), and vectors of norm 8 in classes 3, 4, 5 from fixed sublattices (`witness`)],
   ja: [8 つの格子 $X_j = L_(56,2)(frak(M)) times.o_(frak(M)) Lambda_j$（`build`。Gram 行列と (3.1) の座標での基底を検証用データに）、その mod 2 の枠（`frames`）、固定部分格子から取り出した類 3, 4, 5 のノルム 8 のベクトル（`witness`）], time: [build 4 min; frames 12 min; witness 2 min]),
  (id: "C31", files: ("code/supplementary/genus/genus.py", "code/supplementary/genus/genus_steps.py", "code/supplementary/genus/genus_lattice.py", "code/supplementary/genus/genus_check.py", "code/supplementary/genus/genus_data.py", "code/supplementary/_shared.py"),
   en: [Explicit $"SL"_2(29)$-equivariant isometries class 7 → $L_112$ and class 3 → gluing A, and a recount of $|U(Lambda_j)|$ as equivariant automorphisms (`identify`); integer-arithmetic check, numpy only (`check`): each $G_X$ even with determinant 1, $g_1, g_2$ act on $X_j$, the vectors of norm 8, the isometries ($det T = plus.minus 1$), and $sum_j 1\/|U(Lambda_j)| = 157\/640$],
   ja: [明示的な $"SL"_2(29)$ 同変な等長写像 類 7 → $L_112$、類 3 → 貼り方 A と、同変な自己同型としての $|U(Lambda_j)|$ の数え直し（`identify`）。numpy だけの整数演算の検算（`check`）: 各 $G_X$ が偶で行列式 1、$g_1, g_2$ が $X_j$ に働く、ノルム 8 のベクトル、等長写像（$det T = plus.minus 1$）、$sum_j 1\/|U(Lambda_j)| = 157\/640$], time: [identify 13 min; check 80 s]),
)

#let _calc-ids = calcs.map(c => c.id)

// 本文の参照: #calc("C5") → [C5]（付録の行へのリンク）
#let calc(..ids) = {
  let xs = ids.pos()
  for x in xs { assert(x in _calc-ids, message: "unknown computation " + x) }
  [\[]
  xs.map(x => link(label("calc-" + x), x)).join(", ")
  [\]]
}

#let calc-table(lang: "en") = {
  let head = if lang == "ja" { ([ID], [計算とコード（特記しない限り公開リポジトリでのパス）], [時間]) } else { ([ID], [computation and code (public-repository paths unless marked otherwise)], [time]) }
  block(above: 0.8em, below: 0.4em, text(size: 0.92em, if lang == "ja" [表 D2. 計算とコード。本文の \[C1\] などはこの表の行を指す。] else [Table D2. Computations and code. References such as \[C1\] in the text point to the rows of this table.]))
  table(columns: (auto, 1fr, auto), align: (left, left, right),
    table.header(..head),
    ..calcs.map(c => (
      [#c.id #label("calc-" + c.id)],
      {
        if lang == "ja" { c.ja } else { c.en }
        linebreak()
        text(size: 0.8em, c.files.map(f => if c.at("published", default: true) { link(code-base + f, raw(f)) } else { raw(f) }).join(linebreak()))
      },
      c.time,
    )).flatten()
  )
}
