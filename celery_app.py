"""
Celery configuration and tasks for Therapeutic Companion
"""
import os
from celery import Celery
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Celery
celery = Celery(
    'therapy_companion',
    broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
)

# Celery configuration
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'send-daily-reminders': {
            'task': 'celery_app.send_daily_reminders',
            'schedule': 3600.0,  # Run every hour
        },
    }
)

@celery.task
def send_reminder_test(email):
    """Test task to send a reminder email"""
    try:
        # Email configuration from environment
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SYSTEM_EMAIL')
        smtp_password = os.environ.get('SYSTEM_EMAIL_PASSWORD')

        if not smtp_username or not smtp_password:
            return {'error': 'Email configuration missing'}

        # Create email
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = 'Celery Test - Therapeutic Companion'

        body = """
        This is a test email from the Therapeutic Companion Celery worker.

        If you're receiving this, it means the background task system is working correctly!

        Best regards,
        Therapeutic Companion Team
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()

        return {'success': True, 'message': f'Test email sent to {email}'}

    except Exception as e:
        return {'error': str(e)}


@celery.task
def send_daily_reminders():
    """Send daily reminder emails to all clients with active reminders"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from new_backend import app, db, Client, Reminder, send_single_reminder_email_sync, User
    from datetime import datetime
    import pytz

    with app.app_context():
        try:
            # Get current UTC time and hour
            utc_now = datetime.utcnow()
            current_utc_hour = utc_now.hour

            print(f"[PRODUCTION] Running send_daily_reminders at {utc_now} UTC (hour: {current_utc_hour})")

            # Find all active reminders for this UTC hour
            reminders = db.session.query(Reminder).join(Client).filter(
                Reminder.is_active == True,
                Reminder.reminder_type == 'daily_checkin',
                db.extract('hour', Reminder.reminder_time) == current_utc_hour
            ).all()

            print(f"[PRODUCTION] Found {len(reminders)} reminders for UTC hour {current_utc_hour}")

            sent_count = 0
            failed_count = 0

            for reminder in reminders:
                try:
                    # Send reminder to this client
                    client = reminder.client
                    if client and client.user and client.user.email:
                        # Determine which email to use
                        email_to_use = reminder.reminder_email if reminder.reminder_email else client.user.email

                        # Skip test emails
                        if (email_to_use.endswith('example.com') or
                                email_to_use.endswith('test.test') or
                                email_to_use == 'test@test.test'):
                            print(f"[PRODUCTION] Skipping test email: {email_to_use}")
                            continue

                        print(f"[PRODUCTION] Sending reminder to {client.user.email} (Client: {client.client_serial})")

                        # Check if we've sent recently (to avoid duplicates)
                        if reminder.last_sent:
                            minutes_since = (utc_now - reminder.last_sent).total_seconds() / 60
                            if minutes_since < 30:  # Don't send if sent in last 30 minutes
                                print(
                                    f"[PRODUCTION] Skipping {client.user.email} - sent {minutes_since:.1f} minutes ago")
                                continue

                        # Send the email
                        result = send_single_reminder_email_sync(client)

                        # Update last_sent
                        reminder.last_sent = utc_now
                        sent_count += 1
                        print(f"[PRODUCTION] Successfully sent to {client.user.email}")

                except Exception as e:
                    failed_count += 1
                    print(f"[PRODUCTION] Failed to send to client {reminder.client.client_serial}: {e}")
                    app.logger.error(f"Failed to send reminder to client {reminder.client.client_serial}: {e}")

            db.session.commit()

            result_message = f'[PRODUCTION] Sent {sent_count} daily reminders, {failed_count} failed'
            print(result_message)

            # Also log all active reminders for debugging
            if sent_count == 0:
                all_active = db.session.query(Reminder).filter(
                    Reminder.is_active == True,
                    Reminder.reminder_type == 'daily_checkin'
                ).all()
                print(f"[PRODUCTION] Total active reminders in system: {len(all_active)}")
                for r in all_active[:5]:  # Show first 5
                    print(
                        f"  - Client {r.client.client_serial}: reminder at {r.reminder_time} (hour: {r.reminder_time.hour})")

            return {'message': result_message}

        except Exception as e:
            print(f"[PRODUCTION] Error: {str(e)}")
            return {'error': str(e)}

@celery.task
def send_single_reminder(client_id, reminder_type):
    """Send a single reminder to a specific client"""
    # Placeholder for sending individual reminders
    return {'message': f'Reminder sent to client {client_id}'}


@celery.task
def check_inactive_clients():
    """Check for inactive clients and notify therapists"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from new_backend import check_client_inactivity

    try:
        count = check_client_inactivity()
        return {'success': True, 'notifications_sent': count}
    except Exception as e:
        return {'error': str(e)}