# An extremal even unimodular lattice in dimension 112

[日本語](README.ja.md)

This repository accompanies a paper constructing a 112-dimensional even unimodular lattice with minimum norm 10. It provides the defining matrices, verification programs, and verification data for the computer-assisted proof.

- **Paper:** [English PDF](paper/paper.en.pdf) · [Japanese PDF](paper/paper.ja.pdf) · [paper and supplement sources and build instructions](paper/README.md)
- **Verification:** [instructions and correspondence with the paper](code/README.md)
- **Data:** [matrix conventions](data/README.md) · [verification data formats and hashes](certificates/MANIFEST.md)
- **Formalisation:** [the argument in Lean](lean/README.md)

## Start here

Run the commands from the repository root. The main verifier needs Python 3.10 or later, NumPy, and a C compiler supporting 128-bit integers, such as GCC or Clang.

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-verify.txt
python3 code/verify/v0_inputs.py
```

The final command checks the defining matrices, the group action, and the change of basis to the distributed Gram matrix. **It does not establish the minimum norm.**

For the computational proof, download the verification data assets for the version being checked, then run:

```bash
bash code/verify/fetch.sh certificates-v1
bash code/verify/full.sh 3
```

The full pipeline includes the enumeration proving that the 56-dimensional base lattice has minimum 6, the completeness checks for orbit representatives, and the checks of coset-minimum certificates. Allow about 26 CPU hours (roughly 9.5–10 hours elapsed with three workers); see the [step-by-step resource requirements](code/README.md#the-verification-steps). The final argument also uses the mathematical lemmas in the paper.

`bash code/verify/quick.sh` is a shorter check. It runs the base-lattice enumerator on positive controls only, so **passing it is not a complete verification of the theorem**. Independent implementations and verification-data generation programs are described in the code documentation.

## Versions and reproducibility

Use the paper, code, and verification data hashes from the same tagged version. Large verification data archives are distributed as release assets; their hashes are recorded in `certificates/SHA256SUMS`. Programs check these hashes before using the data. Generated results are written to `out/`.

Route T in the supplement (§S4) is incomplete in this release: the integer certificates for its search (2) cover only part of the classes, as stated in the [code documentation](code/README.md#route-t-supplement-s4-table-d2-c20-c21), and the file will be replaced when the computation is complete. Theorem A does not depend on it.

The main verification pipeline uses Python, NumPy, and C. Verification-data generation and supplementary computations use SageMath; see [environment.yml](environment.yml). The Lean formalisation checks the deductions from stated hypotheses, rather than executing the lattice computations.

## Authorship and licence

roiban1344 directed the work and is responsible for publication. AI systems, including Claude (Anthropic) and OpenAI Codex, contributed to the research, code, checking, and writing; the paper describes their roles.

Code is distributed under the MIT licence; text and data under CC BY 4.0. See [LICENSE](LICENSE).
