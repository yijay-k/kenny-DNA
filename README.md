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

## Design idea: each program *demonstrates and validates* its technique

Every program (1) solves the problem manually, (2) shows **how** the algorithm
reached the answer, and (3) **validates** the result on small inputs. This is
what makes it a clear representation of the technique, not just an answer.

**Problem 1 – Activity Selection (Greedy).** Enter activities as start/finish
times. It sorts them by finish time (manual insertion sort), shows the greedy
decision at **each stage** (selected / skipped and why), and gives the maximum
set of non-overlapping activities. For small inputs it then **confirms the
greedy answer is optimal** against an exhaustive subset search.

**Problem 2 – Coin Change (Dynamic Programming).** Enter coin denominations and
a target amount. It builds the `dp[]` table bottom-up (each amount reuses
smaller solved sub-amounts — overlapping subproblems), prints the table, and
then prints the **recurrence chain** (`dp[11] = dp[8] + 1 …`) so optimal
substructure is visible, not just claimed.

**Problem 3 – Travelling Salesman (Heuristic).** Enter city coordinates. It
shows (a) the canonical **single-start** Nearest-Neighbour tour with a per-leg
breakdown, (b) an **improved** version that keeps the best tour over all start
cities, and (c) for small inputs the **exact optimal** route, reporting how far
each heuristic falls short. This makes the point directly: NN is fast but not
guaranteed optimal.

## Constraints honoured

- **No built-in algorithmic shortcuts** for the core logic: manual insertion
  sort (P1), manual DP table (P2), manual nearest-city search (P3). No
  `sorted()`, `min()`, `itertools`, or graph/optimization libraries. The
  small-input validators (exhaustive subset / permutation search) are written
  manually too and are only checks, not the submitted solution.
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
