# 112 次元の極値偶ユニモジュラー格子の候補

English: [README.md](README.md)

> **現状（2026-10-14）: 候補であって、定理ではありません。**
> 112次元の偶ユニモジュラー格子 $R$ を具体的に与え、その最小ノルムが10（= 極値）であることを示す計算上の証拠を説明します。
> 証拠は有限の計算で、1つずつ確かめられる10のステップ（[§4](#4-論証の10ステップ)）に整理してあります。検証の計算の一部はまだ実行中です（[§5](#5-どこが間違っているかもしれないか)）。**査読を受けておらず、専門家の確認も経ていません。**
> 探索・コード・計算と、この文章の大部分は AI（Anthropic の Claude）によるもので、人間のアマチュアが方向を決めました。各ステップは AI の2つの別々のセッションが別々に書いたコードで確かめましたが、人間が1行ずつ検証したわけではありません。
> この格子が既に調べられていることをご存じの方、ノルム10未満のベクトルを見つけた方は、ぜひお知らせください。そのようなベクトルが1本あれば決着します。

## 1. 主張

$L$ を、$\mathrm{SL}_2(29)$ が作用する56次元の極値偶ユニモジュラー格子とします（[`data/`](data/) にあります。Nebe [[Neb98]](#Neb98) の格子の1つ。何を同定できていて何ができていないかは [§5](#5-どこが間違っているかもしれないか)）。
$L$ には、$\mathrm{SL}_2(29)$ と可換な自己準同型 $\tau$ で

```math
\tau^2 = -5, \qquad \langle x\tau,\, y\tau \rangle = 5\,\langle x, y \rangle \quad (x, y \in L)
```

となるものがあります。これを使って

```math
R = \left\lbrace \tfrac{1}{\sqrt 2}\,(x,\; x\tau + 2y) \;:\; x, y \in L \right\rbrace \subset (L \oplus L) \otimes ℚ
```

と定めます。言い換えると $R = H \otimes_{ℤ[\sqrt{-5}]} L$ で、$H$ は次の Gram 行列をもつ階数2のユニモジュラーなエルミート格子です。

```math
H = \begin{pmatrix} 3 & \sqrt{-5} \\ -\sqrt{-5} & 2 \end{pmatrix}, \qquad \det H = 6 - 5 = 1 .
```

**厳密に確かめたこと**（[`verify/01_basic.py`](verify/01_basic.py)、整数演算、数秒）: $R$ は112次元の偶ユニモジュラー格子で、$\mathrm{SL}_2(29)$ が作用する。

**計算上の証拠に基づく主張（[§4](#4-論証の10ステップ)）**: $\min(R) = 10$。112次元の上界は $2\lfloor 112/24 \rfloor + 2 = 10$ なので、$R$ は極値格子ということになります。これまで極値偶ユニモジュラー格子が知られていた最大の次元は88です [[Sak26]](#Sak26)。

ここで「$\sqrt{-5}$」は、実の格子 $L$ に線形写像 $\tau$ として作用しています（[質問と答え](docs/faq.ja.md)）。

**構成そのものに新しいところはありません。** 格子 $L$ は1998年のものです [[Neb98]](#Neb98)。格子の2枚ないし3枚のコピーを $L/2L$ に沿って貼り合わせる方法と、それと同じ内容を表すエルミートテンソル積は、標準的な道具です: Quebbemann の構成 [[Que84]](#Que84)、$\Gamma_{72}$ の背後にある Turyn 型の構成 [[Neb12]](#Neb12)、エルミートテンソル積 [[CN13]](#CN13), [[Sak26]](#Sak26)。新しいのは（正しければ）、2種類ある $\tau$ の一方で最小ノルムが10になるという観察と、それを支える計算だけです。

このような $\tau$ は、単数による共役を除いて2種類あります。もう一方の $\tau$ から作った格子は最小ノルム8（ノルム8のベクトルがちょうど $`292\,320`$ 本）で、以下のすべての検査の「外れの対照」として使っています。

## 2. 背景

以下、$\langle x, y \rangle$ は内積、$\langle x, x \rangle$（長さの2乗）を $x$ の**ノルム**と呼びます。丸括弧 $(x, v)$ は2つのベクトルの組です。

**偶ユニモジュラー格子**とは、格子 $\Lambda \subset ℝ^n$ で、すべての $x \in \Lambda$ について $\langle x, x \rangle \in 2ℤ$、行列式が1のものです。$n \equiv 0 \pmod 8$ のときだけ存在します。
**テータ級数**

```math
\theta_\Lambda(q) = \sum_{x \in \Lambda} q^{\langle x,x \rangle/2}
```

は $\mathrm{SL}_2(ℤ)$ の重さ $n/2$ の保型形式になり、そこから次の上界が出ます [[MOS75]](#MOS75)。

```math
\min(\Lambda) \le 2\left\lfloor \frac{n}{24} \right\rfloor + 2 .
```

等号を達成する格子を**極値**（extremal）と呼びます。$n > 163264$ では極値格子は存在しません [[JR11]](#JR11)。96次元以上の極値偶ユニモジュラー格子は1つも知られていません。

### 2.1 極値テータ級数

次のように置きます。

```math
\begin{aligned}
A &= \theta_{E_8} = E_4 = 1 + 240q + 2160q^2 + 6720q^3 + \cdots, \\
B &= \theta_{\Lambda_{24}} = E_4^3 - 720\Delta = 1 + 196560q^2 + 16773120q^3 + 398034000q^4 + \cdots .
\end{aligned}
```

ここで $E_8$ は $E_8$ ルート格子（8次元でただ1つの偶ユニモジュラー格子）、$\Lambda_{24}$ は Leech 格子（24次元の偶ユニモジュラー格子のうち、ノルム2のベクトルを持たないただ1つのもの）です。保型形式の側では、$E_4$ は重さ4のアイゼンシュタイン級数、$\Delta$ は重さ12の尖点形式です。

```math
E_4 = 1 + 240\sum_{n \ge 1} \sigma_3(n)\, q^n, \qquad \Delta = q \prod_{n \ge 1} (1 - q^n)^{24} = q - 24q^2 + 252q^3 - \cdots .
```

$\sigma_3(n)$ は $n$ の約数の3乗の和です。

重さ $4k$ の保型形式はすべて $A$ と $B$ の多項式（単項式 $A^{k-3j}B^{j}$ の一次結合）で書け、$n = 8k$ 次元の極値テータ級数は $1 + O(q^{\lfloor n/24 \rfloor + 1})$ の形をした唯一のものです。
$q$ の指数はノルムの半分です。表は [`verify/theta_series.py`](verify/theta_series.py) が有理数の厳密計算で出力します。

| 次元 | 最小 | 極値テータ級数（$A$, $B$ の多項式） | 最初の項（最初の係数が接吻数） |
|---|---|---|---|
| 8 | 2 | $A$ | $1 + 240q + 2160q^{2} + 6720q^{3} + \cdots$ |
| 16 | 2 | $A^{2}$ | $1 + 480q + 61920q^{2} + 1050240q^{3} + \cdots$ |
| 24 | 4 | $B$ | $1 + 196560q^{2} + 16773120q^{3} + 398034000q^{4} + \cdots$ |
| 32 | 4 | $\tfrac{1}{3}\left(- A^{4} + 4AB\right)$ | $1 + 146880q^{2} + 64757760q^{3} + 4844836800q^{4} + \cdots$ |
| 40 | 4 | $\tfrac{1}{3}\left(- 2A^{5} + 5A^{2}B\right)$ | $1 + 39600q^{2} + 87859200q^{3} + 20779902000q^{4} + \cdots$ |
| 48 | 6 | $\tfrac{1}{120}\left(- 91A^{6} + 182A^{3}B + 29B^{2}\right)$ | $1 + 52416000q^{3} + 39007332000q^{4} + 6609020221440q^{5} + \cdots$ |
| 56 | 6 | $\tfrac{1}{240}\left(- 159A^{7} + 238A^{4}B + 161AB^{2}\right)$ | $1 + 15590400q^{3} + 36957286800q^{4} + 15284192071680q^{5} + \cdots$ |
| 64 | 6 | $\tfrac{1}{90}\left(- 41A^{8} + 22A^{5}B + 109A^{2}B^{2}\right)$ | $1 + 2611200q^{3} + 19524758400q^{4} + 19715347537920q^{5} + \cdots$ |
| 72 | 8 | $\tfrac{1}{2160}\left(- 455A^{9} - 1092A^{6}B + 3549A^{3}B^{2} + 158B^{3}\right)$ | $1 + 6218175600q^{4} + 15281788354560q^{5} + 9026867482214400q^{6} + \cdots$ |
| 80 | 8 | $\tfrac{1}{1944}\left(28A^{10} - 2109A^{7}B + 3486A^{4}B^{2} + 539AB^{3}\right)$ | $1 + 1250172000q^{4} + 7541401190400q^{5} + 9236514405888000q^{6} + \cdots$ |
| 88 | 8 | $\tfrac{1}{19440}\left(3413A^{11} - 26466A^{8}B + 29733A^{5}B^{2} + 12760A^{2}B^{3}\right)$ | $1 + 168498000q^{4} + 2480127344640q^{5} + 6298997202432000q^{6} + \cdots$ |
| 96 | 10 | $\tfrac{1}{2073600}\left(532259A^{12} - 2711436A^{9}B + 1795794A^{6}B^{2} + 2413684A^{3}B^{3} + 43299B^{4}\right)$ | $1 + 565866362880q^{5} + 2972108280960000q^{6} + 4164608980546560000q^{7} + \cdots$ |
| 104 | 10 | $\tfrac{1}{74649600}\left(19575997A^{13} - 73035508A^{10}B - 4414098A^{7}B^{2} + 124747532A^{4}B^{3} + 7775677AB^{4}\right)$ | $1 + 91508901120q^{5} + 1000989033408000q^{6} + 2598412027506048000q^{7} + \cdots$ |
| **112** | **10** | $\tfrac{1}{37324800}\left(7883087A^{14} - 18165308A^{11}B - 38110758A^{8}B^{2} + 74301892A^{5}B^{3} + 11415887A^{2}B^{4}\right)$ | $1 + 10888335360q^{5} + 247006775232000q^{6} + 1187911731935232000q^{7} + \cdots$ |
| 120 | 12 | $\tfrac{1}{124416000}\left(16107182A^{15} + 4100915A^{12}B - 221155480A^{9}B^{2} + 241917130A^{6}B^{3} + 82692610A^{3}B^{4} + 753643B^{5}\right)$ | $1 + 45792819072000q^{6} + 406954241261568000q^{7} + 1074181924443974346000q^{8} + \cdots$ |

主張が正しければ、$R$ にはノルム2, 4, 6, 8のベクトルが無く、ノルム10がちょうど $`10\,888\,335\,360`$ 本、ノルム12が $`247\,006\,775\,232\,000`$ 本あります。
（ノルム10の本数は**数えていません**。[§5](#5-どこが間違っているかもしれないか)。）

### 2.2 これまでに知られている極値偶ユニモジュラー格子

| 次元 | 最小 | 知られている個数 | 最初の構成（年） | 文献 |
|---|---|---|---|---|
| 8 | 2 | 1（一意） | $E_8$（Korkine–Zolotareff 1873） | [[SPLAG]](#SPLAG) |
| 16 | 2 | 2（全部） | $E_8 \perp E_8$, $D_{16}^+$（Witt 1941） | [[SPLAG]](#SPLAG) |
| 24 | 4 | 1（一意） | Leech 格子（Leech 1967、一意性は Conway 1969） | [[SPLAG]](#SPLAG) |
| 32 | 4 | $10^7$ 個超 | 多数。質量公式による下界（King 2003） | [[Kin03]](#Kin03) |
| 40 | 4 | $10^{51}$ 個超 | 質量公式による下界（King 2003） | [[Kin03]](#Kin03) |
| 48 | 6 | 4 | $P_{48p}$, $P_{48q}$（Leech–Sloane 1971）、$P_{48n}$（Nebe 1998）、$P_{48m}$（Nebe 2014） | [[LS71]](#LS71), [[Neb98]](#Neb98), [[Neb14]](#Neb14) |
| 56 | 6 | 複数 | Ozeki 1989、Batut–Quebbemann–Scharlau 1995、Nebe 1998 | [[BQS95]](#BQS95), [[Neb98]](#Neb98) |
| 64 | 6 | 多数 | Quebbemann 1984、Shimada 2018 | [[Que84]](#Que84), [[Shi18]](#Shi18) |
| 72 | 8 | 1 | $\Gamma_{72}$（Nebe 2010） | [[Neb12]](#Neb12), [[CN13]](#CN13) |
| 80 | 8 | 4 | Bachoc–Nebe 1998（2個）、Stehlé–Watkins 2010、Watkins 2012 | [[BN98]](#BN98), [[SW10]](#SW10), [[Wat12]](#Wat12) |
| 88 | 8 | 2 | 坂本 2026（プレプリント） | [[Sak26]](#Sak26) |
| 96, 104 | 10 | 0 | 未解決 | |
| **112** | **10** | **0（この候補）** | — | このリポジトリ |
| 120 | 12 | 0 | 未解決 | |

この表は [[Sak26, §1]](#Sak26) のサーベイと *Catalogue of Lattices* [[NS]](#NS) に従っています。原論文をすべて読んだわけではありません。64次元以下の「最初の構成」の帰属は、引用する前に原典で確認してください。発見は次元の順ではありません: 80（1998）→ 72（2010）→ 88（2026）。

## 3. データ

| ファイル | 中身 |
|---|---|
| [`data/L56_gram.txt`](data/L56_gram.txt) | $L$ の Gram 行列 $G$（$56 \times 56$） |
| [`data/sl2_29_generators.txt`](data/sl2_29_generators.txt) | $\mathrm{SL}_2(29) \subset \mathrm{Aut}(L)$ を生成する行列 $g_1, g_2$（位数5と7） |
| [`data/tau.txt`](data/tau.txt) | $\tau$ の行列（$56 \times 56$）、$\tau^2 = -5$ |
| [`data/R112_gram_LLL.txt`](data/R112_gram_LLL.txt) | $R$ の Gram 行列（$112 \times 112$、LLL 簡約済み） |

$L$, $g_1$, $g_2$, $\tau$ は、*Catalogue of Lattices* [[NS]](#NS) の項目 $L_{56,2}(M)$（Gram 行列と、自己同型群の部分群の生成元）から作りました。

約束: 行ベクトル。行列 $M$ は $x \mapsto xM$ で作用し、等長写像は $M G M^{\mathrm{T}} = G$ をみたします。基底 $(x, x\tau)$, $(0, 2y)$（$\sqrt 2$ で割る前）に関する $R$ の Gram 行列は次のとおりです。

```math
\begin{pmatrix} 3G & \tau G \\ (\tau G)^{\mathrm{T}} & 2G \end{pmatrix} .
```

## 4. 論証の10ステップ

なぜ $\min(R) = 10$ と考えるかを、順に述べます。

$R$ のベクトルは $z = \tfrac{1}{\sqrt 2}(x, v)$（$x \in L$、$v \equiv x\tau \pmod{2L}$）で、

```math
\langle z, z \rangle = \tfrac12\bigl[\langle x, x \rangle + \langle v, v \rangle\bigr] .
```

ノルム $a$ の $x$ について、類 $x\tau + 2L$ にノルム $b$ のベクトル $v$ があるとき、**$(a, b)$ 型の衝突**があると言うことにします。

| # | ステップ | 確かめ方 | 誰が |
|---|---|---|---|
| 1 | $R$ は112次元の偶ユニモジュラー格子 | 整数演算（[`verify/01_basic.py`](verify/01_basic.py)） | 両セッション |
| 2 | $\min(L) = 6$。したがって $L$ は極値で、ノルム6が $`15\,590\,400`$ 本、ノルム8が $`36\,957\,286\,800`$ 本（[§2.1](#21-極値テータ級数)） | ノルム4以下の全列挙: fpylll（2つの基底）と PARI `qfminim`（3つ目の基底）。どちらも内部で浮動小数点を使う | 両セッション、別のソフト |
| 3 | $x = 0$ または $v = 0$ なら $\langle z, z \rangle \ge 12$。$R$ が偶格子なので $\langle x, x \rangle + \langle v, v \rangle \equiv 0 \pmod 4$。よってノルム10未満のベクトルは $(6,6)$, $(6,10)$, $(10,6)$, $(8,8)$ 型の衝突から来る | 手計算 | 両方が導き直した |
| 4 | $\tau$ は $\mathrm{SL}_2(29)$ と可換なので、$\mathrm{SL}_2(29)$ の各軌道から $x$ を1つ調べれば足りる | 厳密 | 両方 |
| 5 | $L$ の最小ベクトル $`15\,590\,400`$ 本は $\mathrm{SL}_2(29)$ の656軌道をなし、代表の一覧に漏れがない | 軌道の大きさの合計が $`15\,590\,400`$。軌道は互いに交わらない。球面デザインの恒等式（次数2, 4, 6）が一覧の上で厳密に成り立つ | 両方、別の方法 |
| 6 | $(6,6)$ 型の衝突なし | 厳密（mod $2L$ の類の標準形） | 両方、別のコード |
| 7 | $(6,10)$・$(10,6)$ 型の衝突なし | 整数の証明書: 656個の類それぞれに、その類のノルム14か18のベクトル $w_0$ で、すべての最小ベクトル $u$ について $\lvert \langle w_0, u \rangle \rvert \le 6$ となるもの（これがあれば類にノルム10以下の元は無い）。$\tau^2 \equiv 1 \pmod 2$ なので片方の向きで足りる | 一方のセッションが作成、他方が別のコードで検算 |
| 8 | ノルム8のベクトル $`36\,957\,286\,800`$ 本は $\mathrm{SL}_2(29)$ の $`1\,517\,130`$ 軌道をなし、一覧に漏れがない | 軌道の大きさの合計が $`36\,957\,286\,800`$。デザインの恒等式（次数2, 4, 6）が厳密に成り立つ | 両方、別の方法 |
| 9 | $(8,8)$ 型の衝突なし | （代表, 単数）の全 $`1\,527\,984`$ 組の全数検査で衝突0。同じ検査は、もう一方の $\tau$ では10組（6軌道、ノルム8のベクトル $`292\,320`$ 本）の衝突を見つける | 両方、別のコード、考え方は同じ（標準形）。標準形も群も使わない3本目（最近ベクトルの計算）は**実行中** |
| 10 | よってノルム10未満のベクトルは無い。ノルム10のベクトルは存在する（具体的に見つけた）ので $\min(R) = 10$ | | |

ステップ8と9の**単数**とは、$\mathrm{SL}_2(29)$ と可換な $L$ の等長写像のことで、12個（符号を除いて6個）あります。軌道代表は、$\mathrm{SL}_2(29)$ と単数で生成される大きい群について求めました（$`254\,664`$ 軌道）。単数は $\tau$ と可換でないので、（代表, 単数）の組をすべて調べる必要があり、$254664 \times 6 = 1527984$ 組になります。

ステップ7の証明書の仕組み: $w \ne \pm w_0$ が $w_0$ と同じ類にあれば、$y_\pm = \tfrac12(w_0 \pm w) \in L \setminus \lbrace 0 \rbrace$ なので $\langle w_0, w_0 \rangle + \langle w, w \rangle \pm 2\langle w_0, w \rangle \ge 24$。$\langle w_0, w_0 \rangle \in \lbrace 14, 18 \rbrace$ かつ $\langle w, w \rangle \le 10$ なら、$y_\pm$ の一方が最小ベクトルで $\langle w_0, y_\pm \rangle \ge 7$ となります。

証明の一部ではない整合性の確認: 位数3, 5, 7の自己同型の固定格子は32, 16, 16次元、厳密な最小ノルム12, 10, 14、行列式 $3^{32}$, $5^{16}$, $7^{16}$。その型3-(40,32)-32、5-(24,16)-16、7-(16,16)-16は、Nebe 型の密度の議論 [[Neb13b]](#Neb13b) で112次元の極値格子から排除されない型に入っています。

## 5. どこが間違っているかもしれないか

弱いと考える点を、深刻な順に並べます。

1. **論証の組み立てそのもの。** 2回の確認は、どちらも同じ AI モデルのセッションによるものです。コードが別でも、ステップ3〜4やステップ6〜9の論理に共通の考え違いがあれば防げません。
2. **ステップ9。** 2本の全数検査は同じ考え方を使っています。考え方の違う3本目はまだ終わっていません。
3. **ステップ2。** どちらの全列挙も浮動小数点の枝刈りを使っています。$\min(L) = 6$ の、整数演算だけの証明はここにはありません（$L$ が同定できれば文献から従うはずです。5を参照）。
4. **$R$ への直接の検査が無い。** 112次元の格子そのものへの格子簡約（BKZ、ブロックサイズ60まで）と、群の元の固定格子は試しましたが、これらは**外れのほうの $\tau$** のノルム8のベクトルも検出できませんでした。証拠になりません。112次元の格子の最小ノルムを直接計算することは、私たちの手には負えません。
5. **同定と文献。** $L$ は Nebe の格子 $L_{56,2}(M)$ [[NS]](#NS) の中に作ったもので、カタログのどの格子と等長かを確認できていません。構成は単純なので、既に調べられている可能性は十分にあります。簡単な検索では何も見つかりませんでした。
6. **やっていないこと:** ノルム10のベクトル $`10\,888\,335\,360`$ 本を数えること（強い独立な検算になります）。自己同型群の全体の決定。2つの土台から得られる最小ノルム8の格子2つが等長かどうか。

## 6. ここに至るまで（短い版）

[§2.2](#22-これまでに知られている極値偶ユニモジュラー格子) の表を理解し、できれば伸ばしたい、という趣味のプロジェクトから出てきました。失敗も含めた長い版は [docs/history.md](docs/history.md) にあります。

- 先に、96〜112次元の候補を190個以上調べ、一覧表に記録しました（円分体のイデアル格子とそのイデアル類によるひねり、エルミートテンソル積、48 + 48の貼り合わせ）。そのすべてでノルム8以下のベクトルが見つかりました。
- 見積もり: 「極値の上界より短いベクトルの本数」の Siegel 平均を、自由に作用する群の位数で割ると、でたらめな対称格子に「短すぎるベクトル」の軌道が何個あるかの目安になります。Siegel 平均は96次元で約 $1.6 \times 10^7$、 112次元では $5.1 \times 10^4$ で、$\lvert \mathrm{SL}_2(29) \rvert = 24360$ と同じ桁です。112次元とこの群を試したのはそのためです。

  極値格子が持ってはならないベクトルの本数の Siegel 平均 $S(n)$（[`verify/siegel_mean.py`](verify/siegel_mean.py)）:

  | 周期 | $n \equiv 0$ | $n \equiv 8$ | $n \equiv 16 \pmod{24}$ |
  |---|---|---|---|
  | 1 | 24: $95$ | 32: $4.5$ | 40: $0.08$ |
  | 2 | 48: $4.7 \times 10^3$ | 56: $275$ | 64: $9.1$ |
  | 3 | 72: $2.6 \times 10^5$ | 80: $1.7 \times 10^4$ | 88: $716$ |
  | 4 | 96: $1.6 \times 10^7$ | 104: $1.1 \times 10^6$ | **112: $5.1 \times 10^4$** |
  | 5 | 120: $9.7 \times 10^8$ | 128: $6.6 \times 10^7$ | 136: $3.5 \times 10^6$ |

  $n = 2k$ のとき、ノルム $2m$ のベクトルの本数の平均は $\frac{2k}{\lvert B_k \rvert}\sigma_{k-1}(m)$（Siegel）で、$S(n)$ はその $1 \le m \le \lfloor n/24 \rfloor$ にわたる和です。24次元の周期の中では、 8次元ごとに条件が約15〜20分の1に緩み、上界が上がる次元で跳ね上がります。これは歴史の一部と合います: 80次元（1998）は72次元（2010）より先に、 64次元（1984）は56次元（1989）より先に見つかりました。あくまで粗い目安です（88次元はその周期で最後でした）。
- Nebe の56次元格子2枚を mod 2 で貼り合わせる方法のうち、$\mathrm{SL}_2(29)$ を保つものを全部列挙しました（5類）。2類は即座に外れ、残る3類のうち2類はノルム8のベクトルをちょうど $`292\,320`$ 本持ち、1類がこの候補です。

## 7. 再現

必要なもの: SageMath 10以上（PARI と fpylll を含む）。計算は SageMath 10.9（conda-forge）で行いました。同じ環境は [`environment.yml`](environment.yml) で作れます。[`Dockerfile`](Dockerfile) も置いてありますが、ビルドは未確認です。

```
sage -python verify/theta_series.py 56 112     # §2.1
sage -python verify/theta_series.py --table    # §2.1 の表
sage -python verify/01_basic.py                # ステップ 1 と §1 の事実（数秒）
```

**まだここに無いもの**（順次追加します）: ステップ2, 5〜9の単独で動くスクリプト（今は非公開の作業用リポジトリにあり、そのライブラリに依存しています）。ステップ7の証明書と軌道代表のデータファイル。外れの $\tau$ についてのノルム8の証拠ベクトル。

## 8. 著者と AI の使用

- 方向づけ、問題の選択、判断、公開の責任: roiban1344。
- 探索の方針、コード、計算、検証、この文章の下書き: Claude（Anthropic）。複数の独立したセッションによります。
- ここでの主張と、その誤りの責任は roiban1344 が負います。

## ライセンス

コード（`verify/`）は MIT ライセンス（[LICENSE](LICENSE)）、文章とデータ（`README*.md`, `docs/`, `data/`）は [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) です。

## 文献

- <a id="BN98"></a>[BN98] C. Bachoc, G. Nebe, *Extremal lattices of minimum 8 related to the Mathieu group $M_{22}$*, J. reine angew. Math. 494 (1998) 155–171. [author's PDF](https://www.math.rwth-aachen.de/~Gabriele.Nebe/papers/extremm22.pdf)
- <a id="BQS95"></a>[BQS95] C. Batut, H.-G. Quebbemann, R. Scharlau, *Computations of cyclotomic lattices*, Experiment. Math. 4 (1995) 175–179.
- <a id="CN13"></a>[CN13] R. Coulangeon, G. Nebe, *Dense lattices as Hermitian tensor products*, Contemp. Math. 587 (2013). [arXiv:1201.1832](https://arxiv.org/abs/1201.1832)
- <a id="JR11"></a>[JR11] P. Jenkins, J. Rouse, *Bounds for coefficients of cusp forms and extremal lattices*, Bull. London Math. Soc. 43 (2011). [arXiv:1012.5991](https://arxiv.org/abs/1012.5991)
- <a id="Kin03"></a>[Kin03] O. King, *A mass formula for unimodular lattices with no roots*, Math. Comp. 72 (2003). [arXiv:math/0012231](https://arxiv.org/abs/math/0012231)
- <a id="LS71"></a>[LS71] J. Leech, N. J. A. Sloane, *Sphere packing and error-correcting codes*, Canad. J. Math. 23 (1971) 718–745.
- <a id="MOS75"></a>[MOS75] C. L. Mallows, A. M. Odlyzko, N. J. A. Sloane, *Upper bounds for modular forms, lattices, and codes*, J. Algebra 36 (1975) 68–76. [doi:10.1016/0021-8693(75)90155-6](https://doi.org/10.1016/0021-8693(75)90155-6)
- <a id="Neb98"></a>[Neb98] G. Nebe, *Some cyclo-quaternionic lattices*, J. Algebra 199 (1998) 472–498. [doi:10.1006/jabr.1997.7163](https://doi.org/10.1006/jabr.1997.7163)
- <a id="Neb12"></a>[Neb12] G. Nebe, *An even unimodular 72-dimensional lattice of minimum 8*, J. reine angew. Math. 673 (2012) 237–247. [arXiv:1008.2862](https://arxiv.org/abs/1008.2862)
- <a id="Neb13b"></a>[Neb13b] G. Nebe, *On automorphisms of extremal even unimodular lattices*, Int. J. Number Theory 9 (2013). [arXiv:1212.0865](https://arxiv.org/abs/1212.0865)
- <a id="Neb14"></a>[Neb14] G. Nebe, *A fourth extremal even unimodular lattice of dimension 48*, Discrete Math. 331 (2014). [arXiv:1312.3780](https://arxiv.org/abs/1312.3780)
- <a id="NS"></a>[NS] G. Nebe, N. J. A. Sloane, *A Catalogue of Lattices*. [web page](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/); the entry for [$L_{56,2}(M)$](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/L_56b.html).
- <a id="Que84"></a>[Que84] H.-G. Quebbemann, *A construction of integral lattices*, Mathematika 31 (1984) 137–140.
- <a id="Sak26"></a>[Sak26] R. Sakamoto, *Two extremal even unimodular lattices of rank 88*, preprint (2026). [arXiv:2609.15633](https://arxiv.org/abs/2609.15633); [code](https://github.com/RyotaroSakamoto0113/rank-88-extremal-lattice-computations)
- <a id="Shi18"></a>[Shi18] I. Shimada, *An even extremal lattice of rank 64*, J. Number Theory 185 (2018). [arXiv:1710.02629](https://arxiv.org/abs/1710.02629)
- <a id="SPLAG"></a>[SPLAG] J. H. Conway, N. J. A. Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed., Springer 1999. [doi:10.1007/978-1-4757-6568-7](https://doi.org/10.1007/978-1-4757-6568-7)
- <a id="SW10"></a>[SW10] D. Stehlé, M. Watkins, *On the extremality of an 80-dimensional lattice*, ANTS-IX, LNCS 6197 (2010) 340–356. [doi:10.1007/978-3-642-14518-6_27](https://doi.org/10.1007/978-3-642-14518-6_27)
- <a id="Wat12"></a>[Wat12] M. Watkins, *Another 80-dimensional extremal lattice*, J. Théor. Nombres Bordeaux 24 (2012). [author's PDF](https://magma.maths.usyd.edu.au/~watkins/papers/extrem80.pdf)
