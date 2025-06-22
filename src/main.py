#!/usr/bin/env python3
"""AETHER Trading System - Main Entry Point"""
import asyncio
import click
import logging
from rich.console import Console
from rich.logging import RichHandler
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

console = Console()
logger = logging.getLogger(__name__)

async def run_system(mode: str):
    """Run the trading system"""
    console.print("[bold green]🚀 Starting AETHER Trading System[/bold green]")
    console.print(f"Mode: {mode}")
    
    # Import components
    from src.orchestrator.coordinator import run_orchestrator
    from src.api.main import run_api
    from src.core.database import init_db
    
    try:
        # Initialize database
        console.print("Initializing database...")
        init_db()
        console.print("[green]✓ Database initialized[/green]")
        
        # Test connections
        db_url = os.getenv('DATABASE_URL', 'postgresql://aether:aether123@postgres:5432/aether_trading')
        redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
        console.print(f"Database URL: {db_url}")
        console.print(f"Redis URL: {redis_url}")
        
        # Start API in separate thread
        import threading
        api_thread = threading.Thread(target=run_api, daemon=True)
        api_thread.start()
        console.print("[green]✓ API started on http://localhost:8000[/green]")
        
        # Start orchestrator
        console.print("Starting orchestrator...")
        await run_orchestrator()
        
    except KeyboardInterrupt:
        console.print("\n[red]Shutting down...[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logger.exception("System error")
        sys.exit(1)

@click.command()
@click.option('--mode', default='development', help='Run mode')
def main(mode: str):
    """Main entry point"""
    # Set environment variables if not set
    if not os.getenv('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'postgresql://aether:aether123@postgres:5432/aether_trading'
    if not os.getenv('REDIS_URL'):
        os.environ['REDIS_URL'] = 'redis://redis:6379/0'
    
    # Run the system
    asyncio.run(run_system(mode))

if __name__ == "__main__":
    main()