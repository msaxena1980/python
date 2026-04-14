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


def read_stream_group(stream_name: str, group_name: str, consumer_name: str, count: int = 1, block: int = 5000):
    """
    Read messages as part of a consumer group.
    Each message is tracked and must be acknowledged.

    Uses blocking read by default (block=5000ms) — the call parks at Redis
    and returns the instant a new message arrives, giving sub-millisecond
    delivery latency with zero CPU spin while idle.

    Args:
        stream_name:   Stream name
        group_name:    Consumer group name
        consumer_name: Individual consumer identifier
        count:         Max number of messages to read per call
        block:         Milliseconds to wait for new messages (default 5000).
                       0 = block forever. None = return immediately (pure pull).

    Returns:
        List of (stream_name, [(message_id, data_dict), ...]) tuples,
        or empty list if the block timeout elapsed with no messages.
    """
    return redis_client.xreadgroup(
        group_name, consumer_name,
        {stream_name: ">"},
        count=count,
        block=block
    )


def run_consumer_worker(stream_name: str, group_name: str, consumer_name: str,
                        handler, count: int = 10, block: int = 5000):
    """
    Recommended pattern: blocking consumer worker loop.

    Sits idle at Redis (zero CPU) and wakes up within milliseconds of a new
    message being published. Processes messages in batches, acknowledges each
    one after successful handling, and loops back to wait for the next batch.

    Args:
        stream_name:   Stream name (e.g. "stream:orders")
        group_name:    Consumer group name (e.g. "workers")
        consumer_name: Unique worker ID (e.g. "worker-1")
        handler:       Callable(msg_id: str, msg_data: dict) — your processing logic
        count:         Max messages per batch (default 10)
        block:         Block timeout in ms (default 5000). 0 = wait forever.

    Example:
        def process_order(msg_id, data):
            print(f"Processing order {data['order_id']}")
            # ... do work ...

        run_consumer_worker("stream:orders", "workers", "worker-1", process_order)
    """
    import time
    print(f"[{consumer_name}] Starting — listening on {stream_name} (group: {group_name})")
    while True:
        try:
            messages = read_stream_group(stream_name, group_name, consumer_name,
                                         count=count, block=block)
            if not messages:
                # block timeout elapsed, no messages — loop and wait again
                continue
            for stream_key, msg_list in messages:
                for msg_id, msg_data in msg_list:
                    try:
                        handler(msg_id, msg_data)
                        acknowledge_message(stream_name, group_name, msg_id)
                    except Exception as e:
                        # Leave in PEL — will be reclaimed on next XAUTOCLAIM / restart
                        print(f"[{consumer_name}] Error processing {msg_id}: {e}")
        except Exception as e:
            print(f"[{consumer_name}] Connection error: {e} — retrying in 2s")
            time.sleep(2)


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
