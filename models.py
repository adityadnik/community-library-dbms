"""
models.py — CRUD operations (the Data Access Layer)
Community Tool & Seed Library Management System

DBMS Assignment - 9 (Mini Project)
Name    : Aditya Yadnik
Class   : SY CS-A
Roll No : 2070134
PRN     : 1251070951

Each function executes parameterised SQL queries to prevent SQL-injection
and returns plain Python dicts / lists for the UI layer to display.
"""

from database import get_connection


# ════════════════════════════════════════════════════════════
#  MEMBERS
# ════════════════════════════════════════════════════════════

def add_member(name: str, phone: str, email: str = "") -> int:
    """Insert a new member and return the new member_id."""
    sql = "INSERT INTO members (name, phone, email) VALUES (?, ?, ?)"
    conn = get_connection()
    with conn:
        cur = conn.execute(sql, (name.strip(), phone.strip(), email.strip()))
        new_id = cur.lastrowid
    conn.close()
    return new_id


def get_all_members() -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM members ORDER BY name"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def find_member(search: str) -> list:
    """Search by name or phone (partial match)."""
    like = f"%{search}%"
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM members WHERE name LIKE ? OR phone LIKE ? ORDER BY name",
        (like, like),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_member(member_id: int, name: str, phone: str, email: str) -> bool:
    sql = "UPDATE members SET name=?, phone=?, email=? WHERE member_id=?"
    conn = get_connection()
    with conn:
        cur = conn.execute(sql, (name, phone, email, member_id))
    conn.close()
    return cur.rowcount > 0


def deactivate_member(member_id: int) -> bool:
    conn = get_connection()
    with conn:
        cur = conn.execute(
            "UPDATE members SET active=0 WHERE member_id=?", (member_id,)
        )
    conn.close()
    return cur.rowcount > 0


# ════════════════════════════════════════════════════════════
#  ITEMS
# ════════════════════════════════════════════════════════════

def add_item(name: str, category_id: int, quantity: int,
             condition: str, description: str) -> int:
    sql = """INSERT INTO items (name, category_id, quantity, condition, description)
             VALUES (?, ?, ?, ?, ?)"""
    conn = get_connection()
    with conn:
        cur = conn.execute(sql, (name, category_id, quantity, condition, description))
        new_id = cur.lastrowid
    conn.close()
    return new_id


def get_all_items() -> list:
    sql = """
        SELECT i.item_id, i.name, c.category_name, i.quantity, i.condition, i.description
        FROM items i
        JOIN categories c ON c.category_id = i.category_id
        ORDER BY c.category_name, i.name
    """
    conn = get_connection()
    rows = conn.execute(sql).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def find_item(search: str) -> list:
    like = f"%{search}%"
    sql = """
        SELECT i.item_id, i.name, c.category_name, i.quantity, i.condition
        FROM items i
        JOIN categories c ON c.category_id = i.category_id
        WHERE i.name LIKE ? OR c.category_name LIKE ?
        ORDER BY i.name
    """
    conn = get_connection()
    rows = conn.execute(sql, (like, like)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_item_quantity(item_id: int, delta: int) -> bool:
    """Add delta (positive or negative) to item quantity."""
    conn = get_connection()
    with conn:
        cur = conn.execute(
            "UPDATE items SET quantity = quantity + ? WHERE item_id = ? AND quantity + ? >= 0",
            (delta, item_id, delta),
        )
    conn.close()
    return cur.rowcount > 0


def get_categories() -> list:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM categories ORDER BY category_name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ════════════════════════════════════════════════════════════
#  LOANS
# ════════════════════════════════════════════════════════════

def borrow_item(member_id: int, item_id: int,
                due_date: str, notes: str = "") -> int | None:
    """
    Create a loan record only if the item has available quantity.
    Returns loan_id on success, None if item unavailable.
    """
    conn = get_connection()
    with conn:
        qty = conn.execute(
            "SELECT quantity FROM items WHERE item_id=?", (item_id,)
        ).fetchone()
        if not qty or qty["quantity"] < 1:
            conn.close()
            return None

        # Decrement available quantity
        conn.execute("UPDATE items SET quantity = quantity - 1 WHERE item_id=?", (item_id,))

        # Insert loan record
        cur = conn.execute(
            """INSERT INTO loans (member_id, item_id, due_date, notes)
               VALUES (?, ?, ?, ?)""",
            (member_id, item_id, due_date, notes),
        )
        new_id = cur.lastrowid
    conn.close()
    return new_id


def return_item(loan_id: int) -> bool:
    """Mark a loan as returned and restore item quantity."""
    conn = get_connection()
    with conn:
        loan = conn.execute(
            "SELECT item_id, return_date FROM loans WHERE loan_id=?", (loan_id,)
        ).fetchone()
        if not loan or loan["return_date"] is not None:
            conn.close()
            return False  # already returned or doesn't exist

        conn.execute(
            "UPDATE loans SET return_date = DATE('now') WHERE loan_id=?", (loan_id,)
        )
        conn.execute(
            "UPDATE items SET quantity = quantity + 1 WHERE item_id=?", (loan["item_id"],)
        )
    conn.close()
    return True


def get_active_loans() -> list:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM v_active_loans").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_member_loan_history(member_id: int) -> list:
    sql = """
        SELECT l.loan_id, i.name AS item_name, l.borrow_date,
               l.due_date, l.return_date,
               CASE WHEN l.return_date IS NULL THEN 'Borrowed'
                    ELSE 'Returned' END AS status
        FROM loans l
        JOIN items i ON i.item_id = l.item_id
        WHERE l.member_id = ?
        ORDER BY l.borrow_date DESC
    """
    conn = get_connection()
    rows = conn.execute(sql, (member_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_overdue_loans() -> list:
    sql = """
        SELECT l.loan_id, m.name AS member_name, m.phone,
               i.name AS item_name, l.due_date,
               CAST(JULIANDAY('now') - JULIANDAY(l.due_date) AS INTEGER) AS days_overdue
        FROM loans l
        JOIN members m ON m.member_id = l.member_id
        JOIN items   i ON i.item_id   = l.item_id
        WHERE l.return_date IS NULL AND l.due_date < DATE('now')
        ORDER BY days_overdue DESC
    """
    conn = get_connection()
    rows = conn.execute(sql).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_summary_stats() -> dict:
    conn = get_connection()
    stats = {}
    stats["total_members"]       = conn.execute("SELECT COUNT(*) FROM members WHERE active=1").fetchone()[0]
    stats["total_items"]         = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    stats["items_in_stock"]      = conn.execute("SELECT SUM(quantity) FROM items").fetchone()[0] or 0
    stats["active_loans"]        = conn.execute("SELECT COUNT(*) FROM loans WHERE return_date IS NULL").fetchone()[0]
    stats["overdue_loans"]       = conn.execute(
        "SELECT COUNT(*) FROM loans WHERE return_date IS NULL AND due_date < DATE('now')"
    ).fetchone()[0]
    stats["total_borrows_ever"]  = conn.execute("SELECT COUNT(*) FROM loans").fetchone()[0]
    conn.close()
    return stats
