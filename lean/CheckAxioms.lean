import EEUL.L112.Chain

-- The axioms each theorem depends on. Expected: subsets of [propext, Classical.choice, Quot.sound];
-- `check.sh` compares the output with expected-axioms.txt.
-- 各定理が依存する公理。期待値は [propext, Classical.choice, Quot.sound] の部分集合。
-- `check.sh` が出力を expected-axioms.txt と比較する。
#print axioms EEUL.L112.Setting.norm_sum_mod4
#print axioms EEUL.L112.no_inner_shell_ne8
#print axioms EEUL.L112.no_inner_shell
#print axioms EEUL.L112.midpoints
#print axioms EEUL.L112.midpoint_lemma
#print axioms EEUL.L112.cert_bound
#print axioms EEUL.L112.odd_bound
#print axioms EEUL.L112.even_bound
#print axioms EEUL.L112.class_pred_transport
#print axioms EEUL.L112.theoremA
#print axioms EEUL.L112.theoremA_canonical
