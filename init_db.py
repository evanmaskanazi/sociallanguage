#!/usr/bin/env python
"""Initialize database with proper migration handling"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from new_backend import app, db, TrackingCategory, ensure_default_categories, fix_existing_clients
from sqlalchemy import text

def safe_add_column():
    """Safely add reminder_email column if it doesn't exist"""
    with app.app_context():
        try:
            # Check if column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='reminders' 
                AND column_name='reminder_email'
            """))
            
            if not result.fetchone():
                # Column doesn't exist, add it
                db.session.execute(text("""
                    ALTER TABLE reminders 
                    ADD COLUMN reminder_email VARCHAR(255)
                """))
                db.session.commit()
                print("Successfully added reminder_email column to reminders table")
            else:
                print("reminder_email column already exists - skipping")
                
        except Exception as e:
            print(f"Error checking/adding reminder_email column: {e}")
            db.session.rollback()

def initialize_database():
    """Initialize database with all required setup"""
    print("Starting database initialization...")
    
    try:
        # Create all tables
        db.create_all()
        print("✓ Database tables created/verified")
        
        # Add new columns safely
        safe_add_column()
        
        # Ensure all default tracking categories exist
        categories = ensure_default_categories()
        print(f"✓ Verified {len(categories)} tracking categories")
        
        # Fix any existing clients that might be missing categories
        fix_existing_clients()
        print("✓ Updated existing clients with any missing categories")
        
        # Check if we have the expected 8 categories
        category_count = TrackingCategory.query.count()
        if category_count < 8:
            print(f"⚠️  Warning: Only {category_count} categories found, expected 8")
            print("   Running ensure_default_categories again...")
            ensure_default_categories()
            category_count = TrackingCategory.query.count()
            print(f"   Now have {category_count} categories")
        
        # List all categories for verification
        print("\nTracking categories in database:")
        for cat in TrackingCategory.query.all():
            print(f"  - {cat.name} (ID: {cat.id}, Default: {cat.is_default})")
        
        print("\n✅ Database initialization complete!")
        
    except Exception as e:
        print(f"\n❌ Error during database initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    print("=" * 50)
    print("Therapy Companion Database Initialization")
    print("=" * 50)
    
    # Check if we're in production
    if os.environ.get('PRODUCTION'):
        print("Running in PRODUCTION mode")
    else:
        print("Running in DEVELOPMENT mode")
    
    # Show database URL (masked for security)
    db_url = os.environ.get('DATABASE_URL', 'Not set')
    if db_url != 'Not set':
        # Mask the password in the URL for security
        if '@' in db_url:
            parts = db_url.split('@')
            if '://' in parts[0]:
                proto_and_creds = parts[0].split('://')
                if ':' in proto_and_creds[1]:
                    user = proto_and_creds[1].split(':')[0]
                    masked_url = f"{proto_and_creds[0]}://{user}:****@{parts[1]}"
                    print(f"Database URL: {masked_url}")
                else:
                    print(f"Database URL: {db_url}")
            else:
                print(f"Database URL: [configured]")
        else:
            print(f"Database URL: {db_url}")
    else:
        print("Database URL: [using default]")
    
    print()
    
    with app.app_context():
        initialize_database()
    
    print("\n" + "=" * 50)
    print("Initialization script completed")
    print("=" * 50)
    
    # Exit with success code
    sys.exit(0)
