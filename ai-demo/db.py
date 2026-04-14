import os
import mysql.connector
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DB"),
    )


def get_postgres_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=int(os.getenv("PG_PORT", 5433)),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DB"),
    )
