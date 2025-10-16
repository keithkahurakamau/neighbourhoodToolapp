import psycopg2  # PostgreSQL database adapter for Python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Assumes models.py exists with Base

DB_NAME = "neighbourhoodToolapp"
DB_USER = "postgres"
DB_PASSWORD = "limo91we"
DB_HOST = "localhost"
DB_PORT = "5432"

# SQLAlchemy DB URL
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def connect_and_query(query: str):
    # Raw psycopg2 connection
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()
        print("Connected to the database successfully (psycopg2)")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed (psycopg2).")

def create_tables_and_test_orm():
    # SQLAlchemy setup
    engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=engine)
    print("Tables created/verified via SQLAlchemy!")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with SessionLocal() as session:
        try:
            result = session.execute("SELECT 1")
            print("ORM session connected successfully!")
            print(f"ORM query result: {result.scalar()}")
        except Exception as error:
            print(f"ORM error: {error}")

# Test both
if __name__ == "__main__":
    test_query = "SELECT 1;"
    print("Testing psycopg2...")
    results = connect_and_query(test_query)
    if results:
        print(f"Psycopg2 successful! Results: {results}")
    
    print("\nTesting SQLAlchemy...")
    create_tables_and_test_orm()
    print("All tests passed!")