#!/bin/bash

echo "Starting Therapeutic Companion Application..."

# Print environment info for debugging
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# Check for HTML files
echo ""
echo "Checking for HTML files:"
for file in index.html login.html therapist_dashboard.html client_dashboard.html therapist-dashboard.html client-dashboard.html reset-password.html; do
    if [ -f "$file" ]; then
        echo "✓ Found: $file"
    else
        echo "✗ Missing: $file"
    fi
done

# Initialize database (only if DATABASE_URL is set)
if [ ! -z "$DATABASE_URL" ]; then
    echo ""
    echo "Initializing database..."
    python init_db.py
    
    # Run the migration to fix existing clients
    echo ""
    echo "Fixing client tracking categories..."
    python migration_fix_categories.py
else
    echo ""
    echo "WARNING: DATABASE_URL not set, skipping database initialization"
fi

# Start the application
echo ""
echo "Starting Gunicorn..."
exec gunicorn new_backend:app --bind 0.0.0.0:${PORT:-10000} --workers 2 --threads 2 --timeout 120 --log-level info
