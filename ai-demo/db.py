import os
from dotenv import load_dotenv
from mysql.connector.pooling import MySQLConnectionPool
from psycopg2 import pool

load_dotenv()

# MySQL connection pool
mysql_pool = MySQLConnectionPool(
    pool_name="mysql_pool",
    pool_size=10,
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DB"),
)

# Postgres connection pool
postgres_pool = pool.ThreadedConnectionPool(
    minconn=2,
    maxconn=10,
    host=os.getenv("PG_HOST", "localhost"),
    port=int(os.getenv("PG_PORT", 5433)),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    dbname=os.getenv("PG_DB"),
)


def get_mysql_connection():
    return mysql_pool.get_connection()


def get_postgres_connection():
    return postgres_pool.getconn()


def release_postgres_connection(conn):
    postgres_pool.putconn(conn)
