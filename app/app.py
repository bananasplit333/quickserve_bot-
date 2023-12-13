import database 
import sqlite3

def create_connection():
    try: 
        conn = sqlite3.connect('customer_orders.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

# Function to execute a SELECT query and fetch results
def select_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(e)
    return None

def main():
    # Connect to the database
    conn = create_connection()

    if conn is not None:
        # Example SELECT query
        query = "SELECT * FROM products"

        # Execute the SELECT query
        results = select_query(conn, query)

        if results is not None:
            # Process and print the query results
            for row in results:
                print(row)
        else:
            print("Query execution failed.")

        # Close the database connection
        conn.close()
    else:
        print("Database connection failed.")

if __name__ == '__main__':
    main()