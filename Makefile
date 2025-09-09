.PHONY: help install install-dev test test-cov lint format type-check clean build upload demo docs

help:
	@echo "Pygmalion Development Commands"
	@echo "============================="
	@echo ""
	@echo "install         Install package in current environment"
	@echo "install-dev     Install package with development dependencies"
	@echo "test            Run test suite"
	@echo "test-cov        Run tests with coverage report"
	@echo "lint            Run flake8 linter"
	@echo "format          Format code with black"
	@echo "type-check      Run mypy type checker"
	@echo "clean           Clean build artifacts"
	@echo "build           Build distribution packages"
	@echo "upload          Upload to PyPI (requires credentials)"
	@echo "demo            Run demo CLI application"
	@echo "docs            Generate documentation"
	@echo "all-checks      Run all code quality checks"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=pygmalion --cov-report=term-missing --cov-report=html

lint:
	flake8 pygmalion tests

format:
	black pygmalion tests

type-check:
	mypy pygmalion

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

demo:
	python -m pygmalion.cli demo

docs:
	@echo "Documentation generation not yet implemented"
	@echo "See README.md for current documentation"

all-checks: format lint type-check test

# Development workflow
dev-setup: install-dev
	@echo "Development environment set up successfully!"
	@echo "Run 'make test' to verify everything works."

dev-check: all-checks
	@echo "All checks passed! Ready to commit."

# Quick development cycle
quick-test:
	pytest -x --tb=short

watch-test:
	pytest --tb=short --looponfail

# Release workflow
pre-release: all-checks clean
	@echo "Pre-release checks completed successfully!"

release: pre-release build
	@echo "Release packages built successfully!"
	@echo "Run 'make upload' to publish to PyPI"
