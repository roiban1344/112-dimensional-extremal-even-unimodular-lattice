# Changelog

[日本語](CHANGELOG.ja.md)

Releases are tagged by date (`vYYYY-MM-DD`, with a suffix `.1`, `.2`, … for a second release on the same day). The large verification data are released separately under `certificates-vN` tags. Each entry says first whether a mathematical statement changed; "statements" are the theorems, propositions and facts F0–F5 of the paper and the supplement.

## v2026-11-02 (2026-11-02)

Statements: Theorems A and B and the facts F0–F5 are unchanged, and so are the input data and the verification data. Proposition 3.3 says more (the parity-preserving maps are the elements of reduced norm 1, and the sizes of the classes are given), and parts (a) and (c) now have a proof without a computer. Theorem S6.1(c) now says that the minimum of X₁ is not determined in this paper.

- Corrections to the paper: the account of [Neb98] in §2.4 (Table II of [Neb98] gives the 15,590,400 minimal vectors only for `L_{56,2}(M)`); the node count for Λ₂₄ ⊥ Λ₂₄ ⊥ E₈ in Table 5, from 11,081,124 to 14,101,914; dimension 88 brought up to date: the Catalogue lists six extremal lattices (#40).
- Paper, prior work: §1.4 rewritten with the prior constructions and a paragraph on [Neb98, §5] whose case (5, 29) is checked by the new computation [C33]; original sources in Table G1 and more bibliographic data (#40).
- Supplement §S6 and §3.3: the scope of the classification stated, the hypotheses of the mass formula of [GHY01] matched item by item, with two normalization checks (#41). I. Gauvin's independent verification that X₁ has minimum 10 is cited [Gau26v]; this paper does not determine the minimum of X₁ and does not depend on that result (#42).
- Theorem B and Appendix F: the use of the tables of Hiss–Malle can now be checked from the text (Table F1, with a second route to the list); the inputs of the proof are listed, and the classification of finite simple groups is named in the abstract; the strategy is credited to Nebe (#43).
- What the proof rests on: §1.3 on the scale of the computation, the rounding model of F1 in §6.1, which computed facts prove F2 and F3 (§6.4), the hypotheses of the Lean statements mapped to the checks (Table 9, continued), and the SHA-256 of `certificates/SHA256SUMS` in Appendix D (#47).
- The sampled checks reported in the paper are now distributed code (`crosscheck/second_impl/minimal_orbits.py` in [C8], `crosscheck/second_impl/coset_enumeration.py` in [C11], and in the new row [C34] `supplementary/k8_checks.py` and step (e) of `supplementary/nebe/gluings_m.py`). The check called "implementation 3" is removed from the paper and the READMEs because its code is not available; no statement rested on it alone (#47). `paper/tools/check-paper.py` now refuses a row of Table D2 without distributed code (#52).
- Verification code: two new controls in v1: E₈ in skewed bases, which detects an enumerator without outward rounding, and 60 random positive definite forms compared with exhaustive search, which test vectors of norm equal to the radius and the sign rule (#44); p3 reproduces `certificates/norm8_reps.npz` bit for bit; `out/<step>.json` has a new format 2, with the code, inputs, BLAS and compiler; a preflight check in `proof.sh`, `full.sh` and `quick.sh`; the JSON records of the supplementary scripts are named after the steps of `run_supplementary.sh` (#46).
- CI and pinning: lint job, tests on more Python versions and on macOS, the `proof` workflow (its record is attached to the Release of each tag), second implementations in `data-tests`, numpy pinned with hashes and images by digest, PDFs reproducible with `--creation-timestamp` (#45).
- Documentation: Figure 1 redrawn (#35); a map of the repository and file tables in the READMEs (#36); this changelog, how to report an error, and separate license files (#37); the use of AI tools (#39). Lean: Mathlib's standard linters, a kernel replay with `leanchecker` in `lean/check.sh`, and a CI job (#34).
- Paper PDFs regenerated.

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
