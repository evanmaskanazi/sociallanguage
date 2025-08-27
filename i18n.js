
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
        'login.success': 'Login Successful!',
        'login.password_requirements_update': 'Your password no longer meets security requirements. Please reset it.',

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
        'register.password_length': 'Password must be at least 12 characters long',
        'register.license_exists': 'This license number is already registered. Please use a different one.',
        'register.password_requirements': 'At least 12 characters with uppercase, lowercase, number and special character',
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
           'getting_started': 'Getting Started',
    '3_day_streak': '3-day streak',
    'week_warrior': 'Week Warrior',
    '7_day_streak': '7-day streak',
    'fortnight_focus': 'Fortnight Focus',
    '14_day_streak': '14-day streak',
    'monthly_master': 'Monthly Master',
    '30_day_streak': '30-day streak',
    'quarter_champion': 'Quarter Champion',
    '90_day_streak': '90-day streak',
    'perfect_week': 'Perfect Week',
    'completed_7_days': 'Completed all 7 days this week',
    'consistent_week': 'Consistent Week',
    'completed_5_days': 'Completed 5+ days this week',
    'first_steps': 'First Steps',
    'dedicated': 'Dedicated',
    'century': 'Century',
    'year_round': 'Year-Round',

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
        'client.password_requirements': 'Password must be at least 12 characters long.',
        'client.current_password': 'Current Password',
        'client.new_password': 'New Password',
        'client.confirm_new_password': 'Confirm New Password',
        'client.update_password': 'Update Password',
        'client.password_changed': 'Password changed successfully!',
        'client.passwords_dont_match': 'New passwords do not match',
        'client.password_too_short': 'Password must be at least 12 characters long',
        'client.incorrect_password': 'Current password is incorrect',
        'client.error_changing_password': 'Error changing password:',
        'therapist.generate_pdf': 'Generate PDF Report',
        'client.generate_pdf': 'Generate PDF Report',
        'client.add_goals': 'Add Goals',
        'client.save_goals': 'Save Goals',
        'client.goals_description_header': 'Goals Description',
         'client.goals_placeholder': 'Enter your goals for this week (500 words max)...',
         'client.no_goals_yet': 'No goals set for this week',
         'client.characters': 'characters',
         'client.goals_saved': 'Goals saved successfully!',
         'client.goals_empty': 'Please enter your goals',
         'client.goals_too_long': 'Goals description must be 500 words or less',
         'client.brief_goals_placeholder': 'Brief goals (20 words max)',
         'client.click_add_brief': 'Click to add brief goals',
         'client.brief_goals_saved': 'Brief goals saved successfully!',
         'client.brief_goals_too_long': 'Brief goals must be 20 words or less',
        'client.brief_goals_label': 'Brief Description:',



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
        'nav.daily_checkin': 'Daily Check-in',
        'nav.consent': 'Consent',
        'email.unsubscribe_text': 'To unsubscribe, click',
        'email.unsubscribe_here': 'here',






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
        'footer.copyright': '© 2024 Therapeutic Companion. Supporting wellness journeys with care and technology.',
        'days': 'days'
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
            'getting_started': 'מתחילים',
    '3_day_streak': 'רצף של 3 ימים',
    'week_warrior': 'לוחם השבוע',
    '7_day_streak': 'רצף של 7 ימים',
    'fortnight_focus': 'מיקוד דו-שבועי',
    '14_day_streak': 'רצף של 14 ימים',
    'monthly_master': 'אמן החודש',
    '30_day_streak': 'רצף של 30 ימים',
    'quarter_champion': 'אלוף הרבעון',
    '90_day_streak': 'רצף של 90 ימים',
    'perfect_week': 'שבוע מושלם',
    'completed_7_days': 'השלמת כל 7 הימים השבוע',
    'consistent_week': 'שבוע עקבי',
    'completed_5_days': 'השלמת 5+ ימים השבוע',
    'first_steps': 'צעדים ראשונים',
    'dedicated': 'מסור',
    'century': 'מאה',
    'year_round': 'לאורך השנה',

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
        'login.success': 'הכניסה מוצלחת',
        'login.password_requirements_update': 'הסיסמה שלך אינה עומדת יותר בדרישות האבטחה. אנא אפס אותה.',

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
        'days': 'ימים',

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
        'register.password_length': 'הסיסמה חייבת להיות באורך של לפחות 12 תווים',
        'register.license_exists': 'מספר רישיון זה כבר רשום. אנא השתמש במספר אחר.',
         'register.password_requirements': 'לפחות 12 תווים עם אותיות גדולות, קטנות, מספר ותו מיוחד',
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
        'client.add_goals': 'הוסף יעדים',
         'client.save_goals': 'שמור יעדים',
         'client.goals_description_header': 'תיאור יעדים',
         'client.goals_placeholder': 'הזן את היעדים שלך לשבוע זה (מקסימום 500 מילים)...',
         'client.no_goals_yet': 'לא נקבעו יעדים לשבוע זה',
        'client.characters': 'תווים',
        'client.goals_saved': 'היעדים נשמרו בהצלחה!',
        'client.goals_empty': 'אנא הזן את היעדים שלך',
        'client.goals_too_long': 'תיאור היעדים חייב להיות עד 500 מילים',
        'client.brief_goals_placeholder': 'יעדים בקצרה (מקסימום 20 מילים)',
        'client.click_add_brief': 'לחץ להוספת יעדים בקצרה',
        'client.brief_goals_saved': 'היעדים בקצרה נשמרו בהצלחה!',
        'client.brief_goals_too_long': 'יעדים בקצרה חייבים להיות עד 20 מילים',
        'client.brief_goals_label': 'תיאור קצר:',

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
        'client.password_requirements': 'הסיסמה חייבת להיות באורך של לפחות 12 תווים.',
        'client.current_password': 'סיסמה נוכחית',
        'client.new_password': 'סיסמה חדשה',
        'client.confirm_new_password': 'אשר סיסמה חדשה',
        'client.update_password': 'עדכן סיסמה',
        'client.password_changed': 'הסיסמה שונתה בהצלחה!',
        'client.passwords_dont_match': 'הסיסמאות החדשות אינן תואמות',
        'client.password_too_short': 'הסיסמה חייבת להיות באורך של לפחות  12 תווים',
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
        'therapist.generate_pdf': 'צור דוח PDF',
        'client.generate_pdf': 'צור דוח PDF',
        'nav.daily_checkin': 'צ׳ק-אין יומי',
        'nav.consent': 'הסכמה',
        'email.unsubscribe_text': 'להפסקת הרישום, לחץ',
        'email.unsubscribe_here': 'כאן',

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
            'getting_started': 'Начало пути',
    '3_day_streak': '3-дневная серия',
    'week_warrior': 'Воин недели',
    '7_day_streak': '7-дневная серия',
    'fortnight_focus': 'Двухнедельный фокус',
    '14_day_streak': '14-дневная серия',
    'monthly_master': 'Мастер месяца',
    '30_day_streak': '30-дневная серия',
    'quarter_champion': 'Чемпион квартала',
    '90_day_streak': '90-дневная серия',
    'perfect_week': 'Идеальная неделя',
    'completed_7_days': 'Выполнены все 7 дней на этой неделе',
    'consistent_week': 'Последовательная неделя',
    'completed_5_days': 'Выполнено 5+ дней на этой неделе',
    'first_steps': 'Первые шаги',
    'dedicated': 'Преданный делу',
    'century': 'Столетие',
    'year_round': 'Круглый год',

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
        'login.success': 'Вход выполнен успешно!',
        'login.password_requirements_update': 'Ваш пароль больше не соответствует требованиям безопасности. Пожалуйста, сбросьте его.',

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
        'register.password_length': 'Пароль должен содержать не менее 12 символов',
        'register.license_exists': 'Этот номер лицензии уже зарегистрирован. Пожалуйста, используйте другой.',
        'register.email_exists': 'Этот email уже зарегистрирован. Пожалуйста, используйте вкладку входа.',
        'register.password_requirements': 'Не менее 12 символов с заглавными, строчными буквами, цифрой и специальным символом',
        'days': 'дней',

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
        'therapist.generate_pdf': 'Создать PDF отчет',
        'client.generate_pdf': 'Создать PDF отчет',
        'nav.daily_checkin': 'Ежедневная отметка',
        'client.add_goals': 'Добавить цели',
        'client.save_goals': 'Сохранить цели',
        'client.goals_description_header': 'Описание целей',
        'client.goals_placeholder': 'Введите ваши цели на эту неделю (максимум 500 слов)...',
        'client.no_goals_yet': 'Цели на эту неделю не установлены',
        'client.characters': 'символов',
        'client.goals_saved': 'Цели успешно сохранены!',
        'client.goals_empty': 'Пожалуйста, введите ваши цели',
        'client.goals_too_long': 'Описание целей должно быть не более 500 слов',
        'client.brief_goals_placeholder': 'Краткие цели (максимум 20 слов)',
        'client.click_add_brief': 'Нажмите, чтобы добавить краткие цели',
        'client.brief_goals_saved': 'Краткие цели успешно сохранены!',
        'client.brief_goals_too_long': 'Краткие цели должны быть не более 20 слов',
        'client.brief_goals_label': 'Краткое описание:',


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
        'email.unsubscribe_text': 'Чтобы отписаться, нажмите',
        'email.unsubscribe_here': 'здесь',



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
            'email.dear_therapist': 'المعالج العزيز',
            'email.weekly_report_intro': 'هذا هو تقرير التقدم الأسبوعي الخاص بي لـ',
            'email.report_generated_on': 'تم إنشاء التقرير في',
            'email.best_regards': 'مع أطيب التحيات',
            'getting_started': 'البداية',
    '3_day_streak': 'سلسلة 3 أيام',
    'week_warrior': 'محارب الأسبوع',
    '7_day_streak': 'سلسلة 7 أيام',
    'fortnight_focus': 'تركيز الأسبوعين',
    '14_day_streak': 'سلسلة 14 يوم',
    'monthly_master': 'بطل الشهر',
    '30_day_streak': 'سلسلة 30 يوم',
    'quarter_champion': 'بطل الربع السنوي',
    '90_day_streak': 'سلسلة 90 يوم',
    'perfect_week': 'أسبوع مثالي',
    'completed_7_days': 'أكملت جميع الأيام السبعة هذا الأسبوع',
    'consistent_week': 'أسبوع متسق',
    'completed_5_days': 'أكملت 5 أيام أو أكثر هذا الأسبوع',
    'first_steps': 'الخطوات الأولى',
    'dedicated': 'مكرس',
    'century': 'قرن',
    'year_round': 'على مدار السنة',
            'days': 'أيام',
            'day.monday': 'الاثنين',
            'day.tuesday': 'الثلاثاء',
            'day.wednesday': 'الأربعاء',
'day.thursday': 'الخميس',
'day.friday': 'الجمعة',
'day.saturday': 'السبت',
            'day.sunday': 'الأحد',
            'day.mon': 'اث',
            'day.tue': 'ث',
            'day.wed': 'أر',
            'day.thu': 'خ',
            'day.fri': 'ج',
            'day.sat': 'س',
            'day.sun': 'أح',
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
    'nav.settings': 'الإعدادات',

    // Login Page
    'login.title': 'تسجيل الدخول إلى حسابك',
    'login.email': 'البريد الإلكتروني',
    'login.password': 'كلمة المرور',
    'login.forgot_password': 'نسيت كلمة المرور؟',
    'login.remember_me': 'تذكرني',
    'login.no_account': "ليس لديك حساب؟",
    'login.error': 'البريد الإلكتروني أو كلمة المرور غير صحيحة',
    'login.welcome_back': 'مرحباً بعودتك!',
    'login.instruction': 'يمكن للمعالجين والعملاء تسجيل الدخول هنا باستخدام بيانات الاعتماد الخاصة بهم.',
    'login.forgot_coming_soon': 'وظيفة إعادة تعيين كلمة المرور قادمة قريباً!',
          'login.success': 'تم تسجيل الدخول بنجاح!',
          'login.password_requirements_update': 'كلمة المرور الخاصة بك لم تعد تفي بمتطلبات الأمان. يرجى إعادة تعيينها.',
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

    // Registration
    'register.title': 'إنشاء حساب',
    'register.therapist': 'تسجيل المعالج',
    'register.full_name': 'الاسم الكامل',
    'register.license': 'رقم الترخيص',
    'register.organization': 'المنظمة',
    'register.confirm_password': 'تأكيد كلمة المرور',
    'register.terms': 'أوافق على شروط الخدمة',
    'register.therapist_desc': 'أنشئ حسابك المهني لبدء إدارة العملاء.',
    'register.client_note_title': 'ملاحظة للعملاء:',
    'register.client_note_desc': 'يجب أن يتم إنشاء حسابات العملاء بواسطة المعالج الخاص بك. إذا كنت عميلاً، يرجى استخدام علامة تبويب تسجيل الدخول مع بيانات الاعتماد المقدمة من معالجك.',
    'register.license_note': 'يجب أن يكون فريداً - يمكن تسجيل كل ترخيص مرة واحدة فقط',
    'register.create_account': 'إنشاء حساب المعالج',
    'register.passwords_mismatch': 'كلمات المرور غير متطابقة',
    'register.password_length': 'يجب أن تتكون كلمة المرور من 12 أحرف على الأقل',
    'register.license_exists': 'رقم الترخيص هذا مسجل بالفعل. يرجى استخدام رقم آخر.',
    'register.password_requirements': 'على الأقل 12 حرفًا مع أحرف كبيرة وصغيرة ورقم ورمز خاص',
    'register.email_exists': 'هذا البريد الإلكتروني مسجل بالفعل. يرجى استخدام علامة تبويب تسجيل الدخول.',

    // Dashboard
    'dashboard.welcome': 'مرحباً',
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
    'checkin.emotional': 'كيف هو حالك العاطفية؟',
    'checkin.medication': 'هل تناولت دواءك كما هو موصوف؟',
    'checkin.activity': 'كم كنت نشيطاً؟',
    'checkin.notes': 'ملاحظات إضافية (اختياري)',
    'checkin.scale_1': 'سيء جداً',
    'checkin.scale_2': 'سيء',
    'checkin.scale_3': 'معتدل',
    'checkin.scale_4': 'جيد',
    'checkin.scale_5': 'ممتاز',
    'checkin.med_yes': 'نعم',
    'checkin.med_no': 'لا',
    'checkin.med_partial': 'جزئي',
    'checkin.med_na': 'غير متاح',
    'therapist.generate_pdf': 'إنشاء تقرير PDF',
    'client.generate_pdf': 'إنشاء تقرير PDF',
    'email.unsubscribe_text': 'لإلغاء الاشتراك، انقر',
'email.unsubscribe_here': 'هنا',


    // Goals
    'goals.weekly': 'الأهداف الأسبوعية',
    'goals.add': 'إضافة هدف جديد',
    'goals.completed': 'مكتمل',
    'goals.pending': 'معلق',
    'goals.text': 'وصف الهدف',

    // Reports and other sections continue...
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

    // Messages
    'msg.success': 'نجح!',
    'msg.error': 'خطأ',
    'msg.loading': 'جاري التحميل...',
    'msg.saved': 'تم حفظ التغييرات بنجاح',
    'msg.deleted': 'تم الحذف بنجاح',
    'msg.confirm_delete': 'هل أنت متأكد أنك تريد الحذف؟',
    'msg.no_data': 'لا توجد بيانات متاحة',
    'msg.never': 'أبداً',
    'msg.login_success': 'تم تسجيل الدخول بنجاح! جاري التحويل...',
    'msg.registration_success': 'تم التسجيل بنجاح! جاري تسجيل دخولك...',
    'msg.network_error': 'خطأ في الشبكة. يرجى المحاولة مرة أخرى.',
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

// Client specific translations
'client.dashboard_title': 'رحلتي العلاجية',
'client.encouragement': 'رحلتك نحو العافية مستمرة. كل خطوة مهمة!',
'client.morning_message': 'ابدأ يومك بعقلية إيجابية!',
'client.afternoon_message': 'استمر في العمل الرائع اليوم!',
'client.evening_message': 'حان الوقت للتفكير في يومك والراحة جيداً.',
'client.previous_week': '→ الأسبوع السابق',
'client.next_week': 'الأسبوع القادم ←',
'client.quick_stats': 'إحصائيات سريعة',
'client.week_goals': 'أهداف هذا الأسبوع',
'client.select_date': 'اختر التاريخ:',
'client.checkin_intro': 'خذ لحظة للتفكير في يومك. إجاباتك تساعد في تتبع تقدمك.',
'client.notes_placeholder': 'أي أفكار حول {category}؟ (اختياري)',
'client.submit_checkin': 'إرسال تسجيل الحضور',
'client.clear_form': 'مسح',
'client.select_week': 'اختر الأسبوع:',
'client.load_goals': 'تحميل الأهداف',
'client.select_week_goals': 'اختر أسبوعاً لعرض الأهداف',
'client.your_progress': 'تقدمك',
'client.view_progress': 'عرض التقدم:',
'client.last_7_days': 'آخر 7 أيام',
'client.last_30_days': 'آخر 30 يوماً',
'client.last_90_days': 'آخر 90 يوماً',
'client.update': 'تحديث',
'client.loading_progress': 'جاري تحميل بيانات التقدم...',
'client.report_desc': 'أنشئ تقريراً شاملاً لتسجيلات حضورك لأي أسبوع.',
'client.generate_excel': 'إنشاء تقرير Excel',
'client.prepare_email': 'إعداد تقرير البريد الإلكتروني',
'client.report_status': 'حالة التقرير',
'client.no_checkin': 'لا يوجد تسجيل حضور',
'client.today_marker': '(اليوم)',
'client.past_date': '(تاريخ سابق)',
'client.future_date': '(تاريخ مستقبلي)',
'client.complete_ratings': 'يرجى إكمال جميع التقييمات المطلوبة',
'client.no_goals_week': 'لا توجد أهداف محددة لهذا الأسبوع',
'client.total_checkins': 'إجمالي تسجيلات الحضور:',
'client.avg_emotional': 'متوسط التقييم العاطفي:',
'client.medication_adherence': 'الالتزام بالأدوية:',
'client.avg_activity': 'متوسط مستوى النشاط:',
'client.email_preview': 'معاينة تقرير البريد الإلكتروني',
'client.copy_email': 'انسخ هذا المحتوى لإرساله إلى معالجك',
'client.checkin_success': 'تم إرسال تسجيل الحضور بنجاح! 🎉',
'client.checkin_error': 'لا يمكن إرسال تسجيل الحضور للتواريخ المستقبلية',
'client.select_client_week': 'يرجى اختيار أسبوع',
'client.report_generated': 'تم إنشاء التقرير وتنزيله بنجاح!',
'client.error_progress': 'خطأ في تحميل بيانات التقدم',
'client.account_settings': 'إعدادات الحساب',
'client.change_password': 'تغيير كلمة المرور',
'client.password_requirements': 'يجب أن تتكون كلمة المرور من 12 أحرف على الأقل.',
'client.current_password': 'كلمة المرور الحالية',
'client.new_password': 'كلمة المرور الجديدة',
'client.confirm_new_password': 'تأكيد كلمة المرور الجديدة',
'client.update_password': 'تحديث كلمة المرور',
'client.password_changed': 'تم تغيير كلمة المرور بنجاح!',
'client.passwords_dont_match': 'كلمات المرور الجديدة غير متطابقة',
'client.password_too_short': 'يجب أن تتكون كلمة المرور من 12 أحرف على الأقل',
'client.incorrect_password': 'كلمة المرور الحالية غير صحيحة',
'client.error_changing_password': 'خطأ في تغيير كلمة المرور:',
'client.add_goals': 'إضافة أهداف',
'client.save_goals': 'حفظ الأهداف',
'client.goals_description_header': 'وصف الأهداف',
'client.goals_placeholder': 'أدخل أهدافك لهذا الأسبوع (500 كلمة كحد أقصى)...',
'client.no_goals_yet': 'لم يتم تحديد أهداف لهذا الأسبوع',
'client.characters': 'أحرف',
'client.goals_saved': 'تم حفظ الأهداف بنجاح!',
'client.goals_empty': 'يرجى إدخال أهدافك',
'client.goals_too_long': 'يجب أن يكون وصف الأهداف 500 كلمة أو أقل',
'client.brief_goals_placeholder': 'أهداف موجزة (20 كلمة كحد أقصى)',
'client.click_add_brief': 'انقر لإضافة أهداف موجزة',
'client.brief_goals_saved': 'تم حفظ الأهداف الموجزة بنجاح!',
'client.brief_goals_too_long': 'يجب أن تكون الأهداف الموجزة 20 كلمة أو أقل',
'client.brief_goals_label': 'وصف موجز:',



// Therapist specific translations
'therapist.dashboard_title': 'لوحة تحكم المعالج',
'therapist.dashboard_overview': 'نظرة عامة على لوحة التحكم',
'therapist.checkins_week': 'تسجيلات الحضور هذا الأسبوع',
'therapist.recent_activity': 'النشاط الأخير',
'therapist.loading_activity': 'جاري تحميل النشاط الأخير...',
'therapist.client_management': 'إدارة العملاء',
'therapist.search_placeholder': 'البحث بالرقم التسلسلي أو التاريخ...',
'therapist.all_clients': 'جميع العملاء',
'therapist.active_only': 'النشطون فقط',
'therapist.inactive_only': 'غير النشطين فقط',
'therapist.add_new_client': 'إضافة عميل جديد',
'therapist.week_completion': 'إكمال الأسبوع',
'therapist.loading_clients': 'جاري تحميل العملاء...',
'therapist.client_account_info': 'معلومات حساب العميل',
'therapist.email_required': 'البريد الإلكتروني*',
'therapist.temp_password': 'كلمة مرور مؤقتة (اختياري)',
'therapist.auto_generate_note': 'اتركه فارغاً للإنشاء التلقائي',
'therapist.tracking_categories': 'فئات التتبع',
'therapist.select_categories': 'اختر الفئات التي سيتتبعها هذا العميل:',
'therapist.all_categories_note': 'ملاحظة: جميع الفئات محددة افتراضياً. قم بإلغاء تحديد أي فئة لا تريد أن يتتبعها العميل.',
'therapist.initial_goals': 'الأهداف الأولية (اختياري)',
'therapist.setup_goals': 'حدد ما يصل إلى 5 أهداف أسبوعية أولية للعميل:',
'therapist.goal_placeholder': 'الهدف 1 (مثال: المشي لمدة 15 دقيقة يومياً)',
'therapist.add_another_goal': '+ إضافة هدف آخر',
'therapist.create_client_btn': 'إنشاء حساب العميل',
'therapist.client_reports': 'تقارير العملاء',
'therapist.generate_weekly_report': 'إنشاء تقرير أسبوعي',
'therapist.select_client_option': 'اختر عميلاً...',
'therapist.generate_excel': 'إنشاء تقرير Excel',
'therapist.prepare_email': 'إعداد تقرير البريد الإلكتروني',
'therapist.report_status': 'حالة التقرير',
'therapist.client_details': 'تفاصيل العميل',
'therapist.no_clients': 'لم يتم العثور على عملاء. أضف عميلك الأول للبدء.',
'therapist.license': 'الترخيص',
'therapist.activity_coming_soon': 'ميزة النشاط الأخير قادمة قريباً',
'therapist.check_clients_tab': 'تحقق من علامة تبويب العملاء لعرض تقدم العميل الفردي',
'therapist.max_goals': 'يمكن إضافة 5 أهداف كحد أقصى في البداية',
'therapist.please_enter_email': 'يرجى إدخال بريد إلكتروني العميل',
'therapist.client_created': 'تم إنشاء العميل بنجاح!',
'therapist.serial': 'الرقم التسلسلي',
'therapist.email': 'البريد الإلكتروني',
'therapist.temp_password_label': 'كلمة مرور مؤقتة',
'therapist.save_credentials': 'يرجى حفظ بيانات الاعتماد هذه للعميل. ستبقى هذه الرسالة مرئية حتى تغادر علامة التبويب هذه.',
'therapist.goal_added': 'تمت إضافة الهدف بنجاح!',
'therapist.enter_goal': 'أدخل الهدف لهذا الأسبوع:',
'therapist.note_added': 'تمت إضافة الملاحظة بنجاح!',
'therapist.please_enter_note': 'يرجى إدخال ملاحظة',
'therapist.mark_as_mission': 'وضع علامة كمهمة',
'therapist.this_week_progress': 'تقدم هذا الأسبوع',
'therapist.select_both': 'يرجى اختيار كل من العميل والأسبوع',
'therapist.generating_report': 'جاري إنشاء التقرير...',
'therapist.report_downloaded': 'تم تنزيل التقرير بنجاح!',
'therapist.preparing_email': 'جاري إعداد تقرير البريد الإلكتروني...',
'therapist.email_prepared': 'تم إعداد تقرير البريد الإلكتروني! راجع المعاينة أدناه.',
'therapist.error_loading': 'خطأ في تحميل لوحة التحكم:',
'therapist.error_creating': 'خطأ في إنشاء العميل:',
'therapist.error_adding_goal': 'خطأ في إضافة الهدف:',
'therapist.error_adding_note': 'خطأ في إضافة الملاحظة:',
'therapist.error_loading_details': 'خطأ في تحميل تفاصيل العميل:',
'therapist.error_generating': 'خطأ في إنشاء التقرير:',
'therapist.error_preparing': 'خطأ في إعداد تقرير البريد الإلكتروني:',
'therapist.to': 'إلى',
'therapist.subject': 'الموضوع',
'therapist.email_preview': 'معاينة تقرير البريد الإلكتروني',
'therapist.copy_email_note': 'انسخ هذا المحتوى لإرساله عبر بريدك الإلكتروني',
'therapist.started': 'بدأ',
'therapist.client_info': 'معلومات العميل',
'therapist.week_progress': 'تقدم هذا الأسبوع',
'therapist.active_goals': 'الأهداف النشطة',
'therapist.no_active_goals': 'لا توجد أهداف نشطة لهذا الأسبوع',
'therapist.add_note_mission': 'إضافة ملاحظة أو مهمة',
'therapist.enter_note_placeholder': 'أدخل ملاحظتك أو مهمتك...',
'therapist.recent_notes': 'الملاحظات والمهام الأخيرة',
'therapist.mission': 'مهمة',
'therapist.no_notes': 'لا توجد ملاحظات بعد',
'nav.daily_checkin': 'تسجيل الحضور اليومي',
'nav.consent': 'الموافقة',

// Index page translations
'hero.subtitle': 'نظام رفيق علاجي شامل للمعالجين والعملاء',
'hero.get_started': 'ابدأ الآن',
'hero.learn_more': 'اعرف المزيد',
'features.title': 'ميزات للجميع',
'features.therapists.title': 'للمعالجين',
'features.therapists.desc': 'إدارة عملاء متعددين، وتتبع التقدم، وتحديد الأهداف، وإنشاء تقارير شاملة - كل ذلك في منصة واحدة آمنة.',
'features.clients.title': 'للعملاء',
'features.clients.desc': 'تسجيلات يومية، وتتبع المزاج، وإكمال الأهداف، وتذكيرات لطيفة لدعم رحلة صحتك النفسية.',
'features.tracking.title': 'تتبع التقدم',
'features.tracking.desc': 'رؤى بصرية حول الأنماط العاطفية والالتزام بالأدوية والنشاط البدني بمرور الوقت.',
'features.security.title': 'آمن وخاص',
'features.security.desc': 'بياناتك محمية بالتشفير وفقاً لمعايير الصناعة وضوابط خصوصية صارمة.',
'features.accessible.title': 'يمكن الوصول إليه من أي مكان',
'features.accessible.desc': 'استخدمه على أي جهاز - سطح المكتب أو الجهاز اللوحي أو الهاتف المحمول - للبقاء على اتصال برحلة عافيتك.',
'features.goals.title': 'تحديد الأهداف',
'features.goals.desc': 'أهداف ومهام أسبوعية للحفاظ على التركيز والاحتفال بالإنجازات.',
'how.title': 'كيف يعمل',
'how.step1.title': 'التسجيل',
'how.step1.desc': 'يسجل المعالجون بترخيصهم. ينضم العملاء باستخدام رمز معالجهم.',
'how.step2.title': 'إعداد الملف الشخصي',
'how.step2.desc': 'اختر فئات التتبع وحدد الأهداف الأولية لرحلة العافية.',
'how.step3.title': 'تسجيلات يومية',
'how.step3.desc': 'يكمل العملاء تقييمات يومية موجزة لتتبع تقدمهم.',
'how.step4.title': 'المراقبة والدعم',
'how.step4.desc': 'يراجع المعالجون التقدم ويضيفون الملاحظات ويعدلون خطط العلاج حسب الحاجة.',
'footer.copyright': '© 2024 الرفيق العلاجي. دعم رحلات العافية بالرعاية والتكنولوجيا.'
            // ... (rest of Arabic translations)
        }
    },

    // Initialize i18n
    init() {
    console.log('i18n.init() called');

    // Get language from cookie first
    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    };

    const cookieLang = getCookie('preferred_language');
    const savedLang = localStorage.getItem('userLanguage');
    const browserLang = navigator.language.split('-')[0];

    if (cookieLang && this.translations[cookieLang]) {
        this.currentLang = cookieLang;
        localStorage.setItem('userLanguage', cookieLang); // Sync with localStorage
    } else if (savedLang && this.translations[savedLang]) {
        this.currentLang = savedLang;
    } else if (this.translations[browserLang]) {
        this.currentLang = browserLang;
    } else {
        // Fallback to English if no match
        this.currentLang = 'en';
    }

    console.log('Current language set to:', this.currentLang);

    // Apply RTL if needed
    this.applyRTL();

     // Translate page first
     // Initialize language switcher first
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            this.initLanguageSwitcher();
            this.translatePage(); // Translate after DOM is ready
        });
    } else {
        // DOM is already loaded
        this.initLanguageSwitcher();
        this.translatePage();
    }
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

        setLanguage(lang) {
    if (this.translations[lang]) {
        this.currentLang = lang;
        localStorage.setItem('userLanguage', lang);
        // Also set a cookie for cross-page persistence
        document.cookie = `preferred_language=${lang};path=/;max-age=${60*60*24*365}`;
        this.applyRTL();
        this.translatePage();

        // Update language switcher
        const switcher = document.getElementById('languageSwitcher');
        if (switcher) {
            switcher.value = lang;
        }

        // Reinitialize language switcher to update position for RTL
        this.initLanguageSwitcher();

        window.dispatchEvent(new Event('languageChanged'));
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
       // Translate entire page
    translatePage() {
        console.log('=== translatePage called ===');
        console.log('Current language:', this.currentLang);
        console.log('Document ready state:', document.readyState);

        // Count elements before translation
        const elementsWithDataI18n = document.querySelectorAll('[data-i18n]');
        console.log('Elements with data-i18n found:', elementsWithDataI18n.length);

        // Show first few elements
        elementsWithDataI18n.forEach((element, index) => {
            if (index < 5) {
                console.log(`Element ${index}:`, element.tagName, 'data-i18n=', element.getAttribute('data-i18n'), 'current text=', element.textContent);
            }
        });

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

        console.log('=== translatePage completed ===');
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
        // Force selection for current language
        if (lang.code === this.currentLang) {
            option.selected = true;
        }
        switcher.appendChild(option);
    });

    // Double-check the selected value after all options are added
    if (switcher.value !== this.currentLang) {
        console.warn('Language switcher value mismatch. Expected:', this.currentLang, 'Got:', switcher.value);
        // Force set it again
        Array.from(switcher.options).forEach(option => {
            option.selected = (option.value === this.currentLang);
        });
    }


    // Add change event
    switcher.addEventListener('change', (e) => {
        this.setLanguage(e.target.value);
    });

    // Add or update styles
    let styleElement = document.getElementById('i18n-styles');
    if (!styleElement) {
        styleElement = document.createElement('style');
        styleElement.id = 'i18n-styles';
        document.head.appendChild(styleElement);
    }

    // Update styles with current language direction
    styleElement.textContent = `
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
        // Force a re-translation after a short delay to catch any late-loading elements
        setTimeout(() => {
            if (i18n.currentLang !== 'en') {
                console.log('Re-translating page to:', i18n.currentLang);
                i18n.translatePage();
            }
        }, 500);
    });
} else {
    console.log('DOM already loaded, initializing i18n immediately...');
    i18n.init();
    // Force a re-translation after a short delay to catch any late-loading elements
    setTimeout(() => {
        if (i18n.currentLang !== 'en') {
            console.log('Re-translating page to:', i18n.currentLang);
            i18n.translatePage();
        }
    }, 500);
}

// Export for use in other scripts
window.i18n = i18n;
