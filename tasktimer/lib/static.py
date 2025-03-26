
# flag to test the app.
TEST_TIMER = True


APP_URL = 'http://localhost:8501'

# SMTP server - for send emails.
SMTP_EMAIL_SEND_FROM = "lettertomax@gmail.com"
SMTP_PASSWORD_FROM = "lxwe kyyt tgvu asug"  # genearte password in 'App password' setting.
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
# --------------------------------

USER_NAME = 'username'
USER_ID = 'user_id'
USER_EMAIL = 'user_email'
USER_AUTH_DATA_ENCRYPTED = 'user_auth_data'

FORMAT_DATATIME = '%Y-%m-%d %H:%M:%S'

NOT_COMPLETED = 'Not Completed'
IN_PROGRESS = 'In progress'
DONE = 'Done'
PAUSE = "Pause"

STATUS = {
    NOT_COMPLETED: 0,
    IN_PROGRESS: 1,
    DONE: 2,
    PAUSE: 3
}

def get_status_name(value):
    key = [key for key, val in STATUS.items() if val == value]
    return ''.join(key)


LOW = "🟤Low"
MIDDLE = "🟡Middle"
HIGH = "🟠High"

OPTIONS_PRIORITY = {
    LOW: 0,
    MIDDLE: 1,
    HIGH: 2
}


def get_priority_name(value):
    key = [key for key, val in OPTIONS_PRIORITY.items() if val == value]
    return ''.join(key)


# "hours_minutes", "desc", "priority", task_start_datetime, task_end_datetime
COOKIE_TASK_IS_CREATED = 'task_is_created'
COOKIE_HOURS_MINUTES = 'hours_minutes'
COOKIE_DESC = 'desc'
COOKIE_PRIORITY = 'priority'
COOKIE_TASK_START_DATETIME = 'task_start_datetime'
COOKIE_TASK_END_DATETIME = 'task_end_datetime'

