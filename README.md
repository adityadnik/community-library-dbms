# DBMS Assignment - 9 (Mini Project)
## Community Tool & Seed Library — Relational Database (SQL) Connectivity System

![MIT License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Language-Python%203-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57.svg)

| Field | Details |
|-------|---------|
| **Name** | Aditya Yadnik |
| **Class** | SY CS-A |
| **Roll No** | 2070134 |
| **PRN** | 1251070951 |
| **Subject** | Database Management Systems (DBMS) |
| **Assignment** | Assignment 9: Database Connectivity with Relational Database (SQL) |
| **Language** | Python 3 |
| **Database Engine** | SQLite (via built-in standard library `sqlite3`) |

---

## 📖 What It Is

The **Community Tool & Seed Library Management System** is a real-world relational database application designed for local neighborhood cooperatives and urban-farming communities. Instead of buying expensive power machinery or commercial seeds individually, members borrow shared physical power tools (drills, saws, tillers), hand tools (wrenches, hammers), irrigation kits, and open-pollinated heirloom seeds.

### Problem Statement & Practical Need
1. **Resource Sharing & Waste Reduction:** High-cost tools like angle grinders or tillers sit idle 95% of the time in individual households. A managed community library allows pooled resources.
2. **Inventory & Availability Tracking:** Shared goods require strict tracking to prevent equipment loss, monitor item conditions (from "Excellent" to "Needs Repair"), and ensure items are not double-borrowed.
3. **Accountability & Return Cycles:** Borrowers need clear loan periods and due dates. Cooperative managers need automated alerts for overdue items with contact information for reminders.

---

## ⚙️ How It Works

The system implements a structured **3-tier modular architecture** ensuring separation of concerns:

```
┌────────────────────────────────────────────────────────┐
│            Presentation Layer (ui.py, main.py)         │
│  - Interactive CLI Terminal Interface with ANSI Colors │
│  - Menu Routing, Input Validation & Formatters         │
└───────────────────────────┬────────────────────────────┘
                            │ Method Calls
┌───────────────────────────▼────────────────────────────┐
│         Data Access Layer / DAO (models.py)            │
│  - Parameterized SQL Execution                         │
│  - Transaction Orchestration (Commit / Rollback)       │
│  - Business Logic (Stock decrements, view querying)    │
└───────────────────────────┬────────────────────────────┘
                            │ Raw SQL Queries & DDL
┌───────────────────────────▼────────────────────────────┐
│        Relational Database Layer (database.py)         │
│  - SQLite Engine with Foreign Key Enforcement          │
│  - Schema Definition, Tables, Constraints & Views      │
│  - Persistent storage in library.db                    │
└────────────────────────────────────────────────────────┘
```

### Core Execution Flow & Lifecycle:

1. **Database Initialization & Connection Management (`database.py`):**
   - Establishes a persistent connection to `library.db`.
   - Executes `PRAGMA foreign_keys = ON` to enforce relational constraints.
   - Sets `conn.row_factory = sqlite3.Row` for key-indexed record mapping.
   - Creates normalized tables (`members`, `categories`, `items`, `loans`) and an optimized SQL view (`v_active_loans`).

2. **Atomic Borrowing Workflow (Transaction-Protected):**
   - A member requests an item ID.
   - The system checks available quantity (`quantity > 0`).
   - In a single atomic transaction block (`with conn:`):
     - An active loan entry is inserted into `loans` with `due_date` and `return_date = NULL`.
     - The corresponding item's `quantity` is decremented by 1 in `items`.
   - If stock is insufficient, the transaction halts, preventing negative inventory.

3. **Check-In & Restock Workflow:**
   - On item return, the loan record is stamped with today's return date (`return_date = DATE('now')`).
   - The item's stock count is automatically restored (`quantity = quantity + 1`).

4. **Overdue Loan Calculation Engine:**
   - Computes elapsed time using SQLite's native `JULIANDAY('now') - JULIANDAY(l.due_date)`.
   - Filters loans where `return_date IS NULL` and `due_date < DATE('now')`.
   - Displays real-time day counts overdue along with borrower phone numbers for contact.

5. **Real-Time Analytics Dashboard:**
   - Aggregates system metrics (`COUNT(*)`, `SUM(quantity)`) to surface active cardholders, tools in circulation, total inventory, and outstanding loans on the home screen.

---

## 🗄️ Database Schema & Relational Design

```
members (1) ──────────────┐
                          │
                          ├─────< (M) loans (M) >─────┐
                          │                           │
categories (1) ───< (M) items ────────────────────────┘
```

### Tables Specification

- **`categories`**:
  - `category_id` (INTEGER, PK, AUTOINCREMENT)
  - `category_name` (TEXT, UNIQUE, NOT NULL)
  - `description` (TEXT)

- **`members`**:
  - `member_id` (INTEGER, PK, AUTOINCREMENT)
  - `name` (TEXT, NOT NULL)
  - `phone` (TEXT, UNIQUE, NOT NULL)
  - `email` (TEXT)
  - `join_date` (TEXT, DEFAULT `DATE('now')`)
  - `active` (INTEGER, DEFAULT 1) — enables soft-deletion

- **`items`**:
  - `item_id` (INTEGER, PK, AUTOINCREMENT)
  - `name` (TEXT, NOT NULL)
  - `category_id` (INTEGER, FK -> `categories.category_id`)
  - `quantity` (INTEGER, NOT NULL, CHECK `quantity >= 0`)
  - `condition` (TEXT, CHECK `condition IN ('Excellent', 'Good', 'Fair', 'Needs Repair')`)
  - `description` (TEXT)
  - `added_date` (TEXT, DEFAULT `DATE('now')`)

- **`loans`**:
  - `loan_id` (INTEGER, PK, AUTOINCREMENT)
  - `member_id` (INTEGER, FK -> `members.member_id`)
  - `item_id` (INTEGER, FK -> `items.item_id`)
  - `borrow_date` (TEXT, DEFAULT `DATE('now')`)
  - `due_date` (TEXT, NOT NULL)
  - `return_date` (TEXT, NULLABLE)
  - `notes` (TEXT)

- **`v_active_loans` (SQL View):**
  - Pre-joins `loans`, `members`, `items`, and `categories` to provide instant reporting for unreturned items without repeatedly writing multi-table `JOIN` statements.

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+ installed (no external pip dependencies needed; uses Python standard library `sqlite3`).

### Steps
```bash
# 1. Clone repository
git clone https://github.com/Adityadnik/community-library-dbms.git
cd community-library-dbms

# 2. Seed initial demo data (members, tool inventory, active/overdue loans)
python3 seed_demo.py

# 3. Launch interactive CLI application
python3 main.py
```

### Running Automated Query Verification
```bash
python3 test_queries.py
```

---

## 📂 Project Structure

| File | Purpose |
|------|---------|
| `database.py` | Connection factory, DDL schema generation, view definitions, constraint enforcement |
| `models.py` | Data Access Layer: CRUD queries, parameterized SQL statements, transactions |
| `ui.py` | ANSI-colored terminal components, formatted tables, interactive prompt helpers |
| `main.py` | Application controller, menu routing, screen navigation |
| `seed_demo.py` | Database seeder for populating realistic test fixtures |
| `test_queries.py` | Automated test suite validating all SQL functions and joins |
| `library.db` | Auto-generated SQLite relational database file |
| `LICENSE` | MIT Open-Source License |

---

## 🎓 DBMS Concepts Demonstrated

- **DDL (Data Definition Language):** Strict schema definition using `CREATE TABLE` and `CREATE VIEW` with typed attributes and domain constraints (`CHECK`, `DEFAULT`, `NOT NULL`).
- **Referential Integrity:** Primary key / Foreign key enforcement via `PRAGMA foreign_keys = ON`.
- **DML (Data Manipulation Language):** Secure, parameterized `INSERT`, `SELECT`, `UPDATE`, and `DELETE` operations.
- **Relational Joins:** Three-way inner joins combining `loans`, `members`, and `items`.
- **SQL Aggregations & Built-in Functions:** `COUNT()`, `SUM()`, `JULIANDAY()` date arithmetic.
- **Transactions & Concurrency:** Atomic database commits using context managers (`with conn:`), guaranteeing data consistency during loan creation and item returns.
- **SQL Injection Prevention:** 100% parameter substitution with `?` bind variables.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE) - Copyright (c) 2026 Aditya Yadnik.
