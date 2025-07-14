
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

    from new_backend import app, db, Client, Reminder, send_single_reminder_email_sync
    from datetime import datetime

    with app.app_context():
        try:
            current_hour = datetime.now().hour
            print(f"[TESTING MODE] Running send_daily_reminders at {datetime.now()}")

            # TESTING MODE: Get ALL active reminders, regardless of scheduled time
            # Original line commented out:
            # reminders = db.session.query(Reminder).join(Client).filter(
            #     Reminder.is_active == True,
            #     Reminder.reminder_type == 'daily_checkin',
            #     db.extract('hour', Reminder.reminder_time) == current_hour
            # ).all()
            
            # TESTING: Get ALL active reminders
            reminders = db.session.query(Reminder).join(Client).filter(
                Reminder.is_active == True,
                Reminder.reminder_type == 'daily_checkin'
            ).all()

            print(f"[TESTING MODE] Found {len(reminders)} active reminders (sending to all regardless of scheduled time)")

            sent_count = 0
            for reminder in reminders:
                try:
                    # Send reminder to this client
                    client = reminder.client
                    if client and client.user and client.user.email:
                        print(f"[TESTING MODE] Sending reminder to {client.user.email} (Client: {client.client_serial})")
                        # Use the existing send function
                        send_single_reminder_email_sync(client)
                        reminder.last_sent = datetime.utcnow()
                        sent_count += 1
                        print(f"[TESTING MODE] Successfully sent to {client.user.email}")
                except Exception as e:
                    print(f"[TESTING MODE] Failed to send to client {client.client_serial}: {e}")
                    app.logger.error(f"Failed to send reminder to client {client.client_serial}: {e}")

            db.session.commit()
            
            result_message = f'[TESTING MODE] Sent {sent_count} reminders (out of {len(reminders)} active)'
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
