#!/usr/bin/env python3
"""
AETHER Trading System - Debug Script
Comprehensive testing of all system components
"""
import asyncio
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()

async def test_database():
    """Test PostgreSQL database connectivity"""
    try:
        import asyncpg
        conn = await asyncpg.connect(
            'postgresql://aether:aether123@postgres:5432/aether_trading'
        )
        
        # Test basic query
        version = await conn.fetchval('SELECT version()')
        
        # Test table creation
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # Test insert/select
        await conn.execute(
            "INSERT INTO test_table (name) VALUES ($1)", 
            "AETHER Test"
        )
        result = await conn.fetchval(
            "SELECT name FROM test_table WHERE name = $1", 
            "AETHER Test"
        )
        
        # Cleanup
        await conn.execute("DROP TABLE IF EXISTS test_table")
        await conn.close()
        
        return True, f"PostgreSQL {version.split()[1]} - CRUD operations working"
    except Exception as e:
        return False, str(e)

async def test_redis():
    """Test Redis connectivity"""
    try:
        import redis.asyncio as redis
        r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
        
        # Test ping
        await r.ping()
        
        # Test set/get
        await r.set('aether_test', 'Trading System OK')
        value = await r.get('aether_test')
        
        # Test list operations
        await r.lpush('aether_list', 'item1', 'item2')
        list_len = await r.llen('aether_list')
        
        # Cleanup
        await r.delete('aether_test', 'aether_list')
        await r.close()
        
        return True, f"Redis - String and List operations working (value: {value})"
    except Exception as e:
        return False, str(e)

def test_python_packages():
    """Test required Python packages"""
    packages = [
        'fastapi', 'uvicorn', 'pydantic', 'anthropic', 
        'sqlalchemy', 'asyncpg', 'redis', 'pandas', 
        'numpy', 'ccxt', 'web3', 'rich', 'click'
    ]
    
    results = []
    for package in packages:
        try:
            __import__(package)
            results.append((package, True, "✅"))
        except ImportError as e:
            results.append((package, False, f"❌ {e}"))
    
    return results

def test_environment():
    """Test environment variables"""
    env_vars = [
        'DATABASE_URL',
        'REDIS_URL'
    ]
    
    results = []
    for var in env_vars:
        value = os.getenv(var)
        if value:
            results.append((var, True, value))
        else:
            results.append((var, False, "Not set"))
    
    return results

async def test_api_frameworks():
    """Test FastAPI and related frameworks"""
    try:
        from fastapi import FastAPI
        from uvicorn import Config
        
        # Create a simple FastAPI app
        app = FastAPI(title="AETHER Test API")
        
        @app.get("/health")
        async def health():
            return {"status": "healthy", "service": "AETHER"}
        
        # Test if we can create a config (don't actually run the server)
        config = Config(app, host="0.0.0.0", port=8000)
        
        return True, "FastAPI and Uvicorn configuration successful"
    except Exception as e:
        return False, str(e)

async def test_trading_libs():
    """Test trading-specific libraries"""
    try:
        import ccxt
        import pandas as pd
        import numpy as np
        
        # Test CCXT
        exchange = ccxt.binance()
        markets = exchange.load_markets()
        
        # Test pandas/numpy
        df = pd.DataFrame({'price': [100, 101, 99, 102]})
        mean_price = np.mean(df['price'])
        
        return True, f"Trading libs OK - {len(markets)} markets, mean price: {mean_price}"
    except Exception as e:
        return False, str(e)

async def main():
    """Run all debug tests"""
    console.print("[bold blue]🔍 AETHER Trading System Debug Report[/bold blue]")
    console.print("=" * 60)
    
    # Create results table
    table = Table(title="System Component Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="yellow")
    
    with Progress() as progress:
        task = progress.add_task("Running tests...", total=6)
        
        # Test database
        progress.update(task, advance=1, description="Testing database...")
        db_success, db_msg = await test_database()
        table.add_row("PostgreSQL", "✅ PASS" if db_success else "❌ FAIL", db_msg)
        
        # Test Redis
        progress.update(task, advance=1, description="Testing Redis...")
        redis_success, redis_msg = await test_redis()
        table.add_row("Redis", "✅ PASS" if redis_success else "❌ FAIL", redis_msg)
        
        # Test API frameworks
        progress.update(task, advance=1, description="Testing API frameworks...")
        api_success, api_msg = await test_api_frameworks()
        table.add_row("FastAPI", "✅ PASS" if api_success else "❌ FAIL", api_msg)
        
        # Test trading libraries
        progress.update(task, advance=1, description="Testing trading libraries...")
        trading_success, trading_msg = await test_trading_libs()
        table.add_row("Trading Libs", "✅ PASS" if trading_success else "❌ FAIL", trading_msg)
        
        # Test environment
        progress.update(task, advance=1, description="Testing environment...")
        env_results = test_environment()
        for var, success, value in env_results:
            table.add_row(f"ENV: {var}", "✅ SET" if success else "❌ MISSING", value)
        
        # Test Python packages
        progress.update(task, advance=1, description="Testing packages...")
        package_results = test_python_packages()
        failed_packages = [pkg for pkg, success, _ in package_results if not success]
        
        if failed_packages:
            table.add_row("Python Packages", "❌ SOME MISSING", f"Missing: {', '.join(failed_packages)}")
        else:
            table.add_row("Python Packages", "✅ ALL INSTALLED", f"{len(package_results)} packages verified")
    
    console.print(table)
    
    # Summary
    console.print("\n[bold green]🎯 Debug Summary:[/bold green]")
    
    all_tests = [db_success, redis_success, api_success, trading_success]
    passed = sum(all_tests)
    total = len(all_tests)
    
    if passed == total:
        console.print("✅ All core systems operational!")
        console.print("🚀 AETHER Trading System is ready for development")
    else:
        console.print(f"⚠️  {passed}/{total} core systems passing")
        console.print("🔧 Some components need attention")
    
    console.print(f"\n[bold]Next steps:[/bold]")
    console.print("1. Run: [cyan]python -m src.main[/cyan] to start the system")
    console.print("2. Access API at: [cyan]http://localhost:8000[/cyan]")
    console.print("3. Open Jupyter at: [cyan]http://localhost:8888[/cyan]")

if __name__ == "__main__":
    asyncio.run(main())