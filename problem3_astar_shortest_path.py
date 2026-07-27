"""
Problem 3: Shortest Path on a Map  (A* SEARCH - HEURISTIC ALGORITHM)
===================================================================
Goal      : On a FIXED map of real locations around Sunway, find the shortest
            route (and distance) from a chosen starting location to the other
            locations. The user only selects the starting point.
Heuristic : A* Search. It explores the graph guided by a heuristic h(n) =
            straight-line ("as the crow flies") distance from node n to the
            goal. Because that straight-line distance never over-estimates the
            real road distance (it is "admissible"), A* is guided towards the
            goal yet still returns the true shortest path.

The map (locations, road links and distances) is predefined - the user cannot
edit the graph, which keeps the program simple and easy to test.

NOTE: distances are APPROXIMATE km for demonstration. Replace them with exact
Google Maps values if your report requires precise figures.

All core logic (the A* search) is written manually - no graph libraries.
Run directly:  python3 problem3_astar_shortest_path.py
"""

import math

from ui import paint, box, section, choose

# Each location has an approximate map position (x, y) in km. The straight-line
# distance between positions is A*'s heuristic.
LOCATIONS = {
    "Sunway University":  (0.0, 0.0),
    "Sunway Square":      (0.71, 0.42),
    "Taylor's University": (0.41, -0.35),
    "Monash University":  (-0.22, -0.44),
    "ISKL (Ampang)":      (16.27, 10.19),
}

# Road links between locations with approximate driving distance in km
# (undirected). Not every pair is directly connected, so some trips need
# to be routed through an intermediate location - which is what A* solves.
ROADS = {
    "Sunway University":  [("Sunway Square", 1.1), ("Taylor's University", 0.8), ("Monash University", 0.7)],
    "Sunway Square":      [("Sunway University", 1.1), ("Taylor's University", 1.2), ("ISKL (Ampang)", 25.0)],
    "Taylor's University": [("Sunway University", 0.8), ("Sunway Square", 1.2), ("Monash University", 0.9)],
    "Monash University":  [("Sunway University", 0.7), ("Taylor's University", 0.9)],
    "ISKL (Ampang)":      [("Sunway Square", 25.0)],
}


def straight_line(a, b):
    """Straight-line (Euclidean) distance in km - used as the A* heuristic."""
    (ax, ay), (bx, by) = LOCATIONS[a], LOCATIONS[b]
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def astar(start, goal):
    """
    A* search from `start` to `goal`. Returns (path_list, total_distance),
    or (None, inf) if the goal cannot be reached.

    g[n] = best known road distance from start to n
    f[n] = g[n] + straight_line(n, goal)   (estimated total via n)
    The open set is scanned manually for the lowest f (small graph).
    """
    open_set = [start]
    g = {start: 0.0}
    f = {start: straight_line(start, goal)}
    came_from = {}

    while open_set:
        # Manually pick the open node with the smallest f (no library used).
        current = open_set[0]
        for node in open_set[1:]:
            if f[node] < f[current]:
                current = node

        if current == goal:
            # Reconstruct the path by walking the came_from links backwards.
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, g[goal]

        open_set.remove(current)
        for neighbour, road_dist in ROADS[current]:
            tentative_g = g[current] + road_dist
            if neighbour not in g or tentative_g < g[neighbour]:
                came_from[neighbour] = current
                g[neighbour] = tentative_g
                f[neighbour] = tentative_g + straight_line(neighbour, goal)
                if neighbour not in open_set:
                    open_set.append(neighbour)

    return None, float("inf")


def print_map():
    """Show the fixed road network so the graph is clear before searching."""
    print(paint("\nFixed map - road links (approx. km):", "1"))
    shown = set()
    for place, links in ROADS.items():
        for neighbour, dist in links:
            key = tuple(sorted((place, neighbour)))
            if key not in shown:
                shown.add(key)
                print(f"  {place}  <->  {neighbour}  :  {dist:.1f} km")


def run():
    print(section("🧭 Problem 3 · Shortest Path on a Map  (A* Search)"))
    print_map()

    names = list(LOCATIONS.keys())
    print()
    start = names[choose("Choose your STARTING location:", names)]

    print(paint(f"\nShortest paths from {start} (A* search):", "1"))
    for goal in names:
        if goal == start:
            continue
        path, dist = astar(start, goal)
        route = "  ->  ".join(path)
        print(f"\n  To {goal}:")
        print("    Route   : " + paint(route, "1"))
        print("    Distance: " + paint(f"{dist:.1f} km", "1"))

    print(paint("\nA* uses the straight-line distance to the goal as its heuristic; "
                "because that never over-estimates the real distance, the routes "
                "above are the true shortest paths.", "2"))


if __name__ == "__main__":
    print(box(["🧭 Problem 3 · Shortest Path on a Map (A* Search)"]))
    run()
