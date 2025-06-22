"""
AETHER Trading System - FastAPI Application
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.core.database import get_db, DiscoveredBot, TradingStrategy, TradeSignal, SystemMetrics
import uvicorn
import logging

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AETHER Trading System API",
    description="Autonomous Evolution Trading Hub for Enhanced Returns",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class BotResponse(BaseModel):
    id: str
    address: str
    chain: str
    score: float
    strategy_type: Optional[str]
    performance_metrics: Dict[str, Any]
    is_active: bool
    discovery_time: datetime

class StrategyResponse(BaseModel):
    id: str
    name: str
    version: int
    parameters: Dict[str, Any]
    performance_score: float
    is_active: bool
    created_at: datetime

class SignalResponse(BaseModel):
    id: str
    symbol: str
    action: str
    confidence: float
    price: Optional[float]
    quantity: Optional[float]
    created_at: datetime

class MetricsResponse(BaseModel):
    metric_name: str
    metric_value: float
    metric_data: Dict[str, Any]
    timestamp: datetime

class SystemStatus(BaseModel):
    status: str
    components: Dict[str, bool]
    metrics: Dict[str, Any]
    timestamp: datetime

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AETHER Trading System",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Bot endpoints
@app.get("/api/bots", response_model=List[BotResponse])
async def get_bots(
    chain: Optional[str] = None,
    active_only: bool = True,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get discovered bots"""
    query = db.query(DiscoveredBot)
    
    if chain:
        query = query.filter(DiscoveredBot.chain == chain)
    if active_only:
        query = query.filter(DiscoveredBot.is_active == True)
    
    bots = query.order_by(DiscoveredBot.score.desc()).limit(limit).all()
    
    return [
        BotResponse(
            id=str(bot.id),
            address=bot.address,
            chain=bot.chain,
            score=bot.score,
            strategy_type=bot.strategy_type,
            performance_metrics=bot.performance_metrics or {},
            is_active=bot.is_active,
            discovery_time=bot.discovery_time
        )
        for bot in bots
    ]

@app.get("/api/bots/{bot_id}", response_model=BotResponse)
async def get_bot(bot_id: str, db: Session = Depends(get_db)):
    """Get specific bot details"""
    bot = db.query(DiscoveredBot).filter(DiscoveredBot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    return BotResponse(
        id=str(bot.id),
        address=bot.address,
        chain=bot.chain,
        score=bot.score,
        strategy_type=bot.strategy_type,
        performance_metrics=bot.performance_metrics or {},
        is_active=bot.is_active,
        discovery_time=bot.discovery_time
    )

# Strategy endpoints
@app.get("/api/strategies", response_model=List[StrategyResponse])
async def get_strategies(
    active_only: bool = True,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get trading strategies"""
    query = db.query(TradingStrategy)
    
    if active_only:
        query = query.filter(TradingStrategy.is_active == True)
    
    strategies = query.order_by(TradingStrategy.performance_score.desc()).limit(limit).all()
    
    return [
        StrategyResponse(
            id=str(strategy.id),
            name=strategy.name,
            version=strategy.version,
            parameters=strategy.parameters or {},
            performance_score=strategy.performance_score or 0.0,
            is_active=strategy.is_active,
            created_at=strategy.created_at
        )
        for strategy in strategies
    ]

@app.get("/api/strategies/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(strategy_id: str, db: Session = Depends(get_db)):
    """Get specific strategy details"""
    strategy = db.query(TradingStrategy).filter(TradingStrategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    return StrategyResponse(
        id=str(strategy.id),
        name=strategy.name,
        version=strategy.version,
        parameters=strategy.parameters or {},
        performance_score=strategy.performance_score or 0.0,
        is_active=strategy.is_active,
        created_at=strategy.created_at
    )

# Signal endpoints
@app.get("/api/signals", response_model=List[SignalResponse])
async def get_signals(
    symbol: Optional[str] = None,
    action: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get trade signals"""
    query = db.query(TradeSignal)
    
    if symbol:
        query = query.filter(TradeSignal.symbol == symbol)
    if action:
        query = query.filter(TradeSignal.action == action)
    
    signals = query.order_by(TradeSignal.created_at.desc()).limit(limit).all()
    
    return [
        SignalResponse(
            id=str(signal.id),
            symbol=signal.symbol,
            action=signal.action,
            confidence=signal.confidence or 0.5,
            price=signal.price,
            quantity=signal.quantity,
            created_at=signal.created_at
        )
        for signal in signals
    ]

# Metrics endpoints
@app.get("/api/metrics", response_model=List[MetricsResponse])
async def get_metrics(
    metric_name: Optional[str] = None,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get system metrics"""
    from datetime import timedelta
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(SystemMetrics).filter(SystemMetrics.timestamp >= cutoff_time)
    
    if metric_name:
        query = query.filter(SystemMetrics.metric_name == metric_name)
    
    metrics = query.order_by(SystemMetrics.timestamp.desc()).all()
    
    return [
        MetricsResponse(
            metric_name=metric.metric_name,
            metric_value=metric.metric_value or 0.0,
            metric_data=metric.metric_data or {},
            timestamp=metric.timestamp
        )
        for metric in metrics
    ]

@app.get("/api/status", response_model=SystemStatus)
async def get_system_status(db: Session = Depends(get_db)):
    """Get overall system status"""
    # Get latest health metric
    latest_metric = db.query(SystemMetrics).filter(
        SystemMetrics.metric_name == "system_health"
    ).order_by(SystemMetrics.timestamp.desc()).first()
    
    if latest_metric and latest_metric.metric_data:
        components = latest_metric.metric_data.get('components', {})
        metrics = latest_metric.metric_data.get('metrics', {})
    else:
        components = {}
        metrics = {}
    
    # Determine overall status
    if not components:
        status = "unknown"
    elif all(components.values()):
        status = "operational"
    elif any(components.values()):
        status = "degraded"
    else:
        status = "down"
    
    return SystemStatus(
        status=status,
        components=components,
        metrics=metrics,
        timestamp=datetime.utcnow()
    )

# Statistics endpoint
@app.get("/api/stats")
async def get_statistics(db: Session = Depends(get_db)):
    """Get system statistics"""
    stats = {
        "total_bots": db.query(DiscoveredBot).count(),
        "active_bots": db.query(DiscoveredBot).filter(DiscoveredBot.is_active == True).count(),
        "total_strategies": db.query(TradingStrategy).count(),
        "active_strategies": db.query(TradingStrategy).filter(TradingStrategy.is_active == True).count(),
        "total_signals": db.query(TradeSignal).count(),
        "signals_24h": db.query(TradeSignal).filter(
            TradeSignal.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).count(),
        "top_performing_bot": None,
        "top_strategy": None
    }
    
    # Get top performing bot
    top_bot = db.query(DiscoveredBot).order_by(DiscoveredBot.score.desc()).first()
    if top_bot:
        stats["top_performing_bot"] = {
            "address": top_bot.address,
            "chain": top_bot.chain,
            "score": top_bot.score
        }
    
    # Get top strategy
    top_strategy = db.query(TradingStrategy).order_by(TradingStrategy.performance_score.desc()).first()
    if top_strategy:
        stats["top_strategy"] = {
            "name": top_strategy.name,
            "version": top_strategy.version,
            "score": top_strategy.performance_score
        }
    
    return stats

def run_api():
    """Run the FastAPI application"""
    uvicorn.run(app, host="0.0.0.0", port=8000)