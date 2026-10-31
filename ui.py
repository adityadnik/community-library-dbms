"""
ui.py — Terminal UI helpers (colours, tables, prompts)
Community Tool & Seed Library Management System

DBMS Assignment - 9 (Mini Project)
Name    : Aditya Yadnik
Class   : SY CS-A
Roll No : 2070134
PRN     : 1251070951
"""

import os
import shutil

# ── ANSI colour codes ─────────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    CYAN   = "\033[96m"
    BLUE   = "\033[94m"
    MAGENTA= "\033[95m"
    DIM    = "\033[2m"

def enable_ansi():
    """Enable ANSI escape codes on Windows."""
    if os.name == "nt":
        os.system("")   # activates VT100 on Windows 10+


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def width() -> int:
    return shutil.get_terminal_size((80, 24)).columns


def hr(char="─", color=C.DIM):
    print(color + char * width() + C.RESET)


def banner(title: str, subtitle: str = "", assignment: str = "", student: str = ""):
    w = width()
    clear()
    print(C.GREEN + "=" * w + C.RESET)
    # Assignment line
    if assignment:
        pad0 = max(0, (w - len(assignment)) // 2)
        print(C.BOLD + C.YELLOW + " " * pad0 + assignment + C.RESET)
        print(C.GREEN + "-" * w + C.RESET)
    # Title
    pad = max(0, (w - len(title)) // 2)
    print(C.BOLD + C.GREEN + " " * pad + title + C.RESET)
    # Subtitle
    if subtitle:
        pad2 = max(0, (w - len(subtitle)) // 2)
        print(C.DIM + " " * pad2 + subtitle + C.RESET)
    # Student info
    if student:
        print(C.GREEN + "-" * w + C.RESET)
        pad3 = max(0, (w - len(student)) // 2)
        print(C.CYAN + " " * pad3 + student + C.RESET)
    print(C.GREEN + "=" * w + C.RESET)
    print()


def section(title: str):
    print()
    print(C.CYAN + C.BOLD + f"  ◆ {title}" + C.RESET)
    hr("─", C.DIM)


def success(msg: str):
    print(C.GREEN + f"  ✔  {msg}" + C.RESET)


def error(msg: str):
    print(C.RED + f"  ✘  {msg}" + C.RESET)


def warn(msg: str):
    print(C.YELLOW + f"  ⚠  {msg}" + C.RESET)


def info(msg: str):
    print(C.BLUE + f"  ℹ  {msg}" + C.RESET)


# ── Simple columnar table ─────────────────────────────────────────────────────

def table(rows: list, headers: list, col_widths: list = None):
    """
    Print a plain-text table.
    rows      : list of lists/tuples (values in same order as headers)
    headers   : column header strings
    col_widths: optional list of minimum widths
    """
    if not rows:
        warn("No records found.")
        return

    if col_widths is None:
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in col_widths)
    sep = "  " + "  ".join("─" * w for w in col_widths)

    print(C.BOLD + fmt.format(*headers) + C.RESET)
    print(C.DIM  + sep + C.RESET)
    for row in rows:
        print(fmt.format(*[str(v) for v in row]))


# ── Input helpers ─────────────────────────────────────────────────────────────

def prompt(label: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    val = input(f"  {C.YELLOW}{label}{hint}: {C.RESET}").strip()
    return val if val else default


def prompt_int(label: str, default: int = None) -> int:
    while True:
        raw = prompt(label, str(default) if default is not None else "")
        try:
            return int(raw)
        except ValueError:
            error("Please enter a whole number.")


def prompt_choice(options: list, label: str = "Choose") -> int:
    """Print a numbered menu and return the user's 1-based choice (as int)."""
    for i, opt in enumerate(options, 1):
        print(f"  {C.CYAN}{i:>2}{C.RESET}. {opt}")
    while True:
        raw = prompt(label)
        try:
            n = int(raw)
            if 1 <= n <= len(options):
                return n
        except ValueError:
            pass
        error(f"Enter a number between 1 and {len(options)}.")


def pause():
    input(C.DIM + "\n  Press Enter to continue…" + C.RESET)
