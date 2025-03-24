
# pip install streamlit-cookies-controller   - to work with cookies
from streamlit_cookies_controller import CookieController

from lib.static import COOKIE_TASK_END_DATETIME, COOKIE_TASK_START_DATETIME, \
    COOKIE_HOURS_MINUTES, COOKIE_DESC, COOKIE_PRIORITY

# controller = CookieController()  # !!need create only one obj CookieController.

# Set a cookie
# controller.set('cookie_name', 'testing')

# Get all cookies
# cookies = controller.getAll()

# Get a cookie
# cookie = controller.get('task')

# Remove a cookie
# controller.remove('cookie_name')



def _get_cookie(controller, name):
    return controller.get(name)


def _delete_cookie(controller, name):
    value = _get_cookie(controller, name)
    if value or value == 0:
        controller.remove(name)


def get_cookies_values_and_clear_cookies():
    cc = CookieController()  # !! need create only one obj CookieController..

    hours_minutes = _get_cookie(cc, COOKIE_HOURS_MINUTES)
    desc = _get_cookie(cc, COOKIE_DESC)
    priority = _get_cookie(cc, COOKIE_PRIORITY)
    task_start_datetime = _get_cookie(cc, COOKIE_TASK_START_DATETIME)
    task_end_datetime = _get_cookie(cc, COOKIE_TASK_END_DATETIME)

    # delete cookies.
    _delete_cookie(cc, COOKIE_HOURS_MINUTES)
    _delete_cookie(cc, COOKIE_DESC)
    _delete_cookie(cc, COOKIE_PRIORITY)
    _delete_cookie(cc, COOKIE_TASK_START_DATETIME)
    _delete_cookie(cc, COOKIE_TASK_END_DATETIME)

    return hours_minutes, desc, priority, task_start_datetime, task_end_datetime


