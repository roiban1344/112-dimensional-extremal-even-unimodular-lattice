import Mathlib.Algebra.Group.Hom.Defs
import Mathlib.Algebra.Group.Equiv.Defs
import Mathlib.Algebra.Group.Basic
import Mathlib.Tactic.Abel
import Mathlib.Tactic.Ring
import Mathlib.Tactic.ByContra

/-!
# The deduction for the 112-dimensional lattice `L₁₁₂`, with the computed facts as hypotheses
# 112 次元格子 `L₁₁₂` の論証（計算事実を仮定とした形式化）

## What this file proves

The paper (§7.1, Table 9) reduces "`L₁₁₂` has no vector of norm less than 10" to finitely many
facts F1–F5 about the 56-dimensional lattice `L₅₆`, which programs check. This file proves the
deduction from F1–F5 to that conclusion. The facts themselves are hypotheses here: they are the
fields of the structures `Setting`, `Data`, `DataCert` and `DataCanonical`, and nothing in this
file computes with the actual matrices.

Items of the paper covered: Lemma 3.2 (the evenness part), Lemma 4.2, Corollary 4.3,
Appendix C.4, Lemma 5.1 (the midpoint lemma), Corollaries 5.2 and 5.3, §4.2 (reduction by
symmetry), and the derivation of Theorem A from F1–F5 in §4.3, for both ways of checking F5b
(certificates, §6.7; canonical forms, §6.5).

## How to read it

1. `Setting`: what is assumed about `L₅₆` and `τ`. `L` is an additive group, `B` an integer-valued
   symmetric bilinear form with even norms, every nonzero vector has norm at least 6 (F1), and `τ`
   is an endomorphism with `B (τ x) (τ y) = 5 B x y` and `τ (τ x) = -5 x` (the identities of F4).
2. `Data`, `DataCert`, `DataCanonical`: the computed facts F2–F5 (the symmetry group, orbit
   representatives, and either the certificates or the canonical-form result for the even cosets).
3. `theoremA` and `theoremA_canonical`: the conclusion. If `(x, τ x + 2y) ≠ 0` then
   `N x + N (τ x + 2y) ≥ 20`. By (1.2), the vector `z = (x, x τ + 2y)/√2 ∈ L₁₁₂` has
   `⟨z, z⟩ = (N x + N (τ x + 2y))/2`, so this says that `L₁₁₂` has no vector of norm less than 10;
   the translation through (1.2) is not part of the Lean statement.
4. `no_inner_shell_ne8` and `no_inner_shell`: the same conclusion from the two coset bounds of
   Corollary 4.3 (the case analysis of Lemma 4.2).
5. `midpoint_lemma`, `cert_bound`, `odd_bound`, `even_bound`: Lemma 5.1 and its corollaries, which
   turn one certificate into a bound for its whole coset.
6. `class_pred_transport`, `class_bound_transport`: §4.2, moving a statement about the coset of a
   representative to the coset of its image under an element of the symmetry group.

The proofs are short tactic scripts; the integer case analysis of the paper is done by `omega`.

## Hypotheses (checked by the programs of §6; not proved here)

* `Setting.symm`, `Setting.even`, `Setting.τ_sim`, `Setting.τ_sq`: `B` is symmetric, `L₅₆` is even,
  `τ G τᵀ = 5 G` and `τ² = -5` (the identities of F4 and of the construction (3.1); `v0_inputs.py`).
* `Setting.min6` (F1): every nonzero vector has norm at least 6.
* `Data.sym_iso`, `Data.sym_tau` (F4): every element of `Sym` is an isometry and commutes with `τ`.
  The programs check this for two generators; the extension to the group they generate is a
  one-line induction that is not formalized.
* `Data.cover6`, `Data.cover8` (F2, F3): every vector of norm 6 (norm 8) is the image of an element
  of `reps6` (`reps8`) under an element of `Sym`. The programs establish this from orbit-size sums
  and theta-series coefficients; only the conclusion is assumed here.
* `Data.bound6` (F5a): the coset of every `r ∈ reps6` has an odd certificate (Check 5.4).
* `DataCert.bound8` (F5b by certificates, §6.7): the coset of every `r ∈ reps8` has an even
  certificate.
* `DataCanonical.nocoll8` (F5b by canonical forms, §6.5): the coset of every `r ∈ reps8` contains
  no vector of norm 8. Proposition 6.3, which derives this from the canonical forms, is not
  formalized.

Also outside this file: unimodularity (F0), the theta series, and the upper bound (1.1)
`min L₁₁₂ ≤ 10`. See §7.1 of the paper.

## Notation

Maps are written on the left (`S.τ x`, `g r`), whereas the paper writes row vectors with matrices
acting on the right (`x τ`, `x g`). `S.N x = S.B x x` is the norm and `2 • y` is `y + y`.
`Sym` is a set of additive automorphisms; it need not be closed under composition, since only the
listed elements are used. Only the parts of Mathlib that are needed are imported, to keep the
dependencies small. `EEUL` stands for "extremal even unimodular lattice".

## 日本語

### このファイルで証明すること

論文（§7.1、表 9）は「`L₁₁₂` にノルム 10 未満のベクトルが無い」を、56 次元格子 `L₅₆` についての有限個の
事実 F1〜F5 に帰着し、F1〜F5 はプログラムで確かめる。このファイルは F1〜F5 からその結論への導出を証明する。
事実そのものはここでは仮定であり、構造体 `Setting`・`Data`・`DataCert`・`DataCanonical` のフィールドとして
置く。実際の行列を使う計算はこのファイルには無い。

扱う論文の項目: 補題 3.2（偶性の部分）、補題 4.2、系 4.3、付録 C.4、補題 5.1（中点補題）、系 5.2・5.3、
§4.2（対称性による帰着）、§4.3 の F1〜F5 からの定理 A の導出。F5b の二つの確かめ方（証明書 §6.7、標準形 §6.5）
の両方に対応する。

### 読む順

1. `Setting`: `L₅₆` と `τ` について仮定すること。`L` は加法群、`B` は整数値の対称双線形形式でノルムは偶数、
   0 でないベクトルのノルムは 6 以上（F1）、`τ` は `B (τ x) (τ y) = 5 B x y` と `τ (τ x) = -5 x` を満たす
   自己準同型（F4 の恒等式）。
2. `Data`・`DataCert`・`DataCanonical`: 計算で確かめた事実 F2〜F5（対称性の群、軌道代表、偶の類についての
   証明書または標準形の結果）。
3. `theoremA`・`theoremA_canonical`: 結論。`(x, τ x + 2y) ≠ 0` なら `N x + N (τ x + 2y) ≥ 20`。
   (1.2) により `z = (x, x τ + 2y)/√2 ∈ L₁₁₂` は `⟨z, z⟩ = (N x + N (τ x + 2y))/2` を満たすので、
   これは「`L₁₁₂` にノルム 10 未満のベクトルが無い」である。(1.2) による読み替えは Lean の主張の外。
4. `no_inner_shell_ne8`・`no_inner_shell`: 系 4.3 の二つの類の下界から同じ結論（補題 4.2 の場合分け）。
5. `midpoint_lemma`・`cert_bound`・`odd_bound`・`even_bound`: 補題 5.1 とその系。一つの証明書から
   類全体の下界へ。
6. `class_pred_transport`・`class_bound_transport`: §4.2。代表の類についての主張を、対称性の元による
   像の類へ移す。

証明は短いタクティク列で、論文の整数の場合分けは `omega` が行う。

### 仮定として置くもの（§6 のプログラムで確かめる。ここでは証明しない）

* `Setting.symm`・`Setting.even`・`Setting.τ_sim`・`Setting.τ_sq`: `B` は対称、`L₅₆` は偶、
  `τ G τᵀ = 5 G`、`τ² = -5`（F4 と構成 (3.1) の恒等式。`v0_inputs.py`）。
* `Setting.min6`（F1）: 0 でないベクトルのノルムは 6 以上。
* `Data.sym_iso`・`Data.sym_tau`（F4）: `Sym` のすべての元は等長で `τ` と可換。プログラムは生成元 2 個について
  確かめる。生成する群全体への拡張は 1 行の帰納で、形式化していない。
* `Data.cover6`・`Data.cover8`（F2、F3）: ノルム 6（8）のベクトルはすべて、`reps6`（`reps8`）の元の `Sym` の
  元による像。プログラムは軌道の大きさの和とテータ級数の係数からこれを導く。ここでは結論だけを仮定する。
* `Data.bound6`（F5a）: 各 `r ∈ reps6` の類に奇の証明書（検査 5.4）がある。
* `DataCert.bound8`（F5b を証明書で。§6.7）: 各 `r ∈ reps8` の類に偶の証明書がある。
* `DataCanonical.nocoll8`（F5b を標準形で。§6.5）: 各 `r ∈ reps8` の類はノルム 8 のベクトルを含まない。
  標準形からこれを導く命題 6.3 は形式化していない。

このほかにこのファイルの外にあるもの: ユニモジュラー性（F0）、テータ級数、上界 (1.1) `min L₁₁₂ ≤ 10`。
論文 §7.1 を参照。

### 記法

写像は左から書く（`S.τ x`、`g r`）。論文は行ベクトルに右から行列を掛ける（`x τ`、`x g`）。
`S.N x = S.B x x` がノルム、`2 • y` は `y + y`。`Sym` は加法的自己同型の集合で、使うのは列挙した元だけなので
合成について閉じている必要はない。依存を小さく保つため、Mathlib は必要な部分だけを読み込む。
`EEUL` は extremal even unimodular lattice（極値偶ユニモジュラー格子）の略。
-/

namespace EEUL.L112

/-- The abstract setting: what is assumed about `L₅₆` and `τ`. An additive group `L` (standing
for `L₅₆`) with an integer-valued symmetric bilinear form `B`, and an endomorphism `τ` acting as
`√-5`. The actual Gram matrix never enters.
抽象的な設定: `L₅₆` と `τ` について仮定すること。整数値の対称双線形形式 `B` をもつ加法群 `L`
（`L₅₆` の役）と、`√-5` として働く自己準同型 `τ`。実際の Gram 行列は現れない。 -/
structure Setting (L : Type*) [AddCommGroup L] where
  /-- The bilinear form `⟨x, y⟩` of `L₅₆`, as a ℤ-bilinear map.
  `L₅₆` の双線形形式 `⟨x, y⟩`（ℤ-双線形写像として）。 -/
  B : L →+ L →+ ℤ
  /-- `B` is symmetric. / `B` は対称。 -/
  symm : ∀ x y, B x y = B y x
  /-- Even lattice: norms are even. / 偶格子: ノルムは偶数。 -/
  even : ∀ x, B x x % 2 = 0
  /-- **F1** (hypothesis): every nonzero vector has norm at least 6.
  **F1**（仮定）: 0 でないベクトルのノルムは 6 以上。 -/
  min6 : ∀ x, x ≠ 0 → 6 ≤ B x x
  /-- The endomorphism `τ`, written on the left (`x τ` in the paper).
  自己準同型 `τ`。左から書く（論文では `x τ`）。 -/
  τ : L →+ L
  /-- `τ` is a similarity of ratio 5: `⟨x τ, y τ⟩ = 5 ⟨x, y⟩` (F4: `τ G τᵀ = 5 G`).
  `τ` は比 5 の相似: `⟨x τ, y τ⟩ = 5 ⟨x, y⟩`（F4: `τ G τᵀ = 5 G`）。 -/
  τ_sim : ∀ x y, B (τ x) (τ y) = 5 * B x y
  /-- `τ² = -5` (F4). / `τ² = -5`（F4）。 -/
  τ_sq : ∀ x, τ (τ x) = -(5 • x)

namespace Setting

variable {L : Type*} [AddCommGroup L] (S : Setting L)

/-- The norm `N x = B x x`.
ノルム `N x = B x x`。 -/
def N (x : L) : ℤ := S.B x x

theorem B_add_left (a b c : L) : S.B (a + b) c = S.B a c + S.B b c := by
  rw [map_add, AddMonoidHom.add_apply]

theorem B_add_right (a b c : L) : S.B a (b + c) = S.B a b + S.B a c := by
  rw [map_add]

theorem B_neg_left (a c : L) : S.B (-a) c = -S.B a c := by
  rw [map_neg, AddMonoidHom.neg_apply]

theorem B_neg_right (a c : L) : S.B a (-c) = -S.B a c := by
  rw [map_neg]

theorem N_add (a b : L) : S.N (a + b) = S.N a + S.N b + 2 * S.B a b := by
  unfold N
  rw [B_add_left, B_add_right, B_add_right, S.symm b a]
  ring

theorem N_neg (a : L) : S.N (-a) = S.N a := by
  unfold N
  rw [B_neg_left, B_neg_right, neg_neg]

theorem N_sub (a b : L) : S.N (a - b) = S.N a + S.N b - 2 * S.B a b := by
  rw [sub_eq_add_neg, N_add, N_neg, B_neg_right]
  ring

theorem N_two (y : L) : S.N (2 • y) = 4 * S.N y := by
  rw [two_nsmul, N_add]
  unfold N
  ring

theorem B_two_right (a y : L) : S.B a (2 • y) = 2 * S.B a y := by
  rw [two_nsmul, B_add_right]
  ring

theorem N_tau (x : L) : S.N (S.τ x) = 5 * S.N x := S.τ_sim x x

/-- Twice a nonzero vector has norm at least 24.
0 でないベクトルの 2 倍のノルムは 24 以上。 -/
theorem N_two_ge (y : L) (hy : y ≠ 0) : 24 ≤ S.N (2 • y) := by
  rw [N_two]
  have := S.min6 y hy
  unfold N
  omega

/-- The evenness part of Lemma 3.2: `N x + N (τ x + 2y) = 6 N x + 4 (B (τ x) y + N y)`; in
particular it is a multiple of 4.
補題 3.2 の偶性の部分: `N x + N (τ x + 2y) = 6 N x + 4 (B (τ x) y + N y)`。とくに 4 の倍数。 -/
theorem norm_sum (x y : L) :
    S.N x + S.N (S.τ x + 2 • y) = 6 * S.N x + 4 * (S.B (S.τ x) y + S.N y) := by
  rw [N_add, N_tau, N_two, B_two_right]
  ring

theorem norm_sum_mod4 (x y : L) : (S.N x + S.N (S.τ x + 2 • y)) % 4 = 0 := by
  rw [norm_sum]
  have := S.even x
  unfold N at *
  omega

/-- If `τ x ∈ 2L` then `x ∈ 2L` (the case `v = 0` in the proof of Lemma 4.2).
`τ x ∈ 2L` なら `x ∈ 2L`（補題 4.2 の証明の `v = 0` の場合）。 -/
theorem two_dvd_of_tau (x y : L) (h : S.τ x + 2 • y = 0) : x = 2 • (S.τ y - 2 • x) := by
  have h1 : S.τ x = -(2 • y) := eq_neg_of_add_eq_zero_left h
  have h2 : S.τ (S.τ x) = -(2 • S.τ y) := by rw [h1, map_neg, map_nsmul]
  rw [S.τ_sq] at h2
  have h3 : 5 • x = 2 • S.τ y := neg_injective h2
  calc x = 5 • x - 4 • x := by abel
    _ = 2 • S.τ y - 4 • x := by rw [h3]
    _ = 2 • (S.τ y - 2 • x) := by abel

/-- `τ² ≡ 1 (mod 2)`: if `v = τ x + 2y` then `x = τ v + 2 (3x - τ y)` (Appendix C.4).
`τ² ≡ 1 (mod 2)`: `v = τ x + 2y` なら `x = τ v + 2 (3x - τ y)`（付録 C.4）。 -/
theorem tau_involution_mod2 (x y : L) :
    x = S.τ (S.τ x + 2 • y) + 2 • (3 • x - S.τ y) := by
  rw [map_add, map_nsmul, S.τ_sq]
  abel

end Setting

/-! ## Lemma 4.2 and Corollary 4.3: the two coset bounds imply that there is no inner-shell vector
## 補題 4.2 と系 4.3: 二つの類の下界から内殻ベクトルが無いことが出る -/

section Main

variable {L : Type*} [AddCommGroup L] (S : Setting L)

open Setting

/-- **The two coset conditions of Corollary 4.3 ⟹ no inner-shell vector** (the "⇐" direction of
Corollary 4.3, in the weakest form the case analysis needs).
Hypothesis `h6`: every element of the coset `τ r + 2L` of a minimal vector `r` has norm at least 14.
Hypothesis `h8`: no element of the coset `τ x + 2L` of a norm-8 vector `x` has norm 8.
Conclusion: if `(x, τ x + 2y) ≠ 0` then `N x + N (τ x + 2y) ≥ 20` (norm of `L₁₁₂` ≥ 10).
The hypothesis `h8` is what the canonical-form check (§6.5) establishes; `no_inner_shell` below
takes the bound 12 of Corollary 4.3 (ii) instead.

**系 4.3 の二つの類の条件 ⟹ 内殻ベクトルが無い**（系 4.3 の「⇐」。場合分けに必要な最も弱い形）。
仮定 `h6`: 最小ベクトル `r` の類 `τ r + 2L` の元はノルム 14 以上。
仮定 `h8`: ノルム 8 の `x` の類 `τ x + 2L` にノルム 8 の元は無い。
結論: `(x, τ x + 2y) ≠ 0` なら `N x + N (τ x + 2y) ≥ 20`（`L₁₁₂` のノルム ≥ 10）。
`h8` は標準形の検査（§6.5）が確かめる形。下の `no_inner_shell` は代わりに系 4.3 (ii) の下界 12 を取る。 -/
theorem no_inner_shell_ne8
    (h6 : ∀ r y, S.N r = 6 → 14 ≤ S.N (S.τ r + 2 • y))
    (h8 : ∀ x y, S.N x = 8 → S.N (S.τ x + 2 • y) ≠ 8)
    (x y : L) (hz : x ≠ 0 ∨ S.τ x + 2 • y ≠ 0) :
    20 ≤ S.N x + S.N (S.τ x + 2 • y) := by
  have hmod := S.norm_sum_mod4 x y
  have hex := S.even x
  have hev := S.even (S.τ x + 2 • y)
  unfold N at hmod
  by_cases hx : x = 0
  · -- x = 0: then v = 2y ≠ 0, of norm ≥ 24 / x = 0 のとき v = 2y ≠ 0 でノルム 24 以上
    subst hx
    have hv : S.τ 0 + 2 • y ≠ 0 := by
      rcases hz with h | h
      · exact absurd rfl h
      · exact h
    rw [map_zero, zero_add] at hv ⊢
    have hy : y ≠ 0 := by rintro rfl; simp at hv
    have := S.N_two_ge y hy
    unfold N at this ⊢
    simp only [map_zero]
    omega
  by_cases hv : S.τ x + 2 • y = 0
  · -- v = 0: then x ∈ 2L and x ≠ 0, of norm ≥ 24 / v = 0 のとき x ∈ 2L、x ≠ 0 でノルム 24 以上
    have hxe := S.two_dvd_of_tau x y hv
    have hw : S.τ y - 2 • x ≠ 0 := by
      intro h; rw [h] at hxe; simp at hxe; exact hx hxe
    have := S.N_two_ge _ hw
    rw [← hxe] at this
    rw [hv]
    unfold N at this ⊢
    simp only [map_zero]
    omega
  -- both nonzero / 両方 0 でない
  have hx6 := S.min6 x hx
  have hv6 := S.min6 _ hv
  by_contra hlt
  unfold N at hlt
  -- the sum is 12 or 16 (a multiple of 4 below 20); the four types of Lemma 4.2
  -- 和は 12 か 16（20 未満の 4 の倍数）。補題 4.2 の四つの型に分ける
  have hcases : (S.B x x = 6 ∧ (S.B (S.τ x + 2 • y) (S.τ x + 2 • y) = 6 ∨ S.B (S.τ x + 2 • y) (S.τ x + 2 • y) = 10))
      ∨ (S.B x x = 8 ∧ S.B (S.τ x + 2 • y) (S.τ x + 2 • y) = 8)
      ∨ (S.B x x = 10 ∧ S.B (S.τ x + 2 • y) (S.τ x + 2 • y) = 6) := by omega
  rcases hcases with ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · -- types (6,6) and (6,10): excluded by h6 / (6,6)・(6,10) 型: h6 で排除
    have := h6 x y h1; unfold N at this; omega
  · -- type (8,8): excluded by h8 / (8,8) 型: h8 で排除
    exact h8 x y h1 h2
  · -- type (10,6): x lies in the coset τ v + 2L of v (Appendix C.4), so h6 applies to v
    -- (10,6) 型: x は v の類 τ v + 2L に入る（付録 C.4）ので、v に h6 を使う
    have := h6 (S.τ x + 2 • y) (3 • x - S.τ y) h2
    rw [← S.tau_involution_mod2 x y] at this
    unfold N at this
    omega

/-- **The two coset bounds of Corollary 4.3 ⟹ no inner-shell vector**, with the bound 12 of
Corollary 4.3 (ii) as hypothesis `h8` (the form established by the certificates of §6.7).
**系 4.3 の二つの下界 ⟹ 内殻ベクトルが無い**。`h8` は系 4.3 (ii) の下界 12（§6.7 の証明書が確かめる形）。 -/
theorem no_inner_shell
    (h6 : ∀ r y, S.N r = 6 → 14 ≤ S.N (S.τ r + 2 • y))
    (h8 : ∀ x y, S.N x = 8 → 12 ≤ S.N (S.τ x + 2 • y))
    (x y : L) (hz : x ≠ 0 ∨ S.τ x + 2 • y ≠ 0) :
    20 ≤ S.N x + S.N (S.τ x + 2 • y) :=
  no_inner_shell_ne8 S h6 (fun x y hx => by have := h8 x y hx; omega) x y hz

end Main

/-! ## The midpoint lemma and certificates (Lemma 5.1, Corollaries 5.2 and 5.3)
## 中点補題と証明書（補題 5.1、系 5.2、系 5.3） -/

section Bounding

variable {L : Type*} [AddCommGroup L] (S : Setting L)

open Setting

/-- The inner-product condition on a certificate (Check 5.4 (c)): `|B w0 u| ≤ 6` for every minimal
vector `u`. A *certificate* for a coset is an element `w0` of it with the norm condition of
Check 5.4 (b) and this condition; the paper calls it 下界を保証する代表元 in Japanese.
証明書（下界を保証する代表元、certificate）の内積の条件（検査 5.4 (c)）: すべての最小ベクトル `u` について
`|B w0 u| ≤ 6`。類の証明書とは、その類の元 `w0` で検査 5.4 (b) のノルムの条件とこの条件を満たすもの。 -/
def SmallIP (w0 : L) : Prop := ∀ u, S.N u = 6 → -6 ≤ S.B w0 u ∧ S.B w0 u ≤ 6

/-- Midpoint computation: for `w = w0 + 2y`, the norms of the two midpoints `-y = (w0 - w)/2` and
`w0 + y = (w0 + w)/2`.
中点の計算: `w = w0 + 2y` について、二つの中点 `-y = (w0 - w)/2` と `w0 + y = (w0 + w)/2` のノルム。 -/
theorem midpoints (w0 y : L) :
    4 * S.N y = S.N (w0 + 2 • y) - S.N w0 - 4 * S.B w0 y ∧
    4 * S.N (w0 + y) = 3 * S.N w0 + S.N (w0 + 2 • y) + 4 * S.B w0 y := by
  constructor
  · rw [N_add, N_two, B_two_right]; ring
  · rw [N_add, N_add, N_two, B_two_right]; ring

/-- **Lemma 5.1 (midpoint lemma)**: if `w = w' + 2y` lies in the coset of `w'` and `w ≠ ±w'`, then
`N w + N w' - 2 B w w' ≥ 24` and `N w + N w' + 2 B w w' ≥ 24` (the midpoints `(w ∓ w')/2`, which
are `y` and `w' + y`, are nonzero vectors of `L`).
**補題 5.1（中点補題）**: `w = w' + 2y` が `w'` の類にあり `w ≠ ±w'` なら、
`N w + N w' - 2 B w w' ≥ 24` かつ `N w + N w' + 2 B w w' ≥ 24`（中点 `(w ∓ w')/2`、すなわち `y` と
`w' + y` が `L` の 0 でないベクトル）。 -/
theorem midpoint_lemma (w' y : L) (h1 : w' + 2 • y ≠ w') (h2 : w' + 2 • y ≠ -w') :
    24 ≤ S.N (w' + 2 • y) + S.N w' - 2 * S.B (w' + 2 • y) w' ∧
    24 ≤ S.N (w' + 2 • y) + S.N w' + 2 * S.B (w' + 2 • y) w' := by
  have hy : y ≠ 0 := by rintro rfl; simp at h1
  have hwy : w' + y ≠ 0 := by
    intro h
    apply h2
    rw [two_nsmul, ← add_assoc, h, zero_add]
    exact eq_neg_of_add_eq_zero_right h
  have m1 := S.N_two_ge y hy
  have m2 := S.N_two_ge (w' + y) hwy
  -- N (w - w') = N (2y) and N (w + w') = N (2 (w' + y)) / N (w - w') = N (2y)、N (w + w') = N (2 (w' + y))
  have e1 : S.N (w' + 2 • y) + S.N w' - 2 * S.B (w' + 2 • y) w' = S.N (2 • y) := by
    rw [← N_sub]; congr 1; abel
  have e2 : S.N (w' + 2 • y) + S.N w' + 2 * S.B (w' + 2 • y) w' = S.N (2 • (w' + y)) := by
    rw [← N_add]; congr 1; abel
  omega

/-- Norms in a coset `w0 + 2L` are congruent modulo 4.
類 `w0 + 2L` の中でノルムは 4 を法として合同。 -/
theorem coset_norm_mod4 (w0 y : L) : (S.N (w0 + 2 • y) - S.N w0) % 4 = 0 := by
  rw [N_add, N_two, B_two_right]; omega

/-- **Corollaries 5.2 and 5.3 at once**: a certificate `w0` with `12 ≤ N w0 ≤ 20` forces every
element of its coset to have norm at least 12. This is the common proof of the two corollaries
in the paper: if `w = w0 + 2y` had norm below 12, then `w ≠ ±w0`, and one of the two midpoints
`-y`, `w0 + y` would be a minimal vector `u` with `|B w0 u| > 6`. The four cases below are which
of the two midpoints have norm 6; `omega` does the arithmetic.
**系 5.2 と 5.3 を一度に**: `12 ≤ N w0 ≤ 20` の証明書 `w0` があれば、その類の元はすべてノルム 12 以上。
論文の二つの系に共通の証明: `w = w0 + 2y` のノルムが 12 未満なら `w ≠ ±w0` で、二つの中点 `-y`・`w0 + y` の
一方が最小ベクトル `u` になり `|B w0 u| > 6` となる。下の四つの場合は、二つの中点のどちらがノルム 6 か。
算術は `omega` が行う。 -/
theorem cert_bound (w0 : L) (hlo : 12 ≤ S.N w0) (hhi : S.N w0 ≤ 20) (hip : SmallIP S w0) (y : L) :
    12 ≤ S.N (w0 + 2 • y) := by
  obtain ⟨e1, e2⟩ := midpoints S w0 y
  have ey := S.even y
  have ewy := S.even (w0 + y)
  have ew := S.even (w0 + 2 • y)
  by_contra hlt
  -- w ≠ ±w0, since N w < 12 ≤ N w0 / N w < 12 ≤ N w0 なので w ≠ ±w0
  have hy : y ≠ 0 := by
    rintro rfl; simp at hlt; omega
  have hwy : w0 + y ≠ 0 := by
    intro h
    have : w0 + 2 • y = -w0 := by
      rw [two_nsmul, ← add_assoc, h, zero_add]; exact (eq_neg_of_add_eq_zero_right h)
    rw [this, N_neg] at hlt; omega
  have m1 := S.min6 y hy
  have m2 := S.min6 (w0 + y) hwy
  unfold N at *
  -- a midpoint of norm 6 is a minimal vector, so its inner product with w0 is at most 6 in absolute value
  -- ノルム 6 の中点は最小ベクトルなので、w0 との内積の絶対値は 6 以下
  by_cases c1 : S.B y y = 6
  · have := hip (-y) (by unfold N; rw [B_neg_left, B_neg_right, neg_neg]; exact c1)
    rw [B_neg_right] at this
    omega
  · by_cases c2 : S.B (w0 + y) (w0 + y) = 6
    · have h2 := hip (w0 + y) c2
      rw [B_add_right] at h2
      omega
    · omega

/-- **Corollary 5.2 (bound for odd cosets)**: if there is a certificate `w0` of norm 14 or 18, then
every element of its coset has norm at least 14 (`cert_bound`, and norms in the coset are
`≡ 2 (mod 4)`).
**系 5.2（奇の類の下界）**: ノルム 14 か 18 の証明書 `w0` があれば、その類の元はすべてノルム 14 以上
（`cert_bound` と、類の中でノルムが `≡ 2 (mod 4)` であること）。 -/
theorem odd_bound (w0 : L) (hN : S.N w0 = 14 ∨ S.N w0 = 18) (hip : SmallIP S w0) (y : L) :
    14 ≤ S.N (w0 + 2 • y) := by
  have := cert_bound S w0 (by omega) (by omega) hip y
  have := coset_norm_mod4 S w0 y
  omega

/-- **Corollary 5.3 (bound for even cosets)**: if there is a certificate `w0` of norm 12, 16 or 20,
then every element of its coset has norm at least 12.
**系 5.3（偶の類の下界）**: ノルム 12, 16, 20 の証明書 `w0` があれば、その類の元はすべてノルム 12 以上。 -/
theorem even_bound (w0 : L) (hN : S.N w0 = 12 ∨ S.N w0 = 16 ∨ S.N w0 = 20) (hip : SmallIP S w0)
    (y : L) : 12 ≤ S.N (w0 + 2 • y) :=
  cert_bound S w0 (by omega) (by omega) hip y

end Bounding

/-! ## Reduction by symmetry, and Theorem A from the computed facts F1–F5
## 対称性による帰着と、計算事実 F1〜F5 からの定理 A -/

section Reduction

variable {L : Type*} [AddCommGroup L]

/-- The computed facts shared by both routes (F2–F4 and F5a): the symmetry group `Sym`, orbit
representatives `reps6`, `reps8` of the vectors of norm 6 and 8, and the odd certificates.
`Sym` need not be closed under composition.
二つの経路に共通の計算事実（F2〜F4 と F5a）: 対称性の群 `Sym`、ノルム 6・8 のベクトルの軌道代表 `reps6`・
`reps8`、奇の証明書。`Sym` は合成について閉じていなくてよい。 -/
structure Data (S : Setting L) where
  /-- The symmetry group `S` of the paper (its elements, as additive automorphisms of `L`).
  論文の対称性の群 `S`（その元を `L` の加法的自己同型として）。 -/
  Sym : Set (L ≃+ L)
  /-- Orbit representatives of the vectors of norm 6 (F2). / ノルム 6 のベクトルの軌道代表（F2）。 -/
  reps6 : Set L
  /-- Representatives of the vectors of norm 8 (F3): all pairs (orbit representative) × (element of
  the centralizer), as in the paper. / ノルム 8 のベクトルの代表（F3）: 論文どおり
  (軌道代表) × (中心化群の元) の全体。 -/
  reps8 : Set L
  /-- **F4**: elements of the symmetry group are isometries and commute with `τ`.
  **F4**: 対称性の元は等長で、`τ` と可換。 -/
  sym_iso : ∀ g ∈ Sym, ∀ a b, S.B (g a) (g b) = S.B a b
  sym_tau : ∀ g ∈ Sym, ∀ a, S.τ (g a) = g (S.τ a)
  /-- **F2**: every vector of norm 6 is the image of a representative.
  **F2**: ノルム 6 のベクトルは代表の像。 -/
  cover6 : ∀ x, S.N x = 6 → ∃ g ∈ Sym, ∃ r ∈ reps6, x = g r
  /-- **F3**: every vector of norm 8 is the image of a representative.
  **F3**: ノルム 8 のベクトルは代表の像。 -/
  cover8 : ∀ x, S.N x = 8 → ∃ g ∈ Sym, ∃ r ∈ reps8, x = g r
  /-- **F5a**: the coset `τ r + 2L` of each representative `r ∈ reps6` has an odd certificate
  (Check 5.4, checked by `v5_odd_bounding.py`).
  **F5a**: 各代表 `r ∈ reps6` の類 `τ r + 2L` に奇の証明書がある（検査 5.4。`v5_odd_bounding.py`）。 -/
  bound6 : ∀ r ∈ reps6, ∃ w0 y0, w0 = S.τ r + 2 • y0 ∧ (S.N w0 = 14 ∨ S.N w0 = 18) ∧ SmallIP S w0

/-- `Data` together with F5b checked by even certificates (§6.7, `v7_even_bounding.py`).
`Data` に、偶の証明書で確かめた F5b を加えたもの（§6.7、`v7_even_bounding.py`）。 -/
structure DataCert (S : Setting L) extends Data S where
  /-- **F5b (certificates)**: the coset `τ r + 2L` of each representative `r ∈ reps8` has an even
  certificate. / **F5b（証明書）**: 各代表 `r ∈ reps8` の類 `τ r + 2L` に偶の証明書がある。 -/
  bound8 : ∀ r ∈ reps8, ∃ w0 y0, w0 = S.τ r + 2 • y0 ∧ (S.N w0 = 12 ∨ S.N w0 = 16 ∨ S.N w0 = 20) ∧ SmallIP S w0

/-- `Data` together with F5b checked by canonical forms (§6.5, `v6_canonical_lookup.py`). The
program checks `can(τ r + 2L) ∉ K₈`; Proposition 6.3 turns this into the statement below.
`Data` に、標準形で確かめた F5b を加えたもの（§6.5、`v6_canonical_lookup.py`）。プログラムが確かめるのは
`can(τ r + 2L) ∉ K₈` で、命題 6.3 がそれを下の主張にする。 -/
structure DataCanonical (S : Setting L) extends Data S where
  /-- **F5b (canonical forms)**: the coset `τ r + 2L` of each representative `r ∈ reps8` contains no
  vector of norm 8. / **F5b（標準形）**: 各代表 `r ∈ reps8` の類 `τ r + 2L` はノルム 8 のベクトルを含まない。 -/
  nocoll8 : ∀ r ∈ reps8, ∀ y, S.N (S.τ r + 2 • y) ≠ 8

variable {S : Setting L}

open Setting

/-- Transport a property `P` of all norms in the coset of a representative `r` to the coset of its
image `g r` (§4.2): `τ (g r) + 2y = g (τ r + 2 g⁻¹ y)` and `g` preserves norms.
代表 `r` の類のすべてのノルムの性質 `P` を、像 `g r` の類へ移す（§4.2）: `τ (g r) + 2y = g (τ r + 2 g⁻¹ y)` で、
`g` はノルムを保つ。 -/
theorem class_pred_transport (D : Data S) (P : ℤ → Prop) (g : L ≃+ L) (hg : g ∈ D.Sym) (r : L)
    (hr : ∀ y, P (S.N (S.τ r + 2 • y))) (y : L) : P (S.N (S.τ (g r) + 2 • y)) := by
  have : S.τ (g r) + 2 • y = g (S.τ r + 2 • g.symm y) := by
    rw [map_add, map_nsmul, AddEquiv.apply_symm_apply, D.sym_tau g hg]
  rw [this]
  have := hr (g.symm y)
  unfold N at this ⊢
  rwa [D.sym_iso g hg]

/-- Transport a lower bound on the coset of a representative to the coset of its image (§4.2).
代表の類についての下界を、像の類に移す（§4.2）。 -/
theorem class_bound_transport (D : Data S) (g : L ≃+ L) (hg : g ∈ D.Sym) (r : L) (c : ℤ)
    (hr : ∀ y, c ≤ S.N (S.τ r + 2 • y)) (y : L) : c ≤ S.N (S.τ (g r) + 2 • y) :=
  class_pred_transport D (fun n => c ≤ n) g hg r hr y

/-- From a certificate `w0 = τ r + 2 y0` to a bound on the whole coset `τ r + 2L`.
証明書 `w0 = τ r + 2 y0` から、類 `τ r + 2L` 全体の下界へ。 -/
theorem class_bound_of_rep (r w0 y0 : L) (hw : w0 = S.τ r + 2 • y0) (c : ℤ)
    (hb : ∀ y, c ≤ S.N (w0 + 2 • y)) (y : L) : c ≤ S.N (S.τ r + 2 • y) := by
  have : S.τ r + 2 • y = w0 + 2 • (y - y0) := by rw [hw]; abel
  rw [this]; exact hb _

/-- Corollary 4.3 (i) from F2, F4 and F5a: every element of the coset of a minimal vector has norm
at least 14. / F2・F4・F5a から系 4.3 (i): 最小ベクトルの類の元はノルム 14 以上。 -/
theorem odd_cosets_bound (D : Data S) (r y : L) (hr : S.N r = 6) : 14 ≤ S.N (S.τ r + 2 • y) := by
  obtain ⟨g, hg, r0, hr0, rfl⟩ := D.cover6 r hr
  obtain ⟨w0, y0, hw, hN, hip⟩ := D.bound6 r0 hr0
  exact class_bound_transport D g hg r0 14
    (class_bound_of_rep r0 w0 y0 hw 14 (odd_bound S w0 hN hip)) y

/-- **The logical part of Theorem A (F5b by certificates)**: assuming F1 (`Setting.min6`) and
F2–F5 (`DataCert`), if `(x, τ x + 2y) ≠ 0` then `N x + N (τ x + 2y) ≥ 20`; by (1.2), `L₁₁₂` has
no inner-shell vector.
**定理 A の論理部分（F5b を証明書で）**: F1（`Setting.min6`）と F2〜F5（`DataCert`）を仮定すれば、
`(x, τ x + 2y) ≠ 0` のとき `N x + N (τ x + 2y) ≥ 20`。(1.2) により `L₁₁₂` に内殻ベクトルは無い。 -/
theorem theoremA (D : DataCert S) (x y : L) (hz : x ≠ 0 ∨ S.τ x + 2 • y ≠ 0) :
    20 ≤ S.N x + S.N (S.τ x + 2 • y) := by
  apply no_inner_shell S (odd_cosets_bound D.toData) _ x y hz
  intro x y hx
  obtain ⟨g, hg, r0, hr0, rfl⟩ := D.cover8 x hx
  obtain ⟨w0, y0, hw, hN, hip⟩ := D.bound8 r0 hr0
  exact class_bound_transport D.toData g hg r0 12
    (class_bound_of_rep r0 w0 y0 hw 12 (even_bound S w0 hN hip)) y

/-- **The logical part of Theorem A (F5b by canonical forms)**: the same conclusion from F1 and
`DataCanonical`, where F5b is "the coset of each representative contains no vector of norm 8".
**定理 A の論理部分（F5b を標準形で）**: F1 と `DataCanonical`（F5b を「各代表の類はノルム 8 のベクトルを
含まない」の形で）から同じ結論。 -/
theorem theoremA_canonical (D : DataCanonical S) (x y : L) (hz : x ≠ 0 ∨ S.τ x + 2 • y ≠ 0) :
    20 ≤ S.N x + S.N (S.τ x + 2 • y) := by
  apply no_inner_shell_ne8 S (odd_cosets_bound D.toData) _ x y hz
  intro x y hx
  obtain ⟨g, hg, r0, hr0, rfl⟩ := D.cover8 x hx
  exact class_pred_transport D.toData (fun n => n ≠ 8) g hg r0 (D.nocoll8 r0 hr0) y

end Reduction

end EEUL.L112
