# The argument in Lean

[日本語](README.ja.md)

## What is proved

`EEUL/L112/Chain.lean` proves, in Lean 4 with Mathlib, the deduction from the computational facts F1–F5 of the paper to the conclusion that L₁₁₂ has no vector of norm less than 10. The facts are hypotheses: they are the fields of the structures `Setting`, `Data`, `DataCert` and `DataCanonical`, and the file neither reads the matrices nor runs the certificate checkers. §7.1 of the paper (Table 9) lists the formalized statements and what stays outside Lean.

## How to read Chain.lean

- Start with the module comment at the top: what is proved, the reading order, the hypotheses, the notation. Then read the statements of `theoremA` (F5b checked by certificates) and `theoremA_canonical` (F5b checked by canonical forms), together with the fields of `Setting` and `Data` that they assume. Everything else is proof.
- Maps are written on the left: `S.τ x` and `g r` are xτ and rg of the paper. `S.N x` is the norm ⟨x, x⟩ and `2 • y` is y + y.
- The proofs are short tactic scripts; `omega` closes the integer case analysis of the paper.

## How to check

Lean and Mathlib versions are fixed by `lean-toolchain` and `lake-manifest.json`; `elan` installs the toolchain named in `lean-toolchain`. Then:

```bash
cd lean
lake exe cache get   # Mathlib cache, once (several hundred MB)
./check.sh
```

`check.sh` follows the steps of the Lean reference manual ([Validating Proofs](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)) and does three things.

1. It builds the package with warnings treated as errors (`lake build --wfail`). A `sorry` anywhere gives a warning, as do Mathlib's standard linters.
2. It compares the axioms each theorem depends on (`lake env lean CheckAxioms.lean`) with `expected-axioms.txt`. The axioms are only `propext`, `Classical.choice` and `Quot.sound`; a `sorry`, `native_decide` or an added `axiom` would show up here.
3. It replays the declarations in the kernel with `leanchecker` (`lake env leanchecker EEUL.L112.Chain`), which also catches declarations that bypassed the kernel.

The computational hypotheses remain hypotheses. `./check.sh --fresh` also replays the imported Mathlib modules (about 3 minutes). CI runs it on every pull request.

Once the Mathlib cache is present, the build takes about a minute and 2 GB of memory (measured with Lean 4.34.1: 52 s, 1.7 GB). To cap memory, use a cgroup (for example `systemd-run --user -p MemoryMax=5G`) rather than `ulimit -v`, under which Lean fails to create threads.
