web: python init_db.py && python migration_fix_categories.py && gunicorn new_backend:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120
