#import "paper.typ": *
#import "computations.typ": *
#import "figures/proof-dependencies.typ": proof-dependencies
#show: paper.with(
  lang: "en",
  title: [An extremal even unimodular lattice in dimension 112],
  subtitle: [Gluing with $"SL"_2(29)$ symmetry and a computer-assisted proof],
  authors: [roiban1344 #linebreak() #small[#link("https://github.com/roiban1344")[github.com/roiban1344]]],
  date: [Draft, 18 October 2026],
)

#abstract-box[
We construct an explicit positive-definite even unimodular lattice $L_112$ of dimension 112 and minimum norm 10, attaining the extremal bound. The construction glues two copies of a 56-dimensional extremal lattice of Nebe using an endomorphism whose square is $-5$ and which commutes with $"SL"_2(29)$. Extremality is reduced to finitely many coset bounds and proved by checking orbit completeness and either canonical forms or integer conditions derived from the midpoint lemma. We also determine the full automorphism group, of order $1 thin 169 thin 280$. Defining matrices, verification data and code are supplied, and the deduction from explicit computational hypotheses is formalized in Lean.
]


= 1. Introduction <s1>

== 1.1 Extremal even unimodular lattices

A positive-definite lattice of rank $n$ is a discrete subgroup $Lambda = bb(Z) b_1 xor dots.h xor bb(Z) b_n$ spanning Euclidean space $bb(R)^n$. We write $chevron.l x,y chevron.r$ for the inner product and call $chevron.l x,x chevron.r$ the norm of $x$. The lattice is even if every norm is an even integer. An integral lattice is unimodular if its Gram matrix has determinant 1, or equivalently if it equals its dual. Even unimodular lattices exist only in dimensions divisible by 8, and an example exists in every such positive dimension \[SPLAG, Ch. 7\].

The theta series $theta_Lambda(q)=sum_(x in Lambda)q^(chevron.l x,x chevron.r\/2)$ of an even unimodular lattice is a modular form of weight $n/2$. This gives the bound of Mallows–Odlyzko–Sloane \[MOS75\]:
#tagged("1.1", $ min Lambda <= mu(n):=2 floor(n/24)+2. $)
Here $min Lambda$ is the smallest norm of a nonzero vector. An even unimodular lattice is extremal when equality holds in (1.1). Unless another class of lattices is explicitly specified, “extremal lattice” in this paper means extremal even unimodular lattice. We write $mu(n)$ for this bound.

The bound is 6 in dimension 56 and 10 in dimension 112. Thus the construction below must exclude nonzero vectors of norms 2, 4, 6 and 8 in dimension 112. Examples in lower dimensions include $E_8$ and the Leech lattice. More recently, Sakamoto's preprint \[Sak26\] constructs two examples in dimension 88. Further background and comparison tables are collected in Appendix G; the proof of the result below does not depend on those comparisons.

== 1.2 Construction and main result

Let $L_56$ denote the 56-dimensional lattice whose Gram matrix is the file #raw("L56_gram.txt") listed in Appendix D. (The defining matrices are not printed in this paper; they are distributed as data files identified by their SHA-256 hashes. Appendix D also records a specification of $L_56$ and $tau$ in terms of Nebe's construction that does not depend on the files.) The lattice $L_56$ is $"SL"_2(29)$-equivariantly isometric to Nebe's lattice $L_(56,2)(tilde(M))$ \[Neb98, Table II\]; the identification is established in §7.2. The two matrices in the file #raw("sl2_29_generators.txt") are isometries of $L_56$ and generate a group $S$ isomorphic to $"SL"_2(29)$ (F4). Let $tau$ be the endomorphism given by the file #raw("tau.txt"). It commutes with $S$ and satisfies
$ tau^2=-5 "id", quad chevron.l x tau,y tau chevron.r=5 chevron.l x,y chevron.r quad (x,y in L_56). $
Matrices act on row vectors on the right. These identities and the defining matrices are checked by #calc("C2"). For this choice of $tau$, set
#tagged("1.2", $ L_112 = L_tau := { lr((x,x tau+2 y))/sqrt(2) : x,y in L_56 } subset 1/sqrt(2) (L_56 perp L_56). $)

#thm[
#strong[Theorem A.] The lattice $L_112$ defined by the data files of Appendix D and (1.2) is an even unimodular lattice of dimension 112 with minimum norm 10. In particular, it is extremal.
]

The diagonal action of $S$ preserves $L_112$. The proof of Theorem A is outlined in §1.3 and completed in §4.3 using the finite computations in §6. The construction and the verification are given separately, so the verification does not require repeating the search that led to $tau$.

The choice of $tau$ is not unique. The centralizer $C$ of $S$ in $"Aut"(L_56)$ has order 12, and exactly 24 endomorphisms of $L_56$ commute with $S$ and satisfy $tau^2=-5$ #calc("C2"). Only the reduction of $tau$ modulo $2 L_56$ enters the glued lattice. Proposition 3.3 classifies these reductions into three classes of gluing maps; the 24 endomorphisms reduce into two of them, called B and C below, 12 into each #calc("C2"), and endomorphisms in the same class give isometric glued lattices. The supplied $tau$ lies in class C, which gives $L_112$. Class B gives an even unimodular lattice with minimum norm 8 and exactly $292 thin 320$ vectors of norm 8 #calc("C4"). This second lattice serves as a positive control: the verification programs must detect its short vectors. The classification of the gluings is completed in §3.3.

Two further conclusions are treated separately from the extremality proof. The extremal theta series determines that $L_112$ has $10 thin 888 thin 335 thin 360$ vectors of norm 10 and $247 thin 006 thin 775 thin 232 thin 000$ vectors of norm 12 (Appendix B). Its full automorphism group has order $1 thin 169 thin 280$ (Theorem B, §8 and Appendix F). Theorem A does not use the determination of this full group.

== 1.3 Outline of the proof and the verification methods

We first verify that the lattice in (1.2) is even unimodular (Lemma 3.2). The main remaining task is to prove that it has no nonzero vector of norm below 10. The minimum norm of $L_56$ is 6, as reported in \[Neb98\]; we do not rely on that value but check it directly from the data file by two rigorous enumerations, one using interval arithmetic and one using an integer quadratic form (§6.1). Consequently, a nonzero vector $lr((x,v))/sqrt(2)$ of norm below 10 in $L_112$ would have both components in $L_56$ and would satisfy
$ v equiv x tau med (mod 2 L_56), quad (chevron.l x,x chevron.r, chevron.l v,v chevron.r) in {(6,6),(6,10),(10,6),(8,8)}. $
Lemma 4.2 shows that this list is exhaustive and that neither component is zero. Since $tau^2 equiv 1 med (mod 2)$, interchanging the two components reduces the type $(10,6)$ to $(6,10)$ (Appendix C.4). It therefore suffices to establish the following two bounds:
$ min(r tau+2 L_56)>=14 quad "for all" r in L_56(6), $
$ min(x tau+2 L_56)>=12 quad "for all" x in L_56(8), $
where $L_56(m)$ denotes the vectors of norm $m$ in $L_56$ and the minimum of a coset is taken over all its vectors. This is Corollary 4.3.

Because the group $S$ preserves norms and commutes with $tau$, each bound need only be checked on a collection of orbit representatives. For norm 6 there are 656 orbits. For norm 8 the supplied collections give $1 thin 527 thin 984$ test vectors of $L_56$, with repetitions, covering $1 thin 517 thin 130$ distinct orbits. These are vectors of the 56-dimensional lattice, not norm-8 vectors of $L_112$. The completeness check verifies the norms, disjointness and orbit sizes, and compares the total sizes with the shell sizes determined by the theta series (§§6.2–6.4).

The lower bounds are then verified as follows. For each norm-6 representative, we supply a vector in its prescribed coset whose norm and inner products with all minimal vectors of $L_56$ imply the bound 14. The implication follows from the midpoint lemma and Corollary 5.2; the supplied vector and its conditions are checked in §6.6. For the norm-8 test vectors, there are two alternatives. One uses canonical forms to test whether the prescribed coset contains a norm-8 vector (§6.5). The other checks coset representatives whose norm and inner products imply the bound 12 (Corollary 5.3 and §6.7). Either alternative, together with the common norm-6 bounds and completeness checks, proves the required absence of short vectors. The upper bound (1.1) then gives $min L_112=10$.

Thus the two even-coset tests are alternative ways of completing the same proof, and their shared inputs are part of the verification. Separately written implementations check these inputs and computations. Spherical-design identities, changes of frame and tests on the second gluing provide further consistency checks. Floating-point closest-vector searches and random samples are also reported, but are not substituted for the rigorous checks in the proof. Supplement §S4 describes a further route through support modules. It replaces the reduction of §4 by Coulangeon's inequality and an enumeration of support modules, but it is not independent of the proof, since its last step uses the same computations F5a and F5b (together with a further finite check, Supplement [C32]). The Lean formalization checks the deduction from the stated computational hypotheses (§7.1).


== 1.4 Relation to previous constructions and the choice of dimension

The construction uses established ingredients: Nebe's 56-dimensional lattices \[Neb98\], gluing along cosets modulo twice a lattice \[Que84\], and the Hermitian tensor-product framework used in dimensions 72 and 88 \[Neb12, CN13, Sak26\]. Proposition 3.4 identifies (1.2) with a Hermitian tensor product over $bb(Z)[sqrt(-5)]$. The result of this paper is the extremality of the lattice obtained with the supplied endomorphism, together with the explicit data and verification needed to establish it.

The choice of dimension 112 was motivated by comparison with dimensions 96 and 104, where the extremal bound is also 10. The Siegel weighted mean of the number of nonzero vectors of norm below 10 is approximately $15 thin 732 thin 086$, $1 thin 046 thin 569$ and $51 thin 014$ in these three dimensions, respectively #calc("C1"). The smaller mean in dimension 112 suggested a useful direction for the search. These are averages over a genus, not estimates of the time needed to prove extremality. The available $"SL"_2(29)$ action on $L_56$ also supplies the symmetry used to reduce the verification to orbit representatives. Supplement §S1 gives the numerical comparisons and the search motivation.

== 1.5 Organization of the paper

Sections 2–6 prove Theorem A: notation, construction, reduction to four types, coset bounds and finite computations, respectively. Section 7 describes the scope of the Lean formalization and identifies the base lattice with Nebe's lattice. Section 8 determines the full automorphism group. Appendices A–G collect terminology, theta series, auxiliary proofs, data and code, pseudocode, the group-theoretic proof and known examples.

A separate supplement contains the Siegel means and search motivation (Supplement §§S1–S2), verification routes, running times and additional tests (Supplement §S3), the support-module argument (Supplement §S4), and a comparison of constructions considered in the search (Supplement §S5). Its sections and tables carry the prefix S.

= 2. Preliminaries and terminology <s2>

We fix conventions for lattices, cosets, group actions and Hermitian forms. Norm always means squared length.

== 2.1 Conventions and terminology

We use $L_56$ for the fixed lattice of §1; the letter $L$ in general definitions and lemmas denotes an arbitrary lattice satisfying the stated assumptions. An isometry between lattices is an additive-group isomorphism preserving the inner product; it need not preserve orientation.

Lattices are given by Gram matrices $G in bb(Z)^(n times n)$ with respect to a basis; vectors are integer #strong[row] vectors $x$, with $chevron.l x\,y chevron.r = x G y^(sans(T))$. A matrix $g$ acts by $x mapsto x g$; it is an isometry if $g G g^(sans(T)) = G$. “Norm” always means $chevron.l x\,x chevron.r$, never its square root. For a lattice $L$, the shell of norm $m$ is $L(m) = { x in L : chevron.l x\,x chevron.r = m }$.

#ptable(
  columns: 3, align: (left, left, left,),
  caption: [Table 1. Terms distinguished in this paper.],
  table.header([term], [symbol], [meaning]),
  [minimum (of a lattice)], [$min Lambda$], [smallest norm of a nonzero vector of a specific lattice $Lambda$],
  [extremal bound], [$mu\(n\)$], [the upper bound $2 floor.l n\/24 floor.r + 2$ for the minimum in dimension $n$; $mu\(56\)= 6$, $mu\(112\)= 10$],
  [inner-shell vector], [—], [nonzero vector of norm $< mu\(n\)$; extremal ⟺ none exists],
  [coset minimum], [$min\(c\)$], [smallest norm of a vector in a coset $c$ modulo $2 L$ (§2.2)],
  [centralizer], [$C$], [elements of $"Aut"\(L\)$ commuting with every element of $"SL"_2\(29\)$ (§2.4); not the full unit group of an order],
)

== 2.2 Cosets modulo $2 L$

For an even unimodular $L$, the quotient $L\/2 L$ is an $bb(F)_2$-vector space of dimension $n$; we call its elements $c = x + 2 L$ #strong[cosets]. Since $chevron.l x + 2 y\,x + 2 y chevron.r = chevron.l x\,x chevron.r + 4 chevron.l x\,y chevron.r + 4 chevron.l y\,y chevron.r$, the function $q\(x + 2 L\)= chevron.l x\,x chevron.r\/2 med mod med 2$ is a well-defined quadratic form on $L\/2 L$. We call a coset #emph[even] or #emph[odd] according to $q$; all vectors in an even coset have norm $equiv 0 med\(mod med 4\)$, and all vectors in an odd coset have norm $equiv 2 med\(mod med 4\)$. A linear map $f$ on $L\/2 L$ is #strong[parity-preserving] if $q\(c f\)= q\(c\)$ for all cosets. In dimension 56 there are $2^55 + 2^27$ even cosets (including 0) and $2^55 - 2^27$ odd cosets (these are the numbers of zeros and of nonzeros of a nondegenerate quadratic form of plus type).

== 2.3 Extremal theta series and shells of $L$

If $L$ is extremal of dimension 56, its theta series is $ theta_L = 1 + 15 thin 590 thin 400 thin q^3 + 36 thin 957 thin 286 thin 800 thin q^4 + 15 thin 284 thin 192 thin 071 thin 680 thin q^5 + dots.h.c $ #calc("C1") (by \[Ser73, Ch. VII\], the space of modular forms of weight 28 is 3-dimensional, so “constant term 1, no $q$, no $q^2$” determines the form; Appendix B). Thus $\|L(6)\|= 15 thin 590 thin 400$, $\|L(8)\|= 36 thin 957 thin 286 thin 800$, $\|L(10)\|= 15 thin 284 thin 192 thin 071 thin 680$. Moreover each nonempty shell of an extremal lattice of dimension $24 k + 8$ is a spherical 7-design (Venkov; see \[BV01\]); we use this only as a consistency test (§6.3).

== 2.4 Nebe's lattices with $"SL"_2\(29\)$ and the centralizer

The group $"SL"_2\(29\)$ has a faithful irreducible representation of degree 14 whose character field is $bb(Q)\(sqrt(29)\)$ and which has Schur index 2 over $bb(Q)$; as a rational representation it has degree 56, and its endomorphism algebra is the totally definite quaternion algebra $cal(Q)$ over $bb(Q)\(sqrt(29)\)$ ramified only at the two infinite places \[Neb98\]. Nebe constructs $"SL"_2\(29\)$-invariant even unimodular lattices $L_(56\,2)\(M\)$ and $L_(56\,2)\(tilde(M)\)$ attached to the two conjugacy classes of maximal orders $M\,tilde(M)$ of $cal(Q)$, and reports minimum 6 for both, computed with PARI \[Neb98, Table II\]. To give a proof whose completeness is guaranteed including rounding errors and which does not depend on the identification of §7.2, we verify the minimum of $L_56$ directly from the distributed data (§6.1). The proof of Theorem A does not use the value from \[Neb98\].

For an $"SL"_2\(29\)$-invariant lattice $L$ we write $M' = "End"_("SL"_2\(29\))\(L\)$ for the ring of integer matrices commuting with $"SL"_2\(29\)$ and preserving $L$ ($bb(Z)$-rank 8). Its elements that are isometries of $L$ form the #strong[centralizer] $C = C_("Aut" L)\("SL"_2\(29\)\)$. The adjoint defined by the inner product agrees with the standard quaternion involution, so $u u^*=1$ is equivalent to reduced norm 1. The centralizer $C$ is the finite group of elements of reduced norm 1 of $M'$; it has order 24 for the catalog lattice $L_(56\,2)\(M\)$ and order 12 (6 up to sign) for the lattice $L_56$ used here #calc("C2").

== 2.5 Hermitian lattices and trace forms

Let $K = bb(Q)\(sqrt(- 5)\)$ with ring of integers $cal(O) = bb(Z)\[sqrt(- 5)\]$ (class number 2). If $tau$ is an endomorphism of a lattice $L$ with $tau^2 = - 5$ and $chevron.l x tau\,y tau chevron.r = 5 chevron.l x\,y chevron.r$, then $L$ becomes an $cal(O)$-module $P_tau$ via $sqrt(- 5) dot.op x := x tau$, and $ h\(x\,y\)= chevron.l x\,y chevron.r + frac(chevron.l x tau\,y chevron.r, sqrt(- 5)) $ is a Hermitian form (linear in the first variable) with $"Re" h = chevron.l dot.op\,dot.op chevron.r$ (Appendix C.1). For Hermitian $cal(O)$-lattices $A\,B$ the tensor product $A times.o_(cal(O)) B$ carries the real form $"Re"\(h_A times.o h_B\)$; this is the Hermitian tensor product of \[CN13\].

= 3. The construction <s3>

We glue two copies of a 56-dimensional lattice along a correspondence of cosets modulo $2 L$ to obtain a 112-dimensional lattice (§3.1). Listing all gluings that preserve the $"SL"_2\(29\)$-symmetry gives only five cases (§3.3, Table 2): two have inner-shell vectors forced by symmetry, two have minimum 8, and the remaining one is our $L_112$. Finally we rewrite $L_112$ as a Hermitian tensor product (§3.4).

== 3.1 Gluing two copies modulo 2

#thm[
#strong[Definition 3.1 (gluing).] Let $L$ be even unimodular of dimension $n$ and $f$ an invertible parity-preserving linear map on $L\/2 L$. The #strong[gluing] of two copies of $L$ along $f$ is $ L_f =  {  1 / sqrt(2)\(x\,v\)med : med x\,v in L\,med v + 2 L =\(x + 2 L\)f  } \,#h(2em)  lr(chevron.l frac(\(x\,v\), sqrt(2))\,frac(\(x\,v\), sqrt(2)) chevron.r)  = 1 / 2  (  chevron.l x\,x chevron.r + chevron.l v\,v chevron.r  )  . $
]

We call $f$ the gluing map and $L_f$ the glued lattice. Taking $L=L_56$, when $f$ is the reduction of an integer matrix $tau$ with $chevron.l x tau\,y tau chevron.r = 5 chevron.l x\,y chevron.r$, we get the lattice $L_tau$ of (1.2).

#thm[
#strong[Lemma 3.2.] Let $L$ be even unimodular of dimension $n$ and $tau in "End"\(L\)$ with $chevron.l x tau\,y tau chevron.r = 5 chevron.l x\,y chevron.r$. Then $L_tau$ is an even unimodular lattice of dimension $2n$.
]

#proofbox[
#strong[Proof.] The map $L xor L arrow.r L\/2 L$, $\(x\,v\)mapsto v - x tau + 2 L$ is a surjective homomorphism (already on $x = 0$). Its kernel $L'_tau$ has index $2^n$ in $L xor L$, so $det L'_tau = 2^(2n) det\(L perp L\)= 2^(2n)$, and scaling by $1\/sqrt(2)$ multiplies the  $2n$-dimensional Gram determinant by $2^(-2n)$; hence $det L_tau = 1$. For evenness write $v = x tau + 2 y$: $ chevron.l x\,x chevron.r + chevron.l v\,v chevron.r = chevron.l x\,x chevron.r + 5 chevron.l x\,x chevron.r + 4 chevron.l x tau\,y chevron.r + 4 chevron.l y\,y chevron.r = 6 chevron.l x\,x chevron.r + 4  (  chevron.l x tau\,y chevron.r + chevron.l y\,y chevron.r  )  equiv 0 med\(mod med 4\)\, $ since $chevron.l x\,x chevron.r$ is even. So $1 / 2\(chevron.l x\,x chevron.r + chevron.l v\,v chevron.r\)$ is even. A lattice all of whose norms are even integers is integral by polarization.  #qed
]

The basis $\(e_i\,e_i tau\)\/sqrt(2)$, $\(0\,2 e_i\)\/sqrt(2)$ $\(1 lt.eq i lt.eq 56\)$ of $L_tau$ has Gram matrix #tagged("3.1", $ mat(delim: "(", 3 G, tau G; \(tau G\)^(sans(T)), 2 G)\, $) which is the form in which $L_112$ is distributed (Appendix D).

== 3.2 Forced collisions from the centralizer

If $f$ agrees modulo 2 with an element $u in C$, then $\(x\,x u\)\/sqrt(2) in L_f$ for all $x$, and a minimal vector $x$ of $L_56$ gives an inner-shell vector of norm $1 / 2\(6 + 6\)= 6$. We call this a #strong[forced collision]: it is caused by symmetry, not by chance. Examples of such constructions are discussed in Supplement §S5.

== 3.3 All $"SL"_2\(29\)$-equivariant gluings

To preserve the $"SL"_2\(29\)$-symmetry, we require that $f$ commute with $"SL"_2\(29\)$ acting on $L_56\/2 L_56$. The ring of $bb(F)_2$-linear maps on $L_56\/2 L_56$ commuting with $"SL"_2\(29\)$ has $bb(F)_2$-dimension 8 and equals the image of $M'\/2 M'$ #calc("C3"), so every commuting map is the reduction of an element of $M'$. Since 2 is inert in $bb(Q)\(sqrt(29)\)$ and $cal(Q)$ is unramified at 2, $M'\/2 M' tilde.equiv M_2\(bb(F)_4\)$.

#thm[
#strong[Proposition 3.3.] (a) Exactly 60 elements of $M'\/2 M'$ are invertible and parity-preserving #calc("C3"). (b) $L_f tilde.equiv L_(u f u')$ for $u\,u' in C$, and $L_f tilde.equiv L_(f^(- 1))$. (c) Modulo (b), the 60 maps fall into 2 classes for $L_(56\,2)\(M\)$ and 3 classes for our $L_56$ (Table 2) #calc("C3").
]

For (b): $\(x\,v\)mapsto\(x u\,v u'\)$ maps $L_f$ isometrically onto $L_(u^(- 1) f u')$, and $\(x\,v\)mapsto\(v\,x\)$ maps $L_f$ onto $L_(f^(- 1))$.

#ptable(
  columns: 5, align: (left, left, left, center, left,),
  caption: [Table 2. The five $"SL"_2\(29\)$-equivariant gluings $L_f$ ($f$ from $M'\/2 M'$) of two copies of a lattice with $"SL"_2\(29\)$.],
  table.header([name], [base], [class of $f$ (size)], [$min L_f$], [inner-shell vectors]),
  [—], [$L_(56\,2)\(M\)$], [contains an element of $C$ (12)], [6], [forced collision],
  [A], [$L_(56\,2)\(M\)$], [does not (48)], [8], [$292 thin 320$ of norm 8 #calc("C4")],
  [—], [$L_56$], [contains an element of $C$ (6)], [6], [forced collision],
  [B], [$L_56$], [does not (36)], [8], [$292 thin 320$ of norm 8 #calc("C4")],
  [#strong[C]], [$L_56$], [does not (18)], [#strong[10 (Theorem A)]], [#strong[none]],
)

Both surviving classes B and C on $L_56$ lift to elements $tau in M'$ with $tau^2=-5$. Of the 24 such elements, 12 reduce modulo 2 into class B and 12 into class C #calc("C2"). Gluings A and B are isometric: an $"SL"_2(29)$-equivariant isometry between them is supplied with the verification data and checked in integer arithmetic #calc("C28"). Thus the two gluings of minimum 8 in Table 2 are the same lattice. More generally, every even unimodular lattice of dimension 112 on which $"SL"_2(29)$ acts as on $L_112$ is $L_(56,2)(M) times.o_M Lambda$ for a unimodular Hermitian lattice $Lambda$ of rank 2 over the maximal order $M$, and there are exactly eight such $Lambda$ up to isometry; Table 2 contains four of the resulting lattices. Supplement §S6 states and proves this classification #calc("C29", "C30", "C31").

== 3.4 The Hermitian description

#thm[
#strong[Proposition 3.4.] Let $H$ be the free Hermitian $cal(O)$-lattice with basis $e_1\,e_2$ and Gram matrix $mat(delim: "(", 3, sqrt(- 5); - sqrt(- 5), 2)$ (so $det H = 6 - 5 = 1$), and $P = P_tau$ obtained from $L_56$ as in §2.5. Then $ phi : med H times.o_(cal(O)) P arrow.r L_tau\,#h(2em) e_1 times.o x + e_2 times.o y med mapsto med 1 / sqrt(2)  (  x\,thick x tau + 2 y  )  $ is an isometry for the real form $"Re"\(h_H times.o h_P\)$. (Appendix C.2)
]

This realizes $L_112$ in the Hermitian tensor-product framework of \[CN13, Sak26\]. Its full automorphism group is determined in §8.

= 4. Reduction to collisions <s4>

We show that an inner-shell vector of $L_112$ corresponds to a pair $\(x\,v\)$, with $x in L_56$ and $v$ in the coset $x tau + 2 L_56$, whose norms are $\(6\,6\)$, $\(6\,10\)$, $\(10\,6\)$ or $\(8\,8\)$ (§4.1). The absence of such “collisions” can be expressed in terms of coset minima (Corollary 4.3), and the $"SL"_2\(29\)$-symmetry reduces it to finitely many cases (§4.2, Table 3). We then state the computational facts F0–F5 on which the rest of the proof rests and derive Theorem A from them (§4.3); Figure 1 at the end of §4.3 shows how these facts and the lemmas combine.

== 4.1 Four types

From now on $L_56$ is even unimodular of dimension 56 with $min L_56 = 6$ and $tau$ satisfies $chevron.l x tau\,y tau chevron.r = 5 chevron.l x\,y chevron.r$. The adjoint of $tau$ is $tau^(*) = 5 tau^(- 1)$; since $tau^2=-5$, $tau^(*) = - tau$ (Appendix C.1).

#thm[
#strong[Definition 4.1 (collision).] For $a\,b in { 6\,8\,10 }$, a #strong[collision of type $\(a\,b\)$] is a pair $\(x\,v\)$ with $x in L_56(a)$, $v in L_56(b)$ and $v equiv x tau med\(mod med 2 L_56\)$. Equivalently, the coset $x tau + 2 L_56$ of some $x in L_56(a)$ contains a vector of norm $b$.
]

#thm[
#strong[Lemma 4.2.] If $z = 1 / sqrt(2)\(x\,v\)in L_tau$ is an inner-shell vector ($z eq.not 0$, $chevron.l z\,z chevron.r lt.eq 8$), then $\(x\,v\)$ is a collision of type $\(6\,6\)$, $\(6\,10\)$, $\(10\,6\)$ or $\(8\,8\)$.
]

#proofbox[
#strong[Proof.] If $x = 0$ then $v in 2 L_56\\{ 0 }$, so $chevron.l v\,v chevron.r gt.eq 4 dot.op 6$ and $chevron.l z\,z chevron.r gt.eq 12$. If $v = 0$ then $x tau in 2 L_56$; applying $tau^(*)$ gives $5 x in 2 L_56$, hence $x = 5 x - 2 dot.op 2 x in 2 L_56$ and again $chevron.l z\,z chevron.r gt.eq 12$. So $x\,v eq.not 0$ and $chevron.l x\,x chevron.r\,chevron.l v\,v chevron.r gt.eq 6$. By the proof of Lemma 3.2, $chevron.l x\,x chevron.r + chevron.l v\,v chevron.r equiv 0 med\(mod med 4\)$, and $chevron.l x\,x chevron.r + chevron.l v\,v chevron.r lt.eq 16$. The only pairs of even integers $gt.eq 6$ with these properties are $\(6\,6\)$ with sum 12 and $\(6\,10\)\,\(8\,8\)\,\(10\,6\)$ with sum 16.  #qed
]

In particular, the type $\(6\,8\)$, which would be the most frequent one by a naive count, is excluded by parity. Since $tau^2 = - 5 equiv 1 med\(mod med 2\)$, the coset map $c mapsto c tau$ is an involution on $L_56\/2 L_56$, so a collision $\(x\,v\)$ of type $\(10\,6\)$ is the same as a collision $\(v\,x\)$ of type $\(6\,10\)$ (Appendix C.4).

#thm[
#strong[Corollary 4.3.] $L_tau$ has no inner-shell vectors if and only if  #linebreak() (i) $min\(r tau + 2 L_56\)gt.eq 14$ for every $r in L_56(6)$ (the coset is odd, so its norms are $6\,10\,14\,dots.h$; this says 6 and 10 do not occur), and  #linebreak() (ii) $min\(x tau + 2 L_56\)gt.eq 12$ for every $x in L_56(8)$ (the coset is even, so its norms are $8\,12\,dots.h$; this says 8 does not occur).
]

(That the cosets in (ii) contain neither 0 nor vectors of norm 4 follows from the case $v = 0$ in the proof of Lemma 4.2 and from $min L_56 = 6$.)

== 4.2 Symmetry

Let $S = "SL"_2\(29\)subset "Aut"\(L_56\)$. Every $g in S$ commutes with $tau$ (exactly, not only modulo 2) #calc("C2"). Hence the coset of $\(x g\)tau$ is the image under $g$ of the coset of $x tau$, and $g$ preserves norms. So condition (i) needs to be tested only for one representative of each $S$-orbit on $L_56(6)$, and (ii) for one representative of each $S$-orbit on $L_56(8)$.

To collect representatives for $L_56(8)$ we use the larger group $S^(*) = S dot.op C$. If $x_1\,dots.h\,x_K$ represent the $S^(*)$-orbits on $L_56(8)$, then the vectors $x_i u$ ($u$ in a set of 6 representatives of $C\/{ plus.minus 1 }$) represent all $S$-orbits (with repetitions). The elements of $C$ do #emph[not] commute with $tau$, which is why all pairs $\(x_i\,u\)$ must be tested.

#ptable(
  columns: 4, align: (left, right, right, left,),
  caption: [Table 3. The cases to be tested.],
  table.header([shell], [vectors], [$S$-orbits], [structure and test units]),
  [$L_56(6)$ (minimal vectors)], [$15 thin 590 thin 400$], [$656$], [632 orbits of size $24 thin 360$ and 24 of size $8 thin 120$; 656 representatives],
  [$L_56(8)$], [$36 thin 957 thin 286 thin 800$], [$1 thin 517 thin 130$], [all of size $24 thin 360$; $254 thin 664$ $S^(*)$-orbits × 6 elements of $C\/{ plus.minus 1 }$ = $1 thin 527 thin 984$ pairs],
)

== 4.3 Finite verification and the proof of Theorem A <s43>

Fix the data files of Appendix D: the Gram matrix $G$ of $L_56$, the two generators of the symmetry group $S$, and the endomorphism matrix $tau$. The labels F0–F5 below identify the statements used by the verification programs; the headings describe their mathematical content.

#fact[
#strong[Defining matrices (F0).] The matrix $G$ in Appendix D is positive definite, even integral and of determinant 1; (3.1) is also even and of determinant 1. #calc("C2")
]

#fact[
#strong[Minimum norm of the input lattice (F1).] $min L_56 = 6$. #calc("C5")
]

#fact[
#strong[Complete norm-6 orbit list (F2).] $L_56(6)$ is the disjoint union of the $S$-orbits of 656 explicitly listed vectors. #calc("C8")
]

#fact[
#strong[Complete norm-8 orbit list (F3).] $L_56(8)$ is the union of the $S$-orbits of the $1 thin 527 thin 984$ vectors $x_i u$; it consists of $1 thin 517 thin 130$ regular $S$-orbits, that is, orbits with trivial stabilizer, hence of size $|S| = 24 thin 360$. #calc("C9")
]

#fact[
#strong[Symmetry and endomorphism identities (F4).] The two generators of $S$ preserve the Gram matrix, generate a group of order $24 thin 360$, and commute with $tau$; $tau^2 = - 5$ and $tau G tau^(sans(T)) = 5 G$. #calc("C2")
]

#fact[
#strong[Lower bounds for the prescribed cosets (F5).] (a) $min\(r tau + 2 L_56\)gt.eq 14$ for each of the 656 representatives $r$. (b) $min\(x_i u tau + 2 L_56\)gt.eq 12$ for each of the $1 thin 527 thin 984$ pairs. Part (b) is established by two different methods (§§6.5 and 6.7); either one suffices. #calc("C10", "C11", "C13")
]

#proofbox[
#strong[Proof of Theorem A.] The defining matrices give the even unimodular lattice of dimension 112 described in Lemma 3.2; the required endomorphism identities are part of F4. By F1 and Lemma 4.2, any nonzero vector of norm below 10 would give one of the four types listed in §1.3.

The isometries in $S$ commute with $tau$ by F4. Hence the minimum norm of the coset $(x g)tau+2 L_56$ equals that of $x tau+2 L_56$ for $g in S$. By F2 and F3, the two lower bounds of Corollary 4.3 therefore need only be checked on the supplied norm-6 and norm-8 collections. F5 gives the bounds 14 and 12 on these collections. The type $(10,6)$ is covered by the interchange argument of Appendix C.4. Thus no type can occur, and $min L_112>=10$.

Since $L_112$ is even unimodular of dimension 112, (1.1) gives $min L_112<=10$. This proves the theorem. #qed
]

#figure(
  proof-dependencies(lang: "en"),
  caption: [Figure 1. Dependencies in the proof of Theorem A. Blue boxes are the finite computations F0–F5 of §4.3, each labelled with the section that describes its algorithm and its row in Table D2; F4 appears twice, once for its identities about $tau$ and once for those about $S$. Green boxes are statements proved in the text. An arrow from one box to another means that the second uses the first. F5b is established by two methods (§§6.5 and 6.7), either of which suffices ($or$). Consistency tests and supplementary arguments are not shown.],
  kind: image, numbering: none,
)


= 5. Certificates for coset minima <s5>

We derive lower bounds for a coset minimum from the norm of one representative and its inner products with all minimal vectors. The midpoint lemma proves that the stated conditions on a representative imply the required bound; the finite computations later check these conditions. A representative $w_0$ satisfying these conditions (Check 5.4) is called a #strong[certificate] for its coset: checking it is a finite computation, and the corollaries below turn it into a proof of the bound.

#thm[
#strong[Lemma 5.1 (midpoint lemma).] Let $L$ be even unimodular with $min L = 6$. If $w\,w' in L$ lie in the same coset modulo $2 L$ and $w eq.not plus.minus w'$, then $ chevron.l w\,w chevron.r + chevron.l w'\,w' chevron.r plus.minus 2 chevron.l w\,w' chevron.r med gt.eq med 24 #h(2em) upright("for both signs.") $
]

#proofbox[
#strong[Proof.] $w minus.plus w' in 2 L\\{ 0 }$, so the midpoint $1 / 2\(w minus.plus w'\)$ is a nonzero vector of $L$ and has norm $gt.eq 6$; multiply by 4.  #qed
]

The two corollaries below retain the assumptions on $L$ in Lemma 5.1. Two immediate consequences follow. Two vectors of norm $6$ that are distinct up to sign never lie in the same coset (with $t = chevron.l w\,w' chevron.r$, the inequalities $12 + 2 t gt.eq 24$ and $12 - 2 t gt.eq 24$ cannot both hold), and the same holds for norm 8. Hence each coset contains at most one pair $plus.minus w$ of norm 6, and at most one pair of norm 8 (Appendix C.3).

#thm[
#strong[Corollary 5.2 (lower bound for odd cosets).] If an odd coset $c$ contains a vector $w_0$ of norm $N in { 14\,18 }$ such that $\|chevron.l w_0\,u chevron.r\|lt.eq 6$ for every $u in L(6)$, then $min\(c\)gt.eq 14$.
]

#proofbox[
#strong[Proof.] Suppose $w in c$ has norm $m lt.eq 10$. Norms in $c$ are $equiv N med\(mod med 4\)$, so $m in { 6\,10 }$; in particular $m < N$, $N + m <= 28 < 32$ and $w eq.not plus.minus w_0$. The midpoints $a = 1 / 2\(w_0 + w\)$ and $b = 1 / 2\(w_0 - w\)$ are nonzero vectors of $L$ (Lemma 5.1) with $chevron.l a\,a chevron.r + chevron.l b\,b chevron.r = 1 / 2\(N + m\) < 16$. Since $L$ is even with minimum 6, they cannot both have norm $gt.eq 8$; so one of them is a minimal vector $u$, and $w_0 - 2 u = plus.minus w$. Taking norms, $N - 4 chevron.l w_0\,u chevron.r + 24 = m$, i.e. $chevron.l w_0\,u chevron.r = 1 / 4\(N + 24 - m\) > 6$, a contradiction.  #qed
]

#thm[
#strong[Corollary 5.3 (lower bound for even cosets).] If an even coset $c$ contains a vector $w_0$ of norm $N in { 12\,16\,20 }$ such that $\|chevron.l w_0\,u chevron.r\|lt.eq 6$ for every $u in L(6)$, then $min\(c\)gt.eq 12$.
]

#proofbox[
#strong[Proof.] Norms in the even coset $c$ are $equiv 0 med\(mod med 4\)$. The coset does not contain 0 (otherwise $w_0 in 2 L$ and $N gt.eq 4 dot.op 6$), nor a vector of norm 4 (since $min L=6$). If $w in c$ had norm $m = 8$, then $m < N$ and $N + m <= 28$, and the argument of Corollary 5.2 gives a minimal vector $u$ with $chevron.l w_0\,u chevron.r = 1 / 4\(N + 16\) > 6$, a contradiction.  #qed
]

#thm[
#strong[Check 5.4 (coset-bound data).] To verify a lower bound for a coset $c$, supply a representative $w_0 in c$ satisfying Corollary 5.2 or 5.3. Check: #linebreak()
(a) $w_0 in c$; when $c=x tau+2L$, every coordinate of $w_0-x tau$ is even. #linebreak()
(b) $chevron.l w_0,w_0 chevron.r$ belongs to ${14,18}$ for an odd coset, or to ${12,16,20}$ for an even coset. #linebreak()
(c) $|chevron.l w_0,u chevron.r|<=6$ for every $u in L(6)$, using the complete minimal-vector list.
]

These conditions are sufficient but not necessary: a coset without short vectors need not have a representative satisfying them. For every coset required in §§6.6–6.7, such a representative is supplied and checked.

= 6. Algorithms and the verification <s6>

Three implementations are referred to below: implementation 1 constructed $L_112$ and performed the main computations; implementation 2 re-implemented every step, sharing only the data files; implementation 3 started from the four data files of Appendix D alone (Supplement §S3.3). For each computational fact we describe the algorithm and the checks on its output. Completeness requires both disjointness and agreement of the orbit-size sum with the theta-series coefficient. The two rigorous even-coset methods share these orbit lists and the odd-coset bounds (§1.3); separate implementations and tests on gluings A and B check their results. Floating-point searches and samples have the supplementary scope stated below. Running times are those observed on the machine used (8 cores, 15 GB of memory). Code references are given in Appendix D and pseudocode in Appendix E.

#ptable(
  columns: 4, align: (left, left, left, left,),
  caption: [Table 4. The computational facts and how they were checked.],
  table.header([fact], [main method], [other methods, independent reproductions], [nature]),
  [F1], [interval-arithmetic enumeration (BKZ-40 basis)], [second exact enumeration in integer arithmetic (a′); reduction to $L_(56\,2)\(M\)$ plus $bb(F)_2$ linear algebra; fplll (two bases); PARI #raw("qfminim")], [interval arithmetic, integer (others: floating point)],
  [F2], [closure + orbits, size sum], [disjointness, design identities (implementation 2); implementation 3], [integer],
  [F3], [marked sums of two minimal vectors, size sum], [recount from $K_8$, design identities; implementation 3], [integer],
  [F4], [matrix identities], [two implementations], [integer],
  [F5a], [656 odd-coset certificates], [the checker of implementation 2; CVP on two bases; canonical forms], [integer],
  [F5b], [canonical forms (two implementations)], [exhaustive CVP; implementation 3; even-coset certificates (all pairs)], [integer (CVP: floating point)],
)

== 6.1 F1: the minimum of the base lattice

The enumeration (a), in interval arithmetic, and the enumeration (a′), in integer arithmetic, cannot miss vectors; either one proves F1 directly from the data file without depending on the minimum reported in the literature (§2.4). Route (b), by contrast, assumes the literature value and is used to check consistency with it; (c) is a supplementary check in floating-point arithmetic.

#strong[(a) Interval enumeration.] #calc("C5")

#enum(
  [Reduce the Gram matrix with BKZ-40. Check exactly that the transformation $U$ is an integer matrix with $det U = plus.minus 1$ and compute $G' = U G U^(sans(T))$ in integers (floating point used inside the reduction does not affect correctness).],
  [Compute $G' = V^(sans(T)) "diag"\(D\)V$ ($V$ unit upper triangular) #strong[exactly in rational arithmetic].],
  [Replace every entry of $D$ and $V$ by an interval around its nearest double, with a safety margin on both sides.],
  [Run Fincke–Pohst/Schnorr–Euchner enumeration \[FP85, SE94\] in interval arithmetic, widening every result outward (by $2^(- 51)$ relative, against the $2^(- 53)$ error of round-to-nearest), and prune only when the #strong[lower end] of the interval of the partial norm exceeds the radius 4.],
)

The true partial norm always lies in its interval, so no vector of true norm $lt.eq 4$ can be pruned. The norms of the vectors reaching the leaves are computed in integers. The results are in Table 5: for $L_56$, 8 454 837 756 nodes were visited and the only leaf reached was the zero vector (34 minutes with the published code).

#ptable(
  columns: 6, align: (left, center, center, right, left, left,),
  caption: [Table 5. Results of the interval enumeration (only one of $plus.minus x$ is enumerated; counts include both signs).],
  table.header([lattice], [dim], [radius], [nodes], [nonzero vectors found], [expected]),
  [$E_8$ (control)], [8], [2], [248], [240 of norm 2], [240],
  [Leech lattice (control)], [24], [4], [$2 thin 019 thin 561$], [$196 thin 560$ of norm 4, none of norm 2], [same],
  [$Lambda_24 perp Lambda_24 perp E_8$ (control)], [56], [4], [$11 thin 081 thin 124$], [240 of norm 2, $395 thin 280$ of norm 4], [same],
  [#strong[$L_56$]], [56], [4], [$8 thin 454 thin 837 thin 756$], [#strong[none]], [—],
)

#strong[(a′) A second exact enumeration, by a different method.] A separately written program (developed without reference to the code of (a)) makes every decision in integer arithmetic instead of interval arithmetic. The approximate Cholesky factor of $G'$ (BKZ-40 basis, $U$ checked exactly as in (a)) is scaled by $2^(40)$ and rounded to an integer upper triangular matrix $R$; then $Q(x) = |R x^(sans(T))|^2$ is an integer quadratic form, the error matrix $E = 2^(80) G' - R^(sans(T)) R$ is computed exactly, and $|x E x^(sans(T))| <= norm(E)_F norm(G'^(-1))_infinity chevron.l x\,x chevron.r$ with $G'^(-1)$ an exact integer matrix. Hence $chevron.l x\,x chevron.r <= 4$ implies $Q(x) <= T := 4 dot 2^(80) + 4 norm(E)_F norm(G'^(-1))_infinity$ (a relative enlargement of $3.8 times 10^(-7)$). All $x$ with $Q(x) <= T$ are enumerated in C with 128-bit integers, the range at each level being given by exact integer square roots, so no vector is pruned because of rounding. For $L_56$: $14 thin 773 thin 398 thin 896$ nodes (both signs), no nonzero vector found (96 minutes) #calc("C27"). Positive control: $E_8^7$ in a random basis gives $1 thin 680$ vectors of norm 2 and $1 thin 224 thin 720$ of norm 4, as expected.

#strong[(b) Reduction to Nebe's lattice.] $L_56$ is the sublattice $L_(56\,2)\(M\)X + 2 L_(56\,2)\(M\)$ of the catalog lattice (where $X$ is an element of $M\/2 M$ whose action modulo 2 has an image of dimension 28), rescaled by $1\/sqrt(2)$; the Gram matrix of this sublattice agrees entry by entry with that of $L_56$. Hence norm-4 vectors of $L_56$ correspond bijectively to norm-8 vectors of $L_(56\,2)\(M\)$ whose class lies in an $"SL"_2\(29\)$-invariant 28-dimensional subspace $W$ of $L_(56\,2)\(M\)\/2 L_(56\,2)\(M\)$, and norm-2 vectors of $L_56$ to norm-4 vectors of $L_(56\,2)\(M\)$. Consider the $1 thin 528 thin 956$ pairs (norm-8 orbit representative of $L_(56\,2)\(M\)$, centralizer element); the $127 thin 413$ representatives have orbit sizes summing to the theta coefficient. None of these pairs has its coset in $W$ #calc("C6"). Positive control: the 656 orbit representatives of minimal vectors of $L_56$ all appear in $L_(56\,2)\(M\)$ with norm 12 and class in $W$. This proves “$min L_(56\,2)\(M\)= 6 arrow.r.double min L_56 = 6$”, reducing F1 to a property of the literature lattice \[Neb98, Table II\].

#strong[(c) Floating-point enumerations.] fplll enumeration of all vectors of norm $lt.eq 4.5$ (two bases) and PARI #raw("qfminim") for norm $lt.eq 4$ (implementation 2, BKZ-50 basis) also found none #calc("C7").

== 6.2 F2: orbits of minimal vectors

We grow the set of minimal vectors by a closure operation, split it into orbits, and stop when the orbit sizes add up to the kissing number $15 thin 590 thin 400$. Disjointness and agreement of the total sizes prove completeness.

Starting from a few minimal vectors found by BKZ, we generated minimal vectors by closure: if $r\,s in L_56(6)$ and $chevron.l r\,s chevron.r = 3$ then $r - s in L_56(6)$. For each new vector we computed its $S$-orbit (by applying all $12 thin 180$ elements of $S\/{ plus.minus 1 }$) and recorded it as one orbit; the closure step produces vectors outside the orbits already found. We obtained 656 distinct orbits, with sizes adding up to $632 times 24 thin 360 + 24 times 8 thin 120 = 15 thin 590 thin 400 =\|L_56(6)\|$ #calc("C8"). Since distinct orbits are disjoint, #strong[completeness follows from the size sum and F1]. A separate implementation expanded all orbits, checked pairwise disjointness, and checked the identities of §6.3.

== 6.3 Completeness tests: orbit-size sums and design identities

In addition to the size sum, we verified exact identities (equalities of integers of size about $10^18$) that follow from the shells being spherical 7-designs, computed from the lists of representatives. Barring coincidence, duplicates or omissions would violate them.

For every $a in bb(R)^56$ $ sum_(x in L_56(m)) chevron.l x\,a chevron.r^2 & =\|L_56(m)\|frac(m chevron.l a\,a chevron.r, 56)\, \ sum_(x in L_56(m)) chevron.l x\,a chevron.r^4 & =\|L_56(m)\|frac(3 m^2 chevron.l a\,a chevron.r^2, 56 dot.op 58)\, \ sum_(x in L_56(m)) chevron.l x\,a chevron.r^6 & =\|L_56(m)\|frac(15 m^3 chevron.l a\,a chevron.r^3, 56 dot.op 58 dot.op 60) . $ The left sides were computed from the representative lists (representative $times$ group element $times$ element of $C$, weighted by orbit sizes) for three integer vectors $a$ and for $m = 6$ and $m = 8$; all 18 identities hold exactly #calc("C8").

== 6.4 F3: orbits of norm-8 vectors via marked sums of two minimal vectors

The approximately 37 billion vectors are too many to store, so we distinguish orbits by marking only those of their elements that are sums of two minimal vectors. Completeness is again proved by the size sum.

Every norm-8 vector we need can be written as $x = r + s$ with $r\,s in L_56(6)$ and $chevron.l r\,s chevron.r = - 2$, and by symmetry $r$ may be taken among the (at most 150) $S^(*)$-orbit representatives $r_i$ of minimal vectors. Let $X_i = { r_i + s : s in L_56(6)\,med chevron.l r_i\,s chevron.r = - 2 }$.

#thm[
#strong[Definition 6.1.] For an $S^(*)$-orbit $O subset L_56(8)$, the #strong[marked elements] of $O$ are the elements of $O inter union.big_i X_i$, that is, the elements of $O$ that are sums $r_i + s$ of the above shape (possibly in several ways). Completeness of the orbit list does not rely on every norm-8 vector being such a sum: it follows from the orbit-size sum (Table 3).
]

The algorithm runs through candidates $x in X_i$; whenever $x$ is not yet marked, it starts a new orbit, computes all elements of that orbit in $union.big_i X_i$ and marks them. This needs only one matrix product per orbit: $y = plus.minus x u g^(- 1)$ lies in $X_i$ iff $chevron.l y\,r_i chevron.r = 4$, i.e. iff $chevron.l x u\,r_i g chevron.r = plus.minus 4$, so precomputing $W = { r_i g }$ finds them all at once. The decompositions of $x = r_i + s_0$ can be read off from the minimal vectors with inner product 2 or 3 with $r_i$, which reduces the work by a factor of about 30. The stabilizer order of $x$ is the number of elements of $S^(*)$ that map $x$ to itself, read off from the same matrix product (they are group elements, not decompositions); a wrong count would make the orbit sizes, and hence their sum, wrong. Only the marked elements (tens of millions) are stored.

The result is Table 3: $1 thin 517 thin 130 times 24 thin 360 = 36 thin 957 thin 286 thin 800 =\|L_56(8)\|$ #calc("C9"). This was checked in three ways: (1) the $S^(*)$-orbit sizes add up to $\|L_56(8)\|$; (2) the set $K_8$ of canonical forms (§6.5) of the cosets of all $x_i u$ has exactly $1 thin 517 thin 130$ elements, and recomputing each orbit size from $K_8$ gives the same total (which would fail if an orbit were counted twice); (3) the identities of §6.3. The first 25 orbits were cross-checked against a naive method, and the canonical forms of the cosets of $2 thin 000$ independently generated norm-8 vectors were all found in $K_8$.

== 6.5 F5b: canonical forms on $L_56\/2 L_56$

A coset is stored as a 56-bit integer and its $"SL"_2\(29\)$-orbit is named by the smallest element (canonical form). Since a class contains a norm-8 vector if and only if its canonical form lies in the table $K_8$, each test is a single table look-up. Only integer arithmetic is used, so no rounding occurs.

Identify $L_56\/2 L_56$ with $bb(F)_2^56$ via coordinates modulo 2. Each $g in S\/{ plus.minus 1 }$ acts by an $bb(F)_2$-linear map, implemented with byte-wise lookup tables and XOR.

#thm[
#strong[Definition 6.2 (canonical form).] The #strong[canonical form] $"can"\(c\)$ of a coset $c$ is the smallest 56-bit integer in its orbit ${ c g : g in S }$.
]

#thm[
#strong[Proposition 6.3.] Let $K_8 = { "can"\(x_i u + 2 L_56\)}$ (all pairs). Assuming F3, a coset $c$ contains a vector of norm 8 if and only if $"can"\(c\)in K_8$.
]

#proofbox[
#strong[Proof.] If $w in c$ has norm 8, by F3 $w = x_i u g$ for some $i\,u$ and $g in S$, so $c =\(x_i u + 2 L_56\)g$ and $"can"\(c\)= "can"\(x_i u + 2 L_56\)in K_8$. Conversely, $"can"\(c\)= "can"\(x_i u + 2 L_56\)$ means $c =\(x_i u + 2 L_56\)g$ for some $g$, and $x_i u g in c$ has norm 8.  #qed
]

Test for type $\(8\,8\)$: for each pair, compute the coset of $x_i u tau$, its canonical form ($12 thin 180$ table look-ups, about 0.3 ms), and look it up in $K_8$. The results are in Table 6. The test was implemented twice with separately written code (group enumeration, tables, canonical forms, look-up), with self-tests (table look-up equals matrix product; canonical form is $S$-invariant; the $12 thin 180$ group elements are distinct modulo 2). The type $\(6\,6\)$ was tested on the 656 minimal-vector cosets using $K_6={"can"(r_i+2L_56)}$.

#ptable(
  columns: 5, align: (left, right, right, right, right,),
  caption: [Table 6. Results of the canonical-form test for type $\(8\,8\)$ (identical for $tau$ and $tau^(- 1) med mod med 2$).],
  table.header([gluing], [pairs tested], [colliding pairs], [colliding $S$-orbits], [norm-8 vectors of $L_f$]),
  [class containing an element of $C$], [$3 thin 000$ (sample)], [$3 thin 000$], [—], [— (minimum 6)],
  [gluing A], [$1 thin 528 thin 956$], [36], [6], [$292 thin 320$],
  [gluing B], [$1 thin 527 thin 984$], [10], [6], [$292 thin 320$],
  [#strong[gluing C]], [$1 thin 527 thin 984$], [#strong[0]], [#strong[0]], [#strong[0]],
)

== 6.6 F5a: certificates for the types $\(6\,6\)$, $\(6\,10\)$, $\(10\,6\)$

All 656 odd cosets have a certificate of norm 14 or 18. The search is heuristic; its output is checked by Check 5.4.

For each representative $r$ we start from $w = r tau$ (norm 30) and, while some minimal vector $u$ has $chevron.l w\,u chevron.r gt.eq 7$, replace $w$ by $w - 2 u$ (the #strong[descent]). This lowers the norm by $4\(chevron.l w\,u chevron.r - 6\)> 0$ and stays in the class. Positive control: starting from the sum of a norm-10 vector and an element of $2 L_56$, the descent ended at norm 10 in all 60 trials and never produced a false certificate.

#ptable(
  columns: 3, align: (left, right, left,),
  caption: [Table 7. The 656 odd-coset certificates.],
  table.header([$chevron.l w_0\,w_0 chevron.r$], [number], [maximum of $\|chevron.l w_0\,u chevron.r\|$ over all minimal vectors]),
  [14], [243], [5 (43 vectors), 6 (200)],
  [18], [413], [6 (all 413)],
)

The certificates were produced by one implementation and re-checked by a separate implementation with separately written code, which also re-derived the lemma #calc("C10"). Two closest-vector enumerations on different bases independently found no vector of norm $lt.eq 10$ in these classes #calc("C12").

== 6.7 F5b: bounds from even-coset representatives

#strong[Even-coset certificates.] For every pair we computed an even-coset certificate (Corollary 5.3) by the descent of §6.6, starting from $w = x_i u tau$ (norm 40). Inner products are computed in float64; they are exact because every partial sum of a product $A B$ of integer matrices is bounded by $sum_k |a_k| |b_k| <= (max_"row" sum_k |a_k|) dot max |B|$, which is checked to be below $2^52$ at run time for both products used. The result: #strong[every one of the $1 thin 527 thin 984$ pairs has a certificate] (Table 8) #calc("C13"). Thus F5b also holds by an argument that uses only the midpoint lemma, integer inner products and the list F2, independently of canonical forms. All certificates were re-checked by a separately written program, using integer arithmetic and float32 products only where all partial sums are proved to be below $2^24$ #calc("C27").

#ptable(
  columns: 4, align: (left, left, right, right,),
  caption: [Table 8. Even-coset certificates for all $1 thin 527 thin 984$ pairs.],
  table.header([$chevron.l w_0, w_0 chevron.r$], [max $|chevron.l w_0, u chevron.r|$], [number], [share]),
  [12], [5], [$41 thin 437$], [2.71 %],
  [12], [6], [$692$], [0.05 %],
  [16], [6], [$1 thin 465 thin 524$], [95.91 %],
  [20], [6], [$20 thin 331$], [1.33 %],
)

= 7. Identification and formalization <s7>

== 7.1 Formalization of the deduction (Lean)

The deduction from the computational facts to Theorem A has been proved in the proof assistant Lean 4 (with mathlib) and machine-checked. The Lean statement (#raw("theoremA") and #raw("theoremA_canonical") in #raw("lean/EEUL/L112/Chain.lean")) is: #strong[assuming F1–F5, if $\(x\,x tau + 2 y\)eq.not 0$ then $chevron.l x\,x chevron.r + chevron.l x tau + 2 y\,x tau + 2 y chevron.r gt.eq 20$.] By (1.2) this says that $L_112$ has no inner-shell vector. The facts F1–F5 are hypotheses of the Lean theorems, and the translation through (1.2) is outside Lean. The formalization excludes errors that consist of a gap in this deduction (a missing type, a missing case, or a wrong direction).

The setting is abstract: $L_56$ is an additive group with an integer-valued symmetric bilinear form $B$, even norms, nonzero vectors of norm $gt.eq 6$ (F1), and $tau$ with $B\(x tau\,y tau\)= 5 B\(x\,y\)$ and $tau^2 = - 5$ (F4). The symmetry group, the representatives and the certificates are the fields of a structure whose axioms are F2–F5. Lean writes maps on the left ($tau x$ and $g x$ for our $x tau$ and $x g$). The two ways of checking F5b enter as two forms of the hypothesis: “the coset of each norm-8 representative contains no vector of norm 8” (canonical forms, §6.5; Proposition 6.3, which turns the computed $"can"\(c\)in.not K_8$ into this statement, is applied outside Lean) and “the coset of each norm-8 representative has an even certificate” (§6.7, Corollary 5.3). The formalized statements are listed in Table 9.

#ptable(
  columns: 3, align: (left, left, left,),
  caption: [Table 9. Statements proved in Lean (#raw("lean/EEUL/L112/Chain.lean")).],
  table.header([Lean theorem], [in this paper], [content]),
  [#raw("no_inner_shell_ne8"), #raw("no_inner_shell")], [Lemma 4.2, Corollary 4.3, Appendix C.4], [if (i) $min\(r tau + 2 L_56\)gt.eq 14$ for every $r in L_56(6)$ and (ii) for every $x in L_56(8)$ the coset $x tau + 2 L_56$ contains no vector of norm 8 (or $min\(x tau + 2 L_56\)gt.eq 12$), then $chevron.l x\,x chevron.r + chevron.l x tau + 2 y\,x tau + 2 y chevron.r gt.eq 20$ whenever $\(x\,x tau + 2 y\)eq.not 0$],
  [#raw("midpoint_lemma")], [Lemma 5.1], [if $w eq.not plus.minus w'$ lie in the same coset, then $chevron.l w\,w chevron.r + chevron.l w'\,w' chevron.r plus.minus 2 chevron.l w\,w' chevron.r gt.eq 24$],
  [#raw("cert_bound"), #raw("odd_bound"), #raw("even_bound")], [Corollaries 5.2, 5.3], [a certificate (Check 5.4) of norm $N$ with $12 lt.eq N lt.eq 20$ forces all vectors of its coset to have norm $gt.eq 12$; hence $gt.eq 14$ for odd cosets ($N in { 14\,18 }$) and $gt.eq 12$ for even cosets ($N in { 12\,16\,20 }$)],
  [#raw("class_pred_transport"), #raw("class_bound_transport")], [§4.2], [a property of the norms in the coset $r tau + 2 L_56$ of a representative holds in the coset $\(r g\)tau + 2 L_56$ for every $g in S$],
  [#raw("theoremA")], [§4.3, derivation of Theorem A with F5b checked by certificates (§6.7)], [assuming F1 and F2–F5 (the elements of $S$ are isometries commuting with $tau$; the norm-6 and norm-8 vectors are images of the representatives; the coset of each norm-6 representative has an odd certificate, that of each norm-8 representative an even one), $chevron.l x\,x chevron.r + chevron.l x tau + 2 y\,x tau + 2 y chevron.r gt.eq 20$ whenever $\(x\,x tau + 2 y\)eq.not 0$],
  [#raw("theoremA_canonical")], [§4.3, derivation of Theorem A with F5b checked by canonical forms (§6.5)], [the same conclusion, with F5b in the form “the coset of each norm-8 representative contains no vector of norm 8”],
)

Check: the package builds without warnings (a #raw("sorry") anywhere would give one), each theorem depends only on the standard axioms #raw("propext"), #raw("Classical.choice"), #raw("Quot.sound"), and every declaration passes the kernel again when replayed by #raw("leanchecker"). The script #raw("lean/check.sh") runs the three checks; the expected axioms are in #raw("lean/expected-axioms.txt") #calc("C22").

Not formalized (outside the Lean statements):
- the computational facts themselves: F0 (unimodularity, an integer determinant), the matrix identities of F4, and the individual numbers in F1–F5 (§6);
- the passage from the pair $\(x\,x tau + 2 y\)$ to the vector $\(x\,x tau + 2 y\)\/sqrt(2) in L_112$ and the factor $1\/2$ in its norm (1.2);
- the extension of F4 from the two generators checked by the programs to the whole group $S$ (the Lean hypothesis is about every element of $S$);
- the completeness arguments behind F2 and F3 (disjoint orbits whose sizes add up to the theta-series coefficient, §6.2 and §6.4) and the theta series itself (§2.3, Appendix B); Lean assumes the conclusion “every vector of norm 6 (norm 8) is the image of a representative”;
- Proposition 6.3, which turns the computed $"can"\(c\)in.not K_8$ into “the coset $c$ contains no vector of norm 8”;
- the upper bound (1.1), $min L_112 lt.eq 10$.

== 7.2 Identification with Nebe's lattice

Our $L_56$ is $"SL"_2\(29\)$-equivariantly isometric to $L_(56\,2)\(tilde(M)\)$ built from Nebe's definition \[Neb98\] without external data #calc("C23").

#enum(
  [Build $L_56' = L_(56\,2)\(tilde(M)\)$ and generators $z'$ (order 29), $w'$ (order 4) of $"SL"_2\(29\)$ from the model over $bb(Q)\(zeta_29\)$ (code: #raw("code/supplementary/nebe/cycloquat.py"); of the two classes of maximal orders, the one whose centralizer has order 12 is $tilde(M)$).],
  [Find a group isomorphism between the two copies of $"SL"_2\(29\)$ with GAP (also composed with the outer automorphism), and compute the space of equivariant maps $L_56' arrow.r L_56$; it is 8-dimensional.],
  [On its integral part (rank 8) enumerate the elements with $Q\(T\)= "tr"\(G' ""^(- 1) T G T^(sans(T))\)lt.eq 56$; isometries are exactly the elements with $Q = 56$.],
)

We find 6 (up to sign) unimodular integer matrices $T$ with $T G T^(sans(T)) = G'$ intertwining the two actions, as many as predicted by the centralizer of order 12. Moreover, in the coordinates of $L_56'$, $tau$ becomes right multiplication by an element of $tilde(M)$ of reduced norm 5. Thus #strong[gluing C is built from Nebe's lattice $L_(56\,2)\(tilde(M)\)$ and an element of reduced norm 5 and reduced trace 0 of its maximal order $tilde(M)$; such elements fall into two classes modulo 2 in the sense of §3.3, and $tau$ belongs to the class giving minimum 10].

#strong[The element explicitly.] #raw("cycloquat.py") works in the algebra $bb(Q)(zeta_29) plus.o bb(Q)(zeta_29) b$ with $b^2 = -1$ and $b x = macron(x) b$, where $macron(x)$ is the complex conjugate; $"SL"_2(29)$ acts on it from the left by the construction of \[Neb98, §3\]. Let $K_4 subset bb(Q)(zeta_29)$ be the quartic subfield; its ring of integers has the $bb(Z)$-basis of Gaussian periods $eta_j = sum_(k=0)^6 zeta_29^(2^(4k+j))$ ($j = 0, dots, 3$; 2 is a primitive root modulo 29). Complex conjugation exchanges $eta_0 arrow.l.r eta_2$ and $eta_1 arrow.l.r eta_3$, and its fixed field in $K_4$ is $bb(Q)(sqrt(29))$. The commutant of $"SL"_2(29)$ is right multiplication by $cal(Q) = K_4 plus.o K_4 b$, the quaternion algebra of §2.4. The maximal order $tilde(M)$ constructed by the program is the $bb(Z)$-module with basis
$ m_0 = (eta_0 + 41 eta_1 + 144 eta_2 + 104 eta_3 + (133 eta_0 + 88 eta_1 + 12 eta_2 + 492 eta_3) b) / 145, $
$ m_1 = eta_1 + 2 eta_3 b, quad m_2 = eta_2 + 3 eta_3 b, quad m_3 = eta_3 + 3 eta_3 b, $
$ m_4 = (eta_0 + eta_3) b, quad m_5 = (eta_1 + eta_3) b, quad m_6 = (eta_2 + 4 eta_3) b, quad m_7 = 5 eta_3 b. $
In the coordinates of $L_56'$, the endomorphism $tau$ is right multiplication by
$ h = x + y b, quad x = (33 (eta_0 - eta_2) + 48 (eta_1 - eta_3)) / 145, quad y = (-106 eta_0 + 4 eta_1 - 39 eta_2 - 4 eta_3) / 145, $
that is, $h = 33 m_0 - 9 m_1 - 33 m_2 - 24 m_3 - 31 m_4 - 20 m_5 - 3 m_6 + 28 m_7 in tilde(M)$. Since $macron(x) = -x$, the reduced trace of $h$ is $0$, and its reduced norm $x macron(x) + y macron(y)$ is $5$, so that $h^2 = -5$. Replacing $T$ by another of the 6 isometries replaces $h$ by $u^(-1) h u$ for a unit $u$ of $tilde(M)$, which does not change the isometry class of the gluing (Proposition 3.3(b)). The lattice $L_(56,2)(tilde(M))$ is the $"SL"_2(29)$-invariant unimodular lattice among the lattices $(1 - zeta_29)^i thin bb(Z)[zeta_29] tilde(M)$ ($i gt.eq 0$; spanned by the products of elements of $bb(Z)[zeta_29]$ on the left and of $tilde(M)$ on the right) with the forms $"Tr"_(bb(Q)(zeta_29)\/bb(Q)) (c (x macron(x') + y macron(y')))$ on elements $x + y b$, $x' + y' b$, where $c in bb(Q)(sqrt(29))$ is totally positive \[Neb98, §3\]. Together with (1.2), these data determine $L_112$ up to isometry without the files.

= 8. The automorphism group <s8>

We first compute, by finite exact lattice computations, the normalizer of $"SL"_2\(29\)$ in $"Aut"\(L_112\)$; then we prove that $"SL"_2\(29\)$ is normal in $"Aut"\(L_112\)$, by a group-theoretic argument modeled on Sakamoto's determination of the automorphism groups in dimension 88 \[Sak26, App. A\] (Appendix F). Neither step uses the extremality of $L_112$, and Theorem A does not depend on this section.

#thm[
#strong[Theorem B.] Let $S tilde.equiv "SL"_2\(29\)$ act diagonally on $L_112$. (a) The centralizer $C_("Aut"\(L_112\))\(S\)$ has order exactly $48$ #calc("C24"). (b) The outer automorphism of $S$ is induced by an automorphism of $L_112$; hence $\|N_("Aut"\(L_112\))\(S\)\|= 2 dot.op 24 thin 360 dot.op 48\/2 = 1 thin 169 thin 280$ (the factor $1\/2$ because $S$ and its centralizer share $-1$, the factor 2 for the outer automorphism) #calc("C24"). (c) $S$ is the layer $E\("Aut"\(L_112\)\)$ (the product of the components), in particular normal, so #strong[$\|"Aut"\(L_112\)\|= 1 thin 169 thin 280$] #calc("C25") (Appendix F; it uses the classification of finite simple groups through the tables of Hiss–Malle \[HM01, HM02\] and the Schreier conjecture).
]

Let $G_112$ be the Gram matrix (3.1) of $L_112$.

#strong[Algorithm for (a) and (b).] An endomorphism of $V = L_112 times.o bb(Q)$ commuting with $S$ is a $2 times 2$ block matrix $X = mat(delim: "(", a, b; c, d)$ with $a\,b\,c\,d in M' times.o bb(Q)$ ($M' = "End"_S\(L_56\)$, 8-dimensional), so these form a 32-dimensional space. Those mapping $L_112$ into itself form a $bb(Z)$-lattice $cal(H)$ of rank 32, obtained exactly as the dual of the $bb(Z)$-span of the coefficient rows. On $cal(H)$ the form $Q\(X\)= "tr"\(G_112^(- 1) X G_112 X^(sans(T))\)$ is positive definite and equals $112$ on every isometry, so all isometries are among the finitely many $X in cal(H)$ with $Q\(X\)lt.eq 112$, which we enumerate (Fincke–Pohst, PARI) and test exactly. To guarantee that the enumeration is complete, including rounding errors, the same vectors are enumerated again with the interval-arithmetic enumerator of §6.1 (a), which cannot miss vectors, and the two lists agree #calc("C24"). For (b) we take the outer automorphism $alpha$ of $S$ from GAP and repeat this with the 8-dimensional space of maps $T$ on $L_56$ with $g T = T alpha\(g\)$.

#ptable(
  columns: 4, align: (left, left, left, left,),
  caption: [Table 10. Determination of $"Aut"\(L_112\)$.],
  table.header([Step], [Result], [Method], [Time]),
  [(a) centralizer], [$Q lt.eq 112$: 24 elements up to sign, all isometries; $\|C_("Aut"\(L_112\))\(S\)\|= 48$], [rank-32 lattice $cal(H)$, enumeration], [7 s],
  [(b) outer automorphism], [twisted intertwiners: 8-dimensional on $L_56$; 24 isometries up to sign], [GAP for $alpha$, then as in (a)], [11 min],
  [diagonal case (Appendix F.4)], [none of the 6 involutions $eq.not plus.minus 1$ of $C_("Aut"\(L_112\))\(S\)$ splits $S$], [integrality test], [10 s],
  [(c) normality], [$E\("Aut"\(L_112\)\)= S$], [Appendix F (proof)], [—],
)

The centralizer of order 48 is the unitary automorphism group of the rank-2 $M'$-lattice $Lambda={(a,b) in (M')^2:b equiv a tau med (mod 2M')}\/sqrt(2)$, with $L_112=L_56 times.o_(M') Lambda$. The subgroup $S dot.op C_("Aut"(L_112))(S)$ has order $584 thin 640$; the outer automorphism doubles this order. A matrix inducing the outer automorphism is supplied as #raw("certificates/outer_automorphism_L112.txt") #calc("C24", "C25").

#strong[Structure.] From explicit generators (those of $S$, the 48 elements of $C_("Aut"(L_112))(S)$, and one element inducing the outer automorphism), reduced modulo 3 (which is injective on a finite group of integer matrices), GAP finds a group of order exactly $1 thin 169 thin 280$ #calc("C26"), an independent check of the order. Moreover $C_("Aut"(L_112))(S) tilde.equiv "SL"_2(3) circle.small C_4$ (SmallGroup(48,33)), $"Aut"(L_112) \/ S tilde.equiv C_2 times S_4$, $"Aut"(L_112) \/ C_("Aut"(L_112))(S) tilde.equiv "PGL"_2(29)$, $Z("Aut"(L_112)) = {plus.minus 1}$, and the extension of the index-2 subgroup $S dot.op C_("Aut"(L_112))(S)$ does not split (the outer coset contains no involution) #calc("C26"). In short, $"Aut"(L_112) tilde.equiv ("SL"_2(29) circle.small "SL"_2(3) circle.small C_4) . 2$, central products over the common $-1$. All generators have determinant 1, and the endomorphisms of $L_112$ commuting with $"Aut"(L_112)$ form the ring $ZZ[sqrt(-29)]$; so $L_112$ is a Hermitian $ZZ[sqrt(-29)]$-lattice of rank 56 and $"Aut"(L_112) subset "U"(56) subset "SO"(112)$.

= 9. Authorship and use of AI <ai>

Direction, choice of problem, decisions, and responsibility for publication: roiban1344. Search strategy, code, computations, verification, and the initial draft: Claude (Anthropic), in several sessions that worked in parallel and checked each other's work with separately written code. The framework of gluing two lattices modulo 2 and reducing extremality to four collision types was first worked out, in dimension 96, by a session of OpenAI Codex. OpenAI Codex was used to restructure and revise the paper and supplement in response to the review. The author takes responsibility for the claims and for any errors.

= 10. References <refs>


#refs-list(
  [#strong[\[Asc00\]] M. Aschbacher, #emph[Finite Group Theory], 2nd ed., Cambridge Studies in Advanced Mathematics 10, Cambridge University Press, 2000.],
  [#strong[\[BN98\]] C. Bachoc, G. Nebe, Extremal lattices of minimum 8 related to the Mathieu group $M_22$, J. reine angew. Math. 494 (1998) 155–171.],
  [#strong[\[BV01\]] C. Bachoc, B. Venkov, Modular forms, lattices and spherical designs, in: Réseaux euclidiens, designs sphériques et formes modulaires, Monogr. Enseign. Math. 37 (2001).],
  [#strong[\[CN13\]] R. Coulangeon, G. Nebe, Dense lattices as Hermitian tensor products, Contemp. Math. 587 (2013); arXiv:1201.1832.],
  [#strong[\[Cou00\]] R. Coulangeon, Tensor products of Hermitian lattices, Acta Arith. 92 (2000) 115–130.],
  [#strong[\[FP85\]] U. Fincke, M. Pohst, Improved methods for calculating vectors of short length in a lattice, including a complexity analysis, Math. Comp. 44 (1985) 463–471.],
  [#strong[\[GHY01\]] W. T. Gan, J. P. Hanke, J.-K. Yu, On an exact mass formula of Shimura, Duke Math. J. 107 (2001) 103–133.],
  [#strong[\[HM01\]] G. Hiss, G. Malle, Low-dimensional representations of quasi-simple groups, LMS J. Comput. Math. 4 (2001) 22–63.],
  [#strong[\[HM02\]] G. Hiss, G. Malle, Corrigenda: Low-dimensional representations of quasi-simple groups, LMS J. Comput. Math. 5 (2002) 95–126.],
  [#strong[\[Kin03\]] O. King, A mass formula for unimodular lattices with no roots, Math. Comp. 72 (2003).],
  [#strong[\[MOS75\]] C. L. Mallows, A. M. Odlyzko, N. J. A. Sloane, Upper bounds for modular forms, lattices, and codes, J. Algebra 36 (1975) 68–76.],
  [#strong[\[Neb98\]] G. Nebe, Some cyclo-quaternionic lattices, J. Algebra 199 (1998) 472–498.],
  [#strong[\[Neb12\]] G. Nebe, An even unimodular 72-dimensional lattice of minimum 8, J. reine angew. Math. 673 (2012) 237–247; arXiv:1008.2862.],
  [#strong[\[Neb13\]] G. Nebe, On automorphisms of extremal even unimodular lattices, Int. J. Number Theory 9 (2013); arXiv:1212.0865.],
  [#strong[\[NS\]] G. Nebe, N. J. A. Sloane, A Catalogue of Lattices, entries #raw("L_56b"), #raw("L_56c"). #link("https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/")[Catalogue of Lattices].],
  [#strong[\[Que84\]] H.-G. Quebbemann, A construction of integral lattices, Mathematika 31 (1984) 137–140.],
  [#strong[\[Sak26\]] R. Sakamoto, Two extremal even unimodular lattices of rank 88, preprint (2026); arXiv:2609.15633.],
  [#strong[\[SE94\]] C. P. Schnorr, M. Euchner, Lattice basis reduction: improved practical algorithms and solving subset sum problems, Math. Program. 66 (1994) 181–199.],
  [#strong[\[Ser73\]] J.-P. Serre, #emph[A Course in Arithmetic], Graduate Texts in Mathematics 7, Springer, 1973, Chapter VII.],
  [#strong[\[SPLAG\]] J. H. Conway, N. J. A. Sloane, Sphere Packings, Lattices and Groups, 3rd ed., Springer 1999.],
  [#strong[\[SSP99\]] R. Scharlau, R. Schulze-Pillot, Extremal lattices, in: B. H. Matzat, G.-M. Greuel, G. Hiss (eds.), Algorithmic Algebra and Number Theory (Heidelberg, 1997), Springer 1999, 139–170.],
  [#strong[\[SW10\]] D. Stehlé, M. Watkins, On the extremality of an 80-dimensional lattice, ANTS-IX, LNCS 6197 (2010) 340–356.],
  [#strong[\[Wat12\]] M. Watkins, Another 80-dimensional extremal lattice, J. Théor. Nombres Bordeaux 24 (2012).],
  [#strong[\[Soft\]] The FPLLL development team, #emph[fplll, a lattice reduction library], version 5.5.0, #link("https://github.com/fplll/fplll")[source]; The PARI Group, #emph[PARI/GP], #link("https://pari.math.u-bordeaux.fr/")[website]; The GAP Group, #emph[GAP], #link("https://www.gap-system.org/")[website]; Lean and mathlib, #link("https://github.com/leanprover/lean4")[Lean source], #link("https://github.com/leanprover-community/mathlib4")[mathlib source].],
  [#strong[\[Repo\]] roiban1344, #emph[112-dimensional extremal even unimodular lattice] (data, the code that checks and produces the verification data, the verification data, the Lean formalization), #link("https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice")[public repository] (tag #raw("v2026-10-25")).],
)

= Appendix A. Glossary <appA>

#gloss(
  ([Coset; coset minimum $min\(c\)$], [An element $c = x + 2 L$ of $L\/2 L$, and the smallest norm of a vector in it. Even/odd according to $chevron.l x\,x chevron.r\/2 med mod med 2$ (§2.2).]),
  ([Gluing $L_f$], [The lattice ${ 1 / sqrt(2)\(x\,v\): v equiv x f }$ built from two copies of $L$ and an invertible parity-preserving $f$ (Definition 3.1). Our $L_112$ is $L_f$ with $f = tau med mod med 2$.]),
  ([Collision of type $\(a\,b\)$], [A pair $\(x\,v\)$ with $x$ of norm $a$ and $v$ of norm $b$ in the coset $x tau + 2 L$ (Definition 4.1). The inner-shell vectors of $L_112$ are exactly the collisions of type $\(6\,6\)\,\(6\,10\)\,\(10\,6\)\,\(8\,8\)$ (Lemma 4.2).]),
  ([Certificate (for a coset)], [A vector $w_0$ of a coset $c$ with norm 14 or 18 (odd coset) or 12, 16, 20 (even coset) and $\|chevron.l w_0\,u chevron.r\|lt.eq 6$ for all minimal vectors $u$; it guarantees $min\(c\)gt.eq 14$ (odd) or $min\(c\)gt.eq 12$ (even) (Corollaries 5.2, 5.3; Check 5.4).]),
  ([Canonical form; $K_8$], [$"can"\(c\)$ is the smallest 56-bit integer in the $"SL"_2\(29\)$-orbit of a coset $c$; $K_8$ is the set of canonical forms of cosets of norm-8 vectors. A coset contains a norm-8 vector iff its canonical form is in $K_8$ (Proposition 6.3).]),
  ([Orbit representative], [A vector $r_i$ or $x_i u$ selected from an $S$-orbit; not to be confused with the coset representative $w_0$ that certifies a bound (§§4.2, 5).]),
)

= Appendix B. Extremal theta series <appB>

#strong[Scope.] This appendix gives the sources of the numbers used in the text; all are exact rational computations. With $A = theta_(E_8) = E_4$ and $B = theta_(Lambda_24) = E_4^3 - 720 Delta$, by \[Ser73, Ch. VII\], every modular form of weight $4 k$ is a polynomial in $A$ and $B$, and the extremal theta series in dimension $n = 8 k$ is the unique one of the form $1 + O\(q^(floor.l n\/24 floor.r + 1)\)$.

#ptable(
  columns: 3, align: (left, left, left,),
  caption: [Table B1. Extremal theta series in dimensions 56 and 112.],
  table.header([$n$], [as a polynomial in $A\,B$], [first coefficients]),
  [56], [$1 / 240\(- 159 A^7 + 238 A^4 B + 161 A B^2\)$], [$1 + 15 thin 590 thin 400 q^3 + 36 thin 957 thin 286 thin 800 q^4 + 15 thin 284 thin 192 thin 071 thin 680 q^5 + dots.h.c$],
  [112], [$frac(1, 37 thin 324 thin 800)\(7 thin 883 thin 087 A^14 - 18 thin 165 thin 308 A^11 B - 38 thin 110 thin 758 A^8 B^2 + 74 thin 301 thin 892 A^5 B^3 + 11 thin 415 thin 887 A^2 B^4\)$], [$1 + 10 thin 888 thin 335 thin 360 q^5 + 247 thin 006 thin 775 thin 232 thin 000 q^6 + dots.h.c$],
)

= Appendix C. Proofs of auxiliary facts <appC>

== C.1 $tau$ is skew-adjoint and $h$ is Hermitian

From $tau G tau^(sans(T)) = 5 G$ and $tau^2 = - 5$ we get $G tau^(sans(T)) = 5 tau^(- 1) G = - tau G$, i.e. $chevron.l x tau\,y chevron.r = - chevron.l x\,y tau chevron.r$. With $h\(x\,y\)= chevron.l x\,y chevron.r + chevron.l x tau\,y chevron.r\/sqrt(- 5)$: $h\(x tau\,y\)= chevron.l x tau\,y chevron.r + chevron.l x tau^2\,y chevron.r\/sqrt(- 5) = chevron.l x tau\,y chevron.r + sqrt(- 5) chevron.l x\,y chevron.r = sqrt(- 5) thin h\(x\,y\)$, so $h$ is $cal(O)$-linear in the first variable; and $h\(y\,x\)= chevron.l x\,y chevron.r - chevron.l x tau\,y chevron.r\/sqrt(- 5) = overline(h\(x\,y\))$ because $overline(1\/sqrt(- 5)) = - 1\/sqrt(- 5)$. Clearly $"Re" h = chevron.l dot.op\,dot.op chevron.r$.

== C.2 Proof of Proposition 3.4

Since $H = cal(O) e_1 xor cal(O) e_2$ is free, every element of $H times.o_(cal(O)) P$ is uniquely $e_1 times.o x + e_2 times.o y$, and $phi$ is a bijection onto $L_tau$ (put $v = x tau + 2 y$). For the forms: $"Re"\(h_H\(e_1\,e_1\)h_P\(x\,x'\)\)= 3 chevron.l x\,x' chevron.r = 1 / 2\(chevron.l x\,x' chevron.r + chevron.l x tau\,x' tau chevron.r\)$; $"Re"\(h_H\(e_2\,e_2\)h_P\(y\,y'\)\)= 2 chevron.l y\,y' chevron.r = 1 / 2 chevron.l 2 y\,2 y' chevron.r$; and $"Re"\(sqrt(- 5) thin h_P\(x\,y'\)\)= "Re"\(sqrt(- 5) chevron.l x\,y' chevron.r + chevron.l x tau\,y' chevron.r\)= chevron.l x tau\,y' chevron.r = 1 / 2 chevron.l x tau\,2 y' chevron.r$. These are the inner products of $phi\(e_1 times.o x\)=\(x\,x tau\)\/sqrt(2)$ and $phi\(e_2 times.o y\)=\(0\,2 y\)\/sqrt(2)$, i.e. the blocks of (3.1).

== C.3 Injectivity of the coset map on short shells

If $w eq.not plus.minus w'$ have norm $m in { 6\,8 }$ and lie in the same coset, the midpoint lemma gives $2 m + 2 chevron.l w\,w' chevron.r gt.eq 24$ and $2 m - 2 chevron.l w\,w' chevron.r gt.eq 24$; adding them gives $4 m gt.eq 48$, which is false. So $L(6)\/{ plus.minus 1 } arrow.r L\/2 L$ and $L(8)\/{ plus.minus 1 } arrow.r L\/2 L$ are injective, with disjoint images (odd and even cosets respectively). Consequently an $S$-orbit of norm-8 vectors and its image in $L\/2 L$ have sizes in ratio $2 : 1$ ($- 1 in S$ acts trivially on $L\/2 L$), and since different canonical forms mean different orbits, $\|K_8\|$ equals the number of $S$-orbits.

== C.4 Reduction of $\(10\,6\)$ to $\(6\,10\)$

If $v equiv x tau$ then $v tau equiv x tau^2 = - 5 x equiv x med\(mod med 2 L\)$. So $\(x\,v\)$ is a collision of type $\(10\,6\)$ iff $\(v\,x\)$ is one of type $\(6\,10\)$.

== C.5 Orbit decomposition of $L_56(6)$

$632 dot.op 24 thin 360 + 24 dot.op 8 thin 120 = 15 thin 395 thin 520 + 194 thin 880 = 15 thin 590 thin 400$, and this is the only decomposition into 656 orbits with sizes in ${ 8 thin 120\,24 thin 360 }$ summing to $\|L_56(6)\|$.

= Appendix D. Data, formats and reproduction <appD>

#ptable(
  columns: 3, align: (left, left, left,),
  caption: [Table D1. Data files (as distributed in \[Repo\], #raw("data/")).],
  table.header([file], [content], [SHA-256 (prefix)]),
  [#raw("L56_gram.txt")], [Gram matrix $G$ of $L_56$ (56×56)], [#raw("4d13bd51…")],
  [#raw("sl2_29_generators.txt")], [$g_1\,g_2$ (orders 5, 7) generating $"SL"_2\(29\)$], [#raw("97f88443…")],
  [#raw("tau.txt")], [$tau$ (56×56), $tau^2 = - 5$], [#raw("30b6fa54…")],
  [#raw("L112_gram_LLL.txt")], [LLL-reduced Gram matrix of $L_112$ (112×112)], [#raw("104764e3…")],
)

#block(text(size: 0.85em, {set par(justify: false); [Full SHA-256 hashes:]; linebreak(); raw("4d13bd51fcf3cb8c5706bde45828713d7eeb4d18a37e8e9d84fb2700f4bef2f0"); linebreak(); raw("97f88443de1fd1fdeb010ecb668dbbb03a8e0e989a18c0ad85a751687012ad90"); linebreak(); raw("30b6fa54f7abc2938a8f5ce29237bb92a4224f5418d3cae85183c0a89803a0f1"); linebreak(); raw("104764e3c8add14d124c9e4ffd011e35d4d4659f4b6216651d278d76003bbfce")}))

#strong[Conventions.] Row vectors; a matrix $g$ acts by $x mapsto x g$; isometries satisfy $g G g^(sans(T)) = G$; $tau G tau^(sans(T)) = 5 G$. The file #raw("L112_gram_LLL.txt") is PARI's #raw("qflllgram") reduction of (3.1).

#strong[Specification without the files.] The defining matrices (56×56 and 112×112) are not printed in this paper; they are the files of Table D1. By §7.2, $L_56$ is $"SL"_2(29)$-equivariantly isometric to $L_(56,2)(tilde(M))$ of \[Neb98\], and in those coordinates $tau$ is right multiplication by an element of $tilde(M)$ of reduced norm 5 and reduced trace 0, given in §7.2. Together with (1.2), this specifies $L_112$ up to isometry independently of the data files. The files remain the reference: every verification program reads them and checks their hashes.

#strong[Intermediate data] (orbit representatives of $L_56(6)$ and $L_56(8)$, odd and even-coset certificates, witnesses of norm 8 for B) are distributed as verification data in #raw("certificates/") of \[Repo\]; their SHA-256 hashes are listed in #raw("certificates/SHA256SUMS").

#strong[Elementary checks] (a few seconds in any computer algebra system): (3.1) has even diagonal and determinant 1; $tau^2 = - 5$, $tau G tau^(sans(T)) = 5 G$; $g_i G g_i^(sans(T)) = G$, $g_i tau = tau g_i$. Checking one odd-coset certificate: (a) $w_0 - r tau$ has even coordinates, (b) $chevron.l w_0\,w_0 chevron.r in { 14\,18 }$, (c) $\|chevron.l w_0\,r' g chevron.r\|lt.eq 6$ for all 656 representatives $r'$ and all $12 thin 180$ elements $g$.

#strong[Code.] Every computation used in this paper is listed in Table D2 with the code that performs it; except for supplementary computations explicitly marked unpublished, the paths in Table D2 are those of the public repository \[Repo\]. The text refers to the rows of Table D2 as \[C1\], \[C2\], ….

Checking the computational facts from the supplied data takes about 1.2 CPU hours by the fastest route (route A of Supplement Table S7; the script #raw("code/verify/proof.sh")). Alternative routes and additional tests are described in Supplement §S3.

#calc-table(lang: "en")

= Appendix E. Pseudocode <appE>

```
MINIMAL-ORBITS(L, S):
  candidates <- initial minimal vectors; reps <- []; seen <- {}; total <- 0
  while total < 15590400:
    r <- a candidate outside seen; O <- {r*g : g in S}
    append r to reps; seen <- seen union O; total <- total + size(O)
    for s in O with <r,s> = 3: add r-s to candidates
    if no unused candidates remain: enlarge the initial candidate list
  check distinct orbits and total = 15590400
  return reps

NORM8-ORBITS(L, S_star, minimal_reps):
  for r_i in minimal_reps and s in L(6) with <r_i,s> = -2:
    x <- r_i+s
    if x is marked: continue
    find and mark all marked elements of x*S_star using <x*u,r_j*g> = +/-4
    record x and size(S_star)/size(stabilizer(x))
  check distinct orbits and total orbit size = 36957286800

CANONICAL(c, S):
  return min { pack56(c*g mod 2) : g in S/{+1,-1} }

TEST88(pairs, K8, tau):
  for (x_i,u) in pairs:
    if CANONICAL(x_i*u*tau, S) in K8: report collision

COSET-REPRESENTATIVE(w):
  repeat:
    m <- max { <w,u> : u in L(6) }
    if m <= 6: return w
    choose u with <w,u> = m; w <- w-2*u
  # Check 5.4 also verifies parity and the allowed final norm.
```

= Appendix F. Proof that $"SL"_2\(29\)$ is normal in $"Aut"\(L_112\)$ <appF>

Write $A = "Aut"\(L_112\)$, $S tilde.equiv "SL"_2\(29\)$, $V = L_112 times.o bb(Q)$, so $V\|_S tilde.equiv V_0^2$ with $V_0 = L_56 times.o bb(Q)$ irreducible of dimension 56 and $V times.o bb(C)\|_S = 4 psi + 4 psi'$, where $psi\,psi'$ are the two faithful characters of degree 14. The generalized Fitting subgroup $F^(*)\(A\)= F\(A\)E\(A\)$ satisfies $C_A\(F^(*)\(A\)\)lt.eq F^(*)\(A\)$ (Bender). We show (F.1) that every normal subgroup of $A$ has at most two isotypic components on $V$; (F.2, F.3) that $F\(A\)$ centralizes $S$; and (F.4) that $E\(A\)= S$. Sakamoto \[Sak26, App. A\] used primitivity of the action, which fails here (there are two isotypic components a priori); F.1 replaces it, and F.3 replaces the use of “normal abelian subgroups are cyclic” by a character-degree argument. The finite facts G-F1–G-F5 below were checked with GAP #calc("C25").

#strong[Finite facts.] G-F1: the proper subgroups of $"PSL"_2\(29\)$ of index $lt.eq 112$ are $29 : 14$ (index 30) and $29 : 7$ (index 60). G-F2: every proper subgroup of $"SL"_2\(29\)$ has index $gt.eq 30$. G-F3: the irreducible characters of the preimages in $S$ of $29 : 14$, $29 : 7$ have degrees $1\,14$ and $1\,7$; $psi\,psi'$ restricted to a subgroup $U$ of order 29 do not contain the trivial character. G-F4: the only maximal subgroup of $"Ru"$ of order divisible by 29 is $L_2\(29\)$; both characters of degree 28 of $2 . "Ru"$ restrict irreducibly to $2 . L_2\(29\)$, for each of the 6 possible class fusions. G-F5: $\|"SL"_2\(29\)\|$ divides neither $\|"SL"_2\(59\)\|$ nor $\|"SL"_2\(173\)\|$.

== F.1 At most two isotypic components

Let $N lt.tri.eq A$ and let $V_1\,dots.h\,V_b$ be the isotypic components of $V\|_N$ over $bb(Q)$. $A$ permutes them (Clifford), hence so does $S$, through $"PSL"_2\(29\)$ since $- 1$ is scalar. If the permutation action were nontrivial, a nontrivial orbit would have a stabilizer of index $lt.eq 112$, so of index 30 or 60 (G-F1), and its components would have dimension $lt.eq 3$. The sum of the orbit would be induced from a representation $theta$ of dimension $lt.eq 3$ of the preimage $J$ of the stabilizer; by G-F3, $theta$ is a sum of linear characters, trivial on $U lt.eq\[J\,J\]$. A common constituent of $theta$ and $psi\|_J$ would give a trivial constituent of $psi\|_U$, contradicting G-F3; so by Frobenius reciprocity $"Ind"_J^S theta$ contains neither $psi$ nor $psi'$, which is impossible inside $V\|_S$. Hence $S$ fixes every $V_i$, each $V_i$ is an $S$-submodule of $V_0^2$ of dimension 56 or 112, and #strong[$b lt.eq 2$].

== F.2 Odd primes

Let $P_0 lt.tri.eq A$ be a $p$-group, $p$ odd, with kernel $K_j$ on $V_j$. $P_0\/K_j$ has a faithful irreducible rational representation $U_j$; for a constituent $chi$ of $U_j times.o bb(C)$, $dim U_j =\[bb(Q)\(chi\): bb(Q)\]chi\(1\)$ (Schur index 1, Roquette), and $bb(Q)\(chi\)supset.eq bb(Q)\(zeta_(p^f)\)$ because $Z\(P_0\/K_j\)tilde.equiv C_(p^f)$ ($f gt.eq 1$) acts through a faithful linear character. So $dim U_j =\(p - 1\)p^e chi\(1\)$ divides 56 or 112, which forces $p^e chi\(1\)= 1$ and $p - 1 divides 112$, i.e. $p in { 3\,5\,17\,29\,113 }$ and $P_0\/K_j tilde.equiv C_p$. Thus $P_0 arrow.r.hook C_p times C_p$. For $p eq.not 29$, $29 divides.not\|"GL"_2\(p\)\|$, so the perfect group $S$ acts trivially on $P_0$. For $p = 29$: if $P_0$ is cyclic, $"Aut"\(P_0\)$ is abelian; if $P_0 tilde.equiv C_29^2$ then $b = 2$ and $S$ fixes $K_1$ and $K_2$ (F.1), so its image in $"GL"_2\(29\)$ lies in a split torus, which is abelian. In all cases $\[P_0\,S\]= 1$.

== F.3 The prime 2

Let $P = O_2\(A\)$. $S$ is generated by its elements of order 29, so it suffices to show that such an element $y$ centralizes $P$. Let $D_0$ be a critical subgroup of $P$ in the sense of Thompson: $D_0$ is characteristic in $P$, of class $lt.eq 2$, and every nontrivial automorphism of $P$ of odd order acts nontrivially on $D_0$. Since $D_0 lt.tri.eq A$, F.1 applies: $V\|_(D_0)$ has isotypic components $V_1$ (and $V_2$), fixed by $y$; let $K_j$ be the kernel on $V_j$, so $K_1 inter K_2 = 1$ and $y$ acts on $Q_j = D_0\/K_j$. A constituent $chi$ of $V_j times.o bb(C)$ is a faithful irreducible character of $Q_j$ (Galois conjugates have the same kernel) with $chi\(1\)lt.eq 112$.

#emph[Lemma.] If $Q$ has class $lt.eq 2$ and $chi in "Irr"\(Q\)$ is faithful, then $chi\(1\)^2 =\|Q : Z\(Q\)\|$. #emph[Proof.] For $g in.not Z\(Q\)$ pick $h$ with $z =\[g\,h\]eq.not 1$; $z in Z\(Q\)$ acts as a scalar $lambda\(z\)eq.not 1$, and $chi\(g\)= chi\(h^(- 1) g h\)= chi\(g z\)= lambda\(z\)chi\(g\)$, so $chi\(g\)= 0$. The orthogonality relation $sum_g\|chi\(g\)\|^2 =\|Q\|$ gives $chi\(1\)^2\|Z\(Q\)\|=\|Q\|$. ∎

Hence $\|Q_j : Z\(Q_j\)\|lt.eq 112^2 < 2^14$, and $Z\(Q_j\)$ is cyclic. The element $y$ acts trivially on $Z\(Q_j\)$ (the automorphism group of a cyclic 2-group is a 2-group) and on the abelian group $Q_j\/Z\(Q_j\)$: otherwise it would act nontrivially on its Frattini quotient (Burnside), an $bb(F)_2$-space of dimension $lt.eq 13$, whereas nontrivial irreducible $bb(F)_2\[C_29\]$-modules have dimension 28 (the order of 2 modulo 29). Writing $x^y = x thin zeta\(x\)$ with $zeta : Q_j arrow.r Z\(Q_j\)$ a homomorphism, $x = x^(y^29) = x thin zeta\(x\)^29$ forces $zeta = 1$. So $\[D_0\,y\]lt.eq K_1 inter K_2 = 1$, and by the property of $D_0$, $y$ centralizes $P$.

== F.4 The layer

By F.2–F.3, $F\(A\)lt.eq C_A\(S\)$. Let $E\(A\)= Q_1 dots.h.c Q_r$ be the product of the components (commuting quasisimple subnormal subgroups).

(a) #emph[$S$ normalizes every $Q_i$.] By F.1 for $E\(A\)$, $V\|_(E\(A\))$ has at most two isotypic components; the complex constituents of the $j$-th are Galois conjugates of $X_j = times.o.big_i X_(j\,i)$. Each $Q_i$ acts nontrivially, nontrivial irreducible representations of quasisimple groups have degree $gt.eq 2$, and $2^7 > 112$, so at most 6 of the $Q_i$ act nontrivially on each of the at most two components; hence $r lt.eq 12$. By G-F2, $S$ cannot permute the $Q_i$ nontrivially.

(b) #emph[$S$ induces inner automorphisms on each $Q_i$.] By the Schreier conjecture, a consequence of the classification theorem, the outer automorphism group of the simple group $Q_i/Z(Q_i)$ is solvable. Automorphisms of a quasisimple group act faithfully on its central quotient, so $"Out"(Q_i)$ is solvable as well. Since $S$ is perfect, its image in $"Out"(Q_i)$ is trivial. Thus $S lt.eq E(A)C_A(E(A))$.

(b′) #emph[$S lt.eq E\(A\)$.] Put $T = S E\(A\)inter C_A\(E\(A\)\)$; then $S E\(A\)= E\(A\)T$ and $T\/Z\(E\(A\)\)tilde.equiv S E\(A\)\/E\(A\)$ is perfect. As $S$ and $E\(A\)$ centralize $F\(A\)$, $T lt.eq C_A\(F^(*)\(A\)\)lt.eq Z\(F^(*)\(A\)\)$ is abelian. So $T lt.eq E\(A\)$ and $S lt.eq E\(A\)$.

(c) #emph[$S$ lies in a single component.] Let $I$ be the set of $i$ for which the projection of $S$ to $Q_i\/Z\(Q_i\)$ is nontrivial. For $i in I$, $Q_i$ contains a quotient of $"SL"_2\(29\)$, so its nontrivial irreducible representations have degree $gt.eq 14$; as $14^2 > 112$, each $X_j$ involves at most one $i in I$, so $\|I\|lt.eq 2$. If $\|I\|= 2$, then $b = 2$, $Q_1$ acts only on $V_1$ and $Q_2$ only on $V_2$; writing $s = z q_1 q_2$ ($z in Z\(E\(A\)\)$, $q_i in Q_i$) gives $\[s\,t\]=\[q_1\,q'_1\]\[q_2\,q'_2\]$ with $\[q_1\,q'_1\]in A$ acting as $\[s\,t\]$ on $V_1$ and trivially on $V_2$. Since $S$ is perfect, $s mapsto\(s\|_(V_1)\,"id"_(V_2)\)$ maps $S$ into $A$; the image $c$ of $- 1$ is an involution in $C_A\(S\)$ for which $g mapsto frac(1 - c, 2) g + frac(1 + c, 2)$ preserves $L_112$. A direct check of the 6 involutions $eq.not plus.minus 1$ of the group of order 48 (Theorem B(a)) shows that none does #calc("C25"). So $\|I\|= 1$ and $S =\[S\,S\]lt.eq\[Q_1\,Q_1\]= Q_1$.

(d) #emph[$E\(A\)= Q_1$.] Any other component centralizes $Q_1 supset.eq S$ and hence lies in $C_A\(S\)$ of order 48; but quasisimple groups have order $gt.eq 60$.

(e) #emph[$Q_1 = S$.] Let $X$ be a constituent of $V times.o bb(C)\|_(Q_1)$. Since $- 1 in S$ acts as $- 1$, $macron(Q) = Q_1\/ker X$ is quasisimple with center of even order, contains $S$ faithfully, and $X$ is a faithful irreducible representation of degree $lt.eq 112$ whose restriction to $S$ is a sum of $psi\,psi'$. By the main theorem of \[HM01\] (with the corrigenda \[HM02\]), such a $macron(Q)$ in characteristic 0 with $29 divides\|macron(Q)\|$ is one of the following. From \[HM01, Table 3\], only $"Ru"$, $2 . "Ru"$, $J_4$ have order divisible by 29 (we checked the orders of all simple groups occurring in rows of degree $lt.eq 112$), and only $2 . "Ru"$ (degree 28) occurs in characteristic 0 with even center. From \[HM01, Table 2\], $A_n$ has trivial center, and $2 . L_2\(q\)$ with $29 divides q\(q^2 - 1\)$ and minimal degree $\(q minus.plus 1\)\/2 lt.eq 112$ gives $q in { 29\,59\,173 }$, of which $59$ and $173$ are excluded by G-F5. If $S lt.eq 2 . "Ru"$, the image of $S$ lies in the maximal subgroup $L_2\(29\)$ (G-F4), so $S = 2 . L_2\(29\)$, and $X\|_S$ would be irreducible of degree 28 (G-F4), not a sum of characters of degree 14. Hence $macron(Q) tilde.equiv "SL"_2\(29\)$, $Q_1 = S ker X$ with $ker X$ central, and $Q_1 =\[Q_1\,Q_1\]= S$.

Thus $E\(A\)= S$, which is characteristic in $A$; so $S lt.tri.eq A$, $A = N_A\(S\)$ and $\|A\|= 1 thin 169 thin 280$ by Theorem B(b).  #qed

#small[#strong[What the proof relies on.] The finite computations G-F1–G-F5, Theorem B(a), (b) and the diagonal check #calc("C25") (reproducible in minutes); the main theorem of Hiss–Malle (whose tables were scanned mechanically for all rows of degree $lt.eq 112$); standard textbook facts of finite group theory (Bender, Thompson's critical subgroup, Burnside, Clifford, Roquette).]



For the standard finite-group results on generalized Fitting subgroups, critical subgroups and Clifford theory, see \[Asc00\].

= Appendix G. Comparison with known constructions <appG>

#ptable(
  columns: 4, align: (left, center, left, left,),
  caption: [Table G1. Selected constructions and counting results for extremal even unimodular lattices; historical sources are \[Sak26, §1\] and \[NS\].],
  table.header([dimension $n$], [$mu\(n\)$], [examples or counting results], [sources]),
  [8], [2], [$E_8$ (unique)], [classical],
  [16], [2], [$E_8 perp E_8$, $D_16^(+)$ (all)], [classical],
  [24], [4], [Leech lattice (unique)], [\[SPLAG\]],
  [32], [4], [more than $10^7$], [mass formula by root system \[Kin03, Cor. 5\]],
  [40], [4], [more than $10^51$], [mass formula and Siegel's theorem \[SSP99\]; \[Sak26, §1\]],
  [48], [6], [at least 4], [\[Sak26, §1\]; \[NS\]],
  [56], [6], [Nebe’s constructions \[Neb98\]], [\[Sak26, §1\]; \[NS\]; \[Neb98\]],
  [64], [6], [constructions of Quebbemann and Shimada], [\[Que84\]; \[Sak26, §1\]; \[NS\]],
  [72], [8], [at least 1 ($Gamma_72$)], [Nebe 2010 \[Neb12\]],
  [80], [8], [at least 4], [Bachoc–Nebe 1998 \[BN98\]; \[SW10\]; \[Wat12\]],
  [88], [8], [at least 2], [Sakamoto 2026 \[Sak26\] (preprint)],
  [96], [10], [none known], [open],
  [104], [10], [none known], [open],
  [#strong[112]], [#strong[10]], [#strong[$L_112$ (this paper)]], [this paper],
  [120], [12], [none known], [open],
)
