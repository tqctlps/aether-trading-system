# AETHER Trading System - Usage Guide

## 🚀 Starting the System

### In VS Code DevContainer:
```bash
# Run the complete system
python -m src.main

# Or use the startup script
./scripts/start-dev.sh
```

### System Components:
1. **Bot Hunter** - Scans blockchains for trading bots
2. **Claude Analyzer** - Analyzes bot strategies using AI
3. **Evolution Engine** - Evolves strategies using genetic algorithms
4. **Orchestrator** - Coordinates all components
5. **API** - RESTful API for system interaction

## 📊 API Endpoints

Once running, access the API at http://localhost:8000

### Key Endpoints:
- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /api/bots` - List discovered bots
- `GET /api/strategies` - List trading strategies
- `GET /api/signals` - List trade signals
- `GET /api/metrics` - System metrics
- `GET /api/status` - System status
- `GET /api/stats` - Statistics

### Example API Calls:
```bash
# Check system status
curl http://localhost:8000/api/status

# Get discovered bots
curl http://localhost:8000/api/bots

# Get trading strategies
curl http://localhost:8000/api/strategies

# Get statistics
curl http://localhost:8000/api/stats
```

## 🔧 Configuration

### Environment Variables:
- `CLAUDE_API_KEY` - Your Anthropic Claude API key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string

### Web3 Providers:
To use real blockchain scanning, update the RPC endpoints in `src/bot_hunter/scanner.py`:
```python
web3_providers = {
    "ethereum": "https://eth-mainnet.g.alchemy.com/v2/YOUR-API-KEY",
    "bsc": "https://bsc-dataseed.binance.org/",
    "polygon": "https://polygon-rpc.com/"
}
```

## 📈 Monitoring

### View Logs:
The system uses Rich logging for colored output. Watch the terminal for:
- Component status
- Bot discoveries
- Strategy evolution progress
- Trade signals

### Check Database:
```bash
# Inside container
psql -h postgres -U aether -d aether_trading

# Example queries
SELECT COUNT(*) FROM discovered_bots;
SELECT * FROM trading_strategies ORDER BY performance_score DESC;
SELECT * FROM trade_signals ORDER BY created_at DESC LIMIT 10;
```

### Redis Monitoring:
```bash
# Inside container
redis-cli -h redis

# Commands
PING
INFO
PUBSUB CHANNELS
```

## 🧪 Testing

### Run Verification:
```bash
./scripts/verify-setup.sh
```

### Run Debug Script:
```bash
python scripts/debug-system.py
```

## 🛑 Stopping

Press `Ctrl+C` to gracefully shutdown all components.

## ⚠️ Important Notes

1. **Mock Mode**: The system runs in mock mode by default (no real trades)
2. **API Keys**: Add real API keys for production use
3. **Web3 Providers**: Update RPC endpoints for real blockchain scanning
4. **Trading**: Actual trading execution is not implemented (safety feature)

## 🔍 Troubleshooting

### If components fail:
1. Check logs for errors
2. Verify database/Redis connections
3. Ensure API keys are set
4. Run debug script

### Common Issues:
- **401 Unauthorized**: Add valid Web3 RPC endpoints
- **No Claude API key**: System uses mock analysis
- **Connection refused**: Ensure Docker services are running