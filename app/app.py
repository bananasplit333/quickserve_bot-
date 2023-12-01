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
        query = "SELECT * FROM orders"

        # Execute the SELECT query
        results = select_query(conn, query)

        if results is not None:
            # Process and print the query results
            for row in results:
                print(row)
                if row[2] == 1:
                    print(f"CUSTOMER_ID: {row[1]} ZPODS: {row[-1]} QTY: {row[-2]}")
                elif row[2] == 2:
                    print(f"FG: {row[-1]}")
                elif row[2] == 3:
                    print(f"IVIDA5K: {row[-1]}")
                elif row[2] == 4:
                    print(f"IVIDA7K: {row[-1]}")
                elif row[2] == 5:
                    print(f"RM: {row[-1]}")
                else:
                    print(f"UNKNOWN")
        else:
            print("Query execution failed.")

        # Close the database connection
        conn.close()
    else:
        print("Database connection failed.")

if __name__ == '__main__':
    main()