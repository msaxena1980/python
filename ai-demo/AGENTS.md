# AI Coding Agent Guidelines

## Architecture Overview

Full-stack application with FastAPI backend and Vue 3 frontend. Integrates MySQL, PostgreSQL, and Redis (with Streams for message queuing).

### Backend (Python/FastAPI)
- **Entry point**: `main.py` - FastAPI app with CORS middleware and API routes
- **Database layer**: `db.py` - Connection pools for MySQL/PostgreSQL, Redis client, and Redis Streams functions
- **Key patterns**:
  - Connection pooling for MySQL (`mysql_pool`) and PostgreSQL (`postgres_pool`)
  - Redis client with `decode_responses=True` for string responses
  - Stream names prefixed with `"stream:"` (e.g., `"stream:orders"`)
  - Consumer groups for load-balanced message processing
  - Blocking consumer worker pattern with sub-millisecond delivery latency

### Frontend (Vue 3)
- **Build tool**: Vite with Vue plugin
- **Structure**: Single-page app with router, store, and i18n
- **Layout**: Collapsible sidebar navigation in `AppLayout.vue`
- **State management**: Vuex (sidebar collapse, theme, feedback panel)
- **Internationalization**: Vue i18n with English/French/Hindi locales
- **Icons**: FontAwesome with selective icon imports

## Development Setup

```bash
# Backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload

# Frontend
cd vue-app && npm install && npm run dev
```

## Project Structure

```
├── main.py              # FastAPI entry point, API routes
├── db.py                # Database connections, Redis Streams functions
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── vue-app/
│   ├── src/
│   │   ├── main.js      # Vue app initialization
│   │   ├── App.vue      # Root component
│   │   ├── components/ # AppLayout, AppHeader, FeedbackPanel, HelloWorld
│   │   ├── views/      # Home, Test, About, Profile, Settings, Subscription,
│   │   │               #   Upload, InstaStudy, GroupStudy, StudyCenter
│   │   ├── router/     # Vue Router with lazy-loaded routes
│   │   ├── store/      # Vuex store (sidebar, theme, feedback)
│   │   └── locales/    # i18n (en.json, fr.json, hi.json)
│   ├── package.json     # Node dependencies
│   └── vite.config.js  # Vite configuration
```

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | API routes (hello, mysql/postgres/redis tests, stream CRUD, consumer groups) |
| `db.py` | MySQL/PostgreSQL/Redis pools, Redis Streams (add, read, group operations) |
| `vue-app/src/components/AppLayout.vue` | Sidebar navigation and main layout |
| `vue-app/src/store/index.js` | Vuex store for UI state |
| `vue-app/src/router/index.js` | Route definitions (11 routes) |
| `vue-app/src/locales/en.json` | English translation keys |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/hello` | Health check |
| GET | `/api/mysql/test` | Test MySQL connection |
| GET | `/api/postgres/test` | Test PostgreSQL connection |
| GET | `/api/redis/test` | Test Redis connection |
| POST | `/api/streams/{stream_name}/add` | Add message to stream |
| GET | `/api/streams/{stream_name}/read` | Read messages from stream |
| GET | `/api/streams/{stream_name}/info` | Get stream info |
| POST | `/api/streams/{stream_name}/consumer-group/{group_name}/create` | Create consumer group |
| GET | `/api/streams/{stream_name}/consumer-group/{group_name}/read` | Read via consumer group |
| POST | `/api/streams/{stream_name}/consumer-group/{group_name}/ack/{message_id}` | Acknowledge message |

## Redis Streams Usage

**Core functions** (from `db.py`):
- `add_to_stream(stream_name, data, max_len=1000)` - Add message, returns message ID
- `read_stream(stream_name, start_id="0", count=10)` - Read messages
- `get_stream_length(stream_name)` - Get message count
- `create_consumer_group(stream_name, group_name, start_id="$")` - Create group
- `read_stream_group(stream_name, group_name, consumer_name, count, block=5000)` - Blocking read
- `acknowledge_message(stream_name, group_name, message_id)` - Ack after processing
- `run_consumer_worker(stream_name, group_name, consumer_name, handler)` - Worker loop

**Consumer worker pattern** (zero CPU while waiting):
```python
def process_order(msg_id, data):
    print(f"Processing {data['order_id']}")

run_consumer_worker("stream:orders", "workers", "worker-1", process_order)
```

## Frontend Patterns

**Component with store & i18n**:
```javascript
const { t } = useI18n()
const store = useStore()
const isCollapsed = computed(() => store.getters.isSidebarCollapsed)
```

**Lazy-loaded route**:
```javascript
{ path: '/home', component: () => import('../views/Home.vue') }
```

**FontAwesome icon usage**:
```javascript
import { faHome } from '@fortawesome/free-solid-svg-icons'
library.add(faHome)
```

## Database Configuration

- Environment variables from `.env` (copy from `.env.example`)
- Default ports: MySQL 3306, PostgreSQL 5433, Redis 6379
- Redis requires AOF persistence for Streams durability
