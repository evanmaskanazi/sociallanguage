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


def add_local_reminder_time_column():
    """Add column to store the original local time for display purposes"""
    with app.app_context():
        try:
            # Check if column exists
            result = db.session.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='reminders'
                AND column_name='local_reminder_time'
            """))

            if not result.fetchone():
                # Column doesn't exist, add it
                db.session.execute(text("""
                    ALTER TABLE reminders
                    ADD COLUMN local_reminder_time VARCHAR(5)
                """))
                db.session.commit()
                print("Successfully added local_reminder_time column to reminders table")
            else:
                print("local_reminder_time column already exists - skipping")

        except Exception as e:
            print(f"Error checking/adding local_reminder_time column: {e}")
            db.session.rollback()


def fix_existing_reminder_times():
    """Convert existing reminder times to UTC if they seem to be in local time"""
    with app.app_context():
        try:
            from new_backend import Reminder

            # Get all reminders
            reminders = Reminder.query.filter_by(reminder_type='daily_checkin').all()

            for reminder in reminders:
                # If reminder hour is greater than 12, it's likely in local time (PM hours)
                if reminder.reminder_time and reminder.reminder_time.hour > 12:
                    print(f"Converting reminder time for client {reminder.client_id}: {reminder.reminder_time}")
                    # This is a rough conversion - assumes PST/PDT (UTC-7/8)
                    # You may need to adjust based on your users' locations
                    old_hour = reminder.reminder_time.hour
                    new_hour = (old_hour + 7) % 24  # Add 7 for PDT to UTC

                    from datetime import time
                    reminder.reminder_time = time(new_hour, reminder.reminder_time.minute)
                    print(f"  -> Converted to UTC: {reminder.reminder_time}")

            db.session.commit()
            print("Reminder time conversion complete")

        except Exception as e:
            print(f"Error converting reminder times: {e}")
            db.session.rollback()


def fix_reminder_timezone_issue():
    """Fix reminders that may have been stored with incorrect timezone conversion"""
    with app.app_context():
        try:
            from new_backend import Reminder, Client, User
            from datetime import time

            print("\nChecking for reminder timezone issues...")

            # Get all reminders
            reminders = Reminder.query.filter_by(
                reminder_type='daily_checkin',
                is_active=True
            ).all()

            fixed_count = 0

            for reminder in reminders:
                # Get the client's email to check if it's a test
                client_email = reminder.client.user.email

                # Skip test emails
                if client_email.endswith('test.test') or client_email.endswith('example.com'):
                    continue

                current_hour = reminder.reminder_time.hour
                current_minute = reminder.reminder_time.minute

                print(f"\nClient {reminder.client.client_serial} ({client_email}):")
                print(f"  Current stored UTC time: {reminder.reminder_time}")
                print(f"  Current local_reminder_time: {reminder.local_reminder_time}")

                # Fix missing local_reminder_time
                if not reminder.local_reminder_time:
                    # If the UTC hour is between 16-23 (4 PM - 11 PM UTC)
                    # it's likely this was meant to be morning hours in PDT/PST
                    if 16 <= current_hour <= 23:
                        # Convert from UTC to PDT (subtract 7 hours)
                        local_hour = (current_hour - 7) % 24
                        reminder.local_reminder_time = f"{local_hour:02d}:{current_minute:02d}"
                        fixed_count += 1
                        print(f"  -> Set local_reminder_time to: {reminder.local_reminder_time}")
                    elif 0 <= current_hour <= 6:
                        # Early morning UTC might be evening PDT from previous day
                        local_hour = (current_hour + 17) % 24  # +17 = -7 + 24
                        reminder.local_reminder_time = f"{local_hour:02d}:{current_minute:02d}"
                        fixed_count += 1
                        print(f"  -> Set local_reminder_time to: {reminder.local_reminder_time}")
                    else:
                        # For other hours, assume they might be correct
                        reminder.local_reminder_time = f"{current_hour:02d}:{current_minute:02d}"
                        fixed_count += 1
                        print(f"  -> Set local_reminder_time to: {reminder.local_reminder_time}")

                # Special fix for the specific user
                if client_email == 'ema9u@virginia.edu' and reminder.local_reminder_time == '09:00':
                    # You mentioned they want 2 PM, not 9 AM
                    reminder.local_reminder_time = '14:00'
                    # Calculate UTC time for 2 PM PDT (add 7 hours)
                    reminder.reminder_time = time(21, 0)  # 2 PM PDT = 9 PM UTC
                    fixed_count += 1
                    print(f"  -> SPECIAL FIX: Set to 14:00 local (21:00 UTC)")

            if fixed_count > 0:
                db.session.commit()
                print(f"\nFixed {fixed_count} reminder times")
            else:
                print("\nNo reminder times needed fixing")

        except Exception as e:
            print(f"Error fixing reminder times: {e}")
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
        add_local_reminder_time_column()  # ADD THIS LINE - This is the new function call
        fix_existing_reminder_times()
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

        # Fix any existing reminder timezone issues
        fix_reminder_timezone_issue()

    print("\n" + "=" * 50)
    print("Initialization script completed")
    print("=" * 50)

    # Exit with success code
    sys.exit(0)