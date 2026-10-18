# Verification data

[日本語](MANIFEST.ja.md)

This directory contains verification data: orbit representatives, coset representatives establishing minimum-norm bounds (certificates), change-of-basis matrices, and supporting data. The main inputs are checked by `code/verify/`; supplementary inputs are identified below. The computational part of the proof uses the checked properties, together with the mathematical lemmas in the paper, and does not rely on the programs that produced the data.

The large `.npz` files are attached to the GitHub Release, not stored in git. `SHA256SUMS`
(in git) fixes their content; every reader in `code/lib/certs.py` checks the hash before use.
Download them with `bash code/verify/fetch.sh`; its optional argument is the Release tag (default `certificates-v1`). The Release is at <https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/releases/tag/certificates-v1>.

File names keep the letter R of an earlier draft for the 112-dimensional lattice (`outer_automorphism_R.txt`, `reduction_R.txt`; also `data/R112_gram_LLL.txt`); the paper calls it L₁₁₂.

All `.npz` files are plain NumPy archives without Python objects; they are read with
`numpy.load(..., allow_pickle=False)`. Vectors are integer row vectors in the basis of
`data/L56_gram.txt`.

| file | array | content | checked by | produced by |
|---|---|---|---|---|
| `reduction_R.txt` | 112 × 112 integers | basis change U with U (3.1) Uᵀ = `data/R112_gram_LLL.txt` | v0 | p6 |
| `reduction_L.txt` | 56 × 56 integers | BKZ-40 basis change of L used by the enumeration | v1 | p6 |
| `min_reps.npz` | `reps` int16 (656, 56) | representatives r_j of the S-orbits on L₆ (F2) | v3 | p2 |
| `centralizer.npz` | `units` int64 (6, 56, 56) | representatives u_k of C/{±1} (§4.2), in the order used for `even_bounding.npz` | v4 | p1 |
| `norm8_reps.npz` | `reps` int16 (254664, 56) | representatives x_i of the S*-orbits on L₈ (F3) | v4 | p3 |
| `odd_bounding.npz` | `w0` int16 (656, 56) | row j: odd-class certificate of r_j τ + 2L (F5a) | v5 | p4 |
| `even_bounding.npz` | `w0` int16 (1527984, 56) | row 6i + k: even-class certificate of x_i u_k τ + 2L (F5b) | v7 | p5 |

Data for cross-checks and supplementary computations:

| file | arrays | content | used by |
|---|---|---|---|
| `commutant.npz` | `basis` int64 (8, 56, 56) | a Z-basis of M' = End_{SL2(29)}(L) | crosscheck/all_data, supplementary |
| `negative_control_B.npz` | `tau_class_B` int64 (56, 56) | an element of M' with τ² = −5 in the other class (gluing B) | supplementary |
| | `tau_B`, `x`, `v`, `hit_pairs` | the gluing map of gluing B as found in the search (a lift modulo 2, not of square −5), a collision (x, v), and the colliding pairs | crosscheck/all_data (negative controls) |
| `outer_automorphism_R.txt` | 112 × 112 integers | an automorphism of L₁₁₂ inducing the outer automorphism of SL₂(29) | supplementary/automorphisms |

Route T (supplement §S4.1, [C21]; not used in the proof of Theorem A):

| file | arrays | content | checked by | produced by |
|---|---|---|---|---|
| `route_t_search3.npz` | `w0` int16 (3936, 56) | certificates for the 3,936 classes r u_k μ + 2L of search (3), order in `code/supplementary/route_t/common.py` | route_t/check.py | route_t/certify.py |
| `route_t_search2.npz` | `w0` int16 (763992, 56), `done` bool (763992) | certificates for the classes x_i u_k (1+τ) + 2L of search (2); rows with `done = False` are not yet computed (zero) | route_t/check.py | route_t/certify.py |

`route_t_search2.npz` is incomplete in this release: the computation was still running when the files were published, and the file will be replaced when it is complete. `check.py` reports how many classes are certified and checks exactly those; the remaining classes are covered only by the floating-point search (`route_t/float_cvp.py`).
