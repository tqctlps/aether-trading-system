"""
AETHER Trading System - Database Models and Connection
"""
from sqlalchemy import create_engine, Column, String, Float, DateTime, JSON, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import os

Base = declarative_base()

class DiscoveredBot(Base):
    """Model for discovered trading bots"""
    __tablename__ = 'discovered_bots'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = Column(String, nullable=False)
    chain = Column(String, nullable=False)
    discovery_time = Column(DateTime, default=datetime.utcnow)
    score = Column(Float, nullable=False)
    strategy_type = Column(String)
    performance_metrics = Column(JSON)
    bot_metadata = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TradingStrategy(Base):
    """Model for evolved trading strategies"""
    __tablename__ = 'trading_strategies'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    version = Column(Integer, default=1)
    parent_strategy_id = Column(UUID(as_uuid=True))
    parameters = Column(JSON)
    performance_score = Column(Float)
    backtest_results = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TradeSignal(Base):
    """Model for trade signals"""
    __tablename__ = 'trade_signals'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True))
    symbol = Column(String, nullable=False)
    action = Column(String, nullable=False)  # BUY, SELL, HOLD
    confidence = Column(Float)
    price = Column(Float)
    quantity = Column(Float)
    bot_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemMetrics(Base):
    """Model for system performance metrics"""
    __tablename__ = 'system_metrics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float)
    metric_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database connection setup
def get_database_url():
    return os.getenv('DATABASE_URL', 'postgresql://aether:aether123@postgres:5432/aether_trading')

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()