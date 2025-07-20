#!/usr/bin/env python3
"""
Database-level timezone testing for the reminder system.
Tests database storage, retrieval, and Celery worker time matching.
Modified to work without external dependencies.
"""

import os
import sys
from datetime import datetime, timedelta
from datetime import time as datetime_time  # Rename to avoid conflict
import time  # Import time module for sleep if needed

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from existing app
try:
    from new_backend import app, db, Client, Reminder, User, CircuitBreakerState
    from flask import Flask
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    print("Warning: Could not import from new_backend. Tests will be limited.")

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

class DatabaseTimezoneTester:
    """Test database timezone handling"""
    
    def __init__(self):
        self.test_results = []
        
    def print_header(self, text):
        """Print a formatted header"""
        print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.CYAN}{text.center(60)}{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")
    
    def test_database_timezone(self):
        """Test database timezone configuration"""
        print(f"{Colors.YELLOW}Testing Database Timezone Configuration{Colors.RESET}")
        
        if not BACKEND_AVAILABLE:
            print(f"{Colors.RED}Backend not available - skipping database tests{Colors.RESET}")
            return
        
        with app.app_context():
            # Check database timezone
            result = db.session.execute(db.text("SHOW timezone;"))
            tz = result.scalar()
            print(f"Database timezone: {tz}")
            
            if tz == 'UTC':
                print(f"{Colors.GREEN}✓ Database is correctly using UTC{Colors.RESET}")
            else:
                print(f"{Colors.RED}✗ Database is NOT using UTC (using {tz}){Colors.RESET}")
            
            # Check current time
            result = db.session.execute(db.text("SELECT NOW();"))
            db_now = result.scalar()
            print(f"Database NOW(): {db_now}")
            
            result = db.session.execute(db.text("SELECT NOW() AT TIME ZONE 'UTC';"))
            db_utc = result.scalar()
            print(f"Database UTC: {db_utc}")
    
    def test_reminder_storage(self):
        """Test how reminders are stored in the database"""
        print(f"\n{Colors.YELLOW}Testing Database Reminder Storage{Colors.RESET}")
        
        if not BACKEND_AVAILABLE:
            return
        
        with app.app_context():
            # Get sample reminders
            reminders = Reminder.query.filter_by(
                reminder_type='daily_checkin',
                is_active=True
            ).limit(5).all()
            
            if not reminders:
                print(f"{Colors.YELLOW}No active reminders found{Colors.RESET}")
                return
            
            print(f"\nSample Reminder Analysis:")
            for reminder in reminders[:1]:  # Just show one in detail
                print(f"  Client ID: {reminder.client_id}")
                print(f"  Reminder Time (UTC): {reminder.reminder_time}")
                print(f"  Local Reminder Time: {reminder.local_reminder_time}")
                print(f"  Is Active: {reminder.is_active}")
                print(f"  Last Sent: {reminder.last_sent}")
                
                if reminder.local_reminder_time:
                    print(f"  {Colors.GREEN}✓ local_reminder_time is populated{Colors.RESET}")
                else:
                    print(f"  {Colors.RED}✗ local_reminder_time is NULL{Colors.RESET}")
            
            # Check UTC hour distribution
            print(f"\nUTC Hour Analysis:")
            for reminder in reminders:
                if reminder.reminder_time:
                    utc_hour = reminder.reminder_time.hour
                    print(f"  UTC Hour: {utc_hour}")
            
            # Check current hour
            current_utc = datetime.utcnow()
            print(f"  Current UTC Hour: {current_utc.hour}")
    
    def test_timezone_conversion(self):
        """Test timezone conversion calculations"""
        print(f"\n{Colors.YELLOW}Testing Timezone Conversion Accuracy{Colors.RESET}")
        
        test_cases = [
            ('Asia/Jerusalem', '10:00', -180),  # UTC+3
            ('America/Los_Angeles', '10:00', 420),  # UTC-7
            ('Europe/London', '10:00', -60),  # UTC+1
            ('Asia/Tokyo', '10:00', -540),  # UTC+9
        ]
        
        for timezone, local_time, offset_minutes in test_cases:
            print(f"\nTesting {timezone}:")
            print(f"  Local time: {local_time}")
            print(f"  Expected offset: {offset_minutes} minutes")
            
            # Calculate UTC time
            hour, minute = map(int, local_time.split(':'))
            local_minutes = hour * 60 + minute
            utc_minutes = (local_minutes - offset_minutes) % (24 * 60)
            utc_hour = utc_minutes // 60
            utc_minute = utc_minutes % 60
            
            print(f"  Calculated UTC: {utc_hour:02d}:{utc_minute:02d}")
            print(f"  Note: Actual offset may vary due to DST")
    
    def test_celery_hour_matching(self):
        """Test how Celery matches hours for sending reminders"""
        print(f"\n{Colors.YELLOW}Testing Celery Hour Matching Logic{Colors.RESET}")
        
        if not BACKEND_AVAILABLE:
            return
        
        with app.app_context():
            current_utc = datetime.utcnow()
            print(f"Current UTC time: {current_utc}")
            print(f"Current UTC hour: {current_utc.hour}")
            
            # Query reminders for current hour
            current_hour_reminders = Reminder.query.filter(
                Reminder.reminder_type == 'daily_checkin',
                Reminder.is_active == True,
                db.extract('hour', Reminder.reminder_time) == current_utc.hour
            ).all()
            
            print(f"\nReminders scheduled for current hour ({current_utc.hour}:00 UTC):")
            print(f"Found {len(current_hour_reminders)} reminders")
            
            for reminder in current_hour_reminders[:3]:  # Show first 3
                client = Client.query.get(reminder.client_id)
                if client:
                    print(f"  - Client {client.serial}: {reminder.local_reminder_time}")
    
    def test_common_issues(self):
        """Check for common timezone-related issues"""
        print(f"\n{Colors.YELLOW}Analyzing Common Reminder Issues{Colors.RESET}")
        
        if not BACKEND_AVAILABLE:
            return
        
        with app.app_context():
            # Check for NULL local_reminder_time
            null_local_time = Reminder.query.filter(
                Reminder.reminder_type == 'daily_checkin',
                Reminder.is_active == True,
                Reminder.local_reminder_time == None
            ).count()
            
            if null_local_time > 0:
                print(f"{Colors.RED}✗ Found {null_local_time} reminders with NULL local_reminder_time{Colors.RESET}")
            else:
                print(f"{Colors.GREEN}✓ All reminders have local_reminder_time{Colors.RESET}")
            
            # Check for duplicate reminders
            duplicate_check = db.session.execute(db.text("""
                SELECT client_id, COUNT(*) as count
                FROM reminders
                WHERE reminder_type = 'daily_checkin' 
                AND is_active = true
                GROUP BY client_id
                HAVING COUNT(*) > 1
            """))
            
            duplicates = duplicate_check.fetchall()
            if duplicates:
                print(f"{Colors.RED}✗ Found clients with duplicate active reminders:{Colors.RESET}")
                for client_id, count in duplicates:
                    print(f"    Client {client_id}: {count} active reminders")
            else:
                print(f"{Colors.GREEN}✓ No duplicate reminders found{Colors.RESET}")
    
    def check_reminder_distribution(self):
        """Check distribution of reminders across hours"""
        print(f"\n{Colors.YELLOW}Checking Reminder Distribution{Colors.RESET}")
        
        if not BACKEND_AVAILABLE:
            return
        
        with app.app_context():
            # Get distribution by hour
            distribution = db.session.execute(db.text("""
                SELECT EXTRACT(hour FROM reminder_time) as hour, COUNT(*) as count
                FROM reminders
                WHERE reminder_type = 'daily_checkin' 
                AND is_active = true
                GROUP BY hour
                ORDER BY hour
            """))
            
            print("\nReminder distribution by UTC hour:")
            hour_counts = []
            for hour, count in distribution:
                if hour is not None:
                    hour_counts.append((int(hour), count))
                    bar = '█' * min(count, 20)
                    print(f"  {int(hour):02d}:00 UTC: {bar} ({count})")
            
            if hour_counts:
                peak_hour = max(hour_counts, key=lambda x: x[1])
                print(f"\nPeak hour: {peak_hour[0]:02d}:00 UTC with {peak_hour[1]} reminders")
    
    def generate_fix_sql(self):
        """Generate SQL to fix common issues"""
        print(f"\n{Colors.YELLOW}Generating Fix Script{Colors.RESET}")
        
        sql_fixes = """
-- Fix missing local_reminder_time values
-- This assumes reminders were created in Jerusalem time (UTC+2/+3)
UPDATE reminders 
SET local_reminder_time = 
    CASE 
        WHEN EXTRACT(hour FROM reminder_time) >= 21 THEN 
            LPAD(((EXTRACT(hour FROM reminder_time) + 3) % 24)::text, 2, '0') || ':' || 
            LPAD(EXTRACT(minute FROM reminder_time)::text, 2, '0')
        ELSE 
            LPAD((EXTRACT(hour FROM reminder_time) + 3)::text, 2, '0') || ':' || 
            LPAD(EXTRACT(minute FROM reminder_time)::text, 2, '0')
    END
WHERE local_reminder_time IS NULL 
  AND reminder_type = 'daily_checkin';

-- Remove duplicate reminders (keep the most recent)
DELETE FROM reminders r1
WHERE r1.id NOT IN (
    SELECT MAX(id)
    FROM reminders r2
    WHERE r2.client_id = r1.client_id
      AND r2.reminder_type = 'daily_checkin'
      AND r2.is_active = true
    GROUP BY r2.client_id
)
AND r1.reminder_type = 'daily_checkin'
AND r1.is_active = true;

-- Check and reset circuit breaker if needed
UPDATE circuit_breaker_state
SET is_open = false, failure_count = 0
WHERE service = 'email' AND is_open = true;
"""
        
        print(f"\n{Colors.CYAN}SQL Fix Script:{Colors.RESET}")
        print("=" * 60)
        print(sql_fixes)
        print("=" * 60)
        print(f"\n{Colors.YELLOW}Note: Review and test these queries before running in production!{Colors.RESET}")
    
    def run_all_tests(self):
        """Run all database timezone tests"""
        self.print_header("DATABASE TIMEZONE TESTS")
        
        if not BACKEND_AVAILABLE:
            print(f"{Colors.RED}Cannot run database tests - backend not available{Colors.RESET}")
            print("Make sure new_backend.py and its dependencies are available")
            return
        
        self.test_database_timezone()
        self.test_reminder_storage()
        self.test_timezone_conversion()
        self.test_celery_hour_matching()
        self.test_common_issues()
        self.check_reminder_distribution()
        self.generate_fix_sql()

if __name__ == "__main__":
    tester = DatabaseTimezoneTester()
    tester.run_all_tests()