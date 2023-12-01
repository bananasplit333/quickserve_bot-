import sqlite3

def create_connection():
    return sqlite3.connect('customer_orders.db')

def insert_customer(customer_id, phone_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO customers (
        customer_id, phone_number)
    VALUES (?, ?)
    ''',(customer_id, phone_number,))
    conn.commit()
    conn.close()

def insert_order(customer_id, category_id, order_date, qty):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO orders (
                   customer_id, category_id, orderDate, qty)
                   VALUES (?,?,?,?)
    ''', (customer_id, category_id, order_date, qty))
    conn.commit()
    conn.close()

def get_customer_by_number(phone_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM customers WHERE phone_number=?''', (phone_number,))
    customer = cursor.fetchone()
    conn.close()
    return customer

def get_customer_id(phone_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT customer_id FROM customers WHERE phone_number=?''', (phone_number,))
    customer_id = cursor.fetchone()
    if customer_id is not None:
        customer_id = customer_id[0]
    else:
        customer_id = None
    conn.close()
    return customer_id

def get_customer_by_id(customer_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE customer_id=?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer

# Define other database operations here
