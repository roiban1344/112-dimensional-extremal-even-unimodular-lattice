# The argument in Lean

[日本語](README.ja.md)

`EEUL/L112/Chain.lean` formalizes the deductions from the stated lattice and certificate hypotheses to the absence of short vectors. It does not verify the numerical input or run the certificate checkers. See the paper for the scope of the formalization.

Lean and Mathlib versions are fixed by `lean-toolchain` and `lake-manifest.json`. With the matching Lean toolchain installed:

```bash
cd lean
lake exe cache get
lake build
lake env lean CheckAxioms.lean
```

The first command fetches the Mathlib cache; subsequent builds use the local dependencies. This package contains the argument of the paper (the part that takes the computational facts as hypotheses).

`CheckAxioms.lean` lists the axioms used by the main results. The expected dependencies are only `propext`, `Classical.choice` and `Quot.sound`; the stated computational hypotheses remain hypotheses.
