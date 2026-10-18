# Defining matrices

[日本語](README.ja.md)

| File | Contents |
|---|---|
| `L56_gram.txt` | Gram matrix of the 56-dimensional base lattice |
| `sl2_29_generators.txt` | Two matrices acting on the base lattice |
| `tau.txt` | Endomorphism used in the construction |
| `R112_gram_LLL.txt` | Reduced Gram matrix of the 112-dimensional lattice |

Vectors are integer **row vectors**. Matrices act on the right. Norm means squared length. The paper defines the construction and the corresponding Gram matrix. The basis change to `R112_gram_LLL.txt` is provided in `certificates/reduction_R.txt` and checked by `code/verify/v0_inputs.py`.

`SHA256SUMS` fixes these four files. The verifier also checks their hashes internally. Checksums identify the data; they do not prove its mathematical properties.
