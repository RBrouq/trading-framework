.PHONY: help format lint test lock docs clean ci

help:
    @echo "Usage:"
    @echo "  make format   # format code with Ruff"
    @echo "  make lint     # lint code (Ruff + Mypy)"
    @echo "  make test     # run tests with coverage"
    @echo "  make ci       # lint + test"
    @echo "  make lock     # regen requirements-lock.txt"
    @echo "  make docs     # build MkDocs site"
    @echo "  make clean    # clean build artifacts"

format:
    ruff format .

lint:
    ruff check .
    mypy src/trading_framework --strict

test:
    python -m pytest --cov=src --cov-report=xml

ci: lint test
    @echo "✅ CI checks passed!"

lock:
    python -m piptools compile --upgrade --output-file=requirements-lock.txt pyproject.toml

docs:
    mkdocs build

clean:
    -rm -rf build dist htmlcov .pytest_cache .ruff_cache
