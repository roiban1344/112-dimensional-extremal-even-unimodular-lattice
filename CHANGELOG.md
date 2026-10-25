# Changelog

[日本語](CHANGELOG.ja.md)

Releases are tagged by date (`vYYYY-MM-DD`, with a suffix `.1`, `.2`, … for a second release on the same day). The large verification data are released separately under `certificates-vN` tags. Each entry says first whether a mathematical statement changed; "statements" are the theorems, propositions and facts F0–F5 of the paper and the supplement.

## Unreleased

Statements: unchanged.

- Lean: Mathlib's standard linters, a kernel replay with `leanchecker` in `lean/check.sh`, and a CI job for Lean (#34).

## v2026-10-25 (2026-10-25)

Statements: route T (Supplement §S4), a second proof of extremality that uses the Hermitian structure of L₁₁₂, is now a complete argument (Theorem S4.1). Theorem A, its proof and the input data are unchanged.

- Supplement §S4.1: Theorem S4.1 with proof. Route T reduces, by a further finite check (Proposition S4.3, [C32]), to the same computations F5a and F5b as the main proof; search (2) and the other searches of §S4 become cross-checks (#31). A bound in the first enumeration of route T was corrected from a ≤ 24 to a ≤ 32; the resulting types are unchanged.
- Files of the earlier name R renamed to L112: `data/R112_gram_LLL.txt` → `data/L112_gram_LLL.txt`, `certificates/reduction_R.txt` → `reduction_L112.txt`, `certificates/outer_automorphism_R.txt` → `outer_automorphism_L112.txt`. Header comments changed, matrix entries did not; the hashes in `SHA256SUMS` and `code/lib/data.py` were updated (#32).
- Verification code: certificate files are always checked against the repository's `certificates/SHA256SUMS` (#28); `paper/tools/check-paper.py` uses raising checks (#29); the run time of [C6] corrected to 31 min (#30); shared helpers and the split of `genus.py` (#26, #27).
- Paper PDFs regenerated (#33).

## v2026-10-19.1 (2026-10-19) and certificates-v2

Statements: unchanged. The route-T certificates of search (2) are complete.

- `certificates-v2`: `route_t_search2.npz` covers all 763,992 classes of search (2) (610,664 in `certificates-v1`; the rows present before are unchanged). The other eight `.npz` files are identical to `certificates-v1` (#25).
- Lean: the canonical-form route (`theoremA_canonical`), `lean/check.sh`; §7.1 and Table 9 rewritten (#10).
- The proof path hardened: checks that survive `python -O`, checkpoints bound to their inputs, no stale `out/*.json` (#19); failures show up in exit codes (#18); producers write to `out/` and compare with the distributed data (#15).
- Paper: why min L₅₆ = 6 is re-proved rather than cited (§§1.3, 2.4, 6.1; #22); §8 states the aim of the second enumeration (#24); the record that the group list of `out_facts.g` equals Hiss–Malle Table 3 (#21).
- Containers (`Dockerfile`, `.devcontainer/`, `Dockerfile.sage`; #13); pytest smoke tests in CI (#23); committed PDFs are regenerated once per release (#12).

## v2026-10-18.1 (2026-10-18)

Statements: Supplement §S6 weakened. The lower bounds for the minima of X₁, X₄ and X₅ were removed; only upper bounds are proved. Theorem A is unchanged.

- Supplement §S6 and §7.2 revised after an independent review: the form of X ⊗ ℚ reduced to the orthogonal sum (norm theorem), the dual argument corrected, the identification of the orthogonal-sum classes rewritten, citations of [GHY01] added (#9).
- CI: the paper consistency check and the `checks` workflow (#8).
- READMEs: the prerequisites `python3-venv` and `curl`, and what `fetch.sh` downloads, from a clean verification of the tag (#11).

## v2026-10-18 (2026-10-18)

Statements: unchanged.

- READMEs split into English and Japanese files; the result and its background stated at the entrance; three levels of verification (`v0`, `proof.sh`, `full.sh`); `CITATION.cff` (#2, #6).
- Paper: the two classes of τ described correctly; terms (certificate, implementation, route A) defined; the table of §S6 renumbered to Table S10 (#6, #7).
- Lean: bilingual comments (#3).

## certificates-v1 (2026-10-18)

The first release of the paper and the verification package: the paper and supplement in English and Japanese, the defining matrices, the verification and data-producing code, the Lean formalization of the deduction, and nine verification-data archives (#1). Route T was incomplete: search (2) covered 610,664 of 763,992 classes. Compared with the initial announcement, the headers of `data/tau.txt` and `data/R112_gram_LLL.txt` changed; their matrix entries did not.
