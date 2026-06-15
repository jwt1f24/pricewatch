import psycopg2
import os
from dotenv import load_dotenv

def create_tables():
    conn = psycopg2.connect(
        dbname = os.getenv("DBNAME"),
        host = os.getenv("HOST"),
        port = os.getenv("PORT"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWD")
    )

    conn.close()