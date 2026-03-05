#!/bin/bash

# Local CI/CD Test Script
# Simulates GitHub Actions pipeline locally
# Usage: chmod +x test-ci.sh && ./test-ci.sh

set -e  # Exit on error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Running Local CI/CD Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

FAILED=0

# Job 1: Security Check
echo "🔒 Job 1/4: Security Check"
echo "─────────────────────────────────────"

echo "  Checking for .env files..."
if git ls-files | grep -E "\.env$"; then
    echo "  ❌ FAIL: .env file found in git!"
    FAILED=$((FAILED + 1))
else
    echo "  ✅ PASS"
fi

echo "  Checking for database files..."
if git ls-files | grep -E "\.(db|sqlite|sqlite3)$"; then
    echo "  ❌ FAIL: Database file found in git!"
    FAILED=$((FAILED + 1))
else
    echo "  ✅ PASS"
fi

echo "  Checking for API keys..."
if git grep -E "sk-[a-zA-Z0-9]{20,}" HEAD 2>/dev/null; then
    echo "  ❌ FAIL: API key found in code!"
    FAILED=$((FAILED + 1))
else
    echo "  ✅ PASS"
fi

echo ""

# Job 2: Backend Tests
echo "🐍 Job 2/4: Backend Tests"
echo "─────────────────────────────────────"

echo "  Checking Python syntax..."
cd backend
if python3 -m py_compile main.py database.py llm.py models.py 2>/dev/null; then
    echo "  ✅ PASS: Python syntax valid"
else
    echo "  ❌ FAIL: Python syntax errors"
    FAILED=$((FAILED + 1))
fi
cd ..

echo "  Checking dependencies..."
if [ -f "backend/requirements.txt" ]; then
    echo "  ✅ PASS: requirements.txt exists"
else
    echo "  ❌ FAIL: requirements.txt missing"
    FAILED=$((FAILED + 1))
fi

echo ""

# Job 3: Frontend Tests
echo "⚛️  Job 3/4: Frontend Tests"
echo "─────────────────────────────────────"

echo "  Checking Node.js..."
if command -v node &> /dev/null; then
    echo "  ✅ PASS: Node.js installed ($(node --version))"
else
    echo "  ⚠️  WARN: Node.js not found, skipping frontend tests"
fi

echo "  Building frontend..."
cd frontend
if [ -d "node_modules" ]; then
    if npm run build > /dev/null 2>&1; then
        echo "  ✅ PASS: Frontend build successful"
    else
        echo "  ❌ FAIL: Frontend build failed"
        FAILED=$((FAILED + 1))
    fi
else
    echo "  ⚠️  WARN: node_modules not found, run 'npm install'"
fi
cd ..

echo "  Checking build output..."
if [ -d "frontend/dist" ]; then
    echo "  ✅ PASS: Build directory exists"
else
    echo "  ❌ FAIL: Build directory not found"
    FAILED=$((FAILED + 1))
fi

echo ""

# Job 4: Integration Check
echo "🔗 Job 4/4: Integration Check"
echo "─────────────────────────────────────"

echo "  Checking required files..."
required_files=(
    "README.md"
    "LICENSE"
    ".gitignore"
    "Makefile"
    "backend/main.py"
    "backend/database.py"
    "backend/llm.py"
    "backend/models.py"
    "backend/requirements.txt"
    "backend/.env.example"
    "frontend/package.json"
    "frontend/src/App.jsx"
)

missing=0
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "  ❌ Missing: $file"
        missing=$((missing + 1))
        FAILED=$((FAILED + 1))
    fi
done

if [ $missing -eq 0 ]; then
    echo "  ✅ PASS: All required files present"
fi

echo "  Checking .env.example safety..."
if [ -f "backend/.env.example" ]; then
    if grep -q "sk-" backend/.env.example; then
        echo "  ❌ FAIL: Real API key in .env.example!"
        FAILED=$((FAILED + 1))
    else
        echo "  ✅ PASS: .env.example is safe"
    fi
fi

echo "  Checking documentation..."
if [ -s "README.md" ]; then
    echo "  ✅ PASS: README.md exists"
else
    echo "  ❌ FAIL: README.md missing or empty"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAILED -eq 0 ]; then
    echo "✅ All CI/CD checks passed!"
    echo ""
    echo "Safe to push to GitHub! 🚀"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
else
    echo "❌ $FAILED checks failed!"
    echo ""
    echo "Fix the issues above before pushing."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi
