from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import (
    get_mysql_connection, get_postgres_connection, release_postgres_connection,
    get_redis, add_to_stream, read_stream, get_stream_length,
    create_consumer_group, read_stream_group, acknowledge_message, get_group_info
)

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


@app.get("/api/redis/test")
def redis_test():
    r = get_redis()
    try:
        r.ping()
        r.set("test_key1", "Hello from Redis! Manish", ex=60)
        value = r.get("test_key1")
        return {"status": "connected", "test_value": value}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ==================== Redis Streams Endpoints ====================

@app.post("/api/streams/{stream_name}/add")
def stream_add_message(stream_name: str, data: dict):
    """
    Add a message to a Redis Stream
    Example: POST /api/streams/notifications/add
    Body: {"title": "New Order", "user_id": "123", "amount": "50"}
    """
    try:
        message_id = add_to_stream(f"stream:{stream_name}", data)
        return {
            "status": "success",
            "stream": stream_name,
            "message_id": message_id,
            "data": data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/streams/{stream_name}/read")
def stream_read_messages(stream_name: str, start_id: str = "0", count: int = 10):
    """
    Read messages from a stream
    Query params:
      - start_id: "0" (from beginning), or specific message ID
      - count: number of messages to read (default 10)
    """
    try:
        messages = read_stream(f"stream:{stream_name}", start_id, count)
        formatted_messages = [
            {"id": msg_id, "data": msg_data}
            for msg_id, msg_data in messages
        ]
        return {
            "status": "success",
            "stream": stream_name,
            "total_in_stream": get_stream_length(f"stream:{stream_name}"),
            "messages": formatted_messages
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/streams/{stream_name}/info")
def stream_get_info(stream_name: str):
    """Get info about a stream (total messages, etc.)"""
    try:
        length = get_stream_length(f"stream:{stream_name}")
        return {
            "status": "success",
            "stream": stream_name,
            "total_messages": length
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/streams/{stream_name}/consumer-group/{group_name}/create")
def stream_create_group(stream_name: str, group_name: str, start_from_beginning: bool = False):
    """
    Create a consumer group for a stream

    Consumer groups are useful for:
    - Load balancing messages between workers
    - Tracking which messages each consumer has processed
    - Ensuring each message is processed exactly once
    """
    try:
        start_id = "0" if start_from_beginning else "$"
        result = create_consumer_group(f"stream:{stream_name}", group_name, start_id)
        return {
            "status": "success",
            "stream": stream_name,
            "group": group_name,
            "result": str(result)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/streams/{stream_name}/consumer-group/{group_name}/read")
def stream_read_group(stream_name: str, group_name: str, consumer_name: str, count: int = 1):
    """
    Read messages as part of a consumer group

    Query params:
      - consumer_name: unique identifier for this consumer (e.g., "worker-1")
      - count: number of messages to read
    """
    try:
        messages = read_stream_group(f"stream:{stream_name}", group_name, consumer_name, count)

        if not messages:
            return {
                "status": "success",
                "stream": stream_name,
                "group": group_name,
                "consumer": consumer_name,
                "messages": [],
                "note": "No new messages available"
            }

        formatted_messages = []
        for stream_key, msg_list in messages:
            for msg_id, msg_data in msg_list:
                formatted_messages.append({"id": msg_id, "data": msg_data})

        return {
            "status": "success",
            "stream": stream_name,
            "group": group_name,
            "consumer": consumer_name,
            "messages": formatted_messages,
            "note": "Remember to acknowledge messages after processing!"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/streams/{stream_name}/consumer-group/{group_name}/ack/{message_id}")
def stream_acknowledge_message(stream_name: str, group_name: str, message_id: str):
    """
    Acknowledge a message after successful processing

    This tells Redis the message has been processed and won't be redelivered

    Example: POST /api/streams/notifications/consumer-group/workers/ack/1234-0
    """
    try:
        result = acknowledge_message(f"stream:{stream_name}", group_name, message_id)
        return {
            "status": "success",
            "stream": stream_name,
            "group": group_name,
            "message_id": message_id,
            "acknowledged": result > 0
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/streams/{stream_name}/consumer-group/{group_name}/info")
def stream_get_group_info(stream_name: str, group_name: str):
    """Get info about consumer group (pending messages, consumers, etc.)"""
    try:
        groups_info = get_group_info(f"stream:{stream_name}", group_name)
        return {
            "status": "success",
            "stream": stream_name,
            "groups_info": groups_info
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
