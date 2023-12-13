import sqlite3

conn = sqlite3.connect('customer_orders.db')
conn.execute("PRAGMA foreign_keys=ON;")

cursor = conn.cursor()
cursor.execute('''CREATE TABLE reserved_stock (
                order_id INTEGER PRIMARY KEY NOT NULL,
                product_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                reserved_quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
                )''')

cursor = conn.cursor()
cursor.execute('''CREATE TABLE customers (
               customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT,
               last_name TEXT,
               phone_number INTEGER UNIQUE,
               address TEXT
)''')   

cursor.execute('''CREATE TABLE categories (
               category_id INTEGER PRIMARY KEY AUTOINCREMENT,
               category_name TEXT
)''')

cursor.execute('''CREATE TABLE products (
               product_id INTEGER PRIMARY KEY AUTOINCREMENT,
               product_name TEXT,
               category_id INTEGER,
               price REAL,
               quantity INTEGER,
               FOREIGN KEY (category_id) REFERENCES categories(category_id)
)''') 

cursor.execute('''CREATE TABLE orders (
               order_id INTEGER PRIMARY KEY AUTOINCREMENT,
               customer_id INTEGER,
               order_date DATE,
               total_amount REAL,
               FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)''')

cursor.execute('''CREATE TABLE order_item (
               order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
               order_id INTEGER,
               product_id INTEGER,
               quantity INTEGER,
               subtotal REAL,
               FOREIGN KEY (order_id) REFERENCES orders(order_id),
               FOREIGN KEY (product_id) REFERENCES products(product_id)
)''')

conn.commit()
conn.close()
