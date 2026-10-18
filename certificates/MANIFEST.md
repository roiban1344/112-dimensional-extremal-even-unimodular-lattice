# Verification data

[日本語](MANIFEST.ja.md)

This directory contains verification data: orbit representatives, coset representatives establishing minimum-norm bounds (certificates), change-of-basis matrices, and supporting data. The main inputs are checked by `code/verify/`; supplementary inputs are identified below. The computational part of the proof uses the checked properties, together with the mathematical lemmas in the paper, and does not rely on the programs that produced the data.

The large `.npz` files are attached to the GitHub Release, not stored in git. `SHA256SUMS`
(in git) fixes their content; every reader in `code/lib/certs.py` checks the hash before use.
Download them with `bash code/verify/fetch.sh`; its optional argument is the Release tag (default `certificates-v2`). The Release is at <https://github.com/roiban1344/112-dimensional-extremal-even-unimodular-lattice/releases/tag/certificates-v2>.

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
| `gram_A.txt` | 112 × 112 integers | Gram matrix G_A of gluing A (Nebe's L_{56,2}(M) glued by a lift of a map in the class of 48), in the basis (3.1) | supplementary/isometry_ab.py ([C28]) |
| `isometry_AB.txt` | 112 × 112 integers | basis change T with T G_B Tᵀ = G_A, det T = ±1 (G_B = (3.1) for tau_class_B), an isometry from gluing A onto gluing B | supplementary/isometry_ab.py ([C28]) |
| `genus_classes.txt` | 8 lines of 9 integers | the 8 classes Λ_j of the genus of rank-2 unimodular Hermitian lattices over the maximal order of L_{56,2}(M): j, \|U(Λ_j)\| (PARI `qfauto`) and the numbers of short vectors of Λ_j | supplementary/genus/genus.py ([C29], [C31]) |
| `genus_class_<j>.txt` (j = 0, …, 7) | 112 × 112 integers | Gram matrix G_X of X_j = L_{56,2}(M) ⊗ Λ_j, LLL-reduced | supplementary/genus/genus.py ([C30], [C31]) |
| `genus_basis_<j>.txt` (j = 0, …, 7) | d, then 112 × 112 integers D | the basis D/d of X_j in the coordinates of (3.1) (L ⊕ L, form diag(G, G)/2): D diag(G, G) Dᵀ = 2d² G_X; g₁, g₂ act on X_j | supplementary/genus/genus.py ([C30], [C31]) |
| `genus_witnesses.txt` | 3 lines of 113 integers | class j and a vector v of X_j with v G_X vᵀ = 8 (j = 3, 4, 5) | supplementary/genus/genus.py ([C30], [C31]) |
| `genus_isometry_7_L112.txt` | 112 × 112 integers | T with T G_R Tᵀ = G_X (class 7), det T = ±1, G_R = (3.1): class 7 is L₁₁₂ | supplementary/genus/genus.py ([C31]) |
| `genus_isometry_3_A.txt` | 112 × 112 integers | T with T G_A Tᵀ = G_X (class 3), det T = ±1: class 3 is gluing A | supplementary/genus/genus.py ([C31]) |

Route T (supplement §S4.1, [C21]; not used in the proof of Theorem A):

| file | arrays | content | checked by | produced by |
|---|---|---|---|---|
| `route_t_search3.npz` | `w0` int16 (3936, 56) | certificates for the 3,936 classes r u_k μ + 2L of search (3), order in `code/supplementary/route_t/common.py` | route_t/check.py | route_t/certify.py |
| `route_t_search2.npz` | `w0` int16 (763992, 56), `done` bool (763992) | certificates for all 763,992 classes x_i u_k (1+τ) + 2L of search (2), order in `code/supplementary/route_t/common.py`; `done` is True on every row (kept so that a partial file can be completed with `certify.py search2 --missing`) | route_t/check.py | route_t/certify.py |

`route_t_search2.npz` is complete from Release `certificates-v2` on (all 763,992 classes; `certificates-v1` had 610,664). The rows present in `certificates-v1` are unchanged. `check.py` checks every row.
