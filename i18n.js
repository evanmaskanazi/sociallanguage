// i18n.js - Internationalization Module for Therapeutic Companion
// Place this file in your project root and include it in all HTML files

const i18n = {
    // Current language
    currentLang: localStorage.getItem('userLanguage') || 'en',
    
    // RTL languages
    rtlLanguages: ['he', 'ar'],
    
    // Translations
    translations: {
        en: {
            // Common
            'app.title': 'Therapeutic Companion',
            'app.tagline': 'Your Journey to Wellness',
            'btn.login': 'Login',
            'btn.register': 'Register',
            'btn.logout': 'Logout',
            'btn.save': 'Save',
            'btn.cancel': 'Cancel',
            'btn.submit': 'Submit',
            'btn.back': 'Back',
            'btn.next': 'Next',
            'btn.close': 'Close',
            'btn.add': 'Add',
            'btn.edit': 'Edit',
            'btn.delete': 'Delete',
            'btn.download': 'Download',
            'btn.generate': 'Generate',
            
            // Navigation
            'nav.overview': 'Overview',
            'nav.clients': 'Clients',
            'nav.checkin': 'Check-in',
            'nav.goals': 'Goals',
            'nav.progress': 'Progress',
            'nav.reports': 'Reports',
            'nav.add_client': 'Add Client',
            
            // Login Page
            'login.title': 'Login to Your Account',
            'login.email': 'Email',
            'login.password': 'Password',
            'login.forgot_password': 'Forgot your password?',
            'login.remember_me': 'Remember me',
            'login.no_account': "Don't have an account?",
            'login.error': 'Invalid email or password',
            
            // Registration
            'register.title': 'Create Account',
            'register.therapist': 'Therapist Registration',
            'register.full_name': 'Full Name',
            'register.license': 'License Number',
            'register.organization': 'Organization',
            'register.confirm_password': 'Confirm Password',
            'register.terms': 'I agree to the Terms of Service',
            
            // Dashboard
            'dashboard.welcome': 'Welcome back',
            'dashboard.good_morning': 'Good morning',
            'dashboard.good_afternoon': 'Good afternoon',
            'dashboard.good_evening': 'Good evening',
            'dashboard.today': 'Today',
            'dashboard.this_week': 'This Week',
            'dashboard.total_clients': 'Total Clients',
            'dashboard.active_clients': 'Active Clients',
            'dashboard.recent_checkins': 'Recent Check-ins',
            'dashboard.pending_missions': 'Pending Missions',
            
            // Client Management
            'client.serial': 'Client ID',
            'client.start_date': 'Start Date',
            'client.status': 'Status',
            'client.active': 'Active',
            'client.inactive': 'Inactive',
            'client.last_checkin': 'Last Check-in',
            'client.completion_rate': 'Completion Rate',
            'client.tracking': 'Tracking',
            'client.actions': 'Actions',
            'client.view': 'View',
            'client.add_goal': 'Add Goal',
            'client.add_note': 'Add Note',
            
            // Check-in
            'checkin.title': 'Daily Check-in',
            'checkin.date': 'Date',
            'checkin.emotional': 'How is your emotional state?',
            'checkin.medication': 'Did you take your medication as prescribed?',
            'checkin.activity': 'How active were you?',
            'checkin.notes': 'Additional notes (optional)',
            'checkin.scale_1': 'Very Poor',
            'checkin.scale_2': 'Poor',
            'checkin.scale_3': 'Fair',
            'checkin.scale_4': 'Good',
            'checkin.scale_5': 'Excellent',
            'checkin.med_yes': 'Yes',
            'checkin.med_no': 'No',
            'checkin.med_partial': 'Partial',
            'checkin.med_na': 'N/A',
            
            // Goals
            'goals.weekly': 'Weekly Goals',
            'goals.add': 'Add New Goal',
            'goals.completed': 'Completed',
            'goals.pending': 'Pending',
            'goals.text': 'Goal Description',
            
            // Reports
            'reports.generate': 'Generate Report',
            'reports.weekly': 'Weekly Report',
            'reports.select_client': 'Select Client',
            'reports.select_week': 'Select Week',
            'reports.excel': 'Download Excel',
            'reports.email': 'Email Report',
            
            // Messages
            'msg.success': 'Success!',
            'msg.error': 'Error',
            'msg.loading': 'Loading...',
            'msg.saved': 'Changes saved successfully',
            'msg.deleted': 'Deleted successfully',
            'msg.confirm_delete': 'Are you sure you want to delete this?',
            'msg.no_data': 'No data available',
            'msg.never': 'Never',
            
            // Days of week
            'day.monday': 'Monday',
            'day.tuesday': 'Tuesday',
            'day.wednesday': 'Wednesday',
            'day.thursday': 'Thursday',
            'day.friday': 'Friday',
            'day.saturday': 'Saturday',
            'day.sunday': 'Sunday',
            'day.mon': 'Mon',
            'day.tue': 'Tue',
            'day.wed': 'Wed',
            'day.thu': 'Thu',
            'day.fri': 'Fri',
            'day.sat': 'Sat',
            'day.sun': 'Sun',
            
            // Months
            'month.january': 'January',
            'month.february': 'February',
            'month.march': 'March',
            'month.april': 'April',
            'month.may': 'May',
            'month.june': 'June',
            'month.july': 'July',
            'month.august': 'August',
            'month.september': 'September',
            'month.october': 'October',
            'month.november': 'November',
            'month.december': 'December',
            
            // Additional translations added by pages
            'therapist.to': 'To',
            'therapist.subject': 'Subject',
            'therapist.email_preview': 'Email Report Preview',
            'therapist.copy_email_note': 'Copy this content to send via your email client',
            'therapist.save_credentials': 'Please save these credentials for the client. This message will remain visible until you leave this tab.',
            'therapist.started': 'Started',
            'therapist.client_info': 'Client Information',
            'therapist.week_progress': 'This Week\'s Progress',
            'therapist.active_goals': 'Active Goals',
            'therapist.no_active_goals': 'No active goals for this week',
            'therapist.add_note_mission': 'Add Note or Mission',
            'therapist.enter_note_placeholder': 'Enter your note or mission...',
            'therapist.recent_notes': 'Recent Notes & Missions',
            'therapist.mission': 'MISSION',
            'therapist.no_notes': 'No notes yet'
        },
        
        he: {
            // Common
            'app.title': 'מלווה טיפולי',
            'app.tagline': 'המסע שלך לבריאות',
            'btn.login': 'התחברות',
            'btn.register': 'הרשמה',
            'btn.logout': 'יציאה',
            'btn.save': 'שמירה',
            'btn.cancel': 'ביטול',
            'btn.submit': 'שליחה',
            'btn.back': 'חזרה',
            'btn.next': 'הבא',
            'btn.close': 'סגירה',
            'btn.add': 'הוספה',
            'btn.edit': 'עריכה',
            'btn.delete': 'מחיקה',
            'btn.download': 'הורדה',
            'btn.generate': 'יצירה',
            
            // Navigation
            'nav.overview': 'סקירה כללית',
            'nav.clients': 'מטופלים',
            'nav.checkin': 'צ׳ק-אין',
            'nav.goals': 'יעדים',
            'nav.progress': 'התקדמות',
            'nav.reports': 'דוחות',
            'nav.add_client': 'הוספת מטופל',
            
            // Login Page
            'login.title': 'התחברות לחשבון',
            'login.email': 'דוא״ל',
            'login.password': 'סיסמה',
            'login.forgot_password': 'שכחת סיסמה?',
            'login.remember_me': 'זכור אותי',
            'login.no_account': 'אין לך חשבון?',
            'login.error': 'דוא״ל או סיסמה שגויים',
            
            // Registration
            'register.title': 'יצירת חשבון',
            'register.therapist': 'רישום מטפל',
            'register.full_name': 'שם מלא',
            'register.license': 'מספר רישיון',
            'register.organization': 'ארגון',
            'register.confirm_password': 'אימות סיסמה',
            'register.terms': 'אני מסכים לתנאי השירות',
            
            // Dashboard
            'dashboard.welcome': 'ברוך הבא',
            'dashboard.good_morning': 'בוקר טוב',
            'dashboard.good_afternoon': 'צהריים טובים',
            'dashboard.good_evening': 'ערב טוב',
            'dashboard.today': 'היום',
            'dashboard.this_week': 'השבוע',
            'dashboard.total_clients': 'סך כל המטופלים',
            'dashboard.active_clients': 'מטופלים פעילים',
            'dashboard.recent_checkins': 'צ׳ק-אין אחרונים',
            'dashboard.pending_missions': 'משימות ממתינות',
            
            // Client Management
            'client.serial': 'מזהה מטופל',
            'client.start_date': 'תאריך התחלה',
            'client.status': 'סטטוס',
            'client.active': 'פעיל',
            'client.inactive': 'לא פעיל',
            'client.last_checkin': 'צ׳ק-אין אחרון',
            'client.completion_rate': 'אחוז השלמה',
            'client.tracking': 'מעקב',
            'client.actions': 'פעולות',
            'client.view': 'צפייה',
            'client.add_goal': 'הוספת יעד',
            'client.add_note': 'הוספת הערה',
            
            // Check-in
            'checkin.title': 'צ׳ק-אין יומי',
            'checkin.date': 'תאריך',
            'checkin.emotional': 'איך המצב הרגשי שלך?',
            'checkin.medication': 'האם נטלת את התרופות כמתוכנן?',
            'checkin.activity': 'כמה פעיל היית?',
            'checkin.notes': 'הערות נוספות (אופציונלי)',
            'checkin.scale_1': 'גרוע מאוד',
            'checkin.scale_2': 'גרוע',
            'checkin.scale_3': 'בינוני',
            'checkin.scale_4': 'טוב',
            'checkin.scale_5': 'מצוין',
            'checkin.med_yes': 'כן',
            'checkin.med_no': 'לא',
            'checkin.med_partial': 'חלקי',
            'checkin.med_na': 'לא רלוונטי',
            
            // Goals
            'goals.weekly': 'יעדים שבועיים',
            'goals.add': 'הוספת יעד חדש',
            'goals.completed': 'הושלם',
            'goals.pending': 'ממתין',
            'goals.text': 'תיאור היעד',
            
            // Reports
            'reports.generate': 'יצירת דוח',
            'reports.weekly': 'דוח שבועי',
            'reports.select_client': 'בחר מטופל',
            'reports.select_week': 'בחר שבוע',
            'reports.excel': 'הורדת אקסל',
            'reports.email': 'שליחת דוח במייל',
            
            // Messages
            'msg.success': 'הצלחה!',
            'msg.error': 'שגיאה',
            'msg.loading': 'טוען...',
            'msg.saved': 'השינויים נשמרו בהצלחה',
            'msg.deleted': 'נמחק בהצלחה',
            'msg.confirm_delete': 'האם אתה בטוח שברצונך למחוק?',
            'msg.no_data': 'אין נתונים זמינים',
            'msg.never': 'אף פעם',
            
            // Days of week
            'day.monday': 'יום שני',
            'day.tuesday': 'יום שלישי',
            'day.wednesday': 'יום רביעי',
            'day.thursday': 'יום חמישי',
            'day.friday': 'יום שישי',
            'day.saturday': 'שבת',
            'day.sunday': 'יום ראשון',
            'day.mon': 'ב׳',
            'day.tue': 'ג׳',
            'day.wed': 'ד׳',
            'day.thu': 'ה׳',
            'day.fri': 'ו׳',
            'day.sat': 'ש׳',
            'day.sun': 'א׳',
            
            // Months
            'month.january': 'ינואר',
            'month.february': 'פברואר',
            'month.march': 'מרץ',
            'month.april': 'אפריל',
            'month.may': 'מאי',
            'month.june': 'יוני',
            'month.july': 'יולי',
            'month.august': 'אוגוסט',
            'month.september': 'ספטמבר',
            'month.october': 'אוקטובר',
            'month.november': 'נובמבר',
            'month.december': 'דצמבר',
            
            // Additional translations
            'therapist.to': 'אל',
            'therapist.subject': 'נושא',
            'therapist.email_preview': 'תצוגה מקדימה של דוח דוא״ל',
            'therapist.copy_email_note': 'העתק תוכן זה כדי לשלוח דרך הדוא״ל שלך',
            'therapist.save_credentials': 'אנא שמור את האישורים האלה עבור המטופל. הודעה זו תישאר גלויה עד שתעזוב את הלשונית הזו.',
            'therapist.started': 'התחיל',
            'therapist.client_info': 'פרטי מטופל',
            'therapist.week_progress': 'התקדמות השבוע',
            'therapist.active_goals': 'יעדים פעילים',
            'therapist.no_active_goals': 'אין יעדים פעילים לשבוע זה',
            'therapist.add_note_mission': 'הוספת הערה או משימה',
            'therapist.enter_note_placeholder': 'הזן את ההערה או המשימה שלך...',
            'therapist.recent_notes': 'הערות ומשימות אחרונות',
            'therapist.mission': 'משימה',
            'therapist.no_notes': 'אין הערות עדיין'
        },
        
        ru: {
            // Common
            'app.title': 'Терапевтический Компаньон',
            'app.tagline': 'Ваш путь к здоровью',
            'btn.login': 'Войти',
            'btn.register': 'Регистрация',
            'btn.logout': 'Выйти',
            'btn.save': 'Сохранить',
            'btn.cancel': 'Отмена',
            'btn.submit': 'Отправить',
            'btn.back': 'Назад',
            'btn.next': 'Далее',
            'btn.close': 'Закрыть',
            'btn.add': 'Добавить',
            'btn.edit': 'Редактировать',
            'btn.delete': 'Удалить',
            'btn.download': 'Скачать',
            'btn.generate': 'Создать',
            
            // Navigation
            'nav.overview': 'Обзор',
            'nav.clients': 'Клиенты',
            'nav.checkin': 'Отметка',
            'nav.goals': 'Цели',
            'nav.progress': 'Прогресс',
            'nav.reports': 'Отчеты',
            'nav.add_client': 'Добавить клиента',
            
            // Login Page
            'login.title': 'Вход в аккаунт',
            'login.email': 'Электронная почта',
            'login.password': 'Пароль',
            'login.forgot_password': 'Забыли пароль?',
            'login.remember_me': 'Запомнить меня',
            'login.no_account': 'Нет аккаунта?',
            'login.error': 'Неверный email или пароль',
            
            // Registration
            'register.title': 'Создать аккаунт',
            'register.therapist': 'Регистрация терапевта',
            'register.full_name': 'Полное имя',
            'register.license': 'Номер лицензии',
            'register.organization': 'Организация',
            'register.confirm_password': 'Подтвердите пароль',
            'register.terms': 'Я согласен с условиями использования',
            
            // Dashboard
            'dashboard.welcome': 'С возвращением',
            'dashboard.good_morning': 'Доброе утро',
            'dashboard.good_afternoon': 'Добрый день',
            'dashboard.good_evening': 'Добрый вечер',
            'dashboard.today': 'Сегодня',
            'dashboard.this_week': 'Эта неделя',
            'dashboard.total_clients': 'Всего клиентов',
            'dashboard.active_clients': 'Активные клиенты',
            'dashboard.recent_checkins': 'Недавние отметки',
            'dashboard.pending_missions': 'Ожидающие задания',
            
            // Client Management
            'client.serial': 'ID клиента',
            'client.start_date': 'Дата начала',
            'client.status': 'Статус',
            'client.active': 'Активный',
            'client.inactive': 'Неактивный',
            'client.last_checkin': 'Последняя отметка',
            'client.completion_rate': 'Процент выполнения',
            'client.tracking': 'Отслеживание',
            'client.actions': 'Действия',
            'client.view': 'Просмотр',
            'client.add_goal': 'Добавить цель',
            'client.add_note': 'Добавить заметку',
            
            // Check-in
            'checkin.title': 'Ежедневная отметка',
            'checkin.date': 'Дата',
            'checkin.emotional': 'Как ваше эмоциональное состояние?',
            'checkin.medication': 'Вы приняли лекарства как предписано?',
            'checkin.activity': 'Насколько вы были активны?',
            'checkin.notes': 'Дополнительные заметки (необязательно)',
            'checkin.scale_1': 'Очень плохо',
            'checkin.scale_2': 'Плохо',
            'checkin.scale_3': 'Нормально',
            'checkin.scale_4': 'Хорошо',
            'checkin.scale_5': 'Отлично',
            'checkin.med_yes': 'Да',
            'checkin.med_no': 'Нет',
            'checkin.med_partial': 'Частично',
            'checkin.med_na': 'Не применимо',
            
            // Goals
            'goals.weekly': 'Недельные цели',
            'goals.add': 'Добавить новую цель',
            'goals.completed': 'Выполнено',
            'goals.pending': 'В ожидании',
            'goals.text': 'Описание цели',
            
            // Reports
            'reports.generate': 'Создать отчет',
            'reports.weekly': 'Недельный отчет',
            'reports.select_client': 'Выберите клиента',
            'reports.select_week': 'Выберите неделю',
            'reports.excel': 'Скачать Excel',
            'reports.email': 'Отправить отчет',
            
            // Messages
            'msg.success': 'Успешно!',
            'msg.error': 'Ошибка',
            'msg.loading': 'Загрузка...',
            'msg.saved': 'Изменения успешно сохранены',
            'msg.deleted': 'Успешно удалено',
            'msg.confirm_delete': 'Вы уверены, что хотите удалить?',
            'msg.no_data': 'Нет доступных данных',
            'msg.never': 'Никогда',
            
            // Days of week
            'day.monday': 'Понедельник',
            'day.tuesday': 'Вторник',
            'day.wednesday': 'Среда',
            'day.thursday': 'Четверг',
            'day.friday': 'Пятница',
            'day.saturday': 'Суббота',
            'day.sunday': 'Воскресенье',
            'day.mon': 'Пн',
            'day.tue': 'Вт',
            'day.wed': 'Ср',
            'day.thu': 'Чт',
            'day.fri': 'Пт',
            'day.sat': 'Сб',
            'day.sun': 'Вс',
            
            // Months
            'month.january': 'Январь',
            'month.february': 'Февраль',
            'month.march': 'Март',
            'month.april': 'Апрель',
            'month.may': 'Май',
            'month.june': 'Июнь',
            'month.july': 'Июль',
            'month.august': 'Август',
            'month.september': 'Сентябрь',
            'month.october': 'Октябрь',
            'month.november': 'Ноябрь',
            'month.december': 'Декабрь',
            
            // Additional translations
            'therapist.to': 'Кому',
            'therapist.subject': 'Тема',
            'therapist.email_preview': 'Предварительный просмотр отчета по электронной почте',
            'therapist.copy_email_note': 'Скопируйте это содержимое для отправки через вашу электронную почту',
            'therapist.save_credentials': 'Пожалуйста, сохраните эти учетные данные для клиента. Это сообщение останется видимым, пока вы не покинете эту вкладку.',
            'therapist.started': 'Начато',
            'therapist.client_info': 'Информация о клиенте',
            'therapist.week_progress': 'Прогресс за эту неделю',
            'therapist.active_goals': 'Активные цели',
            'therapist.no_active_goals': 'Нет активных целей на эту неделю',
            'therapist.add_note_mission': 'Добавить заметку или миссию',
            'therapist.enter_note_placeholder': 'Введите вашу заметку или миссию...',
            'therapist.recent_notes': 'Недавние заметки и миссии',
            'therapist.mission': 'МИССИЯ',
            'therapist.no_notes': 'Заметок пока нет'
        },
        
        ar: {
            // Common
            'app.title': 'الرفيق العلاجي',
            'app.tagline': 'رحلتك نحو العافية',
            'btn.login': 'تسجيل الدخول',
            'btn.register': 'التسجيل',
            'btn.logout': 'تسجيل الخروج',
            'btn.save': 'حفظ',
            'btn.cancel': 'إلغاء',
            'btn.submit': 'إرسال',
            'btn.back': 'رجوع',
            'btn.next': 'التالي',
            'btn.close': 'إغلاق',
            'btn.add': 'إضافة',
            'btn.edit': 'تعديل',
            'btn.delete': 'حذف',
            'btn.download': 'تحميل',
            'btn.generate': 'إنشاء',
            
            // Navigation
            'nav.overview': 'نظرة عامة',
            'nav.clients': 'العملاء',
            'nav.checkin': 'تسجيل الحضور',
            'nav.goals': 'الأهداف',
            'nav.progress': 'التقدم',
            'nav.reports': 'التقارير',
            'nav.add_client': 'إضافة عميل',
            
            // Login Page
            'login.title': 'تسجيل الدخول إلى حسابك',
            'login.email': 'البريد الإلكتروني',
            'login.password': 'كلمة المرور',
            'login.forgot_password': 'نسيت كلمة المرور؟',
            'login.remember_me': 'تذكرني',
            'login.no_account': 'ليس لديك حساب؟',
            'login.error': 'البريد الإلكتروني أو كلمة المرور غير صحيحة',
            
            // Registration
            'register.title': 'إنشاء حساب',
            'register.therapist': 'تسجيل المعالج',
            'register.full_name': 'الاسم الكامل',
            'register.license': 'رقم الرخصة',
            'register.organization': 'المنظمة',
            'register.confirm_password': 'تأكيد كلمة المرور',
            'register.terms': 'أوافق على شروط الخدمة',
            
            // Dashboard
            'dashboard.welcome': 'مرحباً بعودتك',
            'dashboard.good_morning': 'صباح الخير',
            'dashboard.good_afternoon': 'مساء الخير',
            'dashboard.good_evening': 'مساء الخير',
            'dashboard.today': 'اليوم',
            'dashboard.this_week': 'هذا الأسبوع',
            'dashboard.total_clients': 'إجمالي العملاء',
            'dashboard.active_clients': 'العملاء النشطون',
            'dashboard.recent_checkins': 'تسجيلات الحضور الأخيرة',
            'dashboard.pending_missions': 'المهام المعلقة',
            
            // Client Management
            'client.serial': 'معرف العميل',
            'client.start_date': 'تاريخ البدء',
            'client.status': 'الحالة',
            'client.active': 'نشط',
            'client.inactive': 'غير نشط',
            'client.last_checkin': 'آخر تسجيل حضور',
            'client.completion_rate': 'معدل الإنجاز',
            'client.tracking': 'التتبع',
            'client.actions': 'الإجراءات',
            'client.view': 'عرض',
            'client.add_goal': 'إضافة هدف',
            'client.add_note': 'إضافة ملاحظة',
            
            // Check-in
            'checkin.title': 'تسجيل الحضور اليومي',
            'checkin.date': 'التاريخ',
            'checkin.emotional': 'كيف حالتك العاطفية؟',
            'checkin.medication': 'هل تناولت أدويتك كما هو موصوف؟',
            'checkin.activity': 'ما مدى نشاطك؟',
            'checkin.notes': 'ملاحظات إضافية (اختياري)',
            'checkin.scale_1': 'سيء جداً',
            'checkin.scale_2': 'سيء',
            'checkin.scale_3': 'متوسط',
            'checkin.scale_4': 'جيد',
            'checkin.scale_5': 'ممتاز',
            'checkin.med_yes': 'نعم',
            'checkin.med_no': 'لا',
            'checkin.med_partial': 'جزئي',
            'checkin.med_na': 'غير منطبق',
            
            // Goals
            'goals.weekly': 'الأهداف الأسبوعية',
            'goals.add': 'إضافة هدف جديد',
            'goals.completed': 'مكتمل',
            'goals.pending': 'معلق',
            'goals.text': 'وصف الهدف',
            
            // Reports
            'reports.generate': 'إنشاء تقرير',
            'reports.weekly': 'التقرير الأسبوعي',
            'reports.select_client': 'اختر العميل',
            'reports.select_week': 'اختر الأسبوع',
            'reports.excel': 'تحميل Excel',
            'reports.email': 'إرسال التقرير بالبريد',
            
            // Messages
            'msg.success': 'نجح!',
            'msg.error': 'خطأ',
            'msg.loading': 'جار التحميل...',
            'msg.saved': 'تم حفظ التغييرات بنجاح',
            'msg.deleted': 'تم الحذف بنجاح',
            'msg.confirm_delete': 'هل أنت متأكد أنك تريد الحذف؟',
            'msg.no_data': 'لا توجد بيانات متاحة',
            'msg.never': 'أبداً',
            
            // Days of week
            'day.monday': 'الإثنين',
            'day.tuesday': 'الثلاثاء',
            'day.wednesday': 'الأربعاء',
            'day.thursday': 'الخميس',
            'day.friday': 'الجمعة',
            'day.saturday': 'السبت',
            'day.sunday': 'الأحد',
            'day.mon': 'إث',
            'day.tue': 'ثل',
            'day.wed': 'أر',
            'day.thu': 'خم',
            'day.fri': 'جم',
            'day.sat': 'سب',
            'day.sun': 'أح',
            
            // Months
            'month.january': 'يناير',
            'month.february': 'فبراير',
            'month.march': 'مارس',
            'month.april': 'أبريل',
            'month.may': 'مايو',
            'month.june': 'يونيو',
            'month.july': 'يوليو',
            'month.august': 'أغسطس',
            'month.september': 'سبتمبر',
            'month.october': 'أكتوبر',
            'month.november': 'نوفمبر',
            'month.december': 'ديسمبر',
            
            // Additional translations
            'therapist.to': 'إلى',
            'therapist.subject': 'الموضوع',
            'therapist.email_preview': 'معاينة تقرير البريد الإلكتروني',
            'therapist.copy_email_note': 'انسخ هذا المحتوى لإرساله عبر بريدك الإلكتروني',
            'therapist.save_credentials': 'يرجى حفظ بيانات الاعتماد هذه للعميل. ستظل هذه الرسالة مرئية حتى تغادر هذه اللسان.',
            'therapist.started': 'بدأ',
            'therapist.client_info': 'معلومات العميل',
            'therapist.week_progress': 'تقدم هذا الأسبوع',
            'therapist.active_goals': 'الأهداف النشطة',
            'therapist.no_active_goals': 'لا توجد أهداف نشطة لهذا الأسبوع',
            'therapist.add_note_mission': 'إضافة ملاحظة أو مهمة',
            'therapist.enter_note_placeholder': 'أدخل ملاحظتك أو مهمتك...',
            'therapist.recent_notes': 'الملاحظات والمهام الأخيرة',
            'therapist.mission': 'مهمة',
            'therapist.no_notes': 'لا توجد ملاحظات بعد'
        }
    },
    
    // Initialize i18n
    init() {
        // Set initial language from localStorage or browser
        const savedLang = localStorage.getItem('userLanguage');
        const browserLang = navigator.language.split('-')[0];
        
        if (savedLang && this.translations[savedLang]) {
            this.currentLang = savedLang;
        } else if (this.translations[browserLang]) {
            this.currentLang = browserLang;
        }
        
        // Apply RTL if needed
        this.applyRTL();
        
        // Initialize language switcher if it exists
        this.initLanguageSwitcher();
        
        // Translate page
        this.translatePage();
    },
    
    // Get translation
    t(key, replacements = {}) {
    const translation = this.translations[this.currentLang]?.[key] || 
                      this.translations.en[key] || 
                      key;
    
    // Replace placeholders like {name} with values
    let result = translation;
    for (const [placeholder, value] of Object.entries(replacements)) {
        // FIX: Escape special regex characters
        const escapedPlaceholder = placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        result = result.replace(new RegExp(`{${escapedPlaceholder}}`, 'g'), value);
    }
    
    return result;
},
    
    // Change language
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('userLanguage', lang);
            this.applyRTL();
            this.translatePage();
            
            // Update language switcher
            const switcher = document.getElementById('languageSwitcher');
            if (switcher) {
                switcher.value = lang;
            }
        }
    },
    
    // Apply RTL
    applyRTL() {
        const isRTL = this.rtlLanguages.includes(this.currentLang);
        document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
        document.documentElement.lang = this.currentLang;
        
        // Add RTL class for additional styling
        document.body.classList.toggle('rtl', isRTL);
    },
    
    // Translate entire page
    translatePage() {
        // Translate elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
        
        // Translate elements with data-i18n-html (for HTML content)
        document.querySelectorAll('[data-i18n-html]').forEach(element => {
            const key = element.getAttribute('data-i18n-html');
            element.innerHTML = this.t(key);
        });
        
        // Update page title
        const titleElement = document.querySelector('title');
        if (titleElement) {
            const baseTitle = titleElement.textContent.split(' - ')[1] || '';
            titleElement.textContent = this.t('app.title') + (baseTitle ? ' - ' + baseTitle : '');
        }
    },
    
    // Initialize language switcher
    initLanguageSwitcher() {
        // Check if switcher already exists
        if (document.getElementById('languageSwitcher')) {
            return;
        }
        
        // Create language switcher
        const switcher = document.createElement('select');
        switcher.id = 'languageSwitcher';
        switcher.className = 'language-switcher';
        
        // Add options
        const languages = [
            { code: 'en', name: 'English', flag: '🇬🇧' },
            { code: 'he', name: 'עברית', flag: '🇮🇱' },
            { code: 'ru', name: 'Русский', flag: '🇷🇺' },
            { code: 'ar', name: 'العربية', flag: '🇸🇦' }
        ];
        
        languages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = `${lang.flag} ${lang.name}`;
            if (lang.code === this.currentLang) {
                option.selected = true;
            }
            switcher.appendChild(option);
        });
        
        // Add change event
        switcher.addEventListener('change', (e) => {
            this.setLanguage(e.target.value);
        });
        
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .language-switcher {
                position: fixed;
                top: 1rem;
                ${this.rtlLanguages.includes(this.currentLang) ? 'left' : 'right'}: 1rem;
                z-index: 9999;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                background: white;
                font-size: 0.875rem;
                cursor: pointer;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .rtl .language-switcher {
                left: 1rem;
                right: auto;
            }
            
            /* Adjust header for language switcher */
            .header-content {
                padding-right: 150px;
            }
            
            .rtl .header-content {
                padding-right: 0;
                padding-left: 150px;
            }
            
            /* RTL specific styles */
            .rtl {
                text-align: right;
            }
            
            .rtl .stats-grid,
            .rtl .progress-grid,
            .rtl .week-view {
                direction: ltr;
            }
            
            .rtl .action-buttons,
            .rtl .search-bar {
                flex-direction: row-reverse;
            }
            
            .rtl .stat-card,
            .rtl .progress-card {
                text-align: right;
            }
            
            .rtl .modal-header {
                flex-direction: row-reverse;
            }
            
            .rtl table {
                direction: rtl;
            }
            
            .rtl th,
            .rtl td {
                text-align: right;
            }
        `;
        document.head.appendChild(style);
        
        // Add to page
        document.body.appendChild(switcher);
    },
    
    // Helper to format dates according to locale
    formatDate(date, format = 'short') {
        const d = new Date(date);
        const options = format === 'short' 
            ? { year: 'numeric', month: '2-digit', day: '2-digit' }
            : { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            
        return d.toLocaleDateString(this.currentLang, options);
    },
    
    // Get day name
    getDayName(dayIndex, short = false) {
        const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
        const key = short ? `day.${days[dayIndex].substr(0, 3)}` : `day.${days[dayIndex]}`;
        return this.t(key);
    },
    
    // Get month name
    getMonthName(monthIndex) {
        const months = ['january', 'february', 'march', 'april', 'may', 'june',
                       'july', 'august', 'september', 'october', 'november', 'december'];
        return this.t(`month.${months[monthIndex]}`);
    }
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => i18n.init());
} else {
    i18n.init();
}

// Export for use in other scripts
window.i18n = i18n;
