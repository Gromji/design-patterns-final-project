.PHONY: help
.DEFAULT_GOAL := help

install: ## Install requirements
	pip install -r requirements.txt

format: ## Run code formatters
	isort wallet
	black wallet

lint: ## Run code linters
	isort --check wallet
	black --check wallet
	flake8 wallet
	rm -rf .mypy_cache
	mypy wallet


test: ## Run tests
	pytest --cov=wallet --cov-report=term-missing wallet/tests/

run: ## Run the program
	python -m wallet.runner

clean: ## Clean up the project
	py3clean .

all: ## Run all commands
	make format
	make lint
	make test

reset:
	rm ./wallet.db
