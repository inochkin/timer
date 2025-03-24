import streamlit as st
st.set_page_config(layout="centered")  # Устанавливает широкий макет

from lib.sidebar_custom import custom_sidebar
from custom.not_main_page_styles import import_not_main_page_styles
from database.db_init import db_settings
from lib.general_func import selector_timezone

import_not_main_page_styles()
custom_sidebar()

st.title("User settings")

# --- 1. Time Zone.
selector_timezone()


# --- 2 Min minutes to select for user.
list_min_options = ("", "02", "05", "10", "15")
min_time_user = db_settings.get_min_time_user()
default_index = list_min_options.index(min_time_user) if min_time_user in list_min_options else 0

min_minutes = st.selectbox("Set your min task time in minutes.", list_min_options, index=default_index)
if min_minutes:
    db_settings.save_user_min_time(min_minutes)

