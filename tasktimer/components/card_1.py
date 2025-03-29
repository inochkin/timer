import streamlit as st
from datetime import time
from custom.run_button import import_run_button_style
from database.db_init import db_users, db_tasks
from lib.static import OPTIONS_PRIORITY, LOW, get_priority_name


def card_1(next_step):
    # Поле для ввода часов и минут
    min_time_option = 15
    step_interval = 900

    min_time_user_setting = db_users.get_min_time_user()
    if min_time_user_setting:
        min_time_option = int(min_time_user_setting)
        step_interval = min_time_option * 60

    _, col2, _ = st.columns([1, 2, 1])
    with col2:

        st.title("Create Task")

        hours_minutes = st.time_input("Choose period time", time(0, min_time_option), step=step_interval)
        hours_minutes = hours_minutes.strftime("%H:%M")

        # -- Show detail options

        # default desc for task if user not set.
        count_completed_tasks_today = db_tasks.count_completed_tasks_today()
        desc = f'Task - {count_completed_tasks_today + 1}'

        priority = OPTIONS_PRIORITY[LOW]  # default

        if st.toggle("Show detail options"):
            with st.container():
                max_length = 300  # Максимальная длина текста
                desc = st.text_area("Task description", max_chars=max_length)
                st.session_state.desc_max_limit = False
                if len(desc) >= max_length:
                    st.warning(f"Max length of description is: {max_length}.")
                    st.session_state.desc_max_limit = True

                priority = st.radio("Set priority 👉", list(OPTIONS_PRIORITY.values()),
                                    format_func=lambda x: f"{x}. {get_priority_name(x)}")

        import_run_button_style()

        if st.button("Run"):
            # -- save fields
            st.session_state.hours_minutes = hours_minutes
            st.session_state.desc = desc
            st.session_state.priority = priority
            next_step()
