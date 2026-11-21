.PHONY: install test lint format typecheck security check run

PYTHON ?= .venv/bin/python

install:
	uv venv --clear .venv
	uv pip install --python $(PYTHON) -e ".[dev]"

test:
	$(PYTHON) -m pytest --cov=app --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check app tests
	$(PYTHON) -m ruff format --check app tests

format:
	$(PYTHON) -m ruff format app tests

typecheck:
	$(PYTHON) -m mypy app tests

security:
	$(PYTHON) -m bandit -q -r app
	$(PYTHON) -m pip_audit -r requirements.txt

check: lint typecheck test

run:
	$(PYTHON) -m uvicorn app.main:app --reload --port 8080
