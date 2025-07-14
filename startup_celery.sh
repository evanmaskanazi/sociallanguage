#!/bin/bash

echo "Starting Celery Workers..."

# Start Redis if running locally (for development)
if [ "$ENVIRONMENT" = "development" ]; then
    redis-server --daemonize yes
fi

# Wait for Redis to be available
echo "Waiting for Redis..."
for i in {1..30}; do
    if redis-cli ping > /dev/null 2>&1; then
        echo "Redis is ready!"
        break
    fi
    echo "Waiting for Redis... ($i/30)"
    sleep 1
done

# Start Celery worker in background
echo "Starting Celery worker..."
celery -A celery_app worker --loglevel=info --concurrency=2 &
WORKER_PID=$!

# Start Celery beat in background
echo "Starting Celery beat..."
celery -A celery_app beat --loglevel=info &
BEAT_PID=$!

# Start Flower for monitoring (optional)
if [ "$ENABLE_FLOWER" = "true" ]; then
    echo "Starting Flower..."
    celery -A celery_app flower --port=5555 &
    FLOWER_PID=$!
fi

# Wait for any process to exit
wait $WORKER_PID $BEAT_PID $FLOWER_PID

# Exit with status of process that exited first
exit $?