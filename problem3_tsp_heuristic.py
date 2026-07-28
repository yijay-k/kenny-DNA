"""
Problem 3: Travelling Salesman  (NEAREST NEIGHBOUR HEURISTIC)
============================================================
Goal      : Visit every city exactly once and return to the starting city,
            keeping the total travel distance short.
Heuristic : Nearest Neighbour - from the current city, always travel next to
            the closest city not yet visited. It is a greedy approximation:
            fast, but not guaranteed to be the shortest possible tour.
Why not check every route: with n cities there are (n-1)! possible tours, which
            grows factorially and quickly becomes impossible to check one by
            one (Bhargava, 2016, Grokking Algorithms, Ch. 8). Nearest Neighbour
            avoids that by only ever moving to the closest unvisited city.

The map is a FIXED set of locations (no free-text input); the user only picks
which city to start from. Coordinates are placeholder (x, y) map units and can
be replaced with real surveyed distances if exact figures are required.

All core logic (distance + nearest search) is written manually.
Run directly:  python3 problem3_tsp_heuristic.py
"""

import math

from ui import paint, box, section, table, choose

# Fixed cities: name + placeholder (x, y) map position.
CITIES = [
    {"name": "Sunway University",   "x": 2,  "y": 2},
    {"name": "Sunway Square",       "x": 4,  "y": 5},
    {"name": "Taylor's University", "x": 6,  "y": 2},
    {"name": "Monash University",   "x": 5,  "y": 8},
    {"name": "ISKL",                "x": 10, "y": 6},
]


def distance(a, b):
    """Straight-line (Euclidean) distance between two cities."""
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2)


def nearest_neighbour_tour(cities, start_index):
    """
    Build a Nearest Neighbour tour starting at cities[start_index]: repeatedly
    move to the closest unvisited city, then return to the start.
    Returns (route, total_distance). The input list is not mutated.
    """
    unvisited = list(cities)                 # NEW list; original untouched
    current = unvisited.pop(start_index)
    route = [current]
    total = 0.0

    while unvisited:
        # Manually find the closest unvisited city (no built-in min()).
        closest_i = 0
        closest_d = distance(current, unvisited[0])
        for i in range(1, len(unvisited)):
            d = distance(current, unvisited[i])
            if d < closest_d:
                closest_d, closest_i = d, i

        current = unvisited.pop(closest_i)
        total += closest_d
        route.append(current)

    total += distance(current, route[0])     # return to the starting city
    route.append(route[0])
    return route, total


def factorial(n):
    """n! computed manually (used to show how many routes a brute force faces)."""
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


def run():
    print(section("🧭 Problem 3 · Travelling Salesman  (Nearest Neighbour)"))

    # Show the fixed map.
    rows = [[c["name"], str(c["x"]), str(c["y"])] for c in CITIES]
    print(paint("\nFixed map of cities (placeholder x, y positions):", "1"))
    print(table(["City", "x", "y"], rows))

    n = len(CITIES)
    print(f"\nChecking every route would mean ({n}-1)! = {factorial(n - 1)} tours. "
          "Nearest Neighbour instead just keeps moving to the closest city.")

    print()
    start = choose("Choose the STARTING city:", [c["name"] for c in CITIES])

    route, total = nearest_neighbour_tour(CITIES, start)

    print(paint(f"\nNearest Neighbour tour from {CITIES[start]['name']}:", "1"))
    print("  Route: " + paint(" -> ".join(c["name"] for c in route), "1"))
    print("  Leg-by-leg distances:")
    for i in range(len(route) - 1):
        print(f"    {route[i]['name']} -> {route[i + 1]['name']}: "
              f"{distance(route[i], route[i + 1]):.2f}")

    print()
    print(box([
        paint("ANSWER", "1"),
        "",
        f"Total tour distance: {total:.2f} (map units)",
    ]))
    print(paint("\nNote: Nearest Neighbour is a heuristic - it finds a good tour "
                "quickly but not always the shortest possible one.", "2"))


if __name__ == "__main__":
    print(box(["🧭 Problem 3 · Travelling Salesman (Nearest Neighbour Heuristic)"]))
    run()
