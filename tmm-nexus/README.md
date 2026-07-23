# TMM Nexus

Internal operating system for **The Mac Media**.

## Stack

- **Backend:** FastAPI, SQLAlchemy 2, Alembic, PostgreSQL, JWT auth
- **Frontend:** React, Vite, TypeScript, TailwindCSS, TanStack Query, React Router

## Local Development

### 1. Start PostgreSQL

```bash
docker compose up -d
```

### 2. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Default admin credentials (from `.env`):

- Email: `admin@themacmedia.com`
- Password: `changeme`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

## Phase 1 (Complete)

- PostgreSQL schema with Alembic migrations
- JWT authentication with refresh tokens
- Role-based permissions
- Dashboard with lead stats
- Frontend shell with dark sidebar layout

## Phase 2 (Next)

- Google Maps scraper service
- Lead CRUD, search, filters, pagination
- Notes, tags, CSV export
