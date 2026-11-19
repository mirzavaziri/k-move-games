# k-move games

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24370916.svg)](https://doi.org/10.5281/zenodo.24370916)

Code accompanying the paper

> M. Mirzavaziri and D. Yaqubi, *Games with k moves per turn: local freedom and global rigidity*.

A finite game played on an acyclic digraph is turned into the game G^(k), in which every turn consists of k consecutive moves. The scripts reproduce all computational claims of the paper.

## Files

| File | Purpose |
|---|---|
| `kmove_games.py` | General checks: rigidity of P-sets (Theorem 3.1, Corollary 3.2), unit gadgets for the independence theorem (Theorem 4.3), k-move Nim on k+1 heaps (Theorem 5.2). |
| `nim4_rows.c` | Level-by-level solver for two-move Nim on four heaps. Computes all P-positions in rows 0..A up to level B and checks that every boundary position is an N-position. |
| `nim4_certificate.py` | Finds the periodicity certificate S_b = S_{b+p} and the least period of every row (Theorem 6.5). |

## Usage

```bash
# general checks (about 15 seconds)
python3 kmove_games.py

# two-move Nim on four heaps (about 40 minutes on one core)
gcc -O2 -o nim4_rows nim4_rows.c
./nim4_rows 30 4500 rows30.txt
python3 nim4_certificate.py rows30.txt 22 4500 1280
```

The last command prints `S_b1 = S_(b1+1280) for b1 = 2105` and the table of least periods given in Theorem 6.5.

## Requirements

Python 3.9 or later (standard library only) and a C compiler.

## Citation

If you use this code, please cite the paper and the archived version of this repository (see `CITATION.cff`).

## License

MIT License, see `LICENSE`.
