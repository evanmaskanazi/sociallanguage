"""
Celery configuration and tasks for Therapeutic Companion
"""
import os
from celery import Celery
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery.schedules import crontab
import jwt

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
            'schedule': crontab(minute=0), # Run every hour
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
            'schedule': crontab(hour=0, minute=0), # Run daily
        },
'send-weekly-reports': {
            'task': 'celery_app.send_weekly_reports',
            'schedule': crontab(minute=0),  # Run every hour
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

        from new_backend import app, db, User, Client, Reminder, generate_unsubscribe_token

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

        unsubscribe_url = None
        if user and user.id:
            unsubscribe_token = generate_unsubscribe_token(user.id, 'reminders')
            base_url = os.environ.get('APP_BASE_URL', 'https://therapy-companion.onrender.com')
            unsubscribe_url = f"{base_url}/api/unsubscribe/{unsubscribe_token}"

        test_bodies = {
            'en': f"""This is a test email from the Therapeutic Companion Celery worker.

        If you're receiving this, it means the background task system is working correctly!

        {f'To unsubscribe, click here: {unsubscribe_url}' if unsubscribe_url else ''}

        Best regards,
        Therapeutic Companion Team""",
            'he': f"""זוהי הודעת בדיקה ממערכת ה-Celery של המלווה הטיפולי.

        אם אתה מקבל את זה, זה אומר שמערכת המשימות ברקע עובדת כראוי!

        {f'להפסקת הרישום, לחץ כאן: {unsubscribe_url}' if unsubscribe_url else ''}

        בברכה,
        צוות המלווה הטיפולי""",
            'ru': f"""Это тестовое письмо от рабочего Celery Терапевтического Компаньона.

        Если вы получили это, значит фоновая система задач работает правильно!

        {f'Чтобы отписаться, нажмите здесь: {unsubscribe_url}' if unsubscribe_url else ''}

        С наилучшими пожеланиями,
        Команда Терапевтического Компаньона""",
            'ar': f"""هذا بريد إلكتروني تجريبي من عامل Celery للرفيق العلاجي.

        إذا كنت تتلقى هذا، فهذا يعني أن نظام المهام في الخلفية يعمل بشكل صحيح!

        {f'لإلغاء الاشتراك، انقر هنا: {unsubscribe_url}' if unsubscribe_url else ''}

        مع أطيب التحيات،
        فريق الرفيق العلاجي"""
        }

        # Create email
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = test_subjects.get(reminder_lang, test_subjects['en'])

        body = test_bodies.get(reminder_lang, test_bodies['en'])
        msg.attach(MIMEText(body, 'plain'))

        if unsubscribe_url:
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; direction: {'rtl' if reminder_lang in ['he', 'ar'] else 'ltr'};">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50;">{test_subjects.get(reminder_lang, test_subjects['en'])}</h2>
                    <p>{test_bodies.get(reminder_lang, test_bodies['en']).split(chr(10))[0]}</p>
                    <p>{test_bodies.get(reminder_lang, test_bodies['en']).split(chr(10))[2]}</p>
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    <p style="text-align: center; color: #666; font-size: 12px;">
                        {'להפסקת הרישום, לחץ' if reminder_lang == 'he' else
            'Чтобы отписаться, нажмите' if reminder_lang == 'ru' else
            'لإلغاء الاشتراك، انقر' if reminder_lang == 'ar' else
            'To unsubscribe, click'}
                        <a href="{unsubscribe_url}" style="color: #666;">
                            {'כאן' if reminder_lang == 'he' else
            'здесь' if reminder_lang == 'ru' else
            'هنا' if reminder_lang == 'ar' else
            'here'}
                        </a>
                    </p>
                    <p style="text-align: center; color: #999; font-size: 12px;">
                        {test_bodies.get(reminder_lang, test_bodies['en']).split(chr(10))[-2]}<br>
                        {test_bodies.get(reminder_lang, test_bodies['en']).split(chr(10))[-1]}
                    </p>
                </div>
            </body>
            </html>
            """

        msg.attach(MIMEText(html_body, 'html'))

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


def generate_unsubscribe_token(user_id, email_type='all'):
    """Generate unsubscribe token"""
    # Get JWT settings from environment
    JWT_SECRET = os.environ.get('SECRET_KEY', 'your-secret-key')
    JWT_ALGORITHM = 'HS256'

    payload = {
        'user_id': user_id,
        'email_type': email_type,
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)




@celery.task
def send_daily_reminders():
    """Send daily reminder emails to all clients with active reminders"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from new_backend import app, db, Client, Reminder, User, EmailQueue, generate_unsubscribe_token

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
                    if client and client.user:
                        # Determine which email to use for sending
                        email_to_use = reminder.reminder_email if reminder.reminder_email else client.user.email

                        # Skip ONLY if the email we're actually sending to is a test email
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
                                'title': "Daily Check-in Reminder",
                                'unsubscribe_text': "To unsubscribe, click",  # ADD THIS
                                'unsubscribe_here': "here"
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
                                'title': "תזכורת יומית לצ'ק-אין",
                                'unsubscribe_text': "להפסקת הרישום, לחץ",  # ADD THIS
                                'unsubscribe_here': "כאן"
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
                                'title': "Ежедневное напоминание об отметке",
                                'unsubscribe_text': "Чтобы отписаться, нажмите",  # ADD THIS
                                 'unsubscribe_here': "здесь"
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
                                'title': "تذكير يومي بتسجيل الحضور",
                                'unsubscribe_text': "لإلغاء الاشتراك، انقر",  # ADD THIS
                                'unsubscribe_here': "هنا"
                            }
                        }

                        # Get the appropriate translation
                        trans = translations.get(reminder_lang, translations['en'])

                        # Create plain text body

                        unsubscribe_token = generate_unsubscribe_token(client.user.id, 'reminders')
                        unsubscribe_url = f"{base_url}/api/unsubscribe/{unsubscribe_token}"


                        body = f"""{trans['greeting']},

{trans['reminder_text']}

{trans['progress_text']}

{trans['login_text']}
{base_url}/login.html

{trans['client_id']}: {client.client_name if client.client_name else client.client_serial}

{trans['unsubscribe_text']} {trans['unsubscribe_here']}: {unsubscribe_url}

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
        <p style="color: #666; font-size: 14px; text-align: center;">
                    {trans['unsubscribe_text']} <a href="{unsubscribe_url}" style="color: #666;">{trans['unsubscribe_here']}</a>
                </p>
        <p style="color: #666; font-size: 14px;">{trans['client_id']}: {client.client_name if client.client_name else client.client_serial}</p>
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


@celery.task
def send_weekly_reports():
    """Send weekly reports to therapists"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from new_backend import app, db, Therapist, Reminder, Client, create_weekly_report_pdf
    from datetime import datetime, date, timedelta
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    with app.app_context():
        try:
            # Get current day and hour
            now = datetime.utcnow()
            current_day = now.weekday()  # Monday is 0, Sunday is 6
            current_hour = now.hour

            # Convert to 0=Sunday format to match our storage
            current_day_sunday_format = (current_day + 1) % 7

            print(f"[CELERY] Checking weekly reports for day {current_day_sunday_format} hour {current_hour}")

            # Find all active weekly report reminders for this day and hour
            reminders = db.session.query(Reminder).join(Therapist, Reminder.client_id == Therapist.id).filter(
                Reminder.is_active == True,
                Reminder.reminder_type == 'weekly_report',
                Reminder.day_of_week == current_day_sunday_format,
                db.extract('hour', Reminder.reminder_time) == current_hour
            ).all()

            print(f"[CELERY] Found {len(reminders)} weekly reports to send")

            sent_count = 0

            for reminder in reminders:
                try:
                    # Get therapist
                    therapist = Therapist.query.get(reminder.client_id)
                    if not therapist or not therapist.user:
                        continue

                    # Get ALL active clients for this therapist
                    active_clients = therapist.clients.filter_by(is_active=True).all()
                    if not active_clients:
                        print(f"[CELERY] No active clients for therapist {therapist.id}")
                        continue

                    # Calculate week dates
                    today = date.today()
                    week_start = today - timedelta(days=today.weekday())
                    week_end = week_start + timedelta(days=6)
                    year = today.year
                    week_num = today.isocalendar()[1]

                    # Determine email
                    email_to_use = reminder.reminder_email if reminder.reminder_email else therapist.user.email

                    # Create email
                    msg = MIMEMultipart()
                    msg['From'] = os.environ.get('SYSTEM_EMAIL')
                    msg['To'] = email_to_use

                    # Translated subjects
                    subjects = {
                        'en': f"Weekly Therapy Report - Week {week_num}, {year}",
                        'he': f"דוח טיפולי שבועי - שבוע {week_num}, {year}",
                        'ru': f"Еженедельный терапевтический отчет - Неделя {week_num}, {year}",
                        'ar': f"التقرير العلاجي الأسبوعي - الأسبوع {week_num}, {year}"
                    }
                    lang = reminder.reminder_language or 'en'
                    msg['Subject'] = subjects.get(lang, subjects['en'])

                    # Translated body
                    bodies = {
                        'en': "Weekly checkin time. Reminder to see how your clients are doing.",
                        'he': "זמן סיכום שבועי. תזכורת לבדוק איך מסתדרים המטופלים שלך.",
                        'ru': "Время еженедельной проверки. Напоминание проверить, как дела у ваших клиентов.",
                        'ar': "وقت الفحص الأسبوعي. تذكير لمعرفة كيف حال عملائك."
                    }
                    body = bodies.get(lang, bodies['en'])
                    msg.attach(MIMEText(body, 'plain', 'utf-8'))

                    # Attach PDF for EACH client
                    attachment_count = 0
                    for client in active_clients:
                        try:
                            # Generate PDF for this client
                            pdf_buffer = create_weekly_report_pdf(
                                client, therapist, week_start, week_end, week_num, year, lang
                            )

                            # Attach PDF
                            pdf_attachment = MIMEBase('application', 'pdf')
                            pdf_attachment.set_payload(pdf_buffer.read())
                            encoders.encode_base64(pdf_attachment)
                            # Sanitize client name for filename (remove spaces and special characters)
                            safe_name = client.client_name.replace(' ', '_').replace('/', '_').replace('\\',
                                                                                                       '_') if client.client_name else client.client_serial
                            pdf_attachment.add_header(
                                'Content-Disposition',
                                f'attachment; filename=report_{safe_name}_week_{week_num}_{year}.pdf'
                            )
                            msg.attach(pdf_attachment)
                            attachment_count += 1

                        except Exception as e:
                            print(f"[CELERY] Failed to generate PDF for client {client.client_serial}: {e}")

                    if attachment_count == 0:
                        print(f"[CELERY] No PDFs generated for therapist {therapist.id}, skipping email")
                        continue

                    # Send email
                    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
                    smtp_port = int(os.environ.get('SMTP_PORT', 587))
                    smtp_username = os.environ.get('SYSTEM_EMAIL')
                    smtp_password = os.environ.get('SYSTEM_EMAIL_PASSWORD')

                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(smtp_username, smtp_password)
                    server.send_message(msg)
                    server.quit()

                    # Update last sent
                    reminder.last_sent = now
                    sent_count += 1
                    print(f"[CELERY] Sent weekly report to {email_to_use} with {attachment_count} PDFs")

                except Exception as e:
                    print(f"[CELERY] Failed to send weekly report to therapist {therapist.id}: {e}")

            db.session.commit()

            return {'message': f'Sent {sent_count} weekly reports'}

        except Exception as e:
            print(f"[CELERY] Error in send_weekly_reports: {str(e)}")
            return {'error': str(e)}


@celery.task(bind=True, max_retries=3)
def send_weekly_report_batch_task(self, therapist_id, batch_size=10):
    """Send weekly report in batches for therapists with many clients"""
    try:
        with app.app_context():
            from models import Therapist, Reminder, Client
            from datetime import datetime, date, timedelta
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
            import smtplib
            import time

            therapist = Therapist.query.get(therapist_id)
            if not therapist:
                return {'error': 'Therapist not found'}

            # Get settings
            settings = Reminder.query.filter_by(
                client_id=therapist.id,
                reminder_type='weekly_report'
            ).first()

            email = therapist.user.email
            if settings and settings.reminder_email:
                email = settings.reminder_email

            # Get ALL active clients
            active_clients = therapist.clients.filter_by(is_active=True).all()
            if not active_clients:
                return {'error': 'No active clients found'}

            # Get current week
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            year = today.year
            week_num = today.isocalendar()[1]

            lang = settings.reminder_language if settings else 'en'
            total_sent = 0

            # Process in batches
            for i in range(0, len(active_clients), batch_size):
                batch = active_clients[i:i + batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = ((len(active_clients) - 1) // batch_size) + 1

                # Create email for this batch
                msg = MIMEMultipart()
                msg['From'] = app.config['MAIL_USERNAME']
                msg['To'] = email

                # Subject with batch info
                subjects = {
                    'en': f"Weekly Therapy Report - Week {week_num}, {year} - Part {batch_num} of {total_batches}",
                    'he': f"דוח טיפולי שבועי - שבוע {week_num}, {year} - חלק {batch_num} מתוך {total_batches}",
                    'ru': f"Еженедельный отчет - Неделя {week_num}, {year} - Часть {batch_num} из {total_batches}",
                    'ar': f"التقرير الأسبوعي - الأسبوع {week_num}, {year} - الجزء {batch_num} من {total_batches}"
                }
                msg['Subject'] = subjects.get(lang, subjects['en'])

                # Body
                bodies = {
                    'en': f"This is part {batch_num} of {total_batches} of your weekly client reports.",
                    'he': f"זהו חלק {batch_num} מתוך {total_batches} של הדוחות השבועיים שלך.",
                    'ru': f"Это часть {batch_num} из {total_batches} ваших еженедельных отчетов.",
                    'ar': f"هذا هو الجزء {batch_num} من {total_batches} من تقاريرك الأسبوعية."
                }
                body = bodies.get(lang, bodies['en'])
                msg.attach(MIMEText(body, 'plain', 'utf-8'))

                # Generate PDFs for this batch
                attachment_count = 0
                from new_backend import create_weekly_report_pdf

                for client in batch:
                    try:
                        pdf_buffer = create_weekly_report_pdf(
                            client, therapist, week_start, week_end, week_num, year, lang
                        )

                        # Attach PDF
                        pdf_attachment = MIMEBase('application', 'pdf')
                        pdf_attachment.set_payload(pdf_buffer.read())
                        pdf_buffer.close()  # Free memory immediately

                        encoders.encode_base64(pdf_attachment)
                        safe_name = client.client_name.replace(' ', '_').replace('/', '_').replace('\\',
                                                                                                   '_') if client.client_name else client.client_serial
                        pdf_attachment.add_header(
                            'Content-Disposition',
                            f'attachment; filename=report_{safe_name}_week_{week_num}_{year}.pdf'
                        )
                        msg.attach(pdf_attachment)
                        attachment_count += 1

                    except Exception as e:
                        app.logger.error(f"Failed to generate PDF for client {client.client_serial}: {e}")

                if attachment_count > 0:
                    # Send this batch
                    server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
                    server.starttls()
                    server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                    server.send_message(msg)
                    server.quit()
                    total_sent += attachment_count

                    # Delay between batches to avoid overwhelming email server
                    if i + batch_size < len(active_clients):
                        time.sleep(2)

            return {
                'success': True,
                'message': f'Reports sent successfully in {total_batches} batches with {total_sent} total reports'
            }

    except Exception as e:
        app.logger.error(f"Weekly report batch task failed: {str(e)}")
        raise self.retry(exc=e, countdown=60)


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

                        # If max retries reached, mark as failed

                        if self.request.retries >= self.max_retries - 1:

                            email.status = 'failed'

                            email.error_message = str(e)

                        else:

                            # Otherwise, reset to pending for retry

                            email.status = 'pending'

                            email.error_message = f"Retry {self.request.retries + 1}: {str(e)}"

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
    from datetime import datetime, timedelta

    with app.app_context():
        try:
            # FIRST: Reset any stuck 'processing' emails older than 10 minutes
            ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
            stuck_emails = EmailQueue.query.filter(
                EmailQueue.status == 'processing',
                EmailQueue.last_attempt_at < ten_minutes_ago
            ).all()

            for email in stuck_emails:
                email.status = 'pending'
                email.attempts = (email.attempts or 0) + 1
                print(f"[CELERY] Reset stuck email {email.id} to pending")

            if stuck_emails:
                db.session.commit()
                print(f"[CELERY] Reset {len(stuck_emails)} stuck emails")

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

                # Mark as processing with timestamp
                email.status = 'processing'
                email.attempts = (email.attempts or 0) + 1
                email.last_attempt_at = datetime.utcnow()

            db.session.commit()

            return {'processed': len(pending_emails),
                    'reset_stuck': len(stuck_emails) if 'stuck_emails' in locals() else 0}

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