from database import get_session, create_neighbor, create_tool, create_loan, get_all_neighbors, get_all_tools, get_overdue_loans, update_loan_return, get_all_loans
from models import Base
from sqlalchemy import create_engine
from datetime import date, timedelta

DB_URL = 'postgresql://postgres:limo91we@localhost:5432/neighbourhoodToolapp'
engine = create_engine(DB_URL)

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid number—try again.")

def main_menu():
    # Ensure tables exist
    Base.metadata.create_all(engine)
    print("Tables ready—welcome to the CLI!")
    
    while True:
        print("\n=== Neighborhood Tool Lending Library ===")
        print("1. Add Neighbor")
        print("2. Add Tool")
        print("3. Add Loan")
        print("4. List Neighbors")
        print("5. List Tools")
        print("6. List Overdue Loans")
        print("7. List All Loans")
        print("8. Return Loan")
        print("9. Exit")
        
        choice = input("Choose an option: ").strip()
        
        with get_session() as session:
            if choice == '1':
                name = input("Name: ").strip()
                address = input("Address: ").strip()
                email = input("Email: ").strip()
                try:
                    neighbor = create_neighbor(session, name, address, email)
                    print(f"Added neighbor: {neighbor.name} (ID: {neighbor.id})")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                name = input("Tool name: ").strip()
                description = input("Description (optional): ").strip() or None
                owner_id = get_int_input("Owner ID: ")
                try:
                    tool = create_tool(session, name, description, owner_id)
                    print(f"Added tool: {tool.name} (ID: {tool.id})")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                borrower_id = get_int_input("Borrower ID (neighbor): ")
                tool_id = get_int_input("Tool ID: ")
                loan_date_input = input("Loan date (YYYY-MM-DD, or Enter for today): ").strip() or date.today().isoformat()
                due_date_input = input("Due date (YYYY-MM-DD, or Enter for +7 days): ").strip() or (date.today() + timedelta(days=7)).isoformat()
                try:
                    from datetime import datetime
                    loan_date = datetime.fromisoformat(loan_date_input).date()
                    due_date = datetime.fromisoformat(due_date_input).date()
                    loan = create_loan(session, borrower_id, tool_id, loan_date, due_date)
                    print(f"Added loan: ID {loan.id} (Borrower: {borrower_id}, Tool: {tool_id})")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '4':
                neighbors = get_all_neighbors(session)
                print("\nNeighbors:")
                if not neighbors:
                    print("No neighbors yet!")
                for n in neighbors:
                    print(f"- {n.name} (ID: {n.id}, Email: {n.email}, Address: {n.address})")
            
            elif choice == '5':
                tools = get_all_tools(session)
                print("\nTools:")
                if not tools:
                    print("No tools yet!")
                for t in tools:
                    print(f"- {t.name} (ID: {t.id}, Description: {t.description or 'N/A'}, Owner ID: {t.owner_id})")
            
            elif choice == '6':
                overdues = get_overdue_loans(session)
                print("\nOverdue Loans:")
                if not overdues:
                    print("No overdues!")
                for l in overdues:
                    print(f"- Loan ID: {l.id}, Due: {l.due_date}, Borrower ID: {l.borrower_id}, Tool ID: {l.tool_id}")
            
            elif choice == '7':
                loans = get_all_loans(session)
                print("\nAll Loans:")
                if not loans:
                    print("No loans yet!")
                for l in loans:
                    status = "Returned" if l.return_date else "Active"
                    print(f"- ID {l.id}, Borrower: {l.borrower_name}, Tool: {l.tool_name}, Loan Date: {l.loan_date}, Due: {l.due_date}, Status: {status}, Note: {l.condition_note or 'N/A'}")
            
            elif choice == '8':
                loan_id = get_int_input("Loan ID to return: ")
                note = input("Condition note (optional): ").strip() or "N/A"
                try:
                    updated = update_loan_return(session, loan_id, date.today(), note)
                    if updated:
                        print(f"Returned loan {loan_id}: {updated.condition_note}")
                    else:
                        print("Loan not found!")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '9':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice—try again.")

if __name__ == "__main__":
    main_menu()