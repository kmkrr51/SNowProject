.PHONY: help install dev build preview lint format test test-watch test-cov clean

help:
	@echo "ITSM Frontend - Available Commands"
	@echo "=================================="
	@echo "make install      - Install dependencies"
	@echo "make dev          - Start development server"
	@echo "make build        - Build for production"
	@echo "make preview      - Preview production build"
	@echo "make lint         - Run ESLint"
	@echo "make format       - Format code with Prettier"
	@echo "make test         - Run tests"
	@echo "make test-watch   - Run tests in watch mode"
	@echo "make test-cov     - Generate coverage report"
	@echo "make storybook    - Start Storybook"
	@echo "make clean        - Clean build artifacts"

install:
	npm install

dev:
	npm run dev

build:
	npm run build

preview:
	npm run preview

lint:
	npm run lint

format:
	npm run format

test:
	npm run test

test-watch:
	npm run test:watch

test-cov:
	npm run test:cov

storybook:
	npm run storybook

clean:
	rm -rf dist node_modules .next coverage
