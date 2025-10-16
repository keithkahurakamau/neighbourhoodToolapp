from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship  # Fixed import for 2.0+

Base = declarative_base()

class Neighbor(Base):
    __tablename__ = 'neighbors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    # Relationships with string refs (avoids NameError)
    tools = relationship('Tool', backref='owner')  # Auto: tool.owner = neighbor
    loans_as_borrower = relationship('Loan', foreign_keys='Loan.borrower_id', backref='borrower')  # Auto: loan.borrower = neighbor

class Tool(Base):
    __tablename__ = 'tools'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('neighbors.id'), nullable=False)
    
    # Relationship with string ref
    loans = relationship('Loan', backref='tool')  # Auto: loan.tool = this tool

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    borrower_id = Column(Integer, ForeignKey('neighbors.id'), nullable=False)
    tool_id = Column(Integer, ForeignKey('tools.id'), nullable=False)
    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    condition_note = Column(Text)
    
    # Constraint: due_date > loan_date (enforced in Postgres)
    __table_args__ = (CheckConstraint('due_date > loan_date', name='check_due_after_loan'),)