"""
AETHER Orchestrator - System Coordination and Management
"""
import asyncio
import logging
from typing import Dict, List, Any
from datetime import datetime
import redis.asyncio as redis
from src.bot_hunter.scanner import run_bot_hunter
from src.claude_analyzer.analyzer import run_claude_analyzer
from src.evolution_engine.evolver import run_evolution_engine
from src.core.database import SystemMetrics, TradeSignal, get_db, init_db
from sqlalchemy.orm import Session
import json

logger = logging.getLogger(__name__)

class Orchestrator:
    """Coordinates all AETHER system components"""
    
    def __init__(self):
        self.redis_client = None
        self.tasks: Dict[str, asyncio.Task] = {}
        self.running = False
        
    async def initialize(self):
        """Initialize orchestrator and dependencies"""
        # Initialize database
        init_db()
        logger.info("Database initialized")
        
        # Connect to Redis
        self.redis_client = redis.Redis(
            host='redis',
            port=6379,
            decode_responses=True
        )
        await self.redis_client.ping()
        logger.info("Redis connected")
        
        self.running = True
        
    async def start_components(self):
        """Start all system components"""
        components = {
            'bot_hunter': run_bot_hunter,
            'claude_analyzer': run_claude_analyzer,
            'evolution_engine': run_evolution_engine,
            'health_monitor': self.run_health_monitor,
            'signal_processor': self.run_signal_processor
        }
        
        for name, coro in components.items():
            try:
                task = asyncio.create_task(coro())
                self.tasks[name] = task
                logger.info(f"Started {name}")
            except Exception as e:
                logger.error(f"Failed to start {name}: {e}")
        
    async def run_health_monitor(self):
        """Monitor system health and collect metrics"""
        while self.running:
            try:
                # Check component status
                component_status = {}
                for name, task in self.tasks.items():
                    component_status[name] = not task.done()
                
                # Collect system metrics
                metrics = await self.collect_metrics()
                
                # Save to database
                db = next(get_db())
                
                metric = SystemMetrics(
                    metric_name="system_health",
                    metric_value=sum(component_status.values()) / len(component_status),
                    metric_data={
                        "components": component_status,
                        "metrics": metrics,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
                db.add(metric)
                db.commit()
                
                # Publish to Redis
                await self.redis_client.publish(
                    'aether:health',
                    json.dumps({
                        'status': component_status,
                        'metrics': metrics
                    })
                )
                
                # Check for failed components and restart
                for name, task in list(self.tasks.items()):
                    if task.done():
                        logger.warning(f"Component {name} stopped. Restarting...")
                        # Get the original coroutine
                        if name == 'bot_hunter':
                            coro = run_bot_hunter
                        elif name == 'claude_analyzer':
                            coro = run_claude_analyzer
                        elif name == 'evolution_engine':
                            coro = run_evolution_engine
                        elif name == 'health_monitor':
                            coro = self.run_health_monitor
                        elif name == 'signal_processor':
                            coro = self.run_signal_processor
                        else:
                            continue
                        
                        # Restart the task
                        self.tasks[name] = asyncio.create_task(coro())
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                await asyncio.sleep(10)
    
    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect system performance metrics"""
        try:
            db = next(get_db())
            
            # Count records
            from src.core.database import DiscoveredBot, TradingStrategy
            
            bot_count = db.query(DiscoveredBot).count()
            strategy_count = db.query(TradingStrategy).count()
            signal_count = db.query(TradeSignal).count()
            
            # Get Redis info
            redis_info = await self.redis_client.info()
            
            return {
                "discovered_bots": bot_count,
                "strategies": strategy_count,
                "signals": signal_count,
                "redis_memory": redis_info.get('used_memory_human', 'unknown'),
                "redis_clients": redis_info.get('connected_clients', 0)
            }
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {}
    
    async def run_signal_processor(self):
        """Process trading signals from strategies"""
        while self.running:
            try:
                # Subscribe to trading signals
                pubsub = self.redis_client.pubsub()
                await pubsub.subscribe('aether:signals')
                
                async for message in pubsub.listen():
                    if message['type'] == 'message':
                        signal_data = json.loads(message['data'])
                        
                        # Save signal to database
                        db = next(get_db())
                        signal = TradeSignal(
                            strategy_id=signal_data.get('strategy_id'),
                            symbol=signal_data['symbol'],
                            action=signal_data['action'],
                            confidence=signal_data.get('confidence', 0.5),
                            price=signal_data.get('price'),
                            quantity=signal_data.get('quantity'),
                            signal_metadata=signal_data.get('metadata', {})
                        )
                        db.add(signal)
                        db.commit()
                        
                        logger.info(f"Processed signal: {signal_data['action']} {signal_data['symbol']}")
                        
                        # Execute trade (in production, connect to exchange)
                        await self.execute_trade(signal_data)
                        
            except Exception as e:
                logger.error(f"Signal processor error: {e}")
                await asyncio.sleep(5)
    
    async def execute_trade(self, signal: Dict[str, Any]):
        """Execute trade based on signal"""
        # This is where you would connect to exchanges
        # For now, just log the trade
        logger.info(f"Would execute trade: {json.dumps(signal, indent=2)}")
        
        # Publish execution result
        await self.redis_client.publish(
            'aether:executions',
            json.dumps({
                'signal': signal,
                'status': 'simulated',
                'timestamp': datetime.utcnow().isoformat()
            })
        )
    
    async def shutdown(self):
        """Gracefully shutdown all components"""
        logger.info("Shutting down orchestrator...")
        self.running = False
        
        # Cancel all tasks
        for name, task in self.tasks.items():
            task.cancel()
            logger.info(f"Cancelled {name}")
        
        # Wait for tasks to complete
        await asyncio.gather(*self.tasks.values(), return_exceptions=True)
        
        # Close connections
        if self.redis_client:
            await self.redis_client.close()
        
        logger.info("Orchestrator shutdown complete")

async def run_orchestrator():
    """Run the AETHER orchestrator"""
    orchestrator = Orchestrator()
    
    try:
        # Initialize
        await orchestrator.initialize()
        logger.info("AETHER Orchestrator initialized")
        
        # Start all components
        await orchestrator.start_components()
        logger.info("All components started")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Orchestrator error: {e}")
    finally:
        await orchestrator.shutdown()