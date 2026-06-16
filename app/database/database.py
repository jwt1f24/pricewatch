import psycopg2
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
        "CREATE TABLE IF NOT EXISTS products ("
        "product_id SERIAL PRIMARY KEY,"
        "name VARCHAR(255) NOT NULL,"
        "price DECIMAL(10, 2) NOT NULL,"
        "url TEXT NOT NULL,"
        "target_price DECIMAL(10, 2) NOT NULL,"
        "email VARCHAR(255) NOT NULL,"
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
def insert_product(name, price, url, target_price, email, stock):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products(name, price, url, target_price, email, stock) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, price, url, target_price, email, stock)
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
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM products"
    )
    cursor.fetchall()
    cursor.close()
    conn.close()

# fetch all price changes from a specific product
def get_history(product_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT price, date FROM history WHERE product_id = %s",
        (product_id,)
    )
    cursor.fetchall()
    cursor.close()
    conn.close()

create_tables()