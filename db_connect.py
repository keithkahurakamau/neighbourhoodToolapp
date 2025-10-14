import psycopg2 # PostgreSQL database adapter for Python

DB_NAME = "neighbourhoodToolapp"
DB_USER = "postgres"
DB_PASSWORD = "limo91we"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_and_query(query: str):
    # Connect to your postgres DB
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
        print("Connected to the database successfully")
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

# Test the connection with a simple query (since DB is empty, use SELECT 1)
if __name__ == "__main__":
    test_query = "SELECT 1;"
    results = connect_and_query(test_query)
    if results:
        print(f"Query successful! Results: {results}")
    else:
        print("No results, but connection worked!")