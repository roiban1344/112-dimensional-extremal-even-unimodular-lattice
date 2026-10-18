# An extremal even unimodular lattice in dimension 112

[日本語](README.ja.md)

This repository accompanies a paper constructing a 112-dimensional even unimodular lattice with minimum norm 10. It provides the defining matrices, verification programs, and verification data for the computer-assisted proof.

- **Paper:** [English PDF](paper/paper.en.pdf) · [Japanese PDF](paper/paper.ja.pdf) · [paper and supplement sources and build instructions](paper/README.md)
- **Verification:** [instructions and correspondence with the paper](code/README.md)
- **Data:** [matrix conventions](data/README.md) · [verification data formats and hashes](certificates/MANIFEST.md)
- **Formalization:** [the argument in Lean](lean/README.md)

## Start here

Run the commands from the repository root. The main verifier needs Python 3.10 or later, NumPy, and a C compiler supporting 128-bit integers, such as GCC or Clang. There are three levels of checking.

**(i) Inputs only (20 seconds).**

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

`fetch.sh` takes the Release tag as an optional argument (default `certificates-v1`). `proof.sh` runs every computational check used in the proof of Theorem A: F1 (the 56-dimensional base lattice has minimum 6) by interval enumeration, F2 and F3 (completeness of the orbit representatives), F5a by the odd-coset certificates, and F5b by canonical forms. The final argument also uses the mathematical lemmas in the paper. See the [step-by-step resource requirements](code/README.md#the-verification-steps).

**(iii) Everything (about 26 CPU hours, roughly 9.5–10 hours elapsed with three workers).**

```bash
bash code/verify/full.sh 3
```

This runs everything in `proof.sh`, and adds the alternative check of F5b by the even-coset certificates (v7, about 24 CPU hours) and the consistency test of the spherical-design identities (v8).

`bash code/verify/quick.sh` is a shorter check of about 40–50 minutes. It runs the base-lattice enumerator on positive controls only and omits v7, so **passing it is not a complete verification of the theorem**. Independent implementations and verification-data generation programs are described in the code documentation.

## Versions and reproducibility

Releases are tagged by date (`v2026-10-DD`). Take the paper, the code, and the verification-data hashes from the same tag. Large verification data archives are distributed as assets of the [Release `certificates-v1`](https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/releases/tag/certificates-v1); their hashes are recorded in `certificates/SHA256SUMS`. Programs check these hashes before using the data. Generated results are written to `out/`.

To cite this work, use GitHub's "Cite this repository", which reads [CITATION.cff](CITATION.cff).

Route T in the supplement (§S4) is incomplete in this release: the integer certificates for its search (2) cover only part of the classes, as stated in the [code documentation](code/README.md#route-t-supplement-s4-table-d2-c20-c21), and the file will be replaced when the computation is complete. Theorem A does not depend on it.

The main verification pipeline uses Python, NumPy, and C. Verification-data generation and supplementary computations use SageMath; see [environment.yml](environment.yml). The Lean formalization checks the deductions from stated hypotheses, rather than executing the lattice computations.

## Authorship and license

roiban1344 directed the work and is responsible for publication. AI systems, including Claude (Anthropic) and OpenAI Codex, contributed to the research, code, checking, and writing; the paper describes their roles.

Code is distributed under the MIT license; text and data under CC BY 4.0. See [LICENSE](LICENSE).
