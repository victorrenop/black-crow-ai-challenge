## Requirements
.PHONY: requirements
requirements:
	@PYTHONPATH=. poetry install

## Style Checks

.PHONY: check-black
check-black:
	@echo ""
	@echo "Code Style With Black"
	@echo "=========="
	@echo ""
	@python -m black --check -t py38 --exclude="build/|buck-out/|dist/|_build/|pip/|\.pip/|\.git/|\.hg/|\.mypy_cache/|\.tox/|\.venv/" . && echo "\n\nSuccess" || (echo "\n\nFailure\n\nRun \"make black\" to apply style formatting to your code"; return 2)
	@echo ""

.PHONY: check-flake8
check-flake8:
	@echo ""
	@echo "Flake 8 Lint"
	@echo "======="
	@echo ""
	@-python -m flake8 etl_builder/ && echo "etl_builder module success"
	@-python -m flake8 tests/ && echo "tests module success"
	@echo ""

.PHONY: checks
checks:
	@echo ""
	@echo "Code Style With Black & Flake 8 Lint"
	@echo "--------------------"
	@echo ""
	@make check-black
	@make check-flake8
	@echo ""

.PHONY: black
black:
	@python -m black -t py38 --exclude="build/|buck-out/|dist/|_build/|pip/|\.pip/|\.git/|\.hg/|\.mypy_cache/|\.tox/|\.venv/" .

## Tests

.PHONY: tests
tests:
	@python -m pytest --cov-branch --cov-report term-missing --cov=etl_builder tests/

.PHONY: build
build:
	@echo " >>> Building docker image"
	@docker build -f Dockerfile -t black_crow_ai_challenge .

## Clean Data

.PHONY: clean
clean:
	@find ./ -type d -name 'htmlcov' -exec rm -rf {} +;
	@find ./ -type d -name 'coverage.xml' -exec rm -rf {} +;
	@find ./ -type f -name 'coverage-badge.svg' -exec rm -f {} \;
	@find ./ -type f -name '.coverage' -exec rm -f {} \;
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
