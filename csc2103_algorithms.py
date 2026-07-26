"""
CSC2103: Data Structures and Algorithms - Group Project
=======================================================
Combined console program containing all three algorithm solutions:

    Problem 1 (Greedy)              : Activity Selection Problem
    Problem 2 (Dynamic Programming) : Coin Change Problem
    Problem 3 (Heuristic)           : Travelling Salesman - Nearest Neighbour

Run this file and pick a problem from the menu.

Design notes (assignment constraints):
  * All CORE algorithmic logic is written manually. No built-in sorting
    (sort/sorted), no built-in min() for algorithmic decisions, and no
    graph/optimization libraries are used. Only `math.sqrt` (for distance)
    and general I/O are used, which is allowed for I/O/formatting.
  * Data is treated immutably where practical: sorting/tour building return
    NEW lists instead of mutating the caller's data.
"""

import math


# =====================================================================
#  SHARED INPUT HELPERS  (input validation lives in one place - DRY)
# =====================================================================

def read_int(prompt, minimum=None):
    """
    Read a whole number from the user, re-prompting until it is valid.

    minimum : if given, the value must be >= minimum, otherwise the user
              is asked again.
    """
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print(f"  -> Please enter a whole number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("  -> Invalid input. Please enter a whole number.")


def ask_run_again():
    """Return True if the user wants to run the current problem again."""
    return input("\nRun again with new input? (y/n): ").strip().lower() == "y"


# =====================================================================
#  PROBLEM 1 - ACTIVITY SELECTION  (GREEDY ALGORITHM)
# ---------------------------------------------------------------------
#  Goal   : From a set of activities (each with a start and finish time),
#           select the maximum number that do NOT overlap, using a single
#           resource.
#  Greedy : Sort by earliest finish time, then repeatedly take the next
#           activity whose start >= the finish of the last one chosen.
#  Why it works: choosing the activity that finishes earliest always
#           leaves the most remaining time for the rest (optimal
#           substructure + greedy-choice property).
# =====================================================================

def p1_get_activities():
    """Prompt for all activities with validation. Returns a list of dicts."""
    n = read_int("Enter number of activities: ", minimum=1)
    activities = []
    for i in range(n):
        while True:
            start = read_int(f"Activity {i + 1} - start time: ", minimum=0)
            finish = read_int(f"Activity {i + 1} - finish time: ", minimum=0)
            if finish <= start:
                print("  -> Finish time must be greater than start time. Try again.")
                continue
            activities.append({"id": i + 1, "start": start, "finish": finish})
            break
    return activities


def p1_insertion_sort_by_finish(activities):
    """
    Manually sort activities by finish time (ascending) using insertion
    sort. Returns a NEW list (the input is not mutated).
    """
    ordered = list(activities)  # shallow copy so we never mutate the caller
    for i in range(1, len(ordered)):
        key = ordered[i]
        j = i - 1
        while j >= 0 and ordered[j]["finish"] > key["finish"]:
            ordered[j + 1] = ordered[j]
            j -= 1
        ordered[j + 1] = key
    return ordered


def p1_select_activities(sorted_activities):
    """
    Greedily pick the maximum set of non-overlapping activities and, at the
    same time, build a human-readable trace of every greedy decision so the
    reasoning is visible (a rubric requirement).

    Returns: (selected_list, trace_list)
      trace item = {"activity": <dict>, "chosen": bool, "reason": str}
    """
    selected = []
    trace = []
    last_finish = None  # finish time of the most recently chosen activity

    for activity in sorted_activities:
        if last_finish is None or activity["start"] >= last_finish:
            selected.append(activity)
            reason = "first activity" if last_finish is None \
                else f"start {activity['start']} >= last finish {last_finish}"
            trace.append({"activity": activity, "chosen": True, "reason": reason})
            last_finish = activity["finish"]
        else:
            reason = f"start {activity['start']} < last finish {last_finish} (overlaps)"
            trace.append({"activity": activity, "chosen": False, "reason": reason})

    return selected, trace


def p1_print_activity_table(title, activities):
    """Display a list of activities in a simple formatted table."""
    print(f"\n{title}")
    print(f"{'Act':<6}{'Start':<8}{'Finish':<8}")
    print("-" * 22)
    for a in activities:
        print(f"{a['id']:<6}{a['start']:<8}{a['finish']:<8}")


def run_problem1():
    print("\n=== Problem 1: Activity Selection (Greedy Algorithm) ===")
    while True:
        activities = p1_get_activities()
        p1_print_activity_table("All activities entered:", activities)

        ordered = p1_insertion_sort_by_finish(activities)
        p1_print_activity_table("Sorted by finish time (greedy order):", ordered)

        selected, trace = p1_select_activities(ordered)

        # Show the greedy decision at each stage.
        print("\nGreedy decisions (in finish-time order):")
        for step in trace:
            act = step["activity"]
            mark = "[SELECTED]" if step["chosen"] else "[  skip  ]"
            print(f"  {mark} Activity {act['id']} ({act['start']}-{act['finish']}): {step['reason']}")

        p1_print_activity_table("Final selected activities:", selected)
        print(f"\nMaximum number of non-overlapping activities: {len(selected)}")

        if not ask_run_again():
            break


# =====================================================================
#  PROBLEM 2 - COIN CHANGE  (DYNAMIC PROGRAMMING)
# ---------------------------------------------------------------------
#  Goal : Given coin denominations and a target amount, find the MINIMUM
#         number of coins needed to make that amount.
#  DP   : dp[a] = fewest coins to make amount a.
#         dp[a] = min over each coin c<=a of ( dp[a-c] + 1 ).
#         Every dp[a] reuses already-solved smaller subproblems
#         (overlapping subproblems + optimal substructure).
# =====================================================================

def p2_get_denominations():
    """Prompt for coin denominations, validate, and remove duplicates."""
    while True:
        raw = input("Enter coin denominations (comma-separated, e.g. 1,3,4): ")
        parts = [p.strip() for p in raw.split(",") if p.strip() != ""]
        if not parts:
            print("  -> Please enter at least one denomination.")
            continue
        try:
            coins = [int(p) for p in parts]
        except ValueError:
            print("  -> Invalid input. Use whole numbers separated by commas.")
            continue
        if any(c <= 0 for c in coins):
            print("  -> All denominations must be positive integers. Try again.")
            continue
        # Remove duplicate denominations so the DP table stays clean.
        unique_coins = []
        for c in coins:
            if c not in unique_coins:
                unique_coins.append(c)
        return unique_coins


def p2_coin_change_dp(coins, amount):
    """
    Bottom-up DP for the minimum-coin problem.

    Returns: (min_coins, combination)
      * min_coins  = fewest coins, or None if the amount cannot be made
      * combination = list of coins actually used
      * dp         = the full DP table (returned too, so the caller can
                     display the decomposition)
    """
    INF = float("inf")
    dp = [INF] * (amount + 1)        # dp[a] = fewest coins for amount a
    choice = [-1] * (amount + 1)     # choice[a] = a coin used to reach a
    dp[0] = 0                        # base case: 0 coins make amount 0

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1
                choice[a] = coin

    if dp[amount] == INF:
        return None, [], dp

    # Reconstruct which coins were used by walking the choice[] table back.
    combination = []
    remaining = amount
    while remaining > 0:
        coin_used = choice[remaining]
        combination.append(coin_used)
        remaining -= coin_used

    return dp[amount], combination, dp


def p2_group_combination(combination):
    """Turn [3,3,1] into a readable 'count x coin' summary. Returns a string."""
    counts = {}
    for coin in combination:
        counts[coin] = counts.get(coin, 0) + 1
    # Show larger coins first for readability (manual selection sort on keys).
    keys = list(counts.keys())
    for i in range(len(keys)):
        max_idx = i
        for j in range(i + 1, len(keys)):
            if keys[j] > keys[max_idx]:
                max_idx = j
        keys[i], keys[max_idx] = keys[max_idx], keys[i]
    return "  +  ".join(f"{counts[k]} x {k}" for k in keys)


def run_problem2():
    print("\n=== Problem 2: Coin Change (Dynamic Programming) ===")
    while True:
        coins = p2_get_denominations()
        amount = read_int("Enter target amount: ", minimum=0)

        min_coins, combination, dp = p2_coin_change_dp(coins, amount)

        # Show the DP table so the overlapping-subproblem decomposition is
        # visible (kept compact for larger amounts).
        if amount <= 30:
            print("\nDP table  dp[a] = fewest coins to make amount a:")
            print(f"{'amount':<8}{'dp[a]':<8}")
            print("-" * 16)
            for a in range(amount + 1):
                cell = "inf" if dp[a] == float("inf") else dp[a]
                print(f"{a:<8}{cell:<8}")

        if min_coins is None:
            print(f"\nNo combination of {coins} can make up {amount}.")
        else:
            print(f"\nMinimum coins needed: {min_coins}")
            if combination:
                print(f"Combination used: {p2_group_combination(combination)}")
            else:
                print("Combination used: none (amount is 0)")

        if not ask_run_again():
            break


# =====================================================================
#  PROBLEM 3 - TRAVELLING SALESMAN  (NEAREST-NEIGHBOUR HEURISTIC)
# ---------------------------------------------------------------------
#  Goal      : Visit every city exactly once and return to the start,
#              keeping the total travel distance short.
#  Heuristic : From the current city, always go to the nearest unvisited
#              city. This is fast but not guaranteed optimal.
#  Improvement over a plain single-start version: we run the heuristic
#  from EVERY possible starting city and keep the shortest tour, because
#  nearest-neighbour is very sensitive to where it starts.
# =====================================================================

def p3_get_cities():
    """Prompt for city names and coordinates, rejecting duplicate points."""
    n = read_int("Enter number of cities (>= 3): ", minimum=3)
    cities = []
    for i in range(n):
        name = input(f"City {i + 1} name: ").strip() or f"City{i + 1}"
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
                print(f"  -> ({x},{y}) is already used by {duplicate_of}. "
                      f"Enter a different location.")
                continue

            cities.append({"name": name, "x": x, "y": y})
            break
    return cities


def p3_distance(city_a, city_b):
    """Euclidean distance between two cities."""
    return math.sqrt((city_a["x"] - city_b["x"]) ** 2
                     + (city_a["y"] - city_b["y"]) ** 2)


def p3_nearest_neighbour_from(cities, start_index):
    """
    Build one nearest-neighbour tour that starts at cities[start_index].
    Returns (route, total_distance). The input list is not mutated.
    """
    unvisited = list(cities)          # NEW list; original stays intact
    current = unvisited.pop(start_index)
    route = [current]
    total_distance = 0.0

    while unvisited:
        # Manually find the closest unvisited city (no built-in min()).
        closest_index = 0
        closest_distance = p3_distance(current, unvisited[0])
        for i in range(1, len(unvisited)):
            d = p3_distance(current, unvisited[i])
            if d < closest_distance:
                closest_distance = d
                closest_index = i

        next_city = unvisited.pop(closest_index)
        total_distance += closest_distance
        route.append(next_city)
        current = next_city

    total_distance += p3_distance(current, route[0])  # return to start
    route.append(route[0])
    return route, total_distance


def p3_best_nearest_neighbour(cities):
    """
    Run the nearest-neighbour heuristic from every possible start city and
    keep the shortest tour found. Returns (best_route, best_distance).
    """
    best_route = None
    best_distance = None
    for start_index in range(len(cities)):
        route, dist = p3_nearest_neighbour_from(cities, start_index)
        if best_distance is None or dist < best_distance:
            best_route = route
            best_distance = dist
    return best_route, best_distance


def run_problem3():
    print("\n=== Problem 3: Travelling Salesman (Nearest-Neighbour Heuristic) ===")
    while True:
        cities = p3_get_cities()
        route, total_distance = p3_best_nearest_neighbour(cities)

        route_names = " -> ".join(city["name"] for city in route)
        print(f"\nBest route found (tried all start cities): {route_names}")

        # Per-leg breakdown so the total is easy to verify.
        print("\nLeg-by-leg distances:")
        for i in range(len(route) - 1):
            leg = p3_distance(route[i], route[i + 1])
            print(f"  {route[i]['name']} -> {route[i + 1]['name']}: {leg:.2f}")

        print(f"\nTotal distance: {total_distance:.2f}")
        print("Note: Nearest-Neighbour is a heuristic; even with multiple "
              "start cities it may not be the globally optimal route.")

        if not ask_run_again():
            break


# =====================================================================
#  MAIN MENU
# =====================================================================

def main():
    menu = {
        "1": ("Activity Selection  (Greedy)", run_problem1),
        "2": ("Coin Change         (Dynamic Programming)", run_problem2),
        "3": ("Travelling Salesman (Nearest-Neighbour Heuristic)", run_problem3),
    }

    print("=" * 60)
    print(" CSC2103 - Data Structures and Algorithms - Group Project")
    print("=" * 60)

    while True:
        print("\nMain Menu")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")
        print("  0. Exit")

        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        if choice in menu:
            menu[choice][1]()  # run the chosen problem
        else:
            print("  -> Invalid choice. Please pick 0, 1, 2, or 3.")


if __name__ == "__main__":
    main()
