# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirement.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy application code
COPY src/ ./src/
COPY main.py setup.py ./
COPY assets/ ./assets/

# Create necessary directories
RUN mkdir -p data output logs backups

# Set environment variables
ENV PYTHONPATH=/app:/app/src
ENV OUTPUT_FILE=data/iceberg_location.json
ENV LOG_LEVEL=INFO

# Create non-root user
RUN useradd --create-home --shell /bin/bash iceberg
RUN chown -R iceberg:iceberg /app
USER iceberg

# Health check
HEALTHCHECK --interval=5m --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('https://www.scp.byu.edu/current_icebergs.html', timeout=10)"

# Default command
CMD ["python", "main.py", "scrape"]

# Labels
LABEL maintainer="Joel Hanson <joel@example.com>"
LABEL description="Antarctic Iceberg Location Tracker"
LABEL version="2.0"
