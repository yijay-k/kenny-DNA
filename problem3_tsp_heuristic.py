"""
Problem 3: Travelling Salesman  (NEAREST-NEIGHBOUR HEURISTIC)
============================================================
Goal      : Visit every city exactly once and return to the start, keeping
            the total travel distance short.
Heuristic : Nearest Neighbour - from the current city, always go to the
            nearest unvisited city. Fast (O(n^2)) but NOT guaranteed optimal,
            because a cheap early move can force expensive moves later.

This program makes the heuristic's limitation visible by showing:
    (a) the canonical single-start tour (start = city 1),
    (b) an improvement: the best tour over all start cities,
    (c) for small n, the TRUE optimal (exhaustive) so the gap is clear.

Run directly:  python3 problem3_tsp_heuristic.py
All core logic (distance, nearest search, permutations) is written manually.
"""

import math

from ui import paint, box, section, read_int, read_line, ask_run_again


def get_cities():
    """Prompt for city names and coordinates, rejecting duplicate points."""
    n = read_int("Enter number of cities (>= 3): ", minimum=3)
    cities = []
    for i in range(n):
        name = read_line(f"City {i + 1} name: ") or f"City{i + 1}"
        while True:
            x = read_int(f"  {name} - x coordinate (>= 0): ", minimum=0)
            y = read_int(f"  {name} - y coordinate (>= 0): ", minimum=0)

            # Manually reject a point already used by another city.
            duplicate_of = None
            for existing in cities:
                if existing["x"] == x and existing["y"] == y:
                    duplicate_of = existing["name"]
                    break
            if duplicate_of is not None:
                print(paint(f"  -> ({x},{y}) is already used by {duplicate_of}. "
                            f"Enter a different location.", "91"))
                continue

            cities.append({"name": name, "x": x, "y": y})
            break
    return cities


def distance(city_a, city_b):
    """Euclidean distance between two cities."""
    return math.sqrt((city_a["x"] - city_b["x"]) ** 2
                     + (city_a["y"] - city_b["y"]) ** 2)


def route_distance(route):
    """Total length of a route (route includes the return-to-start city)."""
    total = 0.0
    for i in range(len(route) - 1):
        total += distance(route[i], route[i + 1])
    return total


def nearest_neighbour_from(cities, start_index):
    """
    Build one nearest-neighbour tour starting at cities[start_index].
    Returns (route, total_distance). The input list is not mutated.
    """
    unvisited = list(cities)          # NEW list; original stays intact
    current = unvisited.pop(start_index)
    route = [current]
    total_distance = 0.0

    while unvisited:
        # Manually find the closest unvisited city (no built-in min()).
        closest_index = 0
        closest_distance = distance(current, unvisited[0])
        for i in range(1, len(unvisited)):
            d = distance(current, unvisited[i])
            if d < closest_distance:
                closest_distance = d
                closest_index = i

        next_city = unvisited.pop(closest_index)
        total_distance += closest_distance
        route.append(next_city)
        current = next_city

    total_distance += distance(current, route[0])  # return to start
    route.append(route[0])
    return route, total_distance


def best_nearest_neighbour(cities):
    """
    Run nearest-neighbour from every start city; keep the shortest tour.
    Returns (best_route, best_distance, best_start_index).
    """
    best_route = None
    best_distance = None
    best_start = 0
    for start_index in range(len(cities)):
        route, dist = nearest_neighbour_from(cities, start_index)
        if best_distance is None or dist < best_distance:
            best_route, best_distance, best_start = route, dist, start_index
    return best_route, best_distance, best_start


def permutations(items):
    """
    Manually generate all permutations of a list (returns a list of lists).
    Used only by the small-input exhaustive optimum below.
    """
    if len(items) <= 1:
        return [list(items)]
    result = []
    for i in range(len(items)):
        rest = items[:i] + items[i + 1:]
        for perm in permutations(rest):
            result.append([items[i]] + perm)
    return result


def brute_force_optimal(cities):
    """
    VALIDATION helper (small n only): exact shortest tour by trying every
    ordering. City 0 is fixed as the start because a cycle has no fixed
    starting point, cutting the work from n! to (n-1)!.
    Returns (route, total_distance).
    """
    n = len(cities)
    best_order = None
    best_distance = None
    for perm in permutations(list(range(1, n))):
        order = [0] + perm
        route = [cities[i] for i in order] + [cities[order[0]]]
        dist = route_distance(route)
        if best_distance is None or dist < best_distance:
            best_distance = dist
            best_order = order
    route = [cities[i] for i in best_order] + [cities[best_order[0]]]
    return route, best_distance


def route_names(route):
    return " -> ".join(city["name"] for city in route)


def run():
    print(section("🧭 Problem 3 · Travelling Salesman  (Nearest-Neighbour)"))
    while True:
        cities = get_cities()

        # (a) Canonical Nearest-Neighbour: single start at the first city.
        nn_route, nn_dist = nearest_neighbour_from(cities, 0)
        print(paint(f"\n[Nearest Neighbour] start = {cities[0]['name']}", "1"))
        print("  Route: " + paint(route_names(nn_route), "1"))
        print("  Leg-by-leg distances:")
        for i in range(len(nn_route) - 1):
            leg = distance(nn_route[i], nn_route[i + 1])
            print(f"    {nn_route[i]['name']} -> {nn_route[i + 1]['name']}: {leg:.2f}")
        print("  Total distance: " + paint(f"{nn_dist:.2f}", "1"))

        # (b) Improvement: best Nearest-Neighbour over all possible starts.
        best_route, best_dist, best_start = best_nearest_neighbour(cities)
        print(paint(f"\n[Improved NN] best of all {len(cities)} start cities "
                    f"(start = {cities[best_start]['name']})", "1"))
        print("  Route: " + paint(route_names(best_route), "1"))
        print("  Total distance: " + paint(f"{best_dist:.2f}", "1"))

        # (c) For small n, show the TRUE optimal so the heuristic gap is clear.
        if len(cities) <= 9:
            opt_route, opt_dist = brute_force_optimal(cities)
            print(paint("\n[Exact optimal] exhaustive search", "1"))
            print("  Route: " + paint(route_names(opt_route), "1"))
            print("  Total distance: " + paint(f"{opt_dist:.2f}", "1"))
            if opt_dist > 0:
                nn_gap = (nn_dist - opt_dist) / opt_dist * 100
                best_gap = (best_dist - opt_dist) / opt_dist * 100
                print("  Gap vs optimal: "
                      + paint(f"single-start NN = +{nn_gap:.1f}%", "1")
                      + ", " + paint(f"improved NN = +{best_gap:.1f}%", "1"))
                if best_gap <= 0.0001:
                    print(paint("  -> The improved heuristic matched the optimal here; "
                                "the single-start version shows why NN can fall short.", "2"))
                else:
                    print(paint("  -> Neither heuristic reached the optimum, confirming "
                                "NN is not guaranteed optimal.", "2"))
        else:
            print(paint("\n[Exact optimal] skipped (too many cities for exhaustive search).", "2"))

        print(paint("\nNote: Nearest-Neighbour is a fast heuristic; it aims for a good "
                    "route, not a guaranteed shortest one.", "2"))

        if not ask_run_again():
            break


if __name__ == "__main__":
    print(box(["🧭 Problem 3 · Travelling Salesman (Nearest-Neighbour Heuristic)"]))
    run()
