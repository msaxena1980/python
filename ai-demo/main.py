from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import get_mysql_connection, get_postgres_connection, release_postgres_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
def hello():
    return {"message": "Hello, World!"}


@app.get("/api/mysql/test")
def mysql_test():
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        cursor.close()
        return {"status": "connected", "database": db_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()  # returns connection back to the pool


@app.get("/api/postgres/test")
def postgres_test():
    conn = get_postgres_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT current_database()")
        db_name = cursor.fetchone()[0]
        cursor.close()
        return {"status": "connected", "database": db_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        release_postgres_connection(conn)  # returns connection back to the pool
