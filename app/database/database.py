import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

# locate .env file & return its contents to establish database connection
load_dotenv(dotenv_path = Path(__file__).parents[2] / "credentials.env")
conn = psycopg2.connect(
    dbname = os.getenv("DBNAME"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT"),
    user = os.getenv("USER"),
    password = os.getenv("PASSWD")
)

# use cursor to execute sql commands
cursor = conn.cursor()

# create tables if they do not exist yet
def create_tables():
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

create_tables()