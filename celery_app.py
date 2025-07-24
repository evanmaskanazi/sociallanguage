"""
Celery configuration and tasks for Therapeutic Companion
"""
import os
from celery import Celery
from datetime import datetime, timedelta
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
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
    beat_schedule={
        'send-daily-reminders': {
            'task': 'celery_app.send_daily_reminders',
            'schedule': 3600.0,  # Run every hour
        },
        'process-email-queue': {
            'task': 'celery_app.process_email_queue_task',
            'schedule': 60.0,  # Run every minute
        },
        'cleanup-old-emails': {
            'task': 'celery_app.cleanup_old_emails',
            'schedule': 86400.0,  # Run daily
        },
    }
)


@celery.task(bind=True, max_retries=3)
def send_reminder_test(self, email):
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
            # Get user's language preference from the email's user
            reminder_lang = 'en'
            try:
                from new_backend import User, Client
                user = User.query.filter_by(email=email).first()
                if user and user.client:
                    reminder = user.client.reminders.filter_by(
                        reminder_type='daily_checkin',
                        is_active=True
                    ).first()
                    if reminder and hasattr(reminder, 'reminder_language'):
                        reminder_lang = reminder.reminder_language
            except:
                pass

            # Translated test messages
            test_subjects = {
                'en': 'Celery Test - Therapeutic Companion',
                'he': 'בדיקת Celery - מלווה טיפולי',
                'ru': 'Тест Celery - Терапевтический Компаньон',
                'ar': 'اختبار Celery - الرفيق العلاجي'
            }

            test_bodies = {
                'en': """This is a test email from the Therapeutic Companion Celery worker.

        If you're receiving this, it means the background task system is working correctly!

        Best regards,
        Therapeutic Companion Team""",
                'he': """זוהי הודעת בדיקה ממערכת ה-Celery של המלווה הטיפולי.

        אם אתה מקבל את זה, זה אומר שמערכת המשימות ברקע עובדת כראוי!

        בברכה,
        צוות המלווה הטיפולי""",
                'ru': """Это тестовое письмо от рабочего Celery Терапевтического Компаньона.

        Если вы получили это, значит фоновая система задач работает правильно!

        С наилучшими пожеланиями,
        Команда Терапевтического Компаньона""",
                'ar': """هذا بريد إلكتروني تجريبي من عامل Celery للرفيق العلاجي.

        إذا كنت تتلقى هذا، فهذا يعني أن نظام المهام في الخلفية يعمل بشكل صحيح!

        مع أطيب التحيات،
        فريق الرفيق العلاجي"""
            }

            # Create email
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = email
            msg['Subject'] = test_subjects.get(reminder_lang, test_subjects['en'])

            body = test_bodies.get(reminder_lang, test_bodies['en'])










        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()

        return {'success': True, 'message': f'Test email sent to {email}'}

    except Exception as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))


@celery.task
def send_daily_reminders():
    """Send daily reminder emails to all clients with active reminders"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from new_backend import app, db, Client, Reminder, User, EmailQueue

    with app.app_context():
        try:
            # Get current UTC time and hour
            utc_now = datetime.utcnow()
            current_utc_hour = utc_now.hour

            print(f"[CELERY] Running send_daily_reminders at {utc_now} UTC (hour: {current_utc_hour})")

            # Find all active reminders for this UTC hour
            reminders = db.session.query(Reminder).join(Client).filter(
                Reminder.is_active == True,
                Reminder.reminder_type == 'daily_checkin',
                db.extract('hour', Reminder.reminder_time) == current_utc_hour
            ).all()

            print(f"[CELERY] Found {len(reminders)} reminders for UTC hour {current_utc_hour}")

            queued_count = 0

            for reminder in reminders:
                try:
                    client = reminder.client
                    if client and client.user and client.user.email:
                        # Determine which email to use
                        email_to_use = reminder.reminder_email if reminder.reminder_email else client.user.email

                        # Skip test emails
                        if (email_to_use.endswith('example.com') or
                                email_to_use.endswith('test.test') or
                                email_to_use == 'test@test.test'):
                            print(f"[CELERY] Skipping test email: {email_to_use}")
                            continue

                        # Check if we've sent recently (to avoid duplicates)
                        if reminder.last_sent:
                            minutes_since = (utc_now - reminder.last_sent).total_seconds() / 60
                            if minutes_since < 30:  # Don't send if sent in last 30 minutes
                                print(f"[CELERY] Skipping {client.user.email} - sent {minutes_since:.1f} minutes ago")
                                continue

                        # Queue the email
                        base_url = os.environ.get('APP_BASE_URL', 'https://therapy-companion.onrender.com')

                        # Get reminder language
                        reminder_lang = reminder.reminder_language if hasattr(reminder, 'reminder_language') else 'en'

                        # Translated subjects
                        subjects = {
                            'en': "Daily Check-in Reminder - Therapeutic Companion",
                            'he': "תזכורת יומית לצ'ק-אין - מלווה טיפולי",
                            'ru': "Ежедневное напоминание об отметке - Терапевтический Компаньон",
                            'ar': "تذكير يومي بتسجيل الحضور - الرفيق العلاجي"
                        }

                        # Translated bodies
                        bodies = {
                            'en': f"""Hello,

                        This is your daily reminder to complete your therapy check-in.

                        Your therapist is tracking your progress, and your daily input is valuable for your treatment.

                        Click here to log in and complete today's check-in:
                        {base_url}/login.html

                        Client ID: {client.client_serial}

                        If you've already completed today's check-in, please disregard this message.

                        Best regards,
                        Your Therapy Team""",
                            'he': f"""שלום,

                        זוהי התזכורת היומית שלך להשלים את הצ'ק-אין הטיפולי שלך.

                        המטפל שלך עוקב אחר ההתקדמות שלך, והקלט היומי שלך חשוב לטיפול שלך.

                        לחץ כאן כדי להתחבר ולהשלים את הצ'ק-אין של היום:
                        {base_url}/login.html

                        מספר מטופל: {client.client_serial}

                        אם כבר השלמת את הצ'ק-אין של היום, אנא התעלם מהודעה זו.

                        בברכה,
                        צוות הטיפול שלך""",
                            'ru': f"""Здравствуйте,

                        Это ваше ежедневное напоминание о необходимости заполнить терапевтическую отметку.

                        Ваш терапевт отслеживает ваш прогресс, и ваши ежедневные данные важны для вашего лечения.

                        Нажмите здесь, чтобы войти и заполнить сегодняшнюю отметку:
                        {base_url}/login.html

                        ID клиента: {client.client_serial}

                        Если вы уже заполнили сегодняшнюю отметку, пожалуйста, игнорируйте это сообщение.

                        С наилучшими пожеланиями,
                        Ваша терапевтическая команда""",
                            'ar': f"""مرحباً،

                        هذا تذكيرك اليومي لإكمال تسجيل الحضور العلاجي الخاص بك.

                        معالجك يتتبع تقدمك، ومدخلاتك اليومية قيمة لعلاجك.

                        انقر هنا لتسجيل الدخول وإكمال تسجيل حضور اليوم:
                        {base_url}/login.html

                        معرف العميل: {client.client_serial}

                        إذا كنت قد أكملت بالفعل تسجيل حضور اليوم، يرجى تجاهل هذه الرسالة.

                        مع أطيب التحيات،
                        فريق العلاج الخاص بك"""
                        }

                        subject = subjects.get(reminder_lang, subjects['en'])
                        body = bodies.get(reminder_lang, bodies['en'])




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

                        # Create email queue entry
                        email_queue = EmailQueue(
                            to_email=email_to_use,
                            subject=subject,
                            body=body,
                            html_body=html_body,
                            status='pending'
                        )
                        db.session.add(email_queue)

                        # Update last_sent
                        reminder.last_sent = utc_now
                        queued_count += 1
                        print(f"[CELERY] Queued reminder for {client.user.email}")

                except Exception as e:
                    print(f"[CELERY] Failed to queue reminder for client {reminder.client.client_serial}: {e}")

            db.session.commit()

            result_message = f'[CELERY] Queued {queued_count} daily reminders'
            print(result_message)

            # Trigger email processing
            process_email_queue_task.delay()

            return {'message': result_message, 'queued': queued_count}

        except Exception as e:
            print(f"[CELERY] Error: {str(e)}")
            return {'error': str(e)}


@celery.task(bind=True, max_retries=3)
def send_email_task(self, to_email, subject, body, html_body=None):
    """Send a single email with retry logic"""
    try:
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SYSTEM_EMAIL')
        smtp_password = os.environ.get('SYSTEM_EMAIL_PASSWORD')

        if not smtp_username or not smtp_password:
            return {'error': 'Email configuration missing'}

        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()

        return {'success': True, 'email': to_email}

    except Exception as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))


@celery.task
def process_email_queue_task():
    """Process pending emails from the queue"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from new_backend import app, db, EmailQueue

    with app.app_context():
        try:
            # Get pending emails
            pending_emails = EmailQueue.query.filter_by(
                status='pending'
            ).filter(
                EmailQueue.attempts < 3
            ).order_by(
                EmailQueue.created_at.asc()
            ).limit(50).all()  # Process up to 50 at a time

            for email in pending_emails:
                # Send each email as a separate Celery task
                send_email_task.delay(
                    email.to_email,
                    email.subject,
                    email.body,
                    email.html_body
                )

                # Mark as processing
                email.status = 'processing'
                email.attempts += 1

            db.session.commit()

            return {'processed': len(pending_emails)}

        except Exception as e:
            return {'error': str(e)}


@celery.task
def cleanup_old_emails():
    """Clean up old sent emails from the queue"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from new_backend import app, db, EmailQueue

    with app.app_context():
        try:
            # Delete emails older than 7 days
            old_date = datetime.utcnow() - timedelta(days=7)
            deleted = EmailQueue.query.filter(
                EmailQueue.status == 'sent',
                EmailQueue.sent_at < old_date
            ).delete()

            db.session.commit()

            return {'deleted': deleted}

        except Exception as e:
            return {'error': str(e)}


@celery.task
def check_client_inactivity():
    """Check for inactive clients and notify therapists"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from new_backend import check_client_inactivity as check_inactivity_func

    try:
        count = check_inactivity_func()
        return {'success': True, 'notifications_sent': count}
    except Exception as e:
        return {'error': str(e)}