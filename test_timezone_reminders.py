#!/usr/bin/env python3
"""
Comprehensive timezone testing for Therapy Companion reminder system.
Tests current and future clients across multiple timezones.
Modified to work without external dependencies - uses only stdlib and existing packages.
"""

import os
import sys
import json
import random
import time  # Import time module for sleep
import traceback
from datetime import datetime, timedelta
from datetime import time as datetime_time  # Rename to avoid conflict
import urllib.request
import urllib.parse
import urllib.error
import ssl

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from existing app
try:
    from new_backend import app, db, Client, Reminder, User, generate_client_serial
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    print("Warning: Could not import from new_backend. Some tests will be limited.")

# Color codes for terminal output (using ANSI escape codes)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# Configuration
BASE_URL = os.environ.get('APP_BASE_URL', 'https://therapy-companion.onrender.com')
TEST_THERAPIST_EMAIL = os.environ.get('TEST_THERAPIST_EMAIL', 'test_therapist@example.com')
TEST_THERAPIST_PASSWORD = os.environ.get('TEST_THERAPIST_PASSWORD', 'testpass123')

# Debug configuration
DEBUG_MODE = os.environ.get('DEBUG_MODE', '1') == '1'
REQUEST_DELAY = float(os.environ.get('REQUEST_DELAY', '1.0'))  # Delay between requests to avoid rate limiting

# Common timezones for testing with their offsets
TIMEZONE_DATA = {
    'Asia/Jerusalem': {'offset': -180, 'name': 'Jerusalem (UTC+3)'},  # UTC+3 in summer
    'America/Los_Angeles': {'offset': 420, 'name': 'PDT (UTC-7)'},   # UTC-7 in summer
    'America/New_York': {'offset': 240, 'name': 'EDT (UTC-4)'},      # UTC-4 in summer
    'Europe/London': {'offset': -60, 'name': 'BST (UTC+1)'},         # UTC+1 in summer
    'Asia/Tokyo': {'offset': -540, 'name': 'JST (UTC+9)'},           # UTC+9 no DST
    'Australia/Sydney': {'offset': -660, 'name': 'AEDT (UTC+11)'},   # UTC+11 in summer
    'America/Sao_Paulo': {'offset': 180, 'name': 'BRT (UTC-3)'},     # UTC-3
    'Asia/Kolkata': {'offset': -330, 'name': 'IST (UTC+5:30)'},      # UTC+5:30
    'Europe/Berlin': {'offset': -120, 'name': 'CEST (UTC+2)'},       # UTC+2 in summer
    'Pacific/Auckland': {'offset': -780, 'name': 'NZDT (UTC+13)'},   # UTC+13 in summer
    'America/Chicago': {'offset': 300, 'name': 'CDT (UTC-5)'},       # UTC-5 in summer
    'Asia/Dubai': {'offset': -240, 'name': 'GST (UTC+4)'},           # UTC+4 no DST
}

class TestResult:
    """Store test results with details"""
    def __init__(self, name, passed, message, details=None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.utcnow()

class TimezoneReminderTester:
    """Main test class for timezone reminder functionality"""
    
    def __init__(self):
        self.results = []
        self.therapist_token = None
        self.test_clients = {}
        self.csrf_token = None
        self.request_count = 0
        # Create SSL context that doesn't verify certificates (for testing)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        # Verify BASE_URL
        print(f"{Colors.CYAN}Configuration:{Colors.RESET}")
        print(f"  Base URL: {BASE_URL}")
        print(f"  Debug Mode: {DEBUG_MODE}")
        print(f"  Request Delay: {REQUEST_DELAY}s")
        print()
        
    def print_header(self, text):
        """Print a formatted header"""
        print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.CYAN}{text.center(60)}{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")
    
    def print_test_result(self, result):
        """Print a single test result with color coding"""
        if result.passed:
            status = f"{Colors.GREEN}✓ PASS{Colors.RESET}"
        else:
            status = f"{Colors.RED}✗ FAIL{Colors.RESET}"
        
        print(f"{status} {result.name}")
        print(f"  {Colors.YELLOW}→{Colors.RESET} {result.message}")
        
        if result.details:
            for key, value in result.details.items():
                if key != 'error_details':  # Handle error_details separately
                    print(f"    {Colors.BLUE}{key}:{Colors.RESET} {value}")
        
        if not result.passed and 'error_details' in result.details:
            print(f"    {Colors.RED}Error Details:{Colors.RESET}")
            for line in result.details['error_details'].split('\n'):
                if line.strip():
                    print(f"      {line}")
    
    def get_csrf_token(self):
        """Get CSRF token from the server"""
        try:
            if DEBUG_MODE:
                print(f"{Colors.YELLOW}Getting CSRF token...{Colors.RESET}")
            
            response = self.make_request('GET', f"{BASE_URL}/api/csrf-token", skip_csrf=True)
            if response['status_code'] == 200:
                self.csrf_token = response['data'].get('csrf_token')
                if DEBUG_MODE:
                    print(f"{Colors.GREEN}Got CSRF token: {self.csrf_token[:20]}...{Colors.RESET}")
                return self.csrf_token
        except Exception as e:
            if DEBUG_MODE:
                print(f"{Colors.RED}Failed to get CSRF token: {e}{Colors.RESET}")
        return None
    
    def make_request(self, method, url, data=None, headers=None, skip_csrf=False):
        """Make HTTP request using urllib with proper error handling and debugging"""
        headers = headers or {}
        self.request_count += 1
        
        # Add rate limiting delay
        if self.request_count > 1:
            time.sleep(REQUEST_DELAY)
        
        # Add CSRF token for state-changing operations
        if not skip_csrf and method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if not self.csrf_token:
                self.get_csrf_token()
            if self.csrf_token:
                headers['X-CSRF-Token'] = self.csrf_token
        
        if data and method in ['POST', 'PUT', 'PATCH']:
            data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        
        if DEBUG_MODE:
            print(f"\n{Colors.BLUE}Request #{self.request_count}:{Colors.RESET}")
            print(f"  Method: {method}")
            print(f"  URL: {url}")
            if data:
                print(f"  Data: {data.decode('utf-8') if isinstance(data, bytes) else data}")
            print(f"  Headers: {headers}")
        
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        try:
            response = urllib.request.urlopen(request, context=self.ssl_context)
            response_data = response.read().decode('utf-8')
            
            if DEBUG_MODE:
                print(f"{Colors.GREEN}Response Status: {response.getcode()}{Colors.RESET}")
                print(f"Response Headers: {dict(response.headers)}")
            
            # Try to parse as JSON
            try:
                json_data = json.loads(response_data)
                if DEBUG_MODE:
                    print(f"Response Data: {json.dumps(json_data, indent=2)[:500]}...")
                
                return {
                    'status_code': response.getcode(),
                    'data': json_data,
                    'headers': dict(response.headers)
                }
            except json.JSONDecodeError:
                if DEBUG_MODE:
                    print(f"{Colors.YELLOW}Non-JSON response received:{Colors.RESET}")
                    print(f"Raw response: {response_data[:500]}...")
                
                # Check if it's HTML (common error response)
                if response_data.strip().startswith('<'):
                    print(f"{Colors.RED}Received HTML response instead of JSON - likely an error page{Colors.RESET}")
                
                return {
                    'status_code': response.getcode(),
                    'data': {},
                    'raw': response_data,
                    'error': 'Non-JSON response'
                }
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            
            if DEBUG_MODE:
                print(f"{Colors.RED}HTTP Error {e.code}: {e.reason}{Colors.RESET}")
            
            try:
                error_data = json.loads(error_body) if error_body else {}
                if DEBUG_MODE:
                    print(f"Error Data: {json.dumps(error_data, indent=2)}")
            except:
                if DEBUG_MODE:
                    print(f"Non-JSON error response: {error_body[:500]}...")
                error_data = {'error': error_body}
            
            return {
                'status_code': e.code,
                'data': error_data,
                'error': str(e)
            }
        except Exception as e:
            if DEBUG_MODE:
                print(f"{Colors.RED}Request Exception: {type(e).__name__}: {e}{Colors.RESET}")
                traceback.print_exc()
            
            return {
                'status_code': 0,
                'error': str(e),
                'exception_type': type(e).__name__
            }
    
    def setup_test_therapist(self):
        """Setup or login test therapist account with full debugging"""
        try:
            login_url = f"{BASE_URL}/api/auth/login"
            print(f"{Colors.YELLOW}Attempting login at: {login_url}{Colors.RESET}")
            
            # Try to login first - skip CSRF since login is exempt
            response = self.make_request(
                'POST',
                login_url,
                {'email': TEST_THERAPIST_EMAIL, 'password': TEST_THERAPIST_PASSWORD},
                skip_csrf=True
            )
            
            if response['status_code'] == 200 and 'token' in response.get('data', {}):
                self.therapist_token = response['data']['token']
                print(f"{Colors.GREEN}✓ Successfully logged in as therapist{Colors.RESET}")
                return True
            
            # Check for rate limiting
            if response['status_code'] == 429:
                print(f"{Colors.RED}Rate limited! Waiting 60 seconds...{Colors.RESET}")
                time.sleep(60)
                # Retry once
                response = self.make_request(
                    'POST',
                    login_url,
                    {'email': TEST_THERAPIST_EMAIL, 'password': TEST_THERAPIST_PASSWORD},
                    skip_csrf=True
                )
                if response['status_code'] == 200:
                    self.therapist_token = response['data']['token']
                    return True
            
            # If login fails with 401, try to register
            if response['status_code'] == 401:
                print(f"{Colors.YELLOW}Login failed with 401, attempting registration...{Colors.RESET}")
                time.sleep(2)  # Wait to avoid rate limiting
                
                # Generate unique license number
                unique_license = f'TEST{int(datetime.utcnow().timestamp())}'
                
                response = self.make_request(
                    'POST',
                    f"{BASE_URL}/api/auth/register",
                    {
                        'email': TEST_THERAPIST_EMAIL,
                        'password': TEST_THERAPIST_PASSWORD,
                        'role': 'therapist',
                        'name': 'Test Therapist',
                        'license_number': unique_license,
                        'organization': 'Test Organization'
                    },
                    skip_csrf=True  # Register might also be exempt
                )
                
                if response['status_code'] in [200, 201] and 'token' in response.get('data', {}):
                    self.therapist_token = response['data']['token']
                    print(f"{Colors.GREEN}✓ Successfully registered new therapist{Colors.RESET}")
                    return True
            
            # If we get here, both login and register failed
            print(f"{Colors.RED}Both login and registration failed{Colors.RESET}")
            if 'data' in response and 'error' in response['data']:
                print(f"{Colors.RED}Server error: {response['data']['error']}{Colors.RESET}")
            
            return False
            
        except Exception as e:
            print(f"{Colors.RED}Failed to setup therapist: {e}{Colors.RESET}")
            traceback.print_exc()
            return False
    
    def create_test_client(self, timezone):
        """Create a test client for a specific timezone"""
        try:
            email = f"test_client_{timezone.replace('/', '_')}_{datetime.utcnow().timestamp():.0f}@test.com"
            
            print(f"{Colors.YELLOW}Creating client for {timezone}...{Colors.RESET}")
            
            response = self.make_request(
                'POST',
                f"{BASE_URL}/api/therapist/create-client",
                {'email': email, 'password': 'testpass123'},
                {'Authorization': f'Bearer {self.therapist_token}'}
            )
            
            if response['status_code'] in [200, 201]:
                client_data = response['data']['client']
                
                # Add delay before login to avoid rate limiting
                time.sleep(REQUEST_DELAY)
                
                # Login as the client to get their token - skip CSRF
                login_response = self.make_request(
                    'POST',
                    f"{BASE_URL}/api/auth/login",
                    {'email': email, 'password': 'testpass123'},
                    skip_csrf=True
                )
                
                if login_response['status_code'] == 200:
                    client_data['token'] = login_response['data']['token']
                    client_data['timezone'] = timezone
                    print(f"{Colors.GREEN}✓ Client created: {client_data['serial']}{Colors.RESET}")
                    return client_data
                else:
                    print(f"{Colors.RED}Failed to login as client{Colors.RESET}")
            else:
                print(f"{Colors.RED}Failed to create client: {response.get('status_code')} - {response.get('data', {}).get('error', 'Unknown error')}{Colors.RESET}")
            
            return None
            
        except Exception as e:
            print(f"{Colors.RED}Failed to create client for {timezone}: {e}{Colors.RESET}")
            traceback.print_exc()
            return None
    
    def test_reminder_time_conversion(self, client_data, local_time, timezone):
        """Test if reminder time is correctly converted and stored"""
        try:
            # Get timezone offset
            tz_data = TIMEZONE_DATA.get(timezone, {'offset': 0, 'name': timezone})
            js_offset = tz_data['offset']
            
            print(f"{Colors.YELLOW}Setting reminder for {local_time} in {timezone} (offset: {js_offset} minutes){Colors.RESET}")
            
            # Set reminder
            response = self.make_request(
                'POST',
                f"{BASE_URL}/api/client/update-reminder",
                {
                    'type': 'daily_checkin',
                    'time': local_time,
                    'is_active': True,
                    'timezone_offset': js_offset
                },
                {'Authorization': f'Bearer {client_data["token"]}'}
            )
            
            if response['status_code'] != 200:
                return TestResult(
                    f"Reminder conversion for {timezone}",
                    False,
                    f"Failed to set reminder: {response['status_code']}",
                    {
                        'timezone': timezone,
                        'local_time': local_time,
                        'offset_minutes': js_offset,
                        'response': str(response.get('data', response.get('error', ''))),
                        'error_details': self._analyze_reminder_failure(response, timezone, local_time)
                    }
                )
            
            # Add delay before verification
            time.sleep(REQUEST_DELAY)
            
            # Verify the reminder was set correctly
            verify_response = self.make_request(
                'GET',
                f"{BASE_URL}/api/client/reminders",
                headers={'Authorization': f'Bearer {client_data["token"]}'}
            )
            
            if verify_response['status_code'] == 200:
                reminders = verify_response['data']['reminders']
                if reminders:
                    reminder = reminders[0]
                    
                    # Calculate expected UTC time
                    hour, minute = map(int, local_time.split(':'))
                    local_minutes = hour * 60 + minute
                    utc_minutes = (local_minutes - js_offset) % (24 * 60)
                    expected_utc_hour = utc_minutes // 60
                    expected_utc_minute = utc_minutes % 60
                    expected_utc_time = f"{expected_utc_hour:02d}:{expected_utc_minute:02d}"
                    
                    actual_utc_time = reminder.get('utc_time', reminder.get('time', ''))
                    
                    if actual_utc_time == expected_utc_time:
                        return TestResult(
                            f"Reminder conversion for {timezone}",
                            True,
                            f"Correctly converted {local_time} to UTC {actual_utc_time}",
                            {
                                'timezone': timezone,
                                'local_time': local_time,
                                'utc_time': actual_utc_time,
                                'offset_minutes': js_offset
                            }
                        )
                    else:
                        return TestResult(
                            f"Reminder conversion for {timezone}",
                            False,
                            f"UTC time mismatch: expected {expected_utc_time}, got {actual_utc_time}",
                            {
                                'timezone': timezone,
                                'local_time': local_time,
                                'expected_utc': expected_utc_time,
                                'actual_utc': actual_utc_time,
                                'offset_minutes': js_offset,
                                'error_details': self._analyze_conversion_mismatch(
                                    local_time, expected_utc_time, actual_utc_time, timezone
                                )
                            }
                        )
            
            return TestResult(
                f"Reminder conversion for {timezone}",
                False,
                "Failed to verify reminder",
                {'error_details': 'Could not retrieve reminder after setting it'}
            )
            
        except Exception as e:
            return TestResult(
                f"Reminder conversion for {timezone}",
                False,
                f"Exception occurred: {str(e)}",
                {
                    'timezone': timezone,
                    'exception': str(e),
                    'error_details': self._analyze_exception(e, 'reminder_conversion')
                }
            )
    
    def _analyze_reminder_failure(self, response, timezone, local_time):
        """Analyze why reminder setting failed"""
        analysis = []
        
        status_code = response.get('status_code', 0)
        
        if status_code == 400:
            analysis.append("Bad Request - Possible issues:")
            analysis.append("- Invalid timezone offset calculation")
            analysis.append("- Missing required fields in request")
            analysis.append("- Time format not matching expected HH:MM format")
        elif status_code == 401:
            analysis.append("Authentication failed - Token may be invalid or expired")
        elif status_code == 403:
            analysis.append("Forbidden - Possible CSRF token issue")
            analysis.append("- Ensure CSRF token is being sent correctly")
        elif status_code == 405:
            analysis.append("Method Not Allowed - Check if endpoint accepts POST")
        elif status_code == 429:
            analysis.append("Rate Limited - Too many requests")
            analysis.append("- Increase REQUEST_DELAY environment variable")
        elif status_code == 500:
            analysis.append("Server error - Possible issues:")
            analysis.append("- Database connection problem")
            analysis.append("- Backend timezone conversion logic error")
            analysis.append("- Check new_backend.py update_reminder() function")
        
        if 'data' in response and 'error' in response['data']:
            analysis.append(f"Server error message: {response['data']['error']}")
        
        analysis.append(f"\nDebug info:")
        analysis.append(f"- Timezone: {timezone}")
        analysis.append(f"- Local time: {local_time}")
        analysis.append(f"- Status code: {status_code}")
        
        return '\n'.join(analysis)
    
    def _analyze_conversion_mismatch(self, local_time, expected_utc, actual_utc, timezone):
        """Analyze why UTC conversion didn't match expected"""
        analysis = []
        
        analysis.append("UTC Conversion Mismatch Analysis:")
        analysis.append(f"- Input local time: {local_time}")
        analysis.append(f"- Expected UTC: {expected_utc}")
        analysis.append(f"- Actual UTC: {actual_utc}")
        analysis.append(f"- Timezone: {timezone}")
        
        # Calculate the difference
        exp_h, exp_m = map(int, expected_utc.split(':'))
        act_h, act_m = map(int, actual_utc.split(':'))
        diff_minutes = (act_h * 60 + act_m) - (exp_h * 60 + exp_m)
        
        analysis.append(f"- Time difference: {diff_minutes} minutes")
        
        if abs(diff_minutes) == 60:
            analysis.append("\nPossible DST issue - the offset might be off by 1 hour")
        elif abs(diff_minutes) % 60 == 0:
            hours_off = diff_minutes // 60
            analysis.append(f"\nTime is off by exactly {hours_off} hours - likely timezone offset calculation error")
        
        analysis.append("\nPotential fixes:")
        analysis.append("1. Check timezone offset calculation in client_dashboard.html saveReminderSettings()")
        analysis.append("2. Verify backend conversion in new_backend.py update_reminder()")
        analysis.append("3. Ensure DST is properly handled for this timezone")
        analysis.append("4. Check if timezone offset sign is being applied correctly")
        
        return '\n'.join(analysis)
    
    def _analyze_exception(self, exception, context):
        """Analyze exceptions and suggest fixes"""
        analysis = []
        
        analysis.append(f"Exception in {context}:")
        analysis.append(f"Type: {type(exception).__name__}")
        analysis.append(f"Message: {str(exception)}")
        
        if "connection" in str(exception).lower():
            analysis.append("\nConnection issue detected:")
            analysis.append("- Check if the server is running")
            analysis.append("- Verify network connectivity")
            analysis.append("- Check if email circuit breaker is blocking requests")
        elif "timeout" in str(exception).lower():
            analysis.append("\nTimeout issue detected:")
            analysis.append("- Server may be overloaded")
            analysis.append("- Database queries might be slow")
            analysis.append("- Check Celery worker status")
        elif "json" in str(exception).lower():
            analysis.append("\nJSON parsing issue detected:")
            analysis.append("- Server might be returning HTML error pages")
            analysis.append("- Check if API endpoints are correct")
            analysis.append("- Verify server is running and accessible")
        
        return '\n'.join(analysis)
    
    def test_timezone_set(self, timezones, test_time="09:00"):
        """Test reminder setting for a set of timezones"""
        results = []
        
        for timezone in timezones:
            print(f"\n{Colors.YELLOW}Testing timezone: {timezone}{Colors.RESET}")
            
            # Create a client for this timezone
            client_data = self.create_test_client(timezone)
            if not client_data:
                results.append(TestResult(
                    f"Client creation for {timezone}",
                    False,
                    "Failed to create test client",
                    {'timezone': timezone}
                ))
                continue
            
            # Test reminder conversion
            result = self.test_reminder_time_conversion(client_data, test_time, timezone)
            results.append(result)
            self.print_test_result(result)
            
            # Store client for future tests
            self.test_clients[timezone] = client_data
        
        return results
    
    def run_all_tests(self):
        """Run all timezone tests"""
        self.print_header("THERAPY COMPANION TIMEZONE TESTING")
        
        # Setup therapist
        print(f"{Colors.YELLOW}Setting up test therapist...{Colors.RESET}")
        if not self.setup_test_therapist():
            print(f"{Colors.RED}Failed to setup test therapist. Cannot continue.{Colors.RESET}")
            return
        
        print(f"{Colors.GREEN}✓ Test therapist ready{Colors.RESET}")
        
        # Test 1: Jerusalem timezone (current working case)
        self.print_header("TEST 1: JERUSALEM TIMEZONE")
        jerusalem_results = self.test_timezone_set(['Asia/Jerusalem'], "10:30")
        self.results.extend(jerusalem_results)
        
        # Test 2: PDT timezone
        self.print_header("TEST 2: PDT TIMEZONE")
        pdt_results = self.test_timezone_set(['America/Los_Angeles'], "07:00")
        self.results.extend(pdt_results)
        
        # Test 3: Random 4 timezones
        self.print_header("TEST 3: RANDOM TIMEZONES")
        available_timezones = [tz for tz in TIMEZONE_DATA.keys() 
                               if tz not in ['Asia/Jerusalem', 'America/Los_Angeles']]
        random_timezones = random.sample(available_timezones, min(4, len(available_timezones)))
        random_results = self.test_timezone_set(random_timezones, "14:00")
        self.results.extend(random_results)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("TEST SUMMARY")
        
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)
        
        print(f"Total tests: {total}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
        print(f"Total API requests made: {self.request_count}")
        
        if failed > 0:
            print(f"\n{Colors.RED}FAILED TESTS:{Colors.RESET}")
            for result in self.results:
                if not result.passed:
                    print(f"\n{Colors.RED}✗ {result.name}{Colors.RESET}")
                    print(f"  {result.message}")
                    if 'error_details' in result.details:
                        print(f"  {Colors.YELLOW}Fix suggestions:{Colors.RESET}")
                        for line in result.details['error_details'].split('\n'):
                            if line.strip():
                                print(f"    {line}")
        
        # Generate fix recommendations
        if failed > 0:
            self.generate_fix_recommendations()
    
    def generate_fix_recommendations(self):
        """Generate specific fix recommendations based on failures"""
        self.print_header("RECOMMENDED FIXES")
        
        # Analyze patterns in failures
        failed_timezones = set()
        error_types = {}
        
        for result in self.results:
            if not result.passed and 'timezone' in result.details:
                failed_timezones.add(result.details['timezone'])
                error_msg = result.message
                error_types[error_msg] = error_types.get(error_msg, 0) + 1
        
        # Specific recommendations
        if len(failed_timezones) > 1:
            print(f"{Colors.YELLOW}Multiple timezone failures detected:{Colors.RESET}")
            print("This suggests a systematic issue with timezone handling.\n")
            
            print("1. Check client_dashboard.html:")
            print("   - Verify the timezone offset calculation in saveReminderSettings()")
            print("   - Ensure getTimezoneOffset() is being used correctly")
            print("   - The offset should be negated for correct UTC conversion\n")
            
            print("2. Check new_backend.py:")
            print("   - Review the update_reminder() function")
            print("   - Verify the UTC conversion logic")
            print("   - Ensure local_reminder_time is being stored correctly\n")
            
            print("3. Check database:")
            print("   - Verify reminder_time is stored as UTC")
            print("   - Ensure local_reminder_time column exists")
            print("   - Check if any timezone data is being lost\n")
            
            print("4. Check celery_app.py:")
            print("   - Verify send_daily_reminders() uses UTC correctly")
            print("   - Ensure hour matching logic is timezone-aware")

if __name__ == "__main__":
    # Allow setting debug mode from command line
    if len(sys.argv) > 1:
        if sys.argv[1] == '--debug':
            os.environ['DEBUG_MODE'] = '1'
        elif sys.argv[1] == '--no-debug':
            os.environ['DEBUG_MODE'] = '0'
    
    tester = TimezoneReminderTester()
    tester.run_all_tests()