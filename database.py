from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Neighbor, Tool, Loan
from datetime import date
from sqlalchemy.exc import IntegrityError
DB_URL = 'postgresql://postgres:limo91we@localhost:5432/neighbourhoodToolapp'

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Returns a new session for transactions."""
    return SessionLocal()

# CREATE
def create_neighbor(session, name, address, email):
    try:
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        neighbor = Neighbor(name=name, address=address, email=email)
        session.add(neighbor)
        session.commit()
        session.refresh(neighbor)
        return neighbor
    except IntegrityError:
        session.rollback()
        raise ValueError("Email already exists")
    except ValueError as e:
        session.rollback()
        raise e

def create_tool(session, name, description, owner_id):
    try:
        if not owner_id:
            raise ValueError("Owner ID required")
        tool = Tool(name=name, description=description, owner_id=owner_id)
        session.add(tool)
        session.commit()
        session.refresh(tool)
        return tool
    except IntegrityError:
        session.rollback()
        raise ValueError("Invalid owner ID")
    except ValueError as e:
        session.rollback()
        raise e

def create_loan(session, borrower_id, tool_id, loan_date, due_date):
    try:
        if due_date <= loan_date:
            raise ValueError("Due date must be after loan date")
        loan = Loan(borrower_id=borrower_id, tool_id=tool_id, loan_date=loan_date, due_date=due_date)
        session.add(loan)
        session.commit()
        session.refresh(loan)
        return loan
    except IntegrityError:
        session.rollback()
        raise ValueError("Invalid borrower or tool ID")
    except ValueError as e:
        session.rollback()
        raise e

# READ
def get_neighbor(session, neighbor_id):
    """Get neighbor by ID (with relationships)."""
    return session.query(Neighbor).filter(Neighbor.id == neighbor_id).first()

def get_all_neighbors(session):
    """Get all neighbors."""
    return session.query(Neighbor).all()

def get_all_tools(session):
    """Get all tools."""
    return session.query(Tool).all()

# Advanced READ with JOIN
def get_neighbor_tools(session, neighbor_id):
    """Get neighbor's tools with JOIN."""
    return session.query(Tool).join(Neighbor).filter(Neighbor.id == neighbor_id).all()

def get_overdue_loans(session):
    """Get overdue loans with borrower/tool JOIN."""
    return session.query(Loan).join(Tool).join(Neighbor).filter(
        Loan.due_date < date.today(), Loan.return_date.is_(None)
    ).all()

# UPDATE
def update_loan_return(session, loan_id, return_date, condition_note):
    """Update loan return."""
    loan = session.query(Loan).filter(Loan.id == loan_id).first()
    if loan:
        loan.return_date = return_date
        loan.condition_note = condition_note
        session.commit()
        return loan
    return None

# DELETE
def delete_loan(session, loan_id):
    """Delete a loan."""
    loan = session.query(Loan).filter(Loan.id == loan_id).first()
    if loan:
        session.delete(loan)
        session.commit()
        return True
    return False

# Quick test
if __name__ == "__main__":
    with get_session() as session:
        # Ensure tables exist
        Base.metadata.create_all(engine)
        
        # Clean slate
        session.query(Loan).delete()
        session.query(Tool).delete()
        session.query(Neighbor).delete()
        session.commit()

        # Sample CREATE
        alice = create_neighbor(session, 'Alice', '123 Oak St', 'alice@test.com')
        print(f"Created neighbor: {alice.name} (ID: {alice.id})")
        
        drill = create_tool(session, 'Cordless Drill', '18V tool', alice.id)
        print(f"Created tool: {drill.name} (ID: {drill.id})")
        
        loan = create_loan(session, alice.id, drill.id, date.today(), date.today().replace(day=21))
        print(f"Created loan: ID {loan.id}")
        
        neighbors = get_all_neighbors(session)
        print(f"All neighbors: {len(neighbors)}")
        
        # Advanced UPDATE (use dynamic ID)
        updated = update_loan_return(session, loan.id, date.today(), 'Good condition')
        print(f"Loan updated: {updated.condition_note if updated else 'None'}")
        
        # DELETE (use dynamic ID)
        deleted = delete_loan(session, loan.id)
        print(f"Loan deleted: {'Success' if deleted else 'Failed'}")
        
        # JOIN READ
        tools = get_neighbor_tools(session, alice.id)
        print(f"Neighbor's tools: {len(tools)}")
        
        overdues = get_overdue_loans(session)
        print(f"Overdue loans: {len(overdues)}")
