#!/bin/bash
echo "🚀 AETHER Post-Create Setup..."

# Install dependencies
pip install --upgrade pip
pip install -r /workspace/aether/requirements.txt || true

# Setup git
git config --global --add safe.directory /workspace/aether

echo "✅ Setup complete!"
