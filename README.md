# DBMS Assignment - 9 (Mini Project)
## Community Tool & Seed Library — Database Connectivity Demo

![MIT License](https://img.shields.io/badge/License-MIT-green.svg)

| Field | Details |
|-------|---------|
| **Name** | Aditya Yadnik |
| **Class** | SY CS-A |
| **Roll No** | 2070134 |
| **PRN** | 1251070951 |
| **Subject** | Database Management Systems (DBMS) |
| **Language** | Python 3 |
| **Database** | SQLite (via built-in `sqlite3` module — no installation needed) |

---

## How to Run

```bash
# Step 1 — go to the project folder
cd community-library-dbms

# Step 2 — load sample data (run only once)
python3 seed_demo.py

# Step 3 — launch the application
python3 main.py
```

---

## Project Structure

| File | Purpose |
|------|---------|
| `database.py` | DB connection, schema (CREATE TABLE), view |
| `models.py` | CRUD operations — all SQL queries live here |
| `ui.py` | Terminal UI helpers (colours, tables, prompts) |
| `main.py` | Menu controller / entry point |
| `seed_demo.py` | Populates sample data for demo |
| `library.db` | SQLite database file (auto-created on first run) |

---

## Database Schema

```
members ──┐
          │  (FK: member_id)
          ├──── loans ────┤
          │               │ (FK: item_id)
categories ─── items ─────┘
```

### Tables

**members** — Library cardholders  
**categories** — Tool/seed categories (seeded: Power Tools, Hand Tools, etc.)  
**items** — Individual tools/seeds with quantity tracking  
**loans** — Borrow/return records (return_date NULL = still borrowed)  
**v_active_loans** — VIEW joining all three tables for active loans

---

## Features Demonstrated

- ✅ Database connection with `sqlite3`  
- ✅ Schema creation with `PRIMARY KEY`, `FOREIGN KEY`, `CHECK` constraints  
- ✅ Referential integrity (`PRAGMA foreign_keys = ON`)  
- ✅ Parameterised queries (prevents SQL injection)  
- ✅ `INSERT`, `SELECT`, `UPDATE` operations  
- ✅ `JOIN` across multiple tables  
- ✅ Aggregate functions (`COUNT`, `SUM`, `JULIANDAY`)  
- ✅ SQL `VIEW` for reusable complex queries  
- ✅ Transaction management (`with conn:` blocks)  
- ✅ Row factory for dict-style column access  
