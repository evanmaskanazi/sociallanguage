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
    # This would need access to your database models
    # You'd typically import your Flask app context here
    # For now, this is a placeholder
    return {'message': 'Daily reminders task placeholder'}

@celery.task
def send_single_reminder(client_id, reminder_type):
    """Send a single reminder to a specific client"""
    # Placeholder for sending individual reminders
    return {'message': f'Reminder sent to client {client_id}'}