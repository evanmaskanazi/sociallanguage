from celery import Celery
from celery.schedules import crontab
import os
from datetime import datetime, timedelta, date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create Celery instance
celery = Celery(
    'therapy_companion',
    broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
)

# Configure Celery
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Schedule periodic tasks
celery.conf.beat_schedule = {
    'send-reminders-every-30-minutes': {
        'task': 'celery_app.send_reminder_batch',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'cleanup-old-sessions-daily': {
        'task': 'celery_app.cleanup_old_sessions',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}

# Import Flask app and models
def create_app():
    from new_backend import app, db
    return app, db

@celery.task(bind=True, max_retries=3)
def send_reminder_batch(self):
    """Send reminder emails in batches"""
    app, db = create_app()
    
    with app.app_context():
        from new_backend import Reminder, Client, DailyCheckin, send_email, logger
        from sqlalchemy import or_
        
        try:
            now = datetime.now()
            current_time = now.time()
            
            # Get reminders for current 30-minute window
            time_window_start = now.time()
            time_window_end = (now + timedelta(minutes=30)).time()
            
            reminders = Reminder.query.filter(
                Reminder.is_active == True,
                Reminder.reminder_type == 'daily_checkin',
                Reminder.reminder_time.between(time_window_start, time_window_end),
                or_(
                    Reminder.last_sent == None,
                    Reminder.last_sent < datetime.now().date()
                )
            ).all()
            
            logger.info(f"Processing {len(reminders)} reminders")
            
            # Process in chunks
            chunk_size = 50
            for i in range(0, len(reminders), chunk_size):
                chunk = reminders[i:i + chunk_size]
                process_reminder_chunk.delay([r.id for r in chunk])
            
            return {'status': 'success', 'total_reminders': len(reminders)}
            
        except Exception as e:
            logger.error(f"Error in send_reminder_batch: {str(e)}")
            raise self.retry(exc=e)

@celery.task(bind=True, max_retries=3)
def process_reminder_chunk(self, reminder_ids):
    """Process a chunk of reminders"""
    app, db = create_app()
    
    with app.app_context():
        from new_backend import Reminder, DailyCheckin, send_single_reminder_email, logger
        
        sent_count = 0
        error_count = 0
        
        for reminder_id in reminder_ids:
            try:
                reminder = Reminder.query.get(reminder_id)
                if not reminder:
                    continue
                
                client = reminder.client
                if not client.is_active or not client.user.email:
                    continue
                
                # Check if already completed today
                today_checkin = client.checkins.filter_by(
                    checkin_date=date.today()
                ).first()
                
                if not today_checkin:
                    # Send reminder
                    send_single_reminder_email.delay(client.id)
                    
                    # Update last sent
                    reminder.last_sent = datetime.now()
                    db.session.commit()
                    sent_count += 1
                    
            except Exception as e:
                logger.error(f"Error processing reminder {reminder_id}: {str(e)}")
                error_count += 1
        
        return {
            'sent': sent_count,
            'errors': error_count,
            'chunk_size': len(reminder_ids)
        }

@celery.task(bind=True, max_retries=3)
def send_single_reminder_email(self, client_id):
    """Send reminder email to a single client"""
    app, db = create_app()
    
    with app.app_context():
        from new_backend import Client, send_email, logger
        import os
        
        try:
            client = Client.query.get(client_id)
            if not client:
                return {'status': 'error', 'message': 'Client not found'}
            
            base_url = os.environ.get('APP_BASE_URL', 'https://therapy-companion.onrender.com')
            
            subject = "Daily Check-in Reminder - Therapeutic Companion"
            
            body = f"""Hello,

This is your daily reminder to complete your therapy check-in.

Your therapist is tracking your progress, and your daily input is valuable for your treatment.

Click here to log in and complete today's check-in:
{base_url}/login.html

Client ID: {client.client_serial}

If you've already completed today's check-in, please disregard this message.

Best regards,
Your Therapy Team"""

            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50;">Daily Check-in Reminder</h2>
                    <p>Hello,</p>
                    <p>This is your daily reminder to complete your therapy check-in.</p>
                    <p>Your therapist is tracking your progress, and your daily input is valuable for your treatment.</p>
                    <div style="text-align: center; margin: 40px 0;">
                        <a href="{base_url}/login.html" 
                           style="background-color: #4CAF50; color: white; padding: 15px 40px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;
                                  font-weight: bold; font-size: 16px;">
                            Complete Today's Check-in
                        </a>
                    </div>
                    <p style="color: #666; font-size: 14px;">Client ID: {client.client_serial}</p>
                    <p style="color: #666; font-size: 14px;">
                        If you've already completed today's check-in, please disregard this message.
                    </p>
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    <p style="color: #999; font-size: 12px;">
                        Best regards,<br>
                        Your Therapy Team
                    </p>
                </div>
            </body>
            </html>
            """
            
            success = send_email(client.user.email, subject, body, html_body)
            
            logger.info(f"Reminder email sent to client {client_id}: {success}")
            
            return {
                'status': 'success' if success else 'error',
                'client_id': client_id,
                'email': client.user.email
            }
            
        except Exception as e:
            logger.error(f"Error sending reminder to client {client_id}: {str(e)}")
            raise self.retry(exc=e)

@celery.task
def cleanup_old_sessions():
    """Clean up old session tokens"""
    app, db = create_app()
    
    with app.app_context():
        from new_backend import SessionToken, logger
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            old_sessions = SessionToken.query.filter(
                SessionToken.created_at < cutoff_date
            ).delete()
            db.session.commit()
            
            logger.info(f"Cleaned up {old_sessions} old session tokens")
            return {'deleted': old_sessions}
            
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {str(e)}")
            db.session.rollback()
            return {'error': str(e)}

@celery.task
def send_reminder_test(email):
    """Test task to verify Celery is working"""
    app, db = create_app()
    
    with app.app_context():
        from new_backend import send_email
        
        subject = "Celery Test - Therapeutic Companion"
        body = "This is a test email to verify Celery is working correctly."
        html_body = "<p>This is a test email to verify Celery is working correctly.</p>"
        
        success = send_email(email, subject, body, html_body)
        return {'success': success, 'email': email}