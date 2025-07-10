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
        'nav.settings': 'Settings',

        // Login Page
        'login.title': 'Login to Your Account',
        'login.email': 'Email',
        'login.password': 'Password',
        'login.forgot_password': 'Forgot your password?',
        'login.remember_me': 'Remember me',
        'login.no_account': "Don't have an account?",
        'login.error': 'Invalid email or password',
        'login.welcome_back': 'Welcome back!',
        'login.instruction': 'Therapists and clients can login here with their credentials.',
        'login.forgot_coming_soon': 'Password reset functionality coming soon!',

        // Password Reset
        'reset.title': 'Reset Password',
        'reset.instruction': 'Enter your email address and we will send you a password reset link.',
        'reset.email_label': 'Email Address',
        'reset.send_link': 'Send Reset Link',
        'reset.back_to_login': 'Back to Login',
        'reset.success': 'Password reset link sent! Check your email.',
        'reset.error': 'Error sending reset link. Please try again.',
        'reset.invalid_email': 'Please enter a valid email address',
        'reset.email_not_found': 'Email address not found',
        'reset.new_password': 'New Password',
        'reset.confirm_password': 'Confirm New Password',
        'reset.update_password': 'Update Password',
        'reset.password_updated': 'Password updated successfully!',
        'reset.invalid_token': 'Invalid or expired reset token',

        // Registration
        'register.title': 'Create Account',
        'register.therapist': 'Therapist Registration',
        'register.full_name': 'Full Name',
        'register.license': 'License Number',
        'register.organization': 'Organization',
        'register.confirm_password': 'Confirm Password',
        'register.terms': 'I agree to the Terms of Service',
        'register.therapist_desc': 'Create your professional account to start managing clients.',
        'register.client_note_title': 'Note for Clients:',
        'register.client_note_desc': 'Client accounts must be created by your therapist. If you\'re a client, please use the Login tab with credentials provided by your therapist.',
        'register.license_note': 'Must be unique - each license can only be registered once',
        'register.create_account': 'Create Therapist Account',
        'register.passwords_mismatch': 'Passwords do not match',
        'register.password_length': 'Password must be at least 8 characters long',
        'register.license_exists': 'This license number is already registered. Please use a different one.',
        'register.email_exists': 'This email is already registered. Please use the login tab.',

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
        'reports.week': 'Week',
        'reports.daily_checkins': 'Daily Check-ins',
        'reports.checkin_time': 'Check-in Time',
        'reports.no_checkin': 'No check-in',
        'reports.weekly_summary': 'Weekly Summary',
        'reports.checkin_completion': 'Check-in Completion',
        'reports.completion_rate': 'Completion Rate',
        'reports.completed': 'Completed',
        'reports.weekly_goals': 'Weekly Goals',
        'reports.weekly_report_title': 'Weekly Therapy Report',

        // Messages
        'msg.success': 'Success!',
        'msg.error': 'Error',
        'msg.loading': 'Loading...',
        'msg.saved': 'Changes saved successfully',
        'msg.deleted': 'Deleted successfully',
        'msg.confirm_delete': 'Are you sure you want to delete this?',
        'msg.no_data': 'No data available',
        'msg.never': 'Never',
        'msg.login_success': 'Login successful! Redirecting...',
        'msg.registration_success': 'Registration successful! Logging you in...',
        'msg.network_error': 'Network error. Please try again.',

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

        // Tracking Categories
        'category.emotion_level': 'Emotion Level',
        'category.emotion_level_desc': 'Overall emotional state',
        'category.energy': 'Energy',
        'category.energy_desc': 'Physical and mental energy levels',
        'category.social_activity': 'Social Activity',
        'category.social_activity_desc': 'Engagement in social interactions',
        'category.sleep_quality': 'Sleep Quality',
        'category.sleep_quality_desc': 'Quality of sleep',
        'category.anxiety_level': 'Anxiety Level',
        'category.anxiety_level_desc': 'Level of anxiety experienced',
        'category.motivation': 'Motivation',
        'category.motivation_desc': 'Level of motivation and drive',
        'category.medication': 'Medication',
        'category.medication_desc': 'Medication adherence',
        'category.physical_activity': 'Physical Activity',
        'category.physical_activity_desc': 'Physical activity level',

        

        // Client specific
        'client.dashboard_title': 'My Therapy Journey',
        'client.encouragement': 'Your journey to wellness continues. Every step counts!',
        'client.morning_message': 'Start your day with a positive mindset!',
        'client.afternoon_message': 'Keep up the great work today!',
        'client.evening_message': 'Time to reflect on your day and rest well.',
        'client.previous_week': '← Previous Week',
        'client.next_week': 'Next Week →',
        'client.quick_stats': 'Quick Stats',
        'client.week_goals': 'This Week\'s Goals',
        'client.select_date': 'Select Date:',
        'client.checkin_intro': 'Take a moment to reflect on your day. Your responses help track your progress.',
        'client.notes_placeholder': 'Notes for {category} (optional)',
        'client.submit_checkin': 'Submit Check-in',
        'client.clear_form': 'Clear',
        'client.select_week': 'Select Week:',
        'client.load_goals': 'Load Goals',
        'client.select_week_goals': 'Select a week to view goals',
        'client.your_progress': 'Your Progress',
        'client.view_progress': 'View Progress:',
        'client.last_7_days': 'Last 7 days',
        'client.last_30_days': 'Last 30 days',
        'client.last_90_days': 'Last 90 days',
        'client.update': 'Update',
        'client.loading_progress': 'Loading progress data...',
        'client.report_desc': 'Generate a comprehensive report of your check-ins for any week.',
        'client.generate_excel': 'Generate Excel Report',
        'client.prepare_email': 'Prepare Email Report',
        'client.report_status': 'Report Status',
        'client.no_checkin': 'No check-in',
        'client.today_marker': '(Today)',
        'client.past_date': '(Past date)',
        'client.future_date': '(Future date)',
        'client.complete_ratings': 'Please complete all required ratings',
        'client.no_goals_week': 'No goals set for this week',
        'client.total_checkins': 'Total check-ins:',
        'client.avg_emotional': 'Average emotional rating:',
        'client.medication_adherence': 'Medication adherence:',
        'client.avg_activity': 'Average activity level:',
        'client.email_preview': 'Email Report Preview',
        'client.copy_email': 'Copy this email content to send to your therapist',
        'client.checkin_success': 'Check-in submitted successfully! 🎉',
        'client.checkin_error': 'Cannot submit check-in for future dates',
        'client.select_client_week': 'Please select a week',
        'client.report_generated': 'Report generated and downloaded successfully!',
        'client.error_progress': 'Error loading progress data',
        'client.account_settings': 'Account Settings',
        'client.change_password': 'Change Password',
        'client.password_requirements': 'Password must be at least 8 characters long.',
        'client.current_password': 'Current Password',
        'client.new_password': 'New Password',
        'client.confirm_new_password': 'Confirm New Password',
        'client.update_password': 'Update Password',
        'client.password_changed': 'Password changed successfully!',
        'client.passwords_dont_match': 'New passwords do not match',
        'client.password_too_short': 'Password must be at least 8 characters long',
        'client.incorrect_password': 'Current password is incorrect',
        'client.error_changing_password': 'Error changing password:',

        // Therapist specific
        'therapist.dashboard_title': 'Therapist Dashboard',
        'therapist.dashboard_overview': 'Dashboard Overview',
        'therapist.checkins_week': 'Check-ins This Week',
        'therapist.recent_activity': 'Recent Activity',
        'therapist.loading_activity': 'Loading recent activity...',
        'therapist.client_management': 'Client Management',
        'therapist.search_placeholder': 'Search by serial or date...',
        'therapist.all_clients': 'All Clients',
        'therapist.active_only': 'Active Only',
        'therapist.inactive_only': 'Inactive Only',
        'therapist.add_new_client': 'Add New Client',
        'therapist.week_completion': 'Week Completion',
        'therapist.loading_clients': 'Loading clients...',
        'therapist.client_account_info': 'Client Account Information',
        'therapist.email_required': 'Email Address*',
        'therapist.temp_password': 'Temporary Password (optional)',
        'therapist.auto_generate_note': 'Leave blank to auto-generate',
        'therapist.tracking_categories': 'Tracking Categories',
        'therapist.select_categories': 'Select which categories this client should track:',
        'therapist.all_categories_note': 'Note: All categories are selected by default. Uncheck any you don\'t want the client to track.',
        'therapist.initial_goals': 'Initial Goals (Optional)',
        'therapist.setup_goals': 'Set up to 5 initial weekly goals for the client:',
        'therapist.goal_placeholder': 'Goal 1 (e.g., Take a 15-minute walk daily)',
        'therapist.add_another_goal': '+ Add Another Goal',
        'therapist.create_client_btn': 'Create Client Account',
        'therapist.client_reports': 'Client Reports',
        'therapist.generate_weekly_report': 'Generate Weekly Report',
        'therapist.select_client_option': 'Select a client...',
        'therapist.generate_excel': 'Generate Excel Report',
        'therapist.prepare_email': 'Prepare Email Report',
        'therapist.report_status': 'Report Status',
        'therapist.client_details': 'Client Details',
        'therapist.no_clients': 'No clients found. Add your first client to get started.',
        'therapist.license': 'License',
        'therapist.activity_coming_soon': 'Recent activity feature coming soon',
        'therapist.check_clients_tab': 'Check the Clients tab to view individual client progress',
        'therapist.max_goals': 'Maximum 5 goals can be added initially',
        'therapist.please_enter_email': 'Please enter client email',
        'therapist.client_created': 'Client created successfully!',
        'therapist.serial': 'Serial',
        'therapist.email': 'Email',
        'therapist.temp_password_label': 'Temporary password',
        'therapist.save_credentials': 'Please save these credentials for the client. This message will remain visible until you leave this tab.',
        'therapist.goal_added': 'Goal added successfully!',
        'therapist.enter_goal': 'Enter the goal for this week:',
        'therapist.note_added': 'Note added successfully!',
        'therapist.please_enter_note': 'Please enter a note',
        'therapist.mark_as_mission': 'Mark as mission',
        'therapist.this_week_progress': 'This Week\'s Progress',
        'therapist.select_both': 'Please select both client and week',
        'therapist.generating_report': 'Generating report...',
        'therapist.report_downloaded': 'Report downloaded successfully!',
        'therapist.preparing_email': 'Preparing email report...',
        'therapist.email_prepared': 'Email report prepared! Review the preview below.',
        'therapist.error_loading': 'Error loading dashboard:',
        'therapist.error_creating': 'Error creating client:',
        'therapist.error_adding_goal': 'Error adding goal:',
        'therapist.error_adding_note': 'Error adding note:',
        'therapist.error_loading_details': 'Error loading client details:',
        'therapist.error_generating': 'Error generating report:',
        'therapist.error_preparing': 'Error preparing email report:',
        'therapist.to': 'To',
        'therapist.subject': 'Subject',
        'therapist.email_preview': 'Email Report Preview',
        'therapist.copy_email_note': 'Copy this content to send via your email client',
        'therapist.started': 'Started',
        'therapist.client_info': 'Client Information',
        'therapist.week_progress': 'This Week\'s Progress',
        'therapist.active_goals': 'Active Goals',
        'therapist.no_active_goals': 'No active goals for this week',
        'therapist.add_note_mission': 'Add Note or Mission',
        'therapist.enter_note_placeholder': 'Enter your note or mission...',
        'therapist.recent_notes': 'Recent Notes & Missions',
        'therapist.mission': 'MISSION',
        'therapist.no_notes': 'No notes yet',
        
         // English
        'email.dear_therapist': 'Dear Therapist',
        'email.weekly_report_intro': 'Here is my weekly progress report for',
        'email.report_generated_on': 'Report generated on',
        'email.best_regards': 'Best regards',


       

        
        

        // Index page
        'hero.subtitle': 'A comprehensive therapy companion system for therapists and clients',
        'hero.get_started': 'Get Started',
        'hero.learn_more': 'Learn More',
        'features.title': 'Features for Everyone',
        'features.therapists.title': 'For Therapists',
        'features.therapists.desc': 'Manage multiple clients, track progress, set goals, and generate comprehensive reports—all in one secure platform.',
        'features.clients.title': 'For Clients',
        'features.clients.desc': 'Daily check-ins, mood tracking, goal completion, and gentle reminders to support your mental health journey.',
        'features.tracking.title': 'Progress Tracking',
        'features.tracking.desc': 'Visual insights into emotional patterns, medication adherence, and physical activity over time.',
        'features.security.title': 'Secure & Private',
        'features.security.desc': 'Your data is protected with industry-standard encryption and strict privacy controls.',
        'features.accessible.title': 'Accessible Anywhere',
        'features.accessible.desc': 'Use on any device—desktop, tablet, or mobile—to stay connected with your wellness journey.',
        'features.goals.title': 'Goal Setting',
        'features.goals.desc': 'Weekly goals and missions to help maintain focus and celebrate achievements.',
        'how.title': 'How It Works',
        'how.step1.title': 'Sign Up',
        'how.step1.desc': 'Therapists register with their license. Clients join using their therapist\'s code.',
        'how.step2.title': 'Set Up Profile',
        'how.step2.desc': 'Choose tracking categories and set initial goals for the wellness journey.',
        'how.step3.title': 'Daily Check-ins',
        'how.step3.desc': 'Clients complete brief daily assessments to track their progress.',
        'how.step4.title': 'Monitor & Support',
        'how.step4.desc': 'Therapists review progress, add notes, and adjust treatment plans as needed.',
        'footer.copyright': '© 2024 Therapeutic Companion. Supporting wellness journeys with care and technology.'
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
        'nav.settings': 'הגדרות',

        // Login Page
        'login.title': 'התחברות לחשבון',
        'login.email': 'דוא״ל',
        'login.password': 'סיסמה',
        'login.forgot_password': 'שכחת סיסמה?',
        'login.remember_me': 'זכור אותי',
        'login.no_account': 'אין לך חשבון?',
        'login.error': 'דוא״ל או סיסמה שגויים',
        'login.welcome_back': 'ברוך הבא!',
        'login.instruction': 'מטפלים ומטופלים יכולים להתחבר כאן עם האישורים שלהם.',
        'login.forgot_coming_soon': 'פונקציית איפוס סיסמה תגיע בקרוב!',

        'email.dear_therapist': 'מטפל יקר',
        'email.weekly_report_intro': 'הנה דוח ההתקדמות השבועי שלי עבור',
        'email.report_generated_on': 'הדוח נוצר בתאריך',
        'email.best_regards': 'בברכה',

        // Password Reset
        'reset.title': 'איפוס סיסמה',
        'reset.instruction': 'הזן את כתובת הדוא״ל שלך ונשלח לך קישור לאיפוס הסיסמה.',
        'reset.email_label': 'כתובת דוא״ל',
        'reset.send_link': 'שלח קישור איפוס',
        'reset.back_to_login': 'חזרה להתחברות',
        'reset.success': 'קישור איפוס נשלח! בדוק את הדוא״ל שלך.',
        'reset.error': 'שגיאה בשליחת קישור איפוס. אנא נסה שוב.',
        'reset.invalid_email': 'אנא הזן כתובת דוא״ל תקינה',
        'reset.email_not_found': 'כתובת דוא״ל לא נמצאה',
        'reset.new_password': 'סיסמה חדשה',
        'reset.confirm_password': 'אשר סיסמה חדשה',
        'reset.update_password': 'עדכן סיסמה',
        'reset.password_updated': 'הסיסמה עודכנה בהצלחה!',
        'reset.invalid_token': 'קישור איפוס לא תקין או שפג תוקפו',

        // Registration
        'register.title': 'יצירת חשבון',
        'register.therapist': 'רישום מטפל',
        'register.full_name': 'שם מלא',
        'register.license': 'מספר רישיון',
        'register.organization': 'ארגון',
        'register.confirm_password': 'אימות סיסמה',
        'register.terms': 'אני מסכים לתנאי השירות',
        'register.therapist_desc': 'צור את החשבון המקצועי שלך כדי להתחיל לנהל מטופלים.',
        'register.client_note_title': 'הערה למטופלים:',
        'register.client_note_desc': 'חשבונות מטופלים חייבים להיווצר על ידי המטפל שלך. אם אתה מטופל, אנא השתמש בלשונית ההתחברות עם האישורים שסופקו על ידי המטפל שלך.',
        'register.license_note': 'חייב להיות ייחודי - כל רישיון יכול להירשם פעם אחת בלבד',
        'register.create_account': 'צור חשבון מטפל',
        'register.passwords_mismatch': 'הסיסמאות אינן תואמות',
        'register.password_length': 'הסיסמה חייבת להיות באורך של לפחות 8 תווים',
        'register.license_exists': 'מספר רישיון זה כבר רשום. אנא השתמש במספר אחר.',
        'register.email_exists': 'כתובת דוא״ל זו כבר רשומה. אנא השתמש בלשונית ההתחברות.',

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
        'reports.week': 'שבוע',
        'reports.daily_checkins': 'צ׳ק-אין יומי',
        'reports.checkin_time': 'זמן צ׳ק-אין',
        'reports.no_checkin': 'אין צ׳ק-אין',
        'reports.weekly_summary': 'סיכום שבועי',
        'reports.checkin_completion': 'השלמת צ׳ק-אין',
        'reports.completion_rate': 'אחוז השלמה',
        'reports.completed': 'הושלם',
        'reports.weekly_goals': 'יעדים שבועיים',
        'reports.weekly_report_title': 'דוח טיפולי שבועי',

        // Messages
        'msg.success': 'הצלחה!',
        'msg.error': 'שגיאה',
        'msg.loading': 'טוען...',
        'msg.saved': 'השינויים נשמרו בהצלחה',
        'msg.deleted': 'נמחק בהצלחה',
        'msg.confirm_delete': 'האם אתה בטוח שברצונך למחוק?',
        'msg.no_data': 'אין נתונים זמינים',
        'msg.never': 'אף פעם',
        'msg.login_success': 'התחברות הצליחה! מעביר...',
        'msg.registration_success': 'ההרשמה הצליחה! מחבר אותך...',
        'msg.network_error': 'שגיאת רשת. אנא נסה שוב.',

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

        // Tracking Categories
        'category.emotion_level': 'רמה רגשית',
        'category.emotion_level_desc': 'מצב רגשי כללי',
        'category.energy': 'אנרגיה',
        'category.energy_desc': 'רמות אנרגיה פיזית ונפשית',
        'category.social_activity': 'פעילות חברתית',
        'category.social_activity_desc': 'מעורבות באינטראקציות חברתיות',
        'category.sleep_quality': 'איכות שינה',
        'category.sleep_quality_desc': 'איכות השינה',
        'category.anxiety_level': 'רמת חרדה',
        'category.anxiety_level_desc': 'רמת החרדה שחווית',
        'category.motivation': 'מוטיבציה',
        'category.motivation_desc': 'רמת מוטיבציה ודחף',
        'category.medication': 'תרופות',
        'category.medication_desc': 'היענות לתרופות',
        'category.physical_activity': 'פעילות גופנית',
        'category.physical_activity_desc': 'רמת פעילות גופנית',

        // Client specific
        'client.dashboard_title': 'המסע הטיפולי שלי',
        'client.encouragement': 'המסע שלך לבריאות ממשיך. כל צעד נחשב!',
        'client.morning_message': 'התחל את היום עם גישה חיובית!',
        'client.afternoon_message': 'המשך בעבודה הטובה היום!',
        'client.evening_message': 'זמן לחשוב על היום שלך ולנוח היטב.',
        'client.previous_week': '→ שבוע קודם',
        'client.next_week': 'שבוע הבא ←',
        'client.quick_stats': 'סטטיסטיקות מהירות',
        'client.week_goals': 'היעדים השבועיים',
        'client.select_date': 'בחר תאריך:',
        'client.checkin_intro': 'קח רגע לחשוב על היום שלך. התשובות שלך עוזרות לעקוב אחר ההתקדמות.',
        'client.notes_placeholder': 'הערות עבור {category} (אופציונלי)',
        'client.submit_checkin': 'שלח צ׳ק-אין',
        'client.clear_form': 'נקה',
        'client.select_week': 'בחר שבוע:',
        'client.load_goals': 'טען יעדים',
        'client.select_week_goals': 'בחר שבוע כדי לראות יעדים',
        'client.your_progress': 'ההתקדמות שלך',
        'client.view_progress': 'צפה בהתקדמות:',
        'client.last_7_days': '7 ימים אחרונים',
        'client.last_30_days': '30 ימים אחרונים',
        'client.last_90_days': '90 ימים אחרונים',
        'client.update': 'עדכן',
        'client.loading_progress': 'טוען נתוני התקדמות...',
        'client.report_desc': 'צור דוח מקיף של הצ׳ק-אינים שלך לכל שבוע.',
        'client.generate_excel': 'צור דוח אקסל',
        'client.prepare_email': 'הכן דוח דוא״ל',
        'client.report_status': 'סטטוס דוח',
        'client.no_checkin': 'אין צ׳ק-אין',
        'client.today_marker': '(היום)',
        'client.past_date': '(תאריך עבר)',
        'client.future_date': '(תאריך עתידי)',
        'client.complete_ratings': 'אנא השלם את כל הדירוגים הנדרשים',
        'client.no_goals_week': 'אין יעדים שהוגדרו לשבוע זה',
        'client.total_checkins': 'סך כל הצ׳ק-אינים:',
        'client.avg_emotional': 'דירוג רגשי ממוצע:',
        'client.medication_adherence': 'היענות לתרופות:',
        'client.avg_activity': 'רמת פעילות ממוצעת:',
        'client.email_preview': 'תצוגה מקדימה של דוח דוא״ל',
        'client.copy_email': 'העתק תוכן זה כדי לשלוח למטפל שלך',
        'client.checkin_success': 'הצ׳ק-אין נשלח בהצלחה! 🎉',
        'client.checkin_error': 'לא ניתן לשלוח צ׳ק-אין לתאריכים עתידיים',
        'client.select_client_week': 'אנא בחר שבוע',
        'client.report_generated': 'הדוח נוצר והורד בהצלחה!',
        'client.error_progress': 'שגיאה בטעינת נתוני התקדמות',
        'client.account_settings': 'הגדרות חשבון',
        'client.change_password': 'שינוי סיסמה',
        'client.password_requirements': 'הסיסמה חייבת להיות באורך של לפחות 8 תווים.',
        'client.current_password': 'סיסמה נוכחית',
        'client.new_password': 'סיסמה חדשה',
        'client.confirm_new_password': 'אשר סיסמה חדשה',
        'client.update_password': 'עדכן סיסמה',
        'client.password_changed': 'הסיסמה שונתה בהצלחה!',
        'client.passwords_dont_match': 'הסיסמאות החדשות אינן תואמות',
        'client.password_too_short': 'הסיסמה חייבת להיות באורך של לפחות 8 תווים',
        'client.incorrect_password': 'הסיסמה הנוכחית שגויה',
        'client.error_changing_password': 'שגיאה בשינוי הסיסמה:',

        // Therapist specific
        'therapist.dashboard_title': 'לוח בקרה למטפל',
        'therapist.dashboard_overview': 'סקירת לוח בקרה',
        'therapist.checkins_week': 'צ׳ק-אינים השבוע',
        'therapist.recent_activity': 'פעילות אחרונה',
        'therapist.loading_activity': 'טוען פעילות אחרונה...',
        'therapist.client_management': 'ניהול מטופלים',
        'therapist.search_placeholder': 'חיפוש לפי מספר סידורי או תאריך...',
        'therapist.all_clients': 'כל המטופלים',
        'therapist.active_only': 'פעילים בלבד',
        'therapist.inactive_only': 'לא פעילים בלבד',
        'therapist.add_new_client': 'הוסף מטופל חדש',
        'therapist.week_completion': 'השלמת שבוע',
        'therapist.loading_clients': 'טוען מטופלים...',
        'therapist.client_account_info': 'פרטי חשבון מטופל',
        'therapist.email_required': 'כתובת דוא״ל*',
        'therapist.temp_password': 'סיסמה זמנית (אופציונלי)',
        'therapist.auto_generate_note': 'השאר ריק ליצירה אוטומטית',
        'therapist.tracking_categories': 'קטגוריות מעקב',
        'therapist.select_categories': 'בחר אילו קטגוריות המטופל יעקוב אחריהן:',
        'therapist.all_categories_note': 'הערה: כל הקטגוריות נבחרות כברירת מחדל. בטל סימון לכל קטגוריה שאינך רוצה שהמטופל יעקוב אחריה.',
        'therapist.initial_goals': 'יעדים ראשוניים (אופציונלי)',
        'therapist.setup_goals': 'הגדר עד 5 יעדים שבועיים ראשוניים למטופל:',
        'therapist.goal_placeholder': 'יעד 1 (למשל, הליכה של 15 דקות ביום)',
        'therapist.add_another_goal': '+ הוסף יעד נוסף',
        'therapist.create_client_btn': 'צור חשבון מטופל',
        'therapist.client_reports': 'דוחות מטופלים',
        'therapist.generate_weekly_report': 'צור דוח שבועי',
        'therapist.select_client_option': 'בחר מטופל...',
        'therapist.generate_excel': 'צור דוח אקסל',
        'therapist.prepare_email': 'הכן דוח דוא״ל',
        'therapist.report_status': 'סטטוס דוח',
        'therapist.client_details': 'פרטי מטופל',
        'therapist.no_clients': 'לא נמצאו מטופלים. הוסף את המטופל הראשון שלך כדי להתחיל.',
        'therapist.license': 'רישיון',
        'therapist.activity_coming_soon': 'תכונת פעילות אחרונה תגיע בקרוב',
        'therapist.check_clients_tab': 'בדוק את לשונית המטופלים כדי לראות התקדמות אישית',
        'therapist.max_goals': 'ניתן להוסיף מקסימום 5 יעדים בהתחלה',
        'therapist.please_enter_email': 'אנא הזן דוא״ל של המטופל',
        'therapist.client_created': 'המטופל נוצר בהצלחה!',
        'therapist.serial': 'מספר סידורי',
        'therapist.email': 'דוא״ל',
        'therapist.temp_password_label': 'סיסמה זמנית',
        'therapist.save_credentials': 'אנא שמור את האישורים האלה עבור המטופל. הודעה זו תישאר גלויה עד שתעזוב את הלשונית הזו.',
        'therapist.goal_added': 'היעד נוסף בהצלחה!',
        'therapist.enter_goal': 'הזן את היעד לשבוע זה:',
        'therapist.note_added': 'ההערה נוספה בהצלחה!',
        'therapist.please_enter_note': 'אנא הזן הערה',
        'therapist.mark_as_mission': 'סמן כמשימה',
        'therapist.this_week_progress': 'התקדמות השבוע',
        'therapist.select_both': 'אנא בחר גם מטופל וגם שבוע',
        'therapist.generating_report': 'מייצר דוח...',
        'therapist.report_downloaded': 'הדוח הורד בהצלחה!',
        'therapist.preparing_email': 'מכין דוח דוא״ל...',
        'therapist.email_prepared': 'דוח הדוא״ל הוכן! עיין בתצוגה המקדימה למטה.',
        'therapist.error_loading': 'שגיאה בטעינת לוח הבקרה:',
        'therapist.error_creating': 'שגיאה ביצירת מטופל:',
        'therapist.error_adding_goal': 'שגיאה בהוספת יעד:',
        'therapist.error_adding_note': 'שגיאה בהוספת הערה:',
        'therapist.error_loading_details': 'שגיאה בטעינת פרטי מטופל:',
        'therapist.error_generating': 'שגיאה ביצירת דוח:',
        'therapist.error_preparing': 'שגיאה בהכנת דוח דוא״ל:',
        'therapist.to': 'אל',
        'therapist.subject': 'נושא',
        'therapist.email_preview': 'תצוגה מקדימה של דוח דוא״ל',
        'therapist.copy_email_note': 'העתק תוכן זה כדי לשלוח דרך הדוא״ל שלך',
        'therapist.started': 'התחיל',
        'therapist.client_info': 'פרטי מטופל',
        'therapist.week_progress': 'התקדמות השבוע',
        'therapist.active_goals': 'יעדים פעילים',
        'therapist.no_active_goals': 'אין יעדים פעילים לשבוע זה',
        'therapist.add_note_mission': 'הוספת הערה או משימה',
        'therapist.enter_note_placeholder': 'הזן את ההערה או המשימה שלך...',
        'therapist.recent_notes': 'הערות ומשימות אחרונות',
        'therapist.mission': 'משימה',
        'therapist.no_notes': 'אין הערות עדיין',

        // Index page
        'hero.subtitle': 'מערכת ליווי טיפולית מקיפה למטפלים ומטופלים',
        'hero.get_started': 'התחל עכשיו',
        'hero.learn_more': 'למידע נוסף',
        'features.title': 'תכונות לכולם',
        'features.therapists.title': 'למטפלים',
        'features.therapists.desc': 'ניהול מטופלים מרובים, מעקב התקדמות, הגדרת יעדים ויצירת דוחות מקיפים - הכל בפלטפורמה מאובטחת אחת.',
        'features.clients.title': 'למטופלים',
        'features.clients.desc': 'צ׳ק-אין יומי, מעקב מצב רוח, השלמת יעדים ותזכורות עדינות לתמיכה במסע הבריאות הנפשית שלך.',
        'features.tracking.title': 'מעקב התקדמות',
        'features.tracking.desc': 'תובנות חזותיות על דפוסים רגשיים, היענות לתרופות ופעילות גופנית לאורך זמן.',
        'features.security.title': 'מאובטח ופרטי',
        'features.security.desc': 'הנתונים שלך מוגנים בהצפנה ברמת התעשייה ובקרות פרטיות קפדניות.',
        'features.accessible.title': 'נגיש מכל מקום',
        'features.accessible.desc': 'השתמש בכל מכשיר - מחשב, טאבלט או נייד - כדי להישאר מחובר למסע הבריאות שלך.',
        'features.goals.title': 'הגדרת יעדים',
        'features.goals.desc': 'יעדים ומשימות שבועיות לשמירה על מיקוד וחגיגת הישגים.',
        'how.title': 'איך זה עובד',
        'how.step1.title': 'הרשמה',
        'how.step1.desc': 'מטפלים נרשמים עם הרישיון שלהם. מטופלים מצטרפים באמצעות קוד המטפל.',
        'how.step2.title': 'הגדרת פרופיל',
        'how.step2.desc': 'בחירת קטגוריות מעקב והגדרת יעדים ראשוניים למסע הבריאות.',
        'how.step3.title': 'צ׳ק-אין יומי',
        'how.step3.desc': 'מטופלים משלימים הערכות יומיות קצרות למעקב אחר ההתקדמות.',
        'how.step4.title': 'ניטור ותמיכה',
        'how.step4.desc': 'מטפלים סוקרים התקדמות, מוסיפים הערות ומתאימים תוכניות טיפול לפי הצורך.',
        'footer.copyright': '© 2024 מלווה טיפולי. תומכים במסעות בריאות עם אכפתיות וטכנולוגיה.'
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
        'nav.settings': 'Настройки',

        // Login Page
        'login.title': 'Вход в аккаунт',
        'login.email': 'Электронная почта',
        'login.password': 'Пароль',
        'login.forgot_password': 'Забыли пароль?',
        'login.remember_me': 'Запомнить меня',
        'login.no_account': 'Нет аккаунта?',
        'login.error': 'Неверный email или пароль',
        'login.welcome_back': 'С возвращением!',
        'login.instruction': 'Терапевты и клиенты могут войти здесь со своими учетными данными.',
        'login.forgot_coming_soon': 'Функция сброса пароля скоро появится!',

        // Password Reset
        'reset.title': 'Сброс пароля',
        'reset.instruction': 'Введите ваш адрес электронной почты, и мы отправим вам ссылку для сброса пароля.',
        'reset.email_label': 'Адрес электронной почты',
        'reset.send_link': 'Отправить ссылку',
        'reset.back_to_login': 'Вернуться к входу',
        'reset.success': 'Ссылка для сброса отправлена! Проверьте вашу почту.',
        'reset.error': 'Ошибка при отправке ссылки. Пожалуйста, попробуйте еще раз.',
        'reset.invalid_email': 'Пожалуйста, введите действительный адрес электронной почты',
        'reset.email_not_found': 'Адрес электронной почты не найден',
        'reset.new_password': 'Новый пароль',
        'reset.confirm_password': 'Подтвердите новый пароль',
        'reset.update_password': 'Обновить пароль',
        'reset.password_updated': 'Пароль успешно обновлен!',
        'reset.invalid_token': 'Недействительная или истекшая ссылка для сброса',

        // Registration
        'register.title': 'Создать аккаунт',
        'register.therapist': 'Регистрация терапевта',
        'register.full_name': 'Полное имя',
        'register.license': 'Номер лицензии',
        'register.organization': 'Организация',
        'register.confirm_password': 'Подтвердите пароль',
        'register.terms': 'Я согласен с условиями использования',
        'register.therapist_desc': 'Создайте свой профессиональный аккаунт, чтобы начать управлять клиентами.',
        'register.client_note_title': 'Примечание для клиентов:',
        'register.client_note_desc': 'Учетные записи клиентов должны быть созданы вашим терапевтом. Если вы клиент, используйте вкладку входа с учетными данными, предоставленными вашим терапевтом.',
        'register.license_note': 'Должен быть уникальным - каждая лицензия может быть зарегистрирована только один раз',
        'register.create_account': 'Создать аккаунт терапевта',
        'register.passwords_mismatch': 'Пароли не совпадают',
        'register.password_length': 'Пароль должен содержать не менее 8 символов',
        'register.license_exists': 'Этот номер лицензии уже зарегистрирован. Пожалуйста, используйте другой.',
        'register.email_exists': 'Этот email уже зарегистрирован. Пожалуйста, используйте вкладку входа.',

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

        'email.dear_therapist': 'المعالج العزيز',
        'email.weekly_report_intro': 'هذا هو تقرير التقدم الأسبوعي الخاص بي لـ',
        'email.report_generated_on': 'تم إنشاء التقرير في',
        'email.best_regards': 'مع أطيب التحيات',

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
        'reports.week': 'Неделя',
        'reports.daily_checkins': 'Ежедневные отметки',
        'reports.checkin_time': 'Время отметки',
        'reports.no_checkin': 'Нет отметки',
        'reports.weekly_summary': 'Недельная сводка',
        'reports.checkin_completion': 'Завершение отметок',
        'reports.completion_rate': 'Процент выполнения',
        'reports.completed': 'Выполнено',
        'reports.weekly_goals': 'Недельные цели',
        'reports.weekly_report_title': 'Недельный терапевтический отчет',

        // Messages
        'msg.success': 'Успешно!',
        'msg.error': 'Ошибка',
        'msg.loading': 'Загрузка...',
        'msg.saved': 'Изменения успешно сохранены',
        'msg.deleted': 'Успешно удалено',
        'msg.confirm_delete': 'Вы уверены, что хотите удалить?',
        'msg.no_data': 'Нет доступных данных',
        'msg.never': 'Никогда',
        'msg.login_success': 'Вход выполнен успешно! Перенаправление...',
        'msg.registration_success': 'Регистрация успешна! Выполняется вход...',
        'msg.network_error': 'Ошибка сети. Пожалуйста, попробуйте еще раз.',

        'email.dear_therapist': 'Уважаемый терапевт',
        'email.weekly_report_intro': 'Вот мой еженедельный отчет о прогрессе за',
        'email.report_generated_on': 'Отчет создан',
        'email.best_regards': 'С уважением',


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

            // Tracking Categories
            'category.emotion_level': 'Эмоциональный уровень',
            'category.emotion_level_desc': 'Общее эмоциональное состояние',
            'category.energy': 'Энергия',
            'category.energy_desc': 'Уровни физической и психической энергии',
            'category.social_activity': 'Социальная активность',
            'category.social_activity_desc': 'Участие в социальных взаимодействиях',
            'category.sleep_quality': 'Качество сна',
            'category.sleep_quality_desc': 'Качество сна',
            'category.anxiety_level': 'Уровень тревожности',
            'category.anxiety_level_desc': 'Уровень испытываемой тревоги',
            'category.motivation': 'Мотивация',
            'category.motivation_desc': 'Уровень мотивации и стремления',
            'category.medication': 'Лекарства',
            'category.medication_desc': 'Приверженность лечению',
            'category.physical_activity': 'Физическая активность',
            'category.physical_activity_desc': 'Уровень физической активности',

            // ... (rest of Russian translations remain the same)
        },

        ar: {
            // ... (Arabic translations remain the same, but add the password reset translations)
            // Password Reset
            'reset.title': 'إعادة تعيين كلمة المرور',
            'reset.instruction': 'أدخل عنوان بريدك الإلكتروني وسنرسل لك رابط إعادة تعيين كلمة المرور.',
            'reset.email_label': 'عنوان البريد الإلكتروني',
            'reset.send_link': 'إرسال الرابط',
            'reset.back_to_login': 'العودة لتسجيل الدخول',
            'reset.success': 'تم إرسال رابط إعادة التعيين! تحقق من بريدك الإلكتروني.',
            'reset.error': 'خطأ في إرسال الرابط. يرجى المحاولة مرة أخرى.',
            'reset.invalid_email': 'يرجى إدخال عنوان بريد إلكتروني صالح',
            'reset.email_not_found': 'عنوان البريد الإلكتروني غير موجود',
            'reset.new_password': 'كلمة المرور الجديدة',
            'reset.confirm_password': 'تأكيد كلمة المرور الجديدة',
            'reset.update_password': 'تحديث كلمة المرور',
            'reset.password_updated': 'تم تحديث كلمة المرور بنجاح!',
            'reset.invalid_token': 'رابط إعادة التعيين غير صالح أو منتهي الصلاحية',
               'reports.generate': 'إنشاء تقرير',
            'reports.weekly': 'تقرير أسبوعي',
            'reports.select_client': 'اختر العميل',
            'reports.select_week': 'اختر الأسبوع',
            'reports.excel': 'تحميل Excel',
            'reports.email': 'إرسال التقرير',
            'reports.week': 'الأسبوع',
            'reports.daily_checkins': 'تسجيلات الحضور اليومية',
            'reports.checkin_time': 'وقت تسجيل الحضور',
            'reports.no_checkin': 'لا يوجد تسجيل حضور',
            'reports.weekly_summary': 'الملخص الأسبوعي',
            'reports.checkin_completion': 'إكمال تسجيل الحضور',
            'reports.completion_rate': 'معدل الإنجاز',
            'reports.completed': 'مكتمل',
            'reports.weekly_goals': 'الأهداف الأسبوعية',
            'reports.weekly_report_title': 'التقرير العلاجي الأسبوعي',
            // ... (rest of Arabic translations)
        }
    },

    // Initialize i18n
    init() {
        console.log('i18n.init() called');

        // Set initial language from localStorage or browser
        const savedLang = localStorage.getItem('userLanguage');
        const browserLang = navigator.language.split('-')[0];

        if (savedLang && this.translations[savedLang]) {
            this.currentLang = savedLang;
        } else if (this.translations[browserLang]) {
            this.currentLang = browserLang;
        }

        console.log('Current language set to:', this.currentLang);

        // Apply RTL if needed
        this.applyRTL();

        // Force initialize language switcher after a short delay to ensure DOM is ready
        setTimeout(() => {
            console.log('Attempting to initialize language switcher...');
            this.initLanguageSwitcher();
        }, 100);

        // Translate page
        this.translatePage();
    },

    // Get translation
    t(key, replacements = {}) {
        const translation = this.translations[this.currentLang]?.[key] ||
                          this.translations.en[key] ||
                          key;

        // If no replacements, return translation as-is
        if (!replacements || Object.keys(replacements).length === 0) {
            return translation;
        }

        // Replace placeholders like {name} with values
        let result = translation;
        for (const [placeholder, value] of Object.entries(replacements)) {
            // Properly escape special regex characters
            const escapedPlaceholder = placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

            result = result.replace(new RegExp(`\\{${escapedPlaceholder}\\}`, 'g'), value);
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

        // Translate elements with data-i18n-placeholder
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.t(key);
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
        console.log('initLanguageSwitcher() called');

        // Remove any existing language switcher first
        const existing = document.getElementById('languageSwitcher');
        if (existing) {
            console.log('Removing existing language switcher');
            existing.remove();
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

        // Add styles if they don't exist
        if (!document.getElementById('i18n-styles')) {
            const style = document.createElement('style');
            style.id = 'i18n-styles';
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
        }

        // Add to page
        document.body.appendChild(switcher);
        console.log('Language switcher created and added to page');

        // If there's a backup switcher, hide it
        const backup = document.getElementById('languageSwitcherBackup');
        if (backup) {
            backup.style.display = 'none';
        }
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
    document.addEventListener('DOMContentLoaded', () => {
        console.log('DOM loaded, initializing i18n...');
        i18n.init();
    });
} else {
    console.log('DOM already loaded, initializing i18n immediately...');
    i18n.init();
}

// Export for use in other scripts
window.i18n = i18n;
