import sqlite3 

conn = sqlite3.connect('customer_orders.db')
conn.execute("PRAGMA foreign_keys=ON;")
print(conn.total_changes)

cursor = conn.cursor()
cursor.execute('''CREATE TABLE customers (
               customer_id INTEGER PRIMARY KEY,
               first_name TEXT,
               last_name TEXT,
               phone_number INTEGER UNIQUE,
               address TEXT,
)''')

cursor.execute('''CREATE TABLE categories (
               category_id INTEGER PRIMARY KEY,
               flavor TEXT,
               stock INTEGER,
)''')

cursor.execute('''CREATE TABLE orders (
               order_id INTEGER PRIMARY KEY,
               customer_id INTEGER,
               category_id INTEGER,
               orderDate DATE,
               qty INTEGER,
               FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
               FOREIGN KEY(category_id) REFERENCES categories(category_id)
)''') 

cursor.execute('''ALTER TABLE orders (
               ADD COLUMN flavor TEXT;
)''')
conn.commit()

conn.close()