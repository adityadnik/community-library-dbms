"""
seed_demo.py — Populates the database with sample data for demonstration.

Run ONCE before showing the project:  python3 seed_demo.py
"""

from database import initialise_db, get_connection
import models
from datetime import date, timedelta

def seed():
    initialise_db()
    conn = get_connection()

    # ── Clear existing demo data ──────────────────────────────────────────────
    with conn:
        conn.execute("DELETE FROM loans")
        conn.execute("DELETE FROM items")
        conn.execute("DELETE FROM members")
        # Reset auto-increment counters
        conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('loans','items','members')")
    conn.close()

    # ── Members ───────────────────────────────────────────────────────────────
    members = [
        ("Aarav Sharma",     "9876543210", "aarav@mail.com"),
        ("Priya Mehta",      "9123456780", "priya@mail.com"),
        ("Rahul Verma",      "9988776655", "rahul@mail.com"),
        ("Sneha Joshi",      "9765432100", "sneha@mail.com"),
        ("Dev Patel",        "9012345678", ""),
        ("Kavya Nair",       "9856741230", "kavya@mail.com"),
    ]
    member_ids = []
    for name, phone, email in members:
        mid = models.add_member(name, phone, email)
        member_ids.append(mid)
        print(f"  Member added: {name} (ID {mid})")

    # ── Items (category IDs from seeded data: 1=Power, 2=Hand, 3=Garden, 4=Seeds, 5=Irrigation) ──
    items = [
        ("Cordless Drill (18V)", 1, 3, "Excellent", "Bosch GSB 18V-21 with 2 batteries"),
        ("Circular Saw",         1, 1, "Good",      "7-inch blade, 1200W"),
        ("Angle Grinder",        1, 2, "Fair",      "115mm disc grinder"),
        ("Hammer",               2, 5, "Good",      "16oz claw hammer"),
        ("Wrench Set (8-piece)", 2, 2, "Good",      "8mm–22mm combination wrenches"),
        ("Screwdriver Set",      2, 4, "Excellent", "Phillips and flathead, 10 pieces"),
        ("Garden Hoe",           3, 3, "Good",      "Long-handle steel hoe"),
        ("Hand Trowel",          3, 5, "Good",      "Stainless steel, ergonomic grip"),
        ("Rotary Tiller",        3, 1, "Good",      "Electric, 30cm width"),
        ("Heirloom Tomato Seeds",4, 20,"Excellent", "Brandywine variety, 50 seeds/pack"),
        ("Marigold Seeds",       4, 15,"Excellent", "Organic, open-pollinated"),
        ("Drip Irrigation Kit",  5, 2, "Good",      "50m kit with emitters and timer"),
        ("Garden Hose (20m)",    5, 3, "Fair",      "Heavy-duty rubber hose"),
    ]
    item_ids = []
    for name, cat_id, qty, cond, desc in items:
        iid = models.add_item(name, cat_id, qty, cond, desc)
        item_ids.append(iid)
        print(f"  Item added: {name} (ID {iid})")

    # ── Loans ─────────────────────────────────────────────────────────────────
    today = date.today()
    loans_data = [
        # (member_idx, item_idx, due_offset_days, already_returned, notes)
        (0, 0,  7, False, "For home shelf installation"),
        (1, 3, 14, False, ""),
        (2, 6,  7,  True, "For vegetable patch"),        # returned
        (3, 9, 14, False, "Growing experiment"),
        (4, 11,-5, False, "Overdue — drip system setup"), # overdue (due 5 days ago)
        (5, 12,-3, False, "Overdue — garden watering"),   # overdue
        (1, 7,  10, True, "Weekend planting"),            # returned
    ]
    for mi, ii, due_offset, returned, note in loans_data:
        due = (today + timedelta(days=due_offset)).isoformat()
        lid = models.borrow_item(member_ids[mi], item_ids[ii], due, note)
        if lid and returned:
            models.return_item(lid)
        print(f"  Loan #{lid}: {members[mi][0]} borrowed {items[ii][0]}")

    print("\n[OK] Sample data loaded successfully!")
    print("     Run  python3 main.py  to start the application.\n")


if __name__ == "__main__":
    seed()
