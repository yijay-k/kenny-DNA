# CSC2103 – Data Structures and Algorithms (Group Project)

Console programs for three algorithm categories required by the assignment:

| # | Category | Problem | Technique |
|---|----------|---------|-----------|
| 1 | Greedy | Activity Selection | Sort by finish time + greedy pick |
| 2 | Dynamic Programming | Coin Change (min coins) | Bottom-up `dp[]` table |
| 3 | Heuristic | Travelling Salesman | Multi-start Nearest-Neighbour |

All three are in one menu-driven file: **`csc2103_algorithms.py`**.

## How to run

Requires **Python 3** (no external libraries).

```bash
python3 csc2103_algorithms.py
```

Pick `1`, `2`, or `3` from the menu, follow the prompts, and enter `0` to exit.

## What each program does

**Problem 1 – Activity Selection (Greedy).** Enter activities as start/finish
times. The program sorts them by finish time (manual insertion sort), then
shows the greedy decision at **each stage** (selected / skipped and why),
and finally the maximum set of non-overlapping activities.

**Problem 2 – Coin Change (Dynamic Programming).** Enter coin denominations
and a target amount. It builds the `dp[]` table bottom-up (each amount reuses
smaller solved sub-amounts — overlapping subproblems), prints the table so the
decomposition is visible, and reconstructs the actual coins used.

**Problem 3 – Travelling Salesman (Heuristic).** Enter city coordinates. It
runs the Nearest-Neighbour heuristic from **every** starting city and keeps the
shortest tour (plain single-start NN depends heavily on where it begins). Output
shows the route, a per-leg distance breakdown, and the total. As a heuristic, it
is fast but not guaranteed optimal.

## Constraints honoured

- **No built-in algorithmic shortcuts** for the core logic: manual insertion
  sort (P1), manual DP table (P2), manual nearest-city search (P3). No
  `sorted()`, `min()`, or graph/optimization libraries for the algorithms.
- Only `math.sqrt` and standard I/O are used (allowed for formatting/distance).
- Input is validated at every prompt; data is treated immutably where practical.

## Repository layout

```
csc2103_algorithms.py   # all three problems (menu-driven)
samples/                # sample inputs + captured outputs for each problem
source_link.txt         # link to this repository
README.md               # this file
```

## Sample runs

See the `samples/` folder — each file records the exact menu input sequence and
the resulting program output for one problem.
