# Makefile for Iceberg Location Tracker

.PHONY: help install test lint clean scrape info map animations setup docker backup ci dev web

# Default target
help:
	@echo "Iceberg Location Tracker - Available commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make install    Install dependencies"
	@echo "  make setup      Initialize project structure"
	@echo ""
	@echo "Development:"
	@echo "  make test       Run tests"
	@echo "  make lint       Run code linting"
	@echo "  make clean      Clean temporary files"
	@echo ""
	@echo "Data Operations:"
	@echo "  make scrape     Scrape latest iceberg data"
	@echo "  make info       Show data summary"
	@echo "  make map        Generate interactive map"
	@echo "  make animations Show iceberg movement animation URLs"
	@echo ""
	@echo "Docker:"
	@echo "  make docker     Build and run Docker container"

# Installation and setup
install:
	@echo "Installing dependencies..."
	pip install -r requirement.txt
	@echo "Dependencies installed"

setup: install
	@echo "Setting up project..."
	python setup.py
	@echo "Project setup complete"

# Development
test:
	@echo "Running tests..."
	cd src && python tests.py
	@echo "Tests completed"

lint:
	@echo "Running code analysis..."
	python -m py_compile src/*.py
	python -m py_compile main.py setup.py
	@echo "Code analysis complete"

clean:
	@echo "Cleaning temporary files..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -f *.log
	@echo "Cleanup complete"

# Data operations
scrape:
	@echo "Scraping iceberg data..."
	python main.py scrape
	@echo "Data scraping complete"

info:
	@echo "� Displaying data info..."
	python main.py info
	@echo "Data info displayed"

map:
	@echo "Generating interactive map..."
	python main.py map
	@echo "Map generated"

animations:
	@echo "Displaying iceberg movement animations..."
	python main.py animations
	@echo "Animation URLs displayed"

# Docker operations
docker:
	@echo "Building Docker container..."
	docker build -t iceberg-tracker .
	@echo "Running container..."
	docker run --rm -v $(PWD)/data:/app/data iceberg-tracker

# Maintenance
backup:
	@echo "Creating backup..."
	mkdir -p backups
	cp data/iceberg_location.json backups/iceberg_location_$(shell date +%Y%m%d_%H%M%S).json
	@echo "Backup created"

# CI/CD
ci: install lint test
	@echo "CI pipeline completed successfully"

# Development workflow
dev: clean install setup test
	@echo "Development environment ready!"

web:
	@echo "Starting web server..."
	python main.py map
	@echo "Open output/iceberg_map.html in your browser"
	@echo "Map generated and ready to view"