#!/bin/bash

# Security Check Script - Run before pushing to GitHub
# Usage: chmod +x security-check.sh && ./security-check.sh

echo "🔒 Running Security Checks..."
echo ""

FAILED=0

# Check 1: .env file should not be tracked
echo "1. Checking for .env files in git..."
if git ls-files | grep -q "\.env$"; then
    echo "   ❌ FAIL: .env file is tracked by git!"
    echo "   Run: git rm --cached backend/.env"
    FAILED=1
else
    echo "   ✅ PASS: No .env files tracked"
fi

# Check 2: Database files should not be tracked
echo "2. Checking for database files..."
if git ls-files | grep -E "\.(db|sqlite|sqlite3)$"; then
    echo "   ❌ FAIL: Database file is tracked!"
    echo "   Run: git rm --cached backend/*.db"
    FAILED=1
else
    echo "   ✅ PASS: No database files tracked"
fi

# Check 3: node_modules should not be tracked
echo "3. Checking for node_modules..."
if git ls-files | grep -q "node_modules"; then
    echo "   ❌ FAIL: node_modules is tracked!"
    echo "   Run: git rm -r --cached frontend/node_modules"
    FAILED=1
else
    echo "   ✅ PASS: node_modules not tracked"
fi

# Check 4: Python cache should not be tracked
echo "4. Checking for Python cache..."
if git ls-files | grep -q "__pycache__"; then
    echo "   ❌ FAIL: __pycache__ is tracked!"
    echo "   Run: git rm -r --cached backend/__pycache__"
    FAILED=1
else
    echo "   ✅ PASS: No Python cache tracked"
fi

# Check 5: Search for API keys in code
echo "5. Scanning for exposed API keys..."
if git grep -E "sk-[a-zA-Z0-9]{48}" HEAD 2>/dev/null; then
    echo "   ❌ FAIL: Potential OpenAI API key found in code!"
    FAILED=1
else
    echo "   ✅ PASS: No API keys found in tracked files"
fi

# Check 6: Verify .gitignore exists
echo "6. Checking for .gitignore..."
if [ -f .gitignore ]; then
    echo "   ✅ PASS: .gitignore exists"
else
    echo "   ❌ FAIL: .gitignore is missing!"
    FAILED=1
fi

# Check 7: Verify .env.example exists
echo "7. Checking for .env.example..."
if [ -f backend/.env.example ]; then
    echo "   ✅ PASS: .env.example exists"
else
    echo "   ⚠️  WARN: backend/.env.example is missing"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $FAILED -eq 0 ]; then
    echo "✅ All security checks passed!"
    echo "Safe to push to GitHub."
    exit 0
else
    echo "❌ Security checks failed!"
    echo "Fix the issues above before pushing."
    exit 1
fi
