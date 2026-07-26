"""
CSC2103 Group Project - menu launcher
=====================================
Optional single entry point that lets you run all three programs from one
menu. Each problem also runs on its own, e.g.:

    python3 problem1_activity_selection.py
    python3 problem2_coin_change.py
    python3 problem3_tsp_heuristic.py
    python3 main.py                     # this menu
"""

from ui import banner, box, paint, read_line
import problem1_activity_selection as p1
import problem2_coin_change as p2
import problem3_tsp_heuristic as p3


MENU = {
    "1": ("Activity Selection      " + paint("(Greedy)", "2"), p1.run),
    "2": ("Coin Change             " + paint("(Dynamic Programming)", "2"), p2.run),
    "3": ("Travelling Salesman     " + paint("(Heuristic)", "2"), p3.run),
}


def print_menu():
    rows = [paint("Main Menu", "1"), ""]
    for key, (label, _) in MENU.items():
        rows.append(paint(f" {key} ", "1", "93") + "  " + label)
    rows.append(paint(" 0 ", "1", "91") + "  " + "Exit")
    print(box(rows, "94"))


def main():
    print(banner("Group Project — three algorithm techniques"))
    while True:
        print_menu()
        choice = read_line("Select an option ▶ ")
        if choice == "0":
            print(paint("Goodbye! 🐱", "95"))
            break
        if choice in MENU:
            MENU[choice][1]()
        else:
            print(paint("  -> Invalid choice. Please pick 0, 1, 2, or 3.", "91"))


if __name__ == "__main__":
    main()
