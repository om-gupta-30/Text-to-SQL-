.PHONY: install dev backend frontend stop clean help

help:
	@echo "Text-to-SQL AI - Available Commands:"
	@echo ""
	@echo "  make install    - Install all dependencies (backend + frontend)"
	@echo "  make dev        - Run both backend and frontend servers"
	@echo "  make backend    - Run backend only"
	@echo "  make frontend   - Run frontend only"
	@echo "  make stop       - Stop all running servers"
	@echo "  make clean      - Clean all dependencies and databases"
	@echo ""

install:
	@echo "Installing backend dependencies..."
	cd backend && pip3 install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ All dependencies installed!"

dev:
	@echo "Starting Text-to-SQL AI..."
	@echo "Backend: http://127.0.0.1:8000"
	@echo "Frontend: http://localhost:5173"
	@echo ""
	@echo "Press Ctrl+C to stop both servers"
	@trap 'kill 0' EXIT; \
	cd backend && python3 -m uvicorn main:app --reload --port 8000 & \
	cd frontend && npm run dev & \
	wait

backend:
	@echo "Starting backend server..."
	@echo "API: http://127.0.0.1:8000"
	@echo "Docs: http://127.0.0.1:8000/docs"
	cd backend && python3 -m uvicorn main:app --reload --port 8000

frontend:
	@echo "Starting frontend server..."
	@echo "UI: http://localhost:5173"
	cd frontend && npm run dev

stop:
	@echo "Stopping all servers..."
	@pkill -f "uvicorn main:app" || true
	@pkill -f "vite" || true
	@echo "✅ All servers stopped"

clean:
	@echo "Cleaning project..."
	rm -rf backend/__pycache__
	rm -rf backend/.pytest_cache
	rm -rf backend/customers.db
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	@echo "✅ Cleaned!"
