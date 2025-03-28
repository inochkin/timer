import streamlit as st
st.set_page_config(layout="centered")

from components.check_user_is_auth import user_is_authorised
from custom.sidebar import custom_sidebar
from components.card_1 import card_1
from components.card_2 import card_2
from custom.main_styles import import_main_styles
from lib.general_func import handle_user_timezone, save_task_to_db


import_main_styles()
custom_sidebar()


if user_is_authorised():

    # Используем session_state
    for key in ["hours_minutes", "desc", "priority"]:
        st.session_state.setdefault(key, None)

    # Используем session_state для отслеживания состояния контейнеров
    if "step" not in st.session_state:
        st.session_state.step = 1

    save_task_to_db()

    # ------------- timezone user -------------------
    data_db = handle_user_timezone()
    if not isinstance(data_db, tuple):
        user_timezone = None
        curr_date_by_user_timezone = None
        count_completed_tasks_today = 0
    else:
        # unpacking variables - TimeZone user handle
        (user_timezone, _, count_completed_tasks_today) = data_db

    # --------------------------------

    def next_step():
        st.session_state.step += 1
        st.rerun()


    # -- Card 1 (Create task)
    if st.session_state.step == 1:
        card_1(count_completed_tasks_today, next_step)


    # -- Card 2 (Run task)
    elif st.session_state.step == 2:
        card_2(user_timezone)

else:
    st.warning("Please login by your account.")


