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
    cursor.execute('''SELECT order_id FROM orders WHERE customer_id=? ORDER BY order_id DESC LIMIT 1''', (customer_id,))
    order_id = cursor.fetchone()
    conn.close()
    return order_id[0] if order_id else None

def get_customer_list():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM customers
    ''')
    customer_list = cursor.fetchall()
    conn.close()
    return customer_list

def get_inventory_stock(product_name, category_id):
    pid = get_product_id_by_name(product_name.replace(" ", "_"), category_id)
    print(pid)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT quantity FROM products WHERE product_id=?''', (pid,))
    remaining_inventory = cursor.fetchone()
    conn.close()
    return remaining_inventory[0]

def get_cost(product_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT price FROM products WHERE product_id=?''', (product_id,))
    price = cursor.fetchone()
    conn.close()
    return price 

def add_to_cart(customer_id, product_name, category_id, qty):
    conn = create_connection()
    pid = get_product_id_by_name(product_name.replace(" ", "_"), category_id)
    oid = get_order_id(customer_id)
    price = get_cost(pid)
    subtotal = round(float(price[0]) * float(qty), 2)  

    cursor = conn.cursor()
    #check available quantity 
    cursor.execute('SELECT quantity FROM products WHERE product_id=?', (pid,))
    stock = cursor.fetchone()[0]

    if stock >= int(qty):
        cursor.execute('''INSERT INTO order_item (
                    order_id, product_name, product_id, quantity, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (oid, product_name, pid, qty, subtotal))
        conn.commit()
        print('added to cart: ', subtotal)
        return True
    else:
        print('insufficient quantity, available, error')
    conn.close()

def finalize_cart(customer_id, confirmation_code):
    conn = create_connection()
    cursor = conn.cursor()
    oid = get_order_id(customer_id)
    cursor.execute('''UPDATE orders 
                   SET total_amount=(
                        SELECT SUM(subtotal) FROM order_item WHERE order_id=?
                   ),
                   confirmation_code=? WHERE order_id=?''', (oid, confirmation_code, oid))
    conn.commit()
    conn.close()
    
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
    return pid[0] if pid else None                      

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

def get_order_summary(customer_id):
    oid = get_order_id(customer_id)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM order_item WHERE order_id=?''', (oid,))
    order_summary = cursor.fetchall()
    conn.close()
    return order_summary

def get_total_cost(customer_id):
    oid = get_order_id(customer_id)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(subtotal) FROM order_item WHERE order_id=?''', (oid,))
    total = cursor.fetchone()
    conn.close()
    return total[0] if total else None

def get_product_name(product_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT product_name FROM products WHERE product_id=? 
''', (product_id,))
    product_name = cursor.fetchone()
    conn.close()
    return product_name


