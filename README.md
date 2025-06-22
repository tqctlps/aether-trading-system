# AETHER Trading System

**A**utonomous **E**volution **T**rading **H**ub for **E**nhanced **R**eturns

A sophisticated AI-powered trading system that discovers profitable trading bots on-chain, analyzes their strategies using Claude AI, and evolves optimal trading parameters through genetic algorithms.

## 🌟 Features

- **🤖 Bot Hunter**: Automatically discovers and analyzes trading bots across multiple blockchains
- **🧠 Claude AI Integration**: Uses Anthropic's Claude for intelligent strategy analysis
- **🧬 Evolution Engine**: Genetic algorithms continuously optimize trading parameters
- **📊 Multi-Exchange Support**: Trade on Binance, Coinbase, Kraken, and more
- **⛓️ Multi-Chain Scanner**: Monitors Ethereum, BSC, Polygon, Arbitrum, and Optimism
- **🛡️ Risk Management**: Built-in position sizing, stop-loss, and portfolio protection
- **📈 Real-time Dashboard**: RESTful API with comprehensive monitoring
- **🔄 Auto-Recovery**: Self-healing system with component health monitoring

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed and running
- VS Code with Remote-Containers extension
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tqctlps/aether-trading-system.git
   cd aether-trading-system
   ```

2. **Open in VS Code DevContainer**
   ```bash
   code .
   ```
   When prompted, click "Reopen in Container"

3. **Configure API Keys**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Start the System**
   ```bash
   python -m src.main
   ```

## 📋 Configuration

### Required API Keys

Add these to your `.env` file:

```env
# AI Services
CLAUDE_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional

# Exchange APIs (at least one required for trading)
BINANCE_API_KEY=your_binance_key
BINANCE_API_SECRET=your_binance_secret
COINBASE_API_KEY=your_coinbase_key
COINBASE_API_SECRET=your_coinbase_secret
KRAKEN_API_KEY=your_kraken_key
KRAKEN_API_SECRET=your_kraken_secret

# Blockchain RPC (optional - defaults provided)
ETHEREUM_RPC=https://eth-mainnet.g.alchemy.com/v2/your-key
BSC_RPC=https://bsc-dataseed.binance.org/
POLYGON_RPC=https://polygon-rpc.com/
```

### Trading Parameters

Adjust in `src/core/config.py` or via environment variables:

- `MAX_POSITION_SIZE`: Maximum position size (default: 10% of portfolio)
- `STOP_LOSS_PERCENTAGE`: Stop loss threshold (default: 5%)
- `TAKE_PROFIT_PERCENTAGE`: Take profit target (default: 10%)
- `MAX_DAILY_LOSS`: Maximum daily loss limit (default: 10%)

## 📊 API Documentation

Once running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `GET /api/bots` - List discovered trading bots
- `GET /api/strategies` - View evolved trading strategies
- `GET /api/signals` - Get trade signals
- `GET /api/status` - System health status
- `GET /api/stats` - Trading statistics

## 🏗️ Architecture

```
AETHER Trading System
├── Bot Hunter          # Discovers on-chain trading bots
├── Claude Analyzer     # AI-powered strategy analysis
├── Evolution Engine    # Genetic algorithm optimization
├── Trading Engine      # Execute trades across exchanges
├── Risk Manager        # Portfolio and position management
├── Orchestrator        # System coordination
└── API Server          # RESTful API & monitoring
```

## 🧪 Development

### Running Tests
```bash
make test
```

### Code Formatting
```bash
make format
```

### Debug Mode
```bash
python scripts/debug-system.py
```

### Verification
```bash
./scripts/verify-setup.sh
```

## 📈 Usage Examples

### Start Trading
```python
# The system automatically:
# 1. Scans blockchains for profitable bots
# 2. Analyzes their strategies with AI
# 3. Evolves optimal parameters
# 4. Generates and executes trade signals
```

### Monitor Performance
```bash
# Check system status
curl http://localhost:8000/api/status

# View statistics
curl http://localhost:8000/api/stats

# Get recent signals
curl http://localhost:8000/api/signals
```

## 🛡️ Safety Features

- **Mock Mode**: Test strategies without real money
- **Position Limits**: Configurable maximum position sizes
- **Stop Loss**: Automatic stop-loss on all positions
- **Daily Loss Limit**: Stops trading after daily loss threshold
- **API Rate Limiting**: Prevents exchange API abuse
- **Error Recovery**: Automatic component restart on failure

## 📚 Documentation

- [Usage Guide](USAGE.md) - Detailed usage instructions
- [API Reference](http://localhost:8000/docs) - Interactive API docs
- [Configuration](src/core/config.py) - All configuration options

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Disclaimer

**IMPORTANT**: This software is for educational purposes. Trading cryptocurrencies carries significant risk. Never trade with money you cannot afford to lose. The developers are not responsible for any financial losses.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude AI
- [CCXT](https://github.com/ccxt/ccxt) for exchange integration
- [Web3.py](https://web3py.readthedocs.io/) for blockchain interaction

---

**Built with ❤️ by the AETHER Team**