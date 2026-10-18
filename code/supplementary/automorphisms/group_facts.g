# S10a. Finite group facts G-F1–G-F5 used in Appendix F (normality of SL_2(29) in Aut(L_112)); Table D2 [C25].
#   Not used in the proof of Theorem A. Requires GAP 4 with the character table library CTblLib.
#   付録 F（Aut(L_112) における SL_2(29) の正規性）で使う有限群の事実 G-F1〜G-F5。表 D2 の [C25]。定理 A の証明には使わない。
#   GAP 4 と指標表ライブラリ CTblLib が要る。
# Run / 実行:  gap -q --quitonbreak code/supplementary/automorphisms/group_facts.g < /dev/null
#   Each value is compared with the one stated in the paper (Appendix F); the script ends with exit code 1 if any
#   differs and with a nonzero code on a GAP error, otherwise 0.
#   各値を論文（付録 F）に書かれた値と比べる。一つでも違えば終了コード 1、GAP のエラーでは非 0、それ以外は 0 で終わる。
# (G-F1) orders of the proper subgroups of PSL_2(29) of index <= 112 (expected: 29:14 and 29:7 only)
#      指数 112 以下の PSL_2(29) の真部分群の位数（29:14 と 29:7 だけのはず）
# (G-F2) minimal index of a proper subgroup of SL_2(29) (expected 30) / SL_2(29) の真部分群の指数の最小（30 のはず）
# (G-F3) character degrees of the preimages of 29:14 and 29:7 in SL_2(29), and the multiplicity of the
#      trivial character of a subgroup of order 29 in the faithful degree-14 characters (expected 0)
#      29:14, 29:7 の逆像の既約指標の次数と、14 次の忠実な指標を位数 29 の部分群に制限したときの自明指標の重複度（0 のはず）
# (G-F4) maximal subgroups of Ru of order divisible by 29 (expected L2(29) only); restriction of the
#      degree-28 characters of 2.Ru to 2.L2(29) over all possible class fusions (irreducible)
#      位数が 29 で割れる Ru の極大部分群（L2(29) だけのはず）。2.Ru の 28 次の指標の 2.L2(29) への制限（可能な融合写像すべてで既約）
# (G-F5) |SL_2(59)| and |SL_2(173)| are not divisible by |SL_2(29)| / |SL_2(29)| で割り切れないこと
OnBreak := function() Print("FAIL: GAP error (see above)\n"); QuitGap(2); end;;   # also without --quitonbreak / --quitonbreak が無くても止める
nfail := 0;;
Expect := function(label, got, expected)   # compare with the value in the paper / 論文の値と比べる
  if got = expected then Print("  [ok] ", label, "\n");
  else Print("  [FAIL] ", label, ": got ", got, ", expected ", expected, "\n"); nfail := nfail + 1; fi;
end;;
P := PSL(2, 29);;
cls := ConjugacyClassesSubgroups(P);;
small := Filtered(cls, c -> Index(P, Representative(c)) <= 112 and Index(P, Representative(c)) > 1);;
Print("G-F1: proper subgroups of PSL(2,29) of index <= 112 (order, index, #classes): ",
      Collected(List(small, c -> [Size(Representative(c)), Index(P, Representative(c))])), "\n");
Expect("G-F1: only 29:14 (index 30) and 29:7 (index 60)",
       Collected(List(small, c -> [Size(Representative(c)), Index(P, Representative(c))])), [[[203, 60], 1], [[406, 30], 1]]);
S := SL(2, 29);;
clsS := ConjugacyClassesSubgroups(S);;
Print("G-F2: minimal index of a proper subgroup of SL(2,29): ",
      Minimum(List(Filtered(clsS, c -> Size(Representative(c)) < Size(S)), c -> Index(S, Representative(c)))), "\n");
Expect("G-F2: minimal index 30", Minimum(List(Filtered(clsS, c -> Size(Representative(c)) < Size(S)), c -> Index(S, Representative(c)))), 30);
tS := CharacterTable(S);;
psi := Filtered(Irr(tS), x -> x[1] = 14);;
Print("G-F3: number of degree-14 irreducible characters of SL(2,29): ", Length(psi),
      "; faithful (value -14 at -1): ", Number(psi, x -> x[PositionProperty(ConjugacyClasses(tS), c -> Representative(c) = -One(S))] = -14), "\n");
Expect("G-F3: two degree-14 irreducibles psi, psi', both faithful",
       [Length(psi), Number(psi, x -> x[PositionProperty(ConjugacyClasses(tS), c -> Representative(c) = -One(S))] = -14)], [2, 2]);
U := SylowSubgroup(S, 29);;
for c in small do
  H := PreImage(NaturalHomomorphismByNormalSubgroup(S, Centre(S)), Representative(c));
  Print("G-F3: preimage of order ", Size(H), " contains a Sylow 29-subgroup: ", ForAny(ConjugacyClassesSubgroups(H), d -> Size(Representative(d)) = 29),
        "; degrees of Irr: ", Collected(List(Irr(CharacterTable(H)), x -> x[1])), "\n");
  # preimage of 29:14 (order 812): degrees 1, 14; of 29:7 (order 406): degrees 1, 7 / 29:14 の逆像は 1, 14、29:7 の逆像は 1, 7
  Expect(Concatenation("G-F3: degrees of Irr of the preimage of order ", String(Size(H))),
         [Size(H) in [406, 812], ForAny(ConjugacyClassesSubgroups(H), d -> Size(Representative(d)) = 29),
          Set(List(Irr(CharacterTable(H)), x -> x[1]))], [true, true, [1, Size(H) / 58]]);
od;
tU := CharacterTable(U);;
Print("G-F3: multiplicity of the trivial character of a 29-subgroup in each degree-14 character: ",
      List(psi, x -> ScalarProduct(tU, RestrictedClassFunction(x, U), TrivialCharacter(tU))), "\n");
Expect("G-F3: psi, psi' restricted to U contain no trivial character",
       List(psi, x -> ScalarProduct(tU, RestrictedClassFunction(x, U), TrivialCharacter(tU))), [0, 0]);
ru := CharacterTable("Ru");;
mx := Maxes(ru);;
Print("G-F4: maximal subgroups of Ru with order divisible by 29: ", Filtered(mx, n -> Size(CharacterTable(n)) mod 29 = 0),
      " (out of ", Length(mx), ")\n");
Expect("G-F4: L2(29) is the only maximal subgroup of Ru of order divisible by 29",
       Filtered(mx, n -> Size(CharacterTable(n)) mod 29 = 0), ["L2(29)"]);
t2 := CharacterTable("2.Ru");;
t2l := CharacterTable("2.L2(29)");;
fusions := PossibleClassFusions(t2l, t2);;           # try all possible fusions, not the stored one / 保存された融合写像に頼らず、可能な融合写像をすべて試す
chi28 := Filtered(Irr(t2), x -> x[1] = 28);;
Print("G-F4: degree-28 characters of 2.Ru: ", Length(chi28), "; number of possible class fusions 2.L2(29) -> 2.Ru: ", Length(fusions), "\n");
Expect("G-F4: two degree-28 characters of 2.Ru and 6 possible class fusions", [Length(chi28), Length(fusions)], [2, 6]);
Print("G-F4: restrictions to 2.L2(29), as lists of [degree, multiplicity], over all possible fusions: ",
      Set(fusions, fus -> List(chi28, x -> List(Filtered(Irr(t2l), y -> ScalarProduct(t2l, x{fus}, y) <> 0), y -> [y[1], ScalarProduct(t2l, x{fus}, y)]))), "\n");
Expect("G-F4: both restrict irreducibly to 2.L2(29) for every possible fusion",
       Set(fusions, fus -> List(chi28, x -> List(Filtered(Irr(t2l), y -> ScalarProduct(t2l, x{fus}, y) <> 0), y -> [y[1], ScalarProduct(t2l, x{fus}, y)]))),
       [[[[28, 1]], [[28, 1]]]]);
Print("G-F5: |SL(2,59)| / |SL(2,29)| = ", Size(SL(2,59)) / Size(S), ", |SL(2,173)| / |SL(2,29)| = ", Size(SL(2,173)) / Size(S), "\n");
Expect("G-F5: |SL(2,29)| divides neither |SL(2,59)| nor |SL(2,173)|",
       [IsInt(Size(SL(2,59)) / Size(S)), IsInt(Size(SL(2,173)) / Size(S))], [false, false]);
if nfail > 0 then Print("RESULT: FAIL (", nfail, " mismatches)\n"); QuitGap(1); fi;
Print("RESULT: PASS (G-F1 to G-F5 agree with Appendix F)\n");
QuitGap(0);
