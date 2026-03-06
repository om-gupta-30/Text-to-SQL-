# Text-to-SQL AI

> Convert natural language into any SQL operation and execute it in real-time — SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, REPLACE, PRAGMA, and EXPLAIN.

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Quick Start

```bash
git clone <your-repo-url>
cd "Text to SQL"

cp backend/.env.example backend/.env
# Add your OpenAI API key to backend/.env

make install
make dev
```

Open **http://localhost:5173**

---

## Features

- AI-powered natural language to SQL conversion (GPT-4o-mini)
- **Full SQL support** — SELECT, INSERT, UPDATE, DELETE, CREATE TABLE, DROP TABLE, ALTER TABLE, REPLACE INTO, PRAGMA, EXPLAIN QUERY PLAN
- Multi-table SQLite database with foreign keys (customers, products, orders, order_items)
- Live schema introspection — newly created tables are immediately available to the LLM
- 12 built-in example queries across all operation types
- DML results show rows affected; DDL/PRAGMA show execution status
- Responsive, modern UI with query-type badges and color-coded suggestions
- Automated CI/CD pipeline with security scanning

---

## Project Structure

```
Text to SQL/
├── backend/
│   ├── main.py              # FastAPI app + routes
│   ├── database.py          # DB init, execute_sql, live schema introspection
│   ├── llm.py               # OpenAI integration + prompt
│   ├── models.py            # Pydantic request/response models
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment template
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main UI component
│   │   ├── App.css          # Styles
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Base reset
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .github/workflows/
│   └── ci.yml               # CI/CD pipeline
├── Makefile                  # Dev commands
├── security-check.sh        # Pre-push security scan
├── .gitignore
├── LICENSE
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.13+
- Node.js 18+
- OpenAI API key

### Installation

```bash
make install
```

### Configure Environment

```bash
cp backend/.env.example backend/.env
```

Add your key to `backend/.env`:

```
OPENAI_API_KEY=sk-...
```

### Run

```bash
make dev
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000 |
| API Docs (Swagger) | http://127.0.0.1:8000/docs |

---

## Available Commands

| Command | Description |
|---------|-------------|
| `make dev` | Run backend + frontend together |
| `make install` | Install all dependencies |
| `make backend` | Run backend only |
| `make frontend` | Run frontend only |
| `make stop` | Stop all servers |
| `make clean` | Clean deps, cache, and database |

---

## Supported SQL Operations

| Type | Keywords | Example Prompt |
|------|----------|----------------|
| **SELECT** | `SELECT`, `WITH` | "Show all customers from USA" |
| **INSERT** | `INSERT` | "Add a customer named Jane from London" |
| **UPDATE** | `UPDATE` | "Update all pending orders to processing" |
| **DELETE** | `DELETE` | "Delete all cancelled orders" |
| **REPLACE** | `REPLACE INTO` | "Upsert a product named Webcam HD at $79.99" |
| **CREATE** | `CREATE TABLE` | "Create a notes table with id, content, created_at" |
| **ALTER** | `ALTER TABLE` | "Add a discount_percent column to products" |
| **DROP** | `DROP TABLE` | "Drop the notes table" |
| **PRAGMA** | `PRAGMA` | "Show column info for the orders table" |
| **EXPLAIN** | `EXPLAIN QUERY PLAN` | "Show the query plan for selecting delivered orders" |

---

## Database Schema

The database is auto-created on startup with seed data.

| Table | Rows | Description |
|-------|------|-------------|
| `customers` | 15 | Customer profiles |
| `products` | 15 | Electronics and Office products |
| `orders` | 20 | Orders with status tracking |
| `order_items` | 34 | Line items per order |

```
customers 1───* orders 1───* order_items *───1 products
```

Schema is introspected live — any tables you create via natural language are immediately available.

---

## Deployment

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |

### Backend (Railway / Render / GCP Cloud Run)

1. Push to GitHub
2. Connect repository
3. Set `OPENAI_API_KEY` as an environment variable in the platform's dashboard
4. Deploy

### Frontend (Vercel / Netlify)

1. Push to GitHub
2. Import project, set root directory to `frontend`
3. Build command: `npm run build`, output: `dist`
4. Deploy

---

## Security

- `.env` files are in `.gitignore` — never committed
- Database files (`*.db`, `*.sqlite`) are gitignored
- `__pycache__`, `node_modules`, `dist` are all gitignored
- `security-check.sh` scans for leaked API keys before push
- CI/CD pipeline runs automated security checks on every push
- `.env.example` contains only placeholder values

**Before pushing:**

```bash
./security-check.sh
```

---

## CI/CD Pipeline

Runs on every push and PR to `main` / `develop`:

| Job | What it does |
|-----|--------------|
| Security Check | Scans for `.env`, `.db`, API keys in tracked files |
| Backend Tests | Python syntax, Black formatting, mypy, Bandit security scan |
| Frontend Tests | ESLint, Vite production build |
| Integration Check | Required files present, `.env.example` safety, README exists |

---

## Troubleshooting

**Port already in use:**
```bash
make stop && make dev
```

**Database issues:**
```bash
make clean && make dev
```

**API key not working:**
- Verify `backend/.env` exists and has `OPENAI_API_KEY=sk-...`
- Restart the backend

---

## License

MIT — see [LICENSE](LICENSE)
