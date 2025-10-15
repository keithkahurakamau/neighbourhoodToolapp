from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Neighbor, Tool, Loan
from datetime import date

DB_URL = 'postgresql://postgres:limo91we@localhost:5432/neighbourhoodToolapp'

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Returns a new session for transactions."""
    return SessionLocal()

# CREATE
def create_neighbor(session, name, address, email):
    """Create a new neighbor."""
    neighbor = Neighbor(name=name, address=address, email=email)
    session.add(neighbor)
    session.commit()
    session.refresh(neighbor)  # Reload for relationships
    return neighbor

def create_tool(session, name, description, owner_id):
    """Create a new tool for an owner."""
    tool = Tool(name=name, description=description, owner_id=owner_id)
    session.add(tool)
    session.commit()
    session.refresh(tool)
    return tool

def create_loan(session, borrower_id, tool_id, loan_date, due_date):
    """Create a new loan."""
    loan = Loan(borrower_id=borrower_id, tool_id=tool_id, loan_date=loan_date, due_date=due_date)
    session.add(loan)
    session.commit()
    session.refresh(loan)
    return loan

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

## Quick test for base CRUD
if __name__ == "__main__":
    with get_session() as session:
        # Ensure tables exist
        Base.metadata.create_all(engine)
        
        # Clean slate
        session.query(Loan).delete()
        session.query(Tool).delete()
        session.query(Neighbor).delete()
        session.commit()

        # Sample CREATE & READ
        alice = create_neighbor(session, 'Alice', '123 Oak St', 'alice@test.com')
        print(f"Created neighbor: {alice.name} (ID: {alice.id})")
        
        drill = create_tool(session, 'Cordless Drill', '18V tool', alice.id)
        print(f"Created tool: {drill.name} (ID: {drill.id})")
        
        loan = create_loan(session, alice.id, drill.id, date.today(), date.today().replace(day=21))
        print(f"Created loan: ID {loan.id}")
        
        neighbors = get_all_neighbors(session)
        print(f"All neighbors: {len(neighbors)}")
        
        tools = get_all_tools(session)
        print(f"All tools: {len(tools)}")