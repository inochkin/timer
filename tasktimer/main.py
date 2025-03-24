import streamlit as st
st.set_page_config(layout="wide")  # Устанавливает широкий макет

from components.card_1 import card_1
from components.card_2 import card_2
from components.card_3 import card_3
from custom.main_styles import import_main_styles
from lib.general_func import handle_user_timezone, save_task_to_db


import_main_styles()


# Используем session_state
for key in ["hours_minutes", "desc", "priority"]:
    st.session_state.setdefault(key, None)


# unpacking variables - TimeZone user handle
(user_timezone, curr_datetime_by_user_timezone,
 curr_date_by_user_timezone, count_completed_tasks_today) = handle_user_timezone()


# ---
save_task_to_db()

# --------------------------------
# Используем session_state для отслеживания состояния контейнеров
if "step" not in st.session_state:
    st.session_state.step = 1


def next_step():
    st.session_state.step += 1
    st.rerun()


# -- Card 1
if st.session_state.step == 1:
    card_1(curr_datetime_by_user_timezone, next_step, count_completed_tasks_today,
           curr_date_by_user_timezone)


# -- Card 2
elif st.session_state.step == 2:
    card_2(count_completed_tasks_today, next_step)


# -- Card 3
elif st.session_state.step == 3:
    card_3(user_timezone)




