FROM python:3.11-slim

LABEL maintainer="CuratAI Team"
LABEL description="CuratAI - Agentic AI for Artist Opportunity Curation"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/
COPY docs/ ./docs/
COPY examples/ ./examples/

# Create non-root user
RUN useradd -m -u 1000 curataai && \
    chown -R curataai:curataai /app

USER curataai

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "src/main.py"]
