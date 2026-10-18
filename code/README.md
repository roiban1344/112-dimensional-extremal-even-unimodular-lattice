# Code for “An extremal even unimodular lattice in dimension 112”

[日本語版](README.ja.md)

This directory contains every computation used in the paper. Table D2 of the paper lists them
as [C1]–[C31]; the last section of this file maps each row to the scripts here.

## What is proved, and what it relies on

Theorem A (L₁₁₂ has minimum 10) follows from the results proved by hand in §§3–6 (Lemmas 3.2,
4.2, 5.1, Corollaries 4.3, 5.2, 5.3 and Proposition 6.3), the known upper bound (1.1) and the
computational facts F0–F5 of §4.3. The deduction from the computational facts (Lemma 4.2,
Corollary 4.3, Lemma 5.1 with its corollaries, and the final step) is also checked in Lean
(`lean/`, Table 9 of §7.1). Lemma 3.2 (unimodularity), Proposition 6.3 and the passage from pairs
(x, xτ + 2y) to vectors of L₁₁₂ through (1.2) remain outside Lean, together with the other items
listed in §7.1. The scripts in **`verify/`** check F0–F5 from two kinds of input:

* the four published files in `data/` (the Gram matrix of L, the generators of SL₂(29), τ, and a
  reduced Gram matrix of L₁₁₂), whose SHA-256 hashes are fixed in `lib/data.py`;
* the **verification data** in `certificates/` (orbit representatives, coset representatives
  establishing minimum-norm bounds, and change-of-basis matrices; see `certificates/MANIFEST.md`), whose hashes are fixed in
  `certificates/SHA256SUMS`.

We use **verification data** for the distributed auxiliary inputs as a whole. A **certificate** here is a coset representative that establishes a lower bound on the minimum norm of that coset: each row of `odd_bounding.npz` or `even_bounding.npz` is such a representative. The checker verifies its coset membership, norm and inner-product conditions; the lemmas in the paper then give the bound. Orbit representatives and change-of-basis matrices are named separately.

The proof of Theorem A relies on the verification code and the hand-proved results. The
verification code consists of about 2,000 lines of Python (`verify/` v0–v7 and `lib/`, counting the
bilingual header comments) and one C program; the Python code uses no package other than numpy.
The proof does **not** rely on the correctness of the code that produced the verification data
(`produce/`): any property of the data that the proof uses is re-checked by `verify/`.

## Layout

| directory | content |
|---|---|
| `lib/` | small shared library (numpy only): reading the data, exactness guards, the group, canonical forms modulo 2, minimal vectors |
| `verify/` | the checks of F0–F5 (v0–v7) and a consistency test (v8) |
| `produce/` | how the verification data were produced (p1–p6); not needed to check the proof |
| `crosscheck/` | second implementations of the checks, written separately with Claude without reading `verify/`, `produce/` or `lib/`. They check the same data by different code, so an error in the main implementation would show up as a disagreement: `all_data/` (all verification data and F1, by a different method) and `second_impl/` (canonical forms, design identities, the odd classes) |
| `supplementary/` | computations behind statements of the paper that are not used in the proof of Theorem A (the classification of gluings, the automorphism group, …) |

## Running verification

Prepare the [requirements](#requirements), then run these commands from the repository root. Python environment setup is described in the [root README](../README.md#start-here). There are three levels of checking.

**(i) Inputs only.** First check the defining matrices and group action (about 20 seconds; no additional data download). This does not establish the minimum norm.

```bash
python3 code/verify/v0_inputs.py
```

**(ii) The computational part of the proof.** Download the large verification data files, then run `proof.sh`. It takes about 1.2 CPU hours (v1 is 34 minutes, v6 is 24 minutes, the others are minutes) and runs v0–v6: F1 by interval enumeration, F2 and F3 (orbit completeness), F5a by the odd-coset certificates, and F5b by canonical forms. This is the shortest complete check of the computational facts F0–F5 used in the proof of Theorem A (route A of supplement Table S7).

```bash
bash code/verify/fetch.sh
bash code/verify/proof.sh
```

The optional argument of `fetch.sh` is the Release tag (default `certificates-v1`).

**(iii) Everything.** The full check takes about 26 CPU hours, or roughly 9.5–10 hours elapsed with three workers. It runs everything in `proof.sh`, and adds the alternative check of F5b by the even-coset certificates (v7, about 24 CPU hours) and the consistency test of the spherical-design identities (v8).

```bash
bash code/verify/full.sh 3
```

`bash code/verify/quick.sh` (about 40–50 minutes) is an abbreviated check. It runs F1 only on the positive controls and omits v7 and v8, so passing it is not a complete verification of the theorem.

Each step prints `[ok]`/`[FAIL]` for every check and writes `out/<step>.json` with the results, software versions and running time. A step removes its old `out/<step>.json` when it starts, and a step that stops on an error (for example a hash mismatch) writes `"passed": false` with the error, so the file never shows a stale pass; the exit code (nonzero on any failure) is the primary verdict. The shell scripts run Python with `-I` (isolated mode), and the library refuses to run under `python -O`.

## The verification steps

Times were measured on the machine used for the paper (8 cores, 15 GB, shared with other jobs).

| step | paper | what is checked | time | memory |
|---|---|---|---|---|
| `v0_inputs.py` | F0, F4, Lemma 3.2 | L even unimodular; g₁, g₂ preserve G, generate a group of order 24,360 containing −I, commute with τ; τ² = −5, τGτᵀ = 5G; (3.1) even unimodular; the distributed Gram matrix of L₁₁₂ is the same lattice | 20 s | < 1 GB |
| `v1_min_L.py` + `enum_interval.c` | F1, §6.1 (a), Table 5 | min L = 6 by an interval-arithmetic enumeration that cannot miss vectors; positive controls E₈, Leech, Leech ⊥ Leech ⊥ E₈ | 34 min | < 1 GB |
| `v2_theta.py` | §2.3, App. B; supplement §S1, §S2 | extremal theta series (\|L₆\|, \|L₈\|), Siegel means, Tables B1, S1, S2, S4, S5 | 1 s | — |
| `v3_minimal_orbits.py` | F2, §6.2 | the 656 orbits cover the 15,590,400 minimal vectors (by expansion and by canonical forms) | 3 min | 2 GB |
| `v4_norm8_orbits.py` | F3, §6.4 | the 1,527,984 vectors x_i u_k give 1,517,130 distinct regular orbits covering \|L₈\| | 9 min | 2 GB |
| `v5_odd_bounding.py` | F5a, Cor. 5.2, Table 7 | 656 odd-class certificates | 2.5 min | 2 GB |
| `v6_canonical_lookup.py` | F5b, Prop. 6.3, Table 6 | no class x_i u_k τ + 2L contains a norm-8 vector (canonical forms); also type (6,6) | 24 min | 2 GB |
| `v7_even_bounding.py` | F5b, Cor. 5.3, Table 8 | 1,527,984 even-class certificates (resumable, with the checkpoint bound to the inputs by SHA-256; `--threads`) | 24 CPU h (7.9 h with 3 threads) | 3 GB |
| `v8_design_identities.py` | §6.3 | 18 spherical-design identities (consistency test, not needed for the proof) | 14 min | 2 GB |

F5b is checked twice by unrelated arguments (v6 and v7); either one suffices for the proof.

### How exactness is ensured

All decisions are made in integer arithmetic. Where a matrix product of integer matrices is
computed in floating point (for speed), the code first checks from the actual inputs that every
partial sum is an integer below 2²⁴ (float32) or 2⁵³ (float64); such products are exact. The
helpers are in `lib/exact.py`; each script's header states which products it computes this way.
These guards, and the other conditions a result depends on (no int64 overflow, a complete expansion
or enumeration), are written as `require(...)`, which raises an error, not as `assert`, which
`python -O` would remove; in addition a step run under `-O` refuses to start (it removes its old `out/<step>.json` and records the refusal there).
The enumeration of F1 uses outward-rounded interval arithmetic (`verify/enum_interval.c`, header).

## Requirements

* `verify/`, `crosscheck/second_impl/`: Python ≥ 3.10 with numpy (tested with Python 3.12, numpy 2.5),
  a C compiler with 128-bit integers (gcc or clang; `$CC` if set, otherwise the first of `cc`, `gcc`, `clang`) for v1, and `curl` for `fetch.sh`. No other package.
* `produce/`, `supplementary/`, `crosscheck/all_data/`: SageMath 10 (which includes PARI/GP, GAP and
  fpylll); tested with SageMath 10.9. `environment.yml` at the repository root installs it with
  conda/micromamba. Run these scripts with the `python3` of that environment (`python3 -I code/...`);
  `sage -python` is not available in the conda-forge build of SageMath.
* Container: the `Dockerfile` at the repository root builds an image with these requirements for `verify/` (and `Dockerfile.sage` one with SageMath); see the root README.
* `lean/`: Lean 4 and Mathlib (versions pinned in `lean/lean-toolchain` and `lean/lake-manifest.json`).

## Producing the verification data

| script | produces | time |
|---|---|---|
| `produce/p1_centralizer.py` | M′ and the centralizer C (`centralizer.npz`, `commutant.npz`) | 10 min |
| `produce/p2_minimal_orbits.py` | `min_reps.npz` (closure, §6.2) | 10 min |
| `produce/p3_norm8_orbits.py` | `norm8_reps.npz` (marked elements (sums of two minimal vectors), §6.4) | 1.2 h |
| `produce/p4_odd_descent.py` | `odd_bounding.npz` (descent, §6.6) | 6 min |
| `produce/p5_even_descent.py` | `even_bounding.npz` (descent, §6.7; 6 parts, resumable) | ≈ 190 CPU h |
| `produce/p6_reduction.py` | `reduction_L.txt`, `reduction_R.txt` | 1 min |

The producers never write to `certificates/`, whose files are fixed by `certificates/SHA256SUMS`: each
writes its files under `out/p<k>/` with the names of the distributed files (for example
`out/p4/odd_bounding.npz`) and then compares them with the distributed verification data; a difference is
reported as `[FAIL]` with exit code 1. p4, p5 and p6 must reproduce the distributed files bit for bit
(p6 compares the text files byte for byte). p1 compares the 6 elements of C/{±1} as a set up to sign and the
basis of M′ by the Z-lattice it spans (equal Hermite normal forms). p2 and p3 may choose other
representatives: p2 compares the set of canonical forms of the classes r + 2L (for minimal vectors this
means the same orbits) and the number of representatives; p3 compares the set of canonical forms of the
classes x u_k + 2L, the number of orbits and the multiset of orbit sizes. Test runs (`p3 --trial`,
`p5 --limit`) use their own file names and never overwrite the files or checkpoints of a full run.

The data-producing steps of `supplementary/genus/genus.py` (`enum`, `build`, `witness`, `identify`) write to
`out/genus/` by default, not to `certificates/`, and compare each file with the distributed one (identical, the
same integers, or different; `genus_classes.txt` must agree, the other files may differ with the random walk or
PARI's enumeration order). `--dest certificates/` replaces the distributed files.

## Second implementations and supplementary computations

`crosscheck/all_data/check_all.py <step>` (Python with SageMath, see the docstring) runs the steps
`theta`, `v0`, `v1` (it builds the table of minimal vectors used by the later steps), `v2`, `v3cheap`,
`v4`, `v3full`, `neg` and `summary` in this order. Each step ends with exit code 1 if its verdict is
FAIL; `summary` ends with exit code 1 unless every required step has passed on the current inputs
(the inputs are checked against `SHA256SUMS`, and the caches are kept per input digest).
`min_L.py 4` and `min_L.py 4 --test e8x7` check F1 and its positive control. The three scripts of
`crosscheck/second_impl/` (numpy only) compare their results with the numbers of the paper and end
with `RESULT: PASS` (exit code 0) or `RESULT: FAIL` (exit code 1).

`bash code/run_supplementary.sh [names…]` runs the computations of `supplementary/` (all of them
by default; the list and what is left out are in its header). It needs a Python with SageMath as
`PYTHON` (default `python3`, for example that of the conda environment of `environment.yml`;
`PYTHON="sage -python"` for a SageMath distribution), GAP with CTblLib as `GAP` (default `gap`), the
data downloaded by `fetch.sh`, and, for the step `gluing_b`, the file `out/K8.npy` written by
`verify/v4_norm8_orbits.py`. A failing step does not stop the others; at the end the failed steps are
listed and the exit code is 1.

## Route T (supplement §S4, Table D2 [C20], [C21])

`supplementary/route_t/` contains the computations of the supplementary argument using the hermitian
structure of L₁₁₂ (route T). They are not used in the proof of Theorem A.

| script | content | time |
|---|---|---|
| `classify.py`, `recount.py` | [C20] classification of the rank-2 support modules (two independent counts: 97 types, 63 dangerous; 58 types at the level of a coarser invariant, identical) | 1–2 min each (SageMath) |
| `certify.py` | [C21] producing the certificates of searches (2) and (3) (split, resumable) | search (3) about 25 min, search (2) about 13 CPU days |
| `check.py` | [C21] checking the certificates in integer arithmetic (numpy only) | search (3) about 2 min, search (2) about 12 CPU hours when complete |
| `float_cvp.py` | [C21] search (2) by floating-point closest-vector enumeration (supplementary) | about 3 × 13 hours (SageMath) |

**State of this release**: the certificates of search (3) are complete (all 3,936 classes). The
computation for search (2) was still running when the files were published, and
`certificates/route_t_search2.npz` is incomplete (`check.py` reports how many of the 763,992 classes
are certified). The remaining classes are covered only by the floating-point search. The file will
be replaced when the computation is complete. To complete it yourself, run `certify.py search2 --missing --part P --nparts Q`
for P = 0, …, Q−1 (only the classes without a certificate; resumable), then
`certify.py collect --base` to add them to the distributed file, and `check.py` again.

## Correspondence with Table D2 of the paper

| Table D2 | scripts |
|---|---|
| [C1] | verify/v2_theta.py |
| [C2] | verify/v0_inputs.py, supplementary/gluings.py (d), produce/p1_centralizer.py |
| [C3] | supplementary/gluings.py, supplementary/nebe/gluings_m.py (a), (b) |
| [C4] | supplementary/gluing_b.py, supplementary/nebe/gluings_m.py (c), (d) |
| [C5] | verify/v1_min_L.py + verify/enum_interval.c, produce/p6_reduction.py |
| [C6] | supplementary/nebe/reduction_to_nebe.py (with nebe/lattices.py, nebe/tables.py) |
| [C7] | supplementary/float_enumerations.py svp, qfminim |
| [C8] | produce/p2_minimal_orbits.py, verify/v3_minimal_orbits.py, verify/v8_design_identities.py |
| [C9] | produce/p3_norm8_orbits.py, verify/v4_norm8_orbits.py, verify/v8_design_identities.py |
| [C10] | produce/p4_odd_descent.py, verify/v5_odd_bounding.py, crosscheck/second_impl/odd_classes.py |
| [C11] | verify/v6_canonical_lookup.py, crosscheck/second_impl/even_classes.py |
| [C12] | supplementary/float_enumerations.py cvp610, cvp88 |
| [C13] | produce/p5_even_descent.py, verify/v7_even_bounding.py |
| [C14] | supplementary/frame_stabilizer.py |
| [C15] | supplementary/sample_check.py |
| [C16] | supplementary/node_estimate.py |
| [C17] | supplementary/frames.py |
| [C18] | supplementary/fixed_sublattices.py (`--tau B` for gluing B; BKZ-20 to BKZ-60 by default: about 10 min for L₁₁₂ and 18 min for B, mostly BKZ-60; `--bkz 30,40` under a minute) |
| [C19] | supplementary/anatomy_b.py |
| [C20] | supplementary/route_t/classify.py, recount.py (with route_t/hermitian.py) |
| [C21] | supplementary/route_t/certify.py, check.py, float_cvp.py (with route_t/common.py) |
| [C22] | lean/ (EEUL/L112/Chain.lean, check.sh) |
| [C23] | supplementary/nebe/identify_nebe.py (with nebe/lattices.py, nebe/cycloquat.py) |
| [C24] | supplementary/automorphisms/aut_normalizer.py |
| [C25] | supplementary/automorphisms/group_facts.g, out_facts.g, aut_diagonal.py |
| [C26] | supplementary/automorphisms/aut_structure.py, aut_character.py, endomorphisms.py |
| [C27] | crosscheck/all_data/check_all.py, min_L.py, min_L_enum.c |
| [C28] | supplementary/isometry_ab.py (find, check) |
| [C29] | supplementary/genus/genus.py local, mass, enum |
| [C30] | supplementary/genus/genus.py build, frames, witness |
| [C31] | supplementary/genus/genus.py identify, check |
