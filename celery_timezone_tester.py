#!/usr/bin/env python3
"""
Test Celery worker timezone handling and email sending logic.
Modified to work without external dependencies.
"""

import os
import sys
from datetime import datetime, timedelta
from datetime import time as datetime_time  # Rename to avoid conflict
import time  # Import time module for sleep if needed
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from existing app
try:
    from celery_app import celery, send_daily_reminders, send_reminder_email
    from new_backend import app, db, Client, Reminder, User, CircuitBreakerState
    CELERY_AVAILABLE = True
except ImportError as e:
    CELERY_AVAILABLE = False
    print(f"Warning: Could not import celery components: {e}")

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

class CeleryTimezoneTester:
    """Test Celery timezone handling"""
    
    def __init__(self):
        self.test_results = []
        
    def print_header(self, text):
        """Print a formatted header"""
        print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.CYAN}{text.center(60)}{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")
    
    def test_celery_config(self):
        """Test Celery configuration"""
        print(f"{Colors.YELLOW}Testing Celery Configuration{Colors.RESET}")
        
        if not CELERY_AVAILABLE:
            print(f"{Colors.RED}Celery not available - skipping tests{Colors.RESET}")
            return
        
        # Check timezone configuration
        print(f"\nCelery Configuration:")
        print(f"  Timezone: {celery.conf.timezone}")
        print(f"  Enable UTC: {celery.conf.enable_utc}")
        
        if celery.conf.timezone == 'UTC':
            print(f"  {Colors.GREEN}✓ Celery correctly using UTC{Colors.RESET}")
        else:
            print(f"  {Colors.RED}✗ Celery NOT using UTC{Colors.RESET}")
        
        if celery.conf.enable_utc:
            print(f"  {Colors.GREEN}✓ UTC is enabled{Colors.RESET}")
        else:
            print(f"  {Colors.RED}✗ UTC is NOT enabled{Colors.RESET}")
        
        # Check beat schedule
        if hasattr(celery.conf, 'beat_schedule'):
            print(f"\nDaily reminder schedule:")
            for task_name, schedule in celery.conf.beat_schedule.items():
                if 'daily_reminders' in task_name:
                    print(f"  Task: {schedule['task']}")
                    print(f"  Schedule: Every {schedule['schedule'].seconds} seconds")
                    if schedule['schedule'].seconds == 3600:
                        print(f"  {Colors.GREEN}✓ Running every hour as expected{Colors.RESET}")
                    else:
                        print(f"  {Colors.YELLOW}⚠ Not running hourly{Colors.RESET}")
    
    def test_worker_status(self):
        """Test Celery worker status"""
        print(f"\n{Colors.YELLOW}Testing Celery Worker Status{Colors.RESET}")
        
        if not CELERY_AVAILABLE:
            return
        
        try:
            # Get active workers
            inspect = celery.control.inspect()
            active_workers = inspect.active()
            
            if active_workers:
                print(f"{Colors.GREEN}✓ Found {len(active_workers)} active worker(s){Colors.RESET}")
                for worker, tasks in active_workers.items():
                    print(f"\nWorker: {worker}")
                    print(f"  Total tasks: {len(tasks) if tasks else 0}")
                    
                    # Get stats
                    stats = inspect.stats()
                    if stats and worker in stats:
                        worker_stats = stats[worker]
                        print(f"  Active tasks: {worker_stats.get('total', {}).get('active', 0)}")
                        print(f"  Scheduled tasks: {worker_stats.get('total', {}).get('scheduled', 0)}")
            else:
                print(f"{Colors.RED}✗ No active workers found{Colors.RESET}")
                print(f"  Start worker with: celery -A celery_app worker --loglevel=info")
        except Exception as e:
            print(f"{Colors.RED}Could not inspect workers: {e}{Colors.RESET}")
    
    def test_reminder_task_logic(self):
        """Test the reminder sending logic"""
        print(f"\n{Colors.YELLOW}Testing Reminder Task Logic{Colors.RESET}")
        
        if not CELERY_AVAILABLE:
            return
        
        with app.app_context():
            current_utc = datetime.utcnow()
            print(f"\nCurrent UTC time: {current_utc}")
            print(f"Current UTC hour: {current_utc.hour}")
            
            # Test hour extraction
            print(f"\nTesting hour extraction for different times:")
            test_times = [
                datetime_time(9, 0),
                datetime_time(14, 30),
                datetime_time(23, 45),
                datetime_time(0, 15)
            ]
            
            for test_time in test_times:
                hour = test_time.hour
                print(f"  Time {test_time}: Hour = {hour}")
    
    def test_email_circuit_breaker(self):
        """Test email circuit breaker status"""
        print(f"\n{Colors.YELLOW}Testing Email Circuit Breaker{Colors.RESET}")
        
        if not CELERY_AVAILABLE:
            return
        
        with app.app_context():
            breaker = CircuitBreakerState.query.filter_by(service='email').first()
            
            if breaker:
                print(f"\nEmail Circuit Breaker Status:")
                print(f"  Failure count: {breaker.failure_count}")
                print(f"  Last failure: {breaker.last_failure_time}")
                print(f"  Is open: {breaker.is_open}")
                
                if breaker.is_open:
                    print(f"  {Colors.RED}✗ Circuit breaker is OPEN - emails blocked{Colors.RESET}")
                else:
                    print(f"  {Colors.GREEN}✓ Circuit breaker is closed - emails can be sent{Colors.RESET}")
            else:
                print(f"  {Colors.GREEN}✓ No circuit breaker record - system ready{Colors.RESET}")
    
    def test_email_config(self):
        """Check email configuration"""
        print(f"\n{Colors.YELLOW}Checking Email Configuration{Colors.RESET}")
        
        email_config = {
            'SMTP Server': os.environ.get('EMAIL_HOST', 'Not set'),
            'SMTP Port': os.environ.get('EMAIL_PORT', 'Not set'),
            'System Email': os.environ.get('SYSTEM_EMAIL', 'Not set'),
            'Password Set': 'Yes' if os.environ.get('EMAIL_PASSWORD') else 'No'
        }
        
        print("\nEmail Configuration:")
        for key, value in email_config.items():
            print(f"  {key}: {value}")
        
        if all(v != 'Not set' for v in [email_config['SMTP Server'], 
                                         email_config['SMTP Port'], 
                                         email_config['System Email']]):
            print(f"\n{Colors.GREEN}✓ Email appears to be configured{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}✗ Email configuration incomplete{Colors.RESET}")
    
    def simulate_reminder_sending(self, target_hour=None):
        """Simulate the reminder sending process"""
        print(f"\n{Colors.YELLOW}Simulating Reminder Sending Process{Colors.RESET}")
        
        if not CELERY_AVAILABLE:
            return
        
        with app.app_context():
            if target_hour is None:
                target_hour = datetime.utcnow().hour
            
            print(f"\nSimulating for hour: {target_hour}:00 UTC")
            
            # Query reminders for the target hour
            reminders = Reminder.query.filter(
                Reminder.reminder_type == 'daily_checkin',
                Reminder.is_active == True,
                db.extract('hour', Reminder.reminder_time) == target_hour
            ).all()
            
            print(f"Found {len(reminders)} reminders for hour {target_hour}")
            
            would_send = 0
            would_skip = 0
            errors = 0
            
            for reminder in reminders:
                client = Client.query.get(reminder.client_id)
                if not client:
                    errors += 1
                    continue
                
                # Check if already sent today
                if reminder.last_sent:
                    if reminder.last_sent.date() == datetime.utcnow().date():
                        would_skip += 1
                        continue
                
                would_send += 1
            
            print(f"\nSummary:")
            print(f"  Would send: {would_send}")
            print(f"  Would skip: {would_skip}")
            print(f"  Errors: {errors}")
    
    def test_timezone_edge_cases(self):
        """Test edge cases in timezone handling"""
        print(f"\n{Colors.YELLOW}Testing Timezone Edge Cases{Colors.RESET}")
        
        edge_cases = [
            ("Midnight local time", "00:00", 180),  # UTC-3
            ("Midnight PDT", "00:00", 420),  # UTC-7
            ("Near day boundary", "23:45", -660),  # UTC+11
            ("DST transition", "02:00", 60),  # UTC-1
        ]
        
        for name, local_time, offset in edge_cases:
            print(f"\nTesting: {name}")
            print(f"  Local time: {local_time}")
            print(f"  Offset: {offset} minutes")
            
            # Calculate UTC
            hour, minute = map(int, local_time.split(':'))
            local_minutes = hour * 60 + minute
            utc_minutes = (local_minutes - offset) % (24 * 60)
            utc_hour = utc_minutes // 60
            utc_minute = utc_minutes % 60
            
            print(f"  UTC time: {utc_hour:02d}:{utc_minute:02d}")
    
    def print_monitoring_commands(self):
        """Print useful monitoring commands"""
        print(f"\n{Colors.CYAN}Monitoring Commands{Colors.RESET}")
        
        commands = [
            ("Check Celery workers", "celery -A celery_app inspect active"),
            ("Check scheduled tasks", "celery -A celery_app inspect scheduled"),
            ("Monitor Celery in real-time", "celery -A celery_app events"),
            ("Start worker if not running", "celery -A celery_app worker --loglevel=info"),
            ("Start beat scheduler if not running", "celery -A celery_app beat --loglevel=info"),
            ("Check Redis (if using Redis as broker)", "redis-cli ping"),
        ]
        
        for i, (desc, cmd) in enumerate(commands, 1):
            print(f"\n{i}. {desc}:")
            print(f"   {Colors.YELLOW}{cmd}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}Note: Run worker and beat in separate terminals or use supervisor{Colors.RESET}")
    
    def run_all_tests(self):
        """Run all Celery timezone tests"""
        self.print_header("CELERY TIMEZONE TESTS")
        
        if not CELERY_AVAILABLE:
            print(f"{Colors.RED}Cannot run Celery tests - Celery not available{Colors.RESET}")
            print("Make sure celery_app.py and its dependencies are available")
            return
        
        self.test_celery_config()
        self.test_worker_status()
        self.test_reminder_task_logic()
        self.test_email_circuit_breaker()
        self.test_email_config()
        self.simulate_reminder_sending()
        self.test_timezone_edge_cases()
        self.print_monitoring_commands()

if __name__ == "__main__":
    tester = CeleryTimezoneTester()
    tester.run_all_tests()