#!/usr/bin/env python3
"""
AETHER Trading System - Automatic Setup Script for macOS
This script automatically creates the complete DevContainer project
"""

import os
import sys
import subprocess
import platform
import shutil
import time
from pathlib import Path
from datetime import datetime

class AETHERSetup:
    def __init__(self):
        self.project_name = "aether-trading-system"
        self.project_path = Path.cwd()  # Use current working directory
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def print_banner(self):
        """Print welcome banner"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                    AETHER Trading System                      ║
║           Autonomous Evolution Trading Hub Setup              ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
    def check_system(self):
        """Check if running on macOS"""
        if platform.system() != "Darwin":
            print("❌ This script is designed for macOS only!")
            sys.exit(1)
        print("✅ macOS detected")
        
    def check_prerequisites(self):
        """Check and install prerequisites"""
        print("\n🔍 Checking prerequisites...")
        
        # Check for Homebrew
        if not shutil.which("brew"):
            print("❌ Homebrew not found. Installing...")
            install_brew = input("Install Homebrew? (y/n): ")
            if install_brew.lower() == 'y':
                subprocess.run(['/bin/bash', '-c', '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'])
            else:
                print("❌ Homebrew is required. Exiting.")
                sys.exit(1)
        else:
            print("✅ Homebrew found")
            
        # Check for Docker
        if not shutil.which("docker"):
            print("❌ Docker not found. Installing Docker Desktop...")
            subprocess.run(["brew", "install", "--cask", "docker"])
            print("⚠️  Please start Docker Desktop manually and wait for it to be ready")
            input("Press Enter when Docker Desktop is running...")
        else:
            print("✅ Docker found")
            
        # Check if Docker is running
        try:
            subprocess.run(["docker", "info"], capture_output=True, check=True)
            print("✅ Docker is running")
        except:
            print("❌ Docker is not running. Please start Docker Desktop")
            input("Press Enter when Docker Desktop is running...")
            
        # Check for VS Code
        if not shutil.which("code"):
            print("❌ VS Code not found. Installing...")
            subprocess.run(["brew", "install", "--cask", "visual-studio-code"])
        else:
            print("✅ VS Code found")
            
        # Check for Git
        if not shutil.which("git"):
            print("❌ Git not found. Installing...")
            subprocess.run(["brew", "install", "git"])
        else:
            print("✅ Git found")
            
    def create_project_structure(self):
        """Create complete project directory structure"""
        print(f"\n📁 Creating project at: {self.project_path}")
        
        # Skip if setup_aether.py exists (don't overwrite working directory)
        if (self.project_path / "setup_aether.py").exists():
            print("📁 Using current directory for project setup...")
                
        # Create all directories
        directories = [
            ".devcontainer/claude_proxy",
            ".devcontainer/config/grafana/provisioning/datasources",
            ".devcontainer/config/grafana/provisioning/dashboards",
            ".devcontainer/config/grafana/dashboards",
            ".devcontainer/init-scripts/postgres",
            ".devcontainer/init-scripts/timescale",
            "src/core",
            "src/bot_hunter",
            "src/claude_analyzer", 
            "src/evolution_engine",
            "src/agent_factory",
            "src/orchestrator",
            "src/dashboard/api",
            "src/dashboard/static/js",
            "src/dashboard/static/css",
            "src/dashboard/static/img",
            "src/dashboard/templates",
            "src/shared",
            "src/strategies",
            "src/ml_models",
            "scripts",
            "configs",
            "data/raw",
            "data/processed",
            "data/models",
            "data/backtest",
            "logs",
            "models/saved",
            "models/checkpoints",
            "notebooks",
            "tests/unit",
            "tests/integration",
            "tests/e2e",
            "docs",
            "deployment/docker",
            "deployment/k8s",
            "deployment/terraform"
        ]
        
        for dir_path in directories:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)
            
        print("✅ Directory structure created")
        
    def create_file(self, path: str, content: str):
        """Create a file with content"""
        file_path = self.project_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip() + '\n')
            
    def create_all_files(self):
        """Create all project files"""
        print("\n📝 Creating project files...")
        
        # Create .devcontainer/devcontainer.json
        self.create_devcontainer_json()
        
        # Create .devcontainer/docker-compose.yml
        self.create_docker_compose()
        
        # Create Dockerfiles
        self.create_dockerfiles()
        
        # Create configuration files
        self.create_config_files()
        
        # Create Python source files
        self.create_source_files()
        
        # Create scripts
        self.create_scripts()
        
        # Create root files
        self.create_root_files()
        
        # Create empty __init__.py files
        self.create_init_files()
        
        print("✅ All files created")
        
    def create_devcontainer_json(self):
        """Create devcontainer.json"""
        content = '''{
  "name": "AETHER - Claude Meta-AI Trading System",
  "dockerComposeFile": "docker-compose.yml",
  "service": "aether-dev",
  "workspaceFolder": "/workspace/aether",
  
  "customizations": {
    "vscode": {
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.linting.flake8Enabled": true,
        "python.formatting.provider": "black",
        "python.formatting.blackPath": "/usr/local/bin/black",
        "python.sortImports.path": "/usr/local/bin/isort",
        "python.testing.pytestEnabled": true,
        "python.testing.pytestPath": "/usr/local/bin/pytest",
        "python.envFile": "${workspaceFolder}/.env",
        "jupyter.jupyterServerType": "local",
        "jupyter.notebookFileRoot": "${workspaceFolder}/notebooks",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
          "source.organizeImports": true,
          "source.fixAll": true
        },
        "files.associations": {
          "*.env*": "dotenv"
        },
        "terminal.integrated.defaultProfile.linux": "zsh",
        "git.autofetch": true,
        "git.confirmSync": false,
        "remote.autoForwardPorts": true
      },
      
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "ms-toolsai.jupyter",
        "ms-toolsai.jupyter-keymap",
        "ms-toolsai.jupyter-renderers",
        "njpwerner.autodocstring",
        "github.copilot",
        "github.copilot-chat",
        "ms-azuretools.vscode-docker",
        "ms-vscode-remote.remote-containers",
        "mtxr.sqltools",
        "mtxr.sqltools-driver-pg",
        "redis.redis-for-vscode",
        "streetsidesoftware.code-spell-checker",
        "usernamehw.errorlens",
        "yzhang.markdown-all-in-one",
        "bierner.markdown-mermaid",
        "eamodio.gitlens",
        "humao.rest-client",
        "gruntfuggly.todo-tree",
        "christian-kohler.path-intellisense",
        "aaron-bond.better-comments",
        "mikestead.dotenv",
        "redhat.vscode-yaml"
      ]
    }
  },
  
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/sshd:1": {},
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers-contrib/features/zsh-plugins:0": {
      "plugins": "git docker docker-compose python pip npm",
      "omzPlugins": "https://github.com/zsh-users/zsh-autosuggestions https://github.com/zsh-users/zsh-syntax-highlighting",
      "username": "vscode"
    }
  },
  
  "forwardPorts": [8000, 8001, 8080, 8888, 5432, 5433, 6379, 3000, 9090, 5000],
  
  "portsAttributes": {
    "8000": {
      "label": "AETHER API",
      "onAutoForward": "notify"
    },
    "8888": {
      "label": "Jupyter Lab",
      "onAutoForward": "openBrowser"
    },
    "3000": {
      "label": "Grafana Dashboard",
      "onAutoForward": "openBrowser"
    }
  },
  
  "postCreateCommand": "bash /workspace/aether/scripts/post-create.sh",
  "postStartCommand": "bash /workspace/aether/scripts/post-start.sh",
  
  "remoteUser": "vscode",
  "containerUser": "vscode",
  
  "mounts": [
    "source=aether-vscode-extensions,target=/home/vscode/.vscode-server/extensions,type=volume",
    "source=aether-cache,target=/home/vscode/.cache,type=volume"
  ],
  
  "runArgs": [
    "--shm-size=16g"
  ],
  
  "containerEnv": {
    "PYTHONPATH": "/workspace/aether/src:${PYTHONPATH}",
    "PROJECT_NAME": "AETHER",
    "ENVIRONMENT": "development"
  }
}'''
        self.create_file(".devcontainer/devcontainer.json", content)
        
    def create_docker_compose(self):
        """Create docker-compose.yml"""
        content = '''version: '3.9'

x-common-env: &common-env
  TZ: UTC
  PROJECT_NAME: AETHER
  ENVIRONMENT: development

services:
  aether-dev:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - PYTHON_VERSION=3.11
        - NODE_VERSION=20
    volumes:
      - ..:/workspace/aether:cached
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      <<: *common-env
      DATABASE_URL: postgresql://aether:aether123@postgres:5432/aether_trading
      REDIS_URL: redis://default:redis123@redis:6379/0
    command: sleep infinity
    networks:
      - aether-network
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: aether
      POSTGRES_PASSWORD: aether123
      POSTGRES_DB: aether_trading
    ports:
      - "5432:5432"
    networks:
      - aether-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    networks:
      - aether-network
    command: redis-server --requirepass redis123

volumes:
  postgres-data:
  redis-data:
  aether-vscode-extensions:
  aether-cache:

networks:
  aether-network:
    driver: bridge'''
        self.create_file(".devcontainer/docker-compose.yml", content)
        
    def create_dockerfiles(self):
        """Create Dockerfile"""
        dockerfile_content = '''FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    git \\
    curl \\
    vim \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \\
    && apt-get install -y nodejs

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \\
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \\
    && echo $USERNAME ALL=\\(root\\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME

# Install Python packages
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Switch to non-root user
USER $USERNAME

# Install oh-my-zsh
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

WORKDIR /workspace/aether

EXPOSE 8000 8888

CMD ["sleep", "infinity"]'''
        self.create_file(".devcontainer/Dockerfile", dockerfile_content)
        
        # Create requirements.txt
        requirements = '''fastapi==0.108.0
uvicorn[standard]==0.25.0
pydantic==2.5.3
anthropic==0.7.8
sqlalchemy==2.0.25
asyncpg==0.29.0
redis==5.0.1
pandas==2.1.4
numpy==1.26.3
ccxt==4.2.25
web3==6.14.0
pytest==7.4.4
black==23.12.1
jupyterlab==4.0.10'''
        self.create_file(".devcontainer/requirements.txt", requirements)
        
    def create_config_files(self):
        """Create configuration files"""
        # PostgreSQL init
        postgres_init = '''CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS trading;

CREATE TABLE IF NOT EXISTS trading.discovered_bots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    address VARCHAR(42) NOT NULL,
    chain VARCHAR(20) NOT NULL,
    discovery_time TIMESTAMP NOT NULL DEFAULT NOW(),
    score DECIMAL(5,4) NOT NULL,
    strategy_type VARCHAR(50),
    performance_metrics JSONB,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);'''
        self.create_file(".devcontainer/init-scripts/postgres/01-init.sql", postgres_init)
        
    def create_source_files(self):
        """Create Python source files"""
        # Main entry point
        main_py = '''#!/usr/bin/env python3
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
        console.print("\\n[red]Shutting down...[/red]")

if __name__ == "__main__":
    asyncio.run(main())'''
        self.create_file("src/main.py", main_py)
        
    def create_scripts(self):
        """Create shell scripts"""
        # Post-create script
        post_create = '''#!/bin/bash
echo "🚀 AETHER Post-Create Setup..."

# Install dependencies
pip install --upgrade pip
pip install -r /workspace/aether/requirements.txt || true

# Setup git
git config --global --add safe.directory /workspace/aether

echo "✅ Setup complete!"'''
        self.create_file("scripts/post-create.sh", post_create)
        os.chmod(self.project_path / "scripts/post-create.sh", 0o755)
        
        # Post-start script
        post_start = '''#!/bin/bash
echo "Waiting for services..."
sleep 5
echo "✅ Services ready!"'''
        self.create_file("scripts/post-start.sh", post_start)
        os.chmod(self.project_path / "scripts/post-start.sh", 0o755)
        
    def create_root_files(self):
        """Create root project files"""
        # .env.example
        env_example = '''# AETHER Configuration
CLAUDE_API_KEY=your_claude_api_key_here
DATABASE_URL=postgresql://aether:aether123@postgres:5432/aether_trading
REDIS_URL=redis://default:redis123@redis:6379/0
DEBUG=true'''
        self.create_file(".env.example", env_example)
        
        # .gitignore
        gitignore = '''__pycache__/
*.py[cod]
.env
.venv/
venv/
.vscode/
.idea/
*.log
data/
logs/
models/
*.db
.DS_Store'''
        self.create_file(".gitignore", gitignore)
        
        # README.md
        readme = '''# AETHER Trading System

Autonomous Evolution Trading Hub for Enhanced Returns

## Quick Start

1. Open in VS Code DevContainer
2. Configure .env file
3. Run: `python -m src.main`

## Features

- Bot Discovery
- Claude Code Integration  
- Autonomous Evolution
- Real-time Dashboard

## Documentation

See docs/ folder for detailed documentation.'''
        self.create_file("README.md", readme)
        
        # requirements.txt
        requirements = '''fastapi==0.108.0
uvicorn[standard]==0.25.0
pydantic==2.5.3
anthropic==0.7.8
langchain==0.1.0
sqlalchemy==2.0.25
asyncpg==0.29.0
redis==5.0.1
pandas==2.1.4
numpy==1.26.3
ccxt==4.2.25
web3==6.14.0
python-binance==1.0.19
ta==0.11.0
scikit-learn==1.3.2
pytest==7.4.4
black==23.12.1
flake8==6.1.0
jupyterlab==4.0.10
rich==13.7.0
click==8.1.7'''
        self.create_file("requirements.txt", requirements)
        
        # Makefile
        makefile = '''help:
	@echo "AETHER Trading System"
	@echo "  make run    - Run the system"
	@echo "  make test   - Run tests"
	@echo "  make format - Format code"

run:
	python -m src.main

test:
	pytest -v

format:
	black src tests'''
        self.create_file("Makefile", makefile)
        
    def create_init_files(self):
        """Create __init__.py files"""
        init_paths = [
            "src/__init__.py",
            "src/bot_hunter/__init__.py",
            "src/claude_analyzer/__init__.py",
            "src/evolution_engine/__init__.py",
            "src/shared/__init__.py",
            "tests/__init__.py"
        ]
        for path in init_paths:
            self.create_file(path, "")
            
    def setup_git(self):
        """Initialize git repository"""
        print("\n📚 Initializing Git repository...")
        os.chdir(self.project_path)
        subprocess.run(["git", "init"])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Initial commit: AETHER Trading System"])
        print("✅ Git repository initialized")
        
    def install_vscode_extensions(self):
        """Install VS Code extensions"""
        print("\n🔧 Installing VS Code extensions...")
        extensions = [
            "ms-vscode-remote.remote-containers",
            "ms-python.python",
            "ms-toolsai.jupyter"
        ]
        for ext in extensions:
            subprocess.run(["code", "--install-extension", ext])
        print("✅ VS Code extensions installed")
        
    def open_in_vscode(self):
        """Open project in VS Code"""
        print("\n📂 Opening project in VS Code...")
        subprocess.run(["code", str(self.project_path)])
        
    def print_next_steps(self):
        """Print next steps"""
        print(f"""
✅ AETHER Trading System setup complete!

📁 Project location: {self.project_path}

🚀 Next steps:
1. VS Code should open automatically
2. When prompted, click "Reopen in Container"
3. Copy .env.example to .env and add your API keys
4. Run 'make run' to start the system

📊 Access points:
- API: http://localhost:8000
- Jupyter: http://localhost:8888

📚 Documentation: {self.project_path}/docs/

Happy trading! 🤖
        """)
        
    def run(self):
        """Run the complete setup"""
        self.print_banner()
        self.check_system()
        self.check_prerequisites()
        self.create_project_structure()
        self.create_all_files()
        self.setup_git()
        self.install_vscode_extensions()
        # Skip auto-opening to avoid crashes
        self.print_next_steps()

if __name__ == "__main__":
    setup = AETHERSetup()
    setup.run()