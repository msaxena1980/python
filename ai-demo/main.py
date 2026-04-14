from flask import Flask, jsonify
from flask_cors import CORS
from db import get_mysql_connection, get_postgres_connection

app = Flask(__name__)
CORS(app)


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})


@app.route('/api/mysql/test', methods=['GET'])
def mysql_test():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"status": "connected", "database": db_name})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/postgres/test', methods=['GET'])
def postgres_test():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT current_database()")
        db_name = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"status": "connected", "database": db_name})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000, debug=True)
