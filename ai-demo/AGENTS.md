# AI Coding Agent Guidelines

## Architecture Overview

This is a full-stack application with a FastAPI backend and Vue 3 frontend, demonstrating multi-database integration (MySQL, PostgreSQL, Redis) and Redis Streams for message queuing.

### Backend (Python/FastAPI)
- **Entry point**: `main.py` - FastAPI app with CORS middleware and API routes
- **Database layer**: `db.py` - Connection pools for MySQL/PostgreSQL, Redis client, and Redis Streams functions
- **Key patterns**:
  - Connection pooling for MySQL (`mysql_pool`) and PostgreSQL (`postgres_pool`)
  - Redis client with `decode_responses=True` for string responses
  - Stream names prefixed with `"stream:"` (e.g., `"stream:orders"`)
  - Consumer groups for load-balanced message processing
  - All streams trimmed to 1000 messages by default (`maxlen=1000, approximate=True`)

### Frontend (Vue 3)
- **Build tool**: Vite with Vue plugin
- **Structure**: Single-page app with router, store, and i18n
- **Layout**: Collapsible sidebar navigation in `AppLayout.vue`
- **State management**: Vuex for sidebar collapse and theme (light/dark)
- **Internationalization**: Vue i18n with English/French locales
- **Icons**: FontAwesome with selective icon imports

## Critical Workflows

### Development Setup
```bash
# Backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload

# Frontend  
cd vue-app
npm install
npm run dev
```

### Database Configuration
- Environment variables in `.env` (copy from `.env.example`)
- Redis requires AOF persistence (`appendonly yes`) for Streams durability
- Default ports: MySQL 3306, PostgreSQL 5433, Redis 6379

### Production Deployment
```bash
# Backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Frontend
cd vue-app && npm run build  # Outputs to vue-app/dist/
```

## Project Conventions

### API Design
- Base path: `/api/`
- Response format: `{"status": "success|error", "data": ..., "message": "..."}`
- CORS enabled for all origins (development-friendly)
- Stream endpoints use path parameters (e.g., `/api/streams/{name}/add`)

### Redis Streams Usage
- **Add messages**: `add_to_stream("stream:name", data_dict, max_len=1000)`
- **Read history**: `read_stream("stream:name", start_id="0")` 
- **Consumer groups**: Create with `start_from_beginning=False` for new messages only
- **Acknowledgment required**: Always call `acknowledge_message()` after processing
- **Error handling**: Check for `BUSYGROUP` when creating consumer groups

### Frontend Patterns
- **Component structure**: Template + `<script setup>` + scoped styles
- **State access**: `const store = useStore()`, `const { t } = useI18n()`
- **Icon usage**: Import specific icons, add to library in component
- **Theme support**: CSS custom properties with `[data-theme]` attribute
- **Navigation**: Lazy-loaded routes in `router/index.js`

### Code Organization
- Backend functions in `db.py` imported into `main.py`
- Frontend components in `src/components/`, views in `src/views/`
- Locales in `src/locales/` with JSON files
- Store mutations/actions in uppercase (e.g., `TOGGLE_SIDEBAR`)

## Integration Points

### Cross-Component Communication
- Backend: Direct function calls between `main.py` and `db.py`
- Frontend: Vuex store for global state, props/events for component communication
- API calls: Not yet implemented in frontend (pure UI demo currently)

### External Dependencies
- **Databases**: MySQL, PostgreSQL, Redis (all required for full functionality)
- **Python packages**: FastAPI, uvicorn, mysql-connector, psycopg2, redis, python-dotenv
- **Node packages**: Vue 3, Vue Router, Vuex, Vue i18n, Vite, FontAwesome

## Common Patterns & Examples

### Adding to Redis Stream
```python
from db import add_to_stream
message_id = add_to_stream("stream:orders", {
    "order_id": "123",
    "user": "john",
    "total": "99.99"
})
```

### Consumer Group Processing
```python
from db import read_stream_group, acknowledge_message

messages = read_stream_group("stream:orders", "workers", "worker-1", count=5)
for stream_key, msg_list in messages:
    for msg_id, msg_data in msg_list:
        process_order(msg_data)
        acknowledge_message("stream:orders", "workers", msg_id)
```

### Vue Component with i18n & Store
```vue
<script setup>
import { useI18n } from 'vue-i18n'
import { useStore } from 'vuex'

const { t } = useI18n()
const store = useStore()
const isCollapsed = computed(() => store.getters.isSidebarCollapsed)
</script>
```

### FontAwesome Icon Usage
```javascript
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHome } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'

library.add(faHome)
```

## Key Files to Reference

- `main.py`: API routes and FastAPI setup
- `db.py`: Database connections and Redis Streams functions  
- `vue-app/src/App.vue`: Root component using AppLayout
- `vue-app/src/components/AppLayout.vue`: Sidebar navigation and layout
- `vue-app/src/store/index.js`: Vuex store for UI state
- `vue-app/src/router/index.js`: Route definitions
- `vue-app/src/locales/en.json`: Translation keys
- `requirements.txt`: Python dependencies
- `vue-app/package.json`: Node dependencies and scripts</content>
<parameter name="filePath">/Users/msaxena/source/git/manish_saxena_leo_gmail/msaxena1980/python/ai-demo/AGENTS.md
