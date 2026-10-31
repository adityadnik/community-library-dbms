"""
main.py -- Entry point & menu controller
Community Tool & Seed Library Management System

DBMS Assignment - 9 (Mini Project)
Name    : Aditya Yadnik
Class   : SY CS-A
Roll No : 2070134
PRN     : 1251070951

Run:  python3 main.py
"""

from datetime import date, timedelta
import sys

import ui
from ui import C
import models
from database import initialise_db

ASSIGNMENT   = "DBMS Assignment - 9 (Mini Project)"
APP_TITLE    = "Community Tool & Seed Library"
STUDENT_INFO = "Name: Aditya Yadnik  |  Class: SY CS-A  |  Roll No: 2070134  |  PRN: 1251070951"


# ════════════════════════════════════════════════════════════
#  MEMBERS MENU
# ════════════════════════════════════════════════════════════

def menu_members():
    while True:
        ui.banner(APP_TITLE, "Members",
                  assignment=ASSIGNMENT, student=STUDENT_INFO)
        ui.section("Members Menu")
        choice = ui.prompt_choice([
            "Add New Member",
            "View All Members",
            "Search Member",
            "Update Member Details",
            "View Member Loan History",
            "Deactivate Member",
            "← Back to Main Menu",
        ])

        if choice == 1:
            _add_member()
        elif choice == 2:
            _view_all_members()
        elif choice == 3:
            _search_member()
        elif choice == 4:
            _update_member()
        elif choice == 5:
            _member_history()
        elif choice == 6:
            _deactivate_member()
        else:
            break


def _add_member():
    ui.section("Add New Member")
    name  = ui.prompt("Full name")
    if not name:
        ui.error("Name cannot be empty."); ui.pause(); return
    phone = ui.prompt("Phone number")
    if not phone:
        ui.error("Phone cannot be empty."); ui.pause(); return
    email = ui.prompt("Email (optional)")
    try:
        mid = models.add_member(name, phone, email)
        ui.success(f"Member added! ID = {mid}")
    except Exception as e:
        ui.error(f"Could not add member: {e}")
    ui.pause()


def _view_all_members():
    ui.section("All Members")
    members = models.get_all_members()
    rows = [
        [m["member_id"], m["name"], m["phone"],
         m["email"] or "—", m["join_date"],
         "Active" if m["active"] else "Inactive"]
        for m in members
    ]
    ui.table(rows, ["ID", "Name", "Phone", "Email", "Joined", "Status"],
             [4, 22, 14, 26, 12, 8])
    ui.pause()


def _search_member():
    ui.section("Search Member")
    q = ui.prompt("Name or phone")
    members = models.find_member(q)
    rows = [[m["member_id"], m["name"], m["phone"], m["email"] or "—"] for m in members]
    ui.table(rows, ["ID", "Name", "Phone", "Email"], [4, 22, 14, 26])
    ui.pause()


def _update_member():
    ui.section("Update Member")
    mid = ui.prompt_int("Member ID to update")
    members = models.find_member(str(mid))
    found = [m for m in members if m["member_id"] == mid]
    if not found:
        ui.error("Member not found."); ui.pause(); return
    m = found[0]
    ui.info(f"Editing: {m['name']} | {m['phone']} | {m['email']}")
    name  = ui.prompt("New name",  m["name"])
    phone = ui.prompt("New phone", m["phone"])
    email = ui.prompt("New email", m["email"] or "")
    if models.update_member(mid, name, phone, email):
        ui.success("Member updated.")
    else:
        ui.error("Update failed.")
    ui.pause()


def _member_history():
    ui.section("Member Loan History")
    mid = ui.prompt_int("Member ID")
    history = models.get_member_loan_history(mid)
    rows = [
        [h["loan_id"], h["item_name"], h["borrow_date"], h["due_date"],
         h["return_date"] or "—", h["status"]]
        for h in history
    ]
    ui.table(rows, ["Loan#", "Item", "Borrowed", "Due", "Returned", "Status"],
             [6, 22, 12, 12, 12, 10])
    ui.pause()


def _deactivate_member():
    ui.section("Deactivate Member")
    mid = ui.prompt_int("Member ID to deactivate")
    confirm = ui.prompt(f"Deactivate member {mid}? (yes/no)", "no")
    if confirm.lower() == "yes":
        if models.deactivate_member(mid):
            ui.success("Member deactivated.")
        else:
            ui.error("Member not found.")
    else:
        ui.warn("Cancelled.")
    ui.pause()


# ════════════════════════════════════════════════════════════
#  ITEMS MENU
# ════════════════════════════════════════════════════════════

def menu_items():
    while True:
        ui.banner(APP_TITLE, "Inventory",
                  assignment=ASSIGNMENT, student=STUDENT_INFO)
        ui.section("Inventory Menu")
        choice = ui.prompt_choice([
            "Add New Item",
            "View All Items",
            "Search Items",
            "Adjust Item Quantity",
            "View Categories",
            "← Back to Main Menu",
        ])

        if choice == 1:
            _add_item()
        elif choice == 2:
            _view_all_items()
        elif choice == 3:
            _search_item()
        elif choice == 4:
            _adjust_quantity()
        elif choice == 5:
            _view_categories()
        else:
            break


def _add_item():
    ui.section("Add New Item")
    cats = models.get_categories()
    ui.info("Select a category:")
    cat_choice = ui.prompt_choice([f"{c['category_name']} — {c['description']}" for c in cats])
    cat_id = cats[cat_choice - 1]["category_id"]

    name  = ui.prompt("Item name")
    if not name:
        ui.error("Name cannot be empty."); ui.pause(); return
    qty   = ui.prompt_int("Quantity available", 1)
    ui.info("Condition options: Excellent / Good / Fair / Needs Repair")
    cond  = ui.prompt("Condition", "Good")
    desc  = ui.prompt("Description (optional)")

    try:
        iid = models.add_item(name, cat_id, qty, cond, desc)
        ui.success(f"Item added! ID = {iid}")
    except Exception as e:
        ui.error(f"Could not add item: {e}")
    ui.pause()


def _view_all_items():
    ui.section("All Inventory Items")
    items = models.get_all_items()
    rows = [
        [i["item_id"], i["name"], i["category_name"],
         i["quantity"], i["condition"], (i["description"] or "")[:30]]
        for i in items
    ]
    ui.table(rows, ["ID", "Name", "Category", "Qty", "Condition", "Description"],
             [4, 24, 18, 4, 14, 32])
    ui.pause()


def _search_item():
    ui.section("Search Items")
    q = ui.prompt("Item name or category")
    items = models.find_item(q)
    rows = [
        [i["item_id"], i["name"], i["category_name"], i["quantity"], i["condition"]]
        for i in items
    ]
    ui.table(rows, ["ID", "Name", "Category", "Qty", "Condition"],
             [4, 24, 18, 4, 14])
    ui.pause()


def _adjust_quantity():
    ui.section("Adjust Item Quantity")
    iid   = ui.prompt_int("Item ID")
    delta = ui.prompt_int("Change in quantity (negative to reduce)")
    if models.update_item_quantity(iid, delta):
        ui.success(f"Quantity updated by {delta:+d}.")
    else:
        ui.error("Update failed — item not found or quantity would go negative.")
    ui.pause()


def _view_categories():
    ui.section("Item Categories")
    cats = models.get_categories()
    rows = [[c["category_id"], c["category_name"], c["description"] or ""] for c in cats]
    ui.table(rows, ["ID", "Category", "Description"], [4, 20, 40])
    ui.pause()


# ════════════════════════════════════════════════════════════
#  LOANS MENU
# ════════════════════════════════════════════════════════════

def menu_loans():
    while True:
        ui.banner(APP_TITLE, "Loans",
                  assignment=ASSIGNMENT, student=STUDENT_INFO)
        ui.section("Loans Menu")
        choice = ui.prompt_choice([
            "Borrow an Item",
            "Return an Item",
            "View All Active Loans",
            "View Overdue Loans",
            "← Back to Main Menu",
        ])

        if choice == 1:
            _borrow()
        elif choice == 2:
            _return()
        elif choice == 3:
            _active_loans()
        elif choice == 4:
            _overdue_loans()
        else:
            break


def _borrow():
    ui.section("Borrow an Item")
    mid  = ui.prompt_int("Member ID")
    iid  = ui.prompt_int("Item ID")
    days = ui.prompt_int("Loan period (days)", 14)
    due  = (date.today() + timedelta(days=days)).isoformat()
    ui.info(f"Due date will be: {due}")
    notes = ui.prompt("Notes (optional)")

    result = models.borrow_item(mid, iid, due, notes)
    if result:
        ui.success(f"Loan created! Loan ID = {result}  |  Due: {due}")
    else:
        ui.error("Could not create loan — item may be out of stock, or IDs are invalid.")
    ui.pause()


def _return():
    ui.section("Return an Item")
    lid = ui.prompt_int("Loan ID to return")
    if models.return_item(lid):
        ui.success("Item returned successfully. Inventory updated.")
    else:
        ui.error("Return failed — loan not found or item was already returned.")
    ui.pause()


def _active_loans():
    ui.section("Active Loans")
    loans = models.get_active_loans()
    rows = [
        [l["loan_id"], l["member_name"], l["item_name"],
         l["category_name"], l["borrow_date"], l["due_date"]]
        for l in loans
    ]
    ui.table(rows,
             ["Loan#", "Member", "Item", "Category", "Borrowed", "Due"],
             [6, 20, 22, 18, 12, 12])
    ui.pause()


def _overdue_loans():
    ui.section("-- Overdue Loans --")
    loans = models.get_overdue_loans()
    if not loans:
        ui.success("No overdue loans — great job, everyone!"); ui.pause(); return
    rows = [
        [l["loan_id"], l["member_name"], l["phone"],
         l["item_name"], l["due_date"], l["days_overdue"]]
        for l in loans
    ]
    ui.table(rows,
             ["Loan#", "Member", "Phone", "Item", "Due Date", "Days Overdue"],
             [6, 20, 14, 22, 12, 13])
    ui.pause()


# ════════════════════════════════════════════════════════════
#  DASHBOARD
# ════════════════════════════════════════════════════════════

def show_dashboard():
    ui.banner(APP_TITLE, "Python + SQLite",
              assignment=ASSIGNMENT, student=STUDENT_INFO)
    stats = models.get_summary_stats()
    ui.section("Dashboard — Library at a Glance")

    def stat_line(label, value, color=C.CYAN):
        print(f"  {C.DIM}{label:<30}{C.RESET} {color}{C.BOLD}{value}{C.RESET}")

    stat_line("Active Members",        stats["total_members"])
    stat_line("Total Item Types",      stats["total_items"])
    stat_line("Items Currently In Stock", stats["items_in_stock"])
    stat_line("Items Currently On Loan",  stats["active_loans"])
    stat_line("Overdue Returns",       stats["overdue_loans"],
              C.RED if stats["overdue_loans"] > 0 else C.GREEN)
    stat_line("All-time Borrows",      stats["total_borrows_ever"])
    print()


# ════════════════════════════════════════════════════════════
#  MAIN MENU
# ════════════════════════════════════════════════════════════

def main():
    ui.enable_ansi()
    initialise_db()

    while True:
        show_dashboard()
        ui.section("Main Menu")
        choice = ui.prompt_choice([
            "[1] Members Management",
            "[2] Inventory Management",
            "[3] Loan Management",
            "[X] Exit",
        ])

        if choice == 1:
            menu_members()
        elif choice == 2:
            menu_items()
        elif choice == 3:
            menu_loans()
        else:
            ui.banner(APP_TITLE, "Goodbye!",
                      assignment=ASSIGNMENT, student=STUDENT_INFO)
            print(C.GREEN + "  Thank you for using the Community Library System.\n" + C.RESET)
            sys.exit(0)


if __name__ == "__main__":
    main()
