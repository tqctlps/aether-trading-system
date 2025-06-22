#!/bin/bash
# Start AETHER Trading System in development mode

echo "🚀 Starting AETHER Trading System..."

# Check if running in devcontainer
if [ -f /.dockerenv ]; then
    echo "✓ Running in Docker container"
else
    echo "⚠️  Not running in Docker container. Use VS Code DevContainer for best results."
fi

# Set environment variables
export PYTHONPATH=/workspace/src:$PYTHONPATH
export DATABASE_URL="postgresql://aether:aether123@postgres:5432/aether_trading"
export REDIS_URL="redis://redis:6379/0"

# Run the system
echo "Starting main application..."
python -m src.main

# Alternative: Run just the API for testing
# echo "Starting API only..."
# cd /workspace && python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload