import sqlite3
from datetime import date 

def create_connection():
    return sqlite3.connect('customer_orders.db')

def insert_customer(phone_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO customers 
    (phone_number)
    VALUES (?)
    ''',(phone_number,))
    conn.commit()
    conn.close()

def get_order_id(customer_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT order_id FROM orders WHERE customer_id=?''', (customer_id,))
    order_id = cursor.fetchone()
    conn.close()
    return order_id

def get_customer_list():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM customers
    ''')
    customer_list = cursor.fetchall()
    conn.close()
    return customer_list


def get_cost(product_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT price FROM products WHERE product_id=?''', (int(product_id[0]),))
    price = cursor.fetchone()
    conn.close()
    return price 

def add_to_cart(customer_id, product_name, category_id, qty):
    conn = create_connection()
    pid = get_product_id_by_name(product_name.replace(" ", "_"), category_id)
    print(pid)
    oid = get_order_id(customer_id)
    price = get_cost(pid)
    print(price)
    subtotal = round(float(price[0]) * float(qty), 2)  
    print(subtotal)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO order_item (
                   order_id, product_id, quantity, subtotal)
                   VALUES (?, ?, ?, ?)
                   ''', (oid[0], pid[0], qty, subtotal))
    conn.commit()
    conn.close()

def finalize_cart():
    conn = create_connection()
    cursor = conn.cursor()


def get_product_list(category_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM products WHERE category_id=? AND quantity>0''', (category_id,))
    products = cursor.fetchall()
    conn.close()
    return products

def get_product_id_by_name(product_name, category_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT product_id FROM products WHERE product_name=? AND category_id=?''', (product_name, category_id,))
    pid = cursor.fetchone()
    conn.close()
    return pid                          

def get_customer_id_by_number(phone_number):
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


def start_order(customer_id):
    conn = create_connection()
    print('start order db method')
    curr_date = date.today()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO orders (
                   customer_id, order_date)
                   VALUES (?, ?)
                   ''', (customer_id, curr_date))
    conn.commit()
    conn.close()

