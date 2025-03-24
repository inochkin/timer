import streamlit as st
from datetime import datetime
import pytz
from database.db_init import db_settings, db_tasks
from lib.cookies import get_cookies_values_and_clear_cookies
from lib.static import NOT_COMPLETED, IN_PROGRESS, DONE, FORMAT_DATATIME


def handle_user_timezone():
    # ---------- check user Time Zone setting.
    curr_datetime_by_user_timezone, user_timezone = get_datetime_and_timezone_user()

    if not curr_datetime_by_user_timezone:
        st.warning("Please set up your Time Zone in the settings.")
        selector_timezone()
        if st.button("Save"):  # to refresh page.
            st.rerun()

        curr_date_by_user_timezone = None
        count_completed_tasks_today = 0
    else:
        curr_date_by_user_timezone = get_curr_date_by_user_timezone()
        count_completed_tasks_today = db_tasks.count_completed_tasks_today(curr_date_by_user_timezone)

    return user_timezone, curr_datetime_by_user_timezone, curr_date_by_user_timezone, count_completed_tasks_today


def save_task_to_db():
    hours_minutes, desc, priority, task_start_datetime, task_end_datetime = get_cookies_values_and_clear_cookies()
    if all([hours_minutes, desc, task_start_datetime, task_end_datetime]):
        # convert string to datetime obj.
        task_start_datetime = datetime.strptime(task_start_datetime, FORMAT_DATATIME)
        task_end_datetime = datetime.strptime(task_end_datetime, FORMAT_DATATIME)
        db_tasks.save_new_task_done(hours_minutes, desc, priority, task_start_datetime, task_end_datetime)


def selector_timezone():
    curr_user_timezone = db_settings.get_timezone_user()
    timezones = pytz.all_timezones

    if timezones[0] != "":
        timezones.insert(0, "")

    default_index = timezones.index(curr_user_timezone) if curr_user_timezone in timezones else 0
    selected_timezone = st.selectbox("Select your Time Zone:", timezones, index=default_index)

    if selected_timezone:
        db_settings.save_user_timezone(selected_timezone)


# Функция для окрашивания ячеек
def highlight_cells(key):
    if key == NOT_COMPLETED:
        return "background-color: grey; color: white;"
    elif key == IN_PROGRESS:
        return "background-color: aqua; color: white;"
    elif key == DONE:
        return "background-color: #afebaf; color: #3a3333;"
    else:
        return "background-color: yellow;"


def time_to_seconds(hours_minutes):
    hh, mm = map(int, hours_minutes.split(":"))
    return hh * 3600 + mm * 60


def get_datetime_and_timezone_user():
    user_timezone = db_settings.get_timezone_user()
    if user_timezone:
        curr_user_timezone_obj = pytz.timezone(user_timezone)
        return datetime.now(curr_user_timezone_obj), user_timezone


def get_curr_date_by_user_timezone():
    user_timezone = db_settings.get_timezone_user()
    if user_timezone:
        curr_user_timezone_obj = pytz.timezone(user_timezone)
        return datetime.now(curr_user_timezone_obj).date()

