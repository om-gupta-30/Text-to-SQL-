# Text-to-SQL AI

> Convert natural language questions into SQL queries and execute them in real-time

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![CI/CD](https://github.com/YOUR_USERNAME/text-to-sql-ai/actions/workflows/ci.yml/badge.svg)

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd "Text to SQL"

# Set up environment
cp backend/.env.example backend/.env
# Edit backend/.env and add your OpenAI API key

# Run the application
make dev
```

Open **http://localhost:5173**

---

## ✨ Features

- 🤖 AI-powered natural language to SQL conversion
- 🗄️ Multi-table database with foreign keys (customers, products, orders)
- 💡 12 built-in query suggestions
- 🔒 Secure: Only SELECT queries, SQL injection protection
- ⚡ Real-time query execution and results
- 📱 Responsive, modern UI
- 🔄 Automated CI/CD pipeline

---

## 📁 Project Structure

```
Text to SQL/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── database.py          # Database operations
│   ├── llm.py               # OpenAI integration
│   ├── models.py            # Pydantic models
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Your API keys (ignored by git)
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main UI
│   │   └── App.css          # Styles
│   ├── package.json
│   └── vite.config.js
├── .github/workflows/
│   └── ci.yml               # CI/CD pipeline
├── Makefile                 # Quick commands
├── .gitignore               # Security rules
└── README.md                # This file
```

---

## 🛠️ Setup

### Prerequisites
- Python 3.13+
- Node.js 18+
- OpenAI API key

### Installation

**1. Install Dependencies**
```bash
make install
```

**2. Configure Environment**
```bash
cp backend/.env.example backend/.env
# Add your OpenAI API key to backend/.env
```

**3. Run Application**
```bash
make dev
```

**4. Access**
- Frontend: http://localhost:5173
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

---

## 📝 Available Commands

| Command | Description |
|---------|-------------|
| `make dev` | Run both backend and frontend |
| `make install` | Install all dependencies |
| `make backend` | Run backend only |
| `make frontend` | Run frontend only |
| `make stop` | Stop all servers |
| `make clean` | Clean dependencies and database |

---

## 💡 Example Queries

**Simple Queries:**
- "Show all customers from USA"
- "List all products in Electronics category"

**JOIN Queries:**
- "What are the top 5 best-selling products?"
- "Show customers with more than 2 orders"

**Aggregation:**
- "What is the total revenue from delivered orders?"
- "What is the average order value?"

---

## 🗄️ Database Schema

**Tables:**
- **customers** (15 rows) - Customer information
- **products** (15 rows) - Electronics and Office products
- **orders** (20 rows) - Customer orders with status
- **order_items** (34 rows) - Order line items

**Relationships:**
```
customers → orders → order_items ← products
```

---

## 🚀 Deployment

### Environment Variables

**Required:**
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Deploy Backend (Railway/Render)

1. Push to GitHub
2. Connect repository to Railway or Render
3. Set environment variable: `OPENAI_API_KEY`
4. Deploy automatically

### Deploy Frontend (Vercel)

1. Push to GitHub
2. Import project to Vercel
3. Set root directory: `frontend`
4. Deploy automatically

---

## 🔒 Security

✅ API keys protected (`.env` in `.gitignore`)  
✅ SQL injection prevention  
✅ Only SELECT queries allowed  
✅ No DROP/DELETE/INSERT/UPDATE operations  
✅ Automated security checks in CI/CD

**Before pushing to GitHub:**
```bash
./security-check.sh
```

---

## 🔄 CI/CD Pipeline

Automated checks run on every push:
- 🔒 Security validation
- 🐍 Backend tests
- ⚛️ Frontend build
- 🔗 Integration tests

View results: Actions tab on GitHub

---

## 🐛 Troubleshooting

**Port already in use:**
```bash
make stop
make dev
```

**Database issues:**
```bash
make clean
make dev
```

**API key not working:**
- Check `backend/.env` exists
- Verify `OPENAI_API_KEY` is correct
- Restart backend server

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `./test-ci.sh` to verify
5. Submit a pull request

---

<div align="center">

**Built with FastAPI, React, and OpenAI**

⭐ Star this repo if you find it helpful!

[Report Bug](../../issues) · [Request Feature](../../issues)

</div>
