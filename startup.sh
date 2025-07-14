#!/bin/bash

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
