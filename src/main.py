#!/usr/bin/env python3
"""AETHER Trading System - Main Entry Point"""
import asyncio
import click
from rich.console import Console

console = Console()

@click.command()
@click.option('--mode', default='development', help='Run mode')
async def main(mode: str):
    """Main entry point"""
    console.print("[bold green]🚀 Starting AETHER Trading System[/bold green]")
    console.print(f"Mode: {mode}")
    
    # Keep running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        console.print("\n[red]Shutting down...[/red]")

if __name__ == "__main__":
    asyncio.run(main())
