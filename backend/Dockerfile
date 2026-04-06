# Production Dockerfile for Google Cloud Run
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080
ENV APP_ENV=production
ENV DISABLE_DATABASE=true
ENV DISABLE_REDIS=true

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Test startup before switching user
RUN python test_startup.py

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8080

# Run the no-database version for Cloud Run
CMD ["python", "-c", "import uvicorn; uvicorn.run('app.main_no_db:app', host='0.0.0.0', port=int(__import__('os').environ.get('PORT', 8080)), workers=1)"]