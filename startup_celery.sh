#!/bin/bash
echo "Starting Celery Worker..."

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Start Celery worker
echo "Starting Celery worker..."
exec celery -A celery_app worker --loglevel=INFO --max-tasks-per-child=50 --concurrency=1 --without-gossip --without-mingle --without-heartbeat