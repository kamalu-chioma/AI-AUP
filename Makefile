.PHONY: help install install-dev test lint format type-check clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install the package in editable mode"
	@echo "  make install-dev  - Install with development dependencies"
	@echo "  make test         - Run tests with pytest"
	@echo "  make lint         - Run ruff linter"
	@echo "  make format       - Format code with ruff"
	@echo "  make type-check   - Run mypy type checker"
	@echo "  make clean        - Remove build artifacts and caches"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests examples

format:
	ruff format src tests examples

type-check:
	mypy src

clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

