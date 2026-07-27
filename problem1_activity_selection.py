"""
Problem 1: Activity Selection  (GREEDY ALGORITHM)
=================================================
Goal   : From a FIXED list of activities (each with a name, a start
         date-time and an end date-time), select the maximum number that
         do NOT overlap, so a single hall/resource is used for as many
         activities as possible.
Greedy : Sort by earliest END time, then repeatedly take the next activity
         whose start is not before the end of the last one chosen.
Why the greedy choice is correct: finishing earliest frees the hall as soon
         as possible, leaving the most room for the remaining activities.

The data set is predefined (no free-text input) so the program stays simple
and easy to test - we just run the algorithm and show how it decides.
All core logic (insertion sort + selection) is written manually.
Run directly:  python3 problem1_activity_selection.py
"""

from datetime import datetime

from ui import paint, box, section, table

# Fixed schedule: hall bookings for one day (name, start, end).
# Each activity carries a full date AND time.
ACTIVITIES = [
    {"name": "Algorithms Lecture", "start": datetime(2026, 8, 10, 9, 0),  "end": datetime(2026, 8, 10, 10, 30)},
    {"name": "Robotics Club",      "start": datetime(2026, 8, 10, 10, 0), "end": datetime(2026, 8, 10, 11, 0)},
    {"name": "Data Science Talk",  "start": datetime(2026, 8, 10, 10, 30),"end": datetime(2026, 8, 10, 12, 0)},
    {"name": "Career Workshop",    "start": datetime(2026, 8, 10, 11, 30),"end": datetime(2026, 8, 10, 13, 0)},
    {"name": "Chess Tournament",   "start": datetime(2026, 8, 10, 12, 0), "end": datetime(2026, 8, 10, 13, 30)},
    {"name": "AI Seminar",         "start": datetime(2026, 8, 10, 13, 0), "end": datetime(2026, 8, 10, 14, 30)},
    {"name": "Study Group",        "start": datetime(2026, 8, 10, 14, 30),"end": datetime(2026, 8, 10, 15, 30)},
]


def fmt(dt):
    """Format a date-time for display, e.g. 'Mon 10 Aug 09:00'."""
    return dt.strftime("%a %d %b %H:%M")


def insertion_sort_by_end(activities):
    """
    Manually sort activities by end time (ascending) with insertion sort.
    Returns a NEW list (the input is not mutated).
    """
    ordered = list(activities)
    for i in range(1, len(ordered)):
        key = ordered[i]
        j = i - 1
        while j >= 0 and ordered[j]["end"] > key["end"]:
            ordered[j + 1] = ordered[j]
            j -= 1
        ordered[j + 1] = key
    return ordered


def select_activities(sorted_activities):
    """
    Greedily pick the maximum set of non-overlapping activities and record a
    trace of every decision so the greedy reasoning is visible.
    Returns: (selected_list, trace_list)
    """
    selected = []
    trace = []
    last_end = None  # end time of the most recently chosen activity

    for activity in sorted_activities:
        if last_end is None or activity["start"] >= last_end:
            selected.append(activity)
            reason = "first (earliest end)" if last_end is None \
                else f"starts {fmt(activity['start'])} >= last end {fmt(last_end)}"
            trace.append({"activity": activity, "chosen": True, "reason": reason})
            last_end = activity["end"]
        else:
            reason = f"starts {fmt(activity['start'])} < last end {fmt(last_end)} (overlaps)"
            trace.append({"activity": activity, "chosen": False, "reason": reason})
    return selected, trace


def print_activity_table(title, activities):
    """Display activities as a bordered table (name, start, end)."""
    print(paint("\n" + title, "1"))
    if not activities:
        print(paint("  (none)", "2"))
        return
    rows = [[a["name"], fmt(a["start"]), fmt(a["end"])] for a in activities]
    print(table(["Activity", "Start", "End"], rows))


def run():
    print(section("🎯 Problem 1 · Activity Selection  (Greedy)"))

    print_activity_table("Fixed list of activities:", ACTIVITIES)

    ordered = insertion_sort_by_end(ACTIVITIES)
    print_activity_table("Step 1 - sorted by earliest end time:", ordered)

    selected, trace = select_activities(ordered)

    print(paint("\nStep 2 - greedy decisions (in end-time order):", "1"))
    for step in trace:
        act = step["activity"]
        mark = paint("● SELECTED", "1") if step["chosen"] else paint("○ skip    ", "2")
        print(f"  {mark}  {act['name']:<20} {step['reason']}")

    print_activity_table("Result - maximum non-overlapping activities:", selected)
    print("\nActivities selected: " + paint(str(len(selected)), "1")
          + f" out of {len(ACTIVITIES)}")


if __name__ == "__main__":
    print(box(["🎯 Problem 1 · Activity Selection (Greedy)"]))
    run()
