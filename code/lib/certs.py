"""Certificate files: the data that the verification scripts check (see certificates/MANIFEST.md; 日本語は MANIFEST.ja.md).
検証用データ: 検算スクリプトが確かめるデータ（certificates/MANIFEST.ja.md を参照）。

  min_reps.npz       reps  int16 (656, 56)       representatives of the S-orbits on L_6 (F2)
                                                 L_6 の S-軌道の代表（F2）
  centralizer.npz    units int64 (6, 56, 56)     representatives of C/{+-1} (paper §4.2)
                                                 C/{±1} の代表（論文 §4.2）
  commutant.npz      basis int64 (8, 56, 56)     a Z-basis of M' = End_{SL2(29)}(L) (produce/p1, supplementary,
                                                 crosscheck/all_data; not read by verify/)
                                                 M' = End_{SL2(29)}(L) の Z-基底（produce/p1、supplementary、
                                                 crosscheck/all_data が使う。verify/ は読まない）
  norm8_reps.npz     reps  int16 (254664, 56)    representatives x_i of the S*-orbits on L_8 (F3)
                                                 L_8 の S*-軌道の代表 x_i（F3）
  odd_bounding.npz   w0    int16 (656, 56)       odd-class certificate of r_j tau + 2L, row j (F5a)
                                                 r_j tau + 2L の奇の類の certificate（第 j 行）（F5a）
  even_bounding.npz  w0    int16 (1527984, 56)   even-class certificate of x_i u_k tau + 2L
                                                 in row 6 i + k (F5b)
                                                 x_i u_k tau + 2L の偶の類の certificate（第 6i+k 行）（F5b）
  reduction_L.txt    U     (56 x 56 integers)    BKZ-40 basis change of L used by the enumeration (F1)
                                                 列挙（F1）に使う L の BKZ-40 の基底変換
  reduction_R.txt    U     (112 x 112 integers)  basis change from (3.1) to data/R112_gram_LLL.txt
                                                 (3.1) から data/R112_gram_LLL.txt への基底変換

The file certificates/SHA256SUMS of the repository lists the hash of every file; `load` checks it. The files
may be read from another directory (--certificates DIR), but they are still checked against the repository's
SHA256SUMS; another list of hashes is used only when named explicitly (--hashes FILE, e.g. for tests on
modified data).
.npz files are read with allow_pickle=False, so loading cannot execute code.
リポジトリの certificates/SHA256SUMS に各ファイルのハッシュがあり、`load` が照合する。ファイルは別のディレクトリから読める
（--certificates DIR）が、照合するのは常にリポジトリの SHA256SUMS である。別のハッシュの一覧は、明示したとき（--hashes FILE。
改変したデータでの試験など）にだけ使う。
.npz は allow_pickle=False で読むので、読み込みでコードが実行されることはない。
"""
import argparse
import os
import sys

import numpy as np

from . import require
from .data import read_integers, sha256_file

DEFAULT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "certificates")

# The certificate files that determine the table K_8 written by verify/v4 (out/K8.npy, out/K8_first.npy).
# verify/v4 が書く表 K_8（out/K8.npy, out/K8_first.npy）を決める検証用データ。
K8_INPUTS = ("norm8_reps.npz", "centralizer.npz")


# The list of hashes the files are checked against: the repository's, unless --hashes names another.
# ファイルを照合するハッシュの一覧。--hashes で別のものを指定しない限りリポジトリのもの。
DEFAULT_HASHES = os.path.join(DEFAULT_DIR, "SHA256SUMS")
HASHES_FILE = DEFAULT_HASHES


class _HashesAction(argparse.Action):
    """--hashes FILE: check the certificate files against FILE instead of the repository's SHA256SUMS.
    --hashes FILE: リポジトリの SHA256SUMS の代わりに FILE と照合する。"""

    def __call__(self, parser, namespace, values, option_string=None):
        global HASHES_FILE
        if not os.path.isfile(values):
            parser.error(f"--hashes: {values} is not a file")
        HASHES_FILE = os.path.abspath(values)
        print(f"[warning] certificate hashes are read from {HASHES_FILE}, not from certificates/SHA256SUMS "
              f"of the repository / 照合の基準はリポジトリの SHA256SUMS ではない", file=sys.stderr)
        setattr(namespace, self.dest, HASHES_FILE)


def add_arguments(ap, help="directory of the certificate files (default: certificates/) / 検証用データの置き場所"):
    """Add --certificates DIR and --hashes FILE to an argparse parser.
    argparse のパーサに --certificates DIR と --hashes FILE を加える。"""
    ap.add_argument("--certificates", default=None, metavar="DIR", help=help)
    ap.add_argument("--hashes", default=None, metavar="FILE", action=_HashesAction,
                    help="check the certificate files against FILE instead of certificates/SHA256SUMS "
                         "(for tests on modified data) / リポジトリの SHA256SUMS の代わりに FILE と照合する（改変したデータでの試験用）")


def expected_hashes(path=None):
    """Parse a SHA256SUMS file ("<hash>  <file>" per line; default: the one in use, see HASHES_FILE).
    SHA256SUMS（1 行に「ハッシュ  ファイル名」。既定は HASHES_FILE）を読む。"""
    path = path or HASHES_FILE
    out = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if line.strip():
                    h, name = line.split()
                    out[name.lstrip("*")] = h
    return out


def path_checked(name, directory=None, require_hash=True):
    """Path of a certificate file after checking its SHA-256 against SHA256SUMS.
    SHA256SUMS と SHA-256 を照合したうえで、検証用データのファイルのパスを返す。"""
    directory = directory or DEFAULT_DIR
    path = os.path.join(directory, name)
    hashes = expected_hashes()
    if name in hashes:
        got = sha256_file(path)
        if got != hashes[name]:
            raise ValueError(f"{path}: SHA-256 {got} differs from {HASHES_FILE}: {hashes[name]}")
    elif require_hash:
        raise ValueError(f"{name} is not listed in {HASHES_FILE}")
    return path


def file_hashes(names, directory=None):
    """{name: SHA-256} of certificate files, after checking them against SHA256SUMS.
    検証用データのファイルの {名前: SHA-256}（SHA256SUMS と照合したうえで）。"""
    return {name: sha256_file(path_checked(name, directory)) for name in names}


def load(name, key, directory=None, require_hash=True):
    """One array from a certificate .npz file. / 検証用データの .npz から配列を 1 つ読む。"""
    with np.load(path_checked(name, directory, require_hash), allow_pickle=False) as z:
        return z[key]


def load_matrix(name, n, directory=None, require_hash=True):
    """An n x n integer matrix from a text certificate. / テキストの検証用データから n × n の整数行列を読む。"""
    v = read_integers(path_checked(name, directory, require_hash))
    require(v.size == n * n, f"{name}: expected {n * n} integers, found {v.size}")
    return v.reshape(n, n)


def save_npz(path, **arrays):
    """Write an .npz atomically (temporary file, then rename). / .npz を不可分に書く（一時ファイルに書いてから改名）。"""
    tmp = path + ".tmp.npz"
    np.savez_compressed(tmp, **arrays)
    os.replace(tmp, path)


def save_matrix(path, M, header):
    """Write an integer matrix as text, one row per line, after '#' header lines.
    整数行列をテキストで書く（'#' の見出し行のあと、1 行に 1 行ずつ）。"""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        for line in header.splitlines():
            f.write("# " + line + "\n")
        for row in np.asarray(M):
            f.write(" ".join(str(int(v)) for v in row) + "\n")
    os.replace(tmp, path)
