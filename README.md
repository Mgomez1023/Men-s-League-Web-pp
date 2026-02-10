# Men's League Web MVP

Monorepo with FastAPI backend and React frontend for a local baseball league source-of-truth app.

## Stack
- API: FastAPI + SQLAlchemy 2.0 + Alembic + Postgres
- Auth: Supabase Auth (frontend login) + backend JWT verification + ADMIN_EMAILS allowlist
- Web: Vite + React + TypeScript

## Repository layout
- `apps/api` - backend API and migrations
- `apps/web` - public + admin frontend

## Environment setup
### API (`apps/api/.env`)
Copy `.env.example` to `.env` and set:
- `DATABASE_URL`
- `SUPABASE_JWT_SECRET`
- `ADMIN_EMAILS`
- `CORS_ORIGINS`

### Web (`apps/web/.env`)
Copy `.env.example` to `.env` and set:
- `VITE_API_URL`
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

## Local run commands
### 1) API
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2) Web
```bash
cd apps/web
npm install
npm run dev
```

## Migration commands
```bash
cd apps/api
source .venv/bin/activate
export $(cat .env | xargs)
alembic upgrade head
```

## Seed command (optional)
```bash
cd apps/api
source .venv/bin/activate
python seed.py
```

## Quick sanity checks
```bash
curl http://localhost:8000/health
curl http://localhost:8000/teams
curl http://localhost:8000/schedule
curl http://localhost:8000/standings
curl http://localhost:8000/announcements
```

Admin flow:
1. Open `http://localhost:5173/admin/login`
2. Login with a Supabase email/password user included in `ADMIN_EMAILS`
3. Create game + announcement at `/admin/dashboard`
