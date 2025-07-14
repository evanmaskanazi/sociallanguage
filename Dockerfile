FROM python:3.11-slim

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libpangocairo-1.0-0 \
    fonts-noto \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Make startup script executable
RUN chmod +x startup.sh

# Use startup script
CMD ["./startup.sh"]
startup.sh:
bash#!/bin/bash

echo "Starting Therapeutic Companion Application..."

# Initialize database (only if DATABASE_URL is set)
if [ ! -z "$DATABASE_URL" ]; then
    echo "Initializing database..."
    python init_db.py
    
    echo "Running category migration..."
    python migration_fix_categories.py
else
    echo "WARNING: DATABASE_URL not set, skipping database initialization"
fi

# Start the application
echo "Starting Gunicorn server..."
exec gunicorn new_backend:app --bind 0.0.0.0:${PORT:-10000} --workers 2 --threads 2 --timeout 120 --log-level info
