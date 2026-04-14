import os
from dotenv import load_dotenv
from mysql.connector.pooling import MySQLConnectionPool
from psycopg2 import pool
import redis

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

# Redis client (connection pool built-in)
redis_password = os.getenv("REDIS_PASSWORD") or None
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    password=redis_password,
    decode_responses=True,
)


def get_mysql_connection():
    return mysql_pool.get_connection()


def get_postgres_connection():
    return postgres_pool.getconn()


def release_postgres_connection(conn):
    postgres_pool.putconn(conn)


def get_redis():
    return redis_client


# ==================== Redis Streams Functions ====================

def add_to_stream(stream_name: str, data: dict, max_len: int = 1000) -> str:
    """
    Add a message to a Redis Stream

    Args:
        stream_name: Name of the stream (e.g., "stream:notifications")
        data: Dictionary of message data
        max_len: Max messages to keep (older ones trimmed, default 1000)

    Returns:
        Message ID from Redis
    """
    return redis_client.xadd(stream_name, data, maxlen=max_len, approximate=True)


def read_stream(stream_name: str, start_id: str = "0", count: int = 10) -> list:
    """
    Read messages from a stream

    Args:
        stream_name: Name of the stream
        start_id: Message ID to start from ("0" for beginning, "$" for new messages only)
        count: Number of messages to read

    Returns:
        List of (message_id, data_dict) tuples
    """
    messages = redis_client.xrange(stream_name, min=start_id, count=count)
    return messages


def get_stream_length(stream_name: str) -> int:
    """Get total number of messages in a stream"""
    return redis_client.xlen(stream_name)


def delete_stream(stream_name: str) -> int:
    """Delete entire stream"""
    return redis_client.delete(stream_name)


def trim_stream(stream_name: str, max_len: int = 1000) -> int:
    """Trim stream to keep only recent messages"""
    return redis_client.xtrim(stream_name, maxlen=max_len, approximate=True)


# ==================== Redis Consumer Group Functions ====================

def create_consumer_group(stream_name: str, group_name: str, start_id: str = "$") -> str:
    """
    Create a consumer group for the stream
    Useful for load balancing multiple workers

    Args:
        stream_name: Name of the stream
        group_name: Name of consumer group
        start_id: "$" = new messages only, "0" = all messages

    Returns:
        Confirmation message
    """
    try:
        return redis_client.xgroup_create(stream_name, group_name, id=start_id, mkstream=True)
    except redis.ResponseError as e:
        if "BUSYGROUP" in str(e):
            return f"Consumer group '{group_name}' already exists"
        raise


def read_stream_group(stream_name: str, group_name: str, consumer_name: str, count: int = 1):
    """
    Read messages as part of a consumer group
    Each message is tracked and must be acknowledged

    Args:
        stream_name: Stream name
        group_name: Consumer group name
        consumer_name: Individual consumer identifier
        count: Number of messages to read

    Returns:
        List of (stream_name, [(message_id, data_dict), ...]) tuples
    """
    return redis_client.xreadgroup(group_name, consumer_name, {stream_name: ">"}, count=count)


def acknowledge_message(stream_name: str, group_name: str, message_id: str) -> int:
    """
    Acknowledge a message (mark as processed by consumer)

    Args:
        stream_name: Stream name
        group_name: Consumer group name
        message_id: Message ID to acknowledge

    Returns:
        Number of messages acknowledged
    """
    return redis_client.xack(stream_name, group_name, message_id)


def get_group_info(stream_name: str, group_name: str) -> list:
    """Get info about a specific consumer group (pending messages, consumers, etc.)"""
    all_groups = redis_client.xinfo_groups(stream_name)
    return [g for g in all_groups if g.get("name") == group_name]
