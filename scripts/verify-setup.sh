#!/bin/bash

echo "🔍 AETHER Trading System - Container Health Check"
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
echo -n "1. Python: "
if python --version &>/dev/null; then
    echo -e "${GREEN}✓${NC} $(python --version)"
else
    echo -e "${RED}✗${NC} Python not found"
fi

# Check pip
echo -n "2. Pip: "
if pip --version &>/dev/null; then
    echo -e "${GREEN}✓${NC} $(pip --version)"
else
    echo -e "${RED}✗${NC} Pip not found"
fi

# Check PostgreSQL connection
echo -n "3. PostgreSQL: "
if PGPASSWORD=aether123 psql -h postgres -U aether -d aether_trading -c '\q' 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Connected successfully"
else
    echo -e "${RED}✗${NC} Connection failed"
fi

# Check Redis connection
echo -n "4. Redis: "
if redis-cli -h redis ping &>/dev/null; then
    echo -e "${GREEN}✓${NC} Connected successfully"
else
    echo -e "${RED}✗${NC} Connection failed"
fi

# Check workspace
echo -n "5. Workspace: "
if [ -f "/workspace/README.md" ]; then
    echo -e "${GREEN}✓${NC} Mounted correctly"
else
    echo -e "${RED}✗${NC} Not mounted correctly"
fi

# Check environment variables
echo -n "6. Environment: "
if [ ! -z "$DATABASE_URL" ] && [ ! -z "$REDIS_URL" ]; then
    echo -e "${GREEN}✓${NC} Variables set"
else
    echo -e "${RED}✗${NC} Variables missing"
fi

# Check Python imports
echo -n "7. Python imports: "
if python -c "import sys; sys.path.append('/workspace/src')" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} PYTHONPATH configured"
else
    echo -e "${RED}✗${NC} PYTHONPATH issue"
fi

# Check if main.py exists
echo -n "8. Main application: "
if [ -f "/workspace/src/main.py" ]; then
    echo -e "${GREEN}✓${NC} Found"
else
    echo -e "${RED}✗${NC} Not found"
fi

echo ""
echo "Quick commands to test:"
echo "  - Python REPL: python"
echo "  - Database: psql -h postgres -U aether -d aether_trading"
echo "  - Redis: redis-cli -h redis"
echo "  - Run app: python -m src.main"