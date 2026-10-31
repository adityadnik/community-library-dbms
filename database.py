"""
database.py — Database connection and schema setup module
Community Tool & Seed Library Management System

DBMS Assignment - 9 (Mini Project)
Name    : Aditya Yadnik
Class   : SY CS-A
Roll No : 2070134
PRN     : 1251070951

Demonstrates:
  - Establishing a connection to a SQLite relational database
  - Creating normalized relational tables with PRIMARY KEY / FOREIGN KEY constraints
  - Enforcing referential integrity via PRAGMA foreign_keys = ON
"""

import sqlite3
import os

# ── Configuration ────────────────────────────────────────────────────────────
DB_FILE = os.path.join(os.path.dirname(__file__), "library.db")


# ── Connection factory ────────────────────────────────────────────────────────
def get_connection() -> sqlite3.Connection:
    """
    Open (or create) the SQLite database and return a connection object.
    Row factory is set so rows behave like dictionaries.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row          # access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # enforce FK constraints
    return conn


# ── Schema creation ───────────────────────────────────────────────────────────
CREATE_MEMBERS = """
CREATE TABLE IF NOT EXISTS members (
    member_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    phone       TEXT    NOT NULL UNIQUE,
    email       TEXT,
    join_date   TEXT    NOT NULL DEFAULT (DATE('now')),
    active      INTEGER NOT NULL DEFAULT 1   -- 1 = active, 0 = deactivated
);
"""

CREATE_CATEGORIES = """
CREATE TABLE IF NOT EXISTS categories (
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT    NOT NULL UNIQUE,
    description   TEXT
);
"""

CREATE_ITEMS = """
CREATE TABLE IF NOT EXISTS items (
    item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL,
    category_id  INTEGER NOT NULL REFERENCES categories(category_id),
    quantity     INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 0),
    condition    TEXT    NOT NULL DEFAULT 'Good'
                         CHECK (condition IN ('Excellent','Good','Fair','Needs Repair')),
    description  TEXT,
    added_date   TEXT    NOT NULL DEFAULT (DATE('now'))
);
"""

CREATE_LOANS = """
CREATE TABLE IF NOT EXISTS loans (
    loan_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id    INTEGER NOT NULL REFERENCES members(member_id),
    item_id      INTEGER NOT NULL REFERENCES items(item_id),
    borrow_date  TEXT    NOT NULL DEFAULT (DATE('now')),
    due_date     TEXT    NOT NULL,
    return_date  TEXT,                      -- NULL means still borrowed
    notes        TEXT
);
"""

# Useful view: active (not-yet-returned) loans with member & item names
CREATE_VIEW_ACTIVE_LOANS = """
CREATE VIEW IF NOT EXISTS v_active_loans AS
SELECT
    l.loan_id,
    m.name        AS member_name,
    m.phone       AS member_phone,
    i.name        AS item_name,
    c.category_name,
    l.borrow_date,
    l.due_date
FROM loans l
JOIN members   m ON m.member_id  = l.member_id
JOIN items     i ON i.item_id    = l.item_id
JOIN categories c ON c.category_id = i.category_id
WHERE l.return_date IS NULL
ORDER BY l.due_date;
"""


def initialise_db() -> None:
    """Create tables and seed categories if the database is brand-new."""
    conn = get_connection()
    with conn:
        conn.execute(CREATE_MEMBERS)
        conn.execute(CREATE_CATEGORIES)
        conn.execute(CREATE_ITEMS)
        conn.execute(CREATE_LOANS)
        conn.execute(CREATE_VIEW_ACTIVE_LOANS)

        # Seed default categories (INSERT OR IGNORE avoids duplicates)
        seed_categories = [
            ("Power Tools",   "Drills, saws, grinders, etc."),
            ("Hand Tools",    "Hammers, wrenches, screwdrivers, etc."),
            ("Garden Equipment", "Rakes, hoes, tillers, mowers, etc."),
            ("Heirloom Seeds",   "Open-pollinated, non-hybrid seeds for sharing"),
            ("Irrigation",       "Hoses, drip-lines, soaker pipes, etc."),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO categories (category_name, description) VALUES (?, ?)",
            seed_categories,
        )
    conn.close()
    print(f"[DB] Connected to '{DB_FILE}' — schema ready.")
