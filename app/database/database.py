import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
from pathlib import Path

# locate .env file & return its contents to establish database connection
def connect():
    load_dotenv(dotenv_path=Path(__file__).parents[2] / "credentials.env")
    return psycopg2.connect(
        dbname=os.getenv("DBNAME"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWD")
    )

# create tables if they do not exist yet
def create_tables():
    conn = connect()
    cursor = conn.cursor() # cursor function allows sql command execution
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "user_id SERIAL PRIMARY KEY,"
        "email VARCHAR(255) NOT NULL,"
        "password VARCHAR(255) NOT NULL,"
        "date_created TIMESTAMP NOT NULL"
        ");"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS products ("
        "product_id SERIAL PRIMARY KEY,"
        "user_id INT REFERENCES users(user_id),"
        "name VARCHAR(255) NOT NULL,"
        "url TEXT NOT NULL,"
        "current_price DECIMAL(10, 2) NOT NULL,"
        "target_price DECIMAL(10, 2) NOT NULL,"
        "stock INT NOT NULL"
        ");"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS history ("
        "history_id SERIAL PRIMARY KEY,"
        "product_id INT REFERENCES products(product_id),"
        "price DECIMAL(10, 2) NOT NULL,"
        "date TIMESTAMP NOT NULL"
        ");"
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("Tables have been created.")

# insert data into the database
def insert_product(user_id, name, url, current_price, target_price, stock):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products(user_id, name, url, current_price, target_price, stock) VALUES (%s, %s, %s, %s, %s, %s)",
        (user_id, name, url, current_price, target_price, stock)
    )
    conn.commit()
    cursor.close()
    conn.close()

# insert existing data
def update_product(product_id, new_price, current_stock):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET current_price = %s, stock = %s WHERE product_id = %s",
        (new_price, current_stock, product_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

# insert price history of a product into the database
def insert_history(product_id, price, date):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history(product_id, price, date) VALUES (%s, %s, %s)",
        (product_id, price, date)
    )
    conn.commit()
    cursor.close()
    conn.close()

# fetch all products in the database
def get_products():
    conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "SELECT * FROM products"
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# fetch all price changes from a specific product
def get_history(product_id):
    conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "SELECT price, date FROM history WHERE product_id = %s",
        (product_id,)
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

create_tables()