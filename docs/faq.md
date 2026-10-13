# Questions and answers

日本語版: [faq.ja.md](faq.ja.md)

Notation: $\langle x, y \rangle$ is the inner product, and the *norm* of $x$ is $\langle x, x \rangle$ (the squared length).

## How can a real lattice be "multiplied by $\sqrt{-5}$"?

$L$ is an ordinary lattice in real Euclidean space; no complex numbers are needed to define it. "Multiplication by $\sqrt{-5}$" is just a name for a particular linear map $\tau : L \to L$ (here an explicit $56 \times 56$ integer matrix, [`data/tau.txt`](../data/tau.txt)) with

```math
\tau^2 = -5 \cdot \mathrm{id}, \qquad \langle x\tau, y\tau \rangle = 5\,\langle x, y \rangle .
```

The smallest example of the same phenomenon is the square lattice $ℤ^2$ with the rotation by $90^\circ$, $J : (a, b) \mapsto (-b, a)$. It satisfies $J^2 = -\mathrm{id}$ and preserves lengths, and if we *call* $J$ "multiplication by $i$", then $ℤ^2$ becomes the Gaussian integers $ℤ[i]$, with $(a, b) \leftrightarrow a + bi$. The lattice has not changed; we have only chosen one of its symmetries and given it a name.

In the same way, once $\tau$ is chosen, $L$ becomes a module over the ring $ℤ[\sqrt{-5}]$ by $(a + b\sqrt{-5}) \cdot x = ax + bx\tau$, of rank $56/2 = 28$, and the real inner product is the trace of a Hermitian form $h$ with values in $ℚ(\sqrt{-5})$:

```math
\langle x, y \rangle = h(x, y) + \overline{h(x, y)} .
```

A lattice together with such a structure is called a *Hermitian lattice*. Such a $\tau$ is extra structure: most lattices have none, and a lattice may have several inequivalent ones. Here there are two; they give different lattices $R$, one with minimum 8 and one which is the candidate.

## Where does the 56-dimensional representation of $\mathrm{SL}_2(29)$ come from?

(From memory and consistency checks, not from a reference we have verified.) $\mathrm{SL}_2(29)$ has two faithful irreducible complex characters of degree $14 = (29-1)/2$; their values involve $\sqrt{29}$ and they are of quaternionic type. To realise them over $ℚ$ one needs a factor 2 for the two Galois conjugates and another factor 2 for the quaternionic type: $14 \cdot 2 \cdot 2 = 56$. The matrices commuting with the group then form a quaternion algebra over $ℚ(\sqrt{29})$, of dimension 8 over $ℚ$, and $\tau$ is an element of it.
Consistent with this, in our data the commuting algebra has dimension 8, and the generators of orders 5 and 7 have traces $-4$ and $0$ (four times the character values $-1$ and $0$).

## Why "candidate"?

Because the minimum of a lattice of dimension 112 cannot at present be computed directly, and the argument given here, although finite and checkable, has been checked only by computer programs written by AI sessions. See "What could be wrong" in the [README](../README.md).

## What would refute the claim?

A single vector of $R$ of norm 2, 4, 6 or 8. In the notation of the README this is a pair $(x, v)$ with $x \in L$, $v \equiv x\tau \pmod{2L}$ and $\langle x, x \rangle + \langle v, v \rangle \le 16$.
