.PHONY: install dev run test lint format typecheck clean build publish-test publish all

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

run:
	python -m devdash

test:
	pytest --cov=src/devdash --cov-report=term-missing

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	mypy src/devdash

clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage

build:
	python -m build

publish-test:
	twine upload --repository testpypi dist/*

publish:
	twine upload dist/*

all: lint typecheck test
