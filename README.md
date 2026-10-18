# An extremal even unimodular lattice in dimension 112

[日本語](README.ja.md)

This repository accompanies a paper constructing a 112-dimensional even unimodular lattice with minimum norm 10. It provides the defining matrices, verification programs, and verification data for the computer-assisted proof.

- **Paper:** [English PDF](paper/paper.en.pdf) · [Japanese PDF](paper/paper.ja.pdf) · [paper and supplement sources and build instructions](paper/README.md)
- **Verification:** [instructions and correspondence with the paper](code/README.md)
- **Data:** [matrix conventions](data/README.md) · [verification data formats and hashes](certificates/MANIFEST.md)
- **Formalization:** [the argument in Lean](lean/README.md)

## Result

Theorem A of the paper: the lattice L₁₁₂ defined by the data in this repository is a positive-definite even unimodular lattice of dimension 112 whose minimum norm is 10. Since 10 is the largest value that the Mallows–Odlyzko–Sloane bound 2⌊n/24⌋+2 allows in dimension 112, L₁₁₂ is extremal. Theorem B determines its automorphism group, of order 1,169,280. Supplement §S6 classifies all even unimodular lattices of dimension 112 on which SL₂(29) acts as on L₁₁₂: there are exactly eight up to equivariant isometry, L₁₁₂ among them, and all but one of the others contain a vector of norm at most 8.

The construction glues two copies of a 56-dimensional extremal lattice of Nebe, which carries the symmetry group SL₂(29), along an endomorphism τ with τ² = −5 that commutes with the group; equivalently, L₁₁₂ is a Hermitian tensor product over ℤ[√−5]. The proof is computer-assisted. Lemmas proved by hand reduce extremality to finitely many lower bounds for cosets modulo 2L₅₆, and programs check these bounds in integer arithmetic from the distributed data (about 1.2 CPU hours). The deduction from the checked facts to the theorem is formalized in Lean 4.

The paper is a draft and has not been peer reviewed. AI systems did most of the computation, code and writing under human direction (see "Authorship" below).

## Background

An even unimodular lattice is a lattice in ℝⁿ all of whose vectors have even squared length (norm) and whose Gram matrix has determinant 1. Such lattices exist only when n is a multiple of 8. The theory of modular forms bounds their minimum norm by 2⌊n/24⌋+2, and a lattice attaining this bound is called extremal: its shortest nonzero vectors are as long as the theory allows, so it is as dense a sphere packing as an even unimodular lattice of that dimension can be. Extremal lattices are rare. The classical examples are E₈ (n = 8) and the Leech lattice (n = 24). Examples are known in every dimension that is a multiple of 8 up to 80 (dimension 80 since 1998, by Bachoc and Nebe; dimension 72 since 2010, by Nebe) and in dimension 88 since a 2026 preprint of Sakamoto. Dimensions 96 and 104 are open. L₁₁₂ is the first known example beyond 88, and the first for which the bound is 10. Dimension 112 was chosen over 96 and 104 because a heuristic based on Siegel's mass formula suggests that an extremal lattice is easiest to find there (Supplement §S1).

## Start here

Run the commands from the repository root. The main verifier needs Python 3.10 or later, NumPy, and a C compiler supporting 128-bit integers, such as GCC or Clang. There are three levels of checking.

**(i) Inputs only (20 seconds).** On Debian and Ubuntu, `python3 -m venv` needs the package `python3-venv`.

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-verify.txt
python3 code/verify/v0_inputs.py
```

The last command checks the defining matrices, the group action, and the change of basis to the distributed Gram matrix. **It does not establish the minimum norm.**

**(ii) The computational part of the proof (about 1.2 CPU hours).** Download the verification data assets for the version being checked, then run:

```bash
bash code/verify/fetch.sh
bash code/verify/proof.sh
```

`fetch.sh` needs `curl`; it takes the Release tag as an optional argument (default `certificates-v1`) and downloads every `.npz` file listed in `certificates/SHA256SUMS` (nine files, about 130 MB), including those used only by `full.sh` and the supplementary checks. `proof.sh` runs every computational check used in the proof of Theorem A: F1 (the 56-dimensional base lattice has minimum 6) by interval enumeration, F2 and F3 (completeness of the orbit representatives), F5a by the odd-coset certificates, and F5b by canonical forms. The final argument also uses the mathematical lemmas in the paper. See the [step-by-step resource requirements](code/README.md#the-verification-steps).

**(iii) Everything (about 26 CPU hours, roughly 9.5–10 hours elapsed with three workers).**

```bash
bash code/verify/full.sh 3
```

This runs everything in `proof.sh`, and adds the alternative check of F5b by the even-coset certificates (v7, about 24 CPU hours) and the consistency test of the spherical-design identities (v8).

`bash code/verify/quick.sh` is a shorter check of about 40–50 minutes. It runs the base-lattice enumerator on positive controls only and omits v7, so **passing it is not a complete verification of the theorem**. Independent implementations and verification-data generation programs are described in the code documentation.

## Versions and reproducibility

Releases are tagged by date; this release is `v2026-10-18.1` (a second release on the same day gets a suffix). Take the paper, the code, and the verification-data hashes from the same tag. Large verification data archives are distributed as assets of the [Release `certificates-v1`](https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/releases/tag/certificates-v1); their hashes are recorded in `certificates/SHA256SUMS`. Programs check these hashes before using the data. Generated results are written to `out/`.

To cite this work, use GitHub's "Cite this repository", which reads [CITATION.cff](CITATION.cff).

Route T in the supplement (§S4) is incomplete in this release: the integer certificates for its search (2) cover only part of the classes, as stated in the [code documentation](code/README.md#route-t-supplement-s4-table-d2-c20-c21), and the file will be replaced when the computation is complete. Theorem A does not depend on it.

The main verification pipeline uses Python, NumPy, and C. Verification-data generation and supplementary computations use SageMath; see [environment.yml](environment.yml). The Lean formalization checks the deductions from stated hypotheses, rather than executing the lattice computations.

## Authorship and license

roiban1344 directed the work and is responsible for publication. AI systems, including Claude (Anthropic) and OpenAI Codex, contributed to the research, code, checking, and writing; the paper describes their roles.

Code is distributed under the MIT license; text and data under CC BY 4.0. See [LICENSE](LICENSE).
