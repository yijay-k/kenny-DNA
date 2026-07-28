# CSC2103 – Data Structures and Algorithms (Group Project)

Three console programs, one per required algorithm category. The programs use
**fixed datasets and menu/choice-based input** (no free-text data entry) — the
user only ever picks from a list, so there is nothing invalid to type and the
focus stays on demonstrating each algorithm clearly.

- **Problem 1** takes no input (runs on a fixed list).
- **Problem 2** and **Problem 3** take a single menu choice each.

| # | Category | Problem | Technique | File |
|---|----------|---------|-----------|------|
| 1 | Greedy | Activity Selection | Sort by end time + greedy pick | `problem1_activity_selection.py` |
| 2 | Dynamic Programming | Coin Change (min coins) | Bottom-up `dp[]` table | `problem2_coin_change.py` |
| 3 | Heuristic | Shortest Path on a map | A* Search | `problem3_astar_shortest_path.py` |

`main.py` is a menu that launches all three; each problem also runs on its own.

## How to run

Requires **Python 3** only — no external libraries.

```bash
python3 problem1_activity_selection.py     # Greedy
python3 problem2_coin_change.py            # Dynamic Programming
python3 problem3_astar_shortest_path.py    # Heuristic (A*)
python3 main.py                            # menu for all three
```

The interface uses light colour and boxes on a real terminal; colours turn off
automatically when output is piped (so the files in `samples/` stay plain).

## What each program does

**Problem 1 – Activity Selection (Greedy).** A **fixed list** of hall bookings
(activity name + start/end **date-time**). The program sorts by earliest end
time, shows the greedy decision for each activity (selected / skipped and why),
and reports the maximum set of non-overlapping activities. No user input.

**Problem 2 – Coin Change (Dynamic Programming).** **Fixed** denominations
`1, 5, 10, 20, 50` cents. The user picks a target amount **from a menu** (no
typing, so nothing to validate). The run is shown in two clear steps:
**Step 1** builds a table of the fewest coins for *every* amount from 0 to the
target (each row also records the "last coin" added); **Step 2** rebuilds the
actual coins by following that "last coin" back from the target down to 0. It
finishes with a highlighted answer (e.g. `37c = 20c + 10c + 5c + 1c + 1c`).

**Problem 3 – Shortest Path / A\* (Heuristic).** A **fixed map** of real
locations around Sunway (Sunway University, Sunway Square, Taylor's University,
Monash University, ISKL) with approximate road distances. The user only picks a
**starting location**; A* then finds the shortest route and distance to each
other location, guided by a straight-line-distance heuristic.

> Distances in Problem 3 are approximate (km). Replace them with exact Google
> Maps values if precise figures are needed — only the numbers in `ROADS` and
> the positions in `LOCATIONS` need editing.

## Constraints honoured

- **No built-in algorithmic shortcuts** for the core logic: manual insertion
  sort (P1), manual DP table (P2), manual A* search (P3). No `sorted()`,
  `min()`, or graph/optimization libraries for the algorithms.
- Only `math`, `datetime`, and standard I/O are used (formatting / dates /
  distance) — allowed for I/O and general utilities.
- Because input is menu/choice-based, validation is a simple range check.

## Repository layout

```
problem1_activity_selection.py    # Greedy
problem2_coin_change.py           # Dynamic Programming
problem3_astar_shortest_path.py   # Heuristic (A*)
main.py                           # optional menu launcher
ui.py                             # shared terminal UI + input helpers
samples/                          # sample outputs for each problem
source_link.txt                   # link to this repository
README.md                         # this file
```
