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
        'process-email-queue-batch': {
            'task': 'celery_app.process_email_queue_batch_task',
            'schedule': 300.0,  # Run every 5 minutes
        },
        'cleanup-old-emails': {
            'task': 'celery_app.cleanup_old_emails',
            'schedule': 86400.0,  # Run daily
        },
    }
)


@celery.task(bind=True, max_retries=3)
def send_reminder_test(self, email, client_id=None):
    """Test task to send a reminder email"""
    try:
        # Import Flask app and models at the top of the task
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        from new_backend import app, db, User, Client, Reminder

        # Email configuration from environment
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SYSTEM_EMAIL')
        smtp_password = os.environ.get('SYSTEM_EMAIL_PASSWORD')

        if not smtp_username or not smtp_password:
            return {'error': 'Email configuration missing'}

        # Get user's language preference within Flask app context
        reminder_lang = 'en'
        with app.app_context():
            try:
                # If client_id is provided, use it directly (most reliable)
                if client_id:
                    client = Client.query.get(client_id)
                    if client:
                        user = client.user
                        reminder = client.reminders.filter_by(
                            reminder_type='daily_checkin',
                            is_active=True
                        ).first()
                        if reminder and reminder.reminder_language:
                            reminder_lang = reminder.reminder_language
                            print(f"[CELERY] Found language via client_id: {reminder_lang} for {email}")
                    else:
                        print(f"[CELERY] Client ID {client_id} not found, falling back to email search")
                        # Fall through to email search below
                        user = None
                else:
                    # No client_id provided, use email search
                    user = None

                # Email search fallback (if no client_id or client not found)
                if not user:
                    # First try to find user by the email address
                    user = User.query.filter_by(email=email).first()

                    # If not found, it might be a reminder email - search reminders
                    if not user:
                        reminder = Reminder.query.filter_by(
                            reminder_email=email,
                            reminder_type='daily_checkin',
                            is_active=True
                        ).first()
                        if reminder and reminder.client:
                            user = reminder.client.user
                            if reminder.reminder_language:
                                reminder_lang = reminder.reminder_language
                                print(f"[CELERY] Found language via reminder email: {reminder_lang} for {email}")
                    # If we found the user by email, check their reminders
                    elif user and user.client:
                        reminder = user.client.reminders.filter_by(
                            reminder_type='daily_checkin',
                            is_active=True
                        ).first()
                        if reminder and hasattr(reminder, 'reminder_language') and reminder.reminder_language:
                            reminder_lang = reminder.reminder_language
                            print(f"[CELERY] Found reminder language: {reminder_lang} for {email}")
                        else:
                            print(f"[CELERY] No reminder language found for {email}, using default: en")
                    else:
                        print(f"[CELERY] No user found for {email}, using default: en")

            except Exception as e:
                print(f"[CELERY] Error getting language preference: {e}")

        print(f"[CELERY] Sending test email to {email} in language: {reminder_lang}")

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

        return {'success': True, 'message': f'Test email sent to {email} in language: {reminder_lang}'}

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
                        reminder_lang = reminder.reminder_language if reminder.reminder_language else 'en'

                        # Complete translation dictionary including HTML content
                        translations = {
                            'en': {
                                'subject': "Daily Check-in Reminder - Therapeutic Companion",
                                'greeting': "Hello",
                                'reminder_text': "This is your daily reminder to complete your therapy check-in.",
                                'progress_text': "Your therapist is tracking your progress, and your daily input is valuable for your treatment.",
                                'login_text': "Click here to log in and complete today's check-in:",
                                'button_text': "Complete Today's Check-in",
                                'client_id': "Client ID",
                                'already_completed': "If you've already completed today's check-in, please disregard this message.",
                                'regards': "Best regards,\nYour Therapy Team",
                                'title': "Daily Check-in Reminder"
                            },
                            'he': {
                                'subject': "תזכורת יומית לצ'ק-אין - מלווה טיפולי",
                                'greeting': "שלום",
                                'reminder_text': "זוהי התזכורת היומית שלך להשלים את הצ'ק-אין הטיפולי שלך.",
                                'progress_text': "המטפל שלך עוקב אחר ההתקדמות שלך, והקלט היומי שלך חשוב לטיפול שלך.",
                                'login_text': "לחץ כאן כדי להתחבר ולהשלים את הצ'ק-אין של היום:",
                                'button_text': "השלם את הצ'ק-אין של היום",
                                'client_id': "מספר מטופל",
                                'already_completed': "אם כבר השלמת את הצ'ק-אין של היום, אנא התעלם מהודעה זו.",
                                'regards': "בברכה,\nצוות הטיפול שלך",
                                'title': "תזכורת יומית לצ'ק-אין"
                            },
                            'ru': {
                                'subject': "Ежедневное напоминание об отметке - Терапевтический Компаньон",
                                'greeting': "Здравствуйте",
                                'reminder_text': "Это ваше ежедневное напоминание о необходимости заполнить терапевтическую отметку.",
                                'progress_text': "Ваш терапевт отслеживает ваш прогресс, и ваши ежедневные данные важны для вашего лечения.",
                                'login_text': "Нажмите здесь, чтобы войти и заполнить сегодняшнюю отметку:",
                                'button_text': "Заполнить сегодняшнюю отметку",
                                'client_id': "ID клиента",
                                'already_completed': "Если вы уже заполнили сегодняшнюю отметку, пожалуйста, игнорируйте это сообщение.",
                                'regards': "С наилучшими пожеланиями,\nВаша терапевтическая команда",
                                'title': "Ежедневное напоминание об отметке"
                            },
                            'ar': {
                                'subject': "تذكير يومي بتسجيل الحضور - الرفيق العلاجي",
                                'greeting': "مرحباً",
                                'reminder_text': "هذا تذكيرك اليومي لإكمال تسجيل الحضور العلاجي الخاص بك.",
                                'progress_text': "معالجك يتتبع تقدمك، ومدخلاتك اليومية قيمة لعلاجك.",
                                'login_text': "انقر هنا لتسجيل الدخول وإكمال تسجيل حضور اليوم:",
                                'button_text': "أكمل تسجيل حضور اليوم",
                                'client_id': "معرف العميل",
                                'already_completed': "إذا كنت قد أكملت بالفعل تسجيل حضور اليوم، يرجى تجاهل هذه الرسالة.",
                                'regards': "مع أطيب التحيات،\nفريق العلاج الخاص بك",
                                'title': "تذكير يومي بتسجيل الحضور"
                            }
                        }

                        # Get the appropriate translation
                        trans = translations.get(reminder_lang, translations['en'])

                        # Create plain text body
                        body = f"""{trans['greeting']},

{trans['reminder_text']}

{trans['progress_text']}

{trans['login_text']}
{base_url}/login.html

{trans['client_id']}: {client.client_serial}

{trans['already_completed']}

{trans['regards']}"""

                        # Create PROPERLY TRANSLATED HTML body
                        html_body = f"""
<html>
<head>
    <meta charset="utf-8">
</head>
<body style="font-family: Arial, sans-serif; color: #333; direction: {'rtl' if reminder_lang in ['he', 'ar'] else 'ltr'};">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #2c3e50;">{trans['title']}</h2>
        <p>{trans['greeting']},</p>
        <p>{trans['reminder_text']}</p>
        <p>{trans['progress_text']}</p>
        <div style="text-align: center; margin: 40px 0;">
            <a href="{base_url}/login.html"
               style="background-color: #4CAF50; color: white; padding: 15px 40px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      font-weight: bold; font-size: 16px;">
                {trans['button_text']}
            </a>
        </div>
        <p style="color: #666; font-size: 14px;">{trans['client_id']}: {client.client_serial}</p>
        <p style="color: #666; font-size: 14px;">
            {trans['already_completed']}
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="color: #999; font-size: 12px;">
            {trans['regards'].replace(chr(10), '<br>')}
        </p>
    </div>
</body>
</html>
"""

                        # Create email queue entry
                        email_queue = EmailQueue(
                            to_email=email_to_use,
                            subject=trans['subject'],
                            body=body,
                            html_body=html_body,
                            status='pending'
                        )
                        db.session.add(email_queue)

                        # Update last_sent
                        reminder.last_sent = utc_now
                        queued_count += 1
                        print(f"[CELERY] Queued reminder for {email_to_use} in language: {reminder_lang}")

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
def send_email_task(self, email_queue_id):
    """Send a single email and update its status in the database"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from new_backend import app, db, EmailQueue

    with app.app_context():
        try:
            # Get the email from the queue
            email = EmailQueue.query.get(email_queue_id)
            if not email:
                return {'error': f'Email with ID {email_queue_id} not found'}

            # Skip if already sent
            if email.status == 'sent':
                return {'success': True, 'message': 'Email already sent'}

            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', 587))
            smtp_username = os.environ.get('SYSTEM_EMAIL')
            smtp_password = os.environ.get('SYSTEM_EMAIL_PASSWORD')

            if not smtp_username or not smtp_password:
                email.status = 'failed'
                email.error_message = 'Email configuration missing'
                db.session.commit()
                return {'error': 'Email configuration missing'}

            # Create the email message
            msg = MIMEMultipart('alternative')
            msg['From'] = smtp_username
            msg['To'] = email.to_email
            msg['Subject'] = email.subject

            # Add both plain text and HTML parts with UTF-8 encoding
            msg.attach(MIMEText(email.body, 'plain', 'utf-8'))
            if email.html_body:
                msg.attach(MIMEText(email.html_body, 'html', 'utf-8'))

            # Send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()

            # CRITICAL: Mark as sent and update timestamp
            email.status = 'sent'
            email.sent_at = datetime.utcnow()
            email.attempts = (email.attempts or 0) + 1
            db.session.commit()

            print(f"[CELERY] Successfully sent email to {email.to_email}")
            return {'success': True, 'email': email.to_email}

        except Exception as e:
            # Update status on failure
            try:
                with app.app_context():
                    email = EmailQueue.query.get(email_queue_id)
                    if email:
                        email.status = 'failed'
                        email.error_message = str(e)
                        email.attempts = (email.attempts or 0) + 1
                        email.last_attempt_at = datetime.utcnow()
                        db.session.commit()
            except:
                pass

            print(f"[CELERY] Failed to send email {email_queue_id}: {str(e)}")
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
                send_email_task.delay(email.id)

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
def process_email_queue_batch_task():
    """Process email queue in batches for better performance"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from new_backend import process_email_queue_batch

    try:
        process_email_queue_batch()
        return {'success': True}
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