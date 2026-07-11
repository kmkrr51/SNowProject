.PHONY: help install dev test lint format clean

help:
	@echo "ITSM Microservices Development Commands"
	@echo "========================================"
	@echo "make install    - Install dependencies"
	@echo "make dev        - Run development server"
	@echo "make test       - Run tests"
	@echo "make lint       - Run linting checks"
	@echo "make format     - Format code with Black"
	@echo "make clean      - Clean up generated files"

install:
	pip install -r requirements.txt

dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

test-cov:
	pytest -v --cov=src --cov-report=html

lint:
	flake8 src tests
	mypy src

format:
	black src tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf *.db
