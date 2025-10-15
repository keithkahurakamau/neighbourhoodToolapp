import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_session, create_neighbor, create_tool, create_loan, get_all_neighbors, get_all_tools, update_loan_return, delete_loan, get_overdue_loans, get_neighbor_tools  # Added get_all_neighbors
from models import Base, Neighbor, Tool, Loan
from datetime import date, timedelta

TEST_DB_URL = "postgresql://postgres:limo91we@localhost:5432/neighbourhoodToolapp"
engine = create_engine(TEST_DB_URL)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def session():
    # Robust setup: Drop all first for isolation (cleans old data)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    # Teardown: Clean data and drop
    try:
        session.query(Loan).delete()
        session.query(Tool).delete()
        session.query(Neighbor).delete()
        session.commit()
    except:
        session.rollback()
    session.close()
    Base.metadata.drop_all(engine)

def test_create_and_read_neighbor(session):
    # Unique email to avoid dupes
    alice = create_neighbor(session, 'Alice', '123 Oak St', 'alice_unique@test.com')
    assert alice.name == 'Alice'
    assert alice.email == 'alice_unique@test.com'
    all_neighbors = get_all_neighbors(session)
    assert len(all_neighbors) == 1

def test_create_tool_and_relationship(session):
    alice = create_neighbor(session, 'Alice', 'Test St', 'alice_tool@test.com')
    drill = create_tool(session, 'Cordless Drill', '18V', alice.id)
    assert drill.name == 'Cordless Drill'
    all_tools = get_all_tools(session)
    assert len(all_tools) == 1
    # Test relationship via JOIN
    tools = get_neighbor_tools(session, alice.id)
    assert len(tools) == 1
    assert tools[0].name == 'Cordless Drill'

def test_update_and_delete_loan(session):
    alice = create_neighbor(session, 'Alice', 'Test St', 'alice_update@test.com')
    drill = create_tool(session, 'Drill', 'Test', alice.id)
    loan = create_loan(session, alice.id, drill.id, date.today(), date.today() + timedelta(days=7))
    
    updated = update_loan_return(session, loan.id, date.today(), 'Good')
    assert updated.condition_note == 'Good'
    assert updated.return_date == date.today()
    
    deleted = delete_loan(session, loan.id)
    assert deleted is True

def test_overdue_loans_query(session):
    alice = create_neighbor(session, 'Alice', 'Test St', 'alice_overdue@test.com')
    drill = create_tool(session, 'Drill', 'Test', alice.id)
    # Valid overdue: Loan started 10 days ago, due 5 days ago (due > loan, but past now)
    overdue_loan = create_loan(session, alice.id, drill.id, 
                               date.today() - timedelta(days=10),  # loan_date past
                               date.today() - timedelta(days=5))   # due_date later than loan, but past
    overdues = get_overdue_loans(session)
    assert len(overdues) == 1
    assert overdues[0].borrower == alice

def test_error_handling(session):
    # Dupe email
    create_neighbor(session, 'Alice', '123 Oak St', 'alice_error@test.com')  # First
    with pytest.raises(ValueError, match="Email already exists"):
        create_neighbor(session, 'Alice2', '456 Pine', 'alice_error@test.com')
    
    # Invalid date in loan
    with pytest.raises(ValueError, match="Due date must be after loan date"):
        create_loan(session, 1, 1, date.today(), date.today() - timedelta(days=1))
    # Invalid owner ID
    with pytest.raises(ValueError, match="Invalid owner ID"):
        create_tool(session, 'Test Tool', 'Desc', 999)  # Non-existent ID
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_session, create_neighbor, create_tool, create_loan, get_all_neighbors, get_all_tools, update_loan_return, delete_loan, get_overdue_loans, get_neighbor_tools  # Added get_all_neighbors
from models import Base, Neighbor, Tool, Loan
from datetime import date, timedelta

TEST_DB_URL = "postgresql://postgres:limo91we@localhost:5432/neighbourhoodToolapp"
engine = create_engine(TEST_DB_URL)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def session():
    # Robust setup: Drop all first for isolation (cleans old data)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    # Teardown: Clean data and drop
    try:
        session.query(Loan).delete()
        session.query(Tool).delete()
        session.query(Neighbor).delete()
        session.commit()
    except:
        session.rollback()
    session.close()
    Base.metadata.drop_all(engine)

def test_create_and_read_neighbor(session):
    # Unique email to avoid dupes
    alice = create_neighbor(session, 'Alice', '123 Oak St', 'alice_unique@test.com')
    assert alice.name == 'Alice'
    assert alice.email == 'alice_unique@test.com'
    all_neighbors = get_all_neighbors(session)
    assert len(all_neighbors) == 1

def test_create_tool_and_relationship(session):
    alice = create_neighbor(session, 'Alice', 'Test St', 'alice_tool@test.com')
    drill = create_tool(session, 'Cordless Drill', '18V', alice.id)
    assert drill.name == 'Cordless Drill'
    all_tools = get_all_tools(session)
    assert len(all_tools) == 1
    # Test relationship via JOIN
    tools = get_neighbor_tools(session, alice.id)
    assert len(tools) == 1
    assert tools[0].name == 'Cordless Drill'

def test_update_and_delete_loan(session):
    alice = create_neighbor(session, 'Alice', 'Test St', 'alice_update@test.com')
    drill = create_tool(session, 'Drill', 'Test', alice.id)
    loan = create_loan(session, alice.id, drill.id, date.today(), date.today() + timedelta(days=7))
    
    updated = update_loan_return(session, loan.id, date.today(), 'Good')
    assert updated.condition_note == 'Good'
    assert updated.return_date == date.today()
    
    deleted = delete_loan(session, loan.id)
    assert deleted is True

def test_overdue_loans_query(session):
    alice = create_neighbor(session, 'Alice', 'Test St', 'alice_overdue@test.com')
    drill = create_tool(session, 'Drill', 'Test', alice.id)
    # Valid overdue: Loan started 10 days ago, due 5 days ago (due > loan, but past now)
    overdue_loan = create_loan(session, alice.id, drill.id, 
                               date.today() - timedelta(days=10),  # loan_date past
                               date.today() - timedelta(days=5))   # due_date later than loan, but past
    overdues = get_overdue_loans(session)
    assert len(overdues) == 1
    assert overdues[0].borrower == alice

def test_error_handling(session):
    # Dupe email
    create_neighbor(session, 'Alice', '123 Oak St', 'alice_error@test.com')  # First
    with pytest.raises(ValueError, match="Email already exists"):
        create_neighbor(session, 'Alice2', '456 Pine', 'alice_error@test.com')
    
    # Invalid date in loan
    with pytest.raises(ValueError, match="Due date must be after loan date"):
        create_loan(session, 1, 1, date.today(), date.today() - timedelta(days=1))
    
    # Invalid owner ID
    with pytest.raises(ValueError, match="Invalid owner ID"):
        create_tool(session, 'Test Tool', 'Desc', 999)  # Non-existent ID