#!/usr/bin/env python
"""Initialize database with proper migration handling"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from new_backend import app, db, TrackingCategory, ensure_default_categories, fix_existing_clients, EmailQueue
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


def create_circuit_breaker_table():
    """Create table for circuit breaker state"""
    with app.app_context():
        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS circuit_breaker_state (
                    service VARCHAR(50) PRIMARY KEY,
                    failure_count INTEGER DEFAULT 0,
                    last_failure_time TIMESTAMP,
                    is_open BOOLEAN DEFAULT FALSE
                )
            """))
            db.session.commit()
            print("Successfully created circuit_breaker_state table")
        except Exception as e:
            print(f"Error creating circuit_breaker_state table: {e}")
            db.session.rollback()


def add_email_valid_column():
    """Add email_valid column to users table"""
    with app.app_context():
        try:
            # Check if column exists
            result = db.session.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='users'
                AND column_name='email_valid'
            """))

            if not result.fetchone():
                # Column doesn't exist, add it
                db.session.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN email_valid BOOLEAN DEFAULT TRUE
                """))
                db.session.commit()
                print("Successfully added email_valid column to users table")
            else:
                print("email_valid column already exists - skipping")

        except Exception as e:
            print(f"Error checking/adding email_valid column: {e}")
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

            print("\nChecking and fixing reminder timezone issues...")

            # Get all reminders
            reminders = Reminder.query.filter_by(
                reminder_type='daily_checkin',
                is_active=True
            ).all()

            fixed_count = 0

            for reminder in reminders:
                if reminder.local_reminder_time:
                    # Parse what the user actually entered
                    local_hour, local_minute = map(int, reminder.local_reminder_time.split(':'))

                    # Get what's currently stored as UTC
                    stored_utc_hour = reminder.reminder_time.hour
                    stored_utc_minute = reminder.reminder_time.minute

                    # For Jerusalem (UTC+2 or UTC+3), if local time is 10:00
                    # UTC should be 07:00 or 08:00 (2-3 hours earlier)
                    # If stored UTC is later than local time, it's wrong

                    # Calculate what UTC should be (assume UTC+3 for summer)
                    expected_utc_minutes = (local_hour * 60 + local_minute) - 180  # Jerusalem is UTC+3
                    if expected_utc_minutes < 0:
                        expected_utc_minutes += 24 * 60

                    expected_utc_hour = (expected_utc_minutes // 60) % 24
                    expected_utc_minute = expected_utc_minutes % 60

                    # Check if it needs fixing
                    if stored_utc_hour != expected_utc_hour or stored_utc_minute != expected_utc_minute:
                        # Fix it
                        reminder.reminder_time = time(expected_utc_hour, expected_utc_minute)
                        fixed_count += 1
                        print(f"  Fixed {reminder.client.client_serial}: "
                              f"{reminder.local_reminder_time} local -> "
                              f"{expected_utc_hour:02d}:{expected_utc_minute:02d} UTC "
                              f"(was {stored_utc_hour:02d}:{stored_utc_minute:02d})")

            if fixed_count > 0:
                db.session.commit()
                print(f"\nFixed {fixed_count} reminder times")
            else:
                print("\nNo reminder times needed fixing")

        except Exception as e:
            print(f"Error fixing reminder times: {e}")
            db.session.rollback()



def add_reminder_language_column():
    """Add reminder_language column to reminders table"""
    with app.app_context():
        try:
            # Check if column exists
            result = db.session.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='reminders'
                AND column_name='reminder_language'
            """))

            if not result.fetchone():
                # Column doesn't exist, add it
                db.session.execute(text("""
                    ALTER TABLE reminders
                    ADD COLUMN reminder_language VARCHAR(2) DEFAULT 'en'
                """))
                db.session.commit()
                print("Successfully added reminder_language column to reminders table")
            else:
                print("reminder_language column already exists - skipping")

        except Exception as e:
            print(f"Error checking/adding reminder_language column: {e}")
            db.session.rollback()


def add_performance_indexes():
    """Add indexes for frequently queried columns"""
    from sqlalchemy import text

    indexes = [
        # Client queries
        "CREATE INDEX IF NOT EXISTS idx_clients_therapist_active ON clients(therapist_id, is_active)",
        "CREATE INDEX IF NOT EXISTS idx_clients_serial ON clients(client_serial)",

        # Daily checkins
        "CREATE INDEX IF NOT EXISTS idx_checkins_client_date ON daily_checkins(client_id, checkin_date DESC)",
        "CREATE INDEX IF NOT EXISTS idx_checkins_date_range ON daily_checkins(checkin_date)",

        # Category responses
        "CREATE INDEX IF NOT EXISTS idx_category_resp_lookup ON category_responses(client_id, category_id, response_date)",

        # Tracking plans
        "CREATE INDEX IF NOT EXISTS idx_tracking_plans_active ON client_tracking_plans(client_id, is_active)",

        # Goals
        "CREATE INDEX IF NOT EXISTS idx_goals_week ON weekly_goals(client_id, week_start, is_active)",

        # Reminders
        "CREATE INDEX IF NOT EXISTS idx_reminders_active ON reminders(client_id, reminder_type, is_active)",
        "CREATE INDEX IF NOT EXISTS idx_reminders_time ON reminders(reminder_time, is_active)",

        # Email queue
        "CREATE INDEX IF NOT EXISTS idx_email_queue_status ON email_queue(status, created_at)",

        # Audit logs
        "CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp DESC)",
    ]

    for index_sql in indexes:
        try:
            db.session.execute(text(index_sql))
            print(f"Created index: {index_sql.split('idx_')[1].split(' ')[0]}")
        except Exception as e:
            print(f"Error creating index: {e}")

    db.session.commit()
    print("All indexes created successfully")





def initialize_database():
    """Initialize database with all required setup"""
    print("Starting database initialization...")

    try:
        # Create all tables
        db.create_all()
        print("✓ Database tables created/verified")

        # Add new columns safely
        safe_add_column()
        add_local_reminder_time_column() # ADD THIS LINE - This is the new function call
        add_reminder_language_column()
        create_circuit_breaker_table()
        add_email_valid_column()
        fix_existing_reminder_times()
        # Ensure all default tracking categories exist
        categories = ensure_default_categories()
        print(f"✓ Verified {len(categories)} tracking categories")

        # Fix any existing clients that might be missing categories
        fix_existing_clients()
        print("✓ Updated existing clients with any missing categories")

        # Create consent records table if missing
        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS consent_records (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER NOT NULL REFERENCES clients(id),
                    consent_type VARCHAR(50) NOT NULL,
                    consent_version VARCHAR(20) NOT NULL,
                    consented BOOLEAN NOT NULL,
                    consent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address VARCHAR(45),
                    withdrawal_date TIMESTAMP
                )
            """))
            db.session.commit()
            print("✓ Created consent_records table")
        except Exception as e:
            print(f"Consent records table may already exist: {e}")

        # Create email queue table if missing
        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS email_queue (
                    id SERIAL PRIMARY KEY,
                    to_email VARCHAR(255) NOT NULL,
                    subject VARCHAR(500) NOT NULL,
                    body TEXT NOT NULL,
                    html_body TEXT,
                    status VARCHAR(50) DEFAULT 'pending',
                    attempts INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sent_at TIMESTAMP,
                    last_attempt_at TIMESTAMP,
                    error_message TEXT
                )
            """))
            db.session.commit()
            print("✓ Created email_queue table")
        except Exception as e:
            print(f"Email queue table may already exist: {e}")
        # Create audit logs table if missing
        try:
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    user_email VARCHAR(255),
                    action VARCHAR(100) NOT NULL,
                    resource_type VARCHAR(50),
                    resource_id INTEGER,
                    ip_address VARCHAR(45),
                    user_agent VARCHAR(500),
                    details JSON,
                    phi_accessed BOOLEAN DEFAULT FALSE,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_audit_user_timestamp ON audit_logs(user_id, timestamp);
                CREATE INDEX IF NOT EXISTS idx_audit_phi_timestamp ON audit_logs(phi_accessed, timestamp);
            """))
            db.session.commit()
            print("✓ Created audit_logs table with indexes")
        except Exception as e:
            print(f"Audit logs table may already exist: {e}")

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

        # Add performance indexes
        add_performance_indexes()

    print("\n" + "=" * 50)
    print("Initialization script completed")
    print("=" * 50)

    print("\nEncrypting existing sensitive data...")
    try:
        from migrations.encrypt_existing_data import migrate_checkin_encryption

        migrate_checkin_encryption()
        print("✅ Sensitive data encrypted successfully")
    except Exception as e:
        print(f"⚠️ Could not encrypt existing data: {e}")
        print("   Run migrations/encrypt_existing_data.py manually")

    # Exit with success code
    sys.exit(0)