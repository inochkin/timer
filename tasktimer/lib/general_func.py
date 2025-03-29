import streamlit as st
from datetime import datetime
from database.db_init import db_tasks
from lib.cookies import get_cookies_task_values_and_clear_cookies
from lib.static import NOT_COMPLETED, IN_PROGRESS, DONE, FORMAT_DATATIME


def save_task_to_db():
    # to avoid saving 2 task to db.
    if "task_saved" not in st.session_state:
        st.session_state.task_saved = False

    if not st.session_state.task_saved:
        cookies_values = get_cookies_task_values_and_clear_cookies()
        if cookies_values:
            (hours_minutes, desc, priority, task_start_datetime, task_end_datetime) = cookies_values

            if all([hours_minutes, desc, task_start_datetime, task_end_datetime]):
                # convert string to datetime obj.
                task_start_datetime = datetime.strptime(task_start_datetime, FORMAT_DATATIME)
                task_end_datetime = datetime.strptime(task_end_datetime, FORMAT_DATATIME)
                db_tasks.save_new_task_done(hours_minutes, desc, priority, task_start_datetime, task_end_datetime)

                st.session_state.task_saved = True


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



