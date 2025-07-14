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
            'schedule': 60.0,  # Run every minute
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

    with app.app_context():
        try:
            current_hour = datetime.now().hour
            print(f"[TESTING MODE] Running send_daily_reminders at {datetime.now()}")

            # TESTING MODE: Send to ALL active clients, not just those with reminders
            all_active_clients = db.session.query(Client).join(User).filter(
                Client.is_active == True,
                User.is_active == True,
                User.email.isnot(None),
                # Skip test emails - check for multiple patterns
                ~User.email.endswith('example.com'),
                ~User.email.endswith('test.test'),
                User.email != 'test@test.test'
            ).all()

            print(f"[TESTING MODE] Found {len(all_active_clients)} active clients with real emails")

            sent_count = 0
            failed_count = 0

            for client in all_active_clients:
                try:
                    if client.user and client.user.email:
                        print(
                            f"[TESTING MODE] Sending reminder to {client.user.email} (Client: {client.client_serial})")

                        # Check if we've sent recently (to avoid spam)
                        reminder = Reminder.query.filter_by(
                            client_id=client.id,
                            reminder_type='daily_checkin'
                        ).first()

                        if reminder and reminder.last_sent:
                            minutes_since = (datetime.utcnow() - reminder.last_sent).total_seconds() / 60
                            if minutes_since < 2:
                                print(
                                    f"[TESTING MODE] Skipping {client.user.email} - sent {minutes_since:.1f} minutes ago")
                                continue

                        # Send the email
                        result = send_single_reminder_email_sync(client)

                        # Update last_sent if reminder exists
                        if reminder:
                            reminder.last_sent = datetime.utcnow()

                        sent_count += 1
                        print(f"[TESTING MODE] Successfully sent to {client.user.email}")
                except Exception as e:
                    failed_count += 1
                    print(f"[TESTING MODE] Failed to send to client {client.client_serial}: {e}")
                    app.logger.error(f"Failed to send reminder to client {client.client_serial}: {e}")

            db.session.commit()

            result_message = f'[TESTING MODE] Sent {sent_count} reminders to real emails, {failed_count} failed'
            print(result_message)
            return {'message': result_message}

        except Exception as e:
            print(f"[TESTING MODE] Error: {str(e)}")
            return {'error': str(e)}


@celery.task
def send_single_reminder(client_id, reminder_type):
    """Send a single reminder to a specific client"""
    # Placeholder for sending individual reminders
    return {'message': f'Reminder sent to client {client_id}'}
