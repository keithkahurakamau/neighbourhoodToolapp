import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Neighbor, Tool, Loan
from datetime import date, timedelta

# Use your Postgres DB for full constraint enforcement (or keep SQLite for speed)
TEST_DB_URL = "postgresql://postgres:limo91we@localhost:5432/neighbourhoodToolapp"  # From db_connect.py
engine = create_engine(TEST_DB_URL)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def session():
    # Setup: Create tables fresh per test (drops/recreates for isolation)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    # Teardown
    session.close()
    Base.metadata.drop_all(engine)

def test_neighbor_creation(session):
    alice = Neighbor(name='Alice', address='123 Oak St', email='alice@email.com')
    session.add(alice)
    session.commit()
    assert alice.id is not None
    assert alice.name == 'Alice'

def test_tool_relationship(session):
    alice = Neighbor(name='Alice', address='Test St', email='alice@test.com')
    session.add(alice)
    session.commit()

    drill = Tool(name='Cordless Drill', owner_id=alice.id)
    session.add(drill)
    session.commit()

    session.refresh(alice)
    assert len(alice.tools) == 1
    assert alice.tools[0].name == 'Cordless Drill'
    assert drill.owner.name == 'Alice'  # Bidirectional via backref

def test_loan_constraint(session):
    alice = Neighbor(name='Alice', address='Test St', email='alice@test.com')
    session.add(alice)
    session.commit()

    drill = Tool(name='Drill', owner_id=alice.id)
    session.add(drill)
    session.commit()

    # Valid loan
    valid_loan = Loan(borrower_id=alice.id, tool_id=drill.id,
                      loan_date=date.today(), due_date=date.today() + timedelta(days=7))
    session.add(valid_loan)
    session.commit()  # Should succeed

    # Invalid: due before loan (raises in Postgres)
    invalid_loan = Loan(borrower_id=alice.id, tool_id=drill.id,
                        loan_date=date.today(), due_date=date.today() - timedelta(days=1))
    session.add(invalid_loan)
    with pytest.raises(Exception):  # Expect CheckViolation
        session.commit()

def test_full_relationship_chain(session):
    alice = Neighbor(name='Alice', address='Test St', email='alice@test.com')
    session.add(alice)
    session.commit()

    drill = Tool(name='Drill', owner_id=alice.id)
    session.add(drill)
    session.commit()

    loan = Loan(borrower_id=alice.id, tool_id=drill.id,
                loan_date=date.today(), due_date=date.today() + timedelta(days=7))
    session.add(loan)
    session.commit()

    session.refresh(alice)
    session.refresh(drill)
    session.refresh(loan)

    assert len(alice.tools) == 1
    assert drill.owner == alice
    assert loan.borrower == alice
    assert loan.tool == drill
    assert len(drill.loans) == 1