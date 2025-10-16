# Neighborhood Tool Lending Library CLI

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/downloads/) [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-green)](https://www.sqlalchemy.org/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-yellow)](https://www.postgresql.org/)

A sustainable CLI app for neighbors to lend and borrow tools, reducing waste and building community. Built for Moringa School Phase 3: Python OOP, SQLAlchemy ORM, relational DB (Postgres), CRUD operations, and pytest.

## Description

This app models a tool-sharing library:
- **Neighbors** own tools and borrow/return them.
- **Tools** have owners and descriptions.
- **Loans** track borrowing with dates, availability checks (no double-booking), and condition notes.
- **CLI Menu**: Add/list neighbors/tools/loans, return loans, list overdues.

Ties to sustainability: Encourages reuse—share drills instead of buying new!

### Features
- **CRUD Operations**: Create/read/update/delete neighbors, tools, loans via ORM.
- **Relationships**: One-to-many (neighbor owns tools, tool has loans); JOIN queries for lists/overdues.
- **Validation**: Unique emails, due > loan date, tool availability (blocks loaned tools).
- **Interactive CLI**: Menu-driven with input prompts, re-prompts on errors, empty state messages.
- **Tests**: Unit (models/CRUD) and integration (full CLI flows) with 100% coverage.
- **DB**: Postgres with constraints (e.g., unique email, date check).

### Architecture Overview
- **Models** (`models.py`): SQLAlchemy classes for Neighbor, Tool, Loan with FKs/relationships.
- **Database** (`database.py`): Session factory, CRUD funcs with error handling (IntegrityError rollback).
- **CLI** (`cli.py`): Input loop menu calling CRUD.
- **Tests** (`tests/`): Pytest for models (`test_models.py`), CRUD (`test_crud.py`), integration (`test_integration.py`).
- **Connection** (`db_connect.py`): Dual psycopg2/SQLAlchemy test.

ERD (text):
```
[Neighbor] (1) --- owns ---> (many) [Tool]
    |                               |
    | borrow                        | used in
(many) <--- (1) [Loan] <--- (many)
    ^
    | (1)
    +--- [Neighbor] (as borrower)
```

## Installation

1. **Clone the Repo**:
   ```
   git clone https://github.com/keithkahurakamau/neighbourhoodToolapp.git
   cd neighbourhoodToolapp
   ```

2. **Setup Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac; venv\Scripts\activate on Windows
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Setup Database**:
   - Install Postgres (e.g., `brew install postgresql` on Mac, `sudo apt install postgresql` on Ubuntu).
   - Create DB: `createdb neighbourhoodToolapp -U postgres` (password: limo91we).
   - Verify: `psql -U postgres -d neighbourhoodToolapp -c "\dt"` (empty tables OK).

## Usage

Run the CLI:
```
python3 cli.py
```

### Example Session
```
Tables ready—welcome to the CLI!

=== Neighborhood Tool Lending Library ===
1. Add Neighbor
2. Add Tool
3. Add Loan
4. List Neighbors
5. List Tools
6. List Overdue Loans
7. List All Loans
8. Return Loan
9. Exit
Choose an option: 1
Name: Alice
Address: 123 Oak St
Email: alice@test.com
Added neighbor: Alice (ID: 1)

Choose an option: 2
Tool name: Cordless Drill
Description (optional): 18V power tool
Owner ID: 1
Added tool: Cordless Drill (ID: 1)

Choose an option: 3
Borrower ID (neighbor): 1
Tool ID: 1
Loan date (YYYY-MM-DD, or Enter for today): 
Due date (YYYY-MM-DD, or Enter for +7 days): 
Added loan: ID 1 (Borrower: 1, Tool: 1)

Choose an option: 7
All Loans:
- ID 1, Borrower: Alice, Tool: Cordless Drill, Loan Date: 2025-10-16, Due: 2025-10-23, Status: Active, Note: N/A

Choose an option: 8
Loan ID to return: 1
Condition note (optional): Good
Returned loan 1: Good

Choose an option: 7
All Loans:
- ID 1, Borrower: Alice, Tool: Cordless Drill, Loan Date: 2025-10-16, Due: 2025-10-23, Status: Returned, Note: Good

Choose an option: 9
Goodbye!
```

### CLI Options
- **1. Add Neighbor**: Prompts name, address, email (unique).
- **2. Add Tool**: Prompts name, description (optional), owner ID.
- **3. Add Loan**: Prompts borrower/tool IDs, dates (defaults today/+7); checks availability.
- **4. List Neighbors**: Shows all with ID/email/address.
- **5. List Tools**: Shows all with ID/desc/owner.
- **6. List Overdue Loans**: Active loans past due date.
- **7. List All Loans**: All with borrower/tool names, status, note (JOIN query).
- **8. Return Loan**: Prompts ID/note → Updates return_date/condition.
- **9. Exit**.

Errors (e.g., dupe email, loaned tool): Printed and re-prompt.

## Architecture

### Data Model
- **Neighbor**: id, name, address, email (unique).
- **Tool**: id, name, description, owner_id (FK to Neighbor).
- **Loan**: id, borrower_id (FK to Neighbor), tool_id (FK to Tool), loan_date, due_date (> loan_date), return_date (nullable), condition_note.
- **Relationships**: Neighbor owns many Tools; Tool has many Loans; Loan links Borrower/Tool.

### Flow
1. CLI menu → User input → CRUD func (`database.py`).
2. CRUD uses SQLAlchemy session → Models (`models.py`).
3. DB: Postgres with constraints (unique email, date check).

### Error Handling
- Validation: Email format, due > loan, availability (no active loan for tool).
- Rollback on IntegrityError (dupes/invalid FKs).

## Testing

Run tests:
```
pytest tests/ -v
```

- **Unit Tests**: `test_models.py` (relationships/constraints), `test_crud.py` (CRUD/error handling)—8 tests.
- **Integration Tests**: `test_integration.py` (full CLI flows with subprocess mocks)—3 tests.
- **Coverage**: `pytest --cov=.` → 90%+ (models/CRUD/CLI).

Example:
```
tests/test_crud.py::test_create_and_read_neighbor PASSED
tests/test_integration.py::test_full_cli_flow PASSED
3 passed in 3.16s
```

## Contributing

1. Fork/clone.
2. Branch: `git checkout -b feature/new-option`.
3. Commit: `git commit -m "feat: add X"`.
4. Push/PR to `develop`.
5. Tests: Run `pytest` before PR.

## License

MIT License—free to use/modify.

## Demo & Contact
- Demo Video: [Link to recording] (add neighbor, loan tool, return, list overdues).
- Author: Keith Kahura Kamau (Moringa Phase 3).
- Questions? Open issue.

---

*Built with love for sustainable communities. Share tools, save the planet! 🌍*