# AI Demo

A full-stack demo app with a FastAPI backend and Vue 3 frontend, connected to MySQL, PostgreSQL, and Redis — with full Redis Streams support for message queues, consumer groups, and event pipelines.

## Project Structure

```
ai-demo/
├── main.py           # FastAPI app and routes
├── db.py             # MySQL, Postgres & Redis connection pools + Streams
├── requirements.txt  # Python dependencies
├── .env              # Environment variables (DB credentials)
├── .env.example      # Environment variable template
├── .gitignore
├── README.md
└── vue-app/          # Vue 3 frontend (Vite)
    ├── src/
    │   ├── App.vue
    │   ├── main.js
    │   └── components/
    ├── index.html
    └── package.json
```

## Prerequisites

- Python 3.7+
- Node.js 18+
- MySQL running on port 3306
- PostgreSQL running on port 5433
- Redis running on port 6379

---

## Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-demo
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env`:
```env
# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=your-mysql-db

# PostgreSQL
PG_HOST=localhost
PG_PORT=5433
PG_USER=postgres
PG_PASSWORD=your-password
PG_DB=your-postgres-db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

---

## Redis Setup

Redis is used for both caching (key-value) and Streams (message queues).

### macOS (Homebrew)

```bash
brew install redis
brew services start redis   # auto-starts on reboot
```

Other service commands:
```bash
brew services stop redis
brew services restart redis
brew services list
```

Or run manually (foreground):
```bash
redis-server
```

Verify Redis is running:
```bash
redis-cli ping   # expected: PONG
```

### Linux

```bash
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### Windows

Use [WSL](https://learn.microsoft.com/en-us/windows/wsl/) and follow the Linux instructions, or use [Memurai](https://www.memurai.com/).

### RedisInsight (GUI)

Download from [redis.io/redisinsight](https://redis.io/redisinsight) and connect with:

| Field    | Value       |
|----------|-------------|
| Host     | `localhost` |
| Port     | `6379`      |
| Password | *(leave blank if none set)* |

---

## Redis Persistence (Required for Streams)

Without persistence, Redis data is lost on crashes. For Streams, enable AOF:

### macOS
```bash
nano /usr/local/etc/redis.conf
```

### Linux
```bash
sudo nano /etc/redis/redis.conf
```

Set these values:
```
appendonly yes
appendfsync everysec
```

Then restart Redis:
```bash
brew services restart redis        # macOS
sudo systemctl restart redis-server  # Linux
```

### Docker
```bash
docker run -d \
  -p 6379:6379 \
  -v redis-data:/data \
  redis:latest redis-server --appendonly yes
```

Verify:
```bash
redis-cli CONFIG GET appendonly
# Should return: 1) "appendonly"  2) "yes"
```

---

## Frontend Setup

```bash
cd vue-app
npm install
```

---

## Running the App

### Backend — Development
```bash
uvicorn main:app --port 8000 --reload
```

### Backend — Production
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

> Tip: set `--workers` to `(2 × CPU cores) + 1` for optimal performance.

### Frontend — Development
```bash
cd vue-app
npm run dev
```

### Frontend — Production Build
```bash
cd vue-app
npm run build
```

Interactive API docs: `http://localhost:8000/docs`

---

## API Endpoints

### Core

| Method | Endpoint             | Description              |
|--------|----------------------|--------------------------|
| GET    | `/api/hello`         | Health check             |
| GET    | `/api/mysql/test`    | Test MySQL connection    |
| GET    | `/api/postgres/test` | Test Postgres connection |
| GET    | `/api/redis/test`    | Test Redis connection    |

### Redis Streams

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/streams/{name}/add` | Add message to stream |
| GET  | `/api/streams/{name}/read` | Read messages (`?start_id=0&count=10`) |
| GET  | `/api/streams/{name}/info` | Get stream message count |
| POST | `/api/streams/{name}/consumer-group/{group}/create` | Create consumer group (`?start_from_beginning=false`) |
| GET  | `/api/streams/{name}/consumer-group/{group}/read` | Read as consumer (`?consumer_name=worker-1&count=5`) |
| POST | `/api/streams/{name}/consumer-group/{group}/ack/{msg_id}` | Acknowledge message |
| GET  | `/api/streams/{name}/consumer-group/{group}/info` | Get group info |

---

## Redis Streams — How It Works

This section explains exactly what happens under the hood in this implementation — from writing a message to surviving a server crash.

### Message Storage

When you call `POST /api/streams/{name}/add`, the backend calls `XADD` on Redis. Redis appends the message to an ordered log structure stored in memory. Each message gets an auto-generated ID like `1713091200000-0` — a millisecond timestamp plus a sequence number. This means the stream is always ordered by insertion time and IDs are globally unique.

```
stream:orders
├── 1713091200000-0  {"order_id": "1", "total": "50.00"}
├── 1713091200001-0  {"order_id": "2", "total": "99.99"}
└── 1713091200002-0  {"order_id": "3", "total": "12.50"}
```

The `maxlen=1000, approximate=True` in `add_to_stream()` tells Redis to trim the stream to roughly 1000 messages. The `approximate` flag lets Redis trim at a natural internal boundary rather than exactly at 1000, which is significantly faster and good enough for most use cases.

### Reading Messages

`GET /api/streams/{name}/read` calls `XRANGE` — a simple range scan from a given ID forward. There is no state involved. Every caller gets the same messages. This is useful for audit logs, replaying history, or any scenario where multiple systems need to read the same data independently.

### How Consumer Groups Work

Consumer groups solve the problem of distributing messages across multiple workers so each message is processed exactly once.

When you call `create_consumer_group()`, Redis creates a **last-delivered-id pointer** on the stream. When a worker calls `read_stream_group()` with `>` (meaning "give me new messages"), Redis:

1. Advances the pointer to the next undelivered message
2. Delivers that message to the requesting consumer
3. Adds it to that consumer's **Pending Entry List (PEL)** — a record of "delivered but not yet acknowledged"

A second worker calling the same endpoint gets the *next* batch, not the same one. This is how load balancing works — Redis hands out different messages to different consumers automatically.

```
stream:orders  [A] [B] [C] [D] [E]
                ↑
         last-delivered-id

Worker-1 reads → gets [A, B] → PEL: {worker-1: [A, B]}
Worker-2 reads → gets [C, D] → PEL: {worker-1: [A, B], worker-2: [C, D]}

Worker-1 acks A → PEL: {worker-1: [B], worker-2: [C, D]}
Worker-1 acks B → PEL: {worker-2: [C, D]}

Next read by Worker-3 → gets [E]  (A, B, C, D already delivered)
```

If a worker crashes before acknowledging, its messages stay in the PEL. They are not lost and can be reclaimed and redelivered to another worker.

### How Data is Persisted

By default Redis is purely in-memory — a crash or restart loses everything. This is fine for caching but not for streams carrying important messages.

**AOF (Append Only File)** is the recommended persistence mode for streams. With `appendonly yes`, every write command (`XADD`, `XACK`, `XGROUP CREATE`, etc.) is written to a log file on disk as it happens. With `appendfsync everysec`, Redis flushes that file to disk once per second — worst case you lose 1 second of data on a hard crash.

On restart, Redis replays the entire AOF file to rebuild state:

```
Redis starts
    ↓
Reads appendonly.aof from disk
    ↓
Replays every XADD, XACK, XGROUP CREATE...
    ↓
Full stream state restored in memory
    ↓
Ready — streams, consumer groups, pending entries all intact
```

This means even the consumer group state (which messages are pending, which consumers exist, the last-delivered-id pointer) survives a restart.

**RDB snapshots** are an alternative — Redis forks and writes a point-in-time snapshot of all data to `dump.rdb`. Faster to restore than AOF but you can lose more data between snapshots. You can run both together for maximum durability.

### What Lives Where

```
Redis memory (runtime)
├── stream:orders          ← the message log (XADD writes here)
│   ├── 1713091200000-0  {...}
│   └── 1713091200001-0  {...}
├── Consumer group: workers
│   ├── last-delivered-id: 1713091200001-0
│   └── PEL (pending entries per consumer)
│       ├── worker-1: [1713091200000-0]   ← delivered, not yet acked
│       └── worker-2: []                  ← all acked

Disk (persistence)
└── appendonly.aof         ← replay log, rebuilt on every restart
```

### Streams vs Pub/Sub

| Feature | Pub/Sub | Streams |
|---------|---------|---------|
| Persistence | ❌ lost on crash | ✅ survives restart |
| Message history | ❌ no replay | ✅ full history |
| Consumer groups | ❌ | ✅ load balancing |
| Acknowledgment | ❌ | ✅ at-least-once delivery |
| Use case | Real-time fire-and-forget | Job queues, logs, pipelines |

### Message Delivery — Pull vs Blocking Pull vs Push

Redis Streams supports two read modes. The consumer always initiates the call (there is no server-side push to a passive listener), but blocking mode makes it behave like push in practice.

**Pull (current default before this change)**
`XREADGROUP` returns immediately with whatever is available. If nothing is there it returns empty. The consumer must loop and sleep manually.

```python
# Returns immediately — empty if no new messages
messages = read_stream_group("stream:orders", "workers", "worker-1", count=5, block=None)
```

Latency = however long your `sleep()` is between polls.

**Blocking pull (recommended)**
Pass a `block` timeout in milliseconds. The call parks the connection at Redis and returns the instant a new message arrives — or after the timeout, whichever comes first. Zero CPU while waiting.

```python
# Parks at Redis for up to 5s, wakes up immediately when a message arrives
messages = read_stream_group("stream:orders", "workers", "worker-1", count=5, block=5000)
```

Latency = **sub-millisecond** from publish to delivery.

**Comparison**

| Mode | Latency | CPU while idle | Crash recovery | Replay history |
|------|---------|---------------|----------------|----------------|
| Pull (polling) | = sleep interval | Low but wasteful | ✅ via PEL | ✅ |
| **Blocking pull** `block=5000` | **Sub-millisecond** | **~zero** | ✅ via PEL | ✅ |
| Pub/Sub | Sub-millisecond | ~zero | ❌ lost on crash | ❌ |

**Blocking pull is the best choice for almost everything.** You get Pub/Sub-level latency with full durability and replay. The timeout (`5000ms`) is a safety net — if Redis hiccups or the connection drops, the loop restarts cleanly rather than hanging forever.

**One thing to know:** each blocking worker holds one open Redis connection while waiting. With `pool_size=10` in this project, you can run up to 10 concurrent blocking workers comfortably.

**Recommended worker loop** — use `run_consumer_worker()` from `db.py`:

```python
from db import run_consumer_worker, create_consumer_group

# One-time setup
create_consumer_group("stream:orders", "workers", start_id="0")

# Define your handler
def process_order(msg_id: str, data: dict):
    print(f"Order {data['order_id']} from {data['user']} — ${data['total']}")
    # ... do real work ...
    # ACK is called automatically by run_consumer_worker after this returns

# Start the worker (blocks forever, handles reconnects automatically)
run_consumer_worker("stream:orders", "workers", "worker-1", process_order)
```

This worker sits idle at Redis, consuming zero CPU, and processes each message within milliseconds of it being published.

### Three Usage Patterns

**Pattern 1 — Append-only log** (audit trails, analytics):
```
Producer → POST /api/streams/events/add
Consumer → GET  /api/streams/events/read (reads full history, no ack needed)
```

**Pattern 2 — Single worker queue**:
```
Producer → POST /api/streams/jobs/add
Worker   → GET  /api/streams/jobs/read?start_id=0
           → processes, then moves start_id forward manually
```

**Pattern 3 — Load-balanced workers** (consumer groups):
```
Producers → POST /api/streams/tasks/add
                 ↓  consumer group: workers
Worker-1  ←  different messages per worker, tracked by Redis
Worker-2
Worker-3
```

---

## Redis Streams — Quick Start

### 1. Add a message
```bash
curl -X POST http://localhost:8000/api/streams/orders/add \
  -H "Content-Type: application/json" \
  -d '{"order_id": "123", "user": "Manish", "total": "99.99"}'
```

### 2. Read messages
```bash
curl "http://localhost:8000/api/streams/orders/read?start_id=0&count=10"
```

### 3. Create a consumer group
```bash
curl -X POST "http://localhost:8000/api/streams/orders/consumer-group/processors/create"
```

### 4. Worker reads messages
```bash
curl "http://localhost:8000/api/streams/orders/consumer-group/processors/read?consumer_name=worker-1&count=5"
```

### 5. Acknowledge after processing
```bash
curl -X POST "http://localhost:8000/api/streams/orders/consumer-group/processors/ack/MESSAGE_ID"
```

### 6. Check group status
```bash
curl "http://localhost:8000/api/streams/orders/consumer-group/processors/info"
```

---

## Redis Streams — Real-World Examples

### Email Notification System

```bash
# Setup (once)
curl -X POST "http://localhost:8000/api/streams/emails/consumer-group/senders/create"

# Enqueue email
curl -X POST http://localhost:8000/api/streams/emails/add \
  -H "Content-Type: application/json" \
  -d '{"to": "user@example.com", "subject": "Welcome!", "template": "welcome", "user_id": "123"}'
```

Worker (Python):
```python
from db import read_stream_group, acknowledge_message, add_to_stream

def email_worker():
    while True:
        messages = read_stream_group("stream:emails", "senders", "worker-1", count=5)
        if not messages:
            time.sleep(1)
            continue
        for stream_key, msg_list in messages:
            for msg_id, msg_data in msg_list:
                try:
                    send_email(msg_data['to'], msg_data['subject'])
                    acknowledge_message("stream:emails", "senders", msg_id)
                except Exception as e:
                    if int(msg_data.get('retry_count', 0)) < 3:
                        msg_data['retry_count'] = str(int(msg_data.get('retry_count', 0)) + 1)
                        add_to_stream("stream:emails", msg_data)
```

### Order Processing Pipeline

```
New Order → stream:orders → Validate → stream:payments → Charge → stream:shipments → Ship → stream:notifications → Email
```

```bash
# Create groups for each stage
for group in orders payments shipments notifications; do
  curl -X POST "http://localhost:8000/api/streams/$group/consumer-group/processors/create"
done
```

### Activity Audit Trail

```python
# Log every important action (never acknowledge — permanent record)
add_to_stream("stream:audit_trail", {
    "user_id": user_id,
    "action": "user_updated",
    "timestamp": str(datetime.now()),
    "ip": request.client.host
})
```

### Job Queue with Dead Letter

```python
MAX_RETRIES = 3

def process_tasks():
    while True:
        messages = read_stream_group("stream:tasks", "workers", "worker-1", count=10)
        if not messages:
            time.sleep(1)
            continue
        for stream_key, msg_list in messages:
            for msg_id, msg_data in msg_list:
                retries = int(msg_data.get('retries', 0))
                try:
                    perform_task(msg_data)
                    acknowledge_message("stream:tasks", "workers", msg_id)
                except Exception as e:
                    if retries < MAX_RETRIES:
                        msg_data['retries'] = str(retries + 1)
                        add_to_stream("stream:tasks", msg_data)
                    else:
                        msg_data['error'] = str(e)
                        add_to_stream("stream:deadletter", msg_data)
                        acknowledge_message("stream:tasks", "workers", msg_id)
```

### Vue.js Frontend Polling

```javascript
let lastId = '0';

async function pollStream() {
  const res = await fetch(`/api/streams/orders/read?start_id=${lastId}&count=10`);
  const data = await res.json();
  if (data.messages.length > 0) {
    data.messages.forEach(msg => addToUI(msg.data));
    lastId = data.messages[data.messages.length - 1].id;
  }
}

setInterval(pollStream, 5000);
```

---

## Redis Streams — Configuration

### Recommended `redis.conf` for production

```
# Persistence
appendonly yes
appendfsync everysec
appendfilename "appendonly.aof"

# Memory management
maxmemory 2gb
maxmemory-policy allkeys-lru
```

### Stream size management

```python
# Keep only last 1000 messages per stream (set in add_to_stream)
add_to_stream("stream:data", data, max_len=1000)
```

---

## Redis Streams — Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Data lost on restart | Persistence not enabled | Set `appendonly yes` in redis.conf |
| `BUSYGROUP` error | Consumer group already exists | Use a different group name or delete the stream |
| Messages not visible to consumer | Group created with `$` (new-only) | Recreate with `start_from_beginning=true` |
| Pending messages growing | Workers not acknowledging | Always `ack` after successful processing |
| Memory issues | Unbounded stream growth | Set `max_len` in `add_to_stream` |

### Useful Redis CLI commands

```bash
redis-cli

KEYS stream:*                          # List all streams
XINFO STREAM stream:orders             # Stream details
XINFO GROUPS stream:orders             # All consumer groups
XINFO CONSUMERS stream:orders workers  # Consumers in a group
XPENDING stream:orders workers         # Pending messages
```

---

## Common Mistakes

**Not acknowledging messages:**
```python
# Wrong — message stays pending forever
messages = read_stream_group(...)
process(messages)

# Correct
for msg_id, data in messages:
    process(data)
    acknowledge_message(..., msg_id)
```

**Unbounded stream growth:**
```python
# Wrong
add_to_stream("stream:data", data)

# Correct
add_to_stream("stream:data", data, max_len=1000)
```

---

## Production Checklist

- [ ] Redis persistence enabled (`appendonly yes`)
- [ ] Redis restarted after config change
- [ ] Tested `POST /api/streams/test/add`
- [ ] Tested `GET /api/streams/test/read`
- [ ] Tested consumer group create → read → ack flow
- [ ] `max_len` set on all streams
- [ ] Pending message monitoring in place
- [ ] Cache endpoints still working (backward compatible ✅)

---

## Test Page UI (`/test`)

The `/test` page at `http://localhost:5173/test` lets you exercise every API endpoint from the browser without needing curl or Postman.

### DB & Redis connection tests

Click **Test MySQL**, **Test PostgreSQL**, or **Test Redis** — each calls the corresponding `/api/{db}/test` endpoint and shows the connected database name or an error message inline.

### Redis Streams — correct order of operations

The stream inputs default to `stream=orders`, `group=workers`, `consumer=worker-1` and the payload textarea is pre-filled with a sample order JSON. The buttons must be used in the right sequence:

**Step 1 — Add Message**
Click **➕ Add Message**. This creates the `stream:orders` stream in Redis (if it doesn't exist) and appends the message. The returned message ID is automatically copied into the "Message ID to acknowledge" field.

**Step 2 — Create Consumer Group**
Click **👥 Create Consumer Group**. Make sure the **"From beginning"** checkbox is **checked** — this creates the group with `start_id=0` so it can see messages that already exist in the stream. If you leave it unchecked (`$`), the group only sees messages added *after* it was created, and Step 3 will return an empty list.

**Step 3 — Read as Consumer**
Click **📥 Read as Consumer**. The message from Step 1 is now delivered to `worker-1` and moved into its Pending Entry List (PEL). It will not be delivered to any other consumer until it is acknowledged or times out.

**Step 4 — Acknowledge**
Click **✅ Acknowledge**. The message ID field was auto-filled in Step 1. This removes the message from the consumer's Pending Entry List (PEL), marking it as fully processed.

> **Important:** ACK does NOT delete the message from the stream. The raw log is immutable — the message stays there until it is naturally trimmed by `maxlen`. What ACK removes is only the "delivered but unconfirmed" tracking entry for that consumer.

To verify the PEL is cleared, click **📊 Group Info** after acknowledging — you should see `"pending": 0`.

### What "removed" means in each context

| Action | What it removes |
|--------|----------------|
| ✅ ACK | Message from the consumer's PEL only — stream untouched |
| 📖 Read Messages | Nothing — `XRANGE` is a read-only scan of the raw log |
| 📥 Read as Consumer (after ACK) | Returns empty — group has no new undelivered messages |
| `maxlen` trim (automatic) | Oldest messages from the raw stream when it exceeds the limit |
| `XDEL` (Redis CLI only) | Physically deletes a specific message from the stream |

So after acknowledging:
- **📖 Read Messages** still shows the message — it's in the raw log
- **📥 Read as Consumer** returns nothing — the group already processed it
- **📊 Group Info** shows `pending: 0` — PEL is clear
- **ℹ️ Stream Info** still shows `total_messages: 1` — count is of the raw log

### Does Redis delete messages once all consumers ACK?

No. Even when every consumer in every group has acknowledged a message, it stays in the stream. Redis never auto-deletes messages based on ACK status.

The stream is an immutable log, not a queue. Think of it like Kafka — messages accumulate and are only removed by:

1. **`maxlen` trim (automatic)** — when a new message is added and the stream exceeds the limit, the oldest messages are dropped. This is the normal cleanup mechanism.
2. **`XDEL` (manual)** — explicit delete of a specific message ID via Redis CLI.
3. **`DEL stream:orders` (manual)** — deletes the entire stream.

```
stream:orders (raw log) — never touched by ACK
├── 1713091200000-0  {...}  ← still here after all groups ACK it
└── 1713091200001-0  {...}

Consumer Group "workers"   PEL: {}  ← empty after ACK
Consumer Group "auditors"  PEL: {}  ← empty after ACK

Message stays in the stream. Both groups are done with it.
Redis does nothing automatically.
```

This is actually useful — you can add a new consumer group later and replay the full history from `start_id=0`, as long as `maxlen` hasn't trimmed those messages yet.

### `maxlen` in this project

This project sets `maxlen=1000` with `approximate=True` in `add_to_stream()`:

```python
def add_to_stream(stream_name: str, data: dict, max_len: int = 1000) -> str:
    return redis_client.xadd(stream_name, data, maxlen=max_len, approximate=True)
```

- Each stream keeps roughly the **last 1000 messages**
- When the 1001st message is added, Redis starts trimming the oldest ones
- `approximate=True` lets Redis trim at a natural internal boundary rather than exactly at 1000 — this is significantly faster and the small overshoot doesn't matter in practice
- You can override per call: `add_to_stream("stream:orders", data, max_len=5000)`

### Why "Read as Consumer" returns empty even though Stream Info shows messages

This is the most common point of confusion:

- **Stream Info** counts all messages in the raw stream log — it has no concept of consumer groups.
- **Read as Consumer** uses `XREADGROUP` which only delivers messages the group hasn't seen yet.
- If the group was created *after* messages were added and with "From beginning" **unchecked** (the `$` mode), those earlier messages are invisible to the group.

**Fix:** Delete the group in Redis CLI and recreate it with "From beginning" checked:

```bash
redis-cli XGROUP DESTROY stream:orders workers
# Then click "Create Consumer Group" in the UI with "From beginning" ✅ checked
```

### Why `NOGROUP` error appears on "Read as Consumer"

```
NOGROUP No such key 'stream:orders' or consumer group 'workers' in XREADGROUP
```

This means either the stream doesn't exist yet or the consumer group hasn't been created. Always do Step 1 (Add Message) and Step 2 (Create Consumer Group) before attempting Step 3.

---

## License

This project is open source. Feel free to use and modify as needed.
