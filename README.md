# CSC2103 – Data Structures and Algorithms (Group Project)

Console programs for three algorithm categories required by the assignment:

| # | Category | Problem | Technique | File |
|---|----------|---------|-----------|------|
| 1 | Greedy | Activity Selection | Sort by finish time + greedy pick | `problem1_activity_selection.py` |
| 2 | Dynamic Programming | Coin Change (min coins) | Bottom-up `dp[]` table | `problem2_coin_change.py` |
| 3 | Heuristic | Travelling Salesman | Multi-start Nearest-Neighbour | `problem3_tsp_heuristic.py` |

Each problem is its **own file** (meaningful names, as the assignment asks) and
runs independently. `main.py` is an optional menu that launches all three.

## How to run

Requires **Python 3** only — no external libraries.

```bash
python3 problem1_activity_selection.py     # Greedy
python3 problem2_coin_change.py            # Dynamic Programming
python3 problem3_tsp_heuristic.py          # Heuristic
python3 main.py                            # menu for all three
```

The interface uses colour and boxes on a real terminal; colours turn off
automatically when output is piped (so the files in `samples/` stay plain).

## Design idea: each program *demonstrates and validates* its technique

Every program (1) solves the problem manually, (2) shows **how** the algorithm
reached the answer, and (3) **validates** the result on small inputs — so it
represents the technique, not just prints an answer.

**Problem 1 – Activity Selection (Greedy).** Sorts by finish time (manual
insertion sort), shows the greedy decision at **each stage** (selected/skipped
and why), then for small inputs **confirms the greedy answer is optimal**
against an exhaustive subset search.

**Problem 2 – Coin Change (Dynamic Programming).** Builds the `dp[]` table
bottom-up (each amount reuses smaller solved sub-amounts — overlapping
subproblems), prints the table, and prints the **recurrence chain**
(`dp[11] = dp[8] + 1 …`) so optimal substructure is visible, not just claimed.

**Problem 3 – Travelling Salesman (Heuristic).** Shows (a) the canonical
**single-start** Nearest-Neighbour tour with a per-leg breakdown, (b) an
**improved** version that keeps the best tour over all start cities, and
(c) for small inputs the **exact optimal** route, reporting how far each
heuristic falls short — making it clear NN is fast but not guaranteed optimal.

## Constraints honoured

- **No built-in algorithmic shortcuts** for the core logic: manual insertion
  sort (P1), manual DP table (P2), manual nearest-city search and permutation
  generation (P3). No `sorted()`, `min()`, `itertools`, or graph/optimization
  libraries. The small-input validators are checks, not the submitted solution.
- Only `math.sqrt` and standard I/O are used (allowed for formatting/distance).
- Input is validated at every prompt; data is treated immutably where practical.

## Repository layout

```
problem1_activity_selection.py   # Greedy
problem2_coin_change.py          # Dynamic Programming
problem3_tsp_heuristic.py        # Heuristic
main.py                          # optional menu launcher
ui.py                            # shared terminal UI + input helpers (DRY)
samples/                         # sample inputs + captured outputs
source_link.txt                  # link to this repository
README.md                        # this file
```

## Sample runs

See the `samples/` folder — each file records the input sequence and the
resulting program output for one problem.
