"""
Problem 1: Activity Selection  (GREEDY ALGORITHM)
=================================================
Goal   : From a set of activities (each with a start and finish time),
         select the maximum number that do NOT overlap, using a single
         resource.
Greedy : Sort by earliest finish time, then repeatedly take the next
         activity whose start >= the finish of the last one chosen.
Why the greedy choice is correct: the activity that finishes earliest frees
         the resource as soon as possible, leaving the most time for the
         remaining activities (greedy-choice property + optimal
         substructure). This is provably optimal - brute_force_max()
         confirms it for small inputs.

Run directly:  python3 problem1_activity_selection.py
All core logic (insertion sort, selection, validation) is written manually.
"""

from ui import paint, box, section, table, read_int, ask_run_again


def get_activities():
    """Prompt for all activities with validation. Returns a list of dicts."""
    n = read_int("Enter number of activities: ", minimum=1)
    activities = []
    for i in range(n):
        while True:
            start = read_int(f"Activity {i + 1} - start time: ", minimum=0)
            finish = read_int(f"Activity {i + 1} - finish time: ", minimum=0)
            if finish <= start:
                print(paint("  -> Finish time must be greater than start time.", "91"))
                continue
            activities.append({"id": i + 1, "start": start, "finish": finish})
            break
    return activities


def insertion_sort_by_finish(activities):
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


def select_activities(sorted_activities):
    """
    Greedily pick the maximum set of non-overlapping activities and build a
    trace of every greedy decision so the reasoning is visible.

    Returns: (selected_list, trace_list)
      trace item = {"activity": <dict>, "chosen": bool, "reason": str}
    """
    selected = []
    trace = []
    last_finish = None  # finish time of the most recently chosen activity

    for activity in sorted_activities:
        if last_finish is None or activity["start"] >= last_finish:
            selected.append(activity)
            reason = "first activity in finish order" if last_finish is None \
                else f"start {activity['start']} >= last finish {last_finish}"
            trace.append({"activity": activity, "chosen": True, "reason": reason})
            last_finish = activity["finish"]
        else:
            reason = f"start {activity['start']} < last finish {last_finish} (overlaps)"
            trace.append({"activity": activity, "chosen": False, "reason": reason})

    return selected, trace


def brute_force_max(activities):
    """
    VALIDATION helper (small inputs only): the size of the largest set of
    non-overlapping activities, found by checking every subset. Confirms the
    greedy answer is optimal. Written manually (no libraries).
    """
    n = len(activities)
    best = 0
    for mask in range(1 << n):                 # every subset as a bit-mask
        chosen = [activities[i] for i in range(n) if mask & (1 << i)]
        compatible = True
        for i in range(len(chosen)):
            for j in range(i + 1, len(chosen)):
                a, b = chosen[i], chosen[j]
                # Two intervals overlap iff each starts before the other ends.
                # Touching endpoints (a.start == b.finish) do NOT overlap.
                if a["start"] < b["finish"] and b["start"] < a["finish"]:
                    compatible = False
                    break
            if not compatible:
                break
        if compatible and len(chosen) > best:
            best = len(chosen)
    return best


def print_activity_table(title, activities):
    """Display a list of activities as a bordered table."""
    print(paint("\n" + title, "1"))
    if not activities:
        print(paint("  (none)", "2"))
        return
    rows = [[str(a["id"]), str(a["start"]), str(a["finish"])] for a in activities]
    print(table(["Act", "Start", "Finish"], rows))


def run():
    print(section("🎯 Problem 1 · Activity Selection  (Greedy)"))
    while True:
        activities = get_activities()
        print_activity_table("All activities entered:", activities)

        ordered = insertion_sort_by_finish(activities)
        print_activity_table("Sorted by finish time (greedy order):", ordered)

        selected, trace = select_activities(ordered)

        print(paint("\nGreedy decisions (in finish-time order):", "1"))
        for step in trace:
            act = step["activity"]
            mark = paint("● SELECTED", "1") if step["chosen"] else paint("○ skip    ", "2")
            print(f"  {mark}  Activity {act['id']} ({act['start']}-{act['finish']}): {step['reason']}")

        print_activity_table("Final selected activities:", selected)
        print("\nMaximum non-overlapping activities: "
              + paint(str(len(selected)), "1"))

        # Validate: for small inputs, confirm greedy == exhaustive optimum.
        if len(activities) <= 12:
            optimum = brute_force_max(activities)
            ok = optimum == len(selected)
            verdict = paint("OPTIMAL", "1") if ok else paint("MISMATCH!", "1", "91")
            print(f"Validation (exhaustive search): optimal = {optimum} -> {verdict}")
        else:
            print(paint("Validation skipped (too many activities for exhaustive check).", "2"))

        if not ask_run_again():
            break


if __name__ == "__main__":
    print(box(["🎯 Problem 1 · Activity Selection (Greedy)"], "95"))
    run()
