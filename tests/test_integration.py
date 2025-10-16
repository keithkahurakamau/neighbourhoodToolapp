import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Neighbor, Tool, Loan
from datetime import date, timedelta

TEST_DB_URL = "postgresql://postgres:limo91we@localhost:5432/neighbourhoodToolapp"
engine = create_engine(TEST_DB_URL)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def test_db():
    # Setup: Create tables
    Base.metadata.create_all(engine)
    yield
    # Teardown: Clean data
    with SessionLocal() as session:
        session.query(Loan).delete()
        session.query(Tool).delete()
        session.query(Neighbor).delete()
        session.commit()
    Base.metadata.drop_all(engine)

def run_cli(inputs):
    """Run CLI with simulated inputs, return output."""
    process = subprocess.Popen(
        ['python3', 'cli.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    stdout, stderr = process.communicate(input='\n'.join(inputs) + '\n')
    return stdout, stderr, process.returncode

def test_full_cli_flow(test_db):
    """Test end-to-end: Add neighbor/tool/loan, list, return, overdues."""
    # Inputs: Add neighbor, add tool, add loan, list loans, return loan, list overdues, exit
    inputs = [
        '1',  # Add Neighbor
        'Bob',  # Name
        '456 Pine St',  # Address
        'bob@test.com',  # Email
        '2',  # Add Tool
        'Hammer',  # Name
        'Wooden handle',  # Description
        '1',  # Owner ID (Bob's ID)
        '3',  # Add Loan
        '1', '1', '', '',  # Today +7
        '7',  # List All Loans
        '8',  # Return Loan
        '1',  # Loan ID
        'Good condition',  # Note
        '6',  # List Overdue
        '9'   # Exit
    ]
    
    stdout, stderr, returncode = run_cli(inputs)
    
    # Assert success (ID-agnostic)
    assert returncode == 0
    assert "Added neighbor: Bob (ID:" in stdout
    assert "Added tool: Hammer (ID:" in stdout
    assert "Added loan: ID " in stdout
    assert "ID " in stdout and "Borrower: Bob" in stdout and "Tool: Hammer" in stdout
    assert "Returned loan " in stdout and "Good condition" in stdout
    assert "No overdues!" in stdout  # After return
    
    # Assert DB state
    with SessionLocal() as session:
        neighbors = session.query(Neighbor).all()
        assert len(neighbors) == 1
        assert neighbors[0].name == 'Bob'
        
        tools = session.query(Tool).all()
        assert len(tools) == 1
        assert tools[0].name == 'Hammer'
        
        loans = session.query(Loan).all()
        assert len(loans) == 1
        assert loans[0].return_date is not None  # Returned
        assert "Good condition" in loans[0].condition_note

def test_availability_check(test_db):
    """Test loan availability error."""
    # Inputs: Add neighbor/tool, add loan, try duplicate loan, exit
    inputs = [
        '1',  # Add Neighbor
        'Alice', '123 Oak St', 'alice@test.com',
        '2',  # Add Tool
        'Drill', '18V', '1',
        '3',  # Add Loan
        '1', '1', '', '',  # Today +7
        '3',  # Try duplicate loan
        '1', '1', '', '',  # Same
        '9'   # Exit
    ]
    
    stdout, stderr, returncode = run_cli(inputs)
    
    assert returncode == 0
    assert "Added loan: ID " in stdout  # ID-agnostic
    assert "Error: Tool is currently loaned out" in stdout  # Availability check

def test_invalid_inputs(test_db):
    """Test validation re-prompts (simulated)."""
    # Inputs: Add tool with bad owner ID, then valid, exit
    inputs = [
        '2',  # Add Tool
        'Bad Tool', 'Desc', 'abc',  # Invalid ID (re-prompts, but simulate once)
        '2',  # Valid ID
        '9'   # Exit
    ]
    
    stdout, stderr, returncode = run_cli(inputs)
    
    assert returncode == 0
    assert "Invalid number—try again." in stdout  # Re-prompt
    assert "Added tool: Bad Tool (ID: 1)" not in stdout  # Didn't add invalid

if __name__ == "__main__":
    pytest.main([__file__, '-v'])