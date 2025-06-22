help:
	@echo "AETHER Trading System"
	@echo "  make run    - Run the system"
	@echo "  make test   - Run tests"
	@echo "  make format - Format code"

run:
	python -m src.main

test:
	pytest -v

format:
	black src tests
