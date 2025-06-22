"""
AETHER Trading System - Configuration Management
"""
import os
from typing import Dict, List, Optional
from pydantic import BaseSettings, validator
import json
from pathlib import Path

class Settings(BaseSettings):
    """System configuration settings"""
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Database
    database_url: str = "postgresql://aether:aether123@postgres:5432/aether_trading"
    redis_url: str = "redis://redis:6379/0"
    
    # API Keys
    claude_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # Exchange API Keys
    binance_api_key: Optional[str] = None
    binance_api_secret: Optional[str] = None
    coinbase_api_key: Optional[str] = None
    coinbase_api_secret: Optional[str] = None
    kraken_api_key: Optional[str] = None
    kraken_api_secret: Optional[str] = None
    
    # Blockchain RPC Endpoints
    ethereum_rpc: str = "https://eth-mainnet.g.alchemy.com/v2/demo"
    bsc_rpc: str = "https://bsc-dataseed.binance.org/"
    polygon_rpc: str = "https://polygon-rpc.com/"
    arbitrum_rpc: str = "https://arb1.arbitrum.io/rpc"
    optimism_rpc: str = "https://mainnet.optimism.io"
    
    # Trading Configuration
    max_position_size: float = 0.1  # 10% of portfolio
    max_slippage: float = 0.02  # 2%
    min_profit_threshold: float = 0.015  # 1.5%
    stop_loss_percentage: float = 0.05  # 5%
    take_profit_percentage: float = 0.10  # 10%
    
    # Bot Hunter Configuration
    bot_scan_interval: int = 60  # seconds
    bot_score_threshold: float = 0.7  # minimum score to track
    max_bots_to_track: int = 100
    
    # Evolution Engine Configuration
    population_size: int = 50
    mutation_rate: float = 0.1
    generations_per_save: int = 10
    fitness_threshold: float = 0.8
    
    # Risk Management
    max_daily_loss: float = 0.1  # 10% of portfolio
    max_open_positions: int = 5
    position_sizing_method: str = "kelly"  # kelly, fixed, proportional
    
    # Monitoring
    health_check_interval: int = 30  # seconds
    metric_retention_days: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @validator("claude_api_key", "binance_api_key", "coinbase_api_key", pre=True)
    def validate_api_keys(cls, v, field):
        if v and v.startswith("your_"):
            return None  # Treat placeholder values as None
        return v
    
    def get_exchange_configs(self) -> Dict[str, Dict[str, str]]:
        """Get exchange configurations"""
        configs = {}
        
        if self.binance_api_key and self.binance_api_secret:
            configs['binance'] = {
                'apiKey': self.binance_api_key,
                'secret': self.binance_api_secret,
                'enableRateLimit': True,
                'options': {'defaultType': 'spot'}
            }
        
        if self.coinbase_api_key and self.coinbase_api_secret:
            configs['coinbase'] = {
                'apiKey': self.coinbase_api_key,
                'secret': self.coinbase_api_secret,
                'enableRateLimit': True
            }
        
        if self.kraken_api_key and self.kraken_api_secret:
            configs['kraken'] = {
                'apiKey': self.kraken_api_key,
                'secret': self.kraken_api_secret,
                'enableRateLimit': True
            }
        
        return configs
    
    def get_web3_providers(self) -> Dict[str, str]:
        """Get Web3 provider configurations"""
        return {
            'ethereum': self.ethereum_rpc,
            'bsc': self.bsc_rpc,
            'polygon': self.polygon_rpc,
            'arbitrum': self.arbitrum_rpc,
            'optimism': self.optimism_rpc
        }
    
    def get_trading_params(self) -> Dict[str, float]:
        """Get trading parameters"""
        return {
            'max_position_size': self.max_position_size,
            'max_slippage': self.max_slippage,
            'min_profit_threshold': self.min_profit_threshold,
            'stop_loss_percentage': self.stop_loss_percentage,
            'take_profit_percentage': self.take_profit_percentage
        }
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment.lower() == "production"
    
    def has_exchange_keys(self) -> bool:
        """Check if any exchange keys are configured"""
        return bool(self.get_exchange_configs())
    
    def has_ai_keys(self) -> bool:
        """Check if AI API keys are configured"""
        return bool(self.claude_api_key or self.openai_api_key)

# Global settings instance
settings = Settings()

# Configuration file management
class ConfigManager:
    """Manage configuration files and secrets"""
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
    
    def save_strategy_config(self, name: str, config: Dict):
        """Save strategy configuration"""
        filepath = self.config_dir / f"strategy_{name}.json"
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_strategy_config(self, name: str) -> Dict:
        """Load strategy configuration"""
        filepath = self.config_dir / f"strategy_{name}.json"
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
    
    def list_strategies(self) -> List[str]:
        """List available strategy configurations"""
        strategies = []
        for file in self.config_dir.glob("strategy_*.json"):
            name = file.stem.replace("strategy_", "")
            strategies.append(name)
        return strategies

# Export instances
config_manager = ConfigManager()

def get_settings() -> Settings:
    """Get current settings instance"""
    return settings