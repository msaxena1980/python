# AI Demo

A full-stack demo app with a FastAPI backend and Vue 3 frontend, connected to MySQL and PostgreSQL.

## Project Structure

```
ai-demo/
├── main.py           # FastAPI app and routes
├── db.py             # MySQL & Postgres connection pools
├── requirements.txt  # Python dependencies
├── .env              # Environment variables (DB credentials)
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
```

## Frontend Setup

```bash
cd vue-app
npm install
```

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

## API Endpoints

| Method | Endpoint            | Description              |
|--------|---------------------|--------------------------|
| GET    | `/api/hello`        | Health check             |
| GET    | `/api/mysql/test`   | Test MySQL connection    |
| GET    | `/api/postgres/test`| Test Postgres connection |

Interactive API docs available at `http://localhost:8000/docs` when the backend is running.

## License

This project is open source. Feel free to use and modify as needed.
