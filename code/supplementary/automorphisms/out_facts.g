# S10b. Finite group facts G-F6–G-F12: an additional check that carries the layer argument of Appendix F.4 without
#   the Schreier conjecture (29 does not divide |Out(T)| for the simple groups T of the Hiss-Malle tables); Table D2 [C25].
#   The proof in the paper uses the Schreier conjecture and needs only G-F1–G-F5 (group_facts.g). Not used in the
#   proof of Theorem A. Requires GAP 4 with CTblLib.
#   付録 F.4 の層の議論を Schreier 予想なしで通すための追加の検査、有限群の事実 G-F6〜G-F12（Hiss-Malle の表の単純群 T について 29 は |Out(T)| を割らない）。
#   論文の証明は Schreier 予想を使い、必要なのは G-F1〜G-F5（group_facts.g）だけ。表 D2 の [C25]。定理 A の証明には使わない。GAP 4 と CTblLib が要る。
# Run / 実行:  gap -q --quitonbreak code/supplementary/automorphisms/out_facts.g < /dev/null
#   Each value is compared with the one stated below (and, for the groups with 29 | |T|, with Appendix F.4 (e));
#   the script ends with exit code 1 if any differs and with a nonzero code on a GAP error, otherwise 0.
#   各値を下に書いた値（29 | |T| の群については付録 F.4 (e)）と比べる。一つでも違えば終了コード 1、GAP のエラーでは非 0、それ以外は 0 で終わる。
#
# G-F6 (groups with 29 not dividing |T|): an automorphism alpha of order 29 has an alpha-invariant Sylow
#   p-subgroup P for each p (the number of Sylow subgroups divides |T|, prime to 29); if alpha != 1 it
#   acts nontrivially on the Frattini quotient of some P (dimension d(P) <= a_p), so d(P) >= ord_29(p).
#   Hence if a_p < ord_29(p) for all p, T has no automorphism of order 29. Cases of equality are listed.
#   G-F6（29 ∤ |T| の群）: 位数 29 の自己同型 alpha は各 p について alpha-不変な Sylow p-部分群 P をもつ（Sylow の個数は |T| を割るので 29 と素）。
#   alpha ≠ 1 ならある P の Frattini 商（次元 d(P) ≤ a_p）に非自明に働くので d(P) ≥ ord_29(p)。よってすべての p で a_p < ord_29(p) なら
#   T は位数 29 の自己同型をもたない。等号の場合は列挙して個別に扱う。
# G-F7: |Aut(PSL_2(p))| = 2 |PSL_2(p)| for p = 29, 59, 173.
# G-F8 (Ru): centralizer orders of elements of order 29 (gives |N_Ru(P)| = 406). The congruence of element
#   counts modulo 29 is recorded only to show that it cannot exclude anything (both sides vanish).
#   G-F8（Ru）: 位数 29 の元の中心化群の位数（|N_Ru(P)| = 406）。元の個数の 29 を法とした比較は、何も排除できない（両辺とも 0）ことの記録。
# G-F9: U8(2) = SU8(2) contains SU4(2), whose Sylow 2-subgroup is not abelian.
#   U8(2) は SU4(2) を含み、その Sylow 2-部分群は可換でない。
# G-F10: the nontrivial irreducible characters of Ru have degree > 112; the faithful irreducible characters of
#   2.Ru of degree <= 112 are two of degree 28 with field of values Q(i).
#   Ru の非自明な既約指標の次数は 112 を超える。2.Ru の次数 112 以下の忠実な既約指標は 28 次の 2 つで、値の体は Q(i)。
# G-F11: every degree-28 irreducible character of SL_2(29) restricts to the Borel subgroup (order 812) as a
#   sum of two different degree-14 irreducibles.
#   SL_2(29) の 28 次の既約指標はどれも、Borel 部分群（位数 812）への制限が異なる 14 次の既約指標 2 つの和。
# G-F12: 2.Ru has no subgroup isomorphic to 2 x L2(29) (no possible class fusion), so the preimage of L2(29)
#   is SL_2(29).
#   2.Ru は 2 × L2(29) と同型な部分群をもたない（可能な融合写像が 0 個）。よって L2(29) の逆像は SL_2(29)。
OnBreak := function() Print("FAIL: GAP error (see above)\n"); QuitGap(2); end;;   # also without --quitonbreak / --quitonbreak が無くても止める
nfail := 0;;
Expect := function(label, got, expected)   # compare with the stated value / 記載の値と比べる
  if got = expected then Print("  [ok] ", label, "\n");
  else Print("  [FAIL] ", label, ": got ", got, ", expected ", expected, "\n"); nfail := nfail + 1; fi;
end;;
ord29 := p -> OrderMod(p, 29);
test := function(name, order)
  local bad, p, a;
  if order mod 29 = 0 then return [name, "29 divides |T|"]; fi;
  bad := [];
  for p in Set(Factors(order)) do
    a := Number(Factors(order), x -> x = p);
    if a >= ord29(p) then Add(bad, [p, a, ord29(p)]); fi;
  od;
  return [name, bad];
end;
res := [];
# Simple groups occurring in rows of degree <= 112 of Hiss-Malle Table 3 (CTblLib names; extracted mechanically from the
#   table, plus L3(3) from the corrigenda). Ru (degree 28) and J4 (degree 112, characteristic 2) are the
#   ones with 29 | |T|; they are listed so that the output matches Appendix F.4 (e).
#   Completeness of the list (checked 2026-10-18 against the text of both tables): the rows of degree <= 112 of
#   Table 3 of [HM01] contain 77 simple groups (the central extension, e.g. "2." or "3_1.", removed), Table 3 of
#   the corrigenda [HM02] the same 77 and L3(3), 78 in all. They are exactly the 75 names below and the 3 groups
#   after them (S4(11), S4(13), U8(2)), with no group missing or extra. (The list of the research computation
#   omitted Ru and J4 because it was used only for the groups with 29 not dividing |T|.)
# Hiss–Malle 表 3 の次数 ≤ 112 の行に現れる単純群（CTblLib の名前。表を機械的に抜き出したもの + 正誤表の L3(3)）。
#   Ru（28 次）と J4（標数 2 の 112 次）は 29 | |T| となる群であり、出力が付録 F.4 (e) と対応するように一覧に含める。
#   一覧が漏れなく正しいこと（2026-10-18 に両方の表のテキストと照合した）: [HM01] の表 3 の次数 112 以下の行には、中心拡大（「2.」「3_1.」など）を
#   外すと 77 個の単純群があり、正誤表 [HM02] の表 3 には同じ 77 個と L3(3) の計 78 個がある。これは下の 75 個の名前と、その後の
#   3 つ（S4(11)、S4(13)、U8(2)）にちょうど一致し、過不足は無い（研究時の計算の一覧に Ru と J4 が無かったのは、29 が |T| を割らない
#   群だけに使っていたため）。
names := ["M22","L3(4)","U4(3)","2F4(2)'","A10","A11","A12","A13","A14","A15","A16","A17","A6","A7","A8","A9","Co1","Co2","Co3","Fi22","F4(2)","G2(4)","G2(3)","HS","J1","J2","J3","L4(3)","M12","O8+(2)","O8-(2)","S4(5)","S4(7)","S4(9)","S4(4)","S6(2)","S6(3)","S6(5)","S8(3)","S8(2)","Suz","Sz(8)","U4(2)","U4(5)","U6(2)","3D4(2)","L3(7)","McL","O7(3)","ON","U3(11)","U3(5)","U3(8)","U3(3)","U3(4)","U3(7)","U3(9)","U4(4)","U5(2)","U5(3)","U7(2)","L3(5)","L3(8)","L3(9)","L4(4)","L5(2)","L6(2)","Ly","He","M11","M23","M24","L3(3)","Ru","J4"];
for n in names do Add(res, test(n, Size(CharacterTable(n)))); od;
# CTblLib に無い 3 つは位数の公式で
Add(res, test("S4(11)", 11^4*(11^2-1)*(11^4-1)/2));
Add(res, test("S4(13)", 13^4*(13^2-1)*(13^4-1)/2));
Add(res, test("U8(2)", 2^28*Product([2..8], i -> 2^i - (-1)^i)/Gcd(8, 3)));
# 表 2 の系列: A_n（5 ≤ n ≤ 28; n ≥ 29 は 29 | |A_n|）、L_2(q)（4 ≤ q ≤ 225 の素数冪。次数 (q-1)/2 ≤ 112）
for n in [5..28] do Add(res, test(Concatenation("A", String(n)), Factorial(n)/2)); od;
for q in Filtered([4..225], IsPrimePowerInt) do
  Add(res, test(Concatenation("L2(", String(q), ")"), q*(q^2-1)/Gcd(2, q-1)));
od;
Print("G-F6: groups tested: ", Length(res), "\n");
Print("G-F6: groups with 29 | |T| (treated separately): ", List(Filtered(res, r -> r[2] = "29 divides |T|"), r -> r[1]), "\n");
Print("G-F6: groups failing a_p < ord_29(p) for some p (listed as [p, a_p, ord_29(p)]): ",
      Filtered(res, r -> IsList(r[2]) and not IsString(r[2]) and r[2] <> []), "\n");
# Appendix F.4 (e): from Table 3 only Ru, J4 (and 2.Ru); from Table 2, L2(q) with q in {29, 59, 173}
# 付録 F.4 (e): 表 3 からは Ru と J4（と 2.Ru）だけ、表 2 からは q ∈ {29, 59, 173} の L2(q) だけ
Expect("G-F6: 29 | |T| exactly for Ru, J4, L2(29), L2(59), L2(173)",
       Set(List(Filtered(res, r -> r[2] = "29 divides |T|"), r -> r[1])), Set(["Ru", "J4", "L2(29)", "L2(59)", "L2(173)"]));
# Equality a_p = ord_29(p) occurs only for U8(2) at p = 2, which G-F9 excludes / 等号は U8(2) の p = 2 だけで、G-F9 で除く
Expect("G-F6: a_p < ord_29(p) fails only for U8(2) (p = 2, a_p = 28 = ord_29(2))",
       Filtered(res, r -> IsList(r[2]) and not IsString(r[2]) and r[2] <> []), [["U8(2)", [[2, 28, 28]]]]);
# G-F7
for p in [29, 59, 173] do
  G := PSL(2, p);
  Print("G-F7: |Aut(PSL(2,", p, "))| / |PSL(2,", p, ")| = ", Size(AutomorphismGroup(G)) / Size(G), "\n");
  Expect(Concatenation("G-F7: |Aut(PSL(2,", String(p), "))| = 2 |PSL(2,", String(p), ")|"), Size(AutomorphismGroup(G)) / Size(G), 2);
od;
# G-F8
ru := CharacterTable("Ru");; l := CharacterTable("L2(29)");;
o29 := Filtered([1..NrConjugacyClasses(ru)], i -> OrdersClassRepresentatives(ru)[i] = 29);
Print("G-F8: Ru: classes of elements of order 29: ", Length(o29), ", centralizer orders ", SizesCentralizers(ru){o29},
      "; |N_Ru(P)| = 29 * 28 / (number of classes) = ", 29*28/Length(o29), "\n");
Expect("G-F8: two classes of order 29 in Ru with centralizer order 29, so |N_Ru(P)| = 406",
       [SizesCentralizers(ru){o29}, 29*28/Length(o29)], [[29, 29], 406]);
cnt := function(t, n) return Sum(Filtered([1..NrConjugacyClasses(t)], i -> OrdersClassRepresentatives(t)[i] = n), i -> SizesConjugacyClasses(t)[i]); end;
ords := Set(OrdersClassRepresentatives(ru));
Print("G-F8: n, #(order n in Ru) mod 29, #(order n in L2(29)) mod 29:\n");
for n in ords do Print("    ", n, ": ", cnt(ru, n) mod 29, " ", cnt(l, n) mod 29, "\n"); od;
Print("G-F8: orders n where the congruence fails: ", Filtered(ords, n -> (cnt(ru, n) - cnt(l, n)) mod 29 <> 0), "\n");
Expect("G-F8: the congruence excludes nothing (it holds for every n)", Filtered(ords, n -> (cnt(ru, n) - cnt(l, n)) mod 29 <> 0), []);
Print("G-F8: multiplicities of character degrees of Ru (max): ", Maximum(List(Collected(List(Irr(ru), x -> x[1])), c -> c[2])), "\n");
Print("G-F8: |PSL(2,29)| / |N_{PSL(2,29)}(P)| = number of Sylow 29-subgroups = ", Size(PSL(2,29)) / Size(Normalizer(PSL(2,29), SylowSubgroup(PSL(2,29), 29))), "\n");
Expect("G-F8: PSL(2,29) has 30 Sylow 29-subgroups", Size(PSL(2,29)) / Size(Normalizer(PSL(2,29), SylowSubgroup(PSL(2,29), 29))), 30);
su4 := SU(4, 2);;
Print("G-F9: |SU(4,2)| = ", Size(su4), ", Sylow 2-subgroup abelian: ", IsAbelian(SylowSubgroup(su4, 2)), ", Gcd(8, 2+1) = ", Gcd(8, 3), "\n");
Expect("G-F9: the Sylow 2-subgroup of SU(4,2) is not abelian (and U8(2) = SU8(2))", [IsAbelian(SylowSubgroup(su4, 2)), Gcd(8, 3)], [false, 1]);
Print("G-F10: Ru: minimal nontrivial degree ", Minimum(List(Filtered(Irr(ru), x -> x[1] > 1), x -> x[1])), "\n");
Expect("G-F10: the nontrivial irreducible characters of Ru have degree > 112", Minimum(List(Filtered(Irr(ru), x -> x[1] > 1), x -> x[1])) > 112, true);
t2 := CharacterTable("2.Ru");;
z := First([1..NrConjugacyClasses(t2)], i -> OrdersClassRepresentatives(t2)[i] = 2 and SizesConjugacyClasses(t2)[i] = 1);;
fl := Filtered(Irr(t2), x -> x[z] = -x[1] and x[1] <= 112);;
Print("G-F10: 2.Ru: faithful irreducibles of degree <= 112: degrees ", List(fl, x -> x[1]), ", fields of values ", List(fl, x -> Field(Rationals, x)), "\n");
Expect("G-F10: 2.Ru has exactly two faithful irreducibles of degree <= 112, of degree 28 with field Q(i)",
       [List(fl, x -> x[1]), List(fl, x -> Field(Rationals, x))], [[28, 28], [GaussianRationals, GaussianRationals]]);
S := SL(2, 29);; B := Normalizer(S, SylowSubgroup(S, 29));; tS := CharacterTable(S);; tB := CharacterTable(B);;
c28 := Filtered(Irr(tS), x -> x[1] = 28);;
Print("G-F11: |B| = ", Size(B), "; number of degree-28 irreducibles of SL(2,29): ", Length(c28), "; their restrictions to B as [degree, multiplicity] lists: ",
      Set(c28, x -> List(Filtered(Irr(tB), y -> ScalarProduct(tB, RestrictedClassFunction(x, B), y) <> 0), y -> [y[1], ScalarProduct(tB, RestrictedClassFunction(x, B), y)])), "\n");
Expect("G-F11: |B| = 812 and every degree-28 irreducible restricts to B as two different degree-14 irreducibles",
       [Size(B), Length(c28) > 0, Set(c28, x -> List(Filtered(Irr(tB), y -> ScalarProduct(tB, RestrictedClassFunction(x, B), y) <> 0), y -> [y[1], ScalarProduct(tB, RestrictedClassFunction(x, B), y)]))],
       [812, true, [[[14, 1], [14, 1]]]]);
dp := CharacterTableDirectProduct(CharacterTable("Cyclic", 2), CharacterTable("L2(29)"));;
Print("G-F12: possible class fusions 2 x L2(29) -> 2.Ru: ", Length(PossibleClassFusions(dp, t2)), "; 2.L2(29) -> 2.Ru: ", Length(PossibleClassFusions(CharacterTable("2.L2(29)"), t2)), "\n");
Expect("G-F12: no possible class fusion 2 x L2(29) -> 2.Ru (and 6 for 2.L2(29), as in G-F4)",
       [Length(PossibleClassFusions(dp, t2)), Length(PossibleClassFusions(CharacterTable("2.L2(29)"), t2))], [0, 6]);
if nfail > 0 then Print("RESULT: FAIL (", nfail, " mismatches)\n"); QuitGap(1); fi;
Print("RESULT: PASS (G-F6 to G-F12 agree with the stated values)\n");
QuitGap(0);
