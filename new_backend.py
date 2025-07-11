"""
Enhanced Therapeutic Companion Backend
With PostgreSQL, Authentication, Role-Based Access, Client Reports, and Password Reset
"""
import random
import string
from flask import Flask, request, jsonify, send_file, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps
import os
from pathlib import Path
import secrets
import jwt
from datetime import datetime, timedelta, date
from sqlalchemy import and_, or_, func
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
import uuid

# Create Flask app
app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
app.static_folder = BASE_DIR
app.template_folder = BASE_DIR

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://localhost/therapy_companion'
).replace('postgres://', 'postgresql://')  # Fix for Render
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('PRODUCTION', False)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('SMTP_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('SYSTEM_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('SYSTEM_EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('SYSTEM_EMAIL')

# Database connection pooling
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'pool_recycle': 300,
    'pool_pre_ping': True,
    'max_overflow': 10,
    'connect_args': {
        'connect_timeout': 10,
        'options': '-c statement_timeout=30000'
    }
}

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

# JWT configuration
JWT_SECRET = app.config['SECRET_KEY']
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# Translation mappings for categories - UPDATED WITH DESCRIPTIONS
CATEGORY_TRANSLATIONS = {
    'en': {
        'Emotion Level': 'Emotion Level',
        'Emotion Level_desc': 'Overall emotional state',
        'Energy': 'Energy',
        'Energy_desc': 'Physical and mental energy levels',
        'Social Activity': 'Social Activity',
        'Social Activity_desc': 'Engagement in social interactions',
        'Sleep Quality': 'Sleep Quality',
        'Sleep Quality_desc': 'Quality of sleep',
        'Anxiety Level': 'Anxiety Level',
        'Anxiety Level_desc': 'Level of anxiety experienced',
        'Motivation': 'Motivation',
        'Motivation_desc': 'Level of motivation and drive',
        'Medication': 'Medication',
        'Medication_desc': 'Medication adherence',
        'Physical Activity': 'Physical Activity',
        'Physical Activity_desc': 'Physical activity level'
    },
    'he': {
        'Emotion Level': 'רמה רגשית',
        'Emotion Level_desc': 'מצב רגשי כללי',
        'Energy': 'אנרגיה',
        'Energy_desc': 'רמות אנרגיה פיזית ומנטלית',
        'Social Activity': 'פעילות חברתית',
        'Social Activity_desc': 'מעורבות באינטראקציות חברתיות',
        'Sleep Quality': 'איכות שינה',
        'Sleep Quality_desc': 'איכות השינה',
        'Anxiety Level': 'רמת חרדה',
        'Anxiety Level_desc': 'רמת החרדה שחווית',
        'Motivation': 'מוטיבציה',
        'Motivation_desc': 'רמת המוטיבציה והדחף',
        'Medication': 'תרופות',
        'Medication_desc': 'היענות לנטילת תרופות',
        'Physical Activity': 'פעילות גופנית',
        'Physical Activity_desc': 'רמת הפעילות הגופנית'
    },
    'ru': {
        'Emotion Level': 'Эмоциональный уровень',
        'Emotion Level_desc': 'Общее эмоциональное состояние',
        'Energy': 'Энергия',
        'Energy_desc': 'Уровни физической и умственной энергии',
        'Social Activity': 'Социальная активность',
        'Social Activity_desc': 'Участие в социальных взаимодействиях',
        'Sleep Quality': 'Качество сна',
        'Sleep Quality_desc': 'Качество сна',
        'Anxiety Level': 'Уровень тревожности',
        'Anxiety Level_desc': 'Испытываемый уровень тревожности',
        'Motivation': 'Мотивация',
        'Motivation_desc': 'Уровень мотивации и стремления',
        'Medication': 'Лекарства',
        'Medication_desc': 'Приверженность лечению',
        'Physical Activity': 'Физическая активность',
        'Physical Activity_desc': 'Уровень физической активности'
    },
    'ar': {
        'Emotion Level': 'المستوى العاطفي',
        'Emotion Level_desc': 'الحالة العاطفية العامة',
        'Energy': 'الطاقة',
        'Energy_desc': 'مستويات الطاقة الجسدية والعقلية',
        'Social Activity': 'النشاط الاجتماعي',
        'Social Activity_desc': 'المشاركة في التفاعلات الاجتماعية',
        'Sleep Quality': 'جودة النوم',
        'Sleep Quality_desc': 'جودة النوم',
        'Anxiety Level': 'مستوى القلق',
        'Anxiety Level_desc': 'مستوى القلق الذي تم اختباره',
        'Motivation': 'الدافع',
        'Motivation_desc': 'مستوى الدافع والحافز',
        'Medication': 'الأدوية',
        'Medication_desc': 'الالتزام بالأدوية',
        'Physical Activity': 'النشاط البدني',
        'Physical Activity_desc': 'مستوى النشاط البدني'
    }
}

# Add other translations for reports
REPORT_TRANSLATIONS = {
    'en': {
        'weekly_report_title': 'Weekly Progress Report',
        'client': 'Client',
        'week': 'Week',
        'daily_checkins': 'Daily Check-ins',
        'date': 'Date',
        'day': 'Day',
        'checkin_time': 'Check-in Time',
        'emotional': 'Emotional',
        'notes': 'Notes',
        'medication': 'Medication',
        'activity': 'Activity',
        'completion': 'Completion',
        'no_checkin': 'No check-in',
        'weekly_summary': 'Weekly Summary',
        'checkin_completion': 'Check-in Completion',
        'days': 'days',
        'average_rating': 'Average Rating',
        'adherence': 'Adherence',
        'weekly_goals': 'Weekly Goals',
        'completion_rate': 'Completion Rate',
        'therapist_notes': 'Therapist Notes',
        'type': 'Type',
        'content': 'Content',
        'status': 'Status',
        'mission': 'MISSION',
        'completed': 'Completed',
        'pending': 'Pending',
        'excellent': 'Excellent',
        'good': 'Good',
        'needs_improvement': 'Needs Improvement',
        'needs_support': 'Needs Support',
        'needs_encouragement': 'Needs Encouragement'
    },
    'he': {
        'weekly_report_title': 'דוח התקדמות שבועי',
        'client': 'מטופל',
        'week': 'שבוע',
        'daily_checkins': 'צ׳ק-אין יומי',
        'date': 'תאריך',
        'day': 'יום',
        'checkin_time': 'זמן צ׳ק-אין',
        'emotional': 'רגשי',
        'notes': 'הערות',
        'medication': 'תרופות',
        'activity': 'פעילות',
        'completion': 'השלמה',
        'no_checkin': 'אין צ׳ק-אין',
        'weekly_summary': 'סיכום שבועי',
        'checkin_completion': 'השלמת צ׳ק-אין',
        'days': 'ימים',
        'average_rating': 'דירוג ממוצע',
        'adherence': 'היענות',
        'weekly_goals': 'יעדים שבועיים',
        'completion_rate': 'אחוז השלמה',
        'therapist_notes': 'הערות מטפל',
        'type': 'סוג',
        'content': 'תוכן',
        'status': 'סטטוס',
        'mission': 'משימה',
        'completed': 'הושלם',
        'pending': 'ממתין',
        'excellent': 'מצוין',
        'good': 'טוב',
        'needs_improvement': 'דורש שיפור',
        'needs_support': 'זקוק לתמיכה',
        'needs_encouragement': 'זקוק לעידוד'
    },
    'ru': {
        'weekly_report_title': 'Еженедельный отчет о прогрессе',
        'client': 'Клиент',
        'week': 'Неделя',
        'daily_checkins': 'Ежедневные отметки',
        'date': 'Дата',
        'day': 'День',
        'checkin_time': 'Время отметки',
        'emotional': 'Эмоциональное',
        'notes': 'Заметки',
        'medication': 'Лекарства',
        'activity': 'Активность',
        'completion': 'Завершение',
        'no_checkin': 'Нет отметки',
        'weekly_summary': 'Недельная сводка',
        'checkin_completion': 'Завершение отметок',
        'days': 'дней',
        'average_rating': 'Средний рейтинг',
        'adherence': 'Приверженность',
        'weekly_goals': 'Недельные цели',
        'completion_rate': 'Процент выполнения',
        'therapist_notes': 'Заметки терапевта',
        'type': 'Тип',
        'content': 'Содержание',
        'status': 'Статус',
        'mission': 'ЗАДАНИЕ',
        'completed': 'Выполнено',
        'pending': 'В ожидании',
        'excellent': 'Отлично',
        'good': 'Хорошо',
        'needs_improvement': 'Требует улучшения',
        'needs_support': 'Нуждается в поддержке',
        'needs_encouragement': 'Нуждается в поощрении'
    },
    'ar': {
        'weekly_report_title': 'تقرير التقدم الأسبوعي',
        'client': 'العميل',
        'week': 'الأسبوع',
        'daily_checkins': 'تسجيلات الحضور اليومية',
        'date': 'التاريخ',
        'day': 'اليوم',
        'checkin_time': 'وقت تسجيل الحضور',
        'emotional': 'عاطفي',
        'notes': 'ملاحظات',
        'medication': 'الأدوية',
        'activity': 'النشاط',
        'completion': 'الإكمال',
        'no_checkin': 'لا يوجد تسجيل حضور',
        'weekly_summary': 'الملخص الأسبوعي',
        'checkin_completion': 'إكمال تسجيل الحضور',
        'days': 'أيام',
        'average_rating': 'التقييم المتوسط',
        'adherence': 'الالتزام',
        'weekly_goals': 'الأهداف الأسبوعية',
        'completion_rate': 'معدل الإنجاز',
        'therapist_notes': 'ملاحظات المعالج',
        'type': 'النوع',
        'content': 'المحتوى',
        'status': 'الحالة',
        'mission': 'مهمة',
        'completed': 'مكتمل',
        'pending': 'معلق',
        'excellent': 'ممتاز',
        'good': 'جيد',
        'needs_improvement': 'يحتاج إلى تحسين',
        'needs_support': 'يحتاج إلى دعم',
        'needs_encouragement': 'يحتاج إلى تشجيع'
    }
}

# Days of week translations
DAYS_TRANSLATIONS = {
    'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'he': ['יום שני', 'יום שלישי', 'יום רביעי', 'יום חמישי', 'יום שישי', 'שבת', 'יום ראשון'],
    'ru': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
    'ar': ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
}


# ============= DATABASE MODELS =============

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    therapist = db.relationship('Therapist', backref='user', uselist=False, cascade='all, delete-orphan')
    client = db.relationship('Client', backref='user', uselist=False, cascade='all, delete-orphan')
    session_tokens = db.relationship('SessionToken', backref='user', cascade='all, delete-orphan')
    password_resets = db.relationship('PasswordReset', backref='user', cascade='all, delete-orphan')


class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reset_token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Therapist(db.Model):
    __tablename__ = 'therapists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    license_number = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    organization = db.Column(db.String(255))
    specializations = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    clients = db.relationship('Client', backref='therapist', lazy='dynamic')
    notes = db.relationship('TherapistNote', backref='therapist', lazy='dynamic')


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    client_serial = db.Column(db.String(50), unique=True, nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapists.id'))
    start_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    checkins = db.relationship('DailyCheckin', backref='client', lazy='dynamic', cascade='all, delete-orphan')
    tracking_plans = db.relationship('ClientTrackingPlan', backref='client', lazy='dynamic',
                                     cascade='all, delete-orphan')
    goals = db.relationship('WeeklyGoal', backref='client', lazy='dynamic', cascade='all, delete-orphan')
    reminders = db.relationship('Reminder', backref='client', lazy='dynamic', cascade='all, delete-orphan')


class TrackingCategory(db.Model):
    __tablename__ = 'tracking_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    scale_min = db.Column(db.Integer, default=1)
    scale_max = db.Column(db.Integer, default=5)
    is_default = db.Column(db.Boolean, default=False)


class ClientTrackingPlan(db.Model):
    __tablename__ = 'client_tracking_plans'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('tracking_categories.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship('TrackingCategory', backref='client_plans')


class WeeklyGoal(db.Model):
    __tablename__ = 'weekly_goals'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapists.id'))
    goal_text = db.Column(db.Text, nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    completions = db.relationship('GoalCompletion', backref='goal', lazy='dynamic', cascade='all, delete-orphan')


class DailyCheckin(db.Model):
    __tablename__ = 'daily_checkins'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    checkin_date = db.Column(db.Date, nullable=False)
    checkin_time = db.Column(db.Time, nullable=False)
    emotional_value = db.Column(db.Integer)
    emotional_notes = db.Column(db.Text)
    medication_value = db.Column(db.Integer)
    medication_notes = db.Column(db.Text)
    activity_value = db.Column(db.Integer)
    activity_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('client_id', 'checkin_date'),)


class CategoryResponse(db.Model):
    __tablename__ = 'category_responses'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('tracking_categories.id'))
    response_date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship('TrackingCategory', backref='responses')


class GoalCompletion(db.Model):
    __tablename__ = 'goal_completions'

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('weekly_goals.id'))
    completion_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('goal_id', 'completion_date'),)


class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    reminder_type = db.Column(db.String(50), nullable=False)
    reminder_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_sent = db.Column(db.DateTime)


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapists.id'))
    report_type = db.Column(db.String(50), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.Text)
    data = db.Column(db.JSON)


class TherapistNote(db.Model):
    __tablename__ = 'therapist_notes'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapists.id'))
    note_type = db.Column(db.String(50), default='general')
    content = db.Column(db.Text, nullable=False)
    is_mission = db.Column(db.Boolean, default=False)
    mission_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)


class SessionToken(db.Model):
    __tablename__ = 'session_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============= AUTHENTICATION HELPERS =============

def generate_token(user_id, role):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(allowed_roles=None):
    """Authentication decorator"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Invalid authorization header'}), 401

            token = auth_header.replace('Bearer ', '')
            payload = verify_token(token)

            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401

            # Check if user exists and is active
            user = User.query.get(payload['user_id'])
            if not user or not user.is_active:
                return jsonify({'error': 'User not found or inactive'}), 401

            # Check role permissions
            if allowed_roles and user.role not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403

            # Add user info to request
            request.current_user = user
            request.user_id = user.id
            request.user_role = user.role

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def generate_client_serial():
    """Generate unique client serial number"""
    import random
    import string
    while True:
        serial = 'C' + ''.join(random.choices(string.digits, k=8))
        if not Client.query.filter_by(client_serial=serial).first():
            return serial


def send_email(to_email, subject, body, html_body=None):
    """Send email using configured SMTP settings"""
    if not app.config.get('MAIL_USERNAME'):
        # Email not configured, return silently
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add plain text part
        msg.attach(MIMEText(body, 'plain'))

        # Add HTML part if provided
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))

        # Send email
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def get_language_from_header():
    """Get preferred language from Accept-Language header"""
    accept_language = request.headers.get('Accept-Language', 'en')
    # Simple parsing - just get the first language code
    lang = accept_language.split(',')[0].split('-')[0].lower()

    # Map to supported languages
    if lang in ['en', 'he', 'ru', 'ar']:
        return lang
    return 'en'


def translate_category_name(name, lang='en'):
    """Translate category name to specified language"""
    result = CATEGORY_TRANSLATIONS.get(lang, {}).get(name, name)
    print(f"Translating '{name}' to '{lang}': '{result}'")
    return result


def translate_report_term(term, lang='en'):
    """Translate report term to specified language"""
    return REPORT_TRANSLATIONS.get(lang, {}).get(term, term)


def translate_day_name(day_index, lang='en'):
    """Translate day name to specified language"""
    days = DAYS_TRANSLATIONS.get(lang, DAYS_TRANSLATIONS['en'])
    return days[day_index] if 0 <= day_index < 7 else ''


# ============= HTML PAGE ROUTES =============

@app.route('/')
def index():
    """Serve the main HTML file"""
    try:
        file_path = os.path.join(BASE_DIR, 'index.html')
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            app.logger.error(f"index.html not found at {file_path}")
            return "index.html not found", 404
    except Exception as e:
        app.logger.error(f"Error serving index.html: {e}")
        return f"Error: {str(e)}", 500


@app.route('/login.html')
def login_page():
    """Serve the login HTML file"""
    try:
        file_path = os.path.join(BASE_DIR, 'login.html')
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            app.logger.error(f"login.html not found at {file_path}")
            return "login.html not found", 404
    except Exception as e:
        app.logger.error(f"Error serving login.html: {e}")
        return f"Error: {str(e)}", 500


@app.route('/therapist-dashboard.html')
def therapist_dashboard_page():
    """Serve the therapist dashboard HTML file"""
    try:
        file_path = os.path.join(BASE_DIR, 'therapist_dashboard.html')
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            # Try alternative filename
            alt_path = os.path.join(BASE_DIR, 'therapist-dashboard.html')
            if os.path.exists(alt_path):
                return send_file(alt_path)
            app.logger.error(f"therapist_dashboard.html not found at {file_path}")
            return "therapist_dashboard.html not found", 404
    except Exception as e:
        app.logger.error(f"Error serving therapist_dashboard.html: {e}")
        return f"Error: {str(e)}", 500


@app.route('/client-dashboard.html')
def client_dashboard_page():
    """Serve the client dashboard HTML file"""
    try:
        file_path = os.path.join(BASE_DIR, 'client_dashboard.html')
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            # Try alternative filename
            alt_path = os.path.join(BASE_DIR, 'client-dashboard.html')
            if os.path.exists(alt_path):
                return send_file(alt_path)
            app.logger.error(f"client_dashboard.html not found at {file_path}")
            return "client_dashboard.html not found", 404
    except Exception as e:
        app.logger.error(f"Error serving client_dashboard.html: {e}")
        return f"Error: {str(e)}", 500


@app.route('/i18n.js')
def serve_i18n():
    """Serve the i18n.js file"""
    try:
        file_path = os.path.join(BASE_DIR, 'i18n.js')
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='application/javascript')
        else:
            app.logger.error(f"i18n.js not found at {file_path}")
            return "i18n.js not found", 404
    except Exception as e:
        app.logger.error(f"Error serving i18n.js: {e}")
        return f"Error: {str(e)}", 500


# ============= API ENDPOINTS =============

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user (therapist or client)"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Validate input
        if not all([email, password, role]):
            return jsonify({'error': 'Missing required fields'}), 400

        if role not in ['therapist', 'client']:
            return jsonify({'error': 'Invalid role'}), 400

        # Check if email exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        # Create user
        user = User(
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
            role=role
        )
        db.session.add(user)
        db.session.flush()

        # Create role-specific profile
        if role == 'therapist':
            # Check if license number already exists
            if Therapist.query.filter_by(license_number=data.get('license_number', '')).first():
                db.session.rollback()
                return jsonify({'error': 'License number already registered'}), 400

            therapist = Therapist(
                user_id=user.id,
                license_number=data.get('license_number', ''),
                name=data.get('name', ''),
                organization=data.get('organization', ''),
                specializations=data.get('specializations', [])
            )
            db.session.add(therapist)
        else:  # client
            client = Client(
                user_id=user.id,
                client_serial=generate_client_serial(),
                therapist_id=data.get('therapist_id'),
                start_date=date.today()
            )
            db.session.add(client)

            # Add default tracking categories
            default_categories = TrackingCategory.query.filter_by(is_default=True).all()
            for category in default_categories:
                plan = ClientTrackingPlan(
                    client_id=client.id,
                    category_id=category.id
                )
                db.session.add(plan)

        db.session.commit()

        # Generate token
        token = generate_token(user.id, role)

        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({'error': 'Missing email or password'}), 400

        # Find user
        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user.is_active:
            return jsonify({'error': 'Account deactivated'}), 401

        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Generate token
        token = generate_token(user.id, user.role)

        # Get role-specific data
        response_data = {
            'success': True,
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        }

        if user.role == 'therapist' and user.therapist:
            response_data['therapist'] = {
                'id': user.therapist.id,
                'name': user.therapist.name,
                'license_number': user.therapist.license_number,
                'organization': user.therapist.organization
            }
        elif user.role == 'client' and user.client:
            response_data['client'] = {
                'id': user.client.id,
                'serial': user.client.client_serial,
                'start_date': user.client.start_date.isoformat()
            }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/request-reset', methods=['POST'])
def request_password_reset():
    """Request password reset"""
    try:
        data = request.json
        email = data.get('email')

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        # Find user
        user = User.query.filter_by(email=email).first()

        # Always return success to prevent email enumeration
        if not user:
            return jsonify({
                'success': True,
                'message': 'If an account exists with this email, a password reset link has been sent.'
            })

        # Create reset token
        reset_token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=1)

        # Save to database
        password_reset = PasswordReset(
            user_id=user.id,
            reset_token=reset_token,
            expires_at=expires_at
        )
        db.session.add(password_reset)
        db.session.commit()

        # Create reset link
        base_url = request.host_url.rstrip('/')
        reset_link = f"{base_url}/reset-password.html?token={reset_token}"

        # Email body
        subject = "Password Reset Request - Therapeutic Companion"
        body = f"""Hello,

You requested a password reset for your Therapeutic Companion account.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you did not request this reset, please ignore this email.

Best regards,
Therapeutic Companion Team"""

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2>Password Reset Request</h2>
            <p>Hello,</p>
            <p>You requested a password reset for your Therapeutic Companion account.</p>
            <p>Click the button below to reset your password:</p>
            <p style="margin: 30px 0;">
                <a href="{reset_link}" style="background-color: #4CAF50; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">
                    Reset Password
                </a>
            </p>
            <p>Or copy this link: {reset_link}</p>
            <p><strong>This link will expire in 1 hour.</strong></p>
            <p>If you did not request this reset, please ignore this email.</p>
            <p>Best regards,<br>Therapeutic Companion Team</p>
        </body>
        </html>
        """

        # Send email
        email_sent = send_email(email, subject, body, html_body)

        return jsonify({
            'success': True,
            'message': 'If an account exists with this email, a password reset link has been sent.',
            'email_configured': email_sent
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    try:
        data = request.json
        reset_token = data.get('token')
        new_password = data.get('password')

        if not all([reset_token, new_password]):
            return jsonify({'error': 'Token and password are required'}), 400

        if len(new_password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400

        # Find valid reset token
        password_reset = PasswordReset.query.filter_by(
            reset_token=reset_token,
            used=False
        ).first()

        if not password_reset:
            return jsonify({'error': 'Invalid or expired reset token'}), 400

        # Check if expired
        if password_reset.expires_at < datetime.utcnow():
            return jsonify({'error': 'Reset token has expired'}), 400

        # Update password
        user = password_reset.user
        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

        # Mark token as used
        password_reset.used = True

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Password has been reset successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= THERAPIST ENDPOINTS =============

@app.route('/api/therapist/dashboard', methods=['GET'])
@require_auth(['therapist'])
def therapist_dashboard():
    """Get therapist dashboard data"""
    try:
        therapist = request.current_user.therapist

        # Get client statistics
        total_clients = therapist.clients.count()
        active_clients = therapist.clients.filter_by(is_active=True).count()

        # Get recent activity
        recent_checkins = db.session.query(DailyCheckin).join(Client).filter(
            Client.therapist_id == therapist.id,
            DailyCheckin.checkin_date >= date.today() - timedelta(days=7)
        ).count()

        # Get pending missions
        pending_missions = TherapistNote.query.filter_by(
            therapist_id=therapist.id,
            is_mission=True,
            mission_completed=False
        ).count()

        return jsonify({
            'success': True,
            'therapist': {
                'name': therapist.name,
                'license_number': therapist.license_number,
                'organization': therapist.organization
            },
            'statistics': {
                'total_clients': total_clients,
                'active_clients': active_clients,
                'recent_checkins': recent_checkins,
                'pending_missions': pending_missions
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/therapist/clients', methods=['GET'])
@require_auth(['therapist'])
def get_therapist_clients():
    """Get list of therapist's clients with translated category names"""
    try:
        therapist = request.current_user.therapist
        lang = get_language_from_header()

        # Get filter parameters
        status = request.args.get('status', 'all')
        sort_by = request.args.get('sort_by', 'start_date')

        # Build query
        query = therapist.clients

        if status == 'active':
            query = query.filter_by(is_active=True)
        elif status == 'inactive':
            query = query.filter_by(is_active=False)

        # Sort
        if sort_by == 'start_date':
            query = query.order_by(Client.start_date.desc())
        elif sort_by == 'serial':
            query = query.order_by(Client.client_serial)

        clients = query.all()

        # Build response
        client_data = []
        for client in clients:
            # Get last check-in
            last_checkin = client.checkins.order_by(DailyCheckin.checkin_date.desc()).first()

            # Get completion rate for last week
            week_start = date.today() - timedelta(days=date.today().weekday())
            week_checkins = client.checkins.filter(
                DailyCheckin.checkin_date >= week_start
            ).count()

            # Translate category names
            tracking_categories = []
            for plan in client.tracking_plans.filter_by(is_active=True):
                translated_name = translate_category_name(plan.category.name, lang)
                tracking_categories.append(translated_name)

            client_data.append({
                'id': client.id,
                'serial': client.client_serial,
                'start_date': client.start_date.isoformat(),
                'is_active': client.is_active,
                'last_checkin': last_checkin.checkin_date.isoformat() if last_checkin else None,
                'week_completion': f"{week_checkins}/7",
                'tracking_categories': tracking_categories
            })

        return jsonify({
            'success': True,
            'clients': client_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/therapist/client/<int:client_id>', methods=['GET'])
@require_auth(['therapist'])
def get_client_details(client_id):
    """Get detailed client information"""
    try:
        therapist = request.current_user.therapist

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Get tracking plans
        tracking_plans = []
        for plan in client.tracking_plans.filter_by(is_active=True):
            tracking_plans.append({
                'id': plan.id,
                'category': plan.category.name,
                'description': plan.category.description
            })

        # Get active goals
        active_goals = []
        week_start = date.today() - timedelta(days=date.today().weekday())
        for goal in client.goals.filter_by(
                week_start=week_start,
                is_active=True
        ):
            # Get completions for each day
            completions = {}
            for i in range(7):
                day = week_start + timedelta(days=i)
                completion = goal.completions.filter_by(completion_date=day).first()
                completions[day.isoformat()] = completion.completed if completion else None

            active_goals.append({
                'id': goal.id,
                'text': goal.goal_text,
                'completions': completions
            })

        # Get recent check-ins
        recent_checkins = []
        for checkin in client.checkins.order_by(
                DailyCheckin.checkin_date.desc()
        ).limit(7):
            recent_checkins.append({
                'date': checkin.checkin_date.isoformat(),
                'emotional': checkin.emotional_value,
                'medication': checkin.medication_value,
                'activity': checkin.activity_value
            })

        # Get therapist notes/missions
        notes = []
        for note in TherapistNote.query.filter_by(
                client_id=client_id,
                therapist_id=therapist.id
        ).order_by(TherapistNote.created_at.desc()).limit(10):
            notes.append({
                'id': note.id,
                'type': note.note_type,
                'content': note.content,
                'is_mission': note.is_mission,
                'completed': note.mission_completed,
                'created_at': note.created_at.isoformat()
            })

        return jsonify({
            'success': True,
            'client': {
                'id': client.id,
                'serial': client.client_serial,
                'start_date': client.start_date.isoformat(),
                'is_active': client.is_active,
                'tracking_plans': tracking_plans,
                'active_goals': active_goals,
                'recent_checkins': recent_checkins,
                'notes': notes
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500











# ============= TRACKING CATEGORY MANAGEMENT =============




# NEW ENDPOINT - Added after /api/categories






# ============= REMINDER ENDPOINTS =============







# ============= PROFILE MANAGEMENT =============







# ============= ANALYTICS ENDPOINTS =============

@app.route('/api/therapist/analytics/<int:client_id>', methods=['GET'])
@require_auth(['therapist'])
def get_client_analytics(client_id):
    """Get detailed analytics for a client"""
    try:
        therapist = request.current_user.therapist
        lang = get_language_from_header()

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Get date range from query params
        days = int(request.args.get('days', 30))
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        # Get check-in completion stats
        total_days = (end_date - start_date).days + 1
        checkins_count = client.checkins.filter(
            DailyCheckin.checkin_date.between(start_date, end_date)
        ).count()
        completion_rate = (checkins_count / total_days) * 100

        # Get category trends
        category_trends = {}
        for plan in client.tracking_plans.filter_by(is_active=True):
            responses = CategoryResponse.query.filter(
                CategoryResponse.client_id == client_id,
                CategoryResponse.category_id == plan.category_id,
                CategoryResponse.response_date.between(start_date, end_date)
            ).order_by(CategoryResponse.response_date).all()

            if responses:
                translated_name = translate_category_name(plan.category.name, lang)
                category_trends[translated_name] = {
                    'data': [
                        {
                            'date': resp.response_date.isoformat(),
                            'value': resp.value
                        } for resp in responses
                    ],
                    'average': sum(r.value for r in responses) / len(responses)
                }

        # Get goal completion stats
        goals = client.goals.filter(
            WeeklyGoal.week_start >= start_date
        ).all()

        goal_stats = {
            'total_goals': len(goals),
            'completion_data': []
        }

        for goal in goals:
            completions = goal.completions.all()
            completed_count = sum(1 for c in completions if c.completed)
            total_days = len(completions)
            goal_stats['completion_data'].append({
                'goal': goal.goal_text,
                'week_start': goal.week_start.isoformat(),
                'completion_rate': (completed_count / total_days * 100) if total_days > 0 else 0
            })

        # Get mission completion stats
        missions = TherapistNote.query.filter_by(
            client_id=client_id,
            therapist_id=therapist.id,
            is_mission=True
        ).all()
        completed_missions = sum(1 for m in missions if m.mission_completed)

        return jsonify({
            'success': True,
            'analytics': {
                'period': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat(),
                    'days': days
                },
                'completion': {
                    'rate': completion_rate,
                    'checkins': checkins_count,
                    'total_days': total_days
                },
                'category_trends': category_trends,
                'goals': goal_stats,
                'missions': {
                    'total': len(missions),
                    'completed': completed_missions,
                    'completion_rate': (completed_missions / len(missions) * 100) if missions else 0
                }
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= EXPORT ENDPOINTS =============

@app.route('/api/export/client-data/<int:client_id>', methods=['GET'])
@require_auth(['therapist'])
def export_client_data(client_id):
    """Export all client data as JSON"""
    try:
        therapist = request.current_user.therapist

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Compile all client data
        export_data = {
            'client': {
                'serial': client.client_serial,
                'start_date': client.start_date.isoformat(),
                'is_active': client.is_active,
                'created_at': client.created_at.isoformat()
            },
            'checkins': [],
            'category_responses': [],
            'goals': [],
            'notes': [],
            'reminders': []
        }

        # Get all check-ins
        for checkin in client.checkins.order_by(DailyCheckin.checkin_date):
            export_data['checkins'].append({
                'date': checkin.checkin_date.isoformat(),
                'time': checkin.checkin_time.strftime('%H:%M'),
                'emotional': checkin.emotional_value,
                'emotional_notes': checkin.emotional_notes,
                'medication': checkin.medication_value,
                'medication_notes': checkin.medication_notes,
                'activity': checkin.activity_value,
                'activity_notes': checkin.activity_notes
            })

        # Get all category responses
        responses = CategoryResponse.query.filter_by(client_id=client_id).order_by(CategoryResponse.response_date).all()
        for response in responses:
            export_data['category_responses'].append({
                'date': response.response_date.isoformat(),
                'category': response.category.name,
                'value': response.value,
                'notes': response.notes
            })

        # Get all goals
        for goal in client.goals.order_by(WeeklyGoal.week_start):
            goal_data = {
                'text': goal.goal_text,
                'week_start': goal.week_start.isoformat(),
                'is_active': goal.is_active,
                'completions': []
            }
            for completion in goal.completions.order_by(GoalCompletion.completion_date):
                goal_data['completions'].append({
                    'date': completion.completion_date.isoformat(),
                    'completed': completion.completed,
                    'notes': completion.notes
                })
            export_data['goals'].append(goal_data)

        # Get all therapist notes
        notes = TherapistNote.query.filter_by(
            client_id=client_id,
            therapist_id=therapist.id
        ).order_by(TherapistNote.created_at).all()

        for note in notes:
            export_data['notes'].append({
                'type': note.note_type,
                'content': note.content,
                'is_mission': note.is_mission,
                'completed': note.mission_completed,
                'created_at': note.created_at.isoformat(),
                'completed_at': note.completed_at.isoformat() if note.completed_at else None
            })

        # Get reminders
        for reminder in client.reminders.all():
            export_data['reminders'].append({
                'type': reminder.reminder_type,
                'time': reminder.reminder_time.strftime('%H:%M'),
                'is_active': reminder.is_active
            })

        return jsonify(export_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= ADMIN ENDPOINTS (if needed) =============

@app.route('/api/admin/stats', methods=['GET'])
@require_auth(['therapist'])  # Could restrict to admin role
def get_system_stats():
    """Get system-wide statistics"""
    try:
        # Only allow specific therapists or add admin role check
        stats = {
            'total_users': User.query.count(),
            'total_therapists': Therapist.query.count(),
            'total_clients': Client.query.count(),
            'active_clients': Client.query.filter_by(is_active=True).count(),
            'total_checkins': DailyCheckin.query.count(),
            'checkins_today': DailyCheckin.query.filter_by(checkin_date=date.today()).count()
        }

        return jsonify({
            'success': True,
            'stats': stats
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= CLIENT REPORT ENDPOINTS =============

@app.route('/api/client/generate-report/<week>', methods=['GET'])
@require_auth(['client'])
def client_generate_report(week):
    """Generate client's own weekly report with translations"""
    try:
        client = request.current_user.client
        lang = get_language_from_header()

        # Parse week
        year, week_num = week.split('-W')
        year = int(year)
        week_num = int(week_num)

        # Calculate week dates
        jan1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan1.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7
        first_monday = jan1 + timedelta(days=days_to_monday - 7)
        week_start = first_monday + timedelta(weeks=week_num - 1)
        week_end = week_start + timedelta(days=6)

        # Use shared function to create workbook with language support
        wb = create_weekly_report_excel(client, None, week_start, week_end, week_num, year, lang)

        # Save to BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        # Generate filename
        filename = f"my_therapy_report_{client.client_serial}_week_{week_num}_{year}.xlsx"

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/email-report', methods=['POST'])
@require_auth(['client'])
def client_email_report():
    """Prepare email report for client to send to therapist with translations"""
    try:
        client = request.current_user.client
        lang = get_language_from_header()
        data = request.json
        week = data.get('week')

        if not week:
            return jsonify({'error': 'Week is required'}), 400

        # Parse week
        year, week_num = week.split('-W')
        year = int(year)
        week_num = int(week_num)

        # Calculate week dates
        jan1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan1.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7
        first_monday = jan1 + timedelta(days=days_to_monday - 7)
        week_start = first_monday + timedelta(weeks=week_num - 1)
        week_end = week_start + timedelta(days=6)

        # Get therapist info
        therapist = client.therapist
        therapist_email = therapist.user.email if therapist and therapist.user else "therapist@example.com"
        therapist_name = therapist.name if therapist else "Therapist"

        # Get check-ins for the week
        checkins = client.checkins.filter(
            DailyCheckin.checkin_date.between(week_start.date(), week_end.date())
        ).order_by(DailyCheckin.checkin_date).all()

        # Build email content
        subject = f"Weekly Therapy Report - {client.client_serial} - Week {week_num}, {year}"

        content = f"""Dear {therapist_name},

Here is my weekly progress report for {week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}.

CLIENT: {client.client_serial}
WEEK: {week_num}, {year}
CHECK-INS COMPLETED: {len(checkins)}/7

DAILY CHECK-IN SUMMARY:
"""

        days = DAYS_TRANSLATIONS.get(lang, DAYS_TRANSLATIONS['en'])

        for i in range(7):
            current_date = week_start + timedelta(days=i)
            checkin = next((c for c in checkins if c.checkin_date == current_date.date()), None)

            content += f"\n{days[i]} ({current_date.strftime('%m/%d')}):\n"

            if checkin:
                content += f"  ✓ Checked in at {checkin.checkin_time.strftime('%H:%M')}\n"

                # Get translated category responses
                category_responses = CategoryResponse.query.filter_by(
                    client_id=client.id,
                    response_date=current_date.date()
                ).all()

                for response in category_responses:
                    cat_name = translate_category_name(response.category.name, lang)
                    content += f"  - {cat_name}: {response.value}/5"
                    if response.notes:
                        content += f" (Notes: {response.notes})"
                    content += "\n"
            else:
                content += "  ✗ No check-in recorded\n"

        # Add summary
        if checkins:
            content += "\nWEEKLY SUMMARY:\n"

            total_checkins = len(checkins)

            # Calculate averages from category responses
            for category in TrackingCategory.query.all():
                responses = []
                for checkin in checkins:
                    response = CategoryResponse.query.filter_by(
                        client_id=client.id,
                        category_id=category.id,
                        response_date=checkin.checkin_date
                    ).first()
                    if response:
                        responses.append(response.value)

                if responses:
                    avg_value = sum(responses) / len(responses)
                    cat_name = translate_category_name(category.name, lang)
                    content += f"- {cat_name}: {avg_value:.1f}/5\n"

            content += f"- Completion Rate: {total_checkins}/7 days ({(total_checkins / 7) * 100:.0f}%)\n"

        # Add goals if any
        weekly_goals = client.goals.filter_by(week_start=week_start.date()).all()
        if weekly_goals:
            content += "\nWEEKLY GOALS:\n"
            for goal in weekly_goals:
                completions = goal.completions.filter(
                    GoalCompletion.completion_date.between(week_start.date(), week_end.date())
                ).all()
                completed_days = sum(1 for c in completions if c.completed)
                content += f"- {goal.goal_text}: Completed {completed_days}/7 days\n"

        content += f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        content += "\nBest regards,\n"
        content += f"Client {client.client_serial}"

        return jsonify({
            'success': True,
            'recipient': therapist_email,
            'subject': subject,
            'content': content,
            'note': 'Copy this email content to send to your therapist'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/week-checkins/<week>', methods=['GET'])
@require_auth(['client'])
def get_client_week_checkins(week):
    """Get client's check-ins for a specific week"""
    try:
        client = request.current_user.client

        # Parse week
        year, week_num = week.split('-W')
        year = int(year)
        week_num = int(week_num)

        # Calculate week dates
        jan1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan1.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7
        first_monday = jan1 + timedelta(days=days_to_monday - 7)
        week_start = first_monday + timedelta(weeks=week_num - 1)
        week_end = week_start + timedelta(days=6)

        # Get check-ins
        checkins = client.checkins.filter(
            DailyCheckin.checkin_date.between(week_start.date(), week_end.date())
        ).all()

        # Format response
        checkin_data = {}
        for checkin in checkins:
            checkin_data[checkin.checkin_date.isoformat()] = {
                'time': checkin.checkin_time.strftime('%H:%M'),
                'emotional': checkin.emotional_value,
                'emotional_notes': checkin.emotional_notes,
                'medication': checkin.medication_value,
                'medication_notes': checkin.medication_notes,
                'activity': checkin.activity_value,
                'activity_notes': checkin.activity_notes
            }

        return jsonify({
            'success': True,
            'week_start': week_start.date().isoformat(),
            'week_end': week_end.date().isoformat(),
            'checkins': checkin_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/goals/<week>', methods=['GET'])
@require_auth(['client'])
def get_client_week_goals(week):
    """Get client's goals for a specific week"""
    try:
        client = request.current_user.client

        # Parse week
        year, week_num = week.split('-W')
        year = int(year)
        week_num = int(week_num)

        # Calculate week start
        jan1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan1.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7
        first_monday = jan1 + timedelta(days=days_to_monday - 7)
        week_start = first_monday + timedelta(weeks=week_num - 1)

        # Get goals for the week
        goals = client.goals.filter_by(
            week_start=week_start.date(),
            is_active=True
        ).all()

        # Format response
        goals_data = []
        for goal in goals:
            # Get completions for the week
            completions = {}
            for i in range(7):
                day = week_start.date() + timedelta(days=i)
                completion = goal.completions.filter_by(completion_date=day).first()
                completions[day.isoformat()] = completion.completed if completion else None

            goals_data.append({
                'id': goal.id,
                'text': goal.goal_text,
                'week_start': goal.week_start.isoformat(),
                'completions': completions
            })

        return jsonify({
            'success': True,
            'goals': goals_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_weekly_report_excel(client, therapist, week_start, week_end, week_num, year, lang='en'):
    """Create Excel workbook for weekly report with language support"""
    # Create Excel workbook
    wb = openpyxl.Workbook()

    # Get translations
    trans = lambda key: translate_report_term(key, lang)
    days = DAYS_TRANSLATIONS.get(lang, DAYS_TRANSLATIONS['en'])

    # 1. Daily Check-ins Sheet
    ws_checkins = wb.active
    ws_checkins.title = trans('daily_checkins')

    # Header styles
    header_font = Font(bold=True, size=12, color="FFFFFF")
    header_fill = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")

    # Cell styles
    cell_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Title
    ws_checkins.merge_cells('A1:J1')
    title_cell = ws_checkins['A1']
    title_cell.value = f"{trans('weekly_report_title')} - {trans('client')} {client.client_serial}"
    title_cell.font = Font(bold=True, size=16)
    title_cell.alignment = header_alignment

    # Week info
    ws_checkins.merge_cells('A2:J2')
    week_cell = ws_checkins['A2']
    week_cell.value = f"{trans('week')} {week_num}, {year} ({week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')})"
    week_cell.font = Font(size=14)
    week_cell.alignment = header_alignment

    # Headers - dynamically based on categories
    all_categories = TrackingCategory.query.all()
    headers = [trans('date'), trans('day'), trans('checkin_time')]

    # Add category headers
    for category in all_categories:
        cat_name = translate_category_name(category.name, lang)
        headers.append(f"{cat_name} (1-5)")
        headers.append(f"{cat_name} {trans('notes')}")

    headers.append(trans('completion'))

    for col, header in enumerate(headers, 1):
        cell = ws_checkins.cell(row=4, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = cell_border

    # Get check-ins for the week
    checkins = client.checkins.filter(
        DailyCheckin.checkin_date.between(week_start.date(), week_end.date())
    ).order_by(DailyCheckin.checkin_date).all()

    # Color fills for ratings
    excellent_fill = PatternFill(start_color="C8E6C9", end_color="C8E6C9", fill_type="solid")
    good_fill = PatternFill(start_color="FFF9C4", end_color="FFF9C4", fill_type="solid")
    poor_fill = PatternFill(start_color="FFCDD2", end_color="FFCDD2", fill_type="solid")

    # Populate daily check-ins
    row = 5
    checkins_completed = 0
    category_values = {cat.id: [] for cat in all_categories}

    for i in range(7):
        current_date = week_start + timedelta(days=i)
        checkin = next((c for c in checkins if c.checkin_date == current_date.date()), None)

        ws_checkins.cell(row=row, column=1).value = current_date.strftime('%Y-%m-%d')
        ws_checkins.cell(row=row, column=2).value = days[i]

        if checkin:
            checkins_completed += 1
            ws_checkins.cell(row=row, column=3).value = checkin.checkin_time.strftime('%H:%M')

            # Get category responses
            col_idx = 4
            for category in all_categories:
                response = CategoryResponse.query.filter_by(
                    client_id=client.id,
                    category_id=category.id,
                    response_date=current_date.date()
                ).first()

                if response:
                    # Value cell
                    value_cell = ws_checkins.cell(row=row, column=col_idx)
                    value_cell.value = response.value
                    category_values[category.id].append(response.value)

                    # Apply color coding
                    if response.value >= 4:
                        value_cell.fill = excellent_fill
                    elif response.value == 3:
                        value_cell.fill = good_fill
                    else:
                        value_cell.fill = poor_fill

                    # Notes cell
                    ws_checkins.cell(row=row, column=col_idx + 1).value = response.notes or ''

                col_idx += 2

            ws_checkins.cell(row=row, column=len(headers)).value = "✓"
            ws_checkins.cell(row=row, column=len(headers)).fill = excellent_fill
        else:
            ws_checkins.cell(row=row, column=3).value = trans('no_checkin')
            ws_checkins.cell(row=row, column=3).font = Font(italic=True, color="999999")
            ws_checkins.cell(row=row, column=len(headers)).value = "✗"
            ws_checkins.cell(row=row, column=len(headers)).fill = poor_fill

        # Apply borders to all cells
        for col in range(1, len(headers) + 1):
            ws_checkins.cell(row=row, column=col).border = cell_border

        row += 1

    # 2. Weekly Summary Sheet
    ws_summary = wb.create_sheet(trans('weekly_summary'))

    # Summary title
    ws_summary.merge_cells('A1:E1')
    summary_title = ws_summary['A1']
    summary_title.value = trans('weekly_summary')
    summary_title.font = Font(bold=True, size=16)
    summary_title.alignment = header_alignment

    # Summary headers
    summary_headers = ['Metric', 'Value', 'Percentage', 'Rating', trans('notes')]
    for col, header in enumerate(summary_headers, 1):
        cell = ws_summary.cell(row=3, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = cell_border

    # Calculate statistics
    summary_data = []

    # Check-in completion
    completion_rate = (checkins_completed / 7) * 100
    summary_data.append({
        'metric': trans('checkin_completion'),
        'value': f"{checkins_completed}/7 {trans('days')}",
        'percentage': f"{completion_rate:.1f}%",
        'rating': trans('excellent') if completion_rate >= 80 else trans('good') if completion_rate >= 60 else trans(
            'needs_improvement'),
        'notes': ''
    })

    # Category averages
    for category in all_categories:
        if category_values[category.id]:
            avg_value = sum(category_values[category.id]) / len(category_values[category.id])
            cat_name = translate_category_name(category.name, lang)

            summary_data.append({
                'metric': f"{trans('average_rating')} - {cat_name}",
                'value': f"{avg_value:.2f}/5",
                'percentage': f"{(avg_value / 5) * 100:.1f}%",
                'rating': trans('excellent') if avg_value >= 4 else trans('good') if avg_value >= 3 else trans(
                    'needs_support'),
                'notes': ''
            })

    # Write summary data
    row = 4
    for data in summary_data:
        ws_summary.cell(row=row, column=1).value = data['metric']
        ws_summary.cell(row=row, column=2).value = data['value']
        ws_summary.cell(row=row, column=3).value = data['percentage']

        rating_cell = ws_summary.cell(row=row, column=4)
        rating_cell.value = data['rating']
        if trans('excellent') in data['rating']:
            rating_cell.fill = excellent_fill
        elif trans('good') in data['rating']:
            rating_cell.fill = good_fill
        else:
            rating_cell.fill = poor_fill

        ws_summary.cell(row=row, column=5).value = data['notes']

        # Apply borders
        for col in range(1, 6):
            ws_summary.cell(row=row, column=col).border = cell_border

        row += 1

    # 3. Weekly Goals Sheet
    ws_goals = wb.create_sheet(trans('weekly_goals'))

    # Goals title
    ws_goals.merge_cells('A1:I1')
    goals_title = ws_goals['A1']
    goals_title.value = f"{trans('weekly_goals')} & {trans('completion')}"
    goals_title.font = Font(bold=True, size=16)
    goals_title.alignment = header_alignment

    # Goals headers
    goal_headers = ['Goal'] + [day[:3] for day in days] + [trans('completion_rate')]
    for col, header in enumerate(goal_headers, 1):
        cell = ws_goals.cell(row=3, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = cell_border

    # Get weekly goals
    weekly_goals = client.goals.filter_by(
        week_start=week_start.date(),
        is_active=True
    ).all()

    row = 4
    for goal in weekly_goals:
        ws_goals.cell(row=row, column=1).value = goal.goal_text

        # Get completions for each day
        completions = goal.completions.filter(
            GoalCompletion.completion_date.between(week_start.date(), week_end.date())
        ).all()

        completed_days = 0
        for day_idx in range(7):
            current_date = week_start.date() + timedelta(days=day_idx)
            completion = next((c for c in completions if c.completion_date == current_date), None)

            cell = ws_goals.cell(row=row, column=day_idx + 2)
            if completion:
                if completion.completed:
                    cell.value = "✓"
                    cell.fill = excellent_fill
                    completed_days += 1
                else:
                    cell.value = "✗"
                    cell.fill = poor_fill
            else:
                cell.value = "-"
                cell.fill = PatternFill(start_color="F5F5F5", end_color="F5F5F5", fill_type="solid")

            cell.alignment = Alignment(horizontal="center")
            cell.border = cell_border

        # Completion rate
        completion_rate = (completed_days / 7) * 100
        rate_cell = ws_goals.cell(row=row, column=9)
        rate_cell.value = f"{completed_days}/7 ({completion_rate:.0f}%)"
        if completion_rate >= 80:
            rate_cell.fill = excellent_fill
        elif completion_rate >= 50:
            rate_cell.fill = good_fill
        else:
            rate_cell.fill = poor_fill
        rate_cell.border = cell_border

        # Apply borders to goal text
        ws_goals.cell(row=row, column=1).border = cell_border

        row += 1

    # 4. Therapist Notes Sheet (only if therapist is provided)
    if therapist:
        ws_notes = wb.create_sheet(trans('therapist_notes'))

        # Notes title
        ws_notes.merge_cells('A1:D1')
        notes_title = ws_notes['A1']
        notes_title.value = f"{trans('therapist_notes')} & {trans('mission')}s"
        notes_title.font = Font(bold=True, size=16)
        notes_title.alignment = header_alignment

        # Notes headers
        note_headers = [trans('date'), trans('type'), trans('content'), trans('status')]
        for col, header in enumerate(note_headers, 1):
            cell = ws_notes.cell(row=3, column=col)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = cell_border

        # Get therapist notes for the week
        week_start_datetime = datetime.combine(week_start.date(), datetime.min.time())
        week_end_datetime = datetime.combine(week_end.date(), datetime.max.time())

        notes = TherapistNote.query.filter(
            TherapistNote.client_id == client.id,
            TherapistNote.therapist_id == therapist.id,
            TherapistNote.created_at.between(week_start_datetime, week_end_datetime)
        ).order_by(TherapistNote.created_at).all()

        row = 4
        for note in notes:
            ws_notes.cell(row=row, column=1).value = note.created_at.strftime('%Y-%m-%d %H:%M')

            type_cell = ws_notes.cell(row=row, column=2)
            if note.is_mission:
                type_cell.value = trans('mission')
                type_cell.font = Font(bold=True, color="E91E63")
            else:
                type_cell.value = note.note_type.title()

            ws_notes.cell(row=row, column=3).value = note.content

            status_cell = ws_notes.cell(row=row, column=4)
            if note.is_mission:
                if note.mission_completed:
                    status_cell.value = trans('completed')
                    status_cell.fill = excellent_fill
                else:
                    status_cell.value = trans('pending')
                    status_cell.fill = good_fill
            else:
                status_cell.value = "-"

            # Apply borders
            for col in range(1, 5):
                ws_notes.cell(row=row, column=col).border = cell_border

            row += 1

    # Adjust column widths for all sheets
    for ws in wb.worksheets:
        for column in ws.columns:
            max_length = 0
            column_letter = None

            for cell in column:
                try:
                    # Skip merged cells
                    if hasattr(cell, 'column_letter'):
                        if column_letter is None:
                            column_letter = cell.column_letter
                        if cell.value and len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                except:
                    pass

            # Only set width if we found a valid column letter
            if column_letter:
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width

    return wb


# ============= REPORT GENERATION =============

@app.route('/api/reports/generate/<int:client_id>/<week>', methods=['GET'])
@require_auth(['therapist'])
def generate_report(client_id, week):
    """Generate comprehensive weekly Excel report with translations"""
    try:
        therapist = request.current_user.therapist
        lang = get_language_from_header()

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Parse week
        year, week_num = week.split('-W')
        year = int(year)
        week_num = int(week_num)

        # Calculate week dates
        jan1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan1.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7
        first_monday = jan1 + timedelta(days=days_to_monday - 7)
        week_start = first_monday + timedelta(weeks=week_num - 1)
        week_end = week_start + timedelta(days=6)

        # Create Excel workbook using the shared function with language support
        wb = create_weekly_report_excel(client, therapist, week_start, week_end, week_num, year, lang)

        # Save to BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        # Generate filename
        filename = f"therapy_report_{client.client_serial}_week_{week_num}_{year}.xlsx"

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# UPDATED EMAIL REPORT FUNCTION
@app.route('/api/therapist/email-report', methods=['POST'])
@require_auth(['therapist'])
def email_therapy_report():
    """Send therapy report via email with translations"""
    try:
        therapist = request.current_user.therapist
        lang = get_language_from_header()
        data = request.json

        client_id = data.get('client_id')
        week = data.get('week')
        recipient_email = data.get('recipient_email')

        # Validate input
        if not client_id:
            return jsonify({'error': 'Client ID is required'}), 400

        if not week:
            return jsonify({'error': 'Week is required'}), 400

        # Ensure client_id is an integer
        try:
            client_id = int(client_id)
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid client ID'}), 400

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Parse week
        try:
            year, week_num = week.split('-W')
            year = int(year)
            week_num = int(week_num)
        except (ValueError, AttributeError):
            return jsonify({'error': 'Invalid week format'}), 400

        # Calculate week dates
        jan1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan1.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7
        first_monday = jan1 + timedelta(days=days_to_monday - 7)
        week_start = first_monday + timedelta(weeks=week_num - 1)
        week_end = week_start + timedelta(days=6)

        # Get check-ins for summary
        checkins = client.checkins.filter(
            DailyCheckin.checkin_date.between(week_start.date(), week_end.date())
        ).order_by(DailyCheckin.checkin_date).all()

        checkins_completed = len(checkins)

        # Build email content with translations
        trans = lambda key: translate_report_term(key, lang)

        # Calculate summary statistics from category responses
        summary_stats = []
        for category in TrackingCategory.query.all():
            responses = []
            for checkin in checkins:
                response = CategoryResponse.query.filter_by(
                    client_id=client.id,
                    category_id=category.id,
                    response_date=checkin.checkin_date
                ).first()
                if response:
                    responses.append(response.value)

            if responses:
                avg_value = sum(responses) / len(responses)
                cat_name = translate_category_name(category.name, lang)
                summary_stats.append(f"- {cat_name}: {avg_value:.1f}/5")

        # Generate language-specific email content
        if lang == 'he':
            email_content = f"""
שלום,

מצורף דוח הטיפול השבועי עבור מטופל {client.client_serial}.

תקופת הדוח: {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')} (שבוע {week_num}, {year})

סיכום:
- צ'ק-אינים שהושלמו: {checkins_completed}/7 ימים
{chr(10).join(summary_stats)}

הקובץ המצורף כולל:
- צ'ק-אינים יומיים מפורטים עם דירוגים צבעוניים
- סטטיסטיקות סיכום שבועיות
- מעקב השלמת יעדים
- הערות ומשימות מטפל

אנא עיין/י בדוח המצורף וצור/י קשר אם יש שאלות.

בברכה,
{therapist.name}
{therapist.organization or ''}
        """
        elif lang == 'ru':
            email_content = f"""
Здравствуйте,

Прилагается еженедельный терапевтический отчет для клиента {client.client_serial}.

Период отчета: {week_start.strftime('%d.%m.%Y')} - {week_end.strftime('%d.%m.%Y')} (Неделя {week_num}, {year})

Сводка:
- Выполнено отметок: {checkins_completed}/7 дней
{chr(10).join(summary_stats)}

Прилагаемый файл Excel содержит:
- Подробные ежедневные отметки с цветовой кодировкой
- Еженедельная сводная статистика
- Отслеживание выполнения целей
- Заметки и задания терапевта

Пожалуйста, просмотрите прилагаемый отчет и свяжитесь со мной, если у вас есть вопросы.

С наилучшими пожеланиями,
{therapist.name}
{therapist.organization or ''}
        """
        elif lang == 'ar':
            email_content = f"""
مرحباً،

يرجى الاطلاع على التقرير العلاجي الأسبوعي المرفق للعميل {client.client_serial}.

فترة التقرير: {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')} (الأسبوع {week_num}، {year})

الملخص:
- تسجيلات الحضور المكتملة: {checkins_completed}/7 أيام
{chr(10).join(summary_stats)}

يحتوي ملف Excel المرفق على:
- تسجيلات الحضور اليومية المفصلة مع التقييمات الملونة
- إحصائيات الملخص الأسبوعي
- تتبع إنجاز الأهداف
- ملاحظات ومهام المعالج

يرجى مراجعة التقرير المرفق والاتصال بي إذا كان لديك أي أسئلة.

مع أطيب التحيات،
{therapist.name}
{therapist.organization or ''}
        """
        else:  # Default to English
            email_content = f"""
Dear Colleague,

Please find attached the weekly therapy report for client {client.client_serial}.

Report Period: {week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')} (Week {week_num}, {year})

Summary:
- Check-ins completed: {checkins_completed}/7 days
{chr(10).join(summary_stats)}

The attached Excel file contains:
- Detailed daily check-ins with color-coded ratings
- Weekly summary statistics
- Goal completion tracking
- Therapist notes and missions

Please review the attached report and contact me if you have any questions.

Best regards,
{therapist.name}
{therapist.organization or ''}
        """

        # If no email configuration, return content for manual sending
        if not app.config.get('MAIL_USERNAME'):
            return jsonify({
                'success': True,
                'email_content': email_content.strip(),
                'recipient': recipient_email or therapist.user.email or 'Your email',
                'subject': f"Weekly Therapy Report - Client {client.client_serial} - Week {week_num}, {year}",
                'note': 'Email configuration not set up. Please copy this content and attach the downloaded Excel file to send manually.'
            })

        # If email is configured, send it
        try:
            # Create the Excel workbook using the shared function
            wb = create_weekly_report_excel(client, therapist, week_start, week_end, week_num, year, lang)

            # Save to BytesIO for email attachment
            excel_buffer = BytesIO()
            wb.save(excel_buffer)
            excel_buffer.seek(0)

            # Create email
            msg = MIMEMultipart()
            msg['From'] = app.config['MAIL_USERNAME']
            msg['To'] = recipient_email or therapist.user.email
            msg['Subject'] = f"Weekly Therapy Report - Client {client.client_serial} - Week {week_num}, {year}"

            # Email body
            msg.attach(MIMEText(email_content, 'plain'))

            # Attach Excel file
            excel_attachment = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            excel_attachment.set_payload(excel_buffer.read())
            encoders.encode_base64(excel_attachment)
            excel_attachment.add_header(
                'Content-Disposition',
                f'attachment; filename=therapy_report_{client.client_serial}_week_{week_num}_{year}.xlsx'
            )
            msg.attach(excel_attachment)

            # Send email
            server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
            server.starttls()
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.send_message(msg)
            server.quit()

            return jsonify({
                'success': True,
                'message': f'Report sent successfully to {recipient_email or therapist.user.email}'
            })

        except Exception as e:
            # Return the email content even if sending fails
            return jsonify({
                'success': True,
                'email_content': email_content.strip(),
                'recipient': recipient_email or therapist.user.email or 'Your email',
                'subject': f"Weekly Therapy Report - Client {client.client_serial} - Week {week_num}, {year}",
                'error': f'Failed to send email: {str(e)}',
                'note': 'Email could not be sent automatically. Please copy this content and send it manually.'
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= HEALTH CHECK =============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle unexpected exceptions"""
    db.session.rollback()
    app.logger.error(f"Unexpected error: {str(error)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500


# ============= STATIC FILE SERVING =============

@app.route('/reset-password.html')
def reset_password_page():
    """Serve the password reset page"""
    try:
        file_path = os.path.join(BASE_DIR, 'reset-password.html')
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            app.logger.error(f"reset-password.html not found at {file_path}")
            return "reset-password.html not found", 404
    except Exception as e:
        app.logger.error(f"Error serving reset-password.html: {e}")
        return f"Error: {str(e)}", 500


@app.route('/favicon.svg')
def favicon():
    """Serve favicon"""
    favicon_path = os.path.join(BASE_DIR, 'favicon.svg')
    if os.path.exists(favicon_path):
        return send_file(favicon_path, mimetype='image/svg+xml')
    else:
        return '', 204


# ============= INITIALIZATION =============

# Flag to ensure single initialization
_initialized = False


def initialize_database():
    """Initialize database with default data"""
    global _initialized
    if _initialized:
        return

    _initialized = True

    try:
        db.create_all()

        # Add default tracking categories if not exist
        if TrackingCategory.query.count() == 0:
            default_categories = [
                ('Emotion Level', 'Overall emotional state', True),
                ('Energy', 'Physical and mental energy levels', True),
                ('Social Activity', 'Engagement in social interactions', True),
                ('Sleep Quality', 'Quality of sleep', False),
                ('Anxiety Level', 'Level of anxiety experienced', False),
                ('Motivation', 'Level of motivation and drive', False),
                ('Medication', 'Medication adherence', True),
                ('Physical Activity', 'Physical activity level', True)
            ]

            for name, description, is_default in default_categories:
                category = TrackingCategory(
                    name=name,
                    description=description,
                    is_default=is_default
                )
                db.session.add(category)

            db.session.commit()
            print("Database initialized with default tracking categories")
    except Exception as e:
        print(f"Database initialization error: {e}")
        _initialized = False


# Initialize on first request
@app.before_request
def before_request():
    initialize_database()


# Don't initialize on import for production
# Let init_db.py handle it during deployment
if not os.environ.get('PRODUCTION'):
    with app.app_context():
        initialize_database()

# ============= MAIN ENTRY POINT =============

if __name__ == '__main__':
    # Ensure database is created when running directly
    with app.app_context():
        db.create_all()
        initialize_database()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=not os.environ.get('PRODUCTION'))




@app.route('/api/therapist/create-client', methods=['POST'])
@require_auth(['therapist'])
def create_client():
    """Create new client"""
    try:
        therapist = request.current_user.therapist
        data = request.json

        # Create user account for client
        email = data.get('email')
        password = data.get('password', secrets.token_urlsafe(8))

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        # Create user
        user = User(
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
            role='client'
        )
        db.session.add(user)
        db.session.flush()

        # Create client
        client = Client(
            user_id=user.id,
            client_serial=generate_client_serial(),
            therapist_id=therapist.id,
            start_date=date.today()
        )
        db.session.add(client)
        db.session.flush()

        # Always add ALL tracking categories
        all_categories = TrackingCategory.query.all()
        for category in all_categories:
            plan = ClientTrackingPlan(
                client_id=client.id,
                category_id=category.id,
                is_active=True  # All categories active by default
            )
            db.session.add(plan)

        # Add initial goals if provided
        goals = data.get('initial_goals', [])
        week_start = date.today() - timedelta(days=date.today().weekday())
        for goal_text in goals:
            if goal_text.strip():  # Only add non-empty goals
                goal = WeeklyGoal(
                    client_id=client.id,
                    therapist_id=therapist.id,
                    goal_text=goal_text,
                    week_start=week_start
                )
                db.session.add(goal)

        # Add welcome note
        welcome_note = TherapistNote(
            client_id=client.id,
            therapist_id=therapist.id,
            note_type='welcome',
            content=f"Welcome to therapy! Your journey begins today. Your temporary password is: {password}"
        )
        db.session.add(welcome_note)

        db.session.commit()

        return jsonify({
            'success': True,
            'client': {
                'id': client.id,
                'serial': client.client_serial,
                'email': email,
                'temporary_password': password
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/therapist/add-goal', methods=['POST'])
@require_auth(['therapist'])
def add_weekly_goal():
    """Add weekly goal for client"""
    try:
        therapist = request.current_user.therapist
        data = request.json

        client_id = data.get('client_id')
        goal_text = data.get('goal_text')
        week_start_str = data.get('week_start')

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Parse week start
        if week_start_str:
            week_start = datetime.strptime(week_start_str, '%Y-%m-%d').date()
        else:
            # Default to current week
            week_start = date.today() - timedelta(days=date.today().weekday())

        # Create goal
        goal = WeeklyGoal(
            client_id=client_id,
            therapist_id=therapist.id,
            goal_text=goal_text,
            week_start=week_start
        )
        db.session.add(goal)
        db.session.commit()

        return jsonify({
            'success': True,
            'goal': {
                'id': goal.id,
                'text': goal.goal_text,
                'week_start': goal.week_start.isoformat()
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/therapist/add-note', methods=['POST'])
@require_auth(['therapist'])
def add_therapist_note():
    """Add note or mission for client"""
    try:
        therapist = request.current_user.therapist
        data = request.json

        client_id = data.get('client_id')
        content = data.get('content')
        is_mission = data.get('is_mission', False)
        note_type = data.get('note_type', 'general')

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Create note
        note = TherapistNote(
            client_id=client_id,
            therapist_id=therapist.id,
            content=content,
            is_mission=is_mission,
            note_type=note_type
        )
        db.session.add(note)
        db.session.commit()

        return jsonify({
            'success': True,
            'note': {
                'id': note.id,
                'content': note.content,
                'is_mission': note.is_mission,
                'created_at': note.created_at.isoformat()
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= CLIENT ENDPOINTS =============

@app.route('/api/client/dashboard', methods=['GET'])
@require_auth(['client'])
def client_dashboard():
    """Get client dashboard data with translated category names"""
    try:
        client = request.current_user.client
        lang = get_language_from_header()

        # Get today's check-in status
        today_checkin = client.checkins.filter_by(checkin_date=date.today()).first()

        # Get active tracking categories with translations
        tracking_categories = []
        for plan in client.tracking_plans.filter_by(is_active=True):
            # Get today's response
            today_response = CategoryResponse.query.filter_by(
                client_id=client.id,
                category_id=plan.category_id,
                response_date=date.today()
            ).first()

            # Translate category name and description
            translated_name = translate_category_name(plan.category.name, lang)

            tracking_categories.append({
                'id': plan.category_id,
                'name': translated_name,
                'original_name': plan.category.name,
                'description': plan.category.description,  # Could also translate this
                'today_value': today_response.value if today_response else None
            })

        # Get this week's goals
        week_start = date.today() - timedelta(days=date.today().weekday())
        weekly_goals = []
        for goal in client.goals.filter_by(
                week_start=week_start,
                is_active=True
        ):
            # Get today's completion
            today_completion = goal.completions.filter_by(
                completion_date=date.today()
            ).first()

            weekly_goals.append({
                'id': goal.id,
                'text': goal.goal_text,
                'today_completed': today_completion.completed if today_completion else None
            })

        # Get reminders
        reminders = []
        for reminder in client.reminders.filter_by(is_active=True):
            reminders.append({
                'type': reminder.reminder_type,
                'time': reminder.reminder_time.strftime('%H:%M')
            })

        return jsonify({
            'success': True,
            'client': {
                'serial': client.client_serial,
                'start_date': client.start_date.isoformat()
            },
            'today': {
                'has_checkin': today_checkin is not None,
                'date': date.today().isoformat()
            },
            'tracking_categories': tracking_categories,
            'weekly_goals': weekly_goals,
            'reminders': reminders
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/checkin', methods=['POST'])
@require_auth(['client'])
def submit_checkin():
    """Submit daily check-in"""
    try:
        client = request.current_user.client
        data = request.json

        checkin_date = data.get('date', date.today().isoformat())
        checkin_date = datetime.strptime(checkin_date, '%Y-%m-%d').date()

        # Check if check-in exists
        existing = client.checkins.filter_by(checkin_date=checkin_date).first()

        if existing:
            # Update existing check-in
            existing.checkin_time = datetime.now().time()

            # Clear old category responses for this date
            CategoryResponse.query.filter_by(
                client_id=client.id,
                response_date=checkin_date
            ).delete()
        else:
            # Create new check-in
            checkin = DailyCheckin(
                client_id=client.id,
                checkin_date=checkin_date,
                checkin_time=datetime.now().time()
            )
            db.session.add(checkin)
            db.session.flush()
            existing = checkin

        # Process category responses
        category_responses = data.get('category_responses', {})
        category_notes = data.get('category_notes', {})

        for cat_id, value in category_responses.items():
            # Get category to check its name
            category = TrackingCategory.query.get(int(cat_id))
            if not category:
                continue

            # Create category response
            response = CategoryResponse(
                client_id=client.id,
                category_id=int(cat_id),
                response_date=checkin_date,
                value=value,
                notes=category_notes.get(cat_id, '')
            )
            db.session.add(response)

            # Also update the legacy fields in daily_checkins for backward compatibility
            if 'emotion' in category.name.lower():
                existing.emotional_value = value
                existing.emotional_notes = category_notes.get(cat_id, '')
            elif 'medication' in category.name.lower():
                existing.medication_value = value
                existing.medication_notes = category_notes.get(cat_id, '')
            elif 'physical activity' in category.name.lower() or 'activity' in category.name.lower():
                existing.activity_value = value
                existing.activity_notes = category_notes.get(cat_id, '')

        # Save goal completions
        goal_completions = data.get('goal_completions', {})
        for goal_id, completed in goal_completions.items():
            # Check if completion exists
            existing_completion = GoalCompletion.query.filter_by(
                goal_id=int(goal_id),
                completion_date=checkin_date
            ).first()

            if existing_completion:
                existing_completion.completed = completed
            else:
                completion = GoalCompletion(
                    goal_id=int(goal_id),
                    completion_date=checkin_date,
                    completed=completed
                )
                db.session.add(completion)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Check-in saved successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/progress', methods=['GET'])
@require_auth(['client'])
def get_client_progress():
    """Get client's progress data"""
    try:
        client = request.current_user.client

        # Get date range
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        # Get check-ins
        checkins = client.checkins.filter(
            DailyCheckin.checkin_date.between(start_date, end_date)
        ).order_by(DailyCheckin.checkin_date).all()

        checkin_data = []
        for checkin in checkins:
            checkin_data.append({
                'date': checkin.checkin_date.isoformat(),
                'emotional': checkin.emotional_value,
                'medication': checkin.medication_value,
                'activity': checkin.activity_value
            })

        # Get category responses
        category_data = {}
        for plan in client.tracking_plans.filter_by(is_active=True):
            responses = CategoryResponse.query.filter(
                CategoryResponse.client_id == client.id,
                CategoryResponse.category_id == plan.category_id,
                CategoryResponse.response_date.between(start_date, end_date)
            ).order_by(CategoryResponse.response_date).all()

            category_data[plan.category.name] = [
                {
                    'date': resp.response_date.isoformat(),
                    'value': resp.value
                } for resp in responses
            ]

        return jsonify({
            'success': True,
            'progress': {
                'checkins': checkin_data,
                'categories': category_data
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/change-password', methods=['POST'])
@require_auth(['client'])
def change_client_password():
    """Allow client to change their own password"""
    try:
        data = request.json
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        # Validate input
        if not all([current_password, new_password]):
            return jsonify({'error': 'Current password and new password are required'}), 400

        if len(new_password) < 8:
            return jsonify({'error': 'New password must be at least 8 characters long'}), 400

        # Verify current password
        user = request.current_user
        if not bcrypt.check_password_hash(user.password_hash, current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401

        # Update password
        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/missions', methods=['GET'])
@require_auth(['client'])
def get_client_missions():
    """Get client's missions from therapist"""
    try:
        client = request.current_user.client

        missions = TherapistNote.query.filter_by(
            client_id=client.id,
            is_mission=True
        ).order_by(TherapistNote.created_at.desc()).all()

        mission_data = []
        for mission in missions:
            mission_data.append({
                'id': mission.id,
                'content': mission.content,
                'completed': mission.mission_completed,
                'created_at': mission.created_at.isoformat(),
                'completed_at': mission.completed_at.isoformat() if mission.completed_at else None
            })

        return jsonify({
            'success': True,
            'missions': mission_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/complete-mission/<int:mission_id>', methods=['POST'])
@require_auth(['client'])
def complete_mission(mission_id):
    """Mark mission as completed"""
    try:
        client = request.current_user.client

        mission = TherapistNote.query.filter_by(
            id=mission_id,
            client_id=client.id,
            is_mission=True
        ).first()

        if not mission:
            return jsonify({'error': 'Mission not found'}), 404

        mission.mission_completed = True
        mission.completed_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Mission completed!'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= TRACKING CATEGORY MANAGEMENT =============

@app.route('/api/categories', methods=['GET'])
@require_auth(['therapist', 'client'])
def get_tracking_categories():
    """Get all tracking categories with translations"""
    try:
        lang = get_language_from_header()
        categories = TrackingCategory.query.all()

        category_data = []
        for category in categories:
            translated_name = translate_category_name(category.name, lang)
            category_data.append({
                'id': category.id,
                'name': translated_name,
                'original_name': category.name,  # Keep original for reference
                'description': category.description,
                'is_default': category.is_default,
                'scale_min': category.scale_min,
                'scale_max': category.scale_max
            })

        return jsonify({
            'success': True,
            'categories': category_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# NEW ENDPOINT - Added after /api/categories
@app.route('/api/categories/translated', methods=['GET'])
@require_auth(['therapist', 'client'])
def get_translated_categories():
    """Get all tracking categories with translations for current language"""
    try:
        lang = get_language_from_header()
        categories = TrackingCategory.query.all()

        category_data = []
        for category in categories:
            translated_name = translate_category_name(category.name, lang)
            # Also translate the description
            desc_key = category.name + '_desc'
            translated_desc = CATEGORY_TRANSLATIONS.get(lang, {}).get(
                desc_key,
                category.description
            )

            category_data.append({
                'id': category.id,
                'name': translated_name,
                'original_name': category.name,
                'description': translated_desc,
                'is_default': category.is_default,
                'scale_min': category.scale_min,
                'scale_max': category.scale_max
            })

        return jsonify({
            'success': True,
            'categories': category_data,
            'language': lang
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/therapist/update-tracking-plan', methods=['POST'])
@require_auth(['therapist'])
def update_client_tracking_plan():
    """Update client's tracking plan"""
    try:
        therapist = request.current_user.therapist
        data = request.json

        client_id = data.get('client_id')
        category_updates = data.get('categories', {})

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Update tracking plans
        for category_id, is_active in category_updates.items():
            plan = ClientTrackingPlan.query.filter_by(
                client_id=client_id,
                category_id=int(category_id)
            ).first()

            if plan:
                plan.is_active = is_active
            else:
                # Create new plan if doesn't exist
                plan = ClientTrackingPlan(
                    client_id=client_id,
                    category_id=int(category_id),
                    is_active=is_active
                )
                db.session.add(plan)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Tracking plan updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= REMINDER ENDPOINTS =============

@app.route('/api/client/reminders', methods=['GET'])
@require_auth(['client'])
def get_reminders():
    """Get client's reminders"""
    try:
        client = request.current_user.client

        reminders = client.reminders.filter_by(is_active=True).all()

        reminder_data = []
        for reminder in reminders:
            reminder_data.append({
                'id': reminder.id,
                'type': reminder.reminder_type,
                'time': reminder.reminder_time.strftime('%H:%M'),
                'last_sent': reminder.last_sent.isoformat() if reminder.last_sent else None
            })

        return jsonify({
            'success': True,
            'reminders': reminder_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/update-reminder', methods=['POST'])
@require_auth(['client'])
def update_reminder():
    """Update or create reminder"""
    try:
        client = request.current_user.client
        data = request.json

        reminder_type = data.get('type')
        reminder_time = data.get('time')
        is_active = data.get('is_active', True)

        # Parse time
        hour, minute = map(int, reminder_time.split(':'))
        time_obj = datetime.strptime(f"{hour:02d}:{minute:02d}", '%H:%M').time()

        # Check if reminder exists
        reminder = client.reminders.filter_by(reminder_type=reminder_type).first()

        if reminder:
            reminder.reminder_time = time_obj
            reminder.is_active = is_active
        else:
            reminder = Reminder(
                client_id=client.id,
                reminder_type=reminder_type,
                reminder_time=time_obj,
                is_active=is_active
            )
            db.session.add(reminder)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Reminder updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= PROFILE MANAGEMENT =============

@app.route('/api/user/profile', methods=['GET'])
@require_auth(['therapist', 'client'])
def get_user_profile():
    """Get user profile information"""
    try:
        user = request.current_user

        profile_data = {
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None
        }

        if user.role == 'therapist' and user.therapist:
            profile_data['therapist'] = {
                'name': user.therapist.name,
                'license_number': user.therapist.license_number,
                'organization': user.therapist.organization,
                'specializations': user.therapist.specializations or []
            }
        elif user.role == 'client' and user.client:
            profile_data['client'] = {
                'serial': user.client.client_serial,
                'start_date': user.client.start_date.isoformat(),
                'therapist_name': user.client.therapist.name if user.client.therapist else None
            }

        return jsonify({
            'success': True,
            'profile': profile_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/update-profile', methods=['POST'])
@require_auth(['therapist', 'client'])
def update_user_profile():
    """Update user profile"""
    try:
        user = request.current_user
        data = request.json

        # Update email if provided
        new_email = data.get('email')
        if new_email and new_email != user.email:
            # Check if email already exists
            if User.query.filter_by(email=new_email).first():
                return jsonify({'error': 'Email already in use'}), 400
            user.email = new_email

        # Update role-specific data
        if user.role == 'therapist' and user.therapist:
            if 'name' in data:
                user.therapist.name = data['name']
            if 'organization' in data:
                user.therapist.organization = data['organization']
            if 'specializations' in data:
                user.therapist.specializations = data['specializations']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= ANALYTICS ENDPOINTS =============

@app.route('/api/therapist/analytics/<int:client_id>', methods=['GET'])
@require_auth(['therapist'])
def get_client_analytics(client_id):
    """Get detailed analytics for a client"""
    try:
        therapist = request.current_user.therapist
        lang = get_language_from_header()

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Get date range from query params
        days = int(request.args.get('days', 30))
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        # Get check-in completion stats
        total_days = (end_date - start_date).days + 1
        checkins_count = client.checkins.filter(
            DailyCheckin.checkin_date.between(start_date, end_date)
        ).count()
        completion_rate = (checkins_count / total_days) * 100

        # Get category trends
        category_trends = {}
        for plan in client.tracking_plans.filter_by(is_active=True):
            responses = CategoryResponse.query.filter(
                CategoryResponse.client_id == client_id,
                CategoryResponse.category_id == plan.category_id,
                CategoryResponse.response_date.between(start_date, end_date)
            ).order_by(CategoryResponse.response_date).all()

            if responses:
                translated_name = translate_category_name(plan.category.name, lang)
                category_trends[translated_name] = {
                    'data': [
                        {
                            'date': resp.response_date.isoformat(),
                            'value': resp.value
                        } for resp in responses
                    ],
                    'average': sum(r.value for r in responses) / len(responses)
                }

        # Get goal completion stats
        goals = client.goals.filter(
            WeeklyGoal.week_start >= start_date
        ).all()

        goal_stats = {
            'total_goals': len(goals),
            'completion_data': []
        }

        for goal in goals:
            completions = goal.completions.all()
            completed_count = sum(1 for c in completions if c.completed)
            total_days = len(completions)
            goal_stats['completion_data'].append({
                'goal': goal.goal_text,
                'week_start': goal.week_start.isoformat(),
                'completion_rate': (completed_count / total_days * 100) if total_days > 0 else 0
            })

        # Get mission completion stats
        missions = TherapistNote.query.filter_by(
            client_id=client_id,
            therapist_id=therapist.id,
            is_mission=True
        ).all()
        completed_missions = sum(1 for m in missions if m.mission_completed)

        return jsonify({
            'success': True,
            'analytics': {
                'period': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat(),
                    'days': days
                },
                'completion': {
                    'rate': completion_rate,
                    'checkins': checkins_count,
                    'total_days': total_days
                },
                'category_trends': category_trends,
                'goals': goal_stats,
                'missions': {
                    'total': len(missions),
                    'completed': completed_missions,
                    'completion_rate': (completed_missions / len(missions) * 100) if missions else 0
                }
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= EXPORT ENDPOINTS =============

@app.route('/api/export/client-data/<int:client_id>', methods=['GET'])
@require_auth(['therapist'])
def export_client_data(client_id):
    """Export all client data as JSON"""
    try:
        therapist = request.current_user.therapist

        # Verify client belongs to therapist
        client = Client.query.filter_by(
            id=client_id,
            therapist_id=therapist.id
        ).first()

        if not client:
            return jsonify({'error': 'Client not found'}), 404

        # Compile all client data
        export_data = {
            'client': {
                'serial': client.client_serial,
                'start_date': client.start_date.isoformat(),
                'is_active': client.is_active,
                'created_at': client.created_at.isoformat()
            },
            'checkins': [],
            'category_responses': [],
            'goals': [],
            'notes': [],
            'reminders': []
        }

        # Get all check-ins
        for checkin in client.checkins.order_by(DailyCheckin.checkin_date):
            export_data['checkins'].append({
                'date': checkin.checkin_date.isoformat(),
                'time': checkin.checkin_time.strftime('%H:%M'),
                'emotional': checkin.emotional_value,
                'emotional_notes': checkin.emotional_notes,
                'medication': checkin.medication_value,
                'medication_notes': checkin.medication_notes,
                'activity': checkin.activity_value,
                'activity_notes': checkin.activity_notes
            })

        # Get all category responses
        responses = CategoryResponse.query.filter_by(client_id=client_id).order_by(CategoryResponse.response_date).all()
        for response in responses:
            export_data['category_responses'].append({
                'date': response.response_date.isoformat(),
                'category': response.category.name,
                'value': response.value,
                'notes': response.notes
            })

        # Get all goals
        for goal in client.goals.order_by(WeeklyGoal.week_start):
            goal_data = {
                'text': goal.goal_text,
                'week_start': goal.week_start.isoformat(),
                'is_active': goal.is_active,
                'completions': []
            }
            for completion in goal.completions.order_by(GoalCompletion.completion_date):
                goal_data['completions'].append({
                    'date': completion.completion_date.isoformat(),
                    'completed': completion.completed,
                    'notes': completion.notes
                })
            export_data['goals'].append(goal_data)

        # Get all therapist notes
        notes = TherapistNote.query.filter_by(
            client_id=client_id,
            therapist_id=therapist.id
        ).order_by(TherapistNote.created_at).all()

        for note in notes:
            export_data['notes'].append({
                'type': note.note_type,
                'content': note.content,
                'is_mission': note.is_mission,
                'completed': note.mission_completed,
                'created_at': note.created_at.isoformat(),
                'completed_at': note.completed_at.isoformat() if note.completed_at else None
            })

        # Get reminders
        for reminder in client.reminders.all():
            export_data['reminders'].append({
                'type': reminder.reminder_type,
                'time': reminder.reminder_time.strftime('%H:%M'),
                'is_active': reminder.is_active
            })

        return jsonify(export_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= ADMIN ENDPOINTS (if needed) =============




@app.route('/api/debug/categories', methods=['GET'])
@require_auth(['therapist'])
def debug_categories():
    """Debug endpoint to check category translations"""
    categories = TrackingCategory.query.all()
    lang = get_language_from_header()

    results = []
    for cat in categories:
        translation_exists = cat.name in CATEGORY_TRANSLATIONS.get(lang, {})
        translated_name = translate_category_name(cat.name, lang)

        results.append({
            'db_name': cat.name,
            'translation_exists': translation_exists,
            'translated_to': translated_name,
            'is_same': cat.name == translated_name
        })

    return jsonify({
        'language': lang,
        'categories': results
    })


# ============= CLIENT REPORT ENDPOINTS =============



@app.route('/api/client/email-report', methods=['POST'])
@require_auth(['client'])
def client_email_report():
    """Prepare email report for client to send to therapist with translations"""
    try:
        client = request.current_user.client
        lang = get_language_from_header()
        data = request.json
        week = data.get('week')

        if not week:
            return jsonify({'error': 'Week is required'}), 400

        # Parse week
        year, week_num = week.split('-W')
        year = int(year)
        week_num = int(week_num)

        # Calculate week dates
        jan1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan1.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7
        first_monday = jan1 + timedelta(days=days_to_monday - 7)
        week_start = first_monday + timedelta(weeks=week_num - 1)
        week_end = week_start + timedelta(days=6)

        # Get therapist info
        therapist = client.therapist
        therapist_email = therapist.user.email if therapist and therapist.user else "therapist@example.com"
        therapist_name = therapist.name if therapist else "Therapist"

        # Get check-ins for the week
        checkins = client.checkins.filter(
            DailyCheckin.checkin_date.between(week_start.date(), week_end.date())
        ).order_by(DailyCheckin.checkin_date).all()

        # Get translations
        trans = lambda key: translate_report_term(key, lang)
        days = DAYS_TRANSLATIONS.get(lang, DAYS_TRANSLATIONS['en'])

        # Build translated email content
        if lang == 'he':
            subject = f"דוח טיפולי שבועי - {client.client_serial} - שבוע {week_num}, {year}"
            content = f"""מטפל יקר,

הנה דוח ההתקדמות השבועי שלי עבור {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')}.

מטופל: {client.client_serial}
שבוע: {week_num}, {year}
צ׳ק-אינים שהושלמו: {len(checkins)}/7

סיכום צ׳ק-אין יומי:
"""
        elif lang == 'ru':
            subject = f"Еженедельный терапевтический отчет - {client.client_serial} - Неделя {week_num}, {year}"
            content = f"""Уважаемый терапевт,

Вот мой еженедельный отчет о прогрессе за {week_start.strftime('%d.%m.%Y')} - {week_end.strftime('%d.%m.%Y')}.

КЛИЕНТ: {client.client_serial}
НЕДЕЛЯ: {week_num}, {year}
ВЫПОЛНЕНО ОТМЕТОК: {len(checkins)}/7

ЕЖЕДНЕВНАЯ СВОДКА ОТМЕТОК:
"""
        elif lang == 'ar':
            subject = f"التقرير العلاجي الأسبوعي - {client.client_serial} - الأسبوع {week_num}, {year}"
            content = f"""المعالج العزيز،

هذا هو تقرير التقدم الأسبوعي الخاص بي لـ {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')}.

العميل: {client.client_serial}
الأسبوع: {week_num}, {year}
تسجيلات الحضور المكتملة: {len(checkins)}/7

ملخص تسجيل الحضور اليومي:
"""
        else:  # English
            subject = f"Weekly Therapy Report - {client.client_serial} - Week {week_num}, {year}"
            content = f"""Dear {therapist_name},

Here is my weekly progress report for {week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}.

CLIENT: {client.client_serial}
WEEK: {week_num}, {year}
CHECK-INS COMPLETED: {len(checkins)}/7

DAILY CHECK-IN SUMMARY:
"""

        # Add daily details with proper translations
        for i in range(7):
            current_date = week_start + timedelta(days=i)
            checkin = next((c for c in checkins if c.checkin_date == current_date.date()), None)

            content += f"\n{days[i]} ({current_date.strftime('%m/%d')}):\n"

            if checkin:
                content += f"  ✓ {trans('checkin_time')}: {checkin.checkin_time.strftime('%H:%M')}\n"

                # Get translated category responses
                category_responses = CategoryResponse.query.filter_by(
                    client_id=client.id,
                    response_date=current_date.date()
                ).all()

                for response in category_responses:
                    cat_name = translate_category_name(response.category.name, lang)
                    content += f"  - {cat_name}: {response.value}/5"
                    if response.notes:
                        content += f" ({trans('notes')}: {response.notes})"
                    content += "\n"
            else:
                content += f"  ✗ {trans('no_checkin')}\n"

        # Add summary with translations
        if checkins:
            content += f"\n{trans('weekly_summary').upper()}:\n"

            total_checkins = len(checkins)

            # Calculate averages from category responses
            for category in TrackingCategory.query.all():
                responses = []
                for checkin in checkins:
                    response = CategoryResponse.query.filter_by(
                        client_id=client.id,
                        category_id=category.id,
                        response_date=checkin.checkin_date
                    ).first()
                    if response:
                        responses.append(response.value)

                if responses:
                    avg_value = sum(responses) / len(responses)
                    cat_name = translate_category_name(category.name, lang)
                    content += f"- {cat_name}: {avg_value:.1f}/5\n"

            content += f"- {trans('completion_rate')}: {total_checkins}/7 {trans('days')} ({(total_checkins / 7) * 100:.0f}%)\n"

        # Add goals if any
        weekly_goals = client.goals.filter_by(week_start=week_start.date()).all()
        if weekly_goals:
            content += f"\n{trans('weekly_goals').upper()}:\n"
            for goal in weekly_goals:
                completions = goal.completions.filter(
                    GoalCompletion.completion_date.between(week_start.date(), week_end.date())
                ).all()
                completed_days = sum(1 for c in completions if c.completed)
                content += f"- {goal.goal_text}: {trans('completed')} {completed_days}/7 {trans('days')}\n"

        # Add footer with proper translation
        if lang == 'he':
            content += f"\nהדוח נוצר בתאריך: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\nבברכה,\nמטופל {client.client_serial}"
        elif lang == 'ru':
            content += f"\nОтчет создан: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\nС уважением,\nКлиент {client.client_serial}"
        elif lang == 'ar':
            content += f"\nتم إنشاء التقرير في: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\nمع أطيب التحيات،\nالعميل {client.client_serial}"
        else:
            content += f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\nBest regards,\nClient {client.client_serial}"

        return jsonify({
            'success': True,
            'recipient': therapist_email,
            'subject': subject,
            'email_content': content,
            'note': 'Copy this email content to send to your therapist'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/week-checkins/<week>', methods=['GET'])
@require_auth(['client'])
def get_client_week_checkins(week):
    """Get client's check-ins for a specific week"""
    try:
        client = request.current_user.client

        # Parse week
        year, week_num = week.split('-W')
        year = int(year)
        week_num = int(week_num)

        # Calculate week dates
        jan1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan1.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7
        first_monday = jan1 + timedelta(days=days_to_monday - 7)
        week_start = first_monday + timedelta(weeks=week_num - 1)
        week_end = week_start + timedelta(days=6)

        # Get check-ins
        checkins = client.checkins.filter(
            DailyCheckin.checkin_date.between(week_start.date(), week_end.date())
        ).all()

        # Format response
        checkin_data = {}
        for checkin in checkins:
            checkin_data[checkin.checkin_date.isoformat()] = {
                'time': checkin.checkin_time.strftime('%H:%M'),
                'emotional': checkin.emotional_value,
                'emotional_notes': checkin.emotional_notes,
                'medication': checkin.medication_value,
                'medication_notes': checkin.medication_notes,
                'activity': checkin.activity_value,
                'activity_notes': checkin.activity_notes
            }

        return jsonify({
            'success': True,
            'week_start': week_start.date().isoformat(),
            'week_end': week_end.date().isoformat(),
            'checkins': checkin_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/client/goals/<week>', methods=['GET'])
@require_auth(['client'])
def get_client_week_goals(week):
    """Get client's goals for a specific week"""
    try:
        client = request.current_user.client

        # Parse week
        year, week_num = week.split('-W')
        year = int(year)
        week_num = int(week_num)

        # Calculate week start
        jan1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan1.weekday()) % 7
        if days_to_monday == 0:
            days_to_monday = 7
        first_monday = jan1 + timedelta(days=days_to_monday - 7)
        week_start = first_monday + timedelta(weeks=week_num - 1)

        # Get goals for the week
        goals = client.goals.filter_by(
            week_start=week_start.date(),
            is_active=True
        ).all()

        # Format response
        goals_data = []
        for goal in goals:
            # Get completions for the week
            completions = {}
            for i in range(7):
                day = week_start.date() + timedelta(days=i)
                completion = goal.completions.filter_by(completion_date=day).first()
                completions[day.isoformat()] = completion.completed if completion else None

            goals_data.append({
                'id': goal.id,
                'text': goal.goal_text,
                'week_start': goal.week_start.isoformat(),
                'completions': completions
            })

        return jsonify({
            'success': True,
            'goals': goals_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# The create_weekly_report_excel function continues from Part 1
# It's already complete in Part 1, starting at line 2324


# ============= REPORT GENERATION =============




# The email_therapy_report function is already complete in Part 1
# It's the UPDATED version starting at line 2773


# ============= HEALTH CHECK =============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle unexpected exceptions"""
    db.session.rollback()
    app.logger.error(f"Unexpected error: {str(error)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500


# ============= STATIC FILE SERVING =============

@app.route('/reset-password.html')
def reset_password_page():
    """Serve the password reset page"""
    try:
        file_path = os.path.join(BASE_DIR, 'reset-password.html')
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            app.logger.error(f"reset-password.html not found at {file_path}")
            return "reset-password.html not found", 404
    except Exception as e:
        app.logger.error(f"Error serving reset-password.html: {e}")
        return f"Error: {str(e)}", 500





# ============= INITIALIZATION =============

# Flag to ensure single initialization
_initialized = False


def initialize_database():
    """Initialize database with default data"""
    global _initialized
    if _initialized:
        return

    _initialized = True

    try:
        db.create_all()

        # Add default tracking categories if not exist
        if TrackingCategory.query.count() == 0:
            default_categories = [
                ('Emotion Level', 'Overall emotional state', True),
                ('Energy', 'Physical and mental energy levels', True),
                ('Social Activity', 'Engagement in social interactions', True),
                ('Sleep Quality', 'Quality of sleep', False),
                ('Anxiety Level', 'Level of anxiety experienced', False),
                ('Motivation', 'Level of motivation and drive', False),
                ('Medication', 'Medication adherence', True),
                ('Physical Activity', 'Physical activity level', True)
            ]

            for name, description, is_default in default_categories:
                category = TrackingCategory(
                    name=name,
                    description=description,
                    is_default=is_default
                )
                db.session.add(category)

            db.session.commit()
            print("Database initialized with default tracking categories")
    except Exception as e:
        print(f"Database initialization error: {e}")
        _initialized = False


# Initialize on first request
@app.before_request
def before_request():
    initialize_database()


# Don't initialize on import for production
# Let init_db.py handle it during deployment
if not os.environ.get('PRODUCTION'):
    with app.app_context():
        initialize_database()

# ============= MAIN ENTRY POINT =============

if __name__ == '__main__':
    # Ensure database is created when running directly
    with app.app_context():
        db.create_all()
        initialize_database()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=not os.environ.get('PRODUCTION'))