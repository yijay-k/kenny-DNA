"""
Shared terminal UI + input helpers for the CSC2103 group project.
=================================================================
Kept in one small module so the three problem programs stay DRY and
consistent (colours, boxes, tables, validated input).

Presentation only: ANSI colours switch on for a real terminal and switch
off automatically when the output is piped/redirected, so captured sample
files stay clean. Set NO_COLOR to force plain text, or FORCE_COLOR to keep
colours even when piping. Pure standard library - no external packages.
"""

import os
import re
import sys

_COLOR = bool(
    (sys.stdout.isatty() or os.environ.get("FORCE_COLOR"))
    and os.environ.get("NO_COLOR") is None
)

_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


# ---------------------------------------------------------------------
#  Colour + layout
# ---------------------------------------------------------------------

def paint(text, *codes):
    """Wrap text in ANSI colour codes (a no-op when colour is disabled)."""
    if not _COLOR or not codes:
        return text
    return f"\033[{';'.join(codes)}m{text}\033[0m"


def visible_len(text):
    """Length of text ignoring any ANSI colour codes (for alignment)."""
    return len(_ANSI_RE.sub("", str(text)))


def box(lines, code="96", pad=1):
    """Draw a rounded box around the given lines (content may be coloured)."""
    width = max((visible_len(l) for l in lines), default=0)
    inner = width + pad * 2
    edge = paint("│", code)
    out = [paint("╭" + "─" * inner + "╮", code)]
    for line in lines:
        gap = width - visible_len(line)
        out.append(edge + " " * pad + line + " " * (gap + pad) + edge)
    out.append(paint("╰" + "─" * inner + "╯", code))
    return "\n".join(out)


def section(title, code="96"):
    """A coloured section header shown before each problem's output."""
    tail = "━" * max(3, 50 - visible_len(title))
    return "\n" + paint("━━━  " + title + "  " + tail, "1", code)


def table(headers, rows, code="96"):
    """Render a bordered table. Cells may already contain colour codes."""
    widths = []
    for i in range(len(headers)):
        cell_widths = [visible_len(r[i]) for r in rows]
        widths.append(max([visible_len(headers[i])] + cell_widths))

    def rule(left, mid, right):
        return paint(left + mid.join("─" * (w + 2) for w in widths) + right, code)

    def row(cells):
        bar = paint("│", code)
        parts = [" " + str(c) + " " * (widths[i] - visible_len(c)) + " "
                 for i, c in enumerate(cells)]
        return bar + bar.join(parts) + bar

    out = [rule("╭", "┬", "╮"),
           row([paint(h, "1") for h in headers]),
           rule("├", "┼", "┤")]
    for r in rows:
        out.append(row(r))
    out.append(rule("╰", "┴", "╯"))
    return "\n".join(out)


def banner(subtitle):
    """The ASCII-art welcome banner (cat mascot + course title)."""
    cat = [paint(" /\\_/\\ ", "95"),
           paint("( o.o )", "95"),
           paint(" > ^ < ", "95")]
    lines = [
        cat[0] + "   " + paint("CSC2103", "1", "93") + "  "
        + paint("Data Structures & Algorithms", "1"),
        cat[1] + "   " + paint(subtitle, "2"),
        cat[2] + "   " + paint("Greedy", "92") + paint(" · ", "2")
        + paint("Dynamic Programming", "96") + paint(" · ", "2")
        + paint("Heuristic", "93"),
    ]
    return box(lines, "96")


# ---------------------------------------------------------------------
#  Input helpers (validation in one place)
# ---------------------------------------------------------------------

def read_int(prompt, minimum=None):
    """Read a whole number, re-prompting until valid (>= minimum if given)."""
    while True:
        try:
            value = int(input(paint(prompt, "96")))
            if minimum is not None and value < minimum:
                print(paint(f"  -> Please enter a whole number >= {minimum}.", "91"))
                continue
            return value
        except ValueError:
            print(paint("  -> Invalid input. Please enter a whole number.", "91"))


def read_line(prompt):
    """Read a trimmed line of text with a coloured prompt."""
    return input(paint(prompt, "96")).strip()


def ask_run_again():
    """Return True if the user wants to run the current problem again."""
    return read_line("\nRun again with new input? (y/n): ").lower() == "y"
