# Urban Copilot Makefile
# Simplifies common development and testing tasks

.PHONY: setup run test load-test check-env clean docker-build docker-run help

# Variables (can be overridden with environment variables)
PORT ?= 5000
FLASK_ENV ?= development
CONCURRENCY ?= 10
REQUESTS ?= 50

# Default target
.DEFAULT_GOAL := help

setup: ## Install dependencies and set up project structure
	@echo "Setting up Urban Copilot environment..."
	pip install -r requirements.txt
	chmod +x test_api.py load_test.py check_env.py
	@echo "Setup complete!"

run: ## Run the Flask application locally
	@echo "Starting Urban Copilot on port $(PORT)..."
	FLASK_APP=app.server:app FLASK_ENV=$(FLASK_ENV) python -m flask run --host=0.0.0.0 --port=$(PORT)

test: ## Run API connectivity tests
	@echo "Running API connectivity tests..."
	./test_api.py

load-test: ## Run load tests on the API
	@echo "Running load tests..."
	./load_test.py --requests=$(REQUESTS) --concurrency=$(CONCURRENCY)

check-env: ## Verify environment variables are properly configured
	@echo "Checking environment variables..."
	./check_env.py

clean: ## Clean up temporary files and caches
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	@echo "Clean complete!"

docker-build: ## Build the Docker image
	@echo "Building Urban Copilot Docker image..."
	docker build -t urban-copilot:latest .

docker-run: ## Run the application using Docker Compose
	@echo "Starting Urban Copilot with Docker Compose..."
	docker-compose up

docker-test: ## Run tests in the Docker environment
	@echo "Running tests in Docker environment..."
	docker-compose run --rm app python -m pytest

help: ## Display this help message
	@echo "Urban Copilot Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Additional options:"
	@echo "  make run PORT=8080        # Run on port 8080"
	@echo "  make load-test REQUESTS=100 CONCURRENCY=20  # Custom load test parameters"
