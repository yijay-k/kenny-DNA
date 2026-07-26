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
import unicodedata

_COLOR = bool(
    (sys.stdout.isatty() or os.environ.get("FORCE_COLOR"))
    and os.environ.get("NO_COLOR") is None
)

_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


# ---------------------------------------------------------------------
#  Colour + layout
# ---------------------------------------------------------------------

def paint(text, *codes):
    """Wrap text in ANSI codes (a no-op when colour is disabled or codes empty)."""
    codes = [c for c in codes if c]
    if not _COLOR or not codes:
        return text
    return f"\033[{';'.join(codes)}m{text}\033[0m"


def visible_len(text):
    """
    On-screen width of text, ignoring ANSI colour codes and counting wide
    glyphs (most emoji / CJK) as 2 columns so boxes stay aligned.
    """
    stripped = _ANSI_RE.sub("", str(text))
    width = 0
    for ch in stripped:
        if ch in ("‍", "️", "︎") or unicodedata.combining(ch):
            continue  # zero-width joiner / variation selectors / accents
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def center(text, width):
    """Centre text within `width` columns (colour-aware)."""
    gap = width - visible_len(text)
    if gap <= 0:
        return text
    left = gap // 2
    return " " * left + text + " " * (gap - left)


def box(lines, code="", pad=1):
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


def section(title, code=""):
    """A clean section header shown before each problem's output."""
    tail = "━" * max(3, 50 - visible_len(title))
    return "\n" + paint("━━━  " + title + "  " + tail, "1", code)


def table(headers, rows, code=""):
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
    """The cute ASCII-art welcome banner (sleepy cat + course title)."""
    width = 50
    cat = [
        r"   |\      _,,,---,,_",
        r"   /,`.-'`'    -.  ;-;;,_",
        r"  |,4-  ) )-,_..;\ (  `'-'",
        r" '---''(_/--'  `-'\_)",
    ]
    # Indent the whole cat by one amount so the art keeps its shape.
    indent = " " * max(0, (width - max(len(c) for c in cat)) // 2)
    lines = [
        "",
        indent + cat[0],
        indent + cat[1],
        indent + cat[2] + paint("   z z z 💤", "2"),
        indent + cat[3],
        "",
        center(paint("✨ CSC2103 ✨", "1") + "  "
               + paint("Data Structures & Algorithms", "1"), width),
        center(paint(subtitle, "2"), width),
        "",
        center(paint("🐾  Greedy  ·  Dynamic Programming  ·  Heuristic", "1"), width),
        "",
    ]
    return box(lines)


# ---------------------------------------------------------------------
#  Input helpers (validation in one place)
# ---------------------------------------------------------------------

def read_int(prompt, minimum=None):
    """Read a whole number, re-prompting until valid (>= minimum if given)."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print(paint(f"  -> Please enter a whole number >= {minimum}.", "91"))
                continue
            return value
        except ValueError:
            print(paint("  -> Invalid input. Please enter a whole number.", "91"))


def read_line(prompt):
    """Read a trimmed line of text."""
    return input(prompt).strip()


def ask_run_again():
    """Return True if the user wants to run the current problem again."""
    return read_line("\nRun again with new input? (y/n): ").lower() == "y"
