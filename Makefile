POETRY_RUN := poetry run
BLUE=\033[0;34m
NC=\033[0m # No Color

.PHONY: all update lint test clean help

all: update lint test

update: ## Just update the environment
	@echo "\n${BLUE}Running poetry update...${NC}\n"
	@${POETRY_RUN} pip install --upgrade pip setuptools
	@${POETRY_RUN} python --version
	poetry update
	@echo "\n${BLUE}Show outdated packages...${NC}\n"
	@${POETRY_RUN} pip list -o --not-required --outdated


lint: ## Run linting tools.
	@echo "\n${BLUE}Running linting...${NC}\n"
	@${POETRY_RUN} black --target-version py310 .
	@${POETRY_RUN} isort .
	@${POETRY_RUN} pyupgrade --py310-plus $(shell find aiven -name "*.py")
	@echo "\n${BLUE}Running mypy...${NC}\n"
	@${POETRY_RUN} mypy aiven
	@echo "\n${BLUE}Running pylint...${NC}\n"
	@${POETRY_RUN} pylint aiven

test: ## Run unit tests.
	@echo "\n${BLUE}Running tests...${NC}\n"
	@${POETRY_RUN} pytest


clean: ## Force a clean environment: remove all temporary files and caches. Start from a new environment.
	@echo "\n${BLUE}Cleaning up...${NC}\n"
	rm -rf .mypy_cache .pytest_cache htmlcov junit coverage.xml .coverage
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	@echo "\n${BLUE}Removing poetry environment...${NC}\n"
	poetry env list
	poetry env info -p
	poetry env remove $(shell poetry run which python)
	poetry env list

help: ## Show this help.
	@egrep -h '\s##\s' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'