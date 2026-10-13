# A candidate for an extremal even unimodular lattice of dimension 112

日本語版: [README.ja.md](README.ja.md)

> **Status (2026-10-14): a candidate, not a theorem.**
> We describe an explicit even unimodular lattice $R$ of dimension 112 and computational evidence that its minimum norm is 10, which would make it extremal.
> The evidence is a finite computation, organised as ten steps that can be checked one by one ([§4](#4-the-argument-in-ten-steps)). Part of the verification is still running ([§5](#5-what-could-be-wrong)). It has **not** been peer reviewed and has **not** been checked by an expert.
> The search, the code, the computations and most of this text were produced with an AI system (Claude, Anthropic), directed by a human amateur. Two separate AI sessions checked each step with separately written code; no human has verified it line by line.
> If you know that this lattice has been studied, or you find a vector of norm $< 10$, please tell us: one such vector settles the question.

## 1. The claim

Let $L$ be the 56-dimensional extremal even unimodular lattice with an action of $\mathrm{SL}_2(29)$ given in [`data/`](data/) (one of the lattices of Nebe [[Neb98]](#Neb98); see [§5](#5-what-could-be-wrong) for what we have and have not identified).
$L$ has an endomorphism $\tau$ commuting with $\mathrm{SL}_2(29)$ such that

```math
\tau^2 = -5, \qquad \langle x\tau,\, y\tau \rangle = 5\,\langle x, y \rangle \quad \text{for all } x, y \in L .
```

Define

```math
R = \left\lbrace \tfrac{1}{\sqrt 2}\,(x,\; x\tau + 2y) \;:\; x, y \in L \right\rbrace \subset (L \oplus L) \otimes ℚ .
```

Equivalently, $R = H \otimes_{ℤ[\sqrt{-5}]} L$, where $H$ is the unimodular Hermitian lattice of rank 2 with Gram matrix

```math
H = \begin{pmatrix} 3 & \sqrt{-5} \\ -\sqrt{-5} & 2 \end{pmatrix}, \qquad \det H = 6 - 5 = 1 .
```

**Verified exactly** ([`verify/01_basic.py`](verify/01_basic.py), integer arithmetic, seconds): $R$ is an even unimodular lattice of dimension 112, and $\mathrm{SL}_2(29)$ acts on it.

**Claimed, on computational evidence ([§4](#4-the-argument-in-ten-steps)):** $\min(R) = 10$. The bound for dimension 112 is $2\lfloor 112/24 \rfloor + 2 = 10$, so $R$ would be extremal. The largest dimension for which an extremal even unimodular lattice was previously known is 88 [[Sak26]](#Sak26).

Here "$\sqrt{-5}$" acts on the real lattice $L$ as the linear map $\tau$; see the [questions and answers](docs/faq.md).

**Nothing in the construction itself is new.** The lattice $L$ is from 1998 [[Neb98]](#Neb98). Gluing two or three copies of a lattice along $L/2L$, and the equivalent language of Hermitian tensor products, are standard tools: Quebbemann's construction [[Que84]](#Que84), the Turyn-type construction behind $\Gamma_{72}$ [[Neb12]](#Neb12), and Hermitian tensor products [[CN13]](#CN13), [[Sak26]](#Sak26). What is new, if it is correct, is only the observation that for one of the two possible $\tau$ the minimum is 10, together with the computation supporting it.

There are two classes of such $\tau$ up to conjugation by units. The other class gives a lattice with minimum 8 (exactly $`292\,320`$ vectors of norm 8); it serves as a negative control for every test below.

## 2. Background

Throughout, $\langle x, y \rangle$ is the inner product, and $\langle x, x \rangle$ (the squared length) is called the *norm* of $x$. Round brackets $(x, v)$ denote a pair of vectors.

An *even unimodular lattice* is a lattice $\Lambda \subset ℝ^n$ with $\langle x, x \rangle \in 2ℤ$ for all $x \in \Lambda$ and determinant 1. Such lattices exist only for $n \equiv 0 \pmod 8$.
Its *theta series*

```math
\theta_\Lambda(q) = \sum_{x \in \Lambda} q^{\langle x,x \rangle/2}
```

is a modular form of weight $n/2$ for $\mathrm{SL}_2(ℤ)$, and this forces [[MOS75]](#MOS75)

```math
\min(\Lambda) \le 2\left\lfloor \frac{n}{24} \right\rfloor + 2 .
```

Lattices attaining the bound are called *extremal*. Extremal lattices cannot exist for $n > 163264$ [[JR11]](#JR11). No extremal even unimodular lattice of dimension $\ge 96$ is known.

### 2.1 Extremal theta series

Write

```math
\begin{aligned}
A &= \theta_{E_8} = E_4 = 1 + 240q + 2160q^2 + 6720q^3 + \cdots, \\
B &= \theta_{\Lambda_{24}} = E_4^3 - 720\Delta = 1 + 196560q^2 + 16773120q^3 + 398034000q^4 + \cdots .
\end{aligned}
```

Here $E_8$ is the $E_8$ root lattice (the unique even unimodular lattice of dimension 8) and $\Lambda_{24}$ is the Leech lattice (the unique even unimodular lattice of dimension 24 without vectors of norm 2). On the side of modular forms, $E_4$ is the Eisenstein series of weight 4 and $\Delta$ is the cusp form of weight 12:

```math
E_4 = 1 + 240\sum_{n \ge 1} \sigma_3(n)\, q^n, \qquad \Delta = q \prod_{n \ge 1} (1 - q^n)^{24} = q - 24q^2 + 252q^3 - \cdots ,
```

where $\sigma_3(n)$ is the sum of the cubes of the divisors of $n$.

Every modular form of weight $4k$ is a polynomial in $A$ and $B$ (a combination of the monomials $A^{k-3j}B^{j}$), and the extremal theta series of dimension $n = 8k$ is the unique one of the form $1 + O(q^{\lfloor n/24 \rfloor + 1})$.
The exponent of $q$ is half the norm. The table is produced by [`verify/theta_series.py`](verify/theta_series.py) in exact rational arithmetic.

| dimension | min | extremal theta series as a polynomial in $A$, $B$ | first terms (the first coefficient is the kissing number) |
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

So if the claim is right, $R$ has no vectors of norm 2, 4, 6, 8, exactly $`10\,888\,335\,360`$ vectors of norm 10 and $`247\,006\,775\,232\,000`$ of norm 12.
(We have **not** counted the vectors of norm 10; see [§5](#5-what-could-be-wrong).)

### 2.2 Previously known extremal even unimodular lattices

| dimension | min | known extremal lattices | first constructions (year) | references |
|---|---|---|---|---|
| 8 | 2 | 1 (unique) | $E_8$ (Korkine–Zolotareff 1873) | [[SPLAG]](#SPLAG) |
| 16 | 2 | 2 (all) | $E_8 \perp E_8$, $D_{16}^+$ (Witt 1941) | [[SPLAG]](#SPLAG) |
| 24 | 4 | 1 (unique) | Leech lattice (Leech 1967; uniqueness Conway 1969) | [[SPLAG]](#SPLAG) |
| 32 | 4 | more than $10^7$ | many; lower bound from the mass formula (King 2003) | [[Kin03]](#Kin03) |
| 40 | 4 | more than $10^{51}$ | lower bound from the mass formula (King 2003) | [[Kin03]](#Kin03) |
| 48 | 6 | 4 | $P_{48p}$, $P_{48q}$ (Leech–Sloane 1971); $P_{48n}$ (Nebe 1998); $P_{48m}$ (Nebe 2014) | [[LS71]](#LS71), [[Neb98]](#Neb98), [[Neb14]](#Neb14) |
| 56 | 6 | several | Ozeki 1989; Batut–Quebbemann–Scharlau 1995; Nebe 1998 | [[BQS95]](#BQS95), [[Neb98]](#Neb98) |
| 64 | 6 | many | Quebbemann 1984; Shimada 2018 | [[Que84]](#Que84), [[Shi18]](#Shi18) |
| 72 | 8 | 1 | $\Gamma_{72}$ (Nebe 2010) | [[Neb12]](#Neb12), [[CN13]](#CN13) |
| 80 | 8 | 4 | Bachoc–Nebe 1998 (two); Stehlé–Watkins 2010; Watkins 2012 | [[BN98]](#BN98), [[SW10]](#SW10), [[Wat12]](#Wat12) |
| 88 | 8 | 2 | Sakamoto 2026 (preprint) | [[Sak26]](#Sak26) |
| 96, 104 | 10 | 0 | open | |
| **112** | **10** | **0 (this candidate)** | — | this repository |
| 120 | 12 | 0 | open | |

This table follows the survey in [[Sak26, §1]](#Sak26) and the *Catalogue of Lattices* [[NS]](#NS). We have not read every original paper; attributions of first constructions in dimensions $\le 64$ should be checked against the sources before being quoted. Note that discoveries did not come in order of dimension: 80 (1998), then 72 (2010), then 88 (2026).

## 3. Data

| file | content |
|---|---|
| [`data/L56_gram.txt`](data/L56_gram.txt) | Gram matrix $G$ of $L$ ($56 \times 56$) |
| [`data/sl2_29_generators.txt`](data/sl2_29_generators.txt) | two matrices $g_1, g_2$ (orders 5 and 7) generating $\mathrm{SL}_2(29) \subset \mathrm{Aut}(L)$ |
| [`data/tau.txt`](data/tau.txt) | the matrix of $\tau$ ($56 \times 56$), $\tau^2 = -5$ |
| [`data/R112_gram_LLL.txt`](data/R112_gram_LLL.txt) | an LLL-reduced Gram matrix of $R$ ($112 \times 112$) |

$L$, $g_1$, $g_2$ and $\tau$ were derived from the entry $L_{56,2}(M)$ of the *Catalogue of Lattices* [[NS]](#NS) (Gram matrix and generators of a subgroup of the automorphism group).

Convention: row vectors; a matrix $M$ acts by $x \mapsto xM$; isometries satisfy $M G M^{\mathrm{T}} = G$. In the basis $(x, x\tau)$, $(0, 2y)$ (before dividing by $\sqrt 2$), the Gram matrix of $R$ is

```math
\begin{pmatrix} 3G & \tau G \\ (\tau G)^{\mathrm{T}} & 2G \end{pmatrix} .
```

## 4. The argument in ten steps

This section explains, step by step, why we believe that $\min(R) = 10$.

A vector of $R$ is $z = \tfrac{1}{\sqrt 2}(x, v)$ with $x \in L$ and $v \equiv x\tau \pmod{2L}$, and

```math
\langle z, z \rangle = \tfrac12\bigl[\langle x, x \rangle + \langle v, v \rangle\bigr] .
```

We say that there is a *collision of type $(a, b)$* if some $x$ of norm $a$ has a vector $v$ of norm $b$ in the class $x\tau + 2L$.

| # | step | how it was checked | by whom |
|---|---|---|---|
| 1 | $R$ is even unimodular of dimension 112 | exact integer arithmetic ([`verify/01_basic.py`](verify/01_basic.py)) | both sessions |
| 2 | $\min(L) = 6$, so $L$ is extremal: $`15\,590\,400`$ vectors of norm 6 and $`36\,957\,286\,800`$ of norm 8 ([§2.1](#21-extremal-theta-series)) | exhaustive enumeration of vectors of norm $\le 4$: fpylll (two bases) and PARI `qfminim` (a third basis). Both use floating point internally | both sessions, different software |
| 3 | if $x = 0$ or $v = 0$ then $\langle z, z \rangle \ge 12$; since $R$ is even, $\langle x, x \rangle + \langle v, v \rangle \equiv 0 \pmod 4$. Hence a vector of norm $< 10$ comes from a collision of type $(6,6)$, $(6,10)$, $(10,6)$ or $(8,8)$ | by hand | re-derived by both |
| 4 | $\tau$ commutes with $\mathrm{SL}_2(29)$, so it suffices to test one $x$ from each $\mathrm{SL}_2(29)$-orbit | exact | both |
| 5 | the $`15\,590\,400`$ minimal vectors of $L$ form 656 $\mathrm{SL}_2(29)$-orbits, and our list of representatives is complete | orbit sizes sum to $`15\,590\,400`$; orbits pairwise disjoint; spherical design identities of degree 2, 4, 6 hold exactly on the list | both, different methods |
| 6 | no collision of type $(6,6)$ | exact (canonical forms of classes mod $2L$) | both, separate code |
| 7 | no collision of type $(6,10)$ or $(10,6)$ | an explicit integer certificate: for each of the 656 classes a vector $w_0$ of norm 14 or 18 in the class with $\lvert \langle w_0, u \rangle \rvert \le 6$ for all minimal vectors $u$ (this excludes vectors of norm $\le 10$ in the class). Since $\tau^2 \equiv 1 \pmod 2$, one direction suffices | produced by one session, re-verified by the other with separate code |
| 8 | the $`36\,957\,286\,800`$ vectors of norm 8 form $`1\,517\,130`$ $\mathrm{SL}_2(29)$-orbits, and our list is complete | orbit sizes sum to $`36\,957\,286\,800`$; design identities of degree 2, 4, 6 hold exactly | both, different methods |
| 9 | no collision of type $(8,8)$ | exhaustive over all $`1\,527\,984`$ (representative, unit) pairs; 0 collisions. The same test finds 10 colliding pairs (6 orbits, $`292\,320`$ vectors of norm 8) for the other $\tau$ | both, separate code, same idea (canonical forms). A third run that uses neither canonical forms nor the group (closest-vector computations) is **in progress** |
| 10 | hence no vector of norm $< 10$; vectors of norm 10 exist (found explicitly), so $\min(R) = 10$ | | |

In steps 8 and 9, a *unit* is an isometry of $L$ that commutes with $\mathrm{SL}_2(29)$; there are 12 of them (6 up to sign). The orbit representatives were computed for the larger group generated by $\mathrm{SL}_2(29)$ and the units ($`254\,664`$ orbits); since the units do not commute with $\tau$, every pair (representative, unit) has to be tested, which gives $254664 \times 6 = 1527984$ pairs.

The certificate in step 7 works as follows. If $w \ne \pm w_0$ lies in the same class as $w_0$, then $y_\pm = \tfrac12(w_0 \pm w) \in L \setminus \lbrace 0 \rbrace$, so $\langle w_0, w_0 \rangle + \langle w, w \rangle \pm 2\langle w_0, w \rangle \ge 24$. For $\langle w_0, w_0 \rangle \in \lbrace 14, 18 \rbrace$ and $\langle w, w \rangle \le 10$ this forces one of $y_\pm$ to be a minimal vector with $\langle w_0, y_\pm \rangle \ge 7$.

Consistency checks that are *not* part of the proof: the automorphisms of orders 3, 5, 7 have fixed lattices of dimension 32, 16, 16 with exact minima 12, 10, 14 and determinants $3^{32}$, $5^{16}$, $7^{16}$; their types 3-(40,32)-32, 5-(24,16)-16, 7-(16,16)-16 are among those not excluded for an extremal lattice of dimension 112 by Nebe-type density arguments [[Neb13b]](#Neb13b).

## 5. What could be wrong

We list what we consider the weakest points, most serious first.

1. **The structure of the argument itself.** Both checks were made by sessions of the same AI model. Different code does not protect against a shared conceptual mistake in steps 3–4 or in the logic of steps 6–9.
2. **Step 9.** The two exhaustive runs use the same idea. The third, conceptually different run is not finished.
3. **Step 2.** Both enumerations use floating-point pruning. There is no proof of $\min(L) = 6$ in exact arithmetic here (it should follow from the literature once $L$ is identified; see 5).
4. **No direct check on $R$.** Lattice reduction on the 112-dimensional lattice itself (BKZ up to block size 60) and fixed sublattices of group elements were tried, but they also fail to detect the norm-8 vectors of the *bad* $\tau$, so they are not evidence. Computing the minimum of a 112-dimensional lattice directly is out of reach for us.
5. **Identification and literature.** $L$ was produced inside Nebe's lattice $L_{56,2}(M)$ [[NS]](#NS); we have not confirmed which catalogued lattice it is isometric to. The construction is simple, and it is entirely possible that it has been examined before. We found nothing in a brief search.
6. **Not done:** counting the $`10\,888\,335\,360`$ vectors of norm 10 (a strong independent test); determining the full automorphism group; deciding whether the two lattices with minimum 8 obtained from the two base lattices are isometric.

## 6. How we got here (short version)

This came out of a hobby project aiming to understand, and possibly extend, the list in [§2.2](#22-previously-known-extremal-even-unimodular-lattices). A longer account, including the failures, is in [docs/history.md](docs/history.md).

- More than 190 candidate lattices in dimensions 96–112 (cyclotomic ideal lattices and their ideal-class twists, Hermitian tensor products, gluings 48 + 48) were tested first and recorded in a table; in every one of them a vector of norm $\le 8$ was found.
- A heuristic: the Siegel mean of the number of vectors of norm below the extremal bound, divided by the order of a group acting freely, estimates how many orbits of "too short" vectors a random symmetric lattice has. The Siegel mean is about $1.6 \times 10^7$ in dimension 96 but only $5.1 \times 10^4$ in dimension 112, comparable to $\lvert \mathrm{SL}_2(29) \rvert = 24360$. That is why dimension 112 and this group were tried.

  The Siegel mean $S(n)$ of the number of vectors that an extremal lattice of dimension $n$ must not have ([`verify/siegel_mean.py`](verify/siegel_mean.py)):

  | period | $n \equiv 0$ | $n \equiv 8$ | $n \equiv 16 \pmod{24}$ |
  |---|---|---|---|
  | 1 | 24: $95$ | 32: $4.5$ | 40: $0.08$ |
  | 2 | 48: $4.7 \times 10^3$ | 56: $275$ | 64: $9.1$ |
  | 3 | 72: $2.6 \times 10^5$ | 80: $1.7 \times 10^4$ | 88: $716$ |
  | 4 | 96: $1.6 \times 10^7$ | 104: $1.1 \times 10^6$ | **112: $5.1 \times 10^4$** |
  | 5 | 120: $9.7 \times 10^8$ | 128: $6.6 \times 10^7$ | 136: $3.5 \times 10^6$ |

  With $n = 2k$, the mean number of vectors of norm $2m$ is $\frac{2k}{\lvert B_k \rvert}\sigma_{k-1}(m)$ (Siegel), and $S(n)$ is the sum over $1 \le m \le \lfloor n/24 \rfloor$. Within a period of 24 the requirement becomes weaker by a factor of about 15–20 for every 8 dimensions, and jumps up when the bound increases. This matches part of the history: dimension 80 (1998) was reached before dimension 72 (2010), and dimension 64 (1984) before dimension 56 (1989). It is a rough guide only (dimension 88 came last in its period).
- All $\mathrm{SL}_2(29)$-equivariant gluings of two copies of Nebe's 56-dimensional lattices modulo 2 were enumerated (5 classes). Two die immediately; of the remaining three, two have exactly $`292\,320`$ vectors of norm 8, and one is the candidate.

## 7. Reproducing

Requirements: SageMath 10 or later (with PARI and fpylll). The computations were done with SageMath 10.9 from conda-forge; [`environment.yml`](environment.yml) recreates that environment. A [`Dockerfile`](Dockerfile) is included but has not been test-built.

```
sage -python verify/theta_series.py 56 112     # §2.1
sage -python verify/theta_series.py --table    # the table of §2.1
sage -python verify/01_basic.py                # step 1 and the facts of §1 (seconds)
```

**Not here yet** (to be added): standalone scripts for steps 2, 5–9 (they currently live in a private working repository and depend on its library), the certificate of step 7 and the orbit representatives as data files, and the witness vectors of norm 8 for the bad $\tau$.

## 8. Authorship and use of AI

- Direction, choice of problem, decisions, and responsibility for publication: roiban1344.
- Search strategy, code, computations, verification, and the drafting of this text: Claude (Anthropic), in several independent sessions.
- roiban1344 takes responsibility for the claims made here, and for any errors.

## License

Code (`verify/`) is released under the MIT License ([LICENSE](LICENSE)); text and data (`README*.md`, `docs/`, `data/`) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## References

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
