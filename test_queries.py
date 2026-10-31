"""Quick smoke test — runs all queries and prints results."""
from database import initialise_db
from models import (get_all_members, get_all_items, get_active_loans,
                    get_overdue_loans, get_summary_stats, get_member_loan_history)

initialise_db()

print("=== MEMBERS ===")
for m in get_all_members():
    print(f"  [{m['member_id']}] {m['name']:25} {m['phone']}")

print("\n=== INVENTORY ===")
for i in get_all_items():
    print(f"  [{i['item_id']:2}] {i['name']:32} Cat:{i['category_name']:18} Qty:{i['quantity']}")

print("\n=== ACTIVE LOANS ===")
for l in get_active_loans():
    print(f"  Loan#{l['loan_id']} {l['member_name']:20} -> {l['item_name']:32} Due:{l['due_date']}")

print("\n=== OVERDUE LOANS ===")
for l in get_overdue_loans():
    print(f"  Loan#{l['loan_id']} {l['member_name']:20} -> {l['item_name']:32} OVERDUE by {l['days_overdue']} days")

print("\n=== DASHBOARD STATS ===")
for k, v in get_summary_stats().items():
    print(f"  {k:<30} {v}")

print("\n=== MEMBER #2 LOAN HISTORY ===")
for h in get_member_loan_history(2):
    print(f"  Loan#{h['loan_id']} {h['item_name']:32} {h['status']}")
