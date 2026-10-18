# 格子を定義する行列

[English](README.md)

| ファイル | 内容 |
|---|---|
| `L56_gram.txt` | 素材となる 56 次元格子 L の Gram 行列 |
| `sl2_29_generators.txt` | L に作用する生成元 2 個 |
| `tau.txt` | 構成に使う自己準同型 |
| `R112_gram_LLL.txt` | 112 次元格子の簡約 Gram 行列 |

ベクトルは整数の**行ベクトル**で、行列は右から作用します。ノルムは長さの二乗です。構成と対応する Gram 行列は論文に定義します。`R112_gram_LLL.txt` への基底変換は `certificates/reduction_R.txt` にあり、`code/verify/v0_inputs.py` が検査します。

`SHA256SUMS` はこの 4 ファイルを固定します。検算プログラムも内部でハッシュを照合します。ハッシュはデータを同定するもので、数学的性質の証明ではありません。
