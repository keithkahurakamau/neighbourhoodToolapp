from database import get_session, create_neighbor, create_tool, get_all_neighbors, get_all_tools, get_overdue_loans
from models import Base  # Add for table creation
from sqlalchemy import create_engine
from datetime import date

DB_URL = 'postgresql://postgres:limo91we@localhost:5432/neighbourhoodToolapp'  # Match database.py
engine = create_engine(DB_URL)

def main_menu():
    # Ensure tables exist at startup
    Base.metadata.create_all(engine)
    print("Tables ready—welcome to the CLI!")
    
    while True:
        print("\n=== Neighborhood Tool Lending Library ===")
        print("1. Add Neighbor")
        print("2. Add Tool")
        print("3. List Neighbors")
        print("4. List Tools")
        print("5. List Overdue Loans")
        print("6. Exit")
        
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
                description = input("Description: ").strip()
                owner_id = input("Owner ID: ").strip()
                try:
                    owner_id = int(owner_id)
                    tool = create_tool(session, name, description, owner_id)
                    print(f"Added tool: {tool.name} (ID: {tool.id})")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                neighbors = get_all_neighbors(session)
                print("\nNeighbors:")
                if not neighbors:
                    print("No neighbors yet!")
                for n in neighbors:
                    print(f"- {n.name} (ID: {n.id}, Email: {n.email}, Address: {n.address})")
            
            elif choice == '4':
                tools = get_all_tools(session)
                print("\nTools:")
                if not tools:
                    print("No tools yet!")
                for t in tools:
                    print(f"- {t.name} (ID: {t.id}, Description: {t.description or 'N/A'}, Owner ID: {t.owner_id})")
            
            elif choice == '5':
                overdues = get_overdue_loans(session)
                print("\nOverdue Loans:")
                if not overdues:
                    print("No overdues!")
                for l in overdues:
                    print(f"- Loan ID: {l.id}, Due: {l.due_date}, Borrower ID: {l.borrower_id}, Tool ID: {l.tool_id}")
            
            elif choice == '6':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice—try again.")

if __name__ == "__main__":
    main_menu()