#import "paper.typ": *
#import "computations.typ": *
#let calc(..ids) = [\[#ids.pos().join(", ")\]]
#show: paper.with(
  lang: "en",
  title: [An extremal even unimodular lattice in dimension 112: supplement],
  authors: [roiban1344 #linebreak() #small[#link("https://github.com/roiban1344")[github.com/roiban1344]]],
  date: [Draft, 18 October 2026],
)

This supplement records search motivation, additional checks, running times and the support-module argument. Section, proposition, appendix and bibliography identifiers without an S prefix, and computation labels [C1]–[C27], refer to the main paper. Theorem A is proved in §§2–6 of that paper. Route T is incomplete: generation and full integer verification of the certificates for test (2) in §S4 remain unfinished. This supplement reports the completed checks without assuming that the outstanding work has been completed.

= S1. Siegel means and search motivation <supp-S1>

Write $Sigma(n)$ for the Siegel weighted mean number of nonzero vectors of norm below the extremal bound $mu(n)$. It is the sum of the corresponding Eisenstein-series coefficients below.

As a measure of how hard it is to find an extremal lattice we use the average over all even unimodular lattices. By Siegel's theorem this average is an explicit modular form (an Eisenstein series), so its coefficients can be computed exactly.

Up to isometry there are finitely many even unimodular lattices of dimension $n$ (they form a single genus). Weighting each lattice $Lambda$ by $1\/\|"Aut" Lambda\|$, Siegel's theorem (a special case of the Siegel–Weil formula) gives $ frac(sum_Lambda theta_Lambda\/\|"Aut" Lambda\|, sum_Lambda 1\/\|"Aut" Lambda\|) = E_(n\/2)\(q\)= 1 - frac(2 k, B_k) sum_(m gt.eq 1) sigma_(k - 1)\(m\)thin q^m #h(2em)\(k = n\/2\) $ \[Kin03, Thm. 18\]. Here $B_k$ is the Bernoulli number (negative for $k equiv 0 med mod med 4$) and $sigma_(k - 1)\(m\)$ the sum of the $\(k - 1\)$-th powers of the divisors of $m$. The coefficient of $q^m$ is the average number of vectors of norm $2 m$. The weight $1\/\|"Aut" Lambda\|$ can be read as the likelihood of obtaining $Lambda$ from a “random” construction (lattices with more symmetry are less likely).

The difference between the extremal theta series and $E_(n\/2)$ is a cusp form. Table S1 compares the coefficients in dimensions 56 and 112.

#ptable(
  columns: 5, align: (left, left, right, right, left,),
  caption: [Table S1. Numbers of vectors by norm: Siegel mean (coefficients of $E_(n\/2)$) versus the extremal theta series.],
  table.header([$n$], [norm], [typical lattice (Siegel mean)], [extremal lattice], [comment]),
  table.cell(colspan: 1, rowspan: 5)[56], [2], [$2 times 10^(- 6)$], [0], [inner shell],
  [4], [$275.3$], [0], [inner shell ($Sigma\(56\)approx 275$)],
  [6], [$15 thin 643 thin 264.9$], [$15 thin 590 thin 400$], [kissing number 0.3 % below the mean],
  [8], [$36 thin 955 thin 007 thin 141.0$], [$36 thin 957 thin 286 thin 800$], [],
  [10], [$15 thin 284 thin 232 thin 608 thin 011.0$], [$15 thin 284 thin 192 thin 071 thin 680$], [],
  table.cell(colspan: 1, rowspan: 6)[112], [2], [$4 times 10^(- 29)$], [0], [inner shell],
  [4], [$1.4 times 10^(- 12)$], [0], [inner shell],
  [6], [$0.0069$], [0], [inner shell],
  [8], [$51 thin 014.2$], [0], [inner shell; the main contribution],
  [10], [$10 thin 907 thin 925 thin 307.1$], [$10 thin 888 thin 335 thin 360$], [kissing number 0.18 % below the mean],
  [12], [$247 thin 007 thin 811 thin 617 thin 624$], [$247 thin 006 thin 775 thin 232 thin 000$], [],
)

The mean number of nonzero vectors of norm at most 6 in dimension 112 is about 0.007; the mean number of norm-8 vectors is about 51,000. Thus most of the mean count below the extremal bound comes from norm 8. These are weighted averages over lattices. §S1.1 explains how they were used to motivate the search without interpreting them as the distribution of lattices with a prescribed symmetry group.

By §S1, with $n = 2 k$ the average number of vectors of norm $2 m$ is $- frac(2 k, B_k) sigma_(k - 1)\(m\)$; $Sigma\(n\)$ is its sum over $1 lt.eq m lt.eq floor.l n\/24 floor.r$.

#ptable(
  columns: 4, align: (left, left, left, left,),
  caption: [Table S2. Siegel means $Sigma\(n\)$ of the number of inner-shell vectors (the Siegel sawtooth). Each row has a fixed extremal bound.],
  table.header([], [$n equiv 0 med\(mod med 24\)$], [$n equiv 8$], [$n equiv 16$]),
  [$mu = 4$], [24: $94.8$], [32: $4.51$], [40: $0.076$],
  [$mu = 6$], [48: $4 thin 651$], [56: $275$], [64: $9.09$],
  [$mu = 8$], [72: $262 thin 716$], [80: $16 thin 801$], [88: $716$],
  [$mu = 10$], [96: $15 thin 732 thin 086$], [104: $1 thin 046 thin 569$], [#strong[112: $51 thin 014$]],
  [$mu = 12$], [120: $9.73 times 10^8$], [128: $6.63 times 10^7$], [136: $3.51 times 10^6$],
)

Within a row, $Sigma\(n\)$ drops by a factor of 15–20 for every 8 dimensions. This is consistent with dimension 80 (1998) being settled before 72 (2010); dimension 88 came only in 2026, so this is a rough guide only.

#ptable(
  columns: 5, align: (left, center, left, right, right,),
  caption: [Table S3. Rounded Siegel means of the number of nonzero vectors below the extremal bound. The last column gives a rounded group-order scale for the illustrative benchmark $Sigma(n)/|G| <= 0.05$; this is not a criterion for extremality.],
  table.header([$n$], [$mu\(n\)$], [inner shells], [$Sigma\(n\)$], [$\|G\|$ for $lambda lt.eq 0.05$]),
  [72], [8], [norms 2–6], [$262 thin 716$], [$5 times 10^6$],
  [88], [8], [norms 2–6], [$716$], [$1 times 10^4$],
  [96], [10], [norms 2–8], [$15 thin 732 thin 086$], [$3 times 10^8$],
  [104], [10], [norms 2–8], [$1 thin 046 thin 569$], [$2 times 10^7$],
  [#strong[112]], [#strong[10]], [norms 2–8], [#strong[$51 thin 014$]], [#strong[$1 times 10^6$]],
  [120], [12], [norms 2–10], [$972 thin 746 thin 306$], [$2 times 10^10$],
)

== S1.1. Symmetry and the mean vector count

Let $Sigma(n)$ be the Siegel weighted mean defined in §S1. For a chosen finite symmetry group $G$, consider the ratio $lambda=Sigma(n)/|G|$. If the stabilizers of the relevant vectors are trivial, their orbits have size $|G|$. This suggests using the ratio to compare the scale of the mean vector count with an orbit size. The weighted mean over all even unimodular lattices does not, by itself, give the conditional mean over lattices carrying a specified group.

As a further modelling assumption, a Poisson number of orbits with mean $lambda$ would give the probability $e^(-lambda)$ for having no such orbit. With only the scalar symmetries $plus.minus 1$, the corresponding scale in dimension 112 is $e^(-Sigma(112)/2) approx e^(-25 thin 507)$. This model helped motivate the imposition of symmetry during the search; it is not a deduction about the actual distribution of lattices, and it estimates neither the correctness nor the running time of the proof.

#ptable(
  columns: 5, align: (left, right, right, right, left,),
  caption: [Table S4. The ratio $lambda=Sigma(n)/|G|$ for selected lattices. $\|G\|$ is the order of the automorphism group (for gluings A, B: of the visible subgroup; for $L_112$: Theorem B, §8).],
  table.header([lattice], [$Sigma\(n\)$], [$\|G\|$], [$lambda$], [how it was found]),
  [$P_(48 n)$], [$4 thin 651$], [$524 thin 160$], [$0.009$], [from a group],
  [$P_(48 p)$], [$4 thin 651$], [$145 thin 728$], [$0.03$], [from a code],
  [$P_(48 q)$], [$4 thin 651$], [$103 thin 776$], [$0.04$], [from a code],
  [$P_(48 m)$], [$4 thin 651$], [$1 thin 200$], [$3.9$], [exhaustive classification],
  [$Gamma_72$], [$262 thin 716$], [$5 thin 241 thin 600$], [$0.05$], [test of all 9 structures],
  [$L_80$ (Bachoc–Nebe)], [$16 thin 801$], [$4.5 times 10^9$], [$4 times 10^(- 6)$], [from a group],
  [gluings A, B (min 8)], [$51 thin 014$], [$292 thin 320$], [$0.17$], [§3],
  [#strong[gluing C $= L_112$]], [$51 thin 014$], [$1 thin 169 thin 280$], [#strong[$0.044$]], [this paper],
  [($L_112$, counting $"SL"_2\(29\)$ only)], [$51 thin 014$], [$24 thin 360$], [$2.1$], [],
)

Group orders are taken from \[NS\], with $Gamma_72$ from \[Neb12\]. The last two rows illustrate that the numerical ratio changes substantially depending on whether one counts only the imposed group or the full automorphism group determined later. The proof uses the imposed group and does not require a small value of this ratio.


= S2. Expected collisions in a random gluing <supp-S2>

If $f$ were a random parity-preserving map, the class $x f$ of $x in L_56(a)$ would be uniformly distributed among classes of the same parity. Since each class contains at most one pair $plus.minus v$ of norm $b$ (a consequence of §5), the expected number of inner-shell vectors of $L_112$ coming from type $\(a\,b\)$ is $ bb(E)  [ \#\(a\,b\) ]  approx frac(\|L_56(a)\|thin\|L_56(b)\|, N_plus.minus)\,#h(2em) N_(-) = 2^55 - 2^27 med\(upright("odd classes")\)\,quad N_(+) = 2^55 + 2^27 med\(upright("even classes")\) $ (computation in §S2.1). This estimate is a heuristic and is not used in the proof.

#ptable(
  columns: 5, align: (left, right, right, right, right,),
  caption: [Table S5. Expected numbers for a random gluing (from the theta series of $L_56$) and the actual values for gluings A, B, C.],
  table.header([type], [expected], [share], [gluings A, B], [gluing C]),
  [$\(6\,6\)$], [$0.007$], [—], [0], [0],
  [$\(6\,10\)$ and $\(10\,6\)$], [$13 thin 228$], [26 %], [0], [0],
  [$\(8\,8\)$], [$37 thin 910$], [74 %], [$292 thin 320$], [0],
  [total], [$51 thin 137$], [], [$292 thin 320$], [0],
)

The total agrees with the Siegel mean $Sigma\(112\)= 51 thin 014$ within $0.2 thin %$. Counting both inputs and partners modulo sign gives the probability scale $(6 thin 614/4)/(15 thin 590 thin 400/2) approx 1/4 thin 714$. Exhaustive tests are required.

== S2.1. Calculation of the expectations

Type $\(6\,10\)$: $\|L_56(6)\|\|L_56(10)\|\/N_(-) = 15 thin 590 thin 400 times 15 thin 284 thin 192 thin 071 thin 680\/\(2^55 - 2^27\)approx 6 thin 614$; type $\(10\,6\)$ gives the same, together $13 thin 228$. Type $\(8\,8\)$: $\|L_56(8)\|^2\/N_(+) approx 37 thin 910$. Type $\(6\,6\)$: $\|L_56(6)\|^2\/N_(-) approx 0.0067$. All under the assumption that the class $x f$ is uniformly distributed among classes of the same parity.


= S3. Reproduction and additional checks <supp-S3>

== S3.1. Running times

#ptable(
  columns: 3, align: (left, left, left,),
  caption: [Table S6. Main computations (single core unless stated).],
  table.header([step], [method], [cost]),
  [F1], [interval enumeration, norm $lt.eq 4$, BKZ-40 basis], [34 min ($8.5 times 10^9$ nodes); floating-point enumerations 51 min – 2.3 h],
  [F2], [closure + orbits], [about 13 min (finding 10 min, checking 3 min)],
  [F3], [marked sums of two minimal vectors], [about 1.2 h (checking 9 min)],
  [F5a], [odd-class certificates (656)], [finding 4 min, checking 2 min],
  [F5b], [canonical forms (two implementations)], [24 min – about 2 h],
  [F5b], [CVP, radius² 2.05], [4 × 9 h],
  [F5b], [even-class certificates], [finding 6 × about 31 h (shared machine); checking 7.9 h on 3 threads],
)



The computations were run with Python 3.12.15, NumPy 2.5.4, SageMath 10.9, fplll 5.5.0 (fpylll 0.6.4), PARI/GP 2.17.3 and GAP 4.15.1 \[Soft\]. Recorded checks in a second environment used Debian 13.7, Python 3.13.5, NumPy 2.5.4 and gcc 14.2. The times above include the load at the time of measurement; each verification program records its Python, NumPy and OS versions and running time in JSON. The Lean version is 4.34.1, with mathlib pinned to revision #raw("d13f23b723b8a846827a245b89c10fc7d3f11612").

== S3.2. Verification routes

A re-checker needs only F0 ($L_112$ is even unimodular) and F1–F5; the search (failed constructions, classification of gluings, choice of $tau$) is not needed. Each of F0–F5 can be checked in several ways, and the combination determines which criteria and programs are used and how long it takes. We do not designate one route as official; Table S7 lists them. The inputs and criteria for each route are listed below.

#strong[Baseline.] Enumerating all vectors of norm $lt.eq 8$ of $L_112$ itself (dimension 112) would need about $10^25$ enumeration nodes by the Gaussian volume estimate ($5.3 times 10^25$ with an LLL basis, $4.1 times 10^24$ with a BKZ-30 basis) #calc("C16"); at $10^7$ nodes per second that is $10^18$ seconds — infeasible.

#ptable(
  columns: 4, align: (left, left, left, left,),
  caption: [Table S7. Verification routes. \[m\] measured; \[e\] estimated from measured per-operation costs.],
  table.header([route], [content], [criteria and programs used], [total]),
  [A (fastest)], [F1 by interval enumeration (34 min \[m\]); F2, F3 by orbit sizes and distinct canonical forms (3 min and 9 min \[m\]); F5a by odd-class certificates (2 min \[m\]); F5b by canonical-form look-up (24 min \[m\])], [the interval enumerator, the canonical-form code, Proposition 6.3], [about 1.2 CPU hours \[m\]],
  [B (no canonical forms in the decision)], [as A, with F5b by checking the distributed even-class certificates (7.9 h on 3 threads \[m\]); finding them again would take 763,992 pairs (using the frame-preserving symmetry #calc("C14")) × 0.7 s \[m\]], [the interval enumerator, the midpoint lemma], [about 25 CPU hours to check \[m\]; about 150 to find again \[e\]],
  [C (closest vectors)], [as A, with F5b by closest-vector enumeration], [pruning in the enumeration (not a proof if floating point)], [about 40 CPU hours \[m\]],
  [D (from scratch)], [rebuild the orbit lists from the four data files only (the approach of implementation 3)], [one's own code only], [A–C plus 2–3 hours \[e\]],
  [S (#calc("C15"), sampling; #strong[not a proof])], [re-check $k$ random certificates with code independent of the producer (group rebuilt from the generators, the distributed $tau$, 64-bit integers only)], [—], [$k = 200 + 200$ in 8 min \[m\]; #strong[all 400 pass]],
  [T (support modules)], [classify the rank-2 support modules that could carry a vector of norm $<= 8$ (97 invariant types, 63 dangerous) and exclude them by three closest-vector searches modulo 2 (§S4.1)], [Coulangeon's inequality; the classification (two independent enumerations agree); the searches (floating point; integer certificates and full verification remain incomplete)], [classification 1 min; searches 1.6 h + 3 × 13 h + F5b \[m\]],
)

Route S is a limited consistency check on the supplied tables: if a fraction $p$ of entries were wrong, a sample of $k = 200$ would detect it with probability $1 -\(1 - p\)^200$, which is 0.87 for $p = 10^(- 2)$ but only 0.001 for $p = 6.5 times 10^(- 6)$ (the rate of collisions in gluing B). Route T uses the Hermitian structure of $L_112 = H times.o P$ for the rank-2 case and the argument of §S4.2 for dependent components. It shares the norm-8 exclusion with the main proof. The extent to which the closest-vector searches have been replaced by checked representatives is stated in §S4.1. The Lean formalisation in §7.1 covers the common deduction from the computational statements to the main conclusion, not the support-module enumeration.

#strong[Search and verification.] Table S6 gives the measured costs of producing and checking each finite data set. A lower-bound verification must check the complete orbit lists and all relevant classes; a counterexample, in contrast, is verified by checking the membership and norm of one supplied vector.

== S3.3. Recomputation by separately written implementations

Implementation 1 constructed $L_112$ and performed the main computations. Implementation 2, sharing only data files (Gram matrices, generators, $tau$, orbit representatives), re-implemented every step: even unimodularity and the group action on the 112-dimensional Gram matrix, the minimum of $L_56$ with different software and basis, disjointness and design identities for the orbit lists, the canonical-form test, the check of the certificates, and a sample of 180 classes by exhaustive enumeration in the lattice $chevron.l 2 L_56\,t chevron.r$ with PARI. Implementation 3 used only the four data files of Appendix D and wrote all of its code from scratch (PARI/GP, fplll, GAP, C). It reproduced the orbit counts with the same completeness proof, found no collision of any type for $L_112$, found exactly 6 colliding orbits ($292 thin 320$ vectors of norm 8) for the other class of $tau$, and reproduced the 112-dimensional Gram matrix as PARI's #raw("qflllgram") of (3.1). Its enumerations also prune in floating point.

== S3.4. Changes of frame

Write $L_112 = L_56 times.o_(M') Lambda$ with $Lambda = {\(a\,b\)in M' ""^2 : b equiv a tau med mod med 2 M' }\/sqrt(2)$, a Hermitian $M'$-lattice of real dimension 16. A #strong[frame] is a pair $\(w_1\,w_2\)$ of orthogonal elements of $Lambda$ of Hermitian norm 2. Each frame exhibits $L_112 supset L_56 w_1 perp L_56 w_2 tilde.equiv sqrt(2) L_56 perp sqrt(2) L_56$ and thus $L_112$ as a gluing $L_phi$; the class of $phi$ in Proposition 3.3(c) determines the minimum, so it must be the same for all frames. $Lambda$ has 72 elements of norm 2 and 864 frames. For $tau$ of class C all 864 frames give class C, and for class B all give class B #calc("C17"). This test is inexpensive and independent of the collision computations.

== S3.5. Fixed sublattices and BKZ

Elements of order 3, 5, 7 of $"SL"_2\(29\)$ have fixed sublattices of $L_112$ of dimension 32, 16, 16 with exact minima 12, 10, 14 (determinants $3^32\,5^16\,7^16$) #calc("C18"). The order-5 section contains explicit vectors of norm 10, so $min L_112 lt.eq 10$. These types are among those not excluded for extremal lattices of dimension 112 by \[Neb13\]. These fixed sublattices do not establish a lower bound for the minimum of the whole lattice: gluing B has the same fixed-sublattice minima while its own minimum is 8. Likewise BKZ reduction of $L_112$ with block size up to 60 finds no vector below norm 12, but also fails to detect a norm-8 vector in B.

== S3.6. Controls and closest-vector searches

Every exhaustive test above was also run on the negative controls with known answers (Table 6). In particular the tests detect #emph[rare] collisions: 10 out of $1 thin 527 thin 984$ pairs for B. The CVP test was cross-checked against the canonical-form test on all colliding pairs and on a sample of 150 pairs.

#strong[CVP.] The class $t + 2 L_56$ ($t = x_i u tau$) contains a vector of norm $lt.eq 8$ iff some $y in L_56$ satisfies $chevron.l y + t\/2\,y + t\/2 chevron.r lt.eq 2$, a closest-vector problem in $L_56$ with target $- t\/2$. We ran fplll's enumeration at squared radius $2.05$ for all $1 thin 527 thin 984$ pairs (four jobs of about 9 hours, without canonical forms or $K_8$): #strong[0 collisions] #calc("C12"). The same enumeration found the norm-8 partner in every one of the 46 colliding pairs of gluings A and B. The radius may be shrunk because a norm-8 element corresponds to squared distance exactly 2, and the next possible norm, 12, to 3.

== S3.7. Scope of the checks

#ptable(
  columns: 2, align: (left, left,),
  caption: [Table S8. Possible errors and the checks that would detect them.],
  table.header([possible error], [would be detected by]),
  [Orbit lists incomplete (shared by all $\(8\,8\)$ tests)], [orbit-size sums (exact); recount from $K_8$; design identities of degree 2, 4, 6; implementation 3 from scratch],
  [The canonical-form criterion is wrong], [Proposition 6.3 (proof); CVP test without canonical forms; even-class certificates for all pairs; support-module route (§S4.1)],
  [A gap in the logic (missing type, case $x = 0$, wrong direction)], [written proofs (§§3–5); three implementations re-deriving the reduction; tests in both directions $tau\,tau^(- 1)$; #strong[formalisation in Lean (§7.1)]],
  [The 112-dimensional Gram matrix is not the lattice described], [two implementations rebuilt (3.1) independently; the third reproduced the LLL-reduced matrix exactly; frame test],
  [$min L_56 < 6$], [#strong[rigorous interval enumeration]; reduction to $L_(56\,2)\(M\)$; three floating-point enumerations; exact agreement of shell sizes and design identities (indirect)],
  [Assignment of minima to classes inconsistent], [frame-change test (864 frames)],
  [The tests are blind to rare collisions], [negative controls A, B (10 in 1.5 million detected)],
  [An error in a shared computational hypothesis], [the corresponding input, completeness and arithmetic checks in §§6–7; Lean checks the deduction from these hypotheses, not their computational verification (§7.1)],
)


= S4. Support modules (route T) <supp-S4>

== S4.1. Rank-two support modules

Gluings B and C use the same base lattice and differ only in the choice of $tau$. For a vector $z = e_1 times.o x + e_2 times.o y$ of $H times.o P$ define its #strong[support module] $N_z = cal(O) x + cal(O) y subset P$. In this section we use the trace-normalised Hermitian form $k_P = h_P \/ 2$, for which $chevron.l x\,x chevron.r = "Tr"_(K\/bb(Q)) k_P\(x\,x\) = 2 k_P\(x\,x\)$, and $k_R = h_H times.o k_P$; determinants $det_k$ of support modules and Table S9 refer to $k_P$. Coulangeon's inequality for tensors of rank 2 gives $k_R\(z\,z\)gt.eq 2 sqrt(det h_H dot.op det_k N_z)$ \[Cou00, CN13\], so a vector of norm 8 ($k_R\(z\,z\) = 4$) needs $det_k N_z lt.eq 4$. For 20 symmetry-inequivalent norm-8 vectors of B the support modules are of two kinds, both saturated and both free of minimal vectors (Table S9) #calc("C19").

#ptable(
  columns: 4, align: (left, left, left, right,),
  caption: [Table S9. Support modules of the norm-8 vectors of gluing B.],
  table.header([type], [reduced Gram matrix of $k_P$], [$det_k$], [count (of 20)]),
  [I], [$mat(delim: "(", 4, - 2 sqrt(- 5); 2 sqrt(- 5), 6) = 2 H^(- 1)$], [4 (equality)], [12],
  [II], [$mat(delim: "(", 4, 9 / 5 sqrt(- 5); - 9 / 5 sqrt(- 5), 5)$], [19/5], [8],
)

These matrices describe the form in a $K$-basis of the support, rather than an integral $cal(O)$-basis. In particular the rational entries for type II do not specify the integral module structure, which is retained separately.


Type I is exactly twice the inverse of $H$, the configuration in which Coulangeon's bound is attained. This parallels the “Barnes-free” criterion for $Gamma_72$ in \[CN13\].

#strong[Complete classification (route T).] Let $z in L_112$ have norm $<= 8$. If $x, y$ are independent over $K$, put $N_0 = cal(O) x + cal(O) y$ and let $N = P inter (K x + K y)$ be its saturation. Since $H$ is free, $z in H times.o N_0 subset H times.o N$. Coulangeon's inequality $k_R(z, z) >= 2 sqrt(det h_H dot.op det_k N_0)$ \[Cou00, Lemma 3.3 and Prop. 3.2\] gives $det_k N_0 <= 4$, and $det_k N = det_k N_0 \/ [N : N_0] <= 4$ (for Hermitian lattices the index enters to the first power; for non-free $N$ the determinant is taken with respect to a pseudo-basis, including the norm of the coefficient ideal). So $N$ is a saturated rank-2 submodule of $P$ with real minimum $>= 6$ and $det_k N <= 4$. If $x, y$ are dependent over $K$, a vector of norm $<= 8$ is a collision of type $(6,6)$ or $(8,8)$ (§S4.2), detected by the searches (3) and (1) below. Because $cal(O) = ZZ[sqrt(-5)]$ has class number 2, $N$ need not be free. All such $N$ were enumerated, free and non-free, as Hermitian $cal(O)$-lattices with even integral trace form, and grouped by invariants (determinant, theta coefficients up to norm 16, minimum and numbers of short vectors of $H times.o N$): #strong[97 invariant types, 63 of them dangerous] ($H times.o N$ has a vector of norm $< 10$; 30 with minimum 6 and 33 with minimum 8). The grouping is by invariants, not by isometry, and the exclusion below was checked on every enumerated candidate, not only on one per type, so isometry classes are not needed. A second, independent enumeration (from a pseudo-basis through the true shortest vector, with exact rational Fincke–Pohst; the first starts from a basis-extendable shortest vector) uses a coarser invariant; regrouping both enumerations by that same invariant gives 58 dangerous types in each, with agreement at this coarser level #calc("C20"). Every dangerous candidate contains a configuration that one of three closest-vector searches modulo 2 must detect: (1) a norm-8 vector $x$ and a norm-8 element of the class $x tau + 2 L_56$ (this is the $(8, 8)$ test of §6); (2) a norm-8 $x$ and an element of norm $<= 8$ (zero included) of $x(1 + tau) + 2 L_56$; (3) a norm-6 $u$ and an element of norm $<= 10$ of $u mu + 2 L_56$, $mu in {1, tau, 1 + tau}$. For $L_112$, test (1) is F5b. Test (2) enumerated $763 thin 992$ pairs in floating point without finding an element of norm at most 8 #calc("C21"). Generation and full integer verification of representatives for these pairs await completion. For (3), the inputs are the 656 norm-6 $S$-orbit representatives times three centralizer representatives after reduction by the symmetry preserving $tau$: $656 times 3=1 thin 968$ input vectors $u$. Each is tested with $mu in {1,tau,1+tau}$. For $mu=1$, $plus.minus u$ already belongs to the coset, and only elements independent of $u$ over $K$ are relevant. For the other two maps, all $1 thin 968 times 2=3 thin 936$ supplied representatives have been checked in integer arithmetic. They exclude norms at most 10 for $mu=tau$, and at most 8 for $mu=1+tau$. The latter cosets are even, so norm 10 is excluded by parity as well #calc("C21"). The enumeration found no dangerous independent configuration.

Completing this as a rigorous alternative route requires generation and full integer verification of every representative in (2), and a completeness check of the support-module parameter ranges and the reduction to the three searches. Theorem A does not use this route and is proved in §4.3 of the main paper. The collisions of gluing B were detected as controls.

== S4.2. Dependent components

Let $z = 1 / sqrt(2)\(x\, v\) in L_112$ with $v = x tau + 2 y$, and let $K = bb(Q)\(sqrt(-5)\)$ act on $L_56 times.o bb(Q)$ by $sqrt(-5) mapsto tau$. Suppose $y in K x$ and $chevron.l z\, z chevron.r <= 8$. By the proof of Lemma 4.2, $x eq.not 0$ and $v eq.not 0$, and $(n, m) = (chevron.l x\,x chevron.r, chevron.l v\,v chevron.r) in {(6,6), (6,10), (10,6), (8,8)}$. We show $m = n in {6, 8}$, i.e. $z$ gives a collision of type $(6,6)$ or $(8,8)$ with $v = lambda x$, $N(lambda) = 1$. (The claim that such a $z$ has norm $>= 12$ is false in general: for a gluing along an element of the centralizer, $v = x u$ gives the forced collisions of §3.2.)

Since $chevron.l x\, x tau chevron.r = 0$ and $chevron.l x tau\, x tau chevron.r = 5 n$, the map $lambda mapsto lambda x$ identifies $K$ with $K x$ and carries the norm form to $n N(lambda)$. The lattice $Lambda = L_56 inter K x$ is a rank-1 $cal(O)$-module, $Lambda = frak(a) x$ for a fractional ideal $frak(a) supset cal(O)$; put $k = [frak(a) : cal(O)]$. As a $ZZ$-lattice of rank 2, $Lambda$ is even with minimum $>= 6$ (F1) and determinant $5 n^2 \/ k^2$; Hermite's bound in dimension 2 gives $det Lambda >= 3 dot 36 \/ 4 = 27$, so $k <= 2, 3, 4$ for $n = 6, 8, 10$. The integral ideals of $cal(O)$ of norm $<= 4$ are $cal(O)$, $frak(p)_2 = (2, 1 + sqrt(-5))$, the two primes $frak(p)_3, frak(p)'_3 = (3, 1 plus.minus sqrt(-5))$ and $frak(p)_2^2 = (2)$, so $frak(a) in {cal(O), frak(p)_2^(-1), frak(p)_3^(-1), frak(p)'_3^(-1), 1/2 cal(O)}$. Write $v = lambda x$; then $lambda in sqrt(-5) + 2 frak(a)$ (because $y in Lambda$) and $N(lambda) = m \/ n in {1, 5\/3, 3\/5}$.
#linebreak() • $frak(a) = cal(O)$: $lambda = 2 p + (1 + 2 q) sqrt(-5)$ with $p, q in ZZ$, so $N(lambda) >= 5$. Impossible.
#linebreak() • $frak(a) = 1/2 cal(O)$ (only $n = 10$): $1\/2 in frak(a)$ would give a vector of norm $n \/ 4$, not an even integer. Impossible.
#linebreak() • $frak(a) = frak(p)_2^(-1)$: $2 frak(a) = frak(p)_2$ and $sqrt(-5) + frak(p)_2 = cal(O) without frak(p)_2$, whose norms are odd integers. Hence $N(lambda) = 1$ and $m = n$.
#linebreak() • $frak(a) = frak(p)_3^(-1)$ or $frak(p)'_3^(-1)$ ($n in {8, 10}$): $N(lambda) in N(frak(a)) ZZ = 1/3 ZZ$ excludes $3 \/ 5$, so $N(lambda) = 1$ and $(n, m) = (8, 8)$.
#linebreak() Such collisions are excluded by F5; on route T they are detected by the searches (3) and (1) of §S4.1.


= S5. Constructions considered in the search <supp-S5>

#strong[Before dimension 112.] More than 190 candidate lattices in dimensions 96–112 (cyclotomic ideal lattices and their ideal-class twists, Hermitian tensor products over imaginary quadratic fields, gluings $48 + 48$ and $48 times 2$) were tested first; every one had inner-shell vectors. In dimension 96 the ratio $lambda$ of the available symmetry groups was $gt.eq 300$; in hindsight this is consistent with these failures, and it motivated the search for constructions with larger symmetry.

#strong[The first four gluings in 112] came from Hermitian tensor products $T times.o L_(56\,2)\(M\)$ over imaginary quadratic fields ($bb(Q)\(sqrt(- 11)\)$: one class; $bb(Q)\(sqrt(- 2)\)$: three classes); all have forced collisions of type $\(6\,6\)$. Generalising these collisions gives the classification of Proposition 3.3.

#strong[Gluings A and B.] Both have exactly 6 colliding $S$-orbits of type $\(8\,8\)$, giving $292 thin 320$ vectors of norm 8, which equals the order of the explicitly constructed automorphism subgroup. They have the same distribution of inner products among norm-8 vectors, but whether A and B are isometric remains undetermined.

#strong[Base lattices.] $L_(56\,2)\(M\)$ is taken from the catalogue entry #raw("L_56b"). The second base lattice was obtained inside it: for each singular $X in M\/2 M$ of rank 28, $L_X = L_(56\,2)\(M\)X + 2 L_(56\,2)\(M\)$ with the form halved is $"SL"_2\(29\)$-invariant; five are even unimodular, one with centralizer of order 24 and four with order 12. Our $L_56$ is one of the latter. The catalogue entry #raw("L_56c") ($= L_(56\,2)\(tilde(M)\)$) lists generators of a subgroup of order $2^3 dot.op 3 dot.op 7 dot.op 29$ only and states that the automorphism group contains $"SL"_2\(29\)compose tilde(S)_3$, which is consistent with a centralizer of order 12.
